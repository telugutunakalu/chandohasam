# EXP-19 — Generation-time tracking

| | |
|---|---|
| **Category** | F. Generation mechanics |
| **Origin** | chandohasam (G2 / NH12) |
| **Depends on** | EXP-09 |
| **Status** | done (base model) |
| **Cost** | minutes per sample |

## Question
What distinguishes generation steps that violate the metre from those that do not?

## Why it matters
Moves from 'the model fails' to 'it fails here, for this reason'. Identifies whether drift is positional decay or triggered by specific linguistic events.

## Methodology
1. Generate a large sample of (bhavam → poem) completions.
2. Log per-step metrics: entropy, top-k margin, position, distance to the nearest sandhi junction and pada boundary.
3. Score each final output with the validator (pass/fail plus violation locations).
4. Align per-step traces with the outcome; test which step-level features predict violation.

## Inputs
(bhavam, poem) pairs; a generation loop exposing per-step distributions; the validator.

## Metrics
Violation rate vs entropy, vs sandhi proximity, vs raw position.

## Expected result / baseline
NH12: violation correlates with entropy spikes and sandhi proximity **more than with position alone**. Position is the null model.

## Observed
Run on the base model in the chandohasam pipeline; full traces in that repo.

## Replication notes
Include raw position as an explicit competing predictor, or any correlation with 'later in the line' will masquerade as a linguistic finding.

## Artifacts
chandohasam `pipeline/`
