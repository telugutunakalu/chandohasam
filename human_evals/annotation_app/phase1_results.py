#!/usr/bin/env python3
"""Phase-1 results: the 100 poems of data/active_pool.json (build_active_pool.py), from a copy of the database.

    .venv/bin/python phase1_results.py          # → reports/phase1/ (results.md, agreement.md / .json, annotations.csv)

The live database is opened read-only and copied with SQLite's backup API; the copy is the only thing changed (its
annotations outside the 100 are left out), so the annotators' data stays exactly as recorded. On the copy:
- progress: each annotator's ratings of the 100 (and of the 25-poem calibration set);
- agreement: padya_eval.report on the 100 (Krippendorff's α with bootstrap CIs, agreement shares, κ, AC1);
- sources: the mean of each question per source, and each source against the real poets (bhāgavatam, vemana,
  kuchimanchi) after removing every annotator's own mean (leniency), with a bootstrap over poems (95% interval).
"""
from __future__ import annotations

import collections
import csv
import json
import random
import sqlite3
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "reports" / "phase1"
SCALES = ["readability", "comprehension", "lexical", "bhavam", "poetic"]
YESNO = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara", "register", "ai_generated"]   # register: 1 = grānthika
REAL = {"bhagavatam", "vemana", "kuchimanchi"}


def group(source: str) -> str:
    return "real poets" if source in REAL else ("generated (Gemini)" if source == "generated" else "textbook reference")


def num(v):
    return None if v in ("", "None", "null") else float(v)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def main() -> None:
    active = json.loads((HERE / "data" / "active_pool.json").read_text(encoding="utf-8"))["ids"]
    keep = set(active)
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "annotations_phase1.db"
        src = sqlite3.connect(f"file:{HERE / 'instance' / 'annotations.db'}?mode=ro", uri=True)
        dst = sqlite3.connect(copy)
        src.backup(dst)
        src.close()
        total = dst.execute("SELECT COUNT(*) FROM annotations").fetchone()[0]
        q = ",".join("?" * len(keep))
        dst.execute(f"DELETE FROM annotations WHERE eval_id NOT IN ({q})", list(keep))     # the copy only
        dst.commit()
        inside = dst.execute("SELECT COUNT(*) FROM annotations").fetchone()[0]
        dst.close()
        subprocess.run([sys.executable, "-m", "padya_eval.report", "--db", str(copy), "--out", str(OUT),
                        "--bootstrap", "1000"], cwd=HERE, check=True, capture_output=True)
    rows = list(csv.DictReader(open(OUT / "annotations.csv", encoding="utf-8")))
    for r in rows:
        r["group"] = group(r["source_dataset"])
        for k in SCALES + YESNO:
            r[k] = num(r.get(k))
    cal = {r["eval_id"] for r in rows if r["calibration"] in ("1", "True", "true")}

    # progress
    users = sorted({r["annotator"] for r in rows})
    prog = {u: (sum(r["annotator"] == u for r in rows), sum(r["annotator"] == u and r["eval_id"] in cal for r in rows))
            for u in users}

    # per-source means
    groups = ["real poets", "textbook reference", "generated (Gemini)"]
    means = {g: {k: mean([r[k] for r in rows if r["group"] == g]) for k in SCALES + YESNO} for g in groups}
    n_by = {g: (sum(r["group"] == g for r in rows), len({r["eval_id"] for r in rows if r["group"] == g})) for g in groups}

    # rater-centred contrasts against the real poets, bootstrap over poems
    rmean = {(u, k): mean([r[k] for r in rows if r["annotator"] == u]) for u in users for k in SCALES}
    per_poem = collections.defaultdict(lambda: collections.defaultdict(list))
    poem_group = {}
    for r in rows:
        poem_group[r["eval_id"]] = r["group"]
        for k in SCALES:
            if r[k] is not None:
                per_poem[r["eval_id"]][k].append(r[k] - rmean[(r["annotator"], k)])
    rng = random.Random(7)
    contrasts = {}
    for g in ("generated (Gemini)", "textbook reference"):
        contrasts[g] = {}
        for k in SCALES:
            a = [sum(v) / len(v) for e, d in per_poem.items() if poem_group[e] == g and (v := d[k])]
            b = [sum(v) / len(v) for e, d in per_poem.items() if poem_group[e] == "real poets" and (v := d[k])]
            if len(a) < 3 or len(b) < 3:
                continue
            boot = sorted(sum(rng.choices(a, k=len(a))) / len(a) - sum(rng.choices(b, k=len(b))) / len(b)
                          for _ in range(5000))
            contrasts[g][k] = {"diff": sum(a) / len(a) - sum(b) / len(b), "lo": boot[124], "hi": boot[4874],
                               "poems": [len(a), len(b)]}

    res = {"created": time.strftime("%Y-%m-%d %H:%M"), "poems": len(active), "ratings_total_in_db": total,
           "ratings_on_the_100": inside, "progress": prog, "groups": n_by, "means": means, "contrasts": contrasts}
    (OUT / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    f = lambda x, d=2: "–" if x is None else f"{x:.{d}f}"                               # noqa: E731
    md = [f"# Human evaluation, phase 1 (100 poems): results as of {res['created']}", "",
          f"100 poems (20 per source: bhāgavatam, vemana, kūcimañci, Gemini-generated, textbook examples; the 25 "
          f"calibration poems included). {inside} of the database's {total} ratings fall on them; the rest are kept "
          f"for the full pass. Agreement statistics: agreement.md.", "",
          "## Progress", "", "| annotator | rated (of 100) | calibration (of 25) |", "|---|---|---|"]
    md += [f"| {u} | {a} | {c} |" for u, (a, c) in prog.items()]
    md += ["", "## Mean rating per source", "",
           "| source | ratings / poems | " + " | ".join(SCALES + YESNO) + " |",
           "|---|---|" + "---|" * len(SCALES + YESNO)]
    for g in groups:
        md.append(f"| {g} | {n_by[g][0]} / {n_by[g][1]} | " + " | ".join(f(means[g][k]) for k in SCALES + YESNO) + " |")
    md += ["", "## Against the real poets (each annotator's own mean removed; bootstrap over poems, 95%)", "",
           "| source | " + " | ".join(SCALES) + " |", "|---|" + "---|" * len(SCALES)]
    for g, c in contrasts.items():
        md.append(f"| {g} | " + " | ".join(
            f"{c[k]['diff']:+.2f} [{c[k]['lo']:+.2f}, {c[k]['hi']:+.2f}]" if k in c else "–" for k in SCALES) + " |")
    md += ["", "1–5 scales: readability, comprehension, lexical (words), bhavam (closeness), poetic. Yes/no questions "
           "as the share of yes; register = the share judged grānthika, ai_generated = the share judged AI-generated "
           "(both rubric v2, from 2026-10-26: ratings made before it lack them until reopened). An interval that excludes 0 marks a difference beyond the sampling noise of the poems "
           "rated so far; with low agreement (agreement.md), only large differences can show."]
    (OUT / "results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
