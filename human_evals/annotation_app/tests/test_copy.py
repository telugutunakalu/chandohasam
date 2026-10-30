# -*- coding: utf-8 -*-
"""The poem page's copy button carries the poem's lines as printed, one per line, and nothing hidden."""
import html
import re


def test_copy_button_holds_the_poem_lines(client, store):
    client.login("alice")
    eval_id = client.get("/next").headers["Location"].rsplit("/", 1)[-1]
    page = client.get(f"/poem/{eval_id}").get_data(as_text=True)
    copied = html.unescape(re.search(r'data-copy="([^"]*)"', page).group(1))
    poem = store.get(eval_id)
    assert copied == "\n".join(poem.plain_lines) and copied.count("\n") == len(poem.lines) - 1
    assert poem.hidden["source_id"] not in copied
