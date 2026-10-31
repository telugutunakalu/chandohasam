"""The grid's Gemma-4 rows (PLAN.md §2 rows 3–6): an instruction-tuned chat model through our constrained decoder.

    E6_RECORDS_DIR=prompts/e6_p1/records ../.venv/bin/python -u run_hf.py --model google/gemma-4-E4B-it \
        --name gemma4_e4b_free --modes baseline --seeds 42 43
    E6_RECORDS_DIR=prompts/e6_p1/records ../.venv/bin/python -u run_hf.py --model google/gemma-4-E4B-it \
        --name gemma4_e4b_constrained --modes masking_backtrack --seeds 42

- **The prompt:** the September grids' instruction prompt (metrical_decoder.prompts.build_messages: the metre, its
  rules, the output format), with the poem's bhāvam — under $E6_RECORDS_DIR the grid's prompt — on one line as the
  topic; metrical_decoder.hf.HFCausalLM (chat template, thinking off).
- **The poems and decoding:** the (metre, poem id) pairs of the reference MDLM run (--reference, default
  e6_120m_t1_test: the grid's 183 source poems), its DecodeConfig, enforcement and per-metre token budgets — as the
  T5 and Nandi rows.

Writes runs/<name>/ (results.jsonl, traces, run.json; resumable per metre) and results/<name>.md.
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "meter_engine"))
from metrical_decoder import DecodeConfig                    # noqa: E402
from metrical_decoder.analysis import report                 # noqa: E402
from metrical_decoder.hf import HFCausalLM                   # noqa: E402
from metrical_decoder.runner import run_grid, summarize      # noqa: E402

RECORDS = Path(os.environ.get("E6_RECORDS_DIR") or REPO / "diffusion_finetuning" / "data" / "e6" / "records")


def evict_page_cache(need_gb: float = 70) -> None:
    """On the GB10 CUDA counts cached file pages as used (its free memory is MemFree): when it reports less than
    ``need_gb`` free, drop the page cache of large files (../diffusion_pretraining/mdlm/checkpoint_eval.py)."""
    import torch
    if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] / 2**30 < need_gb:
        sys.path.insert(0, str(REPO / "diffusion_pretraining"))
        from mdlm.checkpoint_eval import _evict_large_files
        _evict_large_files()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", required=True, help="a Hugging Face id in the local cache")
    ap.add_argument("--name", required=True)
    ap.add_argument("--reference", default="e6_120m_t1_test")
    ap.add_argument("--modes", nargs="+", default=["baseline", "masking_backtrack"])
    ap.add_argument("--seeds", type=int, nargs="+", default=[42])
    ap.add_argument("--meters", nargs="+")
    ap.add_argument("--limit", type=int, default=0, help="at most N poems per metre (a smoke test)")
    ap.add_argument("--mask-workers", type=int, default=4)
    args = ap.parse_args()

    ref_dir = REPO / "diffusion_finetuning" / "runs" / args.reference
    ref = json.loads((ref_dir / "run.json").read_text(encoding="utf-8"))
    poems = collections.defaultdict(set)
    for line in open(ref_dir / "results.jsonl", encoding="utf-8"):
        r = json.loads(line)
        poems[r["meter"]].add(r["topic"])
    meters = [m for m in (args.meters or ref["meters"]) if poems[m]]
    split = "test" if "test" in args.reference else "val"
    recs = {}
    for line in open(RECORDS / f"{split}.jsonl", encoding="utf-8"):
        r = json.loads(line)
        recs[r["id"]] = r
    evict_page_cache()
    source = HFCausalLM(args.model)
    cfg = DecodeConfig(**ref["config"])
    enforce = ref["enforce"]
    out = HERE / "runs" / args.name
    print(f"{args.name}: {args.model}; records {RECORDS}; slice {source.index.size:,} tokens; {len(meters)} metres, "
          f"{sum(len(poems[m]) for m in meters)} poems; modes {args.modes}; seeds {args.seeds}", flush=True)
    t0 = time.time()
    parts = []
    for meter in meters:
        ids = sorted(poems[meter])[: args.limit] if args.limit else sorted(poems[meter])
        budget = ref["token_budget"][meter]
        mcfg = dataclasses.replace(cfg, max_tokens=budget, baseline_max_tokens=budget)
        topics = [(pid, " ".join(recs[pid]["meaning"].split())) for pid in ids]
        run_grid(source, source.index, [meter], args.modes, topics, args.seeds, out / f"m_{meter}", cfg=mcfg,
                 model_name=args.model, prasa=enforce["prasa"], yati=enforce["yati"], profile=enforce["profile"],
                 mask_workers=args.mask_workers)
        parts.append(out / f"m_{meter}")
    for name in ("results.jsonl", "traces.jsonl", "prompts.jsonl"):
        with open(out / name, "w", encoding="utf-8") as fh:
            for part in parts:
                if (part / name).exists():
                    fh.write((part / name).read_text(encoding="utf-8"))
    runs = [json.loads((part / "run.json").read_text(encoding="utf-8")) for part in parts]
    run = {**runs[0], "meters": meters, "modes": args.modes, "seeds": args.seeds,
           "topics": {k: v for r in runs for k, v in r["topics"].items()},
           "token_budget": {k: v for r in runs for k, v in r["token_budget"].items()},
           "records": str(RECORDS), "reference": str(ref_dir.relative_to(REPO)),
           "topic_conditioning": "the September instruction prompt; topic = the record's bhāvam (the grid's prompt)"}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    summarize(out)
    (HERE / "results").mkdir(exist_ok=True)
    print(report([out], out=HERE / "results" / f"{args.name}.md"), flush=True)
    print(f"{args.name}: {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
