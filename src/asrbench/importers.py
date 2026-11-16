"""Build dataset manifests from sources with trusted human references.

- FLEURS (google/fleurs, CC-BY-4.0): ~100 languages, read Wikipedia sentences, train/dev/test
  splits. Files are fetched at a pinned dataset revision so manifests are reproducible.
  FLEURS has no speaker IDs; the same sentence is read by several speakers, so the sentence ID
  is used as the bootstrap cluster (`session`).
- TSV: any local corpus (your own recordings with independently made transcripts, Common Voice
  exports, ...). Columns: id, audio, reference, split, and optionally speaker, session.
"""

from __future__ import annotations

import csv
import tarfile
from pathlib import Path

from .dataset import Item, write_manifest
from .eligibility import check_language

FLEURS_REPO = "google/fleurs"
FLEURS_REVISION = "70bb2e84b976b7e960aa89f1c648e09c59f894dd"
FLEURS_SPLITS = {"train": "train", "dev": "dev", "test": "test"}
SAMPLE_RATE = 16000


def import_fleurs(config: str, splits: list[str], out_dir: Path, language: str | None = None,
                  revision: str = FLEURS_REVISION) -> Path:
    """config: FLEURS config like 'sw_ke'. language: code stored in the manifest (default: 'sw')."""
    from huggingface_hub import hf_hub_download

    language = language or config.split("_")[0]
    check_language(language)
    root = out_dir / "fleurs" / config
    items: list[Item] = []
    for split in splits:
        tsv = hf_hub_download(FLEURS_REPO, f"data/{config}/{FLEURS_SPLITS[split]}.tsv",
                              repo_type="dataset", revision=revision)
        audio_dir = root / split
        if not audio_dir.exists() or not any(audio_dir.iterdir()):
            tar = hf_hub_download(FLEURS_REPO, f"data/{config}/audio/{FLEURS_SPLITS[split]}.tar.gz",
                                  repo_type="dataset", revision=revision)
            audio_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(tar) as tf:
                for m in tf.getmembers():
                    if m.isfile() and m.name.endswith(".wav"):
                        m.name = Path(m.name).name
                        tf.extract(m, audio_dir, filter="data")
        with open(tsv, encoding="utf-8", newline="") as f:
            for row in csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
                sent_id, fname, raw, _norm, _chars, n_samples, gender = row[:7]
                items.append(Item(
                    id=f"fleurs-{config}-{split}-{Path(fname).stem}",
                    audio=f"{split}/{fname}",
                    reference=raw,
                    language=language,
                    split=split,
                    session=f"sent{sent_id}",
                    duration=int(n_samples) / SAMPLE_RATE,
                    source=f"{FLEURS_REPO}@{revision[:12]}:{config}",
                    extra={"gender": gender.lower()},
                ))
    return write_manifest(items, root / "manifest.jsonl")


def import_tsv(tsv_path: Path, language: str, out_path: Path, source: str | None = None) -> Path:
    """Audio paths in the TSV are resolved relative to the TSV and rewritten relative to out_path."""
    import soundfile as sf

    check_language(language)
    tsv_path, out_path = Path(tsv_path), Path(out_path)
    items: list[Item] = []
    with open(tsv_path, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE):
            audio = (tsv_path.parent / row["audio"]).resolve()
            try:
                duration = sf.info(str(audio)).duration
            except Exception:
                duration = None
            rel = Path(_relpath(audio, out_path.parent.resolve()))
            items.append(Item(
                id=row["id"], audio=rel.as_posix(), reference=row.get("reference", ""), language=language,
                split=row["split"], speaker=row.get("speaker") or None, session=row.get("session") or None,
                duration=duration, source=source or tsv_path.name,
            ))
    return write_manifest(items, out_path)


def _relpath(path: Path, start: Path) -> str:
    import os
    try:
        return os.path.relpath(path, start)
    except ValueError:  # different drive on Windows
        return str(path)
