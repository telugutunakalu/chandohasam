# -*- coding: utf-8 -*-
"""
Read-only access to the precomputed poems and ruleset reference (data/*.json).

Both files are written by build_data.py and loaded once per process. The app never
runs meter_engine, so the gaṇa division an annotator sees is identical everywhere.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Optional

VIKALPA_NOTES = {
    "padanta": "పాదాంత లఘువు గురువుగా · pāda-final laghu read as guru",
    "word_initial_conjunct": "తరువాతి పదం సంయుక్తాక్షరంతో మొదలు, వికల్పంగా గురువు · vikalpa: next word begins with a conjunct",
    "repha_conjunct": "రేఫ సంయుక్తానికి ముందు, వికల్పంగా లఘువు · vikalpa: before a ర-vattu conjunct",
    "word_initial_conjunct+repha_conjunct": "వికల్పం (సంయుక్తాక్షరం / రేఫ) · vikalpa: conjunct / ర-vattu",
    "other": "ఛందస్సు కోసం మరో గురులఘు పఠనం · read with the other weight for the meter",
}
GURU_RULE_TE = {
    "deergha": "దీర్ఘము", "sandhyakshara": "సంధ్యక్షరము", "anusvara": "అనుస్వారము", "visarga": "విసర్గ",
    "pollu": "పొల్లు", "samyukta": "సంయుక్తాక్షర పూర్వము", "laghu": "లఘువు",
}


@dataclass(frozen=True)
class Poem:
    raw: dict

    @property
    def id(self) -> str:
        return self.raw["id"]

    @property
    def meter(self) -> str:
        return self.raw["meter"]

    @property
    def meter_te(self) -> str:
        return self.raw["meter_te"]

    @property
    def meters(self) -> list[str]:
        return self.raw["meters"]

    @property
    def lines(self) -> list[list[dict]]:
        return self.raw["lines"]

    @property
    def units(self) -> list[dict]:
        return self.raw["units"]

    @property
    def bhavam(self) -> Optional[dict]:
        return self.raw.get("bhavam")

    @property
    def has_bhavam(self) -> bool:
        b = self.bhavam
        return bool(b and (b.get("te") or b.get("en")))

    @property
    def prasa_applicable(self) -> bool:
        return bool(self.raw.get("prasa_applicable"))

    @property
    def hidden(self) -> dict:
        """Source metadata: for the admin export only, never rendered for annotators."""
        return self.raw["hidden"]

    @property
    def plain_lines(self) -> list[str]:
        return ["".join(t["t"] for t in line) for line in self.lines]


class PoemStore:
    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        payload = json.loads((self.data_dir / "poems.json").read_text(encoding="utf-8"))
        self.meta = {k: v for k, v in payload.items() if k != "poems"}
        self.poems = [Poem(p) for p in payload["poems"]]
        self.by_id = {p.id: p for p in self.poems}
        if len(self.by_id) != len(self.poems):
            raise ValueError("duplicate poem ids in poems.json")
        self.ids = [p.id for p in self.poems]

    def __len__(self) -> int:
        return len(self.poems)

    def __contains__(self, eval_id: str) -> bool:
        return eval_id in self.by_id

    def get(self, eval_id: str) -> Optional[Poem]:
        return self.by_id.get(eval_id)

    @cached_property
    def reference(self) -> dict:
        return json.loads((self.data_dir / "reference.json").read_text(encoding="utf-8"))

    def meter_cards(self, poem: Optional[Poem]) -> list[dict]:
        """Reference cards for the meter(s) of a poem (all cards when ``poem`` is None)."""
        cards = self.reference["meters"]
        if poem is None:
            return list(cards.values())
        return [cards[m] for m in poem.meters if m in cards]

    @property
    def fingerprint(self) -> str:
        """Identifies the poem set a database belongs to."""
        return f"{self.meta.get('dataset')}/{self.meta.get('pool')}/{len(self.poems)}"


_CACHE: dict[str, PoemStore] = {}


def load_store(data_dir: Path) -> PoemStore:
    key = str(Path(data_dir).resolve())
    if key not in _CACHE:
        _CACHE[key] = PoemStore(Path(data_dir))
    return _CACHE[key]
