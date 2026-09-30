# EXP-31: bigram prior and in-beam neural rescoring — summary

Full specification: [`../EXP-31-bigram-prior-and-in-beam-neural-rescoring.md`](../EXP-31-bigram-prior-and-in-beam-neural-rescoring.md).
**Status:** done (partial).

## Question
EXP-30 guarantees form and real words. Can better scoring turn those valid word sequences into sentences?

## Method
- A word-bigram prior replaces the frequency prior, and unattested pairings are penalised.
- The realiser scores partial lines inside the beam, not only finished candidates.
- The lexicon is restricted to frequent words, repetition is penalised, and the planner's content words
  are exempt from any frequency cap.

## Findings
- The word LM has 942,965 unigrams and 183,421 bigrams. The lattice has 259,222 edges, 13,736 after
  capping.
- **All four topics are valid**, using 20/29, 15/30, 15/31 and 14/30 planner words. In EXP-30's run the
  same topics used 7–13.
- Over development, planner-word use for the first topic went 0/20 → 10/24 → 20/29. The 0/20 is the
  spec's; the other two are in the logs.
- Two bugs were instructive:
  - frequency capping deleted the planner's words (0/20) until they were exempted;
  - restricting the lexicon removed junk words but dropped content use to 3/28 until the content bonus
    was raised.

  Form, lexicality and relevance pull against each other, and the weights are the dial.
- **Unsolved:** the outputs are well-formed word *sequences*, not sentences. A bigram cannot enforce
  agreement across a line.

## Evidence
- [`../composer_tuned.log`](../composer_tuned.log): the word LM, the lattice, and each topic's draft and
  composed padyam.
- [`../composed.json`](../composed.json): the four composed padyams, with prāsa, score, validity and planner
  words used.
- The code (`padyam/lattice.py::bigram_scorer`) is not in this repository.
