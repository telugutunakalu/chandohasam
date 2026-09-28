#!/usr/bin/env python3
"""
Every poem of a model's inference ablations as one structured JSON document.

The runs of one model (free baseline + the three constrained strategies) are merged into a single
file: the model and experiment settings, each source run's exact configuration, the meters, the
prompts, and one record per poem with every field the runs recorded — the poem, its prompt, the
engines' evaluation, the generation statistics, the chosen tokens with their probabilities and the
full decoding trace. Field names are the runs' own (so the analysis code's names still apply);
``fields`` in the document describes each one. Rows superseded by reruns (``superseded_*.jsonl``) are
not included.

The file is valid JSON with one poem per line inside ``poems`` (easy to grep or stream). With
``--max-mb`` the poems are split, at meter boundaries and in catalogue order, into as few parts as
keep every file under that size (GitHub refuses files over 100 MB): ``OUT.part1.json``, … Each part is
a complete document — the same header, with the meters and prompts of its own poems — and says
which part it is (``part``).

usage: export_inference_json.py --model-json SPEC.json [--max-mb 95 [--split-after kandamu]] OUT.json RUN_DIR …
       (SPEC.json: {"id", "label", "precision", "decoding", "prefill", …})
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import sys
from pathlib import Path

ABLATIONS = ("baseline", "masking_only", "masking_backtrack", "hybrid")
POEM_FIELDS = ("text",)
ROW_GROUPED = {"key", "meter", "topic", "mode", "seed", "prompt_sha", "status", "text", "eval"}

FIELDS = {
    "poems[]": {
        "id": "meter|topic|ablation|seed — unique within the model",
        "run": "the run directory the poem comes from (see runs)",
        "meter / meter_name / meter_class": "meter id, its Telugu name and class (from the prompt)",
        "topic / topic_text": "topic id (T1–T3) and its Telugu text",
        "ablation": "baseline (free generation) | masking_only | masking_backtrack | hybrid",
        "seed": "random seed of the poem",
        "prompt_sha / prompt": "hash of the prompt messages; the system and user messages and the prefill "
                               "appended after the generation prompt (null when none). Token ids: prompts[sha]",
        "status": "complete (constrained, finished in meter) | eos (baseline: the model ended its reply) | "
                  "budget (hit the token cap) | dead_end",
        "poem.text": "the generated text exactly as decoded",
        "poem.lines / poem.gana_patterns": "the lines the engines read and their scansion (U guru, I laghu)",
        "evaluation": "the engines' verdicts: gana_strict, prasa_strict, yati_strict (strict profile), the "
                      "relaxed variants, all_strict, identified_as, aksharas, duplicate_lines, …",
        "generation": "every other field of the run's result row: model (with settings), n_tokens, ids "
                      "(token ids of the poem), seconds, n_backtracks, n_masks, ms_per_mask, mask_cache, and "
                      "for diffusion n_passes, n_blocks, tokens_per_pass; for baselines left_meter_at (token "
                      "index where the text left the meter) and complete_in_meter",
        "tokens": "the poem's tokens in order: text, prob (the model's probability of the token over its "
                  "whole vocabulary at temperature 1, when it was chosen) and overridden (true: the model's "
                  "own first choice was not allowed; null: not known, e.g. free text out of meter)",
        "trace": "the full decoding log in order (see trace[])",
    },
    "trace[] (event = token)": {
        "in_poem": "true if the token is part of the final poem (false: later rewound by backtracking, "
                   "or the end-of-text token of a baseline)",
        "pos": "index of the token in the poem when it was chosen",
        "id / text": "token id and its text",
        "how": "sample (free autoregressive draw) | accept / alive (hybrid re-ranking pools) | forced_nl "
               "(line break imposed: the line could not continue) | proposal (diffusion: the model's own "
               "sampled token) | masked (drawn from the allowed tokens) | rerank (hybrid) | eos",
        "logp / prob": "log-probability and probability of the token under the model (whole vocabulary, T = 1)",
        "rank": "rank of the token in the model's distribution (1 = the model's first choice)",
        "p_pick": "probability with which the token was drawn (after temperature, top-p and masking)",
        "n_valid / valid_mass": "number of allowed tokens at this step and the model's probability mass on "
                                "them (null when not computed: free text already out of meter)",
        "H": "entropy of the model's distribution (nats, T = 1)",
        "tau": "temperature used for the draw",
        "top": "the model's five most probable tokens: token_id, text, prob, allowed (null if unknown)",
        "line / akshara": "line index (0-based) and akshara count of that line after the token",
        "in_meter": "false once free text has left the meter",
        "block / pass / canvas_pos / run": "diffusion only: canvas block, denoising pass, position in the "
                                           "canvas, position in the pass's accepted run of proposals",
    },
    "trace[] (event = backtrack)": {
        "reason": "few_valid | mass_collapse | stall | empty — why the loop rewound",
        "to": "the poem is cut back to this many tokens",
        "tau / boost": "temperature (autoregressive) or temperature boost (diffusion) after the rewind",
        "n_valid / valid_mass": "the allowed set that triggered the rewind",
    },
}


def _finite(x):
    """JSON has no inf / nan: they become null."""
    if isinstance(x, float) and not math.isfinite(x):
        return None
    if isinstance(x, dict):
        return {k: _finite(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_finite(v) for v in x]
    return x


def _prob(logp):
    return None if logp is None or not math.isfinite(logp) else round(math.exp(logp), 8)


def _surviving(trace: list[dict]) -> set[int]:
    """Indices of the trace's token records that make up the final poem (rewinds applied)."""
    out: list[int] = []
    for i, rec in enumerate(trace):
        if "to" in rec:
            del out[rec["to"]:]
        elif "id" in rec and "pos" in rec and rec.get("how") != "eos":
            del out[rec["pos"]:]
            out.append(i)
    return set(out)


def _trace(trace: list[dict], ids: list[int]) -> tuple[list[dict], list[dict]]:
    keep = _surviving(trace)
    events, tokens = [], []
    for i, rec in enumerate(trace):
        if "to" in rec:
            events.append({"event": "backtrack", **rec})
            continue
        if "id" not in rec:
            events.append({"event": rec.get("how", "other"), **rec})
            continue
        e = {"event": "token", "in_poem": i in keep}
        for k, v in rec.items():
            if k == "top":
                e["top"] = [{"token_id": t[0], "text": t[1], "prob": t[2], "allowed": t[3]} for t in v]
            else:
                e[k] = v
            if k == "logp":
                e["prob"] = _prob(v)
        events.append(e)
        if i in keep:
            top = rec.get("top") or []
            tokens.append({"text": rec["text"], "prob": _prob(rec["logp"]),
                           "overridden": (top[0][3] is False) if top and top[0][3] is not None else None})
    got = [trace[i]["id"] for i in sorted(keep)]
    if got != list(ids):
        raise ValueError("the trace does not reproduce the poem's token ids")
    return events, tokens


def _meter_info(user: str, meter: str) -> tuple[str, str, str]:
    lines = user.splitlines()
    name = lines[0].split(" in the meter ", 1)[-1].split(" (", 1)[0].strip() or meter
    meta = next((ln for ln in lines if ln.startswith("Meter:")), "")
    klass = meta.split("), ", 1)[-1].rstrip(".").removeprefix("a ").removeprefix("an ").removesuffix(" meter")
    start = next(i for i, ln in enumerate(lines) if ln.startswith("Meter:"))
    end = next(i for i, ln in enumerate(lines) if ln.startswith("Guru (U) and laghu"))
    return name, klass, "\n".join(lines[start:end]).strip()


def build(spec: dict, runs: list[Path]) -> tuple[dict, list[dict]]:
    run_meta, prompts, meters, topics, poems = {}, {}, {}, {}, []
    seen = set()
    for run in runs:
        meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
        run_meta[run.name] = meta
        topics.update(meta.get("topics", {}))
        for ln in open(run / "prompts.jsonl", encoding="utf-8"):
            p = json.loads(ln)
            entry = prompts.setdefault(p["prompt_sha"], {"meter": p["meter"], "topic": p["topic"],
                                                          "messages": p["messages"], "prefill": spec.get("prefill"),
                                                          "prompt_token_ids": p.get("prompt_ids")})
            if entry["prompt_token_ids"] is None and p.get("prompt_ids"):
                entry["prompt_token_ids"] = p["prompt_ids"]
            if p["meter"] not in meters:
                name, klass, rules = _meter_info(p["messages"][1]["content"], p["meter"])
                meters[p["meter"]] = {"name": name, "class": klass, "rules": rules,
                                      "token_budget": (meta.get("token_budget") or {}).get(p["meter"])}
        traces = {}
        for ln in open(run / "traces.jsonl", encoding="utf-8"):
            t = json.loads(ln)
            traces[t["key"]] = t["trace"]
        for ln in open(run / "results.jsonl", encoding="utf-8"):
            r = json.loads(ln)
            if r["key"] in seen:
                raise ValueError(f"{r['key']} appears twice")
            seen.add(r["key"])
            ev = dict(r.get("eval") or {})
            lines, patterns = ev.pop("lines", None), ev.pop("patterns", None)
            prompt = prompts[r["prompt_sha"]]
            events, tokens = _trace(traces[r["key"]], r["ids"])
            poems.append({
                "id": r["key"], "run": run.name,
                "meter": r["meter"], "meter_name": meters[r["meter"]]["name"], "meter_class": meters[r["meter"]]["class"],
                "topic": r["topic"], "topic_text": topics.get(r["topic"]),
                "ablation": r["mode"], "seed": r["seed"],
                "prompt_sha": r["prompt_sha"],
                "prompt": {"system": prompt["messages"][0]["content"], "user": prompt["messages"][1]["content"],
                           "prefill": spec.get("prefill")},
                "status": r["status"],
                "poem": {"text": r["text"], "lines": lines, "gana_patterns": patterns},
                "evaluation": ev,
                "generation": {k: v for k, v in r.items() if k not in ROW_GROUPED},
                "tokens": tokens,
                "trace": events,
            })
    order = {m: i for i, m in enumerate(ABLATIONS)}
    meter_order = {m: i for i, m in enumerate(next(iter(run_meta.values()))["meters"])}
    poems.sort(key=lambda p: (meter_order.get(p["meter"], 99), p["topic"], order[p["ablation"]], p["seed"]))
    counts = {a: sum(p["ablation"] == a for p in poems) for a in ABLATIONS}
    in_meter = {a: sum(1 for p in poems if p["ablation"] == a and (
        p["generation"].get("complete_in_meter") if a == "baseline" else
        p["status"] == "complete" and all(p["evaluation"].get(k) for k in ("gana_strict", "prasa_strict", "yati_strict"))))
        for a in ABLATIONS}
    header = {
        "format": "chandohasam inference export, version 1",
        "created": datetime.date.today().isoformat(),
        "model": spec,
        "experiment": {
            "ablations": list(ABLATIONS),
            "meters": len(meters), "topics": topics,
            "seeds": sorted({p["seed"] for p in poems}),
            "constraint": "gaṇa + prāsa + yati enforced exactly on the metrical DAWG (strict profile, yati sandhi "
                          "off) with the orthography filter; the baseline is free generation, the enforcer only "
                          "watches",
            "poems": len(poems), "poems_per_ablation": counts,
            "in_meter_per_ablation": in_meter,
        },
        "runs": run_meta,
        "fields": FIELDS,
        "meters": meters,
        "prompts": prompts,
    }
    return _finite(header), [_finite(p) for p in poems]


def _line(p: dict) -> str:
    return json.dumps(p, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def write(path: Path, header: dict, lines: list[str]) -> None:
    head = json.dumps(header, ensure_ascii=False, indent=1, allow_nan=False)
    assert head.endswith("\n}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head[:-2] + ',\n "poems": [\n')
        f.write(",\n".join(lines))
        f.write("\n ]\n}\n")


def split(header: dict, poems: list[dict], max_bytes: int,
          split_after: tuple[str, ...] = ()) -> list[tuple[dict, list[str]]]:
    """Whole meters, in order, in parts that each stay under ``max_bytes``: cut after the meters in
    ``split_after`` (the same cut for every model), else as evenly as whole meters allow."""
    by_meter: dict[str, list[str]] = {}
    for p in poems:
        by_meter.setdefault(p["meter"], []).append(_line(p))
    budget = max_bytes - len(json.dumps(header, ensure_ascii=False, indent=1).encode()) - 10_000
    sizes = {m: sum(len(x.encode()) + 2 for x in lines) for m, lines in by_meter.items()}
    if split_after:
        groups, cur = [], []
        for meter in sizes:
            cur.append(meter)
            if meter in split_after:
                groups.append(cur)
                cur = []
        groups += [cur] if cur else []
        too_big = [g[0] for g in groups if sum(sizes[m] for m in g) > budget]
        if too_big:
            raise ValueError(f"the part starting at {too_big[0]} exceeds the size limit")
        return _parts(header, by_meter, groups)
    n_parts = max(1, math.ceil(sum(sizes.values()) / budget))
    while True:                                   # the fewest parts, as even as whole meters allow
        target = sum(sizes.values()) / n_parts
        groups, cur, acc = [], [], 0
        for meter, n in sizes.items():
            # cut before a meter whose middle would cross the next part boundary
            if cur and acc + n / 2 > target * (len(groups) + 1) and len(groups) < n_parts - 1:
                groups.append(cur)
                cur = []
            cur.append(meter)
            acc += n
        groups.append(cur)
        if all(sum(sizes[m] for m in g) <= budget for g in groups):
            break
        n_parts += 1
    return _parts(header, by_meter, groups)


def _parts(header: dict, by_meter: dict[str, list[str]], groups: list[list[str]]) -> list[tuple[dict, list[str]]]:
    parts = []
    for i, meters in enumerate(groups, 1):
        keep = set(meters)
        h = dict(header)
        h["part"] = {"index": i, "of": len(groups), "meters": meters,
                     "poems": sum(len(by_meter[m]) for m in meters),
                     "note": "the model's poems are split across the parts by meter; experiment gives the totals"}
        h["meters"] = {m: v for m, v in header["meters"].items() if m in keep}
        h["prompts"] = {k: v for k, v in header["prompts"].items() if v["meter"] in keep}
        parts.append((h, [x for m in meters for x in by_meter[m]]))
    return parts


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("out")
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--model-json", required=True)
    ap.add_argument("--max-mb", type=float, default=None, help="split into parts under this size")
    ap.add_argument("--split-after", default="", help="comma-separated meters that end a part (with --max-mb)")
    ns = ap.parse_args()
    spec = json.loads(Path(ns.model_json).read_text(encoding="utf-8"))
    header, poems = build(spec, [Path(r) for r in ns.runs])
    out = Path(ns.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"{out.name}: {len(poems)} poems; per ablation {header['experiment']['poems_per_ablation']}", flush=True)
    if not ns.max_mb:
        write(out, header, [_line(p) for p in poems])
        print(f"  {out}: {out.stat().st_size / 1e6:.1f} MB", flush=True)
        return
    cuts = tuple(m for m in ns.split_after.split(",") if m)
    for h, lines in split(header, poems, int(ns.max_mb * 1e6), cuts):
        path = out.with_name(f"{out.stem}.part{h['part']['index']}.json")
        write(path, h, lines)
        print(f"  {path}: {h['part']['poems']} poems, meters {h['part']['meters'][0]} … "
              f"{h['part']['meters'][-1]} ({len(h['part']['meters'])}), {path.stat().st_size / 1e6:.1f} MB", flush=True)


if __name__ == "__main__":
    sys.exit(main())
