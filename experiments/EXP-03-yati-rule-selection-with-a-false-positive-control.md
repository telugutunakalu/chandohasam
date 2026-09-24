# EXP-03 — Yati rule selection with a false-positive control

| | |
|---|---|
| **Category** | A. Ground truth |
| **Origin** | ours (E3) |
| **Depends on** | EXP-01 |
| **Status** | done |
| **Cost** | seconds, CPU |

## Question
Which definition of yati maitri should the validator use?

## Why it matters
Yati is one of three constraints enforced during decoding. Too strict and valid poems are rejected; too loose and the constraint stops constraining. Recall alone cannot answer this.

## Methodology
1. Define candidate matching rules of increasing permissiveness (first consonant only; any onset consonant; plus vowel-family fallback).
2. For each, measure recall on padyams a reference scanner certifies yati-perfect.
3. **For each, also measure the acceptance rate on randomly paired aksharas** — the chance rate.
4. Choose by the gap between the two, not by recall.

## Inputs
Gold padyams with per-rule reference scores; a random-pair sample drawn from the same corpus.

## Metrics
Per-meter recall; random-pair acceptance rate (false-positive proxy).

## Expected result / baseline
Permissiveness raises both numbers. The useful rule maximises recall while its chance rate stays near the base rate implied by the equivalence classes.

## Observed
| rule | recall (4 meters) | random pairs accepted |
|---|---|---|
| first consonant only | 64–93% | 12.9% |
| **samyukta (any onset consonant)** | **98.8–99.8%** | **17.0%** |
| + svara fallback | 99.8–100% | **52.6%** ✗ |

Svara yati reaches near-perfect recall and accepts **half of all random pairs** — useless as a constraint. Selected samyukta.

## Replication notes
Step 3 is the whole experiment. Any rule-selection task with a permissiveness dial needs a chance-rate control, or the most permissive rule always appears best.

## Artifacts
`padyam/prosody/meters.py::yati_compatible`
