"""Transformers-based recognizers (extra: `hf`).

- hf-whisper: multilingual Whisper checkpoints (S66-S70). Never use `.en` checkpoints.
- hf-ctc: wav2vec2 / XLS-R / HuBERT checkpoints *with* a CTC head (S49). A bare pretrained
  encoder has no transcript head and cannot transcribe (S47, S88).
"""

from __future__ import annotations

import numpy as np

from .base import Recognizer

_DTYPES = {"float16": "float16", "fp16": "float16", "bfloat16": "bfloat16", "bf16": "bfloat16",
           "float32": "float32", "fp32": "float32"}


def _torch_dtype(name: str):
    import torch
    return getattr(torch, _DTYPES[name])


def split_at_pauses(audio: np.ndarray, sr: int, max_seconds: float) -> list[np.ndarray]:
    """Split a clip into pieces of at most `max_seconds`, cutting at the quietest point (200 ms smoothed frame
    energy) within the last 40 % of each piece. Clips that fit are returned whole. Used for Whisper on languages
    whose transcripts overflow the 448-token decoder budget (Georgian: ~30 tokens per second of speech)."""
    limit = int(max_seconds * sr)
    if len(audio) <= limit:
        return [audio]
    hop, win = int(0.01 * sr), int(0.025 * sr)
    n = max(1, (len(audio) - win) // hop + 1)
    frames = np.lib.stride_tricks.sliding_window_view(audio[: (n - 1) * hop + win], win)[::hop]
    energy = np.convolve((frames.astype(np.float64) ** 2).sum(axis=1), np.ones(20) / 20, mode="same")
    pieces, start = [], 0
    while len(audio) - start > limit:
        lo, hi = (start + int(0.6 * limit)) // hop, min((start + limit - win) // hop, n - 1)
        cut = (lo + int(np.argmin(energy[lo:hi + 1]))) * hop + win // 2 if hi > lo else start + limit
        pieces.append(audio[start:cut])
        start = cut
    pieces.append(audio[start:])
    return pieces


class HFWhisper(Recognizer):
    family = "hf-whisper"
    WINDOW_SECONDS = 30

    def load(self) -> None:
        if self.model_id.endswith(".en"):
            raise ValueError(f"{self.model_id} is English-only; use a multilingual checkpoint (S69).")
        from transformers import WhisperForConditionalGeneration, WhisperProcessor
        self.processor = WhisperProcessor.from_pretrained(self.model_id, revision=self.revision)
        self.model = WhisperForConditionalGeneration.from_pretrained(
            self.model_id, revision=self.revision, dtype=_torch_dtype(self.dtype)
        ).to(self.device).eval()

    def transcribe(self, audios: list[np.ndarray], language: str) -> list[str]:
        chunk = float(self.settings.get("chunk_seconds") or 0)
        if chunk:  # decoding policy: split long clips at low-energy points, decode pieces, join with a space
            pieces, owner = [], []
            for i, a in enumerate(audios):
                for p in split_at_pauses(a, self.sample_rate, chunk):
                    pieces.append(p)
                    owner.append(i)
            texts = self._transcribe(pieces, language)
            out = [[] for _ in audios]
            for i, t in zip(owner, texts):
                if t:
                    out[i].append(t)
            return [" ".join(t) for t in out]
        return self._transcribe(audios, language)

    def _transcribe(self, audios: list[np.ndarray], language: str) -> list[str]:
        import torch
        long_form = any(len(a) > self.WINDOW_SECONDS * self.sample_rate for a in audios)
        kw = dict(sampling_rate=self.sample_rate, return_tensors="pt", return_attention_mask=True)
        if long_form:  # transformers' sequential long-form decoding (S70: declare the policy)
            kw.update(truncation=False, padding="longest")
        feats = self.processor(audios, **kw)
        inputs = feats.input_features.to(self.device, dtype=self.model.dtype)
        gen = dict(
            language=self.hint(language),
            task="transcribe",
            num_beams=int(self.settings.get("beam_size", 1)),
            attention_mask=feats.attention_mask.to(self.device),
        )
        if long_form:
            gen.update(return_timestamps=True, condition_on_prev_tokens=False)
        # Extra decoder settings from the run config (e.g. no_repeat_ngram_size, repetition_penalty), recorded in
        # the run manifest with the rest of `model:`. Select them on dev only, and report them as a decoder ablation.
        gen.update(self.settings.get("generate_kwargs") or {})
        with torch.inference_mode():
            ids = self.model.generate(inputs, **gen)
        return [t.strip() for t in self.processor.batch_decode(ids, skip_special_tokens=True)]


class HFCTC(Recognizer):
    family = "hf-ctc"

    def load(self) -> None:
        from transformers import AutoModelForCTC, AutoProcessor
        self.processor = AutoProcessor.from_pretrained(self.model_id, revision=self.revision)
        # MMS (facebook/mms-1b-all): one shared encoder + per-language adapters and vocabularies.
        # `target_lang` is the ISO 639-3 adapter code from the model card, e.g. kaz, kat.
        self.target_lang = self.settings.get("target_lang")
        if self.target_lang:
            self.processor.tokenizer.set_target_lang(self.target_lang)
        self.decoder = None
        lm = self.settings.get("lm")
        if lm:  # word n-gram LM beam search (pyctcdecode + KenLM; Linux). Decoder first, then fork the pool, then CUDA.
            import multiprocessing
            from pyctcdecode import build_ctcdecoder
            tok = self.processor.tokenizer
            labels = [t for t, _ in sorted(tok.get_vocab().items(), key=lambda x: x[1])]
            labels = ["" if t == tok.pad_token else " " if t == tok.word_delimiter_token else t for t in labels]
            self.decoder = build_ctcdecoder(labels, kenlm_model_path=lm["arpa"], alpha=float(lm["alpha"]),
                                            beta=float(lm["beta"]))
            self.beam_width = int(lm.get("beam_width", 100))
            self.pool = multiprocessing.get_context("fork").Pool(int(lm.get("workers", 8)))
        self.model = AutoModelForCTC.from_pretrained(
            self.model_id, revision=self.revision, dtype=_torch_dtype(self.dtype)
        )
        if self.target_lang:
            self.model.load_adapter(self.target_lang)
        self.model = self.model.to(self.device, dtype=_torch_dtype(self.dtype)).eval()
        self.model_language = self.settings.get("model_language")

    def transcribe(self, audios: list[np.ndarray], language: str) -> list[str]:
        import torch
        if self.model_language and self.model_language != language:
            raise ValueError(f"{self.model_id} is a {self.model_language} model, asked for {language}.")
        batch = self.processor(audios, sampling_rate=self.sample_rate, return_tensors="pt", padding=True)
        values = batch.input_values.to(self.device, dtype=self.model.dtype)
        mask = batch.get("attention_mask")
        with torch.inference_mode():
            logits = self.model(values, attention_mask=None if mask is None else mask.to(self.device)).logits
        if self.decoder is not None:  # beam search with the word n-gram LM, on unpadded log-probs
            lens = ([logits.shape[1]] * len(audios) if mask is None
                    else self.model._get_feat_extract_output_lengths(mask.sum(-1)).tolist())
            lp = torch.log_softmax(logits.float(), dim=-1).cpu().numpy()
            return [t.strip() for t in self.decoder.decode_batch(self.pool, [lp[i, :n] for i, n in enumerate(lens)],
                                                                 beam_width=self.beam_width)]
        ids = logits.argmax(-1)  # greedy CTC: argmax per frame, then collapse repeats + blanks (S50-S52)
        return [t.strip() for t in self.processor.batch_decode(ids)]
