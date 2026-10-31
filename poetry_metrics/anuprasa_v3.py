"""Metric 1, version 3.0: anuprāsa as repeated consonant n-grams across the whole poem.

Versions 1.0/2.0 (anuprasa.py/anuprasa_v2.py) score each line against a chance model of random
consonant pairing and pool the per-line z-scores. Version 3.0 instead counts literal repetition of
consonant patterns across the whole poem directly, with no chance model and no reference corpus:

    A = sum_{n=1}^{K} sum_{g: c(g)>1} n * (c(g) - 1) / N_c

g is a consonant n-gram (n akṣaras, vowels skipped, akṣaras taken by their first onset consonant);
c(g) is how many times it occurs in the poem; K is the longest n for which some n-gram repeats
(if no 1-gram repeats, A = 0); N_c is the number of consonant-bearing akṣaras in the poem. Each
repeated pattern contributes once per *extra* occurrence (c(g) - 1), weighted by its length n, so
a long repeated run counts for more than the same number of short, scattered repeats.

Rubric, anchored at the treatise's own vṛttānuprāsa example (4.77), whose score under this formula
is A* = 1.33 (provided; not independently re-derived here, since the example text itself is not in
this repository -- see anuprasa_v3_baseline.json's "note"):
    0 none    A <  A*/3
    1 weak    A*/3  <= A < 2A*/3
    2 marked  2A*/3 <= A < A*
    3 strong  A >= A*
This rubric needs no corpus at all: A* is a fixed constant, so `score` never requires
`build-baseline` to have run. `build-baseline` only computes the four dataset files' percentile
distribution, for the --no-lines percentile column, exactly as for v1/v2.

Usage:
    python3 anuprasa_v3.py score --text "line 1\\nline 2"     # or --file, --jsonl, --dataset
    python3 anuprasa_v3.py build-baseline                     # -> baselines/anuprasa_v3_baseline.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                                   # noqa: E402
from common.phonology import aksharas, parse_akshara                        # noqa: E402
from common.scoring import add_source_arguments, percentile, quantiles, read_poems, write_results  # noqa: E402

VERSION = "3.0"
BASELINE_PATH = HERE / "baselines" / "anuprasa_v3_baseline.json"
A_STAR = 1.33          # the treatise's own example (4.77), scored under this formula
CUTS = [A_STAR / 3, 2 * A_STAR / 3, A_STAR]
LABELS = ["none", "weak", "marked", "strong"]


def consonant_sequence(lines) -> list:
    """One symbol per consonant-bearing akṣara across the whole poem (its first onset consonant);
    a vowel-initial akṣara with no onset consonant is skipped ("vowels skipped")."""
    seq = []
    for line in lines:
        for ak_text in aksharas(line):
            ak = parse_akshara(ak_text)
            if ak.onset:
                seq.append(ak.onset[0])
    return seq


def level_of(value: float) -> int:
    for i, cut in enumerate(CUTS):
        if value < cut:
            return i
    return len(CUTS)


def anuprasa_score(lines) -> dict:
    """A, K, N_c and the n-grams that actually repeat, for one poem (whole-poem statistic -- not
    computed per line, unlike v1/v2)."""
    seq = consonant_sequence(lines)
    n_c = len(seq)
    if n_c == 0:
        return dict(A=0.0, K=0, n_c=0, repeats=[])

    total, k, repeats = 0.0, 0, []
    n = 1
    while n <= n_c:
        grams = Counter(tuple(seq[i:i + n]) for i in range(n_c - n + 1))
        repeated = {g: c for g, c in grams.items() if c > 1}
        if not repeated:
            break
        k = n
        total += sum(n * (c - 1) for c in repeated.values()) / n_c
        if n <= 3:  # keep only the short, legible examples in the output
            repeats += [{"pattern": "".join(g), "n": n, "count": c} for g, c in repeated.items()]
        n += 1
    return dict(A=total, K=k, n_c=n_c, repeats=sorted(repeats, key=lambda r: -r["n"] * r["count"])[:10])


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 anuprasa_v3.py build-baseline")
    return json.loads(path.read_text(encoding="utf-8"))


def build_baseline(args) -> None:
    poems = [p for c in args.corpora for p in corpus.load(c)]
    scores = [anuprasa_score(p.lines)["A"] for p in poems]
    baseline = {
        "metric": "anuprasa", "version": VERSION,
        "rubric": "fixed: A* = 1.33 (the treatise's own vrttanuprasa example, 4.77), "
                  "cuts at A*/3, 2A*/3, A* -- independent of any corpus",
        "note": "A* is the value given for the treatise's example under this formula; the example "
                "text itself is not in this repository, so A* is taken as provided, not re-derived here.",
        "a_star": A_STAR, "cuts": CUTS, "labels": LABELS,
        "reference_corpora": list(args.corpora),
        "n_poems": len(poems),
        "reference": {"poem_A": quantiles(scores)},   # for the --no-lines percentile column only
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {len(poems)} reference poems "
          f"(a_star={A_STAR}, cuts={CUTS})")


def score_poem(lines, baseline: dict | None = None) -> dict:
    s = anuprasa_score(lines)
    level = level_of(s["A"])
    result = {
        "metric": "anuprasa", "version": VERSION, "score": level, "anuprasa": round(s["A"], 4),
        "level": level, "label": LABELS[level], "longest_repeated_ngram": s["K"],
        "n_consonant_aksharas": s["n_c"], "repeated_patterns": s["repeats"],
    }
    if baseline is not None:
        result["percentile"] = percentile(s["A"], baseline["reference"]["poem_A"])
    return result


def score(args) -> None:
    baseline = load_baseline() if BASELINE_PATH.exists() else None
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="anuprāsa (alliteration), version 3.0: repeated "
                                              "consonant n-grams across the whole poem")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="the four dataset files' percentile distribution "
                                               "(the rubric itself needs no corpus)")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA))
    b.set_defaults(func=build_baseline)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
