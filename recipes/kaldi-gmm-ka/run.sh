#!/usr/bin/env bash
# Georgian MFCC + GMM-HMM baseline (Kaldi), trained by us from scratch on CV 27.0 ka train.
# Standard Kaldi GMM pipeline (as in egs/mini_librispeech/s5, egs/wsj/s5), sized for ~147 h:
#   mono (10k shortest utts) -> tri1 deltas (30k utts, 2500 leaves / 15k Gaussians)
#   -> tri2b LDA+MLLT (all, 4000 / 40k) -> tri3b SAT/fMLLR (all, 4000 / 40k); trigram KN LM on train text only.
# Stages 1-7 never touch test. Stage 8 (test) refuses to run unless decode-frozen.yaml exists (written by
# select_on_dev.sh from CV dev only and committed before the test decode).
#
#   cd ~/ka_gmm && bash run.sh [--stage N] [--stop-stage N]
set -euo pipefail
stage=0; stop_stage=8; nj=12; decode_nj=8  # decode jobs each hold HCLG in RAM
. ./path.sh
. utils/parse_options.sh
train_cmd=run.pl; decode_cmd=run.pl
mark() { echo "$(date -u +%H:%M:%S) $*" | tee -a job.log; }
mark "START stage=$stage stop=$stop_stage"

if [ $stage -le 1 ] && [ $stop_stage -ge 1 ]; then  # data dirs (from prep/), lang, LM
  mkdir -p data
  for d in prep/data/*; do rm -rf data/$(basename $d); cp -r $d data/; utils/fix_data_dir.sh data/$(basename $d); done
  cp -r prep/local data/
  utils/prepare_lang.sh data/local/dict "<UNK>" data/local/lang_tmp data/lang
  mkdir -p data/local/lm
  python3 utils/lang/make_kn_lm.py -ngram-order 3 -text data/local/lm_train.txt -lm data/local/lm/tg.arpa
  gzip -f data/local/lm/tg.arpa
  utils/format_lm.sh data/lang data/local/lm/tg.arpa.gz data/local/dict/lexicon.txt data/lang_test_tg
  mark "STAGE1_OK lang+LM"
fi

if [ $stage -le 2 ] && [ $stop_stage -ge 2 ]; then  # MFCC + CMVN for train and the dev sets (not test)
  for x in cv_train cv_dev fleurs_dev; do
    t0=$SECONDS
    steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj data/$x exp/make_mfcc/$x mfcc
    steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
    echo $((SECONDS - t0)) > exp/make_mfcc/$x/wall_sec
    utils/fix_data_dir.sh data/$x
  done
  utils/subset_data_dir.sh --shortest data/cv_train 10000 data/cv_train_10kshort
  utils/subset_data_dir.sh data/cv_train 30000 data/cv_train_30k
  mark "STAGE2_OK mfcc"
fi

if [ $stage -le 3 ] && [ $stop_stage -ge 3 ]; then
  steps/train_mono.sh --boost-silence 1.25 --nj $nj --cmd "$train_cmd" data/cv_train_10kshort data/lang exp/mono
  steps/align_si.sh --boost-silence 1.25 --nj $nj --cmd "$train_cmd" data/cv_train_30k data/lang exp/mono exp/mono_ali_30k
  mark "STAGE3_OK mono"
fi

if [ $stage -le 4 ] && [ $stop_stage -ge 4 ]; then
  steps/train_deltas.sh --boost-silence 1.25 --cmd "$train_cmd" 2500 15000 data/cv_train_30k data/lang exp/mono_ali_30k exp/tri1
  steps/align_si.sh --nj $nj --cmd "$train_cmd" data/cv_train data/lang exp/tri1 exp/tri1_ali
  mark "STAGE4_OK tri1"
fi

if [ $stage -le 5 ] && [ $stop_stage -ge 5 ]; then
  steps/train_lda_mllt.sh --cmd "$train_cmd" --splice-opts "--left-context=3 --right-context=3" 4000 40000 \
    data/cv_train data/lang exp/tri1_ali exp/tri2b
  steps/align_si.sh --nj $nj --cmd "$train_cmd" --use-graphs true data/cv_train data/lang exp/tri2b exp/tri2b_ali
  mark "STAGE5_OK tri2b"
fi

if [ $stage -le 6 ] && [ $stop_stage -ge 6 ]; then
  steps/train_sat.sh --cmd "$train_cmd" 4000 40000 data/cv_train data/lang exp/tri2b_ali exp/tri3b
  mark "STAGE6_OK tri3b"
fi

if [ $stage -le 7 ] && [ $stop_stage -ge 7 ]; then  # dev decodes (selection data); timed for RTFx
  utils/mkgraph.sh data/lang_test_tg exp/tri3b exp/tri3b/graph_tg
  utils/mkgraph.sh data/lang_test_tg exp/tri2b exp/tri2b/graph_tg
  for x in cv_dev fleurs_dev; do
    n=$(( $(wc -l < data/$x/spk2utt) < decode_nj ? $(wc -l < data/$x/spk2utt) : decode_nj ))
    t0=$SECONDS
    steps/decode_fmllr.sh --skip-scoring true --nj $n --cmd "$decode_cmd" exp/tri3b/graph_tg data/$x exp/tri3b/decode_tg_$x
    echo $((SECONDS - t0 + $(cat exp/make_mfcc/$x/wall_sec))) > exp/tri3b/decode_tg_$x/wall_sec  # MFCC+CMVN+2-pass decode
    t0=$SECONDS
    steps/decode.sh --skip-scoring true --nj $n --cmd "$decode_cmd" exp/tri2b/graph_tg data/$x exp/tri2b/decode_tg_$x
    echo $((SECONDS - t0 + $(cat exp/make_mfcc/$x/wall_sec))) > exp/tri2b/decode_tg_$x/wall_sec
  done
  mark "STAGE7_OK dev decodes"
fi

if [ $stage -le 8 ] && [ $stop_stage -ge 8 ]; then  # FROZEN TEST: run once, with settings selected on CV dev
  [ -f decode-frozen.yaml ] || { echo "decode-frozen.yaml missing: run select_on_dev.sh and commit it first"; exit 1; }
  lmwt=$(grep '^lmwt:' decode-frozen.yaml | awk '{print $2}'); wip=$(grep '^word_ins_penalty:' decode-frozen.yaml | awk '{print $2}')
  for x in cv_test fleurs_test; do
    t0=$SECONDS
    steps/make_mfcc.sh --cmd "$train_cmd" --nj $nj data/$x exp/make_mfcc/$x mfcc
    steps/compute_cmvn_stats.sh data/$x exp/make_mfcc/$x mfcc
    n=$(( $(wc -l < data/$x/spk2utt) < decode_nj ? $(wc -l < data/$x/spk2utt) : decode_nj ))
    steps/decode_fmllr.sh --skip-scoring true --nj $n --cmd "$decode_cmd" exp/tri3b/graph_tg data/$x exp/tri3b/decode_tg_$x
    echo $((SECONDS - t0)) > exp/tri3b/decode_tg_$x/wall_sec  # MFCC+CMVN+2-pass decode
    bash best_path.sh exp/tri3b/graph_tg/words.txt exp/tri3b/decode_tg_$x "$lmwt" "$wip" > exp/tri3b/decode_tg_$x/hyp.frozen.txt
  done
  mark "STAGE8_OK test decodes (lmwt=$lmwt wip=$wip)"
fi
mark DONE
