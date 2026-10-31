# Token choices under the constraint

Runs: `rl_120m_r1_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 0 | 0 | 95 | -1.024 | 75 | 8 | 0.915 | 1.916 | 67 | 7 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 146 | -2.107 | 56 | 20 | 0.766 | 2.196 | 59 | 11 | 1 | 18.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 155 | -1.237 | 46 | 0 | 0.989 |
| baseline | prasa | 103 | -0.678 | 91 | 1 | 0.969 |
| baseline | yati | 15 | -1.036 | 87 | 0 | 0.905 |
| baseline | other | 1097 | -0.888 | 78 | 1 | 0.969 |
| masking_backtrack | line_start | 516 | -1.797 | 56 | 4 | 0.942 |
| masking_backtrack | prasa | 505 | -1.081 | 81 | 8 | 0.849 |
| masking_backtrack | yati | 1942 | -3.017 | 39 | 44 | 0.517 |
| masking_backtrack | other | 13661 | -2.027 | 57 | 18 | 0.792 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % |
|---|---|---|
| ataveladi | 0 / -0.90 / 87 | 100 / -1.38 / 88 |
| bhujangaprayatamu | 0 / -0.86 / 54 | 100 / -3.26 / 14 |
| champakamala | 0 / -1.02 / 61 | 100 / -1.62 / 56 |
| kandamu | 0 / -0.97 / 76 | 100 / -1.69 / 72 |
| malini | 0 / -0.99 / 65 | 100 / -2.86 / 30 |
| mattakokilamu | 0 / -0.98 / 62 | 100 / -2.52 / 45 |
| mattebhavikriditamu | 0 / -1.19 / 60 | 100 / -2.65 / 42 |
| sardulavikriditamu | 0 / -1.12 / 64 | 100 / -2.72 / 44 |
| seesamu | 0 / -1.11 / 62 | 100 / -1.19 / 91 |
| tetagiti | 0 / -0.85 / 75 | 100 / -1.72 / 67 |
| utpalamala | 0 / -1.01 / 60 | 100 / -1.45 / 61 |
