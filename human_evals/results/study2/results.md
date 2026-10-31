# Human evaluation, study 2 (99 model poems): results as of 2026-10-31 15:54

99 poems: the same 33 prompts written by three fine-tuned models with the v2 metrical decoder (33 each); the AI poems only. 220 ratings (latest 2026-10-30T22:32); agreement statistics: agreement.md.

## Progress

| annotator | rated (of 99) | calibration (of 6) |
|---|---|---|
| A5 | 79 | 6 |
| A3 | 79 | 6 |
| A1 | 62 | 6 |

## Mean rating per model (poem means, as rated)

| model | ratings / poems | readability | comprehension | lexical | coherence | bhavam | poetic | chandassu | prasa | yati | shabdalankara | arthalankara | register | ai_generated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MDLM 523M | 62 / 23 | 3.62 | 2.19 | 3.30 | 1.88 | 1.77 | 1.67 | 0.99 | 1.00 | 0.99 | 0.23 | 0.09 | 0.90 | 0.99 |
| T5Gemma 2 1B | 84 / 30 | 3.56 | 2.19 | 3.12 | 2.07 | 1.99 | 1.91 | 1.00 | 1.00 | 1.00 | 0.27 | 0.19 | 0.91 | 0.95 |
| Nandi-Mini-150M | 74 / 27 | 3.36 | 2.01 | 3.06 | 1.80 | 1.64 | 1.69 | 1.00 | 1.00 | 1.00 | 0.22 | 0.12 | 0.96 | 0.95 |
| *the 33 golds, study 1* | | 4.27 | 3.49 | 4.11 | – | 4.71 | 4.02 | | | | | | | |

## Each model against the other two (annotator-centred, same prompt; bootstrap over prompts, 95%)

| model | readability | comprehension | lexical | coherence | bhavam | poetic |
|---|---|---|---|---|---|---|
| MDLM 523M | +0.13 [-0.20, +0.45] | +0.03 [-0.17, +0.25] | +0.19 [-0.08, +0.48] | -0.09 [-0.36, +0.16] | -0.10 [-0.35, +0.15] | -0.11 [-0.29, +0.07] |
| T5Gemma 2 1B | +0.05 [-0.21, +0.31] | +0.11 [-0.07, +0.28] | -0.03 [-0.31, +0.21] | +0.25 [+0.06, +0.44] ✱ | +0.32 [+0.12, +0.52] ✱ | +0.22 [+0.05, +0.40] ✱ |
| Nandi-Mini-150M | -0.16 [-0.43, +0.10] | -0.13 [-0.29, +0.02] | -0.11 [-0.39, +0.18] | -0.20 [-0.38, -0.02] ✱ | -0.24 [-0.43, -0.07] ✱ | -0.15 [-0.29, -0.01] ✱ |

## Against the poets: model poem − the same annotator's study-1 rating of the prompt's gold (bootstrap over prompts, 95%)

| model | readability | comprehension | lexical | bhavam | poetic |
|---|---|---|---|---|---|
| MDLM 523M | -0.72 [-1.02, -0.41] ✱ | -1.34 [-1.75, -0.90] ✱ | -0.86 [-1.17, -0.55] ✱ | -2.96 [-3.17, -2.75] ✱ | -2.39 [-2.71, -2.04] ✱ |
| T5Gemma 2 1B | -0.74 [-1.00, -0.44] ✱ | -1.23 [-1.56, -0.91] ✱ | -0.96 [-1.28, -0.66] ✱ | -2.68 [-2.92, -2.44] ✱ | -2.11 [-2.34, -1.87] ✱ |
| Nandi-Mini-150M | -0.99 [-1.22, -0.75] ✱ | -1.46 [-1.81, -1.10] ✱ | -1.03 [-1.32, -0.74] ✱ | -3.06 [-3.26, -2.86] ✱ | -2.27 [-2.51, -2.01] ✱ |
| all three | -0.78 [-0.98, -0.57] ✱ | -1.37 [-1.68, -1.06] ✱ | -0.98 [-1.21, -0.75] ✱ | -2.90 [-3.06, -2.74] ✱ | -2.24 [-2.46, -2.02] ✱ |

1–5 scales: readability, comprehension, lexical (words), coherence (Q13, how meaningful), bhavam (closeness), poetic. Yes/no questions as the share of yes; register = the share judged grānthika, ai_generated = the share judged AI-generated (not blind: the annotators know every study-2 poem is a model's). ✱: the interval excludes 0. Study 2 shows the metre (gaṇa table) but not the engine's verdicts; study 1 showed both.
