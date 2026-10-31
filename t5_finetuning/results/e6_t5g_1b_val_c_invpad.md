# Token choices under the constraint

Runs: `e6_t5g_1b_val_c_invpad`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 114 | 100 | 100 | 87 | -1.140 | 72 | 5 | 0.941 | 1.863 | 45 | 6 | 0 | 2.9 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 530 | -1.207 | 68 | 1 | 0.973 |
| masking_backtrack | prasa | 376 | -0.839 | 81 | 5 | 0.923 |
| masking_backtrack | yati | 801 | -1.655 | 61 | 22 | 0.723 |
| masking_backtrack | other | 8240 | -1.100 | 73 | 3 | 0.961 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| ataveladi | 100 / -1.02 / 60 |
| bhujangaprayatamu | 100 / -2.23 / 17 |
| champakamala | 100 / -1.08 / 51 |
| kandamu | 100 / -0.97 / 44 |
| malini | 100 / -1.13 / 0 |
| mattakokilamu | 100 / -1.22 / 44 |
| mattebhavikriditamu | 100 / -1.09 / 42 |
| sardulavikriditamu | 100 / -1.22 / 41 |
| seesamu | 100 / -2.17 / 45 |
| tetagiti | 100 / -1.28 / 45 |
| utpalamala | 100 / -1.08 / 41 |
