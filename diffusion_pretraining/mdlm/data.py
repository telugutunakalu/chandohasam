"""Training batches: random 512-token windows from each source's token file, mixed by weight.

Token files are the <source>/{train,val,test}.bin written by data_prep.build_corpus
(uint16; every document as <bos> ... <eos>). A window may start inside a
document and span several (MDLM's "wrapped" setting). Batches are a pure
function of (seed, step), so a resumed run sees exactly the batches it would
have seen without the interruption.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import torch


class TokenMixture:
    def __init__(self, token_dir: Path, weights: dict[str, float], split: str = "train", seq_len: int = 512):
        self.seq_len = seq_len
        self.sources = [s for s, w in weights.items() if w > 0]
        self.arrays = [np.memmap(Path(token_dir) / s / f"{split}.bin", dtype=np.uint16, mode="r") for s in self.sources]
        w = np.array([weights[s] for s in self.sources], dtype=np.float64)
        self.probs = w / w.sum()
        for s, a in zip(self.sources, self.arrays):
            if len(a) <= seq_len:
                raise ValueError(f"{s}/{split}.bin has only {len(a)} tokens")

    def tokens(self) -> dict[str, int]:
        return {s: len(a) for s, a in zip(self.sources, self.arrays)}

    def batch(self, step: int, batch_size: int, seed: int = 0) -> torch.Tensor:
        rng = np.random.default_rng((seed, step))
        which = rng.choice(len(self.arrays), size=batch_size, p=self.probs)
        out = np.empty((batch_size, self.seq_len), dtype=np.int64)
        for i, a in enumerate(which):
            arr = self.arrays[a]
            start = int(rng.integers(0, len(arr) - self.seq_len))
            out[i] = arr[start:start + self.seq_len]
        return torch.from_numpy(out)


def fixed_canvases(token_dir: Path, source: str, split: str, n: int, seq_len: int = 512) -> torch.Tensor:
    """The first ``n`` non-overlapping windows of a split (deterministic evaluation set)."""
    arr = np.memmap(Path(token_dir) / source / f"{split}.bin", dtype=np.uint16, mode="r")
    n = min(n, len(arr) // seq_len)
    return torch.from_numpy(np.asarray(arr[: n * seq_len], dtype=np.int64).reshape(n, seq_len))
