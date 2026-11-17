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


# --- KSC2 (ISSAI Kazakh Speech Corpus 2) -------------------------------------------------------
KSC2_REPO = "issai/Kazakh_Speech_Corpus_2"
KSC2_PARTS = [f"ISSAI_KSC2.tar.gz.parta{c}" for c in "abcdefghij"]
KSC2_SPLITS = {"Train": "train", "Dev": "dev", "Test": "test"}


class _ConcatHTTPStream:
    """Read the split tar.gz parts as one byte stream, resuming a part with a Range request on errors."""

    def __init__(self, urls: list[str], log=print):
        self.urls, self.log = urls, log
        self.i, self.offset, self.resp, self.total = 0, 0, None, 0

    def _open(self):
        import urllib.request
        req = urllib.request.Request(self.urls[self.i], headers={"Range": f"bytes={self.offset}-"} if self.offset else {})
        self.resp = urllib.request.urlopen(req, timeout=60)

    def read(self, n: int = -1) -> bytes:
        import time
        while self.i < len(self.urls):
            if self.resp is None:
                self._open()
            for attempt in range(5):
                try:
                    b = self.resp.read(n)
                    break
                except Exception as e:  # dropped connection: reopen at the current offset
                    self.log(f"  read error on part {self.i} at {self.offset}: {e}; retry {attempt + 1}")
                    time.sleep(5 * (attempt + 1))
                    self._open()
            else:
                raise RuntimeError("KSC2 download failed repeatedly")
            if b:
                self.offset += len(b)
                self.total += len(b)
                return b
            self.i, self.offset, self.resp = self.i + 1, 0, None
            if self.i < len(self.urls):
                self.log(f"  part {self.i + 1}/{len(self.urls)} ({self.total / 1e9:.1f} GB streamed)")
        return b""


def _keep_train(stem: str, fraction: float) -> bool:
    import hashlib
    return int(hashlib.sha1(stem.encode()).hexdigest()[:8], 16) / 0xFFFFFFFF < fraction


def import_ksc2(out_dir: Path, train_fraction: float = 0.03, revision: str | None = None, log=print) -> Path:
    """Stream KSC2 (~81 GB, CC BY 4.0) once without storing the archive. Keeps all of Dev and Test and a
    deterministic `train_fraction` of Train (sha1 of the utterance ID), so the subset is reproducible.

    KSC2 has no speaker IDs, so bootstrap clusters fall back to items; its own Train/Dev/Test split is kept.
    Transcripts are lowercase, unpunctuated, with numbers written as words.
    """
    import soundfile as sf
    from huggingface_hub import HfApi

    check_language("kk")
    sha = revision or HfApi().dataset_info(KSC2_REPO).sha
    urls = [f"https://huggingface.co/datasets/{KSC2_REPO}/resolve/{sha}/{p}" for p in KSC2_PARTS]
    root = out_dir / "ksc2"
    texts: dict[tuple[str, str, str], str] = {}
    audio: dict[tuple[str, str, str], str] = {}
    seen = {"train": 0, "dev": 0, "test": 0}
    with tarfile.open(fileobj=_ConcatHTTPStream(urls, log), mode="r|gz") as tf:
        for m in tf:
            parts = m.name.split("/")
            if not m.isfile() or len(parts) != 4 or parts[1] not in KSC2_SPLITS:
                continue
            split, sub, fname = KSC2_SPLITS[parts[1]], parts[2], parts[3]
            stem, ext = fname.rsplit(".", 1)
            key = (split, sub, stem)
            if ext == "flac":
                seen[split] += 1
                if seen[split] % 20000 == 0:
                    log(f"  {seen}")
            if split == "train" and not _keep_train(stem, train_fraction):
                continue
            if ext == "txt":
                texts[key] = tf.extractfile(m).read().decode("utf-8").strip()
            elif ext == "flac":
                dest = root / split / sub
                dest.mkdir(parents=True, exist_ok=True)
                m.name = fname
                tf.extract(m, dest, filter="data")
                audio[key] = f"{split}/{sub}/{fname}"
    items = []
    for key in sorted(audio):
        if key not in texts:
            log(f"  no transcript for {key}; skipped")
            continue
        split, sub, stem = key
        try:
            duration = sf.info(str(root / audio[key])).duration
        except Exception:
            duration = None
        items.append(Item(id=f"ksc2-{split}-{sub}-{stem}", audio=audio[key], reference=texts[key], language="kk",
                          split=split, duration=duration, source=f"{KSC2_REPO}@{sha[:12]}",
                          extra={"subcorpus": sub, "train_fraction": train_fraction if split == "train" else 1.0}))
    log(f"Utterances in the corpus: {seen}; kept {len(items)}")
    return write_manifest(items, root / "manifest.jsonl")
