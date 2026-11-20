# Georgian speech recognition: baselines, our fine-tunes, and why Georgian is hard for Whisper

ASR Project 3, group "stray" (solo). Language: **Georgian (`ka`)**, eligibility confirmed and registered in the
class register. Code, configs, run manifests, raw predictions and scores are all in this repository; every number
below can be regenerated from the committed run directories (`runs/`).

## 1. Task, language and data

We do same-language ASR: Georgian speech in, a Georgian (Mkhedruli script) transcript out, scored against the
human references that ship with each corpus. No model output is used as a label anywhere.

| Corpus | Use | Train | Dev | Test | Speakers kept apart? |
|---|---|---|---|---|---|
| Common Voice Scripted Speech 27.0 ka (Mozilla Data Collective, CC0) | training + in-domain test | 99,768 utt., 147.5 h, 139 speakers | 14,216 utt., 23.2 h, 221 speakers | 14,259 utt., 23.3 h, 1,058 speakers | yes, official split by `client_id`, verified |
| FLEURS `ka_ge` (CC BY 4.0) | out-of-domain test (read Wikipedia sentences, other speakers and microphones) | not used for training | 409 utt., 1.2 h | 979 utt., 3.1 h | no speaker IDs; sentence-disjoint, the authors state test speakers are unseen |

Split audit (announcement A2, `docs/split-audit.md`): no speaker is shared between CV splits. No dev/test sentence
appears verbatim in train as raw text, and only 21 dev and 18 test sentences (0.1 %) do after normalization.
FLEURS splits share no sentence IDs (train 1,082 / dev 147 / test 350). No FLEURS dev or test sentence occurs in CV
train, the only text our fine-tunes, word LM and GMM-HMM were trained on (0 raw, 0 normalized). FLEURS has no
speaker IDs, so its speaker separation cannot be checked here and rests on its authors' statement that test
speakers are unseen. Data provenance (archive sha256, manifest sha256, import commands) is in
`docs/data-notes-cv-ka.md`.

**Why Georgian counts as low-resource (announcement A1 bonus).** Of the four pretrained ASR families the course
names, only Whisper lists Georgian; Canary v2, Parakeet v3 and Qwen3-ASR do not (README, with model-card links). Even
Whisper is unusable zero-shot: large-v3 scores 72 % WER on CV ka test, and small and turbo loop past 100 %. The
openly licensed data with human references is small: 147.5 h of CV train from only 139 speakers, plus FLEURS. That
is still enough for training and for a 23 h speaker-disjoint test set with trusted references, which is the
condition A1 sets. We do not claim the domain bonus: both corpora are general read speech.

**Protocol.** Everything is chosen on dev: checkpoints, decoder settings, LM weights and chunk length. The harness
refuses a test run unless its config says `frozen: true`. Each test config was run exactly once: there is one run
directory per test config in `runs/`.

**Freeze record (UTC, from git and the run manifests).** The evidence is not equally strong for every row, so it is
listed per system:

| Systems | What was fixed before the test run | When | First test run |
|---|---|---|---|
| Pretrained baselines (Whisper ×3, xsway, MMS, NVIDIA) | the test configs themselves (commit 0c0d0e4) | 18 Nov 22:19 | 18 Nov 22:34 |
| Our fine-tunes, round 1 (turbo FT, MMS FT) | the selection rule, stated in the 0c0d0e4 commit message: best dev-WER checkpoint, decoding identical to the matching baseline. The generated test configs were committed together with their results (159b106, 2edbfbb) | 18 Nov 22:19 | 19 Nov 01:04 |
| Kaldi GMM-HMM | LM weight and insertion penalty, selected on dev (2dd4397) | 19 Nov 15:13 | 19 Nov 16:04 |
| Round 2: LM decoder | the α/β grid and selection rule (02d561f). The generated test configs were committed with their results (383e968) | 19 Nov 23:50 | 20 Nov 00:59 |
| Round 2: turbo r2 (plain) | the test configs (4a47713) | 20 Nov 02:32 | 20 Nov 02:39 |
| Round 2: r2 + chunks | the chunk grid and rule (78ed0a1). The generated test configs were committed with their results (dd312d1) | 19 Nov 23:25 | 20 Nov 03:55 |

**Two rounds.** Round 1 is the primary comparison: all baselines and both fine-tunes. No Georgian test result had
been seen when its configs and rules were fixed. The Kaldi decode settings were selected on dev after the neural
test results existed, but they use no test data. Round 2 is a follow-up: the beam-search + word-LM decoder, the r2
retrain and chunked decoding. Their *ideas* came from the round-1 error analysis, which was done on test outputs
(ea2f5c5). Their settings were then selected on dev only, by rules committed before the dev runs. **Round-2 test
numbers come from a reused test set and are reported as follow-up findings, not as confirmatory results.** Their dev
results agree with them: the beam + LM decoder gives −11.1 WER points on CV dev and chunking gives 0.0.

## 2. Metrics and why (HF audio course, chapter 5 "Evaluation")

Source: <https://huggingface.co/learn/audio-course/en/chapter5/evaluation> (as required by announcement A3).

- **WER, primary.** Word error rate = (S + D + I) / N over words, with counts pooled over the whole test set
  (corpus WER, not a mean of per-clip rates). The course recommends WER as the default ASR metric. It can exceed
  100 % when a model inserts many words, which is visible here for looping Whisper models.
- **CER, always next to WER.** Character error rate is the same formula over characters, spaces included. The
  course recommends it where word boundaries are less informative and as a softer measure of near-miss spellings.
  Georgian is agglutinative: one wrong letter in a suffix makes a whole word wrong. The CER/WER pair separates
  "almost right" systems (low CER, high WER) from systems that make whole-word errors. This matters in our results
  (§5).
- **Normalized vs orthographic.** Following the course ("train on orthographic text and evaluate on normalized
  text"), the primary numbers use one declared policy for every system: NFC, casefold, punctuation → space
  (`configs/scoring.yaml`). Every run also reports orthographic WER/CER (case and punctuation kept). One CV test
  reference is unusable: clip `common_voice_ka_38257760` reads `???????? ???????? ????? ?????? ??????.` in the CV
  release (its Georgian letters were lost in encoding), so it is empty after normalization. Its audio is speech, not
  silence. It is excluded from WER/CER for every system alike, and its per-system output length is listed in each
  run's `scores.json`.
  Word accuracy (1 − WER) is not reported; the course notes it is rarely quoted.
- **RTFx** = audio duration / processing time (higher is faster), the course's speed measure next to WER. For the
  neural systems the timer covers model forward + decoding after the audio is loaded, CUDA-synchronized, after a
  warm-up pass. For the LM rows it includes the CPU beam search. The Kaldi timer is different: it covers MFCC/CMVN
  extraction and lattice decoding on 8 CPU jobs and stops before the final one-best extraction
  (`recipes/kaldi-gmm-ka/run.sh`). Speeds in the results tables were measured on whatever hardware each run used.
  The same-GPU comparison is in §4.
- **Uncertainty.** We report 95 % cluster-bootstrap intervals (2000 resamples) that resample speakers (CV) or
  sentences (FLEURS), plus paired bootstrap differences between systems on identical clip IDs.

## 3. Systems

**Baselines** (announcement A3: every listed family that supports Georgian, at pinned revisions):

| Family | Checkpoint (revision) | Decoding | Documented training data that overlaps our test corpora |
|---|---|---|---|
| Attention enc-dec | `openai/whisper-small` (973afd2), `whisper-large-v3` (06f233f), `whisper-large-v3-turbo` (41f01f3) | greedy, language hint "georgian" | not disclosed (model card: "1 million hours of weakly labeled audio" + pseudo-labels); unknown |
| wav2vec 2.0 + CTC | `xsway/wav2vec2-large-xlsr-georgian` (b29b819) | greedy CTC | CV ka **train + validation**, version not stated (model card) |
| wav2vec 2.0 + CTC | `facebook/mms-1b-all` + `kat` adapter (3d33597) | greedy CTC | FLEURS (Hub card); the MMS paper (Pratap et al., JMLR 2024) also lists Common Voice for the 1162-language model; splits and versions not stated |
| Transducer | `nvidia/stt_ka_fastconformer_hybrid_large_pc` (bdfd787) | NeMo, RNN-T head | CV **17.0** train + dev + other, FLEURS train + dev; FLEURS test held out (model card) |
| MFCC + GMM-HMM | Kaldi tri3b, **trained by us from scratch** (`recipes/kaldi-gmm-ka/`) | lattice, word trigram LM; per-speaker CMVN + two-pass fMLLR (see below) | CV 27.0 ka train only (audio and LM text) |

**The GMM-HMM uses test-time speaker grouping; the neural systems do not.** Following the standard Kaldi SAT
recipe, tri3b pools each test speaker's utterances (CV `client_id`) for CMVN statistics and unsupervised two-pass
fMLLR adaptation. That is side information no neural system receives: they decode every clip independently. Its
strength varies by set. CV test averages 13.5 utterances per speaker and CV dev 64.3. FLEURS has no speaker IDs,
so there the adaptation runs per utterance. The speaker-independent tri2b (per-speaker CMVN only) is 4.6 points
worse on CV dev (24.88 vs 20.29 %), which shows roughly how much the adaptation is worth. Every comparison with
the GMM-HMM should be read with this in mind. It favours the GMM-HMM, so it does not weaken any conclusion that
a neural system beats it.

"Overlap" means the same *corpus*. Common Voice versions reshuffle clips between releases, so a model trained on an
older CV train/dev split may have heard clips that are in CV 27.0 test. Model cards do not list clip IDs, so exact
clip overlap cannot be joined. `scripts/cv_contamination.py` tests it indirectly, by WER per clip-ID age (§5.5).
Every system is worse on the newest clips, which seem harder: MMS, the GMM-HMM and our turbo FT by about 1.5–3×.
NVIDIA is worse by up to 13× (1.8 → 23.0 %), the pattern expected from training-set overlap. The round-3 speed
slice (the 500 oldest CV dev clips) exposed a second case. xsway scores **9.35 %** on those clips against
45.89 % on the rest of dev, consistent with its fine-tuning on an old CV train + *validation* split whose clips
now sit in CV 27.0 dev. On the 500 oldest *test* clips it shows no such gap (47.15 vs 46.23 %), so its test
rows stand. Its dev rows are contaminated, but no choice was made from them. No other system shows a gap on the
oldest 500 clips of either split (all within ±2.4 points). Every fine-tune of ours inherits its base model's
exposure.

Not run because their model cards do not list Georgian: `nvidia/canary-1b-v2`, `nvidia/parakeet-tdt-0.6b-v3`,
`Qwen/Qwen3-ASR-1.7B` / `0.6B` (links in `README.md`). No HuBERT + CTC checkpoint for Georgian was found.

**Ours** (the contribution, A1), trained on the CV ka train split only, with checkpoints selected on dev:

1. **Whisper-large-v3-turbo, full fine-tune** (809 M parameters, 6000 steps × 16, ≈ 1 epoch, A100, 2.2 h).
2. **MMS-1b-all, `kat` adapter fine-tune.** Only the 2.3 M adapter and head parameters are trained (3000 steps,
   A100, 1.3 h). The first run diverged (inf CTC loss → NaN), and `ctc_zero_infinity` fixed it.
3. **MMS fine-tune + our word 3-gram LM** (decoder row). This is the same model decoded by beam search (pyctcdecode +
   KenLM, beam 100) with the trigram we built for the GMM-HMM (Kneser-Ney, CV train transcripts only). LM weight
   α = 0.5 and insertion bonus β = 0 were selected on dev from a 12-point grid by a pre-committed rule. The same
   pair is applied to MMS zero-shot as an ablation.
4. **Whisper-turbo retrain r2 + chunked decoding** (decoder row; §5.1): training finished at step 6000,
   with 17.32 % WER on the 300-clip CV dev selection subset (225-token training evaluation cap).
   The pre-committed candidates were 8, 11 and 14 seconds. The rule selected **14 seconds** by lowest mean
   CV/FLEURS dev WER, breaking ties toward longer chunks.
   Plain and chunked r2 results use the same weights, isolating the decoding change from the retrain.
   Selection was restricted to those chunk candidates; plain decoding was better on dev.
   The splitter cuts at the quietest point in the last 40 % of each window, with no overlap, and joins the pieces with a space.
   That deviates from the course's long-audio advice (S70/L39: overlapping chunks and a frozen merge policy).
   §5.1 shows that this choice, not chunking as such, caused the failure. Only 1 CV dev and 7 CV test clips exceed
   14 s, so on CV "chunking gives 0.0" mostly means it was hardly used.

   | Decoder | CV dev WER (%) | FLEURS dev WER (%) |
   |---|---|---|
   | Plain r2 | 11.92 | 24.86 |
   | 8 s chunks | 34.09 | 55.78 |
   | 11 s chunks | 12.82 | 40.08 |
   | 14 s chunks (selected) | 11.92 | 27.87 |

## 4. Results (test, frozen, run once)

From `docs/results-georgian.md` (generated by `scripts/results_table.py ka`; dev numbers and every paired
comparison are there). WER / CER in %, 95 % CI on WER.

| Group | System | CV ka WER | CV ka CER | FLEURS ka WER | FLEURS ka CER |
|---|---|---|---|---|---|
| baseline | Whisper-small | 825.33 | 320.04 | 284.13 | 139.27 |
| baseline | Whisper-large-v3 | 72.04 | 16.64 | 69.12 | 19.79 |
| baseline | Whisper-large-v3-turbo | 142.14 | 185.45 | 126.84 | 108.54 |
| baseline | XLS-R-300M Georgian (xsway) | 46.26 | 9.02 | 52.49 | 11.83 |
| baseline | MMS-1b-all + kat | 24.14 (23.2–25.2) | 4.45 | 25.32 (24.2–26.5) | **4.76** |
| baseline | NVIDIA FastConformer ka (CV contaminated) | *4.85* | *1.27* | **15.49** (14.3–16.8) | 5.32 |
| baseline | MFCC + GMM-HMM tri3b (trained by us) | 22.64 (21.6–23.8) | 8.22 | 39.64 | 14.95 |
| ours (round 1) | MMS-1b-all kat adapter FT | 22.00 (21.2–23.0) | 3.63 | 26.02 | 5.65 |
| ours (round 1) | Whisper-large-v3-turbo full FT | **12.80** (12.0–13.7) | **2.60** | 27.47 | 12.15 |
| *round 2, follow-up on a reused test set:* | | | | | |
| ours + decoder | MMS kat adapter FT + beam 100 + our 3-gram LM | **11.07** (10.5–11.7) | **2.13** | 19.28 (18.1–20.5) | 4.64 |
| baseline + our decoder | MMS kat zero-shot + beam 100 + our 3-gram LM (ablation) | 13.50 (12.7–14.4) | 3.08 | **18.36** (17.3–19.5) | **3.81** |
| ours | Whisper-large-v3-turbo full FT, retrain r2 (same recipe) | 12.71 (11.9–13.6) | 2.59 | 27.33 (25.5–29.3) | 12.17 |
| ours + decoder | r2 + 14 s chunks (selected on dev) | 12.84 (12.0–13.7) | 2.70 | 30.00 (27.8–32.3) | 13.95 |

Bold = best value in its column within its block (round 1 and round 2 are bolded separately). NVIDIA's CV row is in
italics because it is contaminated and excluded from every comparison.

**Speed on one GPU (round 3, pre-registered).** Every system was run on the same RTX 4070 SUPER (WSL), on the
same 500 CV dev clips (48.8 min of audio, the first 500 by clip ID), with batch 8 and each system's frozen
precision and decoder. The timer covers forward + decoding after a warm-up pass, CUDA-synchronized, and for LM rows
it includes the CPU beam search (12 workers). Runs: `runs/speed4070_*`.

| System | RTFx (higher = faster) | Precision |
|---|---|---|
| XLS-R-300M xsway (CTC, greedy) | 788 | fp16 |
| MMS-1b-all + kat (CTC, greedy) | 382 | fp16 |
| MMS adapter FT (ours, greedy) | 357 | fp16 |
| MMS zero-shot + beam 100 + LM | 341 | fp16 + CPU search |
| MMS adapter FT + beam 100 + LM (ours) | 340 | fp16 + CPU search |
| NVIDIA FastConformer (transducer) | 253 | fp32 |
| Whisper-large-v3-turbo FT r2 (ours) | 40 | fp16 |
| … + 14 s chunks (no clip > 14 s in this slice, so no chunking happened) | 39 | fp16 |
| Whisper-large-v3-turbo zero-shot | 23 | fp16 |
| Whisper-small zero-shot | 14 | fp16 |
| Whisper-large-v3 zero-shot | 12 | fp16 |
| Kaldi GMM-HMM tri3b (CPU, 8 jobs; different timing boundary, §2) | 33 on CV test | CPU |

The CTC systems are an order of magnitude faster than Whisper. The beam + LM search costs MMS only 5–11 % of
its speed. Zero-shot Whisper-small and -turbo are slower than larger fine-tuned models because they loop and
generate up to the token limit. Speed here is throughput (RTFx), not streaming latency.

Key paired differences on test. One convention throughout: **Δ = WER(reference system) − WER(our system)**, in
percentage points, with a 95 % paired cluster-bootstrap CI. **Positive means ours has fewer errors.**

*Primary (round 1, blind test):*
- **CV ka**:
  - Turbo FT vs its own pretrained checkpoint: Δ +129.35 (126.21–132.60), from 142.14 % to 12.80 %.
  - Turbo FT vs the best non-contaminated pretrained baseline (MMS zero-shot): **Δ +11.34 (10.91–11.75)**, from
    24.14 % to 12.80 %.
  - Turbo FT vs our Kaldi GMM-HMM: Δ +9.85 (9.28–10.45).
  - MMS adapter FT vs MMS zero-shot: Δ +2.13 (1.89–2.35).
- **FLEURS ka** (out of domain for our CV training):
  - Turbo FT vs MMS zero-shot: Δ −2.15 (−3.92 to −0.45). Our fine-tune is worse here (§5.2).
  - Turbo FT vs NVIDIA: Δ −11.99. NVIDIA has the best FLEURS WER.
  - MMS adapter FT vs MMS zero-shot: Δ −0.69 (−1.23 to −0.15).

*Follow-up (round 2, reused test set):*
- **CV ka**:
  - MMS FT + beam + LM vs MMS zero-shot (greedy): Δ +13.07 (12.58–13.59), from 24.14 % to 11.07 %.
  - MMS FT + beam + LM vs MMS FT (greedy): Δ +10.94 (10.48–11.41). This is the gain from the *decoder change*
    (beam search + word LM + unpadded frames), not from the LM alone (§5.4).
  - MMS FT + beam + LM vs MMS zero-shot + beam + LM: Δ +2.44 (2.16–2.74). This is the fine-tune's share when both
    systems use the same decoder.
  - MMS FT + beam + LM vs turbo FT: Δ +1.73 (1.33–2.12).
  - Chunked r2 vs plain r2: Δ −0.13 (−0.24 to −0.04), so chunking slightly worsens WER.
- **FLEURS ka**:
  - MMS FT + beam + LM vs MMS zero-shot (greedy): Δ +6.05 (5.16–6.98).
  - MMS FT + beam + LM vs NVIDIA: Δ −3.79 (−4.57 to −2.96), so NVIDIA keeps the best FLEURS WER. On CER ours is
    lower: 4.64 vs 5.32 %, Δ +0.67 (0.33–1.05).
  - Chunked r2 vs plain r2: Δ −2.67 (−4.96 to −0.38).
  - Plain r2 vs the original turbo FT: Δ +0.15 (−0.26 to 0.55). This is two training runs with the same recipe and
    seed (§6).

## 5. Error analysis (summary of `docs/error-analysis-georgian.md`)

1. **Whisper's token budget truncates Georgian.**
   - Whisper's byte-level BPE has almost no Georgian merges: a word costs ~20.6 tokens and a second of speech ~30.
   - The decoder's 448-token window therefore holds only ~14.5 s of Georgian.
   - No CV test reference exceeds the token budget, but 22 % of FLEURS test references do.
   - Our turbo FT deletes 3 % of words on clips under 15 s and 50 % on clips of 25 s or more. Part of the latter
     comes from the long-form bug (item 8), which hit exactly the 32 longest FLEURS clips.
   - On FLEURS clips of up to 20 words, our turbo FT beats MMS in every length bucket (21–22 % vs 25–29 %).
   - The frozen r2 chunking study reduced FLEURS word deletions from 1,384 to 489, but insertions rose from
     188 to 1,441. WER worsened from 27.33 to 30.00 % and CER from 12.17 to 13.95 %.
   - **Why chunking failed** (FLEURS test, plain r2 → r2 + 14 s chunks, by clip duration):

     | Duration | Clips | WER (%) | Insertions | Clips with a repetition loop |
     |---|---|---|---|---|
     | < 14 s (not split) | 782 | 22.8 → 22.8 | 138 → 138 | 0 → 0 |
     | 14–15 s | 53 | 25.9 → **98.3** | 9 → 888 | 0 → **41** |
     | 15–16 s | 50 | 32.3 → 42.3 | 13 → 232 | 0 → 7 |
     | 16–20 s | 72 | 40.4 → **25.7** | 24 → 122 | 0 → 0 |
     | 20–25 s | 15 | 53.5 → **27.9** | 4 → 40 | 0 → 1 |
     | ≥ 25 s | 7 | 60.8 → **28.7** | 0 → 21 | 0 → 0 |

     A clip just over 14 s is cut somewhere in 8.4–14 s. When the quietest point falls late, which the loops in
     the 14–15 s row suggest, the second piece is a short tail of at most a few seconds, often mostly silence.
     Whisper fills such a tail with a repetition loop. The 49 looping clips
     hold 1,049 of the 1,441 insertions (73 %). On CV test, 6 of the 7 clips over 14 s loop the same way, which
     accounts for the whole 12.71 → 12.84 % change. On clips over 16 s, chunking *halved* WER. The truncation
     diagnosis was right. The splitter was wrong: no minimum piece length and no overlap, against S70/L39. A
     balanced splitter (`split_balanced`: equal pieces, no short tail) is now in the harness, but it was not
     evaluated as a chunking decoder, because that would be a third use of this test set. (Plain r2's long-clip
     rows here also include the long-form bug, item 8.)
2. **Digits.** CV ka train has no digits (0 of 99,768 transcripts), while 20 % of FLEURS references have them.
   Our fine-tunes learned the CV convention and spell numbers out. Turbo FT: 39 % WER on clips with digits vs 24 % on
   the rest. The primary policy does not verbalize numbers (it was declared before any run), so this counts as error.
   The same effect explains most of why MMS zero-shot + LM beats MMS FT + LM on FLEURS (18.36 vs 19.28 %). The
   197 clips with digits hold 121 of the 158 extra errors (77 %). On the 782 clips without digits the fine-tune is
   still slightly worse (17.17 vs 16.89 %), so digits are the main cause but not the only one.
3. **Hallucination loops.**
   - Whisper-small loops on 44 % of CV clips, and those loops produce 99 % of its insertions.
   - Turbo zero-shot loops on 6 % of CV clips and writes some outputs in Latin transliteration.
   - Both stay above 100 % WER even without the loops: their "support" for Georgian is not usable.
   - Fine-tuning removes the loops (11 of 14,258 clips).
4. **The decoder matters most, and why.** "LM" below means the round-2 decoder change as a whole: greedy → beam 100,
   plus the word trigram, decoding unpadded frames. §5.8 splits that gain into its parts on dev.
   - About half of the CTC models' substitutions are one character away from the reference word.
   - Beam search with a word LM trained only on CV train text fixes most of these: −10.6 points for MMS zero-shot
     and −10.9 for our MMS FT on CV test.
   - The closed-vocabulary GMM-HMM shows the other side. On clips without OOV words it reaches 14.5 % WER, but it
     cannot output the 6–15 % of OOV tokens. Only 24 % of its substitutions are near misses; its CER is twice
     MMS's.
5. **Contamination.** NVIDIA's WER is 1.8–4.2 % on older CV clip IDs and 23 % on the newest. Other systems degrade
   only 1.5–3× on the newest IDs. NVIDIA trained on CV 17.0 train/dev/other, so its CV row most likely reflects
   overlap with its training clips. We cannot prove which clips it saw, because the card lists no clip IDs. Its CV
   row is therefore excluded from every comparison, and only its FLEURS row (FLEURS test held out per its card) is
   used.
6. **Speakers.**
   - 139 training speakers generalize to 1,058 unseen test speakers. Per-speaker WER of turbo FT: median 9.3 %,
     90th percentile 23.7 %.
   - Teens are the hardest age group for every system.
   - Gender differences are small (≤ 2.4 points).
7. **Remaining errors of our models** are mostly single-letter slips in suffixes, spelling variants (წმიდა/წმინდა)
   and some inconsistencies in the references themselves (აბსიდის/აფსიდის both ways).
8. **A harness bug in Whisper long-form decoding (FLEURS only), found by review and fixed.** If any clip in a
   batch exceeded 30 s, the whole batch was decoded with timestamped long-form generation. Clips are sorted
   longest-first, so FLEURS's one clip over 30 s (dev 32.2 s, test 33.2 s) dragged the 32 longest FLEURS clips into
   that mode in every Whisper run. Pretrained Whisper knows timestamps and partly *escaped* its token limit there.
   On the same clips, our fine-tunes (trained without timestamps) skipped middle sentences and spliced the ends.
   Common Voice is unaffected, because no CV clip exceeds 15 s. The fix decodes only clips over 30 s specially, by
   balanced splitting without timestamps, identically for every Whisper system. The four affected systems were
   re-run once on FLEURS dev and test (round 3 §4); the corrected rows are in §4.
9. **Orthographic scoring reverses the top two.** With case and punctuation kept, Whisper-turbo FT scores
   15.83 % WER on CV test (r2) and MMS FT + beam + LM 30.45 %. The CTC vocabulary and the normalized LM text cannot
   produce punctuation, while Whisper learned it from the orthographic CV transcripts. Our normalized headline
   measures the words. Which system is "best" depends on whether the application needs punctuated text, and for
   that Whisper-turbo FT is clearly better. Full table: `docs/results-georgian.md`.

## 6. Limitations

- **CV vs FLEURS.** CV ka is read speech from a narrow text domain with few training speakers per hour. FLEURS is
  the only out-of-domain set, and it is small (979 clips).
- **Digits.** No number verbalization was applied to either side. A secondary policy that verbalizes numbers would
  measure how much of the FLEURS gap is formatting.
- **Lost weights.** The original turbo FT weights (r1) were not kept (Colab), hence the r2 retrain. Our MMS FT was
  rebuilt exactly from its backed-up adapter: 405/409 hypotheses are identical, and the rest differ through fp16 on a
  different GPU. The r2 final checkpoint and tokenizer are backed up locally under `checkpoints/` (gitignored);
  the model SHA256 matches the Colab source (`runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/checkpoint_backup.json`).
- **Training variance.** All the CIs above cover test-set sampling for fixed checkpoints, not training variance.
  Turbo r1 and r2 are two training runs with the same recipe and seed. Their CV test WERs differ by 0.08 points;
  the CI (−0.06 to 0.24) is only the test-sampling uncertainty of that difference. Two runs cannot estimate
  training variance. For our best system (MMS adapter FT, ± decoder), seeds 7 and 13 were therefore trained as
  well (round 3, §4).
- **Speed in the results tables is not comparable across rows.** RTFx there was measured on whatever hardware each
  run used (A100, L4, RTX 4070 SUPER, CPU). The same-GPU benchmark in §4 is the comparable one. Its 500-clip CV dev
  slice contains no clip over 14 s, so it times the chunked r2 decoder without any chunking.
- **LM rows** use only CV train text (no external text), so they show what the training data alone can give. A
  larger Georgian text corpus would likely help further, but it would need deduplication against dev/test.
- **Chunking is a negative result of this splitter, not of chunking.** The dev grid selected the best chunk
  candidate, not an improvement over plain decoding. §5.1 shows that the loss comes from short tail pieces, while
  chunking helped clips over 16 s.
- **Code provenance of the test runs.** The 20 frozen test runs executed on Colab record `git_commit: null`,
  because the VM had a copy of the code, not a git checkout. The 6 run locally record `git_dirty: true`, because
  generated configs were not yet committed. Each run directory saves its exact config, and the code paths they use
  were not changed in between, except for the two bugs this report discloses. Round-3 runs record their exact
  commit. `git_dirty` used to be true whenever an uncommitted run directory existed, which is always the case
  during a run. It now counts only modified tracked files.
- **Whisper training set: 99,767, not 99,768 clips.** Whisper's 448-token target cap dropped one CV train clip.
  Until round 3 the harness wrote `train_ids.txt` before that filter and did not log the dropped ID. Fixed: the
  file now lists exactly the clips trained on, and the manifest names the dropped ones.

## 7. Reproducing

`README.md` describes the setup: uv environment, data import with sha256 checks, and `asrbench run/score`. The
GMM-HMM is in `recipes/kaldi-gmm-ka/` (WSL + conda Kaldi). LM decoding needs Linux (`uv sync --extra lm`, KenLM).
The LM decoder verifies the ARPA file's sha256 at load, and the MMS adapter is loaded at the pinned revision.

There are two levels of reproduction:
- **From the repository alone:** every WER/CER, CI and paired comparison. `asrbench score` and `compare` need only
  the committed `runs/*/predictions.jsonl` and `configs/scoring.yaml`. `scripts/results_table.py ka` regenerates
  the tables.
- **With the datasets imported:** the split audit, `scripts/error_analysis_ka.py` (speaker metadata, durations,
  OOV) and `scripts/cv_contamination.py`. These need the CV 27.0 and FLEURS manifests, whose sha256 values are in
  `docs/data-notes-cv-ka.md`.

## Appendix: Kazakh pilot

Before switching to Georgian (another group registered Kazakh first), the same pipeline was run on Kazakh (KSC2 +
FLEURS kk; `docs/results-kazakh.md`). It is a pipeline pilot, not our language. Turbo FT on a 34 h KSC2 sample
reached 18.1 % KSC2 test WER vs 36.4 % for the best baseline.
