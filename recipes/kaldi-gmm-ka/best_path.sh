#!/usr/bin/env bash
# One-best word sequence from a Kaldi decode dir's lattices at a given LM weight and word insertion penalty
# (the same lattice ops as steps/score_kaldi.sh). Usage: best_path.sh words.txt decode_dir lmwt wip > hyp.txt
set -euo pipefail
words=$1; dir=$2; lmwt=$3; wip=$4
lattice-scale --inv-acoustic-scale=$lmwt "ark:gunzip -c $dir/lat.*.gz|" ark:- 2>/dev/null \
  | lattice-add-penalty --word-ins-penalty=$wip ark:- ark:- 2>/dev/null \
  | lattice-best-path --word-symbol-table=$words ark:- ark,t:- 2>/dev/null \
  | utils/int2sym.pl -f 2- $words | sort
