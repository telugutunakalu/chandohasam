"""Baseline and validation of the chandas distance (run through `python3 chandas_distance.py ...`).

The baseline (baselines/chandas_distance_baseline.json) is the chance
distribution of the distance, per meter: Pothana's prose cut, without regard to
words, into lines of the meter's lengths. A line's length is the mean length of
the lines its slot accepts. It is kept for the full distance ("all": weights,
yati and prāsa) and for the weights alone.

The validation (outputs/chandas_distance_validation.json):

1. Agreement with meter_engine on the weights. With the engine's reading of a
   closing laghu the weight edits must be 0 exactly when the engine accepts
   the poem in its labelled meter, at any of its reading levels. With the
   default reading they may differ only where the engine accepts a closing
   laghu that no conjunct follows.
2. Agreement with meter_engine on yati and prāsa: for poems in meter, no yati
   edit exactly when the engine's tool says the yati holds, and the same for
   prāsa.
3. The verses the classical texts give as examples of a broken meter and a
   broken yati (fixtures/classical_exemplars.json): the edits must fall in the
   pādas the text names.
4. The four corpora against their labels: distance by kind of edit, rubric
   levels, skill; and the yati and prāsa edits of verse under each profile.
5. The edit ladder. k random akshara edits are made to the weight pattern of a
   poem that is in meter. The weight edits may never exceed k, and must rise
   with k.
6. The sound ladder. The prāsa akshara of k pādas of a sound poem is replaced
   by an akshara that does not rhyme. The prāsa edits must rise with k.
7. The nearest meter under error: after k edits, is the labelled meter still
   the nearest?
8. Meters against each other: poems of one meter measured against another.
9. Chance, by family of meter.
10. Real poems one edit from their meter, with the edit.
"""
from __future__ import annotations

import json
import random
import statistics
from collections import Counter, defaultdict

import chandas_distance as cd
from chandohasam import analyze
from common import corpus
from indic_meter_dawg import automaton as au
from indic_meter_dawg import default_dawg, identify
from indic_meter_dawg import scansion as sc
from indic_meter_dawg.identify import READING_LEVELS, reading_options

CHANCE_POEMS = 1000            # per meter
CHANCE_UNITS = {2: 2}          # a meter of two-pāda units is measured on two units, as a four-line poem
LADDER = (1, 2, 3, 5, 8, 13, 21)
LADDER_POEMS = 1000
SOUND_LADDER = (1, 2, 3)
SOUND_LADDER_POEMS = 500
NEAREST_POEMS = 300
NEAREST_EDITS = (0, 1, 2, 3, 5)
CROSS_POEMS = 200              # per meter, for the meter-against-meter table
MIN_CROSS = 200                # a meter enters that table with this many poems in meter
ENGINE_SOUND_POEMS = 300       # poems compared with meter_engine's tool on yati and prāsa
PROFILE_POEMS = 500            # poems in meter whose yati and prāsa are read under every profile
PROFILE_READINGS = (("strict", "hypothesis"), ("relaxed", "hypothesis"), ("relaxed", "acchu"))
EXAMPLES = 8
FAR = 6                        # edits; poems this far are listed by meter
EXEMPLARS = cd.HERE / "fixtures" / "classical_exemplars.json"
AS_ENGINE = cd.Reading(padanta="engine")
NO_RHYME = ("క", "మ", "ర", "స")      # one per pāda, so that spoiled pādas do not rhyme with each other


# ---------------------------------------------------------------------------
# chance text
# ---------------------------------------------------------------------------

def slot_mean_length(meter: str, name: str) -> float:
    """Mean akshara count of the lines a slot accepts."""
    dfa = default_dawg().slot_dfas[(meter, name)]
    ways = {dfa.start: {0: 1}}
    total = weighted = 0
    for s in au.topological_order(dfa):
        here = ways.get(s, {})
        if dfa.is_accepting(s):
            total += sum(here.values())
            weighted += sum(length * k for length, k in here.items())
        for d in dfa.transitions.get(s, {}).values():
            there = ways.setdefault(d, {})
            for length, k in here.items():
                there[length + 1] = there.get(length + 1, 0) + k
    return weighted / total


def chance_lengths(meter: str) -> list:
    spec = default_dawg().spec(meter)
    unit = [round(slot_mean_length(meter, s)) for s in spec.slot_pattern]
    return unit * CHANCE_UNITS.get(len(unit), 1)


def prose_passages() -> list:
    """Pothana's prose passages as (text, syllables)."""
    out = []
    for p in corpus.load("bhagavatam", "prose"):
        text = " ".join(p.lines)
        out.append((text, sc.syllabify(text)))
    return out


def chance_poems(meter: str, passages: list, limit: int = CHANCE_POEMS):
    """Prose cut into consecutive poems of the meter's line lengths."""
    lengths = chance_lengths(meter)
    size, made = sum(lengths), 0
    for text, syllables in passages:
        for start in range(0, len(syllables) - size + 1, size):
            lines, i = [], start
            for length in lengths:
                lines.append(text[syllables[i].start:syllables[i + length - 1].end])
                i += length
            yield lines
            made += 1
            if made == limit:
                return


def chance_figures(edits: list, longest: list) -> dict:
    """Mean and cut of the chance rate (edits per 100 aksharas), and the raw distance."""
    rates = sorted(100 * e / n for e, n in zip(edits, longest))
    return {"rate_mean": round(statistics.fmean(rates), 3),
            "rate_cut": round(rates[round(cd.CHANCE_PERCENTILE / 100 * (len(rates) - 1))], 3),
            "distance_mean": round(statistics.fmean(edits), 3), "distance_sd": round(statistics.pstdev(edits), 3),
            "exact": sum(e == 0 for e in edits)}


def build_baseline(args) -> None:
    dawg, passages = default_dawg(), prose_passages()
    meters = {}
    for spec in dawg.catalogue.concrete:
        found = [cd.poem_distance(lines, spec.name) for lines in chance_poems(spec.name, passages)]
        longest = [max(pd.n_aksharas, pd.target_aksharas) for pd in found]
        kinds = Counter()
        for pd in found:
            kinds.update(pd.operations())
        meters[spec.name] = {
            "family": spec.family, "line_aksharas": chance_lengths(spec.name), "n": len(found),
            "all": chance_figures([pd.distance for pd in found], longest),
            "weights": chance_figures([pd.weights for pd in found], longest),
            "yati_edits_mean": round(statistics.fmean(pd.yati for pd in found), 3),
            "prasa_edits_mean": round(statistics.fmean(pd.prasa for pd in found), 3),
            "weight_edits_pct": {k: round(100 * v / (sum(kinds.values()) or 1), 1) for k, v in sorted(kinds.items())},
        }
    baseline = {
        "metric": "chandas_distance", "version": cd.VERSION, "reading_level": cd.READING,
        "reading": {"padanta": cd.DEFAULT.padanta, "profile": cd.DEFAULT.profile, "yati_sandhi": cd.DEFAULT.sandhi},
        "chance_text": "bhagavatam prose", "prose_passages": len(passages),
        "chance_poems_per_meter": CHANCE_POEMS, "chance_percentile": cd.CHANCE_PERCENTILE,
        "rate_unit": "edits per 100 aksharas", "meters": meters,
    }
    cd.BASELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    cd.BASELINE_PATH.write_text(json.dumps(baseline, ensure_ascii=False, indent=1), encoding="utf-8")
    by_family = defaultdict(list)
    for m in meters.values():
        by_family[m["family"]].append(m["all"]["rate_mean"])
    print(f"wrote {cd.BASELINE_PATH.relative_to(cd.HERE)}: {len(meters)} meters; mean chance rate "
          + ", ".join(f"{f} {statistics.fmean(v):.1f}" for f, v in sorted(by_family.items())))


# ---------------------------------------------------------------------------
# validation
# ---------------------------------------------------------------------------

def labelled(name: str) -> list:
    """(poem, catalogue meter) for the poems of a corpus whose label is a meter of the catalogue."""
    known = {m.name for m in default_dawg().catalogue.concrete}
    out = []
    for p in corpus.load(name):
        meter = cd.NAME_MAP.get(p.metre, p.metre)
        if meter in known:
            out.append((p, meter))
    return out


def layout_fault(lines, meter: str) -> str:
    """Why a far poem may be far for its printing: a line no pāda could hold, or a line count the meter has not."""
    longest = default_dawg().spec(meter).aksharalu[1]
    scanned = cd.scan(lines)
    if max(len(l.options) for l in scanned) > longest:
        return "a_line_longer_than_any_pada"
    counts = {sum(h for _, _, h in target) for target in cd.targets(meter, len(scanned))}
    return "other" if len(scanned) in counts else "unexpected_line_count"


def engine_accepts(lines, meter: str) -> bool:
    scans = sc.scan(list(lines))
    return any(c.meter == meter for level in READING_LEVELS
               for c in identify(reading_options(scans, level)).candidates)


def engine_sound(sample: list) -> dict:
    """Yati and prāsa of poems in meter: this metric's edits against meter_engine's own tool."""
    table = Counter()
    for p, meter in sample:
        pd = cd.poem_distance(p.lines, meter, AS_ENGINE)
        a = analyze(list(p.lines), profile=AS_ENGINE.profile, yati_sandhi=AS_ENGINE.sandhi, meter=meter)
        if pd.weights or not a.identified or a.units[0].meter != meter:
            table["not_compared"] += 1
            continue
        table["yati_" + ("agree" if (pd.yati == 0) == a.yati_matched else "differ")] += 1
        table["prasa_" + ("agree" if (pd.prasa == 0) == a.prasa_matched else "differ")] += 1
    return dict(sorted(table.items()))


def by_profile(sample: list) -> dict:
    """Share of poems in meter with a yati edit and with a prāsa edit, under each of the engine's readings."""
    out = {}
    for profile, sandhi in PROFILE_READINGS:
        found = [cd.poem_distance(p.lines, meter, cd.Reading(profile=profile, sandhi=sandhi)) for p, meter in sample]
        out[f"{profile}/{sandhi}"] = {
            "n": len(found), "with_yati_edits_pct": round(100 * sum(pd.yati > 0 for pd in found) / len(found), 2),
            "with_prasa_edits_pct": round(100 * sum(pd.prasa > 0 for pd in found) / len(found), 2)}
    return out


def broken_meter_exemplars(baseline: dict) -> list:
    """The texts' own examples of a broken meter: the edits, and the pādas that carry them."""
    rows = []
    for e in json.loads(EXEMPLARS.read_text(encoding="utf-8"))["broken_meter"]:
        row = cd.score_poem(e["lines"], baseline, e["meter"])

        def padas(ops: tuple) -> list:
            return [k + 1 for k, line in enumerate(row["lines"]) if any(x["op"] in ops for x in line["edits"])]

        weights_at, yati_at = padas(("substitute", "insert", "delete")), padas(("yati",))
        named_yati = [e["yati_broken_pada"]] if e.get("yati_broken_pada") else []
        rows.append({"id": e["id"], "meter": e["meter"], "pada_the_text_names": e["broken_pada"],
                     "yati_pada_the_text_names": e.get("yati_broken_pada"),
                     "distance": row["distance"], "weight_edits": row["weight_edits"],
                     "yati_edits": row["yati_edits"], "prasa_edits": row["prasa_edits"], "label": row["label"],
                     "padas_with_weight_edits": weights_at, "padas_with_yati_edits": yati_at,
                     "edits": [edit for line in row["lines"] for edit in line["edits"]],
                     "weight_edits_with_engine_padanta": cd.poem_distance(e["lines"], e["meter"], AS_ENGINE).weights,
                     "engine_accepts": engine_accepts(e["lines"], e["meter"]),
                     "located": weights_at == [e["broken_pada"]] and yati_at == named_yati})
    return rows


def edited(lines: tuple, k: int, rng: random.Random) -> tuple:
    """k akshara edits to the weight patterns of a scanned poem: delete, insert or change the weight."""
    rows = [list(l.options[:-1]) + [cd.LAGHU + cd.GURU if l.heavy_by_next else l.options[-1]] for l in lines]
    for _ in range(k):
        i = rng.randrange(len(rows))
        op = rng.choice(("substitute", "insert", "delete"))
        if op == "insert" or not rows[i]:
            rows[i].insert(rng.randrange(len(rows[i]) + 1), rng.choice((cd.GURU, cd.LAGHU)))
        elif op == "delete":
            del rows[i][rng.randrange(len(rows[i]))]
        else:
            j = rng.randrange(len(rows[i]))
            rows[i][j] = cd.LAGHU if rows[i][j][0] == cd.GURU else cd.GURU
    return tuple(cd.Scanned(l.text, (), tuple(r), "".join(o[0] for o in r)) for l, r in zip(lines, rows))


def ladder(exact: list, rng: random.Random) -> dict:
    sample = rng.sample(exact, min(LADDER_POEMS, len(exact)))
    scanned = [(cd.scan(p.lines), meter, default_dawg().spec(meter).family) for p, meter in sample]
    out = {}
    for k in LADDER:
        rows = [(cd.poem_distance(edited(lines, k, rng), meter).weights, family) for lines, meter, family in scanned]
        entry = {"n": len(rows), "mean": round(statistics.fmean(d for d, _ in rows), 3),
                 "within_k": round(sum(d <= k for d, _ in rows) / len(rows), 4),
                 "equal_k": round(sum(d == k for d, _ in rows) / len(rows), 4),
                 "detected": round(sum(d > 0 for d, _ in rows) / len(rows), 4)}
        for family in sorted({f for _, f in rows}):
            ds = [d for d, f in rows if f == family]
            entry[family] = {"n": len(ds), "mean": round(statistics.fmean(ds), 3),
                             "detected": round(sum(d > 0 for d in ds) / len(ds), 4)}
        out[k] = entry
    return out


def unrhymed(line: str, pada: int = 0) -> str:
    """The line with the consonant of its second akshara (the prāsa akshara) replaced by another."""
    syllable = sc.syllabify(line)[1]
    first = next(k for k, ch in enumerate(syllable.text) if ch in sc.CONSONANTS)
    new = next(c for c in NO_RHYME[pada:] + NO_RHYME[:pada] if c not in syllable.onset)
    return line[:syllable.start + first] + new + line[syllable.start + first + 1:]


def sound_ladder(sound: list, rng: random.Random) -> dict:
    """The prāsa akshara of k pādas spoiled, in four-line poems that are sound and whose prāsa is one consonant."""
    eligible = [(p, m) for p, m in sound if default_dawg().spec(m).prasa and len(p.lines) == 4
                and all(len(sc.syllabify(l)) > 1 and len(sc.syllabify(l)[1].onset) == 1 for l in p.lines)]
    sample = rng.sample(eligible, min(SOUND_LADDER_POEMS, len(eligible)))
    out = {}
    for k in SOUND_LADDER:
        found = []
        for p, meter in sample:
            spoiled = set(rng.sample(range(4), k))
            lines = [unrhymed(l, i) if i in spoiled else l for i, l in enumerate(p.lines)]
            found.append(cd.poem_distance(lines, meter))
        out[k] = {"n": len(found), "mean_prasa_edits": round(statistics.fmean(pd.prasa for pd in found), 3),
                  "mean_distance": round(statistics.fmean(pd.distance for pd in found), 3),
                  "detected": round(sum(pd.prasa > 0 for pd in found) / len(found), 4),
                  "within_k": round(sum(pd.prasa <= k for pd in found) / len(found), 4)}
    return out


def nearest_under_error(exact: list, baseline: dict, rng: random.Random) -> dict:
    """After k edits, is the labelled meter the nearest: by skill (the metric's rule), and by raw edits?"""
    sample = rng.sample(exact, min(NEAREST_POEMS, len(exact)))
    scanned = [(cd.scan(p.lines), meter) for p, meter in sample]
    names = [m.name for m in default_dawg().catalogue.concrete]
    out = {}
    for k in NEAREST_EDITS:
        by_skill = by_distance = 0
        for lines, meter in scanned:
            poem = edited(lines, k, rng)
            found = {m: cd.poem_distance(poem, m) for m in names}
            by_skill += cd.nearest(poem, baseline).meter == meter
            by_distance += min(names, key=lambda m: found[m].weights) == meter
        out[k] = {"n": len(scanned), "nearest_by_skill": round(by_skill / len(scanned), 4),
                  "nearest_by_distance": round(by_distance / len(scanned), 4)}
    return out


def cross_meters(exact_by_meter: dict, rng: random.Random) -> dict:
    """Weight edits per 100 aksharas of poems of one meter against another."""
    meters = sorted(m for m, poems in exact_by_meter.items() if len(poems) >= MIN_CROSS)
    out = {}
    for a in meters:
        sample = [cd.scan(p.lines) for p in rng.sample(exact_by_meter[a], CROSS_POEMS)]
        out[a] = {b: round(statistics.fmean(100 * cd.poem_distance(lines, b, cd.WEIGHTS_ONLY).rate
                                            for lines in sample), 2) for b in meters}
    return out


def run(args) -> None:
    rng = random.Random(args.seed)
    baseline = cd.load_baseline()
    report = {"metric": "chandas_distance", "version": cd.VERSION, "seed": args.seed,
              "reading": baseline["reading"]}

    agreement, corpora, exact, sound, slips = {}, {}, [], [], []
    closing = {name: Counter() for name in corpus.CORPORA}
    for name in corpus.CORPORA:
        table, levels, rows, far, layout = Counter(), Counter(), [], Counter(), Counter()
        for p, meter in labelled(name):
            row = cd.score_poem(p.lines, baseline, meter)
            zero, accepted = row["weight_edits"] == 0, engine_accepts(p.lines, meter)
            as_engine = cd.poem_distance(p.lines, meter, cd.Reading(padanta="engine", sound=False))
            table[("zero" if zero else "nonzero") + "_" + ("accepted" if accepted else "rejected")] += 1
            table["engine_padanta_" + ("agrees" if (as_engine.weights == 0) == accepted else "disagrees")] += 1
            if as_engine.weights == 0:            # where does verse the engine accepts need a closing laghu as guru?
                for pada in as_engine.padas:
                    if pada.line.padanta:
                        closing[name]["before_a_conjunct" if pada.heavy_by_next else "not_before_a_conjunct"] += 1
            levels[row["label"]] += 1
            rows.append(row)
            if row["weight_edits"] >= FAR:
                far[meter] += 1
                layout[layout_fault(p.lines, meter)] += 1
            if zero:
                exact.append((p, meter))
                if row["distance"] == 0:
                    sound.append((p, meter))
            elif row["distance"] == 1:
                slips.append((p, meter, row))
        n = len(rows)
        in_meter = [r for r in rows if r["weight_edits"] == 0]

        def counts(key: str) -> dict:
            return {"0": sum(r[key] == 0 for r in rows), "1": sum(r[key] == 1 for r in rows),
                    "2": sum(r[key] == 2 for r in rows), "3-5": sum(3 <= r[key] <= 5 for r in rows),
                    "6+": sum(r[key] >= FAR for r in rows)}

        agreement[name] = dict(sorted(table.items()))
        corpora[name] = {
            "n": n, "levels_pct": {label: round(100 * levels[label] / n, 2) for label in reversed(cd.LABELS)},
            "distance_counts": counts("distance"), "weight_edit_counts": counts("weight_edits"),
            "in_meter_by_weights": len(in_meter),
            "in_meter_with_yati_edits": sum(r["yati_edits"] > 0 for r in in_meter),
            "in_meter_with_prasa_edits": sum(r["prasa_edits"] > 0 for r in in_meter),
            "six_or_more_weight_edits_by_meter": dict(far.most_common()),
            "six_or_more_weight_edits_by_layout": dict(sorted(layout.items())),
            "mean_distance": round(statistics.fmean(r["distance"] for r in rows), 3),
            "mean_weight_edits": round(statistics.fmean(r["weight_edits"] for r in rows), 3),
            "mean_yati_edits": round(statistics.fmean(r["yati_edits"] for r in rows), 3),
            "mean_prasa_edits": round(statistics.fmean(r["prasa_edits"] for r in rows), 3),
            "mean_skill": round(statistics.fmean(r["skill"] for r in rows), 4),
        }
    report["engine_agreement_on_weights"] = agreement
    report["closing_laghu_read_as_guru"] = {name: dict(sorted(c.items())) for name, c in closing.items()}
    report["engine_agreement_on_yati_and_prasa"] = engine_sound(rng.sample(exact, ENGINE_SOUND_POEMS))
    report["yati_and_prasa_by_profile"] = by_profile(rng.sample(exact, PROFILE_POEMS))
    report["broken_meter_exemplars"] = broken_meter_exemplars(baseline)
    report["corpora"] = corpora

    report["edit_ladder"] = ladder(exact, rng)
    report["sound_ladder"] = sound_ladder(sound, rng)
    report["nearest_meter_under_error"] = nearest_under_error(exact, baseline, rng)
    by_meter = defaultdict(list)
    for p, meter in exact:
        by_meter[meter].append(p)
    report["meter_against_meter_weight_rate"] = cross_meters(by_meter, rng)

    families = defaultdict(list)
    for m in baseline["meters"].values():
        families[m["family"]].append(m)
    report["chance_by_family"] = {
        f: {"meters": len(ms),
            **{f"{kind}_{key}_{end}": fn(m[kind][key] for m in ms)
               for kind in ("all", "weights") for key in ("rate_mean", "rate_cut")
               for end, fn in (("min", min), ("max", max))},
            "yati_edits_mean": round(statistics.fmean(m["yati_edits_mean"] for m in ms), 2),
            "prasa_edits_mean": round(statistics.fmean(m["prasa_edits_mean"] for m in ms), 2),
            "chance_poems_exact": sum(m["all"]["exact"] for m in ms),
            "chance_poems_exact_on_weights": sum(m["weights"]["exact"] for m in ms)}
        for f, ms in sorted(families.items())}

    report["one_edit_examples"] = [
        {"poem": p.key, "meter": meter, "line": line["text"], "pattern": line["pattern"], "target": line["target"],
         "edit": line["edits"][0]}
        for p, meter, row in slips[:EXAMPLES] for line in row["lines"] if line["distance"] == 1]

    cd.OUTPUT_DIR.mkdir(exist_ok=True)
    path = cd.OUTPUT_DIR / "chandas_distance_validation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(cd.HERE)}")
    print("engine agreement on weights:", agreement)
    print("engine agreement on yati and prāsa:", report["engine_agreement_on_yati_and_prasa"])
    print("exemplars:", [(r["id"], r["weight_edits"], r["yati_edits"], r["located"]) for r in report["broken_meter_exemplars"]])
    print("edit ladder:", {k: (v["mean"], v["within_k"]) for k, v in report["edit_ladder"].items()})
    print("sound ladder:", {k: (v["mean_prasa_edits"], v["detected"]) for k, v in report["sound_ladder"].items()})
    print("nearest meter under error:", report["nearest_meter_under_error"])
