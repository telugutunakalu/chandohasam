# -*- coding: utf-8 -*-
"""
A Hugging Face causal LM as a :class:`~metrical_decoder.sources.LogitsSource`.

One token per forward pass with an incremental cache. The prompt is prefilled
once per distinct prompt and the cache snapshot is copied for every run, so
the modes and seeds of one (meter, topic) share the prefill. Rollback
(backtracking) restores that snapshot and re-feeds the kept tokens in one
forward pass; this works for any cache class, sliding-window layers included.

All whole-vocabulary statistics (log-sum-exp, entropy, top-k, rank) are
computed on the device; only the slice logits and a few scalars cross to the
CPU each step.

``push`` runs the forward pass on a worker thread and returns at once; every
read of the logits or the cache waits for it. The decoder computes the next
mask (CPU) in the meantime, so the two overlap. There is only ever one forward
in flight and nothing else touches the model while it runs.

Owns: :class:`HFCausalLM`. The only module of the package that imports torch.
"""
from __future__ import annotations

import copy
import random
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Optional, Sequence

import torch

from .sources import Distribution
from .vocab import TokenIndex

# An empty thinking channel after the generation prompt. Do NOT prefill it for Gemma-4-E4B-it: measured
# 2026-09-24 (kandamu, utpalamala, dvipada), it makes the model answer with an English analysis of the
# rules ("The user wants me to…"): 2.5–10% of the first step's mass on meter-valid tokens, against 99.9%
# with the plain chat template, where the model writes the poem directly.
EMPTY_THOUGHT = "<|channel>thought\n<channel|>"


class HFCausalLM:
    """Gemma-4 (and other chat LMs) as a logits source.

    ``prefill`` (default none) is appended after the chat template's generation prompt, in every mode alike.
    """

    def __init__(self, model_id: str, device: str = "cuda", dtype: str = "bfloat16", top_k: int = 5,
                 local_files_only: bool = True, prefill: Optional[str] = None):
        import transformers
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer, GenerationConfig

        self.model_id = model_id
        self.device = torch.device(device)
        self.top_k = top_k
        self.prefill = prefill
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, local_files_only=local_files_only)
        # load the class the checkpoint declares (Gemma-4-it: Gemma4ForConditionalGeneration), so no
        # weight is silently left at its random initialisation by a text-only class
        config = AutoConfig.from_pretrained(model_id, local_files_only=local_files_only)
        arch = (getattr(config, "architectures", None) or [None])[0]
        cls = getattr(transformers, arch, None) if arch else None
        kw = dict(dtype=getattr(torch, dtype), device_map=device, local_files_only=local_files_only)
        self.model = (cls or AutoModelForCausalLM).from_pretrained(model_id, **kw)
        self.model.eval()
        try:
            gen = GenerationConfig.from_pretrained(model_id, local_files_only=local_files_only)
            eos = gen.eos_token_id
        except OSError:
            eos = self.tokenizer.eos_token_id
        self.eos_ids = tuple(eos if isinstance(eos, (list, tuple)) else [eos])
        self.index = TokenIndex.from_tokenizer(self.tokenizer, eos_ids=self.eos_ids)
        self._slice = torch.tensor(self.index.ids, device=self.device)
        self._prompt_cache: dict[tuple[int, ...], tuple] = {}
        self._cache = None
        self._logits: Optional[torch.Tensor] = None
        self._prompt: tuple[int, ...] = ()
        self.generated: list[int] = []
        self._worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="forward")
        self._pending: Optional[Future] = None

    # ------------------------------------------------------------ prompts
    def prompt_ids(self, messages: list[dict]) -> list[int]:
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                                  enable_thinking=False)
        if self.prefill and not text.endswith(self.prefill):
            text += self.prefill
        return self.tokenizer(text, add_special_tokens=False).input_ids

    # ------------------------------------------------------------ source protocol
    @torch.no_grad()
    def _forward(self, ids: Sequence[int], cache) -> tuple[torch.Tensor, object]:
        inp = torch.tensor([list(ids)], device=self.device)
        out = self.model(input_ids=inp, past_key_values=cache, use_cache=True)
        return out.logits[0, -1].float(), out.past_key_values

    def _wait(self) -> None:
        """Take in the forward pass ``push`` started, if any."""
        if self._pending is not None:
            pending, self._pending = self._pending, None
            self._logits, self._cache = pending.result()

    def start(self, prompt_ids: Sequence[int]) -> None:
        self._wait()
        key = tuple(prompt_ids)
        if key not in self._prompt_cache:
            self._prompt_cache.clear()                          # one prompt at a time: bound memory
            logits, cache = self._forward(key, None)
            self._prompt_cache[key] = (logits, cache)
        logits, cache = self._prompt_cache[key]
        self._prompt = key
        self._cache = copy.deepcopy(cache)
        self._logits = logits.clone()
        self.generated = []

    def next(self) -> Distribution:
        self._wait()
        z = self._logits
        lse = torch.logsumexp(z, dim=0)
        logp = z - lse
        entropy = -(logp.exp() * logp).sum()
        top = torch.topk(z, self.top_k)
        return Distribution(slice_logits=z.index_select(0, self._slice).tolist(), lse=float(lse),
                            entropy=float(entropy),
                            top=list(zip(top.indices.tolist(), top.values.tolist())))

    def logit(self, token_id: int) -> float:
        self._wait()
        return float(self._logits[token_id])

    def rank(self, token_id: int) -> int:
        self._wait()
        return int((self._logits > self._logits[token_id]).sum()) + 1

    def sample_full(self, temperature: float, top_p: float, rng: random.Random) -> tuple[int, float]:
        self._wait()
        probs = torch.softmax(self._logits / temperature, dim=0)
        sorted_p, order = torch.sort(probs, descending=True)
        keep = torch.cumsum(sorted_p, dim=0) - sorted_p < top_p          # smallest prefix reaching top_p
        kept = sorted_p[keep] / sorted_p[keep].sum()
        gen = torch.Generator(device=self.device).manual_seed(rng.getrandbits(62))
        j = int(torch.multinomial(kept, 1, generator=gen))
        return int(order[keep][j]), float(kept[j])

    def push(self, token_id: int) -> None:
        self._wait()
        self._pending = self._worker.submit(self._forward, [token_id], self._cache)
        self.generated.append(token_id)

    def rollback(self, n_generated: int) -> None:
        self._wait()
        keep = self.generated[:n_generated]
        logits, cache = self._prompt_cache[self._prompt]
        self._cache = copy.deepcopy(cache)
        self._logits = logits.clone()
        if keep:
            self._logits, self._cache = self._forward(keep, self._cache)
        self.generated = keep

    def decode(self, ids: Sequence[int]) -> str:
        return self.tokenizer.decode(list(ids), skip_special_tokens=False)
