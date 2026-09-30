"""Validation of the anuprāsa metric (run through `python3 anuprasa.py validate`).

Everything is seeded and written to outputs/anuprasa_validation.json.

1. Per-corpus distributions: line and poem z, poem score, share of lines and
   poems at each rubric level.
2. Controls (proposal Appendix E: a metric is admitted if it declines when the
   verse is degraded). Each keeps part of the real poem:
     word_shuffle       the poem's words permuted across its lines (words and
                        words-per-line kept, their placement lost)
     word_salad         each line rebuilt from random words of the same corpus
                        (words-per-line kept, the poet's word choice lost)
     consonant_shuffle  the poem's consonants permuted over its own consonant
                        slots (inventory and syllable skeleton kept, placement
                        lost; this also undoes the language's avoidance of
                        similar consonants in neighbouring syllables, see 4)
   For each: the share of lines and poems at each level, and how often the real
   poem's z beats its own control's (paired).
3. Ablations, on the same controls: the place-of-articulation grouping
   (sthāna, Viśvanātha's śrutyanuprāsa classes) instead of the varga series,
   and Blain's (1987) distance-weighted statistic (pairs within 8 aksharas,
   weight 1/distance, as in Belouadi & Eger 2023) instead of the whole line.
4. Lift by akshara distance: the observed rate of same-sound pairs at distance
   d over the chance rate q, on the reference corpus. Below 1 at d = 1 is the
   avoidance of similar consonants in adjacent syllables (the OCP; Frisch,
   Pierrehumbert & Broe 2004).
5. Known groups: the 108-poem pilot grid (metrics/initial_evals), where Gemini
   was asked for one alaṅkāra per poem. Sound figures (śabdālaṅkāra) against
   meaning figures (arthālaṅkāra): AUC of the poem z.
6. The top lines of each corpus, for reading.
"""
from __future__ import annotations

import json
import math
import random
import statistics
from collections import Counter, defaultdict

import anuprasa as ap
from common import corpus
from common.phonology import CLASS_OF, Token, line_tokens, series

PILOT = ap.HERE.parent / "metrics" / "initial_evals" / "Outputs" / "chandas_dataset.json"
SABDA = ("vrittyanuprasa", "chekanuprasa", "antyanuprasa", "yamaka", "muktapadagrasta")
ARTHA = ("upama", "rupaka", "shlesha", "atishayokti")
BLAIN_WINDOW = 8

VARIANTS = {                                   # name -> (key function, statistic)
    "varga": (lambda t: series(t.char), "line"),
    "varna": (lambda t: t.char, "line"),
    "ablation_sthana": (lambda t: t.cls, "line"),
    "ablation_blain_varga": (lambda t: series(t.char), "blain"),
}


# --- Blain's distance-weighted statistic (ablation) --------------------------

def blain_stat(tokens, keyf, probs):
    """(A, E, V) with pair weight 1/d for 1 <= d <= BLAIN_WINDOW aksharas."""
    strength, strength2 = defaultdict(float), defaultdict(float)
    a = w_sum = w2_sum = 0.0
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):
            d = tokens[j].akshara - tokens[i].akshara
            if d == 0:
                continue
            if d > BLAIN_WINDOW:
                break
            w = 1.0 / d
            w_sum += w
            w2_sum += w * w
            for t in (i, j):
                strength[t] += w
                strength2[t] += w * w
            if keyf(tokens[i]) == keyf(tokens[j]):
                a += w
    overlap = sum(strength[t] ** 2 - strength2[t] for t in strength)
    q, r = ap.moments(probs)
    return a, q * w_sum, w2_sum * (q - q * q) + overlap * (r - q * q)


def variant_z(poem_tokens, name, level_probs):
    """(poem z, [line z]) of one poem under one variant."""
    keyf, kind = VARIANTS[name]
    probs = level_probs[name]
    if kind == "line":
        stats = [ap.line_stat(t, keyf, probs) for t in poem_tokens]
        return ap.pooled(stats)[0], [s.z for s in stats]
    stats = [blain_stat(t, keyf, probs) for t in poem_tokens]
    a, e, v = (sum(x) for x in zip(*stats)) if stats else (0, 0, 0)
    z = lambda a_, e_, v_: (a_ - e_) / math.sqrt(v_) if v_ > 0 else None
    return z(a, e, v), [z(*s) for s in stats]


# --- controls (token level where possible, so the syllable skeleton is kept) --

def consonant_shuffle(poem_tokens, rng):
    chars = [t.char for line in poem_tokens for t in line]
    rng.shuffle(chars)
    it = iter(chars)
    out = []
    for line in poem_tokens:
        new = []
        for t in line:
            c = next(it)
            new.append(Token(c, t.akshara, CLASS_OF[c]))
        out.append(tuple(new))
    return out


def _retokenise(word_lines):
    return [line_tokens(" ".join(ws))[1] for ws in word_lines]


def word_shuffle(poem, rng):
    word_lines = [l.split() for l in poem.lines]
    words = [w for ws in word_lines for w in ws]
    rng.shuffle(words)
    it = iter(words)
    return _retokenise([[next(it) for _ in ws] for ws in word_lines])


def word_salad(poem, pool, rng):
    return _retokenise([[rng.choice(pool) for _ in l.split()] for l in poem.lines])


# --- summaries -----------------------------------------------------------------

def _at_or_above(values):
    values = [v for v in values if v is not None]
    return {label: round(100 * sum(1 for v in values if v >= cut) / len(values), 2)
            for cut, _, label in reversed(ap.RUBRIC)} if values else {}


def _summary(results):
    line_z = [z for _, zs in results for z in zs if z is not None]
    poem_z = [z for z, _ in results if z is not None]
    scores = [sum(ap.rubric(z) for z in zs) / len(zs) for _, zs in results if zs]
    return {
        "poem_z_median": round(statistics.median(poem_z), 3),
        "poem_z_mean": round(statistics.fmean(poem_z), 3),
        "poem_score_mean": round(statistics.fmean(scores), 4),
        "line_z_median": round(statistics.median(line_z), 3),
        "lines_at_or_above_pct": _at_or_above(line_z),
        "poems_at_or_above_pct": _at_or_above(poem_z),
    }


def _beats(real, control):
    pairs = [(a, b) for (a, _), (b, _) in zip(real, control) if a is not None and b is not None]
    return round(100 * sum(1 for a, b in pairs if a > b) / len(pairs), 2) if pairs else None


def auc(pos, neg):
    """P(a random positive outscores a random negative), ties counted half (Mann-Whitney)."""
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return round(wins / (len(pos) * len(neg)), 4)


# --- analyses ------------------------------------------------------------------

def lift_by_distance(poems_tokens, level_probs, max_d=8):
    total, matched = Counter(), {name: Counter() for name in ("varga", "varna")}
    for lines in poems_tokens:
        for toks in lines:
            for i in range(len(toks)):
                for j in range(i + 1, len(toks)):
                    d = toks[j].akshara - toks[i].akshara
                    if d == 0:
                        continue
                    if d > max_d:
                        break
                    total[d] += 1
                    for name in matched:
                        keyf = VARIANTS[name][0]
                        if keyf(toks[i]) == keyf(toks[j]):
                            matched[name][d] += 1
    return {name: {d: round(matched[name][d] / total[d] / ap.moments(level_probs[name])[0], 3)
                   for d in sorted(total)} for name in matched}


def known_groups(level_probs):
    if not PILOT.exists():
        return {"skipped": f"{PILOT} not found"}
    poems = json.loads(PILOT.read_text(encoding="utf-8"))["poems"]
    by_group = defaultdict(list)
    for p in poems:
        if p.get("alankaram_id") in SABDA + ARTHA:
            toks = [line_tokens(l)[1] for l in p["lines"]]
            by_group[p["alankaram_id"]].append({name: variant_z(toks, name, level_probs)[0] for name in VARIANTS})
    out = {"source": str(PILOT.relative_to(ap.HERE.parent)),
           "groups": {g: {"n": len(v), **{f"median_z_{name}": round(statistics.median(x[name] for x in v), 3)
                                          for name in VARIANTS}}
                      for g, v in sorted(by_group.items())}}
    for name in VARIANTS:
        pos = [x[name] for g in SABDA for x in by_group[g]]
        neg = [x[name] for g in ARTHA for x in by_group[g]]
        out[f"auc_sabda_vs_artha_{name}"] = auc(pos, neg)
    out["n_sabda"] = sum(len(by_group[g]) for g in SABDA)
    out["n_artha"] = sum(len(by_group[g]) for g in ARTHA)
    return out


def run(args) -> None:
    baseline = ap.load_baseline()
    level_probs = {name: ap.level_probabilities(baseline["probabilities"], keyf)
                   for name, (keyf, _) in VARIANTS.items()}
    report = {"version": ap.VERSION, "seed": args.seed, "baseline_corpora": baseline["corpora"], "corpora": {}}
    all_tokens = []
    for cname in corpus.CORPORA:
        poems = corpus.load(cname)
        toks = ap.tokens_of(poems)
        all_tokens += toks
        pool = [w for p in poems for l in p.lines for w in l.split()]
        rng = random.Random(args.seed)
        conditions = {
            "real": toks,
            "word_shuffle": [word_shuffle(p, rng) for p in poems],
            "word_salad": [word_salad(p, pool, rng) for p in poems],
            "consonant_shuffle": [consonant_shuffle(t, rng) for t in toks],
        }
        entry = {"n_poems": len(poems), "n_lines": sum(len(p.lines) for p in poems)}
        for name in VARIANTS:
            results = {cond: [variant_z(t, name, level_probs) for t in ts] for cond, ts in conditions.items()}
            entry[name] = {cond: _summary(res) for cond, res in results.items()}
            for cond in conditions:
                if cond != "real":
                    entry[name][cond]["real_poem_beats_control_pct"] = _beats(results["real"], results[cond])
            if name == ap.HEADLINE:
                scored = sorted(((z, p.key, l) for p, (_, zs) in zip(poems, results["real"])
                                 for l, z in zip(p.lines, zs) if z is not None), key=lambda x: -x[0])
                entry["top_lines"] = [{"z": round(z, 2), "poem": k, "line": l} for z, k, l in scored[:15]]
        report["corpora"][cname] = entry
        print(f"{cname}: {entry['n_poems']} poems")
    report["lift_by_distance"] = lift_by_distance(all_tokens, level_probs)
    report["known_groups"] = known_groups(level_probs)
    ap.OUTPUT_DIR.mkdir(exist_ok=True)
    path = ap.OUTPUT_DIR / "anuprasa_validation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(ap.HERE)}")
