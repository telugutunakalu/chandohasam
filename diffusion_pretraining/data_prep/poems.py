"""The stage-2 poem corpora, and the window-hash set used to keep them out of stage-1 data.

A pretraining document is dropped when any window of POEM_WINDOW consecutive
content tokens (≈ five words) also occurs in one of these poems.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

import numpy as np

from .cleaning import normalize
from .fingerprints import window_hashes
from .sources import PROJECT_ROOT

POEM_WINDOW = 20
POEM_SOURCES = {
    "padyarchana_v2": PROJECT_ROOT / "padyarchana_exports" / "padyarchana_poems_v2.jsonl",
    "bhagavatam": PROJECT_ROOT / "dataset" / "bhagavatam.json",
    "vemana": PROJECT_ROOT / "dataset" / "vemana.json",
    "kuchimanchi": PROJECT_ROOT / "dataset" / "kuchimanchi_timmakavi.json",
    "all_poems_txt": Path.home() / "phd_workspace" / "syllabe_aware_tokenizer" / "data" / "all_poems.txt",
}


def iter_poems(name: str, path: Path) -> Iterator[str]:
    if name == "padyarchana_v2":
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                yield json.loads(line).get("text") or ""
    elif name == "all_poems_txt":
        yield from path.read_text(encoding="utf-8").split("\n\n")
    else:
        for rec in json.loads(path.read_text(encoding="utf-8")):
            verse = rec.get("verse") or []
            yield "\n".join(verse) if isinstance(verse, list) else str(verse)


def build_poem_windows(tok, content: np.ndarray) -> tuple[np.ndarray, dict]:
    """Sorted unique window hashes over every poem, plus per-source poem counts."""
    chunks, counts = [], {}
    for name, path in POEM_SOURCES.items():
        if not path.exists():
            counts[name] = "missing"
            continue
        n = 0
        for poem in iter_poems(name, path):
            text = normalize(poem)
            if not text:
                continue
            ids = np.asarray(tok.encode(text), dtype=np.uint16)
            chunks.append(window_hashes(ids[content[ids]], POEM_WINDOW))
            n += 1
        counts[name] = n
    return np.unique(np.concatenate(chunks)), counts
