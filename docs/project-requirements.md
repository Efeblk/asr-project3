# Project requirements

Sources:
- **L#** = Week 9 course lecture deck (`week09-asr-lecture.pptx`, course material — not redistributed in this repo), slide #
- **S#** = Week 9 course study deck (`week09-asr-study.pptx`, course material — not redistributed in this repo), slide #
- **A1** = the announcement "Project 3 Baselines and Bonus Points" (`materials/course/announcement-2026-11-17-baselines-and-bonus.md`). It is newer than the decks, so **where they disagree, A1 wins.**

> The decks say "the project"; A1 calls it "Project 3", which confirms they are the same project.
>
> **Deadline: Monday 2026-11-23** (told by the student on 2026-11-19). **Still unknown:** grading breakdown (beyond the bonus dimensions in §0), report format, and presentation date/length/format. A1 confirms there will be **presentations**. When more details arrive, add them to `materials/course/` and update this file.
>
> **Likely rubric (from Project 2's grade sheet, shown by the student on 2026-11-21):** Technical Depth, Fluency, Pace,
> Data Novelty, Problem Novelty, Rigor, Correctness. Fluency and Pace are presentation criteria, so **the presentation
> is graded**. Our P2 marks lost the most on Technical Depth (3.5), Correctness (3.5) and Rigor (4.5); no written
> feedback was given. P3 checks against this: blind test or an open disclosure, seed and hardware caveats,
> contamination checks, human references only, no data leaks (A2 is graded under Correctness).

## 0. What A1 changed (read this first)

| Topic | Before A1 (decks) | After A1 |
|---|---|---|
| **Contribution** | Fine-tuning optional (S71, L40); the project looked like evaluation only. | **Running pretrained models is only a baseline.** Every Week 9 method in its standard form is a baseline, including MFCC + GMM-HMM, CTC, attention encoder-decoder, transducers, wav2vec 2.0/HuBERT-based ASR, Whisper, Canary, Parakeet and Qwen3-ASR. **Your own training or fine-tuning is the contribution.** Implementing and training a simpler method yourself also earns credit. |
| **Reporting** | Per-language results. | Keep the standard baseline results and report the trained version **separately on the same test set**. **Clearly separate baseline performance from the contribution.** |
| **Languages** | Cover as many eligible languages as you can (L6, S9). | "Each group must choose **a** non-English language that is **different from the other groups'** languages. Coordinate before starting." At least one language, unique across the class. **Extra languages are welcome** (confirmed by the student, 2026-11-17). |
| **Bonus: low resource** | — | Low-resource languages **can earn higher points**, provided there is enough usable data and reliable reference transcription for evaluation. |
| **Bonus: domain** | MedASR mentioned only as background. | Domain-specific ASR (legal, medical, financial, other specialised domain) is **another bonus dimension**. Needs appropriate audio and trustworthy reference transcripts. |
| **Metrics** | WER and CER (S11). | Compare the applicable baselines on the same test data and scoring rules, and **justify** the choice of WER, CER and additional metrics from the HF audio course evaluation page (see §4a). |
| **Checkpoints** | Exact language support (S9). | Same, plus: a bare HuBERT or wav2vec 2.0 encoder **without an ASR head cannot transcribe**, so it is not a valid baseline. |

## 1. Task

**Speech in, same-language transcript out.** This is automatic speech recognition (ASR), not translation (S1).

The task is to evaluate ASR models on languages the group chooses, measured against trusted reference transcripts.

## 2. Language eligibility (instructor requirements)

Sources: L6, L7, S9, S10.

| Rule | Detail |
|---|---|
| No English | No exceptions, even when the strongest checkpoint is English-only. |
| No mother tongue of any group member | Confirm eligibility publicly, but keep individual mother tongues private. |
| Same-language recognition | The speech and the reference transcript must be in the same language. |
| Trusted references | Use independent reference transcripts. Not knowing a language is no excuse for inventing labels, and a model's own output is never ground truth. |
| Uniqueness (A1) | Choose a language **different from every other group's**. Coordinate before starting. This replaces the decks' softer "prefer unclaimed languages". |
| Breadth | Extra languages are welcome (confirmed 2026-11-17), in line with the decks' "cover as many as you can evaluate adequately". Each one still needs eligibility, data, references and model support. |
| Low-resource bonus (A1) | Higher points for a low-resource language, **only if** there is enough usable data (for training *and* evaluation) and reliable references. |
| Domain bonus (A1) | Optional domain focus (legal, medical, financial, …) with matching audio and trustworthy references. |
| Feasibility | You need trusted references, suitable data splits, and **exact** checkpoint support for the language and variety. |

## 3. Shared language register / tracker

Sources: L7, S10, L36.

Each group proposes its languages in the shared class tracker **before** running experiments.

Fields per entry:
- **Group and language:** group ID, language code and variety.
- **Data and model:** dataset, version and split; the supported checkpoint and its revision.
- **Eligibility and status:** restrictions checked; Proposed, Confirmed or Needs revision.
- **Coverage:** an overlap note. The class counts distinct confirmed languages, and locales of the same language are not counted as separate languages.

The workflow is Proposed → (instructor) Confirmed or Needs revision. **A language only counts as reserved once it is Confirmed.**

L36 is a 15-minute in-class coordination session. Each group should leave it with eligible language choices, data/model plans, a fixed evaluation protocol, and one next experiment.

## 4. Required deliverables: "A project result is more than a transcript"

Sources: S11, L8.

| Artifact | Contents |
|---|---|
| **Run manifest** | Data IDs, model and checkpoint revision, task, language, settings (preprocessing, decoder, chunking, precision, hardware) |
| **Prediction file** | Every prediction paired with its item ID and its reference. Save the raw predictions **before** scoring. |
| **Language-level results** | Errors (at least WER and CER) and runtime for each evaluated language, plus the hardware and conditions |
| **Error analysis** | Representative failures, limitations, and next experiments |

**Added by A1:** a **baseline vs contribution** split. Every table and plot must show standard baseline results and your own trained/fine-tuned system as separate rows, scored on the same test set with the same scoring rules.

A screenshot of one successful transcript is explicitly insufficient: it is neither reproducible nor representative (L8 notes). Don't average away weak languages (S11, S19).

## 4a. Metrics to justify (A1 → HF audio course, ch. 5 "Evaluation")

A1 asks you to justify WER, CER and additional metrics from https://huggingface.co/learn/audio-course/en/chapter5/evaluation. That page covers:

| Metric | Definition | Page's guidance |
|---|---|---|
| WER | (S + I + D) / N over words, with counts summed over the test set (corpus WER). Can exceed 100%. | The default; "we typically use the WER and would encourage you to as well!" |
| CER | The same formula over characters (spaces count). | Use it where words are not meaningful (e.g. Mandarin, Japanese); also penalises near-miss spellings less. |
| WAcc | 1 − WER | "Very infrequently quoted". Mention it only to dismiss it. |
| Orthographic vs normalised WER | WER on raw cased/punctuated text vs on text with case and punctuation removed (Whisper `BasicTextNormalizer`). | "Train on orthographic text and evaluate on normalised text." Report both so the effect of normalisation is visible. Drop references that are empty *after* normalisation from WER (N = 0); our harness reports them separately as silent clips. |
| RTFx | audio duration / processing time (higher is faster). | Consider it together with WER. Our harness logs RTF, which is 1 / RTFx. |

## 5. Final model-choice evidence (S80, L47)

| Question | Evidence to put in the report |
|---|---|
| Eligible? | Non-English and not a group member's mother tongue |
| Supported? | Exact language, variety, checkpoint and revision |
| Accurate? | WER and CER per language, plus important error examples |
| Practical? | Hardware, runtime, latency, and settings someone else can repeat |

Any claim that a model is state of the art needs a dataset, metric, date and comparable setup.

## 6. Experimental protocol rules

These are spread across both decks.

**Data splits** (S7, S8, L5)
- Train fits weights. Development selects settings (beam size, checkpoint, normalization). Test is run **once**, after everything is frozen.
- Keep each speaker or session in a single split.
- When you cut a recording into overlapping windows, assign the recording to a split first and only then create the windows (S8).

**Annotation contract** (S3, S4)
- Choose verbatim, edited, with timestamps, or with speakers. Use the same contract for every system.
- Disclose any text normalization.

**Comparability** (S77, L45)
Hold these fixed across systems:
- identical clip IDs and references
- one normalization policy
- one timing boundary

Record these for each model:
- checkpoint revision and language hint
- decoder settings and chunk/merge policy
- hardware, precision and batch size

Change one pipeline component at a time.

**Silence** (S76, L44)
- Keep clips whose reference is empty, and report them separately: emitted words, affected clips, silent duration.
- Don't delete them: that hides hallucinations.

**Long audio** (S70, L39)
- Use overlapping chunks and freeze the merge policy.
- Don't simply concatenate the window outputs.

**Fine-tuning / training is the contribution** (A1; was "optional" in S71, L40)
- Measure the zero-shot baselines first, then diagnose using dev errors, then train or fine-tune.
- Train only on the train split; select on dev; score the trained model on the **same frozen test set** as the baselines.
- Credit a normalizer change as a pipeline change, not as a model improvement.

**No paid service required** (S81)
- Hosted APIs are optional, and they are a different deployment from local checkpoints.

**The latest model is not mandatory** (S78)
- Check that it is feasible on your resources.
- Compare it against a reproducible smaller baseline.

## 7. In-class time budget (for context only)

The lecture plan is 95 min teaching + 10 min break + 15 min discussion/project coordination = 120 min (from the L-deck notes).
