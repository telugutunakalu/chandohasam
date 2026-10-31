#!/usr/bin/env bash
# The evaluation after the 2026-10-21 decoder findings (PLAN.md §6): free poems from the model's own sampler for the
# 48k adapter, the 24k adapter and the base model (114 E6 val prompts each), then constrained poems (fixed canvas +
# settled commit) for the 48k adapter. One model on the GPU at a time; each step skipped when its output exists.
set -uo pipefail
cd "$(dirname "$0")"
export HF_HUB_OFFLINE=1
PY=$(realpath ..)/.venv/bin/python
log() { echo "[$(date +%F' '%T)] $*"; }
until [ -z "$(nvidia-smi --query-compute-apps=pid --format=csv,noheader)" ]; do sleep 20; done
for spec in "e6_dg_48k_val_free runs/lora-48k/lora.pt" "e6_dg_24k_val_free runs/lora-48k/lora_step_3000.pt" "e6_dg_base_val_free -"; do
    set -- $spec
    name=$1 lora=$2
    [ -s runs/$name/results.jsonl ] && continue
    log "free $name"
    if [ "$lora" = - ]; then $PY -u evaluate_e6.py --name "$name" --modes baseline --free native > "runs/$name.log" 2>&1 || log "$name failed"
    else $PY -u evaluate_e6.py --name "$name" --lora "$lora" --modes baseline --free native > "runs/$name.log" 2>&1 || log "$name failed"; fi
done
name=e6_dg_48k_val_constrained
if [ ! -s runs/$name/results.jsonl ]; then
    log "constrained $name"
    $PY -u evaluate_e6.py --name "$name" --lora runs/lora-48k/lora.pt --modes masking_backtrack --decoder settled \
        > "runs/$name.log" 2>&1 || log "$name failed"
fi
log "done"
