# -*- coding: utf-8 -*-
"""
Prāsa and yati during decoding, checked jointly with the gaṇas and judged by the engines.

The automaton covers the gaṇas. Prāsa and yati depend on the sounds of
particular aksharas, and the prāsa and yati engines already decide them
(profiles, the pre-prāsa weight rule, saṁśleṣa, bindu and saṁyukta yati,
lexical readings, the prāsa-yati fallback, bahuyati). The decoder never
re-implements those rules: it asks the engines, on text.

Liveness has to be joint. The last one or two syllables of the unfinished
word are *pending*: their weights, and even their number, depend on what is
written next (``incremental.split_word``). :func:`continuations` splits those
possibilities into structural classes — the word's last syllable keeps its
onset, grows a conjunct, dies as a pollu, or splits at a trailing virama —
each with its weight strings and a descriptor of every pending syllable
(onset so far, vowel if written, whether marks may follow). For one class and
one weight string the gaṇa parse fixes where the yati aksharas fall
(:func:`line_groups`), and a pending yati akshara is feasible when *some*
realisation consistent with its weight (short vowels for a laghu, a bindu only
for a guru, one more consonant only when the onset can grow) matches its
vaḷi in the engine. A state is alive when some class and weight string pass
the automaton, prāsa and yati together.

Verdicts become final (:meth:`Registers.advance`) when the aksharas involved
are committed, and every line is re-verified whole when it ends
(:meth:`Registers.close_line`; the last line from ``Enforcer.line_complete``,
since it ends at EOS), with complete words, so what is emitted is exactly what
the engines accept (``strict`` profile, yati sandhi ``off``).

One known gap, on the safe side: pairs are judged during a line without the
words around them, so the ubhaya readings a whole word opens (-ఇంచు, ప్రాది
prefixes, deity names such as నారాయణ / మురారి: YATI-UB-*, VY-09/10) are not
used until the line ends. In the corpus this changes 46 of 21,874 yati pairs
(0.21%), always from fail to pass, so the decoder is at worst slightly stricter
than the engines; no word-context blocker changed a verdict.

Owns: :class:`Registers`, :func:`continuations`, :func:`line_groups`,
:func:`gana_starts`. Must not import torch.
"""
from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from .incremental import ENGINE_DIR, _open_cluster, sc, split_word  # noqa: F401  (ENGINE_DIR: sys.path)

import prasa as prasa_engine                                    # noqa: E402
import yati as yati_engine                                      # noqa: E402
from indic_meter_dawg import automaton as au                    # noqa: E402
from indic_meter_dawg import default_dawg                       # noqa: E402
from dataclasses import replace                                 # noqa: E402

NEUTRAL_TAIL = " క"          # closes a prāsa akshara for the prāsa engine without touching it
VIRAMA = sc.VIRAMA_CHAR
MATRA = {"అ": "", "ఆ": "ా", "ఇ": "ి", "ఈ": "ీ", "ఉ": "ు", "ఊ": "ూ", "ఋ": "ృ",
         "ఎ": "ె", "ఏ": "ే", "ఐ": "ై", "ఒ": "ొ", "ఓ": "ో", "ఔ": "ౌ"}
SHORT_VOWELS = ("అ", "ఇ", "ఉ", "ఋ", "ఎ", "ఒ")
ALL_VOWELS = tuple(MATRA)
REP_CONSONANTS = tuple("కచటతపరనమయహశసలవ")      # every yati maitri group, and ర ల వ య as second members


# ----------------------------------------------------------------------------
# where the yati aksharas of a line are
# ----------------------------------------------------------------------------
@lru_cache(maxsize=200_000)
def gana_starts(meter: str, slot: str, pattern: str) -> Optional[tuple[int, ...]]:
    """1-based first akshara of every gaṇa ``pattern`` has started (the next gaṇa
    counts as started when the pattern ends on a boundary); None when ``pattern``
    is not a prefix of the slot's language.

    >>> gana_starts("dvipada", "all", "UIIIIII")        # భ UII, then నల IIII: gaṇa 3 starts at akshara 8
    (1, 4, 8)
    """
    alts = default_dawg().grammars[(meter, slot)].gana_positions
    starts: list[int] = []
    pos = 0
    for choices in alts:
        rest = pattern[pos:]
        starts.append(pos + 1)
        done = next((g for g in choices if rest.startswith(g.pattern)), None)
        if done is not None:
            pos += len(done.pattern)
            continue
        if any(g.pattern.startswith(rest) for g in choices):
            return tuple(starts)
        return None
    return tuple(starts) if pos == len(pattern) else None


def _group_templates(spec, slot: str):
    """Yati groups of a slot as ``yati.plan_from_candidate`` forms them, positions
    relative to gaṇas (``("g", k)``) or aksharas (``("a", n)``)."""
    if spec.is_fixed:
        ys = list(spec.yati_aksharas.get(slot, ()))
        if not ys:
            return ()
        if not spec.prasa_yati and len(ys) > 1:
            return ((("a", 1),) + tuple(("a", y) for y in ys),)
        return tuple(((("a", 1), ("a", y)) for y in ys))
    yg = list(spec.yati_ganas.get(slot, ()))
    if not yg:
        return ()
    if spec.halves_per_line == 2 and len(yg) == 2 and len(spec.slots[slot]) >= 5:
        return ((("a", 1), ("g", yg[0])), (("g", 5), ("g", yg[1])))
    return tuple(((("a", 1), ("g", k)) for k in yg))


def _resolve(template, starts: tuple[int, ...]) -> Optional[tuple[int, ...]]:
    out = []
    for kind, n in template:
        if kind == "a":
            out.append(n)
        elif n - 1 < len(starts):
            out.append(starts[n - 1])
        else:
            return None
    return tuple(out)


@lru_cache(maxsize=10_000)
def slots_for(meter: str, done: tuple[str, ...]) -> tuple[str, ...]:
    """The slots the next line may take, given the weights of the lines written so far:
    a poem keeps one slot pattern (a సీసము is all 'all' lines or all 'laghu' lines).

    >>> slots_for("seesamu", ()), slots_for("seesamu", ("UII" * 6 + "UI" * 2,))
    (('all', 'laghu'), ('all',))
    """
    dawg = default_dawg()
    spec = dawg.spec(meter)
    unit = len(spec.slot_pattern)
    line = len(done)
    return tuple(dict.fromkeys(
        p[line % unit] for p in spec.slot_patterns
        if all(au.accepts(dawg.slot_dfas[(meter, p[i % unit])], pat) for i, pat in enumerate(done))))


def _slots(meter: str, line: int, slots: Optional[tuple[str, ...]]) -> tuple[str, ...]:
    if slots is not None:
        return slots
    spec = default_dawg().spec(meter)
    unit = len(spec.slot_pattern)
    return tuple(dict.fromkeys(p[line % unit] for p in spec.slot_patterns))


@lru_cache(maxsize=200_000)
def slot_groups(meter: str, line: int, pattern: str,
                slots: Optional[tuple[str, ...]] = None) -> tuple[tuple[Optional[tuple[int, ...]], ...], ...]:
    """The yati groups of line ``line`` under each slot (of ``slots``, default every slot of
    the line) that the weights ``pattern`` still fit, a group not placed yet being None.
    Liveness needs *some* slot whose groups can all be met: an all-laghu prefix is a whole
    'all' line of సీసము at 30 aksharas and six short of a 'laghu' line, and the two put the
    yati in different places.

    >>> slot_groups("seesamu", 0, "I" * 30)
    (((1, 9), (17, 25)), ((1, 11), (21, 31)))
    """
    spec = default_dawg().spec(meter)
    out = []
    for slot in _slots(meter, line, slots):
        starts = gana_starts(meter, slot, pattern)
        if starts is not None:
            out.append(tuple(_resolve(t, starts) for t in _group_templates(spec, slot)))
    return tuple(out)


@lru_cache(maxsize=200_000)
def line_groups(meter: str, line: int, pattern: str, complete: bool = False,
                slots: Optional[tuple[str, ...]] = None) -> tuple[Optional[tuple[int, ...]], ...]:
    """The yati groups of line ``line`` (0-based) in order; a group the weights
    ``pattern`` do not place yet is None. With several possible slots (సీసము's
    two forms) a group is placed only when every slot still possible agrees.

    >>> line_groups("utpalamala", 0, "")
    ((1, 10),)
    >>> line_groups("dvipada", 0, "UII"), line_groups("dvipada", 0, "UIIIIII")
    ((None,), ((1, 8),))
    """
    spec = default_dawg().spec(meter)
    per_slot = []
    for slot in _slots(meter, line, slots):
        if complete and not au.accepts(default_dawg().slot_dfas[(meter, slot)], pattern):
            continue
        starts = gana_starts(meter, slot, pattern)
        if starts is None:
            continue
        per_slot.append(tuple(_resolve(t, starts) for t in _group_templates(spec, slot)))
    if not per_slot:
        return ()
    out = []
    for i in range(max(len(x) for x in per_slot)):
        vals = {x[i] if i < len(x) else None for x in per_slot}
        out.append(vals.pop() if len(vals) == 1 else None)
    return tuple(out)


# ----------------------------------------------------------------------------
# engine calls and scanning, cached
# ----------------------------------------------------------------------------
@lru_cache(maxsize=1)
def _prasa_rules():
    """The prāsa ruleset, parsed once (``prasa.evaluate`` re-reads the YAML on every call without one)."""
    return prasa_engine.load_ruleset()


@lru_cache(maxsize=200_000)
def _prasa_ok(meter: str, padas: tuple[str, ...], profile: str) -> bool:
    return bool(prasa_engine.evaluate(list(padas), profile=profile, meter=meter, ruleset=_prasa_rules()).matched)


@lru_cache(maxsize=20_000)
def _prasa_features(text: str):
    return prasa_engine.extract_line(text, 1, _prasa_rules())


@lru_cache(maxsize=400_000)
def _yati_ok(syllables: tuple, group: tuple[int, ...], profile: str, prev_dead: tuple, prev_aras: bool,
             first: bool, allow_prasa_yati: bool) -> bool:
    res = yati_engine.evaluate_line(list(syllables), [group], profile, prev_line_dead=prev_dead,
                                    prev_line_ends_arasunna=prev_aras, first_pada=first,
                                    allow_prasa_yati=allow_prasa_yati, sandhi="off")
    return bool(res.groups and res.groups[0].matched)


@lru_cache(maxsize=200_000)
def _syllables(text: str) -> tuple:
    return sc.classify(sc.syllabify(unicodedata.normalize("NFC", text)))


# ----------------------------------------------------------------------------
# pair-level yati: what the engine reads about two aksharas, and nothing else
# ----------------------------------------------------------------------------
def clear_caches() -> int:
    """Empty the scanning and verdict caches of this module and the incremental scanner
    (they are almost all specific to one meter's lines; a long run clears them per meter
    to bound memory). Returns how many were cleared."""
    from . import incremental
    n = 0
    for mod in (incremental, globals()):
        for v in (vars(mod).values() if not isinstance(mod, dict) else mod.values()):
            if hasattr(v, "cache_clear") and v is not _prasa_rules:
                v.cache_clear()
                n += 1
    return n


def _canon(s):
    """A syllable stripped of where it sits (the engine reads only its sounds)."""
    return replace(s, start=0, end=0, word=0, weight="", rules=(), vikalpa="")


def _side(prev, s, word_initial: bool, prev_line_dead: tuple, prev_aras: bool, first: bool):
    """The key of one side of a yati pair: the akshara, the preceding bindu / drutam, the printed evidence.
    ``prev`` is the syllable before ``s`` in the line (None at the line start)."""
    s0 = _canon(s)
    if prev is None:
        ev = yati_engine.sandhi_evidence([s0], 1, prev_aras, first)
        return s0, False, tuple(prev_line_dead), tuple(ev)
    p0 = _canon(prev)
    seq = [p0, replace(s0, word=1 if word_initial else 0)]
    ev = yati_engine.sandhi_evidence(seq, 2, prev_aras, first)
    return s0, bool(prev.anusvara), tuple(d for d in prev.dead if d in ("న", "ల")), tuple(ev)


@lru_cache(maxsize=1_000_000)
def _pair_serves(a_side: tuple, b_side: tuple, profile: str) -> Optional[frozenset]:
    """The yati engine's verdict on one vaḷi / yati-akshara pair (sandhi off, no lexical context:
    the words are re-checked whole when the line ends): None when they are not in maitri, else
    the constituents of the vaḷi's onset that serve the match (indices; None = a vowel reading,
    which serves any) — what బహుయతి నియతి (YATI-SY-11) compares across a group's caesuras."""
    rs = yati_engine._rs(None)
    a, a_bindu, a_dead, a_ev = a_side
    b, b_bindu, b_dead, b_ev = b_side
    A = yati_engine.parse_akshara(a, a_bindu, a_dead, rs)
    B = yati_engine.parse_akshara(b, b_bindu, b_dead, rs)
    res = yati_engine.check(A, B, profile, ruleset=rs, sandhi="off", evidence_a=list(a_ev), evidence_b=list(b_ev))
    if not res.matched:
        return None
    return frozenset(c.reading_a.index for c in res.candidates if rs.accepted(profile, c.status))


def _pair_ok(a_side: tuple, b_side: tuple, profile: str) -> bool:
    return _pair_serves(a_side, b_side, profile) is not None


@lru_cache(maxsize=10_000)
def _vali_width(a_side: tuple) -> int:
    """Consonants in the vaḷi's onset as the engine parses it (its constituents)."""
    a, a_bindu, a_dead, _ = a_side
    return len(yati_engine.parse_akshara(a, a_bindu, a_dead, yati_engine._rs(None)).onset)


@lru_cache(maxsize=10)
def _niyati_binding(profile: str) -> bool:
    """Is a switch of constituents between caesuras (YATI-RJ-25) a failure under ``profile``?"""
    rs = yati_engine._rs(None)
    return not rs.accepted(profile, rs.status("YATI-RJ-25"))


def _line_side(syls, i: int, prev_line_dead: tuple, prev_aras: bool, first: bool):
    """The pair side of akshara ``i`` (1-based) of a scanned line."""
    s = syls[i - 1]
    prev = syls[i - 2] if i > 1 else None
    return _side(prev, s, prev is None or prev.word != s.word, prev_line_dead, prev_aras, first)


def _canon_prev(prev):
    """The syllable before a yati akshara, reduced to what the engine reads of it: its bindu and
    drutam (the akshara's context), its ఁ and whether its vowel is ఉ (the printed-text evidence
    of ``yati.sandhi_evidence``: a split after ఁ, టుగాగమ / నుగాగమ after ఉ)."""
    if prev is None:
        return None
    return replace(prev, text="", onset=(), vowel="ఉ" if prev.vowel == "ఉ" else "అ", visarga=False,
                   dead=tuple(d for d in prev.dead if d in ("న", "ల")),
                   start=0, end=0, word=0, weight="", rules=(), vikalpa="")


@lru_cache(maxsize=10_000)
def _norm_onset(onset: tuple[str, ...]) -> tuple[str, ...]:
    """An onset as the yati engine compares it (``parse_akshara`` without context)."""
    rs = yati_engine._rs(None)
    return tuple(rs.norm_c(c) for c in onset)


@lru_cache(maxsize=100_000)
def _prasa_yati_pair(onset2: tuple, onset_y1: tuple) -> bool:
    """ప్రాసయతి between akshara 2 and akshara Y+1, on normalised onsets: ``yati.line._prasa_yati``
    with the prāsa ruleset parsed once (the engine re-reads prasa_rules.yaml, 110 ms, on every
    call). The weight rule (YATI-PY-03) is checked by the callers."""
    prs = _prasa_rules()
    if onset2 == onset_y1:
        sub = "PRASA-SAMA-01"
    elif len(onset2) == 1 and len(onset_y1) == 1:
        sub = prs.lookup_pair_rule(onset2[0], onset_y1[0])
    else:
        sub = "PRASA-VAIRA-GENERIC"
    return prs.status(sub) not in ("forbidden",)


def _nfc(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def _canon_purva(text: str, onset: tuple) -> str:
    """The pre-prāsa akshara with its consonants replaced by క: the prāsa engine reads its vowel,
    its marks and its dead consonants (saṁśleṣa), never its onset — so candidates share verdicts."""
    if not onset:
        return text
    head = VIRAMA.join(onset)
    return "క" + text[len(head):] if text.startswith(head) else text


# ----------------------------------------------------------------------------
# the pending syllables of an unfinished word
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Desc:
    """One pending syllable, as far as the text fixes it."""
    text: str                           # as written (its final form when ``fixed``)
    fixed: bool                         # nothing about it can change any more
    onset: tuple[str, ...]              # consonants so far
    grow: bool                          # at least one more consonant will join the onset
    vowel: Optional[str]                # None: not written yet
    marks: bool                         # ం / ః may still be added
    options: Optional[frozenset] = None  # with an inventory: the attested syllables it may still become


@dataclass(frozen=True)
class Cont:
    """A structural way the unfinished word can go on."""
    kind: str                           # keep | grow | die | pollu | split | lone
    weights: tuple[str, ...]            # possible U/I of the pending positions
    descs: tuple[Desc, ...]             # one per pending position
    u_by_conjunct: bool = False         # a final U only through a conjunct the next akshara must open


def _fixed(s) -> Desc:
    return Desc(s.text, True, tuple(s.onset), False, s.vowel or None, False)


@lru_cache(maxsize=200_000)
def continuations(word: str, cluster_can_grow: bool = True, long_pollu: bool = True,
                  bare_pollu: bool = True, inv=None) -> tuple[Cont, ...]:
    """The structural classes behind ``split_word(word, cluster_can_grow, long_pollu).options``.

    ``bare_pollu=False`` says a word may not be dead consonants alone (the orthography filter):
    a word-initial ``C్`` must grow, and a first syllable cannot die. Their weights stay among the
    options (growing gives U or I), but the akshara with neither onset nor vowel that ending there
    would scan is gone — the registers must not count on it as a vaḷi or a yati / prāsa partner.

    With an inventory ``inv`` (:mod:`.inventory`) only attested syllables count: the committed ones
    and every final form must be in it, and the last pending syllable carries the attested completions
    that give it the class's weight (``Desc.options``), one class per weight and route: laghu through the
    completions light by their own rules; guru through those guru by their own rules (long vowel, mark,
    pollu form such as రుఁక్), or through the light ones followed by a conjunct (rule 5). That last route
    binds the next akshara to open a conjunct, so its class says so (``u_by_conjunct``) and the registers
    check it where the next akshara is the prāsa akshara, a yati target or a prāsa-yati partner
    (``Registers.alive``). Each route is judged on its own completions: unchecked, the conjunct route
    promised రుఁ as guru for an ఆటవెలది's ప్రాసయతి (రుఁక్ is not attested, no conjunct rhymes with ర); taken
    only when no guru form existed, it refused a లలిత's line 2 the prāsa akshara న్స్మ, attested only light
    and guru in line 1 through the conjunct after it — random-logit control, two dead ends.

    >>> sorted((c.kind, c.weights) for c in continuations("సత్య"))
    [('die', ('U',)), ('grow', ('UU', 'UI')), ('keep', ('UU', 'UI'))]
    """
    text = _nfc(word)
    syls = _syllables(text)
    if not syls:
        return (Cont("keep", ("",), ()),)
    b = syls[-1]
    a = syls[-2] if len(syls) >= 2 else None
    head_desc = (_fixed(a),) if a is not None else ()

    def w_a(conj: bool) -> str:
        return "U" if (sc.self_rules(a) or conj) else "I"

    out: list[Cont] = []
    ends_virama = text.endswith(VIRAMA)
    if ends_virama and not b.vowel:                            # word-initial C్
        out.append(Cont("grow", ("U", "I"), (Desc("", False, tuple(b.dead), True, None, True),)))
        if bare_pollu and (long_pollu or len(b.dead) < 2):
            out.append(Cont("lone", ("U",), (_fixed(b),)))
    elif ends_virama:                                          # … V C్
        head = w_a(b.is_conjunct) if a is not None else ""
        if long_pollu or len(b.dead) < 2:
            out.append(Cont("pollu", (head + "U",), head_desc + (_fixed(b),)))
        core = Desc(text[b.start:b.end - 2 * len(b.dead)], True, tuple(b.onset), False, b.vowel, False)
        new = Desc("", False, tuple(b.dead), True, None, True)
        out.append(Cont("split", (head + "UU", head + "UI"), head_desc + (core, new)))
    elif _open_cluster(b, text):
        keep_head = w_a(b.is_conjunct) if a is not None else ""
        out.append(Cont("keep", (keep_head + "U", keep_head + "I"),
                        head_desc + (Desc(b.text, False, tuple(b.onset), False, None, True),)))
        if cluster_can_grow:
            grow_head = "U" if a is not None else ""
            out.append(Cont("grow", (grow_head + "U", grow_head + "I"),
                            head_desc + (Desc(b.text, False, tuple(b.onset), True, None, True),)))
            if (long_pollu or len(b.onset) < 2) and (a is not None or bare_pollu):
                # dying leaves every consonant of b dead (with no a, the word is dead consonants alone)
                if a is not None:
                    died = Desc(a.text + b.text + VIRAMA, True, tuple(a.onset), False, a.vowel or None, False)
                else:
                    died = Desc(b.text + VIRAMA, True, (), False, None, False)
                out.append(Cont("die", ("U",), (died,)))
    else:                                                      # closed syllable
        head = w_a(b.is_conjunct) if a is not None else ""
        ws = (head + "U",) if sc.self_rules(b) else (head + "U", head + "I")
        closed = bool(b.anusvara or b.visarga or b.candrabindu)     # after a mark no other may follow (orthography)
        out.append(Cont("keep", ws, head_desc + (Desc(b.text, closed, tuple(b.onset), False, b.vowel, not closed),)))
    if inv is not None:
        return _attested(tuple(out), syls, inv)
    return tuple(out)


def _attested(conts: tuple[Cont, ...], syls: tuple, inv) -> tuple[Cont, ...]:
    """``conts`` restricted to an inventory: final syllables must be attested, pending ones get their
    attested completions, and only the weights those completions have by their own rules remain."""
    if any(s.text not in inv for s in syls[:-2]):
        return ()                                              # a committed syllable is not attested
    out = []
    for c in conts:
        descs = []
        last = len(c.descs) - 1
        for i, d in enumerate(c.descs):
            closed = c.kind == "keep" and i == last and d.fixed and d.vowel   # closed by a mark: a pollu may follow
            if d.fixed and not closed:
                if d.text not in inv:
                    break
                descs.append(d)
                continue
            if d.grow:                                         # the cluster grows: a longer onset
                opts = inv.growing(d.onset)
            elif d.vowel:                                      # written: only marks or a pollu may follow
                opts = inv.extending(d.text, d.onset)
            else:                                              # the cluster takes its vowel
                opts = inv.with_onset(d.onset)
            if not opts:
                break
            descs.append(replace(d, options=opts))
        else:
            d = descs[-1]
            if d.options is None:                                  # every syllable fixed by the text
                out.append(Cont(c.kind, c.weights, tuple(descs)))
                continue
            light = frozenset(u for u in d.options if not _guru(u))
            guru = d.options - light
            head = tuple(descs[:-1])
            for w in c.weights:
                if w[-1] == "I":
                    routes = ((light, False),)
                else:                                              # guru by itself, or light + a conjunct
                    routes = ((guru, False), (light, True))
                for opts, conj in routes:
                    if opts:
                        out.append(Cont(c.kind, (w,), head + (replace(d, options=opts),), u_by_conjunct=conj))
    return tuple(out)


def _onsets(options) -> list[tuple[str, ...]]:
    """The distinct consonant clusters of the attested completions."""
    return sorted({tuple(_syllables(u)[0].onset) for u in options})


def _guru(unit: str) -> bool:
    syls = _syllables(unit)
    return bool(syls and sc.self_rules(syls[0]))


@lru_cache(maxsize=50_000)
def _yati_forms(options) -> tuple[str, ...]:
    """The completions, one syllable per combination the yati engine distinguishes (onset, vowel,
    ం / ః / ఁ, pollu or not): the same verdicts from far fewer candidates."""
    seen, out = set(), []
    for u in sorted(options):
        s = _syllables(u)[0]
        key = (tuple(s.onset), s.vowel, s.anusvara, s.visarga, s.candrabindu, bool(s.dead))
        if key not in seen:
            seen.add(key)
            out.append(u)
    return tuple(out)


def _conjunct_units(inv) -> frozenset:
    """The attested syllables that open with a conjunct."""
    return inv.conjuncts()


def _realizations(d: Desc, weight: str, prefer: tuple[str, ...] = (), signs: tuple[str, ...] = ("ం",),
                  vowels: Optional[tuple[str, ...]] = None) -> list[str]:
    """Texts the pending syllable ``d`` may still become, consistent with ``weight``
    (``prefer``: consonants to try first when the onset grows, e.g. the vaḷi's;
    ``signs``: the marks worth trying — a bindu for yati, ం and ః for a pūrva;
    ``vowels``: the vowels worth trying when it has none yet, default all that fit the weight)."""
    if d.options is not None:                  # an inventory: the class's attested completions
        return _yati_forms(d.options)
    if d.fixed or (d.vowel and not d.marks and not d.grow):
        return [d.text]
    if d.vowel:                                # written: only a mark may still follow
        return [d.text] + ([d.text + s for s in signs] if weight == "U" else [])
    if vowels is None:
        vowels = list(SHORT_VOWELS if weight == "I" else ALL_VOWELS)
    else:
        vowels = [v for v in vowels if weight == "U" or v in SHORT_VOWELS]
    grow_with = tuple(dict.fromkeys(prefer + REP_CONSONANTS))
    onsets = [d.onset + (c,) for c in grow_with] if d.grow else [d.onset]
    marks = [""] + (list(signs) if d.marks and weight == "U" else [])
    out = []
    for on in onsets:
        for v in vowels:
            for mk in marks:
                out.append((VIRAMA.join(on) + MATRA[v] if on else v) + mk)
    return out


@lru_cache(maxsize=200_000)
def _anchor_follows(meter: str, done: tuple[str, ...], before_prasa: str, profile: str) -> bool:
    """Can the prāsa akshara of a line already written follow ``before_prasa`` (the line up to its
    pūrva)? Every written line's own prāsa akshara is tried, not only line 1's: lines in prāsa maitri
    differ (line 1 జన్ చి, line 2 బింజ), and a pūrva that fits line 2's akshara may not fit line 1's
    (random-logit control, మానిని: with only line 1's tried, no first token of line 3 was allowed — a
    dead end). A pūrva may have fused a dead consonant into the prāsa onset (saṁśleṣa), so each
    anchor is tried with and without that consonant written after the pūrva."""
    tails = []
    for line in done:
        anchor = _prasa_features(line)
        fused = "".join(c + VIRAMA for c in anchor.fused_from_purva)
        tails.append(anchor.prasa)
        if fused and not before_prasa.endswith(fused):
            tails.append(fused + anchor.prasa)
    return any(_prasa_ok(meter, done + (before_prasa + t + NEUTRAL_TAIL,), profile) for t in dict.fromkeys(tails))


def _prasa_yati_holds(syls, g: tuple[int, ...]) -> bool:
    """``yati.line._prasa_yati`` on a scanned line: the weights of aksharas P and Y agree and
    akshara Y+1 rhymes with akshara P+1, for the pair group ``g = (P, Y)``."""
    p1, y = g
    if y + 1 > len(syls) or p1 + 1 > len(syls):
        return False
    w1, wy = syls[p1 - 1].weight, syls[y - 1].weight
    if w1 and wy and w1 != wy:
        return False
    return _prasa_yati_pair(_norm_onset(tuple(syls[p1].onset)), _norm_onset(tuple(syls[y].onset)))


@lru_cache(maxsize=10_000)
def _fallback_feasible(onset2: tuple[str, ...], onset: tuple[str, ...], grow: bool) -> bool:
    """Some final onset of the pending akshara Y+1 (``onset`` so far, ``grow``: one more consonant
    at least) rhymes with akshara P+1's normalised ``onset2`` (ప్రాసయతి). A grown onset is a
    conjunct, and a conjunct rhymes only by identity (PRASA-VAIRA-GENERIC is forbidden otherwise)."""
    have = _norm_onset(onset)
    if not grow:
        return _prasa_yati_pair(onset2, have)
    if len(onset2) > len(have) and onset2[:len(have)] == have:
        return True
    return _prasa_rules().status("PRASA-VAIRA-GENERIC") not in ("forbidden",)


# One vowel of each yati vowel class (YATI-SV-01), short and long, and ఋ, the one vowel with rules
# of its own on a consonant (YATI-SV-05.2 / SV-07). With consonants on both sides of a pair, maitri
# reads only these distinctions (checked against the engine: tests/test_dec_registers.py).
CLASS_VOWELS = {"I": ("అ", "ఇ", "ఉ", "ఋ"), "U": ("అ", "ఇ", "ఉ", "ఋ", "ఆ", "ఈ", "ఊ")}


def _vowels_for(vali_side: tuple, d: Desc, weight: str) -> Optional[tuple[str, ...]]:
    """Vowels worth trying for a pending yati akshara: one per class when consonants stand on both
    sides; every vowel when either side is a bare vowel (svara rules name vowels)."""
    if d.vowel or not d.onset or not vali_side[0].onset:
        return None
    return CLASS_VOWELS[weight]


@lru_cache(maxsize=500_000)
def _target_feasible(vali_side: tuple, prev, word_initial: bool, d: Desc, weight: str, profile: str) -> bool:
    """Some realisation of the pending yati akshara ``d`` is in maitri with the vaḷi.
    Keyed by what the engine reads (not by the line), so candidates share the answer."""
    vowels = _vowels_for(vali_side, d, weight)
    for t in _realizations(d, weight, tuple(vali_side[0].onset), vowels=vowels):
        syls = _syllables(t)
        if syls and _pair_ok(vali_side, _side(prev, syls[0], word_initial, (), False, False), profile):
            return True
    return False


@lru_cache(maxsize=100_000)
def _target_serves(vali_side: tuple, prev, word_initial: bool, d: Desc, weight: str, profile: str) -> Optional[frozenset]:
    """The vaḷi constituents some realisation of the pending akshara ``d`` can be matched through
    (None: no realisation matches). Every vowel is tried: this is for బహుయతి నియతి only."""
    out: set = set()
    hit = False
    for t in _realizations(d, weight, tuple(vali_side[0].onset)):
        syls = _syllables(t)
        s = _pair_serves(vali_side, _side(prev, syls[0], word_initial, (), False, False), profile) if syls else None
        if s is not None:
            hit = True
            out |= s
    return frozenset(out) if hit else None


# ----------------------------------------------------------------------------
# the registers
# ----------------------------------------------------------------------------
class _Line:
    """The current line of a state: its committed aksharas and where the pending ones start."""

    def __init__(self, st, committed: str):
        self.st = st
        self.pattern = committed
        self.F = len(committed)
        self._syls = None

    @property
    def syls(self):
        """The line scanned: the finished words once per step (cached), the unfinished word on top."""
        if self._syls is None:
            text, word = self.st.line_text, self.st.word
            finished = text[:len(text) - len(word)] if word else text
            syls = _syllables(finished)
            if word:
                off = len(_nfc(finished))
                base = syls[-1].word + 1 if syls else 0
                syls = syls + tuple(replace(s, start=s.start + off, end=s.end + off, word=s.word + base)
                                    for s in _syllables(word))
            self._syls = syls
        return self._syls

    @property
    def nfc(self) -> str:
        return _nfc(self.st.line_text)

    def pending_start(self) -> int:
        s = self.syls
        return s[self.F].start if self.F < len(s) else len(self.nfc)

    def desc(self, i: int, cont: Cont) -> Desc:
        return _fixed(self.syls[i - 1]) if i <= self.F else cont.descs[i - self.F - 1]


class Registers:
    """Prāsa and yati for one meter, for :class:`~metrical_decoder.enforcer.Enforcer`."""

    def __init__(self, meter: str, prasa: bool = True, yati: bool = True, profile: str = "strict"):
        self.meter = meter
        self.spec = default_dawg().spec(meter)
        self.prasa = prasa and bool(self.spec.prasa)
        self.yati = yati
        self.profile = profile

    def _line_slots(self, st) -> tuple[str, ...]:
        """The slots the current line may take, given the lines already written."""
        return slots_for(self.meter, tuple("".join(s.weight for s in _syllables(t)) for t in st.done))

    # ------------------------------------------------------------ liveness
    def alive(self, enf, st, cluster_can_grow: bool = True, long_pollu: bool = True,
              bare_pollu: bool = True, inv=None) -> bool:
        """Some continuation keeps gaṇa, prāsa and yati satisfiable together (with attested
        syllables only, given an inventory ``inv``)."""
        if st.word:
            split = split_word(st.word, cluster_can_grow, long_pollu)
            q2 = enf.run(st.q, split.committed)
            if q2 is None:
                return False
            line = _Line(st, st.line_pat + split.committed)
            conts = continuations(st.word, cluster_can_grow, long_pollu, bare_pollu, inv)
        else:
            q2 = st.q
            line = _Line(st, st.line_pat)
            conts = (Cont("keep", ("",), ()),)
        for cont in conts:
            for w in cont.weights:
                q3 = enf.run(q2, w)
                if q3 is None:
                    continue
                conj = inv is not None and cont.u_by_conjunct and w.endswith("U")
                if conj and enf.run(q3, "U") is None and enf.run(q3, "I") is None:
                    continue                           # no room for the conjunct akshara in this line
                if self._option_ok(st, line, cont, w, inv if conj else None):
                    return True
        return False

    def _option_ok(self, st, line: _Line, cont: Cont, w: str, conj=None) -> bool:
        """``conj`` (an inventory): the akshara after the pending ones must open with a conjunct."""
        if self.prasa and not st.prasa_ok and not self._prasa_ok(st, line, cont, w):
            return False
        if not self.yati:
            return True
        pattern = line.pattern + w
        n = line.F + len(w)
        per_slot = slot_groups(self.meter, st.lines, pattern, self._line_slots(st))
        if not per_slot:
            return True                        # (the automaton has the final word on the gaṇas)
        # groups before ydone were decided in advance() — they are the same in every slot
        return any(all(g is None or g[0] > n or self._group_possible(st, line, cont, w, pattern, g, conj)
                       for g in groups[st.ydone:])
                   for groups in per_slot)

    def _group_possible(self, st, line: _Line, cont: Cont, w: str, pattern: str, g: tuple[int, ...],
                        conj=None) -> bool:
        """Some continuation satisfies the group: every target in maitri with the vaḷi, or,
        where the meter allows it, ప్రాసయతి for a pair (P, Y) (weights of P and Y equal,
        akshara Y+1 rhyming with akshara P+1)."""
        n = line.F + len(w)
        ctx = (st.pdead, st.paras, st.lines == 0)
        if g[0] > line.F:
            return True                        # the vaḷi itself is still being written
        vali = _line_side(line.syls, g[0], *ctx)
        # బహుయతి నియతి: with a conjunct vaḷi, one constituent must serve every caesura of the group
        niyati = len(g) > 2 and _niyati_binding(self.profile) and _vali_width(vali) > 1
        direct, serves = True, []
        for p in g[1:]:
            if p == n + 1 and conj is not None:
                # the next akshara must open with a conjunct: some attested one in maitri with the vaḷi
                prev = _syllables(cont.descs[-1].text)[-1] if cont.descs and cont.descs[-1].text else None
                d = Desc("", False, (), False, None, True, options=_conjunct_units(conj))
                if not any(_target_feasible(vali, _canon_prev(prev), False, d, wt, self.profile) for wt in "UI"):
                    direct = False
                    break
                serves.append(frozenset((None,)))
                continue
            if p > n:
                continue                       # not written yet: any constituent can still be served
            if p <= line.F:
                s = _pair_serves(vali, _line_side(line.syls, p, *ctx), self.profile)
            elif niyati:
                s = _target_serves(vali, *self._target_args(st, line, cont, w, p), self.profile)
            else:
                s = frozenset((None,)) if _target_feasible(vali, *self._target_args(st, line, cont, w, p),
                                                           self.profile) else None
            if s is None:
                direct = False
                break
            serves.append(s)
        if direct and niyati:
            direct = any(all(i in s or None in s for s in serves) for i in range(_vali_width(vali)))
        if direct:
            return True
        if not (self.spec.prasa_yati and len(g) == 2):
            return False
        p1, y = g
        if pattern[p1 - 1] != pattern[y - 1]:
            return False                       # YATI-PY-03: aksharas P and Y must weigh the same
        if y + 1 == n + 1 and conj is not None:
            # the prāsa-yati akshara must open with a conjunct, and a conjunct rhymes only by identity
            onset2 = _norm_onset(tuple(line.syls[p1].onset)) if p1 <= line.F else None
            return onset2 is None or (len(onset2) >= 2 and _prasa_yati_pair(onset2, onset2))
        if y + 1 > n:
            return True                        # the prāsa-yati akshara is not written yet
        if y + 1 <= line.F:
            return _prasa_yati_holds(line.syls, g)
        # akshara P+1 is committed: Y+1 ≤ F + 3 and every such meter has Y ≥ P + 4
        d = cont.descs[y - line.F]
        onset2 = _norm_onset(tuple(line.syls[p1].onset))
        if d.options is not None:
            return any(_prasa_yati_pair(onset2, _norm_onset(o)) for o in _onsets(d.options))
        return _fallback_feasible(onset2, d.onset, d.grow)

    @staticmethod
    def _target_args(st, line: _Line, cont: Cont, w: str, p: int) -> tuple:
        """What the engine reads of the pending yati akshara ``p`` and its context:
        (previous syllable, reduced; opens the unfinished word; descriptor; weight)."""
        k = p - line.F - 1
        if p - 1 <= line.F:
            prev = line.syls[p - 2] if p > 1 else None
        else:
            before = cont.descs[k - 1]
            prev = _syllables(before.text)[-1] if before.text else None
        word_initial = p == len(st.line_pat) + 1
        return _canon_prev(prev), word_initial, cont.descs[k], w[k]

    def _prasa_ok(self, st, line: _Line, cont: Cont, w: str) -> bool:
        n = line.F + len(w)
        if n == 0:
            return True
        d1 = line.desc(1, cont)
        if st.lines == 0:                      # line 1 sets the prāsa: it must carry a consonant
            if n < 2:
                return True
            d2 = line.desc(2, cont)
            dead1 = _syllables(d1.text)[0].dead if d1.text else ()
            if d2.options is not None:
                return bool(dead1) or any(_onsets(d2.options))
            return not (d2.vowel and not d2.onset and not d2.grow and not dead1)
        done = tuple(st.done)
        purva = _canon_purva(d1.text, d1.onset)
        if n < 2 or not d1.fixed:
            # akshara 2 not started, or the pūrva still open: some final form of the pūrva must take
            # a written line's own prāsa akshara (identity is the canonical prāsa) — in the same word
            # or after a space, unless what follows the pūrva is already written
            after = self._after_purva(line, cont) if n >= 1 and d1.fixed else ""
            seps = (after,) if after else ("", " ")
            weight = w[0] if 1 > line.F else line.pattern[0]
            if d1.fixed:
                pooled = [purva]
            elif d1.options is not None:       # an inventory: the class's attested final forms (a light one
                # is guru through the anchor's conjunct; the prāsa engine reads the pūrva with the anchor)
                pooled = sorted({_canon_purva(u, tuple(_syllables(u)[0].onset)) for u in d1.options})
            elif d1.vowel:                     # the text as it stands (ఁ and all), plus the marks still possible
                pooled = [purva] + ([purva + s for s in ("ం", "ః")] if d1.marks and weight == "U" else [])
            else:                              # consonants only: a canonical onset
                canon = Desc("", False, ("క",) if (d1.onset or d1.grow) else (), False, None, d1.marks)
                pooled = _realizations(canon, weight, signs=("ం", "ః"))
            return any(_anchor_follows(self.meter, done, r + sep, self.profile) for r in pooled for sep in seps)
        head = purva + self._between_1_2(line, cont)
        d2 = line.desc(2, cont)
        if d2.options is not None:
            return any(_prasa_ok(self.meter, done + (head + VIRAMA.join(o) + NEUTRAL_TAIL,), self.profile)
                       for o in _onsets(d2.options) if o)
        if d2.grow:
            eff = list(_syllables(d1.text)[0].dead) + list(d2.onset)
            if not any(len(a.onset) > len(eff) and a.onset[:len(eff)] == eff
                       for a in (_prasa_features(t) for t in st.done)):
                return False
            return _anchor_follows(self.meter, done, head, self.profile)
        if not d2.onset:
            t2 = (d2.vowel or "అ")
        else:
            t2 = VIRAMA.join(d2.onset) + MATRA.get(d2.vowel or "అ", "")
        return _prasa_ok(self.meter, done + (head + t2 + NEUTRAL_TAIL,), self.profile)

    @staticmethod
    def _after_purva(line: _Line, cont: Cont) -> str:
        """What stands after a finished pūrva when akshara 2 has not started (a space, or nothing)."""
        if line.F >= 1:
            return line.nfc[line.syls[0].end:]
        return ""

    @staticmethod
    def _between_1_2(line: _Line, cont: Cont) -> str:
        """The text between the pūrva and the prāsa akshara (a space when they are separate words)."""
        if line.F >= 2:
            return line.nfc[line.syls[0].end:line.syls[1].start]
        if line.F == 1:
            return line.nfc[line.syls[0].end:line.pending_start()]
        return ""

    # ------------------------------------------------------------ verdicts
    def advance(self, st):
        """Record the verdicts the committed aksharas make final (None = dead)."""
        split = split_word(st.word) if st.word else None
        line = _Line(st, st.line_pat + (split.committed if split else ""))
        prasa_ok = st.prasa_ok
        if self.prasa and not prasa_ok and line.F >= 2:
            s1, s2 = line.syls[0], line.syls[1]
            cut = _canon_purva(s1.text, tuple(s1.onset)) + line.nfc[s1.end:s2.end] + NEUTRAL_TAIL
            if st.lines == 0:
                ok = not _prasa_features(cut).bare_vowel
            else:
                ok = _prasa_ok(self.meter, tuple(st.done) + (cut,), self.profile)
            if not ok:
                return None
            prasa_ok = True
        ydone = st.ydone
        if self.yati:
            groups = line_groups(self.meter, st.lines, line.pattern, slots=self._line_slots(st))
            ctx = (st.pdead, st.paras, st.lines == 0)
            while ydone < len(groups):
                g = groups[ydone]
                if g is None or max(g) > line.F:
                    break
                if len(g) == 2:                # a pair: the cached pair verdict; groups of 3+ need బహుయతి నియతి
                    ok = _pair_ok(_line_side(line.syls, g[0], *ctx), _line_side(line.syls, g[1], *ctx), self.profile)
                else:
                    ok = _yati_ok(tuple(line.syls[:max(g)]), g, self.profile, *ctx, False)
                if ok:
                    ydone += 1
                    continue
                if self.spec.prasa_yati and len(g) == 2:
                    if line.pattern[g[0] - 1] != line.pattern[g[1] - 1]:
                        return None            # ప్రాసయతి impossible: aksharas P and Y weigh differently
                    if line.F >= g[1] + 1:     # akshara Y+1 committed: does it rhyme with akshara P+1?
                        if _prasa_yati_holds(line.syls, g):
                            ydone += 1
                            continue
                        return None
                    break                      # the prāsa-yati akshara is not committed yet
                return None
        if prasa_ok == st.prasa_ok and ydone == st.ydone:
            return st
        return st._replace(prasa_ok=prasa_ok, ydone=ydone)

    def close_line(self, st):
        """The line has ended: re-verify it whole, with complete words. Returns the
        state with the context the next line's vaḷi needs, or None."""
        syls = _syllables(st.line_text)
        if not syls:
            return None
        text = _nfc(st.line_text)
        if self.prasa:
            if st.lines == 0:
                ok = len(syls) >= 2 and not _prasa_features(text).bare_vowel
            else:
                ok = _prasa_ok(self.meter, tuple(st.done) + (text,), self.profile)
            if not ok:
                return None
        if self.yati:
            pattern = "".join(s.weight for s in syls)
            ctx = (st.pdead, st.paras, st.lines == 0)
            for g in line_groups(self.meter, st.lines, pattern, True, self._line_slots(st)):
                if g is None:
                    return None
                if _yati_ok(tuple(syls), g, self.profile, *ctx, False):
                    continue
                # the engine's own fallback (evaluate_line(allow_prasa_yati=True)) re-reads the prāsa
                # YAML on every call; _prasa_yati_holds is the same test with the ruleset parsed once
                if not (self.spec.prasa_yati and len(g) == 2 and _prasa_yati_holds(syls, g)):
                    return None
        last = syls[-1]
        return st._replace(pdead=tuple(d for d in last.dead if d in ("న", "ల")), paras=bool(last.candrabindu))
