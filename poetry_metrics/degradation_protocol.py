"""The proposal's degradation protocol, run on every metric of the suite.

The proposal (Evaluation Plans): "each metric is scored on canonical verse
against systematically degraded versions (word-shuffled, synonym-swapped,
meter-broken, filler-injected) and admitted only if it declines monotonically;
a metrically valid nonsense control must be rejected by every meaning metric."

Each degradation is applied at four strengths to the same sample of real poems
(seeded), and every metric is scored on every version:

    word_shuffle   a share of the poem's words change places (every line keeps its word count)
    meter_break    a share of the aksharas are edited: deleted, given another akshara of the poem
                   as a new neighbour, or changed in the length of the vowel
    filler         a share of the words are replaced by one akshara repeated to the word's length,
                   the filler found in the constrained poems (reports/generated_samples.md, finding 6)
    synonym_swap   a share of the verse's units are replaced by their gloss. Bhāgavatamu only: its
                   edition glosses every verse unit by unit. The ladder starts from the units
                   themselves (the verse with sandhi and compounds taken apart), so that its steps
                   differ only in the swap.

The metrics, each as the number that should fall if the verse gets worse:

    anuprasa   z of the same-sound pair count (varga level)
    madhurya   M
    ojas       O
    prasada    clarity, -H (bits per akshara)
    chandas    skill, 1 - rate / chance rate, against the poem's labelled meter

Verdict per metric and degradation, from the paired differences (degraded minus
original) over the sample:

    declines             the mean falls at every step, and at full strength the sign test has z <= -3.09
    declines, not monotone   the sign test is met and some step goes up
    rises                at full strength the sign test has z >= 3.09: the metric rewards the degradation
    no response          neither

The nonsense control is the constrained-decoding poems; its figures are read
from outputs/samples_analysis.json (run samples_analysis.py first).

    python3 degradation_protocol.py        # -> outputs/degradation_protocol.json
"""
from __future__ import annotations

import argparse
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import chandas_distance as cd               # noqa: E402
import samples_analysis as sa               # noqa: E402
from common import corpus                   # noqa: E402
from indic_meter_dawg import scansion as sc  # noqa: E402

SEED = 42
POEMS_PER_CORPUS = 400
LEVELS = {"word_shuffle": (0.10, 0.25, 0.50, 1.00), "meter_break": (0.02, 0.05, 0.10, 0.25),
          "filler": (0.10, 0.25, 0.50, 1.00), "synonym_swap": (0.10, 0.25, 0.50, 1.00)}
METRICS = {"anuprasa": lambda r: r["anuprasa_varga_z"], "madhurya": lambda r: r["madhurya"],
           "ojas": lambda r: r["ojas"], "prasada": lambda r: None if r["surprisal"] is None else -r["surprisal"],
           "chandas": lambda r: r["chandas_skill"]}
FILLERS = ("మ", "న", "ల", "ర", "త")
MIN_UNITS = 5                   # a verse enters the synonym ladder with at least this many glossed units
Z_CUT = 3.09                    # one-sided 0.001
LENGTHEN = {"ి": "ీ", "ు": "ూ", "ె": "ే", "ొ": "ో", "అ": "ఆ", "ఇ": "ఈ", "ఉ": "ఊ", "ఎ": "ఏ", "ఒ": "ఓ"}
SHORTEN = {long: short for short, long in LENGTHEN.items()}
LONG_A = "ా"
BRACKETED = re.compile(r"\([^)]*\)|\{[^}]*\}|\[[^\]]*\]")


# ---------------------------------------------------------------------------
# the degradations
# ---------------------------------------------------------------------------

def word_shuffle(lines: list, share: float, rng: random.Random) -> list:
    rows = [line.split() for line in lines]
    places = [(i, j) for i, row in enumerate(rows) for j in range(len(row))]
    chosen = rng.sample(places, min(len(places), max(2, round(share * len(places)))))
    words = [rows[i][j] for i, j in chosen]
    rng.shuffle(words)
    for (i, j), word in zip(chosen, words):
        rows[i][j] = word
    return [" ".join(row) for row in rows]


def change_length(syllable) -> str | None:
    """The akshara with its vowel's length changed; None when it has no short or long counterpart."""
    text = syllable.text
    for k, ch in enumerate(text):
        if ch in LENGTHEN or ch in SHORTEN:
            return text[:k] + (LENGTHEN.get(ch) or SHORTEN[ch]) + text[k + 1:]
        if ch == LONG_A:
            return text[:k] + text[k + 1:]
    if syllable.vowel == "అ" and syllable.onset:
        last = max(k for k, ch in enumerate(text) if ch in sc.CONSONANTS and not text[k + 1:k + 2] == sc.VIRAMA_CHAR)
        return text[:last + 1] + LONG_A + text[last + 1:]
    return None


def meter_break(lines: list, share: float, rng: random.Random) -> list:
    syllables = [sc.syllabify(line) for line in lines]
    places = [(i, j) for i, row in enumerate(syllables) for j in range(len(row))]
    chosen = sorted(rng.sample(places, min(len(places), max(1, round(share * len(places))))), reverse=True)
    out = list(lines)
    for i, j in chosen:                       # right to left, so earlier offsets stay valid
        s = syllables[i][j]
        op = rng.choice(("delete", "insert", "length"))
        new = change_length(s) if op == "length" else None
        if op == "insert":
            a, b = rng.choice(places)
            new = s.text + syllables[a][b].text
        out[i] = out[i][:s.start] + (new or "") + out[i][s.end:]
    return out


def filler(lines: list, share: float, rng: random.Random) -> list:
    rows = [line.split() for line in lines]
    places = [(i, j) for i, row in enumerate(rows) for j in range(len(row))]
    akshara = rng.choice(FILLERS)
    for i, j in rng.sample(places, min(len(places), max(1, round(share * len(places))))):
        rows[i][j] = akshara * max(1, len(sc.syllabify(rows[i][j])))
    return [" ".join(row) for row in rows]


def gloss_units(record: dict) -> list:
    """(verse unit, its gloss) for the units of a verse that have a gloss."""
    units = []
    for pair in record.get("teeka_pairs") or []:
        word = BRACKETED.sub("", pair.get("word") or "").strip()
        meaning = BRACKETED.sub("", pair.get("meaning") or "").split(" - ")[0].strip(" ,;")
        if word and meaning:
            units.append((word, meaning))
    return units


def synonym_swap(units: list, n_lines: int, share: float, rng: random.Random) -> list:
    """The verse as its units, a share of them replaced by their gloss, laid out on n_lines lines."""
    swap = set(rng.sample(range(len(units)), round(share * len(units)))) if share else set()
    words = [meaning if k in swap else word for k, (word, meaning) in enumerate(units)]
    per_line = math.ceil(len(words) / n_lines)
    return [" ".join(words[k:k + per_line]) for k in range(0, len(words), per_line)]


# ---------------------------------------------------------------------------
# the protocol
# ---------------------------------------------------------------------------

def sample_poems(rng: random.Random) -> list:
    known = set(cd.load_baseline()["meters"])
    out = []
    for name in corpus.CORPORA:
        labelled = [(p, cd.NAME_MAP.get(p.metre, p.metre)) for p in corpus.load(name)]
        labelled = [(p, m) for p, m in labelled if m in known]
        out.extend(rng.sample(labelled, min(POEMS_PER_CORPUS, len(labelled))))
    return out


def ladder(originals: list, versions: dict) -> dict:
    """Per metric: the mean at each strength, the paired comparison with the original, the verdict."""
    out = {}
    for metric, value in METRICS.items():
        base = [value(r) for r in originals]
        steps, means = [], [statistics.fmean(v for v in base if v is not None)]
        for level, rows in versions.items():
            pairs = [(b, value(r)) for b, r in zip(base, rows) if b is not None and value(r) is not None]
            lower = sum(d < b for b, d in pairs)
            higher = sum(d > b for b, d in pairs)
            z = (higher - lower) / math.sqrt(higher + lower) if higher + lower else 0.0     # the last one decides
            means.append(statistics.fmean(d for _, d in pairs))
            steps.append({"strength": level, "n": len(pairs), "mean": round(means[-1], 4),
                          "mean_change": round(statistics.fmean(d - b for b, d in pairs), 4),
                          "lower_pct": round(100 * lower / len(pairs), 1),
                          "higher_pct": round(100 * higher / len(pairs), 1), "sign_z": round(z, 2)})
        monotone = all(b < a for a, b in zip(means, means[1:]))
        verdict = ("declines" if monotone else "declines, not monotone") if z <= -Z_CUT else \
            "rises" if z >= Z_CUT else "no response"
        out[metric] = {"original_mean": round(means[0], 4), "steps": steps, "monotone_decline": monotone,
                       "verdict": verdict}
    return out


def nonsense_control() -> dict | None:
    """The constrained-decoding poems against real verse, per metric (from samples_analysis.json)."""
    path = HERE / "outputs" / "samples_analysis.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    cells = {k: v for k, v in report["cells"].items() if not k.endswith("| baseline")}
    keys = {"anuprasa": "anuprasa_varga_z", "madhurya": "madhurya", "ojas": "ojas", "prasada": "surprisal",
            "chandas": "chandas_skill"}
    out = {"cells": len(cells), "poems": sum(c["n"] for c in cells.values())}
    for metric, key in keys.items():
        above = [c["against_real"][key]["p_generated_above_real"] for c in cells.values()]
        above = [1 - a for a in above] if metric == "prasada" else above      # clarity is -H
        out[metric] = {"p_nonsense_scores_above_real_min": round(min(above), 4),
                       "p_nonsense_scores_above_real_max": round(max(above), 4)}
    return out


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args(argv)
    rng = random.Random(args.seed)
    baselines, none = sa.load_baselines(), frozenset()
    poems = sample_poems(rng)

    def score(lines, meter):
        return sa.score(lines, baselines, none, meter)

    originals = [score(list(p.lines), meter) for p, meter in poems]
    report = {"seed": args.seed, "poems": len(poems), "poems_per_corpus": POEMS_PER_CORPUS,
              "levels": {k: list(v) for k, v in LEVELS.items()}, "z_cut": Z_CUT, "degradations": {}}
    for name, degrade in (("word_shuffle", word_shuffle), ("meter_break", meter_break), ("filler", filler)):
        versions = {level: [score(degrade(list(p.lines), level, rng), meter) for p, meter in poems]
                    for level in LEVELS[name]}
        report["degradations"][name] = ladder(originals, versions)
        print(name, {m: v["verdict"] for m, v in report["degradations"][name].items()})

    records = {f"bhagavatam:{r['id']}": r for r in
               json.loads((corpus.DATASET_DIR / corpus.CORPORA["bhagavatam"]).read_text(encoding="utf-8"))}
    glossed = [(p, meter, gloss_units(records[p.key])) for p, meter in poems if p.corpus == "bhagavatam"]
    glossed = [(p, meter, units) for p, meter, units in glossed if len(units) >= MIN_UNITS]
    units_only = [score(synonym_swap(units, len(p.lines), 0, rng), meter) for p, meter, units in glossed]
    versions = {level: [score(synonym_swap(units, len(p.lines), level, rng), meter) for p, meter, units in glossed]
                for level in LEVELS["synonym_swap"]}
    report["degradations"]["synonym_swap"] = ladder(units_only, versions)
    report["synonym_swap_poems"] = len(glossed)
    printed = [score(list(p.lines), meter) for p, meter, _ in glossed]
    report["synonym_swap_printed_verse_mean"] = {
        m: round(statistics.fmean(v for v in map(value, printed) if v is not None), 4) for m, value in METRICS.items()}
    print("synonym_swap", {m: v["verdict"] for m, v in report["degradations"]["synonym_swap"].items()})

    report["nonsense_control"] = nonsense_control()
    out = HERE / "outputs" / "degradation_protocol.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {out.relative_to(HERE)}")


if __name__ == "__main__":
    main()
