#!/usr/bin/env bash
# The GPU queue after the 2026-10-21 12:29 system OOM: two large jobs at once (DiffusionGemma constrained evaluation,
# 52.7 GB, and T5Gemma 2 270M full fine-tuning, 36 GB + 5.4 GB spikes, + host RAM) exhausted the GB10's shared memory;
# the kernel's OOM killer took VS Code (and with it every job started from it) and the annotation app.
# Now: one GPU job at a time, as a systemd user unit (outside VS Code), each job watched every 2 s — MemAvailable
# below FLOOR_GB → SIGTERM to that job only (never to anything else), SIGKILL 30 s later if it is still there.
#   systemd-run --user --unit=gpu-queue-1021 --collect experiments/scripts/gpu_queue_2026-10-21.sh
# Every step is skipped when its output exists (resumable).
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

# 1. T5Gemma 2 270M, full fine-tuning on the whole T1 pool (user decision 2026-10-21)
T5=$ROOT/t5_finetuning
[ -f $T5/runs/t5g-270m-full/final/config.json ] || run t5g-270m-full $T5 $T5/runs/t5g-270m-full.log \
    $PY -u train.py --size 270m --run t5g-270m-full --data train_full --epochs 1 --warmup 400 --eval-every 1000 --save-every 500

# 2–3. DiffusionGemma constrained E6 (fixed canvas + settled commit): base, then the 24k adapter (resumable per metre)
DG=$ROOT/lora_gemma_diffusion
for spec in "e6_dg_base_val_constrained -" "e6_dg_24k_val_constrained runs/lora-48k/lora_step_3000.pt"; do
    set -- $spec
    name=$1 lora=$2
    [ -s $DG/runs/$name/results.jsonl ] && continue
    args=(--name "$name" --modes masking_backtrack --decoder settled)
    [ "$lora" != - ] && args+=(--lora "$lora")
    run "$name" $DG $DG/runs/$name.log $PY -u evaluate_e6.py "${args[@]}"
done

# 4. The September DiffusionGemma trial (37 metres × 3 strategies, T1, seed 42) on the fixed shared decoder
OUT=$ROOT/experiments/runs/2026-10-22_diffusion_trial_entropyfix
mkdir -p "$OUT"
[ -f "$OUT/DONE" ] || { run september_trial $ROOT/meter_engine "$OUT/run.log" \
    $PY -u -m metrical_decoder diffusion --resident --out "$OUT" --meters all \
    --modes masking_only,masking_backtrack,hybrid --topics T1 --seeds 42 --enforce gana,prasa,yati --profile strict \
    --mask-workers 4 && touch "$OUT/DONE"; }
log "queue done"
