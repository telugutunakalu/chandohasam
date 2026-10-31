# T5Gemma 2: bhāvam → poem as translation, metre-aware

- **Status, 2026-10-31:** done. The 270M and 1B (full) and the 4B (LoRA r 128 on attention and MLP), each one pass
  over the whole pool, are released on huggingface.co/samvaran/chandohasam. [README.md](README.md) has the commands,
  the results and the comparisons; the folder was renamed from `t5_experiments`. Not done: the test split, the 4B's
  constrained E6 val (the grid has it), a second epoch for the 270M.
- **Status, 2026-10-21 12:10:** code written and smoke-tested; all three models downloaded and verified. The 270M is
  training on the **whole T1 pool** (user decision: 300,763 poems, natural metre mix, 1 epoch ≈ 9,900 steps), sharing
  the GPU with ../lora_gemma_diffusion's constrained runs; ETA ≈ 21:00. 1B and 4B use the 48k E6-weighted set.
- **Why:** the poem and its bhāvam are parallel text, so bhāvam → poem is a translation task, and an encoder-decoder
  fits it: the encoder reads the bhāvam (and the metre) in both directions, the decoder writes the poem. The decoder is
  autoregressive, so our constrained decoder (metrical_decoder) can enforce the metre exactly at each step — which
  worked far better for the autoregressive Nandi (constrained real words 77%) than for DiffusionGemma
  (../lora_gemma_diffusion/PLAN.md §6). A strong autoregressive model writing metrical, meaningful poems can also be a
  **teacher** for our diffusion models (its poems as their training data).

## 1. Models

`google/t5gemma-2-{270m-270m, 1b-1b, 4b-4b}` (gated; downloaded 2026-10-21 with the user's token):
encoder-decoder models adapted from Gemma 3, Gemma 3's tokenizer (262,144 tokens; `<pad>` 0, `<eos>` 1, `<bos>` 2;
the decoder starts from `<bos>`). transformers' `T5Gemma2ForConditionalGeneration` (in both of our environments)
computes the loss from `labels` and shifts them itself. 270M and 1B: full fine-tuning; 4B: LoRA on the attention
projections of the encoder and decoder text layers.

## 2. Metre-aware design

- **Input (encoder):** `పని: పద్యం` (the task), the metre's Telugu name, **its rules** (metrical_decoder.prompts.
  meter_rules: lines, gaṇa sequence per line with the guru/laghu pattern, yati position, prāsa; the closing guru/laghu
  paragraph, the same for every metre, dropped), the register, the shared line (samasya/makuṭa) if any, the bhāvam.
- **Output (decoder):** the poem's lines, newline-separated, then `<eos>`.
- **Auxiliary scansion task** (`--aux 0.15`): with probability 0.15 an example is `పని: గురులఘువులు`, the metre and
  the poem → the guru/laghu pattern of each line (the strict engines' scansion). The model learns what makes an akshara
  guru or laghu in Telugu script — the metre's building block — through the same encoder and decoder.
- **ఁ and ఽ are dropped** from the text, as for DiffusionGemma (user decision 2026-10-20): Gemma's tokenizer spells
  them as raw bytes, our constrained decoder cannot write them, and neither changes the scansion (gaṇa 100%, prāsa
  99.9%, yati 98.3% unchanged on 2,089 poems). Word measures compare with ఁ stripped on both sides.
- **Inference:** free sampling (E6: temperature 0.7, top-p 0.9) and, next, constrained decoding through
  metrical_decoder with an encoder-decoder source (to write: the encoder runs once, the decoder steps with its cache).

## 3. Data

E6's T1 pool of the train split (Padyarchana minus ../dataset; poem lines, an engine-confirmed metre, a bhāvam):
48,000 poems drawn with E6's metre weights (rare metres upsampled, dvipada capped; weighted sampling without
replacement, log keys), as ../lora_gemma_diffusion, plus the scansion targets of the same poems. Validation: 200 E6 val
poems. Evaluation: the 114 E6 val prompts (then the 183 test prompts).

## 4. Training and evaluation

`train.py`: AdamW (full: lr 1e-4 for 270M, 5e-5 for 1B; LoRA r 16: 2e-4), warm-up then cosine to 10%, bf16 autocast,
batches by a token budget (padding with attention masks), gradient clipping 1.0. Every `--eval-every` steps: val loss
on the poem with the bhāvam (T1) and with an empty bhāvam (T0; T0 − T1 > 0 = the bhāvam is used), and 11 greedy poems
(one per E6 metre) scored by the strict engines. Checkpoints resumable.

`generate.py`: free poems for the 114 E6 val prompts in the E6 row format → ../lora_gemma_diffusion/score_e6.py
(chandas skill, whole poems in metre, vṛtta lines on the pattern, real words with ఁ stripped, filler, copy,
recognition, beside the MDLMs, Nandi and DiffusionGemma).

## 5. The 1B and the 4B (plan, 2026-10-21)

Parameter counts (configs, meta device): 270M = 0.79B total (vision tower 0.42B, text 0.37B); **1B = 2.12B** (vision
0.42B, text 1.70B, of which MLP 1.24B); **4B = 7.51B** (vision 0.42B, text 7.09B, of which MLP 5.35B). The names count
one stack; the totals hold the encoder, the decoder and a vision tower we never use — now frozen in bf16 at every size
(`common.freeze_vision`).

| | 1B | 4B |
|---|---|---|
| method | **full fine-tuning**, AdamW | **LoRA** r 32 on attention **and MLP** (`--lora-mlp`; 75% of the 4B is MLP) |
| why | text 1.70B × 16 bytes (fp32 weights, gradients, Adam's two moments) ≈ 27 GB + vision 0.8 GB + activations ≈ **40 GB**: fits, alone | full AdamW: 7.09B × 16 bytes ≈ **113 GB** — impossible on the 121 GB GB10. Full fine-tuning with Adafactor (`--optim adafactor`: fp32 weights + gradients ≈ 57 GB, tiny factored statistics, gradient checkpointing) ≈ 70 GB would fit only with the machine to itself, slowly; LoRA on a bf16 base (15 GB) with checkpointing ≈ 30 GB is the practical choice |
| data | the whole T1 pool (300,761, natural mix), as the 270M — a clean size comparison | the 48k E6-weighted set, as the DiffusionGemma LoRA — comparable with it; the full pool if time allows |
| lr | 5e-5, warm-up 400, cosine to 10% | 2e-4, warm-up 200 |
| options | batch 8,192 tokens | batch 8,192 tokens, `--grad-ckpt` |
| time (estimate; measured by a 30-step smoke run first) | ≈ 1.5–2.5 s/step → full pool (≈ 18,500 steps) ≈ 8–13 h | ≈ 4–6 s/step → 48k (≈ 3,000 steps) ≈ 4–5 h |
| command | `train.py --size 1b --run t5g-1b-full --data train_full --lr 5e-5 --warmup 400 --eval-every 1000 --save-every 500` | `train.py --size 4b --run t5g-4b-lora --lora 32 --lora-mlp --grad-ckpt --lr 2e-4 --warmup 200 --eval-every 500 --save-every 250` |

Each runs alone in the sequential systemd queue with the memory watchdog (§6, 10-21 12:29), then `generate.py` and
`../lora_gemma_diffusion/score_e6.py` (the T5 rows are in its table).

**More epochs for the 270M?** One epoch was chosen because Nandi (150M) over-fitted this pool after ≈ 2.5 epochs
(memorisation: 0.89 vs 1.97 nats/token on seen vs unseen poems); with one epoch no poem is seen twice. The val loss was
still falling slowly at the end (2.087 → 2.062 → 2.055 → 2.056 over the last 2,500 steps, with the rate decayed to
10%), so a second epoch might gain ≈ 0.05–0.1 nats with a memorisation risk. Decide from the E6 results:
`--init runs/t5g-270m-full/final --lr 3e-5` (a fresh short schedule), ≈ 4 h, memorisation checked after.

## 6. Log

| when | step | result |
|---|---|---|
| 10-21 11:50 | folder and code | PLAN, common, data, train, generate |
| 10-21 11:52 | downloads | 270M (1,572,182,264 bytes), 1B (4,232,105,984), 4B (4 shards: 4.96 / 4.99 / 4.96 / 0.10 GB) — sizes match the hub listing; the first attempts stalled on Xet, then on a DNS failure during a network switch; done with Xet off on the new network (≈ 21–23 MB/s) |
| 10-21 11:55 | data | 48k E6-weighted (data/train.jsonl): 95.5% with a scansion target; inputs ≈ 944 characters (the rules), poems ≈ 133; every metre has rules text |
| 10-21 12:00 | smoke test (270M, 30 steps) | 786M trainable (full; encoder + decoder + vision tower + embeddings), 3.2 s/step beside the constrained run, peak 33 GB; val T1 5.19 → 4.42, T0 − T1 +0.27 → +0.43; greedy poems still repeat lines (no `<eos>` yet) |
| 10-21 12:10 | full pool for the 270M (user: "lets go full haul") | data/train_full.jsonl: every T1-pool poem once, natural mix (dvipada 31%, not capped; rare metres not upsampled); run `t5g-270m-full` queued to start when the data is built |
| 10-21 12:29 | **system OOM** | the 270M full run (36 GB + 5.4 GB fp32 logit spikes + Python-list token ids) beside DiffusionGemma's constrained evaluation (52.7 GB) exhausted the shared 121 GB; the kernel OOM killer took VS Code (and the jobs started from it) and the annotation app (auto-restarted; DB quick_check ok). Fixes: token ids as int32 arrays, batch 8,192 tokens (peak 18 GB, RSS 4.5 GB); the run restarted from scratch (the crashed one's metrics kept in runs/crashed_2026-10-21/); all GPU jobs now in one sequential queue run as a systemd user unit with a 2-s memory watchdog (experiments/scripts/gpu_queue_2026-10-21.sh). 270M alone: 0.81 s/step, 18,473 steps, ETA ≈ 16:50 |
| 10-21 20:20 | 4B on the whole pool (user decision, ../full_grid_experiments/PLAN.md §9) | the 4B LoRA now trains on the whole T1 pool (`t5g-4b-lora-full`, one pass), keeping the adapter after its first 48,000 examples (`train.py --snapshot-at 48000` → `lora_at_48000.pt`) instead of a separate 48k run; E6 poems for both (`e6_t5g_4b_48k_val`, `e6_t5g_4b_val`). Queue: gpu-queue-1021d (experiments/scripts/gpu_queue_2026-10-21d.sh) |
| 10-21 20:55 | 4B LoRA rank 128 (user decision) | r 32 → 128 on attention + MLP: 119M → 477M trainable (6.7% of the 7.09B text parameters), ≈ +7% matmul compute, ≈ +6 GB for the adapters' weights, gradients and Adam; lr 2e-4 with α = 2r kept. Run `t5g-4b-r128-full` (whole pool, snapshot at 48k) in gpu-queue-1021d (experiments/scripts/gpu_queue_2026-10-21d2.sh) |
| 10-22 18:30 – 10-23 00:30 | constrained E6 val (beside the 4B) | 270M / 1B, masking + backtracking (v1): 114/114 in metre, real words 77.0 / 79.2%, filler 6.0 / 5.2%, first choice blocked 8 / 6%. 1B with v2 Layer A: 78.3%; with v2 A + B (padyarchana inventory + words): **83.4%** (paired +4.3, p < 0.001; held-out lexicon +9.7). Memorisation: 0% at ≥ 12 aksharas (results/t5_memorisation.md). MAUVE with ఁ stripped: 270M free 0.928, 1B free 0.885, constrained 0.891–0.924 (gold 0.922); unstripped values (0.46–0.60) were the ఁ artefact |
