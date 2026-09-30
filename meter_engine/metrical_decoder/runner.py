# -*- coding: utf-8 -*-
"""
Run a grid of meters × topics × modes × seeds and keep everything.

A run directory holds

* ``run.json`` — the configuration;
* ``prompts.jsonl`` — the messages and prompt ids of every (meter, topic);
* ``results.jsonl`` — one row per generation: key, text, status, statistics
  and the evaluation (no trace);
* ``traces.jsonl`` — the same key and the per-token trace.

Rows already written are skipped, so an interrupted run resumes where it
stopped. :func:`summarize` turns ``results.jsonl`` (and the traces, for the
probability statistics) into a per-meter × per-mode table.

Owns: :func:`run_grid`, :func:`summarize`. Must not import torch.
"""
from __future__ import annotations

import hashlib
import json
import statistics
import time
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Callable, Optional, Sequence

from .enforcer import Enforcer
from .evaluate import evaluate
from .parallel import ParallelMaskCache, mask_pool
from .registers import clear_caches
from .prompts import build_messages
from .strategies import DecodeConfig, MaskCache, decode, token_budget
from .vocab import TokenIndex


def _done_keys(path: Path) -> set[str]:
    if not path.exists():
        return set()
    keys = set()
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            try:
                keys.add(json.loads(ln)["key"])
            except (json.JSONDecodeError, KeyError):
                continue
    return keys


def run_grid(source, index: TokenIndex, meters: Sequence[str], modes: Sequence[str],
             topics: Sequence[tuple[str, str]], seeds: Sequence[int], out_dir: str | Path,
             cfg: DecodeConfig = DecodeConfig(), units: int = 1, model_name: str = "",
             log: Callable[[str], None] = print, prasa: bool = False, yati: bool = False,
             profile: str = "strict", mask_workers: int = 0, decode_fn: Callable = decode) -> Path:
    """Generate and evaluate every cell of the grid; returns the run directory.
    ``mask_workers`` > 0 computes the masks in that many worker processes (same masks, faster).
    ``decode_fn`` generates one poem (default: the autoregressive strategies; the diffusion loop is
    ``metrical_decoder.diffusion.decoding.decode_diffusion``)."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "run.json").write_text(json.dumps({
        "model": model_name, "meters": list(meters), "modes": list(modes), "topics": dict(topics),
        "seeds": list(seeds), "units": units, "config": asdict(cfg),
        "enforce": {"gana": True, "prasa": prasa, "yati": yati, "profile": profile}, "mask_workers": mask_workers,
        "token_budget": {m: token_budget(Enforcer(m, units=units), cfg) for m in meters},
        "started": time.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False, indent=1), encoding="utf-8")
    done = _done_keys(out / "results.jsonl")
    total = len(meters) * len(topics) * len(modes) * len(seeds)
    counter = [len(done)]
    with open(out / "results.jsonl", "a", encoding="utf-8") as fr, \
            open(out / "traces.jsonl", "a", encoding="utf-8") as ft, \
            open(out / "prompts.jsonl", "a", encoding="utf-8") as fp:
        for meter in meters:
            todo_meter = [k for k in (f"{meter}|{t}|{m}|{s}" for t, _ in topics for m in modes for s in seeds)
                          if k not in done]
            if not todo_meter:
                continue
            clear_caches()                    # the caches hold one meter's lines: bound memory on long runs
            enf = Enforcer(meter, units=units, prasa=prasa, yati=yati, profile=profile)
            pool = mask_pool(index, mask_workers) if mask_workers > 0 else None     # fresh workers, same reason
            masks = ParallelMaskCache(enf, index, pool, mask_workers) if pool else MaskCache(enf, index)
            try:
                _run_meter(source, index, meter, enf, masks, modes, topics, seeds, done, cfg, units,
                           model_name, log, fr, ft, fp, total, counter, decode_fn)
            finally:
                if pool:
                    pool.shutdown()
    return out


def _run_meter(source, index, meter, enf, masks, modes, topics, seeds, done, cfg, units, model_name, log,
               fr, ft, fp, total, counter, decode_fn: Callable = decode) -> None:
    """Every (topic, mode, seed) of one meter not yet in ``done``."""
    for topic_id, topic in topics:
        messages = build_messages(meter, topic, units)
        prompt_ids = source.prompt_ids(messages) if hasattr(source, "prompt_ids") else []
        sha = hashlib.sha1(json.dumps(messages, ensure_ascii=False).encode()).hexdigest()[:12]
        todo = [(m, s) for m in modes for s in seeds if f"{meter}|{topic_id}|{m}|{s}" not in done]
        if not todo:
            continue
        fp.write(json.dumps({"meter": meter, "topic": topic_id, "prompt_sha": sha, "messages": messages,
                             "prompt_ids": list(prompt_ids)}, ensure_ascii=False) + "\n")
        fp.flush()
        for mode, seed in todo:
            key = f"{meter}|{topic_id}|{mode}|{seed}"
            r = decode_fn(enf, index, source, prompt_ids, mode, seed, cfg, masks)
            trace = r.pop("trace")
            r.pop("config", None)
            ev = evaluate(r["text"], meter, units)
            row = {"key": key, "meter": meter, "topic": topic_id, "mode": mode, "seed": seed,
                   "model": model_name, "prompt_sha": sha, **r, "eval": ev}
            fr.write(json.dumps(row, ensure_ascii=False) + "\n")
            fr.flush()
            ft.write(json.dumps({"key": key, "trace": trace}, ensure_ascii=False) + "\n")
            ft.flush()
            counter[0] += 1
            log(f"[{counter[0]}/{total}] {key}: {r['status']} tok={r['n_tokens']} "
                f"gana={ev['gana_strict']} prasa={ev['prasa_strict']} yati={ev['yati_strict']} "
                f"{r['seconds']:.1f}s")


# ----------------------------------------------------------------------------
# summary
# ----------------------------------------------------------------------------
COLUMNS = ("gana_strict", "gana", "prasa_strict", "yati_strict", "all_strict", "all_relaxed")
# trace records of committed tokens: autoregressive (sample / accept / alive) and diffusion
# (proposal / masked / rerank) choices, and imposed line breaks
TOKEN_HOWS = ("sample", "accept", "alive", "proposal", "masked", "rerank", "forced_nl")


def _trace_stats(path: Path) -> dict[str, dict]:
    """Per key: mean logp of chosen tokens, mean valid mass, share of steps where the model's argmax was valid."""
    stats: dict[str, dict] = {}
    if not path.exists():
        return stats
    with open(path, encoding="utf-8") as fh:
        for ln in fh:
            row = json.loads(ln)
            toks = [t for t in row["trace"] if t.get("how") in TOKEN_HOWS]
            if not toks:
                continue
            masses = [t["valid_mass"] for t in toks if t.get("valid_mass") is not None]
            argmax_ok = [t["top"][0][3] for t in toks if t.get("top") and t["top"][0][3] is not None]
            stats[row["key"]] = {
                "mean_logp": statistics.fmean(t["logp"] for t in toks),
                "mean_valid_mass": statistics.fmean(masses) if masses else None,
                "argmax_valid": statistics.fmean(argmax_ok) if argmax_ok else None,
            }
    return stats


def summarize(run_dir: str | Path, write: bool = True) -> str:
    """A markdown table per meter and mode (rates in %), plus the overall row per mode."""
    run = Path(run_dir)
    rows = [json.loads(ln) for ln in open(run / "results.jsonl", encoding="utf-8")]
    tstats = _trace_stats(run / "traces.jsonl")
    cells: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in rows:
        cells[(r["meter"], r["mode"])].append(r)
        cells[("ALL", r["mode"])].append(r)
    head = ["meter", "mode", "n"] + list(COLUMNS) + ["tok", "s", "logp", "valid_mass", "argmax_valid", "bt"]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    meters = sorted({m for m, _ in cells if m != "ALL"}) + ["ALL"]
    modes = [m for m in ("baseline", "masking_only", "masking_backtrack", "hybrid") if any(k[1] == m for k in cells)]
    for meter in meters:
        for mode in modes:
            rs = cells.get((meter, mode))
            if not rs:
                continue
            ts = [tstats.get(r["key"], {}) for r in rs]

            def mean(key, src):
                xs = [x[key] for x in src if x.get(key) is not None]
                return f"{statistics.fmean(xs):.3f}" if xs else "–"

            rates = [f"{100 * sum(bool(r['eval'].get(c)) for r in rs) / len(rs):.0f}" for c in COLUMNS]
            lines.append("| " + " | ".join([meter, mode, str(len(rs)), *rates,
                                            f"{statistics.fmean(r['n_tokens'] for r in rs):.0f}",
                                            f"{statistics.fmean(r['seconds'] for r in rs):.1f}",
                                            mean("mean_logp", ts), mean("mean_valid_mass", ts),
                                            mean("argmax_valid", ts),
                                            f"{statistics.fmean(r.get('n_backtracks') or 0 for r in rs):.1f}"]) + " |")
    table = "\n".join(lines)
    if write:
        (run / "summary.md").write_text(table + "\n", encoding="utf-8")
    return table
