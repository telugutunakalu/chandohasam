# EXP-11 — Tokenizer syllable-coverage audit

| | |
|---|---|
| **Category** | C. Behavioural capability |
| **Origin** | ours (E13) ★ |
| **Depends on** | EXP-01 |
| **Status** | done |
| **Cost** | seconds, no model |

## Question
What fraction of the language's syllables can this tokenizer emit as a single token?

## Why it matters
Explains EXP-09 mechanically and costs nothing to run. Meter is a property of syllables; if most syllables are not tokens, there is no function from what the model emits to what the rules govern.

## Methodology
1. Enumerate the vocabulary; segment each token into aksharas.
2. Keep tokens that are exactly one akshara **and stable under concatenation on both sides** — a token that merges with a neighbour on render breaks positional alignment even though it looks like one unit.
3. Measure coverage of corpus akshara *types* and *occurrences* separately.

## Inputs
Any tokenizer; a corpus akshara frequency table.

## Metrics
Type coverage; occurrence coverage; count of grid-stable single-akshara tokens.

## Expected result / baseline
Occurrence coverage will look reassuring and type coverage will not — frequent syllables get tokens, the long tail does not. **Type coverage is the number that predicts EXP-09.**

## Observed
| | Gemma 262K | padyam akshara-aligned |
|---|---|---|
| syllable **types** | **15.6%** | **96.0%** |
| syllable occurrences | 87.5% | 99.9% |
| grid-stable single-akshara tokens | 562 | 10,334 |

Common syllables — ధా, చం, బం, నొ, దె — simply do not exist as Gemma tokens.

## Replication notes
Run this before EXP-09 on any new model; it predicts the result and takes seconds. The two-sided stability check is essential — one-sided passes tokens that corrupt alignment on render.

## Artifacts
`padyam/prosody/constraints.py::AksharaTable`, `padyam/data/tokenizer.py`
