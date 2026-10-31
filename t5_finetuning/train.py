"""Fine-tune T5Gemma 2 on bhāvam (+ metre rules) → poem, with the auxiliary scansion task (PLAN.md §2, §4).

    ../.venv/bin/python -u train.py --size 270m --run t5g-270m --epochs 1                 # full fine-tuning
    ../.venv/bin/python -u train.py --size 1b --run t5g-1b --lr 5e-5 --epochs 1
    ../.venv/bin/python -u train.py --size 4b --run t5g-4b-lora --lora 32 --lora-mlp --grad-ckpt --lr 2e-4 --epochs 1
    ../.venv/bin/python -u train.py --size 270m --run t5g-270m-ep2 --init runs/t5g-270m-full/final --data train_full \
        --lr 3e-5 --warmup 200 --epochs 1                                                   # a second epoch
    ../.venv/bin/python -u train.py --size 270m --run smoke --max-steps 20 --eval-every 10    # a smoke test

- **Examples:** data/train.jsonl; each epoch every poem once in a seeded order; with probability --aux (default 0.15)
  an example with a scansion target is used as `పని: గురులఘువులు` (poem → patterns) instead of `పని: పద్యం`.
- **Batches:** examples in order, cut whenever the padded batch would exceed --batch-tokens (source + target tokens);
  padding with attention masks; labels −100 on padding. The loss is the model's own (mean over label tokens).
- **Optimisation:** AdamW (β 0.9, 0.98; weight decay 0.01 on full fine-tuning), linear warm-up then cosine to 10%,
  gradient clipping 1.0, bf16 autocast (full fine-tuning asks for fp32 weights, but the encoder stack and the shared
  embedding load in bf16, so only the decoder layers train in fp32; LoRA: bf16 base, fp32 adapters).
- **Evaluation** every --eval-every steps, at 0 and at the end: val loss on the poem given the bhāvam (T1) and given an
  empty bhāvam (T0) — T0 − T1 > 0 means the model uses the meaning —, and one greedy poem for one E6 val prompt per
  metre (11), scored by the strict engines (lines, gaṇa / prāsa / yati).
- **Checkpoints:** runs/<run>/last.pt (weights or adapters, optimizer, step, position) every --save-every steps and at
  the end; a rerun resumes. The final model: runs/<run>/final/ (save_pretrained) or runs/<run>/lora.pt.
Logs: stdout (runs/<run>.log when redirected) and runs/<run>/metrics.jsonl.
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import random
import signal

import numpy as np
import torch

import common as C

REFERENCE = C.REPO / "diffusion_finetuning" / "runs" / "e6_120m_val"


def lr_at(step: int, total: int, peak: float, warmup: int) -> float:
    if step < warmup:
        return peak * (step + 1) / warmup
    p = (step - warmup) / max(1, total - warmup)
    return peak * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * min(1.0, p))))


def batches(items: list, budget: int):
    out, ls, lt = [], 0, 0
    for it in items:
        s, t = it
        ns, nt = max(ls, len(s)), max(lt, len(t))
        if out and (len(out) + 1) * (ns + nt) > budget:
            yield out
            out, ns, nt = [], len(s), len(t)
        out.append(it)
        ls, lt = ns, nt
    if out:
        yield out


@torch.no_grad()
def evaluate_val(model, tok, val_t1, val_t0, budget) -> dict:
    model.eval()
    res = {}
    for name, items in (("T1", val_t1), ("T0", val_t0)):
        tot, n = 0.0, 0
        for b in batches(items, budget):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(**C.collate(b, tok.pad_token_id))
            k = sum(len(t) for _, t in b)
            tot, n = tot + float(out.loss) * k, n + k
        res[f"val_loss/{name}"] = tot / n
    res["val_gap_T0_minus_T1"] = res["val_loss/T0"] - res["val_loss/T1"]
    model.train()
    return res


@torch.no_grad()
def sample_poems(model, tok, prompts: list[dict]) -> dict:
    from metrical_decoder.evaluate import evaluate
    model.eval()
    rows = []
    for r in prompts:
        enc = tok(C.source_text(r), return_tensors="pt").to("cuda")
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = model.generate(**enc, max_new_tokens=256, do_sample=False)
        text = tok.decode(out[0], skip_special_tokens=True).strip()
        ev = evaluate(text, r["eval_meter"])
        rows.append({"meter": r["eval_meter"], "text": text, "lines": len(ev.get("lines") or []),
                     "all": bool(ev.get("gana_strict") and ev.get("prasa_strict") and ev.get("yati_strict")),
                     "gana": bool(ev.get("gana_strict"))})
    model.train()
    return {"samples": rows, "sample_gana": sum(r["gana"] for r in rows) / len(rows),
            "sample_all": sum(r["all"] for r in rows) / len(rows),
            "sample_lines": float(np.mean([r["lines"] for r in rows]))}


def e6_prompts_one_per_metre() -> list[dict]:
    pairs = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(REFERENCE / "results.jsonl")})
    recs = {r["id"]: r for r in C.read_records("val")}
    seen, out = set(), []
    for m, pid in pairs:
        if m not in seen:
            seen.add(m)
            out.append({**recs[pid], "eval_meter": m})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", choices=list(C.MODELS), required=True)
    ap.add_argument("--run", required=True)
    ap.add_argument("--lora", type=int, default=0, help="LoRA rank (0 = full fine-tuning)")
    ap.add_argument("--lora-mlp", action="store_true", help="LoRA on the MLP projections too (the 4B: 75%% of it)")
    ap.add_argument("--optim", choices=("adamw", "adafactor"), default="adamw",
                    help="adafactor: factored second moments, no first moment (full fine-tuning in less memory)")
    ap.add_argument("--grad-ckpt", action="store_true", help="gradient checkpointing (activation memory)")
    ap.add_argument("--init", default="", help="start from a save_pretrained folder (e.g. a second epoch)")
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--epochs", type=float, default=1.0)
    ap.add_argument("--max-steps", type=int, default=0)
    ap.add_argument("--warmup", type=int, default=100)
    # 8192, not 16384: the decoder's fp32 scores over 262k tokens for a 16k-token batch were a 5.4 GB allocation
    # (the one that failed in the 2026-10-21 system OOM)
    ap.add_argument("--batch-tokens", type=int, default=8192)
    ap.add_argument("--max-src", type=int, default=1024)
    ap.add_argument("--max-tgt", type=int, default=320)
    ap.add_argument("--aux", type=float, default=0.15, help="share of examples given as the scansion task")
    ap.add_argument("--eval-every", type=int, default=250)
    ap.add_argument("--save-every", type=int, default=250)
    ap.add_argument("--snapshot-at", type=int, default=0,
                    help="also keep the model after this many examples of the first epoch (runs/<run>/lora_at_<n>.pt "
                         "or at_<n>/), e.g. 48000: a data-size point inside a whole-pool run")
    ap.add_argument("--seed", type=int, default=20261021)
    ap.add_argument("--data", default="train", help="data/<name>.jsonl (train: 48k E6-weighted; train_full: all 300,763)")
    args = ap.parse_args()
    run = C.RUNS / args.run
    run.mkdir(parents=True, exist_ok=True)
    torch.backends.cuda.matmul.allow_tf32 = True

    model, tok = C.load(args.size, dtype=torch.bfloat16 if args.lora else torch.float32, path=args.init)
    frozen_vision = C.freeze_vision(model)
    if args.grad_ckpt:
        # non-reentrant: with a frozen base (LoRA) the reentrant form would pass no gradient through checkpointed
        # blocks whose inputs do not require one, and the adapters inside them would never learn
        model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
    if args.lora:
        params = C.inject_lora(model, r=args.lora, alpha=2 * args.lora, mlp=args.lora_mlp)
        opt = torch.optim.AdamW(params, lr=args.lr, betas=(0.9, 0.98), weight_decay=0.0)
    elif args.optim == "adafactor":
        from transformers.optimization import Adafactor
        params = [p for p in model.parameters() if p.requires_grad]
        opt = Adafactor(params, lr=args.lr, scale_parameter=False, relative_step=False, warmup_init=False,
                        weight_decay=0.0)
    else:
        params = [p for p in model.parameters() if p.requires_grad]
        decay = [p for p in params if p.dim() >= 2]
        nodecay = [p for p in params if p.dim() < 2]
        opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.01}, {"params": nodecay, "weight_decay": 0.0}],
                                lr=args.lr, betas=(0.9, 0.98))
    model.train()

    rows = [json.loads(l) for l in open(C.DATA / f"{args.data}.jsonl", encoding="utf-8")]
    poem, scan, skipped = [], {}, collections.Counter()
    for i, x in enumerate(rows):
        e = C.encode_pair(tok, x["src"], x["tgt"], args.max_src, args.max_tgt)
        if e is None:
            skipped["poem too long"] += 1
            continue
        poem.append((i, e))
        if "scan_tgt" in x:
            s = C.encode_pair(tok, x["scan_src"], x["scan_tgt"], args.max_src, args.max_tgt)
            if s is not None:
                scan[i] = s
    vrows = [json.loads(l) for l in open(C.DATA / "val.jsonl", encoding="utf-8")]
    val_t1, val_t0 = [], []
    for x in vrows:
        a = C.encode_pair(tok, x["src"], x["tgt"], args.max_src, args.max_tgt)
        b = C.encode_pair(tok, x["src_t0"], x["tgt"], args.max_src, args.max_tgt)
        if a and b:
            val_t1.append(a)
            val_t0.append(b)
    prompts = e6_prompts_one_per_metre()
    steps_per_epoch = None

    def epoch_order(ep: int) -> list:
        rng = random.Random(args.seed + ep)
        idx = list(range(len(poem)))
        rng.shuffle(idx)
        items = []
        for k in idx:
            i, e = poem[k]
            items.append(scan[i] if i in scan and rng.random() < args.aux else e)
        # length-sorted within chunks of 512: little padding, still random across chunks
        chunks = [sorted(items[j:j + 512], key=lambda p: len(p[0]) + len(p[1])) for j in range(0, len(items), 512)]
        return [b for c in chunks for b in batches(c, args.batch_tokens)]

    first = epoch_order(0)
    steps_per_epoch = len(first)
    total = args.max_steps or int(round(args.epochs * steps_per_epoch))
    # the step after which the first epoch's batches hold --snapshot-at examples (the order is seeded, so a resumed
    # run finds the same step)
    snap_step, seen = 0, 0
    if args.snapshot_at:
        for k, b in enumerate(first):
            seen += len(b)
            if seen >= args.snapshot_at:
                snap_step = k + 1
                break
    step, ep, pos = 0, 0, 0
    if (run / "last.pt").exists():
        st = torch.load(run / "last.pt", map_location="cpu", weights_only=False)
        if args.lora:
            sd = st["lora"]
            for n, p in model.named_parameters():
                if n in sd:
                    p.data.copy_(sd[n])
        else:
            model.load_state_dict(st["model"])
        opt.load_state_dict(st["opt"])
        step, ep, pos = st["step"], st["epoch"], st["pos"]
        print(f"resumed at step {step}", flush=True)
    log = open(run / "metrics.jsonl", "a", encoding="utf-8")
    emit = lambda rec: (log.write(json.dumps({"step": step, **rec}, ensure_ascii=False) + "\n"), log.flush())
    stop = {"flag": False}
    signal.signal(signal.SIGTERM, lambda *_: stop.update(flag=True))
    n_params = sum(p.numel() for p in params)
    (run / "config.json").write_text(json.dumps({**vars(args), "total_steps": total, "steps_per_epoch": steps_per_epoch,
                                                 "poems": len(poem), "scansion": len(scan), "skipped": dict(skipped),
                                                 "trainable_M": n_params / 1e6}, indent=1) + "\n")
    print(f"vision tower frozen ({frozen_vision / 1e6:.0f}M parameters, bf16){'; gradient checkpointing' if args.grad_ckpt else ''}"
          f"{'; from ' + args.init if args.init else ''}", flush=True)
    print(f"run {args.run}: T5Gemma 2 {args.size}, {'LoRA r ' + str(args.lora) + (' (attention + MLP)' if args.lora_mlp else '') if args.lora else 'full fine-tuning (' + args.optim + ')'} "
          f"({n_params / 1e6:.0f}M trainable); {len(poem):,} poems ({len(scan):,} with scansion, aux {args.aux}); "
          f"{steps_per_epoch:,} steps per epoch, {total:,} steps; lr {args.lr:g}"
          f"{f'; snapshot at step {snap_step:,} ({args.snapshot_at:,} examples)' if snap_step else ''}", flush=True)

    def save(final: bool = False) -> None:
        st = {"opt": opt.state_dict(), "step": step, "epoch": ep, "pos": pos}
        st["lora" if args.lora else "model"] = C.lora_state(model) if args.lora else model.state_dict()
        torch.save(st, run / "last.pt")
        if final:
            if args.lora:
                torch.save(C.lora_state(model), run / "lora.pt")
            else:
                model.save_pretrained(run / "final")
                tok.save_pretrained(run / "final")
        print(f"saved at step {step}{' (final)' if final else ''}", flush=True)

    def snapshot() -> None:
        if args.lora:
            torch.save(C.lora_state(model), run / f"lora_at_{args.snapshot_at}.pt")
        else:
            model.save_pretrained(run / f"at_{args.snapshot_at}")
            tok.save_pretrained(run / f"at_{args.snapshot_at}")
        print(f"snapshot at step {step} ({args.snapshot_at:,} examples)", flush=True)

    def do_eval() -> None:
        res = evaluate_val(model, tok, val_t1, val_t0, args.batch_tokens)
        res.update(sample_poems(model, tok, prompts))
        emit(res)
        print(f"eval step {step}: T1 {res['val_loss/T1']:.4f} T0 {res['val_loss/T0']:.4f} (gap {res['val_gap_T0_minus_T1']:+.4f}); "
              f"greedy poems: lines {res['sample_lines']:.1f}, gaṇa {res['sample_gana']:.0%}, all three {res['sample_all']:.0%}",
              flush=True)
        for s in res["samples"][:2]:
            print(f"  [{s['meter']}] " + s["text"].replace("\n", " / ")[:200], flush=True)

    if step == 0:
        do_eval()
    order = first if ep == 0 else epoch_order(ep)
    tick, losses = C_timer(), []
    while step < total and not stop["flag"]:
        if pos >= len(order):
            ep, pos = ep + 1, 0
            order = epoch_order(ep)
        b = order[pos]
        pos += 1
        for g in opt.param_groups:
            g["lr"] = lr_at(step, total, args.lr, args.warmup)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = model(**C.collate(b, tok.pad_token_id)).loss
        loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(params, 1.0)
        if torch.isfinite(gn):
            opt.step()
        else:
            print(f"non-finite gradient at step {step}: skipped", flush=True)
        opt.zero_grad(set_to_none=True)
        step += 1
        losses.append(float(loss))
        if step % 20 == 0:
            dt = tick()
            emit({"loss": float(np.mean(losses)), "lr": opt.param_groups[0]["lr"], "grad_norm": float(gn),
                  "s_per_step": dt / 20, "gpu_gb": torch.cuda.max_memory_allocated() / 1e9})
            print(f"step {step}/{total} loss {np.mean(losses):.4f} lr {opt.param_groups[0]['lr']:.2e} {dt / 20:.2f} s/step "
                  f"ETA {(total - step) * dt / 20 / 3600:.1f} h peak {torch.cuda.max_memory_allocated() / 1e9:.0f} GB", flush=True)
            tick, losses = C_timer(), []
        if step == snap_step:
            snapshot()
        if step % args.eval_every == 0 or step == total:
            do_eval()
        if step % args.save_every == 0:
            save()
    save(final=step >= total)
    print("stopped" if stop["flag"] else "end of run", flush=True)


def C_timer():
    import time
    t0 = time.time()
    return lambda: time.time() - t0


if __name__ == "__main__":
    main()
