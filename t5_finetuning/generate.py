"""Free poems for the E6 evaluation's prompts from a fine-tuned T5Gemma 2 (PLAN.md §4).

    ../.venv/bin/python -u generate.py --size 270m --model runs/t5g-270m-full/final --name e6_t5g_270m_val
    ../.venv/bin/python -u generate.py --size 4b --lora runs/t5g-4b-lora/lora.pt --r 32 --lora-mlp --name e6_t5g_4b_val
    ../.venv/bin/python -u generate.py --size 270m --name e6_t5g_270m_base_val            # the untrained base

The (metre, poem id) pairs of the E6 reference run (../diffusion_finetuning/runs/e6_120m_val: 114 val poems; or
--reference e6_120m_t1_test: 183 test poems), each prompted with common.source_text (task, metre, its rules, register,
shared line, bhāvam). E6's sampling: temperature 0.7, top-p 0.9 (the reference run's DecodeConfig), at most 320 new
tokens; --k samples per prompt (seeds 42, 43, …). Each poem is scored by the strict engines.

Writes runs/<name>/results.jsonl in the E6 row format (key, meter, topic, mode "baseline", seed, text, eval), read by
../lora_gemma_diffusion/score_e6.py; resumable by key.
"""
from __future__ import annotations

import argparse
import json
import time

import torch

import common as C


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", choices=list(C.MODELS), required=True)
    ap.add_argument("--model", default="", help="a save_pretrained folder (full fine-tuning); default: the base")
    ap.add_argument("--lora", default="", help="an adapter on the base: runs/<run>/lora.pt or a downloaded "
                    "adapter.safetensors")
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--lora-mlp", action="store_true", help="the adapter also covers the MLP projections")
    ap.add_argument("--name", required=True)
    ap.add_argument("--reference", default="e6_120m_val")
    ap.add_argument("--k", type=int, default=1)
    args = ap.parse_args()
    from metrical_decoder.evaluate import evaluate
    ref_dir = C.REPO / "diffusion_finetuning" / "runs" / args.reference
    cfg = json.loads((ref_dir / "run.json").read_text(encoding="utf-8"))["config"]
    pairs = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(ref_dir / "results.jsonl")})
    recs = {r["id"]: r for r in C.read_records("test" if "test" in args.reference else "val")}
    if args.model:
        from transformers import AutoTokenizer, T5Gemma2ForConditionalGeneration
        tok = AutoTokenizer.from_pretrained(args.model)
        model = T5Gemma2ForConditionalGeneration.from_pretrained(args.model, dtype=torch.bfloat16).to("cuda")
    else:
        model, tok = C.load(args.size)
        if args.lora:
            C.inject_lora(model, r=args.r, alpha=2 * args.r, mlp=args.lora_mlp)
            sd = C.load_adapter(args.lora)
            for n, p in model.named_parameters():
                if n in sd:
                    p.data.copy_(sd[n])
    model.eval()
    out = C.RUNS / args.name
    out.mkdir(parents=True, exist_ok=True)
    path = out / "results.jsonl"
    done = {json.loads(l)["key"] for l in open(path, encoding="utf-8")} if path.exists() else set()
    (out / "run.json").write_text(json.dumps({"size": args.size, "model": args.model, "lora": args.lora,
                                              "reference": args.reference, "k": args.k,
                                              "temperature": cfg["temperature"], "top_p": cfg["top_p"]}, indent=1) + "\n")
    t0, n = time.time(), 0
    with open(path, "a", encoding="utf-8") as fh:
        for m, pid in pairs:
            r = recs[pid]
            enc = tok(C.source_text(r), return_tensors="pt").to("cuda")
            for s in range(args.k):
                key = f"{m}|{pid}|baseline|{42 + s}"
                if key in done:
                    continue
                torch.manual_seed(42 + s)
                with torch.no_grad(), torch.autocast("cuda", dtype=torch.bfloat16):
                    o = model.generate(**enc, max_new_tokens=320, do_sample=True, temperature=cfg["temperature"],
                                       top_p=cfg["top_p"], top_k=0)
                text = tok.decode(o[0], skip_special_tokens=True).strip()
                ev = evaluate(text, m)
                fh.write(json.dumps({"key": key, "meter": m, "topic": pid, "mode": "baseline", "seed": 42 + s,
                                     "text": text, "eval": ev}, ensure_ascii=False, default=str) + "\n")
                fh.flush()
                n += 1
    print(f"{args.name}: {n} poems in {time.time() - t0:.0f} s → {path}", flush=True)


if __name__ == "__main__":
    main()
