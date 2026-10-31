#!/usr/bin/env bash
# Fifth queue: the 100-prompt grid (user decisions 2026-10-28, full_grid_experiments/README.md decisions 14–19). It
# replaces gpu-queue-1023f (gpu_queue_2026-10-25f.sh, stopped while it waited): one seed, masking + backtracking only,
# no September rerun, Gemma-4 12B and E2B out, and the prompts cut to 100 (build_grid100.py).
# Waits for the third queue (gpu-queue-1022e: DiffusionGemma whole-pool LoRA → its E6 check) to end, then, one GPU job
# at a time with the 2-s memory watchdog:
#   P1 prompts for the 10 new Vemana poems (prompts.py with Gemma-4 26B → prompts/grid100/p1/p1_review.md, for the
#   user's review) → the smoke pass → the core cells on the 80 known prompts (grid.py --todo core) → the table →
#   [waits for prompts/grid100/APPROVED, written by build_grid100.py --approve after the user's review] → every row's
#   cells on the 20 new prompts (grid.py --todo new) → the table.
# Every cell is skipped when its results exist (resumable); a failed cell is logged and the next one runs.
#   systemd-run --user --unit=gpu-queue-1028g --collect experiments/scripts/gpu_queue_2026-10-28g.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FLOOR_GB=${FLOOR_GB:-10}
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
FG=$ROOT/full_grid_experiments
G100=$FG/prompts/grid100
export HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1 E6_RECORDS_DIR=$G100/records
log() { echo "[$(date '+%F %T')] $*" >> "$LOG"; }

run() {  # name dir logfile command...
    local name=$1 dir=$2 out=$3
    shift 3
    log "start $name"
    # its own process group (setsid), so the watchdog stops the job with its shards and workers
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
while systemctl --user is-active --quiet gpu-queue-1022e; do sleep 30; done
log "third queue ended; the 100-prompt grid starts (records $E6_RECORDS_DIR)"
[ -s $G100/records/test.jsonl ] && [ -s $G100/p1_todo.json ] || { log "no grid100 records: run build_grid100.py; stop"; exit 1; }

# P1 for the 10 new Vemana poems (resumable: done poems are skipped, and no model is loaded when none is left)
run p1_grid100 $FG $FG/logs/p1_grid100.log $PY -u prompts.py --reference grid100_new_test \
    --ids prompts/grid100/p1_todo.json --out prompts/grid100/p1 \
    || log "p1_grid100 FAILED (see logs/p1_grid100.log); the new cells wait for the user"
log "P1 of the new Vemana poems → prompts/grid100/p1/p1_review.md: waiting for the user's review (APPROVED)"

cells smoke
cells core
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py

until [ -f $G100/APPROVED ]; do sleep 300; done
log "grid100: the new prompts approved; their cells start"
cells new
run score_grid $FG $FG/logs/score_grid.log $PY -u score_grid.py
log "grid queue done"
