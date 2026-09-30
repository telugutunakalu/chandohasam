#!/usr/bin/env python3
"""
EXP-19 step 1-2: greedy bhavam -> poem generation with per-step logging, rerun on gemma-4-E2B-it.

Spec: experiments/EXP-19-generation-time-tracking.md. Model loading and the 200-poem balanced sample
are EXP-35's (experiments/scripts/exp35_surprisal.py).

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp19_generate.py OUT_DIR [--direction EXP22_DIR]

Prompt. The project's own prompt for the metre (experiments/runs/2026-09-24_e4b_baseline/prompts.jsonl:
the system message and the metre's rules generated from the catalogue), with the poem's bhavam in
place of the topic, in the model's chat template. The output is plain text (the four pādas), as the
spec's replication notes recommend; the pipeline's run asked for JSON.

Decoding: a manual greedy loop, next = argmax of the raw logits (no sampling, no processors), KV cache,
at most 1,000 new tokens, stopping at the model's end tokens.

Per step: the token, the entropy of the full-vocabulary distribution, the top-1 minus top-2
log-probability margin, the top-1 probability, and (for the decay curve, step 7) the cosine between
the hidden state that produced the step's logits and EXP-22's coarse chandas direction, at every
hidden-state index. Per-step metre satisfaction, sandhi distances and the validator verdict are
computed afterwards from the text (exp19_analyse.py).

Writes OUT_DIR/run.json and OUT_DIR/generations.jsonl (one row per poem; resumable on the id).
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

PROMPTS = ROOT / "experiments" / "runs" / "2026-09-24_e4b_baseline" / "prompts.jsonl"
PROMPT_METRE = {"aataveladi": "ataveladi", "mattakokila": "mattakokilamu", "shardulavikriditamu": "sardulavikriditamu"}
MAX_NEW = 1000


def build_messages(templates: dict, metre: str, bhavam: str) -> list[dict]:
    t = templates[PROMPT_METRE.get(metre, metre)]
    system, user = t[0]["content"], t[1]["content"]
    head, sep, tail = user.partition("\n\nTopic (విషయము): ")
    assert sep, "prompt layout changed"
    instruction = tail.split("\n\n", 1)[1]
    return [{"role": "system", "content": system},
            {"role": "user", "content": f"{head}\n\nMeaning (భావము): {bhavam}\n\n{instruction}"}]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--direction", type=Path, default=ROOT / "experiments" / "exp22" / "2026-09-29_pairs")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    import numpy as np
    import torch
    import transformers
    from transformers import AutoTokenizer, GenerationConfig
    import exp35_surprisal as e35

    out = args.out_dir
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, eligible, metres = e35.balanced_sample(args.seed)
    if args.limit:
        sample = sample[: args.limit]
    templates = {}
    for line in PROMPTS.open(encoding="utf-8"):
        r = json.loads(line)
        templates.setdefault(r["meter"], r["messages"])
    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    gen_cfg = GenerationConfig.from_pretrained(snap)
    eos = gen_cfg.eos_token_id if isinstance(gen_cfg.eos_token_id, list) else [gen_cfg.eos_token_id]
    model, cfg = e35.build_model(snap, args.device, args.seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)
    direction = torch.tensor(np.load(args.direction / "directions.npz")["coarse"], device=args.device)   # [36, hidden]
    direction = direction / direction.norm(dim=-1, keepdim=True)

    gens = out / "generations.jsonl"
    done = {json.loads(line)["id"] for line in gens.open(encoding="utf-8")} if gens.exists() else set()

    def forward(ids, cache):
        x = torch.tensor([ids])
        emb = model.model.embed_tokens(x.to(args.device))
        pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(args.device)
        return model(inputs_embeds=emb, per_layer_inputs=pli, past_key_values=cache, use_cache=True,
                     output_hidden_states=True, logits_to_keep=1)

    with gens.open("a", encoding="utf-8") as fh, torch.no_grad():
        for n, r in enumerate(sample):
            if r["id"] in done:
                continue
            ts = time.time()
            messages = build_messages(templates, r["metre_roman"], e35.bhavam_text(r))
            prompt_ids = tok.apply_chat_template(messages, add_generation_prompt=True, tokenize=True, return_dict=False)
            if isinstance(prompt_ids, dict):
                prompt_ids = prompt_ids["input_ids"]
            o = forward(list(prompt_ids), None)
            cache = o.past_key_values
            stats, ids, stop = [], [], "max_new_tokens"
            for _ in range(MAX_NEW):
                lp = torch.log_softmax(o.logits[0, -1].float(), dim=-1)
                top = lp.topk(2)
                h = torch.stack([hs[0, -1] for hs in o.hidden_states]).float()        # [36, hidden]
                cos = (h / h.norm(dim=-1, keepdim=True) * direction).sum(-1)
                stats.append(torch.cat([(-(lp.exp() * lp).sum()).view(1), (top.values[0] - top.values[1]).view(1),
                                        top.values[0].exp().view(1), cos]))           # kept on the GPU
                nxt = int(top.indices[0])                                               # the one sync per step
                ids.append(nxt)
                if nxt in eos:
                    stop = "eos"
                    break
                o = forward([nxt], cache)
                cache = o.past_key_values
            S = torch.stack(stats).cpu().tolist()
            steps = [{"entropy": round(v[0], 5), "margin": round(v[1], 5), "p_top1": round(v[2], 5),
                      "cos_coarse": [round(c, 4) for c in v[3:]]} for v in S]
            row = {"id": r["id"], "metre": r["metre_roman"], "prompt_tokens": len(prompt_ids), "stop": stop,
                   "tokens": ids, "pieces": tok.convert_ids_to_tokens(ids),
                   "text": tok.decode([i for i in ids if i not in eos], skip_special_tokens=True),
                   "steps": steps, "seconds": round(time.time() - ts, 2)}
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            print(f"  {n + 1}/{len(sample)} {r['id']} {stop} tokens={len(ids)} {time.time() - ts:.1f}s", flush=True)

    run = {"experiment": "EXP-19 (generation)", "date": datetime.date.today().isoformat(),
           "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "load": load_report},
           "device": {"torch": torch.__version__, "transformers": transformers.__version__},
           "prompt": f"system + metre rules from {PROMPTS.relative_to(ROOT)} (topic replaced by the bhavam, first 2,000 chars), chat template",
           "decoding": {"type": "manual greedy loop, argmax of raw logits, KV cache", "max_new_tokens": MAX_NEW, "eos": eos},
           "direction": f"EXP-22 coarse direction, {args.direction.relative_to(ROOT)}/directions.npz",
           "seed": args.seed, "sample": {"rule": "EXP-35 Inputs 1", "size": len(sample)},
           "seconds": round(time.time() - t0, 1)}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
