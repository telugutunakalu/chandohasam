# EXP-32: corpus ingestion and quality audit — summary

Full specification: [`../EXP-32-corpus-ingestion-and-quality-audit.md`](../EXP-32-corpus-ingestion-and-quality-audit.md).
**Status:** done.

## Question
What does the corpus contain, and at what quality bar should each part be used?

## Method
- The fields and their coverage are enumerated as found, not as documented.
- Separate outputs are written at different quality bars: everything for pretraining, and exact-metre
  poems only for supervised grid targets.
- The vocabulary of the prose annotations is compared with that of the verse (a register audit).

## Findings
- **382,052 poems** in all.
- **33,253** exact-metre grid padyams (7.8× the earlier 4,245).
- **168,371** (meaning, poem) pairs.
- **767,226** glossed words, with **351,991** sandhi decompositions.
- 70.0M pretraining tokens.
- **The strict bar is severe, not the corpus unreliable.** Of 25,637 correctly shaped utpalamala poems,
  15,480 match at all 80 positions. That is close to what 0.99⁸⁰ ≈ 45% predicts for 99% per-position
  agreement.
- **Register:** only **12.8%** of the prose-annotation vocabulary appears in the verse, and 81,530 word
  types occur only in prose. A model trained on classical verse alone will write classical Telugu, not
  the contemporary register the project targets.

## Evidence
The numbers are as reported in the spec. The ingestion scripts (`scripts/ingest_padyarchana.py`,
`scripts/mine_padyams.py`) are not in this repository, and there are no result files for this experiment.
