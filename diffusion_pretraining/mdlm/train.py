"""Pretrain the Telugu MDLM (stage 1). Logs locally: runs/<run>/metrics.jsonl and TensorBoard.

    uv run python -m mdlm.train --run small768 --preset small-768
    uv run python -m mdlm.train --run debug --preset tiny --total-steps 200 --no-compile

Re-running the same command resumes from the newest complete checkpoint
(runs/<run>/ckpt_{a,b}.pt, written alternately and fsync'ed; see checkpoint.py).
Batches, masks and times are a pure function of (seed, step), so a resumed run
sees the same data it would have seen. Ctrl-C or SIGTERM saves before exiting;
on a laptop, losing mains power saves at once, then every 5 min on battery, and
saves and exits at 15 % battery.

Crash handling: a CUDA out-of-memory error retries the step with half the
micro-batch (evaluation/sampling are skipped instead); non-finite losses skip the
update. Exit codes for a supervisor (deploy/telugu-mdlm-pilot.service): 0 finished
or stopped, 75 restart me (low battery; the new process waits for mains power),
3 diverged (do not restart), anything else crashed (restart).
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import math
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch

from tokenizer import load_default

from .checkpoint import PowerMonitor, load_latest, save_checkpoint, save_snapshot
from .data import TokenMixture, fixed_canvases
from .diffusion import EPS, invalid_bias, nelbo
from .metrics import sample_metrics
from .model import PRESETS, Denoiser
from .sampling import sample

ROOT = Path(__file__).resolve().parents[1]


def _doc(default, text: str):
    if isinstance(default, dict):
        return field(default_factory=lambda: dict(default), metadata={"doc": text})
    return field(default=default, metadata={"doc": text})


@dataclass
class TrainConfig:
    run: str = _doc("debug", "Run name; everything is written to runs/<run>/.")
    preset: str = _doc("tiny", "Model preset from mdlm.model.PRESETS.")
    token_dir: str = _doc(str(ROOT.parent / "pretraining_datasets" / "tokens"),
                          "Directory with <source>/{train,val,test}.bin written by data_prep.build_corpus.")
    weights: dict = _doc({"sangraha": 0.75, "indiccorp": 0.20, "wikipedia": 0.05},
                         "Probability that a training window is drawn from each source.")
    seq_len: int = _doc(512, "Canvas length: tokens per training sequence.")
    batch_size: int = _doc(128, "Sequences per optimizer step (128 x 512 = 65,536 tokens).")
    micro_batch: int = _doc(8, "Sequences per forward/backward pass; gradients are accumulated over "
                               "batch_size / micro_batch passes. 8 keeps ~2.5 GB of the 8 GB GPU free "
                               "(16 is only ~2.5 % faster); halved automatically on out-of-memory.")
    lr: float = _doc(3e-4, "Peak AdamW learning rate.")
    min_lr_ratio: float = _doc(0.1, "Final learning rate as a fraction of lr (end of the cosine decay).")
    warmup_steps: int = _doc(2000, "Linear warm-up from lr/warmup_steps to lr.")
    total_steps: int = _doc(76000, "Optimizer steps; the cosine decay reaches min_lr at this step.")
    weight_decay: float = _doc(0.1, "AdamW decoupled weight decay on all matrices (incl. the tied embedding); "
                                    "none on RMSNorm gains.")
    beta2: float = _doc(0.98, "AdamW beta2 (beta1 = 0.9, eps = 1e-8).")
    grad_clip: float = _doc(1.0, "Global gradient-norm clip.")
    ema_decay: float = _doc(0.9999, "EMA decay of the weights used for evaluation and sampling; warmed up as "
                                    "min(ema_decay, (1 + step) / (10 + step)).")
    seed: int = _doc(0, "Seed for init, batch composition, times and masks.")
    compile: bool = _doc(True, "torch.compile the transformer trunk (the output layer runs eagerly).")
    log_every: int = _doc(20, "Steps between training-loss log records.")
    eval_every: int = _doc(1000, "Steps between validation evaluations (EMA weights).")
    eval_canvases: int = _doc(128, "Fixed validation canvases per source.")
    sample_every: int = _doc(5000, "Steps between sample generations (EMA weights).")
    n_samples: int = _doc(16, "Sequences generated at each sampling point.")
    sample_steps: int = _doc(256, "Denoising steps per generated sequence (ancestral sampler with caching).")
    ckpt_every_min: float = _doc(15.0, "Minutes between checkpoints on mains power.")
    battery_ckpt_min: float = _doc(5.0, "Minutes between checkpoints while running on battery.")
    battery_stop_percent: int = _doc(15, "Save and exit when the battery falls to this level.")
    snapshot_every: int = _doc(5000, "Steps between permanent bf16 EMA snapshots.")
    init_from: str = _doc("", "Weights to start a new run from, e.g. a grown model written by mdlm.grow "
                              "(fresh optimizer, step 0); ignored once the run has a checkpoint of its own.")


def lr_at(step: int, cfg: TrainConfig) -> float:
    if step < cfg.warmup_steps:
        return cfg.lr * (step + 1) / cfg.warmup_steps
    frac = min(1.0, (step - cfg.warmup_steps) / max(1, cfg.total_steps - cfg.warmup_steps))
    return cfg.lr * (cfg.min_lr_ratio + (1 - cfg.min_lr_ratio) * 0.5 * (1 + math.cos(math.pi * frac)))


class _Trunk:
    """nelbo() calls .hidden (compiled: fixed shapes) and .logits (eager: one row per masked token)."""
    def __init__(self, model: Denoiser, hidden):
        self.hidden, self.logits = hidden, model.logits


@torch.no_grad()
def evaluate(model: Denoiser, val: dict[str, torch.Tensor], mask_id: int, bias: torch.Tensor,
             micro: int, device) -> dict:
    """Val NELBO per source on fixed canvases with fixed times and masks, CE by mask-rate
    bin, and masked-token accuracy at 15/50/85 % masking."""
    model.eval()
    out, bins_ce, bins_n = {}, torch.zeros(10), torch.zeros(10)
    acc = {r: [0, 0] for r in (0.15, 0.5, 0.85)}
    for src, canvases in val.items():
        total, count = 0.0, 0
        for i, x in enumerate(canvases.split(micro)):
            x = x.to(device)
            g = torch.Generator(device).manual_seed(1000 + i)
            t = EPS + (1 - EPS) * (torch.arange(len(x), device=device) + 0.5) / len(x)
            with torch.autocast(device.type, dtype=torch.bfloat16):
                r = nelbo(model, x, mask_id, bias, t=t, generator=g)
            total += float(r["loss"]) * x.numel()
            count += x.numel()
            b = (r["t"] * 10).long().clamp(max=9).cpu()
            bins_ce.index_add_(0, b, r["ce"].cpu())
            bins_n.index_add_(0, b, torch.ones_like(r["ce"].cpu()))
            if i == 0:
                for rate in acc:
                    with torch.autocast(device.type, dtype=torch.bfloat16):
                        rr = nelbo(model, x, mask_id, bias, t=torch.full((len(x),), rate, device=device),
                                   generator=torch.Generator(device).manual_seed(7))
                    acc[rate][0] += int(rr["correct"].sum())
                    acc[rate][1] += rr["correct"].numel()
        out[f"val_nelbo/{src}"] = total / count
        out[f"val_ppl_bound/{src}"] = math.exp(min(total / count, 50))
    tot = sum(v.numel() for v in val.values())
    out["val_nelbo"] = sum(out[f"val_nelbo/{s}"] * v.numel() for s, v in val.items()) / tot
    out["val_ppl_bound"] = math.exp(min(out["val_nelbo"], 50))
    for k in range(10):
        if bins_n[k]:
            out[f"val_ce_by_t/{k / 10:.1f}-{(k + 1) / 10:.1f}"] = float(bins_ce[k] / bins_n[k])
    for rate, (c, n) in acc.items():
        out[f"masked_acc/{int(rate * 100)}pct"] = c / max(1, n)
    model.train()
    return out


def _known_words(token_dir: Path, tok, max_tokens: int = 20_000_000) -> set[str]:
    """Words attested in the validation split (cached): the reference for known_word_share."""
    cache = token_dir / "val_words.txt"
    if cache.exists():
        return set(cache.read_text(encoding="utf-8").split("\n"))
    words = set()
    for f in sorted(token_dir.glob("*/val.bin")):
        arr = np.memmap(f, dtype=np.uint16, mode="r")[:max_tokens]
        for chunk in range(0, len(arr), 1_000_000):
            words.update(tok.decode(arr[chunk:chunk + 1_000_000].tolist()).split())
    cache.write_text("\n".join(sorted(words)), encoding="utf-8")
    return words


def _state(model, ema, opt, step: int, cfg: TrainConfig) -> dict:
    return {"model": model.state_dict(), "ema": ema.state_dict(), "opt": opt.state_dict(),
            "step": step, "config": dataclasses.asdict(cfg), "model_config": dataclasses.asdict(model.cfg)}


def _truncate_log(path: Path, step: int) -> None:
    """Drop records logged after the checkpoint being resumed (they will be redone)."""
    if not path.exists():
        return
    keep = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln and json.loads(ln)["step"] <= step]
    path.write_text("".join(ln + "\n" for ln in keep), encoding="utf-8")


EXIT_RESTART, EXIT_DIVERGED = 75, 3
MAX_BAD_STEPS = 100


def accumulate_step(trunk, model, x: torch.Tensor, micro: int, mask_id: int, bias: torch.Tensor,
                    seed: int, device) -> tuple[torch.Tensor, int]:
    """Forward and backward over ``x`` in micro-batches, gradients accumulated as the mean.
    On CUDA out-of-memory the partial gradients are cleared and the whole step is retried
    with half the micro-batch. Returns (mean loss, micro-batch used)."""
    while True:
        out = loss_sum = None
        try:
            g = torch.Generator(device).manual_seed(seed)
            chunks = x.split(micro)
            loss_sum = torch.zeros((), device=device)
            for mb in chunks:
                with torch.autocast(device.type, dtype=torch.bfloat16, enabled=device.type == "cuda"):
                    out = nelbo(trunk, mb, mask_id, bias, generator=g)
                (out["loss"] / len(chunks)).backward()
                loss_sum += out["loss"].detach() / len(chunks)
            return loss_sum, micro
        except torch.OutOfMemoryError:
            if micro == 1:
                raise
        out = loss_sum = None                     # outside the handler, so the tensors can be freed
        model.zero_grad(set_to_none=True)
        torch.cuda.empty_cache()
        micro //= 2
        print(f"CUDA out of memory: retrying the step with micro-batch {micro}", flush=True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in dataclasses.fields(TrainConfig):
        if f.name in ("weights", "compile"):
            continue
        ap.add_argument(f"--{f.name.replace('_', '-')}", type=type(f.default) if f.default is not None else str, default=None)
    ap.add_argument("--weights", type=json.loads, default=None, help='e.g. \'{"sangraha": 0.7, "wikipedia": 0.3}\'')
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args(argv)

    cfg = TrainConfig(**{k: v for k, v in vars(args).items() if v is not None and k != "no_compile"})
    if args.no_compile:
        cfg.compile = False
    run_dir = ROOT / "runs" / cfg.run
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "samples").mkdir(exist_ok=True)

    power = PowerMonitor()
    while power.on_mains() is False and (power.battery_percent() or 100) <= cfg.battery_stop_percent + 5:
        print("on low battery: waiting for mains power before starting", flush=True)
        time.sleep(60)

    torch.manual_seed(cfg.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    device = torch.device("cuda")
    tok = load_default()
    mask_id = tok.special_to_id["<mask>"]
    mcfg = dataclasses.replace(PRESETS[cfg.preset], vocab_size=tok.vocab_size, max_len=cfg.seq_len)
    model = Denoiser(mcfg).to(device)
    ema = copy.deepcopy(model).requires_grad_(False)
    decay = [p for n, p in model.named_parameters() if p.dim() >= 2]
    no_decay = [p for n, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                             {"params": no_decay, "weight_decay": 0.0}],
                            lr=cfg.lr, betas=(0.9, cfg.beta2), fused=True)
    step = 0
    state = load_latest(run_dir, device)
    if state is not None:
        model.load_state_dict(state["model"])
        ema.load_state_dict(state["ema"])
        opt.load_state_dict(state["opt"])
        step = state["step"]
        del state
        _truncate_log(run_dir / "metrics.jsonl", step)
        print(f"resumed from step {step}", flush=True)
    elif cfg.init_from:
        init = torch.load(cfg.init_from, map_location=device, weights_only=False)
        model.load_state_dict(init["model"])
        ema.load_state_dict(init["model"])
        del init
        print(f"initialised from {cfg.init_from}", flush=True)
    (run_dir / "config.json").write_text(json.dumps({"train": dataclasses.asdict(cfg), "model": dataclasses.asdict(mcfg),
                                                     "params_non_embedding": model.num_params(),
                                                     "params_total": model.num_params(False)}, indent=2))
    from .describe import model_card                      # imported here: describe imports this module
    meta_path = Path(cfg.token_dir) / "meta.json"
    corpus_meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None
    (run_dir / "MODEL_CARD.md").write_text(model_card(mcfg, cfg, corpus_meta), encoding="utf-8")
    bias = invalid_bias(mcfg.padded_vocab, tok.vocab_size, [mask_id, tok.pad_id, tok.unk_id], device)
    data = TokenMixture(Path(cfg.token_dir), cfg.weights, "train", cfg.seq_len)
    val = {s: fixed_canvases(Path(cfg.token_dir), s, "val", cfg.eval_canvases, cfg.seq_len) for s in data.sources}
    known = _known_words(Path(cfg.token_dir), tok)
    hidden = torch.compile(model.hidden) if cfg.compile else model.hidden
    trunk = _Trunk(model, hidden)
    print(f"{cfg.preset}: {model.num_params() / 1e6:.1f}M non-embedding params; train tokens {data.tokens()}", flush=True)

    from torch.utils.tensorboard import SummaryWriter
    writer = SummaryWriter(str(run_dir / "tb"), purge_step=step or None)
    log = (run_dir / "metrics.jsonl").open("a", encoding="utf-8")

    def emit(rec: dict) -> None:
        rec = {"step": step, **rec}
        log.write(json.dumps(rec) + "\n")
        log.flush()
        for k, v in rec.items():
            if k != "step" and isinstance(v, (int, float)):
                writer.add_scalar(k, v, step)

    stop = {"flag": False}
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.update(flag=True))

    def checkpoint(reason: str) -> None:
        nonlocal last_ckpt
        try:
            slot = save_checkpoint(run_dir, _state(model, ema, opt, step, cfg))
            last_ckpt = time.time()
            print(f"checkpoint at step {step} -> {slot.name} ({reason})", flush=True)
        except OSError as exc:                                  # e.g. disk full: retry in a minute
            last_ckpt = time.time() - cfg.ckpt_every_min * 60 + 60
            print(f"CHECKPOINT FAILED at step {step} ({reason}): {exc}", flush=True)

    def guarded(what: str, fn) -> None:
        """Evaluation, sampling and snapshots must never kill the run."""
        failed = False
        try:
            fn()
        except (torch.OutOfMemoryError, OSError) as exc:
            failed, msg = True, f"{type(exc).__name__}: {exc}"
        if failed:
            torch.cuda.empty_cache()
            print(f"skipped {what} at step {step}: {msg[:200]}", flush=True)

    def do_eval() -> None:
        emit(evaluate(ema, val, mask_id, bias, micro, device))

    def do_sample() -> None:
        gen = torch.Generator(device).manual_seed(step)
        ids, nfe = sample(ema, cfg.n_samples, cfg.seq_len, cfg.sample_steps, mask_id, bias, generator=gen)
        ids = ids.tolist()
        texts = [tok.decode(s) for s in ids]
        emit({f"sample/{k}": v for k, v in sample_metrics(texts, ids, tok, known).items()} | {"sample/nfe": nfe})
        (run_dir / "samples" / f"step_{step:07d}.txt").write_text(
            "\n\n==========\n\n".join(tok.decode(s, skip_special=False) for s in ids), encoding="utf-8")

    on_battery, last_power_check, exit_code, bad_steps = False, 0.0, 0, 0
    micro = cfg.micro_batch
    last_ckpt, t_log, tokens_since = time.time(), time.time(), 0
    model.train()
    while step < cfg.total_steps and not stop["flag"]:
        for grp in opt.param_groups:
            grp["lr"] = lr_at(step, cfg)
        x = data.batch(step, cfg.batch_size, cfg.seed).pin_memory().to(device, non_blocking=True)
        loss_sum, micro = accumulate_step(trunk, model, x, micro, mask_id, bias, cfg.seed * 1_000_003 + step, device)
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        if torch.isfinite(loss_sum) and torch.isfinite(grad_norm):
            opt.step()
            bad_steps = 0
        else:                                                   # skip the update, keep the weights finite
            bad_steps += 1
            print(f"non-finite loss or gradient at step {step}: update skipped ({bad_steps} in a row)", flush=True)
            if bad_steps >= MAX_BAD_STEPS:
                print("training diverged: stopping without saving (the last checkpoint is intact)", flush=True)
                return EXIT_DIVERGED
        opt.zero_grad(set_to_none=True)
        with torch.no_grad():
            d = min(cfg.ema_decay, (1 + step) / (10 + step))
            torch._foreach_lerp_(list(ema.parameters()), list(model.parameters()), 1 - d)
        step += 1
        tokens_since += x.numel()

        if step % cfg.log_every == 0:
            dt = time.time() - t_log
            emit({"loss": float(loss_sum), "lr": lr_at(step, cfg), "grad_norm": float(grad_norm),
                  "tokens_per_s": tokens_since / dt, "gpu_mem_gb": torch.cuda.max_memory_allocated() / 2**30})
            print(f"step {step} loss {float(loss_sum):.4f} lr {lr_at(step, cfg):.2e} "
                  f"{tokens_since / dt:,.0f} tok/s", flush=True)
            t_log, tokens_since = time.time(), 0
        if step % cfg.eval_every == 0 or step == cfg.total_steps:
            guarded("evaluation", do_eval)
        if step % cfg.sample_every == 0 or step == cfg.total_steps:
            guarded("sampling", do_sample)
        if step % cfg.snapshot_every == 0:
            guarded("snapshot", lambda: save_snapshot(run_dir, ema, step))
        now = time.time()
        if now - last_power_check > 30:
            last_power_check = now
            mains = power.on_mains()
            if mains is False and not on_battery:
                on_battery = True
                checkpoint("mains power lost")
            elif mains and on_battery:
                on_battery = False
                print("mains power back", flush=True)
            battery = power.battery_percent()
            if on_battery and battery is not None and battery <= cfg.battery_stop_percent:
                print(f"battery at {battery}%: saving and stopping (the supervisor restarts on mains power)", flush=True)
                exit_code = EXIT_RESTART
                break
        if now - last_ckpt > (cfg.battery_ckpt_min if on_battery else cfg.ckpt_every_min) * 60:
            checkpoint("on battery" if on_battery else "periodic")

    checkpoint("stopped" if stop["flag"] else "end of run" if step >= cfg.total_steps else "low battery")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
