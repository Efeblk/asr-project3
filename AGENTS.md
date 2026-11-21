# AGENTS.md

This file holds context for any coding agent (Claude Code, Codex, Cursor, …) working in this repo. **Read it before re-analysing any course material.** The materials have already been extracted and digested. Use the digests below and search `materials/text/` before opening a PDF or PPTX.

## What this repo is

This repo is for a university **ASR (automatic speech recognition) course project**, done **solo** (a "group" of one, so commit straight to `main`). The students call it "Project 3"; the slides only ever say "the project". The task is to evaluate speech recognizers that output a **same-language transcript** on a **non-English** language, against trusted reference transcripts, and to produce a reproducible, per-language evaluation. Per the instructor's announcement (A1, 2026-11-17), pretrained models are only **baselines**: the graded **contribution is our own training or fine-tuning**, reported separately on the same test set.

The repo holds the course materials, their digests, and `asrbench`, the evaluation harness in `src/asrbench/`. **Language (switched 2026-11-18, eligibility confirmed): main = Georgian (`ka`)** — Common Voice Scripted Speech ka (Mozilla Data Collective; official speaker-disjoint split) + FLEURS `ka_ge`. Our group is "stray" in the class register. Kazakh was our first choice but group GYBZM registered it first (register screenshot, `materials/course/`), so the Kazakh work (KSC2 + FLEURS kk, `docs/results-kazakh.md`) is now only a **pipeline pilot**, not our language; do not present it as our language unless the instructor allows. See `docs/language-shortlist.md`. Swahili appears in example configs only as a pipeline test.

## Status (updated 2026-11-21)

- **r2 weights preserved:** `checkpoints/whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/final` contains the full final checkpoint and tokenizer (gitignored). Model SHA256 verified against the Colab source; backup provenance is in the training run's `checkpoint_backup.json`.

- **All work completed through r2 (2026-11-20); training and experiments closed at the student's request.** r2 selected checkpoint-6000 (300-clip CV dev WER 17.32%, training generation cap 225). All 12 queued evaluations have complete raw predictions, manifests and scores; `evaluation_audit.json` in the r2 training run verifies counts, IDs/references, identical policies and frozen tests. Plain r2 test CV/FLEURS WER: 12.71/27.33%; the dev-selected 14 s chunk variant: 12.84/30.00% (negative result; fewer deletions, more insertions). All chunk candidates and the dev selection are saved. Final report: `docs/report.md`; tables: `docs/results-georgian.md`. Colab `kar` completed at 04:15:05 UTC and the watcher saved final outputs and stopped it. Do not restart training or rerun frozen tests.

- **Announcements A2 (split by speaker) and A3 (exact baseline list)** are in `materials/course/`. A3: run every listed baseline that supports the language; canary-1b-v2, parakeet-tdt-0.6b-v3 and Qwen3-ASR support neither kk nor ka (model cards) → say so in the README with links. Georgian baselines to run: Whisper small/large-v3/turbo, MMS-1b-all `kat`, `xsway/wav2vec2-large-xlsr-georgian` (CTC), `nvidia/stt_ka_fastconformer_hybrid_large_pc` (transducer, NeMo; trained on CV17 + FLEURS train/dev), plus our own MFCC+GMM-HMM (student approved). A2: report speakers/utterances/hours per split and test sentences that appear verbatim in train.

- **Georgian is DONE through frozen test (2026-11-19)** — `docs/results-georgian.md` (`uv run python scripts/results_table.py ka`). CV ka test: ours turbo FT 12.80 % WER / 2.60 % CER vs best clean pretrained baseline MMS kat 24.14 % (Δ 11.3, CI 10.9–11.8); ours MMS adapter FT 22.00 %. FLEURS ka test: NVIDIA transducer 15.49 % best; MMS 25.32 %; ours MMS FT 26.02 %, turbo FT 27.47 % (digits: CV has almost none). NVIDIA CV numbers (4.85 %) are contaminated (CV 17 training; `scripts/cv_contamination.py`). Whisper small/turbo zero-shot loop (WER > 100 %). **MFCC + GMM-HMM baseline (Kaldi, trained by us from scratch on CPU in WSL, `recipes/kaldi-gmm-ka/`) DONE 2026-11-19:** tri3b SAT, CV ka test 22.64 % WER / 8.22 % CER (beats MMS zero-shot on WER thanks to its train-text trigram LM, but CER ~2x worse), FLEURS ka test 39.64 %; LMWT/WIP frozen on CV dev before test. Conda Kaldi needs `OPENBLAS_NUM_THREADS=1` (in `path.sh`). **MMS FT + our CV-train word 3-gram LM (2026-11-20, pyctcdecode/KenLM in WSL on the local GPU; α 0.5/β 0 selected on dev, `scripts/lm_select.py`):** CV ka test **11.07 % WER / 2.13 % CER** (best fair system; beats turbo FT by 1.7, CI 1.3–2.1), FLEURS ka test 19.28 % (CER 4.64 % < NVIDIA 5.32 %). Ablation MMS zero-shot + same LM: 13.50 % / 18.36 % (the LM gives ~10.6 points, the FT +2.4 on CV; on FLEURS the FT costs 0.9 via digits). KenLM does not build on Windows: LM runs use the WSL checkout `~/asr`. Original turbo r1 weights were not kept; MMS FT was rebuilt from its adapter backup, and full r2 weights are preserved locally (see above). Do not re-run Georgian test for these systems.
- **Done:** materials digested; evaluation harness built and verified on the GPU; `asrbench train` (Whisper and CTC fine-tuning) verified on the GPU with a scratch split of Swahili dev clips (pipeline test only); orthographic WER/CER and RTFx added to scoring; 36 tests pass (2026-11-21). KSC2 imported (all dev/test, 3 % train sample, full parliament train) and Russian utterances filtered out. Zero-shot baselines on FLEURS kk/ka dev and KSC2 dev (per subcorpus) committed in `runs/`. Announcement A1 ("Project 3 Baselines and Bonus Points") recorded in `materials/course/` and folded into `docs/project-requirements.md` §0.
- **Deadline: Monday 2026-11-23** (student, 2026-11-19). **Still waiting on:** grading breakdown, report format. The presentation is graded (Fluency, Pace; see docs/project-requirements.md, likely rubric).
- **Ours (dev, 2026-11-18; all trained on the same 34.1 h KSC2 sample, Colab L4/A100):** Whisper-large-v3-turbo full FT — KSC2 dev 18.3 % WER / FLEURS kk dev 18.3 %; MMS-1b-all kaz adapter-only — 30.3 % / 19.3 %; Whisper-small full FT — 31.8 % / 29.7 %. Best baselines: KSC2 aismlv 36.1 %; FLEURS kk MMS zero-shot 16.0 % (MMS-1b-all likely saw FLEURS in training — HF card lists it; paper §5.4; Kazakh specifically unconfirmed), so our models are worse there. Turbo and MMS `final/` dirs were rebuilt locally after Colab VMs were lost (see each train manifest).
- **Kazakh test is DONE (frozen, run once, 2026-11-18)** — tables in `docs/results-kazakh.md` (regenerate with `uv run python scripts/results_table.py > docs/results-kazakh.md`). KSC2 test: ours turbo 18.1 % WER (beam-5 decoder row 17.8 %) vs best baseline aismlv 36.4 %; FLEURS kk test: ours turbo 17.2 % vs MMS zero-shot 14.4 % (still best there). Do not re-run Kazakh test for these systems. Dev ablations done: filler-free scoring (−0.5…1.0 WER, ranking unchanged), decoder (beam5 selected; no_repeat_ngram hurts: it blocks Kazakh subword suffixes).
- **Round 3 DONE (2026-11-21; pre-registered in `docs/preregistration-round3.md`; launcher `scripts/round3_run.sh`, configs `scripts/round3_configs.py` → `configs/runs/ka/round3/`):**
  - Same-GPU speed benchmark on the 4070 (`runs/speed4070_*`, first 500 CV dev clips, batch 8).
  - MMS FT seeds 7 (trained and evaluated on the local 4070, commit 9ad99b9) and 13 (trained and evaluated on a Colab A100 like seed 42, commit b8fbf88; only provenance files differ), dev + frozen test once each. Mean ± SD over seeds 42/7/13 (n = 3, descriptive only): test WER CV 21.97 ± 0.06 (+LM 11.04 ± 0.06), FLEURS 25.79 ± 0.20 (+LM 19.17 ± 0.10). The paired conclusions hold for every seed.
  - Dev-only decoder ablation plus a same-GPU greedy control (added after review): decoding only unpadded frames changes 0 predictions, beam alone ≤ 0.16, the word LM gives the whole gain (−10.9…−11.0 CV dev, −5.5…−6.6 FLEURS dev).
  - Whisper long-form bug-fix FLEURS re-runs (`*+lf-split`, batch 16 on the 4070): r2 27.33 → 27.27 (n.s.), large-v3 and small get worse, turbo unchanged; the corrected rows lead the main table (‡, frozen values in brackets), as pre-registered. Conclusions unchanged.
  - Deviations (seed-13 evaluation on Colab, per-seed commits, post-review control) are recorded in the pre-registration's execution note.
  - Reviewed twice by Codex SOL 6.2 and Antigravity NEON 4 (both: every number reproduces; Rigor 4.0 / Correctness 4.5 before fixes); all findings fixed in 7bb516d and 32cb576. All runs committed. Do not re-run these tests.
- **Next:** the presentation (graded on Fluency and Pace) — the only remaining job. No further runs planned; the Colab VM is stopped and the local GPU is free.

## Harness quick reference

- **Environment:** `uv` with Python 3.12. Install with `uv sync --extra hf --group dev`. Run commands as `uv run asrbench …` and `uv run pytest`. torch 2.14 is pinned, with CUDA 13 wheels on Windows/Linux.
- **Pipeline:** `import-fleurs`/`import-tsv`/`import-ksc2` (+ `filter-lang` for KSC2 Russian) → `validate` → `run <config>` → `score <run>` → `compare <a> <b>`; contribution: `train <config>` → run the saved checkpoint like a baseline. Usage is in README.md.
- **Training** (`train.py`, configs in `configs/train/`): train split only, checkpoint selected by dev WER under the scoring policy, test refused; `train_filter`/`dev_filter` select items by field. Weights go to `checkpoints/` (gitignored); `runs/train_*/` holds the train manifest, log and train IDs (commit). Checkpoints with a `train_manifest.json` are labelled **ours** in run manifests and reports; everything else is **baseline**. On 12 GB: Whisper-small batch 16 ≈ 1.3 s/step; XLS-R-300M CTC batch 8 peaks at 10.9 GB.
- **Data format** (`dataset.py`): manifests are JSONL with `id, audio, reference, language, split[, speaker, session, duration]`. An empty `reference` means the clip contains no speech. Bootstrap clusters use session, then speaker, then the item ID.
- **Models** (`models/`): to add a family, subclass `Recognizer`, implement `load()` and `transcribe(list[np.ndarray 16 kHz], language) -> list[str]`, and register it in `models/__init__.py`. `hf-whisper`, `hf-ctc` and NeMo FastConformer have been verified on the GPU; `qwen` has not been run. Whisper supports `chunk_seconds` (pause-based splitting); CTC supports the CV-train KenLM decoder (`scripts/lm_select.py`, Linux/WSL).
- **Provenance** (`envinfo.py`): every run manifest records commit, dirty flag, packages and hardware. A `git archive` export (e.g. on a Colab VM, no `.git`) reports its commit from `src/asrbench/ARCHIVE_COMMIT` (filled via `.gitattributes` export-subst) with `git_dirty: null`; the marker is checked before git.
- **Scoring policy:** `configs/scoring.yaml`, with per-language overrides. Normalization is applied only at scoring time, and `predictions.jsonl` stays raw. Reports normalized WER/CER (primary) plus orthographic WER/CER (case + punctuation kept) and RTFx.
- **Tests:** `tests/test_metrics.py` encodes the slide examples (S13, S18, S20–S23, S26, S76). Keep them passing.
- **Where things live:** `data/` and `checkpoints/` are gitignored. `runs/<name>_<ts>/` holds real runs and is committed. `runs/_*/` holds scratch or smoke runs and is ignored.

## Project rules (hard constraints, so check every proposal against them)

Full detail, with slide citations, is in `docs/project-requirements.md`.

1. **No English** audio or transcripts, with no exceptions.
2. **No language that is the mother tongue of any group member.** Never ask for or record anyone's mother tongue in this repo. Record only "eligibility confirmed".
3. The speech and the reference must be in the **same language** (ASR, not translation).
4. **Use trusted, independent references only.** A model's output is never ground truth, and you must not invent labels.
5. **Pick a language no other group has** (A1); coordinate first. Extra languages are welcome (confirmed 2026-11-17). Bonus for low-resource languages (if data and references suffice) and for domain-specific ASR (legal, medical, financial, …). The class shares a register where each entry goes from Proposed to **Confirmed** (instructor) or Needs revision.
6. Each chosen checkpoint must **explicitly support** the exact language and variety. Check the model card.
7. **Deliverables:**
   - a run manifest
   - a prediction file (item ID + reference + raw prediction)
   - per-language results (WER and CER, runtime, hardware)
   - an error analysis
   - **baseline results and our trained/fine-tuned system as clearly separate rows**, same test set and scoring rules (A1)
   - a justification of WER, CER and any extra metrics from the HF audio course evaluation page (orthographic vs normalised WER, RTFx)

   Don't average away weak languages.
8. **Running a pretrained model is never the contribution** (A1). Whisper, Canary, Parakeet, Qwen3-ASR, wav2vec2/HuBERT ASR, CTC, enc-dec, transducers and MFCC+GMM-HMM in standard form are all baselines. Our own training or fine-tuning is the contribution; implementing and training a simpler method ourselves also counts.

**Deadline: Monday 2026-11-23** (told by the student). **Still unknown:** grading breakdown and report format. The presentation is graded (see the likely rubric in docs/project-requirements.md). Group size is one (solo). Ask the user rather than guessing.

## Evaluation conventions to follow when writing code

Full digest: `docs/asr-methods-cheatsheet.md`.

- **Splits:** train / dev / test, with each speaker or session in only one split. Select everything (checkpoint, beam, normalizer, λ) on **dev**. Run test once, after freezing.
- **Raw predictions:** save them, keyed by item ID, **before** any normalization or scoring.
- **Scoring policy:** one declared policy per language, covering Unicode normalization, case, punctuation, diacritics, word segmentation, and CER units. Apply it identically to the reference and the hypothesis.
- **Metrics:**
  - Report **corpus** WER (pooled counts) per language, alongside CER.
  - Show per-language rows before any macro or pooled average.
  - Use a paired bootstrap for uncertainty, resampling by speaker or session cluster.
  - Use `jiwer` (`process_words`, `cer`).
- **Comparable runs** hold fixed: clip IDs, references, normalization, chunk/merge policy, and timing boundary. Log for every model: checkpoint and **revision**, language hint, decoder settings, hardware, precision, batch size, and library versions.
- **Silence:** keep clips with empty references and report them separately (emitted words, affected clips).
- **Speed:** report RTF/RTFx for throughput. Streaming latency, if measured, is a separate metric.
- **Fine-tuning/training** is required as the contribution (A1) and comes only after the zero-shot baselines; train on train, select on dev. Ablate normalizer or decoder changes separately from model changes.
- **Hosted or paid APIs are not required.** Prefer local checkpoints.
- **Do not use** `.en` Whisper checkpoints, `parakeet-tdt-0.6b-v2` (English-only), or `google/medasr` (English-only).

## Candidate checkpoints named by the course

These come from the 13 Nov 2026 snapshot. Always re-verify language support on the model card.

- Whisper multilingual (`small`, …)
- `nvidia/canary-1b-v2` (25 European languages)
- `nvidia/parakeet-tdt-0.6b-v3` (25 languages)
- `Qwen/Qwen3-ASR-1.7B` / `0.6B` (30 languages + 22 Chinese dialects)
- Language-specific wav2vec2/XLS-R CTC fine-tunes
- Optional large models: `nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B` (needs about an H100) and `nvidia/nemotron-3.5-asr-streaming-0.6b`

Code snippets for each are in the cheatsheet, §4.

## Repo layout

```
src/asrbench/                  ← harness: dataset, importers, audio, normalize, metrics, bootstrap, models/, runner, scoring, cli
configs/                       ← scoring.yaml (policy) + runs/*.yaml (run configs; examples)
tests/                         ← pytest suite (slide-derived metric checks + end-to-end)
data/                          ← gitignored audio + manifests (regenerable)
runs/                          ← run outputs (deliverables); runs/_*/ = scratch, ignored
AGENTS.md                      ← you are here (CLAUDE.md just imports this)
docs/
  project-requirements.md      ← every project rule, with slide citations
  asr-methods-cheatsheet.md    ← metrics, formulas, model families, checkpoints, code recipes, pitfalls
materials/
  INDEX.md                     ← what each file is, section→page map, relevance rating
  links.md                     ← MedASR post + all URLs cited in the decks
  course/                      ← instructor's Week 9 decks (lecture L1–L47, study S1–S93): PRIMARY
  textbook/                    ← Jurafsky & Martin ch14 (features), ch15 (ASR), ch16 (TTS)
  external-lectures/           ← other universities' slides (background; their dates ≠ ours)
  overviews/                   ← NotebookLM PDF/video/audio summaries (background)
  text/                        ← searchable text of everything above (incl. speaker notes)
```

## How to use the materials efficiently

- **Find a topic:** `grep -n -i "<term>" materials/text/*.txt`.
  - Deck text is split by `## Slide N`, and the speaker notes follow each slide.
  - PDF text is split by `=== page N ===`.
- **Cite as** `S<n>` (study deck), `L<n>` (lecture deck) or `JM15 p.<n>`, so the user can check.
- **Don't re-extract the binaries** unless the text copy is missing something visual (figures, tables drawn as images).
- The two `.mp4`/`.m4a` overviews are **not transcribed**. If you transcribe them, save the result in `materials/text/` and update `materials/INDEX.md`.

## Keeping this file useful

- When the user provides the official project brief (deadline, grading, format), add it under `materials/course/` with a text copy. Then update `docs/project-requirements.md` and the "Still unknown" line above.
- When the harness changes (new model family, new command, new output file), update the quick reference above and README.md.
- Keep this file short. Detail belongs in `docs/`.
