# -*- coding: utf-8 -*-
"""Admin pages: study progress, inter-annotator agreement, exports. Enabled by HE_ADMIN_PASSWORD."""
from __future__ import annotations

import json

from flask import Blueprint, Response, current_app, redirect, render_template, request, session, url_for

from . import assignment, db
from .report import agreement_report, export_rows, to_csv, to_markdown
from .rubric import QUESTIONS
from .security import admin_required, get_db, safe_next, same_secret

bp = Blueprint("admin", __name__, url_prefix="/admin")


def _store():
    return current_app.extensions["poem_store"]


def _skips_by_user(conn) -> dict:
    names = {r["id"]: r["username"] for r in db.list_annotators(conn)}
    return {names[i]: n for i, n in db.skip_counts(conn).items() if i in names}


def _report(n_boot: int = 0) -> dict:
    conn = get_db()
    return agreement_report(db.all_annotations(conn), _store(), k=current_app.config["RATINGS_PER_POEM"],
                            calibration=current_app.config["CALIBRATION_IDS"], skips=_skips_by_user(conn),
                            n_boot=n_boot)


def _n_boot() -> int:
    try:
        return max(0, min(int(request.args.get("bootstrap", 0)), 5000))
    except ValueError:
        return 0


@bp.route("/login", methods=["GET", "POST"])
def login():
    password = current_app.config.get("ADMIN_PASSWORD")
    error = None
    if not password:
        error = "The admin pages are disabled: set HE_ADMIN_PASSWORD and restart."
    elif request.method == "POST":
        if same_secret(request.form.get("password", ""), password):
            session["admin"] = True
            return redirect(safe_next(request.args.get("next"), url_for("admin.dashboard")))
        error = "Wrong password."
    return render_template("admin_login.html", error=error), (401 if error and request.method == "POST" else 200)


@bp.route("/logout", methods=["POST"])
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


@bp.route("/")
@admin_required
def dashboard():
    conn = get_db()
    n_boot = _n_boot()
    report = _report(n_boot)
    progress = assignment.study_progress(conn, _store(), current_app.config["RATINGS_PER_POEM"])
    annotators = {r["username"]: r for r in db.list_annotators(conn)}
    return render_template("admin.html", report=report, progress=progress, questions=QUESTIONS,
                           annotators=annotators, n_boot=n_boot, meta=_store().meta,
                           calibration=current_app.config["CALIBRATION_IDS"])


@bp.route("/agreement.json")
@admin_required
def agreement_json():
    return Response(json.dumps(_report(_n_boot()), ensure_ascii=False, indent=2),
                    mimetype="application/json")


@bp.route("/agreement.md")
@admin_required
def agreement_md():
    return Response(to_markdown(_report(_n_boot())), mimetype="text/markdown; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=agreement.md"})


@bp.route("/annotations.csv")
@admin_required
def annotations_csv():
    rows = export_rows(db.all_annotations(get_db()), _store(), current_app.config["CALIBRATION_IDS"])
    # BOM so spreadsheet programs read the Telugu text as UTF-8
    return Response("﻿" + to_csv(rows), mimetype="text/csv; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=annotations.csv"})


@bp.route("/annotations.json")
@admin_required
def annotations_json():
    rows = export_rows(db.all_annotations(get_db()), _store(), current_app.config["CALIBRATION_IDS"])
    return Response(json.dumps(rows, ensure_ascii=False, indent=1), mimetype="application/json",
                    headers={"Content-Disposition": "attachment; filename=annotations.json"})
