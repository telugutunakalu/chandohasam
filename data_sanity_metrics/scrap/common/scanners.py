"""Two independent chandas scanners behind one interface.

    paper_verdict(poem)      the paper's own dwipada_analyser.py (IndicNeuroSym repo):
                             the scanner that *built* the corpus (Level 1 inclusion rule)
    chandohasam_verdict(...) this repo's meter_engine/chandohasam with the metre
                             forced to dvipada: an independent re-implementation

Both return the same per-rule dict so Level 1 can compare them rule by rule:
    gana     both lines admit an Indra^3 . Surya partition within 11–15 aksharas
    prasa    second-akshara consonant rhyme across the two lines
    yati_l1, yati_l2   foot-1 / foot-3 yati maitri per line
    valid    all of the above
"""
import sys

import config

_paper = None
_chandohasam = None


def _paper_module():
    global _paper
    if _paper is None:
        sys.path.insert(0, str(config.INDICNEUROSYM_REPO))
        import dwipada_analyser  # noqa: E402  (the paper's scanner)
        _paper = dwipada_analyser
    return _paper


def _chandohasam_module():
    global _chandohasam
    if _chandohasam is None:
        sys.path.insert(0, str(config.METER_ENGINE_DIR))
        import chandohasam  # noqa: E402
        _chandohasam = chandohasam
    return _chandohasam


def paper_verdict(poem: str) -> dict:
    try:
        r = _paper_module().analyze_dwipada(poem)
    except ValueError as e:
        return {"error": str(e), "valid": False}
    s = r["validation_summary"]
    yati = [r["yati_line1"], r["yati_line2"]]
    return {
        "gana": bool(s["gana_sequence_line1"] and s["gana_sequence_line2"]
                     and s["syllable_length_line1_in_range"] and s["syllable_length_line2_in_range"]),
        "prasa": bool(s["prasa_match"]),
        "yati_l1": s["yati_line1_match"] is not False,
        "yati_l2": s["yati_line2_match"] is not False,
        "yati_rule": [y.get("match_type") if y else None for y in yati],
        "syllables": [s["syllable_count_line1"], s["syllable_count_line2"]],
        "valid": bool(r["is_valid_dwipada"]),
    }


def chandohasam_verdict(poem: str, profiles=("strict", "relaxed")) -> dict:
    """Identification (the slow step) runs once and is reused across profiles."""
    ch = _chandohasam_module()
    from indic_meter_dawg import identify_text
    ident = identify_text(poem)
    is_dvipada = any(c.meter == "dvipada" for c in ident.candidates)
    out = {"gana": is_dvipada, "candidates": [c.label for c in ident.candidates]}
    for prof in profiles:
        if not is_dvipada:
            out[prof] = {"prasa": None, "yati_l1": None, "yati_l2": None, "valid": False}
            continue
        a = ch.analyze(poem, profile=prof, meter="dvipada", identification=ident)
        unit = a.units[0]
        lines = unit.lines
        out[prof] = {
            "prasa": unit.prasa_matched,
            "yati_l1": lines[0].yati_matched if len(lines) > 0 else None,
            "yati_l2": lines[1].yati_matched if len(lines) > 1 else None,
            "yati_rules": [[s.rule for s in l.yati] for l in lines],
            "valid": a.matched and a.meter == "dvipada",
        }
    return out
