# EXP-03: yati rule selection with a false-positive control — summary

Full specification: [`../EXP-03-yati-rule-selection-with-a-false-positive-control.md`](../EXP-03-yati-rule-selection-with-a-false-positive-control.md).
**Status:** done.

## Question
Which definition of yati maitri should the validator use?

## Method
- Candidate rules of increasing permissiveness are compared.
- For each, recall is measured on padyams certified yati-perfect, together with the acceptance rate on
  **randomly paired aksharas** (the chance rate).
- The rule is chosen by the gap between the two, not by recall alone.

## Findings

| rule | recall (4 metres) | random pairs accepted |
|---|---|---|
| first consonant only | 64–93% | 12.9% |
| **samyukta (any onset consonant)** | **98.8–99.8%** | **17.0%** |
| + svara (vowel) fallback | 99.8–100% | 52.6% |

- The vowel fallback reaches near-perfect recall but accepts half of all random pairs, so it no longer
  constrains anything.
- **Samyukta was selected.** The random-pair control is what decided it.

## Evidence
The numbers are as reported in the spec. The rule (`padyam/prosody/meters.py::yati_compatible`) is not
in this repository, and there are no result files for this experiment.
