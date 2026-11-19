"""Kaldi data + dictionary for the Georgian MFCC + GMM-HMM baseline, from the repo manifests.

Run from the repo root with the repo env (so transcripts use exactly the declared scoring normalizer), then copy
the output directory into WSL as ~/ka_gmm/prep (see README.md here):
    uv run python recipes/kaldi-gmm-ka/prepare_data.py --out <local dir> --wsl-data-root /home/<user>/asrdata

Writes, under --out:
  data/<corpus>_<split>/{wav.scp,text,utt2spk,spk2utt,utt2dur}  (Kaldi data dirs; audio decoded by ffmpeg pipes)
  data/<corpus>_<split>/uttmap      Kaldi utterance id -> asrbench item id
  local/dict/{lexicon,nonsilence_phones,silence_phones,optional_silence,extra_questions}.txt
  local/lm_train.txt                LM text = normalized CV ka TRAIN transcripts only (never dev/test)
  stats.json                        vocabulary, OOV rates on dev/test (word types and tokens)

Choices (fixed before any decoding):
  * Graphemic lexicon: Georgian (Mkhedruli) spelling is close to one letter per phoneme, so each word is
    "pronounced" as its letters. Vocabulary = all words of the train transcripts (closed vocabulary).
  * Text = `configs/scoring.yaml` normalization (NFC, casefold, punctuation -> space), the same policy used
    to score every system, so the GMM-HMM vocabulary and the scorer agree.
  * Train clips whose normalized text has any character outside the Georgian Mkhedruli block (U+10D0-U+10FF)
    are left out of acoustic/LM training (5 clips: emoji, "®", Latin "vs"), so the phone set is Georgian letters.
  * Train speakers with many clips are split into pseudo-speakers of <= --max-utts-per-spk clips (Kaldi job
    balancing and per-speaker CMVN/fMLLR); dev/test keep the real Common Voice speaker. FLEURS has no speaker
    labels, so each FLEURS utterance is its own speaker.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

from asrbench.dataset import load_manifest
from asrbench.normalize import load_policies

NON_GEORGIAN = re.compile(r"[^ა-ჿ ]")
CORPORA = {  # name -> (manifest, splits)
    "cv": ("data/cv/ka/manifest.jsonl", ("train", "dev", "test")),
    "fleurs": ("data/fleurs/ka_ge/manifest.jsonl", ("dev", "test")),
}


def phone(ch: str) -> str:
    """Kaldi phone name for one character: the letter itself, or a safe code for anything else."""
    return ch if unicodedata.category(ch)[0] in "LN" else f"U{ord(ch):04X}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--wsl-data-root", required=True, help="where the repo's data/ tree lives inside WSL")
    ap.add_argument("--max-utts-per-spk", type=int, default=200)
    a = ap.parse_args()
    policy = load_policies("configs/scoring.yaml").for_language("ka")
    data_root = Path("data").resolve()
    out = Path(a.out)
    stats: dict = {"policy": policy.to_dict(), "sets": {}}
    train_words: Counter = Counter()

    for corpus, (manifest_path, splits) in CORPORA.items():
        ds = load_manifest(manifest_path)
        for split in splits:
            items = ds.select(split, ["ka"])
            d = out / "data" / f"{corpus}_{split}"
            d.mkdir(parents=True, exist_ok=True)
            per_spk: dict[str, list] = defaultdict(list)
            for it in items:
                per_spk[it.speaker or it.id].append(it)
            rows, dropped = [], []  # (utt, spk, item, words); train ids left out
            for spk, its in per_spk.items():
                its.sort(key=lambda x: x.id)
                for k, it in enumerate(its):
                    words = policy.normalize(it.reference)
                    if split == "train" and (not words or NON_GEORGIAN.search(words)):
                        dropped.append(it.id)  # nothing to align / not Georgian letters
                        continue
                    s = spk if split != "train" else f"{spk}_{k // a.max_utts_per_spk:03d}"
                    utt = s if s == it.id else f"{s}-{it.id}"
                    rows.append((utt, s, it, words))
            rows.sort(key=lambda r: r[0])
            rel = lambda it: PurePosixPath(*ds.audio_path(it).resolve().relative_to(data_root).parts)  # noqa: E731
            w = lambda name, lines: (d / name).write_text("".join(l + "\n" for l in lines), encoding="utf-8", newline="\n")  # noqa: E731
            w("wav.scp", [f"{u} ffmpeg -nostdin -loglevel error -i {a.wsl_data_root}/{rel(it)} -ac 1 -ar 16000 -f wav - |"
                          for u, _, it, _ in rows])
            w("text", [f"{u} {t}".rstrip() for u, _, _, t in rows])
            w("utt2spk", [f"{u} {s}" for u, s, _, _ in rows])
            spk2utt: dict[str, list] = defaultdict(list)
            for u, s, _, _ in rows:
                spk2utt[s].append(u)
            w("spk2utt", [f"{s} {' '.join(us)}" for s, us in sorted(spk2utt.items())])
            w("utt2dur", [f"{u} {it.duration}" for u, _, it, _ in rows if it.duration])
            w("uttmap", [f"{u}\t{it.id}" for u, _, it, _ in rows])
            toks = Counter(x for *_, t in rows for x in t.split())
            if corpus == "cv" and split == "train":
                train_words = toks
                w_lm = out / "local"
                w_lm.mkdir(parents=True, exist_ok=True)
                (w_lm / "lm_train.txt").write_text("".join(t + "\n" for *_, t in rows), encoding="utf-8", newline="\n")
            stats["sets"][f"{corpus}_{split}"] = {"utts": len(rows), "speakers": len(spk2utt), "tokens": sum(toks.values()),
                                                 "types": len(toks), "hours": round(sum(it.duration or 0 for _, _, it, _ in rows) / 3600, 2)}
            if dropped:
                stats["sets"][f"{corpus}_{split}"]["left_out"] = dropped

    vocab = sorted(train_words)
    for name, st in stats["sets"].items():
        if name == "cv_train":
            continue
        toks = Counter(x for l in (out / "data" / name / "text").read_text(encoding="utf-8").splitlines() for x in l.split()[1:])
        oov = {t: c for t, c in toks.items() if t not in train_words}
        st["oov_token_rate"] = round(sum(oov.values()) / max(1, sum(toks.values())), 4)
        st["oov_type_rate"] = round(len(oov) / max(1, len(toks)), 4)

    dct = out / "local" / "dict"
    dct.mkdir(parents=True, exist_ok=True)
    phones = sorted({phone(c) for wd in vocab for c in wd})
    (dct / "lexicon.txt").write_text("<UNK> SPN\n" + "".join(f"{wd} {' '.join(phone(c) for c in wd)}\n" for wd in vocab),
                                     encoding="utf-8", newline="\n")
    (dct / "nonsilence_phones.txt").write_text("".join(p + "\n" for p in phones), encoding="utf-8", newline="\n")
    (dct / "silence_phones.txt").write_text("SIL\nSPN\n", encoding="utf-8", newline="\n")
    (dct / "optional_silence.txt").write_text("SIL\n", encoding="utf-8", newline="\n")
    (dct / "extra_questions.txt").write_text("", encoding="utf-8", newline="\n")
    stats["lexicon"] = {"words": len(vocab), "phones": phones}
    (out / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8", newline="\n")
    print(json.dumps({k: v for k, v in stats.items() if k != "policy"}, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
