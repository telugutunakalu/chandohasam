#!/usr/bin/env bash
# Sixth queue, after the power outage of 2026-10-29 (rebooted 13:51; full_grid_experiments/README.md decisions 22–25):
# the rest of the 100-prompt grid (gpu-queue-1028g's last cells: DiffusionGemma whole pool, free and constrained; the
# 48k adapter is dropped from the study, decision 25), its table, then DAWG v2 A+B for the two ≈ 52 GB rows (Gemma-4
# 26B, DiffusionGemma) as in gpu_queue_2026-10-29j.sh, ordered for a table tonight. The side queue (grid-v2-side-1029,
# restarted) resumes the smaller rows' last v2 cell beside it. One job at a time here, with the 2-s memory watchdog
# (10 GB):
#   the grid's last cells → its table → the v2 smoke cells of the big rows → Gemma-4 26B and DiffusionGemma whole pool
#   v2 → wait for the side queue → a second try for any failed side cell → the table (every row but DiffusionGemma base
#   v2) → DiffusionGemma base v2 → a second try for any cell still missing → the final table.
# Every cell is skipped when its results exist (resumable: a cell cut off mid-run resumes at the poem level, see
# metrical_decoder.runner); a failed cell is logged and the next one runs. The page cache of the model files is dropped
# before a cell when it holds > 10 GB.
#   systemd-run --user --unit=gpu-queue-1029k --collect experiments/scripts/gpu_queue_2026-10-29k.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
BIG='^grid_(gemma4_26b|dg_[a-z0-9]+)_'
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/grid100/records
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

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

cells() {  # kind label grep-args...: run every listed cell not yet done that the filter keeps
    local kind=$1 label=$2 name dir cmd
    shift 2
    mapfile -t todo < <(cd $FG && $PY grid.py --todo "$kind" | grep "$@")
    log "grid $kind ($label): ${#todo[@]} cells to run"
    for line in "${todo[@]}"; do
        IFS=$'\t' read -r name dir cmd <<< "$line"
        run "$name" "$dir" "$FG/logs/$name.log" bash -c "$cmd" || log "grid $kind: $name FAILED (see logs/$name.log)"
    done
}

mkdir -p $FG/logs
log "after the power outage (rebooted 13:51): the rest of the 100-prompt grid, then DAWG v2 A+B for the big rows"
cells new "the grid's last cells" -E .
run score_grid_v1 $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "grid done: results/grid.md (100 prompts, v1; v2 for the rows done)"
cells v2smoke "big rows" -E "$BIG"
cells v2 "Gemma-4 26B, DiffusionGemma whole pool" -E '^grid_(gemma4_26b|dg_full)_'
while systemctl --user is-active --quiet grid-v2-side-1029; do sleep 60; done
cells v2 "smaller rows left over" -v -E "$BIG"
run score_grid_tonight $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "table without DiffusionGemma base v2: results/grid.md, results/grid_v2_samples.md; DiffusionGemma base v2 follows"
cells v2 "DiffusionGemma base" -E '^grid_dg_base_'
cells v2 "left over" -E .
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "v2 queue done: results/grid.md (v1 and v2, every row), results/grid_v2_samples.md"
