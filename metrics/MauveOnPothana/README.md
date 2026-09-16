# MauveOnPothana — MAUVE sanity gate on the Andhra Mahabhagavatamu

Validates the gate declared in the Chandohasam proposal (Section 5.2): before
MAUVE can be trusted on 15th-century Telugu metrical verse (far out of
distribution for modern multilingual embedders), it must separate:

- **(A)** held-out Pothana vs. Pothana → score **near 1**
- **(B)** Pothana vs. degraded / gibberish text → score **near 0**

**Verdict (2026-08-18): GATE PASSES** with `google/embeddinggemma-300m`.

| Condition | MAUVE (mean ± std, 5 seeds) | n/side | Expectation |
|---|---|---|---|
| Held-out Pothana vs Pothana (meter-stratified 50/50) | **0.957 ± 0.003** | 1601 | near 1 ✓ |
| Held-out Pothana vs Pothana (plain random 50/50) | 0.953 ± 0.004 | 1607 | near 1 ✓ |
| Vritta (ఉ,చ,మ,శా) vs jati/upajati (క,ఆ,తే) | 0.214 ± 0.029 | 721 | diagnostic |
| Pothana vs line-shuffled Pothana (lines intact, order scrambled) | 0.906 ± 0.007 | 1601 | mild drop ✓ |
| Pothana vs word-shuffled Pothana | 0.716 ± 0.034 | 1601 | below split ✓ |
| Pothana vs akshara-shuffled Pothana (own aksharas, no words) | 0.028 ± 0.002 | 1601 | near floor ✓ |
| Pothana vs random-akshara gibberish | **0.005 ± 0.000** | 1601 | near 0 ✓ |

### Readings

1. **The gate passes**: identical-distribution halves score 0.96, gibberish
   scores 0.005 — a 200× separation. EmbeddingGemma is usable for the
   Telugu-verse MAUVE protocol.
2. **Meter-matching matters a lot**: comparing vritta poems against
   jati/upajati poems collapses MAUVE to 0.21 even though both sides are
   canonical Pothana. Generated batches must be compared against
   **meter-matched** canonical verse, exactly as the proposal specifies —
   otherwise distribution drift caused by meter mix is confounded with quality.
3. **Degradation is monotone but compressed at the top**: line-shuffle
   (every line intact, stanza order destroyed, non-identity permutation
   forced) drops MAUVE only to 0.91, and word-shuffle to 0.72 — the ordering
   split > line > word > akshara > gibberish is correct, but the margins at
   the coherent end are thin. The embedder is partially bag-of-words on
   out-of-distribution verse, so MAUVE alone is not a sufficient coherence
   signal at the stanza-order or word-order level — consistent with the
   proposal's decision to pair MAUVE with the Kavyalankara Sangrahamu metric
   suite and human ratings.
   **Word identity is the load-bearing feature**: akshara-shuffle, which
   keeps each poem's exact akshara multiset but destroys word identity,
   collapses MAUVE to 0.028 — a 0.69 fall from word-shuffle, landing just
   above the corpus-inventory gibberish floor (0.005). The embedder is
   bag-of-*words*, not bag-of-aksharas: real lexical items matter enormously,
   their order much less.
4. Caveat: the gibberish control here is unconstrained akshara soup, a proxy
   for the proposal's *metrically valid* nonsense (no trie was used). Rerun
   condition 5 with trie-valid gibberish once the generator is wired in.

## Cross-corpus: Pothana vs Vemana

`extract_vemana.py` converts `vemana_poems.txt` (blank-line-separated padyas;
1258 blocks, 94 exact duplicates removed) into `vemana_poems.json`: **1164
poems** (1160 Ataveladi + 4 Seesamu-style). `compare_vemana_pothana.py` runs
all main comparisons at matched n/side = 582 (results in
`results_vemana.json`):

| Condition | MAUVE (mean ± std, 5 seeds) | n/side |
|---|---|---|
| Vemana vs Vemana (50/50 split) | 0.957 ± 0.015 | 582 |
| Pothana vs Pothana (stratified split, matched n) | 0.952 ± 0.018 | 582 |
| Pothana (mixed meters) vs Vemana | **0.031 ± 0.004** | 582 |
| Pothana Ataveladi-only vs Vemana (meter-controlled) | **0.051 ± 0.007** | 313 |
| Vemana vs Vemana (reference at small n) | 0.957 ± 0.005 | 313 |

Readings: (i) both corpora pass the self-split gate at ~0.96, so the gate
result generalizes beyond Pothana; (ii) MAUVE separates the two canonical
authors almost completely (0.03) — register, era, and diction dominate;
(iii) controlling meter (Ataveladi vs Ataveladi) recovers almost none of it
(0.05 vs a 0.96 same-n reference), so the Pothana–Vemana gap is stylistic,
not a meter-mix artifact. Consequence for the protocol: MAUVE reference
pools must be matched on **author/register**, not just meter — scoring a
generator against the "wrong" canonical corpus would swamp any quality
signal.

## Corpus

`extract_poems.py` parses `../bhagavatam.txt` (blocks: `book-verse-meter.`
header → verse lines → `టీకా:` gloss → `భావము:` commentary) and keeps **only
padyas** (metrical poems):

- Excluded prose forms: వ. vachanam (1537), గ. gadyam (9), దం. (1), శ్లో. (1)
- Removed web boilerplate lines ("ఈ/మీ బ్రౌజరు అను/అనూకూలం కాదు.")
- Dropped 1030 blocks truncated in the source dump (< 4 verse lines; < 8 for
  సీ., which renders as half-lines). Only the verse text is kept — no gloss or
  commentary leakage (verified).

Result: **3214 complete padyas** in `pothana_poems.json`
(fields: id, book, verse, meter, meter_name, n_lines, text);
counts per meter in `extraction_stats.json`. Top meters: క. 1017, తే. 661,
సీ. 464, ఆ. 313, మ. 224, చ. 215, ఉ. 182, శా. 100.

## Method

`run_mauve_experiment.py`:

- Embeds each poem with `google/embeddinggemma-300m`
  (sentence-transformers, `Clustering` prompt, normalized, 768-d, GPU);
  embeddings cached in `embeddings_cache/`.
- Computes MAUVE (`mauve-text`, Pillutla et al. 2021) from
  `p_features`/`q_features` directly (no GPT-2 featurization), defaults:
  PCA + k-means quantization, `num_buckets='auto'`. Equal sample sizes on
  both sides of every comparison; 5 seeds (0–4) for splits and subsampling.
- Degradations (deterministic, samples in `sample_degradations.json`):
  word-shuffle permutes words within each poem preserving per-line word
  counts; gibberish draws uniformly from the corpus's 2337 grapheme-cluster
  inventory, matching each poem's line structure and akshara counts.
- Note: faiss warns that ~1600 points is few for 160 k-means centroids —
  standard for MAUVE at this n; scores are stable across seeds (std ≤ 0.03).

## Reproduce

```bash
python3 extract_poems.py                      # rebuild pothana_poems.json
uv venv .venv && uv pip install --python .venv/bin/python \
  torch --index-url https://download.pytorch.org/whl/cu128
uv pip install --python .venv/bin/python \
  sentence-transformers mauve-text faiss-cpu scikit-learn regex
.venv/bin/python run_mauve_experiment.py      # writes results.json
```

Requires HF access to the gated `google/embeddinggemma-300m` (token on disk).
Full numbers: `results.json`.
