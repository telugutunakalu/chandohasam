"""Metric 5 — prasāda (clarity index): how readily the text is recognised as known language.

What it measures. The treatise defines prasāda by well-known words
("ప్రసిద్ధపదంబుల", 4.57); Mammaṭa by meaning grasped on hearing alone
(Kāvyaprakāśa 8.76). The proposal names two proxies (Appendix E.1): average word
frequency, and perplexity under a language model. Both are computed here against
a reference of 362,247 poems of Telugu verse that does not contain the text
being scored. Full specification, sources and validation: specs/05_prasada.md.

Headline: surprisal under an akshara trigram model (bits per akshara).

    H = -(1/N) * sum_t log2 P(a_t | a_(t-2), a_(t-1))        perplexity = 2^H

The line is read as a stream of aksharas with the spaces taken out, so the
number does not depend on how an edition spaces its words. Surprisal is the
standard measure of how hard a word is to take in (Hale 2001; Smith & Levy 2013:
reading time is linear in it). P is a count model with Witten-Bell
interpolation (Witten & Bell 1991; Chen & Goodman 1999):

    P(a | g,h) = L3 * c(g,h,a)/c(g,h) + (1 - L3) * P(a | h)       L3 = c(g,h) / (c(g,h) + T(g,h))
    P(a | h)   = L2 * c(h,a)/c(h)     + (1 - L2) * P(a)           L2 = c(h)   / (c(h)   + T(h))
    P(a)       = L1 * c(a)/N          + (1 - L1) / (V + 1)        L1 = N / (N + V)

c counts occurrences in the reference, T(.) counts the distinct aksharas seen
after a context, N and V are its akshara tokens and types. An unseen akshara
gets the share 1/(V + 1) of the reserved mass.

Second number: word frequency on the Zipf scale (van Heuven et al. 2014).

    Zipf(w) = log10( (c(w) + 1) / ((T + W) / 10^6) ) + 3      T, W = word tokens and types of the reference

The mean Zipf of the printed words is the "average word frequency" of the
proposal (as in Kao & Jurafsky 2012), and the share of words found in the
reference is the familiar-word share of Dale & Chall (1948). Both depend on
word spacing and on sandhi, so they are reported beside H, not in it.

Rubric, on H, against the four dataset corpora (cut points = their 10th, 30th,
70th and 90th percentiles; lines and poems have their own). Lower H is clearer:
    4 clear            the clearest 10%
    3 leaning clear    10-30%
    2 ordinary         30-70%
    1 leaning obscure  70-90%
    0 obscure          the hardest 10%
Mammaṭa calls prasāda the quality common to every rasa (8.76), so here a higher
level is better.

Usage:
    python3 prasada.py score --text "line 1\\nline 2"       # or --file poem.txt, --jsonl poems.jsonl
    python3 prasada.py score --dataset vemana --no-lines --out outputs/prasada_vemana.jsonl
    python3 prasada.py build-baseline                       # needs ../diffusion_finetuning/data/records/train.jsonl
    python3 prasada.py validate                             # -> outputs/prasada_validation.json
"""
from __future__ import annotations

import argparse
import bisect
import gzip
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                                   # noqa: E402
from common.phonology import aksharas, normalise                            # noqa: E402
from common.scoring import (add_source_arguments, percentile, quantiles,    # noqa: E402
                            read_poems, write_results)

VERSION = "1.0"
ORDER = 3
MIN_BIGRAM, MIN_TRIGRAM, MIN_WORD = 2, 3, 2          # n-grams and words seen less often are not stored
BOS = "<s>"
LABELS = ("obscure", "leaning_obscure", "ordinary", "leaning_clear", "clear")
CUT_PERCENTILES = (10, 30, 70, 90)
REFERENCE_RECORDS = HERE.parent / "diffusion_finetuning" / "data" / "records" / "train.jsonl"
BASELINE_PATH = HERE / "baselines" / "prasada_baseline.json"
NGRAMS_PATH = HERE / "baselines" / "prasada_ngrams.tsv.gz"
WORDS_PATH = HERE / "baselines" / "prasada_words.tsv.gz"
OUTPUT_DIR = HERE / "outputs"
SEED = 42
_SPACE = re.compile(r"\s+")


def words_of(line: str) -> list:
    """The printed words of a line, normalised as the reference was."""
    return normalise(line).split()


# ---------------------------------------------------------------------------
# the model
# ---------------------------------------------------------------------------

class Model:
    """Akshara trigram model with Witten-Bell interpolation, and the word frequency list."""

    def __init__(self, unigrams: dict, bigrams: dict, trigrams: dict, words: dict, meta: dict):
        self.meta = meta
        self.n, self.v = meta["akshara_tokens"], meta["akshara_types"]
        self.ids = {a: i for i, a in enumerate([BOS] + sorted(unigrams))}
        self.k = len(self.ids)
        self.uni = {self.ids[a]: c for a, c in unigrams.items()}
        self.bi, self.bi_total, self.bi_types = {}, Counter(), Counter()
        for (h, a), c in bigrams.items():
            h, a = self.ids[h], self.ids[a]
            self.bi[h * self.k + a] = c
            self.bi_total[h] += c
            self.bi_types[h] += 1
        self.tri, self.tri_total, self.tri_types = {}, Counter(), Counter()
        for (g, h, a), c in trigrams.items():
            ctx = self.ids[g] * self.k + self.ids[h]
            self.tri[ctx * self.k + self.ids[a]] = c
            self.tri_total[ctx] += c
            self.tri_types[ctx] += 1
        self.words = words
        self.word_scale = (meta["word_tokens"] + meta["word_types"]) / 1e6

    def p1(self, a) -> float:
        lam = self.n / (self.n + self.v)
        return lam * self.uni.get(a, 0) / self.n + (1 - lam) / (self.v + 1)

    def p2(self, h, a) -> float:
        total = self.bi_total.get(h, 0) if h is not None else 0
        if not total:
            return self.p1(a)
        lam = total / (total + self.bi_types[h])
        seen = self.bi.get(h * self.k + a, 0) if a is not None else 0
        return lam * seen / total + (1 - lam) * self.p1(a)

    def p3(self, g, h, a) -> float:
        if g is None or h is None:
            return self.p2(h, a)
        ctx = g * self.k + h
        total = self.tri_total.get(ctx, 0)
        if not total:
            return self.p2(h, a)
        lam = total / (total + self.tri_types[ctx])
        seen = self.tri.get(ctx * self.k + a, 0) if a is not None else 0
        return lam * seen / total + (1 - lam) * self.p2(h, a)

    def bits(self, line: str, order: int = ORDER) -> tuple:
        """(aksharas, bits of each) for one line; the context starts afresh at the line's beginning."""
        aks = aksharas(line)
        ids = [self.ids[BOS]] + [self.ids.get(a) for a in aks]
        out = []
        for i in range(1, len(ids)):
            if order >= 3 and i >= 2:
                p = self.p3(ids[i - 2], ids[i - 1], ids[i])
            elif order >= 2:
                p = self.p2(ids[i - 1], ids[i])
            else:
                p = self.p1(ids[i])
            out.append(-math.log2(p))
        return aks, out

    def zipf(self, word: str) -> float:
        return math.log10((self.words.get(word, 0) + 1) / self.word_scale) + 3


def _read_rows(path: Path):
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n").split("\t")


def load_model() -> Model:
    for path in (BASELINE_PATH, NGRAMS_PATH, WORDS_PATH):
        if not path.exists():
            sys.exit(f"no baseline at {path}; run: python3 prasada.py build-baseline")
    meta = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    uni, bi, tri = {}, {}, {}
    for row in _read_rows(NGRAMS_PATH):
        count = int(row[-1])
        if row[0] == "1":
            uni[row[1]] = count
        elif row[0] == "2":
            bi[(row[1], row[2])] = count
        else:
            tri[(row[1], row[2], row[3])] = count
    words = {w: int(c) for w, c in _read_rows(WORDS_PATH)}
    return Model(uni, bi, tri, words, meta)


# ---------------------------------------------------------------------------
# scoring
# ---------------------------------------------------------------------------

def level_of(surprisal, cuts: list):
    """Rubric level 0-4; the lower the surprisal, the higher the level."""
    return None if surprisal is None else 4 - bisect.bisect_right(cuts, surprisal)


def line_stats(model: Model, line: str, order: int = ORDER) -> dict:
    aks, bits = model.bits(line, order)
    words = words_of(line)
    zipfs = [model.zipf(w) for w in words]
    return {"aksharas": aks, "bits": bits, "words": words, "zipfs": zipfs,
            "known": [w in model.words for w in words]}


def _mean(values):
    return sum(values) / len(values) if values else None


def _round(value, digits: int = 3):
    return None if value is None else round(value, digits)


def _describe(surprisal, zipf, known, unit: str, baseline: dict) -> dict:
    ref = baseline["reference"]
    level = level_of(surprisal, baseline["cuts"][unit])
    harder = percentile(surprisal, ref[f"{unit}_surprisal"])
    return {
        "surprisal": _round(surprisal), "perplexity": None if surprisal is None else round(2 ** surprisal, 1),
        "level": level, "label": None if level is None else LABELS[level],
        "percentile": None if harder is None else round(100 - harder, 1),      # 100 = the clearest of the reference
        "zipf": _round(zipf), "known_word_share": _round(known),
    }


def score_poem(lines, model: Model) -> dict:
    baseline = model.meta
    stats = [line_stats(model, line) for line in lines]
    line_out = []
    for text, s in zip(lines, stats):
        entry = {"text": text, **_describe(_mean(s["bits"]), _mean(s["zipfs"]), _mean(s["known"]), "line", baseline),
                 "n_aksharas": len(s["aksharas"])}
        hardest = sorted(range(len(s["bits"])), key=lambda i: -s["bits"][i])[:3]
        entry["hard_spots"] = [{"akshara": s["aksharas"][i], "after": "".join(s["aksharas"][max(0, i - 2):i]),
                                "bits": round(s["bits"][i], 1)} for i in sorted(hardest)]
        entry["unknown_words"] = [w for w, k in zip(s["words"], s["known"]) if not k]
        line_out.append(entry)
    bits = [b for s in stats for b in s["bits"]]
    zipfs = [z for s in stats for z in s["zipfs"]]
    known = [k for s in stats for k in s["known"]]
    poem = _describe(_mean(bits), _mean(zipfs), _mean(known), "poem", baseline)
    return {"metric": "prasada", "version": VERSION, "score": poem["level"], **poem,
            "n_aksharas": len(bits), "n_words": len(zipfs), "n_lines": len(line_out), "lines": line_out}


def poem_figures(model: Model, lines, order: int = ORDER) -> dict:
    """The poem-level numbers only (the fast path for corpus-scale runs)."""
    bits, zipfs, known = [], [], []
    for line in lines:
        bits += model.bits(line, order)[1]
        words = words_of(line)
        zipfs += [model.zipf(w) for w in words]
        known += [w in model.words for w in words]
    return {"surprisal": _mean(bits), "zipf": _mean(zipfs), "known_word_share": _mean(known), "n_aksharas": len(bits)}


# ---------------------------------------------------------------------------
# baseline: the reference counts, and the reference distributions of the four corpora
# ---------------------------------------------------------------------------

def _key(line: str) -> str:
    return _SPACE.sub("", normalise(line))


def reference_poems(records: Path = REFERENCE_RECORDS):
    """The lines of every reference poem that is not in the four dataset files
    (matched on the first line, spaces and punctuation ignored)."""
    own = {_key(p.lines[0]) for c in corpus.CORPORA for p in corpus.load(c)}
    with open(records, encoding="utf-8") as f:
        for raw in f:
            lines = json.loads(raw).get("lines") or []
            if lines and _key(lines[0]) not in own:
                yield lines


def _write_rows(path: Path, rows) -> None:
    """Tab-separated rows, gzipped with a fixed timestamp so that rebuilds are byte-identical."""
    with open(path, "wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        for row in rows:
            gz.write(("\t".join(str(x) for x in row) + "\n").encode("utf-8"))


def build_baseline(args) -> None:
    if not args.records.exists():
        sys.exit(f"the reference corpus is not at {args.records}")
    uni, bi, tri, words, n_poems, cache = Counter(), Counter(), Counter(), Counter(), 0, {}
    for lines in reference_poems(args.records):
        n_poems += 1
        for line in lines:
            seq = [BOS]
            for w in words_of(line):
                words[w] += 1
                if w not in cache:
                    cache[w] = aksharas(w)
                seq += cache[w]
            uni.update(seq[1:])
            bi.update(zip(seq, seq[1:]))
            tri.update(zip(seq, seq[1:], seq[2:]))
    bi = {k: c for k, c in bi.items() if c >= MIN_BIGRAM}
    tri = {k: c for k, c in tri.items() if c >= MIN_TRIGRAM}
    kept_words = {w: c for w, c in words.items() if c >= MIN_WORD}
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _write_rows(NGRAMS_PATH, [(1, a, c) for a, c in sorted(uni.items())]
                + [(2, *k, c) for k, c in sorted(bi.items())] + [(3, *k, c) for k, c in sorted(tri.items())])
    _write_rows(WORDS_PATH, sorted(kept_words.items()))
    meta = {
        "metric": "prasada", "version": VERSION, "order": ORDER,
        "reference": {}, "reference_corpus": args.records.name,
        "reference_poems": n_poems,
        "akshara_tokens": sum(uni.values()), "akshara_types": len(uni),
        "bigrams_kept": len(bi), "trigrams_kept": len(tri),
        "min_counts": {"bigram": MIN_BIGRAM, "trigram": MIN_TRIGRAM, "word": MIN_WORD},
        "word_tokens": sum(words.values()), "word_types": len(words), "words_kept": len(kept_words),
        "corpora": list(corpus.CORPORA), "cut_percentiles": list(CUT_PERCENTILES),
    }
    BASELINE_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")

    # the reference distributions: the four dataset corpora under the model just written
    model = load_model()
    poems = [p for c in corpus.CORPORA for p in corpus.load(c)]
    figures = [poem_figures(model, p.lines) for p in poems]
    line_bits = [_mean(model.bits(l)[1]) for p in poems for l in p.lines]
    meta["n_poems"], meta["n_lines"] = len(poems), len(line_bits)
    meta["reference"] = {
        "line_surprisal": quantiles(line_bits),
        "poem_surprisal": quantiles([f["surprisal"] for f in figures]),
        "poem_zipf": quantiles([f["zipf"] for f in figures]),
        "poem_known_word_share": quantiles([f["known_word_share"] for f in figures]),
    }
    meta["cuts"] = {unit: [meta["reference"][f"{unit}_surprisal"][k] for k in CUT_PERCENTILES]
                    for unit in ("line", "poem")}
    total_bits = sum(f["surprisal"] * f["n_aksharas"] for f in figures)
    meta["mean_surprisal"] = round(total_bits / sum(f["n_aksharas"] for f in figures), 4)
    BASELINE_PATH.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}, {NGRAMS_PATH.name}, {WORDS_PATH.name}: "
          f"{n_poems} reference poems, {meta['akshara_tokens']} aksharas, {len(bi)} bigrams, {len(tri)} trigrams, "
          f"{len(kept_words)} words; cuts {meta['cuts']}")


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def score(args) -> None:
    model = load_model()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, model))


def validate(args) -> None:
    import validation_prasada          # analysis, kept out of the metric itself
    validation_prasada.run(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="prasāda (clarity index) metric")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="reference counts, reference distributions and rubric cut points")
    b.add_argument("--records", type=Path, default=REFERENCE_RECORDS, help="the reference verse corpus (JSONL)")
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="classical examples, degradation controls, model orders")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
