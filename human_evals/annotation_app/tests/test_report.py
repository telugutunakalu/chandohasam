# -*- coding: utf-8 -*-
"""The agreement report built from stored annotations, and the command-line export."""
import json

import pytest

from padya_eval import db, report
from padya_eval.rubric import QUESTIONS


def ann(user, eval_id, value_likert, value_binary, **override):
    answers = {q.key: (value_likert if q.kind == "likert" else value_binary) for q in QUESTIONS}
    answers.update(override)
    return {"username": user, "eval_id": eval_id, "answers": answers, "comments": "", "duration_s": 30.0,
            "revisions": 1, "rubric_version": "1", "created_at": "2026-10-13T10:00:00+00:00",
            "updated_at": "2026-10-13T10:00:00+00:00"}


def test_perfect_agreement_gives_alpha_one(store):
    ids = store.ids[:8]
    rows = [ann(u, e, 1 + i % 5, i % 2) for i, e in enumerate(ids) for u in ("a", "b", "c")]
    rep = report.agreement_report(rows, store, k=3, calibration=ids[:2])
    for q in rep["questions"]:
        assert q["alpha"] == 1.0 and q["pct_agreement"] == 1.0 and q["n_paired_units"] == 8
    assert rep["calibration"][0]["n_paired_units"] == 2
    assert {a["username"]: a["calibration_done"] for a in rep["annotators"]} == {"a": 2, "b": 2, "c": 2}


def test_not_applicable_answers_are_excluded(store):
    ids = store.ids[:4]
    rows = [ann(u, e, 3, 1, bhavam=None) for e in ids for u in ("a", "b")]
    rep = report.agreement_report(rows, store, k=2, calibration=[])
    bhavam = next(q for q in rep["questions"] if q["key"] == "bhavam")
    assert bhavam["n_ratings"] == 0 and bhavam["alpha"] is None
    assert rep["calibration"] == []


def test_outlier_annotator_is_flagged(store):
    ids = store.ids[:12]
    rows = []
    for i, e in enumerate(ids):
        good = 1 + i % 5
        rows += [ann("a", e, good, i % 2), ann("b", e, good, i % 2), ann("x", e, 6 - good, 1 - i % 2)]
    rep = report.agreement_report(rows, store, k=3, calibration=[])
    by_user = {a["username"]: a for a in rep["annotators"]}
    assert by_user["x"]["loo_alpha_delta"] > 0.3 > by_user["a"]["loo_alpha_delta"]
    assert by_user["x"]["mean_kappa"] < by_user["a"]["mean_kappa"]


def test_binary_items_report_ac1_and_prevalence(store):
    ids = store.ids[:10]
    rows = [ann(u, e, 3, 1) for e in ids for u in ("a", "b")]
    rows[-1]["answers"]["chandassu"] = 0
    rep = report.agreement_report(rows, store, k=2, calibration=[])
    ch = next(q for q in rep["questions"] if q["key"] == "chandassu")
    assert ch["prop_yes"] == pytest.approx(0.95) and ch["gwet_ac1"] > 0.85 and ch["fleiss_kappa"] < 0.1


def test_by_source_and_export_rows(store):
    gen = next(p for p in store.poems if p.hidden["source_dataset"] == "generated")
    bh = next(p for p in store.poems if p.hidden["source_dataset"] == "bhagavatam")
    rows = [ann("a", gen.id, 2, 0), ann("a", bh.id, 5, 1)]
    by = {r["source"]: r for r in report.by_source(rows, store)}
    assert by["generated"]["cells"]["poetic"]["value"] == 2 and by["bhagavatam"]["cells"]["poetic"]["value"] == 5
    out = report.export_rows(rows, store, calibration=[bh.id])
    assert [r["calibration"] for r in out] == [0, 1]
    assert out[0]["source_dataset"] == "generated" and out[0]["author"] == gen.hidden["author"]
    csv_text = report.to_csv(out)
    assert csv_text.splitlines()[0].split(",") == report.EXPORT_FIELDS


def test_markdown_report(store):
    rows = [ann(u, e, 3, 1) for e in store.ids[:3] for u in ("a", "b")]
    md = report.to_markdown(report.agreement_report(rows, store, k=2, calibration=store.ids[:1]))
    assert md.startswith("# Human-evaluation agreement") and "## Calibration set" in md and "| a |" in md


def test_cli_writes_report_files(tmp_path, store):
    path = tmp_path / "annotations.db"
    db.init_db(path, store.fingerprint)
    conn = db.connect(path)
    for u in ("a", "b"):
        who = db.get_or_create_annotator(conn, u)
        for e in store.ids[:5]:
            db.save_annotation(conn, who["id"], e, ann(u, e, 4, 1)["answers"], "", 20.0, "1")
    conn.close()
    out = tmp_path / "reports"
    assert report.main(["--db", str(path), "--out", str(out), "--bootstrap", "100"]) == 0
    rep = json.loads((out / "agreement.json").read_text(encoding="utf-8"))
    assert rep["study"]["annotations"] == 10 and rep["study"]["bootstrap"] == 100
    assert (out / "agreement.md").is_file() and (out / "annotations.csv").read_text(encoding="utf-8").count("\n") == 11
    assert report.main(["--db", str(tmp_path / "missing.db"), "--out", str(out)]) == 1


def test_all_mode_in_report(store):
    rows = [ann(u, e, 3, 1) for e in store.ids[:3] for u in ("a", "b")]
    rep = report.agreement_report(rows, store, k=None, calibration=[])
    assert rep["study"]["ratings_per_poem"] == "all"
    assert "every annotator rates every poem" in report.to_markdown(rep)
