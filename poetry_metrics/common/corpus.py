"""The four dataset files in ../dataset/ as (poem id, metre, lines, English meaning) records.

Lines are the units the metrics score. They are the printed lines, except that
a seesa pāda printed on one line with " - " between its halves (chandassu) is
split into its two half-lines, the way Bhagavatam and Kuchimanchi print it and
the way meter_engine reads it (same rule as data_sanity_metrics/common/scansion.py).
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = REPO_ROOT / "dataset"

# dataset name (file stem) -> file; every metric reports per file, in this order
CORPORA = {
    "bhagavatam": "bhagavatam.json",
    "vemana": "vemana.json",
    "kuchimanchi_timmakavi": "kuchimanchi_timmakavi.json",
    "chandassu": "chandassu.json",
}

HALF_LINE_SEPARATOR = re.compile(r"(?<=\S)(?:-\s+-\s*|\s*-\s+|\s+-\s*)(?=\S)")


@dataclass(frozen=True)
class Poem:
    key: str         # "<corpus>:<id>"
    corpus: str
    metre: str | None
    lines: tuple
    meaning_en: str = ""     # the record's English meaning (bhavam_en), '' when absent

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


def _clean(text) -> str:
    return unicodedata.normalize("NFC", text or "").strip()


def _lines(record: dict) -> tuple:
    lines = tuple(_clean(l) for l in record.get("verse") or [] if _clean(l))
    if record.get("metre_roman") == "seesamu":
        lines = tuple(h.strip() for l in lines for h in HALF_LINE_SEPARATOR.split(l) if h.strip())
    return lines


@lru_cache(maxsize=None)
def load(corpus: str, form: str = "verse") -> tuple:
    """Records of one form (verse | prose) of one dataset file, in file order."""
    records = json.loads((DATASET_DIR / CORPORA[corpus]).read_text(encoding="utf-8"))
    poems = []
    for r in records:
        if (r.get("form") or "verse") != form:
            continue
        lines = _lines(r)
        if lines:
            poems.append(Poem(f"{corpus}:{r['id']}", corpus, r.get("metre_roman"), lines,
                              _clean(r.get("bhavam_en"))))
    return tuple(poems)
