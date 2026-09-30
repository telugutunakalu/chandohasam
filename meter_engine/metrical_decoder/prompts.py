# -*- coding: utf-8 -*-
"""
The prompt: the rules of one meter, a topic, and the output format.

The same messages go to the baseline and to the three constrained
strategies, so every mode sees one prompt and the modes differ only in
decoding. The rules are generated from ``meter_rules.yaml`` through the
grammars (``slot_alternatives`` applies the meter's positional constraints),
so they state exactly what the enforcer and the verifier check.

Owns: :data:`TOPICS`, :func:`meter_rules`, :func:`build_messages`. Must not
import torch.
"""
from __future__ import annotations

from typing import Optional

from .incremental import ENGINE_DIR  # noqa: F401  (puts meter_engine on sys.path)
from .enforcer import line_lengths

from indic_meter_dawg import default_dawg                     # noqa: E402
from indic_meter_dawg.grammar import slot_alternatives        # noqa: E402

# the three topics of the IndicNeuroSym benchmark (paper §8, T1–T3)
TOPICS: dict[str, str] = {
    "T1": "తల్లి ప్రేమ అన్నింటికంటే గొప్పది",
    "T2": "హనుమంతుడు సముద్రమును దాటి లంకను చేరెను",
    "T3": "శ్రీరాముడు సీతాదేవిని రక్షించుటకు లంకకు వెళ్ళెను",
}

SYSTEM = ("You are a master of classical Telugu poetry (పద్య కవిత్వము). You compose padyams that follow "
          "chandassu exactly: the gaṇa sequence of every line, yati and prāsa.")

GURU_LAGHU = ("Guru (U) and laghu (I): an akshara is guru when it has a long vowel (ఆ ఈ ఊ ౠ ఏ ఓ), a diphthong "
              "(ఐ ఔ), an anusvāra (ం) or a visarga (ః), when it ends in a pollu (a dead consonant, e.g. న్), or when "
              "the next akshara of the same word begins with a conjunct or doubled consonant (e.g. the స of సత్యము). "
              "Every other akshara is laghu.")

FAMILY_EN = {"vritta": "a vṛtta (fixed gaṇa sequence)", "jati": "a jāti meter", "upajati": "an upajāti meter",
             "ragada": "a ragaḍa (mātrā) meter"}


def _ordinal(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def _choice(ganas) -> str:
    return " or ".join(f"{g.telugu} ({g.pattern})" for g in ganas)


def _slot_lines(spec, slot: str, registry) -> list[str]:
    alts = slot_alternatives(spec, slot, registry)
    lo, hi = line_lengths(spec.name, slot)
    size = f"{lo} aksharas" if lo == hi else f"{lo} to {hi} aksharas"
    if all(len(a) == 1 for a in alts):
        names = " ".join(a[0].telugu for a in alts)
        pattern = " ".join(a[0].pattern for a in alts)
        return [f"{len(alts)} gaṇas: {names}, i.e. {pattern} ({size})"]
    out = [f"{len(alts)} gaṇas ({size}):"]
    for k, a in enumerate(alts, start=1):
        out.append(f"  gaṇa {k}: {_choice(a)}")
    return out


def _line_numbers(pattern: tuple[str, ...], slot: str) -> str:
    idx = [str(i + 1) for i, s in enumerate(pattern) if s == slot]
    return ("Line " + idx[0]) if len(idx) == 1 else "Lines " + ", ".join(idx[:-1]) + " and " + idx[-1]


def _lines_label(spec, slot: str, pattern: tuple[str, ...]) -> str:
    if len(set(pattern)) == 1:
        return "Every line"
    return _line_numbers(pattern, slot)


def _yati(spec) -> str:
    if spec.is_fixed:
        ys = spec.yati_aksharas.get("all", ())
        if not ys:
            return "Yati (యతి): none."
        where = " and ".join(f"the {_ordinal(y)}" for y in ys)
        text = f"Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with {where} akshara."
    else:
        rules = {slot: tuple(ys) for slot, ys in spec.yati_ganas.items() if ys}
        uniform = len(set(rules.values())) == 1 and len(rules) == len(spec.slots)
        parts = []
        for slot, ys in rules.items():
            label = "every line" if uniform else _line_numbers(spec.slot_pattern, slot).lower()
            if spec.name == "seesamu":
                parts.append(f"in {label} the 1st akshara must be in yati-maitri with the first akshara of gaṇa 3, "
                             f"and the first akshara of gaṇa 5 with the first akshara of gaṇa 7")
            else:
                parts.append(f"in {label} the 1st akshara must be in yati-maitri with the first akshara of gaṇa "
                             + " and of gaṇa ".join(str(y) for y in ys))
            if uniform:
                break
        text = "Yati (యతి): " + "; ".join(parts) + "." if parts else "Yati (యతి): none."
    if spec.prasa_yati:
        text += " Prāsa-yati may take the place of yati."
    return text


def _prasa(spec) -> str:
    if not spec.prasa:
        return "Prāsa (ప్రాస): not required."
    return ("Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara "
            "must have the same weight (guru or laghu) in every line.")


def n_lines(meter: str, units: int = 1) -> int:
    spec = default_dawg().spec(meter)
    return len(spec.slot_pattern) * (units if spec.repeatable else 1)


def meter_rules(meter: str, units: int = 1) -> str:
    """The rules of a meter in plain words, generated from the catalogue.

    >>> print(meter_rules("utpalamala").splitlines()[2])
    Every line: 7 gaṇas: భ ర న భ భ ర వ, i.e. UII UIU III UII UII UIU IU (20 aksharas)
    """
    dawg = default_dawg()
    spec = dawg.spec(meter)
    reg = dawg.registry
    lines = n_lines(meter, units)
    family = FAMILY_EN.get(spec.family, f"a {spec.family} meter")
    out = [f"Meter: {spec.name_te.replace('_', ' ')} ({spec.name}), {family}.",
           f"Lines (పాదాలు): {lines}."]
    for j, pattern in enumerate(spec.slot_patterns):
        if j:
            out.append("Alternatively, every line in the all-laghu form:")
        for slot in dict.fromkeys(pattern):
            body = _slot_lines(spec, slot, reg)
            out.append(f"{_lines_label(spec, slot, pattern)}: {body[0]}")
            out.extend(body[1:])
    for c in spec.stanza_constraints:
        if c.rule == "first_akshara_weight_uniform":
            out.append("The 1st akshara of every line has the same weight: all guru or all laghu.")
    out.append(_yati(spec))
    out.append(_prasa(spec))
    out.append(GURU_LAGHU)
    return "\n".join(out)


def build_messages(meter: str, topic: str, units: int = 1, with_example: bool = False) -> list[dict]:
    """System and user messages for one (meter, topic)."""
    spec = default_dawg().spec(meter)
    lines = n_lines(meter, units)
    user = [f"Write a Telugu padyam in the meter {spec.name_te.replace('_', ' ')} ({spec.name}).", "", meter_rules(meter, units), ""]
    if with_example and spec.udaharana:
        user += [f"Example lines of {spec.name_te}: {spec.udaharana}", ""]
    user += [f"Topic (విషయము): {topic}", "",
             f"Write only the {lines} lines of the poem in Telugu script, one pāda per line. "
             f"No title, no numbering, no transliteration, no explanation."]
    return [{"role": "system", "content": SYSTEM}, {"role": "user", "content": "\n".join(user)}]


def topic_items(spec: Optional[str]) -> list[tuple[str, str]]:
    """``None``/``"default"`` → the three benchmark topics; ``"T1,T3"`` → those; other text → one custom topic."""
    if spec in (None, "", "default"):
        return list(TOPICS.items())
    keys = [k.strip() for k in spec.split(",")]
    if all(k in TOPICS for k in keys):
        return [(k, TOPICS[k]) for k in keys]
    return [("custom", spec)]
