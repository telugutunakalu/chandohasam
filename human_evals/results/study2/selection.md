# Study 2: prompt selection

Method: build_study2_pool.py. 44 eligible prompts; excluded: gold rated by fewer than 4 44; a model poem out of metre, repeating a line, copying or empty 2. Chosen 33 prompts × 3 models = 99 poems.

| chosen | source | metre | gold (he_) | raters | gold score | p(real) mdlm523m_ft | p(real) t5_1b_ft | p(real) nandi_ft | z gold | z AI | score |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ✔ | bhagavatam | mattebhavikriditamu | he_0072 | 5 | +0.01 | 0.70 | 0.64 | 0.75 | +0.80 | +2.38 | +3.17 |
| ✔ | bhagavatam | mattebhavikriditamu | he_0494 | 5 | +0.21 | 0.05 | 0.41 | 0.74 | +1.55 | +0.73 | +2.27 |
| ✔ | bhagavatam | champakamala | he_0100 | 5 | +0.05 | 0.13 | 0.78 | 0.36 | +0.95 | +0.85 | +1.79 |
| ✔ | bhagavatam | champakamala | he_0117 | 5 | -0.15 | 0.11 | 0.07 | 0.63 | +0.20 | -0.02 | +0.18 |
| ✔ | bhagavatam | sardulavikriditamu | he_0081 | 5 | -0.11 | 0.36 | 0.15 | 0.13 | +0.35 | -0.32 | +0.03 |
| ✔ | bhagavatam | manini | he_0141 | 5 | -0.15 | 0.05 | 0.07 | 0.29 | +0.20 | -0.76 | -0.57 |
| ✔ | bhagavatam | sragdhara | he_0488 | 5 | -0.31 | 0.00 | 0.30 | 0.06 | -0.41 | -0.86 | -1.27 |
| ✔ | bhagavatam | upendravajra | he_0449 | 5 | -0.31 | 0.07 | 0.21 | 0.05 | -0.41 | -0.90 | -1.30 |
| ✔ | bhagavatam | layavibhati | he_0071 | 5 | -0.51 | 0.09 | 0.17 | 0.07 | -1.16 | -0.91 | -2.07 |
| ✔ | bhagavatam | layagrahi | he_0133 | 5 | -0.75 | 0.15 | 0.44 | 0.13 | -2.06 | -0.18 | -2.24 |
| ✔ | kuchimanchi_timmakavi | champakamala | he_0270 | 5 | -0.03 | 0.83 | 0.71 | 0.29 | +0.71 | +2.14 | +2.85 |
| ✔ | kuchimanchi_timmakavi | tetagiti | he_0259 | 5 | +0.21 | 0.04 | 0.83 | 0.54 | +1.47 | +1.11 | +2.58 |
| ✔ | kuchimanchi_timmakavi | champakamala | he_0093 | 5 | +0.21 | 0.55 | 0.40 | 0.27 | +1.47 | +0.64 | +2.10 |
| ✔ | kuchimanchi_timmakavi | utpalamala | he_0329 | 5 | -0.07 | 0.23 | 0.68 | 0.22 | +0.59 | +0.41 | +1.00 |
| ✔ | kuchimanchi_timmakavi | madhuragati_ragada | he_0311 | 5 | -0.23 | 0.78 | 0.38 | 0.16 | +0.09 | +0.89 | +0.98 |
| ✔ | kuchimanchi_timmakavi | tetagiti | he_0357 | 5 | +0.01 | 0.17 | 0.55 | 0.17 | +0.84 | -0.16 | +0.68 |
| ✔ | kuchimanchi_timmakavi | madhuragati_ragada | he_0469 | 5 | -0.27 | 0.16 | 0.71 | 0.30 | -0.04 | +0.53 | +0.49 |
| ✔ | kuchimanchi_timmakavi | malini | he_0205 | 5 | -0.19 | 0.10 | 0.45 | 0.13 | +0.21 | -0.71 | -0.50 |
| ✔ | kuchimanchi_timmakavi | pamcacamaramu | he_0387 | 5 | -0.35 | 0.11 | 0.31 | 0.24 | -0.29 | -0.74 | -1.03 |
| ✔ | kuchimanchi_timmakavi | kandamu | he_0347 | 5 | -0.39 | 0.22 | 0.06 | 0.39 | -0.41 | -0.70 | -1.12 |
| ✔ | kuchimanchi_timmakavi | mattebhavikriditamu | he_0029 | 5 | -0.79 | 0.42 | 0.31 | 0.39 | -1.67 | +0.38 | -1.29 |
|  | kuchimanchi_timmakavi | totakamu | he_0302 | 4 | -0.34 | 0.12 | 0.03 | 0.27 | -0.26 | -1.32 | -1.58 |
|  | kuchimanchi_timmakavi | mattakokilamu | he_0323 | 5 | -0.43 | 0.09 | 0.27 | 0.10 | -0.54 | -1.20 | -1.74 |
|  | kuchimanchi_timmakavi | bhujangaprayatamu | he_0092 | 5 | -0.95 | 0.12 | 0.08 | 0.24 | -2.17 | -1.27 | -3.44 |
| ✔ | vemana | ataveladi | he_0307 | 5 | +0.53 | 0.09 | 0.47 | 0.82 | +0.68 | +1.64 | +2.32 |
| ✔ | vemana | ataveladi | he_0341 | 5 | +0.69 | 0.04 | 0.06 | 0.95 | +1.56 | +0.58 | +2.13 |
| ✔ | vemana | ataveladi | he_0104 | 5 | +0.61 | 0.24 | 0.59 | 0.28 | +1.12 | +0.78 | +1.90 |
| ✔ | vemana | kandamu | he_0425 | 5 | +0.45 | 0.27 | 0.57 | 0.53 | +0.24 | +1.62 | +1.86 |
| ✔ | vemana | tetagiti | he_0416 | 5 | +0.57 | 0.07 | 0.11 | 0.72 | +0.90 | +0.07 | +0.97 |
| ✔ | vemana | tetagiti | he_0107 | 5 | +0.33 | 0.16 | 0.22 | 0.89 | -0.42 | +1.29 | +0.87 |
| ✔ | vemana | tetagiti | he_0112 | 5 | +0.49 | 0.04 | 0.34 | 0.53 | +0.46 | +0.11 | +0.57 |
| ✔ | vemana | kandamu | he_0199 | 5 | +0.45 | 0.24 | 0.16 | 0.57 | +0.24 | +0.31 | +0.55 |
| ✔ | vemana | utpalamala | he_0457 | 5 | +0.53 | 0.24 | 0.18 | 0.41 | +0.68 | -0.16 | +0.52 |
| ✔ | vemana | kandamu | he_0244 | 4 | +0.51 | 0.19 | 0.24 | 0.39 | +0.56 | -0.17 | +0.39 |
| ✔ | vemana | ataveladi | he_0444 | 5 | +0.57 | 0.08 | 0.31 | 0.30 | +0.90 | -0.62 | +0.28 |
| ✔ | vemana | kandamu | he_0031 | 4 | +0.31 | 0.22 | 0.09 | 0.73 | -0.53 | +0.54 | +0.01 |
|  | vemana | kandamu | he_0392 | 4 | +0.31 | 0.08 | 0.34 | 0.33 | -0.53 | -0.41 | -0.95 |
|  | vemana | kandamu | he_0041 | 5 | +0.17 | 0.18 | 0.56 | 0.24 | -1.29 | +0.33 | -0.96 |
|  | vemana | ataveladi | he_0045 | 5 | +0.53 | 0.03 | 0.25 | 0.08 | +0.68 | -1.69 | -1.01 |
|  | vemana | tetagiti | he_0319 | 5 | +0.09 | 0.13 | 0.29 | 0.58 | -1.73 | +0.40 | -1.33 |
|  | vemana | ataveladi | he_0294 | 5 | +0.45 | 0.05 | 0.09 | 0.20 | +0.24 | -1.74 | -1.50 |
|  | vemana | kandamu | he_0239 | 4 | +0.21 | 0.04 | 0.40 | 0.13 | -1.08 | -0.98 | -2.06 |
|  | vemana | ataveladi | he_0144 | 5 | +0.37 | 0.03 | 0.12 | 0.12 | -0.20 | -1.99 | -2.18 |
|  | vemana | champakamala | he_0280 | 4 | -0.04 | 0.08 | 0.28 | 0.54 | -2.45 | +0.06 | -2.39 |
