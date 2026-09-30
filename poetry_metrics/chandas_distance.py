"""Metric 8 — chandas distance: how many aksharas must change for the poem to be in its meter.

What it measures. The smallest number of akshara edits that turns the poem into
one that keeps every rule of its meter: the weight pattern, the yati and the
prāsa. Full specification, sources and validation: specs/08_chandas_distance.md.

    weight edits   substitute   change the weight of an akshara (guru <-> laghu)
                   insert       add an akshara
                   delete       remove an akshara
    sound edits    yati         replace an akshara at a yati point that does not agree with its వళి
                   prasa        replace the second akshara of a pāda that does not rhyme with the others

Each costs 1.

    D = weight edits + yati edits + prāsa edits

Weights: the target is a language, not a string. A vṛtta has one weight pattern
per pāda; a jāti or upajāti meter has many (kandamu 80 and 320, a sīsa pāda
186,624). The distance of a line x to a meter is therefore

    d(x, L) = min over y in L of lev(x, y)

where L is the set of lines the meter's automaton accepts and lev is the
Levenshtein distance (1966). It is computed exactly, without listing L, by
dynamic programming over (akshara of the line, state of the automaton): the
method of Wagner (1974) for the nearest string of a regular language. The
automaton is meter_engine's, built from meter_rules.yaml, so every meter has
its own distance and no meter has its own code. Over the poem:

    weight edits = sum over pādas of d(pāda, its slot's language)
                   + the aksharas of a printed line that matches no pāda
                   + the shortest line of a pāda that no printed line matches

Yati and prāsa: once each pāda is aligned to its nearest valid line, the yati
points of that line are known (the catalogue gives them by akshara for a
vṛtta and by gaṇa otherwise), and meter_engine's yati and prāsa engines say
whether the aksharas standing there agree.

    yati edits  = yati points whose akshara does not agree with its వళి
    prāsa edits = the fewest pādas to change so that every pāda rhymes with one of them

An akshara that a weight edit already rewrites or inserts costs nothing more:
the same edit can choose its sound. So D is the number of aksharas touched.

    rate       r = D / max(n, N)          n = aksharas of the poem, N = of the nearest valid poem
    closeness  C = 1 - r                  1 = in meter
    skill      S = 1 - r / r_chance       1 = in meter, 0 = no nearer than unmetered text

r_chance is the mean rate of unmetered text (Pothana's prose) cut to the meter's
line lengths. It is what makes the distance comparable across meters: prose is
29 to 59 edits per 100 aksharas from a vṛtta and 12 to 23 from a jāti or upajāti
meter, which accepts many lines. S has the form of a chance-corrected agreement
(Cohen 1960).

Readings. Whatever meter_engine leaves open is free, as it is for the engine: an
akshara whose weight the tradition reads either way (before a ర-conjunct,
before a conjunct that opens the next word or a compound member). Yati and
prāsa are read under the engine's profile `relaxed` with the yati sandhi mode
`acchu`, the reading under which Pothana's yati holds; `--profile` and
`--yati-sandhi` choose another, and `--weights-only` leaves the sound out.

The end of a pāda. A laghu that closes a pāda is read as guru when the next
pāda opens with a conjunct: the conjunct makes it heavy across the break, as it
would inside a line. That is the only case in which Pothana's verse needs the
reading (1,847 of 1,847), and without it the treatise's own example of a broken
meter (4.36) would count as sound. meter_engine reads any closing laghu as
guru; `--padanta engine` does the same, and then the weight edits are 0 exactly
when the engine accepts the poem.

Rubric, on D and on r against the chance cut of the meter (the 5th percentile
of the rate of unmetered text, frozen in the baseline):
    4 exact       D = 0
    3 slip        r below the cut and D <= number of pādas (at most one edit a pāda on average)
    2 partial     r below half the cut
    1 weak        r below the cut
    0 unmetered   r at or above the cut: not told apart from prose cut to length

Usage:
    python3 chandas_distance.py score --meter kandamu --text "line 1\\nline 2\\n..."
    python3 chandas_distance.py score --text "..."                 # no meter given: the nearest one
    python3 chandas_distance.py score --dataset bhagavatam --no-lines --out outputs/chandas_bhagavatam.jsonl
    python3 chandas_distance.py build-baseline                     # rebuilds baselines/chandas_distance_baseline.json
    python3 chandas_distance.py validate                           # -> outputs/chandas_distance_validation.json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import islice, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "meter_engine"))

import prasa_engine                                                         # noqa: E402
import yati as yati_engine                                                  # noqa: E402
from indic_meter_dawg import automaton as au                                # noqa: E402
from indic_meter_dawg import default_dawg                                   # noqa: E402
from indic_meter_dawg import scansion as sc                                 # noqa: E402
from indic_meter_dawg.identify import reading_options                       # noqa: E402
from indic_meter_dawg.parser import segment                                 # noqa: E402

from common import corpus                                                   # noqa: E402
from common.scoring import add_source_arguments, read_poems, write_results  # noqa: E402

VERSION = "1.1"
LABELS = ("unmetered", "weak", "partial", "slip", "exact")
READING = "compound"            # the most permissive reading level of meter_engine; what it accepts at some level
MAX_READINGS = 64               # of a pāda with open aksharas, tried for its yati (meter_engine's own cap)
PADANTA = ("conjunct", "engine")    # a closing laghu is guru: before a conjunct of the next pāda | always
PROFILES = ("strict", "relaxed", "historical")          # meter_engine's profiles for prāsa and yati
YATI_SANDHI = ("off", "hypothesis", "acchu")            # how freely the yati engine may assume a sandhi


@dataclass(frozen=True)
class Reading:
    """How a poem is read: the closing laghu, and whether and how yati and prāsa are counted."""
    padanta: str = "conjunct"
    sound: bool = True               # count yati and prāsa edits as well as weight edits
    profile: str = "relaxed"         # with sandhi "acchu": the reading under which Pothana's yati holds (spec §3.5)
    sandhi: str = "acchu"

    @property
    def kind(self) -> str:
        """Which chance figures of the baseline apply."""
        return "all" if self.sound else "weights"


DEFAULT = Reading()
WEIGHTS_ONLY = Reading(sound=False)
CHANCE_PERCENTILE = 5
BASELINE_PATH = HERE / "baselines" / "chandas_distance_baseline.json"
OUTPUT_DIR = HERE / "outputs"
SEED = 42
INF = float("inf")
GURU, LAGHU = "U", "I"
# dataset metre labels -> the meter ids of the catalogue (meter_engine/scripts/corpus_run.NAME_MAP)
NAME_MAP = {"aataveladi": "ataveladi", "shardulavikriditamu": "sardulavikriditamu", "mattakokila": "mattakokilamu",
            "indravajramu": "indravajra", "upendravajramu": "upendravajra", "panchachamaramu": "pamcacamaramu"}


# ---------------------------------------------------------------------------
# one line against one slot of a meter
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Edit:
    op: str            # substitute | delete | insert (weights); yati | prasa | prasa_weight (sound)
    position: int      # 1-based akshara of the pāda; an insertion goes before it (n + 1 = at the end)
    akshara: str       # the akshara to change or delete; '' for an insertion
    weight: str        # the weight the meter needs there: U or I; '' when the weight is not at issue
    why: str = ""      # for a sound edit: what it fails to agree with

    def to_dict(self) -> dict:
        out = {"op": self.op, "position": self.position, "akshara": self.akshara, "needs": self.weight}
        return {**out, "why": self.why} if self.why else out


@dataclass(frozen=True)
class LineDistance:
    distance: int
    target: str                  # the nearest line the meter accepts, as U/I
    edits: tuple                 # Edit, in line order
    padanta: bool = False        # the final laghu was read as guru
    source: tuple = ()           # per akshara of `target`: the 0-based akshara of the line it is, None if inserted
    rewritten: frozenset = frozenset()   # 0-based aksharas of the line whose weight is changed

    def akshara_at(self, position: int):
        """The line's akshara (0-based) standing at a 1-based position of the nearest line; None when
        that place is filled by an edit, which can then be chosen to satisfy yati and prāsa as well."""
        k = self.source[position - 1] if 0 < position <= len(self.source) else None
        return None if k is None or k in self.rewritten else k


class Slot:
    """The automaton of one (meter, slot), prepared for the distance."""

    def __init__(self, dfa):
        self.start = dfa.start
        self.n = dfa.n_states
        self.accepting = frozenset(s for s in range(dfa.n_states) if dfa.is_accepting(s))
        edges = sorted((p, a, q) for p, row in dfa.transitions.items() for a, q in row.items())
        depth = {dfa.start: 0}                       # acyclic, so longest-path depth orders the states
        for _ in range(dfa.n_states):
            for p, _a, q in edges:
                if p in depth and depth.get(q, -1) < depth[p] + 1:
                    depth[q] = depth[p] + 1
        self.edges = tuple(sorted(edges, key=lambda e: (depth[e[0]], e)))      # sources in topological order
        reach = {dfa.start: 0}
        for p, _a, q in self.edges:
            if p in reach and reach.get(q, INF) > reach[p] + 1:
                reach[q] = reach[p] + 1
        self.shortest = min(reach[s] for s in self.accepting)                  # aksharas of the shortest line

    def distance(self, options: tuple, aksharas: tuple = (), padanta: bool = True) -> LineDistance:
        """Nearest accepted line to a line given as per-akshara weight options ('U', 'I', 'UI', 'IU')."""
        n = len(options)
        cost = [[INF] * self.n for _ in range(n + 1)]
        back = [[None] * self.n for _ in range(n + 1)]
        cost[0][self.start] = 0
        self._insertions(cost[0], back[0], 0)
        for i in range(1, n + 1):
            opt, prev, row, brow = options[i - 1], cost[i - 1], cost[i], back[i]
            for p, a, q in self.edges:               # read akshara i along an edge: free if the weight fits
                c = prev[p] + (0 if a in opt else 1)
                if c < row[q]:
                    row[q], brow[q] = c, (i - 1, p, "match" if a in opt else "substitute", a)
            for q in range(self.n):                  # or drop akshara i
                if prev[q] + 1 < row[q]:
                    row[q], brow[q] = prev[q] + 1, (i - 1, q, "delete", "")
            self._insertions(row, brow, i)
        best, end, final = INF, None, None
        for q in sorted(self.accepting):
            if cost[n][q] < best:
                best, end, final = cost[n][q], q, None
        if padanta and n and LAGHU in options[-1] and GURU not in options[-1]:
            for p, a, q in self.edges:               # the last akshara, a laghu, closes the pāda as a guru
                if a == GURU and q in self.accepting and cost[n - 1][p] < best:
                    best, end, final = cost[n - 1][p], q, (n - 1, p, "padanta", a)
        return self._trace(best, end, final, back, n, aksharas)

    def _insertions(self, row: list, brow: list, i: int) -> None:
        for p, a, q in self.edges:
            if row[p] + 1 < row[q]:
                row[q], brow[q] = row[p] + 1, (i, p, "insert", a)

    def _trace(self, best, end, final, back, n: int, aksharas: tuple) -> LineDistance:
        steps, i, q = [], n, end
        step = final or back[i][q]
        while step is not None:
            pi, pq, op, a = step
            steps.append((op, pi, a))
            i, q = pi, pq
            step = back[i][q]
        steps.reverse()
        target, edits, source, rewritten = [], [], [], set()
        for op, pi, a in steps:
            text = aksharas[pi] if pi < len(aksharas) else ""
            if op == "delete":
                edits.append(Edit("delete", pi + 1, text, ""))
                continue
            target.append(a)
            source.append(None if op == "insert" else pi)
            if op == "substitute":
                edits.append(Edit("substitute", pi + 1, text, a))
                rewritten.add(pi)
            elif op == "insert":
                edits.append(Edit("insert", pi + 1, "", a))
        return LineDistance(int(best), "".join(target), tuple(edits), bool(final), tuple(source), frozenset(rewritten))


@lru_cache(maxsize=None)
def slot(meter: str, name: str) -> Slot:
    return Slot(default_dawg().slot_dfas[(meter, name)])


# ---------------------------------------------------------------------------
# the poem against the meter
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Pada:
    """One row of the alignment: a pāda of the meter, the printed line(s) read as it, or only one of the two."""
    meter: str | None            # None: a printed line that matches no pāda
    slot: str | None
    text: str                    # '' when no printed line matches the pāda
    pattern: str
    line: LineDistance
    heavy_by_next: bool = False  # its closing laghu stands before a conjunct of the next printed line
    printed: tuple = ()          # the Scanned lines read as this pāda
    sound: tuple = ()            # Edit: the yati and prāsa edits of this pāda


@dataclass(frozen=True)
class PoemDistance:
    meter: str
    weights: int                 # edits that put every pāda in the meter's weight pattern
    n_aksharas: int              # of the poem
    target_aksharas: int         # of the nearest valid poem
    padas: tuple

    @property
    def yati(self) -> int:
        return sum(1 for p in self.padas for e in p.sound if e.op == "yati")

    @property
    def prasa(self) -> int:
        return sum(1 for p in self.padas for e in p.sound if e.op.startswith("prasa"))

    @property
    def distance(self) -> int:
        return self.weights + self.yati + self.prasa

    @property
    def rate(self) -> float:
        """Edits per akshara of the longer of the poem and its nearest valid poem."""
        longest = max(self.n_aksharas, self.target_aksharas)
        return self.distance / longest if longest else 0.0

    @property
    def n_padas(self) -> int:
        return sum(1 for p in self.padas if p.meter)

    def operations(self) -> dict:
        ops = {"substitute": 0, "insert": 0, "delete": 0}
        for p in self.padas:
            for e in p.line.edits:
                ops[e.op] += 1
        return ops


@dataclass(frozen=True)
class Scanned:
    """A printed line as the distance reads it."""
    text: str
    aksharas: tuple
    options: tuple
    pattern: str
    heavy_by_next: bool = False      # it ends in a laghu and the next line opens with a conjunct
    syllables: tuple = ()            # the scansion's syllables, for the yati engine


def scan(lines) -> tuple:
    scans = sc.scan(list(lines))
    options = reading_options(scans, READING)
    opens_with_conjunct = [s.syllables[0].is_conjunct for s in scans[1:]] + [False]
    return tuple(Scanned(s.text, s.aksharas, o, s.pattern, o[-1] == LAGHU and nxt, s.syllables)
                 for s, o, nxt in zip(scans, options, opens_with_conjunct))


def joined_options(lines: tuple) -> tuple:
    """The options of printed lines read as one pāda; a laghu before the next line's conjunct may be guru."""
    out = []
    for k, line in enumerate(lines):
        options = line.options
        if line.heavy_by_next and k < len(lines) - 1:
            options = options[:-1] + (LAGHU + GURU,)
        out.extend(options)
    return tuple(out)


def targets(meter: str, n_lines: int) -> list:
    """The pāda sequences a poem of this meter may have: [(meter, slot, printed lines per pāda)]."""
    dawg = default_dawg()
    spec = dawg.spec(meter)
    out = []
    for halves in sorted({1, spec.halves_per_line}):
        for pattern in spec.slot_patterns:
            unit = [(meter, s, halves) for s in pattern]
            if spec.repeatable:
                units = max(1, n_lines // (len(unit) * halves))
                out.extend(unit * k for k in sorted({units, units + 1}))
                continue
            out.append(unit)
            for trailer in spec.followed_by:          # సీసము is followed by a గీతి
                for tail in dawg.spec(trailer).slot_patterns:
                    out.append(unit + [(trailer, s, 1) for s in tail])
    return out


def _align(lines: tuple, target: list, cache: dict, padanta: str):
    """Printed lines against a pāda sequence: a line may match a pāda, or either may be left over."""
    n, m = len(lines), len(target)
    cost = [[INF] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    cost[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            here = cost[i][j]
            if here == INF:
                continue
            if j < m:
                meter, name, halves = target[j]
                if i + halves <= n:                                   # the pāda is printed as `halves` lines
                    key = (meter, name, i, halves)
                    if key not in cache:
                        joined = lines[i:i + halves]
                        cache[key] = slot(meter, name).distance(
                            joined_options(joined), sum((l.aksharas for l in joined), ()),
                            padanta=padanta == "engine" or joined[-1].heavy_by_next)
                    ld = cache[key]
                    if here + ld.distance < cost[i + halves][j + 1]:
                        cost[i + halves][j + 1] = here + ld.distance
                        back[i + halves][j + 1] = (i, j, ld)
                missing = slot(meter, name).shortest                  # no printed line for this pāda
                if here + missing < cost[i][j + 1]:
                    cost[i][j + 1], back[i][j + 1] = here + missing, (i, j, "pada")
            if i < n and here + len(lines[i].options) < cost[i + 1][j]:    # a printed line beyond the meter
                cost[i + 1][j], back[i + 1][j] = here + len(lines[i].options), (i, j, "line")
    rows, i, j = [], n, m
    while back[i][j] is not None:
        pi, pj, how = back[i][j]
        if how == "line":
            line = lines[pi]
            edits = tuple(Edit("delete", k + 1, a, "") for k, a in enumerate(line.aksharas))
            rows.append(Pada(None, None, line.text, line.pattern, LineDistance(len(edits), "", edits)))
        elif how == "pada":
            meter, name, _ = target[pj]
            ld = slot(meter, name).distance(())
            rows.append(Pada(meter, name, "", "", ld))
        else:
            meter, name, _ = target[pj]
            joined = lines[pi:i]
            rows.append(Pada(meter, name, " ".join(l.text for l in joined), "".join(l.pattern for l in joined), how,
                             joined[-1].heavy_by_next, tuple(joined)))
        i, j = pi, pj
    return cost[n][m], tuple(reversed(rows))


# ---------------------------------------------------------------------------
# yati and prāsa: aksharas that have the right weight and the wrong sound
# ---------------------------------------------------------------------------

def units(rows: tuple) -> list:
    """The matched pādas (indices into rows) grouped into the units that share a prāsa: a stanza,
    the gīti after a sīsamu, each unit of a repeatable meter."""
    out, seen = {}, {}
    for k, row in enumerate(rows):
        if row.meter is None:
            continue
        spec = default_dawg().spec(row.meter)
        j = seen.get(row.meter, 0)
        seen[row.meter] = j + 1
        if row.printed:
            out.setdefault((row.meter, j // len(spec.slot_pattern) if spec.repeatable else 0), []).append(k)
    return list(out.values())


def yati_groups(spec, seg) -> list:
    """The yati groups of a pāda, as 1-based aksharas of its nearest valid line. The grouping is that of
    meter_engine's yati.plan_from_candidate: సీసము has {1, g3} and {g5, g7}; a vṛtta with several yati
    points has one group; a meter that allows prāsa-yati has one pair per point."""
    ys = list(seg.yati_aksharas)
    if spec.halves_per_line == 2 and len(ys) == 2 and len(seg.segments) >= 5:
        return [(1, ys[0]), (seg.segments[4].start, ys[1])]
    if spec.system == "fixed" and not spec.prasa_yati and len(ys) > 1:
        return [tuple([1] + ys)]
    return [(1, y) for y in ys]


def pada_syllables(row: Pada) -> list:
    """The syllables of the printed line(s) of a pāda; half-lines are joined with their word ids kept apart."""
    out, shift = [], 0
    for line in row.printed:
        out.extend(replace(s, word=s.word + shift) for s in line.syllables)
        shift = max((s.word for s in out), default=-1) + 1
    return out


def divisions(row: Pada) -> list:
    """The ways a pāda may be divided into gaṇas at its weight distance: [(segmentation, akshara_at)].
    First the nearest line found. When the pāda needs no weight edit, also every other line of the meter
    that its open aksharas allow: the yati points of a jāti meter move with the division."""
    dawg = default_dawg()
    out = [(seg, row.line.akshara_at)
           for seg in segment(row.meter, row.slot, row.line.target, dawg=dawg, final_laghu_as_guru=False)]
    if row.line.distance:
        return out
    options = list(joined_options(row.printed))
    if row.line.padanta:
        options[-1] = GURU
    dfa = dawg.slot_dfas[(row.meter, row.slot)]
    for choice in islice(product(*options), MAX_READINGS):
        pattern = "".join(choice)
        if pattern != row.line.target and au.accepts(dfa, pattern):
            out.extend((seg, lambda position: position - 1)
                       for seg in segment(row.meter, row.slot, pattern, dawg=dawg, final_laghu_as_guru=False))
    return out


def yati_edits(rows: tuple, unit: list, profile: str, sandhi: str) -> dict:
    """{row: [Edit]} — one edit for each yati point whose akshara does not agree with its వళి, under
    the division of the pāda that needs the fewest. A point that a weight edit already rewrites is
    free: that edit can choose the sound too."""
    spec = default_dawg().spec(rows[unit[0]].meter)
    out, prev_dead, prev_aras = {}, (), False
    for n, k in enumerate(unit):
        row, syllables = rows[k], pada_syllables(rows[k])
        best = None
        for seg, akshara_at in divisions(row):
            edits = []
            for group in yati_groups(spec, seg):
                at = [akshara_at(p) for p in group]
                if any(a is None for a in at):
                    continue
                verdict = yati_engine.evaluate_line(
                    syllables, [tuple(a + 1 for a in at)], profile, prev_line_dead=prev_dead,
                    prev_line_ends_arasunna=prev_aras, first_pada=n == 0, allow_prasa_yati=spec.prasa_yati,
                    seesam_halves=len(row.printed) == 2 and spec.system != "fixed", sandhi=sandhi).groups[0]
                if not verdict.matched:
                    failing = [a for a, r in zip(at[1:], verdict.results) if not r.matched] or at[1:2]
                    edits.extend(Edit("yati", a + 1, syllables[a].text, "", f"no yati with {syllables[at[0]].text}")
                                 for a in failing)
            if best is None or len(edits) < len(best):
                best = edits
            if not best:
                break
        if best:
            out[k] = best
        last = syllables[-1]
        prev_dead = tuple(d for d in (last.dead or ()) if d in ("న", "ల"))
        prev_aras = bool(last.candrabindu)
    return out


# meter_engine's prāsa-yati fallback reads prasa_rules.yaml on every call (0.5 s); the rules do not
# change while a script runs, so they are read once here
prasa_engine.load_ruleset = lru_cache(maxsize=None)(prasa_engine.load_ruleset)


def prasa_edits(rows: tuple, unit: list, profile: str) -> dict:
    """{row: [Edit]} — the fewest pādas to change so that every pāda rhymes with one of them.
    A pāda whose first two aksharas a weight edit already touches is free."""
    meter = rows[unit[0]].meter
    if not default_dawg().spec(meter).prasa:
        return {}
    firm = [k for k in unit if rows[k].line.akshara_at(1) == 0 and rows[k].line.akshara_at(2) == 1]
    if len(firm) < 2:
        return {}
    rules = prasa_engine.load_ruleset()
    res = prasa_engine.evaluate([rows[k].text for k in firm], profile=profile, meter=meter, ruleset=rules)
    if res.error or not res.applicable:
        return {}
    rhymes = {}
    for pair in res.pairs:
        i, j = (x - 1 for x in pair["lines"])
        rhymes[i, j] = rhymes[j, i] = (not pair["hard_failures"]
                                       and all(rules.accepted(profile, rules.status(r)) for r in pair["rules_used"]))
    weights = [ln["purva_weight_positional"] for ln in res.lines]
    one_weight = not any(v["rule"].startswith("PRASA-PURVAKSHARA") for v in res.violations)
    best = None
    for r in range(len(firm)):                   # every pāda agrees with pāda r
        edits = {}
        for q in range(len(firm)):
            if q == r:
                continue
            if not rhymes[r, q]:
                edits.setdefault(firm[q], []).append(
                    Edit("prasa", 2, res.lines[q]["prasa"], "", f"no prāsa with {res.lines[r]['prasa']}"))
            if not one_weight and weights[q] != weights[r]:
                edits.setdefault(firm[q], []).append(
                    Edit("prasa_weight", 1, res.lines[q]["purva"], weights[r],
                         "the first aksharas of the pādas must have one weight"))
        if best is None or sum(map(len, edits.values())) < sum(map(len, best.values())):
            best = edits
    return best


def with_sound(rows: tuple, reading: Reading) -> tuple:
    found = {}
    for unit in units(rows):
        for edits in (yati_edits(rows, unit, reading.profile, reading.sandhi),
                      prasa_edits(rows, unit, reading.profile)):
            for k, es in edits.items():
                found.setdefault(k, []).extend(es)
    return tuple(replace(row, sound=tuple(found[k])) if k in found else row for k, row in enumerate(rows))


def poem_distance(lines, meter: str, reading: Reading = DEFAULT) -> PoemDistance:
    """The distance of the poem to one meter, with the nearest valid poem and the edits that reach it."""
    scanned = lines if lines and isinstance(lines[0], Scanned) else scan(lines)
    best, cache = None, {}
    for target in targets(meter, len(scanned)):
        cost, rows = _align(scanned, target, cache, reading.padanta)
        if best is None or cost < best[0]:
            best = (cost, rows)
    cost, rows = best
    if reading.sound and all(l.syllables for l in scanned):        # weight patterns alone carry no sound
        rows = with_sound(rows, reading)
    return PoemDistance(meter, int(cost), sum(len(l.options) for l in scanned),
                        sum(len(r.line.target) for r in rows), rows)


def skill(pd: PoemDistance, baseline: dict, kind: str = "all") -> float:
    """1 in meter, 0 when no nearer to the meter than unmetered text is."""
    return 1 - 100 * pd.rate / baseline["meters"][pd.meter][kind]["rate_mean"]


def nearest(lines, baseline: dict, reading: Reading = DEFAULT) -> PoemDistance:
    """The meter of the catalogue the poem is nearest to. The meter is chosen on the weights, by
    skill, so that a meter which accepts many lines is not favoured (ties: fewer edits, then the
    catalogue's order); the distance to it is then counted in full."""
    scanned = lines if lines and isinstance(lines[0], Scanned) else scan(lines)
    on_weights = replace(reading, sound=False)
    best = None
    for spec in default_dawg().catalogue.concrete:
        pd = poem_distance(scanned, spec.name, on_weights)
        key = (-skill(pd, baseline, "weights"), pd.distance)
        if best is None or key < best[0]:
            best = (key, pd)
    return poem_distance(scanned, best[1].meter, reading) if reading.sound else best[1]


# ---------------------------------------------------------------------------
# rubric and scoring
# ---------------------------------------------------------------------------

def level_of(distance: int, n_padas: int, rate: float, cut: float) -> int:
    """Rubric level 0-4; `rate` and `cut` in the same unit."""
    if distance == 0:
        return 4
    if rate >= cut:
        return 0
    if distance <= n_padas:
        return 3
    return 2 if rate < cut / 2 else 1


def load_baseline(path: Path = BASELINE_PATH) -> dict:
    if not path.exists():
        sys.exit(f"no baseline at {path}; run: python3 chandas_distance.py build-baseline")
    return json.loads(path.read_text(encoding="utf-8"))


def score_poem(lines, baseline: dict, meter: str | None = None, reading: Reading = DEFAULT) -> dict:
    pd = poem_distance(lines, meter, reading) if meter else nearest(lines, baseline, reading)
    chance = baseline["meters"][pd.meter][reading.kind]
    rate = 100 * pd.rate
    level = level_of(pd.distance, pd.n_padas, rate, chance["rate_cut"])
    ops = pd.operations()
    return {
        "metric": "chandas_distance", "version": VERSION, "score": level,
        "meter": pd.meter, "meter_given": bool(meter),
        "distance": pd.distance, "weight_edits": pd.weights, "yati_edits": pd.yati, "prasa_edits": pd.prasa,
        "edits_per_100_aksharas": round(rate, 2),
        "closeness": round(1 - pd.rate, 4), "skill": round(skill(pd, baseline, reading.kind), 4),
        "level": level, "label": LABELS[level],
        "chance_rate_mean": chance["rate_mean"], "chance_rate_cut": chance["rate_cut"],
        "substitutions": ops["substitute"], "insertions": ops["insert"], "deletions": ops["delete"],
        "n_aksharas": pd.n_aksharas, "target_aksharas": pd.target_aksharas, "n_padas": pd.n_padas,
        "n_lines": len(pd.padas),
        "reading": {"padanta": reading.padanta, "yati_and_prasa": reading.sound,
                    "profile": reading.profile, "yati_sandhi": reading.sandhi},
        "lines": [{"text": p.text, "meter": p.meter, "slot": p.slot, "pattern": p.pattern,
                   "target": p.line.target, "distance": p.line.distance + len(p.sound), "padanta": p.line.padanta,
                   "edits": [e.to_dict() for e in p.line.edits + p.sound]} for p in pd.padas],
    }


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def score(args) -> None:
    baseline = load_baseline()
    reading = Reading(args.padanta, not args.weights_only, args.profile, args.yati_sandhi)
    if args.dataset and not args.meter:                       # a dataset poem is scored against its own label
        labels = {p.key: NAME_MAP.get(p.metre, p.metre) for p in corpus.load(args.dataset)}
        known = {m.name for m in default_dawg().catalogue.concrete}
        poems = [(key, (lines, labels[key] if labels[key] in known else None)) for key, lines in read_poems(args)]
        write_results(args, poems, lambda item: score_poem(item[0], baseline, item[1], reading))
        return
    write_results(args, read_poems(args), lambda lines: score_poem(lines, baseline, args.meter, reading))


def build_baseline(args) -> None:
    import validation_chandas_distance          # the chance text is built there
    validation_chandas_distance.build_baseline(args)


def validate(args) -> None:
    import validation_chandas_distance          # analysis, kept out of the metric itself
    validation_chandas_distance.run(args)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description="chandas distance metric")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("score", help="score poems")
    add_source_arguments(s)
    s.add_argument("--meter", help="the meter to measure against (default: the dataset label, else the nearest meter)")
    s.add_argument("--padanta", choices=PADANTA, default=DEFAULT.padanta,
                   help="a laghu closing a pāda is guru: before a conjunct of the next pāda (default) | always, as the engine")
    s.add_argument("--weights-only", action="store_true", help="do not count yati and prāsa edits")
    s.add_argument("--profile", choices=PROFILES, default=DEFAULT.profile, help="meter_engine's profile for yati and prāsa")
    s.add_argument("--yati-sandhi", choices=YATI_SANDHI, default=DEFAULT.sandhi,
                   help="how freely the yati engine may assume a sandhi at a yati point")
    s.set_defaults(func=score)

    b = sub.add_parser("build-baseline", help="the chance distribution of the distance, per meter")
    b.add_argument("--seed", type=int, default=SEED)
    b.set_defaults(func=build_baseline)

    v = sub.add_parser("validate", help="agreement with meter_engine, the edit ladder, chance, corpora")
    v.add_argument("--seed", type=int, default=SEED)
    v.set_defaults(func=validate)

    args = ap.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
