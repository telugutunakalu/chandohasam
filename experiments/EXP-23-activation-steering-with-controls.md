# EXP-23 — Activation steering with controls

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G5 / NH15) |
| **Depends on** | EXP-22 |
| **Status** | TBD |
| **Cost** | hours (alpha × layer sweep) |

## Question
Does injecting the chandas direction improve metrical compliance without damaging meaning?

## Why it matters
The causal test of EXP-22, and the only route examined here that could make the model *prefer* metrical output rather than be filtered into it.

## Methodology
1. Sweep injection coefficient alpha × layer index.
2. At each setting measure metre compliance (validator) **and** bhavam fidelity (semantic similarity to the target meaning).
3. Include a random-direction control at matched norm, and a no-injection control.

## Inputs
EXP-22 directions; a generation loop with injection hooks; the validator; a semantic similarity metric.

## Metrics
Compliance and fidelity as a joint function of (alpha, layer); the random-direction control curve.

## Expected result / baseline
NH15: a non-trivial region where compliance improves without fidelity loss; outside it, either no effect or fidelity collapse.

## Observed
Not yet run.

## Replication notes
The random-direction control at matched norm is essential — any sufficiently large perturbation changes output, and without it a norm effect reads as a semantic one.

## Artifacts
—
