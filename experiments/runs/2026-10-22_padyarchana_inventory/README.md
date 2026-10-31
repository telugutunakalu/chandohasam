# The `padyarchana` syllable inventory (2026-10-22)

**Why:** the v2 decoder's Layer A (`--inventory verse`) allowed only the 3,879 syllables of the verse in
`dataset/*.json` (15,415 poems), the only verse in the repo when v2 was built (2026-10-05..08). The user asked for
every akshara of the Padyarchana corpus instead. Built from the **E6 train split** (Padyarchana minus `dataset/`,
365,679 poems), so it holds no syllable only the held-out poems have, and it can serve their evaluation (the full
grid's 183 source poems are held out).

**Build:** `metrical_decoder.inventory.build_padyarchana_inventory()` → `inventories/padyarchana.txt`;
`--inventory padyarchana` in the CLI. 21.4M syllable tokens, 11,137 distinct, 10,413 writable by the orthography
filter.

| threshold (poems) | syllables | held-out verse syllable tokens allowed | verse-inventory syllables missing | new vs verse |
|---|---|---|---|---|
| ≥ 1 | 10,413 | 99.990% | 112 | 6,646 |
| ≥ 2 | 7,175 | 99.984% | 182 | 3,478 |
| **≥ 3 (chosen)** | **6,131** | **99.975%** | 251 | 2,503 |
| ≥ 5 | 5,115 | 99.963% | 370 | 1,606 |
| ≥ 10 | 4,095 | 99.937% | 576 | 792 |

Seen in one poem only: mostly typos and transliterations (డ్డ్డు, గ్పీ, హ్గ, న్ద్క్ష, స్విచ్, మూడ్); in 2–4 poems still some
doubtful clusters (ఙ్క్త, ఖ్క, ర్డ్సు, బ్ప). Hence ≥ 3.

**Junk it blocks:** words of the September v1 constrained grids with a syllable outside the inventory (would have
been blocked): E4B 27.1% (verse) → 22.4% (padyarchana ≥ 3; ≥ 2: 21.6%); Gemma-4 26B 25.0% → 21.1% (≥ 2: 20.2%).
Some of what the verse inventory blocked is real Telugu (వ్రి: 27 training poems).

**Checks (the decoder's acceptance criteria):**
- completeness (`experiments/scripts/check_inventory_completeness.py`, 351 held-out poems, 21 metres, 2 random token
  chunkings each): 225 pass without an inventory; with padyarchana 219 — 6 lost, **every one explained** by a syllable
  under the threshold (క్కోఁ, న్దుః, బ్దిం, ర్నో: 2 poems each; న్రోఁ: 1; న్శ్రి: 0); unexplained 0 (no liveness flaw).
  `completeness.json`, `completeness.log`.
- random-logit control (Gemma-4 E4B tokenizer, 37 metres × 3 strategies, T1, seed 42): 111/111 complete and in
  metre, no dead end. `control/`, `control.log`.
