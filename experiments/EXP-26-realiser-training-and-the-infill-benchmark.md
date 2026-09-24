# EXP-26 — Realiser training and the infill benchmark

| | |
|---|---|
| **Category** | H. Training |
| **Origin** | ours (E14) ★ |
| **Depends on** | EXP-09,25 |
| **Status** | done |
| **Cost** | 20 min on one GB10 |

## Question
Does an akshara-aligned vocabulary make the EXP-09 task learnable at small scale?

## Why it matters
The direct test of the EXP-09 diagnosis. If the failure was representational, fixing the representation should make a small model succeed where a large one could not.

## Methodology
1. Train from random initialisation, masked diffusion, in two phases: general text for fluency, then the task with the prompt protected from corruption.
2. Evaluate on the **identical** EXP-09 protocol — same padyams, same blanking rates, same baselines.
3. Report alongside the large model's numbers.

## Inputs
Akshara-aligned corpus; exact-metre grid padyams; the EXP-09 harness.

## Metrics
Weight accuracy and exact recovery at each blanking rate; training wall-clock.

## Expected result / baseline
If the diagnosis holds, a small model should substantially beat the frequency baseline and the large model.

## Observed
39.2M params, 20 minutes total from random init.

| blanked | weight correct | exact recovery | freq baseline | 26B model |
|---|---|---|---|---|
| 10% | **99.0%** | 94.8% | 57.3% | 10.4% length |
| 25% | **97.9%** | 90.3% | 57.3% | **0.0%** |
| 50% | **96.2%** | 78.7% | 57.3% | **0.0%** |

A model ~600× smaller solves what the larger one cannot attempt.

## Replication notes
Keep the evaluation protocol byte-identical to EXP-09 or the comparison is worthless. This pairing is the project's central result.

## Artifacts
`padyam/train.py`, `scripts/eval_realiser.py`, `checkpoints/realiser.pt`
