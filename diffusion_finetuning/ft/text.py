"""Text conventions shared by the data builder, the canvases and (later) the decoder.

Poem targets (PLAN §3.1): NFC, ZWJ/ZWNJ stripped, every character that is not a Telugu
letter or sign replaced by a space (punctuation, digits, danda, the line-continuation
"-"), one pāda per line. Meanings keep their punctuation; only whitespace is collapsed.

Canvas headers are plain Telugu lines, so no token is added to the vocabulary.
"""
from __future__ import annotations

import re

from tokenizer.akshara import normalize

# ---- header keys and values (PLAN §5.1) --------------------------------------
METRE_KEY = "ఛందస్సు"
STYLE_KEY = "శైలి"
CLASSICAL, MODERN = "ప్రాచీన", "ఆధునిక"
SAMASYA_KEY, MAKUTAM_KEY = "సమస్య", "మకుటం"
MEANING_KEY = "భావం"
SRC_EDITION, SRC_MACHINE = "గ్రంథం", "యంత్రం"
POEM_KEY = "పద్యం"
GLOSS_KEY = "ప్రతిపదార్థం"
LEXICON_KEY = "అర్థాలకు పదాలు"

MODERN_SOURCE_PREFIX = "శంకరాభరణం"          # the online Śaṅkarābharaṇam forum (all its sub-sources)

_NOT_TELUGU = re.compile(r"[^ఀ-౥౰-౿ ]")     # Telugu digits (U+0C66-6F) are dropped too
_SPACES = re.compile(r"\s+")
_HALF_SEP = re.compile(r"(?<=[ఀ-౿])-\s+(?=[ఀ-౿])|\s+-\s+|\s*[|।॥]\s*")


def register_of(source: str | None) -> str:
    return MODERN if (source or "").startswith(MODERN_SOURCE_PREFIX) else CLASSICAL


def clean_poem_line(line: str) -> str:
    """A pāda as a training target: Telugu letters and single spaces only."""
    line = normalize(line.replace("_x000D_", " "))
    return _SPACES.sub(" ", _NOT_TELUGU.sub(" ", line)).strip()


def clean_poem(lines: list[str]) -> list[str]:
    return [c for c in (clean_poem_line(ln) for ln in lines) if c]


def clean_meaning(text: str | None) -> str:
    if not text:
        return ""
    return _SPACES.sub(" ", normalize(text.replace("_x000D_", " "))).strip()


def content_key(line: str) -> str:
    """Letters only (no spaces): the key used to find lines shared by many poems."""
    return clean_poem_line(line).replace(" ", "")


def raw_lines(lines_or_text) -> list[str]:
    """Printed lines: NFC, ZWJ/ZWNJ stripped (a ZWNJ before a "-" hides the separator), whitespace
    collapsed, empty lines dropped. Punctuation is kept: the engine and split_pieces need it."""
    if isinstance(lines_or_text, str):
        lines_or_text = lines_or_text.split("\n")
    out = []
    for ln in lines_or_text or []:
        ln = _SPACES.sub(" ", normalize((ln or "").replace("_x000D_", " "))).strip()
        if ln:
            out.append(ln)
    return out


def split_pieces(lines: list[str]) -> list[str]:
    """Split printed lines at the separators editions use between pādas or seesa halves:
    "|", "।", "॥", " - " and a hyphen followed by a space ("…రో- రాజ…"). A hyphen at the very
    end of a line (a word running on into the next pāda) is not a separator."""
    out = []
    for ln in lines:
        out += [p.strip() for p in _HALF_SEP.split(ln) if p and p.strip()]
    return out

