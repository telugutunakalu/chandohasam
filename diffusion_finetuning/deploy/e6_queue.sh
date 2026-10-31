#!/usr/bin/env bash
# Queue (2026-10-16): when the 523M pretraining has ended, E6 for the 523M with exactly the 120M's recipe (the user's
# decision: "the 523M fine-tuned on E6 just like the 120M; then task-specific training"):
#   ft.canvas.DEFAULT_MIX, stage 1 from the pretraining's final EMA, stage-2 sweep 3e-5 / 6e-5 / 1e-4 (1 epoch each),
#   the best rate for 2.5 epochs, then the val evaluation; then (the user's go, 2026-10-16 22:00) one epoch of T1 only
#   at 0.3x the chosen rate (run_e6_t1.sh), overlapped with the E6 evaluation, its own evaluation and both
#   memorisation checks.
# (A poem-heavy recipe was queued that morning and withdrawn before it started; ft.canvas.POEM_HEAVY_MIX keeps it.)
# The pretraining counts as ended only when its train.log's last checkpoint line says "(end of run)": a pause or a
# crash keeps the queue waiting. Every step of run_e6.sh resumes or is skipped when done; log: runs/e6-queue.log.
set -uo pipefail
cd "$(dirname "$0")/.."
P=../diffusion_pretraining/runs/stage1-523m
log() { echo "[$(date +%F' '%T)] $*" | tee -a runs/e6-queue.log; }
ended() { [[ "$(systemctl --user is-active telugu-mdlm-523m)" != "active" ]] &&
          grep -a "^checkpoint at step" "$P/train.log" | tail -1 | grep -q "(end of run)"; }
if ! ended; then log "waiting for the 523M pretraining to end (recipe: the 120M's, default mix)"; fi
until ended; do sleep 300; done
log "523M pretraining has ended: $(grep -a '^checkpoint at step' "$P/train.log" | tail -1)"
E6_SKIP_EVAL=1 ./run_e6.sh 523m "$P" "3e-5 6e-5 1e-4" || { log "523M E6 stopped (exit $?)"; exit 1; }
log "523M E6 trained; its evaluation (mostly CPU) now runs beside the T1-only phase (GPU) to save time"
./run_e6.sh 523m "$P" "3e-5 6e-5 1e-4" & eval_pid=$!         # every step is done: only the evaluation runs
E6_SKIP_EVAL=1 ./run_e6_t1.sh 523m || { log "523M T1-only phase stopped (exit $?)"; wait $eval_pid; exit 1; }
wait $eval_pid || { log "523M E6 evaluation failed"; exit 1; }
./run_e6_t1.sh 523m || { log "523M T1-only evaluation failed"; exit 1; }
for run in e6_523m_val e6_523m_t1_val; do
    [[ -f results/${run}_memorisation.md ]] || ../.venv/bin/python memorisation.py --run "$run" \
        --train-records data/e6/records/train.jsonl >> runs/e6-queue.log 2>&1
done
log "queue finished: results/e6_523m_val.md, results/e6_523m_t1_val.md (+ _memorisation)"
