#!/usr/bin/env python3
"""
EXP-35 analysis: akshara grid, token -> metrical-grid alignment, aggregations and the hypothesis tests.

Spec: experiments/EXP-35-teacher-forced-surprisal-gap-corpus-token-vs-top-choice.md ("Per poem, record
the akshara grid", "Alignment rules", "Aggregations", "Tests"). Reads the traces of
experiments/scripts/exp35_surprisal.py; every test uses the `bos` condition.

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp35_tests.py RUN_DIR [--exp08 DIR]   # analysis
    python3 experiments/scripts/exp35_tests.py --plot RUN_DIR                                        # figures

Akshara grid (poems): the scanner's syllables give each akshara's character span, pāda, 1-based index,
weight and word; chandohasam.analyze(lines, profile="relaxed") gives the identified metre, `matched`,
the yati seats (YatiSeat.positions[1:], the vaḷi excluded) and whether prāsa applies (seat = akshara 2).
When the engine identifies no metre, the prāsa seat follows the corpus label (every sampled metre except
aataveladi and tetagiti has prāsa) and there are no yati seats.

Tests (unit = the text; Wilcoxon signed-rank, bootstrap 95% CI over 10,000 resamples of texts):
  NH26   d_i = mean gap(pāda-first tokens) - mean gap(other word-initial text tokens), > 0;
         prose control: the same on the bhavam with sentence-first tokens, delta_i = d_i(poem) - d_i(bhavam) > 0.
  NH21   mean gap over matched token indices j < min(T_poem, T_bhavam): poem > bhavam (paired);
         also without the pairs whose bhavam shares a 3-word n-gram with its poem.
  NH27a  prāsa metres: did_i = [mean_{p>=2} S(p,2) - S(1,2)] - [mean_{p>=2} S(p,3) - S(1,3)] < 0,
         S = akshara-level s_true; placebo: the same on aataveladi and tetagiti (about 0).
  NH27b  mean S at word-initial yati-seat aksharas - mean S at other word-initial, non-pāda-first aksharas < 0.
NH26 and NH27 are also reported without the lowest decile of poems by mean s_true (memorisation check).
NH18 needs EXP-19's free-running traces and is not computed here.

Writes to RUN_DIR: akshara_grid.jsonl, tests.json, fig6_positionwise.csv, fig6b_poemlevel.csv,
fig6c_pada_profile.csv; --plot adds fig6_*.png.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import unicodedata
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))

NO_PRASA = {"aataveladi", "tetagiti"}
BOOT = 10_000
SENT_END = set(".?!।")


# ------------------------------------------------------------------ akshara grid
def grid_for(item):
    rid, metre, text = item
    from indic_meter_dawg.scansion import scan
    from chandohasam import analyze

    lines = text.split("\n")
    scans = scan(lines)
    assert [s.text for s in scans] == lines, rid
    a = analyze(lines, profile="relaxed")
    unit = a.units[0] if a.units else None
    lines_ok = unit is not None and len(unit.lines) == len(lines) and all(
        len(lr.aksharas) == len(sc.syllables) for lr, sc in zip(unit.lines, scans))
    if unit is not None and unit.prasa is not None:
        prasa_applies, prasa_source = bool(unit.prasa.applicable), "engine"
    else:
        prasa_applies, prasa_source = metre not in NO_PRASA, "corpus label"
    aks, off = [], 0
    for p, sc in enumerate(scans, start=1):
        yati = set()
        if lines_ok:
            for seat in unit.lines[p - 1].yati:
                yati.update(seat.positions[1:])
        n = len(sc.syllables)
        prev_word = None
        for i, syl in enumerate(sc.syllables, start=1):
            aks.append([off + syl.start, off + syl.end, p, i, n, syl.weight, syl.word,
                        i in yati, prasa_applies and i == 2, syl.word != prev_word])
            prev_word = syl.word
        off += len(sc.text) + 1
    return rid, {"engine_meter": a.meter, "matched": a.matched, "grid_from_engine": lines_ok,
                 "prasa_source": prasa_source,
                 "aksharas": aks}   # [start, end, pada, idx, n, weight, word, yati, prasa, word_initial]


# ------------------------------------------------------------------ alignment
def norm_metre(name: str) -> str:
    """Corpus labels and catalogue names spell some metres differently (aataveladi / ataveladi)."""
    return name.replace("aataveladi", "ataveladi").replace("shardula", "sardula")


def is_letter(ch: str) -> bool:
    return unicodedata.category(ch)[0] in "LM"


def align(row, grid=None):
    """Per scored token: kind, flags and anchor akshara (poems) following the spec's alignment rules."""
    text, offs = row["text"], row["offsets"]
    char2ak = [-1] * len(text)
    if grid is not None:
        for k, a in enumerate(grid["aksharas"]):
            for c in range(a[0], a[1]):
                char2ak[c] = k
    toks, prev_span, seen_pada = [], None, set()
    first_word_initial_done = False
    after_sentence_end = True
    for j, (s, e) in enumerate(offs):
        span = (s, e)
        anchor = next((c for c in range(s, e) if not text[c].isspace()), None)
        t = {"j": j, "kind": None, "word_initial": False, "pada_first": False, "sentence_first": False,
             "mid_akshara": False, "ak": -1, "anchor": anchor}
        if span == prev_span and s < e:
            t["kind"] = "byte_cont"
        elif anchor is None:
            t["kind"] = "newline" if "\n" in text[s:e] else "space"
        else:
            t["word_initial"] = anchor == 0 or text[anchor - 1].isspace()
            if grid is not None:
                k = char2ak[anchor]
                t["kind"] = "text" if k >= 0 else "punct"
                if k >= 0:
                    a = grid["aksharas"][k]
                    t["ak"], t["mid_akshara"] = k, anchor > a[0]
                    if a[2] not in seen_pada:
                        seen_pada.add(a[2])
                        t["pada_first"] = True
            else:
                t["kind"] = "text" if is_letter(text[anchor]) else "punct"
                if t["kind"] == "text" and t["word_initial"] and (not first_word_initial_done or after_sentence_end):
                    t["sentence_first"] = True
                    first_word_initial_done = True
                    after_sentence_end = False
                if any(ch in SENT_END for ch in text[s:e]):
                    after_sentence_end = True
        prev_span = span
        toks.append(t)
    return toks


def akshara_values(row, grid, field):
    """Spread each scored token's value uniformly over its non-space characters; sum per akshara."""
    text = row["text"]
    char_val = [0.0] * len(text)
    for (s, e), v in zip(row["offsets"], row[field]):
        if v is None:
            continue
        chars = [c for c in range(s, e) if not text[c].isspace()]
        for c in chars:
            char_val[c] += v / len(chars)
    return [sum(char_val[a[0]:a[1]]) for a in grid["aksharas"]]


# ------------------------------------------------------------------ statistics
def test(values, alternative):
    import numpy as np
    from scipy import stats
    v = np.array([x for x in values if x is not None and x == x], dtype=float)
    if len(v) < 5:
        return {"n": int(len(v)), "note": "too few texts"}
    rng = np.random.default_rng(0)
    boot = rng.choice(v, size=(BOOT, len(v))).mean(axis=1)
    w = stats.wilcoxon(v, alternative=alternative)
    return {"n": int(len(v)), "mean": round(float(v.mean()), 4), "median": round(float(np.median(v)), 4),
            "ci95": [round(float(np.percentile(boot, 2.5)), 4), round(float(np.percentile(boot, 97.5)), 4)],
            "share_in_predicted_direction": round(float((v > 0).mean() if alternative == "greater" else (v < 0).mean()), 4),
            "wilcoxon_p_one_sided": float(w.pvalue), "alternative": alternative}


def ngrams(text, n=3):
    """Word n-grams, with punctuation stripped from each word."""
    words = [w for w in ("".join(ch for ch in tok if is_letter(ch)) for tok in re.findall(r"\S+", text)) if w]
    return {tuple(words[i:i + n]) for i in range(len(words) - n + 1)}


def analyse(run: Path, exp08: Path | None) -> dict:
    import numpy as np
    from scipy import stats

    rows = [json.loads(line) for line in (run / "traces.jsonl").open(encoding="utf-8")]
    bos = {(r["id"], r["kind"]): r for r in rows if r["condition"] == "bos"}
    ids = sorted({i for i, k in bos if k == "poem"})
    metre = {r["id"]: r["metre"] for r in rows}

    items = [(i, metre[i], bos[(i, "poem")]["text"]) for i in ids]
    with Pool(8) as pool:
        grids = dict(pool.map(grid_for, items))
    with (run / "akshara_grid.jsonl").open("w", encoding="utf-8") as fh:
        for i in ids:
            fh.write(json.dumps({"id": i, "metre": metre[i], **grids[i]}, ensure_ascii=False) + "\n")

    per_poem = {}
    for i in ids:
        pr, br, g = bos[(i, "poem")], bos[(i, "bhavam")], grids[i]
        gap_p = [None if a is None else a - b for a, b in zip(pr["s_true"], pr["s_model"])]
        gap_b = [None if a is None else a - b for a, b in zip(br["s_true"], br["s_model"])]
        tp, tb = align(pr, g), align(br)
        pf = [gap_p[t["j"]] for t in tp if t["kind"] == "text" and t["pada_first"]]
        ow = [gap_p[t["j"]] for t in tp if t["kind"] == "text" and t["word_initial"] and not t["pada_first"]]
        sf = [gap_b[t["j"]] for t in tb if t["kind"] == "text" and t["sentence_first"]]
        ob = [gap_b[t["j"]] for t in tb if t["kind"] == "text" and t["word_initial"] and not t["sentence_first"]]
        d_poem = mean(pf) - mean(ow) if pf and ow else None
        pf1 = [gap_p[t["j"]] for t in tp if t["kind"] == "text" and t["pada_first"] and t["j"] > 0]
        sf1 = [gap_b[t["j"]] for t in tb if t["kind"] == "text" and t["sentence_first"] and t["j"] > 0]
        d_poem_1 = mean(pf1) - mean(ow) if pf1 and ow else None
        d_bhav_1 = mean(sf1) - mean(ob) if sf1 and ob else None
        d_bhav = mean(sf) - mean(ob) if sf and ob else None
        m = min(len(gap_p), len(gap_b))
        S = akshara_values(pr, g, "s_true")
        cell = {(a[2], a[3]): S[k] for k, a in enumerate(g["aksharas"])}
        padas = sorted({a[2] for a in g["aksharas"]})
        did = None
        if all((p, 2) in cell and (p, 3) in cell for p in padas) and len(padas) >= 2:
            x = mean(cell[(p, 2)] for p in padas if p >= 2) - cell[(1, 2)]
            y = mean(cell[(p, 3)] for p in padas if p >= 2) - cell[(1, 3)]
            did = x - y
        wi_y = [S[k] for k, a in enumerate(g["aksharas"]) if a[9] and a[7] and a[3] > 1]
        wi_o = [S[k] for k, a in enumerate(g["aksharas"]) if a[9] and not a[7] and a[3] > 1]
        per_poem[i] = {
            "metre": metre[i], "s_true_mean": mean(v for v in pr["s_true"] if v is not None),
            "s_model_mean": mean(v for v in pr["s_model"] if v is not None),
            "d_poem": d_poem, "d_bhavam": d_bhav,
            "delta": None if d_poem is None or d_bhav is None else d_poem - d_bhav,
            "d_poem_no_first": d_poem_1,
            "delta_no_first": None if d_poem_1 is None or d_bhav_1 is None else d_poem_1 - d_bhav_1,
            "yati_seats": sum(1 for a in g["aksharas"] if a[7]),
            "yati_seats_word_initial": sum(1 for a in g["aksharas"] if a[7] and a[9]),
            "gap_poem_matched": mean(gap_p[:m]), "gap_bhavam_matched": mean(gap_b[:m]),
            "quotes_poem": bool(ngrams(pr["text"].replace("\n", " ")) & ngrams(br["text"])),
            "did_prasa": did, "yati_contrast": mean(wi_y) - mean(wi_o) if wi_y and wi_o else None,
            "has_yati": bool(wi_y), "prasa_metre": metre[i] not in NO_PRASA,
            "mid_akshara_tokens": sum(t["mid_akshara"] for t in tp), "byte_cont_tokens": sum(t["kind"] == "byte_cont" for t in tp),
        }

    low = set(sorted(ids, key=lambda i: per_poem[i]["s_true_mean"])[: len(ids) // 10])

    def nh26(sel):
        return {"d_poem": test([per_poem[i]["d_poem"] for i in sel], "greater"),
                "delta_vs_prose": test([per_poem[i]["delta"] for i in sel], "greater")}

    def nh27(sel):
        return {"prasa_did": test([per_poem[i]["did_prasa"] for i in sel if per_poem[i]["prasa_metre"]], "less"),
                "prasa_placebo": test([per_poem[i]["did_prasa"] for i in sel if not per_poem[i]["prasa_metre"]], "two-sided"),
                "yati_contrast": test([per_poem[i]["yati_contrast"] for i in sel], "less")}

    def nh21(sel):
        return test([per_poem[i]["gap_poem_matched"] - per_poem[i]["gap_bhavam_matched"] for i in sel], "greater")

    gltr = {}
    for kind in ("poem", "bhavam"):
        rk = np.array([x for i in ids for x in bos[(i, kind)]["rank"] if x is not None])
        edges = [(1, 1), (2, 10), (11, 100), (101, 1000), (1001, None)]
        gltr[kind] = {f"{a}-{b}" if b else f">{a - 1}": round(float(((rk >= a) & ((rk <= b) if b else True)).mean()), 4)
                      for a, b in edges}
        pct = 1 - (rk - 1) / 262144
        gltr[kind]["pct_quartiles"] = [round(float(np.percentile(pct, q)), 6) for q in (25, 50, 75)]

    engine = {"identified": sum(g["engine_meter"] is not None for g in grids.values()),
              "matched_relaxed": sum(bool(g["matched"]) for g in grids.values()),
              "grid_from_engine": sum(g["grid_from_engine"] for g in grids.values()),
              "engine_meter_equals_label": sum(norm_metre(g["engine_meter"] or "") == norm_metre(metre[i])
                                               for i, g in grids.items()),
              "prasa_source_counts": {s: sum(g["prasa_source"] == s for g in grids.values()) for s in ("engine", "corpus label")}}

    x = np.array([per_poem[i]["s_true_mean"] for i in ids]); y = np.array([per_poem[i]["s_model_mean"] for i in ids])
    quoting = [i for i in ids if per_poem[i]["quotes_poem"]]
    tests = {
        "condition": "bos", "poems": len(ids), "engine": engine,
        "NH26": nh26(ids), "NH26_without_lowest_decile": nh26([i for i in ids if i not in low]),
        "NH26_sensitivity_without_text_initial_token": {
            "note": "not in the spec: the first token after <bos> is left out of the pāda-first and sentence-first sets",
            "d_poem": test([per_poem[i]["d_poem_no_first"] for i in ids], "greater"),
            "delta_vs_prose": test([per_poem[i]["delta_no_first"] for i in ids], "greater")},
        "yati_seats": {"total": sum(p["yati_seats"] for p in per_poem.values()),
                       "word_initial": sum(p["yati_seats_word_initial"] for p in per_poem.values()),
                       "poems_with_a_word_initial_seat": sum(p["yati_seats_word_initial"] > 0 for p in per_poem.values())},
        "NH21_gap_poem_minus_bhavam": nh21(ids),
        "NH21_without_quoting_bhavams": dict(nh21([i for i in ids if i not in quoting]), quoting_pairs=len(quoting)),
        "NH27": nh27(ids), "NH27_without_lowest_decile": nh27([i for i in ids if i not in low]),
        "NH18": "not computed: needs EXP-19's free-running traces",
        "lowest_decile": sorted(low),
        "fig6b_poem_level": {"pearson": [round(float(stats.pearsonr(x, y).statistic), 4), float(stats.pearsonr(x, y).pvalue)],
                             "spearman": [round(float(stats.spearmanr(x, y).statistic), 4), float(stats.spearmanr(x, y).pvalue)]},
        "gltr_tiers": gltr,
        "tokens": {"mid_akshara": sum(p["mid_akshara_tokens"] for p in per_poem.values()),
                   "byte_cont": sum(p["byte_cont_tokens"] for p in per_poem.values())},
    }
    if exp08 is not None and (exp08 / "per_poem.csv").exists():
        e8 = {(r["id"], r["condition"]): float(r["nll_genuine"]) for r in csv.DictReader((exp08 / "per_poem.csv").open(encoding="utf-8"))}
        diffs = []
        for r in rows:
            if r["kind"] == "poem" and (r["id"], r["condition"]) in e8:
                diffs.append(abs(mean(v for v in r["s_true"] if v is not None) - e8[(r["id"], r["condition"])]))
        tests["gate6_vs_exp08"] = {"comparisons": len(diffs), "max_abs_difference": max(diffs)}

    # ---- figure data
    with (run / "fig6_positionwise.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["kind", "j", "n", "s_true", "s_model", "gap"])
        for kind in ("poem", "bhavam"):
            T = max(len(bos[(i, kind)]["s_true"]) for i in ids)
            for j in range(T):
                vals = [(bos[(i, kind)]["s_true"][j], bos[(i, kind)]["s_model"][j]) for i in ids
                        if j < len(bos[(i, kind)]["s_true"]) and bos[(i, kind)]["s_true"][j] is not None]
                if len(vals) >= 10:
                    w.writerow([kind, j, len(vals), round(mean(a for a, _ in vals), 4), round(mean(b for _, b in vals), 4),
                                round(mean(a - b for a, b in vals), 4)])
    with (run / "fig6b_poemlevel.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["id", "metre", "s_true_mean", "s_model_mean"])
        for i in ids:
            w.writerow([i, metre[i], round(per_poem[i]["s_true_mean"], 4), round(per_poem[i]["s_model_mean"], 4)])
    prof = defaultdict(list)
    for i in ids:
        pr, g = bos[(i, "poem")], grids[i]
        S, G = akshara_values(pr, g, "s_true"), akshara_values({**pr, "gap": [None if a is None else a - b for a, b in zip(pr["s_true"], pr["s_model"])]}, g, "gap")
        for k, a in enumerate(g["aksharas"]):
            dec = min(9, int(10 * (a[3] - 1) / max(1, a[4] - 1)))
            prof[("decile", str(dec))].append((S[k], G[k]))
            prof[("pada", str(a[2]))].append((S[k], G[k]))
            prof[(f"metre:{metre[i]}", str(a[3]))].append((S[k], G[k]))
    with (run / "fig6c_pada_profile.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["group", "value", "n", "s_true", "gap"])
        for (grp, val), v in sorted(prof.items(), key=lambda kv: (kv[0][0], int(kv[0][1]))):
            w.writerow([grp, val, len(v), round(mean(a for a, _ in v), 4), round(mean(b for _, b in v), 4)])
    (run / "tests.json").write_text(json.dumps(tests, ensure_ascii=False, indent=1), encoding="utf-8")
    return tests


# ------------------------------------------------------------------ figures
def plot(run: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    SURFACE, INK, INK2, GRID, AXIS, BLUE, ORANGE = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7", "#2a78d6", "#eb6834"
    plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                         "font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                         "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "axes.spines.top": False, "axes.spines.right": False, "xtick.color": AXIS, "ytick.color": AXIS,
                         "xtick.labelcolor": INK2, "ytick.labelcolor": INK2, "legend.frameon": False})
    pos = list(csv.DictReader((run / "fig6_positionwise.csv").open(encoding="utf-8")))
    prof = list(csv.DictReader((run / "fig6c_pada_profile.csv").open(encoding="utf-8")))
    pl = list(csv.DictReader((run / "fig6b_poemlevel.csv").open(encoding="utf-8")))
    t = json.loads((run / "tests.json").read_text(encoding="utf-8"))
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.8))
    ax = axes[0]
    for kind, color in (("poem", BLUE), ("bhavam", ORANGE)):
        r = [x for x in pos if x["kind"] == kind]
        ax.plot([int(x["j"]) for x in r], [float(x["s_true"]) for x in r], color=color, lw=1.6, label=f"{kind}: s_true")
        ax.plot([int(x["j"]) for x in r], [float(x["s_model"]) for x in r], color=color, lw=1.2, ls="--", label=f"{kind}: s_model")
    ax.set_xlabel("token index (texts reaching it, n >= 10)"); ax.set_ylabel("nats"); ax.legend(fontsize=7.5)
    ax.set_title("Fig. 6: surprisal by token position", color=INK); ax.grid(axis="y", color=GRID)
    ax = axes[1]
    ax.scatter([float(x["s_true_mean"]) for x in pl], [float(x["s_model_mean"]) for x in pl], s=14, color=BLUE,
               edgecolor=SURFACE, linewidth=0.8)
    pr, sp = t["fig6b_poem_level"]["pearson"], t["fig6b_poem_level"]["spearman"]
    ax.set_xlabel("mean s_true per poem"); ax.set_ylabel("mean s_model per poem")
    ax.set_title(f"Fig. 6b: poem level (Pearson {pr[0]:.2f}, Spearman {sp[0]:.2f})", color=INK); ax.grid(color=GRID)
    ax = axes[2]
    dec = [x for x in prof if x["group"] == "decile"]
    ax.plot([int(x["value"]) + 1 for x in dec], [float(x["s_true"]) for x in dec], color=BLUE, lw=2, marker="o", ms=4, label="s_true")
    ax.plot([int(x["value"]) + 1 for x in dec], [float(x["gap"]) for x in dec], color=ORANGE, lw=2, marker="o", ms=4, label="gap")
    ax.set_xlabel("relative position in the pāda (decile)"); ax.set_ylabel("nats per akshara"); ax.legend(fontsize=7.5)
    ax.set_title("Fig. 6c: akshara-level profile within the pāda", color=INK); ax.grid(axis="y", color=GRID)
    fig.tight_layout()
    fig.savefig(run / "fig6_surprisal.png", dpi=170)
    print(f"wrote {run / 'fig6_surprisal.png'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--exp08", type=Path, default=None, help="EXP-08 run dir, for the gate-6 cross-check")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()
    if args.plot:
        plot(args.run_dir)
        return
    t = analyse(args.run_dir, args.exp08)
    print(json.dumps(t, ensure_ascii=False, indent=1)[:6000])


if __name__ == "__main__":
    main()
