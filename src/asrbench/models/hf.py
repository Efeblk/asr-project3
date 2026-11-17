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
        with torch.inference_mode():
            ids = self.model.generate(inputs, **gen)
        return [t.strip() for t in self.processor.batch_decode(ids, skip_special_tokens=True)]


class HFCTC(Recognizer):
    family = "hf-ctc"

    def load(self) -> None:
        from transformers import AutoModelForCTC, AutoProcessor
        self.processor = AutoProcessor.from_pretrained(self.model_id, revision=self.revision)
        self.model = AutoModelForCTC.from_pretrained(
            self.model_id, revision=self.revision, dtype=_torch_dtype(self.dtype)
        )
        # MMS (facebook/mms-1b-all): one shared encoder + per-language adapters and vocabularies.
        # `target_lang` is the ISO 639-3 adapter code from the model card, e.g. kaz, kat.
        self.target_lang = self.settings.get("target_lang")
        if self.target_lang:
            self.processor.tokenizer.set_target_lang(self.target_lang)
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
        ids = logits.argmax(-1)  # greedy CTC: argmax per frame, then collapse repeats + blanks (S50-S52)
        return [t.strip() for t in self.processor.batch_decode(ids)]
