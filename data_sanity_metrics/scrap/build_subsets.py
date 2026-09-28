"""Step 0 — rebuild the paper's corpus subsets from dwipada_consolidated.json.

The paper's 27,881-couplet "master" corpus is not stored as its own file any
more. It is the Schema-A (dedup) records that pass the paper's own analyser
(dwipada_analyser.analyze_dwipada -> is_valid_dwipada). This script runs that
analyser over every record, stores the per-record verdicts, and checks the
per-source counts against Table 3.

Writes
    outputs/subsets.json                       ids of all / schema_a / master
    outputs/cache/paper_analyser_verdicts.json per-record verdicts (all 34,134)

Run:  python build_subsets.py
"""
import json
from collections import Counter

import config
from common.dataset import file_sha256, load_records, source_of
from common.io import print_table
from common.scanners import paper_verdict


def main():
    records = load_records()
    print(f"dataset: {config.DATASET_PATH}  ({len(records):,} records)")

    verdicts = [paper_verdict(r["poem"]) for r in records]

    ids_all = [r["id"] for r in records]
    ids_schema_a = [r["id"] for r in records if "chandassu_analysis" in r]
    ids_master = [i for i in ids_schema_a if verdicts[i]["valid"]]

    # Table 3 comparison: master count per source
    by_source = Counter(source_of(records[i]) for i in ids_master)
    raw_by_source = Counter(source_of(records[i]) for i in ids_schema_a)
    rows = []
    for src, paper_n in config.PAPER["table3_master_by_source"].items():
        ours = len(ids_master) if src == "total" else by_source.get(src, 0)
        raw = len(ids_schema_a) if src == "total" else raw_by_source.get(src, 0)
        rows.append([src, raw, ours, paper_n, "ok" if ours == paper_n else "DIFF"])
    print("\nTable 3 reproduction (schema_a = dedup set, before the analyser filter)")
    print_table(["source", "schema_a", "master (ours)", "master (paper)", ""], rows)

    rejected = [i for i in ids_schema_a if not verdicts[i]["valid"]]
    print(f"\nschema_a records rejected by the analyser: {len(rejected)}")
    print(f"schema_b records (no analysis) that pass: "
          f"{sum(verdicts[i]['valid'] for i in ids_all if 'chandassu_analysis' not in records[i])}"
          f" of {len(ids_all) - len(ids_schema_a)}")

    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    (config.OUTPUT_DIR / "subsets.json").write_text(json.dumps({
        "dataset_sha256": file_sha256(config.DATASET_PATH),
        "counts": {"all": len(ids_all), "schema_a": len(ids_schema_a), "master": len(ids_master)},
        "master_by_source": dict(by_source),
        "schema_a_by_source": dict(raw_by_source),
        "ids": {"all": ids_all, "schema_a": ids_schema_a, "master": ids_master},
    }))
    (config.CACHE_DIR / "paper_analyser_verdicts.json").write_text(json.dumps(verdicts))
    print(f"\nwrote outputs/subsets.json  (master = {len(ids_master):,})")


if __name__ == "__main__":
    main()
