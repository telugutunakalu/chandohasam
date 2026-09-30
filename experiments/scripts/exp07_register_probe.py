#!/usr/bin/env python3
"""
EXP-07: poem-vs-bhavam register probe, rerun with `<bos>` on EXP-22's pooled states.

Spec: experiments/EXP-07-poem-vs-bhavam-register-probe.md. Inputs are the last-token states that
experiments/scripts/exp22_directions.py extracts (200 poems + their bhavams, `<bos>` prepended, 36
hidden-state indices).

    <env with scikit-learn>/bin/python experiments/scripts/exp07_register_probe.py EXP22_DIR OUT_DIR

One logistic-regression probe per layer (scikit-learn, max_iter=1000, default settings), 5-fold
stratified cross-validation (shuffled, random_state=0), mean fold accuracy. Length-only baseline:
the same probe on the token count alone. Writes OUT_DIR/summary.json.
"""
from __future__ import annotations

import argparse
import json
import warnings
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("exp22_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()

    import numpy as np
    import sklearn
    from sklearn.exceptions import ConvergenceWarning
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_score

    P = np.load(args.exp22_dir / "pooled_poem.npy")
    B = np.load(args.exp22_dir / "pooled_bhavam.npy")
    meta = json.loads((args.exp22_dir / "meta.json").read_text(encoding="utf-8"))
    X = np.concatenate([P, B])
    y = np.array([1] * len(P) + [0] * len(B))
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    layers = []
    for l in range(X.shape[1]):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", ConvergenceWarning)
            acc = cross_val_score(LogisticRegression(max_iter=1000), X[:, l, :], y, cv=cv)
        layers.append({"layer": l, "accuracy": round(float(acc.mean()), 4),
                       "convergence_warnings": sum(issubclass(x.category, ConvergenceWarning) for x in w)})
    length = np.array(meta["tokens"]["poem"] + meta["tokens"]["bhavam"], dtype=float).reshape(-1, 1)
    len_acc = cross_val_score(LogisticRegression(max_iter=1000), length, y, cv=cv).mean()
    peak = max(layers, key=lambda r: r["accuracy"])
    first_perfect = next((r["layer"] for r in layers if r["accuracy"] == 1.0), None)
    summary = {"examples_per_layer": int(len(y)), "chance": 0.5, "length_only_baseline": round(float(len_acc), 4),
               "peak": peak, "first_layer_at_1.0": first_perfect, "by_layer": layers, "sklearn": sklearn.__version__,
               "input": f"{args.exp22_dir} (last-token states, <bos> prepended)",
               "pipeline": {"peak_layer": 7, "accuracy": 1.0, "note": "no <bos>"}}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_layer"}, indent=1))
    print([r["accuracy"] for r in layers])


if __name__ == "__main__":
    main()
