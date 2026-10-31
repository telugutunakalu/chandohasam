#!/usr/bin/env python3
"""Study-2 results: the 99 poems of three fine-tuned models (build_study2_pool.py), from copies of the databases.

    .venv/bin/python study2_results.py          # → reports/study2_results/ (results.md / .json, agreement.md / .json,
                                                #   annotations.csv)

Both live databases are opened read-only and copied with SQLite's backup API; nothing in them changes. On the copies:
- progress: each annotator's ratings of the 99 (and of the 6-poem calibration set);
- agreement: padya_eval.report --study 2 (Krippendorff's α with bootstrap CIs, agreement shares, κ, AC1), Q13 included;
- models: the mean of each question per model as rated, and each model against the other two after removing every
  annotator's own mean (leniency), bootstrap over prompts (95% interval);
- against the poets: every study-2 poem answers a prompt whose gold poem (its he_ poem) the same annotators rated in
  study 1. Per annotator and prompt, the model poem's rating minus that annotator's own study-1 rating of the gold,
  averaged; bootstrap over prompts. Within one annotator, leniency cancels; the two studies differ in other ways
  (study 2 hides the engine's verdicts, and its annotators know every poem is a model's), so read it as a gap, not a
  controlled contrast.
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
OUT = HERE / "reports" / "study2_results"
POOL = HERE.parent / "human_eval_poems_study2.json"
SCALES = ["readability", "comprehension", "lexical", "coherence", "bhavam", "poetic"]     # coherence: Q13, study 2 only
GOLD_SCALES = [k for k in SCALES if k != "coherence"]
YESNO = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara", "register", "ai_generated"]
MODELS = {"mdlm523m_ft": "MDLM 523M", "t5_1b_ft": "T5Gemma 2 1B", "nandi_ft": "Nandi-Mini-150M"}


def num(v):
    return None if v in (None, "", "None", "null") else float(v)     # None: a column the study lacks (coherence)


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def export(db: Path, tmp: Path, study: str) -> list[dict]:
    """A read-only copy of a live database, exported by padya_eval.report (current answers of every rating)."""
    copy = tmp / db.name
    src = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    src.close()
    dst.close()
    out = OUT if study == "2" else tmp / "study1"
    subprocess.run([sys.executable, "-m", "padya_eval.report", "--study", study, "--db", str(copy), "--out", str(out),
                    "--bootstrap", "1000"], cwd=HERE, check=True, capture_output=True)
    rows = list(csv.DictReader(open(out / "annotations.csv", encoding="utf-8")))
    for r in rows:
        for k in SCALES + YESNO:
            r[k] = num(r.get(k))
    return rows


def boot(values_by_prompt: dict, rng: random.Random, n: int = 5000) -> dict | None:
    """Mean over prompts of each prompt's mean, with a 95% bootstrap interval over prompts."""
    v = [sum(x) / len(x) for x in values_by_prompt.values() if x]
    if len(v) < 3:
        return None
    b = sorted(sum(rng.choices(v, k=len(v))) / len(v) for _ in range(n))
    return {"diff": sum(v) / len(v), "lo": b[int(0.025 * n) - 1], "hi": b[int(0.975 * n) - 1], "prompts": len(v)}


def main() -> None:
    pool = json.loads(POOL.read_text(encoding="utf-8"))["poems"]
    meta = {p["eval_id"]: {"model": p["source_dataset"], "prompt": p["metadata"]["prompt_id"],
                           "gold": p["metadata"]["gold_eval_id"], "gold_source": p["metadata"]["gold_source"]}
            for p in pool}
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        rows = export(HERE / "instance" / "annotations_study2.db", tmp, "2")
        gold_rows = export(HERE / "instance" / "annotations.db", tmp, "1")
    latest = max(r["updated_at"] or r["created_at"] for r in rows)
    for r in rows:
        r.update(meta[r["eval_id"]])
    cal = {r["eval_id"] for r in rows if r["calibration"] in ("1", "True", "true")}

    # progress
    users = sorted({r["annotator"] for r in rows})
    prog = {u: (sum(r["annotator"] == u for r in rows), sum(r["annotator"] == u and r["eval_id"] in cal for r in rows))
            for u in users}

    # per-model means as rated (poem means)
    by_poem = collections.defaultdict(list)
    for r in rows:
        by_poem[r["eval_id"]].append(r)
    means, n_by = {}, {}
    for m in MODELS:
        poems = [e for e in by_poem if meta[e]["model"] == m]
        means[m] = {k: mean([mean([r[k] for r in by_poem[e]]) for e in poems]) for k in SCALES + YESNO}
        n_by[m] = (sum(len(by_poem[e]) for e in poems), len(poems))

    rng = random.Random(7)
    # each model against the other two: annotator-centred, the same prompt, bootstrap over prompts
    rmean = {(u, k): mean([r[k] for r in rows if r["annotator"] == u]) for u in users for k in SCALES}
    cell = collections.defaultdict(list)                     # (prompt, model, k) → centred ratings
    for r in rows:
        for k in SCALES:
            if r[k] is not None:
                cell[(r["prompt"], r["model"], k)].append(r[k] - rmean[(r["annotator"], k)])
    contrasts = {}
    for m in MODELS:
        contrasts[m] = {}
        for k in SCALES:
            d = collections.defaultdict(list)
            for p in {r["prompt"] for r in rows}:
                own, others = cell.get((p, m, k)), [x for o in MODELS if o != m for x in cell.get((p, o, k), [])]
                if own and others:
                    d[p].append(sum(own) / len(own) - sum(others) / len(others))
            if (c := boot(d, rng)) is not None:
                contrasts[m][k] = c

    # against the poets: the same annotator's study-1 rating of the prompt's gold poem
    gold = {(r["annotator"], r["eval_id"]): r for r in gold_rows if r["annotator"] in users}     # study 2's raters
    gaps = {}
    for m in list(MODELS) + ["all"]:
        gaps[m] = {}
        for k in GOLD_SCALES:
            d = collections.defaultdict(list)
            for r in rows:
                g = gold.get((r["annotator"], r["gold"]))
                if (m == "all" or r["model"] == m) and g and r[k] is not None and g[k] is not None:
                    d[r["prompt"]].append(r[k] - g[k])
            if (c := boot(d, rng)) is not None:
                gaps[m][k] = c
    gold_means = {k: mean([mean([g[k] for (u, e), g in gold.items() if e == ge])
                           for ge in {v["gold"] for v in meta.values()}]) for k in GOLD_SCALES}

    res = {"created": time.strftime("%Y-%m-%d %H:%M"), "latest_rating": latest, "poems": len(pool),
           "ratings": len(rows), "progress": prog, "models": n_by, "means": means, "contrasts": contrasts,
           "gaps_vs_gold": gaps, "gold_means_study1": gold_means}
    (OUT / "results.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    f = lambda x, d=2: "–" if x is None else f"{x:.{d}f}"                               # noqa: E731
    ci = lambda c: f"{c['diff']:+.2f} [{c['lo']:+.2f}, {c['hi']:+.2f}]{' ✱' if c['lo'] > 0 or c['hi'] < 0 else ''}"  # noqa: E731
    md = [f"# Human evaluation, study 2 (99 model poems): results as of {res['created']}", "",
          f"99 poems: the same 33 prompts written by three fine-tuned models with the v2 metrical decoder (33 each); "
          f"the AI poems only. {len(rows)} ratings (latest {latest[:16]}); agreement statistics: agreement.md.", "",
          "## Progress", "", "| annotator | rated (of 99) | calibration (of 6) |", "|---|---|---|"]
    md += [f"| {u} | {a} | {c} |" for u, (a, c) in prog.items()]
    md += ["", "## Mean rating per model (poem means, as rated)", "",
           "| model | ratings / poems | " + " | ".join(SCALES + YESNO) + " |", "|---|---|" + "---|" * len(SCALES + YESNO)]
    for m, name in MODELS.items():
        md.append(f"| {name} | {n_by[m][0]} / {n_by[m][1]} | " + " | ".join(f(means[m][k]) for k in SCALES + YESNO) + " |")
    md.append("| *the 33 golds, study 1* | | " + " | ".join(f(gold_means.get(k)) for k in SCALES) + " |"
              + " |" * len(YESNO))
    md += ["", "## Each model against the other two (annotator-centred, same prompt; bootstrap over prompts, 95%)", "",
           "| model | " + " | ".join(SCALES) + " |", "|---|" + "---|" * len(SCALES)]
    for m, name in MODELS.items():
        md.append(f"| {name} | " + " | ".join(ci(contrasts[m][k]) if k in contrasts[m] else "–" for k in SCALES) + " |")
    md += ["", "## Against the poets: model poem − the same annotator's study-1 rating of the prompt's gold "
           "(bootstrap over prompts, 95%)", "", "| model | " + " | ".join(GOLD_SCALES) + " |",
           "|---|" + "---|" * len(GOLD_SCALES)]
    for m in list(MODELS) + ["all"]:
        md.append(f"| {MODELS.get(m, 'all three')} | "
                  + " | ".join(ci(gaps[m][k]) if k in gaps[m] else "–" for k in GOLD_SCALES) + " |")
    md += ["", "1–5 scales: readability, comprehension, lexical (words), coherence (Q13, how meaningful), bhavam "
           "(closeness), poetic. Yes/no questions as the share of yes; register = the share judged grānthika, "
           "ai_generated = the share judged AI-generated (not blind: the annotators know every study-2 poem is a "
           "model's). ✱: the interval excludes 0. Study 2 shows the metre (gaṇa table) but not the engine's verdicts; "
           "study 1 showed both."]
    (OUT / "results.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
