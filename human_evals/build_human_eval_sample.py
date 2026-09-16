#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Builds human_eval_poems.json: a stratified ~500-poem pool for the Chandohasam
human evaluation, drawn from four sources and stratified as evenly as possible
across the 33 canonical Pothana meters (meter_engine/meters.txt).

Baseline: every poem in the pool is a 100%-accurate chandassu match, verified
directly against meter_engine's own DAG scanner (indic_meter_dawg), not
against a corpus's declared label or a generation model's self-report. A
candidate must be identified AND carry zero recorded violations (checked on
the head meter and, for సీసము-family composites, on the గీతి trailer too) —
see clean_match(). Corpus/generation labels are only used as the *target* to
verify against; a poem whose declared meter doesn't hold up under
clean_match() is dropped from the pool entirely, not merely down-weighted.

Sources
-------
  bhagavatam  dataset/bhagavatam.json        (label verified via clean_match)
  vemana      dataset/vemana.json            (label verified via clean_match)
  kuchimanchi dataset/kuchimanchi_timmakavi.json  (UNLABELLED -> identified
              AND verified via clean_match(text, target=None))
  generated   metrics/initial_evals/Outputs/chandas_dataset.json
              (LLM-generated poems; declared meter verified via clean_match;
              the older chandas_prosody_eval.json strict/lenient flags are
              kept as *_legacy metadata only, not used for filtering)
  reference   ../telugu_prosody_engine/telugu_prosody/data/catalogue/examples/*.yaml
              (prosody-textbook examples per meter; the only source for several
              rare catalogue meters; verified via clean_match, and dropped when
              the same text is already in another source)

Allocation
----------
Target 500 poems total. Per-meter quota uses a capacity-constrained
"water-filling" split so meters with little/no data get everything they
have and the remaining budget spreads evenly across data-rich meters,
landing on exactly 500. Within each meter's quota, the same water-filling
split runs again across whichever of the 4 sources have poems in that
meter, so each meter's poems are pulled from multiple datasets rather than
just the largest one.

Run: python3 build_human_eval_sample.py   (from anlp_project/ or here; paths
are resolved relative to this file). Deterministic given SEED.
"""
from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "meter_engine"))

from indic_meter_dawg import identify_text  # noqa: E402
from chandohasam import analyze  # noqa: E402
import multiprocessing  # noqa: E402

PROFILES = ("strict", "relaxed", "historical")   # each accepts everything the previous one does


def strictest_profile(args: tuple[list[str], str]) -> str | None:
    """The strictest profile under which the poem fully complies, as the webapp gives
    the verdict: the meter is identified as the target, prāsa is satisfied where the
    meter requires it, and every yati seat (the గీతి trailer's too) is satisfied.
    None when it fails even under historical."""
    lines, meter = args
    text = "\n".join(lines)
    try:
        ident = identify_text(text)
        for profile in PROFILES:
            a = analyze(text, profile=profile, meter=meter, identification=ident)
            if a.matched and a.units and a.units[0].meter == meter:
                return profile
    except Exception:
        return None
    return None

SEED = 42
TARGET_TOTAL = 500

# -----------------------------------------------------------------------------
# 1. Canonical 33-meter catalogue (meter_engine/meters.txt, id order)
# -----------------------------------------------------------------------------
def load_canonical_meters() -> list[dict]:
    meters = []
    lines = (ROOT / "meter_engine" / "meters.txt").read_text(encoding="utf-8").splitlines()
    for line in lines[1:]:
        if not line.strip():
            continue
        parts = line.split("\t")
        meters.append({"id": int(parts[0]), "name": parts[1], "name_te": parts[2], "type": parts[3]})
    return meters


CANONICAL = load_canonical_meters()
CANONICAL_NAMES = {m["name"] for m in CANONICAL}
NAME_TE = {m["name"]: m["name_te"] for m in CANONICAL}

# -----------------------------------------------------------------------------
# 2. Spelling-variant -> canonical slug map (observed in the raw datasets)
# -----------------------------------------------------------------------------
VARIANT_MAP = {
    # bhagavatam.json / vemana.json (metre_roman)
    "aataveladi": "ataveladi",
    "mattakokila": "mattakokilamu",
    "indravajramu": "indravajra",
    "upendravajramu": "upendravajra",
    "panchachamaramu": "pamcacamaramu",
    "shardulavikriditamu": "sardulavikriditamu",
    # chandas_dataset.json (chandassu_id)
    "shardulavikriditam": "sardulavikriditamu",
    "mattebhavikriditam": "mattebhavikriditamu",
    "seesam": "seesamu",
    "kandam": "kandamu",
    "utsaham": "utsahamu",
}
# non-metrical / out-of-catalogue labels present in bhagavatam.json — dropped
EXCLUDE_LABELS = {
    "vachanamu", "gadya", "slokamu", "dandakamu",
}


def normalize_meter(raw: str | None) -> str | None:
    if not raw:
        return None
    raw = raw.strip().lower()
    if raw in EXCLUDE_LABELS:
        return None
    canon = VARIANT_MAP.get(raw, raw)
    return canon if canon in CANONICAL_NAMES else None


# -----------------------------------------------------------------------------
# 2b. Baseline: every poem must be a 100%-accurate, zero-violation chandassu
# match under meter_engine's own DAG scanner (indic_meter_dawg) — a corpus
# metre label or a generation model's claimed metre is never trusted on its
# own. This is a strictly higher bar than "identified": a candidate can be
# identified while still carrying a recorded stanza-rule violation (e.g.
# kandamu's first-akshara-weight-uniform rule), and a సీసము candidate's
# గీతి trailer can carry its own violations independent of the head; both are
# checked and both must be clean.
# -----------------------------------------------------------------------------
def _is_clean(candidate) -> bool:
    if candidate.violations:
        return False
    if candidate.trailer is not None and candidate.trailer.violations:
        return False
    return True


def clean_match(text: str, target: str | None = None) -> str | None:
    """Return the meter name if `text` is a 100%-accurate DAG match, else None.

    If `target` is given, only that meter is accepted (used to verify a
    corpus/generation label against the DAG). If `target` is None, the best
    identified candidate is accepted when clean (used for kuchimanchi, which
    has no declared labels at all).
    """
    try:
        res = identify_text(text)
    except Exception:
        return None
    if not res.identified:
        return None
    # The "compound" fallback may read any conjunct-guru as laghu, unboundedly;
    # it forces unlisted meters (e.g. తరళము) into matra రగడలు. Not 100% accurate.
    if any("compound-boundary" in n for n in res.notes):
        return None
    if target is not None:
        for cand in res.candidates:
            if cand.meter == target and _is_clean(cand):
                return target
        return None
    return res.best.meter if _is_clean(res.best) else None


# -----------------------------------------------------------------------------
# 3. Load each source into a flat list of normalized records
# -----------------------------------------------------------------------------
def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


PROSE_LABELS = {"vachanamu", "gadya", "dandakamu"}


def verify_or_relabel(text: str, raw_label: str | None) -> tuple[str | None, str]:
    """Verify a corpus label; if it is wrong or outside the catalogue, keep the DAG's own clean match.

    The corpus labels have known errors (dataset/CORRECTIONS.md), and a few rare
    catalogue meters only occur under another label (e.g. 6-20 labelled శ్లోకము
    scans as వసంతతిలకము), so the DAG verdict wins whenever it is clean.
    """
    declared = normalize_meter(raw_label)
    if declared is not None:
        meter = clean_match(text, target=declared)
        if meter is not None:
            return meter, "declared_verified"
    meter = clean_match(text, target=None)
    return meter, "engine_relabelled"


def build_bhagavatam() -> list[dict]:
    data = load_json(ROOT / "dataset" / "bhagavatam.json")
    out = []
    n_checked = 0
    for p in data:
        if p.get("complete") is not True or (p.get("metre_roman") or "").lower() in PROSE_LABELS:
            continue
        n_checked += 1
        text = "\n".join(p["verse"])
        meter, label_source = verify_or_relabel(text, p.get("metre_roman"))
        if meter is None:
            continue
        out.append({
            "source_dataset": "bhagavatam",
            "source_id": p["id"],
            "meter_id": meter,
            "meter_label_source": label_source,
            "declared_meter": p.get("metre_roman"),
            "lines": p["verse"],
            "line_count": p["line_count"],
            "author": "Pothana",
            "metadata": {"skandha": p.get("skandha"), "poem_number": p.get("poem_number")},
        })
    print(f"  bhagavatam: {len(out)}/{n_checked} clean (zero-violation) DAG matches", file=sys.stderr)
    return out


def build_vemana() -> list[dict]:
    data = load_json(ROOT / "dataset" / "vemana.json")
    out = []
    n_checked = 0
    for p in data:
        if p.get("complete") is not True:
            continue
        n_checked += 1
        text = "\n".join(p["verse"])
        meter, label_source = verify_or_relabel(text, p.get("metre_roman"))
        if meter is None:
            continue
        out.append({
            "source_dataset": "vemana",
            "source_id": p["id"],
            "meter_id": meter,
            "meter_label_source": label_source,
            "declared_meter": p.get("metre_roman"),
            "lines": p["verse"],
            "line_count": p["line_count"],
            "author": "Vemana",
            "metadata": {"poem_number": p.get("poem_number")},
        })
    print(f"  vemana: {len(out)}/{n_checked} clean (zero-violation) DAG matches", file=sys.stderr)
    return out


def build_kuchimanchi() -> list[dict]:
    data = load_json(ROOT / "dataset" / "kuchimanchi_timmakavi.json")
    out = []
    for p in data:
        if p.get("complete") is not True:
            continue
        text = "\n".join(p["verse"])
        meter = clean_match(text, target=None)
        if meter is None:
            continue
        meter = normalize_meter(meter)
        if meter is None:
            continue
        out.append({
            "source_dataset": "kuchimanchi",
            "source_id": p["id"],
            "meter_id": meter,
            "meter_label_source": "engine_identified_verified",
            "lines": p["verse"],
            "line_count": p["line_count"],
            "author": "Kūcimañci Timmakavi",
            "metadata": {"poem_number": p.get("poem_number")},
        })
    print(f"  kuchimanchi: {len(out)}/{len(data)} clean (zero-violation) DAG matches", file=sys.stderr)
    return out


def build_generated() -> list[dict]:
    dataset = load_json(ROOT / "metrics" / "initial_evals" / "Outputs" / "chandas_dataset.json")
    poems = dataset["poems"]
    prosody = load_json(ROOT / "metrics" / "initial_evals" / "Outputs" / "chandas_prosody_eval.json")
    prosody_by_idx = {r["idx"]: r for r in prosody}

    # dedupe exact duplicates: keep the lowest id in each group
    drop_ids = set()
    for i, p in enumerate(poems):
        for dup_id in (p.get("duplicate_exact") or []):
            drop_ids.add(max(p["id"], dup_id))

    out = []
    n_checked = 0
    for i, p in enumerate(poems):
        if p["id"] in drop_ids:
            continue
        declared = normalize_meter(p.get("chandassu_id"))
        if declared is None:
            continue
        n_checked += 1
        text = "\n".join(p["lines"])
        meter = clean_match(text, target=declared)
        if meter is None:
            continue
        pros = prosody_by_idx.get(i, {})
        out.append({
            "source_dataset": "generated",
            "source_id": p["id"],
            "meter_id": meter,
            "meter_label_source": "declared_generated_verified",
            "lines": p["lines"],
            "line_count": p["line_count"],
            "author": "Gemini 3.7 Flash (generated)",
            "metadata": {
                "title": p.get("title"),
                "topic": p.get("topic"),
                "alankaram": p.get("alankaram"),
                "contributor": p.get("contributor"),
                # from the OLDER, separate validator used in chandas_prosody_eval.json —
                # kept only for comparison; inclusion here is gated on meter_engine's own
                # clean_match (zero-violation DAG match) above, not on these flags.
                "strict_valid_legacy": pros.get("strict", {}).get("valid"),
                "lenient_valid_legacy": pros.get("lenient", {}).get("valid"),
            },
        })
    print(f"  generated: {len(out)}/{n_checked} clean (zero-violation) DAG matches", file=sys.stderr)
    return out


REFERENCE_DIR = ROOT / "telugu_prosody_engine" / "telugu_prosody" / "data" / "catalogue" / "examples"
# catalogue name -> sibling example file stem, where they differ
REFERENCE_FILES = {
    "champakamala": "campakamala", "mattakokilamu": "mattakokila", "bhujangaprayatamu": "bhujamgaprayatamu",
    "indravajra": "imdravajramu", "upendravajra": "upemdravajramu", "rathoddhata": "rathoddhatamu",
    "kandamu": "kamdam", "seesamu": "sisam-purvabhagamu", "sarvalaghu_seesamu": "sarvalaghusisamu-purvabhagamu",
    "madhuragati_ragada": "madhuragati-ragada", "hayapracara_ragada": "hayapracara-ragada",
    "turagagati_ragada": "turagavalgana-ragada", "mangalamahasri": "mamgalamahasri",
}


def text_key(lines: list[str]) -> str:
    """Letters only, so the same verse printed with different spacing/punctuation compares equal."""
    return re.sub(r"[^ఀ-౿]", "", "".join(lines))


def build_reference() -> list[dict]:
    import yaml
    out = []
    n_checked = 0
    for name in sorted(CANONICAL_NAMES):
        path = REFERENCE_DIR / f"{REFERENCE_FILES.get(name, name)}.yaml"
        if not path.is_file():
            continue
        examples = (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("examples") or []
        for i, ex in enumerate(examples, 1):
            lines = [ln.strip() for ln in str(ex.get("text", "")).splitlines() if ln.strip()]
            if not lines:
                continue
            n_checked += 1
            meter = clean_match("\n".join(lines), target=name)
            if meter is None:
                continue
            out.append({
                "source_dataset": "reference",
                "source_id": f"{path.stem}#{i}",
                "meter_id": meter,
                "meter_label_source": "declared_verified",
                "declared_meter": name,
                "lines": lines,
                "line_count": len(lines),
                "author": "prosody reference (telugu_prosody_engine catalogue)",
                "metadata": {"file": path.name, "source_kind": (ex.get("source") or {}).get("kind")},
            })
    print(f"  reference: {len(out)}/{n_checked} clean (zero-violation) DAG matches", file=sys.stderr)
    return out


# -----------------------------------------------------------------------------
# 4. Capacity-constrained split ("water-filling"), equal or weighted
# -----------------------------------------------------------------------------
def water_fill(capacities: dict, total: int) -> dict:
    """Split `total` as evenly as possible across keys, capped by `capacities`."""
    remaining_keys = sorted(capacities, key=lambda k: capacities[k])
    remaining_total = total
    alloc = {}
    i = 0
    while i < len(remaining_keys):
        k = remaining_keys[i]
        n_left = len(remaining_keys) - i
        share = remaining_total / n_left
        if capacities[k] <= share:
            alloc[k] = capacities[k]
            remaining_total -= capacities[k]
            i += 1
        else:
            break
    # remaining keys (i..end) all have capacity > share: split the rest evenly
    rest = remaining_keys[i:]
    if rest:
        base = remaining_total // len(rest)
        extra = remaining_total % len(rest)
        for j, k in enumerate(rest):
            alloc[k] = base + (1 if j < extra else 0)
    return alloc


def weighted_water_fill(capacities: dict, weights: dict, total: int) -> dict:
    """Split `total` across keys proportional to `weights`, capped by `capacities`.

    Same idea as water_fill, but each round's "ideal" share is proportional to a
    key's weight rather than equal, so a high-weight source (e.g. vemana) claims
    more of any meter's quota than a low-weight one (e.g. kuchimanchi) whenever
    both have room, while every source is still capped at what it actually has.
    """
    remaining = {k: c for k, c in capacities.items() if c > 0}
    alloc = {k: 0 for k in capacities}
    remaining_total = total
    while remaining and remaining_total > 0:
        w_sum = sum(weights[k] for k in remaining)
        ideal = {k: remaining_total * weights[k] / w_sum for k in remaining}
        capped = [k for k in remaining if remaining[k] <= ideal[k] + 1e-9]
        if not capped:
            break
        for k in capped:
            alloc[k] += remaining[k]
            remaining_total -= remaining[k]
            del remaining[k]
    if remaining and remaining_total > 0:
        w_sum = sum(weights[k] for k in remaining)
        raw = {k: remaining_total * weights[k] / w_sum for k in remaining}
        floor_alloc = {k: int(raw[k]) for k in remaining}
        leftover = remaining_total - sum(floor_alloc.values())
        by_frac = sorted(remaining, key=lambda k: raw[k] - floor_alloc[k], reverse=True)
        for k in by_frac[:leftover]:
            floor_alloc[k] += 1
        for k in remaining:
            alloc[k] += floor_alloc[k]
    return alloc


# Source weights for the within-meter split: bhagavatam and vemana are
# human-curated with declared labels; vemana is boosted because it only has
# material in 2 of the 33 meters, so it needs a bigger share where it *does*
# appear; generated is boosted (every poem in its pool already passed the
# zero-violation meter_engine check in build_generated(), so no further
# valid/invalid tiering is needed here); kuchimanchi is downweighted because
# its labels are engine-identified, not human-declared.
SOURCE_WEIGHTS = {
    "bhagavatam": 1.0,
    "vemana": 3.0,
    "generated": 1.75,
    "kuchimanchi": 0.4,
    # textbook examples: a small share where corpora exist, everything where they don't
    "reference": 0.25,
}


def sample_from_source(records: list[dict], n: int, source: str) -> list[dict]:
    """Sample n records from one source's pool for one meter.

    Plain random sampling: the 100%-accuracy gate already ran in each
    build_*() loader (clean_match against meter_engine), so every record here
    is already a verified, zero-violation DAG match.
    """
    return random.sample(records, n)


# -----------------------------------------------------------------------------
# 5. Main: pool, allocate, sample
# -----------------------------------------------------------------------------
def main():
    print("Loading and normalizing sources...", file=sys.stderr)
    # one record per verse text: corpora repeat verses internally, and reference examples quote Pothana
    all_records, seen, n_dup = [], set(), 0
    for r in build_bhagavatam() + build_vemana() + build_kuchimanchi() + build_generated() + build_reference():
        key = text_key(r["lines"])
        if key in seen:
            n_dup += 1
            continue
        seen.add(key)
        all_records.append(r)
    print(f"  dropped {n_dup} records whose text repeats an earlier record", file=sys.stderr)

    # second gate: full compliance (meter + prāsa + yati) under a profile; computed once, one pool per profile
    with multiprocessing.Pool() as workers:
        levels = workers.map(strictest_profile, [(r["lines"], r["meter_id"]) for r in all_records], chunksize=16)
    for r, level in zip(all_records, levels):
        r["strictest_profile"] = level
    before = Counter(r["source_dataset"] for r in all_records)
    for profile in PROFILES:
        allowed = set(PROFILES[:PROFILES.index(profile) + 1])
        after = Counter(r["source_dataset"] for r in all_records if r["strictest_profile"] in allowed)
        print(f"  {profile} (meter + prāsa + yati): "
              + ", ".join(f"{src} {after.get(src, 0)}/{before[src]}" for src in before), file=sys.stderr)

    for profile in PROFILES:
        allowed = set(PROFILES[:PROFILES.index(profile) + 1])
        build_pool([dict(r) for r in all_records if r["strictest_profile"] in allowed], profile)


def build_pool(all_records: list[dict], profile: str) -> None:
    """Stratify and write the pool of poems that fully comply under ``profile``."""
    random.seed(SEED)
    print(f"\n[{profile}] {len(all_records)} compliant records", file=sys.stderr)

    # pool[meter][source] = [records]
    pool = defaultdict(lambda: defaultdict(list))
    for r in all_records:
        pool[r["meter_id"]][r["source_dataset"]].append(r)

    # per-meter availability across all sources
    meter_avail = {m["name"]: sum(len(v) for v in pool[m["name"]].values()) for m in CANONICAL}

    meter_quota = water_fill(meter_avail, TARGET_TOTAL)

    sampled = []
    stratification_by_meter = {}
    stratification_by_source = defaultdict(int)

    for m in CANONICAL:
        name = m["name"]
        quota = meter_quota.get(name, 0)
        if quota == 0:
            stratification_by_meter[name] = {"quota": 0, "by_source": {}}
            continue
        source_avail = {src: len(recs) for src, recs in pool[name].items()}
        source_quota = weighted_water_fill(source_avail, SOURCE_WEIGHTS, quota)
        by_source_counts = {}
        for src, q in source_quota.items():
            if q <= 0:
                continue
            chosen = sample_from_source(pool[name][src], q, src)
            sampled.extend(chosen)
            by_source_counts[src] = q
            stratification_by_source[src] += q
        stratification_by_meter[name] = {"quota": quota, "by_source": by_source_counts}

    random.shuffle(sampled)

    for i, rec in enumerate(sampled, start=1):
        rec_eval_id = f"he_{i:04d}"
        rec["eval_id"] = rec_eval_id
        rec["meter_te"] = NAME_TE[rec["meter_id"]]
        rec["ratings"] = {}

    # reorder keys nicely
    ordered = []
    for rec in sampled:
        ordered.append({
            "eval_id": rec["eval_id"],
            "source_dataset": rec["source_dataset"],
            "source_id": rec["source_id"],
            "meter_id": rec["meter_id"],
            "meter_te": rec["meter_te"],
            "meter_label_source": rec["meter_label_source"],
            "declared_meter": rec.get("declared_meter"),
            "strictest_profile": rec["strictest_profile"],
            "author": rec["author"],
            "line_count": rec["line_count"],
            "lines": rec["lines"],
            "metadata": rec["metadata"],
            "ratings": rec["ratings"],
        })
    ordered.sort(key=lambda r: r["eval_id"])

    meters_covered = sum(1 for v in stratification_by_meter.values() if v["quota"] > 0)

    output = {
        "dataset": "chandohasam_human_eval_v1",
        "description": (
            "Stratified human-evaluation pool for the Chandohasam project: poems "
            "drawn from Pothana's Andhra Mahabhagavatamu, Vemana's satakam, "
            "Kuchimanchi Timmakavi's accha-Telugu Ramayanam (meter identified by "
            "meter_engine), and LLM-generated poems, stratified as evenly as "
            "possible across the 33 canonical Pothana meters and across sources "
            "within each meter. Baseline: every poem is a 100%-accurate, "
            "zero-violation chandassu match verified directly against "
            "meter_engine's indic_meter_dawg DAG scanner — declared/self-reported "
            "meter labels were only accepted as a target to verify against, not "
            f"trusted outright. Every poem also passes the full {profile} analysis "
            f"(chandohasam.analyze, profile {profile}): meter, prāsa and every yati seat. "
            "strictest_profile records the strictest profile each poem passes."
        ),
        "compliance_profile": profile,
        "generated_on": date.today().isoformat(),
        "sampling_seed": SEED,
        "target_size": TARGET_TOTAL,
        "actual_size": len(ordered),
        "meters_total": len(CANONICAL),
        "meters_covered": meters_covered,
        "stratification": {
            "by_meter": stratification_by_meter,
            "by_source": dict(stratification_by_source),
        },
        "poems": ordered,
    }

    out_path = HERE / f"human_eval_poems_{profile}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nWrote {len(ordered)} poems to {out_path}", file=sys.stderr)
    print(f"Meters covered: {meters_covered}/{len(CANONICAL)}", file=sys.stderr)
    print(f"By source: {dict(stratification_by_source)}", file=sys.stderr)
    zero = [m["name"] for m in CANONICAL if stratification_by_meter[m["name"]]["quota"] == 0]
    print(f"Meters with 0 poems (no data in any source): {zero}", file=sys.stderr)


if __name__ == "__main__":
    main()
