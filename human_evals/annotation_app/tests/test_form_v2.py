"""The poem form under rubric v2: questions 11–12 with their labels; a v1 rating reopens with its answers filled in."""
from padya_eval import db
from padya_eval.rubric import QUESTIONS


def test_form_shows_the_two_new_questions(client, store):
    client.login("alice")
    html = client.get(f"/poem/{store.ids[0]}").get_data(as_text=True)
    assert "ఇది గ్రాంథికమా, ఆధునికమా?" in html and "గ్రాంథికం · Archaic" in html and "ఆధునికం · Modern" in html
    assert "Do you think this poem is AI-generated?" in html
    assert 'name="register"' in html and 'name="ai_generated"' in html


def test_a_v1_rating_reopens_prefilled(app, client, store):
    client.login("alice")
    eval_id = store.ids[0]
    v1 = {q.key: None for q in QUESTIONS[:10]}
    v1.update(readability=2, comprehension=4, lexical=5, poetic=1)
    with app.app_context():
        conn = db.connect(app.config["DATABASE"])
        aid = conn.execute("SELECT id FROM annotators WHERE username = 'alice'").fetchone()[0]
        db.save_annotation(conn, aid, eval_id, v1, "earlier comment", 60.0, "1")
        conn.commit()
        conn.close()
    html = client.get(f"/poem/{eval_id}").get_data(as_text=True)
    for key, value in (("readability", 2), ("comprehension", 4), ("lexical", 5), ("poetic", 1)):
        assert f'name="{key}" value="{value}" checked' in html
    assert 'name="register" value="0" checked' not in html and 'name="register" value="1" checked' not in html
    assert "earlier comment" in html
