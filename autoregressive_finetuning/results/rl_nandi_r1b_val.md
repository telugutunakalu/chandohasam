# Token choices under the constraint

Runs: `rl_nandi_r1b_val`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| baseline | 114 | 8 | 11 | 77 | -0.702 | 84 | 4 | 0.951 | 1.295 | 50 | 7 | 0 | 0.0 |
| masking_backtrack | 114 | 100 | 100 | 91 | -1.039 | 76 | 7 | 0.929 | 1.364 | 47 | 8 | 0 | 7.1 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| baseline | line_start | 274 | -0.657 | 78 | 0 | 0.996 |
| baseline | prasa | 164 | -0.643 | 85 | 2 | 0.974 |
| baseline | yati | 114 | -0.658 | 91 | 6 | 0.933 |
| baseline | other | 2274 | -0.761 | 83 | 1 | 0.981 |
| masking_backtrack | line_start | 400 | -0.817 | 80 | 1 | 0.987 |
| masking_backtrack | prasa | 417 | -0.628 | 88 | 3 | 0.956 |
| masking_backtrack | yati | 982 | -1.664 | 66 | 21 | 0.769 |
| masking_backtrack | other | 8533 | -0.998 | 77 | 5 | 0.943 |

## By meter

| meter | baseline in meter % / logp / lexical % | masking_backtrack in meter % / logp / lexical % |
|---|---|---|
| ataveladi | 13 / -0.72 / 61 | 100 / -1.20 / 52 |
| bhujangaprayatamu | 0 / -0.69 / 11 | 100 / -1.01 / 38 |
| champakamala | 13 / -0.67 / 52 | 100 / -0.82 / 54 |
| kandamu | 20 / -0.68 / 54 | 100 / -0.86 / 43 |
| malini | 0 / -0.56 / 11 | 100 / -1.53 / 7 |
| mattakokilamu | 0 / -0.69 / 53 | 100 / -1.15 / 44 |
| mattebhavikriditamu | 0 / -0.71 / 48 | 100 / -0.98 / 45 |
| sardulavikriditamu | 7 / -0.71 / 46 | 100 / -1.03 / 39 |
| seesamu | 0 / -0.76 / 69 | 100 / -2.58 / 60 |
| tetagiti | 10 / -0.73 / 49 | 100 / -1.28 / 54 |
| utpalamala | 20 / -0.72 / 46 | 100 / -0.83 / 44 |
