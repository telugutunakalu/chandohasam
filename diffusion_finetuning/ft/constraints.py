"""Stage 3 constraint compiler (PLAN §6.2): which tokens may come next in a poem of a given metre.

A poem is decoded left to right. The state tracks where the syllables written so far can be
in the metre's gaṇa grammar (an NFA built from ``indic_meter_dawg.prosody.flatten``, whose
states know their line, gaṇa and offset), plus what prāsa and yati need.

Weights follow ``indic_meter_dawg.scansion``: a syllable is guru by itself (long vowel,
diphthong, anusvara, visarga, pollu) or because the next syllable of the same word starts
with a conjunct. The last syllable written is therefore *pending* while it is light: its
weight is settled by the next token —

  next syllable, same word, plain conjunct     -> U
  next syllable, same word, ర-vattu conjunct   -> U or I (vikalpa; U only with ``vikalpa=False``)
  next syllable after a space or half-break     -> I, or U when it starts with a conjunct (vikalpa;
                                                   I only with ``vikalpa=False``)
  end of a pāda                                 -> I or U (pādānta guru)

Hard constraints:
- the metre: weights, line count, the sīsa half-break (required: the second half cannot start
  without it) and the ettugīti; no pāda may start after the last unit's ``padalu`` pādas (the couplet
  metres — dvipada, ragaḍas — would otherwise chain couplets without end);
- prāsa: the 2nd syllable of every pāda shares line 1's consonant (the relaxed equivalences unless
  the token table was built with ``prasa_relaxed=False``); line 1's prāsa akshara is not a bare vowel
  (PRASA-SAMA-01); the 1st akshara of every pāda has line 1's positional weight (PRASA-PURVAKSHARA-01,
  mandatory in every profile: chandohasam passes no metre class, so no exemption applies). A pollu on
  a pāda's first akshara fuses into the prāsa onset (PRASA-POS-06: తమ్ + వ reads మ్వ), so the onsets
  compared are the fused ones, and a bare-vowel prāsa akshara is fine after a pollu. The prāsa
  engine counts a pre-prāsa akshara guru when it is guru by itself or when the prāsa akshara is a
  conjunct, across a word break too (its aksharanusarika weights), so with a single-consonant prāsa
  every head must match line 1's head, and with a conjunct prāsa every head is guru already.
Soft: yati, a penalty on syllables that are not in maitri with the head (వళి), wherever some live
parse puts a yati. The seats are grouped as the yati engine's stanza planner groups them
(``yati.stanza.plan_from_candidate``): a half-line metre with two yati points pairs its second seat
with the second half's first syllable (సీసము); a fixed vṛtta without ప్రాసయతి and with several
seats forms one బహుయతి group, where one constituent of a conjunct head must serve every seat
(YATI-SY-11); otherwise every seat pairs with the pāda head. Maitri is ``ft.yati_oracle`` — the yati engine's own
verdict in the known left context, for a chosen profile and sandhi mode (the ప్రాసయతి fallback is
not offered, so metres that allow it are held to plain maitri). The final engine check
(chandohasam.analyze) remains the arbiter.
"""
from __future__ import annotations

import functools
import re
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

from indic_meter_dawg import scansion as sc
from indic_meter_dawg.prosody import flatten

from .metres import dawg

U, I, NL = "U", "I", "\n"
ONSET_PLAIN, ONSET_CONJ, ONSET_REPHA = 0, 1, 2
PRASA_EQUIV = {"శ": "స", "ణ": "న", "ళ": "ల", "ఱ": "ర", "ధ": "థ"}     # the relaxed prāsamaitri of PRASA_README
_NT = re.compile(r"^(?:⟨[UI]⟩)?(?:F(\d+)\.)?L(\d+)\.G(\d+)$")


# -----------------------------------------------------------------------------
# per-token features
# -----------------------------------------------------------------------------
@dataclass
class TokenTable:
    is_syl: np.ndarray           # bool: a whole Telugu akshara usable in a poem
    heavy: np.ndarray            # bool: guru by itself
    onset: np.ndarray            # int8: ONSET_PLAIN / ONSET_CONJ / ONSET_REPHA
    yati_key: np.ndarray         # int32: index into ``yati_keys`` (-1 for non-syllables)
    prasa_key: np.ndarray        # int32: index into ``prasa_keys``
    bindu: np.ndarray            # bool: carries an anusvara (a bindu before the next syllable's consonant)
    vowel_onset: np.ndarray      # bool: a bare vowel (no consonant onset)
    pollu: np.ndarray            # int32: index into ``pollu_tuples`` (0: no pollu)
    pollu_tuples: list           # normalised trailing dead consonants, () first
    yati_keys: list              # (first sound, vowel)
    prasa_keys: list             # normalised onset tuple (("V",) for a bare vowel)
    space: int
    newline: int
    eos: int

    @property
    def cls(self) -> np.ndarray:
        """Weight class of each syllable token: 3 * heavy + onset (0..5)."""
        return self.heavy.astype(np.int8) * 3 + self.onset

    @functools.cached_property
    def key_classes(self) -> np.ndarray:
        """(prāsa keys, 6): which weight classes occur among the syllables with each prāsa key."""
        out = np.zeros((len(self.prasa_keys), 6), bool)
        out[self.prasa_key[self.is_syl], self.cls[self.is_syl]] = True
        return out

    @functools.cached_property
    def key_of(self) -> dict:
        """Normalised onset tuple -> prāsa key (("V",) for a bare vowel)."""
        return {k: i for i, k in enumerate(self.prasa_keys)}

    def onset_of(self, token: int) -> tuple:
        k = self.prasa_keys[self.prasa_key[token]]
        return () if k == ("V",) else k

    @functools.cached_property
    def representative(self) -> np.ndarray:
        """(6, 2): one syllable token per weight class and bindu (-1 if none), for lookahead; a token
        without a pollu where the class has one (a pollu would fuse into the prāsa onset)."""
        out = np.full((6, 2), -1, np.int64)
        syl = np.flatnonzero(self.is_syl)[::-1]
        for i in list(syl[self.pollu[syl] != 0]) + list(syl[self.pollu[syl] == 0]):
            out[self.cls[i], int(self.bindu[i])] = i
        return out

    @functools.cached_property
    def bindu_classes(self) -> np.ndarray:
        """(2, 6): which weight classes occur among syllables without / with a bindu."""
        out = np.zeros((2, 6), bool)
        out[self.bindu[self.is_syl].astype(int), self.cls[self.is_syl]] = True
        return out


def build_token_table(tok, prasa_relaxed: bool = True) -> TokenTable:
    """``prasa_relaxed``: prāsa keys use the relaxed equivalences (శ~స, ణ~న, ళ~ల, ఱ~ర, ధ~థ)."""
    V = tok.vocab_size
    is_syl = np.zeros(V, bool)
    heavy = np.zeros(V, bool)
    onset = np.zeros(V, np.int8)
    yk = np.full(V, -1, np.int32)
    pk = np.full(V, -1, np.int32)
    bindu = np.zeros(V, bool)
    vowel = np.zeros(V, bool)
    pollu = np.zeros(V, np.int32)
    ykeys: dict = {}
    pkeys: dict = {}
    pollus: dict = {(): 0}
    equiv = PRASA_EQUIV if prasa_relaxed else {}
    for s, i in tok.piece_to_id.items():
        if not s or not ("ఀ" <= s[0] <= "ౣ"):
            continue
        syl = sc.syllabify(s)
        if len(syl) != 1 or (syl[0].vowel == "" and syl[0].dead):       # bare dead consonants never stand alone
            continue
        a = syl[0]
        is_syl[i] = True
        heavy[i] = bool(sc.self_rules(a))
        onset[i] = ONSET_REPHA if a.is_repha_conjunct else ONSET_CONJ if a.is_conjunct else ONSET_PLAIN
        yk[i] = ykeys.setdefault((a.first_sound, a.vowel), len(ykeys))
        norm = tuple(equiv.get(c, c) for c in a.onset) or ("V",)
        pk[i] = pkeys.setdefault(norm, len(pkeys))
        bindu[i] = a.anusvara
        vowel[i] = not a.onset
        pollu[i] = pollus.setdefault(tuple(equiv.get(c, c) for c in a.dead), len(pollus))
    return TokenTable(is_syl, heavy, onset, yk, pk, bindu, vowel, pollu, list(pollus), list(ykeys), list(pkeys),
                      tok.encode(" ")[0], tok.encode("\n")[0], tok.eos_id)


# -----------------------------------------------------------------------------
# the metre NFA
# -----------------------------------------------------------------------------
@dataclass
class Place:
    unit: int                    # 0 = main metre, 1 = ettugīti
    line: int                    # 1-based pāda within the unit
    gana: int                    # 1-based gaṇa within the pāda
    offset: int                  # syllables already read in this gaṇa
    slot: str                    # the line's slot name ("odd", "even", "all", ...)


@dataclass
class MetreNFA:
    meters: tuple                # catalogue names of the units
    edges: list                  # state -> {symbol: set(states)}
    place: list                  # state -> Place (None for ACCEPT)
    start: frozenset
    prasa: tuple                 # per unit: prāsa required
    yati_ganas: tuple            # per unit: {slot: gaṇa numbers carrying a yati}
    yati_aksharas: tuple         # per unit: {slot: akshara numbers carrying a yati}
    half_gana: tuple             # per unit: the gaṇa that starts a pāda's second half (0 = none)
    padalu: tuple = ()           # per unit: the number of pādas
    yati_group: tuple = ()       # per unit: "half" / "bahu" / "pairs" (how the seats pair with a head)
    accept: int = 0              # the state reached when the whole poem is read

    def step(self, states: frozenset, sym: str) -> frozenset:
        out = set()
        for s in states:
            out |= self.edges[s].get(sym, set())
        return frozenset(out)


@functools.lru_cache(maxsize=64)
def build_nfa(label: str) -> MetreNFA:
    """label: a catalogue metre, or "seesamu+tetagiti" style (main + ettugīti)."""
    d = dawg()
    meters = tuple(label.split("+"))
    edges: list = []
    place: list = []

    def new(p) -> int:
        edges.append({})
        place.append(p)
        return len(edges) - 1

    accept = new(None)
    unit_start, unit_accept = [], []
    prasa, yg, ya, half, padalu, group = [], [], [], [], [], []
    for u, meter in enumerate(meters):
        spec = d.spec(meter)
        g = flatten(spec, d)
        patterns = spec.slot_patterns
        nt_state: dict[str, int] = {}

        def state_of(nt: str) -> int:
            if nt not in nt_state:
                if nt == g.start:
                    p = Place(u, 1, 1, 0, patterns[0][0])
                else:
                    m = _NT.match(nt)
                    form = int(m.group(1)) - 1 if m.group(1) else 0
                    line, gana = int(m.group(2)), int(m.group(3))
                    p = Place(u, line, gana, 0, patterns[form][line - 1])
                nt_state[nt] = new(p)
            return nt_state[nt]

        u_accept = new(None) if u < len(meters) - 1 else accept
        for prod in g.productions:
            src = state_of(prod.lhs)
            base = place[src]
            cur = src
            syms = list(prod.terminals)
            for k, sym in enumerate(syms):
                last = k == len(syms) - 1
                if last:
                    dst = state_of(prod.rhs) if prod.rhs else u_accept
                else:
                    dst = new(replace(base, offset=base.offset + sum(1 for x in syms[:k + 1] if x != NL)))
                edges[cur].setdefault(sym, set()).add(dst)
                cur = dst
        unit_start.append(state_of(g.start))
        unit_accept.append(u_accept)
        prasa.append(bool(spec.prasa))
        yg.append(dict(spec.yati_ganas))
        ya.append(dict(spec.yati_aksharas))
        half.append(5 if spec.halves_per_line == 2 else 0)
        padalu.append(spec.padalu)
        group.append(_yati_group(meter, spec))
    for u in range(len(meters) - 1):                    # the main unit's end reads ⏎ into the ettugīti
        edges[unit_accept[u]].setdefault(NL, set()).add(unit_start[u + 1])
    return MetreNFA(meters, edges, place, frozenset({unit_start[0]}), tuple(prasa), tuple(yg), tuple(ya), tuple(half),
                    tuple(padalu), tuple(group), accept)


def _yati_group(meter: str, spec) -> str:
    """How the yati engine groups this metre's seats (yati.stanza.plan_from_candidate)."""
    from yati.stanza import _meter_flags
    flags = _meter_flags(meter)
    points = max([len(spec.yati_aksharas.get(s, ())) or len(spec.yati_ganas.get(s, ())) for s in spec.slot_names] or [0])
    if flags["halves"] == 2 and points == 2:
        return "half"
    if flags["system"] == "fixed" and not flags["prasa_yati"] and points > 1:
        return "bahu"
    return "pairs"


# -----------------------------------------------------------------------------
# decoding state
# -----------------------------------------------------------------------------
@dataclass(frozen=True)
class Spec:
    ok_cls: np.ndarray           # the 6 weight classes (3 * heavy + onset) that may come next
    space: bool
    nl: bool                     # a pāda end or a sīsa half-break
    eos: bool
    prasa: int                   # the prāsa key the next syllable must have (-1: none)
    block: bool                  # no syllable at all (bindu-pūrvaka prāsa broken)
    yati: tuple | None           # (head token, head context, seat context) when the next syllable may be on a yati
    bindu: int = -1              # the next syllable must (1) / must not (0) carry a bindu (-1: either)
    no_vowel: bool = False       # the next syllable may not be a bare vowel (line 1's prāsa akshara)
    pollu_ok: frozenset | None = None  # a pāda head's pollu must be one of these (``TokenTable.pollu`` ids)


@dataclass(frozen=True)
class State:
    nfa: frozenset               # NFA states after every settled syllable
    pending: bool = False        # the last syllable is light and not yet settled
    prev: str = "start"          # "start" (of a pāda), "syl", "space" (a space or a sīsa half-break)
    unit: int = 0
    line: int = 0                # pādas finished in this unit
    syl_in_line: int = 0         # syllables written in this pāda
    syl_in_half: int = 0         # syllables written since the pāda or half began
    half_done: bool = False      # this pāda's half-break has been written
    half_open: bool = False      # the half-break was just written: the next syllable starts the second half
    head: int = -1               # token of the first syllable of this pāda / half (the వళి)
    head_ctx: tuple = ()         # its yati context (ft.yati_oracle)
    live: frozenset | None = None  # బహుయతి: head constituents that served every seat so far (None: no seat yet)
    last: int = -1               # the last syllable token written in this unit
    prev_line_last: int = -1     # the previous pāda's last syllable token (context of the next వళి)
    head_heavy: bool = False     # this pāda's first syllable is guru by itself
    head_pollu: int = 0          # the pollu on this pāda's first syllable (``TokenTable.pollu`` id)
    prasa_onset: tuple = ()      # line 1's prāsa onset, the head's pollu fused in (per unit)
    purva: str = ""              # line 1's pre-prāsa head weight, "U" / "I" (PRASA-PURVAKSHARA-01)
    prasa_key: int = -1          # line 1's prāsa key (per unit)
    prasa_bindu: bool = False    # line 1's first syllable carries a bindu (bindu-pūrvaka prāsa)
    first_bindu: bool = False    # this pāda's first syllable carries a bindu
    done: bool = False           # <eos> written


class Constraint:
    """Allowed-token masks and state updates for one metre.

    ``yati``: an ``ft.yati_oracle.YatiOracle`` (None: no yati penalty). ``vikalpa=False`` settles
    pending weights canonically (no ర-vattu or word-initial-conjunct alternatives), as the engines'
    canonical scansion does."""

    def __init__(self, label: str, tt: TokenTable, yati=None, vikalpa: bool = True):
        self.nfa = build_nfa(label)
        self.tt = tt
        self.cls = tt.cls
        self.yati = yati
        self.vikalpa = vikalpa
        self.has_halves = any(self.nfa.half_gana)

    def initial(self) -> State:
        return State(nfa=self.nfa.start)

    # ---- helpers --------------------------------------------------------------------
    def _settle(self, st: State, weights) -> frozenset:
        """NFA states after the pending syllable is read with any of ``weights``."""
        if not st.pending:
            return st.nfa
        out = set()
        for w in weights:
            out |= self.nfa.step(st.nfa, w)
        return frozenset(out)

    def _pending_weights(self, st: State, onset: int) -> tuple:
        if not self.vikalpa:
            return (U,) if st.prev == "syl" and onset != ONSET_PLAIN else (I,)
        if st.prev == "syl":
            return (U,) if onset == ONSET_CONJ else (U, I) if onset == ONSET_REPHA else (I,)
        return (I, U) if onset != ONSET_PLAIN else (I,)

    def _half_start(self, s: int) -> bool:
        p = self.nfa.place[s]
        return bool(p and self.nfa.half_gana[p.unit] and p.gana == self.nfa.half_gana[p.unit] and p.offset == 0)

    def _half_filter(self, states: frozenset, st: State) -> frozenset:
        """A sīsa's second half starts only after the half-break, and right after it."""
        if not self.has_halves:
            return states
        if st.half_open:
            return frozenset(s for s in states if self._half_start(s))
        return frozenset(s for s in states if not self._half_start(s))

    def _half_ok(self, states: frozenset) -> bool:
        """A sīsa half-break may come here: some parse is at the start of the pāda's second half."""
        return any(self._half_start(s) for s in states)

    def _at_yati(self, states: frozenset, st: State) -> bool:
        """Some live parse puts the next syllable on a yati."""
        for s in states:
            p = self.nfa.place[s]
            if p is None:
                continue
            ganas = self.nfa.yati_ganas[p.unit].get(p.slot, ())
            aks = self.nfa.yati_aksharas[p.unit].get(p.slot, ())
            if (p.gana in ganas and p.offset == 0) or (st.syl_in_line + 1) in aks:
                return True
        return False

    def _purva_head_classes(self, st: State) -> np.ndarray:
        """Weight classes the head of pāda 2+ may have: with a single-consonant prāsa, line 1's head
        weight; with a conjunct prāsa every head counts guru, so any."""
        ok = np.ones(6, bool)
        if len(st.prasa_onset) <= 1:
            ok[:3] = st.purva == I
            ok[3:] = st.purva == U
        return ok

    @functools.lru_cache(maxsize=4096)
    def _pollu_ok(self, onset: tuple) -> frozenset:
        """Pollus a pāda head may carry: its fused consonants are a prefix of line 1's prāsa onset and
        some syllable supplies the rest (a bare vowel when nothing is left)."""
        return frozenset(p for p, t in enumerate(self.tt.pollu_tuples)
                         if onset[:len(t)] == t and (onset[len(t):] or ("V",)) in self.tt.key_of)

    @functools.lru_cache(maxsize=4096)
    def _representative(self, c: int, bindu: int, pollu_ok: frozenset) -> int:
        """A syllable token of weight class ``c`` and this bindu whose pollu is allowed (-1: none)."""
        tt = self.tt
        rep = int(tt.representative[c, bindu])
        if rep >= 0 and int(tt.pollu[rep]) in pollu_ok:
            return rep
        cand = np.flatnonzero(tt.is_syl & (self.cls == c) & (tt.bindu == bool(bindu)) & np.isin(tt.pollu, list(pollu_ok)))
        return int(cand[0]) if len(cand) else -1

    def _seat_key(self, st: State) -> int:
        """The prāsa key the 2nd syllable of pāda 2+ must have, given its head's pollu (-1: none possible)."""
        rest = st.prasa_onset[len(self.tt.pollu_tuples[st.head_pollu]):]
        return self.tt.key_of.get(rest or ("V",), -1)

    # ---- the mask -----------------------------------------------------------------------
    def spec(self, st: State) -> "Spec":
        """What may come next, as a few numbers (turned into a vocabulary mask by ``mask_of`` or,
        batched on the GPU, by the decoder)."""
        if st.done:
            return Spec(np.zeros(6, bool), False, False, True, -1, False, None)
        ok_cls = self._classes(st)
        prasa, block, bindu, no_vowel, pollu_ok = -1, False, -1, False, None
        unit = self._unit_of(st)
        prasa_unit = self.nfa.prasa[unit]
        prasa_line = prasa_unit and st.line >= 1 and bool(st.prasa_onset)
        if prasa_line and st.syl_in_line == 0:                    # the pāda head: bindu, pollu, weight as line 1's
            bindu = int(st.prasa_bindu)
            pollu_ok = self._pollu_ok(st.prasa_onset)
            ok_cls = ok_cls & self.tt.bindu_classes[bindu]
            if st.purva:
                ok_cls = ok_cls & self._purva_head_classes(st)
            for c in np.flatnonzero(ok_cls):                      # ... and it must leave room for a prāsa syllable
                rep = self._representative(int(c), bindu, pollu_ok)
                nxt = self.spec(self.advance(st, rep)) if rep >= 0 else None
                if nxt is None or not (nxt.ok_cls.any() or nxt.space):
                    ok_cls[c] = False
        if prasa_unit and st.line == 0 and st.syl_in_line == 1:
            no_vowel = st.head_pollu == 0                         # PRASA-SAMA-01: no consonant, no prāsa
        if prasa_line and st.syl_in_line == 1:
            prasa = self._seat_key(st)
            if st.first_bindu != st.prasa_bindu or prasa < 0:  # the bindu before the prāsa must agree too
                block = True
            else:
                ok_cls = ok_cls & self.tt.key_classes[prasa]
        yati = None
        if self.yati is not None and st.head >= 0 and self._at_yati(self._settle(st, (I, U)), st):
            yati = (st.head, st.head_ctx, self.yati.after_ctx(st.last, st.prev != "syl"), st.live)
        space = nl = eos = False
        if st.prev == "syl":
            after = self._classes(replace(st, prev="space"))
            if prasa_line and st.syl_in_line == 1:
                after = after & self.tt.key_classes[prasa] if prasa >= 0 else np.zeros(6, bool)
            space = bool(after.any()) and not block                          # never a dead end
            settled = self._settle(st, (I, U))                   # pādānta: a final laghu may count as guru
            last_pada = unit == len(self.nfa.meters) - 1 and st.line + 1 >= self.nfa.padalu[unit]
            nl = (bool(self.nfa.step(settled, NL)) and not last_pada) or (not st.half_done and self._half_ok(settled))
            eos = self.nfa.accept in settled
        return Spec(ok_cls, space, nl, eos, prasa, block, yati, bindu, no_vowel, pollu_ok)

    def mask_of(self, sp: "Spec") -> tuple[np.ndarray, np.ndarray]:
        """(hard mask over the vocabulary, soft yati log-penalty) for one Spec."""
        tt = self.tt
        mask = np.zeros(len(tt.is_syl), bool)
        pen = np.zeros(len(tt.is_syl), np.float32)
        mask[tt.is_syl] = sp.ok_cls[self.cls[tt.is_syl]]
        if sp.block:
            mask &= ~tt.is_syl
        elif sp.prasa >= 0:
            mask &= (tt.prasa_key == sp.prasa) | ~tt.is_syl
        if sp.bindu >= 0:
            mask &= (tt.bindu == bool(sp.bindu)) | ~tt.is_syl
        if sp.no_vowel:
            mask &= ~tt.vowel_onset
        if sp.pollu_ok is not None:
            mask &= np.isin(tt.pollu, list(sp.pollu_ok)) | ~tt.is_syl
        if sp.yati is not None:
            pen[tt.is_syl & ~self.yati.row(*sp.yati)] = -1.0
        mask[tt.space], mask[tt.newline], mask[tt.eos] = sp.space, sp.nl, sp.eos
        return mask, pen

    def allowed(self, st: State) -> tuple[np.ndarray, np.ndarray]:
        return self.mask_of(self.spec(st))

    def _classes(self, st: State) -> np.ndarray:
        """Which of the 6 weight classes (3 * heavy + onset) may come next."""
        ok = np.zeros(6, bool)
        for onset in (ONSET_PLAIN, ONSET_CONJ, ONSET_REPHA):
            s1 = self._half_filter(self._settle(st, self._pending_weights(st, onset)), st)
            if not s1:
                continue
            ok[3 + onset] = bool(self.nfa.step(s1, U))
            ok[onset] = bool(self.nfa.step(s1, U) or self.nfa.step(s1, I))
        return ok

    def _unit_of(self, st: State) -> int:
        for s in st.nfa:
            p = self.nfa.place[s]
            if p is not None:
                return p.unit
        return st.unit

    # ---- the update -----------------------------------------------------------------------
    def advance(self, st: State, token: int) -> State:
        tt = self.tt
        if token == tt.eos:
            return replace(st, nfa=self._settle(st, (I, U)), pending=False, done=True)
        if token == tt.space:
            return replace(st, prev="space")
        if token == tt.newline:
            settled = self._settle(st, (I, U))
            end = self.nfa.step(settled, NL)
            if end:                                               # a pāda (or the main unit) ends
                unit_after = self._unit_of(replace(st, nfa=end))
                new_unit = unit_after != st.unit
                return replace(st, nfa=end, pending=False, prev="start", unit=unit_after,
                               line=0 if new_unit else st.line + 1, syl_in_line=0, syl_in_half=0,
                               half_done=False, half_open=False, head=-1, head_ctx=(), live=None, head_heavy=False,
                               last=-1 if new_unit else st.last, prev_line_last=-1 if new_unit else st.last,
                               head_pollu=0, prasa_key=-1 if new_unit else st.prasa_key,
                               prasa_onset=() if new_unit else st.prasa_onset, purva="" if new_unit else st.purva)
            # a sīsa half-break: like a word boundary for the weights; the second half has its own yati head
            return replace(st, prev="space", half_done=True, half_open=True, syl_in_half=0)
        onset = int(tt.onset[token])
        s1 = self._half_filter(self._settle(st, self._pending_weights(st, onset)), st)
        if tt.heavy[token]:
            nfa, pending = self.nfa.step(s1, U), False
        else:
            nfa, pending = s1, True
        head, head_ctx, live = st.head, st.head_ctx, st.live
        unit = self._unit_of(st)
        if st.syl_in_line == 0 or (st.syl_in_half == 0 and self.nfa.yati_group[unit] == "half"):
            head, live = token, None
            if self.yati is not None:
                head_ctx = (self.yati.line_head_ctx(st.prev_line_last, st.line == 0) if st.syl_in_line == 0
                            else self.yati.after_ctx(st.last, True))
        elif (self.yati is not None and self.nfa.yati_group[unit] == "bahu" and st.head >= 0
              and self._at_yati(self._settle(st, (I, U)), st)):          # a seat of the బహుయతి group
            seat_ctx = self.yati.after_ctx(st.last, st.prev != "syl")
            served = self.yati.served(st.head, st.head_ctx, token, seat_ctx, st.live)
            if served is not None:
                live = served if st.live is None else st.live & served
        pk, pb, purva, po = st.prasa_key, st.prasa_bindu, st.purva, st.prasa_onset
        fb = bool(tt.bindu[token]) if st.syl_in_line == 0 else st.first_bindu
        hh = bool(tt.heavy[token]) if st.syl_in_line == 0 else st.head_heavy
        hp = int(tt.pollu[token]) if st.syl_in_line == 0 else st.head_pollu
        if st.syl_in_line == 1 and st.line == 0:
            pk, pb = int(tt.prasa_key[token]), st.first_bindu
            po = tt.pollu_tuples[st.head_pollu] + tt.onset_of(token)
            if self.nfa.prasa[self._unit_of(st)]:
                purva = U if st.head_heavy else I
        return replace(st, nfa=nfa, pending=pending, prev="syl", syl_in_line=st.syl_in_line + 1,
                       syl_in_half=st.syl_in_half + 1, half_open=False, head=head, head_ctx=head_ctx, live=live, last=token,
                       head_heavy=hh, head_pollu=hp, prasa_key=pk, prasa_onset=po, prasa_bindu=pb, first_bindu=fb,
                       purva=purva)


def poem_budget(label: str) -> int:
    """Token room for a poem: the longest pādas, a space after every syllable (real poems average one
    per ~3 aksharas, but an untrained model spaces far more: at 1.5 x, 11 of 555 base-pilot poems ran
    out of room), and the line breaks (a sīsa's half-breaks included)."""
    total = 0
    for meter in label.split("+"):
        spec = dawg().spec(meter)
        total += spec.padalu * (2 * max(spec.aksharalu) + 1 + spec.halves_per_line)
    return total


def accepts(con: Constraint, ids: list[int]) -> tuple[bool, int]:
    """Teacher-forced check of a gold poem (token ids, ending with <eos>): (accepted, index of the
    first forbidden token or -1)."""
    st = con.initial()
    for k, t in enumerate(ids):
        mask, _ = con.allowed(st)
        if not mask[t]:
            return False, k
        st = con.advance(st, t)
    return True, -1


# -----------------------------------------------------------------------------
# the teacher-forced report (G0)
# -----------------------------------------------------------------------------
def main(argv=None) -> int:
    """Report teacher-forced acceptance of the gold eval poems and the yati verdict at their seats (G0)."""
    import argparse
    import collections
    import json

    from tokenizer import load_default

    from . import DATA_DIR
    from .yati_oracle import YatiOracle
    ap = argparse.ArgumentParser(description=main.__doc__)
    ap.add_argument("--data-dir", type=Path, default=DATA_DIR)
    ap.add_argument("--yati-profile", default="relaxed")
    ap.add_argument("--yati-sandhi", default="hypothesis")
    args = ap.parse_args(argv)
    tok = load_default()
    tt = build_token_table(tok)
    oracle = YatiOracle(tok, tt, args.yati_profile, args.yati_sandhi, cache_dir=args.data_dir / "yati_oracle")
    rep: dict = {"yati": {"profile": args.yati_profile, "sandhi": args.yati_sandhi}}
    for split in ("val", "test", "test_seen"):
        acc, yati_pos, yati_ok, poems_ok, n = collections.Counter(), 0, 0, 0, 0
        for line in (args.data_dir / "records" / f"{split}.jsonl").open(encoding="utf-8"):
            r = json.loads(line)
            if r["status"] != "agree":
                continue
            con = Constraint(r["meter_label"], tt, oracle)
            ids = tok.encode("\n".join(r["lines"])) + [tok.eos_id]
            ok, _ = accepts(con, ids)
            acc[ok] += 1
            st, p, q = con.initial(), 0, 0
            for t in ids:
                sp = con.spec(st)
                if sp.yati is not None and tt.is_syl[t]:
                    p += 1
                    q += bool(oracle.row(*sp.yati)[t])
                if not con.mask_of(sp)[0][t]:
                    break
                st = con.advance(st, t)
            yati_pos, yati_ok, poems_ok, n = yati_pos + p, yati_ok + q, poems_ok + (p == q), n + 1
        rep[split] = {"poems": n, "teacher_forced_accept": acc[True] / max(1, n),
                      "yati_positions_maitri": yati_ok / max(1, yati_pos), "poems_all_yati_maitri": poems_ok / max(1, n)}
        print(split, rep[split], flush=True)
    oracle.save()
    (args.data_dir / "constraints_report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
