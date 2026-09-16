# -*- coding: utf-8 -*-
"""
Run the scanner + metrical DAWG over the whole Pothana corpus
(``dataset/bhagavatam.json``) and write a report.

    python3 meter_engine/scripts/corpus_run.py [--out meter_engine/reports] [--limit N]

For every poem whose corpus label maps to a catalogue meter, identify from
the verse text and bucket the outcome:

  agree      best candidate == corpus label
  in-cands   label among the candidates but not best (ambiguity)
  other      identified, but the label is not among the candidates
  none       no meter matched
  skipped    label not in the catalogue (prose, rare vrittas) — counted, not run

Outputs ``corpus_run_<date>.md`` (tables) and ``corpus_run_<date>.json``
(every non-agreeing poem with its scansion and the identifier's verdict).
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

from indic_meter_dawg import default_dawg, identify_text          # noqa: E402

# corpus metre_roman -> catalogue name (identity where the spelling already agrees)
NAME_MAP = {
    "aataveladi": "ataveladi", "shardulavikriditamu": "sardulavikriditamu", "mattakokila": "mattakokilamu",
    "indravajramu": "indravajra", "upendravajramu": "upendravajra", "panchachamaramu": "pamcacamaramu",
}


def catalogue_name(dawg, label: str):
    name = NAME_MAP.get(label, label)
    return name if name in dawg.catalogue.by_name else None


def run(corpus: Path, out_dir: Path, limit: int = 0) -> dict:
    dawg = default_dawg()
    data = json.load(open(corpus, encoding="utf-8"))
    if limit:
        data = data[:limit]
    t0 = time.time()
    per = collections.defaultdict(collections.Counter)
    levels = collections.Counter()
    skipped = collections.Counter()
    details = []
    for p in data:
        label = p["metre_roman"]
        target = catalogue_name(dawg, label)
        if target is None:
            skipped[label] += 1
            continue
        res = identify_text(p["verse"], dawg)
        if not res.identified:
            bucket = "none"
        elif res.best.meter == target or res.best.is_variant_of == target:
            bucket = "agree"
        elif any(c.meter == target for c in res.candidates):
            bucket = "in-cands"
        else:
            bucket = "other"
        per[target][bucket] += 1
        per[target]["complete" if p["complete"] else "incomplete"] += 1
        if res.identified:
            levels["vikalpa" if any("vikalpa" in n for n in res.notes) else "compound" if res.notes else "canonical"] += 1
        if bucket != "agree":
            details.append({
                "id": p["id"], "label": label, "target": target, "complete": p["complete"], "bucket": bucket,
                "best": res.best.label if res.best else None,
                "candidates": [c.label for c in res.candidates],
                "notes": list(res.notes),
                "scansion": [s.format() for s in res.scansions],
                "verse": p["verse"],
                "failures": [f.to_dict() for f in res.failures[:6]],
            })
    elapsed = time.time() - t0
    summary = {
        "date": dt.date.today().isoformat(), "corpus": str(corpus), "poems_in_corpus": len(data),
        "run": sum(sum(c[b] for b in ("agree", "in-cands", "other", "none")) for c in per.values()),
        "skipped": dict(skipped), "levels": dict(levels), "seconds": round(elapsed, 1),
        "per_metre": {m: dict(c) for m, c in per.items()},
        "totals": {b: sum(c[b] for c in per.values()) for b in ("agree", "in-cands", "other", "none")},
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = out_dir / f"corpus_run_{summary['date']}"
    (stem.with_suffix(".json")).write_text(json.dumps({"summary": summary, "details": details}, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
    (stem.with_suffix(".md")).write_text(report_md(summary, details), encoding="utf-8")
    return summary


def report_md(s: dict, details: list) -> str:
    tot = s["totals"]
    run = s["run"] or 1
    md = [f"# Corpus run — scansion + metrical DAWG on the Pothana corpus ({s['date']})", "",
          f"Corpus `{s['corpus']}`: {s['poems_in_corpus']:,} records. Run on the {s['run']:,} whose label maps to a "
          f"catalogue meter; {sum(s['skipped'].values()):,} skipped (label outside the catalogue). {s['seconds']} s.", "",
          "| outcome | poems | share |", "|---|---|---|"]
    for b, label in (("agree", "best candidate = corpus label"), ("in-cands", "label among candidates, not best"),
                     ("other", "identified as something else"), ("none", "no meter matched")):
        md.append(f"| {label} | {tot[b]:,} | {100 * tot[b] / run:.2f}% |")
    md += ["", "Readings needed: " + ", ".join(f"{k} {v:,}" for k, v in s["levels"].items()), "",
           "## Per metre", "", "| metre | poems | agree | in-cands | other | none | agree % |", "|---|---|---|---|---|---|---|"]
    for m, c in sorted(s["per_metre"].items(), key=lambda kv: -sum(kv[1].get(b, 0) for b in ("agree", "in-cands", "other", "none"))):
        n = sum(c.get(b, 0) for b in ("agree", "in-cands", "other", "none"))
        md.append(f"| {m} | {n:,} | {c.get('agree', 0):,} | {c.get('in-cands', 0)} | {c.get('other', 0)} | {c.get('none', 0)} | "
                  f"{100 * c.get('agree', 0) / n:.1f}% |")
    md += ["", "## Skipped labels (not in the catalogue)", "", "| label | poems |", "|---|---|"]
    for k, v in sorted(s["skipped"].items(), key=lambda kv: -kv[1]):
        md.append(f"| {k} | {v:,} |")
    md += ["", f"## Non-agreeing poems ({len(details)})", "",
           "| id | label | outcome | identified as | notes |", "|---|---|---|---|---|"]
    for d in details:
        md.append(f"| {d['id']} | {d['label']} | {d['bucket']} | {d['best'] or '–'} | {'; '.join(d['notes']) or '–'} |")
    md += ["", "Scansions and failure points for each are in the JSON next to this file."]
    return "\n".join(md) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--corpus", default=str(HERE.parent.parent / "dataset" / "bhagavatam.json"))
    ap.add_argument("--out", default=str(HERE.parent / "reports"))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args(argv)
    s = run(Path(a.corpus), Path(a.out), a.limit)
    print(json.dumps({k: s[k] for k in ("run", "totals", "levels", "seconds")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
