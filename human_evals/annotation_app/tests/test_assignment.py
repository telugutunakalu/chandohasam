# -*- coding: utf-8 -*-
"""The queue: calibration first, k ratings per poem, depth-first filling, claims, skips."""
from collections import Counter
from dataclasses import dataclass, field

import pytest

from padya_eval import assignment, db


@dataclass(frozen=True)
class FakePoem:
    id: str
    meter: str
    hidden: dict = field(default_factory=dict)


class FakeStore:
    def __init__(self, n=40):
        sources = ["bhagavatam"] * 18 + ["generated"] * 10 + ["vemana"] * 6 + ["kuchimanchi"] * 4 + ["reference"] * 2
        meters = ["utpalamala", "kandamu", "seesamu", "tetagiti"]
        self.poems = [FakePoem(f"he_{i:04d}", meters[i % 4], {"source_dataset": sources[i % len(sources)]})
                      for i in range(1, n + 1)]
        self.ids = [p.id for p in self.poems]

    def __contains__(self, e):
        return e in self.ids

    def __len__(self):
        return len(self.poems)


@pytest.fixture
def conn(tmp_path):
    path = tmp_path / "q.db"
    db.init_db(path, "fake/test/40")
    c = db.connect(path)
    yield c
    c.close()


def annotator(conn, name):
    return db.get_or_create_annotator(conn, name)


def rate(conn, who, eval_id):
    db.save_annotation(conn, who["id"], eval_id, {"readability": 3}, "", 10.0, "1")


def serve(conn, store, who, k=3, cal=(), now=1000.0, ttl=1800):
    return assignment.next_poem(conn, store, who, k=k, claim_ttl_s=ttl, calibration=list(cal), now=now)


def test_choose_calibration_is_stratified_and_deterministic():
    store = FakeStore()
    cal = assignment.choose_calibration(store.poems, 10, seed=1)
    assert len(cal) == len(set(cal)) == 10
    assert cal == assignment.choose_calibration(store.poems, 10, seed=1)
    by_id = {p.id: p for p in store.poems}
    sources = Counter(by_id[e].hidden["source_dataset"] for e in cal)
    assert set(sources) == {"bhagavatam", "generated", "vemana", "kuchimanchi", "reference"}
    assert sources["bhagavatam"] >= sources["generated"] >= sources["reference"]
    assert len({by_id[e].meter for e in cal}) == 4


def test_choose_calibration_edge_sizes():
    store = FakeStore(6)
    assert assignment.choose_calibration(store.poems, 0) == []
    assert sorted(assignment.choose_calibration(store.poems, 50)) == store.ids


def test_ensure_calibration_is_stored_once(conn):
    store = FakeStore()
    first = assignment.ensure_calibration(conn, store, 8, seed=3)
    assert len(first) == 8
    assert assignment.ensure_calibration(conn, store, 20, seed=99) == first     # later size changes are ignored


def test_calibration_comes_first_for_everyone(conn):
    store = FakeStore()
    cal = assignment.ensure_calibration(conn, store, 5)
    for name in ("a", "b"):
        who = annotator(conn, name)
        seen = []
        for _ in range(5):
            e = serve(conn, store, who, cal=cal)
            seen.append(e)
            rate(conn, who, e)
        assert sorted(seen) == sorted(cal)
        assert serve(conn, store, who, cal=cal) not in cal


def test_annotators_meet_calibration_in_different_orders(conn):
    store = FakeStore()
    cal = assignment.ensure_calibration(conn, store, 8)
    firsts = {serve(conn, store, annotator(conn, f"user{i}"), cal=cal) for i in range(8)}
    assert len(firsts) > 1


def test_depth_first_completes_started_poems(conn):
    store = FakeStore()
    a, b = annotator(conn, "a"), annotator(conn, "b")
    e = serve(conn, store, a)
    rate(conn, a, e)
    assert serve(conn, store, b) == e            # b picks up the poem a started


def test_k_caps_ratings_per_poem(conn):
    store = FakeStore(3)
    users = [annotator(conn, f"u{i}") for i in range(4)]
    for u in users[:2]:
        while (e := serve(conn, store, u, k=2)) is not None:
            rate(conn, u, e)
    assert all(n == 2 for n in db.rating_counts(conn).values())
    assert serve(conn, store, users[2], k=2) is None


def test_claims_stop_concurrent_pile_up(conn):
    store = FakeStore()
    a, b, c = (annotator(conn, n) for n in "abc")
    first = serve(conn, store, a, k=3)
    rate(conn, a, first)
    rate(conn, b, first)                          # first now has 2 of 3 ratings
    d = annotator(conn, "d")
    got_c = serve(conn, store, c, k=3)            # c claims the last slot
    got_d = serve(conn, store, d, k=3)
    assert got_c == first
    assert got_d != first                         # the claim counts towards k


def test_expired_claims_are_ignored(conn):
    store = FakeStore()
    a, b, c = (annotator(conn, n) for n in "abc")
    e = serve(conn, store, a, k=3)
    rate(conn, a, e)
    rate(conn, b, e)
    assert serve(conn, store, c, k=3, now=1000) == e
    d = annotator(conn, "d")
    assert serve(conn, store, d, k=3, now=1000 + 3600, ttl=1800) == e     # c's claim has expired


def test_own_claim_is_served_again_on_reload(conn):
    store = FakeStore()
    a, b = annotator(conn, "a"), annotator(conn, "b")
    mine = serve(conn, store, a)
    other = serve(conn, store, b)
    rate(conn, b, other)                          # other is now the most-rated poem a has not done
    assert serve(conn, store, a) == mine


def test_skips_are_never_served_again(conn):
    store = FakeStore(4)
    a = annotator(conn, "a")
    e = serve(conn, store, a)
    db.skip(conn, a["id"], e)
    served = set()
    while (x := serve(conn, store, a, k=1)) is not None:
        served.add(x)
        rate(conn, a, x)
    assert e not in served and len(served) == 3


def test_full_study_simulation(conn):
    """Four annotators work in turns until the queue is empty: every poem gets exactly k ratings
    (calibration poems: one per annotator), and nobody rates a poem twice."""
    store = FakeStore(40)
    cal = assignment.ensure_calibration(conn, store, 4)
    users = [annotator(conn, f"ann{i}") for i in range(4)]
    k = 3
    active = list(users)
    t = 0.0
    while active:
        for u in list(active):
            t += 1
            e = serve(conn, store, u, k=k, cal=cal, now=t)
            if e is None:
                active.remove(u)
                continue
            assert e not in db.rated_ids(conn, u["id"])
            rate(conn, u, e)
    counts = db.rating_counts(conn)
    assert set(counts) == set(store.ids)
    for e in store.ids:
        assert counts[e] == (4 if e in cal else k)
    progress = assignment.study_progress(conn, store, k)
    assert progress["complete"] == 40 and progress["ratings_needed"] == 0


def test_all_mode_serves_every_poem_to_every_annotator(conn):
    store = FakeStore(12)
    cal = assignment.ensure_calibration(conn, store, 3)
    orders = []
    for name in ("a", "b", "c"):
        who = annotator(conn, name)
        order = []
        while (e := serve(conn, store, who, k=None, cal=cal)) is not None:
            order.append(e)
            rate(conn, who, e)
        assert sorted(order) == sorted(store.ids) and set(order[:3]) == set(cal)
        orders.append(order)
    assert len({tuple(o) for o in orders}) > 1                    # personal orders differ
    assert set(db.rating_counts(conn).values()) == {3}
    progress = assignment.study_progress(conn, store, None)
    assert progress["target"] == 3 and progress["complete"] == 12


def test_all_mode_ignores_other_annotators_claims(conn):
    store = FakeStore(3)
    a, b = annotator(conn, "a"), annotator(conn, "b")
    first_a = serve(conn, store, a, k=None)
    for _ in range(3):
        e = serve(conn, store, b, k=None)
        rate(conn, b, e)
    assert serve(conn, store, b, k=None) is None and first_a in db.rated_ids(conn, b["id"])
