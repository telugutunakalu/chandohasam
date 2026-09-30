"""Metric 3 — mādhurya (euphony index): how soft or harsh a poem sounds.

What it measures: the balance of soft and harsh sound configurations, per
akshara, with harsh aksharas that stand next to each other counted more
heavily. Full specification, sources and validation: specs/03_madhurya.md.

Step 1, the class of each akshara, by its consonant onset:

    class      weight  members                                              source
    madhura     +1     M1  a stop or class nasal (not ట ఠ డ ఢ) right after    Kāvyaprakāśa 8.74; the
                           the anusvāra or its own class nasal: ంక ంగ ంద ంప,   treatise's saukumārya,
                           న్న మ్మ                                           "బొట్లు పిఱుందుల" (4.60)
                       M2  ర or ణ alone, with a short vowel and no coda      Kāvyaprakāśa 8.74
    sonorant    +1/2   a nasal, య ర ల వ ళ ఱ (single or doubled), or no      sonority scale (Parker 2008),
                       consonant at all (a vowel akshara)                   classes 7-17
    voiced       0     a voiced stop or affricate: గ ఘ జ ఝ ద ధ బ భ           classes 4-6
    voiceless  -1/2    a voiceless stop, affricate or fricative:            classes 1-3
                       క ఖ చ ఛ త థ ప ఫ స హ
    conjunct   -1/2    any other conjunct (స్త, త్య, ద్వ, జ్ఞ, ...)             conjuncts make the texture
                                                                            dense (treatise, on ojas)
    parusha     -1     P1  unaspirated + aspirated of one varga: క్ఖ ద్ధ      Kāvyaprakāśa 8.75; the
                       P2  a conjunct with ర: ప్ర ర్క త్ర                       treatise's paruṣa defect,
                       P3  a doubled stop: క్క త్త ద్ద                          "శ్రుతికటువు లైన పదములు"
                       P4  ట ఠ డ ఢ                                           (4.21)
                       P5  శ ష

Step 2, the sequence. An akshara is harsh when its weight is negative, and its
harshness is h = -w (1/2 or 1). A harsh run is a stretch of harsh aksharas with
nothing else between them. Along a run the harshness adds up:

    R_t = R_(t-1) + h_t   if akshara t is harsh,     R_t = 0 otherwise      (run load)

A harsh akshara is charged the load of its run so far, not only its own weight:

    w*_t = w_t   if akshara t is not harsh,          w*_t = -R_t   if it is

    mādhurya index   M = (1/N) * sum_t w*_t = I - P
    inventory        I = (1/N) * sum_t w_t                    the plain weighted proportion
    pile-up          P = (1/N) * sum over harsh t of R_(t-1)   >= 0

So a harsh akshara among soft ones costs its own weight, the second of two
together costs both, the third all three. P is 0, and M = I, when no two harsh
aksharas are adjacent. Any non-harsh akshara ends the run.

Where this comes from: Daṇḍin calls a texture tender when it is *mostly* of
non-harsh letters (aniṣṭhurākṣaraprāyam, Kāvyādarśa 1.69), and names its
opposite by the sequence, "hard to utter" (kṛcchrodyam, 1.72). The run load is
a cumulative sum in the sense of Page (1954), restarted at each non-harsh
akshara: a sustained run registers far more than the same sounds scattered.
I alone is the class-frequency measure of Fónagy (1961) and Auracher et al.
(2011).

A second number is reported beside M, the sonority score of Jacobs (2017,
2018): the mean sonority rank of every sound segment (vowels included), on
Parker's 17-point scale. It is an independent phonetic cross-check.

Rubric, on M, against the reference corpus (cut points = its 10th, 30th, 70th
and 90th percentiles, stored in the baseline; lines and poems have their own):
    0 harsh          bottom 10%
    1 leaning harsh  10-30%
    2 balanced       30-70%
    3 leaning soft   70-90%
    4 soft           top 10%
The rubric describes, it does not grade: the treatise calls harsh words a
defect in the tender rasas and a merit in the fierce ones.

Adjacency and runs go through the poem, across spaces and line ends.

Usage:
    python3 madhurya.py score --text "line 1\\nline 2"      # or --file poem.txt, --jsonl poems.jsonl
    python3 madhurya.py score --dataset vemana --no-lines --out outputs/madhurya_vemana.jsonl
    python3 madhurya.py build-baseline                      # rebuilds baselines/madhurya_baseline.json
    python3 madhurya.py validate                            # -> outputs/madhurya_validation.json
"""
from __future__ import annotations

import argparse
import bisect
import json
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                                   # noqa: E402
from common.phonology import (ANUSVARA, ASPIRATE_PAIRS, CLASS_NASALS, SHORT_VOWELS, SONORANTS,   # noqa: E402
                              SONORITY, SPARSHA, STOPS, VARGAS, VOICED_OBSTRUENTS, Akshara,
                              line_aksharas, segments)
from common.scoring import (add_source_arguments, percentile, quantiles,    # noqa: E402
                            read_poems, write_results)

VERSION = "1.1"
WEIGHTS = {"madhura": 1.0, "sonorant": 0.5, "voiced": 0.0, "voiceless": -0.5, "conjunct": -0.5, "parusha": -1.0}
CLASSES = tuple(WEIGHTS)
RULES = {
    "M1": "a stop or class nasal (not ట ఠ డ ఢ) after the anusvāra or its class nasal",
    "M2": "ర or ణ alone with a short vowel",
    "P1": "unaspirated + aspirated stop of one varga",
    "P2": "a conjunct with ర",
    "P3": "a doubled stop",
    "P4": "ట ఠ డ ఢ",
    "P5": "శ or ష",
}
LABELS = ("harsh", "leaning_harsh", "balanced", "leaning_soft", "soft")
CUT_PERCENTILES = (10, 30, 70, 90)
RETROFLEX_STOPS = frozenset("టఠడఢ")
NASAL_OF = {ch: v[4] for v in VARGAS for ch in v}
BASELINE_PATH = HERE / "baselines" / "madhurya_baseline.json"
OUTPUT_DIR = HERE / "outputs"
SEED = 42


# ---------------------------------------------------------------------------
# step 1: classes
# ---------------------------------------------------------------------------

def closes_with_nasal(prev: Akshara | None, cur: Akshara) -> bool:
    """Whether `prev` ends in the anusvāra, or in the class nasal of `cur`'s first consonant."""
    if prev is None or not prev.coda or not cur.onset:
        return False
    last = prev.coda[-1]
    return last == ANUSVARA or last == NASAL_OF.get(cur.onset[0])


def parusha_rules(onset: tuple) -> list:
    """The Kāvyaprakāśa 8.75 configurations the onset shows."""
    rules = []
    pairs = list(zip(onset, onset[1:]))
    if any(p in ASPIRATE_PAIRS for p in pairs):
        rules.append("P1")
    if len(onset) >= 2 and "ర" in onset:
        rules.append("P2")
    if any(a == b and a in STOPS for a, b in pairs):
        rules.append("P3")
    if any(c in RETROFLEX_STOPS for c in onset):
        rules.append("P4")
    if any(c in "శష" for c in onset):
        rules.append("P5")
    return rules


def classify(a: Akshara, after_nasal: bool = False) -> tuple:
    """(class, [rules]) of one akshara; (None, []) for a vowel-less chunk, which is not scored."""
    if not a.vowel:
        return None, []
    onset = a.onset
    rules = parusha_rules(onset)
    if rules:
        return "parusha", rules
    single = len(onset) == 1
    doubled = len(onset) == 2 and onset[0] == onset[1]
    if (single and onset[0] in SPARSHA and after_nasal) or (doubled and onset[0] in CLASS_NASALS):
        return "madhura", ["M1"]
    if single and onset[0] in "రణ" and a.vowel in SHORT_VOWELS and not a.coda:
        return "madhura", ["M2"]
    if not onset:
        return "sonorant", []
    if single or doubled:
        c = onset[0]
        return ("sonorant" if c in SONORANTS else "voiced" if c in VOICED_OBSTRUENTS else "voiceless"), []
    return "conjunct", []


# ---------------------------------------------------------------------------
# step 2: the sequence
# ---------------------------------------------------------------------------

@dataclass
class Run:
    """A harsh run of two or more aksharas."""
    line: int            # index of the line it starts in
    aksharas: list       # their text
    load: float          # its final run load: the summed harshness


@dataclass
class Profile:
    """One line (or, summed, one poem)."""
    classes: Counter = field(default_factory=Counter)      # class -> aksharas
    rules: Counter = field(default_factory=Counter)        # rule -> aksharas showing it
    weight_sum: float = 0.0                                # sum of class weights
    pileup_sum: float = 0.0                                # sum over harsh aksharas of the load carried to them
    sonority_sum: int = 0
    n_segments: int = 0
    marked: list = field(default_factory=list)             # (akshara text, class, rules) for the two poles
    runs: list = field(default_factory=list)               # harsh runs starting here

    @property
    def n(self) -> int:
        return sum(self.classes.values())

    @property
    def inventory(self):
        return self.weight_sum / self.n if self.n else None

    @property
    def pileup(self):
        return self.pileup_sum / self.n if self.n else None

    def index(self):
        return (self.weight_sum - self.pileup_sum) / self.n if self.n else None

    @property
    def sonority(self):
        return self.sonority_sum / self.n_segments if self.n_segments else None

    def __add__(self, other: "Profile") -> "Profile":
        return Profile(self.classes + other.classes, self.rules + other.rules,
                       self.weight_sum + other.weight_sum, self.pileup_sum + other.pileup_sum,
                       self.sonority_sum + other.sonority_sum, self.n_segments + other.n_segments,
                       runs=self.runs + other.runs)


def profile_poem(lines) -> list:
    """One Profile per line. Adjacency and harsh runs are carried from line to line."""
    profiles, prev, load, run = [], None, 0.0, None
    for number, line in enumerate(lines):
        prof = Profile()
        for a in line_aksharas(line):
            segs = segments(a)
            prof.sonority_sum += sum(SONORITY[s] for s in segs)
            prof.n_segments += len(segs)
            cls, rules = classify(a, closes_with_nasal(prev, a))
            prev = a
            if cls is None:
                continue
            w = WEIGHTS[cls]
            prof.classes[cls] += 1
            prof.weight_sum += w
            prof.rules.update(rules)
            if rules:
                prof.marked.append((a.text, cls, rules))
            if w < 0:
                prof.pileup_sum += load                     # the load carried to this akshara
                if load == 0.0:
                    run = Run(number, [], 0.0)
                load -= w
                run.aksharas.append(a.text)
                run.load = load
                if len(run.aksharas) == 2:              # it is a run now: file it under the line it began in
                    (profiles[run.line] if run.line < number else prof).runs.append(run)
            else:
                load = 0.0
        profiles.append(prof)
    return profiles


def profile_line(line: str) -> Profile:
    """The Profile of one line on its own."""
    return profile_poem([line])[0]


def pooled(profiles: list) -> Profile:
    total = Profile()
    for p in profiles:
        total = total + p
    return total


def level_of(value, cuts: list):
    """Rubric level 0-4: how many cut points the value has reached."""
    return None if value is None else bisect.bisect_right(cuts, value)


# ---------------------------------------------------------------------------
# baseline: reference distributions and cut points
# ---------------------------------------------------------------------------

def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 madhurya.py build-baseline")
    return json.loads(path.read_text(encoding="utf-8"))


def build_baseline(args) -> None:
    poems = [p for c in args.corpora for p in corpus.load(c)]
    per_poem = [profile_poem(p.lines) for p in poems]
    totals = [pooled(profiles) for profiles in per_poem]
    everything = pooled(totals)
    lines = [prof for profiles in per_poem for prof in profiles]
    reference = {
        "line_index": quantiles([prof.index() for prof in lines]),
        "poem_index": quantiles([t.index() for t in totals]),
        "line_inventory": quantiles([prof.inventory for prof in lines]),
        "poem_inventory": quantiles([t.inventory for t in totals]),
        "line_pileup": quantiles([prof.pileup for prof in lines]),
        "poem_pileup": quantiles([t.pileup for t in totals]),
        "line_sonority": quantiles([prof.sonority for prof in lines]),
        "poem_sonority": quantiles([t.sonority for t in totals]),
    }
    baseline = {
        "metric": "madhurya", "version": VERSION, "corpora": list(args.corpora),
        "n_poems": len(poems), "n_lines": sum(len(p.lines) for p in poems), "n_aksharas": everything.n,
        "weights": WEIGHTS,
        "class_shares": {c: round(everything.classes[c] / everything.n, 5) for c in CLASSES},
        "rules_per_100_aksharas": {r: round(100 * everything.rules[r] / everything.n, 3) for r in RULES},
        "mean_index": round(everything.index(), 5),
        "mean_inventory": round(everything.inventory, 5),
        "mean_pileup": round(everything.pileup, 5),
        "mean_sonority": round(everything.sonority, 4),
        "cut_percentiles": list(CUT_PERCENTILES),
        "cuts": {unit: [reference[f"{unit}_index"][k] for k in CUT_PERCENTILES] for unit in ("line", "poem")},
        "reference": reference,
    }
    BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {BASELINE_PATH.relative_to(HERE)}: {baseline['n_poems']} poems, "
          f"{baseline['n_lines']} lines, {baseline['n_aksharas']} aksharas; cuts {baseline['cuts']}")


# ---------------------------------------------------------------------------
# scoring one poem, with the per-line explanation
# ---------------------------------------------------------------------------

def _round(value, digits: int = 4):
    return None if value is None else round(value, digits)


def _describe(prof: Profile, unit: str, baseline: dict) -> dict:
    ref, m = baseline["reference"], prof.index()
    level = level_of(m, baseline["cuts"][unit])
    return {
        "madhurya": _round(m),
        "level": level, "label": None if level is None else LABELS[level],
        "percentile": percentile(m, ref[f"{unit}_index"]),
        "inventory": _round(prof.inventory),
        "pileup": _round(prof.pileup),
        "pileup_percentile": percentile(prof.pileup, ref[f"{unit}_pileup"]),
        "sonority": _round(prof.sonority, 3),
        "sonority_percentile": percentile(prof.sonority, ref[f"{unit}_sonority"]),
        "n_aksharas": prof.n,
        "classes": {c: prof.classes[c] for c in CLASSES},
    }


def _run(run: Run) -> dict:
    return {"aksharas": "".join(run.aksharas), "length": len(run.aksharas), "load": run.load}


def score_poem(lines, baseline: dict) -> dict:
    profiles = profile_poem(lines)
    line_out = []
    for text, prof in zip(lines, profiles):
        entry = {"text": text, **_describe(prof, "line", baseline)}
        entry["soft"] = [{"akshara": t, "rule": r[0]} for t, c, r in prof.marked if c == "madhura"]
        entry["harsh"] = [{"akshara": t, "rules": r} for t, c, r in prof.marked if c == "parusha"]
        entry["harsh_runs"] = [_run(r) for r in prof.runs]
        line_out.append(entry)
    total = pooled(profiles)
    poem = _describe(total, "poem", baseline)
    heaviest = max(total.runs, key=lambda r: r.load, default=None)
    return {"metric": "madhurya", "version": VERSION, "score": poem["level"], **poem,
            "rules": {r: total.rules[r] for r in RULES},
            "harshest_run": None if heaviest is None else _run(heaviest),
            "n_lines": len(line_out), "lines": line_out}


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def score(args) -> None:
    baseline = load_baseline()
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline))


def validate(args) -> None:
    import validation_madhurya          # analysis, kept out of the metric itself
    validation_madhurya.run(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="mādhurya (euphony index) metric")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="reference distributions and rubric cut points")
    b.add_argument("--corpora", nargs="+", choices=list(corpus.CORPORA), default=list(corpus.CORPORA))
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="classical exemplars, known groups, sensitivity")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
