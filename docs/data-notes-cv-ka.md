# Common Voice Georgian data notes (main language)

Source: **Common Voice Scripted Speech 27.0 – Georgian** (`cv-corpus-27.0-2026-09-11/ka`), Mozilla Data Collective
dataset `cmu5x9qda00fenq07byl8rlc8` (https://mozilladatacollective.com/datasets/cmu5x9qda00fenq07byl8rlc8).
Licence CC0-1.0. Archive `common-voice-scripted-speech-27-0-georgi-6faf6605.tar.gz`, 10,435,235,149 bytes,
sha256 `8099ad5a341466ed9993fc3c5984a65cdacdfdf51407b9474c06e5c5da2f1fb6`. Download needs an MDC account that has
accepted the dataset terms, plus an API key (`MDC_API_KEY`; never commit it). Terms: do not re-host the data and do
not try to identify speakers.

Import (keeps the official split; `client_id` → `speaker`, truncated to 16 hex chars):

```bash
uv run --no-project --with datacollective python -c "from datacollective import download_dataset; \
  download_dataset('cmu5x9qda00fenq07byl8rlc8', download_directory='data/cv/raw', extract=True)"
uv run asrbench import-cv data/cv/raw/<archive dir>/cv-corpus-27.0-2026-09-11/ka --language ka --out data/cv/ka/manifest.jsonl
```

Resulting manifest sha256: `8119119998bbec10ce2a37cc96829a9228187cd0fb08456716982a6e9c509b0c`.

## Splits (official; see docs/split-audit.md)

| Split | Speakers | Utterances | Hours |
|---|---|---|---|
| train | 139 | 99,768 | 147.5 |
| dev | 221 | 14,216 | 23.2 |
| test | 1,058 | 14,259 | 23.3 |

No speaker is shared between splits. 18 test and 21 dev sentences equal a training sentence after normalization
(none as raw text). Train is concentrated on few speakers (139 speakers for 147 h), test is very speaker-diverse
(1,058), so test measures generalisation to new voices.

## Contamination of pretrained baselines
- `nvidia/stt_ka_fastconformer_hybrid_large_pc` was trained on Common Voice **17.0** train/dev/other + FLEURS
  train/dev (model card). CV 27.0 test speakers are not in CV 27.0 train, but whether some of their clips were in
  CV 17.0 train/dev/other is not verifiable from the card; report its CV result with this caveat and use FLEURS ka
  test (held out by NVIDIA) as the clean comparison.
- `facebook/mms-1b-all` lists FLEURS among its training data (see the Kazakh notes); its FLEURS numbers may be
  optimistic.
