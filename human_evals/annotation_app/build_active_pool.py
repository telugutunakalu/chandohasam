#!/usr/bin/env python3
"""The first phase of the study: a 100-poem active subset of the 500-poem pool (user decision 2026-10-26).

    .venv/bin/python build_active_pool.py            # → data/active_pool.json (then a graceful restart of the app)

While data/active_pool.json exists, every annotator gets these 100 poems first (after the calibration set; each in
their own order), and can then go on to the rest of the 500 (store.PoemStore.phase_ids, assignment._select; user
decision 2026-10-26: "the first 100 are important, they can do more"). poems.json, the database and its fingerprint
stay the 500-poem study, so every rating already given is kept.

Selection (seeded): 20 poems from each of the five sources (bhagavatam, vemana, kuchimanchi, generated, reference),
so that the sources can be compared on equal footing. Within a source: every calibration poem first, then the poems
that already have ratings (the most rated first), then new poems chosen to cover the meters least represented in the
selection so far. The database is read only.
"""
from __future__ import annotations

import collections
import json
import random
import sqlite3
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PER_SOURCE = 20
SEED = 20261026


def main() -> None:
    poems = {p["id"]: p for p in json.loads((HERE / "data" / "poems.json").read_text(encoding="utf-8"))["poems"]}
    con = sqlite3.connect(f"file:{HERE / 'instance' / 'annotations.db'}?mode=ro", uri=True)
    calibration = [r[0] for r in con.execute("SELECT eval_id FROM calibration ORDER BY position")]
    rated = collections.Counter(r[0] for r in con.execute("SELECT eval_id FROM annotations"))
    con.close()
    source = lambda e: poems[e]["hidden"]["source_dataset"]                    # noqa: E731
    by_source = collections.defaultdict(list)
    for e in poems:
        by_source[source(e)].append(e)
    rng = random.Random(SEED)
    chosen: list[str] = []
    meter_count: collections.Counter = collections.Counter()
    for s in sorted(by_source):
        pick = [e for e in calibration if source(e) == s]
        prior = sorted((e for e in by_source[s] if e in rated and e not in pick), key=lambda e: (-rated[e], e))
        pick += prior[: max(0, PER_SOURCE - len(pick))]
        for e in pick:
            meter_count[poems[e]["meter"]] += 1
        rest = [e for e in by_source[s] if e not in pick]
        rng.shuffle(rest)
        while len(pick) < PER_SOURCE and rest:
            e = min(rest, key=lambda x: meter_count[poems[x]["meter"]])        # the least represented meter
            rest.remove(e)
            pick.append(e)
            meter_count[poems[e]["meter"]] += 1
        chosen += pick
    assert set(calibration) <= set(chosen)
    counts = {"by_source": dict(collections.Counter(source(e) for e in chosen)),
              "calibration": len(calibration), "already_rated": sum(e in rated for e in chosen),
              "ratings_on_them": sum(rated[e] for e in chosen), "meters": len({poems[e]["meter"] for e in chosen})}
    out = {"phase": "phase 1: 100 poems", "created": time.strftime("%Y-%m-%d %H:%M"), "seed": SEED,
           "rule": f"{PER_SOURCE} per source; calibration first, then already rated, then least represented meters",
           "counts": counts, "ids": [e for e in poems if e in set(chosen)]}             # in poems.json order
    (HERE / "data" / "active_pool.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                                    encoding="utf-8")
    print(json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    main()
