#!/usr/bin/env bash
# DiffusionGemma 26B-A4B (NVIDIA's NVFP4 checkpoint, experts decoded once and kept in BF16: ~52 GB),
# the three constrained strategies with gaṇa + prāsa + yati enforced (strict), on the E4B runs' prompts.
#   run_diffusion_constrained.sh OUT_DIR TOPICS SEEDS [MODES]
#   trial:    run_diffusion_constrained.sh .../2026-09-25_diffusion_trial T1 42
#   grid:     run_diffusion_constrained.sh .../2026-09-25_diffusion_constrained default 42,49,56,63,70
#   baseline: run_diffusion_constrained.sh .../2026-09-26_diffusion_baseline default 42,49,56,63,70 baseline
#             (free generation in the same loop: no mask, the model may end its reply; the enforcer watches)
# Resumable: rerunning skips the rows already in results.jsonl. A watchdog stops the run if available
# memory falls below 6 GB (the GB10 shares one memory between GPU and CPU; the model alone needs ~52 GB,
# so it cannot run beside the translategemma server, 76 GB).
set -euo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
OUT=${1:?output directory}
TOPICS=${2:-default}
SEEDS=${3:-42,49,56,63,70}
MODES=${4:-masking_only,masking_backtrack,hybrid}
mkdir -p "$OUT"
cd "$ROOT/meter_engine"
nohup "$ROOT/.venv/bin/python" -u -m metrical_decoder diffusion --resident --out "$OUT" \
    --meters all --modes "$MODES" --topics "$TOPICS" --seeds "$SEEDS" \
    --enforce gana,prasa,yati --profile strict --mask-workers 4 >> "$OUT/run.log" 2>&1 &
pid=$!
echo "$pid" > "$OUT/pid"
nohup "$ROOT/experiments/scripts/mem_watchdog.sh" "$pid" 6 "$OUT/watchdog.log" > /dev/null 2>&1 &
nohup "$ROOT/experiments/scripts/mem_trace.sh" "$pid" "$OUT/mem_trace.log" > /dev/null 2>&1 &
echo "diffusion run pid $pid, log $OUT/run.log"
