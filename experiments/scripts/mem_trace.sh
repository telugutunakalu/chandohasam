#!/usr/bin/env bash
# usage: mem_trace.sh PID LOG
# Memory trace for a run: every 2 s for the first 10 min (the model load), then every 60 s.
# Each line is synced to disk so that it survives a hard crash of the machine.
pid=$1; log=$2; t0=$(date +%s)
while kill -0 "$pid" 2>/dev/null; do
  awk -v d="$(date '+%F %T')" '/^(MemAvailable|MemFree|Cached|Dirty|Writeback):/ {v[$1]=int($2/1048576)}
       END {printf "%s avail %d free %d cached %d dirty %d wb %d GB\n", d, v["MemAvailable:"], v["MemFree:"], v["Cached:"], v["Dirty:"], v["Writeback:"]}' /proc/meminfo >> "$log"
  sync "$log"
  if [ $(( $(date +%s) - t0 )) -lt 600 ]; then sleep 2; else sleep 60; fi
done
echo "$(date '+%F %T') PID $pid finished" >> "$log"
