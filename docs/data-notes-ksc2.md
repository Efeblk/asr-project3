# KSC2 data notes (Kazakh, main language)

Source: ISSAI Kazakh Speech Corpus 2, `issai/Kazakh_Speech_Corpus_2` on Hugging Face (commit recorded in each
manifest row's `source`). Paper: Mussakhojayeva et al., Interspeech 2022,
https://www.isca-archive.org/interspeech_2022/mussakhojayeva22_interspeech.html.
Import: `uv run asrbench import-ksc2 --train-fraction 0.03` (streams the 81 GB archive once; keeps all Dev and
Test and a sha1-hashed 3 % of Train).

## Licence
CC BY 4.0, as stated by ISSAI (https://issai.nu.edu.kz/kz-speech-corpus/) and OpenSLR 102 for KSC1.
The HF card's `license: mit` front matter appears to be a metadata error; cite CC BY 4.0.

## Splits and leakage
- **KSC (crowdsourced) Dev/Test = KSC1 Dev/Test** (paper §3.2: "for the KSC source, the validation and test sets
  are the same as in [10]"). KSC1 made Dev/Test from identifiable speakers that do not overlap Train
  (KSC1 paper §3.3). So `aismlv/wav2vec2-large-xlsr-kazakh` (trained on KSC1 train) has not seen KSC2 Dev/Test
  clips. Unverified: whether a prompt *sentence* appears in both KSC1 train and test.
- **Other subcorpora are not guaranteed speaker-disjoint** (§3.2: "we tried to minimize the speaker overlap
  between different sets, this is not fully guaranteed"). The talk show and radio are single recurring shows,
  so hosts probably appear in every split. State this caveat; KSC2 has no speaker/session IDs, so bootstrap
  clusters fall back to items (CIs are therefore somewhat optimistic).
- KazakhTTS2 has Train only (5 speakers).

## Transcript conventions
Lowercase, no punctuation, numbers written out as words (e.g. "бір мың тоғыз жүз сексен жетінші").
FLEURS `kk_kz` references keep case, punctuation and digits (19 % of FLEURS kk test sentences contain digits),
so number formatting is a known source of cross-dataset error; analyse it separately.

## Language of the speech (rule 3: same-language ASR)
Parliament sessions contain talks in Kazakh **or Russian** (paper §3.1.6; footnote 7: 33 % of parliament
sentences are Russian). Code-switching rates (Table 1): parliament 2–4 %, talk show ~10 %, podcasts ~9 %,
radio ~6 %. Pure-Russian utterances are filtered out of every split before use (see the filter in the importer);
code-switched Kazakh utterances are kept and analysed as an error category.

## Reference results (paper Table 2, ESPnet Transformer + char LM trained on all of KSC2; their conventions)

| Source | WER valid | WER test |
|---|---|---|
| KSC (crowdsourced) | 8.1 | 6.3 |
| TV news | 7.6 | 7.8 |
| Talk show | 31.5 | 36.8 |
| Radio | 27.1 | 27.0 |
| Parliament | 12.3 | 12.7 |
| Podcasts | 30.4 | 29.9 |
| Overall | 15.1 | 15.6 |

Not directly comparable with our normalized WER (different normalization, ~1,200 h training, external LM).

## Parliament subcorpus (legal/legislative domain candidate)
20 plenary sessions of both chambers (Senate and Mazhilis) from the Parliament's official YouTube channel,
mostly read prepared scripts. Train 19.5 h / 9,508 utts, Dev 1.48 h / 723, Test 1.76 h / 865 (Table 1).
