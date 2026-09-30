"""Stage 3 soft word lexicon (PLAN §6.3): a trie over akshara-token ids.

Built only from training-split sources (Bhagavatam is held out):
  * every word of the training poems,
  * the ``word`` and ``split`` pieces of their gloss rows,
  * prose words seen at least ``min_prose`` times in a sample of the pretraining train split.

    uv run --project ../diffusion_pretraining python -m ft.lexicon            # -> data/lexicon/

The trie is stored as sorted edge arrays (CSR): children of node n are
child_tok[off[n]:off[n+1]] (sorted) -> child_node[...]; ``terminal[n]`` marks a word end.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path

import numpy as np

from . import DATA_DIR, PRETRAIN_ROOT

TOKEN_DIR = PRETRAIN_ROOT.parent / "pretraining_datasets" / "tokens"
_WORD = re.compile(r"[ఀ-౥౰-౿]+")


class Trie:
    def __init__(self, off: np.ndarray, child_tok: np.ndarray, child_node: np.ndarray, terminal: np.ndarray):
        self.off, self.child_tok, self.child_node, self.terminal = off, child_tok, child_node, terminal

    @classmethod
    def build(cls, seqs) -> "Trie":
        seqs = sorted(set(tuple(s) for s in seqs if s))
        parent, tokn, term = [], [], [False]            # node 0 = root
        stack: list[tuple[int, int]] = []               # (token, node) along the current path
        for s in seqs:
            k = 0
            while k < len(stack) and k < len(s) and stack[k][0] == s[k]:
                k += 1
            del stack[k:]
            node = stack[-1][1] if stack else 0
            for t in s[k:]:
                new = len(term)
                term.append(False)
                parent.append(node)
                tokn.append(t)
                stack.append((t, new))
                node = new
            term[node] = True
        parent = np.asarray(parent, np.int64)
        tokn = np.asarray(tokn, np.int64)
        child = np.arange(1, len(term), dtype=np.int64)
        order = np.lexsort((tokn, parent))
        parent, tokn, child = parent[order], tokn[order], child[order]
        off = np.zeros(len(term) + 1, np.int64)
        np.add.at(off, parent + 1, 1)
        return cls(np.cumsum(off), tokn.astype(np.int32), child.astype(np.int32), np.asarray(term, bool))

    def children(self, node: int) -> tuple[np.ndarray, np.ndarray]:
        a, b = self.off[node], self.off[node + 1]
        return self.child_tok[a:b], self.child_node[a:b]

    def step(self, node: int, token: int) -> int:
        """Child of ``node`` through ``token``; -1 if there is none."""
        toks, nodes = self.children(node)
        k = int(np.searchsorted(toks, token))
        return int(nodes[k]) if k < len(toks) and toks[k] == token else -1

    def contains(self, seq) -> bool:
        node = 0
        for t in seq:
            node = self.step(node, t)
            if node < 0:
                return False
        return bool(self.terminal[node])

    def save(self, path: Path) -> None:
        np.savez_compressed(path, off=self.off, child_tok=self.child_tok, child_node=self.child_node, terminal=self.terminal)

    @classmethod
    def load(cls, path: Path) -> "Trie":
        z = np.load(path)
        return cls(z["off"], z["child_tok"], z["child_node"], z["terminal"])


class LexiconScorer:
    """Per-particle word state and the soft penalty of PLAN §6.3.

    penalty(node) over the vocabulary: 0 for tokens continuing a lexicon word, -lam for any
    other syllable; at a word end, separators are free and a new word may start without a
    space at -lam2 (compounds, sandhi); inside a word, separators cost -lam."""

    def __init__(self, trie: Trie, tt, lam: float = 2.0, lam2: float = 0.5):
        self.trie, self.tt, self.lam, self.lam2 = trie, tt, lam, lam2
        self.root_toks = trie.children(0)[0]

    def penalty(self, node: int) -> np.ndarray:
        tt = self.tt
        pen = np.zeros(len(tt.is_syl), np.float32)
        if self.lam == 0:
            return pen
        pen[tt.is_syl] = -self.lam
        if node < 0:                                        # already off-lexicon inside this word
            pen[[tt.space, tt.newline, tt.eos]] = 0.0
            return pen
        toks, _ = self.trie.children(node)
        if node != 0 and self.trie.terminal[node]:
            pen[self.root_toks] = -self.lam2
        pen[toks] = 0.0
        if node == 0 or self.trie.terminal[node]:
            pen[[tt.space, tt.newline, tt.eos]] = 0.0
        else:
            pen[[tt.space, tt.newline, tt.eos]] = -self.lam
        return pen

    def advance(self, node: int, token: int) -> int:
        tt = self.tt
        if token in (tt.space, tt.newline, tt.eos):
            return 0
        if node < 0:
            return -1
        nxt = self.trie.step(node, token)
        if nxt < 0 and node != 0 and self.trie.terminal[node]:     # a compound: start the next word
            nxt = self.trie.step(0, token)
        return nxt


# -----------------------------------------------------------------------------
# building
# -----------------------------------------------------------------------------
def poem_words(records: Path) -> collections.Counter:
    c = collections.Counter()
    with records.open(encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            for ln in r.get("lines") or []:
                c.update(_WORD.findall(ln))
            for g in r.get("glosses") or []:
                c.update(_WORD.findall(g[0]))
                if len(g) > 2 and g[2]:
                    c.update(_WORD.findall(g[2]))
    return c


def prose_words(tok, n_tokens: int, seed: int = 0) -> collections.Counter:
    rng = np.random.default_rng(seed)
    c = collections.Counter()
    for src, w in {"sangraha": 0.75, "indiccorp": 0.20, "wikipedia": 0.05}.items():
        arr = np.memmap(TOKEN_DIR / src / "train.bin", dtype=np.uint16, mode="r")
        for _ in range(max(1, int(n_tokens * w) // 500_000)):
            s = int(rng.integers(0, len(arr) - 500_000))
            c.update(_WORD.findall(tok.decode(arr[s:s + 500_000].tolist())))
    return c


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data-dir", type=Path, default=DATA_DIR)
    ap.add_argument("--prose-tokens", type=int, default=100_000_000)
    ap.add_argument("--min-prose", type=int, default=3)
    args = ap.parse_args(argv)
    from tokenizer import load_default
    tok = load_default()
    out = args.data_dir / "lexicon"
    out.mkdir(parents=True, exist_ok=True)
    poems = poem_words(args.data_dir / "records" / "train.jsonl")
    prose = prose_words(tok, args.prose_tokens)
    words = set(poems) | {w for w, n in prose.items() if n >= args.min_prose}
    seqs = [tok.encode(w) for w in words]
    trie = Trie.build(seqs)
    trie.save(out / "trie.npz")
    meta = {"words": len(words), "poem_words": len(poems), "prose_words_kept": sum(1 for n in prose.values() if n >= args.min_prose),
            "nodes": int(len(trie.terminal)), "prose_tokens_sampled": args.prose_tokens, "min_prose": args.min_prose}
    (out / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(meta, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
