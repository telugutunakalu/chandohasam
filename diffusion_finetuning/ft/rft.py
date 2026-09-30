"""Stage 4 (PLAN §7): rejection-sampling self-training.

    # 1. write K constrained poems for N training meanings; keep the best one that passes
    python -m ft.rft generate --run runs/s2-best --n 5000 --k 8 --out data/rft/round1
    # 2. a training set of the kept poems plus as many gold poems (replay)
    python -m ft.rft build --round data/rft/round1
    # 3. one epoch of meaning -> poem training on it, at a low learning rate
    python -m ft.train --stage 2 --run rft1 --init-from runs/s2-best --data-dir data/rft/round1 \\
        --mix '{"T1": 1.0}' --epochs 1 --lr 2e-5
    # 4. judge rft1 on val with ft.evaluate / ft.judge; stop when the judge stops improving

Kept: engine-valid under the strict profiles (metre, prāsa, yati), then the best model poem ->
meaning likelihood, subject to three guards against reward hacking: copy rate from the meaning
at most the gold 95th percentile, distinct-2 at least the gold 5th percentile, no repeated line.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import shutil
import time
from pathlib import Path

import numpy as np

from . import DATA_DIR


def _toks(tok, text: str) -> list[int]:
    return [t for t in tok.encode(text) if t > 4]


def _copy_rate(tok, lines: list[str], meaning: str) -> float:
    p = _toks(tok, "\n".join(lines))
    m = set(tuple(x) for x in np.lib.stride_tricks.sliding_window_view(_toks(tok, meaning), 4)) if len(_toks(tok, meaning)) >= 4 else set()
    g = [tuple(p[i:i + 4]) for i in range(len(p) - 3)]
    return sum(x in m for x in g) / max(1, len(g))


def _distinct2(tok, lines: list[str]) -> float:
    p = _toks(tok, "\n".join(lines))
    return len(set(zip(p, p[1:]))) / max(1, len(p) - 1)


def _train_pool(data_dir: Path) -> list[dict]:
    rows = []
    for line in (data_dir / "records" / "train.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["status"] in ("agree", "engine-only") and r.get("meaning") and r.get("meter_label"):
            rows.append(r)
    return rows


def cmd_generate(args) -> int:
    import torch

    from tokenizer import load_default

    from .decode import DecodeConfig, Decoder, load_model
    tok = load_default()
    pool = _train_pool(args.data_dir)
    rng = np.random.default_rng(args.seed)
    gold = [pool[i] for i in rng.choice(len(pool), size=min(2000, len(pool)), replace=False)]
    copy95 = float(np.percentile([_copy_rate(tok, r["lines"], r["meaning"]) for r in gold], 95))
    dist05 = float(np.percentile([_distinct2(tok, r["lines"]) for r in gold], 5))
    todo = [pool[i] for i in rng.choice(len(pool), size=min(args.n, len(pool)), replace=False)]
    dev = torch.device("cuda")
    model, prov = load_model(args.run, dev)
    cfg = DecodeConfig(particles=args.k, guidance=args.guidance, seed=args.seed)
    dec = Decoder(model, tok, dev, cfg, args.data_dir)
    args.out.mkdir(parents=True, exist_ok=True)
    kept, stats = [], {"tried": 0, "no_candidate": 0, "engine_fail": 0, "guard_fail": 0, "kept": 0}
    t0 = time.time()
    with (args.out / "kept.jsonl").open("w", encoding="utf-8") as fh:
        for i, r in enumerate(todo):
            stats["tried"] += 1
            try:
                out = dec.generate(r["meter_label"], r["meaning"], r["register"], r["meaning_src"])
            except ValueError:
                stats["no_candidate"] += 1
                continue
            cands = [c for c in out["candidates"] if c.get("metre_ok") and c.get("prasa_strict") and c.get("yati_strict")]
            if not out["candidates"]:
                stats["no_candidate"] += 1
                continue
            if not cands:
                stats["engine_fail"] += 1
                continue
            ok = [c for c in cands if _copy_rate(tok, c["lines"], r["meaning"]) <= copy95
                  and _distinct2(tok, c["lines"]) >= dist05 and len(set(c["lines"])) == len(c["lines"])]
            if not ok:
                stats["guard_fail"] += 1
                continue
            best = min(ok, key=lambda c: c["reverse_nll"])
            new = dict(r, id=f"{args.out.name}-{r['id']}", lines=best["lines"], source="rft", samasya=None,
                       glosses=[], rft={"from": r["id"], "reverse_nll": best["reverse_nll"], "model": str(args.run)})
            fh.write(json.dumps(new, ensure_ascii=False) + "\n")
            stats["kept"] += 1
            if (i + 1) % 25 == 0:
                print(f"{i + 1}/{len(todo)} {stats} {(time.time() - t0) / (i + 1):.1f}s/meaning", flush=True)
    stats |= {"copy95": copy95, "distinct2_p05": dist05, "decode": dataclasses.asdict(cfg), "model": str(args.run),
              "init": prov, "seconds": round(time.time() - t0)}
    (args.out / "stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(stats, flush=True)
    return 0


def cmd_build(args) -> int:
    """<round>/records/{train,val}.jsonl: the kept poems plus gold replay; val is the usual val."""
    kept = [json.loads(l) for l in (args.round / "kept.jsonl").open(encoding="utf-8")]
    pool = _train_pool(args.data_dir)
    rng = np.random.default_rng(args.seed)
    n_gold = max(int(round(len(kept) * args.gold_ratio)), args.min_gold)
    gold = [pool[i] for i in rng.choice(len(pool), size=min(n_gold, len(pool)), replace=False)]
    rec = args.round / "records"
    rec.mkdir(parents=True, exist_ok=True)
    with (rec / "train.jsonl").open("w", encoding="utf-8") as fh:
        for r in kept + gold:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    shutil.copy(args.data_dir / "records" / "val.jsonl", rec / "val.jsonl")
    print(f"{len(kept)} kept + {len(gold)} gold -> {rec}", flush=True)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--run", type=Path, required=True)
    g.add_argument("--n", type=int, default=5000)
    g.add_argument("--k", type=int, default=8)
    g.add_argument("--guidance", type=float, default=0.0)
    g.add_argument("--out", type=Path, required=True)
    g.add_argument("--data-dir", type=Path, default=DATA_DIR)
    g.add_argument("--seed", type=int, default=0)
    b = sub.add_parser("build")
    b.add_argument("--round", type=Path, required=True)
    b.add_argument("--gold-ratio", type=float, default=1.0)
    b.add_argument("--min-gold", type=int, default=0, help="at least this many gold poems (smoke runs)")
    b.add_argument("--data-dir", type=Path, default=DATA_DIR)
    b.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    return cmd_generate(args) if args.cmd == "generate" else cmd_build(args)


if __name__ == "__main__":
    raise SystemExit(main())
