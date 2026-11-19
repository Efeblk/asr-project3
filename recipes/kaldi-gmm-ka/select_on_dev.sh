#!/usr/bin/env bash
# Choose the LM weight and word insertion penalty on CV ka DEV only (tri3b), write decode-frozen.yaml, and
# write the dev hypotheses of every decoded dev set with that choice. Commit decode-frozen.yaml before stage 8.
set -euo pipefail
. ./path.sh
words=exp/tri3b/graph_tg/words.txt
best=""; table=""
for lmwt in 7 8 9 10 11 12 13 14 15 16 17; do for wip in 0.0 0.5 1.0; do
  bash best_path.sh $words exp/tri3b/decode_tg_cv_dev $lmwt $wip > /tmp/hyp.$$
  w=$(compute-wer --text --mode=present ark:data/cv_dev/text ark:/tmp/hyp.$$ 2>/dev/null | grep '%WER' | awk '{print $2}')
  table="$table  - {lmwt: $lmwt, word_ins_penalty: $wip, cv_dev_wer: $w}\n"
  if [ -z "$best" ] || awk "BEGIN{exit !($w < ${best%% *})}"; then best="$w $lmwt $wip"; fi
done; done
rm -f /tmp/hyp.$$
read -r w lmwt wip <<< "$best"
{ echo "# Selected on CV 27.0 ka dev only (tri3b, Kaldi WER on normalized text), before any test decode."
  echo "# Applied unchanged to CV ka test and FLEURS ka test (and FLEURS dev). Beams: Kaldi decode_fmllr.sh defaults."
  echo "lmwt: $lmwt"; echo "word_ins_penalty: $wip"; echo "cv_dev_wer: $w"; echo "grid:"; printf "$table"; } > decode-frozen.yaml
for m in tri3b tri2b; do for x in cv_dev fleurs_dev; do
  [ -d exp/$m/decode_tg_$x ] && bash best_path.sh exp/$m/graph_tg/words.txt exp/$m/decode_tg_$x $lmwt $wip > exp/$m/decode_tg_$x/hyp.frozen.txt
done; done
cat decode-frozen.yaml | head -6
