# -*- coding: utf-8 -*-
"""
Data behind the DAWG walk-through page (``/dawg``).

Two payloads, both plain JSON:

* :func:`graph_payload` — the line-level DAWG of ``indic_meter_dawg`` (the
  minimized, labelled DFA every pāda is identified with) as nodes, edges and
  a 3D layout: x is the longest-path depth from the start state, and each
  depth layer is a ring whose order is untangled by barycentre sweeps.
* :func:`trace_payload` — one poem read akshara by akshara through that same
  DFA: after every akshara, the frontier state(s), the edges taken, which
  (metre, slot) hypotheses are still alive, which died there, and where each
  live hypothesis stands inside its gaṇa template; at the end of each pāda,
  the accept labels and the pādānta reading; at the end, the stanza verdict
  of ``identify_text`` (the call ``chandohasam.analyze`` makes).

Nothing is re-implemented: the walk steps ``dawg.dfa``, liveness is
``dawg.reachable``, the reading level is the first of ``READING_LEVELS``
that identifies the poem (as in ``identify_text``), and seesam half-lines
are joined exactly as the best candidate read them.
"""
from __future__ import annotations

import math
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Optional, Sequence

ENGINE_DIR = Path(__file__).resolve().parent.parent / "meter_engine"
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

# the top-level package name, so that the DAWG cache is the one chandohasam uses
from indic_meter_dawg import automaton as au                                    # noqa: E402
from indic_meter_dawg import default_dawg, identify, identify_text              # noqa: E402
from indic_meter_dawg import scansion as sc                                     # noqa: E402
from indic_meter_dawg.identify import READING_LEVELS, reading_options           # noqa: E402
from indic_meter_dawg.stanza import stanza_failure                              # noqa: E402
from indic_meter_dawg.walker import WalkResult                                  # noqa: E402

LAYER_GAP = 2.6          # world units between depth layers
RING_SPACING = 0.55      # arc length between neighbouring nodes of a ring
SWEEPS = 6               # barycentre sweeps (forward + backward each)

EXAMPLES = [
    {"id": "kandamu", "title": "కందము — పలికెడిది భాగవతమఁట (Pōtana)",
     "text": "పలికెడిది భాగవత మఁట,\n"
             "పలికించెడివాడు రామభద్రుం డఁట, నేఁ\n"
             "బలికిన భవహర మగునఁట,\n"
             "పలికెద, వేఱొండు గాథ బలుకఁగ నేలా?"},
    {"id": "kandamu-vikalpa", "title": "కందము, vikalpa reading — మన్నాఁడవు చిరకాలము (Bhāgavatam 1.43)",
     "text": "మన్నాఁడవు చిరకాలము,\n"
             "గన్నాఁడవు పెక్కులైనగ్రంథార్థంబుల్,\n"
             "విన్నాఁడవు వినఁదగినవి,\n"
             "యున్నాఁడవు పెద్దలొద్దనుత్తమగోష్ఠిన్."},
    {"id": "utpalamala", "title": "ఉత్పలమాల — ఎవ్వనిచే జనించు (Bhāgavatam 8.73)",
     "text": "ఎవ్వనిచే జనించు జగ; మెవ్వని లోపల నుండు లీనమై;\n"
             "యెవ్వని యందు డిందుఁ; బరమేశ్వరుఁ డెవ్వఁడు; మూలకారణం\n"
             "బెవ్వఁ; డనాదిమధ్యలయుఁ డెవ్వఁడు; సర్వముఁ దానయైన వాఁ\n"
             "డెవ్వఁడు; వాని నాత్మభవు నీశ్వరు నే శరణంబు వేడెదన్."},
    {"id": "sardula", "title": "శార్దూలము — శ్రీకైవల్య పదంబుఁ (Bhāgavatam 1.1)",
     "text": "శ్రీకైవల్య పదంబుఁ జేరుటకునైచింతించెదన్ లోక ర\n"
             "క్షైకారంభకు, భక్త పాలన కళాసంరంభకున్, దానవో\n"
             "ద్రేకస్తంభకుఁ, గేళి లోల విలసద్దృగ్జాల సంభూత నా\n"
             "నాకంజాత భవాండ కుంభకు, మహానందాంగనాడింభకున్."},
    {"id": "champakamala", "title": "చంపకమాల — అలసులు, మందబుద్దియుతు (Bhāgavatam 1.44)",
     "text": "అలసులు, మందబుద్దియుతు,లల్పతరాయువు, లుగ్రరోగసం\n"
             "కలితులు, మందభాగ్యులు సుకర్మము లెవ్వియుఁ జేయఁజాల రీ\n"
             "కలియుగమందు మానవులు;గావున నెయ్యది సర్వసౌఖ్యమై\n"
             "యలవడు? నేమిటం బొడమునాత్మకు? శాంతి, మునీంద్ర! చెప్పవే."},
    {"id": "tetagiti", "title": "తేటగీతి — చేతులారంగ శివునిఁ (Bhāgavatam 1.14)",
     "text": "చేతులారంగ శివునిఁ బూజింపఁడేని,\n"
             "నోరు నొవ్వంగ హరికీర్తినుడువఁడేని,\n"
             "దయయు సత్యంబు లోనుగాఁదలఁపఁడేనిఁ,\n"
             "గలుగ నేటికిఁ దల్లులకడుపుఁ జేటు."},
    {"id": "seesamu", "title": "సీసము + ఆటవెలది — మెఱుఁగు చెంగట (Bhāgavatam 1.16)",
     "text": "మెఱుఁగు చెంగటనున్నమేఘంబు కైవడి-\n"
             "నువిద చెంగట నుండనొప్పువాఁడు,\n"
             "చంద్రమండల సుధాసారంబు పోలిక-\n"
             "ముఖమునఁ జిఱునవ్వుమొలచువాఁడు,\n"
             "వల్లీయుత తమాలవసుమతీజము భంగిఁ-\n"
             "బలువిల్లు మూఁపునఁబరఁగువాఁడు,\n"
             "నీలనగాగ్ర సన్నిహిత భానుని భంగి-\n"
             "ఘన కిరీటము దలఁగలుగువాఁడు,\n"
             "పుండరీకయుగముఁబోలు కన్నుల వాఁడు,\n"
             "వెడఁద యురమువాఁడు,విపులభద్ర\n"
             "మూర్తివాఁడు, రాజముఖ్యుఁ డొక్కరుఁడు నా\n"
             "కన్నుఁగవకు నెదురఁగానఁబడియె."},
    {"id": "generated-v1", "title": "ఉత్పలమాల, generated — Gemma-4 E4B under the v1 constraint (run 2026-09-24)",
     "note": "experiments/runs/2026-09-24_e4b_constrained, key utpalamala|T1|masking_only|70: in metre, "
             "but with aksharas real verse never writes — what the v2 layers catch",
     "text": "తల్లికరుణ్యమున్రు మధుదైవమునందు నిలిచ్యెనుత్యెనుం\n"
             "అల్లొనమల్లెలొన్యెను మృహాగతమున్రు సకల్రజన్యముం\n"
             "తల్లిపరివ్రతమ్మున నిధయ్యెను దైవమునందు నివ్రమెన్\n"
             "కల్లమలక్రియేన నిలకడ్యెను కమ్యమునందు నిత్యముం"},
    {"id": "mattakokila", "title": "మత్తకోకిల — బల్లిదుం డగు కంసుచేతను (Bhāgavatam 1.190)",
     "text": "బల్లిదుం డగు కంసుచేతను బాధ నొందుచు నున్న మీ\n"
             "తల్లిఁ గాచిన భంగిఁ గాచితి ధార్తరాష్ట్రులచేత నేఁ\n"
             "దల్లడంబునఁ జిక్కకుండఁగఁ దావకీన గుణవ్రజం\n"
             "బెల్ల సంస్తుతి సేసి చెప్పఁగ నెంతదాన, జగత్పతీ!"},
]


# -----------------------------------------------------------------------------
# 1. the graph and its layout
# -----------------------------------------------------------------------------
def _hypotheses(dawg) -> list[dict]:
    out = []
    for i, (meter, slot) in enumerate(dawg.hypotheses):
        spec = dawg.spec(meter)
        out.append({"id": i, "meter": meter, "slot": slot, "name_te": spec.name_te,
                    "family": spec.family, "n_slots": len(spec.slots)})
    return out


def _depths(dfa) -> dict[int, int]:
    """Longest-path depth from the start state, so every edge points forward."""
    depth = {dfa.start: 0}
    for s in au.topological_order(dfa):
        for d in dfa.transitions.get(s, {}).values():
            depth[d] = max(depth.get(d, 0), depth[s] + 1)
    return depth


def _circular_mean(angles: Sequence[float]) -> Optional[float]:
    if not angles:
        return None
    return math.atan2(sum(math.sin(a) for a in angles), sum(math.cos(a) for a in angles))


def _ring_angles(dfa, layers: dict[int, list[int]]) -> dict[int, float]:
    """Order every ring by the circular barycentre of its neighbours, sweeping
    forward over predecessors and backward over successors."""
    preds: dict[int, list[int]] = {}
    succs: dict[int, list[int]] = {}
    for s, row in dfa.transitions.items():
        for d in row.values():
            preds.setdefault(d, []).append(s)
            succs.setdefault(s, []).append(d)
    angle: dict[int, float] = {}
    for nodes in layers.values():
        for i, s in enumerate(nodes):
            angle[s] = 2 * math.pi * i / len(nodes)

    def place(nodes: list[int], neighbours: dict[int, list[int]]) -> None:
        n = len(nodes)
        if n < 2:
            return
        target = {s: _circular_mean([angle[t] for t in neighbours.get(s, ())]) for s in nodes}
        target = {s: (angle[s] if a is None else a) for s, a in target.items()}
        ordered = sorted(nodes, key=lambda s: target[s] % (2 * math.pi))
        step = 2 * math.pi / n
        # rotate the evenly spaced ring onto the targets
        phase = _circular_mean([target[s] - i * step for i, s in enumerate(ordered)]) or 0.0
        for i, s in enumerate(ordered):
            angle[s] = phase + i * step

    depths = sorted(layers)
    for _ in range(SWEEPS):
        for d in depths[1:]:
            place(layers[d], preds)
        for d in reversed(depths[:-1]):
            place(layers[d], succs)
    return angle


def _family_of(dawg, reach: frozenset) -> str:
    families = {dawg.spec(m).family for m, _ in reach}
    return families.pop() if len(families) == 1 else "mixed"


@lru_cache(maxsize=1)
def graph_payload() -> dict:
    """Nodes (with x, y, z), edges and hypotheses of the default DAWG."""
    dawg = default_dawg()
    dfa = dawg.dfa
    hid = {h: i for i, h in enumerate(dawg.hypotheses)}
    depth = _depths(dfa)
    layers: dict[int, list[int]] = {}
    for s in sorted(depth):
        layers.setdefault(depth[s], []).append(s)
    angle = _ring_angles(dfa, layers)
    max_depth = max(layers)
    nodes = []
    for s in range(dfa.n_states):
        d = depth[s]
        n = len(layers[d])
        r = 0.0 if n == 1 else max(0.8, n * RING_SPACING / (2 * math.pi))
        reach = dawg.reachable.get(s, frozenset())
        nodes.append({
            "id": s, "depth": d,
            "x": round((d - max_depth / 2) * LAYER_GAP, 3),
            "y": round(r * math.cos(angle[s]), 3),
            "z": round(r * math.sin(angle[s]), 3),
            "accept": sorted(hid[h] for h in dfa.labels.get(s, frozenset())),
            "reach": sorted(hid[h] for h in reach),
            "family": _family_of(dawg, reach),
            "meters": len({m for m, _ in reach}),
        })
    edges = [[s, sym, d] for s, row in sorted(dfa.transitions.items()) for sym, d in sorted(row.items())]
    stats = dawg.stats()
    return {
        "start": dfa.start,
        "hypotheses": _hypotheses(dawg),
        "nodes": nodes,
        "edges": edges,
        "layers": max_depth + 1,
        "stats": {"states": dfa.n_states, "edges": len(edges), "hypotheses": len(dawg.hypotheses),
                  "meters": stats["meters"], "distinct_lines": stats["distinct_lines"],
                  "nfa_states": stats["nfa_states"], "dfa_states_unminimized": stats["dfa_states_unminimized"],
                  "max_line_length": stats["max_line_length"]},
    }


# -----------------------------------------------------------------------------
# 2. where a hypothesis stands inside its gaṇa template
# -----------------------------------------------------------------------------
# A position is (gaṇa index k, alternative j, symbols read i): i == 0 means
# "about to begin gaṇa k" (j unused, -1); k == number of gaṇas means the line
# is complete. This is the strict grammar's nonterminal (G3_UUI_2 = gaṇa 3,
# alternative UUI, two read), kept structured so the page can draw it.
def _advance(alts, positions: set, symbol: str) -> set:
    out = set()
    n = len(alts)
    for k, j, i in positions:
        if k >= n:
            continue
        cands = range(len(alts[k])) if i == 0 else (j,)
        for jj in cands:
            pat = alts[k][jj].pattern
            if pat[i] != symbol:
                continue
            out.add((k + 1, -1, 0) if i + 1 == len(pat) else (k, jj, i + 1))
    return out


def _describe(alts, positions: set) -> list[dict]:
    out = []
    n = len(alts)
    for k, j, i in sorted(positions):
        if k >= n:
            out.append({"done": True, "ganas": n})
        elif i == 0:
            out.append({"gana": k + 1, "of": n, "next": [g.telugu for g in alts[k]], "read": 0})
        else:
            g = alts[k][j]
            out.append({"gana": k + 1, "of": n, "te": g.telugu, "pattern": g.pattern, "read": i,
                        "len": len(g.pattern)})
    return out


# -----------------------------------------------------------------------------
# 3. one pāda through the DFA
# -----------------------------------------------------------------------------
def _walk_unit(dawg, hid: dict, options: tuple, syllables: list, printed: list[int], text: str,
               unit_no: int) -> dict:
    dfa = dawg.dfa
    all_h = list(dawg.hypotheses)
    alts = {h: dawg.grammars[h].gana_positions for h in all_h}
    pos = {h: {(0, -1, 0)} for h in all_h}
    frontier = [dfa.start]
    alive = set(all_h)
    steps = []
    died_at: dict = {}
    death_step = None
    for k, opt in enumerate(options):
        edges = []
        nxt: list[int] = []
        for s in frontier:
            for sym in opt:
                d = dfa.step(s, sym)
                if d is not None:
                    edges.append([s, sym, d])
                    if d not in nxt:
                        nxt.append(d)
        pos = {h: set().union(*(_advance(alts[h], p, sym) for sym in opt)) for h, p in pos.items()}
        now = set().union(*(dawg.reachable.get(s, frozenset()) for s in nxt)) if nxt else set()
        # the per-hypothesis gaṇa simulation and the DFA must agree on who is alive
        assert now == {h for h, p in pos.items() if p}, f"liveness mismatch at akshara {k + 1}"
        died = alive - now
        for h in died:
            died_at[h] = k
        syl = syllables[k]
        steps.append({
            "k": k + 1, "akshara": syl.text, "options": opt, "weight": syl.weight,
            "rules": list(syl.rules), "vikalpa": syl.vikalpa,
            "edges": edges, "frontier": nxt,
            "alive": sorted(hid[h] for h in now), "died": sorted(hid[h] for h in died),
            "positions": {hid[h]: _describe(alts[h], pos[h]) for h in now},
        })
        alive = now
        frontier = nxt
        if not frontier:
            death_step = k + 1
            break

    accepted = set()
    for s in frontier:
        accepted |= set(dfa.labels.get(s, frozenset()))
    padanta: dict = {}
    if death_step in (None, len(options)) and options and options[-1] == "I":
        # pādānta: the line-final laghu may be read as guru (treatise 4.36), also
        # when the walk died on that very laghu
        prev = steps[-2]["frontier"] if len(steps) > 1 else [dfa.start]
        flip_edges, flip_states, extra = [], [], set()
        for s in prev:
            d = dfa.step(s, "U")
            gained = set(dfa.labels.get(d, frozenset())) - accepted if d is not None else set()
            if gained:
                flip_edges.append([s, "U", d])
                flip_states.append(d)
                extra |= gained
        padanta = {"edges": flip_edges, "states": flip_states, "accepted": sorted(hid[h] for h in extra)}
    # alive at the end but not accepting: the line ended too early for it
    hyps = dawg.hypotheses
    padanta_h = {hyps[i] for i in padanta["accepted"]} if padanta else set()
    for h in alive - accepted - padanta_h:
        died_at[h] = len(options)
    return {
        "unit": unit_no, "printed_lines": printed, "text": text,
        "aksharas": [{"text": s.text, "weight": s.weight, "options": o, "rules": list(s.rules),
                      "vikalpa": s.vikalpa, "word": s.word} for s, o in zip(syllables, options)],
        "steps": steps,
        "death_step": death_step,
        "accepted": sorted(hid[h] for h in accepted),
        "accept_states": [s for s in frontier if dfa.labels.get(s)],
        "padanta": padanta or None,             # None: the last akshara is not a laghu
        "died_at": {hid[h]: i for h, i in died_at.items()},
    }


# -----------------------------------------------------------------------------
# 4. the whole poem
# -----------------------------------------------------------------------------
def _reading_level(scans, dawg) -> str:
    """The first reading level that identifies the poem — identify_text's loop."""
    for level in READING_LEVELS:
        if identify(reading_options(scans, level), dawg).identified:
            return level
    return READING_LEVELS[0]


def _units(scans, options, best) -> list[tuple[tuple, list, list[int], list[tuple[int, int]]]]:
    """(options, syllables, printed line indices, (printed line, word) of
    each syllable) of every pāda as the best candidate read them: seesam
    half-lines joined, a trailer after its head."""
    n = len(scans)
    groups: list[list[int]] = [[i] for i in range(n)]
    if best is not None:
        tail = len(best.trailer.lines) if best.trailer else 0
        head = len(best.lines)
        h = (n - tail) // head if head else 1
        if h > 1:
            groups = [list(range(i, i + h)) for i in range(0, head * h, h)] + [[i] for i in range(head * h, n)]
    out = []
    for g in groups:
        opts = sum((tuple(options[i]) for i in g), ())
        syls = sum((list(scans[i].syllables) for i in g), [])
        # Layer B's words: whitespace tokens of the printed line (analysis._telugu_words), so a
        # comma inside "యుతు,లల్ప" does not end a word the way the scanner's word index does
        word_of = [(i, len(re.findall(r"\S+", scans[i].text[:y.start + 1])) - 1)
                   for i in g for y in scans[i].syllables]
        out.append((opts, syls, g, word_of))
    return out


def _segmentation(lm) -> dict:
    seg = lm.segmentation
    return {"line_no": lm.line_no, "slot": lm.slot, "pattern": seg.line, "padanta": lm.padanta_applied,
            "ganas": [{"te": s.gana.telugu, "name": s.gana.name, "pattern": s.pattern,
                       "start": s.start, "end": s.end} for s in seg.segments],
            "yati": list(seg.yati_aksharas), "n_parses": lm.n_parses}


def _stanza(dawg, hid: dict, units: list[dict], res) -> dict:
    """Which metre accepted which pāda in which slot, and why the losers lost."""
    hyps = list(dawg.hypotheses)
    rows: dict[str, dict] = {}
    for u in units:
        acc = {hyps[i] for i in u["accepted"]}
        pad = {hyps[i] for i in u["padanta"].get("accepted", [])} if u["padanta"] else set()
        for m, slot in acc | pad:
            row = rows.setdefault(m, {"meter": m, "name_te": dawg.spec(m).name_te, "cells": {}})
            row["cells"].setdefault(u["unit"], []).append({"slot": slot, "padanta": (m, slot) in pad})
    walks = []
    for u in units:
        acc = frozenset(hyps[i] for i in u["accepted"])
        pad = frozenset(hyps[i] for i in u["padanta"].get("accepted", [])) if u["padanta"] else frozenset()
        line = "".join(a["options"][0] for a in u["aksharas"])
        walks.append(WalkResult(line=line, accepted=acc, padanta_accepted=pad,
                                died={hyps[int(i)]: k for i, k in u["died_at"].items()}))
    cand_meters = {c.meter for c in res.candidates} | {c.trailer.meter for c in res.candidates if c.trailer}
    out = []
    for m, row in rows.items():
        spec = dawg.spec(m)
        if m in cand_meters:
            verdict, reason = True, ""
        else:
            f = stanza_failure(spec, walks)
            verdict, reason = False, (f[2] if f else "")
        out.append({**row, "cells": {str(k): v for k, v in row["cells"].items()},
                    "matched": verdict, "reason": reason, "pattern": list(spec.slot_pattern)})
    out.sort(key=lambda r: (not r["matched"], -len(r["cells"]), dawg.spec(r["meter"]).id))
    return {"rows": out}


# -----------------------------------------------------------------------------
# 5. v2: the akshara inventory (Layer A) and the word DAWG (Layer B)
# -----------------------------------------------------------------------------
# The v2 constraint of metrical_decoder (plan §17) keeps the metrical DAWG as it
# is and adds two corpus layers: Layer A, only aksharas attested in the verse
# of dataset/*.json may be written (a hard gate); Layer B, a preference for
# words that are real, scored with a suffix automaton (Blumer's DAWG) over the
# corpus words. Here both are read off the poem akshara by akshara.
@lru_cache(maxsize=1)
def v2_layers():
    """(inventory, attestation), built once per process (Layer B: about 6 s)."""
    from metrical_decoder.attestation import load_attestation
    from metrical_decoder.inventory import load_inventory
    return load_inventory("verse"), load_attestation("all")


def _sam_state(att, text: str) -> Optional[int]:
    """The suffix-automaton state reached by ``text`` from the root, None when
    ``text`` occurs inside no corpus word (``Attestation.inside`` as a walk)."""
    v = 0
    for ch in text:
        v = att._next[v].get(ch)
        if v is None:
            return None
    return v


def _v2_unit(syllables: list, word_of: list[tuple[int, int]], inv, att) -> list[dict]:
    """Per akshara: the Layer A check, and the Layer B walk of the word so far,
    one suffix-automaton state per character."""
    from metrical_decoder.attestation import SEPARATOR
    out = []
    word, n_in_word = "", 0
    for k, syl in enumerate(syllables):
        key = word_of[k]
        if k == 0 or key != word_of[k - 1]:
            word, n_in_word = "", 0
        chars = []
        for ch in syl.text:
            word += ch
            state = _sam_state(att, word)
            row = att._next[state] if state is not None else {}
            nxt = sorted(c for c in row if c != SEPARATOR)
            chars.append({"ch": ch, "state": state, "score": att.partial(word), "out": len(nxt),
                          "sample": "".join(nxt[:12]), "can_end": SEPARATOR in row})
        n_in_word += 1
        ends = k == len(syllables) - 1 or word_of[k + 1] != key
        out.append({
            "inventory": syl.text in inv, "word": word, "word_start": n_in_word == 1, "chars": chars,
            "partial": att.partial(word), "ends_word": ends,
            "finished": (att.finished(word) if n_in_word >= 2 else None) if ends else None,
        })
    return out


def _v2_summary(units: list[dict], inv, att) -> dict:
    aksharas = [(a["text"], v["inventory"]) for u in units for a, v in zip(u["aksharas"], u["v2"])]
    words = [v for u in units for v in u["v2"] if v["ends_word"]]
    scored = [v for v in words if v["finished"] is not None]
    return {
        "inventory_size": len(inv), "words_in_corpus": len(att.words), "sam_states": len(att._next),
        "aksharas": len(aksharas), "outside_inventory": sorted({t for t, ok in aksharas if not ok}),
        "n_outside": sum(1 for _, ok in aksharas if not ok),
        "words": len(words), "scored_words": len(scored), "real_words": sum(1 for v in scored if v["finished"]),
        "single_akshara_words": len(words) - len(scored),
        "junk_words": [v["word"] for v in scored if not v["finished"]],
    }


def trace_payload(text: str, version: str = "v1") -> dict:
    """The akshara-by-akshara walk of ``text`` and the identification verdict;
    ``version="v2"`` adds the Layer A and Layer B readings of every akshara."""
    dawg = default_dawg()
    hid = {h: i for i, h in enumerate(dawg.hypotheses)}
    scans = [s for s in sc.scan(text) if s.syllables]
    if not scans:
        raise ValueError("no Telugu aksharas found in the text")
    printed = [s.text.strip() for s in scans]
    level = _reading_level(scans, dawg)
    res = identify_text(text, dawg)                 # the verdict chandohasam.analyze reports
    options = reading_options(scans, level)
    best = res.best
    pieces = _units(scans, options, best)
    units = [_walk_unit(dawg, hid, opts, syls, group, " ".join(printed[i] for i in group), n)
             for n, (opts, syls, group, _) in enumerate(pieces, start=1)]
    verdict = {
        "identified": res.identified, "ambiguous": res.ambiguous,
        "candidates": [c.label for c in res.candidates], "notes": list(res.notes), "level": level,
        "best": None, "failures": [f.to_dict() for f in res.failures[:8]],
    }
    if best is not None:
        lines = [_segmentation(lm) for lm in best.lines]
        if best.trailer:
            lines += [_segmentation(lm) for lm in best.trailer.lines]
        verdict["best"] = {"meter": best.meter, "label": best.label, "name_te": best.name_te,
                           "family": best.family,
                           "trailer": ({"meter": best.trailer.meter, "name_te": best.trailer.name_te}
                                       if best.trailer else None),
                           "notes": list(best.notes), "violations": list(best.violations), "lines": lines}
    payload = {
        "poem": text, "printed": printed, "level": level, "version": version,
        "units": units, "verdict": verdict,
        "stanza": _stanza(dawg, hid, units, res),
    }
    if version == "v2":
        inv, att = v2_layers()
        for u, (_, syls, _, word_of) in zip(units, pieces):
            u["v2"] = _v2_unit(syls, word_of, inv, att)
        payload["v2"] = _v2_summary(units, inv, att)
    return payload
