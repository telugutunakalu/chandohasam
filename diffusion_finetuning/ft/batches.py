"""Training batches for both stages. Like pretraining, a batch is a pure function of
(seed, step), so a resumed run sees exactly the batches it would have seen.

Stage 1: random 512-token windows over the packed poem + meaning documents
(stage1/train.bin, with the per-token trainable flags of stage1/train.mask.bin), and a
``replay`` share of windows from the pretraining corpus.

Stage 2: ``batch_size`` (task, record) draws by the task mix, each turned into a canvas;
the trainer groups them by canvas length (128 / 256 / 384 / 512).
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import torch

from mdlm.data import TokenMixture

from .canvas import GIVEN, TARGET, TASKS, Pools, Rec, Vocab, build


class Stage1Batches:
    def __init__(self, data_dir: Path, token_dir: Path, replay: float, replay_weights: dict, seq_len: int = 512):
        self.docs = np.memmap(data_dir / "stage1" / "train.bin", dtype=np.uint16, mode="r")
        self.flags = np.memmap(data_dir / "stage1" / "train.mask.bin", dtype=np.uint8, mode="r")
        assert len(self.docs) == len(self.flags) > seq_len
        self.replay = replay
        self.general = TokenMixture(token_dir, replay_weights, "train", seq_len) if replay > 0 else None
        self.seq_len = seq_len

    def poem_tokens(self) -> int:
        return len(self.docs)

    def batch(self, step: int, batch_size: int, seed: int) -> tuple[torch.Tensor, torch.Tensor]:
        rng = np.random.default_rng((seed, step, 1))
        L = self.seq_len
        x = np.empty((batch_size, L), dtype=np.int64)
        roles = np.empty((batch_size, L), dtype=np.int8)
        for i in range(batch_size):
            if self.general is not None and rng.random() < self.replay:
                arr = self.general.arrays[int(rng.choice(len(self.general.arrays), p=self.general.probs))]
                s = int(rng.integers(0, len(arr) - L))
                x[i] = arr[s:s + L]
                roles[i] = TARGET
            else:
                s = int(rng.integers(0, len(self.docs) - L))
                x[i] = self.docs[s:s + L]
                roles[i] = np.where(self.flags[s:s + L] > 0, TARGET, GIVEN)
        return torch.from_numpy(x), torch.from_numpy(roles)


class Stage2Batches:
    def __init__(self, recs: list[Rec], vocab: Vocab, mix: dict[str, float]):
        self.v = vocab
        self.pools = Pools(recs)
        self.tasks = [t for t in TASKS if mix.get(t, 0) > 0]
        p = np.asarray([mix[t] for t in self.tasks], dtype=np.float64)
        self.p = p / p.sum()
        self.mix = dict(zip(self.tasks, self.p))
        empty = [t for t in self.tasks if self.pools.sizes()[t] == 0]
        if empty:
            raise ValueError(f"no records for tasks {empty}")

    def steps_per_epoch(self, batch_size: int) -> int:
        """One epoch = one pass over the T1 pool (PLAN §5.5)."""
        return max(1, int(round(self.pools.sizes()["T1"] / (batch_size * self.mix.get("T1", 1.0)))))

    def batch(self, step: int, batch_size: int, seed: int) -> list[tuple[str, np.ndarray, np.ndarray]]:
        rng = np.random.default_rng((seed, step, 2))
        out = []
        for task in rng.choice(self.tasks, size=batch_size, p=self.p):
            for _ in range(16):                       # a record whose canvas does not fit: draw again
                c = build(str(task), self.v, self.pools.draw(str(task), rng), rng)
                if c is not None:
                    out.append((str(task), c[0], c[1]))
                    break
        return out


def group_by_length(examples, micro_tokens: int):
    """Micro-batches of equal-length canvases, at most ``micro_tokens`` tokens each:
    yields (tasks, ids (B, L) int64, roles (B, L) int8)."""
    by_len: dict[int, list] = {}
    for task, ids, roles in examples:
        by_len.setdefault(len(ids), []).append((task, ids, roles))
    for L in sorted(by_len):
        rows = by_len[L]
        per = max(1, micro_tokens // L)
        for i in range(0, len(rows), per):
            chunk = rows[i:i + per]
            yield ([c[0] for c in chunk], torch.from_numpy(np.stack([c[1] for c in chunk])),
                   torch.from_numpy(np.stack([c[2] for c in chunk])))
