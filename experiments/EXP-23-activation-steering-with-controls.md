# EXP-23 — Activation steering with controls

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G5 / NH15) |
| **Depends on** | EXP-22 (including its all-pairs coherence step) |
| **Status** | TBD |
| **Cost** | hours (alpha × layer sweep) |

## Question
Does injecting a chandas direction improve metrical compliance without damaging
meaning?

## Why it matters
This is the causal test of EXP-22, and the only route examined here that could
make the model *prefer* metrical output rather than be filtered into it.

## Design revision (2026-09-24, from EXP-22's results)
The coarse (poem-vs-bhavam) direction is the weak, register-dominated one
(peak coherence 0.322), so steering with it is likely to push towards generic
poeticness. The **primary** run now steers with a chandas-vs-chandas direction,
`d(target metre) − d(contrasting metre)` (coherence 0.5–0.65). The coarse
direction becomes the secondary comparison.

## Methodology
1. **Primary run.** Inject `h_l ← h_l + α·d^(l)` at every generated token,
   using the chandas-vs-chandas direction for the target metre. Start with
   కందము vs మత్తకోకిల, the only pair extracted so far, and add pairs as EXP-22's all-pairs step
   flags them as coherent.
2. **Secondary run.** Repeat with the coarse direction.
3. **Sweep α** over {0.5, 1, 2, 3, 5, 8} and a few candidate layers, chosen from
   EXP-05 and EXP-21 (the literature's starting point is about 2/3 depth).
4. **Controls at every (α, layer)**: a random direction of matched norm, and
   no injection.
5. **Measure together**:
   - metre compliance (validator);
   - bhavam fidelity, by round trip: paraphrase the generated poem back into a
     description and compare it with the original bhavam.
6. **Plot** compliance and fidelity against α, separately for each direction
   type.

## Inputs
EXP-22/39 directions; a generation loop with injection hooks; the validator; a
semantic similarity metric.

## Metrics
- Compliance and fidelity as a joint function of (α, layer), for the
  chandas-vs-chandas direction, the coarse direction and the random control.
- The best operating point for each direction type.
- Whether the chandas-vs-chandas direction beats the coarse one on compliance
  at a matched fidelity cost.

## Expected result / baseline
- NH15: a non-trivial region where compliance improves without fidelity loss.
  Outside it, either no effect or fidelity collapse.
- EXP-22's coherence gap predicts that chandas-vs-chandas outperforms coarse.

## Observed
Not yet run.

## Replication notes
- **The random-direction control at matched norm is essential.** Any
  sufficiently large perturbation changes the output, and without the control a
  norm effect reads as a semantic one.
- **Base compliance is 0/189 (EXP-19).** Report per-step guru/laghu
  satisfaction as well as whole-poem compliance, or every arm may read 0.

## Artifacts
—
