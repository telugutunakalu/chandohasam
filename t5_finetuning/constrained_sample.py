"""T5Gemma 2 through our constrained decoder (metrical_decoder), as Nandi's E6 evaluation
(../autoregressive_finetuning/constrained_sample.py): free and constrained poems for the E6 prompts.

    ../.venv/bin/python -u constrained_sample.py --size 270m --model runs/t5g-270m-full/final --name e6_t5g_270m_val_c
    ../.venv/bin/python -u constrained_sample.py --size 4b --lora runs/t5g-4b-lora-full/lora.pt --r 32 --lora-mlp \
        --name e6_t5g_4b_test_c --reference e6_120m_t1_test --seeds 42 --free-seeds 42 43
    ../.venv/bin/python -u constrained_sample.py --size 270m --model runs/t5g-270m-full/final --name smoke --limit 1 \
        --meters kandamu utpalamala --modes baseline masking_backtrack                      # a smoke test

- **The source:** `T5Source`, metrical_decoder.hf.HFCausalLM for an encoder-decoder model: per prompt the encoder
  runs once (its output kept with the prompt), the decoder starts from `<bos>` and steps one token per forward with
  its cache; rollback replays the kept tokens on a copy of the prompt's state. The prompt is common.source_text of the
  poem's record (task, metre, its rules, register, bhāvam), keyed by the poem id that run_grid passes as the topic.
- **The poems and decoding:** the (metre, poem id) pairs of a reference MDLM run (--reference, default e6_120m_val),
  its DecodeConfig, enforcement and per-metre token budgets; modes as the reference (or --modes), the free baseline
  with --free-seeds and the constrained modes with --seeds.
- **The vocabulary slice:** TokenIndex.from_tokenizer over the Gemma 3 tokenizer, as for Gemma-4 (HFCausalLM).
- **v2 layers** (metrical_decoder, 2026-10-22): `--inventory padyarchana` (Layer A: only syllables of the train split's
  verse) and `--attest-weight/--attest-where/--attest-corpus` (Layer B: prefer tokens that keep words real).
- **Records:** E6 records (../diffusion_finetuning/data/e6/records, or the directory in $E6_RECORDS_DIR: the full
  grid's prompts replace the bhāvams there).

Writes runs/<name>/ (results.jsonl, traces, run.json) and results/<name>.md (metrical_decoder.analysis.report).
"""
from __future__ import annotations

import argparse
import collections
import copy
import dataclasses
import json
import time
from concurrent.futures import ThreadPoolExecutor

import torch

import common as C

from metrical_decoder import DecodeConfig                             # noqa: E402 (sys.path set by common)
from metrical_decoder.analysis import report                          # noqa: E402
from metrical_decoder.hf import HFCausalLM                            # noqa: E402
from metrical_decoder.runner import run_grid, summarize               # noqa: E402
from metrical_decoder.vocab import TokenIndex                         # noqa: E402

MDLM_RUNS = C.REPO / "diffusion_finetuning" / "runs"
TOPIC = "Topic (విషయము): "


class T5Source(HFCausalLM):
    """HFCausalLM over T5Gemma 2: the prompt is the encoder input; the generated tokens are the decoder's."""

    def __init__(self, model, tok, prefixes: dict[str, list[int]], device: str = "cuda", top_k: int = 5):
        self.model_id = "t5gemma-2"
        self.device = torch.device(device)
        self.top_k = top_k
        self.prefill = None
        self.tokenizer = tok
        self.model = model.eval()
        self.eos_ids = (tok.eos_token_id,)
        self.index = TokenIndex.from_tokenizer(tok, eos_ids=self.eos_ids)
        self._slice = torch.tensor(self.index.ids, device=self.device)
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
        line = next(ln for ln in user.splitlines() if ln.startswith(TOPIC))
        return list(self.prefixes[line[len(TOPIC):].strip()])

    @torch.no_grad()
    def _forward(self, ids, cache):
        """``cache`` = (encoder output, decoder cache); ``ids`` = decoder tokens to append."""
        enc, past = cache
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out = self.model(encoder_outputs=enc, decoder_input_ids=torch.tensor([list(ids)], device=self.device),
                             past_key_values=past, use_cache=True)
        return out.logits[0, -1].float(), (enc, out.past_key_values)

    @torch.no_grad()
    def start(self, prompt_ids) -> None:
        self._wait()
        key = tuple(prompt_ids)
        if key not in self._prompt_cache:
            self._prompt_cache.clear()
            with torch.autocast("cuda", dtype=torch.bfloat16):
                enc = self.model.get_encoder()(input_ids=torch.tensor([list(key)], device=self.device))
            self._prompt_cache[key] = self._forward([self.tokenizer.bos_token_id], (enc, None))
        logits, cache = self._prompt_cache[key]
        self._prompt = key
        self._cache = (cache[0], copy.deepcopy(cache[1]))
        self._logits = logits.clone()
        self.generated = []

    def rollback(self, n_generated: int) -> None:
        self._wait()
        keep = self.generated[:n_generated]
        logits, cache = self._prompt_cache[self._prompt]
        self._cache = (cache[0], copy.deepcopy(cache[1]))
        self._logits = logits.clone()
        if keep:
            self._logits, self._cache = self._forward(keep, self._cache)
        self.generated = keep


def load_model(args):
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
    return model, tok


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--size", choices=list(C.MODELS), required=True)
    ap.add_argument("--model", default="", help="a save_pretrained folder (full fine-tuning); default: the base")
    ap.add_argument("--lora", default="", help="an adapter on the base: runs/<run>/lora.pt or a downloaded "
                    "adapter.safetensors")
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--lora-mlp", action="store_true")
    ap.add_argument("--name", required=True)
    ap.add_argument("--reference", default="e6_120m_val")
    ap.add_argument("--modes", nargs="+", help="a subset of the reference run's modes (default: all)")
    ap.add_argument("--seeds", type=int, nargs="+", help="seeds of the constrained modes (default: the reference's)")
    ap.add_argument("--free-seeds", type=int, nargs="+", help="seeds of the free baseline (default: --seeds)")
    ap.add_argument("--meters", nargs="+", help="a subset of the reference run's metres")
    ap.add_argument("--limit", type=int, default=0, help="at most N poems per metre (a smoke test)")
    ap.add_argument("--mask-workers", type=int, default=2)
    ap.add_argument("--inventory", choices=("none", "verse", "padyarchana", "tokenizer"), default="none",
                    help="v2 Layer A: allow only attested syllables")
    ap.add_argument("--attest-weight", type=float, default=0.0, help="v2 Layer B weight (0 = off)")
    ap.add_argument("--attest-where", choices=("override", "all"), default="override")
    ap.add_argument("--attest-corpus", default="all", help="Layer B's word corpus (attestation.load_attestation)")
    args = ap.parse_args()

    reference = MDLM_RUNS / args.reference
    ref = json.loads((reference / "run.json").read_text(encoding="utf-8"))
    poems = collections.defaultdict(set)
    for line in open(reference / "results.jsonl", encoding="utf-8"):
        r = json.loads(line)
        poems[r["meter"]].add(r["topic"])
    meters = [m for m in (args.meters or ref["meters"]) if poems[m]]
    modes = [m for m in ref["modes"] if not args.modes or m in args.modes]
    seeds = args.seeds or ref["seeds"]
    free_seeds = args.free_seeds or seeds
    recs = {r["id"]: r for split in ("val", "test") for r in C.read_records(split)}
    model, tok = load_model(args)
    prefixes = {pid: tok(C.source_text(recs[pid])).input_ids for m in meters for pid in poems[m]}
    source = T5Source(model, tok, prefixes)
    cfg = dataclasses.replace(DecodeConfig(**ref["config"]), attest_weight=args.attest_weight,
                              attest_where=args.attest_where, attest_corpus=args.attest_corpus)
    inventory = None if args.inventory == "none" else args.inventory
    enforce = ref["enforce"]
    out = C.RUNS / args.name
    weights = args.model or args.lora or f"{C.MODELS[args.size]} (base)"
    print(f"{args.name}: T5Gemma 2 {args.size} {weights}; slice {source.index.size:,} tokens; {len(meters)} metres, "
          f"{sum(len(poems[m]) for m in meters)} poems; modes {modes}; seeds free {free_seeds}, constrained {seeds}; "
          f"inventory {args.inventory}; Layer B weight {args.attest_weight} ({args.attest_where}, {args.attest_corpus})",
          flush=True)
    t0 = time.time()
    parts = []
    for meter in meters:
        ids = sorted(poems[meter])[: args.limit] if args.limit else sorted(poems[meter])
        budget = ref["token_budget"][meter]
        mcfg = dataclasses.replace(cfg, max_tokens=budget, baseline_max_tokens=budget)
        for group, group_seeds in ((["baseline"], free_seeds), ([m for m in modes if m != "baseline"], seeds)):
            group = [m for m in group if m in modes]
            if not group:
                continue
            part = out / f"m_{meter}_{'free' if group == ['baseline'] else 'constrained'}"
            run_grid(source, source.index, [meter], group, [(pid, pid) for pid in ids], group_seeds, part,
                     cfg=mcfg, model_name=f"t5gemma-2-{args.size}:{weights}", prasa=enforce["prasa"],
                     yati=enforce["yati"], profile=enforce["profile"], mask_workers=args.mask_workers,
                     inventory=inventory)
            parts.append(part)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("results.jsonl", "traces.jsonl", "prompts.jsonl"):
        with open(out / name, "w", encoding="utf-8") as fh:
            for part in parts:
                if (part / name).exists():
                    fh.write((part / name).read_text(encoding="utf-8"))
    runs = [json.loads((part / "run.json").read_text(encoding="utf-8")) for part in parts]
    run = {**runs[0], "meters": meters, "modes": modes, "seeds": sorted(set(seeds) | set(free_seeds)),
           "free_seeds": free_seeds, "constrained_seeds": seeds,
           "topics": {k: v for r in runs for k, v in r["topics"].items()},
           "token_budget": {k: v for r in runs for k, v in r["token_budget"].items()},
           "weights": weights, "reference": str(reference.relative_to(C.REPO)),
           "topic_conditioning": f"E6: the poems of {args.reference}, T5 source text (common.source_text)"}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    summarize(out)
    (C.HERE / "results").mkdir(exist_ok=True)
    print(report([out], out=C.HERE / "results" / f"{args.name}.md"), flush=True)
    print(f"{args.name}: {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
