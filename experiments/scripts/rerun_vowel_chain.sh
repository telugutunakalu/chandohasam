#!/usr/bin/env bash
# 2026-09-26 rule change (no word of dead consonants alone): gate on the random-logit control, then
# regenerate the superseded poems of the DiffusionGemma grid, then of the E4B grid (one model on the
# GPU at a time). Each launcher resumes: it generates only the keys missing from results.jsonl.
#   rerun_vowel_chain.sh CONTROL_PIDS...     (log: experiments/runs/rerun_vowel_chain.log)
set -u
ROOT=/home/samvaran/phd_workspace/chandohasam
R=$ROOT/experiments/runs; S=$ROOT/experiments/scripts
log() { echo "$(date '+%F %T') $*"; }
wait_pid() { while kill -0 "$1" 2>/dev/null; do sleep 15; done; }
rows() { grep -c "" "$1/results.jsonl"; }

for p in "$@"; do wait_pid "$p"; done
C=$R/2026-09-26_control_vowel
n=$(cat $C/g*.log | grep -a -cE '^\[[0-9]+/')
bad=$(cat $C/g*.log | grep -a -E '^\[[0-9]+/' | grep -avcE ': complete .*gana=True prasa=True yati=True')
if [ "$n" -ne 555 ] || [ "$bad" -ne 0 ] || grep -a -q Traceback $C/g*.log; then
  log "CONTROL FAILED: $n poems, $bad not complete/in meter — no reruns started"; exit 1
fi
log "control passed: $n/555 complete and in meter"

for run in "2026-09-25_diffusion_constrained run_diffusion_constrained.sh default 42,49,56,63,70" \
           "2026-09-24_e4b_constrained run_e4b_constrained.sh"; do
  set -- $run; name=$1; dir=$R/$1; launcher=$2; shift 2
  before=$(rows $dir)
  echo "--- $(date '+%F %T') rerun of the poems superseded by the rule change (SUPERSEDED_VOWEL.txt)" >> $dir/run.log
  $S/$launcher $dir "$@" > /dev/null
  pid=$(cat $dir/pid)
  nohup $S/mem_trace.sh $pid $dir/mem_trace_rerun.log > /dev/null 2>&1 &
  log "$name: rerun started (pid $pid, $before rows kept)"
  wait_pid $pid
  after=$(rows $dir)
  if [ "$after" -ne 1665 ]; then log "$name: RERUN INCOMPLETE ($after/1665 rows); stopping"; exit 1; fi
  log "$name: rerun done, $after/1665 rows"
done
log "all reruns done"
