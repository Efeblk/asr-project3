# Round 3 pre-registration (committed before any round-3 run, 2026-11-21)

Round 3 adds two checks for rigor. It adds no new modelling ideas and changes no selection.

## 1. Seed variance of our best system (MMS-1b-all `kat` adapter fine-tune, ± word 3-gram LM)

- Two more fine-tunes with seeds **7** and **13** (`configs/train/ka/mms-1b-all-kat-adapter-ft_cv-ka-seed{7,13}.yaml`).
  The recipe is byte-identical to the seed-42 run except for `name` and `seed`. Same data, steps, LR, and the same
  checkpoint rule (best dev WER on the same 300 dev clips).
- Hardware: local RTX 4070 SUPER (WSL). The seed-42 run used an A100. Precision and batch (8 × 4 accumulation) are
  unchanged.
  *Amended 2026-11-21, before seed 13 started and before any seed-7 result:* seed 13 trains on a Colab
  A100-SXM4-40GB (the seed-42 hardware) so that the two seeds run in parallel. Seed 7 stays on the RTX 4070 SUPER.
  Source code is the same commit, sent as a `git archive` whose commit is written into the run manifest. Only the
  adapter + head tensors come back from Colab; `scripts/rebuild_mms_adapter.py` restores the model, which is then
  evaluated in WSL like seed 7. Seed spread therefore also includes GPU-type nondeterminism, as seed 42 vs seed 7
  already does.
  *Execution note (2026-11-21, after the runs, recorded as a deviation):* the plan above was not followed exactly.
  (1) Seed 13 was also *evaluated* on the Colab A100, not in WSL. The same VM ran the same generated configs: dev
  first, then each frozen test once. It used the same LM file (sha256 checked at load) and installed the `lm`
  extra from the same `uv.lock`. (2) The seeds did not use "the same commit": seed 7 ran from `9ad99b9`, seed 13
  from `b8fbf88`. Between them only run-manifest provenance code changed (`envinfo.py`, `.gitattributes`,
  `ARCHIVE_COMMIT`). Training and decoding code is identical. (3) The
  decoder ablation (§3) later received an unregistered same-GPU greedy control (see the report).
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

## Fix applied before any round-3 training (2026-11-21, found by an external review)

`train.py` drew the 300-clip dev selection subset with the *training* seed. Seeds 7 and 13 would therefore have
selected their checkpoints on different dev clips from seed 42 (7/300 shared), which contradicts §1. The subset now
uses `dev_seed` (default 42). That reproduces the seed-42 subset exactly, and every earlier run used seed 42. Each
training run now also writes `dev_ids.txt`. `train_ids.txt` is written after the Whisper 448-token filter, and the
dropped IDs go to the train manifest. This commit is pulled into the WSL checkout before seed 7 starts training.

## 4. Bug-fix re-run: Whisper long-form decoding on FLEURS (added 2026-11-21, before these runs)

An external review found a harness bug. In `HFWhisper`, if any clip in a batch was longer than 30 s, the *whole
batch* was decoded with timestamped long-form generation. Because the runner sorts clips longest-first, the one
FLEURS ka clip over 30 s (33.2 s test, 32.2 s dev) put the 32 longest FLEURS clips into that mode, in every
Whisper run. Our fine-tunes were trained without timestamps and produced spliced, truncated outputs there. Common
Voice is not affected: no CV dev/test clip is longer than 15 s.

Fix (`long_form: split`, now the default): only clips over 30 s are handled specially. They are cut at pauses into
the fewest equal pieces of at most 30 s, decoded without timestamps, and joined with a space. The policy is the
same for every Whisper system. Every other clip is decoded whole, whatever its batch.

Re-run, once each, with the original frozen configs changed only in `long_form` and batch size (16, to fit a 12 GB
GPU; decoding no longer depends on the batch): FLEURS ka dev and test for Whisper-small, -large-v3, -large-v3-turbo
and our turbo FT r2 (`configs/runs/ka/round3/lffix/`). The r1 turbo FT cannot be re-run because its weights are
gone, and the chunked r2 runs are unaffected because all their pieces are 14 s or shorter. The report shows the
corrected FLEURS Whisper rows as the main numbers, keeps the original frozen rows next to them, and states why. No
setting is re-selected.
