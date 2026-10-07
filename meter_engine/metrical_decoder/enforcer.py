# -*- coding: utf-8 -*-
"""
The symbolic enforcer: which token texts keep a poem inside its meter.

State (:class:`DecodeState`, immutable and hashable):

* ``q`` — state of the meter's prosodic automaton (the minimal DFA over
  {U, I, ⏎} from ``indic_meter_dawg.prosody``) after every committed symbol,
  i.e. up to the start of the unfinished word;
* ``word`` — the unfinished word;
* ``lines`` — completed lines;
* ``ortho`` — the orthography automaton's state;
* ``line_syl`` — syllables of the current line before ``word``.

A word boundary finalises every weight of the word (``incremental``), a
newline also feeds ⏎. :meth:`Enforcer.step` returns None when the text can no
longer be completed into a poem of the meter. The automaton is trimmed, so a
missing transition *is* a dead state: IndicNeuroSym's dead-state detection
(Alg. 1, closed-form syllable bounds for dvipada) is not needed, for any meter.

Owns: :class:`DecodeState`, :class:`Enforcer`. Must not know about token ids
or models.
"""
from __future__ import annotations

from functools import lru_cache
from typing import NamedTuple, Optional

from .incremental import split_word, word_weights, is_boundary
from . import orthography as ortho
from .incremental import ENGINE_DIR  # noqa: F401  (puts meter_engine on sys.path)

from indic_meter_dawg import default_dawg                       # noqa: E402
from indic_meter_dawg.prosody import prosodic_automaton         # noqa: E402

NL = "\n"


class DecodeState(NamedTuple):
    q: int
    word: str
    lines: int
    ortho: int
    line_pat: str                 # committed U/I of the current line, up to the unfinished word
    # prāsa / yati registers (left at their defaults when they are off)
    line_text: str = ""           # the current line as written
    done: tuple = ()              # finished lines
    prasa_ok: bool = False        # this line's prāsa is verified
    ydone: int = 0                # yati groups of this line verified
    yowed: int = 0                # 1 while a failed group waits for its prāsa-yati akshara
    pdead: tuple = ()             # the previous line's final dead న / ల (context for the vaḷi)
    paras: bool = False           # the previous line ends in ఁ


class Enforcer:
    """Metrical constraints of one meter, as a token-text filter.

    ``prasa`` / ``yati`` add the engines' prāsa and yati verdicts to the gaṇa
    automaton (``registers.py``), under ``profile`` with yati sandhi off.
    ``inventory`` (``"verse"`` / ``"tokenizer"`` or an :class:`~.inventory.Inventory`) allows only
    attested syllables, in the filter and in the liveness test alike (:mod:`.inventory`); ``alphabet``
    (the model's single-character tokens) keeps only the syllables the model can write.

    >>> e = Enforcer("vidyunmala")                   # every akshara guru
    >>> s = e.step(e.initial(), "శ్రీ రామా")
    >>> e.step(s, "ము") is not None                  # ము may still become guru (ముం, ముల్ …)
    True
    >>> e.step(s, "ము ") is None                     # a finished ము is laghu
    True
    """

    def __init__(self, meter: str, units: int = 1, orthography: bool = True, prasa: bool = False,
                 yati: bool = False, profile: str = "strict", inventory=None, alphabet=None):
        dawg = default_dawg()
        self.meter = meter
        self.spec = dawg.spec(meter)
        self.dfa = prosodic_automaton(meter)
        self.units = units if self.spec.repeatable else 1
        self.n_lines = len(self.spec.slot_pattern) * self.units
        self.orthography = orthography
        self._trans = self.dfa.transitions
        self.registers = None
        if prasa or yati:
            from .registers import Registers
            self.registers = Registers(meter, prasa=prasa, yati=yati, profile=profile)
        self.inventory = None
        if inventory is not None:
            from .inventory import Inventory, load_inventory
            if isinstance(inventory, Inventory):
                self.inventory = inventory
            else:
                self.inventory = load_inventory(inventory, frozenset(alphabet)) if alphabet else load_inventory(inventory)
        self._config = dict(meter=meter, units=self.units, orthography=orthography, prasa=prasa, yati=yati,
                            profile=profile, inventory=self.inventory.name if self.inventory is not None else None,
                            alphabet=self.inventory.alphabet if self.inventory is not None else None)

    def config(self) -> dict:
        """The constructor's arguments: ``Enforcer(**e.config())`` behaves like ``e`` (worker processes)."""
        return dict(self._config)

    # ------------------------------------------------------------------ core
    def initial(self) -> DecodeState:
        return DecodeState(self.dfa.start, "", 0, ortho.START, "")

    def run(self, q: Optional[int], symbols: str) -> Optional[int]:
        """Automaton state after ``symbols`` (None when it dies)."""
        for ch in symbols:
            if q is None:
                return None
            q = self._trans.get(q, {}).get(ch)
        return q

    def step(self, state: DecodeState, text: str) -> Optional[DecodeState]:
        """Feed a token's text; None when the poem can no longer be completed."""
        q, word, lines, o, line_pat = state[:5]
        reg = self.registers
        line_text, done, carry = state.line_text, state.done, state
        for ch in text:
            if self.orthography:
                o = ortho.step(o, ch)
                if o is None:
                    return None
            if is_boundary(ch):
                if word:
                    if self.inventory is not None and not self.inventory.all_known(word):
                        return None                    # a syllable outside the inventory
                    w = word_weights(word)
                    q = self.run(q, w)
                    if q is None:
                        return None
                    line_pat += w
                    word = ""
                if ch == NL:
                    if lines + 1 >= self.n_lines:
                        return None                    # nothing may follow the last line
                    if reg is not None:                # every prāsa / yati check of the line must pass now
                        closed = reg.close_line(carry._replace(q=q, word="", lines=lines, ortho=o, line_pat=line_pat,
                                                               line_text=line_text, done=done))
                        if closed is None:
                            return None
                        carry = closed._replace(prasa_ok=False, ydone=0, yowed=0)
                        done, line_text = done + (line_text,), ""
                    q = self.run(q, NL)
                    if q is None:
                        return None
                    lines += 1
                    line_pat = ""
                    continue
            else:
                word += ch
            if reg is not None:
                line_text += ch
        new = carry._replace(q=q, word=word, lines=lines, ortho=o, line_pat=line_pat, line_text=line_text, done=done)
        if not self.alive(new):
            return None
        if reg is not None and line_text:
            new = reg.advance(new)                     # record the verdicts that are final now
        return new

    def alive(self, state: DecodeState) -> bool:
        """Some continuation still completes the poem (with the registers: in gaṇa, prāsa and yati at once)."""
        full_cluster = self.orthography and ortho.full_cluster(state.ortho)
        long_pollu = not self.orthography              # the filter forbids a word ending in 2+ dead consonants
        bare_pollu = not self.orthography              # … and a word of dead consonants alone
        if self.registers is not None:
            return self.registers.alive(self, state, cluster_can_grow=not full_cluster, long_pollu=long_pollu,
                                        bare_pollu=bare_pollu, inv=self.inventory)
        if not state.word:
            return True                                # q is live: the automaton is trimmed
        if self.inventory is not None:
            from .registers import continuations
            committed, _, _ = split_word(state.word, cluster_can_grow=not full_cluster, long_pollu=long_pollu)
            q2 = self.run(state.q, committed)
            return q2 is not None and any(
                self.run(q2, w) is not None
                for c in continuations(state.word, not full_cluster, long_pollu, bare_pollu, self.inventory)
                for w in c.weights)
        committed, options, _ = split_word(state.word, cluster_can_grow=not full_cluster, long_pollu=long_pollu)
        q2 = self.run(state.q, committed)
        return q2 is not None and any(self.run(q2, o) is not None for o in options)

    # ----------------------------------------------------------- line ends
    def flushed(self, state: DecodeState) -> Optional[int]:
        """Automaton state if the unfinished word ended here."""
        return self.run(state.q, word_weights(state.word)) if state.word else state.q

    def last_line(self, state: DecodeState) -> bool:
        return state.lines + 1 >= self.n_lines

    def line_complete(self, state: DecodeState) -> bool:
        """``has_accept``: ending the word here completes a legal line (the poem, on the last line),
        with the registers one whose prāsa and yati pass the whole-line check. The last line
        ends at EOS, not at ⏎, so this is where its check happens."""
        q2 = self.flushed(state)
        if q2 is None or (not state.line_pat and not state.word):
            return False
        if self.orthography and not ortho.can_end(state.ortho):
            return False                               # the word would end in two dead consonants
        if self.inventory is not None and state.word and not self.inventory.all_known(state.word):
            return False                               # a syllable outside the inventory
        if self.last_line(state):
            if not self.dfa.is_accepting(q2):
                return False
        elif self.run(q2, NL) is None:
            return False
        if self.registers is None:
            return True
        flushed = state._replace(q=q2, word="", line_pat=state.line_pat + (word_weights(state.word) if state.word else ""))
        return self.registers.close_line(flushed) is not None

    def must_end_line(self, state: DecodeState) -> bool:
        """The line is complete and cannot be extended: ⏎ (or the end) is the only continuation."""
        if not self.line_complete(state):
            return False
        q2 = self.flushed(state)
        return self.run(q2, "U") is None and self.run(q2, "I") is None

    def poem_complete(self, state: DecodeState) -> bool:
        return self.last_line(state) and self.line_complete(state)

    # ------------------------------------------------------------ reporting
    def akshara(self, state: DecodeState) -> int:
        """Syllables of the current line so far, the unfinished word included."""
        return len(state.line_pat) + (split_word(state.word).syllables if state.word else 0)

    def max_aksharas(self) -> int:
        """The longest poem of this meter (units included), in aksharas."""
        return _max_aksharas(self.meter) * self.units


@lru_cache(maxsize=None)
def _max_aksharas(meter: str) -> int:
    dawg = default_dawg()
    spec = dawg.spec(meter)
    best = 0
    for pattern in spec.slot_patterns:
        total = sum(sum(max(len(g.pattern) for g in alts) for alts in dawg.grammars[(meter, slot)].gana_positions)
                    for slot in pattern)
        best = max(best, total)
    return best


def line_lengths(meter: str, slot: str) -> tuple[int, int]:
    """Shortest and longest line of a slot, in aksharas.

    >>> line_lengths("utpalamala", "all"), line_lengths("dvipada", "all")
    ((20, 20), (11, 15))
    """
    g = default_dawg().grammars[(meter, slot)]
    return (sum(min(len(x.pattern) for x in alts) for alts in g.gana_positions),
            sum(max(len(x.pattern) for x in alts) for alts in g.gana_positions))
