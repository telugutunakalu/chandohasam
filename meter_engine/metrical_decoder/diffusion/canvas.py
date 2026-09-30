# -*- coding: utf-8 -*-
"""
The model side of constrained diffusion decoding: prompt, blocks and denoising passes.

DiffusionGemma writes a reply in blocks of ``canvas_length`` (256) positions.
Its own sampler (``transformers``' ``EntropyBoundSampler``) starts a block from
uniform random tokens and repeats a *denoising pass*: the decoder reads the
canvas, the encoder's cache of everything before the block, and the previous
pass's predictions (*self-conditioning*); it predicts every position; the
lowest-entropy predictions are kept and every other position is refilled with
random tokens. When the block settles, its argmax is appended to the context
and the next block starts.

Constrained decoding keeps the same passes but decides the block from the left:
a *frozen* prefix of committed tokens (every one approved by the enforcer) and
the model's working *draft* after it. :meth:`DiffusionGemmaCanvas.denoise` runs
one pass with the frozen prefix written into the canvas and pinned in the
self-conditioning signal (a one-hot prediction of its own token), so the
model's picture of the block agrees with what has been committed. The rest of
the canvas evolves exactly as under the model's own sampler: after each pass
the jointly confident predictions stay in the draft and every other open
position returns to random noise. (A first version refilled the whole open part
with noise every pass; its poems were markedly worse — plan §15.)

The model plans the whole block at once, the end of its reply included: left
alone it drafts a short free-verse reply and fills the rest of the block with
``<eos>``, which it keeps because it is confident about it. The meter needs
about twice that length, so past the planned end every position would be one
the model wants empty (in the first trial, 52% of the tokens the constraint had
to choose were chosen against an ``<eos>``, with valid mass ≈ 0, and half the
words became single-akshara filler). With ``forbid_end`` (default) end-of-text
tokens are removed from the model's predictions everywhere in the block — the
poem cannot end until the enforcer says so — and the model plans a text long
enough for the meter.

A pass returns a :class:`CanvasPass`: for every open position, a token sampled
from the model's temperature-scaled prediction (the *proposal*) and the entropy
of that prediction, plus, on request, the full distribution at a position in the
form the enforcer and the traces use (:class:`~metrical_decoder.sources.Distribution`).

:class:`RandomCanvas` is the random-logit control: the same interface with
standard-normal logits over the vocabulary slice, no model — for testing the
decoding loop on the CPU.

Owns: :class:`DiffusionGemmaCanvas`, :class:`CanvasPass`, :class:`RandomCanvas`.
"""
from __future__ import annotations

import math
import random
from typing import Optional, Protocol, Sequence

from ..sources import Distribution, logsumexp
from ..vocab import TokenIndex

# DiffusionGemma opens every reply with an empty thinking channel, even with thinking off (its own
# generation, 2026-09-25: <|channel> thought \n <channel|>, then the text). Constrained decoding
# decides the reply from its first position; without this prefill the model puts probability 1.0 on
# <|channel> there and 0.000 on meter-valid tokens, with it 0.98–1.00 (kandamu, utpalamala,
# ataveladi). Gemma-4 E4B is the opposite (0.999 without, English analysis with), so each model
# gets its measured setting.
EMPTY_THOUGHT = "<|channel>thought\n<channel|>"


class Pass(Protocol):
    """What the decoding loop reads from one denoising pass (positions are canvas positions)."""
    first: int                                    # first open (unfrozen) position

    def proposal(self, pos: int) -> int: ...      # token sampled from the scaled prediction
    def entropy(self, pos: int) -> float: ...     # entropy of the scaled prediction (nats)
    def p_scaled(self, pos: int, token_id: int) -> float: ...
    def distribution(self, pos: int) -> Distribution: ...   # T = 1, slice + whole-vocabulary stats
    def rank(self, pos: int, token_id: int) -> int: ...     # rank in the whole vocabulary, T = 1
    def logp(self, pos: int, token_id: int) -> float: ...   # log-probability, whole vocabulary, T = 1


class Canvas(Protocol):
    index: TokenIndex
    canvas_length: int
    passes_in_block: int
    forbid_end: bool                              # end-of-text removed from the model's predictions
    end_token_ids: tuple[int, ...]                # the tokens that end a reply

    def prompt_ids(self, messages: list[dict]) -> list[int]: ...
    def start(self, prompt_ids: Sequence[int], seed: int) -> None: ...
    def denoise(self, frozen: Sequence[int], temperature: float) -> Pass: ...
    def forget(self, from_pos: int) -> None: ...                # backtracking: draft from ``from_pos`` to noise
    def close_block(self, block: Sequence[int]) -> None: ...
    def decode(self, ids: Sequence[int]) -> str: ...


# ----------------------------------------------------------------------------
# the model
# ----------------------------------------------------------------------------
class DiffusionGemmaCanvas:
    """DiffusionGemma, one block at a time, with a frozen prefix per pass.

    ``model``/``tokenizer`` come from :func:`~.loader.load_diffusiongemma_nvfp4`
    (or ``DiffusionGemmaForBlockDiffusion.from_pretrained``). Batch size 1.
    """

    def __init__(self, model, tokenizer, top_k: int = 5, prefill: str = None, entropy_bound: float = 0.1,
                 forbid_end: bool = True):
        import torch
        self.torch = torch
        self.model = model
        self.tokenizer = tokenizer
        # text appended after the generation prompt: by default the model's own empty thinking channel
        self.prefill = EMPTY_THOUGHT if prefill is None else prefill
        self.entropy_bound = entropy_bound                # the model's own draft acceptance (generation_config)
        self.device = next(model.parameters()).device
        self.canvas_length = model.config.canvas_length
        self.vocab_size = model.config.text_config.vocab_size
        eos = model.generation_config.eos_token_id
        eos = eos if isinstance(eos, (list, tuple)) else [eos]
        self.eos_ids = tuple(e for e in eos if e is not None) or (tokenizer.eos_token_id,)
        self.index = TokenIndex.from_tokenizer(tokenizer, eos_ids=self.eos_ids)
        self.slice = torch.tensor(self.index.ids, device=self.device)
        self.top_k = top_k
        self.passes_in_block = 0
        # the tokens that end a reply (<eos>, <turn|>, <|tool_response>) and <pad>: see ``forbid_end``
        pad = model.config.text_config.pad_token_id
        self.end_ids = torch.tensor(sorted(set(self.eos_ids) | ({pad} if pad is not None else set())),
                                    device=self.device)
        self.end_token_ids = tuple(self.end_ids.tolist())
        self.forbid_end = forbid_end

    # ------------------------------------------------------------ prompt
    def prompt_ids(self, messages: list[dict]) -> list[int]:
        """The chat template with the thinking channel off, as for the autoregressive model, plus
        ``prefill`` (see :data:`EMPTY_THOUGHT`)."""
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                                  enable_thinking=False)
        if self.prefill and not text.endswith(self.prefill):
            text += self.prefill
        return self.tokenizer(text, add_special_tokens=False).input_ids

    def decode(self, ids: Sequence[int]) -> str:
        return self.tokenizer.decode(list(ids), skip_special_tokens=False)

    # ------------------------------------------------------------ blocks
    def start(self, prompt_ids: Sequence[int], seed: int) -> None:
        """Encode the prompt into a fresh cache and open the first block."""
        torch = self.torch
        from transformers import DynamicCache
        self.generator = torch.Generator(device=self.device).manual_seed(seed)
        self.cache = DynamicCache(config=self.model.config.get_text_config(decoder=True))
        self.length = 0                                   # tokens in the cache
        self._encode(list(prompt_ids), prefill=True)
        self._open_block()

    def close_block(self, block: Sequence[int]) -> None:
        """The block is fully committed: encode it into the cache, as the model's own loop appends a
        finished block, and open the next one."""
        assert len(block) == self.canvas_length
        self._encode(list(block), prefill=False)
        self._open_block()

    def _encode(self, ids: list[int], prefill: bool) -> None:
        torch = self.torch
        model = self.model
        input_ids = torch.tensor([ids], device=self.device)
        positions = torch.arange(self.length, self.length + len(ids), dtype=torch.int32, device=self.device)[None]
        self.attention = torch.ones((1, self.length + len(ids)), dtype=torch.bool, device=self.device)
        dummy = torch.empty((1, len(ids), 0), dtype=model.dtype, device=self.device)
        masks = model.model.encoder.create_masks_for_generate(
            config=model.config, inputs_embeds=dummy, attention_mask=self.attention,
            past_key_values=self.cache, position_ids=positions, mm_token_type_ids=None)
        with torch.no_grad():
            out = model.model.encoder(input_ids=input_ids, attention_mask=masks, past_key_values=self.cache,
                                      position_ids=positions)
        self.cache = out.past_key_values
        self.length += len(ids)

    def _open_block(self) -> None:
        torch = self.torch
        model = self.model
        C = self.canvas_length
        self.positions = torch.arange(self.length, self.length + C, dtype=torch.int32, device=self.device)[None]
        decoder_attention = torch.nn.functional.pad(self.attention, (0, C), value=True)
        dummy = torch.empty((1, C, 1), dtype=torch.long, device=self.device)
        self.block_masks = model.model.decoder.create_diffusion_decoder_attention_mask(
            config=model.config, inputs_embeds=dummy, past_key_values=self.cache,
            decoder_attention_mask=decoder_attention)
        self.self_conditioning = None                     # the model's own start: no previous prediction
        self.draft = self._noise(self.canvas_length)      # the model's own start: uniform random tokens
        self.passes_in_block = 0

    def _noise(self, n: int):
        return self.torch.randint(0, self.vocab_size, (n,), device=self.device, generator=self.generator)

    def forget(self, from_pos: int) -> None:
        """Return the draft from ``from_pos`` on to noise (backtracking: the unfrozen tokens should not
        simply be proposed again)."""
        self.draft[from_pos:] = self._noise(self.canvas_length - from_pos)

    # ------------------------------------------------------------ one pass
    def denoise(self, frozen: Sequence[int], temperature: float) -> "CanvasPass":
        """One decoder pass over the block: the frozen prefix written and pinned, the model's draft after it.

        After the pass the draft of the open positions is updated as the model's own sampler does it
        (``EntropyBoundSampler``): every open position is sampled from the scaled prediction; the
        jointly confident ones (lowest entropy first, while Σ H − max H ≤ ``entropy_bound``) keep their
        sample; the others return to uniform noise."""
        torch = self.torch
        C, n = self.canvas_length, len(frozen)
        canvas = self.draft.clone()[None]
        conditioning = self.self_conditioning
        if n:
            frozen_ids = torch.tensor(list(frozen), device=self.device)
            canvas[0, :n] = frozen_ids
            if conditioning is not None:              # the frozen tokens are certain: a one-hot prediction
                conditioning[0, :n] = float("-inf")
                conditioning[0, torch.arange(n, device=self.device), frozen_ids] = 0.0
        with torch.no_grad():
            logits = self.model(decoder_input_ids=canvas, self_conditioning_logits=conditioning,
                                decoder_attention_mask=self.block_masks, past_key_values=self.cache,
                                decoder_position_ids=self.positions).logits[0]          # [C, V], float32
        scaled = logits / temperature
        if self.forbid_end:
            # The poem cannot end before the enforcer says so, anywhere in the block: the model's
            # end-of-text predictions are removed before they reach its proposals, its draft and its
            # self-conditioning (a logits processor, as in the model's own loop). The raw ``logits``
            # — kept for the traces — still show how much the model wanted to stop.
            scaled[:, self.end_ids] = float("-inf")
        # the next pass is conditioned on this prediction, as in the model's own loop
        self.self_conditioning = scaled[None].to(self.model.model.decoder.embed_tokens.weight.dtype)
        self.passes_in_block += 1
        p = CanvasPass(self, logits, scaled, first=n)
        # the model's own acceptance and renoising, on the open positions
        entropy = torch.tensor(p._entropy, device=self.device)
        order = torch.argsort(entropy)
        sorted_h = entropy[order]
        keep_sorted = torch.cumsum(sorted_h, 0) - sorted_h <= self.entropy_bound
        keep = torch.zeros_like(keep_sorted).scatter(0, order, keep_sorted)
        tail = torch.where(keep, p._proposals, self._noise(C - n))
        self.draft = torch.cat([canvas[0, :n], tail])
        return p


class CanvasPass:
    """Predictions of one pass for the open positions ``first … canvas_length − 1``.

    Proposals and entropies are computed for all open positions at once on the
    GPU; the full distribution of a position is extracted only when the loop
    needs it (at most a few positions a pass).
    """

    def __init__(self, canvas: DiffusionGemmaCanvas, logits, scaled, first: int):
        torch = canvas.torch
        self.canvas, self.first = canvas, first
        self.logits = logits                              # T = 1
        open_scaled = scaled[first:]
        log_probs = torch.log_softmax(open_scaled, dim=-1)
        probs = log_probs.exp()
        self._entropy = (-(probs * log_probs).sum(-1)).tolist()
        self._proposals = torch.multinomial(probs, 1, generator=canvas.generator).squeeze(-1)
        self._log_probs = log_probs                       # scaled, open positions
        self._proposal_list = self._proposals.tolist()
        self._dist: dict[int, Distribution] = {}

    def proposal(self, pos: int) -> int:
        return self._proposal_list[pos - self.first]

    def entropy(self, pos: int) -> float:
        return self._entropy[pos - self.first]

    def p_scaled(self, pos: int, token_id: int) -> float:
        return float(self._log_probs[pos - self.first, token_id].exp())

    def distribution(self, pos: int) -> Distribution:
        if pos not in self._dist:
            torch = self.canvas.torch
            z = self.logits[pos]
            lse = torch.logsumexp(z, dim=0)
            logp = z - lse
            top = torch.topk(z, self.canvas.top_k)
            self._dist[pos] = Distribution(
                slice_logits=z.index_select(0, self.canvas.slice).tolist(), lse=float(lse),
                entropy=float(-(logp.exp() * logp).sum()),
                top=list(zip(top.indices.tolist(), top.values.tolist())))
        return self._dist[pos]

    def rank(self, pos: int, token_id: int) -> int:
        z = self.logits[pos]
        return int((z > z[token_id]).sum()) + 1

    def logp(self, pos: int, token_id: int) -> float:
        return float(self.logits[pos, token_id]) - self.distribution(pos).lse


# ----------------------------------------------------------------------------
# the random-logit control
# ----------------------------------------------------------------------------
class RandomCanvas:
    """Standard-normal logits over the vocabulary slice at every position, no model.

    The same interface as :class:`DiffusionGemmaCanvas`, for testing the loop.
    ``canvas_length`` is small by default so that tests cross block boundaries.

    >>> ix = TokenIndex.from_texts([(1, "క"), (2, "\\n")])
    >>> c = RandomCanvas(ix, canvas_length=4); c.start([], seed=0)
    >>> p = c.denoise([1], temperature=0.8); p.first, p.proposal(1) in (1, 2)
    (1, True)
    """

    forbid_end = False                                     # it never proposes an end token
    end_token_ids: tuple[int, ...] = ()

    def __init__(self, index: TokenIndex, canvas_length: int = 32, top_k: int = 5):
        self.index = index
        self.canvas_length = canvas_length
        self.top_k = top_k
        self.passes_in_block = 0

    def prompt_ids(self, messages: list[dict]) -> list[int]:
        return []

    def decode(self, ids: Sequence[int]) -> str:
        return "".join(self.index.texts[self.index.position(i)] for i in ids if self.index.position(i) is not None)

    def start(self, prompt_ids: Sequence[int], seed: int) -> None:
        self.rng = random.Random(seed)
        self.passes_in_block = 0

    def close_block(self, block: Sequence[int]) -> None:
        assert len(block) == self.canvas_length
        self.passes_in_block = 0

    def forget(self, from_pos: int) -> None:
        """No draft to forget: every pass is fresh noise."""

    def denoise(self, frozen: Sequence[int], temperature: float) -> "RandomPass":
        self.passes_in_block += 1
        return RandomPass(self, len(frozen), temperature)


class RandomPass:
    def __init__(self, canvas: RandomCanvas, first: int, temperature: float):
        self.canvas, self.first, self.temperature = canvas, first, temperature
        self._z: dict[int, list[float]] = {}
        self._prop: dict[int, int] = {}

    def _logits(self, pos: int) -> list[float]:
        if pos not in self._z:
            self._z[pos] = [self.canvas.rng.gauss(0.0, 1.0) for _ in self.canvas.index.ids]
        return self._z[pos]

    def _scaled_probs(self, pos: int) -> list[float]:
        z = [x / self.temperature for x in self._logits(pos)]
        m = max(z)
        w = [math.exp(x - m) for x in z]
        tot = sum(w)
        return [x / tot for x in w]

    def proposal(self, pos: int) -> int:
        if pos not in self._prop:
            probs = self._scaled_probs(pos)
            r, acc = self.canvas.rng.random(), 0.0
            choice = len(probs) - 1
            for i, p in enumerate(probs):
                acc += p
                if r < acc:
                    choice = i
                    break
            self._prop[pos] = self.canvas.index.ids[choice]
        return self._prop[pos]

    def entropy(self, pos: int) -> float:
        return -sum(p * math.log(p) for p in self._scaled_probs(pos) if p > 0)

    def p_scaled(self, pos: int, token_id: int) -> float:
        i = self.canvas.index.position(token_id)
        return self._scaled_probs(pos)[i] if i is not None else 0.0

    def distribution(self, pos: int) -> Distribution:
        z = self._logits(pos)
        lse = logsumexp(z)
        ent = -sum(math.exp(x - lse) * (x - lse) for x in z)
        top = sorted(((self.canvas.index.ids[i], x) for i, x in enumerate(z)), key=lambda t: -t[1])[: self.canvas.top_k]
        return Distribution(z, lse, ent, top)

    def rank(self, pos: int, token_id: int) -> int:
        z = self._logits(pos)
        i = self.canvas.index.position(token_id)
        x = z[i] if i is not None else float("-inf")
        return 1 + sum(1 for y in z if y > x)

    def logp(self, pos: int, token_id: int) -> float:
        i = self.canvas.index.position(token_id)
        return self._logits(pos)[i] - logsumexp(self._logits(pos)) if i is not None else float("-inf")
