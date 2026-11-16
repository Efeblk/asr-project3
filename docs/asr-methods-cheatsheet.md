# ASR methods and evaluation cheatsheet

This is a digest of the Week 9 decks and the Jurafsky & Martin chapters, so you don't have to re-read them.

- **S#** = study deck slide. **L#** = lecture deck slide. **JM15 p.N** = page N of `materials/textbook/jm-ch15-automatic-speech-recognition.pdf`.
- Model facts are as of the decks' **13 Nov 2026 snapshot**. Re-check each model card before you rely on one.

---

## 1. Metrics (S12–S27, L9–L13, L33–L35; JM15 §"ASR Evaluation" p.22)

### Definitions
- **C** = correct words, **S** = substitutions, **D** = deletions, **I** = insertions
- **N** = reference words = C + S + D
- **M** = predicted words = C + S + I

### Formulas
| Metric | Formula | Notes |
|---|---|---|
| WER | (S + D + I) / N | Can exceed 100%, because insertions are unbounded (S13). 1 − WER can go negative. |
| CER | Same formula over characters | Declare the unit: Unicode code points or grapheme clusters (S17). |
| MER | (S + D + I) / (C + S + D + I) | Bounded |
| WIL | 1 − (C/N)·(C/M) | Bounded, and still lexical (S26) |
| Key-term recall | Recovered reference terms / reference terms | Declare the matching policy, e.g. exact match after Unicode NFC. Example: 1/3 = 33.3% (S23). |
| RTF | Compute seconds / audio seconds | RTFx = 1/RTF. This is throughput, **not** latency (S25). |
| Streaming delays | First-partial delay and finalization delay, each measured in seconds | Report these separately from RTF |

### Aggregation
- **Corpus WER** pools counts: Σerrors / ΣN. For example (1+1)/(2+8) = 0.2.
- **Mean clip WER** gives each clip one vote: (0.5 + 0.125)/2 = 0.3125 (S18).
- **Across languages:** report each language's row. Macro-average weights languages equally; pooled WER weights by reference words (S19). Never show only a pooled number.

### Scoring policy
Fix the scoring policy **before** comparing models (S16, S17):
- normalization (case, punctuation, diacritics, Unicode NFC/NFD)
- word segmentation, e.g. Chinese and Japanese need a declared segmenter
- whether CER counts code points or graphemes

Apply the same policy to the reference and the hypothesis. Different languages aren't directly comparable.

### Uncertainty
Use a **paired bootstrap** on matched items (S24, S27). If clips share a speaker or session, resample by speaker or session. Δ = WER(A) − WER(B) for each resample.

### Error audit
Check numbers, names, negation, silence and code-switching (S22, S27).

### jiwer recipe (S20, S21)
```python
import jiwer
ref = "the cat sat on the mat"; hyp = "the cat sit on the"
out = jiwer.process_words(ref, hyp)
print(out.substitutions, out.deletions, out.insertions)   # 1 1 0
print(round(out.wer, 4), round(jiwer.cer(ref, hyp), 4))   # 0.3333 0.2273
print(jiwer.visualize_alignment(out))
```
jiwer returns ratios, so multiply by 100 to report percentages.

---

## 2. Front end and features (S28–S36, L14–L17; JM14 §"Feature Extraction" p.20–27)

- **Pipeline:** sampling → framing with overlap → window (taper) → DFT → mel filter bank → log, which gives **log-mel**. A DCT of the log-mel gives **MFCC**.
- 16 kHz is the usual speech rate. Telephone audio is 8 kHz. The Nyquist frequency is sr/2.
- The 39-dimensional MFCC is the historical choice: 13 × (static + Δ + ΔΔ). It is not universal.
- librosa recipe (S36):
  ```python
  y, sr = librosa.load("clip.wav", sr=16000, mono=True)
  m = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=400, hop_length=160, n_mels=80, center=False)
  logm = librosa.power_to_db(m); mfcc = librosa.feature.mfcc(S=logm, n_mfcc=13)
  # 16000 samples -> (80, 98) and (13, 98)
  ```
- **Never feed custom features to a pretrained checkpoint.** Always use that checkpoint's own processor (S36 notes).

---

## 3. Model families (S37–S63, L18–L30; JM15)

| Family | Idea | Key source |
|---|---|---|
| GMM-HMM | MFCC → state likelihoods → Viterbi search over states, lexicon and language model. Historical. | S37–S41, L18–L19 |
| CNN front | Learned filters slide across frames; striding downsamples | S42–S43, L20, JM15 p.4 |
| Attention encoder-decoder (Whisper) | Encoder over log-mel; decoder generates tokens autoregressively with cross-attention. Attention weights ≠ token probabilities. | S44–S46, S66–S68, L21, L37, JM15 p.8 |
| Beam search | Keeps alternatives, so a weaker first token can win overall | S46, L22 |
| Self-supervised (HuBERT / wav2vec2) | Pretrain by predicting k-means cluster IDs of masked frames, then add a head and fine-tune with CTC. **A base encoder without an ASR head cannot transcribe.** | S47–S48, S86–S88, L23, JM15 p.13 |
| CTC | Per-frame labels plus a blank. Collapse: merge repeats, **then** remove blanks. The loss sums over all valid paths. | S49–S54, L24–L25, JM15 p.17 |
| RNN-T / TDT | Joint audio-time × token lattice, suited to streaming. TDT also predicts a duration advance. | S55–S56, S73, L27, JM15 p.21 |
| Hybrid CTC + attention | L = λ·CTC + (1−λ)·attention. Tune λ on dev. | S57, L28, JM15 p.20 |
| LM rescoring | score = acoustic + w·LM. Save both the acoustic-only and the rescored outputs. | S61–S62, L30 |

---

## 4. Runnable checkpoints mentioned in the decks

All of these are **multilingual**. Verify that the exact language is supported, using the model card, before proposing it.

| Checkpoint | Coverage (as listed in the decks) | Notes | Slides |
|---|---|---|---|
| `openai-whisper` (e.g. `small`, CLI) | Multilingual | **Avoid `.en` variants.** Needs FFmpeg. | S69, L38 |
| `nvidia/canary-1b-v2` (NeMo) | 25 European languages | ASR when `source_lang == target_lang`; 16 kHz mono | S72, L41 |
| `nvidia/parakeet-tdt-0.6b-v3` (NeMo) | 25 languages + timestamps | **v3 only.** v2 is English-only. | S73, L41 |
| `Qwen/Qwen3-ASR-1.7B` / `0.6B` (`qwen-asr`) | 30 languages + 22 Chinese dialects (≠ 52 languages) | CUDA + bf16; `max_new_tokens` cap can truncate output | S74–S75, L42–L43 |
| `jonatasgrosman/wav2vec2-large-xlsr-53-french` (transformers CTC) | French | Example of a language-specific CTC fine-tune | S49 |
| `nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B` | 40 languages, offline | 34B total / ~4.3B active; vendor reference H100 80 GB. **Optional.** | S78, L46 |
| `nvidia/nemotron-3.5-asr-streaming-0.6b` | 19 ready + 13 broad-coverage + 8 adaptation-ready locales | Adaptation-ready locales (e.g. Greek) need fine-tuning first | S79, L46 |
| Hosted: `gpt-4o-transcribe` / mini, GPT-Realtime-Whisper | — | Optional. **No paid service is required.** | S81 |
| `google/medasr` (from the LinkedIn link) | **English only**, medical dictation | **Not eligible** for this project | `materials/links.md` |

### Code recipes (copy from the slides)
- **Whisper CLI** (S69):
  ```
  whisper sample.wav --model small --language Spanish --task transcribe --output_format json --output_dir transcript
  ```
- **Canary** (S72):
  ```python
  ASRModel.from_pretrained("nvidia/canary-1b-v2").transcribe(["x.wav"], source_lang="es", target_lang="es")[0].text
  ```
- **Parakeet** (S73):
  ```python
  ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v3").transcribe(["x.wav"])[0].text
  ```
- **Qwen3-ASR** (S74–S75):
  ```python
  Qwen3ASRModel.from_pretrained("Qwen/Qwen3-ASR-1.7B", dtype=torch.bfloat16, device_map="cuda:0", max_new_tokens=256)
  model.transcribe(audio="x.wav", language="Spanish")[0].text
  ```
- **wav2vec2 CTC** (S49):
  ```python
  AutoProcessor + AutoModelForCTC, librosa.load(sr=16000), logits.argmax(-1), p.batch_decode(ids)
  ```

---

## 5. Pitfalls the decks call out

- Tuning on the test set. Pick checkpoints, beam size and λ on **dev** (S60).
- Speaker or session leakage across splits. Overlapping windows split across train and test leak too (S8).
- Concatenating chunked outputs without a merge policy (S70).
- Dropping empty-reference clips. Report them as a separate silence result instead (S76).
- Crediting a normalizer change as a model improvement (S71).
- Treating RTF as streaming latency (S25).
- Choosing a metric because its number looks smaller (S26).
- Assuming the newest or largest model is best for your language and conditions (S41, S78).
- Treating a language code as proof of support. Check the model card's tier list (S72, S79).
