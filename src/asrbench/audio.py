"""Audio loading: always returns mono float32 at the requested sample rate (S28)."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np
import soundfile as sf
import soxr


def load_audio(path: str | Path, sr: int = 16000) -> np.ndarray:
    path = Path(path)
    try:
        data, file_sr = sf.read(str(path), dtype="float32", always_2d=True)
        data = data.mean(axis=1)
    except (sf.LibsndfileError, RuntimeError):
        return _load_with_ffmpeg(path, sr)
    if file_sr != sr:
        data = soxr.resample(data, file_sr, sr, quality="HQ")
    return np.ascontiguousarray(data, dtype=np.float32)


def _load_with_ffmpeg(path: Path, sr: int) -> np.ndarray:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(f"Cannot decode {path} with soundfile and ffmpeg is not on PATH.")
    cmd = [ffmpeg, "-nostdin", "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def duration_seconds(audio: np.ndarray, sr: int) -> float:
    return len(audio) / sr
