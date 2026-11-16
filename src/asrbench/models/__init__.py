from .base import Recognizer


def build_recognizer(spec: dict) -> Recognizer:
    spec = dict(spec)
    family = spec.pop("family")
    model_id = spec.pop("id")
    if family == "hf-whisper":
        from .hf import HFWhisper as cls
    elif family == "hf-ctc":
        from .hf import HFCTC as cls
    elif family == "nemo":
        from .other import NeMoASR as cls
    elif family == "qwen":
        from .other import QwenASR as cls
    elif family == "debug-constant":
        from .other import Constant as cls
    else:
        raise ValueError(f"Unknown model family '{family}'. Known: hf-whisper, hf-ctc, nemo, qwen, debug-constant")
    return cls(model_id, **spec)


__all__ = ["Recognizer", "build_recognizer"]
