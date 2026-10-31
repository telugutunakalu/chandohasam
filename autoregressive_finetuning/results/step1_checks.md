# Step 1: Nandi-Mini-150M downloaded, code reviewed, tokenizer and model checked (2026-10-18)

`FrontiersMind/Nandi-Mini-150M` @ `31c8aceaa16e2611a5773bbefc6564db39043370`, in the HF cache
(`model.safetensors` 306,842,392 bytes, SHA-256 `d1360813…20ae14fc` = the Hub's blob id). Numbers:
`step1_checks.json`, from `check_nandi.py` (CPU, seed 20261018; 10k random train poems, all 11,655 val + test poems).

**Verdict: pass**, with one finding for the constrained modes (§4 below).

## 1. Code review (read in full: 480 + 120 + 144 lines)

| question | finding |
|---|---|
| network or file access | none. Imports are torch, transformers and tokenizers only; the scan finds no request, socket, subprocess, open, eval, pickle or download call. `@use_kernel_forward_from_hub("RMSNorm")` is a no-op here (the `kernels` package is not installed) |
| layer sharing | `for layer in layers: for r in range(2): layer(...)`: each of the 16 layers runs twice in a row (L0 L0 L1 L1 …) with the same parameters, so autograd adds both passes' gradients. The KV cache gives repeat r the slots `layer_idx + 16r` (`_VirtualLayerCache`), so generation with a cache is correct |
| factorised embedding | `embed_tokens` 131,072 × 196 → `embedding_proj` 196 → 832; output `lm_head_proj` 832 → 196 → `lm_head` 196 → 131,072, tied to `embed_tokens` (checked: same storage after loading) |
| padding and masks | the stock `create_causal_mask` with the attention mask; positions default to `arange`, so **right padding** only (training pads on the right; generation has no padding). Checked: right padding changes the real tokens' logits by ≤ 3.6e-5 (fp32 noise) |
| precision | weights stored in bf16; RMSNorm and RoPE run in fp32 internally; softmax in fp32 (eager) or SDPA (default) |
| compile | `_can_compile_fullgraph = True`; the training forward (no cache) is plain modules. The cache proxy only matters for generation |
| tokenizer wrapper | `encode` always, and `__call__` unless `add_special_tokens=True` is passed, prepend `"<|im_start|> "`. tokenizer.json has no post-processor, so nothing else is added. We bypass the wrapper: `[1] + raw.encode(" " + text)` gives the same ids (200/200 texts). `decode` keeps the prefix's space; `nandi.decode` drops it |
| generation config | none shipped: `generate` needs `eos_token_id=0` and a `pad_token_id` (the config's is null; the tokenizer's `<|pad|>` is 3) |

## 2. Tokenizer

| check | result |
|---|---|
| newline / space | one token each: `Ċ` = 188, `Ġ` = 210 |
| round trip (encode → decode) on 10,000 train poems | **10,000 / 10,000 exact**; no text in E6 is non-NFC |
| T1 layout: the prompt (ending `పద్యం:⏎`) is a token prefix of its training example; loss starts exactly at the poem | **21,596 / 21,596** (all val + test with a meaning, 10k train); no token crosses the poem start or the newline before a shared line |
| T1 example length (Nandi tokens, with BOS and EOS) | p50 150, p99 412, max **2,377**; 8 of 21,596 exceed 1,024 |
| vocabulary | 131,072 ids; **1,329 decode to a partial UTF-8 character** (`�`); 7,392 whole Telugu tokens + newline + space = the decoder's slice of 7,394 |
| Telugu characters that whole tokens can spell, held-out poems | **99.993%** (pass ≥ 99.9%). Not spellable: ఝ (75), ఙ (55), ఽ (2), in **114 of 11,655** poems |
| the same, train sample | 99.986%; adds rare signs (౽ ౼ ౹ ౢ ౘ ౄ ౠ ఌ ౡ ౝ, 1–5 each) |

## 3. Model (CPU, fp32 and bf16)

| check | result |
|---|---|
| parameters | **153,412,928** (embedding 25,690,112); 16 unique layers, 32 layer passes per token; SDPA attention |
| finite logits, 10 T1 prompts | 10 / 10 (fp32 and bf16) |
| bf16 against fp32 | top-1 agrees 10 / 10; max logit difference 0.15 |
| one backward pass (loss on the poem only) | gradients on 148 / 148 tensors, all finite; zero-shot loss 3.63 nats per Nandi token |
| greedy continuation of 5 first lines (val), and 3 T1 prompts sampled at 0.7 / 0.9 | degenerate repetition (`దనఁ దనఁ …`, `సుతా సుతా …`, `ఆత్మ, ఆత్మ, …`), no poem continued from memory; the T1 layout means nothing to the base model yet. Text in `runs/step1/samples.txt` (not committed). Step 2's leakage probe measures reproduction properly |

## 4. Finding: partial-byte tokens in the constrained modes

The decoder's slice holds whole tokens only (as for Gemma in IndicNeuroSym). But the tokenizer was trained mostly on
modern text, and in classical poems some byte boundaries fall inside a character: **ఱ** after a vowel sign
(`ాఱ`, `ుఱ`, `ేఱ`), `ూఁ`, `ుంభ`, `ూఢ`, `ేఘ`. These come as two partial ids that only decode together.

| canonical tokens outside the slice | tokens | poems with any |
|---|---|---|
| train sample (10,000 poems) | 0.99% | 21.2% |
| held out (val + test, 11,655 poems) | **1.14%** | **31.7%** |
| (MDLM E6 slice, for comparison: aksharas seen ≥ 10 times) | 0.06% | |

The free mode is unaffected. In the constrained modes those words must be spelled with whole tokens (`ఱ` exists alone),
a tokenization the model never trained on, so their probability is understated, and ఝ / ఙ cannot be written at all.
How much this costs is measurable without changing anything: split step 4's "overridden" count into
*first choice was a partial id* and *first choice broke a rule*. If the first share is material, add pair entries
to the slice (PLAN §12, decision 4).
