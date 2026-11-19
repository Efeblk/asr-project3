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
