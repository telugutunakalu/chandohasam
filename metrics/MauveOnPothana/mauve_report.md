# The MAUVE Gate

**Chandohasam · Experiment Report · MauveOnPothana**

Can a modern multilingual embedder support MAUVE on 15th-century Telugu metrical verse? We tested the sanity gate declared in proposal §5.2 on Pothana's *Andhra Mahabhagavatamu* — and then pushed past it with degradation ladders and a second poet.

| | |
|---|---|
| **Verdict** | **GATE: PASS** |
| Embedder | `google/embeddinggemma-300m` (768-d, Clustering prompt, normalized) |
| Corpora | 3,214 Pothana padyas · 1,164 Vemana padyas |
| Date | 2026-08-18 |
| Team | Mahesh Emani · Samvaran Kashyap Rallabandi · Radhe Shyam Salopanthula |

---

## 1. What was at stake

MAUVE compares the *embedding distribution* of one batch of texts against another — no per-poem reference needed. The proposal leans on it as the distributional-semantics leg of evaluation, but multilingual embedders are trained on modern prose, and classical padya text is far out of distribution. So §5.2 commits to a gate before trusting it:

> **Held-out Pothana vs. Pothana must score near 1**, and Pothana vs. metrically-shaped gibberish must score **near 0**. If the conditions do not separate, MAUVE is not measuring what we need.

Every text unit here is one complete padyam embedded as a single 768-d vector. MAUVE then quantizes both point clouds with PCA + k-means (~n/10 buckets) and reports the area under the divergence frontier between the two histograms. All comparisons use equal sample sizes per side and 5 seeds.

## 2. The corpus behind the numbers

From the `bhagavatam.txt` dump we extracted **3,214 complete padyas** — poems only. Excluded:

- 1,537 vachanas and 9 gadyas (prose forms), 1 dandakam, 1 sloka
- Web boilerplate lines lodged inside verses («ఈ బ్రౌజరు అనుకూలం కాదు»)
- **1,030 verses truncated in the source itself** (fewer than 4 lines; 8 for సీసము)

No gloss (టీకా/భావము) leaks into any poem — verified. Top meters: కందము 1,017 · తేటగీతి 661 · సీసము 464 · ఆటవెలది 313 · మత్తేభము 224 · చంపకమాల 215 · ఉత్పలమాల 182 · శార్దూలము 100.

## 3. The gate, and the ladder past it

Beyond the two gate conditions we ran a full degradation ladder, each rung destroying more structure than the last. Mean over 5 seeds, ±1σ:

| Condition | MAUVE | n/side | Reading |
|---|---|---|---|
| Held-out split (stratified) | **0.957 ± 0.003** | 1601 | Same-distribution baseline. Gate condition A: near 1 ✓ |
| Held-out split (random) | 0.953 ± 0.004 | 1607 | Plain random 50/50 — stratification barely matters |
| Line shuffle (within poem) | 0.906 ± 0.007 | 1601 | Lines intact, stanza order destroyed (non-identity permutation forced) |
| Word shuffle (within poem) | 0.716 ± 0.034 | 1601 | Same vocabulary, per-line word counts preserved, order scrambled |
| Meter mismatch (vritta vs jati) | 0.214 ± 0.029 | 721 | ఉ/చ/మ/శా vs క/ఆ/తే — both sides canonical Pothana. Diagnostic |
| Akshara shuffle (within poem) | **0.028 ± 0.002** | 1601 | Poem's own aksharas kept, word identity destroyed |
| Akshara gibberish | **0.005 ± 0.000** | 1601 | Random corpus graphemes, matched structure. Gate condition B: near 0 ✓ |

The gate passes with a ~200× separation, and degradation is monotone: split > line-shuffle > word-shuffle > meter-mismatch > akshara-shuffle > gibberish. The cliff sits between word-shuffle (0.716) and akshara-shuffle (0.028): **word identity, not word order, is the embedder's load-bearing feature.**

### What each rung did to the opening verse (శార్దూలము, 1-1)

**Original** — baseline 0.957:

> శ్రీకైవల్య పదంబుఁ జేరుటకునైచింతించెదన్ లోక ర
> క్షైకారంభకు, భక్త పాలన కళాసంరంభకున్, దానవో
> ద్రేకస్తంభకుఁ, గేళి లోల విలసద్దృగ్జాల సంభూత నా
> నాకంజాత భవాండ కుంభకు, మహానందాంగనాడింభకున్.

**Line shuffle** — lines intact, stanza order destroyed — 0.906:

> శ్రీకైవల్య పదంబుఁ జేరుటకునైచింతించెదన్ లోక ర
> ద్రేకస్తంభకుఁ, గేళి లోల విలసద్దృగ్జాల సంభూత నా
> క్షైకారంభకు, భక్త పాలన కళాసంరంభకున్, దానవో
> నాకంజాత భవాండ కుంభకు, మహానందాంగనాడింభకున్.

**Word shuffle** — same words, order scrambled — 0.716:

> ద్రేకస్తంభకుఁ, కుంభకు, నాకంజాత సంభూత శ్రీకైవల్య
> భవాండ గేళి జేరుటకునైచింతించెదన్ లోక దానవో
> క్షైకారంభకు, పాలన ర మహానందాంగనాడింభకున్. భక్త నా
> కళాసంరంభకున్, పదంబుఁ విలసద్దృగ్జాల లోల

**Akshara shuffle** — the poem's own aksharas, word identity destroyed — 0.028:

> వోచెభజే లోదాంక్త కాభనల,కరతకునం కైల భ
> భపభూమశ్రీళి ళాబుఁ లోరుట డగక్షైదంనాకుచింన్ ద్దృ,.
> జాతిం,న్దకుం భసం రండిం స్తంభద్రేలలకం సనదా వాం
> హాతనాసం గ్జాపాగే కుల్యవనై కనాకుఁకభ,రంకువిన్కు

**Akshara gibberish** — corpus graphemes, matched lengths — 0.005:

> న్సార్మూన్వాంత్తేప్తన్భాడ్డంయ్యెంశధృచ్చుక్క్త్రంకోఁర్ఘా ద్ద్వి లైల్పొం విం
> రెంమోఁస్థ్యంష్ఠింర్వుఁక్లే ద్వ్యార్ధిథిఁల్చిర్దూత్త్వంనేంత్రుర్ఖ నఛబ నుంర్వుపన్దుః
> క్కంషప్పడ్గుఉం ష్ఠిప్రే క్షింవ్రీఫే మ్రం త్కాంష్క తాంస్మేశ్శన్నృన్స్వద్రత్క్షో
> ప్యాళ్లెర్చుఁ హఁత్కింర్వ్యద్భ్రాలెఁఢీస్సబోఁయ్యేఱ్ఱంత్ముచ్ఛఁఘాహశ్రో ళ్ళుగాఁ0 డ్పా

## 4. A second poet enters

Would the gate result generalize beyond one text — and what does MAUVE see between two impeccable canonical corpora? We converted **1,164 unique Vemana padyalu** (1,258 blocks, 94 exact duplicates removed; almost pure ఆటవెలది) and ran every comparison at matched sample size:

| Condition | MAUVE | n/side | Reading |
|---|---|---|---|
| Vemana vs Vemana (split) | 0.957 ± 0.015 | 582 | The gate generalizes to a second corpus |
| Pothana vs Pothana (split, matched n) | 0.952 ± 0.018 | 582 | Stratified split subsampled to the same n |
| Vemana vs Vemana (split, small n) | 0.957 ± 0.005 | 313 | Same-distribution reference for the row below |
| Pothana ఆటవెలది vs Vemana | **0.051 ± 0.007** | 313 | Meter-controlled: both sides pure ఆటవెలది |
| Pothana (mixed) vs Vemana | **0.031 ± 0.004** | 582 | Two canonical corpora, near the gibberish floor |

Both corpora pass their own split gate at ~0.96 — but against each other they score 0.03, near the gibberish floor. Restricting Pothana to its ఆటవెలది poems recovers almost nothing (0.05). The gap is **register and era, not meter mix**.

## 5. Findings

1. **The gate passes, and generalizes.** Same-distribution halves score ≈0.96 for both Pothana and Vemana; gibberish scores 0.005. EmbeddingGemma is usable for the Telugu-verse MAUVE protocol.
2. **Meter-matching is mandatory.** Vritta poems vs. jati/upajati poems — both canonical Pothana — collapse MAUVE to 0.21. An unmatched meter mix masquerades as a quality gap, exactly as §5.2's "meter-matched canonical verse" anticipates.
3. **Register-matching is just as mandatory — and this is new.** Pothana vs. Vemana scores 0.03 even meter-controlled. The reference pool must be matched on author/register/source-tradition, not just meter; §5.2 should be tightened accordingly, and every evaluation should name its reference corpus.
4. **MAUVE is a batch-composition instrument, not a per-poem coherence judge.** Scrambling every poem's line order costs only 0.05; scrambling word order only 0.24 — but destroying word identity while keeping the poem's own aksharas costs 0.93 (word-shuffle 0.716 → akshara-shuffle 0.028). The embedder is bag-of-*words*: real lexical items carry nearly all the signal, their order very little. Per-poem coherence must come from the Kavyalankara Sangrahamu suite and human ratings — the ladder is the concrete evidence for that division of labor.

## 6. Caveats & next steps

- The gibberish control is unconstrained akshara soup — a proxy for the proposal's *trie-valid* nonsense. Rerun once the metrical trie can generate.
- MAUVE values depend on unit size, n, and bucket count; ours are poem-level, n as marked per table, ~n/10 buckets. Generated batches must be scored against a meter- and register-matched pool at the same n.
- The bhagavatam.txt dump loses ~24% of padyas to truncation; a re-crawl would complete the corpus-contribution story (§4.3).
- For సీసము, "lines" are 8 half-lines, so line-shuffle is slightly harsher there than for 4-line meters.

---

**Code & data:** `MauveOnPothana/` — `extract_poems.py`, `extract_vemana.py`, `run_mauve_experiment.py`, `compare_vemana_pothana.py`, `results.json`, `results_vemana.json`.
**MAUVE:** Pillutla et al., NeurIPS 2021 (`mauve-text`, features supplied directly; no GPT-2 step).
