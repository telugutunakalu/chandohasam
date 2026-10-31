# -*- coding: utf-8 -*-
"""Highlighted passages and favourite poems: the span arithmetic, the routes, the database rows."""
import html
import json
import re

from conftest import FormClient
from padya_eval import db
from padya_eval.highlights import clean_span, marked_lines, span_text

JSON = {"Accept": "application/json"}


def rows(app, table):
    conn = db.connect(app.config["DATABASE"])
    try:
        return [dict(r) for r in conn.execute(f"SELECT * FROM {table} ORDER BY rowid")]
    finally:
        conn.close()


def line_texts(page: str) -> list[str]:
    """The text of each .poem-line as a browser sees it (tags stripped)."""
    return [html.unescape(re.sub(r"<[^>]+>", "", m)) for m in re.findall(r'<p class="poem-line">(.*?)</p>', page, re.S)]


# -----------------------------------------------------------------------------
# spans
# -----------------------------------------------------------------------------
LINES = ["ab cd ", " ef", "gh"]


def test_clean_span_trims_white_space_across_lines():
    assert clean_span(LINES, 0, 2, 0, 6) == (0, 3, 0, 5)              # " cd " → "cd"
    assert clean_span(LINES, 0, 5, 1, 3) == (1, 1, 1, 3)              # " " + line end + " ef" → "ef"
    assert clean_span(LINES, 0, 0, 2, 0) == (0, 0, 1, 3)              # ends at a line start → back to "ef"
    assert span_text(LINES, (0, 3, 2, 1)) == "cd \n ef\ng"


def test_clean_span_rejects_empty_and_out_of_range():
    assert clean_span(LINES, 0, 2, 0, 3) is None                       # only a space
    assert clean_span(LINES, 0, 3, 0, 3) is None
    assert clean_span(LINES, 1, 0, 0, 2) is None                       # backwards
    assert clean_span(LINES, 0, 0, 3, 0) is None
    assert clean_span(LINES, 0, 0, 0, 7) is None
    assert clean_span(LINES, 0, -1, 0, 2) is None


def test_marked_lines_cuts_tokens_at_the_span_edges():
    lines = [[{"t": "ab"}, {"t": " ", "s": 1}, {"t": "cde"}], [{"t": "fg"}]]
    out = marked_lines(lines, [(0, 1, 0, 4), (0, 3, 1, 1)])
    assert [t["parts"] for t in out[0]] == [[("a", False), ("b", True)], [(" ", True)], [("cde", True)]]
    assert [t["parts"] for t in out[1]] == [[("f", True), ("g", False)]]
    assert all(t["parts"] == [(t["t"], False)] for t in marked_lines(lines, [])[0])


def test_rendered_lines_are_the_poem_text_for_every_poem(app, store):
    with app.test_request_context():
        from flask import render_template
        for p in store.poems:
            spans = [(0, 1, len(p.lines) - 1, 2)]
            page = render_template("_poem_text.html", poem=p, marked_lines=marked_lines(p.lines, spans))
            assert line_texts(page) == p.plain_lines, p.id


# -----------------------------------------------------------------------------
# routes
# -----------------------------------------------------------------------------
def test_highlight_saved_rendered_and_removed(client, app, store):
    p = store.poems[0]
    client.login("alice")
    word = p.plain_lines[0].split()[0]
    r = client.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 0, "end_line": 0,
                                                      "end_char": len(word) + 1}, headers=JSON)
    assert r.status_code == 200
    body = r.get_json()
    assert body["count"] == 1 and f'<mark class="hl">' in body["poem_html"] and word in body["list_html"]
    assert line_texts(body["poem_html"]) == p.plain_lines
    (h,) = rows(app, "highlights")
    assert (h["start_line"], h["start_char"], h["end_line"], h["end_char"], h["text"]) == (0, 0, 0, len(word), word)

    # the same passage again is not stored twice; the poem page shows it
    client.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 0, "end_line": 0,
                                                  "end_char": len(word)}, headers=JSON)
    assert len(rows(app, "highlights")) == 1
    page = client.get(f"/poem/{p.id}").get_data(as_text=True)
    assert 'id="hl-list"' in page and 'aria-label="My highlights (1)"' in page and '<mark class="hl">' in page

    r = client.post_form(f"/poem/{p.id}/highlights/{h['id']}/delete", headers=JSON)
    assert r.status_code == 200 and r.get_json()["count"] == 0 and rows(app, "highlights") == []
    assert client.post_form(f"/poem/{p.id}/highlights/{h['id']}/delete").status_code == 404


def test_highlight_spanning_lines_keeps_the_text_of_each(client, app, store):
    p = next(p for p in store.poems if len(p.lines) >= 2)
    client.login("alice")
    r = client.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 3, "end_line": 1,
                                                      "end_char": 4}, headers=JSON)
    assert r.status_code == 200
    a, b = p.plain_lines[0], p.plain_lines[1]
    assert rows(app, "highlights")[0]["text"] == (a[3:] + "\n" + b[:4]).strip()


def test_highlight_without_javascript_comes_back_to_the_poem(client, store):
    p = store.poems[0]
    client.login("alice")
    r = client.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 0, "end_line": 0,
                                                      "end_char": 3, "next": "/mine"})
    assert r.status_code == 302 and r.headers["Location"].endswith(f"/poem/{p.id}?next=/mine")


def test_bad_highlights_are_refused(client, app, store):
    p = store.poems[0]
    client.login("alice")
    for form in ({"start_line": 0, "start_char": 0, "end_line": 99, "end_char": 1},
                 {"start_line": 0, "start_char": 0, "end_line": 0, "end_char": 0},
                 {"start_line": "x", "start_char": 0, "end_line": 0, "end_char": 2},
                 {"start_line": 0}):
        assert client.post_form(f"/poem/{p.id}/highlights", form, headers=JSON).status_code == 400
    assert client.post_form("/poem/nope/highlights", {"start_line": 0, "start_char": 0, "end_line": 0,
                                                      "end_char": 2}).status_code == 404
    r = client.post(f"/poem/{p.id}/highlights", data={"start_line": 0, "start_char": 0, "end_line": 0,
                                                       "end_char": 2})                      # no CSRF token
    assert r.status_code == 400 and rows(app, "highlights") == []


def test_highlights_are_per_annotator(app, store):
    p = store.poems[0]
    alice, bob = FormClient(app.test_client()), FormClient(app.test_client())
    alice.login("alice")
    bob.login("bob")
    alice.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 0, "end_line": 0, "end_char": 3})
    (h,) = rows(app, "highlights")
    assert "My highlights" not in bob.get(f"/poem/{p.id}").get_data(as_text=True)
    assert bob.post_form(f"/poem/{p.id}/highlights/{h['id']}/delete").status_code == 404
    assert len(rows(app, "highlights")) == 1


def test_routes_need_login(client, store):
    p = store.poems[0]
    for url in (f"/poem/{p.id}/highlights", f"/poem/{p.id}/highlights/1/delete", f"/poem/{p.id}/favorite"):
        r = client.post_form(url, {"on": "1"})
        assert r.status_code == 302 and "/login" in r.headers["Location"]


# -----------------------------------------------------------------------------
# favourites
# -----------------------------------------------------------------------------
def test_favorite_toggles_and_shows(client, app, store):
    p = store.poems[0]
    client.login("alice")
    assert 'aria-pressed="false"' in client.get(f"/poem/{p.id}").get_data(as_text=True)
    r = client.post_form(f"/poem/{p.id}/favorite", {"on": "1"}, headers=JSON)
    assert r.get_json() == {"favorite": True}
    client.post_form(f"/poem/{p.id}/favorite", {"on": "1"}, headers=JSON)          # idempotent
    assert [f["eval_id"] for f in rows(app, "favorites")] == [p.id]
    page = client.get(f"/poem/{p.id}").get_data(as_text=True)
    assert 'aria-pressed="true"' in page and 'name="on" value="0"' in page
    client.post_form("/poem/" + p.id + "/skip")
    assert "1 favourite" in client.get("/mine").get_data(as_text=True)

    r = client.post_form(f"/poem/{p.id}/favorite", {"on": "0"})                     # without JavaScript
    assert r.status_code == 302 and r.headers["Location"].endswith(f"/poem/{p.id}")
    assert rows(app, "favorites") == []
    assert client.post_form("/poem/nope/favorite", {"on": "1"}).status_code == 404


def test_admin_export(client, app, store):
    p = store.poems[0]
    client.login("alice")
    client.post_form(f"/poem/{p.id}/highlights", {"start_line": 0, "start_char": 0, "end_line": 0, "end_char": 3})
    client.post_form(f"/poem/{p.id}/favorite", {"on": "1"})
    assert client.get("/admin/highlights.json").status_code == 302                  # admin only
    client.post_form("/admin/login", {"password": "pw"})
    assert b"highlights.json" in client.get("/admin/").data
    data = json.loads(client.get("/admin/highlights.json").data)
    assert [(h["eval_id"], h["username"], h["text"]) for h in data["highlights"]] == [(p.id, "alice", p.plain_lines[0][:3].strip())]
    assert [(f["eval_id"], f["username"]) for f in data["favorites"]] == [(p.id, "alice")]
