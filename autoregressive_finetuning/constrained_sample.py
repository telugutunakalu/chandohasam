"""Step 4 of PLAN.md: the E6 evaluation for Nandi, exactly as the MDLM's (../diffusion_finetuning/constrained_sample.py
--e6-split val).

    ../.venv/bin/python -u constrained_sample.py --name e6_nandi_val --weights runs/nandi-t1/snapshots/ema_step_0008225.pt
    ../.venv/bin/python -u constrained_sample.py --name e6_nandi_base_val          # the base model, zero-shot
    ../.venv/bin/python -u constrained_sample.py --name e6_nandi_test --weights <snapshot> --reference e6_120m_t1_test

What is the same as the MDLM rows:
- **the poems:** the (metre, poem id) pairs of a reference MDLM run, by default ../diffusion_finetuning/runs/e6_120m_val
  (114 val poems, 11 metres; the 523M runs used the same; for test, --reference e6_120m_t1_test), minus
  results/nandi_leakage_exclude.json if step 2 listed any;
- **the decoding:** `metrical_decoder.run_grid` with that run's modes (free baseline, masking_only,
  masking_backtrack, hybrid), seed, DecodeConfig, enforcement (gaṇa, prāsa, yati; strict profile) and per-metre
  token budgets;
- **the report:** `metrical_decoder.analysis.report` into results/<name>.md and .json.

What differs, necessarily:
- **the prompt** is the T1 text of nandi.prompt_ids (the same Telugu header, ending `పద్యం:⏎`) in Nandi's tokens;
- **the vocabulary slice** is every token that decodes to Telugu, plus newline and space (nandi.token_index:
  7,394 ids), instead of the MDLM's aksharas seen ≥ 10 times. Partial-UTF-8 ids are outside it (step 1: 1.1% of
  poem tokens), so they count as not allowed;
- **the source** is metrical_decoder.hf.HFCausalLM (one token per forward pass, KV cache, prompt prefill shared by
  the modes), loaded here with the custom code; its constructor resolves models by id without trust_remote_code.

Writes runs/<name>/ (gitignored: generated poems) and results/<name>.{md,json} (numbers only).
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import torch

import nandi
from nandi import E6_RECORDS, EOS, HERE, REPO

from metrical_decoder import DecodeConfig                             # noqa: E402 (sys.path set by nandi)
from metrical_decoder.analysis import report                          # noqa: E402
from metrical_decoder.hf import HFCausalLM                            # noqa: E402
from metrical_decoder.runner import run_grid, summarize               # noqa: E402

MDLM_RUNS = REPO / "diffusion_finetuning" / "runs"
EXCLUDE = HERE / "results" / "nandi_leakage_exclude.json"
TOPIC_RE = re.compile(r"Topic \(విషయము\): (.+)")


class NandiSource(HFCausalLM):
    """HFCausalLM with Nandi loaded by nandi.load_model; prompts are the T1 prompts of held-out poems, keyed by the
    poem id that run_grid passes as the topic."""

    def __init__(self, model, index, prefixes: dict[str, list[int]], device: str = "cuda", top_k: int = 5):
        self.model_id = nandi.MODEL_ID
        self.device = torch.device(device)
        self.top_k = top_k
        self.prefill = None
        self.tokenizer = nandi.load_tokenizer()          # used by decode(ids, skip_special_tokens=False)
        self.model = model.eval()
        self.eos_ids = (EOS,)
        self.index = index
        self._slice = torch.tensor(index.ids, device=self.device)
        self._prompt_cache = {}
        self._cache = None
        self._logits = None
        self._prompt = ()
        self.generated = []
        self._worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="forward")
        self._pending = None
        self.prefixes = prefixes

    def prompt_ids(self, messages: list[dict]) -> list[int]:
        user = "\n".join(m["content"] for m in messages if isinstance(m.get("content"), str))
        return list(self.prefixes[TOPIC_RE.search(user).group(1).strip()])


def reference_poems(reference: Path) -> tuple[dict, dict]:
    """{metre: [poem ids]} of the reference E6 run, and its run.json."""
    run = json.loads((reference / "run.json").read_text(encoding="utf-8"))
    by_metre = collections.defaultdict(set)
    for line in open(reference / "results.jsonl", encoding="utf-8"):
        r = json.loads(line)
        by_metre[r["meter"]].add(r["topic"])
    excluded = set(json.loads(EXCLUDE.read_text(encoding="utf-8"))["ids"]) if EXCLUDE.exists() else set()
    poems = {m: sorted(by_metre[m] - excluded) for m in run["meters"] if by_metre[m] - excluded}
    return poems, run


def merge_runs(out: Path, parts: list[Path], meters: list[str], **extra) -> None:
    """Merge run folders into ``out`` (as ../diffusion_finetuning/constrained_sample.merge_runs)."""
    out.mkdir(parents=True, exist_ok=True)
    for name in ("results.jsonl", "traces.jsonl", "prompts.jsonl"):
        with open(out / name, "w", encoding="utf-8") as fh:
            for part in parts:
                fh.write((part / name).read_text(encoding="utf-8"))
    runs = [json.loads((part / "run.json").read_text(encoding="utf-8")) for part in parts]
    run = runs[0]
    run["meters"] = meters
    run["topics"] = {k: v for r in runs for k, v in r["topics"].items()}
    run["token_budget"] = {k: v for r in runs for k, v in r["token_budget"].items()}
    run.update(extra)
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True, help="runs/<name>/ and results/<name>.md")
    ap.add_argument("--weights", default="", help="a finetune.py EMA snapshot or a downloaded Hugging Face folder "
                    "(default: the base model)")
    ap.add_argument("--reference", default="e6_120m_val", help="the MDLM E6 run (under ../diffusion_finetuning/runs) "
                    "whose poems, budgets and decoding settings are reused")
    ap.add_argument("--meters", nargs="+", help="a subset of the reference run's metres")
    ap.add_argument("--modes", nargs="+", help="a subset of the reference run's modes (default: all)")
    ap.add_argument("--seeds", type=int, nargs="+", help="default: the reference run's seeds")
    ap.add_argument("--limit", type=int, default=0, help="at most N poems per metre (a smoke test)")
    ap.add_argument("--mask-workers", type=int, default=2, help="mask worker processes per shard")
    ap.add_argument("--shards", type=int, default=4, help="run the metres in this many processes at once")
    ap.add_argument("--shard", type=int, default=None, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    reference = MDLM_RUNS / args.reference
    poems, ref = reference_poems(reference)
    meters = [m for m in (args.meters or ref["meters"]) if m in poems]
    modes = [m for m in ref["modes"] if not args.modes or m in args.modes]
    seeds = args.seeds or ref["seeds"]
    out = HERE / "runs" / args.name
    if args.shards > 1 and args.shard is None:
        return run_shards(args, argv if argv is not None else sys.argv[1:], meters, out)
    if args.shard is not None:
        meters = meters[args.shard::args.shards]
        out = out / f"shard_{args.shard}"
        time.sleep(20 * args.shard)                      # stagger the model loads

    from finetune import wait_for_cuda
    wait_for_cuda(4)
    torch.backends.cuda.matmul.allow_tf32 = True
    model = nandi.load_model("bfloat16", "cuda", args.weights or None)
    weights = args.weights or f"{nandi.MODEL_ID}@{nandi.REVISION[:7]} (base)"
    tok = nandi.load_tokenizer()
    index = nandi.token_index(tok)
    recs = {}
    for split in ("val", "test"):
        for line in open(E6_RECORDS / f"{split}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            recs[r["id"]] = r
    prefixes = {pid: nandi.prompt_ids(recs[pid], tok=tok) for m in meters for pid in poems[m]}
    source = NandiSource(model, index, prefixes)
    cfg = DecodeConfig(**ref["config"])
    enforce = ref["enforce"]
    print(f"{args.name}: {weights}; slice {index.size:,} tokens; {len(meters)} metres, "
          f"{sum(len(poems[m]) for m in meters)} poems x {len(modes)} modes x {len(seeds)} seeds", flush=True)
    parts = []
    for meter in meters:
        ids = poems[meter][:args.limit] if args.limit else poems[meter]
        budget = ref["token_budget"][meter]
        mcfg = dataclasses.replace(cfg, max_tokens=budget, baseline_max_tokens=budget)
        run_grid(source, index, [meter], modes, [(pid, pid) for pid in ids], seeds, out / f"m_{meter}",
                 cfg=mcfg, model_name=f"nandi-mini-150m:{weights}", prasa=enforce["prasa"], yati=enforce["yati"],
                 profile=enforce["profile"], mask_workers=args.mask_workers)
        parts.append(out / f"m_{meter}")
    merge_runs(out, parts, [p.name[2:] for p in parts])
    run_json = json.loads((out / "run.json").read_text(encoding="utf-8"))
    run_json.update(weights=weights, reference=str(reference.relative_to(REPO)),
                    topic_conditioning=f"E6: the held-out poems of {args.reference}, T1 prompt (nandi.prompt_ids)",
                    slice={"tokens": index.size, "rule": "every id that decodes to Telugu (one optional leading space) "
                           "+ newline + space; partial-UTF-8 ids excluded"})
    (out / "run.json").write_text(json.dumps(run_json, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.shard is None:
        finish(out, args.name)
    return 0


def run_shards(args, argv: list[str], meters: list[str], out: Path) -> int:
    out.mkdir(parents=True, exist_ok=True)
    procs = []
    for k in range(args.shards):
        log = open(out / f"shard_{k}.log", "a", encoding="utf-8")
        procs.append(subprocess.Popen([sys.executable, __file__, *argv, "--shard", str(k)], stdout=log,
                                      stderr=subprocess.STDOUT, cwd=HERE))
    codes = [p.wait() for p in procs]
    if any(codes):
        print(f"shards exited with {codes}; see runs/{args.name}/shard_*.log", flush=True)
        return 1
    merge_runs(out, [out / f"shard_{k}" for k in range(args.shards) if (out / f"shard_{k}" / "run.json").exists()],
               meters, shards=args.shards)
    finish(out, args.name)
    return 0


def finish(out: Path, name: str) -> None:
    summarize(out)
    (HERE / "results").mkdir(exist_ok=True)
    print(report([out], out=HERE / "results" / f"{name}.md"), flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
