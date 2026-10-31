# LLM judge (gemma4-26b) against the human annotators

148 study-1 poems judged (0 invalid replies left out); method: judge_vs_human.py.

## 1–5 scales

| scale | poems (≥ 2 raters) | judge ρ with the human mean | human ρ, median (range) | passes | α humans | α with the judge | judge's scores 1/2/3/4/5 | humans' scores 1/2/3/4/5 |
|---|---|---|---|---|---|---|---|---|
| readability | 102 | 0.662 | 0.474 (0.347 to 0.611) | yes | 0.139 | 0.132 | 0/8/19/93/28 | 0/7/71/133/328 |
| comprehension | 102 | 0.658 | 0.5 (0.309 to 0.636) | yes | 0.223 | 0.116 | 1/30/73/42/2 | 2/52/127/172/186 |
| lexical | 102 | 0.75 | 0.497 (0.338 to 0.686) | yes | 0.322 | 0.323 | 1/0/24/82/41 | 1/17/84/211/226 |
| bhavam | 102 | 0.201 | 0.476 (-0.001 to 0.533) | no | 0.096 | 0.062 | 1/0/0/8/139 | 4/15/44/96/380 |
| poetic | 102 | 0.531 | 0.327 (-0.265 to 0.537) | yes | 0.053 | 0.067 | 2/3/20/106/17 | 3/30/125/213/168 |

## Yes/no questions

| question | poems | judge = human majority | κ | humans' pairwise agreement | yes: humans | yes: judge |
|---|---|---|---|---|---|---|
| chandassu | 148 | 0.966 | 0.0 | 1 | 1 | 0.966 |
| prasa | 111 | 0.964 | 0.0 | 1 | 1 | 0.964 |
| yati | 148 | 1.0 | None | 0.989 | 0.994 | 1 |
| shabdalankara | 144 | 0.528 | 0.032 | 0.456 | 0.501 | 0.932 |
| arthalankara | 141 | 0.624 | 0.183 | 0.474 | 0.525 | 0.662 |
| register | 134 | 0.91 | 0.464 | 0.796 | 0.824 | 0.959 |
| ai_generated | 134 | 0.851 | 0.282 | 0.881 | 0.082 | 0.189 |

## By source (means; humans raw)

| source | poems | readability H / J | comprehension H / J | lexical H / J | bhavam H / J | poetic H / J | AI flag H / J |
|---|---|---|---|---|---|---|---|
| bhagavatam | 53 | 4.187 / 3.755 | 3.627 / 2.925 | 4.007 / 3.868 | 4.597 / 4.943 | 4.157 / 3.943 | 0.016 / 0.075 |
| generated | 23 | 4.824 / 4.522 | 4.343 / 3.826 | 4.608 / 4.783 | 3.843 / 4.957 | 3.5 / 3.696 | 0.363 / 0.913 |
| kuchimanchi | 26 | 4.183 / 3.769 | 3.5 / 2.923 | 3.769 / 3.885 | 4.644 / 4.923 | 4.029 / 4.038 | 0 / 0.038 |
| reference | 24 | 4.304 / 3.583 | 3.667 / 2.417 | 3.912 / 3.583 | 4.735 / 4.75 | 3.961 / 3.542 | 0.039 / 0.083 |
| vemana | 22 | 4.866 / 4.455 | 4.515 / 3.682 | 4.773 / 4.727 | 4.907 / 5 | 4.052 / 4.227 | 0 / 0 |

Gemini − poets: readability: humans (centred) +0.33, judge +0.61; comprehension: humans (centred) +0.46, judge +0.74; lexical: humans (centred) +0.40, judge +0.72; bhavam: humans (centred) -0.80, judge +0.01; poetic: humans (centred) -0.58, judge -0.33

## Study 2: the judge on each model's poems against their gold poems

| model | pairs | readability model / gold | comprehension model / gold | lexical model / gold | bhavam model / gold | poetic model / gold | AI flag model / gold |
|---|---|---|---|---|---|---|---|
| mdlm523m_ft | 33 | 3.515 / 4.03 | 2.636 / 3.121 | 3.727 / 4.152 | 4.394 / 5 | 3.182 / 4.273 | 0.333 / 0 |
| nandi_ft | 33 | 3.515 / 4.03 | 2.667 / 3.121 | 3.667 / 4.152 | 4.758 / 5 | 3.697 / 4.273 | 0.091 / 0 |
| t5_1b_ft | 33 | 3.364 / 4.03 | 2.606 / 3.121 | 3.697 / 4.152 | 4.606 / 5 | 3.455 / 4.273 | 0.273 / 0 |
