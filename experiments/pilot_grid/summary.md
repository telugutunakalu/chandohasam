# Pilot grid: the base pilot120m on the Gemma decoding grid — summary

Full description, tables and discussion: [`README.md`](README.md).

## Question
Under the same grid, constraints and evaluation as the Gemma runs in [`../runs/`](../runs/README.md),
what does our own 120M masked-diffusion model do before any fine-tuning? Its tokenizer has one token
per akshara, so a constraint can act on single syllables.

## Setup
- Model: `diffusion_pretraining/runs/pilot120m`, EMA weights at step 76,000. It is pretrained on
  Telugu prose only and cannot follow instructions, so the topic is given as the meaning line of the
  decoder's canvas.
- Grid: 37 metres × topics T1–T3 × seeds 42, 49, 56, 63, 70 = 555 poems per mode.
- Decoder: `diffusion_finetuning/ft/decode.py`. The Gemma grids used `metrical_decoder`
  (`meter_engine/metrical_decoder/`).
- Modes:
  - `free`: temperature 0.7, no constraint.
  - `masking`: temperature 0.7 with the grids' strict rules (canonical weights, strict prāsa, hard yati
    with the strict profile and sandhi off).
  - `own`: the decoder's defaults (16 particles, soft lexicon, soft yati weight 3, relaxed profile, rerank).
- Evaluation: the grids' definitions. "In metre" = finished ∧ canonical gaṇa ∧ strict prāsa ∧ strict
  yati (sandhi off).

## Findings (final run, `2026-09-29_ft-fixed/`)

| model | mode | in metre (strict) | attested words, topic words excluded | distinct attested words | single-akshara words | type/token |
|---|---|---|---|---|---|---|
| pilot120m | free | 0 / 555 | 17.9% | 183 | 5.9% | 0.40 |
| pilot120m | masking | **555 / 555** | **36.9%** | **757** | 19.7% | 0.55 |
| pilot120m | own | 35 / 555 (relaxed: 313) | 45.6% | 1,451 | 17.8% | 0.59 |
| Gemma (E4B, 26B, diffusion 26B) | free | 0 / 555 | 33.7–37.2% | 485–545 | 0.4–4.4% | 0.83–0.92 |
| Gemma (E4B, 26B, diffusion 26B) | masking | 555 / 555 | **10.7–16.9%** | 323–375 | 9.2–28.7% | 0.62–0.87 |

Real unseen verse (Chandassu, 555 poems) has 5.6% single-akshara words and a type/token ratio of 0.975.

- **Free generation: 0 of 555 in metre, as for every Gemma model.** The base pilot rarely stops (459
  of 555 poems run out of budget) and repeats itself.
- **Under the matched constraint, the pilot keeps its words and Gemma does not.** Masking cuts Gemma's
  attested-word share to 10.7–16.9%. The pilot keeps 36.9%, about Gemma's *unconstrained* level, with
  about twice as many distinct real words. Copying the topic accounts for only 2.8% of its words. This
  is what the one-token-per-akshara design predicts: the mask removes whole syllables, not multi-akshara
  subwords, so the model can still finish the words it starts.
- **But its words are fragmented and repetitive.** 19.7% of its words are single aksharas, and 248 of
  555 masked poems repeat a line. It has form and vocabulary without composition, as expected before
  fine-tuning.
- **The first run exposed rule gaps in the pilot decoder.** In `2026-09-29/`, masking reached only 425
  of 555. The main cause was the yati table, which accepted pairs such as త–య that no poem context
  supports. There were also gaps in the sīsa half-break, the couplet metres and prāsa. After the fixes
  in `diffusion_finetuning/ft/`, masking reaches 555 of 555.
- **The own mode's low strict rate is a design choice, not a bug.** Its yati is soft and relaxed
  (strict yati 78 / 555, relaxed 314), and it may use vikalpa weight readings (canonical gaṇa
  222 / 555). Under the relaxed profile it reaches 313 of 555. Whether to keep yati soft is an open
  decision (PLAN §6.4).
- **Judge perplexity is not a usable signal on verse.** The Gemma-3-1B judge rates real verse at 113
  and the same verse with shuffled words at 150. Repetitive outputs score far better than real verse
  (pilot free 3.5). No conclusion rests on it.

## Files
- `2026-09-29/`: the first run (the decoder before the fixes).
  - `results.jsonl`, `metrics.json`, `copy_diversity.json`, `run.json`: as for the final run below.
    This `copy_diversity.json` also holds the Gemma rows used in the table above.
  - `yati_maitri_*.npy`: the pairwise yati tables (strict and relaxed profiles, sandhi off) built for
    the first run.
- `2026-09-29_ft-fixed/`: the final run.
  - `results.jsonl`: one row per poem, with its engine verdict and per-step statistics.
  - `metrics.json`: all models' measures.
  - `copy_diversity.json`: topic copying and diversity for the pilot's modes.
  - `run.json`: the grid and the modes.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/pilot_grid.py generate OUT_DIR --modes free masking own
diffusion_pretraining/.venv/bin/python experiments/scripts/pilot_grid.py evaluate OUT_DIR
diffusion_pretraining/.venv/bin/python experiments/scripts/pilot_grid.py metrics OUT_DIR
```
The script needs `diffusion_finetuning/ft/` and `writeups/scripts/compute_generation_metrics.py`.
