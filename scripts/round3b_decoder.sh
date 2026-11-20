#!/usr/bin/env bash
# Round 3 §3 + §4 (docs/preregistration-round3.md): dev-only CTC decoder ablation, then the Whisper long-form
# bug-fix re-runs on FLEURS. Waits until round 3 is complete, so that the code those runs use is not changed under
# them, then updates the checkout and runs the configs once each.
set -euo pipefail
LOG=runs/_round3/round3.log
until grep -q "ROUND 3 COMPLETE" "$LOG" 2>/dev/null; do sleep 60; done
git pull -q --ff-only origin main
source <(sed -n '/^STATE=/,/^}$/p' scripts/round3_run.sh)
for cfg in configs/runs/ka/round3/decoder/*.yaml; do run_cfg "$cfg"; done
for split in dev test; do
  for cfg in configs/runs/ka/round3/lffix/*_fleurs-"$split".yaml; do run_cfg "$cfg"; done
done
log "ROUND 3B COMPLETE"
