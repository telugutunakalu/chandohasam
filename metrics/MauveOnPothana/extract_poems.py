"""Extract padyas (metrical poems only, no vachanas/prose) from bhagavatam.txt into JSON.

Input format: blocks headed by `<book>-<verse>[.<sub>]-<meter>.`, followed by the
verse text, then optional `టీకా:` (gloss) and `భావము:` (commentary) sections,
until the next header.

We keep only the verse text (lines between the header and టీకా:/భావము:) and only
for metrical forms. Excluded as non-padya / prose forms:
  వ. (vachanam), గ. (gadyam), దం. (dandakam), శ్లో. (Sanskrit sloka)

Cleaning: the source dump contains web boilerplate lines ("ఈ బ్రౌజరు అనుకూలం
కాదు.") and ~1k verses truncated to their first line(s). A padyam is a 4-line
stanza (సీసము renders as 8 half-lines), so blocks with fewer than 4 verse lines
(8 for సీ./ససీ.) are dropped as incomplete and counted in the stats.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "bhagavatam.txt"
OUT = Path(__file__).resolve().parent / "pothana_poems.json"

HEADER_RE = re.compile(r"^(\d+)-(\d+(?:\.\d+)?)-(\S+)\s*$")

EXCLUDE_METERS = {"వ.", "గ.", "దం.", "శ్లో."}

JUNK_RE = re.compile(r"బ్రౌజరు")  # web boilerplate: "ఈ/మీ బ్రౌజరు అను/అనూకూలం కాదు."

def min_lines(meter):
    return 8 if meter in ("సీ.", "ససీ.") else 4

METER_NAMES = {
    "క.": "Kandamu",
    "తే.": "Tetagiti",
    "సీ.": "Seesamu",
    "ఆ.": "Ataveladi",
    "మ.": "Mattebhamu",
    "చ.": "Champakamala",
    "ఉ.": "Utpalamala",
    "శా.": "Sardulamu",
    "మత్త.": "Mattakokila",
    "త.": "Taralamu",
    "మాలి.": "Malini",
    "లగ్రా.": "Layagrahi",
    "ఇం.": "Indravajra",
    "స్రగ్వి.": "Sragvini",
    "స్రగ్ద.": "Sragdhara",
    "ససీ.": "Seesamu(sa)",
    "వన.": "Vanamayuramu",
    "మస్ర.": "Mahasragdhara",
    "మం": "Manigananikaramu",
    "తో.": "Totakamu",
    "కవి.": "Kavirajavirajitamu",
    "ఉత్సా.": "Utsahamu",
}


def main():
    lines = SRC.read_text(encoding="utf-8").splitlines()

    poems = []
    excluded = Counter()
    cur = None  # dict for current block
    in_verse = False

    def flush():
        nonlocal cur
        if cur is None:
            return
        text_lines = [l.strip() for l in cur["lines"]]
        text_lines = [l for l in text_lines if l and not JUNK_RE.search(l)]
        if cur["meter"] in EXCLUDE_METERS:
            excluded[cur["meter"]] += 1
        elif len(text_lines) < min_lines(cur["meter"]):
            excluded["incomplete"] += 1
        else:
            poems.append(
                {
                    "id": cur["id"],
                    "book": cur["book"],
                    "verse": cur["verse"],
                    "meter": cur["meter"],
                    "meter_name": METER_NAMES.get(cur["meter"], cur["meter"]),
                    "n_lines": len(text_lines),
                    "text": "\n".join(text_lines),
                }
            )
        cur = None

    for line in lines:
        m = HEADER_RE.match(line.strip())
        if m:
            flush()
            book, verse, meter = m.group(1), m.group(2), m.group(3)
            cur = {
                "id": f"{book}-{verse}-{meter}",
                "book": int(book),
                "verse": verse,
                "meter": meter,
                "lines": [],
            }
            in_verse = True
            continue
        if cur is None:
            continue
        stripped = line.strip()
        if stripped.startswith("టీకా:") or stripped.startswith("భావము:"):
            in_verse = False
            continue
        if in_verse:
            cur["lines"].append(line)
    flush()

    meter_counts = Counter(p["meter"] for p in poems)
    stats = {
        "source": str(SRC),
        "total_poems": len(poems),
        "excluded_blocks": dict(excluded),
        "meter_counts": {
            f"{k} ({METER_NAMES.get(k, '?')})": v
            for k, v in meter_counts.most_common()
        },
    }

    OUT.write_text(json.dumps(poems, ensure_ascii=False, indent=1), encoding="utf-8")
    Path(OUT.parent / "extraction_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"\nWrote {len(poems)} poems -> {OUT}")


if __name__ == "__main__":
    main()
