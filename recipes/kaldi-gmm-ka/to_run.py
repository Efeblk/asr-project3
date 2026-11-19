"""Turn a Kaldi decode of the Georgian GMM-HMM into an asrbench run directory, then score it like any system.

    uv run python recipes/kaldi-gmm-ka/to_run.py --work //wsl.localhost/Ubuntu/home/<user>/ka_gmm --model tri3b --set cv_dev
    uv run python recipes/kaldi-gmm-ka/to_run.py --work ... --model tri3b --set cv_test   # needs decode-frozen.yaml

Reads <work>/exp/<model>/decode_tg_<set>/{hyp.frozen.txt,wall_sec}, <work>/data/<set>/uttmap and the repo manifest,
and writes runs/kaldi-gmm-hmm-<model>_<corpus>-ka_<split>_<UTC>/{config.yaml,manifest.json,predictions.jsonl}.
The hypothesis is the Kaldi one-best word string at the LM weight / insertion penalty selected on CV dev
(recipes/kaldi-gmm-ka/decode-frozen.yaml). Its words are already in normalized form (lower case, no punctuation),
so orthographic WER/CER are not meaningful for this system. Timing: wall clock of MFCC+CMVN extraction plus the
two-pass fMLLR decode on CPU (parallel jobs), excluding graph building; per-clip compute_sec is that wall time
pro-rated by duration, so only the corpus RTFx is meaningful.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import yaml

from asrbench import envinfo
from asrbench.dataset import load_manifest

MANIFESTS = {"cv": "data/cv/ka/manifest.jsonl", "fleurs": "data/fleurs/ka_ge/manifest.jsonl"}
DESCR = {
    "tri3b": "MFCC(13)+splice(±3)+LDA(40)+MLLT, speaker-adaptive (fMLLR/SAT) triphone GMM-HMM, 4000 leaves / 40k Gaussians",
    "tri2b": "MFCC(13)+splice(±3)+LDA(40)+MLLT triphone GMM-HMM (no speaker adaptation), 4000 leaves / 40k Gaussians",
}
REC = Path(__file__).resolve().parent


def wsl_cpu() -> str:
    try:
        out = subprocess.run(["wsl.exe", "-d", "Ubuntu", "--", "sh", "-c", "grep -m1 'model name' /proc/cpuinfo; nproc"],
                             capture_output=True, text=True, check=True).stdout.splitlines()
        return f"{out[0].split(':', 1)[1].strip()} ({out[1]} threads, WSL2 Ubuntu 24.04)"
    except Exception:
        return "CPU (WSL2)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="Kaldi work dir (~/ka_gmm), as seen from this machine")
    ap.add_argument("--model", default="tri3b", choices=sorted(DESCR))
    ap.add_argument("--set", required=True, help="cv_dev | cv_test | fleurs_dev | fleurs_test")
    ap.add_argument("--runs-dir", default="runs")
    a = ap.parse_args()
    corpus, split = a.set.split("_")
    work = Path(a.work)
    dec = work / "exp" / a.model / f"decode_tg_{a.set}"
    frozen = yaml.safe_load((REC / "decode-frozen.yaml").read_text(encoding="utf-8"))
    if split == "test" and not (frozen and "lmwt" in frozen):
        raise SystemExit("decode-frozen.yaml (selected on CV dev) is required before a test run")

    uttmap = dict(l.split("\t") for l in (work / "data" / a.set / "uttmap").read_text(encoding="utf-8").splitlines())
    hyps = {}
    for line in (dec / "hyp.frozen.txt").read_text(encoding="utf-8").splitlines():
        utt, _, words = line.partition(" ")
        hyps[uttmap[utt]] = " ".join(w for w in words.split() if w != "<UNK>")
    ds = load_manifest(MANIFESTS[corpus])
    items = ds.select(split, ["ka"])
    wall = float((dec / "wall_sec").read_text().strip())
    total = sum(it.duration or 0 for it in items)

    stats = json.loads((work / "prep" / "stats.json").read_text(encoding="utf-8"))
    with gzip.open(work / "data" / "local" / "lm" / "tg.arpa.gz", "rt", encoding="utf-8") as f:
        ngrams = {}
        for line in f:
            m = re.match(r"ngram (\d)=(\d+)", line)
            if m:
                ngrams[f"{m.group(1)}-grams"] = int(m.group(2))
            elif line.startswith("\\1-grams"):
                break

    name = f"kaldi-gmm-hmm-{a.model}_{corpus}-ka_{split}"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(a.runs_dir) / f"{name}_{stamp}"
    out.mkdir(parents=True)
    cfg = {"name": name, "dataset": MANIFESTS[corpus], "split": split, "languages": ["ka"], "eligibility_confirmed": True,
           "model": {"family": "kaldi-gmm-hmm", "id": f"recipes/kaldi-gmm-ka ({a.model})"},
           "decode": {"lmwt": frozen["lmwt"], "word_ins_penalty": frozen["word_ins_penalty"],
                      "selected_on": "CV ka dev (decode-frozen.yaml)", "beams": "Kaldi decode_fmllr.sh / decode.sh defaults"},
           "frozen": split == "test"}
    (out / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    env = envinfo.capture()
    env["hardware"] = {"cpu": wsl_cpu(), "kaldi": "5.5.1068 (conda-forge cpu build); steps/utils kaldi-asr/kaldi e02e35f0"}
    missing = [it.id for it in items if it.id not in hyps]
    manifest = {
        "name": name, "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task": "transcribe (same-language ASR)", "split": split, "languages": ["ka"],
        "dataset": {"path": MANIFESTS[corpus], "sha256": ds.sha256(), "items": len(items), "limit": None},
        "model": {
            "trained_by_us": None, "family": "kaldi-gmm-hmm", "model_id": f"kaldi-gmm-hmm-{a.model} (recipes/kaldi-gmm-ka)",
            "revision_resolved": env.get("git_commit"), "device": "cpu", "dtype": "float32", "language_hints": {},
            "system": (f"**baseline, trained by us from scratch** (standard MFCC + GMM-HMM, A3): {DESCR[a.model]}; "
                       f"graphemic lexicon ({stats['lexicon']['words']} words), trigram KN LM on CV ka train text only; "
                       f"trained on CV 27.0 ka train ({stats['sets']['cv_train']['hours']} h)"),
            "settings": {"lexicon_words": stats["lexicon"]["words"], "phones": len(stats["lexicon"]["phones"]),
                         "lm": {"order": 3, "smoothing": "Kneser-Ney (utils/lang/make_kn_lm.py)", **ngrams},
                         "oov_token_rate": stats["sets"][a.set].get("oov_token_rate"), **cfg["decode"]},
        },
        "batch_size": None,
        "timing_boundary": "wall clock of MFCC+CMVN extraction and decoding (incl. fMLLR 2nd pass) over parallel CPU jobs; "
                           "graph building and model loading excluded; per-clip compute_sec is pro-rated by duration",
        "chunking": "none (whole clips)",
        "env": env,
        "missing_hypotheses": missing,
    }
    with (out / "predictions.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for it in items:
            d = it.duration or 0
            f.write(json.dumps({"id": it.id, "language": "ka", "reference": it.reference, "hypothesis": hyps.get(it.id, ""),
                                "audio_sec": round(d, 3), "compute_sec": round(wall * d / total, 4),
                                "speaker": it.speaker, "session": it.session}, ensure_ascii=False) + "\n")
    manifest["completed_utc"] = manifest["created_utc"]
    manifest["totals"] = {"items": len(items), "audio_sec": round(total, 2), "compute_sec": wall, "rtf": round(wall / total, 4)}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(f"Run directory: {out}  ({len(missing)} items without hypothesis)")


if __name__ == "__main__":
    main()
