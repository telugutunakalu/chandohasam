# Token choices under the constraint

Runs: `grid_t5_1b_base_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 124 | -2.828 | 41 | 47 | 0.547 | 3.090 | 26 | 0 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 28 | -3.773 | 0 | 86 | 0.211 |
| masking_backtrack | prasa | 11 | -4.619 | 18 | 82 | 0.079 |
| masking_backtrack | yati | 32 | -4.127 | 16 | 78 | 0.375 |
| masking_backtrack | other | 176 | -2.329 | 53 | 33 | 0.661 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -3.37 / 50 |
| mattakokilamu | 100 / -2.54 / 15 |
