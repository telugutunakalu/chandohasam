# Token choices under the constraint

Runs: `grid_t5_1b_ft_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 64 | -1.434 | 67 | 6 | 0.922 | 2.171 | 70 | 9 | 0 | 2.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 8 | -1.909 | 50 | 12 | 0.850 |
| masking_backtrack | prasa | 6 | -0.775 | 100 | 0 | 0.851 |
| masking_backtrack | yati | 13 | -1.654 | 69 | 15 | 0.762 |
| masking_backtrack | other | 101 | -1.407 | 66 | 5 | 0.952 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.98 / 56 |
| mattakokilamu | 100 / -1.16 / 75 |
