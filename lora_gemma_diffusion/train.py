"""LoRA training of DiffusionGemma on the T1 task (PLAN.md §2).

    ../.venv/bin/python -u train.py --run smoke --max-steps 200 --eval-every 50          # gate 3
    ../.venv/bin/python -u train.py --run lora-r16 --epochs 1                             # the full run
    ../.venv/bin/python -u train.py --run lora-full --data train_full --batch 2 --epochs 1   # the whole pool

`--batch` examples per forward (prompts left-padded: common.encode_batch; the default 1 is the 48k run's recipe),
`--accum` examples per optimizer step; within a step the examples are grouped by prompt length (less padding). Each example: t ~ U(0, 1), uniform-noise corruption of the canvas at rate t, self-conditioning (a first
no-gradient pass) with probability 0.5 (per forward: for a whole batch or not), cross-entropy of the clean canvas at
every position. AdamW on the LoRA
parameters only (rank --r, α --alpha, q/k/v/o, one adapter per tied encoder/decoder pair), linear warm-up then cosine
to 10%; gradient clipping 1.0; decoder gradient checkpointing; bf16 autocast.

Validation every --eval-every optimizer steps (and at 0 and the end): the val poems of data/val.pt (first --val-n) at
t = 0.25, 0.5, 0.75, without self-conditioning, fixed noise per poem and t; loss on the poem positions and on all.

Checkpoints: runs/<run>/last.pt (LoRA, optimizer, step, position in the shuffled data) every --save-every steps,
at the end and on SIGTERM; a resumed run continues exactly. The final adapter: runs/<run>/lora.pt; --snapshot-at keeps
the adapter at chosen steps too (the 48k run: step 3,000 = the first 24k examples).
Logs: runs/<run>.log (stdout), runs/<run>/metrics.jsonl.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import signal

import numpy as np
import torch

import common as C


def lr_at(step: int, total: int, peak: float, warmup: int) -> float:
    if step < warmup:
        return peak * (step + 1) / warmup
    p = (step - warmup) / max(1, total - warmup)
    return peak * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, p))))


@torch.no_grad()
def evaluate(model, val: list[dict]) -> dict:
    model.eval()
    out = {}
    for t in (0.25, 0.5, 0.75):
        poem, allp = [], []
        for k, e in enumerate(val):
            g = torch.Generator(device="cuda").manual_seed(10_000 + k)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                ce = C.diffusion_loss(model, torch.tensor([e["prompt"]], device="cuda"),
                                      torch.tensor([e["canvas"]], device="cuda"), t, False, g, reduce=False)[0]
            poem.append(float(ce[:e["n_poem"]].mean()))
            allp.append(float(ce.mean()))
        out[f"val_poem/t{t}"], out[f"val_all/t{t}"] = float(np.mean(poem)), float(np.mean(allp))
    model.train()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=float, default=32)
    ap.add_argument("--accum", type=int, default=8, help="examples per optimizer step")
    ap.add_argument("--batch", type=int, default=1, help="examples per forward (divides --accum)")
    ap.add_argument("--data", default="train", help="data/<name>.pt (train: 48k E6-weighted; train_full: the pool)")
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--warmup", type=int, default=30)
    ap.add_argument("--eval-every", type=int, default=100)
    ap.add_argument("--save-every", type=int, default=50)
    ap.add_argument("--snapshot-at", type=int, nargs="*", default=[],
                    help="also keep the adapter at these steps (runs/<run>/lora_step_<N>.pt)")
    ap.add_argument("--val-n", type=int, default=48)
    ap.add_argument("--self-cond", type=float, default=0.5)
    ap.add_argument("--seed", type=int, default=20261020)
    args = ap.parse_args()
    assert args.accum % args.batch == 0, "--batch must divide --accum"
    run = C.RUNS / args.run
    run.mkdir(parents=True, exist_ok=True)
    train = torch.load(C.DATA / f"{args.data}.pt")
    val = torch.load(C.DATA / "val.pt")[: args.val_n]
    total = args.max_steps or int(args.epochs * len(train) / args.accum)
    order = np.random.default_rng(args.seed).permutation(len(train)).tolist()
    order = (order * (math.ceil(total * args.accum / len(order)) + 1))[: total * args.accum]

    import psutil
    if psutil.virtual_memory().available / 2**30 > 90 and torch.cuda.mem_get_info()[0] / 2**30 < 80:
        import sys
        sys.path.insert(0, str(C.REPO / "diffusion_pretraining"))
        from mdlm.checkpoint_eval import _evict_large_files
        _evict_large_files()
    model, tok = C.load(resident=True)
    adapters = C.inject_lora(model, r=args.r, alpha=args.alpha)
    params = [p for m in {id(a): a for a in adapters.values()}.values() for p in (m.A, m.B)]
    opt = torch.optim.AdamW(params, lr=args.lr, betas=(0.9, 0.99), weight_decay=0.0)
    step, pos = 0, 0
    if (run / "last.pt").exists():
        st = torch.load(run / "last.pt", map_location="cpu")
        C.load_lora(model, run / "last_lora.pt")
        opt.load_state_dict(st["opt"])
        step, pos = st["step"], st["pos"]
        print(f"resumed at step {step}", flush=True)
    model.gradient_checkpointing_enable()
    model.train()
    (run / "config.json").write_text(json.dumps({**vars(args), "total_steps": total, "train": len(train),
                                                 "lora_params_M": sum(p.numel() for p in params) / 1e6}, indent=1))
    log = open(run / "metrics.jsonl", "a", encoding="utf-8")
    emit = lambda rec: (log.write(json.dumps({"step": step, **rec}) + "\n"), log.flush())
    stop = {"flag": False}
    signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))

    def save(final: bool = False) -> None:
        torch.save(C.lora_state(model), run / "last_lora.pt")
        torch.save({"opt": opt.state_dict(), "step": step, "pos": pos}, run / "last.pt")
        if final:
            torch.save(C.lora_state(model), run / "lora.pt")
        print(f"saved at step {step}{' (final)' if final else ''}", flush=True)

    print(f"run {args.run}: {total} steps × {args.accum} examples ({args.batch} per forward), "
          f"{len(train):,} training examples, "
          f"LoRA r {args.r} ({sum(p.numel() for p in params) / 1e6:.1f}M parameters), lr {args.lr:g}", flush=True)
    if step == 0:
        res = evaluate(model, val)
        emit(res)
        print("eval step 0:", json.dumps({k: round(v, 4) for k, v in res.items()}), flush=True)
    rng = random.Random(args.seed + step)
    tick, losses = C.timer(), []
    while step < total and not stop["flag"]:
        for g_ in opt.param_groups:
            g_["lr"] = lr_at(step, total, args.lr, args.warmup)
        acc = 0.0
        if args.batch == 1:
            for _ in range(args.accum):
                e = train[order[pos]]
                pos += 1
                t = rng.random()
                gen = torch.Generator(device="cuda").manual_seed(args.seed * 7 + pos)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    loss = C.diffusion_loss(model, torch.as_tensor(e["prompt"], device="cuda")[None].long(),
                                            torch.as_tensor(e["canvas"], device="cuda")[None].long(), t,
                                            rng.random() < args.self_cond, gen)
                (loss / args.accum).backward()
                acc += float(loss) / args.accum
        else:
            group = sorted((train[order[pos + k]] for k in range(args.accum)), key=lambda e: len(e["prompt"]))
            pos += args.accum
            for j in range(0, args.accum, args.batch):
                es = group[j:j + args.batch]
                ts = torch.tensor([rng.random() for _ in es])
                gen = torch.Generator(device="cuda").manual_seed(args.seed * 7 + pos + j)
                clean = torch.stack([torch.as_tensor(e["canvas"]) for e in es]).long().cuda()
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    loss = C.diffusion_loss_batch(model, [torch.as_tensor(e["prompt"]).long() for e in es], clean,
                                                  ts, rng.random() < args.self_cond, gen)
                (loss * len(es) / args.accum).backward()
                acc += float(loss) * len(es) / args.accum
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0)
        if torch.isfinite(gn):
            opt.step()
        else:
            print(f"non-finite gradient at step {step}: update skipped", flush=True)
        opt.zero_grad(set_to_none=True)
        step += 1
        losses.append(acc)
        if step % 10 == 0:
            dt = tick()
            emit({"loss": float(np.mean(losses)), "lr": opt.param_groups[0]["lr"], "grad_norm": float(gn),
                  "s_per_step": dt / 10, "gpu_gb": torch.cuda.max_memory_allocated() / 1e9})
            print(f"step {step}/{total} loss {np.mean(losses):.4f} lr {opt.param_groups[0]['lr']:.2e} "
                  f"{dt / 10:.1f} s/step, ETA {(total - step) * dt / 10 / 3600:.1f} h, "
                  f"peak {torch.cuda.max_memory_allocated() / 1e9:.0f} GB", flush=True)
            tick, losses = C.timer(), []
        if step % args.eval_every == 0 or step == total:
            res = evaluate(model, val)
            emit(res)
            print(f"eval step {step}:", json.dumps({k: round(v, 4) for k, v in res.items()}), flush=True)
        if step % args.save_every == 0:
            save()
        if step in args.snapshot_at:
            torch.save(C.lora_state(model), run / f"lora_step_{step}.pt")
            print(f"snapshot: adapter at step {step} ({step * args.accum:,} examples)", flush=True)
    save(final=step >= total)
    print("stopped" if stop["flag"] else "end of run", flush=True)


if __name__ == "__main__":
    main()
