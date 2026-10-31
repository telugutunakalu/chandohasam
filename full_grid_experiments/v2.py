"""Run a grid evaluator with DAWG v2 A+B (PLAN.md decision 22): Layer A, the padyarchana syllable inventory; Layer B,
word attestation against the padyarchana words (E6 train split, ≥ 3 poems), weight 2 at every step. That is the T5 1B
v2 A+B setting (../t5_finetuning/runs/e6_t5g_1b_val_c_v2), and both corpora leave out the held-out poems.

    V2_TARGET=../autoregressive_finetuning/constrained_sample.py ../.venv/bin/python -u v2.py <its own arguments>

The evaluator is loaded as a module and its run_grid wrapped: inventory="padyarchana", and a DecodeConfig with Layer B
on. DiffusionGemma's evaluate_e6.py also gets settled_attest.decode_settled_attest as its settled decoder (Layer B in
the diffusion loop; its config is a DiffusionConfig). The module's __file__ is set to this file, so a sharded evaluator
starts its shards through it as well (they inherit V2_TARGET). T5's constrained_sample.py has the options itself
(--inventory, --attest-*), so grid.py calls it directly. No evaluator file is changed.
"""
from __future__ import annotations

import dataclasses
import importlib.util
import inspect
import os
import sys
from pathlib import Path

INVENTORY, WEIGHT, WHERE, CORPUS = "padyarchana", 2.0, "all", "padyarchana"


def load(target: Path):
    sys.path.insert(0, str(target.parent))                 # its siblings (nandi, common, settled …)
    spec = importlib.util.spec_from_file_location(f"v2_{target.stem}", target)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    base = mod.run_grid
    if target.name == "evaluate_e6.py":
        from settled_attest import decode_settled_attest
        mod.decode_settled = decode_settled_attest

        def run_grid(*a, **kw):
            return base(*a, **{**kw, "inventory": INVENTORY})
    else:
        def run_grid(*a, **kw):
            cfg = dataclasses.replace(kw.pop("cfg"), attest_weight=WEIGHT, attest_where=WHERE, attest_corpus=CORPUS)
            return base(*a, cfg=cfg, **{**kw, "inventory": INVENTORY})
    mod.run_grid = run_grid
    mod.__file__ = str(Path(__file__).resolve())
    return mod


def main() -> int:
    mod = load(Path(os.environ["V2_TARGET"]).resolve())
    rc = mod.main(sys.argv[1:]) if inspect.signature(mod.main).parameters else mod.main()
    return rc or 0


if __name__ == "__main__":
    raise SystemExit(main())
