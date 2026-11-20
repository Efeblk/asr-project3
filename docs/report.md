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
FLEURS splits share no sentences. Data provenance (archive sha256, manifest sha256, import commands) is in
`docs/data-notes-cv-ka.md`.

**Protocol.** Everything is chosen on dev: checkpoints, decoder settings, LM weights and chunk length. Every test
config is frozen with `frozen: true` before its test run, and each test is run once (the harness refuses test
runs that are not frozen). Generated fine-tune and decoder configs follow the pre-committed rules. Where a choice was made on dev, the candidate grid and the selection rule were committed
before the dev runs (commits 0c0d0e4, 2dd4397, 78ed0a1, 02d561f).

## 2. Metrics and why (HF audio course, chapter 5 "Evaluation")

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
  (`configs/scoring.yaml`). Every run also reports orthographic WER/CER (case and punctuation kept). References that
  are empty after normalization (1 CV test clip) are excluded from WER and reported separately as silent clips.
  Word accuracy (1 − WER) is not reported; the course notes it is rarely quoted.
- **RTFx** = audio duration / processing time (higher is faster), the course's speed measure next to WER. The
  timing boundary is model forward + decoding. Loading is excluded, and for the GMM-HMM and LM decoders the CPU
  search is included. Hardware is listed per row.
- **Uncertainty.** We report 95 % cluster-bootstrap intervals (2000 resamples) that resample speakers (CV) or
  sentences (FLEURS), plus paired bootstrap differences between systems on identical clip IDs.

## 3. Systems

**Baselines** (announcement A3: every listed family that supports Georgian, at pinned revisions):

| Family | Checkpoint (revision) | Notes |
|---|---|---|
| Attention enc-dec | `openai/whisper-small` (973afd2), `whisper-large-v3` (06f233f), `whisper-large-v3-turbo` (41f01f3) | greedy, language hint "georgian" |
| wav2vec 2.0 + CTC | `xsway/wav2vec2-large-xlsr-georgian` (b29b819), `facebook/mms-1b-all` + `kat` adapter (3d33597) | greedy CTC |
| Transducer | `nvidia/stt_ka_fastconformer_hybrid_large_pc` (bdfd787) | NeMo, RNN-T head. Trained on CV 17.0 incl. dev, so contaminated on CV (§5.4) |
| MFCC + GMM-HMM | Kaldi tri3b, **trained by us from scratch** (`recipes/kaldi-gmm-ka/`) | graphemic lexicon, word trigram LM on CV train text, LDA+MLLT+SAT, CPU |

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
   Full plain dev/test evaluation and chunk-length selection are pending. The pre-committed candidates are
   8, 11 and 14 seconds; select the lowest mean CV/FLEURS dev WER, breaking ties toward longer chunks.
   Plain and chunked r2 results use the same weights, isolating the decoding change from the retrain.

## 4. Results (test, frozen, run once)

From `docs/results-georgian.md` (generated by `scripts/results_table.py ka`; dev numbers and every paired
comparison are there). WER / CER in %, 95 % CI on WER.

| Group | System | CV ka WER | CV ka CER | FLEURS ka WER | FLEURS ka CER |
|---|---|---|---|---|---|
| baseline | Whisper-small | 825.33 | 320.04 | 284.13 | 139.27 |
| baseline | Whisper-large-v3 | 72.04 | 16.64 | 69.12 | 19.79 |
| baseline | Whisper-large-v3-turbo | 142.14 | 185.45 | 126.84 | 108.54 |
| baseline | XLS-R-300M Georgian (xsway) | 46.26 | 9.02 | 52.49 | 11.83 |
| baseline | MMS-1b-all + kat | 24.14 (23.2–25.2) | 4.45 | 25.32 (24.2–26.5) | 4.76 |
| baseline | NVIDIA FastConformer ka (CV contaminated) | *4.85* | *1.27* | **15.49** (14.3–16.8) | 5.32 |
| baseline | MFCC + GMM-HMM tri3b (trained by us) | 22.64 (21.6–23.8) | 8.22 | 39.64 | 14.95 |
| ours | MMS-1b-all kat adapter FT | 22.00 (21.2–23.0) | 3.63 | 26.02 | 5.65 |
| ours | Whisper-large-v3-turbo full FT | 12.80 (12.0–13.7) | 2.60 | 27.47 | 12.15 |
| ours + decoder | MMS kat adapter FT + our 3-gram LM | **11.07** (10.5–11.7) | **2.13** | 19.28 (18.1–20.5) | **4.64** |
| ablation | MMS kat zero-shot + our 3-gram LM | 13.50 (12.7–14.4) | 3.08 | 18.36 (17.3–19.5) | 3.81 |

Speed (RTFx on CV test): MMS 283 (L4), turbo FT 87 (A100), MMS FT + LM 374 (RTX 4070 SUPER + 12 CPU workers),
GMM-HMM 33 (8 CPU jobs).

Key paired differences (test, Δ WER = reference − ours, 95 % CI):

- **CV ka**:
  - Our best (MMS FT + LM) vs the best clean pretrained baseline (MMS zero-shot): **−13.1 points**, from 24.14 % to 11.07 %
    (Δ 13.07).
  - Turbo FT vs MMS zero-shot: Δ 11.34 (10.91–11.75).
  - MMS FT + LM vs turbo FT: Δ 1.73 (1.33–2.12).
  - MMS FT + LM vs MMS zero-shot + LM: Δ 2.44 (2.16–2.74). That is the fine-tune's share once both use the LM.
- **FLEURS ka**:
  - MMS FT + LM vs MMS zero-shot: Δ 6.04.
  - vs NVIDIA: −3.79 (−4.57 to −2.96), so NVIDIA keeps the best FLEURS WER.
  - Our CER is lower than NVIDIA's: 4.64 vs 5.32 %, Δ 0.67 (0.33–1.05).

## 5. Error analysis (summary of `docs/error-analysis-georgian.md`)

1. **Whisper's token budget truncates Georgian.**
   - Whisper's byte-level BPE has almost no Georgian merges: a word costs ~20.6 tokens and a second of speech ~30.
   - The decoder's 448-token window therefore holds only ~14.5 s of Georgian.
   - No CV clip is that long, but 22 % of FLEURS test references are.
   - Our turbo FT deletes 3 % of words on clips under 15 s and 50 % on clips of 25 s or more.
   - On FLEURS clips of up to 20 words, our turbo FT beats MMS in every length bucket (21–22 % vs 25–29 %).
   - Chunking long clips at pauses is intended to reduce truncation; the r2 decoder evaluation is pending.
2. **Digits.** CV ka train has no digits (0 of 99,768 transcripts), while 20 % of FLEURS references have them.
   Our fine-tunes learned the CV convention and spell numbers out. Turbo FT: 39 % WER on clips with digits vs 24 % on
   the rest. The primary policy does not verbalize numbers (it was declared before any run), so this counts as error.
   The same effect is why MMS zero-shot + LM beats MMS FT + LM on FLEURS (18.36 vs 19.28 %).
3. **Hallucination loops.**
   - Whisper-small loops on 44 % of CV clips, and those loops produce 99 % of its insertions.
   - Turbo zero-shot loops on 6 % of CV clips and writes some outputs in Latin transliteration.
   - Both stay above 100 % WER even without the loops: their "support" for Georgian is not usable.
   - Fine-tuning removes the loops (11 of 14,258 clips).
4. **The LM matters most, and why.**
   - About half of the CTC models' substitutions are one character away from the reference word.
   - A word LM trained only on CV train text fixes most of these: −10.6 points for MMS zero-shot and −10.9 for our
     MMS FT on CV.
   - The closed-vocabulary GMM-HMM shows the other side. On clips without OOV words it reaches 14.5 % WER, but it
     cannot output the 6–15 % of OOV tokens. Only 24 % of its substitutions are near misses; its CER is twice
     MMS's.
5. **Contamination.** NVIDIA's WER is 1.8–4.2 % on older CV clip IDs and 23 % on the newest. Other systems degrade
   only 1.5–3× on the newest IDs. Its CV row therefore reflects training-data overlap (CV 17.0 incl. dev). Only its
   FLEURS row is a fair comparison.
6. **Speakers.**
   - 139 training speakers generalize to 1,058 unseen test speakers. Per-speaker WER of turbo FT: median 9.3 %,
     90th percentile 23.7 %.
   - Teens are the hardest age group for every system.
   - Gender differences are small (≤ 2.4 points).
7. **Remaining errors of our models** are mostly single-letter slips in suffixes, spelling variants (წმიდა/წმინდა)
   and some inconsistencies in the references themselves (აბსიდის/აფსიდის both ways).

## 6. Limitations

- **CV vs FLEURS.** CV ka is read speech from a narrow text domain with few training speakers per hour. FLEURS is
  the only out-of-domain set, and it is small (979 clips).
- **Digits.** No number verbalization was applied to either side. A secondary policy that verbalizes numbers would
  measure how much of the FLEURS gap is formatting.
- **Lost weights.** The original turbo FT weights (r1) were not kept (Colab), hence the r2 retrain. Our MMS FT was
  rebuilt exactly from its backed-up adapter: 405/409 hypotheses are identical, and the rest differ through fp16 on a
  different GPU.
- **LM rows** use only CV train text (no external text), so they show what the training data alone can give. A
  larger Georgian text corpus would likely help further, but it would need deduplication against dev/test.

## 7. Reproducing

`README.md` describes the setup: uv environment, data import with sha256 checks, and `asrbench run/score`. The
GMM-HMM is in `recipes/kaldi-gmm-ka/` (WSL + conda Kaldi). LM decoding needs Linux (KenLM). Tables come from
`scripts/results_table.py ka` and `scripts/error_analysis_ka.py`.

## Appendix: Kazakh pilot

Before switching to Georgian (another group registered Kazakh first), the same pipeline was run on Kazakh (KSC2 +
FLEURS kk; `docs/results-kazakh.md`). It is a pipeline pilot, not our language. Turbo FT on a 34 h KSC2 sample
reached 18.1 % KSC2 test WER vs 36.4 % for the best baseline.
