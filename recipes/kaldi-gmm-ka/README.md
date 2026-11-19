# MFCC + GMM-HMM baseline for Georgian (Kaldi), trained by us from scratch

This is a classical baseline (A3 lists "MFCC + GMM-HMM"). No pretrained Georgian checkpoint exists for it, so we
train it ourselves with the standard Kaldi GMM recipe on the same CV 27.0 ka train split as our fine-tunes, and score
it on the same dev/test sets with the same policy. It is reported as a **baseline** row (standard form, rule 8),
not as our contribution.

| Step | What | Data |
|---|---|---|
| Features | 13 MFCC (no energy), per-speaker CMVN; +Δ+ΔΔ (tri1) or splice ±3 → LDA 40 + MLLT (tri2b/tri3b) | |
| Lexicon | Graphemic: each word spelled with its letters (Georgian Mkhedruli is close to one letter per phoneme); 33+2 letters + SIL/SPN | 91k words of CV train |
| LM | Trigram, Kneser-Ney (`utils/lang/make_kn_lm.py`), unpruned | CV ka **train** transcripts only |
| mono | Monophone, 10k shortest train clips | |
| tri1 | Δ+ΔΔ triphones, 2500 leaves / 15k Gaussians | 30k random train clips |
| tri2b | LDA+MLLT, 4000 / 40k | all train (147.5 h) |
| tri3b | SAT (fMLLR), 4000 / 40k; decoded with two-pass fMLLR | all train |

Selection and freezing: the LM weight and word insertion penalty are chosen on **CV dev only** (`select_on_dev.sh`,
grid LMWT 7–17 × WIP {0, 0.5, 1}) and written to `decode-frozen.yaml`, which is committed before the single test
decode (`run.sh --stage 8`). Beams are the Kaldi defaults. Test features are computed only in stage 8.

Text: transcripts are normalized with the declared scoring policy (`configs/scoring.yaml`: NFC, casefold, punctuation
→ space), so the system's vocabulary matches the scorer. Hypotheses are therefore already lower-case without
punctuation: the orthographic WER/CER of this system are not meaningful. Five train clips whose text contains
non-Georgian characters (emoji, "®", Latin "vs") are left out (listed in `stats.json`).

## Reproduce (Windows + WSL2 Ubuntu 24.04, CPU only)

```bash
# WSL: Kaldi 5.5.1068 (conda-forge CPU build) + steps/utils (kaldi-asr/kaldi e02e35f0) + work dir ~/ka_gmm
bash recipes/kaldi-gmm-ka/setup.sh
# WSL: CV 27.0 ka from Mozilla Data Collective (archive sha256 8099ad5a...) under ~/data/cv/raw, linked at
#      ~/asrdata/cv/raw/common-voice-scripted-speech-27-0-georgi-6faf6605; FLEURS ka_ge dev/test wavs in ~/asrdata/fleurs/ka_ge
# Windows (repo env; MSYS_NO_PATHCONV=1 in Git Bash): Kaldi data dirs, dictionary, LM text
uv run python recipes/kaldi-gmm-ka/prepare_data.py --out <dir> --wsl-data-root /home/<user>/asrdata   # copy <dir> to ~/ka_gmm/prep
# WSL
cd ~/ka_gmm && nice -n 19 bash run.sh --stop-stage 7    # train + dev decodes (~hours on 12 CPU jobs)
bash select_on_dev.sh                                    # -> decode-frozen.yaml: copy into this folder and commit
bash run.sh --stage 8                                    # frozen test decode, once
# Windows: asrbench run dirs, then score like every other system
uv run python recipes/kaldi-gmm-ka/to_run.py --work //wsl.localhost/Ubuntu/home/<user>/ka_gmm --model tri3b --set cv_test
uv run asrbench score runs/kaldi-gmm-hmm-tri3b_cv-ka_test_<UTC>
```

`stats.json` (copied here from the prep step) has utterances, speakers, hours, vocabulary and OOV rates per set.
