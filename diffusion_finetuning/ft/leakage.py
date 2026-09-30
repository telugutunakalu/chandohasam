"""Leakage audit (PLAN §3.2): do the val / test poems or their meanings occur in the
pretraining corpus?

Every 20-content-token window of each eval poem and meaning is hashed with the fingerprint
data_prep used to keep poems out of the pretraining corpus, and every pretraining token
file (train / val / test of each source) is scanned for those hashes.

    uv run --project ../diffusion_pretraining python -m ft.leakage

Writes <data>/leakage.json: per eval item with any hit, the number of its poem and meaning
windows found and where; plus totals. Items listed there should be excluded from reporting.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import time
from pathlib import Path

import numpy as np

from data_prep.fingerprints import content_mask, window_hashes
from data_prep.poems import POEM_WINDOW
from tokenizer import load_default

from . import DATA_DIR, PRETRAIN_ROOT

TOKEN_DIR = PRETRAIN_ROOT.parent / "pretraining_datasets" / "tokens"
CHUNK = 2_000_000

_Q: np.ndarray | None = None
_CONTENT: np.ndarray | None = None


def _scan(job: tuple[str, int, int]) -> np.ndarray:
    """Query hashes found in tokens [start, end) of one file (content tokens, windows may run
    into the next chunk by POEM_WINDOW - 1 tokens)."""
    path, start, end = job
    arr = np.memmap(path, dtype=np.uint16, mode="r")
    ids = np.asarray(arr[start:min(len(arr), end + 4 * POEM_WINDOW)])
    c = ids[_CONTENT[ids]]
    h = window_hashes(c, POEM_WINDOW)
    if not len(h):
        return np.empty(0, dtype=np.uint64)
    pos = np.searchsorted(_Q, h).clip(max=len(_Q) - 1)
    return np.unique(h[_Q[pos] == h])


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", type=Path, default=DATA_DIR)
    ap.add_argument("--token-dir", type=Path, default=TOKEN_DIR)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args(argv)
    t0 = time.time()
    tok = load_default()
    content = content_mask(tok)

    owners: list[tuple[str, str]] = []                  # (eval id, "poem" | "meaning")
    hashes, owner_of = [], []
    for split in ("val", "test", "test_seen"):
        path = args.data_dir / "records" / f"{split}.jsonl"
        if not path.exists():
            continue
        for line in path.open(encoding="utf-8"):
            r = json.loads(line)
            for kind, text in (("poem", "\n".join(r["lines"])), ("meaning", r.get("meaning") or "")):
                ids = np.asarray(tok.encode(text), dtype=np.uint16)
                h = np.unique(window_hashes(ids[content[ids]], POEM_WINDOW))
                if len(h):
                    owners.append((r["id"], kind))
                    hashes.append(h)
                    owner_of.append(np.full(len(h), len(owners) - 1))
    all_h = np.concatenate(hashes)
    all_o = np.concatenate(owner_of)
    order = np.argsort(all_h)
    all_h, all_o = all_h[order], all_o[order]
    query = np.unique(all_h)
    print(f"{len(owners):,} eval texts, {len(query):,} distinct windows", flush=True)

    jobs = []
    for f in sorted(args.token_dir.glob("*/*.bin")):
        n = len(np.memmap(f, dtype=np.uint16, mode="r"))
        jobs += [(str(f), s, s + CHUNK) for s in range(0, n, CHUNK)]
    global _Q, _CONTENT
    _Q, _CONTENT = query, content
    found: dict[str, set] = {}
    with mp.get_context("fork").Pool(args.workers) as pool:
        for (path, _, _), hits in zip(jobs, pool.imap(_scan, jobs, chunksize=4)):
            if len(hits):
                found.setdefault(path, set()).update(int(x) for x in hits)
    print(f"scanned {len(jobs):,} chunks in {time.time() - t0:.0f}s", flush=True)

    per_item: dict[str, dict] = {}
    for path, hs in found.items():
        hs = np.fromiter(hs, dtype=np.uint64)
        lo, hi = np.searchsorted(all_h, hs, "left"), np.searchsorted(all_h, hs, "right")
        for a, b in zip(lo, hi):
            for o in set(all_o[a:b].tolist()):
                rid, kind = owners[o]
                item = per_item.setdefault(rid, {"poem": 0, "meaning": 0, "files": []})
                item[kind] += 1
                src = str(Path(path).relative_to(args.token_dir))
                if src not in item["files"]:
                    item["files"].append(src)
    report = {"eval_texts": len(owners), "items_with_hits": len(per_item),
              "poem_hits": sum(1 for v in per_item.values() if v["poem"]),
              "meaning_hits": sum(1 for v in per_item.values() if v["meaning"]),
              "items": dict(sorted(per_item.items()))}
    (args.data_dir / "leakage.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print({k: v for k, v in report.items() if k != "items"}, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
