#!/usr/bin/env bash
# User decisions 2026-10-21: fix the shared decoder's NaN entropy and rerun the September trial; constrained E6 for
# the base model and the 24k adapter too. After the 48k constrained run exits: apply the fix (fix_canvas_entropy.py),
# run the decoder tests (stop on failure), then constrained base → constrained 24k → the September trial rerun
# (37 metres × 3 strategies, T1, seed 42; as run_diffusion_constrained.sh … T1 42, the fixed canvas).
set -uo pipefail
cd "$(dirname "$0")"
export HF_HUB_OFFLINE=1
ROOT=$(realpath ..)
PY=$ROOT/.venv/bin/python
log() { echo "[$(date +%F' '%T)] $*"; }
WAIT_PID=${1:?pid of the 48k constrained run}
while kill -0 "$WAIT_PID" 2>/dev/null; do sleep 30; done
until [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ]; do sleep 20; done
log "48k constrained run finished"
$PY fix_canvas_entropy.py || { log "fix failed"; exit 1; }
(cd "$ROOT/meter_engine" && $PY -m unittest discover -s tests -p "test_dec_diffusion.py" -v) > runs/decoder_tests.log 2>&1 \
    || { log "decoder tests FAILED: runs/decoder_tests.log"; exit 1; }
log "decoder tests passed: $(tail -n 3 runs/decoder_tests.log | tr '\n' ' ')"
for spec in "e6_dg_base_val_constrained -" "e6_dg_24k_val_constrained runs/lora-48k/lora_step_3000.pt"; do
    set -- $spec
    name=$1 lora=$2
    [ -s runs/$name/results.jsonl ] && continue
    log "constrained $name"
    if [ "$lora" = - ]; then $PY -u evaluate_e6.py --name "$name" --modes masking_backtrack --decoder settled > "runs/$name.log" 2>&1 || log "$name failed"
    else $PY -u evaluate_e6.py --name "$name" --lora "$lora" --modes masking_backtrack --decoder settled > "runs/$name.log" 2>&1 || log "$name failed"; fi
done
OUT=$ROOT/experiments/runs/2026-10-22_diffusion_trial_entropyfix
log "September trial rerun → $OUT"
mkdir -p "$OUT"
(cd "$ROOT/meter_engine" && $PY -u -m metrical_decoder diffusion --resident --out "$OUT" --meters all \
    --modes masking_only,masking_backtrack,hybrid --topics T1 --seeds 42 --enforce gana,prasa,yati --profile strict \
    --mask-workers 4) >> "$OUT/run.log" 2>&1 || log "September trial rerun failed"
log "done"
