#!/usr/bin/env python3
"""
EXP-05: per-layer linear probe for guru/laghu, with the lookup control, rerun with `<bos>`.

Spec: experiments/EXP-05-per-layer-linear-probe-for-guru-laghu.md (steps 1-7). Model loading and the
balanced sample are EXP-35's (experiments/scripts/exp35_surprisal.py).

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp05_probe.py extract OUT_DIR   # GPU: states + labels
    <env with scikit-learn>/bin/python experiments/scripts/exp05_probe.py probe OUT_DIR         # CPU: probes + control

Sample: the first 10 poems of each metre in EXP-35's shuffled 200-poem sample (80 poems, 8 metres,
metre-balanced), every pāda scored separately as `<bos>` + pāda text, no chat template.

Labels: each token is mapped to the akshara (scanner syllable) containing its non-space characters.
A token whose characters fall in more than one akshara, or in none, has no clean span and is left out.
Its label is the akshara's weight from the scanner (canonical reading).

Lookup control (steps 5-7): an akshara is
  self-determined     when a guru rule of the akshara itself fires (deergha, sandhyakshara, anusvara,
                      visarga, pollu): its own characters decide the weight;
  context-determined  otherwise: it is guru only because a conjunct follows (samyukta), else laghu.
Baseline A (lookup) predicts guru exactly when a self rule fires. Baseline B adds the next akshara's
conjunct status (guru when the next akshara in the pāda is a conjunct), without the scanner's
word-boundary policy, so it can fall short of 100%.

probe: one logistic regression per hidden-state index (scikit-learn, max_iter=1000, default settings),
5-fold stratified cross-validation (shuffled, random_state=0); accuracy of the out-of-fold predictions,
overall and on each subset, beside both baselines and the majority-class rate.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / "meter_engine"))

PER_METRE = 10
SELF_RULES = {"deergha", "sandhyakshara", "anusvara", "visarga", "pollu"}


def extract(out: Path, seed: int, device: str) -> None:
    import numpy as np
    import torch
    import transformers
    from transformers import AutoTokenizer
    import exp35_surprisal as e35
    from indic_meter_dawg.scansion import scan

    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, eligible, metres = e35.balanced_sample(seed)
    chosen, seen = [], {}
    for r in sample:
        if seen.get(r["metre_roman"], 0) < PER_METRE:
            chosen.append(r)
            seen[r["metre_roman"]] = seen.get(r["metre_roman"], 0) + 1
    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    model, cfg = e35.build_model(snap, device, seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)

    states, labels = [], []
    counts = {"padas": 0, "tokens": 0, "clean": 0, "multi_akshara": 0, "no_akshara": 0}
    with torch.no_grad():
        for r in chosen:
            for p, line in enumerate(scan(r["verse"]), start=1):
                sy = line.syllables
                char2syl = [-1] * len(line.text)
                for k, s in enumerate(sy):
                    for c in range(s.start, s.end):
                        char2syl[c] = k
                enc = tok(line.text, add_special_tokens=False, return_offsets_mapping=True)
                keep = []
                for j, (a, b) in enumerate(enc["offset_mapping"]):
                    counts["tokens"] += 1
                    ks = {char2syl[c] for c in range(a, b) if not line.text[c].isspace()}
                    if len(ks) != 1 or -1 in ks:
                        counts["multi_akshara" if len(ks) > 1 else "no_akshara"] += 1
                        continue
                    keep.append((j, ks.pop()))
                counts["padas"] += 1
                if not keep:
                    continue
                ids = [tok.bos_token_id] + enc["input_ids"]
                x = torch.tensor([ids])
                emb = model.model.embed_tokens(x.to(device))
                pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(device)
                hs = model.model(inputs_embeds=emb, per_layer_inputs=pli, use_cache=False, output_hidden_states=True).hidden_states
                H = torch.stack([h[0] for h in hs], dim=1)          # [len(ids), 36, hidden]
                pos = torch.tensor([j + 1 for j, _ in keep], device=device)
                states.append(H[pos].to(torch.float16).cpu().numpy())
                for j, k in keep:
                    s = sy[k]
                    selfr = sorted(set(s.rules) & SELF_RULES)
                    nxt = sy[k + 1] if k + 1 < len(sy) else None
                    labels.append({"id": r["id"], "metre": r["metre_roman"], "pada": p, "token": enc["input_ids"][j],
                                   "piece": tok.convert_ids_to_tokens(enc["input_ids"][j]), "akshara": k + 1,
                                   "akshara_text": s.text, "weight": s.weight, "rules": list(s.rules),
                                   "subset": "self" if selfr else "context",
                                   "baseline_A": "U" if selfr else "I",
                                   "baseline_B": "U" if (selfr or (nxt is not None and nxt.is_conjunct)) else "I"})
                counts["clean"] += len(keep)
    np.save(out / "states.npy", np.concatenate(states))
    with (out / "labels.jsonl").open("w", encoding="utf-8") as fh:
        for lab in labels:
            fh.write(json.dumps(lab, ensure_ascii=False) + "\n")
    run = {"experiment": "EXP-05", "date": datetime.date.today().isoformat(),
           "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "load": load_report},
           "device": {"torch": torch.__version__, "transformers": transformers.__version__},
           "input": "<bos> + pāda text, one forward pass per pāda, no chat template",
           "sample": {"rule": f"first {PER_METRE} poems per metre of EXP-35's shuffled sample (seed {seed})",
                      "poems": len(chosen), "ids": [r["id"] for r in chosen]},
           "counts": counts, "states": "float16 [tokens, 36, hidden]; L0 = embedding output", "seconds": round(time.time() - t0, 1)}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(counts))


def probe_layer(args):
    import warnings
    import numpy as np
    from sklearn.exceptions import ConvergenceWarning
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    X, y, layer = args
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always", ConvergenceWarning)
        pred = cross_val_predict(LogisticRegression(max_iter=1000), X.astype(np.float32), y,
                                 cv=StratifiedKFold(5, shuffle=True, random_state=0))
    return layer, pred, sum(issubclass(x.category, ConvergenceWarning) for x in w)


def probe(out: Path, jobs: int) -> dict:
    import numpy as np
    import sklearn
    from multiprocessing import Pool

    S = np.load(out / "states.npy", mmap_mode="r")
    labels = [json.loads(line) for line in (out / "labels.jsonl").open(encoding="utf-8")]
    y = np.array([lab["weight"] == "U" for lab in labels], dtype=int)
    subset = np.array([lab["subset"] for lab in labels])
    A = np.array([lab["baseline_A"] == "U" for lab in labels], dtype=int)
    B = np.array([lab["baseline_B"] == "U" for lab in labels], dtype=int)
    L = S.shape[1]
    with Pool(jobs) as pool:
        res = pool.map(probe_layer, [(np.asarray(S[:, l, :]), y, l) for l in range(L)])
    res.sort()
    acc = lambda p, m=slice(None): round(float((p[m] == y[m]).mean()), 4)    # noqa: E731
    masks = {"all": np.ones(len(y), bool), "self": subset == "self", "context": subset == "context"}
    layers = [{"layer": l, "all": acc(p), "self": acc(p, masks["self"]), "context": acc(p, masks["context"]),
               "convergence_warnings": int(cw)} for l, p, cw in res]
    peak = max(layers, key=lambda r: r["all"])
    ctx_peak = max(layers, key=lambda r: r["context"])
    summary = {
        "tokens": int(len(y)), "subset_sizes": {k: int(m.sum()) for k, m in masks.items()},
        "guru_share": {k: round(float(y[m].mean()), 4) for k, m in masks.items()},
        "majority_class_rate": {k: round(float(max(y[m].mean(), 1 - y[m].mean())), 4) for k, m in masks.items()},
        "baseline_A_lookup": {k: acc(A, m) for k, m in masks.items()},
        "baseline_B_next_akshara": {k: acc(B, m) for k, m in masks.items()},
        "peak_layer_all": peak, "peak_layer_context": ctx_peak,
        "layers_beating_baseline_A_on_context": [r["layer"] for r in layers if r["context"] > acc(A, masks["context"])],
        "by_layer": layers, "sklearn": sklearn.__version__,
        "pipeline": {"L0": 0.796, "L7": 0.667, "L10": 0.644, "L27": 0.735, "tokens": 6696, "note": "no <bos>, first 300 pādas"},
    }
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", choices=("extract", "probe"))
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    if args.mode == "extract":
        extract(args.out_dir, args.seed, args.device)
    else:
        s = probe(args.out_dir, args.jobs)
        print(json.dumps({k: v for k, v in s.items() if k != "by_layer"}, ensure_ascii=False, indent=1))
        for r in s["by_layer"]:
            print(r)


if __name__ == "__main__":
    main()
