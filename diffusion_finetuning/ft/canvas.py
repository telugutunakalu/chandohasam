"""Stage 2 canvases (PLAN §5.1): one poem record -> (token ids, roles) for one task.

Roles per position:
  GIVEN  (0)  clean in the input, never masked, no loss
  TARGET (1)  masked at rate t, loss, counted in the normaliser
  FILL   (2)  the <eos> run after a generated text: masked and scored like a target (so the
              model learns where the text ends) but left out of the normaliser, so a long
              bucket does not dilute the loss of the real tokens

Tasks: T1 metre + meaning -> poem; T0 the same with an empty meaning (for classifier-free
guidance); T2 poem -> meaning; T3 poem -> gloss meanings; T4 gloss meanings -> poetic words;
T5 metre + meaning + poem with a line or some words missing -> the missing spans.
A shared samasya / makuṭam line is part of the condition wherever it appears.
"""
from __future__ import annotations

import json
import pickle
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

from .text import GLOSS_KEY, LEXICON_KEY, MEANING_KEY, METRE_KEY, POEM_KEY, STYLE_KEY

GIVEN, TARGET, FILL = 0, 1, 2
TASKS = ("T1", "T2", "T3", "T4", "T5", "T0")
DEFAULT_MIX = {"T1": 0.40, "T2": 0.20, "T3": 0.10, "T4": 0.05, "T5": 0.15, "T0": 0.10}
BUCKETS = (128, 256, 384, 512)
METRE_OK = ("agree", "engine-only")
RARE_METRE = 500            # metres with fewer training poems are upsampled ...
MAX_UPSAMPLE = 5.0          # ... at most this much
DVIPADA_SHARE = 0.10        # cap on dvipada in the metre-conditioned tasks


@dataclass
class Rec:
    """One poem, pre-tokenised (uint16 arrays; lists of arrays for lines and glosses)."""
    id: str
    meter: str | None
    metre_ok: bool
    metre_head: np.ndarray | None           # "ఛందస్సు: X\n"
    style_head: np.ndarray                  # "శైలి: X\n"
    samasya_head: np.ndarray | None         # "సమస్య: <line>\n" / "మకుటం: <line>\n"
    meaning_line: np.ndarray | None         # "భావం (src): <meaning>\n"
    meaning_head: np.ndarray | None         # "భావం (src):\n"   (T2 puts the meaning below it)
    meaning_body: np.ndarray | None         # "<meaning>"
    lines: list = field(default_factory=list)        # one array per poem line
    glosses: list = field(default_factory=list)      # (word ids, meaning ids)
    samasya: bool = False                   # the last poem line is a given shared line


class Vocab:
    """Token ids of the fixed strings."""

    def __init__(self, tok):
        self.tok = tok
        e = lambda s: np.asarray(tok.encode(s), dtype=np.uint16)
        self.bos, self.eos = tok.bos_id, tok.eos_id
        self.nl = e("\n")
        self.poem_head = e(f"{POEM_KEY}:\n")
        self.empty_meaning = e(f"{MEANING_KEY}:\n")
        self.gloss_head = e(f"{GLOSS_KEY}:\n")
        self.lexicon_head = e(f"{LEXICON_KEY}:\n")
        self.eq = e(" = ")
        self.space = e(" ")
        self.enc = e


def tokenise_record(v: Vocab, r: dict) -> Rec:
    e = v.enc
    ok = r["status"] in METRE_OK and bool(r.get("meter_te"))
    m = r.get("meaning") or ""
    src = r.get("meaning_src") or ""
    sam = r.get("samasya")
    return Rec(
        id=r["id"], meter=r.get("meter") if ok else None, metre_ok=ok,
        metre_head=e(f"{METRE_KEY}: {r['meter_te']}\n") if ok else None,
        style_head=e(f"{STYLE_KEY}: {r['register']}\n"),
        samasya_head=e(f"{sam['kind']}: {sam['line']}\n") if sam else None,
        meaning_line=e(f"{MEANING_KEY} ({src}): {m}\n") if m else None,
        meaning_head=e(f"{MEANING_KEY} ({src}):\n") if m else None,
        meaning_body=e(m) if m else None,
        lines=[e(ln) for ln in r["lines"]],
        glosses=[(e(g[0]), e(g[1])) for g in r.get("glosses") or []],
        samasya=bool(sam),
    )


_WORKER_VOCAB: Vocab | None = None


def _tokenise_chunk(lines: list[str]) -> list[Rec]:
    global _WORKER_VOCAB
    if _WORKER_VOCAB is None:
        from tokenizer import load_default
        _WORKER_VOCAB = Vocab(load_default())
    out = []
    for line in lines:
        r = json.loads(line)
        if r.get("lines"):
            out.append(tokenise_record(_WORKER_VOCAB, r))
    return out


def load_records(path: Path, v: Vocab, cache: bool = True, workers: int = 12) -> list[Rec]:
    """Tokenised records of one split, cached next to the JSONL (keyed by its size and mtime).
    Tokenising the full train split takes ~10 min on one core, so it is spread over processes."""
    st = path.stat()
    cpath = path.with_suffix(f".{st.st_size}_{int(st.st_mtime)}.tok.pkl")
    if cache and cpath.exists():
        with cpath.open("rb") as fh:
            return pickle.load(fh)
    lines = path.read_text(encoding="utf-8").splitlines()
    chunks = [lines[i:i + 4000] for i in range(0, len(lines), 4000)]
    if workers > 1 and len(chunks) > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(min(workers, len(chunks))) as pool:
            recs = [r for part in pool.map(_tokenise_chunk, chunks) for r in part]
    else:
        recs = [tokenise_record(v, json.loads(ln)) for ln in lines if json.loads(ln).get("lines")]
    if cache:
        with cpath.open("wb") as fh:
            pickle.dump(recs, fh, protocol=pickle.HIGHEST_PROTOCOL)
    return recs


# -----------------------------------------------------------------------------
# canvas assembly
# -----------------------------------------------------------------------------
class _Builder:
    def __init__(self, v: Vocab):
        self.v, self.ids, self.roles = v, [v.bos], [GIVEN]

    def add(self, arr, role: int) -> None:
        if arr is None:
            return
        self.ids.extend(int(x) for x in arr)
        self.roles.extend([role] * len(arr))

    def finish(self, fill_role: int, min_fill: int = 1) -> tuple[np.ndarray, np.ndarray] | None:
        n = len(self.ids) + (min_fill if fill_role != GIVEN else 0)
        length = next((b for b in BUCKETS if b >= n), None)
        if length is None:
            return None
        pad = length - len(self.ids)
        ids = np.asarray(self.ids + [self.v.eos] * pad, dtype=np.int64)
        roles = np.asarray(self.roles + [fill_role] * pad, dtype=np.int8)
        return ids, roles


def _poem(b: _Builder, r: Rec, target_role: int, span_roles: list[np.ndarray] | None = None) -> None:
    """Poem lines separated by newlines. span_roles (T5) gives a role per token of each line;
    otherwise every token is target_role. A given samasya line and the newline before it stay GIVEN."""
    last = len(r.lines) - 1
    for i, ln in enumerate(r.lines):
        fixed = r.samasya and i == last
        if i:
            b.add(b.v.nl, GIVEN if (fixed or span_roles is not None) else target_role)
        if span_roles is not None:
            b.ids.extend(int(x) for x in ln)
            b.roles.extend(GIVEN if fixed else int(x) for x in span_roles[i])
        else:
            b.add(ln, GIVEN if fixed else target_role)


def canvas_T1(v: Vocab, r: Rec, empty_meaning: bool = False):
    b = _Builder(v)
    b.add(r.metre_head, GIVEN)
    b.add(r.style_head, GIVEN)
    b.add(r.samasya_head, GIVEN)
    b.add(v.empty_meaning if empty_meaning else r.meaning_line, GIVEN)
    b.add(v.poem_head, GIVEN)
    _poem(b, r, TARGET)
    return b.finish(FILL)


def canvas_T2(v: Vocab, r: Rec):
    b = _Builder(v)
    b.add(r.metre_head, GIVEN)
    b.add(r.style_head, GIVEN)
    b.add(v.poem_head, GIVEN)
    _poem(b, r, GIVEN)
    b.add(v.nl, GIVEN)
    b.add(r.meaning_head, GIVEN)
    b.add(r.meaning_body, TARGET)
    return b.finish(FILL)


def _rows(v: Vocab, r: Rec, rng: np.random.Generator, budget: int):
    """A random contiguous run of gloss rows whose tokens fit in ``budget``."""
    sizes = [len(w) + len(v.eq) + len(m) + len(v.nl) for w, m in r.glosses]
    start = 0 if sum(sizes) <= budget else int(rng.integers(0, len(sizes)))
    end, used = start, 0
    while end < len(sizes) and used + sizes[end] <= budget:
        used += sizes[end]
        end += 1
    return r.glosses[start:end]


def canvas_T3(v: Vocab, r: Rec, rng: np.random.Generator):
    b = _Builder(v)
    b.add(v.poem_head, GIVEN)
    _poem(b, r, GIVEN)
    b.add(v.nl, GIVEN)
    b.add(v.gloss_head, GIVEN)
    rows = _rows(v, r, rng, BUCKETS[-1] - len(b.ids) - 1)
    if not rows:
        return None
    for w, m in rows:
        b.add(w, GIVEN)
        b.add(v.eq, GIVEN)
        b.add(m, TARGET)
        b.add(v.nl, GIVEN)
    return b.finish(GIVEN)


def canvas_T4(v: Vocab, r: Rec, rng: np.random.Generator):
    b = _Builder(v)
    b.add(v.lexicon_head, GIVEN)
    rows = _rows(v, r, rng, BUCKETS[-1] - len(b.ids) - 1)
    if not rows:
        return None
    for w, m in rows:
        b.add(m, GIVEN)
        b.add(v.eq, GIVEN)
        b.add(w, TARGET)
        b.add(v.nl, GIVEN)
    return b.finish(GIVEN)


def canvas_T5(v: Vocab, r: Rec, rng: np.random.Generator):
    """Half the time one whole line is missing; otherwise ~25% of the words (at least one)."""
    free = [i for i in range(len(r.lines)) if not (r.samasya and i == len(r.lines) - 1)]
    if not free:
        return None
    span = [np.zeros(len(ln), dtype=np.int8) for ln in r.lines]
    if rng.random() < 0.5:
        span[int(rng.choice(free))][:] = TARGET
    else:
        words = []                                            # (line, start, end) of every word
        for i in free:
            ln, s = r.lines[i], 0
            sp = set(int(x) for x in np.flatnonzero(ln == v.space[0])) if len(v.space) == 1 else set()
            for j in range(len(ln) + 1):
                if j == len(ln) or j in sp:
                    if j > s:
                        words.append((i, s, j))
                    s = j + 1
        k = max(1, int(round(0.25 * len(words))))
        for w in rng.choice(len(words), size=min(k, len(words)), replace=False):
            i, s, e = words[int(w)]
            span[i][s:e] = TARGET
    b = _Builder(v)
    b.add(r.metre_head, GIVEN)
    b.add(r.style_head, GIVEN)
    b.add(r.samasya_head, GIVEN)
    b.add(r.meaning_line, GIVEN)
    b.add(v.poem_head, GIVEN)
    _poem(b, r, GIVEN, span_roles=span)
    return b.finish(GIVEN)


def build(task: str, v: Vocab, r: Rec, rng: np.random.Generator):
    if task == "T1":
        return canvas_T1(v, r)
    if task == "T0":
        return canvas_T1(v, r, empty_meaning=True)
    if task == "T2":
        return canvas_T2(v, r)
    if task == "T3":
        return canvas_T3(v, r, rng)
    if task == "T4":
        return canvas_T4(v, r, rng)
    if task == "T5":
        return canvas_T5(v, r, rng)
    raise ValueError(task)


# -----------------------------------------------------------------------------
# sampling pools
# -----------------------------------------------------------------------------
class Pools:
    """Which records each task may draw, with the metre-task weights of PLAN §3.4."""

    def __init__(self, recs: list[Rec], dvipada_share: float = DVIPADA_SHARE):
        self.recs = recs
        metre = [i for i, r in enumerate(recs) if r.metre_ok]
        with_meaning = [i for i in metre if recs[i].meaning_line is not None]
        self.index = {
            "T1": np.asarray(with_meaning, dtype=np.int64),
            "T5": np.asarray([i for i in with_meaning if len(recs[i].lines) >= 1], dtype=np.int64),
            "T0": np.asarray(metre, dtype=np.int64),
            "T2": np.asarray([i for i, r in enumerate(recs) if r.meaning_line is not None], dtype=np.int64),
            "T3": np.asarray([i for i, r in enumerate(recs) if r.glosses], dtype=np.int64),
        }
        self.index["T4"] = self.index["T3"]
        self.cdf = {}                                       # None = uniform
        for task, idx in self.index.items():
            if task in ("T1", "T5", "T0") and len(idx):
                self.cdf[task] = np.cumsum(self._metre_weights(idx, dvipada_share))
            else:
                self.cdf[task] = None

    def _metre_weights(self, idx: np.ndarray, dvipada_share: float) -> np.ndarray:
        meters = [self.recs[i].meter for i in idx]
        counts: dict = {}
        for m in meters:
            counts[m] = counts.get(m, 0) + 1
        w = np.asarray([min(MAX_UPSAMPLE, RARE_METRE / counts[m]) if counts[m] < RARE_METRE else 1.0 for m in meters])
        dv = np.asarray([m == "dvipada" for m in meters])
        d, o = w[dv].sum(), w[~dv].sum()
        if d > 0 and o > 0 and d / (d + o) > dvipada_share:
            w[dv] *= dvipada_share / (1 - dvipada_share) * o / d
        return w / w.sum()

    def draw(self, task: str, rng: np.random.Generator) -> Rec:
        idx, cdf = self.index[task], self.cdf[task]
        k = int(rng.integers(0, len(idx))) if cdf is None else min(int(np.searchsorted(cdf, rng.random() * cdf[-1])), len(idx) - 1)
        return self.recs[int(idx[k])]

    def sizes(self) -> dict:
        return {k: int(len(v)) for k, v in self.index.items()}
