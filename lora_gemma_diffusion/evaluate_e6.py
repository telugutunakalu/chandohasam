"""The E6 evaluation of DiffusionGemma, base or with an adapter (PLAN.md §4): free and constrained poems.

    ../.venv/bin/python -u evaluate_e6.py --name e6_dg_base_val
    ../.venv/bin/python -u evaluate_e6.py --name e6_dg_48k_val --lora runs/lora-48k/lora.pt
    ../.venv/bin/python -u evaluate_e6.py --name e6_dg_48k_test --lora runs/lora-48k/lora.pt --reference e6_120m_t1_test

The E6 evaluation's poems and settings: the (metre, poem id) pairs of the reference run
(../diffusion_finetuning/runs/<reference>: 114 val poems in 11 metres, or 183 test poems in 25), seed 42, its
enforcement (strict profile, prāsa, yati). The decoding is our diffusion decoder (metrical_decoder.diffusion.decoding,
the September grids'), unchanged: `baseline` = free generation with the model's own sampling recipe (end tokens
allowed), `masking_backtrack` = the constrained strategy E6 reports. Only the prompt differs from the September grids:
`T1Canvas` answers the runner's prompt request with the poem's T1 prompt (common.prompt_ids: metre, register,
[shared line], bhāvam; chat template, empty thinking channel), looked up by the poem id the runner passes as topic.

Writes runs/<name>/m_<metre>/ (run_grid's results and traces, resumable) and runs/<name>/results.jsonl (all metres),
in the E6 row format, so ../RL/reward.py score-e6, memorisation.py and the MAUVE script read them as they are.

Decoding options (2026-10-21; the first 48k run used the original decoder for both modes and wrote metrical akshara
soup under the constraint and short broken free poems — settled.py explains why):
- `--decoder settled` (default): constrained modes through settled.SettledRun (the left edge waits until the model's
  prediction there is confident); `--decoder original`: our September decoder unchanged.
- `--free native` (default): free poems from the model's own `generate` (its sampler commits its most confident
  positions anywhere on the canvas), one per prompt and seed of --free-seeds (seed + a number from the poem id), cut
  at the first end token and scored by the strict engines into the same row format (runs/<name>/free_native.jsonl);
  `--free decoder`: the decoder's baseline mode.

Full grid options (../full_grid_experiments/README.md, The design; records from $E6_RECORDS_DIR carry its prompts as bhāvams):
- `--prompt instruction`: the September grids' instruction prompt (metrical_decoder.prompts.build_messages: the
  metre's rules, the bhāvam as the topic) in place of the T1 prompt — for the base model;
- `--free-seeds` (default 42) and `--seeds` (constrained modes; default 42).
"""
from __future__ import annotations

import argparse
import json
import re
import time
import zlib

import torch

import common as C
from metrical_decoder.diffusion.canvas import CanvasPass, DiffusionGemmaCanvas
from metrical_decoder.diffusion.decoding import DiffusionConfig, decode_diffusion
from metrical_decoder.evaluate import evaluate
from metrical_decoder.prompts import build_messages
from metrical_decoder.runner import run_grid
from settled import decode_settled

TOPIC_RE = re.compile(r"Topic \(విషయము\): (.+)")


class FinitePass(CanvasPass):
    """CanvasPass with a finite entropy. With ``forbid_end`` the end tokens' scaled logits are −inf, so their
    probability is 0 and log-probability −inf, and CanvasPass's −Σ p log p is NaN at every position (0 · −inf):
    every entropy comparison is then False — the canvas keeps no prediction (its draft returns wholly to noise every
    pass) and the decoder's entropy bound never stops a run of proposals. Found 2026-10-21 (the shared package's
    September code; fixed here only, by 0 · log 0 = 0)."""

    def __init__(self, canvas, logits, scaled, first: int):
        super().__init__(canvas, logits, scaled, first)
        torch = canvas.torch
        lp = self._log_probs
        pr = lp.exp()
        self._entropy = torch.where(pr > 0, -pr * lp, torch.zeros_like(pr)).sum(-1).tolist()


class T1Canvas(DiffusionGemmaCanvas):
    """DiffusionGemmaCanvas whose prompt is the poem's T1 prompt (the runner passes the poem id as the topic), with
    finite entropies (FinitePass)."""

    prefixes: dict[str, list[int]] = {}

    def denoise(self, frozen, temperature: float):
        """DiffusionGemmaCanvas.denoise with FinitePass in place of CanvasPass (otherwise unchanged)."""
        torch = self.torch
        C, n = self.canvas_length, len(frozen)
        canvas = self.draft.clone()[None]
        conditioning = self.self_conditioning
        if n:
            frozen_ids = torch.tensor(list(frozen), device=self.device)
            canvas[0, :n] = frozen_ids
            if conditioning is not None:
                conditioning[0, :n] = float("-inf")
                conditioning[0, torch.arange(n, device=self.device), frozen_ids] = 0.0
        with torch.no_grad():
            logits = self.model(decoder_input_ids=canvas, self_conditioning_logits=conditioning,
                                decoder_attention_mask=self.block_masks, past_key_values=self.cache,
                                decoder_position_ids=self.positions).logits[0]
        scaled = logits / temperature
        if self.forbid_end:
            scaled[:, self.end_ids] = float("-inf")
        self.self_conditioning = scaled[None].to(self.model.model.decoder.embed_tokens.weight.dtype)
        self.passes_in_block += 1
        p = FinitePass(self, logits, scaled, first=n)
        entropy = torch.tensor(p._entropy, device=self.device)
        order = torch.argsort(entropy)
        sorted_h = entropy[order]
        keep_sorted = torch.cumsum(sorted_h, 0) - sorted_h <= self.entropy_bound
        keep = torch.zeros_like(keep_sorted).scatter(0, order, keep_sorted)
        tail = torch.where(keep, p._proposals, self._noise(C - n))
        self.draft = torch.cat([canvas[0, :n], tail])
        return p

    def prompt_ids(self, messages: list[dict]) -> list[int]:
        user = "\n".join(m["content"] for m in messages if isinstance(m.get("content"), str))
        return list(self.prefixes[TOPIC_RE.search(user).group(1).strip()])


def native_free(model, tok, canvas, by_metre: dict, limit: int, path, seeds=(42,)) -> None:
    """One free poem per prompt and seed from the model's own sampler (resumable by key)."""
    done = {json.loads(l)["key"] for l in open(path, encoding="utf-8")} if path.exists() else set()
    eos = model.generation_config.eos_token_id
    end = set(eos if isinstance(eos, (list, tuple)) else [eos]) | {0}
    with open(path, "a", encoding="utf-8") as fh:
        for m in sorted(by_metre):
            for pid, seed in ((p, s) for p in (by_metre[m][:limit] if limit else by_metre[m]) for s in seeds):
                key = f"{m}|{pid}|baseline|{seed}"
                if key in done:
                    continue
                t0 = time.time()
                ids = torch.tensor([canvas.prefixes[pid]], device="cuda")
                torch.manual_seed(seed + zlib.crc32(pid.encode()) % 100_000)
                with torch.no_grad():
                    o = model.generate(input_ids=ids, max_new_tokens=canvas.canvas_length)
                seq = (o.sequences[0] if hasattr(o, "sequences") else o[0])[ids.shape[1]:].tolist()
                cut = next((i for i, x in enumerate(seq) if x in end), len(seq))
                text = C.from_model(tok.decode(seq[:cut], skip_special_tokens=True).strip())
                ev = evaluate(text, m)
                row = {"key": key, "meter": m, "topic": pid, "mode": "baseline", "seed": seed, "decoder": "native",
                       "status": "eos" if cut < len(seq) else "budget", "text": text, "n_tokens": cut, "eval": ev,
                       "seconds": round(time.time() - t0, 2)}
                fh.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")
                fh.flush()
                print(f"[free native] {key}: {len(ev.get('lines') or [])} lines, gaṇa {ev.get('gana_strict')}, "
                      f"prāsa {ev.get('prasa_strict')}, yati {ev.get('yati_strict')}, {cut} tokens, "
                      f"{row['seconds']}s", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--name", required=True)
    ap.add_argument("--lora", default="")
    ap.add_argument("--r", type=int, default=16)
    ap.add_argument("--alpha", type=float, default=32)
    ap.add_argument("--reference", default="e6_120m_val")
    ap.add_argument("--modes", nargs="+", default=["baseline", "masking_backtrack"])
    ap.add_argument("--mask-workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="at most N poems per metre (a smoke test)")
    ap.add_argument("--meters", nargs="+", help="a subset of the reference run's metres")
    ap.add_argument("--decoder", choices=("settled", "original"), default="settled")
    ap.add_argument("--free", choices=("native", "decoder"), default="native")
    ap.add_argument("--prompt", choices=("t1", "instruction"), default="t1")
    ap.add_argument("--free-seeds", type=int, nargs="+", default=[42])
    ap.add_argument("--seeds", type=int, nargs="+", default=[42], help="seeds of the constrained modes")
    args = ap.parse_args()
    ref_dir = C.REPO / "diffusion_finetuning" / "runs" / args.reference
    ref = json.loads((ref_dir / "run.json").read_text(encoding="utf-8"))
    split = "test" if "test" in args.reference else "val"
    pairs = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(ref_dir / "results.jsonl")})
    if args.meters:
        pairs = [(m, pid) for m, pid in pairs if m in args.meters]
    recs = {r["id"]: r for r in C.read_records(split)}
    model, tok = C.load(resident=True)
    if args.lora:
        C.inject_lora(model, r=args.r, alpha=args.alpha)
        C.load_lora(model, args.lora)
    model.eval()
    canvas = T1Canvas(model, tok)
    if args.prompt == "t1":
        canvas.prefixes = {pid: C.prompt_ids(tok, recs[pid]) for _, pid in pairs}
    else:       # the bhāvam on one line as the topic (the runner's topic pattern reads one line)
        canvas.prefixes = {pid: DiffusionGemmaCanvas.prompt_ids(
            canvas, build_messages(m, " ".join(C.to_model(recs[pid]["meaning"]).split()))) for m, pid in pairs}
    enforce = ref["enforce"]
    out = C.RUNS / args.name
    by_metre: dict[str, list[str]] = {}
    for m, pid in pairs:
        by_metre.setdefault(m, []).append(pid)
    label = (f"diffusiongemma-26B-A4B NVFP4{' + LoRA ' + args.lora if args.lora else ' (base)'}; {args.prompt} prompt; "
             f"{args.decoder} decoder; free {args.free}")
    grid_modes = [m for m in args.modes if not (m == "baseline" and args.free == "native")]
    decode_fn = decode_settled if args.decoder == "settled" else decode_diffusion
    print(f"{args.name}: {label}; {len(pairs)} poems in {len(by_metre)} metres; modes {args.modes}; slice "
          f"{canvas.index.size} tokens", flush=True)
    out.mkdir(parents=True, exist_ok=True)
    if "baseline" in args.modes and args.free == "native":
        native_free(model, tok, canvas, by_metre, args.limit, out / "free_native.jsonl", args.free_seeds)
    for m in sorted(by_metre):
        ids = by_metre[m][: args.limit] if args.limit else by_metre[m]
        if grid_modes:
            run_grid(canvas, canvas.index, [m], grid_modes, [(pid, pid) for pid in ids], args.seeds, out / f"m_{m}",
                     DiffusionConfig(), 1, label, prasa=enforce["prasa"], yati=enforce["yati"],
                     profile=enforce["profile"], mask_workers=args.mask_workers, decode_fn=decode_fn)
    n = 0
    with open(out / "results.jsonl", "w", encoding="utf-8") as fh:
        for path in sorted(out.glob("m_*/results.jsonl")) + [out / "free_native.jsonl"]:
            if not path.exists():
                continue
            for line in open(path, encoding="utf-8"):
                fh.write(line)
                n += 1
    (out / "run.json").write_text(json.dumps({"name": args.name, "lora": args.lora, "reference": args.reference,
                                              "modes": args.modes, "decoder": args.decoder, "free": args.free,
                                              "prompt": args.prompt, "free_seeds": args.free_seeds,
                                              "seeds": args.seeds, "poems": len(pairs), "rows": n,
                                              "enforce": enforce, "label": label}, indent=1) + "\n")
    print(f"{args.name}: {n} rows → {out / 'results.jsonl'}", flush=True)


if __name__ == "__main__":
    main()
