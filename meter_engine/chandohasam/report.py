# -*- coding: utf-8 -*-
"""
Plain-text rendering of a :class:`~chandohasam.models.PadyaAnalysis`.

The layout, per pāda::

    pāda 1  UIIUIUIIIUIIUIIUIUIU   యతి 1-10: ఎ ↔ మె  YATI-SV-02 స్వరప్రధాన యతి
      భ   ర   న   భ   భ   ర   వ
      ఎవ్వ నిచే జనిం చు జ గ మె …
"""
from __future__ import annotations

from .models import LineReport, PadyaAnalysis, UnitReport


def _gana_table(line: LineReport) -> list[str]:
    """Two aligned rows: gaṇa letters over the aksharas that fill them."""
    heads, cells = [], []
    for g in line.ganas:
        text = " ".join(a.text for a in g.aksharas)
        marks = " ".join(a.weight for a in g.aksharas)
        width = max(len(text), len(marks), len(g.telugu) + 2)
        heads.append(f"{g.telugu:<{width}}")
        cells.append((f"{text:<{width}}", f"{marks:<{width}}"))
    return ["  " + " | ".join(heads),
            "  " + " | ".join(c[0] for c in cells),
            "  " + " | ".join(c[1] for c in cells)]


def _yati_lines(line: LineReport) -> list[str]:
    out = []
    for s in line.yati:
        pos = "-".join(str(p) for p in s.positions)
        pair = " ↔ ".join(s.aksharas)
        if s.matched:
            tag = f"{s.rule} {s.label_te}"
            if s.prasa_yati:
                tag += " (ప్రాసయతి)"
            if s.hypothesis:
                tag += " [sandhi hypothesis]"
            out.append(f"  యతి {pos}: {pair}  ✓ {tag}  — {s.detail}")
        else:
            extra = f" (would match under {s.min_profile})" if s.min_profile else ""
            out.append(f"  యతి {pos}: {pair}  ✗ {s.detail}{extra}")
        for v in s.violations:
            out.append(f"      {v}")
    return out


def _unit_text(u: UnitReport, k: int) -> list[str]:
    out = [f"── unit {k}: {u.name_te} ({u.meter}, {u.family}) ──"]
    for n in u.notes:
        out.append(f"  note: {n}")
    for v in u.violations:
        out.append(f"  stanza rule broken: {v}")
    for line in u.lines:
        out.append(f"pāda {line.line_no}: {line.text}")
        out.append(f"  {line.pattern}   గణాలు: {' '.join(line.gana_names)}"
                   + ("   (పాదాంత లఘువు → గురువు)" if line.padanta_laghu_as_guru else ""))
        out.extend(_gana_table(line))
        out.extend(_yati_lines(line))
    if u.prasa is None or not u.prasa.applicable:
        seats = ", ".join(s.prasa for s in u.prasa.seats) if u.prasa and u.prasa.seats else ""
        out.append("ప్రాస: not required by this metre" + (f" (second aksharas: {seats})" if seats else ""))
    else:
        p = u.prasa
        seats = ", ".join(f"{s.line_no}:{s.purva}·{s.prasa}" for s in p.seats)
        out.append(f"ప్రాస: {'✓' if p.matched else '✗'} {p.label_te} — consonant {p.consonant or '–'} — aksharas {seats}")
        for v in p.violations:
            out.append(f"  {v['rule']} {v.get('scope', '')}: {v['detail']}")
        if not p.matched and p.min_profile:
            out.append(f"  would match under profile {p.min_profile}")
    return out


def render_text(a: PadyaAnalysis) -> str:
    if not a.identified:
        out = ["metre: NOT IDENTIFIED"]
        out += [f"  {f['meter']} line {f['line_no']} akshara {f['akshara']}: {f['reason']}" for f in a.failures[:8]]
        return "\n".join(out)
    head = f"metre: {a.name_te} ({a.meter})" + ("  [ambiguous: " + ", ".join(a.candidates) + "]" if a.ambiguous else "")
    head += f"   ప్రాస {'✓' if a.prasa_matched else '✗'}   యతి {'✓' if a.yati_matched else '✗'}   profile {a.profile}, sandhi {a.yati_sandhi}"
    out = [head]
    for n in a.notes:
        out.append(f"note: {n}")
    for k, u in enumerate(a.units, 1):
        out.extend(_unit_text(u, k))
    return "\n".join(out)
