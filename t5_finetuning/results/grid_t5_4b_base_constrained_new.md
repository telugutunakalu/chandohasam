# Token choices under the constraint

Runs: `grid_t5_4b_base_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 146 | -2.665 | 45 | 36 | 0.589 | 2.973 | 24 | 13 | 30 | 20.7 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 570 | -3.373 | 32 | 37 | 0.466 |
| masking_backtrack | prasa | 279 | -3.289 | 35 | 59 | 0.329 |
| masking_backtrack | yati | 1228 | -3.342 | 36 | 51 | 0.442 |
| masking_backtrack | other | 7564 | -2.478 | 48 | 33 | 0.632 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.10 / 36 |
| champakamala | 100 / -2.59 / 8 |
| kandamu | 100 / -3.14 / 30 |
| mattakokilamu | 100 / -1.95 / 6 |
| mattebhavikriditamu | 100 / -2.54 / 10 |
| sardulavikriditamu | 100 / -2.70 / 12 |
| seesamu | 100 / -1.69 / 22 |
| tetagiti | 100 / -2.87 / 30 |
| utpalamala | 100 / -2.15 / 24 |
| utsahamu | 100 / -2.18 / 24 |
