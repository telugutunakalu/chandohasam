#!/usr/bin/env bash
# The training-curve figures (the user, 2026-10-18 20:20), queued behind the Nandi fine-tuning:
#   1. exposure_probe.py: memorisation over training for the three models (results/exposure_probe.json; GPU, ~45 min);
#   2. plot_curves.py: SVG figures (svgplot.py, standard library only: matplotlib could not be installed) into plots/
#      here and ../diffusion_finetuning/plots/.
# Steps are skipped when their output exists. Log: runs/curves-queue.log.
set -uo pipefail
cd "$(dirname "$0")/.."
PY=../.venv/bin/python
log() { echo "[$(date +%F' '%T)] $*" | tee -a runs/curves-queue.log; }
mkdir -p runs results

if [[ ! -f runs/nandi-t1/DONE ]]; then log "waiting for the Nandi fine-tuning (runs/nandi-t1/DONE)"; fi
until [[ -f runs/nandi-t1/DONE ]]; do sleep 300; done

if [[ -f results/exposure_probe.json ]]; then
    log "exposure probe: already done"
else
    log "exposure probe: start"
    $PY -u exposure_probe.py >> runs/exposure_probe.log 2>&1 || { log "exposure probe failed (see runs/exposure_probe.log)"; exit 1; }
    log "exposure probe: done (results/exposure_probe.json)"
fi

$PY -u plot_curves.py >> runs/plot_curves.log 2>&1 || { log "plotting failed (see runs/plot_curves.log)"; exit 1; }
log "figures written: plots/ and ../diffusion_finetuning/plots/ (README.md in each)"
