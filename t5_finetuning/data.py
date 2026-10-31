"""Training and validation examples (PLAN.md §3), as text (tokenised at training time: one build serves every size).

    ../.venv/bin/python -u data.py --n 48000                     # E6-weighted sample → data/train.jsonl
    ../.venv/bin/python -u data.py --n 0 --name train_full      # the whole T1 pool (300,763), natural mix → data/train_full.jsonl

- **Train:** E6's T1 pool of the train split, N poems drawn without replacement with E6's metre weights
  (ft.canvas.Pools: metres under RARE_METRE poems upsampled up to MAX_UPSAMPLE, dvipada capped at DVIPADA_SHARE), by
  weighted random keys in log form (Efraimidis & Spirakis). Each row: id, meter, src (common.source_text), tgt (the
  poem), and, when the strict engines scan every line, scan_src / scan_tgt (the auxiliary scansion task).
- **Full** (`--n 0`, user decision 2026-10-21 for the 270M): every poem of the pool once, in a seeded order, at its
  natural metre mix (no upsampling, dvipada not capped).
- **Val:** 200 poems of E6's val T1 pool (fixed seed), with src_t0 (the same input with an empty bhāvam) for the
  T0 − T1 check.

Writes data/train.jsonl, data/val.jsonl, data/stats.json.
"""
from __future__ import annotations

import argparse
import collections
import json
import sys

import numpy as np

import common as C

sys.path.append(str(C.REPO / "diffusion_finetuning"))
from ft.canvas import DVIPADA_SHARE, MAX_UPSAMPLE, RARE_METRE        # noqa: E402

SEED = 20261021


def weights(meters: list[str]) -> np.ndarray:
    """ft.canvas.Pools._metre_weights."""
    counts = collections.Counter(meters)
    w = np.asarray([min(MAX_UPSAMPLE, RARE_METRE / counts[m]) if counts[m] < RARE_METRE else 1.0 for m in meters])
    dv = np.asarray([m == "dvipada" for m in meters])
    d, o = w[dv].sum(), w[~dv].sum()
    if d > 0 and o > 0 and d / (d + o) > DVIPADA_SHARE:
        w[dv] *= DVIPADA_SHARE / (1 - DVIPADA_SHARE) * o / d
    return w / w.sum()


def row(r: dict, with_scan: bool) -> dict:
    out = {"id": r["id"], "meter": C.metre_key(r.get("meter")), "src": C.source_text(r), "tgt": C.target_text(r)}
    if with_scan:
        s = C.scansion(r)
        if s:
            out["scan_src"], out["scan_tgt"] = C.scansion_source(r), s
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=48000, help="0 = the whole pool, natural mix")
    ap.add_argument("--name", default="train", help="data/<name>.jsonl")
    args = ap.parse_args()
    pool = [r for r in C.read_records("train") if C.t1_pool(r)]
    if args.n <= 0:
        pick = np.random.default_rng(SEED).permutation(len(pool))
    else:
        w = weights([C.metre_key(r.get("meter")) or "" for r in pool])
        pick = np.argsort(-(np.log(np.random.default_rng(SEED).random(len(pool))) / w))[: args.n]
    train = [row(pool[i], True) for i in pick]
    vpool = [r for r in C.read_records("val") if C.t1_pool(r)]
    val = []
    for i in np.random.default_rng(SEED + 1).permutation(len(vpool))[:200]:
        r = vpool[i]
        val.append({**row(r, False), "src_t0": C.source_text(r, empty_meaning=True)})
    C.DATA.mkdir(exist_ok=True)
    for name, rows in ((args.name, train), ("val", val)):
        with open(C.DATA / f"{name}.jsonl", "w", encoding="utf-8") as fh:
            for x in rows:
                fh.write(json.dumps(x, ensure_ascii=False) + "\n")
    stats = {"train": len(train), "with_scansion": sum("scan_tgt" in x for x in train), "val": len(val),
             "pool": len(pool), "metres": dict(collections.Counter(x["meter"] for x in train).most_common()),
             "src_chars": float(np.mean([len(x["src"]) for x in train])),
             "tgt_chars": float(np.mean([len(x["tgt"]) for x in train])),
             "metres_without_rules": sorted({x["meter"] for x in train if not C.rules(x["meter"] or "")})}
    (C.DATA / f"stats_{args.name}.json").write_text(json.dumps(stats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    main()
