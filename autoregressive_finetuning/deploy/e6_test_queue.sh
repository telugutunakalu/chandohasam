#!/usr/bin/env bash
# The E6 test evaluation of the three final models (the user, 2026-10-18: the val rule, 15 poems per metre, seed 42:
# 183 test poems over 25 metres), free and constrained, then memorisation:
#   1. the 120M after E6 + its meaning → poem phase (../diffusion_finetuning/runs/e6-t1-120m);
#   2. the 523M, the same (runs/e6-t1-523m), once Nandi's fine-tuning is done: its 512-token forward passes cut the
#      trainer to a third of its speed (the user, 2026-10-18 18:20: wait for the Nandi training);
#   3. Nandi's final run, once its val evaluation is done (nandi-eval), on the (metre, poem) pairs and token budgets
#      of the 120M's test run;
#   4. memorisation of the three against the E6 train split.
# Every step is skipped when its result exists, and a stopped evaluation resumes where it was. Log:
# runs/e6-test-queue.log.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=../.venv/bin/python
DF=../diffusion_finetuning
log() { echo "[$(date +%F' '%T)] $*" | tee -a runs/e6-test-queue.log; }
mkdir -p runs results

mdlm_test() {                               # mdlm_test <tag>: runs/e6-t1-<tag> on the test split
    local name=e6_${1}_t1_test
    if [[ -f $DF/results/$name.md ]]; then log "$name: already done"; return 0; fi
    log "$name: start"
    (cd $DF && $PY -u constrained_sample.py --model "runs/e6-t1-$1" --name "$name" --e6-split test --shards 4 \
        --mask-workers 2 >> "runs/$name.log" 2>&1) || { log "$name: failed (see $DF/runs/$name.log)"; exit 1; }
    log "$name: done ($DF/results/$name.md)"
}
mdlm_test 120m
if [[ ! -f runs/nandi-t1/DONE ]]; then log "waiting for the Nandi fine-tuning (runs/nandi-t1/DONE) before the 523M"; fi
until [[ -f runs/nandi-t1/DONE ]]; do sleep 300; done
mdlm_test 523m

if [[ ! -f results/e6_nandi_val.md ]]; then log "waiting for Nandi's val evaluation (nandi-eval)"; fi
until [[ -f results/e6_nandi_val.md ]]; do sleep 300; done
snap=$(ls runs/nandi-t1/snapshots/ema_step_*.pt | sort | tail -1)
if [[ -f results/e6_nandi_test.md ]]; then
    log "e6_nandi_test: already done"
else
    log "e6_nandi_test: start ($snap)"
    $PY -u constrained_sample.py --name e6_nandi_test --weights "$snap" --reference e6_120m_t1_test --shards 4 \
        --mask-workers 2 >> runs/e6_nandi_test.log 2>&1 || { log "e6_nandi_test: failed (see runs/e6_nandi_test.log)"; exit 1; }
    log "e6_nandi_test: done (results/e6_nandi_test.md)"
fi

ln -sfn ../../autoregressive_finetuning/runs/e6_nandi_test $DF/runs/e6_nandi_test
for run in e6_120m_t1_test e6_523m_t1_test e6_nandi_test; do
    [[ -f $DF/results/${run}_memorisation.md ]] && continue
    (cd $DF && $PY memorisation.py --run "$run" --train-records data/e6/records/train.jsonl) >> runs/e6-test-queue.log 2>&1 \
        || log "$run: memorisation failed"
done
log "queue finished: $DF/results/e6_{120m,523m}_t1_test.md, results/e6_nandi_test.md (+ _memorisation in $DF/results)"
