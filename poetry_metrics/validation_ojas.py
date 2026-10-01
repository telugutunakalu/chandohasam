"""Validation of the ojas metric (run through `python3 ojas.py validate`).

Everything is written to outputs/ojas_validation.json.

1. Per-corpus figures: word length, conjunct rate, aspirate rate, the index,
   rubric levels.
2. Classical contrasts (fixtures/classical_exemplars.json): pairs of verses that
   a text itself sets against each other as more and less ojas. The index must
   put each pair in the text's order.
3. The gloss check. The Bhāgavatamu edition glosses every verse word by word,
   with compounds and sandhi taken apart. Do longer printed words hold more
   gloss units?
4. Known groups: meters; prose against verse (Daṇḍin 1.80 calls ojas the life
   of prose); fierce against tender poems (Kāvyaprakāśa 8.69-70 places ojas in
   the heroic and furious rasas).
5. Sensitivity: each term alone, aspirates as a third term, the share of long
   words instead of the mean, and version 1.0's standardised index.
8. Reference dependence: each corpus in turn plays a new poet. Version 1.0
   rebuilt from the other three corpora relabels part of its poems; version
   2.0 cannot, since O uses no corpus statistic.
6. Relations to the other metrics, and between the two terms.
7. The densest and lightest lines.
"""
from __future__ import annotations

import json
import statistics
from collections import Counter, defaultdict

import anuprasa
import madhurya
import ojas as oj
import validation_madhurya as vm
from common import corpus
from common.phonology import aksharas, normalise
from common.stats import auc, spearman, summary

MIN_LINE_WORDS = 3            # for the lists of densest and lightest lines
MIN_PROSE_AKSHARAS = 20       # a prose passage shorter than this is not compared
LONG_WORD = 6                 # aksharas; for the long-word variant


# version 1.0 standardised L and J on the four corpora (baselines/ojas_baseline.json of version 1.0)
V1_SCALE = {"word_length": {"mean": 3.84362, "sd": 0.72973}, "conjunct_rate": {"mean": 12.0379, "sd": 5.12301}}
V1_CUT_PERCENTILES = (10, 30, 70, 90)


def v1_index(c: oj.Counts, scale: dict = V1_SCALE):
    if c.word_length is None or c.conjunct_rate is None:
        return None
    return 0.5 * ((c.word_length - scale["word_length"]["mean"]) / scale["word_length"]["sd"]
                  + (c.conjunct_rate - scale["conjunct_rate"]["mean"]) / scale["conjunct_rate"]["sd"])


def variants(c: oj.Counts) -> dict:
    """The index under other choices of terms (all shares of aksharas, in percent), and version 1.0's."""
    w, j, a = c.bound_share, c.conjunct_rate, c.aspirate_rate
    return {"headline": (w + j) / 2, "bound_share_only": w, "conjunct_rate_only": j,
            "with_aspirates": (w + j + a) / 3, "version_1_0": v1_index(c)}


def reference_dependence(totals_by_corpus: dict) -> dict:
    """Each corpus as a new poet: rebuild version 1.0 on the other three and count its relabelled poems."""
    from common.scoring import quantiles
    out = {}
    everything = [t for ts in totals_by_corpus.values() for t in ts]

    def scale_of(ts):
        return {name: {"mean": statistics.fmean(getattr(t, name) for t in ts),
                       "sd": statistics.pstdev(getattr(t, name) for t in ts)} for name in ("word_length", "conjunct_rate")}

    def cuts_of(ts, sc):
        q = quantiles([v1_index(t, sc) for t in ts])
        return [q[k] for k in V1_CUT_PERCENTILES]

    full_scale = scale_of(everything)
    full_cuts = cuts_of(everything, full_scale)
    for cname, ts in totals_by_corpus.items():
        rest = [t for other, us in totals_by_corpus.items() if other != cname for t in us]
        sc = scale_of(rest)
        cuts = cuts_of(rest, sc)
        before = [oj.level_of(v1_index(t, full_scale), full_cuts) for t in ts]
        after = [oj.level_of(v1_index(t, sc), cuts) for t in ts]
        out[cname] = {"share_of_reference_pct": round(100 * len(ts) / len(everything), 1),
                      "v1_word_length_mean_without_it": round(sc["word_length"]["mean"], 3),
                      "v1_relabelled_pct": round(100 * sum(x != y for x, y in zip(before, after)) / len(ts), 1),
                      "v1_rank_spearman": spearman([v1_index(t, full_scale) for t in ts], [v1_index(t, sc) for t in ts]),
                      "v2_relabelled_pct": 0.0}
    return out


def exemplar_counts() -> dict:
    return {e["id"]: oj.pooled(oj.count_poem(e["lines"])) for e in vm.load_exemplars()}


def contrasts_report(base: dict) -> dict:
    counts = exemplar_counts()
    data = json.loads(vm.EXEMPLARS.read_text(encoding="utf-8"))
    rows = []
    for c in data["contrasts"]:
        if c["metric"] != "ojas":
            continue
        more, less = counts[c["more"]], counts[c["less"]]
        if c["on"] == "conjuncts":
            a, b = more.conjunct_rate, less.conjunct_rate
        else:
            a, b = oj.index(more), oj.index(less)
        rows.append({"more": c["more"], "less": c["less"], "on": c["on"], "basis": c["basis"],
                     "value_more": round(a, 3), "value_less": round(b, 3), "in_order": a > b,
                     "with_aspirates_in_order": (variants(more)["with_aspirates"] > variants(less)["with_aspirates"])
                     if c["on"] == "index" else None})
    figures = {eid: {"ojas": round(oj.index(c), 3), "bound_share": round(c.bound_share, 2),
                     "word_length": round(c.word_length, 2),
                     "conjunct_rate": round(c.conjunct_rate, 1), "aspirate_rate": round(c.aspirate_rate, 1)}
               for eid, c in counts.items()}
    on_index = [r for r in rows if r["on"] == "index"]
    return {"contrasts": rows, "in_order": f"{sum(r['in_order'] for r in rows)}/{len(rows)}",
            "with_aspirates_in_order": f"{sum(r['with_aspirates_in_order'] for r in on_index)}/{len(on_index)}",
            "exemplars": figures}


def gloss_check() -> dict:
    """Bhāgavatamu verses with a word-by-word gloss: printed word length against gloss units per printed word."""
    records = json.loads((corpus.DATASET_DIR / corpus.CORPORA["bhagavatam"]).read_text(encoding="utf-8"))
    length, units_per_word, unit_length = [], [], []
    for r in records:
        if (r.get("form") or "verse") != "verse" or r.get("parent_id") or r.get("child_id"):
            continue                                   # seesa poems are split across two records; skip them
        units = [p["word"] for p in r.get("teeka_pairs") or [] if p.get("word")]
        lines = [l for l in r.get("verse") or [] if l.strip()]
        c = oj.pooled(oj.count_poem(lines))
        if not units or not c.words:
            continue
        length.append(c.word_length)
        units_per_word.append(len(units) / c.words)
        unit_length.append(statistics.fmean(len(aksharas(u)) or 1 for u in units))
    return {"poems": len(length),
            "gloss_units_per_printed_word": round(statistics.fmean(units_per_word), 3),
            "aksharas_per_printed_word": round(statistics.fmean(length), 3),
            "aksharas_per_gloss_unit": round(statistics.fmean(unit_length), 3),
            "spearman_word_length_with_units_per_word": spearman(length, units_per_word)}


def long_word_share(lines) -> float:
    lengths = [len(aksharas(w)) for l in lines for w in normalise(l).split()]
    lengths = [n for n in lengths if n]
    return sum(n >= LONG_WORD for n in lengths) / len(lengths) if lengths else None


def run(args) -> None:
    base = oj.load_baseline()
    md_base, an_base = madhurya.load_baseline(), anuprasa.load_baseline()
    report = {"version": oj.VERSION, "formula": base["formula"], "anchors": base["anchors"], "cuts": base["cuts"],
              "corpora": {}}
    totals_by_corpus = {}

    everything, all_variants = [], defaultdict(list)
    for cname in corpus.CORPORA:
        poems = corpus.load(cname)
        per_poem = [oj.count_poem(p.lines) for p in poems]
        totals = [oj.pooled(c) for c in per_poem]
        everything += totals
        totals_by_corpus[cname] = [t for t in totals if t.word_length is not None and t.conjunct_rate is not None]
        index = [oj.index(t) for t in totals]
        levels = Counter(oj.level_of(o, base["cuts"]["poem"]) for o in index)
        entry = {
            "n_poems": len(poems),
            "bound_share": summary([t.bound_share for t in totals]),
            "word_length": summary([t.word_length for t in totals]),
            "conjunct_rate": summary([t.conjunct_rate for t in totals]),
            "aspirate_rate": summary([t.aspirate_rate for t in totals]),
            "ojas": summary(index),
            "poem_levels_pct": {oj.LABELS[k]: round(100 * levels[k] / len(index), 2) for k in range(5)},
        }

        groups = [vm.content_group(p) for p in poems]
        n = Counter(groups)
        if min(n["fierce"], n["tender"]) >= vm.MIN_GROUP:
            entry["fierce_above_tender"] = {
                name: auc([getattr(t, attr) if attr else oj.index(t)
                           for t, g in zip(totals, groups) if g == "fierce"],
                          [getattr(t, attr) if attr else oj.index(t)
                           for t, g in zip(totals, groups) if g == "tender"])
                for name, attr in (("ojas", None), ("word_length", "word_length"), ("conjunct_rate", "conjunct_rate"),
                                   ("aspirate_rate", "aspirate_rate"))}

        by_meter = defaultdict(list)
        for p, o in zip(poems, index):
            by_meter[p.metre].append(o)
        entry["by_meter"] = {str(m): {"n": len(v), "mean_ojas": round(statistics.fmean(v), 3)}
                             for m, v in sorted(by_meter.items(), key=lambda kv: -len(kv[1])) if len(v) >= 100}

        prose = [oj.pooled(oj.count_poem(p.lines)) for p in corpus.load(cname, "prose")]
        prose = [t for t in prose if t.aksharas >= MIN_PROSE_AKSHARAS and t.words]
        if len(prose) >= vm.MIN_GROUP:
            entry["prose"] = {
                "n": len(prose),
                "word_length": round(statistics.fmean(t.word_length for t in prose), 3),
                "conjunct_rate": round(statistics.fmean(t.conjunct_rate for t in prose), 3),
                "prose_above_verse": {name: auc([f(t) for t in prose], [f(t) for t in totals])
                                      for name, f in (("ojas", lambda t: oj.index(t)),
                                                      ("word_length", lambda t: t.word_length),
                                                      ("conjunct_rate", lambda t: t.conjunct_rate))}}

        m = [madhurya.pooled(madhurya.profile_poem(p.lines)).index() for p in poems]
        az = [anuprasa.poem_levels(t, an_base["level_probs"])[anuprasa.HEADLINE][0]
              for t in anuprasa.tokens_of(poems)]
        keep = [i for i, v in enumerate(az) if v is not None]
        entry["spearman"] = {
            "word_length_with_conjunct_rate": spearman([t.word_length for t in totals],
                                                       [t.conjunct_rate for t in totals]),
            "ojas_with_madhurya": spearman(index, m),
            "conjunct_rate_with_madhurya": spearman([t.conjunct_rate for t in totals], m),
            "word_length_with_madhurya": spearman([t.word_length for t in totals], m),
            "ojas_with_anuprasa_z": spearman([index[i] for i in keep], [az[i] for i in keep]),
            "ojas_with_poem_length": spearman(index, [t.aksharas for t in totals]),
            "word_length_with_long_word_share": spearman([t.word_length for t in totals],
                                                         [long_word_share(p.lines) for p in poems]),
        }

        lines = [(oj.index(c), p.key, text) for p, counts in zip(poems, per_poem)
                 for text, c in zip(p.lines, counts) if c.words >= MIN_LINE_WORDS]
        lines.sort(key=lambda x: x[0])
        entry["lightest_lines"] = [{"ojas": round(o, 2), "poem": k, "line": l} for o, k, l in lines[:8]]
        entry["densest_lines"] = [{"ojas": round(o, 2), "poem": k, "line": l} for o, k, l in lines[:-9:-1]]
        longest = sorted(((n, w, p.key) for p, t in zip(poems, totals) for n, w in t.longest), reverse=True)[:8]
        entry["longest_words"] = [{"aksharas": n, "word": w, "poem": k} for n, w, k in longest]
        report["corpora"][cname] = entry
        print(f"{cname}: {len(poems)} poems")

    for t in everything:
        if t.word_length is None or t.conjunct_rate is None:
            continue
        for name, v in variants(t).items():
            all_variants[name].append(v)
    report["sensitivity"] = {name: {"spearman_with_headline": spearman(all_variants["headline"], v)}
                             for name, v in all_variants.items()}
    report["sensitivity"]["spearman_bound_share_with_conjunct_rate"] = spearman(all_variants["bound_share_only"],
                                                                               all_variants["conjunct_rate_only"])
    report["reference_dependence"] = reference_dependence(totals_by_corpus)
    report["contrasts"] = contrasts_report(base)
    report["gloss_check"] = gloss_check()
    report["madhurya_version"] = md_base["version"]

    oj.OUTPUT_DIR.mkdir(exist_ok=True)
    path = oj.OUTPUT_DIR / "ojas_validation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(oj.HERE)}")
