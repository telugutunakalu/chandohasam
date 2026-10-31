# Token choices under the constraint

Runs: `grid_t5_4b_ft_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 87 | -1.329 | 68 | 6 | 0.933 | 2.078 | 47 | 6 | 0 | 4.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 351 | -1.355 | 64 | 7 | 0.937 |
| masking_backtrack | prasa | 189 | -0.851 | 78 | 8 | 0.887 |
| masking_backtrack | yati | 502 | -1.832 | 58 | 23 | 0.726 |
| masking_backtrack | other | 4700 | -1.292 | 69 | 3 | 0.957 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.32 / 60 |
| champakamala | 100 / -1.25 / 45 |
| kandamu | 100 / -1.27 / 48 |
| mattakokilamu | 100 / -1.18 / 40 |
| mattebhavikriditamu | 100 / -1.28 / 42 |
| sardulavikriditamu | 100 / -1.23 / 39 |
| seesamu | 100 / -1.91 / 41 |
| tetagiti | 100 / -1.52 / 50 |
| utpalamala | 100 / -1.30 / 47 |
| utsahamu | 100 / -1.36 / 50 |
