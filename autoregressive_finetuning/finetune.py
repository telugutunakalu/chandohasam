"""Step 3 of PLAN.md: full fine-tuning of Nandi-Mini-150M on meaning → poem (E6's T1), the AR partner of ft.train.

    ../.venv/bin/python -u finetune.py --run nandi-t1-lr1.5e-4 --lr 1.5e-4 --epochs 1
    ../.venv/bin/python -u finetune.py --run nandi-speed-compile --max-steps 60 --eval-every 0   # step 2's speed test
    ../.venv/bin/python -u finetune.py --run rl-nandi --records ../RL/data/nandi/records/train.jsonl \
        --init runs/nandi-t1/snapshots/ema_step_0008225.pt --lr 1e-4 --batch-size 32 --epochs 2   # ../RL (expert iteration)

The recipe of E6's meaning → poem phase (ft.train stage 2, mix T1 = 1.0), with an AR loss:
- **Examples:** E6's T1 pool of the train split (poem lines, a metre the engines accept, a meaning), in the T1 layout
  of nandi.encode_t1; examples over nandi.MAX_TOKENS (1,024) tokens are dropped. Each example of a batch is drawn
  with E6's metre weights (ft.canvas.Pools: rare metres upsampled, dvipada capped), with replacement, as E6 draws.
- **Steps:** 128 examples per step; one epoch = ceil(pool / 128) steps (2,350, as E6's T1 phase).
- **Loss:** next-token cross-entropy on the poem tokens and the final `<|endoftext|>` (nandi.encode_t1's mask), summed
  and divided by the batch's loss tokens. The output layer is applied to the loss positions only.
- **Optimisation:** AdamW β (0.9, 0.98), weight decay 0.1 on matrices, gradient clip 1.0, linear warm-up then cosine
  to 10% (mdlm.train.lr_at), bf16 autocast over fp32 weights, an EMA (0.999) of the weights, which is what is
  evaluated and saved.
- **Batches** are a pure function of (seed, step), so a resumed run sees exactly the batches it would have seen.
  As in E6, a batch is a random draw; it is sorted by length only to cut it into micro-batches (little padding).
- **Padding:** on the right, with no attention mask: causal attention never lets a real token see the padding
  after it (check_nandi.py: right padding changes real tokens' logits by ≤ 4e-5).
- **Validation** every 250 steps (EMA): all val records of the T1 pool, given metre + meaning (T1) and given the
  metre only (T0, an empty `భావం:` line), in nats per MDLM target token (E6's unit) and per Nandi token.
- **Other data / start:** `--records` trains on another records JSONL of the same layout (../RL's reward-selected
  poems plus replay) instead of E6's train split; `--init` starts from an EMA snapshot instead of the base model (the
  optimizer starts fresh; a resumed run still resumes from its own checkpoint).
- **Checkpoints** in two alternating slots every 15 min and at the end (mdlm.checkpoint); the last line logged is
  "checkpoint at step N -> ... (end of run)" when the run completed, as ft.train. bf16 EMA snapshots every 1,000
  steps and at the end (snapshots/ema_step_*.pt: what step 4 evaluates). SIGTERM saves and exits 0.

Logs: runs/<run>.log (stdout), runs/<run>/metrics.jsonl, runs/<run>/samples/ (generated text, not committed).
"""
from __future__ import annotations

import argparse
import copy
import dataclasses
import json
import math
import signal
import time
import types
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

import nandi
from nandi import E6_RECORDS, EOS, HERE, PAD

from ft.canvas import DVIPADA_SHARE, Pools                          # noqa: E402 (sys.path set by nandi)
from mdlm.checkpoint import load_latest, save_checkpoint, save_snapshot
from mdlm.checkpoint_eval import _evict_large_files
from mdlm.train import _truncate_log, lr_at

RUNS = HERE / "runs"
CACHE = HERE / "data"                  # the encoded T1 examples (built from the confidential corpus; gitignored)
EXIT_DIVERGED, MAX_BAD_STEPS = 3, 100


@dataclass
class Config:
    run: str
    lr: float = 1.5e-4
    epochs: float = 1.0
    max_steps: int = 0                       # > 0: stop after this many steps (the speed test); else from epochs
    batch_size: int = 128
    warmup_steps: int = 100
    min_lr_ratio: float = 0.1
    beta2: float = 0.98
    weight_decay: float = 0.1
    grad_clip: float = 1.0
    ema_decay: float = 0.999
    seed: int = 20261018
    records: str = ""                        # a records JSONL to train on instead of E6's train split
    init: str = ""                           # an EMA snapshot to start from instead of the base model
    compile: bool = True
    micro_tokens: int = 8192                 # padded tokens per forward/backward chunk
    log_every: int = 10
    eval_every: int = 250
    sample_every: int = 1000
    snapshot_every: int = 1000
    ckpt_every_min: float = 15.0
    min_free_gb: float = 20.0
    total_steps: int = 0                     # derived


# --------------------------------------------------------------------------- data
def load_pool(records: str = "") -> dict:
    """The T1 pool of the train split (or of ``records``), encoded once and cached (keyed by the JSONL's size and
    mtime)."""
    src = Path(records).resolve() if records else E6_RECORDS / "train.jsonl"
    st = src.stat()
    tag = "train" if not records else f"{src.parent.parent.name}_{src.stem}"
    path = CACHE / f"t1_{tag}.{st.st_size}_{int(st.st_mtime)}_{nandi.MAX_TOKENS}.pt"
    if path.exists():
        return torch.load(path, weights_only=False)
    t0 = time.time()
    tok = nandi.load_tokenizer()
    ids, masks, lengths, meters, kept, dropped = [], [], [], [], 0, 0
    with open(src, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if not nandi.in_t1_pool(r):
                continue
            s, m = nandi.encode_t1(r, tok=tok)
            if len(s) > nandi.MAX_TOKENS:
                dropped += 1
                continue
            ids.append(np.asarray(s, dtype=np.int32))
            masks.append(np.asarray(m, dtype=np.bool_))
            lengths.append(len(s))
            meters.append(r.get("meter"))
            kept += 1
    lengths = np.asarray(lengths, dtype=np.int64)
    pool = {"ids": np.concatenate(ids), "mask": np.concatenate(masks), "lengths": lengths,
            "offsets": np.concatenate([[0], np.cumsum(lengths)]), "meters": meters, "dropped": dropped}
    CACHE.mkdir(parents=True, exist_ok=True)
    torch.save(pool, path)
    print(f"T1 pool: {kept:,} examples ({dropped} over {nandi.MAX_TOKENS} tokens dropped), "
          f"{int(lengths.sum()):,} tokens, encoded in {time.time() - t0:.0f} s", flush=True)
    return pool


class Batches:
    """Examples of a step, a pure function of (seed, step)."""

    def __init__(self, pool: dict, batch_size: int, seed: int):
        self.pool, self.B, self.seed = pool, batch_size, seed
        recs = [types.SimpleNamespace(meter=m) for m in pool["meters"]]
        w = Pools._metre_weights(types.SimpleNamespace(recs=recs), np.arange(len(recs)), DVIPADA_SHARE)
        self.cdf = np.cumsum(w)

    def steps_per_epoch(self) -> int:
        return math.ceil(len(self.pool["lengths"]) / self.B)

    def indices(self, step: int) -> np.ndarray:
        rng = np.random.default_rng([self.seed, step])
        return np.minimum(np.searchsorted(self.cdf, rng.random(self.B) * self.cdf[-1]), len(self.cdf) - 1)

    def example(self, i: int) -> tuple[np.ndarray, np.ndarray]:
        a, b = self.pool["offsets"][i], self.pool["offsets"][i + 1]
        return self.pool["ids"][a:b], self.pool["mask"][a:b]


ROUND, CHUNK_COST = 16, 256


def split_sorted(lengths: list[int], budget: int) -> list[tuple[int, int]]:
    """Cut length-sorted rows into chunks of at most ``budget`` padded tokens, minimising padded tokens plus
    CHUNK_COST per chunk (dynamic programming). Measured on random batches: 7.8% padding at ~8 chunks per step,
    against 19% for a greedy cut."""
    n = len(lengths)
    pad = [-(-x // ROUND) * ROUND for x in lengths]
    best, prev = [0.0] + [math.inf] * n, [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j - 1, -1, -1):
            if (j - i) * pad[j - 1] > budget and i < j - 1:
                break
            v = best[i] + (j - i) * pad[j - 1] + CHUNK_COST
            if v < best[j]:
                best[j], prev[j] = v, i
    cuts, j = [], n
    while j:
        cuts.append((prev[j], j))
        j = prev[j]
    return cuts[::-1]


def micro_batches(examples: list, micro_tokens: int):
    """Right-padded (ids, labels) chunks of a batch, sorted by length and cut by split_sorted."""
    examples = sorted(examples, key=lambda e: len(e[0]))
    for i, j in split_sorted([len(s) for s, _ in examples], micro_tokens):
        rows = examples[i:j]
        L = -(-len(rows[-1][0]) // ROUND) * ROUND
        ids = torch.full((len(rows), L), PAD, dtype=torch.long)
        lab = torch.full((len(rows), L), -100, dtype=torch.long)
        for k, (s, m) in enumerate(rows):
            s_t = torch.from_numpy(s.astype(np.int64))
            ids[k, :len(s)] = s_t
            lab[k, :len(s)] = torch.where(torch.from_numpy(m), s_t, torch.full_like(s_t, -100))
        yield ids, lab


def loss_sum(model, ids: torch.Tensor, lab: torch.Tensor) -> tuple[torch.Tensor, int]:
    """Summed next-token NLL over the loss positions; the vocabulary projection only where there is a label."""
    hidden = model.model(input_ids=ids, use_cache=False).last_hidden_state
    h = model.lm_head_proj(hidden[:, :-1])
    tgt = lab[:, 1:]
    sel = tgt != -100
    logits = model.lm_head(h[sel])
    return F.cross_entropy(logits.float(), tgt[sel], reduction="sum"), int(sel.sum())


# --------------------------------------------------------------------------- helpers
def wait_for_cuda(min_gb: float) -> None:
    """Block until CUDA reports min_gb free; evict page cache first (on the GB10 CUDA free = MemFree)."""
    first = True
    while True:
        try:
            free = torch.cuda.mem_get_info()[0] / 2**30
        except RuntimeError as exc:                     # the E6 evaluator once crashed here: retry instead
            print(f"CUDA memory query failed ({exc}); retrying in 60 s", flush=True)
            time.sleep(60)
            continue
        if free >= min_gb:
            return
        if first:
            _evict_large_files()
            first = False
            continue
        print(f"{free:.1f} GB CUDA memory free, waiting for {min_gb:g} GB", flush=True)
        time.sleep(60)
        _evict_large_files()


SAMPLE_IDS = 4


@torch.no_grad()
def write_samples(ema, val_recs: list[dict], step: int, out: Path, seed: int) -> None:
    tok = nandi.load_tokenizer()
    texts = []
    for k, r in enumerate(val_recs[:SAMPLE_IDS]):
        p = torch.tensor([nandi.prompt_ids(r, tok=tok)], device="cuda")
        torch.manual_seed(seed + k)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            g = ema.generate(input_ids=p, attention_mask=torch.ones_like(p), do_sample=True, temperature=0.7,
                             top_p=0.9, max_new_tokens=200, eos_token_id=EOS, pad_token_id=PAD)
        new = g[0, p.shape[1]:].tolist()
        texts.append(f"## {r['id']} ({r.get('meter')})\n{nandi.decode(new[:new.index(EOS)] if EOS in new else new, tok)}\n"
                     f"-- gold --\n" + "\n".join(r["lines"]) + "\n")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"step_{step:07d}.txt").write_text("\n".join(texts), encoding="utf-8")


# --------------------------------------------------------------------------- main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    for f in dataclasses.fields(Config):
        if f.name not in ("run", "total_steps", "compile"):
            ap.add_argument("--" + f.name.replace("_", "-"), type=type(f.default), default=f.default)
    ap.add_argument("--no-compile", action="store_true")
    args = ap.parse_args(argv)
    cfg = Config(**{k: v for k, v in vars(args).items() if k != "no_compile"})
    cfg.compile = not args.no_compile

    run_dir = RUNS / cfg.run
    run_dir.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch._dynamo.config.cache_size_limit = 64
    device = torch.device("cuda")
    pool = load_pool(cfg.records)
    data = Batches(pool, cfg.batch_size, cfg.seed)
    cfg.total_steps = cfg.max_steps or int(round(cfg.epochs * data.steps_per_epoch()))
    val_recs = [r for r in (json.loads(l) for l in open(E6_RECORDS / "val.jsonl", encoding="utf-8")) if nandi.in_t1_pool(r)]
    items = nandi.val_items(val_recs)

    wait_for_cuda(cfg.min_free_gb)
    state = load_latest(run_dir, "cpu")
    model = nandi.load_model("float32", "cpu", (cfg.init or None) if state is None else None)
    provenance = {"from": f"{nandi.MODEL_ID}@{nandi.REVISION}", "weights": cfg.init or "base",
                  "records": cfg.records or str(E6_RECORDS / "train.jsonl")}
    step = 0
    if state is not None:
        model.load_state_dict(state["model"])
    model.to(device).train()
    ema = copy.deepcopy(model).requires_grad_(False).eval()
    decay = [p for p in model.parameters() if p.dim() >= 2]
    no_decay = [p for p in model.parameters() if p.dim() < 2]
    opt = torch.optim.AdamW([{"params": decay, "weight_decay": cfg.weight_decay},
                             {"params": no_decay, "weight_decay": 0.0}],
                            lr=cfg.lr, betas=(0.9, cfg.beta2), fused=True)
    if state is not None:
        ema.load_state_dict(state["ema"])
        opt.load_state_dict(state["opt"])
        step = state["step"]
        provenance = state.get("provenance", provenance)
        del state
        _truncate_log(run_dir / "metrics.jsonl", step)
        print(f"resumed from step {step}", flush=True)
    else:
        print(f"initialised from {provenance['from']} ({provenance['weights']} weights)", flush=True)
    print(f"run {cfg.run}: {cfg.total_steps} steps of {cfg.batch_size} ({data.steps_per_epoch()} per epoch over "
          f"{len(pool['lengths']):,} examples), lr {cfg.lr:g}, compile {cfg.compile}", flush=True)
    (run_dir / "config.json").write_text(json.dumps(dataclasses.asdict(cfg), indent=1) + "\n", encoding="utf-8")

    compiled = False
    if cfg.compile:
        for layer in model.model.layers:
            layer.compile()
        compiled = True

    def uncompile() -> None:
        nonlocal compiled
        for layer in model.model.layers:
            layer._compiled_call_impl = None
        compiled = False

    log = (run_dir / "metrics.jsonl").open("a", encoding="utf-8")

    def emit(rec: dict) -> None:
        log.write(json.dumps({"step": step, **rec}) + "\n")
        log.flush()

    stop = {"flag": False}
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.update(flag=True))

    last_ckpt = time.time()

    def checkpoint(reason: str) -> None:
        nonlocal last_ckpt
        try:
            st = {"model": model.state_dict(), "ema": ema.state_dict(), "opt": opt.state_dict(), "step": step,
                  "config": dataclasses.asdict(cfg), "provenance": provenance}
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
        res = nandi.evaluate_t1(ema, items, device)
        emit(res)
        print(f"eval step {step}: T1 {res['val_nll/T1']:.4f} T0 {res['val_nll/T0']:.4f} nats/MDLM token "
              f"(gap {res['val_nll/T0'] - res['val_nll/T1']:.3f})", flush=True)

    def one_step(micro: int) -> tuple[torch.Tensor, int, int]:
        examples = [data.example(int(i)) for i in data.indices(step)]
        denom = sum(int(m[1:].sum()) for _, m in examples)
        total = torch.zeros((), device=device)
        real = 0
        for ids, lab in micro_batches(examples, micro):
            ids, lab = ids.to(device, non_blocking=True), lab.to(device, non_blocking=True)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                s, _ = loss_sum(model, ids, lab)
            (s / denom).backward()
            total += s.detach() / denom
            real += int((ids != PAD).sum())
        return total, denom, real

    if step == 0 and cfg.eval_every:
        guarded("evaluation", do_eval)
    micro = cfg.micro_tokens
    bad, t_log, tok_log, loss_tok_log = 0, time.time(), 0, 0
    while step < cfg.total_steps and not stop["flag"]:
        for g in opt.param_groups:
            g["lr"] = lr_at(step, cfg)
        while True:
            try:
                loss, n_loss, n_real = one_step(micro)
                break
            except torch.OutOfMemoryError:
                model.zero_grad(set_to_none=True)
                torch.cuda.empty_cache()
                if micro <= 1024:
                    raise
                micro //= 2
                print(f"CUDA out of memory: retrying the step with {micro} tokens per micro-batch", flush=True)
            except Exception as exc:                       # a torch.compile failure: continue eager
                if not compiled:
                    raise
                model.zero_grad(set_to_none=True)
                print(f"torch.compile failed ({type(exc).__name__}: {str(exc)[:300]}); continuing without it", flush=True)
                uncompile()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
        if torch.isfinite(loss) and torch.isfinite(grad_norm):
            opt.step()
            bad = 0
        else:
            bad += 1
            print(f"non-finite loss or gradient at step {step}: update skipped ({bad} in a row)", flush=True)
            if bad >= MAX_BAD_STEPS:
                print("training diverged: stopping without saving", flush=True)
                return EXIT_DIVERGED
        opt.zero_grad(set_to_none=True)
        with torch.no_grad():
            d = min(cfg.ema_decay, (1 + step) / (10 + step))
            torch._foreach_lerp_(list(ema.parameters()), list(model.parameters()), 1 - d)
        step += 1
        tok_log += n_real
        loss_tok_log += n_loss

        if step % cfg.log_every == 0:
            dt = time.time() - t_log
            rec = {"loss": float(loss), "lr": lr_at(step, cfg), "grad_norm": float(grad_norm),
                   "tok_per_s": tok_log / dt, "loss_tok_per_s": loss_tok_log / dt,
                   "seq_per_s": cfg.batch_size * cfg.log_every / dt, "micro_tokens": micro,
                   "gpu_mem_gb": torch.cuda.max_memory_allocated() / 2**30, "compiled": compiled}
            emit(rec)
            print(f"step {step}/{cfg.total_steps} loss {float(loss):.4f} lr {rec['lr']:.2e} "
                  f"{rec['tok_per_s']:,.0f} tok/s {rec['seq_per_s']:.1f} seq/s mem {rec['gpu_mem_gb']:.1f} GB", flush=True)
            t_log, tok_log, loss_tok_log = time.time(), 0, 0
        if cfg.eval_every and (step % cfg.eval_every == 0 or step == cfg.total_steps):
            guarded("evaluation", do_eval)
        if cfg.sample_every and (step % cfg.sample_every == 0 or step == cfg.total_steps):
            guarded("sampling", lambda: write_samples(ema, val_recs, step, run_dir / "samples", cfg.seed))
        if cfg.snapshot_every and (step % cfg.snapshot_every == 0 or step == cfg.total_steps):
            guarded("snapshot", lambda: save_snapshot(run_dir, ema, step))
        if time.time() - last_ckpt > cfg.ckpt_every_min * 60:
            checkpoint("periodic")

    checkpoint("stopped" if stop["flag"] else "end of run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
