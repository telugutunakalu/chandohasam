# EXP-20 — Causal drift analysis by component ablation

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G6c / NH17, §6.1 item 3) |
| **Depends on** | EXP-05 (including its lookup control), EXP-19 |
| **Status** | **parked**: preconditions not met on the base model (see below) |
| **Cost** | hours |

## Question
Is the probe-identified weight representation *causally* responsible for
metrical compliance?

## Why it matters
EXP-05 establishes correlation; ablation establishes dependence. That is the
difference between a representation the model uses and one that merely exists.

## Why it is parked (2026-09-24)
There is currently nothing meaningful to ablate, and nothing ablation could make
worse.
- **No component to ablate.** On the base model the only strong weight signal
  is L0, which is the embedding lookup (EXP-05). Mid-layer decodability is
  lower than L0's. Ablating L0 tests a lookup, not a prosodic representation.
- **No compliance to lose.** Base-model compliance is 0/189 (EXP-19).

**Checked 2026-09-29: still parked.**
- EXP-05's lookup control, now run with `<bos>`, finds no layer that beats the
  lookup baseline on context-determined weights (best 0.847 at L0, against
  0.887).
- EXP-19's rerun keeps base compliance at 0/200.

**Unpark when either holds:**
- EXP-05's lookup control shows a layer that beats the lookup baseline on
  context-determined weights;
- the experiment is run on a model that complies, such as the realiser
  (EXP-26) or a fine-tuned checkpoint.

The other §6 instruments now live elsewhere:

| instrument | where |
|---|---|
| decay curve and regression | EXP-19 |
| teacher-forced vs free running | EXP-35 (NH18) |
| targeted steering | EXP-41, also parked |

## Methodology
1. **Choose the component.** Take the layer (and head, if head-level probes are
   run) where EXP-05's probe beats the lookup baseline on context-determined
   aksharas.
2. **Ablate during generation.** Use zero-ablation, and mean-ablation (replace
   the output with its mean over a reference set) as the gentler control.
3. **Compare** the per-step violation pattern under ablation with unmodified
   generation, by position in the pāda.
4. **Control.** Ablate a random component of matched size at the same layer.

## Inputs
EXP-05 probe results; a generation loop with intervention hooks; the validator.

## Metrics
- Per-step guru/laghu satisfaction under ablation, against baseline and against
  the random-component control.
- Whether the ablated drift reproduces EXP-19's drift shape.

## Expected result / baseline
NH17: ablating the weight-carrying component reproduces the drift seen in
unmodified generation. Random ablation of the same size does not.

## Observed
Not run (parked).

## Replication notes
Use per-step satisfaction as the outcome. Poem-level compliance on the base
model is already 0.

## Artifacts
—
