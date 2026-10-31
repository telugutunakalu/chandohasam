# Token choices under the constraint

Runs: `grid_t5_270m_ft_constrained_new`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 66 | 100 | 100 | 87 | -1.325 | 78 | 5 | 0.939 | 2.072 | 48 | 4 | 0 | 4.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 340 | -1.423 | 79 | 2 | 0.963 |
| masking_backtrack | prasa | 204 | -0.906 | 86 | 6 | 0.903 |
| masking_backtrack | yati | 471 | -1.802 | 70 | 24 | 0.766 |
| masking_backtrack | other | 4700 | -1.288 | 78 | 4 | 0.957 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.27 / 55 |
| champakamala | 100 / -1.23 / 52 |
| kandamu | 100 / -1.24 / 40 |
| mattakokilamu | 100 / -1.35 / 57 |
| mattebhavikriditamu | 100 / -1.30 / 39 |
| sardulavikriditamu | 100 / -1.21 / 37 |
| seesamu | 100 / -3.29 / 40 |
| tetagiti | 100 / -1.33 / 61 |
| utpalamala | 100 / -1.16 / 47 |
| utsahamu | 100 / -1.71 / 43 |
