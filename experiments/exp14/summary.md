# EXP-14: repetition penalties, priority-ordered relaxation and rejection sampling — summary

Full specification: [`../EXP-14-repetition-penalties-and-priority-ordered-constraint.md`](../EXP-14-repetition-penalties-and-priority-ordered-constraint.md).
**Status:** done.

## Question
Can EXP-13's degenerate output be fixed without weakening the metre?

## Method
- **Priority order:** on a conflict the lowest-priority constraint is dropped, and gaṇa never is. Each
  relaxation is counted.
- **Soft repetition penalties:** three kinds, applied to the logits (same index in another line, a local
  window in the line, frequency across the canvas).
- **Rejection sampling** (formerly EXP-15): up to N candidates per prompt, stopping at the first the
  validator accepts. The informative number is the attempts needed.

## Findings
- Spec numbers:
  - gaṇa was relaxed **0 times**, yati 15–33 times and prāsa 0;
  - the distinct-akshara ratio rose from 15.9% to **70.0%**, above the unconstrained 62.2%;
  - duplicate lines fell from 6 to 0;
  - the real-word rate rose from 15.9% to 41.5%.
- In the file, the penalty run's constrained arm gives 3 of 4 valid poems; raithu fails one yati.
- **Rejection sampling: 4 of 4 valid, with attempts 1, 2, 1 and 1** (five generations for four poems).
- Lesson: instrument the relaxation counters. The first implementation's fallback silently discarded the
  most important constraint.

## Evidence
- [`../gemma_v2_reppenalty.json`](../gemma_v2_reppenalty.json): the repetition-penalty run.
- [`../gemma_v3_bestof.json`](../gemma_v3_bestof.json): rejection sampling, with `attempts` per topic.
  This file confirms the 4/4 and the attempts.
- The relaxation counts and the diversity numbers are not in these files and are the spec's.
- The script (`scripts/gemma_constrained.py`) is not in this repository.
