# EXP-13: metrical constraint on a large pretrained model — summary

Full specification: [`../EXP-13-metrical-constraint-on-a-large-pretrained-model.md`](../EXP-13-metrical-constraint-on-a-large-pretrained-model.md).
**Status:** done.

## Question
Does the constraint that works on random weights (EXP-12) transfer to a model that knows the language?

## Method
- The constraint is attached to the pretrained model's own sampling loop. The spec does not name
  the model; the result files belong to the same `gemma_*` series as EXP-09 and EXP-18 (DiffusionGemma 26B).
- A free and a constrained arm run on the same four topics (amma, raithu, bhasha, vaana) and seeds.
- Metre is scored with the validator, and lexicality with a word-membership rate.

## Findings
- **Form transfers.** Gaṇa-valid lines rise from 0/16 (free) to **16/16** (constrained). Whole poems:
  0/4 free and 3/4 constrained; the amma poem fails yati.
- **Content collapses** (spec numbers):
  - the real-word rate falls from 55.7% to 15.9%;
  - the distinct-akshara ratio is 15.9%;
  - lines 2–4 are identical in three of the four topics.
- Lesson: always pair a metre metric with lexicality and repetition metrics. Metre alone reports success
  on degenerate output.

## Evidence
- [`../gemma_constrained_results.json`](../gemma_constrained_results.json): per topic and arm, the text,
  validity, and gaṇa / yati / prāsa results. The line and poem counts above are computed from it.
- The file has no real-word field, so the lexicality numbers are the spec's.
- The script (`scripts/gemma_constrained.py`) is not in this repository.
