"""E3: our models beside the three models of CONSTRAINED_DECODING_PLAN.md §16, one table (prediction P3).

    ../.venv/bin/python compare_e3.py [--ours e3_e2_pretrained e3_pilot_seed42]

Every row is computed by `metrical_decoder.analysis.collect` from the runs' own results and traces:
- the Gemma runs in experiments/runs/;
- ours in runs/.
So the columns are those of §16, from one code path. The Gemma rows therefore double as a check: they should
reproduce the §16 table.

Writes results/e3_comparison.md and .json (numbers only).
"""
from __future__ import annotations

import argparse
import json
import sys

from common import HERE, REPO

sys.path.insert(0, str(REPO / "meter_engine"))
from metrical_decoder.analysis import _telugu_words, collect, corpus_lexicon   # noqa: E402
from metrical_decoder.registers import _syllables                             # noqa: E402

GEMMA = {
    "Gemma-4 E4B": ["2026-09-24_e4b_baseline", "2026-09-24_e4b_constrained"],
    "Gemma-4 26B-A4B": ["2026-09-26_g26b"],
    "DiffusionGemma 26B-A4B": ["2026-09-26_diffusion_baseline", "2026-09-25_diffusion_constrained"],
}
MODES = ("baseline", "masking_only", "masking_backtrack", "hybrid")
COLUMNS = (("poems", "poems", None), ("all_strict", "in meter %", "pct"), ("mean_logp", "chosen-token logp", 2),
           ("overridden", "first choice overridden %", "pct"), ("valid_mass", "mass on allowed", 2),
           ("real_words", "real words %", "pct"), ("one_akshara_words", "1-akshara words %", "pct"),
           ("repeated_line", "poems repeating a line %", "pct"), ("tokens_per_poem", "tokens", 0))


def real_words(dirs) -> dict[str, float]:
    """§16's real words, per strategy: words of ≥ 2 aksharas found in the corpora, as a share of all words.
    (`collect`'s `lexical` counts single-akshara filler as words too.) With today's lexicon this gives the
    §16 rates within 2 points; the lexicon changed with the dataset fixes of 2026-09-28."""
    lex, real, total = corpus_lexicon(), {}, {}
    for d in dirs:
        for line in open(d / "results.jsonl", encoding="utf-8"):
            r = json.loads(line)
            ws = _telugu_words(r["text"])
            total[r["mode"]] = total.get(r["mode"], 0) + len(ws)
            real[r["mode"]] = real.get(r["mode"], 0) + sum(len(_syllables(w)) >= 2 and w in lex for w in ws)
    return {m: real[m] / total[m] for m in total if total[m]}


def fmt(v, kind) -> str:
    if v is None:
        return "–"
    if kind == "pct":
        return f"{100 * v:.1f}"
    if kind is None:
        return f"{v:,}"
    return f"{v:.{kind}f}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ours", nargs="+", default=["e3_e2_pretrained", "e3_pilot_seed42"], help="run folders under runs/")
    args = ap.parse_args(argv)
    models = {name: [REPO / "experiments" / "runs" / d for d in dirs] for name, dirs in GEMMA.items()}
    for run in args.ours:
        if (HERE / "runs" / run / "results.jsonl").exists():
            models[f"ours: {run}"] = [HERE / "runs" / run]
    table, data = [], {}
    for name, dirs in models.items():
        by_mode = collect(dirs)["by_mode"]
        for m, v in real_words(dirs).items():
            if m in by_mode:
                by_mode[m]["real_words"] = v
        data[name] = {m: by_mode[m] for m in MODES if m in by_mode}
        for m in MODES:
            if m in by_mode:
                table.append([name, m] + [fmt(by_mode[m].get(k), kind) for k, _, kind in COLUMNS])
    md = ["# E3: token choices under the constraint, by model and strategy", "",
          "Computed by `metrical_decoder.analysis.collect` from each run's results and traces. Real words as in §16: "
          "words of ≥ 2 aksharas found in `dataset/*.json`, as a share of all words. The fine-tuned model was "
          "trained on those corpora, so for it this partly measures recall of training vocabulary (see E4).", "",
          "| model | strategy | " + " | ".join(h for _, h, _ in COLUMNS) + " |",
          "|---|---|" + "---|" * len(COLUMNS)]
    md += ["| " + " | ".join(row) + " |" for row in table]
    out = HERE / "results" / "e3_comparison"
    out.parent.mkdir(exist_ok=True)
    out.with_suffix(".md").write_text("\n".join(md) + "\n", encoding="utf-8")
    out.with_suffix(".json").write_text(json.dumps(data, indent=1, default=str), encoding="utf-8")
    print("\n".join(md))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
