"""E4: does the model copy poems from its training split?

    ../.venv/bin/python memorisation.py --run e3_e2_pretrained

For every poem of an E3 run (runs/<run>/results.jsonl), against the poem train split
(data/tokens/poems/train.bin, cut into poems by data/poems_index.jsonl):

- **longest shared run.** The longest run of aksharas the poem shares with any one training poem,
  measured at fixed lengths N in LENGTHS: the largest N for which some N-akshara window of the poem
  occurs in a training poem.
  - Spaces and line breaks are ignored, so a copied line counts whatever its spacing.
  - Windows never cross a poem boundary.
  - Uses 64-bit polynomial hashes of the akshara-token windows.
- **verbatim pādas.** The share of the poem's lines that occur as a whole line in the train split.
  Reported in two parts:
  - **refrain lines**: lines found in at least REFRAIN training poems (a makuta, a samasya);
  - **other lines**: a copy of an ordinary line.

With --train-records (e.g. data/e6/records/train.jsonl, for E6 runs) the train split is those records' poem
lines instead of the E-series token file.

Writes results/<run>_memorisation.md and .json: numbers per strategy, and the keys of the most-copied
poems (no text).
"""
from __future__ import annotations

import argparse
import collections
import json

import numpy as np

from pathlib import Path

from common import HERE, INDEX, TOKENS, tokenizer

LENGTHS = (6, 8, 12, 16, 24, 32)
REFRAIN = 5
BASE = np.uint64(0x9E3779B97F4A7C15 | 1)        # odd, so invertible modulo 2^64


def window_hashes(seq: np.ndarray, n: int, boundary: np.ndarray | None = None) -> np.ndarray:
    """Hashes of every n-token window of ``seq`` (uint64 arithmetic wraps modulo 2^64); windows that
    contain a ``boundary`` position are dropped."""
    L = len(seq)
    if L < n:
        return np.zeros(0, dtype=np.uint64)
    with np.errstate(over="ignore"):
        powers = np.cumprod(np.full(L, BASE, dtype=np.uint64), dtype=np.uint64)
        powers = np.concatenate(([np.uint64(1)], powers[:-1]))                 # BASE^j
        inv = np.uint64(pow(int(BASE), -1, 2**64))
        inv_powers = np.cumprod(np.full(L, inv, dtype=np.uint64), dtype=np.uint64)
        inv_powers = np.concatenate(([np.uint64(1)], inv_powers[:-1]))         # BASE^-j
        prefix = np.concatenate(([np.uint64(0)], np.cumsum((seq.astype(np.uint64) + np.uint64(1)) * powers,
                                                             dtype=np.uint64)))
        h = (prefix[n:] - prefix[:-n]) * inv_powers[: L - n + 1]
    if boundary is not None:
        b = np.concatenate(([0], np.cumsum(boundary)))
        h = h[(b[n:] - b[:-n]) == 0]
    return h


def contains_any(sorted_hashes: np.ndarray, h: np.ndarray) -> bool:
    """Whether any of ``h`` occurs in ``sorted_hashes`` (binary search; np.isin would re-sort the 22M each call)."""
    if not len(h) or not len(sorted_hashes):
        return False
    i = np.minimum(np.searchsorted(sorted_hashes, h), len(sorted_hashes) - 1)
    return bool((sorted_hashes[i] == h).any())


def akshara_ids(ids, drop: set[int]) -> np.ndarray:
    return np.array([i for i in ids if i not in drop], dtype=np.uint16)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="an E3 run folder under runs/")
    ap.add_argument("--train-records", type=Path, help="ft.build_data train records (E6) instead of the E-series split")
    args = ap.parse_args(argv)

    tok = tokenizer()
    nl, sp = tok.encode("\n")[0], tok.encode(" ")[0]
    drop = {tok.bos_id, tok.eos_id, sp, nl}

    # the train split as akshara-only poems separated by a boundary, and its lines
    seqs, line_poems = [], collections.Counter()
    if args.train_records:
        for row in map(json.loads, open(args.train_records, encoding="utf-8")):
            lines = [akshara_ids(tok.encode(ln), drop) for ln in row.get("lines") or []]
            lines = [ln for ln in lines if len(ln)]
            if lines:
                line_poems.update({tuple(ln.tolist()) for ln in lines})
                seqs.append(np.concatenate(lines))
    else:
        train = np.fromfile(TOKENS / "poems" / "train.bin", dtype=np.uint16)
        with INDEX.open(encoding="utf-8") as fh:
            for row in map(json.loads, fh):
                if row["split"] != "train":
                    continue
                ids = train[row["offset"]: row["offset"] + row["n_tokens"]]
                lines, cur = set(), []
                for i in ids.tolist():
                    if i == nl or i == tok.eos_id:
                        if cur:
                            lines.add(tuple(cur))
                        cur = []
                    elif i not in drop:
                        cur.append(i)
                line_poems.update(lines)
                seqs.append(akshara_ids(ids.tolist(), drop))
    sep = np.uint16(tok.pad_id)                     # never inside a poem
    flat = np.concatenate([np.concatenate((s, [sep])) for s in seqs])
    boundary = (flat == sep).astype(np.int64)
    train_hashes = {n: np.unique(window_hashes(flat, n, boundary)) for n in LENGTHS}
    print(f"train: {len(seqs):,} poems, {int((flat != sep).sum()):,} aksharas, {len(line_poems):,} distinct lines",
          flush=True)

    run = HERE / "runs" / args.run
    per_mode = collections.defaultdict(lambda: collections.defaultdict(list))
    worst = []
    for r in map(json.loads, open(run / "results.jsonl", encoding="utf-8")):
        ids = tok.encode(r["text"])
        seq = akshara_ids(ids, drop)
        longest = 0
        for n in LENGTHS:
            if contains_any(train_hashes[n], window_hashes(seq, n)):
                longest = n
        lines = [akshara_ids(tok.encode(l), drop) for l in r["text"].split("\n") if l.strip()]
        lines = [tuple(l.tolist()) for l in lines if len(l)]
        refrain = sum(line_poems.get(l, 0) >= REFRAIN for l in lines)
        other = sum(0 < line_poems.get(l, 0) < REFRAIN for l in lines)
        m = per_mode[r["mode"]]
        m["longest"].append(longest)
        m["lines"].append(len(lines))
        m["refrain_lines"].append(refrain)
        m["other_verbatim_lines"].append(other)
        worst.append((other, longest, r["key"]))

    summary = {}
    for mode, m in per_mode.items():
        n_lines = max(1, sum(m["lines"]))
        summary[mode] = {
            "poems": len(m["longest"]),
            "longest_run_share": {f">={n}": sum(x >= n for x in m["longest"]) / len(m["longest"]) for n in LENGTHS},
            "verbatim_refrain_line_share": sum(m["refrain_lines"]) / n_lines,
            "verbatim_other_line_share": sum(m["other_verbatim_lines"]) / n_lines,
            "poems_with_a_copied_ordinary_line": sum(x > 0 for x in m["other_verbatim_lines"]) / len(m["longest"]),
        }
    worst.sort(reverse=True)
    out = {"run": args.run, "lengths": LENGTHS, "refrain_min_poems": REFRAIN, "by_mode": summary,
           "most_copied": [{"key": k, "other_verbatim_lines": o, "longest_run_at_least": lg} for o, lg, k in worst[:20]]}
    path = HERE / "results" / f"{args.run.replace('/', '_')}_memorisation"
    path.with_suffix(".json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    md = [f"# Memorisation: `{args.run}`", "",
          f"Shares of poems whose longest akshara run shared with a training poem reaches N; verbatim lines: "
          f"refrain = a line found in ≥ {REFRAIN} training poems.", "",
          "| strategy | poems | " + " | ".join(f"run ≥ {n}" for n in LENGTHS) +
          " | refrain lines % | other verbatim lines % | poems copying an ordinary line % |",
          "|---|---|" + "---|" * len(LENGTHS) + "---|---|---|"]
    for mode, s in summary.items():
        md.append(f"| {mode} | {s['poems']} | " + " | ".join(f"{100 * s['longest_run_share'][f'>={n}']:.1f}"
                                                         for n in LENGTHS) +
                  f" | {100 * s['verbatim_refrain_line_share']:.1f} | {100 * s['verbatim_other_line_share']:.1f} | "
                  f"{100 * s['poems_with_a_copied_ordinary_line']:.1f} |")
    path.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
