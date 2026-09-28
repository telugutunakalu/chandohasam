"""meter_engine scansion of every poem, cached (used by level 1 and the summary).

scan(lines, label) runs the engine once per poem:

    1. identification (the slow step): scansion into guru/laghu, then every metre
       of the catalogue that the lines fit (indic_meter_dawg.identify_text)
    2. `scans_as_label`: the poem's labelled metre is among those metres (gaṇa check)
    3. for each profile in config.SCAN_PROFILES, the full analysis under the
       labelled metre (chandohasam.analyze): prāsa, yati, and `valid` = all rules.
       A poem whose label does not scan fails `valid`; its prāsa and yati are
       None (there is no frame to check them in). An unlabelled poem is checked
       under the metre the engine finds best.

Corpus labels use the corpus's names; meter_engine/scripts/corpus_run.NAME_MAP
maps them to the engine's catalogue names (aataveladi -> ataveladi, ...).

Layout: meter_engine reads a seesa pāda as two printed half-lines, the way
Bhagavatam and Kuchimanchi write it. Chandassu writes many seesa pādas on one
line with " - " between the halves; lines_for_scansion() splits those, so the
metric measures the verse and not the line layout.

scan_poems(poems) scans in parallel and caches each verdict under
outputs/cache/scansion.json, keyed by poem and by a hash of its lines and
label, so edited poems are rescanned and everything else is reused.
"""
import hashlib
import json
import re
import sys
from multiprocessing import Pool

import config

sys.path.insert(0, str(config.METER_ENGINE_DIR))
from chandohasam import analyze                       # noqa: E402
from indic_meter_dawg import identify_text            # noqa: E402
from scripts.corpus_run import NAME_MAP               # noqa: E402

CACHE = config.CACHE_DIR / "scansion.json"


# " - " between the halves; also "X- Y" and "X -Y" (the space on one side only) and "X- - Y" (a word
# running across the halves). A dash at the end of a line, or inside a word, is not a separator.
HALF_LINE_SEPARATOR = re.compile(r"(?<=\S)(?:-\s+-\s*|\s*-\s+|\s+-\s*)(?=\S)")


def engine_name(label):
    return NAME_MAP.get(label, label) if label else None


def lines_for_scansion(poem) -> tuple:
    """The poem's lines as meter_engine reads them: a seesa pāda printed on one
    line with " - " between its halves becomes two half-lines. A dash that ends
    a line (a word running into the next line) is not a separator."""
    if poem.metre != "seesamu":
        return poem.lines
    return tuple(h.strip() for line in poem.lines for h in HALF_LINE_SEPARATOR.split(line) if h.strip())


def layout_split(poem) -> bool:
    """Whether lines_for_scansion() had to split this poem's lines."""
    return lines_for_scansion(poem) != poem.lines


def _fits(candidate, target) -> bool:
    return candidate.meter == target or getattr(candidate, "is_variant_of", None) == target


def _yati_seats(analysis) -> list:
    """[vaḷi akshara, yati akshara, rule, matched, needs a sandhi hypothesis, prāsa-yati] per seat."""
    seats = []
    for unit in analysis.units:
        for line in unit.lines:
            for s in line.yati:
                if len(s.aksharas) >= 2:
                    seats.append([s.aksharas[0], s.aksharas[1], s.rule, s.matched, s.hypothesis, s.prasa_yati])
    return seats


def _prasa_applicable(analysis) -> bool:
    return any(u.prasa is not None and u.prasa.applicable for u in analysis.units)


def scan(lines, label=None) -> dict:
    """The engine's verdict on one poem (see module docstring)."""
    ident = identify_text(list(lines))
    target = engine_name(label)
    label_candidate = next((c for c in ident.candidates if _fits(c, target)), None) if target else None
    verdict = {
        "identified": ident.identified,
        "best": ident.best.label if ident.best else None,
        "candidates": [c.label for c in ident.candidates],
        "labelled": target is not None,
        "scans_as_label": label_candidate is not None,
        "best_is_label": bool(target and ident.best and _fits(ident.best, target)),
    }
    # the metre to check prāsa and yati in: the label when it scans, the engine's best when unlabelled
    if label_candidate is not None:
        meter = label_candidate.meter
    elif target is None and ident.best is not None:
        meter = ident.best.meter
    else:
        meter = None
    for profile in config.SCAN_PROFILES:
        if meter is None:
            verdict[profile] = {"prasa": None, "yati": None, "valid": False}
            continue
        a = analyze(list(lines), profile=profile, yati_sandhi=config.YATI_SANDHI, meter=meter,
                    identification=ident)
        verdict[profile] = {
            "prasa_applicable": _prasa_applicable(a),
            "prasa": a.prasa_matched,
            "yati": a.yati_matched,
            "valid": a.matched,
            "yati_seats": _yati_seats(a),
        }
    return verdict


def _fingerprint(poem) -> str:
    return hashlib.sha1(json.dumps([lines_for_scansion(poem), poem.metre], ensure_ascii=False).encode()).hexdigest()[:12]


def _scan_one(item):
    key, lines, label = item
    try:
        return key, scan(lines, label)
    except Exception as e:                            # one bad poem must not stop the run
        return key, {"error": f"{type(e).__name__}: {e}", "identified": False, "scans_as_label": False,
                     **{p: {"prasa": None, "yati": None, "valid": False} for p in config.SCAN_PROFILES}}


def scan_poems(poems, workers: int = 12) -> dict:
    """{poem key: verdict} for every poem, from the cache where the poem is unchanged."""
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    todo = [(p.key, lines_for_scansion(p), p.metre) for p in poems
            if cache.get(p.key, {}).get("fingerprint") != _fingerprint(p)]
    if todo:
        print(f"scanning {len(todo):,} poems with meter_engine ({workers} workers)...", flush=True)
        fingerprints = {p.key: _fingerprint(p) for p in poems}
        with Pool(workers) as pool:
            for k, (key, verdict) in enumerate(pool.imap_unordered(_scan_one, todo, chunksize=16), 1):
                cache[key] = {"fingerprint": fingerprints[key], "verdict": verdict}
                if k % 1000 == 0 or k == len(todo):
                    print(f"  {k:,}/{len(todo):,}", flush=True)
        config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    return {p.key: cache[p.key]["verdict"] for p in poems}
