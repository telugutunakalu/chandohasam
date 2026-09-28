"""Cheap quality metrics for generated Telugu (no external model needed).

Generative perplexity alone can be gamed by repetitive, low-entropy text, so it
is always read next to entropy, distinct-n and repetition; the Telugu-specific
checks catch malformed script that fluent-looking perplexity would hide.
"""
from __future__ import annotations

import collections
import math

from data_prep.cleaning import telugu_share


def _words(text: str) -> list[str]:
    return text.split()


def sample_metrics(texts: list[str], ids: list[list[int]], tok, known_words: set[str] | None = None) -> dict:
    ent, rep, bad_pairs, pairs = [], [], 0, 0
    ngram = {n: collections.Counter() for n in (1, 2, 3)}
    telugu = rare = words_total = words_known = 0
    for text, seq in zip(texts, ids):
        counts = collections.Counter(seq)
        total = sum(counts.values())
        ent.append(-sum(c / total * math.log(c / total) for c in counts.values()) if total else 0.0)
        w = _words(text)
        for n in ngram:
            ngram[n].update(tuple(w[i:i + n]) for i in range(len(w) - n + 1))
        grams = [tuple(w[i:i + 4]) for i in range(len(w) - 3)]
        rep.append(1 - len(set(grams)) / len(grams) if grams else 0.0)
        for a, b in zip(seq, seq[1:]):
            pairs += 1
            bad_pairs += tok.blocks_next(a, b)
        _, t, r = tok.encode_with_stats(text)
        telugu, rare = telugu + t, rare + r
        if known_words is not None:
            tw = [x for x in w if telugu_share(x) == 1.0]
            words_total += len(tw)
            words_known += sum(x in known_words for x in tw)
    out = {
        "token_entropy": sum(ent) / max(1, len(ent)),
        "repeated_4gram_share": sum(rep) / max(1, len(rep)),
        "rare_akshara_share": rare / max(1, telugu),
        "dangling_virama_per_1k": 1000 * bad_pairs / max(1, pairs),
        "telugu_share": telugu_share(" ".join(texts)),
    }
    for n, c in ngram.items():
        out[f"distinct_{n}"] = len(c) / max(1, sum(c.values()))
    if known_words is not None:
        out["known_word_share"] = words_known / max(1, words_total)
    return out
