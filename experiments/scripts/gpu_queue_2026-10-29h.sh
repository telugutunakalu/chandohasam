#!/usr/bin/env bash
# Sixth queue: DAWG v2 A+B on the 100-prompt grid (user decision 2026-10-28, full_grid_experiments/README.md decision
# 22). Waits for the grid queue (gpu-queue-1028g) to end, then, one GPU job at a time with the 2-s memory watchdog:
#   the v2 smoke pass (every v2 cell on 1 poem of 2 metres; failures logged, the queue goes on) → the 17 v2 cells
#   (grid.py --todo v2: every row's constrained cell on all 100 prompts with Layer A + Layer B; DiffusionGemma last)
#   → the table (score_grid.py: v1 and v2 side by side, paired tests, results/grid_v2_samples.md).
# Every cell is skipped when its results exist (resumable); a failed cell is logged and the next one runs.
#   systemd-run --user --unit=gpu-queue-1029h --collect experiments/scripts/gpu_queue_2026-10-29h.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/grid100/records
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

run() {  # name dir logfile command...
    local name=$1 dir=$2 out=$3
    shift 3
    log "start $name"
    (cd "$dir" && exec setsid "$@") >> "$out" 2>&1 &
    local pid=$! avail target
    while kill -0 "$pid" 2>/dev/null; do
        avail=$(awk '/^MemAvailable:/ {print int($2 / 1048576)}' /proc/meminfo)
        if [ "$avail" -lt "$FLOOR_GB" ]; then
            target=$pid
            [ "$(ps -o pgid= -p "$pid" | tr -d ' ')" = "$pid" ] && target=-$pid    # the group, only if it leads one
            log "$name: MemAvailable ${avail} GB < ${FLOOR_GB} GB: SIGTERM to $target"
            kill -TERM -- "$target"
            sleep 30
            kill -KILL -- "$target" 2>/dev/null
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
while systemctl --user is-active --quiet gpu-queue-1028g; do sleep 60; done
log "grid queue ended; DAWG v2 A+B on the 100 prompts starts"
cells v2smoke
cells v2
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "v2 queue done: results/grid.md (v1 and v2), results/grid_v2_samples.md"
