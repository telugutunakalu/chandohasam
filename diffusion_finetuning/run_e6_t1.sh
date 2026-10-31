#!/usr/bin/env bash
# Task-specific phase after E6 (tested on the 120M 2026-10-16: val T1 NELBO 2.2525 -> 2.2301): from runs/e6-s2-<tag>,
# one epoch of T1 only (metre + meaning -> poem), at 0.3x the stage-2 rate the E6 sweep chose (the 120M: 3e-5 after
# 1e-4), 50 warm-up steps; then the val evaluation, unless E6_SKIP_EVAL is set.
#   ./run_e6_t1.sh <tag>
set -uo pipefail
cd "$(dirname "$0")"
tag=${1:?tag}
PY=../.venv/bin/python
name=e6-t1-$tag
log() { echo "[$(date +%F' '%T)] $*" | tee -a "runs/$name.chain.log"; }
best=$(cat "runs/e6-$tag.best_lr") || { log "no runs/e6-$tag.best_lr: run run_e6.sh first"; exit 1; }
lr=$($PY -c "print(f'{0.3 * float(\"$best\"):.2g}')")
if [[ ! -f runs/$name/DONE ]]; then
    for try in 1 2 3 4 5; do
        log "$name: start (lr $lr = 0.3 x $best; attempt $try)"
        $PY -u -m ft.train --stage 2 --run "$name" --data-dir data/e6 --init-from "runs/e6-s2-$tag" --mix '{"T1": 1.0}' \
            --lr "$lr" --warmup-steps 50 --epochs 1 >> "runs/$name.log" 2>&1
        rc=$?
        if [[ $rc -eq 0 ]] && grep -a "^checkpoint at step" "runs/$name.log" | tail -1 | grep -q "(end of run)"; then
            touch "runs/$name/DONE"; log "$name: done"; break
        fi
        if [[ $rc -eq 0 ]]; then log "$name: stopped before the end; not marked done"; exit 0; fi
        if [[ $rc -eq 3 ]]; then log "$name: diverged"; exit 3; fi
        log "$name: exit $rc; retrying in 5 min"; sleep 300
    done
    [[ -f runs/$name/DONE ]] || { log "$name: failed 5 times"; exit 1; }
fi
if [[ -n ${E6_SKIP_EVAL:-} ]]; then exit 0; fi
if [[ ! -f results/e6_${tag}_t1_val.md ]]; then
    log "evaluation: start"
    $PY -u constrained_sample.py --model "runs/$name" --name "e6_${tag}_t1_val" --e6-split val --shards 4 --mask-workers 2 \
        >> "runs/e6_${tag}_t1_val.log" 2>&1 || { log "evaluation failed"; exit 1; }
    log "evaluation: done (results/e6_${tag}_t1_val.md)"
fi
