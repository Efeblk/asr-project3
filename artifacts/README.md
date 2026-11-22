# artifacts/

Lightweight trained artifacts committed directly in the repository so our **best fair Georgian system** (`MMS-1b-all kat adapter FT + CV-train word 3-gram LM`, 11.07% CV test WER across 3 seeds: `11.04 ± 0.06%`) can be reconstructed and run using only this repository and the public pinned Hugging Face base model (`facebook/mms-1b-all@3d33597edbdaaba14a8e858e2c8caa76e3cec0cd`).

| Path | Size | Uncompressed SHA256 | Purpose |
|---|---:|---|---|
| `mms-kat-adapters/seed42/adapter.kat.safetensors` | 8.69 MB | `8b243d3078a8dc58...` | Trained `kat` adapter + CTC head (2.3 M params, seed 42, primary) |
| `mms-kat-adapters/seed7/adapter.kat.safetensors` | 8.69 MB | `5abbc09c948252c5...` | Trained `kat` adapter + CTC head (seed 7, Round 3 variance) |
| `mms-kat-adapters/seed13/adapter.kat.safetensors` | 8.69 MB | `24e7ec0d94bd258c...` | Trained `kat` adapter + CTC head (seed 13, Round 3 variance) |
| `lm/ka_cv_train_tg.arpa.gz` | 13.67 MB | `1eab5b3af5ece42c93c04473155613cf928d0b342e44f0e37afa64eafe953547` | Kneser-Ney word 3-gram LM trained strictly on CV 27.0 `ka` train text (91,155 words; SHA256 verified at load) |

## Reconstructing the runnable checkpoints

```bash
# 1. Decompress the CV-train 3-gram ARPA LM (verified by asrbench against its pinned SHA256)
mkdir -p lm
gzip -dc artifacts/lm/ka_cv_train_tg.arpa.gz > lm/ka_cv_train_tg.arpa

# 2. Rebuild any MMS adapter fine-tune checkpoint from the pinned public base model + committed adapter
uv run python scripts/rebuild_mms_adapter.py \
  artifacts/mms-kat-adapters/seed42/adapter.kat.safetensors \
  checkpoints/mms-1b-all-kat-adapter-ft_cv-ka_seed42/final
```

*(Full 809 M-parameter Whisper-large-v3-turbo weights exceed GitHub file limits (~1.6 GB) and are excluded; r2 backup SHA256 provenance is recorded in `runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/checkpoint_backup.json` and r1 weights were not retained from Colab, as disclosed in `docs/report.md` §6.)*
