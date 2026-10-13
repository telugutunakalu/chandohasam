# Chandohasam progress seminar: speaker notes

Deck: `chandohasam_seminar.pptx` (editable, 28 slides = title + 26 content slides + closing); PDF: `chandohasam_seminar.pdf`; figures used by the deck: `figures/`.

Source of every number and claim: the mid-submission paper *Chandohasam: Towards Semantically Coherent Telugu Metrical Poetry Generation with Text Diffusion* (Tables 1, 2, 4, 5, 6; Figures 1, 2; Algorithms 1 to 4; §1 to §6). Each slide note below starts with the paper section it is grounded in. Three items are **not** in the paper and are marked as such: the pilot120m training-loss curve (slide 19), the kandamu rule-card figure (slide 8) and the pilot120m architecture figure (slide 18), all from the project write-ups, and the demonstration output (slides 7 and 27), which is the live output of `python3 -m chandohasam` and `python3 -m indic_meter_dawg prefix` on Pothana’s opening verse.

## The narrative

1. **The problem.** A padyaṃ must balance śabdaṃ (sound) and arthaṃ (meaning). Prior work solves one at the expense of the other: soft control drifts, hard control produces metrically perfect verse that humans rate 2.1 to 2.7 of 5. Telugu adds three positional constraints per line, 37 metres in three families, an alpha-syllabary script and an evaluation gap.
2. **Chandassu.** Akṣara weights, gaṇas, yati and prāsa; what the controller annotates; fixed, class-based and composite metres.
3. **The benchmark.** 12,673 labelled poems from four sources, audited for metre, meaning and duplication.
4. **The controller.** Constrained decoding as a puzzle; the DAWG; one labelled DAWG for 37 metres (1,431 states, 370,315 lines, 99.85% on the Bhāgavatamu); the enforcer; plugging it into autoregressive and diffusion models.
5. **Results.** Form by construction for every model (0 → 555 in metre); the lexical cost of subword tokens; our 120M akṣara-level diffusion model keeps the words; MAUVE says no one writes like the corpus yet; scale does not buy coherence.
6. **Measuring poetry and the road ahead.** Why validity is not quality; the five deterministic metrics; the metrics in design; the full framework with RLVR; progress so far; next steps to 31 October 2026; a live demonstration.

Timing: about 1.5 minutes per content slide gives 40 minutes plus questions. If time is short, compress slides 12 and 13 (DAWG) into one and skip slide 22 (caṃdomiti details).

## Live demonstration (slide 27)

```bash
cd meter_engine
python3 -m chandohasam --file poem.txt            # poem.txt = presentation/demo_poem.txt, the four pādas of slide 27
python3 -m indic_meter_dawg prefix UUUI        # metres still completable after the prefix
python3 -m indic_meter_dawg stats                 # 37 metres, 1,431 states, 2,514 edges, 370,315 lines
```

## Slide-by-slide notes

### Slide 1: Title

Welcome. This seminar reports the progress of Chandohasam as written up in the mid-submission paper. The decorative line is the weight pattern (ma sa ja sa ta ta ga) of śārdūlavikrīḍitamu, the metre of the Bhāgavatamu’s opening verse, which returns in the demonstration.

### Slide 2: The narrative in one page

Six movements. 1: the problem, a padyaṃ must balance sound and sense. 2: what chandassu asks of every line. 3: the benchmark and its audit. 4: the deterministic controller (DAWG) and constrained decoding. 5: the results with four generators and our own 120M diffusion model. 6: how to measure poetry, the final architecture and the plan. The story: form is now guaranteed by construction; meaning under form is the open problem and the rest of the project attacks it.

### Slide 3: Problem statement

Goal (paper, abstract and §1): compose Telugu padyaṃs that are metrically accurate and genuinely meaningful at the same time. Three requirements, all at once: strict metre (gaṇa, yati, prāsa), coherent meaning for a given bhāvaṃ, and poetic expression (figures of sound and of meaning). Prior work struggles to satisfy the joint requirement. Our answer is a constrained text-diffusion framework: a deterministic metrical controller guarantees form, the generator supplies words and meaning, a poetry evaluation suite and a semantic coherence metric measure what the controller cannot, and RLVR uses them as rewards.

### Slide 4: Why poetry is hard: śabdaṃ and arthaṃ in balance

Paper §1. A poem must do far more than make surface sense. The left circle is the sound side: gaṇa, yati, prāsa, and the figures of sound. The right circle is the meaning side: coherent ideas, contextual fit, and the figures of meaning. The padyaṃ lives in the overlap, which the classical tradition calls śabdārtha samanvaya, sound and sense in equivalence. Pull one way and you get metrically perfect nonsense; pull the other and you get prose. The intertwined constraints make Telugu poetry harder than conventional text generation and than poetry generation in English, Chinese or Hindi.

### Slide 5: Existing methods and their flaws

Paper §2. Two routes. The soft route steers a model and discards failures: Deep-speare (English sonnets), SongNet (Chinese SongCi), PoeLM (control codes, generate many, keep what passes a scansion check; Spanish and Basque), and a Bangla adaptation with rhyme, matra-count, word-count and line-boundary tokens that follows the requested structure over 90% of the time. But those constraints are aggregates, and the authors report semantic drift when several control tokens apply at once. The hard route guarantees form at decode time (Ghazvininejad 2016, NeuroLogic 2021, grammar-constrained decoding 2023). For Sanskrit, Chandomitra and PINGALA reach near-perfect Anushtubh metre with greedy decoding, yet human raters score coherence at 2.1 to 2.7 out of 5. PoetryDiffusion aims at both with text diffusion and a BERT-based metrical controller. Our position: keep a deterministic controller inside the decoding loop and work on meaning.

### Slide 6: Why Telugu is different

Paper §1 to §2 and §4.2. Four reasons. One: every line carries three simultaneous constraints, gaṇa, yati and prāsa, which are positional, not aggregates like a matra total or an end rhyme. Two: 37 metres in three families, including class-based (jāti) metres whose gaṇas are chosen from classes, and composite (upajāti) metres. Three: the alpha-syllabary script. The weight of an akṣara stays pending until the next onset is known, because a following conjunct makes it heavy, and sandhi can hide a yati seat; a general subword tokenizer spends 1.2 to 1.4 tokens per akṣara. Four: the evaluation gap. Sanskrit has a deterministic metre identifier; Telugu had only an approximate post-hoc checker; nothing exists for meaning; MAUVE is unvalidated on classical poetry; śabdālaṅkāra identifiers exist only for Sanskrit, and arthālaṅkāras are out of reach for deterministic modelling.

### Slide 7: Chandassu and the akṣara: what is annotated

Paper, Appendix A terms and §4.2. An akṣara is a syllable; it is guru (heavy, U) or laghu (light, I). A gaṇa is a fixed group of weights: bha = UII, ja = IUI, sa = IIU, na = III, ya = IUU, ra = UIU, ta = UUI, ma = UUU, ga = U, va = IU, gaga = UU. A poem has pādas (lines). At a yati seat the akṣara must agree in sound (maitri) with the vaḷi, the first akṣara of the line. By prāsa, the second akṣara of every line repeats the consonant of the second akṣara of line 1. On the right is the controller’s own annotation of pāda 1 of Pothana’s opening verse: scanned into akṣaras with weights, split into gaṇas ma sa ja sa ta ta ga, the yati at akṣara 13 matched to the vaḷi, the prāsa consonant క held across all four lines. Note the pāda-final laghu read as guru. Weights are settled by the following onset, so the annotation is a lattice until the next consonant is known.

### Slide 8: Three families of metres: fixed, class-based, composite

Paper, Table 6 (the 37 metres). Vṛtta (26): a fixed gaṇa sequence per pāda, e.g. utpalamāla bha ra na bha bha ra va, 20 akṣaras, yati at akṣara 10; śārdūlavikrīḍitamu ma sa ja sa ta ta ga, 19 akṣaras, yati at 13; some have two or three yati seats (sragdhara 8 and 15; mānini 7, 13, 19). Jāti (8): the line is a sequence of gaṇa classes, and each position may take any gaṇa of its class: sūrya = na, ha; indra = bha, ra, ta, nala, naga, sala; kanda = bha, ja, sa, nala, gaga. So the line length varies and the yati sits at the first akṣara of a given gaṇa. Kandamu has two slots, odd lines of 3 kanda gaṇas and even lines of 5. Upajāti (3): sīsamu (6 indra + 2 sūrya, followed by a gīti), āṭaveladi, tēṭagīti; no prāsa, and prāsa-yati is accepted in place of yati. The figure shows the controller’s rule card for kandamu, with the yati seat at gaṇa 4 of the even slot.

### Slide 9: Constrained decoding is a puzzle with no dead ends

Paper §4.1 (viable_prefix, next_symbols) and §4.2. Think of writing the poem as solving a puzzle. Each akṣara placed narrows the set of metres that can still be completed. The chain shows the controller’s own viable_prefix query: after one guru, 28 (metre, slot) hypotheses are alive; after U U, 14; after U U U, 7; after U U U I, 4; after U U U I I U, 3; after U U U I I U I U, only śārdūlavikrīḍitamu remains. A move that leaves no completable metre is simply not offered. Rules of the game: the gaṇa grid masks from the first token; prāsa and yati act once their anchor is written; liveness is exact, so there are no dead ends and every finished poem is valid; the language model chooses among allowed moves, the controller never writes the poem; and meaning has no closed-form check, it is left to the generator and the evaluation.

### Slide 10: The benchmark: 12,673 labelled poems, four sources

Paper §3 and Table 1. Sources: Pothana’s Āndhra Mahābhāgavatamu from an online compilation with word glosses and meanings (the golden set: largest, edition meanings); Vemana’s śatakam; Kuchimanchi Timmakavi’s acca-telugu Rāmāyaṇamu and three śatakams; and the Chandassu dataset of Pavan and Sree (2025) from its Kaggle release. Meanings for the last three are LLM-generated (Gemini), and every English meaning is a machine translation of the Telugu bhāvaṃ. Table 1 gives the validity rates the controller measures: gaṇa 95.3% overall (99.85% on Bhāgavatamu), prāsa 99.2% relaxed and 95.9% strict, yati 91.5% relaxed and 90.6% strict. Chandassu and Vemana are the noisiest on gaṇa, 85.0% and 87.2%.

### Slide 11: Data sanity: do the meanings belong to their poems?

Paper §3 and Table 2. Two gates compare each poem with its own meaning against a shuffled pairing. The length-ratio gate (meaning length over verse length in [0.8, 2.5]) separates real from shuffled in three files, 96 to 98% against 62 to 67%, but not in Vemana, whose machine meanings are of uniform length (84.5% against 82.6%). The LaBSE Telugu–English gate (cosine at or above 0.65) passes 90 to 98% of real pairs and none of the shuffled, but it measures translation consistency since the English is a translation of the Telugu meaning; on the pair that bears on fidelity, poem versus Telugu meaning, LaBSE still ranks the correct pairing first with AUC 0.85 to 0.94. Lexical diversity is similar across files (type–token ratio 0.59 to 0.64). Verbatim duplication is negligible: 13 near-duplicate pairs among 12,704 poems. The remaining repetition is formulaic: refrains recur in 77.1% of Vemana’s poems and 25.3% of Chandassu’s, which raises Vemana’s Yule’s K to 99.9 against 1.4 to 4.1 elsewhere; evaluation splits must keep refrain groups together. A general subword tokenizer (Gemma-4) spends 1.23 to 1.36 tokens per akṣara, which motivates the syllable tokenizer.

### Slide 12: The DAWG: every legal line of a metre, stored once

Paper §4.1 and Figure 1. Take a toy slot of two gaṇas, each UU, IIU or UII. It has 9 legal lines. Stored as a trie, that is 29 states, because the three ways of finishing gaṇa 1 each carry their own copy of gaṇa 2. A DAWG, a minimal deterministic acyclic automaton, merges states with equal futures: the three ways to finish gaṇa 1 meet in one state and gaṇa 2 is stored once, 11 states and 14 edges for the same 9 lines. The decoder’s question is: after the prefix U I, what may follow? Here only I. Construction follows Daciuk et al. (2000) and the full catalogue builds in under half a second.

### Slide 13: One labelled DAWG for all 37 metres

Paper §4.1 and Algorithm 1. The rules are data: YAML specifications of 37 metres and their gaṇa classes, with 64 prāsa and 92 yati rules derived from Kakanuri Appakavi’s Appakavīyaṃ. Each metre is a prosodic grammar, poem → lines → gaṇa classes → gaṇas → U/I. The grammar is flattened into one right-linear grammar per line slot (a vṛtta has one slot; kandamu has two, its odd and even lines), turned into an automaton per slot, united, made deterministic into a DFA of 1,573 states whose accepting states carry their (metre, slot) labels, and then minimised while preserving labels into the DAWG: 1,431 states, 2,514 edges, exactly the 370,315 legal lines, built in under half a second. Three queries: identify walks a poem’s scansion lattice and returns every accepting metre and slot and the point at which each rejected metre became impossible; viable_prefix and next_symbols return what can still lead to a completed slot; segment returns gaṇa divisions and yati positions. Validation, independent of generation: of 7,366 Bhāgavatamu poems with catalogue metres, 7,355 are identified with their labelled metre (99.85%), none as a wrong metre, and 10 are rejected as unclassified.

### Slide 14: Inside the decoding loop: the enforcer

Paper §4.2 and Algorithm 2. The DAWG is a hard constraint, not a post-hoc validator. The enforcer keeps a state with four parts: the live automaton states of the chosen metre, the last akṣaras whose weight is still open, the prāsa register (the consonant of line 1’s second akṣara) and the yati register (the line’s first akṣara, the vaḷi). For each new akṣara: settle the open weights by its first consonant; move every live state along the settled weights and drop those with no move; if it is the second akṣara of a line and breaks the prāsa, DEAD; drop the states whose gaṇa division puts it on a yati seat where it is not in maitri with the vaḷi; if no state can still reach the end of the poem, DEAD. A token is allowed when the state stays alive after all of its akṣaras, cached per state. Because liveness is exact, a valid decoding path cannot reach a dead end, and every completed poem satisfies the selected metre and its structural constraints.

### Slide 15: The same controller on autoregressive and diffusion models

Paper §4.2, §4.3 and Algorithm 3. Four generators, one controller, applied as ablations so that the effect of the model and the decoding paradigm is isolated with the formal constraints fixed. Autoregressive (gemma-4-E4B-it, gemma-4-26B-A4B-it): the DAWG masks the next-token distribution directly; initial temperature 0.7. Block diffusion (diffusiongemma-26B-A4B-it-NVFP4): the model’s proposals are committed left to right when allowed and sufficiently confident; otherwise decoding selects the first open position, and a backtrack returns committed positions to noise. Masked diffusion (chandohasam 120M, ours): the constraint is applied to the positions being resolved while the committed context the controller needs is preserved; a 512-token canvas with the meaning unmasked, lines decoded left to right within the line. Three strategies: masking only samples from the model after removing invalid tokens (top-p 90%); masking with backtracking saves checkpoints every third step (last 15), rewinds when stuck (fewer than 3 allowed tokens, less than 0.001 of the probability mass, or 4 steps without a new akṣara) and raises the temperature by 0.15 per consecutive backtrack up to 1.2; hybrid walks the allowed tokens by probability (at most 100) collecting those that complete the line.

### Slide 16: Results: the constrained-decoding grid

Paper §5 and Table 5. Every row uses the same grid: 37 metres × 3 topics × 5 seeds = 555 poems per model and decoding mode. A poem is in metre if it is complete and satisfies its canonical gaṇa, strict prāsa and strict yati with no sandhi assumed. Attested: words of two or more akṣaras found in held-out verse (topic words excluded); distinct: distinct attested words; single akṣara: share of words that are one akṣara; strong anuprāsa and obscure: the extreme bands of the poetics metrics; MAUVE against real verse of the same metre mix (120 a side, 5 seeds). Read the table row-pair by row-pair: free decoding never lands in metre; constrained decoding always does; and then look at what the constraint costs each model in words.

### Slide 17: Results: form is guaranteed, words are the cost

Paper §5. Finding 1: unconstrained, no model writes a poem in metre; constrained, all 555 are in metre for every model. Form is guaranteed by the decoder, not learned. Finding 2: for the subword Gemma models the guarantee has a lexical cost: attested words fall from 33.7–37.2% to 10.7–16.9%, 33.7–71.9% of the poems reach a strong anuprāsa that only 2.7% of real verse reaches, and 91.0–98.9% are rated obscure against 10.0% of real verse. Finding 3: Chandohasam 120M, whose tokens are single akṣaras, keeps 36.9% attested words under the same rules, about the subword models’ unconstrained level, with 757 distinct attested words, roughly twice their 323–375; its deficits reflect pretraining without verse: 19.7% single-akṣara words (real 5.6%) and 62.9% obscure. Finding 4: MAUVE confirms that no system yet writes like the corpus; the constraint raises it for every model, but every generated row stays between 0.006 and 0.057 against 0.965 for real verse. Finding 5: layer probes of the Gemma E2B and E4B variants and the recorded token-wise probabilities show that regardless of size all generations underperform equally, so parameter scaling does not have a significant effect on coherence.

### Slide 18: Pretraining our own diffusion model, one token per akṣara

Paper §4.4. Why an akṣara tokenizer: the controller reasons in akṣara weights, and an akṣara’s weight is settled by the next onset. A general subword tokenizer spends 1.2 to 1.4 tokens per akṣara (Table 2), so a token can hold part of an akṣara or several, and masking at that granularity is what strips the Gemma models of their vocabulary. We design a syllable-based tokenizer aware of akṣara boundaries: 45,591 tokens that cover 99.8% of the akṣara types in our verse, so the constraint acts on single syllables, the tokens themselves. The model, chandohasam 120M, is a 120M-parameter bidirectional transformer (12 layers, hidden size 768, rotary positions, SwiGLU) trained from scratch as a masked diffusion language model (MDLM, Sahoo et al., 2024). It saw 4.98B tokens of Telugu prose from Sangraha, IndicCorp v2 and Wikipedia on a single 8 GB laptop GPU in 2 days 19 hours. Generation fills a 512-token canvas in which the meaning is given unmasked, and the metre’s lines are decoded left to right within the line. The architecture figure comes from the project write-up and matches the paper’s description.

### Slide 19: What pretraining bought us

Paper §4.4 and the Chandohasam 120M rows of Table 5; the loss curve is from the project write-up and is NOT in the paper (validation NELBO fell from 2.921 at step 1k to 1.747 over 76,000 steps of 65,536 tokens; test NELBO 1.783 nats per token, weighted like the training mix). From the paper: the model trained on prose only, in 2 days 19 hours on an 8 GB GPU. Under the controller it keeps 36.9% attested words, up from 17.9% free, with 757 distinct attested words against 183, and MAUVE 0.035 against 0.006; both the opposite direction from the subword models, for which the constraint removed vocabulary. What it still lacks reflects pretraining without verse: 19.7% of its words are single akṣaras (real verse 5.6%) and 62.9% of its poems are rated obscure (real 10.0%), and MAUVE is still far from the 0.965 of real verse. Fine-tuning on the poetry corpus is the next step.

### Slide 20: Why poetry needs its own metrics, for sound and for sense

Paper §2 (evaluation side) and §4.6. On the sound side, metre identification is solved by the controller, but validity is binary; we also need graded measures of how far a poem is from a metre and of its sound qualities. On the meaning side nothing existed: for Sanskrit the only coherence measure was a human rating (2.1 to 2.7 of 5); MAUVE was built for human-versus-AI detection and is unvalidated on classical poetry; a training loss does not say whether a poem reads like Telugu. The classical treatise Kāvyālaṅkārasaṅgrahamu (16th c., Bhattumurthy) codifies the sound qualities: anuprāsa, mādhurya, ojas, prasāda and the śabdālaṅkāras, and its alpha-syllabary rules transfer from the Sanskrit identifiers. The suite separates hard structural validity from the semantic, stylistic and poetic qualities of a poem, and later becomes the reward for RLVR.

### Slide 21: The poetry evaluation suite: four sound qualities

Paper Table 4. Anuprāsa (alliteration): A observed same-sound consonant pairs across different akṣaras within a line, E the expected pairs under corpus unigram frequencies, z = (A − E)/√V with V the chance variance; line levels at z = 1.645, 2.326 and 3.090; the poem score is the mean line level. Mādhurya (euphony): M = I − P, I the mean akṣara weight, P the mean harsh-akṣara run load; harsh below −0.283, leaning harsh to −0.123, balanced to 0.049, leaning soft to 0.156, soft above. Ojas (lexical density): O = (W + J)/2 with W = 100(1 − words/akṣaras) and J = 100 × conjunct-initial akṣaras / akṣaras; light below 39.3 up to dense at or above 47.5. Prasāda (clarity): H, the bits per akṣara of the sequence under a reference akṣara trigram model; clear below 5.12, leaning clear to 5.54, ordinary to 6.33, leaning obscure to 7.06, obscure above. Each quantifies a poetic property independently of metrical validity.

### Slide 22: caṃdomiti: a graded distance to the nearest valid metre

Paper Table 4 and Algorithm 4. Caṃdomiti, the chandas distance, is the minimum number of akṣara edits that make a poem conform to a specified metre, including weight, yati and prāsa constraints: D = Dw + Dy + Dp. Weight edits come from a dynamic programme over the slot’s own automaton: reading an akṣara along an edge costs 0 if the edge’s weight is one the akṣara may take, else 1 (substitution); skipping it costs 1 (deletion); following an edge without reading costs 1 (insertion); a pāda-final laghu may also read as U, and the path gives the nearest legal line. Lines are matched to the metre’s pādas with the fewest edits; a line left over costs its length, a pāda left empty its shortest line. Yati edits: one for each yati seat whose akṣara is not in maitri with the vaḷi. Prāsa edits: the fewest pādas to change so that all the pādas rhyme. An akṣara a weight edit already rewrites is counted once. The rate r = D / max(n, N) is chance-corrected per metre: S = 1 − r / r_chance(m), with r_chance the mean rate of prose cut to the line lengths of m. Rubric: exact (D = 0), slip, partial, weak, unmetered (r at or above the metre-specific chance cut).

### Slide 23: Metrics in design

Paper §4.6 and §6. Four things are being built next on the evaluation side. A word resolution metric aligned with a compiled Telugu macro-dictionary resolves the lexicon of classical Telugu after sandhi and samāsa splitting, measuring word-level coherence across the poem; in the architecture it also acts as a lexical gate that rejects candidates with no valid segmentation. A semantic coherence metric modelled on expert human acceptability judgements on Telugu metrical poetry, validated against the ratings; it is evaluated apart from the controller because meaning cannot be reduced to formal constraints. Deterministic identifiers for the śabdālaṅkāras, adapted from the Sanskrit yamaka and anuprāsa identifiers. And a euphony index whose weights over sound euphony, alliteration and word density are learned. Arthālaṅkāras stay out of scope.

### Slide 24: The Chandohasam framework: diffusion, controller, rewards

Paper Figure 2, §4 and §4.7. The generator is a masked diffusion language model whose canvas length is fixed a priori by the metre; it denoises from noise to a Telugu padyaṃ in akṣara tokens. Below it sits the deterministic metrical DAWG controller, which replaces the learned BERT metrical classifier of PoetryDiffusion: no loss terms, no gradients, an exact verdict with gaṇa, yati and prāsa predictions, plus the edit distance D. A lexical gate backed by the macro-dictionary resolves words after sandhi and samāsa splitting and rejects candidates with no valid segmentation. The sampled padyaṃ is scored by the poetics suite: anuprāsa, mādhurya, ojas, prasāda and caṃdomiti, combined as R = Σ λi ri together with the śabdālaṅkāra checks and the semantic coherence metric, and the policy is updated with RLVR. The DAWG stays active during RLVR generation, so metre, yati and prāsa remain hard constraints and RLVR optimises quality within the valid region. Each model is trained independently and its RLVR variant is compared against its base.

### Slide 25: Progress so far

Paper §6, first paragraph. Established: the dataset of 12,673 labelled poems with its sanity audit; the deterministic metrical controller over 37 metres, validated at 99.85% on the Bhāgavatamu; the poetry evaluation suite of five metrics operationalised from Kāvyālaṅkārasaṅgrahamu; baseline generations in free and constrained settings for four models, 555 poems per model and mode, with MAUVE against real verse; and our own 120M masked-diffusion model pretrained from scratch with an akṣara tokenizer. What remains centres on meaning: evaluating and improving semantic coherence, extending the metrics and modelling the coherence metric against human evaluations.

### Slide 26: Next steps and timeline

Paper §6. Seven items. 1 Word resolution metric for word-level coherence inside a poem. 2 Human evaluation on generated and reference poems with the final rubric and a frozen test split. 3 Semantic coherence metric from the human acceptability judgements, validated against the ratings; in parallel, learn the weights of the euphony index. 4 Poetry fine-tuning of the diffusion model on the curated corpus, including the meaning-to-poem setting and ablations. 5 RLVR with the metrical constraints, the evaluation suite and the coherence metric as verifiable rewards, against rejection sampling and other constrained-generation baselines. 6 Final evaluation of all systems and the corpus with the automatic metrics, MAUVE and human evaluations, and an analysis of how automatic metrics relate to human judgements. 7 Final report and release of the controller, benchmark, evaluation suite and human ratings; final paper by 31 October 2026.

### Slide 27: Demonstration: reading Pothana’s opening verse

Live demo cue: run `python3 -m chandohasam --file ../presentation/demo_poem.txt` from meter_engine/ (the four pādas shown), and `python3 -m indic_meter_dawg prefix UUUI` for the narrowing query. The slide shows the tool’s actual output. The controller identifies śārdūlavikrīḍitamu, splits every pāda into ma sa ja sa ta ta ga, confirms yati at akṣara 13 in all four pādas (sound-class matches with the vaḷi: śrī–ciṃ, kṣai–saṃ, drē–ddṛ, nā–naṃ) and prāsa on the consonant క at the second akṣara of every pāda. Note the pāda-final laghu of line 1 read as guru. Then show the prefix query: with each weight the set of completable metres narrows, 28 → 14 → 7 → 4 → 3 → 1, which is exactly what the enforcer uses to mask tokens during generation.

### Slide 28: Thank you

Closing. Invite questions. The demonstration can be re-run live from meter_engine/.
