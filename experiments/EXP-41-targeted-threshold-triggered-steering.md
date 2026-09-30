# EXP-41 — Targeted, threshold-triggered steering

| | |
|---|---|
| **Category** | G. Steering |
| **Origin** | chandohasam (G6d / NH19, §6.1 item 2) |
| **Depends on** | EXP-22 (direction), EXP-19 (decay curve and threshold), EXP-23 (constant-steering baseline) |
| **Status** | **parked**: run as an extra arm of EXP-23, and only once EXP-23 shows an effect (EXP-23 blocked, 2026-09-29) |
| **Cost** | hours (threshold × alpha sweep) |

## Question
Does injecting the chandas direction *only* when it starts to fade prevent the
violations that follow, at a lower intervention cost than steering throughout?

## Why it matters
Global steering (EXP-23) shows at most that adding a vector helps on average.
Intervening only after a drop is detected is a sharper causal test. If
restoring the direction at that moment arrests the violations that follow, then
weakening of that direction mediates the drift. It also costs less fidelity,
because most steps are left untouched.

## Why it is parked (2026-09-24)
This experiment rests on three results that do not exist yet:
- constant steering must work (EXP-23, not run);
- the decay curve must show drops sharp enough to set a threshold from (EXP-19
  step 7, not run);
- a coherent direction must exist (EXP-22: 1 of 28 pairs done).

**Unpark when** EXP-23 shows any compliance or per-step-satisfaction gain over
its random-direction control. At that point run the arms below inside EXP-23's
harness.

## Methodology
1. **Monitor.** During generation, compute the cosine between the current
   hidden state and the direction `d^(l)` at each step. Use EXP-22's
   chandas-vs-chandas direction for the target metre; the coarse direction is a
   control.
2. **Trigger.** Once the cosine falls below a threshold `τ` (calibrated from
   EXP-19's decay curve), inject `h_l ← h_l + α·d^(l)` at the following steps,
   either for a fixed window or until the cosine recovers above `τ`.
3. **Arms**, compared at **matched average intervention magnitude**, i.e. mean
   `‖α·d‖` per generated step:
   - no steering;
   - constant steering (EXP-23's best `(layer, α)`);
   - targeted steering;
   - targeted steering with a random direction of matched norm.
4. **Score** each output with the validator for compliance, and with EXP-23's
   round-trip similarity for bhavam fidelity.
5. **Locality.** Measure the violation rate in the window after each trigger,
   compared with matched windows in the no-steering arm.

## Inputs
- A direction (EXP-22) and a threshold `τ` (EXP-19).
- A generation loop with hooks that can read and inject hidden states per
  step.
- The validator and the fidelity metric.

## Metrics
- Compliance and fidelity per arm, at matched average magnitude.
- The post-trigger violation rate compared with matched windows.
- Trigger frequency per generation.

## Expected result / baseline
NH19: targeted steering reaches compliance equal to or better than constant
steering at lower average magnitude, and so loses less fidelity.

## Observed
Not run (parked).

## Replication notes
- **Match the average magnitude across arms.** Otherwise targeted steering wins
  simply by perturbing less.
- **Include the random-direction control.** The claim is about this direction,
  not about perturbing at the moment of drift.
- **Know the baseline.** Base-model compliance is 0/189 (EXP-19), so use
  per-step guru/laghu satisfaction as the primary outcome.

## Artifacts
—
