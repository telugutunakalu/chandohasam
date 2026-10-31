#!/usr/bin/env bash
# Task-specific test (2026-10-16): after the 120M E6 (runs/e6-s2-120m: default mix, 2.5 epochs at 1e-4), one more
# epoch on T1 only (metre + meaning -> poem), lr 3e-5, 50 warm-up steps; then the same val evaluation. Compared with
# results/e6_120m_val.md, it decides whether the 523M gets the same phase after its E6.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=../.venv/bin/python
name=e6-t1-120m
log() { echo "[$(date +%F' '%T)] $*" | tee -a runs/$name.chain.log; }
if [[ ! -f runs/$name/DONE ]]; then
    log "$name: start"
    $PY -u -m ft.train --stage 2 --run $name --data-dir data/e6 --init-from runs/e6-s2-120m --mix '{"T1": 1.0}' \
        --lr 3e-5 --warmup-steps 50 --epochs 1 >> runs/$name.log 2>&1
    rc=$?
    if [[ $rc -ne 0 ]] || ! grep -a "^checkpoint at step" runs/$name.log | tail -1 | grep -q "(end of run)"; then
        log "$name: not finished (exit $rc)"; exit 1
    fi
    touch runs/$name/DONE; log "$name: done"
fi
if [[ ! -f results/e6_120m_t1_val.md ]]; then
    log "evaluation: start"
    $PY -u constrained_sample.py --model runs/$name --name e6_120m_t1_val --e6-split val --shards 4 --mask-workers 2 \
        >> runs/e6_120m_t1_val.log 2>&1 || { log "evaluation failed"; exit 1; }
    log "evaluation: done (results/e6_120m_t1_val.md)"
fi
