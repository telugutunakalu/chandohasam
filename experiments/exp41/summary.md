# EXP-41: targeted, threshold-triggered steering — summary

Full specification: [`../EXP-41-targeted-threshold-triggered-steering.md`](../EXP-41-targeted-threshold-triggered-steering.md).
**Status:** parked. Not run.

## Question
Does injecting the chandas direction *only* when it starts to fade prevent the violations that follow, at a
lower cost than steering throughout (EXP-23)?

## Planned design
- Monitor the cosine between the hidden state and the direction at each step.
- Once it falls below a threshold calibrated from EXP-19's decay curve, inject the direction for a short
  window.
- Compare no steering, constant steering and targeted steering (plus a random direction) at matched
  average intervention magnitude.

## Why it is parked
It runs as an extra arm of EXP-23, and only once EXP-23 shows an effect. EXP-23 is blocked (2026-09-29): no
coherent metre direction exists (EXP-22, EXP-38).

Of its other inputs, EXP-19's decay curve now exists. It shows no smooth decay, but sharp changes at pāda
starts; see [`../exp19/summary.md`](../exp19/summary.md).

## Evidence
No results.
