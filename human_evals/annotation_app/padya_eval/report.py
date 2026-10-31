# -*- coding: utf-8 -*-
"""
The agreement report and the exports, shared by the admin page and the command line.

    python -m padya_eval.report --db instance/annotations.db --out reports/ --bootstrap 1000

This writes agreement.json, agreement.md and annotations.csv. The CSV has one row per
(annotator, poem), with the hidden source columns joined in for analysis.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Optional, Sequence

from . import agreement as ag
from . import db
from .rubric import QUESTIONS, RUBRIC_VERSION, STUDY2_QUESTIONS, STUDY2_RUBRIC_VERSION, Question

MIN_PAIR_OVERLAP = 5


# -----------------------------------------------------------------------------
# reshaping
# -----------------------------------------------------------------------------
def ratings_by_question(annotations: Iterable[dict], subset: Optional[set] = None,
                        questions: Sequence[Question] = QUESTIONS) -> dict:
    """{question key: {eval_id: {username: value}}}, None answers (not applicable) left out."""
    out: dict = {q.key: defaultdict(dict) for q in questions}
    for a in annotations:
        if subset is not None and a["eval_id"] not in subset:
            continue
        for q in questions:
            v = a["answers"].get(q.key)
            if v is not None:
                out[q.key][a["eval_id"]][a["username"]] = v
    return {k: dict(v) for k, v in out.items()}


def _units(ratings: dict) -> dict:
    return {e: list(r.values()) for e, r in ratings.items()}


def _r(x: Optional[float], nd: int = 3) -> Optional[float]:
    return None if x is None else round(x, nd)


# -----------------------------------------------------------------------------
# per-question statistics
# -----------------------------------------------------------------------------
def question_stats(q: Question, ratings: dict, n_boot: int = 0, seed: int = 0,
                   min_overlap: int = MIN_PAIR_OVERLAP) -> dict:
    units = _units(ratings)
    values = [v for vs in units.values() for v in vs]
    paired = {e: vs for e, vs in units.items() if len(vs) >= 2}
    weights = "quadratic" if q.kind == "likert" else None
    pairs = ag.pairwise_cohen(ratings, weights=weights, categories=q.choices, min_overlap=min_overlap)
    out = {
        "key": q.key, "number": q.number, "text": q.text, "kind": q.kind, "level": q.level,
        "n_ratings": len(values), "n_units": len(units), "n_paired_units": len(paired),
        "alpha": _r(ag.krippendorff_alpha(units, q.level)),
        "alpha_ci": None,
        "pct_agreement": _r(ag.percent_agreement(units)),
        "mean_pairwise_kappa": _r(ag.mean_pairwise_kappa(pairs)),
        "kappa_weights": weights or "none",
        "n_annotator_pairs": sum(1 for p in pairs.values() if p["kappa"] is not None),
        "distribution": {str(c): Counter(values).get(c, 0) for c in q.choices},
    }
    if n_boot and len(paired) >= 2:
        ci = ag.bootstrap_alpha_ci(units, q.level, n_boot=n_boot, seed=seed)
        out["alpha_ci"] = [_r(ci[0]), _r(ci[1])] if ci else None
    if q.kind == "likert":
        out["alpha_interval"] = _r(ag.krippendorff_alpha(units, "interval"))
        out["within_one"] = _r(ag.within_one_agreement(units))
        out["mean"] = _r(statistics.fmean(values), 2) if values else None
    else:
        out["fleiss_kappa"] = _r(ag.fleiss_kappa(units))
        out["gwet_ac1"] = _r(ag.gwet_ac1(units, categories=q.choices))
        out["prop_yes"] = _r(sum(values) / len(values)) if values else None
    return out


def annotator_stats(annotations: list[dict], skips: dict, calibration: Sequence[str],
                    questions: Sequence[Question] = QUESTIONS) -> list[dict]:
    """Per-annotator workload and two agreement diagnostics.

    * loo_alpha_delta: mean over questions of (alpha without this annotator) - (alpha with
      everyone). A clearly positive value means the others agree better without them.
    * mean_kappa: their mean pairwise Cohen's kappa with the other annotators, averaged over questions.
    """
    users = sorted({a["username"] for a in annotations})
    by_q = ratings_by_question(annotations, questions=questions)
    base = {q.key: ag.krippendorff_alpha(_units(by_q[q.key]), q.level) for q in questions}
    pair_tables = {q.key: ag.pairwise_cohen(by_q[q.key], weights="quadratic" if q.kind == "likert" else None,
                                            categories=q.choices, min_overlap=MIN_PAIR_OVERLAP)
                   for q in questions}
    cal = set(calibration)
    rows = []
    for u in users:
        mine = [a for a in annotations if a["username"] == u]
        durations = [a["duration_s"] for a in mine if a.get("duration_s")]
        deltas, kappas = [], []
        for q in questions:
            without = {e: [v for r, v in per.items() if r != u] for e, per in by_q[q.key].items()}
            a_wo = ag.krippendorff_alpha(without, q.level)
            if a_wo is not None and base[q.key] is not None:
                deltas.append(a_wo - base[q.key])
            ks = [p["kappa"] for pair, p in pair_tables[q.key].items() if u in pair and p["kappa"] is not None]
            if ks:
                kappas.append(sum(ks) / len(ks))
        rows.append({
            "username": u, "rated": len(mine), "skipped": skips.get(u, 0),
            "calibration_done": sum(1 for a in mine if a["eval_id"] in cal), "calibration_total": len(cal),
            "median_seconds": _r(statistics.median(durations), 1) if durations else None,
            "loo_alpha_delta": _r(sum(deltas) / len(deltas)) if deltas else None,
            "mean_kappa": _r(sum(kappas) / len(kappas)) if kappas else None,
            "last_update": max((a["updated_at"] for a in mine), default=None),
        })
    return rows


def by_source(annotations: list[dict], store, span: Optional[dict] = None,
              questions: Sequence[Question] = QUESTIONS) -> list[dict]:
    """Mean rating (Likert) or share of 'yes' (binary) per source: for the admin only.

    With span ({question key: {"min", "max"}}), the cells of those questions also get "norm": the
    source mean min-max scaled from [min, max] onto the question's full range (1-5); None when min == max.
    """
    groups: dict = defaultdict(lambda: defaultdict(list))
    n_by_source: Counter = Counter()
    for a in annotations:
        poem = store.get(a["eval_id"])
        if poem is None:
            continue
        src = poem.hidden["source_dataset"]
        n_by_source[src] += 1
        for q in questions:
            v = a["answers"].get(q.key)
            if v is not None:
                groups[src][q.key].append(v)
    rows = []
    for src in sorted(groups):
        cells = {}
        for q in questions:
            vs = groups[src][q.key]
            cells[q.key] = {"value": _r(statistics.fmean(vs), 2) if vs else None, "n": len(vs)}
            if span is not None and q.key in span:
                lo, hi = span[q.key]["min"], span[q.key]["max"]
                bottom, top = q.choices[0], q.choices[-1]
                cells[q.key]["norm"] = (_r(bottom + (top - bottom) * (statistics.fmean(vs) - lo) / (hi - lo), 2)
                                        if vs and hi is not None and hi > lo else None)
        rows.append({"source": src, "n_annotations": n_by_source[src], "cells": cells})
    return rows


def by_source_by_annotator(annotations: list[dict], store, questions: Sequence[Question] = QUESTIONS) -> list[dict]:
    """by_source() for each annotator, with the 1-5 questions also min-max scaled: for the admin only.

    Per annotator and per 1-5 question, ratings are stretched from that annotator's own lowest and
    highest answer (over every poem they rated) onto the full 1-5 range, 1 + 4 * (x - min) / (max - min),
    so that the scores are comparable across annotators (answers 2-4: 2 -> 1, 3 -> 3, 4 -> 5). The map
    is linear, so a source's scaled mean is the map of its mean. None when min == max. Yes/no
    questions are left as they are.
    """
    mine: dict = defaultdict(list)
    for a in annotations:
        if store.get(a["eval_id"]) is not None:
            mine[a["username"]].append(a)
    out = []
    for u in sorted(mine):
        span = {}
        for q in questions:
            if q.kind == "likert":
                vs = [a["answers"][q.key] for a in mine[u] if a["answers"].get(q.key) is not None]
                span[q.key] = {"min": min(vs, default=None), "max": max(vs, default=None)}
        out.append({"username": u, "rows": by_source(mine[u], store, span=span, questions=questions), "span": span})
    return out


def agreement_report(annotations: list[dict], store, *, k: Optional[int], calibration: Sequence[str],
                     skips: Optional[dict] = None, n_boot: int = 0, seed: int = 0,
                     questions: Sequence[Question] = QUESTIONS, rubric_version: str = RUBRIC_VERSION) -> dict:
    by_q = ratings_by_question(annotations, questions=questions)
    cal = set(calibration)
    by_q_cal = ratings_by_question(annotations, subset=cal, questions=questions) if cal else None
    return {
        "study": {"dataset": store.meta.get("dataset"), "pool": store.meta.get("pool"), "poems": len(store),
                  "ratings_per_poem": "all" if k is None else k, "calibration_size": len(cal),
                  "rubric_version": rubric_version,
                  "annotators": len({a["username"] for a in annotations}), "annotations": len(annotations),
                  "bootstrap": n_boot},
        "questions": [question_stats(q, by_q[q.key], n_boot=n_boot, seed=seed) for q in questions],
        "calibration": [question_stats(q, by_q_cal[q.key], n_boot=n_boot, seed=seed) for q in questions] if cal else [],
        "annotators": annotator_stats(annotations, skips or {}, calibration, questions),
        "by_source": by_source(annotations, store, questions=questions),
        "by_source_by_annotator": by_source_by_annotator(annotations, store, questions),
    }


# -----------------------------------------------------------------------------
# exports
# -----------------------------------------------------------------------------
def export_fields(questions: Sequence[Question] = QUESTIONS) -> list[str]:
    return (["annotator", "eval_id", "meter", "source_dataset", "source_id", "author", "calibration"]
            + [q.key for q in questions]
            + ["comments", "duration_s", "revisions", "rubric_version", "created_at", "updated_at"])


EXPORT_FIELDS = export_fields()


def export_rows(annotations: Iterable[dict], store, calibration: Sequence[str],
                questions: Sequence[Question] = QUESTIONS) -> list[dict]:
    cal = set(calibration)
    rows = []
    for a in annotations:
        poem = store.get(a["eval_id"])
        hidden = poem.hidden if poem else {}
        row = {"annotator": a["username"], "eval_id": a["eval_id"], "meter": poem.meter if poem else "",
               "source_dataset": hidden.get("source_dataset", ""), "source_id": hidden.get("source_id", ""),
               "author": hidden.get("author", ""), "calibration": int(a["eval_id"] in cal)}
        for q in questions:
            v = a["answers"].get(q.key)
            row[q.key] = "" if v is None else v
        row.update({"comments": a.get("comments", ""), "duration_s": a.get("duration_s") or "",
                    "revisions": a.get("revisions"), "rubric_version": a.get("rubric_version"),
                    "created_at": a.get("created_at"), "updated_at": a.get("updated_at")})
        rows.append(row)
    return rows


def to_csv(rows: list[dict], questions: Sequence[Question] = QUESTIONS) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=export_fields(questions), extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def _fmt(x) -> str:
    if x is None:
        return "–"
    if isinstance(x, list):
        return f"[{_fmt(x[0])}, {_fmt(x[1])}]"
    return f"{x:.3f}" if isinstance(x, float) else str(x)


def to_markdown(report: dict) -> str:
    s = report["study"]
    lines = [f"# Human-evaluation agreement — {s['dataset']} ({s['pool']} pool)", "",
             f"{s['annotations']} annotations by {s['annotators']} annotators on {s['poems']} poems; "
             + ("every annotator rates every poem; " if s['ratings_per_poem'] == "all" else f"target {s['ratings_per_poem']} ratings per poem; ")
             + f"calibration set of {s['calibration_size']}; "
             f"rubric v{s['rubric_version']}.", ""]

    def table(title: str, rows: list[dict]) -> None:
        lines.extend([f"## {title}", "",
                      "| # | question | level | paired poems | α | α 95% CI | % agree | ±1 / AC1 | Fleiss κ | mean pairwise κ | mean / % yes |",
                      "|---|---|---|---|---|---|---|---|---|---|---|"])
        for r in rows:
            extra = r.get("within_one") if r["kind"] == "likert" else r.get("gwet_ac1")
            centre = r.get("mean") if r["kind"] == "likert" else r.get("prop_yes")
            lines.append(f"| {r['number']} | {r['text']} | {r['level']} | {r['n_paired_units']} | {_fmt(r['alpha'])} | "
                         f"{_fmt(r['alpha_ci'])} | {_fmt(r['pct_agreement'])} | {_fmt(extra)} | {_fmt(r.get('fleiss_kappa'))} | "
                         f"{_fmt(r['mean_pairwise_kappa'])} | {_fmt(centre)} |")
        lines.append("")

    table("All poems", report["questions"])
    if report["calibration"]:
        table("Calibration set (rated by every annotator)", report["calibration"])
    lines.extend(["## Annotators", "", "| annotator | rated | skipped | calibration | median s | LOO Δα | mean κ |",
                  "|---|---|---|---|---|---|---|"])
    for a in report["annotators"]:
        lines.append(f"| {a['username']} | {a['rated']} | {a['skipped']} | {a['calibration_done']}/{a['calibration_total']} | "
                     f"{_fmt(a['median_seconds'])} | {_fmt(a['loo_alpha_delta'])} | {_fmt(a['mean_kappa'])} |")
    lines.extend(["", "α: Krippendorff's alpha (ordinal for the 1–5 questions, nominal for yes/no). "
                  "±1: share of rater pairs within one point. AC1: Gwet's AC1. Pairwise κ: Cohen's kappa, "
                  "quadratic-weighted for 1–5 questions, over annotator pairs sharing ≥ 5 poems. "
                  "LOO Δα: mean change in α when the annotator is left out (positive = others agree better without them).", ""])
    return "\n".join(lines)


def main(argv=None) -> int:
    from .store import load_store
    here = Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Write the agreement report and the annotations CSV.")
    ap.add_argument("--study", choices=("1", "2"), default="1",
                    help="2: study 2's questions (with Q13 coherence), database and data unless given")
    ap.add_argument("--db", type=Path, help="default: instance/annotations.db (study 2: annotations_study2.db)")
    ap.add_argument("--data", type=Path, help="default: data/ (study 2: data_study2/)")
    ap.add_argument("--out", type=Path, default=here / "reports")
    ap.add_argument("--k", type=int, default=None, help="target ratings per poem (summary only; default: all)")
    ap.add_argument("--bootstrap", type=int, default=1000, help="bootstrap resamples for the α CIs (0 = off)")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    two = args.study == "2"
    args.db = args.db or here / "instance" / ("annotations_study2.db" if two else "annotations.db")
    args.data = args.data or here / ("data_study2" if two else "data")
    questions = STUDY2_QUESTIONS if two else QUESTIONS
    if not args.db.is_file():
        print(f"no database at {args.db}", file=sys.stderr)
        return 1
    store = load_store(args.data)
    conn = db.connect(args.db)
    try:
        annotations = db.all_annotations(conn)
        calibration = db.calibration_ids(conn)
        names = {r["id"]: r["username"] for r in db.list_annotators(conn)}
        skips = {names[i]: n for i, n in db.skip_counts(conn).items() if i in names}
    finally:
        conn.close()
    report = agreement_report(annotations, store, k=args.k, calibration=calibration, skips=skips,
                              n_boot=args.bootstrap, seed=args.seed, questions=questions,
                              rubric_version=STUDY2_RUBRIC_VERSION if two else RUBRIC_VERSION)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "agreement.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "agreement.md").write_text(to_markdown(report), encoding="utf-8")
    (args.out / "annotations.csv").write_text(
        to_csv(export_rows(annotations, store, calibration, questions), questions), encoding="utf-8")
    print(f"wrote agreement.json, agreement.md and annotations.csv ({len(annotations)} annotations) to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
