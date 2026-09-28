"""Syllable-aware Telugu tokenizer with a byte-BPE failover (zero OOV).

Design (two levels)
-------------------
1. **Segment** text into aksharas (orthographic syllables) with aksharanusarika
   (the meter engine's splitter, via ``aksharanusarika_split.py``), after
   ``akshara.normalize``.  Lossless: ``"".join(pieces) == normalize(text)``.
2. **Primary — one token per syllable.**  Every sufficiently frequent Telugu
   akshara is an *atomic* token.  This is the "ideally, every syllable is its
   own token" path.  Numbers are first-class: each digit (ASCII 0-9 and Telugu
   ౦-౯) is its own token.
3. **Failover — byte-level BPE (Telugu only).**  A rare or *unseen* akshara that
   has no atomic token is encoded by a byte-level BPE trained on Telugu
   aksharas.  Its base alphabet is the 256 raw bytes, so it always bottoms out —
   **OOV is impossible by construction**, for any input whatsoever.

Scope: only Telugu + numbers are *modeled*.  Text in other languages/scripts is
"ignored" in the modelling sense — no dedicated tokens, no BPE merges spent on
it — but is still preserved losslessly through the 256-byte base so it never
OOVs.  (Configurable via ``foreign``: ``"bytes"`` keeps it, ``"drop"`` discards
it, ``"unk"`` collapses each foreign run to a single <unk>.)

Guarantees (see tests/):
* ``decode(encode(t)) == normalize(t)``           for foreign="bytes"  (lossless)
* ``encode`` never raises / never yields OOV       for ANY unicode input
"""
from __future__ import annotations

import json
import re
from collections import Counter
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from . import akshara
from .aksharanusarika_split import aksharas
from .bpe import ByteBPE, train_byte_bpe

# --- unicode ranges we treat as "in scope" -------------------------------
_TEL_LO, _TEL_HI = 0x0C00, 0x0C7F
_TEL_DIGITS = [chr(c) for c in range(0x0C66, 0x0C70)]        # ౦..౯
_ASCII_DIGITS = [chr(c) for c in range(0x30, 0x3A)]          # 0..9
# Split a non-Telugu run into: one piece per ASCII digit | whitespace run | other run.
_FOREIGN_SPLIT = re.compile(r"[0-9]|\s+|[^0-9\s]+")

DEFAULT_SPECIALS = ["<pad>", "<unk>", "<bos>", "<eos>", "<mask>"]


def _is_telugu_char(ch: str) -> bool:
    return _TEL_LO <= ord(ch) <= _TEL_HI


def _is_telugu_digit_run(piece: str) -> bool:
    return all(0x0C66 <= ord(c) <= 0x0C6F for c in piece)


def _is_syllabic_akshara(piece: str) -> bool:
    """True for a real Telugu syllable (consonant/independent-vowel nucleus).

    Excludes digit runs, the standalone avagraha, and orphan combining shards
    (a stray matra/virama/anusvara) — those are failover material, not syllables.
    """
    if not piece:
        return False
    c0 = piece[0]
    if not _is_telugu_char(c0):
        return False
    if 0x0C66 <= ord(c0) <= 0x0C6F:      # Telugu digit
        return False
    if c0 == "ఽ":                    # avagraha, standalone
        return False
    return akshara.emittable(piece)       # False if it opens with a combining mark


class SyllableAwareTeluguTokenizer:
    # -------------------------------------------------------------- construct
    def __init__(
        self,
        specials: Optional[List[str]] = None,
        bpe: Optional[ByteBPE] = None,
        atomic_aksharas: Optional[Sequence[str]] = None,
        foreign: str = "bytes",
    ):
        self.specials: List[str] = list(specials or DEFAULT_SPECIALS)
        if foreign not in ("bytes", "drop", "unk"):
            raise ValueError("foreign must be 'bytes', 'drop', or 'unk'")
        self.foreign = foreign
        self.bpe = bpe if bpe is not None else ByteBPE([])
        self._atomic_aksharas = list(atomic_aksharas or [])
        self._build_vocab(self._atomic_aksharas)

    def _build_vocab(self, atomic_aksharas: Sequence[str]) -> None:
        """Assign contiguous ids and build all lookup tables.

        Layout: specials | 256 base bytes | BPE merges | Telugu digits | aksharas.
        Byte-identical tokens are de-duplicated (a frequent akshara that BPE
        already represents as one token reuses that id instead of wasting a slot).
        """
        self.id_to_bytes: List[Optional[bytes]] = []
        self.id_to_str: List[str] = []
        self.bytes_to_id: Dict[bytes, int] = {}

        # 1) specials — no byte value; decode to nothing.
        self.special_to_id: Dict[str, int] = {}
        for s in self.specials:
            i = len(self.id_to_bytes)
            self.special_to_id[s] = i
            self.id_to_bytes.append(None)
            self.id_to_str.append(s)
        self.special_ids = set(self.special_to_id.values())
        self.unk_id = self.special_to_id.get("<unk>")
        self.pad_id = self.special_to_id.get("<pad>")
        self.bos_id = self.special_to_id.get("<bos>")
        self.eos_id = self.special_to_id.get("<eos>")

        def _add(tok_bytes: bytes, display: str) -> int:
            existing = self.bytes_to_id.get(tok_bytes)
            if existing is not None:
                return existing
            i = len(self.id_to_bytes)
            self.id_to_bytes.append(tok_bytes)
            self.id_to_str.append(display)
            self.bytes_to_id[tok_bytes] = i
            return i

        # 2) byte-BPE vocabulary (256 base bytes first -> guarantees no OOV).
        for tok in self.bpe.tokens():
            try:
                disp = tok.decode("utf-8")
            except UnicodeDecodeError:
                disp = "<0x%s>" % tok.hex().upper() if len(tok) == 1 else "<bytes:%s>" % tok.hex()
            _add(tok, disp)

        # 3) numbers: each Telugu digit its own token (ASCII digits are base bytes).
        self.digit_to_id: Dict[str, int] = {}
        for d in _TEL_DIGITS:
            self.digit_to_id[d] = _add(d.encode("utf-8"), d)

        # 4) atomic syllables — one token per frequent akshara.
        self.akshara_to_id: Dict[str, int] = {}
        for ak in atomic_aksharas:
            self.akshara_to_id[ak] = _add(ak.encode("utf-8"), ak)

        # Direct piece->id lookup used at encode time: syllables + Telugu digits.
        # (ASCII digits are single base-byte tokens, reached via the failover.)
        self.piece_to_id: Dict[str, int] = dict(self.digit_to_id)
        self.piece_to_id.update(self.akshara_to_id)

        self.vocab_size = len(self.id_to_bytes)
        self._emit_cache: Optional[List[bool]] = None

    # ------------------------------------------------------------ pretokenize
    def pretokenize(self, text: str) -> List[str]:
        """Normalize then segment into modelling pieces.

        Piece kinds: Telugu syllable | single digit (ASCII/Telugu) | whitespace
        run | other-foreign run.  Lossless: ``"".join(out) == normalize(text)``.
        """
        text = akshara.normalize(text)
        out: List[str] = []
        for p in aksharas(text):
            if not p:
                continue
            if _is_telugu_char(p[0]):
                if _is_telugu_digit_run(p):
                    out.extend(p)              # one Telugu digit per piece
                else:
                    out.append(p)              # syllable
            else:
                out.extend(_FOREIGN_SPLIT.findall(p))  # digits / whitespace / other
        return out

    def syllabify(self, text: str) -> List[str]:
        """Public alias: the syllable/piece segmentation (for inspection)."""
        return self.pretokenize(text)

    # ------------------------------------------------------------------ encode
    def _is_foreign(self, piece: str) -> bool:
        """Foreign = this piece carries a letter from a non-Telugu script.

        A piece that is purely whitespace / punctuation / symbols / digits is
        script-neutral structure and is never foreign, so *standalone*
        punctuation and whitespace survive foreign='drop'/'unk'.  Punctuation
        fused into a foreign word with no separator (e.g. "COVID-19",
        "www.site.com") lives in the same piece and is dropped/collapsed with
        it; only the default foreign='bytes' keeps every byte.
        """
        for ch in piece:
            if _is_telugu_char(ch):
                return False
            if ch.isalpha():
                return True
        return False

    def _encode_piece(self, piece: str, ids: List[int]) -> None:
        # 1) atomic syllable or Telugu digit?
        aid = self.piece_to_id.get(piece)
        if aid is not None:
            ids.append(aid)
            return
        # 2) foreign handling (drop / unk) short-circuits before byte fallback.
        if self.foreign != "bytes" and self._is_foreign(piece):
            if self.foreign == "unk" and self.unk_id is not None:
                ids.append(self.unk_id)
            return  # "drop": emit nothing
        # 3) byte-level BPE failover — always succeeds (256-byte base).
        # surrogatepass so a lone surrogate (invalid strict UTF-8, but a legal
        # Python str) is encoded as WTF-8 bytes rather than raising.
        for tok in self.bpe.encode(piece.encode("utf-8", "surrogatepass")):
            ids.append(self.bytes_to_id[tok])

    def encode(
        self,
        text: str,
        add_bos: bool = False,
        add_eos: bool = False,
    ) -> List[int]:
        ids: List[int] = []
        if add_bos and self.bos_id is not None:
            ids.append(self.bos_id)
        for piece in self.pretokenize(text):
            self._encode_piece(piece, ids)
        if add_eos and self.eos_id is not None:
            ids.append(self.eos_id)
        return ids

    def encode_batch(self, texts: Iterable[str], **kw) -> List[List[int]]:
        return [self.encode(t, **kw) for t in texts]

    def encode_with_stats(self, text: str) -> Tuple[List[int], int, int]:
        """encode(), plus the number of Telugu pieces and how many of them have no
        atomic token (rare aksharas, orphan signs) — a high share means garbled text."""
        ids: List[int] = []
        telugu = rare = 0
        for piece in self.pretokenize(text):
            if _is_telugu_char(piece[0]) and not _is_telugu_digit_run(piece):
                telugu += 1
                rare += piece not in self.piece_to_id
            self._encode_piece(piece, ids)
        return ids, telugu, rare

    # ------------------------------------------------------------------ decode
    def decode(self, ids: Sequence[int], skip_special: bool = True) -> str:
        chunks: List[bytes] = []
        for i in ids:
            if i < 0 or i >= self.vocab_size:
                continue
            b = self.id_to_bytes[i]
            if b is None:  # special
                if not skip_special:
                    chunks.append(self.id_to_str[i].encode("utf-8"))
                continue
            chunks.append(b)
        raw = b"".join(chunks)
        # surrogatepass round-trips WTF-8 (lone surrogates) exactly; the replace
        # fallback keeps decode total for arbitrary/hand-crafted id sequences.
        try:
            return raw.decode("utf-8", "surrogatepass")
        except UnicodeDecodeError:
            return raw.decode("utf-8", "replace")

    def tokens(self, ids: Sequence[int]) -> List[str]:
        """Human-readable token strings, for inspection."""
        return [self.id_to_str[i] if 0 <= i < self.vocab_size else "<oob>" for i in ids]

    # ------------------------------------------------ decode-time masks (advisory)
    def emittable_mask(self) -> List[bool]:
        """Per-id: is this a clean, standalone-emittable text unit?

        Masks failover shards (orphan matra / bare virama / stray anusvara /
        mid-codepoint byte fragments) and specials, per ``akshara.emittable``.
        Advisory helper for constrained generation; not needed for encode/decode.
        """
        if self._emit_cache is not None:
            return self._emit_cache
        mask: List[bool] = []
        for i in range(self.vocab_size):
            b = self.id_to_bytes[i]
            if b is None:
                mask.append(False)
                continue
            try:
                s = b.decode("utf-8")
            except UnicodeDecodeError:
                mask.append(False)       # partial-codepoint byte fragment
                continue
            mask.append(akshara.emittable(s))
        self._emit_cache = mask
        return mask

    def blocks_next(self, prev_id: int, next_id: int) -> bool:
        """Is the transition prev->next invalid Telugu (dangling virama)?

        Best-effort wrapper over ``akshara.blocks_next``; exact for
        atomic-syllable to atomic-syllable transitions, False otherwise.
        """
        if not (0 <= prev_id < self.vocab_size and 0 <= next_id < self.vocab_size):
            return False
        pb, nb = self.id_to_bytes[prev_id], self.id_to_bytes[next_id]
        if pb is None or nb is None:
            return False
        try:
            return akshara.blocks_next(pb.decode("utf-8"), nb.decode("utf-8"))
        except UnicodeDecodeError:
            return False

    # ------------------------------------------------------------- persistence
    def to_dict(self) -> dict:
        return {
            "format": "syllable-aware-telugu-tokenizer",
            "version": 1,
            "specials": self.specials,
            "foreign": self.foreign,
            "bpe_merges": self.bpe.to_json(),
            "atomic_aksharas": self._atomic_aksharas,
        }

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "SyllableAwareTeluguTokenizer":
        return cls(
            specials=d.get("specials"),
            bpe=ByteBPE.from_json(d.get("bpe_merges", [])),
            atomic_aksharas=d.get("atomic_aksharas", []),
            foreign=d.get("foreign", "bytes"),
        )

    @classmethod
    def load(cls, path: str) -> "SyllableAwareTeluguTokenizer":
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    # ---------------------------------------------------------------- training
    @classmethod
    def train(
        cls,
        corpus: Iterable[str],
        vocab_size: int = 32000,
        num_bpe_merges: int = 4000,
        min_akshara_freq: int = 2,
        min_pair_freq: int = 2,
        specials: Optional[List[str]] = None,
        foreign: str = "bytes",
        extra_aksharas: Optional[Sequence[str]] = None,
        verbose: bool = True,
    ) -> "SyllableAwareTeluguTokenizer":
        """Learn the vocabulary from a stream of raw text lines.

        vocab_size       : soft target total vocab; atomic-akshara budget is
                           vocab_size - specials - 256 - merges - 10 digits.
        num_bpe_merges   : size of the Telugu byte-BPE failover.
        min_akshara_freq : an akshara needs at least this many occurrences to
                           earn an atomic token (rarer ones ride the failover).
        extra_aksharas   : aksharas to force into the atomic vocab even if
                           unseen/rare (e.g. a curated list, or the aksharas a
                           previous eval flagged as failover). Guarantees one
                           token each. Filtered to valid syllables, de-duped.
        """
        specials = list(specials or DEFAULT_SPECIALS)
        akshara_freq: Counter = Counter()
        # Reuse one tokenizer just for its (config-independent) pretokenizer.
        seg = cls(specials=specials, bpe=ByteBPE([]), atomic_aksharas=[], foreign=foreign)

        lines = corpus
        if verbose:
            try:
                from tqdm import tqdm
                lines = tqdm(corpus, desc="counting aksharas")
            except Exception:
                pass
        for line in lines:
            for p in seg.pretokenize(line):
                if _is_syllabic_akshara(p):
                    akshara_freq[p] += 1

        # Byte-BPE failover trained on Telugu aksharas only (weighted by freq).
        bpe_words: Dict[bytes, int] = {
            ak.encode("utf-8"): f for ak, f in akshara_freq.items()
        }
        bpe = train_byte_bpe(
            bpe_words, num_bpe_merges, min_pair_freq=min_pair_freq, verbose=verbose
        )

        # Atomic-akshara budget (numbers/base bytes/merges/specials are fixed).
        reserved = len(specials) + 256 + len(bpe.merges) + len(_TEL_DIGITS)
        budget = max(0, vocab_size - reserved)
        # Force-included aksharas come first (guaranteed a token), then the
        # frequency-ranked ones fill the remaining budget.
        forced = [a for a in dict.fromkeys(extra_aksharas or []) if _is_syllabic_akshara(a)]
        forced_set = set(forced)
        ranked = [ak for ak, f in akshara_freq.most_common()
                  if f >= min_akshara_freq and ak not in forced_set]
        atomic = (forced + ranked)[:budget]

        if verbose:
            print(
                f"[train] distinct aksharas={len(akshara_freq)} "
                f"bpe_merges={len(bpe.merges)} atomic_aksharas={len(atomic)} "
                f"(forced {len(forced)}, budget {budget})"
            )
        return cls(specials=specials, bpe=bpe, atomic_aksharas=atomic, foreign=foreign)

    # --------------------------------------------------------------- reporting
    def coverage(self, text: str) -> dict:
        """How the pieces of ``text`` are handled — a diagnostic, not required."""
        pieces = self.pretokenize(text)
        c = dict(atomic_syllable=0, failover_syllable=0, digit=0,
                 whitespace=0, punctuation=0, foreign=0)
        for p in pieces:
            c0 = p[0]
            if p in self.akshara_to_id:
                c["atomic_syllable"] += 1
            elif len(p) == 1 and (p in self.digit_to_id or "0" <= p <= "9"):
                c["digit"] += 1
            elif _is_telugu_char(c0) and not (0x0C66 <= ord(c0) <= 0x0C6F):
                c["failover_syllable"] += 1
            elif p.isspace():
                c["whitespace"] += 1
            elif self._is_foreign(p):
                c["foreign"] += 1
            else:
                c["punctuation"] += 1
        ids = self.encode(text)
        c["pieces"] = len(pieces)
        c["tokens"] = len(ids)
        c["tokens_per_piece"] = (len(ids) / len(pieces)) if pieces else 0.0
        return c
