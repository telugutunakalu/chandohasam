# -*- coding: utf-8 -*-
"""
The vocabulary slice a constrained decoder chooses from.

IndicNeuroSym's static mask: the model's Telugu tokens plus space and
newline. Texts come from the tokenizer's own ``decode``, so the enforcer sees
exactly the text the verifier will scan (Gemma-4: 0 mismatches over 1,786
tokens and 3,000 random sequences). Tokens carrying zero-width characters are
left out; the orthography filter would reject them anyway.

Owns: :class:`TokenIndex`. Must not import torch.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional, Sequence

TELUGU_TOKEN = re.compile(r"^ ?[ఀ-౥]+$")       # optional leading space, then Telugu letters and signs
                                                          # (digits ౦–౯ and the fraction signs U+0C66– are left out)
SPIECE_SPACE = "▁"


@dataclass(frozen=True)
class TokenIndex:
    """Token ids of the slice, their texts, and where newline and space sit in it."""
    ids: tuple[int, ...]
    texts: tuple[str, ...]
    newline: int                         # position (not id) of the newline token in ``ids``
    space: Optional[int]                 # position of the bare-space token, if any
    eos_ids: tuple[int, ...] = ()        # model end-of-sequence ids (outside the slice)
    _pos: dict = field(default_factory=dict, compare=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "_pos", {t: i for i, t in enumerate(self.ids)})

    @property
    def size(self) -> int:
        return len(self.ids)

    def position(self, token_id: int) -> Optional[int]:
        """Position of a token id in the slice (None when outside it)."""
        return self._pos.get(token_id)

    @classmethod
    def from_texts(cls, pairs: Iterable[tuple[int, str]], eos_ids: Sequence[int] = ()) -> "TokenIndex":
        """Build from ``(token_id, text)`` pairs; must contain ``"\\n"``.

        >>> ix = TokenIndex.from_texts([(5, "క"), (6, " రా"), (107, "\\n"), (9, " ")])
        >>> ix.size, ix.texts[ix.newline], ix.space, ix.position(6)
        (4, '\\n', 3, 1)
        """
        pairs = list(pairs)
        ids = tuple(i for i, _ in pairs)
        texts = tuple(t for _, t in pairs)
        if "\n" not in texts:
            raise ValueError("the slice needs a newline token")
        space = texts.index(" ") if " " in texts else None
        return cls(ids=ids, texts=texts, newline=texts.index("\n"), space=space, eos_ids=tuple(eos_ids))

    @classmethod
    def from_tokenizer(cls, tokenizer, eos_ids: Sequence[int] = ()) -> "TokenIndex":
        """Every token that decodes to Telugu (optionally after one space), plus newline and space."""
        vocab = tokenizer.get_vocab()
        pairs: list[tuple[int, str]] = []
        for tok, i in sorted(vocab.items(), key=lambda kv: kv[1]):
            if not TELUGU_TOKEN.match(tok.replace(SPIECE_SPACE, " ")):
                continue
            text = tokenizer.decode([i])
            if TELUGU_TOKEN.match(text):
                pairs.append((i, text))
        for special in ("\n", " "):
            tid = _single_token_id(tokenizer, special)
            if tid is None:
                if special == "\n":
                    raise ValueError("the tokenizer has no single newline token")
                continue
            pairs.append((tid, special))
        return cls.from_texts(pairs, eos_ids=eos_ids)


def _single_token_id(tokenizer, text: str) -> Optional[int]:
    """The id of the one token that decodes to ``text``, if there is one."""
    candidates = [text, text.replace(" ", SPIECE_SPACE)]
    vocab = tokenizer.get_vocab()
    for c in candidates:
        tid = vocab.get(c)
        if tid is not None and tokenizer.decode([tid]) == text:
            return tid
    ids = tokenizer.encode(text, add_special_tokens=False)
    if len(ids) == 1 and tokenizer.decode(ids) == text:
        return ids[0]
    return None
