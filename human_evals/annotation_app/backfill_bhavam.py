#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill the bhavams the corpora lack from the Padyarchana export.

``build_data.py`` finds no bhavam for about a hundred poems of each pool: the textbook
reference examples, which come with none, and the Bhāgavatam సీసము heads, whose bhavam
``dataset/bhagavatam.json`` keeps on the గీతి trailer record and so covers lines the pool
poem does not print. This script looks each of them up in
``padyarchana_exports/padyarchana_poems_v2.jsonl`` and writes the bhavams it finds to
``data/bhavam_padyarchana.json``, keyed by the poem's Telugu letters, so it serves all
three pools. ``build_data.py`` reads that file as a fallback after the corpora.

Matching and choice
-------------------
* A record matches when the two texts share at least 95% of their Telugu letters
  (ardhabindu ignored) both ways. Lines that are only a parenthesised attribution, such
  as "(భీమన ఛందము)", are left out of the record side.
* The edition's own bhavam (``editorial``) is preferred to the model gloss
  (``generated``). It is skipped when a neighbouring record carries the same text, since
  the edition then wrote one bhavam for a సీసము and its trailer together.
* A bhavam that contains letters of a script other than Telugu or Latin is skipped;
  some model glosses carry stray Japanese, for example.
* A bhavam that names the record's poet, when the poem itself does not, is skipped:
  rating is blind, and one Bhāgavatam bhavam tells a story about Pothana.
* REJECTED lists the glosses read and found wrong. A leading "[భావము]" label is dropped.

Run from anywhere (the export is about 2 GB and is read once, in parallel):

    python3 backfill_bhavam.py
    python3 build_data.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

import build_data

ROOT = build_data.ROOT
EXPORT = ROOT / "padyarchana_exports" / "padyarchana_poems_v2.jsonl"
OUT = build_data.DATA_OUT / "bhavam_padyarchana.json"
POOLS = ("strict", "relaxed", "historical")

MIN_COVER = 0.95      # share of Telugu letters matched, each way
ANCHOR = 18           # letters per anchor; a record must contain two anchors of a target
NON_TE = re.compile(r"[^ఀ-౿]")
ATTRIBUTION = re.compile(r"^\s*\(.*\)\s*$")
LABEL = re.compile(r"^\s*(\[\s*భావ(ము|ం)\s*\]|భావ(ము|ం)\s*:)\s*")

# glosses read and found wrong: (Padyarchana record id, kind) → why
REJECTED = {
    (374518, "generated"): "glosses the ఆటవెలది lakṣaṇa verse as the lakṣaṇa of చంపకమాల",
    (374642, "generated"): "reads the gaṇa names as words and lists the gaṇas of లలిత wrongly",
}


def match_key(text: str) -> str:
    """Telugu letters only, without ardhabindu: editions differ on it."""
    return NON_TE.sub("", text).replace(build_data.ARDHABINDU, "")


def names_poet(text: str, poet: str | None, poem: str) -> bool:
    """The bhavam names the poet (any word of the name, three letters or more) and the poem does not."""
    return any(len(w) >= 3 and w in text and w not in poem for w in (poet or "").split())


def clean_script(text: str) -> bool:
    for ch in text:
        if unicodedata.category(ch)[0] in "LM" and not unicodedata.name(ch, "").startswith(("TELUGU", "LATIN")):
            return False
    return True


# -----------------------------------------------------------------------------
# 1. the poems that need a bhavam
# -----------------------------------------------------------------------------
def targets() -> dict[str, dict]:
    """Text key → the pool poem, for every poem of any pool that build_data gives no bhavam."""
    sources = build_data.load_bhavam_sources(backfill=False)
    out = {}
    for pool in POOLS:
        for poem in json.loads((build_data.HUMAN_EVALS / f"human_eval_poems_{pool}.json").read_text("utf-8"))["poems"]:
            if build_data.find_bhavam(poem, sources, {}) is None:
                entry = out.setdefault(build_data._text_key(poem["lines"]), {"poem": poem, "eval_ids": {}})
                entry["eval_ids"][pool] = poem["eval_id"]
    return out


# -----------------------------------------------------------------------------
# 2. one pass over the export
# -----------------------------------------------------------------------------
_KEYS: dict[str, str] = {}
_ANCHORS: dict[str, list[str]] = {}


def _init(keys: dict[str, str]) -> None:
    _KEYS.update(keys)
    for tkey, k in keys.items():
        n = len(k)
        starts = {0, n // 4, max(0, n // 2 - ANCHOR // 2), max(0, 3 * n // 4 - ANCHOR), max(0, n - ANCHOR)}
        _ANCHORS[tkey] = [k[s:s + ANCHOR] for s in sorted(starts)]


def _cover(a: str, b: str) -> int:
    return sum(block.size for block in SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks())


def _digest(text: str | None) -> str | None:
    return hashlib.md5(text.encode("utf-8")).hexdigest() if text else None


def _scan(line: str) -> tuple[int, str | None, list[tuple[str, float, float]], dict | None]:
    """(record id, digest of its editorial bhavam, matched targets, the record when it matched)."""
    rec = json.loads(line)
    lines = rec.get("lines") or (rec.get("text") or "").splitlines()
    rk = match_key("".join(ln for ln in lines if not ATTRIBUTION.match(ln)))
    editorial = (rec.get("editorial") or {}).get("bhavam")
    found = []
    if rk:
        for tkey, anchors in _ANCHORS.items():
            if sum(a in rk for a in anchors) >= 2 or _KEYS[tkey] == rk:
                shared = _cover(_KEYS[tkey], rk)
                found.append((tkey, shared / len(_KEYS[tkey]), shared / len(rk)))
    if not found:
        return rec["id"], _digest(editorial), found, None
    gen = rec.get("generated") or {}
    slim = {"id": rec["id"], "title": rec.get("title"), "meter": (rec.get("meter") or {}).get("name"),
            "poet": (rec.get("poet") or {}).get("name"),
            "lines": lines, "editorial": editorial, "generated": gen.get("bhavam"),
            "model": gen.get("model"), "run": gen.get("run")}
    return rec["id"], _digest(editorial), found, slim


def scan_export(path: Path, keys: dict[str, str], workers: int) -> tuple[dict, dict, dict]:
    """Matches (text key → [(record id, cover of target, cover of record)]), the matched
    records by id, and the editorial digests of those records and their neighbours."""
    matches: dict[str, list] = {k: [] for k in keys}
    records: dict[int, dict] = {}
    digests: dict[int, str | None] = {}
    prev: tuple[int, str | None] = (-1, None)
    need_next: set[int] = set()
    with path.open(encoding="utf-8") as fh, multiprocessing.Pool(workers, _init, (keys,)) as pool:
        for rid, digest, found, slim in pool.imap(_scan, fh, chunksize=256):
            if rid in need_next:
                digests[rid] = digest
            if found:
                records[rid] = slim
                digests[rid] = digest
                if prev[0] == rid - 1:
                    digests[rid - 1] = prev[1]
                need_next.add(rid + 1)
                for tkey, ct, cr in found:
                    matches[tkey].append((rid, ct, cr))
            prev = (rid, digest)
    return matches, records, digests


# -----------------------------------------------------------------------------
# 3. choose one bhavam per poem
# -----------------------------------------------------------------------------
def choose(poem_text: str, matches: list, records: dict, digests: dict) -> tuple[dict | None, str]:
    good = sorted(((min(ct, cr), ct == cr == 1.0, rid) for rid, ct, cr in matches
                   if ct >= MIN_COVER and cr >= MIN_COVER), key=lambda t: (-t[0], not t[1], t[2]))
    if not good:
        return None, "no record matches the text" if not matches else "only partial matches (a longer or shorter text)"
    skipped = []
    for kind in ("editorial", "generated"):
        for cover, _, rid in good:
            rec = records[rid]
            text = rec[kind]
            if not text:
                continue
            if (rid, kind) in REJECTED:
                skipped.append(f"{rid} {kind} rejected: {REJECTED[rid, kind]}")
                continue
            if kind == "editorial" and _digest(text) in (digests.get(rid - 1), digests.get(rid + 1)):
                skipped.append(f"{rid} editorial spans a neighbouring record")
                continue
            if not clean_script(text):
                skipped.append(f"{rid} {kind} has letters of another script")
                continue
            if names_poet(text, rec["poet"], poem_text):
                skipped.append(f"{rid} {kind} names the poet")
                continue
            source = ("padyarchana_editorial" if kind == "editorial"
                      else f"padyarchana_llm_gloss:{rec['run'] or '?'}:{rec['model'] or '?'}")
            return {"te": LABEL.sub("", text).strip(), "en": None, "source": source,
                    "padyarchana_id": rid, "padyarchana_title": rec["title"], "padyarchana_meter": rec["meter"],
                    "match": round(cover, 4), "skipped": skipped}, "ok"
    return None, "matching records carry no usable bhavam: " + "; ".join(skipped)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--export", type=Path, default=EXPORT)
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--workers", type=int, default=max(1, multiprocessing.cpu_count() - 2))
    args = ap.parse_args(argv)
    if not args.export.is_file():
        print(f"no Padyarchana export at {args.export}", file=sys.stderr)
        return 1

    want = targets()
    keys = {tkey: match_key("".join(t["poem"]["lines"])) for tkey, t in want.items()}
    matches, records, digests = scan_export(args.export, keys, args.workers)

    entries, missing = {}, {}
    for tkey, t in want.items():
        poem = t["poem"]
        chosen, why = choose("\n".join(poem["lines"]), matches[tkey], records, digests)
        about = {"eval_ids": t["eval_ids"], "source_dataset": poem["source_dataset"],
                 "source_id": poem["source_id"], "meter_id": poem["meter_id"]}
        if chosen:
            entries[tkey] = {**chosen, **about}
        else:
            missing[tkey] = {**about, "reason": why, "lines": poem["lines"]}

    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = {"export": args.export.name, "min_cover": MIN_COVER, "n_filled": len(entries),
               "n_missing": len(missing), "bhavams": entries, "missing": missing}
    with args.out.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)

    kinds = Counter((e["source_dataset"], e["source"].split(":")[0]) for e in entries.values())
    print(f"{len(want)} poems without a bhavam across the pools; filled {len(entries)}, still missing {len(missing)}")
    for (src, kind), n in sorted(kinds.items()):
        print(f"  {src:<11} {kind:<22} {n}")
    for m in missing.values():
        print(f"  missing {m['eval_ids']} {m['source_id']}: {m['reason']}")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
