"""Akshara segmentation for the tokenizer, delegated to aksharanusarika.

The tokenizer and the meter engine must agree on what an akshara is, so the
segmentation comes from the one copy of aksharanusarika the meter engine uses
(meter_engine/aksharanusarika.py), loaded through the meter engine's own loader
so the same table extensions (ౘ/ౙ, ౢ/ౣ) apply.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

METER_ENGINE_DIR = Path(__file__).resolve().parents[2] / "meter_engine"


@lru_cache(maxsize=1)
def _aksharanusarika():
    if str(METER_ENGINE_DIR) not in sys.path:
        sys.path.append(str(METER_ENGINE_DIR))
    from prasa.aksharanusarika_loader import load_aksharanusarika
    return load_aksharanusarika()


def _is_telugu(ch: str) -> bool:
    return "ఀ" <= ch <= "౿"


def aksharas(text: str) -> list[str]:
    """Split text into aksharas exactly as aksharanusarika does, except that each
    run of non-Telugu characters (which aksharanusarika emits one character at a
    time) is kept together. Lossless for text without ZWNJ: "".join(out) == text."""
    out: list[str] = []
    for piece in _aksharanusarika().split_aksharalu(text):
        if out and not _is_telugu(piece[0]) and not _is_telugu(out[-1][0]):
            out[-1] += piece
        else:
            out.append(piece)
    return out
