#!/usr/bin/env python3
"""
EXP-08: teacher-forced NLL of genuine metrical word order against a random shuffle of the same words.

Spec: experiments/EXP-08-metrical-order-nll-contrast-against-shuffle-and-pros.md. This run covers the
genuine and random-shuffle conditions (steps 1-4); the natural-prose reordering is not run. Poems,
inputs and scorer are EXP-35's (experiments/scripts/exp35_surprisal.py): the same 200-poem balanced
sample, the scanner's NFC lines joined with newlines, gemma-4-E2B-it in bf16, `<bos>` prepended.

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp08_order_contrast.py OUT_DIR   # score + statistics
    python3 experiments/scripts/exp08_order_contrast.py --plot OUT_DIR                           # figure (needs matplotlib)

Shuffle: the poem's own words (whitespace-separated, punctuation attached) are permuted with a
per-poem seed (`random.Random(f"exp08:{seed}:{id}")`) and put back into the poem's lines, so each
line keeps its word count and the newlines stay where they were; only the order of the words changes.
The word multiset is checked to be unchanged.

Conditions: `bos` (primary, EXP-35's input) and `nobos` (diagnostic: the presumed setup of the
pipeline run whose numbers the spec reports). NLL is the mean surprisal per scored token.

Writes OUT_DIR/run.json, traces.jsonl (one row per poem x order x condition, with EXP-35's per-token
fields), per_poem.csv and summary.json; `--plot` adds fig_shared_difficulty.png.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exp35_surprisal as e35        # noqa: E402

ORDERS = ("genuine", "shuffle")
CONDITIONS = ("bos", "nobos")
BOOTSTRAP = 10_000
PIPELINE = {"poems": 200, "delta_mean": 0.571, "shuffle_preferred": 144, "pearson": 0.556, "spearman": 0.503}   # EXP-08 "Observed"


def shuffle_text(text: str, key: str) -> str:
    lines = text.split("\n")
    sizes = [len(ln.split()) for ln in lines]
    words = [w for ln in lines for w in ln.split()]
    rng = random.Random(key)
    perm = words[:]
    for _ in range(100):                       # a permutation that actually changes the order
        rng.shuffle(perm)
        if perm != words:
            break
    assert Counter(perm) == Counter(words)
    out, i = [], 0
    for n in sizes:
        out.append(" ".join(perm[i:i + n]))
        i += n
    return "\n".join(out)


# ------------------------------------------------------------------ scoring
def run_scoring(out: Path, seed: int, device: str) -> None:
    import torch
    import transformers
    from transformers import AutoTokenizer

    out.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    sample, eligible, metres = e35.balanced_sample(seed)
    snap = e35.snapshot_dir()
    tok = AutoTokenizer.from_pretrained(snap)
    bos = tok.bos_token_id
    texts = {}
    irregular = 0
    for r in sample:
        g = e35.poem_text(r)
        irregular += any(" ".join(ln.split()) != ln for ln in g.split("\n"))
        texts[(r["id"], "genuine")] = g
        texts[(r["id"], "shuffle")] = shuffle_text(g, f"exp08:{seed}:{r['id']}")
    metre_of = {r["id"]: r["metre_roman"] for r in sample}

    traces = out / "traces.jsonl"
    done = {json.loads(line)["key"] for line in traces.open(encoding="utf-8")} if traces.exists() else set()
    model, cfg = e35.build_model(snap, device, seed)
    ple_weight, load_report = e35.load_trained(model, snap)
    ple = e35.ple_module(cfg, weight=ple_weight)
    with traces.open("a", encoding="utf-8") as fh:
        for cond in CONDITIONS:
            prefix = [bos] if cond == "bos" else []
            for n, ((rid, order), text) in enumerate(texts.items()):
                key = f"{rid}|{order}|{cond}"
                if key in done:
                    continue
                enc = tok(text, add_special_tokens=False, return_offsets_mapping=True)
                ids = enc["input_ids"]
                res = e35.score(model, ple, cfg, ids, prefix, device)
                row = {"key": key, "id": rid, "metre": metre_of[rid], "order": order, "condition": cond, "text": text,
                       "prefix_len": len(prefix), "tokens": ids, "pieces": tok.convert_ids_to_tokens(ids),
                       "offsets": [list(o) for o in enc["offset_mapping"]], **res}
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                done.add(key)
                if n % 100 == 0:
                    print(f"  {cond} {n}/{len(texts)}", flush=True)
    run = {
        "experiment": "EXP-08", "stage": "genuine vs random shuffle, 200 poems (prose control not run)",
        "date": datetime.date.today().isoformat(),
        "model": {"id": e35.MODEL_ID, "snapshot": snap.name, "dtype": "bfloat16", "load": load_report,
                  "placement": "PLE table in CPU RAM, passed as per_layer_inputs (see exp35_surprisal.py)"},
        "device": {"name": torch.cuda.get_device_name(0) if device.startswith("cuda") else "cpu",
                   "torch": torch.__version__, "transformers": transformers.__version__},
        "seed": seed, "conditions": list(CONDITIONS), "orders": list(ORDERS),
        "sample": {"rule": "EXP-35 Inputs 1 (same sample and seed)", "eligible_per_metre": eligible, "metres": metres,
                   "ids": [r["id"] for r in sample],
                   "poems_with_irregular_spacing": irregular},
        "shuffle": "per-poem random.Random(f'exp08:{seed}:{id}'); words permuted across the poem, "
                   "line word counts and newlines kept; word multiset checked",
        "nll": "mean surprisal per scored token (EXP-35 s_true)",
        "seconds": round(time.time() - t0, 1),
    }
    (out / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ statistics
def summarise(out: Path) -> dict:
    import numpy as np
    from scipy import stats

    rows = [json.loads(line) for line in (out / "traces.jsonl").open(encoding="utf-8")]
    nll = {}
    for r in rows:
        st = [v for v in r["s_true"] if v is not None]
        nll[(r["id"], r["order"], r["condition"])] = (mean(st), sum(st), len(st))
    ids = sorted({r["id"] for r in rows})
    metre_of = {r["id"]: r["metre"] for r in rows}

    per_poem, result = [], {}
    for cond in CONDITIONS:
        g = np.array([nll[(i, "genuine", cond)][0] for i in ids])
        s = np.array([nll[(i, "shuffle", cond)][0] for i in ids])
        gt = np.array([nll[(i, "genuine", cond)][1] for i in ids])
        stt = np.array([nll[(i, "shuffle", cond)][1] for i in ids])
        ntok = np.array([nll[(i, "genuine", cond)][2] - nll[(i, "shuffle", cond)][2] for i in ids])
        d = g - s
        rng = np.random.default_rng(0)
        boot = rng.choice(d, size=(BOOTSTRAP, len(d))).mean(axis=1)
        pear, spear, wil = stats.pearsonr(g, s), stats.spearmanr(g, s), stats.wilcoxon(d)
        by_metre = defaultdict(list)
        for i, di in zip(ids, d):
            by_metre[metre_of[i]].append(di)
        result[cond] = {
            "poems": len(ids),
            "nll_genuine_mean": round(float(g.mean()), 4), "nll_shuffle_mean": round(float(s.mean()), 4),
            "delta_mean": round(float(d.mean()), 4), "delta_median": round(float(np.median(d)), 4),
            "delta_mean_ci95": [round(float(np.percentile(boot, 2.5)), 4), round(float(np.percentile(boot, 97.5)), 4)],
            "wilcoxon_p": float(wil.pvalue),
            "shuffle_preferred": int((d > 0).sum()), "genuine_preferred": int((d < 0).sum()), "ties": int((d == 0).sum()),
            "delta_total_nll_mean": round(float((gt - stt).mean()), 3),
            "total_nll_shuffle_preferred": int((gt > stt).sum()),
            "token_count_difference": {"mean": round(float(ntok.mean()), 3), "min": int(ntok.min()), "max": int(ntok.max())},
            "pearson": {"r": round(float(pear.statistic), 4), "p": float(pear.pvalue)},
            "spearman": {"rho": round(float(spear.statistic), 4), "p": float(spear.pvalue)},
            "by_metre": {m: {"poems": len(v), "delta_mean": round(float(np.mean(v)), 4),
                             "shuffle_preferred": int(sum(x > 0 for x in v))} for m, v in sorted(by_metre.items())},
        }
        for i, gi, si in zip(ids, g, s):
            per_poem.append({"id": i, "metre": metre_of[i], "condition": cond, "nll_genuine": round(float(gi), 5),
                             "nll_shuffle": round(float(si), 5), "delta": round(float(gi - si), 5),
                             "preferred": "shuffle" if si < gi else "genuine"})

    cross = {}
    e35_traces = out.parent.parent / "exp35" / "2026-09-29_gates" / "traces.jsonl"
    if e35_traces.exists():
        diffs = []
        for line in e35_traces.open(encoding="utf-8"):
            r = json.loads(line)
            if r["kind"] == "poem" and r["condition"] in CONDITIONS and (r["id"], "genuine", r["condition"]) in nll:
                st = [v for v in r["s_true"] if v is not None]
                diffs.append(abs(mean(st) - nll[(r["id"], "genuine", r["condition"])][0]))
        cross = {"poems_compared": len(diffs), "max_abs_difference": max(diffs) if diffs else None,
                 "note": "EXP-35 gate 6: per-poem mean s_true of the EXP-35 gates run vs this run's NLL(genuine)"}

    with (out / "per_poem.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(per_poem[0]))
        w.writeheader()
        w.writerows(per_poem)
    summary = {"conditions": result, "exp35_gate6_cross_check": cross,
               "pipeline_2026_09_24": dict(PIPELINE, note="EXP-08 'Observed' (suspect input, presumed no <bos>)")}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


# ------------------------------------------------------------------ figure
def plot(out: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    SURFACE, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
    BLUE, ORANGE = "#2a78d6", "#eb6834"
    plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                         "font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                         "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "axes.spines.top": False, "axes.spines.right": False, "xtick.color": AXIS, "ytick.color": AXIS,
                         "xtick.labelcolor": INK2, "ytick.labelcolor": INK2, "legend.frameon": False})
    rows = list(csv.DictReader((out / "per_poem.csv").open(encoding="utf-8")))
    summary = json.loads((out / "summary.json").read_text(encoding="utf-8"))["conditions"]
    titles = {"bos": "With <bos> (primary)", "nobos": "Without <bos> (the pipeline's setup)"}
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.9))
    for ax, cond in zip(axes, CONDITIONS):
        rs = sorted((r for r in rows if r["condition"] == cond), key=lambda r: float(r["nll_genuine"]))
        x = range(len(rs))
        ax.plot(x, [float(r["nll_genuine"]) for r in rs], color=INK2, lw=2, zorder=2)
        for pref, color in (("genuine", BLUE), ("shuffle", ORANGE)):
            pts = [(i, float(r["nll_shuffle"])) for i, r in enumerate(rs) if r["preferred"] == pref]
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=22, color=color, edgecolor=SURFACE, linewidth=1, zorder=3)
        s = summary[cond]
        ax.set_title(f"{titles[cond]}\nshuffle preferred in {s['shuffle_preferred']}/{s['poems']} poems; "
                     f"Pearson r = {s['pearson']['r']:.2f}", color=INK)
        ax.set_xlabel("poems, sorted by NLL of the genuine order")
        ax.set_ylabel("NLL (nats per token)")
        ax.grid(axis="y", color=GRID, lw=0.8)
        ax.set_axisbelow(True)
    handles = [Line2D([], [], color=INK2, lw=2, label="genuine order (sorted)"),
               Line2D([], [], ls="", marker="o", ms=6, color=BLUE, label="shuffle, genuine preferred"),
               Line2D([], [], ls="", marker="o", ms=6, color=ORANGE, label="shuffle preferred")]
    fig.legend(handles=handles, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.02))
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    fig.savefig(out / "fig_shared_difficulty.png", dpi=180)
    print(f"wrote {out / 'fig_shared_difficulty.png'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--plot", action="store_true", help="only draw the figure from per_poem.csv and summary.json")
    args = ap.parse_args()
    if args.plot:
        plot(args.out_dir)
        return
    run_scoring(args.out_dir, args.seed, args.device)
    s = summarise(args.out_dir)
    print(json.dumps(s, ensure_ascii=False, indent=1)[:4000])


if __name__ == "__main__":
    main()
