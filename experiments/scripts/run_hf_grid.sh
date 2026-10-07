#!/usr/bin/env bash
# A Hugging Face model through the autoregressive loop: the free baseline and the three constrained
# strategies (gaṇa + prāsa + yati enforced, strict), with the E4B runs' prompts, topics, seeds and config.
#   run_hf_grid.sh MODEL OUT_DIR TOPICS SEEDS [MODES] [INVENTORY]
#   (INVENTORY: none | verse | tokenizer — only attested syllables, metrical_decoder/inventory.py)
#   trial:  run_hf_grid.sh google/gemma-4-26B-A4B-it .../2026-09-26_g26b_trial T1 42
#   grid:   run_hf_grid.sh google/gemma-4-26B-A4B-it .../2026-09-26_g26b default 42,49,56,63,70
# Resumable: rerunning skips the rows already in results.jsonl. A watchdog stops the run if available
# memory falls below 6 GB (the GB10 shares one memory between GPU and CPU); mem_trace.log records
# memory every 2 s during the load (synced to disk, so it survives a crash of the machine).
set -euo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
MODEL=${1:?model id}
OUT=${2:?output directory}
TOPICS=${3:-default}
SEEDS=${4:-42,49,56,63,70}
MODES=${5:-baseline,masking_only,masking_backtrack,hybrid}
INVENTORY=${6:-none}
mkdir -p "$OUT"
cd "$ROOT/meter_engine"
nohup "$ROOT/.venv/bin/python" -u -m metrical_decoder run --model "$MODEL" --out "$OUT" \
    --meters all --modes "$MODES" --topics "$TOPICS" --seeds "$SEEDS" \
    --enforce gana,prasa,yati --profile strict --mask-workers 4 --inventory "$INVENTORY" >> "$OUT/run.log" 2>&1 &
pid=$!
echo "$pid" > "$OUT/pid"
nohup "$ROOT/experiments/scripts/mem_watchdog.sh" "$pid" 6 "$OUT/watchdog.log" > /dev/null 2>&1 &
nohup "$ROOT/experiments/scripts/mem_trace.sh" "$pid" "$OUT/mem_trace.log" > /dev/null 2>&1 &
echo "run pid $pid, log $OUT/run.log"
