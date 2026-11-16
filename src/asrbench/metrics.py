"""Lexical error metrics (S12-S26, JM15 p.22).

Per-item edit counts are computed once, then *pooled* for corpus metrics (S18):
corpus WER = sum(S+D+I) / sum(N). Clips with an empty reference are excluded from WER/CER
denominators and reported separately in the silence report (S76).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import jiwer
import numpy as np

from .normalize import Policy


@dataclass
class Counts:
    hits: int = 0
    sub: int = 0
    dele: int = 0
    ins: int = 0

    @property
    def n_ref(self) -> int:
        return self.hits + self.sub + self.dele

    @property
    def n_hyp(self) -> int:
        return self.hits + self.sub + self.ins

    @property
    def errors(self) -> int:
        return self.sub + self.dele + self.ins

    def __add__(self, o: "Counts") -> "Counts":
        return Counts(self.hits + o.hits, self.sub + o.sub, self.dele + o.dele, self.ins + o.ins)

    def as_dict(self) -> dict:
        return {"C": self.hits, "S": self.sub, "D": self.dele, "I": self.ins, "N": self.n_ref, "M": self.n_hyp}


def _token_counts(ref: str, hyp: str) -> tuple[Counts, list]:
    """Minimum-edit alignment counts between space-separated token strings."""
    if not ref:
        return Counts(ins=len(hyp.split())), []
    if not hyp:
        return Counts(dele=len(ref.split())), []
    out = jiwer.process_words(ref, hyp)
    c = Counts(out.hits, out.substitutions, out.deletions, out.insertions)
    pairs = []
    for chunk in out.alignments[0]:
        if chunk.type == "substitute":
            r = out.references[0][chunk.ref_start_idx:chunk.ref_end_idx]
            h = out.hypotheses[0][chunk.hyp_start_idx:chunk.hyp_end_idx]
            pairs.extend(zip(r, h))
    return c, pairs


@dataclass
class ItemScore:
    id: str
    ref_norm: str
    hyp_norm: str
    words: Counts | None   # None when the policy has word_unit = none
    chars: Counts
    sub_pairs: list

    @property
    def is_silence(self) -> bool:
        return not self.ref_norm


def score_item(item_id: str, reference: str, hypothesis: str, policy: Policy) -> ItemScore:
    ref = policy.normalize(reference)
    hyp = policy.normalize(hypothesis or "")
    words, pairs = (None, []) if policy.word_unit == "none" else _token_counts(ref, hyp)
    chars, _ = _token_counts(" ".join(policy.char_tokens(ref)), " ".join(policy.char_tokens(hyp)))
    return ItemScore(item_id, ref, hyp, words, chars, pairs)


def ratio(num: float, den: float) -> float | None:
    return None if den == 0 else num / den


def corpus_metrics(scores: list[ItemScore]) -> dict:
    speech = [s for s in scores if not s.is_silence]
    out: dict = {"items": len(speech)}
    if speech and speech[0].words is not None:
        w = sum((s.words for s in speech), Counts())
        out["word_counts"] = w.as_dict()
        out["wer"] = ratio(w.errors, w.n_ref)
        out["mer"] = ratio(w.errors, w.hits + w.errors)
        out["wil"] = None if not (w.n_ref and w.n_hyp) else 1 - (w.hits / w.n_ref) * (w.hits / w.n_hyp)
        clip = [s.words.errors / s.words.n_ref for s in speech if s.words.n_ref]
        out["mean_clip_wer"] = float(np.mean(clip)) if clip else None
    c = sum((s.chars for s in speech), Counts())
    out["char_counts"] = c.as_dict()
    out["cer"] = ratio(c.errors, c.n_ref)
    return out


def silence_report(scores: list[ItemScore]) -> dict:
    silent = [s for s in scores if s.is_silence]
    emitted = [len(s.hyp_norm.split()) for s in silent]
    return {
        "silent_items": len(silent),
        "items_with_output": sum(1 for e in emitted if e > 0),
        "emitted_words": int(sum(emitted)),
        "examples": [{"id": s.id, "hyp": s.hyp_norm} for s in silent if s.hyp_norm][:10],
    }


def top_substitutions(scores: list[ItemScore], k: int = 15) -> list[tuple[str, str, int]]:
    c = Counter(p for s in scores for p in s.sub_pairs)
    return [(r, h, n) for (r, h), n in c.most_common(k)]
