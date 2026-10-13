"""Metric 3, version 2.0 (candidate, under evaluation): mādhurya with a rubric that no poet moves.

Version 1.1 (madhurya.py) stays the default. Its index M = I - P is already
free of any corpus: fixed class weights and a fixed sequence rule. Its rubric
was not: the cut points were the 10th, 30th, 70th and 90th percentiles of the
four dataset files, so a poet added to or removed from them moved every label.
Version 2.0 keeps M and anchors the rubric to the scale and to the treatise.
Full comparison: reports/v2_comparison.md.

    M = 0  is the balance point of the scale: the class weights are symmetric
           (+1, +1/2, 0, -1/2, -1) and a voiced stop weighs 0, so at M = 0 the
           soft and the harsh weights cancel.
    a      the M of the treatise's example of saukumārya (4.62), 0.394.

    cut points -a, -a/3, +a/3, +a, for lines and poems alike:
        0 harsh          M < -a           as far below balance as the treatise's soft example is above it
        1 leaning harsh  -a <= M < -a/3
        2 balanced       -a/3 <= M < a/3
        3 leaning soft   a/3 <= M < a
        4 soft           M >= a           at least as soft as the treatise's example

Every harsh example of the root texts lies below -a (the mildest, Kāvyaprakāśa
8.75, at -0.476). The treatise's own harsh example (4.21, -1.25) is one
compound built to show the defect, harsher than all but 3 of the 12,704
reference poems, so it is not used as a cut point: with the cuts in thirds
between it and 4.62, four of the six harsh examples of the texts would read
"balanced" (compare_versions.py, "alternative_rubrics").

The rubric describes; softer is not better (spec §5). The percentile reported
beside M is against the four dataset files, and is the one number here that is
relative to them.

Usage:
    python3 madhurya_v2.py score --text "line 1\\nline 2"      # or --file, --jsonl, --dataset, as madhurya.py
    python3 madhurya_v2.py build-baseline                      # -> baselines/madhurya_v2_baseline.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import madhurya as v1                                                       # noqa: E402
from common.scoring import add_source_arguments, read_poems, write_results  # noqa: E402

VERSION = "2.0"
EXEMPLARS = HERE / "fixtures" / "classical_exemplars.json"
ANCHOR = "kas_4_62_saukumarya"           # the treatise's example of saukumārya (4.60, 4.62)
BASELINE_PATH = HERE / "baselines" / "madhurya_v2_baseline.json"


def anchored_cuts() -> tuple[list, dict]:
    """[-a, -a/3, a/3, a], a = M of the treatise's soft example; and the anchor."""
    e = next(e for e in json.loads(EXEMPLARS.read_text(encoding="utf-8"))["exemplars"] if e["id"] == ANCHOR)
    a = v1.pooled(v1.profile_poem(e["lines"])).index()
    anchor = {"id": ANCHOR, "locus": e["locus"], "madhurya": a}
    return [-a, -a / 3, a / 3, a], anchor              # unrounded, so that the example itself is "soft"


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    """The anchored cut points, with version 1.1's reference quantiles for the percentiles."""
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 madhurya_v2.py build-baseline")
    own = json.loads(path.read_text(encoding="utf-8"))
    reference = v1.load_baseline()
    return {**own, "reference": reference["reference"], "reference_corpora": reference["corpora"]}


def build_baseline(args) -> None:
    cuts, anchor = anchored_cuts()
    baseline = {
        "metric": "madhurya", "version": VERSION,
        "rubric": "symmetric about M = 0, the balance point of the weights; outer cuts at the M of the treatise's "
                  "saukumārya example (4.62), inner cuts at a third of it; no statistic of any corpus",
        "anchor": anchor,
        "cuts": {"line": cuts, "poem": cuts},
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: anchor {anchor}; cuts {cuts}")


def score_poem(lines, baseline: dict) -> dict:
    """Version 1.1's scoring under the anchored rubric."""
    result = v1.score_poem(lines, baseline)
    result["version"] = VERSION
    return result


def score(args) -> None:
    baseline = load_baseline()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="mādhurya (euphony index), version 2.0 candidate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="the anchored cut points")
    b.set_defaults(func=build_baseline)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
