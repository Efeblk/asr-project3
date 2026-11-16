"""Metric checks against the worked examples in the Week 9 study deck."""

import pytest

from asrbench.bootstrap import corpus_rate_ci, paired_delta_ci
from asrbench.metrics import corpus_metrics, score_item, silence_report
from asrbench.normalize import Policy

P = Policy()


def test_s20_s21_jiwer_example():
    s = score_item("x", "the cat sat on the mat", "the cat sit on the", P)
    assert (s.words.sub, s.words.dele, s.words.ins) == (1, 1, 0)
    m = corpus_metrics([s])
    assert round(m["wer"], 4) == 0.3333
    assert round(m["cer"], 4) == 0.2273


def test_s13_s26_wer_can_exceed_100_percent():
    m = corpus_metrics([score_item("x", "go", "please go now today", P)])
    assert m["wer"] == 3.0
    assert m["mer"] == pytest.approx(0.75)
    assert m["wil"] == pytest.approx(0.75)


def test_s18_corpus_vs_mean_clip_wer():
    a = score_item("a", "w1 w2", "w1 x", P)                        # 1 error / 2 words
    b = score_item("b", "w1 w2 w3 w4 w5 w6 w7 w8", "w1 w2 w3 w4 w5 w6 w7 x", P)  # 1 / 8
    m = corpus_metrics([a, b])
    assert m["wer"] == pytest.approx(0.2)
    assert m["mean_clip_wer"] == pytest.approx(0.3125)


def test_s23_accent_difference_is_an_error_by_default():
    assert score_item("x", "Málaga", "Malaga", P).words.sub == 1
    assert score_item("x", "Málaga", "Malaga", Policy(strip_diacritics=True)).words.errors == 0


def test_unicode_nfc_makes_composed_and_decomposed_equal():
    assert score_item("x", "café", "café", P).words.errors == 0


def test_case_and_punctuation_policy():
    assert score_item("x", "Je pars, à huit heures.", "je pars à huit heures", P).words.errors == 0
    strict = Policy(lowercase=False, remove_punctuation=False)
    assert score_item("x", "Je pars.", "je pars", strict).words.errors == 2


def test_empty_hypothesis_is_all_deletions():
    s = score_item("x", "a b c", "", P)
    assert (s.words.dele, s.words.n_ref) == (3, 3)


def test_s76_silence_is_reported_separately():
    speech = score_item("a", "one two", "one two", P)
    silent = score_item("b", "", "thank you", P)
    m = corpus_metrics([speech, silent])
    assert m["items"] == 1 and m["wer"] == 0.0
    rep = silence_report([speech, silent])
    assert rep == {"silent_items": 1, "items_with_output": 1, "emitted_words": 2,
                   "examples": [{"id": "b", "hyp": "thank you"}]}


def test_no_word_unit_reports_cer_only():
    m = corpus_metrics([score_item("x", "東京に行く", "東京へ行く", Policy(word_unit="none"))])
    assert "wer" not in m and m["cer"] == pytest.approx(1 / 5)


def test_grapheme_cer_counts_displayed_characters():
    # 'नमस्ते' = 6 code points but 3 grapheme clusters (न, म, स्ते).
    cp = score_item("x", "नमस्ते", "", Policy(cer_unit="codepoint")).chars.n_ref
    gr = score_item("x", "नमस्ते", "", Policy(cer_unit="grapheme")).chars.n_ref
    assert cp == 6 and gr == 3


def test_bootstrap_ci_contains_point_estimate():
    keys = [f"s{i % 5}" for i in range(50)]
    errors = [i % 3 for i in range(50)]
    n = [10] * 50
    ci = corpus_rate_ci(keys, errors, n, n_boot=500)
    point = sum(errors) / sum(n)
    assert ci["low"] <= point <= ci["high"] and ci["clusters"] == 5


def test_paired_delta_identical_systems_is_zero():
    keys = ["a", "b", "c", "d"]
    d = paired_delta_ci(keys, [1, 2, 0, 3], [1, 2, 0, 3], [5, 5, 5, 5], n_boot=200)
    assert d["delta"] == 0 and d["low"] == 0 and d["high"] == 0
