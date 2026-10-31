#!/usr/bin/env bash
# The grid's small-model cells beside DiffusionGemma's whole-pool training (user decision 2026-10-24: "run small model
# cells alongside, let's save time"; full_grid_experiments/PLAN.md §8): Nandi ×2, MDLM ×4, T5Gemma 2 270M / 1B ×4 —
# 1–5 GB of GPU each and mostly CPU (the metre masks), against the training's ≈ 57 GB. The smoke cells of these rows,
# then their core cells, then the extra cells of the small † rows (Nandi, MDLM 523M). Every cell is skipped when its
# results exist, so the main grid queue (gpu-queue-1023f) later skips what this did. The 2-s memory watchdog stops
# only the running cell (never the training).
#   systemd-run --user --unit=grid-small-1024 --collect experiments/scripts/grid_small_alongside_2026-10-24.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
ROWS='^grid_(nandi_|mdlm120m_|mdlm523m_|t5_270m_|t5_1b_)'
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/e6_p1/records
log() { echo "[$(date '+%F %T')] alongside: $*" >> "$LOG"; }

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

cells() {  # kind: the small rows' cells of that kind not yet done
    local kind=$1 name dir cmd
    mapfile -t todo < <(cd $FG && $PY grid.py --todo "$kind" | grep -E "$ROWS")
    log "$kind: ${#todo[@]} small-model cells"
    for line in "${todo[@]}"; do
        IFS=$'\t' read -r name dir cmd <<< "$line"
        run "$name" "$dir" "$FG/logs/$name.log" bash -c "$cmd" || log "$kind: $name FAILED (see logs/$name.log)"
    done
}

mkdir -p $FG/logs
[ -s $E6_RECORDS_DIR/test.jsonl ] || { log "no grid records: stop"; exit 1; }
cells smoke
cells core
cells extra
log "done"
