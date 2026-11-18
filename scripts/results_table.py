"""Build the Kazakh results tables (docs/results-kazakh.md) from committed run directories.

Every number is read from runs/<run>/scores.json (and scores.nofillers.json when present), so the tables can be
regenerated at any time:  uv run python scripts/results_table.py > docs/results-kazakh.md
Baselines and ours are separate row groups (A1); no cross-dataset or cross-language average is shown (S19).
"""

from __future__ import annotations

import glob
import json
import os

SYSTEMS = [  # (row label, run-name prefix, group)
    ("Whisper-small (zero-shot)", "whisper-small", "baseline"),
    ("Whisper-large-v3 (zero-shot)", "whisper-large-v3", "baseline"),
    ("Whisper-large-v3-turbo (zero-shot)", "whisper-large-v3-turbo", "baseline"),
    ("MMS-1b-all + kaz adapter (zero-shot)", "mms-1b-all-kaz", "baseline"),
    ("XLS-R-300M Kazakh, aismlv (zero-shot)", "xlsr-kazakh-aismlv", "baseline"),
    ("Whisper-small, full fine-tune", "whisper-small-ft_ksc2-sample", "ours"),
    ("MMS-1b-all, kaz adapter fine-tune (2.3 M params)", "mms-1b-all-kaz-adapter-ft_ksc2-sample", "ours"),
    ("Whisper-large-v3-turbo, full fine-tune", "whisper-large-v3-turbo-ft_ksc2-sample", "ours"),
    ("… + beam 5 (decoder row, selected on dev)", "whisper-large-v3-turbo-ft_ksc2-sample+beam5", "ours+decoder"),
]
SETS = [("ksc2", "KSC2"), ("fleurs", "FLEURS kk")]


def _run(prefix: str, ds: str, split: str) -> str | None:
    runs = sorted(glob.glob(f"runs/{prefix}_{ds}-kk_{split}_*"))
    return runs[-1] if runs else None


def _scores(run: str | None, tag: str = "") -> dict | None:
    if not run:
        return None
    p = os.path.join(run, f"scores{tag}.json")
    return json.load(open(p, encoding="utf-8"))["languages"]["kk"] if os.path.exists(p) else None


def pct(x) -> str:
    return "—" if x is None else f"{100 * x:.2f}"


def main_table(split: str) -> list[str]:
    head = ("| Group | System | " + " | ".join(f"{n} WER | {n} CER | {n} 95% CI (WER)" for _, n in SETS)
            + " | RTFx (KSC2) | GPU (KSC2 run) |")
    out = [head, "|" + "---|" * (4 + 3 * len(SETS))]
    for label, prefix, group in SYSTEMS:
        cells, rtfx, gpu = [], "—", "—"
        for ds, _ in SETS:
            m = _scores(_run(prefix, ds, split))
            ci = m.get("wer_ci") if m else None
            cells += [pct(m and m["wer"]), pct(m and m["cer"]), f"{pct(ci['low'])}–{pct(ci['high'])}" if ci else "—"]
            if ds == "ksc2" and m and m.get("rtfx"):
                rtfx = f"{m['rtfx']:.0f}"
                man = json.load(open(os.path.join(_run(prefix, ds, split), "manifest.json"), encoding="utf-8"))
                gpu = man.get("env", {}).get("hardware", {}).get("gpu", "—").replace("NVIDIA ", "")
        if any(c != "—" for c in cells):
            out.append(f"| {group} | {label} | " + " | ".join(cells) + f" | {rtfx} | {gpu} |")
    return out


PAIRS = [  # (ours/other, reference system): paired cluster bootstrap on matched clips
    ("whisper-large-v3-turbo-ft_ksc2-sample", "xlsr-kazakh-aismlv"),
    ("whisper-large-v3-turbo-ft_ksc2-sample", "mms-1b-all-kaz"),
    ("whisper-large-v3-turbo-ft_ksc2-sample", "whisper-large-v3-turbo"),
    ("mms-1b-all-kaz-adapter-ft_ksc2-sample", "mms-1b-all-kaz"),
    ("whisper-small-ft_ksc2-sample", "whisper-small"),
    ("whisper-large-v3-turbo-ft_ksc2-sample+beam5", "whisper-large-v3-turbo-ft_ksc2-sample"),
]


def paired_table(split: str) -> list[str]:
    from asrbench.scoring import compare
    out = ["| Set | B (ours / variant) | A (reference) | WER A | WER B | Δ WER (A−B) | 95% CI | CER A | CER B | Δ CER | 95% CI |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ds, name in SETS:
        for b, a in PAIRS:
            ra, rb = _run(a, ds, split), _run(b, ds, split)
            if not (ra and rb):
                continue
            row = [l for l in compare(ra, rb, "configs/scoring.yaml").splitlines() if l.startswith("| kk")][0]
            c = [x.strip() for x in row.strip("|").split("|")]  # kk, items, werA, werB, d, ci, p, cerA, cerB, dcer, ci
            out.append(f"| {name} | {b} | {a} | {c[2]} | {c[3]} | {c[4]} | {c[5]} | {c[7]} | {c[8]} | {c[9]} | {c[10]} |")
    return out


def subcorpus_table(split: str) -> list[str]:
    rows, groups = [], None
    for label, prefix, group in SYSTEMS:
        m = _scores(_run(prefix, "ksc2", split))
        if not m or not m.get("by_subcorpus"):
            continue
        groups = groups or list(m["by_subcorpus"])
        rows.append(f"| {group} | {label} | " + " | ".join(pct(m["by_subcorpus"][g]["wer"]) for g in groups) + " |")
    if not groups:
        return []
    return ["| Group | System | " + " | ".join(groups) + " |", "|" + "---|" * (2 + len(groups))] + rows


def filler_table(split: str) -> list[str]:
    out = ["| Group | System | KSC2 WER (primary) | KSC2 WER without fillers | Δ |", "|---|---|---|---|---|"]
    for label, prefix, group in SYSTEMS:
        run = _run(prefix, "ksc2", split)
        a, b = _scores(run), _scores(run, ".nofillers")
        if a and b:
            out.append(f"| {group} | {label} | {pct(a['wer'])} | {pct(b['wer'])} | {100 * (a['wer'] - b['wer']):.2f} |")
    return out


if __name__ == "__main__":
    lines = ["# Kazakh results", "",
             "Generated by `scripts/results_table.py` from the committed `runs/*/scores.json`; do not edit by hand.",
             "WER/CER: corpus rates (%) under the declared policy `configs/scoring.yaml`; CI: 95% cluster bootstrap "
             "over sessions/speakers. All fine-tunes trained on the same 34.1 h KSC2 train sample "
             "(`runs/train_*`); checkpoints and decoding selected on dev; test run once with frozen configs "
             "(`configs/runs/kk/*-test.yaml`, committed in 7e36fe2 before any test run).", ""]
    for split, title in (("test", "Test (frozen, run once)"), ("dev", "Dev (selection)")):
        lines += [f"## {title}", ""] + main_table(split) + [""]
        lines += [f"### Paired comparisons ({split})", "", "Positive Δ = B has fewer errors than A. Cluster bootstrap "
                  "(2000 resamples) over sessions/speakers on matched clip IDs.", ""] + paired_table(split) + [""]
        sub = subcorpus_table(split)
        if sub:
            lines += [f"### KSC2 {split} WER by subcorpus", ""] + sub + [""]
    fill = filler_table("dev")
    if len(fill) > 2:
        lines += ["## Scoring ablation: hesitation fillers (KSC2 dev)", "",
                  "Secondary policy `configs/scoring-nofillers.yaml` drops tokens made only of ы/і/м from references "
                  "and hypotheses alike. The primary metric is unchanged.", ""] + fill + [""]
    print("\n".join(lines))
