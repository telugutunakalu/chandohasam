# -*- coding: utf-8 -*-
"""
Passages an annotator highlights in a poem (2026-10-30).

A highlight runs from (start_line, start_char) to (end_line, end_char): lines counted from 0, characters (code points)
within the line as printed, ``Poem.plain_lines``, end exclusive. app.js measures the selection the same way, in the
text of each ``.poem-line``, which is exactly the line's tokens; the server keeps the text the offsets cover, so a
browser cannot store words that are not in the poem.
"""
from __future__ import annotations

from typing import Optional, Sequence

SPAN_FIELDS = ("start_line", "start_char", "end_line", "end_char")
Span = tuple[int, int, int, int]


def clean_span(lines: Sequence[str], start_line: int, start_char: int, end_line: int, end_char: int) -> Optional[Span]:
    """The span inside the poem with the white space at both ends left out, or None when it is out of range or
    covers no text."""
    if not (0 <= start_line <= end_line < len(lines)):
        return None
    if not (0 <= start_char <= len(lines[start_line]) and 0 <= end_char <= len(lines[end_line])):
        return None
    a, sc, b, ec = start_line, start_char, end_line, end_char
    while (a, sc) < (b, ec):            # leading white space, and line ends, onto the next line
        if sc < len(lines[a]) and not lines[a][sc].isspace():
            break
        a, sc = (a + 1, 0) if sc >= len(lines[a]) else (a, sc + 1)
    while (a, sc) < (b, ec):            # trailing white space, and line starts, back onto the line before
        if ec > 0 and not lines[b][ec - 1].isspace():
            break
        b, ec = (b - 1, len(lines[b - 1])) if ec == 0 else (b, ec - 1)
    return (a, sc, b, ec) if (a, sc) < (b, ec) else None


def line_ranges(lines: Sequence[str], span: Span) -> dict[int, tuple[int, int]]:
    """The span cut at line ends: line → (start, end) character offsets."""
    a, sc, b, ec = span
    return {i: (sc if i == a else 0, ec if i == b else len(lines[i])) for i in range(a, b + 1)}


def span_text(lines: Sequence[str], span: Span) -> str:
    """The highlighted text, its lines joined with a newline."""
    return "\n".join(lines[i][lo:hi] for i, (lo, hi) in line_ranges(lines, span).items())


def marked_lines(lines: Sequence[Sequence[dict]], spans: Sequence[Span]) -> list[list[dict]]:
    """``Poem.lines`` with each token's text cut into ``parts``, (text, highlighted) pairs, for _poem_text.html."""
    plain = ["".join(t["t"] for t in line) for line in lines]
    covered: dict[int, list[tuple[int, int]]] = {}
    for span in spans:
        for i, r in line_ranges(plain, span).items():
            covered.setdefault(i, []).append(r)
    out = []
    for i, line in enumerate(lines):
        ranges = covered.get(i, [])
        pos, tokens = 0, []
        for t in line:
            text, start = t["t"], pos
            pos += len(text)
            cuts = sorted({0, len(text)} | {min(max(x - start, 0), len(text)) for r in ranges for x in r})
            parts = []
            for lo, hi in zip(cuts, cuts[1:]):
                hl = any(r0 <= start + lo and start + hi <= r1 for r0, r1 in ranges)
                if parts and parts[-1][1] == hl:
                    parts[-1] = (parts[-1][0] + text[lo:hi], hl)
                else:
                    parts.append((text[lo:hi], hl))
            tokens.append({**t, "parts": parts})
        out.append(tokens)
    return out
