# EXP-04 — End-to-end validator accept/reject

| | |
|---|---|
| **Category** | A. Ground truth |
| **Origin** | ours (E4) |
| **Depends on** | EXP-01,02,03 |
| **Status** | done |
| **Cost** | seconds, CPU |

## Question
Does the assembled validator agree with expert judgement in both directions?

## Why it matters
High accuracy on accepting good poems is worthless if it also accepts bad ones. Both directions must be measured.

## Methodology
1. Select padyams a reference scanner certifies perfect on **all** rules — the positive set.
2. Select padyams it scores below 0.5 on gana — the negative set.
3. Run the validator on both; report accept rate and reject rate separately.

## Inputs
Gold corpus with per-rule reference scores.

## Metrics
Accept rate on positives; reject rate on negatives.

## Expected result / baseline
Accept >94% and reject >98%. Residual disagreement on positives is expected — sources contain OCR noise and poetic licence.

## Observed
Accepts **96.0%** of certified padyams (n=349); rejects **100.0%** of gana-broken ones (n=58).

## Replication notes
Report both rates always. A single 'accuracy' on a mixed set conceals which direction fails.

## Artifacts
`padyam/prosody/meters.py::validate`
