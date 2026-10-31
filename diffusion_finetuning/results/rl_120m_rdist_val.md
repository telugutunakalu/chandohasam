# Token choices under the constraint

Runs: `rl_120m_rdist_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 118 | -0.962 | 76 | 7 | 0.915 | 1.822 | 70 | 9 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 132 | -1.819 | 59 | 16 | 0.817 | 2.290 | 61 | 13 | 1 | 14.7 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 151 | -1.188 | 48 | 0 | 0.991 |
| baseline | prasa | 122 | -0.726 | 89 | 1 | 0.969 |
| baseline | yati | 13 | -1.109 | 62 | 0 | 0.929 |
| baseline | other | 1147 | -1.065 | 73 | 1 | 0.962 |
| masking_backtrack | line_start | 514 | -1.519 | 62 | 2 | 0.964 |
| masking_backtrack | prasa | 469 | -0.739 | 87 | 4 | 0.913 |
| masking_backtrack | yati | 1498 | -2.793 | 40 | 41 | 0.522 |
| masking_backtrack | other | 12593 | -1.755 | 60 | 14 | 0.842 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % |
|---|---|---|
| ataveladi | 0 / -0.51 / 88 | 100 / -1.27 / 86 |
| bhujangaprayatamu | 0 / -1.21 / 33 | 100 / -3.09 / 0 |
| champakamala | 0 / -1.09 / 67 | 100 / -1.59 / 54 |
| kandamu | 0 / -0.96 / 71 | 100 / -1.89 / 74 |
| malini | 0 / -0.72 / 40 | 100 / -2.80 / 15 |
| mattakokilamu | 0 / -1.15 / 65 | 100 / -2.39 / 54 |
| mattebhavikriditamu | 0 / -1.40 / 56 | 100 / -2.13 / 39 |
| sardulavikriditamu | 0 / -1.27 / 53 | 100 / -1.98 / 50 |
| seesamu | 0 / -1.01 / 87 | 100 / -1.58 / 66 |
| tetagiti | 0 / -0.71 / 88 | 100 / -1.26 / 83 |
| utpalamala | 0 / -1.11 / 61 | 100 / -1.36 / 61 |
