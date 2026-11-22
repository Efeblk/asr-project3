# data/

This directory holds the **cleaned dataset manifests** and cleaning log for our Georgian (`ka`) corpora.

## What is committed vs excluded

- **Committed (`data/manifests/`):**
  - `cv_ka_manifest.jsonl.gz` — complete cleaned Common Voice Scripted Speech 27.0 `ka` manifest (128,243 clips across official speaker-disjoint train/dev/test splits: item ID, relative audio path, human reference transcript, hashed speaker ID, duration, demographics). Uncompressed SHA256: `8119119998bbec10ce2a37cc96829a9228187cd0fb08456716982a6e9c509b0c`.
  - `fleurs_ka_ge_manifest.jsonl.gz` — complete cleaned FLEURS `ka_ge` manifest (train/dev/test, pinned Hugging Face revision `70bb2e84b976`). Uncompressed SHA256: `d95e58e9db459736af88f3ff659dd44a58789e6d04173ef618298ce4b8127aed`.
- **Committed (`data/CLEANING.md`):** exact log of every corrupted, filtered, or dropped utterance across training, decoding, and scoring.
- **Not committed (raw audio):** Raw Common Voice 27.0 `ka` audio is **10.4 GB** (exceeding GitHub repository/file size limits, and Mozilla Data Collective terms prohibit redistributing the raw archive). Raw FLEURS audio is downloaded deterministically from the pinned Hugging Face revision.

## Regenerating raw audio + local manifests

```bash
# 1. Common Voice 27.0 ka (after downloading the official CC0 archive from Mozilla Data Collective;
#    archive SHA256 and exact steps in docs/data-notes-cv-ka.md)
uv run asrbench import-cv data/cv/raw/.../cv-corpus-27.0-2026-09-11/ka --out data/cv/ka/manifest.jsonl

# 2. FLEURS ka_ge (pinned dataset revision)
uv run asrbench import-fleurs ka_ge --splits dev test --out data/fleurs/ka_ge/manifest.jsonl

# 3. Verify split integrity (speaker separation, duplicate IDs, missing audio)
uv run asrbench validate data/cv/ka/manifest.jsonl
uv run asrbench validate data/fleurs/ka_ge/manifest.jsonl
```

Every run manifest under `runs/*/manifest.json` records the dataset manifest SHA256 so regenerated manifests can be verified byte-for-byte against the committed `data/manifests/*.jsonl.gz`.
