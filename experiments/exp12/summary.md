# EXP-12: metrical constraint on an untrained model — summary

Full specification: [`../EXP-12-metrical-constraint-on-an-untrained-model.md`](../EXP-12-metrical-constraint-on-an-untrained-model.md).
**Status:** done.

## Question
Can sampling-time constraints alone guarantee metrical validity?

## Method
- A model with **random weights** samples with and without the constraint, with fixed seeds.
- The validator scores both arms. The text is nonsense in both, which is intended: it takes the model
  out of the question.

## Findings
- Fully valid poems rose from **0/20** without the constraint to **20/20** with it.
- Four bugs surfaced on the way, each invisible without an independent validator:
  - missing successor coupling (gaṇa 0/20);
  - the sampler and the validator bucketing prāsa differently (prāsa 0/20);
  - a top-k fallback overwriting positions already committed;
  - slot tokens exporting codas rightward on render (yati and prāsa 12/20).
- Lesson: run the constraint on random weights before any trained model. Otherwise these bugs would be
  blamed on the model.

## Evidence
The numbers are as reported in the spec. The code (`padyam/prosody/constraints.py`,
`scripts/demo_constrained_decoding.py`) is not in this repository, and there are no result files for this
experiment.
