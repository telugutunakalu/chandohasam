# Token choices under the constraint

Runs: `grid_t5_1b_ft_constrained_smoke`

logp: the model's log-probability of the chosen token (whole vocabulary, T = 1); overridden: the model's first choice was not allowed; valid mass: the model's probability on allowed tokens (baseline: known only while its text is still in meter); lexical: share of words found in the corpora; 1-akshara words: words of a single akshara (the lexical rate counts filler such as క క క as words); repeated line: a poem that writes some line twice; complete (baseline): a whole poem in meter.

## By strategy

| strategy | poems | complete % | in meter % | tokens | mean logp | rank 1 % | overridden % | valid mass | entropy | lexical % | 1-akshara words % | repeated line % | backtracks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| masking_backtrack | 2 | 100 | 100 | 111 | -1.161 | 74 | 5 | 0.929 | 1.496 | 50 | 3 | 0 | 15.0 |

## By position in the line

| strategy | position | tokens | mean logp | rank 1 % | overridden % | valid mass |
|---|---|---|---|---|---|---|
| masking_backtrack | line_start | 7 | -1.463 | 43 | 0 | 0.990 |
| masking_backtrack | prasa | 8 | -0.433 | 88 | 0 | 0.992 |
| masking_backtrack | yati | 39 | -1.779 | 72 | 23 | 0.680 |
| masking_backtrack | other | 168 | -1.039 | 76 | 1 | 0.981 |

## By meter

| meter | masking_backtrack in meter % / logp / lexical % |
|---|---|
| kandamu | 100 / -1.25 / 43 |
| utpalamala | 100 / -1.04 / 55 |
