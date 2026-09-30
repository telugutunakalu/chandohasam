"""Fine-tuning the Telugu MDLM on metrical poems (see ../PLAN.md).

Run everything from diffusion_finetuning/ inside the pretraining environment:

    uv run --project ../diffusion_pretraining python -m ft.build_data
    uv run --project ../diffusion_pretraining python -m ft.train --stage 1 ...

Importing this package puts diffusion_pretraining/ (mdlm, tokenizer, data_prep) and
meter_engine/ (indic_meter_dawg, chandohasam) on sys.path.
"""
from __future__ import annotations

import sys
from pathlib import Path

FT_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = FT_ROOT.parent
PRETRAIN_ROOT = PROJECT_ROOT / "diffusion_pretraining"
ENGINE_ROOT = PROJECT_ROOT / "meter_engine"
DATA_DIR = FT_ROOT / "data"
RUNS_DIR = FT_ROOT / "runs"

for _p in (PRETRAIN_ROOT, ENGINE_ROOT):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
