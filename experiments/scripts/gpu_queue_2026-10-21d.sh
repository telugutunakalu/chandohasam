#!/usr/bin/env bash
# Second queue, v3 (user decisions 2026-10-21 20:00, full_grid_experiments/README.md, Decisions): the T5Gemma 2 4B LoRA trains on
# the whole pool, keeping a snapshot after its first 48,000 examples (no separate 48k run); the DiffusionGemma 24k
# constrained E6 run is dropped (the grid's row 19 covers it).
# The first queue (gpu-queue-1021) is steered to stop after its base run by placeholder outputs that its skip rules
# honour (runs/e6_dg_24k_val_constrained/results.jsonl, experiments/runs/2026-10-22_diffusion_trial_entropyfix/DONE);
# this queue waits for it to end, removes the placeholders, then runs, one GPU job at a time with the same 2-s memory
# watchdog: T5Gemma 2 1B full fine-tuning (whole pool) → its E6 poems → T5Gemma 2 4B LoRA (r 32, attention + MLP, whole
# pool, snapshot at 48k) → E6 poems of the snapshot and the final adapter → the comparison table → the September rerun.
#   systemd-run --user --unit=gpu-queue-1021d --collect experiments/scripts/gpu_queue_2026-10-21d.sh
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

T5=$ROOT/t5_finetuning
DG=$ROOT/lora_gemma_diffusion
OUT=$ROOT/experiments/runs/2026-10-22_diffusion_trial_entropyfix
while systemctl --user is-active --quiet gpu-queue-1021; do sleep 30; done
log "first queue ended; second queue (v3) starts"
[ "$(cat $DG/runs/e6_dg_24k_val_constrained/results.jsonl 2>/dev/null)" = "placeholder" ] && \
    rm -f $DG/runs/e6_dg_24k_val_constrained/results.jsonl && rmdir $DG/runs/e6_dg_24k_val_constrained
[ "$(cat $OUT/DONE 2>/dev/null)" = "placeholder" ] && rm -f $OUT/DONE

# 1. T5Gemma 2 1B, full fine-tuning on the whole T1 pool (t5_finetuning/PLAN.md §5)
[ -f $T5/runs/t5g-1b-full/final/config.json ] || run t5g-1b-full $T5 $T5/runs/t5g-1b-full.log \
    $PY -u train.py --size 1b --run t5g-1b-full --data train_full --lr 5e-5 --warmup 400 --eval-every 1000 --save-every 500
# 2. its E6 poems
if [ -f $T5/runs/t5g-1b-full/final/config.json ] && [ ! -s $T5/runs/e6_t5g_1b_val/results.jsonl ]; then
    run e6_t5g_1b_val $T5 $T5/runs/e6_t5g_1b_val.log $PY -u generate.py --size 1b --model runs/t5g-1b-full/final --name e6_t5g_1b_val
fi
# 3. T5Gemma 2 4B, LoRA r 32 on attention + MLP, gradient checkpointing, the whole T1 pool; the adapter after the first
#    48,000 examples kept as lora_at_48000.pt (full_grid_experiments/README.md, Phase 0)
[ -f $T5/runs/t5g-4b-lora-full/lora.pt ] || run t5g-4b-lora-full $T5 $T5/runs/t5g-4b-lora-full.log \
    $PY -u train.py --size 4b --run t5g-4b-lora-full --data train_full --lora 32 --lora-mlp --grad-ckpt --lr 2e-4 \
    --warmup 400 --eval-every 1000 --save-every 250 --snapshot-at 48000
for spec in "e6_t5g_4b_48k_val lora_at_48000.pt" "e6_t5g_4b_val lora.pt"; do
    set -- $spec
    if [ -f $T5/runs/t5g-4b-lora-full/$2 ] && [ ! -s $T5/runs/$1/results.jsonl ]; then
        run $1 $T5 $T5/runs/$1.log $PY -u generate.py --size 4b --lora runs/t5g-4b-lora-full/$2 --r 32 --lora-mlp --name $1
    fi
done
# 4. the comparison table (all sets on disk)
run score_e6 $DG $DG/runs/score_e6.log $PY -u score_e6.py
# 5. the September trial rerun (37 metres × 3 strategies, T1, seed 42) on the fixed shared decoder
mkdir -p "$OUT"
[ -f "$OUT/DONE" ] || { run september_trial $ROOT/meter_engine "$OUT/run.log" \
    $PY -u -m metrical_decoder diffusion --resident --out "$OUT" --meters all \
    --modes masking_only,masking_backtrack,hybrid --topics T1 --seeds 42 --enforce gana,prasa,yati --profile strict \
    --mask-workers 4 && touch "$OUT/DONE"; }
log "second queue (v3) done"
