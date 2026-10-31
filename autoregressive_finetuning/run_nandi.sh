#!/usr/bin/env bash
# Steps 2–3 of PLAN.md for Nandi-Mini-150M, end to end, as run_e6.sh does for the MDLM:
#   1. the leakage probe and zero-shot likelihoods of the base model (leakage_probe.py);
#   2. a learning-rate sweep, 1 epoch per rate (2,350 steps of 128 E6 T1 examples), from the base model;
#      if the best rate is at an edge of the sweep, one more rate ×3 beyond it;
#   3. the final run from the base model at the rate with the lowest val T1 loss: 3.5 epochs (8,225 steps), the
#      meaning → poem exposure of the MDLM partner (E6's 2.5 passes + its 1-epoch T1 phase).
# (The speed test of step 2 is results/step2_speed.md.)
#
#   ./run_nandi.sh ["<sweep learning rates>"] [final epochs]
#   ./run_nandi.sh "5e-5 1.5e-4 4.5e-4" 3.5
#
# Every step resumes or is skipped when done, so the script can be stopped (systemctl --user stop nandi-ft) and
# rerun at any point. A training step counts as done only when its trainer logged "(end of run)": finetune.py also
# exits 0 when it is stopped. A failed step is retried 5 times, 5 minutes apart.
# Logs: runs/<run>.log and runs/nandi.chain.log.
set -uo pipefail
cd "$(dirname "$0")"
lrs=${1:-"5e-5 1.5e-4 4.5e-4"}; final_epochs=${2:-3.5}
PY=../.venv/bin/python
CHAIN=runs/nandi.chain.log
mkdir -p runs results
log() { echo "[$(date +%F' '%T)] $*" | tee -a "$CHAIN"; }

step() {                                   # step <run name> <finetune.py arguments...>
    local name=$1; shift
    if [[ -f runs/$name/DONE ]]; then log "$name: already done"; return 0; fi
    for try in 1 2 3 4 5; do
        log "$name: start (attempt $try)"
        $PY -u finetune.py --run "$name" "$@" >> "runs/$name.log" 2>&1
        local rc=$?
        if [[ $rc -eq 0 ]] && grep -a "^checkpoint at step" "runs/$name.log" | tail -1 | grep -q "(end of run)"; then
            touch "runs/$name/DONE"; log "$name: done ($(grep -a '^eval step' "runs/$name.log" | tail -1))"; return 0
        fi
        if [[ $rc -eq 0 ]]; then log "$name: stopped before the end (exit 0); not marked done"; exit 0; fi
        if [[ $rc -eq 3 ]]; then log "$name: diverged (exit 3); stopping the chain"; exit 3; fi
        log "$name: exit $rc; retrying in 5 min"; sleep 300
    done
    log "$name: failed 5 times; stopping the chain"; exit 1
}

best_rate() {                              # best_rate <rates...>: prints the rate with the lowest last val T1 loss
    $PY - "$@" <<'EOF'
import json, sys
score = {}
for lr in sys.argv[1:]:
    vals = [json.loads(l)["val_nll/T1"] for l in open(f"runs/nandi-t1-lr{lr}/metrics.jsonl") if '"val_nll/T1"' in l]
    score[lr] = vals[-1]
print(min(score, key=score.get))
print("sweep (last val T1, nats per MDLM token): " + ", ".join(f"{k} {v:.4f}" for k, v in score.items()), file=sys.stderr)
EOF
}

log "recipe: sweep rates $lrs (1 epoch each), final $final_epochs epochs"

# ---- step 2: leakage probe and zero-shot likelihoods (the base model)
if [[ -f results/step2_leakage.json ]]; then
    log "leakage probe: already done"
else
    log "leakage probe: start"
    $PY -u leakage_probe.py >> runs/leakage_probe.log 2>&1 || { log "leakage probe failed: see runs/leakage_probe.log"; exit 1; }
    log "leakage probe: done (results/step2_leakage.md)"
fi

# ---- step 3: sweep, then the final run
read -r -a rates <<< "$lrs"
for lr in "${rates[@]}"; do
    step "nandi-t1-lr$lr" --lr "$lr" --epochs 1
done
best=$(best_rate "${rates[@]}" 2>> "$CHAIN") || { log "could not pick a learning rate"; exit 1; }
sorted=($(printf '%s\n' "${rates[@]}" | sort -g))
edge=""
[[ $best == "${sorted[0]}" ]] && edge=$($PY -c "print(f'{float(\"$best\") / 3:.3g}')")
[[ $best == "${sorted[-1]}" ]] && edge=$($PY -c "print(f'{float(\"$best\") * 3:.3g}')")
if [[ -n $edge ]]; then
    log "best rate $best is at the edge of the sweep: adding $edge"
    step "nandi-t1-lr$edge" --lr "$edge" --epochs 1
    rates+=("$edge")
    best=$(best_rate "${rates[@]}" 2>> "$CHAIN") || { log "could not pick a learning rate"; exit 1; }
fi
log "learning rate: $best"
echo "$best" > runs/nandi.best_lr
step "nandi-t1" --lr "$best" --epochs "$final_epochs"
log "Nandi fine-tuning finished: runs/nandi-t1/snapshots/ (step 4, the E6 evaluation, is next)"
