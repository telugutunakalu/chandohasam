# Token choices under the constraint

Runs: `grid_gemma4_26b_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 128 | -2.225 | 55 | 29 | 0.659 | 1.826 | 37 | 13 | 50 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 10 | -1.912 | 30 | 30 | 0.706 |
| masking_backtrack | prasa | 7 | -2.123 | 57 | 43 | 0.582 |
| masking_backtrack | yati | 54 | -2.910 | 39 | 35 | 0.581 |
| masking_backtrack | other | 186 | -2.046 | 61 | 26 | 0.683 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.86 / 36 |
| mattakokilamu | 100 / -1.89 / 37 |
