#!/usr/bin/env python3
"""
How "unattested" are the generated words? A minimal-absent-factor measurement against real verse.

A suffix automaton (Blumer's DAWG; arXiv 2307.01428 builds the same structure) is built over the
aksharas of the words of 90% of the real poems in ``dataset/*.json`` (verse fields only). For any
word, a scan through the automaton gives its *minimal absent factor* (MAF): the shortest run of
consecutive aksharas inside the word that occurs inside no real word. Its length separates junk
from novelty:

* MAF 1–2: an akshara, or a pair of aksharas, never seen in any real word (``junk``);
* MAF 3 / ≥ 4: a new combination of attested pieces;
* no MAF: the word occurs inside some real word (``attested``); ``corpus word`` when it is one.

The held-out 10% of real poems shows what unseen real verse scores; every generated poem of the
inference runs is scored the same way, by model and ablation. For the constrained poems each word
is also marked by whether the constraint overrode the model on any of its tokens (the model's own
first choice was not allowed), from the trace.

usage: measure_absent_words.py OUT_DIR
"""
from __future__ import annotations

import json
import random
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "meter_engine"))
sys.path.insert(0, str(ROOT / "experiments" / "scripts"))

from metrical_decoder.analysis import _telugu_words          # noqa: E402
from metrical_decoder.registers import _syllables             # noqa: E402
from export_inference_json import _trace                      # noqa: E402

RUNS = ROOT / "experiments" / "runs"
MODELS = {
    "Gemma-4 E4B": ["2026-09-24_e4b_baseline", "2026-09-24_e4b_constrained"],
    "Gemma-4 26B-A4B": ["2026-09-26_g26b"],
    "DiffusionGemma 26B-A4B": ["2026-09-26_diffusion_baseline", "2026-09-25_diffusion_constrained"],
}
ABLATIONS = ("baseline", "masking_only", "masking_backtrack", "hybrid")
CLASSES = ("corpus word", "attested", "MAF ≥ 4", "MAF 3", "junk (MAF ≤ 2)")


# ----------------------------------------------------------------------------- suffix automaton
class SuffixAutomaton:
    """Blumer et al.'s DAWG over integer symbols, built online; words are separated by -1 so that
    no factor crosses a word boundary."""

    def __init__(self):
        self.next: list[dict[int, int]] = [{}]
        self.link: list[int] = [-1]
        self.len: list[int] = [0]
        self.last = 0

    def add(self, c: int) -> None:
        nxt, link, ln = self.next, self.link, self.len
        cur = len(ln)
        nxt.append({}); link.append(0); ln.append(ln[self.last] + 1)
        p = self.last
        while p != -1 and c not in nxt[p]:
            nxt[p][c] = cur
            p = link[p]
        if p != -1:
            q = nxt[p][c]
            if ln[p] + 1 == ln[q]:
                link[cur] = q
            else:
                clone = len(ln)
                nxt.append(dict(nxt[q])); link.append(link[q]); ln.append(ln[p] + 1)
                while p != -1 and nxt[p].get(c) == q:
                    nxt[p][c] = clone
                    p = link[p]
                link[q] = link[cur] = clone
        self.last = cur

    def maf(self, word: list[int]) -> int | None:
        """Length of the shortest factor of ``word`` that is not a factor of the text (None: all are)."""
        v, l, best = 0, 0, None
        for i, c in enumerate(word):
            while v and c not in self.next[v]:
                v = self.link[v]
                l = self.len[v]
            if c in self.next[v]:
                v, l = self.next[v][c], l + 1
            else:
                v, l = 0, 0
            if l < i + 1:                         # the factor of length l + 1 ending here is absent
                best = l + 1 if best is None else min(best, l + 1)
        return best


# ----------------------------------------------------------------------------- corpus
def aksharas(word: str) -> list[str]:
    return [s.text for s in _syllables(word)]


def real_poems() -> list[list[str]]:
    poems = []
    for path in sorted((ROOT / "dataset").glob("*.json")):
        for rec in json.loads(path.read_text(encoding="utf-8")):
            verse = [unicodedata.normalize("NFC", ln) for ln in rec.get("verse") or [] if ln.strip()]
            if verse:
                poems.append(verse)
    return poems


class Scorer:
    def __init__(self, train: list[list[str]]):
        self.ids: dict[str, int] = {}
        self.sa = SuffixAutomaton()
        self.lexicon: set[str] = set()
        n = 0
        for poem in train:
            for ln in poem:
                for w in _telugu_words(ln):
                    self.lexicon.add(w)
                    for a in aksharas(w):
                        self.sa.add(self.ids.setdefault(a, len(self.ids)))
                        n += 1
                    self.sa.add(-1)
        self.n_aksharas = n

    def classify(self, word: str) -> str:
        if word in self.lexicon:
            return "corpus word"
        m = self.sa.maf([self.ids.get(a, -2) for a in aksharas(word)])
        if m is None:
            return "attested"
        return "MAF ≥ 4" if m >= 4 else "MAF 3" if m == 3 else "junk (MAF ≤ 2)"


# ----------------------------------------------------------------------------- generated poems
def words_with_override(text: str, tokens: list[dict]) -> list[tuple[str, bool | None]]:
    """The poem's words, each with whether the constraint overrode the model on one of its tokens."""
    pieces = "".join(t["text"] for t in tokens)
    if pieces != text:                            # free text whose decoding differs from the token texts
        return [(w, None) for w in _telugu_words(text)]
    flags, pos = [False] * len(text), 0
    for t in tokens:
        if t.get("overridden"):
            for k in range(pos, pos + len(t["text"])):
                flags[k] = True
        pos += len(t["text"])
    out, start = [], None
    for k, ch in enumerate(text + " "):
        if ch.isspace():
            if start is not None:
                for w in _telugu_words(text[start:k]):
                    out.append((w, any(flags[start:k])))
                start = None
        elif start is None:
            start = k
    return out


def main() -> None:
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    poems = real_poems()
    rng = random.Random(0)
    order = list(range(len(poems)))
    rng.shuffle(order)
    cut = len(poems) // 10
    held = [poems[i] for i in order[:cut]]
    train = [poems[i] for i in order[cut:]]
    train_lines = {ln for p in train for ln in p}
    held = [[ln for ln in p if ln not in train_lines] for p in held]        # no verbatim leakage
    held = [p for p in held if p]
    print(f"real poems: {len(poems)} (train {len(train)}, held out {len(held)})", flush=True)
    scorer = Scorer(train)
    print(f"suffix automaton: {scorer.n_aksharas} aksharas, {len(scorer.ids)} distinct, "
          f"{len(scorer.sa.len)} states", flush=True)

    counts: dict[tuple, Counter] = defaultdict(Counter)       # (model, ablation, split) -> class counts
    poems_junk: dict[tuple, list[int]] = defaultdict(list)
    for p in held:
        ws = [w for ln in p for w in _telugu_words(ln)]
        cls = [scorer.classify(w) for w in ws]
        counts[("real verse (held out)", "—", "all")].update(cls)
        poems_junk[("real verse (held out)", "—")].append(sum(c == "junk (MAF ≤ 2)" for c in cls))

    for model, runs in MODELS.items():
        for run in runs:
            rows = {}
            for ln in open(RUNS / run / "results.jsonl", encoding="utf-8"):
                r = json.loads(ln)
                rows[r["key"]] = r
            for ln in open(RUNS / run / "traces.jsonl", encoding="utf-8"):
                t = json.loads(ln)
                r = rows[t["key"]]
                _, tokens = _trace(t["trace"], r["ids"])
                junk = 0
                for w, over in words_with_override(r["text"], tokens):
                    c = scorer.classify(w)
                    junk += c == "junk (MAF ≤ 2)"
                    counts[(model, r["mode"], "all")][c] += 1
                    if r["mode"] != "baseline" and over is not None:
                        counts[(model, r["mode"], "overridden" if over else "model's own")][c] += 1
                poems_junk[(model, r["mode"])].append(junk)
            print(f"scored {run}", flush=True)

    def shares(c: Counter) -> dict:
        n = sum(c.values())
        return {"words": n, **{k: c[k] / n if n else None for k in CLASSES}}

    data = {f"{m}|{a}|{s}": shares(c) for (m, a, s), c in counts.items()}
    data.update({f"{m}|{a}|poems_with_junk": sum(1 for x in v if x) / len(v) for (m, a), v in poems_junk.items()})
    (out_dir / "absent_words.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

    lines = ["| set | ablation | words | corpus word | attested | MAF ≥ 4 | MAF 3 | junk (MAF ≤ 2) | poems with junk |",
             "|---|---|---|---|---|---|---|---|---|"]
    keys = [("real verse (held out)", "—")] + [(m, a) for m in MODELS for a in ABLATIONS]
    for m, a in keys:
        s = data.get(f"{m}|{a}|all")
        if not s:
            continue
        lines.append(f"| {m} | {a} | {s['words']} | " + " | ".join(f"{100 * s[k]:.1f}%" for k in CLASSES)
                     + f" | {100 * data[f'{m}|{a}|poems_with_junk']:.0f}% |")
    lines += ["", "Constrained poems, words split by whether the constraint overrode the model on one of their tokens:", "",
              "| model | ablation | words | split | corpus word | attested | MAF ≥ 4 | MAF 3 | junk (MAF ≤ 2) |",
              "|---|---|---|---|---|---|---|---|---|"]
    for m in MODELS:
        for a in ABLATIONS[1:]:
            for split in ("model's own", "overridden"):
                s = data.get(f"{m}|{a}|{split}")
                if s:
                    lines.append(f"| {m} | {a} | {s['words']} | {split} | " + " | ".join(f"{100 * s[k]:.1f}%" for k in CLASSES) + " |")
    md = "\n".join(lines) + "\n"
    (out_dir / "absent_words.md").write_text(md, encoding="utf-8")
    print(md)


if __name__ == "__main__":
    main()
