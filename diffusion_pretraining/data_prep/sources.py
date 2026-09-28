"""Raw documents of each stage-1 source, split into shards for parallel processing.

Iteration order within a shard is deterministic, so a document can be addressed
by (shard, position) across passes.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import pyarrow.parquet as pq

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "pretraining_datasets" / "raw"
SOURCE_ORDER = ("wikipedia", "sangraha", "indiccorp")   # exact duplicates keep the earliest source
INDICCORP_CHUNKS = 48


@dataclass(frozen=True)
class Shard:
    source: str
    path: str
    start: int = 0      # byte range, for the IndicCorp text file
    end: int = 0

    @property
    def name(self) -> str:
        stem = Path(self.path).stem
        return f"{self.source}-{stem}" if self.source != "indiccorp" else f"indiccorp-{self.start:012d}"


@dataclass(frozen=True)
class Doc:
    id: str
    text: str
    kind: str           # wiki | web | pdf | speech | paragraph


def list_shards(raw_dir: Path = RAW_DIR) -> list[Shard]:
    shards = [Shard("wikipedia", str(p)) for p in sorted((raw_dir / "wikipedia").rglob("*.parquet"))]
    shards += [Shard("sangraha", str(p)) for p in sorted((raw_dir / "sangraha").rglob("*.parquet"),
                                                         key=lambda p: int(p.stem.split("-")[-1]))]
    txt = raw_dir / "indiccorp" / "data" / "te.txt"
    if txt.exists():
        size = txt.stat().st_size
        bounds = [size * i // INDICCORP_CHUNKS for i in range(INDICCORP_CHUNKS + 1)]
        shards += [Shard("indiccorp", str(txt), a, b) for a, b in zip(bounds, bounds[1:])]
    return shards


def _iter_parquet(shard: Shard, id_col: str, kind_col: str | None, default_kind: str) -> Iterator[Doc]:
    cols = [id_col, "text"] + ([kind_col] if kind_col else [])
    for batch in pq.ParquetFile(shard.path).iter_batches(batch_size=4096, columns=cols):
        ids = batch.column(id_col).to_pylist()
        texts = batch.column("text").to_pylist()
        kinds = batch.column(kind_col).to_pylist() if kind_col else [default_kind] * len(ids)
        for i, t, k in zip(ids, texts, kinds):
            yield Doc(f"{shard.source}:{i}", t or "", k or default_kind)


def _iter_indiccorp(shard: Shard) -> Iterator[Doc]:
    """One paragraph per line; a line belongs to the chunk its first byte falls in."""
    with open(shard.path, "rb") as fh:
        fh.seek(shard.start)
        if shard.start:
            fh.readline()                      # finish the line the previous chunk owns
        pos = fh.tell()
        while pos < shard.end:
            line = fh.readline()
            if not line:
                break
            text = line.decode("utf-8", "replace").strip()
            if text:
                yield Doc(f"indiccorp:{pos}", text, "paragraph")
            pos += len(line)


def iter_docs(shard: Shard) -> Iterator[Doc]:
    if shard.source == "wikipedia":
        return _iter_parquet(shard, "id", None, "wiki")
    if shard.source == "sangraha":
        return _iter_parquet(shard, "doc_id", "type", "web")
    if shard.source == "indiccorp":
        return _iter_indiccorp(shard)
    raise ValueError(shard.source)
