"""Paths, thresholds and the numbers IndicNeuroSym reports (§5, Tables 4, 14–18).

Every script imports from here, so a path or threshold is changed in one place.
Paths can be overridden with environment variables:

    DSM_DATASET              dwipada_consolidated.json (the real file, not the LFS pointer)
    DSM_INDICNEUROSYM_REPO   checkout of github.com/samvarankashyap/indicnuerosym
                             (for the paper's own dwipada_analyser.py)
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent

DATASET_PATH = Path(os.environ.get(
    "DSM_DATASET", Path.home() / "Downloads" / "dwipada_consolidated.json"))
# sha256 recorded in the LFS pointer at indicnuerosym/datasets/dwipada_consolidated.json
DATASET_SHA256 = "4f63ed94e1585b405e12ba4ada7d88c8eb779b78aebb75b24e63e57014cdab99"

INDICNEUROSYM_REPO = Path(os.environ.get(
    "DSM_INDICNEUROSYM_REPO", Path.home() / "workspace" / "indicnuerosym-main"))
METER_ENGINE_DIR = REPO_ROOT / "meter_engine"

OUTPUT_DIR = HERE / "outputs"
CACHE_DIR = OUTPUT_DIR / "cache"          # large per-record arrays, gitignored

SEED = 42

# ---- thresholds stated in the paper ---------------------------------------
LENGTH_RATIO_BOUNDS = (0.8, 2.5)          # §5.2, 0.8 <= |P|/|V| <= 2.5
SIMILARITY_THRESHOLD = 0.65               # §5.3, stated for LaBSE; the paper gives no
                                          # threshold for mSBERT / IndicSBERT, and 0.65 is
                                          # the only one consistent with Tables 15–16
MATTR_WINDOW_CORPUS = 50                  # Table 18
MATTR_WINDOW_POEM = 2                     # Table 18

# ---- sentence encoders (§5.3) ---------------------------------------------
EMBEDDING_MODELS = {
    "labse": "sentence-transformers/LaBSE",
    "msbert": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    # The paper cites Deode et al. (2023) without naming a checkpoint; the NLI
    # model is the one that paper calls "IndicSBERT".
    "indicsbert": "l3cube-pune/indic-sentence-bert-nli",
    # Negative control, not in the paper: an English-only encoder that cannot
    # read Telugu script. Any "pass rate" it earns on Telugu pairs is what the
    # threshold gives away for free.
    "minilm_en_control": "sentence-transformers/all-MiniLM-L6-v2",
}

# ---- tokenizer (§5.4) -----------------------------------------------------
# google/gemma-3-1b-it is gated; unsloth's copy ships the same tokenizer files.
GEMMA3_TOKENIZER = "unsloth/gemma-3-1b-it"

# ---- what the paper reports, for side-by-side comparison ------------------
PAPER = {
    "table3_master_by_source": {
        "ranganatha_ramayanam": 21828, "basava_puranam": 1859,
        "dwipada_bhagavatam": 2002, "palanati_veera_charitra": 65,
        "srirama_parinayamu": 374, "synthetic": 1753, "total": 27881,
    },
    "level1_pass_pct": 100.0,
    "level2": {"pass_pct": 99.1, "pass_n": 27633, "n": 27881, "mean": 1.63, "median": 1.61,
               "top5_extreme": [5.11, 4.73, 4.71, 4.65, 4.36],
               "bins": {"0.50-0.80": 1, "0.80-1.00": 78, "1.00-1.50": 9333,
                        "1.50-2.00": 15449, "2.00-5.11": 3020}},
    "level3": {
        "n": 29343,
        "labse": {"te_en": {"pass_pct": 77.1, "mean": 0.721}},
        "msbert": {"poem_te": {"pass_pct": 63.7, "mean": 0.685, "median": 0.701},
                   "poem_en": {"pass_pct": 4.4, "mean": 0.424, "median": 0.422},
                   "te_en": {"pass_pct": 23.7, "mean": 0.501, "median": 0.515}},
        "indicsbert": {"poem_te": {"pass_pct": 40.1, "mean": 0.614, "median": 0.618},
                       "poem_en": {"pass_pct": 0.0, "mean": 0.255, "median": 0.251},
                       "te_en": {"pass_pct": 21.0, "mean": 0.579, "median": 0.585}},
        "labse_te_en_bins": {"0.00-0.30": 3, "0.30-0.50": 592, "0.50-0.70": 10620,
                             "0.70-0.85": 16294, "0.85-1.00": 1834},
    },
    "level4": {
        "tokens": 179812, "types": 88295,
        "ttr": 0.491, "mattr_w50": 0.501, "yule_k": 3.497, "honore_h": 6164.7,
        "hapax_ratio": 0.804, "sichel_s": 0.091,
        "poem_ttr_mean": 0.993, "poem_mattr_w2_mean": 1.000,
        "poem_yule_k_mean": 22.74, "poem_honore_h_mean": 2356.4,
        "gemma_telugu_vocab": 1784, "gemma_telugu_used": 1328, "gemma_coverage_pct": 74.4,
        "gemma_corpus_tokens": 804671, "poem_subword_ttr_mean": 0.897,
        "exact_duplicates": 0, "near_duplicate_poems": 160, "near_duplicate_groups": 79,
    },
    "table4_pass_all_1_to_3_pct": 68.9,
}
