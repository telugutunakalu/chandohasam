# -*- coding: utf-8 -*-
"""Two studies in one site (create_site): study 1 at /, study 2 (data_study2, he2_ poems) at /study2."""
import json
import re
import sqlite3

import pytest

from conftest import APP_DIR, DATA_DIR
from padya_eval import create_site

STUDY2_DATA = APP_DIR / "data_study2"
pytestmark = pytest.mark.skipif(not (STUDY2_DATA / "poems.json").is_file(), reason="study 2 data not built")


def site(tmp_path, **study2):
    config = {"TESTING": True, "SECRET_KEY": "test-secret", "DATABASE": tmp_path / "study1.db", "DATA_DIR": DATA_DIR,
              "RATINGS_PER_POEM": 3, "CALIBRATION_SIZE": 5, "ADMIN_PASSWORD": "pw", "ACCESS_CODE": None, "USERS": None}
    return create_site(config, {"DATABASE": tmp_path / "study2.db", **study2})


def token(html: str) -> str:
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def login(client, prefix: str, username: str):
    page = client.get(f"{prefix}/login").get_data(as_text=True)
    return client.post(f"{prefix}/login", data={"username": username, "csrf_token": token(page)})


def annotators(db) -> list[str]:
    con = sqlite3.connect(db)
    try:
        return [r[0] for r in con.execute("SELECT username FROM annotators")]
    finally:
        con.close()


def test_without_study2_data_the_site_is_study_1_alone(tmp_path):
    app = site(tmp_path, DATA_DIR=tmp_path / "missing")
    assert "study2_app" not in app.extensions
    r = app.test_client().get("/")
    assert r.status_code == 302 and r.headers["Location"].endswith("/login")


def test_home_page_offers_both_studies(tmp_path):
    c = site(tmp_path).test_client()
    html = c.get("/").get_data(as_text=True)
    assert "Study 1" in html and "Study 2" in html and 'href="/study2/"' in html
    assert 'href="/login"' in html                                  # study 1 before login


def test_study2_is_its_own_app(tmp_path):
    app = site(tmp_path)
    second = app.extensions["study2_app"]
    assert second.config["SESSION_COOKIE_NAME"] != app.config.get("SESSION_COOKIE_NAME", "session")
    assert second.config["SHOW_ENGINE_CHECKS"] is False and second.config["RATINGS_PER_POEM"] == 3
    c = app.test_client()
    assert c.get("/study2/healthz").get_json()["poems"] == 99
    assert "Study 2" in c.get("/study2/login").get_data(as_text=True)


def test_logins_and_ratings_stay_in_their_own_database(tmp_path):
    app = site(tmp_path)
    c = app.test_client()
    r = login(c, "/study2", "alice")
    assert r.status_code == 302 and r.headers["Location"].startswith("/study2/")
    nxt = c.get("/study2/next")
    assert re.search(r"/study2/poem/he2_\d{4}$", nxt.headers["Location"])
    assert annotators(tmp_path / "study2.db") == ["alice"] and annotators(tmp_path / "study1.db") == []
    # study 1 has its own session: not logged in there until the annotator logs in to it
    assert c.get("/next").headers["Location"].startswith("/login")
    login(c, "", "bob")
    assert re.search(r"/poem/he_\d{4}$", c.get("/next").headers["Location"])
    assert annotators(tmp_path / "study1.db") == ["bob"]


def test_study2_poem_page_hides_engine_verdicts_and_shows_the_prompt(tmp_path):
    app = site(tmp_path)
    c = app.test_client()
    login(c, "/study2", "alice")
    page = c.get(c.get("/study2/next").headers["Location"])
    html = page.get_data(as_text=True)
    assert page.status_code == 200 and "Study 2" in html
    poem = app.extensions["study2_app"].extensions["poem_store"].get(re.search(r"he2_\d{4}", html).group(0))
    assert poem.bhavam["source"] == "grid_p1" and poem.bhavam["te"][:20] in html


# ---------------------------------------------------------------------------------------------------------------------
# Q13 coherence: study 2 only; ratings made before it are served again, earlier answers filled in and editable
# ---------------------------------------------------------------------------------------------------------------------
from padya_eval import db as pdb                                            # noqa: E402
from padya_eval.rubric import QUESTIONS, STUDY2_QUESTIONS                   # noqa: E402


def full_answers(questions, value=4):
    return {q.key: (value if q.kind == "likert" else 1) for q in questions}


def poem_form(html: str, answers: dict) -> dict:
    return {"csrf_token": token(html), "started": re.search(r'name="started" value="([^"]+)"', html).group(1),
            **{k: str(v) for k, v in answers.items()}}


def test_study2_asks_coherence_after_q3_and_study1_does_not(tmp_path):
    c = site(tmp_path).test_client()
    login(c, "/study2", "alice")
    html = c.get(c.get("/study2/next").headers["Location"]).get_data(as_text=True)
    assert html.index('id="q-lexical"') < html.index('id="q-coherence"') < html.index('id="q-bhavam"')
    assert "పద్యం ఎంత అర్థవంతంగా ఉంది?" in html and "(answer 1–3, 13 first)" in html
    login(c, "", "bob")
    html1 = c.get(c.get("/next").headers["Location"]).get_data(as_text=True)
    assert 'name="coherence"' not in html1 and "(answer 1–3 first)" in html1


def test_study2_requires_coherence_and_records_rubric_v3(tmp_path):
    c = site(tmp_path).test_client()
    login(c, "/study2", "alice")
    url = c.get("/study2/next").headers["Location"]
    html = c.get(url).get_data(as_text=True)
    without = {k: v for k, v in full_answers(STUDY2_QUESTIONS).items() if k != "coherence"}
    assert c.post(url, data=poem_form(html, without)).status_code == 422
    assert c.post(url, data=poem_form(html, full_answers(STUDY2_QUESTIONS, 5))).status_code == 302
    row = sqlite3.connect(tmp_path / "study2.db").execute("SELECT answers, rubric_version FROM annotations").fetchone()
    assert json.loads(row[0])["coherence"] == 5 and row[1] == "3"


def test_old_study2_ratings_are_served_again_with_their_answers_editable(tmp_path):
    app = site(tmp_path)
    second = app.extensions["study2_app"]
    cal = second.config["CALIBRATION_IDS"]
    st = second.extensions["poem_store"]
    extra = next(e for e in st.ids if e not in cal)
    c = app.test_client()
    login(c, "/study2", "alice")
    conn = pdb.connect(tmp_path / "study2.db")
    aid = conn.execute("SELECT id FROM annotators WHERE username = 'alice'").fetchone()[0]
    old = full_answers(QUESTIONS, 2)                     # rated before Q13 existed (rubric v2)
    for e in [*cal, extra]:
        pdb.save_annotation(conn, aid, e, old, "earlier note", 30.0, "2")
    seen = []
    for _ in range(len(cal) + 1):                        # the calibration poems first, then the other old rating
        url = c.get("/study2/next").headers["Location"]
        e = url.rsplit("/", 1)[1]
        seen.append(e)
        html = c.get(url).get_data(as_text=True)
        assert "Your earlier answers are filled in, and you" in html and "new question: 13" in html
        assert re.search(r'name="readability" value="2" checked', html) and "disabled" not in html
        changed = {**old, "readability": 5, "coherence": 4}       # an earlier answer may be changed too
        assert c.post(url, data=poem_form(html, changed)).status_code == 302
        saved = json.loads(conn.execute("SELECT answers FROM annotations WHERE annotator_id = ? AND eval_id = ?",
                                        (aid, e)).fetchone()[0])
        assert saved["coherence"] == 4 and saved["readability"] == 5
        assert all(saved[k] == v for k, v in old.items() if k not in ("prasa", "readability"))  # prasa: None if no prāsa
        before = json.loads(conn.execute("SELECT answers FROM annotation_history WHERE annotator_id = ? AND eval_id = ?",
                                         (aid, e)).fetchone()[0])
        assert before["readability"] == 2 and "coherence" not in before    # the old version is kept in history
    assert seen[:len(cal)] and set(seen[:len(cal)]) == set(cal) and seen[-1] == extra
    assert conn.execute("SELECT COUNT(*) FROM annotation_history WHERE annotator_id = ?", (aid,)).fetchone()[0] == len(cal) + 1
    nxt = c.get("/study2/next").headers["Location"].rsplit("/", 1)[1]
    assert nxt not in seen                                # then new poems, as usual
    # opened again from "my ratings", a complete rating shows no note
    html = c.get(f"/study2/poem/{extra}").get_data(as_text=True)
    assert "Your earlier answers are filled in" not in html


def test_study2_admin_and_exports_include_coherence_study1_does_not(tmp_path):
    c = site(tmp_path).test_client()
    for prefix in ("/study2", ""):
        page = c.get(f"{prefix}/admin/login").get_data(as_text=True)
        c.post(f"{prefix}/admin/login", data={"password": "pw", "csrf_token": token(page)})
    head2 = c.get("/study2/admin/annotations.csv").get_data(as_text=True).lstrip("﻿").splitlines()[0].split(",")
    head1 = c.get("/admin/annotations.csv").get_data(as_text=True).lstrip("﻿").splitlines()[0].split(",")
    assert head2.index("lexical") + 1 == head2.index("coherence") and "coherence" not in head1
    assert "How meaningful (coherent) is the poem?" in c.get("/study2/admin/").get_data(as_text=True)
    assert "How meaningful (coherent) is the poem?" not in c.get("/admin/").get_data(as_text=True)


def test_admin_dashboards_have_a_tab_per_study(tmp_path):
    c = site(tmp_path).test_client()
    for prefix in ("/study2", ""):
        page = c.get(f"{prefix}/admin/login").get_data(as_text=True)
        c.post(f"{prefix}/admin/login", data={"password": "pw", "csrf_token": token(page)})
    for prefix, current in (("", "Study 1"), ("/study2", "Study 2")):
        html = c.get(f"{prefix}/admin/").get_data(as_text=True)
        assert 'href="/admin/"' in html and 'href="/study2/admin/"' in html
        assert re.search(rf'aria-current="page">{current}</a>', html) and f"Study dashboard · {current}" in html
    # the study 2 tab asks for the admin password once: its login is separate from study 1's
    other = tmp_path / "other"
    other.mkdir()
    c2 = site(other).test_client()
    page = c2.get("/admin/login").get_data(as_text=True)
    c2.post("/admin/login", data={"password": "pw", "csrf_token": token(page)})
    assert c2.get("/study2/admin/").headers["Location"].startswith("/study2/admin/login")


def test_without_study2_the_admin_has_no_tabs(tmp_path):
    app = site(tmp_path, DATA_DIR=tmp_path / "missing")
    c = app.test_client()
    page = c.get("/admin/login").get_data(as_text=True)
    c.post("/admin/login", data={"password": "pw", "csrf_token": token(page)})
    assert 'class="study-tabs"' not in c.get("/admin/").get_data(as_text=True)


def test_poem_pages_of_both_studies_have_the_dictionary_button(tmp_path):
    c = site(tmp_path).test_client()
    for prefix in ("", "/study2"):
        login(c, prefix, "alice")
        html = c.get(c.get(f"{prefix}/next").headers["Location"]).get_data(as_text=True)
        assert re.search(r'<a [^>]*href="https://andhrabharati.com/dictionary/"[^>]*data-dict-lookup', html)
