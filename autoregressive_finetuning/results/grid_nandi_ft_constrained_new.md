# Token choices under the constraint

Runs: `grid_nandi_ft_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 83 | -1.189 | 75 | 7 | 0.925 | 1.654 | 44 | 7 | 0 | 5.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 222 | -1.023 | 79 | 1 | 0.979 |
| masking_backtrack | prasa | 199 | -0.760 | 85 | 3 | 0.953 |
| masking_backtrack | yati | 487 | -2.237 | 58 | 32 | 0.662 |
| masking_backtrack | other | 4548 | -1.104 | 76 | 4 | 0.949 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.00 / 57 |
| champakamala | 100 / -0.92 / 41 |
| kandamu | 100 / -0.98 / 48 |
| mattakokilamu | 100 / -1.20 / 26 |
| mattebhavikriditamu | 100 / -1.16 / 40 |
| sardulavikriditamu | 100 / -1.39 / 40 |
| seesamu | 100 / -3.39 / 48 |
| tetagiti | 100 / -1.13 / 52 |
| utpalamala | 100 / -1.10 / 36 |
| utsahamu | 100 / -1.03 / 17 |
