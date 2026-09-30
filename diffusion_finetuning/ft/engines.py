"""The engine verdict on a finished poem (the arbiter for reranking and evaluation)."""
from __future__ import annotations

from .metres import identify


def verdict(lines: list[str], label: str) -> dict:
    """metre_ok: the engine identifies the requested metre (main unit; an ettugīti must parse too);
    prāsa / yati under the relaxed and strict profiles (False when the metre is not identified)."""
    from chandohasam.analysis import analyze
    from indic_meter_dawg import identify_text

    from .metres import dawg
    out = {"metre_ok": False, "identified_as": None, "prasa_relaxed": False, "yati_relaxed": False,
           "prasa_strict": False, "yati_strict": False}
    if not lines:
        return out
    main = label.split("+")[0]
    opt = identify(lines).pick(frozenset({main}))
    ident = identify(lines)
    out["identified_as"] = ident.options[0].label if ident.options else None
    if opt is None or ("+" in label and opt.label != label):
        return out
    out["metre_ok"] = True
    res = identify_text(lines, dawg())
    for profile in ("relaxed", "strict"):
        a = analyze(lines, profile=profile, meter=opt.label, identification=res)
        out[f"prasa_{profile}"], out[f"yati_{profile}"] = bool(a.prasa_matched), bool(a.yati_matched)
    return out
