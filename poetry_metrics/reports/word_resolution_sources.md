# Word resolution on every poem source

Written by `word_resolution_sources.py` (`outputs/word_resolution/<source>.json`, `summary.json`). Mean share of a poem's tokens that resolve to dictionary headwords, over the source's poems. **Resolved** is the live path with the verified ByT5 gate, the paper's reading; *as shipped* counts a ByT5 analysis without looking its headwords up; *dictionary only* drops ByT5 and bare stems; *with table* lets the corpus table answer first (it holds the dataset poems' own words). By-metre means, class shares, the most frequent unresolved words and every poem's readings are in the source's JSON.

| source | kind | poems | tokens | **resolved** | as shipped | dictionary only | with table, verified | attested | tokens ByT5 resolves (as shipped) | unresolved types |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `dataset_bhagavatam` | human | 7366 | 103,821 | **86.7%** | 99.3% | 38.4% | 86.6% | 98.8% | 55.2% | 12,538 |
| `dataset_vemana` | human | 1164 | 14,730 | **87.2%** | 99.7% | 37.6% | 92.9% | 99.8% | 51.9% | 840 |
| `dataset_kuchimanchi_timmakavi` | human | 1642 | 31,045 | **88.5%** | 99.5% | 52.4% | 88.7% | 99.3% | 44.4% | 3,236 |
| `dataset_chandassu` | human | 2532 | 54,471 | **87.2%** | 99.4% | 42.8% | 87.2% | 99.3% | 52.5% | 5,558 |
| `human_evals_study1_bhagavatam` | human | 227 | 3,767 | **85.8%** | 99.3% | 35.7% | 84.9% | 98.7% | 57.0% | 519 |
| `human_evals_study1_vemana` | human | 47 | 621 | **90.1%** | 99.8% | 48.5% | 92.4% | 99.6% | 44.9% | 44 |
| `human_evals_study1_kuchimanchi` | human | 70 | 1,422 | **86.6%** | 99.2% | 48.3% | 86.2% | 99.2% | 48.2% | 182 |
| `human_evals_study1_textbook` | human | 72 | 1,091 | **77.7%** | 97.8% | 36.2% | 79.0% | 95.1% | 52.3% | 186 |
| `human_evals_study1_gemini` | ai | 84 | 2,002 | **96.5%** | 100.0% | 78.3% | 95.2% | 99.9% | 17.9% | 55 |
| `human_evals_study2_mdlm523m_ft` | ai | 33 | 729 | **85.6%** | 99.9% | 57.3% | 84.1% | 99.2% | 35.9% | 103 |
| `human_evals_study2_t5_1b_ft` | ai | 33 | 617 | **84.4%** | 99.7% | 52.2% | 82.1% | 99.7% | 43.4% | 100 |
| `human_evals_study2_nandi_ft` | ai | 33 | 534 | **79.2%** | 98.4% | 41.5% | 78.1% | 97.9% | 53.4% | 115 |
| `gemini_initial_evals` | ai | 246 | 6,112 | **96.1%** | 100.0% | 74.1% | 95.0% | 99.8% | 22.4% | 153 |

## Study 2 against the gold poems of the same prompts

Each model poem minus the study-1 gold poem of its prompt (33 pairs per model), in points of the share of tokens; in brackets the share of prompts where the model's poem resolves more.

| model | **resolved** | as shipped | dictionary only | with table, verified |
|---|---|---|---|---|
| `human_evals_study2_mdlm523m_ft` | -2.0 (48%) | +0.1 (3%) | +9.9 (70%) | -3.8 (42%) |
| `human_evals_study2_t5_1b_ft` | -3.2 (33%) | -0.2 (3%) | +4.9 (58%) | -5.8 (30%) |
| `human_evals_study2_nandi_ft` | -8.5 (21%) | -1.5 (3%) | -5.8 (45%) | -9.8 (27%) |

