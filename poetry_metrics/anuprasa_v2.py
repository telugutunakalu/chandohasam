"""Metric 1, version 2.0 (candidate, under evaluation): anuprāsa with a chance model that no poet moves.

Version 1.0 (anuprasa.py) stays the default. Version 2.0 keeps its statistic,
its rubric and its output, and changes one thing: where the chance model's
consonant frequencies come from. Full comparison: reports/v2_comparison.md.

    version 1.0   p = the consonant frequencies of the four dataset files, the
                  same poems the metric is used to describe. A poet added to or
                  removed from them moves q and r, and with them every z and label.
    version 2.0   p = a constant of the language: the consonant frequencies of the
                  verse collection that prasāda's model was built from (362,247
                  crawled poems, none of them in the four dataset files), read once
                  from that model's akshara counts (baselines/prasada_ngrams.tsv.gz)
                  and frozen in baselines/anuprasa_v2_baseline.json.

The statistic is unchanged (anuprasa.py): per line, A same-sound pairs among the
M pairs of consonant tokens in different aksharas, E = qM, V = M(q - q^2) +
K(r - q^2), z = (A - E) / sqrt(V), with q = sum_s p_s^2 and r = sum_s p_s^3.
The rubric of version 1.0 was already free of any corpus (the one-sided 5%, 1%
and 0.1% points of the standard normal), and is kept:
    0 none    z < 1.645
    1 weak    1.645 <= z < 2.326
    2 marked  2.326 <= z < 3.090
    3 strong  z >= 3.090
The percentiles reported beside the score are against the four dataset files,
and are the one number here that is relative to them.

Why the frequencies cannot come from the poem itself, which would free the
metric of every corpus: a poem whose consonants are its own chance model cannot
show a sound carried through the whole poem, which is what the treatise calls
vṛttyanuprāsa (4.76). With that model the treatise's own example (4.77) scores
z = 0.17, and the pilot grid's sound figures are told from its meaning figures
with AUC 0.61 instead of 0.78 (compare_versions.py, section "corpus_free").

Usage:
    python3 anuprasa_v2.py score --text "line 1\\nline 2"      # or --file, --jsonl, --dataset, as anuprasa.py
    python3 anuprasa_v2.py build-baseline                      # -> baselines/anuprasa_v2_baseline.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import anuprasa as v1                                                       # noqa: E402
import prasada                                                              # noqa: E402
from common import corpus                                                   # noqa: E402
from common.phonology import SOUNDS, akshara_consonants                     # noqa: E402
from common.scoring import add_source_arguments, quantiles, read_poems, write_results   # noqa: E402

VERSION = "2.0"
BASELINE_PATH = HERE / "baselines" / "anuprasa_v2_baseline.json"


def language_counts() -> tuple[Counter, int]:
    """Consonant tokens of the language reference, from the akshara counts of prasāda's model:
    each akshara type adds its count to each of its consonant tokens. Returns (counts, aksharas)."""
    counts, n_aksharas = Counter(), 0
    for row in prasada._read_rows(prasada.NGRAMS_PATH):
        if row[0] == "1":
            akshara, count = row[1], int(row[2])
            n_aksharas += count
            for token in akshara_consonants(akshara):
                counts[token] += count
    return counts, n_aksharas


def chance_probabilities(counts: Counter) -> dict:
    """p_s with version 1.0's pseudo-count on every symbol."""
    total = sum(counts.values()) + v1.PSEUDO_COUNT * len(SOUNDS)
    return {s: (counts.get(s, 0) + v1.PSEUDO_COUNT) / total for s in SOUNDS}


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 anuprasa_v2.py build-baseline")
    return v1.load_baseline(path)            # adds the per-level frequencies, as for version 1.0


def build_baseline(args) -> None:
    """The frozen chance model, and (for the percentiles only) the reference distributions of the four files."""
    counts, n_aksharas = language_counts()
    probs = chance_probabilities(counts)
    level_probs = {name: v1.level_probabilities(probs, keyf) for name, keyf in v1.LEVELS.items()}
    meta = json.loads(prasada.BASELINE_PATH.read_text(encoding="utf-8"))
    poems = [p for c in args.corpora for p in corpus.load(c)]
    results = [v1.poem_levels(t, level_probs) for t in v1.tokens_of(poems)]
    reference = {name: {
        "line_z": quantiles([z for r in results for z in r[name][2]]),
        "poem_z": quantiles([r[name][0] for r in results]),
        "poem_score": quantiles([r[name][1] for r in results]),
    } for name in v1.LEVELS}
    baseline = {
        "metric": "anuprasa", "version": VERSION,
        "chance_model": "consonant frequencies of the language reference (prasāda's verse collection), frozen; "
                        "no statistic of the four dataset files enters a score or a label",
        "language_reference": {"source": f"baselines/{prasada.NGRAMS_PATH.name}, akshara unigram counts",
                               "poems": meta["reference_poems"], "aksharas": n_aksharas,
                               "excludes": "every poem of the four dataset files (matched on the first line)"},
        "n_tokens": sum(counts.values()), "pseudo_count": v1.PSEUDO_COUNT,
        "moments": {name: dict(zip(("q", "r"), (round(x, 6) for x in v1.moments(level_probs[name]))))
                    for name in v1.LEVELS},
        "counts": dict(counts.most_common()),
        "probabilities": {s: round(p, 8) for s, p in sorted(probs.items(), key=lambda kv: -kv[1])},
        "reference_corpora": list(args.corpora),
        "n_poems": len(poems), "n_lines": sum(len(p.lines) for p in poems),
        "reference": reference,
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {baseline['n_tokens']} consonant tokens of the language "
          f"reference; q, r = {baseline['moments']}")


def score_poem(lines, baseline: dict) -> dict:
    """Version 1.0's scoring under the frozen chance model."""
    result = v1.score_poem(lines, baseline)
    result["version"] = VERSION
    return result


def score(args) -> None:
    baseline = load_baseline()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="anuprāsa (alliteration density), version 2.0 candidate")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="the frozen chance model; reference distributions for percentiles")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA),
                   help="the files the percentiles refer to (the chance model does not depend on them)")
    b.set_defaults(func=build_baseline)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
