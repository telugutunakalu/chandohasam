"""Evaluation (PLAN §8). Everything is local; no score here reuses a training or reranking signal.

    # predictions: our model (constrained or free), the retrieval baseline, the real poems
    python -m ft.evaluate decode    --run runs/s2-... --split val --n 200 --out runs/s2-.../eval/val.jsonl
    python -m ft.evaluate decode    --run runs/s2-... --split val --n 200 --free --out .../val_free.jsonl
    python -m ft.evaluate retrieval --split val --n 200 --out data/eval/val_retrieval.jsonl
    python -m ft.evaluate reference --split val --n 200 --out data/eval/val_reference.jsonl
    # metrics for any prediction file, and the words for the hand-checked non-word audit
    python -m ft.evaluate score --pred runs/s2-.../eval/val.jsonl
    python -m ft.evaluate audit --pred runs/s2-.../eval/val.jsonl --n 100

Items: metrical eval poems with an edition meaning, a fixed metre-stratified sample (seed 0),
leaked poems (data/leakage.json) excluded. The meaning judge is ft.judge.
"""
from __future__ import annotations

import argparse
import collections
import csv
import dataclasses
import json
import math
import re
import time
from pathlib import Path

import numpy as np

from . import DATA_DIR, PRETRAIN_ROOT

TOKEN_DIR = PRETRAIN_ROOT.parent / "pretraining_datasets" / "tokens"
_WORD = re.compile(r"[ఀ-౥౰-౿]+")


def eval_items(split: str, n: int, data_dir: Path = DATA_DIR, seed: int = 0) -> list[dict]:
    leaked = set()
    lp = data_dir / "leakage.json"
    if lp.exists():
        leaked = {k for k, v in json.loads(lp.read_text(encoding="utf-8"))["items"].items() if v["poem"]}
    rows = [json.loads(l) for l in (data_dir / "records" / f"{split}.jsonl").open(encoding="utf-8")]
    rows = [r for r in rows if r["status"] == "agree" and r.get("meaning") and r["meaning_src"] == "గ్రంథం"
            and r["id"] not in leaked]
    if n <= 0 or n >= len(rows):
        return rows
    by = collections.defaultdict(list)
    for r in rows:
        by[r["meter_label"]].append(r)
    rng = np.random.default_rng(seed)
    out = []
    for label, group in sorted(by.items()):
        k = max(1, round(n * len(group) / len(rows)))
        out += [group[i] for i in rng.choice(len(group), size=min(k, len(group)), replace=False)]
    rng.shuffle(out)
    return out[:n]


def _write(rows: list[dict], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")


def _base(r: dict) -> dict:
    return {"id": r["id"], "metre": r["meter_label"], "meaning": r["meaning"], "meaning_en": r.get("meaning_en"),
            "gold": r["lines"]}


# -----------------------------------------------------------------------------
# prediction makers
# -----------------------------------------------------------------------------
def cmd_decode(args) -> int:
    import torch

    from tokenizer import load_default

    from .decode import DecodeConfig, Decoder, load_model
    dev = torch.device("cuda")
    model, prov = load_model(args.run, dev)
    cfg = DecodeConfig(particles=args.particles, guidance=args.guidance, temperature=args.temperature,
                       lexicon_lam=0.0 if args.free else args.lexicon_lam, yati_weight=0.0 if args.free else args.yati_weight,
                       constrained=not args.free, seed=args.seed)
    dec = Decoder(model, load_default(), dev, cfg, args.data_dir)
    rows = []
    for i, r in enumerate(eval_items(args.split, args.n, args.data_dir)):
        t0 = time.time()
        out = dec.generate(r["meter_label"], r["meaning"])
        best = out.get("best") or (out["candidates"][0] if out["candidates"] else None)
        rows.append(_base(r) | {"system": "free" if args.free else "constrained", "model": str(args.run),
                                "decode": dataclasses.asdict(cfg), "poem": best["lines"] if best else [],
                                "candidates": [c["lines"] for c in out["candidates"]],
                                "allowed_mass": out.get("allowed_mass"), "resamples": out.get("resamples"),
                                "seconds": round(time.time() - t0, 1)})
        print(f"[{i + 1}] {r['id']} {r['meter_label']}: {len(out['candidates'])} candidates, "
              f"{time.time() - t0:.1f}s", flush=True)
        if (i + 1) % 10 == 0:
            _write(rows, args.out)
    _write(rows, args.out)
    return 0


def cmd_reference(args) -> int:
    _write([_base(r) | {"system": "reference", "poem": r["lines"], "candidates": [r["lines"]]}
            for r in eval_items(args.split, args.n, args.data_dir)], args.out)
    return 0


def _tfidf(texts: list[str]):
    """Word unigram + bigram TF-IDF vectors as dicts (L2-normalised), and the idf table."""
    docs = []
    for t in texts:
        w = _WORD.findall(t)
        docs.append(collections.Counter(w + [a + " " + b for a, b in zip(w, w[1:])]))
    df = collections.Counter(term for d in docs for term in d)
    n = len(docs)
    idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
    vecs = []
    for d in docs:
        v = {t: c * idf[t] for t, c in d.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs.append({t: x / norm for t, x in v.items()})
    return vecs, idf


def cmd_retrieval(args) -> int:
    """Baseline: the training poem, in the same metre, whose meaning is closest (TF-IDF cosine)."""
    items = eval_items(args.split, args.n, args.data_dir)
    wanted = {r["meter_label"] for r in items}
    pool = collections.defaultdict(list)
    for line in (args.data_dir / "records" / "train.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["status"] in ("agree", "engine-only") and r.get("meaning") and r.get("meter_label") in wanted:
            pool[r["meter_label"]].append((r["meaning"], r["lines"], r["id"]))
    rows = []
    for label, group in pool.items():
        queries = [r for r in items if r["meter_label"] == label]
        vecs, idf = _tfidf([g[0] for g in group] + [q["meaning"] for q in queries])
        index = collections.defaultdict(list)
        for i, v in enumerate(vecs[: len(group)]):
            for t, x in v.items():
                index[t].append((i, x))
        for q, qv in zip(queries, vecs[len(group):]):
            scores = collections.Counter()
            for t, x in qv.items():
                for i, y in index.get(t, ()):
                    scores[i] += x * y
            i, s = scores.most_common(1)[0] if scores else (0, 0.0)
            rows.append(_base(q) | {"system": "retrieval", "poem": group[i][1], "candidates": [group[i][1]],
                                    "retrieved": group[i][2], "similarity": round(s, 4)})
    _write(rows, args.out)
    return 0


# -----------------------------------------------------------------------------
# metrics
# -----------------------------------------------------------------------------
def eval_lexicon(data_dir: Path) -> set[str]:
    """Words of the pretraining val split (cached by mdlm.train): disjoint from the decoding lexicon,
    which is built from the train split and the training poems."""
    return {w for x in (TOKEN_DIR / "val_words.txt").read_text(encoding="utf-8").split("\n") for w in _WORD.findall(x)}


def _grams(tokens: list[int], n: int) -> list[tuple]:
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def score_rows(rows: list[dict], data_dir: Path) -> dict:
    from tokenizer import load_default

    from .engines import verdict
    tok = load_default()
    lex = eval_lexicon(data_dir)
    agg = collections.defaultdict(list)
    per_metre = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        lines = r["poem"]
        v = verdict(lines, r["metre"]) if lines else {"metre_ok": False, "prasa_relaxed": False, "yati_relaxed": False,
                                                       "prasa_strict": False, "yati_strict": False}
        words = [w for ln in lines for w in _WORD.findall(ln)]
        ptoks = [t for t in tok.encode("\n".join(lines)) if t > 4]
        mtoks = set(_grams([t for t in tok.encode(r["meaning"]) if t > 4], 4))
        pg = _grams(ptoks, 4)
        cands = [[t for t in tok.encode("\n".join(c)) if t > 4] for c in r.get("candidates") or []]
        rec = {"produced": float(bool(lines)), "metre_ok": float(v["metre_ok"]),
               "prasa_relaxed": float(v["prasa_relaxed"]), "yati_relaxed": float(v["yati_relaxed"]),
               "prasa_strict": float(v["prasa_strict"]), "yati_strict": float(v["yati_strict"]),
               "all_strict": float(v["metre_ok"] and v["prasa_strict"] and v["yati_strict"]),
               "lexicon_share": sum(w in lex for w in words) / max(1, len(words)) if words else 0.0,
               "copy_rate": sum(g in mtoks for g in pg) / max(1, len(pg)) if pg else 0.0,
               "distinct2": len(set(_grams(ptoks, 2))) / max(1, len(ptoks) - 1) if ptoks else 0.0,
               "repeated_line": float(len(set(lines)) < len(lines)),
               "candidates": float(len(cands))}
        if len(cands) > 1:
            sets = [set(_grams(c, 4)) for c in cands]
            pair = [len(a & b) / max(1, len(a | b)) for i, a in enumerate(sets) for b in sets[i + 1:]]
            rec["self_overlap4"] = float(np.mean(pair))
        if r.get("allowed_mass") is not None:
            rec["allowed_mass"] = r["allowed_mass"]
        for k, x in rec.items():
            agg[k].append(x)
            per_metre[r["metre"]][k].append(x)
    out = {"items": len(rows), "system": rows[0].get("system") if rows else None,
           "mean": {k: round(float(np.mean(v)), 4) for k, v in agg.items()},
           "per_metre": {m: {"items": len(d["metre_ok"]), **{k: round(float(np.mean(v)), 4) for k, v in d.items()
                                                             if k in ("metre_ok", "all_strict", "lexicon_share")}}
                         for m, d in sorted(per_metre.items())}}
    return out


def cmd_score(args) -> int:
    rows = [json.loads(l) for l in args.pred.open(encoding="utf-8")]
    rep = score_rows(rows, args.data_dir)
    out = args.pred.with_suffix(".score.json")
    out.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(rep["mean"], indent=2))
    return 0


def cmd_audit(args) -> int:
    """Random words outside the evaluation lexicon, for a person to mark real / non-word."""
    lex = eval_lexicon(args.data_dir)
    rows = [json.loads(l) for l in args.pred.open(encoding="utf-8")]
    pool = [(w, r["id"], ln) for r in rows for ln in r["poem"] for w in _WORD.findall(ln) if w not in lex]
    total = sum(len(_WORD.findall(ln)) for r in rows for ln in r["poem"])
    rng = np.random.default_rng(args.seed)
    pick = [pool[i] for i in rng.choice(len(pool), size=min(args.n, len(pool)), replace=False)] if pool else []
    out = args.pred.with_suffix(".audit.csv")
    with out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["word", "poem_id", "line", "label (real / non-word)"])
        w.writerows([[a, b, c, ""] for a, b, c in pick])
    print(f"{len(pool)} of {total} words are outside the evaluation lexicon; {len(pick)} written to {out}. "
          f"Non-word rate = (non-words in the sample / {len(pick)}) x {len(pool) / max(1, total):.4f}.")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("decode", "reference", "retrieval"):
        p = sub.add_parser(name)
        p.add_argument("--split", default="val", choices=["val", "test", "test_seen"])
        p.add_argument("--n", type=int, default=200)
        p.add_argument("--out", type=Path, required=True)
        p.add_argument("--data-dir", type=Path, default=DATA_DIR)
        if name == "decode":
            p.add_argument("--run", type=Path, required=True)
            p.add_argument("--particles", type=int, default=16)
            p.add_argument("--guidance", type=float, default=0.0)
            p.add_argument("--temperature", type=float, default=1.0)
            p.add_argument("--lexicon-lam", type=float, default=2.0)
            p.add_argument("--yati-weight", type=float, default=3.0)
            p.add_argument("--free", action="store_true", help="no constraints, no lexicon: the model alone")
            p.add_argument("--seed", type=int, default=0)
    for name in ("score", "audit"):
        p = sub.add_parser(name)
        p.add_argument("--pred", type=Path, required=True)
        p.add_argument("--data-dir", type=Path, default=DATA_DIR)
        p.add_argument("--n", type=int, default=100)
        p.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    return {"decode": cmd_decode, "reference": cmd_reference, "retrieval": cmd_retrieval,
            "score": cmd_score, "audit": cmd_audit}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
