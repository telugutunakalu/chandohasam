#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Study 2's pool: poems of the three best fine-tuned grid models, rated against the poets' study-1 scores.

    ../../.venv/bin/python -u build_study2_pool.py
        → ../human_eval_poems_study2.json, data_study2/bhavam_overrides.json, reports/study2/selection.{md,json}
    ../../.venv/bin/python build_data.py --pool-file ../human_eval_poems_study2.json --out data_study2 \
        --overrides data_study2/bhavam_overrides.json

The user's design (2026-10-30): the AI poems only (the gold poems are not shown again: they keep their study-1
ratings); three fine-tuned models with the v2 controller, every one on the same prompts; about 100 poems; prompts
chosen by "a mix of best-rated gold per source and closest AI poems":

- **Eligible:** a grid prompt whose source is a poet (not Gemini) and whose gold poem (its he_ poem of the pool) has
  ≥ MIN_RATERS complete study-1 ratings of Q1–Q4 and Q10; each model's poem non-empty, in metre (strict), with no
  repeated line and no GOLD_RUN-akshara run of its gold.
- **Gold score:** the gold's mean over its study-1 ratings of (the mean of Q1–Q4, Q10 − that annotator's mean of the
  same over all their ratings). The study-1 database is opened read-only.
- **AI score:** the mean over the three models' poems of p(real), out of fold, by the method of
  ../../final_report_metrics/separability.py (its 15 features with word resolution read without the table; fitted
  per model on its 100 grid poems against the 90 human golds; 10 prompt-grouped folds × 5 repeats).
- **Score** = z(gold) + z(AI), each z within the source; the top QUOTA per source.
- **Ids:** he2_0001… over the poems in a shuffled order (seed SEED), so an id shows neither the model nor the prompt.
- **Shown bhāvam:** the grid prompt (the P1 retelling, Telugu only), the text the models wrote from.
- **hidden.source_dataset** is the model: the app stratifies its calibration set on it, and the admin page's
  per-source panel then reads per model. The poem's own source and every score are in hidden.metadata.

Half of the score is the AI poems' closeness to real verse, so study 2 rates the models on prompts where they did
comparatively well: report its numbers as near-best-case, not typical.
"""
from __future__ import annotations

import json
import random
import sqlite3
import statistics as st
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "final_report_metrics"))
import separability as S                                             # noqa: E402

DB = HERE / "instance" / "annotations.db"
POOL1 = HERE.parent / "human_eval_poems_strict.json"
SELECTION = REPO / "full_grid_experiments" / "prompts" / "grid100" / "selection.json"
RECORDS = REPO / "full_grid_experiments" / "prompts" / "grid100" / "records"
POEMS = REPO / "final_report_metrics" / "results" / "poems_all_metrics.jsonl"
OUT_POOL = HERE.parent / "human_eval_poems_study2.json"
OUT_DATA = HERE / "data_study2"
OUT_REPORT = HERE / "reports" / "study2"

MODELS = {"mdlm523m_ft": "Chandohasam MDLM-523M SFT", "t5_1b_ft": "T5Gemma 2 1B SFT", "nandi_ft": "Nandi-Mini-150M SFT"}
MODE = "masking_backtrack_v2"
LIKERT = ("readability", "comprehension", "lexical", "bhavam", "poetic")
MIN_RATERS, GOLD_RUN, SEED = 4, 12, 20261030
QUOTA = {"bhagavatam": 10, "vemana": 12, "kuchimanchi_timmakavi": 11}
TABLE_FREE = tuple(f for f in S.FEATURES if not f.startswith("wr_")) + (
    "wr_resolved_live", "wr_resolved_live_strict", "wr_resolved_live_verified")


def gold_scores() -> dict[str, tuple[float, int]]:
    """he_ id → (annotator-centred mean of the five 1–5 scales, raters)."""
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    rows = con.execute("SELECT annotator_id, eval_id, answers FROM annotations").fetchall()
    con.close()
    per, own = defaultdict(list), defaultdict(list)
    for ann, eid, answers in rows:
        vals = [json.loads(answers).get(q) for q in LIKERT]
        if all(isinstance(v, (int, float)) for v in vals):
            per[eid].append((ann, st.mean(vals)))
            own[ann].append(st.mean(vals))
    centre = {a: st.mean(v) for a, v in own.items()}
    return {e: (st.mean(v - centre[a] for a, v in r), len(r)) for e, r in per.items()}


def p_real(poems: list[dict]) -> dict[tuple[str, str], float]:
    """(row, prompt) → out-of-fold p(real) of the model's poem against the 90 human golds."""
    real = S.complete([p for p in poems if p["cell"] == "gold" and p["prompt_id"].startswith("dataset/")])
    out = {}
    for row in MODELS:
        gen = S.complete([p for p in poems if p["cell"] == f"{row}|{MODE}"])
        _, score = S.oof(real, gen, TABLE_FREE)
        out.update({(row, p["prompt_id"]): float(s) for p, s in zip(gen, score[len(real):])})
    return out


def z(xs: dict) -> dict:
    m, sd = st.mean(xs.values()), st.pstdev(xs.values()) or 1.0
    return {k: (v - m) / sd for k, v in xs.items()}


def main() -> None:
    sel = json.loads(SELECTION.read_text(encoding="utf-8"))["prompts"]
    pool1 = {p["eval_id"]: p for p in json.loads(POOL1.read_text(encoding="utf-8"))["poems"]}
    meaning = {}
    for f in RECORDS.glob("*.jsonl"):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            meaning[r["id"]] = r["meaning"]
    poems = [json.loads(line) for line in open(POEMS, encoding="utf-8")]
    by = {(p["row"], p["prompt_id"]): p for p in poems if p["set"] == "grid" and p.get("mode") == MODE}
    gold = gold_scores()
    pr = p_real(poems)

    cands, excluded = [], Counter()
    for s in sel:
        if s["source"] == "gemini":
            continue
        g, n = gold.get(s["human_eval_id"], (None, 0))
        if n < MIN_RATERS:
            excluded["gold rated by fewer than 4"] += 1
            continue
        ai = {row: by.get((row, s["id"])) for row in MODELS}
        bad = [row for row, p in ai.items() if not p or not p["lines"] or not p.get("grid_all")
               or p.get("grid_repeated") or (p.get("grid_gold_run") or 0) >= GOLD_RUN or (row, s["id"]) not in pr]
        if bad:
            excluded["a model poem out of metre, repeating a line, copying or empty"] += 1
            continue
        cands.append({"prompt_id": s["id"], "source": s["source"], "meter": s["metre"], "gold_eval_id": s["human_eval_id"],
                      "gold_score": g, "gold_raters": n, "p_real": {row: pr[(row, s["id"])] for row in MODELS},
                      "ai_score": st.mean(pr[(row, s["id"])] for row in MODELS)})
    chosen = []
    for src, k in QUOTA.items():
        group = [c for c in cands if c["source"] == src]
        zg = z({c["prompt_id"]: c["gold_score"] for c in group})
        za = z({c["prompt_id"]: c["ai_score"] for c in group})
        for c in group:
            c["z_gold"], c["z_ai"] = zg[c["prompt_id"]], za[c["prompt_id"]]
            c["score"] = c["z_gold"] + c["z_ai"]
        group.sort(key=lambda c: (-c["score"], c["prompt_id"]))
        for i, c in enumerate(group):
            c["chosen"] = i < k
        chosen += [c for c in group if c["chosen"]]

    items = [(c, row) for c in chosen for row in MODELS]
    random.Random(SEED).shuffle(items)
    pool, overrides = [], {}
    for i, (c, row) in enumerate(items, 1):
        eid = f"he2_{i:04d}"
        p, g = by[(row, c["prompt_id"])], pool1[c["gold_eval_id"]]
        assert p["meter"] == g["meter_id"], (eid, p["meter"], g["meter_id"])
        pool.append({"eval_id": eid, "source_dataset": row, "source_id": c["prompt_id"], "meter_id": g["meter_id"],
                     "meter_te": g["meter_te"], "meter_label_source": "grid_prompt", "declared_meter": g["meter_id"],
                     "strictest_profile": "strict", "author": f"{MODELS[row]} · v2 controller",
                     "line_count": len(p["lines"]), "lines": p["lines"],
                     "metadata": {"model": row, "cell": f"{row}|{MODE}", "prompt_id": c["prompt_id"],
                                  "gold_source": c["source"], "gold_eval_id": c["gold_eval_id"],
                                  "gold_score": round(c["gold_score"], 4), "p_real": round(c["p_real"][row], 4),
                                  "selection_score": round(c["score"], 4)},
                     "ratings": {}})
        overrides[eid] = {"te": " ".join(meaning[c["prompt_id"]].split()), "en": None, "source": "grid_p1"}

    OUT_POOL.write_text(json.dumps({
        "dataset": "chandohasam_study2", "description": __doc__.strip().split("\n\n")[0],
        "compliance_profile": "strict", "generated_on": date.today().isoformat(), "sampling_seed": SEED,
        "target_size": len(pool), "actual_size": len(pool), "models": MODELS, "quota": QUOTA, "poems": pool},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    OUT_DATA.mkdir(exist_ok=True)
    (OUT_DATA / "bhavam_overrides.json").write_text(json.dumps(overrides, ensure_ascii=False, indent=1) + "\n",
                                                   encoding="utf-8")
    OUT_REPORT.mkdir(parents=True, exist_ok=True)
    (OUT_REPORT / "selection.json").write_text(json.dumps({"candidates": cands, "excluded": excluded},
                                                          ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    md = ["# Study 2: prompt selection", "", f"Method: build_study2_pool.py. {len(cands)} eligible prompts; excluded: "
          + "; ".join(f"{k} {v}" for k, v in excluded.items()) + f". Chosen {len(chosen)} prompts × {len(MODELS)} "
          f"models = {len(pool)} poems.", "",
          "| chosen | source | metre | gold (he_) | raters | gold score | " + " | ".join(f"p(real) {r}" for r in MODELS)
          + " | z gold | z AI | score |", "|---|---|---|---|---|---|" + "---|" * len(MODELS) + "---|---|---|"]
    for c in sorted(cands, key=lambda c: (c["source"], -c["score"])):
        md.append(f"| {'✔' if c['chosen'] else ''} | {c['source']} | {c['meter']} | {c['gold_eval_id']} | "
                  f"{c['gold_raters']} | {c['gold_score']:+.2f} | "
                  + " | ".join(f"{c['p_real'][r]:.2f}" for r in MODELS)
                  + f" | {c['z_gold']:+.2f} | {c['z_ai']:+.2f} | {c['score']:+.2f} |")
    (OUT_REPORT / "selection.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:3]))
    print(Counter(c["source"] for c in chosen), Counter(c["meter"] for c in chosen).most_common())


if __name__ == "__main__":
    main()
