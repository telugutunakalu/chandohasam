"""Metric 5, version 2.0 (candidate, under evaluation): prasāda with a rubric that no poet moves.

Version 1.0 (prasada.py) stays the default. Version 2.0 keeps its headline,
the surprisal H of the akshara trigram model, and keeps the model: the frozen
files in baselines/, built once from 362,247 crawled poems with every poem of
the four dataset files left out, and not rebuilt when the dataset changes. The
treatise defines prasāda by well-known words (4.57), so a record of what is
well known cannot be dropped; the model is that record. Full comparison:
reports/v2_comparison.md.

What changes is the rubric. Version 1.0 cut H at the 10th, 30th, 70th and 90th
percentiles of the four dataset files, so a poet added to or removed from them
moved every label. Version 2.0 anchors it to the treatise: its example of
prasāda, "well-known words" (4.57, 4.59), and its example of a word found only
in the śāstras and purāṇas (apratīta, 4.15), with the interval split in three.
Lower H is clearer, and lines and poems share the cuts:
    4 clear            H < 5.31          clearer than the treatise's example of prasāda
    3 leaning clear    5.31 <= H < 5.73
    2 ordinary         5.73 <= H < 6.14
    1 leaning obscure  6.14 <= H < 6.56
    0 obscure          H >= 6.56         at least as obscure as its example of apratīta
Of the treatise's word defects set against prasāda (spec §1), two lie in the
form of a word, which a model of familiar forms can see: apratīta and a word
poets do not use (aprayukta, 4.5, at 8.82 bits). The cut is at the clearer of
the two, so that both read "obscure"; the other two defects lie in the sense a
word is given (spec §6.1). With aprayukta as the anchor, the treatise's
apratīta example would read "ordinary" (compare_versions.py,
"alternative_rubrics").

The percentile reported beside H is against the four dataset files, and is the
one number here that is relative to them.

Usage:
    python3 prasada_v2.py score --text "line 1\\nline 2"       # or --file, --jsonl, --dataset, as prasada.py
    python3 prasada_v2.py build-baseline                       # -> baselines/prasada_v2_baseline.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import prasada as v1                                                        # noqa: E402
from common.scoring import add_source_arguments, read_poems, write_results  # noqa: E402

VERSION = "2.0"
EXEMPLARS = HERE / "fixtures" / "classical_exemplars.json"
ANCHORS = {"clear": "kas_4_59_prasada",      # the treatise's example of prasāda (4.57, 4.59)
           "obscure": "kas_4_15_apratita"}   # its example of a word found only in śāstras and purāṇas (4.15)
BASELINE_PATH = HERE / "baselines" / "prasada_v2_baseline.json"


def anchored_cuts(model: v1.Model) -> tuple[list, dict]:
    """[clear, clear + d, clear + 2d, obscure] in bits per akshara, d = (obscure - clear) / 3; and the anchors."""
    exemplars = {e["id"]: e for e in json.loads(EXEMPLARS.read_text(encoding="utf-8"))["exemplars"]}
    anchors = {}
    for pole, eid in ANCHORS.items():
        e = exemplars[eid]
        h = v1.poem_figures(model, e["lines"])["surprisal"]
        anchors[pole] = {"id": eid, "locus": e["locus"], "surprisal": h}
    lo, hi = anchors["clear"]["surprisal"], anchors["obscure"]["surprisal"]
    step = (hi - lo) / 3
    return [lo, lo + step, lo + 2 * step, hi], anchors        # unrounded: each example sits exactly on its cut


def load_model() -> v1.Model:
    """Version 1.0's frozen model, with the anchored cut points in place of the percentile ones."""
    if not BASELINE_PATH.exists():
        sys.exit(f"no baseline at {BASELINE_PATH}; run: python3 prasada_v2.py build-baseline")
    model = v1.load_model()
    own = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    model.meta = {**model.meta, "version": VERSION, "anchors": own["anchors"], "cuts": own["cuts"],
                  "reference_corpora": model.meta["corpora"]}
    return model


def build_baseline(args) -> None:
    cuts, anchors = anchored_cuts(v1.load_model())
    baseline = {
        "metric": "prasada", "version": VERSION,
        "rubric": "anchored to the treatise: its prasāda example (4.59) and its example of a word found only in "
                  "śāstras and purāṇas (apratīta, 4.15), the interval in thirds; the model is version 1.0's frozen "
                  "files; no statistic of the four dataset files",
        "anchors": anchors,
        "cuts": {"line": cuts, "poem": cuts},
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: anchors {anchors}; cuts {cuts}")


def score_poem(lines, model: v1.Model) -> dict:
    """Version 1.0's scoring under the anchored rubric."""
    result = v1.score_poem(lines, model)
    result["version"] = VERSION
    return result


def score(args) -> None:
    model = load_model()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, model))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="prasāda (clarity index), version 2.0 candidate")
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
