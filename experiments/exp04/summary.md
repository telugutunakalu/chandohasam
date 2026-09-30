# EXP-04: end-to-end validator accept/reject — summary

Full specification: [`../EXP-04-end-to-end-validator-accept-reject.md`](../EXP-04-end-to-end-validator-accept-reject.md).
**Status:** done.

## Question
Does the assembled validator agree with expert judgement in both directions?

## Method
- Positive set: padyams that a reference scanner certifies perfect on all rules.
- Negative set: padyams it scores below 0.5 on gaṇa.
- The accept rate and the reject rate are reported separately.

## Findings
- The validator accepts **96.0%** of the certified padyams (n = 349).
- It rejects **100.0%** of the gaṇa-broken ones (n = 58).

## Evidence
The numbers are as reported in the spec. The validator (`padyam/prosody/meters.py::validate`) is not in
this repository, and there are no result files for this experiment.
