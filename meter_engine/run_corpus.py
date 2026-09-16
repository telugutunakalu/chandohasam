#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_corpus.py — evaluate the prāsa of every poem in a poems JSON corpus
(dataset/bhagavatam.json layout) with prasa_engine, and write

    <out>_results.jsonl   one record per poem: verdict, label, classifications, violations, per-line prāsa data
    <out>_results.csv     the same, flattened for spreadsheets
    <out>_summary.md      aggregate tables (by metre, by named prāsa variety, by violation rule, failing verses)

Usage
    python3 meter_engine/run_corpus.py --dataset dataset/bhagavatam.json --out meter_engine/corpus_runs/bhagavatam
    python3 meter_engine/run_corpus.py --dataset ... --out ... --profile relaxed --limit 500

Prose records (form == "prose": వచనము, గద్య, దండకము) are skipped.  Every verse
record is evaluated; metres whose lakṣaṇam has no prāsa (సీసము, తేటగీతి,
ఆటవెలది, శ్లోకము) are still run but reported separately as "incidental".
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import prasa_engine as pe  # noqa: E402

# ---------------------------------------------------------------------------
# Metre table: prāsa eligibility (Notes/Prasa.md "Meter Eligibility" + meter_rules.yaml)
# and how the corpus prints the pādas.
#   layout "lines"     : every printed line is a pāda
#   layout "odd_lines" : pādas are printed as two half-lines each; the odd lines open the pādas
#   layout "pairs"     : same as odd_lines but the halves are re-joined (8 printed lines = 4 pādas)
# ---------------------------------------------------------------------------
METRES = {
    "కందము":              {"prasa": True,  "layout": "lines",     "class": "jati",  "meter": "kandamu"},
    "మత్తేభవిక్రీడితము":   {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "mattebhavikriditamu"},
    "చంపకమాల":            {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "champakamala"},
    "ఉత్పలమాల":           {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "utpalamala"},
    "శార్దూలవిక్రీడితము":  {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "sardulavikriditamu"},
    "మత్తకోకిల":           {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "mattakokilamu"},
    "తరలము":              {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": None},
    "మాలిని":              {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": None},
    "ఇంద్రవజ్రము":         {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "indravajra"},
    "ఉపేంద్రవజ్రము":       {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "upendravajra"},
    "కవిరాజవిరాజితము":     {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": None},
    "స్రగ్ధర":             {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "sragdhara"},
    "మహాస్రగ్ధర":          {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "mahasragdhara"},
    "ఉత్సాహము":            {"prasa": True,  "layout": "lines",     "class": "jati",  "meter": "utsahamu"},
    "భుజంగప్రయాతము":       {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "bhujangaprayatamu"},
    "మంగళమహశ్రీ":          {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": None},
    "వనమయూరము":            {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": None},
    "స్రగ్విణి":            {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "sragvini"},
    "తోటకము":              {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "totakamu"},
    "పంచచామరము":           {"prasa": True,  "layout": "lines",     "class": "sama_vritta", "meter": "pamcacamaramu"},
    "లయగ్రాహి":            {"prasa": True,  "layout": "pairs",     "class": "sama_vritta", "meter": None},
    "లయవిభాతి":            {"prasa": True,  "layout": "pairs",     "class": "sama_vritta", "meter": None},
    "మానిని":              {"prasa": True,  "layout": "pairs",     "class": "sama_vritta", "meter": None},
    # no prāsa in the lakṣaṇam — evaluated only to report incidental prāsa
    "సీసము":              {"prasa": False, "layout": "odd_lines", "class": "upajati", "meter": "seesamu"},
    "తేటగీతి":             {"prasa": False, "layout": "lines",     "class": "upajati", "meter": "tetagiti"},
    "ఆటవెలది":             {"prasa": False, "layout": "lines",     "class": "upajati", "meter": "ataveladi"},
    "శ్లోకము":             {"prasa": False, "layout": "lines",     "class": "sanskrit_sloka", "meter": None},
}


def padas_for(record: dict) -> list[str]:
    lines = [ln for ln in record["verse"] if ln and ln.strip()]
    spec = METRES.get(record.get("metre"), {"layout": "lines"})
    if spec["layout"] == "odd_lines":
        body = lines[:8] if len(lines) >= 8 else lines          # a 12-line సీసము carries its ఎత్తుగీతి after line 8
        return body[0::2]
    if spec["layout"] == "pairs":
        if len(lines) % 2 == 0 and len(lines) >= 6:
            return [lines[i] + " " + lines[i + 1] for i in range(0, len(lines), 2)]
        return lines
    return lines


def evaluate_record(record: dict, rs: pe.Ruleset, profile: str) -> dict:
    spec = METRES.get(record.get("metre"))
    padas = padas_for(record)
    out = {
        "id": record["id"], "skandha": record.get("skandha"), "poem_number": record.get("poem_number"),
        "sub_number": record.get("sub_number"), "metre": record.get("metre"), "metre_code": record.get("metre_code"),
        "known_metre": spec is not None, "prasa_required": bool(spec["prasa"]) if spec else None,
        "layout": spec["layout"] if spec else "lines", "printed_lines": len(record["verse"]), "padas": len(padas),
    }
    try:
        res = pe.evaluate(padas, profile=profile, ruleset=rs, meter=(spec or {}).get("meter"),
                          meter_class=(spec or {}).get("class"))
    except Exception as exc:  # keep the run going; the record is reported
        out.update({"error": f"{type(exc).__name__}: {exc}"})
        return out
    strict = res.min_profile is not None and rs.profile_order.index(res.min_profile) <= 0
    relaxed = res.min_profile is not None and rs.profile_order.index(res.min_profile) <= 1
    historical = res.min_profile is not None
    out.update({
        "error": res.error,
        "min_profile": res.min_profile,
        "matched_strict": strict, "matched_relaxed": relaxed, "matched_historical": historical,
        "prasa_consonant": res.prasa_consonant, "label_te": res.label_te, "label_en": res.label_en,
        "classifications": [c["rule"] for c in res.classifications],
        "violation_rules": sorted({v["rule"] for v in res.violations}),
        "hard_violation_rules": sorted({h["rule"] for pv in res.pairs for h in pv["hard_failures"]}
                                       | {t["rule"] for t in res.trail if t["scope"] == "stanza" and t["status"] == "fail"}),
        "first_violation_rule": res.violations[0]["rule"] if res.violations else None,
        "first_violation": res.violations[0]["detail"] if res.violations else None,
        "first_violation_scope": res.violations[0]["scope"] if res.violations else None,
        "pairs_total": len(res.pairs),
        "pairs_ok": sum(1 for pv in res.pairs if pv["min_profile"] is not None),
        "readings": sorted({ln["reading"] for ln in res.lines}),
        "lines": [{"n": ln["index"], "purva": ln["purva"], "prasa": ln["prasa"], "onset": pe.render_onset(ln["onset"]) or ln["vowel"],
                   "vowel": ln["vowel"], "purva_weight": ln["purva_weight_positional"],
                   "bindu_before": ln["purva_purnabindu"], "visarga_before": ln["purva_visarga"],
                   "ardhabindu_before": ln["ardhabindu_before"], "fused": pe.render_onset(ln["fused_from_purva"])}
                  for ln in res.lines],
        "dvyakshara": any(t["rule"] == "PRASA-DEFECT-ADHIKA" and t["status"] == "info" for t in res.trail),
        "santa_pattern": any(t["rule"] == "PRASA-DEFECT-SANTA" for t in res.trail),
    })
    return out


def write_outputs(rows: list[dict], out_prefix: Path, rs: pe.Ruleset, elapsed: float, dataset: str, profile: str) -> Path:
    out_prefix.parent.mkdir(parents=True, exist_ok=True)
    jsonl = out_prefix.with_name(out_prefix.name + "_results.jsonl")
    with open(jsonl, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    csv_path = out_prefix.with_name(out_prefix.name + "_results.csv")
    cols = ["id", "skandha", "poem_number", "metre", "metre_code", "prasa_required", "padas", "prasa_aksharas",
            "prasa_consonant", "label_te", "min_profile", "matched_strict", "matched_relaxed", "matched_historical",
            "classifications", "violation_rules", "hard_violation_rules", "pairs_ok", "pairs_total",
            "first_violation_rule", "first_violation_scope", "first_violation", "readings", "error"]
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({
                **{k: r.get(k) for k in cols if k not in ("prasa_aksharas", "classifications", "violation_rules", "hard_violation_rules", "readings")},
                "prasa_aksharas": "|".join(ln["prasa"] for ln in r.get("lines", [])),
                "classifications": "|".join(r.get("classifications", [])),
                "violation_rules": "|".join(r.get("violation_rules", [])),
                "hard_violation_rules": "|".join(r.get("hard_violation_rules", [])),
                "readings": "|".join(r.get("readings", [])),
            })
    digest = hashlib.sha256(jsonl.read_bytes()).hexdigest()
    summary = out_prefix.with_name(out_prefix.name + "_summary.md")
    summary.write_text(render_summary(rows, rs, elapsed, dataset, profile, jsonl.name, digest), encoding="utf-8")
    return summary


def _pct(n: int, d: int) -> str:
    return f"{100.0 * n / d:.1f}%" if d else "–"


def render_summary(rows, rs, elapsed, dataset, profile, jsonl_name, digest) -> str:
    L = []
    req = [r for r in rows if r.get("prasa_required") and not r.get("error")]
    inc = [r for r in rows if r.get("prasa_required") is False and not r.get("error")]
    errs = [r for r in rows if r.get("error")]
    unknown = [r for r in rows if not r.get("known_metre")]
    L.append("# Prāsa over the Bhāgavatam corpus — run summary\n")
    L.append(f"- dataset: `{dataset}`  ·  poems evaluated: **{len(rows)}** (prose skipped)  ·  runtime {elapsed:.1f}s")
    L.append(f"- ruleset: `{rs.path.name}` schema {rs.version}  ·  engine profile for violation listing: `{profile}`")
    L.append(f"- results: `{jsonl_name}` (sha256 `{digest[:16]}…`) — identical bytes on every re-run of the same inputs")
    L.append(f"- prāsa-bearing metres: **{len(req)}** poems  ·  no-prāsa metres (incidental only): **{len(inc)}**  ·  errors: {len(errs)}  ·  unknown metres: {len(unknown)}\n")

    # ---- 1. verdicts by metre
    L.append("## 1. Verdict by metre (prāsa-bearing metres)\n")
    L.append("| metre | poems | strict | relaxed only | historical only | no match | strict % | any-profile % |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    by_m = collections.defaultdict(list)
    for r in req:
        by_m[r["metre"]].append(r)
    def bucket(rs_):
        c = collections.Counter(r["min_profile"] for r in rs_)
        return c["strict"], c["relaxed"], c["historical"], c[None]
    for m, rs_ in sorted(by_m.items(), key=lambda kv: -len(kv[1])):
        s, rl, h, n = bucket(rs_)
        L.append(f"| {m} | {len(rs_)} | {s} | {rl} | {h} | {n} | {_pct(s, len(rs_))} | {_pct(s + rl + h, len(rs_))} |")
    s, rl, h, n = bucket(req)
    L.append(f"| **all** | **{len(req)}** | **{s}** | **{rl}** | **{h}** | **{n}** | **{_pct(s, len(req))}** | **{_pct(s + rl + h, len(req))}** |\n")

    # ---- 2. named prāsa varieties
    L.append("## 2. Named prāsa varieties observed (prāsa-bearing metres, all profiles)\n")
    L.append("| rule | name | status | poems |")
    L.append("|---|---|---|---:|")
    cc = collections.Counter(c for r in req for c in set(r["classifications"]))
    for rid, n in sorted(cc.items(), key=lambda kv: (rs.rule_order.get(kv[0], 999))):
        L.append(f"| {rid} | {rs.name(rid, 'te')} | {rs.status(rid)} | {n} |")
    L.append("")

    # ---- 3. prāsa consonants
    L.append("## 3. Prāsa consonant / cluster frequency (matched poems, prāsa-bearing metres)\n")
    pc = collections.Counter(r["prasa_consonant"] for r in req if r["min_profile"] and r["prasa_consonant"])
    top = pc.most_common(40)
    L.append("| onset | poems | onset | poems | onset | poems | onset | poems |")
    L.append("|---|---:|---|---:|---|---:|---|---:|")
    for i in range(0, len(top), 4):
        chunk = top[i:i + 4]
        cells = []
        for k, v in chunk:
            cells += [k, str(v)]
        while len(cells) < 8:
            cells += ["", ""]
        L.append("| " + " | ".join(cells) + " |")
    simple = sum(v for k, v in pc.items() if "్" not in k)
    clusters = sum(v for k, v in pc.items() if "్" in k)
    L.append(f"\nsimple consonant prāsa: {simple} poems · conjunct prāsa: {clusters} poems · distinct onsets: {len(pc)}\n")

    # ---- 4. violations
    L.append("## 4. Violations (prāsa-bearing metres that match under no profile)\n")
    fails = [r for r in req if r["min_profile"] is None]
    vc = collections.Counter(v for r in fails for v in r["hard_violation_rules"])
    L.append("| rule | name | poems |")
    L.append("|---|---|---:|")
    for rid, n in vc.most_common():
        L.append(f"| {rid} | {rs.name(rid, 'en')} | {n} |")
    ortho = [r for r in req if "PRASA-MAITRI-RA-RRA-ORTHO" in r["classifications"]]
    none_rhyme = [r for r in fails if r["pairs_ok"] == 0]
    L.append("")
    L.append(f"- ర/ఱ pairs accepted as an orthographic relaxation (PRASA-MAITRI-RA-RRA-ORTHO, project decision "
             f"2026-09-13): {len(ortho)} poems; they count as `relaxed`, and the trail names the superseded treatise "
             f"rule PRASA-VAIRA-RA-RRA. Set that rule's status back to forbidden in prasa_rules.yaml to restore the "
             f"treatise verdict.")
    L.append(f"- poems where NO pair of lines rhymes at all (pairs_ok = 0): {len(none_rhyme)} — usually a metre label or "
             f"line-layout problem in the source rather than a prāsa fault"
             + (": " + ", ".join(r["id"] for r in none_rhyme) if none_rhyme else ""))
    L.append("")
    L.append("### 4.1 Every non-matching poem\n")
    L.append("| id | metre | prāsa aksharas | pairs ok | rule | detail |")
    L.append("|---|---|---|---:|---|---|")
    for r in fails:
        aks = " · ".join(ln["prasa"] for ln in r["lines"])
        detail = (r["first_violation"] or "").replace("|", "¦")
        L.append(f"| {r['id']} | {r['metre']} | {aks} | {r['pairs_ok']}/{r['pairs_total']} | {r['first_violation_rule'] or ''} | {detail} |")
    L.append("")

    # ---- 5. relaxed / historical
    L.append("## 5. Poems that need a relaxation (min_profile = relaxed or historical)\n")
    L.append("| id | metre | prāsa aksharas | min_profile | label |")
    L.append("|---|---|---|---|---|")
    for r in [r for r in req if r["min_profile"] in ("relaxed", "historical")]:
        aks = " · ".join(ln["prasa"] for ln in r["lines"])
        L.append(f"| {r['id']} | {r['metre']} | {aks} | {r['min_profile']} | {r['label_te']} |")
    L.append("")

    # ---- 6. readings / notes
    dr = [r for r in req if "druta_sandhi" in r.get("readings", [])]
    dv = sum(1 for r in req if r.get("dvyakshara"))
    L.append("## 6. Notes\n")
    L.append(f"- poems matched only under the druta-sandhi reading (PRASA-POS-07): {len(dr)}" + (" — " + ", ".join(r["id"] for r in dr[:20]) if dr else ""))
    L.append(f"- poems whose 3rd aksharas also rhyme (dvyakṣara prāsa, informational): {dv}")

    # ---- 7. incidental prāsa in no-prāsa metres
    L.append("\n## 7. Incidental prāsa in metres without a prāsa rule (informational)\n")
    L.append("| metre | poems | would match strict | would match relaxed/historical | no prāsa |")
    L.append("|---|---:|---:|---:|---:|")
    by_i = collections.defaultdict(list)
    for r in inc:
        by_i[r["metre"]].append(r)
    for m, rs_ in sorted(by_i.items(), key=lambda kv: -len(kv[1])):
        s, rl, h, n = bucket(rs_)
        L.append(f"| {m} | {len(rs_)} | {s} | {rl + h} | {n} |")
    if errs:
        L.append("\n## 8. Records with errors\n")
        for r in errs:
            L.append(f"- {r['id']} ({r['metre']}): {r['error']}")
    if unknown:
        L.append("\n## 9. Unknown metres (evaluated with default layout)\n")
        for m, n in collections.Counter(r["metre"] for r in unknown).items():
            L.append(f"- {m}: {n}")
    return "\n".join(L) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run prasa_engine over a poems corpus")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--out", required=True, help="output prefix, e.g. meter_engine/corpus_runs/bhagavatam")
    ap.add_argument("--profile", default="strict", choices=pe.PROFILE_ORDER, help="profile used for the violation text")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)
    rs = pe.load_ruleset()
    data = json.load(open(args.dataset, encoding="utf-8"))
    verses = [d for d in data if d.get("form") == "verse" and d.get("verse")]
    if args.limit:
        verses = verses[:args.limit]
    t0 = time.time()
    rows = [evaluate_record(d, rs, args.profile) for d in verses]
    elapsed = time.time() - t0
    summary = write_outputs(rows, Path(args.out), rs, elapsed, args.dataset, args.profile)
    req = [r for r in rows if r.get("prasa_required") and not r.get("error")]
    c = collections.Counter(r["min_profile"] for r in req)
    print(f"poems: {len(rows)}  prāsa-bearing: {len(req)}  strict={c['strict']} relaxed={c['relaxed']} "
          f"historical={c['historical']} none={c[None]}  errors={sum(1 for r in rows if r.get('error'))}  "
          f"time={elapsed:.1f}s")
    print(f"summary: {summary}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
