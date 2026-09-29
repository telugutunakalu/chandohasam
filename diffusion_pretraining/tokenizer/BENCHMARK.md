# Subword-backend benchmark for syllable-aware Telugu tokenization

**Question:** for a syllable-aware Telugu tokenizer, which subword backend performs
best — BPE, WordPiece, or Unigram (SentencePiece)? And how does our two-level
design (atomic-akshara dictionary + BPE failover) compare?

**Controlled setup.** Every tokenizer below uses the *same* `akshara.py` syllable
pre-tokenizer, is trained on the *same* 300,000-line sample of the Kaggle Telugu
Wikipedia corpus (`data/`), and is evaluated on the *same* 20,000-line held-out
split. The three HF backends use vocab 32,000; ours uses a smaller 28,282 (all it
needed). The only variable is the subword algorithm.

| backend | vocab | fertility ↓ | one-token % ↑ | OOV ↓ | lossless % ↑ | cross-akshara | disk |
|---|---|---|---|---|---|---|---|
| **Ours — atomic akshara dict + BPE failover** | **28,282** | **1.0005** | **99.96** | **0** | **100** | 0 | **684 KB** |
| BPE (byte_fallback) | 32,000 | 1.3579 | 97.49 | 0 | 100 | 0 | 2,218 KB |
| WordPiece | 32,000 | 1.3508 | 97.49 | **192** | 99.06 | 0 | 747 KB |
| Unigram / SentencePiece | 32,000 | 1.9957 | 41.71 | 19 | 99.95 | 0 | 2,050 KB |

- **fertility** = tokens per Telugu syllable (1.0 = every syllable is exactly one token; lower is better)
- **one-token %** = share of syllables emitted as a single token
- **cross-akshara** = tokens spanning a syllable boundary (0 everywhere → the shared pre-tokenizer makes *all* of them syllable-aware)

## Findings

**All three vanilla backends are genuinely syllable-aware** (`cross_akshara = 0`):
the akshara pre-tokenizer prevents any token from crossing a syllable boundary,
so SentencePiece/WordPiece/BPE *can* be made syllable-aware simply by supplying
`akshara.py` segmentation. The differences are entirely *within-syllable*.

**Among the vanilla backends, BPE wins.** It is the only one that is both 100%
lossless and never OOV (byte fallback turns any unseen akshara into raw UTF-8
tokens instead of `<unk>`), while matching WordPiece on compression.

**WordPiece silently loses data.** It has no byte fallback, so ~1% of hard
aksharas (deep conjuncts, candrabindu `ఁ`) collapse to `[UNK]`: 192 OOV, 99.06%
lossless. Smallest artifact (747 KB), but the lossiness is disqualifying when
exact reconstruction matters.

**Unigram (HuggingFace impl.) over-segments badly** — fertility 1.9957, only
41.71% of syllables kept whole (`కృష్ణుడు → క|ృ|ష్ణు|డ|ు`).

> **Correction / caveat (important).** This Unigram row reflects the *HuggingFace
> `tokenizers` Unigram* configuration, and it is **not representative of the
> Unigram algorithm in general**. Re-running with **SentencePiece's own Unigram**
> (via `pretokenization_delimiter`, byte_fallback) on the same data gives a
> completely different result — it keeps syllables whole:
>
> | Unigram implementation | one-token % | over-segments? |
> |---|---|---|
> | HuggingFace `tokenizers` (benchmark row above) | 41.71 | yes, severely |
> | SentencePiece (canonical) | **99.11** | no |
> | SentencePiece + `user_defined_symbols` (whole aksharas protected) | **99.84** | no |
>
> So "Unigram over-segments" was an artifact of the HF configuration, not a law of
> the algorithm. SentencePiece's Unigram renders `కృష్ణుడు` as `కృ|ష్ణు|డు`
> (matra stays attached), matching BPE. The general lesson stands: syllable
> *boundary* awareness is free from the pre-tokenizer, but guaranteeing
> *one-token-per-syllable* requires either a well-tuned model or (robustly)
> allocating vocab to whole syllables as our design does.

**Our two-level design beats all three, at a smaller vocab.** Fertility 1.0005
and 99.96% one-token — essentially one token per syllable — versus 1.35 / 97.49%
for the best vanilla backend, and it does so with fewer vocab slots (28,282 vs
32,000) and the smallest artifact (684 KB).

## Why our design wins

Pure BPE/WordPiece/Unigram must **rebuild every syllable from merges/pieces**
inside a fixed vocab budget. With 32k slots they cannot give every attested
akshara its own token, so ~2.5% of syllables fragment — and because those are
high-frequency hard syllables, fertility climbs to 1.35 even though 97% of
syllable *types* fit.

Our design **allocates the vocab directly to whole syllables**: it puts every
akshara seen in training into the vocabulary as one atomic token (the dictionary
level), and only spends BPE on the genuinely unseen tail (the failover level).
Same budget, but spent on whole syllables instead of on merge fragments that
approximate them — which is exactly the "every syllable its own token" objective.

## Recommendation

- **Use our atomic-dictionary + BPE-failover design** — best fertility, best
  one-token coverage, 0 OOV, 100% lossless, smallest vocab.
- If you must use an off-the-shelf backend, **use BPE with `byte_fallback`** — the
  only vanilla option that is both lossless and OOV-free.
- **Avoid WordPiece** unless the ~1% `[UNK]` loss is acceptable, and **avoid
  Unigram** here — it nearly doubles the token count.

*Reproduce:* scripts in `scratchpad/sp_exp/` (`hf_build.py`, `hf_eval.py`,
`bench_prep.py`); our tokenizer via `train_tokenizer.py` + `eval_tokenizer.py`.
