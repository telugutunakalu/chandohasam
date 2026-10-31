"""Shared pieces of the DiffusionGemma LoRA work (PLAN.md): the model, LoRA, the T1 prompt, the canvas and the loss.

- load(): DiffusionGemma 26B-A4B from NVIDIA's NVFP4 checkpoint through our loader (experts resident in BF16), then
  the checkpoint's page cache dropped (on the GB10, CUDA's free memory is MemFree).
- LoRA: `inject_lora` wraps the attention projections; encoder layer i and decoder layer i share their weights, so
  each tied pair gets one adapter (the same module object in both places).
- `prompt_ids(record)`: the E6 T1 fields as a chat message, the template with thinking off and the model's empty
  thinking channel prefilled (metrical_decoder.diffusion.canvas.EMPTY_THOUGHT), as our decoder prompts it.
- `canvas_ids(record)`: the poem's tokens, the end-of-turn token, then the end-of-reply fill to the canvas length.
- `diffusion_loss`: uniform-noise corruption at rate t, optional self-conditioning pass, cross-entropy of the clean
  canvas at every position.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time
from pathlib import Path

import torch
from torch import nn

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
# $E6_RECORDS_DIR: records whose bhāvams are the full grid's prompts (../full_grid_experiments/PLAN.md)
RECORDS = Path(os.environ.get("E6_RECORDS_DIR") or REPO / "diffusion_finetuning" / "data" / "e6" / "records")
RUNS, DATA, CACHE = HERE / "runs", HERE / "data", HERE / "cache"
sys.path.insert(0, str(REPO / "meter_engine"))

from metrical_decoder.diffusion.canvas import EMPTY_THOUGHT          # noqa: E402
from metrical_decoder.diffusion.loader import DEFAULT_MODEL, load_diffusiongemma_nvfp4  # noqa: E402

TARGETS = ("q_proj", "k_proj", "v_proj", "o_proj")
# Gemma's tokenizer has no token for Telugu arasunna ఁ (1.3% of the poems' characters) or avagraha ఽ: it spells them as
# 3 raw bytes, which parallel denoising breaks apart (the first smoke run's poems: '����' and runs of 'ఁఁఁ'). Both are
# dropped from the training text (user decision 2026-10-20; a Devanagari stand-in was tried first): neither carries
# syllable weight, and on 2,089 poems with ఁ the strict verdicts were unchanged for gaṇa 100%, prāsa 99.9%, yati 98.3%.
# Our constrained decoder could not write them anyway (raw-byte tokens are outside its token slice). Word measures
# must compare with ఁ stripped on both sides (poems and lexicon), for every model.
DROP = ("ఁ", "ఽ")
STANDINS: dict[str, str] = {}
METRE_KEY, STYLE_KEY, MEANING_KEY = "ఛందస్సు", "శైలి", "భావం"
INSTRUCTION = "ఈ భావాన్ని ఈ ఛందస్సులో ఒక తెలుగు పద్యంగా వ్రాయండి."


# --------------------------------------------------------------------------- model
def evict_page_cache(paths) -> None:
    for p in paths:
        try:
            fd = os.open(p, os.O_RDONLY)
            os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
            os.close(fd)
        except OSError:
            pass


def load(resident: bool = True, log=print):
    # on the GB10 CUDA's free memory is MemFree: evict large files' page cache first when it is short
    if torch.cuda.mem_get_info()[0] / 2**30 < 70:
        sys.path.insert(0, str(REPO / "diffusion_pretraining"))
        from mdlm.checkpoint_eval import _evict_large_files
        _evict_large_files()
    model, tok = load_diffusiongemma_nvfp4(DEFAULT_MODEL, "cuda", resident=resident, log=log)
    from huggingface_hub import snapshot_download
    snap = Path(snapshot_download(DEFAULT_MODEL, local_files_only=True))
    evict_page_cache([os.path.realpath(p) for p in snap.glob("*.safetensors")])
    for p in model.parameters():
        p.requires_grad_(False)
    return model, tok


class LoRALinear(nn.Module):
    """y = base(x) + (α / r) · B(A(dropout(x))); base frozen; B starts at 0 (the model is unchanged at step 0)."""

    def __init__(self, base: nn.Linear, r: int, alpha: float, dropout: float = 0.0):
        super().__init__()
        self.base = base
        self.r, self.scale = r, alpha / r
        dev = base.weight.device
        self.A = nn.Parameter(torch.empty(r, base.in_features, device=dev, dtype=torch.float32))
        self.B = nn.Parameter(torch.zeros(base.out_features, r, device=dev, dtype=torch.float32))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))
        self.dropout = nn.Dropout(dropout) if dropout else nn.Identity()

    def forward(self, x):
        y = self.base(x)
        d = (self.dropout(x).to(self.A.dtype) @ self.A.T) @ self.B.T
        return y + (self.scale * d).to(y.dtype)


LANGUAGE_LAYERS = ("model.encoder.language_model.layers.", "model.decoder.layers.")


def _linear_children(model):
    """(parent, attribute name, nn.Linear, name) for every attention projection named in TARGETS in the language
    layers (encoder and decoder; not the vision tower, which never sees an image here)."""
    out = []
    for name, mod in model.named_modules():
        if not name.startswith(LANGUAGE_LAYERS):
            continue
        for attr in TARGETS:
            child = getattr(mod, attr, None)
            if child is None:
                continue
            lin = child.linear if hasattr(child, "linear") and isinstance(child.linear, nn.Linear) else child
            holder, hattr = (child, "linear") if lin is not child else (mod, attr)
            if isinstance(lin, nn.Linear):
                out.append((holder, hattr, lin, f"{name}.{attr}"))
    return out


def inject_lora(model, r: int = 16, alpha: float = 32, dropout: float = 0.0) -> dict[str, LoRALinear]:
    """Wrap every target projection; projections that share a weight tensor share one adapter."""
    by_weight: dict[int, LoRALinear] = {}
    adapters: dict[str, LoRALinear] = {}
    for holder, attr, lin, name in _linear_children(model):
        key = lin.weight.data_ptr()
        if key not in by_weight:
            by_weight[key] = LoRALinear(lin, r, alpha, dropout)
            adapters[name] = by_weight[key]
        setattr(holder, attr, by_weight[key])
    return adapters


def lora_state(model) -> dict:
    seen, out = set(), {}
    for name, mod in model.named_modules():
        if isinstance(mod, LoRALinear) and id(mod) not in seen:
            seen.add(id(mod))
            out[name + ".A"], out[name + ".B"] = mod.A.detach().cpu(), mod.B.detach().cpu()
    return out


def load_lora(model, path) -> None:
    """runs/<run>/lora.pt, or the release's adapter.safetensors (the same tensors under the same names)."""
    if str(path).endswith(".safetensors"):
        from safetensors.torch import load_file
        sd = load_file(str(path))
    else:
        sd = torch.load(path, map_location="cpu")
    mods = {n: m for n, m in model.named_modules() if isinstance(m, LoRALinear)}
    for key, t in sd.items():
        name, which = key.rsplit(".", 1)
        getattr(mods[name], which).data.copy_(t)


# --------------------------------------------------------------------------- data
def read_records(split: str) -> list[dict]:
    return [json.loads(l) for l in open(RECORDS / f"{split}.jsonl", encoding="utf-8")]


def t1_pool(r: dict) -> bool:
    return bool(r.get("lines")) and r.get("status") in ("agree", "engine-only") and bool(r.get("meter_te")) \
        and bool(r.get("meaning"))


def to_model(text: str) -> str:
    for ch in DROP:
        text = text.replace(ch, "")
    for te, dv in STANDINS.items():
        text = text.replace(te, dv)
    return text


def from_model(text: str) -> str:
    for te, dv in STANDINS.items():
        text = text.replace(dv, te)
    return text


def messages(r: dict) -> list[dict]:
    """E6's T1 fields (ft.canvas): metre, register, [the shared line], bhāvam; then one instruction line."""
    parts = [f"{METRE_KEY}: {r['meter_te']}", f"{STYLE_KEY}: {r['register']}"]
    if r.get("samasya"):
        parts.append(f"{r['samasya']['kind']}: {r['samasya']['line']}")
    parts += [f"{MEANING_KEY}: {r['meaning']}", INSTRUCTION]
    return [{"role": "user", "content": to_model("\n".join(parts))}]


def prompt_ids(tok, r: dict) -> list[int]:
    text = tok.apply_chat_template(messages(r), tokenize=False, add_generation_prompt=True, enable_thinking=False)
    if not text.endswith(EMPTY_THOUGHT):
        text += EMPTY_THOUGHT
    return tok(text, add_special_tokens=False).input_ids


def canvas_ids(tok, r: dict, end_ids: list[int], fill_id: int, length: int) -> list[int] | None:
    """The reply block: poem tokens + end ids, filled with ``fill_id``; None if the poem does not fit."""
    ids = tok(to_model("\n".join(r["lines"])), add_special_tokens=False).input_ids + list(end_ids)
    if len(ids) > length:
        return None
    return ids + [fill_id] * (length - len(ids))


# --------------------------------------------------------------------------- loss
def new_cache(model):
    from transformers import DynamicCache
    return DynamicCache(config=model.config.get_text_config(decoder=True))


def encode(model, prompt: torch.Tensor):
    """The prompt through the encoder into a fresh cache, with the explicit masks and positions our decoder uses
    (metrical_decoder.diffusion.canvas._encode / _open_block). transformers' encoder builds its causal masks but
    discards them (``self.create_masks_for_generate(...)`` unassigned, 5.15–5.20), so the masks must be passed.
    Returns (cache, decoder masks, decoder positions) for a canvas after the prompt."""
    dev, Lp, Cn = prompt.device, prompt.shape[1], model.config.canvas_length
    cache = new_cache(model)
    positions = torch.arange(0, Lp, dtype=torch.int32, device=dev)[None]
    attention = torch.ones((1, Lp), dtype=torch.bool, device=dev)
    dummy = torch.empty((1, Lp, 0), dtype=model.dtype, device=dev)
    masks = model.model.encoder.create_masks_for_generate(
        config=model.config, inputs_embeds=dummy, attention_mask=attention, past_key_values=cache,
        position_ids=positions, mm_token_type_ids=None)
    cache = model.model.encoder(input_ids=prompt, attention_mask=masks, past_key_values=cache,
                                position_ids=positions).past_key_values
    dec_positions = torch.arange(Lp, Lp + Cn, dtype=torch.int32, device=dev)[None]
    dec_attention = torch.nn.functional.pad(attention, (0, Cn), value=True)
    block_masks = model.model.decoder.create_diffusion_decoder_attention_mask(
        config=model.config, inputs_embeds=torch.empty((1, Cn, 1), dtype=torch.long, device=dev),
        past_key_values=cache, decoder_attention_mask=dec_attention)
    return cache, block_masks, dec_positions


def denoise(model, ctx, canvas: torch.Tensor, self_conditioning=None):
    cache, block_masks, positions = ctx
    return model(decoder_input_ids=canvas, self_conditioning_logits=self_conditioning,
                 decoder_attention_mask=block_masks, past_key_values=cache, decoder_position_ids=positions).logits


def forward(model, prompt: torch.Tensor, canvas: torch.Tensor, self_conditioning=None):
    """The prompt encoded, then one decoder pass over the canvas: the inference path, with gradients."""
    return denoise(model, encode(model, prompt), canvas, self_conditioning)          # [1, C, V] float32


def corrupt(clean: torch.Tensor, t: float, vocab: int, gen: torch.Generator) -> torch.Tensor:
    noise = torch.randint(0, vocab, clean.shape, device=clean.device, generator=gen)
    flip = torch.rand(clean.shape, device=clean.device, generator=gen) < t
    return torch.where(flip, noise, clean)


def diffusion_loss(model, prompt: torch.Tensor, clean: torch.Tensor, t: float, self_cond: bool,
                   gen: torch.Generator, reduce: bool = True):
    """Cross-entropy of the clean canvas from its corruption at rate t (uniform noise), optionally after a first
    no-gradient pass whose logits condition the second (self-conditioning)."""
    vocab = model.config.text_config.vocab_size
    noisy = corrupt(clean, t, vocab, gen)
    ctx = encode(model, prompt)                                          # once; both passes read the same cache
    sc = None
    if self_cond:
        with torch.no_grad():
            sc = denoise(model, ctx, noisy).to(model.model.decoder.embed_tokens.weight.dtype)
    logits = denoise(model, ctx, noisy, sc)
    ce = torch.nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]), clean.reshape(-1), reduction="none")
    return ce.mean() if reduce else ce.view(clean.shape)


# --------------------------------------------------------------------------- batches (full_grid_experiments Phase 0)
def encode_batch(model, prompts: list[list[int]]):
    """`encode` for several prompts at once: left-padded to the longest, padding masked, each prompt's positions from
    0 (the cache slot distances between real tokens are those of the unpadded prompt, and every prompt fits the
    1,024-token sliding window, so each example sees what `encode` gives it alone). Returns (cache, decoder masks,
    decoder positions) for a [B, canvas] batch of canvases after the prompts."""
    dev, Cn = model.device, model.config.canvas_length
    B, Lm = len(prompts), max(len(p) for p in prompts)
    pad = model.config.get_text_config().pad_token_id or 0
    ids = torch.full((B, Lm), pad, dtype=torch.long, device=dev)
    attention = torch.zeros((B, Lm), dtype=torch.bool, device=dev)
    for i, p in enumerate(prompts):
        ids[i, Lm - len(p):] = torch.as_tensor(p, device=dev)
        attention[i, Lm - len(p):] = True
    positions = (attention.cumsum(-1) - 1).clamp(min=0).to(torch.int32)
    lengths = attention.sum(-1, keepdim=True).to(torch.int32)
    cache = new_cache(model)
    dummy = torch.empty((B, Lm, 0), dtype=model.dtype, device=dev)
    masks = model.model.encoder.create_masks_for_generate(
        config=model.config, inputs_embeds=dummy, attention_mask=attention, past_key_values=cache,
        position_ids=positions, mm_token_type_ids=None)
    cache = model.model.encoder(input_ids=ids, attention_mask=masks, past_key_values=cache,
                                position_ids=positions).past_key_values
    dec_positions = lengths + torch.arange(Cn, dtype=torch.int32, device=dev)[None]
    dec_attention = torch.nn.functional.pad(attention, (0, Cn), value=True)
    block_masks = model.model.decoder.create_diffusion_decoder_attention_mask(
        config=model.config, inputs_embeds=torch.empty((B, Cn, 1), dtype=torch.long, device=dev),
        past_key_values=cache, decoder_attention_mask=dec_attention)
    return cache, block_masks, dec_positions


def diffusion_loss_batch(model, prompts: list[list[int]], clean: torch.Tensor, ts: torch.Tensor, self_cond: bool,
                         gen: torch.Generator, reduce: bool = True):
    """`diffusion_loss` for a batch: each example its own noise rate (ts [B]); self-conditioning for the whole batch
    or not at all. The mean over the batch equals the mean of the examples' losses (all canvases have one length)."""
    vocab = model.config.text_config.vocab_size
    noise = torch.randint(0, vocab, clean.shape, device=clean.device, generator=gen)
    flip = torch.rand(clean.shape, device=clean.device, generator=gen) < ts.to(clean.device)[:, None]
    noisy = torch.where(flip, noise, clean)
    ctx = encode_batch(model, prompts)
    sc = None
    if self_cond:
        with torch.no_grad():
            sc = denoise(model, ctx, noisy).to(model.model.decoder.embed_tokens.weight.dtype)
    logits = denoise(model, ctx, noisy, sc)
    ce = torch.nn.functional.cross_entropy(logits.reshape(-1, logits.shape[-1]), clean.reshape(-1), reduction="none")
    return ce.mean() if reduce else ce.view(clean.shape)


def timer():
    t0 = time.time()
    return lambda: time.time() - t0
