"""The first phase (data/active_pool.json): its poems come first for every annotator, then the rest of the pool;
progress counts the phase; the study's fingerprint does not change."""
import json
import sqlite3
import time

from padya_eval import assignment, db
from padya_eval.rubric import QUESTIONS
from padya_eval.store import PoemStore


def _data(tmp_path, n=5, active=None):
    poems = [{"id": f"he_{i:04d}", "meter": "kandamu", "meter_te": "కందము", "meters": ["kandamu"], "lines": [],
              "units": [], "bhavam": None, "prasa_applicable": True, "hidden": {"source_dataset": "x"}}
             for i in range(n)]
    (tmp_path / "poems.json").write_text(json.dumps({"dataset": "d", "pool": "p", "poems": poems}), encoding="utf-8")
    if active is not None:
        (tmp_path / "active_pool.json").write_text(json.dumps({"ids": active}), encoding="utf-8")
    return tmp_path


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(db.SCHEMA)
    conn.execute("INSERT INTO annotators(id, username, created_at) VALUES (1, 'a', 'now')")
    return conn


FULL = {q.key: (None if q.key == "bhavam" else 3 if q.kind == "likert" else 1) for q in QUESTIONS}


def test_without_a_phase_the_whole_pool_is_the_phase(tmp_path):
    store = PoemStore(_data(tmp_path))
    assert store.phase_ids == store.ids and len(store.ids) == 5 and store.fingerprint == "d/p/5"


def test_a_phase_keeps_every_poem_servable_and_the_fingerprint(tmp_path):
    store = PoemStore(_data(tmp_path, active=["he_0003", "he_0001", "he_9999"]))
    assert store.phase_ids == ["he_0001", "he_0003"]        # poems.json order; unknown ids ignored
    assert len(store.ids) == 5 and store.fingerprint == "d/p/5"


def test_every_annotator_gets_the_phase_first_then_the_rest(tmp_path):
    store, conn = PoemStore(_data(tmp_path, active=["he_0001", "he_0003"])), _conn()
    me = {"id": 1, "username": "a"}
    pick = lambda: assignment._select(conn, store, me, k=None, claim_ttl_s=1800, calibration=[], now=time.time())
    seen = []
    for _ in range(5):
        e = pick()
        seen.append(e)
        db.save_annotation(conn, 1, e, FULL, "", 10.0, "2")
    assert set(seen[:2]) == {"he_0001", "he_0003"} and set(seen[2:]) == {"he_0000", "he_0002", "he_0004"}
    assert pick() is None


def test_progress_counts_the_phase(tmp_path):
    store, conn = PoemStore(_data(tmp_path, active=["he_0000", "he_0002"])), _conn()
    db.save_annotation(conn, 1, "he_0000", FULL, "", 10.0, "2")
    db.save_annotation(conn, 1, "he_0004", FULL, "", 10.0, "2")
    p = assignment.study_progress(conn, store, k=1)
    assert p["poems"] == 2 and p["complete"] == 1 and p["ratings_needed"] == 1
