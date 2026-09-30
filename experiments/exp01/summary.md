# EXP-01: prosody engine validation against gold annotation — summary

Full specification: [`../EXP-01-prosody-engine-validation-against-gold-annotation.md`](../EXP-01-prosody-engine-validation-against-gold-annotation.md).
**Status:** done.

## Question
Does rule-based akshara segmentation and laghu/guru scansion reproduce expert annotation?

## Method
- The rule engine segments and scans every padyam of the Chandassu corpus
  (`BodduSriPavan111/chandassu`, 4,651 padyams with gold `lg_data`).
- The akshara lists and the weights are compared with the gold labels.
- Disagreements are grouped by (akshara, next akshara), so each group points to one rule.

## Findings
- Segmentation matches the gold for **99.87%** of padyams.
- Weights match for **99.9984%** of aksharas (5 errors in 320,159), and **99.89%** of padyams are fully
  correct. The remaining errors are malformed gold (OCR artefacts).
- The measurement found four engine bugs:
  - word-final pollu attachment;
  - the geminate ఱ్ఱ misread as ra-vattu;
  - line breaks acting as cluster barriers (spaces do not);
  - an onset cluster hidden behind a trailing coda.
- The spec's published baseline for the same task is 99.43% for syllable counting and 93.82% for the gaṇa
  sequence.

## Evidence
The numbers are as reported in the spec. The engine (`padyam/prosody/akshara.py`) and its tests are not
in this repository, and there are no result files for this experiment.
