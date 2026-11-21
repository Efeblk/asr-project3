"""Generate the round-3 run configs (docs/preregistration-round3.md) from the frozen round-1/2 configs.

  speed:  every frozen CV ka test config -> a dev-subset speed config (first 500 CV dev clips by ID, batch 8,
          everything else unchanged), so all systems are timed on the same GPU, clips and batch size.
  seed S: the four frozen MMS-FT test configs (CV/FLEURS x plain/+LM) and their dev twins -> the same configs with
          only the checkpoint path and run name changed to the seed-S fine-tune.

Usage:
  python scripts/round3_configs.py speed
  python scripts/round3_configs.py seed 7 checkpoints/mms-1b-all-kat-adapter-ft_cv-ka-seed7_<ts>/final
  python scripts/round3_configs.py decoder   # dev-only CTC decoder ablation (preregistration §3)
"""
import sys
from pathlib import Path

import yaml

KA = Path("configs/runs/ka")
OUT = KA / "round3"
SPEED_LIMIT = 500
SPEED_BATCH = 8
BASE = "mms-1b-all-kat-adapter-ft_cv-ka"
BASE_CKPT = "checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_20261119T014308Z/final"


def dump(cfg: dict, path: Path, header: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(header + yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    print(path)


def speed() -> None:
    for src in sorted(KA.glob("*_cv-test.yaml")):
        if src.name.startswith("whisper-large-v3-turbo-ft_cv-ka_"):
            continue  # r1 weights were not kept (report §6); r2 is the same recipe
        cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
        cfg["name"] = f"speed4070_{cfg['name'].removesuffix('_cv-ka_test')}_cv-ka_dev{SPEED_LIMIT}"
        cfg["split"] = "dev"
        cfg["limit"] = SPEED_LIMIT
        cfg["batch_size"] = SPEED_BATCH
        cfg.pop("frozen", None)
        if cfg["model"].get("lm"):
            cfg["model"]["lm"]["workers"] = 12
        dump(cfg, OUT / "speed" / src.name.replace("_cv-test.yaml", "_speed.yaml"),
             f"# Round 3 speed benchmark, generated from {src.name} by scripts/round3_configs.py.\n"
             f"# Same GPU, first {SPEED_LIMIT} CV ka dev clips by ID, batch {SPEED_BATCH}; model/decoder unchanged.\n")


def seed(s: int, ckpt: str) -> None:
    for kind in ("", "+lm"):
        for corpus in ("cv", "fleurs"):
            for split in ("dev", "test"):
                src = KA / f"{BASE}{kind}_{corpus}-{split}.yaml"
                cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
                assert cfg["model"]["id"] == BASE_CKPT, (src, cfg["model"]["id"])
                cfg["model"]["id"] = ckpt
                cfg["name"] = cfg["name"].replace(BASE, f"{BASE}-seed{s}", 1)
                if split == "test":
                    cfg["frozen"] = True
                dump(cfg, OUT / f"seed{s}" / src.name.replace(BASE, f"{BASE}-seed{s}", 1),
                     f"# Round 3 seed {s}, generated from {src.name} by scripts/round3_configs.py: only the checkpoint\n"
                     f"# and the name differ. LM alpha/beta stay as selected in round 2 (no reselection).\n")


def decoder() -> None:
    variants = {
        "greedy-valid": lambda m: m.update(greedy_valid_frames=True),
        "beam100-nolm": lambda m: m.update(lm={"arpa": None, "alpha": 0.0, "beta": 0.0, "beam_width": 100,
                                               "workers": 12}),
    }
    for base in ("mms-1b-all-kat-adapter-ft_cv-ka", "mms-1b-all-kat"):
        for corpus in ("cv", "fleurs"):
            src = KA / f"{base}_{corpus}-dev.yaml"
            for tag, apply in variants.items():
                cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
                assert cfg["split"] == "dev" and not cfg["model"].get("lm"), src
                apply(cfg["model"])
                cfg["name"] = cfg["name"].replace(base, f"{base}+{tag}", 1)
                dump(cfg, OUT / "decoder" / f"{base}+{tag}_{corpus}-dev.yaml",
                     f"# Round 3 decoder ablation (dev only), generated from {src.name} by scripts/round3_configs.py.\n"
                     f"# Variant {tag}; everything else unchanged.\n")


def decoder_control() -> None:
    """Added after review (not pre-registered), dev only: the frozen greedy dev configs re-run unchanged on the GPU
    that ran the decoder variants, so the ablation ladder compares decoders on one GPU."""
    for base in ("mms-1b-all-kat-adapter-ft_cv-ka", "mms-1b-all-kat"):
        for corpus in ("cv", "fleurs"):
            src = KA / f"{base}_{corpus}-dev.yaml"
            cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
            assert cfg["split"] == "dev" and not cfg["model"].get("lm"), src
            cfg["name"] = cfg["name"].replace(base, f"{base}+greedy-samegpu", 1)
            dump(cfg, OUT / "decoder" / f"{base}+greedy-samegpu_{corpus}-dev.yaml",
                 f"# Round 3 decoder ablation control (dev only, added after review), generated from {src.name} by\n"
                 f"# scripts/round3_configs.py: unchanged greedy config, re-run on the GPU used for the decoder variants.\n")


LFFIX_SYSTEMS =("whisper-small", "whisper-large-v3", "whisper-large-v3-turbo", "whisper-large-v3-turbo-ft-r2_cv-ka")


def lffix() -> None:
    """Preregistration §4: FLEURS re-runs of every Whisper system whose frozen FLEURS runs hit the batch long-form
    bug. Only `long_form: split` is new; everything else, test freezing included, is copied from the original."""
    for base in LFFIX_SYSTEMS:
        for split in ("dev", "test"):
            src = KA / f"{base}_fleurs-{split}.yaml"
            cfg = yaml.safe_load(src.read_text(encoding="utf-8"))
            assert cfg["model"]["family"] == "hf-whisper" and not cfg["model"].get("chunk_seconds"), src
            cfg["model"]["long_form"] = "split"
            cfg["batch_size"] = 16  # decoding is batch-independent after the fix; 16 fits a 12 GB GPU
            cfg["name"] = cfg["name"].replace(base, f"{base}+lf-split", 1)
            assert cfg["name"] != base
            dump(cfg, OUT / "lffix" / f"{base}+lf-split_fleurs-{split}.yaml",
                 f"# Round 3 §4 bug-fix re-run, generated from {src.name} by scripts/round3_configs.py.\n"
                 f"# Changes: model.long_form = split (no batch-wide timestamped long-form decoding); batch 16\n"
                 f"# (12 GB GPU; decoding no longer depends on the batch).\n")


if __name__ == "__main__":
    if sys.argv[1] == "speed":
        speed()
    elif sys.argv[1] == "lffix":
        lffix()
    elif sys.argv[1] == "decoder":
        decoder()
    elif sys.argv[1] == "decoder-control":
        decoder_control()
    elif sys.argv[1] == "seed":
        seed(int(sys.argv[2]), sys.argv[3])
    else:
        raise SystemExit(__doc__)
