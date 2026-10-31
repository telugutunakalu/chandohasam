"""The poetics suite on every poem source: the four dataset files and both human-evaluation studies, one JSON per source.

    python3 score_sources.py                  # ≈ 3 min → outputs/sources/<source>.json, summary.json, reports/sources.md
    python3 score_sources.py --only dataset_vemana human_evals_study2_nandi_ft

Sources (the unit is the printed line, a sīsa pāda split into its half-lines as every metric reads it):
- `dataset_<file>`: the verse records of ../dataset/{bhagavatam,vemana,kuchimanchi_timmakavi,chandassu}.json
  (common/corpus.py; prose records are left out).
- `human_evals_study1_<source>`: the 500 poems of study 1 (../human_evals/human_eval_poems_strict.json, the pool the
  app shows), by source: Bhāgavatam, Vemana, Kūcimañci, the textbook examples, and Gemini's poems.
- `human_evals_study2_<model>`: the 99 poems of study 2 (../human_evals/human_eval_poems_study2.json), by model:
  MDLM 523M, T5Gemma 2 1B and Nandi-Mini-150M, each fine-tuned and under the v2 metrical decoder.
- `gemini_initial_evals`: every Gemini-written poem of ../metrics/initial_evals/Outputs/chandas_dataset.json (255;
  exact duplicates dropped by ../human_evals/build_human_eval_sample.py's rule: 246), the set
  ../final_report_metrics/export_poems.py exports. Study 1's 84 Gemini poems are among them. Broken down also by the
  alaṅkāra the prompt asked for and by whether the poem is in study 1's pool.

Metrics, each the metric script's own score_poem with its frozen baseline (nothing is rebuilt): anuprāsa 1.0, 2.0
and 3.0; mādhurya 1.1 and 2.0; ojas 2.0; prasāda 1.0 and 2.0; chandas distance 1.1 against the poem's own metre
(the nearest metre when the label is missing or not in the catalogue). Versions 2.0 of mādhurya and prasāda keep
version 1's scores and change only the labels.

Each source file holds, per metric, the summary of its main value (n, mean, sd, quantiles), its label counts and
shares, the same by metre (and by the source's own groups), and every poem's main values and labels (no text). Study 2's file also compares each poem
with the gold poem of its prompt (its study-1 poem), metric by metric.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import corpus                                                   # noqa: E402

import anuprasa, anuprasa_v2, anuprasa_v3                                   # noqa: E402,E401
import chandas_distance as cd                                               # noqa: E402
import madhurya, madhurya_v2, ojas, prasada, prasada_v2                     # noqa: E402,E401

HUMAN_EVALS = HERE.parent / "human_evals"
GEMINI = HERE.parent / "metrics" / "initial_evals" / "Outputs" / "chandas_dataset.json"
# chandas_dataset.json's metre ids -> the catalogue's (as ../final_report_metrics/export_poems.py maps them)
GEMINI_METRES = {"shardulavikriditam": "sardulavikriditamu", "mattebhavikriditam": "mattebhavikriditamu",
                 "aataveladi": "ataveladi", "seesam": "seesamu", "kandam": "kandamu", "utsaham": "utsahamu"}
OUT = HERE / "outputs" / "sources"
REPORT = HERE / "reports" / "sources.md"

# metric -> (module, its main continuous value, the extra values kept per poem)
METRICS = {
    "anuprasa_v1": (anuprasa, "z", []),
    "anuprasa_v2": (anuprasa_v2, "z", []),
    "anuprasa_v3": (anuprasa_v3, "anuprasa", ["longest_repeated_ngram", "percentile"]),
    "madhurya_v1": (madhurya, "madhurya", ["percentile", "pileup", "sonority"]),
    "madhurya_v2": (madhurya_v2, "madhurya", []),
    "ojas": (ojas, "ojas", ["percentile", "conjunct_rate", "word_length"]),
    "prasada_v1": (prasada, "surprisal", ["percentile", "known_word_share", "zipf"]),
    "prasada_v2": (prasada_v2, "surprisal", []),
    "chandas_distance": (cd, "skill", ["meter", "meter_given", "distance", "edits_per_100_aksharas"]),
}
# a metric's labels from its lowest to its highest level
LABEL_ORDER = {                                    # the version 2.0 candidates keep version 1's labels
    "anuprasa_v1": list(anuprasa.LABELS.values()), "anuprasa_v2": list(anuprasa.LABELS.values()),
    "anuprasa_v3": anuprasa_v3.LABELS, "madhurya_v1": madhurya.LABELS, "madhurya_v2": madhurya.LABELS,
    "ojas": ojas.LABELS, "prasada_v1": prasada.LABELS, "prasada_v2": prasada.LABELS, "chandas_distance": cd.LABELS,
}
DATASETS = {"bhagavatam": "Pothana's Bhāgavatam", "vemana": "Vemana", "kuchimanchi_timmakavi": "Kūcimañci Timmakavi",
            "chandassu": "chandassu: 25 śatakams (the Kaggle Chandassu dataset)"}
STUDY1 = {"bhagavatam": ("bhagavatam", "Pothana's Bhāgavatam", "human"), "vemana": ("vemana", "Vemana", "human"),
          "kuchimanchi": ("kuchimanchi", "Kūcimañci Timmakavi", "human"),
          "reference": ("textbook", "textbook examples (prosody textbooks)", "human"),
          "generated": ("gemini", "Gemini-generated", "ai")}
STUDY2 = {"mdlm523m_ft": "MDLM 523M, fine-tuned, v2 decoder", "t5_1b_ft": "T5Gemma 2 1B, fine-tuned, v2 decoder",
          "nandi_ft": "Nandi-Mini-150M, fine-tuned, v2 decoder"}


def load_scorers() -> dict:
    """metric -> score(lines, metre) with the metric's frozen baseline or model loaded once."""
    known = {m.name for m in cd.default_dawg().catalogue.concrete}
    cd_base = cd.load_baseline()
    out = {}
    for name, (mod, _, _) in METRICS.items():
        if mod is cd:
            out[name] = lambda lines, metre: cd.score_poem(lines, cd_base, metre if metre in known else None)
        else:
            base = mod.load_model() if mod in (prasada, prasada_v2) else mod.load_baseline()
            out[name] = (lambda m, b: lambda lines, metre: m.score_poem(lines, b))(mod, base)
    return out


def sources() -> dict:
    """source name -> {meta, poems: [(id, metre for chandas, metre label, lines, extra)]}."""
    out = {}
    for stem, title in DATASETS.items():
        poems = [(p.key, cd.NAME_MAP.get(p.metre, p.metre), p.metre, list(p.lines), {}) for p in corpus.load(stem)]
        out[f"dataset_{stem}"] = {"family": "dataset", "title": title, "kind": "human",
                                  "from": f"dataset/{corpus.CORPORA[stem]} (verse records)", "poems": poems}
    for study, path, groups, key in (("study1", "human_eval_poems_strict.json", STUDY1, "source_dataset"),
                                     ("study2", "human_eval_poems_study2.json", STUDY2, "source_dataset")):
        recs = json.loads((HUMAN_EVALS / path).read_text(encoding="utf-8"))["poems"]
        by = defaultdict(list)
        for r in recs:
            extra = {"source_id": r["source_id"]}
            if study == "study2":
                md = r["metadata"]
                extra |= {"prompt_id": md["prompt_id"], "gold_eval_id": md["gold_eval_id"]}
            lines = [corpus._clean(l) for l in r["lines"] if corpus._clean(l)]
            by[r[key]].append((r["eval_id"], cd.NAME_MAP.get(r["meter_id"], r["meter_id"]), r["meter_id"], lines, extra))
        for src, poems in by.items():
            if study == "study1":
                short, title, kind = groups[src]
            else:
                short, title, kind = src, groups[src], "ai"
            out[f"human_evals_{study}_{short}"] = {"family": f"human_evals_{study}", "title": title, "kind": kind,
                                                   "from": f"human_evals/{path} (source_dataset {src})", "poems": poems}
    recs = json.loads(GEMINI.read_text(encoding="utf-8"))["poems"]
    drop = {max(r["id"], d) for r in recs for d in (r.get("duplicate_exact") or [])}
    pool = {r["source_id"] for r in json.loads((HUMAN_EVALS / "human_eval_poems_strict.json").read_text(encoding="utf-8"))["poems"]
            if r["source_dataset"] == "generated"}
    poems = []
    for r in recs:
        if r["id"] in drop:
            continue
        metre = GEMINI_METRES.get(r.get("chandassu_id"), r.get("chandassu_id"))
        lines = [corpus._clean(l) for l in r["lines"] if corpus._clean(l)]
        extra = {"alankaram": r.get("alankaram_id") or "(none asked)", "in_study1_pool": r["id"] in pool}
        poems.append((f"gemini:{r['id']}", cd.NAME_MAP.get(metre, metre), metre, lines, extra))
    out["gemini_initial_evals"] = {"family": "gemini", "title": "Gemini-written poems (metrics/initial_evals)",
                                   "kind": "ai", "from": "metrics/initial_evals/Outputs/chandas_dataset.json "
                                   "(exact duplicates dropped)", "poems": poems, "group_by": ["alankaram", "in_study1_pool"]}
    return out


def score_source(src: dict, scorers: dict) -> list:
    rows = []
    for pid, cd_metre, metre, lines, extra in src["poems"]:
        row = {"id": pid, "metre": metre, "n_lines": len(lines), **extra}
        for name, (_, main, keep) in METRICS.items():
            r = scorers[name](lines, cd_metre)
            row[name] = {"value": r.get(main), "level": r.get("level", r.get("score")), "label": r.get("label"),
                         **{k: r.get(k) for k in keep}}
        rows.append(row)
    return rows


def describe(values: list) -> dict:
    v = sorted(x for x in values if x is not None)
    if not v:
        return {"n": 0}
    q = lambda p: v[min(len(v) - 1, round(p * (len(v) - 1)))]
    return {"n": len(v), "mean": round(statistics.fmean(v), 4), "sd": round(statistics.pstdev(v), 4),
            "p10": q(0.1), "median": q(0.5), "p90": q(0.9)}


def summarise(rows: list) -> dict:
    out = {}
    for name in METRICS:
        labels = Counter(r[name]["label"] for r in rows)
        n = sum(labels.values())
        entry = {"value": describe([r[name]["value"] for r in rows]),
                 "labels": {lab: {"n": labels.get(lab, 0), "share": round(labels.get(lab, 0) / n, 4) if n else None}
                            for lab in LABEL_ORDER[name]}}
        if name == "chandas_distance":
            entry["distance"] = describe([r[name]["distance"] for r in rows])
            entry["edits_per_100_aksharas"] = describe([r[name]["edits_per_100_aksharas"] for r in rows])
            entry["metre_given"] = sum(bool(r[name]["meter_given"]) for r in rows)
        out[name] = entry
    return out


def by_metre(rows: list, key: str = "metre") -> dict:
    groups = defaultdict(list)
    for r in rows:
        groups[str(r[key]) if r[key] is not None else "(none)"].append(r)
    return {m: {"n": len(g), **{name: {"mean": describe([r[name]["value"] for r in g]).get("mean"),
                                       "labels": dict(Counter(r[name]["label"] for r in g))} for name in METRICS}}
            for m, g in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))}


def against_gold(rows: list, gold: dict) -> dict:
    """Study 2: each poem minus the gold poem of its prompt, per metric's main value (and the share above gold)."""
    out = {}
    for name in METRICS:
        diffs = [r[name]["value"] - gold[r["gold_eval_id"]][name]["value"] for r in rows
                 if r["gold_eval_id"] in gold and r[name]["value"] is not None
                 and gold[r["gold_eval_id"]][name]["value"] is not None]
        out[name] = {"n_pairs": len(diffs), "mean_difference": round(statistics.fmean(diffs), 4) if diffs else None,
                     "share_above_gold": round(sum(d > 0 for d in diffs) / len(diffs), 4) if diffs else None,
                     "share_equal": round(sum(d == 0 for d in diffs) / len(diffs), 4) if diffs else None}
    return out


def versions() -> dict:
    return {name: mod.VERSION for name, (mod, _, _) in METRICS.items()} | {
        "main_value": {name: main for name, (_, main, _) in METRICS.items()}}


def report(index: dict) -> str:
    cols = [("anuprasa_v3", "anuprāsa 3.0 A", "strong"), ("madhurya_v1", "mādhurya M", "harsh"),
            ("ojas", "ojas", "dense"), ("prasada_v1", "prasāda surprisal", "clear"),
            ("chandas_distance", "chandas skill", "exact")]
    out = ["# The poetics suite on every poem source", "",
           "Written by `score_sources.py` (`outputs/sources/<source>.json`, `outputs/sources/summary.json`). Medians "
           "of each metric's main value (a few showpieces pull some means far off: two textbook examples reach "
           "anuprāsa A = 50 and 176); in brackets the share of poems at the label named in the column. Means, "
           "quantiles, per-metre breakdowns, every label's share and every poem's scores are in the source's JSON.", "",
           "Directions: anuprāsa A higher = more repeated consonant patterns; mādhurya M higher = softer; ojas higher "
           "= denser; prasāda surprisal higher = more obscure (lower = clearer); chandas skill 1 = exactly in metre.", "",
           "| source | kind | poems | " + " | ".join(f"{t} [{lab}]" for _, t, lab in cols) + " |",
           "|---|---|---:|" + "---|" * len(cols)]
    for name, s in index["sources"].items():
        cells = []
        for metric, _, lab in cols:
            m = s["summary"][metric]
            share = m["labels"].get(lab, {}).get("share")
            cells.append(f"{m['value'].get('median', float('nan')):.3f} [{100 * share:.0f}%]" if share is not None
                         else f"{m['value'].get('median', float('nan')):.3f}")
        out.append(f"| `{name}` | {s['kind']} | {s['n_poems']} | " + " | ".join(cells) + " |")
    out += ["", "Labels: anuprāsa 3.0 none / weak / marked / strong (A against the treatise's example, 1.33); mādhurya "
            + " / ".join(madhurya.LABELS) + "; ojas " + " / ".join(ojas.LABELS) + "; prasāda (1.0) "
            + " / ".join(prasada.LABELS) + "; chandas distance " + " / ".join(cd.LABELS) + ".", ""]
    s2 = {k: v for k, v in index["sources"].items() if "against_gold" in v}
    if s2:
        out += ["## Study 2 against the gold poems of the same prompts", "",
                "Each model poem minus the study-1 gold poem of its prompt (33 pairs per model): mean difference of the "
                "main value, and the share of prompts where the model's poem scores higher (for prasāda surprisal, "
                "higher is more obscure).", "",
                "| model | " + " | ".join(t for _, t, _ in cols) + " |", "|---|" + "---|" * len(cols)]
        for name, s in s2.items():
            g = s["against_gold"]
            out.append(f"| `{name}` | " + " | ".join(
                "equal on every prompt" if g[m]["share_equal"] == 1 else
                f"{g[m]['mean_difference']:+.3f} ({100 * g[m]['share_above_gold']:.0f}% above)" for m, _, _ in cols) + " |")
        out.append("")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="these sources only (default: every source)")
    args = ap.parse_args(argv)
    srcs = sources()
    todo = args.only or list(srcs)
    scorers = load_scorers()
    OUT.mkdir(parents=True, exist_ok=True)
    scored = {}
    for name in todo:
        scored[name] = score_source(srcs[name], scorers)
        print(f"{name}: {len(scored[name])} poems", flush=True)
    gold = {}
    for name, rows in scored.items():
        if name.startswith("human_evals_study1_"):
            gold |= {r["id"]: r for r in rows}
    if any(n.startswith("human_evals_study2_") for n in todo) and not gold:      # the golds, for the comparison
        for name in (n for n in srcs if n.startswith("human_evals_study1_")):
            gold |= {r["id"]: r for r in score_source(srcs[name], scorers)}
    index = {"metrics": versions(), "sources": {}}
    for name, rows in scored.items():
        src = srcs[name]
        doc = {"source": name, "title": src["title"], "family": src["family"], "kind": src["kind"],
               "from": src["from"], "n_poems": len(rows), "metrics": versions(),
               "summary": summarise(rows), "by_metre": by_metre(rows)}
        for key in src.get("group_by", []):
            doc[f"by_{key}"] = by_metre(rows, key)
        if name.startswith("human_evals_study2_"):
            doc["against_gold"] = against_gold(rows, gold)
        doc["poems"] = "@POEMS@"                   # one compact line per poem, the rest indented
        poems = ",\n".join("  " + json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows)
        text = json.dumps(doc, ensure_ascii=False, indent=1).replace('"@POEMS@"', "[\n" + poems + "\n ]")
        (OUT / f"{name}.json").write_text(text + "\n", encoding="utf-8")
        index["sources"][name] = {k: doc[k] for k in ("title", "family", "kind", "from", "n_poems", "summary")} | (
            {"against_gold": doc["against_gold"]} if "against_gold" in doc else {})
    if not args.only:
        (OUT / "summary.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        REPORT.write_text(report(index) + "\n", encoding="utf-8")
        print(f"wrote {OUT.relative_to(HERE)}/ ({len(scored)} sources + summary.json) and {REPORT.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
