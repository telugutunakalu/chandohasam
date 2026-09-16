# -*- coding: utf-8 -*-
"""
Relabel poems in dataset/bhagavatam.json (+ .txt headers), the way
dataset/CORRECTIONS.md documents: the record is edited textually (every
other byte untouched), the original id/metre fields are kept in a
``metre_corrected`` object, ``child_id`` references and the txt header line
are renamed, and a table is appended to CORRECTIONS.md.

    python3 meter_engine/scripts/corpus_fix.py --apply FIXES.json
    FIXES.json = [{"id": "1-259-ఉ.", "code": "మ", "reason": "..."}, ...]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON = ROOT / "dataset" / "bhagavatam.json"
TXT = ROOT / "dataset" / "bhagavatam.txt"
LOG = ROOT / "dataset" / "CORRECTIONS.md"


def code_table(records: list[dict]) -> dict[str, tuple[str, str]]:
    """metre_code -> (metre, metre_roman) as used in the corpus."""
    out = {}
    for p in records:
        out.setdefault(p["metre_code"], (p["metre"], p["metre_roman"]))
    return out


def new_id(old_id: str, code: str) -> str:
    prefix = old_id.rsplit("-", 1)[0]
    return f"{prefix}-{code}."


def apply(fixes: list[dict], date: str, by: str) -> list[dict]:
    j = JSON.read_text(encoding="utf-8")
    t = TXT.read_text(encoding="utf-8")
    table = code_table(json.loads(j))
    done = []
    for f in fixes:
        old_id, code = f["id"], f["code"]
        metre, roman = table[code]
        nid = new_id(old_id, code)
        head = f'  "id": "{old_id}",\n'
        assert j.count(head) == 1, f"record {old_id} not found once"
        i = j.index(head)
        nxt = j.index("\n {\n", i) if "\n {\n" in j[i:] else len(j)
        rec = j[i:nxt]
        import re
        m = re.search(r'  "metre_code": "([^"]*)",\n  "metre": "([^"]*)",\n  "metre_roman": "([^"]*)",\n', rec)
        assert m, old_id
        old_code, old_metre, old_roman = m.groups()
        assert '"metre_corrected"' not in rec, f"{old_id} already corrected"
        block = (f'  "metre_code": "{code}",\n  "metre": "{metre}",\n  "metre_roman": "{roman}",\n'
                 f'  "metre_corrected": {{\n   "from_id": "{old_id}",\n   "from_metre_code": "{old_code}",\n'
                 f'   "from_metre": "{old_metre}",\n   "from_metre_roman": "{old_roman}",\n   "date": "{date}",\n'
                 f'   "reason": "{f["reason"]}",\n   "corrected_by": "{by}"\n  }},\n')
        rec2 = rec.replace(head, f'  "id": "{nid}",\n', 1).replace(m.group(0), block, 1)
        j = j[:i] + rec2 + j[nxt:]
        ref = f'"child_id": "{old_id}"'
        refs = j.count(ref)
        j = j.replace(ref, f'"child_id": "{nid}"')
        assert j.count(f'"{old_id}"') == 1, f"{old_id}: unexpected remaining reference"
        line = f"\n{old_id}\n"
        n_hdr = t.count(line)
        assert n_hdr <= 1, f"{old_id}: txt header found {n_hdr} times"
        t = t.replace(line, f"\n{nid}\n")                 # records with source 'inserted' have no txt header
        done.append({"old_id": old_id, "new_id": nid, "from": old_roman, "to": roman, "refs": refs,
                     "reason": f["reason"], "txt_header": bool(n_hdr)})
    json.loads(j)                                   # still valid
    JSON.write_text(j, encoding="utf-8")
    TXT.write_text(t, encoding="utf-8")
    return done


def log(done: list[dict], date: str, title: str) -> None:
    rows = ["", f"## {date} — {len(done)} poems relabelled ({title})", "", "| old id | new id | from → to | reason |", "|---|---|---|---|"]
    for d in done:
        extra = "" if d.get("txt_header", True) else " (record inserted into the json; no header line in bhagavatam.txt)"
        rows.append(f"| {d['old_id']} | {d['new_id']} | {d['from']} → {d['to']} | {d['reason']}{extra} |")
    rows += ["", "Same procedure as above (textual edit, originals in `metre_corrected`, txt headers renamed"
             + ("; `child_id` references of seesam parents updated" if any(d["refs"] for d in done) else "") + ").", ""]
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write("\n".join(rows))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", required=True, help="JSON list of {id, code, reason}")
    ap.add_argument("--title", default="scansion + metrical DAWG full-corpus run")
    ap.add_argument("--by", default="meter_engine scansion + DAWG full-corpus run, reviewed from the scansion output")
    a = ap.parse_args(argv)
    fixes = json.load(open(a.apply, encoding="utf-8"))
    date = dt.date.today().isoformat()
    done = apply(fixes, date, a.by)
    log(done, date, a.title)
    for d in done:
        print(f"{d['old_id']} -> {d['new_id']}  ({d['from']} -> {d['to']}, child refs {d['refs']}, txt header {'yes' if d['txt_header'] else 'NO'})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
