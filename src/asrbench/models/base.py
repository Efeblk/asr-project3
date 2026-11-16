"""Recognizer interface. Every model family implements `transcribe` on a batch of 16 kHz mono
float32 arrays and reports what it is (`describe`) for the run manifest (S77)."""

from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np


class Recognizer(ABC):
    sample_rate: int = 16000

    def __init__(self, model_id: str, revision: str = "main", device: str = "cuda", dtype: str = "float16",
                 language_hints: dict[str, str] | None = None, **settings):
        self.model_id = model_id
        self.revision = revision
        self.device = device
        self.dtype = dtype
        self.language_hints = language_hints or {}
        self.settings = settings

    def hint(self, language: str) -> str:
        """Model-specific language argument for a manifest language code (declared in config)."""
        return self.language_hints.get(language, language)

    @abstractmethod
    def load(self) -> None: ...

    @abstractmethod
    def transcribe(self, audios: list[np.ndarray], language: str) -> list[str]: ...

    def resolved_revision(self) -> str | None:
        """Exact commit hash of the checkpoint on the Hugging Face Hub, if resolvable."""
        try:
            from huggingface_hub import model_info
            return model_info(self.model_id, revision=self.revision).sha
        except Exception:
            return None

    def describe(self) -> dict:
        return {
            "family": type(self).family,
            "model_id": self.model_id,
            "revision_requested": self.revision,
            "revision_resolved": self.resolved_revision(),
            "device": self.device,
            "dtype": self.dtype,
            "language_hints": self.language_hints,
            "settings": self.settings,
        }

    def sync(self) -> None:
        """Block until queued GPU work is done so timings are honest."""
        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.synchronize()
        except ImportError:
            pass
