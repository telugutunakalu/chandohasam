# -*- coding: utf-8 -*-
"""Shared helpers for the metrical_decoder tests (not a test module).

The test vocabulary imitates a subword tokenizer without needing one: every
Telugu character of the corpus (so any text can be spelled), the most frequent
aksharas, and frequent whole words with and without a leading space — tokens
that start and end inside aksharas, like Gemma's.
"""
from __future__ import annotations

import json
import sys
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from indic_meter_dawg import scansion as sc                      # noqa: E402
from metrical_decoder import TokenIndex                          # noqa: E402

DATASET = HERE.parent.parent / "dataset"
FIXTURES = HERE / "fixtures"


@lru_cache(maxsize=1)
def corpus_lines() -> tuple[str, ...]:
    """Vemana and Kūcimañci lines (the small corpora), NFC, stripped."""
    out = []
    for name in ("vemana.json", "kuchimanchi_timmakavi.json"):
        for rec in json.loads((DATASET / name).read_text(encoding="utf-8")):
            for ln in rec.get("verse") or []:
                ln = unicodedata.normalize("NFC", ln).strip()
                if ln:
                    out.append(ln)
    return tuple(out)


@lru_cache(maxsize=1)
def test_vocab() -> TokenIndex:
    chars, aks, words = Counter(), Counter(), Counter()
    for ln in corpus_lines():
        clean = "".join(ch for ch in ln if ch not in "​‌‍﻿")
        chars.update(ch for ch in clean if "ఀ" <= ch <= "౿")
        aks.update(s.text for s in sc.syllabify(clean))
        words.update(w for w in clean.split() if all("ఀ" <= ch <= "౿" for ch in w))
    texts = list(chars) + [a for a, _ in aks.most_common(300)]
    for w, _ in words.most_common(300):
        texts += [w, " " + w]
    texts = list(dict.fromkeys(texts)) + [" ", "\n"]
    return TokenIndex.from_texts(list(enumerate(texts, start=1000)), eos_ids=(1,))


@lru_cache(maxsize=1)
def classics() -> list[dict]:
    return yaml.safe_load((FIXTURES / "classics.yaml").read_text(encoding="utf-8"))["stanzas"]
