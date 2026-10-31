# Token choices under the constraint

Runs: `e6_t5g_1b_val_c`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 100 | 100 | 94 | -1.229 | 70 | 6 | 0.921 | 1.864 | 44 | 6 | 0 | 5.8 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 534 | -1.226 | 68 | 1 | 0.979 |
| masking_backtrack | prasa | 376 | -0.802 | 80 | 4 | 0.939 |
| masking_backtrack | yati | 1242 | -1.986 | 56 | 28 | 0.662 |
| masking_backtrack | other | 8558 | -1.138 | 72 | 4 | 0.954 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.20 / 57 |
| bhujangaprayatamu | 100 / -2.69 / 9 |
| champakamala | 100 / -1.16 / 50 |
| kandamu | 100 / -1.00 / 40 |
| malini | 100 / -1.13 / 0 |
| mattakokilamu | 100 / -1.18 / 46 |
| mattebhavikriditamu | 100 / -1.17 / 37 |
| sardulavikriditamu | 100 / -1.41 / 39 |
| seesamu | 100 / -2.58 / 43 |
| tetagiti | 100 / -1.19 / 44 |
| utpalamala | 100 / -1.09 / 42 |
