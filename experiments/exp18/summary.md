# EXP-18: multi-akshara span placement — summary

Full specification: [`../EXP-18-multi-akshara-span-placement.md`](../EXP-18-multi-akshara-span-placement.md).
**Status:** done (negative).

## Question
EXP-11 showed that Gemma has few single-akshara tokens. Does admitting multi-syllable tokens, placed as
spans over several canvas slots, improve the output?

## Method
- A token of m syllables fills m slots: the first slot holds the token, and the rest hold padding.
- The token's internal weights, its final-syllable weight and its onset effect on the previous syllable
  are precomputed and coupled to the neighbours.
- The mechanism is checked with **random logits** first, then run with DiffusionGemma.

## Findings
- Spec numbers:
  - the placeable inventory grows from 562 to **1,424** tokens;
  - with random logits, 5 of 6 trials are fully valid, and real words appear unprompted.
  - Multi-syllable placements are **39.4%** with random logits but only **6.8%** with DiffusionGemma.
- From the result file (four topics):

| arm | valid | real words |
|---|---|---|
| free | 0/4 | 71.5% |
| single-akshara constraint | 4/4 | 34.4% |
| span constraint | 3/4 | 32.7% |
| span + refine | 3/4 | 35.4% |

- **The real-word rate does not improve.** The mechanism works, but the model declines to use it: a
  morpheme followed by padding slots is a layout it never saw in training. The random-logit control is
  what separates "the mechanism is broken" from "the model won't use it".
- The fine-tuning plan (`diffusion_finetuning/PLAN.md`) draws the same lesson: decode in the layout the
  model was trained on, and train any other layout first.

## Evidence
- [`../gemma_v8_span.json`](../gemma_v8_span.json): per topic and arm, the text, `realword`, `diversity`,
  validity and attempts. The table is computed from it.
- The inventory and placement shares are not in the file and are the spec's.
- The code (`padyam/prosody/spans.py`, `scripts/gemma_span.py`) is not in this repository.
