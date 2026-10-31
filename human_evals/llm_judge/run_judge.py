#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run an LLM judge on the rubric through an OpenAI-compatible server (vLLM), two turns per poem as judge_prompt.py builds.

    python3 -u run_judge.py --set study1-rated --out results/gemma4-26b_study1.jsonl    # the poems humans have rated
    python3 -u run_judge.py --set study2 --out results/gemma4-26b_study2.jsonl          # the 99 he2_ poems

- **Server:** --url (default the vllm-judge-gemma4 container, http://127.0.0.1:8011/v1), --model its served name.
- **Turns:** [system, turn 1] → reply 1; [system, turn 1, reply 1, turn 2] → reply 2, as the annotators answer 1–3
  before the bhāvam is shown.
- **Replies** are constrained by vLLM's JSON-schema mode to the rubric's values: 1–5, 0/1, or null for a question
  that does not apply; "reasons" come first. judge_prompt.check() validates them again; a failed check is stored
  with its error, never repaired.
- **Decoding:** temperature 0 (greedy), so a rerun gives the same scores.
- **Sets:** study1-rated = the study-1 poems with at least one complete human rating (instance/annotations.db,
  opened read-only); study1 = all 500; study2 = the 99 he2_ poems. --limit N takes the first N.
- **Resumable:** poems already in --out are skipped.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import sqlite3
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge_prompt as jp                                            # noqa: E402

APP = HERE.parent / "annotation_app"
SETS = {"study1": APP / "data", "study1-rated": APP / "data", "study2": APP / "data_study2"}


def answer_schema(poem: dict, keys) -> dict:
    view, props = jp.PoemView(poem), {}
    for k in keys:
        q = jp.rubric.BY_KEY[k]
        props[k] = {"type": "null"} if not jp.rubric.applicable(q, view) else \
            {"type": "integer", "enum": list(q.choices)}
    return {"type": "object", "properties": {
        "reasons": {"type": "object", "properties": {k: {"type": "string", "maxLength": 400} for k in keys},
                    "required": list(keys), "additionalProperties": False},
        "answers": {"type": "object", "properties": props, "required": list(keys), "additionalProperties": False}},
        "required": ["reasons", "answers"], "additionalProperties": False}


def chat(url: str, model: str, messages: list, schema: dict, max_tokens: int) -> tuple[str, dict]:
    body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens,
            "response_format": {"type": "json_schema", "json_schema": {"name": "rubric", "schema": schema}}}
    req = urllib.request.Request(f"{url}/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                out = json.loads(r.read())
            return out["choices"][0]["message"]["content"], out.get("usage") or {}
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 3:
                raise RuntimeError(f"HTTP {e.code}: {e.read()[:500]!r}") from e
        except (urllib.error.URLError, TimeoutError):
            if attempt == 3:
                raise
        time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


def judge(eid: str, poem: dict, ref: dict, args) -> dict:
    m = jp.build(poem, ref, reasons=True, show_checks=args.show_checks)
    row = {"eval_id": eid, "model": args.model, "rubric_version": m["rubric_version"],
           "show_checks": args.show_checks, "errors": []}
    msgs = [{"role": "system", "content": m["system"]}, {"role": "user", "content": m["turn1"]}]
    t0 = time.time()
    for turn, keys, nxt in (("turn1", jp.TURN1, m["turn2"]), ("turn2", jp.TURN2, None)):
        text, usage = chat(args.url, args.model, msgs, answer_schema(poem, keys), args.max_tokens)
        row[f"{turn}_raw"], row[f"{turn}_usage"] = text, usage
        try:
            reply = json.loads(text)
            row["errors"] += [f"{turn}: {e}" for e in jp.check(reply, poem, keys)]
            row.setdefault("answers", {}).update(reply.get("answers") or {})
            row.setdefault("reasons", {}).update(reply.get("reasons") or {})
        except json.JSONDecodeError as e:
            row["errors"].append(f"{turn}: not JSON ({e})")
        msgs = msgs + [{"role": "assistant", "content": text}]
        if nxt:
            msgs.append({"role": "user", "content": nxt})
    row["seconds"] = round(time.time() - t0, 1)
    return row


def rated_ids() -> set[str]:
    con = sqlite3.connect(f"file:{APP / 'instance' / 'annotations.db'}?mode=ro", uri=True)
    try:
        rows = con.execute("SELECT eval_id, answers FROM annotations").fetchall()
    finally:
        con.close()
    likert = [q.key for q in jp.rubric.QUESTIONS if q.kind == "likert" and q.key != "bhavam"]
    return {e for e, a in rows if all(json.loads(a).get(k) is not None for k in likert)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--set", choices=sorted(SETS), required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--url", default="http://127.0.0.1:8011/v1")
    ap.add_argument("--model", default="gemma4-26b")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--max-tokens", type=int, default=1500)
    ap.add_argument("--limit", type=int)
    ap.add_argument("--show-checks", action="store_true")
    args = ap.parse_args()
    poems, ref = jp.load(SETS[args.set])
    ids = sorted(rated_ids() & set(poems)) if args.set == "study1-rated" else sorted(poems)
    ids = ids[:args.limit] if args.limit else ids
    args.out.parent.mkdir(parents=True, exist_ok=True)
    done = {json.loads(l)["eval_id"] for l in open(args.out, encoding="utf-8")} if args.out.exists() else set()
    todo = [e for e in ids if e not in done]
    print(f"{args.set}: {len(ids)} poems, {len(done)} done, {len(todo)} to judge with {args.model}", flush=True)
    lock, t0, n = threading.Lock(), time.time(), 0
    with open(args.out, "a", encoding="utf-8") as fh, cf.ThreadPoolExecutor(args.workers) as pool:
        futs = {pool.submit(judge, e, poems[e], ref, args): e for e in todo}
        for f in cf.as_completed(futs):
            e = futs[f]
            try:
                row = f.result()
            except Exception as ex:                                  # a server failure: report, leave for a rerun
                print(f"{e}: FAILED {ex}", flush=True)
                continue
            with lock:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                fh.flush()
                n += 1
            el = time.time() - t0
            print(f"[{n}/{len(todo)}] {e} {row['seconds']} s {row['answers']} "
                  f"{'ERR ' + '; '.join(row['errors']) if row['errors'] else ''} "
                  f"(eta {el / n * (len(todo) - n) / 60:.0f} min)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
