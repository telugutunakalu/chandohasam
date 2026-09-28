"""Level 1 (sense check) — how often would prāsa and yati pass by chance?

A prosodic-integrity rate is informative only in proportion to how hard each
rule is to satisfy. This script measures each rule's chance pass rate with
meter_engine's own yati and prāsa engines, by pairing material from UNRELATED
poems of the same metre:

    yati   the vaḷi (first akshara) of a pāda  vs  the yati-seat akshara of a
           random pāda of another poem of the same metre.
           Real pairs (vaḷi and seat of the same pāda) are re-checked the same
           way, out of context, so real and chance rates are comparable.
    prāsa  4-pāda poems of a prāsa metre: the real stanza, and a stanza whose
           pādas 2-4 come from three random other poems of the same metre.

A rule whose chance rate is close to its real rate cannot certify much.
Only poems that scan as their labelled metre are used (common/scansion.py).
Every seat and every stanza is checked; the prāsa evaluations (about 0.1 s
each) run in parallel.

Writes outputs/level1_chance_pass_rates.json

Run:  python level1_chance_pass_rates.py [--workers 12] [--datasets ...]
"""
import argparse
import random
from collections import defaultdict
from multiprocessing import Pool

import config
from common.controls import corpus_seed
from common.dataset import add_dataset_argument, by_corpus, load_poems
from common.io import pct, print_table, save_result
from common.scansion import engine_name, scan_poems
import prasa_engine                      # noqa: E402  (meter_engine, on the path via common.scansion)
from yati import check as yati_check     # noqa: E402


def yati_rates(poems, verdicts, profile, rng) -> dict:
    """Real vs chance yati pass rate over every seat of one group of poems."""
    seats_by_metre = defaultdict(list)                 # metre -> [(poem key, vaḷi, seat akshara)]
    for p in poems:
        for s in verdicts[p.key][profile].get("yati_seats", []):
            seats_by_metre[p.metre].append((p.key, s[0], s[1]))
    real = chance = n = n_chance = 0
    for metre, seats in seats_by_metre.items():
        for key, vali, seat in seats:
            real += yati_check(vali, seat, profile, sandhi=config.YATI_SANDHI).matched
            n += 1
            other = seats[rng.randrange(len(seats))]
            if other[0] != key:
                chance += yati_check(vali, other[2], profile, sandhi=config.YATI_SANDHI).matched
                n_chance += 1
    return {"seats": n, "real_pct": pct(real, n), "chance_pct": pct(chance, n_chance)}


def prasa_stanzas(poems, verdicts, profile, rng) -> list:
    """(real pādas, mixed pādas, engine metre) for every 4-pāda prāsa poem of one group."""
    by_metre = defaultdict(list)
    for p in poems:
        if len(p.lines) == 4 and verdicts[p.key][profile].get("prasa_applicable"):
            by_metre[p.metre].append(p)
    jobs = []
    for metre, group in by_metre.items():
        if len(group) < 4:
            continue
        for p in group:
            others = rng.sample([q for q in group if q.key != p.key], 3)
            mixed = [p.lines[0], others[0].lines[1], others[1].lines[2], others[2].lines[3]]
            jobs.append((list(p.lines), mixed, engine_name(metre), profile))
    return jobs


def _prasa_pair(job) -> tuple:
    real, mixed, meter, profile = job
    return (prasa_engine.evaluate(real, profile=profile, meter=meter).matched,
            prasa_engine.evaluate(mixed, profile=profile, meter=meter).matched)


def prasa_rates(jobs, pool) -> dict:
    results = pool.map(_prasa_pair, jobs, chunksize=8)
    n = len(results)
    return {"stanzas": n, "real_pct": pct(sum(r for r, _ in results), n),
            "chance_pct": pct(sum(c for _, c in results), n)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=12)
    add_dataset_argument(ap)
    args = ap.parse_args()

    poems = load_poems(tuple(args.datasets))
    verdicts = scan_poems(poems, args.workers)
    scanned = [p for p in poems if p.metre and verdicts[p.key]["scans_as_label"]]

    result = {}
    rows = []
    with Pool(args.workers) as pool:
        for corpus, group in by_corpus(scanned).items():
            result[corpus] = {}
            for profile in config.SCAN_PROFILES:
                rng = random.Random(corpus_seed(config.SEED, f"{corpus}/{profile}"))
                print(f"  {corpus} / {profile} ...", flush=True)
                y = yati_rates(group, verdicts, profile, rng)
                pr = prasa_rates(prasa_stanzas(group, verdicts, profile, rng), pool)
                result[corpus][profile] = {"yati": y, "prasa": pr}
                rows.append([corpus, profile, y["seats"], y["real_pct"], y["chance_pct"],
                             pr["stanzas"], pr["real_pct"], pr["chance_pct"]])
    print_table(["corpus", "profile", "yati seats", "yati real %", "yati CHANCE %",
                 "prāsa stanzas", "prāsa real %", "prāsa CHANCE %"], rows,
                "Chance pass rates: material from unrelated poems of the same metre")
    save_result("level1_chance_pass_rates", result)


if __name__ == "__main__":
    main()
