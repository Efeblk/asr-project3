# ASR Project 3 — Georgian (`ka`) Speech Recognition

Reproducible evaluation and fine-tuning benchmark for **Georgian (`ka`)** automatic speech recognition (ASR), solo group **`stray`** (İsmet Efe Balık). This repository contains `asrbench` (our evaluation and training harness), all frozen run deliverables (`runs/`), cleaned dataset manifests (`data/manifests/`), lightweight trained MMS adapters and our CV-train word 3-gram LM (`artifacts/`), classical Kaldi recipe (`recipes/kaldi-gmm-ka/`), final report (`docs/report.md`), and presentation deck (`presentation/`).

## 1. Language, Data, Splits & Cleaning

- **Language:** **Georgian (`ka`, Mkhedruli script)** — non-English, eligibility confirmed, unique in the class register (`materials/course/images/class-language-register-2026-11-18.png`).
- **Why Georgian qualifies for low-resource:** Among the four pretrained ASR families listed by the course, only Whisper lists Georgian (`nvidia/canary-1b-v2`, `nvidia/parakeet-tdt-0.6b-v3`, and `Qwen/Qwen3-ASR` do not), and zero-shot Whisper is unusable (`large-v3`: 72.04% WER; `small` and `turbo` loop past 100%). Openly licensed human-transcribed training audio is 147.5 h from only 139 speakers.

| Dataset | Split | Clips (utt) | Hours | Speakers | Speaker-disjoint? | Overlap with CV train (raw / norm.) |
|---|---|---:|---:|---:|---|---|
| [Common Voice Scripted Speech 27.0 – `ka`](https://mozilladatacollective.com/datasets/cmu5x9qda00fenq07byl8rlc8) (CC0) | `train` | 99,768 | 147.47 | 139 | Official `client_id` split, verified (0 shared) | — |
| Common Voice 27.0 – `ka` | `dev` | 14,216 | 23.22 | 221 | Verified (0 shared) | 0 raw / 21 norm. (0.15%) |
| Common Voice 27.0 – `ka` | `test` | 14,259 | 23.28 | 1,058 | Verified (0 shared) | 0 raw / 18 norm. (0.13%) |
| [FLEURS `ka_ge`](https://huggingface.co/datasets/google/fleurs) (CC BY 4.0, rev `70bb2e84b976`) | `dev` | 409 | 1.2 | N/A | Sentence-disjoint (147 sent); unseen test speakers per authors | 0 raw / 0 norm. |
| FLEURS `ka_ge` | `test` | 979 | 3.1 | N/A | Sentence-disjoint (350 sent) | 0 raw / 0 norm. |

- **Committed data & cleaning log:** Complete cleaned text manifests (IDs, relative audio paths, raw human references, hashed speaker IDs, durations) are committed in [`data/manifests/`](data/manifests/) (`cv_ka_manifest.jsonl.gz`, `fleurs_ka_ge_manifest.jsonl.gz`), with full cleaning and exclusion records in [`data/CLEANING.md`](data/CLEANING.md) (1 corrupted CV test reference `common_voice_ka_38257760`, 1 Whisper 448-token train drop, 5 Kaldi non-Georgian train drops). Raw Common Voice audio (10.4 GB) is excluded due to GitHub size limits and Mozilla Data Collective redistribution terms; archive SHA256 and exact import commands are in [`data/README.md`](data/README.md) and [`docs/data-notes-cv-ka.md`](docs/data-notes-cv-ka.md).
- **Evaluation protocol:** All checkpoints, LM weights (`α`, `β`), Kaldi `LMWT`/`WIP`, and chunk lengths were selected strictly on **dev**. Test configs require `frozen: true` and ran once each. Round 1 (all baselines + Whisper FT + MMS FT) was strictly blind test; Round 2 (`+LM`, r2 retrain, chunking) is disclosed as a follow-up on a reused test set; Round 3 ([`docs/preregistration-round3.md`](docs/preregistration-round3.md)) added 3-seed variance, same-GPU speed, dev decoder ablation, and one-time FLEURS re-runs after fixing a >30 s Whisper batch bug.

## 2. Metrics & Justification (HF Audio Course, Ch. 5)

Metric choices follow the [Hugging Face Audio Course, Chapter 5: Evaluation](https://huggingface.co/learn/audio-course/en/chapter5/evaluation):

- **Normalized Corpus WER `(S + D + I) / N` (primary):** Counts pooled over the whole test set (not per-clip mean) under one declared policy (`configs/scoring.yaml`: Unicode NFC, casefold, punctuation → space), applied identically to reference and hypothesis at scoring time while keeping `predictions.jsonl` raw. WER can exceed 100%, which exposes Whisper zero-shot hallucination loops (Word Accuracy `1 − WER` breaks down above 100% and is not reported).
- **CER (always alongside WER):** Character error rate over characters (spaces included). Georgian is agglutinative: a single wrong suffix letter marks an entire word wrong. CER separates near-miss acoustic models (greedy MMS FT: 22.00% WER, 3.63% CER) from closed-vocabulary swaps (Kaldi GMM-HMM: 22.64% WER, 8.22% CER — 2.3× higher CER at identical WER).
- **Orthographic WER / CER:** Case and punctuation kept, revealing the real-world trade-off when punctuated output is required (Whisper-turbo FT 15.83–15.91% vs MMS FT + LM 30.45%, since CTC/LM outputs carry no punctuation).
- **RTFx (throughput):** Audio duration divided by decoding time (higher = faster). Because runs spanned several GPUs, a comparable same-GPU benchmark (`runs/speed4070_*`, RTX 4070 SUPER, first 500 CV dev clips, batch 8) isolates the 8.5× speed gap between MMS+LM (340×) and Whisper FT r2 (40×). *(Note: NeMo timing includes temporary WAV staging inside `transcribe()`; Kaldi timing covers CPU MFCC + lattice decode on 8 jobs.)*
- **Uncertainty & empty-reference handling:** 95% paired and unpaired cluster-bootstrap CIs (2,000 resamples, `seed=0`, resampling speakers on CV and sentences on FLEURS). One corrupted CV test clip (`common_voice_ka_38257760`, raw reference `????...`) becomes empty after normalization and is excluded identically from WER/CER and reported separately in every `scores.json`.

## 3. Systems: Architecture vs Specific Checkpoints (Baselines & Ours)

| Paradigm / Architecture | Specific Model & Pinned Revision | Role |
|---|---|---|
| MFCC + GMM-HMM (LDA+MLLT+SAT) | Kaldi `tri3b` trained from scratch on CPU ([`recipes/kaldi-gmm-ka/`](recipes/kaldi-gmm-ka/README.md), 91k closed vocab + CV-train 3-gram LM) | Classical baseline (trained by us) |
| Attention Encoder-Decoder (Transformer) | `openai/whisper-small` (`973afd24`), `openai/whisper-large-v3` (`06f233fe`), `openai/whisper-large-v3-turbo` (`41f01f3f`) | Pretrained baselines |
| Attention Encoder-Decoder (Transformer) | **Full fine-tune of `openai/whisper-large-v3-turbo`** (809 M params, orthographic targets, r1 & r2) + 14 s pause-chunk ablation | **Ours (contribution)** |
| Self-Supervised Encoder + CTC (`wav2vec 2.0`) | `xsway/wav2vec2-large-xlsr-georgian` (`b29b8194`), `facebook/mms-1b-all` + `kat` adapter (`3d33597e`) | Pretrained baselines |
| Self-Supervised Encoder + CTC (`wav2vec 2.0`) | **`kat` adapter-only fine-tune** (2.3 M params, `ctc_zero_infinity`, seeds 42/7/13) + **shallow-fusion beam-100 Kneser-Ney 3-gram LM** (`α=0.5, β=0`, `pyctcdecode`/KenLM) | **Ours (contribution)** |
| Conformer Hybrid Transducer-CTC (RNN-T) | `nvidia/stt_ka_fastconformer_hybrid_large_pc` (`bdfd7871`, NeMo RNN-T head) | Pretrained baseline *(CV17-contaminated on CV; valid on FLEURS)* |

### Course-listed baselines that do not support Georgian

Checked on each Hugging Face model card and omitted rather than run with wrong language hints:
- [`nvidia/canary-1b-v2`](https://huggingface.co/nvidia/canary-1b-v2): 25 European languages (no Georgian).
- [`nvidia/parakeet-tdt-0.6b-v3`](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3): 25 European languages (no Georgian).
- [`Qwen/Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) / [`Qwen/Qwen3-ASR-0.6B`](https://huggingface.co/Qwen/Qwen3-ASR-0.6B): 30 languages + 22 Chinese dialects (no Georgian).
- **HuBERT + CTC (`ka`):** no Georgian HuBERT ASR checkpoint found on Hugging Face Hub ([Hub search](https://huggingface.co/models?pipeline_tag=automatic-speech-recognition&language=ka&search=hubert)).

## 4. Headline Georgian Test Results (Frozen Test)

Regenerated directly from committed `runs/*/scores.json` via `uv run python scripts/results_table.py ka` (full tables, 95% CIs, orthographic scores, and paired bootstrap tests in [`docs/results-georgian.md`](docs/results-georgian.md) and [`docs/report.md`](docs/report.md)).

| Group | System | CV ka WER (%) | CV ka CER (%) | CV Ortho WER (%) | FLEURS ka WER (%) | FLEURS ka CER (%) | Same-GPU RTFx (4070S) |
|---|---|---:|---:|---:|---:|---:|---:|
| baseline | Whisper-small (zero-shot) | 825.33 | 320.04 | 834.43 | 288.95 ‡ | 139.05 ‡ | 14 |
| baseline | Whisper-large-v3 (zero-shot) | 72.04 | 16.64 | 74.73 | 69.68 ‡ | 21.23 ‡ | 12 |
| baseline | Whisper-large-v3-turbo (zero-shot) | 142.14 | 185.45 | 140.03 | 126.05 ‡ | 108.51 ‡ | 23 |
| baseline | XLS-R-300M Georgian, xsway (CTC) | 46.26 | 9.02 | 57.85 | 52.49 | 11.83 | 788 |
| baseline | MMS-1b-all + `kat` (best pretrained CV) | 24.14 | 4.45 | 40.14 | 25.32 | 4.76 | 382 |
| baseline | Kaldi `tri3b` GMM-HMM + LM + SAT (trained by us, CPU) | 22.64 | 8.22 | 39.64 | 39.64 | 14.95 | 33 (CPU) |
| baseline | NVIDIA FastConformer `ka` (RNN-T)\* | *4.85* | *1.27* | *9.53* | **15.49** | 5.32 | 253 |
| **ours (Round 1, blind)** | **MMS `kat` adapter FT (2.3 M params, greedy)** | 22.00 | 3.63 | 39.15 | 26.02 | 5.65 | 357 |
| **ours (Round 1, blind)** | **Whisper-large-v3-turbo full FT (809 M params, r1)** | **12.80** | **2.60** | **15.91** | 27.47 § | 12.15 § | 40 (r2) |
| baseline + our LM (Round 2) | MMS `kat` zero-shot + our CV-train 3-gram LM (ablation) | 13.50 | 3.08 | 32.20 | 18.36 | 3.81 | 341 |
| **ours + decoder (Round 2)** | **MMS `kat` adapter FT + our 3-gram LM (seed 42)** | **11.07** | **2.13** | 30.45 | 19.28 | **4.64** | **340** |
| **ours (Round 2)** | Whisper-large-v3-turbo full FT retrain `r2` (plain) | 12.71 | 2.59 | **15.83** | 27.27 ‡ | 12.10 ‡ | 40 |
| **ours + decoder (Round 2)** | `r2` + 14 s pause chunks (negative result) | 12.84 | 2.70 | 15.96 | 30.00 | 13.95 | 39 |

- **3-seed variance (Round 3, MMS adapter FT, seeds 42 / 7 / 13):** greedy CV **21.97 ± 0.06%** (FLEURS **25.79 ± 0.20%**); + 3-gram LM CV **11.04 ± 0.06%** (FLEURS **19.17 ± 0.10%**).
- \* NVIDIA CV numbers are italicized and excluded from CV comparisons due to CV 17.0 training overlap (`scripts/cv_contamination.py`: 1.77% in older 40M bin → 22.98% on newest clips). FLEURS test is held out per NVIDIA's card.
- ‡ Post-fix FLEURS re-run after fixing the >30 s Whisper batch bug (frozen values in `docs/report.md` §4); § r1 weights were not retained from Colab so r1 could not be re-run (`r2` is the same recipe). Run-level git provenance caveats (`git_commit: null` on Colab archive runs, `git_dirty: true` on local pre-commit runs) are fully disclosed in [`docs/report.md`](docs/report.md) §6.

### Fixed Seeds

| Component | Fixed Seed(s) | Where configured |
|---|---|---|
| Primary fine-tuning (Whisper FT r1/r2, MMS FT seed 42) | `42` | `configs/train/*` |
| Multi-seed MMS adapter FT (Round 3) | `42`, `7`, `13` | `configs/train/ka_mms_kat_adapter*.yaml` |
| In-training dev evaluation subset (300 clips) | `dev_seed: 42` | `src/asrbench/train.py` |
| Cluster bootstrap CIs & paired tests (2,000 draws) | `seed: 0` | `src/asrbench/bootstrap.py` |

## 5. Setup, Tests & Reproducing

Requires Python 3.12, [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip`, and `ffmpeg` on `PATH`. Every dependency is pinned in [`requirements.txt`](requirements.txt) (exported from [`uv.lock`](uv.lock)) and [`pyproject.toml`](pyproject.toml).

```bash
# Option A (recommended): exact locked environment via uv
uv sync --locked --extra hf --group dev         # add `--extra lm` on Linux/WSL for KenLM beam search

# Option B: standard pip with pinned requirements.txt
pip install --extra-index-url https://download.pytorch.org/whl/cu130 -r requirements.txt

# Run the automated test suite (data importers, leakage/frozen checks, slide metrics, CPU training):
uv run pytest                                   # 36 tests with `--extra hf` (32 passed + 1 skipped without torch)
```

### Reproducing from the repository

```bash
# 1. Regenerate every score & table from committed raw predictions (no audio download needed)
uv run asrbench score runs/mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka_test_20261120T005922Z
uv run asrbench compare \
  runs/mms-1b-all-kat_cv-ka_test_20261118T224542Z \
  runs/mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka_test_20261120T005922Z
uv run python scripts/results_table.py ka > docs/results-georgian.md

# 2. Rebuild our best fair checkpoint (MMS kat adapter FT + CV-train 3-gram LM) from committed artifacts/
mkdir -p lm
gzip -dc artifacts/lm/ka_cv_train_tg.arpa.gz > lm/ka_cv_train_tg.arpa
uv run python scripts/rebuild_mms_adapter.py \
  artifacts/mms-kat-adapters/seed42/adapter.kat.safetensors \
  checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_seed42/final

# 3. Full pipeline from audio (see data/README.md for CV archive & SHA256 verification)
uv run asrbench import-cv data/cv/raw/.../ka --out data/cv/ka/manifest.jsonl
uv run asrbench import-fleurs ka_ge --splits dev test --out data/fleurs/ka_ge/manifest.jsonl
uv run asrbench validate data/cv/ka/manifest.jsonl
uv run asrbench train configs/train/ka_mms_kat_adapter.yaml
uv run asrbench run configs/runs/ka/mms-1b-all-kat-adapter-ft_cv-ka+lm_cv-ka-test.yaml
```

*(Training on Colab A100/L4 was executed via CLI using the exact `uv run asrbench train <config>` commands above, not via a manual-upload notebook; exact training configs, logs, and `train_ids.txt` are committed under `runs/train_*`.)*

## 6. Kazakh Pipeline Pilot (Archived)

Before switching to Georgian, Kazakh (`KSC2` + `FLEURS kk`) was explored first as an initial pipeline test until another group (`GYBZM`) registered Kazakh in the class register. The Kazakh pilot runs, configs (`configs/runs/kk/`), and summary ([`docs/results-kazakh.md`](docs/results-kazakh.md)) are retained solely as an archived pilot and are not our graded project language.

## 7. Repository Map (Every Root File & Folder)

| Entry | Purpose |
|---|---|
| `README.md` | Project overview, data/metric justification, headline Georgian results, setup, and reproduction guide |
| `LICENSE` | MIT license covering all original code in this repository (upstream datasets & checkpoints keep their own licenses) |
| `pyproject.toml` | Package metadata and exact pinned dependencies for `asrbench` |
| `requirements.txt` | Exact `==`-pinned pip requirements exported directly from `uv.lock` |
| `uv.lock` | Cross-platform lockfile generated by `uv` |
| `.python-version` | Pinned Python version (`3.12`) |
| `.gitattributes` | Git `export-subst` attribute for recording commit SHA in `src/asrbench/ARCHIVE_COMMIT` |
| `.gitignore` | Excludes raw audio, multi-GB checkpoints, caches, and temporary preview exports |
| `artifacts/` | Committed lightweight trained MMS `kat` adapters (seeds 42/7/13, 8.7 MB each) and gzipped CV-train 3-gram KenLM ARPA (`artifacts/README.md`) |
| `configs/` | Scoring policies (`scoring.yaml`, `scoring-nofillers.yaml`), Georgian/Kazakh evaluation configs (`runs/`), and training configs (`train/`) |
| `contributions/` | Required per-member contribution record (`IsmetEfeBalik_2509011061_Efeblk.md`) |
| `data/` | Committed cleaned text manifests (`data/manifests/*.jsonl.gz`), cleaning log (`data/CLEANING.md`), and audio import instructions (`data/README.md`) |
| `docs/` | Final report (`report.md`), generated result tables (`results-georgian.md`, `results-kazakh.md`), error analysis (`error-analysis-georgian*.md`), split audit (`split-audit.md`), data provenance (`data-notes-*.md`), Round 3 pre-registration (`preregistration-round3.md`), and project reference notes |
| `materials/` | Instructor announcements (A1, A2, A3) and class language register screenshot (`materials/course/`) |
| `presentation/` | Final 5-slide English presentation (`project3-presentation-short.pptx`), figure/slide generator scripts (`make_figures.py`, `make_short.py`, plotting the verified numbers from `docs/results-georgian.md` and `docs/error-analysis-georgian-data.md`), figures (`figures/`), and rehearsal guide (`SPEAKER_GUIDE.md`) |
| `recipes/` | Classical Kaldi MFCC+GMM-HMM (`LDA+MLLT+SAT`) recipe trained from scratch on CPU (`recipes/kaldi-gmm-ka/`) |
| `runs/` | Committed run manifests, raw `predictions.jsonl`, `scores.json`, `item_scores.jsonl`, and training logs (`runs/README.md`) |
| `scripts/` | Analysis, selection, and table-generation scripts (`results_table.py`, `split_audit.py`, `cv_contamination.py`, `error_analysis_ka.py`, `lm_select.py`, `chunk_select.py`, `rebuild_mms_adapter.py`, `round3_*.py`) |
| `src/asrbench/` | Core evaluation and training harness (`cli.py`, `dataset.py`, `importers.py`, `audio.py`, `normalize.py`, `metrics.py`, `bootstrap.py`, `runner.py`, `scoring.py`, `train.py`, `models/`, `eligibility.py`, `envinfo.py`, `langfilter.py`) |
| `tests/` | Automated `pytest` suite covering slide metric checks, CV importer, speaker leakage & frozen-test guards, pause splitting, language filter, and CPU training |

## Licensing

All original code in this repository is licensed under the **MIT License** ([`LICENSE`](LICENSE)). Datasets (Common Voice 27.0 CC0 + Mozilla Data Collective terms; FLEURS CC BY 4.0) and third-party pretrained checkpoints (OpenAI Whisper, Meta MMS, xsway XLS-R, NVIDIA FastConformer) remain governed by their respective upstream licenses.
