"""Paths and settings shared by every data-sanity script.

The scripts measure the four corpora in ../dataset/ (see common/dataset.py).
The metric definitions and thresholds follow the corpus-validation pipeline of
IndicNeuroSym §5, levels 1-4 (level 5, LLM-as-a-judge, is not implemented).
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DATASET_DIR = REPO_ROOT / "dataset"
METER_ENGINE_DIR = REPO_ROOT / "meter_engine"

OUTPUT_DIR = HERE / "outputs"               # one JSON per script
CACHE_DIR = OUTPUT_DIR / "cache"            # scansions and embeddings, gitignored

# dataset name (the file stem) -> file in dataset/, in the order every table reports them.
# Every metric is reported per file.
CORPORA = {
    "bhagavatam": "bhagavatam.json",
    "vemana": "vemana.json",
    "kuchimanchi_timmakavi": "kuchimanchi_timmakavi.json",
    "chandassu": "chandassu.json",
}

SEED = 42

# ---- level 1: prosodic integrity (meter_engine) ----------------------------
SCAN_PROFILES = ("strict", "relaxed")       # meter_engine profiles gating prāsa and yati
YATI_SANDHI = "hypothesis"                  # the yati engine's default sandhi mode

# ---- level 2: length ratio -------------------------------------------------
LENGTH_RATIO_BOUNDS = (0.8, 2.5)            # pass if 0.8 <= |bhavam| / |verse| <= 2.5

# ---- level 3: semantic fidelity --------------------------------------------
SIMILARITY_THRESHOLD = 0.65                 # pass if cosine >= 0.65
GATE_MODEL = "labse"                        # the level-3 gate is LaBSE, Telugu bhavam vs English bhavam
RETRIEVAL_POOL = 2000                       # candidates in the retrieval control
EMBEDDING_MODELS = {
    "labse": "sentence-transformers/LaBSE",
    "msbert": "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
    "indicsbert": "l3cube-pune/indic-sentence-bert-nli",
    # negative control: an English-only encoder that cannot read Telugu script;
    # whatever it "passes" is what the threshold gives away for free
    "minilm_en_control": "sentence-transformers/all-MiniLM-L6-v2",
}

# ---- level 4: lexical diversity and subword coverage -----------------------
MATTR_WINDOW_CORPUS = 50
MATTR_WINDOW_POEM = 2
# Gemma 4 and Gemma 3 share one text tokenizer: the same 1,784 Telugu tokens, and identical token ids
# for every verse and bhavam of the four files (checked 2026-09-28; they differ only in special tokens).
TOKENIZER = "google/gemma-4-E2B-it"
