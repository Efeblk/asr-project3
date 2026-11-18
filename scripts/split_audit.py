"""Split audit required by announcement A2 ("split by speaker, not by clip").

For each manifest and split: speakers (or the closest grouping unit when the corpus has no speaker IDs),
utterances, hours; groups shared between splits (= leakage); and how many dev/test sentences appear word for word
in the training set (raw text, and after the declared scoring normalization).

    uv run python scripts/split_audit.py data/fleurs/ka_ge/manifest.jsonl [more manifests ...] > docs/split-audit.md

`--train-filter key=value` restricts "the training set" to the items we actually train on (e.g. in_train_sample=true).
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict

from asrbench.dataset import load_manifest
from asrbench.normalize import load_policies

# KSC2 has no speaker IDs. Its file names encode the source recording for most subcorpora, which is the closest
# grouping unit (A2, points 3-4): parliament senate_03_427 -> session senate_03; podcasts/radio/talkshow
# 07_03_188 -> show 07, episode 03. Crowdsourced and tv_news names are opaque hashes / running numbers.
_KSC2_REC = re.compile(r"^(?P<rec>.+)_\d+$")


def group_of(item) -> tuple[str, str]:
    """(unit name, group id) used for the leakage check."""
    if item.speaker:
        return "speaker", item.speaker
    sub = item.extra.get("subcorpus")
    if sub:  # KSC2
        stem = item.audio.rsplit("/", 1)[-1].rsplit(".", 1)[0]
        m = _KSC2_REC.match(stem)
        if sub in ("parliament", "podcasts", "radio", "talkshow") and m:
            return "recording", f"{sub}/{m.group('rec')}"
        return "none (opaque file names)", ""
    if item.session and item.session.startswith("sent"):  # FLEURS: sentence ID, no speaker IDs
        return "none (no speaker IDs)", ""
    return "none", ""


NOTES = {
    "fleurs": "FLEURS has no speaker IDs. Its splits are sentence-disjoint, and its authors state that test speakers do "
              "not occur in train (paper arXiv 2205.12446; HF card google/fleurs). We use the documented split.",
    "Kazakh_Speech_Corpus_2": "KSC2 has no speaker IDs. Documented split used: crowdsourced dev/test come from KSC1, whose "
              "dev/test speakers do not overlap train; for the other subcorpora the paper says speaker overlap was "
              "minimised but 'not fully guaranteed' (the recurring radio/talk-show hosts likely appear in every split). "
              "Recordings (parliament sessions, podcast/radio/talk-show episodes) are not shared between splits.",
    "cv-corpus": "Common Voice: official split, speaker-disjoint by construction (client_id); verified above.",
}


def audit(path: str, train_filter: dict[str, str]) -> list[str]:
    m = load_manifest(path)
    langs = sorted({i.language for i in m.items})
    policy = load_policies("configs/scoring.yaml").for_language(langs[0])
    by_split = defaultdict(list)
    for it in m.items:
        by_split[it.split].append(it)

    def in_filter(it) -> bool:
        return all(str(getattr(it, k, it.extra.get(k))).lower() == v.lower() for k, v in train_filter.items())

    train = [i for i in by_split.get("train", []) if in_filter(i)]
    out = [f"## `{path}` ({', '.join(langs)})", ""]
    if train_filter:
        out += [f"Training set = train items with {train_filter} ({len(train)} utterances).", ""]
    out += ["| Split | Grouping unit | Groups | Utterances | Hours | Groups shared with train | Sentences also in train (raw / normalized) |",
            "|---|---|---|---|---|---|---|"]
    train_groups = {group_of(i)[1] for i in train} - {""}
    train_raw = {i.reference.strip() for i in train if i.reference.strip()}
    train_norm = {policy.normalize(i.reference) for i in train} - {""}
    for split in ("train", "dev", "test"):
        items = train if split == "train" else by_split.get(split, [])
        if not items:
            continue
        units = defaultdict(int)
        for i in items:
            units[group_of(i)[0]] += 1
        groups = {group_of(i)[1] for i in items} - {""}
        hours = sum(i.duration or 0 for i in items) / 3600
        unit = ", ".join(f"{u} ({n})" if len(units) > 1 else u for u, n in sorted(units.items()))
        if split == "train":
            shared, overlap = "—", "—"
        else:
            shared = str(len(groups & train_groups)) if groups else "n/a"
            sents = [i.reference.strip() for i in items if i.reference.strip()]
            raw = sum(s in train_raw for s in sents)
            norm = sum(policy.normalize(s) in train_norm for s in sents)
            overlap = f"{raw} / {norm} of {len(sents)} ({100 * norm / max(len(sents), 1):.1f}%)"
        out.append(f"| {split} | {unit} | {len(groups) if groups else '—'} | {len(items)} | {hours:.2f} | {shared} | {overlap} |")
    dt = {group_of(i)[1] for i in by_split.get("dev", [])} & {group_of(i)[1] for i in by_split.get("test", [])} - {""}
    out += ["", f"Groups shared between dev and test: {len(dt)}.", ""]
    src = (m.items[0].source or "") if m.items else ""
    for key, note in NOTES.items():
        if key in src or key in path:
            out += [f"Note: {note}", ""]
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--train-filter", action="append", default=[], help="key=value, may repeat (applies to all)")
    a = ap.parse_args()
    tf = dict(kv.split("=", 1) for kv in a.train_filter)
    lines = ["# Split audit (announcement A2)", "",
             "Generated by `scripts/split_audit.py`; do not edit by hand. \"Groups\" are speakers when the corpus has "
             "speaker IDs, otherwise the closest unit it has (A2 point 3). \"Sentences also in train\" counts dev/test "
             "utterances whose transcript appears word for word in the training set.", ""]
    for p in a.manifests:
        lines += audit(p, tf)
    print("\n".join(lines))
