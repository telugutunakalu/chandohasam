"""Memorisation over the meaning → poem training, the same measure for the three models (figures: plot_curves.py).

    ../.venv/bin/python -u exposure_probe.py

At every saved EMA snapshot of the meaning → poem training, the T1 loss (the poem given metre + meaning, nats per MDLM
target token, E6's unit) on two fixed sets of the same records for every model:
- **train:** 900 training records of the T1 pool in the register and meaning source of val (ప్రాచీన, గ్రంథం), a
  fixed random sample;
- **val:** the val records (Bhagavatam skandhas 1, 2, 7; held out).
A gap (val − train) that grows during training means the model is fitting its training poems more than it
generalises. The level of the gap also holds the difference between the two sets, so its growth is what counts.
Only records whose T1 canvas fits the MDLM's 512 tokens are used, so all models are scored on the same poems.

- **MDLM 120M / 523M:** ft.train.evaluate_stage2 (NELBO with fixed times and masks) on the snapshots of e6-s2-<tag>
  (steps 1,000–11,000 and the final checkpoint, 11,748) and e6-t1-<tag> (1,000, 2,000 and the final, 2,350).
  The MDLM's stage 1 had already shown every training poem three times (poem + meaning documents), so there is no
  "never seen" poem for it.
- **Nandi:** nandi.evaluate_t1 on the snapshots of nandi-t1 (1,000–8,000 and the final, 8,225). Also, since Nandi saw
  no poem before this run: training examples drawn at least once so far against examples never drawn yet, matched by
  metre (from the replayed draws of finetune.Batches).
- **x axis:** passes over the T1 pool (300,763): E6 stage 2 draws 64 T1 examples per step (half of 128), the T1 phase
  and Nandi 128.

Writes results/exposure_probe.json (numbers only).
"""
from __future__ import annotations

import json
import random
import time
from pathlib import Path

import numpy as np
import torch

import nandi
from nandi import E6_RECORDS, HERE, REPO

DF = REPO / "diffusion_finetuning"
T1_POOL = 300_763
N_TRAIN = 900
SEED = 20261018
OUT = HERE / "results" / "exposure_probe.json"


def train_sample() -> list[dict]:
    rng, keep, seen = random.Random(SEED), [], 0
    for line in open(E6_RECORDS / "train.jsonl", encoding="utf-8"):
        r = json.loads(line)
        if not (nandi.in_t1_pool(r) and r.get("register") == "ప్రాచీన" and r.get("meaning_src") == "గ్రంథం"):
            continue
        seen += 1
        if len(keep) < 2 * N_TRAIN:
            keep.append(r)
        elif rng.random() < 2 * N_TRAIN / seen:
            keep[rng.randrange(2 * N_TRAIN)] = r
    return keep                        # twice N_TRAIN: some do not fit the MDLM canvas


def mdlm_sets(recs: list[dict]):
    """T1 canvases (ft.canvas) of the records that fit, and their ids."""
    from common import tokenizer
    from ft.canvas import Vocab, build, tokenise_record
    v = Vocab(tokenizer())
    rng = np.random.default_rng(0)
    rows, ids = [], []
    for r in recs:
        c = build("T1", v, tokenise_record(v, r), rng)
        if c is not None:
            rows.append(("T1", c[0], c[1]))
            ids.append(r["id"])
    return rows, ids


def mdlm_points(tag: str, sets: dict, device) -> list[dict]:
    from common import load_model, output_bias, tokenizer
    from ft.train import evaluate_stage2
    tok = tokenizer()
    mask_id = tok.special_to_id["<mask>"]
    specs = []
    for run, base, per_step in ((f"e6-s2-{tag}", 0.0, 64), (f"e6-t1-{tag}", 11748 * 64 / T1_POOL, 128)):
        for snap in sorted((DF / "runs" / run / "snapshots").glob("ema_step_*.pt")):
            specs.append((str(snap), base + int(snap.stem.split("_")[-1]) * per_step / T1_POOL, run))
        last = 11748 if run.startswith("e6-s2") else 2350
        specs.append((str(DF / "runs" / run), base + last * per_step / T1_POOL, run))     # the final checkpoint
    out = []
    for spec, x, run in specs:
        t0 = time.time()
        model, weights = load_model(spec, "cpu")
        model = model.to(device).eval()
        bias = output_bias(model.cfg, tok, device)
        row = {"model": f"mdlm-{tag}", "run": run, "weights": weights, "passes": x}
        for name, rows in sets.items():
            row[f"T1_{name}"] = evaluate_stage2(model, {"T1": rows}, mask_id, bias, 16384, device)["val_nelbo/T1"]
        row["gap"] = row["T1_val"] - row["T1_train"]
        out.append(row)
        print(f"{row['model']} {weights}: passes {x:.2f} train {row['T1_train']:.4f} val {row['T1_val']:.4f} "
              f"gap {row['gap']:.4f} ({time.time() - t0:.0f} s)", flush=True)
        del model
        torch.cuda.empty_cache()
    return out


def nandi_points(train_recs: list[dict], val_recs: list[dict], device) -> list[dict]:
    import finetune
    tok = nandi.load_tokenizer()
    items = {"train": nandi.val_items(train_recs, tok), "val": nandi.val_items(val_recs, tok)}
    pool = finetune.load_pool()
    batches = finetune.Batches(pool, 128, SEED)
    meters = np.array([m or "" for m in pool["meters"]])
    run = HERE / "runs" / "nandi-t1"
    total = json.loads((run / "config.json").read_text())["total_steps"]
    snaps = sorted(run.glob("snapshots/ema_step_*.pt"))
    counts, done = np.zeros(len(meters), dtype=np.int64), 0
    out = []
    for snap in snaps:
        step = int(snap.stem.split("_")[-1])
        for s in range(done, step):
            np.add.at(counts, batches.indices(s), 1)
        done = step
        model = nandi.load_model("bfloat16", "cuda", str(snap)).eval()
        row = {"model": "nandi", "run": "nandi-t1", "weights": f"{snap.name}", "passes": step * 128 / T1_POOL,
               "final": step == total}
        for name, its in items.items():
            row[f"T1_{name}"] = nandi.evaluate_t1(model, its, device)["val_nll/T1"]
        row["gap"] = row["T1_val"] - row["T1_train"]
        rng = np.random.default_rng(7)
        seen_ix, unseen_ix = [], []
        for m in np.unique(meters):
            u = np.where((meters == m) & (counts == 0))[0]
            s1 = np.where((meters == m) & (counts >= 1))[0]
            k = min(len(u), len(s1), 120)
            if k:
                unseen_ix += list(rng.choice(u, k, replace=False))
                seen_ix += list(rng.choice(s1, k, replace=False))

        def tok_nll(ix):
            seqs = [(pool["ids"][pool["offsets"][i]:pool["offsets"][i + 1]].tolist(),
                     pool["mask"][pool["offsets"][i]:pool["offsets"][i + 1]].tolist()) for i in ix]
            sums = nandi.nll_sums(model, seqs, device)
            return sum(a for a, _ in sums) / sum(n for _, n in sums)

        row |= {"seen_nll_tok": tok_nll(seen_ix), "unseen_nll_tok": tok_nll(unseen_ix), "matched_pairs": len(seen_ix),
                "unseen_pct": float(np.mean(counts == 0) * 100)}
        out.append(row)
        print(f"nandi {snap.name}: passes {row['passes']:.2f} train {row['T1_train']:.4f} val {row['T1_val']:.4f} "
              f"gap {row['gap']:.4f}; seen {row['seen_nll_tok']:.3f} vs unseen {row['unseen_nll_tok']:.3f} "
              f"per Nandi token ({len(seen_ix)} pairs)", flush=True)
        del model
        torch.cuda.empty_cache()
    return out


def main() -> None:
    from finetune import wait_for_cuda
    torch.backends.cuda.matmul.allow_tf32 = True
    device = torch.device("cuda")
    wait_for_cuda(8)
    train_recs = train_sample()
    val_recs = [json.loads(l) for l in open(E6_RECORDS / "val.jsonl", encoding="utf-8")]
    val_recs = [r for r in val_recs if nandi.in_t1_pool(r)]
    tr_rows, tr_ids = mdlm_sets(train_recs)
    va_rows, va_ids = mdlm_sets(val_recs)
    tr_rows, tr_ids = tr_rows[:N_TRAIN], tr_ids[:N_TRAIN]
    keep_tr, keep_va = set(tr_ids), set(va_ids)
    train_recs = [r for r in train_recs if r["id"] in keep_tr]
    val_recs = [r for r in val_recs if r["id"] in keep_va]
    print(f"exposure probe: {len(train_recs)} train and {len(val_recs)} val records (the same for every model)", flush=True)
    points = []
    for tag in ("120m", "523m"):
        points += mdlm_points(tag, {"train": tr_rows, "val": va_rows}, device)
    points += nandi_points(train_recs, val_recs, device)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"train_records": len(train_recs), "val_records": len(val_recs), "seed": SEED,
                               "unit": "nats per MDLM target token (T1); seen/unseen: per Nandi token",
                               "points": points}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT}", flush=True)


if __name__ == "__main__":
    main()
