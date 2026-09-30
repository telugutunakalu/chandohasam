# diffusion_finetuning

This folder fine-tunes the pretrained Telugu MDLM (`../diffusion_pretraining`) to write
metrical poems from a Telugu meaning and a metre name. The design, and the reasons behind
it, are in [PLAN.md](PLAN.md). [ALTERNATIVES.md](ALTERNATIVES.md) records one option we
considered and did not adopt: training on T1 + T2 only.

The code reuses the pretraining environment and modules: the model, checkpoints, sampler
and tokenizer. It also uses the metre engines in `../meter_engine`. Run everything from
this folder:

```
cd diffusion_finetuning
uv run --project ../diffusion_pretraining python -m <module> ...
uv run --project ../diffusion_pretraining python -m pytest -q tests
```

## Implemented

| module | stage | what it does |
|---|---|---|
| `ft/text.py` | all | Cleans poem and meaning text, splits at separators, and holds the header strings |
| `ft/metres.py` | 0 | Maps metre labels to the catalogue (spelling variants included), runs engine identification, and puts every poem into one layout: one pāda per line, with sīsa pādas kept as two half-lines |
| `ft/dedup.py` | 0 | Finds near-duplicates by character 8-gram containment |
| `ft/build_data.py` | 0 | Builds splits, labels, near-duplicate removal, the round-trip check, shared-line (samasya / makuṭam) detection, prāsa/yati verdicts for eval poems (cached), Stage 1 documents, Stage 2 records and the data card |
| `ft/leakage.py` | 0 | Checks whether eval poems or meanings appear in the pretraining corpus |
| `ft/canvas.py` | 2 | Builds the T0–T5 canvases with per-token roles (given / target / eos-fill), 128–512 buckets and the sampling pools (dvipada cap, rare-metre upsampling) |
| `ft/loss.py` | 1, 2 | The MDLM loss, restricted to maskable positions |
| `ft/batches.py` | 1, 2 | Deterministic batches: Stage 1 windows plus general-text replay; Stage 2 task draws grouped by length |
| `ft/train.py` | 1, 2, 4 | The trainer: init from EMA, resume, out-of-memory and NaN guards, power awareness, validation, and metre-probe samples |
| `ft/constraints.py` | 3 | The constraint compiler: per-token weight/prāsa features; a gaṇa-level NFA per metre (+ ettugīti, required sīsa half-breaks, no pāda after the last); pending weights (vikalpa or canonical); prāsa with bindu, lookahead, a head's pollu fused into the onset, no bare-vowel prāsa and the pre-prāsa weight rule; soft yati from `ft/yati_oracle.py`. `python -m ft.constraints` reports teacher-forced acceptance |
| `ft/yati_oracle.py` | 3 | Yati maitri at a seat: the yati engine's own verdict for every syllable token in the known left context (bindu, pollu, printed sandhi evidence), for a chosen profile and sandhi mode; cached in `data/yati_oracle/` |
| `ft/lexicon.py` | 3 | The soft word lexicon: a trie over token ids built from training poems, glosses and frequent prose words; penalties for leaving a word or joining one without a space |
| `ft/decode.py` | 3 | The decoder: left-to-right sequential Monte Carlo with batched GPU masks, optional classifier-free guidance, resampling on low effective sample size, and a rerank by engine verdict then poem → meaning likelihood |
| `ft/engines.py` | 3, eval | The engine verdict on a finished poem: metre, prāsa and yati, strict and relaxed |
| `ft/rft.py` | 4 | Self-training: generate and keep (strict engine pass + copy-rate / diversity / no-repeat guards), then build the replay set |
| `ft/evaluate.py` | eval | Predictions (constrained, free, retrieval baseline, the real poems) and metrics (engine pass rates, evaluation-lexicon share, copy rate, diversity), plus the non-word audit sheet |
| `ft/judge.py` | eval | The local meaning judge: LaBSE similarity and an LLM round trip (write a meaning for the poem, compare it). `validate` measures AUC on real poems |

Tests: `tests/` (49), all on the CPU.

## Commands

```
# Stage 0: data (about 20 min on 14 cores), the leakage audit, the decoding lexicon,
# the yati tables and the teacher-forced report.
uv run --project ../diffusion_pretraining python -m ft.build_data
uv run --project ../diffusion_pretraining python -m ft.leakage
uv run --project ../diffusion_pretraining python -m ft.lexicon
uv run --project ../diffusion_pretraining python -m ft.constraints

# Stage 1: poem + meaning documents, starting from the pilot's EMA weights (~4 h).
uv run --project ../diffusion_pretraining python -m ft.train --stage 1 --run s1-pilot120m \
    --init-from ../diffusion_pretraining/runs/pilot120m

# Stage 2: multi-task SFT from Stage 1. Sweep lr over 3e-5 / 6e-5 / 1e-4 (1 epoch each), then 2-2.5 epochs.
uv run --project ../diffusion_pretraining python -m ft.train --stage 2 --run s2-lr6e-5 \
    --init-from runs/s1-pilot120m --lr 6e-5 --epochs 1

# Stage 3: write a poem.
uv run --project ../diffusion_pretraining python -m ft.decode --run runs/s2-lr6e-5 \
    --metre utpalamala --meaning "..." --particles 16

# Evaluation (val, 200 items): ours, ours without constraints, the retrieval baseline, the real poems.
P="uv run --project ../diffusion_pretraining python -m ft.evaluate"
$P decode --run runs/s2-lr6e-5 --split val --n 200 --out runs/s2-lr6e-5/eval/val.jsonl
$P decode --run runs/s2-lr6e-5 --split val --n 200 --free --out runs/s2-lr6e-5/eval/val_free.jsonl
$P retrieval --split val --n 200 --out data/eval/val_retrieval.jsonl
$P reference --split val --n 200 --out data/eval/val_reference.jsonl
$P score --pred runs/s2-lr6e-5/eval/val.jsonl          # repeat for each file
$P audit --pred runs/s2-lr6e-5/eval/val.jsonl --n 100   # a sheet for the hand-checked non-word audit
uv run --project ../diffusion_pretraining python -m ft.judge validate --split val --llm google/gemma-3-12b-it  # on the Spark
uv run --project ../diffusion_pretraining python -m ft.judge score --pred runs/s2-lr6e-5/eval/val.jsonl --llm google/gemma-3-12b-it

# Stage 4: one round of self-training.
uv run --project ../diffusion_pretraining python -m ft.rft generate --run runs/s2-best --n 1000 --k 8 --out data/rft/round1
uv run --project ../diffusion_pretraining python -m ft.rft build --round data/rft/round1
uv run --project ../diffusion_pretraining python -m ft.train --stage 2 --run rft1 --init-from runs/s2-best \
    --data-dir data/rft/round1 --mix '{"T1": 1.0}' --epochs 1 --lr 2e-5
```

Runs are written to `runs/<run>/`: `metrics.jsonl`, TensorBoard logs, checkpoints and
samples. Running the same command again resumes the run.

## Measured so far (2026-09-29)

- **Stage 0 data:** 367.6k train, 906 val, 5,411 test and 2,242 Test-seen poems. 303k train poems are metrical, and the metre round trip is 100%.
- **Leakage:** 3 eval poems and 297 eval meanings occur in the pretraining text (`data/leakage.json`).
- **Constraint compiler:** teacher-forced acceptance of gold poems is 99.7% (val), 99.3% (test) and 99.6% (Test-seen). The yati oracle (relaxed, sandhi hypothesis) finds 96.4% / 91.7% / 89.5% of gold yati positions in maitri, the engine's own verdict. Its predecessor, a widened out-of-context table, accepted pairs the engine rejects (PLAN §14).
- **Decoder:** about 7 s per poem at 16 particles on the laptop. On the Gemma decoding grid (37 metres × 3 topics × 5 seeds), the *base* model under the grids' strict rule set (`yati_profile="strict"`, `yati_sandhi="off"`, `prasa_relaxed=False`, `vikalpa=False`, hard yati) writes 555 / 555 poems in metre. With the defaults (soft yati, weight 3), 313 / 555 pass the relaxed profile. The poems still read as nonsense (experiments/pilot_grid/README.md).
- **Judge:** direct LaBSE similarity separates matched from mismatched val meanings with AUC 0.88 (60 items). The LLM round trip still needs a 12B+ model on the Spark.

## Known limits

- A sīsa with a long meaning (more than about 170 tokens) does not fit the 512-token canvas together with its poem.
- The samasya / makuṭam line is used in training, but the decoder does not yet force it into the poem.
- Yati is a soft constraint by default (weight 3); the engine verdict at the end is the arbiter.
- The yati oracle leaves out the lexical word context (the word is not written yet), and it does not offer the ప్రాసయతి fallback that some metres allow. Without the ప్రాసయతి fallback the decoder is stricter than the engine. A lexical blocker could in principle make it looser, but on 919 gold seats that never happened.
