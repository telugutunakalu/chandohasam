# Token choices under the constraint

Runs: `grid_mdlm523m_ft_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 122 | -1.178 | 68 | 9 | 0.885 | 1.759 | 44 | 3 | 0 | 18.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 8 | -2.042 | 38 | 0 | 0.990 |
| masking_backtrack | prasa | 9 | -0.506 | 100 | 0 | 0.963 |
| masking_backtrack | yati | 13 | -2.964 | 31 | 38 | 0.554 |
| masking_backtrack | other | 213 | -1.065 | 70 | 8 | 0.898 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -1.61 / 44 |
| utpalamala | 100 / -0.94 / 45 |
