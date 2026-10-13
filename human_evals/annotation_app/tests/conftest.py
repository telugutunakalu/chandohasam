# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import pytest

APP_DIR = Path(__file__).resolve().parent.parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from padya_eval import create_app                      # noqa: E402
from padya_eval.rubric import QUESTIONS                # noqa: E402
from padya_eval.store import load_store                # noqa: E402

DATA_DIR = APP_DIR / "data"


@pytest.fixture(scope="session")
def store():
    return load_store(DATA_DIR)


def make_app(tmp_path, **overrides):
    config = {
        "TESTING": True,
        "SECRET_KEY": "test-secret",
        "DATABASE": tmp_path / "annotations.db",
        "DATA_DIR": DATA_DIR,
        "RATINGS_PER_POEM": 3,
        "CALIBRATION_SIZE": 5,
        "ADMIN_PASSWORD": "pw",
        "ACCESS_CODE": None,
    }
    config.update(overrides)
    return create_app(config)


@pytest.fixture
def app(tmp_path):
    return make_app(tmp_path)


class FormClient:
    """A Flask test client that sends the session's CSRF token with every form post."""

    def __init__(self, client):
        self.c = client

    def __getattr__(self, name):
        return getattr(self.c, name)

    def token(self) -> str:
        with self.c.session_transaction() as s:
            tok = s.get("csrf")
        if tok is None:
            self.c.get("/login")
            with self.c.session_transaction() as s:
                tok = s["csrf"]
        return tok

    def post_form(self, url, data=None, **kw):
        data = dict(data or {})
        data.setdefault("csrf_token", self.token())
        return self.c.post(url, data=data, **kw)

    def login(self, username="alice", **extra):
        return self.post_form("/login", {"username": username, **extra})


@pytest.fixture
def client(app):
    return FormClient(app.test_client())


def full_answers(poem, likert=4, binary=1) -> dict:
    """A complete, valid submission for ``poem``."""
    from padya_eval.rubric import applicable
    data = {}
    for q in QUESTIONS:
        if applicable(q, poem):
            data[q.key] = likert if q.kind == "likert" else binary
    return data


def poem_where(store, predicate):
    return next(p for p in store.poems if predicate(p))
