"""Build the stage-1 pretraining corpus: raw sources -> clean, deduplicated, poem-free token files.

    uv run python -m data_prep.build_corpus --workers 12            # everything
    uv run python -m data_prep.build_corpus --limit 2000 --out-dir /tmp/trial   # quick trial

Pass A  normalise every document; find exact-duplicate documents and boilerplate
        lines (a line found in >= 10 distinct documents) across all sources.
Pass B  clean and filter each document, tokenize it, and fingerprint it: MinHash
        over 8-token shingles (near-duplicates) and 20-token windows (poem overlap).
Pass C  cluster near-duplicates (Wikipedia + Sangraha; IndicCorp paragraphs are
        exact-deduplicated only), drop documents that overlap a poem, split
        val/test by document hash, and write <source>/{train,val,test}.bin
        (uint16; every document as <bos> ... <eos>), meta.json and report.md.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import multiprocessing as mp
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

import numpy as np

from tokenizer import VOCAB_PATH, load_default

from .cleaning import Thresholds, clean_doc, normalize, stable_hash
from .fingerprints import NUM_PERM, content_mask, minhash, near_duplicate_clusters, window_hashes
from .poems import POEM_WINDOW, build_poem_windows
from .sources import PROJECT_ROOT, SOURCE_ORDER, Shard, iter_docs, list_shards

SHINGLE = 8
MAX_RARE_SHARE = 0.02          # Telugu pieces with no atomic token (garbled or non-standard text)
MIN_CONTENT_SHARE = 0.5        # content tokens among all tokens (tables, number lists)
VAL_PER_MILLE, TEST_PER_MILLE = 5, 5
KINDS = ["wiki", "web", "pdf", "speech", "paragraph"]
TH = Thresholds()

_W: dict = {}                  # per-worker state


def _in_sorted(sorted_arr: np.ndarray, values: np.ndarray) -> np.ndarray:
    if sorted_arr.size == 0 or values.size == 0:
        return np.zeros(values.size, dtype=bool)
    pos = np.minimum(np.searchsorted(sorted_arr, values), sorted_arr.size - 1)
    return sorted_arr[pos] == values


# ------------------------------------------------------------------ pass A
def pass_a(shard: Shard, work: Path, limit: int) -> dict:
    doc_h, line_h, line_doc, chars = [], [], [], 0
    for i, doc in enumerate(itertools.islice(iter_docs(shard), limit or None)):
        text = normalize(doc.text)
        chars += len(text)
        doc_h.append(stable_hash(text))
        for line in set(text.split("\n")) if text else ():
            line_h.append(stable_hash(line))
            line_doc.append(i)
    np.savez(work / "A" / f"{shard.name}.npz", doc_hash=np.array(doc_h, dtype=np.uint64),
             line_hash=np.array(line_h, dtype=np.uint64), line_doc=np.array(line_doc, dtype=np.int32))
    return {"shard": shard.name, "docs": len(doc_h), "chars": chars}


def after_pass_a(shards: list[Shard], work: Path) -> dict:
    """Exact-duplicate keep masks and the boilerplate line set."""
    data = {s.name: np.load(work / "A" / f"{s.name}.npz") for s in shards}
    doc_hash = [data[s.name]["doc_hash"] for s in shards]
    _, first = np.unique(np.concatenate(doc_hash), return_index=True)
    keep_all = np.zeros(sum(len(h) for h in doc_hash), dtype=bool)
    keep_all[first] = True
    keeps = np.split(keep_all, np.cumsum([len(h) for h in doc_hash])[:-1])

    lines = [data[s.name]["line_hash"][k[data[s.name]["line_doc"]]] for s, k in zip(shards, keeps)]
    uniq, counts = np.unique(np.concatenate(lines), return_counts=True)
    frequent = uniq[counts >= TH.frequent_line_docs]
    np.save(work / "frequent_lines.npy", frequent)

    # IndicCorp paragraphs that already occur as a line of a Wikipedia/Sangraha document
    exact = int((~keep_all).sum())
    other = np.unique(np.concatenate([ln for s, ln in zip(shards, lines) if s.source != "indiccorp"] or [np.empty(0, np.uint64)]))
    cross = 0
    for s, h, k in zip(shards, doc_hash, keeps):
        if s.source == "indiccorp":
            dup = k & _in_sorted(other, h)
            cross += int(dup.sum())
            k &= ~dup
        np.save(work / "A" / f"keep-{s.name}.npy", k)
    return {"frequent_lines": int(frequent.size), "exact_duplicates": exact,
            "indiccorp_in_other_sources": cross}


# ------------------------------------------------------------------ pass B
def _init_worker(work: str) -> None:
    tok = load_default()
    _W.update(tok=tok, content=content_mask(tok),
              poems=np.load(Path(work) / "poem_windows.npy", mmap_mode="r"),
              frequent=np.load(Path(work) / "frequent_lines.npy", mmap_mode="r"))


def pass_b(shard: Shard, work: Path, limit: int) -> dict:
    tok, content = _W["tok"], _W["content"]
    keep = np.load(work / "A" / f"keep-{shard.name}.npy")
    reasons = collections.Counter()
    offsets, lengths, hashes, kinds, poem_hits, poem_at, sigs = [], [], [], [], [], [], []
    pos = 0
    with open(work / "B" / f"{shard.name}.bin", "wb") as out:
        for i, doc in enumerate(itertools.islice(iter_docs(shard), limit or None)):
            if not keep[i]:
                reasons["exact_duplicate"] += 1
                continue
            text = normalize(doc.text)
            cleaned, why = clean_doc(text, _W["frequent"], TH)
            if why:
                reasons[why] += 1
                continue
            ids, n_telugu, n_rare = tok.encode_with_stats(cleaned)
            ids = np.asarray(ids, dtype=np.uint16)
            cmask = content[ids]
            n_content = int(cmask.sum())
            if n_content < MIN_CONTENT_SHARE * len(ids):
                reasons["low_content_share"] += 1
                continue
            if n_rare > MAX_RARE_SHARE * n_telugu:
                reasons["garbled_text"] += 1
                continue
            cpos = np.flatnonzero(cmask)
            hits = np.flatnonzero(_in_sorted(_W["poems"], window_hashes(ids[cpos], POEM_WINDOW)))
            poem_hits.append(len(hits))
            poem_at.append(int(cpos[hits[0]]) if len(hits) else -1)
            if shard.source != "indiccorp":
                sigs.append(minhash(window_hashes(ids[cpos], SHINGLE)))
            ids.tofile(out)
            offsets.append(pos)
            lengths.append(len(ids))
            pos += len(ids)
            hashes.append(stable_hash(text))
            kinds.append(KINDS.index(doc.kind) if doc.kind in KINDS else 1)
            reasons["kept"] += 1
    np.savez(work / "B" / f"{shard.name}.npz", offset=np.array(offsets, np.int64), length=np.array(lengths, np.int64),
             doc_hash=np.array(hashes, np.uint64), kind=np.array(kinds, np.uint8),
             poem_hits=np.array(poem_hits, np.int32), poem_at=np.array(poem_at, np.int64),
             sig=np.array(sigs, np.uint32).reshape(-1, NUM_PERM))
    return {"shard": shard.name, "reasons": dict(reasons), "tokens": pos}


# ------------------------------------------------------------------ pass C
def pass_c(shards: list[Shard], work: Path, out_dir: Path, keep_work: bool) -> dict:
    tok = load_default()
    meta = {s.name: dict(np.load(work / "B" / f"{s.name}.npz")) for s in shards}

    # near-duplicates among Wikipedia + Sangraha documents: keep the longest of each cluster
    dedup = [s for s in shards if s.source != "indiccorp"]
    sigs = np.concatenate([meta[s.name]["sig"] for s in dedup]) if dedup else np.empty((0, NUM_PERM), np.uint32)
    lens = np.concatenate([meta[s.name]["length"] for s in dedup]) if dedup else np.empty(0, np.int64)
    root = near_duplicate_clusters(sigs)
    best = {}
    for i, (r, n) in enumerate(zip(root.tolist(), lens.tolist())):
        if r not in best or n > lens[best[r]]:
            best[r] = i
    near_keep = np.zeros(len(root), dtype=bool)
    near_keep[list(best.values())] = True
    near_split = dict(zip([s.name for s in dedup], np.split(near_keep, np.cumsum([len(meta[s.name]["length"]) for s in dedup])[:-1])))

    out_dir.mkdir(parents=True, exist_ok=True)
    handles, counts = {}, collections.defaultdict(collections.Counter)
    poem_examples = []
    for s in shards:
        m = meta[s.name]
        n = len(m["length"])
        keep = near_split.get(s.name, np.ones(n, dtype=bool)).copy()
        counts[s.source]["near_duplicate"] += int((~keep).sum())
        poem = m["poem_hits"] > 0
        counts[s.source]["poem_overlap"] += int((poem & keep).sum())
        tokens = np.fromfile(work / "B" / f"{s.name}.bin", dtype=np.uint16)
        for j in np.flatnonzero(poem & keep)[:2]:
            if len(poem_examples) < 12:
                a = int(m["poem_at"][j]) + int(m["offset"][j])
                poem_examples.append((s.name, tok.decode(tokens[max(int(m["offset"][j]), a - 20):a + 40].tolist())))
        keep &= ~poem
        split = (m["doc_hash"] % np.uint64(1000)).astype(np.int64)
        bos, eos = np.array([tok.bos_id], np.uint16), np.array([tok.eos_id], np.uint16)
        for name, lo, hi in (("val", 0, VAL_PER_MILLE), ("test", VAL_PER_MILLE, VAL_PER_MILLE + TEST_PER_MILLE),
                             ("train", VAL_PER_MILLE + TEST_PER_MILLE, 1000)):
            idx = np.flatnonzero(keep & (split >= lo) & (split < hi))
            if not len(idx):
                continue
            pieces = []
            for j in idx:
                pieces += [bos, tokens[m["offset"][j]:m["offset"][j] + m["length"][j]], eos]
            arr = np.concatenate(pieces)
            key = (s.source, name)
            if key not in handles:
                (out_dir / s.source).mkdir(exist_ok=True)
                handles[key] = open(out_dir / s.source / f"{name}.bin", "wb")
            arr.tofile(handles[key])
            counts[s.source][f"{name}_docs"] += len(idx)
            counts[s.source][f"{name}_tokens"] += int(arr.size)
        del tokens
        if not keep_work:
            (work / "B" / f"{s.name}.bin").unlink()
    for h in handles.values():
        h.close()
    return {"counts": {k: dict(v) for k, v in counts.items()}, "poem_examples": poem_examples,
            "near_dup_clusters": int(len(best)), "near_dup_docs": int(len(root))}


# ------------------------------------------------------------------ report
def _samples(out_dir: Path, tok, n: int = 20, length: int = 512, seed: int = 0) -> list[tuple[str, str]]:
    files = sorted(out_dir.glob("*/train.bin"))
    sizes = np.array([f.stat().st_size // 2 for f in files], dtype=np.float64)
    rng = np.random.default_rng(seed)
    out = []
    for f_idx in rng.choice(len(files), size=n, p=sizes / sizes.sum()):
        arr = np.memmap(files[f_idx], dtype=np.uint16, mode="r")
        start = int(rng.integers(0, max(1, len(arr) - length)))
        out.append((files[f_idx].parent.name, tok.decode(arr[start:start + length].tolist(), skip_special=False)))
    return out


def write_report(out_dir: Path, summary: dict) -> None:
    tok = load_default()
    lines = ["# Stage-1 pretraining corpus", "",
             f"Built {summary['finished']} in {summary['seconds'] / 60:.0f} min. Tokenizer: `{summary['tokenizer']}` "
             f"(sha256 `{summary['tokenizer_sha256'][:16]}…`).", "",
             "## Funnel (documents)", "",
             "| source | raw | duplicate | cleaning rejects | token-level rejects | near dup | poem overlap | kept |",
             "|---|---|---|---|---|---|---|---|"]
    for src in SOURCE_ORDER:
        f = summary["funnel"].get(src)
        if not f:
            continue
        clean = sum(f.get(r, 0) for r in ("no_telugu_lines", "too_short", "low_telugu_share", "repeated_lines"))
        token = sum(f.get(r, 0) for r in ("low_content_share", "garbled_text"))
        kept = sum(f.get(f"{s}_docs", 0) for s in ("train", "val", "test"))
        lines.append(f"| {src} | {f['raw']:,} | {f.get('exact_duplicate', 0):,} | {clean:,} | {token:,} | "
                     f"{f.get('near_duplicate', 0):,} | {f.get('poem_overlap', 0):,} | {kept:,} |")
    lines += ["", "Duplicate = exact duplicate document, or (IndicCorp) a paragraph already present in a "
              "Wikipedia/Sangraha document.", "",
              "## Tokens (including <bos>/<eos>)", "", "| source | train | val | test |", "|---|---|---|---|"]
    tot = collections.Counter()
    for src in SOURCE_ORDER:
        f = summary["funnel"].get(src)
        if f:
            lines.append(f"| {src} | {f.get('train_tokens', 0):,} | {f.get('val_tokens', 0):,} | {f.get('test_tokens', 0):,} |")
            for s in ("train", "val", "test"):
                tot[s] += f.get(f"{s}_tokens", 0)
    lines.append(f"| **total** | **{tot['train']:,}** | **{tot['val']:,}** | **{tot['test']:,}** |")
    lines += ["", f"Rejection reasons: {json.dumps(summary['reasons'], ensure_ascii=False)}", "",
              f"Boilerplate lines removed: {summary['after_a']['frequent_lines']:,} distinct lines; "
              f"IndicCorp paragraphs already present in other sources: {summary['after_a']['indiccorp_in_other_sources']:,}.",
              "", "## Poem-overlap examples (the matched region)", ""]
    lines += [f"- `{name}`: {text.replace(chr(10), ' / ')}" for name, text in summary["poem_examples"]]
    lines += ["", "## 20 random 512-token training canvases", ""]
    for k, (src, text) in enumerate(_samples(out_dir, tok), 1):
        lines += [f"### {k}. {src}", "", "```text", text, "```", ""]
    (out_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ main
def _run(pool, fn, shards, *args) -> list[dict]:
    t0, results = time.time(), []
    futures = [pool.submit(fn, s, *args) for s in shards]
    for k, fut in enumerate(as_completed(futures), 1):
        results.append(fut.result())
        print(f"  [{fn.__name__}] {k}/{len(shards)} {results[-1]['shard']} ({time.time() - t0:.0f}s)", flush=True)
    return results


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--limit", type=int, default=0, help="documents per shard (0 = all)")
    ap.add_argument("--work-dir", type=Path, default=PROJECT_ROOT / "pretraining_datasets" / "work")
    ap.add_argument("--out-dir", type=Path, default=PROJECT_ROOT / "pretraining_datasets" / "tokens")
    ap.add_argument("--keep-work", action="store_true", help="keep pass-B token files after pass C")
    args = ap.parse_args(argv)
    if args.out_dir.exists() and any(args.out_dir.iterdir()) and not (args.out_dir / "meta.json").exists():
        raise SystemExit(f"{args.out_dir} is not empty and is not a previous build; refusing to overwrite it")
    t0 = time.time()
    work = args.work_dir
    for sub in ("A", "B"):
        (work / sub).mkdir(parents=True, exist_ok=True)
    shards = sorted(list_shards(), key=lambda s: (SOURCE_ORDER.index(s.source), s.start, s.path))
    big_first = sorted(shards, key=lambda s: s.source != "sangraha")
    ctx = mp.get_context("fork")

    print(f"pass A over {len(shards)} shards", flush=True)
    with ProcessPoolExecutor(args.workers, mp_context=ctx) as pool:
        res_a = _run(pool, pass_a, big_first, work, args.limit)
    after_a = after_pass_a(shards, work)
    print(f"  {after_a}", flush=True)

    if not (work / "poem_windows.npy").exists():
        tok = load_default()
        windows, poem_counts = build_poem_windows(tok, content_mask(tok))
        np.save(work / "poem_windows.npy", windows)
        (work / "poem_windows.json").write_text(json.dumps({"windows": int(windows.size), "poems": poem_counts}, indent=2))
    print(f"poem windows: {json.loads((work / 'poem_windows.json').read_text())}", flush=True)

    print("pass B", flush=True)
    with ProcessPoolExecutor(args.workers, mp_context=ctx, initializer=_init_worker, initargs=(str(work),)) as pool:
        res_b = _run(pool, pass_b, big_first, work, args.limit)

    print("pass C", flush=True)
    if args.out_dir.exists():
        shutil.rmtree(args.out_dir)
    res_c = pass_c(shards, work, args.out_dir, args.keep_work)

    funnel = collections.defaultdict(collections.Counter)
    reasons = collections.Counter()
    for r in res_a:
        funnel[r["shard"].split("-")[0]]["raw"] += r["docs"]
    for r in res_b:
        funnel[r["shard"].split("-")[0]].update(r["reasons"])
        reasons.update({k: v for k, v in r["reasons"].items() if k != "kept"})
    for src, c in res_c["counts"].items():
        funnel[src].update(c)
    summary = {
        "finished": time.strftime("%Y-%m-%d %H:%M"), "seconds": time.time() - t0,
        "tokenizer": str(VOCAB_PATH.relative_to(PROJECT_ROOT)),
        "tokenizer_sha256": hashlib.sha256(VOCAB_PATH.read_bytes()).hexdigest(),
        "limit_per_shard": args.limit, "thresholds": asdict(TH),
        "filters": {"max_rare_share": MAX_RARE_SHARE, "min_content_share": MIN_CONTENT_SHARE,
                    "shingle": SHINGLE, "poem_window": POEM_WINDOW, "val_per_mille": VAL_PER_MILLE,
                    "test_per_mille": TEST_PER_MILLE},
        "sources": json.loads((PROJECT_ROOT / "pretraining_datasets" / "raw" / "manifest.json").read_text(encoding="utf-8")),
        "after_a": after_a, "reasons": dict(reasons), "funnel": {k: dict(v) for k, v in funnel.items()},
        "near_dup": {"docs": res_c["near_dup_docs"], "clusters": res_c["near_dup_clusters"]},
        "poem_examples": res_c["poem_examples"],
    }
    for src in summary["sources"].values():
        src.pop("files", None)
    (args.out_dir / "meta.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(args.out_dir, summary)
    print(f"done in {(time.time() - t0) / 60:.1f} min -> {args.out_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
