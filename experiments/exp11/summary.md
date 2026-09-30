# EXP-11: tokenizer syllable-coverage audit — summary

Full specification: [`../EXP-11-tokenizer-syllable-coverage-audit.md`](../EXP-11-tokenizer-syllable-coverage-audit.md).
**Status:** done.

## Question
What fraction of Telugu syllables (aksharas) can a tokenizer emit as a single token?

## Method
- Each vocabulary token is segmented into aksharas.
- A token counts only if it is exactly one akshara **and** stays one unit when joined to a neighbour
  on either side.
- Coverage is measured over corpus akshara *types* and *occurrences* separately.

## Findings

| | Gemma (262K vocabulary) | padyam akshara-aligned (EXP-25) |
|---|---|---|
| syllable **types** covered | **15.6%** | **96.0%** |
| syllable occurrences covered | 87.5% | 99.9% |
| grid-stable single-akshara tokens | 562 | 10,334 |

- Occurrence coverage looks reassuring, but type coverage does not: common syllables such as ధా, చం, బం,
  నొ and దె do not exist as Gemma tokens.
- Type coverage is the number that predicts EXP-09's infill failure. The audit needs no model forward
  pass.

## Evidence
The numbers are as reported in the spec. The code (`padyam/prosody/constraints.py::AksharaTable`,
`padyam/data/tokenizer.py`) is not in this repository, and there are no result files for this experiment.
