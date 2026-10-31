#!/usr/bin/env bash
# E6 for one model size, end to end (exp_checklist.md, E6):
#   1. stage 1: poem + meaning documents with 15% prose replay (ft.train defaults: 3 passes, lr 1e-4);
#   2. stage 2: a learning-rate sweep, 1 epoch per rate;
#   3. stage 2 at the rate with the lowest val T1 NELBO (metre + meaning -> poem), 2.5 epochs;
#   4. the E6 evaluation on val (constrained_sample.py --e6-split val).
#
#   ./run_e6.sh <tag> <initial weights> "<sweep learning rates>" [evaluation shards]
#   ./run_e6.sh 120m ../diffusion_pretraining/runs/pilot120m_hf/ema_step_0076000.pt "3e-5 6e-5 1e-4"
#
# Optional environment: E6_MIX (stage-2 task mix as JSON; default ft.canvas.DEFAULT_MIX), E6_FINAL_EPOCHS (default
# 2.5), E6_SUFFIX (added to the stage-2 and evaluation names, so a variant recipe keeps its own runs; stage 1 is
# shared), E6_EXTRA (more ft.train arguments, e.g. "--micro-tokens 8192"). With a single learning rate there is no
# sweep: the final run uses it. E6_SKIP_EVAL=1 stops after the final training run.
#
# Every step resumes or is skipped when done, so the script can be stopped (systemctl --user stop) and rerun at any
# point. A training step counts as done only when its trainer logged "(end of run)": ft.train also exits 0 when it is
# stopped. A failed step is retried 5 times, 5 minutes apart. Logs: runs/<run>.log and runs/e6-<tag>.chain.log.
set -uo pipefail
cd "$(dirname "$0")"
tag=${1:?tag}; init=${2:?initial weights}; lrs=${3:?sweep learning rates}; shards=${4:-4}
PY=../.venv/bin/python
sfx=${E6_SUFFIX:-}
final_epochs=${E6_FINAL_EPOCHS:-2.5}
read -r -a extra <<< "${E6_EXTRA:-}"
mix=()
[[ -n ${E6_MIX:-} ]] && mix=(--mix "$E6_MIX")
CHAIN=runs/e6-$tag$sfx.chain.log
mkdir -p runs results
log() { echo "[$(date +%F' '%T)] $*" | tee -a "$CHAIN"; }

step() {                                   # step <run name> <ft.train arguments...>
    local name=$1; shift
    if [[ -f runs/$name/DONE ]]; then log "$name: already done"; return 0; fi
    for try in 1 2 3 4 5; do
        log "$name: start (attempt $try)"
        $PY -u -m ft.train --run "$name" --data-dir data/e6 "${extra[@]}" "$@" >> "runs/$name.log" 2>&1
        local rc=$?
        if [[ $rc -eq 0 ]] && grep -a "^checkpoint at step" "runs/$name.log" | tail -1 | grep -q "(end of run)"; then
            touch "runs/$name/DONE"; log "$name: done"; return 0
        fi
        if [[ $rc -eq 0 ]]; then log "$name: stopped before the end (exit 0); not marked done"; exit 0; fi
        if [[ $rc -eq 3 ]]; then log "$name: diverged (exit 3); stopping the chain"; exit 3; fi
        log "$name: exit $rc; retrying in 5 min"; sleep 300
    done
    log "$name: failed 5 times; stopping the chain"; exit 1
}

log "recipe: mix ${E6_MIX:-default}, final epochs $final_epochs, rates $lrs, extra '${E6_EXTRA:-}'"
step "e6-s1-$tag" --stage 1 --init-from "$init"
read -r -a rates <<< "$lrs"
if [[ ${#rates[@]} -eq 1 ]]; then
    best=${rates[0]}
else
    for lr in "${rates[@]}"; do
        step "e6-s2-$tag$sfx-lr$lr" --stage 2 --init-from "runs/e6-s1-$tag" --lr "$lr" --epochs 1 "${mix[@]}"
    done
    best=$($PY - "$tag$sfx" "${rates[@]}" <<'EOF'
import json, sys
name, lrs = sys.argv[1], sys.argv[2:]
score = {}
for lr in lrs:
    vals = [json.loads(l)["val_nelbo/T1"] for l in open(f"runs/e6-s2-{name}-lr{lr}/metrics.jsonl") if '"val_nelbo/T1"' in l]
    score[lr] = vals[-1]
print(min(score, key=score.get))
print("sweep (last val T1 NELBO): " + ", ".join(f"{k} {v:.4f}" for k, v in score.items()), file=sys.stderr)
EOF
) || { log "could not pick a learning rate"; exit 1; }
fi
log "stage-2 learning rate: $best"
echo "$best" > "runs/e6-$tag$sfx.best_lr"
step "e6-s2-$tag$sfx" --stage 2 --init-from "runs/e6-s1-$tag" --lr "$best" --epochs "$final_epochs" "${mix[@]}"
tag=$tag$sfx                                  # the evaluation's names carry the variant
if [[ -n ${E6_SKIP_EVAL:-} ]]; then log "evaluation left to the caller (E6_SKIP_EVAL)"; exit 0; fi
if [[ -f results/e6_${tag}_val.md ]]; then
    log "evaluation: already done"
else
    log "evaluation: start"
    $PY -u constrained_sample.py --model "runs/e6-s2-$tag" --name "e6_${tag}_val" --e6-split val --shards "$shards" \
        --mask-workers 2 >> "runs/e6_${tag}_val.log" 2>&1 || { log "evaluation failed: see runs/e6_${tag}_val.log"; exit 1; }
    log "evaluation: done (results/e6_${tag}_val.md)"
fi
log "E6 $tag finished"
