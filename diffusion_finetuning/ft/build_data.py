"""Stage 0 (PLAN §3): labels, splits, near-duplicate removal, round-trip check, and the
Stage 1 / Stage 2 data.

    uv run --project ../diffusion_pretraining python -m ft.build_data                 # full build
    uv run --project ../diffusion_pretraining python -m ft.build_data --limit 3000 --out data_smoke

Writes <out>/:
  records/{train,val,test,test_seen}.jsonl   one poem per line (the Stage 2 source of truth)
  records/dropped.jsonl                      training poems removed as near-duplicates of eval poems
  stage1/{train,val}.bin + {train,val}.mask.bin + meta.json
                                             packed poem + meaning documents (uint16 tokens) and
                                             per-token trainable flags (uint8; 0 = a fixed samasya line)
  report.json, DATA_CARD.md

Splits: Pothana's Bhagavatam (dataset/bhagavatam.json) is held out whole: skandhas 1, 2, 7
are val, the rest test; its Padyarchana copy is excluded. Two Mahābhārata parvams are
Test-seen. Every other Padyarchana poem is train unless it is a near-duplicate of an
eval poem.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np

from . import DATA_DIR, PROJECT_ROOT
from .dedup import GramIndex
from .metres import canonicalise
from .text import (CLASSICAL, MAKUTAM_KEY, MEANING_KEY, METRE_KEY, MODERN, POEM_KEY, SAMASYA_KEY, SRC_EDITION,
                   SRC_MACHINE, STYLE_KEY, clean_meaning, clean_poem_line, content_key, raw_lines, register_of)

PADYARCHANA = PROJECT_ROOT / "padyarchana_exports" / "padyarchana_poems_v2.jsonl"
BHAGAVATAM = PROJECT_ROOT / "dataset" / "bhagavatam.json"
BHAGAVATAM_SOURCE = "శ్రీమదాంధ్ర మహాభాగవతం"
VAL_SKANDHAS = {"1", "2", "7"}
TEST_SEEN = {("శ్రీమదాంధ్ర మహాభారతము", "సభాపర్వము"), ("శ్రీమదాంధ్ర మహాభారతము", "విరాటపర్వము")}
DUP_THRESHOLD = 0.5
METRE_OK = ("agree", "engine-only")
SHARED_MIN_LETTERS = 12        # a shared last line shorter than this is a formula ("అనిన"), not a refrain
SHARED_MIN_POEMS = {MODERN: 2, CLASSICAL: 5}   # a samasya is shared by 2+ poets; a makuṭam repeats through a śataka


# -----------------------------------------------------------------------------
# loading
# -----------------------------------------------------------------------------
def _glosses(rows) -> list[list[str]]:
    out = []
    for g in rows or []:
        w, m = clean_poem_line(g.get("word") or ""), clean_meaning(g.get("meaning"))
        if w and m:
            out.append([w, m, clean_meaning(g.get("split")) or ""])
    return out


def load_padyarchana(path: Path, limit: int = 0):
    with path.open(encoding="utf-8") as fh:
        for n, line in enumerate(fh):
            if limit and n >= limit:
                break
            r = json.loads(line)
            ed, gen = r.get("editorial") or {}, r.get("generated") or {}
            if ed.get("bhavam"):
                meaning, src = ed["bhavam"], SRC_EDITION
            else:
                meaning, src = gen.get("bhavam"), SRC_MACHINE
            glosses = _glosses(ed.get("prathipadartham")) or _glosses(gen.get("prathipadartham"))
            yield {"id": f"p{r['id']}", "source": r.get("source") or "", "kanda": r.get("kanda") or "",
                   "label": (r.get("meter") or {}).get("name"), "printed": raw_lines(r.get("lines") or r.get("text")),
                   "meaning": clean_meaning(meaning), "meaning_src": src if meaning else None,
                   "meaning_en": None, "glosses": glosses, "skandha": None}


def load_bhagavatam(path: Path, limit: int = 0) -> list[dict]:
    """Verse records; a sīsa and its ettugīti (stored as parent + child) become one poem."""
    data = json.loads(path.read_text(encoding="utf-8"))
    by_id = {r["id"]: r for r in data}
    out = []
    for r in data:
        if r.get("form") != "verse" or r.get("metre_roman") in ("vachanamu", "gadya"):
            continue
        parent = by_id.get(r.get("parent_id")) if r.get("parent_id") else None
        if parent is not None and parent.get("metre_roman") == "seesamu":
            continue                                       # absorbed by its sīsa below
        verse, label, carrier = list(r.get("verse") or []), r.get("metre"), r
        child = by_id.get(r.get("child_id")) if r.get("child_id") else None
        if r.get("metre_roman") == "seesamu" and child is not None:
            verse += list(child.get("verse") or [])
            label = f"{r.get('metre')} + {child.get('metre')}"
            carrier = child if child.get("bhavam") else r      # the edition explains the whole poem once
        meaning = carrier.get("bhavam") or r.get("bhavam")
        glosses = _glosses(r.get("teeka_pairs")) + (_glosses(child.get("teeka_pairs")) if child is not None and child is not r else [])
        out.append({"id": f"b{r['id']}", "source": BHAGAVATAM_SOURCE, "kanda": str(r.get("skandha") or ""),
                    "label": label, "printed": raw_lines(verse), "meaning": clean_meaning(meaning),
                    "meaning_src": SRC_EDITION if meaning else None,
                    "meaning_en": clean_meaning(carrier.get("bhavam_en") or r.get("bhavam_en")) or None,
                    "glosses": glosses, "skandha": str(r.get("skandha") or "")})
        if limit and len(out) >= limit:
            break
    return out


# -----------------------------------------------------------------------------
# per-poem work (run in a process pool)
# -----------------------------------------------------------------------------
def _canon_job(job: tuple) -> dict:
    c = canonicalise(*job)
    return {"lines": c.lines, "status": c.status, "meter": c.meter, "meter_label": c.label, "meter_te": c.name_te,
            "layout": c.layout, "roundtrip": c.roundtrip}


def _prosody_job(job: tuple) -> dict:
    """prāsa / yati verdicts on the cleaned target lines (eval poems only: ~0.5 s per poem)."""
    from chandohasam.analysis import analyze
    from indic_meter_dawg import identify_text
    from .metres import dawg
    lines, meter = job
    out = {}
    ident = identify_text(lines, dawg())
    for profile in ("relaxed", "strict"):
        a = analyze(lines, profile=profile, meter=meter, identification=ident)
        out[f"prasa_{profile}"], out[f"yati_{profile}"] = bool(a.prasa_matched), bool(a.yati_matched)
    return out


def _dup_job(args) -> tuple[str, list]:
    key, text = args
    return key, _INDEX.matches(text, DUP_THRESHOLD)[:3]


_INDEX: GramIndex | None = None


def _init_dup(index: GramIndex) -> None:
    global _INDEX
    _INDEX = index


def _pool_map(fn, items, workers: int, chunksize: int = 64, initializer=None, initargs=()):
    if workers <= 1:
        if initializer:
            initializer(*initargs)
        return [fn(x) for x in items]
    ctx = mp.get_context("fork")
    with ctx.Pool(workers, initializer=initializer, initargs=initargs) as pool:
        return pool.map(fn, items, chunksize=chunksize)


# -----------------------------------------------------------------------------
# Stage 1 documents
# -----------------------------------------------------------------------------
def _flip(rec_id: str, seed: int) -> bool:
    return hashlib.blake2b(f"{seed}:{rec_id}".encode(), digest_size=2).digest()[0] & 1 == 1


def stage1_pieces(rec: dict, seed: int) -> list[tuple[str, bool]]:
    """(text, trainable) pieces of one document; the samasya line (header and poem) is fixed."""
    pieces: list[tuple[str, bool]] = []
    if rec["status"] in METRE_OK and rec["meter_te"]:
        pieces.append((f"{METRE_KEY}: {rec['meter_te']}\n", True))
    pieces.append((f"{STYLE_KEY}: {rec['register']}\n", True))
    sam = rec.get("samasya")
    if sam:
        pieces += [(f"{sam['kind']}: ", True), (sam["line"], False), ("\n", True)]
    poem = [(f"{POEM_KEY}:\n", True)]
    for i, ln in enumerate(rec["lines"]):
        fixed = bool(sam) and i == len(rec["lines"]) - 1
        poem += [(ln, not fixed), ("\n", True)]
    meaning = [(f"{MEANING_KEY} ({rec['meaning_src']}): {rec['meaning']}\n", True)] if rec.get("meaning") else []
    return pieces + (meaning + poem if _flip(rec["id"], seed) else poem + meaning)


def encode_pieces(tok, pieces: list[tuple[str, bool]]) -> tuple[list[int], list[int]]:
    """Token ids with <bos>/<eos> and a trainable flag per token. Pieces are encoded one by one:
    every piece boundary is at a space or newline, where the tokenizer never merges."""
    ids, flags = [tok.bos_id], [1]
    for text, trainable in pieces:
        t = tok.encode(text)
        ids += t
        flags += [int(trainable)] * len(t)
    ids.append(tok.eos_id)
    flags.append(1)
    return ids, flags


def write_stage1(tok, recs: list[dict], out: Path, name: str, seed: int) -> dict:
    ids, flags, n = [], [], 0
    for rec in recs:
        if not rec["lines"]:
            continue
        i, f = encode_pieces(tok, stage1_pieces(rec, seed))
        ids += i
        flags += f
        n += 1
    out.mkdir(parents=True, exist_ok=True)
    np.asarray(ids, dtype=np.uint16).tofile(out / f"{name}.bin")
    np.asarray(flags, dtype=np.uint8).tofile(out / f"{name}.mask.bin")
    return {"documents": n, "tokens": len(ids), "fixed_tokens": int(len(flags) - sum(flags))}


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=DATA_DIR)
    ap.add_argument("--padyarchana", type=Path, default=PADYARCHANA)
    ap.add_argument("--bhagavatam", type=Path, default=BHAGAVATAM)
    ap.add_argument("--limit", type=int, default=0, help="first N Padyarchana rows and N Bhagavatam poems (smoke runs)")
    ap.add_argument("--workers", type=int, default=max(1, (mp.cpu_count() or 2) - 2))
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--prosody-train", action="store_true", help="also compute prāsa/yati for training poems (hours)")
    ap.add_argument("--skip-prosody", action="store_true", help="no prāsa/yati verdicts at all (smoke runs)")
    args = ap.parse_args(argv)
    out = args.out if args.out.is_absolute() else (Path.cwd() / args.out)
    t0 = time.time()

    def say(msg: str) -> None:
        print(f"[{time.time() - t0:6.0f}s] {msg}", flush=True)

    recs = list(load_padyarchana(args.padyarchana, args.limit)) + load_bhagavatam(args.bhagavatam, args.limit)
    say(f"loaded {len(recs):,} poems")
    for r in recs:
        r["register"] = register_of(r["source"])
        if r["source"] == BHAGAVATAM_SOURCE:
            r["split"] = ("val" if r["skandha"] in VAL_SKANDHAS else "test") if r["id"].startswith("b") else "excluded"
        elif (r["source"], r["kanda"]) in TEST_SEEN:
            r["split"] = "test_seen"
        else:
            r["split"] = "train"
    recs = [r for r in recs if r["split"] != "excluded"]

    for r, c in zip(recs, _pool_map(_canon_job, [(r["printed"], r["label"]) for r in recs], args.workers, chunksize=256)):
        r.update(c)
    say("metres identified and layouts canonicalised")

    # ---- near-duplicates of eval poems (only metrical eval poems are ever scored) -------------
    evals = {r["id"]: "\n".join(r["printed"]) for r in recs if r["split"] != "train" and r["status"] in METRE_OK}
    index = GramIndex(evals)
    train = [r for r in recs if r["split"] == "train"]
    hits = dict(_pool_map(_dup_job, [(r["id"], "\n".join(r["printed"])) for r in train], args.workers,
                          chunksize=256, initializer=_init_dup, initargs=(index,)))
    dropped = []
    for r in train:
        if hits.get(r["id"]):
            r["split"] = "dropped"
            r["dup_of"] = [[k, round(a, 3), round(b, 3)] for k, a, b in hits[r["id"]]]
            dropped.append(r)
    say(f"near-duplicates of eval poems dropped from train: {len(dropped):,}")

    # ---- shared last lines (samasya / makuṭam) among metrical training poems -----------------
    train = [r for r in recs if r["split"] == "train" and r["status"] in METRE_OK and r["lines"]]
    last = collections.Counter(content_key(r["lines"][-1]) for r in train)
    for r in recs:
        r["samasya"] = None
    for r in train:
        key = content_key(r["lines"][-1])
        if len(key) >= SHARED_MIN_LETTERS and last[key] >= SHARED_MIN_POEMS[r["register"]]:
            r["samasya"] = {"kind": SAMASYA_KEY if r["register"] == MODERN else MAKUTAM_KEY,
                            "line": r["lines"][-1], "group": last[key]}
    say(f"poems with a shared last line: {sum(r['samasya'] is not None for r in recs):,}")

    # ---- prāsa / yati ceilings -------------------------------------------------------------
    want = [] if args.skip_prosody else [
        r for r in recs if r["status"] in METRE_OK and (args.prosody_train or r["split"] in ("val", "test", "test_seen"))]
    cache_path = out / "prosody_cache.json"                  # keyed by the target text: rebuilds reuse it
    cache = json.loads(cache_path.read_text(encoding="utf-8")) if cache_path.exists() else {}
    pkey = lambda r: hashlib.blake2b(("\n".join(r["lines"]) + "|" + str(r["meter_label"])).encode(), digest_size=12).hexdigest()
    todo = [r for r in want if pkey(r) not in cache]
    for r, p in zip(todo, _pool_map(_prosody_job, [(r["lines"], r["meter_label"] or r["meter"]) for r in todo],
                                    args.workers, chunksize=8)):
        cache[pkey(r)] = p
    for r in want:
        r.update(cache[pkey(r)])
    if todo:
        out.mkdir(parents=True, exist_ok=True)
        cache_path.write_text(json.dumps(cache), encoding="utf-8")
    say(f"prāsa/yati verdicts for {len(want):,} poems ({len(todo):,} computed)")

    # ---- write records --------------------------------------------------------------------
    rec_dir = out / "records"
    rec_dir.mkdir(parents=True, exist_ok=True)
    keep = ("id", "split", "source", "kanda", "skandha", "register", "label", "status", "meter", "meter_label", "meter_te",
            "layout", "roundtrip", "lines", "meaning", "meaning_src", "meaning_en", "glosses", "samasya",
            "prasa_relaxed", "yati_relaxed", "prasa_strict", "yati_strict", "dup_of")
    by_split = collections.defaultdict(list)
    for r in recs:
        by_split[r["split"]].append(r)
    for split, rows in by_split.items():
        with (rec_dir / f"{split}.jsonl").open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps({k: r.get(k) for k in keep if k in r or k in ("samasya",)}, ensure_ascii=False) + "\n")
    say("records written")

    # ---- Stage 1 documents -----------------------------------------------------------------
    from tokenizer import load_default
    tok = load_default()
    s1 = {"train": write_stage1(tok, by_split["train"], out / "stage1", "train", args.seed),
          "val": write_stage1(tok, by_split["val"], out / "stage1", "val", args.seed)}
    (out / "stage1" / "meta.json").write_text(json.dumps(s1, indent=2), encoding="utf-8")
    say(f"stage 1 documents: {s1}")

    report = build_report(recs, s1, dropped)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "DATA_CARD.md").write_text(data_card(report, args), encoding="utf-8")
    say(f"done -> {out}")
    return 0


# -----------------------------------------------------------------------------
# report
# -----------------------------------------------------------------------------
def build_report(recs: list[dict], s1: dict, dropped: list[dict]) -> dict:
    C = collections.Counter
    rep: dict = {"splits": dict(C(r["split"] for r in recs))}
    for split in ("train", "val", "test", "test_seen"):
        rows = [r for r in recs if r["split"] == split]
        ok = [r for r in rows if r["status"] in METRE_OK]
        rep[split] = {
            "poems": len(rows),
            "status": dict(C(r["status"] for r in rows)),
            "layout": dict(C(r["layout"] for r in rows)),
            "register": dict(C(r["register"] for r in rows)),
            "with_meaning": sum(bool(r["meaning"]) for r in rows),
            "meaning_src": dict(C(r["meaning_src"] for r in rows if r["meaning"])),
            "with_glosses": sum(bool(r["glosses"]) for r in rows),
            "gloss_rows": sum(len(r["glosses"]) for r in rows),
            "metres": dict(C(r["meter_label"] for r in ok).most_common(30)),
            "roundtrip_ok": sum(r["roundtrip"] is True for r in ok),
            "roundtrip_checked": sum(r["roundtrip"] is not None for r in ok),
            "samasya": dict(C(r["samasya"]["kind"] for r in rows if r.get("samasya"))),
        }
        if split != "train":
            for k in ("prasa_relaxed", "yati_relaxed", "prasa_strict", "yati_strict"):
                vals = [r[k] for r in ok if k in r]
                rep[split][f"{k}_rate"] = round(sum(vals) / len(vals), 4) if vals else None
    rep["dropped_near_duplicates"] = {"poems": len(dropped), "by_source": dict(C(r["source"] for r in dropped).most_common(10))}
    rep["stage1"] = s1
    return rep


def data_card(rep: dict, args) -> str:
    lines = ["# Fine-tuning data card", "",
             f"Built by `ft.build_data` on {time.strftime('%Y-%m-%d %H:%M')} (limit={args.limit or 'none'}, seed={args.seed}).",
             "", "## Splits", "", "| split | poems |", "|---|---|"]
    lines += [f"| {k} | {v:,} |" for k, v in sorted(rep["splits"].items())]
    for split in ("train", "val", "test", "test_seen"):
        s = rep[split]
        rt = f"{s['roundtrip_ok']:,} / {s['roundtrip_checked']:,}"
        lines += ["", f"## {split}", "",
                  f"- poems: {s['poems']:,}; with a meaning: {s['with_meaning']:,} ({s['meaning_src']}); "
                  f"with glosses: {s['with_glosses']:,} ({s['gloss_rows']:,} rows)",
                  f"- metre status: {s['status']}",
                  f"- layout used: {s['layout']}",
                  f"- register: {s['register']}",
                  f"- round trip (cleaned target identifies as the same metre): {rt}",
                  f"- shared last lines: {s['samasya']}",
                  f"- metres (agree + engine-only): {s['metres']}"]
        if split != "train":
            lines.append("- prāsa / yati pass on real poems (ceilings): " + ", ".join(
                f"{k.replace('_rate', '')} {s[k]}" for k in s if k.endswith("_rate")))
    d = rep["dropped_near_duplicates"]
    lines += ["", "## Near-duplicates", "", f"{d['poems']:,} training poems dropped (≥ {DUP_THRESHOLD:.0%} 8-gram containment "
              f"either way with an eval poem): {d['by_source']}", "", "## Stage 1", "", f"{rep['stage1']}", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
