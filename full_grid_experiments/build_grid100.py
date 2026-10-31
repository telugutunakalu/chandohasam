"""The 100-prompt grid (user decisions 2026-10-28, PLAN.md decisions 19–20): Bhāgavatam 50, Vemana 20, Kūcimañci 20,
Gemini 10, every prompt a poem of the human-evaluation pool, so each grid prompt has a human-rated poem on the same
bhāvam.

    ../.venv/bin/python build_grid100.py                    # select the 100; write the records and the reference runs
    ../.venv/bin/python build_grid100.py --approve          # after the user's review of prompts/grid100/p1/p1_review.md

- **Eligible:** a poem of ../human_evals/annotation_app/data/poems.json (the 500-poem pool) that is a held-out test
  record with an agreed metre and a bhāvam, not leaked into pretraining, and fits the MDLM canvas (prefix + 1.5 ×
  gold ≤ 512 tokens; e6_prompts' rule). The pool's textbook poems are out: their lines are in the training split.
- **Phase 1 first:** every eligible poem of phase 1 (the 100 being rated; data/active_pool.json) up to the quota:
  Bhāgavatam 10, Vemana 20, Kūcimañci 16, Gemini 10 of 20 (spread over their metres) = 56 rated poems.
- **The rest of the pool** fills the quota (Bhāgavatam 40, Kūcimañci 4) for the annotators' phase 2
  (phase2_candidates.json): split over the metres in proportion to the eligible poems (one per metre first when the
  quota allows; largest remainder); within a metre, poems of the earlier 183 first (their P1 is reviewed and the rows
  already run keep their poems), then a seeded draw.
- **Prompts:** P1 (prompts.py: Gemma-4 26B, the same instruction and checks, then the user's review) for every poem
  outside the 183; Gemini's own bhāvam as is (user decision). The Gemini records use the grid's prompt format
  unchanged (register ప్రాచీన, meaning_src "full_grid P1", as the other 90), so only the bhāvam text differs.

Writes prompts/grid100/: selection.json and selection.md, phase2_candidates.json, p1_todo.json (the poems that need
P1), records/test.jsonl (prompts/e6_p1's test records + the 10 Gemini records; with --approve, the new poems'
bhāvams replaced by their P1), links to val/train/leakage, and APPROVED (with --approve); and the reference runs
../diffusion_finetuning/runs/grid100_known_test (the prompts of the 183), grid100_new_test (the others) and
grid100_all_test (all 100, for the DAWG v2 cells).
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys
import time
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / "prompts" / "grid100"
E6P1 = HERE / "prompts" / "e6_p1"
E6 = REPO / "diffusion_finetuning" / "data" / "e6"
RUNS = REPO / "diffusion_finetuning" / "runs"
REFERENCE = RUNS / "e6_120m_t1_test"
HE = REPO / "human_evals" / "annotation_app" / "data"
GEMINI = REPO / "metrics" / "initial_evals" / "Outputs" / "chandas_dataset.json"
QUOTA = {"bhagavatam": 50, "vemana": 20, "kuchimanchi_timmakavi": 20, "gemini": 10}
HE_SOURCE = {"bhagavatam": "bhagavatam", "vemana": "vemana", "kuchimanchi": "kuchimanchi_timmakavi"}
SEED, CANVAS = 42, 512


def source_of(pid: str) -> str:
    return "gemini" if pid.startswith("gemini:") else pid.split(":")[0].split("/")[-1]


def proportional(counts: dict[str, int], total: int) -> dict[str, int]:
    """In proportion to each metre's poems (largest remainder); one per metre first when the total allows."""
    one = total >= len(counts)
    out = {m: int(one) for m in counts}
    base = {m: n - int(one) for m, n in counts.items()}
    rest = total - sum(out.values())
    share = {m: rest * e / max(1, sum(base.values())) for m, e in base.items()}
    for m in counts:
        out[m] += int(share[m])
    order = sorted(counts, key=lambda m: (-(share[m] - int(share[m])), -counts[m], m))
    for m in order[: total - sum(out.values())]:
        out[m] += 1
    assert all(out[m] <= counts[m] for m in counts), (out, counts)
    return out


def waterfill(counts: dict[str, int], total: int) -> dict[str, int]:
    """As even over the metres as their poems allow; ties go to the metres with more poems."""
    out = {m: 0 for m in counts}
    while sum(out.values()) < total:
        open_ = [m for m in counts if out[m] < counts[m]]
        if not open_:
            raise SystemExit(f"only {sum(counts.values())} poems for {total}")
        m = min(open_, key=lambda m: (out[m], -counts[m], m))
        out[m] += 1
    return out


def pick(ids: list[str], k: int, first: set[str], rng: random.Random) -> list[str]:
    """k of ids: those in ``first`` before the others (a seeded draw within each group)."""
    a = sorted(i for i in ids if i in first)
    b = sorted(i for i in ids if i not in first)
    return sorted(rng.sample(a, k) if len(a) >= k else a + rng.sample(b, k - len(a)))


class Fit:
    """Tokens by which a record's T1 prompt overflows the MDLM canvas (≤ 0: it fits)."""

    def __init__(self):
        sys.path.insert(0, str(REPO / "diffusion_finetuning"))
        from common import tokenizer
        from ft.canvas import Vocab
        self.v = Vocab(tokenizer())

    def __call__(self, r: dict) -> float:
        from ft.canvas import tokenise_record
        rec = tokenise_record(self.v, r)
        prefix = 1 + sum(len(p) for p in (rec.metre_head, rec.style_head, rec.samasya_head, rec.meaning_line,
                                          self.v.poem_head) if p is not None)
        return prefix + 1.5 * (sum(len(ln) for ln in rec.lines) + len(rec.lines)) - CANVAS


def gemini_records(phase1: dict) -> dict[str, dict]:
    """{id: E6-style record} of phase 1's Gemini poems."""
    gem = {x.get("id"): x for x in json.loads(GEMINI.read_text(encoding="utf-8"))["poems"]}
    out = {}
    for he_id, p in phase1.items():
        h = p["hidden"]
        if h["source_dataset"] != "generated":
            continue
        g = gem[h["source_id"]]
        b = p["bhavam"]
        assert b.get("source") == "generation_meaning", he_id          # Gemini's own bhāvam
        pid = f"gemini:{h['source_id']}"
        out[pid] = {"id": pid, "split": "test", "source": f"{GEMINI.relative_to(REPO)} (Gemini-generated)",
                    "kanda": "", "skandha": "", "register": "ప్రాచీన", "label": p["meter_te"], "status": "agree",
                    "meter": p["meter"], "meter_label": p["meter"], "meter_te": p["meter_te"], "layout": "raw",
                    "roundtrip": True, "lines": [unicodedata.normalize("NFC", ln).strip() for ln in g["lines"]],
                    "meaning": " ".join(unicodedata.normalize("NFC", b["te"]).split()), "meaning_src": "full_grid P1",
                    "meaning_p0": b["te"], "prompt_source": "Gemini's own bhāvam, as is (user decision 2026-10-28)",
                    "meaning_en": g.get("meaning_english"), "glosses": None, "samasya": None, "dataset": "gemini",
                    "human_eval_id": he_id, "author": h.get("author")}
    return out


def select() -> dict:
    ref = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(REFERENCE / "results.jsonl",
                                                                                 encoding="utf-8")})
    in183 = {pid for _, pid in ref}
    leak = json.loads((E6 / "leakage.json").read_text())
    seen = {k for k, x in leak["items"].items() if x["poem"]}
    test = {}
    for l in open(E6P1 / "records" / "test.jsonl", encoding="utf-8"):
        r = json.loads(l)
        test[r["id"]] = r
    active = set(json.loads((HE / "active_pool.json").read_text(encoding="utf-8"))["ids"])
    poems = {p["id"]: p for p in json.loads((HE / "poems.json").read_text(encoding="utf-8"))["poems"]}
    fit = Fit()
    rng = random.Random(SEED)
    chosen, why, he = {}, {}, {}

    eligible = {s: {"phase1": collections.defaultdict(list), "pool": collections.defaultdict(list)}
                for s in HE_SOURCE.values()}
    for he_id, p in sorted(poems.items()):
        h = p["hidden"]
        if h["source_dataset"] not in HE_SOURCE:
            continue
        src = HE_SOURCE[h["source_dataset"]]
        pid = f"dataset/{src}:{h['source_id']}"
        r = test.get(pid)
        if r is None or r["status"] != "agree" or not r.get("meaning") or pid in seen or fit(r) > 0:
            continue
        eligible[src]["phase1" if he_id in active else "pool"][r["meter"]].append(pid)
        he[pid] = he_id
    for src in ("bhagavatam", "vemana", "kuchimanchi_timmakavi"):
        for part in ("phase1", "pool"):
            left = QUOTA[src] - sum(source_of(p) == src for p in chosen)
            by = eligible[src][part]
            if left <= 0 or not by:
                continue
            n = sum(len(v) for v in by.values())
            quota = {m: len(v) for m, v in by.items()} if n <= left else proportional(
                {m: len(v) for m, v in by.items()}, left)
            for m in sorted(by):
                for pid in pick(by[m], quota[m], in183, rng):
                    chosen[pid] = m
                    why[pid] = ("phase 1" if part == "phase1" else "pool → phase 2") + \
                        (", the 183" if pid in in183 else ", new P1")

    phase1 = {i: poems[i] for i in sorted(active)}
    gem = gemini_records(phase1)                               # Gemini: phase 1's, spread over their metres
    by = collections.defaultdict(list)
    for pid, r in gem.items():
        if fit(r) <= 0:
            by[r["meter"]].append(pid)
    quota = waterfill({m: len(v) for m, v in by.items()}, QUOTA["gemini"])
    for m in sorted(by):
        for pid in pick(by[m], quota[m], set(), rng):
            chosen[pid], why[pid] = m, "phase 1, Gemini bhāvam as is"
            he[pid] = gem[pid]["human_eval_id"]

    counts = collections.Counter(source_of(p) for p in chosen)
    assert counts == collections.Counter(QUOTA), counts
    return {"chosen": chosen, "why": why, "gemini": {p: gem[p] for p in chosen if p in gem}, "test": test,
            "human_eval": {p: he[p] for p in chosen}, "in183": in183}


def write_reference(name: str, pairs: list[tuple[str, str]], note: str) -> None:
    run = json.loads((REFERENCE / "run.json").read_text(encoding="utf-8"))
    ids = {pid for _, pid in pairs}
    run.update(name=name, topics={k: v for k, v in run.get("topics", {}).items() if k in ids},
               grid100=note, created=time.strftime("%Y-%m-%d %H:%M"))
    d = RUNS / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "run.json").write_text(json.dumps(run, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(d / "results.jsonl", "w", encoding="utf-8") as fh:      # the pairs only (meter, topic) as a run's rows
        for m, pid in sorted(pairs):
            fh.write(json.dumps({"meter": m, "topic": pid, "mode": "reference", "seed": SEED},
                                ensure_ascii=False) + "\n")


def write_records(sel: dict, p1: dict[str, str]) -> None:
    (OUT / "records").mkdir(parents=True, exist_ok=True)
    tmp = OUT / "records" / "test.jsonl.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for l in open(E6P1 / "records" / "test.jsonl", encoding="utf-8"):
            r = json.loads(l)
            if r["id"] in p1:
                r = {**r, "meaning": " ".join(p1[r["id"]].split()), "meaning_p0": r["meaning"],
                     "meaning_src": "full_grid P1"}
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        for r in sel["gemini"].values():
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, OUT / "records" / "test.jsonl")
    for name, target in (("records/val.jsonl", E6 / "records" / "val.jsonl"),
                         ("records/train.jsonl", E6 / "records" / "train.jsonl"),
                         ("leakage.json", E6 / "leakage.json")):
        link = OUT / name
        if not link.exists():
            os.symlink(os.path.relpath(target, link.parent), link)


def summary_md(sel: dict) -> str:
    chosen, why = sel["chosen"], sel["why"]
    srcs = ["bhagavatam", "vemana", "kuchimanchi_timmakavi", "gemini"]
    metres = sorted({m for m in chosen.values()}, key=lambda m: -sum(v == m for v in chosen.values()))
    rated = [p for p in chosen if not why[p].startswith("pool")]
    cell = lambda ps: f"{len(ps)}" + (f" ({sum(not why[p].startswith('pool') for p in ps)})" if ps else "")  # noqa: E731
    md = ["# The 100-prompt grid: selection", "",
          f"Built {time.strftime('%Y-%m-%d %H:%M')} by build_grid100.py (rules in its docstring). Every prompt is a poem "
          f"of the human-evaluation pool: **{len(rated)} are phase-1 poems** (rated now), {len(chosen) - len(rated)} "
          f"are to be rated in a phase 2 (phase2_candidates.json). {sum(p in sel['in183'] for p in chosen)} prompts "
          f"are from the earlier 183 (P1 reviewed); {sum(p not in sel['in183'] and p not in sel['gemini'] for p in chosen)} "
          f"need P1 and review; {len(sel['gemini'])} are Gemini bhāvams as is.", "",
          "Cells: prompts (of them, phase 1).", "",
          "| metre | " + " | ".join(srcs) + " | total |", "|---|" + "---|" * (len(srcs) + 1)]
    for m in metres:
        row = [[p for p in chosen if chosen[p] == m and source_of(p) == s] for s in srcs]
        md.append(f"| {m} | " + " | ".join(cell(ps) if ps else "" for ps in row) + f" | {sum(map(len, row))} |")
    md.append("| **total** | " + " | ".join(cell([p for p in chosen if source_of(p) == s]) for s in srcs) +
              f" | {cell(list(chosen))} |")
    new = sorted(p for p in chosen if p not in sel["in183"])
    md += ["", f"## The {len(new)} prompts outside the 183", ""]
    for pid in new:
        r = sel["gemini"].get(pid) or sel["test"][pid]
        md += [f"### {pid} · {chosen[pid]} · {why[pid]} · human eval {sel['human_eval'].get(pid, '–')}", "",
               "> " + "  \n> ".join(r["lines"]), "",
               f"bhāvam{' (the prompt)' if pid in sel['gemini'] else ' (edition; P1 to come)'}: {r['meaning']}", ""]
    return "\n".join(md) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--approve", action="store_true", help="the user approved the Vemana P1 prompts: use them")
    ap.add_argument("--allow-flagged", action="store_true")
    args = ap.parse_args()
    sel = select()
    chosen, why = sel["chosen"], sel["why"]
    new = sorted(p for p in chosen if p not in sel["in183"])
    vemana_new = [p for p in new if p not in sel["gemini"]]               # every new poem that needs P1
    p1 = {}
    if args.approve:
        rows = {r["id"]: r for r in map(json.loads, open(OUT / "p1" / "p1.jsonl", encoding="utf-8"))}
        edits_path = OUT / "p1_edits.jsonl"
        edits = ({e["id"]: e["p1"] for e in map(json.loads, open(edits_path, encoding="utf-8"))}
                 if edits_path.exists() else {})
        missing = [p for p in vemana_new if p not in rows and p not in edits]
        if missing:
            raise SystemExit(f"no P1 prompt for {len(missing)} poems: {missing}")
        flagged = [p for p in vemana_new if p not in edits and not rows[p]["result"]["passed"]]
        if flagged and not args.allow_flagged:
            raise SystemExit(f"{len(flagged)} prompts still flagged ({flagged}): edit them in {edits_path.name}, "
                             "or --allow-flagged")
        p1 = {p: edits.get(p, rows.get(p, {}).get("p1")) for p in vemana_new}
    OUT.mkdir(parents=True, exist_ok=True)
    write_records(sel, p1)
    known = [(m, p) for p, m in chosen.items() if p in sel["in183"]]
    write_reference("grid100_known_test", known, f"the {len(known)} prompts of the 183 (build_grid100.py)")
    write_reference("grid100_new_test", [(chosen[p], p) for p in new],
                    f"the {len(new)} new prompts: {len(vemana_new)} with P1 + {len(sel['gemini'])} Gemini "
                    "(bhāvam as is) (build_grid100.py)")
    write_reference("grid100_all_test", [(m, p) for p, m in chosen.items()],
                    "all 100 prompts: the DAWG v2 A+B cells (build_grid100.py)")
    phase2 = sorted(p for p in chosen if why[p].startswith("pool"))
    (OUT / "phase2_candidates.json").write_text(json.dumps(
        {"note": "grid prompts outside human-eval phase 1: to be rated in a phase 2 (user decision 2026-10-28), so "
                 "every grid prompt has a human-rated poem", "count": len(phase2),
         "poems": [{"eval_id": sel["human_eval"][p], "id": p, "metre": chosen[p]} for p in phase2]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT / "p1_todo.json").write_text(json.dumps(vemana_new, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT / "selection.json").write_text(json.dumps(
        {"created": time.strftime("%Y-%m-%d %H:%M"), "quota": QUOTA, "seed": SEED,
         "prompts": [{"id": p, "metre": chosen[p], "source": source_of(p), "from": why[p],
                      "human_eval_id": sel["human_eval"].get(p)} for p in sorted(chosen)]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (OUT / "selection.md").write_text(summary_md(sel), encoding="utf-8")
    if args.approve:
        kept = sum(p not in edits and not rows[p]["result"]["passed"] for p in vemana_new)
        (OUT / "APPROVED").write_text(f"{time.strftime('%Y-%m-%d %H:%M')}: the {len(vemana_new)} P1 prompts approved "
                                      f"(build_grid100.py --approve; {len(edits)} hand-edited, {kept} kept with a "
                                      "failed check)\n", encoding="utf-8")
    print(f"100 prompts: {len(known)} from the 183, {len(new)} new ({len(vemana_new)} with P1, "
          f"{len(sel['gemini'])} Gemini); phase 1 {sum(not why[p].startswith('pool') for p in chosen)}, phase 2 "
          f"{len(phase2)}; records → {OUT / 'records'}; P1 {'applied' if p1 else 'pending'}", flush=True)


if __name__ == "__main__":
    main()
