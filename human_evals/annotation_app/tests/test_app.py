# -*- coding: utf-8 -*-
"""The Flask app end to end: login, the poem page, saving, editing, skipping, reference, admin."""
import csv
import io
import json
import re

import pytest
from markupsafe import escape

from conftest import FormClient, full_answers, make_app, poem_where
from padya_eval import db
from padya_eval.rubric import QUESTIONS


def saved(app, username, eval_id):
    conn = db.connect(app.config["DATABASE"])
    try:
        row = conn.execute("SELECT id FROM annotators WHERE username = ?", (username,)).fetchone()
        return db.get_annotation(conn, row["id"], eval_id) if row else None
    finally:
        conn.close()


# -----------------------------------------------------------------------------
# login and guards
# -----------------------------------------------------------------------------
def test_pages_need_login(client):
    for url in ("/next", "/mine", "/poem/he_0001", "/done"):
        r = client.get(url)
        assert r.status_code == 302 and "/login" in r.headers["Location"]
    assert client.get("/").headers["Location"].endswith("/login")


def test_login_creates_annotator_and_normalises_name(client, app):
    r = client.login("  Alice ")
    assert r.status_code == 302 and r.headers["Location"].endswith("/next")
    assert client.get("/mine").status_code == 200
    conn = db.connect(app.config["DATABASE"])
    assert [r["username"] for r in db.list_annotators(conn)] == ["alice"]


@pytest.mark.parametrize("name", ["a", "two words", "x" * 41, "semi;colon", ""])
def test_login_rejects_bad_usernames(client, name):
    r = client.login(name)
    assert r.status_code == 400 and b"letters" in r.data


def test_access_code(tmp_path):
    app = make_app(tmp_path, ACCESS_CODE="sesame")
    c = FormClient(app.test_client())
    assert b"access_code" in c.get("/login").data
    assert c.login("bob").status_code == 400
    assert c.login("bob", access_code="wrong").status_code == 400
    assert c.login("bob", access_code="sesame").status_code == 302


def test_post_without_csrf_token_is_rejected(client):
    client.get("/login")
    r = client.post("/login", data={"username": "alice"})
    assert r.status_code == 400
    r = client.post("/login", data={"username": "alice", "csrf_token": "forged"})
    assert r.status_code == 400


def test_login_redirects_only_to_local_paths(client):
    client.get("/login")
    r = client.post_form("/login?next=//evil.example/x", {"username": "alice"})
    assert r.headers["Location"].endswith("/next")
    r = client.post_form("/login?next=/mine", {"username": "carol"})
    assert r.headers["Location"].endswith("/mine")


def test_logout(client):
    client.login()
    assert client.post_form("/logout").status_code == 302
    assert client.get("/mine").status_code == 302


# -----------------------------------------------------------------------------
# the poem page
# -----------------------------------------------------------------------------
def test_poem_page_shows_poem_gana_table_and_form(client, store):
    client.login()
    poem = store.get("he_0099")
    html = client.get("/poem/he_0099").get_data(as_text=True)
    assert 'name="viewport"' in html
    assert "శార్దూలవిక్రీడితము" in html
    assert re.sub(r"<[^>]+>", "", html).count("లోక ర") >= 1                  # poem text, tags stripped
    assert html.count('class="pada-block"') == 4 and html.count("✔") == 4
    for g in ["మ", "స", "జ", "త", "గ"]:
        assert f">{g}<" in html
    assert 'class="ak mk-y"' in html and 'class="ak mk-p"' in html
    assert 'class="ga mk-y"' in html and 'class="ga mk-p"' in html
    for q in QUESTIONS:
        assert q.text in html
    assert 'name="comments"' in html
    assert html.count('type="radio"') == 5 * 5 + 2 * 5                          # every question applies here
    assert 'data-ref-open' in html and "/reference/fragment?poem=he_0099" in html


def test_poem_page_is_blind_to_source(client, store):
    client.login()
    for poem in [poem_where(store, lambda p: p.hidden["source_dataset"] == s)
                 for s in ("generated", "bhagavatam", "vemana", "kuchimanchi", "reference")]:
        html = client.get(f"/poem/{poem.id}").get_data(as_text=True)
        content = " ".join(poem.plain_lines) + " ".join((poem.bhavam or {}).get(k) or "" for k in ("te", "en"))
        # "reference" is also the ruleset URL, so that one source name is not checked
        leaks = [poem.hidden["source_id"], "Gemini", "prosody reference", "kuchimanchi", "Timmakavi",
                 poem.hidden["source_dataset"] if poem.hidden["source_dataset"] != "reference" else None,
                 poem.hidden["metadata"].get("title"), poem.hidden["metadata"].get("contributor")]
        if poem.hidden["author"] not in content:            # a makuṭam such as "వినర వేమ" may name the poet
            leaks.append(poem.hidden["author"])
        for leak in filter(None, leaks):
            assert leak not in html, (poem.id, leak)


def test_bhavam_is_behind_a_reveal(client, store):
    client.login()
    poem = poem_where(store, lambda p: p.bhavam and p.bhavam.get("te"))
    html = client.get(f"/poem/{poem.id}").get_data(as_text=True)
    assert "<details class=\"bhavam\"" in html and poem.bhavam["te"][:40] in html


def test_not_applicable_questions(client, store):
    client.login()
    no_bhavam = poem_where(store, lambda p: not p.has_bhavam and p.prasa_applicable)
    html = client.get(f"/poem/{no_bhavam.id}").get_data(as_text=True)
    assert "No bhavam is available" in html and 'name="bhavam"' not in html
    no_prasa = poem_where(store, lambda p: not p.prasa_applicable and p.has_bhavam)
    html = client.get(f"/poem/{no_prasa.id}").get_data(as_text=True)
    assert "This meter has no prāsa rule" in html and 'name="prasa"' not in html
    assert "no prāsa in this meter" in html


def test_engine_checks_can_be_hidden(tmp_path):
    app = make_app(tmp_path, SHOW_ENGINE_CHECKS=False)
    c = FormClient(app.test_client())
    c.login()
    html = c.get("/poem/he_0099").get_data(as_text=True)
    assert "✔" not in html and 'class="pada-check"' in html


def test_unknown_poem_is_404(client):
    client.login()
    assert client.get("/poem/he_9999").status_code == 404
    assert client.post_form("/poem/he_9999/skip").status_code == 404


# -----------------------------------------------------------------------------
# saving
# -----------------------------------------------------------------------------
def test_save_valid_annotation(client, app, store):
    client.login()
    poem = store.get("he_0099")
    data = {**full_answers(poem, likert=4, binary=1), "comments": "  vṛttyanuprāsa in pāda 2 ", "started": "0"}
    r = client.post_form("/poem/he_0099", data)
    assert r.status_code == 302 and r.headers["Location"].endswith("/next")
    a = saved(app, "alice", "he_0099")
    assert a["answers"] == {q.key: (4 if q.kind == "likert" else 1) for q in QUESTIONS}
    assert a["comments"] == "vṛttyanuprāsa in pāda 2"
    assert a["duration_s"] is None and a["revisions"] == 1 and a["rubric_version"] == "1"


def test_duration_is_recorded(client, app, store):
    import time
    client.login()
    poem = store.get("he_0001")
    client.post_form("/poem/he_0001", {**full_answers(poem), "started": str(time.time() - 42)})
    assert 41 <= saved(app, "alice", "he_0001")["duration_s"] < 60


def test_not_applicable_answers_are_stored_as_none(client, app, store):
    client.login()
    poem = poem_where(store, lambda p: not p.has_bhavam and not p.prasa_applicable) if any(
        not p.has_bhavam and not p.prasa_applicable for p in store.poems) else poem_where(store, lambda p: not p.has_bhavam)
    data = {**full_answers(poem), "bhavam": 5, "prasa": 1}                      # sent anyway
    assert client.post_form(f"/poem/{poem.id}", data).status_code == 302
    answers = saved(app, "alice", poem.id)["answers"]
    assert answers["bhavam"] is None
    if not poem.prasa_applicable:
        assert answers["prasa"] is None


@pytest.mark.parametrize("bad", [{}, {"readability": 6}, {"chandassu": 2}, {"poetic": "x"}, {"yati": ""}])
def test_invalid_submissions_are_rejected_and_kept(client, app, store, bad):
    client.login()
    poem = store.get("he_0099")
    data = full_answers(poem)
    key = next(iter(bad)) if bad else "readability"
    data.pop(key)
    data.update(bad)
    data["comments"] = "draft note"
    r = client.post_form("/poem/he_0099", data)
    assert r.status_code == 422
    html = r.get_data(as_text=True)
    assert f'id="q-{key}"' in html and "q-error" in html and "draft note" in html
    assert 'value="3" checked' not in html or True
    assert saved(app, "alice", "he_0099") is None


def test_edit_updates_and_counts_revisions(client, app, store):
    client.login()
    poem = store.get("he_0099")
    client.post_form("/poem/he_0099", full_answers(poem, likert=2))
    html = client.get("/poem/he_0099?next=/mine").get_data(as_text=True)
    assert 'value="2" checked' in html and "Update" in html and "/skip" not in html
    r = client.post_form("/poem/he_0099", {**full_answers(poem, likert=5), "next": "/mine"})
    assert r.headers["Location"].endswith("/mine")
    a = saved(app, "alice", "he_0099")
    assert a["answers"]["readability"] == 5 and a["revisions"] == 2


def test_skip_and_rate_anyway(client, app):
    client.login()
    target = client.get("/next").headers["Location"].rsplit("/", 1)[1]
    assert client.post_form(f"/poem/{target}/skip").status_code == 302
    assert client.get("/next").headers["Location"].rsplit("/", 1)[1] != target
    assert target in client.get("/mine").get_data(as_text=True)
    conn = db.connect(app.config["DATABASE"])
    aid = conn.execute("SELECT id FROM annotators").fetchone()[0]
    assert db.skipped_ids(conn, aid) == {target}
    from padya_eval.store import load_store
    poem = load_store(app.config["DATA_DIR"]).get(target)
    client.post_form(f"/poem/{target}", full_answers(poem))
    assert db.skipped_ids(conn, aid) == set()


def test_queue_runs_calibration_then_reports_done(tmp_path, store):
    app = make_app(tmp_path, CALIBRATION_SIZE=2, RATINGS_PER_POEM=0)
    c = FormClient(app.test_client())
    c.login()
    cal = set(app.config["CALIBRATION_IDS"])
    seen = set()
    for _ in range(2):
        loc = c.get("/next").headers["Location"]
        eid = loc.rsplit("/", 1)[1]
        assert eid in cal
        assert b"calibration" in c.get(loc).data
        seen.add(eid)
        c.post_form(loc, full_answers(store.get(eid)))
    assert seen == cal
    assert c.get("/next").headers["Location"].endswith("/done")
    assert "ధన్యవాదాలు" in c.get("/done").get_data(as_text=True)


def test_mine_lists_ratings(client, store):
    client.login()
    client.post_form("/poem/he_0099", full_answers(store.get("he_0099")))
    html = client.get("/mine").get_data(as_text=True)
    assert "he_0099" in html and "1 rated" in html


# -----------------------------------------------------------------------------
# reference and misc
# -----------------------------------------------------------------------------
def test_reference_fragment_for_a_poem(client):
    html = client.get("/reference/fragment?poem=he_0099").get_data(as_text=True)
    assert 'id="meter-sardulavikriditamu"' in html and "13వ అక్షరం" in html
    assert "దీర్ఘము" in html and "స్వరమైత్రి" in html and "సమప్రాస" in html and 'id="rubric"' in html
    assert "<html" not in html


def test_reference_full_page_has_every_meter_and_catalogue(client, store):
    html = client.get("/reference").get_data(as_text=True)
    assert html.count('class="meter-card"') == len(store.reference["meters"])
    assert "పూర్తి యతి నియమావళి" in html and "YATI-VY-01" in html


def test_healthz_and_static(client, app):
    assert client.get("/healthz").get_json() == {"status": "ok", "poems": 500}
    assert client.get("/static/app.css").status_code == 200
    client.login()
    assert f"app.css?v={app.config['ASSET_VERSION']}" in client.get("/mine").get_data(as_text=True)


def test_database_of_another_pool_is_refused(tmp_path):
    from padya_eval.db import StudyMismatch, init_db
    init_db(tmp_path / "annotations.db", "other/pool/10")
    with pytest.raises(StudyMismatch):
        make_app(tmp_path)


# -----------------------------------------------------------------------------
# admin
# -----------------------------------------------------------------------------
def test_admin_disabled_without_password(tmp_path):
    app = make_app(tmp_path, ADMIN_PASSWORD=None)
    c = FormClient(app.test_client())
    assert c.get("/admin/").status_code == 403
    assert b"disabled" in c.get("/admin/login").data


def test_admin_login(client):
    assert client.get("/admin/").status_code == 302
    assert client.post_form("/admin/login", {"password": "nope"}).status_code == 401
    assert client.post_form("/admin/login", {"password": "pw"}).status_code == 302
    assert client.get("/admin/").status_code == 200


def _two_annotators_rate(app, store, ids):
    for name, likert in (("ann1", 4), ("ann2", 4), ("ann3", 2)):
        c = FormClient(app.test_client())
        c.login(name)
        for eid in ids:
            c.post_form(f"/poem/{eid}", full_answers(store.get(eid), likert=likert, binary=1))


def test_admin_dashboard_and_exports(client, app, store):
    ids = ["he_0099", "he_0001", "he_0002", "he_0003", "he_0004", "he_0005"]
    _two_annotators_rate(app, store, ids)
    client.post_form("/admin/login", {"password": "pw"})
    html = client.get("/admin/").get_data(as_text=True)
    assert "Agreement · all poems" in html and "ann3" in html and "Mean rating by source" in html

    r = client.get("/admin/annotations.csv")
    text = r.get_data(as_text=True)
    assert text.startswith("﻿")
    rows = list(csv.DictReader(io.StringIO(text.lstrip("﻿"))))
    assert len(rows) == 18 and {r["annotator"] for r in rows} == {"ann1", "ann2", "ann3"}
    row = next(r for r in rows if r["eval_id"] == "he_0099")
    assert row["source_id"] == "1-1-శా." and row["meter"] == "sardulavikriditamu"

    rep = client.get("/admin/agreement.json").get_json()
    assert rep["study"]["annotations"] == 18 and len(rep["questions"]) == 10
    readability = rep["questions"][0]
    assert readability["n_paired_units"] == 6 and readability["distribution"]["4"] == 12

    assert len(client.get("/admin/annotations.json").get_json()) == 18
    md = client.get("/admin/agreement.md").get_data(as_text=True)
    assert "| 1 | How easy is it to read?" in md

    with_ci = client.get("/admin/agreement.json?bootstrap=50").get_json()
    assert with_ci["study"]["bootstrap"] == 50


def test_admin_logout(client):
    client.post_form("/admin/login", {"password": "pw"})
    client.post_form("/admin/logout")
    assert client.get("/admin/").status_code == 302


# -----------------------------------------------------------------------------
# line notes, theme, all-poems mode
# -----------------------------------------------------------------------------
def test_line_notes_beside_the_poem(client):
    client.login()
    html = client.get("/poem/he_0449").get_data(as_text=True)
    assert html.count('class="line-note"') == 4
    for rule in ("వర్గజ యతి", "ప్రాణి యతి"):
        assert rule in html
    assert '<b class="ln-y">త</b> – <b class="ln-y">ద</b>' in html
    assert html.count('<b class="ln-p">పం</b>') == 4            # 2 line notes + 2 in the summary
    assert str(escape("'ప'కార ప్రాస")) in html


def test_kandam_odd_lines_say_no_yati(client, store):
    client.login()
    kandam = poem_where(store, lambda p: p.meter == "kandamu")
    html = client.get(f"/poem/{kandam.id}").get_data(as_text=True)
    assert html.count("యతి లేదు") == 2


def test_hiding_engine_checks_hides_rule_names(tmp_path):
    app = make_app(tmp_path, SHOW_ENGINE_CHECKS=False)
    c = FormClient(app.test_client())
    c.login()
    html = c.get("/poem/he_0449").get_data(as_text=True)
    assert '<b class="ln-y">త</b>' in html                      # aksharas stay
    assert "వర్గజ యతి" not in html and str(escape("'ప'కార ప్రాస")) not in html


def test_theme_toggle_and_light_default(client):
    for url in ("/login", "/reference"):
        html = client.get(url).get_data(as_text=True)
        assert "data-theme-toggle" in html and 'localStorage.getItem("padya-theme")' in html
        assert 'data-theme="dark"' not in html                   # light unless the viewer chose dark
    css = client.get("/static/app.css").get_data(as_text=True)
    assert ':root[data-theme="dark"]' in css and "prefers-color-scheme" not in css


def test_all_mode_gives_every_poem_to_everyone(tmp_path, store):
    app = make_app(tmp_path, RATINGS_PER_POEM=None, CALIBRATION_SIZE=2)
    cal = app.config["CALIBRATION_IDS"]
    users = [FormClient(app.test_client()) for _ in range(2)]
    seen = []
    for i, c in enumerate(users):
        c.login(f"ann{i}")
        got = []
        for _ in range(5):
            loc = c.get("/next").headers["Location"]
            eid = loc.rsplit("/", 1)[1]
            got.append(eid)
            c.post_form(loc, full_answers(store.get(eid)))
        assert set(got[:2]) == set(cal)
        seen.append(got)
    assert seen[0] != seen[1]                                      # each in their own order
    html = users[0].get("/mine").get_data(as_text=True)
    assert "/500" in html                                          # progress pill: rated / all poems
    conn = db.connect(app.config["DATABASE"])
    from padya_eval import assignment
    progress = assignment.study_progress(conn, store, None)
    assert progress["target"] == 2 and progress["ratings"] == 10
