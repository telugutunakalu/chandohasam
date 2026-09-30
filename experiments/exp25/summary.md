# EXP-25: akshara-aligned tokenizer construction and round-trip validation — summary

Full specification: [`../EXP-25-akshara-aligned-tokenizer-construction-and-round-tri.md`](../EXP-25-akshara-aligned-tokenizer-construction-and-round-tri.md).
**Status:** done.

## Question
Can a vocabulary be built in which every token boundary falls on a syllable boundary?

## Method
- The text is pre-tokenised into syllables first, so subword merges can only join whole syllables.
- Each attempt is validated by a **round trip**: a gold padyam is rendered through the tokens and
  re-scanned. If the metre does not survive, the training targets are wrong.

## Findings

| attempt | approach | round-trip survival |
|---|---|---|
| 1 | isolate syllables, drop whitespace | **49.7%**: half of all targets metrically wrong |
| 2 | attach whitespace to tokens | alignment broken: merges crossed syllables |
| 3 | scansion units carrying unabsorbed whitespace | **99.3%** |

- There are two notions of a syllable. The written unit is word-local, while the scansion unit binds
  across spaces (`ముల్ కం` scans as two units, not three).
- The final vocabulary has 13,710 tokens, with 96.0% type coverage (Gemma: 15.6%, EXP-11), 99.9%
  occurrence coverage and 0 reconstruction failures.
- A model trained on attempt 1 wrote run-together text with no word boundaries (0/30 valid). Coverage
  statistics looked fine for that attempt; only the round trip exposed it.

## Evidence
The numbers are as reported in the spec. The code (`padyam/data/tokenizer.py`,
`padyam/prosody/akshara.py::split_aksharas_spaced`) is not in this repository, and there are no result
files for this experiment. The tokenizer that pilot120m uses is a different one, in
`diffusion_pretraining/tokenizer/`.
