# EXP-17: recursive context expansion across iterations — summary

Full specification: [`../EXP-17-recursive-context-expansion-across-iterations.md`](../EXP-17-recursive-context-expansion-across-iterations.md).
**Status:** done (saturates).

## Question
Does feeding back every earlier attempt, each with the validator's exact diagnosis, keep improving the
output?

## Method
- The pretrained model of EXP-13, four topics, five iterations.
- Iteration 0 sees the meaning only. Iteration k also sees all earlier free drafts, each annotated with
  its diagnosis.
- Each iteration writes a free draft and a constrained poem.

## Findings (computed from the result file; means over the four topics)

| iteration | context (tokens) | free real words | free gaṇa-valid lines | free line length | constrained real words |
|---|---|---|---|---|---|
| 0 | 264–295 | 73.7% | 0/16 | 14.6 | 32.3% |
| 1 | 539–572 | 70.5% | 0/16 | 15.2 | **40.8%** |
| 2 | 753–796 | 73.3% | 0/16 | 15.1 | 40.9% |
| 3 | 965–1,020 | 73.3% | 0/16 | 15.1 | 30.9% |
| 4 | 1,177–1,244 | 72.7% | 0/16 | 15.4 | 39.4% |

- **It saturates at one draft.** Over iterations 1–4, the constrained real-word rate has a mean of 38.0%
  and an sd of 10.3 points across topic × iteration, so variance swamps any trend. The context grew
  about 4.3× for nothing.
- **The free arm never improves.** It has 0/16 gaṇa-valid lines at every iteration, with mean line length
  14.6–15.4 against a target of 20, although it is shown up to four annotated attempts.
- The limit is therefore not information.

## Evidence
- [`../gemma_v7_iterative.json`](../gemma_v7_iterative.json): per topic, five rows with `ctx_tokens`, the
  free and constrained texts, `free_realword`, `free_gana`, `free_meanlen` and `con_realword`. The table
  is computed from it.
- The script (`scripts/gemma_iterative.py`) is not in this repository.
