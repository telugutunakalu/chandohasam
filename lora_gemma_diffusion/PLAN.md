# LoRA fine-tuning of DiffusionGemma 26B-A4B on Padyarchana (meaning → poem)

- **Status, 2026-10-31:** done. After this log: the whole-pool adapter (`runs/lora-full`, 300,762 poems, one pass,
  10-24 → 10-28) is the grid's DiffusionGemma row and is staged for the Hugging Face release; its E6 free poems are
  in `results/e6_comparison.md`. Memorisation of every E6 run: `results/memorisation.md`. [README.md](README.md) has the
  method, commands and results. Dropped (10-28): the 24k constrained run and the September trial rerun.
- **Status, 2026-10-21 03:40:** training done (`lora-48k`: val poem loss −59% vs base; T0−T1 at t = 1 doubled). The
  first E6 run exposed a NaN-entropy bug in our shared diffusion decoder (§6); fixed locally in evaluate_e6.py. Free
  (native) E6 for 48k / 24k / base, then constrained (fixed + settled) for 48k, queued (`run_eval2.sh`).
- **Why:** the RL trials on the 120M/150M models (../RL/PLAN.md §8–9) did not teach metre by default and no automatic
  measure could reward meaning; the most likely route to *meaningful* poems is a large pretrained model that already
  knows Telugu, fine-tuned on our corpus. The user requires a **diffusion** model (2026-10-19): DiffusionGemma.
- **Question:** does LoRA on DiffusionGemma, trained on the E6 meaning → poem task, write better poems than our MDLMs
  and Nandi — in metre (free and constrained), with real words and less filler — under the E6 evaluation?

## 1. The model and its weights

- `nvidia/diffusiongemma-26B-A4B-it-NVFP4` (on disk, 18 GB), loaded by
  `../meter_engine/metrical_decoder/diffusion/loader.py` into transformers' `DiffusionGemmaForBlockDiffusion` with
  the experts decoded once to BF16 (`resident`, ~52 GB). NVIDIA quantised **only the MoE experts**: attention, dense MLP,
  router, norms, embeddings and self-conditioning are Google's BF16 weights. The BF16 original
  (`google/diffusiongemma-26B-A4B-it`, 51.7 GB) does not download here (the hub CDN stalls at 0 bytes, 2026-10-19) and
  is not needed: LoRA trains on the exact attention weights, the experts stay frozen (the QLoRA recipe).
- Architecture (model card): block diffusion. An autoregressive **encoder** caches the prompt; a **decoder** denoises a
  **256-token canvas** with bidirectional attention over the canvas and the cached prompt. A canvas starts as uniform
  random tokens; each pass predicts every position, sees the previous pass's prediction (**self-conditioning**), keeps
  the confident tokens and returns the rest to uniform noise. Encoder layer *i* and decoder layer *i* share weights.
- Our poems (≈ 100–200 Gemma tokens) fit in one canvas: the reply is one block.

## 2. Training (what we reconstruct; the model card gives no training recipe)

- **Example:** the T1 prompt (metre, register, [shared line], bhāvam, one instruction line) in the chat template with
  thinking off and the model's empty thinking channel prefilled (as our decoder prompts it), the poem in the canvas:
  the poem's tokens, the end-of-turn token, then the model's own end-of-reply fill to 256 (read from its own
  generations in step 1).
- **Corruption:** t ~ U(0, 1); each canvas position is replaced by a uniform random token with probability t (the
  model's own start and renoising are uniform tokens).
- **Self-conditioning:** for half of the examples, a first pass without gradient gives logits that the second pass
  sees as self-conditioning (`self_conditioning_logits`; transformers' docstring: "enabled per example with some
  probability" in training); the loss is on the second pass. Otherwise one pass without it.
- **Loss:** cross-entropy of the clean canvas at every position (the decoder predicts every position).
- **LoRA:** rank 16, α 32, on the attention projections (q, k, v, o); one adapter per tied encoder/decoder pair; base
  weights frozen; gradients reach the lower layers through the frozen experts (`F.grouped_mm` backpropagates to its
  input: checked 2026-10-20).
- **Data:** the E6 train split's T1 pool (Padyarchana minus ../dataset), ~20–30k poems sampled with E6's metre weights;
  validation: E6 val poems at fixed noise levels.
- **Optimisation:** AdamW on the LoRA parameters, lr 1e-4, warm-up, cosine; one example per forward with gradient
  accumulation (effective batch 8), decoder gradient checkpointing, bf16.

## 3. Gates before the full run

1. **Loss check (untouched model):** on val poems, the loss with the matching prompt must be clearly lower than with
   another poem's prompt and than on a word-shuffled poem, at every noise level. If not, our objective does not match
   the model's training and is fixed before anything is trained.
2. **One-call = inference path:** the training call (prompt + canvas in one forward) gives the same logits as the
   decoder's encode-then-denoise path.
3. **Smoke run** (~200 steps): val loss falls; poems generated with the adapter are sane Telugu.

## 4. Evaluation (E6 protocol, base vs LoRA)

Free generation (the model's own sampler) and constrained decoding (masking + backtracking, our diffusion decoder)
on the 114 E6 val prompts; then test. Measures as ../RL: chandas skill, whole poems in metre (strict engines), vṛtta
lines on the pattern, real words v2, one-akshara words, recognition, copy, memorisation, MAUVE; human rating sample.

## 5. Timeline (target)

| day | work |
|---|---|
| Oct 20 | step 1 checks; data; training code; gates 1–2 |
| Oct 21 | smoke run (gate 3); full run overnight (~6–10 h, the GPU alone) |
| Oct 22–23 | E6 evaluation base vs LoRA, free and constrained |
| Oct 24+ | human rating; write-up |

Runs, data and caches (Padyarchana-derived, generated text, adapters) are gitignored.

## 6. Log

| when | step | result |
|---|---|---|
| 10-20 01:05 | gradients through the frozen NVFP4 experts | `F.grouped_mm` backpropagates to its input (rel. error 0.3%, bf16): no custom backward needed |
| 10-20 01:10 | step 1, first run | loads in 55 s, 51.8 GB; the base model's replies are chatty (intro, **పద్యం:** header, free verse, analysis) and run past one canvas. **Gate 2 failed** (max logit difference 6.8, argmax agreement 90%): transformers' encoder builds its causal masks and discards them (`self.create_masks_for_generate(...)` unassigned), so a one-call forward encodes the prompt without them |
| 10-20 01:25 | step 1, second run | training forward = the decoder's path (explicit masks and positions): **gate 2 passed** (difference 0.0, agreement 100%). End of a reply (a one-word answer): the reply then `<eos>` to the end of the block. **Gate 1 passed**: poem-position loss matched / word-shuffled / other prompt = 1.49 / 1.77 / 1.84 (t 0.25), 3.38 / 3.66 / 4.09 (0.5), 5.57 / 5.72 / 6.40 (0.75). LoRA r 16 on q/k/v/o of the language layers: 115 shared adapters, 11.5M parameters, 1.2–1.4 s per example, peak 56 GB |
| 10-20 01:35 | data | 24,000 training poems (E6 metre weights, weighted sampling without replacement; the first build's keys underflowed and followed file order — fixed with log-keys), 200 val |
| 10-20 08:28 | smoke run 1 (200 steps) | val poem loss −49 / −40 / −35% (t 0.25 / 0.5 / 0.75) — but **gate 3 failed on the samples**: broken byte sequences (`����`) and runs of `ఁఁఁ`. Gemma has no token for arasunna ఁ (1.3% of the poems' characters, 8.6% of poem tokens as raw bytes, in 64% of poems); parallel denoising breaks the 3-byte groups apart. Fix: ఁ → Devanagari candrabindu ँ and ఽ → ऽ (one token each, separate next to Telugu), mapped back on decoding; ఁ is weightless in the scansion. Raw-byte tokens 8.6% → 0.007% |
| 10-20 08:50 | ఁ: stand-in → dropped (user decision) | dropping ఁ (and ఽ) leaves the strict verdicts unchanged on 2,089 poems with ఁ: gaṇa 100%, prāsa 99.9%, yati 98.3% (36 poems lose a nasal yati match); 20% of words lose it (60% at the word end, e.g. పదంబుఁ → పదంబు). The constrained decoder could not write ఁ anyway (raw-byte tokens are outside its slice). Word measures compare with ఁ stripped on both sides, for every model. The stand-in smoke run (step 30) was stopped. Data rebuilt: 48,000 poems (the full run can use 24k or 48k), raw-byte tokens 0.010% |
| 10-20 09:28 | smoke run 3 (ఁ dropped, 200 steps) | val poem loss 1.83 → 0.99 / 3.56 → 2.28 / 5.41 → 3.95 (t 0.25 / 0.5 / 0.75). Samples: **clean Telugu, no byte garbage** (gate 3 passed) — but after 1,600 poems the form is far from verse: the bhāvam's content, often as modern prose cut into lines (some classical forms: హరిస్తయెన్, ముల్), messy line counts (2–9), a few lines starting mid-akshara, gaṇa 0/11. Whether more data teaches the verse form is what the full run tests |
| 10-20 09:30 | full run started (user: "start the LoRA training") | `train.py --run lora-48k --epochs 1 --eval-every 250 --save-every 100 --snapshot-at 3000` |
| 10-20 18:00 | 24k snapshot | `lora_step_3000.pt`; val poem loss at steps 1,000 / 2,000 / 3,000: 0.856 / 0.814 / 0.779 (t 0.25), 2.098 / 2.005 / 1.932 (0.5), 3.809 / 3.694 / 3.626 (0.75): still improving |
| 10-20 18:40 | evaluation code | `val_metrics.py` (integrated loss over 8 noise levels, T1 vs T0 with an empty bhāvam, per metre; base = adapter with B = 0, one load) and `evaluate_e6.py` (our diffusion decoder unchanged, E6 pairs and enforcement; `T1Canvas` maps the runner's topic = poem id to the T1 prompt); wiring tested on the CPU with the random-logit canvas (prompt lookup, baseline, masking + backtracking: a complete kandamu in metre). Queued: `run_eval.sh` (after training: val metrics → E6 48k → base → 24k) |
| 10-21 02:23 | full run done | val poem loss (t 0.25 / 0.5 / 0.75): base 1.826 / 3.565 / 5.408 → 24k 0.779 / 1.932 / 3.626 → 48k 0.743 / 1.878 / 3.576 |
| 10-21 02:54 | val diagnostics (results/val_metrics.md) | integrated loss base 4.10 → 24k 2.60 → 48k 2.55; T0 − T1 at t = 1.0: +0.19 → +0.43 → +0.50 (the adapters lean on the bhāvam more when writing from noise); every metre ≈ −45% |
| 10-21 03:00 | E6, original decoder (kept: runs/e6_dg_48k_val_original, 36 rows) | constrained poems in metre but **akshara soup**; free poems short and broken. Trace: 96–99.8% of the mass on allowed tokens, entropy 3–5 nats at the commits |
| 10-21 03:20 | **bug in the shared decoder** (metrical_decoder/diffusion/canvas.py, Sept 25 on) | with `forbid_end` the end tokens' scaled logits are −inf, so CanvasPass's −Σ p log p is **NaN** at every position (0 · −inf): every entropy comparison is False — the canvas keeps no prediction (the draft returns wholly to noise each pass) and the entropy bound never stops a run of proposals, so runs of first-pass guesses were committed. The September DiffusionGemma constrained grids ran with it. Fixed **locally** (evaluate_e6.FinitePass / T1Canvas.denoise: 0 · log 0 = 0); the shared package is untouched pending the user's decision |
| 10-21 03:30 | fixed canvas + settled commit (11-poem test) | the left edge settles in 3–4 passes (entropy 2.94 → 0.35 → 0.003); the draft grows as Telugu; constrained poems become partly meaningful and on topic (āṭaveladi: భాగవతమును … చెప్పలేరు … త్రిశూల్ … పదమభవుని) with junk fragments where the metre forces syllables; 130–212 s per poem (488–795 passes, up to 30 backtracks) |
| 10-21 03:55 | fixed + settled, 11 poems (1 per metre) | 11/11 in metre; 196 s per poem (68–310); 8/11 hit the 30-backtrack limit. Jāti metres keep some words and the bhāvam's topic; the vṛttas are mostly junk: repeated nonsense lines (mattebha, mattakōkila), runs of dead-consonant filler 'న్న్న్లన్' that the orthography allows (≤ 3 viramas) and the scansion accepts (śārdūla, utpalamāla), cluster gibberish (mālini). With the bug fixed the decoder behaves as designed; for long vṛttas the metre and the model's wording still collide, backtracking runs out and the constraint fills with what scans. Queued: free (native) 48k / 24k / base, then constrained 48k (~6 h) |
| 10-21 09:45 | free E6 (native sampler), first comparison (results/e6_comparison.md) | DiffusionGemma's free poems are weak: chandas skill median base −0.87 → 24k −0.57 → 48k −0.48 (worse than prose; MDLM 523M 0.71, Nandi 0.92), vṛtta lines on the pattern 0%, real words (ఁ stripped) base 92.3% (fluent modern prose) → LoRA 68–70% (attempted archaic forms; MDLMs 88–90%, Nandi 79.5%), **copy from the bhāvam ~20%** (gold 2.5%), 3.1–3.2 lines per poem. The LoRA moved free generation toward metre but far less than the MDLMs/Nandi. Suspect beyond training: the native sampler stops at 48 passes, so a poem that has not settled is filled in parallel (non-words); more passes is the cheap test once the GPU is free. User decisions (10-21): fix the shared decoder and rerun the September trial; constrained E6 for base and 24k too → `run_eval3.sh` (after the 48k constrained run: patch + decoder tests → base → 24k → September trial, 111 poems) |
| 10-21 12:29 | **system OOM** (my scheduling error: this evaluation, 52.7 GB, ran beside the T5Gemma 270M training) | the kernel OOM killer took VS Code and with it the evaluation chain; constrained base had 22 poems (resumable per metre). Resumed in the sequential systemd queue (experiments/scripts/gpu_queue_2026-10-21.sh) after the T5Gemma 270M run: constrained base → 24k → September trial rerun; the shared decoder fix (canvas.py) is applied and its 17 tests pass |
