# Kaldi 5.5.1068 (conda-forge, CPU build) + egs/wsj/s5 steps/utils (kaldi-asr/kaldi e02e35f0); see setup.sh.
export PATH=$HOME/mamba/envs/kaldi/bin:$PWD/utils:$PWD:$PATH
export LC_ALL=C
export PYTHONUNBUFFERED=1
# conda-forge Kaldi links multithreaded OpenBLAS: one BLAS thread per process (Kaldi parallelises with jobs).
# Without this, 12 jobs x 16 threads oversubscribe the CPU and training slows down ~10x.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
