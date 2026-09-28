#!/usr/bin/env bash
# Gemma-4 E4B, the three constrained strategies with gaṇa + prāsa + yati enforced (strict profile),
# on the baseline's prompts, topics, seeds and decoding config (2026-09-24_e4b_baseline).
# Resumable: rerunning skips the rows already in results.jsonl.
# A watchdog stops the run if the machine's available memory falls below 6 GB
# (GPU and CPU share one memory on the GB10, with the translategemma vLLM server).
set -euo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
OUT=${1:-$ROOT/experiments/runs/2026-09-24_e4b_constrained}
mkdir -p "$OUT"
cd "$ROOT/meter_engine"
nohup "$ROOT/.venv/bin/python" -u -m metrical_decoder run --model google/gemma-4-E4B-it --out "$OUT" \
    --meters all --modes masking_only,masking_backtrack,hybrid --topics default --seeds 42,49,56,63,70 \
    --enforce gana,prasa,yati --profile strict --mask-workers 4 >> "$OUT/run.log" 2>&1 &
pid=$!
echo "$pid" > "$OUT/pid"
nohup "$ROOT/experiments/scripts/mem_watchdog.sh" "$pid" 6 "$OUT/watchdog.log" > /dev/null 2>&1 &
echo "grid pid $pid, log $OUT/run.log"
