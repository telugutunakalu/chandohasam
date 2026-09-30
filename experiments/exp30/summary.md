# EXP-30: word-lattice composition — summary

Full specification: [`../EXP-30-word-lattice-composition.md`](../EXP-30-word-lattice-composition.md).
**Status:** done.

## Question
Can composing with whole words, instead of syllables, remove the sub-word fragments that syllable-level
decoding produces?

## Method
- A lattice whose edges are whole lexicon words (2–6 aksharas) and whose paths are exactly the
  metrically legal lines.
- Each state is (position, obligation), where the obligation records that a word's last syllable weight
  depends on the next word's onset.
- Yati and prāsa are checked wherever the rule position falls, even inside a word.
- The lattice is searched by beam, scored by the realiser and by the planner's content words.

## Findings
- The lattice has **1,166,174 edges** (spec: over 60 states), reduced to 5,116 after frequency capping.
- **All four topics give metrically valid poems.** The spec reports zero fragments.
- The poems use 7–13 of the 23–25 planner content words (10/24, 13/25, 7/24, 7/23). The spec's
  "10–13 of ~25" covers only the first two topics.
- Metre and lexicality now hold by construction, so the open question moves to which path is chosen
  (EXP-31). Lexicon quality becomes the bottleneck, because OCR fragments in the word list are placed
  happily.

## Evidence
- [`../composer_run.log`](../composer_run.log): the lattice size, and for each topic the planner draft,
  its content words and the composed padyam, with validity and planner words used.
- The code (`padyam/lattice.py`, `scripts/compose.py`) is not in this repository.
