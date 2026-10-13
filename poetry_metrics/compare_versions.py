"""Versions 1 and 2 of anuprāsa, mādhurya and prasāda, side by side.

Version 2 of each (anuprasa_v2.py, madhurya_v2.py, prasada_v2.py) puts no
statistic of the four dataset files into a score or a label. This script
measures what that changes, on the checks each metric was admitted with, and
writes outputs/v2_comparison.json. Findings: reports/v2_comparison.md.

1. agreement     Over the 12,704 reference poems: Spearman between the two
                 versions' scores, the share of poems and lines that keep their
                 label, and the label shares of each corpus under each version.
2. examples      The classical texts' own examples, scored and labelled by both.
3. degradations  The degradation protocol (degradation_protocol.py: the same seed,
                 the same degraded texts) for the anuprāsa z, the one score that
                 changes; mādhurya's M and prasāda's H are the same numbers in both
                 versions. The nonsense control (the constrained poems of
                 ../samples/json) for every metric, scores and labels.
4. known_groups  The pilot grid's sound figures against its meaning figures
                 (anuprāsa; validation_anuprasa.py).
5. new_poet      Each corpus in turn plays a new poet: it is left out of the
                 reference, version 1 is rebuilt from the other three, and its
                 poems are scored again. The share relabelled. Version 2 is rebuilt
                 the same way, and its constants must not move.
6. corpus_free   Anuprāsa with the poem as its own chance model, the one way to
                 need no corpus at all, and why it is not version 2. Then the other
                 rubrics considered for mādhurya and prasāda.

    python3 compare_versions.py        # about 75 s -> outputs/v2_comparison.json
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import anuprasa as ap                       # noqa: E402
import anuprasa_v2 as ap2                   # noqa: E402
import degradation_protocol as dp           # noqa: E402
import madhurya as md                       # noqa: E402
import madhurya_v2 as md2                   # noqa: E402
import prasada as pr                        # noqa: E402
import prasada_v2 as pr2                    # noqa: E402
import samples_analysis as sa               # noqa: E402
import validation_anuprasa as va            # noqa: E402
import validation_madhurya as vm            # noqa: E402
from common import corpus                   # noqa: E402
from common.phonology import akshara_consonants, aksharas, line_tokens, normalise   # noqa: E402
from common.scoring import quantiles        # noqa: E402
from common.stats import spearman           # noqa: E402

SEED = 42
OUTPUT = HERE / "outputs" / "v2_comparison.json"
HEADLINE = ap.HEADLINE
NEAR = 5                     # aksharas: the farthest a single letter's repeat still counts (Barbadikar & Kulkarni 2024, §5)
# Kāvyālaṅkārasaṅgrahamu 4.77 (1920 edition), the treatise's example of vṛttyanuprāsa: క్ష through three lines
TREATISE_VRTTYANUPRASA = {"locus": "KAS 4.77", "lines": [
    "సమదవిపక్షశిక్షణవిచక్షణదక్షిణదోరనుక్షణ", "భ్రమదసిదుర్ణిరీక్షసమరక్షపితక్షితిపక్షతక్షర",
    "త్సమధికశోణితక్షరకృతక్షణరక్షితపక్షిలోక నిన్", "గమలదళాక్షుఁ డేలు బలగౌరవసింహ నృసింహభూవరా."]}


def r4(x):
    return None if x is None else round(x, 4)


def shares(values: list, labels) -> dict:
    """Percentage of the values at each label index."""
    values = [v for v in values if v is not None]
    c = Counter(values)
    return {labels[k]: round(100 * c[k] / len(values), 1) for k in range(len(labels))} if values else {}


def same_pct(a: list, b: list) -> float:
    pairs = [(x, y) for x, y in zip(a, b) if x is not None and y is not None]
    return round(100 * sum(x == y for x, y in pairs) / len(pairs), 2)


def confusion(a: list, b: list, labels) -> dict:
    """{label under version 1: {label under version 2: poems}}."""
    out = defaultdict(Counter)
    for x, y in zip(a, b):
        if x is not None and y is not None:
            out[labels[x]][labels[y]] += 1
    return {k: dict(v) for k, v in out.items()}


# ---------------------------------------------------------------------------
# anuprāsa: the two chance models, and the poem as its own
# ---------------------------------------------------------------------------

def level_probs(probs: dict, levels=ap.LEVELS) -> dict:
    return {name: ap.level_probabilities(probs, keyf) for name, keyf in levels.items()}


def anuprasa_poem(tokens, lp: dict) -> dict:
    """{level: (poem z, poem score, [line z])}, as anuprasa.poem_levels."""
    return ap.poem_levels(tokens, lp)


def anuprasa_z(lp: dict):
    """tokens -> the poem's headline z, rounded as anuprasa.score_poem (and so the protocol) rounds it."""
    def z_of(tokens):
        z = anuprasa_poem(tokens, lp)[HEADLINE][0]
        return None if z is None else round(z, 3)
    return z_of


def poem_label(score: float) -> int:
    return int(score + 0.5)


def falling(x: int, k: int) -> int:
    out = 1
    for i in range(k):
        out *= x - i
    return out


def own_chance_z(poem_tokens, keyf, window=None):
    """The anuprāsa z with the poem's own consonants as the chance model: the poem's tokens are dealt at
    random over its consonant slots (a permutation), and A counts the same-sound pairs in different aksharas
    of one line (within `window` aksharas, if given). E and V are exact under the permutation:
        a2 = sum_s (x_s)_2 / (n)_2,  a3 = sum_s (x_s)_3 / (n)_3,
        a22 = [sum_s (x_s)_4 + sum_(s != t) (x_s)_2 (x_t)_2] / (n)_4
        E = |P| a2,   V = |P| a2 + K a3 + D a22 - E^2,   D = |P|^2 - |P| - K
    with (x)_k the falling factorial, P the counted pairs and K = sum_t d_t (d_t - 1).
    A poem of one sound has no variance, and z = 0: its repeats are exactly what its own sounds predict.
    Returns (poem z, [line z])."""
    counts = Counter(keyf(t) for line in poem_tokens for t in line)
    n = sum(counts.values())
    c2 = sum(falling(x, 2) for x in counts.values())
    a2 = c2 / falling(n, 2) if n >= 2 else 0.0
    a3 = sum(falling(x, 3) for x in counts.values()) / falling(n, 3) if n >= 3 else 0.0
    a22 = ((sum(falling(x, 4) for x in counts.values()) + c2 * c2 - sum(falling(x, 2) ** 2 for x in counts.values()))
           / falling(n, 4)) if n >= 4 else 0.0

    def z_of(a, p, k):
        if not p:
            return None
        e = p * a2
        v = p * a2 + k * a3 + (p * p - p - k) * a22 - e * e
        return (a - e) / math.sqrt(v) if v > 1e-12 else 0.0       # no variance: A is fixed, and equals E

    stats = []
    for line in poem_tokens:
        keys = [keyf(t) for t in line]
        degree = [0] * len(line)
        a = p = 0
        for i in range(len(line)):
            for j in range(i + 1, len(line)):
                d = line[j].akshara - line[i].akshara
                if d == 0 or (window is not None and d > window):
                    continue
                p += 1
                degree[i] += 1
                degree[j] += 1
                a += keys[i] == keys[j]
        stats.append((a, p, sum(x * (x - 1) for x in degree)))
    lines = [z_of(*s) for s in stats]
    return z_of(*(sum(x) for x in zip(*stats))) if stats else None, lines


CORPUS_FREE = {"own_chance_line": None, f"own_chance_near_{NEAR}": NEAR}


# ---------------------------------------------------------------------------
# 1. agreement over the reference poems
# ---------------------------------------------------------------------------

def anuprasa_agreement(tokens_by_corpus: dict, lp1: dict, lp2: dict) -> tuple[dict, dict]:
    out, results = {"corpora": {}}, {}
    all_poem, all_line, all_lev, all_lab = [[], []], [[], []], [[], []], [[], []]
    for cname, toks in tokens_by_corpus.items():
        r1 = [anuprasa_poem(t, lp1) for t in toks]
        r2 = [anuprasa_poem(t, lp2) for t in toks]
        results[cname] = (r1, r2)
        entry = {}
        for v, rs in (("v1", r1), ("v2", r2)):
            line_z = [z for r in rs for z in r[HEADLINE][2]]
            k = 0 if v == "v1" else 1
            all_poem[k] += [r[HEADLINE][0] for r in rs]
            all_line[k] += line_z
            all_lev[k] += [ap.rubric(z) for z in line_z]
            all_lab[k] += [poem_label(r[HEADLINE][1]) for r in rs]
            entry[v] = {"lines_at_or_above_pct": va._at_or_above(line_z),
                        "poem_labels_pct": shares([poem_label(r[HEADLINE][1]) for r in rs], ap.LABELS),
                        "median_poem_z": round(statistics.median(r[HEADLINE][0] for r in rs if r[HEADLINE][0] is not None), 3)}
        out["corpora"][cname] = entry
    pairs = [(a, b) for a, b in zip(*all_poem) if a is not None and b is not None]
    lpairs = [(a, b) for a, b in zip(*all_line) if a is not None and b is not None]
    out.update({
        "spearman_poem_z": spearman([a for a, _ in pairs], [b for _, b in pairs]),
        "spearman_line_z": spearman([a for a, _ in lpairs], [b for _, b in lpairs]),
        "mean_change_poem_z": round(statistics.fmean(b - a for a, b in pairs), 4),
        "lines_same_level_pct": same_pct(*all_lev),
        "poems_same_label_pct": same_pct(*all_lab),
        "line_levels_confusion": confusion(*all_lev, ap.LABELS),
    })
    return out, results


def rubric_agreement(values_by_corpus: dict, cuts1: dict, cuts2: dict, level_of, labels) -> dict:
    """Mādhurya and prasāda: one score, two rubrics. values_by_corpus: {corpus: ([poem values], [line values])}."""
    out, a_poems, b_poems, a_lines, b_lines = {"corpora": {}}, [], [], [], []
    for cname, (poems, lines) in values_by_corpus.items():
        p1, p2 = [level_of(v, cuts1["poem"]) for v in poems], [level_of(v, cuts2["poem"]) for v in poems]
        l1, l2 = [level_of(v, cuts1["line"]) for v in lines], [level_of(v, cuts2["line"]) for v in lines]
        a_poems += p1
        b_poems += p2
        a_lines += l1
        b_lines += l2
        out["corpora"][cname] = {"v1": {"poem_labels_pct": shares(p1, labels), "line_labels_pct": shares(l1, labels)},
                                 "v2": {"poem_labels_pct": shares(p2, labels), "line_labels_pct": shares(l2, labels)}}
    out["all"] = {"v1": {"poem_labels_pct": shares(a_poems, labels), "line_labels_pct": shares(a_lines, labels)},
                  "v2": {"poem_labels_pct": shares(b_poems, labels), "line_labels_pct": shares(b_lines, labels)}}
    out["poems_same_label_pct"] = same_pct(a_poems, b_poems)
    out["lines_same_label_pct"] = same_pct(a_lines, b_lines)
    out["poem_labels_confusion"] = confusion(a_poems, b_poems, labels)
    return out


# ---------------------------------------------------------------------------
# 2. the classical examples
# ---------------------------------------------------------------------------

def anuprasa_examples(base1: dict, base2: dict) -> dict:
    out = {}
    exemplars = {e["id"]: e for e in vm.load_exemplars()}
    for key, lines in (("kas_4_77_vrttyanuprasa", TREATISE_VRTTYANUPRASA["lines"]),
                       ("kd_1_72_krcchrodya", exemplars["kd_1_72_krcchrodya"]["lines"])):
        row = {}
        for v, base, score in (("v1", base1, ap.score_poem), ("v2", base2, ap2.score_poem)):
            r = score(lines, base)
            row[v] = {level: {k: r[level][k] for k in ("score", "label", "z", "lift", "z_percentile")}
                      for level in ap.LEVELS}
            row[v]["line_labels_varna"] = [l["varna"]["label"] for l in r["lines"]]
            row[v]["line_carriers_varna"] = [l["varna"]["carriers"][0]["sound"] if l["varna"]["carriers"] else None
                                             for l in r["lines"]]
        out[key] = row
    out["kas_4_77_vrttyanuprasa"]["locus"] = TREATISE_VRTTYANUPRASA["locus"]
    return out


def madhurya_examples(cuts1: dict, cuts2: dict) -> dict:
    rows = []
    for e in vm.load_exemplars():
        if e["pole"] is None:
            continue
        m = md.pooled(md.profile_poem(e["lines"])).index()
        unit = "poem" if len(e["lines"]) > 1 else "line"        # as validation_madhurya: a single line is a line
        rows.append({"id": e["id"], "locus": e["locus"], "pole": e["pole"], "tier": e["tier"], "madhurya": r4(m),
                     "v1": md.LABELS[md.level_of(m, cuts1[unit])], "v2": md.LABELS[md.level_of(m, cuts2[unit])]})
    poles = [r for r in rows if r["pole"] in ("soft", "harsh")]

    def on_side(r, v):
        level = md.LABELS.index(r[v])
        return level >= 3 if r["pole"] == "soft" else level <= 1

    return {"exemplars": rows,
            "same_label": f"{sum(r['v1'] == r['v2'] for r in rows)}/{len(rows)}",
            **{f"{v}_on_their_side": f"{sum(on_side(r, v) for r in poles)}/{len(poles)}" for v in ("v1", "v2")},
            **{f"{v}_harsh_examples_labelled_harsh": f"{sum(r[v] == 'harsh' for r in poles if r['pole'] == 'harsh')}/"
                                                       f"{sum(r['pole'] == 'harsh' for r in poles)}" for v in ("v1", "v2")}}


def prasada_examples(model, cuts1: dict, cuts2: dict) -> dict:
    data = json.loads(vm.EXEMPLARS.read_text(encoding="utf-8"))
    lines = {e["id"]: e["lines"] for e in vm.load_exemplars()}
    ids = sorted({c[k] for c in data["contrasts"] if c["metric"] == "prasada" for k in ("more", "less")})
    rows = []
    for eid in ids:
        h = pr.poem_figures(model, lines[eid])["surprisal"]
        rows.append({"id": eid, "surprisal": r4(h), "v1": pr.LABELS[pr.level_of(h, cuts1["poem"])],
                     "v2": pr.LABELS[pr.level_of(h, cuts2["poem"])]})
    h = {r["id"]: r["surprisal"] for r in rows}
    contrasts = [c for c in data["contrasts"] if c["metric"] == "prasada"]
    return {"exemplars": rows, "contrasts_in_order_both_versions":
            f"{sum(h[c['more']] < h[c['less']] for c in contrasts)}/{len(contrasts)}"}


# ---------------------------------------------------------------------------
# 3. degradations and the nonsense control
# ---------------------------------------------------------------------------

def degraded_texts(seed: int) -> dict:
    """The texts degradation_protocol.py scores, drawn with the same seed in the same order."""
    rng = random.Random(seed)
    poems = dp.sample_poems(rng)
    out = {"original": [list(p.lines) for p, _ in poems]}
    for name, degrade in (("word_shuffle", dp.word_shuffle), ("meter_break", dp.meter_break), ("filler", dp.filler)):
        out[name] = {level: [degrade(list(p.lines), level, rng) for p, _ in poems] for level in dp.LEVELS[name]}
    records = {f"bhagavatam:{r['id']}": r for r in
               json.loads((corpus.DATASET_DIR / corpus.CORPORA["bhagavatam"]).read_text(encoding="utf-8"))}
    glossed = [(p, dp.gloss_units(records[p.key])) for p, _ in poems if p.corpus == "bhagavatam"]
    glossed = [(p, units) for p, units in glossed if len(units) >= dp.MIN_UNITS]
    out["synonym_swap_original"] = [dp.synonym_swap(units, len(p.lines), 0, rng) for p, units in glossed]
    out["synonym_swap"] = {level: [dp.synonym_swap(units, len(p.lines), level, rng) for p, units in glossed]
                           for level in dp.LEVELS["synonym_swap"]}
    return out


def anuprasa_degradations(texts: dict, scorers: dict) -> dict:
    """Ladders and verdicts of each anuprāsa scorer ({name: poem tokens -> poem z}) on the protocol's texts."""
    metrics = {name: (lambda r, n=name: r[n]) for name in scorers}

    def rows(list_of_lines):
        return [{name: f([line_tokens(l)[1] for l in lines]) for name, f in scorers.items()}
                for lines in list_of_lines]

    original = rows(texts["original"])
    out = {}
    for name in ("word_shuffle", "meter_break", "filler"):
        out[name] = dp.ladder(original, {level: rows(t) for level, t in texts[name].items()}, metrics)
    out["synonym_swap"] = dp.ladder(rows(texts["synonym_swap_original"]),
                                    {level: rows(t) for level, t in texts["synonym_swap"].items()}, metrics)
    return out


def nonsense_control(real: dict, base1, base2, cuts: dict, model) -> tuple[dict, list]:
    """The constrained-decoding poems against real verse, under both versions of each metric.
    Returns the report and the surprisal of every constrained poem."""
    z1, z2 = anuprasa_z(base1["level_probs"]), anuprasa_z(base2["level_probs"])
    cells = defaultdict(list)
    for p in sa.generated_poems():
        lines = p["lines"]
        if not lines:
            continue
        toks = [line_tokens(l)[1] for l in lines]
        cells[(p["model"], p["ablation"])].append({
            "anuprasa_v1": z1(toks), "anuprasa_v2": z2(toks),
            "madhurya": md.pooled(md.profile_poem(lines)).index(),
            "surprisal": pr.poem_figures(model, lines)["surprisal"]})
    constrained = [r for (m, a), rs in cells.items() if a != "baseline" for r in rs]
    out = {"cells": {}, "constrained_poems": len(constrained)}
    for (m, a), rs in sorted(cells.items()):
        if a == "baseline":
            continue
        out["cells"][f"{m} | {a}"] = {k: sa.above([r[k] for r in rs], real[k]) for k in ("anuprasa_v1", "anuprasa_v2")}
    for k in ("anuprasa_v1", "anuprasa_v2"):
        vals = [c[k] for c in out["cells"].values()]
        out[f"{k}_p_above_real"] = [min(vals), max(vals)]

    def anuprasa_strong(values):
        values = [v for v in values if v is not None]
        return round(100 * sum(v >= ap.RUBRIC[0][0] for v in values) / len(values), 1)

    out["poems_with_poem_z_strong_pct"] = {
        v: {"constrained": anuprasa_strong([r[f"anuprasa_{v}"] for r in constrained]),
            "real": anuprasa_strong(real[f"anuprasa_{v}"])} for v in ("v1", "v2")}
    out["madhurya_labels_pct"] = {
        v: {"constrained": shares([md.level_of(r["madhurya"], cuts["madhurya"][v]["poem"]) for r in constrained], md.LABELS),
            "real": shares([md.level_of(x, cuts["madhurya"][v]["poem"]) for x in real["madhurya"]], md.LABELS)}
        for v in ("v1", "v2")}
    out["prasada_labels_pct"] = {
        v: {"constrained": shares([pr.level_of(r["surprisal"], cuts["prasada"][v]["poem"]) for r in constrained], pr.LABELS),
            "real": shares([pr.level_of(x, cuts["prasada"][v]["poem"]) for x in real["surprisal"]], pr.LABELS)}
        for v in ("v1", "v2")}
    for v in ("v1", "v2"):
        levels = [pr.level_of(r["surprisal"], cuts["prasada"][v]["poem"]) for r in constrained]
        real_levels = [pr.level_of(x, cuts["prasada"][v]["poem"]) for x in real["surprisal"]]
        out["prasada_labels_pct"][v]["gate"] = {
            gate: {"constrained_passing": sum(l >= pr.LABELS.index(gate) for l in levels),
                   "real_passing_pct": round(100 * sum(l >= pr.LABELS.index(gate) for l in real_levels)
                                             / len(real_levels), 1)}
            for gate in ("ordinary", "leaning_clear")}
    return out, [r["surprisal"] for r in constrained]


# ---------------------------------------------------------------------------
# 5. a new poet
# ---------------------------------------------------------------------------

def anuprasa_new_poet(tokens_by_corpus: dict, results: dict, base1: dict, base2: dict) -> dict:
    out = {}
    again = ap2.chance_probabilities(ap2.language_counts()[0])
    v2_moves = {s: round(p, 8) for s, p in again.items()} != base2["probabilities"]      # stored to 8 decimals
    total = sum(len(t) for t in tokens_by_corpus.values())
    for cname, toks in tokens_by_corpus.items():
        counts = Counter(t.char for other, ts in tokens_by_corpus.items() if other != cname
                         for lines in ts for line in lines for t in line)
        total_count = sum(counts.values()) + ap.PSEUDO_COUNT * len(ap.SOUNDS)
        lp = level_probs({s: (counts.get(s, 0) + ap.PSEUDO_COUNT) / total_count for s in ap.SOUNDS})
        without = [anuprasa_poem(t, lp) for t in toks]
        full = results[cname][0]
        line_full = [ap.rubric(z) for r in full for z in r[HEADLINE][2]]
        line_without = [ap.rubric(z) for r in without for z in r[HEADLINE][2]]
        out[cname] = {
            "share_of_reference_pct": round(100 * len(toks) / total, 1),
            "q_without_it": round(ap.moments(lp[HEADLINE])[0], 5),
            "v1_lines_relabelled_pct": round(100 - same_pct(line_full, line_without), 2),
            "v1_poems_relabelled_pct": round(100 - same_pct([poem_label(r[HEADLINE][1]) for r in full],
                                                            [poem_label(r[HEADLINE][1]) for r in without]), 2),
            "v2_lines_relabelled_pct": 0.0 if not v2_moves else None,
        }
    out["v2_chance_model_moves_with_the_reference"] = v2_moves
    out["q_v1"] = round(ap.moments(base1["level_probs"][HEADLINE])[0], 5)
    out["q_v2"] = round(ap.moments(base2["level_probs"][HEADLINE])[0], 5)
    return out


def rubric_new_poet(values_by_corpus: dict, cuts1: dict, cuts2_again: dict, cuts2: dict, level_of) -> dict:
    """Version 1 cut at the 10/30/70/90th percentiles of the other three corpora; version 2 rebuilt."""
    out, total = {}, sum(len(p) for p, _ in values_by_corpus.values())
    for cname, (poems, lines) in values_by_corpus.items():
        rest_p = [v for other, (p, _) in values_by_corpus.items() if other != cname for v in p]
        rest_l = [v for other, (_, l) in values_by_corpus.items() if other != cname for v in l]
        qp, ql = quantiles(rest_p), quantiles(rest_l)
        without = {"poem": [qp[k] for k in (10, 30, 70, 90)], "line": [ql[k] for k in (10, 30, 70, 90)]}
        out[cname] = {
            "share_of_reference_pct": round(100 * len(poems) / total, 1),
            "v1_poem_cuts_without_it": without["poem"],
            "v1_poems_relabelled_pct": round(100 - same_pct([level_of(v, cuts1["poem"]) for v in poems],
                                                            [level_of(v, without["poem"]) for v in poems]), 2),
            "v1_lines_relabelled_pct": round(100 - same_pct([level_of(v, cuts1["line"]) for v in lines],
                                                            [level_of(v, without["line"]) for v in lines]), 2),
            "v2_poems_relabelled_pct": round(100 - same_pct([level_of(v, cuts2["poem"]) for v in poems],
                                                            [level_of(v, cuts2_again["poem"]) for v in poems]), 2),
        }
    out["v2_cuts_move_with_the_reference"] = cuts2_again != cuts2
    return out


# ---------------------------------------------------------------------------
# 6. a chance model from the poem itself, and the other rubrics considered
# ---------------------------------------------------------------------------

def corpus_free_anuprasa(tokens_by_corpus: dict, results: dict, texts: dict, base1: dict, seed: int) -> dict:
    keyf = ap.LEVELS[HEADLINE]
    scorers = {name: (lambda t, w=w: own_chance_z(t, keyf, w)[0]) for name, w in CORPUS_FREE.items()}
    out = {"definition": "the poem's own consonants as the chance model (a random deal of its tokens over its "
                         "consonant slots); pairs in one line, or in one line and at most "
                         f"{NEAR} aksharas apart (Daṇḍin 1.55, 1.58; Barbadikar & Kulkarni 2024, §5)",
           "treatise_example_4_77": {}, "controls": {}, "spearman_with_v1_poem_z": {}}
    tex = [line_tokens(l)[1] for l in TREATISE_VRTTYANUPRASA["lines"]]
    for name, w in CORPUS_FREE.items():
        z, lines = own_chance_z(tex, keyf, w)
        out["treatise_example_4_77"][name] = {"poem_z": r4(z), "line_z": [r4(x) for x in lines]}
    # the controls of validation_anuprasa.py, drawn the same way
    v1_all, cand_all = [], defaultdict(list)
    v1_z = lambda t: anuprasa_poem(t, base1["level_probs"])[HEADLINE][0]          # noqa: E731
    for cname, toks in tokens_by_corpus.items():
        poems = corpus.load(cname)
        pool = [w for p in poems for l in p.lines for w in l.split()]
        rng = random.Random(seed)
        shuffle = [va.word_shuffle(p, rng) for p in poems]
        salad = [va.word_salad(p, pool, rng) for p in poems]
        entry = {}
        v1_real = [r[HEADLINE][0] for r in results[cname][0]]
        v1_all += v1_real
        for name, f in scorers.items():
            real = [f(t) for t in toks]
            cand_all[name] += real
            entry[name] = {"real_beats_word_shuffle_pct": va._beats([(x, None) for x in real],
                                                                     [(f(t), None) for t in shuffle]),
                           "real_beats_word_salad_pct": va._beats([(x, None) for x in real],
                                                                   [(f(t), None) for t in salad])}
        entry["v1"] = {"real_beats_word_shuffle_pct": va._beats([(x, None) for x in v1_real],
                                                                 [(v1_z(t), None) for t in shuffle]),
                       "real_beats_word_salad_pct": va._beats([(x, None) for x in v1_real],
                                                               [(v1_z(t), None) for t in salad])}
        out["controls"][cname] = entry
    for name, vals in cand_all.items():
        pairs = [(a, b) for a, b in zip(v1_all, vals) if a is not None and b is not None]
        out["spearman_with_v1_poem_z"][name] = spearman([a for a, _ in pairs], [b for _, b in pairs])
    # the pilot grid
    pilot = json.loads(va.PILOT.read_text(encoding="utf-8"))["poems"] if va.PILOT.exists() else []
    groups = defaultdict(lambda: defaultdict(list))
    for p in pilot:
        g = p.get("alankaram_id")
        if g in va.SABDA + va.ARTHA:
            toks = [line_tokens(l)[1] for l in p["lines"]]
            for name, f in scorers.items():
                groups[name]["sabda" if g in va.SABDA else "artha"].append(f(toks))
    out["pilot_auc_sabda_vs_artha"] = {name: va.auc([x for x in g["sabda"] if x is not None],
                                                    [x for x in g["artha"] if x is not None])
                                       for name, g in groups.items()}
    deg = anuprasa_degradations(texts, scorers)
    out["degradation_verdicts"] = {d: {name: v["verdict"] for name, v in ladder.items()} for d, ladder in deg.items()}
    out["filler_full_strength_mean"] = {name: deg["filler"][name]["steps"][-1]["mean"] for name in scorers}
    return out


def alternative_rubrics(madhurya_values: dict, prasada_values: dict, model, constrained_h: list) -> dict:
    exemplars = {e["id"]: e for e in vm.load_exemplars()}
    m = {k: md.pooled(md.profile_poem(e["lines"])).index() for k, e in exemplars.items() if e["pole"] in ("soft", "harsh")}
    lo, hi = m["kas_4_21_parusha"], m["kas_4_62_saukumarya"]
    rubrics = {
        "thirds_between_4_21_and_4_62": [lo, lo + (hi - lo) / 3, lo + 2 * (hi - lo) / 3, hi],
        "four_anchors_4_21_tikkana_peddana_4_62": [lo, m["kasc_tikkana_gadha"], m["kasc_peddana_ekkadi"], hi],
    }
    poems = [v for p, _ in madhurya_values.values() for v in p]
    out = {"madhurya": {}, "prasada": {}}
    for name, cuts in rubrics.items():
        labels = {k: md.LABELS[md.level_of(v, cuts)] for k, v in m.items()}
        out["madhurya"][name] = {
            "cuts": [r4(c) for c in cuts],
            "poem_labels_pct": shares([md.level_of(v, cuts) for v in poems], md.LABELS),
            "harsh_examples_read_balanced_or_softer": sorted(k for k, lab in labels.items()
                                                             if exemplars[k]["pole"] == "harsh"
                                                             and md.LABELS.index(lab) >= 2),
            "exemplar_labels": labels}
    out["madhurya"]["reference_poems_below_4_21"] = sum(v < lo for v in poems)
    # prasāda: the other form-level defect, a word poets do not use (aprayukta, 4.5), as the obscure anchor
    ids = ("kas_4_59_prasada", "kas_4_5_aprayukta", "kas_4_15_apratita", "kas_4_17_klishta", "kas_4_8_asamartha")
    h = {k: pr.poem_figures(model, exemplars[k]["lines"])["surprisal"] for k in ids}
    a, b = h["kas_4_59_prasada"], h["kas_4_5_aprayukta"]
    cuts = [a, a + (b - a) / 3, a + 2 * (b - a) / 3, b]
    real = [v for p, _ in prasada_values.values() for v in p]
    levels = [pr.level_of(v, cuts) for v in constrained_h]
    real_levels = [pr.level_of(v, cuts) for v in real]
    out["prasada"]["obscure_anchor_4_5"] = {
        "cuts": [r4(c) for c in cuts],
        "poem_labels_pct": shares(real_levels, pr.LABELS),
        "constrained_labels_pct": shares(levels, pr.LABELS),
        "gate": {gate: {"constrained_passing": sum(l >= pr.LABELS.index(gate) for l in levels),
                        "real_passing_pct": round(100 * sum(l >= pr.LABELS.index(gate) for l in real_levels)
                                                  / len(real_levels), 1)} for gate in ("ordinary", "leaning_clear")},
        "exemplar_labels": {k: pr.LABELS[pr.level_of(v, cuts)] for k, v in h.items()}}
    return out


# ---------------------------------------------------------------------------

def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--seed", type=int, default=SEED)
    args = parser.parse_args(argv)

    base1, base2 = ap.load_baseline(), ap2.load_baseline()
    mbase1, mbase2 = md.load_baseline(), md2.load_baseline()
    model, model2 = pr.load_model(), pr2.load_model()
    cuts = {"madhurya": {"v1": mbase1["cuts"], "v2": mbase2["cuts"]},
            "prasada": {"v1": model.meta["cuts"], "v2": model2.meta["cuts"]}}
    report = {"seed": args.seed,
              "versions": {"anuprasa": [ap.VERSION, ap2.VERSION], "madhurya": [md.VERSION, md2.VERSION],
                           "prasada": [pr.VERSION, pr2.VERSION]},
              "what_changes": {
                  "anuprasa": "the chance model's consonant frequencies: the four dataset files (v1) -> the language "
                              "reference, prasāda's crawled verse (v2); statistic and rubric unchanged",
                  "madhurya": "the rubric: reference percentiles (v1) -> symmetric about M = 0 with outer cuts at the "
                              "treatise's saukumārya example, 4.62 (v2); M unchanged",
                  "prasada": "the rubric: reference percentiles (v1) -> the treatise's prasāda example (4.59) and its "
                             "example of a word found only in śāstras (apratīta, 4.15), in thirds (v2); H and the model "
                             "unchanged"},
              "cuts": cuts}

    tokens_by_corpus = {c: ap.tokens_of(corpus.load(c)) for c in corpus.CORPORA}
    anu, anu_results = anuprasa_agreement(tokens_by_corpus, base1["level_probs"], base2["level_probs"])
    anu["moments"] = {"v1": {n: dict(zip(("q", "r"), (round(x, 6) for x in ap.moments(base1["level_probs"][n]))))
                             for n in ap.LEVELS},
                      "v2": base2["moments"]}
    # prasāda's model counted aksharas word by word, anuprāsa splits lines: the same consonant tokens?
    line_wise = Counter(t.char for ts in tokens_by_corpus.values() for poem in ts for line in poem for t in line)
    word_wise = Counter(c for name in corpus.CORPORA for p in corpus.load(name) for l in p.lines
                        for w in normalise(l).split() for a in aksharas(w) for c in akshara_consonants(a))
    anu["four_files_tokens"] = {"line_wise": sum(line_wise.values()), "word_wise": sum(word_wise.values()),
                                "same_count_of_every_sound": line_wise == word_wise}
    report["anuprasa"] = {"agreement": anu}
    print("anuprāsa agreement:", anu["spearman_poem_z"], anu["lines_same_level_pct"])

    m_values, h_values = {}, {}
    for cname in corpus.CORPORA:
        poems = corpus.load(cname)
        profiles = [md.profile_poem(p.lines) for p in poems]
        m_values[cname] = ([md.pooled(pf).index() for pf in profiles],
                           [pf.index() for prof in profiles for pf in prof if pf.n])
        h_values[cname] = ([pr.poem_figures(model, p.lines)["surprisal"] for p in poems],
                           [statistics.fmean(b) for p in poems for l in p.lines for b in [model.bits(l)[1]] if b])
    report["madhurya"] = {"agreement": rubric_agreement(m_values, cuts["madhurya"]["v1"], cuts["madhurya"]["v2"],
                                                        md.level_of, md.LABELS)}
    report["prasada"] = {"agreement": rubric_agreement(h_values, cuts["prasada"]["v1"], cuts["prasada"]["v2"],
                                                       pr.level_of, pr.LABELS)}
    print("mādhurya, prasāda agreement:", report["madhurya"]["agreement"]["poems_same_label_pct"],
          report["prasada"]["agreement"]["poems_same_label_pct"])

    report["anuprasa"]["examples"] = anuprasa_examples(base1, base2)
    report["madhurya"]["examples"] = madhurya_examples(cuts["madhurya"]["v1"], cuts["madhurya"]["v2"])
    report["prasada"]["examples"] = prasada_examples(model, cuts["prasada"]["v1"], cuts["prasada"]["v2"])

    texts = degraded_texts(args.seed)
    deg = anuprasa_degradations(texts, {"v1": anuprasa_z(base1["level_probs"]), "v2": anuprasa_z(base2["level_probs"])})
    protocol = HERE / "outputs" / "degradation_protocol.json"
    if protocol.exists():
        stored = json.loads(protocol.read_text(encoding="utf-8"))["degradations"]
        deg["v1_reproduces_degradation_protocol_json"] = all(
            stored[d]["anuprasa"]["steps"] == deg[d]["v1"]["steps"] for d in stored)
    report["anuprasa"]["degradations"] = deg
    print("anuprāsa degradations:", {d: (v["v1"]["verdict"], v["v2"]["verdict"]) for d, v in deg.items() if isinstance(v, dict)})

    rounded = lambda z: None if z is None else round(z, 3)          # noqa: E731
    real = {"anuprasa_v1": [rounded(r[HEADLINE][0]) for c in corpus.CORPORA for r in anu_results[c][0]],
            "anuprasa_v2": [rounded(r[HEADLINE][0]) for c in corpus.CORPORA for r in anu_results[c][1]],
            "madhurya": [v for c in corpus.CORPORA for v in m_values[c][0]],
            "surprisal": [v for c in corpus.CORPORA for v in h_values[c][0]]}
    report["nonsense_control"], constrained_h = nonsense_control(real, base1, base2, cuts, model)
    stored = HERE / "outputs" / "samples_analysis.json"
    if stored.exists():
        cells = json.loads(stored.read_text(encoding="utf-8"))["cells"]
        report["nonsense_control"]["v1_reproduces_samples_analysis_json"] = all(
            cells[k]["against_real"]["anuprasa_varga_z"]["p_generated_above_real"] == v["anuprasa_v1"]
            for k, v in report["nonsense_control"]["cells"].items())
    print("nonsense:", report["nonsense_control"]["anuprasa_v1_p_above_real"], report["nonsense_control"]["anuprasa_v2_p_above_real"])

    lp_variants1 = {name: ap.level_probabilities(base1["probabilities"], keyf) for name, (keyf, _) in va.VARIANTS.items()}
    lp_variants2 = {name: ap.level_probabilities(base2["probabilities"], keyf) for name, (keyf, _) in va.VARIANTS.items()}
    kg1, kg2 = va.known_groups(lp_variants1), va.known_groups(lp_variants2)
    report["anuprasa"]["known_groups"] = {
        f"auc_sabda_vs_artha_{level}": {"v1": kg1.get(f"auc_sabda_vs_artha_{level}"),
                                        "v2": kg2.get(f"auc_sabda_vs_artha_{level}")} for level in ap.LEVELS}

    report["anuprasa"]["new_poet"] = anuprasa_new_poet(tokens_by_corpus, anu_results, base1, base2)
    report["madhurya"]["new_poet"] = rubric_new_poet(m_values, cuts["madhurya"]["v1"],
                                                     {"poem": md2.anchored_cuts()[0], "line": md2.anchored_cuts()[0]},
                                                     cuts["madhurya"]["v2"], md.level_of)
    again = pr2.anchored_cuts(model)[0]
    report["prasada"]["new_poet"] = rubric_new_poet(h_values, cuts["prasada"]["v1"], {"poem": again, "line": again},
                                                    cuts["prasada"]["v2"], pr.level_of)
    report["prasada"]["new_poet"]["not_measured"] = (
        "version 1 rebuilt for a new poet would also retrain its model without that poet's poems; version 2 never "
        "retrains. Only the rubric's share is measured here.")
    print("new poet:", {c: v.get("v1_lines_relabelled_pct") for c, v in report["anuprasa"]["new_poet"].items()
                        if isinstance(v, dict)})

    report["anuprasa"]["corpus_free"] = corpus_free_anuprasa(tokens_by_corpus, anu_results, texts, base1, args.seed)
    report["alternative_rubrics"] = alternative_rubrics(m_values, h_values, model, constrained_h)

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(HERE)}")


if __name__ == "__main__":
    main()
