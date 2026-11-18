"""NeMo (Canary v2, Parakeet TDT v3) and Qwen3-ASR recognizers.

These follow the documented interfaces quoted in the Week 9 study deck (S72-S75) but have
NOT been executed in this repo yet (NeMo is best installed on Linux/WSL; Qwen3-ASR needs a
bf16-capable CUDA GPU). Verify on a few dev clips before relying on them.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from .base import Recognizer


def _write_wavs(audios: list[np.ndarray], sr: int, tmp: Path) -> list[str]:
    paths = []
    for i, a in enumerate(audios):
        p = tmp / f"{i:05d}.wav"
        sf.write(p, a, sr, subtype="PCM_16")
        paths.append(str(p))
    return paths


def _text(result) -> str:
    return (getattr(result, "text", result) or "").strip()


class NeMoASR(Recognizer):
    """family: nemo. Canary needs source_lang == target_lang for ASR (S72);
    Parakeet v3 detects the language itself (S73) - v2 is English-only."""

    family = "nemo"

    def load(self) -> None:
        if "parakeet" in self.model_id and "-v2" in self.model_id:
            raise ValueError("parakeet-tdt v2 is English-only; use v3 (S73, L41).")
        from nemo.collections.asr.models import ASRModel
        if Path(self.model_id).exists():
            path = self.model_id
        else:  # download the .nemo file at the pinned Hub revision (from_pretrained cannot pin one)
            from huggingface_hub import hf_hub_download, list_repo_files
            name = next(f for f in list_repo_files(self.model_id, revision=self.revision) if f.endswith(".nemo"))
            path = hf_hub_download(self.model_id, name, revision=self.revision)
        self.model = ASRModel.restore_from(path, map_location=self.device).eval()
        # Hybrid Transducer-CTC checkpoints decode with the transducer by default; `decoder_type: ctc` switches.
        if self.settings.get("decoder_type") and hasattr(self.model, "change_decoding_strategy"):
            self.model.change_decoding_strategy(decoder_type=self.settings["decoder_type"])
        self.is_canary = "canary" in self.model_id

    def transcribe(self, audios: list[np.ndarray], language: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _write_wavs(audios, self.sample_rate, Path(tmp))
            kw = {"batch_size": len(paths), "verbose": False}
            if self.is_canary:
                kw.update(source_lang=self.hint(language), target_lang=self.hint(language))
            out = self.model.transcribe(paths, **kw)
        if isinstance(out, tuple):  # older NeMo RNNT models return (best_hypotheses, all_hypotheses)
            out = out[0]
        return [_text(r) for r in out]


class QwenASR(Recognizer):
    """family: qwen. Watch max_new_tokens: a low cap truncates long outputs (S74)."""

    family = "qwen"

    def load(self) -> None:
        import torch
        from qwen_asr import Qwen3ASRModel
        self.model = Qwen3ASRModel.from_pretrained(
            self.model_id, dtype=getattr(torch, self.dtype if self.dtype != "float16" else "bfloat16"),
            device_map=self.device if ":" in self.device else f"{self.device}:0",
            max_new_tokens=int(self.settings.get("max_new_tokens", 256)),
        )

    def transcribe(self, audios: list[np.ndarray], language: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            paths = _write_wavs(audios, self.sample_rate, Path(tmp))
            return [_text(self.model.transcribe(audio=p, language=self.hint(language))[0]) for p in paths]


class Constant(Recognizer):
    """family: debug-constant. Returns a fixed string; for pipeline tests only."""

    family = "debug-constant"

    def load(self) -> None:
        self.text = self.settings.get("text", "")

    def transcribe(self, audios, language):
        return [self.text for _ in audios]

    def resolved_revision(self):
        return None
