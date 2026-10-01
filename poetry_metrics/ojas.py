"""Metric 4 — ojas (word-density index): how long the words are and how tightly the syllables are bound.

What it measures. The classical texts give ojas two sources, and the proposal
asks for both (Appendix E.1: "average compound length and conjunct clusters per
syllable"). Full specification, sources and validation: specs/04_ojas.md.

    W  bound share      the percentage of the aksharas of printed words that continue a word,
                        i.e. are not its first: 100 * (1 - words / aksharas) = 100 * (1 - 1/L),
                        where L is the mean word length in aksharas
                        ojas as abundance of compounds: Daṇḍin 1.80 "ojaḥ samāsabhūyastvam";
                        the treatise 4.69 "సమాసభరితోజ్జ్వలబంధం బోజము"; Kāvyaprakāśa 8.75
    J  conjunct rate    the percentage of aksharas that begin with a conjunct
                        ojas as a tight texture: Vāmana 3.1.5 "gāḍhabandhatvam ojaḥ"

    ojas index   O = (W + J) / 2

O is the mean of two shares of the poem's own aksharas, so it is a percentage
and it uses no statistic of any corpus: a poem gets the same O whichever poets
the reference holds, and any new poet is scored on the same scale (version 2.0;
version 1.0 standardised L and J on the reference corpus, so its scale moved
when the corpus changed). The two shares spread about equally across poems
(standard deviations 4.7 and 5.1 points in the reference) and are unrelated
(Spearman 0.01), so weighting them equally lets neither dominate.

The form is that of the readability formulas: a sum of word length and a
second count (Flesch 1948). For Indic scripts Sinha et al. (2012) fitted
"1.37 * average word length + 0.005 * conjuncts" to readers' judgements of
Hindi text, and found the conjunct count the feature most correlated with
judged hardness. Their coefficients belong to Hindi prose and to their units;
here both terms are shares of aksharas, so they need no coefficient.

Word length stands in for compound length. A compound is printed as one word
in most editions, but an edition that prints its members apart will read
lower. True compound length needs the sandhi and compound splitter of metric 6.

Reported beside O, not in it: aspirated consonants per 100 aksharas. The
proposal lists them, but Vāmana's own example of a texture that is not tight
is the one with the aspirates (3.1.5), so they are left out of the index.

Rubric, on O, anchored to the treatise's own two examples, not to a corpus:
the light cut is the O of its example of words standing apart (mādhurya,
4.61), the dense cut the O of its example of ojas (4.70), and the interval
between them is split in three. Lines and poems share the cuts.
    0 light          below the treatise's words-apart example
    1 leaning light
    2 moderate
    3 leaning dense
    4 dense          at least as dense as the treatise's ojas example
The rubric describes; denser is not better. Mammaṭa places ojas in the heroic
rasa, and more of it in the repulsive and the furious (8.69-70). The
percentile against the reference poems is reported too, and that number,
unlike O and the level, is relative to the reference.

Usage:
    python3 ojas.py score --text "line 1\\nline 2"          # or --file poem.txt, --jsonl poems.jsonl
    python3 ojas.py score --dataset vemana --no-lines --out outputs/ojas_vemana.jsonl
    python3 ojas.py build-baseline                          # rebuilds baselines/ojas_baseline.json (anchors,
                                                            # cuts, reference percentiles; O itself needs none)
    python3 ojas.py validate                                # -> outputs/ojas_validation.json
"""
from __future__ import annotations

import argparse
import bisect
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                                   # noqa: E402
from common.phonology import aksharas, line_aksharas, normalise             # noqa: E402
from common.scoring import (add_source_arguments, percentile, quantiles,    # noqa: E402
                            read_poems, write_results)

VERSION = "2.0"
ASPIRATES = frozenset("ఖఘఛఝఠఢథధఫభ")
LABELS = ("light", "leaning_light", "moderate", "leaning_dense", "dense")
EXEMPLARS = HERE / "fixtures" / "classical_exemplars.json"
ANCHORS = {"light": "kas_4_61_madhurya",     # the treatise's mādhurya: words standing apart (4.60, 4.61)
           "dense": "kas_4_70_ojas"}         # the treatise's ojas: a texture filled with compounds (4.69, 4.70)
BASELINE_PATH = HERE / "baselines" / "ojas_baseline.json"
OUTPUT_DIR = HERE / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# the counts
# ---------------------------------------------------------------------------

@dataclass
class Counts:
    """One line (or, summed, one poem)."""
    words: int = 0               # printed words
    word_aksharas: int = 0       # their aksharas
    aksharas: int = 0            # aksharas with a vowel
    conjuncts: int = 0           # of these, beginning with two or more consonants
    aspirates: int = 0           # of these, holding an aspirated consonant
    longest: list = field(default_factory=list)      # (aksharas, word), the longest words

    @property
    def word_length(self):
        return self.word_aksharas / self.words if self.words else None

    @property
    def bound_share(self):
        """W: the percentage of the aksharas of printed words that continue a word, 100 * (1 - 1/L)."""
        return 100 * (1 - self.words / self.word_aksharas) if self.words else None

    @property
    def conjunct_rate(self):
        return 100 * self.conjuncts / self.aksharas if self.aksharas else None

    @property
    def aspirate_rate(self):
        return 100 * self.aspirates / self.aksharas if self.aksharas else None

    def __add__(self, other: "Counts") -> "Counts":
        return Counts(self.words + other.words, self.word_aksharas + other.word_aksharas,
                      self.aksharas + other.aksharas, self.conjuncts + other.conjuncts,
                      self.aspirates + other.aspirates, sorted(self.longest + other.longest, reverse=True)[:3])


def count_line(line: str) -> Counts:
    c = Counts()
    for word in normalise(line).split():
        n = len(aksharas(word))
        if n:
            c.words += 1
            c.word_aksharas += n
            c.longest.append((n, word))
    c.longest = sorted(c.longest, reverse=True)[:3]
    for a in line_aksharas(line):
        if a.vowel:
            c.aksharas += 1
            c.conjuncts += len(a.onset) >= 2
            c.aspirates += any(ch in ASPIRATES for ch in a.onset)
    return c


def count_poem(lines) -> list:
    return [count_line(line) for line in lines]


def pooled(counts: list) -> Counts:
    total = Counts()
    for c in counts:
        total = total + c
    return total


def index(c: Counts):
    """O = (W + J) / 2: the mean of two shares of the poem's own aksharas, in percent. No corpus constant."""
    if c.bound_share is None or c.conjunct_rate is None:
        return None
    return 0.5 * (c.bound_share + c.conjunct_rate)


def anchored_cuts() -> tuple[list, dict]:
    """The rubric's cut points from the treatise's two examples: [light, light + d, light + 2d, dense],
    d = (dense - light) / 3. Returns the cuts and the two anchors."""
    exemplars = {e["id"]: e for e in json.loads(EXEMPLARS.read_text(encoding="utf-8"))["exemplars"]}
    anchors = {}
    for pole, eid in ANCHORS.items():
        e = exemplars[eid]
        anchors[pole] = {"id": eid, "locus": e.get("locus"), "ojas": round(index(pooled(count_poem(e["lines"]))), 4)}
    lo, hi = anchors["light"]["ojas"], anchors["dense"]["ojas"]
    step = (hi - lo) / 3
    return [round(lo, 4), round(lo + step, 4), round(lo + 2 * step, 4), round(hi, 4)], anchors


def level_of(value, cuts: list):
    """Rubric level 0-4: how many cut points the value has reached."""
    return None if value is None else bisect.bisect_right(cuts, value)


# ---------------------------------------------------------------------------
# baseline
# ---------------------------------------------------------------------------

def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 ojas.py build-baseline")
    return json.loads(path.read_text(encoding="utf-8"))


def build_baseline(args) -> None:
    """Version 2.0: O needs no constant, so the baseline holds only the rubric's anchored cuts and, for the
    percentile reported beside O, the distributions of the reference corpus."""
    poems = [p for c in args.corpora for p in corpus.load(c)]
    per_poem = [count_poem(p.lines) for p in poems]
    totals = [pooled(counts) for counts in per_poem]
    lines = [c for counts in per_poem for c in counts]
    cuts, anchors = anchored_cuts()
    reference = {
        "line_index": quantiles([index(c) for c in lines]),
        "poem_index": quantiles([index(t) for t in totals]),
        "poem_bound_share": quantiles([t.bound_share for t in totals]),
        "poem_word_length": quantiles([t.word_length for t in totals]),
        "poem_conjunct_rate": quantiles([t.conjunct_rate for t in totals]),
        "poem_aspirate_rate": quantiles([t.aspirate_rate for t in totals]),
    }
    spread = {name: {"mean": round(statistics.fmean(v), 4), "sd": round(statistics.pstdev(v), 4)}
              for name, v in (("bound_share", [t.bound_share for t in totals if t.bound_share is not None]),
                              ("conjunct_rate", [t.conjunct_rate for t in totals if t.conjunct_rate is not None]))}
    everything = pooled(totals)
    baseline = {
        "metric": "ojas", "version": VERSION,
        "formula": "O = (W + J) / 2; W = 100 * (1 - words / aksharas of words); J = 100 * conjunct-initial aksharas / aksharas",
        "anchors": anchors,
        "cuts": {"line": cuts, "poem": cuts},
        "corpora": list(args.corpora),
        "n_poems": len(poems), "n_lines": len(lines), "n_words": everything.words, "n_aksharas": everything.aksharas,
        "reference_spread": spread,
        "corpus_word_length": round(everything.word_length, 4),
        "corpus_conjunct_rate": round(everything.conjunct_rate, 4),
        "corpus_aspirate_rate": round(everything.aspirate_rate, 4),
        "reference": reference,
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {baseline['n_poems']} poems; anchors {anchors}; cuts {cuts}")


# ---------------------------------------------------------------------------
# scoring
# ---------------------------------------------------------------------------

def _round(value, digits: int = 3):
    return None if value is None else round(value, digits)


def _describe(c: Counts, unit: str, baseline: dict) -> dict:
    o = index(c)
    level = level_of(o, baseline["cuts"][unit])
    return {
        "ojas": _round(o), "level": level, "label": None if level is None else LABELS[level],
        "percentile": percentile(o, baseline["reference"][f"{unit}_index"]),
        "bound_share": _round(c.bound_share, 2), "conjunct_rate": _round(c.conjunct_rate, 2),
        "word_length": _round(c.word_length),
        "aspirate_rate": _round(c.aspirate_rate, 2),
        "n_words": c.words, "n_aksharas": c.aksharas,
        "longest_words": [{"word": w, "aksharas": n} for n, w in c.longest],
    }


def score_poem(lines, baseline: dict) -> dict:
    counts = count_poem(lines)
    line_out = [{"text": text, **_describe(c, "line", baseline)} for text, c in zip(lines, counts)]
    poem = _describe(pooled(counts), "poem", baseline)
    return {"metric": "ojas", "version": VERSION, "score": poem["level"], **poem,
            "n_lines": len(line_out), "lines": line_out}


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def score(args) -> None:
    baseline = load_baseline()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def validate(args) -> None:
    import validation_ojas          # analysis, kept out of the metric itself
    validation_ojas.run(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="ojas (word-density index) metric")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="the anchored cut points and the reference distributions")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA))
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="classical contrasts, the gloss check, known groups, sensitivity")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
