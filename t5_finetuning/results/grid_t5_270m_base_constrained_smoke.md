# Token choices under the constraint

Runs: `grid_t5_270m_base_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 135 | -2.435 | 59 | 32 | 0.614 | 2.885 | 14 | 18 | 50 | 25.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 22 | -2.318 | 55 | 14 | 0.620 |
| masking_backtrack | prasa | 17 | -3.429 | 35 | 65 | 0.338 |
| masking_backtrack | yati | 11 | -2.797 | 36 | 64 | 0.400 |
| masking_backtrack | other | 220 | -2.352 | 63 | 30 | 0.645 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -1.89 / 14 |
| utpalamala | 100 / -2.88 / 14 |
