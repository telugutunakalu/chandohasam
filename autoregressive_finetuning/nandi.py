"""Nandi-Mini-150M, the autoregressive partner of the E6 MDLMs (PLAN.md §1, §3, §6).

    from nandi import load_model, load_tokenizer, encode_t1, prompt_ids, token_index

- **Pinned loading.** Revision 31c8ace… from the HF cache only (`local_files_only`); the custom model code is run
  with `trust_remote_code` (reviewed in step 1: no network or file access).
- **Encoding.** The model was trained on `<|im_start|> ` + text (the tokenizer's own `encode` and `__call__` add it,
  and add nothing else: tokenizer.json has no post-processor). Here the raw `tokenizers.Tokenizer` is used and the
  id 1 is prepended by hand, `[1] + encode(" " + text)`, which is the same ids (checked in step 1) without the
  wrapper's keyword-dependent behaviour.
- **T1 layout.** The E6 header (ft.canvas.tokenise_record: ఛందస్సు, శైలి, [సమస్య/మకుటం], భావం (src), పద్యం) and the
  poem lines joined by newlines, encoded as one string; the poem span comes from the character offsets. No token
  crosses the header/poem boundary or the newline before a given shared line (step 1: 0 of 906 val and 9,840
  train records), so a prompt that ends at `పద్యం:⏎` is a token prefix of its training example.
- **Token index.** The vocabulary is byte-level (Ġ, Ċ, Telugu as byte characters), so the slice is built by
  decoding every id: ids whose text is Telugu (one optional leading space) plus newline and space. 1,329 ids
  decode to a partial UTF-8 character (`�`) and are left out.

Model weights stay in the HF cache (never committed). Must not modify metrical_decoder or ../diffusion_finetuning.
"""
from __future__ import annotations

import os
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
for p in (REPO / "meter_engine", REPO / "diffusion_finetuning", REPO / "diffusion_pretraining"):
    if str(p) not in sys.path:
        sys.path.append(str(p))                       # after this folder: its finetune.py, constrained_sample.py win

from ft.text import MEANING_KEY, METRE_KEY, POEM_KEY, STYLE_KEY        # noqa: E402

# $E6_RECORDS_DIR: records whose bhāvams are the full grid's prompts (../full_grid_experiments/PLAN.md)
E6_RECORDS = Path(os.environ.get("E6_RECORDS_DIR") or REPO / "diffusion_finetuning" / "data" / "e6" / "records")
METRE_OK = ("agree", "engine-only")                                    # as ft.canvas / ft.build_data

MODEL_ID = "FrontiersMind/Nandi-Mini-150M"
REVISION = "31c8aceaa16e2611a5773bbefc6564db39043370"
WEIGHTS_BYTES = 306_842_392
EOS, BOS, PAD = 0, 1, 3                                                # <|endoftext|>, <|im_start|>, <|pad|>
NEWLINE_ID, SPACE_ID = 188, 210                                        # Ċ and Ġ; checked by check_nandi.py

TELUGU_TOKEN = re.compile(r"^ ?[ఀ-౥]+$")                               # as metrical_decoder.vocab
MAX_TOKENS = 1024                      # T1 examples longer than this are dropped (0.04%; the context is 2,048)


@lru_cache(maxsize=1)
def snapshot() -> Path:
    """The local snapshot folder of the pinned revision in the HF cache (raises if it was never downloaded)."""
    from huggingface_hub.constants import HF_HUB_CACHE
    p = Path(HF_HUB_CACHE) / f"models--{MODEL_ID.replace('/', '--')}" / "snapshots" / REVISION
    if not (p / "config.json").exists():
        raise FileNotFoundError(f"{MODEL_ID}@{REVISION[:7]} is not in the HF cache ({p})")
    return p


@lru_cache(maxsize=1)
def load_tokenizer():
    """The raw byte-level BPE (`tokenizers.Tokenizer`), NFC normaliser included."""
    from tokenizers import Tokenizer
    return Tokenizer.from_file(str(snapshot() / "tokenizer.json"))


def load_model(dtype: str = "bfloat16", device: str = "cpu", weights: str | None = None):
    """The base model, or with ``weights`` a fine-tuned one: an EMA snapshot or checkpoint written by finetune.py, or
    the released folder (huggingface.co/samvaran/chandohasam, nandi-150m-padyam/, downloaded)."""
    import torch
    from transformers import AutoModelForCausalLM
    if weights and (Path(weights) / "model.safetensors").exists():
        return AutoModelForCausalLM.from_pretrained(
            str(weights), trust_remote_code=True, local_files_only=True, dtype=getattr(torch, dtype)).to(device)
    model = AutoModelForCausalLM.from_pretrained(
        str(snapshot()), trust_remote_code=True, local_files_only=True, dtype=getattr(torch, dtype))
    if weights:
        st = torch.load(weights, map_location="cpu", weights_only=False)
        sd = st.get("ema", st)
        missing, unexpected = model.load_state_dict({k: v.to(getattr(torch, dtype)) for k, v in sd.items()},
                                                    strict=False)
        bad = [k for k in missing if k != "lm_head.weight"] + list(unexpected)   # lm_head is tied to the embedding
        if bad:
            raise ValueError(f"{weights}: state dict does not match the model: {bad[:5]}")
        model.tie_weights()
    return model.to(device)


def encode(text: str, tok=None) -> list[int]:
    """`<|im_start|> ` + text, as the model was trained (no end-of-text)."""
    tok = tok or load_tokenizer()
    return [BOS] + tok.encode(" " + text, add_special_tokens=False).ids


def decode(ids, tok=None) -> str:
    """The text of ids after the BOS prefix (its space removed)."""
    tok = tok or load_tokenizer()
    ids = [i for i in ids if i not in (BOS, EOS, PAD)]
    text = tok.decode(ids)
    return text[1:] if text.startswith(" ") else text


# --------------------------------------------------------------------------- T1 layout
def has_metre(r: dict) -> bool:
    return r["status"] in METRE_OK and bool(r.get("meter_te"))


def t1_header(r: dict, empty_meaning: bool = False) -> str:
    """The E6 T1 header up to and including `పద్యం:⏎` (empty_meaning: the T0 form, an empty `భావం:` line)."""
    h = f"{METRE_KEY}: {r['meter_te']}\n" if has_metre(r) else ""
    h += f"{STYLE_KEY}: {r['register']}\n"
    sam = r.get("samasya")
    if sam:
        h += f"{sam['kind']}: {sam['line']}\n"
    if empty_meaning:
        h += f"{MEANING_KEY}:\n"
    elif r.get("meaning"):
        h += f"{MEANING_KEY} ({r.get('meaning_src') or ''}): {r['meaning']}\n"
    return h + f"{POEM_KEY}:\n"


def in_t1_pool(r: dict) -> bool:
    """E6's T1 pool (ft.canvas.Pools): poem lines, a metre the engines accept, and a meaning."""
    return bool(r.get("lines")) and has_metre(r) and bool(r.get("meaning"))


@lru_cache(maxsize=1)
def mdlm_tokenizer():
    from tokenizer import load_default                                 # ../diffusion_pretraining (akshara tokens)
    return load_default()


def mdlm_target_tokens(r: dict) -> int:
    """The MDLM's T1 target size for this poem: its lines' akshara tokens and the newlines between them, a given
    shared line excluded (ft.canvas._poem). Likelihoods are reported per these tokens, E6's unit."""
    tok = mdlm_tokenizer()
    lines = r["lines"][:-1] if r.get("samasya") and len(r["lines"]) > 1 else r["lines"]
    return sum(len(tok.encode(ln)) for ln in lines) + len(lines) - 1


def prompt_ids(r: dict, empty_meaning: bool = False, tok=None) -> list[int]:
    return encode(t1_header(r, empty_meaning), tok)


def encode_t1(r: dict, empty_meaning: bool = False, tok=None) -> tuple[list[int], list[bool]]:
    """ids of `<|im_start|> header poem <|endoftext|>` and a per-token loss flag: True on the poem tokens and the
    final end-of-text; False on the header and on a given shared line (with the newline before it), as E6."""
    tok = tok or load_tokenizer()
    header, lines = t1_header(r, empty_meaning), r["lines"]
    text = " " + header + "\n".join(lines)
    enc = tok.encode(text, add_special_tokens=False)
    start = len(" " + header)
    given = len(text) - len(lines[-1]) - 1 if r.get("samasya") and len(lines) > 1 else len(text)
    loss = [start <= s < given for s, _ in enc.offsets]
    return [BOS] + enc.ids + [EOS], [False] + loss + [True]


# --------------------------------------------------------------------------- the decoder's vocabulary slice
def token_index(tok=None):
    """metrical_decoder's TokenIndex for Nandi: every id that decodes to Telugu, plus newline and space."""
    from metrical_decoder.vocab import TokenIndex
    tok = tok or load_tokenizer()
    pairs = []
    for i in range(tok.get_vocab_size()):
        text = tok.decode([i])
        if TELUGU_TOKEN.match(text):
            pairs.append((i, text))
    assert tok.decode([NEWLINE_ID]) == "\n" and tok.decode([SPACE_ID]) == " "
    pairs += [(NEWLINE_ID, "\n"), (SPACE_ID, " ")]
    return TokenIndex.from_texts(pairs, eos_ids=(EOS,))


# --------------------------------------------------------------------------- validation likelihood
def val_items(recs: list[dict], tok=None) -> list[dict]:
    """T1 and T0 encodings of the val records in the T1 pool, with their MDLM target sizes."""
    out = []
    for r in recs:
        if not in_t1_pool(r):
            continue
        t1, m1 = encode_t1(r, tok=tok)
        t0, m0 = encode_t1(r, empty_meaning=True, tok=tok)
        if len(t1) <= MAX_TOKENS:
            out.append({"id": r["id"], "T1": (t1, m1), "T0": (t0, m0), "mdlm_tokens": mdlm_target_tokens(r)})
    return out


def nll_sums(model, seqs: list[tuple[list[int], list[bool]]], device, micro_tokens: int = 8192) -> list[tuple[float, int]]:
    """Summed next-token NLL (nats) over each sequence's loss positions, and their count. Right-padded batches
    with no attention mask: causal attention never lets a real token see the padding after it."""
    import torch
    import torch.nn.functional as F
    order = sorted(range(len(seqs)), key=lambda i: len(seqs[i][0]))
    out: list = [None] * len(seqs)
    i = 0
    while i < len(order):
        L = len(seqs[order[i]][0])
        j = i
        while j < len(order) and (j - i + 1) * len(seqs[order[j]][0]) <= micro_tokens:
            j += 1
        j = max(j, i + 1)
        rows = order[i:j]
        L = max(len(seqs[k][0]) for k in rows)
        ids = torch.full((len(rows), L), PAD, dtype=torch.long)
        lab = torch.full((len(rows), L), -100, dtype=torch.long)
        for r_, k in enumerate(rows):
            s, m = seqs[k]
            ids[r_, :len(s)] = torch.tensor(s)
            lab[r_, :len(s)] = torch.tensor([t if keep else -100 for t, keep in zip(s, m)])
        ids, lab = ids.to(device), lab.to(device)
        with torch.no_grad(), torch.autocast(device.type, dtype=torch.bfloat16, enabled=device.type == "cuda"):
            logits = model(input_ids=ids, use_cache=False).logits[:, :-1].float()
        tgt = lab[:, 1:]
        nll = F.cross_entropy(logits.reshape(-1, logits.size(-1)), tgt.reshape(-1), reduction="none",
                              ignore_index=-100).view(tgt.shape)
        for r_, k in enumerate(rows):
            out[k] = (float(nll[r_].sum()), int((tgt[r_] != -100).sum()))
        i = j
    return out


def evaluate_t1(model, items: list[dict], device) -> dict:
    """val_nll/T1 and val_nll/T0: nats per MDLM target token (E6's unit, for the T1-T0 gap); val_nll_tok/*: per
    Nandi token."""
    was = model.training
    model.eval()
    res = {}
    for task in ("T1", "T0"):
        sums = nll_sums(model, [it[task] for it in items], device)
        nats = sum(s for s, _ in sums)
        res[f"val_nll/{task}"] = nats / sum(it["mdlm_tokens"] for it in items)
        res[f"val_nll_tok/{task}"] = nats / sum(n for _, n in sums)
    model.train(was)
    return res
