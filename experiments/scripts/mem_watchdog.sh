#!/usr/bin/env bash
# Stop a job before it starves the machine (GB10: GPU and CPU share one memory).
# usage: mem_watchdog.sh PID MIN_AVAILABLE_GB [LOG]
# Every 20 s reads MemAvailable; below the floor it sends SIGTERM to PID (never to anything else)
# and logs why. Exits when PID is gone.
pid=$1; floor_gb=$2; log=${3:-/dev/stdout}
floor_kb=$((floor_gb * 1024 * 1024))
while kill -0 "$pid" 2>/dev/null; do
  avail=$(awk '/^MemAvailable:/ {print $2}' /proc/meminfo)
  if [ "$avail" -lt "$floor_kb" ]; then
    echo "$(date '+%F %T') MemAvailable $((avail / 1024 / 1024)) GB < ${floor_gb} GB: SIGTERM to $pid" >> "$log"
    kill -TERM "$pid"
    exit 1
  fi
  sleep 20
done
echo "$(date '+%F %T') PID $pid finished; watchdog exits" >> "$log"
