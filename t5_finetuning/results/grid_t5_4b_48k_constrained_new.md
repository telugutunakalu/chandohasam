# Token choices under the constraint

Runs: `grid_t5_4b_48k_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 102 | -2.072 | 51 | 16 | 0.808 | 2.920 | 43 | 7 | 0 | 7.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 378 | -2.018 | 47 | 3 | 0.924 |
| masking_backtrack | prasa | 250 | -1.605 | 73 | 20 | 0.726 |
| masking_backtrack | yati | 606 | -2.800 | 43 | 37 | 0.570 |
| masking_backtrack | other | 5530 | -2.017 | 52 | 15 | 0.830 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -2.00 / 57 |
| champakamala | 100 / -1.85 / 42 |
| kandamu | 100 / -1.85 / 37 |
| mattakokilamu | 100 / -2.88 / 35 |
| mattebhavikriditamu | 100 / -2.14 / 34 |
| sardulavikriditamu | 100 / -2.47 / 31 |
| seesamu | 100 / -2.40 / 39 |
| tetagiti | 100 / -1.83 / 62 |
| utpalamala | 100 / -1.95 / 37 |
| utsahamu | 100 / -2.66 / 19 |
