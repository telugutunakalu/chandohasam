# E6 comparison: DiffusionGemma beside the MDLMs and Nandi (114 val poems, 1 per prompt)

Scored by ../RL/reward.py (the RL report's definitions). Real words with ఁ stripped on both sides (poems and training lexicon) for every model. Recognition is a topic signal, not meaning. Constrained = masking + backtracking (MDLMs, Nandi: the E6 runs; DiffusionGemma: our diffusion decoder with the NaN-entropy fix and the settled commit).

| set | poems | in metre % | chandas skill mean / median | vṛtta lines on pattern % | real words % (ఁ stripped) | one-akshara % | copy % | recognised (raw) % | repeating a line % | lines |
|---|---|---|---|---|---|---|---|---|---|---|
| gold (real poems) | 114 | 39.5 | 0.96 / 1.00 | 98.6 | 86.8 | 7.0 | 2.5 | 78.1 | 0.0 | 4.00 |
| MDLM 120M, free | 114 | 0.0 | 0.52 / 0.61 | 11.6 | 90.0 | 8.6 | 6.2 | 86.0 | 0.0 | 3.93 |
| MDLM 120M, constrained | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 81.1 | 11.4 | 2.9 | 76.3 | 0.0 | 4.00 |
| MDLM 523M, free | 114 | 0.0 | 0.67 / 0.71 | 34.6 | 88.3 | 8.4 | 5.7 | 85.1 | 0.0 | 3.99 |
| MDLM 523M, constrained | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 83.1 | 10.3 | 3.1 | 81.6 | 0.0 | 4.00 |
| Nandi-Mini-150M, free | 114 | 3.5 | 0.88 / 0.92 | 76.4 | 79.5 | 7.5 | 1.8 | 74.6 | 0.0 | 4.00 |
| Nandi-Mini-150M, constrained | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 76.6 | 8.0 | 1.5 | 74.6 | 0.0 | 4.00 |
| DiffusionGemma base, free (native) | 114 | 0.0 | -1.06 / -0.87 | 0.0 | 92.3 | 4.8 | 21.2 | 62.3 | 0.0 | 4.00 |
| DiffusionGemma LoRA 24k, free (native) | 114 | 0.0 | -0.69 / -0.57 | 0.0 | 67.9 | 9.9 | 18.9 | 95.6 | 0.9 | 3.13 |
| DiffusionGemma LoRA 48k, free (native) | 114 | 0.0 | -0.59 / -0.48 | 0.0 | 70.0 | 9.4 | 20.8 | 91.2 | 0.9 | 3.19 |
| DiffusionGemma LoRA full pool, free (native) | 114 | 0.0 | 0.07 / 0.16 | 0.0 | 80.2 | 4.3 | 13.9 | 95.6 | 0.0 | 3.89 |
| DiffusionGemma base, constrained (fixed + settled) | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 35.0 | 22.1 | 1.8 | 27.2 | 0.0 | 4.00 |
| DiffusionGemma LoRA 48k, constrained (fixed + settled) | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 29.6 | 17.9 | 2.3 | 63.2 | 7.0 | 4.00 |
| T5Gemma 2 270M (full pool), free | 114 | 8.8 | 0.89 / 0.96 | 74.3 | 80.4 | 5.9 | 2.7 | 77.2 | 0.0 | 4.00 |
| T5Gemma 2 1B (full pool), free | 114 | 6.1 | 0.90 / 0.96 | 77.1 | 82.5 | 5.8 | 3.0 | 77.2 | 0.9 | 4.00 |
| T5Gemma 2 270M (full pool), constrained | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 77.0 | 6.0 | 3.2 | 83.3 | 0.0 | 4.00 |
| T5Gemma 2 1B (full pool), constrained | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 79.2 | 5.2 | 2.4 | 79.8 | 0.0 | 4.00 |
| T5Gemma 2 1B (full pool), constrained, v2 Layer A (padyarchana inventory) | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 78.3 | 5.6 | 2.2 | 79.8 | 0.0 | 4.00 |
| T5Gemma 2 1B (full pool), constrained, v2 A + B (padyarchana inventory and words, weight 2, every step) | 114 | 100.0 | 1.00 / 1.00 | 100.0 | 83.4 | 4.6 | 3.3 | 79.8 | 0.0 | 4.00 |
| T5Gemma 2 4B LoRA (first 48k of the pool), free | 114 | 0.0 | 0.52 / 0.62 | 14.7 | 76.4 | 5.8 | 3.9 | 67.5 | 0.0 | 3.97 |
| T5Gemma 2 4B LoRA (full pool), free | 114 | 7.9 | 0.87 / 0.93 | 68.2 | 81.0 | 5.5 | 2.5 | 77.2 | 0.9 | 4.00 |
