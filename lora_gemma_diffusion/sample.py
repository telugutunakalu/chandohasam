"""Free poems from DiffusionGemma (base or with a LoRA adapter), the model's own sampler (PLAN.md §3 gate 3, §4).

    ../.venv/bin/python -u sample.py --name base_smoke --n 11
    ../.venv/bin/python -u sample.py --name smoke_200 --lora runs/smoke/lora.pt --n 11

Prompts: the E6 evaluation's (metre, poem id) pairs (../diffusion_finetuning/runs/e6_120m_val), the first --n taken
round-robin across metres, each as common.prompt_ids (T1 fields, chat template, empty thinking channel). One reply
block (256 tokens) by the model's own `generate` (its sampler and generation_config), cut at the first end token.
Each poem is scored by the strict engines (metrical_decoder.evaluate): lines, gaṇa / prāsa / yati.
Writes runs/<name>/samples.jsonl (generated text: gitignored) and prints the poems.
"""
from __future__ import annotations

import argparse
import collections
import json

import torch

import common as C

REFERENCE = C.REPO / "diffusion_finetuning" / "runs" / "e6_120m_val"


def e6_prompts(n: int) -> list[dict]:
    pairs = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(REFERENCE / "results.jsonl")})
    recs = {r["id"]: r for r in C.read_records("val")}
    by_m = collections.defaultdict(list)
    for m, pid in pairs:
        by_m[m].append({**recs[pid], "eval_meter": m})
    out, k = [], 0
    while len(out) < n and any(by_m.values()):
        for m in sorted(by_m):
            if by_m[m] and len(out) < n:
                out.append(by_m[m].pop(0))
        k += 1
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--lora", default="")
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=float, default=32)
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    from metrical_decoder.evaluate import evaluate
    model, tok = C.load(resident=True)
    if args.lora:
        C.inject_lora(model, r=args.r, alpha=args.alpha)
        C.load_lora(model, args.lora)
    model.eval()
    eos = model.generation_config.eos_token_id
    eos = set(eos if isinstance(eos, (list, tuple)) else [eos]) | {0}
    out_dir = C.RUNS / args.name
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for k, r in enumerate(e6_prompts(args.n)):
        ids = torch.tensor([C.prompt_ids(tok, r)], device="cuda")
        torch.manual_seed(args.seed + k)
        with torch.no_grad():
            out = model.generate(input_ids=ids, max_new_tokens=model.config.canvas_length)
        seq = (out.sequences[0] if hasattr(out, "sequences") else out[0])[ids.shape[1]:].tolist()
        cut = next((i for i, x in enumerate(seq) if x in eos), len(seq))
        text = C.from_model(tok.decode(seq[:cut], skip_special_tokens=True).strip())
        ev = evaluate(text, r["eval_meter"])
        row = {"id": r["id"], "meter": r["eval_meter"], "text": text, "n_tokens": cut, "lines": len(ev.get("lines") or []),
               "gana": bool(ev.get("gana_strict")), "prasa": bool(ev.get("prasa_strict")), "yati": bool(ev.get("yati_strict"))}
        rows.append(row)
        print(f"\n[{k + 1}] {r['eval_meter']} ({r['id']}): {row['lines']} lines, gaṇa {row['gana']}, prāsa {row['prasa']}, "
              f"yati {row['yati']}, {cut} tokens\n{text}", flush=True)
    with open(out_dir / "samples.jsonl", "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    n = len(rows)
    print(f"\n{args.name}: {n} poems; 4-line {sum(r['lines'] == 4 for r in rows)}/{n}; gaṇa {sum(r['gana'] for r in rows)}/{n}; "
          f"all three {sum(r['gana'] and r['prasa'] and r['yati'] for r in rows)}/{n}", flush=True)


if __name__ == "__main__":
    main()
