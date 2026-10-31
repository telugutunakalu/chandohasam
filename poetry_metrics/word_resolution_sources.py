"""Word resolution (../word_resolution_metric) on every poem source of score_sources.py, one JSON per source.

    ../.venv/bin/python -u word_resolution_sources.py     # ≈ 15 s with its ByT5 cache, ≈ 5 min without (CPU) →
                                                          #   outputs/word_resolution/<source>.json, summary.json, reports/word_resolution_sources.md

The sources are score_sources.py's own (the four dataset files; study 1 by source; study 2 by model; every Gemini
poem of ../metrics/initial_evals), tokenised by
the resolver itself (`WordResolver.tokens`: the recorded line-end joins, the spacing rules). Each word type is
resolved exactly as ../final_report_metrics/score_resolution.py does it, with that script's own functions: the live
path (lexicon, then ByT5's four beams), the resolver's verified gate, and the corpus table. A type that script already
resolved (its scores/resolution_types.jsonl, read only) keeps that answer; the rest go through the same passes here,
ByT5 on the CPU, its analyses cached in cache/word_resolution_byt5.json (gitignored).

Readings per poem (shares of its tokens), as in ../final_report_metrics:
- `resolved_live_verified`: the live path, a ByT5 analysis counted only when every headword it names is a lexicon
  entry. The paper's *resolved*, and the reading to compare sources by.
- `resolved_live`: the live path as shipped (a ByT5 analysis counts without its headwords being looked up).
- `resolved_live_strict`: the live path without ByT5 and bare-stem readings: the dictionary alone.
- `resolved`, `resolved_verified`, `resolved_strict`: the same three with the corpus table answering first. The table
  holds the words of the dataset's own poems, so these favour them.
- `in_table`, `attested`: the token is a corpus word type; it is resolved or attested in a dictionary or the glossary.

Each source file holds, per reading, the summary over poems (mean, sd, quantiles) and the token-weighted share, the
live path's class shares, the most frequent unresolved words, the same by metre, and every poem's readings. Study 2's
file also compares each poem with the gold poem of its prompt.
"""
from __future__ import annotations

import collections
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path[:0] = [str(HERE), str(REPO / "final_report_metrics")]

import score_resolution as sr                                                # noqa: E402  (adds the resolver's paths)
import score_sources as ss                                                   # noqa: E402

TYPES = REPO / "final_report_metrics" / "scores" / "resolution_types.jsonl"
CACHE = HERE / "cache" / "word_resolution_byt5.json"        # ByT5Splitter derives …_nbest4.json from it
OUT = HERE / "outputs" / "word_resolution"
REPORT = HERE / "reports" / "word_resolution_sources.md"
READINGS = ["resolved_live_verified", "resolved_live", "resolved_live_strict", "resolved", "resolved_verified",
            "resolved_strict", "in_table", "attested"]


def strict(res: dict) -> bool:
    return res["resolved"] and res["class"] != "resolved-by-byt5" and not res["source"].startswith("lexicon:stem")


def resolve_types(words: set) -> dict:
    """word -> {default, live, verified, live_verified, attested}, as score_resolution.py writes them."""
    from resolve import STRONG
    known = {}
    for line in open(TYPES, encoding="utf-8"):
        r = json.loads(line)
        if r["word"] in words:
            known[r["word"]] = r
    todo = sorted(words - set(known))
    print(f"{len(words):,} types: {len(known):,} already resolved by score_resolution.py, {len(todo):,} to resolve",
          flush=True)
    if not todo:
        return known
    table = sr.R.table
    live, attested = {}, {}
    for w, res, att in sr.lexicon_pass(todo):
        live[w], attested[w] = res, att
    need = [w for w in todo if live[w]["class"] == "unresolved"]
    if need:
        from byt5_splitter import ByT5Splitter
        CACHE.parent.mkdir(exist_ok=True)
        sp = ByT5Splitter(checkpoint=sr.WR / "models" / "byt5_distill_v2", device="cpu", cache=CACHE)
        sr.NBEST = dict(zip(need, sp.headwords_nbest(need, n=sr.BEAMS)))
        sp.save_nbest()
    live_ver = dict(live)
    for w, res, ver in sr.byt5_pass(need):
        live[w], live_ver[w] = res, ver
    table_ok = dict(sr.table_pass([w for w in todo if w in table and table[w][0] == "resolved-by-byt5"]))
    print(f"lexicon left {len(need):,} for ByT5: {sum(live[w]['resolved'] for w in need):,} resolved as shipped, "
          f"{sum(live_ver[w]['resolved'] for w in need):,} verified", flush=True)
    for w in todo:
        if w in table:
            cls, an, conf, src, cnt = table[w]
            default = {"class": cls, "resolved": cls in STRONG, "source": f"table:{src}", "analysis": an,
                       "confidence": conf, "corpus_count": cnt}
            verified = table_ok[w] if cls == "resolved-by-byt5" else default["resolved"]
        else:
            default, verified = live[w], live_ver[w]["resolved"]
        known[w] = {"word": w, "default": default, "live": live[w], "verified": verified,
                    "live_verified": live_ver[w]["resolved"], "attested": attested[w]}
    return known


def poem_readings(tokens: list, types: dict) -> dict:
    n = len(tokens)
    if not n:
        return {"n_tokens": 0, **{k: None for k in READINGS}, "classes_live": {}, "unresolved": []}
    t = [types[w] for w in tokens]
    count = {
        "resolved_live_verified": sum(x["live_verified"] for x in t),
        "resolved_live": sum(x["live"]["resolved"] for x in t),
        "resolved_live_strict": sum(strict(x["live"]) for x in t),
        "resolved": sum(x["default"]["resolved"] for x in t),
        "resolved_verified": sum(x["verified"] for x in t),
        "resolved_strict": sum(strict(x["default"]) for x in t),
        "in_table": sum(x["default"]["source"].startswith("table:") for x in t),
        "attested": sum(x["default"]["resolved"] or (x["default"]["source"].startswith("table:")
                                                     and x["default"]["class"] != "unresolved") or x["attested"]
                        for x in t),
    }
    return {"n_tokens": n, **{k: round(v / n, 4) for k, v in count.items()}, "_count": count,
            "classes_live": dict(collections.Counter(x["live"]["class"] for x in t)),
            "unresolved": [w for w, x in zip(tokens, t) if not x["live_verified"]]}


def summarise(rows: list) -> dict:
    tokens = sum(r["n_tokens"] for r in rows)
    out = {"n_poems": len(rows), "n_tokens": tokens, "readings": {}}
    for k in READINGS:
        out["readings"][k] = {"over_poems": ss.describe([r[k] for r in rows]),
                              "over_tokens": round(sum(r["_count"][k] for r in rows if r["n_tokens"]) / tokens, 4)
                              if tokens else None}
    classes = collections.Counter()
    for r in rows:
        classes.update(r["classes_live"])
    out["classes_live"] = {c: {"tokens": n, "share": round(n / tokens, 4)} for c, n in classes.most_common()}
    unresolved = collections.Counter(w for r in rows for w in r["unresolved"])
    out["unresolved_live_verified"] = {"tokens": sum(unresolved.values()), "types": len(unresolved),
                                       "most_frequent": unresolved.most_common(40)}
    return out


def by_metre(rows: list, key: str = "metre") -> dict:
    groups = collections.defaultdict(list)
    for r in rows:
        groups[str(r[key]) if r[key] is not None else "(none)"].append(r)
    return {m: {"n_poems": len(g), "n_tokens": sum(r["n_tokens"] for r in g),
                **{k: ss.describe([r[k] for r in g]).get("mean") for k in READINGS}}
            for m, g in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))}


def against_gold(rows: list, gold: dict) -> dict:
    out = {}
    for k in READINGS:
        d = [r[k] - gold[r["gold_eval_id"]][k] for r in rows
             if r["gold_eval_id"] in gold and r[k] is not None and gold[r["gold_eval_id"]][k] is not None]
        out[k] = {"n_pairs": len(d), "mean_difference": round(statistics.fmean(d), 4) if d else None,
                  "share_above_gold": round(sum(x > 0 for x in d) / len(d), 4) if d else None}
    return out


def report(index: dict) -> str:
    out = ["# Word resolution on every poem source", "",
           "Written by `word_resolution_sources.py` (`outputs/word_resolution/<source>.json`, `summary.json`). Mean "
           "share of a poem's tokens that resolve to dictionary headwords, over the source's poems. **Resolved** is the "
           "live path with the verified ByT5 gate, the paper's reading; *as shipped* counts a ByT5 analysis without "
           "looking its headwords up; *dictionary only* drops ByT5 and bare stems; *with table* lets the corpus table "
           "answer first (it holds the dataset poems' own words). By-metre means, class shares, the most frequent "
           "unresolved words and every poem's readings are in the source's JSON.", "",
           "| source | kind | poems | tokens | **resolved** | as shipped | dictionary only | with table, verified | attested | tokens ByT5 resolves (as shipped) | unresolved types |",
           "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    pct = lambda x: "–" if x is None else f"{100 * x:.1f}%"
    for name, s in index["sources"].items():
        r = s["summary"]["readings"]
        byt5 = s["summary"]["classes_live"].get("resolved-by-byt5", {}).get("share", 0.0)
        out.append(f"| `{name}` | {s['kind']} | {s['summary']['n_poems']} | {s['summary']['n_tokens']:,} | "
                   f"**{pct(r['resolved_live_verified']['over_poems'].get('mean'))}** | "
                   f"{pct(r['resolved_live']['over_poems'].get('mean'))} | "
                   f"{pct(r['resolved_live_strict']['over_poems'].get('mean'))} | "
                   f"{pct(r['resolved_verified']['over_poems'].get('mean'))} | "
                   f"{pct(r['attested']['over_poems'].get('mean'))} | {pct(byt5)} | "
                   f"{s['summary']['unresolved_live_verified']['types']:,} |")
    out.append("")
    s2 = {k: v for k, v in index["sources"].items() if "against_gold" in v}
    if s2:
        out += ["## Study 2 against the gold poems of the same prompts", "",
                "Each model poem minus the study-1 gold poem of its prompt (33 pairs per model), in points of the share "
                "of tokens; in brackets the share of prompts where the model's poem resolves more.", "",
                "| model | **resolved** | as shipped | dictionary only | with table, verified |", "|---|---|---|---|---|"]
        for name, s in s2.items():
            g = s["against_gold"]
            out.append(f"| `{name}` | " + " | ".join(
                f"{100 * g[k]['mean_difference']:+.1f} ({100 * g[k]['share_above_gold']:.0f}%)"
                for k in ("resolved_live_verified", "resolved_live", "resolved_live_strict", "resolved_verified")) + " |")
        out.append("")
    return "\n".join(out)


def main() -> int:
    from resolve import WordResolver
    sr.R = WordResolver(use_byt5=False)
    srcs = ss.sources()
    tokens = {name: [sr.R.tokens(lines) for _, _, _, lines, _ in src["poems"]] for name, src in srcs.items()}
    types = resolve_types({w for ts in tokens.values() for t in ts for w in t})
    rows = {}
    for name, src in srcs.items():
        rows[name] = [{"id": pid, "metre": metre, **extra, **poem_readings(ts, types)}
                      for (pid, _, metre, _, extra), ts in zip(src["poems"], tokens[name])]
    gold = {r["id"]: r for name, rs in rows.items() if name.startswith("human_evals_study1_") for r in rs}
    OUT.mkdir(parents=True, exist_ok=True)
    index = {"readings": READINGS, "primary": "resolved_live_verified", "sources": {}}
    for name, rs in rows.items():
        src = srcs[name]
        doc = {"source": name, "title": src["title"], "family": src["family"], "kind": src["kind"],
               "from": src["from"], "summary": summarise(rs), "by_metre": by_metre(rs)}
        for key in src.get("group_by", []):
            doc[f"by_{key}"] = by_metre(rs, key)
        if name.startswith("human_evals_study2_"):
            doc["against_gold"] = against_gold(rs, gold)
        poems = [{k: v for k, v in r.items() if k not in ("_count", "unresolved")} | {"n_unresolved": len(r["unresolved"])}
                 for r in rs]
        doc["poems"] = "@POEMS@"
        body = ",\n".join("  " + json.dumps(p, ensure_ascii=False, separators=(",", ":")) for p in poems)
        text = json.dumps(doc, ensure_ascii=False, indent=1).replace('"@POEMS@"', "[\n" + body + "\n ]")
        (OUT / f"{name}.json").write_text(text + "\n", encoding="utf-8")
        index["sources"][name] = {k: doc[k] for k in ("title", "family", "kind", "from", "summary")} | (
            {"against_gold": doc["against_gold"]} if "against_gold" in doc else {})
        print(f"{name}: {len(rs)} poems, resolved {doc['summary']['readings']['resolved_live_verified']['over_poems'].get('mean')}",
              flush=True)
    (OUT / "summary.json").write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    REPORT.write_text(report(index) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(HERE)}/ and {REPORT.relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
