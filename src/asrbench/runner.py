"""`asrbench run`: produce raw predictions + a run manifest (S8, S11, S77).

Output directory runs/<name>_<UTC timestamp>/:
  config.yaml        exact config used
  manifest.json      data hash, model + resolved revision, settings, env, timing summary
  predictions.jsonl  one line per item: id, language, reference, hypothesis (RAW, never normalized),
                     audio_sec, compute_sec, plus speaker/session for bootstrap clustering
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

from . import envinfo
from .audio import load_audio
from .dataset import load_manifest, validate
from .eligibility import check_run_languages
from .models import build_recognizer


def load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def run(config_path: str | Path, runs_dir: str | Path = "runs", resume: str | Path | None = None,
        log=print) -> Path:
    cfg = load_config(config_path)
    split = cfg["split"]
    languages = list(cfg["languages"])
    check_run_languages(languages, bool(cfg.get("eligibility_confirmed")))

    if split == "test" and not cfg.get("frozen"):
        raise ValueError("Test-split runs need `frozen: true`: pick checkpoint, decoding and normalization on "
                         "dev first, then evaluate test once (S7, S60).")
    if split == "test" and cfg.get("limit"):
        raise ValueError("`limit` is for dev smoke tests; evaluate the whole test split (S11).")

    dataset = load_manifest(cfg["dataset"])
    problems = validate(dataset, check_audio=False)
    if problems:
        raise ValueError("Dataset manifest problems:\n  " + "\n  ".join(problems[:20]))
    items = dataset.select(split, languages)
    missing = set(languages) - {i.language for i in items}
    if missing:
        raise ValueError(f"No {split} items for languages {sorted(missing)} in {cfg['dataset']}")
    if cfg.get("limit"):
        n = int(cfg["limit"])
        items = [i for lang in languages for i in sorted((x for x in items if x.language == lang), key=lambda x: x.id)[:n]]

    if resume:
        out = Path(resume)
    else:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out = Path(runs_dir) / f"{cfg.get('name', 'run')}_{stamp}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")

    pred_path = out / "predictions.jsonl"
    done = set()
    if pred_path.exists():
        done = {json.loads(l)["id"] for l in pred_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    todo = [i for i in items if i.id not in done]

    model_spec = dict(cfg["model"])
    recognizer = build_recognizer(model_spec)
    t0 = time.perf_counter()
    recognizer.load()
    load_sec = time.perf_counter() - t0
    log(f"Loaded {recognizer.model_id} in {load_sec:.1f}s; {len(todo)} items to transcribe ({len(done)} done).")

    bs = int(cfg.get("batch_size", 8))
    manifest = {
        "name": cfg.get("name"),
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task": "transcribe (same-language ASR)",
        "split": split,
        "languages": languages,
        "dataset": {"path": str(cfg["dataset"]), "sha256": dataset.sha256(), "items": len(items),
                    "limit": cfg.get("limit")},
        "model": recognizer.describe(),
        "batch_size": bs,
        "timing_boundary": "model forward/decode only; audio loading and model loading excluded; "
                           "CUDA synchronized before and after each batch; first batch preceded by a warm-up pass",
        "chunking": "none for clips <=30 s; family default long-form decoding above that",
        "env": envinfo.capture(),
        "model_load_sec": round(load_sec, 2),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    warmed = False
    with pred_path.open("a", encoding="utf-8", newline="\n") as f:
        for lang in languages:
            lang_items = sorted((i for i in todo if i.language == lang), key=lambda i: -(i.duration or 0))
            for b in range(0, len(lang_items), bs):
                batch = lang_items[b:b + bs]
                audios = [load_audio(dataset.audio_path(i), recognizer.sample_rate) for i in batch]
                if not warmed:
                    recognizer.transcribe(audios[:1], lang)
                    warmed = True
                recognizer.sync()
                t = time.perf_counter()
                hyps = recognizer.transcribe(audios, lang)
                recognizer.sync()
                elapsed = time.perf_counter() - t
                secs = [len(a) / recognizer.sample_rate for a in audios]
                total = sum(secs) or 1.0
                for it, hyp, s in zip(batch, hyps, secs):
                    row = {"id": it.id, "language": it.language, "reference": it.reference, "hypothesis": hyp,
                           "audio_sec": round(s, 3), "compute_sec": round(elapsed * s / total, 4),
                           "speaker": it.speaker, "session": it.session}
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                f.flush()
                log(f"[{lang}] {min(b + bs, len(lang_items))}/{len(lang_items)}  batch {elapsed:.2f}s")

    preds = [json.loads(l) for l in pred_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    audio_sec = sum(p["audio_sec"] for p in preds)
    compute_sec = sum(p["compute_sec"] for p in preds)
    manifest["completed_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    manifest["totals"] = {"items": len(preds), "audio_sec": round(audio_sec, 2), "compute_sec": round(compute_sec, 2),
                          "rtf": round(compute_sec / audio_sec, 4) if audio_sec else None}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"Wrote {pred_path}")
    return out
