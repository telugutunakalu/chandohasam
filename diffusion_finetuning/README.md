# diffusion_finetuning

Fine-tunes the project's masked diffusion language models (MDLMs, `../diffusion_pretraining`) to write a *padyam*
from a metre and a bhāvam (the poem's meaning in prose). Status 2026-10-31: both models are trained, evaluated and
released.

| model | starts from | run (here) | released as |
|---|---|---|---|
| MDLM 120M, fine-tuned | `pilot120m`: 120M, trained from scratch on 4.98B tokens of general Telugu (EMA, step 76,000) | `runs/e6-t1-120m` | [`samvaran/chandohasam/mdlm-120m-padyam`](https://huggingface.co/samvaran/chandohasam/tree/main/mdlm-120m-padyam) |
| MDLM 523M, fine-tuned | `stage1-523m`: the pilot **grown** to 1536 × 16 (function-preserving: same outputs at step 0; `mdlm/grow.py`), then pretrained to step 160,000 (10.49B tokens) | `runs/e6-t1-523m` | [`samvaran/chandohasam/mdlm-523m-padyam`](https://huggingface.co/samvaran/chandohasam/tree/main/mdlm-523m-padyam) |

Both bases are released too: `pilot120m` at the root of
[samvaran/chandohasam](https://huggingface.co/samvaran/chandohasam), the 523M as `mdlm-523m/`. How they were
pretrained and grown: [`../diffusion_pretraining/README.md`](../diffusion_pretraining/README.md).

The training poems come from a crawled corpus of over 300k Telugu poems with meanings (`padyarchana_exports/`). It is
confidential: it is not in this repository, and nothing built from it (`data/`, `runs/`) is ever committed. Without it,
everything here runs except training and the evaluations that read `data/`. The released models need none of it.

## Write a poem with the released models

Free decoding (left to right, temperature 0.7, top-p 0.9; the "free" rows of the results), from the Hub, on a GPU or
a CPU:

```python
from huggingface_hub import snapshot_download

repo = snapshot_download("samvaran/chandohasam", allow_patterns=[
    "chandohasam_mdlm/*", "telugu_alldomain.tokenizer.json", "padyam.py", "metres.json",
    "mdlm-523m-padyam/*"])            # or mdlm-120m-padyam/*
print(repo)
```

```bash
python <repo>/padyam.py --model mdlm-523m-padyam --metre utpalamala \
    --bhavam "ఓ రామా! నీ నామమే నాకు రక్ష. నిన్ను ఎల్లప్పుడూ స్మరిస్తాను."    # ≈ 9 s with loading, one GPU
python <repo>/padyam.py --model mdlm-120m-padyam --metre కందము --bhavam-file bhavam.txt --n 3
python <repo>/padyam.py --list-metres         # the 37 metres of the fine-tuning poems
```

Options: `--register ప్రాచీన|ఆధునిక` (classical, the default, or modern), `--source యంత్రం|గ్రంథం` (who wrote the
bhāvam: a machine, the default, or an edition), `--samasya` / `--makutam` (a given last line; untested in evaluation),
`--n`, `--seed`, `--temperature`, `--top-p`. The model cards on the Hub give the prompt layout and the full results.

**In metre.** Free decoding is almost never in metre (0–1%, below). The metrical decoder
(`../meter_engine/metrical_decoder`) allows only tokens that keep the poem completable in its metre, and
`constrained_sample.py` runs it with these models. `--model` takes a run folder or a downloaded Hub folder (the
released weights give exactly the runs' logits). It needs two things built from the corpus:
- `data/tokens/poems/train.bin` (`prepare_poems.py`), which sets the vocabulary slice;
- `data/e6/records` (`ft.build_data`), the prompts.

So it runs only where the data has been built:

```bash
cd diffusion_finetuning
../.venv/bin/python -u constrained_sample.py --model <repo>/mdlm-523m-padyam --name e6_523m_hub_val --e6-split val \
    --modes baseline masking_backtrack --shards 2 --mask-workers 2     # → runs/e6_523m_hub_val/, results/e6_523m_hub_val.md
```

The paper's grid ran the same script on its 100 prompts through `../full_grid_experiments/grid.py` (rows
`mdlm120m_ft`, `mdlm523m_ft`); its v2 cells wrap it in `../full_grid_experiments/v2.py`.

## How the models were trained

Recipe "E6 + T1", identical for both sizes (the user's decisions of 2026-10-13 and 10-16; `exp_checklist.md`, E6).

### Data (`ft.build_data --out data/e6`, 222 s on the CPU)

- **Held out whole:** every poem of the repo's own corpora, `../dataset/{bhagavatam,vemana,kuchimanchi_timmakavi,
  chandassu}.json`, so no evaluation poem is in the fine-tuning data.
- **Dropped from train:** 14,634 poems with the text of a `dataset/` record, 1,295 near-duplicates of one (≥ 50%
  8-gram containment either way) and 443 other records of the held-out works.
- **Leakage:** 112 held-out poems occur in the *pretraining* text (105 of them the Venugopāla śatakam); every
  evaluation skips them (`ft.leakage`, `data/e6/leakage.json`).

| split | poems | what |
|---|---|---|
| train | 365,680 | the crawled corpus: 247,451 classical, 118,229 modern; 363,821 with a meaning (153,198 from editions, 210,623 machine-written) |
| val | 906 | Bhāgavatam skandhas 1, 2, 7, with edition bhāvams; every development decision |
| test | 10,749 | the rest of `dataset/`: Bhāgavatam 5,411, Vemana 1,164, Kūcimañci Timmakavi 1,642, chandassu 2,532 |

The metre-and-meaning pool (task T1) is the 300,763 training poems whose metre the engines confirm and that have a
meaning. Stage 1 reads 85.5M tokens of poem + meaning documents.

### Strategy: full-parameter supervised fine-tuning

Every weight of the model trains: nothing is frozen and no adapter (LoRA) is used. The three stages below run in
sequence. Each starts from the previous stage's EMA weights with a fresh optimizer; stage 1 starts from the base's EMA
(`pilot120m` at step 76,000 for the 120M; the 523M at step 160,000).

| setting | value (`runs/e6-*/config.json`, `ft/train.py`, `ft/loss.py`) |
|---|---|
| objective | the MDLM NELBO: each maskable position is masked with probability t (t drawn low-discrepancy across the batch) and scored by −log p / t. Stage 1: every trainable position of a window is maskable, and the sum is divided by the step's tokens. Stages 2 and T1: only the target and the `<eos>` fill after it are maskable (the given part never is), and the sum is divided by the step's target tokens |
| optimizer | AdamW (fused), β (0.9, 0.98), weight decay 0.1 on matrices, 0 on vectors |
| schedule | linear warm-up, then cosine decay to 10% of the peak rate |
| batch | 128 sequences per step: stage 1, 128 windows of 512 tokens; stages 2 and T1, 128 canvases in length buckets of 128 / 256 / 384 / 512 tokens. Each step runs as micro-batches of at most 4,096 tokens, with the gradients accumulated |
| precision | fp32 weights and optimizer state, bf16 autocast; `torch.compile` on the trunk |
| clipping, seed | gradient norm 1.0; seed 1 |
| EMA | decay 0.999. The EMA weights are what is evaluated, what the next stage starts from, and what is released |
| replay | stage 1 only: each window is general Telugu text from pretraining with probability 0.15 (Sangraha 0.75, IndicCorp 0.20, Wikipedia 0.05). Stages 2 and T1 read poems only; their configs carry the field, unused |
| sampling | stages 2 and T1 draw canvases with replacement. The metre tasks (T1, T5, T0) are metre-weighted: metres with fewer than 500 poems up-sampled, at most 5×, and dvipada capped at 10%. An epoch is the T1 pool over 128 (2,350 steps) |

### Stages (`ft.train`)

| stage | what | steps | lr | 120M | 523M |
|---|---|---|---|---|---|
| 1 | continued pretraining on poem + meaning documents, 512-token windows, 3 passes | 4,606 | 1e-4 (200 warm-up) | 5.9 h | 7.8 h |
| 2, sweep | the six tasks below, 1 epoch at each of 3e-5 / 6e-5 / 1e-4; keep the rate with the lowest val T1 NELBO | 3 × 4,699 | → **1e-4** for both | 9.0 h | 12.9 h |
| 2 | the six tasks, 2.5 epochs at the chosen rate | 11,748 | 1e-4 (100 warm-up) | 7.6 h | 10.7 h |
| T1 | metre + bhāvam → poem only: 2,350 × 128 weighted draws, one epoch of the 300,763-poem pool | 2,350 | 3e-5 = 0.3 × 1e-4 (50 warm-up) | 1.6 h | 2.6 h |

Wall times on the GB10. The 120M trained beside the 523M's pretraining, sharing the GPU.

The stage-2 tasks (`ft/canvas.py`, `DEFAULT_MIX`), one per canvas; the loss is the MDLM objective on the target
positions only, the given part is never masked:

| task | given → target | share |
|---|---|---|
| T1 | metre + register + bhāvam (+ a samasya / makuṭam line) → poem | 50% |
| T5 | a poem with a line or some words missing → the missing spans | 15% |
| T2 | poem → bhāvam | 15% |
| T0 | metre → poem | 10% |
| T3 | poem → word glosses | 5% |
| T4 | glosses → poetic words | 5% |

T1 prompt layout (plain Telugu lines after `<bos>`; the poem follows, one pāda per line, then `<eos>`):

```
ఛందస్సు: ఉత్పలమాల
శైలి: ప్రాచీన
భావం (యంత్రం): <the bhāvam>
పద్యం:
```

### Commands

Each step resumes, or is skipped when done; a run counts as done only when its trainer logged "(end of run)".

```bash
cd diffusion_finetuning
P="../.venv/bin/python -m"
$P ft.build_data --out data/e6                # data: needs padyarchana_exports/ (≈ 4 min with the prāsa/yati cache)
../.venv/bin/python prepare_poems.py          # data/tokens/poems/: the evaluations' vocabulary slice counts its aksharas
$P ft.leakage --data-dir data/e6              # held-out texts in the pretraining corpus (≈ 3 min)
$P ft.lexicon --data-dir data/e6              # decoding lexicon from the training split
$P ft.constraints --data-dir data/e6          # teacher-forced acceptance of the gold poems: val 99.7%, test 98.4%

# stage 1 → stage-2 sweep → stage 2 → val evaluation, for one size
./run_e6.sh 120m ../diffusion_pretraining/runs/pilot120m_hf/ema_step_0076000.pt "3e-5 6e-5 1e-4"
./run_e6.sh 523m ../diffusion_pretraining/runs/stage1-523m "3e-5 6e-5 1e-4"
# the T1 phase (0.3 × the sweep's rate) and its val evaluation
./run_e6_t1.sh 120m
./run_e6_t1.sh 523m
# test evaluation and memorisation of a finished model
../.venv/bin/python -u constrained_sample.py --model runs/e6-t1-523m --name e6_523m_t1_test --e6-split test \
    --shards 4 --mask-workers 2
../.venv/bin/python -u memorisation.py --run e6_523m_t1_test --train-records data/e6/records/train.jsonl
```

`run_e6.sh` takes `E6_MIX`, `E6_FINAL_EPOCHS`, `E6_SUFFIX`, `E6_EXTRA` and `E6_SKIP_EVAL` (its header). On the GB10
the runs went through systemd user services (`deploy/`):
- `e6-120m.service`: `run_e6.sh 120m`.
- `e6-queue.service`: `deploy/e6_queue.sh`, which waited for the 523M pretraining to end, then ran `run_e6.sh 523m`
  and `run_e6_t1.sh 523m`, overlapping the evaluation with the T1 phase.

`deploy/e6_t1_test.sh` is the T1 trial on the 120M that decided the phase.

## Results

### Validation loss (NELBO, nats per token; `runs/*/metrics.jsonl`)

| model | T1: metre + bhāvam → poem | T0: metre → poem | T2: poem → bhāvam |
|---|---|---|---|
| 120M before fine-tuning (pilot) | 4.05 | 3.79 | |
| 120M after stage 2 | 2.253 | 2.803 | 2.051 |
| **120M after T1** (released) | **2.230** | 2.803 | 2.065 |
| 523M after stage 2 | 1.937 | 2.570 | 1.788 |
| **523M after T1** (released) | **1.934** | 2.567 | 1.799 |

Stage-2 sweep, val T1 after one epoch at 3e-5 / 6e-5 / 1e-4: 120M 2.588 / 2.510 / 2.443; 523M 2.126 / 2.085 /
2.069.

### Held-out poems (`constrained_sample.py --e6-split`; `results/e6_{120m,523m}_t1_{val,test}.md`)

Each held-out poem is a prompt: its own metre and bhāvam, one poem per strategy (seed 42, strict profile). val: 114
prompts in 11 metres; test: 183 in 25. Free = the model alone; masking + backtracking = the metrical decoder.

| model, split | free: in metre | constrained: in metre | constrained: words in the corpora | constrained: one-akshara words | constrained: model's first choice overridden | constrained: model's mass on allowed tokens |
|---|---|---|---|---|---|---|
| 120M, val | 0% | 100% | 57% | 12% | 19% | 0.786 |
| 523M, val | 0% | 100% | 56% | 11% | 12% | 0.855 |
| 120M, test | 0% | 99% | 50% | 13% | 24% | 0.725 |
| 523M, test | 1% | 100% | 52% | 13% | 19% | 0.781 |

**Memorisation** (`results/*_memorisation.md`, against the training split): no poem of any strategy shares a run of
12 or more aksharas with a training poem, and none copies a line.

### The paper's grid (100 prompts; `../full_grid_experiments/results/grid.json`)

One poem per prompt and decoding (seed 42). The prompts are 90 poems of the held-out works (Bhāgavatam 50, Vemana 20,
Kūcimañci Timmakavi 20) with bhāvams retold by Gemma-4 26B, and 10 Gemini poems with Gemini's own. v2 adds two
layers to the decoder: attested syllables only, and a preference for tokens that keep a word real.

| model | decoding | in metre (strict) | real words | recognised (1 of 10) | one-akshara words | a line repeated |
|---|---|---|---|---|---|---|
| 120M base | free | 0% | 98.2% | 44% | 5.1% | 3% |
| | constrained | 93% | 58.0% | 20% | 20.8% | 11% |
| | constrained v2 | 100% | 66.0% | 24% | 9.3% | 8% |
| **120M fine-tuned** | free | 0% | 91.6% | 83% | 6.2% | 1% |
| | constrained | 100% | 77.7% | 73% | 12.7% | 1% |
| | constrained v2 | 100% | 81.6% | 63% | 5.4% | 0% |
| 523M base | free | 0% | 98.7% | 45% | 3.9% | 19% |
| | constrained | 85% | 59.6% | 19% | 17.7% | 13% |
| | constrained v2 | 100% | 67.0% | 22% | 7.8% | 39% |
| **523M fine-tuned** | free | 1% | 89.0% | 80% | 6.2% | 1% |
| | constrained | 99% | 77.5% | 77% | 10.6% | 2% |
| | constrained v2 | 100% | 85.4% | 76% | 6.9% | 3% |
| *the 100 source poems* | | 53% | 85.7% | 63% | 5.0% | 0% |

- **Real words:** words of two or more aksharas that are known forms of the fine-tuning text, or 2–3-part compounds of
  them.
- **Recognised:** LaBSE ranks the poem's own bhāvam first among 10. It is a topic signal, not a judgement of meaning.
- **The source poems pass the strict profile only 53%:** it rejects readings that poets use.

No fine-tuned model's grid poem copies a training line or 12 aksharas of its source poem. The 523M base copies a
training line in 1% of its free poems. The paper also scores these poems on fluency, sound and density metrics:
`../final_report_metrics/`.

### What the results say

- **The models use the bhāvam.** Given it, the poem costs 0.57 (120M) and 0.63 (523M) nats per token less than from the
  metre alone. Under the decoder, 73–77% of poems are recognised from their bhāvam, against 19–20% for the bases.
- **Size helps.** The 523M is 0.30 nats below the 120M on T1, and its first choice needs overriding less often (12%
  against 19% on val).
- **The T1 phase is a small gain:** 2.253 → 2.230 on the 120M, 1.937 → 1.934 on the 523M.
- **Metre comes from the decoder, not the model.** Free poems are fluent (89–92% real words) and fit the gaṇa pattern
  only partly (20% of the 120M's vṛtta lines, 39% of the 523M's). Constrained poems are in metre, at a cost in real
  words (78%), which v2 mostly recovers (82–85%).
- **No copying** of training poems, in any mode.

## Earlier experiments (E1–E5, 2026-10-05 → 10-11)

Before E6 the models trained on poems alone. E6 replaced this line: those runs trained on most of `dataset/`, which
is now the test set. Their tools and results stay here (`exp_checklist.md` §4, §8).

| | question | tool | result |
|---|---|---|---|
| E1 | How far is verse from the pilot's prose? | `eval_nelbo.py` (data: `prepare_poems.py`) | verse costs 1.37 nats/token more than prose with the same content |
| E2 | What does the pretraining buy? | `finetune.py --init pilot` / `scratch` | from the pilot test verse 2.685, from scratch 3.197 (5 passes; 10 passes: 2.553) |
| E3 | How do the models behave under the metre constraint? | `constrained_sample.py` (37 metres × 3 topics × 5 seeds), `compare_e3.py` | real words 26–33%, one-akshara filler 30–44% (the 10-pass model) |
| E4 | Do they copy training poems? | `memorisation.py` | no copying under the constraint |
| E5 | Does a metre tag help? | `prepare_tags.py` | filler falls by about a third; the rare vṛttams barely move |
| E5b | Only catalogue-metre poems? | `prepare_metrical.py` | no gain; worse likelihood |

## Files

| file | what |
|---|---|
| `run_e6.sh`, `run_e6_t1.sh` | the E6 recipe for one size, and the T1 phase (above) |
| `deploy/` | the systemd user services and queue scripts that ran them on the GB10 |
| `constrained_sample.py` | runs `metrical_decoder` with an MDLM (left-to-right commitment over the 512-token canvas): the E3 grid, or held-out poems as prompts (`--e6-split`) |
| `memorisation.py` | longest akshara run shared with a training poem; verbatim lines |
| `common.py` | paths, the tokenizer, `load_model` (pilot, run folders, checkpoints, snapshots, Hub folders), memory waits for the GB10 |
| `prepare_poems.py`, `prepare_tags.py`, `prepare_metrical.py`, `finetune.py`, `eval_nelbo.py`, `compare_e3.py` | the E1–E5 tools |
| `ft/` | the E6 pipeline (table below) |
| `tests/` | 49 tests of `ft/`, on the CPU |
| `results/` | every evaluation, numbers only (no poem text). `e6_*`: E6 (`_memorisation`: E4-style checks); `grid_mdlm*`: the paper grid's MDLM cells, written here by `../full_grid_experiments/grid.py`; `rl_*`: the trial in `../RL`; `e1_*` – `e5b_*`: the earlier experiments |
| `plots/` | training curves (`plots/README.md`) |
| `PLAN.md`, `ALTERNATIVES.md` | the fine-tuning design (2026-09) and an option not taken |
| `exp_checklist.md` | the experiment log: questions, predictions, every result with its date |
| `RLVR_PLAN.md` | the plan for reinforcement learning with verifiable rewards (2026-10-17) |
| `data/`, `runs/`, `models/` | gitignored: the built data, the runs (174 GB), and a local copy of `pilot120m` |

`ft/`, by stage of `PLAN.md`. "E6" marks the modules the released models were trained and checked with:

| module | E6 | what it does |
|---|---|---|
| `text.py` | ✓ | cleans poem and meaning text, splits at separators, holds the header strings |
| `metres.py` | ✓ | maps metre labels to the catalogue, runs engine identification, puts every poem in one layout (one pāda per line; sīsa pādas as two half-lines) |
| `dedup.py` | ✓ | near-duplicates by character 8-gram containment |
| `build_data.py` | ✓ | splits, labels, near-duplicate removal, round-trip check, shared-line (samasya / makuṭam) detection, prāsa/yati verdicts for eval poems (cached), stage-1 documents, records, data card |
| `leakage.py` | ✓ | eval poems and meanings in the pretraining corpus |
| `canvas.py` | ✓ | the T0–T5 canvases with per-token roles, 128–512 buckets, the task mixes and sampling pools |
| `loss.py`, `batches.py`, `train.py` | ✓ | the MDLM loss on maskable positions; deterministic batches with replay; the trainer (init from EMA, resume, OOM and NaN guards, power awareness, validation, samples) |
| `constraints.py`, `yati_oracle.py`, `lexicon.py` | checks | `PLAN.md`'s own constraint compiler, yati oracle and word lexicon. E6 used them only for the data checks; decoding used `metrical_decoder` |
| `decode.py`, `engines.py`, `evaluate.py`, `judge.py`, `rft.py` | | `PLAN.md`'s sequential Monte Carlo decoder, engine verdicts, evaluation, meaning judge (LaBSE AUC 0.88 on 60 val items) and self-training; built and tested, not used for the released models |

## Setup and tests

Everything runs with the repository's venv from this folder: `../.venv/bin/python`. The code imports
`../diffusion_pretraining` (`mdlm`, `tokenizer`) and `../meter_engine` itself. Training and decoding need a CUDA
GPU; `common.wait_for_memory` holds a job until the GB10's shared memory is free.

```bash
cd diffusion_finetuning
../.venv/bin/python -m pytest -q tests        # 49 tests, ≈ 30 s, CPU
```

## Known limits

- A sīsa with a long meaning (more than about 170 tokens) does not fit the 512-token canvas with its poem; the
  evaluations skip such prompts.
- A samasya / makuṭam line is trained (17% of the training poems have one), but no evaluation tested writing to a
  given last line.
- The modern register (32% of the training poems) is untested: every evaluation prompt is classical.
