#!/usr/bin/env bash
# Run every data-sanity script in order. Outputs go to outputs/*.json.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-../.venv/bin/python}"

$PY build_subsets.py
$PY level1_prosodic_integrity.py --workers "${WORKERS:-12}"
$PY level1_chance_pass_rates.py
$PY level2_length_ratio.py
$PY level3_semantic_fidelity.py
$PY level4_lexical_diversity.py
$PY level4_subword_coverage.py
$PY level4_duplicates.py
$PY cross_level_summary.py
