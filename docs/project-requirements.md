# Project requirements (from the Week 9 ASR decks)

Everything here comes from the two Week 9 decks:
- **L#** = `materials/course/week09-asr-lecture.pptx`, slide #
- **S#** = `materials/course/week09-asr-study.pptx`, slide #

The searchable text, including the speaker notes, is in `materials/text/week09-asr-*.txt`. Search for `## Slide N`.

> **Naming caveat:** the decks always say "the project". They never call it "Project 3". We think it's the same thing, but nobody has confirmed that.
>
> **Still unknown:** deadline, group size, grading breakdown, and report/presentation format. None of the course materials so far contain them. When the official brief arrives, add it to `materials/course/` and update this file.

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
| Breadth | Cover as many eligible languages as you can evaluate adequately. There is no minimum count. |
| Class coordination | Prefer languages nobody has claimed yet, and coordinate when the same language is chosen twice. |
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

A screenshot of one successful transcript is explicitly insufficient: it is neither reproducible nor representative (L8 notes). Don't average away weak languages (S11, S19).

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

**Fine-tuning is optional** (S71, L40)
- Measure the zero-shot baseline first, then diagnose using dev errors, then fine-tune.
- Credit a normalizer change as a pipeline change, not as a model improvement.

**No paid service required** (S81)
- Hosted APIs are optional, and they are a different deployment from local checkpoints.

**The latest model is not mandatory** (S78)
- Check that it is feasible on your resources.
- Compare it against a reproducible smaller baseline.

## 7. In-class time budget (for context only)

The lecture plan is 95 min teaching + 10 min break + 15 min discussion/project coordination = 120 min (from the L-deck notes).
