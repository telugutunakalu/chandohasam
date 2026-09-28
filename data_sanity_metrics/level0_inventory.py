"""Level 0 — Dataset inventory and structural checks.

What the four corpora contain, and whether each record is well formed, before
any metric reads them. Per corpus, on the raw records (verse and prose):

    size          records, verse, prose, unique ids
    structure     empty verse; `line_count` equal to the number of lines;
                  a labelled poem's line count inside its metre's `allowed_lines`;
                  seesa pādas written on one line with " - " between the halves
                  (the other files write them as two half-lines);
                  Bhagavatam seesa links (every parent_id / child_id resolves)
    labels        how many poems carry a metre label, and where the label comes from
    annotation    verse poems with a Telugu bhavam (edition or machine), with
                  `bhavam_en`, with a gloss; gloss rows per poem
    machine runs  provenance of `generated`: run, model, rescued, problems, script_fixes
    script purity Telugu fields (verse, bhavam, gloss) with letters of another
                  script; English `bhavam_en` with letters of an Indic script

Writes outputs/level0_inventory.json

Run:  python level0_inventory.py [--datasets vemana chandassu ...]
"""
import argparse
from collections import Counter
import unicodedata

from common.dataset import add_dataset_argument, load_records
from common.io import pct, print_table, save_result


def foreign_letters(text) -> int:
    """Letters or vowel signs outside the Telugu block."""
    return sum(1 for c in text or "" if unicodedata.category(c)[0] in "LM" and not "ఀ" <= c <= "౿")


def indic_letters(text) -> int:
    """Letters of any Indic script (Devanagari to Malayalam), for the English field."""
    return sum(1 for c in text or "" if "ऀ" <= c <= "෿")


def telugu_fields(record) -> list:
    """Every Telugu text of a record: verse, bhavam, gloss words and meanings (edition or machine)."""
    g = record.get("generated") or {}
    texts = list(record.get("verse") or []) + [record.get("bhavam"), g.get("bhavam")]
    for p in (record.get("teeka_pairs") or []) + (g.get("prathipadartham") or []):
        texts += [p.get("word"), p.get("meaning")]
    return texts


def structure(records) -> dict:
    ids = Counter(r["id"] for r in records)
    by_id = {r["id"]: r for r in records}
    labelled = [r for r in records if r.get("metre_roman") and r.get("allowed_lines")]
    return {
        "records": len(records),
        "verse": sum(r.get("form") == "verse" for r in records),
        "prose": sum(r.get("form") == "prose" for r in records),
        "duplicate_ids": sum(n - 1 for n in ids.values() if n > 1),
        "empty_verse": sum(not any((l or "").strip() for l in r.get("verse") or []) for r in records),
        "line_count_mismatch": sum(r.get("line_count") != len(r.get("verse") or []) for r in records),
        "lines_outside_allowed": sum(len(r["verse"]) not in r["allowed_lines"] for r in labelled),
        "seesa_pada_on_one_line": sum(r.get("metre_roman") == "seesamu" and any(" - " in l for l in r["verse"])
                                      for r in records),
        "seesa_parents": sum(bool(r.get("child_id")) for r in records),
        "seesa_children": sum(bool(r.get("parent_id")) for r in records),
        "broken_parent_links": sum(bool(r.get("parent_id")) and r["parent_id"] not in by_id for r in records),
        "broken_child_links": sum(bool(r.get("child_id")) and r["child_id"] not in by_id for r in records),
    }


def labels(records) -> dict:
    verse = [r for r in records if r.get("form") == "verse"]
    return {
        "labelled_verse": sum(bool(r.get("metre_roman")) for r in verse),
        "unlabelled_verse": sum(not r.get("metre_roman") for r in verse),
        "label_source": dict(Counter(r.get("label_source") or ("edition" if r.get("metre_roman") else "none")
                                     for r in verse)),
        "metres": dict(Counter(r.get("metre_roman") for r in verse if r.get("metre_roman")).most_common()),
    }


def annotation(records) -> dict:
    verse = [r for r in records if r.get("form") == "verse"]
    def gen(r):
        return r.get("generated") or {}
    edition = sum(bool((r.get("bhavam") or "").strip()) for r in verse)
    machine = sum(not (r.get("bhavam") or "").strip() and bool((gen(r).get("bhavam") or "").strip()) for r in verse)
    gloss_rows = [len(r.get("teeka_pairs") or gen(r).get("prathipadartham") or []) for r in verse]
    return {
        "bhavam_edition": edition,
        "bhavam_machine": machine,
        "bhavam_en": sum(bool((r.get("bhavam_en") or "").strip()) for r in verse),
        "with_gloss": sum(n > 0 for n in gloss_rows),
        "gloss_rows": sum(gloss_rows),
        "gloss_rows_per_glossed_poem": sum(gloss_rows) / max(1, sum(n > 0 for n in gloss_rows)),
        "bhavam_without_bhavam_en": sum(bool((r.get("bhavam") or gen(r).get("bhavam") or "").strip())
                                        and not (r.get("bhavam_en") or "").strip() for r in verse),
    }


def machine_runs(records) -> dict:
    gens = [r["generated"] for r in records if r.get("generated")]
    return {
        "annotated": len(gens),
        "runs": dict(Counter(g.get("run") for g in gens)),
        "models": dict(Counter(g.get("model") for g in gens)),
        "rescued": sum(bool(g.get("rescued")) for g in gens),
        "with_problems": sum(bool(g.get("problems")) for g in gens),
        "with_script_fixes": sum(bool(g.get("script_fixes")) for g in gens),
    }


def purity(records) -> dict:
    return {
        "records_foreign_letters_in_telugu": sum(any(foreign_letters(t) for t in telugu_fields(r)) for r in records),
        "records_foreign_letters_in_verse": sum(any(foreign_letters(l) for l in r.get("verse") or []) for r in records),
        "records_indic_letters_in_bhavam_en": sum(indic_letters(r.get("bhavam_en")) > 0 for r in records),
    }


def main():
    ap = argparse.ArgumentParser()
    add_dataset_argument(ap)
    args = ap.parse_args()

    result = {}
    for corpus in args.datasets:
        records = load_records(corpus)
        result[corpus] = {"structure": structure(records), "labels": labels(records),
                          "annotation": annotation(records), "machine_runs": machine_runs(records),
                          "purity": purity(records)}
    corpora = list(args.datasets)

    def table(section, keys, title):
        print_table(["", *corpora], [[k, *(result[c][section][k] for c in corpora)] for k in keys], title)

    table("structure", list(result[corpora[0]]["structure"]), "Size and structure (all records)")
    table("labels", ["labelled_verse", "unlabelled_verse"], "Metre labels (verse)")
    for c in corpora:
        print(f"  {c}: label source {result[c]['labels']['label_source']}")
    table("annotation", list(result[corpora[0]]["annotation"]), "Annotation coverage (verse)")
    table("machine_runs", ["annotated", "rescued", "with_problems", "with_script_fixes"],
          "Machine annotation (`generated`)")
    table("purity", list(result[corpora[0]]["purity"]), "Script purity (records)")

    totals = {k: sum(result[c]["annotation"][k] for c in corpora) for k in ("bhavam_edition", "bhavam_machine")}
    verse = sum(result[c]["structure"]["verse"] for c in corpora)
    print(f"\nverse poems: {verse:,}; with a Telugu bhavam: {sum(totals.values()):,} "
          f"({pct(sum(totals.values()), verse):.1f}%), of which edition {totals['bhavam_edition']:,}, "
          f"machine {totals['bhavam_machine']:,}")
    save_result("level0_inventory", result)


if __name__ == "__main__":
    main()
