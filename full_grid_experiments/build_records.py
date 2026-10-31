"""The grid's E6 records (PLAN.md §5): the test records with each source poem's bhāvam replaced by its P1 prompt.

    ../.venv/bin/python -u build_records.py                  # after the user's review of prompts/p1_review.md

Every evaluator of the grid reads its prompts from these records ($E6_RECORDS_DIR=prompts/e6_p1/records, or
--e6-data prompts/e6_p1 for the MDLMs), so each model's own prompt builder is used unchanged:
- prompts/e6_p1/records/test.jsonl: the test split, the 183 source poems with `meaning` = P1 (one paragraph) and
  `meaning_p0` = the edition bhāvam; every other record as it was;
- val.jsonl, train.jsonl and ../leakage.json: links to the E6 originals.

P1 is prompts/p1.jsonl's text, or a hand-edited text from prompts/p1_edits.jsonl ({id, p1}) when the review gave one.
A prompt still flagged by a check stops the build unless --allow-flagged.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
E6 = HERE.parent / "diffusion_finetuning" / "data" / "e6"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--allow-flagged", action="store_true")
    args = ap.parse_args()
    rows = {r["id"]: r for r in map(json.loads, open(HERE / "prompts" / "p1.jsonl", encoding="utf-8"))}
    edits_path = HERE / "prompts" / "p1_edits.jsonl"
    edits = {e["id"]: e["p1"] for e in map(json.loads, open(edits_path, encoding="utf-8"))} if edits_path.exists() else {}
    flagged = [i for i, r in rows.items() if not r["result"]["passed"] and i not in edits]
    if flagged and not args.allow_flagged:
        raise SystemExit(f"{len(flagged)} prompts still flagged (edit them in {edits_path.name}, or --allow-flagged)")
    out = HERE / "prompts" / "e6_p1"
    (out / "records").mkdir(parents=True, exist_ok=True)
    n = 0
    with open(out / "records" / "test.jsonl", "w", encoding="utf-8") as fh:
        for line in open(E6 / "records" / "test.jsonl", encoding="utf-8"):
            r = json.loads(line)
            if r["id"] in rows:
                p1 = edits.get(r["id"], rows[r["id"]]["p1"])
                r = {**r, "meaning": " ".join(p1.split()), "meaning_p0": r["meaning"], "meaning_src": "full_grid P1"}
                n += 1
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    for name, target in (("records/val.jsonl", E6 / "records" / "val.jsonl"),
                         ("records/train.jsonl", E6 / "records" / "train.jsonl"),
                         ("leakage.json", E6 / "leakage.json")):
        link = out / name
        if not link.exists():
            os.symlink(os.path.relpath(target, link.parent), link)
    assert n == len(rows), f"{n} of {len(rows)} source poems found in the test split"
    print(f"{n} source poems re-prompted ({len(edits)} hand-edited, {len(flagged)} flagged kept) → {out}", flush=True)


if __name__ == "__main__":
    main()
