# Token choices under the constraint

Runs: `e6_t5g_270m_val_c`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 100 | 100 | 94 | -1.393 | 76 | 8 | 0.909 | 2.001 | 43 | 7 | 0 | 5.5 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 582 | -1.389 | 76 | 3 | 0.950 |
| masking_backtrack | prasa | 409 | -1.024 | 86 | 11 | 0.863 |
| masking_backtrack | yati | 1180 | -2.275 | 57 | 32 | 0.625 |
| masking_backtrack | other | 8558 | -1.289 | 78 | 5 | 0.947 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.24 / 58 |
| bhujangaprayatamu | 100 / -1.82 / 17 |
| champakamala | 100 / -1.19 / 47 |
| kandamu | 100 / -1.32 / 37 |
| malini | 100 / -1.28 / 0 |
| mattakokilamu | 100 / -1.51 / 48 |
| mattebhavikriditamu | 100 / -1.53 / 36 |
| sardulavikriditamu | 100 / -1.49 / 36 |
| seesamu | 100 / -2.42 / 44 |
| tetagiti | 100 / -1.32 / 46 |
| utpalamala | 100 / -1.31 / 46 |
