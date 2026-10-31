# Token choices under the constraint

Runs: `grid_mdlm523m_base_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 66 | -0.797 | 80 | 10 | 0.869 | 1.406 | 61 | 12 | 50 | 1.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 6 | -2.189 | 50 | 0 | 0.800 |
| masking_backtrack | prasa | 8 | -0.689 | 75 | 25 | 0.797 |
| masking_backtrack | yati | 7 | -1.729 | 71 | 29 | 0.608 |
| masking_backtrack | other | 112 | -0.672 | 83 | 8 | 0.895 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.29 / 89 |
| mattakokilamu | 100 / -0.61 / 50 |
