# -*- coding: utf-8 -*-
"""
SQLite storage for the evaluation: annotators, annotations, skips, poem claims and
the calibration set.

One database file holds one study. WAL journaling and a busy timeout let several
gunicorn workers write at once. Every annotation row keeps the answers as JSON,
keyed by the rubric question keys, plus the comments, the time spent and the rubric
version, so an export needs nothing else.
"""
from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS annotators (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    username     TEXT NOT NULL UNIQUE,
    created_at   TEXT NOT NULL,
    last_seen_at TEXT
);
CREATE TABLE IF NOT EXISTS annotations (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    annotator_id   INTEGER NOT NULL REFERENCES annotators(id),
    eval_id        TEXT NOT NULL,
    answers        TEXT NOT NULL,
    comments       TEXT NOT NULL DEFAULT '',
    duration_s     REAL,
    rubric_version TEXT NOT NULL,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL,
    revisions      INTEGER NOT NULL DEFAULT 1,
    UNIQUE (annotator_id, eval_id)
);
CREATE INDEX IF NOT EXISTS annotations_eval ON annotations(eval_id);
CREATE TABLE IF NOT EXISTS skips (
    annotator_id INTEGER NOT NULL REFERENCES annotators(id),
    eval_id      TEXT NOT NULL,
    created_at   TEXT NOT NULL,
    PRIMARY KEY (annotator_id, eval_id)
);
CREATE TABLE IF NOT EXISTS claims (
    annotator_id INTEGER PRIMARY KEY REFERENCES annotators(id),
    eval_id      TEXT NOT NULL,
    claimed_at   REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS calibration (
    position INTEGER PRIMARY KEY,
    eval_id  TEXT NOT NULL UNIQUE
);
"""


class StudyMismatch(RuntimeError):
    """The database was created for a different poem set."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(path), timeout=10, isolation_level=None)   # autocommit; explicit BEGIN when needed
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def init_db(path: str | Path, fingerprint: str) -> None:
    """Create the schema and record which poem set this database belongs to."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = connect(path)
    try:
        conn.execute("PRAGMA journal_mode = WAL")
        conn.executescript(SCHEMA)
        row = conn.execute("SELECT value FROM meta WHERE key = 'fingerprint'").fetchone()
        if row is None:
            conn.execute("INSERT INTO meta(key, value) VALUES ('fingerprint', ?)", (fingerprint,))
            conn.execute("INSERT INTO meta(key, value) VALUES ('created_at', ?)", (now_iso(),))
        elif row["value"] != fingerprint:
            raise StudyMismatch(f"database {path} belongs to poem set {row['value']!r}, "
                                f"but the app loaded {fingerprint!r}; use a new HE_DATABASE file")
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# annotators
# -----------------------------------------------------------------------------
def get_or_create_annotator(conn, username: str) -> sqlite3.Row:
    ts = now_iso()
    conn.execute("INSERT OR IGNORE INTO annotators(username, created_at, last_seen_at) VALUES (?, ?, ?)",
                 (username, ts, ts))
    conn.execute("UPDATE annotators SET last_seen_at = ? WHERE username = ?", (ts, username))
    return conn.execute("SELECT * FROM annotators WHERE username = ?", (username,)).fetchone()


def get_annotator(conn, annotator_id: int) -> Optional[sqlite3.Row]:
    return conn.execute("SELECT * FROM annotators WHERE id = ?", (annotator_id,)).fetchone()


def touch_annotator(conn, annotator_id: int) -> None:
    conn.execute("UPDATE annotators SET last_seen_at = ? WHERE id = ?", (now_iso(), annotator_id))


def list_annotators(conn) -> list[sqlite3.Row]:
    return conn.execute("SELECT * FROM annotators ORDER BY username").fetchall()


# -----------------------------------------------------------------------------
# annotations
# -----------------------------------------------------------------------------
def get_annotation(conn, annotator_id: int, eval_id: str) -> Optional[dict]:
    row = conn.execute("SELECT * FROM annotations WHERE annotator_id = ? AND eval_id = ?",
                       (annotator_id, eval_id)).fetchone()
    return _annotation(row) if row else None


def _annotation(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["answers"] = json.loads(d["answers"])
    return d


def save_annotation(conn, annotator_id: int, eval_id: str, answers: dict, comments: str,
                    duration_s: Optional[float], rubric_version: str) -> None:
    """Insert, or update an existing annotation (adding to its time and revision count)."""
    ts = now_iso()
    conn.execute(
        """INSERT INTO annotations(annotator_id, eval_id, answers, comments, duration_s, rubric_version,
                                   created_at, updated_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(annotator_id, eval_id) DO UPDATE SET
               answers = excluded.answers,
               comments = excluded.comments,
               duration_s = COALESCE(annotations.duration_s, 0) + COALESCE(excluded.duration_s, 0),
               rubric_version = excluded.rubric_version,
               updated_at = excluded.updated_at,
               revisions = annotations.revisions + 1""",
        (annotator_id, eval_id, json.dumps(answers, ensure_ascii=False, sort_keys=True), comments,
         duration_s, rubric_version, ts, ts))
    conn.execute("DELETE FROM skips WHERE annotator_id = ? AND eval_id = ?", (annotator_id, eval_id))
    release_claim(conn, annotator_id)


def annotations_of(conn, annotator_id: int) -> list[dict]:
    rows = conn.execute("SELECT * FROM annotations WHERE annotator_id = ? ORDER BY updated_at DESC",
                        (annotator_id,)).fetchall()
    return [_annotation(r) for r in rows]


def all_annotations(conn) -> list[dict]:
    rows = conn.execute(
        """SELECT a.*, n.username FROM annotations a JOIN annotators n ON n.id = a.annotator_id
           ORDER BY a.eval_id, n.username""").fetchall()
    return [_annotation(r) for r in rows]


def rated_ids(conn, annotator_id: int) -> set[str]:
    return {r[0] for r in conn.execute("SELECT eval_id FROM annotations WHERE annotator_id = ?", (annotator_id,))}


def rating_counts(conn) -> dict[str, int]:
    return {r[0]: r[1] for r in conn.execute("SELECT eval_id, COUNT(*) FROM annotations GROUP BY eval_id")}


def count_annotations(conn, annotator_id: Optional[int] = None) -> int:
    if annotator_id is None:
        return conn.execute("SELECT COUNT(*) FROM annotations").fetchone()[0]
    return conn.execute("SELECT COUNT(*) FROM annotations WHERE annotator_id = ?", (annotator_id,)).fetchone()[0]


# -----------------------------------------------------------------------------
# skips and claims
# -----------------------------------------------------------------------------
def skip(conn, annotator_id: int, eval_id: str) -> None:
    conn.execute("INSERT OR IGNORE INTO skips(annotator_id, eval_id, created_at) VALUES (?, ?, ?)",
                 (annotator_id, eval_id, now_iso()))
    release_claim(conn, annotator_id)


def skipped_ids(conn, annotator_id: int) -> set[str]:
    return {r[0] for r in conn.execute("SELECT eval_id FROM skips WHERE annotator_id = ?", (annotator_id,))}


def skip_counts(conn) -> dict[int, int]:
    return {r[0]: r[1] for r in conn.execute("SELECT annotator_id, COUNT(*) FROM skips GROUP BY annotator_id")}


def claim(conn, annotator_id: int, eval_id: str, at: Optional[float] = None) -> None:
    conn.execute("INSERT INTO claims(annotator_id, eval_id, claimed_at) VALUES (?, ?, ?) "
                 "ON CONFLICT(annotator_id) DO UPDATE SET eval_id = excluded.eval_id, claimed_at = excluded.claimed_at",
                 (annotator_id, eval_id, time.time() if at is None else at))


def release_claim(conn, annotator_id: int) -> None:
    conn.execute("DELETE FROM claims WHERE annotator_id = ?", (annotator_id,))


def active_claims(conn, ttl_s: float, now: Optional[float] = None) -> list[sqlite3.Row]:
    cutoff = (time.time() if now is None else now) - ttl_s
    return conn.execute("SELECT * FROM claims WHERE claimed_at >= ?", (cutoff,)).fetchall()


# -----------------------------------------------------------------------------
# calibration set
# -----------------------------------------------------------------------------
def calibration_ids(conn) -> list[str]:
    return [r[0] for r in conn.execute("SELECT eval_id FROM calibration ORDER BY position")]


def set_calibration(conn, ids: Iterable[str]) -> None:
    conn.executemany("INSERT INTO calibration(position, eval_id) VALUES (?, ?)", list(enumerate(ids)))


def get_meta(conn, key: str) -> Optional[str]:
    row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
    return row[0] if row else None


def set_meta(conn, key: str, value: str) -> None:
    conn.execute("INSERT INTO meta(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                 (key, value))
