"""Rubric v2 (questions 11–12): v1 ratings are reopened for the new questions only, and nothing recorded is lost."""
import json
import sqlite3
import time

from padya_eval import assignment, db
from padya_eval.rubric import BY_KEY, QUESTIONS, RUBRIC_VERSION
from padya_eval.store import PoemStore


def _store(tmp_path, n=3):
    poems = [{"id": f"he_{i:04d}", "meter": "kandamu", "meter_te": "కందము", "meters": ["kandamu"], "lines": [],
              "units": [], "bhavam": None, "prasa_applicable": True, "hidden": {"source_dataset": "x"}}
             for i in range(n)]
    (tmp_path / "poems.json").write_text(json.dumps({"dataset": "d", "pool": "p", "poems": poems}), encoding="utf-8")
    return PoemStore(tmp_path)


def _conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(db.SCHEMA)
    conn.execute("INSERT INTO annotators(id, username, created_at) VALUES (1, 'a', 'now')")
    return conn


V1 = {q.key: (None if q.key == "bhavam" else 3 if q.kind == "likert" else 1) for q in QUESTIONS[:10]}


def test_rubric_v2_adds_two_questions_with_their_labels():
    assert RUBRIC_VERSION == "2" and [q.number for q in QUESTIONS] == list(range(1, 13))
    assert BY_KEY["register"].label(1).startswith("గ్రాంథికం") and BY_KEY["register"].label(0).startswith("ఆధునికం")
    assert BY_KEY["ai_generated"].label(1).startswith("అవును")
    assert [q.key for q in QUESTIONS[:10]] == ["readability", "comprehension", "lexical", "bhavam", "chandassu",
                                                "prasa", "yati", "shabdalankara", "arthalankara", "poetic"]


def test_a_v1_rating_is_reopened_before_new_poems_and_then_left_alone(tmp_path):
    store, conn = _store(tmp_path), _conn()
    me = {"id": 1, "username": "a"}
    db.save_annotation(conn, 1, "he_0002", V1, "first pass", 90.0, "1")
    assert assignment.incomplete_ids(conn, store, 1) == {"he_0002"}
    pick = lambda: assignment._select(conn, store, me, k=None, claim_ttl_s=1800, calibration=[], now=time.time())
    assert pick() == "he_0002"                          # reopened first: only questions 11–12 are missing
    db.save_annotation(conn, 1, "he_0002", {**V1, "register": 1, "ai_generated": 0}, "first pass", 20.0, "2")
    assert assignment.incomplete_ids(conn, store, 1) == set()
    assert pick() in {"he_0000", "he_0001"}              # now a new poem


def test_reopening_keeps_the_first_version_in_history(tmp_path):
    conn = _conn()
    db.save_annotation(conn, 1, "he_0001", V1, "first pass", 90.0, "1")
    db.save_annotation(conn, 1, "he_0001", {**V1, "register": 0, "ai_generated": 1}, "first pass", 15.0, "2")
    hist = conn.execute("SELECT answers, duration_s, rubric_version, revisions FROM annotation_history").fetchall()
    assert len(hist) == 1
    assert json.loads(hist[0]["answers"]) == V1 and hist[0]["duration_s"] == 90.0 and hist[0]["rubric_version"] == "1"
    now = conn.execute("SELECT answers, rubric_version, revisions FROM annotations").fetchone()
    assert json.loads(now["answers"])["register"] == 0 and now["rubric_version"] == "2" and now["revisions"] == 2
