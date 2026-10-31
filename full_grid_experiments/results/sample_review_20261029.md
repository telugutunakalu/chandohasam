# Random-sample review: dataset/kuchimanchi_timmakavi:kuchimanchi-87 · mattebhavikriditamu

Drawn by random.Random(20261029).choice over the 100 grid prompts. One poem per cell (seed 42). Scorer verdicts from results/grid_poems.jsonl; non-words: words of ≥ 2 syllables the real-words matcher rejects (ఁ stripped).

**Bhāvam (the prompt):** ఓ పార్వతీపతి! ఓ భార్గవ! కలియుగంలో పాపాలు పెరిగిపోవడం వల్ల గోసంగులు, పవినాలు, వివేకం లేని మోటకాపు దొరలు, పాషాండులు, దాసరులు, శివసత్తులు, మతిమరుపు చెందిన పెద్దలు, బానిసల్లా ప్రవర్తించే ప్రభువులు మరియు చెడ్డ కవులు విపరీతంగా విస్తరిస్తున్నారు. వీరి నడుమ ఉన్న పరిస్థితిని నేను ఇంకా ఎలా వర్ణించగలను?

## What this sample shows (one prompt, 50 poems; my reading, not a human rating)

The drawn prompt is Kūcimañci 87 (mattebhavikrīḍitamu). The bhāvam is a list of groups that thrive in the Kali age, ending in the question "how can I describe it", addressed to Śiva. It is a demanding prompt, because the list of named groups is the poem.

**By reading:**
- **Constrained, base models (17 poems): all are gibberish or loops.** Even when the metre is perfect, nothing of the bhāvam survives beyond a few fragments.
- **Constrained, fine-tuned models (16 poems):**
  - 8 are readable and on the bhāvam: Nandi FT v1, T5 270M FT v2, T5 1B FT v2, T5 4B FT v1 and v2, MDLM 120M FT v1, MDLM 523M FT v1 and v2.
  - 5 are partial.
  - 3 fail: DiffusionGemma FT v1 and v2, T5 4B 48k v2.
  - The best is MDLM 523M FT v1. The best single line is T5 4B FT v1's pāda 4.
- **Free:**
  - The fine-tuned rows give the poems closest to the gold in content and diction: near-metrical (skill 0.89–0.96) but not strictly in metre.
  - The base rows give prose, loops, metadata or a paraphrase of the bhāvam.

**Where the scorer's measures go wrong on this prompt:**
1. **In metre (strict)** fails the gold: the strict reader doesn't carry a word-initial conjunct back across a space (Kūcimañci's detached drutam, as in బాషాండులు న్దాసరుల్). It also passes syllables that cannot be written (MDLM 120M base v1: వ్వ్వ).
2. **Real words** misses in both directions.
   - *Missed real words:* sandhi chains, gasaḍadavādeśa forms (గల్పాంతముల్, గలుషంబుల్), the detached drutam, words split across pādas, dialect spellings, and lexicon gaps for the prompt's own nouns (దాసరుల్, శివసత్తుల్, పాషాండులు). The gold scores 50%, and the good fine-tuned poems are undercounted by roughly 15–30 points.
   - *Accepted non-words:* invented compounds (Gemma-4 26B free: బలియుగమున, మలియుగమున, నలియుగమున; 94%). Prose scores 78–98%, and a repeated line counts as many real words (Gemma-4 26B v2: one line ×4 gives 60%).
   - It measures validity, not sense. Real words used in the wrong sense count fully (గోవులం, కౌశేయ, పులకంబుల్, పవళించున్).
3. **Recognised** is noisy for a single poem.
   - Clear false positives on gibberish: Nandi base v2, MDLM 120M base v2, DiffusionGemma FT v1.
   - Borderline (prompt-word fragments in gibberish): Gemma-4 26B v1, T5 1B base v1, DiffusionGemma FT v2.
   - False negatives on on-topic poems: MDLM 120M FT free, MDLM 523M FT v2.
4. **Repeated line** catches exact repeats but misses two things:
   - Near-repeats that change only the first akshara (Nandi base v1, T5 270M base v1, T5 1B base v1). This is how base models satisfy gaṇa and prāsa cheaply.
   - Loops inside one line (Nandi base free).
5. **Skill** is 1.00 for every constrained poem, so it doesn't separate them. It does separate free poems (fine-tuned 0.89–0.96, base negative).
6. **None of the measures checks the bhāvam's content.** No measure checks whether the named groups, the question and the addressee are present. That is where poems differ most (the wrong addressee in T5 270M FT v1, the inverted sense in MDLM 523M FT v2, the added community name in MDLM 120M FT v1).

**v1 vs v2 on this prompt:**
- Layer A removed impossible syllables everywhere.
- Layer B raised real words in 5 of the 8 fine-tuned rows (Nandi, T5 1B, T5 4B, MDLM 523M, DiffusionGemma). T5 270M was unchanged, and T5 4B 48k and MDLM 120M went down.
- The sense was better in T5 270M FT and T5 1B FT, and mixed in T5 4B FT (a classical pāda 1 in v2 against v1's apt pāda 4). It was worse in Nandi FT, MDLM 120M FT, T5 4B 48k (off-topic) and MDLM 523M FT (more fluent but inverted). DiffusionGemma FT was gibberish in both.
- On base models v2 often loops (Gemma-4 26B, Gemma-4 E4B, T5 270M, MDLM 523M), which matches the rise in repeated lines in the 100-prompt table.

One prompt is an anecdote, not an estimate. The patterns above are leads to check on the 100 prompts, not results.

## Gold

```
భువిలో నిక్కలిదోషహేతుకమునం బొల్పారి గోసంగులున్
బవినాలున్బలుమోటకాఁపుదొరలుం బాషాండులు న్దాసరుల్
సివసత్తుల్ నెఱబోయపెద్దలును దాసేయుప్రభుల్ దుష్టకా
కవులు న్మీఱిరిఁకేమి చెప్పనగు భర్గా పార్వతీవల్లభా
```

*Scorer:* in metre no · skill 1.00 · real words 50% · one-akshara 0% · copy 6% · recognised yes · repeated line no · gold run 80

*Non-words (8):* నిక్కలిదోషహేతుకమునం · బవినాలున్బలుమోటకాపుదొరలుం · బాషాండులు · న్దాసరుల్ · సివసత్తుల్ · దాసేయుప్రభుల్ · దుష్టకా · న్మీఱిరికేమి

*Reading:* A sound mattebhavikrīḍitamu: every pāda on the pattern, prāsa on వ (భువి / బవి / సివ / కవు), the groups listed in the bhāvam's order, the question (ఇఁకేమి చెప్పనగు) and the addressee (భర్గా పార్వతీవల్లభా). **Two scorer errors.** (1) *Not in metre* is a reader artefact. Kūcimañci writes the drutam detached (బాషాండులు న్దాసరుల్, కవులు న్మీఱిరి), and the strict gaṇa reader does not let the conjunct opening the next written word make లు guru, so pādas 2 and 4 read I where U is due. The relaxed reader and the record's own prāsa/yati flags pass it. (2) *Real words 50%*: all 8 "non-words" are real. They are sandhi chains (నిక్కలిదోషహేతుకమునం, బవినాలున్బలుమోటకాపుదొరలుం), the detached drutam (న్దాసరుల్, న్మీఱిరికేమి), a word split across pādas (దుష్టకా|కవులు), a dialect spelling (సివసత్తుల్) and lexicon gaps (బాషాండులు).

## Nandi-Mini-150M · base · free

```
పుట్టిన రోజు పౌర్ణమి; లౌకికమైన ఆలోచనలను జీర్ణించుకోలేక, తృప్తిగా ఉంటున్న ఒక యువకుడు. చదువుతున్నప్పుడు ఆయన చదివే మద్రాసు, వికారాబాద్, నెల్లూరు, చెన్నై, నెల్లూరులోని అన్ని ప్రదేశాల నుండి కొందరు గురువులు, గురువులు, గురువులు లకు మించి ఉన్నవారు. ఆయన చదువుతున్నా, గురువుల చదువుని మద్రాసు, నెల్లూరు, చెన్నై, నెల్లూరులోని గురువులకి మించి ఎక్కువ మంది గురువులు చదివారు. వారిలో చాలా మంది గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా, గుర
```

*Scorer:* in metre no · skill -2.31 · real words 78% · one-akshara 0% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (22):* వికారాబాద్ · చదువుతున్నా · గురువులకి · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా · గురువులకి · చదువుతున్నా

*Reading:* Prose about a young man and his gurus that falls into a loop (గురువులకి మించి ఎక్కువ మంది గురువులు చదువుతున్నా ×12). Unrelated to the bhāvam. The scorer gives it 78% real words, though the flagged forms (చదువుతున్నా, గురువులకి, వికారాబాద్) are real colloquial words, so it is really ≈ 100%. *Repeated line: no*, because the loop sits inside a single line.

## Nandi-Mini-150M · base · constrained v1

```
ఇవి సుజ్యన్మహముల్ని పోలి యిచడేల్య్ర్యిన్లూ మృణానామిగా
స్వవినాభ్యమ్రినులూ మృణానములుగా మ్వంగుల్య రిన్తివ్యనూ
పవినాభ్యమ్రినులూ మృణానములుగా మ్వంగుల్య రిన్తివ్యనూ
అవి దన్కమ్ములకూ మృణానములకుమ్వ్గ్యన్లుమ్వ్గ్యనూ సజ్దనమ్
```

*Scorer:* in metre yes · skill 1.00 · real words 29% · one-akshara 0% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (12):* సుజ్యన్మహముల్ని · యిచడేల్య్ర్యిన్లూ · మృణానామిగా · స్వవినాభ్యమ్రినులూ · మ్వంగుల్య · రిన్తివ్యనూ · పవినాభ్యమ్రినులూ · మ్వంగుల్య · రిన్తివ్యనూ · దన్కమ్ములకూ · మృణానములకుమ్వ్గ్యన్లుమ్వ్గ్యనూ · సజ్దనమ్

*Reading:* Gibberish: only ఇవి, పోలి and అవి are words. Pādas 2 and 3 are the same line except for the first akshara (స్వ / ప). Copying a line and changing its first akshara keeps gaṇa and prāsa for free, and the exact-match repeated-line check misses it.

## Nandi-Mini-150M · base · constrained v2 A+B

```
ఇవి మత్తెఱ్వజలో పదమ్ముల మృణామృత్యమ్సుకట్టుక్రశం
కెవడల్ మన్మథుడుం యతిథ్యముదొదగ్రీపర్ సుగమ్మర్యురీ
స్వవశమ్మర్యురి సుగ్మముచ్యుదురముల్పణ్యుర్వదమ్లుగ్మరీ
అవరభ్యాధినముక్వినమ్లుగరముభ్యాధిన్మలమ్లుగ్మరీ
```

*Scorer:* in metre yes · skill 1.00 · real words 18% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (9):* మత్తెఱ్వజలో · మృణామృత్యమ్సుకట్టుక్రశం · కెవడల్ · మన్మథుడుం · యతిథ్యముదొదగ్రీపర్ · సుగమ్మర్యురీ · స్వవశమ్మర్యురి · సుగ్మముచ్యుదురముల్పణ్యుర్వదమ్లుగ్మరీ · అవరభ్యాధినముక్వినమ్లుగరముభ్యాధిన్మలమ్లుగ్మరీ

*Reading:* Gibberish with a few real words (పదమ్ముల, మన్మథుడుం, స్వవశ…). Nothing of the bhāvam. **Recognised: yes is a false positive.**

## Nandi-Mini-150M · FT (bhāvam → poem) · free

```
కలిశీఘ్రంబె గళంకముల్ బెరుగ దుష్కర్షంబులౌ గోసఁగుల్
పవినంబుల్ మరమేనిమోటకలు ప్రాప్పాషాండులున్ దాసరుల్
శివసత్తుల్ మతిమారపెద్దలును దాసీశక్తులున్ వర్తిల్లు దు
ష్కవులున్ వేరొగి విస్తరింతురు గదా గౌరీశ నేఁ జెప్పుదున్
```

*Scorer:* in metre no · skill 0.93 · real words 53% · one-akshara 10% · copy 0% · recognised yes · repeated line no · gold run 5

*Non-words (9):* దుష్కర్షంబులౌ · గోసగుల్ · పవినంబుల్ · మరమేనిమోటకలు · ప్రాప్పాషాండులున్ · దాసరుల్ · శివసత్తుల్ · ష్కవులున్ · వేరొగి

*Reading:* Very close to the gold in structure and diction. The groups come in order (గోసఁగుల్, పవినంబుల్, …మోట…, పాషాండులున్, దాసరుల్, శివసత్తుల్, మతిమార పెద్దలు), దుష్కవులు is split across pādas as in the gold, and the vocative is గౌరీశ. Flaws: కలిశీఘ్రంబె, దుష్కర్షంబులౌ and మరమేనిమోటకలు are not words, and the close is "నేఁ జెప్పుదున్" (I shall tell) instead of "how can I tell". Skill 0.93: one or two syllables off. Real words (53%) is underrated, since గోసగుల్, దాసరుల్, శివసత్తుల్ and ష్కవులున్ (the pāda-split half) are fine.

## Nandi-Mini-150M · FT (bhāvam → poem) · constrained v1

```
కలినాఁటన్ గలుషంబు పెచ్చరిలుటన్ గాసంగునిల్ పూతులున్
మెలఁతల్ గాక వివేకహీనముఖదోనిక్షిప్లు పాషాండులున్
దలవర్లున్ హరసత్తులున్ మఱుపు పెద్దల్ బానిసల్ రాజు కా
దిలకున్ దుర్గమకవ్లకుల్ నుడియ నేర్తే గౌరి నాథాత్మకా
```

*Scorer:* in metre yes · skill 1.00 · real words 52% · one-akshara 5% · copy 0% · recognised yes · repeated line no · gold run 2

*Non-words (10):* పెచ్చరిలుటన్ · గాసంగునిల్ · పూతులున్ · వివేకహీనముఖదోనిక్షిప్లు · పాషాండులున్ · దలవర్లున్ · హరసత్తులున్ · దుర్గమకవ్లకుల్ · నేర్తే · నాథాత్మకా

*Reading:* Follows the bhāvam item by item. It has కలి, కలుషంబు పెచ్చరిలుట (≈ పెచ్చరిల్లుట, sin swelling), గాసంగు (for గోసంగు), వివేకహీన, పాషాండులున్, హరసత్తులున్ (a fair stand-in for శివసత్తులు), మఱుపు పెద్దల్, బానిసల్ and దుష్కవుల as దుర్గమకవ్లకుల్. It closes with the question (నుడియ నేర్తే, can I speak of it?) and the right addressee (గౌరి నాథ). Broken forms: గాసంగునిల్, …ముఖదోనిక్షిప్లు, దుర్గమకవ్లకుల్, నాథాత్మకా. The scorer's 52% and recognised are fair.

## Nandi-Mini-150M · FT (bhāvam → poem) · constrained v2 A+B

```
కలినీల్గంగను బాపముల్ పెరుగ గోకల్వాపవిన్యక్తకే
పులకంబుల్ దొరపాషడుల్ దసరు లప్పుల్గేవలున్ సత్తముల్
మలినంబౌ పెనుమాయ లేశ కఱవమ్మల్ బెద్దలున్ బానిసల్
చెలఁగన్ నీతరు లంటు విస్తరిలె గోష్ఠీభర్త శర్వాణిపా
```

*Scorer:* in metre yes · skill 1.00 · real words 67% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (7):* కలినీల్గంగను · గోకల్వాపవిన్యక్తకే · పులకంబుల్ · దొరపాషడుల్ · లప్పుల్గేవలున్ · నీతరు · శర్వాణిపా

*Reading:* Pāda 1 is fine (బాపముల్ పెరుగ). After that, real words appear in the wrong sense: పులకంబుల్ (horripilation), సత్తముల్, పెనుమాయ. Pādas 3–4 drift. The addressee is attempted (శర్వాణిపా ≈ శర్వాణీపతీ, a good choice), but the question is lost. Real words rise from 52% to 67% while the sense is weaker than v1, so **more valid words did not mean a closer poem here.**

## Gemma-4 E4B-it · base · free

```
కలియుగపు లోకాన దైవమా నీ రూపం ఎంతటి దివ్యమా
పాపపు చీకటిలోన పడిపోయిన మానవుల హేళనల మాధుర్యమా
వివేకం లేని వీరుల వలన విలసించే ఈ జగతిని ఎలా వర్ణించగలను
ఓ భార్గవ! నీ శాంతితో ఈ భ్రమలన్నిటిని తొలగించవా దయతో
```

*Scorer:* in metre no · skill 0.01 · real words 88% · one-akshara 17% · copy 20% · recognised yes · repeated line no · gold run 1

*Non-words (3):* దివ్యమా · మాధుర్యమా · విలసించే

*Reading:* Modern Telugu free verse addressed to దైవమా / ఓ భార్గవ. It keeps only the frame of the bhāvam (Kali age, sin, people without discretion, the copied "ఎలా వర్ణించగలను") and drops the list of groups, which is the poem's substance. "హేళనల మాధుర్యమా" makes no sense. It is not verse. All three "non-words" (దివ్యమా, మాధుర్యమా, విలసించే) are real, and copy 20% is right.

## Gemma-4 E4B-it · base · constrained v1

```
భగవత్కృత్యము నై శివశ్రవణమున్ త్వంభార్గవః ఝ్యప్యతే
అగమవ్యన్యథ విచ్యతే పతనమర్ధ్ర్యత్యాం వ్రజిత్యేతయే
విగతిల్యాన్ పృథురాంసమున్ విహరితిన్ న్వేనై త్వమవ్రేతయే
పగమిత్యే విధియే న సంధ్య్యత త్వమహ్య్య్వైకేశవః ఝ్యప్యతే
```

*Scorer:* in metre yes · skill 1.00 · real words 11% · one-akshara 10% · copy 0% · recognised no · repeated line no · gold run 0

*Non-words (16):* శివశ్రవణమున్ · త్వంభార్గవః · ఝ్యప్యతే · అగమవ్యన్యథ · విచ్యతే · పతనమర్ధ్ర్యత్యాం · వ్రజిత్యేతయే · విగతిల్యాన్ · పృథురాంసమున్ · విహరితిన్ · న్వేనై · త్వమవ్రేతయే · పగమిత్యే · సంధ్య్యత · త్వమహ్య్య్వైకేశవః · ఝ్యప్యతే

*Reading:* Sanskrit-looking pseudo-words (త్వంభార్గవః, ఝ్యప్యతే, విచ్యతే, వ్రజిత్యేతయే); only భార్గవ ties it to the prompt. The scorer is right (11%, not recognised). Syllables like ఝ్య and ర్ధ్ర్య are what Layer A removes.

## Gemma-4 E4B-it · base · constrained v2 A+B

```
భగవాన్ శివ్వర భక్తినిల్యుని నిలుప్యమ్మా త్వరిత్రాణిహిం
కృగమించున్రియెనక్రియేన నవనియ్యెన్యుం త్వరిత్రాణిహిం
కృగమించున్రియెనక్రియేన నవనియ్యెన్యుం త్వరిత్రాణిహిం
భగవాన్ శివ్వర భక్తినిల్యుని నిలుప్యమ్మా త్వరిత్రాణిహిం
```

*Scorer:* in metre yes · skill 1.00 · real words 25% · one-akshara 0% · copy 0% · recognised no · repeated line yes · gold run 1

*Non-words (12):* శివ్వర · నిలుప్యమ్మా · త్వరిత్రాణిహిం · కృగమించున్రియెనక్రియేన · నవనియ్యెన్యుం · త్వరిత్రాణిహిం · కృగమించున్రియెనక్రియేన · నవనియ్యెన్యుం · త్వరిత్రాణిహిం · శివ్వర · నిలుప్యమ్మా · త్వరిత్రాణిహిం

*Reading:* Two gibberish lines, each used twice (pāda 1 = pāda 4, pāda 2 = pāda 3). Layer A cleaned the syllables, but the model loops. *Repeated line: yes*, correctly.

## Gemma-4 26B-A4B-it · base · free

```
కలియుగమున పాపము పెరిగిపోవుచున్నది చూడగా
బలియుగమున భీకర పాషాండులు పదిలము లేక
మలియుగమున మతిమరుపు పెద్దల మందలందు
నలియుగమున నరకము నడుమనే నరులందు!
```

*Scorer:* in metre no · skill -0.11 · real words 94% · one-akshara 0% · copy 12% · recognised yes · repeated line no · gold run 3

*Non-words (1):* పాషాండులు

*Reading:* Four lines that invent a rhyme: కలియుగమున / బలియుగమున / మలియుగమున / నలియుగమున. This imitates prāsa (లి in every second place) with made-up words. The content is partial (sin growing, pāṣaṇḍas, forgetful elders, hell among men), and the metre is free. **Real words 94% is a false positive:** the matcher accepts బలియుగమున, మలియుగమున and నలియుగమున, presumably as బలి/మలి/నలి + యుగమున.

## Gemma-4 26B-A4B-it · base · constrained v1

```
కలియుగ్యమ్యము పాపముల్ పెరిగిపోవ్వ్వ్గన్ వ్రిత్యునౌ స్త్రీలముల్
నలిగియ్రే గొసగుల్రు పవ్రిలలతల్ గైవొక్రు మూర్ఖుల్ దొరల్
విలుగెడ్రుడ్రు శివస్రులువ్రిత మతిమ్ర్మ్లెడ్రుల్ వృడెడ్రుల్ మతిమ్
వలిగెడ్రుల్ ప్రభువుల్ వ్రితక్రత కవిన్ వ్రత్యాన్ వ్రితాన్ వ్రణ్యునౌ
```

*Scorer:* in metre yes · skill 1.00 · real words 26% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (17):* పెరిగిపోవ్వ్వ్గన్ · వ్రిత్యునౌ · స్త్రీలముల్ · నలిగియ్రే · గొసగుల్రు · పవ్రిలలతల్ · గైవొక్రు · విలుగెడ్రుడ్రు · శివస్రులువ్రిత · మతిమ్ర్మ్లెడ్రుల్ · వృడెడ్రుల్ · మతిమ్ · వలిగెడ్రుల్ · వ్రితక్రత · వ్రత్యాన్ · వ్రితాన్ · వ్రణ్యునౌ

*Reading:* The prompt's words mangled into non-words (పెరిగిపోవ్వ్వ్గన్, గొసగుల్రు, మతిమ్ర్మ్లెడ్రుల్, వ్రితక్రత). Recognised: yes comes from fragments (కలియుగ…, పాపముల్, మూర్ఖుల్ దొరల్, ప్రభువుల్, కవిన్), so it is borderline. Real words 26% is fair.

## Gemma-4 26B-A4B-it · base · constrained v2 A+B

```
కలియుగ్యమ్యము పాపముల్ పెరిగి పోర్గా నిర్యుపాయంబు లే
కలియుగ్యమ్యము పాపముల్ పెరిగి పోర్గా నిర్యుపాయంబు లే
కలియుగ్యమ్యము పాపముల్ పెరిగి పోర్గా నిర్యుపాయంబు లే
కలియుగ్యమ్యము పాపముల్ పెరిగి పోర్గా నిర్యుపాయంబు లే
```

*Scorer:* in metre yes · skill 1.00 · real words 60% · one-akshara 17% · copy 0% · recognised yes · repeated line yes · gold run 1

*Non-words (8):* పోర్గా · నిర్యుపాయంబు · పోర్గా · నిర్యుపాయంబు · పోర్గా · నిర్యుపాయంబు · పోర్గా · నిర్యుపాయంబు

*Reading:* **One line repeated four times** (కలియుగ్యమ్యము పాపముల్ పెరిగి పోర్గా నిర్యుపాయంబు లే). The scorer gives 60% real words (up from 26% in v1), recognised and in metre, because repetition satisfies prāsa trivially. Only the repeated-line flag catches it. This is one way v2's real-words gain on base models can come from looping.

## T5Gemma 2 270M · base · free

```
<bAvanapatha (పద్యం)</b
<bĀyūdhāna (యాష్టా)</b
<bAṇḍuṣṭhā (వాస్తవం)</b
<bAśvāyā (కూర్పు)</b
```

*Scorer:* in metre no · skill -1.63 · real words 75% · one-akshara 0% · copy 0% · recognised no · repeated line no · gold run 0

*Non-words (1):* యాష్టా

*Reading:* HTML-like fragments with romanised pseudo-words and Telugu glosses in parentheses. It is not a poem. 75% real words is computed over only four Telugu words.

## T5Gemma 2 270M · base · constrained v1

```
మరియుక్రీడితముబ్రిమారినము లింగ్వస్మక్రియాయిస్ పఠా
సరిదా హవ్రి పఠాకరీతముబృకృశ్మక్రియ్రియాయిస్ పఠా
చరిదా హవ్రి పఠాకరీతముబృకృశ్మక్రియ్రియాయిస్ పఠా
భరిదా హవ్రి పఠాకరీతముడిపవ్వర్గమ్రియాయిస్ మకృశ్
```

*Scorer:* in metre yes · skill 1.00 · real words 0% · one-akshara 0% · copy 0% · recognised no · repeated line no · gold run 0

*Non-words (15):* మరియుక్రీడితముబ్రిమారినము · లింగ్వస్మక్రియాయిస్ · పఠా · సరిదా · హవ్రి · పఠాకరీతముబృకృశ్మక్రియ్రియాయిస్ · పఠా · చరిదా · హవ్రి · పఠాకరీతముబృకృశ్మక్రియ్రియాయిస్ · పఠా · భరిదా · హవ్రి · పఠాకరీతముడిపవ్వర్గమ్రియాయిస్ · మకృశ్

*Reading:* Gibberish, 0% real words, which is correct. Pādas 2 and 3 are the same line apart from the first akshara (సరిదా / చరిదా), and pāda 4 shares its first half (భరిదా హవ్రి పఠాకరీత…). This is the same copy-and-change-one-akshara trick, and *repeated line: no* misses it.

## T5Gemma 2 270M · base · constrained v2 A+B

```
మరియున్ మిగ్వయలక్ష్మినుండి మరణం ఖ్యాతిగ్రియే మృత్యువల్
మరియున్ మిగ్వయలక్ష్మినుండి మరణం ఖ్యాతిగ్రియే మృత్యువల్
అరణియ్మర్ముడివుండికివ్రతువుడుమ్యా పద్మశీలాకు కీ
మరియున్ మిగ్వయలక్ష్మినుండి మరణం ఖ్యాతిగ్రియే మృత్యువల్
```

*Scorer:* in metre yes · skill 1.00 · real words 35% · one-akshara 6% · copy 0% · recognised no · repeated line yes · gold run 1

*Non-words (11):* మిగ్వయలక్ష్మినుండి · ఖ్యాతిగ్రియే · మృత్యువల్ · మిగ్వయలక్ష్మినుండి · ఖ్యాతిగ్రియే · మృత్యువల్ · అరణియ్మర్ముడివుండికివ్రతువుడుమ్యా · పద్మశీలాకు · మిగ్వయలక్ష్మినుండి · ఖ్యాతిగ్రియే · మృత్యువల్

*Reading:* Pādas 1, 2 and 4 are identical (మరియున్ మిగ్వయలక్ష్మినుండి మరణం ఖ్యాతిగ్రియే మృత్యువల్), half words and half fragments, and unrelated to the bhāvam. *Repeated line: yes*, correctly.

## T5Gemma 2 270M · FT (full) · free

```
కలియుగంబున బాపముల్ పెరిగి గోసంగుల్ పవానల్ వివే
కలభంబైన మొలంతలాదిరలు పాషాండుల్ విదాసారులున్
మలినాక్షుల్ మతిమర్దనుల్ పతియు దుర్మార్గంబులం బొల్చుచున్
జెలగంజెల్లుదు రిందులో గలదె యే జెప్పంగ నే నేర్తునే
```

*Scorer:* in metre no · skill 0.96 · real words 60% · one-akshara 9% · copy 0% · recognised yes · repeated line no · gold run 2

*Non-words (8):* గోసంగుల్ · పవానల్ · కలభంబైన · మొలంతలాదిరలు · పాషాండుల్ · మలినాక్షుల్ · జెలగంజెల్లుదు · రిందులో

*Reading:* Tracks the bhāvam: కలియుగంబున బాపముల్ పెరిగి గోసంగుల్ పవానల్, then పాషాండుల్, దుర్మార్గంబులం బొల్చుచున్, and it ends on the question (…గలదె యే జెప్పంగ నే నేర్తునే). There is no addressee. Skill 0.96: near-metrical. Several flagged words are real (గోసంగుల్, పాషాండుల్, మలినాక్షుల్, and (చెల్లుదు)రిందులో, which is a sandhi form).

## T5Gemma 2 270M · FT (full) · constrained v1

```
కలియుం గిల్లిక లగ్గలించ పవినూకల్ బట్టపుంబొట్టులున్
మొలకల్ తమ్ములు దాసరుల్ శివసముల్ మూర్ధావిభాగంబులున్
చెలియల్ గండలు వట్టి చెడ్డకవు లచ్చెల్వార వర్తింతు రీ
యెలుగెట్లున్నయెడం గలంక గలవా డృశ్యాంబుజాక్షీమణీ
```

*Scorer:* in metre yes · skill 1.00 · real words 60% · one-akshara 5% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (8):* కలియుం · గిల్లిక · పవినూకల్ · బట్టపుంబొట్టులున్ · దాసరుల్ · లచ్చెల్వార · యెలుగెట్లున్నయెడం · డృశ్యాంబుజాక్షీమణీ

*Reading:* Mostly real words, but pādas 1–2 are a word salad (గిల్లిక, పవినూకల్, బట్టపుంబొట్టులున్, మొలకల్ తమ్ములు). Pāda 3 is good: వట్టి చెడ్డకవు లచ్చెల్వార వర్తింతు రీ (worthless bad poets thrive). It addresses అంబుజాక్షీమణీ (a lotus-eyed lady), **the wrong addressee**. Real words 60% and recognised overrate its coherence.

## T5Gemma 2 270M · FT (full) · constrained v2 A+B

```
కలియుగ్యంబున బాపముల్ పెరుగగా గల్పాంతముల్ వానితో
బలుకుల్ గానివివేకరాని మరుదుప్రాలున్ సుపాషాండుతో
జలముల్ దాసరుతో శివార్భటులతో సంభావితుల్ వానితో
గెలుచున్ దుష్కవులొండొరుల్ గలయ నేగెన్ వీరి నన్నేలనో
```

*Scorer:* in metre yes · skill 1.00 · real words 60% · one-akshara 0% · copy 5% · recognised yes · repeated line no · gold run 1

*Non-words (8):* కలియుగ్యంబున · గల్పాంతముల్ · మరుదుప్రాలున్ · సుపాషాండుతో · దాసరుతో · శివార్భటులతో · సంభావితుల్ · దుష్కవులొండొరుల్

*Reading:* The most padyam-like poem in this row. It runs కలియుగ(్య)ంబున బాపముల్ పెరుగగా …, …సుపాషాండుతో, దాసరుతో, శివార్భటులతో, and దుష్కవులొండొరుల్ గలయ (bad poets mingling with one another). The close వీరి నన్నేలనో loosely carries the question. Errors: కలియుగ్యంబున, మరుదుప్రాలున్, శివార్భటులతో. The non-word list includes real forms: గల్పాంతముల్ (కల్పాంతముల్ after gasaḍadavādeśa), దాసరుతో, దుష్కవులొండొరుల్ (a sandhi compound) and సంభావితుల్. Real words 60% is an undercount.

## T5Gemma 2 1B · base · free

```
ఇప్పుడు ఈ సముద్రంలో, ఈ ఖండంలో, ఈ పసుపునాడులో, ఈ వసంతపునాడులో, ఈ మరణపునాడులో, ఈ ఇంద్రపునాడులో, ఈ నక్షత్రపునాడులో, ఈ మహాపునాడులో, ఈ ఆనందపునాడులో, ఈ సత్యపునాడులో, ఈ స్వర్ణపునాడులో, ఈ ఆంజనేయుపునాడులో, ఈ బ్రహ్మపునాడులో, ఈ ముక్తిపునాడులో, ఈ మంత్రపునాడులో, ఈ పుణ్యపునాడులో, ఈ ఆనందపునాడులో, ఈ ప్రశస్తపునాడులో, ఈ ఆత్మపునాడులో, ఈ ఈవనిపునాడులో, ఈ సప్తపునాడులో, ఈ పురుష్కపునాడులో, ఈ ప్రవక్తపునాడులో, ఈ ప్రసిద్ధపునాడులో, ఈ ప్రవక్తపునాడులో, ఈ పురుష్కపునాడులో
```

*Scorer:* in metre no · skill -2.58 · real words 11% · one-akshara 49% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (24):* పసుపునాడులో · వసంతపునాడులో · మరణపునాడులో · ఇంద్రపునాడులో · నక్షత్రపునాడులో · మహాపునాడులో · ఆనందపునాడులో · సత్యపునాడులో · స్వర్ణపునాడులో · ఆంజనేయుపునాడులో · బ్రహ్మపునాడులో · ముక్తిపునాడులో · మంత్రపునాడులో · పుణ్యపునాడులో · ఆనందపునాడులో · ప్రశస్తపునాడులో · ఆత్మపునాడులో · ఈవనిపునాడులో · సప్తపునాడులో · పురుష్కపునాడులో · ప్రవక్తపునాడులో · ప్రసిద్ధపునాడులో · ప్రవక్తపునాడులో · పురుష్కపునాడులో

*Reading:* A loop of invented compounds (ఈ …పునాడులో ×26). The one-akshara measure (49%, the repeated ఈ) catches it, and real words is 11%.

## T5Gemma 2 1B · base · constrained v1

```
సకలంగా పెరిగింటె పాపములు చూసారూ చురుగ్గా పరా
ధృ కనబ్రిన్రు పులజ్మ గీగన నమస్తే మెచ్చినజ్మగ్రజన్
చొకసారూ నమశేషమంటగమతమ్య్మ్జోగ్రజ్మతమ్యమ్య్మగమ్
చొకసారూ నమశేషమంటగమతమ్య్మ్జోగ్రజ్మతమ్య్మ్యగ్య్మగమ్
```

*Scorer:* in metre yes · skill 1.00 · real words 53% · one-akshara 6% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (7):* చూసారూ · కనబ్రిన్రు · పులజ్మ · గీగన · మెచ్చినజ్మగ్రజన్ · నమశేషమంటగమతమ్య్మ్జోగ్రజ్మతమ్యమ్య్మగమ్ · నమశేషమంటగమతమ్య్మ్జోగ్రజ్మతమ్య్మ్యగ్య్మగమ్

*Reading:* Pādas 1–2 are half Telugu (పెరిగింటె పాపములు చూసారూ చురుగ్గా … నమస్తే మెచ్చిన…), and pādas 3–4 are gibberish and nearly identical (only the last aksharas differ), which the repeated-line check misses. **Real words 53% and recognised are overrated.** Short real words (సకలంగా, పాపములు, నమస్తే) count one each, while each long nonsense string also counts as only one word.

## T5Gemma 2 1B · base · constrained v2 A+B

```
వినవయ్మత్తెననిప్యుమత్తెననిపవ్యే నమ్రతన్మృప్యుమత్
నిని శోభా యితరమ్యుమత్నమృపవస్యే నమ్రతన్మృప్యుమత్
సొన వ్రాతం శ్మశకృత్రి శ్మశ్మశకరేషుమ్యుమ్యుమత్నమ్యుమత్
వినివచ్చోభసనమ్యుమత్నమృపకృత్విప్యుమ్యుమత్నమ్యుమత్
```

*Scorer:* in metre yes · skill 1.00 · real words 36% · one-akshara 0% · copy 0% · recognised no · repeated line no · gold run 0

*Non-words (7):* వినవయ్మత్తెననిప్యుమత్తెననిపవ్యే · నమ్రతన్మృప్యుమత్ · యితరమ్యుమత్నమృపవస్యే · నమ్రతన్మృప్యుమత్ · శ్మశకృత్రి · శ్మశ్మశకరేషుమ్యుమ్యుమత్నమ్యుమత్ · వినివచ్చోభసనమ్యుమత్నమృపకృత్విప్యుమ్యుమత్నమ్యుమత్

*Reading:* Gibberish ending in a …మ్యుమత్ loop. Real words 36% comes from four short fragments (నిని, శోభా, సొన, వ్రాతం) against seven long non-words. By reading it is ≈ 0%.

## T5Gemma 2 1B · FT (full) · free

```
పొలుపారన్ గలికాలమందు గలుషంబుల్ వృద్ధి నొందన్ జని
నలు గోసంగులు నొండు పవ్వళులు నానావేద్యమోటంచెలున్
దొలగుం దాసరులున్ శివార్యులును బంధుర్వృద్ధులున్ ధూర్తరా
ష్ట్రులు దుష్కర్వులు బేర్చి రెక్కుడుగ వాక్రువ్వంగ భార్గవ్యమా
```

*Scorer:* in metre no · skill 0.96 · real words 73% · one-akshara 0% · copy 5% · recognised yes · repeated line no · gold run 3

*Non-words (6):* గలుషంబుల్ · నానావేద్యమోటంచెలున్ · శివార్యులును · బంధుర్వృద్ధులున్ · ధూర్తరా · భార్గవ్యమా

*Reading:* Good. It opens పొలుపారన్ గలికాలమందు గలుషంబుల్ వృద్ధి నొందన్ (as Kali's sins grow), lists the groups, and splits ధూర్తరా|ష్ట్రులు across pādas, a classical device the gold also uses. The vocative is garbled (భార్గవ్యమా). Skill 0.96. The scorer flags గలుషంబుల్ (కలుషంబుల్ in sandhi) and the pāda-split ధూర్తరా as non-words, wrongly.

## T5Gemma 2 1B · FT (full) · constrained v1

```
కలుషం బేపడ గోవుసంగులు పవల్ గాంక్షించి యాజాతిగా
కలుషం బేమి వివేకహీనవసుధాఖ్యాకస్థితారావముల్
కలుషం బేమిశివాళియున్ మఱపినన్ గర్హించి బానిస్రముల్
కలుషానాథులు దుష్కవుల్ కవులు వర్ధ్లాంభోధిభార్గూద్వహా
```

*Scorer:* in metre yes · skill 1.00 · real words 56% · one-akshara 0% · copy 6% · recognised yes · repeated line no · gold run 3

*Non-words (8):* బేపడ · యాజాతిగా · వివేకహీనవసుధాఖ్యాకస్థితారావముల్ · బేమిశివాళియున్ · మఱపినన్ · బానిస్రముల్ · కలుషానాథులు · వర్ధ్లాంభోధిభార్గూద్వహా

*Reading:* Anaphora on కలుషం బే… in pādas 1–3. It reads as a device, but the sense is thin. Part of the list survives (వివేకహీన, శివాళి, మఱపి, బానిస…, దుష్కవుల్), and the vocative is garbled (…భార్గూద్వహా). Real words 56% and recognised are fair.

## T5Gemma 2 1B · FT (full) · constrained v2 A+B

```
కలుషం బేపున గోవులం బవనముల్ కౌశేయ వాచంయముల్
కలుషం బేమియు మోటకాపుదొరలుం గైదుష్యదాసారులున్
కలుషం బేమియు శంభు సౌభ్రవులు బ్రఖ్యాతాధిపుల్ దుష్కవుల్
కలియుగ్యంబున నిట్టు లున్న తెఱ గెట్లన్ మాతృభూతాధిపా
```

*Scorer:* in metre yes · skill 1.00 · real words 77% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (5):* గైదుష్యదాసారులున్ · సౌభ్రవులు · బ్రఖ్యాతాధిపుల్ · కలియుగ్యంబున · గెట్లన్

*Reading:* The same anaphora, with two good pādas. Pāda 2 has the prompt's exact term (మోటకాపుదొరలుం). Pāda 4, కలియుగ్యంబున నిట్టు లున్న తెఱ గెట్లన్ మాతృభూతాధిపా, is the prompt's question (how [to tell] the state that is thus in the Kali age) addressed by an apt Śiva epithet (lord of the Mātṛs and Bhūtas). Some real words are used in the wrong sense and still count fully: గోవులం (cows, for గోసంగులు), కౌశేయ (silk), వాచంయముల్ (silent sages). Real words 77% fits the words; the sense is about half there.

## T5Gemma 2 4B · base · free

```
సారాంశం: క్రీ.శ. 10వ శతాబ్దంలో ప్రాచీన భాషలో రచించిన పద్యం.
```

*Scorer:* in metre no · skill -1.56 · real words 86% · one-akshara 12% · copy 0% · recognised no · repeated line no · gold run 0

*Non-words (1):* శతాబ్దంలో

*Reading:* One line of prose metadata (సారాంశం: క్రీ.శ. 10వ శతాబ్దంలో ప్రాచీన భాషలో రచించిన పద్యం.). Not a poem. Real words 86%.

## T5Gemma 2 4B · base · constrained v1

```
విచరించేటపుడుమ్రొనిప్యముగుచేయ్య్వేషంబు నన్వయ్యమన్
భెచినాడెమ్యునగువ్వనల్యముగెవన్వ్యెద్యావధాస్యమ్ముణో
త్వొచనమ్యుచ్యుచినాదమధ్యవదిమధ్య్వుచ్యుచ్యుచీత్యావధా
త్వొచనమ్యుచ్యుచినాదమధ్యవదిమధ్య్వుచ్యుచ్యుచీత్యావధా
```

*Scorer:* in metre yes · skill 1.00 · real words 0% · one-akshara 0% · copy 0% · recognised no · repeated line yes · gold run 0

*Non-words (5):* విచరించేటపుడుమ్రొనిప్యముగుచేయ్య్వేషంబు · నన్వయ్యమన్ · భెచినాడెమ్యునగువ్వనల్యముగెవన్వ్యెద్యావధాస్యమ్ముణో · త్వొచనమ్యుచ్యుచినాదమధ్యవదిమధ్య్వుచ్యుచ్యుచీత్యావధా · త్వొచనమ్యుచ్యుచినాదమధ్యవదిమధ్య్వుచ్యుచ్యుచీత్యావధా

*Reading:* Pure gibberish, and pādas 3 and 4 are identical. The scorer is right (0%, not recognised, repeated).

## T5Gemma 2 4B · base · constrained v2 A+B

```
మనిషిగ్రాహకుడుగ్రమిన్యబభృశం ధ్యానమ్యవధ్వేజవిం
భినవాహభ్రతుకబ్యుజభ్రగులపప్రేహభ్రతుక్రీడచా
భ్రునతృధ్వజ్వగభజ్వభగ్వరభృశభ్రున్రత్రియభ్రగ్వగై
భ్రునతృధ్వజ్వగభజ్వభగ్వరభృశభ్రున్రత్రియభ్రగ్వగై
```

*Scorer:* in metre yes · skill 1.00 · real words 0% · one-akshara 0% · copy 0% · recognised no · repeated line yes · gold run 1

*Non-words (5):* మనిషిగ్రాహకుడుగ్రమిన్యబభృశం · ధ్యానమ్యవధ్వేజవిం · భినవాహభ్రతుకబ్యుజభ్రగులపప్రేహభ్రతుక్రీడచా · భ్రునతృధ్వజ్వగభజ్వభగ్వరభృశభ్రున్రత్రియభ్రగ్వగై · భ్రునతృధ్వజ్వగభజ్వభగ్వరభృశభ్రున్రత్రియభ్రగ్వగై

*Reading:* Pure gibberish, and pādas 3 and 4 are identical. The scorer is right.

## T5Gemma 2 4B · FT (LoRA r 128) · free

```
కలికాలంబున బాపముల్ పెరుగ గోసంగుల్ పవ ల్విజ్ఞత
ల్గలుగ న్మోటలు పాషణంబులును దాసారంబులు న్మౌనియున్
మలు బానిసల్ చరియించునట్టిదొరలున్ మర్త్యేశ్వరు ల్వీరి యం
తలము న్నేనెటు లీడు పార్వతిపతిం దా నెట్లు వర్ణింతునే
```

*Scorer:* in metre no · skill 0.96 · real words 55% · one-akshara 8% · copy 0% · recognised yes · repeated line no · gold run 2

*Non-words (10):* గోసంగుల్ · ల్విజ్ఞత · ల్గలుగ · న్మోటలు · పాషణంబులును · న్మౌనియున్ · మర్త్యేశ్వరు · ల్వీరి · న్నేనెటు · వర్ణింతునే

*Reading:* A close paraphrase in verse (కలికాలంబున బాపముల్ పెరుగ గోసంగుల్ …). It ends on the prompt's close with the addressee: పార్వతిపతిం దా నెట్లు వర్ణింతునే. Skill 0.96. It writes the drutam detached as Kūcimañci does (పవ ల్విజ్ఞత, ల్గలుగ, న్మోటలు, ల్వీరి), and the matcher rejects every such piece, so real words 55% understates it.

## T5Gemma 2 4B · FT (LoRA r 128) · constrained v1

```
కలికాలంబున గల్మషంబులును గోగంబుల్ పవళ్లీవివే
కలు మోటల్ కడు బాషముల్ పవళు లూకంబుల్ శివాసత్తులున్
మలినాక్షిం గలవారి బానిసలు దుర్మానప్రభుల్ బానిసుల్
విలసిల్లం గలవారి నడ్మిగతి యెట్లెన్నంగ నెంచంగలన్
```

*Scorer:* in metre yes · skill 1.00 · real words 48% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (11):* గోగంబుల్ · పవళ్లీవివే · మోటల్ · బాషముల్ · పవళు · లూకంబుల్ · శివాసత్తులున్ · మలినాక్షిం · బానిసుల్ · నడ్మిగతి · యెట్లెన్నంగ

*Reading:* Pāda 4 is the best single line in the constrained poems: విలసిల్లం గలవారి నడ్మిగతి యెట్లెన్నంగ నెంచంగలన్ (how can I set out to recount the state amid those who flourish), which is the bhāvam's last sentence. Pādas 1–3 list the groups in corrupted forms (గోగంబుల్, పవళ్లీ…, బాషముల్, లూకంబుల్, శివాసత్తులున్). There is no addressee. Real words 48% understates it: మోటల్, బానిసుల్, నడ్మి (≈ నడుమ) and యెట్లెన్నంగ are real or near.

## T5Gemma 2 4B · FT (LoRA r 128) · constrained v2 A+B

```
కలికాలంబున గల్మషంబు లడరం గాసంగులుం బవ్వినల్
వెలయంగా బరమప్రబోధములు లేవిశ్వాసదోషంబులున్
బలుమాఱున్ దురితాత్మజాతములు సర్పంబుల్ సుమాళంబు లౌ
పలుమాఱున్ బరిపూర్ణముల్ విరియ దుర్బంబుల్ వచింపన్ వచః
```

*Scorer:* in metre yes · skill 1.00 · real words 67% · one-akshara 5% · copy 0% · recognised yes · repeated line no · gold run 2

*Non-words (6):* గాసంగులుం · బవ్వినల్ · లేవిశ్వాసదోషంబులున్ · సర్పంబుల్ · బరిపూర్ణముల్ · దుర్బంబుల్

*Reading:* Pāda 1 is classical and apt: కలికాలంబున గల్మషంబు లడరం గాసంగులుం బవ్వినల్ (as sins swell in Kali, the Gāsaṅgis and Pavinas…). Pāda 2 is fine. Pādas 3–4 drift (సర్పంబుల్ snakes, సుమాళంబు, బరిపూర్ణముల్ విరియ) and end in filler (వచింపన్ వచః), with no addressee. The matcher flags real words (సర్పంబుల్, బరిపూర్ణముల్).

## T5Gemma 2 4B · FT (LoRA r 128), first 48k · free

```
అనఘుల్ గల్గి యఘంబు లంచు గలిగినంతేర న్వీక స
ల్మినిపౌవాంఘ్రమున న్వ్యాఘములచే మేల్మేమి మతింప న్నవ
ల్ఘనత ల్బానిస ల్గ న ర్విభువు లొండొ న్వీను లి ట్లౌట న
ట్లని చెప్పెన్ వాడె నా న ట్లకట యె ట్లౌటన్ పార్వతీపతిన్
```

*Scorer:* in metre no · skill 0.67 · real words 65% · one-akshara 26% · copy 0% · recognised yes · repeated line no · gold run 3

*Non-words (8):* ల్మినిపౌవాంఘ్రమున · న్వ్యాఘములచే · మేల్మేమి · ల్ఘనత · ల్బానిస · ర్విభువు · న్వీను · ట్లౌటన్

*Reading:* Fragmented: detached consonants everywhere (…ల్మినిపౌ…, న ర్విభువు, ట్లౌటన్). One-akshara 26% catches it, and it is barely tied to the bhāvam (బానిస, పార్వతీపతిన్). Skill 0.67.

## T5Gemma 2 4B · FT (LoRA r 128), first 48k · constrained v1

```
అనఘుల్ గల్గియు నగ్గియున్ గలిగియున్ నందెన్ సముద్యత్క్రియన్
వనఘల్ పాషకు లింతదాసరులు మౌవా ల్మింపగా జెల్లుచున్
జననాథుల్ చెడుభూతదానవనమొక్య్సంగ్రాహమున్ వెల్విలన్
వినుతించున్ గలిగింప గీడు సతియౌ వీరాకటా సల్పెదన్
```

*Scorer:* in metre yes · skill 1.00 · real words 62% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 0

*Non-words (8):* నగ్గియున్ · వనఘల్ · పాషకు · మౌవా · ల్మింపగా · జెల్లుచున్ · చెడుభూతదానవనమొక్య్సంగ్రాహమున్ · వెల్విలన్

*Reading:* A filler opening (అనఘుల్ గల్గియు నగ్గియున్ గలిగియున్ …), mangled groups (పాషకు, …దాసరులు) and some sense in pāda 3 (జననాథుల్ చెడు…). A weak close (వీరాకటా సల్పెదన్). **Real words 62% and recognised overrate it.**

## T5Gemma 2 4B · FT (LoRA r 128), first 48k · constrained v2 A+B

```
అనఘుం డాహరహంబు నైజమహియై యంచిత్యు లిగ్గల్గినన్
వినిపింపం బవనజ్వలానఘులు నైవేద్యంబు లౌచున్ సదా
దనఘా ల్గణ్యవరుల్ మతిమ్రగుపె పెంతౌ జక్కగన్ నైన నీ
జననాథుం డుదరౌఘు లింక వణికాస్వస్త్రస్వరాళుండ నై
```

*Scorer:* in metre yes · skill 1.00 · real words 50% · one-akshara 9% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (10):* డాహరహంబు · నైజమహియై · యంచిత్యు · లిగ్గల్గినన్ · బవనజ్వలానఘులు · ల్గణ్యవరుల్ · మతిమ్రగుపె · పెంతౌ · డుదరౌఘు · వణికాస్వస్త్రస్వరాళుండ

*Reading:* Off-topic (అనఘుం డాహరహంబు నైజమహియై…), with only జననాథుం and మతి… near the prompt. Not recognised, which is fair.

## chandohasam MDLM 120M · base (pre-trained) · free

```
కవి: మన కవులు ఆ పద్యంలో చెప్పే పాటలకు సామాన్య పరిస్థితి కనిపించదు. అలాంటి వారి గురించి ఎందుకు వర్ణించలేదు? అలాంటి వారిని గురించి ఎన్నో కవితలు వ్రాశాను. ఎన్నో కవితలు వ్రాశాను. ఇలాంటి వారిని గురించి చాలా సార్లు వ్రాశాను. అలాంటి వారు చాలా మంది ఉన్నారు. వారు అలాంటి వారు. అందుకే నేను ప్రజలకు తెలుసు. ప్రజల మధ్య వస్తున్న ప్రేమ, విశ్వాసం, ఆదరణ, సంపద, మర్యాదలు, అనుభవ నిర్వచనం అందులో లేదు. వాటిని పరిగణించడం తప్పు. ప్రజలకు ఎంత సరదాగా ఉంటారో పరిగణిస్తాను. ఇలా చాలా సా
```

*Scorer:* in metre no · skill -2.60 · real words 98% · one-akshara 3% · copy 3% · recognised no · repeated line no · gold run 3

*Non-words (1):* పరిగణిస్తాను

*Reading:* Prose meta-commentary (కవి: మన కవులు ఆ పద్యంలో…) with repeats (ఎన్నో కవితలు వ్రాశాను ×2). 98% real words: the measure rewards prose.

## chandohasam MDLM 120M · base (pre-trained) · constrained v1

```
ఇది అన్నిక్వత కావటట్లు నిలుపబ్ న్వ్వ్వృత్వ్వ్వష్వ్వ్వ వ్యవ్వ్వ్వస్వ్వ్వ వ్యా
క ద యప్వ్వ్వద్వ్వ్వ వృషభ్వ్వ్వ అన్న పదమున్న్వ్కవ్వ్వ్వువ్వ్వ్వ వ్యా కద్వ్వ్వ వ్యా
క ద య్వ్వ్వష్వ్వ్వజ్వ్వ వ్యవహ్వ్వ్వ వ్యా క ఇతరమ్వ్వ్కవ్వ్వ్వజ్వ్వ్వ వ్యా కర్వ్వ్వ వ్యా
క దశమ్వ్వ్వం అని పద్యమందు అభివర్ణ్వ్కం వ్యాకరణ్వ్వ్వస్త వ్యా
```

*Scorer:* in metre yes · skill 1.00 · real words 25% · one-akshara 39% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (15):* అన్నిక్వత · నిలుపబ్ · న్వ్వ్వృత్వ్వ్వష్వ్వ్వ · వ్యవ్వ్వ్వస్వ్వ్వ · యప్వ్వ్వద్వ్వ్వ · వృషభ్వ్వ్వ · పదమున్న్వ్కవ్వ్వ్వువ్వ్వ్వ · కద్వ్వ్వ · య్వ్వ్వష్వ్వ్వజ్వ్వ · వ్యవహ్వ్వ్వ · ఇతరమ్వ్వ్కవ్వ్వ్వజ్వ్వ్వ · కర్వ్వ్వ · దశమ్వ్వ్వం · అభివర్ణ్వ్కం · వ్యాకరణ్వ్వ్వస్త

*Reading:* Gibberish with runs of వ్వ్వ. It passes the metre check: **the strict reader accepts syllables that cannot be written** (triple conjuncts). One-akshara 39% does catch it.

## chandohasam MDLM 120M · base (pre-trained) · constrained v2 A+B

```
ఇది అత్యాదర భావకల్పనకు చాల్ ప్యే కారణమ్చద్వ అం
మదనప్నే సకలశ్వ విల్చత తయా మద్వచ్చతా మద్వచన్
భ్య దయజ్వువ్య పదప్య అవ్వ అన అన్యత్చత్చతస్వన్చతా
తద తర్వ్వత్వ అవయ్వ అవ్వ అవయత్చత్వత్వ అవ్వత్వ అం
```

*Scorer:* in metre yes · skill 1.00 · real words 38% · one-akshara 19% · copy 0% · recognised yes · repeated line no · gold run 1

*Non-words (13):* అత్యాదర · కారణమ్చద్వ · మదనప్నే · విల్చత · మద్వచ్చతా · మద్వచన్ · దయజ్వువ్య · పదప్య · అన్యత్చత్చతస్వన్చతా · తర్వ్వత్వ · అవయ్వ · అవయత్చత్వత్వ · అవ్వత్వ

*Reading:* Layer A removed the impossible clusters, but the poem is still gibberish (only అత్యాదర భావకల్పనకు is real). **Recognised: yes is a false positive.**

## chandohasam MDLM 120M · FT (E6 + T1) · free

```
పవినా లా వివేక మాటలు మహా పాషండులు దాసరుల్
శివసత్తు లను వారు మతిమరుపు పెద్దలు దాసరుల్ బానిస
ల్లవు లై చను వారు నాటి వికవుల్ విస్తారింప వ
న్నెవరే భార్గవ గన్న గబ్బితనము న్నిశాకాశరీ కమున్
```

*Scorer:* in metre no · skill 0.52 · real words 76% · one-akshara 11% · copy 12% · recognised no · repeated line no · gold run 2

*Non-words (6):* పవినా · దాసరుల్ · దాసరుల్ · వికవుల్ · న్నెవరే · న్నిశాకాశరీ

*Reading:* The bhāvam's list rewritten almost word for word into lines (పవినా లా వివేక మాటలు మహా పాషండులు దాసరుల్ / శివసత్తు లను వారు మతిమరుపు పెద్దలు…). Copy is 12%, దాసరుల్ is repeated, and it isn't verse (skill 0.52). **Not recognised is a false negative**: it is the most on-topic free poem after the fine-tuned paraphrases.

## chandohasam MDLM 120M · FT (E6 + T1) · constrained v1

```
అలి గోసంగుల లోలు విస్తరిత మాహర్త్యస్థితివ్వారికల్
అలికాపుట్టని మోటకాపుదొరలున్ నాసక్తులున్ బాసరుల్
మలపుల్ బెద్దలు బానిసన్నలు దురామత్కద్రుజుల్ నేరముల్
విల రాగంబులు కమ్మవారలు గదా వెన్నార్తురాభర్గవా
```

*Scorer:* in metre yes · skill 1.00 · real words 68% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 3

*Non-words (6):* మాహర్త్యస్థితివ్వారికల్ · అలికాపుట్టని · నాసక్తులున్ · బాసరుల్ · దురామత్కద్రుజుల్ · వెన్నార్తురాభర్గవా

*Reading:* Pādas 2–3 list the groups (మోటకాపుదొరలున్, బెద్దలు, బానిసన్నలు). Pāda 4 **adds a community name the bhāvam does not have** (కమ్మవారలు), generalised from మోటకాపు, and the vocative is garbled (వెన్నార్తురాభర్గవా). Real words 68% is fair.

## chandohasam MDLM 120M · FT (E6 + T1) · constrained v2 A+B

```
పవినా మోటక పాషణావళి యనన్ బాషాణ గోసంగులున్
జవనా మోటక పాషడయ్య తలదాసత్తామరుల్మత్తులున్
బవమానమ్మున బంధనాల పతి బాణాగమ్ము కాళిందమున్
బవమానమ్మున మోటు మాస నెలు పంపం జెప్పఁగా భార్గవా
```

*Scorer:* in metre yes · skill 1.00 · real words 64% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 4

*Non-words (8):* పవినా · మోటక · పాషణావళి · జవనా · మోటక · పాషడయ్య · తలదాసత్తామరుల్మత్తులున్ · కాళిందమున్

*Reading:* Repetitive: మోటక appears twice, and బవమానమ్మున opens both pādas 3 and 4. Non-words include పాషణావళి, పాషడయ్య and తలదాసత్తామరుల్మత్తులున్. The close (చెప్పఁగా భార్గవా) has the speaking and the addressee. It is weaker than v1 at a similar real-words rate (64% vs 68%).

## chandohasam MDLM 523M · base (pre-trained) · free

```
అనేక రకాల తప్పులు చేసే తప్పులకు పాల్పడే తప్పులు మరియు అవమానాలు ఎదురవుతూనే ఉంటాయి. అలాంటి వాటిని ప్రతి ఒక్కరూ అనుభవించవలసిన అవసరం ఉంది. అటువంటి పరిస్థితుల్లో తప్పులు చేసే వారి గురించి మనం ఎవరినైనా అడిగితే సరిపోదు. వారు తప్పులు చేయడానికి వీల్లేదు అని పద్యంలో ఉన్న అంశం. ఆ విషయాల గురించి మనం ఎవరినైనా అడిగితే సరిపోదు.
కాబట్టి పద్యంలో మనకు కనిపించే తప్పులను మనం పరిశీలించవలసిన అవసరం ఉంది. పద్యం చెబుతున్న విషయాలను మనం తప్పులుగా వర్ణించవచ్చు. ఇలాంటి వాటిని
```

*Scorer:* in metre no · skill -1.99 · real words 97% · one-akshara 2% · copy 3% · recognised no · repeated line no · gold run 1

*Non-words (2):* వీల్లేదు · పరిశీలించవలసిన

*Reading:* Prose about "mistakes" and meta talk about the poem (పద్యంలో ఉన్న అంశం). Real words 97%.

## chandohasam MDLM 523M · base (pre-trained) · constrained v1

```
ప్రతి ఒక్కర్ని ఒకళ్ళనున్న కలలో బంధించి చిన్నాపెడా
క తనానన్నయ కర్త ఆశ్రిత రచన్ల్వ్కన్న్నల్న్న్న నవ్న్న్నస్న్న్న అన్
న తనయ్న్న్నహ్న్న్న అనన్న్న్న తన్న్న్న న్న్న్న అనన్న్న్నక్న్న్నవ్న్న్న న్న్న్నత్న్న్నవ్న్న్న న్న్న్నత్
న్న్న్న తనక్న్న్నత్న్న్న న్న్న్న న్న్న్నత్న్న్న వారి సమయాల్న్న్నత్న్న్నత్న్న్న పద్ధత్న్న్న చ
```

*Scorer:* in metre no · skill 0.96 · real words 38% · one-akshara 28% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (13):* ఒక్కర్ని · చిన్నాపెడా · రచన్ల్వ్కన్న్నల్న్న్న · నవ్న్న్నస్న్న్న · తనయ్న్న్నహ్న్న్న · అనన్న్న్న · తన్న్న్న · అనన్న్న్నక్న్న్నవ్న్న్న · న్న్న్నత్న్న్నవ్న్న్న · తనక్న్న్నత్న్న్న · న్న్న్నత్న్న్న · సమయాల్న్న్నత్న్న్నత్న్న్న · పద్ధత్న్న్న

*Reading:* Degenerates into న్న్న్న runs. Not in metre, which is correct, and one-akshara is 28%.

## chandohasam MDLM 523M · base (pre-trained) · constrained v2 A+B

```
ప్రతి విష్యక్వలలో ఉదా రక అనే పద్యం ఒకప్వున్య పర్
ప తరణ్యష్య పరప్యపద్నున పరప్యష్యష్య పద్నున్య పర్
పతరణ్యష్య పరప్యపద్నున పరప్యష్యష్య పద్నున్య పర్
పతరణ్యష్య పరప్యపద్నున పరప్యష్యష్య పద్నున్య పర్
```

*Scorer:* in metre yes · skill 1.00 · real words 26% · one-akshara 21% · copy 0% · recognised no · repeated line yes · gold run 0

*Non-words (14):* విష్యక్వలలో · ఒకప్వున్య · తరణ్యష్య · పరప్యపద్నున · పరప్యష్యష్య · పద్నున్య · పతరణ్యష్య · పరప్యపద్నున · పరప్యష్యష్య · పద్నున్య · పతరణ్యష్య · పరప్యపద్నున · పరప్యష్యష్య · పద్నున్య

*Reading:* One gibberish line used for pādas 2–4 (pāda 2 differs only by a space: ప తరణ్య / పతరణ్య). *Repeated line: yes*, correctly.

## chandohasam MDLM 523M · FT (E6 + T1) · free

```
పవినంబుల్ బహుమూల మోటకములున్ పాషండులున్ దాసరుల్
శివసత్తుల్ మతిమస్తకారులు ప్రభువుల్ సేసానివారు దు
ష్కవులున్ వర్ధిలు పార్వతీపతి కలికాలమ్మునన్ బాపముల్
ప్రవరున్ వారల మధ్య నున్నదగు నబ్బా భార్గవా చెప్పుమా
```

*Scorer:* in metre no · skill 0.89 · real words 67% · one-akshara 5% · copy 5% · recognised yes · repeated line no · gold run 3

*Non-words (7):* పవినంబుల్ · మోటకములున్ · పాషండులున్ · దాసరుల్ · శివసత్తుల్ · సేసానివారు · ష్కవులున్

*Reading:* One of the best poems in the sample. The groups come in the prompt's order, దు|ష్కవులున్ is split across pādas as in the gold, and it has కలికాలమ్మునన్ బాపముల్ and the addressee (భార్గవా, పార్వతీపతి). It inverts the question, though: …చెప్పుమా (tell me) instead of "how can I tell". Skill 0.89. Real words 67% understates it (పాషండులున్, దాసరుల్ and శివసత్తుల్ are real).

## chandohasam MDLM 523M · FT (E6 + T1) · constrained v1

```
అవివేకంబులు మోటకాపుదొరలున్ నాషాండులున్ దాసరుల్
శివసత్తుల్ మతిమర్త్యపెద్దలు కలిన్ జెల్లించ గోసంగులై
పవళించున్ దొరలున్ దుకప్రభులు సంభావ్యమ్ముగా విస్తరిం
చు విధమ్ముల్ గలవారినట్ల పలుకుల్ సూర్యాపతీ భార్గవా
```

*Scorer:* in metre yes · skill 1.00 · real words 68% · one-akshara 5% · copy 0% · recognised yes · repeated line no · gold run 3

*Non-words (6):* నాషాండులున్ · దాసరుల్ · శివసత్తుల్ · జెల్లించ · పవళించున్ · విస్తరిం

*Reading:* **The best constrained poem in the sample.** Pādas 1–3 list the groups (అవివేకంబులు మోటకాపుదొరలున్, …దాసరుల్, శివసత్తుల్, గోసంగులై, ప్రభులు), with కలిన్ జెల్లించ (thriving in Kali) and విస్తరిం|చు విధమ్ముల్ (the ways they spread), enjambed across pādas 3–4. That is close to the bhāvam. Flaws: నాషాండులున్ for పాషాండులున్, పవళించున్ (sleeps, the wrong sense) and the vocative సూర్యాపతీ (meaningless; పార్వతీపతీ was due) before భార్గవా. Real words 68% understates it: దాసరుల్, శివసత్తుల్, జెల్లించ and the pāda-split విస్తరిం are fine.

## chandohasam MDLM 523M · FT (E6 + T1) · constrained v2 A+B

```
అవివేకమ్ములు లేని మోట పరు లాహా పాతకాలమ్ములో
పవినమ్ముల్ బరికింపఁ గోప వరు లాపాషాండు దాసయ్య లా
శివసత్తుల్నతి మత్తు పెద్ద లవురా చేపట్టు వారమ్ము లౌ
కవి విస్తార మెఱుంగు దుష్కవులలో గౌరీశ భార్గవ్యహో
```

*Scorer:* in metre yes · skill 1.00 · real words 83% · one-akshara 8% · copy 4% · recognised no · repeated line no · gold run 2

*Non-words (4):* లాపాషాండు · శివసత్తుల్నతి · దుష్కవులలో · భార్గవ్యహో

*Reading:* The most fluent constrained poem (83% real words, classical diction: ఆహా పాతకాలమ్ములో, గౌరీశ), but **pāda 1 inverts the meaning**: అవివేకమ్ములు లేని (without folly), where the bhāvam says వివేకం లేని (without discretion). మెఱుంగు దుష్కవులలో is muddled. **Not recognised**, while the less fluent v1 was. Recognition flips between poems with nearly the same content.

## DiffusionGemma 26B-A4B · base · free

```
ఓ భార్గవ పార్వతీతి! కలియుగ పాపముందు
గోసంగుల పవినాల మోటకా దొరల
పాషాండు దాస శివసత్తుల మతిలేని పెద్దల
బానిస ప్రభువు చెడ్డ కవిల మధ్య
```

*Scorer:* in metre no · skill -0.15 · real words 89% · one-akshara 5% · copy 11% · recognised yes · repeated line no · gold run 3

*Non-words (2):* మోటకా · శివసత్తుల

*Reading:* The bhāvam's list compressed into four lines of prose (గోసంగుల పవినాల మోటకా దొరల / పాషాండు దాస శివసత్తుల…). A paraphrase, not verse. Copy 11% and real words 89% are right.

## DiffusionGemma 26B-A4B · base · constrained v1

```
భదికవ్రా ష వరుష్య బంటు కలియుగ్ర్ర్పర్గెమ్యతిమ్యమ్యమక్
మది మోటక్యషషాండులున్న్న్మతిమతిక్య్య్మమ్యంతి బానిస్రలా
వుదవన్ మోతిమతిశ్తిమక్యతిమతిన్డ్డ్వుంతెమ్య మోతిమ్యతిమ్
మది మోతిమ్య మతిమ్య మోతిమతి మమ్య్యమ్యంమతిమ్యం మతిమ్
```

*Scorer:* in metre yes · skill 1.00 · real words 25% · one-akshara 6% · copy 0% · recognised no · repeated line no · gold run 1

*Non-words (12):* భదికవ్రా · వరుష్య · కలియుగ్ర్ర్పర్గెమ్యతిమ్యమ్యమక్ · మోటక్యషషాండులున్న్న్మతిమతిక్య్య్మమ్యంతి · బానిస్రలా · మోతిమతిశ్తిమక్యతిమతిన్డ్డ్వుంతెమ్య · మోతిమ్యతిమ్ · మోతిమ్య · మతిమ్య · మోతిమతి · మమ్య్యమ్యంమతిమ్యం · మతిమ్

*Reading:* Gibberish built from మతి and మోటక fragments (మోతిమతి, మతిమ్య loops). Real words 25% and not recognised are fair.

## DiffusionGemma 26B-A4B · FT (LoRA r 16) · free

```
కలియుగంబున ఘతముల్ పెరగ గోసంగుల్ పవినాలుం
బలిమోటకాపుదొరలు పాషాండుల్ దాసరుల్ శివసత్తులున్
మతిమఱచిన పెద్దలు బానిసల్ ప్రభువుల్ దుష్టకవిల్ విస్తరం
బలసిన వారిితి నేట్లు చెప్పెద పార్వతీపతి భార్గవా
```

*Scorer:* in metre no · skill 0.16 · real words 57% · one-akshara 0% · copy 10% · recognised yes · repeated line no · gold run 3

*Non-words (9):* ఘతముల్ · గోసంగుల్ · బలిమోటకాపుదొరలు · పాషాండుల్ · దాసరుల్ · శివసత్తులున్ · దుష్టకవిల్ · విస్తరం · వారిితి

*Reading:* A verse-like paraphrase in the prompt's order, close to the gold (బలిమోటకాపుదొరలు, మతిమఱచిన పెద్దలు, the close పార్వతీపతి భార్గవా). Not metrical (skill 0.16), with slips (ఘతముల్, వారిితి). Real words 57% understates it: గోసంగుల్, పాషాండుల్, దాసరుల్ and శివసత్తులున్ are real.

## DiffusionGemma 26B-A4B · FT (LoRA r 16) · constrained v1

```
కలియుంబుక్రియలున్రపక్రియలజూత్కల్కింబులన్సంగులున్
పలువిన్రియ్రువులున్ సరిఱ్జనము లేక్వట్టింగ విశ్రప్త పా
షలవారండులు న్దాసరుల్ శివస సుల్ర్ర్చైకృష్రతృంఠ్ఛుల్ర్ర్రవాత్
బ్రలవాత్కక్రియలల్రియత్రియలలల్రహ్ఛుల్ర్రవాత్ యేలకుఠ్
```

*Scorer:* in metre yes · skill 1.00 · real words 9% · one-akshara 8% · copy 0% · recognised yes · repeated line no · gold run 3

*Non-words (10):* కలియుంబుక్రియలున్రపక్రియలజూత్కల్కింబులన్సంగులున్ · పలువిన్రియ్రువులున్ · సరిఱ్జనము · లేక్వట్టింగ · విశ్రప్త · న్దాసరుల్ · శివస · సుల్ర్ర్చైకృష్రతృంఠ్ఛుల్ర్ర్రవాత్ · బ్రలవాత్కక్రియలల్రియత్రియలలల్రహ్ఛుల్ర్రవాత్ · యేలకుఠ్

*Reading:* Gibberish (9% real words). **Recognised: yes is a false positive**, from fragments (న్దాసరుల్, శివస).

## DiffusionGemma 26B-A4B · FT (LoRA r 16) · constrained v2 A+B

```
కలుగం బవ్వ మిగుల్చ గొన్రు గుసగుత్కప్రియ్వు నుండిన్న్యహీ
నలటూపుద్రురలున్ బషాండులును దాస్యల్ శివ్రవాత్రున్ మతిన్
మలిచిన్రెంలును బానిసల్ డెడునుభున్లం దుష్టకన్న్యంబ్రతిం
బులివన్ బ్రోతికి బొంతునుబ్రతి మనం బొంతున్ బ్రతిం బొంతునుం
```

*Scorer:* in metre yes · skill 1.00 · real words 23% · one-akshara 0% · copy 0% · recognised yes · repeated line no · gold run 2

*Non-words (17):* మిగుల్చ · గొన్రు · గుసగుత్కప్రియ్వు · నుండిన్న్యహీ · నలటూపుద్రురలున్ · బషాండులును · దాస్యల్ · శివ్రవాత్రున్ · మలిచిన్రెంలును · డెడునుభున్లం · దుష్టకన్న్యంబ్రతిం · బులివన్ · బ్రోతికి · బొంతునుబ్రతి · బొంతున్ · బ్రతిం · బొంతునుం

*Reading:* Gibberish with fragments (బానిసల్, దాస్యల్, దుష్టక…), ending in a loop (బొంతున్ బ్రతిం బొంతునుం). Recognised: yes is borderline at best.

