# Token choices under the constraint

Runs: `grid_gemma4_e4b_constrained_smoke_v2`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 116 | -1.749 | 59 | 30 | 0.680 | 1.324 | 38 | 10 | 0 | 30.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 7 | -1.824 | 71 | 14 | 0.787 |
| masking_backtrack | prasa | 5 | -6.942 | 40 | 60 | 0.424 |
| masking_backtrack | yati | 33 | -1.293 | 82 | 15 | 0.650 |
| masking_backtrack | other | 188 | -1.688 | 55 | 33 | 0.688 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| madhuragati_ragada | 100 / -1.41 / 64 |
| mattakokilamu | 100 / -1.92 / 22 |
