#!/usr/bin/env python3
"""Where the study stands: agreement, and what the ratings can support, on every rating so far.

    .venv/bin/python state_analysis.py          # → reports/state/analysis.md and analysis.json

The live database is opened read-only and copied with SQLite's backup API; nothing in it changes. On the copy:
- data: ratings per annotator, poems by number of raters, rubric versions;
- agreement: padya_eval.report (Krippendorff's α with bootstrap CIs, agreement shares, κ, AC1), and for the 1–5
  questions the exact and ±1 agreement expected by chance from the pooled answers;
- consistency: α counts differences in scale use (leniency) as disagreement, so beside it: the mean pairwise
  Spearman ρ, the interval α after removing each annotator's own mean, and the Spearman–Brown reliability of the mean
  of 3 and of 5 ratings;
- annotators: each one's mean on the 1–5 questions, and the share of their most frequent answer (straight-lining:
  ≥ 90% one answer over ≥ 20 ratings), with α recomputed without the straight-lined answers;
- sources: Gemini-generated and textbook poems against the real poets (bhāgavatam, vemana, kuchimanchi), each
  annotator's mean removed, bootstrap over poems; yes-rates per source for register and ai_generated (Wilson 95%);
  AI detection per annotator (Gemini poems flagged, other poems flagged) and per poem (flagged by any / by a majority);
- Q4 re-rating: A3's and A5's Q4 answers were cleared on 2026-10-29 (old rows in annotation_history) for a
  fresh pass; their old answer against the new one on every poem re-rated so far, and how close each is to the others;
- ablation: annotator groups A (A1, A3, A5) and B (A2, A4), leave-one-annotator-out, and the poems
  rated by every annotator: α per question, and Gemini − real poets on the 1–5 questions in three views (as rated;
  each annotator's mean removed; min–max scaled per annotator onto 1–5, as on the admin dashboard), bootstrap over
  poems; per source group, each group's mean and the rank correlation of A's and B's poem means.

Each run also keeps a dated copy in reports/state/history/, so runs can be compared.
"""
from __future__ import annotations

import collections
import itertools
import json
import math
import random
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path

from padya_eval import agreement as ag
from padya_eval import db
from padya_eval.report import agreement_report, export_rows
from padya_eval.rubric import QUESTIONS
from padya_eval.store import load_store

HERE = Path(__file__).resolve().parent
OUT = HERE / "reports" / "state"
LIKERT = [q.key for q in QUESTIONS if q.kind == "likert"]
REAL = {"bhagavatam", "vemana", "kuchimanchi"}
GROUPS = ["real poets", "textbook reference", "generated (Gemini)"]
N_BOOT_ALPHA, N_BOOT_GROUPS, MIN_COMMON = 2000, 5000, 15
STRAIGHT_SHARE, STRAIGHT_MIN_N = 0.9, 20
GROUP_A_CODES, GROUP_B_CODES = ("A1", "A3", "A5"), ("A2", "A4")     # annotator codes, not names (2026-10-31)
def _usernames(codes: tuple[str, ...]) -> tuple[str, ...]:
    """The usernames behind annotator codes: instance/pseudonyms.json (gitignored; written by ../publish_results.py)."""
    path = HERE / "instance" / "pseudonyms.json"
    if not path.exists():
        raise SystemExit(f"{path} is missing: run ../publish_results.py once to write it")
    by_code = {c: u for u, c in json.loads(path.read_text(encoding="utf-8")).items()}
    return tuple(sorted(by_code[c] for c in codes))


GROUP_A, GROUP_B = _usernames(GROUP_A_CODES), _usernames(GROUP_B_CODES)
Q4_RESET_AT = "2026-10-29T07:34:03+00:00"      # archived_at of the Q4 answers cleared for the re-rating
VIEWS = ("as rated", "centred", "min–max")
N_BOOT_ABLATION = 2000


def group(source: str) -> str:
    return "real poets" if source in REAL else ("generated (Gemini)" if source == "generated" else "textbook reference")


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else None


def ranks(xs: list[float]) -> list[float]:
    order = sorted(range(len(xs)), key=xs.__getitem__)
    out = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for t in range(i, j + 1):
            out[order[t]] = (i + j) / 2
        i = j + 1
    return out


def pearson(a: list[float], b: list[float]):
    ma, mb = mean(a), mean(b)
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    return None if sa == 0 or sb == 0 else sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb)


def wilson(k: int, n: int, z: float = 1.96):
    if n == 0:
        return None, None
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def quartiles(xs: list[float]):
    xs = sorted(xs)
    return (xs[len(xs) // 4], statistics.median(xs), xs[3 * len(xs) // 4]) if xs else None


def units_of(val_k: dict, users=None, poems=None) -> dict:
    """{poem: [values]} of one question, restricted to some annotators and/or poems."""
    units = collections.defaultdict(list)
    for (u, e), v in val_k.items():
        if (users is None or u in users) and (poems is None or e in poems):
            units[e].append(v)
    return dict(units)


def contrast(per_poem: dict, poem_group: dict, g: str, rng: random.Random, n_boot: int):
    """Mean over the poems of group g minus the mean over the real poets' poems; 95% bootstrap over poems."""
    x = [m for e, m in per_poem.items() if poem_group[e] == g]
    y = [m for e, m in per_poem.items() if poem_group[e] == "real poets"]
    if len(x) < 3 or len(y) < 3:
        return None
    boot = sorted(mean(rng.choices(x, k=len(x))) - mean(rng.choices(y, k=len(y))) for _ in range(n_boot))
    lo, hi = boot[int(0.025 * n_boot)], boot[int(0.975 * n_boot) - 1]
    return {"diff": mean(x) - mean(y), "lo": lo, "hi": hi, "poems": [len(x), len(y)], "excludes_zero": lo > 0 or hi < 0}


def copy_database(tmp: Path) -> Path:
    copy = tmp / "annotations_state.db"
    src = sqlite3.connect(f"file:{HERE / 'instance' / 'annotations.db'}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    src.close()
    dst.close()
    return copy


def main() -> None:
    store = load_store(HERE / "data")
    with tempfile.TemporaryDirectory() as tmp:
        conn = db.connect(copy_database(Path(tmp)))
        anns = db.all_annotations(conn)
        calibration = [r[0] for r in conn.execute("SELECT eval_id FROM calibration ORDER BY position")]
        q4_before = {(r[0], r[1]): json.loads(r[2]).get("bhavam") for r in conn.execute(
            """SELECT n.username, h.eval_id, h.answers FROM annotation_history h
               JOIN annotators n ON n.id = h.annotator_id WHERE h.archived_at = ?""", (Q4_RESET_AT,))}
        conn.close()

    users = sorted({a["username"] for a in anns})
    by_poem = collections.Counter(a["eval_id"] for a in anns)
    data = {"ratings": len(anns), "latest": max(a["updated_at"] for a in anns),
            "per_annotator": {u: sum(a["username"] == u for a in anns) for u in users},
            "calibration_done": {u: sum(a["username"] == u and a["eval_id"] in set(calibration) for a in anns)
                                 for u in users},
            "poems_rated": len(by_poem),
            "poems_by_raters": dict(sorted(collections.Counter(by_poem.values()).items())),
            "rubric_versions": dict(collections.Counter(str(a["rubric_version"]) for a in anns)),
            "q4_rerating": {u: {"answered": sum(a["username"] == u and a["answers"].get("bhavam") is not None
                                                for a in anns),
                                "ratings": sum(a["username"] == u for a in anns)}
                            for u in sorted({u for u, _ in q4_before})}}

    # --- agreement (the dashboard's statistics) ----------------------------------------------------------------------
    report = agreement_report(anns, store, k=None, calibration=calibration, n_boot=N_BOOT_ALPHA)
    qstats = {q["key"]: q for q in report["questions"]}
    for k in LIKERT:
        dist = {int(c): n for c, n in qstats[k]["distribution"].items()}
        tot = sum(dist.values())
        p = {c: n / tot for c, n in dist.items()}
        qstats[k]["chance_exact"] = sum(v * v for v in p.values())
        qstats[k]["chance_within_one"] = sum(p[i] * p[j] for i in p for j in p if abs(i - j) <= 1)

    # --- values per (annotator, poem) --------------------------------------------------------------------------------
    val = {q.key: {} for q in QUESTIONS}
    for a in anns:
        for q in QUESTIONS:
            v = a["answers"].get(q.key)
            if v is not None:
                val[q.key][(a["username"], a["eval_id"])] = float(v)
    umean = {(u, k): mean(v for (x, _), v in val[k].items() if x == u) for u in users for k in LIKERT}
    span = {(u, k): (min(vs), max(vs)) for u in users for k in LIKERT
            for vs in [[v for (x, _), v in val[k].items() if x == u]] if vs}

    def view_value(view: str, u: str, k: str, v: float):
        if view == "as rated":
            return v
        if view == "centred":
            return v - umean[(u, k)]
        lo, hi = span[(u, k)]                 # min–max onto 1–5; no range (one answer throughout) → left out
        return 1 + 4 * (v - lo) / (hi - lo) if hi > lo else None

    def poem_means(k: str, view: str, users_in=None, poems_in=None) -> dict:
        per = collections.defaultdict(list)
        for (u, e), v in val[k].items():
            if (users_in is None or u in users_in) and (poems_in is None or e in poems_in):
                x = view_value(view, u, k, v)
                if x is not None:
                    per[e].append(x)
        return {e: mean(xs) for e, xs in per.items()}

    # --- consistency beside α ----------------------------------------------------------------------------------------
    consistency = {}
    for k in LIKERT:
        rhos = []
        for u, w in itertools.combinations(users, 2):
            common = sorted({e for (x, e) in val[k] if x == u} & {e for (x, e) in val[k] if x == w})
            if len(common) >= MIN_COMMON:
                r = pearson(ranks([val[k][(u, e)] for e in common]), ranks([val[k][(w, e)] for e in common]))
                if r is not None:
                    rhos.append(r)
        centred = collections.defaultdict(list)
        for (u, e), v in val[k].items():
            centred[e].append(v - umean[(u, k)])
        a = qstats[k]["alpha"]
        consistency[k] = {
            "alpha_ordinal": a, "alpha_interval": qstats[k].get("alpha_interval"),
            "alpha_interval_centred": ag.krippendorff_alpha(dict(centred), "interval"),
            "mean_spearman": mean(rhos), "spearman_pairs": len(rhos),
            "reliability_mean_of_3": None if a is None else 3 * a / (1 + 2 * a),
            "reliability_mean_of_5": None if a is None else 5 * a / (1 + 4 * a)}

    # --- annotators: leniency and straight-lining --------------------------------------------------------------------
    annotators, straight = {}, set()
    for u in users:
        row = {}
        for k in LIKERT:
            vs = [v for (x, _), v in val[k].items() if x == u]
            top, n_top = collections.Counter(vs).most_common(1)[0] if vs else (None, 0)
            share = n_top / len(vs) if vs else None
            flagged = bool(vs) and len(vs) >= STRAIGHT_MIN_N and share >= STRAIGHT_SHARE
            if flagged:
                straight.add((u, k))
            row[k] = {"mean": mean(vs), "n": len(vs), "modal": top, "modal_share": share, "straight": flagged}
        annotators[u] = row
    without_straight = {}
    for k in LIKERT:
        units = collections.defaultdict(list)
        for (u, e), v in val[k].items():
            if (u, k) not in straight:
                units[e].append(v)
        without_straight[k] = ag.krippendorff_alpha(dict(units), "ordinal")

    # --- sources -----------------------------------------------------------------------------------------------------
    poem_group = {r["eval_id"]: group(r["source_dataset"]) for r in export_rows(anns, store, calibration)}
    rng = random.Random(7)
    contrasts = {}
    for g in ("generated (Gemini)", "textbook reference"):
        contrasts[g] = {}
        for k in LIKERT:
            c = contrast(poem_means(k, "centred"), poem_group, g, rng, N_BOOT_GROUPS)
            if c is not None:
                contrasts[g][k] = c
    yes_rates = {}
    for k in ("register", "ai_generated", "chandassu", "prasa", "yati", "shabdalankara", "arthalankara"):
        yes_rates[k] = {}
        for g in GROUPS:
            vs = [v for (_, e), v in val[k].items() if poem_group[e] == g]
            lo, hi = wilson(int(sum(vs)), len(vs))
            yes_rates[k][g] = {"yes": int(sum(vs)), "n": len(vs), "rate": mean(vs), "lo": lo, "hi": hi}
    poems_per_group = dict(collections.Counter(poem_group[e] for e in by_poem))
    gen = "generated (Gemini)"
    ai_by_annotator = {}
    for u in users:
        mine = [(e, v) for (x, e), v in val["ai_generated"].items() if x == u]
        ai_by_annotator[u] = {"generated_flagged": int(sum(v for e, v in mine if poem_group[e] == gen)),
                              "generated_rated": sum(poem_group[e] == gen for e, _ in mine),
                              "others_flagged": int(sum(v for e, v in mine if poem_group[e] != gen)),
                              "others_rated": sum(poem_group[e] != gen for e, _ in mine)}
    per_gen = collections.defaultdict(list)
    for (_, e), v in val["ai_generated"].items():
        if poem_group[e] == gen:
            per_gen[e].append(v)
    ai_poems = {"rated": len(per_gen), "flagged_by_any": sum(any(v) for v in per_gen.values()),
                "flagged_by_majority": sum(sum(v) > len(v) / 2 for v in per_gen.values())}
    ai_by_group = {name: {f: sum(ai_by_annotator[u][f] for u in members if u in ai_by_annotator)
                          for f in ("generated_flagged", "generated_rated", "others_flagged", "others_rated")}
                   for name, members in (("A", GROUP_A), ("B", GROUP_B))}
    timing = {u: quartiles([a["duration_s"] for a in anns if a["username"] == u and a.get("duration_s")]) for u in users}

    # --- Q4 re-rating: old answer (archived when cleared) against the new one ----------------------------------------
    reset_users = sorted({u for u, _ in q4_before})
    kept = set(users) - set(reset_users)              # annotators whose Q4 answers were not cleared
    q4_retest = {}
    for u in reset_users:
        poems = sorted(e for (x, e), old in q4_before.items() if x == u and old is not None and (u, e) in val["bhavam"])
        if not poems:
            continue
        old = [float(q4_before[(u, e)]) for e in poems]
        new = [val["bhavam"][(u, e)] for e in poems]
        others = {e: [v for (x, p), v in val["bhavam"].items() if p == e and x in kept] for e in poems}
        with_others = [e for e in poems if others[e]]
        dist = lambda vals: mean(abs(v - mean(others[e])) for e, v in zip(poems, vals) if others[e])  # noqa: E731
        alpha_with = lambda vals: ag.krippendorff_alpha(                                                # noqa: E731
            {e: others[e] + [v] for e, v in zip(poems, vals) if others[e]}, "ordinal")
        q4_retest[u] = {
            "poems": len(poems), "same": sum(a == b for a, b in zip(old, new)) / len(poems),
            "within_one": sum(abs(a - b) <= 1 for a, b in zip(old, new)) / len(poems),
            "mean_old": mean(old), "mean_new": mean(new), "mean_change": mean(new) - mean(old),
            "kappa_quadratic": ag.cohen_kappa(old, new, weights="quadratic", categories=[1, 2, 3, 4, 5]),
            "spearman": pearson(ranks(old), ranks(new)),
            "poems_with_others": len(with_others), "others": sorted(kept),
            "dist_to_others_old": dist(old), "dist_to_others_new": dist(new),
            "alpha_with_others_old": alpha_with(old), "alpha_with_others_new": alpha_with(new),
            "transitions": {f"{int(a)}→{int(b)}": n for (a, b), n in sorted(collections.Counter(zip(old, new)).items())}}

    # --- ablation: annotator groups, leave-one-out, poems rated by everyone ------------------------------------------
    crossed = {e for e, n in by_poem.items() if n == len(users)}
    subsets = {"all": (None, None), "A": (set(GROUP_A), None), "B": (set(GROUP_B), None)}
    subsets.update({f"without {u}": (set(users) - {u}, None) for u in users})
    subsets["all, crossed poems"] = (None, crossed)
    ablation_alpha, ablation_paired = {}, {}
    for name, (us, ps) in subsets.items():
        ablation_alpha[name], ablation_paired[name] = {}, {}
        for q in QUESTIONS:
            units = units_of(val[q.key], us, ps)
            ablation_alpha[name][q.key] = ag.krippendorff_alpha(units, q.level)
            ablation_paired[name][q.key] = sum(len(v) >= 2 for v in units.values())
    rng_ab = random.Random(11)
    ablation_gap = {name: {view: {k: contrast(poem_means(k, view, us, ps), poem_group, gen, rng_ab, N_BOOT_ABLATION)
                                  for k in LIKERT} for view in VIEWS}
                    for name, (us, ps) in subsets.items()}
    group_levels = {}
    for q in QUESTIONS:
        row = {name: {g: mean(v for (u, e), v in val[q.key].items()
                              if (subsets[name][0] is None or u in subsets[name][0]) and poem_group[e] == g)
                      for g in GROUPS} for name in ("all", "A", "B")}
        pa, pb = poem_means(q.key, "as rated", set(GROUP_A)), poem_means(q.key, "as rated", set(GROUP_B))
        common = sorted(set(pa) & set(pb))
        row["rho_AB"] = (pearson(ranks([pa[e] for e in common]), ranks([pb[e] for e in common]))
                         if len(common) >= MIN_COMMON else None)
        row["poems_AB"] = len(common)
        group_levels[q.key] = row

    res = {"created": time.strftime("%Y-%m-%d %H:%M"), "data": data, "poems_per_group": poems_per_group,
           "agreement": report["questions"], "agreement_calibration": report["calibration"],
           "annotator_diagnostics": report["annotators"], "consistency": consistency, "annotators": annotators,
           "straight_lined": sorted(f"{u}:{k}" for u, k in straight), "alpha_without_straight_lined": without_straight,
           "contrasts_vs_real_poets": contrasts, "yes_rates": yes_rates,
           "ai_by_annotator": ai_by_annotator, "ai_generated_poems": ai_poems, "ai_by_group": ai_by_group,
           "timing_seconds": timing, "groups": {"A": GROUP_A, "B": GROUP_B}, "q4_retest": q4_retest,
           "crossed_poems": len(crossed), "ablation_alpha": ablation_alpha, "ablation_paired": ablation_paired,
           "ablation_gap_generated_vs_real": ablation_gap, "group_levels": group_levels}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "analysis.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = to_markdown(res, qstats)
    (OUT / "analysis.md").write_text(md, encoding="utf-8")
    history = OUT / "history"
    history.mkdir(exist_ok=True)
    stamp = time.strftime("%Y-%m-%d_%H%M")
    (history / f"analysis_{stamp}.md").write_text(md, encoding="utf-8")
    (history / f"analysis_{stamp}.json").write_text((OUT / "analysis.json").read_text(encoding="utf-8"), encoding="utf-8")
    print(md)


def to_markdown(res: dict, qstats: dict) -> str:
    f = lambda x, d=3: "–" if x is None else f"{x:.{d}f}"                               # noqa: E731
    pct = lambda x: "–" if x is None else f"{100 * x:.1f}%"                             # noqa: E731
    d = res["data"]
    md = [f"# Human evaluation: state of the ratings as of {res['created']}", "",
          f"{d['ratings']} ratings (latest {d['latest'][:16].replace('T', ' ')} UTC) on {d['poems_rated']} poems "
          f"({', '.join(f'{n} {g}' for g, n in res['poems_per_group'].items())}). Rubric versions: "
          f"{', '.join(f'v{v}: {n}' for v, n in d['rubric_versions'].items())} (Q11–12 exist only in v2).", "",
          "| annotator | ratings | calibration (of 25) |", "|---|---|---|"]
    md += [f"| {u} | {n} | {d['calibration_done'][u]} |" for u, n in d["per_annotator"].items()]
    md += ["", "Poems by number of raters: " + ", ".join(f"{k} → {v}" for k, v in d["poems_by_raters"].items()), ""]
    if d.get("q4_rerating"):
        md += ["**Q4 (bhavam) is provisional:** the Q4 answers of " + ", ".join(
            f"{u} ({r['answered']}/{r['ratings']} re-rated so far)" for u, r in d["q4_rerating"].items())
            + " were cleared on 2026-10-29 for a fresh pass; until they finish, Q4 rests mostly on the other annotators. "
            "Their old answers are compared with the new ones below.", ""]
    md += ["## Agreement (all poems)", "",
           "α: Krippendorff (ordinal for 1–5, nominal for yes/no), 95% bootstrap CI. For 1–5 questions the chance "
           "columns give the agreement two answers drawn from the pooled distribution would reach.", "",
           "| # | question | poems ≥2 | α | 95% CI | % agree | chance | ±1 / AC1 | chance ±1 | pairwise κ | mean / % yes |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for q in res["agreement"]:
        lik = q["kind"] == "likert"
        ci = q.get("alpha_ci")
        s = qstats[q["key"]]
        md.append(f"| {q['number']} | {q['key']} | {q['n_paired_units']} | {f(q['alpha'])} | "
                  f"{f'{f(ci[0])} – {f(ci[1])}' if ci else '–'} | {f(q['pct_agreement'])} | "
                  f"{f(s.get('chance_exact')) if lik else ''} | {f(q['within_one'] if lik else q.get('gwet_ac1'))} | "
                  f"{f(s.get('chance_within_one')) if lik else ''} | {f(q.get('mean_pairwise_kappa'))} | "
                  f"{f(q.get('mean'), 2) if lik else f(q.get('prop_yes'))} |")
    md += ["", "## Consistency beside α (1–5 questions)", "",
           "α counts a lenient and a harsh annotator who order the poems the same way as disagreeing. Spearman ρ: mean "
           f"over annotator pairs sharing ≥ {MIN_COMMON} poems. Centred α: interval α after removing each annotator's "
           "own mean. Mean of 3 / 5: Spearman–Brown reliability of the averaged rating, from the ordinal α.", "",
           "| question | α ordinal | α interval | α interval, centred | Spearman ρ (pairs) | mean of 3 | mean of 5 | α without straight-lined answers |",
           "|---|---|---|---|---|---|---|---|"]
    for k, c in res["consistency"].items():
        md.append(f"| {k} | {f(c['alpha_ordinal'])} | {f(c['alpha_interval'])} | {f(c['alpha_interval_centred'])} | "
                  f"{f(c['mean_spearman'])} ({c['spearman_pairs']}) | {f(c['reliability_mean_of_3'], 2)} | "
                  f"{f(c['reliability_mean_of_5'], 2)} | {f(res['alpha_without_straight_lined'][k])} |")
    md += ["", "## Annotators", "",
           f"Mean answer per 1–5 question; ⚑ = straight-lined (≥ {STRAIGHT_SHARE:.0%} one answer over ≥ "
           f"{STRAIGHT_MIN_N} ratings). LOO Δα: change in α when the annotator is left out (positive = the others agree "
           "better without them).", "",
           "| annotator | group | " + " | ".join(LIKERT) + " | LOO Δα | mean κ | s / poem: median [IQR] |",
           "|---|---|" + "---|" * (len(LIKERT) + 3)]
    diag = {a["username"]: a for a in res["annotator_diagnostics"]}
    member = {u: g for g, us in res["groups"].items() for u in us}
    for u, row in res["annotators"].items():
        cells = [f"{f(row[k]['mean'], 2)}{' ⚑ ' + pct(row[k]['modal_share']) + ' ' + str(int(row[k]['modal'])) + 's' if row[k]['straight'] else ''}"
                 for k in LIKERT]
        a = diag.get(u, {})
        t = res["timing_seconds"].get(u)
        md.append(f"| {u} | {member.get(u, '')} | " + " | ".join(cells) + f" | {f(a.get('loo_alpha_delta'))} | "
                  f"{f(a.get('mean_kappa'))} | {f'{t[1]:.0f} [{t[0]:.0f}–{t[2]:.0f}]' if t else '–'} |")
    if res.get("q4_retest"):
        md += ["", "Times add up over revisions, so the Q4 re-rating adds to "
               + " and ".join(f"{u}'s" for u in res["q4_retest"]) + "."]
    md += ["", "## Sources against the real poets", "",
           "Each annotator's own mean removed; poem means compared; 95% bootstrap over poems. * = interval excludes 0.", "",
           "| question | " + " | ".join(f"{g} − real poets" for g in res["contrasts_vs_real_poets"]) + " |",
           "|---|" + "---|" * len(res["contrasts_vs_real_poets"])]
    for k in LIKERT:
        cells = []
        for g, row in res["contrasts_vs_real_poets"].items():
            c = row.get(k)
            cells.append("–" if c is None else f"{c['diff']:+.2f} [{c['lo']:+.2f}, {c['hi']:+.2f}]{' *' if c['excludes_zero'] else ''}")
        md.append(f"| {k} | " + " | ".join(cells) + " |")
    md += ["", "Yes-rates per source (all ratings; Wilson 95%; ratings of one poem are not independent, so the "
           "intervals are optimistic):", "", "| question | " + " | ".join(GROUPS) + " |", "|---|" + "---|" * len(GROUPS)]
    for k, row in res["yes_rates"].items():
        md.append(f"| {k} | " + " | ".join(
            f"{c['yes']}/{c['n']} = {pct(c['rate'])} [{pct(c['lo'])}, {pct(c['hi'])}]" if c["n"] else "–"
            for c in (row[g] for g in GROUPS)) + " |")
    gp = res["ai_generated_poems"]
    md += ["", f"AI detection: of the {gp['rated']} Gemini poems with an answer, {gp['flagged_by_any']} were flagged by "
           f"at least one annotator and {gp['flagged_by_majority']} by a majority of their raters.", "",
           "| annotator | Gemini poems flagged | other poems flagged |", "|---|---|---|"]
    for u, a in res["ai_by_annotator"].items():
        md.append(f"| {u} | {a['generated_flagged']}/{a['generated_rated']} | {a['others_flagged']}/{a['others_rated']} |")
    for g, a in res["ai_by_group"].items():
        md.append(f"| **group {g}** | {a['generated_flagged']}/{a['generated_rated']} = "
                  f"{pct(a['generated_flagged'] / a['generated_rated'] if a['generated_rated'] else None)} | "
                  f"{a['others_flagged']}/{a['others_rated']} = "
                  f"{pct(a['others_flagged'] / a['others_rated'] if a['others_rated'] else None)} |")

    if res["q4_retest"]:
        md += ["", "## Q4 re-rating: old answer against the new one", "",
               "Every poem re-rated so far. Others = the annotators whose Q4 answers were not cleared ("
               + ", ".join(next(iter(res["q4_retest"].values()))["others"]) + "); distance = mean |answer − others' "
               "mean|; α = ordinal α of the others plus this annotator, on these poems, with the old and with the new answer.", "",
               "| annotator | poems | same | ±1 | mean old → new | κ quadratic | Spearman | distance to others old → new | α with others old → new |",
               "|---|---|---|---|---|---|---|---|---|"]
        for u, r in res["q4_retest"].items():
            md.append(f"| {u} | {r['poems']} | {pct(r['same'])} | {pct(r['within_one'])} | {f(r['mean_old'], 2)} → "
                      f"{f(r['mean_new'], 2)} | {f(r['kappa_quadratic'])} | {f(r['spearman'])} | "
                      f"{f(r['dist_to_others_old'], 2)} → {f(r['dist_to_others_new'], 2)} | "
                      f"{f(r['alpha_with_others_old'])} → {f(r['alpha_with_others_new'])} |")
        md += ["", "Old → new answers: " + "; ".join(
            f"{u}: " + ", ".join(f"{t} ×{n}" for t, n in r["transitions"].items() if t[0] != t[-1])
            for u, r in res["q4_retest"].items()) + " (unchanged answers left out)."]

    A, B = ", ".join(res["groups"]["A"]), ", ".join(res["groups"]["B"])
    names = list(res["ablation_alpha"])
    label = lambda n: {"all": "all 5", "A": "A", "B": "B", "all, crossed poems": f"all 5, {res['crossed_poems']} crossed"}.get(  # noqa: E731
        n, n.replace("without ", "−"))
    md += ["", "## Ablation: annotator groups, leave-one-out, crossed poems", "",
           f"Group A = {A}; group B = {B}. −x = everyone but x. Crossed = the {res['crossed_poems']} poems every "
           "annotator has rated (Q4 is not fully crossed while the re-rating runs).", "",
           "**Krippendorff's α per question** (ordinal for 1–5, nominal for yes/no):", "",
           "| question | " + " | ".join(label(n) for n in names) + " |", "|---|" + "---|" * len(names)]
    for q in QUESTIONS:
        md.append(f"| Q{q.number} {q.key} | " + " | ".join(f(res["ablation_alpha"][n][q.key]) for n in names) + " |")
    md.append("| poems paired (Q1) | " + " | ".join(str(res["ablation_paired"][n]["readability"]) for n in names) + " |")
    gap = res["ablation_gap_generated_vs_real"]
    cell = lambda c: "–" if c is None else f"{c['diff']:+.2f} [{c['lo']:+.2f}, {c['hi']:+.2f}]{' *' if c['excludes_zero'] else ''}"  # noqa: E731
    main = ["all", "A", "B", "all, crossed poems"]
    md += ["", "**Gemini − real poets** on the 1–5 questions: mean over poems, 95% bootstrap over poems, * = interval "
           "excludes 0. Views: as rated; centred = each annotator's own mean removed; min–max = each annotator's answers "
           "stretched from their own lowest–highest onto 1–5 (an annotator with one answer throughout is left out).", "",
           "| question | view | " + " | ".join(label(n) for n in main) + " |", "|---|---|" + "---|" * len(main)]
    for k in LIKERT:
        for v in VIEWS:
            md.append(f"| {k} | {v} | " + " | ".join(cell(gap[n][v][k]) for n in main) + " |")
    loo = [n for n in names if n.startswith("without ")]
    md += ["", "Leave-one-out, Gemini − real poets (as rated / min–max; * = interval excludes 0):", "",
           "| question | " + " | ".join(label(n) for n in loo) + " |", "|---|" + "---|" * len(loo)]
    short = lambda c: "–" if c is None else f"{c['diff']:+.2f}{'*' if c['excludes_zero'] else ''}"  # noqa: E731
    for k in LIKERT:
        md.append(f"| {k} | " + " | ".join(f"{short(gap[n]['as rated'][k])} / {short(gap[n]['min–max'][k])}"
                                           for n in loo) + " |")
    md += ["", "**Mean per source group** (as rated; yes/no = share of yes) for all, A and B, and the Spearman ρ between "
           "A's and B's poem means on the poems both groups rated:", "",
           "| question | " + " | ".join(f"{n} · {g.split(' ')[0]}" for n in ("all", "A", "B") for g in GROUPS)
           + " | ρ(A, B) (poems) |", "|---|" + "---|" * (3 * len(GROUPS) + 1)]
    for q in QUESTIONS:
        r = res["group_levels"][q.key]
        md.append(f"| Q{q.number} {q.key} | " + " | ".join(f(r[n][g], 2) for n in ("all", "A", "B") for g in GROUPS)
                  + f" | {f(r['rho_AB'])} ({r['poems_AB']}) |")
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    main()
