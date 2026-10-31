# Absent-word measurement (2026-10-05): is a corpus DAWG worth a v2?

`experiments/scripts/measure_absent_words.py` builds a suffix automaton (Blumer's DAWG, the structure of
arXiv 2307.01428) over the aksharas of the words of 90% of the real poems in `dataset/*.json` (15,415
poems; verse only — the Gemini-written meanings are not used) and scores every word by its minimal
absent factor (MAF): the shortest run of aksharas inside it that occurs inside no real word. Tables:
`absent_words.md` / `absent_words.json` (held-out real verse vs all 6,660 generated poems).

Share of words, by MAF (corpus word / attested inside a real word / MAF ≥ 4 / 3 / 2 / 1):

| set | corpus word | attested | MAF ≥ 4 | MAF 3 | MAF 2 (unseen pair) | MAF 1 (unseen akshara) |
|---|---|---|---|---|---|---|
| real verse, held out (33,619 words) | 55.5% | 6.6% | 8.4% | 20.2% | 9.0% | 0.3% |
| free baselines (E4B / 26B / Diffusion) | 42–46% | 8–12% | 5–10% | 24–31% | 9–13% | 0.0–1.1% |
| constrained, E4B (3 strategies) | 18–20% | 6% | 4% | 16–19% | 26–27% | 24–30% |
| constrained, 26B | 24–27% | 10% | 3% | 11–13% | 22–24% | 22–29% |
| constrained, DiffusionGemma | 29–33% | 8% | 1% | 12% | 21–24% | 21–27% |

* Free generation looks like real verse; the constraint is what produces the junk.
* Words where the constraint overrode the model on one of their tokens: junk (MAF ≤ 2) 60–67%, corpus
  words 10–16%; words the model wrote itself: corpus words 33–37% (E4B, 26B), 52–63% (DiffusionGemma).
* 8.8% of all aksharas in constrained poems never occur in 1,261,980 aksharas of real verse — 8,090
  distinct invented aksharas (ల్రు 839, ల్రి 737, న్యె 505, వ్రి 388, న్రి 348, య్రి 336, మమ్ 265 …).
  Real verse uses 3,879 distinct aksharas; the top 2,000 cover 99.62% of its akshara tokens.
* Allowed tokens at the steps where the constraint overrode the model: median 38–222; 11–22% of those
  steps had fewer than 10.
