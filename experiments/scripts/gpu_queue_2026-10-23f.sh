#!/usr/bin/env bash
# Fourth queue: the full grid (full_grid_experiments/PLAN.md; user decisions 2026-10-21: the grid runs last; levers
# ② the September rerun after the grid, ③ the extra strategies after the core cells).
# Waits for the third queue (gpu-queue-1022e: P1 prompts → DiffusionGemma whole pool) to end AND for the grid's records
# (full_grid_experiments/prompts/e6_p1/records/test.jsonl, written by build_records.py after the user's review of the
# prompts), then, one GPU job at a time with the 2-s memory watchdog:
#   the smoke pass (every core cell on 1 poem of 2 metres; failures logged, the queue goes on) → the core cells
#   (grid.py --todo core: free + constrained of every row; lever ④ read from the speed test) → the table
#   (score_grid.py) → the September rerun → the extra cells (grid.py --todo extra) → the table again.
# Every cell is skipped when its results exist (resumable); a failed cell is logged and the next one runs.
#   systemd-run --user --unit=gpu-queue-1023f --collect experiments/scripts/gpu_queue_2026-10-23f.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/e6_p1/records
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

cells() {  # kind: run every listed cell not yet done
    local kind=$1 name dir cmd
    mapfile -t todo < <(cd $FG && $PY grid.py --todo "$kind")
    log "grid $kind: ${#todo[@]} cells to run"
    for line in "${todo[@]}"; do
        IFS=$'\t' read -r name dir cmd <<< "$line"
        run "$name" "$dir" "$FG/logs/$name.log" bash -c "$cmd" || log "grid $kind: $name FAILED (see logs/$name.log)"
    done
}

mkdir -p $FG/logs
while systemctl --user is-active --quiet gpu-queue-1022e; do sleep 30; done
log "third queue ended; the grid waits for its records (the user's review of the prompts, then build_records.py)"
until [ -s $E6_RECORDS_DIR/test.jsonl ]; do sleep 300; done
log "grid records present; the grid starts"

cells smoke
cells core
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py

# lever ②: the September rerun (deferred by the user until after the grid)
OUT=$ROOT/experiments/runs/2026-10-22_diffusion_trial_entropyfix
grep -q '^deferred' "$OUT/DONE" 2>/dev/null && rm -f "$OUT/DONE"
[ -f "$OUT/DONE" ] || { run september_trial $ROOT/meter_engine "$OUT/run.log" \
    env -u E6_RECORDS_DIR $PY -u -m metrical_decoder diffusion --resident --out "$OUT" --meters all \
    --modes masking_only,masking_backtrack,hybrid --topics T1 --seeds 42 --enforce gana,prasa,yati --profile strict \
    --mask-workers 4 && touch "$OUT/DONE"; }

# lever ③: the † rows' other strategies, then the table again
cells extra
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "grid queue done"
