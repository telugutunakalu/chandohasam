# diffusion_finetuning — experiment checklist

Stage 2 of the Telugu masked diffusion model (MDLM).
- **Starting point:** the stage-1 model in [`../diffusion_pretraining/`](../diffusion_pretraining/), `pilot120m`.
- **Goal:** fine-tune it to generate padyams.
- **Metre** is enforced at decoding time by [`../meter_engine/metrical_decoder/`](../meter_engine/metrical_decoder/).

**All tooling for these experiments lives in this folder.**

Status on 2026-10-31: E1–E6 are done. The released models (`mdlm-120m-padyam`, `mdlm-523m-padyam` on
huggingface.co/samvaran/chandohasam) are E6 + the T1 phase; [README.md](README.md) has the recipe, commands and
results.

Status on 2026-10-05, 09:15:
- the tooling is built and tested (§7);
- E1 is done;
- E2, E3 and E4 are running (§8).

## Contents

1. [Where things stand](#1-where-things-stand)
2. [Hypothesis for stage 2](#2-hypothesis-for-stage-2)
3. [Prerequisites](#3-prerequisites)
4. [Experiments](#4-experiments)
5. [Time estimate](#5-time-estimate)
6. [What the results decide](#6-what-the-results-decide)
7. [Tooling](#7-tooling)
8. [Results log](#8-results-log)

## 1. Where things stand

### 1.1 Is there enough data for the pretraining?

Yes, for both continuing the 120M and pretraining a ~500M model. Data is not the limit.
- For the 120M, the limit is its size.
- For a ~500M model, the limit is GPU time.

**The stage-1 corpus.** 9.41B unique training tokens after cleaning, near-duplicate removal and poem decontamination
(`pilot120m_training_report.md` §5.4):

| source | tokens |
|---|---|
| Sangraha | 7.33B |
| IndicCorp | 1.98B |
| Wikipedia | 0.10B |

**Continuing the 120M.**
- `pilot120m` saw 4.98B tokens, about 0.5 passes over Sangraha and IndicCorp. Doubling the run would still be about
  one pass.
- The returns have flattened:
  - the last 1.4B tokens lowered validation NELBO by only 0.037 nats;
  - sample quality stopped improving at step 15k;
  - the sampling study traces the limit to the model's capacity (report §10.6, §11).

**A ~500M model** (`grow-1536x16`, 523M):

| tokens per parameter | tokens needed | passes over 9.41B | Wikipedia passes at 5% weight | GB10 time (estimate) |
|---|---|---|---|---|
| 20 (compute-optimal, Hoffmann et al. 2022) | 10.5B | 1.1 | 5 | ~12 days |
| 41 (what `pilot120m` used) | 21.5B | 2.3 | 10 | ~24 days |
| 80 (the diffusion figure in `experiments/notes/scaling-sufficiency-analysis.md`) | 41.9B | 4.4 | 20 | ~7 weeks |

How much repetition is safe:
- For left-to-right models, up to about 4 passes is nearly as good as fresh data (Muennighoff et al. 2023).
- The scaling note puts the passes a diffusion model tolerates at 313 for 111M and 175 for 320M. Extending that trend
  gives about 130 for 523M; these magnitudes are indicative only.
- Growing from `pilot120m` keeps what that model computes, so the grown model needs fewer tokens than training from
  scratch would.

Notes:
- **GB10 times** assume about 10k tokens/s for 523M. That figure is scaled from the measured 16.7k tokens/s at 320M
  (`experiments/notes/training-throughput-benchmark.md`). The GB10 is shared with the vLLM server.
- **Wikipedia** would be repeated 5–20 times. Lower its weight, or first filter the templated village articles
  (report §11, finding 5).

### 1.2 Inputs

| input | where | note |
|---|---|---|
| the stage-1 model | `models/pilot120m/`, from [huggingface.co/samvaran/chandohasam](https://huggingface.co/samvaran/chandohasam) at revision `5e7ab314` | EMA weights at step 76,000, float32; they load strictly into `mdlm.model.Denoiser`; the tokenizer is byte-identical to `diffusion_pretraining/tokenizer/` (sha256 `200c814d…`) |
| the poems | `../padyarchana_exports/padyarchana_poems_v3.json` (**never committed**) | 382,052 poems; same ids as v2, the file stage 1 was decontaminated against |
| more poems | `../dataset/*.json` | the verse records, with the 2026-09-28 corrections |

Not needed:
- **The stage-1 prose token files.** E1 uses the bhavams of the held-out poems as its prose reference, plus the
  report's own test numbers.
- **`all_poems.txt`.** It was only used for stage-1 decontamination.

## 2. Hypothesis for stage 2

The stage-1 pretraining is enough as a foundation, but not on its own:
- it supplies Telugu that is written correctly;
- the metre engine supplies the form;
- the classical register and putting probability on what the metre allows must come from fine-tuning;
- meaning across a poem depends on model size.

| what a padyam needs | supplied by | evidence |
|---|---|---|
| metre: gaṇa, prāsa, yati | constrained decoding, exactly | with random logits in place of a model, the decoder made 555 of 555 poems complete and in metre (`experiments/runs/2026-09-26_control_vowel`) |
| correctly formed Telugu | stage 1 | `pilot120m` samples are 98–100% Telugu, with under one dangling virama per 1k tokens (report §10.3) |
| real words and modern morphology | stage 1 | 78% real words in free samples, 86% at temperature 0.9 (report §10.3, §10.6) |
| classical register: ఁ, -ంబు, compounds fused by sandhi | **stage 2 only** | documents overlapping any of ~767k poems were removed from stage 1 (report §2.7, §5.2) |
| probability mass on the aksharas the metre allows | **stage 2 only** | see below |
| meaning across the poem | model size, plus conditioning | `pilot120m` never holds a thread; its judge perplexity sits at the level of word-shuffled text (report §10.6) |

**The deciding factor is the model's mass on the aksharas the metre allows.**
- A constrained decoder samples from the model's distribution restricted to the allowed aksharas.
- When most of the model's mass is already there, the constraint changes little.
- When it isn't, each override pushes the sample into the model's unlikely tail.

The three-model comparison (`meter_engine/CONSTRAINED_DECODING_PLAN.md` §16) shows this:

| | free generation | constrained |
|---|---|---|
| real words, Gemma-4 26B-A4B | 41% | 17–21% |
| mass on allowed aksharas, across the three models | | 0.49–0.77 |
| first choices overridden | | 22–47% |
| typical failures | | single-akshara padding, repeated lines |

Those models were given the rules in a prompt and never trained on verse. A model fine-tuned on real padyams learns a
distribution that is itself mostly in metre: the corpora scan as their labelled metre 85.0–99.9% of the time
(`data_sanity_metrics/data_sanity_metrics_report.md`). The constraint should then act as a correction, not a fight.

**Two advantages of this setup over the Gemma runs:**
- **One token is one akshara**, so every token is a metrical unit. Gemma's tokens cut aksharas, which forced the vowel
  and dead-consonant rules.
- **The constraint can act at any position.** The MDLM is trained to fill any position in any order. Prāsa sits at
  the second akshara of every line, and vruttams have a fixed guru/laghu template, so the constraint can be applied to
  every masked position at once. DiffusionGemma's frozen-prefix loop instead overrode the plan it was drafting (§16:
  "a constraint that works with the model's own order of commitment is the open problem").

**Is the poem corpus enough for stage 2?**
- **Size.** It is **26.5M training tokens**: 351,708 poems after duplicates are removed; §3 has the build.
  - That is less than the scaling note's ~70M. With one token per akshara the average poem is ~75 tokens, and
    over a quarter of the poems are two-line ద్విపద.
- **From scratch.** The scaling note said the poems alone would support only about 150M parameters, and that was at
  ~70M tokens. At 26.5M they support less.
- On top of stage 1 it is a fine-tuning regime. Pretraining acts like extra fine-tuning data; that benefit is largest
  when the fine-tuning data is scarce, and it grows with model size (Hernandez et al. 2021, *Scaling Laws for
  Transfer*).

**Predictions:**

| | prediction | tested by |
|---|---|---|
| P1 | `pilot120m` scores held-out poems worse than held-out prose (direction only) | E1 |
| P2 | starting from `pilot120m` reaches a lower verse NELBO than starting from scratch, at an equal number of steps | E2 |
| P3 | under the constraint, the fine-tuned model has mass on allowed aksharas well above 0.77, and real words above 21% (the best Gemma figures) | E3 |
| P4 | at 120M the poems are metrically exact and locally fluent, but loose in meaning | E3, by reading the samples |
| P5 | refrain lines (makuta) are reproduced verbatim; whole poems are not | E4 |

**Expected weak points:**
- **Meaning at 120M.** A vruttam is about 80 aksharas, but verse is dense.
- **Modern words leaking into verse**, because stage 1 learned modern prose.
- **Rare classical vocabulary.** 85% of verse word types occur only once, so real-word counts will miss valid new
  compounds.
- **Little data for conditioning on meaning.** Only ~11.6k poems have a bhavam. A seesa with its bhavam may also
  exceed the 512-token canvas.

## 3. Prerequisites

- [x] **Inputs** (§1.2). The pilot model came from Hugging Face. The poems are v3, provided in `padyarchana_exports/`.
- [x] **Environment.** The repo's `.venv` runs the `mdlm` code unchanged (torch 2.13 cu130).
  - The 120M fine-tunes at **35–37k tokens/s** on the GB10, while E3 sampling runs beside it.
  - On the GB10, CUDA counts page cache as used, so it sees only about MemFree as free. The tools therefore wait for
    `torch.cuda.mem_get_info`, not only MemAvailable (`common.wait_for_memory`).
- [x] **The poem corpus** (`prepare_poems.py`, 25 s; `data/report.md`):

  | | poems | poem tokens | bhavam tokens |
  |---|---|---|---|
  | train | 351,708 | 26,479,938 | — |
  | val | 3,473 | 258,915 | 425,703 |
  | test | 3,523 | 257,833 | 428,659 |

  - **Sources.** 359,858 Padyarchana v3 verse poems (prose — వచనము, గద్యము — skipped) and 11,655 `dataset/` verse
    poems.
  - **Duplicates.** Exact duplicates are removed, ignoring spacing, punctuation and ఁ: 12,804, nearly all Padyarchana
    copies of `dataset/` poems. The `dataset/` copy is kept.
  - **Splits keep shared lines together.** Any line of ≥ 10 Telugu letters shared by two poems puts them in one
    group: 271,840 groups. The strongest links are refrains: విశ్వదాభిరామ వినర వేమ (893 poems), the śataka makutas
    (~100–230 each) and samasyas. val and test take whole groups of ≤ 200 poems, so no line of a held-out poem
    occurs in training.
  - **Copyright flag.** 60% of the Padyarchana poems come from poets marked `copyright_protected`. They are used in
    these internal experiments and flagged per poem in `data/poems_index.jsonl`, so they can be excluded later.

## 4. Experiments

### E1 — Domain gap, zero-shot
- [x] Done (2026-10-05)

| | |
|---|---|
| **Question** | How far is classical verse from what stage 1 learned? |
| **Method** | `pilot120m`, with no fine-tuning, on the test split. Prose reference: the bhavams of the same test poems (same content, modern register) and the report's stage-1 test numbers. Stage 1's protocol (`mdlm.train.evaluate`): fixed canvases, mask rates and masks. Each source is scored in its own call, so the accuracy and per-bin numbers are not pooled. Stage 1 was decontaminated of these poems, so the comparison is clean. |
| **Metrics** | NELBO (nats/token); cross-entropy by mask-rate bin; masked-token accuracy at 15 / 50 / 85% masking |
| **Prediction** | P1 |
| **Time** | tooling ~1 h; GPU 10 s per source |
| **Result** | **P1 holds, and the gap is large** (`results/e1_pilot_test_{poems,bhavam}.json`); see the tables below |

| `pilot120m` on | NELBO | perplexity bound | masked accuracy 15 / 50 / 85% | cross-entropy, t 0–0.1 | cross-entropy, t 0.9–1.0 |
|---|---|---|---|---|---|
| held-out **verse** (503 canvases) | **3.494** | 32.9 | 49.2 / 29.6 / 17.4% | 1.94 | 5.21 |
| the **bhavams** of the same poems (512) | 2.122 | 8.4 | 81.1 / 57.8 / 25.7% | 0.46 | 4.61 |
| stage-1 test prose (report §10.5) | 1.783 | 5.9 | 87.9 / 69.1 / 31.4% | | |

- **Verse costs 1.37 nats per token more** than prose with the same content, and 1.71 more than stage 1's own test
  prose.
- **The gap is largest when almost everything is visible.** At t < 0.1, cross-entropy is 1.94 on verse against 0.46
  on prose, four times higher. With 90%+ masked, it is 5.21 against 4.61.
- **What that says.** Stage 1 does not know verse's local word forms, sandhi and orthography (ఁ, -ంబు, fused
  compounds), even with nearly all the context in view. This is the register gap that stage 2 has to close (§2).

### E2 — What the pretraining buys
- [ ] Done (running)

| | |
|---|---|
| **Question** | How much better does fine-tuning from `pilot120m` do than training the same model on poems alone? |
| **Method** | Two runs on the poem train split (`finetune.py`): (a) `e2_pretrained`, from `pilot120m`; (b) `e2_scratch`, from random initialisation. Everything else is shared: preset `small-768`; 512-token windows; batch 128 × 512; **5 epochs = 2,020 steps (132M tokens)**; AdamW as in stage 1; peak lr 3e-4, 200 warm-up steps, cosine to 10%; data order and masks fixed by the seed. Evaluation every 100 steps (≈ 0.25 epoch), with EMA weights and stage 1's protocol, on 256 val canvases each of verse and of bhavam. The bhavam curve shows how much prose ability the fine-tuning costs. Final checkpoints are scored on the test split (`eval_nelbo.py`). |
| **Metrics** | verse NELBO curve; the gap at equal steps; steps for (b) to reach (a)'s loss; bhavam NELBO; masked accuracy |
| **Prediction** | P2 |
| **Time** | tooling ~1 h; GPU ~65 min per run at 30–37k tokens/s, run one after the other (one run keeps the GPU at 95%) |
| **Result** | Both done. **P2 holds, decisively.** Details in the table below (`results/e2_*_test.json`; curves in `results/e2_pretrained.json` and `results/e2_scratch.json`) |

| | from the pilot | from scratch | gap |
|---|---|---|---|
| verse val NELBO, step 300 | 3.078 | 4.525 | 1.45 |
| verse val NELBO, step 900 | 2.851 | 3.606 | 0.76 |
| verse val NELBO, step 1,500 | 2.749 | 3.294 | 0.55 |
| verse val NELBO, step 2,020 | 2.710 | 3.193 | 0.48 |
| **test verse** | **2.685** | 3.197 | **0.51** |
| test prose (bhavam) | 2.465 | 3.680 | |

- **Less than one pass from the pilot beats five from scratch.** The scratch run never reaches the pilot-start run's
  step-300 loss (3.078).
- **Poems alone do little.** Five passes on poems only end 0.30 better than the untuned pilot (3.494).
- **At this data size the prose pretraining is worth more than the poems.** Details for (a) are below.

| `e2_pretrained`, 5 passes | verse NELBO | bhavam NELBO | masked accuracy 15 / 50 / 85% (pooled) |
|---|---|---|---|
| val, step 0 (the pilot) | 3.487 | 2.099 | |
| val, step 300 / 700 / 1,300 / 2,020 | 3.078 / 2.905 / 2.775 / **2.710** | 2.326 / 2.452 / 2.455 / 2.438 | |
| **test**, final (`results/e2_pretrained_test.json`) | **2.685** (pilot: 3.494) | 2.465 (pilot: 2.122) | 69.7 / 45.9 / 21.9% |

- **Verse.** The loss fell 0.81 nats/token on test (−23%).
- **Prose.** The prose loss rose by 0.34, mostly in the first pass, then flattened.
- **Still improving at the end.** Validation went 2.7160 → 2.7108 → 2.7100 over the last 120 steps, with the learning
  rate at its floor, and no sign of overfitting.
- **The samples are verse.** Unconditional samples at temperature 0.9 (`runs/e2_pretrained/samples.txt`):
  - classical spelling and sandhi (ఁ, -ంబు);
  - కందము shapes, with words running across lines;
  - vruttam-like lines that share a prāsa;
  - each poem closed with `<eos>`;
  - meaning loose, as P4 expected.

**10 passes (decided 2026-10-05).** Because the 5-pass run was still improving, the main stage-2 model is
`e2_pretrained_10ep`:
- a fresh run from the pilot, with the schedule spread over 10 passes (4,040 steps, 265M tokens);
- the full E3 grid runs on it.

**Result (done 14:01).** More passes help the poems and cost a little prose (`results/e2_pretrained_10ep_test.json`):

| test NELBO | pilot | 5 passes | 10 passes |
|---|---|---|---|
| verse | 3.494 | 2.685 | **2.553** |
| prose (bhavam) | 2.122 | 2.465 | 2.484 |

- The gain from 5 to 10 passes (0.13) is about a sixth of the gain from 0 to 5 (0.81). Validation flattened only as the
  learning rate decayed (2.641 at step 2,500, 2.584 at the end), so a larger model's poem stage should use at least 10.
- At step 1,000 the two runs were level (2.827 and 2.828).

The 5-pass run stays as the P2 comparison against `e2_scratch`, which has 5 passes on the same schedule. Its E3 stops
at seed 42.

### E3 — Behaviour under the metre constraint
- [x] Done: the 5-pass model and the pilot at seed 42; the 10-pass model and E5 at all five seeds (2026-10-06, 03:52;
  the five-seed table is under E5)

| | |
|---|---|
| **Question** | Does fine-tuning make the constraint a light correction? |
| **Method** | The §16 grid, read from `experiments/runs/2026-09-26_g26b/run.json`: 37 metres × T1–T3 × seeds 42–70; the free baseline and the three constrained strategies, 2,220 poems; gaṇa, prāsa and yati enforced under the strict profile; the same `DecodeConfig`. It runs through `metrical_decoder`'s own `run_grid` and `evaluate`, and is reported by `metrical_decoder.analysis.report`, so the numbers compare directly with the Gemma rows. Three runs: (a) the main model `e2_pretrained_10ep`, all 5 seeds; (b) the 5-pass `e2_pretrained`, seed 42 (444 poems); (c) a reference with `pilot120m`, seed 42. |
| **Metrics** | the §16 table: in metre; chosen-token logp; first choice overridden; mass on allowed aksharas; real words; single-akshara words (verse: 4.0%); poems repeating a line |
| **Prediction** | P3, P4 |
| **Time** | tooling ~2 h. Compute: 15–115 s per poem with the pilot; masks dominate. Runs as 8 shards for (a) and 2 for (b), beside E2 |
| **Result** | (b) done, the 5-pass model at seed 42 (`results/e3_e2_pretrained.md`, `results/e3_comparison.md`); (a) and (c) running. **P3 holds in part:** real words yes, mass on allowed no overall. The mass depends on the metre; see the tables below |

| 5-pass model, seed 42 | poems | in metre | chosen-token logp | first choice overridden | mass on allowed | real words | 1-akshara words | poems repeating a line |
|---|---|---|---|---|---|---|---|---|
| free | 111 (3 distinct) | 0% | −2.01 | 22% | 0.77 | 70% | 4% | 0% |
| masking only | 111 | 100% | −2.43 | 31% | 0.62 | **24%** | 42% | 9% |
| masking + backtracking | 111 | 100% | −2.72 | 31% | 0.61 | **26%** | 38% | 4% |
| hybrid | 111 | 99%* | −2.42 | 31% | 0.61 | **27%** | 33% | 6% |
| *Gemma-4 26B, constrained (§16)* | 555 each | 100% | −1.68 to −1.94 | 22–28% | 0.71–0.77 | 19–23% | 12–16% | 29–42% |
| *Gemma-4 E4B, constrained (§16)* | 555 each | 100% | −2.18 to −2.34 | 31–35% | 0.63–0.67 | 14–15% | 8–9% | 17–21% |

\* One hybrid poem (స్రగ్ధర, T2) used up its 472-token budget.

- **Real words: more than any Gemma model** under the constraint, 24–27% against at most 23%. Repeated lines are rarer
  too.
- **The mass on allowed aksharas depends on the metre** (constrained modes, mean per poem):

  | metres | mass |
  |---|---|
  | common in the corpus: సీసము 0.85, ఆటవెలది 0.82, కందము 0.79, the రగడలు 0.77–0.78, తేటగీతి 0.77, ద్విపద 0.75 | at or above Gemma-26B's best average |
  | rare vruttams, plus శార్దూల: ఇంద్రవజ్ర 0.50, శాలిని 0.52, ఉపేంద్రవజ్ర, విద్యున్మాల and భుజంగప్రయాతము 0.53, శార్దూల and మానిని 0.54, లలిత 0.55 | well below |

  The model is never told which metre is wanted. The Gemma models had the rules in their prompt. So for a rare
  vruttam the model's prior pulls toward common patterns and the constraint has to fight it. Those fights produce the
  single-akshara filler, 33–42% against 4% in real verse.
- **By position**, the hardest seats are yati (mass 0.38–0.42, overridden 47–55%) and prāsa (0.51–0.52).
- **The free baseline does not depend on the metre** without conditioning. Its 111 poems are 3 distinct poems, one per
  topic.
- **Reading the samples (P4).**
  - Where the model knows the metre, the constrained poem is real Telugu in metre, e.g. the ఆటవెలది
    `అన్న ప్రేమ విడిచి యతివ కలియుగంబు / అనుదినమును కలిగి యాశ్చయమ్మ / …`, and its meaning is loose.
  - Where it doesn't, the constraint forces dead-consonant fragments (`కలత్ కలిగి మ్న్న్యర్`).
- **Implication.** Conditioning on the metre should raise the mass for every metre. That is the compose task of stage
  3, or a metre tag on each poem in stage-2 training.

**Against the pilot (c), seed 42, all 37 metres. This corrects the first reading of P3.** Under the constraint, the 5-pass
model is no better than the pilot, which never saw a poem:

| constrained | real words | mass on allowed | first choice overridden | chosen-token logp | 1-akshara words |
|---|---|---|---|---|---|
| pilot (prose only) | 23–27% | 0.63–0.66 | 27–30% | −1.85 to −2.20 | 17–25% |
| 5-pass poem model | 24–27% | 0.61–0.62 | 31% | −2.42 to −2.72 | 33–42% |

| mass on allowed, mean per poem | pilot | 5-pass |
|---|---|---|
| common metres: సీసము, ఆటవెలది, కందము, తేటగీతి, ద్విపద, ఉత్పలమాల, చంపకమాల | 0.70 | **0.75** |
| rare vruttams, plus శార్దూల | **0.61** | 0.53 |

- **The real-words lead over Gemma comes from our setup** (the akshara tokenizer and the model's Telugu), not from the
  poem pretraining. The prose pilot has it too.
- **Poem pretraining shifted the mass by metre.** It moved toward the metres the corpus is full of and away from the rare
  vruttams; it also raised single-akshara filler.
- **Free generation is where poem pretraining clearly shows.**
  - 70% real words in verse register, against the pilot's 26% in prose;
  - poems that end with `<eos>` after ~35 tokens, where the pilot writes prose up to the budget.
- **So P3 does not hold at 5 passes.** The constraint is not yet a light correction. E5, naming the metre, is the direct
  test of the explanation; the 10-pass model shows whether more passes change it.

How the MDLM is decoded (`constrained_sample.py`):
- **Order of commitment: left to right**, as for the autoregressive rows. The canvas holds the committed tokens, then
  `<mask>` up to 512 positions. The model's prediction at the first masked position is the next-token distribution,
  a proper conditional of the prefix for a masked model. There is one forward pass per token and no cache.
  - Any-order commitment is the natural next step. Vruttams have a fixed guru/laghu template per position, so every
    masked position could be constrained at once.
  - It is not part of E3: E3 compares against the left-to-right Gemma rows.
- **The vocabulary slice** is the 4,110 aksharas seen ≥ 10 times in the poem train split, plus space and newline. They
  cover 99.94% of poem tokens.
  - Masks over all 45,262 Telugu tokens took 0.4–4.4 s each; over the 10,535 aksharas that occur, ~0.5 s on 4 workers.
  - Tokens outside the slice count as not allowed. The whole-vocabulary statistics (logp, rank, entropy, mass on
    allowed tokens) use the full distribution.
- **The topic** is a prose document before the poem: `<bos> topic <eos> <bos> poem`. The model follows no
  instructions, and without a topic the three topics would repeat each seed's poem.
- **Budget.** At most 472 generated tokens, the 512-token canvas less the prefix. That is at least twice any poem, since
  one token is one akshara.
- **Weights** are bf16 for inference.

### E4 — Memorisation
- [ ] Done

| | |
|---|---|
| **Question** | Does the fine-tuned model copy poems from its training data? |
| **Method** | `memorisation.py`, for each poem of an E3 run, against the poem train split (20.6M aksharas; spaces and line breaks ignored): (1) the longest run of aksharas shared with any one training poem, at N = 6, 8, 12, 16, 24, 32 (64-bit rolling hashes; windows never cross a poem); (2) the share of its lines found as a whole line in training, split into **refrain** lines (found in ≥ 5 training poems: makuta, samasya) and **ordinary** lines. |
| **Metrics** | share of poems whose longest shared run reaches N; refrain-line share; ordinary-line share; poems copying an ordinary line |
| **Prediction** | P5 |
| **Time** | tooling ~1 h; ~3 min per run (3.9 GB peak) |
| **Result** | the 5-pass model at seed 42 (`results/e3_e2_pretrained_memorisation.md`): **no copying**. Half of P5 does not hold: refrain lines are not reproduced. Details below |

- **No copying.** No poem shares a run of ≥ 12 aksharas with a training poem. No line is copied verbatim, refrain or
  ordinary.
- **Short shared runs are common phrases:**
  - runs of ≥ 6 aksharas: 67% of the free poems and 30–32% of the constrained ones;
  - runs of ≥ 8: at most 1.8%.
- **No makuta reappears.** The model is not conditioned on a śataka, so none is reproduced.

### E5 — Telling the model the metre (a metre tag in stage 2)
- [x] Done: seed 42 at 16:46, all five seeds at 03:52 (2026-10-06)

| | |
|---|---|
| **Question** | E3 on the 5-pass model shows mass on allowed aksharas of 0.75–0.85 for common metres but 0.50–0.55 for rare vruttams. Does naming the metre before each poem, in training and at decoding, close that gap? |
| **Method** | `prepare_tags.py` writes `data/tokens/poems_tagged/`: every poem whose metre is in the catalogue is preceded by `<bos> name <eos>` (313,031 of 351,708 train poems, 89%; 35 of the 37 catalogue metres; 28.3M tokens). The untagged rest are Unknown, గీతము, ఉత్కళిక and శ్లోకము. Train `e5_tagged_10ep` from the pilot with `--source poems_tagged --steps 4040`, the same compute as the untagged 10-pass run (4,041 steps, from rounding 10 passes). Run E3 with `--metre-tag`: the metre's name goes before the poem, after the topic. Compare with `e3_e2_pretrained_10ep`. |
| **Metrics** | the E3 table; mass on allowed aksharas by metre (rare vruttams against common metres); single-akshara words; test NELBO on untagged verse, the cost of tagging for plain verse modelling |
| **Prediction** | P6: with the tag, the rare vruttams' mass rises toward the common metres' (≥ 0.75), and single-akshara filler falls |
| **Time** | tooling ~0.5 h; GPU ~2.1 h; E3 ~2 h |
| **Result** | **P6 holds in part.** The tag cuts the filler by a third and lifts the common metres, but the rare vruttams barely move. `results/e5_tagged_10ep_test.json`, `results/e3_comparison.md`, `results/e3_*_10ep_memorisation.md` |

All five seeds, 555 poems per strategy; masking only / backtracking / hybrid (seed 42 alone gave the same picture):

| | 10 passes, untagged | E5, tagged | Gemma-4 26B-A4B |
|---|---|---|---|
| single-akshara words % (verse 4–5%) | 39.7 / 36.5 / 30.9 | **24.6 / 23.0 / 20.4** | 16.1 / 12.0 / 14.1 |
| real words % (held-out real poems 42.8%) | 26.5 / 29.5 / 29.8 | **35.5 / 37.8 / 37.0** | 18.6 / 23.0 / 18.7 |
| mass on allowed | 0.63 / 0.61 / 0.63 | **0.67 / 0.66 / 0.67** | 0.77 / 0.71 / 0.76 |
| first choice overridden % | 30.3 / 31.8 / 30.1 | **26.0 / 27.2 / 25.6** | 21.9 / 27.8 / 22.8 |
| poems repeating a line % | 13.0 / 8.6 / 7.4 | 17.5 / 9.9 / 11.0 | 41.6 / 30.3 / 28.5 |
| in meter % | 100 / 100 / 99.6 | 99.6 / 99.3 / 100 | 100 each |
| free generation: in meter; mass on allowed; first choice overridden | 0%; 0.77; 18.3% | **2.5%; 0.89; 7.6%** | 0%; 0.75; 24.0% |

| mass on allowed, constrained, mean per poem | 10 passes | E5 |
|---|---|---|
| common metres (the 7 of E3; 315 poems) | 0.743 | **0.870** |
| rare vruttams, plus శార్దూల (the 8 of E3; 360 poems) | 0.526 | 0.566 |

- **The prediction's second half holds:** filler falls by about a third in every strategy (by half at seed 42), and
  real words rise by 7–9 points, towards the held-out real poems' 42.8%.
- **Its first half fails:** the rare vruttams rise only from 0.53 to 0.57, far from 0.75, and the gap to the common
  metres widens from 0.22 to 0.30. A name cannot teach a metre the model has seen in few poems.
- **Free generation follows the metre.** 89% of the mass is on allowed aksharas and the first choice is allowed 92%
  of the time; 14 of 555 unconstrained poems (2.5%) are fully in metre (untagged models and Gemma: 0). The free poems
  are full length (136 tokens against 87).
- **Costs.** More poems repeat a line. Untagged verse is modelled worse (test NELBO 2.638 against the 10-pass model's
  2.553); tagged verse scores 2.387.
- **Memorisation (E4):** none under the constraint. In free generation 2 of 555 tagged poems (0.4%) copy an ordinary
  training line, with a shared run of ≥ 12 aksharas; the untagged model copies none. Named metres pull free text
  closer to the corpus.
- **Implication for the 523M's poem stage:** train with tags, and keep E4 on every free-generation run.

### E5b — Metre-tagged, catalogue-metre poems only
- [x] Trained (2026-10-09 18:53 – 2026-10-11 ~19:00, throttled beside the 523M pretraining); E3 not run (see Result)

| | |
|---|---|
| **Question** | Does training only on poems in a catalogue metre (dropping Unknown, గీతము, ఉత్కళిక, శ్లోకము and the other untagged poems) make the tagged model fit the metre better under the constraint than E5, which also trained on the untagged 11%? |
| **Method** | `prepare_metrical.py` writes `data/tokens/poems_metrical/`: the train split keeps the 313,031 tagged poems of E5 (25.3M tokens; 38,677 dropped, 33,304 of them Unknown). val and test are E5's own files (hard links), so every number compares with E5. Train `e5b_metrical_10ep` from the pilot with `--source poems_metrical --steps 4040` (E5's compute: 10.5 passes over the smaller set), with `--duty 0.1`: it sleeps 9× each step's busy time, to share the GPU with the 523M run. Then E3 with `--metre-tag` and E4, against `e3_e5_tagged_10ep`. |
| **Metrics** | the E3 table (filler, real words, mass on allowed, overrides, repeated lines, free in-metre rate); mass by metre (rare vruttams against common metres); val NELBO on tagged and untagged verse |
| **Prediction** | small gains at most: the dropped poems are 11% of the train split and add no data for the rare vruttams (most under 500 poems each) |
| **Time** | ~2.2 h of GPU at full speed. At duty 0.1 beside the 523M (measured 2026-10-09/10): 86 steps/h, ~1,690 tokens/s, so ~47 h in all. The 523M ran 5.1% slower (12,693 → 12,041 tokens/s, means over evaluator-free windows), ~2.5 h of delay over the 47 h; pausing it would have cost ~2.3 h. Side effect: page cache from the extra job left CUDA 15.5 GB free (83.5 GB available), and the 523M's evaluator waited 7 h until the cache was evicted (`mdlm/checkpoint_eval.py` now evicts by itself) |
| **Result** | **No gain; worse on likelihood.** Test NELBO (`results/e5b_metrical_10ep_test.json` against `e5_tagged_10ep_test.json`): tagged verse 2.414 against E5's 2.387 (+0.027); untagged verse 2.743 against 2.638 (+0.105); bhāvam 2.813 against 2.488 (+0.325, twice E5's loss of prose ability). The dropped poems were 74% Śaṅkarābharaṇam online poems and 95% by copyright-protected (modern) poets, against 28% and 57% of the kept ones: "catalogue metres only" also removed most of the modern-register verse, which kept the model closer to modern Telugu. Implication: keep the whole corpus for E6, whose condition (the bhāvam) is modern prose. |

### E6 — Task training: metre + meaning → poem, on both sizes
- [x] CPU preparation done (2026-10-13)
- [x] 120M done 2026-10-14 15:31 (beside the 523M pretraining, uncapped; `run_e6.sh` as the user service `e6-120m`). Stage-2 sweep, 1 epoch each, val T1 NELBO: 3e-5 2.588, 6e-5 2.510, **1e-4 2.443** (best, at the top of the range). Final, 2.5 epochs at 1e-4: **T1 2.253 against T0 2.803**: given the meaning, the poem costs 0.55 nats less, so the model uses it (untrained: T1 4.05 above T0 3.79); T2 2.051. Val E6 evaluation (`results/e6_120m_val.md`; 11 metres, 114 poems per strategy): constrained 100% in metre; single-akshara words 12–16% (E5 20–25%, E2 31–40%, verse 4–5%); mass on allowed 0.69–0.76 (E5 0.66–0.67); first choice overridden 21–27%; repeated lines 0% (E5 10–17%). Words copied verbatim from the bhāvam: 2.7–3.6% (real poems 2.5%): the poems paraphrase the meaning in classical forms (ధర్మజు అంతటివాడు → ధర్మజునంతవాఁడు) with some non-words left.
- [x] 523M done 2026-10-18 10:23 (E6 evaluation 10:55, T1-phase evaluation 11:32). Sweep, val T1 NELBO: 3e-5 2.126, 6e-5 2.085, **1e-4 2.069** (best, as for the 120M). Final, 2.5 epochs at 1e-4: **T1 1.937 against T0 2.570** (0.63 nats; 120M 0.55), T2 1.788. T1 phase (1 epoch, 3e-5): T1 1.934, T0 2.567, T2 1.799, so almost no gain at this size. Val evaluation of the T1 model (`results/e6_523m_t1_val.md`): constrained 100% in metre; backtracking logp −1.52 (120M −2.07), overridden 12% (19%), valid mass 0.855 (0.786), real words 56% (57%); free 0% in metre. Memorisation: none (no run ≥ 12 aksharas, no verbatim line). Test (`results/e6_*_t1_test.md`, 183 poems in 25 metres) agrees. The queue as planned: 523M, queued 2026-10-16 (`deploy/e6_queue.sh`, user service `e6-queue`; starts when the pretraining logs "(end of run)"), **with exactly the 120M's recipe** (the user's decision, 07:30): `DEFAULT_MIX`, stage 1 from the pretraining's final EMA, sweep 3e-5 / 6e-5 / 1e-4, the best rate for 2.5 epochs, val evaluation. A poem-heavy recipe (`POEM_HEAVY_MIX`, 3 epochs) was queued at 07:14 and withdrawn before it started; task-specific training comes after E6.
- [x] Task-specific test on the 120M (`deploy/e6_t1_test.sh`, 2026-10-16): 1 epoch of T1 only from `runs/e6-s2-120m` (2,350 steps, lr 3e-5). Val T1 NELBO 2.2525 → **2.2301**; T0 unchanged (2.803); T2 2.051 → 2.065. Evaluation (`results/e6_120m_t1_val.md` against `e6_120m_val.md`): backtracking logp −2.22 → −2.07, real words 54 → 57%, mass 0.759 → 0.786, overrides 21 → 19%; masking-only filler 16 → 19%, hybrid about equal (114 poems per strategy: differences of a few points are noise). Memorisation unchanged (none); words copied from the bhāvam 2.7–3.6% → 2.1–2.9%. A small, cheap gain: added to the 523M queue (the user's go, 2026-10-16 22:00) as `run_e6_t1.sh 523m` (0.3x the chosen stage-2 rate), its training overlapped with the E6 evaluation to save ~1.7 h.
- Memorisation of the 120M E6 against its own train split (`memorisation.py --train-records data/e6/records/train.jsonl`; `results/e6_120m_val_memorisation.md`): no poem shares a run of ≥ 12 aksharas with a training poem, no verbatim line; runs ≥ 6: 49–57% of constrained poems (common phrases), ≥ 8: 1.8–3.5%.

**Decisions (2026-10-13, the user's).**
- **Split.** The repo's own corpora, `../dataset/{bhagavatam,vemana,kuchimanchi_timmakavi,chandassu}.json`, are held
  out whole; every Padyarchana v3 poem trains except the ones inside them. val = Bhagavatam skandhas 1, 2, 7 (edition
  bhāvams; every development decision); test = all other `dataset/` verse poems.
- **Tasks.** All six of PLAN §5.1, weighted toward writing poems: T1 (metre + meaning → poem) 50%, T5 (repair a poem)
  15%, T0 (metre → poem) 10%, T2 (poem → meaning) 15%, T3 and T4 (glosses) 5% each. Poem writing is 75% of canvases
  (PLAN's mix: 65%; kept as `ft.canvas.PLAN_MIX`).
- **Starting points.** The 120M pilot and the 523M pretraining's final snapshot. Not E2/E5: they trained on most of
  the `dataset/` poems, which are now the test set.
- **Path.** PLAN's stage 1 (poem + meaning documents, 15% prose replay), then stage 2 (the six tasks), for each size.

**Data** (`ft.build_data --out data/e6`; `data/e6/DATA_CARD.md`):

| split | poems | note |
|---|---|---|
| train | 365,680 | Padyarchana v3: 247,894 classical, 118,229 modern (Śaṅkarābharaṇam); 364,262 with a meaning (153,639 edition, 210,623 Gemini) |
| dropped | 16,372 | 14,634 with the text of a `dataset/` record (prose records included), 1,295 near-duplicates (≥ 50% 8-gram containment either way), 443 other records of the held-out works (prose formulas, empty records) |
| val | 906 | Bhagavatam skandhas 1, 2, 7; all with edition bhāvams |
| test | 10,749 | Bhagavatam 5,411 (edition bhāvams), Vemana 1,164, Kuchimanchi Timmakavi 1,642, chandassu 2,532 (Gemini bhāvams) |

Stage 1 documents: 85.5M tokens. Stage 2 pools: T1/T5 300,763 poems, T0 301,163, T2 363,820, T3/T4 364,365;
~4,700 steps per epoch at 128 canvases (~33k tokens per step, ~155M tokens per epoch).

**Checks done (CPU):**
- `ft.constraints --data-dir data/e6`: teacher-forced acceptance of the gold poems 99.7% (val), 98.4% (test); yati
  seats in maitri 96.4% / 89.6% (relaxed / hypothesis).
- `ft.lexicon --data-dir data/e6`: 2.99M word forms from the training split only (2.75M poem, 339k prose).
- `ft.leakage --data-dir data/e6` (20-token windows against the pretraining corpus): 477 of 23,308 held-out texts hit. **112 poems** — 111 chandassu, 105 of them the Venugopāla śatakam (in Sangraha; stage 1's decontamination missed it), and 1 Bhagavatam — are excluded from every evaluation (`ft.evaluate` and `constrained_sample.py --e6-split` read `leakage.json`). **375 meanings** (353 Bhagavatam edition commentaries on web pages, 16 chandassu, 6 Kuchimanchi) stay usable as prompts (the model read the prose, not the poem) but are left out of poem → meaning scoring, the rule of PLAN §3.2. (Run with an empty `pyarrow` stand-in on PYTHONPATH: `data_prep.sources` imports it at the top, `.venv` lacks it.)
- Tests: `ft/` 49 passed, `diffusion_pretraining` 36 passed (pytest from a scratch folder; not in `.venv`).
- GPU smoke runs (a few steps each, deleted): stage 1 from the pilot, stage 2 from it, stage 2 from a 523M snapshot,
  and the E6 evaluation below. First reading: before any poem training, T1 val NELBO is 3.70 for the 523M (step 112k)
  against 4.05 for the 120M.

**Code changed for E6:** `ft/build_data.py` (v3 reader; all four `dataset/` corpora held out; exact-text, near-
duplicate and held-out-work filters; report), `ft/canvas.py` (the poem-weighted mix), `ft/constraints.py` (skips a
missing split), `ft/train.py` (TensorBoard optional), `constrained_sample.py` (`--e6-split`: held-out poems as
prompts).

**Evaluation.** `constrained_sample.py --e6-split val|test`: for each grid metre, up to 15 held-out poems (fixed
sample), each prompted with its own metre and bhāvam in the T1 layout, decoded by `metrical_decoder` exactly as E3
(the free baseline and the three constrained strategies, strict profile), keyed by poem id. val covers 12 metres,
test 26. Meaning faithfulness: `ft.judge` (LaBSE; AUC 0.88 on 60 val items, PLAN §14).

**GPU phase** (estimates from measured speeds: 120M ~35k tokens/s, 523M ~12.5k tokens/s, GPU otherwise idle):

| step | 120M | 523M |
|---|---|---|
| stage 1: 3 passes of poem + meaning documents + 15% replay (~300M tokens), lr 1e-4 | ~2.4 h | ~6.7 h |
| stage 2: learning-rate sweep (3e-5 / 6e-5 / 1e-4), 1 epoch each | ~3.7 h | ~10 h (or two rates, ~6.8 h) |
| stage 2: 2.5 epochs at the chosen rate | ~3.1 h | ~8.6 h |
| E6 evaluation on val (12 metres × 15 poems × 4 modes) | ~2 h, masks on the CPU | ~3 h |

```bash
P="../.venv/bin/python -m"
# 120M
$P ft.train --stage 1 --run e6-s1-120m --data-dir data/e6 --init-from ../diffusion_pretraining/runs/pilot120m_hf/ema_step_0076000.pt
$P ft.train --stage 2 --run e6-s2-120m-lr6e-5 --data-dir data/e6 --init-from runs/e6-s1-120m --lr 6e-5 --epochs 1   # and 3e-5, 1e-4
$P ft.train --stage 2 --run e6-s2-120m --data-dir data/e6 --init-from runs/e6-s1-120m --lr <best> --epochs 2.5
../.venv/bin/python constrained_sample.py --model runs/e6-s2-120m --name e6_120m_val --e6-split val --shards 4 --mask-workers 2
# 523M: the same with --init-from ../diffusion_pretraining/runs/stage1-523m/snapshots/ema_step_0160000.pt
```


## 5. Time estimate

The estimate of 2026-10-05 morning was ~3–4 days of engineering and 10–13 h of compute. In practice:

| item | engineering | compute | done |
|---|---|---|---|
| prerequisites (inputs, environment, poem corpus) | ~1 h | 25 s corpus build | 08:29 |
| E1 domain gap | ~0.5 h | 10 s per source | 08:30 |
| E2 pretrained vs scratch, 5 passes | ~0.5 h | ~65–75 min per run, one after the other | (a) 09:46; (b) ~11:00 (estimate) |
| E2, the 10-pass main model | — | ~2.1 h, after E2(b) | ~13:35 (estimate) |
| E5, the metre-tagged 10-pass model | ~0.5 h | ~2.1 h, after the 10-pass run; then E3 ~2 h | training ~15:45; E3 ~18:00 (estimates) |
| E3 under the constraint | ~2 h | 15–115 s per poem with the pilot; 8 shards beside E2 | 5-pass seed 42 ~10:30; pilot ~11:15; 10-pass all seeds ~15:30–16:00 (estimates) |
| E4 memorisation | ~0.5 h | ~3 min | after each E3 run |

Engineering was fast because the existing code was reused unchanged:
- `mdlm` for model, objective, windows, evaluation and sampler;
- `metrical_decoder` for the enforcer, strategies, grid, evaluation and analysis.

The poem corpus is smaller than assumed (26.5M tokens, not ~70M), which made E2 three times cheaper.

## 6. What the results decide

- **The fine-tuned 120M fits the metre well (P3 holds) but its poems are loose in meaning.** Grow to 523M:
  - continue pretraining, ~12 days for 10.5B tokens on the GB10 (§1.1);
  - then repeat E2 and E3.
- **The fine-tuned model fits the metre poorly (P3 fails).** The problem is the stage-2 recipe, not model size. Options:
  - more epochs on the poems;
  - training conditioned on the metre, e.g. the metre name or template on the canvas;
  - a different mix of masking rates.
- **Pretraining gives little advantage over scratch (P2 fails).** Reconsider stage 1's register before spending GPU
  time on a 523M stage 1. Options include adding classical prose that does not overlap the poems.

## 7. Tooling

Everything is in this folder. It reuses `../diffusion_pretraining/` (`mdlm`, the tokenizer) and
`../meter_engine/metrical_decoder/` without modifying them. Run each tool from this folder with the repo's venv,
`../.venv/bin/python <tool>`.

| file | purpose | for | status |
|---|---|---|---|
| `common.py` | paths, loaders (the pilot from `models/`, a fine-tuning checkpoint), memory checks for the shared GB10 | all | built |
| `prepare_poems.py` | poem corpora → `data/tokens/{poems,bhavam}/{train,val,test}.bin`, `data/poems_index.jsonl`, `data/report.md` | prerequisites | built, run |
| `eval_nelbo.py` | fixed-mask NELBO, cross-entropy by mask rate and masked accuracy, per source → `results/<name>.json` | E1, E2 | built, run |
| `finetune.py` | fine-tuning from `pilot120m` or from scratch; resumes; evaluation curve → `results/<run>.json` | E2 | built, running |
| `constrained_sample.py` | our MDLM as a `metrical_decoder` logits source; the §16 grid, sharded → `runs/<name>/`, `results/<name>.md/.json` | E3 | built, running |
| `memorisation.py` | longest shared akshara run and verbatim lines against the train split → `results/<run>_memorisation.md/.json` | E4 | built, tested |
| `compare_e3.py` | ours beside the §16 Gemma runs, every row from `metrical_decoder.analysis.collect` → `results/e3_comparison.md/.json` | E3 (P3) | built; its Gemma rows reproduce §16 |
| `prepare_tags.py` | the metre-tagged copy of the corpus → `data/tokens/poems_tagged/`, `data/tags.json` (mapping, coverage) | E5 | built, run |

Options added for E5:
- `finetune.py --source poems_tagged --steps N` (defaults unchanged);
- `constrained_sample.py --metre-tag`.

Commands:

```bash
../.venv/bin/python prepare_poems.py
../.venv/bin/python eval_nelbo.py --model pilot --name e1_pilot_test_poems --sources poems
../.venv/bin/python eval_nelbo.py --model pilot --name e1_pilot_test_bhavam --sources bhavam
../.venv/bin/python finetune.py --run e2_pretrained --init pilot
../.venv/bin/python finetune.py --run e2_scratch --init scratch
../.venv/bin/python eval_nelbo.py --model runs/e2_pretrained/final.pt --name e2_pretrained_test
../.venv/bin/python constrained_sample.py --model runs/e2_pretrained/final.pt --name e3_e2_pretrained --shards 8 --mask-workers 2
../.venv/bin/python constrained_sample.py --model pilot --name e3_pilot_seed42 --seeds 42 --shards 2 --mask-workers 7
../.venv/bin/python memorisation.py --run e3_e2_pretrained
../.venv/bin/python compare_e3.py --ours e3_e2_pretrained e3_pilot_seed42
```

**Real words, as defined in §16:** words of ≥ 2 aksharas found in `dataset/*.json`, as a share of all words.
- `metrical_decoder.analysis`'s own "lexical" rate counts single-akshara filler as words. For DiffusionGemma that
  gives 29–33%, against §16's 9–10%.
- `compare_e3.py` therefore computes the §16 definition itself. It reproduces §16 within 2 points: the lexicon changed
  with the dataset fixes of 2026-09-28.

What is and isn't committed:
- **Not committed:** `models/`, `data/` and `runs/`. They hold weights, the poem text and generated poems, and come
  from `padyarchana_exports/`, which is never committed.
- **`results/`** holds numbers only.

## 8. Results log

Dated entries, newest last.

- **2026-10-05, morning.**
  - Analysis only: data sufficiency (§1) and hypothesis (§2).
- **2026-10-05, 08:20–09:15.**
  - **Inputs:** the pilot model from Hugging Face; the v3 poems.
  - **Corpus built:** 26.5M training tokens; group splits (§3).
  - **Tooling built and tested** (§7).
  - **E1 done:** P1 holds; verse costs 1.37 nats/token more than prose with the same content.
  - **E2(a) started.** Then the vLLM server was stopped, which freed ~65 GB. With it E3 runs sharded beside E2: E3 is
    CPU-bound (masks), while E2 alone keeps the GPU at 95%, so the two E2 runs stay one after the other.
- **2026-10-05, 09:46.**
  - **E2(a), 5 passes, done:** test verse NELBO 3.494 → 2.685; prose 2.122 → 2.465.
  - **The free samples are verse.**
  - **Next run:** validation was still improving, so a 10-pass run follows E2(b) as the main stage-2 model.
- **2026-10-05, 10:51.**
  - **E3 and E4 on the 5-pass model (seed 42).** Real words 24–27%, more than any Gemma model.
  - **Mass on allowed aksharas** is 0.75–0.85 for common metres but 0.50–0.55 for rare vruttams.
  - **No memorisation.**
  - **P2 holds at every step.**
  - **Decision:** add E5, a metre-tagged 10-pass run after the untagged one.
- **2026-10-05, 14:43.**
  - **10 passes done:** test verse NELBO 2.553 (5 passes: 2.685); prose 2.484.
  - **E3 at seed 42:** real words up (25.8–32.7%), mass on allowed back to the pilot's level (0.61–0.64), single-akshara
    filler unchanged (30–44%). No memorisation.
  - **The filler, traced** (10 passes, masking only): half of the one-syllable words are a bare akshara, half an akshara
    plus a word-final dead consonant (యర్, నడ్, మన్), which makes the syllable heavy. Only ~11% of the bare ones end
    because the constraint blocked a continuation; mostly the model breaks the word itself. Not the tokenizer: free
    generation has 3.8% (verse 4–5%), and Gemma, writing Telugu 82–86% one akshara per token, also gets 8–29% under the
    constraint.
  - **Speed:** 4 mask workers per shard instead of 2 cut the grid from 62 to 42 minutes.
- **2026-10-05, 16:46.**
  - **E5 at seed 42:** P6 holds in part (above). The tag halves the filler; the rare vruttams barely move.
- **2026-10-05, 17:15.**
  - **The other seeds' grids filled the swap** next to the 523M run: 8 shards × 4 workers, ~1.8 GB per worker. Stopped
    and resumed at 4 shards × 2 workers (`constrained_sample.py --shards 4 --mask-workers 2`); the poems are unchanged,
    since rows already written are skipped and masks are exact.
- **2026-10-06, 03:52.**
  - **Both grids complete,** five seeds each; merged files hold 2,220 unique poems. Changing 8 shards to 4 moved metres
    between shard folders, so ~349 poems were decoded twice; the merge reads only the current shards, and decoding is
    deterministic, so nothing is double-counted. (Stale `shard_4`–`shard_7` folders remain: read the merged files.)
  - **E5 over five seeds:** P6 holds in part, as at seed 42 (above). E4: no copying under the constraint; 2 of 555
    free tagged poems copy an ordinary line.
