# Materials index

These are the files the instructor uploaded. Every binary has a searchable text copy in `materials/text/`, and that copy keeps the same base name. **Search `materials/text/` before opening any binary.**

The **Relevance** column means relevance to the project: ★★★ = primary, ★ = background only.

## course/: the instructor's own Week 9 decks (primary source for project rules)

| File | What it is | Relevance |
|---|---|---|
| `week09-asr-lecture.pptx` | "W9 · Automatic Speech Recognition" lecture, 47 slides, with speaker notes. Covers project rules (L6–L8, L36), metrics (L9–L13, L33–L35), front end (L14–L17), model families (L18–L30), model choice (L31–L47). Snapshot 13 Nov 2026. | ★★★ |
| `week09-asr-study.pptx` | Expanded study version, 93 slides, with worked calculations, runnable code and a self-check (S64–S65). Project rules: S9–S11. Deliverables: S11. Model recipes: S66–S81. | ★★★ |

Both text copies include every slide's speaker notes, which are organised as "Purpose", "Origins of values", "Step-by-step reasoning" and "Teaching script". Slides are delimited by `## Slide N`.

## textbook/: Jurafsky & Martin, *Speech and Language Processing* (August 24, 2025 draft)

Text copies are delimited by `=== page N ===`.

| File | Sections (PDF page) | Relevance |
|---|---|---|
| `jm-ch14-phonetics-and-feature-extraction.pdf` (31 pp) | Phonetic transcription 1 · Articulatory phonetics 3 · Prosody 8 · Acoustic phonetics and signals 10 · Source-filter model 19 · **Log mel spectrum** 20 (sampling 21, windowing 22, DFT 23, mel filter bank 24) · **MFCC** 25 · Exercises 27 | ★★ |
| `jm-ch15-automatic-speech-recognition.pdf` (29 pp) | ASR task and datasets (LibriSpeech, Common Voice, …) 2 · CNNs 4 · **Encoder-decoder (Whisper)** 8 · **HuBERT** 13 (k-means 15) · **CTC** 17 (inference 18, training 20, CTC + enc-dec 20, RNN-T 21) · **WER evaluation** 22 · Exercises 24 | ★★★ (the decks are built on this chapter) |
| `jm-ch16-text-to-speech.pdf` (15 pp) | TTS overview 2 · EnCodec / VQ / RVQ 3–7 · VALL-E 9 · TTS evaluation 11 · Spoken language models 12 | ★ (TTS is out of scope for an ASR project) |

## external-lectures/: other universities' slides (background reading)

**Their homework dates and "project presentations" refer to those courses, not ours.**

| File | What it is | Relevance |
|---|---|---|
| `tufts-cs136-lect03-phonetics-and-front-end.pdf` (77 pp) | Tufts CS136 (Meteer, 2017). ARPAbet, phonetics, MFCC feature-extraction pipeline. Adapted from Jurafsky. | ★ |
| `berkeley-cs294-5-fa05-lect20-asr-overview.pdf` (11 pp) | Berkeley CS294-5 (Fall 2005), statistical ASR overview (HMM era). Its "Nov 30, Dec 7: Project Presentations" belongs to that course. The upload included a byte-identical duplicate, which was dropped. | ★ |
| `stanford-cs224s-2025-lect02-phonetics.pdf` (57 pp) | Stanford CS224S (Maas, Spring 2025), phonetics lecture. Its "Homework 1 due April 14" belongs to that course. | ★ |
| `speech-processing-02-acoustic-phonetics.pptx` (64 slides) | Acoustic phonetics: sound waves, time vs frequency, Fourier transform, spectrograms, source-filter model, formants, vowel space. | ★ |

## overviews/: NotebookLM-generated summaries

| File | What it is | Relevance |
|---|---|---|
| `notebooklm-human-voice-to-machine-understanding.pdf` | 15 image-only slides. The summary is in `text/notebooklm-human-voice-to-machine-understanding.md`. | ★ |
| `notebooklm-the-science-of-speech.mp4` | Video, 7 min 05 s. **Not transcribed yet.** Judging by the title, it's a NotebookLM video overview. | ★ (unverified) |
| `notebooklm-speech-recognition-radio-rex-to-transformers.m4a` | Audio, 12 min 51 s. **Not transcribed yet.** Judging by the title, it's a NotebookLM audio overview (ASR history from Radio Rex to transformers). | ★ (unverified) |

If you transcribe the media, save the output as `text/<same-base-name>.txt` and update this table.

## links.md

The MedASR LinkedIn post (English-only, so ineligible) and all external URLs cited in the decks.
