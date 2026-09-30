#!/usr/bin/env python3
"""
EXP-22: chandas directions by difference in means — the coarse (poem vs bhavam) contrast and all 28
chandas-vs-chandas pairs, with `<bos>`.

Spec: experiments/EXP-22-chandas-direction-extraction-diff-in-means-caa.md (steps 1, 2, 3 and 4; the
tight contrast is EXP-38). Poems, bhavams, sample and model loading are EXP-35's
(experiments/scripts/exp35_surprisal.py).

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp22_directions.py extract OUT_DIR   # GPU
    diffusion_pretraining/.venv/bin/python experiments/scripts/exp22_directions.py analyse OUT_DIR   # CPU
    python3 experiments/scripts/exp22_directions.py plot OUT_DIR                                     # matplotlib

extract: one forward pass per text (`<bos>` + text, no chat template) through the text model with
output_hidden_states; the last token's state at every one of the 36 hidden-state indices is kept
(L0 = embedding output, L1-L35 = decoder-layer outputs; transformers returns the final-norm output as
the last entry). Writes pooled_poem.npy and pooled_bhavam.npy ([200, 36, hidden] float32), meta.json
and run.json. These arrays are also the input of the EXP-07 and EXP-24 reruns.

analyse:
- per-poem diff  D_i = h(poem_i) - h(bhavam_i); per-metre vector d_c = mean over the metre's poems.
- coherence of a set of vectors = their mean pairwise cosine, per layer.
- coarse: coherence of the 200 D_i; direction = mean D_i.
- pair (a, b): direction d_a - d_b. Coherence (the spec's fallback definition; the pipeline's
  phase4_direction.py is not available here): match a's 25 poems to b's with a seeded random
  permutation, c_k = D_{a,k} - D_{b,pi(k)}, coherence of the 25 c_k. The primary value uses matching 0;
  20 matchings give its stability.
- null: the 50 poems of a pair split at random into two groups of 25 (same computation); its peak over
  layers, over 20 splits per pair, gives the chance level of a peak.
- a pair is flagged unfit for steering when its peak coherence is below THRESHOLD, fixed before this
  run at the coarse contrast's pipeline value 0.322 (the spec's example).
Writes summary.json, coherence_by_layer.csv, directions.npz.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import itertools
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

THRESHOLD = 0.322          # fixed in advance: the pipeline's coarse peak (EXP-22 "Observed")
MATCHINGS = 20
NULL_SPLITS = 20
MID_LATE = range(8, 36)    # "mid-to-late layers" for the kandamu/mattakokila check


# ------------------------------------------------------------------ extract (GPU)
def extract(out: Path, seed: int, device: str, bos: bool = True) -> None:
    import numpy as np
    import torch
    import transformers
    from transformers import AutoTokenizer
    import exp35_surprisal as e35

    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, eligible, metres = e35.balanced_sample(seed)
    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    model, cfg = e35.build_model(snap, device, seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)
    arrays = {"poem": [], "bhavam": []}
    ntok = {"poem": [], "bhavam": []}
    checks = {}
    with torch.no_grad():
        for n, r in enumerate(sample):
            for kind, text in (("poem", e35.poem_text(r)), ("bhavam", e35.bhavam_text(r))):
                ids = ([tok.bos_token_id] if bos else []) + tok(text, add_special_tokens=False)["input_ids"]
                x = torch.tensor([ids])
                emb = model.model.embed_tokens(x.to(device))
                pli = ple(x).reshape(1, len(ids), cfg.num_hidden_layers, cfg.hidden_size_per_layer_input).to(device)
                o = model.model(inputs_embeds=emb, per_layer_inputs=pli, use_cache=False, output_hidden_states=True)
                hs = o.hidden_states
                if not checks:
                    checks = {"hidden_states": len(hs),
                              "L0_equals_inputs_embeds": bool(torch.equal(hs[0], emb)),
                              "last_equals_final_norm_output": bool(torch.equal(hs[-1], o.last_hidden_state))}
                arrays[kind].append(torch.stack([h[0, -1] for h in hs]).float().cpu().numpy())
                ntok[kind].append(len(ids) - int(bos))
            if n % 50 == 0:
                print(f"  {n}/{len(sample)}", flush=True)
    for kind in arrays:
        np.save(out / f"pooled_{kind}.npy", np.stack(arrays[kind]))
    meta = {"ids": [r["id"] for r in sample], "metres": [r["metre_roman"] for r in sample],
            "tokens": ntok, "layers": checks["hidden_states"], "hidden_size": cfg.hidden_size}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False), encoding="utf-8")
    run = {"experiment": "EXP-22 (pooled states also used by EXP-07 and EXP-24)", "date": datetime.date.today().isoformat(),
           "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "load": load_report},
           "device": {"name": torch.cuda.get_device_name(0) if device.startswith("cuda") else "cpu",
                      "torch": torch.__version__, "transformers": transformers.__version__},
           "input": ("<bos> + text" if bos else "text only, NO <bos> (diagnostic: the pipeline's presumed setup)")
                    + ", no chat template; poem = scanner lines joined with newlines; bhavam = NFC, first 2,000 chars",
           "pooling": "last token (batch of one, no padding), every hidden-state index", "checks": checks,
           "seed": seed, "sample": {"rule": "EXP-35 Inputs 1", "eligible_per_metre": eligible, "metres": metres},
           "seconds": round(time.time() - t0, 1)}
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(checks))


# ------------------------------------------------------------------ analyse (CPU)
def coherence(v):
    """Mean pairwise cosine of the rows of v, per layer. v: [n, layers, dim] -> [layers].

    A zero vector has no direction, so it is left out of that layer (this happens at L0, where the
    pooled state is the embedding of the final token and many texts end in the same token)."""
    import numpy as np
    norm = np.linalg.norm(v, axis=-1, keepdims=True)
    ok = norm[..., 0] > 1e-9
    u = np.where(ok[..., None], v / np.where(norm > 0, norm, 1.0), 0.0)
    s = u.sum(axis=0)
    n = ok.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        c = ((s * s).sum(axis=-1) - n) / (n * (n - 1))
    return np.where(n >= 2, c, np.nan)


def zero_rows(v):
    """Rows with no direction, per layer."""
    import numpy as np
    return (np.linalg.norm(v, axis=-1) <= 1e-9).sum(axis=0)


def pair_coherence(da, db, key: str):
    import numpy as np
    perm = list(range(len(db)))
    random.Random(key).shuffle(perm)
    return coherence(da - db[np.array(perm)])


def analyse(out: Path, seed: int) -> dict:
    import numpy as np

    P = np.load(out / "pooled_poem.npy").astype(np.float64)
    B = np.load(out / "pooled_bhavam.npy").astype(np.float64)
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    metres = sorted(set(meta["metres"]))
    idx = {m: np.array([i for i, x in enumerate(meta["metres"]) if x == m]) for m in metres}
    D = P - B
    L = D.shape[1]

    coarse = coherence(D)
    coarse_dir = D.mean(axis=0)
    per_metre = np.stack([D[idx[m]].mean(axis=0) for m in metres])

    pairs, curves, null_peaks = {}, {}, []
    pair_dirs = []
    for a, b in itertools.combinations(metres, 2):
        Da, Db = D[idx[a]], D[idx[b]]
        c0 = pair_coherence(Da, Db, f"exp22:{seed}:{a}|{b}:0")
        peaks = [float(np.nanmax(pair_coherence(Da, Db, f"exp22:{seed}:{a}|{b}:{m}"))) for m in range(MATCHINGS)]
        pool = np.concatenate([Da, Db])
        for t in range(NULL_SPLITS):
            order = list(range(len(pool)))
            random.Random(f"exp22-null:{seed}:{a}|{b}:{t}").shuffle(order)
            g1, g2 = pool[np.array(order[:len(Da)])], pool[np.array(order[len(Da):])]
            null_peaks.append(float(np.nanmax(pair_coherence(g1, g2, f"exp22-null-match:{seed}:{a}|{b}:{t}"))))
        d = per_metre[metres.index(a)] - per_metre[metres.index(b)]
        pair_dirs.append(d)
        curves[f"{a}|{b}"] = c0
        pairs[f"{a}|{b}"] = {
            "peak": round(float(np.nanmax(c0)), 4), "peak_layer": int(np.nanargmax(c0)),
            "peak_over_matchings": {"mean": round(float(np.mean(peaks)), 4), "sd": round(float(np.std(peaks)), 4)},
            "direction_norm_at_peak": round(float(np.linalg.norm(d[int(np.nanargmax(c0))])), 3),
            "flagged_unfit": bool(np.nanmax(c0) < THRESHOLD)}
    null95, null99 = float(np.percentile(null_peaks, 95)), float(np.percentile(null_peaks, 99))
    for p in pairs.values():
        p["above_null95"] = p["peak"] > null95
    km = curves.get("kandamu|mattakokila")
    peaks_sorted = sorted(pairs.items(), key=lambda kv: -kv[1]["peak"])
    summary = {
        "n_per_metre": {m: int(len(idx[m])) for m in metres},
        "zero_diff_vectors_by_layer": {f"L{l}": int(z) for l, z in enumerate(zero_rows(D)) if z},
        "coarse": {"n": int(D.shape[0]), "peak": round(float(np.nanmax(coarse)), 4), "peak_layer": int(np.nanargmax(coarse)),
                   "coherence_by_layer": [round(float(x), 4) for x in coarse],
                   "direction_norm_by_layer": [round(float(x), 2) for x in np.linalg.norm(coarse_dir, axis=-1)],
                   "pipeline": {"peak": 0.322, "peak_layer": 4, "n_pairs": 100}},
        "threshold": {"value": THRESHOLD, "source": "pipeline coarse peak, fixed before this run"},
        "null": {"splits": len(null_peaks), "peak_p95": round(null95, 4), "peak_p99": round(null99, 4),
                 "peak_max": round(float(max(null_peaks)), 4)},
        "pairs": dict(peaks_sorted),
        "pairs_flagged_unfit": sum(p["flagged_unfit"] for p in pairs.values()),
        "pairs_above_null95": sum(p["above_null95"] for p in pairs.values()),
        "peak_distribution": {"min": min(p["peak"] for p in pairs.values()), "median": float(np.median([p["peak"] for p in pairs.values()])),
                              "max": max(p["peak"] for p in pairs.values())},
        "peak_layer_counts": {str(k): v for k, v in sorted(
            {l: sum(p["peak_layer"] == l for p in pairs.values()) for l in range(L)}.items()) if v},
        "kandamu_vs_mattakokila": None if km is None else {
            "range_L8_L35": [round(float(np.nanmin(km[list(MID_LATE)])), 4), round(float(np.nanmax(km[list(MID_LATE)])), 4)],
            "peak": round(float(np.nanmax(km)), 4), "peak_layer": int(np.nanargmax(km)),
            "pipeline_range": [0.5, 0.65]},
    }
    with (out / "coherence_by_layer.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["contrast"] + [f"L{l}" for l in range(L)])
        w.writerow(["coarse"] + [f"{x:.4f}" for x in coarse])
        for k, c in curves.items():
            w.writerow([k] + [f"{x:.4f}" for x in c])
    np.savez(out / "directions.npz", metres=np.array(metres), coarse=coarse_dir.astype(np.float32),
             per_metre=per_metre.astype(np.float32), pair_names=np.array(list(curves)),
             pairs=np.stack(pair_dirs).astype(np.float32))
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


# ------------------------------------------------------------------ plot (matplotlib)
def plot(out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    SURFACE, INK, INK2, GRID, AXIS, BLUE = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7", "#2a78d6"
    plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                         "font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                         "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "xtick.color": AXIS, "ytick.color": AXIS, "xtick.labelcolor": INK2, "ytick.labelcolor": INK2})
    rows = list(csv.reader((out / "coherence_by_layer.csv").open(encoding="utf-8")))
    s = json.loads((out / "summary.json").read_text(encoding="utf-8"))
    header, coarse = rows[0], [float(x) for x in rows[1][1:]]
    pairs = sorted(rows[2:], key=lambda r: -max(float(x) for x in r[1:]))
    M = [[float(x) for x in r[1:]] for r in pairs]
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9.5, 9.2), gridspec_kw={"height_ratios": [3.2, 1]})
    cmap = LinearSegmentedColormap.from_list("blues", ["#f3f2ee", "#cde2fb", "#86b6ef", "#2a78d6", "#1c5cab", "#0d3a73"])
    im = ax1.imshow(M, aspect="auto", cmap=cmap, vmin=0, vmax=max(max(r) for r in M))
    ax1.set_yticks(range(len(pairs)), [r[0].replace("|", " vs ") for r in pairs])
    ax1.set_xticks(range(0, len(header) - 1, 5), [f"L{l}" for l in range(0, len(header) - 1, 5)])
    ax1.set_title("Coherence of the 28 chandas-vs-chandas directions by layer (with <bos>)", color=INK)
    fig.colorbar(im, ax=ax1, fraction=0.025, pad=0.01, label="mean pairwise cosine")
    ax2.plot(range(len(coarse)), coarse, color=BLUE, lw=2)
    ax2.axhline(s["threshold"]["value"], color=INK2, lw=1, ls="--")
    ax2.axhline(s["null"]["peak_p95"], color=AXIS, lw=1, ls=":")
    ax2.text(len(coarse) - 0.5, s["threshold"]["value"], " flag threshold 0.322", va="bottom", ha="right", color=INK2, fontsize=8)
    ax2.text(len(coarse) - 0.5, s["null"]["peak_p95"], " null peak, 95th pct", va="bottom", ha="right", color=INK2, fontsize=8)
    ax2.set_xlim(-0.5, len(coarse) - 0.5)
    ax2.set_xticks(range(0, len(coarse), 5), [f"L{l}" for l in range(0, len(coarse), 5)])
    ax2.set_ylabel("coherence")
    ax2.set_title(f"Coarse contrast (poem vs its own bhavam, n = {s['coarse']['n']}): peak {s['coarse']['peak']:.3f} "
                  f"at L{s['coarse']['peak_layer']}", color=INK)
    ax2.grid(axis="y", color=GRID, lw=0.8)
    for sp in ("top", "right"):
        ax2.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(out / "fig_coherence.png", dpi=170)
    print(f"wrote {out / 'fig_coherence.png'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("mode", choices=("extract", "analyse", "plot"))
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--no-bos", action="store_true", help="extract without <bos> (diagnostic)")
    args = ap.parse_args()
    if args.mode == "extract":
        extract(args.out_dir, args.seed, args.device, bos=not args.no_bos)
    elif args.mode == "analyse":
        s = analyse(args.out_dir, args.seed)
        print(json.dumps({k: v for k, v in s.items() if k != "pairs"}, ensure_ascii=False, indent=1)[:3500])
    else:
        plot(args.out_dir)


if __name__ == "__main__":
    main()
