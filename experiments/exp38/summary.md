# EXP-38: synthetic tight-contrast set for a metre-specific direction — summary

Full specification and discussion: [`../EXP-38-synthetic-tight-contrast-set-for-a-metre-specific-direction.md`](../EXP-38-synthetic-tight-contrast-set-for-a-metre-specific-direction.md).

## Question
EXP-22's contrasts mix metre with register (poem vs prose). Can pairs of texts that keep content and
register fixed, and differ only in metrical correctness, isolate a metre direction?

## How the synthetic data is made (`build`)
- **Sources:** 4-line Bhāgavatam poems of the 8 sample metres that the engine accepts in their
  labelled metre (relaxed profile, sandhi hypothesis).
- **Edits:**
  - *Synonym:* a verse word is replaced by its single-word gloss from the commentary (teeka).
  - *Swap:* two adjacent words in one line are exchanged.
- **Roles:** each triple is (source, break, preserve).
  - A *break* is an edit after which the labelled metre is no longer among the DAWG's candidates.
  - A *preserve* is an edit that the engine still accepts.
- **Limits:** at most one triple per source poem, and 25 per metre and edit kind.
- 361 triples are built, and every metre yields some. Mattakokila (19 triples, from 41 poems) and
  śārdūlavikrīḍitamu (42) fall short of the cap of 50.

## Extraction and analysis
- **Content check** (in `extract`): the IndicSBERT cosine of each variant with the source's bhavam may
  be at most 0.05 below the source's. 357 of 361 triples pass (169 synonym, 188 swap), with a median
  drop of 0.003.
- Last-token states of `gemma-4-E2B-it` with `<bos>` (as in EXP-22) for all three texts of each triple.
- Directions:
  - `d_break` = source − break;
  - `d_preserve` = source − preserve;
  - `d_metre` = `d_break` − `d_preserve`, i.e. preserve − break for each triple.
- Coherence is the mean pairwise cosine across triples. The null for `d_metre` flips the sign of each
  triple at random.

## Findings

| | all 357 | synonym 169 | swap 188 |
|---|---|---|---|
| peak coherence, `d_break` | 0.138 (L0) | 0.023 (L4) | 0.138 (L0) |
| peak coherence, `d_preserve` | 0.135 (L0) | 0.012 (L35) | 0.151 (L0) |
| peak coherence, `d_metre` | **0.011** (L0); ≤ 0.002 at L1–L35 | 0.008 (L2) | 0.011 (L0) |
| sign-flip null for `d_metre`, 95th / 99th percentile | 0.034 / 0.059 | 0.005 / 0.008 | 0.035 / 0.057 |
| cos(`d_break`, `d_preserve`) over layers, median (range) | **0.72** (0.58–0.91) | 0.40 (0.04–0.82) | 0.74 (0.59–0.89) |

- **No metre-specific direction.** The per-triple metre difference has no consistent direction at any
  layer. Its coherence is at or below the null everywhere, apart from a negligible 0.008 in the
  synonym subset.
- **The break and preserve directions are largely parallel** (median cosine 0.72; 0.74 for swaps).
  What the contrast isolates is "this text was edited", not metrical correctness.
- **NH14 is not supported.** The tight contrast is no more coherent than EXP-22's coarse contrast
  (0.475) or its metre pairs (at most 0.158).
- **Consequence:** with EXP-22, no coherent metre direction exists to steer with, so EXP-23 is blocked.

## Files
- `2026-09-29_tight/`:
  - `triples.jsonl`: all 361 triples: the source, its bhavam, and the break and preserve variants.
  - `kept.jsonl`: the ids of the 357 that pass the content check, with their similarity scores.
  - `build.json`, `extract.json`: the yield per metre and the extraction record.
  - `summary.json`: the coherence results.
- The pooled states (`pooled_source.npy`, `pooled_break.npy`, `pooled_preserve.npy`, 75 MB each) are
  not in git; `extract` rebuilds them.

## Reproduce
```bash
diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py build OUT_DIR     # CPU
diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py extract OUT_DIR   # GPU
diffusion_pretraining/.venv/bin/python experiments/scripts/exp38_tight_contrast.py analyse OUT_DIR   # CPU
```
