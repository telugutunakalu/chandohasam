"""E2: fine-tune on the poem corpus, starting from the stage-1 model or from random weights.

    ../.venv/bin/python finetune.py --run e2_pretrained --init pilot
    ../.venv/bin/python finetune.py --run e2_scratch --init scratch

Both runs share everything except the initial weights: preset (small-768), data order, masks,
steps, batch and learning-rate schedule (all a pure function of the seed and the step). The gap
between their verse NELBO at equal steps is what stage 1 buys.

Training reuses stage 1's code unchanged (`mdlm`):
- 512-token windows from data/tokens/poems/train.bin (`TokenMixture`; a window spans several poems);
- the NELBO objective (`accumulate_step`) with bf16 autocast;
- AdamW as in stage 1 (β = (0.9, 0.98), weight decay 0.1 on matrices, clip 1.0);
- the linear warm-up then cosine schedule (`lr_at`);
- EMA weights for evaluation, with stage 1's warm-up, min(0.9999, (1 + step) / (10 + step));
- fixed-mask evaluation (`evaluate`) on the val split of the poems, and of their bhavams, to watch
  how much prose ability the fine-tuning costs.

The GB10 shares memory with the vLLM server: training waits for MIN_FREE_GB before starting and
saves and exits if available memory falls below STOP_FREE_GB. Re-running the command resumes.

Writes runs/<run>/ (gitignored): config.json, metrics.jsonl, last.pt (resume), final.pt, samples.txt;
and results/<run>.json (the evaluation curve, numbers only).
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import time

import torch

from common import HERE, RUNS, TOKENS, load_pilot, mem_available_gb, output_bias, pilot_config, special_ids, \
    tokenizer, wait_for_memory
from mdlm.data import TokenMixture, fixed_canvases
from mdlm.model import Denoiser
from mdlm.sampling import sample
from mdlm.train import TrainConfig, _Trunk, accumulate_step, evaluate, lr_at

MIN_FREE_GB, STOP_FREE_GB = 12, 5         # a run takes ~11 GB; CUDA on the GB10 sees ~MemFree (common.cuda_free_gb)


class Tempered:
    """The sampler's view of a Denoiser whose logits are divided by a temperature (as in mdlm.final_eval)."""

    def __init__(self, model, temperature: float):
        self.model, self.temperature = model, temperature

    def hidden(self, x):
        return self.model.hidden(x)

    def logits(self, h):
        return self.model.logits(h) / self.temperature


def save(path, model, ema, opt, step, args) -> None:
    tmp = path.with_suffix(".tmp")
    torch.save({"model": model.state_dict(), "ema": ema.state_dict(), "opt": opt.state_dict(), "step": step,
                "args": vars(args), "model_config": dataclasses.asdict(model.cfg)}, tmp)
    tmp.replace(path)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--init", required=True, choices=("pilot", "scratch"))
    ap.add_argument("--source", default="poems", help="token source under data/tokens: poems, or poems_tagged (E5)")
    ap.add_argument("--epochs", type=float, default=5.0, help="passes over the poem train split")
    ap.add_argument("--steps", type=int, default=None, help="optimizer steps (overrides --epochs; E5 matches E2's compute)")
    ap.add_argument("--batch", type=int, default=128, help="sequences per optimizer step (x 512 tokens)")
    ap.add_argument("--micro", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--min-lr-ratio", type=float, default=0.1)
    ap.add_argument("--eval-every", type=int, default=100)
    ap.add_argument("--eval-canvases", type=int, default=256)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--no-compile", action="store_true")
    ap.add_argument("--duty", type=float, default=1.0,
                    help="share of wall-clock time the run keeps the GPU busy; below 1 it sleeps after each step, "
                         "busy * (1/duty - 1), to leave the GPU to another job (E5b ran at 0.1 beside the 523M)")
    args = ap.parse_args(argv)

    run_dir = RUNS / args.run
    run_dir.mkdir(parents=True, exist_ok=True)
    wait_for_memory(MIN_FREE_GB, args.run)
    torch.manual_seed(args.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    device = torch.device("cuda")
    tok = tokenizer()
    mask_id = special_ids(tok)["mask"]

    data = TokenMixture(TOKENS, {args.source: 1.0}, "train", 512)
    tokens_per_step = args.batch * 512
    train_tokens = data.tokens()[args.source]
    total_steps = args.steps or round(args.epochs * train_tokens / tokens_per_step)
    sched = TrainConfig(lr=args.lr, warmup_steps=args.warmup, total_steps=total_steps, min_lr_ratio=args.min_lr_ratio)

    model = load_pilot(device) if args.init == "pilot" else Denoiser(pilot_config()).to(device)
    ema = copy.deepcopy(model).requires_grad_(False)
    decay = [p for p in model.parameters() if p.dim() >= 2]
    no_decay = [p for p in model.parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1}, {"params": no_decay, "weight_decay": 0.0}],
                            lr=args.lr, betas=(0.9, 0.98), fused=True)
    step = 0
    last = run_dir / "last.pt"
    if last.exists():
        state = torch.load(last, map_location=device, weights_only=False)
        model.load_state_dict(state["model"])
        ema.load_state_dict(state["ema"])
        opt.load_state_dict(state["opt"])
        step = state["step"]
        del state
        print(f"resumed from step {step}", flush=True)
    bias = output_bias(model.cfg, tok, device)
    val = {s: fixed_canvases(TOKENS, s, "val", args.eval_canvases, 512) for s in dict.fromkeys((args.source, "poems", "bhavam"))}
    trunk = _Trunk(model, model.hidden if args.no_compile else torch.compile(model.hidden))
    (run_dir / "config.json").write_text(json.dumps({"args": vars(args), "total_steps": total_steps,
                                                     "tokens_per_step": tokens_per_step,
                                                     "train_tokens": train_tokens}, indent=2))
    log = (run_dir / "metrics.jsonl").open("a", encoding="utf-8")
    curve_path = HERE / "results" / f"{args.run}.json"
    curve = json.loads(curve_path.read_text()) if curve_path.exists() and step else {"run": args.run, "eval": []}
    curve.update(init=args.init, total_steps=total_steps, tokens_per_step=tokens_per_step, args=vars(args))

    def do_eval() -> None:
        try:
            res = evaluate(ema, val, mask_id, bias, args.micro, device)
        except torch.OutOfMemoryError:                    # an evaluation must never kill the run (as in stage 1)
            torch.cuda.empty_cache()
            print(f"step {step}: evaluation skipped (CUDA out of memory)", flush=True)
            return
        rec = {"step": step, "epoch": step * tokens_per_step / train_tokens, **res}
        log.write(json.dumps({"eval": rec}) + "\n")
        log.flush()
        curve["eval"] = [e for e in curve["eval"] if e["step"] != step] + [rec]
        curve_path.parent.mkdir(exist_ok=True)
        curve_path.write_text(json.dumps(curve, indent=2))
        print(f"step {step} eval: poems {res['val_nelbo/poems']:.4f}  bhavam {res['val_nelbo/bhavam']:.4f}", flush=True)

    print(f"{args.run}: init {args.init}, {total_steps} steps x {tokens_per_step:,} tokens "
          f"({args.epochs} epochs of {train_tokens:,})", flush=True)
    if step == 0:
        do_eval()
    model.train()
    micro, t_log, tokens_since = args.micro, time.time(), 0
    while step < total_steps:
        t_step = time.time()
        if mem_available_gb() < STOP_FREE_GB:
            save(last, model, ema, opt, step, args)
            print(f"only {mem_available_gb():.1f} GB available: saved at step {step} and stopped", flush=True)
            return 75
        for grp in opt.param_groups:
            grp["lr"] = lr_at(step, sched)
        x = data.batch(step, args.batch, args.seed).pin_memory().to(device, non_blocking=True)
        loss, micro = accumulate_step(trunk, model, x, micro, mask_id, bias, args.seed * 1_000_003 + step, device)
        gnorm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        if torch.isfinite(loss) and torch.isfinite(gnorm):
            opt.step()
        opt.zero_grad(set_to_none=True)
        with torch.no_grad():
            d = min(0.9999, (1 + step) / (10 + step))
            torch._foreach_lerp_(list(ema.parameters()), list(model.parameters()), 1 - d)
        step += 1
        tokens_since += x.numel()
        if args.duty < 1:                                 # share the GPU: idle for (1/duty - 1) x the busy time
            torch.cuda.synchronize()
            time.sleep((time.time() - t_step) * (1 / args.duty - 1))
        if step % 20 == 0:
            dt = time.time() - t_log
            log.write(json.dumps({"step": step, "loss": float(loss), "lr": lr_at(step, sched),
                                  "grad_norm": float(gnorm), "tokens_per_s": tokens_since / dt}) + "\n")
            log.flush()
            print(f"step {step} loss {float(loss):.4f} lr {lr_at(step, sched):.2e} {tokens_since / dt:,.0f} tok/s",
                  flush=True)
            t_log, tokens_since = time.time(), 0
        if step % args.eval_every == 0 or step == total_steps:
            do_eval()
        if step % 500 == 0:
            save(last, model, ema, opt, step, args)
    save(run_dir / "final.pt", model, ema, opt, step, args)
    gen = torch.Generator(device).manual_seed(args.seed)
    ids, _ = sample(Tempered(ema, 0.9), 16, 512, 512, mask_id, bias, generator=gen)
    (run_dir / "samples.txt").write_text("\n\n==========\n\n".join(tok.decode(s, skip_special=False)
                                                                  for s in ids.tolist()), encoding="utf-8")
    print(f"done: {run_dir / 'final.pt'}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
