"""Text normalisation, line-level cleaning and document-level filters.

Normalisation matches the tokenizer (NFC, ZWJ/ZWNJ/BOM stripped) plus whitespace
tidying, so the hashes computed here are stable across passes.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass

import numpy as np

from tokenizer import akshara

_SPACES = re.compile(r"[ \t  -​  　]+")
_CONTROL = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
_URL = re.compile(r"(?:https?://|www\.)\S+|\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
_TELUGU_LETTER = re.compile(r"[అ-హౘ-ౡ]")
_OTHER_LETTER = re.compile(r"[^\W\d_ఀ-౿]")


@dataclass(frozen=True)
class Thresholds:
    min_line_telugu_share: float = 0.5    # a kept line is mostly Telugu script
    min_doc_telugu_letters: int = 40       # ≈ 15 aksharas; shorter docs are fragments
    min_doc_telugu_share: float = 0.8
    max_dup_line_share: float = 0.3        # share of a doc's lines that repeat inside it
    frequent_line_docs: int = 10           # a line in this many distinct docs is boilerplate


def normalize(text: str) -> str:
    """NFC + tokenizer normalisation, control characters removed, spaces collapsed,
    lines stripped, blank lines dropped. URLs and e-mail addresses are cut out of lines
    by clean_doc, not here, so hashes see the text as published."""
    text = text.replace("\\n", "\n").replace("\r\n", "\n").replace("\r", "\n")   # some docs carry a literal "\\n"
    text = _CONTROL.sub(" ", akshara.normalize(text))
    lines = (_SPACES.sub(" ", ln).strip() for ln in text.split("\n"))
    return "\n".join(ln for ln in lines if ln)


def stable_hash(text: str) -> int:
    """64-bit content hash, identical across processes and runs."""
    return int.from_bytes(hashlib.blake2b(text.encode("utf-8", "surrogatepass"), digest_size=8).digest(), "little")


def telugu_share(text: str) -> float:
    """Telugu letters / all letters (0.0 when the text has no letters)."""
    tel = len(_TELUGU_LETTER.findall(text))
    other = len(_OTHER_LETTER.findall(text))
    return tel / (tel + other) if tel + other else 0.0


def clean_doc(text: str, frequent_lines: np.ndarray | None, th: Thresholds = Thresholds()) -> tuple[str, str]:
    """Return (cleaned text, "") or ("", rejection reason). ``text`` must already be
    normalised; ``frequent_lines`` is a sorted array of boilerplate line hashes."""
    lines = text.split("\n")
    boiler = np.zeros(len(lines), dtype=bool)
    if frequent_lines is not None and frequent_lines.size:
        hashes = np.fromiter((stable_hash(ln) for ln in lines), dtype=np.uint64, count=len(lines))
        pos = np.minimum(np.searchsorted(frequent_lines, hashes), frequent_lines.size - 1)
        boiler = frequent_lines[pos] == hashes
    kept = []
    for ln, b in zip(lines, boiler):
        if b:
            continue
        ln = _SPACES.sub(" ", _URL.sub(" ", ln)).strip()
        if ln and telugu_share(ln) >= th.min_line_telugu_share:
            kept.append(ln)
    if not kept:
        return "", "no_telugu_lines"
    out = "\n".join(kept)
    if len(_TELUGU_LETTER.findall(out)) < th.min_doc_telugu_letters:
        return "", "too_short"
    if telugu_share(out) < th.min_doc_telugu_share:
        return "", "low_telugu_share"
    if len(kept) >= 4 and 1 - len(set(kept)) / len(kept) > th.max_dup_line_share:
        return "", "repeated_lines"
    return out, ""
