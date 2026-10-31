#!/usr/bin/env bash
# Side queue (user decision 2026-10-29 07:15, full_grid_experiments/README.md decision 23): the DAWG v2 A+B cells of the
# 14 smaller rows (Nandi ×2, Gemma-4 E4B, T5 ×7, MDLM ×4) run now, beside the 100-prompt grid (gpu-queue-1028g), not
# after it: these models leave the GPU mostly idle (T5 1B constrained: ≈ 20% busy, one CPU core), so the job beside
# them loses little. Gemma-4 26B and DiffusionGemma (≈ 52 GB each) stay in the GPU queue (gpu-queue-1029i), one at a
# time. This queue's watchdog floor is 20 GB (the GPU queues': 10 GB), so it stops its own cell first; before each cell
# the page cache of the model files is dropped when it holds > 10 GB (on the GB10 CUDA sees MemFree, not MemAvailable).
#   the v2 smoke cells → the v2 cells → an interim table (score_grid.py: v1, and v2 for the rows done)
# Every cell is skipped when its results exist; a failed cell is logged, and gpu-queue-1029i retries it after its own.
#   systemd-run --user --unit=grid-v2-side-1029 --collect experiments/scripts/grid_v2_side_2026-10-29.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-20}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
BIG='^grid_(gemma4_26b|dg_[a-z0-9]+)_'          # the ≈ 52 GB rows: gpu-queue-1029i's
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/grid100/records
log() { echo "[$(date '+%F %T')] side: $*" >> "$LOG"; }

evict() {  # the page cache of the model files, when it holds > 10 GB
    local free avail
    free=$(awk '/^MemFree:/ {print int($2 / 1048576)}' /proc/meminfo)
    avail=$(awk '/^MemAvailable:/ {print int($2 / 1048576)}' /proc/meminfo)
    [ $((avail - free)) -gt 10 ] && log "$($PY $ROOT/experiments/scripts/evict_model_cache.py 2>&1 | tail -n 1)"
    return 0
}

run() {  # name dir logfile command...
    local name=$1 dir=$2 out=$3
    shift 3
    evict
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

cells() {  # kind: run every listed cell not yet done, except the big rows'
    local kind=$1 name dir cmd
    mapfile -t todo < <(cd $FG && $PY grid.py --todo "$kind" | grep -v -E "$BIG")
    log "grid $kind (smaller rows): ${#todo[@]} cells to run"
    for line in "${todo[@]}"; do
        IFS=$'\t' read -r name dir cmd <<< "$line"
        run "$name" "$dir" "$FG/logs/$name.log" bash -c "$cmd" || log "grid $kind: $name FAILED (see logs/$name.log)"
    done
}

mkdir -p $FG/logs
log "DAWG v2 A+B for the 14 smaller rows starts beside the grid queue (floor ${FLOOR_GB} GB)"
cells v2smoke
cells v2
run score_grid_interim $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "side queue done: interim results/grid.md and results/grid_v2_samples.md (the big rows' v2 cells follow in gpu-queue-1029i)"
