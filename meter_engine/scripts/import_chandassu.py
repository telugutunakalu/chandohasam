#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
import_chandassu.py — convert the Kaggle "Chandassu" dataset into the dataset/bhagavatam.json
record layout, dropping poems we already have in dataset/*.json.

    python3 scripts/import_chandassu.py ../dataset/raw/chandassu/Chandassu_Dataset.csv ../dataset/chandassu.json

Source: kaggle.com/datasets/boddusripavan111/chandassu (MIT; Boddu Sri Pavan & Boddu Swathi Sree,
arXiv 2510.01233; texts from andhrabharati.com): 4,651 padyams from 28 satakams in 8 metres.

Layout (as in vemana.json):
* one pāda per line; a "-" at the end of a line (a word running into the next pāda) is kept as printed;
* tetagiti rows printed with two pādas per line ("…-…", "…।…", "…|…") are split into pādas;
* every seesamu row is joined with the ettugeeti row that follows it (the seesa satakams alternate
  seesamu / tetagiti rows): 4 seesa lines with their halves joined by " - ", then the 4 ettugeeti pādas;
* rows whose pāda breaks were lost in the source (a whole seesa part on one line) are kept as printed
  and marked complete = false.

Duplicates: exact duplicates within the file (after normalisation), and poems already in dataset/*.json:
a new poem is dropped when ≥ THRESHOLD of its character 8-grams occur in one existing record (or that
record's 8-grams in it). Dropped rows and their matches go to import_report.json next to the CSV.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_datasets import LABELS, record  # noqa: E402

TYPES = {"aataveladi": "ఆ.", "kandamu": "క.", "teytageethi": "తే.", "seesamu": "సీ.",
         "vutpalamaala": "ఉ.", "champakamaala": "చ.", "saardulamu": "శా.", "mattebhamu": "మ."}
SOURCE = "Chandassu_Dataset.csv"
EXISTING = ("bhagavatam.json", "vemana.json", "kuchimanchi_timmakavi.json")
GRAM = 8
THRESHOLD = 0.6


def lines_of(text: str) -> list[str]:
    text = unicodedata.normalize("NFC", text.replace("_x000D_", "\n").replace("\r", "\n"))
    return [re.sub(r"\s+", " ", ln).strip() for ln in text.split("\n") if ln.strip()]


def split_padas(lines: list[str]) -> list[str]:
    """Pādas of a gīti (tetagiti/ataveladi) row printed two or more to a line."""
    if len(lines) >= 4:
        return lines
    out = []
    for ln in lines:
        out += [p.strip() for p in re.split(r"\s*[।|]\s*|(?<=\S)-(?=\s*\S)", ln) if p.strip()]
    return out


def seesa_line(line: str) -> str:
    """One seesa pāda with its two halves joined by " - " (vemana.json style)."""
    line = re.sub(r"(?<=[ఀ-౿])-\s+(?=[ఀ-౿])", " - ", line)    # "half1- half2"
    line = re.sub(r"\s*[।|]\s*", " - ", line)                                     # "half1 । half2"
    if " - " not in line:
        line = re.sub(r"(?<=[ఀ-౿])-(?=[ఀ-౿])", " - ", line, count=1)
    return re.sub(r"\s+", " ", line).strip()


def canon(text: str) -> str:
    """Telugu letters and signs only: no spacing, punctuation, digits, ZWJ/ZWNJ or ఁ (editions differ)."""
    text = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in text if "ఀ" <= ch <= "ౣ" and ch != "ఁ")


def grams(text: str) -> set[str]:
    c = canon(text)
    return {c[i:i + GRAM] for i in range(max(0, len(c) - GRAM + 1))}


def build_records(rows: list[dict]) -> list[tuple[dict, list[int]]]:
    """(record, csv row numbers) in file order; seesamu rows absorb their ettugeeti row."""
    out, counters, i = [], collections.Counter(), 0
    while i < len(rows):
        r = rows[i]
        label, sat = TYPES[r["type"]], r["satakam"]
        lines, used = lines_of(r["raw_padyam_text"]), [i]
        if r["type"] == "seesamu":
            seesa = [seesa_line(ln) for ln in lines]
            nxt = rows[i + 1] if i + 1 < len(rows) else None
            gita = []
            if nxt and nxt["satakam"] == sat and nxt["type"] in ("teytageethi", "aataveladi"):
                gita = split_padas(lines_of(nxt["raw_padyam_text"]))
                used.append(i + 1)
            lines = seesa + gita
            complete = len(seesa) == 4 and len(gita) == 4
        else:
            lines = split_padas(lines) if r["type"] in ("teytageethi", "aataveladi") else lines
            complete = len(lines) == LABELS[label][2]
        counters[sat] += 1
        slug = re.sub(r"[^a-z]", "", sat.lower())
        rec = record(f"chandassu-{slug}", counters[sat], lines, label, SOURCE,
                     "Vemana" if sat == "Vemana" else None, "corpus")
        rec["skandha"] = f"{sat} satakam"
        rec["complete"] = complete
        out.append((rec, used))
        i += len(used)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv", type=Path)
    ap.add_argument("out", type=Path)
    ns = ap.parse_args(argv)
    csv.field_size_limit(sys.maxsize)
    rows = list(csv.DictReader(ns.csv.open(encoding="utf-8-sig")))
    built = build_records(rows)

    # existing poems: bhagavatam seesa parents are matched together with their ettugeeti child
    existing, index = {}, collections.defaultdict(set)
    for name in EXISTING:
        recs = json.loads((ns.out.parent / name).read_text(encoding="utf-8"))
        by_id = {x["id"]: x for x in recs}
        for x in recs:
            text = "\n".join(x.get("verse") or [])
            if x.get("child_id") in by_id:
                text += "\n" + "\n".join(by_id[x["child_id"]].get("verse") or [])
            g = grams(text)
            if len(g) >= 20:
                existing[x["id"]] = g
                for gram in g:
                    index[gram].add(x["id"])

    kept, dropped, seen = [], [], {}
    for rec, used in built:
        text = "\n".join(rec["verse"])
        key = canon(text)
        if key in seen:
            dropped.append({"csv_rows": used, "reason": "duplicate within the Kaggle file", "match": seen[key]})
            continue
        g = grams(text)
        hits = collections.Counter(eid for gram in g for eid in index.get(gram, ()))
        best = max(((n / len(g), n / len(existing[eid]), eid) for eid, n in hits.most_common(5)),
                   key=lambda t: max(t[0], t[1]), default=(0.0, 0.0, None))
        if g and max(best[0], best[1]) >= THRESHOLD:
            dropped.append({"csv_rows": used, "reason": "already in dataset", "match": best[2],
                            "share_of_new_in_existing": round(best[0], 3), "share_of_existing_in_new": round(best[1], 3)})
            continue
        seen[key] = rec["id"]
        kept.append((rec, used, max(best[0], best[1])))

    ns.out.write_text(json.dumps([r for r, _, _ in kept], ensure_ascii=False, indent=1), encoding="utf-8")
    report = {
        "source": "kaggle.com/datasets/boddusripavan111/chandassu (MIT), arXiv 2510.01233",
        "csv_rows": len(rows), "records_built": len(built), "kept": len(kept), "dropped": len(dropped),
        "dropped_by_reason": collections.Counter(d["reason"] for d in dropped),
        "dropped_by_existing_file": collections.Counter(d["match"].split("-")[0] if d["reason"] == "already in dataset"
                                                        else "kaggle" for d in dropped),
        "kept_incomplete": sum(not r["complete"] for r, _, _ in kept),
        "kept_by_metre": collections.Counter(r["metre_roman"] for r, _, _ in kept),
        "kept_by_satakam": collections.Counter(r["skandha"] for r, _, _ in kept),
        "max_similarity_of_kept": sorted(round(s, 2) for _, _, s in kept)[-10:],
        "kept_csv_rows": {r["id"]: used for r, used, _ in kept},
        "dropped_rows": dropped,
    }
    (ns.csv.parent / "import_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k not in ("kept_csv_rows", "dropped_rows")},
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
