"""Eligibility, manifest validation, and an end-to-end run/score/compare with a dummy recognizer."""

import json

import numpy as np
import pytest
import soundfile as sf
import yaml

from asrbench.dataset import Item, load_manifest, validate, write_manifest
from asrbench.eligibility import IneligibleLanguageError, check_language, check_run_languages
from asrbench.runner import run
from asrbench.scoring import compare, score


@pytest.mark.parametrize("code", ["en", "EN", "en-US", "en_gb", "eng"])
def test_english_is_rejected(code):
    with pytest.raises(IneligibleLanguageError):
        check_language(code)


def test_eligibility_must_be_confirmed():
    check_language("sw")
    with pytest.raises(IneligibleLanguageError):
        check_run_languages(["sw"], eligibility_confirmed=False)
    check_run_languages(["sw"], eligibility_confirmed=True)


def test_speaker_leakage_is_detected(tmp_path):
    items = [Item("a", "a.wav", "x", "sw", "train", speaker="spk1"),
             Item("b", "b.wav", "y", "sw", "test", speaker="spk1")]
    m = load_manifest(write_manifest(items, tmp_path / "m.jsonl"))
    problems = validate(m, check_audio=False)
    assert any("speaker leakage" in p for p in problems)


@pytest.fixture
def toy_dataset(tmp_path):
    sr = 16000
    items = []
    refs = ["habari ya asubuhi", "habari ya jioni", "asante sana", ""]
    for i, ref in enumerate(refs):
        wav = tmp_path / f"clip{i}.wav"
        sf.write(wav, (0.01 * np.random.default_rng(i).standard_normal(sr)).astype("float32"), sr)
        items.append(Item(f"id{i}", wav.name, ref, "sw", "dev", session=f"s{i % 2}", duration=1.0))
    return write_manifest(items, tmp_path / "manifest.jsonl")


def _config(tmp_path, manifest, text, **over):
    cfg = {"name": f"const-{text or 'empty'}", "dataset": str(manifest), "split": "dev", "languages": ["sw"],
           "eligibility_confirmed": True, "batch_size": 2,
           "model": {"family": "debug-constant", "id": "debug", "device": "cpu", "text": text}}
    cfg.update(over)
    path = tmp_path / f"{cfg['name']}.yaml"
    path.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    return path


def test_end_to_end_run_score_compare(tmp_path, toy_dataset):
    runs = tmp_path / "runs"
    a = run(_config(tmp_path, toy_dataset, "habari ya asubuhi"), runs, log=lambda *_: None)
    b = run(_config(tmp_path, toy_dataset, ""), runs, log=lambda *_: None)

    preds = [json.loads(l) for l in (a / "predictions.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(preds) == 4 and all(p["hypothesis"] == "habari ya asubuhi" for p in preds)
    manifest = json.loads((a / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["dataset"]["sha256"] and manifest["model"]["family"] == "debug-constant"

    res = score(a)
    sw = res["languages"]["sw"]
    # refs (8 words): exact match (0 errors) + "jioni"->"asubuhi" (1) + 2 subs and 1 insertion (3) = 4
    assert sw["items"] == 3 and sw["word_counts"]["N"] == 8 and sw["wer"] == pytest.approx(4 / 8)
    assert sw["silence"]["items_with_output"] == 1 and sw["silence"]["emitted_words"] == 3
    assert (a / "report.md").exists()

    primary = (a / "scores.json").read_text(encoding="utf-8")
    alt = tmp_path / "alt.yaml"
    alt.write_text(yaml.safe_dump({"languages": {"sw": {"drop_tokens": "ya"}}}), encoding="utf-8")
    res_alt = score(a, str(alt), tag="alt")  # secondary policy: written beside, never over, the primary scores
    assert (a / "scores.alt.json").exists() and (a / "report.alt.md").exists()
    assert (a / "scores.json").read_text(encoding="utf-8") == primary
    assert res_alt["languages"]["sw"]["word_counts"]["N"] == 6

    assert score(b)["languages"]["sw"]["wer"] == 1.0
    table = compare(a, b)
    assert "| sw | 3 |" in table


def test_test_split_requires_frozen(tmp_path, toy_dataset):
    with pytest.raises(ValueError, match="frozen"):
        run(_config(tmp_path, toy_dataset, "x", split="test"), tmp_path / "runs", log=lambda *_: None)


def test_english_only_whisper_is_refused():
    from asrbench.models import build_recognizer
    with pytest.raises(ValueError, match="English-only"):
        build_recognizer({"family": "hf-whisper", "id": "openai/whisper-small.en"}).load()
