# EXP-30 — Word-lattice composition

| | |
|---|---|
| **Category** | I. Composition |
| **Origin** | ours (E16) |
| **Depends on** | EXP-04 |
| **Status** | done |
| **Cost** | minutes, CPU |

## Question
Can composition at the level of whole words eliminate sub-word fragments?

## Why it matters
Syllable-level decoding produces single-syllable pieces that are not words — the clearest sign the output is a metrical artefact rather than language.

## Methodology
1. Build a lattice whose edges are whole lexicon words of ≥2 syllables and whose paths are exactly the metrically legal lines.
2. State is `(position, obligation)`, where the obligation encodes that a word's final syllable weight depends on whether the next word opens with a cluster.
3. Check the caesura and line-agreement rules on whichever syllable lands at the rule position, wherever inside a word it falls.
4. Search by beam; score paths with any scorer.

## Inputs
A corpus word lexicon; meter definitions; a scoring function.

## Metrics
Valid rate; single-syllable fragment count; fraction of planner content words used.

## Expected result / baseline
Metre and lexicality become guaranteed by construction. The open question moves to which path is chosen.

## Observed
1,166,174 edges over 60 states. All topics metrically valid, **zero fragments**, 10–13 of ~25 planner words used. Random walks through the lattice already produce metrically perfect lines of real words with no model at all.

## Replication notes
Lexicon quality becomes the bottleneck — OCR fragments in the word list get placed happily. Filter by frequency or validate against a morphological resource.

## Artifacts
`padyam/lattice.py`, `scripts/compose.py`
