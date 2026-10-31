# t5_finetuning

Fine-tunes **T5Gemma 2**, Google's encoder-decoder models adapted from Gemma 3, to write a Telugu *padyam* from a
metre and a bhāvam. The idea: a poem and its bhāvam are parallel text, so bhāvam → poem is a translation task. The
encoder reads the bhāvam and the metre's rules in both directions; the decoder writes the poem left to right, so the
project's metrical decoder can enforce the metre at every step. The design and its log are in [PLAN.md](PLAN.md).
Status 2026-10-31: three sizes trained, evaluated, and released. This folder was called `t5_experiments` until
2026-10-31.

| model | base | fine-tuning | trainable parameters | run (here) | released as |
|---|---|---|---|---|---|
| T5Gemma 2 270M | `google/t5gemma-2-270m-270m` | full | 369M (the text model) | `runs/t5g-270m-full/final` | [`t5gemma2-270m-padyam`](https://huggingface.co/samvaran/chandohasam/tree/main/t5gemma2-270m-padyam) |
| T5Gemma 2 1B | `google/t5gemma-2-1b-1b` | full | 1,699M (the text model) | `runs/t5g-1b-full/final` | [`t5gemma2-1b-padyam`](https://huggingface.co/samvaran/chandohasam/tree/main/t5gemma2-1b-padyam) |
| T5Gemma 2 4B | `google/t5gemma-2-4b-4b` | LoRA r 128, α 256, on q, k, v, o, gate, up, down of every text layer | 477M (476 projections) | `runs/t5g-4b-r128-full/lora.pt` | [`t5gemma2-4b-padyam-lora`](https://huggingface.co/samvaran/chandohasam/tree/main/t5gemma2-4b-padyam-lora) |
| T5Gemma 2 4B, first 48k | the same | the same run's adapter after its first 48,000 examples | | `runs/t5g-4b-r128-full/lora_at_48000.pt` | not released |

- **Strategy:** the 270M and the 1B are full-parameter supervised fine-tunes: every weight of the text model (encoder,
  decoder, embeddings) trains. The 4B trains LoRA adapters only, on a frozen bf16 base.
- **Names and sizes:** each name counts one stack, so the 1B holds 2.12B parameters (encoder + decoder + a vision
  tower of 417M). The vision tower never sees an image here and never changes. In the 1B and 4B runs it is frozen
  (`common.freeze_vision`). The 270M ran on an earlier `train.py` without that freeze: its tower sat in the optimizer
  but never received a gradient, so its weights are the base's and the training is the same.
- **Untrained bases:** all three are also evaluated as they are, as reference rows.
- **Licence:** the bases are under the Gemma Terms of Use, and so are the released models.

## What is where

Only code, documentation and results are in git.

| what | where | in git |
|---|---|---|
| code | `common.py`, `data.py`, `train.py`, `generate.py`, `constrained_sample.py` | yes |
| results | `results/` (numbers only, no poem text) | yes |
| training data | `data/`: the training and validation examples, built from the E6 records of `../diffusion_finetuning` (the confidential crawled corpus) | no (`.gitignore`) |
| base models | the Hugging Face cache (`google/t5gemma-2-*`, gated: accept the Gemma terms first) | no |
| fine-tuned models | `runs/t5g-*/`, released on [the Hub](https://huggingface.co/samvaran/chandohasam) | no |
| runs | `runs/`: checkpoints, generated poems (`e6_*`, `grid_*`), logs (34 GB) | no (`.gitignore`) |

## Write a poem with the released models

Free decoding (temperature 0.7, top-p 0.9), from the Hub:

```python
from huggingface_hub import snapshot_download

repo = snapshot_download("samvaran/chandohasam", allow_patterns=["t5gemma2-1b-padyam/*"])   # or -270m-, -4b-…-lora
```

```bash
cd <repo>/t5gemma2-1b-padyam
python padyam.py --metre utpalamala --bhavam "ఓ రామా! నీ నామమే నాకు రక్ష. నిన్ను ఎల్లప్పుడూ స్మరిస్తాను."
python padyam.py --metre కందము --bhavam-file bhavam.txt --n 3
python padyam.py --list-metres
```

Time for the first command, with loading, on one GPU: 270M ≈ 13 s, 1B ≈ 24 s, 4B ≈ 100 s. The 4B adapter needs its
gated base: accept the Gemma terms on `google/t5gemma-2-4b-4b`, then `huggingface-cli login`. Its `padyam.py`
downloads the base (15 GB) on first use. Each folder's card gives the encoder input and the adapter format.

**In metre**, with the metrical decoder: `constrained_sample.py` (and `generate.py`) take either the run's weights or
the downloaded release.
- `--model <repo>/t5gemma2-1b-padyam`: the same files as `runs/t5g-1b-full/final`.
- `--lora <repo>/t5gemma2-4b-padyam-lora/adapter.safetensors --r 128 --lora-mlp`: the same tensors as `lora.pt`.

They also need the E6 records and an MDLM reference run, so they run only where `../diffusion_finetuning` has been
built:

```bash
cd t5_finetuning
../.venv/bin/python -u constrained_sample.py --size 1b --model <repo>/t5gemma2-1b-padyam --name e6_t5g_1b_hub_val \
    --modes masking_backtrack                      # 114 val prompts → runs/e6_t5g_1b_hub_val/, results/e6_t5g_1b_hub_val.md
```

## How the models were trained

### Input and output (`common.py`)

- **Encoder input:** the task, the metre, the metre's rules (`metrical_decoder.prompts.meter_rules`; the paragraph
  common to every metre dropped), the register, an optional shared line (samasya / makuṭam), the bhāvam:

```
పని: పద్యం
ఛందస్సు: ఉత్పలమాల
Meter: ఉత్పలమాల (utpalamala), a vrutta meter.
Lines (పాదాలు): 4.
Every line: 7 gaṇas: భ ర న భ భ ర వ, i.e. UII UIU III UII UII UIU IU (20 aksharas)
Yati (యతి): in every line the 1st akshara must be in yati-maitri (harmony of the first sound) with the 10th akshara.
Prāsa (ప్రాస): the 2nd akshara of every line must carry the same consonant, and the 1st akshara must have the same weight (guru or laghu) in every line.
శైలి: ప్రాచీన
భావం: <the bhāvam>
```

- **Decoder output:** the poem, one pāda per line, then `<eos>`.
- **Auxiliary scansion task:** 15% of the examples are given instead as `పని: గురులఘువులు`, the metre and the poem →
  each line's guru/laghu pattern from the strict engines. It teaches what makes an akshara heavy or light.
- **ఁ and ఽ are dropped** everywhere. Gemma's tokenizer spells them as raw bytes, the constrained decoder cannot write
  them, and they change no scansion (gaṇa 100%, prāsa 99.9%, yati 98.3% unchanged on 2,089 poems). Word measures
  strip ఁ on both sides.

### Data (`data.py --n 0 --name train_full`)

- **Source:** E6's meaning → poem pool from `../diffusion_finetuning`: the 300,763 training poems with an
  engine-confirmed metre and a bhāvam. The four `dataset/` works are held out whole, as for every model of the
  project.
- **Train:** every poem once, in a seeded order, at the natural metre mix (dvipada 31%; nothing up-sampled). Two
  poems exceed the length limits (source 1,024, target 320 tokens), leaving **300,761**. 290,229 of them also have a
  scansion target.
- **Lengths:** inputs average 905 characters (mostly the rules), poems 116.
- **Validation:** 200 E6 val poems, each also with an empty bhāvam (T0) to measure how much the bhāvam is used.

`data.py --n 48000` writes a 48k sample drawn with E6's metre weights (`data/train.jsonl`). Only the first 4B attempt
used it, and that attempt was replaced.

### Recipe (`train.py`): one pass, 18,473 steps of up to 8,192 tokens

| | 270M | 1B | 4B |
|---|---|---|---|
| method | full fine-tuning of the text model's 369.2M parameters | full fine-tuning of the text model's 1,699.1M parameters | LoRA r 128, α 256, dropout 0, on q, k, v, o, gate, up, down of all 34 encoder and 34 decoder text layers (476 adapters, 476,839,936 parameters; A Kaiming-uniform, B zero); frozen bf16 base; gradient checkpointing |
| weight precision | encoder stack and shared embedding bf16 (bf16 AdamW moments), decoder layers fp32 | the same: 999.9M bf16, 697.9M fp32 | bf16 base, fp32 adapters |
| learning rate, warm-up | 1e-4, 400 | 5e-5, 400 | 2e-4, 400 |
| peak GPU memory | 21 GB | 50 GB | 31 GB |
| wall time (mean s/step × steps) | ≈ 4.4 h | ≈ 12.4 h | ≈ 49.5 h |
| val T1 loss, step 0 → end (nats per Gemma token) | 5.186 → **2.056** | 4.725 → **1.776** | 3.929 → **2.003** |
| val T0 − T1 (the bhāvam's value), step 0 → end | 0.27 → 0.90 | 0.26 → 1.07 | 0.45 → 0.91 |

All three runs share the same settings:
- loss: sequence-to-sequence cross-entropy on the target and its `<eos>`, the mean over label tokens;
- AdamW (β 0.9, 0.98, eps 1e-8; weight decay 0.01 on matrices for full fine-tuning, 0 for the adapters), linear
  warm-up then cosine to 10%;
- batches cut from the length-ordered data at 8,192 padded source + target tokens (≈ 16 examples), one optimizer step
  each, no gradient accumulation;
- bf16 autocast, gradient clipping 1.0, seed 20261021, TF32; no EMA (the released weights are the last step's);
- the scansion task replaces 15% of the examples that have a scansion target (≈ 14.5% of all examples);
- evaluation every 1,000 steps: val loss, plus one greedy poem per E6 metre scored by the engines.

The full fine-tunes asked for fp32 weights (`train.py` loads them with `dtype=torch.float32`), but the trained
checkpoints hold the encoder stack and the shared embedding in bf16, with bf16 optimizer moments; only the decoder
layers are fp32 (`last.pt`, `final/model.safetensors`). The released files keep these dtypes.

The runs went one at a time on the GB10 through the GPU queues `../experiments/scripts/gpu_queue_2026-10-21*.sh`,
systemd user units with a memory watchdog. The 4B moved from r 32 to r 128 on 10-21 (the user's decision; `PLAN.md` §6).

### Commands

```bash
cd t5_finetuning
P=../.venv/bin/python
$P -u data.py --n 0 --name train_full                    # data/train_full.jsonl + data/val.jsonl (needs the E6 records)
$P -u train.py --size 270m --run t5g-270m-full --data train_full --epochs 1 --warmup 400 --eval-every 1000 --save-every 500
$P -u train.py --size 1b --run t5g-1b-full --data train_full --lr 5e-5 --warmup 400 --eval-every 1000 --save-every 500
$P -u train.py --size 4b --run t5g-4b-r128-full --data train_full --lora 128 --lora-mlp --grad-ckpt --lr 2e-4 \
    --warmup 400 --eval-every 1000 --save-every 250 --snapshot-at 48000
# E6 val (114 prompts): free poems, then the metrical decoder (v1; v2 Layer A; v2 A + B)
$P -u generate.py --size 270m --model runs/t5g-270m-full/final --name e6_t5g_270m_val              # ≈ 3 min
$P -u generate.py --size 4b --lora runs/t5g-4b-r128-full/lora.pt --r 128 --lora-mlp --name e6_t5g_4b_val
$P -u generate.py --size 4b --lora runs/t5g-4b-r128-full/lora_at_48000.pt --r 128 --lora-mlp --name e6_t5g_4b_48k_val
$P -u constrained_sample.py --size 1b --model runs/t5g-1b-full/final --name e6_t5g_1b_val_c --modes masking_backtrack
$P -u constrained_sample.py --size 1b --model runs/t5g-1b-full/final --name e6_t5g_1b_val_c_invpad \
    --modes masking_backtrack --inventory padyarchana                                                # v2 Layer A
$P -u constrained_sample.py --size 1b --model runs/t5g-1b-full/final --name e6_t5g_1b_val_c_v2 --modes masking_backtrack \
    --inventory padyarchana --attest-weight 2 --attest-where all --attest-corpus padyarchana           # v2 A + B
```

Every step resumes. The paper's grid runs `constrained_sample.py` from `../full_grid_experiments/grid.py` (rows
`t5_270m_*`, `t5_1b_*`, `t5_4b_*`, `t5_4b_48k`), which writes `results/grid_t5_*`.

## Results

### E6 validation set (114 prompts; `../lora_gemma_diffusion/results/e6_comparison.md`)

Each val poem's own metre and bhāvam is a prompt, one poem per prompt (seed 42). The T5 rows sit beside every other
model of the project, all scored by one script (`../lora_gemma_diffusion/score_e6.py`, using `../RL/reward.py`'s
definitions; real words with ఁ stripped). Constrained = masking + backtracking, strict profile.

| set | in metre | chandas skill (mean) | vṛtta lines on the gaṇa pattern | real words | one-akshara words | copy | recognised | a line repeated |
|---|---|---|---|---|---|---|---|---|
| *gold (the real poems)* | 39.5% | 0.96 | 98.6% | 86.8% | 7.0% | 2.5% | 78.1% | 0.0% |
| **T5Gemma 2 270M, free** | 8.8% | 0.89 | 74.3% | 80.4% | 5.9% | 2.7% | 77.2% | 0.0% |
| **T5Gemma 2 270M, constrained** | 100% | 1.00 | 100% | 77.0% | 6.0% | 3.2% | 83.3% | 0.0% |
| **T5Gemma 2 1B, free** | 6.1% | 0.90 | 77.1% | 82.5% | 5.8% | 3.0% | 77.2% | 0.9% |
| **T5Gemma 2 1B, constrained** | 100% | 1.00 | 100% | 79.2% | 5.2% | 2.4% | 79.8% | 0.0% |
| **T5Gemma 2 1B, constrained, v2 Layer A** | 100% | 1.00 | 100% | 78.3% | 5.6% | 2.2% | 79.8% | 0.0% |
| **T5Gemma 2 1B, constrained, v2 A + B** | 100% | 1.00 | 100% | **83.4%** | 4.6% | 3.3% | 79.8% | 0.0% |
| **T5Gemma 2 4B LoRA, first 48k, free** | 0.0% | 0.52 | 14.7% | 76.4% | 5.8% | 3.9% | 67.5% | 0.0% |
| **T5Gemma 2 4B LoRA, free** | 7.9% | 0.87 | 68.2% | 81.0% | 5.5% | 2.5% | 77.2% | 0.9% |
| *MDLM 120M, free / constrained* | 0.0% / 100% | 0.52 / 1.00 | 11.6% / 100% | 90.0% / 81.1% | 8.6% / 11.4% | 6.2% / 2.9% | 86.0% / 76.3% | 0.0% / 0.0% |
| *MDLM 523M, free / constrained* | 0.0% / 100% | 0.67 / 1.00 | 34.6% / 100% | 88.3% / 83.1% | 8.4% / 10.3% | 5.7% / 3.1% | 85.1% / 81.6% | 0.0% / 0.0% |
| *Nandi-Mini-150M, free / constrained* | 3.5% / 100% | 0.88 / 1.00 | 76.4% / 100% | 79.5% / 76.6% | 7.5% / 8.0% | 1.8% / 1.5% | 74.6% / 74.6% | 0.0% / 0.0% |
| *DiffusionGemma LoRA, whole pool, free* | 0.0% | 0.07 | 0.0% | 80.2% | 4.3% | 13.9% | 95.6% | 0.0% |

- **In metre:** gaṇa, prāsa and yati under the strict profile.
- **Chandas skill:** 1 − the share of aksharas that would need changing to reach the metre, against unmetered prose (1
  = in metre).
- **Copy:** the share of the poem's words of two or more aksharas that also occur in its bhāvam.
- **Recognised:** LaBSE ranks the poem's own bhāvam first among 10. It is a topic signal, not a judgement of meaning.

The metrical decoder's own report on the constrained T5 runs (`results/e6_t5g_*_val_c*.md`):

| run | model's first choice overridden | model's mass on allowed tokens | words in the corpora | backtracks per poem |
|---|---|---|---|---|
| 270M | 8% | 0.909 | 43% | 5.5 |
| 1B | 6% | 0.921 | 44% | 5.8 |
| 1B, v2 Layer A | 5% | 0.941 | 45% | 2.9 |
| 1B, v2 A + B | 6% | 0.929 | 52% | 4.3 |

For comparison on the same prompts (`../diffusion_finetuning`): the MDLM 120M's first choice is overridden 19% of
the time and the 523M's 12%; Nandi's 7%.

### MAUVE (E6 val; ఁ and ఽ stripped on every side; `../metrics/mauve_padyarchana/report_more_stripped.md`)

Distribution similarity to the crawled training corpus (metre-matched), and to the gold poems of the same prompts;
mean of 5 seeds.

| set | vs the training corpus | vs the gold poems |
|---|---|---|
| *gold val* | 0.922 | 1.000 |
| T5Gemma 2 270M, free / constrained | 0.928 / 0.891 | 0.973 / 0.981 |
| T5Gemma 2 1B, free / constrained | 0.885 / 0.896 | 0.965 / 0.978 |
| T5Gemma 2 1B, constrained v2 Layer A / A + B | 0.924 / 0.843 | 0.988 / 0.950 |
| T5Gemma 2 4B LoRA, free (`../paper/analysis/mauve_val_extra.json`) | | 0.940 |
| *MDLM 523M, free / constrained* | 0.845 / 0.885 | 0.941 / 0.953 |
| *Nandi-150M, free / constrained* | 0.910 / 0.921 | 0.940 / 0.978 |

### Memorisation (`results/t5_memorisation.md`; `../diffusion_finetuning/memorisation.py` against the 365,679 E6 training poems)

The share of poems whose longest run of aksharas shared with any one training poem reaches N, and the share of their
lines found verbatim in a training poem. A run of 6–8 aksharas is a common phrase; a vṛtta line is about 20.

| run | poems | run ≥ 6 | run ≥ 8 | run ≥ 12 | verbatim lines |
|---|---|---|---|---|---|
| 270M, free | 114 | 63.2% | 4.4% | **0.0%** | 0.0% |
| 270M, constrained | 114 | 57.9% | 1.8% | **0.0%** | 0.0% |
| 1B, free | 114 | 67.5% | 6.1% | **0.0%** | 0.0% |
| 1B, constrained | 114 | 65.8% | 5.3% | **0.0%** | 0.0% |
| 1B, constrained v2 A + B | 114 | 61.4% | 3.5% | **0.0%** | 0.0% |
| 4B LoRA, free | 114 | 67.5% | 0.9% | **0.0%** | 0.0% |
| 4B LoRA first 48k, free | 114 | 59.6% | 1.8% | **0.0%** | 0.0% |
| *MDLM 523M, free / constrained* | 114 | 79.8% / 61.4% | 7.9% / 0.9% | 0.0% / 0.0% | 0.0% / 0.0% |

No T5 poem shares 12 aksharas with a training poem or copies a line. One pass over the pool means no training poem
was seen twice.

### The paper's grid (100 prompts; `../full_grid_experiments/results/grid.json`)

One poem per prompt and decoding (seed 42), on the prompts of `../diffusion_finetuning/README.md`. v2 adds attested
syllables and a real-word preference to the decoder.

| model | decoding | in metre (strict) | vṛtta lines on the gaṇa pattern | real words | recognised (1 of 10) | one-akshara words | a line repeated |
|---|---|---|---|---|---|---|---|
| 270M base | free / constrained / v2 | 0% / 100% / 100% | 0.0% / 100% / 100% | 84.4% / 39.0% / 49.9% | 33% / 25% / 27% | 23.9% / 11.6% / 6.3% | 11% / 30% / 42% |
| **270M fine-tuned** | free / constrained / v2 | 8% / 100% / 100% | 78.2% / 100% / 100% | 79.5% / 75.3% / **82.9%** | 75% / 64% / 66% | 4.2% / 4.4% / 4.8% | 1% / 1% / 2% |
| 1B base | free / constrained / v2 | 0% / 100% / 100% | 0.0% / 100% / 100% | 88.8% / 39.1% / 50.2% | 38% / 31% / 22% | 27.7% / 9.9% / 5.0% | 19% / 17% / 26% |
| **1B fine-tuned** | free / constrained / v2 | 8% / 100% / 100% | 73.4% / 100% / 100% | 82.8% / 74.1% / **82.3%** | 75% / 66% / 72% | 4.1% / 5.3% / 4.6% | 1% / 1% / 1% |
| 4B base | free / constrained / v2 | 0% / 100% / 100% | 0.0% / 100% / 100% | 95.0% / 38.0% / 45.1% | 26% / 28% / 25% | 75.4% / 12.0% / 5.7% | 1% / 29% / 37% |
| 4B LoRA, first 48k | free / constrained / v2 | 0% / 100% / 100% | 10.1% / 100% / 100% | 77.4% / 63.1% / 71.6% | 65% / 42% / 44% | 5.7% / 7.3% / 5.9% | 1% / 0% / 1% |
| **4B LoRA** | free / constrained / v2 | 7% / 99% / 100% | 64.9% / 100% / 100% | 80.6% / 72.8% / **79.7%** | 71% / 63% / 70% | 4.9% / 6.2% / 5.3% | 0% / 0% / 0% |
| *MDLM 523M fine-tuned* | free / constrained / v2 | 1% / 99% / 100% | 39.4% / 100% / 100% | 89.0% / 77.5% / 85.4% | 80% / 77% / 76% | 6.2% / 10.6% / 6.9% | 1% / 2% / 3% |
| *Nandi fine-tuned* | free / constrained / v2 | 5% / 100% / 100% | 77.1% / 100% / 100% | 80.4% / 73.0% / 79.1% | 65% / 64% / 61% | 5.5% / 6.7% / 5.9% | 2% / 0% / 0% |
| *the 100 source poems* | | 53% | 95.7% | 85.7% | 63% | 5.0% | 0% |

No fine-tuned T5 grid poem copies a training line or 12 aksharas of its source poem. The 270M and 1B bases' free poems
copy a training line in 1% of cases.

### What the results say

- **The bhāvam is used, more as the model grows.** The val gap T0 − T1 is 0.90 nats for the 270M and 1.07 for the 1B.
- **The full 1B fits best.** It has the lowest val loss (1.776). On E6 its constrained poems have 79.2% real words,
  and 83.4% with v2 A + B, close to the gold poems' 86.8%. Under the decoder its first choice is overridden only 6%
  of the time. On the grid the three fine-tuned sizes are within 3 points of each other on real words.
- **The 4B LoRA does not beat the full 1B.** Its val loss ends at 2.003, between the 270M and the 1B. Its first 48k
  examples alone are far behind (free poems 15% on the gaṇa pattern, recognised 42% constrained), so the whole pool
  mattered.
- **Encoder-decoders learn the rhythm.** Free T5 poems put 68–77% of their vṛtta lines on the gaṇa pattern and 6–9%
  pass the strict check, like Nandi (76%) and unlike the MDLMs (12–35%).
- **Their words are a little less real than the MDLMs'.** On the grid, v1 real words are 73–75% against the 523M's
  78%, and recognition is lower (63–66% against 77%). v2 closes most of the gap (80–83% against 85%).
- **They read like the corpus.** MAUVE against the training corpus is 0.89–0.93 for the free and v1 poems, at the
  gold poems' own level (0.92). The v2 A + B poems drop to 0.84.
- **No copying:** see the memorisation table.

## Scripts

Every script runs from this folder with `../.venv/bin/python`, and every step resumes.

| script | purpose | reads | writes |
|---|---|---|---|
| `common.py` | The shared library (no command line). `MODELS` (the three Hub ids); `source_text` / `target_text` (encoder input, poem); `rules` (the metre's rules text); `scansion_source` / `scansion_target` (the auxiliary task); `t1_pool` / `read_records` (E6 records); `load` (a base from the HF cache or a `save_pretrained` folder); `freeze_vision`; `inject_lora` / `LoRALinear` / `lora_state` / `load_adapter` (the LoRA adapters, from `lora.pt` or the released `adapter.safetensors`) | E6 records, the HF cache | |
| `data.py` | Builds the training and validation examples as text, tokenised at training time, so one build serves every size. `--n 0`: the whole pool at its natural mix; `--n 48000`: an E6-weighted sample | `../diffusion_finetuning/data/e6/records` | `data/<name>.jsonl`, `data/val.jsonl`, `data/stats_<name>.json` |
| `train.py` | Fine-tunes one size (full or LoRA) on bhāvam → poem with the auxiliary scansion task. Evaluates val loss (T1, T0) and greedy poems every `--eval-every` steps; resumable checkpoints; `--snapshot-at N` keeps the adapter after N examples | `data/` | `runs/<run>/`: `metrics.jsonl`, `last.pt`, `final/` or `lora.pt` |
| `generate.py` | Free poems (temperature 0.7, top-p 0.9) for the E6 prompts, the (metre, poem id) pairs of an MDLM reference run, in the E6 row format | a model or adapter, E6 records, `../diffusion_finetuning/runs/<reference>` | `runs/<name>/results.jsonl` (scored by `../lora_gemma_diffusion/score_e6.py`) |
| `constrained_sample.py` | The metrical decoder with T5Gemma (`T5Source`: the encoder runs once, the decoder steps with its cache, rollback replays). Free and constrained modes, v2 layers (`--inventory`, `--attest-*`), the same prompts and token budgets as the MDLM rows | the same, plus `meter_engine/metrical_decoder` | `runs/<name>/` (poems, traces), `results/<name>.{md,json}` |

Scripts elsewhere that produced this folder's results:
- `../diffusion_finetuning/memorisation.py`: copying from training poems.
- `../lora_gemma_diffusion/score_e6.py`: the cross-model E6 table.
- `../metrics/mauve_padyarchana/score_more.py`: MAUVE.
- `../full_grid_experiments/grid.py`: the grid cells.
- `../experiments/scripts/gpu_queue_2026-10-21*.sh`: the training queues.

## Results files

| file | what |
|---|---|
| `results/e6_t5g_{270m,1b}_val_c.{md,json}` | the decoder's report on the constrained E6 val poems |
| `results/e6_t5g_1b_val_c_invpad.*`, `…_v2.*` | the same with v2 Layer A, and with Layer A + B |
| `results/t5_memorisation.md`, `results/e6_t5g_*_memorisation.{md,json}` | memorisation of every E6 run |
| `results/grid_t5_*` | the grid's T5 cells: `free` and `constrained` on the 80 prompts reused from the earlier test set (plain) and on the 20 new ones (`_new`: 10 Vemana, 10 Gemini), `_v2` on all 100, and `_smoke` checks |
| `results/smoke_c.*` | the first smoke test of `constrained_sample.py` (2 poems) |

## Known limits and open items

- **No test-split evaluation.** The plan's 183 test prompts were never run for T5. The val set (114) and the grid
  (100) are the evaluations.
- **The 4B's constrained E6 val** was not run; the grid has its constrained and v2 cells.
- **A second epoch for the 270M** (PLAN.md §5) was not tried.
- **ఁ and ఽ cannot be written**: they are dropped from training and from the decoder's vocabulary.
- **The rules text is in English** inside a Telugu prompt, as `metrical_decoder` writes it.
- **Untested inputs:** the modern register and the samasya / makuṭam line were trained but never evaluated, as for
  the other models.
