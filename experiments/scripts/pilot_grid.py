#!/usr/bin/env python3
"""
The base pilot120m (no fine-tuning) on the Gemma decoding grid: same metres, topics, seeds and
evaluation as experiments/runs (README "The program shared by every run").

    diffusion_pretraining/.venv/bin/python experiments/scripts/pilot_grid.py generate OUT_DIR [--modes free masking own]
    ... pilot_grid.py evaluate OUT_DIR          # the engines' verdict (CPU, parallel)
    ... pilot_grid.py metrics OUT_DIR           # Table 8 measures + judge perplexity for every grid

Grid: the 37 metres of experiments/runs/2026-09-24_e4b_baseline/prompts.jsonl x topics T1-T3 x seeds
42, 49, 56, 63, 70 = 555 poems per mode. The pilot cannot read instructions (base model, pretrained on
poem-free text), so the topic is given as the meaning of the decoder's T1 canvas; it is not a prompt.

Modes (diffusion_finetuning/ft/decode.py, the pilot's own decoder; `metrical_decoder`, which drove the
Gemma grids, is not in this repository):
  free     one sample, temperature 0.7, no constraint           ~ the grids' `baseline`
  masking  one sample, temperature 0.7, no lexicon, with the grids' strict rule set: canonical weights
           (vikalpa=False), strict prāsa (prasa_relaxed=False), hard yati (weight 1e4) under the yati
           engine's strict profile with sandhi off (ft.yati_oracle)          ~ `masking_only`
  own      the decoder's defaults: 16 particles, temperature 1.0, soft lexicon (2, 0.5), soft yati 3,
           engine + likelihood rerank                             (no Gemma counterpart)
The rule gaps that the first run exposed (ft's yati table, the sīsa half-break, the couplet chains, bare-vowel
prāsa, the pre-prāsa weight) were fixed in ft/constraints.py and ft/yati_oracle.py on 2026-09-29; the first
run's results (with its workarounds) are in 2026-09-29/, the rerun in 2026-09-29_ft-fixed/.
Budgets: ft.constraints.poem_budget (the grids' free baseline had 3 x the longest poem + 32 tokens).

Per step (every live particle; line breaks and end-of-text excluded, as the grids exclude forced line
breaks and end-of-text): the chosen token's log-probability under the model over the whole vocabulary
at temperature 1, whether the model's own first choice was allowed, and the model's mass on the
allowed tokens. The pilot decides one akshara (or a space) per step; Gemma decided one subword, so
these three are comparable across modes, not in magnitude across models.

Evaluation (the grids' definitions, experiments/runs/README.md "Evaluation"):
  gana, prasa_strict, yati_strict: chandohasam.analyze with the metre forced, strict profile, yati sandhi
  off; gana_canonical: the DAWG accepts the canonical scansion (no vikalpa or compound reading), the
  counterpart of the grids' gana_strict; in_meter = finished and gana_canonical and prasa_strict and
  yati_strict (the grids' "in meter"); in_meter_licensed allows the vikalpa readings too;
  in_meter_relaxed = finished, canonical or vikalpa reading, prasa_relaxed and yati_relaxed (relaxed
  profile, yati sandhi hypothesis), the level the pilot decoder enforces.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import math
import random
import sys
import time
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "experiments" / "runs"
PROMPTS = RUNS / "2026-09-24_e4b_baseline" / "prompts.jsonl"
SEEDS = (42, 49, 56, 63, 70)
PILOT = ROOT / "diffusion_pretraining" / "runs" / "pilot120m"
MODES = {
    "free": dict(particles=1, temperature=0.7, lexicon_lam=0.0, yati_weight=0.0, constrained=False, rerank=False),
    "masking": dict(particles=1, temperature=0.7, lexicon_lam=0.0, yati_weight=1e4, constrained=True, rerank=False,
                    yati_profile="strict", yati_sandhi="off", prasa_relaxed=False, vikalpa=False),
    "own": dict(),
}
for sub in ("meter_engine", "diffusion_finetuning", "diffusion_pretraining"):
    sys.path.insert(0, str(ROOT / sub))
GRIDS = {                     # the Gemma grids, as in writeups/scripts/compute_generation_metrics.py
    "gemma-4-E4B-it": ["2026-09-24_e4b_baseline", "2026-09-24_e4b_constrained"],
    "gemma-4-26B-A4B-it": ["2026-09-26_g26b"],
    "diffusiongemma-26B-A4B-it": ["2026-09-26_diffusion_baseline", "2026-09-25_diffusion_constrained"],
}


def grid():
    meters = sorted({json.loads(l)["meter"] for l in PROMPTS.open(encoding="utf-8")})
    topics = json.loads((RUNS / "2026-09-24_e4b_baseline" / "run.json").read_text(encoding="utf-8"))["topics"]
    return meters, topics


# ------------------------------------------------------------------ generation (GPU)
def make_decoder_class():
    import torch
    from ft.constraints import Constraint
    from ft.decode import Decoder, replace_done

    class TracingDecoder(Decoder):
        """ft.decode.Decoder.generate with per-step statistics, and the text of an unfinished sample."""

        @torch.no_grad()
        def generate(self, label, meaning, register=None, src=None):
            from ft.constraints import poem_budget
            from ft.text import CLASSICAL, SRC_EDITION
            register, src = register or CLASSICAL, src or SRC_EDITION
            cfg, dev, K, V = self.cfg, self.device, self.cfg.particles, self.V
            g = torch.Generator(dev).manual_seed(cfg.seed)
            pre = self.prefix(label, meaning, register, src)
            budget = min(poem_budget(label), cfg.canvas - len(pre) - 1)
            L = len(pre) + budget + 1
            canv = torch.full((K, L), self.mask_id, dtype=torch.long, device=dev)
            canv[:, : len(pre)] = torch.tensor(pre, device=dev)
            con = Constraint(label, self.tt, self.yati, vikalpa=cfg.vikalpa) if cfg.constrained else None
            states = [con.initial() if con else None] * K
            words = [0] * K
            logw = torch.zeros(K, device=dev, dtype=torch.float64)
            alive = torch.ones(K, dtype=torch.bool, device=dev)
            done = torch.zeros(K, dtype=torch.bool, device=dev)
            stats = Counter()
            n_resample, last = 0, 0
            nl, eos = self.tt.newline, self.tt.eos
            for pos in range(budget):
                todo = alive & ~done
                if not todo.any():
                    break
                last = pos
                p = len(pre) + pos
                with torch.autocast(dev.type, dtype=torch.bfloat16, enabled=dev.type == "cuda"):
                    logits = self.model.logits(self.model.hidden(canv)[:, p]).float()
                logp1 = torch.log_softmax(logits + self.bias, dim=-1)[:, :V]
                logp = torch.log_softmax(logits / cfg.temperature + self.bias, dim=-1)[:, :V]
                if con is not None:
                    specs = [con.spec(states[k]) if todo[k] else con.spec(replace_done(states[k])) for k in range(K)]
                    hard, soft = self._masks(specs, words, todo)
                else:
                    hard = torch.ones((K, V), dtype=torch.bool, device=dev)
                    soft = torch.zeros((K, V), device=dev)
                score = torch.where(hard, logp + soft, torch.full_like(logp, -math.inf))
                logz = torch.logsumexp(score, dim=-1)
                dead = todo & ~torch.isfinite(logz)
                alive &= ~dead
                logw[dead] = -math.inf
                u = torch.rand(score.shape, device=dev, generator=g).clamp_(1e-20, 1.0)
                nxt = (score - torch.log(-torch.log(u))).argmax(-1)
                live = todo & alive
                chosen = nxt[live]
                keep = (chosen != nl) & (chosen != eos)
                if keep.any():
                    lp = logp1[live].gather(1, chosen[:, None])[:, 0][keep]
                    stats["tokens"] += int(keep.sum())
                    stats["logp_sum"] += float(lp.sum())
                    stats["rank1"] += int((logp1[live].argmax(-1) == chosen)[keep].sum())
                    if con is not None:
                        top = logp1[live].argmax(-1)
                        stats["overridden"] += int((~hard[live].gather(1, top[:, None])[:, 0])[keep].sum())
                        vm = torch.exp(torch.logsumexp(torch.where(hard[live], logp1[live], torch.full_like(logp1[live], -math.inf)), -1))
                        stats["vm_sum"] += float(vm[keep].sum())
                for k in range(K):
                    if not (todo[k] and alive[k]):
                        continue
                    t = int(nxt[k])
                    logw[k] += float(logz[k])
                    canv[k, p] = t
                    if con is not None:
                        states[k] = con.advance(states[k], t)
                    if self.lex is not None:
                        words[k] = self.lex.advance(words[k], t)
                    if t == self.tok.eos_id:
                        done[k] = True
                        canv[k, p:] = self.tok.eos_id
                lv = alive & (logw > -math.inf)
                if lv.sum() > 1:
                    w = torch.exp(logw[lv] - logw[lv].max())
                    ess = float(w.sum() ** 2 / (w ** 2).sum())
                    if ess < cfg.ess_threshold * int(lv.sum()):
                        idx = torch.nonzero(lv).squeeze(1)
                        pick = idx[self._systematic(w / w.sum(), K, g)]
                        canv = canv[pick].clone()
                        states = [states[int(i)] for i in pick]
                        words = [words[int(i)] for i in pick]
                        done = done[pick].clone()
                        alive = torch.ones(K, dtype=torch.bool, device=dev)
                        m = torch.logsumexp(logw[lv], 0) - math.log(int(lv.sum()))
                        logw = torch.full((K,), float(m), device=dev, dtype=torch.float64)
                        n_resample += 1

            def text_of(k):
                ids = canv[k, len(pre):].tolist()
                ids = ids[: ids.index(self.tok.eos_id)] if self.tok.eos_id in ids else [i for i in ids if i != self.mask_id]
                return self.tok.decode(ids)

            cands = {}
            for k in range(K):
                if done[k] and alive[k]:
                    t = text_of(k)
                    if t not in cands or float(logw[k]) > cands[t]["logw"]:
                        cands[t] = {"poem": t, "lines": [ln.strip() for ln in t.split("\n") if ln.strip()], "logw": float(logw[k])}
            out = {"candidates": list(cands.values()), "resamples": n_resample, "stats": dict(stats)}
            if cfg.rerank and out["candidates"]:
                self.rerank(out, label, meaning, register, src)
            if out["candidates"]:
                best = out.get("best") or out["candidates"][0]
                out.update(text=best["poem"], status="complete")
            else:
                k = int(alive.float().argmax()) if alive.any() else 0
                out.update(text=text_of(k), status="max_tokens" if alive.any() else "dead")
            out["n_tokens"] = last + 1
            return out

    return TracingDecoder


def generate(out: Path, modes: list[str], only_meters=None, seeds=SEEDS) -> None:
    out.mkdir(parents=True, exist_ok=True)
    import torch
    from tokenizer import load_default
    from ft.decode import DecodeConfig, load_model
    tok = load_default()
    meters, topics = grid()
    if only_meters:
        meters = [m for m in meters if m in only_meters]
    dev = torch.device("cuda")
    model, prov = load_model(PILOT, dev)
    Tracing = make_decoder_class()
    res = out / "results.jsonl"
    done = {json.loads(l)["key"] for l in res.open(encoding="utf-8")} if res.exists() else set()
    with res.open("a", encoding="utf-8") as fh:
        for mode in modes:
            decoders = {s: Tracing(model, tok, dev, DecodeConfig(**MODES[mode], seed=s)) for s in seeds}
            n = 0
            for meter in meters:
                for tkey, topic in topics.items():
                    for s in seeds:
                        key = f"{meter}|{tkey}|{mode}|{s}"
                        if key in done:
                            continue
                        t0 = time.time()
                        o = decoders[s].generate(meter, topic)
                        row = {"key": key, "meter": meter, "topic": tkey, "mode": mode, "seed": s, "model": "pilot120m (base)",
                               "status": o["status"], "text": o["text"], "n_tokens": o["n_tokens"], "resamples": o["resamples"],
                               "stats": o["stats"], "candidates": len(o["candidates"]), "seconds": round(time.time() - t0, 2)}
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                        fh.flush()
                        n += 1
                        if n % 50 == 0:
                            print(f"  {mode} {n}/{len(meters) * len(topics) * len(SEEDS)}", flush=True)
                            decoders[s].save_yati_cache()
            next(iter(decoders.values())).save_yati_cache()
    (out / "run.json").write_text(json.dumps({
        "model": {"run": str(PILOT.relative_to(ROOT)), "provenance": prov},
        "grid": {"meters": meters, "topics": topics, "seeds": list(SEEDS)},
        "modes": {m: dataclasses.asdict(DecodeConfig(**MODES[m])) for m in MODES},
        "masking_rule_set": "DecodeConfig(yati_profile=strict, yati_sandhi=off, prasa_relaxed=False, vikalpa=False, "
                            "yati_weight=1e4): canonical weights, strict prāsa, hard yati from ft.yati_oracle",
        "decoder": "diffusion_finetuning/ft/decode.py (TracingDecoder: same sampler, plus per-step statistics)",
        "torch": torch.__version__}, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ evaluation (CPU)
def reading_level(notes) -> str:
    text = " ".join(notes)
    return "compound" if "compound-boundary" in text else ("vikalpa" if "vikalpa" in text else "canonical")


def evaluate_one(row):
    from chandohasam import analyze
    from indic_meter_dawg import identify_text
    lines = [ln.strip() for ln in row["text"].split("\n") if ln.strip()]
    ev = {"lines": lines, "duplicate_lines": len(lines) - len(set(lines))}
    if not lines:
        return row["key"], dict(ev, gana=False, gana_canonical=False, prasa_strict=False, yati_strict=False,
                                prasa_relaxed=False, yati_relaxed=False)
    ident = identify_text("\n".join(lines))
    meter = row["meter"]
    listed = meter in [c.meter for c in ident.candidates]
    ev["reading"] = reading_level(ident.notes) if listed else None
    ev["gana_canonical"] = bool(listed and ev["reading"] == "canonical")
    for prof, sandhi, suf in (("strict", "off", "strict"), ("relaxed", "hypothesis", "relaxed")):
        a = analyze(lines, profile=prof, yati_sandhi=sandhi, meter=meter, identification=ident)
        head = bool(a.identified and a.units and a.units[0].meter == meter)
        if suf == "strict":
            ev["gana"] = head
        ev[f"prasa_{suf}"] = bool(head and a.prasa_matched)
        ev[f"yati_{suf}"] = bool(head and a.yati_matched)
    return row["key"], ev


def evaluate(out: Path, jobs: int) -> None:
    rows = [json.loads(l) for l in (out / "results.jsonl").open(encoding="utf-8")]
    with Pool(jobs) as pool:
        ev = dict(pool.map(evaluate_one, rows, chunksize=4))
    with (out / "results.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            e = ev[r["key"]]
            e["in_meter"] = bool(r["status"] == "complete" and e["gana_canonical"] and e["prasa_strict"] and e["yati_strict"])
            lic = e.get("reading") in ("canonical", "vikalpa")
            e["in_meter_licensed"] = bool(r["status"] == "complete" and lic and e["prasa_strict"] and e["yati_strict"])
            e["in_meter_relaxed"] = bool(r["status"] == "complete" and lic and e["prasa_relaxed"] and e["yati_relaxed"])
            fh.write(json.dumps(dict(r, eval=e), ensure_ascii=False) + "\n")
    print("evaluated", len(rows))


# ------------------------------------------------------------------ metrics (judge on GPU)
def metrics(out: Path) -> dict:
    sys.path.insert(0, str(ROOT / "data_sanity_metrics"))
    sys.path.insert(0, str(ROOT / "writeups" / "scripts"))
    from common.dataset import load_poems
    from common.telugu import words
    import compute_generation_metrics as cgm
    from mdlm.judge import load_judge, perplexity

    poems = load_poems()
    lexicon = {w for p in poems if p.corpus != "chandassu" for ln in p.lines for w in words(ln)}
    chandassu = [p.text for p in poems if p.corpus == "chandassu"]
    rng = random.Random(0)
    ref = rng.sample(chandassu, 555)
    shuffled = []
    for t in ref:
        ws = t.split()
        rng.shuffle(ws)
        shuffled.append(" ".join(ws))
    rows = [json.loads(l) for l in (out / "results.jsonl").open(encoding="utf-8")]
    jtok, jmodel = load_judge()
    result = {"pilot120m (base)": {}}
    by_mode = defaultdict(list)
    for r in rows:
        by_mode[r["mode"]].append(r)
    for mode, rs in by_mode.items():
        st = Counter()
        for r in rs:
            st.update(r["stats"])
        texts = [r["text"] for r in rs]
        result["pilot120m (base)"][mode] = {
            "poems": len(rs), "status": dict(Counter(r["status"] for r in rs)),
            "in_meter": sum(r["eval"]["in_meter"] for r in rs),
            "in_meter_licensed": sum(r["eval"]["in_meter_licensed"] for r in rs),
            "in_meter_relaxed": sum(r["eval"]["in_meter_relaxed"] for r in rs),
            "yati_relaxed": sum(r["eval"]["yati_relaxed"] for r in rs), "prasa_relaxed": sum(r["eval"]["prasa_relaxed"] for r in rs),
            "gana": sum(r["eval"]["gana"] for r in rs), "gana_canonical": sum(r["eval"]["gana_canonical"] for r in rs),
            "prasa_strict": sum(r["eval"]["prasa_strict"] for r in rs), "yati_strict": sum(r["eval"]["yati_strict"] for r in rs),
            "reading": dict(Counter(r["eval"].get("reading") for r in rs)),
            **cgm.word_stats(texts, lexicon),
            "poems_repeating_a_line": sum(r["eval"]["duplicate_lines"] > 0 for r in rs),
            "mean_logp": st["logp_sum"] / st["tokens"] if st["tokens"] else None,
            "rank1_share": st["rank1"] / st["tokens"] if st["tokens"] else None,
            "overridden_share": st["overridden"] / st["tokens"] if st.get("vm_sum") else None,
            "mean_valid_mass": st["vm_sum"] / st["tokens"] if st.get("vm_sum") else None,
            "mean_seconds": mean(r["seconds"] for r in rs),
            "judge_ppl": perplexity(texts, jtok, jmodel),
        }
        print(mode, json.dumps(result["pilot120m (base)"][mode], ensure_ascii=False)[:400], flush=True)
    step = json.loads((ROOT / "writeups" / "data" / "generation_metrics.json").read_text(encoding="utf-8"))["models"]
    for model, run_list in GRIDS.items():
        result[model] = {}
        grows = defaultdict(list)
        for run in run_list:
            for r in cgm.run_rows(run):
                grows[r["mode"]].append(r)
        for mode, rs in grows.items():
            ts = [r["text"] for r in rs]
            result[model][mode] = {
                "poems": len(rs), "in_meter": sum(cgm.in_meter(r) for r in rs),
                "all_relaxed": sum(bool((r.get("eval") or {}).get("all_relaxed")) for r in rs),
                **cgm.word_stats(ts, lexicon),
                "poems_repeating_a_line": sum(1 for r in rs if (r.get("eval") or {}).get("duplicate_lines", 0) > 0),
                "judge_ppl": perplexity(ts, jtok, jmodel),
                **{k: step.get(model, {}).get(mode, {}).get(k) for k in ("mean_logp", "overridden_share", "mean_valid_mass")}}
            print(model, mode, result[model][mode], flush=True)
    result["reference"] = {"chandassu_555": {**cgm.word_stats(ref, lexicon), "judge_ppl": perplexity(ref, jtok, jmodel)},
                           "chandassu_555_word_shuffled": {"judge_ppl": perplexity(shuffled, jtok, jmodel)},
                           "judge": "google/gemma-3-1b-pt (mdlm.judge)", "lexicon_word_types": len(lexicon)}
    (out / "metrics.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    return result


def table(out: Path) -> str:
    """The comparison as a Markdown table (metrics.json)."""
    m = json.loads((out / "metrics.json").read_text(encoding="utf-8"))
    pct = lambda x: "—" if x is None else f"{100 * x:.1f}%"                    # noqa: E731
    num = lambda x, f="{:.2f}": "—" if x is None else f.format(x)            # noqa: E731
    names = {"baseline": "free", "masking_only": "masking", "masking_backtrack": "backtracking", "hybrid": "hybrid"}
    rows = ["| model | mode | in metre (strict) | attested words | single-akshara words | poems repeating a line "
            "| judge PPL | chosen-token log-prob* | first choice not allowed* | allowed mass* |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    ref = m["reference"]
    for model, modes in m.items():
        if model == "reference":
            continue
        for mode, v in modes.items():
            n = v["poems"]
            rows.append(f"| {model} | {names.get(mode, mode)} | {v['in_meter']} / {n} | {pct(v.get('attested_share'))} | "
                        f"{pct(v.get('single_akshara_share'))} | {v['poems_repeating_a_line']} / {n} | {num(v['judge_ppl'], '{:.1f}')} | "
                        f"{num(v.get('mean_logp'))} | {pct(v.get('overridden_share'))} | {num(v.get('mean_valid_mass'))} |")
    c = ref["chandassu_555"]
    rows.append(f"| real verse, unseen (Chandassu, 555 poems) | | | {pct(c['attested_share'])} | {pct(c['single_akshara_share'])} | "
                f"| {c['judge_ppl']:.1f} | | | |")
    rows.append(f"| the same, words shuffled | | | | | | {ref['chandassu_555_word_shuffled']['judge_ppl']:.1f} | | | |")
    return "\n".join(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("cmd", choices=("generate", "evaluate", "metrics", "table"))
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--modes", nargs="+", default=list(MODES))
    ap.add_argument("--jobs", type=int, default=10)
    ap.add_argument("--meters", nargs="+", default=None, help="restrict the grid (smoke tests)")
    ap.add_argument("--seeds", nargs="+", type=int, default=list(SEEDS))
    args = ap.parse_args()
    out = args.out_dir.resolve()
    if args.cmd == "generate":
        generate(out, args.modes, args.meters, tuple(args.seeds))
    elif args.cmd == "evaluate":
        evaluate(out, args.jobs)
    elif args.cmd == "metrics":
        metrics(out)
    else:
        print(table(out))


if __name__ == "__main__":
    main()
