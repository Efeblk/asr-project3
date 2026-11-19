"""Chunked Whisper decoding for Georgian: dev candidates, the selection rule, and the frozen test configs.

Why: Whisper spends ~20.6 tokens per Georgian word (~30 tokens per second of speech), so a single 30-s window
overflows the 448-token decoder budget after ~14.5 s and long FLEURS clips are truncated
(docs/error-analysis-georgian.md §1). Splitting long clips at pauses (`chunk_seconds`, `asrbench.models.hf.
split_at_pauses`) is a DECODING change, reported as its own row next to the unchanged model.

Rule (committed before any chunked run):
  candidates chunk_seconds in CANDIDATES; pick the one with the lowest mean of CV ka dev WER and FLEURS ka dev
  WER; ties -> the longer chunk. Everything else in the config is identical to the model's plain dev/test config.

    python scripts/chunk_select.py dev  <model-name>   # write the dev candidate configs
    python scripts/chunk_select.py test <model-name>   # apply the rule to the scored dev runs, write frozen test configs
"""

from __future__ import annotations

import glob
import json
import sys

import yaml

CANDIDATES = [8, 11, 14]
SETS = ["cv", "fleurs"]
CFG = "configs/runs/ka"


def write(name: str, ds: str, split: str, chunk: int, extra_head: str) -> str:
    src = f"{CFG}/{name}_{ds}-{split}.yaml"
    cfg = yaml.safe_load(open(src, encoding="utf-8"))
    tag = f"{name}+chunk{chunk}"
    cfg["name"] = cfg["name"].replace(name, tag, 1)
    cfg["model"]["chunk_seconds"] = chunk
    head = (f"# Georgian, OURS + decoding change: {src.split('/')[-1]} with long clips split at pauses into <= {chunk} s\n"
            f"# pieces (scripts/chunk_select.py). {extra_head}\n")
    out = f"{CFG}/{tag}_{ds}-{split}.yaml"
    open(out, "w", encoding="utf-8", newline="\n").write(head + yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
    return out


def dev_wer(name: str, chunk: int, ds: str) -> float:
    runs = sorted(glob.glob(f"runs/{name}+chunk{chunk}_{ds}-ka_dev_*"))
    if not runs:
        raise SystemExit(f"missing dev run for chunk {chunk} on {ds}")
    return json.load(open(f"{runs[-1]}/scores.json", encoding="utf-8"))["languages"]["ka"]["wer"]


def main() -> None:
    mode, name = sys.argv[1], sys.argv[2]
    if mode == "dev":
        for c in CANDIDATES:
            for ds in SETS:
                print(write(name, ds, "dev", c, "Dev candidate."))
        return
    table = {c: {ds: dev_wer(name, c, ds) for ds in SETS} for c in CANDIDATES}
    best = min(CANDIDATES, key=lambda c: (sum(table[c].values()) / len(SETS), -c))
    sel = {"model": name, "rule": "min mean(CV dev WER, FLEURS dev WER); ties -> longer chunk", "candidates": CANDIDATES,
           "dev_wer": {c: {ds: round(100 * w, 2) for ds, w in v.items()} for c, v in table.items()}, "selected": best}
    open(f"{CFG}/{name}+chunk-selection.yaml", "w", encoding="utf-8", newline="\n").write(
        yaml.safe_dump(sel, sort_keys=False))
    for ds in SETS:
        print(write(name, ds, "test", best, f"FROZEN TEST RUN, run once; chunk selected on dev ({name}+chunk-selection.yaml)."))
    print(json.dumps(sel))


if __name__ == "__main__":
    main()
