# -*- coding: utf-8 -*-
"""
Per-line feature extraction: every property of a pāda that the prāsa rules refer to
(``LineFeatures``), and the optional druta-sandhi reading of the pre-prāsa akshara.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from .constants import ARDHABINDU, DANTYA_MAP, IGNORABLE
from .aksharanusarika_loader import load_aksharanusarika
from .akshara import intrinsic_weight, parse_akshara, render_onset, sanitize
from .ruleset import Ruleset


@dataclass
class LineFeatures:
    index: int
    raw: str
    sanitized: str
    tokens: list[str]
    weights: list[str]
    purva: str
    prasa: str
    third: Optional[str]
    space_between: bool
    ardhabindu_before: bool
    ardhabindu_after: bool
    purva_parts: dict
    prasa_parts: dict
    purva_purnabindu: bool
    purva_visarga: bool
    fused_from_purva: list[str]
    onset: list[str]
    onset_written: list[str]
    vowel: str
    bare_vowel: bool
    trailing_anusvara: bool
    trailing_visarga: bool
    trailing_pollu: list[str]
    dantya_forms: list[str]
    purva_weight_positional: str
    purva_weight_intrinsic: str
    prasa_weight: str
    repha_cluster: bool
    light_cluster_hint: Optional[str]
    laghu_ya_hint: bool
    prasa_word: str
    third_onset: list[str]
    reading: str = "as_written"
    error: Optional[str] = None

    @property
    def onset_text(self) -> str:
        return render_onset(self.onset)


def _bare(akshara: str) -> str:
    """ఁ has no metrical significance: an akshara with ఁ is the same akshara (రుఁ ≡ రు)."""
    return akshara.replace(ARDHABINDU, "")


def _word_around(tokens: list[str], idx: int) -> str:
    lo = idx
    while lo > 0 and tokens[lo - 1] != " ":
        lo -= 1
    hi = idx
    while hi + 1 < len(tokens) and tokens[hi + 1] != " ":
        hi += 1
    return _bare("".join(tokens[lo:hi + 1]))


def _too_short(text: str, index: int, clean: str, tokens: list[str], weights: list[str], core: list[int]) -> LineFeatures:
    """A pāda with fewer than two aksharas cannot carry a prāsa akshara (PRASA-POS-01)."""
    blank = dict(text="", onset=[], onset_raw=[], vowel="", bare_vowel=False, anusvara=False,
                 visarga=False, trailing_pollu=[], dantya=[])
    return LineFeatures(
        index=index, raw=text, sanitized=clean, tokens=tokens, weights=weights,
        purva=_bare(tokens[core[0]]) if core else "", prasa="", third=None, space_between=False,
        ardhabindu_before=False, ardhabindu_after=False, purva_parts=blank, prasa_parts=blank,
        purva_purnabindu=False, purva_visarga=False, fused_from_purva=[], onset=[], onset_written=[],
        vowel="", bare_vowel=False, trailing_anusvara=False, trailing_visarga=False, trailing_pollu=[],
        dantya_forms=[], purva_weight_positional="", purva_weight_intrinsic="", prasa_weight="",
        repha_cluster=False, light_cluster_hint=None, laghu_ya_hint=False, prasa_word="", third_onset=[],
        error="PRASA-POS-01: a pāda needs at least two aksharas to carry a prāsa akshara",
    )


def _light_cluster_hint(repha_cluster: bool, prasa_word: str, space_between: bool, fused: list[str],
                        ruleset: Ruleset) -> Optional[str]:
    """Heuristic for PRASA-PURVAKSHARA-04: a ర-conjunct that may be read LIGHT (Telugu
    krāravaḍi / laghudvitva) — a lexicon stem, or a word-initial cluster."""
    if not repha_cluster:
        return None
    if any(prasa_word.startswith(stem) for stem in ruleset.light_lexicon):
        return "lexicon"
    if space_between and not fused:
        return "word_initial_kraravadi"
    return None


def extract_line(text: str, index: int, ruleset: Ruleset, ak=None) -> LineFeatures:
    """Split one pāda and compute every feature the prāsa rules refer to.

    Implements PRASA-POS-01 (positions), PRASA-POS-06 (saṁśleṣa of a dead
    consonant on the pre-prāsa akshara), PRASA-POS-08 (dantya normalisation),
    PRASA-PURVAKSHARA-02 (positional vs intrinsic weight) and the heuristic
    hints for PRASA-PURVAKSHARA-04 and PRASA-SAMA-11.
    """
    ak = ak or load_aksharanusarika()
    clean = sanitize(text)
    tokens: list[str] = ak.split_aksharalu(clean) if clean else []
    weights: list[str] = ak.akshara_ganavibhajana(tokens) if tokens else []
    core = [i for i, t in enumerate(tokens) if t not in IGNORABLE]        # indices of real aksharas
    if len(core) < 2:
        return _too_short(text, index, clean, tokens, weights, core)
    i1, i2 = core[0], core[1]                       # pre-prāsa akshara, prāsa akshara
    i3 = core[2] if len(core) > 2 else None
    between = tokens[i1 + 1:i2]
    after = tokens[i2 + 1:i3] if i3 is not None else tokens[i2 + 1:]
    purva, prasa = _bare(tokens[i1]), _bare(tokens[i2])
    third = _bare(tokens[i3]) if i3 is not None else None
    purva_p = parse_akshara(purva)
    prasa_p = parse_akshara(prasa)
    third_p = parse_akshara(third) if third is not None else None
    fused = list(purva_p.trailing_pollu)             # a dead consonant on the pre-prāsa akshara joins the onset
    onset = [DANTYA_MAP.get(c, c) for c in fused] + list(prasa_p.onset)
    onset_written = list(fused) + list(prasa_p.onset_raw)
    repha_cluster = len(onset) == 2 and onset[1] == "ర"
    space_between = " " in between
    prasa_word = _word_around(tokens, i2)
    laghu_ya = (onset == ["య"] and space_between
                and not (purva_p.anusvara or purva_p.visarga or purva_p.trailing_pollu))
    return LineFeatures(
        index=index, raw=text, sanitized=clean, tokens=tokens, weights=weights,
        purva=purva, prasa=prasa, third=third,
        space_between=space_between,
        ardhabindu_before=ARDHABINDU in tokens[i1] or ARDHABINDU in between,   # ఁ is attached to its akshara
        ardhabindu_after=ARDHABINDU in tokens[i2] or ARDHABINDU in after,
        purva_parts=asdict(purva_p), prasa_parts=asdict(prasa_p),
        purva_purnabindu=purva_p.anusvara, purva_visarga=purva_p.visarga,
        fused_from_purva=fused, onset=onset, onset_written=onset_written,
        vowel=prasa_p.vowel, bare_vowel=prasa_p.bare_vowel and not fused,
        trailing_anusvara=prasa_p.anusvara, trailing_visarga=prasa_p.visarga,
        trailing_pollu=list(prasa_p.trailing_pollu), dantya_forms=list(prasa_p.dantya),
        purva_weight_positional=weights[i1] or intrinsic_weight(purva_p),
        purva_weight_intrinsic=intrinsic_weight(purva_p),
        prasa_weight=weights[i2] or intrinsic_weight(prasa_p),
        repha_cluster=repha_cluster,
        light_cluster_hint=_light_cluster_hint(repha_cluster, prasa_word, space_between, fused, ruleset),
        laghu_ya_hint=laghu_ya, prasa_word=prasa_word, third_onset=list(third_p.onset) if third_p else [],
    )


def druta_sandhi_reading(line: LineFeatures, ruleset: Ruleset) -> Optional[LineFeatures]:
    """PRASA-POS-07: 'Xన్ + parusha' read as 'Xం + sarala' (పుత్రున్ కని -> పుత్రుంగని).
    Returns a re-featured copy, or None when the pattern does not apply."""
    if line.fused_from_purva != ["న"] or len(line.onset) != 2:
        return None
    head = line.onset[1]
    if head not in ruleset.druta_sandhi_map and head not in ruleset.sarala:
        return None
    soft = ruleset.druta_sandhi_map.get(head, head)
    alt = LineFeatures(**{**asdict(line)})
    alt.purva_purnabindu = True
    alt.fused_from_purva = []
    alt.onset = [soft]
    alt.onset_written = [soft]
    alt.repha_cluster = False
    alt.light_cluster_hint = None
    alt.reading = "druta_sandhi"
    return alt
