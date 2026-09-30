#!/usr/bin/env python3
"""
EXP-24: representational similarity of per-metre directions against symbolic gaṇa distance, rerun
with `<bos>` on EXP-22's pooled states.

Spec: experiments/EXP-24-representational-similarity-vs-symbolic-gana-distanc.md.

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp24_rsa.py EXP22_DIR OUT_DIR

- d_c per metre and layer: mean over the metre's 25 poems of h(poem) - h(bhavam) (last-token states).
- D_act per layer: 1 - cos(d_i, d_j), raw and centred (d_c - mean_c d_c).
- D_struct: Levenshtein distance between the metres' canonical guru/laghu strings. The canonical
  string is the plurality-mode whole-poem pattern (the four pādas' U/I strings, concatenated) over
  every eligible corpus poem of the metre, scanned with the canonical reading. Sensitivity variant:
  the concatenation of the plurality-mode pattern of each pāda position separately.
- statistic: Spearman r between the 28 upper-triangle entries; one-sided Mantel test with 999
  permutations of the metre labels, p = (#{r_perm >= r} + 1) / 1000.
Writes OUT_DIR/summary.json.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
PERMS = 999


def levenshtein(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def canonical_patterns(metres):
    from indic_meter_dawg.scansion import scan
    records = json.loads((ROOT / "dataset" / "bhagavatam.json").read_text(encoding="utf-8"))
    whole, per_pada, n = defaultdict(Counter), defaultdict(lambda: defaultdict(Counter)), Counter()
    for r in records:
        m = r["metre_roman"]
        if m not in metres or r["form"] != "verse" or not r["verse"]:
            continue
        pats = [s.pattern for s in scan(r["verse"])]
        if len(pats) != 4:
            continue
        n[m] += 1
        whole[m]["".join(pats)] += 1
        for k, p in enumerate(pats):
            per_pada[m][k][p] += 1
    out = {}
    for m in metres:
        (w, wc), = whole[m].most_common(1)
        out[m] = {"poems_scanned": n[m], "mode_whole": w, "mode_whole_share": round(wc / n[m], 4),
                  "mode_per_pada": "".join(per_pada[m][k].most_common(1)[0][0] for k in range(4))}
    return out


def rsa(d, ds, rng):
    """Spearman r between upper triangles of D_act (from vectors d: [8, dim]) and D_struct, with Mantel p."""
    import numpy as np
    from scipy.stats import spearmanr
    u = d / np.linalg.norm(d, axis=-1, keepdims=True)
    da = 1 - u @ u.T
    iu = np.triu_indices(len(d), 1)
    r = spearmanr(da[iu], ds[iu]).statistic
    k = 0
    for _ in range(PERMS):
        p = rng.permutation(len(d))
        k += int(spearmanr(da[p][:, p][iu], ds[iu]).statistic >= r)
    return float(r), float((k + 1) / (PERMS + 1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("exp22_dir", type=Path)
    ap.add_argument("out_dir", type=Path)
    args = ap.parse_args()
    import numpy as np

    P = np.load(args.exp22_dir / "pooled_poem.npy").astype(np.float64)
    B = np.load(args.exp22_dir / "pooled_bhavam.npy").astype(np.float64)
    meta = json.loads((args.exp22_dir / "meta.json").read_text(encoding="utf-8"))
    metres = sorted(set(meta["metres"]))
    lab = np.array(meta["metres"])
    d = np.stack([(P[lab == m] - B[lab == m]).mean(axis=0) for m in metres])       # [8, 36, dim]
    canon = canonical_patterns(metres)
    result = {"metres": metres, "canonical": canon, "variants": {}}
    for variant, key in (("mode_whole", "mode_whole"), ("mode_per_pada", "mode_per_pada")):
        ds = np.array([[levenshtein(canon[a][key], canon[b][key]) for b in metres] for a in metres], dtype=float)
        rows = []
        for l in range(d.shape[1]):
            rng = np.random.default_rng(l)
            r_raw, p_raw = rsa(d[:, l], ds, rng)
            dc = d[:, l] - d[:, l].mean(axis=0)
            r_c, p_c = rsa(dc, ds, rng)
            rows.append({"layer": l, "r_raw": round(r_raw, 3), "p_raw": p_raw, "r_centred": round(r_c, 3), "p_centred": p_c})
        result["variants"][variant] = {
            "D_struct": ds.astype(int).tolist(),
            "significant_layers_raw": int(sum(r["p_raw"] < 0.05 for r in rows)),
            "significant_layers_centred": int(sum(r["p_centred"] < 0.05 for r in rows)),
            "peak_raw": max(rows, key=lambda r: r["r_raw"]), "peak_centred": max(rows, key=lambda r: r["r_centred"]),
            "by_layer": rows}
    result["pipeline"] = {"significant_layers_raw": 26, "peak_raw": {"layer": 8, "r": 0.617, "p": 0.005},
                          "peak_centred": {"layer": 8, "r": 0.702, "p": 0.004}, "L0": {"r": -0.071, "p": 0.733},
                          "L33": {"r_raw": 0.5, "r_centred": 0.123}, "note": "no <bos>"}
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in result["canonical"].items()}, indent=1))
    for v, s in result["variants"].items():
        print(v, "sig raw", s["significant_layers_raw"], "sig centred", s["significant_layers_centred"],
              "peak raw", s["peak_raw"], "peak centred", s["peak_centred"])
        for l in (0, 7, 8, 9, 15, 33):
            print("   ", s["by_layer"][l])


if __name__ == "__main__":
    main()
