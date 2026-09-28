"""Syllable-aware Telugu tokenizer: one token per akshara, byte-BPE failover, zero OOV.

Copied from ~/phd_workspace/syllabe_aware_tokenizer (2026-09-26); segmentation now
comes from aksharanusarika so tokens and the meter engine agree on akshara boundaries.
"""
from pathlib import Path

from .telugu_tokenizer import SyllableAwareTeluguTokenizer

VOCAB_PATH = Path(__file__).resolve().parent / "telugu_alldomain.tokenizer.json"


def load_default() -> SyllableAwareTeluguTokenizer:
    """The frozen pretraining tokenizer (telugu_alldomain vocabulary)."""
    return SyllableAwareTeluguTokenizer.load(str(VOCAB_PATH))


__all__ = ["SyllableAwareTeluguTokenizer", "VOCAB_PATH", "load_default"]
