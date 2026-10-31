# Token choices under the constraint

Runs: `grid_gemma4_e4b_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 122 | -1.784 | 59 | 33 | 0.661 | 1.354 | 27 | 4 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 9 | -2.891 | 33 | 33 | 0.573 |
| masking_backtrack | prasa | 5 | -4.817 | 40 | 60 | 0.405 |
| masking_backtrack | yati | 34 | -1.217 | 85 | 15 | 0.631 |
| masking_backtrack | other | 196 | -1.755 | 56 | 35 | 0.677 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.34 / 67 |
| mattakokilamu | 100 / -2.01 / 6 |
