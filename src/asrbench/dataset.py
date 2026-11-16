"""Dataset manifests: one JSON object per line, one line per evaluation item.

Required fields: id, audio, reference, language, split.
Optional: speaker, session, duration (seconds), source.
`audio` is a path relative to the manifest file (or absolute).
An empty `reference` means the clip is labelled as containing no speech (silence report, S76).
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path

SPLITS = ("train", "dev", "test")


@dataclass
class Item:
    id: str
    audio: str
    reference: str
    language: str
    split: str
    speaker: str | None = None
    session: str | None = None
    duration: float | None = None
    source: str | None = None
    extra: dict = field(default_factory=dict)

    def cluster_key(self) -> str:
        """Unit for bootstrap resampling: session, else speaker, else the item itself (S24, S27)."""
        return self.session or self.speaker or self.id


@dataclass
class Manifest:
    path: Path
    items: list[Item]

    @property
    def root(self) -> Path:
        return self.path.parent

    def audio_path(self, item: Item) -> Path:
        p = Path(item.audio)
        return p if p.is_absolute() else self.root / p

    def select(self, split: str | None = None, languages: list[str] | None = None) -> list[Item]:
        out = self.items
        if split:
            out = [i for i in out if i.split == split]
        if languages:
            out = [i for i in out if i.language in set(languages)]
        return out

    def sha256(self) -> str:
        return hashlib.sha256(self.path.read_bytes()).hexdigest()


_KNOWN = {f for f in Item.__dataclass_fields__ if f != "extra"}


def load_manifest(path: str | Path) -> Manifest:
    path = Path(path)
    items = []
    with path.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            missing = {"id", "audio", "reference", "language", "split"} - row.keys()
            if missing:
                raise ValueError(f"{path}:{n} missing fields {sorted(missing)}")
            known = {k: v for k, v in row.items() if k in _KNOWN}
            extra = {k: v for k, v in row.items() if k not in _KNOWN}
            items.append(Item(**known, extra=extra))
    return Manifest(path, items)


def write_manifest(items: list[Item], path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for it in items:
            row = {k: v for k, v in asdict(it).items() if k != "extra" and v is not None}
            row.update(it.extra)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return path


def validate(manifest: Manifest, check_audio: bool = True) -> list[str]:
    """Return a list of problems (empty = OK)."""
    problems: list[str] = []
    seen: set[str] = set()
    for it in manifest.items:
        if it.id in seen:
            problems.append(f"duplicate id {it.id}")
        seen.add(it.id)
        if it.split not in SPLITS:
            problems.append(f"{it.id}: split '{it.split}' not in {SPLITS}")
        if check_audio and not manifest.audio_path(it).exists():
            problems.append(f"{it.id}: audio not found: {manifest.audio_path(it)}")

    # Speaker/session leakage across splits (S7, S8).
    for attr in ("speaker", "session"):
        splits_by_key: dict[tuple[str, str], set[str]] = defaultdict(set)
        for it in manifest.items:
            key = getattr(it, attr)
            if key:
                splits_by_key[(it.language, key)].add(it.split)
        for (lang, key), splits in sorted(splits_by_key.items()):
            if len(splits) > 1:
                problems.append(f"{attr} leakage: {lang}/{key} appears in splits {sorted(splits)}")
    return problems


def summary(manifest: Manifest) -> dict:
    out: dict = defaultdict(lambda: defaultdict(lambda: {"items": 0, "seconds": 0.0, "empty_refs": 0}))
    for it in manifest.items:
        s = out[it.language][it.split]
        s["items"] += 1
        s["seconds"] += it.duration or 0.0
        s["empty_refs"] += int(not it.reference.strip())
    return {lang: dict(v) for lang, v in out.items()}
