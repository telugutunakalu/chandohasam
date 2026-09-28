"""Level 2 — Length ratio of the bhavam to its verse.

Metric: r = |bhavam| / |verse|, where the verse is the lines the bhavam explains
(for a Bhagavatam seesa child, the parent's seesa lines as well). A poem passes
if 0.8 <= r <= 2.5 (config.LENGTH_RATIO_BOUNDS); |.| counts non-space
characters. Only verse poems with a Telugu bhavam are measured.

Per corpus: pass rate, mean, median, distribution, the most extreme poems.

Sense checks:
    * other units (words, aksharas): how much the verdict depends on |.|.
    * shuffled control: each verse with the bhavam of a random other poem of
      the same corpus. If wrong pairs pass as often as true ones, the gate can
      only catch a bhavam of implausible length, never a wrong one.
    * neighbour control: the bhavam of the previous poem of the same work.
    * direction of failure: too short (r < 0.8) or too long (r > 2.5). An
      edition bhavam that goes on into commentary fails "too long".

Writes outputs/level2_length_ratio.json

Run:  python level2_length_ratio.py [--datasets ...]
"""
import argparse
import statistics

import config
from common.controls import neighbour_index, shuffled_index
from common.dataset import add_dataset_argument, by_corpus, flat, load_poems, with_bhavam
from common.io import pct, print_table, save_result
from common.telugu import aksharas, non_space_chars, words

LO, HI = config.LENGTH_RATIO_BOUNDS
BINS = [(0.0, 0.5), (0.5, 0.8), (0.8, 1.5), (1.5, 2.5), (2.5, 5.0), (5.0, float("inf"))]
UNITS = {
    "characters": non_space_chars,
    "words": lambda t: len(words(t)),
    "aksharas": lambda t: len(aksharas(t)),
}


def ratio(verse: str, bhavam: str, unit) -> float:
    return unit(bhavam) / max(unit(verse), 1)


def summarise(rs) -> dict:
    n = len(rs)
    return {
        "n": n,
        "pass_pct": pct(sum(LO <= r <= HI for r in rs), n),
        "too_short_pct": pct(sum(r < LO for r in rs), n),
        "too_long_pct": pct(sum(r > HI for r in rs), n),
        "mean": statistics.fmean(rs) if rs else None,
        "median": statistics.median(rs) if rs else None,
        "bins": {f"{lo}-{hi}": sum(lo <= r < hi for r in rs) for lo, hi in BINS},
    }


def length_ratios(poems) -> dict:
    """{poem key: character ratio} for poems with a bhavam (used by cross_level_summary.py)."""
    return {p.key: ratio(flat(p.bhavam_verse), p.bhavam, UNITS["characters"]) for p in with_bhavam(poems)}


def main():
    ap = argparse.ArgumentParser()
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = with_bhavam(load_poems(tuple(args.datasets)))
    verses = [flat(p.bhavam_verse) for p in poems]
    shuffled = shuffled_index(poems, config.SEED)
    neighbour = neighbour_index(poems)
    index = {p.key: i for i, p in enumerate(poems)}

    result = {"bounds": [LO, HI], "corpora": {}}
    rows, unit_rows = [], []
    for corpus, group in by_corpus(poems).items():
        idx = [index[p.key] for p in group]
        entry = {}
        for name, unit in UNITS.items():
            true = [ratio(verses[i], poems[i].bhavam, unit) for i in idx]
            shuf = [ratio(verses[i], poems[shuffled[i]].bhavam, unit) for i in idx]
            neigh = [ratio(verses[i], poems[neighbour[i]].bhavam, unit) for i in idx if neighbour[i] >= 0]
            entry[name] = {"true": summarise(true), "shuffled": summarise(shuf), "neighbour": summarise(neigh)}
        chars = entry["characters"]
        order = sorted(idx, key=lambda i: ratio(verses[i], poems[i].bhavam, UNITS["characters"]))
        entry["extremes"] = {
            "lowest": [{"key": poems[i].key, "ratio": ratio(verses[i], poems[i].bhavam, UNITS["characters"]),
                        "verse": verses[i], "bhavam": poems[i].bhavam} for i in order[:3]],
            "highest": [{"key": poems[i].key, "ratio": ratio(verses[i], poems[i].bhavam, UNITS["characters"]),
                         "verse": verses[i], "bhavam": poems[i].bhavam[:600]} for i in order[-3:]],
        }
        result["corpora"][corpus] = entry
        rows.append([corpus, chars["true"]["n"], chars["true"]["mean"], chars["true"]["median"],
                     chars["true"]["pass_pct"], chars["true"]["too_short_pct"], chars["true"]["too_long_pct"],
                     chars["shuffled"]["pass_pct"], chars["neighbour"]["pass_pct"]])
        unit_rows.append([corpus, *(entry[u]["true"]["pass_pct"] for u in UNITS)])

    print_table(["corpus", "poems", "mean r", "median r", "PASS %", "too short %", "too long %",
                 "shuffled pass %", "neighbour pass %"], rows,
                f"Level 2 — |bhavam| / |verse| in non-space characters, pass if {LO} <= r <= {HI}")
    print_table(["corpus", *(f"pass % ({u})" for u in UNITS)], unit_rows, "Sense check — the unit of |.|")
    print_table(["corpus", *(f"{lo}-{hi}" for lo, hi in BINS)],
                [[c, *e["characters"]["true"]["bins"].values()] for c, e in result["corpora"].items()],
                "Distribution of r (characters)")
    save_result("level2_length_ratio", result)


if __name__ == "__main__":
    main()
