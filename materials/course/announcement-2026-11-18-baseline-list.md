# Course announcement (A3): the exact Project 3 baseline list

Passed on by the student on 2026-11-18, together with a screenshot of the class language register
(`images/class-language-register-2026-11-18.png`). The exact posting date is not recorded. Verbatim text below
(only the list formatting is added).

---

Dear all,

This list names the Project 3 baselines exactly, so that you know what to run before you start your own training. It follows the Week 9 slides.

**1. The baselines**

Classical
- MFCC (or log-mel) features + GMM-HMM

Neural model families
- CTC encoder
- Attention-based encoder-decoder, including hybrid CTC/attention
- Transducer (RNN-T)

Self-supervised encoders with an ASR head
- wav2vec 2.0 + CTC head, fine-tuned for your language
- HuBERT + CTC head, fine-tuned for your language
- Example of the right kind of checkpoint: jonatasgrosman/wav2vec2-large-xlsr-53-french (wav2vec 2.0, fine-tuned for French ASR)
- A bare wav2vec 2.0 or HuBERT encoder has no ASR head and cannot transcribe audio. It is not a baseline result.

Pretrained ASR checkpoints
- Whisper: a multilingual checkpoint (for example "small"), not an ".en" checkpoint
- nvidia/canary-1b-v2
- nvidia/parakeet-tdt-0.6b-v3 (v3 is multilingual; v2 is English only)
- Qwen/Qwen3-ASR-1.7B or Qwen/Qwen3-ASR-0.6B

**2. Baseline or contribution?**
- Running any model above without more training by your group is a baseline. An advanced model is still a baseline. Running Qwen3-ASR is not your model contribution.
- A checkpoint that someone else fine-tuned and published is also a baseline.
- Your own training or fine-tuning is your contribution, for example, fine-tuning Whisper or wav2vec 2.0 on your training split.
- If you implement and train a classical method yourself (for example, your own GMM-HMM or CTC model), it is still a baseline, but you get credit for that work.

**3. Which baselines you must run**
- Run every baseline above that supports your language.
- Check language support on the model card. If a model does not support your language, write that in the README and link the model card. Do not run it with the wrong language setting and report the result.

**4. How to compare**
- Use the same test clips and the same reference transcripts for every system.
- Use one text normalization policy and the same scoring for every system.
- Write the exact checkpoint name and revision for every pretrained model. "Whisper" is a model family. "openai/whisper-small" is a specific model.
- Report the baseline results and your own trained results in separate tables, or in clearly separate rows of one table.
- Justify WER, CER, and any other metric with the Hugging Face audio course, chapter 5 "Evaluation": https://huggingface.co/learn/audio-course/en/chapter5/evaluation

Good luck.

---

## Class language register (screenshot, 2026-11-18)

Transcribed from the screenshot. Languages already claimed by other groups:

| Group | Language | Dataset | Audio |
|---|---|---|---|
| DSU | Turkish | — | — |
| Team 7 | Urdu (ur) | Kathbath – Urdu subset (AI4Bharat) | ~25 h planned (≈164 h available) |
| Anonymous | Greek / Modern Greek (el) | HParl + CSS10 Greek (Kaggle v1) | ~124 h available |
| Avengers | Basque (eu) | Basque Parliament Speech Corpus 1.0 | 25.4 h used (~320 h available) |
| Group 8 | Hungarian (hu) | VoxPopuli (hu) | 18.9 h used (60 h available) |
| LucidAI | Uzbek (uz-UZ) | Uzbek Speech Corpus (USC, ISSAI) + FLEURS Uzbek | 25 h used (≈105 h available) |
| Tokens | Finnish (fi) | Common Voice 27.0 (fi) + Aalto Finnish Parliament ASR + FLEURS (fi) | 23.6 h used (≈3150 h available) |
| Ultron | Icelandic (is-IS) | Samrómur 21.05 (OpenSLR 112) | 20 h planned (≈145 h available) |
| **GYBZM** | **Kazakh ("Qazaqstan (kaz)")** | ISSAI KSC2, spontaneous subset (podcasts, radio, talk show) + KSC read test | ~32 h used (≈1,128 h available) |
| trial by ice | Dutch (NL) | — | — |

Rows with no language yet: NLPioneers, indecisive 1, Wolves, Coders, stray, AEK, Developers, indecisive 2,
trial by fire, Out of Vocabulary. Georgian does not appear in the register.
