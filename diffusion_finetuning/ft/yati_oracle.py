"""Exact yati verdicts for the decoder: which syllable tokens may stand at a yati seat (PLAN §6.2).

``yati.check(a, b)`` is an OR over reading pairs. Each akshara expands into readings (its consonants,
its vowel, detachments, sandhi hypotheses, printed-text evidence), and a pair of readings matches when
``pair_rule`` finds a positive rule whose status the profile accepts; two sandhi hypotheses may not
pair (except in the ``acchu`` mode). The readings of an akshara depend on its text and on its left
context:

- a preceding anusvāra (``pre_bindu``);
- a pollu న / ల on the previous syllable, which fuses into it (``prev_dead``);
- printed-text sandhi evidence (``yati.line.sandhi_evidence``): a word-initial akshara after ఁ, a
  word-initial lone న / య (not at the head of the first pāda), a ట / న augment inside a word after ఉ.

This module computes each token's readings once per context and the acceptance of each reading pair
once, and answers a seat as a gather over the token-reading incidence. The answer equals
``yati.check`` with the same context arguments and no word context. The lexical blockers and
triggers need the whole word, which is not yet written when the seat is decoded; on 919 gold
Bhāgavatam seats, leaving them out never accepted a seat the engine rejected in context (2026-09-29).

The decoder's earlier table called ``yati.check`` out of context with the default sandhi hypotheses
and widened it with pairs seen in gold poems; it accepted pairs such as త–య and త–హ that no poem
context supports (experiments/pilot_grid/README.md).
"""
from __future__ import annotations

import pickle
from dataclasses import astuple
from pathlib import Path

import numpy as np

import yati
from indic_meter_dawg import scansion as sc
from yati.akshara import parse_akshara
from yati.constants import RANK_CONSTITUENT, RANK_DETACH
from yati.pairing import pair_rule
from yati.readings import readings_for
from yati.ruleset import _rs

# A context: (pre_bindu, prev_dead, word_initial, prev_arasunna, prev_u_bare, first_pada_head)
Ctx = tuple
NO_CTX: Ctx = (False, (), True, False, False, False)


class YatiOracle:
    def __init__(self, tok, tt, profile: str = "relaxed", sandhi: str = "hypothesis",
                 cache_dir: Path | None = None):
        self.rs = _rs(None)
        if profile not in self.rs.profiles:
            raise ValueError(f"unknown yati profile {profile!r}")
        self.profile, self.sandhi = profile, sandhi
        self.V = len(tt.is_syl)
        self.syl = np.flatnonzero(tt.is_syl)
        id_to_piece = {i: s for s, i in tok.piece_to_id.items()}
        self.text = {int(i): id_to_piece[int(i)] for i in self.syl}
        self.feat = {}                       # token -> (onset, vowel, anusvara, candrabindu, dead న/ల)
        for i, t in self.text.items():
            a = sc.syllabify(t)[0]
            self.feat[i] = (tuple(a.onset), a.vowel, bool(a.anusvara), bool(a.candrabindu),
                            tuple(d for d in a.dead if d in ("న", "ల")))
        self.sigs: list = []                  # reading signature -> id
        self.sig_id: dict = {}
        self.reading: list = []               # one Reading object per signature
        self.acc: dict = {}                   # head signature id -> bool array over signatures (acceptance)
        self.incidence: dict = {}             # seat ctx -> (token ids, signature ids)
        self.rows: dict = {}                  # (head token, head ctx, seat ctx) -> bool over the vocabulary
        self.cache = (cache_dir / f"yati_oracle_{profile}_{sandhi}.pkl") if cache_dir else None
        if self.cache is not None and self.cache.exists():
            self._load()

    # ---- contexts -----------------------------------------------------------------------------
    def line_head_ctx(self, prev_line_last: int, first_pada: bool) -> Ctx:
        """The pāda head (వళి): the previous pāda's final pollu న/ల and ఁ carry over (YATI-SY-08)."""
        if prev_line_last >= 0:
            _, _, _, cb, dead = self.feat[prev_line_last]
            return (False, dead, True, cb, False, first_pada)
        return (False, (), True, False, False, first_pada)

    def after_ctx(self, prev_tok: int, word_initial: bool) -> Ctx:
        """An akshara inside a pāda, after syllable ``prev_tok`` (with a word boundary or not)."""
        if prev_tok < 0:
            return (False, (), word_initial, False, False, False)
        _, vowel, anus, cb, dead = self.feat[prev_tok]
        return (anus, dead, word_initial, cb and word_initial, vowel == "ఉ" and not anus and not word_initial, False)

    # ---- readings -----------------------------------------------------------------------------
    def _evidence(self, token: int, ctx: Ctx) -> tuple:
        """yati.line.sandhi_evidence for this token in this context."""
        onset, vowel, *_ = self.feat[token]
        _, _, word_initial, prev_arasunna, prev_u_bare, first_pada_head = ctx
        if not onset or not vowel:
            return ()
        if not word_initial:
            if len(onset) == 1 and onset[0] in ("ట", "న") and prev_u_bare:
                return ((vowel, RANK_DETACH, "టుగాగమ" if onset[0] == "ట" else "నుగాగమ"),)
            return ()
        out = []
        if prev_arasunna:
            out.append((vowel, RANK_CONSTITUENT, "printed split after ఁ"))
        if onset in (("న",), ("య",)) and not first_pada_head:
            out.append((vowel, RANK_DETACH, "word-initial న/య (drutam / యడాగమ)"))
        return tuple(out)

    def check_args(self, token: int, ctx: Ctx) -> dict:
        """The context arguments of yati.check for this akshara (one side, without the _a/_b suffix)."""
        return {"pre_bindu": ctx[0], "prev_dead": ctx[1], "evidence": self._evidence(token, ctx)}

    def _readings(self, token: int, ctx: Ctx) -> list[int]:
        a = parse_akshara(self.text[token], ctx[0], ctx[1], self.rs)
        out = []
        for r in readings_for(a, self.rs, sandhi=self.sandhi, evidence_vowels=self._evidence(token, ctx)):
            sig = (r.track, r.consonant, r.vowel, r.bindu, r.via, r.rank, r.hypothesis, r.detached,
                   r.unit_rule, r.status_override)
            if sig not in self.sig_id:
                self.sig_id[sig] = len(self.sigs)
                self.sigs.append(sig)
                self.reading.append(r)
            out.append(self.sig_id[sig])
        return out

    def _accepts(self, ra, rb) -> bool:
        both = ra.hypothesis and rb.hypothesis
        if both and self.sandhi != "acchu":
            return False
        m = pair_rule(ra, rb, self.rs)
        if not m.positive:
            return False
        status = self.rs.status("YATI-SV-02.10") if both else m.status
        return self.rs.accepted(self.profile, status)

    def _acc_row(self, a: int) -> np.ndarray:
        row = self.acc.get(a)
        n = len(self.sigs)
        if row is None or len(row) < n:
            old = 0 if row is None else len(row)
            ext = np.fromiter((self._accepts(self.reading[a], self.reading[b]) for b in range(old, n)), bool, n - old)
            row = ext if row is None else np.concatenate([row, ext])
            self.acc[a] = row
        return row

    def _incidence(self, ctx: Ctx) -> tuple[np.ndarray, np.ndarray]:
        inc = self.incidence.get(ctx)
        if inc is None:
            toks, sids = [], []
            for t in self.syl:
                for s in self._readings(int(t), ctx):
                    toks.append(int(t))
                    sids.append(s)
            inc = (np.asarray(toks, np.int64), np.asarray(sids, np.int64))
            self.incidence[ctx] = inc
        return inc

    # ---- the verdict ----------------------------------------------------------------------------
    def _head_readings(self, head: int, head_ctx: Ctx, live) -> list[int]:
        """The head's reading ids; with ``live`` (constituent indices), only readings of those
        constituents and vowel readings (index None, which serve any; YATI-SY-11)."""
        ra = self._readings(head, head_ctx)
        if live is None:
            return ra
        return [a for a in ra if self.reading[a].index is None or self.reading[a].index in live]

    def row(self, head: int, head_ctx: Ctx, seat_ctx: Ctx, live=None) -> np.ndarray:
        """Bool over the vocabulary: syllable tokens that satisfy yati with ``head`` at this seat.
        ``live``: in a బహుయతి group, the head constituents that served every earlier seat."""
        key = (head, head_ctx, seat_ctx, live)
        out = self.rows.get(key)
        if out is None:
            toks, sids = self._incidence(seat_ctx)
            ra = self._head_readings(head, head_ctx, live)
            v = np.zeros(len(self.sigs), bool)
            for a in ra:
                r = self._acc_row(a)
                v[: len(r)] |= r
            out = np.zeros(self.V, bool)
            out[toks[v[sids]]] = True
            self.rows[key] = out
        return out

    def ok(self, head: int, head_ctx: Ctx, seat: int, seat_ctx: Ctx, live=None) -> bool:
        return bool(self.row(head, head_ctx, seat_ctx, live)[seat])

    def constituents(self, head: int, head_ctx: Ctx) -> frozenset:
        """Indices of the head's onset constituents (a fused pollu included), as yati.line numbers them."""
        a = parse_akshara(self.text[head], head_ctx[0], head_ctx[1], self.rs)
        return frozenset(range(len(a.onset)))

    def served(self, head: int, head_ctx: Ctx, seat: int, seat_ctx: Ctx, live=None):
        """The head constituents through which ``seat`` is in maitri with ``head`` (None: a vowel reading
        of the head serves, which serves any constituent)."""
        rb = self._readings(seat, seat_ctx)
        out = set()
        for a in self._head_readings(head, head_ctx, live):
            r = self._acc_row(a)
            if any(b < len(r) and r[b] for b in rb):
                idx = self.reading[a].index
                if idx is None:
                    return None
                out.add(idx)
        return frozenset(out)

    # ---- cache ----------------------------------------------------------------------------------
    def save(self) -> None:
        if self.cache is None:
            return
        self.cache.parent.mkdir(parents=True, exist_ok=True)
        blob = {"sigs": self.sigs, "reading": [astuple(r) for r in self.reading],
                "acc": {a: np.packbits(r) for a, r in self.acc.items()},
                "acc_len": {a: len(r) for a, r in self.acc.items()}, "incidence": self.incidence}
        with self.cache.open("wb") as fh:
            pickle.dump(blob, fh)

    def _load(self) -> None:
        from yati.readings import Reading
        with self.cache.open("rb") as fh:
            blob = pickle.load(fh)
        self.sigs = blob["sigs"]
        self.sig_id = {s: i for i, s in enumerate(self.sigs)}
        self.reading = [Reading(*t) for t in blob["reading"]]
        self.acc = {a: np.unpackbits(p)[: blob["acc_len"][a]].astype(bool) for a, p in blob["acc"].items()}
        self.incidence = blob["incidence"]


def check_like_engine(oracle: YatiOracle, head: int, head_ctx: Ctx, seat: int, seat_ctx: Ctx) -> bool:
    """The same question asked of the engine directly (for tests)."""
    a, b = oracle.check_args(head, head_ctx), oracle.check_args(seat, seat_ctx)
    return yati.check(oracle.text[head], oracle.text[seat], oracle.profile, sandhi=oracle.sandhi,
                      pre_bindu_a=a["pre_bindu"], prev_dead_a=a["prev_dead"], evidence_a=a["evidence"],
                      pre_bindu_b=b["pre_bindu"], prev_dead_b=b["prev_dead"], evidence_b=b["evidence"]).matched
