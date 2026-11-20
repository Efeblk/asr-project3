"""Build the results tables (docs/results-georgian.md, docs/results-kazakh.md) from committed run directories.

Every number is read from runs/<run>/scores.json (and scores.nofillers.json when present), so the tables can be
regenerated at any time:
    uv run python scripts/results_table.py ka > docs/results-georgian.md
    uv run python scripts/results_table.py kk > docs/results-kazakh.md
Baselines and ours are separate row groups (A1); no cross-dataset or cross-language average is shown (S19).
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

KK_SYSTEMS = [  # (row label, run-name prefix, group)
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
KK_SETS = [("ksc2", "KSC2"), ("fleurs", "FLEURS kk")]
KA_SYSTEMS = [
    ("Whisper-small (zero-shot)", "whisper-small", "baseline"),
    ("Whisper-large-v3 (zero-shot)", "whisper-large-v3", "baseline"),
    ("Whisper-large-v3-turbo (zero-shot)", "whisper-large-v3-turbo", "baseline"),
    ("XLS-R-300M Georgian, xsway (zero-shot, CTC)", "xlsr-georgian-xsway", "baseline"),
    ("MMS-1b-all + kat adapter (zero-shot, CTC)", "mms-1b-all-kat", "baseline"),
    ("NVIDIA FastConformer hybrid ka (zero-shot, transducer)*", "nvidia-stt-ka-fastconformer", "baseline"),
    ("MFCC + GMM-HMM, LDA+MLLT (Kaldi tri2b, trained by us from scratch, CPU)", "kaldi-gmm-hmm-tri2b", "baseline"),
    ("MFCC + GMM-HMM, LDA+MLLT+SAT (Kaldi tri3b, trained by us from scratch, CPU)", "kaldi-gmm-hmm-tri3b", "baseline"),
    ("MMS-1b-all, kat adapter fine-tune (2.3 M params)", "mms-1b-all-kat-adapter-ft_cv-ka", "ours"),
    ("Whisper-large-v3-turbo, full fine-tune", "whisper-large-v3-turbo-ft_cv-ka", "ours"),
    ("MMS-1b-all + kat adapter, zero-shot + our CV-train word 3-gram LM (LM ablation)", "mms-1b-all-kat+lm", "baseline+our LM"),
    ("MMS-1b-all, kat adapter fine-tune + our word 3-gram LM (beam 100; α/β selected on dev)", "mms-1b-all-kat-adapter-ft_cv-ka+lm",
     "ours+decoder"),
    ("Whisper-large-v3-turbo, full fine-tune, retrain r2 (same config; r1 weights not kept)", "whisper-large-v3-turbo-ft-r2_cv-ka",
     "ours"),
]
KA_SYSTEMS += [  # round 3 (docs/preregistration-round3.md); rows appear once their runs exist
    ("MMS-1b-all, kat adapter fine-tune, seed 7", "mms-1b-all-kat-adapter-ft_cv-ka-seed7", "ours (round 3 seed)"),
    ("MMS-1b-all, kat adapter fine-tune, seed 13", "mms-1b-all-kat-adapter-ft_cv-ka-seed13", "ours (round 3 seed)"),
    ("… seed 7 + our word 3-gram LM (same α/β)", "mms-1b-all-kat-adapter-ft_cv-ka-seed7+lm", "ours+decoder (round 3 seed)"),
    ("… seed 13 + our word 3-gram LM (same α/β)", "mms-1b-all-kat-adapter-ft_cv-ka-seed13+lm", "ours+decoder (round 3 seed)"),
    ("Whisper-small (zero-shot), long-form fix", "whisper-small+lf-split", "baseline (FLEURS re-run, §4 fix)"),
    ("Whisper-large-v3 (zero-shot), long-form fix", "whisper-large-v3+lf-split", "baseline (FLEURS re-run, §4 fix)"),
    ("Whisper-large-v3-turbo (zero-shot), long-form fix", "whisper-large-v3-turbo+lf-split", "baseline (FLEURS re-run, §4 fix)"),
    ("Whisper-large-v3-turbo FT r2, long-form fix", "whisper-large-v3-turbo-ft-r2_cv-ka+lf-split", "ours (FLEURS re-run, §4 fix)"),
]
_chunk = "configs/runs/ka/whisper-large-v3-turbo-ft-r2_cv-ka+chunk-selection.yaml"
if os.path.exists(_chunk):  # chunk length selected on dev by scripts/chunk_select.py
    _s = re.search(r"^selected: (\d+)", open(_chunk, encoding="utf-8").read(), re.M).group(1)
    KA_SYSTEMS.append((f"… r2 + chunked decoding (long clips split at pauses into ≤ {_s} s; selected on dev)",
                       f"whisper-large-v3-turbo-ft-r2_cv-ka+chunk{_s}", "ours+decoder"))
KA_SETS = [("cv", "CV ka"), ("fleurs", "FLEURS ka")]
LANG = sys.argv[1] if len(sys.argv) > 1 else "kk"
SYSTEMS, SETS = (KA_SYSTEMS, KA_SETS) if LANG == "ka" else (KK_SYSTEMS, KK_SETS)


def _run(prefix: str, ds: str, split: str) -> str | None:
    runs = sorted(glob.glob(f"runs/{prefix}_{ds}-{LANG}_{split}_*"))
    return runs[-1] if runs else None


def _scores(run: str | None, tag: str = "") -> dict | None:
    if not run:
        return None
    p = os.path.join(run, f"scores{tag}.json")
    return json.load(open(p, encoding="utf-8"))["languages"][LANG] if os.path.exists(p) else None


def pct(x) -> str:
    return "—" if x is None else f"{100 * x:.2f}"


def main_table(split: str) -> list[str]:
    head = ("| Group | System | " + " | ".join(f"{n} WER | {n} CER | {n} 95% CI (WER)" for _, n in SETS)
            + f" | RTFx ({SETS[0][1]}) | GPU ({SETS[0][1]} run) |")
    out = [head, "|" + "---|" * (4 + 3 * len(SETS))]
    for label, prefix, group in SYSTEMS:
        cells, rtfx, gpu = [], "—", "—"
        for ds, _ in SETS:
            m = _scores(_run(prefix, ds, split))
            ci = m.get("wer_ci") if m else None
            cells += [pct(m and m["wer"]), pct(m and m["cer"]), f"{pct(ci['low'])}–{pct(ci['high'])}" if ci else "—"]
            if ds == SETS[0][0] and m and m.get("rtfx"):
                rtfx = f"{m['rtfx']:.0f}"
                man = json.load(open(os.path.join(_run(prefix, ds, split), "manifest.json"), encoding="utf-8"))
                hw = man.get("env", {}).get("hardware", {})
                gpu = (hw.get("gpu") or ("CPU: " + hw["cpu"].split(" (")[0] if hw.get("cpu") else "—")).replace("NVIDIA ", "")
        if any(c != "—" for c in cells):
            out.append(f"| {group} | {label} | " + " | ".join(cells) + f" | {rtfx} | {gpu} |")
    return out


KK_PAIRS = [  # (ours/other, reference system): paired cluster bootstrap on matched clips
    ("whisper-large-v3-turbo-ft_ksc2-sample", "xlsr-kazakh-aismlv"),
    ("whisper-large-v3-turbo-ft_ksc2-sample", "mms-1b-all-kaz"),
    ("whisper-large-v3-turbo-ft_ksc2-sample", "whisper-large-v3-turbo"),
    ("mms-1b-all-kaz-adapter-ft_ksc2-sample", "mms-1b-all-kaz"),
    ("whisper-small-ft_ksc2-sample", "whisper-small"),
    ("whisper-large-v3-turbo-ft_ksc2-sample+beam5", "whisper-large-v3-turbo-ft_ksc2-sample"),
]
KA_PAIRS = [
    ("whisper-large-v3-turbo-ft_cv-ka", "mms-1b-all-kat"),
    ("whisper-large-v3-turbo-ft_cv-ka", "nvidia-stt-ka-fastconformer"),
    ("whisper-large-v3-turbo-ft_cv-ka", "whisper-large-v3-turbo"),
    ("mms-1b-all-kat-adapter-ft_cv-ka", "mms-1b-all-kat"),
    ("whisper-large-v3-turbo-ft_cv-ka", "mms-1b-all-kat-adapter-ft_cv-ka"),
    ("kaldi-gmm-hmm-tri3b", "mms-1b-all-kat"),
    ("whisper-large-v3-turbo-ft_cv-ka", "kaldi-gmm-hmm-tri3b"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "mms-1b-all-kat-adapter-ft_cv-ka"),
    ("mms-1b-all-kat+lm", "mms-1b-all-kat"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "mms-1b-all-kat+lm"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "kaldi-gmm-hmm-tri3b"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "whisper-large-v3-turbo-ft_cv-ka"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "nvidia-stt-ka-fastconformer"),
    ("whisper-large-v3-turbo-ft-r2_cv-ka", "whisper-large-v3-turbo-ft_cv-ka"),
    ("mms-1b-all-kat-adapter-ft_cv-ka+lm", "mms-1b-all-kat"),
    ("whisper-large-v3-turbo-ft-r2_cv-ka+lf-split", "whisper-large-v3-turbo-ft-r2_cv-ka"),
    ("whisper-large-v3+lf-split", "whisper-large-v3"),
    ("whisper-large-v3-turbo-ft-r2_cv-ka+lf-split", "mms-1b-all-kat"),
]
if KA_SYSTEMS[-1][1].startswith("whisper-large-v3-turbo-ft-r2_cv-ka+chunk"):
    KA_PAIRS.append((KA_SYSTEMS[-1][1], "whisper-large-v3-turbo-ft-r2_cv-ka"))
PAIRS = KA_PAIRS if LANG == "ka" else KK_PAIRS


def paired_table(split: str) -> list[str]:
    from asrbench.scoring import compare
    out = ["| Set | B (ours / variant) | A (reference) | WER A | WER B | Δ WER (A−B) | 95% CI | CER A | CER B | Δ CER | 95% CI |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ds, name in SETS:
        for b, a in PAIRS:
            ra, rb = _run(a, ds, split), _run(b, ds, split)
            if not (ra and rb):
                continue
            row = [l for l in compare(ra, rb, "configs/scoring.yaml").splitlines() if l.startswith(f"| {LANG}")][0]
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


KA_INTRO = ["# Georgian results (our language)", "",
            "Generated by `scripts/results_table.py ka` from the committed `runs/*/scores.json`; do not edit by hand.",
            "WER/CER: corpus rates (%) under the declared policy `configs/scoring.yaml`; CI: 95% cluster bootstrap over "
            "speakers (CV) / sentences (FLEURS). Both fine-tunes trained on the official CV 27.0 ka train split "
            "(147.5 h, 139 speakers, speaker-disjoint from dev/test; `runs/train_*`); checkpoint chosen by dev WER; "
            "decoding identical to the corresponding baseline; test run once with frozen configs (baselines frozen in "
            "0c0d0e4, rule for ours in the same commit, before any Georgian test run).",
            "",
            "\\* The NVIDIA model was trained on Common Voice 17.0 train/dev/other (model card), and "
            "`scripts/cv_contamination.py` shows it has seen many of these CV clips (WER 1.8-4.2% on older clip IDs, "
            "23% on the newest). Its CV numbers are not a fair comparison; FLEURS ka test (held out by NVIDIA) is.", "",
            "The MFCC + GMM-HMM rows are a classical baseline we trained from scratch (`recipes/kaldi-gmm-ka/`) on the "
            "same CV train split, on CPU. Unlike the neural baselines (greedy / beam decoding without an external LM) it "
            "decodes with a trigram LM built from CV train transcripts (no dev/test text; 0.1% of dev/test sentences "
            "occur verbatim in train, `docs/split-audit.md`) and a closed 91k-word vocabulary (OOV: 5.6% of CV dev "
            "tokens, 14.8% of FLEURS dev). LM weight and insertion penalty were selected on CV dev "
            "(`recipes/kaldi-gmm-ka/decode-frozen.yaml`). Its output has no case or punctuation, so only normalized "
            "WER/CER apply. RTFx is wall clock on 8 parallel CPU decode jobs, MFCC extraction included.", "",
            "\"+ our word 3-gram LM\" rows decode the CTC model with that same CV-train trigram (pyctcdecode + KenLM, "
            "beam 100). LM weight α and insertion bonus β were selected on dev by a rule committed beforehand "
            "(`scripts/lm_select.py`, `configs/runs/ka/mms-1b-all-kat-adapter-ft_cv-ka+lm-selection.yaml`: α 0.5, β 0), and "
            "the same pair is applied to MMS zero-shot as an ablation that separates the LM's gain from the fine-tune's. "
            "Our MMS fine-tune was rebuilt from the pinned base model + its backed-up adapter "
            "(`scripts/rebuild_mms_adapter.py`; 405/409 FLEURS dev hypotheses identical to the original greedy run).", ""]


def ortho_table(split: str) -> list[str]:
    """Orthographic WER/CER (case and punctuation kept, Unicode form only) next to the normalized primary numbers,
    plus what each system emitted on references that are empty after normalization (CV: 1 corrupted reference)."""
    out = ["| Group | System | " + " | ".join(f"{n} WER norm. | {n} WER ortho. | {n} CER ortho." for _, n in SETS)
           + " | Empty-reference clips: items / words emitted (CV) |", "|" + "---|" * (3 + 3 * len(SETS))]
    for label, prefix, group in SYSTEMS:
        cells, sil = [], "—"
        for ds, _ in SETS:
            m = _scores(_run(prefix, ds, split))
            o = (m or {}).get("orthographic") or {}
            cells += [pct(m and m["wer"]), pct(o.get("wer")), pct(o.get("cer"))]
            if ds == "cv" and m and m.get("silence"):
                sil = f"{m['silence']['silent_items']} / {m['silence']['emitted_words']}"
        if any(c != "—" for c in cells):
            out.append(f"| {group} | {label} | " + " | ".join(cells) + f" | {sil} |")
    return out


def seed_table(split: str) -> list[str]:
    """Round 3 §1: MMS adapter FT over training seeds {42, 7, 13}; mean ± sample SD of corpus WER/CER."""
    import statistics
    out = []
    for kind, suffix in (("greedy CTC", ""), ("beam 100 + word 3-gram LM", "+lm")):
        prefixes = [f"mms-1b-all-kat-adapter-ft_cv-ka{suffix}"] + [f"mms-1b-all-kat-adapter-ft_cv-ka-seed{s}{suffix}"
                                                                   for s in (7, 13)]
        for ds, name in SETS:
            ms = [_scores(_run(p, ds, split)) for p in prefixes]
            if not all(ms):
                continue
            w, c = [100 * m["wer"] for m in ms], [100 * m["cer"] for m in ms]
            out.append(f"| {kind} | {name} | " + " | ".join(f"{x:.2f}" for x in w)
                       + f" | {statistics.mean(w):.2f} ± {statistics.stdev(w):.2f} | "
                       + f"{statistics.mean(c):.2f} ± {statistics.stdev(c):.2f} |")
    if out:
        out = ["| Decoder | Set | WER seed 42 | WER seed 7 | WER seed 13 | WER mean ± SD | CER mean ± SD |",
               "|---|---|---|---|---|---|---|"] + out
    return out


if __name__ == "__main__" and LANG == "ka":
    lines = list(KA_INTRO)
    for split, title in (("test", "Test (frozen, run once)"), ("dev", "Dev (selection)")):
        lines += [f"## {title}", ""] + main_table(split) + [""]
        lines += [f"### Paired comparisons ({split})", "", "Positive Δ = B has fewer errors than A. Cluster bootstrap "
                  "(2000 resamples) on matched clip IDs.", ""] + paired_table(split) + [""]
        seeds = seed_table(split)
        if seeds:
            lines += [f"### Training-seed variance, MMS adapter FT ({split}, round 3)", ""] + seeds + [""]
        lines += [f"### Orthographic scores and empty references ({split})", "",
                  "Primary numbers are normalized (`configs/scoring.yaml`). Orthographic WER/CER keep case and "
                  "punctuation, so they also count punctuation as words: CTC systems and the GMM-HMM output none, "
                  "Whisper fine-tunes learned it from the orthographic CV transcripts.", ""] + ortho_table(split) + [""]
    print("\n".join(lines))
elif __name__ == "__main__":
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
