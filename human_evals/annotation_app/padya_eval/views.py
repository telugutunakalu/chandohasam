# -*- coding: utf-8 -*-
"""Annotator-facing pages: login, the annotation form, the queue, the ruleset reference."""
from __future__ import annotations

import time

from flask import (Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, session,
                   url_for)

from . import assignment, db
from .rubric import COMMENTS_MAX, QUESTIONS, RUBRIC_VERSION, applicable, parse_answers
from .security import (USERNAME_RE, check_csrf, csrf_token, current_annotator, get_db, login_required,
                       normalise_username, safe_next, same_secret)
from .store import GURU_RULE_TE, VIKALPA_NOTES

bp = Blueprint("main", __name__)

MAX_DURATION_S = 3 * 3600


def store():
    return current_app.extensions["poem_store"]


def calibration() -> list[str]:
    return current_app.config["CALIBRATION_IDS"]


@bp.app_context_processor
def inject_globals():
    ann = current_annotator()
    ctx = {"csrf_token": csrf_token, "asset_version": current_app.config["ASSET_VERSION"], "annotator": ann,
           "guru_rule_te": GURU_RULE_TE, "vikalpa_notes": VIKALPA_NOTES,
           "show_checks": current_app.config.get("SHOW_ENGINE_CHECKS", True)}
    if ann is not None:
        conn = get_db()
        k = current_app.config["RATINGS_PER_POEM"]
        target = assignment.target_per_poem(conn, k)
        counts = db.rating_counts(conn)
        ctx["progress"] = {"mine": db.count_annotations(conn, ann["id"]), "all_mode": k is None,
                           "complete": sum(1 for e in store().ids if counts.get(e, 0) >= target),
                           "poems": len(store())}
    return ctx


@bp.app_template_filter("mark")
def weight_mark(weight: str) -> str:
    return "U" if weight == "U" else "|"


@bp.app_template_filter("rules_te")
def rules_te(rules) -> str:
    return ", ".join(GURU_RULE_TE.get(r, r) for r in rules)


@bp.before_app_request
def _csrf_guard():
    if request.method == "POST":
        check_csrf()


# -----------------------------------------------------------------------------
# login
# -----------------------------------------------------------------------------
@bp.route("/")
def index():
    return redirect(url_for("main.next_poem") if current_annotator() else url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    need_code = bool(current_app.config.get("ACCESS_CODE"))
    error = None
    username = ""
    if request.method == "POST":
        username = normalise_username(request.form.get("username", ""))
        code = request.form.get("access_code", "")
        if not USERNAME_RE.match(username):
            error = "Use 2–40 letters, digits, dots, dashes or underscores (no spaces)."
        elif need_code and not same_secret(code, current_app.config["ACCESS_CODE"]):
            error = "The access code is not right."
        else:
            row = db.get_or_create_annotator(get_db(), username)
            session.clear()
            session.permanent = True
            session["annotator_id"] = row["id"]
            return redirect(safe_next(request.args.get("next"), url_for("main.next_poem")))
    return render_template("login.html", need_code=need_code, error=error, username=username), (400 if error else 200)


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("main.login"))


# -----------------------------------------------------------------------------
# the queue
# -----------------------------------------------------------------------------
@bp.route("/next")
@login_required
def next_poem():
    cfg = current_app.config
    eval_id = assignment.next_poem(get_db(), store(), current_annotator(), k=cfg["RATINGS_PER_POEM"],
                                   claim_ttl_s=cfg["CLAIM_TTL_MINUTES"] * 60, calibration=calibration())
    if eval_id is None:
        return redirect(url_for("main.done"))
    return redirect(url_for("main.poem", eval_id=eval_id))


@bp.route("/done")
@login_required
def done():
    return render_template("done.html")


@bp.route("/mine")
@login_required
def mine():
    conn = get_db()
    ann = current_annotator()
    rows = []
    for a in db.annotations_of(conn, ann["id"]):
        poem = store().get(a["eval_id"])
        if poem is not None:
            rows.append({"a": a, "poem": poem})
    skipped = [store().get(e) for e in sorted(db.skipped_ids(conn, ann["id"])) if e in store()]
    cal = calibration()
    cal_done = sum(1 for r in rows if r["poem"].id in set(cal))
    return render_template("mine.html", rows=rows, skipped=skipped, cal_done=cal_done, cal_total=len(cal))


# -----------------------------------------------------------------------------
# one poem
# -----------------------------------------------------------------------------
def _questions_for(poem):
    return [{"q": q, "applies": applicable(q, poem)} for q in QUESTIONS]


@bp.route("/poem/<eval_id>", methods=["GET", "POST"])
@login_required
def poem(eval_id: str):
    p = store().get(eval_id)
    if p is None:
        abort(404, description=f"No poem {eval_id!r}.")
    conn = get_db()
    ann = current_annotator()
    existing = db.get_annotation(conn, ann["id"], eval_id)
    errors, values, comments = {}, {}, ""
    if existing:
        values = {k: v for k, v in existing["answers"].items() if v is not None}
        comments = existing["comments"]

    if request.method == "POST":
        answers, errors = parse_answers(request.form, p)
        comments = (request.form.get("comments") or "").strip()[:COMMENTS_MAX]
        if not errors:
            try:
                started = float(request.form.get("started", ""))
                duration = time.time() - started
                duration = duration if 0 <= duration <= MAX_DURATION_S else None
            except ValueError:
                duration = None
            db.save_annotation(conn, ann["id"], eval_id, answers, comments, duration, RUBRIC_VERSION)
            flash(f"Saved {eval_id}.", "ok")
            return redirect(safe_next(request.form.get("next"), url_for("main.next_poem")))
        values = {k: v for k, v in answers.items() if v is not None}

    return render_template(
        "poem.html", poem=p, questions=_questions_for(p), values=values, comments=comments, errors=errors,
        existing=existing, started=time.time(), is_calibration=eval_id in set(calibration()),
        next_url=safe_next(request.values.get("next"), ""), meter_cards=store().meter_cards(p),
    ), (422 if errors else 200)


@bp.route("/poem/<eval_id>/skip", methods=["POST"])
@login_required
def skip(eval_id: str):
    if eval_id not in store():
        abort(404)
    db.skip(get_db(), current_annotator()["id"], eval_id)
    flash(f"Skipped {eval_id}.", "info")
    return redirect(url_for("main.next_poem"))


# -----------------------------------------------------------------------------
# ruleset reference
# -----------------------------------------------------------------------------
def _reference_context(eval_id: str | None, meter: str | None):
    s = store()
    ref = s.reference
    poem = s.get(eval_id) if eval_id else None
    if poem is not None:
        focus = s.meter_cards(poem)
    elif meter and meter in ref["meters"]:
        focus = [ref["meters"][meter]]
    else:
        focus = []
    return {"ref": ref, "focus": focus, "questions": QUESTIONS}


@bp.route("/reference")
def reference():
    ctx = _reference_context(request.args.get("poem"), request.args.get("meter"))
    return render_template("reference.html", full=True, **ctx)


@bp.route("/reference/fragment")
def reference_fragment():
    ctx = _reference_context(request.args.get("poem"), request.args.get("meter"))
    resp = current_app.make_response(render_template("_reference_body.html", full=False, **ctx))
    resp.headers["Cache-Control"] = "private, max-age=3600"
    return resp


@bp.route("/healthz")
def healthz():
    return jsonify(status="ok", poems=len(store()))


@bp.app_errorhandler(400)
@bp.app_errorhandler(403)
@bp.app_errorhandler(404)
def http_error(err):
    return render_template("error.html", code=err.code, message=err.description), err.code
