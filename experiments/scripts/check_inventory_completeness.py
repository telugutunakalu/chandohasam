#!/usr/bin/env python3
"""
Completeness of the enforcer with an akshara inventory: real poems must still get through.

Corpus poems (``dataset/*.json``) whose canonical scansion our engine accepts in the meter it
identifies are cleaned to what a model can write (Telugu words, one space between words, a line
break between lines), skipped if the orthography filter rejects them, and fed through the enforcer
(gaṇa + prāsa + yati, strict) in random token chunkings — with no inventory, the verse inventory and
the tokenizer inventory. Every poem that gets through without an inventory must get through with
the verse inventory (it holds every syllable of that verse); a loss would be a flaw in the
inventory's liveness test. The tokenizer inventory lacks 12 verse syllables, so a few losses there
are expected and are listed.

usage: check_inventory_completeness.py OUT_JSON [--per-meter 40] [--workers 16]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import unicodedata
from collections import Counter, defaultdict
from multiprocessing import get_context
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))

INVENTORIES = (None, "verse", "tokenizer")


def candidates(per_meter: int, seed: int = 0) -> list[tuple[str, str, str]]:
    from indic_meter_dawg import identify, patterns
    from indic_meter_dawg.prosody import accepts_poem
    from metrical_decoder.analysis import _telugu_words
    from metrical_decoder.orthography import is_well_formed
    poems = []
    for path in sorted((ROOT / "dataset").glob("*.json")):
        for rec in json.loads(path.read_text(encoding="utf-8")):
            verse = rec.get("verse") or []
            lines = [" ".join(_telugu_words(unicodedata.normalize("NFC", ln))) for ln in verse]
            lines = [ln for ln in lines if ln]
            if len(lines) >= 2:
                poems.append((f"{path.stem}:{rec.get('id')}", "\n".join(lines)))
    random.Random(seed).shuffle(poems)
    by_meter: dict[str, list] = defaultdict(list)
    for pid, text in poems:
        if not is_well_formed(text):
            continue
        pats = list(patterns(text.split("\n")))
        try:
            meter = identify(pats).best.meter
        except Exception:
            continue
        if meter and len(by_meter[meter]) < per_meter and accepts_poem(meter, pats):
            by_meter[meter].append((pid, meter, text))
    return [x for v in by_meter.values() for x in v]


def chunks(text: str, rng: random.Random) -> list[str]:
    out, i = [], 0
    while i < len(text):
        k = rng.randint(1, 4)
        out.append(text[i:i + k])
        i += k
    return out


def check(task: tuple) -> tuple[str, str, dict]:
    from metrical_decoder import Enforcer
    pid, meter, text = task
    verdict = {}
    for inv in INVENTORIES:
        enf = Enforcer(meter, prasa=True, yati=True, profile="strict", inventory=inv)
        ok = True
        for trial in range(2):
            rng = random.Random(hash((pid, trial)) & 0xFFFF)
            s = enf.initial()
            for piece in chunks(text, rng):
                s = enf.step(s, piece)
                if s is None:
                    break
            if s is None or not enf.poem_complete(s):
                ok = False
                break
        verdict[str(inv)] = ok
    return pid, meter, verdict


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--per-meter", type=int, default=40)
    ap.add_argument("--workers", type=int, default=16)
    ns = ap.parse_args()
    tasks = candidates(ns.per_meter)
    print(f"{len(tasks)} poems over {len({m for _, m, _ in tasks})} meters", flush=True)
    results = []
    with get_context("spawn").Pool(ns.workers) as pool:
        for i, r in enumerate(pool.imap_unordered(check, tasks), 1):
            results.append(r)
            if i % 100 == 0:
                print(f"[{i}/{len(tasks)}]", flush=True)
    passed = Counter()
    losses = defaultdict(list)
    for pid, meter, v in results:
        for k, ok in v.items():
            passed[k] += ok
        for k in ("verse", "tokenizer"):
            if v["None"] and not v[k]:
                losses[k].append((pid, meter))
    summary = {"poems": len(results), "passed": dict(passed),
               "lost_with_verse": losses["verse"], "lost_with_tokenizer": losses["tokenizer"],
               "results": [{"id": p, "meter": m, **v} for p, m, v in sorted(results)]}
    Path(ns.out).write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"passed without inventory {passed['None']}, with verse {passed['verse']}, with tokenizer "
          f"{passed['tokenizer']} (of {len(results)})")
    print("lost with the verse inventory:", losses["verse"][:20])
    print("lost with the tokenizer inventory:", losses["tokenizer"][:20])


if __name__ == "__main__":
    main()
