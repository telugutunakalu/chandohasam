"""Training and validation examples for the LoRA (PLAN.md §2), in DiffusionGemma's tokens.

    ../.venv/bin/python -u data.py --n 24000          # after check_model.py (it fixes the canvas end rule)
    ../.venv/bin/python -u data.py --n 0 --name train_full   # the whole T1 pool (full_grid_experiments Phase 0)

- **Train:** E6's T1 pool of the train split (300,763 poems with a confirmed metre and a bhāvam; Padyarchana minus
  ../dataset), N drawn **without replacement** with E6's metre weights (ft.canvas.Pools: metres under RARE_METRE poems
  upsampled up to MAX_UPSAMPLE, dvipada capped at DVIPADA_SHARE of the weight), by weighted random keys (Efraimidis &
  Spirakis): the rare metres come in essentially whole, the common ones in proportion.
- **Whole pool** (`--n 0`): every T1-pool poem that fits, natural metre mix (no weights), as T5Gemma's train_full;
  token ids as int32 tensors (300k examples as lists of Python ints would take ≈ 8 GB of the shared memory).
- **Val:** 200 poems of E6's val split T1 pool (fixed seed), for the validation loss at fixed noise levels.
- An example is kept when its poem fits one canvas (poem tokens + end ids ≤ canvas length) and its prompt is at most
  MAX_PROMPT tokens.

Writes data/<name>.pt (default train.pt; lists of {id, meter, prompt, canvas, n_poem}), data/val.pt (once: it is the
same for every --n) and data/stats.json (stats_<name>.json for another name).
"""
from __future__ import annotations

import argparse
import collections
import json
import sys

import numpy as np
import torch

import common as C

sys.path.append(str(C.REPO / "diffusion_finetuning"))
from ft.canvas import DVIPADA_SHARE, MAX_UPSAMPLE, RARE_METRE        # noqa: E402

MAX_PROMPT = 768
SEED = 20261020


def metre(r: dict) -> str:
    m = r.get("meter") or ""
    return "seesamu" if m.startswith("seesamu") else m


def weights(meters: list[str]) -> np.ndarray:
    """ft.canvas.Pools._metre_weights."""
    counts = collections.Counter(meters)
    w = np.asarray([min(MAX_UPSAMPLE, RARE_METRE / counts[m]) if counts[m] < RARE_METRE else 1.0 for m in meters])
    dv = np.asarray([m == "dvipada" for m in meters])
    d, o = w[dv].sum(), w[~dv].sum()
    if d > 0 and o > 0 and d / (d + o) > DVIPADA_SHARE:
        w[dv] *= DVIPADA_SHARE / (1 - DVIPADA_SHARE) * o / d
    return w / w.sum()


def encode(tok, recs: list[dict], rule: dict, length: int,
           compact: bool = False) -> tuple[list[dict], collections.Counter]:
    """``compact``: token ids as int32 tensors, converted as they come (the peak never holds the lists)."""
    out, dropped = [], collections.Counter()
    for r in recs:
        p = C.prompt_ids(tok, r)
        c = C.canvas_ids(tok, r, rule["end_ids"], rule["fill_id"], length)
        if c is None:
            dropped["poem over the canvas"] += 1
            continue
        if len(p) > MAX_PROMPT:
            dropped["prompt over MAX_PROMPT"] += 1
            continue
        n_poem = len(tok(C.to_model("\n".join(r["lines"])), add_special_tokens=False).input_ids)
        if compact:
            p, c = torch.tensor(p, dtype=torch.int32), torch.tensor(c, dtype=torch.int32)
        out.append({"id": r["id"], "meter": metre(r), "prompt": p, "canvas": c, "n_poem": n_poem})
    return out, dropped


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=24000, help="0: the whole pool")
    ap.add_argument("--name", default="train")
    args = ap.parse_args()
    from transformers import AutoTokenizer
    from huggingface_hub import snapshot_download
    tok = AutoTokenizer.from_pretrained(snapshot_download(C.DEFAULT_MODEL, local_files_only=True))
    check = json.loads((C.RUNS / "check_model.json").read_text(encoding="utf-8"))
    rule, length = check["canvas_rule"], check["model"]["canvas_length"]

    pool = [r for r in C.read_records("train") if C.t1_pool(r)]
    if args.n:
        w = weights([metre(r) for r in pool])
        rng = np.random.default_rng(SEED)
        keys = np.log(rng.random(len(pool))) / w                  # Efraimidis–Spirakis in log form: top-n keys
        # (u ** (1 / w) underflows to 0 for normalised weights ~1e-6, leaving the pick to file order: 2026-10-20)
        pick = np.argsort(-keys)[: int(args.n * 1.05)]           # a margin for the examples that do not fit
        train, dropped = encode(tok, [pool[i] for i in pick], rule, length)
        train = train[: args.n]
    else:
        train, dropped = encode(tok, pool, rule, length, compact=True)

    val_pool = [r for r in C.read_records("val") if C.t1_pool(r)]
    order = np.random.default_rng(SEED + 1).permutation(len(val_pool))
    val, vdrop = encode(tok, [val_pool[i] for i in order[:260]], rule, length)
    val = val[:200]

    C.DATA.mkdir(exist_ok=True)
    torch.save(train, C.DATA / f"{args.name}.pt")
    if not (C.DATA / "val.pt").exists():
        torch.save(val, C.DATA / "val.pt")
    stats = {"train": len(train), "val": len(val), "pool": len(pool), "dropped_train": dict(dropped),
             "dropped_val": dict(vdrop), "canvas_rule": rule,
             "train_metres": dict(collections.Counter(e["meter"] for e in train).most_common()),
             "prompt_tokens": {"mean": float(np.mean([len(e["prompt"]) for e in train])),
                               "max": int(max(len(e["prompt"]) for e in train))},
             "poem_tokens": {"mean": float(np.mean([e["n_poem"] for e in train])),
                             "p95": float(np.percentile([e["n_poem"] for e in train], 95))}}
    out = C.DATA / ("stats.json" if args.name == "train" else f"stats_{args.name}.json")
    out.write_text(json.dumps(stats, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=1), flush=True)


if __name__ == "__main__":
    main()
