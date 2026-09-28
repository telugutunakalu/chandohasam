"""Corpus loaders — stream text lines from the formats found in the wild.

Handles: plain text (one doc/line), the Telugu-Wikipedia TSV export
(``Sentence<TAB>Frequency`` with a header), JSON (recursively pulls every
Telugu-bearing string), and CSV (Telugu-bearing string cells).  Everything is a
generator so a multi-GB corpus never has to be held in memory.
"""
from __future__ import annotations

import csv
import json
import os
from typing import Iterator, List

_TEL_LO, _TEL_HI = 0x0C00, 0x0C7F


def _has_telugu(s: str) -> bool:
    return any(_TEL_LO <= ord(c) <= _TEL_HI for c in s)


def _iter_txt(path: str) -> Iterator[str]:
    """Plain text.  Auto-detects the ``Sentence<TAB>Frequency`` TSV export and
    yields only the sentence column (dropping the header + count)."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        first = fh.readline()
        cols = first.rstrip("\n").split("\t")
        is_tsv = len(cols) == 2 and cols[1].strip().lower() in ("frequency", "count", "freq")
        if not is_tsv and first.strip():
            yield first.rstrip("\n")
        for line in fh:
            line = line.rstrip("\n")
            if not line:
                continue
            if is_tsv:
                yield line.split("\t", 1)[0]
            else:
                yield line


def _walk_json(obj) -> Iterator[str]:
    if isinstance(obj, str):
        if _has_telugu(obj):
            yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_json(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_json(v)


def _iter_json(path: str) -> Iterator[str]:
    with open(path, encoding="utf-8", errors="replace") as fh:
        yield from _walk_json(json.load(fh))


def _iter_csv(path: str) -> Iterator[str]:
    with open(path, encoding="utf-8", errors="replace", newline="") as fh:
        for row in csv.reader(fh):
            for cell in row:
                if _has_telugu(cell):
                    yield cell


def _iter_parquet(path: str) -> Iterator[str]:
    """Stream Telugu-bearing string cells from a .parquet file, row group by
    row group (keeps memory bounded on large files). Needs pyarrow."""
    import pyarrow.parquet as pq

    pf = pq.ParquetFile(path)
    for batch in pf.iter_batches(batch_size=8192):
        for col in batch.schema.names:
            arr = batch.column(col)
            # Only string-like columns can carry text.
            for val in arr.to_pylist():
                if isinstance(val, str) and _has_telugu(val):
                    yield val


def iter_file(path: str) -> Iterator[str]:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        yield from _iter_json(path)
    elif ext == ".csv":
        yield from _iter_csv(path)
    elif ext == ".parquet":
        yield from _iter_parquet(path)
    else:  # .txt and everything else
        yield from _iter_txt(path)


def iter_corpus(paths: List[str]) -> Iterator[str]:
    """Stream text from many files/dirs (dirs are walked recursively)."""
    for path in paths:
        if os.path.isdir(path):
            for root, _, files in os.walk(path):
                for name in sorted(files):
                    if name.lower().endswith((".txt", ".json", ".csv", ".parquet")):
                        yield from iter_file(os.path.join(root, name))
        else:
            yield from iter_file(path)
