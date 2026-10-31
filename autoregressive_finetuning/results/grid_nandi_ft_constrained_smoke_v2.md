# Token choices under the constraint

Runs: `grid_nandi_ft_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 98 | -1.590 | 68 | 21 | 0.793 | 0.995 | 34 | 3 | 0 | 20.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 64 | -2.755 | 48 | 45 | 0.553 |
| masking_backtrack | prasa | 7 | -0.399 | 86 | 0 | 0.897 |
| masking_backtrack | yati | 9 | -2.009 | 56 | 44 | 0.549 |
| masking_backtrack | other | 115 | -0.981 | 78 | 6 | 0.939 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.48 / 25 |
| mattakokilamu | 100 / -0.87 / 38 |
