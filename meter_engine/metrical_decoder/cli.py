# -*- coding: utf-8 -*-
"""
Command line::

    python3 -m metrical_decoder rules kandamu                 # the rules text the model is given
    python3 -m metrical_decoder control --tokenizer google/gemma-4-E4B-it --out RUN_DIR
    python3 -m metrical_decoder run --model google/gemma-4-E4B-it --out RUN_DIR \\
        [--meters all|utpalamala,kandamu] [--modes baseline,masking_only,masking_backtrack,hybrid] \\
        [--topics default|T1,T3|"custom topic"] [--seeds 42,49,56]
    python3 -m metrical_decoder diffusion --out RUN_DIR [--resident] [--mask-workers 4] [grid options]
    python3 -m metrical_decoder diffusion --control --out RUN_DIR       # random-logit canvas, no model
    python3 -m metrical_decoder summarize RUN_DIR
    python3 -m metrical_decoder report RUN_DIR [RUN_DIR …] [--out report.md]

``control`` is the EXP-12 random-logit control (no model, CPU only): it
needs only the tokenizer, to build the same vocabulary slice as the model.
"""
from __future__ import annotations

import argparse
import sys
from typing import Optional

from .prompts import meter_rules, topic_items
from .runner import run_grid, summarize
from .strategies import MODES, DecodeConfig

CONSTRAINED = ("masking_only", "masking_backtrack", "hybrid")


def _meters(spec: str) -> list[str]:
    from indic_meter_dawg import default_dawg
    names = [s.name for s in default_dawg().catalogue.concrete if not s.abstract]
    if spec in ("all", ""):
        return names
    wanted = [m.strip() for m in spec.split(",")]
    unknown = [m for m in wanted if m not in names]
    if unknown:
        raise SystemExit(f"unknown meter(s): {', '.join(unknown)}")
    return wanted


def _modes(spec: str) -> list[str]:
    modes = [m.strip() for m in spec.split(",")]
    bad = [m for m in modes if m not in MODES]
    if bad:
        raise SystemExit(f"unknown mode(s): {', '.join(bad)}; choose from {', '.join(MODES)}")
    return modes


def _config(ns) -> DecodeConfig:
    return DecodeConfig(temperature=ns.temperature, top_p=ns.top_p, force_nl=ns.force_nl,
                        baseline_max_tokens=ns.baseline_max_tokens)


def _grid_args(p: argparse.ArgumentParser, default_modes: str) -> None:
    p.add_argument("--out", required=True, help="run directory (created; resumes if it exists)")
    p.add_argument("--meters", default="all")
    p.add_argument("--modes", default=default_modes)
    p.add_argument("--topics", default="default")
    p.add_argument("--seeds", default="42")
    p.add_argument("--units", type=int, default=1, help="units of a repeatable meter (dvipada couplets)")
    p.add_argument("--enforce", default="gana,prasa,yati",
                   help="constraints the decoder enforces: gana, or gana,prasa / gana,yati / gana,prasa,yati")
    p.add_argument("--profile", default="strict", help="prāsa / yati profile for enforcement (strict | relaxed)")
    p.add_argument("--temperature", type=float, default=0.7)
    p.add_argument("--top-p", type=float, default=0.9)
    p.add_argument("--force-nl", choices=("must_end", "on_accept"), default="must_end")
    p.add_argument("--baseline-max-tokens", type=int, default=None,
                   help="baseline budget (default 3 × the meter's longest poem + 32)")
    p.add_argument("--mask-workers", type=int, default=0,
                   help="compute masks in N worker processes (same masks; 0 = in this process)")


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(prog="metrical_decoder", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("rules", help="print the rules text of a meter")
    p.add_argument("meter")
    p.add_argument("--units", type=int, default=1)
    p = sub.add_parser("control", help="random-logit control over the model's vocabulary slice (no model)")
    p.add_argument("--tokenizer", required=True)
    _grid_args(p, ",".join(CONSTRAINED))
    p = sub.add_parser("run", help="generate with a Hugging Face model and evaluate")
    p.add_argument("--model", required=True)
    p.add_argument("--device", default="cuda")
    _grid_args(p, ",".join(MODES))
    p = sub.add_parser("diffusion", help="the three strategies with DiffusionGemma (NVFP4 checkpoint)")
    p.add_argument("--model", default="nvidia/diffusiongemma-26B-A4B-it-NVFP4")
    p.add_argument("--device", default="cuda")
    p.add_argument("--resident", action="store_true",
                   help="decode the NVFP4 experts once and keep BF16 (about 52 GB; much faster per pass)")
    p.add_argument("--control", action="store_true",
                   help="random-logit canvas over the model's vocabulary slice instead of the model (CPU)")
    p.add_argument("--entropy-bound", type=float, default=0.1,
                   help="a run of the model's proposals is kept while Σ entropy − max entropy ≤ this")
    p.add_argument("--allow-end", action="store_true",
                   help="let end-of-text tokens into the model's draft (the first trial's behaviour; see canvas.py)")
    _grid_args(p, ",".join(CONSTRAINED))
    p = sub.add_parser("summarize", help="per-meter × per-mode table of a run directory")
    p.add_argument("run_dir")
    p = sub.add_parser("report", help="token choices and probabilities across run directories (markdown)")
    p.add_argument("run_dirs", nargs="+")
    p.add_argument("--out", help="write the report here (and the numbers next to it as .json)")
    ns = ap.parse_args(argv)

    if ns.cmd == "rules":
        print(meter_rules(ns.meter, ns.units))
        return 0
    if ns.cmd == "summarize":
        print(summarize(ns.run_dir))
        return 0
    if ns.cmd == "report":
        from .analysis import report
        print(report(ns.run_dirs, ns.out))
        return 0
    meters, modes = _meters(ns.meters), _modes(ns.modes)
    topics, seeds = topic_items(ns.topics), [int(s) for s in ns.seeds.split(",")]
    if ns.cmd == "diffusion":
        return _diffusion(ns, meters, modes, topics, seeds)
    if ns.cmd == "control":
        from transformers import AutoTokenizer
        from .sources import RandomLogits
        from .vocab import TokenIndex
        tok = AutoTokenizer.from_pretrained(ns.tokenizer, local_files_only=True)
        index = TokenIndex.from_tokenizer(tok)
        source, name = RandomLogits(index), f"random-logits/{ns.tokenizer}"
    else:
        from .hf import HFCausalLM
        print(f"loading {ns.model} …", flush=True)
        source = HFCausalLM(ns.model, device=ns.device)
        index, name = source.index, ns.model
        print(f"loaded {type(source.model).__name__}: slice {index.size} tokens, eos {source.eos_ids}", flush=True)
    enforce = {x.strip() for x in ns.enforce.split(",")}
    out = run_grid(source, index, meters, modes, topics, seeds, ns.out, _config(ns), ns.units, name,
                   prasa="prasa" in enforce, yati="yati" in enforce, profile=ns.profile,
                   mask_workers=ns.mask_workers)
    print(summarize(out))
    return 0


def _diffusion(ns, meters, modes, topics, seeds) -> int:
    """The diffusion grid: same prompts, runner and outputs as ``run``, the diffusion decoding loop."""
    from .diffusion.decoding import MODES as DIFFUSION_MODES, DiffusionConfig, decode_diffusion
    bad = [m for m in modes if m not in DIFFUSION_MODES]
    if bad:
        raise SystemExit(f"unknown diffusion mode(s): {', '.join(bad)}; choose from {', '.join(DIFFUSION_MODES)}")
    cfg = DiffusionConfig(entropy_bound=ns.entropy_bound, force_nl=ns.force_nl)
    if ns.control:
        from transformers import AutoTokenizer
        from .diffusion.canvas import RandomCanvas
        from .vocab import TokenIndex
        tok = AutoTokenizer.from_pretrained(ns.model, local_files_only=True)
        canvas, name = RandomCanvas(TokenIndex.from_tokenizer(tok), canvas_length=256), f"random-canvas/{ns.model}"
    else:
        from .diffusion.canvas import DiffusionGemmaCanvas
        from .diffusion.loader import load_diffusiongemma_nvfp4
        print(f"loading {ns.model} (resident={ns.resident}) …", flush=True)
        model, tokenizer = load_diffusiongemma_nvfp4(ns.model, device=ns.device, resident=ns.resident,
                                                     log=lambda m: print(m, flush=True))
        canvas = DiffusionGemmaCanvas(model, tokenizer, entropy_bound=ns.entropy_bound, forbid_end=not ns.allow_end)
        if set(modes) == {"baseline"}:
            ends = "free generation, end tokens allowed"
        else:
            ends = f"end tokens {'allowed' if ns.allow_end else 'forbidden'} in the canvas"
            ends += "; allowed in the baseline" if "baseline" in modes else ""
        name = f"{ns.model} [experts {'resident BF16' if ns.resident else 'NVFP4 per pass'}; prefill empty thought; {ends}]"
        print(f"loaded: slice {canvas.index.size} tokens, canvas {canvas.canvas_length}", flush=True)
    enforce = {x.strip() for x in ns.enforce.split(",")}
    out = run_grid(canvas, canvas.index, meters, modes, topics, seeds, ns.out, cfg, ns.units, name,
                   prasa="prasa" in enforce, yati="yati" in enforce, profile=ns.profile,
                   mask_workers=ns.mask_workers, decode_fn=decode_diffusion)
    print(summarize(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
