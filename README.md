# ASR Project 3

This is a course project that evaluates automatic speech recognition on non-English languages. It contains `asrbench`, a harness that runs speech recognition models on a dataset and scores them in a reproducible way, following the course rules in [docs/project-requirements.md](docs/project-requirements.md).

## Language, data and splits

**Our language is Georgian (`ka`).** Eligibility is confirmed; it is unique in the class register (group "stray").
Kazakh was explored first and is kept only as a pipeline pilot ([docs/results-kazakh.md](docs/results-kazakh.md)),
because another group registered Kazakh.

| Dataset | Split used | Are speakers separate? |
|---|---|---|
| [Common Voice Scripted Speech 27.0 – Georgian](https://mozilladatacollective.com/datasets/cmu5x9qda00fenq07byl8rlc8) (CC0, Mozilla Data Collective) | the official train / dev / test | Yes: Common Voice assigns each speaker (`client_id`) to one split; `asrbench validate` and `scripts/split_audit.py` check it |
| [FLEURS `ka_ge`](https://huggingface.co/datasets/google/fleurs) (CC BY 4.0), pinned revision | the official train / dev / test | No speaker IDs; sentence-disjoint splits, and the authors state test speakers are not in train |

Per-split speakers, utterances, hours and test sentences that also occur in train are in
[docs/split-audit.md](docs/split-audit.md) (announcement A2). Dev is used for every choice (checkpoint, decoder,
normalizer); test is run once with frozen configs.

### Baselines that do not support Georgian (announcement A3)

These course-listed checkpoints were not run, because their model cards do not list Georgian (or Kazakh):
- [`nvidia/canary-1b-v2`](https://huggingface.co/nvidia/canary-1b-v2): 25 European languages.
- [`nvidia/parakeet-tdt-0.6b-v3`](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3): the same 25 European languages.
- [`Qwen/Qwen3-ASR-1.7B`](https://huggingface.co/Qwen/Qwen3-ASR-1.7B) / [`Qwen/Qwen3-ASR-0.6B`](https://huggingface.co/Qwen/Qwen3-ASR-0.6B): 30 languages + 22 Chinese dialects.

Georgian baselines that are run, per family: Whisper (`openai/whisper-small`, `-large-v3`, `-large-v3-turbo`;
attention encoder-decoder), wav2vec 2.0 + CTC (`xsway/wav2vec2-large-xlsr-georgian`, `facebook/mms-1b-all` with
the `kat` adapter), transducer (`nvidia/stt_ka_fastconformer_hybrid_large_pc`, FastConformer hybrid
Transducer-CTC) and an MFCC + GMM-HMM that we train from scratch with the standard Kaldi recipe on CPU
([`recipes/kaldi-gmm-ka/`](recipes/kaldi-gmm-ka/README.md): graphemic lexicon, trigram LM on CV train text, LDA+MLLT+SAT
triphones; reported as a baseline row). No HuBERT + CTC checkpoint for Georgian was found.

Exact checkpoints and revisions (also in every run manifest):

| Checkpoint | Revision |
|---|---|
| `openai/whisper-small` | `973afd24965f72e36ca33b3055d56a652f456b4d` |
| `openai/whisper-large-v3` | `06f233fe06e710322aca913c1bc4249a0d71fce1` |
| `openai/whisper-large-v3-turbo` | `41f01f3fe87f28c78e2fbf8b568835947dd65ed9` |
| `xsway/wav2vec2-large-xlsr-georgian` | `b29b81945f5fa2e35fbb05da5256815d8cc71e20` |
| `facebook/mms-1b-all` (adapter `kat`) | `3d33597edbdaaba14a8e858e2c8caa76e3cec0cd` |
| `nvidia/stt_ka_fastconformer_hybrid_large_pc` | `bdfd7871e0574001e650e741d6201d40205db6bb` |

## Setup

You need [uv](https://docs.astral.sh/uv/) and `ffmpeg` on your PATH.

```bash
uv sync --extra hf --group dev        # Whisper + wav2vec2/CTC (CUDA torch on Windows/Linux); add `--extra lm` on Linux/WSL for LM decoding
uv run pytest                         # 34 tests: metrics, pipeline, CPU training, importers, language filter, pause splitting
```

Extras for other model families. Each goes in its own environment:
- `uv sync --extra nemo`: NVIDIA FastConformer (verified on Georgian), Canary v2 and Parakeet v3. Linux or WSL recommended.
- `uv sync --extra qwen`: Qwen3-ASR (not run here). Needs a bf16 CUDA GPU.

## Workflow

```bash
# 1. Build a dataset manifest from a source with trusted references
uv run asrbench import-fleurs tr_tr --splits dev test         # FLEURS, pinned dataset revision
uv run asrbench import-tsv recs.tsv --language xx --out data/mine/manifest.jsonl
uv run asrbench import-ksc2 --train-fraction 0.03 --full-train parliament   # Kazakh KSC2: all dev/test + hashed train sample
uv run asrbench filter-lang data/ksc2/manifest.jsonl          # drop Russian utterances from KSC2 (rule 3)
uv run asrbench validate data/fleurs/tr_tr/manifest.jsonl     # duplicate IDs, missing audio, speaker leakage

# 2. Run a model (copy a config from configs/runs/ and edit it)
uv run asrbench run configs/runs/my-run.yaml                  # -> runs/<name>_<timestamp>/

# 3. Score each language with the declared policy (configs/scoring.yaml)
uv run asrbench score runs/<run-dir>                          # -> scores.json, item_scores.jsonl, report.md
uv run asrbench score runs/<run-dir> --policy configs/scoring-nofillers.yaml --tag nofillers   # secondary policy -> scores.nofillers.json (ablation; primary files untouched)

# 4. Compare two systems on the same items (paired bootstrap)
uv run asrbench compare runs/<run-a> runs/<run-b>

# 5. Our contribution (announcement A1): fine-tune on train, select on dev, never touch test
uv run asrbench train configs/train/my-train.yaml             # -> checkpoints/<name>_<ts>/final (weights, gitignored)
                                                              #    runs/train_<name>_<ts>/ (manifest + log, commit)
# then run the saved model like any baseline: model.id = checkpoints/<name>_<ts>/final
uv run asrbench train configs/train/my-train.yaml --resume checkpoints/<name>_<ts>   # continue an interrupted run
```

To train on a Google Colab GPU instead of the local one, open `notebooks/colab_train.ipynb` (data via a tar on Google Drive; checkpoints on Drive; auto-resume; fp16 on T4), or drive a VM with the `colab` CLI (`colab new --gpu A100`, `colab exec`, `colab upload/download`): rebuild the data with the import commands and check the manifest sha256 against the local one. Keep the local machine on while a Colab VM runs, copy checkpoints off the VM as they appear, and do not `colab download` multi-GB files (stream big uploads over `colab ssh` in 100 MB parts instead).

Pretrained checkpoints run as they are count as **baselines**; a model trained by `asrbench train` counts as **ours**. The run manifest and `report.md` label every system as one or the other, so the two can be reported separately on the same test set (A1). Training supports `hf-whisper` (full fine-tune, orthographic targets) and `hf-ctc` (wav2vec2/XLS-R/MMS with a new character head, or `reuse_vocab: true`). `train_hours` subsamples the train split for learning curves; `train_filter`/`dev_filter` keep only items whose fields match (e.g. `{in_train_sample: true}`, `{subcorpus: parliament}`). MMS-1b-all baselines take `target_lang` (e.g. `kaz`) to load the language adapter; for training, `target_lang` + `reuse_vocab` + `adapter_only: true` trains only the adapter layers and LM head and also saves `adapter.<lang>.safetensors`. Whisper run configs accept `generate_kwargs` (e.g. `{no_repeat_ngram_size: 3}`) for decoder ablations, selected on dev only. Policies accept `drop_tokens` (a regex of whole tokens to remove, e.g. hesitation fillers). Example configs are in `configs/train/`.

Each run directory holds the deliverables the course asks for (slide S11):

| File | Contents |
|---|---|
| `manifest.json` | Run manifest: dataset sha256, model and resolved commit hash, settings, timing boundary, library versions, GPU |
| `predictions.jsonl` | Raw predictions, never normalized, paired with item ID and reference |
| `scores.json` / `report.md` | Per language: normalized WER and CER (primary) with 95% cluster-bootstrap CIs, orthographic WER/CER, MER, WIL, RTF and RTFx, silence report, top substitutions, worst items; baseline vs ours label |

The harness enforces these rules:
- English is rejected.
- Every run needs `eligibility_confirmed: true`.
- `.en` Whisper checkpoints and Parakeet v2 are refused.
- Test-split runs need `frozen: true` and can't be subsampled.
- Results are never averaged across languages.
- Clips with empty references go into a separate silence report.

## Docs

- Final report: [docs/report.md](docs/report.md); Georgian results: [docs/results-georgian.md](docs/results-georgian.md).
  All queued r2 evaluations are complete. Dev selected 14 s chunks; they worsened test performance, so the
  plain and decoder rows are reported separately. The r2 checkpoint is backed up locally with a verified SHA256
  (`runs/train_whisper-large-v3-turbo-ft-r2_cv-ka_20261120T000532Z/checkpoint_backup.json`). Training is closed.
- Project rules and deliverables: [docs/project-requirements.md](docs/project-requirements.md)
- Metrics, model families and code recipes: [docs/asr-methods-cheatsheet.md](docs/asr-methods-cheatsheet.md)
- Course materials and what's in them: [materials/INDEX.md](materials/INDEX.md)
- Agent instructions: [AGENTS.md](AGENTS.md)
