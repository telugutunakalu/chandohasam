"""Training throughput and peak GPU memory of each model preset on this GPU.

    uv run python -m mdlm.benchmark --presets small-512 small-768 --micro-batch 8 16 --steps 20

Runs forward + backward + AdamW on random 512-token batches (the full MDLM loss,
masked-position logits included) and reports tokens/s, peak memory, tokens/day
and model FLOPs utilisation against the measured bf16 matmul peak.
"""
from __future__ import annotations

import argparse
import dataclasses
import time

import torch

from .diffusion import invalid_bias, nelbo
from .model import PRESETS, Denoiser
from .train import _Trunk

V, MASK = 45591, 4


def matmul_peak_tflops() -> float:
    x = torch.randn(4096, 4096, device="cuda", dtype=torch.bfloat16)
    for _ in range(3):
        x @ x
    torch.cuda.synchronize()
    t0 = time.time()
    for _ in range(30):
        x @ x
    torch.cuda.synchronize()
    return 2 * 4096 ** 3 * 30 / (time.time() - t0) / 1e12


def run(preset: str, micro: int, steps: int, compile_: bool, seq: int = 512) -> dict:
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    cfg = dataclasses.replace(PRESETS[preset], vocab_size=V, max_len=seq)
    model = Denoiser(cfg).cuda()
    opt = torch.optim.AdamW(model.parameters(), lr=1e-4, fused=True)
    trunk = _Trunk(model, torch.compile(model.hidden) if compile_ else model.hidden)
    bias = invalid_bias(cfg.padded_vocab, V, [MASK, 0, 1], "cuda")
    x = torch.randint(10, V, (micro, seq), device="cuda")
    try:
        for i in range(steps + 5):
            if i == 5:
                torch.cuda.synchronize()
                t0 = time.time()
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = nelbo(trunk, x, MASK, bias)
            out["loss"].backward()
            opt.step()
            opt.zero_grad(set_to_none=True)
        torch.cuda.synchronize()
    except torch.OutOfMemoryError:
        return {"preset": preset, "micro_batch": micro, "status": "out of memory"}
    tok_s = steps * micro * seq / (time.time() - t0)
    n = model.num_params()
    # 6N per token for the trunk, the tied output layer on ~half the positions, and attention
    flops_tok = 6 * n + 6 * cfg.d_model * cfg.padded_vocab * 0.5 + 12 * cfg.n_layers * cfg.d_model * seq
    return {"preset": preset, "micro_batch": micro, "params_M": round(n / 1e6, 1), "tokens_per_s": round(tok_s),
            "tokens_per_day_B": round(tok_s * 86400 / 1e9, 2), "peak_mem_GB": round(torch.cuda.max_memory_allocated() / 2**30, 2),
            "model_tflops": round(tok_s * flops_tok / 1e12, 1)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--presets", nargs="+", default=["small-512", "small-768"])
    ap.add_argument("--micro-batch", nargs="+", type=int, default=[8, 16])
    ap.add_argument("--steps", type=int, default=20)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args(argv)
    peak = matmul_peak_tflops()
    print(f"bf16 matmul peak: {peak:.1f} TFLOPS", flush=True)
    for p in args.presets:
        for mb in args.micro_batch:
            r = run(p, mb, args.steps, not args.no_compile)
            if "model_tflops" in r:
                r["mfu"] = f"{100 * r['model_tflops'] / peak:.0f}%"
            print(r, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
