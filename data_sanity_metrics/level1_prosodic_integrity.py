"""Level 1 — Prosodic integrity, scanned by meter_engine.

Metric: the share of verse poems that satisfy their labelled metre on every
rule: gaṇa (the lines scan as that metre), prāsa (where the metre requires it)
and yati. Scansion is meter_engine's (see common/scansion.py), under each
profile in config.SCAN_PROFILES.

Per corpus, and per metre within each corpus:
    identified       the engine finds at least one metre the lines fit
    scans as label   the labelled metre is among them (the gaṇa check)
    best is label    ... and it is the engine's first choice
    prāsa, yati      pass rates among the poems that scan as their label
    valid            every rule passes: the level-1 metric
Unlabelled poems (31 in Kuchimanchi) have no label to test and are reported
apart.

Sense checks:
    * agreement by label source. Most Kuchimanchi labels were MADE by this
      engine (label source 'engine'), so they agree by construction; the
      edition's, the heuristic's (Vemana) and the Kaggle corpus's labels are
      the independent tests.
    * how the yati passes: seats accepted per rule, and the share that needs a
      sandhi hypothesis or the prāsa-yati fallback. A pass rate that rests on
      fallbacks certifies less. (Chance pass rates: level1_chance_pass_rates.py.)
    * failing poems per corpus, for manual review.
    * layout: how many seesa poems had pādas written on one line, which are
      split into half-lines before scanning (common/scansion.py).

Writes outputs/level1_prosodic_integrity.json (and the scansion cache).

Run:  python level1_prosodic_integrity.py [--workers 12] [--datasets bhagavatam ...]
"""
import argparse
from collections import Counter

import config
from common.dataset import add_dataset_argument, by_corpus, load_poems
from common.io import pct, print_table, save_result
from common.scansion import layout_split, scan_poems

PROFILES = config.SCAN_PROFILES


def rates(poems, verdicts) -> dict:
    """The level-1 rates of a group of labelled poems."""
    v = [verdicts[p.key] for p in poems]
    scans = [x for x in v if x["scans_as_label"]]
    out = {
        "poems": len(v),
        "identified_pct": pct(sum(x["identified"] for x in v), len(v)),
        "scans_as_label_pct": pct(len(scans), len(v)),
        "best_is_label_pct": pct(sum(x.get("best_is_label", False) for x in v), len(v)),
    }
    for prof in PROFILES:
        with_prasa = [x for x in scans if x[prof].get("prasa_applicable")]
        out[prof] = {
            "prasa_pct": pct(sum(bool(x[prof]["prasa"]) for x in with_prasa), len(with_prasa)),
            "prasa_applicable": len(with_prasa),
            "yati_pct": pct(sum(bool(x[prof]["yati"]) for x in scans), len(scans)),
            "valid_pct": pct(sum(x[prof]["valid"] for x in v), len(v)),
        }
    return out


def yati_usage(poems, verdicts, profile) -> dict:
    """How the yati seats of poems that scan as their label were accepted."""
    seats = [s for p in poems if verdicts[p.key]["scans_as_label"]
             for s in verdicts[p.key][profile].get("yati_seats", [])]
    matched = [s for s in seats if s[3]]
    return {
        "seats": len(seats),
        "matched_pct": pct(len(matched), len(seats)),
        "matched_needing_sandhi_hypothesis_pct": pct(sum(bool(s[4]) for s in matched), len(matched)),
        "matched_by_prasa_yati_pct": pct(sum(bool(s[5]) for s in matched), len(matched)),
        "matched_by_rule": dict(Counter(s[2] for s in matched).most_common(10)),
    }


def failures(poems, verdicts, profile, k=8) -> list:
    """The first k labelled poems that fail, with the reason."""
    out = []
    for p in poems:
        v = verdicts[p.key]
        if v[profile]["valid"]:
            continue
        if not v["scans_as_label"]:
            reason = f"does not scan as {p.metre} (engine: {v.get('best') or 'nothing'})"
        else:
            reason = ", ".join(r for r in ("prasa", "yati") if v[profile][r] is False) or "?"
        out.append({"key": p.key, "metre": p.metre, "reason": reason, "verse": p.text})
        if len(out) == k:
            break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = load_poems(tuple(args.datasets))
    verdicts = scan_poems(poems, args.workers)
    labelled = [p for p in poems if p.metre]
    unlabelled = [p for p in poems if not p.metre]
    result = {"profiles": PROFILES, "yati_sandhi": config.YATI_SANDHI, "corpora": {}, "per_metre": {},
              "by_label_source": {}, "yati_usage": {}, "failures": {},
              "errors": sum("error" in v for v in verdicts.values())}

    # per corpus
    rows = []
    for corpus, group in by_corpus(labelled).items():
        r = rates(group, verdicts)
        r["seesa_split_into_half_lines"] = sum(layout_split(p) for p in group)
        result["corpora"][corpus] = r
        rows.append([corpus, r["poems"], r["identified_pct"], r["scans_as_label_pct"], r["best_is_label_pct"],
                     r["relaxed"]["prasa_pct"], r["relaxed"]["yati_pct"], r["relaxed"]["valid_pct"],
                     r["strict"]["valid_pct"]])
    print_table(["corpus", "poems", "identified %", "scans as label %", "best is label %", "prāsa % (rel)",
                 "yati % (rel)", "VALID % (relaxed)", "VALID % (strict)"], rows,
                "Level 1 — prosodic integrity of labelled verse poems")

    # per metre (metres with at least 10 poems)
    rows = []
    for corpus, group in by_corpus(labelled).items():
        result["per_metre"][corpus] = {}
        for metre, n in Counter(p.metre for p in group).most_common():
            r = rates([p for p in group if p.metre == metre], verdicts)
            result["per_metre"][corpus][metre] = r
            if n >= 10:
                rows.append([corpus, metre, n, r["scans_as_label_pct"], r["relaxed"]["yati_pct"],
                             r["relaxed"]["valid_pct"], r["strict"]["valid_pct"]])
    print_table(["corpus", "metre", "poems", "scans as label %", "yati % (rel)", "valid % (rel)",
                 "valid % (strict)"], rows, "Per metre (metres with >= 10 poems)")

    # sense check: agreement by where the label comes from
    rows = []
    for (corpus, source), n in Counter((p.corpus, p.label_source) for p in labelled).items():
        r = rates([p for p in labelled if p.corpus == corpus and p.label_source == source], verdicts)
        result["by_label_source"][f"{corpus}/{source}"] = r
        rows.append([corpus, source, n, r["scans_as_label_pct"], r["best_is_label_pct"], r["relaxed"]["valid_pct"]])
    print_table(["corpus", "label source", "poems", "scans as label %", "best is label %", "valid % (rel)"],
                rows, "Sense check — agreement by label source ('engine' labels agree by construction)")

    # sense check: how the yati passes
    rows = []
    for corpus, group in by_corpus(labelled).items():
        u = yati_usage(group, verdicts, "relaxed")
        result["yati_usage"][corpus] = u
        rows.append([corpus, u["seats"], u["matched_pct"], u["matched_needing_sandhi_hypothesis_pct"],
                     u["matched_by_prasa_yati_pct"]])
    print_table(["corpus", "yati seats", "matched %", "of matched: sandhi hypothesis %",
                 "of matched: prāsa-yati %"], rows, "Sense check — how the yati passes (relaxed)")

    # unlabelled poems, and failures to review
    result["unlabelled"] = {"poems": len(unlabelled),
                            "identified": sum(verdicts[p.key]["identified"] for p in unlabelled),
                            "identified_as": dict(Counter(verdicts[p.key]["best"] for p in unlabelled))}
    print(f"\nunlabelled poems: {len(unlabelled)}; the engine identifies {result['unlabelled']['identified']}")
    for corpus, group in by_corpus(labelled).items():
        result["failures"][corpus] = failures(group, verdicts, "relaxed")
    print(f"seesa poems split into half-lines before scanning: "
          f"{ {c: r['seesa_split_into_half_lines'] for c, r in result['corpora'].items()} }")
    print(f"scansion errors: {result['errors']}")
    save_result("level1_prosodic_integrity", result)


if __name__ == "__main__":
    main()
