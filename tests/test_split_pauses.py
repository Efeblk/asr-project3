import numpy as np

from asrbench.models.hf import split_at_pauses


def test_split_at_pauses_cuts_in_silence_and_keeps_all_samples():
    sr = 16000
    rng = np.random.default_rng(0)
    audio = rng.normal(0, 0.3, 25 * sr).astype(np.float32)
    for gap in (9.0, 18.0):  # 300 ms pauses
        audio[int(gap * sr):int((gap + 0.3) * sr)] = 0.0
    pieces = split_at_pauses(audio, sr, 11.0)
    assert len(pieces) == 3
    assert all(len(p) <= 11 * sr for p in pieces)
    assert np.array_equal(np.concatenate(pieces), audio)
    cuts = np.cumsum([len(p) for p in pieces])[:-1] / sr
    assert 9.0 <= cuts[0] <= 9.3 and 18.0 <= cuts[1] <= 18.3


def test_split_at_pauses_short_clip_untouched():
    a = np.ones(16000 * 5, dtype=np.float32)
    assert len(split_at_pauses(a, 16000, 11.0)) == 1


def test_split_balanced_no_short_tail_and_keeps_all_samples():
    from asrbench.models.hf import split_balanced
    sr = 16000
    rng = np.random.default_rng(1)
    for dur in (30.5, 33.24, 45.0, 61.0, 89.9):
        audio = rng.normal(0, 0.3, int(dur * sr)).astype(np.float32)
        audio[int(dur / 2 * sr):int((dur / 2 + 0.3) * sr)] = 0.0  # one pause near the middle
        pieces = split_balanced(audio, sr, 30.0)
        n = int(np.ceil(dur / 30.0))
        assert len(pieces) == n
        assert np.array_equal(np.concatenate(pieces), audio)
        assert all(len(p) <= 30 * sr for p in pieces)
        assert min(len(p) for p in pieces) >= 0.69 * len(audio) / n  # no tiny shard (search 0.15 -> >= 0.7 L)


def test_split_balanced_cuts_at_pause_and_short_clip_untouched():
    from asrbench.models.hf import split_balanced
    sr = 16000
    audio = np.random.default_rng(2).normal(0, 0.3, int(33.24 * sr)).astype(np.float32)
    audio[int(15.0 * sr):int(15.3 * sr)] = 0.0
    pieces = split_balanced(audio, sr, 30.0)
    assert len(pieces) == 2 and 15.0 <= len(pieces[0]) / sr <= 15.3
    short = np.ones(10 * sr, dtype=np.float32)
    assert len(split_balanced(short, sr, 30.0)) == 1
