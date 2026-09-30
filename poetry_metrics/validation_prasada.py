"""Validation of the prasāda metric (run through `python3 prasada.py validate`).

Everything is seeded and written to outputs/prasada_validation.json.

1. Per-corpus figures: surprisal, perplexity, Zipf word frequency, known-word
   share, rubric levels. The reference model has seen none of these poems.
2. Classical contrasts (fixtures/classical_exemplars.json): the treatise's
   example of prasāda against its examples of words that are not well known,
   and Daṇḍin's pair. The clear one must have the lower surprisal.
3. Degradation controls (proposal, Appendix E: a metric is admitted if it
   declines when the verse is degraded). The poem's words shuffled, and its
   aksharas shuffled, each keeping the line lengths.
4. The order of the model: unigram, bigram, trigram.
5. Relations: surprisal against the word-frequency figures, and against the
   other metrics.
6. The clearest and hardest lines.

The test against generated poems is in samples_analysis.py, which loads them.
"""
from __future__ import annotations

import json
import random
import statistics
from collections import Counter

import anuprasa
import madhurya
import ojas
import prasada as pr
import validation_madhurya as vm
from common import corpus
from common.phonology import aksharas
from common.stats import spearman, summary

MIN_LINE_AKSHARAS = 8


def shuffled(poem, rng, unit: str) -> list:
    """The poem with its words, or its aksharas, shuffled; every line keeps its count of them."""
    if unit == "word":
        per_line = [pr.words_of(l) for l in poem.lines]
        joiner = " "
    else:
        per_line = [aksharas(l) for l in poem.lines]
        joiner = ""
    pieces = [x for line in per_line for x in line]
    rng.shuffle(pieces)
    it = iter(pieces)
    return [joiner.join(next(it) for _ in line) for line in per_line if line]


def surprisal(model, lines, order: int = pr.ORDER):
    return pr.poem_figures(model, lines, order)["surprisal"]


def contrasts_report(model) -> dict:
    lines = {e["id"]: e["lines"] for e in vm.load_exemplars()}
    data = json.loads(vm.EXEMPLARS.read_text(encoding="utf-8"))
    figures, rows = {}, []
    for c in data["contrasts"]:
        if c["metric"] != "prasada":
            continue
        for eid in (c["more"], c["less"]):
            if eid not in figures:
                r = pr.score_poem(lines[eid], model)
                figures[eid] = {k: r[k] for k in ("surprisal", "label", "percentile", "zipf", "known_word_share")}
        a, b = figures[c["more"]]["surprisal"], figures[c["less"]]["surprisal"]
        rows.append({"clearer": c["more"], "obscurer": c["less"], "basis": c["basis"],
                     "surprisal_clearer": a, "surprisal_obscurer": b, "in_order": a < b})
    return {"contrasts": rows, "in_order": f"{sum(r['in_order'] for r in rows)}/{len(rows)}", "exemplars": figures}


def run(args) -> None:
    model = pr.load_model()
    base = model.meta
    md_base, oj_base, an_base = madhurya.load_baseline(), ojas.load_baseline(), anuprasa.load_baseline()
    report = {
        "version": pr.VERSION, "seed": args.seed, "cuts": base["cuts"],
        "reference": {k: base[k] for k in ("reference_corpus", "reference_poems", "akshara_tokens", "akshara_types",
                                           "bigrams_kept", "trigrams_kept", "min_counts", "word_tokens",
                                           "word_types", "words_kept")},
        "contrasts": contrasts_report(model), "corpora": {},
    }
    for cname in corpus.CORPORA:
        poems = corpus.load(cname)
        figures = [pr.poem_figures(model, p.lines) for p in poems]
        h = [f["surprisal"] for f in figures]
        levels = Counter(pr.level_of(x, base["cuts"]["poem"]) for x in h)
        entry = {
            "n_poems": len(poems),
            "surprisal": summary(h),
            "perplexity_of_mean": round(2 ** statistics.fmean(h), 1),
            "zipf": summary([f["zipf"] for f in figures]),
            "known_word_share": summary([f["known_word_share"] for f in figures]),
            "poem_levels_pct": {pr.LABELS[k]: round(100 * levels[k] / len(h), 2) for k in range(5)},
        }

        rng = random.Random(args.seed)
        for unit in ("word", "akshara"):
            control = [surprisal(model, shuffled(p, rng, unit)) for p in poems]
            pairs = [(a, b) for a, b in zip(h, control) if a is not None and b is not None]
            entry[f"{unit}_shuffle"] = {
                "mean_real": round(statistics.fmean(a for a, _ in pairs), 3),
                "mean_shuffled": round(statistics.fmean(b for _, b in pairs), 3),
                "real_clearer_pct": round(100 * sum(a < b for a, b in pairs) / len(pairs), 2),
            }

        rng = random.Random(args.seed)
        entry["by_order"] = {}
        for order in (1, 2, 3):
            real = [surprisal(model, p.lines, order) for p in poems]
            control = [surprisal(model, shuffled(p, rng, "word"), order) for p in poems]
            entry["by_order"][str(order)] = {
                "mean_surprisal": round(statistics.fmean(real), 3),
                "real_clearer_than_word_shuffled_pct": round(100 * sum(a < b for a, b in zip(real, control))
                                                             / len(real), 2)}

        m = [madhurya.pooled(madhurya.profile_poem(p.lines)).index() for p in poems]
        counts = [ojas.pooled(ojas.count_poem(p.lines)) for p in poems]
        o = [ojas.index(c, oj_base["scale"]) for c in counts]
        az = [anuprasa.poem_levels(t, an_base["level_probs"])[anuprasa.HEADLINE][0]
              for t in anuprasa.tokens_of(poems)]
        keep = [i for i, v in enumerate(az) if v is not None]
        entry["spearman_of_surprisal_with"] = {
            "zipf": spearman(h, [f["zipf"] for f in figures]),
            "known_word_share": spearman(h, [f["known_word_share"] for f in figures]),
            "ojas": spearman(h, o),
            "word_length": spearman(h, [c.word_length for c in counts]),
            "conjunct_rate": spearman(h, [c.conjunct_rate for c in counts]),
            "madhurya": spearman(h, m),
            "anuprasa_z": spearman([h[i] for i in keep], [az[i] for i in keep]),
            "poem_length": spearman(h, [f["n_aksharas"] for f in figures]),
        }

        lines = []
        for p in poems:
            for text in p.lines:
                aks, bits = model.bits(text)
                if len(aks) >= MIN_LINE_AKSHARAS:
                    lines.append((sum(bits) / len(bits), p.key, text))
        lines.sort(key=lambda x: x[0])
        entry["clearest_lines"] = [{"surprisal": round(s, 2), "poem": k, "line": l} for s, k, l in lines[:8]]
        entry["hardest_lines"] = [{"surprisal": round(s, 2), "poem": k, "line": l} for s, k, l in lines[:-9:-1]]
        report["corpora"][cname] = entry
        print(f"{cname}: {len(poems)} poems")
    report["versions"] = {"madhurya": md_base["version"], "ojas": oj_base["version"]}

    pr.OUTPUT_DIR.mkdir(exist_ok=True)
    path = pr.OUTPUT_DIR / "prasada_validation.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {path.relative_to(pr.HERE)}")
