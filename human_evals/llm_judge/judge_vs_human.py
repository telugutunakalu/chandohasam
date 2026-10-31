#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
How the LLM judge agrees with the human annotators (study 1), by the admission test of the paper's App. "LLM-judge
validation": its scores must follow the annotator-centred human means at least as well as the annotators follow
each other.

    python3 judge_vs_human.py results/gemma4-26b_study1.jsonl [--study2 results/gemma4-26b_study2.jsonl]
        → results/<name>_vs_human.{md,json}

Human ratings: instance/annotations.db of the annotation app, opened read-only (current answers; a reset answer is
null and left out).
- **1–5 scales.** Centred rating = an annotator's rating − their own mean on that question over all their ratings.
  Human mean = the mean of the centred ratings a poem received. Judge ρ = Spearman(judge's score, human mean) over
  the poems with ≥ 2 raters. Human ρ = for each annotator, Spearman(their centred rating, the mean of the others'
  centred ratings) over the poems they share with ≥ 1 other; the median and range over annotators. The judge passes
  on a scale when its ρ ≥ the median human ρ. Also Krippendorff's α (ordinal) of the humans, and with the judge
  added as one more rater (raw scores).
- **Yes/no questions.** The judge against the human majority of a poem (ties left out): agreement and Cohen's κ;
  the humans' own pairwise agreement; the share of "yes".
- **By source:** the mean of each 1–5 scale and the AI-flag rate, humans (raw) and judge, per source; and the
  Gemini − poets difference on readability, comprehension and lexical (centred for humans).
- **Study 2** (optional): the judge's scores of each model's poems against its scores of their gold poems
  (hidden.metadata.gold_eval_id), paired, and its AI-flag rate per model; and, when study 2 has ratings
  (instance/annotations_study2.db, read-only), the same 1–5 and yes/no tests against them, by model. Study 2's Q13
  (coherence) is not asked of the judge, so it is not compared.
- **--raters a,b,c** (added 2026-10-30): only these annotators' ratings, in both studies (the user's rule: report
  the three annotators of group A only, ../annotation_app/state_analysis.GROUP_A). **--tag NAME** names the output results/<model>_vs_human_<NAME>.{md,json}.
  Without either flag the script gives the pilot's numbers unchanged.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sqlite3
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent / "annotation_app"
sys.path.insert(0, str(HERE))
import judge_prompt as jp                                            # noqa: E402

_spec = importlib.util.spec_from_file_location("agreement", APP / "padya_eval" / "agreement.py")
agreement = sys.modules["agreement"] = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agreement)

LIKERT = [q.key for q in jp.rubric.QUESTIONS if q.kind == "likert"]
BINARY = [q.key for q in jp.rubric.QUESTIONS if q.kind == "binary"]
POETS = {"bhagavatam", "vemana", "kuchimanchi"}             # study 1's source labels
GEMINI = "generated"                                             # Gemini's poems in study 1


def ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a: list[float], b: list[float]) -> float | None:
    if len(a) < 3:
        return None
    ra, rb = ranks(a), ranks(b)
    ma, mb = st.mean(ra), st.mean(rb)
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va, vb = sum((x - ma) ** 2 for x in ra), sum((y - mb) ** 2 for y in rb)
    return cov / (va * vb) ** 0.5 if va and vb else None


def human_ratings(db: str = "annotations.db", raters: set[str] | None = None) -> dict[str, dict[str, dict[int, int]]]:
    """question → eval_id → annotator → value (only the named raters, when given)."""
    con = sqlite3.connect(f"file:{APP / 'instance' / db}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT annotator_id, eval_id, answers FROM annotations").fetchall()
        users = dict(con.execute("SELECT id, username FROM annotators").fetchall())
    finally:
        con.close()
    out: dict = defaultdict(lambda: defaultdict(dict))
    for ann, eid, answers in rows:
        if raters is not None and users.get(ann) not in raters:
            continue
        for k, v in json.loads(answers).items():
            if v is not None:
                out[k][eid][ann] = v
    return out


def r3(x):
    return None if x is None else round(x, 3)


def likert_stats(q: str, human: dict, judge: dict) -> dict:
    per = {e: by for e, by in human[q].items() if e in judge}
    own = defaultdict(list)
    for eid, by in per.items():
        for a, v in by.items():
            own[a].append(v)
    centre = {a: st.mean(v) for a, v in own.items()}
    cen = {eid: {a: v - centre[a] for a, v in by.items()} for eid, by in per.items()}
    multi = [e for e in cen if len(cen[e]) >= 2 and e in judge and judge[e].get(q) is not None]
    rho_j = spearman([judge[e][q] for e in multi], [st.mean(cen[e].values()) for e in multi])
    loo = {}
    for a in centre:
        shared = [e for e in cen if a in cen[e] and len(cen[e]) >= 2]
        if len(shared) >= 10:
            loo[a] = spearman([cen[e][a] for e in shared],
                              [st.mean(v for b, v in cen[e].items() if b != a) for e in shared])
    hr = [v for v in loo.values() if v is not None]
    units = {e: list(by.values()) for e, by in per.items() if len(by) >= 2}
    with_j = {e: list(by.values()) + ([judge[e][q]] if e in judge and judge[e].get(q) is not None else [])
              for e, by in per.items() if e in judge}
    jd = [judge[e][q] for e in judge if judge[e].get(q) is not None]
    return {"poems_2plus": len(multi), "judge_rho": r3(rho_j), "human_rho_median": r3(st.median(hr)) if hr else None,
            "human_rho_range": [r3(min(hr)), r3(max(hr))] if hr else None, "human_rho_by_annotator": {
                str(a): r3(v) for a, v in loo.items()},
            "passes": None if rho_j is None or not hr else rho_j >= st.median(hr),
            "alpha_humans": r3(agreement.krippendorff_alpha(units, "ordinal")),
            "alpha_with_judge": r3(agreement.krippendorff_alpha(with_j, "ordinal")),
            "judge_counts": {v: jd.count(v) for v in (1, 2, 3, 4, 5)},
            "human_counts": {v: sum(list(by.values()).count(v) for e, by in per.items() if e in judge)
                             for v in (1, 2, 3, 4, 5)}}


def binary_stats(q: str, human: dict, judge: dict) -> dict:
    per = {e: by for e, by in human[q].items() if e in judge}
    a, b = [], []
    for e, by in per.items():
        if e not in judge or judge[e].get(q) is None:
            continue
        ones = sum(by.values())
        if ones * 2 == len(by):
            continue
        a.append(int(ones * 2 > len(by)))
        b.append(judge[e][q])
    pairs = [int(x == y) for e, by in per.items() for i, x in enumerate(by.values()) for y in list(by.values())[i + 1:]]
    hv = [v for e, by in per.items() if e in judge for v in by.values()]
    return {"poems": len(a), "agreement_with_majority": r3(sum(x == y for x, y in zip(a, b)) / len(a)) if a else None,
            "kappa": r3(agreement.cohen_kappa(a, b)) if a else None,
            "human_pairwise_agreement": r3(st.mean(pairs)) if pairs else None,
            "yes_human": r3(st.mean(hv)) if hv else None,
            "yes_judge": r3(st.mean(judge[e][q] for e in judge if judge[e].get(q) is not None))}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("study1", type=Path)
    ap.add_argument("--study2", type=Path)
    ap.add_argument("--raters", help="comma-separated usernames; only their ratings are used")
    ap.add_argument("--tag", help="output suffix: results/<model>_vs_human_<tag>.{md,json}")
    a = ap.parse_args()
    raters = set(a.raters.split(",")) if a.raters else None
    rows = [json.loads(l) for l in open(a.study1, encoding="utf-8")]
    judge = {r["eval_id"]: r["answers"] for r in rows if not r["errors"]}
    poems1, _ = jp.load(APP / "data")
    human = human_ratings(raters=raters)
    res = {"judge_file": a.study1.name, "model": rows[0]["model"] if rows else None, "poems": len(rows),
           "raters": sorted(raters) if raters else "all",
           "invalid": sum(bool(r["errors"]) for r in rows), "likert": {}, "binary": {}, "by_source": {}}
    for q in LIKERT:
        res["likert"][q] = likert_stats(q, human, judge)
    for q in BINARY:
        res["binary"][q] = binary_stats(q, human, judge)
    src = {e: poems1[e]["hidden"]["source_dataset"] for e in judge}
    for s in sorted(set(src.values())):
        ids = [e for e in judge if src[e] == s]
        row = {"poems": len(ids)}
        for q in LIKERT + ["ai_generated"]:
            hv = [v for e in ids for v in human[q].get(e, {}).values()]
            jv = [judge[e][q] for e in ids if judge[e].get(q) is not None]
            row[q] = {"human": r3(st.mean(hv)) if hv else None, "judge": r3(st.mean(jv)) if jv else None}
        res["by_source"][s] = row
    contrast = {}
    for q in ("readability", "comprehension", "lexical", "bhavam", "poetic"):
        own = defaultdict(list)
        for e, by in human[q].items():
            for ann, v in by.items():
                own[ann].append(v)
        centre = {ann: st.mean(v) for ann, v in own.items()}
        hc = {e: st.mean(v - centre[ann] for ann, v in by.items()) for e, by in human[q].items() if e in judge}
        g = [e for e in hc if src[e] == GEMINI]
        p = [e for e in hc if src[e] in POETS]
        if g and p:
            contrast[q] = {"human_centred": r3(st.mean(hc[e] for e in g) - st.mean(hc[e] for e in p)),
                           "judge": r3(st.mean(judge[e][q] for e in g) - st.mean(judge[e][q] for e in p))}
    res["gemini_minus_poets"] = contrast

    if a.study2 and a.study2.exists():
        poems2, _ = jp.load(APP / "data_study2")
        allj = {}
        for path in (a.study1, a.study2):
            for l in open(path, encoding="utf-8"):
                r = json.loads(l)
                if not r["errors"]:
                    allj[r["eval_id"]] = r["answers"]
        s2 = {}
        for e, p in poems2.items():
            md = p["hidden"]["metadata"]
            if e in allj and md["gold_eval_id"] in allj:
                s2.setdefault(md["model"], []).append((allj[e], allj[md["gold_eval_id"]]))
        res["study2"] = {m: {"pairs": len(v), **{q: {"model": r3(st.mean(x[q] for x, _ in v)),
                                                     "gold": r3(st.mean(y[q] for _, y in v))} for q in LIKERT},
                             "ai_flag": {"model": r3(st.mean(x["ai_generated"] for x, _ in v)),
                                         "gold": r3(st.mean(y["ai_generated"] for _, y in v))}}
                         for m, v in sorted(s2.items())}
        human2 = human_ratings("annotations_study2.db", raters)
        judge2 = {}
        for l in open(a.study2, encoding="utf-8"):
            r = json.loads(l)
            if not r["errors"]:
                judge2[r["eval_id"]] = r["answers"]
        if any(human2[q] for q in LIKERT):
            h2 = {"poems_rated": len({e for q in LIKERT for e in human2[q] if e in judge2}), "likert": {}, "binary": {},
                  "by_model": {}}
            for q in LIKERT:
                h2["likert"][q] = likert_stats(q, human2, judge2)
            for q in BINARY:
                h2["binary"][q] = binary_stats(q, human2, judge2)
            mdl = {e: poems2[e]["hidden"]["source_dataset"] for e in judge2 if e in poems2}
            for m in sorted(set(mdl.values())):
                ids = [e for e in judge2 if mdl.get(e) == m]
                row = {"poems": len(ids), "rated": len([e for e in ids if any(e in human2[q] for q in LIKERT)])}
                for q in LIKERT + ["ai_generated"]:
                    hv = [v for e in ids for v in human2[q].get(e, {}).values()]
                    jv = [judge2[e][q] for e in ids if judge2[e].get(q) is not None]
                    row[q] = {"human": r3(st.mean(hv)) if hv else None, "judge": r3(st.mean(jv)) if jv else None}
                h2["by_model"][m] = row
            res["study2_humans"] = h2

    stem = a.study1.stem.removesuffix("_study1")
    out = f"{stem}_vs_human" + (f"_{a.tag}" if a.tag else "")
    (a.study1.parent / f"{out}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                                                           encoding="utf-8")
    md = [f"# LLM judge ({res['model']}) against the human annotators", "",
          f"{res['poems']} study-1 poems judged ({res['invalid']} invalid replies left out); human raters: "
          f"{', '.join(res['raters']) if raters else 'all annotators'}; method: judge_vs_human.py.",
          "", "## 1–5 scales", "",
          "| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | "
          "α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |", "|---|---|---|---|---|---|---|---|---|"]
    for q, s in res["likert"].items():
        rng = s["human_rho_range"] or [None, None]
        md.append(f"| {q} | {s['poems_2plus']} | {s['judge_rho']} | {s['human_rho_median']} ({rng[0]} to {rng[1]}) | "
                  f"{'yes' if s['passes'] else 'no'} | {s['alpha_humans']} | {s['alpha_with_judge']} | "
                  f"{'/'.join(str(s['judge_counts'][v]) for v in (1, 2, 3, 4, 5))} | "
                  f"{'/'.join(str(s['human_counts'][v]) for v in (1, 2, 3, 4, 5))} |")
    md += ["", "## Yes/no questions", "", "| question | poems | judge = human majority | κ | humans' pairwise "
           "agreement | yes: humans | yes: judge |", "|---|---|---|---|---|---|---|"]
    for q, s in res["binary"].items():
        md.append(f"| {q} | {s['poems']} | {s['agreement_with_majority']} | {s['kappa']} | "
                  f"{s['human_pairwise_agreement']} | {s['yes_human']} | {s['yes_judge']} |")
    md += ["", "## By source (means; humans raw)", "", "| source | poems | " + " | ".join(
        f"{q} H / J" for q in LIKERT) + " | AI flag H / J |", "|---|---|" + "---|" * (len(LIKERT) + 1)]
    for s, row in res["by_source"].items():
        md.append(f"| {s} | {row['poems']} | " + " | ".join(
            f"{row[q]['human']} / {row[q]['judge']}" for q in LIKERT + ["ai_generated"]) + " |")
    md += ["", "Gemini − poets: " + "; ".join(f"{q}: humans (centred) {v['human_centred']:+.2f}, judge "
                                              f"{v['judge']:+.2f}" for q, v in contrast.items())]
    if res.get("study2"):
        md += ["", "## Study 2: the judge on each model's poems against their gold poems", "",
               "| model | pairs | " + " | ".join(f"{q} model / gold" for q in LIKERT) + " | AI flag model / gold |",
               "|---|---|" + "---|" * (len(LIKERT) + 1)]
        for m, s in res["study2"].items():
            md.append(f"| {m} | {s['pairs']} | " + " | ".join(f"{s[q]['model']} / {s[q]['gold']}" for q in LIKERT)
                      + f" | {s['ai_flag']['model']} / {s['ai_flag']['gold']} |")
    if res.get("study2_humans"):
        h2 = res["study2_humans"]
        md += ["", "## Study 2: the judge against the human ratings", "",
               f"{h2['poems_rated']} of the judged study-2 poems have ratings from these raters. Q13 (coherence) is "
               "not asked of the judge.", "",
               "| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | "
               "α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |", "|---|---|---|---|---|---|---|---|---|"]
        for q, s in h2["likert"].items():
            rng = s["human_rho_range"] or [None, None]
            md.append(f"| {q} | {s['poems_2plus']} | {s['judge_rho']} | {s['human_rho_median']} ({rng[0]} to {rng[1]}) | "
                      f"{'–' if s['passes'] is None else ('yes' if s['passes'] else 'no')} | {s['alpha_humans']} | "
                      f"{s['alpha_with_judge']} | {'/'.join(str(s['judge_counts'][v]) for v in (1, 2, 3, 4, 5))} | "
                      f"{'/'.join(str(s['human_counts'][v]) for v in (1, 2, 3, 4, 5))} |")
        md += ["", "| question | poems | judge = human majority | κ | humans' pairwise agreement | yes: humans | yes: judge |",
               "|---|---|---|---|---|---|---|"]
        for q, s in h2["binary"].items():
            md.append(f"| {q} | {s['poems']} | {s['agreement_with_majority']} | {s['kappa']} | "
                      f"{s['human_pairwise_agreement']} | {s['yes_human']} | {s['yes_judge']} |")
        md += ["", "| model | poems | rated | " + " | ".join(f"{q} H / J" for q in LIKERT) + " | AI flag H / J |",
               "|---|---|---|" + "---|" * (len(LIKERT) + 1)]
        for m, row in h2["by_model"].items():
            md.append(f"| {m} | {row['poems']} | {row['rated']} | " + " | ".join(
                f"{row[q]['human']} / {row[q]['judge']}" for q in LIKERT + ["ai_generated"]) + " |")
    (a.study1.parent / f"{out}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
