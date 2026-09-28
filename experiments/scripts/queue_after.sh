#!/usr/bin/env bash
# Start a job once a run has finished cleanly.
#   queue_after.sh PID RUN_DIR EXPECTED_ROWS LOG -- COMMAND...
# Waits for PID to exit; then starts COMMAND only if RUN_DIR/results.jsonl has EXPECTED_ROWS rows and
# every constrained row is complete and accepted by the engines (gaṇa, prāsa, yati strict).
set -u
pid=$1; run=$2; expected=$3; log=$4; shift 5
while kill -0 "$pid" 2>/dev/null; do sleep 15; done
read n bad < <(python3 - "$run/results.jsonl" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1])]
bad = sum(1 for r in rows if r["mode"] != "baseline" and not (r["status"] == "complete" and
          all((r.get("eval") or {}).get(k) for k in ("gana_strict", "prasa_strict", "yati_strict"))))
print(len(rows), bad)
PY
)
if [ "$n" -ne "$expected" ] || [ "$bad" -ne 0 ]; then
  echo "$(date '+%F %T') NOT started: $run has $n/$expected rows, $bad constrained rows not in meter: $*" >> "$log"; exit 1
fi
sleep 20                                                   # let the finished run release its memory
echo "$(date '+%F %T') $run finished ($n rows, all constrained in meter); starting: $*" >> "$log"
"$@" >> "$log" 2>&1
