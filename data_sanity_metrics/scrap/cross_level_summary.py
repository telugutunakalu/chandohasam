"""Cross-level summary — Table 4 rebuilt from the per-level outputs.

Paper's Table 4:
    L1 prosodic integrity 100.0% · L2 length ratio 99.1% · L3 LaBSE 77.1%
    · L4 "lexical diversity (TTR) 0.90 avg" · L5 LLM judge 97.0% (not done here)
    · pass all levels 1–3: 68.9%

Everything here is computed on one denominator, the 27,881 master couplets
(the paper's L3 used a 29,343-record augmented set). Two extra rows use this
repo's chandohasam scanner as Level 1 instead of the paper's own analyser.

Needs: build_subsets.py, level1_prosodic_integrity.py, level2_length_ratio.py,
       level3_semantic_fidelity.py, level4_*.py already run.

Writes outputs/cross_level_summary.json

Run:  python cross_level_summary.py
"""
import json

import numpy as np

import config
from common.dataset import load_subset
from common.io import load_result, pct, print_table, save_result


def main():
    master = load_subset("master")
    ids = [r["id"] for r in master]
    n = len(ids)

    paper_l1 = json.loads((config.CACHE_DIR / "paper_analyser_verdicts.json").read_text())
    ch = {int(k): v for k, v in json.loads((config.CACHE_DIR / "chandohasam_verdicts.json").read_text()).items()}
    l1_paper = np.array([paper_l1[i]["valid"] for i in ids])
    l1_ch = np.array([bool(ch[i].get("relaxed", {}).get("valid")) for i in ids])

    l2 = json.loads((config.CACHE_DIR / "level2_ratios.json").read_text())
    assert l2["ids"] == ids
    l2_pass = np.array(l2["pass"])

    scores_path = config.CACHE_DIR / "level3_scores.npz"
    if scores_path.exists():
        sc = np.load(scores_path)
        assert list(sc["ids"]) == ids
        l3_pass = sc["labse__te_en"] >= config.SIMILARITY_THRESHOLD
        l3_clean_pass = sc["labse__te_clean_en"] >= config.SIMILARITY_THRESHOLD
    else:
        print("level3_scores.npz missing: run level3_semantic_fidelity.py for the L3 rows")
        l3_pass = l3_clean_pass = None

    subword = load_result("level4_subword_coverage")
    lexical = load_result("level4_lexical_diversity")

    rows = [
        ["1", "prosodic integrity (paper analyser)", 100.0, pct(l1_paper.sum(), n)],
        ["1'", "prosodic integrity (chandohasam, relaxed)", None, pct(l1_ch.sum(), n)],
        ["2", "length ratio [0.8, 2.5)", 99.1, pct(l2_pass.sum(), n)],
        ["3", "LaBSE Te–En >= 0.65", 77.1, pct(l3_pass.sum(), n) if l3_pass is not None else None],
        ["3*", "LaBSE Te–En >= 0.65, prompt prefix stripped", None,
         pct(l3_clean_pass.sum(), n) if l3_clean_pass is not None else None],
        ["4", "per-poem subword TTR (the '0.90 avg')", 0.90, subword["verse"]["per_text_subword_ttr_mean"]],
        ["4", "per-poem word TTR", 0.993, lexical["per_poem"]["ttr_mean"]],
    ]
    summary = {"n": n}
    if l3_pass is not None:
        all_paper = l1_paper & l2_pass & l3_pass
        all_ch = l1_ch & l2_pass & l3_pass
        all_clean = l1_paper & l2_pass & l3_clean_pass
        rows += [["1–3", "pass all levels 1–3 (paper L1)", 68.9, pct(all_paper.sum(), n)],
                 ["1–3*", "pass all levels 1–3, prefix stripped for L3", None, pct(all_clean.sum(), n)],
                 ["1'–3", "pass all levels 1–3 (chandohasam L1)", None, pct(all_ch.sum(), n)]]
        summary.update({"pass_all_1_3_pct": pct(all_paper.sum(), n),
                        "pass_all_1_3_prefix_stripped_pct": pct(all_clean.sum(), n),
                        "pass_all_1_3_chandohasam_pct": pct(all_ch.sum(), n),
                        "l2_and_l3_pct": pct((l2_pass & l3_pass).sum(), n),
                        "l3_pct": pct(l3_pass.sum(), n)})
    print(f"Table 4 on one denominator (master, n={n})")
    print_table(["level", "check", "paper", "ours"], rows)

    summary["rows"] = [{"level": r[0], "check": r[1], "paper": r[2], "ours": r[3]} for r in rows]
    save_result("cross_level_summary", summary)


if __name__ == "__main__":
    main()
