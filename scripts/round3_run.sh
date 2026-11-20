#!/usr/bin/env bash
# Round 3 (docs/preregistration-round3.md): same-GPU speed benchmark, then MMS FT seeds 7 and 13 with their
# dev + frozen test evaluations. Resumable: each finished step leaves a marker in runs/_round3/done/.
# Run from the repo root on Linux/WSL (KenLM), detached:  setsid nohup bash scripts/round3_run.sh >/dev/null 2>&1 &
set -euo pipefail
STATE=runs/_round3; mkdir -p "$STATE/done"
LOG="$STATE/round3.log"
log() { echo "[$(date -u +%FT%TZ)] $*" | tee -a "$LOG"; }
done_() { [ -e "$STATE/done/$1" ]; }
mark() { touch "$STATE/done/$1"; }

run_cfg() {  # run_cfg <config> [venv-bin-dir]; runs + scores once, resumes an unfinished run dir
  local cfg=$1 bin=${2:-} key name prev
  key=$(basename "$cfg" .yaml)
  done_ "$key" && { log "skip $key (done)"; return; }
  name=$(grep -m1 '^name:' "$cfg" | awk '{print $2}')
  prev=$(ls -d runs/"${name}"_2*/ 2>/dev/null | tail -1 || true)
  local asr="uv run asrbench"; [ -n "$bin" ] && asr="$bin/asrbench"
  if [ -n "$prev" ] && ! grep -q '"completed_utc"' "$prev/manifest.json" 2>/dev/null; then
    log "resume $key in $prev"; $asr run "$cfg" --resume "${prev%/}" >>"$LOG" 2>&1
  elif [ -z "$prev" ]; then
    log "run $key"; $asr run "$cfg" >>"$LOG" 2>&1
  fi
  prev=$(ls -d runs/"${name}"_2*/ | tail -1)
  uv run asrbench score "${prev%/}" >>"$LOG" 2>&1
  log "done $key -> $prev"; mark "$key"
}

# 1. Speed benchmark on this GPU (nothing else may use the GPU meanwhile).
for cfg in configs/runs/ka/round3/speed/*_speed.yaml; do
  case "$cfg" in *nvidia*) continue ;; esac
  run_cfg "$cfg"
done
if [ -x .venv-nemo/bin/asrbench ]; then
  run_cfg configs/runs/ka/round3/speed/nvidia-stt-ka-fastconformer_speed.yaml .venv-nemo/bin
else
  log "WARNING: .venv-nemo missing; NVIDIA speed row skipped"
fi

# 2. Seeds: train (resumable), generate configs, dev then frozen test (each once).
for s in 7 13; do
  name=mms-1b-all-kat-adapter-ft_cv-ka-seed$s
  if ! done_ "train-seed$s"; then
    ck=$(ls -d checkpoints/"${name}"_2*/ 2>/dev/null | tail -1 || true)
    if [ -n "$ck" ] && [ ! -d "$ck/final" ]; then
      log "resume training seed $s from $ck"; uv run asrbench train "configs/train/ka/$name.yaml" --resume "${ck%/}" >>"$LOG" 2>&1
    elif [ -z "$ck" ]; then
      log "train seed $s"; uv run asrbench train "configs/train/ka/$name.yaml" >>"$LOG" 2>&1
    fi
    mark "train-seed$s"
  fi
  ck=$(ls -d checkpoints/"${name}"_2*/ | tail -1); ck=${ck%/}
  [ -d "$ck/final" ] || { log "ERROR: $ck/final missing"; exit 1; }
  done_ "configs-seed$s" || { uv run python scripts/round3_configs.py seed "$s" "$ck/final" >>"$LOG" 2>&1; mark "configs-seed$s"; }
  for split in dev test; do
    for cfg in configs/runs/ka/round3/seed$s/*_"$split".yaml configs/runs/ka/round3/seed$s/*-"$split".yaml; do
      [ -e "$cfg" ] && run_cfg "$cfg"
    done
  done
done
log "ROUND 3 COMPLETE"
