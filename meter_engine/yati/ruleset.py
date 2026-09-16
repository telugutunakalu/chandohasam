# -*- coding: utf-8 -*-
"""The yati ruleset: an in-memory view of ``yati_rules.yaml``.

``Ruleset`` keeps the vowel classes, the consonant lookup tables, the bindu
table, the vowel bridges, the sandhi readings, the ubhaya triggers and the
rule catalogue, plus small helpers (status of a rule, is it accepted under a
profile, the least permissive profile that accepts it).
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml

from .constants import DEFAULT_RULES_PATH, NEVER_ACCEPTED, PROFILE_ORDER


class Ruleset:
    """In-memory view of yati_rules.yaml with the lookups the engine needs."""

    def __init__(self, data: dict, path: Optional[Path] = None):
        self.data = data
        self.path = path
        self.profile_order: list[str] = list(data.get("profile_order", PROFILE_ORDER))
        self.profiles: dict[str, set[str]] = {k: set(v["accepted_statuses"]) for k, v in data["profiles"].items()}
        self.rules: dict[str, dict] = {r["id"]: r for r in data["rules"]}
        al = data["alphabet"]
        self.vowel_class: dict[str, str] = {}
        for cls, vs in al["vowel_classes"].items():
            for v in vs:
                self.vowel_class[v] = cls
        self.matras: dict[str, str] = dict(al["matras"])
        self.consonants: list[str] = list(al["consonants"])
        self.dantya: dict[str, str] = dict(al.get("dantya_map", {}))
        self.vargas: dict[str, list[str]] = {v["name"]: list(v["members"]) for v in al["vargas"]}
        self.varga_of: dict[str, str] = {c: v["name"] for v in al["vargas"] for c in v["members"]}
        cl = al["classes"]
        self.stops = set(cl["stops"])
        self.nasals = set(cl["nasal"])
        self.mavarna_hosts = set(cl["mavarna_hosts"])
        mt = data["maitri_table"]
        self.identity_rule = mt["identity_rule"]
        self.default_rule = mt["default_rule"]
        self.vargaja_rule = mt["vargaja_rule"]
        self.stop_nasal_rule = mt["stop_nasal_without_bindu_rule"]
        self.pairs: dict[frozenset, str] = {}
        for p in mt["pairs"]:
            key = frozenset(p["consonants"])
            if key in self.pairs and self.pairs[key] != p["rule"]:
                raise ValueError(f"maitri_table lists {sorted(key)} twice")
            self.pairs[key] = p["rule"]
        self.conditional: list[dict] = list(data.get("conditional_pairs", []))
        self.bindu_table: list[dict] = list(data.get("bindu_table", []))
        self.cluster_units: list[dict] = list(data.get("cluster_unit_table", []))
        self.vowel_bridges: list[dict] = list(data.get("vowel_bridges", []))
        self.detachable: dict[str, dict] = dict(data.get("detachable_vowels", {}))
        self.sandhi_readings: dict[str, list] = dict(data.get("sandhi_readings", {}))
        self.ubhaya: dict = data.get("ubhaya_triggers", {})
        self.blockers: list[dict] = list(data.get("blockers", []))
        self.examples: list[dict] = list(data.get("attested_examples", []))

    # --- helpers ---------------------------------------------------------------
    def rule(self, rid: str) -> dict:
        return self.rules[rid]

    def status(self, rid: str) -> str:
        return self.rules[rid]["status"]

    def name(self, rid: str, lang: str = "en") -> str:
        names = self.rules[rid]["names"]
        return names.get(lang) or names["en"]

    def label(self, rid: str) -> str:
        r = self.rules[rid]
        return r.get("label", {}).get("te") or r["names"].get("te") or r["names"]["en"]

    def accepted(self, profile: str, status: str) -> bool:
        return status in self.profiles[profile]

    def min_profile(self, status: str) -> Optional[str]:
        if status in NEVER_ACCEPTED:
            return None
        for p in self.profile_order:
            if status in self.profiles[p]:
                return p
        return None

    def vclass(self, v: str) -> Optional[str]:
        return self.vowel_class.get(v)

    def norm_c(self, c: str) -> str:
        return self.dantya.get(c, c)

    def is_positive(self, rid: str) -> bool:
        return self.status(rid) not in NEVER_ACCEPTED and self.rules[rid]["kind"] != "reject"


def load_ruleset(path: Optional[str | Path] = None) -> Ruleset:
    p = Path(path) if path else DEFAULT_RULES_PATH
    with open(p, "r", encoding="utf-8") as fh:
        return Ruleset(yaml.safe_load(fh), p)


_DEFAULT_RS: Optional[Ruleset] = None


def _rs(ruleset: Optional[Ruleset]) -> Ruleset:
    global _DEFAULT_RS
    if ruleset is not None:
        return ruleset
    if _DEFAULT_RS is None:
        _DEFAULT_RS = load_ruleset()
    return _DEFAULT_RS
