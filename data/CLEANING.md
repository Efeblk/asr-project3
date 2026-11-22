# Data Cleaning & Filtering Log

This log documents every real data-quality issue found and every item excluded or filtered across our Georgian (`ka`) datasets (and the earlier Kazakh pilot). Text normalization (`configs/scoring.yaml`) is **never** baked into the saved manifests or predictions; raw transcripts are preserved verbatim and normalized identically on reference and hypothesis only at scoring time.

## 1. Common Voice Scripted Speech 27.0 — Georgian (`ka`)

Source: Mozilla Data Collective CC0 release (`cv-corpus-27.0-2026-09-11/ka`; archive provenance & SHA256 in `docs/data-notes-cv-ka.md`). Official speaker-disjoint splits (`client_id` hashed to 16-char hex in `data/manifests/cv_ka_manifest.jsonl.gz`):

| Split | Clips | Hours | Speakers | Raw verbatim overlap with train | Normalized overlap with train |
|---|---:|---:|---:|---:|---:|
| train | 99,768 | 147.47 | 139 | — | — |
| dev | 14,216 | 23.22 | 221 | 0 | 21 (0.15%) |
| test | 14,259 | 23.28 | 1,058 | 0 | 18 (0.13%) |

Verified by `asrbench validate` and `scripts/split_audit.py` (`docs/split-audit.md`): **0 shared speakers** across train/dev/test, **0 duplicate clip IDs**, **0 missing audio files**.

### Real data issues found & logged removals

| Stage | Count | Item(s) / Rule | Reason | Logged in |
|---|---:|---|---|---|
| **CV test scoring (all systems identically)** | **1** | `cv-ka-test-common_voice_ka_38257760` | Corrupted source reference in CV 27.0 release: reads `???????? ???????? ????? ?????? ??????.` (Georgian Unicode lost upstream). Becomes empty after normalization, so it is excluded from WER/CER identically for every model and reported separately in the silence/empty-reference table (`scores.json`). | `docs/report.md` §2, `docs/results-georgian.md`, every `runs/*/scores.json` |
| **Whisper full FT training (`r1`, `r2`)** | **1** | 1 of 99,768 CV train clips (`99,767` trained) | Target transcript exceeded Whisper's 448-token decoder budget (`max_label_tokens=448`) due to Georgian byte-BPE expansion (~20.6 tokens/word). Dropped cleanly during dataset filtering (`dropped_too_many_tokens: 1`). | `runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_*/train_manifest.json` |
| **Kaldi GMM-HMM training (`recipes/kaldi-gmm-ka/`)** | **5** | 5 of 99,768 CV train clips | Transcripts contained non-Georgian Latin/foreign characters outside the Georgian Mkhedruli graphemic phone inventory (`recipes/kaldi-gmm-ka/prepare_data.py`). Excluded before acoustic training and 91,155-word closed-lexicon LM construction. | `recipes/kaldi-gmm-ka/stats.json`, `docs/error-analysis-georgian-data.md` §5 |
| **MMS adapter FT training (seeds 42, 7, 13)** | **0** | All 99,768 train clips retained | No clips exceeded `max_train_seconds=30.0`; infinite CTC loss frames handled numerically via `ctc_zero_infinity=True` (fixing NaN divergence observed in the first smoke run). | `runs/train_mms-1b-all-kat-adapter-ft_cv-ka*/train_manifest.json` |
| **Digit / spelling audit (retained, not altered)** | 0 removed | 0 of 99,768 CV train transcripts contain digits; spelling variants (`წმიდა`/`წმინდა`) and reference inconsistencies (`აბსიდის`/`აფსიდის`) | Preserved untouched to keep human references independent; quantified in `docs/error-analysis-georgian.md` §2 & §7. | `docs/error-analysis-georgian.md` |

## 2. FLEURS `ka_ge` (Out-of-Domain Evaluation Only)

Source: `google/fleurs` (`ka_ge`, CC BY 4.0, pinned revision `70bb2e84b976`), committed text manifest in `data/manifests/fleurs_ka_ge_manifest.jsonl.gz`. Never used in any of our training or LM construction.

- **Splits used:** dev (409 clips, 1.2 h, 147 sentences), test (979 clips, 3.1 h, 350 sentences).
- **Leakage check (`docs/split-audit.md`):** 0 sentence IDs shared between FLEURS splits; **0 FLEURS dev/test sentences appear in CV 27.0 train** (0 raw, 0 normalized).
- **Removals:** 0 clips removed; all 979 test clips scored identically across every system.

## 3. Kazakh Pipeline Pilot (`KSC2`, archived pilot only)

Before switching to Georgian (another group registered Kazakh first), our KSC2 import applied `asrbench filter-lang` (`src/asrbench/langfilter.py`) to remove **10,245 Russian-language utterances** from the Kazakh corpus so that only same-language Kazakh speech remained (Rule 3). Details: `docs/data-notes-ksc2.md`.
