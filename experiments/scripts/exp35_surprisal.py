#!/usr/bin/env python3
"""
EXP-35: teacher-forced surprisal of each corpus token against the model's own top choice.

Spec: experiments/EXP-35-teacher-forced-surprisal-gap-corpus-token-vs-top-choice.md. This script
implements the spec's inputs, conditions and per-token record, and evaluates sanity gates 1-5 (gate 6
needs EXP-08's rerun). The replication notes say to run the gates on 5-10 poems before the full
sample; `--n` sets how many poems of the shuffled 200-poem sample are scored (poem and bhavam).

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp35_surprisal.py --n 10 OUT_DIR

Conditions (every text is scored under each):
    random  `<bos>` + text, randomly initialised weights   harness reference (gate 5)
    bos     `<bos>` + text                                  primary
    nobos   text only; token 0 has no prediction            the presumed pipeline setup (gate 4)

Memory. The text model of gemma-4-E2B-it is 9.3 GB in bf16 and the laptop GPU has 8 GB. The per-layer
embedding table (PLE; 262,144 x 35 x 256, 4.7 GB) is a pure lookup, so it stays in CPU RAM: the tokens
are looked up there and passed to the model as `per_layer_inputs`, which Gemma4ForCausalLM.forward
accepts in place of its own lookup (`get_per_layer_inputs`, the same table and reshape). Everything
else (4.6 GB) runs on the GPU. The model is built with a one-row PLE placeholder, so the full table is
never allocated on the GPU. The random-weights model uses the library's own initialisation
(`_from_config`, and `_init_weights` for the CPU table).

Writes OUT_DIR/run.json, OUT_DIR/traces.jsonl (one row per text x condition, keyed
"{id}|{poem|bhavam}|{condition}"; an interrupted run resumes) and OUT_DIR/summary.json (the gates).
The akshara grid of the spec's output record is not computed yet (the gates do not use it).
`--summarise-only` recomputes summary.json from the traces without loading the model.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import gc
import json
import math
import platform
import random
import sys
import time
import unicodedata
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))

from indic_meter_dawg.scansion import scan      # noqa: E402

MODEL_ID = "google/gemma-4-E2B-it"
DATASET = ROOT / "dataset" / "bhagavatam.json"
PER_METRE = 25            # poems drawn per metre (spec, Inputs 1)
MIN_ELIGIBLE = 25         # metres with fewer eligible records are dropped
BHAVAM_CHARS = 2000       # bhavam truncation (spec, Inputs 3)
CONDITIONS = ("random", "bos", "nobos")    # random first: it uses the freshly initialised weights
KINDS = ("poem", "bhavam")
CHUNK = 128               # logits rows per log_softmax chunk (V = 262,144: 128 MB in float32)
INVARIANT_TOL = 1e-4      # gate 1
RANDOM_TOL = 1.0          # gate 5, the spec's wording: |mean s_true - ln V| and mean gap, in nats
ANALYTIC_TOL = 0.1        # gate 5, analytic floor: allowed |measured - expected|, in nats
PIPELINE = {"poems": 102, "s_true_mean": 13.15, "s_model_mean": 0.41, "gap_mean": 12.74}   # EXP-35 "Observed"
SMOKE = [
    ("english", "The capital of France is Paris. The capital of Germany is Berlin. The capital of Italy is Rome."),
    ("telugu_prose", "తెలుగు భారతదేశంలోని ఆంధ్రప్రదేశ్, తెలంగాణ రాష్ట్రాల అధికార భాష."),
]


# ------------------------------------------------------------------ inputs
def balanced_sample(seed: int):
    """Spec, Inputs 1: 25 poems per metre with >= 25 eligible records, drawn with a fixed seed, then shuffled."""
    records = json.loads(DATASET.read_text(encoding="utf-8"))
    by_metre = defaultdict(list)
    for r in records:
        if r["form"] == "verse" and any(ln.strip() for ln in r["verse"] or []) and (r["bhavam"] or "").strip():
            by_metre[r["metre_roman"]].append(r)
    eligible = {m: len(rs) for m, rs in sorted(by_metre.items(), key=lambda kv: -len(kv[1]))}
    metres = sorted(m for m, rs in by_metre.items() if len(rs) >= MIN_ELIGIBLE)
    rng = random.Random(seed)
    sample = [r for m in metres for r in rng.sample(by_metre[m], PER_METRE)]
    rng.shuffle(sample)
    return sample, eligible, metres


def poem_text(rec) -> str:
    """Spec, Inputs 2: the scanner's NFC-normalised, stripped lines, joined with newlines."""
    return "\n".join(s.text for s in scan(rec["verse"]))


def bhavam_text(rec) -> str:
    """Spec, Inputs 3: NFC, stripped, the first 2,000 characters."""
    return unicodedata.normalize("NFC", rec["bhavam"]).strip()[:BHAVAM_CHARS]


# ------------------------------------------------------------------ model
def snapshot_dir() -> Path:
    from transformers.utils import cached_file
    return Path(cached_file(MODEL_ID, "config.json", local_files_only=True)).parent


def build_model(snap: Path, device: str, seed: int):
    """The text model with randomly initialised weights and a one-row PLE placeholder, on `device`."""
    import torch
    from transformers import AutoConfig
    from transformers.models.gemma4.modeling_gemma4 import Gemma4ForCausalLM

    cfg = AutoConfig.from_pretrained(snap).text_config
    small = copy.deepcopy(cfg)
    small.vocab_size_per_layer_input = 1
    torch.manual_seed(seed)
    with torch.device(device):
        model = Gemma4ForCausalLM._from_config(small, dtype=torch.bfloat16)
    model.eval().requires_grad_(False)
    return model, cfg


def ple_module(cfg, weight=None, init_from=None):
    """The PLE table on the CPU: the checkpoint's `weight`, or a fresh table initialised by `init_from._init_weights`."""
    import torch
    from transformers.models.gemma4.modeling_gemma4 import Gemma4TextScaledWordEmbedding

    dim = cfg.num_hidden_layers * cfg.hidden_size_per_layer_input
    scale = cfg.hidden_size_per_layer_input ** 0.5
    if weight is not None:
        ple = Gemma4TextScaledWordEmbedding(1, dim, cfg.pad_token_id, embed_scale=scale)
        ple.weight = torch.nn.Parameter(weight, requires_grad=False)
        ple.num_embeddings = weight.shape[0]
    else:
        with torch.device("meta"):
            ple = Gemma4TextScaledWordEmbedding(cfg.vocab_size_per_layer_input, dim, cfg.pad_token_id, embed_scale=scale)
        ple = ple.to(torch.bfloat16).to_empty(device="cpu")
        init_from._init_weights(ple)       # normal(0, initializer_range), padding row zero, embed_scale
    return ple.requires_grad_(False)


def load_trained(model, snap: Path):
    """Copy the checkpoint's text weights into `model` (GPU) and return the PLE table (CPU) and a load report."""
    import torch
    from safetensors import safe_open

    prefix = "model.language_model."
    skip = {"model.embed_tokens_per_layer.weight", "lm_head.weight"}   # PLE: CPU table; lm_head: tied to embed_tokens
    params = {n for n, _ in model.named_parameters()}
    state = model.state_dict()
    missing, buffers_kept, used = [], [], set()
    with safe_open(str(snap / "model.safetensors"), framework="pt", device="cpu") as f:
        keys = set(f.keys())
        for name, t in state.items():
            if name in skip:
                continue
            ck = prefix + name[len("model."):]
            if ck not in keys:
                (missing if name in params else buffers_kept).append(name)   # buffers keep their computed values
                continue
            src = f.get_tensor(ck)
            if tuple(src.shape) != tuple(t.shape):
                raise RuntimeError(f"shape mismatch for {name}: checkpoint {tuple(src.shape)}, model {tuple(t.shape)}")
            t.copy_(src.to(t.dtype))
            used.add(ck)
        ple_key = prefix + "embed_tokens_per_layer.weight"
        ple_weight = f.get_tensor(ple_key)
        used.add(ple_key)
    if missing:
        raise RuntimeError(f"{len(missing)} model tensors are not in the checkpoint, e.g. {missing[:5]}")
    tied = model.lm_head.weight.data_ptr() == model.model.embed_tokens.weight.data_ptr()
    if not tied:
        model.lm_head.weight.copy_(model.model.embed_tokens.weight)
    unused = sorted(k for k in keys if k.startswith(prefix) and k not in used)
    report = {"tensors_loaded": len(used), "lm_head_tied_to_embed_tokens": tied,
              "buffers_not_in_checkpoint": buffers_kept,
              "unused_text_tensors": len(unused), "unused_examples": unused[:6]}
    return ple_weight, report


# ------------------------------------------------------------------ scoring
def score(model, ple, cfg, ids: list[int], prefix: list[int], device: str) -> dict:
    """One forward pass; per target token: s_true, s_model, entropy, rank, argmax (None where unscored)."""
    import torch

    full = prefix + ids
    P, T = len(prefix), len(ids)
    x = torch.tensor([full])
    with torch.no_grad():
        emb = model.model.embed_tokens(x.to(device))
        pli = ple(x).reshape(1, len(full), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(device)
        logits = model(inputs_embeds=emb, per_layer_inputs=pli, use_cache=False).logits[0]
        full_t = torch.tensor(full, device=device)
        out = {k: [None] * T for k in ("s_true", "s_model", "entropy", "rank", "argmax")}
        offby1 = []
        first = 0 if P else 1                   # without a prefix, token 0 has no prediction
        for a in range(first, T, CHUNK):
            js = torch.arange(a, min(a + CHUNK, T), device=device)
            rows = P + js - 1                   # logits row r predicts position r + 1
            lp = torch.log_softmax(logits[rows].float(), dim=-1)
            t_lp = lp.gather(1, full_t[P + js][:, None])[:, 0]
            m_lp, m_id = lp.max(dim=-1)
            rank = 1 + (lp > t_lp[:, None]).sum(dim=-1)
            ent = -(lp.exp() * lp).sum(dim=-1)
            ob = -lp.gather(1, full_t[rows][:, None])[:, 0]     # surprisal of the token just read
            for i, j in enumerate(js.tolist()):
                out["s_true"][j] = round(-t_lp[i].item(), 5)
                out["s_model"][j] = round(-m_lp[i].item(), 5)
                out["entropy"][j] = round(ent[i].item(), 5)
                out["rank"][j] = int(rank[i].item())
                out["argmax"][j] = int(m_id[i].item())
                if j >= 1:                      # x_{j-1} is a text token, not <bos>
                    offby1.append(ob[i].item())
        out["offby1_mean"] = round(mean(offby1), 5) if offby1 else None
    return out


def greedy(model, ple, cfg, ids: list[int], steps: int, device: str) -> list[int]:
    """A short greedy continuation (full recompute per step), as a smoke test of the split model."""
    import torch

    ids = list(ids)
    with torch.no_grad():
        for _ in range(steps):
            x = torch.tensor([ids])
            emb = model.model.embed_tokens(x.to(device))
            pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(device)
            ids.append(int(model(inputs_embeds=emb, per_layer_inputs=pli, use_cache=False).logits[0, -1].argmax()))
    return ids


# ------------------------------------------------------------------ summary and gates
def expected_max_normal(n: int, step: float = 1e-3) -> float:
    """E[max of n iid N(0,1)] = integral of x * n * phi(x) * Phi(x)^(n-1), by the trapezoid rule on [0, 12]."""
    def f(x: float) -> float:
        log_cdf = math.log(0.5 * math.erfc(-x / math.sqrt(2)))
        return x * n * math.exp(-x * x / 2 + (n - 1) * log_cdf) / math.sqrt(2 * math.pi)
    xs = [i * step for i in range(int(12 / step) + 1)]
    return step * (sum(f(x) for x in xs) - (f(xs[0]) + f(xs[-1])) / 2)


def text_stats(row) -> dict:
    st = [v for v in row["s_true"] if v is not None]
    sm = [v for v in row["s_model"] if v is not None]
    rk = [v for v in row["rank"] if v is not None]
    en = [v for v in row["entropy"] if v is not None]
    return {"id": row["id"], "tokens": len(st), "s_true": mean(st), "s_model": mean(sm),
            "gap": mean(a - b for a, b in zip(st, sm)), "top1": sum(r == 1 for r in rk) / len(rk),
            "entropy": mean(en), "offby1": row["offby1_mean"]}


def summarise(out_dir: Path) -> dict:
    rows = [json.loads(line) for line in (out_dir / "traces.jsonl").open(encoding="utf-8")]
    run = json.loads((out_dir / "run.json").read_text(encoding="utf-8"))
    ln_v = math.log(run["model"]["vocab_size"])
    per = defaultdict(list)
    positions = violations = 0
    worst = 0.0
    for r in rows:
        per[(r["condition"], r["kind"])].append(text_stats(r))
        for a, b in zip(r["s_true"], r["s_model"]):
            if a is None:
                continue
            positions += 1
            if b > a + INVARIANT_TOL:
                violations += 1
                worst = max(worst, b - a)

    def agg(stats):
        return {"texts": len(stats), "tokens": sum(s["tokens"] for s in stats),
                "s_true_mean": round(mean(s["s_true"] for s in stats), 4),
                "s_true_median": round(median(s["s_true"] for s in stats), 4),
                "s_model_mean": round(mean(s["s_model"] for s in stats), 4),
                "gap_mean": round(mean(s["gap"] for s in stats), 4),
                "top1_mean": round(mean(s["top1"] for s in stats), 4),
                "entropy_mean": round(mean(s["entropy"] for s in stats), 4),
                "offby1_mean": round(mean(s["offby1"] for s in stats if s["offby1"] is not None), 4)}

    by = {f"{c}/{k}": agg(v) for (c, k), v in sorted(per.items())}
    g = lambda c, k, f: by[f"{c}/{k}"][f]                                        # noqa: E731
    align_ok = all(g("bos", k, "s_true_mean") < g("bos", k, "offby1_mean") for k in KINDS)
    nobos_breaks = g("nobos", "poem", "s_true_mean") >= ln_v
    sigma = run["model"]["initializer_range"] * math.sqrt(run["model"]["hidden_size"])
    floor = {"s_true": ln_v + sigma ** 2 / 2, "entropy": ln_v - sigma ** 2 / 2,
             "gap": sigma * expected_max_normal(run["model"]["vocab_size"])}
    pairs = {s["id"]: s["s_true"] for s in per[("bos", "poem")]}
    prose_easier = sum(1 for s in per[("bos", "bhavam")] if s["id"] in pairs and s["s_true"] < pairs[s["id"]])
    gates = {
        "1_invariant": {"positions": positions, "violations": violations, "largest_excess": round(worst, 6),
                        "pass": violations == 0},
        "2_uniform_bound": {"ln_V": round(ln_v, 4), "bos_poem": g("bos", "poem", "s_true_mean"),
                            "bos_bhavam": g("bos", "bhavam", "s_true_mean"),
                            "pass": g("bos", "poem", "s_true_mean") < ln_v and g("bos", "bhavam", "s_true_mean") < ln_v},
        "3_prose_control": {"bos_bhavam": g("bos", "bhavam", "s_true_mean"), "bos_poem": g("bos", "poem", "s_true_mean"),
                            "pairs_bhavam_lower": f"{prose_easier}/{len(pairs)}",
                            "pass": g("bos", "bhavam", "s_true_mean") < g("bos", "poem", "s_true_mean")},
        "4_bos_alignment": {
            "s_true_mean": {k: {"bos": g("bos", k, "s_true_mean"), "nobos": g("nobos", k, "s_true_mean")} for k in KINDS},
            "aligned_vs_offby1": {f"{c}/{k}": {"aligned": g(c, k, "s_true_mean"), "offby1": g(c, k, "offby1_mean")}
                                  for c in ("bos", "nobos") for k in KINDS},
            "alignment_ok_under_bos": align_ok,
            "nobos_poem_above_ln_V": nobos_breaks,
            "nobos_poem_vs_pipeline": {"this_run": {f: g("nobos", "poem", f"{f}_mean") for f in ("s_true", "s_model", "gap")},
                                       "pipeline": {f: PIPELINE[f"{f}_mean"] for f in ("s_true", "s_model", "gap")}},
            "diagnosis": ("missing <bos>: without it the poem mean exceeds ln V, with it the mean is far below, "
                          "and under <bos> the aligned surprisal is below the off-by-one value")
                         if (align_ok and nobos_breaks and g("bos", "poem", "s_true_mean") < ln_v) else "not established",
            "pass": align_ok},
        "5_random_reference": {
            "measured": {k: {f: g("random", k, f"{f}_mean") for f in ("s_true", "entropy", "gap", "s_model")} for k in KINDS},
            "spec_criterion": f"mean s_true within {RANDOM_TOL} nat of ln V and mean gap below {RANDOM_TOL} nat (an exactly uniform output)",
            "spec_criterion_met": all(abs(g("random", k, "s_true_mean") - ln_v) <= RANDOM_TOL
                                      and g("random", k, "gap_mean") <= RANDOM_TOL for k in KINDS),
            "analytic_floor": dict({f: round(v, 4) for f, v in floor.items()}, logit_sd=round(sigma, 4),
                                   basis="the final RMSNorm gives |h| = sqrt(hidden_size) and lm_head rows are "
                                         "N(0, initializer_range^2), so logits are ~N(0, sd^2) with sd = "
                                         "initializer_range * sqrt(hidden_size): s_true = ln V + sd^2/2, "
                                         "entropy = ln V - sd^2/2, gap = sd * E[max of V standard normals]"),
            "analytic_tolerance_nats": ANALYTIC_TOL,
            "pass": all(abs(g("random", k, f"{f}_mean") - floor[f]) <= ANALYTIC_TOL
                        for k in KINDS for f in ("s_true", "entropy", "gap"))},
        "6_nll_cross_check": {"pass": None, "note": "needs EXP-08's per-poem nll_true under the same condition; EXP-08 has not been rerun"},
    }
    summary = {"conditions": by, "gates": gates,
               "pipeline_2026_09_24": dict(PIPELINE, note="poem side, presumed no <bos>; EXP-35 'Observed'")}
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


# ------------------------------------------------------------------ main
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--n", type=int, default=10, help="poems of the shuffled sample to score (poem and bhavam)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--summarise-only", action="store_true")
    args = ap.parse_args()
    out = args.out_dir
    if args.summarise_only:
        print(json.dumps(summarise(out)["gates"], ensure_ascii=False, indent=1))
        return

    import torch
    import transformers
    from transformers import AutoTokenizer

    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, eligible, metres = balanced_sample(args.seed)
    chosen = sample[: args.n]
    snap = snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    bos = tok.bos_token_id
    probe = poem_text(chosen[0])
    texts = {(r["id"], "poem"): poem_text(r) for r in chosen}
    texts.update({(r["id"], "bhavam"): bhavam_text(r) for r in chosen})
    metre_of = {r["id"]: r["metre_roman"] for r in chosen}

    traces = out / "traces.jsonl"
    done = set()
    if traces.exists():
        done = {json.loads(line)["key"] for line in traces.open(encoding="utf-8")}

    model, cfg = build_model(snap, args.device, args.seed)
    run = {
        "experiment": "EXP-35", "stage": f"sanity gates on {args.n} poems",
        "date": datetime.date.today().isoformat(),
        "model": {"id": MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "vocab_size": cfg.vocab_size,
                  "layers": cfg.num_hidden_layers, "hidden_size": cfg.hidden_size,
                  "initializer_range": cfg.initializer_range, "logits": "cast to float32 before log_softmax",
                  "placement": "PLE table (4.7 GB) in CPU RAM, passed as per_layer_inputs; the rest on the GPU"},
        "device": {"name": torch.cuda.get_device_name(0) if args.device.startswith("cuda") else "cpu",
                   "python": platform.python_version(), "torch": torch.__version__,
                   "transformers": transformers.__version__},
        "seed": args.seed,
        "sample": {"rule": "form == verse, non-empty verse and bhavam; metres with >= 25 eligible records; "
                           "25 per metre (random.Random(seed).sample), then shuffled",
                   "eligible_per_metre": eligible, "metres": metres, "size": len(sample),
                   "ids": [r["id"] for r in sample], "scored_ids": [r["id"] for r in chosen]},
        "conditions": list(CONDITIONS), "kinds": list(KINDS),
        "tokenizer": {"bos_token_id": bos,
                      "default_call_adds_bos": tok(probe)["input_ids"][0] == bos,
                      "default_call_first_ids": tok(probe)["input_ids"][:3]},
        "akshara_grid": "not computed in this run (the gates do not use it)",
    }

    def run_condition(cond: str, ple) -> None:
        with traces.open("a", encoding="utf-8") as fh:
            for (rid, kind), text in texts.items():
                key = f"{rid}|{kind}|{cond}"
                if key in done:
                    continue
                enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
                ids = enc["input_ids"]
                prefix = [] if cond == "nobos" else [bos]
                res = score(model, ple, cfg, ids, prefix, args.device)
                row = {"key": key, "id": rid, "metre": metre_of[rid], "kind": kind, "condition": cond, "text": text,
                       "prefix_len": len(prefix), "tokens": ids, "pieces": tok.convert_ids_to_tokens(ids),
                       "offsets": [list(o) for o in enc["offset_mapping"]], **res}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                done.add(key)
                print(f"  {cond:6s} {kind:6s} {rid:14s} tokens={len(ids):4d} "
                      f"s_true={mean(v for v in res['s_true'] if v is not None):6.3f}", flush=True)

    # random weights first: the model was just built with the library's random initialisation
    if any(f"{rid}|{kind}|random" not in done for rid, kind in texts):
        t = time.time()
        ple = ple_module(cfg, init_from=model)
        print(f"random PLE initialised in {time.time() - t:.0f}s")
        run_condition("random", ple)
        del ple
        gc.collect()

    t = time.time()
    ple_weight, report = load_trained(model, snap)
    ple = ple_module(cfg, weight=ple_weight)
    run["model"]["load"] = dict(report, seconds=round(time.time() - t, 1))
    print(f"trained weights loaded in {time.time() - t:.0f}s: {report}")

    smoke = {}
    for name, text in SMOKE:
        ids = tok(text, add_special_tokens=False)["input_ids"]
        res = score(model, ple, cfg, ids, [bos], args.device)
        st = [v for v in res["s_true"] if v is not None]
        smoke[name] = {"tokens": len(ids), "s_true_mean": round(mean(st), 4),
                       "top1": round(sum(r == 1 for r in res["rank"]) / len(ids), 4)}
    cont = greedy(model, ple, cfg, [bos] + tok("The capital of France is", add_special_tokens=False)["input_ids"], 6, args.device)
    smoke["greedy_continuation"] = tok.decode(cont[1:])
    run["smoke_test"] = smoke
    print("smoke test:", json.dumps(smoke, ensure_ascii=False))

    for cond in ("bos", "nobos"):
        run_condition(cond, ple)
    run["seconds"] = round(time.time() - t0, 1)
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    summary = summarise(out)
    print(json.dumps(summary["gates"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
