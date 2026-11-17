"""Kazakh vs Russian transcript filter (rule 3: same-language ASR).

KSC2's parliament subcorpus mixes Kazakh and Russian talks (paper footnote 7: 33 % Russian). Both use Cyrillic,
so we label each transcript with a small, auditable classifier:

1. Kazakh-specific letters (ә ғ қ ң ө ұ ү һ і) are strong Kazakh evidence.
2. A character 1-4-gram naive Bayes model scores each *word*; it is trained on pure Kazakh read speech
   (KSC2 crowdsourced + TTS transcripts) and on high-confidence Russian lines (parliament lines with no Kazakh
   letters and >= 2 Russian function words, none Kazakh).

Labels: `kk` (keep), `ru` (drop: Russian speech; >= 80 % Russian-looking words, or >= 75 % with no Kazakh evidence),
`mixed` (keep: code-switched Kazakh, 50-80 % Russian-looking words; analysed as an error category).
Thresholds were set by auditing random samples per subcorpus (docs/data-notes-ksc2.md).
"""

from __future__ import annotations

import math
from collections import Counter

KK_LETTERS = set("әғқңөұүһі")
RU_FUNCTION = {"и", "в", "не", "что", "на", "с", "по", "это", "как", "для", "мы", "вы", "они", "он", "она", "но",
               "к", "из", "о", "у", "за", "от", "же", "так", "все", "бы", "было", "который", "также", "только",
               "если", "при", "или", "уважаемые", "спасибо", "прошу", "уважаемый"}
KK_FUNCTION = {"және", "мен", "бұл", "бойынша", "үшін", "деп", "да", "де", "ол", "біз", "сіз", "бар", "жоқ", "екі",
               "бір", "керек", "болып", "жылы", "осы", "сол", "мына", "ғой", "ма", "ме", "па", "пе", "емес", "рахмет"}
FILLER_CHARS = set("ыэмауфхнъ")  # hesitation tokens (ыыы, э, мхм, уф, ...) carry no language evidence


def _grams(word: str, n_max: int = 4) -> list[str]:
    w = f"^{word}$"
    return [w[i:i + n] for n in range(1, n_max + 1) for i in range(len(w) - n + 1)]


class CharNB:
    def __init__(self):
        self.counts = {"kk": Counter(), "ru": Counter()}
        self.totals = {"kk": 0, "ru": 0}

    def fit(self, texts: dict[str, list[str]]) -> "CharNB":
        for lab, lines in texts.items():
            for line in lines:
                for w in line.split():
                    g = _grams(w)
                    self.counts[lab].update(g)
                    self.totals[lab] += len(g)
        self.vocab = len(set(self.counts["kk"]) | set(self.counts["ru"]))
        return self

    def word_logodds(self, word: str) -> float:
        """log P(word | ru) - log P(word | kk); > 0 means Russian-looking."""
        s = 0.0
        for g in _grams(word):
            p_ru = (self.counts["ru"][g] + 1) / (self.totals["ru"] + self.vocab)
            p_kk = (self.counts["kk"][g] + 1) / (self.totals["kk"] + self.vocab)
            s += math.log(p_ru) - math.log(p_kk)
        return s


def is_confident_russian(text: str) -> bool:
    toks = text.split()
    return (not any(c in KK_LETTERS for c in text) and sum(t in RU_FUNCTION for t in toks) >= 2
            and not any(t in KK_FUNCTION for t in toks))


def label(text: str, nb: CharNB) -> tuple[str, float]:
    """Return (label, share of Russian-looking words)."""
    toks = [t for t in text.split() if not set(t) <= FILLER_CHARS]
    if not toks:
        return "kk", 0.0
    ru_words = [t for t in toks if not any(c in KK_LETTERS for c in t) and t not in KK_FUNCTION
                and (t in RU_FUNCTION or nb.word_logodds(t) > 0)]
    share = len(ru_words) / len(toks)
    has_kk = any(c in KK_LETTERS for c in text) or any(t in KK_FUNCTION for t in toks)
    if share >= 0.8 or (not has_kk and share >= 0.75):  # Russian speech, at most a Kazakh name or term inside
        return "ru", share
    if share >= 0.5:
        return "mixed", share
    return "kk", share


def train_from_manifest(rows: list[dict]) -> CharNB:
    kk = [r["reference"] for r in rows if r["split"] == "train" and r.get("subcorpus") in ("crowdsourced", "tts")]
    ru = [r["reference"] for r in rows if r["split"] == "train" and r.get("subcorpus") == "parliament"
          and is_confident_russian(r["reference"])]
    return CharNB().fit({"kk": kk, "ru": ru})


def filter_manifest(path, log=print) -> dict:
    """Label every transcript (`text_lang`), drop `ru` rows into <manifest>.removed_ru.jsonl, rewrite the manifest.
    The classifier is trained on train-split transcripts only."""
    import json
    from pathlib import Path
    path = Path(path)
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    if rows and all("text_lang" in r for r in rows):
        raise ValueError(f"{path} is already language-filtered; re-import it to filter again.")
    nb = train_from_manifest(rows)
    keep, removed, stats = [], [], Counter()
    for r in rows:
        lab, share = label(r["reference"], nb)
        r["text_lang"], r["ru_word_share"] = lab, round(share, 3)
        stats[(r["split"], r.get("subcorpus"), lab)] += 1
        (removed if lab == "ru" else keep).append(r)
    dump = lambda rs: "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rs)  # noqa: E731
    path.with_suffix(".removed_ru.jsonl").write_text(dump(removed), encoding="utf-8", newline="\n")
    path.write_text(dump(keep), encoding="utf-8", newline="\n")
    log(f"kept {len(keep)}, removed {len(removed)} Russian utterances")
    return {"/".join(map(str, k)): v for k, v in sorted(stats.items())}
