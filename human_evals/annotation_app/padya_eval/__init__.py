# -*- coding: utf-8 -*-
"""
Padya-eval: a Flask app for the Chandohasam human evaluation.

    from padya_eval import create_app
    app = create_app()

Configuration comes from environment variables (see README.md) or a mapping passed
to create_app (the tests use that).
"""
from __future__ import annotations

import hashlib
import os
import secrets
from datetime import timedelta
from pathlib import Path

from flask import Flask, g

from . import assignment, db
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
    return {
        "DATA_DIR": Path(os.environ.get("HE_DATA_DIR", APP_DIR / "data")),
        "DATABASE": Path(os.environ.get("HE_DATABASE", instance / "annotations.db")),
        "RATINGS_PER_POEM": _env_ratings_per_poem(),     # None = all poems for everyone (fully crossed)
        "CALIBRATION_SIZE": _env_int("HE_CALIBRATION_SIZE", 25),
        "CALIBRATION_SEED": _env_int("HE_CALIBRATION_SEED", 42),
        "CLAIM_TTL_MINUTES": _env_int("HE_CLAIM_TTL_MINUTES", 30),
        "ACCESS_CODE": os.environ.get("HE_ACCESS_CODE") or None,
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
    }


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
