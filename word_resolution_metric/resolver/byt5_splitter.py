"""ByT5 in the splitter slot: the same `.split(words, ...)` interface as model.Splitter, so every stage
that takes a splitter (resolve_corpus, resolve_final, resolve_join, postprocess.lexicon_rerank,
annotate/evaluate_gold) can run with the distilled ByT5 instead of the BiLSTM.

The model generates the analysis in the project's notation (parts with →headword); the splitter
view keeps the surface parts only and validates them: every part must start like a word and the
parts must re-assemble to the input up to the sandhi rewrites the editions use (otherwise the word
is returned unsplit). Generations are cached on disk (results/resolution/byt5_splits_cache.json),
since one pass over the corpus takes about an hour and the stages ask for the same words at several
thresholds. `headwords(words)` returns the full analyses for the resolver slot.
"""
import json
import re
import sys
from pathlib import Path

import torch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from sandhi_data import COPY, SEP, WORD_START, clean_word, encode  # noqa: E402

TEL = re.compile(r"[ఀ-౿]+")


def _edit(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


class ByT5Splitter:
    def __init__(self, checkpoint=None, device=None, cache=None, batch_size=192, max_new=None):
        from transformers import AutoTokenizer, T5ForConditionalGeneration
        checkpoint = Path(checkpoint or HERE.parent / "byt5" / "checkpoints" / "distill")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(checkpoint)
        self.model = T5ForConditionalGeneration.from_pretrained(checkpoint)
        if self.device == "cuda":
            self.model = self.model.to(torch.bfloat16)
        self.model = self.model.to(self.device).eval()
        self.batch_size, self.max_new = batch_size, max_new
        self.cache_path = Path(cache) if cache else HERE / "results" / "resolution" / "byt5_splits_cache.json"
        self.cache = json.load(open(self.cache_path, encoding="utf-8")) if self.cache_path.exists() else {}
        # an entry that filled its output budget (the old fixed 96 bytes, or a runaway repetition that reached the
        # per-word budget) is generated again; every other entry is kept whatever its length
        stale = [w for w, a in self.cache.items() if len(a.encode()) >= 94 and len(a.encode()) >= (max_new or self.budget(w)) - 2]
        for w in stale:
            del self.cache[w]
        if stale:
            print(f"byt5 cache: {len(self.cache):,} analyses loaded, {len(stale):,} at the budget discarded", flush=True)
        self._dirty = 0
        # what the pipeline reads off a splitter
        self.config = {"postprocess": [], "threshold": None, "data": "data_dict", "lexicon_splits": ["train", "dev", "test"], "arch": "byt5"}
        self.context = False
        self.labels = [COPY]

    def budget(self, word):
        """Output bytes allowed for a word: the analysis repeats the word (as parts) and adds →headword
        rewrites and separators, so 2.5x the word's bytes plus a margin (ByT5 is byte level: 3 bytes per
        Telugu character); 96 bytes, the old fixed budget, cut every word beyond about 18 aksharas."""
        return self.max_new or min(1024, int(2.5 * len(word.encode())) + 24)

    @torch.no_grad()
    def generate(self, words):
        todo = [w for w in dict.fromkeys(words) if w not in self.cache]
        order = sorted(todo, key=len)
        b = 0
        while b < len(order):
            n = self.batch_size if len(order[b]) <= 12 else max(32, self.batch_size // 2) if len(order[b]) <= 20 else max(16, self.batch_size // 4)
            chunk = order[b:b + n]
            b += n
            enc = self.tok(chunk, return_tensors="pt", padding=True).to(self.device)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=self.device == "cuda"):
                gen = self.model.generate(**enc, max_new_tokens=self.budget(chunk[-1]), num_beams=1, do_sample=False)
            for w, g in zip(chunk, self.tok.batch_decode(gen, skip_special_tokens=True)):
                self.cache[w] = g.strip()
            self._dirty += len(chunk)
            if self._dirty >= 20000:
                self.save()
        return [self.cache.get(w, w) for w in words]

    def save(self):
        if self._dirty:
            json.dump(self.cache, open(self.cache_path, "w", encoding="utf-8"), ensure_ascii=False)
            self._dirty = 0

    @staticmethod
    def surface_split(word, analysis):
        """The split view of an analysis: parts without →headword, validated against the word."""
        parts = [clean_word(p.split("→")[0]) for p in analysis.split(SEP)]
        parts = [p for p in parts if p]
        if not parts or not all(WORD_START.match(p) for p in parts):
            return word
        joined = "".join(parts)
        if len(parts) == 1:
            return word
        if _edit(joined, word) > 2 * (len(parts) - 1) + 1:  # not a rewrite of this word
            return word
        return SEP.join(parts)

    def split(self, words, batch_size=None, threshold="config", rules="config", contexts=None):
        """(splits, labels) like model.Splitter.split; thresholds and rules have no effect."""
        analyses = self.generate(words)
        splits = [self.surface_split(w, a) for w, a in zip(words, analyses)]
        labels = []
        for w, s in zip(words, splits):
            try:
                labels.append(encode(w, s) if SEP in s else [COPY] * len(w))
            except Exception:
                labels.append([COPY] * len(w))
        return splits, labels

    def headwords(self, words):
        """The full analyses (parts with →headword) for the resolver slot."""
        return self.generate(words)

    @torch.no_grad()
    def headwords_nbest(self, words, n=4):
        """The n best analyses per word (beam search), cached beside the greedy cache (…_nbest{n}.json). On the
        gold pairs the dictionary gate accepts 0.726 of the greedy analyses at 0.760 precision and 0.879 of
        4-beam lists at 0.721, 0.634 right of all pairs against 0.552 (byt5/evaluate_nbest.py)."""
        path = self.cache_path.with_name(self.cache_path.stem + f"_nbest{n}.json")
        if not hasattr(self, "_nbest") or self._nbest_n != n:
            self._nbest = json.load(open(path, encoding="utf-8")) if path.exists() else {}
            self._nbest_n, self._nbest_path, self._nbest_dirty = n, path, 0
        todo = [w for w in dict.fromkeys(words) if w not in self._nbest]
        order = sorted(todo, key=len)
        b = 0
        while b < len(order):
            k = max(8, self.batch_size // 4) if len(order[b]) <= 12 else max(8, self.batch_size // 8) if len(order[b]) <= 20 else max(4, self.batch_size // 16)
            chunk = order[b:b + k]
            b += k
            enc = self.tok(chunk, return_tensors="pt", padding=True).to(self.device)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=self.device == "cuda"):
                gen = self.model.generate(**enc, max_new_tokens=self.budget(chunk[-1]), num_beams=n, num_return_sequences=n, do_sample=False)
            dec = self.tok.batch_decode(gen, skip_special_tokens=True)
            for i, w in enumerate(chunk):
                self._nbest[w] = [d.strip() for d in dec[i * n:(i + 1) * n]]
            self._nbest_dirty += len(chunk)
            if self._nbest_dirty >= 20000:
                self.save_nbest()
        return [self._nbest.get(w, []) for w in words]

    def save_nbest(self):
        if getattr(self, "_nbest_dirty", 0):
            json.dump(self._nbest, open(self._nbest_path, "w", encoding="utf-8"), ensure_ascii=False)
            self._nbest_dirty = 0

    def _probs(self, words):
        raise NotImplementedError("ByT5 has no per-character label probabilities")


if __name__ == "__main__":
    sp = ByT5Splitter(checkpoint=sys.argv[1] if len(sys.argv) > 1 else None, device="cpu")
    ws = ["రాముడతడు", "చదివాను", "కార్యముల్", "సోమవారములు", "భక్తితో"]
    print(list(zip(ws, sp.headwords(ws), sp.split(ws)[0])))
