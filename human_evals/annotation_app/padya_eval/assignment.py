# -*- coding: utf-8 -*-
"""
Which poem an annotator sees next. The design gives every poem enough overlapping
ratings for inter-annotator agreement.

Two modes, chosen by RATINGS_PER_POEM:

* **all** (the default, ``None``): every annotator rates every poem, the calibration set
  first and then the rest in their own order. The design is fully crossed.
* **k** (a number): every annotator rates the calibration set, and the rest are shared
  out until each poem has k ratings (points 2 and 3 below).

1. **Calibration set.** Every annotator first rates the same small stratified set
   (CALIBRATION_SIZE poems, spread across sources and meters). It is fully crossed,
   so the admin page can compare every pair of annotators on it before the main pass.
2. **Redundancy k.** After that, each poem is served until it has k ratings
   (RATINGS_PER_POEM, default 3). The queue is depth-first: poems that already have
   some ratings are completed before untouched ones are opened, so the study yields
   fully rated poems even if it stops early.
3. **Claims.** A served poem is claimed by its annotator for CLAIM_TTL minutes. Other
   annotators count the claim towards k, so several people working at once do not
   all pile onto the same poem.
4. **Order.** Ties are broken by a hash of (annotator, poem). Each annotator therefore
   meets the poems in their own fixed order, which spreads order effects and stays
   stable across reloads.

A poem an annotator rated or skipped is never served to that annotator again.
"""
from __future__ import annotations

import hashlib
import random
import time
from collections import Counter, defaultdict
from typing import Optional, Sequence

from . import db


def order_key(username: str, eval_id: str) -> int:
    return int.from_bytes(hashlib.sha256(f"{username}\x1f{eval_id}".encode()).digest()[:8], "big")


def choose_calibration(poems: Sequence, size: int, seed: int = 42) -> list[str]:
    """A stratified calibration set: sources in proportion (at least one each), meters spread within a source."""
    if size <= 0 or not poems:
        return []
    size = min(size, len(poems))
    rng = random.Random(seed)
    by_source: dict[str, list] = defaultdict(list)
    for p in poems:
        by_source[p.hidden["source_dataset"]].append(p)
    sources = sorted(by_source)
    total = len(poems)
    # largest-remainder allocation, then make sure every source gets one when there is room
    raw = {s: size * len(by_source[s]) / total for s in sources}
    alloc = {s: int(raw[s]) for s in sources}
    for s in sorted(sources, key=lambda s: raw[s] - alloc[s], reverse=True)[: size - sum(alloc.values())]:
        alloc[s] += 1
    if size >= len(sources):
        for s in sources:
            if alloc[s] == 0:
                donor = max(sources, key=lambda d: alloc[d])
                alloc[donor] -= 1
                alloc[s] = 1
    chosen: list[str] = []
    for s in sources:
        by_meter: dict[str, list] = defaultdict(list)
        for p in by_source[s]:
            by_meter[p.meter].append(p.id)
        meters = sorted(by_meter)
        rng.shuffle(meters)
        for m in meters:
            rng.shuffle(by_meter[m])
        picked: list[str] = []
        while len(picked) < alloc[s] and any(by_meter.values()):
            for m in meters:
                if by_meter[m] and len(picked) < alloc[s]:
                    picked.append(by_meter[m].pop())
        chosen.extend(picked)
    return sorted(chosen)


def ensure_calibration(conn, store, size: int, seed: int = 42) -> list[str]:
    """Return the study's calibration set, choosing and storing it on first use.

    The stored set wins over later changes of ``size``, so the set never shifts mid-study.
    """
    ids = db.calibration_ids(conn)
    if ids or size <= 0:
        return [i for i in ids if i in store]
    ids = choose_calibration(store.poems, size, seed)
    conn.execute("BEGIN IMMEDIATE")
    try:
        if not db.calibration_ids(conn):
            db.set_calibration(conn, ids)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return db.calibration_ids(conn)


def next_poem(conn, store, annotator, *, k: Optional[int], claim_ttl_s: float, calibration: Sequence[str],
              now: Optional[float] = None) -> Optional[str]:
    """The next poem for ``annotator`` (a row with id and username), claimed for them; None when done.

    ``k`` None means every annotator rates every poem.
    """
    now = time.time() if now is None else now
    conn.execute("BEGIN IMMEDIATE")          # serialise selection + claim across workers
    try:
        choice = _select(conn, store, annotator, k=k, claim_ttl_s=claim_ttl_s, calibration=calibration, now=now)
        if choice is None:
            db.release_claim(conn, annotator["id"])
        else:
            db.claim(conn, annotator["id"], choice, at=now)
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return choice


def _select(conn, store, annotator, *, k, claim_ttl_s, calibration, now) -> Optional[str]:
    aid, user = annotator["id"], annotator["username"]
    excluded = db.rated_ids(conn, aid) | db.skipped_ids(conn, aid)
    key = lambda e: order_key(user, e)                       # noqa: E731

    pending_cal = [e for e in calibration if e not in excluded and e in store]
    if pending_cal:
        return min(pending_cal, key=key)
    if k is None:                            # everyone rates everything: just their own order
        rest = [e for e in store.ids if e not in excluded]
        return min(rest, key=key) if rest else None

    counts = db.rating_counts(conn)
    others: Counter = Counter()
    mine = None
    for c in db.active_claims(conn, claim_ttl_s, now):
        if c["annotator_id"] == aid:
            mine = c["eval_id"]
        else:
            others[c["eval_id"]] += 1

    def open_slots(e: str) -> int:
        return k - counts.get(e, 0) - others.get(e, 0)

    if mine and mine not in excluded and mine in store and k - counts.get(mine, 0) > 0:
        return mine                          # keep serving the poem already on their screen
    candidates = [e for e in store.ids if e not in excluded and open_slots(e) > 0]
    if not candidates:
        return None
    return min(candidates, key=lambda e: (-counts.get(e, 0), key(e)))


def target_per_poem(conn, k: Optional[int]) -> int:
    """Ratings each poem should end with: k, or (all mode) the number of annotators signed up."""
    if k is not None:
        return k
    return max(1, conn.execute("SELECT COUNT(*) FROM annotators").fetchone()[0])


def study_progress(conn, store, k: Optional[int]) -> dict:
    k = target_per_poem(conn, k)
    counts = db.rating_counts(conn)
    complete = sum(1 for e in store.ids if counts.get(e, 0) >= k)
    needed = sum(max(0, k - counts.get(e, 0)) for e in store.ids)
    histogram = Counter(min(counts.get(e, 0), k) for e in store.ids)
    return {"poems": len(store), "complete": complete, "ratings_needed": needed, "target": k,
            "ratings": sum(counts.values()), "histogram": {n: histogram.get(n, 0) for n in range(k + 1)}}
