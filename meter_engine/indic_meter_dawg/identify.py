# -*- coding: utf-8 -*-
"""
Top-level identification: lines in, ranked candidates out.

Owns: :class:`IdentificationResult`, ranking, variant handling, trailers
(seesam + gīta), the unknown report, and the plain-language explanation.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, replace
from typing import Optional, Sequence

from . import symbols
from . import scansion as sc
from .builder import LineDawg, default_dawg
from .parser import Segmentation, segment
from .stanza import StanzaMatch, match_stanza, stanza_failure
from .walker import Options, WalkResult, as_options, canonical, walk, walk_options


@dataclass(frozen=True)
class LineMatch:
    line_no: int                          # 1-based
    line: str
    slot: str
    segmentation: Segmentation            # canonical parse
    n_parses: int
    padanta_applied: bool


@dataclass(frozen=True)
class Candidate:
    meter: str
    name_te: str
    family: str
    lines: tuple[LineMatch, ...]
    is_variant_of: Optional[str]
    units: int
    padanta_lines: tuple[int, ...]
    trailer: Optional["Candidate"] = None       # the gīta after a seesam, when present
    notes: tuple[str, ...] = ()
    violations: tuple[str, ...] = ()            # stanza rules broken

    @property
    def label(self) -> str:
        return f"{self.meter}+{self.trailer.meter}" if self.trailer else self.meter

    @property
    def uses_padanta(self) -> bool:
        return bool(self.padanta_lines)

    def to_dict(self) -> dict:
        return {
            "meter": self.meter, "name_te": self.name_te, "family": self.family,
            "is_variant_of": self.is_variant_of, "units": self.units,
            "padanta_lines": [i + 1 for i in self.padanta_lines],
            "lines": [{"line_no": lm.line_no, "line": lm.line, "slot": lm.slot,
                       "ganas": list(lm.segmentation.gana_names),
                       "patterns": [s.pattern for s in lm.segmentation.segments],
                       "yati_aksharas": list(lm.segmentation.yati_aksharas),
                       "n_parses": lm.n_parses, "padanta_applied": lm.padanta_applied}
                      for lm in self.lines],
            "trailer": self.trailer.to_dict() if self.trailer else None,
            "notes": list(self.notes),
            "violations": list(self.violations),
        }


@dataclass(frozen=True)
class Failure:
    meter: str
    line_no: int              # 1-based
    akshara: Optional[int]    # 1-based, None when the problem is not inside a line
    reason: str
    lines_survived: int

    def to_dict(self) -> dict:
        return {"meter": self.meter, "line_no": self.line_no, "akshara": self.akshara,
                "reason": self.reason, "lines_survived": self.lines_survived}


@dataclass(frozen=True)
class IdentificationResult:
    lines: tuple[str, ...]
    candidates: tuple[Candidate, ...]         # ranked, best first
    ambiguous: bool
    failures: tuple[Failure, ...] = ()        # populated only when there is no candidate
    walks: tuple[WalkResult, ...] = field(default=(), repr=False)
    scansions: tuple = ()                     # LineScansion per line when identified from text
    notes: tuple[str, ...] = ()               # e.g. which vikalpa reading was needed

    @property
    def best(self) -> Optional[Candidate]:
        return self.candidates[0] if self.candidates else None

    @property
    def identified(self) -> bool:
        return bool(self.candidates)

    @property
    def meters(self) -> tuple[str, ...]:
        return tuple(c.label for c in self.candidates)

    def to_dict(self) -> dict:
        return {
            "lines": list(self.lines),
            "identified": self.identified,
            "ambiguous": self.ambiguous,
            "best": self.best.label if self.best else None,
            "candidates": [c.to_dict() for c in self.candidates],
            "failures": [f.to_dict() for f in self.failures],
            "scansions": [s.to_dict() for s in self.scansions],
            "notes": list(self.notes),
        }

    def to_json(self, **kw) -> str:
        kw.setdefault("ensure_ascii", False)
        kw.setdefault("indent", 2)
        return json.dumps(self.to_dict(), **kw)

    def explain(self) -> str:
        """Plain-language account of the verdict."""
        out = []
        for i, s in enumerate(self.scansions, start=1):
            out.append(f"  scan {i}. {s.format()}")
        for n in self.notes:
            out.append(f"  note: {n}")
        if not self.candidates:
            out.append(f"No meter matches these {len(self.lines)} lines.")
            for f in self.failures[:8]:
                out.append(f"  - {f.meter}: {f.reason}; survived {f.lines_survived} line(s)")
            return "\n".join(out)
        best = self.candidates[0]
        head = f"{best.label} ({best.name_te}, {best.family})"
        if self.ambiguous:
            others = ", ".join(c.label for c in self.candidates[1:] if not _related(c, best, self))
            head += f" — AMBIGUOUS with {others}; yati/prāsa needed to decide"
        out.append(head)
        for lm in best.lines:
            flag = " [pādānta laghu read as guru]" if lm.padanta_applied else ""
            alt = f" (+{lm.n_parses - 1} other parse(s))" if lm.n_parses > 1 else ""
            out.append(f"  {lm.line_no}. [{lm.slot}] {lm.segmentation.format()}{flag}{alt}")
        if best.trailer:
            out.append(f"  followed by {best.trailer.meter} ({best.trailer.name_te}):")
            for lm in best.trailer.lines:
                out.append(f"  {lm.line_no}. [{lm.slot}] {lm.segmentation.format()}")
        for n in best.notes:
            out.append(f"  note: {n}")
        if len(self.candidates) > 1:
            out.append("also possible: " + ", ".join(c.label for c in self.candidates[1:]))
        return "\n".join(out)


def _related(a: Candidate, b: Candidate, res: "IdentificationResult") -> bool:
    return a.is_variant_of == b.meter or b.is_variant_of == a.meter


def _line_matches(dawg: LineDawg, meter: str, lines: Sequence[str], slots: Sequence[str],
                  padanta_lines: Sequence[int], offset: int = 0,
                  walks: Sequence[WalkResult] = ()) -> tuple[LineMatch, ...]:
    out = []
    for i, (line, slot) in enumerate(zip(lines, slots)):
        if walks:
            line = walks[i].pattern_for((meter, slot))
        segs = segment(meter, slot, line, dawg=dawg, final_laghu_as_guru=True)
        if not segs:  # cannot happen after a stanza match; keep the invariant loud
            raise RuntimeError(f"{meter}/{slot} accepted {line!r} but no segmentation found")
        out.append(LineMatch(line_no=offset + i + 1, line=line, slot=slot, segmentation=segs[0],
                             n_parses=len(segs), padanta_applied=(i in padanta_lines) or segs[0].padanta_applied))
    return tuple(out)


def join_halves(lines: Sequence, h: int) -> tuple:
    """Concatenate every ``h`` consecutive printed lines into one pada
    (strings or per-akshara option tuples).

    >>> join_halves(["UI", "IU", "UU", "II"], 2)
    ('UIIU', 'UUII')
    >>> join_halves([("U", "I"), ("IU",), ("U",), ("I",)], 2)
    (('U', 'I', 'IU'), ('U', 'I'))
    """
    if h <= 1:
        return tuple(lines)
    out = []
    for i in range(0, len(lines), h):
        chunk = lines[i:i + h]
        out.append("".join(chunk) if isinstance(chunk[0], str) else sum((tuple(c) for c in chunk), ()))
    return tuple(out)


def _candidate(dawg: LineDawg, sm: StanzaMatch, lines: Sequence[str], offset: int = 0,
               trailer: Optional[Candidate] = None, halves: int = 1,
               walks: Sequence[WalkResult] = ()) -> Candidate:
    spec = dawg.spec(sm.meter)
    notes = []
    if spec.notes:
        notes.append(spec.notes)
    if halves > 1:
        notes.append(f"read as {len(lines)} padas printed as {halves} half-lines each")
    if sm.padanta_lines:
        notes.append("line-final laghu read as guru in line(s) " + ", ".join(str(i + 1) for i in sm.padanta_lines))
    for v in sm.violations:
        notes.append(f"stanza rule broken: {v}")
    return Candidate(meter=spec.name, name_te=spec.name_te, family=spec.family,
                     lines=_line_matches(dawg, spec.name, lines, sm.slots, sm.padanta_lines, offset, walks),
                     is_variant_of=spec.is_variant_of, units=sm.units, padanta_lines=sm.padanta_lines,
                     trailer=trailer, notes=tuple(notes), violations=sm.violations)


def rank_key(dawg: LineDawg, c: Candidate) -> tuple:
    """Clean matches first: no broken stanza rule, then fewer pādānta lines,
    then the deeper variant, then catalogue order."""
    depth = dawg.catalogue.variant_depth(c.meter)
    return (len(c.violations), len(c.padanta_lines), -depth, dawg.spec(c.meter).id)


def identify(lines: Sequence[str], dawg: Optional[LineDawg] = None, final_laghu_as_guru: bool = True,
             include_parents: bool = True) -> IdentificationResult:
    """Identify the meter of a stanza given as guru/laghu lines. A line is a
    U/I string, or a sequence of per-akshara options (``'U'``, ``'I'``,
    ``'UI'`` = canonical U but I admissible, ``'IU'``) when the scansion
    leaves a reading open; the result then reports the pattern actually
    accepted per line.

    >>> res = identify(["UIIUIUIIIUIIUIIUIUIU"] * 4)
    >>> res.best.meter, res.ambiguous
    ('utpalamala', False)
    >>> identify(["UIUUIUUIUUIU"] * 4).best.meter
    'sragvini'
    >>> identify([["U", "UI", "U", "U", "U", "U", "U", "U"]] * 4).best.meter
    'vidyunmala'
    """
    dawg = dawg or default_dawg()
    opts_lines = tuple(as_options(ln) for ln in lines if (ln if not isinstance(ln, str) else ln.strip()))
    opts_lines = tuple(o for o in opts_lines if o)
    lattice = any(len(o) > 1 for line in opts_lines for o in line)
    norm = tuple(canonical(o) for o in opts_lines)
    cache: dict = {}

    def walks_for(lns: Sequence) -> tuple[WalkResult, ...]:
        out = []
        for ln in lns:
            key = ln if isinstance(ln, str) else tuple(ln)
            if key not in cache:
                if isinstance(ln, str):
                    cache[key] = walk(ln, dawg=dawg, final_laghu_as_guru=final_laghu_as_guru)
                else:
                    cache[key] = walk_options(ln, dawg=dawg, final_laghu_as_guru=final_laghu_as_guru)
            out.append(cache[key])
        return tuple(out)

    if not lattice:
        opts_lines = norm          # plain strings: full death-point diagnostics

    walks = walks_for(opts_lines)
    cands: list[Candidate] = []

    def text_of(lns):
        return tuple(ln if isinstance(ln, str) else canonical(ln) for ln in lns)

    for spec in dawg.catalogue.concrete:
        if spec.repeatable:
            sm = match_stanza(spec, walks)
            if sm is not None:
                cands.append(_candidate(dawg, sm, norm, walks=walks))
            continue
        # a pada may be printed whole (h = 1) or as h half-lines (seesam); try each grouping
        for h in sorted({1, spec.halves_per_line}):
            head_n = spec.padalu * h
            if len(opts_lines) < head_n or (h > 1 and len(opts_lines) % h):
                continue
            head_lines = join_halves(opts_lines[:head_n], h)
            head_walks = walks_for(head_lines)
            head = match_stanza(spec, head_walks)
            if head is None:
                continue
            if len(opts_lines) == head_n:
                cands.append(_candidate(dawg, head, text_of(head_lines), halves=h, walks=head_walks))
                continue
            # composite: the meter's own lines followed by one of its trailers (seesam + gīta)
            if spec.followed_by:
                tail_lines = opts_lines[head_n:]
                tail_walks = walks_for(tail_lines)
                for tname in spec.followed_by:
                    tm = match_stanza(dawg.spec(tname), tail_walks)
                    if tm is not None:
                        trailer = _candidate(dawg, tm, text_of(tail_lines), offset=head_n, walks=tail_walks)
                        cands.append(_candidate(dawg, head, text_of(head_lines), trailer=trailer, halves=h,
                                                walks=head_walks))
    if not include_parents:
        variants = {c.is_variant_of for c in cands if c.is_variant_of}
        cands = [c for c in cands if c.meter not in variants]
    cands.sort(key=lambda c: rank_key(dawg, c))
    ambiguous = _is_ambiguous(dawg, cands)
    failures: tuple[Failure, ...] = ()
    if not cands:
        failures = _failures(dawg, walks, opts_lines, walks_for)
    return IdentificationResult(lines=norm, candidates=tuple(cands), ambiguous=ambiguous,
                                failures=failures, walks=walks)


READING_LEVELS = ("canonical", "vikalpa", "compound")


def reading_options(scans: Sequence[sc.LineScansion], level: str) -> tuple[Options, ...]:
    """Per-akshara options for a reading level:

    * ``canonical`` — the scanner's weights only;
    * ``vikalpa`` — also the other reading wherever the scanner recorded one
      (laghu before a word-initial conjunct, syllable before a ర-vattu conjunct);
    * ``compound`` — additionally, any guru that is guru *only* because a
      conjunct follows may be read laghu: the conjunct may begin a word
      inside a compound written without a space.

    >>> reading_options(sc.scan("స త్యము"), "vikalpa")
    (('IU', 'I', 'I'),)
    >>> reading_options(sc.scan("సత్యము"), "compound")
    (('UI', 'I', 'I'),)
    """
    if level not in READING_LEVELS:
        raise ValueError(f"unknown reading level {level!r}")
    out = []
    for s in scans:
        opts = []
        for syl in s.syllables:
            w = syl.weight
            alt = ""
            if level != "canonical" and syl.vikalpa:
                alt = syl.alternative_weight
            elif level == "compound" and syl.rules == ("samyukta",):
                alt = "I"
            opts.append(w + alt if alt and alt != w else w)
        out.append(tuple(opts))
    return tuple(out)


def identify_text(text, dawg: Optional[LineDawg] = None, policy: sc.ScanPolicy = sc.DEFAULT_POLICY,
                  try_variants: bool = True, final_laghu_as_guru: bool = True,
                  include_parents: bool = True) -> IdentificationResult:
    """Identify the meter of Telugu *text* (a string with one line per row,
    or a sequence of lines): scan to U/I, then identify. When the canonical
    scansion matches nothing and ``try_variants`` is on, the admissible
    alternative readings (vikalpa) are tried in order and the one that
    matches is reported in ``notes``.

    >>> res = identify_text(["శ్రీరాముని దయచేతను", "నారూఢిగ సకల జనులు నౌరా యనగా",
    ...                      "ధారాళమైన నీతులు", "నోరూరగ జవులు పుట్ట నుడివెద సుమతీ"])
    >>> res.best.meter
    'kandamu'
    """
    dawg = dawg or default_dawg()
    scans = sc.scan(text, policy)
    levels = READING_LEVELS if try_variants else READING_LEVELS[:1]
    res = None
    notes: list[str] = []
    for level in levels:
        opts = reading_options(scans, level)
        r = identify(opts, dawg, final_laghu_as_guru=final_laghu_as_guru, include_parents=include_parents)
        if res is None:
            res = r
        if r.identified:
            if level != "canonical":
                changed = _changed_aksharas(r, scans)
                why = ("an alternative reading (vikalpa)" if level == "vikalpa"
                       else "a compound-boundary reading (guru before a conjunct read as laghu)")
                notes.append(f"identified under {why} at " + (", ".join(changed) or "no akshara"))
            res = r
            break
    return replace(res, scansions=scans, notes=tuple(notes))


def _changed_aksharas(res: IdentificationResult, scans: Sequence[sc.LineScansion]) -> list[str]:
    """'line 3 akshara 7 (గ)' for every akshara whose accepted weight differs
    from the canonical scansion, in the best candidate."""
    out = []
    best = res.best
    if best is None:
        return out
    lines = list(best.lines) + (list(best.trailer.lines) if best.trailer else [])
    canon = [s.pattern for s in scans]
    accepted = [lm.line for lm in lines]
    # padas printed as halves: compare against the joined canonical text
    if len(accepted) != len(canon) and canon and len(canon) % max(len(accepted), 1) == 0:
        h = len(canon) // len(accepted)
        canon = ["".join(canon[i:i + h]) for i in range(0, len(canon), h)]
        texts = [sum((list(s.syllables) for s in scans[i:i + h]), []) for i in range(0, len(scans), h)]
    else:
        texts = [list(s.syllables) for s in scans]
    for i, (a, b) in enumerate(zip(canon, accepted)):
        for k, (x, y) in enumerate(zip(a, b)):
            if x != y:
                syl = texts[i][k].text if k < len(texts[i]) else "?"
                out.append(f"line {i + 1} akshara {k + 1} ({syl})")
    return out


def _is_ambiguous(dawg: LineDawg, cands: Sequence[Candidate]) -> bool:
    """True when two candidates of equal rank tier are not variant-related."""
    if len(cands) < 2:
        return False
    best = cands[0]
    tier = rank_key(dawg, best)[:2]
    for c in cands[1:]:
        if rank_key(dawg, c)[:2] != tier:
            continue
        if c.is_variant_of == best.meter or best.is_variant_of == c.meter:
            continue
        if c.is_variant_of and c.is_variant_of == best.is_variant_of:
            continue
        return True
    return False


def _failures(dawg: LineDawg, walks: Sequence[WalkResult], norm: Sequence[str] = (),
              walks_for=None) -> tuple[Failure, ...]:
    out = []
    for spec in dawg.catalogue.concrete:
        w = walks
        h = spec.halves_per_line
        if h > 1 and walks_for is not None and norm and len(norm) % h == 0 and len(norm) >= spec.padalu * h:
            w = walks_for(join_halves(norm, h)[:spec.padalu])       # judge the halved reading instead
        f = stanza_failure(spec, w)
        if f is None:
            continue
        line_no, idx, reason = f
        out.append(Failure(meter=spec.name, line_no=line_no + 1, akshara=(idx + 1) if idx is not None else None,
                           reason=reason, lines_survived=line_no))
    # most informative first: survived more lines, then failed later in the line;
    # line-count mismatches (no akshara) go last
    out.sort(key=lambda f: (-f.lines_survived, f.akshara is None, -(f.akshara or 0), f.meter))
    return tuple(out)
