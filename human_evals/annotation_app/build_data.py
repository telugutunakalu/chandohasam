#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Precompute everything the annotation app shows, so the app never runs the engine.

For every poem of a human-evaluation pool (default ``../human_eval_poems_strict.json``)
this runs ``meter_engine``'s ``chandohasam.analyze`` (the indic_meter_dawg DAG scanner,
then the prāsa and yati engines), using the pool's compliance profile and the pool's
meter label. It writes two files:

  data/poems.json      the gaṇa division, the guru/laghu reading of every akshara,
                       the yati and prāsa aksharas, the printed lines as akshara tokens,
                       the bhavam, and the source metadata. The app keeps the source
                       metadata on the server and never shows it to annotators.
  data/reference.json  the ruleset reference: one card per meter, the guru/laghu
                       rules, the gaṇa tables, and the yati and prāsa rules, all read
                       from the engine's own files.

Run from anywhere (paths are relative to this file):

    python3 build_data.py                    # strict pool (the default)
    python3 build_data.py --pool relaxed     # another pool

The script needs only PyYAML, the same as meter_engine. It stops with an error
whenever a poem fails to analyse or its aksharas do not line up with the printed text,
so a stale or broken data file is never written.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
from collections import Counter, OrderedDict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
HUMAN_EVALS = HERE.parent
ROOT = HUMAN_EVALS.parent
ENGINE = ROOT / "meter_engine"
DATA_OUT = HERE / "data"

ARDHABINDU = "ఁ"          # ఁ — the prāsa engine drops it, the scanner keeps it on the akshara
ZERO_WIDTH = {"​", "‌", "‍", "⁠", "﻿"}

# gaṇa classes named in meter_rules.yaml slots → the label shown under a gaṇa
CLASS_TE = {"indra": "ఇంద్ర", "surya": "సూర్య"}
CLASS_LONG_TE = {
    "indra": "ఇంద్ర గణము", "surya": "సూర్య గణము", "kanda": "కంద గణము (చతుర్మాత్ర)",
    "m3": "త్రిమాత్రా గణము", "m4": "చతుర్మాత్రా గణము", "m5": "పంచమాత్రా గణము",
}
SHORT_GANA = {"గురువు": "గ", "లఘువు": "ల"}     # one-akshara gaṇas, labelled as in the printed tables
FAMILY_TE = {"vrutta": "వృత్తము", "jati": "జాతి", "upajati": "ఉపజాతి"}
STATUS_TE = {
    "canonical": "ప్రామాణికం", "canonical_subtype": "ప్రామాణిక ఉపభేదం", "mandatory": "తప్పనిసరి",
    "accepted_relaxation": "సడలింపు", "orthographic_relaxation": "లిపి సడలింపు",
    "deprecated": "అప్రశస్తం", "forbidden": "నిషిద్ధం", "informational": "సమాచారం",
}


class BuildError(RuntimeError):
    """A poem could not be turned into display data; the build stops."""


def is_telugu(ch: str) -> bool:
    return "ఀ" <= ch <= "౿"


def nfd(s: str) -> str:
    return unicodedata.normalize("NFD", s)


def strip_ardhabindu(s: str) -> str:
    return s.replace(ARDHABINDU, "")


# -----------------------------------------------------------------------------
# 1. engine
# -----------------------------------------------------------------------------
def load_engine():
    """Import chandohasam and the DAWG catalogue from meter_engine."""
    if str(ENGINE) not in sys.path:
        sys.path.insert(0, str(ENGINE))
    from chandohasam import analyze                      # noqa: E402
    from indic_meter_dawg import load_catalogue          # noqa: E402
    from indic_meter_dawg import scansion                # noqa: E402
    return analyze, load_catalogue(), scansion


def engine_revision() -> str:
    """The commit meter_engine was last changed in, plus '-dirty' when it has local edits."""
    try:
        rev = subprocess.run(["git", "-C", str(ROOT), "log", "-1", "--format=%h", "--", "meter_engine"],
                             capture_output=True, text=True, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "meter_engine"],
                               capture_output=True, text=True, check=True).stdout.strip()
        return rev + ("-dirty" if dirty else "")
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


# -----------------------------------------------------------------------------
# 2. one poem → units → pādas → gaṇas → aksharas
# -----------------------------------------------------------------------------
def _reading_note(cell, reading: str, is_last: bool, padanta: bool) -> str:
    """Why the meter reads an akshara with the other weight ('' when it doesn't)."""
    if reading == cell.weight:
        return ""
    if is_last and padanta and cell.weight == "I" and reading == "U":
        return "padanta"
    return cell.vikalpa or "other"


def _slot_classes(spec, line_index: int, n_ganas: int) -> list[str]:
    """The gaṇa class of each position of a pāda (indra / surya …), '' where none applies."""
    if spec is None or not spec.slot_pattern:
        return [""] * n_ganas
    slot = spec.slot_pattern[line_index % len(spec.slot_pattern)]
    tokens = spec.slots.get(slot, ())
    if len(tokens) != n_ganas:
        return [""] * n_ganas
    return [t if t in CLASS_TE else "" for t in tokens]


def _prasa_index(line, seat) -> int:
    """1-based index of the prāsa akshara in the scanner's split (the 2nd, unless ఁ moved things)."""
    target = strip_ardhabindu(seat.prasa)
    if len(line.aksharas) >= 2 and strip_ardhabindu(line.aksharas[1].text) == target:
        return 2
    for cell in line.aksharas[:4]:
        if strip_ardhabindu(cell.text) == target:
            return cell.index
    raise BuildError(f"prāsa akshara {seat.prasa!r} not found in pāda {line.line_no}: {line.text!r}")


def unit_records(analysis, catalogue) -> list[dict]:
    """Display records for the metrical units of one analysed poem."""
    units = []
    for unit in analysis.units:
        try:
            spec = catalogue.get(unit.meter)
        except Exception:                      # noqa: BLE001 — a composite label has no spec of its own
            spec = None
        prasa_on = bool(unit.prasa and unit.prasa.applicable)
        seats = {s.line_no: s for s in (unit.prasa.seats if unit.prasa else [])}
        padas = []
        for k, line in enumerate(unit.lines):
            texts = {c.index: c.text for c in line.aksharas}
            # a prāsa-yati rhymes the akshara AFTER each seat, so show two aksharas per side (గిత్త – బుత్తి)
            yati_seats = [{"pos": list(s.positions),
                           "ak": [texts[q] + (texts.get(q + 1, "") if s.prasa_yati else "") for q in s.positions],
                           "rule": s.rule, "te": s.label_te, "ok": s.matched, "hyp": s.hypothesis, "py": s.prasa_yati}
                          for s in line.yati]
            yati_pos = {p for seat in yati_seats for p in seat["pos"]}
            prasa_idx = _prasa_index(line, seats[line.line_no]) if prasa_on and line.line_no in seats else None
            classes = _slot_classes(spec, k, len(line.ganas))
            n = len(line.aksharas)
            ganas = []
            for g, cls in zip(line.ganas, classes):
                if len(g.pattern) != len(g.aksharas):
                    raise BuildError(f"gaṇa {g.telugu} pattern {g.pattern} vs {len(g.aksharas)} aksharas")
                aks = []
                for cell, reading in zip(g.aksharas, g.pattern):
                    marks = ("y" if cell.index in yati_pos else "") + ("p" if cell.index == prasa_idx else "")
                    aks.append({
                        "i": cell.index, "t": cell.text, "w": reading, "cw": cell.weight,
                        "r": list(cell.rules), "alt": _reading_note(cell, reading, cell.index == n, line.padanta_laghu_as_guru),
                        "m": marks,
                    })
                ganas.append({"n": SHORT_GANA.get(g.telugu, g.telugu), "id": g.name, "pat": g.pattern, "cls": cls, "ak": aks})
            covered = sum(len(g["ak"]) for g in ganas)
            if covered != n:
                raise BuildError(f"gaṇas cover {covered} of {n} aksharas in pāda {line.line_no}: {line.text!r}")
            padas.append({
                "no": line.line_no, "text": line.text, "pattern": "".join(a["w"] for g in ganas for a in g["ak"]),
                "ganas": ganas, "yati": yati_seats, "prasa": prasa_idx, "padanta": line.padanta_laghu_as_guru,
                # the ✔ beside a pāda: its gaṇas fit the meter (the DAWG matched it) and every yati seat holds
                "ok": bool(line.ganas) and line.yati_matched,
            })
        units.append({"meter": unit.meter, "name_te": unit.name_te, "family": unit.family,
                      "prasa_applicable": prasa_on, "prasa_label": unit.prasa.label_te if prasa_on else None,
                      "padas": padas})
    return units


def display_lines(printed: list[str], units: list[dict]) -> list[list[dict]]:
    """The printed lines as tokens: aksharas (with their yati/prāsa marks) and the text between them.

    Every Telugu-block character belongs to exactly one akshara of the analysis, in order;
    everything else (spaces, punctuation, dashes) is kept verbatim as a separator, and
    zero-width characters stay inside the akshara they interrupt. Joining the tokens of a
    line gives back the printed line exactly.
    """
    return align(printed, units)[0]


def align(printed: list[str], units: list[dict]) -> tuple[list[list[dict]], dict]:
    """display_lines, plus where[(unit, pāda, akshara)] = the printed line the akshara is on."""
    cells = [((ui, pi, a["i"]), a) for ui, u in enumerate(units) for pi, p in enumerate(u["padas"])
             for g in p["ganas"] for a in g["ak"]]
    where: dict = {}
    it = iter(cells)
    key, cur = next(it, (None, None))
    out: list[list[dict]] = []
    raw, letters = "", ""
    for line in printed:
        toks: list[dict] = []
        for ch in line:
            if is_telugu(ch) or (ch in ZERO_WIDTH and letters):
                if cur is None:
                    raise BuildError(f"text left over after the last akshara: {line!r}")
                raw += ch
                if is_telugu(ch):
                    letters += ch
                # compare decomposed forms: the scanner NFC-normalises (ె + ౖ → ై), the printed text may not
                have, want = nfd(letters), nfd(cur["t"])
                if have == want:
                    toks.append({"t": raw, "c": cur["m"]} if cur["m"] else {"t": raw})
                    where[key] = len(out)
                    raw, letters = "", ""
                    key, cur = next(it, (None, None))
                elif not want.startswith(have):
                    raise BuildError(f"akshara {cur['t']!r} does not match the text {letters!r} in {line!r}")
            else:
                if letters:
                    raise BuildError(f"akshara {cur['t']!r} is split by {ch!r} in {line!r}")
                if toks and toks[-1].get("s"):
                    toks[-1]["t"] += ch
                else:
                    toks.append({"t": ch, "s": 1})
        if letters:
            raise BuildError(f"akshara {cur['t']!r} runs past the end of the line {line!r}")
        out.append(toks)
    if cur is not None:
        raise BuildError(f"akshara {cur['t']!r} and later ones were not found in the printed lines")
    return out, where


def line_notes(units: list[dict], where: dict, n_lines: int) -> list[dict]:
    """What to print beside each printed line: its prāsa akshara and the yati seats that start on it.

    A సీసము pāda spans two printed lines; each of its two yati seats goes beside the line its వళి is on.
    """
    notes = [{"prasa": None, "yati": [], "no_yati": False} for _ in range(n_lines)]
    for ui, u in enumerate(units):
        for pi, p in enumerate(u["padas"]):
            text = {a["i"]: a["t"] for g in p["ganas"] for a in g["ak"]}
            first = where[(ui, pi, 1)]
            if p["prasa"]:
                notes[where[(ui, pi, p["prasa"])]]["prasa"] = text[p["prasa"]]
            for seat in p["yati"]:
                notes[where[(ui, pi, seat["pos"][0])]]["yati"].append(seat)
            if not p["yati"]:
                notes[first]["no_yati"] = True
    return notes


# -----------------------------------------------------------------------------
# 3. bhavam (the meaning the poem is judged against in question 4)
# -----------------------------------------------------------------------------
def _text_key(lines: list[str]) -> str:
    return re.sub(r"[^ఀ-౿]", "", "".join(lines))


BACKFILL = DATA_OUT / "bhavam_padyarchana.json"     # written by backfill_bhavam.py
MANUAL = DATA_OUT / "bhavam_manual.json"            # written by hand, matched by the poem's lines


def load_bhavam_sources(backfill: bool = True) -> dict:
    """Index every corpus record that can carry a bhavam, the hand-written bhavams and the
    Padyarchana backfill."""
    by_id, by_text = {}, {}
    for name in ("bhagavatam", "vemana", "kuchimanchi_timmakavi", "chandassu"):
        path = ROOT / "dataset" / f"{name}.json"
        if not path.is_file():
            continue
        for rec in json.loads(path.read_text(encoding="utf-8")):
            by_id[rec["id"]] = rec
            if rec.get("verse"):
                by_text.setdefault(_text_key(rec["verse"]), rec)
    generated = {}
    gen_path = ROOT / "metrics" / "initial_evals" / "Outputs" / "chandas_dataset.json"
    if gen_path.is_file():
        generated = {p["id"]: p for p in json.loads(gen_path.read_text(encoding="utf-8"))["poems"]}
    filled = {}
    if backfill and BACKFILL.is_file():
        filled = json.loads(BACKFILL.read_text(encoding="utf-8"))["bhavams"]
    manual = {}
    if MANUAL.is_file():
        manual = {_text_key(b["lines"]): b for b in json.loads(MANUAL.read_text(encoding="utf-8"))["bhavams"]}
    return {"by_id": by_id, "by_text": by_text, "generated": generated, "backfill": filled, "manual": manual}


def _corpus_bhavam(rec: dict) -> dict | None:
    te, en = rec.get("bhavam"), rec.get("bhavam_en")
    src = "corpus_bhavam"
    if not te:
        gen = rec.get("generated") or {}
        te = gen.get("bhavam")
        src = f"llm_gloss:{gen.get('run', '?')}:{gen.get('model', '?')}" if te else None
    if not te and not en:
        return None
    return {"te": te or None, "en": en or None, "source": src or "llm_translation_only"}


def find_bhavam(poem: dict, sources: dict, overrides: dict) -> dict | None:
    if poem["eval_id"] in overrides:
        o = overrides[poem["eval_id"]]
        return {"te": o.get("te"), "en": o.get("en"), "source": o.get("source", "override")}
    if m := sources.get("manual", {}).get(_text_key(poem["lines"])):
        return {"te": m.get("te"), "en": m.get("en"), "source": m.get("source", "manual")}
    src = poem["source_dataset"]
    if src == "generated":
        g = sources["generated"].get(poem["source_id"])
        if g and (g.get("meaning_telugu") or g.get("meaning_english")):
            return {"te": g.get("meaning_telugu"), "en": g.get("meaning_english"), "source": "generation_meaning"}
        return None
    rec = sources["by_id"].get(poem["source_id"]) if src != "reference" else None
    if rec is None:
        rec = sources["by_text"].get(_text_key(poem["lines"]))
    found = _corpus_bhavam(rec) if rec else None
    if found is None and (b := sources.get("backfill", {}).get(_text_key(poem["lines"]))):
        return {"te": b["te"], "en": b.get("en"), "source": f"{b['source']}:{b['padyarchana_id']}"}
    return found


# -----------------------------------------------------------------------------
# 4. the ruleset reference
# -----------------------------------------------------------------------------
def _yati_text(spec) -> list[str]:
    """Plain-language yati position(s) of a meter, one string per distinct slot."""
    out = []
    slots = list(dict.fromkeys(spec.slot_pattern))
    for slot in slots:
        lines = [i + 1 for i, s in enumerate(spec.slot_pattern) if s == slot]
        where = "" if len(slots) == 1 else f"పాదాలు {', '.join(map(str, lines))}: "
        pos = spec.yati_for(slot)
        if not pos:
            out.append(where + "యతి లేదు")
        elif spec.name == "seesamu":
            out.append(where + "రెండు యతులు — 1వ గణం ↔ 3వ గణం, 5వ గణం ↔ 7వ గణం (మొదటి అక్షరాలు)")
        elif spec.is_fixed:
            out.append(where + "1వ అక్షరం ↔ " + ", ".join(f"{p}వ అక్షరం" for p in pos))
        else:
            out.append(where + "1వ గణం మొదటి అక్షరం ↔ " + ", ".join(f"{p}వ గణం మొదటి అక్షరం" for p in pos))
    return out


def _slot_rows(spec, registry) -> list[dict]:
    rows = []
    patterns = [spec.slot_pattern] + list(spec.alt_slot_patterns)
    for j, pattern in enumerate(patterns):
        for slot in dict.fromkeys(pattern):
            tokens = spec.slots.get(slot, ())
            lines = [i + 1 for i, s in enumerate(pattern) if s == slot]
            cells = []
            for tok in tokens:
                if tok in CLASS_LONG_TE:
                    cells.append({"t": CLASS_TE.get(tok) or CLASS_LONG_TE[tok].split()[0], "cls": tok})
                else:
                    try:
                        g = registry.get(tok)
                        cells.append({"t": tok, "pat": g.pattern})
                    except Exception:                  # noqa: BLE001
                        cells.append({"t": tok})
            rows.append({"slot": slot, "lines": lines, "alt": j > 0, "ganas": cells})
    return rows


def meter_card(spec, registry) -> dict:
    lo, hi = spec.aksharalu
    return {
        "name": spec.name, "name_te": spec.name_te, "family": spec.family,
        "family_te": FAMILY_TE.get(spec.family, spec.family), "padalu": spec.padalu,
        "system": spec.system, "aksharalu": [lo, hi], "ganalu_text": spec.ganalu_text,
        "slots": _slot_rows(spec, registry), "yati": _yati_text(spec),
        "prasa": spec.prasa, "prasa_yati": spec.prasa_yati, "halves_per_line": spec.halves_per_line,
        "followed_by": list(spec.followed_by), "repeatable": spec.repeatable,
        "constraints": [c.why for c in spec.constraints if c.why] + [c.why for c in spec.stanza_constraints if c.why],
        "notes": spec.notes,
    }


def _parse_compact(path: Path) -> dict[str, dict]:
    """yathi_compact.md: one rule per line, `- id=X | key=value | …`."""
    rules = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("- id="):
            continue
        fields = OrderedDict()
        for part in line[2:].split(" | "):
            if "=" in part:
                k, v = part.split("=", 1)
                fields[k.strip()] = v.strip()
        rules[fields["id"]] = fields
    return rules


def _guru_rules(scansion) -> list[dict]:
    """The scanner's guru rules, read from the table in its module docstring."""
    rows = []
    for line in (scansion.__doc__ or "").splitlines():
        cols = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cols) == 3 and cols[0] in scansion.RULE_NAMES:
            rows.append({"id": cols[0], "te": cols[1], "when": cols[2]})
    return rows


YATI_FAMILIES = [
    ("POS", "యతిస్థానములు", "positions"), ("MOD", "సంధి చిహ్నాలు (ఁ ం ః న్)", "signs at the junction"),
    ("SV", "స్వర యతులు", "vowel yatis"), ("VY", "వ్యంజన యతులు", "consonant yatis"),
    ("SY", "సంయుక్త యతులు", "conjunct yatis"), ("SP", "విశేష వ్యంజన యతులు", "special consonant yatis"),
    ("UB", "ఉభయ యతులు", "ubhaya yatis"), ("PY", "ప్రాస యతి", "prāsa-yati"),
    ("DL", "తరువాతి / వ్యుత్పన్న యతులు", "derived and late yatis"), ("RJ", "నిషిద్ధ యతులు", "rejected yatis"),
]


def build_reference(meters: list[str], catalogue, scansion) -> dict:
    import yaml
    from indic_meter_dawg.ganas import load_registry
    registry = load_registry()

    ganas_yaml = yaml.safe_load((ENGINE / "ganas.yaml").read_text(encoding="utf-8"))
    gana_tables = []
    for key in ("ekakshara_ganas", "dvyakshara_ganas", "trika_ganas"):
        block = ganas_yaml.get(key) or {}
        gana_tables.append({"key": key, "description": block.get("description", ""), "ganas": block.get("ganas", [])})
    for key, block in (ganas_yaml.get("upaganas") or {}).items():
        if isinstance(block, dict) and "ganas" in block:
            gana_tables.append({"key": key, "description": block.get("description", ""), "ganas": block["ganas"]})
    kanda = ganas_yaml.get("kanda_ganas")
    if kanda:
        gana_tables.append({"key": "kanda_ganas", "description": kanda.get("description", ""), "ganas": kanda["ganas"]})

    y = yaml.safe_load((ENGINE / "yati_rules.yaml").read_text(encoding="utf-8"))
    compact = _parse_compact(ENGINE / "yathi_docs" / "yathi_compact.md")
    yati_rule_names = {r["id"]: r for r in y["rules"]}
    maitri = []
    groups: dict[str, list[list[str]]] = OrderedDict()
    for pair in y["maitri_table"]["pairs"]:
        groups.setdefault(pair["rule"], []).append(pair["consonants"])
    vargaja = y["maitri_table"]["vargaja_rule"]
    maitri.append({"rule": vargaja, "pairs": [], "vargas": [v["members"][:4] for v in y["alphabet"]["vargas"]]})
    for rule, pairs in groups.items():
        maitri.append({"rule": rule, "pairs": pairs})
    for row in y.get("conditional_pairs", []):
        maitri.append({"rule": row["rule"], "pairs": [row["consonants"]], "note": f"అచ్చులు రెండూ {row['vowel_class']}-వర్గం"})
    for row in maitri:
        r = yati_rule_names.get(row["rule"], {})
        c = compact.get(row["rule"], {})
        row.update({"te": (r.get("names") or {}).get("te") or c.get("name", ""),
                    "en": (r.get("names") or {}).get("en", ""),
                    "status": r.get("status") or c.get("status", "")})

    yati_families = []
    for code, te, en in YATI_FAMILIES:
        rows = [{"id": rid, "name": f.get("name", ""), "status": f.get("status", ""), "when": f.get("when", ""),
                 "match": f.get("match", ""), "scope": f.get("scope", "")}
                for rid, f in compact.items() if rid.split("-")[1] == code]
        if rows:
            yati_families.append({"code": code, "te": te, "en": en, "rules": rows})

    p = yaml.safe_load((ENGINE / "prasa_rules.yaml").read_text(encoding="utf-8"))
    prasa_rules = [{"id": r["id"], "te": r["names"].get("te", ""), "en": r["names"].get("en", ""),
                    "status": r["status"], "statement": " ".join((r.get("statement") or "").split())}
                   for r in p["rules"]]

    cards = OrderedDict()
    for name in sorted(meters, key=lambda n: catalogue.get(n).id):
        cards[name] = meter_card(catalogue.get(name), registry)
    return {
        "meters": cards,
        "guru_rules": _guru_rules(scansion),
        "gana_tables": gana_tables,
        "class_names": CLASS_LONG_TE,
        "yati": {
            "vowel_classes": y["alphabet"]["vowel_classes"],
            "vargas": [{"name": v["name"], "members": v["members"]} for v in y["alphabet"]["vargas"]],
            "maitri": maitri,
            "profiles": {k: {"te": v.get("label_te"), "en": v.get("label_en"), "accepts": v.get("accepted_statuses")}
                         for k, v in y["profiles"].items()},
            "families": yati_families,
        },
        "prasa": {
            "profiles": {k: {"te": v.get("label_te"), "en": v.get("label_en"), "accepts": v.get("accepted_statuses")}
                         for k, v in p["profiles"].items()},
            "rules": prasa_rules,
        },
        "status_te": STATUS_TE,
    }


# -----------------------------------------------------------------------------
# 5. main
# -----------------------------------------------------------------------------
def build_poem(poem: dict, profile: str, analyze, catalogue, sources: dict, overrides: dict) -> dict:
    text = "\n".join(poem["lines"])
    analysis = analyze(text, profile=profile, meter=poem["meter_id"])
    if not analysis.identified or not analysis.units:
        raise BuildError(f"{poem['eval_id']}: meter_engine did not identify the poem")
    head = analysis.units[0].meter
    if head != poem["meter_id"]:
        raise BuildError(f"{poem['eval_id']}: engine read {head}, pool says {poem['meter_id']}")
    units = unit_records(analysis, catalogue)
    lines, where = align(poem["lines"], units)
    return {
        "id": poem["eval_id"],
        "meter": analysis.meter,
        "meter_te": " + ".join(u["name_te"] for u in units),
        "meters": [u["meter"] for u in units],
        "prasa_applicable": any(u["prasa_applicable"] for u in units),
        "lines": lines,
        "notes": line_notes(units, where, len(lines)),
        "prasa_summary": [{"label": u["prasa_label"],
                           "ak": [next(a["t"] for g in p["ganas"] for a in g["ak"] if a["i"] == p["prasa"])
                                  for p in u["padas"] if p["prasa"]]}
                          for u in units if u["prasa_applicable"]],
        "units": units,
        "bhavam": find_bhavam(poem, sources, overrides),
        "hidden": {
            "source_dataset": poem["source_dataset"], "source_id": poem["source_id"], "author": poem["author"],
            "meter_id": poem["meter_id"], "meter_label_source": poem["meter_label_source"],
            "strictest_profile": poem["strictest_profile"], "engine_matched": analysis.matched,
            "metadata": poem.get("metadata") or {},
        },
    }


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--pool", default="strict", choices=["strict", "relaxed", "historical"],
                    help="which human_eval_poems_<pool>.json to annotate (default: strict)")
    ap.add_argument("--out", type=Path, default=DATA_OUT)
    ap.add_argument("--overrides", type=Path, default=DATA_OUT / "bhavam_overrides.json",
                    help="optional {eval_id: {te, en, source}} bhavams that replace or fill the corpus ones")
    args = ap.parse_args(argv)

    pool_path = HUMAN_EVALS / f"human_eval_poems_{args.pool}.json"
    pool = json.loads(pool_path.read_text(encoding="utf-8"))
    profile = pool["compliance_profile"]
    analyze, catalogue, scansion = load_engine()
    sources = load_bhavam_sources()
    overrides = json.loads(args.overrides.read_text(encoding="utf-8")) if args.overrides.is_file() else {}

    poems, errors = [], []
    for poem in pool["poems"]:
        try:
            poems.append(build_poem(poem, profile, analyze, catalogue, sources, overrides))
        except BuildError as exc:
            errors.append(str(exc))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"{len(errors)} poem(s) failed; nothing written.", file=sys.stderr)
        return 1

    meters = sorted({m for p in poems for m in p["meters"]})
    reference = build_reference(meters, catalogue, scansion)
    meta = {
        "dataset": pool["dataset"], "pool": args.pool, "pool_file": pool_path.name,
        "compliance_profile": profile, "built_on": date.today().isoformat(),
        "engine": "meter_engine/chandohasam.analyze (indic_meter_dawg + prasa + yati)",
        "engine_revision": engine_revision(), "n_poems": len(poems),
    }
    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "poems.json").open("w", encoding="utf-8") as fh:
        json.dump({**meta, "poems": poems}, fh, ensure_ascii=False, separators=(",", ":"))
    with (args.out / "reference.json").open("w", encoding="utf-8") as fh:
        json.dump({**meta, **reference}, fh, ensure_ascii=False, indent=1)

    bh = Counter((p["bhavam"] or {}).get("source", "none").split(":")[0] for p in poems)
    src = Counter(p["hidden"]["source_dataset"] for p in poems)
    print(f"wrote {len(poems)} poems ({args.pool} pool, profile {profile}) to {args.out}")
    print("  sources: " + ", ".join(f"{k} {v}" for k, v in src.most_common()))
    print("  bhavam:  " + ", ".join(f"{k} {v}" for k, v in bh.most_common()))
    print(f"  meters:  {len(meters)}; reference cards: {len(reference['meters'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
