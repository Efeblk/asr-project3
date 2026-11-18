"""Common Voice importer: official split kept, client_id as speaker, durations from clip_durations.tsv."""

import numpy as np
import soundfile as sf

from asrbench.dataset import load_manifest, validate
from asrbench.importers import import_cv

HEAD = "client_id\tpath\tsentence_id\tsentence\tsentence_domain\tup_votes\tdown_votes\tage\tgender\taccents\tvariant\tlocale\tsegment\n"


def _cv(tmp_path, rows):
    d = tmp_path / "cv-corpus-27.0" / "ka"
    (d / "clips").mkdir(parents=True)
    for split in ("train", "dev", "test"):
        lines = [f"{spk}\t{clip}\t{sid}\t{text}\t\t2\t0\t\t\t\t\tka\t\n" for s, spk, clip, sid, text in rows if s == split]
        (d / f"{split}.tsv").write_text(HEAD + "".join(lines), encoding="utf-8")
    with open(d / "clip_durations.tsv", "w", encoding="utf-8") as f:
        f.write("clip\tduration[ms]\n")
        for _, _, clip, _, _ in rows:
            sf.write(d / "clips" / clip.replace(".mp3", ".wav"), np.zeros(1600, dtype="float32"), 16000)
            f.write(f"{clip}\t1500\n")
    return d


def test_import_cv_keeps_split_and_speakers(tmp_path):
    rows = [("train", "a" * 40, "c1.mp3", "s1", "გამარჯობა"), ("train", "a" * 40, "c2.mp3", "s2", "მადლობა"),
            ("dev", "b" * 40, "c3.mp3", "s3", "კარგი"), ("test", "c" * 40, "c4.mp3", "s4", "ნახვამდის")]
    m = load_manifest(import_cv(_cv(tmp_path, rows), "ka", tmp_path / "m.jsonl"))
    assert [i.split for i in m.items] == ["train", "train", "dev", "test"]
    assert m.items[0].speaker == "a" * 16 and m.items[0].duration == 1.5
    assert m.items[3].id == "cv-ka-test-c4" and m.items[3].extra["sentence_id"] == "s4"
    assert not [p for p in validate(m, check_audio=False) if "leakage" in p]


def test_import_cv_leak_is_detected(tmp_path):
    rows = [("train", "a" * 40, "c1.mp3", "s1", "ერთი"), ("test", "a" * 40, "c2.mp3", "s2", "ორი")]
    m = load_manifest(import_cv(_cv(tmp_path, rows), "ka", tmp_path / "m.jsonl"))
    assert any("speaker leakage" in p for p in validate(m, check_audio=False))
