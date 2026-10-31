"""Phase 0 speed test (../full_grid_experiments/README.md, Phase 0 and decision 11, lever ①): examples per forward for the whole-pool LoRA.

    ../.venv/bin/python -u speed_batch.py            # → runs/speed_batch.json (≈ 5 min with the GPU to itself)

1. **Gate:** 4 training examples, no gradient, bf16: the logits of one batched forward (common.encode_batch, prompts
   left-padded) against four single forwards (common.encode). Passes when every example's cross-entropy differs by
   less than 0.01 nats (bf16 kernels with other shapes differ slightly; a masking error gives ≫ 0.1, the CPU check of
   a tiny model gave exactly 0).
2. **Speed:** for --batch 1, 2, 4 (those whose gate passed): the training step of train.py (LoRA r 16, decoder gradient
   checkpointing, self-conditioning on every other forward) over 1 warm-up and 4 timed optimizer steps of 8
   examples; seconds per example and peak memory. A size that runs out of memory is recorded and the larger skipped.
`best` = the fastest size that passed; train.py's --batch takes it.
"""
from __future__ import annotations

import json
import time

import numpy as np
import torch

import common as C


def main() -> None:
    data = C.DATA / ("train_full.pt" if (C.DATA / "train_full.pt").exists() else "train.pt")
    train = torch.load(data)
    order = np.random.default_rng(7).permutation(len(train))[:64].tolist()
    ex = [train[i] for i in order]
    del train
    model, tok = C.load(resident=True)
    adapters = C.inject_lora(model, r=16, alpha=32)
    params = [p for m in {id(a): a for a in adapters.values()}.values() for p in (m.A, m.B)]
    for m in {id(a): a for a in adapters.values()}.values():     # a trained-like adapter: B ≠ 0 exercises the LoRA path
        torch.nn.init.normal_(m.B, std=1e-3)
    out = {"data": data.name, "gate": {}, "s_per_example": {}, "peak_gb": {}}

    prompts = [torch.as_tensor(e["prompt"]).long() for e in ex[:4]]
    clean = torch.stack([torch.as_tensor(e["canvas"]) for e in ex[:4]]).long().cuda()
    model.eval()
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        g = torch.Generator(device="cuda").manual_seed(1)
        noisy = C.corrupt(clean, 0.5, model.config.text_config.vocab_size, g)
        batch = C.denoise(model, C.encode_batch(model, prompts), noisy).float()
        diffs = []
        for i, p in enumerate(prompts):
            one = C.denoise(model, C.encode(model, p[None].cuda()), noisy[i:i + 1]).float()
            ce1 = torch.nn.functional.cross_entropy(one[0], clean[i])
            ceb = torch.nn.functional.cross_entropy(batch[i], clean[i])
            diffs.append(abs(float(ce1 - ceb)))
            out["gate"][f"example_{i}"] = {"prompt_tokens": len(p), "ce_single": float(ce1), "ce_batch": float(ceb),
                                           "max_abs_logit_diff": float((one[0] - batch[i]).abs().max())}
    passed = max(diffs) < 0.01
    out["gate"]["passed"] = passed
    print(f"gate: max |Δ ce| {max(diffs):.4f} nats → {'passed' if passed else 'FAILED'}", flush=True)

    model.gradient_checkpointing_enable()
    model.train()
    opt = torch.optim.AdamW(params, lr=1e-5)
    for b in (1, 2, 4):
        if b > 1 and not passed:
            break
        torch.cuda.reset_peak_memory_stats()
        try:
            times = []
            for step in range(5):
                torch.cuda.synchronize()
                t0 = time.time()
                group = sorted(ex[8 * step: 8 * step + 8], key=lambda e: len(e["prompt"]))
                for j in range(0, 8, b):
                    es = group[j:j + b]
                    ts = torch.full((len(es),), 0.5)
                    gen = torch.Generator(device="cuda").manual_seed(step * 10 + j)
                    cl = torch.stack([torch.as_tensor(e["canvas"]) for e in es]).long().cuda()
                    with torch.autocast("cuda", dtype=torch.bfloat16):
                        loss = C.diffusion_loss_batch(model, [torch.as_tensor(e["prompt"]).long() for e in es], cl,
                                                      ts, (j // b) % 2 == 0, gen)
                    (loss * len(es) / 8).backward()
                opt.step()
                opt.zero_grad(set_to_none=True)
                torch.cuda.synchronize()
                times.append(time.time() - t0)
            out["s_per_example"][b] = float(np.mean(times[1:])) / 8
            out["peak_gb"][b] = torch.cuda.max_memory_allocated() / 1e9
            print(f"batch {b}: {out['s_per_example'][b]:.3f} s per example, peak {out['peak_gb'][b]:.1f} GB",
                  flush=True)
        except torch.cuda.OutOfMemoryError:
            out["peak_gb"][b] = "out of memory"
            print(f"batch {b}: out of memory", flush=True)
            opt.zero_grad(set_to_none=True)
            torch.cuda.empty_cache()
            break
    out["best"] = min(out["s_per_example"], key=out["s_per_example"].get)
    out["speedup"] = out["s_per_example"][1] / out["s_per_example"][out["best"]]
    (C.RUNS / "speed_batch.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"best: --batch {out['best']} ({out['speedup']:.2f}× batch 1)", flush=True)


if __name__ == "__main__":
    main()
