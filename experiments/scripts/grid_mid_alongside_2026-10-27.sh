#!/usr/bin/env bash
# The grid's mid-size cells beside DiffusionGemma's whole-pool training (asked 2026-10-27: "can we do anything in
# parallel from the grid?"): T5Gemma 2 4B ×3 rows (base, whole pool, 48k) and Gemma-4 E2B / E4B — ≈ 16–20 GB each
# against the training's ≈ 60 GB (MemAvailable ≈ 51 GB). Not here: Gemma-4 12B (23 GB of weights, too close to the
# floor), Gemma-4 26B and the DiffusionGemma cells (≈ 50 GB each). The smoke cells of these rows, then their core
# cells, then the T5 4B extra cells. Every cell is skipped when its results exist, so the main grid queue
# (gpu-queue-1023f) later skips what this did.
# - the 2-s memory watchdog (floor 20 GB, the training's queue stops at 10) stops only the running cell's group;
# - page cache: every 30 s, when MemFree < 20 GB, the large files' page cache is dropped (the GB10 gives CUDA only
#   MemFree; loading a 15 GB model fills the cache);
# - no new cell when the training is near its end (ETA < 4 h, < 8 h for an extra cell) or its queue has ended, so a
#   cell never runs twice beside gpu-queue-1023f.
#   systemd-run --user --unit=grid-mid-1027 --collect experiments/scripts/grid_mid_alongside_2026-10-27.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-20}
FREE_GB=${FREE_GB:-20}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
TRAIN_LOG=$ROOT/lora_gemma_diffusion/runs/lora-full.log
ROWS='^grid_(t5_4b_|gemma4_e2b_|gemma4_e4b_)'
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$FG/prompts/e6_p1/records
log() { echo "[$(date '+%F %T')] alongside-mid: $*" >> "$LOG"; }

evict() {  # drop the page cache of large files (repo + Hugging Face cache); clean pages only
    $PY -c "import sys; sys.path.insert(0, '$ROOT/diffusion_pretraining')
from mdlm.checkpoint_eval import _evict_large_files; _evict_large_files()" >/dev/null 2>&1
}

training_left_h() {  # hours left of the DiffusionGemma training; 0 once its queue has ended
    systemctl --user is-active --quiet gpu-queue-1022e || { echo 0; return; }
    grep -a -o 'ETA [0-9.]* h' "$TRAIN_LOG" | tail -n 1 | awk '{print int($2)}'
}

run() {  # name dir logfile command...
    local name=$1 dir=$2 out=$3
    shift 3
    log "start $name"
    (cd "$dir" && exec setsid "$@") >> "$out" 2>&1 &
    local pid=$! avail free target tick=0 epid=
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
        if [ $((tick++ % 15)) -eq 0 ] && { [ -z "$epid" ] || ! kill -0 "$epid" 2>/dev/null; }; then
            free=$(awk '/^MemFree:/ {print int($2 / 1048576)}' /proc/meminfo)
            [ "$free" -lt "$FREE_GB" ] && { evict & epid=$!; }
        fi
        sleep 2
    done
    wait "$pid"
    local rc=$?
    log "end $name (exit $rc)"
    return $rc
}

cells() {  # kind min_hours: these rows' cells of that kind not yet done, while the training has min_hours left
    local kind=$1 min_h=$2 name dir cmd left
    mapfile -t todo < <(cd $FG && $PY grid.py --todo "$kind" | grep -E "$ROWS")
    log "$kind: ${#todo[@]} mid-size cells"
    for line in "${todo[@]}"; do
        IFS=$'\t' read -r name dir cmd <<< "$line"
        left=$(training_left_h)
        if [ "${left:-0}" -lt "$min_h" ]; then
            log "stop before $name: the training has ${left:-0} h left (< $min_h h); gpu-queue-1023f runs the rest"
            exit 0
        fi
        evict
        run "$name" "$dir" "$FG/logs/$name.log" bash -c "$cmd" || log "$kind: $name FAILED (see logs/$name.log)"
    done
}

mkdir -p $FG/logs
[ -s $E6_RECORDS_DIR/test.jsonl ] || { log "no grid records: stop"; exit 1; }
cells smoke 4
cells core 4
cells extra 8
log "done"
