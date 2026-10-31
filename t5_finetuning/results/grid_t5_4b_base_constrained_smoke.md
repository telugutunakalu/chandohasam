# Token choices under the constraint

Runs: `grid_t5_4b_base_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 96 | -3.160 | 39 | 46 | 0.526 | 2.960 | 17 | 12 | 50 | 18.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 10 | -3.010 | 30 | 60 | 0.371 |
| masking_backtrack | prasa | 6 | -2.254 | 67 | 33 | 0.403 |
| masking_backtrack | yati | 23 | -3.626 | 26 | 35 | 0.575 |
| masking_backtrack | other | 154 | -3.135 | 41 | 47 | 0.533 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -3.06 / 25 |
| mattakokilamu | 100 / -3.21 / 12 |
