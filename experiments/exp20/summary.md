# EXP-20: causal drift analysis by component ablation — summary

Full specification: [`../EXP-20-causal-drift-analysis-by-component-ablation.md`](../EXP-20-causal-drift-analysis-by-component-ablation.md).
**Status:** parked. Not run.

## Question
Is the weight representation that a probe finds *causally* responsible for metrical compliance? The
test is to ablate it during generation and see whether the metre drifts.

## Why it is parked
There is nothing meaningful to ablate, and nothing to lose (re-checked 2026-09-29):
- **No component to ablate.** EXP-05's lookup control finds no layer that beats a token lookup on
  context-determined weights. The best is 0.847 at L0, the embedding output, against 0.887.
- **No compliance to lose.** The base model writes 0 of 200 poems in metre (EXP-19).

## Unpark when
- EXP-05's lookup control shows a layer that beats the lookup on context-determined weights; or
- the experiment can run on a model that complies with the metre, such as the realiser (EXP-26) or a
  fine-tuned checkpoint.

## Evidence
No results. The preconditions come from [`../exp05/summary.md`](../exp05/summary.md) and
[`../exp19/summary.md`](../exp19/summary.md).
