# Georgian error analysis

Numbers come from the frozen test runs in `docs/results-georgian.md`. The supporting tables are in
[`error-analysis-georgian-data.md`](error-analysis-georgian-data.md), regenerated with
`uv run python scripts/error_analysis_ka.py`. The analysis is descriptive: nothing here was used to select a model,
decoder or normalizer for those frozen runs. The findings motivated later LM and chunking studies, with their
candidate grids and selection rules committed before running dev. Section numbers (§) refer to the data file.

## Summary

| # | Finding | Who it affects | Evidence |
|---|---|---|---|
| 1 | Whisper's tokenizer spends ~20.6 tokens per Georgian word (~1 token per UTF-8 byte). The 448-token decoder limit therefore holds only ~14.5 s of Georgian speech, so long clips are cut off. | All Whisper systems, ours included; FLEURS only | §2; token counts below |
| 2 | FLEURS writes numbers as digits; CV ka train has **no** digits, so our fine-tunes spell numbers out in words. | Ours on FLEURS | §3 |
| 3 | Zero-shot Whisper-small/turbo do not really know Georgian: they loop and hallucinate (WER > 100 % even without the loops). | Whisper baselines | §1, §4 |
| 4 | The GMM-HMM is a word-level LM system: it is best when every word is in vocabulary, and helpless otherwise. | GMM-HMM baseline | §5, §8 |
| 5 | NVIDIA's CV numbers are contaminated by its training data. | NVIDIA baseline | §7 |
| 6 | 139 training speakers generalize to 1058 unseen test speakers. Teens and over-40s are hardest for every system. | All | §6 |
| 7 | Our model's remaining errors are mostly one-letter spelling slips, some of them inconsistencies in the CV references themselves. | Ours | §8 |

## 1. The Whisper token budget truncates long Georgian clips

Whisper's byte-level BPE has almost no merges for the Georgian (Mkhedruli) script. Each letter is 3 bytes in UTF-8,
and a Georgian word costs **20.6 tokens** on average (FLEURS test; CV 21.5). Read speech runs at ~31 tokens per
second (CV ~27). The decoder emits at most 448 tokens per 30-s window, prompt included, which is about **14.5 s of
Georgian speech**. No CV ka reference exceeds the budget (CV train clips: median 5.1 s, max 15.5 s). On FLEURS,
**217 of 979 test references (22 %)** are longer than 440 tokens and cannot be transcribed in full by any Whisper
model in one window.

The deletions follow clip length exactly. For our Whisper-turbo FT on FLEURS test, the deletion rate is:

| Clip length | < 15 s | 15–20 s | 20–25 s | ≥ 25 s |
|---|---|---|---|---|
| Deletion rate | 3.4 % | 18.6 % | 40.5 % | 49.7 % |

For the 284 FLEURS clips with ≥ 21 reference words, the hypotheses have a median of 443 tokens, and 204 of them stop
within 8 tokens of the limit. The ones we inspected end mid-word.

The truncation hides how good the model is on FLEURS. On clips of up to 20 words, our turbo FT beats MMS zero-shot
in every length bucket:

| Words in reference | ≤ 8 | 9–14 | 15–20 |
|---|---|---|---|
| Our turbo FT | 22.1 % | 22.3 % | 21.0 % |
| MMS zero-shot | 29.0 % | 26.3 % | 24.9 % |

On long clips it collapses: 30.6 % WER at 21–30 words and 53.0 % at 31+ words. The zero-shot Whisper-large-v3
baseline shows the same deletion pattern (D 20.7 % at 31+ words). CTC and transducer models have no output
budget, and their deletion rate stays flat (§2).

The same budget explains why the in-training dev CER looked inflated. In-training evaluation capped generation at 225
tokens, about 7 s of Georgian speech. The final evaluation used the model's full 448.

**Follow-up (completed, negative result):** r2 was retrained because the original turbo weights were not kept.
`scripts/chunk_select.py` evaluates 8/11/14-second chunks split at low-energy points, selects the lowest mean
CV/FLEURS dev WER (ties toward longer chunks), and freezes that choice before test. Plain and chunked r2
rows use the same weights. The candidate grid and rule were committed in 78ed0a1 before the chunked dev runs;
no chunk length is selected using test results.

The selected 14-second candidate worsened FLEURS test WER from **27.33 % (plain r2) to 30.00 %**, and CER
from 12.17 to 13.95 %. Word deletions fell from 1,384 to 489, but insertions rose from 188 to 1,441
(same 17,138 reference words). Splitting addresses truncation while introducing more errors elsewhere.
CV test also worsened slightly (12.71 to 12.84 % WER). Shorter chunks were worse on dev: 8 s gave
34.09/55.78 % CV/FLEURS WER, 11 s gave 12.82/40.08 %, and 14 s gave 11.92/27.87 %; plain r2 gave
11.92/24.86 %. This implementation is not an effective fix. The study is closed with no further tuning.

## 2. Digits: a mismatch between the training and test text conventions

Of the 99,768 CV ka train transcripts, **0** contain a digit: Common Voice prompts spell numbers out. In FLEURS ka
test, 197 of 979 references (20 %) contain digits ("1940", "800"). The scoring policy was declared before any run
and does not verbalize numbers, so "800" only matches "800".

Our fine-tunes learned the CV convention:
- **Turbo FT** never outputs a digit. Its WER is 39.4 % on clips with digits and 24.0 % on the rest.
- **MMS FT** outputs digits in 29 % of those clips, down from 94 % for MMS zero-shot. Fine-tuning on CV taught it to
  stop writing digits.

MMS zero-shot handles digits well (28.7 % vs 24.3 %). MMS-1b-all's training data includes FLEURS (model card),
which also explains MMS's strong FLEURS numbers in general. On references without digits, our turbo FT and MMS
zero-shot are level (24.0 % vs 24.3 %), despite the truncation in §1.

**Fix (not applied):** a secondary scoring policy that verbalizes Georgian numbers on both sides would measure the
formatting share of the gap without touching the primary metric. Mixing digit-bearing text into fine-tuning would fix
the behavior itself.

## 3. Zero-shot Whisper-small and turbo hallucinate Georgian

A "loop" here is an n-gram repeated 4+ times in a row:
- **Whisper-small** loops on 44 % of CV clips, and those loops produce 99 % of its insertions.
- **Whisper-turbo** loops on 5.9 % of CV clips (81 % of its insertions) and 19 % of FLEURS clips. On FLEURS it also
  deletes 71 % of reference words; its outputs average 0.55 of the reference length. A loop spends the token budget
  of §1 on repeats, and 38 of 979 FLEURS outputs (4 %) are romanized Georgian ("Qundalini yogisiz…") instead of
  Georgian script.
- **Even without the loop clips**, both stay above 100 % WER (108 % on CV). They hallucinate rather than transcribe,
  which is why they are the extreme rows of the table.
- **Whisper-large-v3** rarely loops (0.6 %), but 72 % WER makes it unusable.
- **After fine-tuning** (our turbo FT), loops all but vanish: 11 CV clips and none on FLEURS.

These loops are the clearest case of the gap between Whisper's nominal Georgian support and its usable quality.

## 4. Closed vocabulary vs open vocabulary (GMM-HMM, LM effect)

Georgian is agglutinative. Against the 91k word types of CV train, 6.0 % of CV test tokens and 14.7 % of FLEURS test
tokens are out of vocabulary (OOV). The GMM-HMM has a closed graphemic lexicon, so its OOV recall is 0 by
construction, and its WER doubles on clips with an OOV word:

| GMM-HMM WER | Clips without OOV | Clips with OOV |
|---|---|---|
| CV test | 14.5 % | 36.5 % |
| FLEURS test | 19.9 % | 41.7 % |

On clips without OOV words, its trigram LM makes it better than MMS zero-shot (14.5 % vs 22.9 % on CV). The neural
models recover most OOV words: our turbo FT gets 72 % of OOV tokens right, MMS 63 %, NVIDIA 75 %.

The error types differ as well:
- **GMM-HMM:** only 24 % of its substituted words are within one character edit of the reference. The rest are
  whole-word LM swaps: "და" → "სადა", "იგი" → "დიდი", "ეს" → "ის".
- **Neural models:** 50–54 % of their substitutions are within one character edit.

This is why the GMM-HMM beats MMS on CV WER but has nearly twice its CER (8.2 % vs 4.5 %, `results-georgian.md`).
It also points to the missing piece of the CTC baselines: MMS decodes greedily without any LM.

**Applied afterwards (decoder rows, α/β selected on dev by `scripts/lm_select.py`):** we decoded MMS with the same
CV-train trigram (beam search, pyctcdecode + KenLM). On CV test, MMS zero-shot drops from 24.14 to 13.50 % WER, and
our MMS fine-tune drops from 22.00 to **11.07 %** (2.13 % CER), the best fair CV result. On FLEURS test the scores
are 18.36 % and 19.28 %. There the fine-tune is slightly worse than zero-shot because of the digit convention (§2).

## 5. NVIDIA FastConformer: contamination, not skill, on CV

NVIDIA's model card lists Common Voice 17.0 train/dev/other as training data. CV 27.0 ka dev/test contain clips that
were already in CV 17.0. Grouping our dev+test clips by clip ID (newer clips have larger IDs):
- **NVIDIA:** 1.8–4.2 % WER on older clips, rising to 23 % on the newest IDs (≥ 44 M).
- **MMS, the GMM-HMM and our turbo FT:** they also degrade on the newest bucket, which seems somewhat harder, but
  only about 1.5–3×. NVIDIA degrades by up to 13× (1.77 → 22.98 %).

Its 4.85 % CV test WER therefore reflects memorized training clips. FLEURS ka test, held out from its training,
gives 15.49 %. That is still the best FLEURS result in the table, but it is the only fair comparison.

## 6. Speakers

CV ka train has only 139 speakers, while test has 1058 different ones. Per-speaker WER of our turbo FT (676 speakers
with ≥ 50 words): median 9.3 %, 90th percentile 23.7 %. For MMS zero-shot: median 21.1 %, 90th percentile 38.9 %.

The self-reported demographics (often blank) show:
- **Gender:** small differences for every non-contaminated system (≤ 2.4 points).
- **Age:** teens are the hardest group for every system (ours 20.0 % vs 12.8 % overall; MMS 33.0 %), followed by
  speakers in their forties and fifties. The age groups are unevenly represented, and train-side demographics are
  mostly blank, so we report this without a causal claim.

## 7. What our model still gets wrong (CV test)

Our turbo FT substitutes 12,024 words, and 54 % of them are a single character away from the reference:
- **Spelling variants:** "წმიდა" / "წმინდა" (both spellings of "holy" are in use), "ჯეიმს" / "ჯეიმზ" ("James").
- **Reference inconsistency:** "აბსიდის" → "აფსიდის" 6× and "აფსიდის" → "აბსიდის" 5×. The CV references themselves
  spell this word ("apse") both ways, so some of these errors are not errors.
- **Morphology:** "რომლებიც" → "რომელიც" (plural → singular relative pronoun), "თავისი" → "თავის", "ცენტრალური" →
  "ცენტრალურ" (case endings that are barely audible).
- **Compounds:** "შავიზღვისპირა" → "ზღვისპირა" (part of a compound dropped).

The 2.6 % CER against 12.8 % WER shows the same pattern: most word errors are one or two letters wrong. In an
agglutinative language, a single letter in a suffix makes the whole word wrong.

## Implications for the comparison

- **On CV ka,** the later MMS FT + our CV-train trigram LM row is the best fair system (11.07 % WER),
  ahead of turbo FT (12.80 %). Turbo FT alone improves over MMS zero-shot by 11.3 points (CI 10.9–11.8).
- **On FLEURS ka,** our greedy fine-tunes trail NVIDIA and roughly match MMS. Two major causes are:
  Whisper's token budget for Georgian (§1) and the digit convention (§2). The later MMS FT + LM row reaches
  19.28 % WER, still behind NVIDIA's 15.49 %, with lower CER (4.64 vs 5.32 %). The completed chunking study
  worsened WER and CER; it does not change the main system ranking.
- **For the classical baseline,** the GMM-HMM shows how much a word-level n-gram LM is worth on CV's narrow-domain
  read speech. The original neural CTC rows use no LM; the later matched MMS rows with the same CV-train LM
  separate the benefit of train-text decoding from adapter fine-tuning (`docs/results-georgian.md`).
