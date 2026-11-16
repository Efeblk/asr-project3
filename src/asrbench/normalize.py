"""Scoring policy: the text normalization declared *before* comparing models (S16, S17).

The same policy is applied to references and hypotheses. Raw predictions are never modified
on disk; normalization happens only at scoring time.
"""

from __future__ import annotations

import unicodedata
from dataclasses import asdict, dataclass, field

import regex
import yaml

_PUNCT = regex.compile(r"\p{P}+")
_SPACES = regex.compile(r"\s+")
_GRAPHEME = regex.compile(r"\X")


@dataclass
class Policy:
    unicode_form: str = "NFC"          # NFC | NFD | NFKC | NFKD | none
    lowercase: bool = True             # casefold()
    remove_punctuation: bool = True    # Unicode category P
    strip_diacritics: bool = False     # off by default: accents can change meaning (S23)
    word_unit: str = "whitespace"      # whitespace | none (no reliable spaces -> report CER only)
    cer_unit: str = "codepoint"        # codepoint | grapheme
    note: str = ""

    def normalize(self, text: str) -> str:
        if self.unicode_form != "none":
            text = unicodedata.normalize(self.unicode_form, text)
        if self.lowercase:
            text = text.casefold()
        if self.remove_punctuation:
            text = _PUNCT.sub(" ", text)
        if self.strip_diacritics:
            decomposed = unicodedata.normalize("NFD", text)
            text = "".join(c for c in decomposed if unicodedata.category(c) != "Mn")
            if self.unicode_form != "none":
                text = unicodedata.normalize(self.unicode_form, text)
        return _SPACES.sub(" ", text).strip()

    def char_tokens(self, normalized: str) -> list[str]:
        """Units for CER. Spaces count as a unit (as in jiwer's CER)."""
        if self.cer_unit == "grapheme":
            return ["▁" if g == " " else g for g in _GRAPHEME.findall(normalized)]
        return ["▁" if c == " " else c for c in normalized]

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PolicySet:
    default: Policy = field(default_factory=Policy)
    languages: dict[str, Policy] = field(default_factory=dict)

    def for_language(self, lang: str) -> Policy:
        return self.languages.get(lang, self.default)

    def to_dict(self) -> dict:
        return {"default": self.default.to_dict(), "languages": {k: v.to_dict() for k, v in self.languages.items()}}


def load_policies(path: str | None) -> PolicySet:
    if not path:
        return PolicySet()
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    default = Policy(**cfg.get("default", {}))
    langs = {k: Policy(**{**default.to_dict(), **(v or {})}) for k, v in (cfg.get("languages") or {}).items()}
    return PolicySet(default, langs)
