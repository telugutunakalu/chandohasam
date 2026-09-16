# yathi1.pdf — rule extraction

**Source.** *పద్యవిద్య*, chapter 6 "యతి నియమము", printed pages 239–280 (42 scanned pages, no text layer; read visually). Sections covered: §6.0 – §6.3.9 (the §6.3.9 example list ends mid-way at example 174; it continues in the next document). Author not visible on these pages.

**Conventions in this file.**
- Rule IDs `Y1-…` are ours (this file), so the engine and the later documents can cite them. The book's own section numbers are kept in brackets, e.g. `[6.1.9]`.
- Forward references the book makes to later sections (6.8, 6.10, 6.11, 6.12, 6.14, 6.15, 6.28, 6.29, 6.30, 6.34, 6.42, 6.51, 6.75, 6.77, 6.79, 4.6, 4.9, 5.23, 7.63, 8.2) are listed in §10 so that yathi2–yathi20 can be linked to them.
- Telugu terms are kept; a gloss follows the first use. "వళి" = the first akshara of a pāda; "యతిస్థానము" = the prescribed position; "యతిమైత్రి" = the required sound agreement.
- Transcriptions of the examples are from a scan and should be verified against the printed book before being used as gold data (§Appendix B).

---

## 1. Definition [6.0, 6.1.2]

| id | rule |
|---|---|
| **Y1.1** | In every pāda the first akshara is the **వళి**. |
| **Y1.2** | Each meter's lakshaṇa fixes one (sometimes more) **యతిస్థానము** in the pāda. |
| **Y1.3** | The akshara at the యతిస్థానము must be in **యతిమైత్రి** with the వళి: it is either the same akshara or a "friend" (మిత్రము) of it. Which aksharas are friends is what the 41 yati rules define. |
| **Y1.4** | The rule holds in **every pāda, independently**: the వళి of pāda *k* is compared with the yati akshara of pāda *k* only [6.1.7 (3)(ii)]. |
| **Y1.5** | Names: వళి, విరతి, విశ్రాంతి, విశ్రామము, విశ్రమము, శ్రాంతి, విరమణము, విరమము, విరామము, యతి, వడి (11 names; Appakavi uses 10 of them). In ordinary usage యతి and వళి are synonyms; the book uses **యతులు**. Note the usage "ఉత్పలమాలలో 1–10 అక్షరములకు యతి" means *the 1st and the 10th akshara* must agree. |

## 2. Where the yati falls [6.1.6]

**Y2.1** The *maitri* rules (which sounds pair) are the same for every meter; only the *position* depends on the meter. ("క–ఖ" is a yati pair in every meter; "క–చ" in none.)

| meter class | position rule | book's examples |
|---|---|---|
| **వృత్తములు** (fixed akshara count) | the *n*-th akshara, given per meter | ఉత్పలమాల 10, చంపకమాల 11, శార్దూలము 13, మత్తేభము 14 |
| **జాతులు / ఉపజాతులు** (gana meters) | "on the *k*-th gana" = **the first akshara of gana *k*+1** | ఆటవెలది, తేటగీతి: "3వ గణము మీద" = first akshara of gana 4 (విశ్వదాభిరామ వినుర వేమ: వి…వి) |
| **కందము** | **no yati in pādas 1 and 3**; in pādas 2 and 4, on the 3rd gana = first akshara of gana 4 [4.6] | |
| **సీసము** | 8 ganas per pāda (6 ఇంద్ర + 2 సూర్య); **two independent yatis per pāda**: first akshara of gana 1 ↔ first akshara of gana 3 (పూర్వార్ధము), first akshara of gana 5 ↔ first akshara of gana 7 (ఉత్తరార్ధము). The two halves are unrelated [4.9]. | |
| **బహుయతులు** (several yatis in one pāda) | all listed aksharas of the pāda are mutually in maitri | స్రగ్ధర 1-8-15, మహాస్రగ్ధర 1-9-16, మంగళమహాశ్రీ 1-9-17 |
| **యతి లేని పద్యము** | only **దండకము** has neither yati nor prāsa | |

**Y2.2 బహుయతి నియతి** [6.30, forward]. When a pāda has several yatis and a conjunct akshara (సంయుక్తాక్షరము) stands at the pāda start or at a yati position, **the same member of the conjunct must serve for every yati of that pāda**.

**Y2.3** Note for our catalogue: seesam's second yati is *not* between the pāda's first akshara and gana 7; it is between gana 5 and gana 7. The engine needs yati **pairs** (or groups), not bare positions: vrittas `{1, n}`; jati `{1, gana k+1}`; seesam `{1,3}` and `{5,7}` (gana starts); sragdhara-type `{1, 8, 15}` all mutual.

**Y2.4 ప్రాసయతి** (rhyme instead of yati at the yati position) [6.1.6 (6), 6.1.7]:
- (i) **not allowed** in vrittas (ఉత్పలమాల …) nor in jatis such as కందము;
- (ii) **allowed, even freely,** in సీసము, తేటగీతి, ఆటవెలది;
- (iii) in the **ఉద్ధురమాలా వృత్తములు** (more than 26 aksharas per pāda: లయగ్రాహి, లయవిభాతి, లయహారి, త్రిభంగి) **only** prāsayati is used.
- It is one of the 41 yatis (§5). Where it is allowed, one pāda may use prāsayati and another an ordinary yati; the choice is free per pāda [6.1.7 (3)(ii)].

## 3. What "maitri" means — the vowel groups [6.2.1, 6.1.7 (5)(ii)]

**Y3.1 స్వరమైత్రి (vowel groups).** Vowels pair only inside their group; there is **no exception** to this division; every other yati rule presupposes it.

| group | members |
|---|---|
| అ-వర్గము | అ ఆ ఐ ఔ |
| ఇ-వర్గము | ఇ ఈ ఋ ౠ ఎ ఏ |
| ఉ-వర్గము | ఉ ఊ ఒ ఓ |

**Y3.2 An akshara's yati = consonant maitri AND vowel maitri.** "క–గ చెల్లును" is shorthand for క్–గ్; the vowels riding on them must *also* belong to the same group (Y3.1). So క–గ, కా–గై, కౌ–గ are yatis; క–గి is not. Illustration [6.1.3]: for a వళి క, the "ordinary" (సాధారణ) yati aksharas are the 16 క కా కై కౌ ఖ ఖా ఖై ఖౌ గ గా గై గౌ ఘ ఘా ఘై ఘౌ.

**Y3.3 Word position is irrelevant** [6.1.3, 6.1.8 (3), (9)]. The yati akshara may be word-initial, word-medial or word-final, and may be preceded or followed by a పూర్ణబిందువు or అర్ధబిందువు. (Examples: రాజ… word-initial at 10; ప్రసన్న medial; విభాసిత medial; ఒకో final.)

**Y3.4 The four pādas are independent** [6.1.7 (3)(ii)]. One pāda may use a స్వరయతి, another a వ్యంజనయతి, another an ఉభయయతి; nothing forces the same kind across pādas. In a seesam + gīta, 4×2 + 4 = 12 independent yatis.

## 4. Signs that do (not) matter [6.1.9, page 253 (5)]

| id | sign | rule |
|---|---|---|
| **Y4.1** | అర్ధబిందువు ఁ (అరసున్న) | **No effect whatsoever** on yati, before or after the akshara: ఁక–గ, క–ఁగ, ఁక–ఁగ are all simply క–గ. (It matters for prāsa [5.7, 5.8], not for yati.) |
| **Y4.2** | పూర్ణబిందువు ం **before** the yati akshara (i.e. on the preceding akshara) | Never *breaks* a maitri: ంక–గ, క–ంగ, ంక–ంగ = క–గ. **In addition** it *creates* maitri for some pairs that otherwise have none: త–న is no yati, but ంత–న is. Those are the బిందు యతులు [6.12], అనునాసికాక్షర యతులు [6.14], అనుస్వారసంబంధ యతులు [6.15] (later documents). |
| **Y4.3** | పూర్ణబిందువు ం **on** the yati akshara itself (కం) | No effect: కం–గ, క–గం, కం–గం = క–గ; అం–ఆ, అ–ఆం = అ–ఆ. |
| **Y4.4** | విసర్గ ః | In Sanskrit words it usually changes or drops; where it stays (అంతఃకరణము, దుఃఖము, అంతఃపురము, తపఃఫలము) it has **no effect**: క–ఃఖ = క–ఖ, for the akshara before or after it. |
| **Y4.5** | ద్రుతము న్ **after** the yati akshara | No effect: క … గన్ = క–గ. (న్ is written separately only for reading ease; at the *pāda start* it is not separated because it influences the next, prāsa, akshara [5.23].) |
| **Y4.6** | ద్రుతము న్ **before** an akshara (end of the previous pāda before the వళి, or immediately before the yati akshara) | *Extra* possibilities arise: సంయుక్తయతి – నకార సంశ్లేషము [6.28]; the same for ల్ [6.29]. (Later documents.) |

## 5. The 41 yatis of Appakavi [6.1.3, 6.1.4, 6.1.5]

**Y5.1 Count.** Appakavi lists 41 yatis (more than any earlier lakṣaṇika, adding new ones to the inherited ones). Some he marks **అగ్రాహ్య** (not to be used). Later lakṣaṇikas and commentators added more. **అఖండయతి** Appakavi calls అప్రశస్త; some later writers defend it with earlier poets' usage; modern commentators examine it widely.

**Y5.2 The four divisions** (7 + 21 + 12 + 1 = 41):

| division | count | meaning |
|---|---|---|
| (1) స్వరయతులు | 7 | which vowels pair with which |
| (2) వ్యంజనయతులు (హల్లు యతులు) | 21 | which consonants pair with which |
| (3) ఉభయ యతులు | 12 | at a **sandhi** position inside a word, yati may be made **either** to the consonant that stands there **or** to the initial vowel of the second word: మంజీర = మంజు+ఈర → at జీ either a హల్లుయతి for జ or a స్వరయతి for ఈ; రామయ్య = రామ+అయ్య → మ or అ |
| (4) ప్రాసయతి | 1 | see Y2.4 |

**Y5.3 యతి భేదములు vs యతి విధానములు** (a division suggested by commentators, not by Appakavi) [6.1.5, 6.79]:
- *భేదము* = which varṇas pair with which (a table);
- *విధానము* = at sandhi positions and in certain words, **which varṇa is the one to test** (the vowel there, the consonant there, or an ādeśa akshara).
The rest of this document's §7 is a విధానము; §3 and the later documents' pair tables are భేదములు.

## 6. The seven స్వరయతులు [6.2]

(1) స్వరమైత్రి వళి (§3 above), (2) స్వరప్రధాన వళి (§7), (3) లుప్తవిసర్గకస్వర వళి, (4) ఋు వళి, (5) ఋత్వసంబంధ వళి, (6) ఋత్వసామ్య వళి, (7) వృద్ధివళి. (3)–(7) are treated in later sections (yathi2 onwards). Only (1) is a pure భేదము; (2)–(7) have their own names because they are విధానములు on top of (1).

## 7. స్వరప్రధాన యతి — the sandhi rule [6.3 – 6.3.9]

**Y7.1 Core rule.** When the akshara standing at a yati position (or at the pāda start) is the **product of a sandhi**, the sound to be tested is **the initial vowel of the second word (పరపదాది స్వరము)**, not the consonant of the resulting akshara.

> వేద + అర్థ = వేదార్థ. If దా stands at the yati position, yati is made to **అ** (any అ-వర్గ vowel at the వళి satisfies it). Making a హల్లుయతి to దా is **not** allowed. Conversely, if వేదార్థ begins the pāda, the వళి counts as అ.

**Y7.2 Scope of the rule** [6.3.1]. Any junction of two words where the second begins with a vowel, whether or not a formal స్వరసంధి applies: "రెండు పదముల కలయికలో, పరపదమునకు మొదట అచ్చు ఉన్నచో దానికే యతి."

**Y7.3 Sandhi types covered** [6.3.2, 6.3.3, 6.3.9]:

| family | sandhis named | example (split → pair) |
|---|---|---|
| Sanskrit అచ్-సంధులు | సవర్ణదీర్ఘ, గుణ, యణాదేశ, పూర్వరూప, అవఙాదేశము | వేద+అర్థ → అ; పరమ+ఈశ్వర → ఈ; చతుర+ఉక్తి → ఉ; భ్రాతృ+అన్వీత (యణాదేశ) → అ; విశ్వకర్త్రే+అక్షరాయ (పూర్వరూప) → అ; గో+అశ్వ = గవాశ్వ → అ |
| Sanskrit హల్-సంధి | జశ్త్వ | దృక్+అంచల = దృగంచల → అ (at గం); మరుత్+అధ్వ → అ; జగత్+ఏక → ఏ |
| Sanskrit విసర్గ సంధి | | చతుః+అభ్ధి → అ; పునః+ఉద్భవ → ఉ; ఆయుః+ఆరోగ్య → ఆ |
| Telugu sandhis | ఉత్వ, ఇత్వ, అత్వ | భూమిసురుడు+అంబర → అ; ఖురము+ఐ → ఐ (a one-akshara word counts as పరపదము); జనులు+ఎవ్వని → ఎ; అక్కటికము(న్)+ఊనుట → ఊ; నాది+ఐన → ఐ; ఒక్క+ఇంత → ఇ |
| Telugu ఆగమములు | నుగాగమము, టుగాగమము | same rule [6.75] |
| ద్రుతము + అచ్చు [6.3.4] | న్+అ=న, న్+ఆ=నా, న్+ఇ=ని … | the resulting న/నా/ని/నీ/ను/నూ is tested as **అ/ఆ/ఇ/ఈ/ఉ/ఊ**; హల్లుయతులు of న are **not** allowed (నగరిలోన్+ఆ → ఆ; సేరుటకున్+ఎద్ది → ఎ; కొండదరిలోన్+ఒంటిన్ → ఒ). The book repeats "ఇక్కడ న–నా లకు యతి అని పొరపడరాదు" at several examples. |
| యడాగమము + అచ్చు [6.3.5] | మా+అమ్మ = మా+య్+అమ్మ = మాయమ్మ | the య carries the vowel: test **అ**, not య's హల్లుయతులు (అలసత…యమ్ముని → అ–అ) |

**Y7.4 Applies at both ends** [6.3.6]. The sandhi may be at the **yati position** or at the **pāda start** (the వళి itself may be a sandhi product), or at both: భాషా+అపర at the pāda start and వివిధ+అధ్వర at the 10th → అ–అ; పరమ+ఈశ్వరి … యుందున్+ఇంద్రాణి → ఈ–ఇ; తరుణ+ఉష్ణద్యుతి … పంకజ+ఉద్భవ → ఉ–ఉ; తత్కులంబు+ఎల్లను … య్+ఏమి → ఎ–ఏ; దేశాళితోన్+ఆది … అజితుండు+ఐ → ఆ–ఐ.

**Y7.5 Only the sandhi akshara is affected.** Other aksharas of the same word keep their ordinary యతులు: in కవి+ఈశ్వర = కవీశ్వర, వీ is tested as ఈ, but క, శ్వ, ర take their హల్లు యతులు.

**Y7.6 The ద్రుతము elides when sandhi happens** [examples 18, 24, 85, 121]. సమిజ్జయమ్మునందున్+అతని → with sandhi నందతని (ఉత్వసంధి, న్ dropped); without sandhi నందునతని (న్ stays). Some junctions are **vikalpa** (sandhi optional): ఇంకన్+ఏల → ఇంకేల or ఇంకనేల; అనుచున్ = అంచున్ ('చు' of the శత్రర్థ form). The text as printed decides which happened.

**Y7.7 అపదము** [6.3.7 (iii)]. If the second element is not a word but an అపదము (రెండు+అవ = రెండవ; ఎడు, ఎడి …) the rule *may* still be applied; the book defers to విభాగయతులు [6.42] and [6.77].

**Y7.8 Special names** [6.3.7]. వృద్ధిసంధి → వృద్ధియతి [6.8]; అంత్యోష్మసంధి → అంత్యోష్మసంధి యతి [6.34]; రుగాగమము → రాగమ సంధియతి (an ఉభయయతి) [6.51]; నుగాగమము, టుగాగమము [6.75].

**Y7.9 స్వరయతి vs స్వరప్రధానయతి** [6.3.8]. స్వరయతి (Y3.1) is a *భేదము* (which vowels pair); స్వరప్రధానయతి (Y7.1) is a *విధానము* (at a sandhi, test the second word's initial vowel). The second always resolves through the first.

**Y7.10 Observed pairs.** Every one of the 174 examples resolves to a pair inside a single group of Y3.1: అ-వర్గ {అ-అ, అ-ఆ, అ-ఐ, అ-ఔ, ఆ-అ, ఆ-ఆ, ఆ-ఐ, ఐ-అ, ఐ-ఆ, ఐ-ఐ, ఔ-అ}; ఇ-వర్గ {ఇ-ఇ, ఇ-ఈ, ఇ-ఏ, ఇ-ఋ, ఈ-ఇ, ఈ-ఈ, ఈ-ఎ, ఈ-ఏ, ఎ-ఇ, ఎ-ఈ, ఎ-ఎ, ఎ-ఏ, ఎ-ఋ, ఏ-ఇ, ఏ-ఈ, ఏ-ఎ, ఏ-ఏ, ఏ-ఋ, ఋ-ఇ, ఋ-ఎ, ఋ-ఏ}; ఉ-వర్గ {ఉ-ఉ, ఉ-ఊ, ఉ-ఒ, ఉ-ఓ, ఊ-ఉ, ఊ-ఊ, ఊ-ఒ, ఒ-ఉ, ఒ-ఊ, ఒ-ఒ, ఒ-ఓ, ఓ-ఉ, ఓ-ఊ, ఓ-ఒ, ఓ-ఓ}. No cross-group pair occurs — a useful consistency check for the engine.

## 8. Yati vs prāsa [6.1.7]

| | ప్రాస | యతి |
|---|---|---|
| present in | not every meter (సీసము, తేటగీతి, ఆటవెలది, మంజరీద్విపద have none); must be stated per meter | every meter except దండకము; need not be stated |
| position | always the 2nd akshara of every pāda | varies per meter; must be stated, with prāsayati / బహుయతులు where relevant |
| relation between pādas | the 2nd aksharas of all four pādas are tied to the first pāda's | the four pādas' yatis are independent (Y3.4); only బహుయతులు inside one pāda are tied to each other (Y2.2) |
| what agrees | normally the **same** akshara in all pādas; maitri between different varṇas is the "extra" case (based on pronunciation similarity) | identity is the first rule, but friends are allowed → many భేదములు; a chief cause of friendship is **సజాతీయత** (same వర్గము: క ఖ గ ఘ) |
| vowel vs consonant | **consonants only**: క కా కి కీ కు కూ కృ కె కే కై కొ కో కౌ కం కః all rhyme with each other | **both**: the consonants must pair **and** the vowels on them must pair (Y3.2) |
| extra rule | ప్రాసపూర్వాక్షర నియమము exists | no such rule |

## 9. Sanskrit yati vs Telugu yati [6.1.8]

- **Y9.1** Sanskrit yati = a **word break (పదచ్ఛేదము)** at the yati position ("యతిర్విచ్ఛేద సంజ్ఞికా", వృత్తరత్నాకరము); hence the names విరామము, విశ్రామము, విశ్రాంతి. No sound agreement with the pāda's first akshara is required.
- **Y9.2** Telugu yati requires **no word break**; it requires **sound agreement** with the వళి (Y1.3, Y3.3). The two systems share nothing but the word.
- **Y9.3** Telugu **positions** in Sanskrit-origin vrittas (ఉత్పలమాల, చంపకమాల, మత్తేభము, శార్దూలము, స్రగ్ధర, మహాస్రగ్ధర) follow the Sanskrit yatis: శార్దూలము has Sanskrit yatis 12 and 7 (break after the 12th; the 19th is the pādānta yati); Telugu takes the first akshara after the break, the **13th**, and has no pādānta yati. (Some vrittas differ slightly.) Jati/upajati positions are native.
- **Y9.4** In Telugu a word may run across the pāda boundary; Sanskrit forbids it (పాదాంత యతి).
- Example [6.1.8 (8)]: శాకుంతలము 4-9 — పాతుం న ప్రథమం వ్యవస్యతి **జలం** … : the 12th akshara లం ends a word; likewise భవతాం, సమయే, గృహం.

## 10. Notes for the yati engine

1. **Inputs needed.** The scansion already gives syllables with `onset`, `vowel`, `anusvara`, `visarga`, `candrabindu`, `dead` (pollu), `word`; and the parser gives the yati akshara indices. What is missing is (a) **yati pairs/groups per meter** (Y2.3) instead of single positions, (b) **maitri tables** for consonants (later documents), (c) a **sandhi-split hypothesis** for Y7.
2. **Normalise before comparing** (Y4): drop ఁ everywhere; drop ం/ః on the yati akshara and on the వళి; drop a trailing న్/ల్ on the yati akshara (but keep the *preceding* bindu/drutam as a flag, because Y4.2 and Y4.6 *add* pairs).
3. **Compare as (consonant class, vowel group)** (Y3.2). Vowel groups are fixed (Y3.1). Consonant classes come from the 21 వ్యంజనయతులు (later docs); the simplest confirmed class is the వర్గము (క ఖ గ ఘ …).
4. **స్వరప్రధాన yati is a lattice, not a decision** (Y7). From the surface text alone the engine cannot know that దా in వేదార్థ hides అ. Practical policy, in line with how we already handle vikalpa in the DAWG: at a yati position and at the వళి, admit **both** readings — the akshara as written, and "vowel-initial second word" with each vowel that the akshara's vowel could result from under the listed sandhis (దా → అ/ఆ via సవర్ణదీర్ఘ; దే → ఇ/ఈ or ఎ/ఏ via గుణ or ఉత్వ+ఎ; దో → ఉ/ఊ or ఒ/ఓ; a bare న/నా/ని… → the vowel via ద్రుతము; య+vowel → the vowel via యడాగమము). Accept the yati if any admissible reading agrees, and **report which reading was used**. A lexicon/sandhi splitter can later narrow it to the true one.
5. **ఉభయ యతులు** (Y5.2 (3)) are the same lattice from the other side: at a sandhi position, either the consonant or the vowel reading may win.
6. **ప్రాసయతి** (Y2.4) must be tried only for సీసము / తేటగీతి / ఆటవెలది and the ఉద్ధురమాలా vrittas; there it is the *second-akshara* consonant test between the వళి word and the yati word.
7. **Consistency checks** the corpus run can enforce: Y7.10 (no cross-group vowel pairs), Y2.4 (i) (no prāsayati in vrittas/kanda), Y2.1 (kanda has no yati in pādas 1, 3).
8. **Forward references to resolve in later documents:** 6.8 వృద్ధియతి · 6.10 ప్రాణియతి (identity) · 6.11 వర్గజయతి (same varga) · 6.12 బిందు యతులు · 6.14 అనునాసికాక్షర యతులు · 6.15 అనుస్వారసంబంధ యతులు · 6.28 సంయుక్తయతి / నకార సంశ్లేషము · 6.29 ల్ · 6.30 బహుయతి నియతి · 6.34 అంత్యోష్మసంధి యతి · 6.42 విభాగయతులు · 6.51 రాగమ సంధియతి · 6.75 నుగాగమ / టుగాగమ · 6.77 అపదములు · 6.79 భేద/విధాన analysis · 4.6 కందపద్య లక్షణము · 4.9 సీసపద్య లక్షణము · 5.7 / 5.8 అర్ధబిందు / ఖండాఖండ ప్రాస · 5.23 సంధిగత ప్రాస · 7.63 మధ్యాక్కర (Nannaya's 5th-gana yati) · 8.2 seesam specifics.

---

## Appendix A — worked examples in the prose sections

**§6.1.1** (position + kind of yati)

| meter | pāda (yati akshara underlined in the book) | వళి / yati akshara | kind | source |
|---|---|---|---|---|
| మ (14) | క్రలలోఁదోఁచిన యర్థముల్ నిజములే క్రర్మానుబంధంబులన్ | క / క | ప్రాణియతి [6.10] | భాగ-7-55 |
| ఉ (10) | కాదనకిట్టిపాటి యపకారము తక్షకుఁడేక విప్ర సం | కా / కా | ప్రాణియతి | భారత-ఆది-1-124 |
| చ (11) | కనుగొని గౌరవంబును మొగంబును గేలుఁబురఃప్రసారమున్ | క / గం | వర్గజయతి [6.11] | భారత-విరా-1-310 |
| మ (14) | కరుణాసింధుఁడు శౌరి వారిచరమున్ ఖండింపఁగా బంపె స/త్వరితా… | క / ఖం | వర్గజయతి | భాగ-8-109 |
| శా (13) | కాంచెన్వేష్ణవుఁడర్ధయోజన జటా ఘాటోత్థ శాఖోప శా | కాం / ఘా | వర్గజయతి | ఆముక్త-6-15 |

**§6.1.8 (9)** — position of the yati akshara inside the word is free: రాజకులైక భూషణుఁడు **రా**జమనోహరుడన్యరాజ తే (word-initial, 10) [భారత-ఆది-1-3]; సారమతిం గవీంద్రులు ప్ర**స**న్నకథాకలితార్థయుక్తి లో (సా–స, medial) [భారత-ఆది-1-26]; పరమవివేక సౌరభ వి**భా**సిత… (ప–భా, medial) [భారత-ఆది-1-24]; కుసుమసముద్గమంబగునొ**కో** … (కు–కో, final) [భారత-ఆది-3-170].

**§6.3** first examples: అమితాఖ్యానక శాఖలంబొలిచి వే**దా**ర్థామలచ్ఛాయమై (అ ← వేద+అర్థ) [భారత-ఆది-1-66]; ఇట్టి పదంబుగాంచి పర**మే**శ్వరు… (ఇ–ఈ, పరమ+ఈశ్వర, గుణ) [భారత-విరా-1-27]; ఉన్నత సంస్కృతాది చతు**రో**క్తి… (ఉ–ఉ, చతుర+ఉక్తి, గుణ) [నృసింహ-1-17]; ఆ కమలాక్షి యింపున దృ**గం**చల… (ఆ–అ, దృక్+అంచల, జశ్త్వ) [మను-3-90].

## Appendix B — the 174 స్వరప్రధాన examples [6.3.9]

Format: no. | meter | పాదాది reading — యతిస్థాన reading (split, sandhi) | pair | source. "X ---" alone means the pāda starts with the bare vowel X. Sandhi labels are the book's. Pādas printed with `/` in the book mark the yati position. Verify against the print before using as gold.

| # | m | split (sandhi) | pair | source |
|---|---|---|---|---|
| 1 | చ | అ — అమర+అరుల (సవర్ణదీర్ఘ) | అ-అ | భారత-ఆది-1-105 |
| 2 | చ | అ — ఉరగ+అంగన (సవర్ణదీర్ఘ) | అ-అ | పారి-1-82 |
| 3 | చ | అ — గో+అశ్వ = గవాశ్వ (అవఙాదేశము) | అ-అ | భారత-ఆశ్రమ-1-135 |
| 4 | చ | అ — మరుత్+అధ్వ (జశ్త్వ) | అ-అ | వసు-3-139 |
| 5 | సీ | అ — మెచ్చరు+అఖిల (ఉత్వ) | అ-అ | మను-1-50 |
| 6 | శా | అం — వదనుండు+అద్వంద్వుఁడు (ఉత్వ) | అ-అ | ఆముక్త-1-77 |
| 7 | తే | అ — పాలనున్న+అప్పుడు (అత్వ) | అ-అ | భారత-విరా-2-13 |
| 8 | తే | అ — శయ్యనున్న+అంత (అత్వ) | అ-అ | రామా-4-153 |
| 9 | తే | అ — య్+అర్థమెల్ల (యడాగమము+అచ్చు) | అ-అ | మను-2-59 |
| 10 | చ | అ — శరణ+ఆగత (సవర్ణదీర్ఘ) | అ-ఆ | భా.రామ-కి-205 |
| 11 | ఉ | అం — వలయ+ఆభరణంబుల (సవర్ణదీర్ఘ) | అ-ఆ | ఆముక్త-1-61 |
| 12 | చ | అ — ముఖుఁడు+ఐ (ఉత్వ) | అ-ఐ | భాగ-10-ఉ-271 |
| 13 | ఉ | అం — కొలువు+ఐ (ఉత్వ) | అ-ఐ | ఉ.రామ-8-5 |
| 14 | తే | అ — నాది+ఐన (ఇత్వ) | అ-ఐ | భారత-ఆది-5-224 |
| 15 | చ | అ — పులిన్+ఐనను (ద్రుతము+అచ్చు) | అ-ఐ | భారత-విరా-1-83 |
| 16 | క | కృష్ణ+అరుణ (సవర్ణదీర్ఘ) — ఘనతర+అంగ (సవర్ణదీర్ఘ) | అ-అ | భారత-ఆది-2-89 |
| 17 | ఉ | ఆత్మ+అనుజ (సవర్ణదీర్ఘ) — కద+అన్న (అత్వ) | అ-అ | ఉ.రామ-4-124 |
| 18 | చ | సమిజ్జయమ్మునందు(న్)+అతని (ఉత్వ; న్ elides) — చతుః+అభ్ధి (విసర్గ) | అ-అ | వి.వి-1-93 |
| 19 | క | హరిత్+అశ్వ (జశ్త్వ) — తేజుఁడు+అస్త్ర (ఉత్వ) | అ-అ | భారత-ఉ-2-211 |
| 20 | ఉ | భాషితంబు+అందము (ఉత్వ) — మరుత్+అంచిత (జశ్త్వ) | అ-అ | నృసింహ-2-62 |
| 21 | సీ | గగనస్థము+అగు (ఉత్వ) — షట్+అంశ (జశ్త్వ) | అ-అ | భాగ-3-345 |
| 22 | ఆ | సురులతోన్+అజుఁడు (ద్రుతము+అచ్చు) — ధన+అధిపతియు (సవర్ణదీర్ఘ) [not న-నా] | అ-అ | నిర్వ.రామ-2-45 |
| 23 | క | ధుర్ధరులు+అరగొనక (ఉత్వ) — తాఁకిరి+అతి (ఇత్వ) | అ-అ | కుమార-12-63 |
| 24 | ఆ | దానికి(న్)+అజరులు (ఇత్వ; న్ elides) — వీరులు+అతుల (ఉత్వ) | అ-అ | భారత-ఆది-3-64 |
| 25 | తే | చెఱుచుట+అప్పనము (అత్వ) — అర్మత్వము+అరసి (ఉత్వ) | అ-అ | భారత-ఆశ్రమ-1-68 |
| 26 | క | సాపత్న్యంబు+అను (ఉత్వ) — దీనన్+అదియును (ద్రుతము+అచ్చు) | అ-అ | భారత-ఆది-4-185 |
| 27 | క | ఒక్క+అంతగ(న్) (అత్వ) — వృత్తిన్+అక్షోభ్య (ద్రుతము+అచ్చు) | అ-అ | భారత-శాం-5-337 |
| 28 | క | వెడపగన్+అమేయ (ద్రుతము+అచ్చు) — చేసిన+అట్టి (అత్వ) [not న-న] | అ-అ | భారత-అను-5-109 |
| 29 | క | తెగువకున్+అనుజన్ములు (ద్రుతము+అచ్చు) — వాంచుట+అనుమతి (అత్వ) | అ-అ | నిర్వ.రామ-8-127 |
| 30 | క | చుట్టునున్+అమేయ (ద్రుతము+అచ్చు) — అంతన్+అతి (ద్రుతము+అచ్చు) [not న-న] | అ-అ | భారత-ఆది-2-90 |
| 31 | చ | య్+అ (యడాగమము+అచ్చు) — య్+అ (యడాగమము+అచ్చు) | అ-అ | మను-5-62 |
| 32 | క | పుర+అరాతి (సవర్ణదీర్ఘ) — జన+ఆసక్త (సవర్ణదీర్ఘ) | అ-ఆ | భారత-ఆది-3-227 |
| 33 | చ | భాక్+అలఘు (జశ్త్వ) — కళికా+ఆకృతి (సవర్ణదీర్ఘ) [not గ-కా] | అ-ఆ | వసు-1-121 |
| 34 | చ | నిక్కువంబు+అనఘ (ఉత్వ) — గుణ+ఆఢ్యుఁడవున్ (సవర్ణదీర్ఘ) | అ-ఆ | భారత-ఆది-4-220 |
| 35 | తే | వచ్చెన్+అఖిల (ద్రుతము+అచ్చు) — మధు+ఆగమంబు (యణాదేశ) | అ-ఆ | భీమ-5-93 |
| 36 | సీ | ..ఐన+అది (అత్వ) — లోక+ఆగమంబు (సవర్ణదీర్ఘ) | అ-ఆ | భారత-ఆది-8-93 |
| 37 | క | తిమిర+అరాతి (సవర్ణదీర్ఘ) — యుక్తుఁడు+ఐ (ఉత్వ) | అ-ఐ | కుమార-11-62 |
| 38 | క | వంశజులకున్+అనిరి (ద్రుతము+అచ్చు) — నిపుణులు+ఐన (ఉత్వ) | అ-ఐ | భారత-ఆది-4-182 |
| 39 | చ | అగున్+అనవరత (ద్రుతము+అచ్చు) — సుఖ,ఆయుః+ఐశ్వర్యంబుల్ (విసర్గ) | అ-ఐ | భారత-ఆది-6-287 |
| 40 | క | గెల్వు+అరుదు (ఉత్వ) — గెల్వన్+ఔనని (ద్రుతము+అచ్చు) | అ-ఔ | కుమార-3-58 |
| 41 | ఉ | ఆ — వివిధ+అర్థ (సవర్ణదీర్ఘ) | ఆ-అ | భారత-విరా-1-6 |
| 42 | తే | ఆ — విశ్వకర్త్రే+అక్షరాయ (పూర్వరూప) | ఆ-అ | ఉ.హరి-2-219 |
| 43 | శా | ఆ — భ్రాతృ+అన్వీతుఁడై (యణాదేశ) | ఆ-అ | ఉ.రామ-2-213 |
| 44 | ఉ | ఆ — జగత్+అంబిక (జశ్త్వ) | ఆ-అ | ఉ.హరి-3-151 |
| 45 | శా | ఆ — లేదు+అంతంబు (ఉత్వ) | ఆ-అ | భాగ-8-574 |
| 46 | ఉ | ఆ — తగున్+అంగనకున్ (ద్రుతము+అచ్చు) | ఆ-అ | భాగ-10-పూర్వ-1711 |
| 47 | ఉ | ఆ — య్+అన్య (యడాగమము+అచ్చు) | ఆ-అ | భారత-ఆది-5-6 |
| 48 | శా | ఆ — మనీషా+ఆయత్తమున్ (సవర్ణదీర్ఘ) | ఆ-ఆ | భాగ-1-215 |
| 49 | ఉ | ఆ — తనువు+ఐ (ఉత్వ) | ఆ-ఐ | పాండు-2-151 |
| 50 | శా | చిత్త+ఆనందంబు (సవర్ణదీర్ఘ) — జనులకు(న్)+అర్థాంశు (ఉత్వ) | ఆ-అ | భారత-ఆది-3-21 |
| 51 | ఉ | షేషా+ఆవళి (సవర్ణదీర్ఘ) — హరిత్+అంతములు (జశ్త్వ) | ఆ-అ | శ్రీకాళ-2-35 |
| 52 | సీ | ఆయుః+ఆరోగ్య (విసర్గ) — యుక్తులు+అగుదురెల్ల (ఉత్వ) | ఆ-అ | భారత-ఆర-2-231 |
| 53 | తే | వియచ్చర+ఆది (సవర్ణదీర్ఘ) — పుట్టిన+అట్టి (అత్వ) | ఆ-అ | ఉ.రామ-8-286 |
| 54 | ఉ | బద్ధ+అనిరతాత్ముఁడై (సవర్ణదీర్ఘ) — అరిగెన్+అత్తఱి (ద్రుతము+అచ్చు) | ఆ-అ | భారత-మహా-42 |
| 55 | ఆ | చెడన్+ఆడన్ (ద్రుతము+అచ్చు) — మృగ+అక్షి (సవర్ణదీర్ఘ) | ఆ-అ | నిర్వ.రామ-5-11 |
| 56 | ఉ | లోన్+ఆరసి (ద్రుతము+అచ్చు) — ఇతరులు+అక్షర (ఉత్వ) | ఆ-అ | భారత-ఆది-1-26 |
| 57 | క | య్,ఉచితంబు+ఆ (ఉత్వ) — పోవుట+అర్మంబు (అత్వ) | ఆ-అ | కళా-3-282 |
| 58 | సీ | య్+ఆ (యడాగమము+అచ్చు) — ..న్+అ (ద్రుతము+అచ్చు) | ఆ-అ | మను-1-59 |
| 59 | శా | పూర్ణ+ఆలోల (సవర్ణదీర్ఘ) — ప్రభూత+ఆశ్చర్యులు (సవర్ణదీర్ఘ) | ఆ-ఆ | భారత-ఆది-6-31 |
| 60 | శా | దేశాళితోన్+ఆది (ద్రుతము+అచ్చు) — అజితుండు+ఐ (ఉత్వ) | ఆ-ఐ | భారత-ఆది-4-8 |
| 61 | క | అర్జునుఁడు+ఆరంగ (ఉత్వ) — య్+ఐ (యడాగమము+అచ్చు) | ఆ-ఐ | భారత-ఆది-3-16 |
| 62 | ఆ | ముదమునన్+ఆదరించె (ద్రుతము+అచ్చు) — ప్రీతిన్+ఆది (ద్రుతము+అచ్చు) [not నా-నా] | ఆ-ఆ | భారత-ఆది-7-226 |
| 63 | శా | ఐ — వినూత్న+అలంక్రియా (సవర్ణదీర్ఘ) | ఐ-అ | కళా-7-51 |
| 64 | సీ | ఐ — శరములన్+అందఱు (ద్రుతము+అచ్చు) | ఐ-అ | భారత-ద్రో-4-27 |
| 65 | సీ | ఐ — య్+అశనిచే (యడాగమము+అచ్చు) | ఐ-అ | కాశీ-6-193 |
| 66 | ఉ | ఐ — ద్రుపద+ఆత్మజన్ (సవర్ణదీర్ఘ) | ఐ-ఆ | భారత-ఉ-3-75 |
| 67 | ఉ | ఐ — దర్శనుఁడవు+ఐన (ఉత్వ) | ఐ-ఐ | ఉ.రామ-2-189 |
| 68 | సీ | ప్రీతుడు+ఐ (ఉత్వ) — ఇట్టులు+అనియె (ఉత్వ) | ఐ-అ | భారత-ఆది-2-106 |
| 69 | తే | భోగ్యము+ఐన (ఉత్వ) — నీకు(న్)+అర్మము (ఉత్వ) | ఐ-అ | భారత-ఆది-6-57 |
| 70 | తే | ఔ — అభిధానంబున్+అంబుజాక్షి (ద్రుతము+అచ్చు) | ఔ-అ | భారత-అను-5-178 |
| 71 | తే | ఔ — జముకంటెన్+అర్కు (ద్రుతము+అచ్చు) | ఔ-అ | కాశీ-2-89 |
| 72 | తే | న్+ఔపయిక (ద్రుతము+అచ్చు) — దుష్ట+అసురేంద్ర (సవర్ణదీర్ఘ) | ఔ-అ | గోపి.రామ-సుం-491 |
| 73 | సీ | య్+ఔన్నత్యమున (యడాగమము+అచ్చు) — మ్రింగిన+అట్టి (అత్వ) | ఔ-అ | మను-6-3 |
| 74 | తే | ఇ — నర+ఇంద్రుఁడు (గుణ) | ఇ-ఇ | రామా-5-44 |
| 75 | మ | ఇ — కరంబు+ఇష్టంబులు (ఉత్వ) | ఇ-ఇ | భారత-ఆది-1-12 |
| 76 | ఆ | ఇ — మెఱుఁగులు+ఈను (ఉత్వ) | ఇ-ఈ | భా.రామ-ఆర-1-218 |
| 77 | చ | ఇ — య్+ఏలొకో (యడాగమము+అచ్చు) | ఇ-ఏ | భారత-ఆది-4-30 |
| 78 | తే | తోఁచున్+ఇందు (ద్రుతము+అచ్చు) — ఋ | ఇ-ఋ | హర-4-53 |
| 79 | చ | భోజనంబు+ఇడిన (ఉత్వ) — యథా+ఇష్టము (గుణ) | ఇ-ఇ | ఉ.రామ-8-212 |
| 80 | తే | గుణములు+ఇంద్రియ (ఉత్వ) — బాల+ఇందు (గుణ) [not లి-లే] | ఇ-ఇ | భారత-అను-4-220 |
| 81 | క | య్,అర్థంబు+ఇదె (ఉత్వ) — సమూహము+ఇన్నిట (ఉత్వ) | ఇ-ఇ | భారత-ఆది-5-242 |
| 82 | తే | ..న్,ఆనతి+ఇచ్చి (ఇత్వ) — రక్షింపుము+ఇంపు (ఉత్వ) | ఇ-ఇ | హరి-ఉ-8-40 |
| 83 | క | ఒక్క+ఇంతయు (అత్వ) — ముట్టకుండన్+ఇటు (ద్రుతము+అచ్చు) | ఇ-ఇ | హరి-పూర్వ-8-117 |
| 84 | శా | వీరు+ఇమార్గమ్ము (ఉత్వ) — కాదు+ఏనిన్ (ఉత్వ) | ఇ-ఏ | భాగ-10-పూర్వ-337 |
| 85 | సీ | పాత్తు+ఇంతియ (ఉత్వ) — ఇంక(న్)+ఏల (అత్వ; sandhi vikalpa: ఇంకేల / ఇంకనేల) | ఇ-ఏ | భారత-ఆది-2-21 |
| 86 | ఆ | చేయుచున్+ఇవ్విధమునన్ (ద్రుతము+అచ్చు) — పెక్కులు+ఏండ్లు (ఉత్వ) | ఇ-ఏ | భారత-ఆది-3-110 |
| 87 | తే | చంపున్+ఇంద (ద్రుతము+అచ్చు) — తాన్+ఏర్చున్ (ద్రుతము+అచ్చు) [not ని-నే] | ఇ-ఏ | భారత-ఆది-8-308 |
| 88 | తే | య్+ఇతర (యడాగమము+అచ్చు) — పంక్తులు+ఏమి (ఉత్వ) | ఇ-ఏ | మను-4-34 |
| 89 | సీ | ఈ — య్+ఇందు (యడాగమము+అచ్చు) | ఈ-ఇ | భాగ-10-పూర్వ-1029 |
| 90 | ఉ | ఈ — పరమ+ఈశు (గుణ) | ఈ-ఈ | భాగ-7-459 |
| 91 | శా | ఈ — లేరు+ఈనాఁటి (ఉత్వ) | ఈ-ఈ | కాశీ-1-14 |
| 92 | శా | ఈ — ఎందు+ఏన్ (ఉత్వ) | ఈ-ఏ | మను-2-64 |
| 93 | ఉ | p1: ఈ — జగత్+ఏక (జశ్త్వ) → ఈ-ఏ; p2: భీమ+ఈశ్వర (గుణ) — గురుఁడు+ఈఁగులు (ఉత్వ) → ఈ-ఈ | | కాశీ-1-50 |
| 94 | క | య్,అమృతంబు+ఈ(న్) (ఉత్వ) — మగుడన్+ఇచ్చిన (ద్రుతము+అచ్చు) | ఈ-ఇ | భారత-ఆది-2-110 |
| 95 | క | వల్కలాజినములకున్+ఈ (no sandhi: న్+ఈ=నీ, ద్రుతము+అచ్చు) — ఫలాశనములకు(న్)+ఈ (sandhi: కు+ఈ=కీ, ఉత్వ) | ఈ-ఈ | భారత-ఆది-4-53 |
| 96 | శా | య్+ఈ (యడాగమము+అచ్చు) — మునులతోన్+ఈ (ద్రుతము+అచ్చు) | ఈ-ఈ | మను-3-102 |
| 97 | ఉ | విశ్వ+ఈశ్వర (గుణ) — నినున్+ఎప్పుడు (ద్రుతము+అచ్చు) | ఈ-ఎ | భాగ-10-పూర్వ-126 |
| 98 | ఉ | p1: ఎ — హరిణ+ఈక్షణ (గుణ) → ఎ-ఈ; p2: లేక+ఇవ్వన (అత్వ) — భూసురుఁడన్+ఏన్ (ద్రుతము+అచ్చు) → ఇ-ఏ | | మను-2-39 |
| 99 | ఉ | ఎ — నిలువక+ఇంటికి (అత్వ) | ఎ-ఇ | మను-2-50 |
| 100 | ఉ | ఎ — కలుగున్+ఇక్షు (ద్రుతము+అచ్చు) | ఎ-ఇ | మను-2-57 |
| 101 | ఉ | ఎ — య్+ఇయ్యమునానది (యడాగమము+అచ్చు) | ఎ-ఇ | భారత-ఆది-4-173 |
| 102 | ఉ | ఎ — జగము+ఎవ్వని (ఉత్వ) | ఎ-ఎ | భాగ-8-73 |
| 103 | శా | ఎ — రహిచేన్+ఏకాగ్రతన్ (ద్రుతము+అచ్చు) | ఎ-ఏ | మను-2-62 |
| 104 | ఆ | న్,అభిప్రాయము+ఎఱిఁగి (ఉత్వ) — పురుషుఁడు+ఇట్టులు (ఉత్వ) | ఎ-ఇ | భారత-ఆది-1-114 |
| 105 | సీ | పానర్చున్+ఎయ్యవి (ద్రుతము+అచ్చు) — ఒక్క+ఇంత (అత్వ) | ఎ-ఇ | భారత-శాం-4-172 |
| 106 | క | నాఁడు,ఎవ్వరున్+ఎఱుఁగక (ద్రుతము+అచ్చు) — కౌరవ+ఇంద్ర (గుణ) | ఎ-ఇ | భారత-ఆది-5-178 |
| 107 | మ | శాబకుండు+ఎదురై (ఉత్వ) — సర్వ+ఈశ (గుణ) | ఎ-ఈ | భాగ-1-285 |
| 108 | ఉ | చెందఁగాన్+ఎట్టు (ద్రుతము+అచ్చు) — జగత్+ఈశ (జశ్త్వ) | ఎ-ఈ | ఉ.రామ-5-11 |
| 109 | తే | బుద్ధిన్+ఎఱిఁగె (ద్రుతము+అచ్చు) — శాస్త్రంబులన్+ఎల్ల (ద్రుతము+అచ్చు) [not నె-నె] | ఎ-ఎ | భారత-ఆది-2-161 |
| 110 | క | పురము+ఎక్కడి (ఉత్వ) — య్+ఏ(న్) (యడాగమము+అచ్చు) | ఎ-ఏ | మను-2-15 |
| 111 | తే | య్+ఎలుక (యడాగమము+అచ్చు) — తఱుచునున్+ఏమి (ద్రుతము+అచ్చు) | ఎ-ఏ | మను-4-25 |
| 112 | ఉ | ఏ — ధరణి+ఇంద్ర (సవర్ణదీర్ఘ) | ఏ-ఇ | తి.వేం-చాటువు |
| 113 | ఆ | ఏ — నమస్కరింతున్+ఇంద్ర (ద్రుతము+అచ్చు) | ఏ-ఇ | భాగ-9-134 |
| 114 | ఉ | ఏ — పాదయుగము+ఎప్పుడున్ (ఉత్వ) | ఏ-ఎ | భాగ-2-61 |
| 115 | శా | ఏ — బలంబు+ఏకాదశ (ఉత్వ) | ఏ-ఏ | భారత-ఆది-1-69 |
| 116 | ఉ | ఏ — య్+ఏలర (యడాగమము+అచ్చు) | ఏ-ఏ | మను-3-93 |
| 117 | శా | p1: ఏ — భుజగంబు+ఏ (ఉత్వ) → ఏ-ఏ; p2: తాన్+ఏ (ద్రుతము+అచ్చు) — చెంచు+ఏ (ఉత్వ) → ఏ-ఏ | | శ్రీకాళ.శతకము |
| 118 | శా | నీవు+ఏ (ఉత్వ) — ఒక్క+ఇంత (అత్వ) | ఏ-ఇ | నిర్వ.రామ-8-94 |
| 119 | తే | పలుకకుండిరి+ఏను (ఇత్వ) — పూనెన్+ఇంద్రసుతుఁడు (ద్రుతము+అచ్చు) | ఏ-ఇ | భారత-ఆది-5-224 |
| 120 | ఉ | నన్ను(న్)+ఏలిన (ఉత్వ) — నర+ఈశ్వర (గుణ) | ఏ-ఈ | భారత-ఆది-3-174 |
| 121 | తే | మీఁదన్+ఏల (ద్రుతము+అచ్చు) — అంచు(న్)+ఈవు (ఉత్వ; అనుచున్=అంచున్, sandhi vikalpa; printed form అంచీవు) | ఏ-ఈ | కాశీ-7-127 |
| 122 | క | p2: అపూర్వంబు+ఏయది (ఉత్వ) — వినినన్+ఎఱుక (ద్రుతము+అచ్చు) → ఏ-ఎ; p4: నిబర్హణము+ఏయది (ఉత్వ) — వినఁగన్+ఇష్టము (ద్రుతము+అచ్చు) → ఏ-ఇ | | భారత-ఆది-1-30 |
| 123 | శా | నారాయణుండు+ఏతత్ (ఉత్వ) — వాఁడు+ఎందుండు (ఉత్వ) | ఏ-ఎ | భాగ-7-271 |
| 124 | తే | లోలన్+ఏలన్ (ద్రుతము+అచ్చు; ఏలన్ = జోలపాటను) — ఋషి | ఏ-ఋ | భీమ-2-59 |
| 125 | సీ | ఋ — చూడన్+ఇందుధరుఁడు (ద్రుతము+అచ్చు) | ఋ-ఇ | భీమ-6-19 |
| 126 | చ | ఋ — దేవతాగణములు+ఎంతయు (ఉత్వ) | ఋ-ఎ | నిర్వ.రామ-2-87 |
| 127 | తే | ఋ — సంరంభము+ఎసఁగ (ఉత్వ) | ఋ-ఎ | భీమ-4-181 |
| 128 | తే | ఋ — భక్తిన్+ఎదురుకొనియె (ద్రుతము+అచ్చు) | ఋ-ఎ | హర-4-55 |
| 129 | తే | ఋ — తేజంబులు+ఏకభావ (ఉత్వ) | ఋ-ఏ | మార్క-7-76 |
| 130 | తే | య్+ఎ — ఋ | ఎ-ఋ | భారత-ద్రో-5-25 |
| 131 | చ | ఉ — శిఖా+ఉత్కలిత (గుణ) | ఉ-ఉ | భారత-ఆది-8-230 |
| 132 | తే | ఉ — వృద్ధునాన్+ఉండెనేని (ద్రుతము+అచ్చు) | ఉ-ఉ | భారత-సభా-2-25 |
| 133 | తే | ఉ — నిష్ఠితుఁడు+ఊర్ధ్వ (ఉత్వ) | ఉ-ఊ | భారత-ఆది-4-32 |
| 134 | ఆ | ఉ — కప్పురంబున్+ఒక్క (ద్రుతము+అచ్చు) | ఉ-ఒ | వేమన పద్యము |
| 135 | మ | ఉ — య్+ఒప్పారు (యడాగమము+అచ్చు) | ఉ-ఒ | మను-3-59 |
| 136 | చ | ఉ — కయ్యమునకు(న్)+ఓర్వఁగ (ఉత్వ) | ఉ-ఓ | భారత-విరా-5-186 |
| 137 | ఉ | ప్రభావ+ఉన్నతి (గుణ) — పునః+ఉద్భవ (విసర్గ) | ఉ-ఉ | నిర్వ.రామ-5-19 |
| 138 | సీ | సంవిత్+ఉపలబ్ధి (జశ్త్వ) — నామంబులు+ఒంది (ఉత్వ) | ఉ-ఒ | భారత-అశ్వ-2-135 |
| 139 | ఉ | భాక్+ఉన్నత (జశ్త్వ) — కొలువు+ఉండి (ఉత్వ) | ఉ-ఉ | వసు-5-58 |
| 140 | క | దర్పంబు+ఉడిగించెదన్ (ఉత్వ) — చూచుచు(న్)+ఉండుఁడు (ఉత్వ) | ఉ-ఉ | భారత-ఆది-7-193 |
| 141 | క | మర్త్య+ఉదయ (గుణ) — చెప్పము+ఒగిన్ (ఉత్వ) | ఉ-ఉ | భారత-ఆది-3-58 |
| 142 | శా | శాస్త్ర+ఉపాధ్యాయువి (గుణ) — మేలు+ఓహో (ఉత్వ) | ఉ-ఓ | మను-2-64 |
| 143 | చ | పేరు+ఉలివు (ఉత్వ) — పృథుతర+ఉరుతర (గుణ) | ఉ-ఉ | కుమార-11-66 |
| 144 | మ | ఇష్ట+ఉదకాంతః (printed "ఉత్వ"; reads as గుణ) — మధ్య+ఉపస్థిత (గుణ) | ఉ-ఉ | శృం.నై-8-191 |
| 145 | మ | నాకు(న్)+ఉడురాజ (ఉత్వ) — ఈన్+ఉన్నాఁడు (ద్రుతము+అచ్చు) | ఉ-ఉ | కాశీ-4-50 |
| 146 | సీ | తపమునన్+ఉన్న (ద్రుతము+అచ్చు) — గురులపైన్+ఉరగ (ద్రుతము+అచ్చు) [not ను-ను] | ఉ-ఉ | భారత-ఆది-2-179 |
| 147 | తే | య్+ఉడుప (యడాగమము+అచ్చు) — కుందేళ్ళన్+ఉందురువుల (ద్రుతము+అచ్చు) | ఉ-ఉ | మను-4-51 |
| 148 | ఆ | జమదగ్నికి(న్)+ఉద్భవించి (ఇత్వ) — ఇరువది+ఒక్క (ఇత్వ) | ఉ-ఒ | భారత-శాం-2-44 |
| 149 | సీ+తే | రంగులీనన్+ఉపనిషత్తులు (ద్రుతము+అచ్చు) — య్+ఓలగింప (యడాగమము+అచ్చు) | ఉ-ఓ | మను-1-5 |
| 150 | తే | ఊ — ప్రేవు+ఉరివి (ఉత్వ) | ఊ-ఉ | భారత-శాం-3-499 |
| 151 | తే | ఊ — మానవులు+ఉండునట్టి (ఉత్వ) | ఊ-ఉ | భారత-అశ్వ-1-184 |
| 152 | సీ | ఊర్ధ్వ — లోకమునకున్+ఊర్జిత (ద్రుతము+అచ్చు) | ఊ-ఊ | భారత-మౌ-86 |
| 153 | తే | ఊ — య్+ఊళ్ళకుఱికి (యడాగమము+అచ్చు) | ఊ-ఊ | మను-5-26 |
| 154 | ఉ | ఊ — చందమునన్+ఒక్కట (ద్రుతము+అచ్చు) | ఊ-ఒ | మను-4-79 |
| 155 | ఉ | రంభా+ఊరు(న్) (గుణ) — నిజోరుదేశమునన్+ఉండఁగన్ (ద్రుతము+అచ్చు) | ఊ-ఉ | భారత-సభా-2-249 |
| 156 | తే | య్+ఊడిగంబులు (యడాగమము+అచ్చు) — కైకొంచున్+ఉన్న (ద్రుతము+అచ్చు) | ఊ-ఉ | కళా-2-15 |
| 157 | క | నవ+ఊఢా (printed "ఉత్వ") — వేడుక+ఒసఁగెన్ (అత్వ) | ఊ-ఒ | వి.వి-3-223 |
| 158 | మ | ఒ — విదర్భదేశమునయందు(న్)+ఉద్భూతమై (ఉత్వ) | ఒ-ఉ | శృం.నై-3-18 |
| 159 | మ | ఒ — మనములోన్+ఊహింపుచున్ (ద్రుతము+అచ్చు) | ఒ-ఊ | భాగ-8-123 |
| 160 | మ | ఒ — కర్ణములలోన్+ఒయ్యారమై (ద్రుతము+అచ్చు) | ఒ-ఒ | భాగ-9-141 |
| 161 | చ | ఒ — య్+ఒక్కఁడు (యడాగమము+అచ్చు) | ఒ-ఒ | పాండు-4-264 |
| 162 | క | నెయ్యంబు+ఒందఁగన్ (ఉత్వ) — చేయుచు(న్)+ఉండఁగన్ (ఉత్వ) | ఒ-ఉ | భారత-ఆది-8-181 |
| 163 | తే | కొలఁకులు+ఒక్క (ఉత్వ) — పెక్కు+ఉపవనములు (ఉత్వ) | ఒ-ఉ | కాశీ-7-206 |
| 164 | మధ్యాక్కర | రూపవు+ఒనరన్ (అత్వ) — అన్నన్+ఒడఁబడి (ద్రుతము+అచ్చు); Nannaya's madhyākkara yati = first akshara of gana 5 [7.63] | ఒ-ఒ | భారత-ఆది-4-142 |
| 165 | ఉ | p2: ప్రగాఢముష్టిన్,ఒక్క+ఒక్కని (అత్వ) — అవియన్+ఒక్కొక (ద్రుతము+అచ్చు) → ఒ-ఒ; p4: ..న్+ఒక్కొకరుండ (ద్రుతము+అచ్చు) — కూలిరి,ఉసుఱు+ఒక్కట (ఉత్వ) → ఒ-ఒ | | హరి-పూర్వ-6-168 |
| 166 | క | య్+ఒడళ్ళతో (యడాగమము+అచ్చు) — రెండున్+ఒకటియు (ద్రుతము+అచ్చు) | ఒ-ఒ | మను-4-21 |
| 167 | క | ఇనుఁడు+ఒనరఁగన్ (ఉత్వ) — ఏఁగన్+ఓడఁడె (ద్రుతము+అచ్చు) | ఒ-ఓ | భారత-ఆది-2-158 |
| 168 | చ | ఓ — కలశ+ఉదధి (గుణ) | ఓ-ఉ | శృం.నై-3-63 |
| 169 | ఉ | ఓ — కలశ+ఉదధి (గుణ) | ఓ-ఉ | మను-1-70 |
| 170 | చ | ఓ — శకల+ఉపమ (గుణ) | ఓ-ఉ | పారి-1-135 |
| 171 | శా | ఓ — మీరు+ఊహింపుఁడా (ఉత్వ) | ఓ-ఊ | భాగ-1-289 |
| 172 | ఉ | ఓ — ప్రథమము+ఒల్కెడు (ఉత్వ) (ఓహరిసాహరిన్ = తండోపతండముగా) | ఓ-ఒ | ఆముక్త-4-93 |
| 173 | ఉ | ఓ — య్+ఓ (యడాగమము+అచ్చు) | ఓ-ఓ | భాగ-8-92 |
| 174 | ఆ | భంగికి(న్)+ఓహటించి (ఇత్వ) — పాఱుచు(న్)+ఉన్నారు (ఉత్వ) (ఓహటించి = భయపడి; analysis on p. 281, see yathi2.md) | ఓ-ఉ | భారత-క-2-275 |

Statistics of the 174: sandhi labels seen — సవర్ణదీర్ఘ, గుణ, యణాదేశ, పూర్వరూప, అవఙాదేశ, జశ్త్వ, విసర్గ, ఉత్వ, ఇత్వ, అత్వ, ద్రుతము+అచ్చు, యడాగమము+అచ్చు; meters seen — ఉ, చ, మ, శా, క, తే, ఆ, సీ, మధ్యాక్కర; sources — mostly భారతము (Nannaya/Tikkana/Errana), భాగవతము, మనుచరిత్ర, కాశీఖండము, ఆముక్తమాల్యద, రామాయణము, వసుచరిత్ర, కుమారసంభవము, హరివంశము and others.

## Appendix C — reading notes / uncertainties

- The 6.1.1 example verses are hand-transcribed from the scan; the quoted pādas (not the analysis) may carry small errors.
- #144 and #157: the book labels the sandhi "ఉత్వసంధి" where the split shown is Sanskrit అ+ఉ (గుణ would be expected); recorded as printed.
- #174's analysis line is on page 281 (yathi2.md); the row above was completed from it. Example 175 is in yathi2.md.
- Page 253 (5)(ii) cites 5.23 for ద్రుతము at the pāda start; the exact wording of that cross-reference is partly cut in the scan margin.
- The author of *పద్యవిద్య* is not identified on these pages; record it when a title page is found among the other PDFs.
