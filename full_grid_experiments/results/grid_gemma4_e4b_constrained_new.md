# Token choices under the constraint

Runs: `grid_gemma4_e4b_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 156 | -2.485 | 46 | 38 | 0.603 | 1.881 | 23 | 8 | 8 | 26.4 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 612 | -2.592 | 40 | 34 | 0.651 |
| masking_backtrack | prasa | 210 | -4.634 | 30 | 67 | 0.333 |
| masking_backtrack | yati | 1347 | -3.221 | 39 | 47 | 0.497 |
| masking_backtrack | other | 8150 | -2.300 | 48 | 36 | 0.624 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.30 / 38 |
| champakamala | 100 / -2.69 / 12 |
| kandamu | 100 / -2.29 / 33 |
| mattakokilamu | 100 / -2.45 / 0 |
| mattebhavikriditamu | 100 / -2.59 / 7 |
| sardulavikriditamu | 100 / -2.15 / 11 |
| seesamu | 100 / -2.36 / 38 |
| tetagiti | 100 / -2.34 / 37 |
| utpalamala | 100 / -2.88 / 14 |
| utsahamu | 100 / -2.40 / 17 |
