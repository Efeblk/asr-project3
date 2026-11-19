"""CTC + word n-gram LM decoding for Georgian: dev grid, the selection rule, and the frozen test configs.

Why: the error analysis (docs/error-analysis-georgian.md §4, §7) shows that about half of the CTC models' word
errors are a single character away from the reference, and that a word trigram LM is worth a lot on CV
(the GMM-HMM beats MMS greedy on WER with ~2x its CER). The LM is the one we built for the GMM-HMM baseline:
trigram Kneser-Ney on the CV ka TRAIN transcripts only (recipes/kaldi-gmm-ka, stage 1: data/local/lm/tg.arpa.gz,
gunzipped to lm/ka_cv_train_tg.arpa). Decoding: pyctcdecode beam search (beam 100) with KenLM; a DECODING change,
reported as its own row next to the unchanged (greedy) model.

Rule (committed before any LM-decoded dev run):
  alpha (LM weight) in ALPHAS x beta (word insertion bonus) in BETAS; pick the pair with the lowest mean of
  CV ka dev WER and FLEURS ka dev WER (full dev sets); ties -> smaller alpha, then smaller beta.
  The same pair is then used for every model decoded with this LM (ours and the MMS zero-shot ablation).

    python scripts/lm_select.py dev  <model-name>          # write the dev grid configs
    python scripts/lm_select.py test <model-name> [others]  # apply the rule to <model-name>'s dev runs; write
                                                            # "+lm" dev + frozen test configs for it and [others]
"""

from __future__ import annotations

import glob
import json
import sys

import yaml

ALPHAS = [0.3, 0.5, 0.8, 1.2]
BETAS = [0.0, 1.0, 2.0]
SETS = ["cv", "fleurs"]
CFG = "configs/runs/ka"
LM = {"arpa": "lm/ka_cv_train_tg.arpa",
      "arpa_sha256": "1eab5b3af5ece42c93c04473155613cf928d0b342e44f0e37afa64eafe953547", "beam_width": 100, "workers": 12}


def tag(a: float, b: float) -> str:
    return f"+lm-a{a}-b{b}"


def write(name: str, ds: str, split: str, suffix: str, a: float, b: float, note: str) -> str:
    src = f"{CFG}/{name}_{ds}-{split}.yaml"
    cfg = yaml.safe_load(open(src, encoding="utf-8"))
    cfg["name"] = cfg["name"].replace(name, name + suffix, 1)
    cfg["model"]["lm"] = {**LM, "alpha": a, "beta": b}
    head = (f"# Georgian: {src.split('/')[-1]} decoded with our CV-train word trigram LM (alpha {a}, beta {b}, beam 100;\n"
            f"# scripts/lm_select.py). {note}\n")
    out = f"{CFG}/{name}{suffix}_{ds}-{split}.yaml"
    open(out, "w", encoding="utf-8", newline="\n").write(head + yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True))
    return out


def dev_wer(name: str, suffix: str, ds: str) -> float:
    runs = sorted(glob.glob(f"runs/{name}{suffix}_{ds}-ka_dev_*"))
    if not runs:
        raise SystemExit(f"missing dev run {name}{suffix} on {ds}")
    return json.load(open(f"{runs[-1]}/scores.json", encoding="utf-8"))["languages"]["ka"]["wer"]


def main() -> None:
    mode, name, others = sys.argv[1], sys.argv[2], sys.argv[3:]
    grid = [(a, b) for a in ALPHAS for b in BETAS]
    if mode == "dev":
        for a, b in grid:
            for ds in SETS:
                print(write(name, ds, "dev", tag(a, b), a, b, "Dev grid candidate."))
        return
    table = {(a, b): {ds: dev_wer(name, tag(a, b), ds) for ds in SETS} for a, b in grid}
    a, b = min(grid, key=lambda p: (sum(table[p].values()) / len(SETS), p[0], p[1]))
    sel = {"model": name, "rule": "min mean(CV dev WER, FLEURS dev WER); ties -> smaller alpha, then beta",
           "alphas": ALPHAS, "betas": BETAS,
           "dev_wer": [{"alpha": p[0], "beta": p[1], **{ds: round(100 * w, 2) for ds, w in v.items()}} for p, v in table.items()],
           "selected": {"alpha": a, "beta": b}, "applied_to": [name, *others]}
    open(f"{CFG}/{name}+lm-selection.yaml", "w", encoding="utf-8", newline="\n").write(yaml.safe_dump(sel, sort_keys=False))
    for m in [name, *others]:
        for ds in SETS:
            print(write(m, ds, "dev", "+lm", a, b, f"Selected on dev ({name}+lm-selection.yaml)."))
            print(write(m, ds, "test", "+lm", a, b, f"FROZEN TEST RUN, run once; alpha/beta selected on dev ({name}+lm-selection.yaml)."))
    print(json.dumps(sel["selected"]))


if __name__ == "__main__":
    main()
