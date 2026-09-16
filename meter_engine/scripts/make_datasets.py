#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_datasets.py — convert raw poem text files into the ``dataset/bhagavatam.json``
record layout, so every corpus can be run through the same evaluation scripts.

    python3 scripts/make_datasets.py kuchimanchi  ../kuchimanchi_timmakavi_poems.txt  ../dataset/kuchimanchi_timmakavi.json
    python3 scripts/make_datasets.py vemana       /path/to/vemana_poems.txt           ../dataset/vemana.json

Input: poems separated by blank lines, one pāda (or printed half-line) per row.
Output: a JSON list of records with the keys of bhagavatam.json (``id``,
``poem_number``, ``metre_code``, ``metre``, ``metre_roman``, ``form``,
``expected_lines``, ``allowed_lines``, ``line_count``, ``complete``, ``verse``,
``source`` …).  Labels are filled only when the source carries them (Vemana:
every 4-line poem is an ఆటవెలది, the 8-line ones సీసము); otherwise the metre
fields are ``null`` and the metre engine's identification is the reference.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# corpus metre_roman spellings used by dataset/bhagavatam.json
LABELS = {
    "ఆ.": ("ఆటవెలది", "aataveladi", 4),
    "సీ.": ("సీసము", "seesamu", 8),
    "క.": ("కందము", "kandamu", 4),
}


def blocks_of(text: str) -> list[list[str]]:
    out = []
    for block in re.split(r"\n\s*\n", text):
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if lines:
            out.append(lines)
    return out


def record(prefix: str, n: int, lines: list[str], label: str | None, source: str, author: str,
           label_source: str | None = None) -> dict:
    metre_te, metre_roman, expected = LABELS.get(label or "", (None, None, None))
    form = "verse" if len(lines) > 1 else "prose"           # one-line blocks are colophons / gadya
    return {
        "id": f"{prefix}-{n}" + (f"-{label}" if label else ""),
        "skandha": None, "poem_number": n, "sub_number": 0, "parent_id": None,
        "metre_code": label.rstrip(".") if label else None, "metre": metre_te, "metre_roman": metre_roman,
        "form": form, "expected_lines": expected, "allowed_lines": [expected] if expected else None,
        "metre_variant": None, "line_count": len(lines), "complete": True,
        "verse": lines, "teeka": None, "teeka_pairs": [], "bhavam": None,
        "source": source, "author": author, "child_id": None,
        "label_source": label_source,      # "corpus" = the source carries the label; "heuristic" = assigned by line count
    }


def convert(kind: str, src: Path, out: Path) -> dict:
    text = src.read_text(encoding="utf-8")
    blocks = blocks_of(text)
    seen: set[str] = set()
    records = []
    dupes = 0
    for lines in blocks:
        key = "\n".join(lines)
        if key in seen:
            dupes += 1
            continue
        seen.add(key)
        if kind == "vemana":
            # the Vemana source carries no labels: 4-line poems are ALMOST all ఆటవెలది (the metre engine
            # identifies ~13% of them as కందము), 8-line ones సీసము — record the label as a heuristic
            label = "ఆ." if len(lines) == 4 else "సీ." if len(lines) == 8 else None
            rec = record("vemana", len(records) + 1, lines, label, src.name, "Vemana", "heuristic" if label else None)
        else:
            rec = record("kuchimanchi", len(records) + 1, lines, None, src.name, "Kūcimañci Timmakavi", None)
        records.append(rec)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
    return {"blocks": len(blocks), "records": len(records), "duplicates_dropped": dupes,
            "verse": sum(r["form"] == "verse" for r in records), "prose": sum(r["form"] == "prose" for r in records)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=["kuchimanchi", "vemana"])
    ap.add_argument("src"); ap.add_argument("out")
    ns = ap.parse_args(argv)
    print(json.dumps(convert(ns.kind, Path(ns.src), Path(ns.out)), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
