"""Command-line entry point: `uv run asrbench <command> --help`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(prog="asrbench", description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("import-fleurs", help="Download a FLEURS language (pinned revision) and write a manifest")
    p.add_argument("config", help="FLEURS config, e.g. sw_ke, tr_tr, el_gr")
    p.add_argument("--splits", nargs="+", default=["dev"], choices=["train", "dev", "test"])
    p.add_argument("--language", help="code stored in the manifest (default: prefix of config)")
    p.add_argument("--out", default="data", help="data root (default: data/)")

    p = sub.add_parser("import-ksc2", help="Stream ISSAI KSC2 (Kazakh): all of dev/test + a fixed train fraction")
    p.add_argument("--train-fraction", type=float, default=0.03, help="share of Train kept (default 0.03 ~ 35 h)")
    p.add_argument("--out", default="data", help="data root (default: data/)")

    p = sub.add_parser("import-tsv", help="Write a manifest from a local TSV (id, audio, reference, split, speaker, session)")
    p.add_argument("tsv")
    p.add_argument("--language", required=True)
    p.add_argument("--out", required=True, help="output manifest .jsonl")

    p = sub.add_parser("validate", help="Check a manifest: duplicate IDs, missing audio, speaker/session leakage")
    p.add_argument("manifest")

    p = sub.add_parser("run", help="Transcribe a split and save raw predictions + run manifest")
    p.add_argument("config")
    p.add_argument("--runs-dir", default="runs")
    p.add_argument("--resume", help="existing run directory to continue")

    p = sub.add_parser("train", help="Fine-tune a checkpoint on the train split, select on dev (our contribution)")
    p.add_argument("config")
    p.add_argument("--checkpoints-dir", default="checkpoints", help="where weights go (gitignored)")
    p.add_argument("--runs-dir", default="runs", help="where the training manifest + log go (commit these)")
    p.add_argument("--policy", default="configs/scoring.yaml", help="scoring policy for dev selection")

    p = sub.add_parser("score", help="Score a run directory per language")
    p.add_argument("run_dir")
    p.add_argument("--policy", default="configs/scoring.yaml")
    p.add_argument("--n-boot", type=int, default=2000)

    p = sub.add_parser("compare", help="Paired comparison of two runs on matched items")
    p.add_argument("run_a")
    p.add_argument("run_b")
    p.add_argument("--policy", default="configs/scoring.yaml")
    p.add_argument("--n-boot", type=int, default=2000)

    a = ap.parse_args(argv)

    if a.cmd == "import-fleurs":
        from .dataset import load_manifest, summary
        from .importers import import_fleurs
        path = import_fleurs(a.config, a.splits, Path(a.out), language=a.language)
        print(f"Wrote {path}")
        print(json.dumps(summary(load_manifest(path)), indent=2))
    elif a.cmd == "import-ksc2":
        from .dataset import load_manifest, summary
        from .importers import import_ksc2
        path = import_ksc2(Path(a.out), a.train_fraction)
        print(f"Wrote {path}")
        print(json.dumps(summary(load_manifest(path)), indent=2))
    elif a.cmd == "import-tsv":
        from .importers import import_tsv
        print(f"Wrote {import_tsv(Path(a.tsv), a.language, Path(a.out))}")
    elif a.cmd == "validate":
        from .dataset import load_manifest, summary, validate
        m = load_manifest(a.manifest)
        problems = validate(m)
        print(json.dumps(summary(m), indent=2))
        for pr in problems:
            print("PROBLEM:", pr)
        print("OK" if not problems else f"{len(problems)} problem(s)")
        return 1 if problems else 0
    elif a.cmd == "run":
        from .runner import run
        out = run(a.config, a.runs_dir, a.resume)
        print(f"Run directory: {out}\nNext: asrbench score {out.as_posix()}")
    elif a.cmd == "train":
        from .train import train
        final = train(a.config, a.checkpoints_dir, a.runs_dir, a.policy)
        print(f"Saved {final.as_posix()}\nNext: set model.id to this path in a run config and `asrbench run` it "
              "on dev, then on the frozen test set alongside the baselines.")
    elif a.cmd == "score":
        from .scoring import score
        policy = a.policy if Path(a.policy).exists() else None
        res = score(a.run_dir, policy, a.n_boot)
        print((Path(a.run_dir) / "report.md").read_text(encoding="utf-8").split("\n## ")[0])
        _ = res
    elif a.cmd == "compare":
        from .scoring import compare
        policy = a.policy if Path(a.policy).exists() else None
        print(compare(a.run_a, a.run_b, policy, a.n_boot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
