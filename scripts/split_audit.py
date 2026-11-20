"""Split audit required by announcement A2 ("split by speaker, not by clip").

For each manifest and split: speakers (or the closest grouping unit when the corpus has no speaker IDs),
utterances, hours; groups shared between splits (= leakage); and how many dev/test sentences appear word for word
in the training set (raw text, and after the declared scoring normalization).

    uv run python scripts/split_audit.py data/fleurs/ka_ge/manifest.jsonl [more manifests ...] > docs/split-audit.md

`--train-filter key=value` restricts "the training set" to the items we actually train on (e.g. in_train_sample=true).
`--cross-train MANIFEST` also checks every dev/test sentence against the train split of another corpus, i.e. the
text our models and LM were actually trained on (FLEURS dev/test vs CV ka train).
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


def sentence_id(item) -> str:
    """FLEURS: one sentence is read by several speakers; the manifest keeps its ID as the session ("sent<id>")."""
    return item.session if item.session and item.session.startswith("sent") else ""


def audit(path: str, train_filter: dict[str, str], cross: tuple[str, set, set] | None = None) -> list[str]:
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
    dev_g = {group_of(i)[1] for i in by_split.get("dev", [])} - {""}
    test_g = {group_of(i)[1] for i in by_split.get("test", [])} - {""}
    if dev_g and test_g:
        out += ["", f"Groups shared between dev and test: {len(dev_g & test_g)}.", ""]
    else:
        out += ["", "Groups shared between dev and test: n/a (no speaker or recording IDs in this corpus; "
                "speaker separation cannot be checked here, see the note).", ""]
    sids = {sp: {sentence_id(i) for i in (train if sp == "train" else by_split.get(sp, []))} - {""}
            for sp in ("train", "dev", "test")}
    if any(sids.values()):
        out += [f"Sentence IDs (one sentence, several readers): train {len(sids['train'])}, dev {len(sids['dev'])}, "
                f"test {len(sids['test'])}; shared train–dev {len(sids['train'] & sids['dev'])}, train–test "
                f"{len(sids['train'] & sids['test'])}, dev–test {len(sids['dev'] & sids['test'])}.", ""]
    if cross:
        name, xraw, xnorm = cross
        out += [f"Overlap with the text we trained on ({name}; fine-tunes, word LM and GMM-HMM):", ""]
        for split in ("dev", "test"):
            sents = [i.reference.strip() for i in by_split.get(split, []) if i.reference.strip()]
            if sents:
                raw = sum(t in xraw for t in sents)
                norm = sum(policy.normalize(t) in xnorm for t in sents)
                out.append(f"- {split}: {raw} raw / {norm} normalized of {len(sents)} sentences "
                           f"({100 * norm / len(sents):.1f}%) also occur in it.")
        out.append("")
    src = (m.items[0].source or "") if m.items else ""
    for key, note in NOTES.items():
        if key in src or key in path:
            out += [f"Note: {note}", ""]
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--train-filter", action="append", default=[], help="key=value, may repeat (applies to all)")
    ap.add_argument("--cross-train", help="manifest whose train split is the text we trained on (checked for others)")
    ap.add_argument("--no-header", action="store_true", help="omit the title (when appending a second section)")
    a = ap.parse_args()
    tf = dict(kv.split("=", 1) for kv in a.train_filter)
    cross = None
    if a.cross_train:
        xm = load_manifest(a.cross_train)
        xpol = load_policies("configs/scoring.yaml").for_language(xm.items[0].language)
        xtrain = [i.reference.strip() for i in xm.items if i.split == "train" and i.reference.strip()]
        cross = (f"`{a.cross_train}` train, {len(xtrain)} transcripts", set(xtrain),
                 {xpol.normalize(t) for t in xtrain} - {""})
    lines = [] if a.no_header else ["# Split audit (announcement A2)", "",
             "Generated by `scripts/split_audit.py`; do not edit by hand. \"Groups\" are speakers when the corpus has "
             "speaker IDs, otherwise the closest unit it has (A2 point 3). \"Sentences also in train\" counts dev/test "
             "utterances whose transcript appears word for word in the training set.", ""]
    for p in a.manifests:
        lines += audit(p, tf, cross if a.cross_train and p != a.cross_train else None)
    print("\n".join(lines))
