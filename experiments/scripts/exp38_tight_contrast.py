#!/usr/bin/env python3
"""
EXP-38: synthetic tight-contrast set (metre-breaking vs metre-preserving single edits) and the
direction it gives, with `<bos>`.

Spec: experiments/EXP-38-synthetic-tight-contrast-set-for-a-metre-specific-direction.md.

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py build OUT_DIR     # CPU
    diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py extract OUT_DIR   # GPU
    diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py analyse OUT_DIR   # CPU

build:
- sources: Bhāgavatam verse poems of the 8 balanced-sample metres (4 lines, non-empty bhavam) that the
  engine accepts in their labelled metre (chandohasam.analyze, profile relaxed, sandhi hypothesis,
  metre forced), visited in a seeded random order per metre.
- edits, one per variant:
    synonym  a word of the verse (present exactly once) replaced by its single-word teeka gloss
             (teeka_pairs), the spec's synonym source;
    swap     two adjacent words of one line exchanged.
  A variant *breaks* the metre when the DAWG no longer lists the labelled metre among its candidates
  (a gaṇa/weight failure). It *preserves* the metre when the engine still accepts it (same analysis
  as the source).
- a triple = (source, break, preserve) with both edits of the same kind; at most one triple per
  source poem, at most TARGET triples per metre and edit kind; at most CAP candidate edits per poem.
extract:
- content check (spec step 4): IndicSBERT (l3cube-pune/indic-sentence-bert-nli; mean pooling over tokens,
  L2-normalised) cosine of each text with the source's bhavam; a triple is kept when
  neither variant falls more than DELTA below the source.
- last-token hidden states (`<bos>` + poem, 36 indices) of the three texts of every kept triple.
analyse:
- per layer: d_break = mean(h(src) - h(break)), d_preserve = mean(h(src) - h(pres)), d_metre =
  d_break - d_preserve; coherence (EXP-22's mean pairwise cosine) of the per-triple differences;
  cos(d_break, d_preserve) (near 1 means the "metre" direction is an edit direction); a sign-flip
  null for d_metre's coherence (break and preserve exchanged at random within triples).
"""
from __future__ import annotations

import argparse
import datetime
import json
import random
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

METRES = ("aataveladi", "champakamala", "kandamu", "mattakokila", "mattebhavikriditamu", "shardulavikriditamu",
          "tetagiti", "utpalamala")
CATALOGUE = {"aataveladi": "ataveladi", "shardulavikriditamu": "sardulavikriditamu", "mattakokila": "mattakokilamu"}
TARGET = 25          # triples per metre and edit kind
CAP = 60             # candidate edits tried per source poem
DELTA = 0.05         # content check
FLIPS = 1000
SENTENCE_MODEL = "l3cube-pune/indic-sentence-bert-nli"


def nfc(x: str) -> str:
    return unicodedata.normalize("NFC", x).strip()


def accepts(lines, metre):
    from chandohasam import analyze
    a = analyze(lines, profile="relaxed", yati_sandhi="hypothesis", meter=CATALOGUE.get(metre, metre))
    target = CATALOGUE.get(metre, metre)
    head = bool(a.identified and a.units and a.units[0].meter == target)
    return head and a.matched, target in [c.split("+")[0] for c in a.candidates]


def candidates(rec):
    lines = [nfc(x) for x in rec["verse"]]
    words = [w for ln in lines for w in ln.split()]
    count = Counter(words)
    out = []
    for tp in rec.get("teeka_pairs") or []:
        w, m = nfc(tp.get("word", "")), nfc(tp.get("meaning", ""))
        if w and m and " " not in m and m != w and count.get(w) == 1:
            out.append(("synonym", {"word": w, "replacement": m}))
    for li, ln in enumerate(lines):
        ws = ln.split()
        for k in range(len(ws) - 1):
            if ws[k] != ws[k + 1]:
                out.append(("swap", {"line": li, "position": k}))
    return lines, out


def apply(lines, kind, e):
    if kind == "synonym":
        return [" ".join(e["replacement"] if w == e["word"] else w for w in ln.split()) for ln in lines]
    ws = lines[e["line"]].split()
    ws[e["position"]], ws[e["position"] + 1] = ws[e["position"] + 1], ws[e["position"]]
    return [(" ".join(ws) if i == e["line"] else ln) for i, ln in enumerate(lines)]


def triples_for(rec):
    lines, cands = candidates(rec)
    ok, _ = accepts(lines, rec["metre_roman"])
    if not ok:
        return rec["id"], "source_not_accepted", None
    rng = random.Random(f"exp38:{rec['id']}")
    rng.shuffle(cands)
    found = defaultdict(dict)
    tried = 0
    for kind, e in cands[:CAP]:
        if "break" in found[kind] and "preserve" in found[kind]:
            continue
        variant = apply(lines, kind, e)
        tried += 1
        matched, listed = accepts(variant, rec["metre_roman"])
        role = "preserve" if matched else ("break" if not listed else None)
        if role and role not in found[kind]:
            found[kind][role] = {"edit": e, "lines": variant}
        if any(len(v) == 2 for v in found.values()):
            break
    for kind in ("synonym", "swap"):
        if len(found[kind]) == 2:
            return rec["id"], "triple", {"id": rec["id"], "metre": rec["metre_roman"], "kind": kind, "source": lines,
                                         "bhavam": nfc(rec["bhavam"])[:2000], "tried": tried, **found[kind]}
    return rec["id"], "no_triple", {"tried": tried}


# ------------------------------------------------------------------ build (CPU)
def build(out: Path, seed: int, jobs: int) -> None:
    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    records = json.loads((ROOT / "dataset" / "bhagavatam.json").read_text(encoding="utf-8"))
    pools = defaultdict(list)
    for r in records:
        if r["metre_roman"] in METRES and r["form"] == "verse" and r["verse"] and len(r["verse"]) == 4 and (r["bhavam"] or "").strip():
            pools[r["metre_roman"]].append(r)
    got, stats = [], defaultdict(Counter)
    with Pool(jobs) as pool:
        for m in METRES:
            order = pools[m][:]
            random.Random(f"exp38:{seed}:{m}").shuffle(order)
            per_kind = Counter()
            for start in range(0, len(order), jobs * 4):
                if all(per_kind[k] >= TARGET for k in ("synonym", "swap")):
                    break
                for rid, status, t in pool.map(triples_for, order[start:start + jobs * 4]):
                    stats[m][status] += 1
                    if status == "triple" and per_kind[t["kind"]] < TARGET:
                        per_kind[t["kind"]] += 1
                        got.append(t)
            stats[m]["triples_synonym"] = per_kind["synonym"]
            stats[m]["triples_swap"] = per_kind["swap"]
            stats[m]["pool"] = len(pools[m])
            print(m, dict(stats[m]), flush=True)
    with (out / "triples.jsonl").open("w", encoding="utf-8") as fh:
        for t in got:
            fh.write(json.dumps(t, ensure_ascii=False) + "\n")
    (out / "build.json").write_text(json.dumps({"date": datetime.date.today().isoformat(), "seed": seed, "target_per_kind": TARGET,
                                                 "cap": CAP, "yield": {m: dict(v) for m, v in stats.items()},
                                                 "seconds": round(time.time() - t0, 1)}, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ extract (GPU)
def extract(out: Path, seed: int, device: str) -> None:
    import numpy as np
    import torch
    from transformers import AutoModel, AutoTokenizer
    import exp35_surprisal as e35

    triples = [json.loads(l) for l in (out / "triples.jsonl").open(encoding="utf-8")]
    # content check
    stok = AutoTokenizer.from_pretrained(SENTENCE_MODEL, local_files_only=True)
    smod = AutoModel.from_pretrained(SENTENCE_MODEL, local_files_only=True).to(device).eval()

    def embed(texts):
        vs = []
        with torch.no_grad():
            for i in range(0, len(texts), 32):
                b = stok(texts[i:i + 32], padding=True, truncation=True, max_length=512, return_tensors="pt").to(device)
                h = smod(**b).last_hidden_state
                m = b["attention_mask"].unsqueeze(-1).float()
                v = (h * m).sum(1) / m.sum(1)
                vs.append(torch.nn.functional.normalize(v, dim=-1).cpu())
        return torch.cat(vs)

    join = lambda ls: "\n".join(ls)                                             # noqa: E731
    S = embed([join(t["source"]) for t in triples]); Bv = embed([join(t["break"]["lines"]) for t in triples])
    Pv = embed([join(t["preserve"]["lines"]) for t in triples]); H = embed([t["bhavam"] for t in triples])
    sim = lambda a: (a * H).sum(-1).tolist()                                    # noqa: E731
    s_src, s_brk, s_prs = sim(S), sim(Bv), sim(Pv)
    kept = []
    for t, a, b, c in zip(triples, s_src, s_brk, s_prs):
        t["similarity"] = {"source": round(a, 4), "break": round(b, 4), "preserve": round(c, 4)}
        t["content_ok"] = b >= a - DELTA and c >= a - DELTA
        if t["content_ok"]:
            kept.append(t)
    del smod
    torch.cuda.empty_cache()

    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    model, cfg = e35.build_model(snap, device, seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)
    arrays = {"source": [], "break": [], "preserve": []}
    with torch.no_grad():
        for t in kept:
            for role, lines in (("source", t["source"]), ("break", t["break"]["lines"]), ("preserve", t["preserve"]["lines"])):
                text = "\n".join(e35.poem_text({"verse": lines}).split("\n"))
                ids = [tok.bos_token_id] + tok(text, add_special_tokens=False)["input_ids"]
                x = torch.tensor([ids])
                emb = model.model.embed_tokens(x.to(device))
                pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(device)
                hs = model.model(inputs_embeds=emb, per_layer_inputs=pli, use_cache=False, output_hidden_states=True).hidden_states
                arrays[role].append(torch.stack([h[0, -1] for h in hs]).float().cpu().numpy())
    for role, v in arrays.items():
        np.save(out / f"pooled_{role}.npy", np.stack(v))
    with (out / "kept.jsonl").open("w", encoding="utf-8") as fh:
        for t in kept:
            fh.write(json.dumps({k: t[k] for k in ("id", "metre", "kind", "similarity")}, ensure_ascii=False) + "\n")
    (out / "extract.json").write_text(json.dumps({"triples": len(triples), "content_ok": len(kept), "delta": DELTA,
                                                   "sentence_model": SENTENCE_MODEL, "similarity_all": [t["similarity"] for t in triples],
                                                   "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "load": load_report}},
                                                  ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"triples {len(triples)}, content check passed {len(kept)}")


# ------------------------------------------------------------------ analyse (CPU)
def analyse(out: Path) -> dict:
    import numpy as np
    from exp22_directions import coherence

    Ssrc = np.load(out / "pooled_source.npy").astype(np.float64)
    Sb = np.load(out / "pooled_break.npy").astype(np.float64)
    Sp = np.load(out / "pooled_preserve.npy").astype(np.float64)
    kept = [json.loads(l) for l in (out / "kept.jsonl").open(encoding="utf-8")]
    kinds = np.array([k["kind"] for k in kept])

    def block(mask):
        db, dp = Ssrc[mask] - Sb[mask], Ssrc[mask] - Sp[mask]
        dm = db - dp                                  # = h(preserve) - h(break) per triple
        mb, mp = db.mean(0), dp.mean(0)
        cos_bp = (mb * mp).sum(-1) / (np.linalg.norm(mb, axis=-1) * np.linalg.norm(mp, axis=-1))
        rng = np.random.default_rng(0)
        null = []
        for _ in range(FLIPS):
            sgn = rng.choice([-1.0, 1.0], size=(len(dm), 1, 1))
            null.append(float(np.nanmax(coherence(dm * sgn))))
        c_b, c_p, c_m = coherence(db), coherence(dp), coherence(dm)
        L = len(c_m)
        return {"triples": int(mask.sum()),
                "coherence_break": {"peak": round(float(np.nanmax(c_b)), 4), "layer": int(np.nanargmax(c_b))},
                "coherence_preserve": {"peak": round(float(np.nanmax(c_p)), 4), "layer": int(np.nanargmax(c_p))},
                "coherence_metre": {"peak": round(float(np.nanmax(c_m)), 4), "layer": int(np.nanargmax(c_m)),
                                    "by_layer": [round(float(x), 4) for x in c_m]},
                "sign_flip_null_peak": {"p95": round(float(np.percentile(null, 95)), 4), "p99": round(float(np.percentile(null, 99)), 4)},
                "cos_d_break_d_preserve": {"min": round(float(np.nanmin(cos_bp)), 4), "median": round(float(np.nanmedian(cos_bp)), 4),
                                           "max": round(float(np.nanmax(cos_bp)), 4), "by_layer": [round(float(x), 4) for x in cos_bp]},
                "norm_d_metre_by_layer": [round(float(np.linalg.norm((mb - mp)[l])), 3) for l in range(L)]}

    summary = {"all": block(np.ones(len(kept), bool)),
               "synonym": block(kinds == "synonym") if (kinds == "synonym").sum() >= 5 else None,
               "swap": block(kinds == "swap") if (kinds == "swap").sum() >= 5 else None,
               "per_metre_triples": dict(Counter(k["metre"] for k in kept)),
               "per_kind_triples": dict(Counter(k["kind"] for k in kept)),
               "compare": {"exp22_coarse_peak": 0.475, "exp22_best_pair_peak": 0.158, "pipeline_coarse": 0.322,
                           "pipeline_pair": "0.5-0.65 (not reproduced, see EXP-22)"}}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", choices=("build", "extract", "analyse"))
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--jobs", type=int, default=10)
    args = ap.parse_args()
    if args.mode == "build":
        build(args.out_dir, args.seed, args.jobs)
    elif args.mode == "extract":
        extract(args.out_dir, args.seed, args.device)
    else:
        s = analyse(args.out_dir)
        print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk not in ("by_layer",)} if isinstance(v, dict) else v)
                          for k, v in s.items()}, ensure_ascii=False, indent=1)[:5000])


if __name__ == "__main__":
    main()
