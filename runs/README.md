# runs/

Committed evaluation deliverables and training manifests. Every evaluation directory contains `manifest.json` (model, pinned revision, dataset SHA256, settings, hardware), `predictions.jsonl` (raw unnormalized hypotheses paired with item IDs and references), `scores.json`, `item_scores.jsonl`, and `report.md`. Every table in `docs/results-georgian.md` and `docs/report.md` is regenerated directly from these directories via `uv run python scripts/results_table.py ka`.

## Directory naming guide

| Prefix / Pattern | Scope | Description |
|---|---|---|
| `whisper-*_cv-ka_*`, `whisper-*_fleurs-ka_*` | Georgian baselines (Round 1) | Zero-shot `openai/whisper-small`, `large-v3`, `large-v3-turbo` on CV & FLEURS dev/test |
| `xlsr-georgian-xsway_*`, `mms-1b-all-kat_*`, `nvidia-stt-ka-fastconformer_*` | Georgian baselines (Round 1) | Zero-shot wav2vec 2.0 CTC (`xsway`, `MMS kat`) and NeMo FastConformer transducer |
| `kaldi-gmm-hmm-tri2b_*`, `kaldi-gmm-hmm-tri3b_*` | Georgian classical baseline | MFCC+GMM-HMM (`LDA+MLLT` and `LDA+MLLT+SAT`) trained from scratch on CPU (`recipes/kaldi-gmm-ka/`) |
| `mms-1b-all-kat-adapter-ft_cv-ka_*`, `whisper-large-v3-turbo-ft_cv-ka_*` | Georgian ours (Round 1, blind test) | Our MMS `kat` adapter FT (2.3 M params) and Whisper-turbo full FT (809 M params) |
| `*+lm-a*-b*_*_dev_*` | Georgian Round 2 dev grid | 12-point `(α, β)` dev grid for shallow-fusion KenLM selection (`scripts/lm_select.py`) |
| `mms-1b-all-kat-adapter-ft_cv-ka+lm_*`, `mms-1b-all-kat+lm_*` | Georgian Round 2 follow-up | MMS FT + our 3-gram LM (`α=0.5, β=0`) and zero-shot MMS + same LM ablation |
| `whisper-large-v3-turbo-ft-r2_cv-ka*` | Georgian Round 2 follow-up | Whisper-turbo full FT retrain (`r2`) + pause-chunking dev grid (`+chunk8/11/14`) and frozen test |
| `mms-1b-all-kat-adapter-ft_cv-ka-seed7*`, `*-seed13*` | Georgian Round 3 (pre-registered) | Multi-seed variance check (`seeds 7, 13`, greedy and `+lm`) |
| `speed4070_*` | Georgian Round 3 (pre-registered) | Same-GPU throughput benchmark on RTX 4070 SUPER (first 500 CV dev clips, batch 8) |
| `dec-*` | Georgian Round 3 (pre-registered) | Dev-only decoder ablation isolating unpadded frames, beam 100, and 3-gram LM |
| `*+lf-split_fleurs-ka_*` | Georgian Round 3 (pre-registered) | One-time FLEURS re-runs after fixing the >30 s Whisper batch long-form bug |
| `train_*` | Training manifests | Training logs, configs, hyperparameters, seeds, and exact `train_ids.txt` (no weights) |
| `*_ksc2-*`, `*_fleurs-kk_*`, `*-kaz*`, `*-aismlv*` | Kazakh pipeline pilot (archived) | Earlier pilot before switching to Georgian (`docs/results-kazakh.md`); not our graded language |

*Note:* Four early `20261117*` FLEURS dev baseline runs were superseded by the pinned `20261118*` runs (and `scripts/results_table.py` always selects the latest matching run). All 38 Georgian test runs have verified identical clip IDs and raw references (14,259 CV / 979 FLEURS).
