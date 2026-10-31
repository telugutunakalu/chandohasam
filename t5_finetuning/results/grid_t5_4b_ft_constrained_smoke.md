# Token choices under the constraint

Runs: `grid_t5_4b_ft_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 60 | -1.416 | 65 | 10 | 0.903 | 2.188 | 67 | 6 | 0 | 2.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 6 | -1.341 | 83 | 0 | 0.940 |
| masking_backtrack | prasa | 6 | -2.173 | 50 | 33 | 0.668 |
| masking_backtrack | yati | 12 | -2.517 | 33 | 42 | 0.601 |
| masking_backtrack | other | 95 | -1.234 | 68 | 5 | 0.954 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.48 / 56 |
| mattakokilamu | 100 / -0.90 / 70 |
