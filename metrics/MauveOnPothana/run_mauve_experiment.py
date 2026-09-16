"""MAUVE sanity-gate experiment on Pothana's Andhra Mahabhagavatamu.

Tests the gate declared in the Chandohasam proposal (Section 5.2): before MAUVE
can be trusted on 15th-century Telugu metrical verse (far out of distribution
for modern multilingual embedders), it must pass:

  (A) held-out Pothana vs. Pothana  -> score near 1   (main claim tested here)
  (B) Pothana vs. degraded/gibberish controls -> score clearly lower / near 0

Embedder: google/embeddinggemma-300m (sentence-transformers).
MAUVE: mauve-text (Pillutla et al., 2021), with p_features/q_features supplied
directly from the embedder, so no GPT-2 featurization is involved.

Conditions
----------
1. split_stratified   : 50/50 meter-stratified split, seeds 0..4. Expect ~1.
2. split_random       : plain random 50/50 split, seeds 0..4. Expect ~1.
3. meter_mismatch     : vritta poems (ఉ,చ,మ,శా) vs jati/upajati (క,ఆ,తే).
                        Diagnostic: how much within-corpus prosodic shift moves
                        MAUVE. (Not a pass/fail condition.)
4. word_shuffle       : held-out half vs the same poems with words shuffled
                        within each poem (line lengths preserved). Expect a
                        clear drop below the split scores.
4b. line_shuffle      : held-out half vs the same poems with whole verse
                        lines reordered within each poem (every line intact,
                        stanza-level order destroyed; the permutation is
                        forced to differ from the identity). Mildest
                        degradation — probes stanza-level sensitivity.
5. char_gibberish     : held-out half vs random akshara soup drawn from the
                        corpus grapheme distribution, matched in length and
                        line structure. Proxy for "metrically valid nonsense"
                        (no trie constraint here — noted honestly). Expect ~0.

All comparisons use equal sample sizes on both sides and mauve defaults
(PCA + k-means, num_buckets='auto'). Embeddings are cached to .npy.
"""

import argparse
import json
import random
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
POEMS = HERE / "pothana_poems.json"
CACHE = HERE / "embeddings_cache"
RESULTS = HERE / "results.json"

MODEL_NAME = "google/embeddinggemma-300m"
VRITTA = {"ఉ.", "చ.", "మ.", "శా."}
JATI = {"క.", "ఆ.", "తే."}
SEEDS = [0, 1, 2, 3, 4]


# ---------------------------------------------------------------- text utils
def grapheme_clusters(text):
    """Approximate Telugu akshara segmentation via extended grapheme clusters."""
    import regex

    return regex.findall(r"\X", text)


def word_shuffle(poem_text, rng):
    """Shuffle words within a poem, preserving the per-line word counts."""
    lines = poem_text.split("\n")
    counts = [len(l.split()) for l in lines]
    words = poem_text.split()
    rng.shuffle(words)
    out, i = [], 0
    for c in counts:
        out.append(" ".join(words[i : i + c]))
        i += c
    return "\n".join(out)


def line_shuffle(poem_text, rng):
    """Reorder whole lines within a poem; guaranteed non-identity permutation."""
    lines = poem_text.split("\n")
    order = list(range(len(lines)))
    while True:
        rng.shuffle(order)
        if order != sorted(order):
            break
    return "\n".join(lines[i] for i in order)


def akshara_shuffle(poem_text, rng):
    """Shuffle the poem's own aksharas (grapheme clusters) across the poem.

    Preserves the exact akshara multiset, line lengths, and space positions;
    destroys word identity and order. Sits between word_shuffle (words kept)
    and char_gibberish (aksharas drawn from the corpus, not the poem).
    """
    lines = [grapheme_clusters(l) for l in poem_text.split("\n")]
    pool = [g for line in lines for g in line if g != " "]
    rng.shuffle(pool)
    it = iter(pool)
    return "\n".join(
        "".join(" " if g == " " else next(it) for g in line) for line in lines
    )


def char_gibberish(poem_text, inventory, rng):
    """Random akshara soup matching the poem's line structure and lengths."""
    out_lines = []
    for line in poem_text.split("\n"):
        n = len(grapheme_clusters(line.replace(" ", "")))
        soup = [rng.choice(inventory) for _ in range(n)]
        # re-insert spaces at roughly the same positions
        n_spaces = line.count(" ")
        for _ in range(n_spaces):
            pos = rng.randint(1, max(1, len(soup) - 1))
            soup.insert(pos, " ")
        out_lines.append("".join(soup))
    return "\n".join(out_lines)


# ---------------------------------------------------------------- embeddings
def get_model():
    from sentence_transformers import SentenceTransformer
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SentenceTransformer(MODEL_NAME, device=device)
    print(f"Loaded {MODEL_NAME} on {device}; prompts: {list(model.prompts)}")
    return model


def embed(model, texts, cache_name, prompt_name):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{cache_name}.npy"
    if path.exists():
        emb = np.load(path)
        if len(emb) == len(texts):
            return emb
    kwargs = dict(batch_size=16, show_progress_bar=True, normalize_embeddings=True)
    if prompt_name and prompt_name in model.prompts:
        kwargs["prompt_name"] = prompt_name
    emb = model.encode(texts, **kwargs)
    np.save(path, emb)
    return emb


# ---------------------------------------------------------------- mauve
def mauve_score(p_feat, q_feat, seed):
    import mauve

    n = min(len(p_feat), len(q_feat))
    rng = np.random.default_rng(seed)
    p = p_feat[rng.choice(len(p_feat), n, replace=False)]
    q = q_feat[rng.choice(len(q_feat), n, replace=False)]
    out = mauve.compute_mauve(
        p_features=p, q_features=q, seed=seed, verbose=False
    )
    return out.mauve, n


def stratified_split(poems, seed):
    """Meter-stratified 50/50 split; returns (idx_a, idx_b)."""
    rng = random.Random(seed)
    by_meter = {}
    for i, p in enumerate(poems):
        by_meter.setdefault(p["meter"], []).append(i)
    a, b = [], []
    for idxs in by_meter.values():
        idxs = idxs[:]
        rng.shuffle(idxs)
        half = len(idxs) // 2
        a.extend(idxs[:half])
        b.extend(idxs[half:])
    return sorted(a), sorted(b)


def random_split(n, seed):
    rng = random.Random(seed)
    idxs = list(range(n))
    rng.shuffle(idxs)
    half = n // 2
    return sorted(idxs[:half]), sorted(idxs[half:])


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt-name", default="Clustering",
                    help="embeddinggemma prompt to use for all texts")
    args = ap.parse_args()

    poems = json.loads(POEMS.read_text(encoding="utf-8"))
    texts = [p["text"] for p in poems]
    print(f"{len(poems)} poems loaded")

    # Build degraded corpora (deterministic, seed 0)
    rng = random.Random(0)
    shuffled_texts = [word_shuffle(t, rng) for t in texts]
    line_shuffled_texts = [line_shuffle(t, rng) for t in texts]
    akshara_shuffled_texts = [akshara_shuffle(t, rng) for t in texts]
    inventory = sorted({g for t in texts for g in grapheme_clusters(t)
                        if g.strip() and g != "\n"})
    print(f"akshara inventory: {len(inventory)} grapheme types")
    gibberish_texts = [char_gibberish(t, inventory, rng) for t in texts]

    (HERE / "sample_degradations.json").write_text(json.dumps(
        {"original": texts[0], "word_shuffle": shuffled_texts[0],
         "line_shuffle": line_shuffled_texts[0],
         "akshara_shuffle": akshara_shuffled_texts[0],
         "char_gibberish": gibberish_texts[0]}, ensure_ascii=False, indent=1),
        encoding="utf-8")

    model = get_model()
    pn = args.prompt_name
    emb = embed(model, texts, f"pothana_{pn}", pn)
    emb_shuf = embed(model, shuffled_texts, f"shuffled_{pn}", pn)
    emb_lshuf = embed(model, line_shuffled_texts, f"line_shuffled_{pn}", pn)
    emb_akshuf = embed(model, akshara_shuffled_texts, f"akshara_shuffled_{pn}", pn)
    emb_gib = embed(model, gibberish_texts, f"gibberish_{pn}", pn)
    print("embedding dims:", emb.shape)

    results = {"model": MODEL_NAME, "prompt_name": pn,
               "n_poems": len(poems), "conditions": {}}

    def record(name, scores_ns, expect):
        scores = [s for s, _ in scores_ns]
        ns = [n for _, n in scores_ns]
        results["conditions"][name] = {
            "mauve_mean": float(np.mean(scores)),
            "mauve_std": float(np.std(scores)),
            "scores": [float(s) for s in scores],
            "n_per_side": ns[0],
            "expectation": expect,
        }
        print(f"{name:20s} MAUVE = {np.mean(scores):.4f} ± {np.std(scores):.4f} "
              f"(n/side={ns[0]})  [{expect}]")

    # 1 & 2: held-out Pothana vs Pothana
    for name, splitter in [
        ("split_stratified", lambda s: stratified_split(poems, s)),
        ("split_random", lambda s: random_split(len(poems), s)),
    ]:
        sc = []
        for s in SEEDS:
            a, b = splitter(s)
            sc.append(mauve_score(emb[a], emb[b], seed=s))
        record(name, sc, "near 1")

    # 3: meter mismatch (vritta vs jati/upajati)
    vr = [i for i, p in enumerate(poems) if p["meter"] in VRITTA]
    ja = [i for i, p in enumerate(poems) if p["meter"] in JATI]
    sc = [mauve_score(emb[vr], emb[ja], seed=s) for s in SEEDS]
    record("meter_mismatch", sc, "diagnostic (within-corpus shift)")

    # 4, 4b & 5: held-out half vs degraded versions of the *other* half's poems
    sc4, sc4b, sc4c, sc5 = [], [], [], []
    for s in SEEDS:
        a, b = stratified_split(poems, s)
        sc4.append(mauve_score(emb[a], emb_shuf[b], seed=s))
        sc4b.append(mauve_score(emb[a], emb_lshuf[b], seed=s))
        sc4c.append(mauve_score(emb[a], emb_akshuf[b], seed=s))
        sc5.append(mauve_score(emb[a], emb_gib[b], seed=s))
    record("word_shuffle", sc4, "clearly below split scores")
    record("line_shuffle", sc4b, "mildest degradation; between split and word_shuffle?")
    record("akshara_shuffle", sc4c, "between word_shuffle and gibberish?")
    record("char_gibberish", sc5, "near 0")

    RESULTS.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote {RESULTS}")

    gate = results["conditions"]["split_stratified"]["mauve_mean"]
    gib = results["conditions"]["char_gibberish"]["mauve_mean"]
    print("\n=== SANITY GATE VERDICT ===")
    print(f"held-out Pothana vs Pothana : {gate:.4f} (need ~1)")
    print(f"Pothana vs gibberish        : {gib:.4f} (need ~0)")
    ok = gate > 0.9 and gib < 0.1 and gate - gib > 0.8
    print("GATE:", "PASS — MAUVE separates the conditions" if ok
          else "FAIL — MAUVE does not separate; embedder unsuitable as-is")


if __name__ == "__main__":
    main()
