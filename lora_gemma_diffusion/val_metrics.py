"""Validation diagnostics for the base model and the adapters (PLAN.md §4), one model load.

    ../.venv/bin/python -u val_metrics.py --adapters runs/lora-48k/lora_step_3000.pt runs/lora-48k/lora.pt

The base model is the adapter with B = 0 (exactly the untouched model), so LoRA is injected once and each adapter's
weights are swapped in. On the first --n poems of data/val.pt (E6 val, never trained on), with fixed noise per poem and
level, without self-conditioning, loss on the poem positions:
- **integrated loss:** the mean over t = 1/8 … 8/8 (an ELBO-like summary of the uniform-noise objective; not the
  model's own NELBO, whose schedule and weighting are unpublished, and not comparable with the MDLMs' NELBO: other
  tokens, other noise);
- **T1 vs T0:** the loss with the bhāvam (T1) and with an empty bhāvam line (T0, E6's form) at t = 0.25, 0.5, 0.75,
  1.0; T0 − T1 > 0 means the model uses the meaning;
- **per metre:** T1 at t = 0.5.
Writes results/val_metrics.{json,md}.
"""
from __future__ import annotations

import argparse
import collections
import json

import numpy as np
import torch

import common as C

GRID = [k / 8 for k in range(1, 9)]
GAP_T = (0.25, 0.5, 0.75, 1.0)


def poem_loss(model, prompt, canvas, n_poem, t, seed) -> float:
    g = torch.Generator(device="cuda").manual_seed(seed)
    with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
        ce = C.diffusion_loss(model, torch.tensor([prompt], device="cuda"), torch.tensor([canvas], device="cuda"),
                              t, False, g, reduce=False)[0]
    return float(ce[:n_poem].mean())


def measure(model, items) -> dict:
    t1 = {t: [] for t in GRID}
    t0 = {t: [] for t in GAP_T}
    by_m = collections.defaultdict(list)
    for k, (e, p0) in enumerate(items):
        for t in GRID:
            v = poem_loss(model, e["prompt"], e["canvas"], e["n_poem"], t, 50_000 + 100 * k + int(t * 8))
            t1[t].append(v)
            if t == 0.5:
                by_m[e["meter"]].append(v)
        for t in GAP_T:
            t0[t].append(poem_loss(model, p0, e["canvas"], e["n_poem"], t, 50_000 + 100 * k + int(t * 8)))
    return {"integrated_T1": float(np.mean([np.mean(v) for v in t1.values()])),
            "T1": {str(t): float(np.mean(v)) for t, v in t1.items()},
            "T0": {str(t): float(np.mean(v)) for t, v in t0.items()},
            "gap_T0_minus_T1": {str(t): float(np.mean(t0[t]) - np.mean(t1[t])) for t in GAP_T},
            "per_metre_T1_t0.5": {m: {"n": len(v), "loss": float(np.mean(v))} for m, v in sorted(by_m.items())}}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--adapters", nargs="*", default=[])
    ap.add_argument("--n", type=int, default=120)
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=float, default=32)
    args = ap.parse_args()
    model, tok = C.load(resident=True)
    recs = {r["id"]: r for r in C.read_records("val")}
    items = []
    for e in torch.load(C.DATA / "val.pt")[: args.n]:
        r = dict(recs[e["id"]], meaning="")                         # T0: E6's empty bhāvam line
        items.append((e, C.prompt_ids(tok, r)))
    adapters = C.inject_lora(model, r=args.r, alpha=args.alpha)
    model.eval()
    res = {"poems": len(items), "grid": GRID, "results": {}}
    for name in ["base"] + args.adapters:
        if name == "base":
            for a in {id(a): a for a in adapters.values()}.values():
                a.B.data.zero_()
        else:
            C.load_lora(model, name)
        clock = C.timer()
        res["results"][name] = m = measure(model, items)
        print(f"{name}: integrated T1 {m['integrated_T1']:.4f}; T0−T1 " +
              " ".join(f"t{t}={v:+.3f}" for t, v in m["gap_T0_minus_T1"].items()) + f" ({clock():.0f} s)", flush=True)
    out = C.HERE / "results"
    out.mkdir(exist_ok=True)
    (out / "val_metrics.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    names = list(res["results"])
    md = ["# Validation diagnostics: base vs adapters", "",
          f"{len(items)} E6 val poems (data/val.pt), loss on the poem positions (nats per Gemma token), fixed noise, no "
          "self-conditioning. Integrated = mean over t = 1/8 … 1 (an ELBO-like summary of our objective, not the "
          "model's own NELBO). T0 = the same prompt with an empty bhāvam line.", "",
          "| measure | " + " | ".join(names) + " |", "|---|" + "---|" * len(names),
          "| integrated T1 | " + " | ".join(f"{res['results'][n]['integrated_T1']:.4f}" for n in names) + " |"]
    for t in GAP_T:
        md.append(f"| T1 at t {t} | " + " | ".join(f"{res['results'][n]['T1'][str(t)]:.4f}" for n in names) + " |")
        md.append(f"| T0 − T1 at t {t} | " + " | ".join(f"{res['results'][n]['gap_T0_minus_T1'][str(t)]:+.4f}"
                                                         for n in names) + " |")
    md += ["", "Per metre (T1, t = 0.5):", "", "| metre | poems | " + " | ".join(names) + " |",
           "|---|---|" + "---|" * len(names)]
    for m, v in res["results"]["base"]["per_metre_T1_t0.5"].items():
        md.append(f"| {m} | {v['n']} | " + " | ".join(f"{res['results'][n]['per_metre_T1_t0.5'][m]['loss']:.3f}"
                                                       for n in names) + " |")
    (out / "val_metrics.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)


if __name__ == "__main__":
    main()
