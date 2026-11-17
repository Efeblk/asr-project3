"""`asrbench train`: fine-tune a pretrained checkpoint on our train split. This is the project's
*contribution* (announcement A1): pretrained models run as-is are baselines; our training is not.

Families
  hf-whisper  full fine-tune of a multilingual Whisper checkpoint (Seq2SeqTrainer; HF audio course ch.5 recipe).
              Targets are the raw orthographic references ("train orthographic, evaluate normalized").
  hf-ctc      CTC fine-tune of a wav2vec2 / XLS-R / MMS encoder. By default a new character vocabulary is
              built from the train references after the declared scoring normalization (CTC outputs no case or
              punctuation); `reuse_vocab: true` keeps the head and vocabulary of an existing CTC checkpoint.

Protocol (S7, S8, S60, S71)
  - fits weights on `train` only; selects the checkpoint by dev WER (or CER for word_unit: none);
  - never reads `test`. Evaluate the saved model afterwards with `asrbench run` like any baseline, on the
    same frozen test set and scoring policy, and report it in a separate "ours" row (A1);
  - refuses English, unconfirmed eligibility, and manifests with speaker/session leakage.

Outputs
  checkpoints/<name>_<ts>/final/   best-dev model + processor + train_manifest.json   (gitignored: weights)
  runs/train_<name>_<ts>/          train_manifest.json, log_history.json, train_ids.txt  (commit these)
"""

from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

from . import envinfo
from .audio import load_audio
from .dataset import Item, load_manifest, validate
from .eligibility import check_run_languages
from .metrics import corpus_metrics, score_item
from .normalize import Policy, load_policies

SR = 16000

# Defaults merged under the config's `training:` block, then passed to (Seq2Seq)TrainingArguments.
_COMMON_DEFAULTS = dict(eval_strategy="steps", save_strategy="steps", logging_steps=25, save_total_limit=2,
                        load_best_model_at_end=True, greater_is_better=False, report_to=[],
                        remove_unused_columns=False, label_names=["labels"], dataloader_num_workers=0,
                        gradient_checkpointing=True, gradient_checkpointing_kwargs={"use_reentrant": False})
_FAMILY_DEFAULTS = {
    "hf-whisper": dict(learning_rate=1e-5, warmup_steps=500, max_steps=4000, per_device_train_batch_size=16,
                       per_device_eval_batch_size=16, eval_steps=500, save_steps=500, bf16=True,
                       predict_with_generate=True, generation_max_length=225),
    "hf-ctc": dict(learning_rate=3e-4, warmup_steps=500, max_steps=6000, per_device_train_batch_size=4,
                   gradient_accumulation_steps=4,  # batch 8 peaked at 10.9 GB on a 12 GB GPU (XLS-R-300M) per_device_eval_batch_size=8, eval_steps=500, save_steps=500,
                   bf16=True, weight_decay=0.005),
}


class AudioTextDataset:
    """Loads audio lazily; module-level so DataLoader workers can pickle it on Windows."""

    def __init__(self, paths: list[str], texts: list[str]):
        self.paths, self.texts = paths, texts

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, i: int) -> dict:
        return {"audio": load_audio(self.paths[i], SR), "text": self.texts[i]}


class WhisperCollator:
    def __init__(self, processor, decoder_start_token_id: int):
        self.processor, self.start = processor, decoder_start_token_id

    def __call__(self, feats: list[dict]) -> dict:
        x = self.processor.feature_extractor([f["audio"] for f in feats], sampling_rate=SR, return_tensors="pt")
        lab = self.processor.tokenizer([f["text"] for f in feats], padding=True, return_tensors="pt")
        labels = lab.input_ids.masked_fill(lab.attention_mask.ne(1), -100)
        if (labels[:, 0] == self.start).all():  # the model prepends <|startoftranscript|> itself
            labels = labels[:, 1:]
        return {"input_features": x.input_features, "labels": labels}


class CTCCollator:
    def __init__(self, processor):
        self.processor = processor

    def __call__(self, feats: list[dict]) -> dict:
        fe = self.processor.feature_extractor
        x = fe([f["audio"] for f in feats], sampling_rate=SR, padding=True, return_tensors="pt",
               return_attention_mask=bool(fe.return_attention_mask))
        lab = self.processor.tokenizer([f["text"] for f in feats], padding=True, return_tensors="pt")
        out = {"input_values": x.input_values,
               "labels": lab.input_ids.masked_fill(lab.attention_mask.ne(1), -100)}
        if fe.return_attention_mask:
            out["attention_mask"] = x.attention_mask
        return out


def _duration(item: Item, path: Path) -> float | None:
    if item.duration:
        return float(item.duration)
    try:
        import soundfile as sf
        return float(sf.info(str(path)).duration)
    except Exception:
        return None


def subsample_hours(items: list[Item], durations: dict[str, float], hours: float | None, seed: int) -> list[Item]:
    """Deterministic random subset with at least `hours` of audio (learning-curve experiments)."""
    if not hours:
        return items
    order = sorted(items, key=lambda i: i.id)
    random.Random(seed).shuffle(order)
    out, total = [], 0.0
    for it in order:
        if total >= hours * 3600:
            break
        out.append(it)
        total += durations.get(it.id) or 0.0
    return out


def build_ctc_vocab(texts: list[str]) -> dict[str, int]:
    chars = sorted({c for t in texts for c in t} - {" "})
    vocab = {"[PAD]": 0, "[UNK]": 1, "|": 2}
    for c in chars:
        vocab.setdefault(c, len(vocab))
    return vocab


def _dev_error(refs: list[str], hyps: list[str], policy: Policy) -> dict:
    m = corpus_metrics([score_item(str(k), r, h, policy) for k, (r, h) in enumerate(zip(refs, hyps))])
    return {k: m[k] for k in ("wer", "cer") if m.get(k) is not None}


def _load_config(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def train(config_path: str | Path, checkpoints_dir: str | Path = "checkpoints", runs_dir: str | Path = "runs",
          policy_path: str | None = "configs/scoring.yaml", log=print) -> Path:
    cfg = _load_config(config_path)
    lang = cfg["language"]
    check_run_languages([lang], bool(cfg.get("eligibility_confirmed")))
    spec = dict(cfg["model"])
    family = spec["family"]
    if family not in _FAMILY_DEFAULTS:
        raise ValueError(f"`asrbench train` supports {sorted(_FAMILY_DEFAULTS)}, not '{family}'.")
    if family == "hf-whisper" and spec["id"].endswith(".en"):
        raise ValueError(f"{spec['id']} is English-only; fine-tune a multilingual checkpoint (S69).")
    if "test" in (cfg.get("train_split", "train"), cfg.get("dev_split", "dev")):
        raise ValueError("Training and checkpoint selection must never use the test split (S7, S60).")

    seed = int(cfg.get("seed", 42))
    policies = load_policies(policy_path if policy_path and Path(policy_path).exists() else None)
    policy = policies.for_language(lang)
    metric = "wer" if policy.word_unit != "none" else "cer"

    dataset = load_manifest(cfg["dataset"])
    problems = validate(dataset, check_audio=False)
    if problems:
        raise ValueError("Dataset manifest problems:\n  " + "\n  ".join(problems[:20]))
    train_items = dataset.select(cfg.get("train_split", "train"), [lang])
    dev_items = dataset.select(cfg.get("dev_split", "dev"), [lang])
    if not train_items or not dev_items:
        raise ValueError(f"Need train and dev items for '{lang}' in {cfg['dataset']} "
                         f"(found {len(train_items)} train, {len(dev_items)} dev).")

    for key, want in (cfg.get("train_filter") or {}).items():  # e.g. {in_train_sample: true} or {subcorpus: parliament}
        want = want if isinstance(want, list) else [want]
        train_items = [i for i in train_items if (getattr(i, key, None) if key in Item.__dataclass_fields__
                                                  else i.extra.get(key)) in want]
    max_sec = float(cfg.get("max_audio_sec", 30))
    durations = {i.id: _duration(i, dataset.audio_path(i)) for i in train_items + dev_items}
    too_long = [i.id for i in train_items if (durations[i.id] or 0) > max_sec]
    train_items = [i for i in train_items if (durations[i.id] or 0) <= max_sec]
    train_items = subsample_hours(train_items, durations, cfg.get("train_hours"), seed)
    if family == "hf-ctc":  # an empty CTC target teaches nothing useful; Whisper keeps them (anti-hallucination)
        train_items = [i for i in train_items if i.reference.strip()]
    for key, want in (cfg.get("dev_filter") or {}).items():
        want = want if isinstance(want, list) else [want]
        dev_items = [i for i in dev_items if (getattr(i, key, None) if key in Item.__dataclass_fields__
                                              else i.extra.get(key)) in want]
    dev_items = sorted((i for i in dev_items if i.reference.strip()), key=lambda i: i.id)
    if cfg.get("dev_limit"):
        dev_items = random.Random(seed).sample(dev_items, min(int(cfg["dev_limit"]), len(dev_items)))
    train_hours = sum(durations[i.id] or 0 for i in train_items) / 3600
    log(f"Train: {len(train_items)} items, {train_hours:.2f} h ({len(too_long)} > {max_sec:.0f}s dropped). "
        f"Dev for selection: {len(dev_items)} items.")

    import torch
    from transformers import set_seed
    set_seed(seed)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = cfg.get("name", "train")
    ckpt_dir = Path(checkpoints_dir) / f"{name}_{stamp}"
    run_dir = Path(runs_dir) / f"train_{name}_{stamp}"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "config.yaml").write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8", newline="\n")
    (run_dir / "train_ids.txt").write_text("\n".join(sorted(i.id for i in train_items)) + "\n", encoding="utf-8", newline="\n")

    args_kw = {**_COMMON_DEFAULTS, **_FAMILY_DEFAULTS[family], **(cfg.get("training") or {})}
    args_kw.update(output_dir=str(ckpt_dir), seed=seed, metric_for_best_model=metric)
    if args_kw.get("use_cpu") or not torch.cuda.is_available():
        args_kw.update(bf16=False, fp16=False)

    paths = lambda items: [str(dataset.audio_path(i)) for i in items]  # noqa: E731
    dev_refs = [i.reference for i in dev_items]
    vocab_info = None

    if family == "hf-whisper":
        from transformers import (Seq2SeqTrainer, Seq2SeqTrainingArguments, WhisperForConditionalGeneration,
                                  WhisperProcessor)
        hint = spec.get("language_hint") or (spec.get("language_hints") or {}).get(lang, lang)
        processor = WhisperProcessor.from_pretrained(spec["id"], revision=spec.get("revision", "main"))
        processor.tokenizer.set_prefix_tokens(language=hint, task="transcribe")
        model = WhisperForConditionalGeneration.from_pretrained(spec["id"], revision=spec.get("revision", "main"))
        model.config.forced_decoder_ids = None
        model.generation_config.forced_decoder_ids = None
        model.generation_config.language = hint
        model.generation_config.task = "transcribe"
        if args_kw.get("gradient_checkpointing"):
            model.config.use_cache = False
        too_many_tokens = [i.id for i in train_items if len(processor.tokenizer(i.reference).input_ids) > 448]
        train_items = [i for i in train_items if i.id not in set(too_many_tokens)]
        train_hours = sum(durations[i.id] or 0 for i in train_items) / 3600
        train_ds = AudioTextDataset(paths(train_items), [i.reference for i in train_items])
        dev_ds = AudioTextDataset(paths(dev_items), dev_refs)
        collator = WhisperCollator(processor, model.config.decoder_start_token_id)

        def compute_metrics(pred):
            ids = np.where(pred.predictions != -100, pred.predictions, processor.tokenizer.pad_token_id)
            hyps = processor.batch_decode(ids, skip_special_tokens=True)
            return _dev_error(dev_refs, [h.strip() for h in hyps], policy)

        trainer = Seq2SeqTrainer(model=model, args=Seq2SeqTrainingArguments(**args_kw), train_dataset=train_ds,
                                 eval_dataset=dev_ds, data_collator=collator, compute_metrics=compute_metrics)
    else:
        from transformers import (AutoModelForCTC, AutoProcessor, Trainer, TrainingArguments, Wav2Vec2CTCTokenizer,
                                  Wav2Vec2FeatureExtractor, Wav2Vec2Processor)
        args_kw.pop("predict_with_generate", None)
        args_kw.pop("generation_max_length", None)
        to_target = (lambda t: t) if spec.get("raw_targets") else policy.normalize
        train_texts = [to_target(i.reference) for i in train_items]
        if spec.get("reuse_vocab"):
            processor = AutoProcessor.from_pretrained(spec["id"], revision=spec.get("revision", "main"))
            vocab_info = {"source": "checkpoint", "size": len(processor.tokenizer)}
        else:
            vocab = build_ctc_vocab(train_texts)
            vocab_path = ckpt_dir / "vocab.json"
            vocab_path.write_text(json.dumps(vocab, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
            tok = Wav2Vec2CTCTokenizer(str(vocab_path), unk_token="[UNK]", pad_token="[PAD]",
                                       word_delimiter_token="|")
            fe = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=SR, padding_value=0.0, do_normalize=True,
                                          return_attention_mask=True)
            processor = Wav2Vec2Processor(feature_extractor=fe, tokenizer=tok)
            vocab_info = {"source": "built from train targets", "size": len(vocab), "chars": "".join(vocab)}
        model_kw = dict(ctc_loss_reduction="mean", pad_token_id=processor.tokenizer.pad_token_id)
        if not spec.get("reuse_vocab"):
            model_kw.update(vocab_size=len(processor.tokenizer), ignore_mismatched_sizes=True)
        model_kw.update(spec.get("model_kwargs") or {})  # e.g. mask_time_prob, layerdrop, *_dropout
        model = AutoModelForCTC.from_pretrained(spec["id"], revision=spec.get("revision", "main"), **model_kw)
        if spec.get("freeze_feature_encoder", True) and hasattr(model, "freeze_feature_encoder"):
            model.freeze_feature_encoder()
        train_ds = AudioTextDataset(paths(train_items), train_texts)
        dev_ds = AudioTextDataset(paths(dev_items), [to_target(r) for r in dev_refs])
        collator = CTCCollator(processor)

        def compute_metrics(pred):
            ids = np.where(pred.predictions != -100, pred.predictions, processor.tokenizer.pad_token_id)
            hyps = processor.batch_decode(ids)
            return _dev_error(dev_refs, [h.strip() for h in hyps], policy)

        trainer = Trainer(model=model, args=TrainingArguments(**args_kw), train_dataset=train_ds,
                          eval_dataset=dev_ds, data_collator=collator, compute_metrics=compute_metrics,
                          preprocess_logits_for_metrics=lambda logits, labels: logits.argmax(-1))

    base_revision = None
    try:
        from huggingface_hub import model_info
        base_revision = model_info(spec["id"], revision=spec.get("revision", "main")).sha
    except Exception:
        pass

    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
    t0 = time.perf_counter()
    trainer.train()
    train_sec = time.perf_counter() - t0
    final = ckpt_dir / "final"
    trainer.save_model(str(final))
    processor.save_pretrained(str(final))
    best_eval = trainer.evaluate()

    manifest = {
        "name": name,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kind": "training (our contribution, A1)",
        "language": lang,
        "base_model": {"family": family, "model_id": spec["id"], "revision_requested": spec.get("revision", "main"),
                       "revision_resolved": base_revision},
        "language_hint": spec.get("language_hint") if family == "hf-whisper" else None,
        "targets": ("raw orthographic references" if family == "hf-whisper" or spec.get("raw_targets")
                    else "references normalized with the scoring policy"),
        "vocab": vocab_info,
        "dataset": {"path": str(cfg["dataset"]), "sha256": dataset.sha256(),
                    "train_split": cfg.get("train_split", "train"), "dev_split": cfg.get("dev_split", "dev"),
                    "train_items": len(train_items), "train_hours": round(train_hours, 3),
                    "train_hours_requested": cfg.get("train_hours"), "dropped_too_long": len(too_long),
                    "dev_items_for_selection": len(dev_items), "dev_limit": cfg.get("dev_limit"),
                    "train_filter": cfg.get("train_filter"), "dev_filter": cfg.get("dev_filter")},
        "selection": {"metric": f"dev {metric} under the scoring policy", "best_checkpoint": trainer.state.best_model_checkpoint,
                      "best_metric": trainer.state.best_metric, "final_eval": best_eval},
        "training_args": {k: v for k, v in args_kw.items() if k != "output_dir"},
        "seed": seed,
        "train_sec": round(train_sec, 1),
        "global_steps": trainer.state.global_step,
        "peak_gpu_memory_gb": round(torch.cuda.max_memory_allocated() / 2**30, 2) if torch.cuda.is_available() else None,
        "scoring_policy": policy.to_dict(),
        "checkpoint_dir": final.as_posix(),
        "run_dir": run_dir.as_posix(),
        "env": envinfo.capture(),
    }
    text = json.dumps(manifest, indent=2, ensure_ascii=False, default=str)
    (final / "train_manifest.json").write_text(text, encoding="utf-8", newline="\n")
    (run_dir / "train_manifest.json").write_text(text, encoding="utf-8", newline="\n")
    (run_dir / "log_history.json").write_text(json.dumps(trainer.state.log_history, indent=1), encoding="utf-8", newline="\n")
    log(f"Best dev {metric}: {trainer.state.best_metric}. Model: {final.as_posix()}  Log: {run_dir.as_posix()}")
    return final
