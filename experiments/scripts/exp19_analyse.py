#!/usr/bin/env python3
"""
EXP-19 analysis (steps 3, 5-7) and EXP-35's NH18, on the generations of exp19_generate.py.

Spec: experiments/EXP-19-generation-time-tracking.md; NH18 in experiments/EXP-35-...md.

    diffusion_pretraining/.venv/bin/python experiments/scripts/exp19_analyse.py GEN_DIR --exp35 EXP35_FULL_DIR --exp24 EXP24_DIR
    python3 experiments/scripts/exp19_analyse.py --plot GEN_DIR

Operational definitions (the spec leaves them open; recorded in the output):
- validator: chandohasam.analyze on the non-empty lines, profile strict / yati sandhi off (the project's
  standard) and relaxed / hypothesis; "clean" = exactly 4 non-empty lines.
- per-step outcome (step 6): only the 5 fixed-pattern metres (template = EXP-24's per-pāda canonical
  pattern, the catalogue pattern) and clean poems. A token that writes at least one akshara (the akshara
  starts inside the token) violates when any such akshara's weight differs from the template at its
  slot; the pāda-final slot is free (pādānta); an akshara beyond the template length violates.
- sandhi junction: a word boundary (the scanner's word index changes); predictor = aksharas since the
  last junction (0 for a word-initial akshara).
- rare word: the token occurs fewer than RARE times in the tokenised Bhāgavatam verse corpus.
- regression: logistic, fitted by Newton/IRLS; cluster-robust (by generation) sandwich standard errors
  with the small-sample factor G/(G-1)*(N-1)/(N-K); null model = intercept + absolute position.
- decay curve (step 7): cosine of each step's hidden state with EXP-22's coarse direction at layers 6
  and 35 (the coarse contrast's two peaks); the change in cosine at pāda-initial steps (the first token
  after a newline) against other steps, and the per-poem slope over steps.
- NH18: per-slot satisfaction of the fixed metres, teacher-forced (EXP-35's argmax from the true
  prefix, first akshara of the argmax token, weight resolved inside the token or else from the true
  next akshara) against free-running (the generated aksharas).
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import unicodedata
from collections import Counter, defaultdict
from multiprocessing import Pool
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

FIXED = ("champakamala", "mattakokila", "mattebhavikriditamu", "shardulavikriditamu", "utpalamala")
CATALOGUE_NAME = {"aataveladi": "ataveladi", "shardulavikriditamu": "sardulavikriditamu", "mattakokila": "mattakokilamu"}
RARE = 10
LAYERS = (6, 35)


def norm(name: str) -> str:
    return (name or "").replace("aataveladi", "ataveladi").replace("shardula", "sardula").replace("mattakokilamu", "mattakokila")


# ------------------------------------------------------------------ validator (parallel)
def validate(item):
    rid, metre, text = item
    from chandohasam import analyze
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    out = {"id": rid, "lines": len(lines), "clean": len(lines) == 4}
    if not lines:
        return out
    a = analyze(lines, profile="strict", yati_sandhi="off")
    out.update(identified=a.identified, meter=a.meter, candidates=a.candidates[:5],
               as_target=norm(a.meter) == norm(metre), failures=a.failures[:3])
    for prof, sandhi in (("strict", "off"), ("relaxed", "hypothesis")):
        f = analyze(lines, profile=prof, yati_sandhi=sandhi, meter=CATALOGUE_NAME.get(metre, metre))
        head = bool(f.identified and f.units and norm(f.units[0].meter) == norm(metre))
        out[f"valid_{prof}"] = bool(head and f.matched)
    return out


# ------------------------------------------------------------------ helpers
def line_spans(text: str):
    """(global start of the stripped line, stripped line) for each non-empty line."""
    spans, pos = [], 0
    for raw in text.split("\n"):
        st = raw.strip()
        if st:
            spans.append((pos + len(raw) - len(raw.lstrip()), st))
        pos += len(raw) + 1
    return spans


def aksharas_of(text: str):
    """Scanner aksharas with global offsets: (start, end, pada, idx, weight, word, rules)."""
    from indic_meter_dawg.scansion import scan_line
    out = []
    for p, (start, line) in enumerate(line_spans(text), start=1):
        for i, s in enumerate(scan_line(line).syllables, start=1):
            out.append((start + s.start, start + s.end, p, i, s.weight, s.word, s.rules))
    return out


def logistic(X, y, groups, iters=50):
    import numpy as np
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        H = X.T @ (X * W[:, None])
        step = np.linalg.solve(H, X.T @ (y - p))
        b += step
        if np.abs(step).max() < 1e-10:
            break
    p = np.clip(1 / (1 + np.exp(-X @ b)), 1e-12, 1 - 1e-12)
    Hinv = np.linalg.inv(X.T @ (X * (p * (1 - p))[:, None]))
    u = (y - p)[:, None] * X
    meat = np.zeros((X.shape[1], X.shape[1]))
    G = 0
    for g in np.unique(groups):
        s = u[groups == g].sum(axis=0)
        meat += np.outer(s, s)
        G += 1
    N, K = X.shape
    V = Hinv @ meat @ Hinv * (G / (G - 1)) * ((N - 1) / (N - K))
    dev = -2 * float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))
    return b, np.sqrt(np.diag(V)), dev


def normal_p(z):
    return math.erfc(abs(z) / math.sqrt(2))


# ------------------------------------------------------------------ analysis
def analyse(gen_dir: Path, exp35: Path, exp24: Path) -> dict:
    import numpy as np
    from scipy import stats
    from transformers import AutoTokenizer
    import exp35_surprisal as e35

    rows = [json.loads(line) for line in (gen_dir / "generations.jsonl").open(encoding="utf-8")]
    tok = AutoTokenizer.from_pretrained(e35.snapshot_dir())
    templates = {}
    canon = json.loads((exp24 / "summary.json").read_text(encoding="utf-8"))["canonical"]
    from indic_meter_dawg.scansion import scan, scan_line
    corpus = json.loads((ROOT / "dataset" / "bhagavatam.json").read_text(encoding="utf-8"))
    for m in FIXED:     # per-pāda canonical pattern: the plurality mode of each pāda position
        pats = defaultdict(Counter)
        for r in corpus:
            if r["metre_roman"] == m and r["form"] == "verse" and r["verse"]:
                ps = [s.pattern for s in scan(r["verse"])]
                if len(ps) == 4:
                    for k, x in enumerate(ps):
                        pats[k][x] += 1
        templates[m] = [pats[k].most_common(1)[0][0] for k in range(4)]
        assert "".join(templates[m]) == canon[m]["mode_per_pada"]
    counts = Counter()
    for r in corpus:
        if r["form"] == "verse" and r["verse"]:
            counts.update(tok("\n".join(r["verse"]), add_special_tokens=False)["input_ids"])

    with Pool(8) as pool:
        val = {v["id"]: v for v in pool.map(validate, [(r["id"], r["metre"], r["text"]) for r in rows])}
    clean = [r for r in rows if val[r["id"]]["clean"]]
    validator = {
        "generations": len(rows), "truncated": sum(r["stop"] != "eos" for r in rows), "clean_4_lines": len(clean),
        "line_counts": dict(Counter(val[r["id"]]["lines"] for r in rows)),
        "identified_any_metre": sum(bool(v.get("identified")) for v in val.values()),
        "identified_any_metre_clean": sum(bool(val[r["id"]].get("identified")) for r in clean),
        "identified_as_target": sum(bool(v.get("as_target")) for v in val.values()),
        "valid_target_strict": sum(bool(v.get("valid_strict")) for v in val.values()),
        "valid_target_relaxed": sum(bool(v.get("valid_relaxed")) for v in val.values()),
        "mean_tokens": round(mean(len(r["tokens"]) for r in rows), 1)}

    # ---- per-step records (fixed metres, clean poems)
    steps, skipped_nfc, skipped_offsets = [], 0, 0
    decay = []
    for r in rows:
        text, ids = r["text"], r["tokens"]
        if unicodedata.normalize("NFC", text) != text:
            skipped_nfc += 1
            continue
        offs, prev, ok = [], 0, True
        for j in range(len(ids)):
            cur = len(tok.decode(ids[: j + 1], skip_special_tokens=True))
            ok = ok and cur >= prev
            offs.append((prev, max(cur, prev)))
            prev = max(cur, prev)
        if not ok or prev != len(text):
            skipped_offsets += 1
            continue
        aks = aksharas_of(text)
        starts = {a[0]: k for k, a in enumerate(aks)}
        pada_initial = [False] * len(ids)
        for j, (s, e) in enumerate(offs):
            if j > 0 and "\n" in text[offs[j - 1][0]:offs[j - 1][1]] and e > s:
                pada_initial[j] = True
        for j, st in enumerate(r["steps"]):
            decay.append({"id": r["id"], "metre": r["metre"], "step": j, "pada_initial": pada_initial[j],
                          **{f"cos_L{l}": st["cos_coarse"][l] for l in LAYERS}})
        if r["metre"] not in FIXED or not val[r["id"]]["clean"]:
            continue
        tmpl = templates[r["metre"]]
        for j, (s, e) in enumerate(offs):
            written = [aks[starts[c]] for c in range(s, e) if c in starts]
            if not written:
                continue
            viol, beyond = 0, 0
            for a in written:
                t = tmpl[a[2] - 1]
                if a[3] > len(t):
                    viol, beyond = 1, 1
                elif a[3] < len(t) and a[4] != t[a[3] - 1]:
                    viol = 1
            first = written[0]
            k0 = starts[first[0]]
            since = 0
            while k0 - since - 1 >= 0 and aks[k0 - since - 1][2] == first[2] and aks[k0 - since - 1][5] == first[5]:
                since += 1
            steps.append({"id": r["id"], "violation": viol, "beyond_template": beyond, "abs_pos": j, "pos_in_pada": first[3],
                          "since_junction": since, "entropy": r["steps"][j]["entropy"],
                          "rare": int(counts.get(ids[j], 0) < RARE)})

    def fit(steps):
        y = np.array([s["violation"] for s in steps], dtype=float)
        groups = np.array([s["id"] for s in steps])
        feats = ["abs_pos", "pos_in_pada", "since_junction", "entropy", "rare"]
        Z = {f: np.array([s[f] for s in steps], dtype=float) for f in feats}
        for f in ("abs_pos", "pos_in_pada", "since_junction", "entropy"):
            Z[f] = (Z[f] - Z[f].mean()) / Z[f].std()
        one = np.ones(len(y))
        _, _, dev0 = logistic(np.column_stack([one, Z["abs_pos"]]), y, groups)
        b, se, dev = logistic(np.column_stack([one] + [Z[f] for f in feats]), y, groups)
        coefs = {name: {"coef": round(float(b[k]), 4), "cluster_se": round(float(se[k]), 4), "z": round(float(b[k] / se[k]), 3),
                        "p": normal_p(b[k] / se[k])} for k, name in enumerate(["intercept"] + feats)}
        drops = {}
        for f in feats:
            keep = [g for g in feats if g != f]
            _, _, d = logistic(np.column_stack([one] + [Z[g] for g in keep]), y, groups)
            drops[f] = round(d - dev, 2)
        return {"steps": int(len(y)), "poems": int(len(np.unique(groups))), "violation_rate": round(float(y.mean()), 4),
                "null_deviance_position_only": round(dev0, 2), "full_deviance": round(dev, 2),
                "deviance_drop_over_null": round(dev0 - dev, 2), "coefficients_standardised": coefs,
                "deviance_increase_when_dropped": drops}

    regression = fit(steps)
    regression["within_template_only"] = fit([s for s in steps if not s["beyond_template"]])
    regression.update(rare_threshold=RARE, note="continuous predictors standardised; p from cluster-robust z; "
                      "within_template_only drops tokens that write an akshara beyond the template's length")
    y = np.array([s["violation"] for s in steps], dtype=float)

    # ---- decay curve
    shape = {}
    for l in LAYERS:
        key = f"cos_L{l}"
        by_id = defaultdict(list)
        for d in decay:
            by_id[d["id"]].append(d)
        slopes, bdiff = [], []
        for rid, ds in by_id.items():
            ds.sort(key=lambda d: d["step"])
            c = np.array([d[key] for d in ds])
            if len(c) >= 10:
                slopes.append(float(np.polyfit(np.arange(len(c)), c, 1)[0]) * 100)
            dc = np.diff(c)
            pi = np.array([d["pada_initial"] for d in ds[1:]])
            if pi.any() and (~pi).any():
                bdiff.append(float(dc[pi].mean() - dc[~pi].mean()))
        w1 = stats.wilcoxon(slopes)
        w2 = stats.wilcoxon(bdiff)
        shape[f"L{l}"] = {"slope_per_100_steps": {"mean": round(float(np.mean(slopes)), 4), "median": round(float(np.median(slopes)), 4),
                                                  "n": len(slopes), "wilcoxon_p": float(w1.pvalue)},
                          "pada_initial_minus_other_step_change": {"mean": round(float(np.mean(bdiff)), 4),
                                                                   "median": round(float(np.median(bdiff)), 4),
                                                                   "n": len(bdiff), "wilcoxon_p": float(w2.pvalue)}}
    with (gen_dir / "decay_by_step.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["step", "n"] + [f"cos_L{l}" for l in LAYERS] + ["pada_initial_share"])
        agg = defaultdict(list)
        for d in decay:
            agg[d["step"]].append(d)
        for st in sorted(agg):
            ds = agg[st]
            if len(ds) >= 10:
                w.writerow([st, len(ds)] + [round(mean(d[f"cos_L{l}"] for d in ds), 4) for l in LAYERS]
                           + [round(mean(d["pada_initial"] for d in ds), 3)])

    # ---- NH18
    tf, fr = defaultdict(list), defaultdict(list)
    for line in (exp35 / "traces.jsonl").open(encoding="utf-8"):
        r = json.loads(line)
        if r["condition"] != "bos" or r["kind"] != "poem" or r["metre"] not in FIXED:
            continue
        tmpl = templates[r["metre"]]
        aks = aksharas_of(r["text"])
        starts = {a[0]: k for k, a in enumerate(aks)}
        for (s, e), am in zip(r["offsets"], r["argmax"]):
            anchor = next((c for c in range(s, e) if not r["text"][c].isspace()), None)
            if anchor is None or anchor not in starts or am is None:
                continue
            k = starts[anchor]
            a = aks[k]
            if a[3] >= len(tmpl[a[2] - 1]):
                continue
            piece = tok.decode([am]).strip()
            sy = scan_line(piece).syllables if piece else ()
            if not sy:
                continue
            if sy[0].weight == "U" or len(sy) > 1:
                wgt = sy[0].weight              # decided inside the argmax token
            else:
                wgt = "U" if "samyukta" in a[6] else "I"   # no self rule: the true next akshara decides
            tf[(r["metre"], a[3])].append(int(wgt == tmpl[a[2] - 1][a[3] - 1]))
    for r in clean:
        if r["metre"] not in FIXED:
            continue
        tmpl = templates[r["metre"]]
        for a in aksharas_of(r["text"]):
            t = tmpl[a[2] - 1]
            if a[3] < len(t):
                fr[(r["metre"], a[3])].append(int(a[4] == t[a[3] - 1]))
    slots = sorted(set(tf) & set(fr))
    tf_all = [x for k in slots for x in tf[k]]
    fr_all = [x for k in slots for x in fr[k]]
    by_slot = defaultdict(lambda: [[], []])
    for (m, k) in slots:
        by_slot[k][0].append(mean(tf[(m, k)])); by_slot[k][1].append(mean(fr[(m, k)]))
    with (gen_dir / "nh18_by_slot.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(["slot", "teacher_forced", "free_running", "gap"])
        for k in sorted(by_slot):
            a, b2 = mean(by_slot[k][0]), mean(by_slot[k][1])
            w.writerow([k, round(a, 4), round(b2, 4), round(a - b2, 4)])
    gaps = [mean(tf[k]) - mean(fr[k]) for k in slots]
    nh18 = {"slots": len(slots), "teacher_forced_rate": round(mean(tf_all), 4), "free_running_rate": round(mean(fr_all), 4),
            "tf_aksharas": len(tf_all), "fr_aksharas": len(fr_all),
            "mean_slot_gap_tf_minus_fr": round(mean(gaps), 4), "slots_tf_higher": sum(g > 0 for g in gaps),
            "wilcoxon_p_slot_gaps": float(stats.wilcoxon(gaps).pvalue)}

    summary = {"validator": validator, "regression": regression, "decay": shape, "nh18": nh18,
               "per_step_skipped_not_nfc": skipped_nfc, "per_step_skipped_offsets": skipped_offsets, "templates": templates,
               "pipeline": {"truncated": "5% (10/200)", "clean": "94% (189/200)", "compliant": "0/189", "note": "JSON prompt, 1,000 tokens"}}
    (gen_dir / "validation.jsonl").write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in val.values()), encoding="utf-8")
    (gen_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    return summary


def plot(gen_dir: Path) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    SURFACE, INK, INK2, GRID, AXIS, BLUE, ORANGE = "#fcfcfb", "#0b0b0b", "#52514e", "#e1e0d9", "#c3c2b7", "#2a78d6", "#eb6834"
    plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                         "font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                         "axes.titlesize": 9.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
                         "axes.spines.top": False, "axes.spines.right": False, "xtick.color": AXIS, "ytick.color": AXIS,
                         "xtick.labelcolor": INK2, "ytick.labelcolor": INK2, "legend.frameon": False})
    dec = list(csv.DictReader((gen_dir / "decay_by_step.csv").open(encoding="utf-8")))
    nh = list(csv.DictReader((gen_dir / "nh18_by_slot.csv").open(encoding="utf-8")))
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 3.8))
    ax = axes[0]
    for l, color in zip(LAYERS, (BLUE, ORANGE)):
        ax.plot([int(d["step"]) for d in dec], [float(d[f"cos_L{l}"]) for d in dec], color=color, lw=1.8, label=f"layer {l}")
    ax.set_xlabel("generation step (steps reached by >= 10 poems)"); ax.set_ylabel("cosine with the coarse direction")
    ax.set_title("EXP-19 step 7: alignment with the chandas direction", color=INK); ax.legend(); ax.grid(axis="y", color=GRID)
    ax = axes[1]
    ax.plot([int(d["slot"]) for d in nh], [float(d["teacher_forced"]) for d in nh], color=BLUE, lw=1.8, marker="o", ms=3, label="teacher-forced (EXP-35)")
    ax.plot([int(d["slot"]) for d in nh], [float(d["free_running"]) for d in nh], color=ORANGE, lw=1.8, marker="o", ms=3, label="free-running (EXP-19)")
    ax.set_xlabel("akshara slot in the pāda (fixed metres)"); ax.set_ylabel("share matching the template weight")
    ax.set_title("NH18: template weight satisfied, by slot", color=INK); ax.legend(); ax.grid(axis="y", color=GRID); ax.set_ylim(0, 1)
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.tight_layout(); fig.savefig(gen_dir / "fig_exp19.png", dpi=170); print(f"wrote {gen_dir / 'fig_exp19.png'}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("gen_dir", type=Path)
    ap.add_argument("--exp35", type=Path, default=ROOT / "experiments" / "exp35" / "2026-09-29_full")
    ap.add_argument("--exp24", type=Path, default=ROOT / "experiments" / "exp24" / "2026-09-29_bos")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()
    if args.plot:
        plot(args.gen_dir)
        return
    s = analyse(args.gen_dir, args.exp35, args.exp24)
    print(json.dumps({k: v for k, v in s.items() if k != "templates"}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
