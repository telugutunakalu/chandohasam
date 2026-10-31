#!/usr/bin/env python3
"""Publish the human-evaluation results to results/, with every annotator's username replaced by a code (A1, A2, …).

    annotation_app/.venv/bin/python publish_results.py          # → results/{study1,study2,llm_judge}/

The reports are written elsewhere by their own scripts, with usernames, into folders git ignores; this copies the
current ones here pseudonymised (the user's decision 2026-10-31: raw ratings committed, no names):
- ratings: every rating of both studies (current answers), exported by padya_eval.report from read-only copies of the
  live databases (SQLite's backup API; nothing in them changes), with the annotator's code and group;
- study 1: ../paper/analysis/human_eval_study1.md (the paper's final analysis, group A) and human_eval_drift.md;
- study 2: annotation_app/reports/study2_results/ (study2_results.py) and reports/study2/selection.* (the pool);
- LLM judge: llm_judge/results/*_vs_human*.{md,json} (judge_vs_human.py) and ../paper/analysis/llm_judge_vs_human.md.

The codes are fixed in annotation_app/instance/pseudonyms.json (gitignored): the study-1 annotators who rated, in the
order their accounts were made, then anyone new. Every text written is checked: a username, or the two-letter pair
abbreviations of the paper's report (ma–sa), left anywhere stops the script.
"""
from __future__ import annotations

import collections
import csv
import io
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE / "annotation_app"
PAPER = HERE.parent / "paper" / "analysis"
OUT = HERE / "results"
MAPPING = APP / "instance" / "pseudonyms.json"
DBS = {"study1": APP / "instance" / "annotations.db", "study2": APP / "instance" / "annotations_study2.db"}
COPIES = {                                    # source → published path under results/
    PAPER / "human_eval_study1.md": "study1/results.md",
    PAPER / "human_eval_drift.md": "study1/drift.md",
    APP / "reports" / "study2_results" / "results.md": "study2/results.md",
    APP / "reports" / "study2_results" / "results.json": "study2/results.json",
    APP / "reports" / "study2_results" / "agreement.md": "study2/agreement.md",
    APP / "reports" / "study2_results" / "agreement.json": "study2/agreement.json",
    APP / "reports" / "study2" / "selection.md": "study2/selection.md",
    APP / "reports" / "study2" / "selection.json": "study2/selection.json",
    PAPER / "llm_judge_vs_human.md": "llm_judge/paper_tables.md",          # both ρ tests; Table 5 is like-for-like
    **{p: f"llm_judge/{p.name}" for p in sorted((HERE / "llm_judge" / "results").glob("*_vs_human*"))},
}


def annotators(db: Path) -> list[tuple[str, int]]:
    """(username, ratings) in the order the accounts were made, read-only."""
    c = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        return c.execute("SELECT username, (SELECT COUNT(*) FROM annotations a WHERE a.annotator_id = n.id) "
                         "FROM annotators n ORDER BY created_at, id").fetchall()
    finally:
        c.close()


def mapping() -> dict:
    """The fixed username → code map, extended (never renumbered) when someone new has rated."""
    codes = json.loads(MAPPING.read_text(encoding="utf-8")) if MAPPING.exists() else {}
    for db in DBS.values():
        for user, n in annotators(db):
            if n and user not in codes:
                codes[user] = f"A{len(codes) + 1}"
    MAPPING.write_text(json.dumps(codes, indent=1) + "\n", encoding="utf-8")
    MAPPING.chmod(0o600)
    return codes


def abbreviations(codes: dict) -> dict:
    """The paper's pair labels use a username's first two letters (ma–sa); only the unambiguous ones."""
    first = collections.Counter(u[:2] for u in codes)
    return {u[:2]: c for u, c in codes.items() if first[u[:2]] == 1}


def pseudonymise(text: str, codes: dict) -> str:
    for user in sorted(codes, key=len, reverse=True):          # longest first: a name may contain another
        text = re.sub(rf"\b{re.escape(user)}\b", codes[user], text)
    ab = abbreviations(codes)
    return re.sub(r"\b([a-z]{2})–([a-z]{2})\b",
                  lambda m: f"{ab[m[1]]}–{ab[m[2]]}" if m[1] in ab and m[2] in ab else m[0], text)


def leftovers(text: str, codes: dict) -> list[str]:
    names = re.findall(r"\b(?:" + "|".join(map(re.escape, codes)) + r")\b", text, flags=re.I)
    ab = abbreviations(codes)
    pairs = [f"{a}–{b}" for a, b in re.findall(r"\b([a-z]{2})–([a-z]{2})\b", text) if a in ab and b in ab]
    return names + pairs


def ratings(study: str, db: Path, tmp: Path, codes: dict, group_a: set) -> str:
    copy = tmp / db.name
    src = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    dst = sqlite3.connect(copy)
    src.backup(dst)
    src.close()
    dst.close()
    subprocess.run([sys.executable, "-m", "padya_eval.report", "--study", study[-1], "--db", str(copy),
                    "--out", str(tmp / study), "--bootstrap", "0"], cwd=APP, check=True, capture_output=True)
    rows = list(csv.DictReader(open(tmp / study / "annotations.csv", encoding="utf-8")))
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=["annotator", "group"] + [k for k in rows[0] if k != "annotator"])
    w.writeheader()
    for r in rows:
        w.writerow({**r, "annotator": codes[r["annotator"]], "group": "A" if r["annotator"] in group_a else "B"})
    return buf.getvalue()


def main() -> int:
    sys.path.insert(0, str(APP))
    from state_analysis import GROUP_A                          # the three annotators the paper reports
    codes = mapping()
    written = {}
    with tempfile.TemporaryDirectory() as t:
        for study, db in DBS.items():
            written[f"{study}/ratings.csv"] = ratings(study, db, Path(t), codes, set(GROUP_A))
    for src, dst in COPIES.items():
        if not src.exists():
            print(f"missing (run its script first): {src}", file=sys.stderr)
            return 1
        written[dst] = pseudonymise(src.read_text(encoding="utf-8"), codes)
    bad = {dst: left for dst, text in written.items() if (left := leftovers(text, codes))}
    if bad:
        print(f"names left, nothing written: {bad}", file=sys.stderr)
        return 1
    if OUT.exists():
        shutil.rmtree(OUT)
    for dst, text in written.items():
        (OUT / dst).parent.mkdir(parents=True, exist_ok=True)
        (OUT / dst).write_text(text, encoding="utf-8")
    groups = {codes[u]: ("A" if u in GROUP_A else "B") for u in codes}
    print(f"{len(written)} files → {OUT}; codes {dict(sorted(groups.items()))} (group A is what the paper reports)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
