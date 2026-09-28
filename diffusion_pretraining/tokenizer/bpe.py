"""Byte-level BPE — the OOV-proof failover layer for the syllable tokenizer.

Why byte level?  The base alphabet is the 256 raw bytes, so *any* UTF-8 string
can be encoded as a sequence of base tokens in the worst case.  There is no
`<unk>`: OOV is impossible by construction, independent of how well BPE was
trained.  Merges only make the failover *shorter* (fewer tokens for a rare
akshara or a stray Latin word); they never affect whether encoding succeeds.

The trainer is the classic Sennrich-style pair-merge algorithm with an
incremental pair index + lazy heap, so it scales to the whole corpus.  Input is
a `{piece_bytes: frequency}` table produced by the tokenizer's pre-tokenizer,
i.e. BPE never merges across akshara / word boundaries — those boundaries are
already baked into the pieces it is handed.
"""
from __future__ import annotations
import heapq
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


class ByteBPE:
    """A trained byte-level BPE model: apply-merges encoder + vocabulary view.

    A "token" here is a ``bytes`` value.  The vocabulary is the 256 single
    bytes followed by one entry per learned merge (in merge order).
    """

    def __init__(self, merges: List[Tuple[bytes, bytes]]):
        self.merges: List[Tuple[bytes, bytes]] = list(merges)
        # rank[(a, b)] = position in the merge list; lower = merged earlier.
        self.ranks: Dict[Tuple[bytes, bytes], int] = {
            pair: i for i, pair in enumerate(self.merges)
        }
        self._cache: Dict[bytes, Tuple[bytes, ...]] = {}

    # ------------------------------------------------------------------ vocab
    def tokens(self) -> List[bytes]:
        """Every token this model can emit: 256 base bytes + merge results,
        in a fixed, reproducible order."""
        toks = [bytes([i]) for i in range(256)]
        for a, b in self.merges:
            toks.append(a + b)
        return toks

    # ---------------------------------------------------------------- encode
    def encode(self, data: bytes) -> Tuple[bytes, ...]:
        """Encode a piece's bytes into a tuple of token byte-strings.

        Greedy: repeatedly merge the adjacent pair with the lowest rank until
        no learned pair remains.  Always terminates in base tokens, so the
        output is guaranteed to be encodable by the parent tokenizer.
        """
        if not data:
            return ()
        cached = self._cache.get(data)
        if cached is not None:
            return cached

        symbols: List[bytes] = [bytes([b]) for b in data]
        ranks = self.ranks
        while len(symbols) > 1:
            best_rank = None
            best_i = -1
            for i in range(len(symbols) - 1):
                r = ranks.get((symbols[i], symbols[i + 1]))
                if r is not None and (best_rank is None or r < best_rank):
                    best_rank = r
                    best_i = i
            if best_i < 0:
                break
            symbols[best_i : best_i + 2] = [symbols[best_i] + symbols[best_i + 1]]

        out = tuple(symbols)
        self._cache[data] = out
        return out

    # -------------------------------------------------------------- (de)serialize
    def to_json(self) -> List[List[str]]:
        """Merges as [hexA, hexB] pairs (hex is portable for arbitrary bytes)."""
        return [[a.hex(), b.hex()] for a, b in self.merges]

    @classmethod
    def from_json(cls, data: List[List[str]]) -> "ByteBPE":
        return cls([(bytes.fromhex(a), bytes.fromhex(b)) for a, b in data])


def train_byte_bpe(
    word_freqs: Dict[bytes, int],
    num_merges: int,
    min_pair_freq: int = 2,
    verbose: bool = False,
) -> ByteBPE:
    """Learn ``num_merges`` merges from a byte-piece frequency table.

    word_freqs : {piece_as_bytes: count}.  Each piece is one pre-token unit
                 (a rare akshara, a Latin word, a whitespace run, ...).  BPE
                 stays inside these units.
    min_pair_freq : stop early once the best pair is rarer than this.
    """
    # Each word is a list of integer symbol ids; ids 0..255 are the raw bytes,
    # ids >= 256 are merged symbols. sym_bytes maps id -> its byte-string.
    sym_bytes: List[bytes] = [bytes([i]) for i in range(256)]

    words: List[List[int]] = []
    freqs: List[int] = []
    for w, f in word_freqs.items():
        if not w or f <= 0:
            continue
        words.append(list(w))  # ints 0..255
        freqs.append(f)

    # pair_freq[(a,b)] = total weighted count; pair_words[(a,b)] = word indices.
    pair_freq: Counter = Counter()
    pair_words: Dict[Tuple[int, int], set] = defaultdict(set)
    for i, syms in enumerate(words):
        f = freqs[i]
        for a, b in zip(syms, syms[1:]):
            pair_freq[(a, b)] += f
            pair_words[(a, b)].add(i)

    # Lazy max-heap keyed by (-freq, pair); stale entries are filtered on pop.
    heap = [(-c, p) for p, c in pair_freq.items()]
    heapq.heapify(heap)

    merges: List[Tuple[int, int]] = []
    _rng = range(num_merges)
    if verbose:
        try:
            from tqdm import tqdm
            _rng = tqdm(_rng, desc="bpe merges")
        except Exception:
            pass

    for _ in _rng:
        # Pop until the heap top reflects a current, positive frequency.
        best = None
        best_f = 0
        while heap:
            neg_f, pair = heapq.heappop(heap)
            cur = pair_freq.get(pair, 0)
            if cur == -neg_f and cur > 0:
                best, best_f = pair, cur
                break
            # else: stale entry, discard.
        if best is None or best_f < min_pair_freq:
            break

        a, b = best
        new_id = len(sym_bytes)
        sym_bytes.append(sym_bytes[a] + sym_bytes[b])
        merges.append((a, b))

        touched_pairs = set()
        for i in list(pair_words[best]):
            old = words[i]
            f = freqs[i]
            # Remove this word's contribution to every adjacent pair.
            for x, y in zip(old, old[1:]):
                pair_freq[(x, y)] -= f
                pair_words[(x, y)].discard(i)
                touched_pairs.add((x, y))
            # Rebuild the word, merging every adjacent (a, b) into new_id.
            new: List[int] = []
            j = 0
            n = len(old)
            while j < n:
                if j < n - 1 and old[j] == a and old[j + 1] == b:
                    new.append(new_id)
                    j += 2
                else:
                    new.append(old[j])
                    j += 1
            words[i] = new
            # Add the rebuilt word's contribution back.
            for x, y in zip(new, new[1:]):
                pair_freq[(x, y)] += f
                pair_words[(x, y)].add(i)
                touched_pairs.add((x, y))

        # The merged pair is now fully consumed.
        pair_freq.pop(best, None)
        pair_words.pop(best, None)
        touched_pairs.discard(best)
        # Push refreshed entries for every pair whose count changed.
        for p in touched_pairs:
            c = pair_freq.get(p, 0)
            if c > 0:
                heapq.heappush(heap, (-c, p))

    return ByteBPE([(sym_bytes[a], sym_bytes[b]) for a, b in merges])
