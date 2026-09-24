# EXP-28 — Diffusion objective ablation — masked vs uniform vs continuous

| | |
|---|---|
| **Category** | H. Training |
| **Origin** | ours (E19) |
| **Depends on** | EXP-26 |
| **Status** | done |
| **Cost** | ~45 min for three arms |

## Question
Which corruption process is best for this task at matched compute?

## Why it matters
A foundational architecture choice. Published guidance exists but is derived at much larger scale and on different data.

## Methodology
1. Hold backbone, tokenizer, data, steps, batch and learning rate fixed; vary only corruption and loss.
2. **Do not compare training losses.** They are not commensurable: masked computes loss at corrupted positions only, uniform at all positions, continuous is an embedding MSE.
3. Score all three on the same downstream task (EXP-09 infill) judged by the rule validator.
4. Record wall-clock per arm — objectives differ in cost.

## Inputs
One corpus; three objective implementations; the EXP-09 harness.

## Metrics
Weight accuracy and exact recovery at several corruption rates; minutes per arm.

## Expected result / baseline
Published work favours masked over uniform at scale. Continuous latent text diffusion is known to be unstable.

## Observed
49M tokens per arm. Uniform finished at CE 2.41 vs masked's 4.65 **while being the harder task** — it computes loss over positions never corrupted. That is why loss cannot be the verdict.

| objective | weight@15 | exact@15 | weight@35 | exact@35 | weight@60 | exact@60 | min |
|---|---|---|---|---|---|---|---|
| masked | 79.8% | 16.7% | **71.1%** | 10.1% | 52.2% | 2.9% | 10 |
| uniform | **80.1%** | **21.5%** | 70.7% | **13.6%** | **57.1%** | **6.1%** | 11 |
| continuous | 61.9% | 0.6% | 46.7% | 1.1% | **17.9%** ✗ | 0.8% | 22 |

**Continuous rejected**: training loss rose during the run and at 60% corruption it scores *below* the 57% chance baseline — outputs anticorrelated with the metre — at half the throughput.

**Masked selected despite uniform's edge**, on architectural grounds: under uniform corruption there is no mask symbol, so 'which positions remain open' is undefined, and the constraint, the anchor-ordered sampler, the recovery procedure and the infill benchmark all require it.

## Replication notes
Two caveats on the uniform result: it receives ~2× the supervised positions per step (compute matched, gradient signal not), and 49M tokens measures early-training behaviour. To settle it, match supervision-per-step and scale the budget 10–20×.

## Artifacts
`padyam/objectives.py`, `scripts/ablate.py`, `experiments/ablation.json`
