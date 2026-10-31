#!/usr/bin/env bash
# After the 48k run: validation diagnostics (base, 24k, 48k), then the E6 evaluation (free + masking/backtracking,
# 114 val poems) of the 48k adapter, the base model and the 24k adapter, one model on the GPU at a time.
# Every step is skipped when its output exists.                                   ./run_eval.sh
set -uo pipefail
cd "$(dirname "$0")"
export HF_HUB_OFFLINE=1
PY=$(realpath ..)/.venv/bin/python            # not realpath'd itself: that leaves the venv
log() { echo "[$(date +%F' '%T)] $*"; }
until grep -aq "end of run" runs/lora-48k.log 2>/dev/null && [ -f runs/lora-48k/lora.pt ]; do sleep 60; done
until [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ]; do sleep 10; done
if [ ! -s results/val_metrics.json ]; then
    log "val metrics"; $PY -u val_metrics.py --adapters runs/lora-48k/lora_step_3000.pt runs/lora-48k/lora.pt \
        > runs/val_metrics.log 2>&1 || log "val metrics failed"
fi
for spec in "e6_dg_48k_val runs/lora-48k/lora.pt" "e6_dg_base_val -" "e6_dg_24k_val runs/lora-48k/lora_step_3000.pt"; do
    set -- $spec
    name=$1 lora=$2
    [ -s runs/$name/results.jsonl ] && continue
    log "E6 $name"
    if [ "$lora" = - ]; then $PY -u evaluate_e6.py --name "$name" > "runs/$name.log" 2>&1 || log "$name failed"
    else $PY -u evaluate_e6.py --name "$name" --lora "$lora" > "runs/$name.log" 2>&1 || log "$name failed"; fi
done
log "done"
