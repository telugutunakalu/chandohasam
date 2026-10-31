# Token choices under the constraint

Runs: `grid_gemma4_26b_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 136 | -2.301 | 56 | 29 | 0.685 | 1.699 | 41 | 3 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 8 | -1.552 | 50 | 0 | 0.994 |
| masking_backtrack | prasa | 8 | -1.247 | 75 | 25 | 0.747 |
| masking_backtrack | yati | 51 | -2.201 | 65 | 29 | 0.693 |
| masking_backtrack | other | 205 | -2.397 | 53 | 31 | 0.668 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.10 / 60 |
| mattakokilamu | 100 / -2.97 / 32 |
