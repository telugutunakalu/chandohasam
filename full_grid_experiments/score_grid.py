"""The grid's table (PLAN.md §5): every cell on disk scored the same way, with paired tests.

    ../.venv/bin/python -u score_grid.py            # → results/grid.{md,json}, results/grid_poems.jsonl (numbers)
    ../.venv/bin/python -u score_grid.py --out /tmp/rescore && diff -r /tmp/rescore results   # a reproduction check

- **Scorer:** ../RL/reward.py's (as ../lora_gemma_diffusion/score_e6.py): whole poem in metre (strict engines), chandas
  skill, vṛtta lines on the gold pattern, one-akshara words, copy from the prompt, recognition (raw: the own prompt
  first among it and 9 others; a topic signal, not meaning), repeated lines, a line copied from the training split.
  Records from prompts/grid100/records, so the prompt is P1 (Gemini: its own bhāvam); the recognition's 9 others are
  other prompts of the same metre from a fixed pool: the 183 earlier prompts and the grid's 100 (so the pool does not
  shrink with the 100).
- **Words:** real words with ఁ stripped on both sides (poems and training lexicon), for every model.
- **Gold copy:** the longest akshara run shared with the poem's own gold poem; ≥ 12 counts as copied (the
  memorisation measure's threshold; the Google models may have read these poems on the web).
- **The 100 prompts** (build_grid100.py, prompts/grid100/selection.json): a row's poems are its core cell's poems on
  them (rows run on the 183 keep their 34) and its `new` cell's (the 66 new prompts), once that has run.
- **DAWG v2 A+B** (grid.py's v2 cells): every row's constrained cell again with Layer A and Layer B, scored as
  `masking_backtrack_v2`, tested against the row's v1 constrained cell, and shown poem by poem on three fixed prompts
  (one per source family) in results/grid_v2_samples.md.
- **Gold layout** (fixed 2026-10-30): dataset/ writes each pāda of a metre with two halves per line (sīsa, mānini,
  layagrāhi, layavibhāti) as two lines, and evaluate() keeps the metre's first n lines, so 5 golds were scored on
  their first half-lines read as pādas (all out of metre). Their halves are now joined into pādas, the layout the
  models write (`padas`); a sīsa's closing gīti stays beyond the 4 lines scored, as for the models. The 2
  madhuragati golds (2 units) are scored on their first unit, the length the models were asked for.
- **Paired tests** over the 100 prompts (a prompt's value = the mean of its poems): each fine-tuned row against its base
  and each row's constrained cell against its free cell, by bootstrap (10,000 resamples: the difference, its 95%
  interval, a two-sided p); in-metre also by McNemar's exact test on the seed-42 poems.
"""
from __future__ import annotations

import ast
import collections
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
os.environ.setdefault("E6_RECORDS_DIR", str(HERE / "prompts" / "grid100" / "records"))
sys.path.insert(0, str(REPO / "RL"))
sys.path.insert(0, str(REPO / "lora_gemma_diffusion"))
import reward as rw                                                  # noqa: E402
import rlcommon as rc                                                # noqa: E402
from score_e6 import stripped_matcher, words_stripped                # noqa: E402
import grid as G                                                     # noqa: E402
from prompts import aksharas, longest_run                            # noqa: E402
from indic_meter_dawg import default_dawg                            # noqa: E402
from metrical_decoder.evaluate import extract_poem                   # noqa: E402
from metrical_decoder.prompts import n_lines                         # noqa: E402

MEASURES = ("all", "skill", "line_gana", "words_s", "filler", "copy", "meaning", "repeated", "training_line",
            "gold_copy")
TESTED = ("all", "skill", "words_s", "meaning", "copy")
GOLD_RUN = 12
SOURCES = HERE / "prompts" / "p1.jsonl"                             # the 183 earlier prompts
SELECTION = HERE / "prompts" / "grid100" / "selection.json"          # the 100
OUT = HERE / "results"


def cell_rows(path: Path, modes: list[str], ids: set[str]) -> list[dict]:
    out = []
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if r["mode"] not in modes or r.get("seed", 42) != 42:      # seed 42 only: the rows done before 2026-10-28
            continue                                               # also hold a seed-43 free sample
        if r["topic"] not in ids:                                  # the 100 (rows run on the 183 keep their 34)
            continue
        ev = r.get("eval") or {}
        ev = ast.literal_eval(ev) if isinstance(ev, str) else ev
        out.append({"prompt_id": r["topic"], "meter": r["meter"], "mode": r["mode"], "seed": r.get("seed"),
                    "text": "\n".join(ev.get("lines") or [])})
    return out


def padas(lines: list[str], meter: str) -> list[str]:
    """A gold poem with one pāda per line: halves written as two lines are joined (see the docstring)."""
    lines, n = extract_poem("\n".join(lines)), n_lines(meter)
    if default_dawg().spec(meter).halves_per_line == 2 and len(lines) >= 2 * n:
        return [f"{lines[2 * i]} {lines[2 * i + 1]}" for i in range(n)] + lines[2 * n:]
    return lines


def summary(rows: list[dict]) -> dict:
    def mean(k):
        v = [float(r[k]) for r in rows if r.get(k) is not None]
        return float(np.mean(v)) if v else None
    sk = [r["skill"] for r in rows if r.get("skill") is not None]
    return {"poems": len(rows), "prompts": len({r["prompt_id"] for r in rows}),
            **{k: mean(k) for k in MEASURES if k != "skill"},
            "skill_mean": float(np.mean(sk)) if sk else None, "skill_median": float(np.median(sk)) if sk else None,
            "n_lines": mean("n_lines")}


def per_prompt(rows: list[dict], k: str) -> dict:
    by = collections.defaultdict(list)
    for r in rows:
        if r.get(k) is not None:
            by[r["prompt_id"]].append(float(r[k]))
    return {p: float(np.mean(v)) for p, v in by.items()}


def bootstrap(a: dict, b: dict, n: int = 10_000, seed: int = 7) -> dict | None:
    keys = sorted(set(a) & set(b))
    if len(keys) < 10:
        return None
    d = np.array([b[k] - a[k] for k in keys])
    rng = np.random.default_rng(seed)
    boot = d[rng.integers(0, len(d), (n, len(d)))].mean(1)
    p = min(1.0, 2 * min((boot <= 0).mean(), (boot >= 0).mean()))
    return {"n": len(keys), "diff": float(d.mean()), "lo": float(np.percentile(boot, 2.5)),
            "hi": float(np.percentile(boot, 97.5)), "p": float(p)}


def mcnemar(a: list[dict], b: list[dict]) -> dict | None:
    """Exact McNemar on the seed-42 poems' in-metre verdicts, paired by prompt."""
    x = {r["prompt_id"]: bool(r["all"]) for r in a if r.get("seed") in (42, None)}
    y = {r["prompt_id"]: bool(r["all"]) for r in b if r.get("seed") in (42, None)}
    keys = set(x) & set(y)
    if not keys:
        return None
    up, down = sum(y[k] and not x[k] for k in keys), sum(x[k] and not y[k] for k in keys)
    n = up + down
    p = min(1.0, 2 * sum(math.comb(n, i) for i in range(min(up, down) + 1)) / 2 ** n) if n else 1.0
    return {"pairs": len(keys), "b_only": up, "a_only": down, "p": p}


def compare(a: list[dict], b: list[dict]) -> dict:
    out = {k: bootstrap(per_prompt(a, k), per_prompt(b, k)) for k in TESTED}
    out["mcnemar_all"] = mcnemar(a, b)
    return out


def main(argv=None) -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Score every grid cell on disk.")
    ap.add_argument("--out", type=Path, default=OUT,
                    help="write elsewhere, e.g. to check that a rescore reproduces results/ (diff -r)")
    args = ap.parse_args(argv)
    rw.COPY_MEANING = 1.01          # raw recognition (the reward withholds it above 10% copy); copy is its own column
    s = rw.Scorer("test")
    grid = [p["id"] for p in json.loads(SELECTION.read_text(encoding="utf-8"))["prompts"]]
    ids = set(grid)
    sources = {json.loads(l)["id"] for l in open(SOURCES, encoding="utf-8")} | ids     # the recognition pool
    s.recs = {k: v for k, v in s.recs.items() if k in sources}
    assert ids <= set(s.recs), sorted(ids - set(s.recs))
    s.by_metre = collections.defaultdict(list)
    for pid, r in s.recs.items():
        s.by_metre[rc.metre_key(r.get("meter"))].append(pid)
    m = stripped_matcher()
    gold_ak = {pid: aksharas("\n".join(r["lines"])) for pid, r in s.recs.items()}

    def score(rows):
        scored = s.score(rows)
        for r in scored:
            r["words_s"] = words_stripped(m, r["lines"])
            r["gold_run"] = longest_run(aksharas("\n".join(r["lines"])), gold_ak[r["prompt_id"]])
            r["gold_copy"] = r["gold_run"] >= GOLD_RUN
        return scored

    gold = [{"prompt_id": pid, "meter": rc.metre_key(r["meter"]), "mode": "gold", "seed": None,
             "text": "\n".join(padas(r["lines"], rc.metre_key(r["meter"])))} for pid, r in s.recs.items() if pid in ids]
    cells = {"gold": {"label": "gold (the source poems)", "rows": score(gold)}}
    for kind in ("core", "extra"):
        for row, c in G.cells(kind):
            _, _, path = G.command(row, c)
            if not G.done(path):
                continue
            modes = G.CELLS[c][0]
            _, _, new = G.command(row, c, new=True)
            for mode in modes:
                rows = cell_rows(path, [mode], ids)
                if kind == "core" and G.done(new):
                    rows += cell_rows(new, [mode], ids)
                if rows:
                    key = f"{row.key}|{mode}"
                    cells[key] = {"label": f"{row.model} · {row.state} · {mode}", "row": row.key, "mode": mode,
                                  "rows": score(rows)}
                    print(f"{key}: {len(rows)} poems", flush=True)
    for row, c in G.cells("v2"):
        _, _, path = G.command(row, c, v2=True)
        rows = cell_rows(path, ["masking_backtrack"], ids) if G.done(path) else []
        if rows:
            key = f"{row.key}|masking_backtrack_v2"
            cells[key] = {"label": f"{row.model} · {row.state} · masking_backtrack · v2 A+B", "row": row.key,
                          "mode": "masking_backtrack_v2", "rows": score(rows)}
            print(f"{key}: {len(rows)} poems", flush=True)
    res = {k: {"label": v["label"], **summary(v["rows"])} for k, v in cells.items()}

    tests = {}
    bases = {"nandi_ft": "nandi_base", "t5_270m_ft": "t5_270m_base", "t5_1b_ft": "t5_1b_base",
             "t5_4b_ft": "t5_4b_base", "t5_4b_48k": "t5_4b_base", "mdlm120m_ft": "mdlm120m_base",
             "mdlm523m_ft": "mdlm523m_base", "dg_full": "dg_base"}
    for ft, base in bases.items():
        for mode in ("baseline", "masking_backtrack"):
            a, b = cells.get(f"{base}|{mode}"), cells.get(f"{ft}|{mode}")
            if a and b:
                tests[f"{ft} vs {base} ({mode})"] = compare(a["rows"], b["rows"])
    for row in G.ROWS:
        a, b = cells.get(f"{row.key}|baseline"), cells.get(f"{row.key}|masking_backtrack")
        if a and b:
            tests[f"{row.key}: constrained vs free"] = compare(a["rows"], b["rows"])
    for row in G.ROWS:
        a, b = cells.get(f"{row.key}|masking_backtrack"), cells.get(f"{row.key}|masking_backtrack_v2")
        if a and b:
            tests[f"{row.key}: v2 A+B vs v1 (constrained)"] = compare(a["rows"], b["rows"])

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    out.mkdir(exist_ok=True)
    (out / "grid.json").write_text(json.dumps({"cells": res, "tests": tests}, ensure_ascii=False, indent=1) + "\n",
                                   encoding="utf-8")
    with open(out / "grid_poems.jsonl", "w", encoding="utf-8") as fh:
        for key, v in cells.items():
            for r in v["rows"]:
                fh.write(json.dumps({"cell": key, "prompt_id": r["prompt_id"], "seed": r.get("seed"),
                                     **{k: r.get(k) for k in MEASURES + ("gold_run", "n_lines")}},
                                    ensure_ascii=False, default=float) + "\n")
    p = lambda x, pct=True: "–" if x is None else (f"{100 * x:.1f}" if pct else f"{x:.2f}")
    md = ["# Full grid: every model on the 100 prompts (Bhāgavatam 50, Vemana 20, Kūcimañci 20, Gemini 10)", "",
          "Scored by ../RL/reward.py (the RL report's definitions). Real words with ఁ stripped on both sides. Recognition "
          "(raw) is a topic signal, not meaning. Gold copy: a run of ≥ 12 aksharas shared with the poem's own gold poem. "
          "One poem per prompt in every cell (seed 42; the seed-43 free poems of the rows done before 2026-10-28 are kept "
          "on disk, not scored).", "",
          "| cell | poems | in metre % | skill mean / median | vṛtta lines on pattern % | real words % | one-akshara % "
          "| copy % | recognised % | repeating a line % | training line % | gold copy % | lines |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in res.items():
        md.append(f"| {v['label']} | {v['poems']} | {p(v['all'])} | {p(v['skill_mean'], False)} / "
                  f"{p(v['skill_median'], False)} | {p(v['line_gana'])} | {p(v['words_s'])} | {p(v['filler'])} | "
                  f"{p(v['copy'])} | {p(v['meaning'])} | {p(v['repeated'])} | {p(v['training_line'])} | "
                  f"{p(v['gold_copy'])} | {p(v['n_lines'], False)} |")
    md += ["", "## Paired tests (per-prompt means; bootstrap 95% interval and p; in-metre also McNemar on seed 42)", "",
           "| comparison | in metre Δ pts [95%] p | skill Δ [95%] p | real words Δ pts p | recognised Δ pts p "
           "| copy Δ pts p | McNemar in metre (B only / A only, p) |", "|---|---|---|---|---|---|---|"]

    def f(t, pct=True):
        if not t:
            return "–"
        s_ = 100 if pct else 1
        return f"{s_ * t['diff']:+.1f} [{s_ * t['lo']:+.1f}, {s_ * t['hi']:+.1f}] p {t['p']:.3f}" if pct else \
            f"{t['diff']:+.2f} [{t['lo']:+.2f}, {t['hi']:+.2f}] p {t['p']:.3f}"
    for name, t in tests.items():
        mc = t["mcnemar_all"]
        mcs = "–" if not mc else f"{mc['b_only']} / {mc['a_only']}, p {mc['p']:.3f}"
        md.append(f"| {name} | {f(t['all'])} | {f(t['skill'], False)} | {f(t['words_s'])} | {f(t['meaning'])} | "
                  f"{f(t['copy'])} | {mcs} |")
    (out / "grid.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)
    if any(k.endswith("|masking_backtrack_v2") for k in cells):
        (out / "grid_v2_samples.md").write_text(v2_samples(cells, s.recs, grid), encoding="utf-8")


def v2_samples(cells: dict, recs: dict, grid: list[str]) -> str:
    """Three fixed prompts (a Bhāgavatam vṛtta, a Vemana poem, a Gemini poem; seeded), every row's v1 and v2 poem."""
    import random
    rng = random.Random(42)
    pick = []
    for want in (lambda p: p.startswith("dataset/bhagavatam") and rc.metre_key(recs[p]["meter"]) in rw.VRTTA,
                 lambda p: p.startswith("dataset/vemana"), lambda p: p.startswith("gemini:")):
        pool = sorted(p for p in grid if want(p))
        if pool:
            pick.append(rng.choice(pool))
    md = ["# DAWG v2 A+B against v1: the same prompts, poem by poem", "",
          "Masking + backtracking, seed 42. v1: the grid's constrained cell; v2: Layer A (padyarchana syllable inventory) "
          "+ Layer B (padyarchana words, weight 2 at every step). Under each poem: in metre (strict), real words, "
          "one-akshara words, recognised. The table of all 100 prompts and the paired tests: grid.md.", ""]
    for pid in pick:
        r = recs[pid]
        md += [f"## {pid} · {r['meter']}", "", f"**Prompt (bhāvam):** {' '.join(r['meaning'].split())}", "",
               "**Gold:**", "", "```", *r["lines"], "```", ""]
        for row in G.ROWS:
            for dec, key in (("v1", f"{row.key}|masking_backtrack"), ("v2 A+B", f"{row.key}|masking_backtrack_v2")):
                c = cells.get(key)
                x = next((x for x in c["rows"] if x["prompt_id"] == pid), None) if c else None
                if x is None:
                    continue
                pct = lambda k: "–" if x.get(k) is None else f"{100 * float(x[k]):.0f}%"      # noqa: E731
                md += [f"**{row.model} · {row.state} · {dec}** — in metre {'yes' if x.get('all') else 'no'}, real words "
                       f"{pct('words_s')}, one-akshara {pct('filler')}, recognised {'yes' if x.get('meaning') else 'no'}",
                       "", "```", *(x.get("lines") or []), "```", ""]
    return "\n".join(md) + "\n"


if __name__ == "__main__":
    main()
