#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
label_with_engine.py — fill missing metre labels in a dataset/*.json corpus.

    python3 scripts/label_with_engine.py ../dataset/kuchimanchi_timmakavi.json --chandassu ../dataset/raw/chandassu

For every verse record that has no metre, in this order:
  1. the metre engine (scansion + metrical DAWG) identifies it      -> label_source "engine"
  2. the poem is also in the Kaggle Chandassu dataset (matched by
     import_chandassu.py) and that dataset labels it                  -> label_source "chandassu"
  3. one metre scans at least 3/4 of the poem's lines                 -> label_source "engine-partial"
  otherwise the labels stay null. Metre names, codes and line counts follow dataset/bhagavatam.json;
seesa poems with their ettugeeti are labelled సీసము. Records that already have a metre are not touched.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from indic_meter_dawg import default_dawg, identify_text  # noqa: E402
from scripts.corpus_run import NAME_MAP                    # noqa: E402

KAGGLE_TO_CATALOGUE = {"aataveladi": "ataveladi", "kandamu": "kandamu", "teytageethi": "tetagiti",
                       "seesamu": "seesamu", "vutpalamaala": "utpalamala", "champakamaala": "champakamala",
                       "saardulamu": "sardulavikriditamu", "mattebhamu": "mattebhavikriditamu"}
PARTIAL = 0.75


def conventions(dataset_dir: Path) -> dict:
    """corpus metre_roman -> (metre_code, metre, expected_lines, allowed_lines), most common in bhagavatam.json."""
    seen = collections.defaultdict(collections.Counter)
    for r in json.loads((dataset_dir / "bhagavatam.json").read_text(encoding="utf-8")):
        if r.get("metre_roman"):
            seen[r["metre_roman"]][(r["metre_code"], r["metre"], r["expected_lines"], tuple(r["allowed_lines"] or ()))] += 1
    return {roman: c.most_common(1)[0][0] for roman, c in seen.items()}


def chandassu_labels(folder: Path) -> dict:
    """record id -> catalogue metre, for records that import_chandassu.py matched to a labelled Kaggle poem."""
    csv.field_size_limit(sys.maxsize)
    rows = list(csv.DictReader((folder / "Chandassu_Dataset.csv").open(encoding="utf-8-sig")))
    report = json.loads((folder / "import_report.json").read_text(encoding="utf-8"))
    return {d["match"]: KAGGLE_TO_CATALOGUE[rows[d["csv_rows"][0]]["type"]]
            for d in report["dropped_rows"] if d["reason"] == "already in dataset"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dataset", type=Path)
    ap.add_argument("--chandassu", type=Path, help="dataset/raw/chandassu (CSV + import_report.json)")
    ns = ap.parse_args(argv)
    dawg = default_dawg()
    conv = conventions(ns.dataset.parent)
    corpus_roman = {cat: roman for roman, cat in NAME_MAP.items()}          # catalogue -> corpus spelling
    external = chandassu_labels(ns.chandassu) if ns.chandassu else {}
    records = json.loads(ns.dataset.read_text(encoding="utf-8"))
    counts, by_metre, unlabelled = collections.Counter(), collections.Counter(), []

    for r in records:
        if r["form"] != "verse" or r.get("metre"):
            continue
        res = identify_text(r["verse"], dawg)
        name, source = None, None
        if res.identified:
            name, source = res.best.is_variant_of or res.best.meter, "engine"
        elif r["id"] in external:
            name, source = external[r["id"]], "chandassu"
        else:
            best = max(res.failures, key=lambda f: (f.lines_survived or 0, f.akshara or 0), default=None)
            if best and (best.lines_survived or 0) >= PARTIAL * r["line_count"]:
                name, source = best.meter, "engine-partial"
        if name is None:
            unlabelled.append(r["id"])
            continue
        roman = corpus_roman.get(name, name)
        code, metre, expected, allowed = conv.get(roman, (None, dawg.catalogue.by_name[name].name_te.replace("_", " "), None, ()))
        r.update(metre_code=code, metre=metre, metre_roman=roman, expected_lines=expected,
                 allowed_lines=list(allowed) if allowed else ([expected] if expected else None), label_source=source)
        counts[source] += 1
        by_metre[metre] += 1

    ns.dataset.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({"labelled": dict(counts), "left_unlabelled": len(unlabelled), "unlabelled_ids": unlabelled,
                      "by_metre": dict(by_metre.most_common())}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
