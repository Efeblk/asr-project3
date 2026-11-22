# Project 3 — 2-Minute Speaker Guide (5-Slide Deck)

**Deck:** `presentation/project3-presentation-short.pptx` (5 slides, benchmark-first & graph-first)
**Word count:** **212 printed words** (~240 spoken words with numbers read aloud) → **~1 min 47 sec** at a calm 135 wpm (~13 s buffer under 2:00).

---

## Full 2-Minute Script (Slide by Slide)

### Slide 1 — Cover (`0:00 – 0:05`, 12 words)
> "Georgian speech recognition — I'm İsmet Efe Balık, group stray, working solo."

### Slide 2 — `the task: Georgian ASR across four paradigms` (`0:05 – 0:27`, 49 words)
> "Georgian is low-resource: Canary, Parakeet and Qwen3-ASR don't support it.
> I benchmark all four lecture paradigms, separating architecture from checkpoints: a Kaldi GMM-HMM I trained myself, Whisper, wav2vec-2 CTC, and NVIDIA's transducer.
> My contribution is fine-tuning Whisper-turbo and a small MMS adapter, plus a 3-gram language-model decoder."

### Slide 3 — `the benchmark: baselines vs ours (frozen test)` (`0:27 – 1:01`, 60 words)
> "Here is the frozen benchmark with 95-percent intervals.
> The best pretrained CV baseline, MMS, scores 24 percent.
> Fine-tuned Whisper reaches 12.8 and wins when punctuation counts.
> In a follow-up round, MMS plus our 3-gram LM reaches 11.0 to 11.1 percent over three seeds, and runs eight-and-a-half times faster.
> On FLEURS test, NVIDIA still leads at 15.5."

### Slide 4 — `can we trust it? splits, CV17 overlap & 4 metrics` (`1:01 – 1:25`, 47 words)
> "We train on 147 hours of Common Voice with zero speaker or raw verbatim overlap.
> Left: NVIDIA jumps 13 times from 1.8 to 23 percent on the newest clips, versus 1.5 to 3 times for other models, consistent with CV17 overlap.
> Right: CER exposes Kaldi, and punctuation flips the winner."

### Slide 5 — `why models break: two mechanisms` (`1:25 – 1:47`, 44 words)
> "Two mechanisms explain the errors.
> Left: Whisper spends about 20 tokens per Georgian word, cutting off around 14.5 seconds. Pause chunking cut long-clip error 41 percent, but looped on short tails, a negative result.
> Right: dev ablation shows the LM drives almost the entire 11-point gain."

---

## Q&A Cheat Sheet

1. **"Why did you choose WER + CER + orthographic WER + RTFx?"**
   - Corpus WER `(S+D+I)/N` is the HF Audio Course ch. 5 standard and can exceed 100%, exposing Whisper loops (WAcc breaks >100%).
   - CER matters because Georgian is agglutinative — one wrong suffix letter breaks a whole word. At the same ~22% WER, Kaldi has 8.2% CER vs 3.6% for greedy MMS FT (2.3× worse).
   - Orthographic WER shows the rank reversal when punctuation matters (Whisper FT 15.9% vs MMS+LM 30.5%).
   - RTFx on one RTX 4070 SUPER (500 CV dev clips, batch 8) exposes the 8.5× throughput gap (340× vs 40× on Whisper r2).

2. **"How does your CTC + 3-gram LM decoder work, and how much came from training vs the LM?"**
   - Shallow-fusion beam search (`pyctcdecode` + KenLM, beam 100): `argmax_W [ log P_CTC(W|X) + α log P_LM(W) + β|W| ]`, using a Kneser-Ney trigram built strictly from CV train text (`α=0.5, β=0` chosen on dev).
   - On CV test, pretrained MMS + our LM gets **13.50%**, and training the `kat` adapter improves that to **11.07%** (**+2.44 pts**, CI 2.16–2.74) under the identical decoder. On dev, beam search alone moves CV WER from 21.43% to 21.26% (−0.16), while adding the LM drops it to 10.28% (−10.98).

3. **"How was your fine-tuning configured?"**
   - **Whisper-large-v3-turbo full FT:** all 809 M params trained on orthographic CV train transcripts (99,767 clips; 1 clip >448 tokens dropped), 6,000 steps × effective batch 16 (~1 epoch, A100, 2.2 h), best checkpoint selected by dev WER.
   - **MMS-1b-all `kat` adapter FT:** frozen 1 B backbone; only the 2.3 M `kat` adapter + CTC head parameters trained (3,000 steps, seeds 42/7/13, `ctc_zero_infinity=True` to prevent infinite CTC loss → NaN).

4. **"Why didn't you run HuBERT, Canary, Parakeet, or Qwen3-ASR?"**
   - Canary v2 (25 EU languages), Parakeet v3 (25 EU languages), and Qwen3-ASR (30 languages) do not list Georgian on their model cards (linked in README). No Georgian HuBERT+CTC ASR checkpoint was found on Hugging Face Hub (search link in README).

5. **"How do you know NVIDIA is contaminated on Common Voice?"**
   - Its model card lists CV 17.0 train/dev/other without clip IDs, so exact clip overlap cannot be proven. However, grouping CV 27.0 dev+test by clip-ID age shows NVIDIA jumping 13× from 1.77% (40.0–40.3M bin) to 22.98% (newest 44M+ bin), whereas MMS, Kaldi, and our Whisper FT degrade only 1.5–3× — consistent with CV 17.0 training overlap. On FLEURS test (held out per its card, though trained on FLEURS train/dev), it is clean and leads at 15.49%.

6. **"Did you peek at the test set for Round 2 (LM and chunking)?"**
   - We disclose this openly: Round 1 (Whisper FT, MMS FT) was strictly blind test. Round 2 ideas came from Round 1 error analysis, so we label them as follow-up on a reused test set — though all settings (`α=0.5, β=0`; 14 s chunks) were still selected strictly on dev with pre-committed rules.

7. **"Why did your MMS fine-tune score slightly worse than zero-shot MMS on FLEURS (19.28% vs 18.36%, both with LM)?"**
   - Digits mismatch: 0 of 99,768 CV train transcripts contain digits (numbers are spelled out), while 20% of FLEURS test references contain digits. Those 197 digit clips account for 77% of the extra errors between MMS FT+LM and MMS zero-shot+LM.

8. **"Is 11.07% just a lucky training run?"**
   - No — across 3 independent seeds (42, 7, 13), MMS FT+LM scores 11.04 ± 0.06% on CV (10.97–11.07%) and 19.17 ± 0.10% on FLEURS. Our three headline paired comparisons (CV MMS FT vs zero-shot, CV MMS FT+LM vs turbo FT, FLEURS MMS FT+LM vs NVIDIA) keep their sign with 95% CIs excluding zero for every seed. *(Greedy MMS FT vs zero-shot on FLEURS crosses 0 for seeds 7 and 13.)*

9. **"Why did pause chunking fail for Whisper?"**
   - `split_at_pauses` cut in the last 40% of each 14 s window with no minimum piece length and no overlap (deviating from S70/L39). Across all 94 FLEURS clips ≥16 s, pooled WER dropped 45.10% → 26.45% (−41% relative), but on 14–15 s clips 41 of 53 looped on short silent tails (all 49 looping clips caused 73% of insertions: 1,049 of 1,441), raising overall FLEURS WER from 27.33% to 30.00%. Balanced splitting (`split_balanced`) is now in the harness, deliberately not re-tested on test to avoid a third peek.

10. **"Why is Kaldi (22.64%) lower than pretrained MMS (24.14%) on CV?"**
    - Two advantages none of the neural baselines got: Kaldi decodes with our CV-train 3-gram LM and uses test-time per-speaker CMVN + two-pass fMLLR SAT adaptation. Even with that advantage, our two best neural systems beat it by 9.9–11.6 points, and greedy MMS FT beats it on WER while cutting CER more than in half (3.6% vs 8.2%).
