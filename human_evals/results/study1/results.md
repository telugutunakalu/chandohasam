# Study 1, group A (A5, A3, A1)

Snapshot: annotations-paper-snapshot-2026-10-30-study1-final.db; latest rating 2026-10-30T07:10:06+00:00.

## 0. Data

All annotators: 544 ratings; group A 310, group B 234 (left out below).

- A5: 101 ratings, calibration 25/25
- A3: 103 ratings, calibration 25/25
- A1: 106 ratings, calibration 25/25

Poems rated by group A: 116; by number of raters: {1: 16, 2: 6, 3: 94}
Poems per source group: {'real poets': 75, 'textbook reference': 20, 'generated (Gemini)': 21}
Poems per source: {'bhagavatam': 35, 'reference': 20, 'generated': 21, 'kuchimanchi': 20, 'vemana': 20}
Ratings per source group: {'real poets': 190, 'textbook reference': 59, 'generated (Gemini)': 61}

## 1. Agreement (group A)

| # | question | level | poems ≥2 | α | 95% CI | exact agree | AC1 | mean % yes / mean |
|---|---|---|---|---|---|---|---|---|
| 1 | readability | ordinal | 100 | 0.333 | 0.202 – 0.451 | 0.487 | – | 4.235 |
| 2 | comprehension | ordinal | 100 | 0.485 | 0.352 – 0.593 | 0.377 | – | 3.500 |
| 3 | lexical | ordinal | 100 | 0.442 | 0.305 – 0.569 | 0.497 | – | 4.016 |
| 4 | bhavam | ordinal | 100 | 0.432 | 0.263 – 0.562 | 0.507 | – | 4.358 |
| 5 | chandassu | nominal | 100 | – | – | 1.000 | 1.000 | 1.000 |
| 6 | prasa | nominal | 74 | – | – | 1.000 | 1.000 | 1.000 |
| 7 | yati | nominal | 100 | 0.000 | -0.010 – 0.000 | 0.993 | 0.993 | 0.997 |
| 8 | shabdalankara | nominal | 100 | 0.009 | -0.115 – 0.128 | 0.517 | 0.051 | 0.448 |
| 9 | arthalankara | nominal | 100 | 0.030 | -0.085 – 0.137 | 0.517 | 0.042 | 0.477 |
| 10 | poetic | ordinal | 100 | 0.342 | 0.203 – 0.460 | 0.317 | – | 3.745 |
| 11 | register | nominal | 100 | 0.331 | 0.185 – 0.467 | 0.770 | 0.651 | 0.782 |
| 12 | ai_generated | nominal | 100 | 0.529 | 0.352 – 0.677 | 0.887 | 0.851 | 0.144 |

On the 1–5 questions beside α:

| question | Spearman ρ, 3 pairs (n) | mean ρ | interval α centred | reliability of mean of 3 | ±1 agree |
|---|---|---|---|---|---|
| readability | A5–A3 0.43 (100), A5–A1 0.32 (94), A3–A1 0.54 (94) | 0.43 | 0.432 | 0.60 | 0.883 |
| comprehension | A5–A3 0.47 (100), A5–A1 0.47 (94), A3–A1 0.58 (94) | 0.51 | 0.492 | 0.74 | 0.883 |
| lexical | A5–A3 0.42 (100), A5–A1 0.35 (94), A3–A1 0.68 (94) | 0.48 | 0.483 | 0.70 | 0.890 |
| bhavam | A5–A3 0.60 (100), A5–A1 0.51 (94), A3–A1 0.44 (94) | 0.51 | 0.564 | 0.69 | 0.923 |
| poetic | A5–A3 0.54 (100), A5–A1 0.25 (94), A3–A1 0.42 (94) | 0.40 | 0.422 | 0.61 | 0.853 |

Calibration poems only (all three rated):

| question | α (25 calibration poems) | α (other poems) |
|---|---|---|
| readability | 0.228 | 0.335 |
| comprehension | 0.223 | 0.559 |
| lexical | 0.331 | 0.484 |
| bhavam | 0.351 | 0.458 |
| chandassu | – | – |
| prasa | – | – |
| yati | – | 0.000 |
| shabdalankara | 0.051 | -0.014 |
| arthalankara | 0.098 | 0.011 |
| poetic | 0.541 | 0.273 |
| register | 0.804 | 0.207 |
| ai_generated | 0.310 | 0.584 |

## 2. Sources

Annotator-centred difference of poem means (1–5), 95% bootstrap over poems; ✱ = interval excludes 0.

| question | Gemini − poets | 95% CI | textbook − poets | 95% CI | poems (G / T / P) |
|---|---|---|---|---|---|
| readability | +0.57✱ | [+0.38, +0.75] | -0.26✱ | [-0.52, -0.01] | 21 / 20 / 75 |
| comprehension | +0.67✱ | [+0.32, +1.02] | -0.35✱ | [-0.67, -0.03] | 21 / 20 / 75 |
| lexical | +0.50✱ | [+0.26, +0.75] | -0.47✱ | [-0.73, -0.20] | 21 / 20 / 75 |
| bhavam | -1.57✱ | [-1.89, -1.23] | -0.02 | [-0.25, +0.17] | 21 / 20 / 75 |
| poetic | -1.00✱ | [-1.24, -0.75] | -0.30 | [-0.74, +0.12] | 21 / 20 / 75 |

Mean as rated per source (poem means):

| question | bhagavatam | vemana | kuchimanchi | textbook | generated |
|---|---|---|---|---|---|
| readability | 3.93 (35) | 4.82 (20) | 3.88 (20) | 3.94 (20) | 4.78 (21) |
| comprehension | 3.27 (35) | 4.28 (20) | 2.97 (20) | 3.10 (20) | 4.13 (21) |
| lexical | 3.89 (35) | 4.77 (20) | 3.48 (20) | 3.55 (20) | 4.54 (21) |
| bhavam | 4.58 (35) | 4.89 (20) | 4.64 (20) | 4.67 (20) | 3.13 (21) |
| poetic | 4.19 (35) | 3.92 (20) | 3.97 (20) | 3.71 (20) | 3.00 (21) |

Yes-rates per source group (ratings), Wilson 95%:

| question | poets | textbook | Gemini |
|---|---|---|---|
| chandassu | 190/190 = 100.0% [98–100] | 59/59 = 100.0% [94–100] | 61/61 = 100.0% [94–100] |
| prasa | 129/129 = 100.0% [97–100] | 53/53 = 100.0% [93–100] | 49/49 = 100.0% [93–100] |
| yati | 189/190 = 99.5% [97–100] | 59/59 = 100.0% [94–100] | 61/61 = 100.0% [94–100] |
| shabdalankara | 87/190 = 45.8% [39–53] | 29/59 = 49.2% [37–62] | 23/61 = 37.7% [27–50] |
| arthalankara | 99/190 = 52.1% [45–59] | 34/59 = 57.6% [45–69] | 15/61 = 24.6% [16–37] |
| register | 147/178 = 82.6% [76–87] | 57/59 = 96.6% [88–99] | 29/61 = 47.5% [36–60] |
| ai_generated | 1/178 = 0.6% [0–3] | 4/59 = 6.8% [3–16] | 38/61 = 62.3% [50–73] |

## 3. AI detection per annotator

| annotator | Gemini flagged | others flagged |
|---|---|---|
| A5 | 11/21 | 3/80 |
| A3 | 13/20 | 1/83 |
| A1 | 14/20 | 1/74 |
| group A | 38/61 = 62.3% | 5/237 = 2.1% |

Gemini poems: 21 rated; flagged by a majority of their group-A raters: 15; by any: 19

## 4. Q4 re-rating (answers cleared 2026-10-29, rated again)

| annotator | poems | same | within 1 | mean old → new | quadratic κ | Spearman |
|---|---|---|---|---|---|---|
| A5 | 101 | 0.634 | 0.871 | 4.59 → 4.55 | 0.361 | 0.307 |
| A3 | 102 | 0.353 | 0.716 | 4.18 → 4.14 | -0.038 | -0.021 |

## 5. Drift

Residual = answer − the other group-A raters' mean on the same poem; first vs second half of each annotator's ratings by creation time.

| annotator | question | n | first half | second half | change |
|---|---|---|---|---|---|
| A5 | readability | 50 + 50 | +0.78 | +0.37 | -0.41 |
| A5 | comprehension | 50 + 50 | +0.42 | -0.37 | -0.79 |
| A5 | lexical | 50 + 50 | +0.67 | +0.14 | -0.53 |
| A5 | bhavam | 50 + 50 | +0.47 | +0.14 | -0.33 |
| A5 | poetic | 50 + 50 | -0.18 | -0.67 | -0.49 |
| A3 | readability | 51 + 49 | -0.25 | -0.14 | +0.10 |
| A3 | comprehension | 51 + 49 | +0.07 | -0.23 | -0.30 |
| A3 | lexical | 51 + 49 | -0.37 | -0.27 | +0.11 |
| A3 | bhavam | 51 + 49 | -0.16 | -0.46 | -0.30 |
| A3 | poetic | 51 + 49 | +0.02 | -0.04 | -0.06 |
| A1 | readability | 44 + 50 | -0.43 | -0.38 | +0.05 |
| A1 | comprehension | 44 + 50 | -0.17 | +0.26 | +0.43 |
| A1 | lexical | 44 + 50 | -0.28 | +0.08 | +0.36 |
| A1 | bhavam | 44 + 50 | -0.33 | +0.29 | +0.62 |
| A1 | poetic | 44 + 50 | +0.27 | +0.63 | +0.36 |

α (group A) on the ratings made up to each date:

| up to | ratings | poems ≥2 | readability | comprehension | lexical | bhavam | poetic |
|---|---|---|---|---|---|---|---|
| 2026-10-13 | 9 | 0 | – | – | – | – | – |
| 2026-10-15 | 12 | 1 | – | 0.000 | – | – | 0.000 |
| 2026-10-18 | 54 | 3 | 0.778 | 0.086 | 0.778 | 0.778 | 0.571 |
| 2026-10-19 | 76 | 16 | 0.590 | 0.288 | 0.725 | 0.573 | 0.473 |
| 2026-10-21 | 86 | 16 | 0.590 | 0.288 | 0.725 | 0.573 | 0.473 |
| 2026-10-26 | 140 | 33 | 0.167 | 0.200 | 0.293 | 0.378 | 0.393 |
| 2026-10-28 | 304 | 100 | 0.328 | 0.481 | 0.447 | 0.433 | 0.375 |
| 2026-10-29 | 305 | 100 | 0.328 | 0.481 | 0.447 | 0.433 | 0.375 |
| 2026-10-30 | 310 | 100 | 0.333 | 0.485 | 0.442 | 0.432 | 0.342 |
