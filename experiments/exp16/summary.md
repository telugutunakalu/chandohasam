# EXP-16: constraint annealing, canvas warm start and prompt richness — summary

Full specification: [`../EXP-16-constraint-annealing-canvas-warm-start-and-prompt-ri.md`](../EXP-16-constraint-annealing-canvas-warm-start-and-prompt-ri.md).
**Status:** done (negative).

## Question
Do softer constraint schedules, a better starting canvas, or richer prompts improve meaning?

## Method
- The pretrained model of EXP-13, four topics, identical seeds. The arms:
  - `free`;
  - `hard` (constrained from step 0);
  - `anneal` (grid only, then a soft penalty ramp, then a hard mask);
  - `warm` (the canvas seeded with a free draft);
  - `anneal+warm`.
- Two prompt types: a one-word topic, and rich per-line prose meanings.

## Findings (computed from the two result files)

| arm | topic prompt: valid, real words | rich prompt: valid, real words |
|---|---|---|
| free | 0/4, 55.7% | 0/4, 62.9% |
| hard | 4/4, 54.3% | 4/4, **41.5%** |
| anneal | 4/4, 53.1% | 4/4, 35.9% |
| warm | 4/4, 30.6% | 4/4, 30.1% |
| anneal+warm | 4/4, 30.6% | 4/4, 30.0% |

- **All three interventions fail.** Under both prompts, no arm beats `hard` on real words, and warm
  starting is clearly worse. The spec's table is the rich-prompt column.
- **Inversion:** the richer prompt raises the free arm and lowers every constrained arm. A specific prompt
  makes the model attempt words it cannot express within the syllable constraint.
  - The spec quotes 55.7% → 71.9% for the free arm. The rich-prompt file gives 62.9%; 71.9% is the free arm
    of `gemma_v6_iterative_refine.json`. The direction is the same.
- The first annealing implementation was silently inert (`cur_step` counts down), and identical to `hard`.

## Evidence
- [`../gemma_v4_arms_topicprompt.json`](../gemma_v4_arms_topicprompt.json) and
  [`../gemma_v5_arms_richprompt.json`](../gemma_v5_arms_richprompt.json): per topic and arm, the text,
  validity, attempts, gaṇa / yati / prāsa, and `realword`.
- [`../gemma_v6_iterative_refine.json`](../gemma_v6_iterative_refine.json): a later refine run (arms `free`,
  `hard`, `refine_free`, `refine_hard`, `refine2_hard`) that the spec does not describe.
- The script (`scripts/gemma_constrained.py --arms`) is not in this repository.
