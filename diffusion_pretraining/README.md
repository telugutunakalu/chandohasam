# Telugu MDLM — pretraining

A masked-diffusion language model (MDLM) for Telugu. Stage 1 (this folder) pretrains on general Telugu (Wikipedia +
AI4Bharat corpora) for fluency. Stage 2, the specialisation to metrical poetry, is
[../diffusion_finetuning](../diffusion_finetuning). Canvas: 512 tokens. Logging is local only.

## Runs

| run | model | steps, tokens | when | result | details |
|---|---|---|---|---|---|
| `pilot120m` | `small-768`, 120M | 76,000, 4.98B | finished 2026-09-29 (2 days 19 h) | test NELBO 1.846 nats/token | [docs/pilot120m_training_report.md](docs/pilot120m_training_report.md), [model card](docs/pilot120m_model_card.md) |
| `stage1-523m` | `grow-1536x16`, 523M (453M non-embedding), grown from the pilot | 160,000, 10.49B | 2026-10-05 → 10-17 | prose NELBO 1.758 (the grown pilot) → 1.548; held-out verse 3.487 → 3.221 | `runs/stage1-523m/PROGRESS.md` (every checkpoint), [docs/stage1_523m_plan.md](docs/stage1_523m_plan.md) |
| `apatch-small768` | `akshara_patch`: code points composed into akshara positions, no token vocabulary | 15,000 | 2026-10-05/06 | 0.076 nats per akshara behind the pilot at equal steps | [akshara_patch/README.md](akshara_patch/README.md) |

`runs/` (gitignored, 226 GB) holds `pilot120m_hf/` (the pilot's config, its final EMA `ema_step_0076000.pt` and
`grown/grow-1536x16.pt`, the 523M's starting weights), `stage1-523m/`, the anneal probe `stage1-523m-anneal-20000/`
and `apatch-small768/`. Stage 2 loads its snapshots through `diffusion_finetuning/common.load_model`.

## Setup

The services and the rest of the repository use the project venv (`../.venv`, Python 3.12, torch 2.13 + CUDA 13).
`pyproject.toml` and `uv.lock` pin the stack for a fresh machine (`uv sync`: torch 2.14, CUDA 13; then `uv run` works
wherever the commands below say `../.venv/bin/python`). The project venv lacks `pyarrow`, which only `data_prep` (the finished
corpus build) needs.

```bash
cd diffusion_pretraining
CUDA_VISIBLE_DEVICES= ../.venv/bin/python -m pytest -q tests akshara_patch/tests --ignore=tests/test_data_prep.py
                             # 48 passed, 2 skipped (CUDA only), ≈ 1 min on the CPU; test_data_prep needs pyarrow
```

## Layout

| Path | What it is |
|---|---|
| `tokenizer/` | The syllable-aware tokenizer (copied from `~/phd_workspace/syllabe_aware_tokenizer`): one token per akshara, byte-BPE failover, zero OOV. Frozen vocabulary: `telugu_alldomain.tokenizer.json` (45,591 tokens; `<pad>`=0, `<unk>`=1, `<bos>`=2, `<eos>`=3, `<mask>`=4). [tokenizer/README.md](tokenizer/README.md), [BENCHMARK.md](tokenizer/BENCHMARK.md). |
| `tokenizer/aksharanusarika_split.py` | Akshara segmentation comes from `meter_engine/aksharanusarika.py`, so tokens and the meter engine always agree on akshara boundaries (ఁ stays on its akshara, ZWNJ is stripped). |
| `data_prep/` | `download.py` (the corpora into `../pretraining_datasets/raw/`, with `manifest.json`: Hub commit, licence, size, sha256), `build_corpus.py` (raw → clean, deduplicated, poem-free token files `../pretraining_datasets/tokens/<source>/{train,val,test}.bin` with `meta.json` and `report.md`), `cleaning.py`, `fingerprints.py` (MinHash-LSH), `poems.py` (the stage-2 poems and the window hashes that keep them out of stage 1), `sources.py`. |
| `mdlm/` | `model.py` (bidirectional transformer: RoPE, RMSNorm, SwiGLU, tied embeddings, no time input; `PRESETS`), `diffusion.py` (the MDLM objective, log-linear schedule), `sampling.py` (ancestral with caching, confidence), `data.py` (the source mixture), `metrics.py` (cheap sample metrics), `train.py`, `checkpoint.py` (crash-safe slots, power awareness), `grow.py` (function-preserving growth), `describe.py` (model card), `benchmark.py` (throughput), `judge.py` / `judge_watch.py` (gen-PPL under a causal LM), `checkpoint_eval.py` (every checkpoint as it appears → `PROGRESS.md`), `final_eval.py` (a finished run). |
| `akshara_patch/` | The token-free comparison model (own README and tests). |
| `deploy/` | systemd user units and scripts (below). |
| `docs/` | The pilot's training report and model card, the 523M plan, `make_report_figures.py` → `figures/`. |
| `tests/` | Tokenizer (lossless, zero OOV, aksharanusarika alignment), data prep, MDLM (loss ≈ ln V at init, masked positions only, samplers, overfitting, deterministic batches), growth (identical logits, float64), checkpoints. |

## Training

```bash
../.venv/bin/python -m mdlm.train --run pilot120m --preset small-768 --total-steps 76000 \
    --weights '{"sangraha": 0.75, "indiccorp": 0.20, "wikipedia": 0.05}'     # re-run to resume
../.venv/bin/python -m mdlm.benchmark --presets small-512 small-768 --micro-batch 8 16
../.venv/bin/python -m mdlm.judge --samples runs/pilot120m/samples/step_0005000.txt   # gen-PPL
../.venv/bin/python -m mdlm.final_eval --run pilot120m                     # test NELBO + a sampler study
```

Every hyperparameter and weight tensor of a run is documented by `mdlm.describe`; each run also writes
`runs/<run>/MODEL_CARD.md`.

Growth ladder (`mdlm.model.PRESETS`): `small-768` (120M) → `grow-1536x16` (523M) → `grow-1536x32` (976M), or
`grow-2304x16` (1.12B) directly. Every stage keeps head_dim 64, the RoPE base, the tokenizer and mlp_hidden =
8/3 · d_model, and widths are whole multiples of the previous stage, so each stage can be initialised
function-preservingly from the one before (the pilot's run folder is now `runs/pilot120m_hf`):

```bash
../.venv/bin/python -m mdlm.grow --from runs/pilot120m_hf --to grow-1536x16 --out runs/pilot120m_hf/grown/grow-1536x16.pt
../.venv/bin/python -m mdlm.train --run stage1-523m --preset grow-1536x16 \
    --init-from runs/pilot120m_hf/grown/grow-1536x16.pt --lr 2e-4 --warmup-steps 2000 --total-steps 160000 \
    --micro-batch 16 --seed 1092699556 --snapshot-every 2000 --archive-every 10000 \
    --weights '{"sangraha": 0.75, "indiccorp": 0.20, "wikipedia": 0.05}'
```

That is the 523M's run as its service ran it (`deploy/telugu-mdlm-523m.service`; `runs/stage1-523m/config.json`):
full pre-training of all 523,224,576 parameters with the MDLM objective, AdamW β (0.9, 0.98), weight decay 0.1,
gradient clipping 1.0, lr 2e-4 with 2,000 warm-up steps then cosine to 2e-5, 128 × 512-token sequences per step in
micro-batches of 16, EMA 0.9999, 160,000 steps (10.49B tokens).

`mdlm.grow` widens by cloning (HyperCloning: every hidden vector carried k times, each head repeated, linear layers
as k × k grids of w/k plus noise that cancels across the copies, final RMSNorm gain / k for the tied output) and
deepens by inserting copies of existing blocks whose output projections are zero. The grown model computes exactly
the same logits as the one it came from (`tests/test_grow.py`, float64), and `--check` compares the two on real
weights before writing. `--init-from` starts the new run with a fresh optimizer at step 0.

Each run writes `runs/<run>/`: `config.json`, `metrics.jsonl`, TensorBoard logs (when tensorboard is installed),
`samples/step_*.txt`, `snapshots/ema_step_*.pt` (bf16 EMA weights), `archive/ckpt_step_*.pt` (permanent
checkpoints, `--archive-every`) and two checkpoint slots `ckpt_a.pt` / `ckpt_b.pt` (model, EMA, optimizer, step),
written alternately and fsync'ed so a power cut always leaves one complete checkpoint. Re-running the same command
resumes from the newest readable slot; batches, masks and times are a pure function of (seed, step). Checkpoints are
saved every 15 min, on Ctrl-C/SIGTERM, immediately when a laptop loses mains power (then every 5 min on battery), and
before exiting at 15 % battery. The loss is computed only at masked positions, in chunks whose logits are recomputed
during backward, so the 45.7k-wide output layer fits in 8 GB.

## Services (`deploy/`)

| unit / script | what it does |
|---|---|
| `telugu-mdlm-523m.service` | the 523M trainer (the exact command line of the run). Finished; a start finds step 160,000 and exits. |
| `telugu-mdlm-523m-eval.service` | `mdlm.checkpoint_eval`: scores each new EMA snapshot (NELBO on prose and on held-out verse and bhāvam, 32 samples, gen-PPL under Gemma-4 E2B, real words) into `checkpoint_evals.jsonl` and `PROGRESS.md`. Every checkpoint through 160,000 is scored; it now only polls. |
| `rollback.sh <run> <step> [unit]` | roll a run back to `archive/ckpt_step_<step>.pt`, so the next start resumes there |
| `anneal_probe.sh <run> <step> [steps]` | what an archived step is worth once its learning rate is annealed (the 2026-10-07 G1 check) |
| `telugu-mdlm-pilot.service`, `telugu-mdlm-judge.service` | the pilot's trainer and CPU judge, as they ran in September (paths of the repository's old location, `anlp_project/`; not installed) |

```bash
systemctl --user status telugu-mdlm-523m-eval     # the log is runs/stage1-523m/checkpoint_eval.log
systemctl --user stop telugu-mdlm-523m-eval       # stop it (it holds no GPU memory between checkpoints)
```

Before editing `mdlm/` while a unit runs: the trainer imports it at start only, but the eval service's child
re-imports it at every checkpoint.

## Data

```bash
../.venv/bin/python -m data_prep.download         # ~31 GB, verified against the Hub (needs pyarrow)
../.venv/bin/python -m data_prep.build_corpus --workers 12
```

| Source | Hub dataset | Files |
|---|---|---|
| Telugu Wikipedia | `wikimedia/wikipedia` | `20231101.te/*.parquet` |
| Sangraha (verified) | `ai4bharat/sangraha` | `verified/tel/*.parquet` |
| IndicCorp v2 | `ai4bharat/IndicCorpV2` | `data/te.txt` |

`../pretraining_datasets/` is not tracked by git.
