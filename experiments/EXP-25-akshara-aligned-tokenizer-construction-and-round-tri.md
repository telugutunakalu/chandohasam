# EXP-25 — Akshara-aligned tokenizer construction and round-trip validation

| | |
|---|---|
| **Category** | H. Training |
| **Origin** | ours (E13) ★ |
| **Depends on** | EXP-01,11 |
| **Status** | done |
| **Cost** | seconds to train, minutes to validate |

## Question
Can a vocabulary be built in which every token boundary falls on a syllable boundary?

## Why it matters
The perception layer. It makes token-sequence → syllable-sequence → weight-string total and deterministic, which is the precondition EXP-09 showed is missing.

## Methodology
1. Pre-tokenise into syllables **first**, so subword merges can only combine whole syllables.
2. Choose whether whitespace is attached to tokens or split off — this is the decision that matters (see below).
3. **Validate by round trip**: render a gold padyam through the representation and re-score it. If the metre does not survive, the training targets are wrong.
4. Measure type and occurrence coverage against the corpus.

## Inputs
A normalised monolingual corpus; the EXP-01 segmenter.

## Metrics
Round-trip metrical survival rate; syllable type and occurrence coverage; vocabulary size; fertility (tokens per syllable).

## Expected result / baseline
Round-trip survival should approach 100%. Anything materially lower means a fraction of every training target is silently corrupt.

## Observed
Three attempts, and the failures are the lesson — two definitions of 'syllable' are in play: the **written** unit is word-local, the **scansion** unit binds across spaces (`ముల్ కం` scans as two units, not three).

| attempt | approach | round-trip survival |
|---|---|---|
| 1 | isolate syllables, drop whitespace | **49.7%** ✗ half of all targets metrically wrong |
| 2 | attach whitespace to tokens | alignment broken — merges crossed syllables |
| 3 | scansion units carrying unabsorbed whitespace | **99.3%** ✓ |

Final: 13,710 tokens, **96.0%** type coverage (vs 15.6%), 99.9% occurrence coverage, 0 reconstruction failures. Attempt 1 trained a model that produced run-together output with no word boundaries at all — 0/30 valid.

## Replication notes
**Do the round-trip check before training on anything.** Coverage statistics look fine under attempt 1; only the round trip reveals that half the targets are corrupt.

## Artifacts
`padyam/data/tokenizer.py`, `padyam/prosody/akshara.py::split_aksharas_spaced`
