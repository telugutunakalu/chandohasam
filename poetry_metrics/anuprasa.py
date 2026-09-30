"""Metric 1 — anuprāsa (alliteration density), with vṛttyanuprāsa.

What it measures: how much more a line repeats its consonants than chance
would, where chance is set by the consonant frequencies of the reference
corpus. Frequent consonants (న, ర, ల, మ, ...) repeat in any Telugu line;
scoring against their corpus frequency keeps that noise out of the score.
Full specification, sources and validation: specs/01_anuprasa.md.

Two levels, one statistic:
    varga  the four stops of a varga that differ only in voicing or aspiration
           count as one sound (k/kh/g/gh, c/ch/j/jh, ...); nasals, semivowels,
           sibilants, h and the anusvāra stand alone. This is the proposal's
           "consonant-class recurrence" (Appendix E.1) and the headline.
    varna  only the identical consonant counts: vṛttyanuprāsa, "one or more
           consonants repeated many times" (Viśvanātha, via Barbadikar &
           Kulkarni 2024).

Statistic (per line). The line's n consonant tokens are counted per sound s
(x_s). Pairs of tokens inside one akshara (a conjunct) are left out, because
their co-occurrence is phonotactics, not the poet's choice:
    M  = pairs of tokens in different aksharas
    A  = pairs of tokens in different aksharas that are the same sound
    q  = sum_s p_s^2,  r = sum_s p_s^3        p = reference-corpus frequencies
    E  = q M
    V  = M (q - q^2) + K (r - q^2)            K = sum_t d_t (d_t - 1), d_t = pairs token t is in
    z  = (A - E) / sqrt(V)
A / M is Simpson's (1949) index of the line's consonants and q is the same
index for the corpus. E and V are the exact mean and variance of A if the
line's consonants were drawn independently at their corpus frequencies (the
chance model of Skinner 1939 and Benner 2014). lift = (A / M) / q is the same
excess as an observed/expected ratio: 2.0 means twice the chance rate of
repeats.

Rubric, per line, on the varga z (one-sided 5%, 1% and 0.1% points of the
standard normal):
    0 none    z < 1.645
    1 weak    1.645 <= z < 2.326
    2 marked  2.326 <= z < 3.090
    3 strong  z >= 3.090
A poem's score is the mean level of its lines (0-3). Its z pools the lines
(A, E and V add over lines) and says how sure we are that the poem as a whole
repeats beyond chance; lift says by how much.

Usage:
    python3 anuprasa.py score --text "line 1\\nline 2"      # or --file poem.txt, --jsonl poems.jsonl
    python3 anuprasa.py score --dataset vemana --no-lines --out outputs/anuprasa_vemana.jsonl
    python3 anuprasa.py build-baseline                      # rebuilds baselines/anuprasa_baseline.json
    python3 anuprasa.py validate                            # controls -> outputs/anuprasa_validation.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                        # noqa: E402
from common.phonology import CLASS_OF, SOUNDS, Token, line_tokens, series  # noqa: E402
from common.scoring import (add_source_arguments, percentile, quantiles,   # noqa: E402
                            read_poems, write_results)

VERSION = "1.0"
LEVELS = {
    "varga": lambda t: series(t.char),        # headline
    "varna": lambda t: t.char,                # vṛttyanuprāsa
}
HEADLINE = "varga"
RUBRIC = ((3.090, 3, "strong"), (2.326, 2, "marked"), (1.645, 1, "weak"))
LABELS = {0: "none", 1: "weak", 2: "marked", 3: "strong"}
PSEUDO_COUNT = 0.5
BASELINE_PATH = HERE / "baselines" / "anuprasa_baseline.json"
OUTPUT_DIR = HERE / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# the statistic
# ---------------------------------------------------------------------------

@dataclass
class LineStat:
    n: int               # consonant tokens
    pairs: int           # M
    overlap: int         # K
    observed: int        # A
    expected: float      # E
    variance: float      # V
    counts: Counter      # x_s

    @property
    def z(self):
        return (self.observed - self.expected) / math.sqrt(self.variance) if self.variance > 0 else None

    @property
    def rate(self):
        return self.observed / self.pairs if self.pairs else None


def moments(probs: dict) -> tuple:
    """(q, r): the chance that 2 (3) independent draws are the same sound."""
    return sum(p * p for p in probs.values()), sum(p ** 3 for p in probs.values())


def level_probabilities(varna_probs: dict, keyf) -> dict:
    """Sound frequencies at a level, summed from the consonant frequencies."""
    out = Counter()
    for ch, p in varna_probs.items():
        out[keyf(Token(ch, 0, CLASS_OF[ch]))] += p
    return dict(out)


def line_stat(tokens, keyf, probs: dict) -> LineStat:
    n = len(tokens)
    per_akshara = Counter(t.akshara for t in tokens)
    counts = Counter(keyf(t) for t in tokens)
    within = Counter((keyf(t), t.akshara) for t in tokens)
    pairs = n * (n - 1) // 2 - sum(c * (c - 1) // 2 for c in per_akshara.values())
    observed = (sum(c * (c - 1) // 2 for c in counts.values())
                - sum(c * (c - 1) // 2 for c in within.values()))
    overlap = sum(d * (d - 1) for d in (n - per_akshara[t.akshara] for t in tokens))
    q, r = moments(probs)
    return LineStat(n, pairs, overlap, observed, q * pairs, pairs * (q - q * q) + overlap * (r - q * q), counts)


def rubric(z) -> int:
    if z is None:
        return 0
    for cut, level, _ in RUBRIC:
        if z >= cut:
            return level
    return 0


def binomial_tail(x: int, n: int, p: float) -> float:
    """P(X >= x) for X ~ Binomial(n, p)."""
    return max(0.0, 1.0 - sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(x)))


def carriers(stat: LineStat, tokens, keyf, probs: dict, aks: list, top: int = 3) -> list:
    """The sounds that carry the repetition: Benner's (2014) binomial test of each
    sound's count against its corpus frequency, most surprising first."""
    out = []
    for s, x in stat.counts.items():
        expected = stat.n * probs[s]
        if x >= 2 and x > expected:
            out.append({
                "sound": s, "count": x, "expected": round(expected, 2),
                "p": float(f"{binomial_tail(x, stat.n, probs[s]):.3g}"),
                "aksharas": [aks[a] for a in sorted({t.akshara for t in tokens if keyf(t) == s})],
            })
    out.sort(key=lambda c: (c["p"], -c["count"]))
    return out[:top]


# ---------------------------------------------------------------------------
# baseline: corpus frequencies and reference distributions
# ---------------------------------------------------------------------------

def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 anuprasa.py build-baseline")
    baseline = json.loads(path.read_text(encoding="utf-8"))
    baseline["level_probs"] = {name: level_probabilities(baseline["probabilities"], keyf)
                               for name, keyf in LEVELS.items()}
    return baseline


def pooled(stats: list):
    """(z, lift) of a poem from its line stats."""
    a = sum(s.observed for s in stats)
    e = sum(s.expected for s in stats)
    v = sum(s.variance for s in stats)
    m = sum(s.pairs for s in stats)
    z = (a - e) / math.sqrt(v) if v > 0 else None
    lift = (a / m) / (e / m) if m and e else None
    return z, lift


def poem_levels(line_tokens_list: list, level_probs: dict, levels: dict = LEVELS) -> dict:
    """{level: (poem z, poem score, [line z])} — the fast path for corpus-scale runs."""
    out = {}
    for name, keyf in levels.items():
        stats = [line_stat(t, keyf, level_probs[name]) for t in line_tokens_list]
        zs = [s.z for s in stats]
        score = sum(rubric(z) for z in zs) / len(zs) if zs else 0.0
        out[name] = (pooled(stats)[0], score, zs)
    return out


def tokens_of(poems) -> list:
    return [[line_tokens(l)[1] for l in p.lines] for p in poems]


# ---------------------------------------------------------------------------
# scoring one poem, with the per-line explanation
# ---------------------------------------------------------------------------

def score_poem(lines, baseline: dict) -> dict:
    ref = baseline["reference"]
    parsed = [(text, *line_tokens(text)) for text in lines]
    line_out = [{"text": text, "n_aksharas": len(aks)} for text, aks, _ in parsed]
    poem = {}
    for name, keyf in LEVELS.items():
        probs = baseline["level_probs"][name]
        stats = []
        for (text, aks, tokens), lo in zip(parsed, line_out):
            s = line_stat(tokens, keyf, probs)
            stats.append(s)
            level = rubric(s.z)
            lo["n_consonants"] = s.n
            lo[name] = {
                "z": None if s.z is None else round(s.z, 3),
                "lift": None if s.rate is None else round(s.rate / moments(probs)[0], 3),
                "level": level, "label": LABELS[level],
                "percentile": percentile(s.z, ref[name]["line_z"]),
                "repeats": s.observed, "pairs": s.pairs, "expected_repeats": round(s.expected, 2),
                "carriers": carriers(s, tokens, keyf, probs, aks),
            }
        z, lift = pooled(stats)
        score = sum(lo[name]["level"] for lo in line_out) / len(line_out) if line_out else 0.0
        poem[name] = {
            "score": round(score, 3), "label": LABELS[int(score + 0.5)],
            "z": None if z is None else round(z, 3), "lift": None if lift is None else round(lift, 3),
            "z_percentile": percentile(z, ref[name]["poem_z"]),
            "score_percentile": percentile(score, ref[name]["poem_score"]),
            "lines_with_anuprasa": sum(1 for lo in line_out if lo[name]["level"] >= 1),
        }
    head = poem[HEADLINE]
    return {"metric": "anuprasa", "version": VERSION, "score": head["score"], "label": head["label"],
            "z": head["z"], **poem, "n_lines": len(line_out), "lines": line_out}


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def build_baseline(args) -> None:
    poems = [p for c in args.corpora for p in corpus.load(c)]
    toks = tokens_of(poems)
    counts = Counter(t.char for lines in toks for line in lines for t in line)
    total = sum(counts.values()) + PSEUDO_COUNT * len(SOUNDS)
    probs = {s: (counts.get(s, 0) + PSEUDO_COUNT) / total for s in SOUNDS}
    level_probs = {name: level_probabilities(probs, keyf) for name, keyf in LEVELS.items()}
    results = [poem_levels(t, level_probs) for t in toks]
    reference = {name: {
        "line_z": quantiles([z for r in results for z in r[name][2]]),
        "poem_z": quantiles([r[name][0] for r in results]),
        "poem_score": quantiles([r[name][1] for r in results]),
    } for name in LEVELS}
    baseline = {
        "metric": "anuprasa", "version": VERSION, "corpora": list(args.corpora),
        "n_poems": len(poems), "n_lines": sum(len(p.lines) for p in poems), "n_tokens": sum(counts.values()),
        "pseudo_count": PSEUDO_COUNT,
        "counts": dict(counts.most_common()),
        "probabilities": {s: round(p, 8) for s, p in sorted(probs.items(), key=lambda kv: -kv[1])},
        "reference": reference,
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {baseline['n_poems']} poems, "
          f"{baseline['n_lines']} lines, {baseline['n_tokens']} consonant tokens")


def score(args) -> None:
    baseline = load_baseline()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def validate(args) -> None:
    import validation_anuprasa          # analysis, kept out of the metric itself
    validation_anuprasa.run(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="anuprāsa (alliteration density) metric")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="corpus frequencies and reference distributions")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA))
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="controls, ablations and known groups")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
