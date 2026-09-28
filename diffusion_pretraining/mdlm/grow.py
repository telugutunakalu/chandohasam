"""Grow a trained Denoiser into a wider and/or deeper preset without changing what it computes.

    uv run python -m mdlm.grow --from runs/pilot120m --to grow-1536x16 --out runs/pilot120m/grown/grow-1536x16.pt
    uv run python -m mdlm.train --run stage1 --preset grow-1536x16 \\
        --init-from runs/pilot120m/grown/grow-1536x16.pt --warmup-steps 1000 ...

Width, by a whole factor k (HyperCloning, Samragh et al. 2024). The grown model
carries k copies of every hidden vector side by side. Embedding rows and RMSNorm
gains are tiled; each attention head is repeated k times, and because head_dim
stays 64 every copy attends exactly as the original head did. Every linear layer
becomes a k x k grid of blocks w/k, which maps k copies of x to k copies of w @ x.
With tied embeddings the k copies would make the logits k times too large, so the
final RMSNorm gain is divided by k. Each grid also gets noise that sums to zero
over the input copies. It leaves the function unchanged but gives the copies
different gradients, so they drift apart in training instead of staying clones.

Depth. New blocks are copies of the block they follow, spread evenly through the
stack, with their two residual output projections (proj, down) set to zero, so
each adds nothing to the residual stream until training moves those weights.

The output file holds {"model": state_dict, "model_config", "grown_from"};
mdlm.train --init-from starts a new run from it (fresh optimizer, step 0).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
from pathlib import Path

import torch

from .checkpoint import load_latest
from .model import PRESETS, Denoiser, ModelConfig


def plan(src: ModelConfig, dst: ModelConfig) -> tuple[int, list[int]]:
    """(width factor k, [index of the old block each new block follows]); raises ValueError when dst
    cannot be reached from src function-preservingly."""
    for f in ("vocab_size", "max_len", "rope_base", "norm_eps"):
        if getattr(src, f) != getattr(dst, f):
            raise ValueError(f"{f} must not change ({getattr(src, f)} -> {getattr(dst, f)})")
    k, rem = divmod(dst.d_model, src.d_model)
    if rem or k < 1:
        raise ValueError(f"d_model {dst.d_model} is not a whole multiple of {src.d_model}")
    if src.d_model % src.n_heads or dst.d_model % dst.n_heads or dst.head_dim != src.head_dim:
        raise ValueError(f"head_dim must stay the same ({src.head_dim} -> {dst.head_dim})")
    if dst.mlp_hidden != k * src.mlp_hidden:
        raise ValueError(f"mlp_hidden must grow with the width ({src.mlp_hidden} x {k} != {dst.mlp_hidden})")
    new = dst.n_layers - src.n_layers
    if new < 0:
        raise ValueError(f"cannot remove layers ({src.n_layers} -> {dst.n_layers})")
    return k, [math.ceil((i + 1) * src.n_layers / new) - 1 for i in range(new)]


def _tile(w: torch.Tensor, k: int, noise: float, gen: torch.Generator) -> torch.Tensor:
    """(out, in) -> (k*out, k*in): block (i, j) is w/k + n_ij with sum_j n_ij = 0, so the result maps
    k side-by-side copies of x to k copies of w @ x. Built in float64."""
    w = w.double()
    out, inp = w.shape
    blocks = (w / k).expand(k, k, out, inp).clone()
    if noise:
        n = torch.randn(blocks.shape, generator=gen, dtype=torch.float64) * (noise * float(w.std()) / k)
        blocks += n - n.mean(dim=1, keepdim=True)
    return blocks.permute(0, 2, 1, 3).reshape(k * out, k * inp)


def widen(sd: dict, cfg: ModelConfig, k: int, noise: float, gen: torch.Generator, dtype) -> dict:
    """State dict of cfg -> state dict of the model k times as wide (see the module docstring)."""
    if k == 1:
        return {name: w.to(dtype) for name, w in sd.items()}
    out = {}
    for name, w in sd.items():
        w = w.double()
        if name == "embed.weight":
            g = w.repeat(1, k)
        elif name == "norm.weight":
            g = w.repeat(k) / k                                    # tied logits: k copies sum to k x logits
        elif name.endswith(("norm1.weight", "norm2.weight")):
            g = w.repeat(k)
        elif name.endswith("qkv.weight"):                          # q, k and v each become k copies of their heads
            g = torch.cat([_tile(part, k, noise, gen) for part in w.split(cfg.d_model)])
        elif name.endswith("gate_up.weight"):                      # gate and up each become k copies
            g = torch.cat([_tile(part, k, noise, gen) for part in w.split(cfg.mlp_hidden)])
        elif name.endswith(("proj.weight", "down.weight")):
            g = _tile(w, k, noise, gen)
        else:
            raise KeyError(f"no widening rule for {name}")
        out[name] = g.to(dtype)
    return out


def deepen(sd: dict, n_layers: int, after: list[int]) -> dict:
    """Insert, after block p for every p in `after`, a copy of block p whose proj and down are zero."""
    blocks = [{n.split(".", 2)[2]: w for n, w in sd.items() if n.startswith(f"blocks.{i}.")} for i in range(n_layers)]
    stack = []
    for i, blk in enumerate(blocks):
        stack.append(blk)
        for _ in range(after.count(i)):
            new = {n: w.clone() for n, w in blk.items()}
            new["proj.weight"].zero_()
            new["down.weight"].zero_()
            stack.append(new)
    out = {n: w for n, w in sd.items() if not n.startswith("blocks.")}
    for i, blk in enumerate(stack):
        out.update({f"blocks.{i}.{n}": w for n, w in blk.items()})
    return out


def grow(sd: dict, src: ModelConfig, dst: ModelConfig, noise: float = 0.1, seed: int = 0,
         dtype=torch.float32) -> dict:
    """State dict of a src-shaped model -> state dict of a dst-shaped model computing the same function."""
    k, after = plan(src, dst)
    gen = torch.Generator().manual_seed(seed)
    return deepen(widen(sd, src, k, noise, gen, dtype), src.n_layers, after)


def load_source(path: Path, which: str) -> tuple[dict, ModelConfig, dict]:
    """(state dict, config, provenance) from a run directory (its newest checkpoint) or an EMA snapshot."""
    if path.is_dir():
        state = load_latest(path, "cpu")
        if state is None:
            raise FileNotFoundError(f"no checkpoint in {path}")
        return (state[which], ModelConfig(**state["model_config"]),
                {"source": str(path), "weights": which, "step": state["step"]})
    state = torch.load(path, map_location="cpu", weights_only=False)
    run_dir = path.parent.parent if path.parent.name == "snapshots" else path.parent
    cfg = ModelConfig(**json.loads((run_dir / "config.json").read_text())["model"])
    return state["ema"], cfg, {"source": str(path), "weights": "ema", "step": state["step"]}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="src", type=Path, required=True,
                    help="a run directory (its newest checkpoint) or a snapshots/ema_step_*.pt file")
    ap.add_argument("--to", required=True, choices=sorted(PRESETS), help="target preset")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--weights", choices=["ema", "model"], default="ema",
                    help="which weights of a run checkpoint to grow (default: ema)")
    ap.add_argument("--noise", type=float, default=0.1,
                    help="symmetry-breaking noise as a fraction of each weight block's std (default: 0.1)")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--check", type=int, default=2,
                    help="random 128-token sequences on which to compare the two models' logits (0: skip)")
    args = ap.parse_args(argv)

    sd, src, prov = load_source(args.src, args.weights)
    dst = dataclasses.replace(PRESETS[args.to], vocab_size=src.vocab_size, max_len=src.max_len)
    k, after = plan(src, dst)
    grown = grow(sd, src, dst, args.noise, args.seed)
    report = {"from": prov, "width_factor": k, "new_blocks_after": after,
              "params": {"before": sum(w.numel() for w in sd.values()),
                         "after": sum(w.numel() for w in grown.values())}}
    if args.check:
        small, big = Denoiser(src).eval(), Denoiser(dst).eval()
        small.load_state_dict({n: w.float() for n, w in sd.items()})
        big.load_state_dict(grown)
        x = torch.randint(0, src.vocab_size, (args.check, 128), generator=torch.Generator().manual_seed(args.seed))
        with torch.no_grad():
            a, b = small(x), big(x)
        report["check"] = {"max_abs_logit_diff": float((a - b).abs().max()),
                           "max_abs_logit": float(a.abs().max()),
                           "same_argmax_share": float((a.argmax(-1) == b.argmax(-1)).float().mean())}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    torch.save({"step": 0, "model": grown, "model_config": dataclasses.asdict(dst),
                "grown_from": prov | {"model_config": dataclasses.asdict(src), "width_factor": k,
                                      "new_blocks_after": after, "noise": args.noise, "seed": args.seed}},
               args.out)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
