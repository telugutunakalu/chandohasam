# Token choices under the constraint

Runs: `grid_mdlm523m_base_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 188 | -2.514 | 51 | 30 | 0.633 | 2.339 | 63 | 33 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 16 | -4.078 | 19 | 31 | 0.565 |
| masking_backtrack | prasa | 18 | -2.804 | 50 | 44 | 0.450 |
| masking_backtrack | yati | 28 | -2.554 | 50 | 39 | 0.509 |
| masking_backtrack | other | 315 | -2.414 | 53 | 29 | 0.658 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -2.79 / 83 |
| utpalamala | 100 / -2.34 / 41 |
