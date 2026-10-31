# Token choices under the constraint

Runs: `e6_nandi_base_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 241 | -0.846 | 83 | 37 | 0.627 | 1.612 | 42 | 9 | 8 | 0.0 |
| masking_only | 114 | 95 | 96 | 111 | -2.687 | 50 | 36 | 0.588 | 3.481 | 25 | 26 | 37 | 0.0 |
| masking_backtrack | 114 | 99 | 99 | 153 | -3.509 | 34 | 40 | 0.540 | 4.347 | 26 | 24 | 23 | 20.0 |
| hybrid | 114 | 97 | 97 | 107 | -2.351 | 55 | 31 | 0.625 | 3.173 | 22 | 21 | 28 | 0.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 112 | -3.140 | 6 | 37 | 0.711 |
| baseline | prasa | 67 | -3.307 | 30 | 9 | 0.770 |
| baseline | other | 170 | -3.151 | 33 | 25 | 0.726 |
| masking_only | line_start | 640 | -3.394 | 26 | 27 | 0.571 |
| masking_only | prasa | 407 | -3.260 | 48 | 48 | 0.374 |
| masking_only | yati | 1238 | -3.655 | 37 | 57 | 0.387 |
| masking_only | other | 10372 | -2.505 | 53 | 33 | 0.622 |
| masking_backtrack | line_start | 714 | -3.836 | 14 | 31 | 0.529 |
| masking_backtrack | prasa | 406 | -3.818 | 34 | 60 | 0.278 |
| masking_backtrack | yati | 1710 | -4.267 | 23 | 65 | 0.308 |
| masking_backtrack | other | 14579 | -3.395 | 37 | 37 | 0.575 |
| hybrid | line_start | 660 | -3.081 | 32 | 24 | 0.590 |
| hybrid | prasa | 510 | -2.966 | 54 | 43 | 0.433 |
| hybrid | yati | 1212 | -3.193 | 46 | 49 | 0.444 |
| hybrid | other | 9827 | -2.166 | 57 | 29 | 0.660 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_only in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % | hybrid in meter % / logp / lexical % |
|---|---|---|---|---|
| ataveladi | 0 / -0.87 / 43 | 100 / -3.25 / 43 | 100 / -3.67 / 45 | 100 / -2.40 / 36 |
| bhujangaprayatamu | 0 / -1.12 / 12 | 100 / -3.12 / 6 | 100 / -4.07 / 7 | 100 / -3.01 / 40 |
| champakamala | 0 / -0.79 / 40 | 100 / -2.31 / 18 | 100 / -3.29 / 21 | 100 / -2.60 / 12 |
| kandamu | 0 / -0.60 / 36 | 100 / -2.87 / 44 | 100 / -3.35 / 40 | 100 / -2.70 / 34 |
| malini | 0 / -1.39 / 32 | 100 / -2.89 / 6 | 100 / -4.09 / 18 | 100 / -2.00 / 12 |
| mattakokilamu | 0 / -0.70 / 43 | 100 / -2.96 / 22 | 100 / -4.00 / 13 | 89 / -2.05 / 18 |
| mattebhavikriditamu | 0 / -0.86 / 47 | 93 / -2.47 / 7 | 100 / -3.25 / 9 | 100 / -2.42 / 17 |
| sardulavikriditamu | 0 / -0.93 / 50 | 93 / -2.80 / 17 | 100 / -3.57 / 13 | 100 / -2.01 / 15 |
| seesamu | 0 / -0.62 / 7 | 100 / -2.55 / 23 | 100 / -4.11 / 26 | 100 / -2.98 / 14 |
| tetagiti | 0 / -0.80 / 36 | 100 / -3.30 / 38 | 100 / -3.75 / 30 | 100 / -2.37 / 39 |
| utpalamala | 0 / -1.14 / 46 | 80 / -2.48 / 23 | 93 / -3.39 / 31 | 87 / -2.38 / 12 |
