# Language shortlist (research snapshot, 2026-11-17)

This is a neutral list of candidates. **Cross out any language that is ineligible for you** (rule 2 in AGENTS.md: no mother tongue, never recorded here), and check the class register for languages other groups have already claimed (A1). Every number has a source URL. Anything not checked against a primary source is marked **unverified**.

Constraints assumed: one MAIN language (zero-shot baselines plus our own fine-tune of Whisper-small and/or XLS-R-300M / MMS CTC on one RTX 4070 SUPER 12 GB), and 1–3 EXTRA languages (baselines only, maybe a second fine-tune).

## Decision (2026-11-17)

- **Main: Kazakh (kk).** Baselines + our own fine-tune. Training data: a fixed 3 % sample of KSC2 Train (≈35 h, sha1-hashed utterance IDs) plus FLEURS `kk_kz`. Test sets: KSC2 Test (in-domain, numbers written as words) and FLEURS `kk_kz` test (read Wikipedia, with digits and punctuation).
- **Extra: Georgian (ka).** Baselines on FLEURS `ka_ge`; optional second fine-tune on FLEURS train (≈5 h) or Common Voice via MDC.
- Eligibility confirmed by the student (reasons not recorded). Neither language is in the class register yet (claimed so far: Turkish, Basque, Hungarian, Uzbek, Icelandic).

## Summary table

"Trusted train h" counts human-transcribed training audio we can actually obtain. FLEURS is about 10 h per language everywhere ([card](https://huggingface.co/datasets/google/fleurs)), so it is left out of that column. CV = Common Voice v27 **validated** hours. W-s = Whisper-small FLEURS WER from the Whisper paper, Table 13 ([arXiv 2212.04356](https://arxiv.org/abs/2212.04356)).

| Language | Code / FLEURS cfg | Trusted train h (beyond FLEURS) | Test source | Baselines that explicitly support it | Resource tier | Verdict |
|---|---|---|---|---|---|---|
| Kazakh | kk / `kk_kz` | KSC2 ≈1,200 h; CV 3 h | FLEURS test (856) | Whisper (W-s 70.3), MMS `kaz`, omniASR, XLS-R FT | low–mid | **MAIN #1** |
| Amharic | am / `am_et` | ALFFA ≈20 h; WAXAL 38k utts (h unverified); CV 2 h | FLEURS test (516) | Whisper (W-s 120.2), MMS `amh`, omniASR, XLS-R FT | low | **MAIN #2** |
| Georgian | ka / `ka_ge` | CV 262 h | FLEURS test (979) | Whisper (W-s 118.3), MMS `kat`, omniASR, XLS-R FT | low–mid | **MAIN #3** |
| Nepali | ne / `ne_np` | OpenSLR-54 ≈144 h | FLEURS test (726) | Whisper (W-s 69.5), MMS `npi`, omniASR, XLS-R FT | low | MAIN alt / EXTRA |
| Luganda | lg / `lg_ug` | CV 437 h; WAXAL 5.5k utts | FLEURS test (723) | MMS `lug`, omniASR, Sunbird Whisper FTs. **No base Whisper** | low | EXTRA (strong bonus) |
| Maltese | mt / `mt_mt` | CV 9 h; MASRI ≈19 h+ (on request) | FLEURS test (926) | Whisper (W-s 110.1), **Canary-1b-v2**, **Parakeet-v3**, MMS `mlt`, omniASR | low | **EXTRA #1** |
| Vietnamese (medical) | vi / `vi_vn` | VietMed 5 h train / 5 dev / 6 test (medical) | VietMed test + FLEURS | Whisper (W-s 21.2), **Qwen3-ASR**, MMS `vie`, omniASR, wav2vec2 FT | mid (domain) | **EXTRA #2 (domain bonus)** |
| Welsh | cy / `cy_gb` | CV 124 h; BTB (CC0, gated-auto) | FLEURS test (1021) | Whisper (W-s 59.3), MMS `cym`, omniASR, XLS-R FT | low–mid | EXTRA |
| isiZulu | zu / `zu_za` | NCHLT ≈56 h | FLEURS test (854) | MMS `zul`, omniASR, w2v-BERT FT. **No Whisper** | low | EXTRA |
| Swahili | sw / `sw_ke` | CV 392 h; ALFFA ≈10 h | FLEURS test (487) | Whisper (W-s 73.7), MMS `swh`, omniASR, XLS-R FT | low–mid | EXTRA (claim risk) |
| Yoruba | yo / `yo_ng` | CV 6 h; OpenSLR-86 (h unverified) | FLEURS test (831) | Whisper (W-s 116.4), MMS `yor`, omniASR, Yoruba-ASR FT | low | risky (diacritics, little data) |
| Mongolian | mn / `mn_mn` | CV 46 h | FLEURS test (949) | Whisper (W-s 144.2), MMS `mon`, omniASR, XLS-R FT | low | EXTRA |
| Belarusian | be / `be_by` | CV 1,819 h | FLEURS test (967) | Whisper (W-s 75.1), MMS `bel`, omniASR, wav2vec2 FT | mid (data-rich) | EXTRA |
| Latvian | lv / `lv_lv` | CV 267 h | FLEURS test (851) | Whisper (W-s 53.2), **Canary** (9.66), **Parakeet** (22.84), MMS `lav`, omniASR | mid | EXTRA (hard to beat Canary) |

## Shared facts (apply to every row)

**FLEURS.**
- About 10–12 h of read Wikipedia sentences per language. CC-BY-4.0, ungated, and the harness already has `import-fleurs`.
- The splits are sentence-disjoint (1509/150/350 sentences). The paper says speakers are disjoint "between train/dev and test", while the HF card says train speakers differ from dev/test speakers. Either way, **test is speaker-disjoint from train** ([paper](https://arxiv.org/abs/2205.12446), [card](https://huggingface.co/datasets/google/fleurs)).
- Clip counts in this file come from the HF datasets-server, e.g. [`/info?dataset=google/fleurs&config=kk_kz`](https://datasets-server.huggingface.co/info?dataset=google/fleurs&config=kk_kz).
- **Dev sets are small (200–450 clips)**, so bootstrap CIs on dev will be wide.

**Common Voice in 2026.**
- Latest release is **v27.0 (cut-off 2026-09-11)**. Per-locale stats are in [cv-corpus-27.0-2026-09-11.json](https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json), and the release table is in the [cv-dataset README](https://github.com/common-voice/cv-dataset).
- Since **October 2025, CV is distributed only via Mozilla Data Collective (MDC)**, not the HF hub. The HF `mozilla-foundation/common_voice_17_0` card now points to MDC ([HF card](https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0)). Whether the old HF files still download is unverified, and they are frozen at ≤17.0 anyway.
- **Scriptable, after one manual step:**
  1. Create an MDC account.
  2. Accept each locale's terms **in the browser**. API-only acceptance is not supported.
  3. Create an API key.
  4. Run `pip install datacollective` (v0.7.1) and set `MDC_API_KEY`.

  Sources: [PyPI](https://pypi.org/project/datacollective/), [API docs](https://datacollective.mozillafoundation.org/api-reference). Licence CC0.
- **Splits:** the official splits keep each speaker in one split ([Mozilla forum](https://discourse.mozilla.org/t/speaker-id-split-between-train-test-dev/34289/3)). Verify this after download by checking `client_id` overlap.
- **Caveat:** the official `train.tsv` is much smaller than `validated` (e.g. Welsh: 124 validated h but only 8,044 train clips) because it keeps roughly one clip per sentence. To use all validated hours, rebuild train as validated minus the dev/test speakers and sentences.

**Baseline checks (done on 2026-11-17).**
- **Whisper:** language list in [`tokenizer.py`](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py). **lg, zu and xh are absent.**
- **Whisper WER:** FLEURS WER for small and large-v2 is from Table 13 of [the paper](https://arxiv.org/abs/2212.04356). It uses Whisper's own text normalizer, so the numbers aren't directly comparable to our scoring.
- **Whisper large-v3:** per-language FLEURS WER exists only as a chart image in the Whisper README (**unverified** numbers).
- **MMS-1b-all:** I HEAD-checked each adapter file `adapter.<iso3>.safetensors` on [facebook/mms-1b-all](https://huggingface.co/facebook/mms-1b-all). Present: swh, yor, hau, amh, lug, zul, xho, cym, mlt, kat, kaz, mon, npi, est, lav, vie, tur, bel, hun, lit, plus `uzb-script_latin`.
- **Canary-1b-v2 and Parakeet-tdt-0.6b-v3:** both list the same 25 European languages, which include **mt, lv, lt, et, hu** ([canary](https://huggingface.co/nvidia/canary-1b-v2), [parakeet](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)). Neither covers any African or Central Asian candidate.
- **Qwen3-ASR:** 30 languages ([card](https://huggingface.co/Qwen/Qwen3-ASR-1.7B)). Of our candidates, **only vi** (also tr, hu, el, fa, mk, ro, cs, fi, pl, …).
- **Meta Omnilingual ASR (omniASR, Nov 2025, Apache-2.0):** not in the course's list, but it is a pretrained ASR checkpoint that explicitly covers 1,600+ languages, so it is a valid extra baseline. The per-language training hours and 7B-LLM CER are in [this CSV](https://github.com/facebookresearch/omnilingual-asr/blob/main/per_language_results_table_7B_llm_asr.csv). Inference takes clips under 40 s only (FLEURS is fine). **The harness has no omniASR wrapper yet** (needs `omnilingual_asr`/fairseq2).
- **Contamination:** MMS-1b-all and omniASR were trained on public corpora that likely include FLEURS/CV *train*. Their use of *test* splits is unverified, so always evaluate on FLEURS **test**.

**12 GB feasibility (general).**
- Whisper-small (244 M) full fine-tune: bf16, batch about 8–16, gradient checkpointing.
- XLS-R-300M CTC fine-tune.
- MMS-1b-all adapter-only training (about 2 M trainable parameters).

All three fit in 12 GB. 10–50 h of training audio trains within a few hours. Hundreds of hours are a bonus, but subsample to fit the time budget.

**Script tip.** Whisper's byte-level BPE tokenises non-Latin scripts (Ge'ez, Georgian, Devanagari) into many tokens per word. Training and decoding are slower and the 448-token limit binds sooner. CTC on characters avoids this.

---

## Candidates

### 1. Kazakh (kk, `kk_kz`)
- **FLEURS:** 3,200 / 369 / 856 clips ([ds-server](https://datasets-server.huggingface.co/info?dataset=google/fleurs&config=kk_kz)).
- **Training data:**
  - **KSC2:** ≈1.2k h, 600k+ utterances, human-transcribed ([ISSAI](https://issai.nu.edu.kz/kz-speech-corpus/), [Interspeech 2022](https://www.isca-archive.org/interspeech_2022/mussakhojayeva22_interspeech.html)).
  - **KSC2 access:** on HF, **ungated**, as `issai/Kazakh_Speech_Corpus_2` ([HF](https://huggingface.co/datasets/issai/Kazakh_Speech_Corpus_2)). It is **81 GB in ten split tar.gz parts**.
  - **KSC2 licence:** CC BY 4.0 per ISSAI. The HF tag says MIT, a mismatch; cite CC BY 4.0.
  - **KSC1:** the older ≈330 h set on [OpenSLR 102](https://openslr.org/102/) is a smaller download.
  - **CV v27:** 3 h validated.
  - KSC2 test/dev speaker-disjointness: **unverified**.
- **Models:**
  - Whisper: kk supported. FLEURS WER small 70.3, large-v2 37.7.
  - MMS: `kaz` adapter.
  - omniASR: 407 training h, CER 2.6.
  - Fine-tune: [aismlv/wav2vec2-large-xlsr-kazakh](https://huggingface.co/aismlv/wav2vec2-large-xlsr-kazakh).
  - Canary, Parakeet, Qwen3-ASR: not supported.
- **Tier:** low–mid. CV is tiny and the language is commonly called low-resource, but KSC2 is large, so the bonus case is "low-resource language with enough data". That is exactly A1's condition, though not the most extreme case.
- **Expected gain:** a bad Whisper-small baseline (≈70 % WER), so a big visible fine-tuning gain is likely.
- **Risks:**
  - Kazakh–Russian code-switching in KSC2. Filter or report it.
  - Cyrillic (with Kazakh letters ә ғ қ ң ө ұ ү һ і) needs a case/punctuation policy only.
  - The 81 GB download (KSC1 is the fallback).

### 2. Amharic (am, `am_et`)
- **FLEURS:** 3,163 / 223 / 516 clips ([ds-server](https://datasets-server.huggingface.co/info?dataset=google/fleurs&config=am_et)).
- **Training data:**
  - **ALFFA:** ≈20 h train and ≈2 h test read speech, Kaldi format, MIT ([README](https://github.com/besacier/ALFFA_PUBLIC/tree/master/ASR/AMHARIC), [OpenSLR 25](https://www.openslr.org/25)).
  - **WAXAL `amh_asr`:** 38,022 / 2,912 / 3,420 train/val/test utterances of transcribed natural (image-prompted) speech, with a `speaker_id` field. CC-BY-4.0, ungated ([HF](https://huggingface.co/datasets/google/WaxalNLP), [ds-server](https://datasets-server.huggingface.co/info?dataset=google/WaxalNLP&config=amh_asr), [blog](https://research.google/blog/waxal-a-large-scale-open-resource-for-african-language-speech-technology/)). WAXAL Amharic **hours and split speaker-disjointness are unverified**.
  - **CV v27:** 2 h.
- **Models:**
  - Whisper: am listed. FLEURS WER small 120.2, large-v2 140.3, so it is effectively non-functional.
  - MMS: `amh` adapter.
  - omniASR: 188 training h, CER 5.7.
  - Fine-tune: [agkphysics/wav2vec2-large-xlsr-53-amharic](https://huggingface.co/agkphysics/wav2vec2-large-xlsr-53-amharic).
  - Canary, Parakeet, Qwen3-ASR: not supported.
- **Tier:** low. This is a clean bonus case: tens of hours of trusted data, three independent corpora, and failing general-purpose baselines.
- **Risks:**
  - Ge'ez syllabary: normalise the homophone letters (e.g. ሀ/ሐ/ኀ, ሰ/ሠ, አ/ዐ, ጸ/ፀ) **identically on reference and hypothesis**. Declare this in `scoring.yaml`; it is an ablation.
  - Word separators (፡ vs space) and Ethiopic punctuation (።, ፣).
  - CER should be the headline metric next to WER.
  - Whisper's tokeniser is inefficient on Ge'ez, so prefer the CTC fine-tune as the main contribution.

### 3. Georgian (ka, `ka_ge`)
- **FLEURS:** 1,491 / 409 / 979 clips. The train set is unusually small ([ds-server](https://datasets-server.huggingface.co/info?dataset=google/fleurs&config=ka_ge)).
- **Training data:** CV v27 has **262 h validated**, 3,149 speakers, and official train/dev/test of 99,768 / 14,216 / 14,259 clips ([stats](https://github.com/common-voice/cv-dataset/blob/main/datasets/scripted-speech/cv-corpus-27.0-2026-09-11.json)). Access is via MDC, CC0.
- **Models:**
  - Whisper: ka supported. FLEURS WER small 118.3, large-v2 105.0.
  - MMS: `kat` adapter.
  - omniASR: 327 training h, CER 1.9.
  - Fine-tune: [xsway/wav2vec2-large-xlsr-georgian](https://huggingface.co/xsway/wav2vec2-large-xlsr-georgian).
  - Canary, Parakeet, Qwen3-ASR: not supported.
- **Tier:** low–mid. Whisper fails, but CV data is plentiful.
- **Expected gain:** the largest of any candidate (118 → likely <30).
- **Risks:**
  - The Mkhedruli script has **no case and no diacritics**, which makes normalisation simple (a plus).
  - Only CV is available for training, which is read speech with short prompts. Test on FLEURS to measure the domain shift.
  - The 4-step MDC access process.

### 4. Nepali (ne, `ne_np`)
- **FLEURS:** 3,332 / 305 / 726 clips.
- **Training data:**
  - **OpenSLR 54:** ≈157k utterances from 527 speakers, CC BY-SA 4.0 ([OpenSLR](https://openslr.org/54/)).
  - **Usable hours:** about 143.6 h after removing numeric-only transcripts ([arXiv 2406.17825](https://arxiv.org/abs/2406.17825)).
  - **Splits:** OpenSLR 54 has no official split, so build a speaker-disjoint split from its speaker IDs.
  - **CV v27:** 1 h.
- **Models:**
  - Whisper: ne supported. FLEURS WER small 69.5, large-v2 47.1.
  - MMS: `npi` adapter.
  - omniASR: only 24.5 training h, CER 12.3.
  - Fine-tune: [gagan3012/wav2vec2-xlsr-nepali](https://huggingface.co/gagan3012/wav2vec2-xlsr-nepali).
- **Tier:** low. A good bonus case.
- **Risks:**
  - Devanagari normalisation (nukta, ZWJ/ZWNJ, chandrabindu vs anusvara variants).
  - Transcript quality issues in OpenSLR 54 (cited as needing filtering).
  - Byte-heavy tokens in Whisper.

### 5. Luganda (lg, `lg_ug`)
- **FLEURS:** 2,478 / 306 / 723 clips.
- **Training data:**
  - **CV v27:** **437 h validated**, 672 speakers.
  - **WAXAL `lug_asr`:** 5,455 / 664 / 638 utterances, CC-BY-4.0 ([ds-server](https://datasets-server.huggingface.co/info?dataset=google/WaxalNLP&config=lug_asr)).
  - **Makerere radio:** 20 h ([HF](https://huggingface.co/datasets/allandclive/MakerereRadioSpeech_20Hrs)).
  - **Sunbird SALT:** gated ([HF](https://huggingface.co/datasets/Sunbird/salt)).
- **Models:**
  - **Whisper does not list Luganda.** Base Whisper is therefore not a valid baseline (rule 6). Fine-tuning Whisper-small on it is still a legitimate contribution.
  - MMS: `lug` adapter.
  - omniASR: 178 training h, CER 4.2.
  - Community Whisper fine-tunes that explicitly target Luganda: [Sunbird/asr-whisper-large-v3-salt](https://huggingface.co/Sunbird/asr-whisper-large-v3-salt).
- **Tier:** low. Strong bonus with plenty of data.
- **Risks:**
  - Fewer baselines.
  - Orthography variants (double vowels/consonants) cause many near-miss word errors, so CER is important.

### 6. Maltese (mt, `mt_mt`)
- **FLEURS:** 2,895 / 404 / 926 clips.
- **Training data:**
  - **CV v27:** 9 h.
  - **MASRI** (Univ. of Malta): the full release requires accepting the terms and getting a download link, **non-commercial** ([MASRI](https://www.um.edu.mt/projects/masri/), [paper](https://arxiv.org/abs/2008.05760)). The HEADSET v2 / Farfield / Booths subsets are 6h39 / 9h37 / 2h27 ([model card](https://huggingface.co/carlosdanielhernandezmena/whisper-large-maltese-8k-steps-64h)). A "≈64 h" MASRI pool is referenced but **unverified**.
  - **MASRI-Synthetic** (99 h) is TTS output. **Not trusted as training references** for our purposes.
- **Models:**
  - Whisper: mt supported. FLEURS WER small 110.1, large-v2 115.7.
  - **Canary-1b-v2:** FLEURS WER 18.31.
  - **Parakeet-v3:** FLEURS WER 20.46 (both from the model-card metadata).
  - MMS: `mlt` adapter.
  - omniASR: 156.5 training h.
  - Fine-tune: [carlosdanielhernandezmena/wav2vec2-large-xlsr-53-maltese-64h](https://huggingface.co/carlosdanielhernandezmena/wav2vec2-large-xlsr-53-maltese-64h).
- **Tier:** low. This gives the **richest baseline comparison** of any low-resource candidate: Whisper fails while NVIDIA models are decent.
- **Risks:**
  - Training data without MASRI is only about 20 h.
  - Diacritics ċ ġ ħ ż and apostrophe/hyphen clitics (*il-*, *t'*) need a clear word-segmentation policy.
  - English code-switching in real speech.

### 7. Vietnamese, medical domain (vi, `vi_vn` + VietMed)
- **FLEURS:** 2,994 / 361 / 857 clips.
- **VietMed:** 16 h labelled real medical conversations, split 5 h train / 5 h dev / 6 h test, plus unlabelled audio ([paper](https://arxiv.org/abs/2404.05659), [HF](https://huggingface.co/datasets/leduckhai/VietMed)).
  - HF is ungated, but the licence is ambiguous: the HF tag says MIT and the paper says CC BY-NC 4.0, so use it for research only.
  - Speaker-disjointness of the splits: **unverified**.
- **CV v27:** 8 h.
- **Models:**
  - Whisper: vi supported. FLEURS WER small 21.2, large-v2 10.3.
  - **Qwen3-ASR-1.7B:** vi supported.
  - MMS: `vie` adapter.
  - omniASR: 1,025 training h.
  - Fine-tune: [nguyenvulebinh/wav2vec2-base-vi-vlsp2020](https://huggingface.co/nguyenvulebinh/wav2vec2-base-vi-vlsp2020).
- **Tier:** mid-resource language. The **domain bonus** comes from medical speech: a general model will miss terminology, and fine-tuning on VietMed train should show a gain.
- **Risks:**
  - Tonal diacritics are essential. Never strip them, and use NFC normalisation.
  - Syllable-based spacing makes WER close to a syllable error rate.
  - VietMed train is only 5 h.
  - Medical English loanwords.
- This is the only domain-specific non-English set found that is downloadable and human-transcribed. The related ViMedCSS ([alphaxiv](https://www.alphaxiv.org/abs/2602.12911)) is code-switched, which risks English content.

### 8. Welsh (cy, `cy_gb`)
- **FLEURS:** 3,427 / 447 / 1,021 clips.
- **Training data:**
  - **CV v27:** 124 h validated, but only 8,044 official train clips (see the caveat above).
  - **Banc Trawsgrifiadau Bangor:** spontaneous speech, verbatim transcripts, CC0, HF gated-auto ([HF](https://huggingface.co/datasets/techiaith/banc-trawsgrifiadau-bangor)). Hours: **unverified** (a 2023 paper said about 20 h, [SIGUL](https://sigul-2023.ilc.cnr.it/wp-content/uploads/2023/08/11_Paper.pdf)). It contains some English (filter it).
- **Models:**
  - Whisper: cy supported. FLEURS WER small 59.3, large-v2 33.0.
  - MMS: `cym` adapter.
  - omniASR: 101.7 training h.
  - Fine-tunes: [infinitejoy/wav2vec2-large-xls-r-300m-welsh](https://huggingface.co/infinitejoy/wav2vec2-large-xls-r-300m-welsh) and the strong [techiaith/whisper-large-v3-ft-btb-cv-cy](https://huggingface.co/techiaith/whisper-large-v3-ft-btb-cv-cy).
- **Tier:** low–mid.
- **Risks:**
  - Code-switching with English in BTB is a rule-1 hazard.
  - Mutations and the circumflex/diaeresis (ŵ ŷ ï) need a policy.

### 9. isiZulu (zu, `zu_za`)
- **FLEURS:** 2,858 / 354 / 854 clips.
- **Training data:**
  - **NCHLT isiZulu:** ≈56 h of 3–5-word read prompts from 210 speakers, with a test suite of 8 speakers. 4.36 GB on SADiLaR ([repo](https://hdl.handle.net/20.500.12185/275)). Licence CC BY 3.0 per a secondary source; **verify on download**.
  - **CV:** ≈0 h.
- **Models:**
  - **Whisper does not list Zulu.**
  - MMS: `zul` adapter.
  - omniASR: 633.7 training h, but CER 17.9.
  - Fine-tunes: [badrex/w2v-bert-2.0-zulu-asr](https://huggingface.co/badrex/w2v-bert-2.0-zulu-asr), [TheirStory/whisper-medium-zulu](https://huggingface.co/TheirStory/whisper-medium-zulu).
- **Tier:** low. A strong bonus case.
- **Risks:**
  - Agglutinative conjunctive orthography means very long words, so WER is harsh and CER is important.
  - Domain mismatch between short NCHLT prompts and FLEURS sentences.
  - isiXhosa (`xh_za`, MMS `xho`, NCHLT) is a near-identical alternative.

### 10. Swahili (sw, `sw_ke`)
- **FLEURS:** 3,070 / 211 / 487 clips. The dev set is small.
- **Training data:**
  - **CV v27:** 392 h validated.
  - **ALFFA:** ≈10 h train / 1.8 h test broadcast news, MIT ([README](https://github.com/besacier/ALFFA_PUBLIC/tree/master/ASR/SWAHILI)).
- **Models:**
  - Whisper: sw supported. FLEURS WER small 73.7, large-v2 39.3.
  - MMS: `swh` adapter.
  - omniASR: 461.8 training h.
  - Fine-tune: [eddiegulay/wav2vec2-large-xlsr-mvc-swahili](https://huggingface.co/eddiegulay/wav2vec2-large-xlsr-mvc-swahili).
- **Tier:** low–mid. Technically excellent: Latin script, no diacritics, lots of data.
- **Risks:**
  - **Claim risk:** it is the most obvious African pick, and it is already the harness's pipeline test language.
  - Variety: FLEURS is Kenyan (`sw_ke`), while CV and ALFFA are mixed or Tanzanian.

### 11. Yoruba (yo, `yo_ng`)
- **FLEURS:** 2,339 / 378 / 831 clips.
- **Training data:**
  - **CV v27:** 6 h.
  - **OpenSLR 86:** Google crowdsourced, CC BY-SA 4.0, hours **unverified** ([OpenSLR](https://openslr.org/86/)).
  - **NaijaVoices:** 1,838 h across ig/ha/yo, CC BY-NC-SA. Yoruba share and access process are **unverified** ([arXiv](https://arxiv.org/abs/2505.20564)).
  - **ÌròyìnSpeech:** ≈42 h ([arXiv](https://arxiv.org/abs/2307.16071)), licence **unverified**.
  - WAXAL has Yoruba **TTS only**, no ASR config.
- **Models:**
  - Whisper: yo supported. FLEURS WER small 116.4, large-v2 94.8.
  - MMS: `yor` adapter.
  - omniASR: 828 training h, CER 9.0.
  - Fine-tune: [NCAIR1/Yoruba-ASR](https://huggingface.co/NCAIR1/Yoruba-ASR).
- **Tier:** low.
- **Risks:**
  - **Tone diacritics and underdots.** References are inconsistently diacritised across corpora, so the scoring policy (keep vs strip) dominates the results.
  - Openly downloadable trusted data is thin. Hausa (`ha_ng`, W-s 90.1, MMS `hau`, CV 4 h) has the same data story.

### 12. Mongolian (mn, `mn_mn`)
- **FLEURS:** 3,074 / 405 / 949 clips.
- **Training data:** CV v27 has 46 h validated, but only 2,196 official train clips (rebuild from validated).
- **Models:**
  - Whisper: mn supported. FLEURS WER small **144.2**, large-v2 110.5.
  - MMS: `mon` adapter.
  - omniASR: 28.2 training h, CER 5.5.
  - Fine-tune: [anton-l/wav2vec2-large-xlsr-53-mongolian](https://huggingface.co/anton-l/wav2vec2-large-xlsr-53-mongolian).
- **Tier:** low.
- **Risks:**
  - Whisper hallucinates (WER >100 %), so report insertions separately.
  - Cyrillic Mongolian only; the traditional script is not involved.

### 13. Belarusian (be, `be_by`)
- **FLEURS:** 2,433 / 408 / 967 clips.
- **Training data:** CV v27 has **1,819 h validated** and 8,624 speakers, the largest of any candidate.
- **Models:**
  - Whisper: be supported. FLEURS WER small 75.1, large-v2 45.4.
  - MMS: `bel` adapter.
  - omniASR: 483 training h.
  - Fine-tune: [ales/wav2vec2-cv-be](https://huggingface.co/ales/wav2vec2-cv-be).
- **Tier:** mid by data volume. The bonus claim is weaker.
- **Risks:**
  - Russian-trained models confuse і/и and ў.
  - The CV download is huge (subsample).

### 14. Latvian (lv, `lv_lv`)
- **FLEURS:** 2,110 / 356 / 851 clips.
- **Training data:** CV v27 has 267 h validated.
- **Models:**
  - Whisper: lv supported. FLEURS WER small 53.2, large-v2 23.1.
  - **Canary:** 9.66.
  - **Parakeet:** 22.84.
  - MMS: `lav` adapter.
  - omniASR: 62.3 training h.
  - Fine-tune: [jimregan/wav2vec2-large-xlsr-latvian-cv](https://huggingface.co/jimregan/wav2vec2-large-xlsr-latvian-cv).
- **Tier:** mid. A fine-tuned Whisper-small will probably not beat Canary, which is fine to report but not flashy.
- **Risks:** diacritics (ā č ē ģ ī ķ ļ ņ š ū ž). Lithuanian and Estonian (Canary 12.36 / 12.55) are near-equivalent alternatives.

Also considered but not listed:
- **Kinyarwanda:** CV 2,002 h, but it is **not in FLEURS and not in Whisper**.
- **Basque:** CV 473 h, Whisper supported, not in FLEURS.
- **Hausa / Igbo:** see the Yoruba row.

---

## Ranked recommendation

**MAIN (pick one):**
1. **Kazakh.** It has the most trusted training data of any low-resource candidate (KSC2 ≈1.2k h, ungated) and a failing Whisper-small (70 % WER). Normalisation is simple, and four baselines are available. Watch the 81 GB download (KSC1 330 h is the fallback) and the Russian code-switching.
2. **Amharic.** It is the clearest low-resource bonus: three independent human-transcribed corpora (ALFFA 20 h, WAXAL, FLEURS) and Whisper failing completely (120 %). It needs a careful Ge'ez normalisation policy, and the CTC fine-tune should be the main contribution.
3. **Georgian.** It has the biggest expected visible gain (Whisper-small 118 %), 262 h of CC0 CV data, and the easiest normalisation (no case, no diacritics). Access needs one manual MDC step.
   - **Runner-up: Nepali.** OpenSLR 54 has about 144 h and Whisper-small scores 69.5 %. Its risk is noisier transcripts.

**EXTRA (baselines only, maybe a second fine-tune):**
- **Maltese.** Low-resource and the only one where Whisper, Canary-1b-v2, Parakeet-v3, MMS and omniASR all explicitly apply, which makes for a rich baseline table on one test set.
- **Vietnamese + VietMed.** It earns the domain (medical) bonus, has Qwen3-ASR as a baseline, and its 5 h train set makes a cheap second fine-tune.
- **Luganda** or **isiZulu.** Strong low-resource bonus with enough data (CV 437 h / NCHLT 56 h). There is no Whisper baseline, so use MMS and omniASR.
- **Swahili** is only a fallback if nobody else claims it.

**Avoid as MAIN:**
- **Yoruba:** diacritic inconsistency and thin open data.
- **Latvian/Belarusian:** the bonus is weak, and for Latvian, Canary is hard to beat.
- **Mongolian:** only 46 h, and the official CV train split is tiny.

**Unverified items to resolve before registering:**
- KSC2 split speakers.
- WAXAL Amharic hours and speaker-disjointness.
- VietMed licence and split speakers.
- MASRI full-release size.
- NCHLT licence text.
- Whisper large-v3 per-language WER.
