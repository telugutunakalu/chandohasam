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

69 of the judged study-2 poems have ratings from these raters. Q13 (coherence) is not asked of the judge.

| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |
|---|---|---|---|---|---|---|---|---|
| readability | 52 | 0.464 | 0.406 (0.328 to 0.653) | yes | 0.211 | 0.254 | 1/17/20/57/4 | 9/20/53/33/25 |
| comprehension | 52 | 0.396 | 0.336 (0.321 to 0.592) | yes | 0.034 | 0.057 | 3/38/50/8/0 | 40/67/29/4/0 |
| lexical | 52 | 0.543 | 0.593 (0.58 to 0.594) | no | 0.368 | 0.244 | 0/3/32/56/8 | 8/37/53/32/10 |
| bhavam | 52 | 0.141 | 0.539 (0.448 to 0.545) | no | 0.305 | -0.186 | 2/3/3/18/73 | 58/57/23/2/0 |
| poetic | 52 | 0.149 | 0.405 (0.372 to 0.419) | no | 0.069 | -0.248 | 5/8/27/56/3 | 79/39/15/7/0 |

| question | poems | judge = human majority | κ | humans' pairwise agreement | yes: humans | yes: judge |
|---|---|---|---|---|---|---|
| chandassu | 68 | 0.912 | 0.0 | 0.989 | 0.993 | 0.889 |
| prasa | 52 | 0.942 | 0.0 | 1 | 1 | 0.944 |
| yati | 68 | 0.956 | 0.0 | 0.989 | 0.993 | 0.939 |
| shabdalankara | 64 | 0.125 | -0.064 | 0.567 | 0.179 | 0.808 |
| arthalankara | 66 | 0.47 | 0.025 | 0.789 | 0.093 | 0.576 |
| register | 69 | 1.0 | None | 0.978 | 0.993 | 1 |
| ai_generated | 68 | 0.25 | 0.017 | 0.944 | 0.964 | 0.232 |

| model | poems | rated | readability H / J | comprehension H / J | lexical H / J | bhavam H / J | poetic H / J | AI flag H / J |
|---|---|---|---|---|---|---|---|---|
| mdlm523m_ft | 33 | 18 | 3.333 / 3.515 | 2.028 / 2.636 | 3.056 / 3.727 | 1.75 / 4.394 | 1.583 / 3.182 | 0.972 / 0.333 |
| nandi_ft | 33 | 25 | 3.34 / 3.515 | 1.88 / 2.667 | 2.9 / 3.667 | 1.52 / 4.758 | 1.54 / 3.697 | 0.96 / 0.091 |
| t5_1b_ft | 33 | 26 | 3.296 / 3.364 | 2.037 / 2.606 | 3.037 / 3.697 | 2.037 / 4.606 | 1.778 / 3.455 | 0.963 / 0.273 |
