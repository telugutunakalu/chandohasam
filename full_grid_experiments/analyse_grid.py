"""Checks and breakdowns of the scored grid, independent of score_grid.py's aggregation (README "Checks").

    ../.venv/bin/python analyse_grid.py         # → results/analysis.md and analysis.json (≈ 10 s, CPU)

Reads the per-poem scores (results/grid_poems.jsonl), the raw cell files (grid.py's paths, as score_grid.py) and the
prompt selection (prompts/grid100/selection.json); writes numbers only.

1. **The prompts:** sources, how each was obtained (the earlier 183 or new; P1 or Gemini's own bhāvam), human-eval
   membership, metres, and which are among the 7 common vṛttas whose line pattern the scorer checks (../RL/reward.py
   VRTTA: utpalamāla, campakamāla, mattebha, śārdūla, mattakōkila, mālini, bhujaṅgaprayāta).
2. **Integrity of every cell:** poems on the 100 (34 for the extra strategies), prompts missing or duplicated, seeds,
   the decoder's end status of each poem, and poems whose text is empty.
3. **Constrained poems out of metre:** every masking + backtracking poem the scorer does not count as in metre, with the
   decoder's own verdicts (gaṇa / prāsa / yati, strict) at generation time, to say why.
4. **By source** (Bhāgavatam 50, Vemana 20, Kūcimañci 20, Gemini 10) and **by metre type** (the 7 common vṛttas /
   every other metre, other fixed-pattern vṛttas included): in metre,
   real words, recognised, one-akshara words, per cell.
5. **Means recomputed** from grid_poems.jsonl for every cell, compared with results/grid.json (a check that the table
   is the mean of the per-poem scores).
6. **The extra strategies on equal terms:** masking only and hybrid ran on the 34 earlier prompts only, so each is set
   beside masking + backtracking on the same 34.
7. **Cost:** seconds per poem (the decoder's own timing; the machine was sometimes shared, so a guide, not a benchmark).
"""
from __future__ import annotations

import ast
import collections
import json
from pathlib import Path

import grid as G

HERE = Path(__file__).resolve().parent
RES = HERE / "results"
SELECTION = HERE / "prompts" / "grid100" / "selection.json"
SOURCE_NAMES = {"bhagavatam": "Bhāgavatam", "vemana": "Vemana", "kuchimanchi_timmakavi": "Kūcimañci", "gemini": "Gemini"}
KEYS = ("all", "words_s", "meaning", "filler")       # in metre, real words, recognised, one-akshara words


def pct(x) -> str:
    return "–" if x is None else f"{100 * x:.1f}"


def mean(xs):
    xs = [float(x) for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def raw_rows(path: Path, modes: list[str]) -> list[dict]:
    out = []
    if not path.exists():
        return out
    data = path.read_bytes()
    assert b"\x00" not in data, f"NUL bytes in {path}"
    for line in data.decode("utf-8").splitlines():
        r = json.loads(line)
        if r["mode"] in modes:
            ev = r.get("eval") or {}
            r["eval"] = ast.literal_eval(ev) if isinstance(ev, str) else ev
            out.append(r)
    return out


def main() -> None:
    sel = json.loads(SELECTION.read_text(encoding="utf-8"))["prompts"]
    ids = {p["id"] for p in sel}
    src = {p["id"]: p["source"] for p in sel}
    poems = [json.loads(l) for l in open(RES / "grid_poems.jsonl", encoding="utf-8")]
    by_cell = collections.defaultdict(list)
    for r in poems:
        by_cell[r["cell"]].append(r)
    vrtta = {r["prompt_id"]: r["line_gana"] is not None for r in by_cell["gold"]}
    grid = json.loads((RES / "grid.json").read_text(encoding="utf-8"))
    cells_json = grid.get("cells", grid)
    res: dict = {}

    # 1. the prompts
    res["prompts"] = {
        "n": len(sel), "by_source": dict(collections.Counter(src.values())),
        "by_origin": dict(collections.Counter(p["from"] for p in sel)),
        "phase1": sum(p["from"].startswith("phase 1") for p in sel),
        "metres": len({p["metre"] for p in sel}), "by_metre": dict(collections.Counter(p["metre"] for p in sel)),
        "vrtta": sum(vrtta.values())}

    # 2. integrity, from the raw files the scorer reads
    integrity = {}
    for kind in ("core", "extra"):
        for row, c in G.cells(kind):
            _, _, path = G.command(row, c)
            _, _, new = G.command(row, c, new=True)
            for mode in G.CELLS[c][0]:
                rows = raw_rows(path, [mode]) + (raw_rows(new, [mode]) if kind == "core" else [])
                rows = [r for r in rows if r.get("seed", 42) == 42 and r["topic"] in ids]
                integrity[f"{row.key}|{mode}"] = rows
    for row, c in G.cells("v2"):
        _, _, path = G.command(row, c, v2=True)
        integrity[f"{row.key}|masking_backtrack_v2"] = [r for r in raw_rows(path, ["masking_backtrack"])
                                                         if r.get("seed", 42) == 42 and r["topic"] in ids]
    table = {}
    for key, rows in integrity.items():
        topics = [r["topic"] for r in rows]
        expect = 34 if key.split("|")[1] in ("masking_only", "hybrid") else 100
        table[key] = {"poems": len(rows), "expected": expect, "distinct_prompts": len(set(topics)),
                      "duplicates": len(topics) - len(set(topics)),
                      "status": dict(collections.Counter(str(r.get("status")) for r in rows)),
                      "empty": sum(1 for r in rows if not (r["eval"].get("lines") or r.get("text", "").strip())),
                      "scored": len(by_cell.get(key, []))}
    res["integrity"] = table

    # 3. constrained poems out of metre
    out_of_metre = []
    for key, rows in by_cell.items():
        mode = key.split("|")[-1] if "|" in key else ""
        if not mode.startswith("masking") and mode != "hybrid":
            continue
        raw = {r["topic"]: r for r in integrity.get(key, [])}
        for r in rows:
            if r["all"]:
                continue
            ev, st = raw.get(r["prompt_id"], {}).get("eval", {}), raw.get(r["prompt_id"], {}).get("status")
            out_of_metre.append({"cell": key, "prompt_id": r["prompt_id"], "status": st,
                                 "gana_strict": ev.get("gana_strict"), "prasa_strict": ev.get("prasa_strict"),
                                 "yati_strict": ev.get("yati_strict"), "n_lines": r["n_lines"]})
    res["constrained_out_of_metre"] = out_of_metre

    # 4. by source and by metre type; 5. means recomputed
    breakdown, recomputed = {}, {}
    for key, rows in by_cell.items():
        groups = {SOURCE_NAMES[s]: [r for r in rows if src.get(r["prompt_id"]) == s] for s in SOURCE_NAMES}
        groups |= {"7 common vṛttas": [r for r in rows if vrtta.get(r["prompt_id"])],
                   "other metres": [r for r in rows if not vrtta.get(r["prompt_id"])]}
        breakdown[key] = {g: {"n": len(rs), **{k: mean(r[k] for r in rs) for k in KEYS}} for g, rs in groups.items()}
        recomputed[key] = {k: mean(r[k] for r in rows) for k in ("all", "words_s", "meaning", "copy", "filler",
                                                                  "repeated", "training_line", "gold_copy")}
    res["by_group"] = breakdown
    diffs = []
    for key, m in recomputed.items():
        j = cells_json.get(key)
        if not j:
            diffs.append(f"{key}: not in grid.json")
            continue
        for k, v in m.items():
            jv = j.get(k)
            if isinstance(jv, dict):
                jv = jv.get("mean")
            if v is not None and jv is not None and abs(v - jv) > 1e-9:
                diffs.append(f"{key} {k}: per-poem mean {v:.6f}, grid.json {jv:.6f}")
    res["recomputed_differences"] = diffs

    # 6. the extra strategies against masking + backtracking on the same 34 prompts
    extra = {}
    for key, rows in by_cell.items():
        row, _, mode = key.partition("|")
        if mode not in ("masking_only", "hybrid"):
            continue
        same = {r["prompt_id"] for r in rows}
        mb = [r for r in by_cell[f"{row}|masking_backtrack"] if r["prompt_id"] in same]
        extra[key] = {"n": len(rows), "this": {k: mean(r[k] for r in rows) for k in KEYS + ("repeated",)},
                      "masking_backtrack": {k: mean(r[k] for r in mb) for k in KEYS + ("repeated",)}}
    res["extra_vs_masking_backtrack"] = extra

    # 7. seconds per poem
    cost = {}
    for key, rows in integrity.items():
        s = sorted(float(r["seconds"]) for r in rows if r.get("seconds") is not None)
        if s:
            cost[key] = {"mean": sum(s) / len(s), "median": s[len(s) // 2], "n": len(s)}
    res["seconds_per_poem"] = cost
    (RES / "analysis.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    labels = {k: v.get("label", k) for k, v in cells_json.items()}
    p = res["prompts"]
    md = ["# Grid checks and breakdowns", "",
          "Written by `analyse_grid.py` from `grid_poems.jsonl`, the raw cell files and the prompt selection. Numbers only.",
          "", "## 1. The prompts", "",
          f"{p['n']} prompts in {p['metres']} metres; {p['vrtta']} in the 7 common vṛttas whose line pattern the scorer "
          f"checks, {p['n'] - p['vrtta']} in other metres (other fixed-pattern vṛttas among them). {p['phase1']} are phase-1 "
          f"poems of the human evaluation.", "",
          "| source | prompts |", "|---|---|"] + [f"| {SOURCE_NAMES[s]} | {n} |" for s, n in p["by_source"].items()] + [
          "", "| how the prompt was obtained | prompts |", "|---|---|"] + [
          f"| {k} | {n} |" for k, n in sorted(p["by_origin"].items())] + [
          "", "| metre | prompts |", "|---|---|"] + [
          f"| {k} | {n} |" for k, n in sorted(p["by_metre"].items(), key=lambda x: -x[1])]
    md += ["", "## 2. Integrity of every cell", "",
           "Poems on the 100 prompts (34 for the extra strategies), from the raw files; `scored` = rows in grid_poems.jsonl.",
           "", "| cell | poems | distinct prompts | duplicates | empty | scored | decoder end status |",
           "|---|---|---|---|---|---|---|"]
    for key, t in table.items():
        flag = "" if t["poems"] == t["expected"] == t["distinct_prompts"] == t["scored"] else " **⚠**"
        md.append(f"| {labels.get(key, key)}{flag} | {t['poems']} | {t['distinct_prompts']} | {t['duplicates']} | "
                  f"{t['empty']} | {t['scored']} | {', '.join(f'{k} {n}' for k, n in sorted(t['status'].items()))} |")
    md += ["", "## 3. Constrained poems the scorer does not count as in metre", "",
           f"{len(out_of_metre)} poems. The decoder's own verdicts at generation (strict) beside the scorer's.", "",
           "| cell | prompt | end status | gaṇa | prāsa | yati | lines |", "|---|---|---|---|---|---|---|"]
    md += [f"| {labels.get(o['cell'], o['cell'])} | {o['prompt_id']} | {o['status']} | {o['gana_strict']} | "
           f"{o['prasa_strict']} | {o['yati_strict']} | {o['n_lines']} |" for o in out_of_metre]
    for title, groups in (("4. By source", list(SOURCE_NAMES.values())), ("5. By metre type", ["7 common vṛttas", "other metres"])):
        md += ["", f"## {title}", "", "In metre % / real words % / recognised % per group (n poems in the header).", "",
               "| cell | " + " | ".join(f"{g} (n {breakdown['gold'][g]['n']})" for g in groups) + " |",
               "|---|" + "---|" * len(groups)]
        for key, b in breakdown.items():
            if key.split("|")[-1] in ("masking_only", "hybrid"):
                continue
            md.append(f"| {labels.get(key, key)} | " + " | ".join(
                f"{pct(b[g]['all'])} / {pct(b[g]['words_s'])} / {pct(b[g]['meaning'])}" for g in groups) + " |")
    md += ["", "## 6. The extra strategies on the same 34 prompts", "",
           "Masking only and hybrid ran on the 34 earlier prompts; masking + backtracking (MB) on the same 34 beside them.",
           "", "| cell | in metre % (MB) | real words % (MB) | recognised % (MB) | one-akshara % (MB) | repeating a line % (MB) |",
           "|---|---|---|---|---|---|"]
    for key, e in extra.items():
        t, b = e["this"], e["masking_backtrack"]
        md.append(f"| {labels.get(key, key)} | " + " | ".join(
            f"{pct(t[k])} ({pct(b[k])})" for k in ("all", "words_s", "meaning", "filler", "repeated")) + " |")
    md += ["", "## 7. Seconds per poem", "",
           "The decoder's own timing per poem (mean / median). Some cells ran beside other jobs on the shared GB10, so "
           "read these as a guide.", "", "| cell | mean s | median s |", "|---|---|---|"]
    md += [f"| {labels.get(k, k)} | {c['mean']:.1f} | {c['median']:.1f} |" for k, c in cost.items()]
    md += ["", "## 8. The table against the per-poem scores", "",
           ("Every cell's means in grid.json equal the means of its rows in grid_poems.jsonl." if not diffs
            else "Differences:\n\n" + "\n".join(f"- {d}" for d in diffs))]
    (RES / "analysis.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(table)} cells checked; {len(out_of_metre)} constrained poems out of metre; "
          f"{len(diffs)} differences against grid.json")


if __name__ == "__main__":
    main()
