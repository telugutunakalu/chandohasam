# full_grid_experiments

The paper's main experiment: **every model of the project, fine-tuned and not, free and under the metrical decoder,
on one set of 100 prompts, scored by one scorer.** Earlier results came from separate experiments with different
prompt sets, prompt formats and decoders. This grid answers one question with everything else held fixed: which model
family, size and training, with or without the metre constraint, writes the best padyams for a prompt?

Status 2026-10-31:
- **Complete.** 17 rows, 34 v1 cells, 8 extra-strategy cells and 17 v2 cells, 5,472 scored poems with the gold.
- **Reproduced 10-31:** scored again from the raw runs, the table, the per-poem scores and the v2 samples come out
  byte-identical ([Checks](#checks)).

The user's design decisions, numbered, are listed at the end ([Decisions](#decisions)); other folders cite them by
number.

## Contents

1. [The findings, in short](#the-findings-in-short)
2. [What is where](#what-is-where)
3. [The design](#the-design): prompts, rows, cells, measures
4. [How it ran](#how-it-ran), with [Phase 0](#phase-0)
5. [Results](#results)
6. [Checks](#checks)
7. [Caveats](#caveats)
8. [Scripts](#scripts), [reproducing](#reproducing), [results files](#results-files)
9. [Decisions](#decisions)

## The findings, in short

Every number below is from `results/grid.md` (paired tests over the 100 prompts: bootstrap, 10,000 resamples) or
`results/analysis.md`.

1. **No model writes metrical poems freely.**
   - The fine-tuned T5Gemma 270M and 1B are best: 8% of free poems in metre; T5Gemma 4B 7%, Nandi 5%, the MDLMs
     0–1%, the 48k snapshot and DiffusionGemma FT 0%.
   - Every base model: 0%.
   - The source poems themselves pass the strict check 53% of the time.
2. **The metrical decoder puts 99–100% in metre** for every fine-tuned row and every instruction-tuned base. Below
   100% are the two MDLM bases (93%, 85%), the MDLM 523M FT and the T5Gemma 4B FT (99% each). Every one of those
   poems ran out of its token budget before it was finished. No finished poem is out of metre.
3. **Fine-tuning is what makes the constrained poems real**, for every family but DiffusionGemma:
   - real words +18 to +36 points over the base under the decoder, every p < 0.001;
   - recognition of the prompt +35 to +58 points for the whole-pool rows (+14 for the 48k snapshot).

   The whole-pool DiffusionGemma LoRA did not help: real words −3.9 (p 0.052), recognition −17 (p 0.008).
4. **The best constrained rows** (v1 real words / recognised):
   - MDLM 120M FT 77.7% / 73%;
   - MDLM 523M FT 77.5% / 77%;
   - T5Gemma 270M FT 75.3% / 64%;
   - T5Gemma 1B FT 74.1% / 66%;
   - Nandi FT 73.0% / 64%;
   - T5Gemma 4B FT 72.8% / 63%.

   The source poems score 85.7% / 63%.
5. **The constraint costs the fine-tuned rows little and the bases a lot.**
   - Real words from free to constrained, the six whole-pool fine-tuned rows other than DiffusionGemma: −4.2
     (T5Gemma 270M FT) to −13.9 points (MDLM 120M FT); the 48k snapshot −14.3.
   - For the bases: −39 to −67 points (the −67 rests on the 26 T5Gemma 4B base poems with any word). They write fluent
     prose freely and break it into non-words to fit the metre. DiffusionGemma FT behaves like a base here: −50.1.
6. **Decoder v2 (A + B) raises real words in all 17 rows,** by +3.9 to +13.1 points (every p ≤ 0.007), and keeps
   everything in metre; the two MDLM bases reach 100%.
   - **Recognition is unchanged,** except MDLM 120M FT −10 (p 0.039).
   - **The best cell of the grid** is MDLM 523M FT with v2: 85.4% real words, 76% recognised, 100% in metre. That is
     the source poems' level on real words (85.7%).
   - **The cost:** repeated lines rise on five base rows. The largest rise is MDLM 523M base, from 13% to 39% of
     poems; the highest v2 rate is T5Gemma 270M base, 42%.
7. **No model copies its source poem:** no grid poem shares 12 aksharas with its gold. Lines copied from the training
   split appear only in four bases' free poems (1–3%).
8. **Gemma-4 and DiffusionGemma as bases paraphrase rather than compose.**
   - Free, they write fluent prose (real words 87–97%, recognised 92–100%) but copy 16–29% of their words from the
     prompt.
   - Under the decoder their real words fall to 34–53%. Gemma-4 26B repeats a line in 30% of poems.

## What is where

| what | where | in git |
|---|---|---|
| code | `grid.py`, `prompts.py`, `build_records.py`, `build_grid100.py`, `run_hf.py`, `v2.py`, `score_grid.py`, `sample_review.py`, `analyse_grid.py` | yes |
| results | `results/`: the table, every poem's scores (numbers only), the per-cell decoder reports, the v2 samples, a sample close reading, the checks | yes |
| prompts | `prompts/`: the P1 retellings (first batch: `p1.jsonl`, every attempt, the review sample and the hand edits; second batch: `grid100/p1/`), the selection of the 100, and the grid's records (`prompts/grid100/records/test.jsonl`: the held-out `dataset/` poems with their bhāvams, glosses and P1, and the 10 Gemini records) | yes, except the first batch's records (`prompts/e6_p1/records/`, a near-duplicate) and the records' `train.jsonl` / `val.jsonl` links into the confidential E6 split |
| generated poems (Gemma-4 rows) | `runs/grid_gemma4_*`: `results.jsonl` (the poems), `traces.jsonl`, `prompts.jsonl`, `run.json` | yes |
| generated poems (other rows) | each model's own folder: `../autoregressive_finetuning/runs/grid_nandi_*`, `../t5_finetuning/runs/grid_t5_*`, `../diffusion_finetuning/runs/grid_mdlm*`, `../lora_gemma_diffusion/runs/grid_dg_*` (those `runs/` folders also hold checkpoints) | no |
| logs | `logs/`: one per cell, and the first P1 batch's run (`prompts_p1_183.log`) | yes |

The queues that ran the cells are `../experiments/scripts/gpu_queue_2026-10-2*.sh` and `grid_*_2026-10-*.sh`, with
their log `../experiments/runs/gpu_queue_2026-10-21.log` (described in `../experiments/README.md`).

## The design

### Prompts: 100 held-out poems (`build_grid100.py`, `prompts.py`)

**Source poems.**
- Every prompt is a poem held out of all fine-tuning: poems of three of the `dataset/` works (no chandassu poem was
  drawn), removed with the rest of `dataset/` from the training split on 2026-10-13, and Gemini poems.
- Every one of them is also a poem of the human-evaluation pool (decision 20), so the grid's poems can be set beside
  human ratings of the same prompts.
- Each prompt keeps its source poem, the **gold**: the reference for the metre pattern and for the copy check.

| source | prompts | how the prompt text was made |
|---|---|---|
| Pothana's Bhāgavatam | 50 | P1 retelling |
| Vemana | 20 | P1 retelling |
| Kūcimañci Timmakavi | 20 | P1 retelling |
| Gemini-written poems | 10 | Gemini's own bhāvam, as is |

| origin (`selection.json`) | prompts |
|---|---|
| human-eval phase 1, P1 of the first batch | 13 |
| human-eval phase 1, P1 of the second batch | 33 |
| human-eval phase 1, Gemini bhāvam | 10 |
| rest of the 500-poem pool, P1 of the first batch | 21 |
| rest of the pool, P1 of the second batch | 23 |

The P1 retellings were made in two batches: the first for 183 held-out poems, 34 of which are in the grid; the second
for the 56 grid poems the first did not cover. 56 prompts are phase-1 poems that annotators rated; the other 44 are
candidates for a phase 2 of the human evaluation
(`prompts/grid100/phase2_candidates.json`). They span 24 metres: 47 prompts in the 7 common vṛttas whose line pattern
the scorer checks (utpalamāla, campakamāla, mattebha, śārdūla, mattakōkila, mālini, bhujaṅgaprayāta) and 53 in other
metres, 16 of them in 11 other fixed-pattern vṛttas (sragdhara, layagrāhi, …). The largest are kandamu and āṭaveladi (11 each), mattebha, campakamāla and
tēṭagīti (10 each); `results/analysis.md` §1 has them all.

**P1, the retold bhāvam** (the one prompt form; decision 7).
- **How:** Gemma-4 26B-A4B-it, running locally, retells the poem's bhāvam: the same events and meaning, new wording
  and order. No model can recall the wording from training or web text, and the meaning can still be measured against
  it. Up to three attempts: the first at temperature 0.3 (seed 42), the retries at 0.7 (seeds 43, 44).
- **Automatic checks** (`prompts.py`):
  - Telugu script only;
  - meaning kept: LaBSE similarity to the source bhāvam ≥ 0.567 (the 99th percentile of similarities between
    different bhāvams), and the source bhāvam ranked first among all the batch's sources (the second batch: the 183
    and its own 56 together);
  - not a copy: ≤ 40% of 2+-akshara words shared with the source bhāvam;
  - no gold text: no run of 12 aksharas shared with the gold poem;
  - length 0.6–1.4× the source;
  - it fits the MDLM canvas.
- **The grid's 90 P1 prompts all passed every automatic check as generated.**
  - **The 34 of the first batch** (`prompts/p1.jsonl`, every attempt in `p1_attempts.jsonl`): 7 of them were in the
    user's review sample (`prompts/p1_review.md`), and 4 carry the user's hand edits (`prompts/p1_edits.jsonl`), which
    restore addresses; one of them (`kuchimanchi-1209`) takes its prompt over the copy limit.
  - **The 56 of the second batch** (`prompts/grid100/p1/`): approved in advance by the user (decision 21), without a
    hand review.
- **Known bias:** the retelling model is itself a grid row (Gemma-4 26B).

### Rows: 17 checkpoints (`grid.py` ROWS)

| family | model | base | fine-tuned (training poems × passes) |
|---|---|---|---|
| autoregressive | Nandi-Mini-150M | ✓ | bhāvam → poem, 300,763 × 3.5 |
| autoregressive | Gemma-4 E4B-it | ✓ | — |
| autoregressive | Gemma-4 26B-A4B-it | ✓ | — |
| encoder-decoder | T5Gemma 2 270M | ✓ | full, 300,763 × 1 |
| encoder-decoder | T5Gemma 2 1B | ✓ | full, 300,763 × 1 |
| encoder-decoder | T5Gemma 2 4B | ✓ | LoRA r 128, 300,763 × 1; and its snapshot after the first 48,000 examples |
| diffusion | chandohasam MDLM 120M | ✓ (pre-trained only) | E6 + T1 phase, 300,763 |
| diffusion | chandohasam MDLM 523M | ✓ (pre-trained only) | E6 + T1 phase, 300,763 |
| diffusion | DiffusionGemma 26B-A4B | ✓ | LoRA r 16, 300,762 × 1 (one over-length prompt dropped) |

How each was trained is in its own folder's README. Every fine-tuned row saw the whole pool ([Phase 0](#phase-0))
except the T5Gemma 4B 48k snapshot, which is the data-size point.

**Prompt format.** Each model gets the same content (metre + prompt text) in its own format:
- the instruction-tuned bases (Gemma-4, DiffusionGemma base) get the metrical decoder's instruction prompt
  (`metrical_decoder.prompts.build_messages`: the metre's rules, the prompt as the topic);
- the fine-tuned rows get the format they were trained on (the E6 T1 header; T5Gemma's encoder input with the rules);
- the pre-trained-only bases get the same prompt as their fine-tuned row, so the pair differs only in the weights.

### Cells

| cell | decoding | rows | prompts |
|---|---|---|---|
| free | the model alone: temperature 0.7, top-p 0.9 (DiffusionGemma: its own sampler); seed 42 | 17 | 100 |
| constrained (v1) | `metrical_decoder` masking + backtracking, strict profile, gaṇa + prāsa + yati (DiffusionGemma: the diffusion decoder of `../lora_gemma_diffusion`); seed 42 | 17 | 100 |
| extra | masking only and hybrid | Nandi ×2, MDLM 523M ×2 | 34 |
| v2 | the constrained cell with decoder v2: Layer A (the training corpus's syllable inventory) and Layer B (attested-word preference, weight 2, every step) | 17 | 100 |

**Token budget:** every evaluator takes its per-metre budget from the reference MDLM run: 512 minus that metre's longest
MDLM prompt, 197–376 tokens (`../diffusion_finetuning/runs/grid100_*_test/run.json`), counted in each model's own
tokens. DiffusionGemma uses its own 256-token canvas.

### Measures (`score_grid.py`, the definitions of `../RL/reward.py`)

| measure | definition |
|---|---|
| in metre | the whole poem passes gaṇa, prāsa and yati under the strict engines |
| chandas skill | 1 − the akshara edits needed to reach the metre, relative to unmetered prose (1 = in metre; below 0 = farther than prose) |
| vṛtta lines on pattern | for the 7 common vṛttas only, the share of lines on the gold's most common guru/laghu pattern, the last syllable free |
| real words | the share of 2+-akshara words that are known forms of the training split, or compounds of 2–3 known forms; ఁ stripped on both sides for every model |
| one-akshara words | the share of words of a single akshara |
| copy | the share of the poem's 2+-akshara words found in its prompt |
| recognised | LaBSE ranks the poem's own prompt first among it and 9 other prompts of the same metre, drawn from the 100 and the 183 of the first P1 batch; for 21 prompts whose metre has fewer than 9 others there, prompts of other metres fill up (4 metres have none). A topic signal, not meaning |
| repeating a line | the poem writes some line twice |
| training line | a line identical to a line of the training split |
| gold copy | a run of ≥ 12 aksharas shared with its own gold poem |

**Statistics:**
- **Paired tests** over the 100 prompts, by bootstrap (10,000 resamples; difference, 95% interval, two-sided p): each
  fine-tuned row against its base, each row's constrained cell against its free cell, and each v2 cell against its v1
  cell.
- **In metre** is also tested by McNemar's exact test.
- **A poem with no word of 2+ aksharas** has no real-words value and drops out of that measure's mean and tests. This
  matters only for the T5Gemma bases' free cells (many empty outputs): their real words rest on 81 (270M), 78 (1B) and
  26 (4B) poems.

## How it ran

The cells ran from 2026-10-24 to 2026-10-30 on one GB10, one large job at a time, through the sequential GPU queues
of `../experiments/scripts` (the 14 smaller rows' v2 cells in a second lane beside them). Every cell resumes at the
poem level, and every poem is seeded by its key.

### Phase 0

Before the grid, every fine-tuned model was brought to the whole 300,763-poem pool (decision 6), so that rows differ by
family and size, not by data:
- **Already there:** Nandi, both MDLMs and the T5Gemma 270M.
- **T5Gemma 1B:** full fine-tuning on the whole pool (10-21 → 10-22).
- **T5Gemma 4B:** one LoRA r 128 run on the whole pool, keeping its adapter after the first 48,000 examples as the
  data-size point (decision 9; 10-22 → 10-24).
- **DiffusionGemma:** a fresh LoRA on the whole pool (decision 8), one example per forward pass, 37,595 steps,
  ≈ 107 h (10-24 → 10-28).

## Results

### The table (`results/grid.md`, `results/grid.json`)

In metre %, real words %, recognised %; under the decoder also one-akshara words % and poems repeating a line %.
Constrained = masking + backtracking.

| row | free: in metre / real / recognised | constrained: in metre / real / recognised | one-akshara / repeating | v2: real / recognised / repeating |
|---|---|---|---|---|
| *gold (the source poems)* | *53 / 85.7 / 63* | | *5.0 / 0* | |
| Nandi base | 0 / 95.6 / 43 | 100 / 40.2 / 17 | 18.7 / 33 | 53.3 / 19 / 27 |
| **Nandi FT** | 5 / 80.4 / 65 | 100 / 73.0 / 64 | 6.7 / 0 | 79.1 / 61 / 0 |
| Gemma-4 E4B | 0 / 95.2 / 94 | 100 / 42.0 / 60 | 7.6 / 6 | 50.5 / 59 / 17 |
| Gemma-4 26B-A4B | 0 / 96.9 / 92 | 100 / 53.1 / 63 | 7.8 / 30 | 62.1 / 60 / 29 |
| T5Gemma 270M base | 0 / 84.4 / 33 | 100 / 39.0 / 25 | 11.6 / 30 | 49.9 / 27 / 42 |
| **T5Gemma 270M FT** | 8 / 79.5 / 75 | 100 / 75.3 / 64 | 4.4 / 1 | 82.9 / 66 / 2 |
| T5Gemma 1B base | 0 / 88.8 / 38 | 100 / 39.1 / 31 | 9.9 / 17 | 50.2 / 22 / 26 |
| **T5Gemma 1B FT** | 8 / 82.8 / 75 | 100 / 74.1 / 66 | 5.3 / 1 | 82.3 / 72 / 1 |
| T5Gemma 4B base | 0 / 95.0 / 26 | 100 / 38.0 / 28 | 12.0 / 29 | 45.1 / 25 / 37 |
| **T5Gemma 4B FT** | 7 / 80.6 / 71 | 99 / 72.8 / 63 | 6.2 / 0 | 79.7 / 70 / 0 |
| T5Gemma 4B FT, first 48k | 0 / 77.4 / 65 | 100 / 63.1 / 42 | 7.3 / 0 | 71.6 / 44 / 1 |
| MDLM 120M base | 0 / 98.2 / 44 | 93 / 58.0 / 20 | 20.8 / 11 | 66.0 / 24 / 8 |
| **MDLM 120M FT** | 0 / 91.6 / 83 | 100 / 77.7 / 73 | 12.7 / 1 | 81.6 / 63 / 0 |
| MDLM 523M base | 0 / 98.7 / 45 | 85 / 59.6 / 19 | 17.7 / 13 | 67.0 / 22 / 39 |
| **MDLM 523M FT** | 1 / 89.0 / 80 | 99 / 77.5 / 77 | 10.6 / 2 | **85.4** / 76 / 3 |
| DiffusionGemma base | 0 / 87.2 / 100 | 100 / 33.5 / 64 | 23.0 / 0 | 40.0 / 59 / 0 |
| DiffusionGemma FT | 0 / 79.7 / 90 | 100 / 29.6 / 47 | 11.7 / 12 | 38.6 / 41 / 13 |

Every v2 cell is 100% in metre. `results/grid.md` also has chandas skill, vṛtta lines on the pattern, copy, training
lines, gold copy and lines per poem for every cell.

Free poems of the bases read as fluent prose: high real words, no metre. Some of them copy the prompt heavily:
- **copy:** DiffusionGemma base 29.2%, Gemma-4 E4B 20.3%, Gemma-4 26B 15.8%, against 2.0% for the gold;
- **recognition:** DiffusionGemma base 100%, Gemma-4 92–94%;
- **empty outputs:** the T5Gemma bases often write nothing at all (16, 19 and 66 empty poems for 270M, 1B, 4B).

### What fine-tuning buys (paired, fine-tuned row − its base)

| row | free: real words / recognised | constrained: real words / recognised |
|---|---|---|
| Nandi | −15.2 / +22 (p 0.003) | **+32.8 / +47** |
| T5Gemma 270M | −3.9 (p 0.246) / +42 | **+36.3 / +39** |
| T5Gemma 1B | −6.2 (p 0.036) / +37 | **+35.0 / +35** |
| T5Gemma 4B | −18.0 / +45 | **+34.7 / +35** |
| T5Gemma 4B, first 48k | −20.1 / +39 | +25.1 / +14 (p 0.030) |
| MDLM 120M | −6.6 / +39 | **+19.8 / +53** |
| MDLM 523M | −9.8 / +35 | **+18.0 / +58** |
| DiffusionGemma | −7.5 / −10 | −3.9 (p 0.052) / −17 (p 0.008) |

Points; p < 0.001 unless given.
- **Free poems** lose real words with fine-tuning, because the bases write modern prose and the fine-tuned models
  attempt classical verse. They gain recognition, except DiffusionGemma (−10).
- **Under the decoder** fine-tuning gains on both, except DiffusionGemma.
- The T5Gemma 4B rows' free real-words differences rest on the 26 base poems with any word.
- **In metre** also rises with fine-tuning:
  - free: Nandi, T5Gemma 270M, 1B and 4B gain +5 to +8 points (McNemar p 0.008–0.062);
  - constrained: the MDLMs gain +7 and +14, because their bases run out of budget.

### What the constraint costs (paired, constrained − free)

- **Real words:**
  - the six whole-pool fine-tuned rows other than DiffusionGemma −4.2 (T5Gemma 270M) to −13.9 points (MDLM 120M); the
    48k snapshot −14.3;
  - bases −39.2 (MDLM 523M) to −67.1 (T5Gemma 4B);
  - DiffusionGemma −53.7 (base) and −50.1 (FT).
- **Recognition:** the fine-tuned rows other than DiffusionGemma keep it, with no change at p < 0.05 except MDLM 120M FT
  (−10, p 0.036) and the 48k snapshot (−23). The Nandi, Gemma-4 and MDLM bases and both DiffusionGemma rows lose
  24–43 points. The T5Gemma bases recognise little to begin with (26–38%, counting the empty poems LaBSE scores on a
  blank string: 2, 3 and 8 of them come out recognised) and change by −8 to +2 (not significant).
- **Copy** does not rise under the decoder for any row; it falls significantly for every base and every DiffusionGemma
  row.

### Decoder v2 (paired, v2 − v1 constrained cell)

- **Real words up in all 17 rows:**
  - Nandi base +13.1, T5Gemma 1B base +11.1, T5Gemma 270M base +10.9, DiffusionGemma FT +9.0, Gemma-4 26B +8.9,
    Gemma-4 E4B +8.5, T5Gemma 4B 48k +8.5, T5Gemma 1B FT +8.1, MDLM 120M base +8.0, MDLM 523M FT +7.8, T5Gemma 270M FT
    +7.7, MDLM 523M base +7.4, T5Gemma 4B base +7.1, T5Gemma 4B FT +7.0, DiffusionGemma base +6.5, Nandi FT +6.1,
    MDLM 120M FT +3.9;
  - every p ≤ 0.007.
- **In metre:** MDLM 120M base +7 and MDLM 523M base +15 points, both to 100%: their v2 poems all finish within the
  token budget.
- **Recognition:** no significant change, except MDLM 120M FT −10 (p 0.039).
- **Repeated lines** rise on five base rows: Gemma-4 E4B 6 → 17, T5Gemma 270M base 30 → 42, 1B base 17 → 26, 4B base
  29 → 37, MDLM 523M base 13 → 39. The fine-tuned rows stay at 0–3%, except DiffusionGemma FT (12 → 13).
- **Poem by poem:** `results/grid_v2_samples.md` shows every row's v1 and v2 poems on three fixed prompts.

### By source and by metre type (`results/analysis.md` §4–5)

- **Vemana and the Gemini poems are the easiest prompts; Bhāgavatam and Kūcimañci the hardest:**
  - gold in metre: Gemini 100%, Vemana 80%, Kūcimañci 50%, Bhāgavatam 34%;
  - real words under the decoder, the six whole-pool fine-tuned rows other than DiffusionGemma: Vemana 87–94%,
    Bhāgavatam 63–70%, Kūcimañci 62–76%, Gemini 78–91%;
  - which of Bhāgavatam and Kūcimañci is lowest varies by row (Kūcimañci for Nandi base and FT and T5Gemma 270M FT).
- **The 7 common vṛttas cost real words** under the decoder for every row, and most for the bases:
  - Gemma-4 E4B: 22.9% in them against 58.9% in the other metres;
  - MDLM 523M FT: 70.6% against 83.7%.

### The extra strategies (`results/analysis.md` §6)

Masking only and hybrid ran on four rows, on the 34 prompts of the first P1 batch. On the same 34 prompts:

| row | masking + backtracking | masking only | hybrid |
|---|---|---|---|
| Nandi base: in metre / real words | 100 / 26.5 | 97.1 / 21.0 | 88.2 / 22.5 |
| Nandi FT | 100 / 57.7 | 100 / 57.2 | 100 / 60.6 |
| MDLM 523M base | 79.4 / 46.0 | 79.4 / 42.1 | 91.2 / 42.4 |
| MDLM 523M FT | 97.1 / 62.0 | 94.1 / 56.6 | 100 / 58.9 |

- **On these 34 prompts no strategy wins everywhere.** For MDLM 523M FT masking + backtracking leads on real words
  (62.0% against 56.6% and 58.9%; masking only also doubles its one-akshara words, 25.7% against 13.0%). For Nandi FT
  hybrid leads (60.6% against 57.7%).
- **Hybrid helps the MDLM 523M base finish in metre** (+11.8 points) but costs the Nandi base as much (−11.8).
- n = 34, no tests: read these as indications.

### MAUVE (`../paper/analysis/mauve_vs_gold_cells_human90.md`)

Distribution similarity to the gold poems of the same 90 human-written prompts, ఁ and ఽ stripped.
- **Every whole-pool fine-tuned row** except DiffusionGemma scores 0.93–0.99, free, constrained and v2, against a
  ceiling of 0.980 ± 0.013.
- **Word-shuffled other poems also score 0.982 ± 0.013,** so MAUVE here measures vocabulary and saturates. It cannot
  rank the fine-tuned rows.
- **Where it does separate:** the bases (0.005–0.41, except DiffusionGemma base under the decoder: v1 0.83, v2 0.76),
  the 48k snapshot under the decoder (v1 0.79, v2 0.72) and DiffusionGemma FT under the decoder (0.13).

### Seconds per poem (`results/analysis.md` §7)

| | free | constrained | constrained v2 |
|---|---|---|---|
| T5Gemma 270M / 1B FT | 2.7 / 3.5 | 5.4 / 6.1 | 7.2 / 7.1 |
| Nandi FT | 5.1 | 14.7 | 22.6 |
| Gemma-4 E4B / 26B | 5.4 / 5.2 | 14.8 / 14.8 | 25.1 / 15.0 |
| MDLM 120M / 523M FT | 3.0 / 5.2 | 25.6 / 23.0 | 40.4 / 35.9 |
| DiffusionGemma base / FT | 7.4 / 14.6 | 179.3 / 179.1 | 148.2 / 176.3 |

Means, on the GB10, sometimes beside other jobs.

## Checks

Run on 2026-10-31 (`analyse_grid.py` → `results/analysis.md`; the reproduction with `score_grid.py --out`, below).

- **Reproducible.** `score_grid.py --out <scratch>`, run again from the raw runs (122 s), writes `grid.md`,
  `grid.json`, `grid_poems.jsonl` and `grid_v2_samples.md` byte-identical to the ones here (`cmp`): every measure of
  all 60 cells and all 50 paired tests.
- **The table is the mean of the poems.** Every cell's means in `grid.json` equal the means of its rows in
  `grid_poems.jsonl`.
- **Integrity of every cell:** all 59 cells (34 v1, 8 extra, 17 v2) hold exactly their 100 prompts (34 for the extra
  strategies), each once, at seed 42, with no NUL bytes.
- **Every constrained poem out of metre** (41 of them: 24 in the v1 cells, 17 in the extra cells; none in v2) ended
  at the token budget, unfinished. No finished poem is out of metre.
  - Their metres: layagrāhi 10, mattebha 8, śārdūla 6, sragdhara 5, mahāsragdhara 4, mānini 3, campakamāla 3,
    mattakōkila 1, pañcacāmara 1.
  - 32 of the 41 come from the MDLM bases.
- **Empty outputs:** only in the T5Gemma bases' free cells.

## Caveats

- **One poem per prompt and cell** (seed 42). Rates rest on 100 poems: a free in-metre rate of 7% has a 95% interval
  of about ± 5 points.
- **Recognition is a topic signal,** not a judgement of meaning, and copying inflates it (the bases' free poems).
  Meaning is left to the human evaluation; 56 of the prompts are rated there.
- **Real words measures the vocabulary of the training split,** not grammar or sense. A poem of real words can still
  say nothing (`results/sample_review_20261029.md` reads one prompt's poems closely).
- **The strict profile rejects readings poets use,** hence the gold's 53%. In metre here means "accepted by the strict
  engines".
- **Few P1 prompts were read in a review:** of the grid's 90, 7 were in the user's review sample; the 56 of the second
  batch were checked automatically only. The automatic checks cannot see a changed meaning.
- **The retelling model, Gemma-4 26B, is also a grid row.**
- **Rows differ in passes over the pool:** 1 to 3.5, and the MDLMs also had the E6 tasks.
- **The decoders differ by family where they must:**
  - DiffusionGemma's constrained cells use the settled diffusion decoder;
  - T5Gemma's use an encoder-decoder source;
  - the rest share the autoregressive loop.

## Scripts

| script | purpose | reads | writes |
|---|---|---|---|
| `grid.py` | The rows and cells, one definition for the queues and the scorer: each cell's command, working folder and results path; `--todo core|extra|smoke|new|v2|v2smoke` lists the cells not yet done as queue lines | | (stdout) |
| `prompts.py` | Generates the P1 retellings with Gemma-4 26B, runs the six checks (up to three attempts), writes the review file | the held-out records, the model | `prompts/p1.jsonl`, `p1_attempts.jsonl`, `p1_review.md`, `summary.json` |
| `build_records.py` | Turns the reviewed P1 into the evaluators' records (`meaning` = P1, `meaning_p0` = the original; hand edits from `p1_edits.jsonl`) | `prompts/p1*.jsonl` | `prompts/e6_p1/records` |
| `build_grid100.py` | Draws the 100 prompts (quotas, human-eval pool, metres in proportion), builds their records and the reference runs; `--approve` applies the second-batch P1 | the first P1 batch, the human-eval pool, the second batch | `prompts/grid100/`, `../diffusion_finetuning/runs/grid100_*_test` |
| `run_hf.py` | The Gemma-4 rows: the metrical decoder's instruction prompt with P1 as the topic, through `metrical_decoder` | the records, the model | `runs/grid_gemma4_*`, `results/grid_gemma4_*` |
| `v2.py` | Runs an evaluator (Nandi, Gemma-4, MDLM, DiffusionGemma) with decoder v2's two layers, without changing its file | the evaluator | its run folder |
| `score_grid.py` | Scores every cell on disk the same way; the paired tests; the v2 samples | the run folders, the records | `results/grid.{md,json}`, `grid_poems.jsonl`, `grid_v2_samples.md` |
| `sample_review.py` | One random prompt's poems from every row's free, constrained and v2 cell, beside their metrics, for a close reading | the run folders | `results/sample_review_<seed>.md` |
| `analyse_grid.py` | The checks and breakdowns above | `results/grid_poems.jsonl`, `grid.json`, the raw runs, `selection.json` | `results/analysis.{md,json}` |

## Reproducing

```bash
cd full_grid_experiments
P=../.venv/bin/python
$P grid.py                                  # every cell: done or not, its command
$P grid.py --todo core                      # the cells still to run, as queue lines (name, folder, command)
$P -u score_grid.py                         # → results/ (≈ 2 min; LaBSE on the GPU)
$P -u score_grid.py --out /tmp/grid_check   # the reproduction check: then cmp each file with results/
$P analyse_grid.py                          # → results/analysis.md (≈ 1 s)
```

Running the cells needs the prompts (in `prompts/`; rebuilding them needs the confidential E6 records, through
`prompts.py`, `build_records.py` and `build_grid100.py`) and every model's weights. Each cell resumes at the poem level, and each
poem is seeded by its key.

## Results files

| file | what |
|---|---|
| `results/grid.md`, `grid.json` | the table: every cell's measures, and the 50 paired tests |
| `results/grid_poems.jsonl` | every poem's scores (5,472 rows; no text) |
| `results/grid_v2_samples.md` | every row's v1 and v2 poems on three fixed prompts |
| `results/sample_review_20261029.md` | one random prompt (seed 20261029): the gold and 50 poems (every row's free, constrained and v2 cell except DiffusionGemma base v2, which ran after it), read closely beside their metrics |
| `results/analysis.md`, `analysis.json` | the checks and breakdowns of this README |
| `results/grid_gemma4_*.{md,json}` | the decoder's token-level report of each Gemma-4 cell (Nandi's, T5Gemma's and the MDLMs' are in their folders' `results/`; DiffusionGemma's evaluator writes none) |

## Decisions

The user's design decisions behind the grid, numbered; other folders cite them by number.

| # | date | decision | the user's words, where recorded |
|---|---|---|---|
| 1 | 10-21 | prompts from held-out poems, never the 300k training pool (the fine-tuned models learned it) | |
| 2 | 10-21 | P1 retellings by Gemma-4 26B, with automatic checks and a review sample read by the user | |
| 3 | 10-21 | Gemma-4 fine-tuning outside the grid | |
| 4 | 10-21 | the other two constrained strategies (masking only, hybrid) on a subset of rows: the extra cells | |
| 5 | 10-21 | the grid runs last in the GPU queue | |
| 6 | 10-21 | Phase 0: every fine-tuned model sees the whole pool before the grid | |
| 7 | 10-21 | one prompt form, P1 | |
| 8 | 10-21 | DiffusionGemma: a fresh LoRA on the whole pool | |
| 9 | 10-21 | T5Gemma 4B: one whole-pool run with a 48k snapshot; LoRA rank 128 | |
| 10 | 10-21 | no DiffusionGemma 24k constrained E6 run | |
| 11 | 10-21 | the schedule for an Oct 28 finish: ① a batched-forward speed test for the DiffusionGemma LoRA, ② the September DiffusionGemma rerun after the grid, ③ the extra strategies after Oct 28 | "yes, and yes" |
| 12 | 10-21 | P1 is the one prompt form | |
| 13 | 10-21 | no DiffusionGemma 24k row | |
| 14 | 10-28 | masking + backtracking is the grid's constrained strategy; the extra cells stay as a comparison | "masking + backtracking is the only strategy proved to be good; drop the other two" |
| 15 | 10-28 | no Gemma-4 12B row | |
| 16 | 10-28 | the September DiffusionGemma rerun not in the grid | |
| 17 | 10-28 | no Gemma-4 E2B row | "no comparable model" |
| 18 | 10-28 | one seed (42) in every cell | "we can have a single seed" |
| 19 | 10-28 | the 100-prompt grid: Bhāgavatam 50, Vemana 20, Kūcimañci 20, Gemini 10 | "reduce the distribution … up to 100 prompts" |
| 20 | 10-28 | every grid prompt a human-evaluation pool poem | "make the 100 out of 100 comparable with human annotators" |
| 21 | 10-28 | the 56 second-batch P1 approved in advance (no hand review; the automatic checks stand in) | "approve it please" |
| 22 | 10-28 | decoder v2 (A + B) on every row's constrained cell, all 100 prompts; Layer B built for DiffusionGemma | "once the grid is done, another queue with DAWG v2 (A+B) … samples compared" |
| 23 | 10-29 | v2 in two lanes: the 14 smaller rows beside the grid, Gemma-4 26B and DiffusionGemma in the GPU queue | "since we have a lot of memory can the inferencing be done in parallel?" |
| 24 | 10-29 | the queue ordered for a table the same night | "we are due finishing it today right?" |
| 25 | 10-29 | no DiffusionGemma 48k row: the whole-pool adapter only | "remove it from the ablation study, we will use only the whole pool one" |
