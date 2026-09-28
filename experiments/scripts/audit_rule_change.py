#!/usr/bin/env python3
"""
Which poems of a constrained run would the enforcer, as it is now, have generated differently?

Written for the rule "a word may not be dead consonants alone" (orthography.py, 2026-09-26),
which only ever removes tokens. Every poem's trace is replayed in order (commits and backtracks)
through the current enforcer, and the poem is flagged when an input of some decision differs:

1. ``rejected``   — a committed token is no longer allowed;
2. ``n_valid``    — the number of allowed tokens at a state differs from the recorded one
                    (the rule only removes tokens, so an equal count is an equal set);
3. ``rerank``     — hybrid only: an allowed token leads to a state whose line-end verdict the
                    rule changed (re-ranking reads ``line_complete`` of each candidate). The trace
                    does not hold the re-ranked pool, so this is conservative: the token may not
                    have been among the candidates scanned;
4. ``incomplete`` — a poem recorded complete is not complete now.

A poem with none of these would come out identically from the same model outputs, so only the
flagged poems need generating again.

usage: audit_rule_change.py RUN_DIR [RUN_DIR ...] [--workers N]
Writes RUN_DIR/rule_audit.json: {"rule": …, "changed": {key: reason}, "unchanged": n}.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")

RULE = "orthography: a word may not be dead consonants alone (2026-09-26)"
BARE_POLLU = re.compile(r"^(?:[క-హ]్)+$")

_index = {}          # per worker: tokenizer name -> TokenIndex
_enf = {}            # per worker: meter -> Enforcer (one meter at a time)


def _tokenizer_name(model: str) -> str:
    """run.json's model field, without the settings note ("id [..]") or a control prefix."""
    return model.split(" [")[0].replace("random-logits/", "").replace("random-canvas/", "")


def _init(names: list[str]) -> None:
    from transformers import AutoTokenizer
    from metrical_decoder.vocab import TokenIndex
    from metrical_decoder.diffusion.loader import _snapshot
    for name in names:
        _index[name] = TokenIndex.from_tokenizer(AutoTokenizer.from_pretrained(_snapshot(name)))


def _enforcer(meter: str, enforce: dict):
    from metrical_decoder.enforcer import Enforcer
    from metrical_decoder.registers import clear_caches
    if meter not in _enf:
        _enf.clear()
        clear_caches()                                  # bound memory: the caches hold one meter's lines
        _enf[meter] = Enforcer(meter, prasa=enforce["prasa"], yati=enforce["yati"], profile=enforce["profile"])
    return _enf[meter]


def audit(task: tuple) -> tuple[str, str | None]:
    """(key, reason the poem would differ, or None)."""
    from metrical_decoder import orthography as ortho
    key, tokenizer, meter, mode, status, enforce, trace = task
    index, enf = _index[tokenizer], _enforcer(meter, enforce)
    memo: dict = {}

    def allowed(state):
        v = memo.get(state)
        if v is None:
            v = memo[state] = [(t, n) for t in index.texts if (n := enf.step(state, t)) is not None]
        return v

    states, out = [enf.initial()], []
    for rec in trace:
        if "to" in rec:                                             # backtrack: check, then rewind
            if rec.get("n_valid") is not None and len(allowed(states[-1])) != rec["n_valid"]:
                return key, f"n_valid at backtrack (pos {len(out)}): {rec['n_valid']} -> {len(allowed(states[-1]))}"
            del out[rec["to"]:], states[rec["to"] + 1:]
            continue
        if "id" not in rec:
            continue
        if rec["pos"] != len(out):
            return key, f"replay mismatch at pos {len(out)}"
        state = states[-1]
        if rec.get("n_valid") is not None:
            ok = allowed(state)
            if len(ok) != rec["n_valid"]:
                return key, f"n_valid (pos {len(out)}): {rec['n_valid']} -> {len(ok)}"
            # the autoregressive loop records "alive" when no scanned candidate ended the line: then no
            # candidate's verdict was True before the rule either, and the pool is the same
            if mode == "hybrid" and rec.get("how") != "alive":
                for text, nxt in ok:
                    if (BARE_POLLU.match(unicodedata.normalize("NFC", nxt.word))
                            and enf.line_complete(nxt._replace(ortho=nxt.ortho | ortho.VOWELED))):
                        return key, f"rerank (pos {len(out)}): {text!r} ended a line before the rule"
        nxt = enf.step(state, index.texts[index.position(rec["id"])])
        if nxt is None:
            return key, f"rejected (pos {len(out)}): {rec.get('text')!r}"
        states.append(nxt)
        out.append(rec["id"])
    if status == "complete" and not enf.poem_complete(states[-1]):
        return key, "incomplete now"
    return key, None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("runs", nargs="+")
    ap.add_argument("--workers", type=int, default=16)
    ns = ap.parse_args()
    runs = [Path(r) for r in ns.runs]
    tasks, per_run, names = [], {}, set()
    for run in runs:
        meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
        name = _tokenizer_name(meta["model"])
        names.add(name)
        rows = {}
        for ln in open(run / "results.jsonl", encoding="utf-8"):
            r = json.loads(ln)
            rows[r["key"]] = r
        n = 0
        for ln in open(run / "traces.jsonl", encoding="utf-8"):
            t = json.loads(ln)
            r = rows.get(t["key"])
            if r is None or r["mode"] == "baseline":
                continue
            # the key names the run too, so two runs' poems never mix
            tasks.append((f"{run}::{t['key']}", name, r["meter"], r["mode"], r["status"], meta["enforce"], t["trace"]))
            n += 1
        per_run[str(run)] = n
    tasks.sort(key=lambda t: (t[2], t[0]))                          # meter by meter: warm caches per worker
    print(f"{len(tasks)} poems from {len(runs)} runs; {ns.workers} workers", flush=True)
    changed: dict[str, dict[str, str]] = {str(r): {} for r in runs}
    t0 = time.time()
    with get_context("spawn").Pool(ns.workers, initializer=_init, initargs=(sorted(names),)) as pool:
        for i, (key, reason) in enumerate(pool.imap_unordered(audit, tasks, chunksize=1), 1):
            run, k = key.split("::", 1)
            if reason:
                changed[run][k] = reason
                print(f"CHANGED {Path(run).name} {k}: {reason}", flush=True)
            if i % 100 == 0 or i == len(tasks):
                print(f"[{i}/{len(tasks)}] {sum(map(len, changed.values()))} changed, "
                      f"{time.time() - t0:.0f}s", flush=True)
    for run in runs:
        out = {"rule": RULE, "changed": dict(sorted(changed[str(run)].items())),
               "unchanged": per_run[str(run)] - len(changed[str(run)])}
        (run / "rule_audit.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{run.name}: {len(changed[str(run)])} changed, {out['unchanged']} unchanged", flush=True)


if __name__ == "__main__":
    main()
