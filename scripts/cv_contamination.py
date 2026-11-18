"""Evidence for training-data contamination of a pretrained baseline on Common Voice (error analysis).

Common Voice clip IDs grow over time (common_voice_ka_<n>.mp3). A checkpoint trained on an older Common Voice
release (nvidia/stt_ka_fastconformer_hybrid_large_pc: CV 17.0 train/dev/other, per its model card) may have seen
older clips of our CV 27.0 dev/test. If so, its error rate rises sharply for newer clip IDs, much more than for
systems without that exposure. This script prints corpus WER per clip-ID bucket for the given run prefixes.

    uv run python scripts/cv_contamination.py nvidia-stt-ka-fastconformer mms-1b-all-kat xlsr-georgian-xsway

The buckets are descriptive (no cutoff is selected on test for any reported number).
"""

from __future__ import annotations

import glob
import json
import sys

EDGES = [0, 38_000_000, 39_500_000, 40_000_000, 40_300_000, 40_400_000, 40_500_000, 40_700_000, 41_000_000,
         42_000_000, 44_000_000, 10**9]


def load(prefix: str, split: str) -> dict:
    runs = sorted(glob.glob(f"runs/{prefix}_cv-ka_{split}_*"))
    if not runs:
        return {}
    return {j["id"]: j for j in map(json.loads, open(runs[-1] + "/item_scores.jsonl", encoding="utf-8"))}


def main(prefixes: list[str]) -> None:
    systems = {p: {**load(p, "dev"), **load(p, "test")} for p in prefixes}
    num = lambda k: int(k.rsplit("_", 1)[-1])  # noqa: E731
    common = set.intersection(*(set(k for k, v in d.items() if v["words"]) for d in systems.values()))
    print("| Clip-ID range (CV 27.0 ka dev + test) | Clips | " + " | ".join(f"{p} WER" for p in prefixes) + " |")
    print("|---|---|" + "---|" * len(prefixes))
    for lo, hi in zip(EDGES, EDGES[1:]):
        chunk = [k for k in common if lo <= num(k) < hi]
        if not chunk:
            continue
        cells = []
        for d in systems.values():
            w = [d[k]["words"] for k in chunk]
            cells.append(f"{100 * sum(x['S'] + x['D'] + x['I'] for x in w) / sum(x['N'] for x in w):.2f}")
        hi_s = "∞" if hi == EDGES[-1] else f"{hi / 1e6:.1f} M"
        print(f"| {lo / 1e6:.1f} M – {hi_s} | {len(chunk)} | " + " | ".join(cells) + " |")


if __name__ == "__main__":
    main(sys.argv[1:] or ["nvidia-stt-ka-fastconformer", "mms-1b-all-kat", "xlsr-georgian-xsway"])
