"""E3: the §16 grid of constrained decoding with our masked diffusion model.

    ../.venv/bin/python constrained_sample.py --model pilot --name e3_pilot
    ../.venv/bin/python constrained_sample.py --model runs/e2_pretrained/final.pt --name e3_e2_pretrained

The grid is the one of meter_engine/CONSTRAINED_DECODING_PLAN.md §16, read from the 26B run
(experiments/runs/2026-09-26_g26b/run.json):
- 37 meters × topics T1–T3 × seeds 42–70;
- the free baseline and the three constrained strategies;
- gaṇa, prāsa and yati enforced under the strict profile;
- the same DecodeConfig (temperature 0.7, top-p 0.9, …).
`metrical_decoder` runs the grid unchanged (`run_grid`, `decode`, `evaluate`); this file only supplies the model.

How the model is used: commitment is left to right, as for the autoregressive rows. At each step the
canvas holds the committed tokens followed by <mask> up to 512 positions, and the model's prediction
at the first masked position is the next-token distribution. A masked diffusion model is trained to
fill any position given the visible ones, so this is a proper conditional of the prefix. No cache: one
forward pass per token, cheap at 120M.

Two choices differ from the Gemma runs, both recorded in run.json:
- **The vocabulary slice** is the aksharas that occur at least --min-count (default 10) times in the poem
  train split, plus space and newline: 4,110 tokens covering 99.94% of poem tokens (all 10,535 aksharas
  that occur: 100%), instead of every Telugu token (45,262). A mask steps the enforcer once per token of
  the slice, ~0.5 s per mask over 10,535 tokens on 4 workers with the prāsa and yati registers. Tokens
  outside the slice count as not allowed; the whole-vocabulary statistics (log-probability, rank,
  entropy, mass on allowed tokens) still use the full distribution.
- **The topic.** The model follows no instructions, so the topic is placed before the poem as a prose
  document of its own: <bos> topic <eos> <bos> poem. Without it the three topics would repeat the same
  poems for each seed.

E6 mode (--e6-split val|test): the prompts are held-out poems of ft.build_data's split (data/e6/records): for each
grid metre, up to --e6-per-metre poems in that metre (a fixed sample), each prompted with its own metre header and
meaning in the T1 layout the E6 models train on (ft.canvas: ఛందస్సు, శైలి, [సమస్య/మకుటం], భావం (src), పద్యం). The
topic key is the poem's id, so every output can be set beside its gold poem. Only poems whose prompt plus 1.5x the
gold poem's tokens fit the 512-token canvas are used; a metre's generation budget is the canvas less its longest
prompt. Seed 42 unless --seeds is given.

Writes runs/<name>/ (run.json, prompts.jsonl, results.jsonl, traces.jsonl, summary.md; gitignored, as
they hold generated poems) and results/<name>.md and .json: the per-mode report of
`metrical_decoder.analysis` (numbers only).
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import json
import random
import re
import sys
import time
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Sequence

import numpy as np
import torch

from common import HERE, REPO, TOKENS, load_model, output_bias, tokenizer, wait_for_memory

sys.path.insert(0, str(REPO / "meter_engine"))
from metrical_decoder import DecodeConfig, TokenIndex                         # noqa: E402
from metrical_decoder.analysis import report                                  # noqa: E402
from metrical_decoder.runner import run_grid, summarize                       # noqa: E402
from metrical_decoder.sources import Distribution                             # noqa: E402
from metrical_decoder.vocab import TELUGU_TOKEN                               # noqa: E402

REFERENCE_RUN = REPO / "experiments" / "runs" / "2026-09-26_g26b" / "run.json"
CANVAS = 512
MAX_PREFIX = 48                       # <bos> topic <eos> [<bos> metre <eos>] <bos>
MAX_TOKENS = 472                      # constrained and baseline budgets: at least twice any poem (the same in every E3 run)
TOPIC_RE = re.compile(r"Topic \(విషయము\): (.+)")
METRE_RE = re.compile(r"Write a Telugu padyam in the meter (.+?) \(([a-z_]+)\)\.")
E6_DATA = HERE / "data" / "e6"


def e6_prompts(tok, split: str, per_metre: int, seed: int, meters: Sequence[str], data_dir: Path,
               only: dict | None = None) -> dict:
    """E6: {grid metre: [(poem id, prompt ids)]}: held-out poems in that metre, each with the T1 canvas prefix of
    ft.canvas (bos, metre, register, shared line, meaning, poem key), a fixed sample of at most ``per_metre``.
    ``only`` ({metre: poem ids}, the pairs of a reference run): exactly those poems, unsampled — the full grid's
    prompts change the prefixes, so the fit rule could otherwise change the sample."""
    from ft.canvas import Vocab, tokenise_record
    v = Vocab(tok)
    leak = data_dir / "leakage.json"                  # poems found in the pretraining corpus are never used
    seen = {k for k, x in json.loads(leak.read_text())["items"].items() if x["poem"]} if leak.exists() else set()
    by_metre: dict[str, list] = collections.defaultdict(list)
    for line in (data_dir / "records" / f"{split}.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["status"] != "agree" or not r.get("meaning") or not r.get("lines") or r["id"] in seen:
            continue
        m = r.get("meter") or ""
        key = m if m in meters else ("seesamu" if m.startswith("seesamu") and "seesamu" in meters else None)
        if key is None:
            continue
        if only is not None and r["id"] not in only.get(key, ()):
            continue
        rec = tokenise_record(v, r)
        prefix = [v.bos] + [int(x) for part in (rec.metre_head, rec.style_head, rec.samasya_head, rec.meaning_line,
                                                 v.poem_head) if part is not None for x in part]
        gold = sum(len(ln) for ln in rec.lines) + len(rec.lines)
        if only is not None or len(prefix) + 1.5 * gold <= CANVAS:
            by_metre[key].append((r["id"], prefix))
    if only is not None:
        return {m: sorted(items) for m, items in by_metre.items()}
    rng = random.Random(seed)
    return {m: sorted(rng.sample(items, min(per_metre, len(items)))) for m, items in by_metre.items()}


def merge_runs(out: Path, parts: list[Path], meters: list[str], **extra) -> None:
    """Merge run folders (shards, or E6's per-metre runs) into ``out``."""
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


def poem_slice(tok, min_count: int) -> TokenIndex:
    """Aksharas that occur at least ``min_count`` times in the poem train split, plus newline and space."""
    counts = np.bincount(np.fromfile(TOKENS / "poems" / "train.bin", dtype=np.uint16), minlength=tok.vocab_size)
    pairs = [(i, tok.id_to_str[i]) for i in range(tok.vocab_size)
             if counts[i] >= min_count and TELUGU_TOKEN.match(tok.id_to_str[i])]
    nl, sp = tok.encode("\n"), tok.encode(" ")
    assert len(nl) == 1 and len(sp) == 1, "newline and space must be single tokens"
    return TokenIndex.from_texts(pairs + [(nl[0], "\n"), (sp[0], " ")], eos_ids=[tok.eos_id])


class MDLMSource:
    """Our masked diffusion model as a metrical_decoder LogitsSource (left-to-right commitment).

    ``push`` starts the next forward pass on a worker thread and returns, so it runs while the decoder
    computes the next mask (as in metrical_decoder.hf)."""

    def __init__(self, model, tok, index: TokenIndex, device, top_k: int = 5, metre_tag: bool = False):
        self.model, self.tok, self.index, self.device, self.top_k = model, tok, index, device, top_k
        self.metre_tag = metre_tag            # E5: the metre's name as a document right before the poem
        self.mask_id = tok.special_to_id["<mask>"]
        self.bias = output_bias(model.cfg, tok, device)[: tok.vocab_size]
        self._slice = torch.tensor(index.ids, device=device)
        self.prefix: list[int] = [tok.bos_id]
        self.prefixes: dict[str, list[int]] = {}     # E6: poem id -> T1 prompt ids
        self.generated: list[int] = []
        self._logits: Optional[torch.Tensor] = None
        self._worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="forward")
        self._pending: Optional[Future] = None

    def prompt_ids(self, messages: list[dict]) -> list[int]:
        user = "\n".join(m["content"] for m in messages if isinstance(m.get("content"), str))
        m = TOPIC_RE.search(user)
        if self.prefixes:                                 # E6: the topic is a held-out poem's id
            return list(self.prefixes[m.group(1).strip()])
        ids = self.tok.encode(m.group(1).strip(), add_bos=True, add_eos=True) if m else []
        if self.metre_tag:
            metre = METRE_RE.search(user)
            if metre is None:
                raise ValueError("no metre name in the prompt messages")
            ids += self.tok.encode(metre.group(1).strip(), add_bos=True, add_eos=True)
        ids += [self.tok.bos_id]
        if len(ids) > MAX_PREFIX:
            raise ValueError(f"topic prefix of {len(ids)} tokens exceeds {MAX_PREFIX}")
        return ids

    @torch.no_grad()
    def _forward(self, ids: Sequence[int]) -> torch.Tensor:
        n = len(ids)
        x = torch.full((1, CANVAS), self.mask_id, dtype=torch.long, device=self.device)
        if n >= CANVAS:                               # the canvas is full: only <eos> remains
            z = torch.full((self.tok.vocab_size,), -1e9, device=self.device)
            z[self.tok.eos_id] = 0.0
            return z
        x[0, :n] = torch.tensor(list(ids), device=self.device)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            z = self.model.logits(self.model.hidden(x)[0, n]).float()[: self.tok.vocab_size] + self.bias
        return z.masked_fill(torch.isinf(z), -1e9)    # never-output ids: finite, so entropy stays defined

    def _wait(self) -> None:
        if self._pending is not None:
            pending, self._pending = self._pending, None
            self._logits = pending.result()

    def _launch(self) -> None:
        self._wait()
        self._pending = self._worker.submit(self._forward, self.prefix + self.generated)

    # ---- LogitsSource protocol
    def start(self, prompt_ids: Sequence[int]) -> None:
        self._wait()
        self.prefix = list(prompt_ids) or [self.tok.bos_id]
        self.generated = []
        self._launch()

    def next(self) -> Distribution:
        self._wait()
        z = self._logits
        lse = torch.logsumexp(z, dim=0)
        logp = z - lse
        entropy = -(logp.exp() * logp).sum()
        top = torch.topk(z, self.top_k)
        return Distribution(slice_logits=z.index_select(0, self._slice).tolist(), lse=float(lse),
                            entropy=float(entropy), top=list(zip(top.indices.tolist(), top.values.tolist())))

    def logit(self, token_id: int) -> float:
        self._wait()
        return float(self._logits[token_id])

    def rank(self, token_id: int) -> int:
        self._wait()
        return int((self._logits > self._logits[token_id]).sum()) + 1

    def sample_full(self, temperature: float, top_p: float, rng: random.Random) -> tuple[int, float]:
        self._wait()
        probs = torch.softmax(self._logits / temperature, dim=0)
        sorted_p, order = torch.sort(probs, descending=True)
        keep = torch.cumsum(sorted_p, dim=0) - sorted_p < top_p
        kept = sorted_p[keep] / sorted_p[keep].sum()
        gen = torch.Generator(device=self.device).manual_seed(rng.getrandbits(62))
        j = int(torch.multinomial(kept, 1, generator=gen))
        return int(order[keep][j]), float(kept[j])

    def push(self, token_id: int) -> None:
        self._wait()
        self.generated.append(token_id)
        self._launch()

    def rollback(self, n_generated: int) -> None:
        self._wait()
        self.generated = self.generated[:n_generated]
        self._launch()

    def decode(self, ids: Sequence[int]) -> str:
        return self.tok.decode([i for i in ids if i not in (self.tok.bos_id, self.tok.eos_id)])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="pilot", help="'pilot', a run folder or checkpoint (finetune.py, ft.train), or "
                    "a downloaded Hugging Face folder (common.load_model)")
    ap.add_argument("--name", required=True, help="runs/<name>/ and results/<name>.md")
    ap.add_argument("--meters", nargs="+", help="default: the 37 meters of the reference run")
    ap.add_argument("--modes", nargs="+", help="default: the reference run's modes")
    ap.add_argument("--seeds", nargs="+", type=int, help="default: the reference run's seeds")
    ap.add_argument("--topics", nargs="+", help="topic ids (default: the reference run's T1-T3)")
    ap.add_argument("--min-count", type=int, default=10, help="slice: aksharas seen this often in the poem train split")
    ap.add_argument("--metre-tag", action="store_true", help="E5: put the metre's name before the poem, as in training")
    ap.add_argument("--mask-workers", type=int, default=7, help="mask worker processes per shard")
    ap.add_argument("--shards", type=int, default=1, help="run the meters in this many processes at once")
    ap.add_argument("--shard", type=int, default=None, help=argparse.SUPPRESS)          # set for the child processes
    ap.add_argument("--e6-split", choices=("val", "test"), help="E6: prompt with held-out poems of this split")
    ap.add_argument("--e6-data", type=Path, default=E6_DATA, help="E6: ft.build_data output")
    ap.add_argument("--e6-per-metre", type=int, default=15, help="E6: held-out poems per metre")
    ap.add_argument("--e6-reference", help="E6: exactly the (metre, poem id) pairs of this run (under runs/)")
    args = ap.parse_args(argv)

    ref = json.loads(REFERENCE_RUN.read_text(encoding="utf-8"))
    meters = args.meters or ref["meters"]
    only = None
    if args.e6_reference:
        only = collections.defaultdict(set)
        for line in open(HERE / "runs" / args.e6_reference / "results.jsonl", encoding="utf-8"):
            r = json.loads(line)
            only[r["meter"]].add(r["topic"])
    out = HERE / "runs" / args.name
    if args.e6_split and args.shard is None:          # E6: only the metres that have held-out poems
        have = e6_prompts(tokenizer(), args.e6_split, args.e6_per_metre, 42, meters, args.e6_data, only)
        meters = [m for m in meters if have.get(m)]
    if args.shards > 1 and args.shard is None:
        return run_shards(args, argv if argv is not None else sys.argv[1:], meters, out)
    if args.shard is not None:
        if args.e6_split:                             # the parent passes all metres; keep the ones with poems
            have = e6_prompts(tokenizer(), args.e6_split, args.e6_per_metre, 42, meters, args.e6_data, only)
            meters = [m for m in meters if have.get(m)]
        meters = meters[args.shard::args.shards]
        out = out / f"shard_{args.shard}"
    modes = args.modes or ref["modes"]
    seeds = args.seeds or ([42] if args.e6_split else ref["seeds"])
    topics = [(k, v) for k, v in ref["topics"].items() if not args.topics or k in args.topics]
    cfg = dataclasses.replace(DecodeConfig(**ref["config"]), max_tokens=MAX_TOKENS, baseline_max_tokens=MAX_TOKENS)
    enforce = ref["enforce"]

    if args.shard:                                    # stagger the shards' start: one model load at a time
        time.sleep(45 * args.shard)
    wait_for_memory(4, args.name)
    device = torch.device("cuda")
    torch.backends.cuda.matmul.allow_tf32 = True
    model, weights = load_model(args.model, "cpu")
    model = model.to(device=device, dtype=torch.bfloat16).eval()       # inference only: half the memory
    tok = tokenizer()
    index = poem_slice(tok, args.min_count)
    source = MDLMSource(model, tok, index, device, metre_tag=args.metre_tag)
    print(f"{args.name}: {weights}; slice {index.size:,} tokens; {len(meters)} meters x {len(topics)} topics x "
          f"{len(modes)} modes x {len(seeds)} seeds", flush=True)
    if args.e6_split:
        prompts = e6_prompts(tok, args.e6_split, args.e6_per_metre, 42, meters, args.e6_data, only)
        source.prefixes = {pid: ids for items in prompts.values() for pid, ids in items}
        parts = []
        for meter in meters:
            items = prompts.get(meter)
            if not items:
                print(f"{meter}: no held-out poem fits", flush=True)
                continue
            budget = CANVAS - max(len(ids) for _, ids in items)
            mcfg = dataclasses.replace(cfg, max_tokens=budget, baseline_max_tokens=budget)
            run_grid(source, index, [meter], modes, [(pid, pid) for pid, _ in items], seeds, out / f"m_{meter}",
                     cfg=mcfg, model_name=f"chandohasam-mdlm:{weights}", prasa=enforce["prasa"], yati=enforce["yati"],
                     profile=enforce["profile"], mask_workers=args.mask_workers)
            parts.append(out / f"m_{meter}")
        merge_runs(out, parts, [p.name[2:] for p in parts])
    else:
        run_grid(source, index, meters, modes, topics, seeds, out, cfg=cfg, model_name=f"chandohasam-mdlm:{weights}",
                 prasa=enforce["prasa"], yati=enforce["yati"], profile=enforce["profile"],
                 mask_workers=args.mask_workers)
    run_json = json.loads((out / "run.json").read_text(encoding="utf-8"))
    run_json.update(weights=weights, canvas=CANVAS,
                    topic_conditioning=(f"E6: held-out {args.e6_split} poems, T1 prompt (ft.canvas)" if args.e6_split
                                        else "<bos> topic <eos> <bos> metre <eos> <bos> poem" if args.metre_tag
                                        else "<bos> topic <eos> <bos> poem"),
                    slice={"tokens": index.size, "min_count": args.min_count,
                           "rule": "aksharas seen min_count times in the poem train split + space + newline"})
    (out / "run.json").write_text(json.dumps(run_json, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.shard is not None:
        return 0
    finish(out, args.name)
    return 0


def run_shards(args, argv: list[str], meters: list[str], out) -> int:
    """Run the meters in ``args.shards`` child processes (each with its own model copy and mask workers),
    then merge their run folders into runs/<name>/ and write the report."""
    import subprocess
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
    merge_runs(out, [out / f"shard_{k}" for k in range(args.shards)], meters, shards=args.shards)
    finish(out, args.name)
    return 0


def finish(out, name: str) -> None:
    summarize(out)
    results = HERE / "results"
    results.mkdir(exist_ok=True)
    print(report([out], out=results / f"{name}.md"), flush=True)        # also writes results/<name>.json


if __name__ == "__main__":
    raise SystemExit(main())
