# AGENTS.md

This file holds context for any coding agent (Claude Code, Codex, Cursor, …) working in this repo. **Read it before re-analysing any course material.** The materials have already been extracted and digested. Use the digests below and search `materials/text/` before opening a PDF or PPTX.

## What this repo is

This repo is for a university **ASR (automatic speech recognition) course project**, done **solo** (a "group" of one, so commit straight to `main`). The students call it "Project 3"; the slides only ever say "the project". The task is to evaluate speech recognizers that output a **same-language transcript** on several **non-English** languages, against trusted reference transcripts, and to produce a reproducible, per-language evaluation.

The repo holds the course materials, their digests, and `asrbench`, the evaluation harness in `src/asrbench/`. **No languages have been chosen yet.** Swahili appears in the example config only as a test of the pipeline.

## Status (paused 2026-11-16)

- **Done:** materials digested; evaluation harness built and verified on the GPU (Whisper-small smoke run on 40 FLEURS Swahili dev clips; 22 tests pass).
- **Waiting on:** the instructor's project details, expected around the week of 2026-11-23: deadline, grading, report format, how many languages and models. Update `docs/project-requirements.md` when they arrive.
- **Next:** choose eligible languages → check FLEURS and model support → register them in the class tracker → dev runs with 2–3 models → one frozen test run → error analysis and report. Optional: install and verify the NeMo and Qwen extras.

## Harness quick reference

- **Environment:** `uv` with Python 3.12. Install with `uv sync --extra hf --group dev`. Run commands as `uv run asrbench …` and `uv run pytest`. torch 2.14 is pinned, with CUDA 13 wheels on Windows/Linux.
- **Pipeline:** `import-fleurs`/`import-tsv` → `validate` → `run <config>` → `score <run>` → `compare <a> <b>`. Usage is in README.md.
- **Data format** (`dataset.py`): manifests are JSONL with `id, audio, reference, language, split[, speaker, session, duration]`. An empty `reference` means the clip contains no speech. Bootstrap clusters use session, then speaker, then the item ID.
- **Models** (`models/`): to add a family, subclass `Recognizer`, implement `load()` and `transcribe(list[np.ndarray 16 kHz], language) -> list[str]`, and register it in `models/__init__.py`. `hf-whisper` and `hf-ctc` have been verified on the GPU. `nemo` and `qwen` follow the slide APIs but have **not been run yet**.
- **Scoring policy:** `configs/scoring.yaml`, with per-language overrides. Normalization is applied only at scoring time, and `predictions.jsonl` stays raw.
- **Tests:** `tests/test_metrics.py` encodes the slide examples (S13, S18, S20–S23, S26, S76). Keep them passing.
- **Where things live:** `data/` is gitignored and can be regenerated. `runs/<name>_<ts>/` holds real runs and is committed. `runs/_*/` holds scratch or smoke runs and is ignored.

## Project rules (hard constraints, so check every proposal against them)

Full detail, with slide citations, is in `docs/project-requirements.md`.

1. **No English** audio or transcripts, with no exceptions.
2. **No language that is the mother tongue of any group member.** Never ask for or record anyone's mother tongue in this repo. Record only "eligibility confirmed".
3. The speech and the reference must be in the **same language** (ASR, not translation).
4. **Use trusted, independent references only.** A model's output is never ground truth, and you must not invent labels.
5. **Cover as many eligible languages as you can evaluate adequately.** There is no minimum. Prefer languages no other group has claimed. The class shares a register where each entry goes from Proposed to **Confirmed** (instructor) or Needs revision.
6. Each chosen checkpoint must **explicitly support** the exact language and variety. Check the model card.
7. **Deliverables:**
   - a run manifest
   - a prediction file (item ID + reference + raw prediction)
   - per-language results (WER and CER, runtime, hardware)
   - an error analysis

   Don't average away weak languages.

**Still unknown:** deadline, group size, grading, and report format. No material so far specifies them, so ask the user rather than guessing.

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
- **Fine-tuning** is optional and comes only after a zero-shot baseline. Ablate normalizer or decoder changes separately from model changes.
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
