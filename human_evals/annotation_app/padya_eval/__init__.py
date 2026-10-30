# -*- coding: utf-8 -*-
"""
Padya-eval: a Flask app for the Chandohasam human evaluation.

    from padya_eval import create_app
    app = create_app()

Configuration comes from environment variables (see README.md) or a mapping passed
to create_app (the tests use that).

Two studies (2026-10-30): :func:`create_site` (wsgi.py) serves study 1 at ``/`` and, when
``data_study2/poems.json`` exists, study 2 (the he2_ poems) at ``/study2`` as a second app with
its own data, database and session cookie; the home page ``/`` lets an annotator choose.
"""
from __future__ import annotations

import hashlib
import os
import secrets
from datetime import timedelta
from pathlib import Path

from flask import Flask, g

from . import assignment, db
from .rubric import STUDY2_QUESTIONS, STUDY2_RUBRIC_VERSION
from .store import load_store

APP_DIR = Path(__file__).resolve().parent.parent


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.environ.get(name, default))
    except ValueError:
        return default


def _env_ratings_per_poem() -> int | None:
    """HE_RATINGS_PER_POEM: 'all' (default) = every annotator rates every poem; a number k = k ratings per poem."""
    raw = os.environ.get("HE_RATINGS_PER_POEM", "all").strip().lower()
    if raw in ("all", "", "none"):
        return None
    try:
        return max(0, int(raw))
    except ValueError:
        return None


def _secret_key(instance: Path) -> str:
    """HE_SECRET_KEY, or a random key kept in instance/secret_key so sessions survive restarts."""
    if os.environ.get("HE_SECRET_KEY"):
        return os.environ["HE_SECRET_KEY"]
    path = instance / "secret_key"
    if path.is_file():
        return path.read_text().strip()
    instance.mkdir(parents=True, exist_ok=True)
    key = secrets.token_hex(32)
    path.write_text(key)
    path.chmod(0o600)
    return key


def default_config(instance: Path) -> dict:
    from .users import load_users, users_path   # not at module level: `python -m padya_eval.users` imports this package
    return {
        "DATA_DIR": Path(os.environ.get("HE_DATA_DIR", APP_DIR / "data")),
        "DATABASE": Path(os.environ.get("HE_DATABASE", instance / "annotations.db")),
        "RATINGS_PER_POEM": _env_ratings_per_poem(),     # None = all poems for everyone (fully crossed)
        "CALIBRATION_SIZE": _env_int("HE_CALIBRATION_SIZE", 25),
        "CALIBRATION_SEED": _env_int("HE_CALIBRATION_SEED", 42),
        "CLAIM_TTL_MINUTES": _env_int("HE_CLAIM_TTL_MINUTES", 30),
        "ACCESS_CODE": os.environ.get("HE_ACCESS_CODE") or None,
        # username -> password hash (instance/users.json); None = open login. See padya_eval/users.py
        "USERS": load_users(users_path(instance)),
        "ADMIN_PASSWORD": os.environ.get("HE_ADMIN_PASSWORD") or None,
        # the ✔ beside each pāda in the gaṇa table (the engine's verdict); HE_SHOW_ENGINE_CHECKS=0 hides it
        "SHOW_ENGINE_CHECKS": os.environ.get("HE_SHOW_ENGINE_CHECKS", "1") != "0",
        "CSRF_ENABLED": True,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_HTTPONLY": True,
        "SESSION_COOKIE_SECURE": os.environ.get("HE_SECURE_COOKIES") == "1",
        "PERMANENT_SESSION_LIFETIME": timedelta(days=30),
        "SEND_FILE_MAX_AGE_DEFAULT": timedelta(days=7),
        "BEHIND_PROXY": os.environ.get("HE_BEHIND_PROXY") == "1",
        # two studies (create_site): the studies the home page offers (None = "/" goes straight to the queue),
        # the label in the top bar, and the home page's URL for the second study's top bar
        "HOME_STUDIES": None,
        "STUDY_LABEL": None,
        "HOME_URL": None,
    }


STUDY2_PREFIX = "/study2"


def study2_config(instance: Path) -> dict:
    """Study 2: the AI poems of build_study2_pool.py, 3 ratings each, engine verdicts hidden, its own database."""
    return {
        "DATA_DIR": APP_DIR / "data_study2",
        "DATABASE": instance / "annotations_study2.db",
        "RATINGS_PER_POEM": 3,
        "CALIBRATION_SIZE": 6,          # stratified on hidden.source_dataset, here the model: 2 poems per model
        "SHOW_ENGINE_CHECKS": False,
        "SESSION_COOKIE_NAME": "he2_session",
        "SESSION_COOKIE_PATH": STUDY2_PREFIX,
        "STUDY_LABEL": "అధ్యయనం 2 · Study 2",
        "HOME_URL": "/",
        "QUESTIONS": STUDY2_QUESTIONS,   # adds Q13 coherence; ratings made before it are served again for it,
        "RUBRIC_VERSION": STUDY2_RUBRIC_VERSION,
        "BACKFILL_NOTE": True,           # with their earlier answers filled in (editable) and a note naming Q13
    }


def create_site(config: dict | None = None, study2: dict | None = None) -> Flask:
    """Study 1 at /, and study 2 at STUDY2_PREFIX when its data exists; the home page then offers both."""
    first = create_app(config)
    second_cfg = {**(config or {}), **study2_config(Path(first.instance_path)), **(study2 or {})}
    if not (Path(second_cfg["DATA_DIR"]) / "poems.json").is_file():
        return first
    second = create_app(second_cfg)
    first.config.update(STUDY_LABEL="అధ్యయనం 1 · Study 1", HOME_STUDIES=[
        {"key": "1", "title": "అధ్యయనం 1 · Study 1", "url": None,
         "text": "మొదటి అధ్యయనం కొనసాగించండి · Continue the first study."},
        {"key": "2", "title": "అధ్యయనం 2 · Study 2", "url": STUDY2_PREFIX + "/",
         "text": "కొత్త పద్యాల సమితి · A new set of poems (separate login, same username and password)."},
    ])
    tabs = [{"key": "1", "label": "Study 1", "url": "/admin/"},          # the admin dashboards link to each other
            {"key": "2", "label": "Study 2", "url": STUDY2_PREFIX + "/admin/"}]
    first.config.update(ADMIN_TABS=tabs, ADMIN_TAB="1")
    second.config.update(ADMIN_TABS=tabs, ADMIN_TAB="2")
    first.extensions["study2_app"] = second
    from werkzeug.middleware.dispatcher import DispatcherMiddleware
    first.wsgi_app = DispatcherMiddleware(first.wsgi_app, {STUDY2_PREFIX: second})
    return first


def create_app(config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_path=os.environ.get("HE_INSTANCE_DIR", str(APP_DIR / "instance")),
                instance_relative_config=True)
    instance = Path(app.instance_path)
    app.config.update(default_config(instance))
    if config:
        app.config.update(config)
    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = _secret_key(instance)
    if app.config["BEHIND_PROXY"]:
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    store = load_store(app.config["DATA_DIR"])
    app.extensions["poem_store"] = store
    db.init_db(app.config["DATABASE"], store.fingerprint)
    conn = db.connect(app.config["DATABASE"])
    try:
        app.config["CALIBRATION_IDS"] = assignment.ensure_calibration(
            conn, store, app.config["CALIBRATION_SIZE"], app.config["CALIBRATION_SEED"])
    finally:
        conn.close()

    static_dir = Path(app.static_folder)
    digest = hashlib.sha256(b"".join(p.read_bytes() for p in sorted(static_dir.glob("*.*")))).hexdigest()[:10]
    app.config["ASSET_VERSION"] = digest

    @app.teardown_appcontext
    def _close_db(_exc):
        conn = g.pop("db", None)
        if conn is not None:
            conn.close()

    from .views import bp as main_bp
    from .admin import bp as admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    return app
