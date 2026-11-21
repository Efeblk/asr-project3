"""Environment capture for run manifests (S8, S77: hardware, precision, library versions)."""

from __future__ import annotations

import platform
import subprocess
import sys
from importlib import metadata
from pathlib import Path

PACKAGES = ["asrbench", "torch", "transformers", "accelerate", "jiwer", "numpy", "soundfile", "soxr",
            "nemo_toolkit", "qwen-asr", "huggingface-hub"]


def _git(*args: str) -> str | None:
    try:
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True,
                              cwd=Path(__file__).resolve().parent).stdout.strip()
    except Exception:
        return None


def package_versions() -> dict:
    out = {}
    for p in PACKAGES:
        try:
            out[p] = metadata.version(p)
        except metadata.PackageNotFoundError:
            pass
    return out


def hardware() -> dict:
    info = {"platform": platform.platform(), "machine": platform.machine(), "processor": platform.processor(),
            "python": sys.version.split()[0]}
    try:
        import torch
        info["torch_cuda"] = torch.version.cuda
        if torch.cuda.is_available():
            info["gpu"] = torch.cuda.get_device_name(0)
            info["gpu_memory_gb"] = round(torch.cuda.get_device_properties(0).total_memory / 2**30, 1)
    except ImportError:
        pass
    return info


def _archive_commit() -> str | None:
    """Commit of a `git archive` export (no .git dir, e.g. a Colab VM): git fills ARCHIVE_COMMIT via export-subst."""
    try:
        sha = (Path(__file__).resolve().parent / "ARCHIVE_COMMIT").read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return sha if len(sha) == 40 and all(c in "0123456789abcdef" for c in sha) else None


def capture() -> dict:
    out = {"packages": package_versions(), "hardware": hardware()}
    # Check the archive marker first: an export unpacked inside another checkout must not report that checkout's SHA.
    if sha := _archive_commit():
        return {"git_commit": sha, "git_dirty": None,
                "source": "git archive (export-subst): the commit the code was exported from; local edits after "
                          "export are not detectable", **out}
    status = _git("status", "--porcelain", "--untracked-files=no")  # run outputs are untracked until committed
    return {"git_commit": _git("rev-parse", "HEAD"), "git_dirty": bool(status) if status is not None else None, **out}
