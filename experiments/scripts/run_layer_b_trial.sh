#!/usr/bin/env bash
# Layer B trial (2026-10-07, fixed scoring): the E4B v2 trial's 111 poems (37 meters × 3 strategies, T1, seed 42) with the
# verse inventory and the attestation preference at weight 2 — only where the model's first choice is not
# allowed, then at every step. One model at a time; watchdog and memory trace as in run_hf_grid.sh.
set -u
W=/home/samvaran/phd_workspace/chandohasam
R=/home/samvaran/phd_workspace/chandohasam/experiments/runs
S=$W/experiments/scripts
cd $W/meter_engine
for where in override all; do
  OUT=$R/2026-10-07_e4b_v2_verse_attestB_$where
  mkdir -p $OUT
  nohup $W/.venv/bin/python -u -m metrical_decoder run --model google/gemma-4-E4B-it --out $OUT \
      --meters all --modes masking_only,masking_backtrack,hybrid --topics T1 --seeds 42 \
      --enforce gana,prasa,yati --profile strict --mask-workers 4 --inventory verse \
      --attest-weight 2 --attest-where $where >> $OUT/run.log 2>&1 &
  pid=$!
  echo $pid > $OUT/pid
  nohup $S/mem_watchdog.sh $pid 6 $OUT/watchdog.log > /dev/null 2>&1 &
  nohup $S/mem_trace.sh $pid $OUT/mem_trace.log > /dev/null 2>&1 &
  echo "$(date '+%F %T') $where: pid $pid"
  while kill -0 $pid 2>/dev/null; do sleep 15; done
  echo "$(date '+%F %T') $where: done, $(grep -c '' $OUT/results.jsonl) rows"
done
