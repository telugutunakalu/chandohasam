#!/usr/bin/env bash
# Step 4 of PLAN.md, queued behind the fine-tuning (run_nandi.sh): once runs/nandi-t1 is done,
#   1. the E6 evaluation of its final EMA snapshot on the 114 val poems of the MDLM rows (constrained_sample.py);
#   2. the same for the base model, if it has not been run, and for the step-4,000 snapshot (the lowest val loss
#      saved; the run overfits after ~4,500 steps, and the user chose to complete it: 2026-10-18 20:05);
#   3. memorisation against the E6 train split (../diffusion_finetuning/memorisation.py, through a link in its runs/,
#      so the result sits beside the MDLM ones in ../diffusion_finetuning/results/).
# Every step is skipped when its result exists. Log: runs/nandi-eval-queue.log.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=../.venv/bin/python
log() { echo "[$(date +%F' '%T)] $*" | tee -a runs/nandi-eval-queue.log; }
mkdir -p runs results

if [[ ! -f runs/nandi-t1/DONE ]]; then log "waiting for the final fine-tuning run (runs/nandi-t1/DONE)"; fi
until [[ -f runs/nandi-t1/DONE ]]; do sleep 300; done
snap=$(ls runs/nandi-t1/snapshots/ema_step_*.pt | sort | tail -1)
log "fine-tuning done: evaluating $snap"

evaluate() {                               # evaluate <name> [--weights <snapshot>]
    local name=$1; shift
    if [[ -f results/$name.md ]]; then log "$name: already done"; return 0; fi
    log "$name: start"
    $PY -u constrained_sample.py --name "$name" "$@" --shards 4 --mask-workers 2 >> "runs/$name.log" 2>&1 \
        || { log "$name: failed (see runs/$name.log)"; exit 1; }
    log "$name: done (results/$name.md)"
}
evaluate e6_nandi_val --weights "$snap"
evaluate e6_nandi_base_val
evaluate e6_nandi_s4000_val --weights runs/nandi-t1/snapshots/ema_step_0004000.pt

for run in e6_nandi_val e6_nandi_base_val e6_nandi_s4000_val; do
    [[ -f ../diffusion_finetuning/results/${run}_memorisation.md ]] && continue
    ln -sfn "../../autoregressive_finetuning/runs/$run" "../diffusion_finetuning/runs/$run"
    (cd ../diffusion_finetuning && $PY memorisation.py --run "$run" --train-records data/e6/records/train.jsonl) \
        >> runs/nandi-eval-queue.log 2>&1 || log "$run: memorisation failed"
done
log "queue finished: results/e6_nandi_val.md, results/e6_nandi_base_val.md, ../diffusion_finetuning/results/e6_nandi_*_memorisation.md"
