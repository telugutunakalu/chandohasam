# lora_gemma_diffusion

LoRA fine-tuning of **DiffusionGemma 26B-A4B**, Google's block-diffusion mixture-of-experts model, to write a Telugu
*padyam* from a metre and a bhāvam, and its evaluation beside the project's other models.

**Why this model:**
- The RL trials on the 120M and 150M models (`../RL`) taught neither metre by default nor meaning.
- The likeliest route to meaningful poems was a large pretrained model that already knows Telugu, fine-tuned on the
  project's poems.
- The user required a diffusion model (2026-10-19).

The design and the step log are in [PLAN.md](PLAN.md). Status 2026-10-31: three adapters trained and evaluated. The
final one is staged for the Hugging Face release as `diffusiongemma-26b-padyam-lora` but not yet uploaded; its
inference script still awaits a GPU check (`../hf_release/README.md`).

| adapter | training data | steps × 8 examples | file (here) | evaluated |
|---|---|---|---|---|
| none (the base model) | | | | E6 val free and constrained; the grid |
| "24k" | the first half of the 48k run | 3,000 | `runs/lora-48k/lora_step_3000.pt` | E6 val free |
| "48k" | 48,000 poems drawn with E6's metre weights | 6,000 | `runs/lora-48k/lora.pt` | E6 val free and constrained |
| **whole pool** | all 300,762 pool poems, natural metre mix, one pass | 37,595 | `runs/lora-full/lora.pt` | E6 val free; the grid (free, constrained, v2); the release |

Each adapter is LoRA r 16, α 32 on q, k, v, o of the language layers: 115 projections, 11,489,280 parameters.

## What is where

Only code, documentation and results are in git.

| what | where | in git |
|---|---|---|
| code | the scripts below | yes |
| results | `results/` (numbers only, no poem text) | yes |
| training data | `data/`: the examples in Gemma's tokens, built from the E6 records of `../diffusion_finetuning` (the confidential crawled corpus) | no (`.gitignore`) |
| base model | `nvidia/diffusiongemma-26B-A4B-it-NVFP4` in the Hugging Face cache (18 GB) | no |
| adapters, generated poems, logs | `runs/` (0.9 GB) | no (`.gitignore`) |

## Use the adapter

The release folder (`../hf_release/src/diffusiongemma-26b-padyam-lora/`) holds a self-contained `padyam.py` with the
NVFP4 loader. Once the folder is on the Hub:

```bash
python padyam.py --metre utpalamala --bhavam "<a bhāvam in Telugu>"     # ≈ 52 GB of GPU memory
python padyam.py --metre కందము --bhavam-file bhavam.txt --n 3 --packed    # experts kept in NVFP4: ≈ 19 GB, slower
```

Here, `evaluate_e6.py`, `val_metrics.py` and `sample.py` take `--lora` with either `runs/<run>/lora.pt` or the
release's `adapter.safetensors`; both hold the same tensors under the same names.

```bash
cd lora_gemma_diffusion
../.venv/bin/python -u sample.py --name try --lora runs/lora-full/lora.pt --n 11       # 11 free poems, one per metre
```

## How it was fine-tuned

### The model

- **Weights:** NVIDIA's NVFP4 checkpoint, loaded by `../meter_engine/metrical_decoder/diffusion/loader.py` into
  transformers' `DiffusionGemmaForBlockDiffusion`, with the experts decoded once to BF16 (≈ 52 GB resident). NVIDIA
  quantised only the mixture-of-experts experts; attention, router, norms, embeddings and self-conditioning are
  Google's BF16 weights. The BF16 original would not download here and is not needed: the LoRA trains on the exact
  attention weights, and the experts stay frozen (the QLoRA recipe).
- **Block diffusion:** an autoregressive encoder caches the prompt. A decoder denoises a 256-token canvas, with
  bidirectional attention over the canvas and the cached prompt.
  - A canvas starts as uniform random tokens.
  - Each pass predicts every position and sees the previous pass's prediction (self-conditioning).
  - It keeps the confident tokens and returns the rest to noise.
  - Encoder layer *i* and decoder layer *i* share their weights.
  - A poem (≈ 100–200 Gemma tokens) fits in one canvas.

### One training example (`common.py`)

- **Prompt:** one user message in the chat template, with thinking off and the empty thinking channel prefilled, as
  the project's decoder prompts it:

```
ఛందస్సు: ఉత్పలమాల
శైలి: ప్రాచీన
[సమస్య / మకుటం: <a given last line>]
భావం: <the bhāvam>
ఈ భావాన్ని ఈ ఛందస్సులో ఒక తెలుగు పద్యంగా వ్రాయండి.
```

- **Canvas:** the poem's tokens, the end-of-turn token, then the model's own end-of-reply fill up to 256 tokens. The
  fill was read from the model's own replies (`check_model.py`).
- **Noise:** t ~ U(0, 1); each canvas position is replaced by a uniform random token with probability t, as the model
  starts and re-noises.
- **Self-conditioning:** for half of the examples, a first pass without gradient gives logits that the second pass
  sees; the loss is on the second pass.
- **Loss:** cross-entropy of the clean canvas at every position.
- **ఁ and ఽ are dropped from the text** (user decision 2026-10-20):
  - Gemma has no token for ఁ, so it is spelled as three raw bytes (8.6% of poem tokens), and parallel denoising breaks
    them apart (`����`, `ఁఁఁ`).
  - Dropping both leaves the strict verdicts unchanged on 2,089 poems with ఁ: gaṇa 100%, prāsa 99.9%, yati 98.3%.
  - Word measures strip ఁ on both sides, for every model of the project.

### LoRA and optimisation (`train.py`)

| | |
|---|---|
| adapter | rank 16, α 32, on q, k, v, o of the language layers. One adapter per tied encoder/decoder pair (115), so 11.5M parameters; the base frozen. Gradients reach the lower layers through the frozen NVFP4 experts (`F.grouped_mm` backpropagates: checked 2026-10-20) |
| optimiser | AdamW on the LoRA parameters, lr 1e-4, 30 warm-up steps, cosine to 10%, gradient clipping 1.0 |
| batch | 8 examples per step: 1 per forward × 8 accumulated. Batched forwards were tried (`speed_batch.py`) and failed the equality gate (cross-entropy differences up to 0.07 nats) |
| memory and speed | decoder gradient checkpointing, bf16 autocast; ≈ 1.3 s per example, peak 56–60 GB |
| validation | 48 E6 val poems at t = 0.25, 0.5, 0.75, fixed noise, no self-conditioning, every 250 / 1,000 steps |
| seed | 20261020 |

### Data (`data.py`)

- **48k:** 48,000 poems of E6's meaning → poem pool, drawn without replacement with E6's metre weights: rare metres
  up-sampled, dvipada capped, weighted random keys in log form.
- **Whole pool** (`--n 0 --name train_full`): every pool poem that fits, at its natural mix. 300,762 of the 300,763
  fit (poem in one canvas, prompt ≤ 768 tokens).
- **Validation:** 200 E6 val poems.
- The four `dataset/` works are held out whole, as for every model of the project.

### Gates before training (`check_model.py`; PLAN.md §3, §6)

1. **The objective matches the model.** On untouched weights, the poem loss with the matching prompt is below the loss
   with another poem's prompt and on a word-shuffled poem, at every noise level:
   - t = 0.25: 1.49 / 1.84 / 1.77;
   - t = 0.5: 3.38 / 4.09 / 3.66;
   - t = 0.75: 5.57 / 6.40 / 5.72.
2. **Training forward = inference path.** The first version failed (max logit difference 6.8): transformers'
   encoder builds its causal masks and then discards them when called without a mask dict. Encoding with explicit
   masks, as the decoder does, gives difference 0.0.
3. **Smoke run** (200 steps): the val loss falls, and the samples are clean Telugu once ఁ is dropped.

### The runs

| run | data | steps | wall time | val poem loss at t = 0.25 / 0.5 / 0.75 |
|---|---|---|---|---|
| base | | | | 1.826 / 3.565 / 5.408 |
| `lora-48k`, step 3,000 ("24k") | 24,000 poems | 3,000 | | 0.779 / 1.932 / 3.626 |
| `lora-48k` | 48,000 | 6,000 | 16.9 h (10-20 09:30 → 10-21 02:23) | 0.743 / 1.878 / 3.576 |
| `lora-full` | 300,762 | 37,595 | ≈ 107 h (10-24 → 10-28 22:52) | **0.580 / 1.612 / 3.331** |

The whole-pool run flattened over its last quarter (t = 0.5: 1.674 at step 20,000, 1.620 at 28,000, 1.612 at
32,000, 1.614 at 36,000).

```bash
cd lora_gemma_diffusion
P=../.venv/bin/python
$P -u check_model.py                           # step 1 and gates 1–2 → runs/check_model.json
$P -u data.py --n 48000                        # data/train.pt (+ data/val.pt)
$P -u data.py --n 0 --name train_full          # data/train_full.pt, the whole pool
$P -u train.py --run lora-48k --epochs 1 --eval-every 250 --save-every 100 --snapshot-at 3000
$P -u train.py --run lora-full --data train_full --epochs 1 --eval-every 1000
```

Training resumes from `runs/<run>/last.pt` (also written on SIGTERM). The final adapter is `runs/<run>/lora.pt`. On the
GB10 the runs went one at a time through the GPU queues in `../experiments/scripts/`.

## How it was evaluated

**Prompts:** the 114 E6 val prompts (11 metres; `evaluate_e6.py`) and the paper's 100-prompt grid
(`../full_grid_experiments/grid.py`, rows `dg_base`, `dg_full`).
- On E6, every model, the base included, gets the T1 prompt above.
- In the grid, the base model gets the September grids' instruction prompt (the metre's rules, the bhāvam as the
  topic) instead, because it was never trained on the T1 layout.

**Decodings:**
- **Free:** the model's own `generate` (it commits its most confident positions anywhere on the canvas), cut at the
  first end token.
- **Constrained:** the project's diffusion decoder (`metrical_decoder.diffusion`, masking + backtracking, the strict
  profile), with two changes found here:
  1. **A bug in the shared decoder, fixed 2026-10-21.** Under `forbid_end` the canvas entropy was NaN at every
     position (0 · −∞): the draft never settled and the entropy bound never stopped a run of proposals. The
     September DiffusionGemma grids ran with it. The fix (`fix_canvas_entropy.py`, the user's decision) is in the shared
     package with a regression test.
  2. **Settled commit** (`settled.py`). The decoder committed the left edge of the canvas on every pass, from
     predictions that were still near-uniform (entropy 3–5 nats), so poems were assembled from first-pass guesses
     ("akshara soup"). `SettledRun` makes the left edge wait until the model's prediction there is confident.
- **v2:** the grid's v2 cells add the word-attestation layer inside the diffusion decoder (`settled_attest.py`): both
  where the constraint decides and where a run of the model's proposals is accepted.

```bash
$P -u val_metrics.py --adapters runs/lora-48k/lora_step_3000.pt runs/lora-48k/lora.pt   # → results/val_metrics.*
$P -u evaluate_e6.py --name e6_dg_full_val_free --lora runs/lora-full/lora.pt --modes baseline --free native
$P -u evaluate_e6.py --name e6_dg_48k_val_constrained --lora runs/lora-48k/lora.pt --modes masking_backtrack \
    --decoder settled                          # 68–310 s per poem
$P -u score_e6.py                              # → results/e6_comparison.*, every model on the 114 val prompts
```

`run_eval.sh`, `run_eval2.sh` and `run_eval3.sh` are the queues that ran these on 10-20 and 10-21.

## Results

### Validation diagnostics (`results/val_metrics.md`; 120 E6 val poems, nats per Gemma token)

| measure | base | 24k | 48k |
|---|---|---|---|
| integrated loss (mean over t = 1/8 … 1) | 4.10 | 2.60 | 2.55 |
| T0 − T1 at t = 1.0 (the bhāvam's value when writing from pure noise) | +0.19 | +0.43 | +0.50 |

Every metre improves by about 45% at t = 0.5. The adapters lean on the bhāvam more than the base model when writing
from noise. The whole-pool adapter was not run through `val_metrics.py`; its training-time validation is above.

### E6 validation set (114 prompts; `results/e6_comparison.md`)

All scored by one script (`score_e6.py`, `../RL/reward.py`'s definitions; real words with ఁ stripped):
- **chandas skill:** 1 = in metre, 0 = as far as prose, below 0 farther;
- **copy:** the share of the poem's words found in its bhāvam;
- **recognised:** LaBSE ranks its own bhāvam first of 10.

| set | in metre | chandas skill (mean) | real words | one-akshara words | copy | recognised | lines |
|---|---|---|---|---|---|---|---|
| *gold (the real poems)* | 39.5% | 0.96 | 86.8% | 7.0% | 2.5% | 78.1% | 4.00 |
| DiffusionGemma base, free | 0% | −1.06 | 92.3% | 4.8% | 21.2% | 62.3% | 4.00 |
| 24k, free | 0% | −0.69 | 67.9% | 9.9% | 18.9% | 95.6% | 3.13 |
| 48k, free | 0% | −0.59 | 70.0% | 9.4% | 20.8% | 91.2% | 3.19 |
| **whole pool, free** | 0% | **0.07** | **80.2%** | 4.3% | 13.9% | 95.6% | 3.89 |
| base, constrained | 100% | 1.00 | 35.0% | 22.1% | 1.8% | 27.2% | 4.00 |
| 48k, constrained | 100% | 1.00 | 29.6% | 17.9% | 2.3% | 63.2% | 4.00 |
| *MDLM 523M, free / constrained* | 0% / 100% | 0.67 / 1.00 | 88.3% / 83.1% | 8.4% / 10.3% | 5.7% / 3.1% | 85.1% / 81.6% | 3.99 / 4.00 |
| *T5Gemma 2 1B, free / constrained* | 6.1% / 100% | 0.90 / 1.00 | 82.5% / 79.2% | 5.8% / 5.2% | 3.0% / 2.4% | 77.2% / 79.8% | 4.00 / 4.00 |
| *Nandi-Mini-150M, free / constrained* | 3.5% / 100% | 0.88 / 1.00 | 79.5% / 76.6% | 7.5% / 8.0% | 1.8% / 1.5% | 74.6% / 74.6% | 4.00 / 4.00 |

### MAUVE (E6 val; ఁ stripped; `../metrics/mauve_padyarchana/report_more_stripped.md`)

| set | vs the training corpus | vs the gold poems |
|---|---|---|
| *gold val* | 0.922 | 1.000 |
| base, free / constrained | 0.004 / 0.025 | 0.004 / 0.038 |
| 48k, free / constrained | 0.330 / 0.232 | 0.554 / 0.229 |
| *MDLM 523M, free / constrained* | 0.845 / 0.885 | 0.941 / 0.953 |

### Memorisation (`results/memorisation.md`; `../diffusion_finetuning/memorisation.py` against the E6 training poems)

The share of poems whose longest run of aksharas shared with any one training poem reaches N, and the share of
their lines found verbatim in a training poem. A run of 6–8 aksharas is a common phrase; a vṛtta line is about 20.

| run | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | ordinary lines copied |
|---|---|---|---|---|---|
| base, free | 114 | 98.2% | 22.8% | 0.9% | 0.0% |
| 24k, free | 114 | 67.5% | 7.9% | 0.9% | 0.0% |
| 48k, free | 114 | 67.5% | 6.1% | 0.9% | 0.0% |
| whole pool, free | 114 | 74.6% | 6.1% | 0.9% | 0.0% |
| base, constrained | 114 | 9.6% | 0.0% | 0.0% | 0.0% |
| 48k, constrained | 114 | 15.8% | 0.0% | 0.0% | 0.0% |

- **The one ≥ 12 poem** is the same prompt in every free run (`dataset/bhagavatam:1-89-ఉ.`), the base model's
  included. The base never saw the training poems, so the shared run comes from the prompt, not from fine-tuning. No
  poem copies an ordinary line; the base model's free poems hold one refrain (a line found in ≥ 5 training poems).
- **The base model's free poems share the most short runs** (98% at ≥ 6): its fluent modern prose reuses common
  phrases.
- **Constrained poems share few,** because the decoder breaks up the model's words.

### The paper's grid (100 prompts; `../full_grid_experiments/results/grid.json`)

| model | decoding | in metre (strict) | vṛtta lines on the gaṇa pattern | real words | recognised (1 of 10) | one-akshara words | a line repeated |
|---|---|---|---|---|---|---|---|
| DiffusionGemma base | free / constrained / v2 | 0% / 100% / 100% | 0% / 100% / 100% | 87.2% / 33.5% / 40.0% | 100% / 64% / 59% | 4.1% / 23.0% / 16.9% | 0% / 0% / 0% |
| **DiffusionGemma, whole-pool LoRA** | free / constrained / v2 | 0% / 100% / 100% | 0% / 100% / 100% | 79.7% / 29.6% / 38.6% | 90% / 47% / 41% | 4.5% / 11.7% / 7.0% | 0% / 12% / 13% |
| *MDLM 523M fine-tuned* | free / constrained / v2 | 1% / 99% / 100% | 39.4% / 100% / 100% | 89.0% / 77.5% / 85.4% | 80% / 77% / 76% | 6.2% / 10.6% / 6.9% | 1% / 2% / 3% |
| *T5Gemma 2 1B fine-tuned* | free / constrained / v2 | 8% / 100% / 100% | 73.4% / 100% / 100% | 82.8% / 74.1% / 82.3% | 75% / 66% / 72% | 4.1% / 5.3% / 4.6% | 1% / 1% / 1% |
| *the 100 source poems* | | 53% | 95.7% | 85.7% | 63% | 5.0% | 0% |

No DiffusionGemma grid poem copies a training line or 12 aksharas of its source poem.

### What the results say

- **The LoRA learned the corpus's language, not its metre.** The whole-pool adapter's validation loss fell by half
  or more, and its free poems moved from prose toward verse: chandas skill −1.06 → 0.07, real words 80%. Yet not one
  free line in the grid is on the gaṇa pattern. The MDLM 523M manages 39% and T5Gemma 1B 73%.
- **It paraphrases the bhāvam.** The adapters' free poems take 14–21% of their words from the bhāvam (gold 2.5%) and
  are recognised 91–96% of the time on E6 (90% on the grid). That recognition is a topic signal, and copying
  inflates it.
- **The metre constraint fights the model.** Constrained poems are in metre, but real words collapse to 30–40%. The
  MDLMs and T5Gemma keep 74–85% under the same constraint. A diffusion model that writes the whole canvas at once
  does not fit a left-to-right metre automaton. Even with the bug fixed and the settled commit, long vṛttas run out of
  backtracking and fill with what scans.
- **More data helped, a little.** From 24k to 48k to the whole pool, chandas skill rose (−0.69 → −0.59 → 0.07) and
  so did real words (68% → 70% → 80%). Most of the gain came from 48k to the whole pool, where copying also fell
  (21% → 14%).
- **It is slow:** 68–310 s per constrained poem (mean ≈ 196 s on 11 poems), against seconds for the small models.

## Scripts

Every script runs from this folder with `../.venv/bin/python`.

| script | purpose | reads | writes |
|---|---|---|---|
| `common.py` | The shared library (no command line): `load` (the NVFP4 checkpoint through the project's loader, then its page cache dropped), `inject_lora` / `load_lora` / `lora_state` (adapters shared by tied layers; `.pt` or `.safetensors`), `prompt_ids` (the T1 prompt in the chat template), `canvas_ids`, `encode` (with explicit masks), `diffusion_loss` | the HF cache, E6 records | |
| `check_model.py` | Step 1 and gates 1–2: loads the model, reads its reply format and canvas fill, compares the training forward with the decoder's path, checks the loss against mismatched prompts and shuffled poems, one LoRA step | the model, E6 val | `runs/check_model.json` |
| `data.py` | Builds the training and validation examples in Gemma's tokens: an E6-weighted sample (`--n`) or the whole pool (`--n 0`) | E6 records, `runs/check_model.json` | `data/<name>.pt`, `data/val.pt`, `data/stats*.json` |
| `train.py` | LoRA training: uniform-noise corruption, self-conditioning, cross-entropy on the whole canvas; validation at fixed noise; resumable; snapshots | `data/` | `runs/<run>/` (`metrics.jsonl`, `last.pt`, `lora.pt`, `lora_step_*.pt`) |
| `speed_batch.py` | Tests batched forwards for the whole-pool run (equality gate, then speed); the gate failed, so batch 1 | `data/train_full.pt` | `runs/speed_batch.json` |
| `sample.py` | Free poems from the model's own sampler, base or adapter, one per metre, scored by the engines | E6 prompts | `runs/<name>/samples.jsonl` |
| `val_metrics.py` | Validation diagnostics in one model load: integrated loss, T1 against T0 at four noise levels, per metre (the base = an adapter with B = 0) | `data/val.pt`, adapters | `results/val_metrics.{md,json}` |
| `evaluate_e6.py` | The E6 evaluation: free (native sampler) and constrained (the project's diffusion decoder, settled commit), on a reference run's prompts or the grid's | the model, E6 records | `runs/<name>/` (poems, traces) |
| `settled.py` | `SettledRun`: the constrained decoder with the left edge waiting until the model is confident | | |
| `settled_attest.py` | `AttestedRun`: the v2 word-attestation layer inside the settled diffusion decoder (the grid's v2 cells) | `meter_engine/metrical_decoder/attestation` | |
| `fix_canvas_entropy.py` | The one-off patch of the shared decoder's NaN entropy (applied 2026-10-21; idempotent) and its regression test | | `meter_engine/metrical_decoder/diffusion/canvas.py`, its test |
| `score_e6.py` | Scores every model's E6 val poems with one definition set: DiffusionGemma beside the MDLMs, Nandi and T5Gemma | every folder's `runs/e6_*` | `results/e6_comparison.{md,json}` |
| `run_eval.sh`, `run_eval2.sh`, `run_eval3.sh` | The evaluation queues of 10-20 and 10-21 (val metrics and E6 runs; then free native; then the fix, its tests and the constrained runs) | | |

Scripts elsewhere that produced results here:
- `../diffusion_finetuning/memorisation.py`: copying from training poems.
- `../metrics/mauve_padyarchana/score_more.py`: MAUVE.
- `../full_grid_experiments/grid.py`: the grid cells.

## Results files

| file | what |
|---|---|
| `results/e6_comparison.{md,json}` | every model on the 114 E6 val prompts (`../t5_finetuning/README.md` cites it) |
| `results/val_metrics.{md,json}` | validation diagnostics: base, 24k, 48k |
| `results/memorisation.md`, `results/e6_dg_*_memorisation.{md,json}` | memorisation of every E6 run |

## Known limits and open items

- **Not done:**
  - the 24k adapter's constrained E6 run and the rerun of the September trial with the fixed decoder (both dropped,
    2026-10-28);
  - `val_metrics.py` for the whole-pool adapter;
  - a test-split evaluation.
- **The native sampler stops at 48 passes**, so a poem that has not settled is filled in parallel. More passes is an
  untested lever.
- **ఁ and ఽ cannot be written:** they are not in the training text.
- **The release** waits for the GPU check of its inference script (`../hf_release/test_release.py --only
  diffusiongemma-26b-padyam-lora`, ≈ 55 GB free).
