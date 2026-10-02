# -*- coding: utf-8 -*-
"""
The prāsa ruleset: an in-memory view of ``prasa_rules.yaml`` (profiles, alphabet, the consonant-pair
lookup table) plus the meter index of ``meter_rules.yaml``.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from .constants import DANTYA_MAP, DEFAULT_METER_RULES_PATH, DEFAULT_RULES_PATH, HERE, NEVER_ACCEPTED, PROFILE_ORDER


class Ruleset:
    """In-memory view of prasa_rules.yaml with the lookups the engine needs."""

    def __init__(self, data: dict, path: Optional[Path] = None):
        self.data = data
        self.path = path
        self.version = data.get("schema_version")
        self.rules: dict[str, dict] = {r["id"]: r for r in data["rules"]}
        self.rule_order: dict[str, int] = {r["id"]: i for i, r in enumerate(data["rules"])}
        self.profile_order: list[str] = list(data.get("profile_order", PROFILE_ORDER))
        self.profiles: dict[str, set[str]] = {
            name: set(p["accepted_statuses"]) for name, p in data["profiles"].items()
        }
        alphabet = data["alphabet"]
        self.consonants: list[str] = [c["letter"] for c in alphabet["consonants"]]
        self.consonant_info: dict[str, dict] = {c["letter"]: c for c in alphabet["consonants"]}
        classes = alphabet["classes"]
        self.parusha = set(classes["parusha"])
        self.sarala = set(classes["sarala"])
        self.nasals = set(classes["nasal"])
        self.vargas: dict[str, list[str]] = {v["name"]: list(v["members"]) for v in alphabet["vargas"]}
        self.druta_sandhi_map: dict[str, str] = dict(alphabet["druta_sandhi_map"])
        # vikalpa: class nasal (5th) <-> class voiced stop (3rd) of the same varga
        self.vikalpa_pairs = {frozenset((m[4], m[2])) for m in self.vargas.values()}
        mt = data["maitri_table"]
        self.maitri: dict[frozenset, str] = {}
        for pair in mt["pairs"]:
            key = frozenset(pair["consonants"])
            if key in self.maitri and self.maitri[key] != pair["rule"]:
                raise ValueError(f"maitri_table lists {sorted(key)} twice with different rules")
            self.maitri[key] = pair["rule"]
        self.maitri_default: str = mt["default_rule"]
        kk = self.rules["PRASA-PURVAKA-04A"]["condition"]
        self.khanda_ananta = set(kk["consonants"])
        self.light_lexicon: list[str] = list(data.get("light_repha_lexicon", {}).get("stems", []))
        self.examples: list[dict] = list(data.get("attested_examples", []))
        self.meter_eligibility: dict = data.get("meter_eligibility", {})

    # --- rule helpers ----------------------------------------------------------
    def rule(self, rule_id: str) -> dict:
        return self.rules[rule_id]

    def status(self, rule_id: str) -> str:
        return self.rules[rule_id]["status"]

    def name(self, rule_id: str, lang: str = "en") -> str:
        r = self.rules[rule_id]
        return r["names"].get(lang) or r["names"]["en"]

    def label(self, rule_id: str, lang: str = "te") -> str:
        r = self.rules[rule_id]
        return r.get("label", {}).get(lang) or self.name(rule_id, lang)

    def accepted(self, profile: str, status: str) -> bool:
        return status in self.profiles[profile]

    def min_profile(self, statuses) -> Optional[str]:
        statuses = set(statuses)
        if statuses & NEVER_ACCEPTED:
            return None
        for p in self.profile_order:
            if statuses <= self.profiles[p]:
                return p
        return None

    def lookup_pair_rule(self, x: str, y: str) -> str:
        x = DANTYA_MAP.get(x, x)
        y = DANTYA_MAP.get(y, y)
        if x == y:
            return "PRASA-SAMA-01"
        return self.maitri.get(frozenset((x, y)), self.maitri_default)

    def sort_rules(self, rule_ids) -> list[str]:
        seen: list[str] = []
        for r in sorted(set(rule_ids), key=lambda r: self.rule_order.get(r, 10_000)):
            seen.append(r)
        return seen


def load_ruleset(path: Optional[str | Path] = None) -> Ruleset:
    p = Path(path) if path else DEFAULT_RULES_PATH
    with open(p, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return Ruleset(data, p)


_DEFAULT_RS: Optional[Ruleset] = None


def _rs(ruleset: Optional[Ruleset]) -> Ruleset:
    """``ruleset``, or the default ruleset loaded once (parsing the YAML on every call is the slow part)."""
    global _DEFAULT_RS
    if ruleset is not None:
        return ruleset
    if _DEFAULT_RS is None:
        _DEFAULT_RS = load_ruleset()
    return _DEFAULT_RS


_METER_INDEX: Optional[dict] = None


def _meter_index() -> dict:
    """name / telugu name -> meter record from meter_rules.yaml + meters.txt (optional)."""
    global _METER_INDEX
    if _METER_INDEX is not None:
        return _METER_INDEX
    index: dict[str, dict] = {}
    if DEFAULT_METER_RULES_PATH.is_file():
        with open(DEFAULT_METER_RULES_PATH, "r", encoding="utf-8") as fh:
            mr = yaml.safe_load(fh)
        for m in mr.get("meters", []):
            index[m["name"]] = m
        meters_txt = HERE / "meters.txt"
        if meters_txt.is_file():
            with open(meters_txt, "r", encoding="utf-8") as fh:
                header = fh.readline().rstrip("\n").split("\t")
                for line in fh:
                    cols = line.rstrip("\n").split("\t")
                    row = dict(zip(header, cols))
                    rec = index.get(row.get("name", ""))
                    if rec is not None:
                        rec["name_te"] = row.get("name_in_telugu")
                        rec["type_of_chandassu"] = row.get("type_of_chandassu")
                        index[row["name_in_telugu"]] = rec
    _METER_INDEX = index
    return index
