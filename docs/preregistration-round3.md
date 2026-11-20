# Round 3 pre-registration (committed before any round-3 run, 2026-11-21)

Round 3 adds two checks for rigor. It adds no new modelling ideas and changes no selection.

## 1. Seed variance of our best system (MMS-1b-all `kat` adapter fine-tune, ± word 3-gram LM)

- Two more fine-tunes with seeds **7** and **13** (`configs/train/ka/mms-1b-all-kat-adapter-ft_cv-ka-seed{7,13}.yaml`).
  The recipe is byte-identical to the seed-42 run except for `name` and `seed`. Same data, steps, LR, and the same
  checkpoint rule (best dev WER on the same 300 dev clips).
- Hardware: local RTX 4070 SUPER (WSL). The seed-42 run used an A100. Precision and batch (8 × 4 accumulation) are
  unchanged.
- Evaluation: the four frozen seed-42 configs (CV/FLEURS × plain/+LM) and their dev twins, with only the checkpoint
  path and run name changed (`scripts/round3_configs.py seed`). **LM α 0.5 / β 0 is not re-selected.** Each test run
  happens once.
- Report: per-seed rows, plus mean ± sample SD over seeds {42, 7, 13} for CV and FLEURS test WER/CER, plain and +LM.
  The round-2 headline (seed 42) stays as it is; the 3-seed mean is reported next to it. If the seed-42 result turns
  out to be a lucky draw, the report says so.

## 2. Speed on one GPU

- Every system with a frozen CV test config is re-timed on the **same RTX 4070 SUPER**, on the **first 500 CV ka
  dev clips by ID**, with **batch 8**. Model, precision and decoder settings are unchanged
  (`configs/runs/ka/round3/speed/`, `scripts/round3_configs.py speed`). The GPU must not be used for anything else
  during these runs (no training, no games).
- The timing boundary is unchanged: forward/decode only, CUDA-synchronized, warm-up pass. LM rows include the CPU
  beam search with 12 workers.
- The r1 turbo FT is excluded because its weights were not kept; r2 is the same recipe. The Kaldi GMM-HMM is a
  CPU system and keeps its CPU RTFx.
- These runs are on dev and are used only for speed. Their WER on 500 clips is logged as a sanity check but not
  used for any choice.

## 3. Decoder ablation on dev (added 2026-11-21, before any of these runs; prompted by an external review)

The round-2 LM rows change two things at once: greedy → beam-100 search, and no LM → word 3-gram LM. The beam path
also decodes only the valid (unpadded) frames. To separate these effects, MMS FT (seed 42) and MMS zero-shot are
decoded on **CV dev and FLEURS dev only**, in two more variants (`configs/runs/ka/round3/decoder/`):

- `greedy-valid`: greedy CTC on unpadded frames only. This isolates the padding difference.
- `beam100-nolm`: pyctcdecode beam 100 without an LM. This isolates the beam search.

Together with the existing greedy and beam+LM dev runs, the chain is greedy → greedy-valid → beam → beam+LM. The test
set is not used, and nothing is selected from this ablation. It changes only how the round-2 gain is attributed in
the report.
