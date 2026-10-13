# -*- coding: utf-8 -*-
"""Sessions, CSRF tokens and the login guards."""
from __future__ import annotations

import hmac
import re
import secrets
from functools import wraps

from flask import abort, current_app, g, redirect, request, session, url_for

from . import db

USERNAME_RE = re.compile(r"^[\w.\-]{2,40}$", re.UNICODE)


def get_db():
    if "db" not in g:
        g.db = db.connect(current_app.config["DATABASE"])
    return g.db


def csrf_token() -> str:
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def check_csrf() -> None:
    if not current_app.config.get("CSRF_ENABLED", True):
        return
    sent = request.form.get("csrf_token", "")
    if not sent or not hmac.compare_digest(sent, session.get("csrf", "")):
        abort(400, description="The form expired. Reload the page and try again.")


def same_secret(given: str, expected: str) -> bool:
    return hmac.compare_digest(given.encode(), expected.encode())


def normalise_username(raw: str) -> str:
    return (raw or "").strip().lower()


def current_annotator():
    """The logged-in annotator row, or None (a stale session is cleared)."""
    if "annotator" in g:
        return g.annotator
    row = None
    aid = session.get("annotator_id")
    if aid is not None:
        row = db.get_annotator(get_db(), aid)
        if row is None:
            session.pop("annotator_id", None)
    g.annotator = row
    return row


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if current_annotator() is None:
            return redirect(url_for("main.login", next=request.full_path if request.method == "GET" else None))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_app.config.get("ADMIN_PASSWORD"):
            abort(403, description="The admin pages are disabled: set HE_ADMIN_PASSWORD to enable them.")
        if not session.get("admin"):
            return redirect(url_for("admin.login", next=request.full_path))
        return view(*args, **kwargs)
    return wrapped


def safe_next(target: str | None, fallback: str) -> str:
    """Only allow redirects to local paths."""
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    return fallback
