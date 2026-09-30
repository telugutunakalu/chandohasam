# EXP-26: realiser training and the infill benchmark — summary

Full specification: [`../EXP-26-realiser-training-and-the-infill-benchmark.md`](../EXP-26-realiser-training-and-the-infill-benchmark.md).
**Status:** done.

## Question
Does an akshara-aligned vocabulary (EXP-25) make EXP-09's infill task learnable at small scale?

## Method
- A small masked-diffusion model, the realiser, is trained from random initialisation in two phases:
  general text for fluency, then the task, with the prompt protected from corruption.
- It is evaluated on the identical EXP-09 protocol, with the same blanking rates and the same frequency
  baseline.

## Findings (60 held-out padyams, out of 720 usable gold padyams)

| blanked | weight correct | exact recovery | frequency baseline | DiffusionGemma 26B (EXP-09) |
|---|---|---|---|---|
| 10% | **99.0%** | 94.8% | 57.3% | lines keep their length only 10.4% of the time |
| 25% | **97.9%** | 90.3% | 57.3% | 0 of 48 lines keep their length |
| 50% | **96.2%** | 78.7% | 57.3% | 0 of 48 lines keep their length |

- The spec gives 39.2M parameters and 20 minutes of training from random initialisation on one GB10.
- **A model about 600× smaller solves what the 26B model cannot attempt.** This supports EXP-09's
  diagnosis that the failure is representational (the tokenizer, EXP-11), not a matter of scale. The
  spec calls this pairing the project's central result.

## Evidence
- [`../realiser_eval.log`](../realiser_eval.log), "TASK 1": the table above. The log begins with a
  traceback from an earlier failed attempt (a CPU/GPU device mismatch); the results follow it.
- The code and checkpoint (`padyam/train.py`, `scripts/eval_realiser.py`, `checkpoints/realiser.pt`) are
  not in this repository.
