#!/usr/bin/env python3
"""
EXP-08 step 1, third condition: the natural-prose reordering control, produced by gemma-4-E2B-it.

Spec: experiments/EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md ("an LLM prompted to
reorder into natural prose word order, changing nothing else. Verify the word multiset is unchanged").

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp08_prose_control.py OUT_DIR --exp08 EXP08_DIR

1. Reorder: for each poem of EXP-35's 200-poem sample, the model is asked (chat template, greedy,
   at most 400 new tokens) to put the poem's words into natural prose order without changing any word.
2. Verify: the reply's whitespace-separated words must be exactly the poem's words as a multiset.
   A reply that fails is rejected (no repair, no retry); the yield is reported.
3. Layout: an accepted order is put back into the poem's lines (each line keeps its word count), as the
   shuffle control is, so genuine, shuffle and prose differ only in word order.
4. Score: teacher-forced NLL with `<bos>` (EXP-35's scorer), compared on the accepted poems with the
   genuine and shuffle NLLs of the EXP-08 run (per_poem.csv, condition bos).
Writes OUT_DIR/run.json, reorderings.jsonl, traces.jsonl, summary.json.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import sys
import time
from collections import Counter
from pathlib import Path
from statistics import mean

sys.path.insert(0, str(Path(__file__).resolve().parent))
MAX_NEW = 400
SYSTEM = "You are an expert in Telugu grammar and classical Telugu poetry."
INSTRUCTION = ("Rewrite the following Telugu poem as a single prose sentence by putting its words into natural "
               "prose word order. Change nothing else: use exactly the same words, each written exactly as it "
               "appears (including any punctuation attached to it), and do not add, remove, split, join or "
               "change any word. Output only the reordered words on one line, with no explanation.\n\n")


def relayout(order: list[str], genuine: str) -> str:
    sizes = [len(ln.split()) for ln in genuine.split("\n")]
    out, i = [], 0
    for n in sizes:
        out.append(" ".join(order[i:i + n]))
        i += n
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--exp08", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    import numpy as np
    import torch
    import transformers
    from scipy import stats
    from transformers import AutoTokenizer, GenerationConfig
    import exp35_surprisal as e35

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, _, _ = e35.balanced_sample(args.seed)
    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    gen_cfg = GenerationConfig.from_pretrained(snap)
    eos = gen_cfg.eos_token_id if isinstance(gen_cfg.eos_token_id, list) else [gen_cfg.eos_token_id]
    model, cfg = e35.build_model(snap, args.device, args.seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)

    def forward(ids, cache):
        x = torch.tensor([ids])
        emb = model.model.embed_tokens(x.to(args.device))
        pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(args.device)
        return model(inputs_embeds=emb, per_layer_inputs=pli, past_key_values=cache, use_cache=True, logits_to_keep=1)

    reorder_file = out / "reorderings.jsonl"
    done = {json.loads(l)["id"]: json.loads(l) for l in reorder_file.open(encoding="utf-8")} if reorder_file.exists() else {}
    with reorder_file.open("a", encoding="utf-8") as fh, torch.no_grad():
        for n, r in enumerate(sample):
            if r["id"] in done:
                continue
            genuine = e35.poem_text(r)
            msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": INSTRUCTION + genuine}]
            prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=False)
            if isinstance(prompt, dict):
                prompt = prompt["input_ids"]
            o = forward(list(prompt), None)
            ids = []
            for _ in range(MAX_NEW):
                nxt = int(o.logits[0, -1].argmax())
                if nxt in eos:
                    break
                ids.append(nxt)
                o = forward([nxt], o.past_key_values)
            reply = tok.decode(ids, skip_special_tokens=True).strip()
            words, want = reply.split(), genuine.split()
            ok = Counter(words) == Counter(want)
            row = {"id": r["id"], "metre": r["metre_roman"], "reply": reply, "accepted": ok,
                   "same_order": ok and words == want,
                   "prose": relayout(words, genuine) if ok else None,
                   "missing": sum((Counter(want) - Counter(words)).values()), "extra": sum((Counter(words) - Counter(want)).values())}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            done[r["id"]] = row
            print(f"  {n + 1}/{len(sample)} {r['id']} accepted={ok}", flush=True)

    accepted = [v for v in done.values() if v["accepted"] and not v["same_order"]]
    traces = out / "traces.jsonl"
    scored = {json.loads(l)["id"]: json.loads(l) for l in traces.open(encoding="utf-8")} if traces.exists() else {}
    with traces.open("a", encoding="utf-8") as fh:
        for v in accepted:
            if v["id"] in scored:
                continue
            enc = tok(v["prose"], add_special_tokens=False, return_offsets_mapping=True)
            res = e35.score(model, ple, cfg, enc["input_ids"], [tok.bos_token_id], args.device)
            row = {"id": v["id"], "text": v["prose"], "tokens": enc["input_ids"],
                   "offsets": [list(o) for o in enc["offset_mapping"]], **res}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            scored[v["id"]] = row

    e8 = {r["id"]: r for r in csv.DictReader((args.exp08 / "per_poem.csv").open(encoding="utf-8")) if r["condition"] == "bos"}
    ids_ = sorted(scored)
    g = np.array([float(e8[i]["nll_genuine"]) for i in ids_])
    s = np.array([float(e8[i]["nll_shuffle"]) for i in ids_])
    p = np.array([mean(v for v in scored[i]["s_true"] if v is not None) for i in ids_])

    def contrast(a, b):
        d = a - b
        rng = np.random.default_rng(0)
        boot = rng.choice(d, size=(10_000, len(d))).mean(axis=1)
        return {"delta_mean": round(float(d.mean()), 4), "delta_median": round(float(np.median(d)), 4),
                "ci95": [round(float(np.percentile(boot, 2.5)), 4), round(float(np.percentile(boot, 97.5)), 4)],
                "first_preferred": int((d < 0).sum()), "second_preferred": int((d > 0).sum()),
                "wilcoxon_p": float(stats.wilcoxon(d).pvalue),
                "pearson": round(float(stats.pearsonr(a, b).statistic), 4), "spearman": round(float(stats.spearmanr(a, b).statistic), 4)}

    rows = list(done.values())
    summary = {
        "reorderings": {"poems": len(rows), "accepted": sum(v["accepted"] for v in rows),
                        "accepted_but_unchanged": sum(v["same_order"] for v in rows), "usable": len(accepted),
                        "by_metre": {m: sum(v["accepted"] and not v["same_order"] for v in rows if v["metre"] == m)
                                     for m in sorted({v["metre"] for v in rows})}},
        "scored_poems": len(ids_),
        "nll_mean": {"genuine": round(float(g.mean()), 4), "shuffle": round(float(s.mean()), 4), "prose": round(float(p.mean()), 4)},
        "genuine_vs_prose": contrast(g, p) if len(ids_) >= 5 else None,
        "genuine_vs_shuffle_same_poems": contrast(g, s) if len(ids_) >= 5 else None,
        "prose_vs_shuffle": contrast(p, s) if len(ids_) >= 5 else None,
        "note": "delta = NLL(first) - NLL(second); 'first_preferred' counts poems where the first order has the lower NLL",
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    run = {"experiment": "EXP-08 prose control", "date": datetime.date.today().isoformat(),
           "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "load": load_report},
           "device": {"torch": torch.__version__, "transformers": transformers.__version__},
           "reordering_prompt": {"system": SYSTEM, "user": INSTRUCTION + "<poem>"}, "decoding": f"greedy, at most {MAX_NEW} new tokens",
           "verification": "exact multiset of whitespace-separated words; rejected replies are not repaired",
           "layout": "accepted order put back into the poem's lines (same word count per line)",
           "scoring": "<bos> + text, EXP-35 scorer", "seconds": round(time.time() - t0, 1)}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
