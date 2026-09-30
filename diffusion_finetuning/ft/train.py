"""Fine-tune the Telugu MDLM: Stage 1 (poetic continued pretraining) or Stage 2 (conditional
multi-task SFT). Logs to runs/<run>/metrics.jsonl and TensorBoard, like mdlm.train.

    uv run --project ../diffusion_pretraining python -m ft.train --stage 1 --run s1-pilot120m \\
        --init-from ../diffusion_pretraining/runs/pilot120m
    uv run --project ../diffusion_pretraining python -m ft.train --stage 2 --run s2-pilot120m-lr6e-5 \\
        --init-from runs/s1-pilot120m --lr 6e-5

--init-from takes a run directory (its newest checkpoint's EMA weights), an EMA snapshot
(snapshots/ema_step_*.pt), or a file with a "model" state dict (mdlm.grow output). The
optimizer starts fresh; re-running the same command resumes from the run's own newest
checkpoint instead. Batches, masks and times are a pure function of (seed, step).

Crash handling follows mdlm.train: out-of-memory halves the micro-batch and retries the
step; non-finite losses skip the update; power loss checkpoints at once; exit 75 asks a
supervisor to restart, 3 means diverged.
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch

from mdlm.checkpoint import PowerMonitor, load_latest, save_checkpoint, save_snapshot
from mdlm.data import fixed_canvases
from mdlm.diffusion import EPS, invalid_bias
from mdlm.model import Denoiser, ModelConfig
from mdlm.sampling import sample
from mdlm.train import _Trunk, _truncate_log, evaluate, lr_at
from tokenizer import load_default

from . import DATA_DIR, PRETRAIN_ROOT, RUNS_DIR
from .batches import Stage1Batches, Stage2Batches, group_by_length
from .canvas import DEFAULT_MIX, TARGET, Vocab, build, load_records
from .loss import role_nelbo
from .metres import identify, parse_label
from .text import CLASSICAL, MEANING_KEY, METRE_KEY, POEM_KEY, STYLE_KEY

EXIT_RESTART, EXIT_DIVERGED = 75, 3
MAX_BAD_STEPS = 100
STAGE_DEFAULTS = {
    1: {"lr": 1e-4, "warmup_steps": 200, "epochs": 3.0},
    2: {"lr": 6e-5, "warmup_steps": 100, "epochs": 2.5},
}
PROBE_METRES = ("ఉత్పలమాల", "కందము", "సీసము+తేటగీతి", "ఆటవెలది")


def _doc(default, text: str):
    if isinstance(default, dict):
        return field(default_factory=lambda: dict(default), metadata={"doc": text})
    return field(default=default, metadata={"doc": text})


@dataclass
class FTConfig:
    run: str = _doc("debug", "Run name; everything is written to runs/<run>/.")
    stage: int = _doc(1, "1 = poem + meaning documents (continued pretraining); 2 = conditional multi-task SFT.")
    init_from: str = _doc("", "Run directory, EMA snapshot or 'model' state-dict file to start from.")
    data_dir: str = _doc(str(DATA_DIR), "Output of ft.build_data.")
    token_dir: str = _doc(str(PRETRAIN_ROOT.parent / "pretraining_datasets" / "tokens"),
                          "Pretraining token files, for Stage 1 replay and the general validation canvases.")
    replay: float = _doc(0.15, "Stage 1: share of windows drawn from the general pretraining corpus.")
    replay_weights: dict = _doc({"sangraha": 0.75, "indiccorp": 0.20, "wikipedia": 0.05}, "Replay source mix.")
    mix: dict = _doc(dict(DEFAULT_MIX), "Stage 2 task mix (PLAN §5.1).")
    seq_len: int = _doc(512, "Stage 1 window length; Stage 2 canvases use buckets of 128 / 256 / 384 / 512.")
    batch_size: int = _doc(128, "Sequences per optimizer step.")
    micro_tokens: int = _doc(4096, "Tokens per forward/backward pass (8 x 512); halved on out-of-memory.")
    lr: float = _doc(0.0, "Peak AdamW learning rate (0 = stage default: 1e-4 for Stage 1, 6e-5 for Stage 2).")
    min_lr_ratio: float = _doc(0.1, "Final learning rate as a fraction of lr.")
    warmup_steps: int = _doc(0, "Linear warm-up steps (0 = stage default: 200 / 100).")
    epochs: float = _doc(0.0, "Stage 1: passes over the poem documents; Stage 2: passes over the T1 pool "
                              "(0 = stage default: 3 / 2.5).")
    total_steps: int = _doc(0, "Optimizer steps; 0 = derived from epochs.")
    weight_decay: float = _doc(0.1, "AdamW weight decay on matrices.")
    beta2: float = _doc(0.98, "AdamW beta2.")
    grad_clip: float = _doc(1.0, "Global gradient-norm clip.")
    ema_decay: float = _doc(0.999, "EMA decay (PLAN §4: ~1k-step horizon for runs of a few thousand steps).")
    seed: int = _doc(1, "Seed for batches, times and masks (not 0: the pilot used 0).")
    compile: bool = _doc(True, "torch.compile the transformer trunk.")
    log_every: int = _doc(20, "Steps between training-loss records.")
    eval_every: int = _doc(250, "Steps between validation evaluations (EMA weights).")
    eval_canvases: int = _doc(128, "Validation canvases per source / task.")
    sample_every: int = _doc(500, "Steps between sample generations (EMA weights).")
    n_samples: int = _doc(16, "Samples per sampling point.")
    sample_steps: int = _doc(256, "Denoising steps per sample.")
    ckpt_every_min: float = _doc(15.0, "Minutes between checkpoints on mains power.")
    battery_ckpt_min: float = _doc(5.0, "Minutes between checkpoints on battery.")
    battery_stop_percent: int = _doc(15, "Save and exit at this battery level.")
    snapshot_every: int = _doc(1000, "Steps between permanent bf16 EMA snapshots.")


# -----------------------------------------------------------------------------
# weights
# -----------------------------------------------------------------------------
def load_init(path: str) -> tuple[dict, dict | None, dict]:
    """(state dict, model config or None, provenance)."""
    p = Path(path)
    if p.is_dir():
        st = load_latest(p, "cpu")
        if st is None:
            raise FileNotFoundError(f"no checkpoint in {p}")
        return st["ema"], st.get("model_config"), {"from": str(p), "weights": "ema", "step": st["step"]}
    st = torch.load(p, map_location="cpu", weights_only=False)
    if "model" in st:
        return st["model"], st.get("model_config"), {"from": str(p), "weights": "model", "step": st.get("step")}
    run_dir = p.parent.parent if p.parent.name == "snapshots" else p.parent
    cfg = json.loads((run_dir / "config.json").read_text())["model"]
    return {k: v.float() for k, v in st["ema"].items()}, cfg, {"from": str(p), "weights": "ema", "step": st.get("step")}


# -----------------------------------------------------------------------------
# evaluation
# -----------------------------------------------------------------------------
def _poem_windows(path: Path, n: int, L: int) -> torch.Tensor:
    arr = np.memmap(path, dtype=np.uint16, mode="r")
    n = min(n, len(arr) // L)
    return torch.from_numpy(np.asarray(arr[: n * L], dtype=np.int64).reshape(n, L))


def stage2_val_sets(recs, v: Vocab, n: int) -> dict[str, list]:
    rng = np.random.default_rng(0)
    out = {}
    for task in ("T1", "T0", "T2"):
        rows = []
        for r in recs:
            if len(rows) >= n:
                break
            if task in ("T1", "T0") and not r.metre_ok or task in ("T1", "T2") and r.meaning_line is None:
                continue
            c = build(task, v, r, rng)
            if c is not None:
                rows.append((task, c[0], c[1]))
        out[task] = rows
    return out


@torch.no_grad()
def evaluate_stage2(model, sets: dict[str, list], mask_id: int, bias: torch.Tensor, micro_tokens: int, device) -> dict:
    """Val NELBO per TARGET token (the <eos> fill excluded) with fixed times and masks, and the
    masked-token accuracy of T1 at 50% masking."""
    model.eval()
    out = {}
    for task, rows in sets.items():
        num, den = 0.0, 0
        for i, (_, x, roles) in enumerate(group_by_length(rows, micro_tokens)):
            x, roles = x.to(device), roles.to(device)
            g = torch.Generator(device).manual_seed(1000 + i)
            t = EPS + (1 - EPS) * (torch.arange(len(x), device=device) + 0.5) / len(x)
            with torch.autocast(device.type, dtype=torch.bfloat16):
                r = role_nelbo(model, x, roles, mask_id, bias, t=t, generator=g)
            keep = ~r["fill"]
            num += float((r["ce"][keep] / r["t"][keep]).sum())
            den += r["n_target"]
        out[f"val_nelbo/{task}"] = num / max(1, den)
    correct = total = 0
    for i, (_, x, roles) in enumerate(group_by_length(sets.get("T1", []), micro_tokens)):
        x, roles = x.to(device), roles.to(device)
        with torch.autocast(device.type, dtype=torch.bfloat16):
            r = role_nelbo(model, x, roles, mask_id, bias, t=torch.full((len(x),), 0.5, device=device),
                           generator=torch.Generator(device).manual_seed(7 + i))
        keep = ~r["fill"]
        correct += int(r["correct"][keep].sum())
        total += int(keep.sum())
    out["val_acc50/T1"] = correct / max(1, total)
    model.train()
    return out


def _poem_lines(text: str) -> list[str]:
    """Poem lines of a decoded sample: stop at an empty line or at a header line."""
    out = []
    for ln in text.split("\n"):
        ln = ln.strip()
        if not ln or ln.startswith((MEANING_KEY, METRE_KEY, STYLE_KEY, POEM_KEY)):
            if out:
                break
            continue
        out.append(ln)
    return out


@torch.no_grad()
def probe_samples(model, tok, prompts: list[tuple[str, list[int], int]], length: int, steps: int,
                  mask_id: int, bias: torch.Tensor, seed: int, device) -> tuple[dict, str]:
    """prompts: (catalogue metre label wanted, prefix ids, count). Unconstrained ancestral samples;
    a sample passes when the engine identifies the requested metre in its poem lines."""
    passed = total = 0
    dump = []
    for k, (want, prefix, n) in enumerate(prompts):
        pre = torch.tensor(prefix, device=device).repeat(n, 1)
        g = torch.Generator(device).manual_seed(seed * 1000 + k)
        ids, _ = sample(model, n, length, steps, mask_id, bias, prefix=pre, generator=g)
        for row in ids.tolist():
            gen = row[len(prefix):]
            if tok.eos_id in gen:
                gen = gen[: gen.index(tok.eos_id)]
            lines = _poem_lines(tok.decode(gen))
            allowed, _ = parse_label(want)
            ok = bool(lines) and identify(lines).pick(allowed) is not None
            passed += ok
            total += 1
            dump.append(f"[{want}] {'PASS' if ok else 'fail'}\n" + tok.decode(prefix[1:]) + "\n".join(lines))
    return {"sample/metre_pass": passed / max(1, total)}, "\n\n==========\n\n".join(dump)


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for f in dataclasses.fields(FTConfig):
        if f.name in ("replay_weights", "mix", "compile"):
            continue
        ap.add_argument(f"--{f.name.replace('_', '-')}", type=type(f.default), default=None)
    ap.add_argument("--replay-weights", type=json.loads, default=None)
    ap.add_argument("--mix", type=json.loads, default=None, help='e.g. \'{"T1": 0.7, "T2": 0.3}\'')
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args(argv)
    cfg = FTConfig(**{k: v for k, v in vars(args).items() if v is not None and k != "no_compile"})
    if args.no_compile:
        cfg.compile = False
    for k, v in STAGE_DEFAULTS[cfg.stage].items():
        if not getattr(cfg, k):
            setattr(cfg, k, v)

    run_dir = RUNS_DIR / cfg.run
    (run_dir / "samples").mkdir(parents=True, exist_ok=True)
    data_dir = Path(cfg.data_dir)
    power = PowerMonitor()
    while power.on_mains() is False and (power.battery_percent() or 100) <= cfg.battery_stop_percent + 5:
        print("on low battery: waiting for mains power before starting", flush=True)
        time.sleep(60)

    torch.manual_seed(cfg.seed)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch._dynamo.config.cache_size_limit = 64
    device = torch.device("cuda")
    tok = load_default()
    v = Vocab(tok)
    mask_id = tok.special_to_id["<mask>"]

    state = load_latest(run_dir, "cpu")
    if state is not None:
        mcfg = ModelConfig(**state["model_config"])
    elif cfg.init_from:
        init_sd, init_cfg, provenance = load_init(cfg.init_from)
        mcfg = ModelConfig(**init_cfg)
    else:
        raise SystemExit("a new run needs --init-from")
    model = Denoiser(mcfg).to(device)
    ema = copy.deepcopy(model).requires_grad_(False)
    decay = [p for _, p in model.named_parameters() if p.dim() >= 2]
    no_decay = [p for _, p in model.named_parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                             {"params": no_decay, "weight_decay": 0.0}],
                            lr=cfg.lr, betas=(0.9, cfg.beta2), fused=True)
    step = 0
    if state is not None:
        model.load_state_dict(state["model"])
        ema.load_state_dict(state["ema"])
        opt.load_state_dict(state["opt"])
        step = state["step"]
        provenance = state.get("provenance")
        del state
        _truncate_log(run_dir / "metrics.jsonl", step)
        print(f"resumed from step {step}", flush=True)
    else:
        model.load_state_dict(init_sd)
        ema.load_state_dict(init_sd)
        del init_sd
        print(f"initialised from {provenance}", flush=True)
    bias = invalid_bias(mcfg.padded_vocab, tok.vocab_size, [mask_id, tok.pad_id, tok.unk_id], device)

    # ---- data, validation sets, probes -------------------------------------------------
    if cfg.stage == 1:
        data = Stage1Batches(data_dir, Path(cfg.token_dir), cfg.replay, cfg.replay_weights, cfg.seq_len)
        per_step = cfg.batch_size * cfg.seq_len * (1 - cfg.replay)
        derived = int(round(cfg.epochs * data.poem_tokens() / per_step))
        val = {"poems": _poem_windows(data_dir / "stage1" / "val.bin", cfg.eval_canvases, cfg.seq_len)}
        val |= {s: fixed_canvases(Path(cfg.token_dir), s, "val", cfg.eval_canvases, cfg.seq_len) for s in cfg.replay_weights}
        prompts = []
        for m in PROBE_METRES:
            pre = [tok.bos_id] + tok.encode(f"{METRE_KEY}: {m}\n{STYLE_KEY}: {CLASSICAL}\n{POEM_KEY}:\n")
            prompts.append((m, pre, max(1, cfg.n_samples // len(PROBE_METRES))))
        sample_len = cfg.seq_len
        data_info = {"poem_tokens": data.poem_tokens()}
    else:
        train_recs = load_records(data_dir / "records" / "train.jsonl", v)
        val_recs = load_records(data_dir / "records" / "val.jsonl", v)
        data = Stage2Batches(train_recs, v, cfg.mix)
        derived = int(round(cfg.epochs * data.steps_per_epoch(cfg.batch_size)))
        val_sets = stage2_val_sets(val_recs, v, cfg.eval_canvases)
        prompts = []
        for _, ids, roles in val_sets["T1"][: cfg.n_samples]:
            first = int(np.flatnonzero(roles != 0)[0])
            want = tok.decode(ids[:first].tolist()).split("\n")[0].split(":", 1)[1].strip()
            prompts.append((want, ids[:first].tolist(), 1))
        sample_len = 512
        data_info = {"pools": data.pools.sizes(), "mix": {k: round(float(x), 4) for k, x in data.mix.items()},
                     "steps_per_epoch": data.steps_per_epoch(cfg.batch_size)}
    if not cfg.total_steps:
        cfg.total_steps = max(1, derived)
    (run_dir / "config.json").write_text(json.dumps(
        {"train": dataclasses.asdict(cfg), "model": dataclasses.asdict(mcfg), "init": provenance, "data": data_info},
        indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    hidden = torch.compile(model.hidden) if cfg.compile else model.hidden
    trunk = _Trunk(model, hidden)
    print(f"stage {cfg.stage}: {cfg.total_steps} steps; {data_info}", flush=True)

    from torch.utils.tensorboard import SummaryWriter
    writer = SummaryWriter(str(run_dir / "tb"), purge_step=step or None)
    log = (run_dir / "metrics.jsonl").open("a", encoding="utf-8")

    def emit(rec: dict) -> None:
        rec = {"step": step, **rec}
        log.write(json.dumps(rec) + "\n")
        log.flush()
        for k, val_ in rec.items():
            if k != "step" and isinstance(val_, (int, float)):
                writer.add_scalar(k, val_, step)

    stop = {"flag": False}
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.update(flag=True))

    def checkpoint(reason: str) -> None:
        nonlocal last_ckpt
        try:
            st = {"model": model.state_dict(), "ema": ema.state_dict(), "opt": opt.state_dict(), "step": step,
                  "config": dataclasses.asdict(cfg), "model_config": dataclasses.asdict(mcfg), "provenance": provenance}
            slot = save_checkpoint(run_dir, st)
            last_ckpt = time.time()
            print(f"checkpoint at step {step} -> {slot.name} ({reason})", flush=True)
        except OSError as exc:
            last_ckpt = time.time() - cfg.ckpt_every_min * 60 + 60
            print(f"CHECKPOINT FAILED at step {step} ({reason}): {exc}", flush=True)

    def guarded(what: str, fn) -> None:
        try:
            fn()
        except (torch.OutOfMemoryError, OSError) as exc:
            torch.cuda.empty_cache()
            print(f"skipped {what} at step {step}: {type(exc).__name__}: {str(exc)[:200]}", flush=True)

    def do_eval() -> None:
        if cfg.stage == 1:
            emit(evaluate(ema, val, mask_id, bias, max(1, micro_tokens // cfg.seq_len), device))
        else:
            emit(evaluate_stage2(ema, val_sets, mask_id, bias, micro_tokens, device))

    def do_sample() -> None:
        rec, text = probe_samples(ema, tok, prompts, sample_len, cfg.sample_steps, mask_id, bias, step + 1, device)
        emit(rec)
        (run_dir / "samples" / f"step_{step:07d}.txt").write_text(text, encoding="utf-8")

    def one_step(micro: int) -> tuple[torch.Tensor, dict]:
        """Forward/backward of one optimizer step; returns (mean loss, per-task [sum, count])."""
        g = torch.Generator(device).manual_seed(cfg.seed * 1_000_003 + step)
        per_task: dict[str, list] = {}
        loss_sum = torch.zeros((), device=device)
        if cfg.stage == 1:
            x, roles = data.batch(step, cfg.batch_size, cfg.seed)
            denom = x.numel()
            per = max(1, micro // cfg.seq_len)
            chunks = [("s1", x[i:i + per], roles[i:i + per]) for i in range(0, len(x), per)]
        else:
            examples = data.batch(step, cfg.batch_size, cfg.seed)
            denom = max(1, sum(int((r == TARGET).sum()) for _, _, r in examples))
            chunks = [(tasks, xx, rr) for tasks, xx, rr in group_by_length(examples, micro)]
        for tasks, xx, rr in chunks:
            xx, rr = xx.to(device, non_blocking=True), rr.to(device, non_blocking=True)
            with torch.autocast(device.type, dtype=torch.bfloat16):
                out = role_nelbo(trunk, xx, rr, mask_id, bias, generator=g)
            (out["sum"] / denom).backward()
            loss_sum += out["sum"].detach() / denom
            if cfg.stage == 2:
                rs, rt = out["row_sum"].tolist(), out["row_target"].tolist()
                for task, a, b in zip(tasks, rs, rt):
                    acc = per_task.setdefault(task, [0.0, 0])
                    acc[0] += a
                    acc[1] += b
        return loss_sum, per_task

    on_battery, last_power_check, exit_code, bad_steps = False, 0.0, 0, 0
    micro_tokens = cfg.micro_tokens
    last_ckpt, t_log = time.time(), time.time()
    if step == 0:
        guarded("evaluation", do_eval)                      # the starting point, for the gates
    model.train()
    while step < cfg.total_steps and not stop["flag"]:
        for grp in opt.param_groups:
            grp["lr"] = lr_at(step, cfg)
        while True:
            try:
                loss_sum, per_task = one_step(micro_tokens)
                break
            except torch.OutOfMemoryError:
                if micro_tokens <= 256:
                    raise
            model.zero_grad(set_to_none=True)
            torch.cuda.empty_cache()
            micro_tokens //= 2
            print(f"CUDA out of memory: retrying the step with {micro_tokens} tokens per micro-batch", flush=True)
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        if torch.isfinite(loss_sum) and torch.isfinite(grad_norm):
            opt.step()
            bad_steps = 0
        else:
            bad_steps += 1
            print(f"non-finite loss or gradient at step {step}: update skipped ({bad_steps} in a row)", flush=True)
            if bad_steps >= MAX_BAD_STEPS:
                print("training diverged: stopping without saving", flush=True)
                return EXIT_DIVERGED
        opt.zero_grad(set_to_none=True)
        with torch.no_grad():
            d = min(cfg.ema_decay, (1 + step) / (10 + step))
            torch._foreach_lerp_(list(ema.parameters()), list(model.parameters()), 1 - d)
        step += 1

        if step % cfg.log_every == 0:
            dt = time.time() - t_log
            rec = {"loss": float(loss_sum), "lr": lr_at(step, cfg), "grad_norm": float(grad_norm),
                   "seq_per_s": cfg.batch_size * cfg.log_every / dt, "gpu_mem_gb": torch.cuda.max_memory_allocated() / 2**30}
            if per_task:
                rec |= {f"loss/{k}": v_[0] / max(1, v_[1]) for k, v_ in per_task.items()}
            emit(rec)
            print(f"step {step}/{cfg.total_steps} loss {float(loss_sum):.4f} lr {lr_at(step, cfg):.2e} "
                  f"{cfg.batch_size * cfg.log_every / dt:.1f} seq/s", flush=True)
            t_log = time.time()
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
                print(f"battery at {battery}%: saving and stopping", flush=True)
                exit_code = EXIT_RESTART
                break
        if now - last_ckpt > (cfg.battery_ckpt_min if on_battery else cfg.ckpt_every_min) * 60:
            checkpoint("on battery" if on_battery else "periodic")

    checkpoint("stopped" if stop["flag"] else "end of run" if step >= cfg.total_steps else "low battery")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
