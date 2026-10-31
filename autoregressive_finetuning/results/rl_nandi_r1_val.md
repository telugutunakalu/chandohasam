# Token choices under the constraint

Runs: `rl_nandi_r1_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 6 | 9 | 77 | -0.601 | 86 | 5 | 0.949 | 1.110 | 50 | 7 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 98 | -0.933 | 80 | 7 | 0.919 | 1.102 | 46 | 8 | 0 | 10.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 237 | -0.541 | 77 | 1 | 0.989 |
| baseline | prasa | 143 | -0.605 | 85 | 1 | 0.976 |
| baseline | yati | 87 | -0.779 | 84 | 3 | 0.933 |
| baseline | other | 2098 | -0.601 | 87 | 1 | 0.984 |
| masking_backtrack | line_start | 432 | -0.681 | 83 | 2 | 0.976 |
| masking_backtrack | prasa | 404 | -0.739 | 84 | 7 | 0.915 |
| masking_backtrack | yati | 1220 | -1.488 | 73 | 17 | 0.775 |
| masking_backtrack | other | 9150 | -0.880 | 80 | 6 | 0.936 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % |
|---|---|---|
| ataveladi | 20 / -0.60 / 59 | 100 / -0.95 / 59 |
| bhujangaprayatamu | 0 / -0.79 / 33 | 100 / -1.82 / 0 |
| champakamala | 7 / -0.55 / 54 | 100 / -0.77 / 43 |
| kandamu | 27 / -0.58 / 53 | 100 / -0.78 / 50 |
| malini | 0 / -0.75 / 11 | 100 / -0.99 / 27 |
| mattakokilamu | 0 / -0.57 / 56 | 100 / -1.01 / 50 |
| mattebhavikriditamu | 0 / -0.62 / 46 | 100 / -0.78 / 43 |
| sardulavikriditamu | 0 / -0.64 / 43 | 100 / -0.99 / 37 |
| seesamu | 0 / -0.65 / 42 | 100 / -3.03 / 45 |
| tetagiti | 20 / -0.61 / 54 | 100 / -1.05 / 52 |
| utpalamala | 0 / -0.58 / 46 | 100 / -0.82 / 48 |
