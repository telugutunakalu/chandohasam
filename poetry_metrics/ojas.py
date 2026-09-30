"""Metric 4 — ojas (word-density index): how long the words are and how tightly the syllables are bound.

What it measures. The classical texts give ojas two sources, and the proposal
asks for both (Appendix E.1: "average compound length and conjunct clusters per
syllable"). Full specification, sources and validation: specs/04_ojas.md.

    L  word length      aksharas per printed word, the mean over the poem
                        ojas as abundance of compounds: Daṇḍin 1.80 "ojaḥ samāsabhūyastvam";
                        the treatise 4.69 "సమాసభరితోజ్జ్వలబంధం బోజము"; Kāvyaprakāśa 8.75
    J  conjunct rate    aksharas that begin with a conjunct, per 100 aksharas
                        ojas as a tight texture: Vāmana 3.1.5 "gāḍhabandhatvam ojaḥ"

    ojas index   O = 1/2 * ( (L - mu_L) / sd_L  +  (J - mu_J) / sd_J )

mu and sd are the mean and standard deviation of L and J over the poems of the
reference corpus, frozen in the baseline. O is 0 for a poem of average word
length and average conjunct rate, and positive for a denser one.

The form is that of the readability formulas: a weighted sum of word length
and a second count (Flesch 1948). For Indic scripts Sinha et al. (2012) fitted
"1.37 * average word length + 0.005 * conjuncts" to readers' judgements of
Hindi text, and found the conjunct count the feature most correlated with
judged hardness. Their coefficients belong to Hindi prose and to their units,
so here each term is put on the scale of Telugu verse by standardising it, and
the two are weighted equally.

Word length stands in for compound length. A compound is printed as one word
in most editions, but an edition that prints its members apart will read
lower. True compound length needs the sandhi and compound splitter of metric 6.

Reported beside O, not in it: aspirated consonants per 100 aksharas. The
proposal lists them, but Vāmana's own example of a texture that is not tight
is the one with the aspirates (3.1.5), so they are left out of the index.

Rubric, on O, against the reference corpus (cut points = its 10th, 30th, 70th
and 90th percentiles; lines and poems have their own):
    0 light          bottom 10%
    1 leaning light  10-30%
    2 moderate       30-70%
    3 leaning dense  70-90%
    4 dense          top 10%
The rubric describes; denser is not better. Mammaṭa places ojas in the heroic
rasa, and more of it in the repulsive and the furious (8.69-70).

Usage:
    python3 ojas.py score --text "line 1\\nline 2"          # or --file poem.txt, --jsonl poems.jsonl
    python3 ojas.py score --dataset vemana --no-lines --out outputs/ojas_vemana.jsonl
    python3 ojas.py build-baseline                          # rebuilds baselines/ojas_baseline.json
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

VERSION = "1.0"
ASPIRATES = frozenset("ఖఘఛఝఠఢథధఫభ")
LABELS = ("light", "leaning_light", "moderate", "leaning_dense", "dense")
CUT_PERCENTILES = (10, 30, 70, 90)
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


def index(c: Counts, scale: dict):
    """O: the mean of the two standardised terms."""
    if c.word_length is None or c.conjunct_rate is None:
        return None
    return 0.5 * ((c.word_length - scale["word_length"]["mean"]) / scale["word_length"]["sd"]
                  + (c.conjunct_rate - scale["conjunct_rate"]["mean"]) / scale["conjunct_rate"]["sd"])


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
    poems = [p for c in args.corpora for p in corpus.load(c)]
    per_poem = [count_poem(p.lines) for p in poems]
    totals = [pooled(counts) for counts in per_poem]
    lines = [c for counts in per_poem for c in counts]
    scale = {}
    for name in ("word_length", "conjunct_rate"):
        values = [getattr(t, name) for t in totals if getattr(t, name) is not None]
        scale[name] = {"mean": round(statistics.fmean(values), 5), "sd": round(statistics.pstdev(values), 5)}
    reference = {
        "line_index": quantiles([index(c, scale) for c in lines]),
        "poem_index": quantiles([index(t, scale) for t in totals]),
        "poem_word_length": quantiles([t.word_length for t in totals]),
        "poem_conjunct_rate": quantiles([t.conjunct_rate for t in totals]),
        "poem_aspirate_rate": quantiles([t.aspirate_rate for t in totals]),
    }
    everything = pooled(totals)
    baseline = {
        "metric": "ojas", "version": VERSION, "corpora": list(args.corpora),
        "n_poems": len(poems), "n_lines": len(lines), "n_words": everything.words, "n_aksharas": everything.aksharas,
        "scale": scale,
        "corpus_word_length": round(everything.word_length, 4),
        "corpus_conjunct_rate": round(everything.conjunct_rate, 4),
        "corpus_aspirate_rate": round(everything.aspirate_rate, 4),
        "cut_percentiles": list(CUT_PERCENTILES),
        "cuts": {unit: [reference[f"{unit}_index"][k] for k in CUT_PERCENTILES] for unit in ("line", "poem")},
        "reference": reference,
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {baseline['n_poems']} poems, {baseline['n_words']} words; "
          f"scale {scale}; cuts {baseline['cuts']}")


# ---------------------------------------------------------------------------
# scoring
# ---------------------------------------------------------------------------

def _round(value, digits: int = 3):
    return None if value is None else round(value, digits)


def _describe(c: Counts, unit: str, baseline: dict) -> dict:
    o = index(c, baseline["scale"])
    level = level_of(o, baseline["cuts"][unit])
    return {
        "ojas": _round(o), "level": level, "label": None if level is None else LABELS[level],
        "percentile": percentile(o, baseline["reference"][f"{unit}_index"]),
        "word_length": _round(c.word_length), "conjunct_rate": _round(c.conjunct_rate, 2),
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

    b = sub.add_parser("build-baseline", help="the scale of the two terms, reference distributions, cut points")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA))
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="classical contrasts, the gloss check, known groups, sensitivity")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
