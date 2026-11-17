"""`asrbench train` end to end on CPU with a tiny randomly initialised CTC model (no downloads)."""

import json

import numpy as np
import pytest
import soundfile as sf
import yaml

from asrbench.dataset import Item, write_manifest
from asrbench.eligibility import IneligibleLanguageError
from asrbench.train import build_ctc_vocab, subsample_hours, train

transformers = pytest.importorskip("transformers")


@pytest.fixture
def tiny_ctc(tmp_path):
    from transformers import Wav2Vec2Config, Wav2Vec2ForCTC
    cfg = Wav2Vec2Config(hidden_size=32, num_hidden_layers=2, num_attention_heads=2, intermediate_size=64,
                         conv_dim=(32, 32), conv_stride=(5, 4), conv_kernel=(10, 8), num_feat_extract_layers=2,
                         num_conv_pos_embeddings=16, num_conv_pos_embedding_groups=2, vocab_size=8,
                         do_stable_layer_norm=True, feat_extract_norm="layer")
    path = tmp_path / "tiny-ctc"
    Wav2Vec2ForCTC(cfg).save_pretrained(path)
    return path


@pytest.fixture
def toy_corpus(tmp_path):
    rng = np.random.default_rng(0)
    items, texts = [], ["Habari ya asubuhi.", "Asante sana!", "Karibu tena", "Habari za jioni"]
    for split, n in (("train", 8), ("dev", 4), ("test", 2)):
        for k in range(n):
            wav = tmp_path / f"{split}{k}.wav"
            sf.write(wav, (0.05 * rng.standard_normal(16000)).astype("float32"), 16000)
            items.append(Item(f"{split}{k}", wav.name, texts[k % 4], "sw", split, speaker=f"{split}-spk{k % 2}",
                              duration=1.0))
    return write_manifest(items, tmp_path / "manifest.jsonl")


def _cfg(tmp_path, manifest, model_path, **over):
    cfg = {"name": "tiny", "dataset": str(manifest), "language": "sw", "eligibility_confirmed": True,
           "model": {"family": "hf-ctc", "id": str(model_path)},
           "training": {"use_cpu": True, "max_steps": 2, "eval_steps": 1, "save_steps": 1, "warmup_steps": 0,
                        "per_device_train_batch_size": 4, "gradient_accumulation_steps": 1,
                        "gradient_checkpointing": False, "logging_steps": 1}}
    cfg.update(over)
    p = tmp_path / "train.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return p


def test_ctc_training_end_to_end(tmp_path, toy_corpus, tiny_ctc):
    final = train(_cfg(tmp_path, toy_corpus, tiny_ctc), tmp_path / "ckpt", tmp_path / "runs", None,
                  log=lambda *_: None)
    m = json.loads((final / "train_manifest.json").read_text(encoding="utf-8"))
    assert m["dataset"]["train_items"] == 8 and m["dataset"]["dev_items_for_selection"] == 4
    assert m["global_steps"] == 2 and m["selection"]["best_metric"] is not None
    ids = (tmp_path / "runs" / f"train_tiny_{final.parent.name.split('_', 1)[1]}" / "train_ids.txt").read_text()
    assert "test" not in ids  # never trains on test

    from asrbench.models import build_recognizer
    rec = build_recognizer({"family": "hf-ctc", "id": str(final), "device": "cpu", "dtype": "float32"})
    rec.load()
    assert len(rec.transcribe([np.zeros(16000, dtype="float32")], "sw")) == 1
    assert rec.local_training()["trained_by_us"] is True


def test_training_resumes_from_checkpoint(tmp_path, toy_corpus, tiny_ctc):
    first = train(_cfg(tmp_path, toy_corpus, tiny_ctc), tmp_path / "ckpt", tmp_path / "runs", None,
                  log=lambda *_: None)
    over = _cfg(tmp_path, toy_corpus, tiny_ctc)  # same run, longer budget: continues at step 2, not from scratch
    cfg = yaml.safe_load(over.read_text(encoding="utf-8"))
    cfg["training"]["max_steps"] = 3
    over.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    final = train(over, tmp_path / "ignored", tmp_path / "runs", None, log=lambda *_: None, resume=first.parent)
    assert final == first
    m = json.loads((final / "train_manifest.json").read_text(encoding="utf-8"))
    assert m["global_steps"] == 3 and m["resumed"] is True
    with pytest.raises(ValueError):
        train(over, tmp_path / "c", tmp_path / "runs", None, resume=tmp_path / "runs")


def test_training_refuses_test_split_and_english(tmp_path, toy_corpus, tiny_ctc):
    with pytest.raises(ValueError, match="test split"):
        train(_cfg(tmp_path, toy_corpus, tiny_ctc, dev_split="test"), tmp_path / "c", tmp_path / "r", None)
    with pytest.raises(IneligibleLanguageError):
        train(_cfg(tmp_path, toy_corpus, tiny_ctc, language="en"), tmp_path / "c", tmp_path / "r", None)


def test_vocab_and_subsample():
    v = build_ctc_vocab(["ab c", "ca"])
    assert list(v) == ["[PAD]", "[UNK]", "|", "a", "b", "c"]
    items = [Item(str(i), "x.wav", "a", "sw", "train") for i in range(10)]
    sub = subsample_hours(items, {str(i): 360.0 for i in range(10)}, 0.3, seed=1)
    assert len(sub) == 3 and sub == subsample_hours(items, {str(i): 360.0 for i in range(10)}, 0.3, seed=1)
