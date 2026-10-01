"""The poetry metrics on the generated poems of ../samples/json.

Three models (Gemma-4 E4B, Gemma-4 26B-A4B, DiffusionGemma 26B-A4B), four
ablations each (free baseline, masking only, masking + backtracking, hybrid),
555 poems per cell: 37 meters x 3 topics x 5 seeds. Every constrained poem is in
meter by construction, and most of its words are not real words
(samples/README.md). The questions here:

1. How do the metrics (anuprāsa, mādhurya, ojas, prasāda, chandas distance) of generated poems
   compare with real verse, overall and within the eight meters that both have
   in number?
2. What in the generated text drives the difference: repetition, conjuncts,
   filler aksharas?
3. Do the metrics move with how hard the constraint pushed (the share of tokens
   it overrode, the model's probability of its tokens) and with the share of
   real words?
4. Does the topic change the texture, as content does in real verse?

    python3 samples_analysis.py            # -> outputs/samples_analysis.json, outputs/samples_scores.jsonl
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import anuprasa as ap                                     # noqa: E402
import chandas_distance as cd                             # noqa: E402
import madhurya as md                                     # noqa: E402
import ojas as oj                                         # noqa: E402
import prasada as pr                                      # noqa: E402
import validation_madhurya as vm                          # noqa: E402
from common import corpus                                 # noqa: E402
from common.phonology import aksharas, line_aksharas, normalise   # noqa: E402

SAMPLES_DIR = HERE.parent / "samples" / "json"
MODELS = ("gemma-4-E4B-it", "gemma-4-26B-A4B-it", "diffusiongemma-26B-A4B-it")
ABLATIONS = ("baseline", "masking_only", "masking_backtrack", "hybrid")
# dataset metre labels -> the meter ids of the samples
NAME_MAP = cd.NAME_MAP
MIN_REAL_PER_METER = 500         # a meter is "shared" when the datasets have this many real poems of it
TENDER_TOPIC = "T1"              # తల్లి ప్రేమ (a mother's love); T2 and T3 are heroic journeys
METRICS = ("anuprasa_varga_z", "anuprasa_varna_z", "anuprasa_score", "madhurya", "inventory", "pileup",
           "sonority", "runs_z", "conjunct_share", "parusha_share", "madhura_share", "sonorant_share",
           "ojas", "word_length", "conjunct_rate", "aspirate_rate", "surprisal", "zipf", "known_word_share",
           "chandas_distance", "chandas_rate", "chandas_skill",
           "chandas_weight_edits", "chandas_yati_edits", "chandas_prasa_edits")
DRIVERS = ("overridden_share", "mean_logprob", "real_word_share", "one_akshara_word_share",
           "distinct_akshara_ratio", "duplicate_lines")


# --- scoring one poem -------------------------------------------------------------

def words_of(lines) -> list:
    return [w for l in lines for w in normalise(l).split()]


def chandas(lines, baseline: dict, meter) -> dict:
    """The distance to the poem's own meter; empty figures when the meter is not in the catalogue."""
    if meter not in baseline["meters"]:
        return {"chandas_distance": None, "chandas_rate": None, "chandas_skill": None, "chandas_level": None,
                "chandas_weight_edits": None, "chandas_yati_edits": None, "chandas_prasa_edits": None,
                "chandas_edits": None, "chandas_length_gap": None}
    row = cd.score_poem(lines, baseline, meter)
    return {"chandas_distance": row["distance"], "chandas_rate": row["edits_per_100_aksharas"],
            "chandas_skill": row["skill"], "chandas_level": row["level"],
            "chandas_weight_edits": row["weight_edits"], "chandas_yati_edits": row["yati_edits"],
            "chandas_prasa_edits": row["prasa_edits"],
            "chandas_edits": {k: row[k] for k in ("substitutions", "insertions", "deletions")},
            # below 0: the poem is shorter than the nearest poem in meter
            "chandas_length_gap": (row["n_aksharas"] - row["target_aksharas"]) / row["target_aksharas"]}


def score(lines, baselines, vocabulary, meter=None) -> dict:
    """Every figure the analysis uses, for one poem given as lines."""
    a = ap.score_poem(lines, baselines["anuprasa"])
    profiles = md.profile_poem(lines)
    total = md.pooled(profiles)
    n = total.n or 1
    classes = vm.class_sequence(lines)
    words = words_of(lines)
    long_words = [w for w in words if len(aksharas(w)) >= 2]
    z = vm.runs_z([md.WEIGHTS[c] < 0 for c in classes])
    heaviest = max(total.runs, key=lambda r: r.load, default=None)
    clusters = Counter("్".join(a.onset) for l in lines for a in line_aksharas(l) if len(a.onset) >= 2)
    density = oj.pooled(oj.count_poem(lines))
    clarity = pr.poem_figures(baselines["prasada"], lines)
    return {
        **chandas(lines, baselines["chandas"], meter),
        "ojas": oj.index(density), "word_length": density.word_length,
        "conjunct_rate": density.conjunct_rate, "aspirate_rate": density.aspirate_rate,
        "ojas_level": oj.level_of(oj.index(density), baselines["ojas"]["cuts"]["poem"]),
        "surprisal": clarity["surprisal"], "zipf": clarity["zipf"], "known_word_share": clarity["known_word_share"],
        "prasada_level": pr.level_of(clarity["surprisal"], baselines["prasada"].meta["cuts"]["poem"]),
        "rules": dict(total.rules), "clusters": clusters,
        "anuprasa_varga_z": a["varga"]["z"], "anuprasa_varna_z": a["varna"]["z"], "anuprasa_score": a["varga"]["score"],
        "madhurya": total.index(), "inventory": total.inventory, "pileup": total.pileup, "sonority": total.sonority,
        "level": md.level_of(total.index(), baselines["madhurya"]["cuts"]["poem"]),
        "runs_z": z,
        "harshest_run_load": heaviest.load if heaviest else 0.0,
        **{f"{c}_share": total.classes[c] / n for c in md.CLASSES},
        "n_aksharas": total.n, "n_lines": len(lines),
        "one_akshara_word_share": (len(words) - len(long_words)) / len(words) if words else None,
        "real_word_share": sum(w in vocabulary for w in long_words) / len(long_words) if long_words else None,
    }


def load_baselines() -> dict:
    return {"anuprasa": ap.load_baseline(), "madhurya": md.load_baseline(),
            "ojas": oj.load_baseline(), "prasada": pr.load_model(), "chandas": cd.load_baseline()}


def real_vocabulary() -> frozenset:
    """Words of two or more aksharas in the verse of the four dataset files."""
    return frozenset(w for c in corpus.CORPORA for p in corpus.load(c) for w in words_of(p.lines)
                     if len(aksharas(w)) >= 2)


# --- loading -----------------------------------------------------------------------

def generated_poems():
    """Every poem of every model, with the fields the analysis needs."""
    for model in MODELS:
        for part in (1, 2, 3, 4):
            path = SAMPLES_DIR / f"{model}.part{part}.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            label = data["model"]["label"]
            for p in data["poems"]:
                probs = [t["prob"] for t in p["tokens"] if t.get("prob")]
                known = [t["overridden"] for t in p["tokens"] if t.get("overridden") is not None]
                ev = p["evaluation"]
                yield {
                    "model": label, "id": p["id"], "meter": p["meter"], "meter_class": p["meter_class"],
                    "topic": p["topic"], "ablation": p["ablation"], "seed": p["seed"], "status": p["status"],
                    "lines": [l for l in p["poem"]["lines"] if l.strip()],
                    "in_meter": bool(ev.get("all_strict")),
                    "duplicate_lines": ev.get("duplicate_lines"),
                    "distinct_akshara_ratio": ev.get("distinct_akshara_ratio"),
                    "mean_logprob": statistics.fmean(math.log(x) for x in probs) if probs else None,
                    "overridden_share": sum(known) / len(known) if known else None,
                }
            del data


# --- summaries ----------------------------------------------------------------------

def mean(values):
    values = [v for v in values if v is not None]
    return round(statistics.fmean(values), 4) if values else None


def median(values):
    values = [v for v in values if v is not None]
    return round(statistics.median(values), 4) if values else None


def above(gen: list, real: list):
    """P(a generated poem scores above a real one), ties half."""
    gen = [v for v in gen if v is not None]
    real = [v for v in real if v is not None]
    return vm.auc(gen, real)["auc"] if gen and real else None


def summarise(rows: list) -> dict:
    out = {"n": len(rows)}
    for m in METRICS + DRIVERS + ("harshest_run_load", "in_meter"):
        out[m] = mean([r[m] for r in rows])
    out["median_anuprasa_varga_z"] = median([r["anuprasa_varga_z"] for r in rows])
    out["median_madhurya"] = median([r["madhurya"] for r in rows])
    levels = Counter(r["level"] for r in rows if r["level"] is not None)
    out["madhurya_levels_pct"] = {md.LABELS[k]: round(100 * levels[k] / len(rows), 1) for k in range(5)}
    for name, labels in (("ojas", oj.LABELS), ("prasada", pr.LABELS), ("chandas", cd.LABELS)):
        levels = Counter(r[f"{name}_level"] for r in rows if r[f"{name}_level"] is not None)
        out[f"{name}_levels_pct"] = {labels[k]: round(100 * levels[k] / len(rows), 1) for k in range(5)}
    out["median_surprisal"] = median([r["surprisal"] for r in rows])
    out["median_ojas"] = median([r["ojas"] for r in rows])
    out["anuprasa_poems_at_or_above_pct"] = {
        label: round(100 * sum(1 for r in rows if (r["anuprasa_varga_z"] or 0) >= cut) / len(rows), 1)
        for cut, _, label in reversed(ap.RUBRIC)}
    out["poems_with_a_repeated_line_pct"] = round(100 * sum(1 for r in rows if r["duplicate_lines"]) / len(rows), 1)
    zs = [r["runs_z"] for r in rows if r["runs_z"] is not None]
    out["harsh_runs_clumped_pct"] = round(100 * sum(z < -1.645 for z in zs) / len(zs), 1) if zs else None
    n_aksharas = sum(r["n_aksharas"] for r in rows)
    out["rules_per_100_aksharas"] = {rule: round(100 * sum(r["rules"].get(rule, 0) for r in rows) / n_aksharas, 2)
                                     for rule in md.RULES}
    clusters = Counter()
    for r in rows:
        clusters.update(r["clusters"])
    out["conjunct_onsets_per_100_aksharas"] = round(100 * sum(clusters.values()) / n_aksharas, 2)
    out["commonest_conjunct_onsets_per_100_aksharas"] = {c: round(100 * k / n_aksharas, 2)
                                                         for c, k in clusters.most_common(10)}
    return out


def compare(gen_rows: list, real_rows: list, real_by_meter: dict, shared: list) -> dict:
    """Generated against real verse: over all poems, and within the shared meters."""
    out = {}
    for m in METRICS:
        overall = above([r[m] for r in gen_rows], [r[m] for r in real_rows])
        per_meter = []
        for meter in shared:
            g = [r[m] for r in gen_rows if r["meter"] == meter and r[m] is not None]
            real = [r[m] for r in real_by_meter[meter] if r[m] is not None]
            if g and real:
                per_meter.append((statistics.fmean(g) - statistics.fmean(real), vm.auc(g, real)["auc"]))
        out[m] = {
            "p_generated_above_real": overall,
            "within_meter_mean_difference": round(statistics.fmean(d for d, _ in per_meter), 4) if per_meter else None,
            "within_meter_p_generated_above_real": round(statistics.fmean(a for _, a in per_meter), 4)
            if per_meter else None,
        }
    return out


def correlations(rows: list) -> dict:
    out = {}
    for m in ("anuprasa_varga_z", "madhurya", "inventory", "pileup", "ojas", "surprisal"):
        out[m] = {}
        for d in DRIVERS:
            pairs = [(r[m], r[d]) for r in rows if r[m] is not None and r[d] is not None]
            out[m][d] = vm.spearman([a for a, _ in pairs], [b for _, b in pairs]) if len(pairs) > 30 else None
    return out


def topic_effect(rows: list) -> dict:
    tender = [r["madhurya"] for r in rows if r["topic"] == TENDER_TOPIC and r["madhurya"] is not None]
    heroic = [r["madhurya"] for r in rows if r["topic"] != TENDER_TOPIC and r["madhurya"] is not None]
    return {**vm.auc(tender, heroic), "mean_tender_topic": mean(tender), "mean_heroic_topics": mean(heroic)}


def examples(rows: list, key: str, top: int = 4, reverse: bool = True) -> list:
    chosen = sorted((r for r in rows if r[key] is not None), key=lambda r: r[key], reverse=reverse)[:top]
    return [{"model": r["model"], "id": r["id"], key: round(r[key], 3), "lines": r["lines"]} for r in chosen]


def chandas_by_class(rows: list) -> dict:
    """How far the poems are from their meter, per class of meter and over all: distance, kinds of edit, length."""
    out = {}
    for cls in sorted({r["meter_class"] for r in rows}) + ["all"]:
        sub = [r for r in rows if cls in ("all", r["meter_class"])]
        edits = Counter()
        for r in sub:
            edits.update(r["chandas_edits"])
        total = sum(edits.values()) or 1
        out[cls] = {"n": len(sub), **{m: mean([r[m] for r in sub])
                                      for m in ("chandas_distance", "chandas_weight_edits", "chandas_yati_edits",
                                                "chandas_prasa_edits", "chandas_rate", "chandas_skill",
                                                "chandas_length_gap")},
                    "weight_edits_pct": {k: round(100 * v / total, 1) for k, v in sorted(edits.items())},
                    "skill_above_half_pct": round(100 * sum(r["chandas_skill"] > 0.5 for r in sub) / len(sub), 1)}
    return out


def prasada_gate(rows: list, top: int = 500) -> dict:
    """The constrained poems that prasāda rates "ordinary" or clearer, and what gets through with them."""
    ordinary = pr.LABELS.index("ordinary")
    passed = [r for r in rows if r["prasada_level"] is not None and r["prasada_level"] >= ordinary]
    failed = [r for r in rows if r["prasada_level"] is not None and r["prasada_level"] < ordinary]
    alliterative = sorted((r for r in rows if r["anuprasa_varga_z"] is not None),
                          key=lambda r: r["anuprasa_varga_z"], reverse=True)[:top]
    levels = Counter(r["prasada_level"] for r in alliterative)
    return {
        "constrained_poems": len(rows), "ordinary_or_clearer": len(passed),
        "by_model": dict(sorted(Counter(r["model"] for r in passed).items())),
        "by_meter_class": dict(sorted(Counter(r["meter_class"] for r in passed).items())),
        "with_a_repeated_line": sum(1 for r in passed if r["duplicate_lines"]),
        "real_word_share": {"ordinary_or_clearer": mean([r["real_word_share"] for r in passed]),
                            "below_ordinary": mean([r["real_word_share"] for r in failed])},
        "most_alliterative": {"n": len(alliterative), **{pr.LABELS[k]: levels[k] for k in range(5)}},
    }


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.parse_args(argv)
    baselines = load_baselines()
    vocabulary = real_vocabulary()

    # real verse, scored the same way
    real_rows, real_by_meter = [], defaultdict(list)
    for cname in corpus.CORPORA:
        for p in corpus.load(cname):
            meter = NAME_MAP.get(p.metre, p.metre)
            row = {"corpus": cname, "meter": meter, **score(p.lines, baselines, vocabulary, meter)}
            real_rows.append(row)
            real_by_meter[row["meter"]].append(row)
    shared = sorted(m for m, rows in real_by_meter.items() if m and len(rows) >= MIN_REAL_PER_METER)
    print(f"real verse: {len(real_rows)} poems; shared meters: {shared}")

    gen_rows = []
    for p in generated_poems():
        lines = p.pop("lines")
        if not lines:
            continue
        gen_rows.append({**p, "lines": lines, **score(lines, baselines, vocabulary, p["meter"])})
    print(f"generated: {len(gen_rows)} poems")

    report = {
        "anuprasa_version": ap.VERSION, "madhurya_version": md.VERSION,
        "ojas_version": oj.VERSION, "prasada_version": pr.VERSION, "chandas_distance_version": cd.VERSION,
        "shared_meters": shared,
        "real": {"all": summarise_real(real_rows),
                 "shared_meters": summarise_real([r for r in real_rows if r["meter"] in shared])},
        "cells": {}, "models": {},
    }
    cells = defaultdict(list)
    for r in gen_rows:
        cells[(r["model"], r["ablation"])].append(r)
    for (model, ablation), rows in cells.items():
        report["cells"][f"{model} | {ablation}"] = {
            **summarise(rows),
            "against_real": compare(rows, real_rows, real_by_meter, shared),
            "topic_effect_on_madhurya": topic_effect(rows),
        }
    # how often the generated poems' commonest conjuncts occur in real verse
    wanted = {c for cell in report["cells"].values() for c in cell["commonest_conjunct_onsets_per_100_aksharas"]}
    real_clusters, real_aksharas = Counter(), sum(r["n_aksharas"] for r in real_rows)
    for r in real_rows:
        real_clusters.update(r["clusters"])
    report["real"]["rate_of_generated_conjuncts_per_100_aksharas"] = {
        c: round(100 * real_clusters[c] / real_aksharas, 3) for c in sorted(wanted, key=lambda c: -real_clusters[c])}
    report["real"]["by_shared_meter"] = {
        meter: {"n": len(real_by_meter[meter]),
                **{m: mean([r[m] for r in real_by_meter[meter]])
                   for m in ("anuprasa_varga_z", "madhurya", "pileup", "ojas", "surprisal")}}
        for meter in shared}
    for model in sorted({r["model"] for r in gen_rows}):
        constrained = [r for r in gen_rows if r["model"] == model and r["ablation"] != "baseline"]
        report["models"][model] = {
            "constrained_poems": len(constrained),
            "by_shared_meter": {
                meter: {m: mean([r[m] for r in constrained if r["meter"] == meter])
                        for m in ("anuprasa_varga_z", "madhurya", "pileup", "overridden_share", "real_word_share",
                                  "ojas", "surprisal")}
                for meter in shared},
            "spearman_with_generation": correlations(constrained),
            "by_meter_class": {cls: {m: mean([r[m] for r in constrained if r["meter_class"] == cls])
                                     for m in ("anuprasa_varga_z", "madhurya", "pileup", "conjunct_share",
                                               "overridden_share", "real_word_share", "ojas", "surprisal")}
                               for cls in sorted({r["meter_class"] for r in constrained})},
            "highest_anuprasa": examples(constrained, "anuprasa_varga_z", top=3),
            "softest": examples(constrained, "madhurya", top=3),
            "harshest": examples(constrained, "madhurya", top=3, reverse=False),
            "clearest": examples(constrained, "surprisal", top=3, reverse=False),
            "most_obscure": examples(constrained, "surprisal", top=3),
            "unconstrained_chandas_by_meter_class": chandas_by_class(
                [r for r in gen_rows if r["model"] == model and r["ablation"] == "baseline"]),
        }

    report["prasada_gate"] = prasada_gate([r for r in gen_rows if r["ablation"] != "baseline"])

    md.OUTPUT_DIR.mkdir(exist_ok=True)
    path = md.OUTPUT_DIR / "samples_analysis.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    scores = md.OUTPUT_DIR / "samples_scores.jsonl"
    with open(scores, "w", encoding="utf-8") as f:
        for r in gen_rows:
            row = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()
                   if k not in ("lines", "clusters")}
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"wrote {path.relative_to(HERE)} and {scores.relative_to(HERE)}")


def summarise_real(rows: list) -> dict:
    """The summary of real verse; the generation fields do not apply."""
    padded = [{**{d: None for d in DRIVERS}, "in_meter": None, **r} for r in rows]
    return summarise(padded)


if __name__ == "__main__":
    main()
