# Token choices under the constraint

Runs: `grid_t5_1b_base_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 145 | -3.164 | 34 | 43 | 0.533 | 3.617 | 22 | 9 | 18 | 23.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 411 | -3.775 | 16 | 41 | 0.519 |
| masking_backtrack | prasa | 206 | -3.806 | 30 | 67 | 0.252 |
| masking_backtrack | yati | 1195 | -3.776 | 26 | 63 | 0.349 |
| masking_backtrack | other | 7770 | -3.021 | 36 | 40 | 0.569 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -3.29 / 29 |
| champakamala | 100 / -2.92 / 8 |
| kandamu | 100 / -3.32 / 27 |
| mattakokilamu | 100 / -3.66 / 21 |
| mattebhavikriditamu | 100 / -3.05 / 16 |
| sardulavikriditamu | 100 / -3.17 / 15 |
| seesamu | 100 / -2.40 / 34 |
| tetagiti | 100 / -3.35 / 25 |
| utpalamala | 100 / -3.25 / 20 |
| utsahamu | 100 / -3.35 / 0 |
