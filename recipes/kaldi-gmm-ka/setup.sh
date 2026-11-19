#!/usr/bin/env bash
# One-time WSL setup (Ubuntu 24.04): Kaldi binaries from conda-forge + Kaldi's steps/utils scripts, work dir ~/ka_gmm.
set -euo pipefail
REC=$(cd "$(dirname "$0")" && pwd)
[ -x ~/bin/micromamba ] || (cd ~ && curl -Ls https://micro.mamba.pm/api/micromamba/linux-64/latest | tar -xj bin/micromamba)
export MAMBA_ROOT_PREFIX=~/mamba
[ -d ~/mamba/envs/kaldi ] || ~/bin/micromamba create -y -n kaldi -c conda-forge "kaldi=5.5.1068=cpu*" ffmpeg sox python=3.12
if [ ! -d ~/kaldi-src ]; then
  git clone -q --filter=blob:none --sparse https://github.com/kaldi-asr/kaldi.git ~/kaldi-src
  (cd ~/kaldi-src && git checkout -q e02e35f0254bb033fab73d1df99fc34123e31d56 && git sparse-checkout set egs/wsj/s5/steps egs/wsj/s5/utils)
fi
mkdir -p ~/ka_gmm && cd ~/ka_gmm
ln -sfn ~/kaldi-src/egs/wsj/s5/steps steps; ln -sfn ~/kaldi-src/egs/wsj/s5/utils utils
for f in run.sh path.sh best_path.sh select_on_dev.sh conf; do ln -sfn "$REC/$f" $f; done
echo "SETUP_OK $(pwd)"
