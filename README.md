# ASR Project 3

This is a course project that evaluates automatic speech recognition on non-English languages. It contains `asrbench`, a harness that runs speech recognition models on a dataset and scores them in a reproducible way, following the course rules in [docs/project-requirements.md](docs/project-requirements.md).

## Setup

You need [uv](https://docs.astral.sh/uv/) and `ffmpeg` on your PATH.

```bash
uv sync --extra hf --group dev        # Whisper + wav2vec2/CTC (CUDA torch on Windows/Linux)
uv run pytest                         # 22 tests: metrics are checked against the slide examples
```

Extras for other model families. Each goes in its own environment, and neither has been tested in this repo yet:
- `uv sync --extra nemo`: Canary v2 and Parakeet v3. Linux or WSL recommended.
- `uv sync --extra qwen`: Qwen3-ASR. Needs a bf16 CUDA GPU.

## Workflow

```bash
# 1. Build a dataset manifest from a source with trusted references
uv run asrbench import-fleurs tr_tr --splits dev test         # FLEURS, pinned dataset revision
uv run asrbench import-tsv recs.tsv --language xx --out data/mine/manifest.jsonl
uv run asrbench validate data/fleurs/tr_tr/manifest.jsonl     # duplicate IDs, missing audio, speaker leakage

# 2. Run a model (copy a config from configs/runs/ and edit it)
uv run asrbench run configs/runs/my-run.yaml                  # -> runs/<name>_<timestamp>/

# 3. Score each language with the declared policy (configs/scoring.yaml)
uv run asrbench score runs/<run-dir>                          # -> scores.json, item_scores.jsonl, report.md

# 4. Compare two systems on the same items (paired bootstrap)
uv run asrbench compare runs/<run-a> runs/<run-b>
```

Each run directory holds the deliverables the course asks for (slide S11):

| File | Contents |
|---|---|
| `manifest.json` | Run manifest: dataset sha256, model and resolved commit hash, settings, timing boundary, library versions, GPU |
| `predictions.jsonl` | Raw predictions, never normalized, paired with item ID and reference |
| `scores.json` / `report.md` | WER and CER per language, MER, WIL, 95% cluster-bootstrap CIs, RTF, silence report, top substitutions, worst items |

The harness enforces these rules:
- English is rejected.
- Every run needs `eligibility_confirmed: true`.
- `.en` Whisper checkpoints and Parakeet v2 are refused.
- Test-split runs need `frozen: true` and can't be subsampled.
- Results are never averaged across languages.
- Clips with empty references go into a separate silence report.

## Docs

- Project rules and deliverables: [docs/project-requirements.md](docs/project-requirements.md)
- Metrics, model families and code recipes: [docs/asr-methods-cheatsheet.md](docs/asr-methods-cheatsheet.md)
- Course materials and what's in them: [materials/INDEX.md](materials/INDEX.md)
- Agent instructions: [AGENTS.md](AGENTS.md)
