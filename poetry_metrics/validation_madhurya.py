"""Validation of the mādhurya metric (run through `python3 madhurya.py validate`).

Everything is seeded and written to outputs/madhurya_validation.json.

1. Per-corpus distributions: poem index, inventory, pile-up, class shares,
   rubric levels, sonority.
2. Classical exemplars (fixtures/classical_exemplars.json): the verses the
   treatise, the Kāvyaprakāśa and the Kāvyādarśa give as examples of a soft or
   a harsh texture. The index must put every soft exemplar above every harsh one.
3. Known groups, after Fónagy (1961): poems of tender against poems of fierce
   content. The treatise says harsh words are a defect in the tender rasas and
   a merit in the fierce ones (commentary on 4.21), so fierce poems should score
   lower. Groups are drawn by keywords in the English meaning (bhavam_en).
4. Sensitivity: the same checks under other sequence rules (no sequence term, a
   cumulative sum that soft sounds drain, adjacent pairs only, runs of paruṣa
   aksharas only), other weights, other readings of the class rules, and the
   sonority score alone.
5. Order: do harsh aksharas come in runs more than chance would give? The runs
   test of Wald & Wolfowitz (1940) on each poem, and the pile-up against the
   same classes in shuffled order. Then the poem's aksharas and its words
   shuffled as text.
6. Relations to other measures: inventory, the sonority score, the share of
   harsh aksharas, poem length and the anuprāsa z.
7. A check the corpus does not pass: whether the plain consonants that poets
   use beside the classical soft configurations are the more sonorous ones.
8. Prose against verse in the Bhāgavatamu; the softest and harshest lines; the
   heaviest harsh runs.
"""
from __future__ import annotations

import json
import math
import random
import re
import statistics
from collections import Counter, defaultdict

import anuprasa
import madhurya as md
from common import corpus
from common.phonology import SONORITY, VISARGA, line_aksharas, segments
from common.stats import auc, spearman
from common.stats import summary as _stats
from common.translit import iast_to_telugu

EXEMPLARS = md.HERE / "fixtures" / "classical_exemplars.json"
MIN_LINE_AKSHARAS = 8          # for the lists of softest and harshest lines
MIN_GROUP = 50                 # a known-groups comparison needs this many poems on each side

FIERCE = ("battle fight fought war warrior warriors arrow arrows weapon weapons sword mace kill killed slay slew "
          "slain destroy destroyed demon demons fierce terrible furious fury wrath anger angry rage roar roared "
          "blood army armies enemy enemies attack attacked struck thunderbolt").split()
TENDER = ("love beloved loving affection tender gentle sweet soft beautiful beauty lotus moon smile smiling child "
          "mother compassion mercy devotion bliss joy delight fragrance flower flowers embrace").split()
_FIERCE = re.compile(r"\b(" + "|".join(FIERCE) + r")\b")
_TENDER = re.compile(r"\b(" + "|".join(TENDER) + r")\b")


# --- the runs test ---------------------------------------------------------------

def runs_z(harsh: list):
    """Wald & Wolfowitz (1940): z of the number of runs in a harsh / not-harsh sequence.
    Negative: fewer runs than chance, so the harsh aksharas clump."""
    n1 = sum(harsh)
    n2 = len(harsh) - n1
    if n1 < 2 or n2 < 2:
        return None
    runs = 1 + sum(a != b for a, b in zip(harsh, harsh[1:]))
    mean = 2 * n1 * n2 / (n1 + n2) + 1
    var = 2 * n1 * n2 * (2 * n1 * n2 - n1 - n2) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
    return (runs - mean) / math.sqrt(var) if var > 0 else None


# --- the index under other sequence rules, weights and class readings ----------

def class_sequence(lines, amend=None) -> list:
    """The poem's akshara classes in order; `amend(akshara, cls)` may return another class."""
    out, prev = [], None
    for line in lines:
        for a in line_aksharas(line):
            cls, _ = md.classify(a, md.closes_with_nasal(prev, a))
            prev = a
            if cls is not None:
                out.append(amend(a, cls) if amend else cls)
    return out


def inventory(classes: list, weights: dict):
    return sum(weights[c] for c in classes) / len(classes) if classes else None


def pileup(classes: list, weights: dict, accumulates=None):
    """The pile-up P of madhurya.py: the mean load carried to harsh aksharas.
    `accumulates` limits which classes build a run (default: every class of negative weight)."""
    total, load = 0.0, 0.0
    for c in classes:
        w = weights[c]
        if w < 0 and (accumulates is None or c in accumulates):
            total += load
            load -= w
        else:
            load = 0.0
    return total / len(classes) if classes else None


def run_index(classes: list, weights: dict, accumulates=None):
    """The headline rule: inventory minus pile-up."""
    return inventory(classes, weights) - pileup(classes, weights, accumulates) if classes else None


def cusum_index(classes: list, weights: dict, allowance: float):
    """A cumulative sum that soft sounds drain (Page 1954, reference value `allowance`):
    load = max(0, load + harshness - allowance), where a soft akshara has negative harshness."""
    total, load = 0.0, 0.0
    for c in classes:
        w = weights[c]
        load = max(0.0, load - w - allowance)
        total += w if w >= 0 else -max(load, -w)
    return total / len(classes) if classes else None


def adjacent_pairs_index(classes: list, weights: dict):
    """Inventory minus one extra charge for a harsh akshara that follows a harsh one."""
    total, after_harsh = 0.0, False
    for c in classes:
        w = weights[c]
        total += 2 * w if (w < 0 and after_harsh) else w
        after_harsh = w < 0
    return total / len(classes) if classes else None


def _mid(w: float) -> dict:
    return {"madhura": 1.0, "sonorant": w, "voiced": 0.0, "voiceless": -w, "conjunct": -w, "parusha": -1.0}


def _every_geminate_harsh(a, cls):
    doubled = len(a.onset) == 2 and a.onset[0] == a.onset[1]
    return "parusha" if doubled else cls


def _visarga_harsh(a, cls):
    return "parusha" if VISARGA in a.coda else cls


W = md.WEIGHTS
VARIANTS = {          # name -> (amendment of the classes, scoring function of the class sequence)
    "headline": (None, lambda c: run_index(c, W)),
    # other sequence rules
    "inventory_only": (None, lambda c: inventory(c, W)),                        # no sequence term (version 1.0)
    "cusum_soft_sounds_drain": (None, lambda c: cusum_index(c, W, 0.25)),
    "adjacent_pairs_only": (None, lambda c: adjacent_pairs_index(c, W)),
    "runs_of_parusha_only": (None, lambda c: run_index(c, W, accumulates=("parusha",))),
    # other weights
    "middle_weights_quarter": (None, lambda c: run_index(c, _mid(0.25))),
    "middle_weights_three_quarters": (None, lambda c: run_index(c, _mid(0.75))),
    "classical_only": (None, lambda c: run_index(c, _mid(0.0))),                # the two poles alone
    "conjunct_neutral": (None, lambda c: run_index(c, {**W, "conjunct": 0.0})),
    # other readings of the class rules
    "every_geminate_harsh": (_every_geminate_harsh, lambda c: run_index(c, W)),  # 'tulyayoḥ' of any consonant
    "visarga_harsh": (_visarga_harsh, lambda c: run_index(c, W)),                # the 1945 commentary's list
}


def sonority_of(lines):
    segs = [SONORITY[s] for line in lines for a in line_aksharas(line) for s in segments(a)]
    return sum(segs) / len(segs) if segs else None


# --- analyses --------------------------------------------------------------------

def corpus_report(totals, baseline) -> dict:
    index = [t.index() for t in totals]
    levels = Counter(md.level_of(m, baseline["cuts"]["poem"]) for m in index)
    everything = md.pooled(totals)
    return {
        "poem_index": _stats(index),
        "poem_inventory": _stats([t.inventory for t in totals]),
        "poem_pileup": _stats([t.pileup for t in totals]),
        "poem_sonority": _stats([t.sonority for t in totals]),
        "poem_levels_pct": {md.LABELS[k]: round(100 * levels[k] / len(index), 2) for k in range(5)},
        "class_shares": {c: round(everything.classes[c] / everything.n, 4) for c in md.CLASSES},
        "rules_per_100_aksharas": {r: round(100 * everything.rules[r] / everything.n, 2) for r in md.RULES},
    }


def load_exemplars() -> list:
    data = json.loads(EXEMPLARS.read_text(encoding="utf-8"))
    for e in data["exemplars"]:
        if e["script"] == "iast":
            e["lines"] = [iast_to_telugu(l) for l in e["lines"]]
    return data["exemplars"]


def pairs_ordered(rows: list, key) -> str:
    soft = [key(r) for r in rows if r["pole"] == "soft"]
    harsh = [key(r) for r in rows if r["pole"] == "harsh"]
    return f"{sum(s > h for s in soft for h in harsh)}/{len(soft) * len(harsh)}"


def exemplar_report(baseline) -> dict:
    rows = []
    for e in load_exemplars():
        if e["pole"] is None:                      # an example quoted for another metric
            continue
        result = md.score_poem(e["lines"], baseline)
        unit = result if len(e["lines"]) > 1 else result["lines"][0]      # a single line is judged as a line
        rows.append({"id": e["id"], "source": e["source"], "locus": e["locus"], "pole": e["pole"], "tier": e["tier"],
                     **{k: unit[k] for k in ("madhurya", "percentile", "label", "inventory", "pileup",
                                             "sonority", "sonority_percentile", "classes")},
                     "harshest_run": result["harshest_run"]})
    out = {"exemplars": rows}
    for tier in ("primary", "all"):
        chosen = [r for r in rows if tier == "all" or r["tier"] == "primary"]
        for key in ("madhurya", "inventory", "sonority"):
            out[f"pairs_ordered_{key}_{tier}"] = pairs_ordered(chosen, lambda r: r[key])
    return out


def content_group(poem) -> str | None:
    """'fierce' | 'tender' | None, from keywords in the poem's English meaning."""
    text = poem.meaning_en.lower()
    fierce, tender = len(_FIERCE.findall(text)), len(_TENDER.findall(text))
    if fierce >= 2 and tender == 0:
        return "fierce"
    if tender >= 2 and fierce == 0:
        return "tender"
    return None


def known_groups(poems, values: dict) -> dict:
    """AUC of tender over fierce poems for each named list of poem values."""
    groups = [content_group(p) for p in poems]
    n = Counter(groups)
    if min(n["fierce"], n["tender"]) < MIN_GROUP:
        return {"skipped": f"fewer than {MIN_GROUP} poems in a group", "n_tender": n["tender"], "n_fierce": n["fierce"]}
    out = {}
    for name, vals in values.items():
        tender = [v for v, g in zip(vals, groups) if g == "tender" and v is not None]
        fierce = [v for v, g in zip(vals, groups) if g == "fierce" and v is not None]
        out[name] = {**auc(tender, fierce), "mean_tender": round(statistics.fmean(tender), 4),
                     "mean_fierce": round(statistics.fmean(fierce), 4)}
    return out


def order_report(sequences: list, rng) -> dict:
    """Harsh runs in the real order against the same classes in shuffled order."""
    zs = [z for z in (runs_z([W[c] < 0 for c in seq]) for seq in sequences) if z is not None]
    real = [pileup(seq, W) for seq in sequences]
    shuffled = []
    for seq in sequences:
        copy = list(seq)
        rng.shuffle(copy)
        shuffled.append(pileup(copy, W))
    return {
        "runs_test_mean_z": round(statistics.fmean(zs), 3),
        "poems_clumped_pct": round(100 * sum(z < -1.645 for z in zs) / len(zs), 2),      # nominal 5%
        "poems_alternating_pct": round(100 * sum(z > 1.645 for z in zs) / len(zs), 2),   # nominal 5%
        "pileup_real": round(statistics.fmean(real), 4),
        "pileup_classes_shuffled": round(statistics.fmean(shuffled), 4),
        "real_above_shuffled_pct": round(100 * sum(a > b for a, b in zip(real, shuffled)) / len(real), 2),
    }


def text_shuffle(poem, rng, unit: str):
    """The poem's index after shuffling its aksharas, or its words, as text."""
    if unit == "akshara":
        pieces = [a.text for l in poem.lines for a in line_aksharas(l)]
        joiner = ""
    else:
        pieces = [w for l in poem.lines for w in l.split()]
        joiner = " "
    rng.shuffle(pieces)
    return run_index(class_sequence([joiner.join(pieces)]), W)


def ordering_check(poems) -> dict:
    """Do poets put the more sonorous plain consonants beside the classical soft configurations?
    For each plain middle-class consonant: the mean (madhura - parusha) share of the rest of its line."""
    total, count = defaultdict(float), Counter()
    for poem in poems:
        prev = None
        for line in poem.lines:
            classes = []
            for a in line_aksharas(line):
                cls, _ = md.classify(a, md.closes_with_nasal(prev, a))
                classes.append((a, cls))
                prev = a
            scored = [c for _, c in classes if c is not None]
            if len(scored) < MIN_LINE_AKSHARAS:
                continue
            balance = (scored.count("madhura") - scored.count("parusha")) / (len(scored) - 1)
            for a, cls in classes:
                if cls in ("sonorant", "voiced", "voiceless") and len(a.onset) == 1:
                    total[a.onset[0]] += balance
                    count[a.onset[0]] += 1
    overall = sum(total.values()) / sum(count.values())
    rows = [(ch, count[ch], total[ch] / count[ch] - overall, SONORITY[ch]) for ch in count if count[ch] >= 300]
    rows.sort(key=lambda r: -r[2])
    return {"n_consonants": len(rows), "spearman_with_sonority": spearman([r[2] for r in rows], [r[3] for r in rows]),
            "consonants": [{"consonant": ch, "n": n, "balance_of_line": round(d, 4), "sonority": s}
                           for ch, n, d, s in rows]}


def run(args) -> None:
    baseline = md.load_baseline()
    anuprasa_base = anuprasa.load_baseline()
    report = {"version": md.VERSION, "seed": args.seed, "baseline_corpora": baseline["corpora"],
              "weights": md.WEIGHTS, "cuts": baseline["cuts"], "corpora": {}}
    report["exemplars"] = exemplar_report(baseline)

    all_poems, variant_values, sonority_values = [], {name: [] for name in VARIANTS}, []
    for cname in corpus.CORPORA:
        poems = corpus.load(cname)
        all_poems += poems
        profiles = [md.profile_poem(p.lines) for p in poems]
        totals = [md.pooled(pr) for pr in profiles]
        entry = corpus_report(totals, baseline)

        sequences = {None: [class_sequence(p.lines) for p in poems]}
        for amend, _ in VARIANTS.values():
            if amend not in sequences:
                sequences[amend] = [class_sequence(p.lines, amend) for p in poems]
        values = {name: [score(seq) for seq in sequences[amend]] for name, (amend, score) in VARIANTS.items()}
        values["sonority_score"] = [t.sonority for t in totals]
        for name in VARIANTS:
            variant_values[name] += values[name]
        sonority_values += values["sonority_score"]
        entry["tender_vs_fierce"] = known_groups(poems, values)

        rng = random.Random(args.seed)
        entry["order"] = order_report(sequences[None], rng)
        real = values["headline"]
        for unit in ("akshara", "word"):
            shuffled = [text_shuffle(p, rng, unit) for p in poems]
            pairs = [(a, b) for a, b in zip(real, shuffled) if a is not None and b is not None]
            entry[f"{unit}_shuffle"] = {
                "mean_real": round(statistics.fmean(a for a, _ in pairs), 4),
                "mean_shuffled": round(statistics.fmean(b for _, b in pairs), 4),
                "real_above_shuffled_pct": round(100 * sum(a > b for a, b in pairs) / len(pairs), 2),
                "mean_abs_change": round(statistics.fmean(abs(a - b) for a, b in pairs), 4),
            }

        z = [anuprasa.poem_levels(t, anuprasa_base["level_probs"])[anuprasa.HEADLINE][0]
             for t in anuprasa.tokens_of(poems)]
        keep = [i for i, v in enumerate(z) if v is not None and real[i] is not None]
        harsh_share = [sum(t.classes[c] for c in md.CLASSES if W[c] < 0) / t.n for t in totals]
        entry["spearman_with"] = {
            "inventory": spearman(real, values["inventory_only"]),
            "pileup": spearman(real, [t.pileup for t in totals]),
            "sonority_score": spearman(real, values["sonority_score"]),
            "harsh_share": spearman(real, harsh_share),
            "n_aksharas": spearman(real, [t.n for t in totals]),
            "anuprasa_z": spearman([real[i] for i in keep], [z[i] for i in keep]),
        }

        lines = [(prof.index(), p.key, text) for p, profs in zip(poems, profiles)
                 for text, prof in zip(p.lines, profs) if prof.n >= MIN_LINE_AKSHARAS]
        lines.sort(key=lambda x: x[0])
        entry["harshest_lines"] = [{"madhurya": round(m, 3), "poem": k, "line": l} for m, k, l in lines[:10]]
        entry["softest_lines"] = [{"madhurya": round(m, 3), "poem": k, "line": l} for m, k, l in lines[:-11:-1]]
        runs = sorted(((r, p.key) for p, t in zip(poems, totals) for r in t.runs), key=lambda x: -x[0].load)
        entry["heaviest_runs"] = [{"aksharas": "".join(r.aksharas), "length": len(r.aksharas), "load": r.load,
                                   "poem": k} for r, k in runs[:10]]

        prose = corpus.load(cname, "prose")
        if len(prose) >= MIN_GROUP:
            prose_totals = [md.pooled(md.profile_poem(p.lines)) for p in prose]
            entry["prose"] = {"poem_index": _stats([t.index() for t in prose_totals]),
                              "verse_above_prose": auc([t.index() for t in totals],
                                                       [t.index() for t in prose_totals if t.n])}
        report["corpora"][cname] = entry
        print(f"{cname}: {len(poems)} poems")

    # sensitivity: every variant against the headline, over all poems
    exemplars = [e for e in load_exemplars() if e["pole"] in ("soft", "harsh")]
    bhagavatam = corpus.load("bhagavatam")
    sensitivity = {}
    for name, (amend, score) in VARIANTS.items():
        rows = [{"pole": e["pole"], "v": score(class_sequence(e["lines"], amend))} for e in exemplars]
        sensitivity[name] = {
            "spearman_with_headline": spearman(variant_values["headline"], variant_values[name]),
            "exemplar_pairs_ordered": pairs_ordered(rows, lambda r: r["v"]),
            "tender_vs_fierce_auc_bhagavatam": known_groups(
                bhagavatam, {"v": variant_values[name][:len(bhagavatam)]})["v"]["auc"],
        }
    rows = [{"pole": e["pole"], "v": sonority_of(e["lines"])} for e in exemplars]
    sensitivity["sonority_score"] = {
        "spearman_with_headline": spearman(variant_values["headline"], sonority_values),
        "exemplar_pairs_ordered": pairs_ordered(rows, lambda r: r["v"]),
        "tender_vs_fierce_auc_bhagavatam": known_groups(
            bhagavatam, {"v": sonority_values[:len(bhagavatam)]})["v"]["auc"],
    }
    report["sensitivity"] = sensitivity
    report["ordering_check"] = ordering_check(all_poems)
    report["known_group_keywords"] = {"fierce": FIERCE, "tender": TENDER,
                                      "rule": "fierce: >= 2 fierce words and no tender word; tender: the reverse"}

    md.OUTPUT_DIR.mkdir(exist_ok=True)
    path = md.OUTPUT_DIR / "madhurya_validation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(md.HERE)}")
