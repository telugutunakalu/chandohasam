"""Near-duplicate detection by character 8-gram containment (the matcher of
meter_engine/scripts/import_chandassu.py, made fast enough for 380k queries).

Texts are compared on Telugu letters and signs only, without ఁ: spacing, punctuation and
the ardhabindu differ between editions of the same poem. Grams shared by more than
``max_df`` indexed texts (formulae, refrains) are ignored on both sides of the ratio.
"""
from __future__ import annotations

import collections
import unicodedata

GRAM = 8


def canon(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    return "".join(ch for ch in text if "ఀ" <= ch <= "ౣ" and ch != "ఁ")


def grams(text: str) -> set[str]:
    c = canon(text)
    return {c[i:i + GRAM] for i in range(max(0, len(c) - GRAM + 1))}


class GramIndex:
    def __init__(self, texts: dict[str, str], max_df: int = 50):
        df = collections.Counter()
        per = {}
        for key, text in texts.items():
            g = grams(text)
            per[key] = g
            df.update(g)
        self.stop = {g for g, n in df.items() if n > max_df}
        self.index: dict[str, list[str]] = collections.defaultdict(list)
        self.size = {}
        for key, g in per.items():
            g = g - self.stop
            self.size[key] = len(g)
            for gram in g:
                self.index[gram].append(key)

    def matches(self, text: str, threshold: float) -> list[tuple[str, float, float]]:
        """(key, share of the indexed text's grams found in ``text``, share of ``text``'s grams found
        in the indexed text) for every indexed text where either share reaches ``threshold``."""
        g = grams(text) - self.stop
        if not g:
            return []
        hits = collections.Counter(k for gram in g for k in self.index.get(gram, ()))
        out = []
        for key, h in hits.items():
            a, b = h / max(1, self.size[key]), h / len(g)
            if max(a, b) >= threshold:
                out.append((key, a, b))
        return sorted(out, key=lambda x: -max(x[1], x[2]))
