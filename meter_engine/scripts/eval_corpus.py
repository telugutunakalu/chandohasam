#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eval_corpus.py — run the end-to-end tool (metre + ప్రాస + యతి) over a corpus in
the bhagavatam.json layout and write reports/eval_<name>_<date>.{json,md}.

    python3 scripts/eval_corpus.py ../dataset/vemana.json --name vemana
    python3 scripts/eval_corpus.py ../dataset/kuchimanchi_timmakavi.json --name kuchimanchi --limit 200

Per poem: identify once, then analyse under (relaxed, hypothesis) and
(relaxed, acchu).  When the corpus carries metre labels, the identification
is also compared with them.
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

from chandohasam import analyze                      # noqa: E402
from indic_meter_dawg import identify_text           # noqa: E402
from scripts.corpus_run import NAME_MAP              # noqa: E402

CONFIGS = [("relaxed", "hypothesis"), ("relaxed", "acchu")]


def run(corpus: Path, name: str, out_dir: Path, limit: int = 0) -> dict:
    data = [r for r in json.load(open(corpus, encoding="utf-8")) if r.get("form") == "verse"]
    if limit:
        data = data[:limit]
    t0 = time.time()
    meters = collections.Counter()
    label_agree = collections.Counter()
    per_cfg = {c: collections.Counter() for c in CONFIGS}
    per_meter = {c: collections.defaultdict(collections.Counter) for c in CONFIGS}
    yati_rules = collections.Counter()
    prasa_labels = collections.Counter()
    unidentified: list[dict] = []
    failing: dict[str, list[dict]] = {f"{p}/{s}": [] for p, s in CONFIGS}
    for rec in data:
        text = "\n".join(rec["verse"])
        ident = identify_text(text)
        if not ident.identified:
            unidentified.append({"id": rec["id"], "label": rec.get("metre_roman"),
                                 "failures": [f.to_dict() for f in ident.failures[:3]]})
            meters["(none)"] += 1
            continue
        best = ident.best
        meters[best.label] += 1
        if rec.get("metre_roman"):
            target = NAME_MAP.get(rec["metre_roman"], rec["metre_roman"])
            label_agree["agree" if best.meter == target or best.is_variant_of == target else "differ"] += 1
        for cfg in CONFIGS:
            prof, sandhi = cfg
            a = analyze(text, profile=prof, yati_sandhi=sandhi, identification=ident)
            key = f"{prof}/{sandhi}"
            c = per_cfg[cfg]
            c["poems"] += 1
            c["prasa_applicable"] += any(u.prasa and u.prasa.applicable for u in a.units)
            c["prasa_ok"] += a.prasa_matched
            c["yati_ok"] += a.yati_matched
            c["all_ok"] += a.matched
            pm = per_meter[cfg][a.meter]
            pm["poems"] += 1; pm["prasa_ok"] += a.prasa_matched; pm["yati_ok"] += a.yati_matched; pm["all_ok"] += a.matched
            if cfg == CONFIGS[0]:
                for u in a.units:
                    if u.prasa and u.prasa.applicable:
                        prasa_labels[u.prasa.label_te if u.prasa.matched else "✗ " + (u.prasa.violations[0]["rule"] if u.prasa.violations else "fail")] += 1
                    for l in u.lines:
                        for s in l.yati:
                            yati_rules[s.rule if s.matched else "✗"] += 1
            if not a.matched:
                bad = []
                for u in a.units:
                    if u.prasa and u.prasa.applicable and not u.prasa.matched:
                        bad.append({"kind": "prasa", "unit": u.meter, "detail": u.prasa.violations[0]["detail"] if u.prasa.violations else u.prasa.label_te})
                    for l in u.lines:
                        for s in l.yati:
                            if not s.matched:
                                bad.append({"kind": "yati", "unit": u.meter, "pada": l.line_no, "positions": s.positions,
                                            "aksharas": s.aksharas, "detail": s.detail})
                failing[key].append({"id": rec["id"], "meter": a.meter, "label": rec.get("metre_roman"), "problems": bad})
    elapsed = time.time() - t0
    summary = {
        "date": dt.date.today().isoformat(), "corpus": str(corpus), "name": name, "poems": len(data),
        "identified": len(data) - len(unidentified), "unidentified": len(unidentified), "seconds": round(elapsed, 1),
        "identified_meters": dict(meters.most_common()), "label_agreement": dict(label_agree),
        "configs": {f"{p}/{s}": {"totals": dict(per_cfg[(p, s)]),
                                  "per_meter": {m: dict(c) for m, c in per_meter[(p, s)].items()}} for p, s in CONFIGS},
        "yati_rules": dict(yati_rules.most_common()), "prasa_labels": dict(prasa_labels.most_common()),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / f"eval_{name}_{summary['date']}"
    stem.with_suffix(".json").write_text(json.dumps({"summary": summary, "unidentified": unidentified, "failing": failing},
                                                    ensure_ascii=False, indent=1), encoding="utf-8")
    stem.with_suffix(".md").write_text(report_md(summary, unidentified, failing), encoding="utf-8")
    return summary


def pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f}%" if b else "–"


def report_md(s: dict, unidentified: list, failing: dict) -> str:
    md = [f"# Evaluation — {s['name']} ({s['date']})", "",
          f"Corpus `{s['corpus']}`: {s['poems']:,} verse records. Identified by the metrical DAWG: "
          f"{s['identified']:,} ({pct(s['identified'], s['poems'])}); not identified: {s['unidentified']:,}. {s['seconds']} s.", ""]
    if s["label_agreement"]:
        la = s["label_agreement"]
        md += [f"Label agreement (corpus label vs identified metre): {la.get('agree', 0):,} agree, {la.get('differ', 0):,} differ "
               f"({pct(la.get('agree', 0), la.get('agree', 0) + la.get('differ', 0))}).", ""]
    md += ["## Identified metres", "", "| metre | poems |", "|---|---|"]
    md += [f"| {m} | {n:,} |" for m, n in s["identified_meters"].items()]
    md += ["", "## ప్రాస and యతి over the identified poems", "",
           "| profile / yati sandhi | poems | prāsa required | prāsa ok | yati ok | prāsa and yati ok |", "|---|---|---|---|---|---|"]
    for name, c in s["configs"].items():
        t = c["totals"]; n = t.get("poems", 0)
        md.append(f"| {name} | {n:,} | {t.get('prasa_applicable', 0):,} | {t.get('prasa_ok', 0):,} ({pct(t.get('prasa_ok', 0), n)}) | "
                  f"{t.get('yati_ok', 0):,} ({pct(t.get('yati_ok', 0), n)}) | {t.get('all_ok', 0):,} ({pct(t.get('all_ok', 0), n)}) |")
    for name, c in s["configs"].items():
        md += ["", f"### per metre — {name}", "", "| metre | poems | prāsa ok | yati ok | both |", "|---|---|---|---|---|"]
        for m, cc in sorted(c["per_meter"].items(), key=lambda kv: -kv[1]["poems"]):
            md.append(f"| {m} | {cc['poems']:,} | {pct(cc['prasa_ok'], cc['poems'])} | {pct(cc['yati_ok'], cc['poems'])} | {pct(cc['all_ok'], cc['poems'])} |")
    md += ["", "## Yati rules that satisfied a group (relaxed/hypothesis)", "", "| rule | groups |", "|---|---|"]
    md += [f"| {r} | {n:,} |" for r, n in s["yati_rules"].items()]
    md += ["", "## Prāsa classifications (relaxed/hypothesis)", "", "| label | units |", "|---|---|"]
    md += [f"| {r} | {n:,} |" for r, n in s["prasa_labels"].items()]
    md += ["", f"## Not identified ({len(unidentified)})", "", "| id | label | first failure |", "|---|---|---|"]
    md += [f"| {u['id']} | {u['label'] or '–'} | {u['failures'][0]['meter'] + ': ' + u['failures'][0]['reason'] if u['failures'] else '–'} |" for u in unidentified[:60]]
    key = list(failing)[0]
    md += ["", f"## Poems failing prāsa or yati under {key} ({len(failing[key])}; first 80)", "",
           "| id | metre | problem |", "|---|---|---|"]
    for f in failing[key][:80]:
        for b in f["problems"][:2]:
            where = f"pāda {b['pada']} {'-'.join(map(str, b['positions']))} {' ↔ '.join(b['aksharas'])}" if b["kind"] == "yati" else "prāsa"
            md.append(f"| {f['id']} | {f['meter']} | {where}: {b['detail'][:80]} |")
    return "\n".join(md) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("corpus"); ap.add_argument("--name", required=True)
    ap.add_argument("--out", default=str(HERE.parent / "reports")); ap.add_argument("--limit", type=int, default=0)
    ns = ap.parse_args(argv)
    s = run(Path(ns.corpus), ns.name, Path(ns.out), ns.limit)
    print(json.dumps({k: s[k] for k in ("poems", "identified", "label_agreement", "seconds")}, ensure_ascii=False))
    for name, c in s["configs"].items():
        print(name, c["totals"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
