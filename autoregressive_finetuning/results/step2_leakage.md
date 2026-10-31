# Step 2: leakage probe and zero-shot likelihood (FrontiersMind/Nandi-Mini-150M@31c8ace (base))

11655 val + test poems; greedy continuation of the first line; longest akshara run shared with the rest of the real poem. 1027 s.

| corpus | poems | run ≥ 12 % | run ≥ 24 % | mean run | max run |
|---|---|---|---|---|---|
| bhagavatam | 6317 | 0.0 | 0.0 | 0.9 | 6 |
| chandassu | 2532 | 0.0 | 0.0 | 1.0 | 6 |
| kuchimanchi_timmakavi | 1642 | 0.0 | 0.0 | 0.9 | 5 |
| positive control (leakage.json poem hits) | 112 | 0.0 | 0.0 | 1.2 | 4 |
| vemana | 1164 | 0.0 | 0.0 | 1.0 | 7 |
| all | 11655 | 0.0 | 0.0 | 1.0 | 7 |

Excluded from every model's evaluation (run ≥ 24): **0** poems.

| zero-shot likelihood (val) | nats |
|---|---|
| val_nll/T1 | 4.185 |
| val_nll/T0 | 4.284 |
| val_nll_tok/T1 | 5.106 |
| val_nll_tok/T0 | 5.225 |
| val_nll/bhavam_prose | 2.588 |

val_nll/*: per MDLM target token (E6's unit); val_nll_tok/*: per Nandi token. Not comparable as levels with the MDLM's NELBO (an upper bound); the T1-T0 gap is.
