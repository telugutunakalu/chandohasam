#!/usr/bin/env bash
# Third queue: Phase 0's DiffusionGemma part (full_grid_experiments/PLAN.md §3; user decisions 2026-10-21: a fresh
# LoRA run on the whole T1 pool; lever ① the speed test of examples per forward first).
# Waits for the second queue (gpu-queue-1021d: T5 1B → T5 4B whole pool) to end, then, one GPU job at a time with the
# same 2-s memory watchdog: the grid's P1 prompts (full_grid_experiments/prompts.py, Gemma-4 26B-A4B-it; then the
# user's review of prompts/p1_review.md while the rest runs) → the speed test (runs/speed_batch.json; its `best` is the
# --batch of the run, 1 if the test failed or its gate did not pass) → the whole-pool LoRA (lora-full; snapshots at
# 24k / 48k / ≈ half the pool) → its E6 free poems → the comparison table.
#   systemd-run --user --unit=gpu-queue-1022e --collect experiments/scripts/gpu_queue_2026-10-22e.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

run() {  # name dir logfile command...
    local name=$1 dir=$2 out=$3
    shift 3
    log "start $name"
    (cd "$dir" && exec "$@") >> "$out" 2>&1 &
    local pid=$! avail
    while kill -0 "$pid" 2>/dev/null; do
        avail=$(awk '/^MemAvailable:/ {print int($2 / 1048576)}' /proc/meminfo)
        if [ "$avail" -lt "$FLOOR_GB" ]; then
            log "$name: MemAvailable ${avail} GB < ${FLOOR_GB} GB: SIGTERM to $pid"
            kill -TERM "$pid"
            sleep 30
            kill -KILL "$pid" 2>/dev/null
        fi
        sleep 2
    done
    wait "$pid"
    local rc=$?
    log "end $name (exit $rc)"
    return $rc
}

DG=$ROOT/lora_gemma_diffusion
FG=$ROOT/full_grid_experiments
while systemctl --user is-active --quiet gpu-queue-1021d; do sleep 30; done
log "second queue ended; third queue (P1 prompts, DiffusionGemma whole pool) starts"

# 0. the grid's P1 prompts (183 source poems; resumable)
[ -f $FG/prompts/summary.json ] || run p1_prompts $FG $FG/prompts.log $PY -u prompts.py

# 1. the speed test: examples per forward (gate: batched = single forwards)
[ -f $DG/runs/speed_batch.json ] || run speed_batch $DG $DG/runs/speed_batch.log $PY -u speed_batch.py
B=$($PY -c "import json; d = json.load(open('$DG/runs/speed_batch.json')); print(d['best'] if d['gate']['passed'] else 1)" 2>/dev/null || echo 1)
log "DiffusionGemma whole pool: --batch $B"

# 2. the whole-pool LoRA: the 48k run's recipe (r 16 on q/k/v/o, lr 1e-4, 8 examples per step), one pass, natural mix
[ -f $DG/runs/lora-full/lora.pt ] || run lora-full $DG $DG/runs/lora-full.log \
    $PY -u train.py --run lora-full --data train_full --batch "$B" --epochs 1 --eval-every 1000 --save-every 100 \
    --snapshot-at 3000 6000 18800

# 3. its E6 free poems (native sampler), then the comparison table
if [ -f $DG/runs/lora-full/lora.pt ] && [ ! -s $DG/runs/e6_dg_full_val_free/results.jsonl ]; then
    run e6_dg_full_val_free $DG $DG/runs/e6_dg_full_val_free.log \
        $PY -u evaluate_e6.py --name e6_dg_full_val_free --lora runs/lora-full/lora.pt --modes baseline --free native
fi
run score_e6 $DG $DG/runs/score_e6.log $PY -u score_e6.py
log "third queue done"
