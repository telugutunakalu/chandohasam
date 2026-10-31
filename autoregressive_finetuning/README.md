# autoregressive_finetuning

Fine-tunes [FrontiersMind/Nandi-Mini-150M](https://huggingface.co/FrontiersMind/Nandi-Mini-150M), a 150M
autoregressive (AR) model, to write a *padyam* from a metre and a bhāvam. It is the size-matched AR partner of the
project's 120M diffusion model (`../diffusion_finetuning`): same poems, same prompt fields, same evaluation. The
design is in [PLAN.md](PLAN.md). Status 2026-10-31: trained, evaluated and released.

| model | base | run (here) | released as |
|---|---|---|---|
| Nandi-Mini-150M, fine-tuned | `FrontiersMind/Nandi-Mini-150M` at revision `31c8ace` (Apache-2.0; 153,412,928 parameters) | `runs/nandi-t1`, EMA at step 8,225 | [`samvaran/chandohasam/nandi-150m-padyam`](https://huggingface.co/samvaran/chandohasam/tree/main/nandi-150m-padyam) |

## What is where

Only code, documentation and results are in git. The training data and the model weights are not.

| what | where | in git |
|---|---|---|
| code | `nandi.py`, `finetune.py`, `constrained_sample.py`, the probes, `run_nandi.sh`, `deploy/` | yes |
| results | `results/` (numbers only, no poem text), `plots/` (SVG figures) | yes |
| training data | `../diffusion_finetuning/data/e6/records/`: the E6 split, built from the confidential crawled corpus; `data/`: the encoded training examples (cache) | no |
| base model | the Hugging Face cache (`nandi.snapshot()`), pinned to revision `31c8ace` | no |
| fine-tuned model | `runs/nandi-t1/snapshots/`, released on [the Hub](https://huggingface.co/samvaran/chandohasam/tree/main/nandi-150m-padyam) | no |
| runs | `runs/`: checkpoints, generated poems (`e6_*`, `grid_*`), logs (37 GB) | no |

## Write a poem with the released model

Free decoding (temperature 0.7, top-p 0.9), from the Hub:

```python
from huggingface_hub import snapshot_download

repo = snapshot_download("samvaran/chandohasam", allow_patterns=["nandi-150m-padyam/*"])
print(f"{repo}/nandi-150m-padyam")
```

```bash
cd <repo>/nandi-150m-padyam
python padyam.py --metre utpalamala --bhavam "ఓ రామా! నీ నామమే నాకు రక్ష. నిన్ను ఎల్లప్పుడూ స్మరిస్తాను."   # ≈ 6 s with loading, one GPU
python padyam.py --metre కందము --bhavam-file bhavam.txt --n 3
python padyam.py --list-metres
```

With transformers directly: `AutoModelForCausalLM.from_pretrained(folder, trust_remote_code=True)`. Encode a
prompt as the model was trained, `[1] + tokenizer.encode(" " + prompt)` with the raw `tokenizers` tokenizer (id 1 is
`<|im_start|>`); generation ends at `<|endoftext|>` (id 0).

**In metre**, with the metrical decoder: `constrained_sample.py --weights` takes a training snapshot or the
downloaded folder; the two give identical logits. It needs three more things:
- the base model in the HF cache, for the tokenizer;
- the E6 records;
- the MDLM run whose poems it reuses.

So it runs only where `../diffusion_finetuning` has been built:

```bash
cd autoregressive_finetuning
../.venv/bin/python -c "from huggingface_hub import snapshot_download as d; \
    d('FrontiersMind/Nandi-Mini-150M', revision='31c8aceaa16e2611a5773bbefc6564db39043370')"
../.venv/bin/python -u constrained_sample.py --name e6_nandi_hub_test --weights <repo>/nandi-150m-padyam \
    --reference e6_120m_t1_test --modes baseline masking_backtrack    # → results/e6_nandi_hub_test.md
```

## How it was trained

### Data and prompt

- **Pool:** E6's meaning → poem (T1) pool from `../diffusion_finetuning`: the 300,763 training poems with a metre
  the engines confirm and a meaning. The four `dataset/` works are held out whole, exactly as for the MDLMs.
- **Length cap:** examples over 1,024 Nandi tokens are dropped (0.04%; the longest is 2,377, above the 2,048 context).
- **Prompt:** the MDLMs' T1 header as plain text, encoded `[1] + encode(" " + text)` (= the wrapper's
  `<|im_start|> ` prefix):

```
ఛందస్సు: ఉత్పలమాల
శైలి: ప్రాచీన
భావం (యంత్రం): <the bhāvam>
పద్యం:
<the poem, one pāda per line><|endoftext|>
```

No token crosses the boundary between prompt and poem, so the prompt ending `పద్యం:⏎` is a token prefix of its
training example. This holds for all 21,596 checked examples (`results/step1_checks.md`).

### Recipe (`finetune.py`, mirroring E6's T1 phase with an AR loss)

- **Loss:** next-token cross-entropy on the poem tokens and the final `<|endoftext|>`; the prompt carries no loss.
- **Batches:** 128 examples per step, drawn with E6's metre weights (rare metres up-sampled, dvipada capped). One
  epoch = 2,350 steps. Batches are a pure function of (seed, step), so a resumed run is identical.
- **Optimiser:** AdamW, β (0.9, 0.98), weight decay 0.1 on matrices, clip 1.0, 100 warm-up steps then cosine to 10%,
  bf16 autocast over fp32 weights.
- **EMA:** decay 0.999; the EMA is what is evaluated and saved.
- **Speed:** torch.compile, 12.5k tokens/s, 1.08 h per epoch, 11 GB (`results/step2_speed.md`).
- **Length:** 3.5 epochs = 8,225 steps. This is the meaning → poem exposure of the MDLM partner: E6's 2.5 passes
  plus its 1-epoch T1 phase.

| step | what | steps | lr | wall time |
|---|---|---|---|---|
| 1 | download, code review, tokenizer and model checks (`check_nandi.py`, CPU) | | | |
| 2 | leakage probe of the base model (`leakage_probe.py`) | | | 17 min |
| 3, sweep | one epoch at each of 5e-5 / 1.5e-4 / 4.5e-4. The best was at the edge, so 1.35e-3 was added | 4 × 2,350 | → **1.35e-3** | 4.7 h |
| 3 | final run from the base model at 1.35e-3 | 8,225 | 1.35e-3 | 4.1 h |
| 4 | E6 evaluation: val (114 poems) and test (183 poems) | | | 38 min, 75 min |

The step-3 schedule ran 2026-10-18 12:32 → 21:36 (`runs/nandi.chain.log`).

### Commands

Each step resumes, or is skipped when done.

```bash
cd autoregressive_finetuning
../.venv/bin/python check_nandi.py                  # step 1 (CPU) → results/step1_checks.{md,json}
./run_nandi.sh "5e-5 1.5e-4 4.5e-4" 3.5             # steps 2–3: leakage probe, sweep (+ an edge rate), final run
# step 4: the E6 evaluation, on the MDLM rows' poems; then memorisation against the E6 train split
../.venv/bin/python -u constrained_sample.py --name e6_nandi_val --weights runs/nandi-t1/snapshots/ema_step_0008225.pt
../.venv/bin/python -u constrained_sample.py --name e6_nandi_base_val                 # the base model
../.venv/bin/python -u constrained_sample.py --name e6_nandi_test --weights runs/nandi-t1/snapshots/ema_step_0008225.pt \
    --reference e6_120m_t1_test
ln -sfn ../../autoregressive_finetuning/runs/e6_nandi_val ../diffusion_finetuning/runs/e6_nandi_val
(cd ../diffusion_finetuning && ../.venv/bin/python memorisation.py --run e6_nandi_val \
    --train-records data/e6/records/train.jsonl)                                      # → its results/
../.venv/bin/python -u exposure_probe.py            # memorisation over training, the 3 models (≈ 30 min, GPU)
../.venv/bin/python plot_curves.py                  # plots/ here and in ../diffusion_finetuning/plots/
```

On the GB10 these ran as systemd user services (`deploy/`):

| service | script | what |
|---|---|---|
| `nandi-ft` | `run_nandi.sh` | steps 2–3 |
| `nandi-eval` | `deploy/nandi_eval_queue.sh` | step 4 on val (final, base, step 4,000) and memorisation, after training |
| `e6-test` | `deploy/e6_test_queue.sh` | the test evaluation of the three final models (120M, 523M, Nandi) and memorisation |
| `curves` | `deploy/curves_queue.sh` | the exposure probe, then the figures |

The paper's grid runs `constrained_sample.py` from `../full_grid_experiments/grid.py` (rows `nandi_base`, `nandi_ft`),
which writes `results/grid_nandi_*`.

## Results

### Before training (steps 1–2)

- **Checks pass** (`results/step1_checks.md`):
  - code reviewed, no network or file access;
  - round trip exact on 10,000 training poems;
  - the custom layers verified (each of 16 layers runs twice; tied, factorised embedding).
- **Not spellable:** whole tokens can spell 99.993% of the held-out poems' characters; ఝ, ఙ and ఽ cannot be spelled
  (114 of 11,655 poems).
- **Partial-byte tokens:** 1,329 vocabulary ids decode to part of a UTF-8 character. They cover 1.14% of held-out poem
  tokens, for example ఱ after a vowel sign. The constrained modes cannot write them (see Known limits).
- **No leakage** (`results/step2_leakage.md`). Continuing the first line of each of the 11,655 held-out poems, the base
  model never reproduces a run of 12 or more aksharas of the real poem. The longest run is 7, and the web-known
  positive control is no different. No poem had to be excluded.
- **Zero-shot loss:** val T1 4.185, T0 4.284 nats per MDLM target token.

### Validation loss (nats per MDLM target token, E6's unit; `runs/nandi-t1*/metrics.jsonl`)

| run | T1: metre + bhāvam → poem | T0: metre → poem | T0 − T1 |
|---|---|---|---|
| base model, zero-shot | 4.185 | 4.284 | 0.10 |
| sweep, 1 epoch: 5e-5 / 1.5e-4 / 4.5e-4 / 1.35e-3 | 2.705 / 2.395 / 2.171 / 2.061 | 3.271 / 3.081 / 2.953 / 2.858 | |
| final run, lowest (step 4,500, 1.9 passes) | 1.890 | 2.729 | 0.84 |
| **final run, end** (step 8,225; released) | **2.126** | 3.100 | 0.97 |

- **Units:** Nandi's loss is an exact NLL and the MDLM's a NELBO (an upper bound), so compare gaps and shapes across
  the families, not levels.
- **Overfitting:** the run overfits after about 1.9 passes. The released model is its end, as run and evaluated in
  the paper. The saved snapshot nearest the minimum, step 4,000 (T1 1.895), decodes almost the same (below).

### Held-out poems (`constrained_sample.py`; `results/e6_nandi_*.md`)

The same (metre, poem) pairs and token budgets as the MDLM rows, one poem per strategy (seed 42, strict profile).
val: 114 poems in 11 metres; test: 183 in 25.

| model, split | free: in metre | constrained: in metre | constrained: words in the corpora | constrained: one-akshara words | constrained: first choice overridden | constrained: mass on allowed tokens | constrained: a line repeated |
|---|---|---|---|---|---|---|---|
| base, val | 0% | 99% | 26% | 24% | 40% | 0.540 | 23% |
| step 4,000, val | 4% | 100% | 47% | 8% | 8% | 0.913 | 0% |
| **final, val** | 4% | 100% | 47% | 9% | 7% | 0.922 | 0% |
| **final, test** | 5% | 100% | 43% | 12% | 13% | 0.863 | 0% |
| *MDLM 120M fine-tuned, val* | 0% | 100% | 57% | 12% | 19% | 0.786 | 0% |
| *MDLM 120M fine-tuned, test* | 0% | 99% | 50% | 13% | 24% | 0.725 | 0% |

Constrained = masking + backtracking. **Memorisation**
(`../diffusion_finetuning/results/e6_nandi_*_memorisation.md`): no fine-tuned poem, in any strategy, shares a run of
12 or more aksharas with a training poem or copies a line. The base model's free poems copy an ordinary line in 0.9%
of cases.

### The paper's grid (100 prompts; `../full_grid_experiments/results/grid.json`)

One poem per prompt and decoding (seed 42), on the prompts of `../diffusion_finetuning/README.md`. v2 adds attested
syllables and a real-word preference to the decoder.

| model | decoding | in metre (strict) | vṛtta lines on the gaṇa pattern | real words | recognised (1 of 10) | one-akshara words | a line repeated |
|---|---|---|---|---|---|---|---|
| Nandi base | free | 0% | 0.0% | 95.6% | 43% | 7.2% | 5% |
| | constrained | 100% | 100% | 40.2% | 17% | 18.7% | 33% |
| | constrained v2 | 100% | 100% | 53.3% | 19% | 16.2% | 27% |
| **Nandi fine-tuned** | free | 5% | 77.1% | 80.4% | 65% | 5.5% | 2% |
| | constrained | 100% | 100% | 73.0% | 64% | 6.7% | 0% |
| | constrained v2 | 100% | 100% | 79.1% | 61% | 5.9% | 0% |
| *MDLM 120M fine-tuned* | free | 0% | 20.2% | 91.6% | 83% | 6.2% | 1% |
| | constrained | 100% | 100% | 77.7% | 73% | 12.7% | 1% |
| | constrained v2 | 100% | 100% | 81.6% | 63% | 5.4% | 0% |
| *the 100 source poems* | | 53% | 95.7% | 85.7% | 63% | 5.0% | 0% |

No fine-tuned grid poem copies a training line or 12 aksharas of its source poem. The base model's free poems copy a
training line in 3% of cases.

### Memorisation over training (`exposure_probe.py`; `results/exposure_probe.json`, `plots/fig5_memorisation.svg`)

At every snapshot it records the T1 loss on 900 training records and on the val records. The gap between the two
grows as the model fits its own training poems:

| model | gap early (≈ 0.2–0.4 passes) | gap at 3.5 passes |
|---|---|---|
| MDLM 120M | 0.26 | 0.34 |
| MDLM 523M | 0.27 | 0.37 |
| **Nandi** | 0.30 | **1.15** (train 0.97, val 2.11) |

At the end, training examples Nandi has seen score 0.89 nats per Nandi token, against 1.97 for those not yet drawn.

### What the results say

- **Fine-tuning works.** The model follows the format and its bhāvam: under the decoder 64% of grid poems are
  recognised, against 17% for the base. The base model meets the metre only with broken text: 40% real words and
  repeated lines in a third of its poems.
- **The AR model learns the metre's rhythm better than the MDLM.** 77% of its free vṛtta lines are on the gaṇa
  pattern (MDLM 120M: 20%), and 5% of its free poems pass the strict check outright. Under the decoder its first
  choice is overridden less (7% against 19% on val).
- **Its words are a little less real.** Constrained grid poems have 73% real words (MDLM 120M: 78%), and recognition
  is lower (64% against 73%).
- **It memorises; the MDLMs barely do.** Its val loss turns up after 1.9 passes and the train–val gap reaches
  1.15 nats. The MDLMs' gap stays under 0.4. It still never copies a training line in generation.

`plots/` has the curves (`plots/README.md`): val loss against passes, the meaning gap, train against val, the sweeps
and memorisation, for the three models.

## Files

| file | what |
|---|---|
| `nandi.py` | pinned loading (the HF cache; `trust_remote_code`, reviewed), the encoding, the T1 layout, the decoder's token slice (7,394 whole Telugu tokens + newline + space), `evaluate_t1` |
| `finetune.py` | the trainer (above). `../RL` reuses it for expert iteration (`--records`, `--init`) |
| `run_nandi.sh` | steps 2–3, end to end, resumable |
| `constrained_sample.py` | step 4: `metrical_decoder.run_grid` with Nandi (`HFCausalLM` with the custom code), on a reference MDLM run's poems |
| `check_nandi.py` | step 1's checks |
| `leakage_probe.py` | step 2: first-line continuation of the held-out poems; zero-shot likelihoods |
| `exposure_probe.py` | memorisation over training for the 120M, the 523M and Nandi |
| `plot_curves.py`, `svgplot.py` | the figures, in standard-library SVG (matplotlib could not be installed) |
| `deploy/` | the systemd user services and queue scripts |
| `results/` | `step1_checks`, `step2_leakage`, `step2_speed`, `nandi_leakage_exclude.json` (empty); `e6_nandi_*` (E6 evaluation); `exposure_probe.json`; `grid_nandi_*` (the paper grid's cells, smoke runs included); `rl_nandi_*` (the trial in `../RL`) |
| `PLAN.md` | the design (v2, 2026-10-18), with the steps' time and compute estimates |

## Setup

Everything runs with the repository's venv: `../.venv/bin/python`. `nandi.py` puts `../diffusion_finetuning`
(`ft.canvas`), `../diffusion_pretraining` (`mdlm`) and `../meter_engine` on `sys.path`, appending them. It never edits
them: the decoder is subclassed, not changed. Training and decoding need a CUDA GPU. The base model must be in
the HF cache (download above). There are no unit tests here; `check_nandi.py` is the model's check.

## Known limits and open items

- **Partial-byte tokens.** The decoder's slice holds whole tokens, so in the constrained modes 1.14% of held-out poem
  tokens must be spelled another way, and ఝ / ఙ cannot be written. PLAN §12 decision 4 proposed splitting
  "overridden" into partial-id against rule-breaking first choices. That split was not run; overrides are 7–13% in
  all.
- **Control C1** (the MDLM 120M trained on meaning → poem only, to separate recipe from family; PLAN §12) was not run.
- **The released model is the overfitted end of the run** (step 8,225), kept because it is what the paper evaluated.
- **Untested inputs:** the modern register and the samasya / makuṭam line were trained but never evaluated, as for
  the MDLMs.
