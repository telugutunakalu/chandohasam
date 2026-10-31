# Token choices under the constraint

Runs: `e6_t5g_1b_val_c_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 100 | 100 | 92 | -1.240 | 69 | 6 | 0.929 | 1.885 | 52 | 5 | 0 | 4.3 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 555 | -1.243 | 69 | 2 | 0.968 |
| masking_backtrack | prasa | 384 | -0.838 | 80 | 5 | 0.927 |
| masking_backtrack | yati | 938 | -1.899 | 60 | 24 | 0.692 |
| masking_backtrack | other | 8577 | -1.186 | 70 | 4 | 0.953 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.13 / 70 |
| bhujangaprayatamu | 100 / -2.44 / 0 |
| champakamala | 100 / -1.20 / 54 |
| kandamu | 100 / -1.32 / 50 |
| malini | 100 / -1.61 / 30 |
| mattakokilamu | 100 / -1.20 / 50 |
| mattebhavikriditamu | 100 / -1.09 / 47 |
| sardulavikriditamu | 100 / -1.27 / 45 |
| seesamu | 100 / -2.28 / 43 |
| tetagiti | 100 / -1.40 / 56 |
| utpalamala | 100 / -1.14 / 52 |
