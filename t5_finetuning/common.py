"""Shared pieces of the T5Gemma 2 experiments (PLAN.md): models, the metre-aware input, targets, LoRA.

- `source_text(r)`: the encoder input — task, metre, the metre's rules, register, shared line, bhāvam (PLAN.md §2).
- `target_text(r)`: the poem's lines (ఁ and ఽ dropped), newline-separated.
- `scansion_source(r)` / `scansion_target(r)`: the auxiliary task — the poem → each line's guru/laghu pattern.
- `load(size)`: tokenizer and `T5Gemma2ForConditionalGeneration` from the local Hugging Face cache.
- `inject_lora`: LoRA on q/k/v/o of the encoder and decoder text layers, and with `mlp=True` on gate/up/down too
  (the 4B); `load_adapter` reads it back from lora.pt or the released adapter.safetensors.
"""
from __future__ import annotations

import json
import os
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import torch
from torch import nn

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
# $E6_RECORDS_DIR: records whose bhāvams are the full grid's prompts (../full_grid_experiments/README.md)
RECORDS = Path(os.environ.get("E6_RECORDS_DIR") or REPO / "diffusion_finetuning" / "data" / "e6" / "records")
RUNS, DATA = HERE / "runs", HERE / "data"
sys.path.insert(0, str(REPO / "meter_engine"))

MODELS = {"270m": "google/t5gemma-2-270m-270m", "1b": "google/t5gemma-2-1b-1b", "4b": "google/t5gemma-2-4b-4b"}
DROP = ("ఁ", "ఽ")                     # Gemma spells them as raw bytes; weightless in the scansion (PLAN.md §2)
TASK_POEM, TASK_SCAN = "పని: పద్యం", "పని: గురులఘువులు"
METRE_OK = ("agree", "engine-only")
TARGETS = ("q_proj", "k_proj", "v_proj", "o_proj")
MLP_TARGETS = ("gate_proj", "up_proj", "down_proj")      # 75% of the 4B's parameters sit in the MLPs


def clean(text: str) -> str:
    for ch in DROP:
        text = text.replace(ch, "")
    return text


def metre_key(m: str | None) -> str | None:
    if not m:
        return None
    return "seesamu" if m.startswith("seesamu") else m


def t1_pool(r: dict) -> bool:
    return bool(r.get("lines")) and r.get("status") in METRE_OK and bool(r.get("meter_te")) and bool(r.get("meaning"))


def read_records(split: str) -> list[dict]:
    return [json.loads(l) for l in open(RECORDS / f"{split}.jsonl", encoding="utf-8")]


@lru_cache(maxsize=None)
def rules(meter: str) -> str:
    """metrical_decoder's rules of the metre, without the closing guru/laghu paragraph (the same for every metre);
    empty for a metre the catalogue does not know."""
    from metrical_decoder.prompts import meter_rules
    try:
        text = meter_rules(meter)
    except Exception:
        return ""
    return "\n".join(ln for ln in text.splitlines() if not ln.startswith("Guru (U) and laghu (I)"))


def source_text(r: dict, with_rules: bool = True, empty_meaning: bool = False) -> str:
    m = metre_key(r.get("meter")) or ""
    parts = [TASK_POEM, f"ఛందస్సు: {r['meter_te']}"]
    if with_rules and rules(m):
        parts.append(rules(m))
    parts.append(f"శైలి: {r['register']}")
    if r.get("samasya"):
        parts.append(f"{r['samasya']['kind']}: {r['samasya']['line']}")
    parts.append(f"భావం: {'' if empty_meaning else r['meaning']}")
    return clean("\n".join(parts))


def target_text(r: dict) -> str:
    return clean("\n".join(r["lines"]))


def scansion(r: dict) -> str | None:
    """Each line's guru/laghu pattern by the strict engines (one line per pāda), or None."""
    from metrical_decoder.evaluate import evaluate
    pats = evaluate("\n".join(r["lines"]), metre_key(r.get("meter")) or "").get("patterns") or []
    return "\n".join(pats) if pats and len(pats) == len(r["lines"]) else None


def scansion_source(r: dict) -> str:
    return clean(f"{TASK_SCAN}\nఛందస్సు: {r['meter_te']}\nపద్యం:\n" + "\n".join(r["lines"]))


def freeze_vision(model) -> int:
    """The vision tower never sees an image here: no gradient, no optimizer state, bf16 (it is 0.42B parameters at
    every size). Returns the number of frozen parameters."""
    n = 0
    for name, p in model.named_parameters():
        if "vision" in name:
            p.requires_grad_(False)
            p.data = p.data.to(torch.bfloat16)
            n += p.numel()
    return n


def load(size: str, dtype=torch.bfloat16, device: str = "cuda", path: str = ""):
    """The base model, or with ``path`` a save_pretrained folder (e.g. runs/<run>/final, to continue training)."""
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer, T5Gemma2ForConditionalGeneration
    path = path or snapshot_download(MODELS[size], local_files_only=True)
    tok = AutoTokenizer.from_pretrained(path)
    model = T5Gemma2ForConditionalGeneration.from_pretrained(path, dtype=dtype).to(device)
    return model, tok


def encode_pair(tok, src: str, tgt: str, max_src: int, max_tgt: int) -> tuple[list[int], list[int]] | None:
    """Encoder ids (with <bos>, as the tokenizer adds it) and label ids (target + <eos>); None if either is too long."""
    s = tok(src).input_ids
    t = tok(tgt, add_special_tokens=False).input_ids + [tok.eos_token_id]
    if len(s) > max_src or len(t) > max_tgt:
        return None
    # int32 arrays, not Python lists: 300k pairs as lists of int objects took several GB of the shared memory
    # (one cause of the 2026-10-21 system OOM)
    return np.asarray(s, dtype=np.int32), np.asarray(t, dtype=np.int32)


def collate(pairs: list[tuple[list[int], list[int]]], pad: int, device: str = "cuda") -> dict:
    ls, lt = max(len(s) for s, _ in pairs), max(len(t) for _, t in pairs)
    ids = torch.full((len(pairs), ls), pad, dtype=torch.long)
    att = torch.zeros((len(pairs), ls), dtype=torch.long)
    lab = torch.full((len(pairs), lt), -100, dtype=torch.long)
    for i, (s, t) in enumerate(pairs):
        ids[i, :len(s)], att[i, :len(s)], lab[i, :len(t)] = torch.from_numpy(np.asarray(s)), 1, torch.from_numpy(np.asarray(t))
    return {"input_ids": ids.to(device), "attention_mask": att.to(device), "labels": lab.to(device)}


# --------------------------------------------------------------------------- LoRA (the 4B)
class LoRALinear(nn.Module):
    """y = base(x) + (α / r) · B(A(x)); base frozen; B starts at 0."""

    def __init__(self, base: nn.Linear, r: int, alpha: float):
        super().__init__()
        self.base, self.scale = base, alpha / r
        dev = base.weight.device
        self.A = nn.Parameter(torch.empty(r, base.in_features, device=dev, dtype=torch.float32))
        self.B = nn.Parameter(torch.zeros(base.out_features, r, device=dev, dtype=torch.float32))
        nn.init.kaiming_uniform_(self.A, a=math.sqrt(5))

    def forward(self, x):
        y = self.base(x)
        return y + (self.scale * ((x.to(self.A.dtype) @ self.A.T) @ self.B.T)).to(y.dtype)


def inject_lora(model, r: int = 16, alpha: float = 32, mlp: bool = False) -> list[nn.Parameter]:
    """LoRA on the attention projections of the text layers (encoder and decoder; not the vision tower), and with
    ``mlp`` on the MLP projections too."""
    for p in model.parameters():
        p.requires_grad_(False)
    sites = []
    targets = TARGETS + (MLP_TARGETS if mlp else ())
    for name, mod in model.named_modules():
        if "vision" in name:
            continue
        for attr in targets:
            child = getattr(mod, attr, None)
            if isinstance(child, nn.Linear):
                sites.append((mod, attr, child))
    params = []
    for mod, attr, lin in sites:
        a = LoRALinear(lin, r, alpha)
        setattr(mod, attr, a)
        params += [a.A, a.B]
    return params


def lora_state(model) -> dict:
    return {n: p.detach().cpu() for n, p in model.named_parameters() if n.endswith(".A") or n.endswith(".B")}


def load_adapter(path) -> dict:
    """An adapter's A/B matrices: runs/<run>/lora.pt (train.py) or the released adapter.safetensors (the same tensors
    under the same names, huggingface.co/samvaran/chandohasam/t5gemma2-4b-padyam-lora)."""
    if str(path).endswith(".safetensors"):
        from safetensors.torch import load_file
        return load_file(str(path))
    return torch.load(path, map_location="cpu")
