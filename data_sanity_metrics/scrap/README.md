# data_sanity_metrics

Re-implementation of the corpus-validation ("data sanity") metrics in
IndicNeuroSym (`Notes/indic_nuerosym.pdf`, §5 and Appendix C), run on the
paper's own dataset. Each metric has a sense check that tests whether its
number means what the paper says it means. Findings are in [report.md](report.md).

## The data sanity metrics in the paper

The paper certifies its 27,881-couplet Telugu dvipada corpus with a five-level
pipeline (§5, Table 4). Level 5 (LLM-as-a-judge) is out of scope here.

| Level | Metric (paper's definition) | Paper value | Script |
|---|---|---|---|
| 1 | Prosodic integrity: share passing the chandas scanner (gaṇa, prāsa, yati, 11–15 syllables) | 100% (27,881) | `level1_prosodic_integrity.py` |
| 2 | Length ratio r = \|P\|/\|V\| (Telugu prose ÷ verse), pass if 0.8 ≤ r ≤ 2.5; distribution (Table 14) | 99.1%, mean 1.63, median 1.61 | `level2_length_ratio.py` |
| 3 | LaBSE cosine, Telugu meaning ↔ English meaning ≥ 0.65 (the gate); distribution (Table 17) | 77.1%, mean 0.721 | `level3_semantic_fidelity.py` |
| 3 | mSBERT-mpnet cosine for poem↔Te, poem↔En, Te↔En (Table 15) | 63.7 / 4.4 / 23.7% | `level3_semantic_fidelity.py` |
| 3 | L3Cube-IndicSBERT cosine for the same three pairs (Table 16) | 40.1 / 0.0 / 21.0% | `level3_semantic_fidelity.py` |
| 4 | Corpus TTR (V/N) | 0.491 | `level4_lexical_diversity.py` |
| 4 | Corpus MATTR (window 50) | 0.501 | `level4_lexical_diversity.py` |
| 4 | Yule's K | 3.497 | `level4_lexical_diversity.py` |
| 4 | Honoré's H | 6,164.7 | `level4_lexical_diversity.py` |
| 4 | Hapax ratio V₁/V | 0.804 | `level4_lexical_diversity.py` |
| 4 | Sichel's S = V₂/V | 0.091 | `level4_lexical_diversity.py` |
| 4 | Per-poem TTR / MATTR(w=2) / Yule's K / Honoré's H (means) | 0.993 / 1.000 / 22.74 / 2,356.4 | `level4_lexical_diversity.py` |
| 4 | Gemma 3 Telugu "coverage": Telugu vocab tokens the corpus uses | 74.4% (1,328/1,784), 804,671 tokens | `level4_subword_coverage.py` |
| 4 | Per-poem subword TTR (mean) | 0.897 | `level4_subword_coverage.py` |
| 4 | Exact duplicates; near-duplicates "under normalisation" | 0; 160 poems in 79 groups | `level4_duplicates.py` |
| 1–3 | Pass all of levels 1–3 | 68.9% | `cross_level_summary.py` |
| 5 | LLM-as-a-judge (Gemini 3 Pro, 1–5 rubric, n=250) | 97.0% | **not implemented (by request)** |

Table 3 (per-source "Master (Validated)" counts and purity) is reproduced by
`build_subsets.py`.

## Sense checks added to each level

| Script | Check | Question it answers |
|---|---|---|
| `level1_prosodic_integrity.py` | Independent re-scan with this repo's `meter_engine/chandohasam` (forced dvipada), per-rule agreement, 181 paper-rejected couplets as a control | Is "100%" a property of the corpus, or of the particular scanner that also built it? |
| `level1_chance_pass_rates.py` | Prāsa and yati pass rates for akshara pairs taken from unrelated lines | How hard is each rule to satisfy by chance? |
| `level2_length_ratio.py` | Same gate on shuffled and same-source neighbour pairs; four length units | Can the gate tell a right gloss from a wrong one? |
| `level3_semantic_fidelity.py` | Shuffled and neighbour controls, AUC, retrieval recall@1 over 2,000 candidates | Does a similarity score separate true pairings from wrong ones? |
| `level4_lexical_diversity.py` | Telugu-prose and English-prose control corpora at equal token count, TTR growth curve, MATTR by window | Are the reference ranges the paper compares against valid for this corpus? |
| `level4_subword_coverage.py` | Fertility (tokens per word and per akshara), share of token boundaries inside an akshara | Does "coverage" measure tokenizer fit? |
| `level4_duplicates.py` | Normalisation variants, MinHash near-duplicates, reused pādas, reused glosses | What are the "near-duplicates", and what other repetition is there? |

## Layout

```
data_sanity_metrics/
├── config.py                      paths, thresholds, the paper's reported numbers
├── common/
│   ├── dataset.py                 loading, subsets, field cleaning
│   ├── telugu.py                  words, aksharas, normalisation
│   ├── lexical.py                 TTR, MATTR, Yule's K, Honoré's H, hapax, Sichel's S
│   ├── embeddings.py              cached sentence encoding, AUC, retrieval
│   ├── scanners.py                paper's analyser and chandohasam behind one interface
│   ├── minhash.py                 MinHash-LSH near-duplicate search
│   └── io.py                      JSON output, console tables
├── build_subsets.py               step 0: all / schema_a / master subsets
├── level1_prosodic_integrity.py
├── level1_chance_pass_rates.py
├── level2_length_ratio.py
├── level3_semantic_fidelity.py
├── level4_lexical_diversity.py
├── level4_subword_coverage.py
├── level4_duplicates.py
├── cross_level_summary.py
├── run_all.sh
├── outputs/                       one JSON per script (outputs/cache/ is gitignored)
└── report.md                      findings
```

## Requirements

- **Dataset**: `dwipada_consolidated.json` from
  [indicnuerosym](https://github.com/samvarankashyap/indicnuerosym) (Git LFS,
  sha256 `4f63ed94…cdab99`; the scripts check it). Default path
  `~/Downloads/dwipada_consolidated.json`; override with `DSM_DATASET=…`.
- **Paper's scanner**: a checkout of the same repo for `dwipada_analyser.py`.
  Default `~/workspace/indicnuerosym-main`; override with `DSM_INDICNEUROSYM_REPO=…`.
- **Python**: the repo `.venv` plus `sentence-transformers` (installed).
- **Models** (downloaded once from the HF Hub): `sentence-transformers/LaBSE`,
  `sentence-transformers/paraphrase-multilingual-mpnet-base-v2`,
  `l3cube-pune/indic-sentence-bert-nli`, and the Gemma 3 tokenizer
  (`unsloth/gemma-3-1b-it`, an ungated copy of `google/gemma-3-1b-it`'s tokenizer).

## Running

```bash
cd data_sanity_metrics
bash run_all.sh                     # everything, in order
# or one level at a time:
../.venv/bin/python build_subsets.py
../.venv/bin/python level2_length_ratio.py
```

Every script prints its tables and writes `outputs/<script>.json`. The
chandohasam re-scan takes about 15 minutes on 14 workers; its result is cached,
so re-runs are instant. Level 3 encodes 4 × 27,881 texts per model on the GPU
(about 2 GB of GPU memory).
