# The poetics suite on every poem source

Written by `score_sources.py` (`outputs/sources/<source>.json`, `outputs/sources/summary.json`). Medians of each metric's main value (a few showpieces pull some means far off: two textbook examples reach anuprāsa A = 50 and 176); in brackets the share of poems at the label named in the column. Means, quantiles, per-metre breakdowns, every label's share and every poem's scores are in the source's JSON.

Directions: anuprāsa A higher = more repeated consonant patterns; mādhurya M higher = softer; ojas higher = denser; prasāda surprisal higher = more obscure (lower = clearer); chandas skill 1 = exactly in metre.

| source | kind | poems | anuprāsa 3.0 A [strong] | mādhurya M [harsh] | ojas [dense] | prasāda surprisal [clear] | chandas skill [exact] |
|---|---|---:|---|---|---|---|---|
| `dataset_bhagavatam` | human | 7366 | 1.038 [15%] | -0.036 [10%] | 43.125 [9%] | 5.770 [13%] | 1.000 [100%] |
| `dataset_vemana` | human | 1164 | 1.000 [24%] | 0.030 [7%] | 41.509 [3%] | 5.593 [17%] | 1.000 [84%] |
| `dataset_kuchimanchi_timmakavi` | human | 1642 | 1.071 [22%] | -0.038 [11%] | 39.655 [5%] | 6.391 [2%] | 1.000 [93%] |
| `dataset_chandassu` | human | 2532 | 1.197 [38%] | -0.038 [10%] | 42.857 [11%] | 6.158 [4%] | 1.000 [81%] |
| `human_evals_study1_bhagavatam` | human | 227 | 1.096 [21%] | -0.066 [15%] | 43.750 [22%] | 6.164 [6%] | 1.000 [100%] |
| `human_evals_study1_vemana` | human | 47 | 1.120 [30%] | 0.030 [13%] | 41.509 [4%] | 5.696 [11%] | 1.000 [96%] |
| `human_evals_study1_kuchimanchi` | human | 70 | 1.095 [27%] | -0.081 [10%] | 41.250 [26%] | 6.794 [3%] | 1.000 [100%] |
| `human_evals_study1_textbook` | human | 72 | 1.083 [25%] | -0.093 [18%] | 45.161 [36%] | 6.257 [8%] | 1.000 [100%] |
| `human_evals_study1_gemini` | ai | 84 | 1.113 [12%] | -0.041 [5%] | 37.273 [0%] | 6.042 [4%] | 1.000 [100%] |
| `human_evals_study2_mdlm523m_ft` | ai | 33 | 1.143 [30%] | -0.028 [15%] | 37.037 [9%] | 6.239 [6%] | 1.000 [100%] |
| `human_evals_study2_t5_1b_ft` | ai | 33 | 1.048 [24%] | -0.031 [18%] | 41.304 [12%] | 6.245 [3%] | 1.000 [100%] |
| `human_evals_study2_nandi_ft` | ai | 33 | 1.133 [24%] | -0.068 [18%] | 41.071 [6%] | 6.425 [3%] | 1.000 [100%] |

Labels: anuprāsa 3.0 none / weak / marked / strong (A against the treatise's example, 1.33); mādhurya harsh / leaning_harsh / balanced / leaning_soft / soft; ojas light / leaning_light / moderate / leaning_dense / dense; prasāda (1.0) obscure / leaning_obscure / ordinary / leaning_clear / clear; chandas distance unmetered / weak / partial / slip / exact.

## Study 2 against the gold poems of the same prompts

Each model poem minus the study-1 gold poem of its prompt (33 pairs per model): mean difference of the main value, and the share of prompts where the model's poem scores higher (for prasāda surprisal, higher is more obscure).

| model | anuprāsa 3.0 A | mādhurya M | ojas | prasāda surprisal | chandas skill |
|---|---|---|---|---|---|
| `human_evals_study2_mdlm523m_ft` | +0.600 (55% above) | -0.007 (48% above) | -3.307 (18% above) | +0.223 (52% above) | equal on every prompt |
| `human_evals_study2_t5_1b_ft` | +0.140 (52% above) | -0.030 (55% above) | -0.229 (39% above) | +0.386 (64% above) | equal on every prompt |
| `human_evals_study2_nandi_ft` | -0.054 (48% above) | -0.067 (42% above) | -0.568 (30% above) | +0.630 (70% above) | equal on every prompt |

