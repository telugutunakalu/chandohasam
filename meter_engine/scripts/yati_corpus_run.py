#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yati_corpus_run.py — run the yati engine over the whole Pothana corpus.

For every poem whose corpus label maps to a catalogue meter, identify it ONCE
with the metrical DAWG (prepare_stanza), then evaluate its yati under several
engine configurations, and write reports/yati_run_<date>.{json,md}.

    python3 scripts/yati_corpus_run.py [--corpus ../dataset/bhagavatam.json] [--limit N]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent.parent))

import yati_engine as ye                               # noqa: E402
from indic_meter_dawg import default_dawg               # noqa: E402
from scripts.corpus_run import catalogue_name           # noqa: E402

CONFIGS = [("strict", "off"), ("strict", "hypothesis"), ("relaxed", "hypothesis"), ("relaxed", "acchu")]


def run(corpus: Path, out_dir: Path, limit: int = 0) -> dict:
    dawg = default_dawg()
    data = json.load(open(corpus, encoding="utf-8"))
    if limit:
        data = data[:limit]
    t0 = time.time()
    counts = {c: collections.Counter() for c in CONFIGS}
    per_meter = {c: collections.defaultdict(collections.Counter) for c in CONFIGS}
    rules = {c: collections.Counter() for c in CONFIGS}
    reasons = {c: collections.Counter() for c in CONFIGS}
    failing = {c: [] for c in CONFIGS}
    n_groups = collections.Counter()
    skipped = collections.Counter()
    unidentified = []
    run_n = 0
    for p in data:
        target = catalogue_name(dawg, p["metre_roman"])
        if target is None:
            skipped[p["metre_roman"]] += 1
            continue
        run_n += 1
        plan = ye.prepare_stanza(p["verse"])
        if not plan.identified or not plan.padas:
            unidentified.append(p["id"])
            continue
        for cfg in CONFIGS:
            prof, sandhi = cfg
            res = ye.evaluate_plan(plan, prof, sandhi=sandhi)
            groups = [g for l in res.lines for g in l.groups]
            ok = res.matched
            counts[cfg]["ok" if ok else "fail"] += 1
            per_meter[cfg][plan.meter]["ok" if ok else "fail"] += 1
            for g in groups:
                n_groups[cfg] += 1
                if g.matched:
                    rules[cfg][g.rule] += 1
                elif g.results:
                    r0 = g.results[0]
                    reasons[cfg][r0.rejected[0].rule if r0.rejected else "no-candidate"] += 1
            if not ok:
                bad = []
                for li, l in enumerate(res.lines, 1):
                    for g in l.groups:
                        if not g.matched and g.results:
                            r0 = g.results[0]
                            bad.append({"pada": li, "positions": list(g.positions), "a": r0.a.describe(), "b": r0.b.describe(),
                                        "why": r0.why, "min_profile": r0.min_profile})
                failing[cfg].append({"id": p["id"], "meter": plan.meter, "label": p["metre_roman"], "fails": bad})
    elapsed = time.time() - t0
    summary = {
        "date": dt.date.today().isoformat(), "corpus": str(corpus), "poems_in_corpus": len(data), "run": run_n,
        "skipped": dict(skipped), "unidentified": len(unidentified), "seconds": round(elapsed, 1),
        "configs": {f"{p}/{s}": {"poems": dict(counts[(p, s)]), "groups": n_groups[(p, s)],
                                  "per_meter": {m: dict(c) for m, c in per_meter[(p, s)].items()},
                                  "rules": dict(rules[(p, s)].most_common()), "fail_reasons": dict(reasons[(p, s)].most_common())}
                    for (p, s) in CONFIGS},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / f"yati_run_{summary['date']}"
    stem.with_suffix(".json").write_text(json.dumps({"summary": summary, "unidentified": unidentified,
                                                     "failing": {f"{p}/{s}": failing[(p, s)] for (p, s) in CONFIGS}},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")
    stem.with_suffix(".md").write_text(report_md(summary, failing), encoding="utf-8")
    return summary


def report_md(s: dict, failing: dict) -> str:
    md = [f"# Yati run — yati engine over the Pothana corpus ({s['date']})", "",
          f"Corpus `{s['corpus']}`: {s['poems_in_corpus']:,} records; {s['run']:,} with a catalogue label were run; "
          f"{s['unidentified']} not identified by the DAWG (skipped); {sum(s['skipped'].values()):,} labels outside the catalogue. {s['seconds']} s.", "",
          "A poem *passes* when every yati group of every pāda is satisfied (prāsa-yati fallback where the meter allows it).", "",
          "| profile / sandhi mode | poems pass | poems fail | pass % | yati groups |", "|---|---|---|---|---|"]
    for name, c in s["configs"].items():
        ok, fail = c["poems"].get("ok", 0), c["poems"].get("fail", 0)
        md.append(f"| {name} | {ok:,} | {fail:,} | {100 * ok / max(1, ok + fail):.1f}% | {c['groups']:,} |")
    for name, c in s["configs"].items():
        md += ["", f"## {name}", "", "| metre | pass | fail | pass % |", "|---|---|---|---|"]
        for m, cc in sorted(c["per_meter"].items(), key=lambda kv: -(kv[1].get("ok", 0) + kv[1].get("fail", 0))):
            n = cc.get("ok", 0) + cc.get("fail", 0)
            md.append(f"| {m} | {cc.get('ok', 0):,} | {cc.get('fail', 0):,} | {100 * cc.get('ok', 0) / n:.1f}% |")
        md += ["", "Rules that satisfied a yati group:", "", "| rule | groups |", "|---|---|"]
        md += [f"| {r} | {n:,} |" for r, n in c["rules"].items()]
        md += ["", "Named reasons for failing groups:", "", "| reason | groups |", "|---|---|"]
        md += [f"| {r} | {n:,} |" for r, n in c["fail_reasons"].items()]
    key = list(s["configs"])[-1]
    md += ["", f"## Poems still failing under {key} ({len(failing[tuple(key.split('/'))])})", "",
           "| id | metre | pāda | positions | వళి | yati akshara | why |", "|---|---|---|---|---|---|---|"]
    for f in failing[tuple(key.split('/'))]:
        for b in f["fails"]:
            md.append(f"| {f['id']} | {f['meter']} | {b['pada']} | {'-'.join(map(str, b['positions']))} | {b['a']} | {b['b']} | {b['why'][:90]} |")
    return "\n".join(md) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--corpus", default=str(HERE.parent.parent / "dataset" / "bhagavatam.json"))
    ap.add_argument("--out", default=str(HERE.parent / "reports"))
    ap.add_argument("--limit", type=int, default=0)
    ns = ap.parse_args(argv)
    s = run(Path(ns.corpus), Path(ns.out), ns.limit)
    for name, c in s["configs"].items():
        print(name, dict(c["poems"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
