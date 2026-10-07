#!/usr/bin/env python3
"""
v1 against v2 (akshara inventory) on the same poems: does the inventory make the poems more real?

Every run is restricted to the keys all of them share (the trial's: 37 meters × 3 strategies × the
trial's topic and seed), so the comparison is poem for poem. Per run and strategy: poems complete and
accepted by the engines (strict), dead ends, chosen-token log-probability, the model's first choice
overridden, mass on allowed tokens, and the word measures of the absent-word study (90% / 10% split
of the real verse): corpus words, words containing an akshara never seen in real verse, junk (minimal
absent factor ≤ 2), single-akshara words; plus poems repeating a line.

usage: compare_inventory_trial.py OUT_MD LABEL=RUN_DIR [LABEL=RUN_DIR …]
"""
from __future__ import annotations

import json
import random
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
sys.path.insert(0, str(ROOT / "experiments" / "scripts"))

from metrical_decoder.analysis import _telugu_words                     # noqa: E402
from measure_absent_words import Scorer, aksharas, real_poems          # noqa: E402

MODES = ("masking_only", "masking_backtrack", "hybrid")


def main() -> None:
    out = Path(sys.argv[1])
    runs = dict(a.split("=", 1) for a in sys.argv[2:])
    rows, traces = {}, {}
    for label, d in runs.items():
        rows[label] = {json.loads(l)["key"]: json.loads(l) for l in open(Path(d) / "results.jsonl", encoding="utf-8")}
        traces[label] = {json.loads(l)["key"]: json.loads(l)["trace"] for l in open(Path(d) / "traces.jsonl", encoding="utf-8")}
    keys = set.intersection(*(set(k for k, r in rs.items() if r["mode"] in MODES) for rs in rows.values()))
    poems = real_poems()
    rng = random.Random(0)
    order = list(range(len(poems)))
    rng.shuffle(order)
    train = [poems[i] for i in order[len(poems) // 10:]]
    scorer = Scorer(train)
    verse_aksharas = {a for p in poems for ln in p for w in _telugu_words(ln) for a in aksharas(w)}

    table = []
    for label in runs:
        for mode in MODES:
            ks = sorted(k for k in keys if rows[label][k]["mode"] == mode)
            rs = [rows[label][k] for k in ks]
            n = len(rs)
            ok = sum(r["status"] == "complete" and all((r.get("eval") or {}).get(x) for x in
                                                        ("gana_strict", "prasa_strict", "yati_strict")) for r in rs)
            dead = sum(r["status"] == "dead_end" for r in rs)
            toks = [e for k in ks for e in traces[label][k] if e.get("how") in ("sample", "accept", "alive", "forced_nl")]
            logp = statistics.fmean(e["logp"] for e in toks)
            judged = [e for e in toks if e.get("top") and e["top"][0][3] is not None]
            over = sum(e["top"][0][3] is False for e in judged) / len(judged)
            vm = statistics.fmean(e["valid_mass"] for e in toks if e.get("valid_mass") is not None)
            cls, unseen, single, words = Counter(), 0, 0, 0
            for r in rs:
                for w in _telugu_words(r["text"]):
                    words += 1
                    cls[scorer.classify(w)] += 1
                    ak = aksharas(w)
                    unseen += any(a not in verse_aksharas for a in ak)
                    single += len(ak) == 1
            rep = sum(((r.get("eval") or {}).get("duplicate_lines") or 0) > 0 for r in rs)
            table.append({"run": label, "mode": mode, "poems": n, "in_meter": ok, "dead_ends": dead,
                          "logp": logp, "overridden": over, "valid_mass": vm,
                          "corpus_words": cls["corpus word"] / words, "unseen_akshara_words": unseen / words,
                          "junk_words": cls["junk (MAF ≤ 2)"] / words, "single_akshara_words": single / words,
                          "repeated_line": rep / n, "tokens": statistics.fmean(r["n_tokens"] for r in rs),
                          "seconds": statistics.fmean(r["seconds"] for r in rs)})
    head = ("| run | strategy | poems | in meter | dead ends | logp | overridden | valid mass | corpus words | "
            "unseen-akshara words | junk words (MAF ≤ 2) | 1-akshara words | repeated line | tokens | s |")
    lines = [f"Same {len(keys)} keys in every run.", "", head, "|" + "---|" * 15]
    for t in table:
        lines.append(f"| {t['run']} | {t['mode']} | {t['poems']} | {t['in_meter']} | {t['dead_ends']} | {t['logp']:.2f} | "
                     f"{100 * t['overridden']:.0f}% | {t['valid_mass']:.2f} | {100 * t['corpus_words']:.1f}% | "
                     f"{100 * t['unseen_akshara_words']:.1f}% | {100 * t['junk_words']:.1f}% | "
                     f"{100 * t['single_akshara_words']:.1f}% | {100 * t['repeated_line']:.0f}% | {t['tokens']:.0f} | {t['seconds']:.1f} |")
    md = "\n".join(lines) + "\n"
    out.write_text(md, encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(table, ensure_ascii=False, indent=1), encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
