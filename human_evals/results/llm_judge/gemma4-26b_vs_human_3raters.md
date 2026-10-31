# LLM judge (gemma4-26b) against the human annotators

148 study-1 poems judged (0 invalid replies left out); human raters: A5, A3, A1; method: judge_vs_human.py.

## 1–5 scales

| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |
|---|---|---|---|---|---|---|---|---|
| readability | 100 | 0.671 | 0.555 (0.461 to 0.614) | yes | 0.333 | 0.367 | 0/8/19/93/28 | 0/5/59/104/142 |
| comprehension | 100 | 0.673 | 0.58 (0.514 to 0.61) | yes | 0.485 | 0.468 | 1/30/73/42/2 | 2/49/115/80/64 |
| lexical | 100 | 0.771 | 0.642 (0.437 to 0.65) | yes | 0.442 | 0.491 | 1/0/24/82/41 | 1/15/70/116/108 |
| bhavam | 100 | 0.208 | 0.499 (0.453 to 0.607) | no | 0.432 | 0.207 | 1/0/0/8/139 | 4/15/33/72/186 |
| poetic | 100 | 0.474 | 0.464 (0.391 to 0.61) | yes | 0.342 | 0.302 | 2/3/20/106/17 | 3/30/90/107/80 |

## Yes/no questions

| question | poems | judge = human majority | κ | humans' pairwise agreement | yes: humans | yes: judge |
|---|---|---|---|---|---|---|
| chandassu | 116 | 0.966 | 0.0 | 1 | 1 | 0.966 |
| prasa | 88 | 1.0 | None | 1 | 1 | 0.964 |
| yati | 116 | 1.0 | None | 0.993 | 0.997 | 1 |
| shabdalankara | 115 | 0.417 | 0.046 | 0.503 | 0.448 | 0.932 |
| arthalankara | 113 | 0.646 | 0.282 | 0.517 | 0.477 | 0.662 |
| register | 103 | 0.854 | 0.389 | 0.767 | 0.782 | 0.959 |
| ai_generated | 104 | 0.904 | 0.68 | 0.882 | 0.144 | 0.189 |

## By source (means; humans raw)

| source | poems | readability H / J | comprehension H / J | lexical H / J | bhavam H / J | poetic H / J | AI flag H / J |
|---|---|---|---|---|---|---|---|
| bhagavatam | 53 | 3.853 / 3.755 | 3.107 / 2.925 | 3.787 / 3.868 | 4.547 / 4.943 | 4.053 / 3.943 | 0.016 / 0.075 |
| generated | 23 | 4.77 / 4.522 | 4.098 / 3.826 | 4.525 / 4.783 | 3.066 / 4.957 | 3 / 3.696 | 0.623 / 0.913 |
| kuchimanchi | 26 | 3.914 / 3.769 | 2.983 / 2.923 | 3.5 / 3.885 | 4.638 / 4.923 | 3.966 / 4.038 | 0 / 0.038 |
| reference | 24 | 3.932 / 3.583 | 3.102 / 2.417 | 3.559 / 3.583 | 4.661 / 4.75 | 3.712 / 3.542 | 0.068 / 0.083 |
| vemana | 22 | 4.807 / 4.455 | 4.316 / 3.682 | 4.772 / 4.727 | 4.895 / 5 | 3.947 / 4.227 | 0 / 0 |

Gemini − poets: readability: humans (centred) +0.57, judge +0.50; comprehension: humans (centred) +0.67, judge +0.66; lexical: humans (centred) +0.50, judge +0.63; bhavam: humans (centred) -1.57, judge -0.01; poetic: humans (centred) -1.00, judge -0.41

## Study 2: the judge on each model's poems against their gold poems

| model | pairs | readability model / gold | comprehension model / gold | lexical model / gold | bhavam model / gold | poetic model / gold | AI flag model / gold |
|---|---|---|---|---|---|---|---|
| mdlm523m_ft | 33 | 3.515 / 4.03 | 2.636 / 3.121 | 3.727 / 4.152 | 4.394 / 5 | 3.182 / 4.273 | 0.333 / 0 |
| nandi_ft | 33 | 3.515 / 4.03 | 2.667 / 3.121 | 3.667 / 4.152 | 4.758 / 5 | 3.697 / 4.273 | 0.091 / 0 |
| t5_1b_ft | 33 | 3.364 / 4.03 | 2.606 / 3.121 | 3.697 / 4.152 | 4.606 / 5 | 3.455 / 4.273 | 0.273 / 0 |

## Study 2: the judge against the human ratings

64 of the judged study-2 poems have ratings from these raters. Q13 (coherence) is not asked of the judge.

| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |
|---|---|---|---|---|---|---|---|---|
| readability | 45 | 0.443 | 0.337 (0.263 to 0.622) | yes | 0.176 | 0.222 | 1/17/20/57/4 | 9/19/49/30/20 |
| comprehension | 45 | 0.489 | 0.382 (0.348 to 0.577) | yes | 0.082 | 0.081 | 3/38/50/8/0 | 34/64/25/4/0 |
| lexical | 45 | 0.507 | 0.555 (0.537 to 0.631) | no | 0.362 | 0.231 | 0/3/32/56/8 | 8/35/49/30/5 |
| bhavam | 45 | 0.115 | 0.585 (0.532 to 0.616) | no | 0.345 | -0.215 | 2/3/3/18/73 | 49/56/20/2/0 |
| poetic | 45 | 0.21 | 0.415 (0.372 to 0.432) | no | 0.056 | -0.267 | 5/8/27/56/3 | 71/35/14/7/0 |

| question | poems | judge = human majority | κ | humans' pairwise agreement | yes: humans | yes: judge |
|---|---|---|---|---|---|---|
| chandassu | 63 | 0.921 | 0.0 | 0.988 | 0.992 | 0.889 |
| prasa | 49 | 0.939 | 0.0 | 1 | 1 | 0.944 |
| yati | 63 | 0.952 | 0.0 | 0.988 | 0.992 | 0.939 |
| shabdalankara | 60 | 0.133 | -0.063 | 0.531 | 0.197 | 0.808 |
| arthalankara | 61 | 0.459 | 0.026 | 0.765 | 0.102 | 0.576 |
| register | 64 | 1.0 | None | 0.975 | 0.992 | 1 |
| ai_generated | 63 | 0.238 | 0.017 | 0.938 | 0.961 | 0.232 |

| model | poems | rated | readability H / J | comprehension H / J | lexical H / J | bhavam H / J | poetic H / J | AI flag H / J |
|---|---|---|---|---|---|---|---|---|
| mdlm523m_ft | 33 | 16 | 3.258 / 3.515 | 2 / 2.636 | 2.968 / 3.727 | 1.71 / 4.394 | 1.613 / 3.182 | 0.968 / 0.333 |
| nandi_ft | 33 | 23 | 3.267 / 3.515 | 1.933 / 2.667 | 2.8 / 3.667 | 1.578 / 4.758 | 1.578 / 3.697 | 0.956 / 0.091 |
| t5_1b_ft | 33 | 25 | 3.255 / 3.364 | 2.039 / 2.606 | 2.98 / 3.697 | 2.059 / 4.606 | 1.765 / 3.455 | 0.961 / 0.273 |
