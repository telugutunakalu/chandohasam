"""Level 2 — Length ratio check (§5.2, Table 14).

Paper's metric: r = |P| / |V| (Telugu prose meaning over verse); pass if r is
in the window [0.8, 2.5]. Reported: 99.1% pass (27,633/27,881), mean 1.63,
median 1.61, five largest 5.11 4.73 4.71 4.65 4.36.

The paper does not define |.|. It is reproduced exactly (every Table 14 bin,
the pass count and the five extremes) by:
    |.| = non-whitespace characters, P taken raw (the "తెలుగు:" / "Telugu:"
    prefix left by the generation prompt is counted), window half-open [0.8, 2.5)
That is the "paper" variant below; "cleaned" strips the prefix.

Sense checks added:
    * other units (words, aksharas), to show how much the verdict depends on |.|
    * shuffled control: each poem paired with a random other couplet's prose.
      If mismatched pairs pass as often as true pairs, the gate cannot detect a
      wrong gloss, only one of implausible length.
    * neighbour control: the previous couplet of the same source.
    * what the failures are: records whose Telugu meaning field also holds the
      English gloss (the "extreme ratios" the paper reads as bad translations).

Writes outputs/level2_length_ratio.json and outputs/cache/level2_ratios.json

Run:  python level2_length_ratio.py
"""
import json
import random
import re
import statistics

import config
from common.dataset import clean_meaning, load_subset, poem_flat, source_of
from common.io import pct, print_table, save_result
from common.telugu import aksharas, non_space_chars, words

LO, HI = config.LENGTH_RATIO_BOUNDS
BINS = [(0.5, 0.8), (0.8, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, float("inf"))]

# name -> (length function, prose field getter, upper bound inclusive?)
VARIANTS = {
    "paper":            (non_space_chars, lambda r: r["telugu_meaning"], False),
    "cleaned":          (non_space_chars, lambda r: clean_meaning(r["telugu_meaning"]), False),
    "cleaned_words":    (lambda t: len(words(t)), lambda r: clean_meaning(r["telugu_meaning"]), False),
    "cleaned_aksharas": (lambda t: len(aksharas(t)), lambda r: clean_meaning(r["telugu_meaning"]), False),
}


def passes(r, hi_inclusive):
    return LO <= r <= HI if hi_inclusive else LO <= r < HI


def ratios(verses, proses, length):
    return [length(p) / max(length(v), 1) for v, p in zip(verses, proses)]


def summarise(rs, hi_inclusive):
    ok = sum(passes(r, hi_inclusive) for r in rs)
    return {"n": len(rs), "pass_n": ok, "pass_pct": pct(ok, len(rs)),
            "mean": statistics.fmean(rs), "median": statistics.median(rs),
            "bins": {f"{lo:.2f}-{hi:.2f}": sum(lo <= r < hi for r in rs) for lo, hi in BINS}}


def neighbour_prose(records, proses):
    """Prose of the previous record from the same source (ids are file order)."""
    last_by_source, out = {}, []
    for r, p in zip(records, proses):
        src = source_of(r)
        out.append(last_by_source.get(src))
        last_by_source[src] = p
    return out


def main():
    master = load_subset("master")
    verses = [r["poem"] for r in master]
    rng = random.Random(config.SEED)
    perm = list(range(len(master)))
    rng.shuffle(perm)

    result = {"paper_reported": config.PAPER["level2"], "variants": {}}
    rows = []
    for name, (length, prose_of, hi_inc) in VARIANTS.items():
        proses = [prose_of(r) for r in master]
        v = [poem_flat(r) for r in master] if name != "paper" else verses
        true = ratios(v, proses, length)
        shuf = ratios(v, [proses[j] for j in perm], length)
        neigh = neighbour_prose(master, proses)
        keep = [i for i, p in enumerate(neigh) if p is not None]
        nb = ratios([v[i] for i in keep], [neigh[i] for i in keep], length)
        s_true, s_shuf, s_nb = summarise(true, hi_inc), summarise(shuf, hi_inc), summarise(nb, hi_inc)
        result["variants"][name] = {"true": s_true, "shuffled": s_shuf, "neighbour": s_nb}
        rows.append([name, s_true["mean"], s_true["median"], s_true["pass_n"], s_true["pass_pct"],
                     s_shuf["pass_pct"], s_nb["pass_pct"]])
        if name == "paper":
            paper_ratios = true
    print(f"Length ratio |P|/|V| on master (n={len(master)}).  "
          f"paper: mean 1.63, median 1.61, pass 27,633 (99.1%)")
    print_table(["variant", "mean", "median", "pass n", "pass %", "shuffled pass %",
                 "neighbour pass %"], rows)

    print("\nTable 14 bins, paper variant (paper: 1 / 78 / 9,333 / 15,449 / 3,020):")
    print_table(["bin", "count"], list(result["variants"]["paper"]["true"]["bins"].items()))

    order = sorted(range(len(master)), key=lambda i: -paper_ratios[i])
    result["most_extreme"] = [{"id": master[i]["id"], "ratio": paper_ratios[i], "poem": master[i]["poem"],
                               "telugu_meaning": master[i]["telugu_meaning"]} for i in order[:5]]
    print("five largest ratios:", [round(paper_ratios[i], 2) for i in order[:5]],
          " paper:", config.PAPER["level2"]["top5_extreme"])

    prefixed = sum(clean_meaning(r["telugu_meaning"]) != r["telugu_meaning"].strip() for r in master)
    result["records_with_prompt_prefix"] = prefixed
    print(f"records whose Telugu meaning carries a 'తెలుగు:'/'Telugu:' prefix: {prefixed:,}")

    # What the gate actually catches: Telugu meaning fields that also hold the
    # English gloss (a parsing defect of the LLM output), inflating |P|.
    fails = {master[i]["id"] for i, x in enumerate(paper_ratios) if not passes(x, False)}
    merged = [r["id"] for r in master if re.search(r"English\s*:", r["telugu_meaning"])]
    result["telugu_field_contains_english"] = {
        "records": len(merged), "among_gate_failures": len(fails & set(merged)),
        "gate_failures": len(fails), "ids": merged}
    print(f"Telugu meaning fields that also contain the English gloss: {len(merged)}; "
          f"{len(fails & set(merged))} of the {len(fails)} gate failures")

    (config.CACHE_DIR / "level2_ratios.json").write_text(json.dumps(
        {"variant": "paper", "ids": [r["id"] for r in master], "ratio": paper_ratios,
         "pass": [passes(x, False) for x in paper_ratios]}))
    save_result("level2_length_ratio", result)


if __name__ == "__main__":
    main()
