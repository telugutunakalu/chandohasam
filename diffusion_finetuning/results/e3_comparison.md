# E3: token choices under the constraint, by model and strategy

Computed by `metrical_decoder.analysis.collect` from each run's results and traces. Real words as in §16: words of ≥ 2 aksharas found in `dataset/*.json`, as a share of all words. The fine-tuned model was trained on those corpora, so for it this partly measures recall of training vocabulary (see E4).

| model | strategy | poems | in meter % | chosen-token logp | first choice overridden % | mass on allowed | real words % | 1-akshara words % | poems repeating a line % | tokens |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemma-4 E4B | baseline | 555 | 0.0 | -0.84 | 22.0 | 0.78 | 42.9 | 0.4 | 0.7 | 65 |
| Gemma-4 E4B | masking_only | 555 | 100.0 | -2.18 | 31.4 | 0.67 | 14.1 | 9.2 | 20.0 | 107 |
| Gemma-4 E4B | masking_backtrack | 555 | 100.0 | -2.29 | 35.4 | 0.63 | 15.4 | 9.3 | 21.4 | 161 |
| Gemma-4 E4B | hybrid | 555 | 100.0 | -2.34 | 31.9 | 0.66 | 14.8 | 7.9 | 17.3 | 101 |
| Gemma-4 26B-A4B | baseline | 555 | 0.0 | -0.48 | 24.0 | 0.75 | 45.0 | 0.2 | 10.8 | 70 |
| Gemma-4 26B-A4B | masking_only | 555 | 100.0 | -1.68 | 21.9 | 0.77 | 18.6 | 16.1 | 41.6 | 107 |
| Gemma-4 26B-A4B | masking_backtrack | 555 | 100.0 | -1.94 | 27.8 | 0.71 | 23.0 | 12.0 | 30.3 | 156 |
| Gemma-4 26B-A4B | hybrid | 555 | 100.0 | -1.87 | 22.8 | 0.76 | 18.7 | 14.1 | 28.5 | 101 |
| DiffusionGemma 26B-A4B | baseline | 555 | 0.0 | -0.47 | 18.8 | 0.77 | 38.5 | 4.4 | 2.5 | 57 |
| DiffusionGemma 26B-A4B | masking_only | 555 | 100.0 | -3.84 | 47.2 | 0.49 | 9.2 | 28.7 | 3.8 | 102 |
| DiffusionGemma 26B-A4B | masking_backtrack | 555 | 100.0 | -3.13 | 35.9 | 0.61 | 9.9 | 25.0 | 2.2 | 194 |
| DiffusionGemma 26B-A4B | hybrid | 555 | 100.0 | -3.49 | 47.2 | 0.50 | 10.8 | 26.5 | 2.9 | 98 |
| ours: e3_e5_tagged_10ep | baseline | 555 | 2.5 | -0.96 | 7.6 | 0.89 | 70.5 | 7.9 | 7.7 | 136 |
| ours: e3_e5_tagged_10ep | masking_only | 555 | 99.6 | -2.48 | 26.0 | 0.67 | 35.5 | 24.6 | 17.5 | 130 |
| ours: e3_e5_tagged_10ep | masking_backtrack | 555 | 99.3 | -2.69 | 27.2 | 0.66 | 37.8 | 23.0 | 9.9 | 165 |
| ours: e3_e5_tagged_10ep | hybrid | 555 | 100.0 | -2.49 | 25.6 | 0.67 | 37.0 | 20.4 | 11.0 | 122 |
| ours: e3_e2_pretrained_10ep | baseline | 555 | 0.0 | -0.92 | 18.3 | 0.77 | 82.3 | 2.0 | 6.7 | 87 |
| ours: e3_e2_pretrained_10ep | masking_only | 555 | 100.0 | -2.50 | 30.3 | 0.63 | 26.5 | 39.7 | 13.0 | 146 |
| ours: e3_e2_pretrained_10ep | masking_backtrack | 555 | 100.0 | -2.79 | 31.8 | 0.61 | 29.5 | 36.5 | 8.6 | 187 |
| ours: e3_e2_pretrained_10ep | hybrid | 555 | 99.6 | -2.53 | 30.1 | 0.63 | 29.8 | 30.9 | 7.4 | 141 |
| ours: e3_e2_pretrained | baseline | 111 | 0.0 | -2.01 | 22.2 | 0.77 | 70.4 | 3.7 | 0.0 | 35 |
| ours: e3_e2_pretrained | masking_only | 111 | 100.0 | -2.43 | 31.0 | 0.62 | 24.3 | 41.6 | 9.0 | 149 |
| ours: e3_e2_pretrained | masking_backtrack | 111 | 100.0 | -2.72 | 31.4 | 0.61 | 26.3 | 37.7 | 3.6 | 194 |
| ours: e3_e2_pretrained | hybrid | 111 | 99.1 | -2.42 | 31.1 | 0.61 | 26.6 | 33.0 | 6.3 | 147 |
| ours: e3_pilot_seed42 | baseline | 111 | 0.0 | -0.77 | 10.1 | 0.74 | 25.9 | 10.0 | 0.0 | 472 |
| ours: e3_pilot_seed42 | masking_only | 111 | 100.0 | -1.85 | 27.2 | 0.66 | 22.6 | 25.1 | 8.1 | 158 |
| ours: e3_pilot_seed42 | masking_backtrack | 111 | 100.0 | -2.20 | 30.1 | 0.63 | 24.3 | 25.2 | 5.4 | 202 |
| ours: e3_pilot_seed42 | hybrid | 111 | 100.0 | -2.07 | 28.2 | 0.65 | 27.0 | 16.6 | 12.6 | 138 |
