# Contribution Record

- **Name:** İsmet Efe Balık
- **Student ID:** 2509011061
- **GitHub Username:** `Efeblk`
- **Group:** `stray` (solo — group of one)
- **Language:** Georgian (`ka`) — eligibility confirmed, unique in class register

## Git History & Tooling Disclosure

- This is a **solo project** (group of one), so all commits on `main` were authored by me.
- Local commits were made from my personal Windows/WSL workstation under the git author name `efehomepcwindows`, linked to my GitHub account `Efeblk`.
- AI coding assistants (Claude / Codex / Gemini) were used as development and code-review tools during implementation, which is reflected in `Co-Authored-By` trailers on some commits; all experimental design decisions, executions, verification, and submission responsibility are mine.

## Individual Contributions (100% — Solo)

1. **Evaluation & training harness (`src/asrbench/`, `tests/`):** Designed and built the reproducible CLI harness (`import-cv`, `import-fleurs`, `validate`, `run`, `score`, `compare`, `train`), cluster-bootstrap CIs, normalized + orthographic WER/CER + RTFx scoring, silence/empty-reference reporting, and 36-test automated suite.
2. **Data preparation, split audit & cleaning (`data/`, `scripts/split_audit.py`, `scripts/cv_contamination.py`):** Imported Common Voice Scripted Speech 27.0 `ka` and FLEURS `ka_ge`, verified 0 speaker overlap and 0 raw verbatim sentence overlap across splits, audited NVIDIA FastConformer CV 17.0 contamination by clip-ID age, and documented all filtered/corrupted clips in `data/CLEANING.md`.
3. **Baselines (`configs/runs/ka/`, `recipes/kaldi-gmm-ka/`):** Evaluated all Georgian-supporting baselines across all four course paradigms (Whisper `small`/`large-v3`/`large-v3-turbo`, `xsway/wav2vec2-large-xlsr-georgian`, `facebook/mms-1b-all` `kat`, `nvidia/stt_ka_fastconformer_hybrid_large_pc`), documented unsupported checkpoints (Canary v2, Parakeet v3, Qwen3-ASR, HuBERT+CTC), and implemented/trained the classical MFCC+GMM-HMM (`Kaldi tri3b`, LDA+MLLT+SAT) baseline from scratch on CPU.
4. **Model & decoder contributions (`configs/train/`, `scripts/lm_select.py`, `scripts/chunk_select.py`, `artifacts/`):**
   - Full fine-tuning of `openai/whisper-large-v3-turbo` (809 M params, orthographic targets) on CV 27.0 `ka` train (r1 + r2 retrain) and pause-chunked decoding negative-result analysis.
   - Adapter-only fine-tuning of `facebook/mms-1b-all` (`kat` adapter, 2.3 M params, `ctc_zero_infinity`) across 3 seeds (`42`, `7`, `13`).
   - Shallow-fusion beam-100 decoding with our CV-train Kneser-Ney word 3-gram KenLM (`α=0.5, β=0` selected on dev) + same-GPU dev decoder ablation and RTX 4070 SUPER speed benchmark.
5. **Analysis, reporting & presentation (`docs/`, `presentation/`):** Full error analysis (Whisper byte-BPE token-budget truncation, digits mismatch, OOV vs closed-vocab, speaker breakdown), final report (`docs/report.md`), and 5-slide presentation deck (`presentation/`).
