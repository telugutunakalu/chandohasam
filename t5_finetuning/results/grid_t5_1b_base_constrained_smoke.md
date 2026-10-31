# Token choices under the constraint

Runs: `grid_t5_1b_base_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 128 | -3.398 | 36 | 49 | 0.465 | 3.638 | 20 | 10 | 0 | 15.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 14 | -3.143 | 29 | 36 | 0.509 |
| masking_backtrack | prasa | 13 | -4.679 | 23 | 77 | 0.273 |
| masking_backtrack | yati | 50 | -5.880 | 6 | 92 | 0.062 |
| masking_backtrack | other | 178 | -2.628 | 47 | 35 | 0.588 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -2.38 / 25 |
| utpalamala | 100 / -3.65 / 17 |
