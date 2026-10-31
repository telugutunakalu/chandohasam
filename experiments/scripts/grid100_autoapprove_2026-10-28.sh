#!/usr/bin/env bash
# Approval of the 100-prompt grid's P1 prompts (full_grid_experiments/README.md decision 21): the user approved them on
# 2026-10-28 ("approve it please") before they existed, so they get no hand review; the automatic checks stand in.
# Waits for prompts.py (gpu-queue-1028g's first step) to finish them (prompts/grid100/p1/summary.json is written last),
# then build_grid100.py --approve --allow-flagged: the P1 go into the records and APPROVED lets the queue's new cells
# start. A prompt kept with a failed check is accepted (as the user accepted the 183's flagged prompts), except a gold
# or telugu failure (a retelling sharing ≥ 12 aksharas with its poem, or non-Telugu letters): then nothing is
# approved and the log says which, for a decision. CPU only (the MDLM tokenizer).
#   systemd-run --user --unit=grid100-approve-1028 --collect experiments/scripts/grid100_autoapprove_2026-10-28.sh
set -uo pipefail
ROOT=/home/samvaran/phd_workspace/chandohasam
PY=$ROOT/.venv/bin/python
FG=$ROOT/full_grid_experiments
P1=$FG/prompts/grid100/p1
LOG=$ROOT/experiments/runs/gpu_queue_2026-10-21.log
export CUDA_VISIBLE_DEVICES= HF_HUB_OFFLINE=1 PYTHONUNBUFFERED=1
log() { echo "[$(date '+%F %T')] grid100-approve: $*" >> "$LOG"; }

N=$($PY -c "import json; print(len(json.load(open('$FG/prompts/grid100/p1_todo.json'))))")
log "waiting for the $N P1 prompts ($P1/summary.json)"
until [ -s "$P1/summary.json" ] && [ "$(wc -l < "$P1/p1.jsonl")" -ge "$N" ]; do sleep 60; done

hard=$($PY - "$P1/p1.jsonl" <<'EOF'
import json, sys
bad = [f"{r['id']} ({', '.join(k for k in ('gold', 'telugu') if not r['result']['checks'][k])})"
       for r in map(json.loads, open(sys.argv[1], encoding="utf-8"))
       if not (r["result"]["checks"]["gold"] and r["result"]["checks"]["telugu"])]
print("; ".join(bad))
EOF
)
if [ -n "$hard" ]; then
    log "NOT approved: gold/telugu check failed for $hard; edit them in prompts/grid100/p1_edits.jsonl, then build_grid100.py --approve"
    exit 1
fi
soft=$($PY -c "import json; print(sum(not json.loads(l)['result']['passed'] for l in open('$P1/p1.jsonl', encoding='utf-8')))")
cd $FG && $PY -u build_grid100.py --approve --allow-flagged >> $FG/logs/grid100_approve.log 2>&1 \
    && log "approved ($N P1 prompts, $soft kept with a failed check): APPROVED written, records updated" \
    || log "build_grid100.py --approve FAILED (see logs/grid100_approve.log)"
