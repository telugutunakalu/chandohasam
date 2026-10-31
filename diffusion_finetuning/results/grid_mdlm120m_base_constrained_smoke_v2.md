# Token choices under the constraint

Runs: `grid_mdlm120m_base_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 120 | -2.425 | 47 | 33 | 0.573 | 2.739 | 51 | 22 | 50 | 16.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 14 | -3.921 | 36 | 50 | 0.483 |
| masking_backtrack | prasa | 7 | -3.915 | 29 | 71 | 0.279 |
| masking_backtrack | yati | 20 | -3.533 | 30 | 65 | 0.372 |
| masking_backtrack | other | 198 | -2.155 | 51 | 28 | 0.610 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -2.04 / 67 |
| mattakokilamu | 100 / -2.50 / 47 |
