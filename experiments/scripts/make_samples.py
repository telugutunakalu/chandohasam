#!/usr/bin/env python3
"""
Sample poems of a constrained grid as a readable Markdown document.

For every meter and strategy the document shows the best ``--per-cell`` poems that are metrically
perfect — complete, and accepted by the engines for gaṇa, prāsa and yati under the strict profile —
with the prompt they answer and every chosen token with the model's probability of it.

Selection within a (meter, strategy) cell, among the metrically perfect poems:
  1. poems that repeat no line come first (a repeated line satisfies prāsa trivially);
  2. then the higher share of words that have two or more aksharas and occur in the corpora
     (``dataset/*.json``) — single aksharas are excluded because filler such as క క క is in the
     lexicon;
  3. then the higher mean token log-probability.

Token probabilities come from the run's trace: the model's probability of the chosen token over its
whole vocabulary at temperature 1, recorded when the token was chosen. For masking + backtracking
the trace is replayed (commits and rewinds) so that only the tokens of the final poem are shown.

usage: make_samples.py RUN_DIR OUT_MD [--per-cell 2]
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))

from metrical_decoder.analysis import _telugu_words, corpus_lexicon   # noqa: E402
from metrical_decoder.registers import _syllables                      # noqa: E402

MODES = {"masking_only": "Masking only",
         "masking_backtrack": "Masking + backtracking",
         "hybrid": "Hybrid (mask + accept-state re-ranking)"}
STRICT = ("gana_strict", "prasa_strict", "yati_strict")


# ----------------------------------------------------------------------------- data
def load(run: Path):
    meta = json.loads((run / "run.json").read_text(encoding="utf-8"))
    rows = [json.loads(ln) for ln in open(run / "results.jsonl", encoding="utf-8")]
    traces = {}
    for ln in open(run / "traces.jsonl", encoding="utf-8"):
        t = json.loads(ln)
        traces[t["key"]] = t["trace"]
    prompts = {}
    for ln in open(run / "prompts.jsonl", encoding="utf-8"):
        p = json.loads(ln)
        prompts[(p["meter"], p["topic"])] = p
    return meta, rows, traces, prompts


def final_tokens(trace: list[dict], ids: list[int]) -> list[dict]:
    """The trace records of the tokens that make up the final poem (rewinds applied)."""
    out: list[dict] = []
    for rec in trace:
        if "to" in rec:
            del out[rec["to"]:]
        elif "id" in rec and "pos" in rec:
            del out[rec["pos"]:]
            out.append(rec)
    if [r["id"] for r in out] != list(ids):
        raise ValueError("trace replay does not reproduce the poem's tokens")
    return out


def word_stats(lines: list[str], lexicon: frozenset[str]) -> tuple[float, float]:
    """(share of words with ≥ 2 aksharas found in the corpora, share of 1-akshara words)."""
    words = [w for ln in lines for w in _telugu_words(ln)]
    if not words:
        return 0.0, 0.0
    long_known = sum(1 for w in words if len(_syllables(w)) >= 2 and w in lexicon)
    single = sum(1 for w in words if len(_syllables(w)) == 1)
    return long_known / len(words), single / len(words)


def perfect(row: dict) -> bool:
    ev = row.get("eval") or {}
    return row.get("status") == "complete" and all(ev.get(k) for k in STRICT)


# ----------------------------------------------------------------------------- formatting
def tok_text(text: str) -> str:
    return text.replace("\n", "⏎").replace(" ", "␣") or "∅"


def prob(p: float) -> str:
    return f"{p:.2f}" if p >= 0.01 else f"{p:.1e}".replace("e-0", "e-")


def rule_summary(user_prompt: str) -> str:
    """The prompt's description of the meter: from "Meter:" up to the guru/laghu definition."""
    lines = user_prompt.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("Meter:"))
    end = next(i for i, ln in enumerate(lines) if ln.startswith("Guru (U) and laghu"))
    return "\n".join(lines[start:end]).strip()


def telugu_name(user_prompt: str, meter: str) -> str:
    first = user_prompt.splitlines()[0]                  # "Write a Telugu padyam in the meter ఉత్పలమాల (utpalamala)."
    name = first.split(" in the meter ", 1)[-1].split(" (", 1)[0].strip()
    return name or meter


def poem_block(row: dict, recs: list[dict], lexicon: frozenset[str], topics: dict, n: int) -> list[str]:
    ev = row["eval"]
    lexical, single = word_stats(ev["lines"], lexicon)
    logps = [r["logp"] for r in recs if r.get("how") not in ("forced_nl",)]
    judged = [r for r in recs if r.get("top") and r["top"][0][3] is not None]
    kept = sum(1 for r in recs if r.get("rank") == 1) / len(recs)
    over = sum(1 for r in judged if r["top"][0][3] is False) / len(judged) if judged else 0.0
    out = [f"**Sample {n}** · topic {row['topic']} ({topics.get(row['topic'], '')}) · seed {row['seed']} · "
           f"{row['n_tokens']} tokens · {row['seconds']:.1f} s", "",
           "| పాదము | line | gaṇa pattern (U = guru, I = laghu) |", "|---|---|---|"]
    for i, (ln, pat) in enumerate(zip(ev["lines"], ev["patterns"]), 1):
        out.append(f"| {i} | {ln} | `{pat}` |")
    out += ["",
            f"Engines (strict): gaṇa ✓ · prāsa ✓ · yati ✓ — corpus words (≥ 2 aksharas) {100 * lexical:.0f}% · "
            f"single-akshara words {100 * single:.0f}% · repeated lines {ev.get('duplicate_lines', 0)} · "
            f"mean token probability (geometric) {math.exp(sum(logps) / len(logps)):.3f} · "
            f"model's first choice kept {100 * kept:.0f}% · constraint overrode {100 * over:.0f}% · "
            f"backtracks {row.get('n_backtracks') or 0}", "",
            f"<details><summary>Token probabilities ({len(recs)} tokens)</summary>", "",
            "| line | chosen tokens with the model's probability (✱ = the model's first choice was not allowed) |",
            "|---|---|"]
    line, cells = 1, []
    for r in recs:
        mark = "✱" if r.get("top") and r["top"][0][3] is False else ""
        forced = " forced" if r.get("how") == "forced_nl" else ""
        cells.append(f"`{tok_text(r['text'])}` {prob(math.exp(r['logp']))}{mark}{forced}")
        if r["text"] == "\n":
            out.append(f"| {line} | {' · '.join(cells)} |")
            line, cells = line + 1, []
    if cells:
        out.append(f"| {line} | {' · '.join(cells)} |")
    out += ["", "</details>", ""]
    return out


def prompt_block(meter: str, used: list[str], prompts: dict, topics: dict) -> list[str]:
    """The prompt of the first topic in full; the others are the same but for the topic line (checked)."""
    first = prompts[(meter, used[0])]
    out = [f"<details><summary>Prompt (topic {used[0]}; the other topics differ only in the topic line)</summary>", ""]
    for m in first["messages"]:
        out += [f"*{m['role']}*", "", "```text", m["content"].strip(), "```", ""]
    for t in used[1:]:
        other = prompts[(meter, t)]["messages"]
        same = [m["content"].replace(topics[t], topics[used[0]]) for m in other] == [m["content"] for m in first["messages"]]
        if not same:
            raise ValueError(f"{meter}: the prompt for {t} differs beyond its topic")
        out += [f"Topic {t}: `Topic (విషయము): {topics[t]}`", ""]
    return out + ["</details>", ""]


# ----------------------------------------------------------------------------- document
def build(run: Path, per_cell: int, title: str, intro: list[str]) -> tuple[str, list[str]]:
    meta, rows, traces, prompts = load(run)
    lexicon = corpus_lexicon()
    topics = meta.get("topics", {})
    cells: dict[tuple[str, str], list[tuple]] = defaultdict(list)
    for r in rows:
        if r["mode"] in MODES and perfect(r):
            lexical, single = word_stats(r["eval"]["lines"], lexicon)
            logps = [x["logp"] for x in traces[r["key"]] if "id" in x]
            score = ((r["eval"].get("duplicate_lines") or 0) == 0, round(lexical, 6), sum(logps) / len(logps))
            cells[(r["meter"], r["mode"])].append((score, r))
    short = []
    doc = [f"# {title}", ""] + intro + ["", "## Meters", "", "| # | meter | |", "|---|---|---|"]
    body: list[str] = []
    for i, meter in enumerate(meta["meters"], 1):
        prompt = prompts.get((meter, "T1")) or next(p for (m, _), p in prompts.items() if m == meter)
        user = prompt["messages"][1]["content"]
        name = telugu_name(user, meter)
        doc.append(f"| {i} | {name} ({meter}) | [samples](#{meter}) |")
        body += [f'<a id="{meter}"></a>', "", f"## {i}. {name} ({meter})", "", "```text", rule_summary(user), "```", ""]
        chosen = {}
        for mode in MODES:
            picks = [r for _, r in sorted(cells[(meter, mode)], key=lambda sr: sr[0], reverse=True)[:per_cell]]
            if len(picks) < per_cell:
                short.append(f"{meter} / {mode}: {len(picks)}")
            chosen[mode] = picks
        used_topics = sorted({r["topic"] for picks in chosen.values() for r in picks})
        if used_topics:
            body += prompt_block(meter, used_topics, prompts, topics)
        for mode, label in MODES.items():
            body += [f"### {label}", ""]
            if not chosen[mode]:
                body += ["*No metrically perfect poem in this cell.*", ""]
            for n, r in enumerate(chosen[mode], 1):
                body += poem_block(r, final_tokens(traces[r["key"]], r["ids"]), lexicon, topics, n)
        body += ["[↑ meters](#meters)", "", "---", ""]
    return "\n".join(doc + ["", "---", ""] + body) + "\n", short


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("run")
    ap.add_argument("out")
    ap.add_argument("--per-cell", type=int, default=2)
    ap.add_argument("--title", required=True)
    ap.add_argument("--intro", default="", help="a Markdown file whose text goes under the title")
    ns = ap.parse_args()
    intro = Path(ns.intro).read_text(encoding="utf-8").splitlines() if ns.intro else []
    md, short = build(Path(ns.run), ns.per_cell, ns.title, intro)
    Path(ns.out).parent.mkdir(parents=True, exist_ok=True)
    Path(ns.out).write_text(md, encoding="utf-8")
    print(f"{ns.out}: {len(md.encode('utf-8')) / 1e6:.2f} MB")
    for s in short:
        print("fewer than per-cell:", s)


if __name__ == "__main__":
    main()
