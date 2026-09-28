#!/usr/bin/env bash
# Run every data-sanity script in order. Each writes outputs/<script>.json.
# Every script also runs on its own; this is only the convenient full run.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-../.venv/bin/python}"
WORKERS="${WORKERS:-16}"

$PY level0_inventory.py
$PY level1_prosodic_integrity.py --workers "$WORKERS"
$PY level1_chance_pass_rates.py --workers "$WORKERS"
$PY level2_length_ratio.py
$PY level3_semantic_fidelity.py
$PY level4_lexical_diversity.py
$PY level4_subword_coverage.py
$PY level4_duplicates.py
$PY cross_level_summary.py --workers "$WORKERS"
