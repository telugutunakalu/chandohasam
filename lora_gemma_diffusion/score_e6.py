"""E6 comparison: DiffusionGemma (base, 24k, 48k; free and constrained) beside the MDLMs and Nandi, on the 114 E6
val poems (PLAN.md §4).

    ../.venv/bin/python -u score_e6.py          # → results/e6_comparison.{md,json}; sets missing on disk are skipped

Every set is scored by ../RL/reward.py's Scorer (one process; the RL report's definitions): whole poem in metre
(strict engines), chandas skill (1 = in metre, 0 = prose; mean and median, since it is unbounded below), vṛtta lines on
the gold pattern, one-akshara words, copy from the bhāvam, bhāvam recognised (LaBSE top-1 among 10 of the same metre;
a topic signal, not meaning; reported raw here, without the reward's rule that withholds it above 10% copy, since
copy is its own column), poems repeating a line, lines per poem. Plus the real-words measure **with ఁ stripped on
both sides** (the poems' words and the training lexicon, for every model): DiffusionGemma writes no ఁ (dropped from its
training text, PLAN.md §6), and without the stripping its words would be judged against ఁ forms.
"""
from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "RL"))
import reward as rw                                                              # noqa: E402
import rlcommon as rc                                                            # noqa: E402
from metrical_decoder.analysis import _syllables, _telugu_words                 # noqa: E402

DF, AR, DG = REPO / "diffusion_finetuning" / "runs", REPO / "autoregressive_finetuning" / "runs", HERE / "runs"
SETS = [  # label, results.jsonl, mode
    ("MDLM 120M, free", DF / "e6_120m_t1_val/results.jsonl", "baseline"),
    ("MDLM 120M, constrained", DF / "e6_120m_t1_val/results.jsonl", "masking_backtrack"),
    ("MDLM 523M, free", DF / "e6_523m_t1_val/results.jsonl", "baseline"),
    ("MDLM 523M, constrained", DF / "e6_523m_t1_val/results.jsonl", "masking_backtrack"),
    ("Nandi-Mini-150M, free", AR / "e6_nandi_val/results.jsonl", "baseline"),
    ("Nandi-Mini-150M, constrained", AR / "e6_nandi_val/results.jsonl", "masking_backtrack"),
    ("DiffusionGemma base, free (native)", DG / "e6_dg_base_val_free/results.jsonl", "baseline"),
    ("DiffusionGemma LoRA 24k, free (native)", DG / "e6_dg_24k_val_free/results.jsonl", "baseline"),
    ("DiffusionGemma LoRA 48k, free (native)", DG / "e6_dg_48k_val_free/results.jsonl", "baseline"),
    ("DiffusionGemma LoRA full pool, free (native)", DG / "e6_dg_full_val_free/results.jsonl", "baseline"),
    ("DiffusionGemma base, constrained (fixed + settled)", DG / "e6_dg_base_val_constrained/results.jsonl",
     "masking_backtrack"),
    ("DiffusionGemma LoRA 48k, constrained (fixed + settled)", DG / "e6_dg_48k_val_constrained/results.jsonl",
     "masking_backtrack"),
    ("T5Gemma 2 270M (full pool), free", REPO / "t5_finetuning/runs/e6_t5g_270m_val/results.jsonl", "baseline"),
    ("T5Gemma 2 1B (full pool), free", REPO / "t5_finetuning/runs/e6_t5g_1b_val/results.jsonl", "baseline"),
    ("T5Gemma 2 270M (full pool), constrained", REPO / "t5_finetuning/runs/e6_t5g_270m_val_c/results.jsonl",
     "masking_backtrack"),
    ("T5Gemma 2 1B (full pool), constrained", REPO / "t5_finetuning/runs/e6_t5g_1b_val_c/results.jsonl",
     "masking_backtrack"),
    ("T5Gemma 2 1B (full pool), constrained, v2 Layer A (padyarchana inventory)",
     REPO / "t5_finetuning/runs/e6_t5g_1b_val_c_invpad/results.jsonl", "masking_backtrack"),
    ("T5Gemma 2 1B (full pool), constrained, v2 A + B (padyarchana inventory and words, weight 2, every step)",
     REPO / "t5_finetuning/runs/e6_t5g_1b_val_c_v2/results.jsonl", "masking_backtrack"),
    ("T5Gemma 2 4B LoRA (first 48k of the pool), free", REPO / "t5_finetuning/runs/e6_t5g_4b_48k_val/results.jsonl",
     "baseline"),
    ("T5Gemma 2 4B LoRA (full pool), free", REPO / "t5_finetuning/runs/e6_t5g_4b_val/results.jsonl", "baseline"),
]


def stripped_matcher():
    import real_words
    train = collections.Counter()
    for w, c in real_words.lexicon()["train"].items():
        train[w.replace("ఁ", "")] += c
    return real_words.Matcher(False, train=dict(train))


def words_stripped(m, lines: list[str]) -> float | None:
    ws = [w.replace("ఁ", "") for ln in lines for w in _telugu_words(ln)]
    ws2 = [w for w in ws if w and len(_syllables(w)) >= 2]
    return sum(m.verdict(w)["compound"] for w in ws2) / len(ws2) if ws2 else None


def summary(rows: list[dict]) -> dict:
    def mean(k):
        v = [float(r[k]) for r in rows if r.get(k) is not None]
        return float(np.mean(v)) if v else None
    sk = [r["skill"] for r in rows if r.get("skill") is not None]
    return {"poems": len(rows), "in_metre": mean("all"), "skill_mean": float(np.mean(sk)) if sk else None,
            "skill_median": float(np.median(sk)) if sk else None, "line_gana": mean("line_gana"),
            "words_stripped": mean("words_s"), "filler": mean("filler"), "copy": mean("copy"),
            "recognised": mean("meaning"), "repeated": mean("repeated"), "n_lines": mean("n_lines")}


def main() -> None:
    rw.COPY_MEANING = 1.01          # raw recognition here (the reward withholds it above 10% copy); copy is its own column
    s = rw.Scorer("val")
    m = stripped_matcher()
    vp = rc.prompts("val")
    sets = {"gold (real poems)": [{"prompt_id": r["id"], "meter": r["meter"], "text": "\n".join(r["lines"])} for r in vp]}
    for label, path, mode in SETS:
        if not path.exists():
            print(f"skipped (not on disk): {label}", flush=True)
            continue
        rows = rw.e6_rows(path, mode).get(mode, [])
        if rows:
            sets[label] = rows
    res = {}
    for label, rows in sets.items():
        scored = s.score(rows)
        for r in scored:
            r["words_s"] = words_stripped(m, r["lines"])
        res[label] = summary(scored)
        print(f"{label}: {json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in res[label].items()})}",
              flush=True)
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / "e6_comparison.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = lambda x, s=100: "–" if x is None else (f"{100 * x:.1f}" if s == 100 else f"{x:.2f}")
    md = ["# E6 comparison: DiffusionGemma beside the MDLMs and Nandi (114 val poems, 1 per prompt)", "",
          "Scored by ../RL/reward.py (the RL report's definitions). Real words with ఁ stripped on both sides (poems and "
          "training lexicon) for every model. Recognition is a topic signal, not meaning. Constrained = masking + "
          "backtracking (MDLMs, Nandi: the E6 runs; DiffusionGemma: our diffusion decoder with the NaN-entropy fix and "
          "the settled commit).", "",
          "| set | poems | in metre % | chandas skill mean / median | vṛtta lines on pattern % | real words % (ఁ stripped) "
          "| one-akshara % | copy % | recognised (raw) % | repeating a line % | lines |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for label, v in res.items():
        md.append(f"| {label} | {v['poems']} | {p(v['in_metre'])} | {p(v['skill_mean'], 1)} / {p(v['skill_median'], 1)} | "
                  f"{p(v['line_gana'])} | {p(v['words_stripped'])} | {p(v['filler'])} | {p(v['copy'])} | "
                  f"{p(v['recognised'])} | {p(v['repeated'])} | {p(v['n_lines'], 1)} |")
    (out / "e6_comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)


if __name__ == "__main__":
    main()
