# -*- coding: utf-8 -*-
"""Annotator-facing pages: login, the annotation form, the queue, the ruleset reference."""
from __future__ import annotations

import time

from flask import (Blueprint, abort, current_app, flash, jsonify, redirect, render_template, request, session,
                   url_for)

from . import assignment, db, highlights
from .rubric import COMMENTS_MAX, QUESTIONS, RUBRIC_VERSION, applicable, parse_answers
from .security import (USERNAME_RE, check_csrf, csrf_token, current_annotator, get_db, login_required,
                       normalise_username, safe_next, same_secret)
from .store import GURU_RULE_TE, VIKALPA_NOTES
from .users import check_password

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
    studies = current_app.config.get("HOME_STUDIES")
    if studies:                         # two studies (create_site): the annotator chooses one
        here = url_for("main.next_poem") if current_annotator() else url_for("main.login")
        return render_template("home.html", studies=[{**s, "url": s["url"] or here} for s in studies])
    return redirect(url_for("main.next_poem") if current_annotator() else url_for("main.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    users = current_app.config.get("USERS")
    need_code = users is None and bool(current_app.config.get("ACCESS_CODE"))
    error = None
    username = ""
    if request.method == "POST":
        username = normalise_username(request.form.get("username", ""))
        code = request.form.get("access_code", "")
        if not USERNAME_RE.match(username):
            error = "Use 2–40 letters, digits, dots, dashes or underscores (no spaces)."
        elif users is not None and not check_password(users, username, request.form.get("password", "")):
            error = "The username or password is not right."
        elif need_code and not same_secret(code, current_app.config["ACCESS_CODE"]):
            error = "The access code is not right."
        else:
            row = db.get_or_create_annotator(get_db(), username)
            session.clear()
            session.permanent = True
            session["annotator_id"] = row["id"]
            return redirect(safe_next(request.args.get("next"), url_for("main.next_poem")))
    return render_template("login.html", need_code=need_code, need_password=users is not None, error=error, username=username), (400 if error else 200)


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
                                   claim_ttl_s=cfg["CLAIM_TTL_MINUTES"] * 60, calibration=calibration(),
                                   questions=study_questions())
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
    return render_template("mine.html", rows=rows, skipped=skipped, cal_done=cal_done, cal_total=len(cal),
                           favorites=db.favorite_ids(conn, ann["id"]))


# -----------------------------------------------------------------------------
# one poem
# -----------------------------------------------------------------------------
def study_questions() -> tuple:
    """This study's rubric: rubric.QUESTIONS, or the study's own list (study 2 adds Q13 coherence)."""
    return current_app.config.get("QUESTIONS") or QUESTIONS


def _questions_for(poem):
    return [{"q": q, "applies": applicable(q, poem)} for q in study_questions()]


def _number_runs(numbers: list[int]) -> str:
    """[1, 2, 3, 13] → '1–3, 13'."""
    runs: list[list[int]] = []
    for n in numbers:
        if runs and n == runs[-1][-1] + 1:
            runs[-1].append(n)
        else:
            runs.append([n])
    return ", ".join(f"{r[0]}–{r[-1]}" if len(r) > 2 else ", ".join(map(str, r)) for r in runs)


def _before_bhavam(questions) -> str:
    """The numbers of the questions shown before the bhavam question, for the 'answer … first' hint."""
    numbers = []
    for q in questions:
        if q.applies == "bhavam":
            break
        numbers.append(q.number)
    return _number_runs(numbers)


@bp.route("/poem/<eval_id>", methods=["GET", "POST"])
@login_required
def poem(eval_id: str):
    p = store().get(eval_id)
    if p is None:
        abort(404, description=f"No poem {eval_id!r}.")
    conn = get_db()
    ann = current_annotator()
    existing = db.get_annotation(conn, ann["id"], eval_id)
    qs = study_questions()
    errors, values, comments, missing = {}, {}, "", []
    if existing:
        values = {k: v for k, v in existing["answers"].items() if v is not None}
        comments = existing["comments"]
        missing = [q.number for q in qs if applicable(q, p) and existing["answers"].get(q.key) is None]

    if request.method == "POST":
        answers, errors = parse_answers(request.form, p, qs)
        comments = (request.form.get("comments") or "").strip()[:COMMENTS_MAX]
        if not errors:
            try:
                started = float(request.form.get("started", ""))
                duration = time.time() - started
                duration = duration if 0 <= duration <= MAX_DURATION_S else None
            except ValueError:
                duration = None
            db.save_annotation(conn, ann["id"], eval_id, answers, comments, duration,
                               current_app.config.get("RUBRIC_VERSION") or RUBRIC_VERSION)
            flash(f"Saved {eval_id}.", "ok")
            return redirect(safe_next(request.form.get("next"), url_for("main.next_poem")))
        values = {k: v for k, v in answers.items() if v is not None}

    return render_template(
        "poem.html", poem=p, questions=_questions_for(p), values=values, comments=comments, errors=errors,
        existing=existing, started=time.time(), is_calibration=eval_id in set(calibration()),
        next_url=safe_next(request.values.get("next"), ""), meter_cards=store().meter_cards(p),
        backfill=missing if current_app.config.get("BACKFILL_NOTE") else [], bhavam_first=_before_bhavam(qs),
        favorite=eval_id in db.favorite_ids(conn, ann["id"]), **_highlight_context(conn, ann, p),
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
# highlights and favourites: app.js posts these with fetch and asks for JSON; a plain form post comes back to the poem
# -----------------------------------------------------------------------------
def _highlight_context(conn, ann, p) -> dict:
    rows = db.highlights_of(conn, ann["id"], p.id)
    spans = [tuple(h[k] for k in highlights.SPAN_FIELDS) for h in rows]
    return {"highlights": rows, "marked_lines": highlights.marked_lines(p.lines, spans)}


def _wants_json() -> bool:
    return request.accept_mimetypes.best == "application/json"


def _back_to_poem(eval_id: str):
    return redirect(url_for("main.poem", eval_id=eval_id, next=safe_next(request.form.get("next"), "") or None))


def _highlights_changed(p):
    if not _wants_json():
        return _back_to_poem(p.id)
    ctx = {"poem": p, "next_url": safe_next(request.form.get("next"), ""),
           **_highlight_context(get_db(), current_annotator(), p)}
    return jsonify(poem_html=render_template("_poem_text.html", **ctx),
                   list_html=render_template("_highlights.html", **ctx), count=len(ctx["highlights"]))


@bp.route("/poem/<eval_id>/highlights", methods=["POST"])
@login_required
def add_highlight(eval_id: str):
    p = store().get(eval_id)
    if p is None:
        abort(404)
    try:
        span = highlights.clean_span(p.plain_lines, *(int(request.form[k]) for k in highlights.SPAN_FIELDS))
    except (KeyError, ValueError):
        span = None
    if span is None:
        abort(400, description="Select some of the poem's text, then press Highlight.")
    db.add_highlight(get_db(), current_annotator()["id"], eval_id, span, highlights.span_text(p.plain_lines, span))
    return _highlights_changed(p)


@bp.route("/poem/<eval_id>/highlights/<int:highlight_id>/delete", methods=["POST"])
@login_required
def delete_highlight(eval_id: str, highlight_id: int):
    p = store().get(eval_id)
    if p is None or not db.delete_highlight(get_db(), current_annotator()["id"], eval_id, highlight_id):
        abort(404)
    return _highlights_changed(p)


@bp.route("/poem/<eval_id>/favorite", methods=["POST"])
@login_required
def favorite(eval_id: str):
    if eval_id not in store():
        abort(404)
    on = request.form.get("on") == "1"
    db.set_favorite(get_db(), current_annotator()["id"], eval_id, on)
    return jsonify(favorite=on) if _wants_json() else _back_to_poem(eval_id)


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
    return {"ref": ref, "focus": focus, "questions": study_questions()}


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
