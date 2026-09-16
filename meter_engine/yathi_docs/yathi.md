### System Architecture and Formal Mechanics of Yati (6.0 – 6.1.2)

* **Vali (వళి):** The very first syllable (అక్షరము) of any poetic line (*pāda*).  
* **Yati-Sthāna (యతిస్థానము):** A metrically predetermined, fixed syllabic or gaṇa coordinate within a line where the caesura must occur.  
* **Yati-Maitri (యతిమైత్రి):** The mandatory phonetic affinity or identity required between the initial syllable (*vali*) and the syllable occupying the *yati-sthāna*.  
* **Core Computational Rule:** For each metered line, $\\text{PhoneticClass}(\\text{Syllable}*1\) \\equiv \\text{PhoneticClass}(\\text{Syllable}*{\\text{YatiSthāna}})$. This matching is satisfied either by absolute identity of the letter (*Prāṇi Yati*) or through membership within an approved phonetic equivalence class (*Maitri*).  
* **Canonical Nomenclature (Appakavi 6.1.2):** Classical prosody uses 11 interchangeable terms for this structural caesura: *వళి (Vali), వడి (Vaḍi), యతి (Yati), విరతి (Virati), విశ్రాంతి (Viśrānti), విశ్రామము (Viśrāmamu), విశ్రమము (Viśramamu), శ్రాంతి (Śrānti), విరమణము (Viramaṇamu), విరమము (Viramamu), విరామము (Virāmamu)*. Appakavi actively uses 10 of these in his treatise, omitting only *విరమము*.

---

### Structural Divergence: Yati vs. Prāsa vs. Sanskrit Yati (6.1.7 – 6.1.8)

| Dimension | Prāsa (ప్రాస) | Telugu Yati (తెలుగు యతి) | Sanskrit Yati (సంస్కృత యతి) |
| :---- | :---- | :---- | :---- |
| **Position** | Strictly the 2nd syllable across lines 1, 2, 3, 4\. |  |  |

| Syllable 1 paired with an internal line coordinate.

| An internal caesura coordinate.

| | **Phonetic Target** | Consonants only; vowels are completely ignored.

| Both consonant and vowel must simultaneously align.

| No phonetic alliteration; purely a metric word boundary.

| | **Word Boundary** | Unrestricted; ignores lexical boundaries.

| Unrestricted; can fall on word-start, word-middle, or word-end.

| Mandatory lexical pause (*padacchēdamu*: *యతిర్విచ్ఛేద సంజ్ఞికా*).

| | **Line Independence** | Dependent; Line 1 sets the rhyme for all 4 lines.

| Strictly line-independent; each line resolves its own yati.

| Line-independent pause.

| | **Preceding Constraints** | Governed by *Prāsa-Pūrvākṣara* metric weight uniformity.

| None; preceding syllables carry no weight constraints.

| None.

|

---

### Coordinate Resolution Across Meter Categories (6.1.6)

* **Sama Vṛttas (Fixed Syllable Offsets):** Determined strictly by an absolute syllable index:  
* *Utpalamāla:* Syllable 1 $\\rightarrow$ Syllable 10\.  
* *Campakamāla:* Syllable 1 $\\rightarrow$ Syllable 11\.  
* *Śārdūlamu:* Syllable 1 $\\rightarrow$ Syllable 13\.  
* *Mattēbhamu:* Syllable 1 $\\rightarrow$ Syllable 14\.  
* **Jāti and Upajāti Meters (Gaṇa-Based Offsets):** Determined by gaṇa indices rather than fixed character counts, accommodating fluctuating syllable lengths:  
* *Āṭaveladi & Tēṭagīti:* Caesura falls on the 1st syllable of the 4th gaṇa (expressed as "3వ గణము మీద యతి").  
* *Kandamu:* Odd lines (1 & 3\) enforce **no Yati rule**. Even lines (2 & 4\) mandate Yati between the line's 1st syllable and the 1st syllable of the 4th gaṇa.  
* *Sēsamu:* Features two completely independent Yati resolutions per line: Line-Half 1 (Gaṇa 1 $\\rightarrow$ Gaṇa 3\) and Line-Half 2 (Gaṇa 5 $\\rightarrow$ Gaṇa 7).  
* *Bahu-Yatulu (Multi-Yati Vṛttas):* Lines containing multiple internal caesuras that must all mutually rhyme (*Sragdhara*: 1-8-15; *Mahāsragdhara*: 1-9-16; *Maṅgalamahāśrī*: 1-9-17). Governed by *Bahu-yati Niyati* (6.30).  
* *Exception:* *Daṇḍakamu* is the sole classical meter completely devoid of both Yati and Prāsa rules.

---

### Phonetic Modifiers at the Yati Junction (6.1.9)

* **Ardhabindu (ఁ):** Has zero functional effect or authority in Yati. Unlike in Prāsa, half-nasals are discarded during scansion: a rhyme of **ఁక $\\rightarrow$ గ** is evaluated strictly as a standard **క $\\rightarrow$ గ** match.  
* **Pūrṇabindu (ం):**  
* *Trailing Bindu:* Appending an anusvāra after a vowel (e.g., **అం $\\rightarrow$ ఆ** or **కం $\\rightarrow$ గ**) does not disrupt the basic vowel/consonant match.  
* *Preceding Bindu (Class Bridge):* When an anusvāra precedes an unvoiced stop, it generates new affinity classes that would otherwise be metrically illegal (e.g., Dental **త** cannot match Nasal **న**, but **ంత** validly rhymes with **న** under *Bindu Yati* 6.12 and *Anunāsika Yati* 6.14).  
* **Visarga (ః):** Operates transparently without impacting consonant/vowel compatibility. In forms like **అంతఃపురము** or **దుఃఖము**, the cluster **ఃఖ** is scanned simply as **ఖ**.  
* **Drutamu (న్):**  
* *Trailing:* An isolated line-break or caesura nasal (**న్**) appended after the yati syllable has no effect on the match.  
* *Preceding:* If a *drutamu* directly precedes the initial syllable or the yati syllable, it alters the consonant cluster, triggering compound sandhi rules (*Saṁyukta Yati* 6.28).

---

### Svara Yati: Foundational Vowel Equivalence Classes (6.2 – 6.2.1)

All vowels in classical Telugu prosody are strictly partitioned into three mutually exclusive equivalence groups (*Svaramaitri Vargamulu*). Any vowel within a class possesses automatic, bidirectional Yati affinity with every other vowel in that same class:

$$\\begin{aligned} \\mathbf{Class\\ 1\\ (A-Varga):} &\\quad {అ,\\ ఆ,\\ ఐ,\\ ఔ} \\ \\mathbf{Class\\ 2\\ (I-Varga):} &\\quad {ఇ,\\ ఈ,\\ ఎ,\\ ఏ,\\ ఋ,\\ ౠ} \\ \\mathbf{Class\\ 3\\ (U-Varga):} &\\quad {ఉ,\\ ఊ,\\ ఒ,\\ ఓ} \\end{aligned}$$

* **Invariable Systemic Law:** This tripartite grouping forms the absolute baseline for the entire prosodic engine. Every consonant Yati (*Vyañjana Yati*) that incorporates a vowel must satisfy these precise group boundaries without exception.

---

### Svara-Pradhāna Yati: Sandhi Resolution Architecture (6.3 – 6.3.9)

When a phonetic compound or sandhi occurs at the Yati coordinate, the metric match is governed by the **initial vowel of the second component word** (*para-padādi svara*), **never** by the resulting consonant or surface-level orthography.

               \[ Compound at Yati Site: Word-1 \+ Word-2 \]

                                    │

               ┌────────────────────┴────────────────────┐

               ▼                                         ▼

         Prāsa Engine                              Yati Engine

   Evaluates strictly the                    Disregards the consonant;

  resulting surface consonant                resolves directly to the

    (Śabda-svarūpamu)                       Para-padādi Svara (Vowel of Word-2)

&nbsp;

**Operational Scenarios and Resolution Logic**

* **Sanskrit Svara Sandhi (6.3):**  
* *Savarnadīrgha Sandhi:* $\\text{వేద} \+ \\text{అర్థ} \= \\text{వేదార్థ}$. The yati syllable falls on **దా**, but the engine matches against **అ** (*Bhāratam*, Ādi 1-66).  
* *Guṇa Sandhi:* $\\text{పరమ} \+ \\text{ఈశ్వర} \= \\text{పరమేశ్వర}$. Evaluated as **ఈ** (Class 2), matching line-initial **ఇ** (*Bhāratam*, Virāṭa 1-27).  
* *Pūrvarūpa Sandhi:* $\\text{విశ్వకర్తే} \+ \\text{అక్షరాయ} \= \\text{విశ్వకర్తేఁక్షరాయ}$. Evaluated as **అ** (Class 1), matching line-initial **ఆ** (*Bhāratam*, Śānti 2-219).  
* **Consonant & Visarga Sandhis (6.3.2):**  
* *Jaśtva Sandhi:* $\\text{దృక్} \+ \\text{అంచల} \= \\text{దృగంచల}$. Evaluated as **అ**, matching line-initial **ఆ** (*Manu Caritra* 3-90).  
* *Visarga Sandhi:* $\\text{చతుః} \+ \\text{అబ్ధి} \= \\text{చతురబ్ధి}$. Evaluated as **అ**.  
* **Telugu Vowel Elision Sandhis (6.3.3):**  
* *Utva Sandhi:* $\\text{భూమిసురుఁడు} \+ \\text{అంబర} \= \\text{భూమిసురుఁడంబర}$. Evaluated as **అ**, matching line-initial **అ** (*Manu Caritra* 2-3).  
* *Itva Sandhi:* $\\text{నాది} \+ \\text{ఐన} \= \\text{నాదైన}$. Evaluated as **ఐ**, matching line-initial **అ** (*Bhāratam*, Ādi 5-224).  
* *Atva Sandhi:* $\\text{పాలనున్న} \+ \\text{అప్పుడు} \= \\text{పాలనున్నప్పుడు}$. Evaluated as **అ**, matching line-initial **అ** (*Bhāratam*, Sabhā 2-13).  
* **Druta-Vowel Combinations (6.3.4):**  
* When an inflected drutamu fuses with a following vowel ($\\text{న్} \+ \\text{Vowel}$), the engine maps the resulting syllable (**న, నా, ని, ను**) purely to that **Vowel**, prohibiting any consonant match with **'న'**\!  
* *Example:* $\\text{నగరిలోన్} \+ \\text{ఆ} \= \\text{నగరిలోనా}$. Evaluated as **ఆ**, matching line-initial **అ** (*Bhāgavatam* 8-95).  
* *Example:* $\\text{సేరుటకున్} \+ \\text{ఎద్ది} \= \\text{సేరుటకునెద్ది}$. Evaluated as **ఎ**, matching line-initial **ఏ** (*Manu Caritra* 2-49).  
* **Yaḍāgama Augments (6.3.5):**  
* When a glide augment fuses with a vowel ($\\text{య్} \+ \\text{Vowel}$), the engine maps the resulting syllable (**య, యా, యి**) purely to that **Vowel**, prohibiting any consonant match with **'య'**\!  
* *Example:* $\\text{తరుణి} \+ \\text{య్} \+ \\text{అమ్ముని} \= \\text{తరుణి యమ్ముని}$. Evaluated as **అ**, matching line-initial **అ** (*Bhāratam*, Ādi 4-44).  
* **Bidirectional Sandhi Matching (Pādārambha Sandhi 6.3.6):**  
* If a sandhi occurs across the first two syllables of the line, the initial coordinate itself resolves to its underlying *para-padādi svara*.  
* *Compound-to-Compound Example:* Line opens with $\\text{భాషా} \+ \\text{అపర} \= \\text{భాషాపర}$ (resolves to **అ**) and caesura falls on $\\text{వివిధ} \+ \\text{అధ్వర} \= \\text{వివిధాధ్వర}$ (resolves to **అ**) $\\rightarrow$ perfectly satisfies an **అ $\\rightarrow$ అ** Svara Yati (*Manu Caritra* 1-51).  
* *Druta-to-Sandhi Example:* Line opens with $\\text{దేశాళితోన్} \+ \\text{ఆది}$ (resolves to **ఆ**) and caesura falls on $\\text{అజితుండు} \+ \\text{ఐ}$ (resolves to **ఐ**) $\\rightarrow$ validly satisfies an **ఆ $\\rightarrow$ ఐ** Class 1 Svara Yati (*Bhāratam*, Ādi 4-8).

---

### Structural Inventory of Appakavi's 41 Yatis (6.1.3 – 6.1.5)

                       Appakavi's 41 Yati Taxonomy

                                    │

       ┌──────────────┬─────────────┴──────────────┬──────────────┐

       ▼              ▼                            ▼              ▼

  Svara Yatulu   Vyañjana Yatulu             Ubhaya Yatulu    Prāsa Yati

    (7 Rules)      (21 Rules)                  (12 Rules)       (1 Rule)

   Pure Vowels    Consonants &               Dual Sandhi/     Functional

   \[Sec 6.2\]      Class Alliteration         Vowel Rhymes     Caesura Rhyme

\`\`\`\[cite: 3\]

&nbsp;

1\. \*\*Svara Yatulu (7 Vowel Classes)\[cite: 3\]:\*\*

   \* \*6.2.1 Svaramaitri Vali (స్వరమైత్రి వళి)\*\[cite: 3\]

   \* \*6.3 Svarapradhāna Vali (స్వరప్రధాన వళి)\*\[cite: 3\]

   \* \*6.4 Luptavisargakasvara Vali (లుప్తవిసర్గకస్వర వళి)\*

   \* \*6.5 R̥ Vali (ఋ వళి)\*

   \* \*6.6 R̥tvasambandha Vali (ఋత్వసంబంధ వళి)\*

   \* \*6.7 R̥tvasāmya Vali (ఋత్వసామ్య వళి)\*

   \* \*6.8 Vr̥ddhi Vali (వృద్ధి వళి)\*\[cite: 3\]

2\. \*\*Vyañjana Yatulu (21 Consonant Classes)\[cite: 3\]:\*\* Covering identity (\*Prāṇi\* 6.10), varga-affinity (\*Vargaja\* 6.11), bindu-governed alignments (6.12–6.15), and phonetic series\[cite: 3\].

3\. \*\*Ubhaya Yatulu (12 Dual/Permissive Classes)\[cite: 3\]:\*\* Governing junctions where the poet is granted the choice to align with either the consonant or the underlying sandhi vowel\[cite: 3, 3\].

4\. \*\*Prāsa Yati (1 Meta-Rule):\*\* The authorized structural substitution of a second-syllable rhyme in place of standard Yati, restricted strictly to \*Sēsamu\*, \*Tēṭagīti\*, \*Āṭaveladi\*, and long \*Uddhuramāla\* meters (\*Layagrāhi\*, etc.)\[cite: 3\].

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.3.10 'ఋ' వర్ణముతో యతులు (R̥-Varṇa Svara Yati Mechanics)

* **Independent Lexical Occurrence:** While most vowels appear isolated only at line starts and merge via sandhi elsewhere, the vocalic vowel **'ఋ'** (*R̥*) frequently occurs as an independent lexical onset without undergoing compounding (e.g., *వాఁడు ఋషి*, *చేసిన ఋణము*, *పలికిన ఋతము*).  
* **Equivalence Class (Class 2 / I-Varga):** In the foundational vowel taxonomy (Section 6.2.1), **'ఋ'** is grouped strictly under the **'ఇ' వర్గము** along with **ఇ, ఈ, ఎ, ఏ, ౠ**.  
* **Direct Svara Yati Pairings:** Independent **'ఋ'** directly and bidirectionally rhymes with any member of Class 2 (**ఇ, ఈ, ఎ, ఏ, ఋ**):  
* **ఇ $\\leftrightarrow$ ఋ:** *ఇంద్రేశ తీర్థంబు ఋషిసమాకీర్ణంబు...* (*Kāśīkhaṇḍam* 2-74)  
* **ఈ $\\leftrightarrow$ ఋ:** *ఈశ్వరద్రోహి గర్వాంధ ఋషిసురేంద్ర...* (*Bhāratam*, Śānti 7-95)  
* **ఋ $\\leftrightarrow$ ఋ:** *ఋణములును మఱి పితరుల ఋణము దేహ...* (*Bhāratam*, Ādi 5-71)  
* **Svara-Pradhāna Compounding with 'ఋ':**  
* When **'ఋ'** is the *para-padādi svara* (initial vowel of the second word in a compound like *మాతృ \+ ఋణము \= మాతౄణము* or *దేవ \+ ఋషి \= దేవర్షి*), the compound junction is evaluated strictly as **'ఋ'**.  
* *Example:* Line opens with **ఎ** and caesura lands on **మాతౄణము** $\\rightarrow$ evaluated as an **ఎ $\\leftrightarrow$ ఋ** match under Class 2 Svara Yati.

---

### 6.4 లుప్తవిసర్గక స్వరయతి / గూఢస్వరయతి (Lupta-Visargaka / Gūḍha Svara Yati)

* **Phonetic & Morphological Environment:** Occurs exclusively in Sanskrit compounds where a first word ending in short *'a'* \+ visarga (or *as*, e.g., *దాసః / దాసస్, మనస్, తపస్*) combines with a second word beginning with a short *'a'* (e.g., *అహమ్, అబ్జ, అనల*).  
* **Underlying Sandhi Mechanics (Pāṇinian Svādi Sandhi):**  
1. Root base takes nominative singular: $\\text{దాస} \+ \\text{సు} \\rightarrow \\text{దాసస్}$.  
2. Final *'s'* undergoes rutva by *Sasajuṣō ruḥ* (8-2-66): $\\text{దాసస్} \\rightarrow \\text{దాసర్}$.  
3. The repha changes to *'u'* before short *'a'* by *Atō rōraplutādaplutē* (6-1-113): $\\text{దాస్} \+ \\text{అ} \+ \\text{ఉ} \+ \\text{అహమ్}$.  
4. Guṇa sandhi merges $a \+ u \\rightarrow o$: $\\text{దాస్} \+ \\text{ఓ} \+ \\text{అహమ్}$.  
5. Pūrvarūpa sandhi by *Ēṅaḥ padāntādati* (6-1-109) absorbs the following *'a'* into *'o'*, marked orthographically by an avagraha (ఽ): $\\text{దాసోఁహమ్}$ (*dāsō'ham*).  
* **The Yati Rule:** When a caesura lands on this resulting syllable (**సో, నో, పో, తో, ధో, రో**, etc.), the rhyme **disregards the surface consonant and the 'o' vowel**; it matches strictly against the underlying, absorbed short vowel **'అ'** (*para-padādi svara*)\!  
* **Provenance Examples:**  
* *Bhāratam* (Anuśāsanika 4-180): **సోఁహమనిన కాన్పు రుద్ర యతనిఁ గనుటగున్** ($\\text{సః} \+ \\text{అహమ్} \\rightarrow \\text{సోఁహమ్}$ matches with $\\text{య్} \+ \\text{అతనిన్} \\rightarrow \\mathbf{అ \\leftrightarrow అ}$).  
* *Manu Caritra* (3-184): **అని ప్రియభాషణంబుల మనోఁబ్జము...** (Line-start **అ** matches $\\text{మనస్} \+ \\text{అబ్జ} \\rightarrow \\text{మనోఁబ్జ}$ via underlying $\\mathbf{అ \\leftrightarrow అ}$).  
* *Bhāgavatam* (10-Pūrvabhāga-1): **...వక్షోఁలంకార మణిప్రకాండము నవీనార్కుండుగా...** ($\\text{వక్షస్} \+ \\text{అలంకార}$ matches **నవీన \+ అర్క** via $\\mathbf{అ \\leftrightarrow అ}$).  
* *Gōpīnātha Rāmāyaṇamu* (Sundara 1356): **...వచోఁమృతధారల...** ($\\text{వచస్} \+ \\text{అమృత}$ matches underlying **అ**).

#### Special Sub-Case: 'అన్యోన్య' (Anyōnya) Yati (6.4.3 – 6.4.4)

* **Grammatical Formation:** Formed under semantic reciprocal action (*karma-vyatihāra* via Pāṇini 8-1-12 vartikas). The reduplicated base $\\text{అన్యమ్} \+ \\text{అన్యమ్}$ replaces the first case ending with nominative *su* ($\\text{అన్యస్} \+ \\text{అన్య}$), proceeding through rutva and pūrvarūpa into **అన్యోన్య** (*anyō'nya*).  
* **Caesura Behavior:** Caesura on the cluster **'న్యో'** (*nyō*) is resolved as an underlying short **'అ'**.  
* **Examples:**  
* *Bhāratam* (Ādi 1-80): **అమరశ్రేణికి దైత్యసంతతికినన్యోన్యాహవంబు...** (Line-start **అ** matches **అన్యోన్య** via $\\mathbf{అ \\leftrightarrow అ}$).  
* *Appakavīyamu* (3-21 citation of *Bhāratam*, Udyōga 1-32): **...పుచ్చికొందమన్యోన్య విరుద్ధ భాషణములాడినఁ...** (**అన్యోన్య** matches **ఆడినన్** via $\\mathbf{అ \\leftrightarrow ఆ}$).

#### Theoretical Dispute: Appakavi vs. Anantudu (6.4.5 – 6.4.6)

* **Appakavi's Framing Error (3-17):** Appakavi stated that the resulting *ō-kāra* matches with letters **'అ, య, హ'** (*"అమరునోత్వంబునకుఁ జెల్లు నయహ లిపులు"*). Commentators point out a structural contradiction: **'ఓ'** belongs to Class 3 (U-varga) and cannot phonetically rhyme with Class 1 **'అ'**.  
* **Anantudu's Correction (*Chandodarpaṇam* 1-86):** Anantudu correctly identifies that the match is not directed at the *ō-kāra*, but at the underlying hidden short vowel *'a'*, formally designating the rule as **గూఢస్వర యతి (Gūḍha Svara Yati — Hidden Vowel Yati)**.  
* **Why "Gūḍha Svara" is Acoustically Accurate:** In *vētārtha* ($a \+ a \= \\bar{a}$), the resulting vowel is homogeneous (*savarṇa*). In *dāsō'ham* ($o \+ a \= o$), the resulting surface vowel **'ఓ'** is non-homogeneous with the elided **'అ'**. Because the *'a'* remains phonetically concealed (*gūḍhamu*) within the *ō-kāra*, *Gūḍha Svara Yati* is the accurate scientific term.

#### Strict Negative Constraint (6.4.7)

* When a word-final visarga / *'as'* turns into **'ఓ'** before a **voiced consonant** (e.g., $\\text{యశస్} \+ \\text{నాశము} \= \\text{యశోనాశము}$; $\\text{మనస్} \+ \\text{రథము} \= \\text{మనోరథము}$; $\\text{అంభస్} \+ \\text{యాన} \= \\text{అంభోయాన}$), **this rule does not apply**.  
* There is no elided vowel *'a'*; the caesura must be matched as a standard consonant yati on the surface consonant (**శో, నో, భో**).

---

### 6.5 'ఋ' యతి / రివడి (R̥ Yati / Ri-Vaḍi)

* **Definition:** A prosodic bridge allowing the vocalic vowel **'ఋ'** (*R̥*) to rhyme directly with consonantal repha (**ర్** / *r*) combined with vowels of Class 2 (**ఇ, ఈ, ఎ, ఏ**).  
* **Canonical Affinity Set:**

$$\\mathbf{‘ఋ’} \\quad\\longleftrightarrow\\quad {\\mathbf{రి,\\ రీ,\\ రె,\\ రే}}$$

* **Phonetic Rationale:**  
1. *Acoustic Articulation:* Pronouncing the vocalic vowel *R̥* generates a dental/retroflex trill identical to *repha*.  
2. *Vowel Class Harmony:* By grouping rules (6.2.1), *R̥* belongs to Class 2 (I-varga: *ఇ, ఈ, ఎ, ఏ, ఋ*); combining consonant *repha* with the other members of its own vowel class creates exact acoustic resonance.

                 Tripartite Acoustic Bridge of 'ఋ' Yati

    \[ ఋ (Vocalic Vowel) \] \<──────── Phonetic Trill ────────\> \[ ర్ (Consonant Repha) \]

              │                                                         │

              ▼                                                         ▼

      Member of Class 2                                        Bound to Class 2 Vowels

    { ఇ,  ఈ,  ఎ,  ఏ,  ఋ }                                        { ఇ,  ఈ,  ఎ,  ఏ }

              │                                                         │

              └──────────────── Fully Harmonized Set ───────────────────┘

                               { రి,  రీ,  రె,  రే }

\`\`\`\[cite: 4\]

&nbsp;

\#\#\#\# Category 1: కేవల 'ఋ' వర్ణము (Pure Standalone R̥) (6.5.1)

\* Matches standalone \*\*'ఋ'\*\* with \*\*రి, రీ, రె, రే\*\* across base words and complex consonant clusters\[cite: 4\]:

  \* \*\*ఋ $\\leftrightarrow$ రి:\*\* \*ఋత్విజుండని విచారించి పూజించితే...\* (\*Bhāratam\*, Sabhā 2-11)\[cite: 4\]

  \* \*\*ఋ $\\leftrightarrow$ రీ:\*\* \*ఋష్యసారంగమృగ చమరీమృగముల...\* (\*Bhāgavatam\* 3-89)\[cite: 4\]

  \* \*\*ఋ $\\leftrightarrow$ రె:\*\* \*ఋషివంటి నన్నయ్య రెండవ వాల్మీకి...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 29)\[cite: 4\]

\* \*\*Extension to Conjunct Clusters:\*\* When \*\*రి, రీ, రె, రే\*\* appear within a consonant cluster (whether repha is the first or second consonant), \*Saṁyukta Yati\* (6.26) permits isolating the repha component to satisfy \*R̥ Yati\*\[cite: 4\]:

  \* \*Repha as 1st Consonant:\* \*\*ఋ $\\leftrightarrow$ ర్చి\*\* (in \*యర్చించి\*, matches $\\text{ర్} \+ \\text{ఇ} \= \\text{రి}$)\[cite: 4\].

  \* \*Repha as 2nd Consonant:\* \*\*ఋ $\\leftrightarrow$ త్రీ\*\* (in \*ధరిత్రీ\*, matches $\\text{ర్} \+ \\text{ఈ} \= \\text{రీ}$)\[cite: 4\]; \*\*బ్రీ $\\leftrightarrow$ ఋ\*\* (in \*ప్రీతిమై\*, matches $\\text{ర్} \+ \\text{ఈ} \= \\text{రీ}$)\[cite: 4\].

&nbsp;

\#\#\#\# Category 2: హల్లుతో కూడిన 'ఋ' వర్ణము / వట్రసుడి (Consonant \+ R̥) (6.5.2)

\* Applies when \*\*'ఋ'\*\* is attached to any consonant as a subscript curl (\*vaṭrasuḍi\* / వట్రువసుడి: \*\*కృ, గృ, ఘృ, దృ, నృ, పృ, బృ, భృ, మృ, వృ\*\*, etc.)\[cite: 4\].

\* The consonant is bypassed, and the underlying vocalic \*vaṭrasuḍi\* rhymes freely with \*\*రి, రీ, రె, రే\*\* or clusters containing them\[cite: 4\]:

  \* \*\*నృ (ఋ) $\\leftrightarrow$ రి:\*\* \*నృపవరేణ్యుఁడిట్లు రిపుఁబట్టువఱిచి...\* (\*Bhāratam\*, Śalyā 2-57)\[cite: 4\]

  \* \*\*మృ (ఋ) $\\leftrightarrow$ రి:\*\* \*మృగయులందఱుఁజనివెల్వరించి...\* (\*Manu Caritra\* 4-48)\[cite: 4\]

  \* \*\*కృ (ఋ) $\\leftrightarrow$ రీ:\*\* \*కృతి యొక బెబ్బులింబలె శరీర...\* (\*Manu Caritra\* 1-61)\[cite: 4\]

  \* \*\*రె $\\leftrightarrow$ దృ (ఋ):\*\* \*రెండవ నాకలోకమన దృష్టికినింపొనరించెనెంతయున్...\* (\*Haravilāsam\* 4-258)\[cite: 4\]

  \* \*\*కృ (ఋ) $\\leftrightarrow$ రే:\*\* \*కృష్ణుఁడందిష్టగోష్ఠినా రేయి గడపి...\* (\*Bhāratam\*, Sabhā 2-87)\[cite: 4\]

\* \*\*Cluster-to-Cluster Matching:\*\* A consonant taking a \*vaṭrasuḍi\* can rhyme with another distinct consonant cluster containing a repha\[cite: 4\]:

  \* \*\*కృ (ఋ) $\\leftrightarrow$ ప్రి (రి):\*\* \*కృతివినిర్మింపుమిఁక మాకుఁ బ్రియముకాగ...\* (\*Manu Caritra\* 1-13)\[cite: 4\]

  \* \*\*వృ (ఋ) $\\leftrightarrow$ శ్రీ (రీ):\*\* \*వృతమగుసేతుమండలము శ్రీఁబరివేషము...\* (\*Bhāratam\*, Virāṭa 4-97)\[cite: 4\]

  \* \*\*కృ (ఋ) $\\leftrightarrow$ శ్రే (రే):\*\* \*...దీపాంకురాకృతి... శ్రేణిచ్ఛిదం జేయుతన్...\* (\*Bhāratam\*, Ādi 1-9)\[cite: 4\]

  \* \*\*కృ (ఋ) $\\leftrightarrow$ ర్మి (రి):\*\* \*కృష్ణరాయేంద్ర కృతి వినిర్మింపుమనిరి...\* (\*Amuktamālyada\* 1-44)\[cite: 4\]

&nbsp;

\#\#\#\# The Metrical Marvel of Vaṭrasuḍi (మహత్త్వము) (6.5.3)

\* In standard Telugu metric scansion, vowels bound to consonants cannot be detached to claim an independent vowel rhyme (e.g., \*\*క\*\* \[$\\text{క్} \+ \\text{అ}$\] cannot rhyme with standalone \*\*అ\*\*; \*\*కి\*\* cannot rhyme with standalone \*\*ఇ\*\*)\[cite: 4\]. The consonant and vowel must match together\[cite: 4\].

\* \*\*The Unique Exception:\*\* The subscript vocalic vowel \*\*'ఋ'\*\* (\*vaṭrasuḍi\*) is the \*\*only vowel in the language\*\* permitted to ignore its host consonant entirely and project an independent rhyme across the line to a consonantal repha set (\*\*రి, రీ, రె, రే\*\*)\[cite: 4\].

\* Appakavi marvels at this structural anomaly as an inherent divine mystery (\*Mahattvamu\* / మహత్త్వము) of prosody (\*Appakavīyamu\* 3-22)\[cite: 4\]:

  \> \*క॥ ఇత్వైత్వంబులఁ దొలఁగక, ఋత్వంబును ఋవళి యనఁగ రేఫముతో మి\*  

  \> \*త్రత్వంబు నెఱపునట్టి మ,హత్త్వమొ యట్లయగుఁ గాదులందున్నపుడున్\*\[cite: 4\]

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (6.5.4 Summary)

&nbsp;

| Input Coordinate 1 (\*Vali\*) | Input Coordinate 2 (\*Yati-Sthāna\*) | Evaluated Phonetic Value | Valid Engine Match? |

| :--- | :--- | :--- | :--- |

| \*\*ఋ\*\* (Standalone) | \*\*రి / రీ / రె / రే\*\* (Simple) | $R̥ \\longleftrightarrow R \+ \\{i, \\bar{i}, e, \\bar{e}\\}$ | \*\*VALID\*\* (\*Kēvala ఋ-Yati\*)\[cite: 4\] |

| \*\*ఋ\*\* (Standalone) | \*\*ర్చి / త్రీ / బ్రీ\*\* (Cluster) | $R̥ \\longleftrightarrow R \+ \\{i, \\bar{i}, e, \\bar{e}\\}$ (Extracted) | \*\*VALID\*\* (\*Saṁyukta ఋ-Yati\*)\[cite: 4\] |

| \*\*కృ / గృ / దృ\*\* (\*Vaṭrasuḍi\*) | \*\*రి / రీ / రె / రే\*\* (Simple) | $R̥\\text{ (Extracted)} \\longleftrightarrow R \+ \\{i, \\bar{i}, e, \\bar{e}\\}$ | \*\*VALID\*\* (\*Vaṭrasuḍi ఋ-Yati\*)\[cite: 4\] |

| \*\*కృ / మృ / వృ\*\* (\*Vaṭrasuḍi\*) | \*\*ప్రి / శ్రీ / శ్రే / ర్మి\*\* (Cluster) | $R̥\\text{ (Extracted)} \\longleftrightarrow R \+ \\{i, \\bar{i}, e, \\bar{e}\\}$ (Extracted) | \*\*VALID\*\* (\*Ubhayasaṁyukta ఋ-Yati\*)\[cite: 4\] |

| \*\*కృ / గృ\*\* (\*Vaṭrasuḍi\*) | \*\*రు / రూ / ర / రా\*\* (Non-Class 2\) | $R̥ \\longleftrightarrow R \+ \\{u, \\bar{u}, a, \\bar{a}\\}$ | \*\*INVALID\*\* (Breaches Class 2 Vowel Boundary)\[cite: 4\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.6 ఋత్వ సంబంధ యతి (R̥tva Sambandha Yati — Consonant-Bound R̥-to-Vowel Yati)

* **Definition & Mechanics:** When a consonant is bound to vocalic *'R̥'* in the form of a subscript curl (*vaṭrasuḍi* / వట్రువసుడి, e.g., **కృ, గృ, దృ, నృ, పృ, మృ, వృ**), the host consonant is disregarded, and the bound *r̥tvamu* is permitted to rhyme directly with any independent vowel of Class 2 (**ఇ, ఈ, ఋ, ౠ, ఎ, ఏ**).  
* **Nomenclature:** Named **ఋత్వసంబంధవళి** by Appakavi.  
* **Theoretical Foundation:** In the primary vowel classification (6.2.1), **'ఋ'** is an intrinsic member of the **'ఇ' వర్గము** (Class 2: *ఇ, ఈ, ఋ, ౠ, ఎ, ఏ*). While matching independent *ఋ* with Class 2 vowels is standard *Svaramaitri Yati*, extending this privilege to a consonant-bound vowel is a unique structural exception.

               \[ Consonant \+ Vaṭrasuḍi (e.g., కృ, గృ, దృ) \]

                                    │

               (Host consonant is bypassed by Yati Engine)

                                    │

                                    ▼

                    \[ Underlying Vocalic Sound: ఋ \]

                                    │

                    (Rhymes with Class 2 Vowel Class)

                                    ▼

                      { ఇ,  ఈ,  ఋ,  ౠ,  ఎ,  ఏ }

\`\`\`\[cite: 5\]

&nbsp;

\* \*\*Absolute Prosodic Exception (మహత్త్వము 6.6.1):\*\*

  \* In all other consonants, an attached vowel cannot be isolated to rhyme with an independent vowel\[cite: 5\]. For instance, \*\*కి\*\* ($\\text{క్} \+ \\text{ఇ}$) cannot rhyme with independent \*\*ఇ, ఈ, ఎ, ఏ\*\*; \*\*క\*\* ($\\text{క్} \+ \\text{అ}$) cannot rhyme with \*\*అ, ఆ\*\*; \*\*కు\*\* ($\\text{క్} \+ \\text{ఉ}$) cannot rhyme with \*\*ఉ, ఊ\*\*\[cite: 5\].

  \* The bound vocalic \*vaṭrasuḍi\* is the sole vocalic element in Telugu prosody endowed with the license to ignore its host consonant and execute a direct vowel caesura (\*Svara Yati\*)\[cite: 5\].

&nbsp;

\#\#\#\# Canonical Provenance & Structural Categories (6.6.2)

&nbsp;

\* \*\*Direct Bound-R̥ to Independent Vowel:\*\*

  \* \*\*ఇ $\\longleftrightarrow$ గృ (ఋ):\*\* \*ఇరుగడలం ద్విరూపములఁ గృష్ణుఁడు...\* (\*Bhāgavatam\* 4-122)\[cite: 5\].

  \* \*\*ఈ $\\longleftrightarrow$ కృ (ఋ):\*\* \*ఈ తరుణాగ్నిహోత్రి కృతకృత్యతఁ జెంది...\* (\*Amuktamālyada\* 4-118)\[cite: 5\].

  \* \*\*ఈ $\\longleftrightarrow$ భృ (ఋ):\*\* \*ఈ సర్వంసహ దేవదానవ మహీభృన్మౌని...\* (\*Bhāgavatam\* 6-48)\[cite: 5\].

  \* \*\*ఎ $\\longleftrightarrow$ నృ (ఋ):\*\* \*ఎఱుఁగవే ధర్మపరుఁడవు నృపకుమార...\* (\*Appakavīyamu\* 3-32 / \*Bhāratam\*, Ādi)\[cite: 5\].

  \* \*\*ఏ $\\longleftrightarrow$ మృ (ఋ):\*\* \*ఏనవిద్యవలన మృత్యువుఁ దరియింప...\* (\*Bhāratam\*, Sabhā 1-158)\[cite: 5\].

  \* \*\*ఏ $\\longleftrightarrow$ వృ (ఋ):\*\* \*ఏనుంగులెనిమిది వృషభంబులెనిమిది...\* (\*Bhāratam\*, Āraṇya 3-64)\[cite: 5\].

  \* \*\*మృ (ఋ) $\\longleftrightarrow$ ఎ:\*\* \*మృతిఁబొందిన వారు నిందలెనసిన వారల్...\* (\*Bhāgavatam\* 6-218)\[cite: 5\].

&nbsp;

\* \*\*Svara-Pradhāna Compounding Intersecting with R̥tva-Sambandha:\*\*

  \* When the initial coordinate resolves via sandhi to an underlying vowel (\*para-padādi svara\*), that resolved vowel matches the bound \*vaṭrasuḍi\*\[cite: 5\]:

  \* \*\*ఇ (via Druta Sandhi) $\\longleftrightarrow$ కృ (ఋ):\*\* \*...నిందుండుమీవని కృష్ణ...\* ($\\text{న్} \+ \\text{ఇందు} \\rightarrow \\text{ఇ} \\longleftrightarrow \\text{కృ}$) (\*Bhāratam\*, Āraṇya 3-97, Madhyākkara)\[cite: 5\].

  \* \*\*ఇ (via Sandhi) $\\longleftrightarrow$ తృ (ఋ):\*\* \*...నిచ్చి యిష్టాన్న సంతృప్తులఁగాఁ...\* ($\\text{న్} \+ \\text{ఇచ్చి} \\rightarrow \\text{ఇ} \\longleftrightarrow \\text{తృ}$) (\*Appakavīyamu\* 3-29)\[cite: 5\].

  \* \*\*ఎ (via Utva Sandhi) $\\longleftrightarrow$ మృ (ఋ):\*\* \*...రహితుఁడెత్తెఱంగున దైవ సమృద్ధిఁ...\* ($\\text{రహితుఁడు} \+ \\text{ఎత్తెఱంగున} \\rightarrow \\text{ఎ} \\longleftrightarrow \\text{మృ}$) (\*Bhāratam\*, Anuśāsanika 5-155)\[cite: 5\].

&nbsp;

\* \*\*Complex Cluster Support (Saṁyuktākṣara):\*\*

  \* When \*vaṭrasuḍi\* is attached to a multi-consonant cluster (e.g., \*\*ష్కృ\*\* \= $\\text{ష్} \+ \\text{క్} \+ \\text{ఋ}$), the entire consonantal cluster is bypassed, resolving purely to \*'ఋ'\*\[cite: 5\]:

  \* \*...నిష్కృతములు నిల్చునే తలఁపనేటికి...\* (\*\*ష్కృ\*\* \[ఋ\] $\\longleftrightarrow$ \*\*ఏ\*\* in \*తలఁపన్ \+ ఏటికి\*) (\*Amuktamālyada\* 5-236)\[cite: 5\].

&nbsp;

\* \*\*Appakavi's Definitive Lakṣya-Lakṣaṇa Stanza (3-27):\*\*

  \* \*ఇనతనూభవుండు పృషదశ్వ సుతునేసె\* (Line 1: \*\*ఇ $\\longleftrightarrow$ పృ\*\* \[ఋ\])\[cite: 5\].

  \* \*ఋభునదీసుతుండు కృష్ణునేసె\* (Line 2: \*\*ఋ $\\longleftrightarrow$ కృ\*\* \[ఋ\])\[cite: 5\].

  \* \*నేమి చెప్పనపుడు దృఢశక్తి శల్యుండు\* (Line 3: $\\text{న్} \+ \\text{ఏమి} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{దృ}$ \[ఋ\])\[cite: 5\].

  \* \*హీనబలుని జేసె వృష్టికులుని\* (Line 4: Sarasayati bridge between \*\*హీ $\\longleftrightarrow$ వృ\*\* \[ఋ\])\[cite: 5\].

&nbsp;

\* \*\*Disambiguation Warnings:\*\* In lines like \*...నిమ్మహాస్థానికనఁదోచె నృపుహజార...\* or \*...కృష్ణు దర్శింపకున్న నాకేమి చిక్కు...\*, scansion engines must not classify these as \*Prāṇi Yati\* (\*\*ని-నృ\*\* or \*\*కృ-కే\*\*); they are structurally governed by \*R̥tva Sambandha Yati\* via the underlying vowels\[cite: 5\].

&nbsp;

\---

&nbsp;

\#\#\# 6.7 ఋత్వసామ్య యతి (R̥tvasāmya Yati — Mutual Vaṭrasuḍi Identity Yati)

&nbsp;

\* \*\*Definition & Mechanics:\*\* Any two syllables that both carry a consonant-bound vocalic \*'R̥'\* (\*vaṭrasuḍi\*) are legally permitted to rhyme with each other, \*\*even if their underlying host consonants possess zero phonetic affinity (\*Vyañjana Maitri\*)\*\*\[cite: 5\]\!

\* \*\*Nomenclature:\*\* Designated \*\*ఋత్వసామ్యవళి\*\* by Appakavi\[cite: 5\].

\* \*\*The Structural Principle:\*\*

  $$\\text{Consonant}\_1 \+ \\mathbf{ఋ} \\quad\\longleftrightarrow\\quad \\text{Consonant}\_2 \+ \\mathbf{ఋ}$$

  The caesura is authenticated solely by the mutual identity and phonetic parity (\*sāmyamu\*) of the two \*vaṭrasuḍi\* markers ($\\mathbf{ఋ \\longleftrightarrow ఋ}$)\[cite: 5\].

\* \*\*Phonetic Justification (6.7.1):\*\*

  \* Vocalic \*'R̥'\* carries a consonantal vocalic trill identical to \*repha\* (\*\*ర్\*\*)\[cite: 5\].

  \* Under \*Saṁyukta Yati\* (6.26), matching any single consonant within a cluster validates the caesura\[cite: 5\]. Because a consonant bound to \*vaṭrasuḍi\* articulates phonetically like a conjunct cluster ($\\text{Host} \+ \\text{Repha-glide}$), the engine is permitted to align the shared \*r̥tva\* elements while disregarding the disparate base consonants\[cite: 5\].

\* \*\*Strict Negative Constraint:\*\* This license exists \*\*exclusively for ఋ\*\*\[cite: 5\]. No other vowel can bridge incompatible consonants:

  \* $\\text{క} \\neq \\text{ప}$ (even though both contain short \*'a'\*)\[cite: 5\].

  \* $\\text{కి} \\neq \\text{పి}$; $\\text{కు} \\neq \\text{పు}$; $\\text{గ} \\neq \\text{శ}$; $\\text{గి} \\neq \\text{శి}$\[cite: 5\].

  \* But \*\*గృ $\\longleftrightarrow$ శృ\*\* is fully authorized under \*R̥tvasāmya Yati\*\[cite: 5\]\!

&nbsp;

\#\#\#\# Canonical Provenance & Structural Categories (6.7.2 – 6.7.3)

&nbsp;

\* \*\*Simple Consonant Pairings (Host Consonants Lacking Affinity):\*\*

  \* \*\*మృ $\\longleftrightarrow$ గృ (M $\\neq$ G):\*\* \*...మృతుని గావించెఁ గంసునిఁ గృష్ణుఁడనఁగ\* (\*Appakavīyamu\* 3-34)\[cite: 5\].

  \* \*\*హృ $\\longleftrightarrow$ మృ (H $\\neq$ M):\*\* \*...హృతమై పిసాళించు మృగమదంబు...\* (\*Manu Caritra\* 2-55)\[cite: 5\].

  \* \*\*భృ $\\longleftrightarrow$ కృ (Bh $\\neq$ K):\*\* \*భృంగీరవంబహంకృతిఁదీఁగె సాగించె...\* (\*Manu Caritra\* 6-29)\[cite: 5\].

  \* \*\*పృ $\\longleftrightarrow$ కృ (P $\\neq$ K):\*\* \*పృతన భవదసిననిఁదెగి కృష్ణరాయ...\* (\*Appakavīyamu\* 3-35 / \*Rāyavācakamu\*)\[cite: 5\].

  \* \*\*గృ $\\longleftrightarrow$ శృ (G $\\neq$ Ś):\*\* \*గృహసమ్మార్జనమో జలాహరణమో శృంగార...\* (\*Appakavīyamu\* 3-36)\[cite: 5\].

  \* \*\*తృ $\\longleftrightarrow$ కృ (T $\\neq$ K):\*\* \*తృట్యమాన పతద్బిసాకృతి వహింప...\* (\*Bhāgavatam\* 8-121)\[cite: 5\].

  \* \*\*ఘృ $\\longleftrightarrow$ నృ (Gh $\\neq$ N):\*\* \*ఘృణికినచ్యుత రఘునాథ నృపతిమణికి...\* (\*Amuktamālyada\* 1-25)\[cite: 5\].

&nbsp;

\* \*\*Textual Critique on Appakavi's Example (6.7.2):\*\*

  \* In verse 3-34, Appakavi pairs \*\*వృ $\\longleftrightarrow$ పృ\*\* (\*వృష్ణవంశాబ్ది... పృథివిఁబుట్టి\*)\[cite: 5\]. Commentators note this is technically an unconvincing illustration of \*R̥tvasāmya\* because \*\*ప\*\* and \*\*వ\*\* already possess natural homorganic affinity under \*Abhēdavarga Yati\* (6.22)\[cite: 5\]. The true demonstration in that stanza is \*\*మృ $\\longleftrightarrow$ గృ\*\* in line 4\[cite: 5\].

&nbsp;

\* \*\*Conjunct Clusters Bound to Vaṭrasuḍi (6.7.3):\*\*

  \* Multi-consonant clusters taking \*vaṭrasuḍi\* ($\\text{Consonant}\_1 \+ \\text{Consonant}\_2 \+ \\text{ఋ}$) freely rhyme with single-consonant \*vaṭrasuḍi\* forms\[cite: 5\]:

  \* \*\*స్కృ $\\longleftrightarrow$ దృ:\*\* \*...సంస్కృతశరీరులును యాదృచ్ఛికముగ...\* (\*\*స్కృ\*\* \= $\\text{స్} \+ \\text{క్} \+ \\text{ఋ} \\longleftrightarrow \\mathbf{దృ}$ \= $\\text{ద్} \+ \\text{ఋ}$) (\*Bhāratam\*, Śānti 4-302)\[cite: 5\].

  \* \*\*స్మృ $\\longleftrightarrow$ వృ:\*\* \*...భూభృద్వలన్మృదువాతంబతి పక్వ పాదప లతా వృంతావళీ...\* (\*\*స్మృ\*\* $\\longleftrightarrow$ \*\*వృ\*\*) (\*Bhāgavatam\* 5-108)\[cite: 5\].

&nbsp;

\---

&nbsp;

\#\#\# 6.8 వృద్ధి యతి (Vr̥ddhi Yati — Dual-Option Caesura in Vr̥ddhi Sandhi)

&nbsp;

\* \*\*Phonetic & Morphological Environment:\*\* Pāṇinian \*Vr̥ddhi Sandhi\* occurs when short or long \*'a'\* combines with diphthongs:

  1\. $a / \\bar{a} \+ \\bar{e} / ai \\longrightarrow \\mathbf{ఐ}$ (\*ai\*)\[cite: 5\]

  2\. $a / \\bar{a} \+ \\bar{o} / au \\longrightarrow \\mathbf{ఔ}$ (\*au\*)\[cite: 5\]

\* \*\*The Dual-Licensing Architecture:\*\* In all other Sanskrit and Telugu vowel sandhis, prosody strictly enforces \*Svara-Pradhāna Yati\* (matching exclusively the \*para-padādi svara\*, the initial vowel of word 2)\[cite: 5\]. Vr̥ddhi Sandhi is granted a specialized dual-license (\*Ubhayasvara Yati\*)\[cite: 5\]:

&nbsp;

&nbsp;

                   Vr̥ddhi Sandhi at Yati Coordinate

                                  │

    ┌─────────────────────────────┴─────────────────────────────┐

    ▼                                                           ▼

&nbsp;

Option A: వృద్ధి యతి                               Option B: స్వరప్రధాన యతి (Vr̥ddhi Yati — Matches the                         (Matches the underlying Resulting Substituted Vowel)                        Para-padādi Svara) │                                                           │ Substituted Vowels:                                 Original Word-2 Vowels: { ఐ,  ఔ }                                           { ఏ,  ఓ } │                                                           │ Belong to Class 1                                   Belong to Class 2 & 3 (A-Varga Equivalence)                               (I-Varga & U-Varga) ▼                                                           ▼ Matches: { అ,  ఆ,  ఐ,  ఔ }                           Matches: { ఇ, ఈ, ఎ, ఏ } for 'ఏ' { ఉ, ఊ, ఒ, ఓ } for 'ఓ'

&nbsp;

\#\#\#\# Option A: వృద్ధి యతి (Matching Substituted Vowels 'ఐ' and 'ఔ') (6.8.1 – 6.8.2)

&nbsp;

Because the resulting vowels \*\*'ఐ'\*\* and \*\*'ఔ'\*\* belong to \*\*Class 1 (A-Varga: అ, ఆ, ఐ, ఔ)\*\*, the caesura syllable matches any member of Class 1\[cite: 5\]:

&nbsp;

\* \*\*Substituted 'ఐ' (ఏకాదేశ ఐ-కారము) matching Class 1 Vowels:\*\*

  \* \*\*అ $\\longleftrightarrow$ భోగైక (ఐ):\*\* \*అనురాగాకృతి... భోగైకాంతసారంబు...\* ($\\text{భోగ} \+ \\text{ఏక} \\rightarrow \\mathbf{ఐ} \\longleftrightarrow \\mathbf{అ}$) (\*Manu Caritra\* 3-68)\[cite: 5\].

  \* \*\*అ $\\longleftrightarrow$ రక్షైక (ఐ):\*\* \*అనిశము సమస్త లోకరక్షైకదీక్ష...\* ($\\text{రక్షా} \+ \\text{ఏక}$) (\*Śivarātri Māhātmyamu\* 1-132)\[cite: 5\].

  \* \*\*అ (via Sandhi) $\\longleftrightarrow$ లోకైక (ఐ):\*\* \*...సహస్రాక్షునక్షరుని లోకైక నాథు...\* ($\\text{సహస్ర} \+ \\text{అక్షున్} \\rightarrow \\mathbf{అ} \\longleftrightarrow \\mathbf{ఐ}$) (\*Bhāratam\*, Śānti 4-216)\[cite: 5\].

  \* \*\*భోగైక (ఐ) $\\longleftrightarrow$ అ (via Sandhi):\*\* \*...భోగైక పరాయణుల్ పురుషులంగజుఁడు...\* (\*Appakavīyamu\* 3-40 / \*Bhāratam\*, Virāṭa 3-33)\[cite: 5\].

  \* \*\*ఆ $\\longleftrightarrow$ హేమైక (ఐ):\*\* \*ఆ పర్వతాగ్ర హేమైకశృంగంబునా...\* ($\\text{హేమ} \+ \\text{ఏక} \\rightarrow \\mathbf{ఐ} \\longleftrightarrow \\mathbf{ఆ}$) (\*Bhāgavatam\* 1-2)\[cite: 5\].

  \* \*\*ఐ $\\longleftrightarrow$ భాగైక (ఐ):\*\* \*...పర్యంకమిట్లై యొప్పారుచునుండగానుదరభాగైకప్రదేశంబునన్...\* (\*Bhāratam\*, Āraṇya 4-261)\[cite: 5\].

&nbsp;

\* \*\*Substituted 'ఔ' (ఏకాదేశ ఔ-కారము) matching Class 1 Vowels:\*\*

  \* \*\*అ $\\longleftrightarrow$ బలౌఘ (ఔ):\*\* \*అత్తఱిఁదద్బలంబరిబలౌఘములన్...\* ($\\text{బల} \+ \\text{ఓఘ} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\mathbf{అ}$) (\*Bhāgavatam\* 8-58)\[cite: 5\].

  \* \*\*అం $\\longleftrightarrow$ అయుక్తౌఘ (ఔ):\*\* \*అంచల్లీల హరించెఁ... అయుక్తౌఘక్షమా...\* ($\\text{అయుక్త} \+ \\text{ఓఘ}$) (\*Manu Caritra\* 3-140)\[cite: 5\].

  \* \*\*అ (via Sandhi) $\\longleftrightarrow$ వనౌకస (ఔ):\*\* \*...దేశాంతరమేఁగుఁడింకను వనౌకసులార...\* ($\\text{వన} \+ \\text{ఓకస్} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\mathbf{అ}$) (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 268)\[cite: 5\].

  \* \*\*నాకౌకస (ఔ) $\\longleftrightarrow$ అ (via Sandhi):\*\* \*నాకౌకసులందఱున్ సురగణాధిపుతోఁ...\* ($\\text{నాక} \+ \\text{ఓకస్} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\text{గణ} \+ \\text{అధిపు} \[\\mathbf{అ}\]$) (\*Uttara Harivaṁśamu\* 8-300)\[cite: 5\].

  \* \*\*ఆ $\\longleftrightarrow$ బాణౌఘ (ఔ):\*\* \*ఆలోకించెదు శార్ఙ్గ ముక్తపటు బాణౌఘంబుచే...\* ($\\text{బాణ} \+ \\text{ఓఘ} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\mathbf{ఆ}$) (\*Bhāgavatam\* 4-195)\[cite: 5\].

  \* \*\*లంకౌక (ఔ) $\\longleftrightarrow$ ఆ (via Sandhi):\*\* \*లంకౌకమురీతిఁ బుణ్యజనతాశ్రయమా...\* ($\\text{లంకా} \+ \\text{ఓకము} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\text{జనతా} \+ \\text{ఆశ్రయము} \[\\mathbf{ఆ}\]$) (\*Ghaṭikācala Māhātmyamu\* 1-4)\[cite: 5\].

  \* \*\*దుఃఖౌఘ (ఔ) $\\longleftrightarrow$ ఐ:\*\* \*...దుఃఖౌఘ నిపీడితనైతినింక...\* ($\\text{దుఃఖ} \+ \\text{ఓఘ} \\rightarrow \\mathbf{ఔ} \\longleftrightarrow \\mathbf{ఐ}$) (\*Bhāgavatam\* 10-Pūrvabhāga 171)\[cite: 5\].

&nbsp;

\#\#\#\# Option B: స్వరప్రధాన యతి in Vr̥ddhi Sandhi (Matching Original Vowels 'ఏ' and 'ఓ') (6.8.3)

&nbsp;

Alternatively, the poet may bypass the substituted diphthong and align directly with the underlying \*para-padādi svara\* (\*\*ఏ\*\* $\\rightarrow$ Class 2; \*\*ఓ\*\* $\\rightarrow$ Class 3)\[cite: 5\]:

&nbsp;

\* \*\*Matching Underlying 'ఏ' with Class 2 Vowels (\*ఇ, ఈ, ఎ, ఏ\*):\*\*

  \* \*\*ఈ $\\longleftrightarrow$ మదీయైకత్వ (ఏ):\*\* \*...యేనీగోసంతతి... మదీయైకత్వ...\* ($\\text{మదీయ} \+ \\mathbf{ఏకత్వ} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{ఈ}$ in \*ఏన్ \+ ఈ\*) (\*Bhāgavatam\* 10-Pūrvabhāga 7-174)\[cite: 5\].

  \* \*\*ఎ $\\longleftrightarrow$ లోకైక (ఏ):\*\* \*...డెఱ్ఱనార్యుండు సకలలోకైక విదితు...\* ($\\text{లోక} \+ \\mathbf{ఏక} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{ఎ}$ in \*తత్పరాత్ముఁడు \+ ఎఱ్ఱనార్యుండు\*) (\*Bhāratam\*, Araṇya 7-469)\[cite: 5\].

  \* \*\*ఎ $\\longleftrightarrow$ ప్రభుత్వైకాప్తి (ఏ):\*\* \*...మేఁకెరువుం... ప్రభుత్వైకాప్తి...\* (\*Appakavīyamu\* 3-39 / \*Bhāratam\*, Virāṭa 4-134)\[cite: 5\].

  \* \*\*ఏ $\\longleftrightarrow$ చిత్తైక (ఏ):\*\* \*...చిత్తైకాధీనత నిద్ర లేక వగతోనేనున్న...\* ($\\text{చిత్త} \+ \\mathbf{ఏక} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{ఏ}$ in \*వగతోన్ \+ ఏన్\*) (\*Bhāratam\*, Sabhā 2-184)\[cite: 5\].

  \* \*\*ఏ $\\longleftrightarrow$ క్రోధైక (ఏ):\*\* \*...క్రోధైక ధురీణతన్ గఱచి యేసిన...\* ($\\text{క్రోధ} \+ \\mathbf{ఏక} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{ఏ}$ in \*యేసిన\*) (\*Manu Caritra\* 3-90)\[cite: 5\].

&nbsp;

\* \*\*Matching Underlying 'ఓ' with Class 3 Vowels (\*ఉ, ఊ, ఒ, ఓ\*):\*\*

  \* \*\*ఉ $\\longleftrightarrow$ బిడౌజ (ఓ):\*\* \*...రక్కసులెందఱిందఱత్యున్నతిఁ... బిడౌజ తుదింజెడిపోరె...\* ($\\text{బిడ} \+ \\mathbf{ఓజ} \\rightarrow \\mathbf{ఓ} \\longleftrightarrow \\mathbf{ఉ}$ in \*అతి \+ ఉన్నతిన్\*) (\*Bhāskara Rāmāyaṇamu\*, Bāla 95)\[cite: 5\].

  \* \*\*ఓ $\\longleftrightarrow$ పవనౌషధి (ఓ):\*\* \*...నాకోవనజాక్షి మందపవనౌషధినాయక...\* ($\\text{పవన} \+ \\mathbf{ఓషధి} \\rightarrow \\mathbf{ఓ} \\longleftrightarrow \\mathbf{ఓ}$ in \*నాకున్ \+ ఓ\*) (\*Amuktamālyada\* 5-136)\[cite: 5\].

&nbsp;

\* \*\*Appakavi's Dual Demonstrative Stanza (3-41):\*\*

  \* Line 2: \*\*లంకౌకస్\*\* ($\\text{లంకా} \+ \\mathbf{ఓకస్} \\rightarrow \\mathbf{ఓ} \\longleftrightarrow \\mathbf{ఉ}$ in \*బద్ధ \+ ఉదగ్ర\* \[Option B, Class 3\])\[cite: 5\].

  \* Line 4: \*\*లోకైక\*\* ($\\text{లోక} \+ \\mathbf{ఏక} \\rightarrow \\mathbf{ఏ} \\longleftrightarrow \\mathbf{ఈ}$ in \*నీకున్ \+ ఈ\* \[Option B, Class 2\])\[cite: 5\].

&nbsp;

\* \*\*Simultaneous Co-existence in Single Verse (\*Channabasava Purāṇamu\* 1-150):\*\*

  \* Line 2 executes \*\*Option A (Vr̥ddhi Yati):\*\* \*\*అ\*\* $\\longleftrightarrow$ \*\*జనతైక\*\* ($\\text{జనతా} \+ \\text{ఏక} \\rightarrow \\mathbf{ఐ}$)\[cite: 5\].

  \* Line 4 executes \*\*Option B (Svara-Pradhāna Yati):\*\* \*\*ఎ\*\* $\\longleftrightarrow$ \*\*నియతైహిక\*\* ($\\text{నియత} \+ \\mathbf{ఈహా} \\rightarrow \\mathbf{ఈ}$)\[cite: 5\].

&nbsp;

\---

&nbsp;

\#\#\# 6.9 వ్యంజనాక్షర యతులు (Consonant Yati Taxonomy — 21 Rules)

&nbsp;

Vyañjana Yatulu (హల్లు యతులు) regulate consonantal alliteration and class affinities across the caesura\[cite: 5\]. Appakavi cataloged exactly \*\*21 Consonant Yatis\*\* (\*Vyañjanākṣara Virutulu\*)\[cite: 5\]:

&nbsp;

| \# | Canonical Name (శాస్త్ర నామము) | Structural Domain |

| :---: | :--- | :--- |

| 1 | \*\*ప్రాణి విరామము (Prāṇi Virāmamu)\*\*\[cite: 5\] | Consonant identity with vowel-class alignment\[cite: 5\]. |

| 2 | \*\*వర్గజయతి (Vargaja Yati)\*\*\[cite: 5\] | Class-stop affinity (Stops 1, 2, 3, 4 within a varga)\[cite: 5\]. |

| 3 | \*\*బిందుయతి (Bindu Yati)\*\*\[cite: 5\] | Anusvāra-preceded stop affinities\[cite: 5\]. |

| 4 | \*\*తద్భవవ్యాజ విశ్రమము (Tadbhavavyāja Viśramamu)\*\*\[cite: 5\] | Borrowed/Tadbhava sound correspondences\[cite: 5\]. |

| 5 | \*\*విశేషవళి (Viśēṣavaḷi)\*\*\[cite: 5\] | Specialized consonant pairings\[cite: 5\]. |

| 6 | \*\*అనుస్వార సంబంధ యతి (Anusvāra Sambandha Yati)\*\*\[cite: 5\] | Nasal-resonant harmonic bridges\[cite: 5\]. |

| 7 | \*\*అనునాసికాక్షర యతి (Anunāsikākṣara Yati)\*\*\[cite: 5\] | Nasal stop pairings (Class 5 consonants)\[cite: 5\]. |

| 8 | \*\*'ము'విభక్తి యతి ('Mu' Vibhakti Yati)\*\*\[cite: 5\] | Case-ending nominal \*'mu'\* caesura\[cite: 5\]. |

| 9 | \*\*'ము'కారయతి ('Mu'kāra Yati)\*\*\[cite: 5\] | Radical/stem \*'mu'\* interactions\[cite: 5\]. |

| 10 | \*\*'మ'వర్ణ విరామము ('Ma'varṇa Virāmamu)\*\*\[cite: 5\] | Structural labial nasal caesuras\[cite: 5\]. |

| 11 | \*\*ఋజు యతి (R̥ju Yati)\*\*\[cite: 5\] | Direct consonant identity alignments\[cite: 5\]. |

| 12 | \*\*ప్రత్యేకయతి (Pratyēka Yati)\*\*\[cite: 5\] | Isolated anomalous licenses\[cite: 5\]. |

| 13 | \*\*భిన్నయతి (Bhinna Yati)\*\*\[cite: 5\] | Dual-function vowel/consonant split (Ubhaya Yati)\[cite: 5\]. |

| 14 | \*\*ఏకతర యతి (Ēkatara Yati)\*\*\[cite: 5\] | Liquid distinctions (Soft \*Ra\* vs. Hard \*Ṟa\*)\[cite: 5\]. |

| 15 | \*\*అభేద విరతి (Abhēda Virati)\*\*\[cite: 5\] | Identity pairings between homorganic liquids (\*La-Ḷa\*)\[cite: 5\]. |

| 16 | \*\*అభేదవర్గ యతి (Abhēdavarga Yati)\*\*\[cite: 5\] | Inter-class homorganic bridges (e.g., \*Pa-Va\*)\[cite: 5\]. |

| 17 | \*\*ఊష్మ విశ్రాంతి (Ūṣma Viśrānti)\*\*\[cite: 5\] | Sibilant affinities (\*Śa, Ṣa, Sa\*)\[cite: 5\]. |

| 18 | \*\*సరసవళి (Sarasavaḷi)\*\*\[cite: 5\] | Vowel-consonant bridges (\*A-Ya-Ha\*)\[cite: 5\]. |

| 19 | \*\*సంయుక్త విశ్రామము (Saṁyukta Viśrāmamu)\*\*\[cite: 5\] | Conjunct consonant cluster scansion\[cite: 5\]. |

| 20 | \*\*అంత్యోష్మ సంధివడి (Antyōṣma Sandhivaḍi)\*\*\[cite: 5\] | Final spirant sandhi alignments\[cite: 5\]. |

| 21 | \*\*వికల్ప విరమణము (Vikalpa Viramaṇamu)\*\*\[cite: 5\] | Optional/alternative morphophonemic caesuras\[cite: 5\]. |

&nbsp;

\---

&nbsp;

\#\#\# 6.10 ప్రాణి యతులు (Prāṇi Yatulu — Consonant Identity with Vowel-Class Alignment)

&nbsp;

\* \*\*Etymological Architecture:\*\* A bare consonant without a vowel is a lifeless corpse (\*pollu-hallu\*: \*\*క్, గ్, చ్\*\*)\[cite: 5\]. Vowels are vital breaths (\*prāṇamulu\*)\[cite: 5\]. A consonant infused with a vowel is designated a \*\*ప్రాణి\*\* (\*prāṇi\* \= living entity, e.g., \*\*క, కా, కి, కీ\*\*)\[cite: 5\].

\* \*\*The Core Axiom:\*\* When matching identical consonants, \*\*the consonants must be identical AND their attached vowels must belong to the exact same vowel equivalence class\*\*\[cite: 5\]\!

  $$\\text{Consonant}\_A \+ \\text{Vowel}\_X \\quad\\longleftrightarrow\\quad \\text{Consonant}\_A \+ \\text{Vowel}\_Y \\quad\\iff\\quad \\text{Class}(\\text{Vowel}\_X) \\equiv \\text{Class}(\\text{Vowel}\_Y)$$\[cite: 5\]

\* \*\*Strict Intra-Class Partitioning (Tripartite Vowel Grid):\*\*

  A consonant (e.g., \*\*'క'\*\*) splits into three non-overlapping caesura realms\[cite: 5\]:

  1\. \*\*Group 1 (A-Varga Diphthongs):\*\* $\\{\\text{క, కా, కై, కౌ}\\}$ $\\longleftrightarrow$ mutually rhyme\[cite: 5\].

  2\. \*\*Group 2 (I-Varga Resonants):\*\* $\\{\\text{కి, కీ, కృ, కౄ, కె, కే}\\}$ $\\longleftrightarrow$ mutually rhyme\[cite: 5\].

  3\. \*\*Group 3 (U-Varga Labials):\*\* $\\{\\text{కు, కూ, కొ, కో}\\}$ $\\longleftrightarrow$ mutually rhyme\[cite: 5\].

\* \*\*Cross-Group Invalidation:\*\* Consonant identity cannot overcome vowel-group conflicts\[cite: 5\]:

  \* $\\text{క} \\neq \\text{కి}$ (Class 1 vs. Class 2 breach)\[cite: 5\].

  \* $\\text{కి} \\neq \\text{కు}$ (Class 2 vs. Class 3 breach)\[cite: 5\].

  \* $\\text{క} \\neq \\text{కు}$ (Class 1 vs. Class 3 breach)\[cite: 5\].

\* \*\*Bidirectionality:\*\* Any valid pairing is fully bidirectional ($\\mathbf{క \\longleftrightarrow కా} \\iff \\mathbf{కా \\longleftrightarrow క}$)\[cite: 5\]. Pure identity (\*\*క-క, చె-చె, పు-పు\*\*) is the foundational default\[cite: 5\].

&nbsp;

\#\#\#\# Exhaustive Corpus Alignments Across Consonants (6.10.2 – 6.10.3)

&nbsp;

\* \*\*క-Series:\*\*

  \* Group 1: \*\*కా $\\longleftrightarrow$ క\*\* (\*Bhāratam\*, Sabhā 1-30)\[cite: 5\]; \*\*కై $\\longleftrightarrow$ క\*\* (\*Bhāratam\*, Āraṇya 3-982)\[cite: 5\]; \*\*క $\\longleftrightarrow$ కౌ\*\* (\*Bhāratam\*, Ādi 8-16)\[cite: 5\]; \*\*కా $\\longleftrightarrow$ కై\*\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 5\]; \*\*కౌ $\\longleftrightarrow$ కా\*\* (\*Bhāratam\*, Udyōga 6-36)\[cite: 5\]; \*\*కౌ $\\longleftrightarrow$ కై\*\* (\*Bhāratam\*, Udyōga 1-210)\[cite: 5\].

  \* Group 2: \*\*కీ $\\longleftrightarrow$ కి\*\* (\*Manu Caritra\* 5-64)\[cite: 5\]; \*\*కృ $\\longleftrightarrow$ కి\*\* (\*Manu Caritra\* 2-17)\[cite: 5\]; \*\*కె $\\longleftrightarrow$ కి\*\* (\*Bhāgavatam\* 4-14)\[cite: 5\]; \*\*కే $\\longleftrightarrow$ కి\*\* (\*Amuktamālyada\* 4-102)\[cite: 5\]; \*\*కృ $\\longleftrightarrow$ కీ\*\* (\*Bhāratam\*, Ādi 5-37)\[cite: 5\]; \*\*కె $\\longleftrightarrow$ కీ\*\* (\*Bhāgavatam\* 5-184)\[cite: 5\]; \*\*కీ $\\longleftrightarrow$ కే\*\* (\*Bhāratam\*, Anuśāsanika 5-325)\[cite: 5\]; \*\*కె $\\longleftrightarrow$ కృ\*\* (\*Śivarātri Māhātmyamu\* 1-50)\[cite: 5\]; \*\*కె $\\longleftrightarrow$ కే\*\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 211)\[cite: 5\]; \*\*కే $\\longleftrightarrow$ కృ\*\* (\*Manu Caritra\* 1-19)\[cite: 5\].

  \* Group 3: \*\*కూ $\\longleftrightarrow$ కు\*\* (\*Manu Caritra\* 4-12)\[cite: 5\]; \*\*కొ $\\longleftrightarrow$ కు\*\* (\*Bhāratam\*, Ādi 6-118)\[cite: 5\]; \*\*కో $\\longleftrightarrow$ కు\*\* (\*Bhāgavatam\* 1-191)\[cite: 5\]; \*\*కొ $\\longleftrightarrow$ కూ\*\* (\*Bhāratam\*, Āraṇya 2-150)\[cite: 5\]; \*\*కో $\\longleftrightarrow$ కూ\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 59)\[cite: 5\]; \*\*కొ $\\longleftrightarrow$ కో\*\* (\*Bhāgavatam\* 1-167)\[cite: 5\].

\* \*\*Aspirates, Mediae & Voiced Stops:\*\*

  \* \*\*ఖ-Series:\*\* \*\*ఖ $\\longleftrightarrow$ ఖ\*\* (\*Manu Caritra\* 4-33)\[cite: 5\]; \*\*ఖి $\\longleftrightarrow$ ఖే\*\* (\*Bhāratam\*, Ādi 3-186)\[cite: 5\]; \*\*ఖి $\\longleftrightarrow$ ఖే\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 306)\[cite: 5\].

  \* \*\*గ-Series:\*\* \*\*గౌ $\\longleftrightarrow$ గ\*\* (\*Bhāratam\*, Ādi 5-3)\[cite: 5\]; \*\*గే $\\longleftrightarrow$ గృ\*\* (\*Bhāratam\*, Ādi 1-205)\[cite: 5\]; \*\*గ $\\longleftrightarrow$ గౌ\*\* (\*Bhāgavatam\* 7-437)\[cite: 5\]; \*\*గీ $\\longleftrightarrow$ గి\*\* (\*Bhāratam\*, Ādi 8-131)\[cite: 5\]; \*\*గు $\\longleftrightarrow$ గో\*\* (\*Amuktamālyada\* 4-98)\[cite: 5\].

  \* \*\*ఘ-Series:\*\* \*\*ఘ $\\longleftrightarrow$ ఘా\*\* (\*Bhāratam\*, Virāṭa 3-167)\[cite: 5\]; \*\*ఘూ $\\longleftrightarrow$ ఘో\*\* (\*Amuktamālyada\* 3-91)\[cite: 5\].

  \* \*\*చ/ఛ/జ-Series:\*\* \*\*చై $\\longleftrightarrow$ చా\*\* (\*Bhāgavatam\* 7-6)\[cite: 5\]; \*\*చీ $\\longleftrightarrow$ చె\*\* (\*Vēmana Śatakam\*)\[cite: 5\]; \*\*చె $\\longleftrightarrow$ చ\*\* (\*Manu Caritra\* 2-10)\[cite: 5\]; \*\*చు $\\longleftrightarrow$ చూ\*\* (\*Amuktamālyada\* 4-143)\[cite: 5\]; \*\*ఛా $\\longleftrightarrow$ ఛ\*\* (\*Manu Caritra\* 3-26)\[cite: 5\]; \*\*జ $\\longleftrightarrow$ జా\*\* (\*Bhāratam\*, Sabhā 1-121)\[cite: 5\]; \*\*జే $\\longleftrightarrow$ జృ\*\* (\*Bhāgavatam\* 10-Pūrvabhāga 105)\[cite: 5\]; \*\*జి $\\longleftrightarrow$ జీ\*\* (\*Bhāgavatam\* 8-273)\[cite: 5\]; \*\*జే $\\longleftrightarrow$ జో\*\* (Breach? No, \*జ-జా / జు-జూ\* \*Bhāratam\*, Ādi 7-3)\[cite: 5\].

  \* \*\*Retroflexes (ట/ఠ/డ/ఢ/ణ):\*\* \*\*ట $\\longleftrightarrow$ టా\*\* (\*Amuktamālyada\* 4-100)\[cite: 5\]; \*\*టె $\\longleftrightarrow$ టి\*\* (\*Bhāratam\*, Āraṇya 7-433)\[cite: 5\]; \*\*టు $\\longleftrightarrow$ టో\*\* (\*Bhāratam\*, Virāṭa 1-315)\[cite: 5\]; \*\*ఠ $\\longleftrightarrow$ ఠ\*\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 846)\[cite: 5\]; \*\*ఠ $\\longleftrightarrow$ ఠి\*\* (\*Amuktamālyada\* 6-32)\[cite: 5\]; \*\*డ $\\longleftrightarrow$ డా\*\* (\*Bhāratam\*, Virāṭa 2-7)\[cite: 5\]; \*\*డె $\\longleftrightarrow$ డి\*\* (\*Bhāgavatam\* 10-Pūrvabhāga 1245)\[cite: 5\]; \*\*డు $\\longleftrightarrow$ డో\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 37)\[cite: 5\]; \*\*ఢ $\\longleftrightarrow$ ఢ\*\* (\*Bhāgavatam\* 7-170)\[cite: 5\]; \*\*ణ $\\longleftrightarrow$ ణ\*\* (\*Bhāratam\*, Udyōga 4-354)\[cite: 5\].

  \* \*\*Dentals & Labials (త/థ/ద/ధ/న/ప/ఫ/బ/భ/మ):\*\* \*\*తా $\\longleftrightarrow$ త\*\* (\*Bhāratam\*, Ādi 6-152)\[cite: 5\]; \*\*తీ $\\longleftrightarrow$ తె\*\* (\*Manu Caritra\* 1-57)\[cite: 5\]; \*\*తో $\\longleftrightarrow$ తొ\*\* (\*Bhāgavatam\* 10-Pūrvabhāga 375)\[cite: 5\]; \*\*థి $\\longleftrightarrow$ థి\*\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 103)\[cite: 5\]; \*\*దా $\\longleftrightarrow$ ద\*\* (\*Bhāratam\*, Ādi 4-172)\[cite: 5\]; \*\*దై $\\longleftrightarrow$ ద\*\* (\*Bhāratam\*, Śānti 7-115)\[cite: 5\]; \*\*దే $\\longleftrightarrow$ దృ\*\* (\*Bhāgavatam\* 1-224)\[cite: 5\]; \*\*దు $\\longleftrightarrow$ దొ\*\* (\*Bhāratam\*, Śānti 7-140)\[cite: 5\]; \*\*దు $\\longleftrightarrow$ దో\*\* (\*Bhāgavatam\* 10-Pūrvabhāga 1575)\[cite: 5\]; \*\*ధ $\\longleftrightarrow$ ధౌ\*\* (\*Bhāratam\*, Āraṇya 1-65)\[cite: 5\]; \*\*ధే $\\longleftrightarrow$ ధృ\*\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 462)\[cite: 5\]; \*\*ధు $\\longleftrightarrow$ ధూ\*\* (\*Manu Caritra\* 1-71)\[cite: 5\]; \*\*నా $\\longleftrightarrow$ న\*\* (\*Manu Caritra\* 2-54)\[cite: 5\]; \*\*నృ $\\longleftrightarrow$ ని\*\* (\*Bhāratam\*, Āraṇya 3-176)\[cite: 5\]; \*\*ను $\\longleftrightarrow$ నో\*\* (\*Bhāratam\*, Ādi 4-103)\[cite: 5\]; \*\*ప $\\longleftrightarrow$ పౌ\*\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 102)\[cite: 5\]; \*\*పి $\\longleftrightarrow$ పీ\*\* (\*Bhāratam\*, Ādi 4-226)\[cite: 5\]; \*\*పు $\\longleftrightarrow$ పొ\*\* (\*Sumati Śatakam\*)\[cite: 5\]; \*\*ఫ $\\longleftrightarrow$ ఫ\*\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 102)\[cite: 5\]; \*\*ఫా $\\longleftrightarrow$ ఫ\*\* (\*Manu Caritra\* 6-37)\[cite: 5\]; \*\*బా $\\longleftrightarrow$ బౌ\*\* (\*Bhāratam\*, Ādi 4-74)\[cite: 5\]; \*\*బా $\\longleftrightarrow$ బ\*\* (\*Bhāratam\*, Virāṭa 2-333)\[cite: 5\]; \*\*బె $\\longleftrightarrow$ బి\*\* (\*Amuktamālyada\* 4-251)\[cite: 5\]; \*\*బూ $\\longleftrightarrow$ బో\*\* (\*Manu Caritra\* 2-29)\[cite: 5\]; \*\*బో $\\longleftrightarrow$ బు\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 429)\[cite: 5\]; \*\*భ $\\longleftrightarrow$ భా\*\* (\*Amuktamālyada\* 2-51)\[cite: 5\]; \*\*భే $\\longleftrightarrow$ భృ\*\* (\*Manu Caritra\* 2-136)\[cite: 5\]; \*\*భూ $\\longleftrightarrow$ భో\*\* (\*Manu Caritra\* 2-55)\[cite: 5\]; \*\*మ $\\longleftrightarrow$ మా\*\* (\*Amuktamālyada\* 1-74)\[cite: 5\]; \*\*మృ $\\longleftrightarrow$ మే\*\* (\*Bhāratam\*, Virāṭa 1-103)\[cite: 5\]; \*\*మో $\\longleftrightarrow$ ము\*\* (\*Bhāgavatam\* 7-137)\[cite: 5\].

  \* \*\*Liquids, Sibilants & Aspirate (య/ర/ఱ/ల/ళ/వ/శ/ష/స/హ):\*\* \*\*యా $\\longleftrightarrow$ య\*\* (\*Bhāratam\*, Ādi 5-34)\[cite: 5\]; \*\*యో $\\longleftrightarrow$ యు\*\* (\*Bhāratam\*, Sabhā 2-29)\[cite: 5\]; \*\*రా $\\longleftrightarrow$ ర\*\* (\*Bhāgavatam\* 8-90)\[cite: 5\]; \*\*రి $\\longleftrightarrow$ రీ\*\* (\*Bhāratam\*, Ādi 8-178)\[cite: 5\]; \*\*రో $\\longleftrightarrow$ రు\*\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 5\]; \*\*ఱ $\\longleftrightarrow$ ఱ\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 174)\[cite: 5\]; \*\*ఱు $\\longleftrightarrow$ ఱు\*\* (\*Śṛṅgāra Śakuntalamu\* 2-382)\[cite: 5\]; \*\*ల $\\longleftrightarrow$ లా\*\* (\*Manu Caritra\* 3-49)\[cite: 5\]; \*\*లె $\\longleftrightarrow$ లే\*\* (\*Manu Caritra\* 3-129)\[cite: 5\]; \*\*లో $\\longleftrightarrow$ లు\*\* (\*Bhāratam\*, Sabhā 6-125)\[cite: 5\]; \*\*ళీ $\\longleftrightarrow$ ళీ\*\* (\*Bhāgavatam\* 8-215)\[cite: 5\]; \*\*వ $\\longleftrightarrow$ వా\*\* (\*Bhāgavatam\* 9-267)\[cite: 5\]; \*\*వా $\\longleftrightarrow$ వై\*\* (\*Manu Caritra\* 1-52)\[cite: 5\]; \*\*వి $\\longleftrightarrow$ వే\*\* (\*Bhāgavatam\* 3-1024)\[cite: 5\]; \*\*వు $\\longleftrightarrow$ వు\*\* (\*Bhāratam\*, Ādi 5-74)\[cite: 5\]; \*\*శై $\\longleftrightarrow$ శౌ\*\* (\*Amuktamālyada\* 1-32)\[cite: 5\]; \*\*శీ $\\longleftrightarrow$ శే\*\* (\*Amuktamālyada\* 4-208)\[cite: 5\]; \*\*శు $\\longleftrightarrow$ శో\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 341)\[cite: 5\]; \*\*షా $\\longleftrightarrow$ షా\*\* (\*Kavi Karṇarasāyanamu\* 1-5)\[cite: 5\]; \*\*షి $\\longleftrightarrow$ షి\*\* (\*Amuktamālyada\* 2-41)\[cite: 5\]; \*\*స $\\longleftrightarrow$ సౌ\*\* (\*Amuktamālyada\* 5-143)\[cite: 5\]; \*\*సి $\\longleftrightarrow$ సృ\*\* (\*Bhāratam\*, Ādi 2-211)\[cite: 5\]; \*\*సు $\\longleftrightarrow$ సో\*\* (\*Molla Rāmāyaṇamu\*, Araṇya 32)\[cite: 5\]; \*\*హ $\\longleftrightarrow$ హై\*\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 104)\[cite: 5\]; \*\*హి $\\longleftrightarrow$ హృ\*\* (\*Bhāratam\*, Śānti 5-511)\[cite: 5\]; \*\*హు $\\longleftrightarrow$ హో\*\* (\*Manu Caritra\* 6-79)\[cite: 5\].

&nbsp;

\#\#\#\# Engine Disambiguation Trap: Prāṇi vs. Svara-Pradhāna (6.10.4)

&nbsp;

An automated parser must strictly test for morphological sandhi boundaries before classifying an apparent consonant identity match as \*Prāṇi Yati\*\[cite: 5\]:

\* \*Illusion 1:\* \*...నీ వొక్కరుఁడవ యున్నవాఁడవుర్వీరాజ్యం...\*

  \* Surface appearance: \*\*వొ $\\longleftrightarrow$ వు\*\* (appears to be a 'va'-consonant Prāṇi match)\[cite: 5\].

  \* Actual parse: Compound boundary $\\text{నీవు} \+ \\mathbf{ఒక్కరుఁడవ} \\longleftrightarrow \\text{ఉన్నవాఁడవు} \+ \\mathbf{ఉర్వీ}$.

  \* Classification: \*\*స్వరప్రధాన యతి (Svara-Pradhāna Yati)\*\* matching \*\*ఒ $\\longleftrightarrow$ ఉ\*\* (Class 3)\[cite: 5\]\!

\* \*Illusion 2:\* \*...పాయక చీకటి యందును / నేయం దానభ్యసించెనిట్టియెడం...\*

  \* Surface appearance: \*\*నే $\\longleftrightarrow$ ని\*\*\[cite: 5\].

  \* Actual parse: $\\text{యందునున్} \+ \\mathbf{ఏయన్} \\longleftrightarrow \\text{అభ్యసించెన్} \+ \\mathbf{ఇట్టి}$.

  \* Classification: \*\*స్వరప్రధాన యతి\*\* matching \*\*ఏ $\\longleftrightarrow$ ఇ\*\* (Class 2)\[cite: 5\]\!

\* \*Illusion 3:\* \*...రాజనందను / లెల్లను సమకట్టి రథములెక్కి...\*

  \* Surface appearance: \*\*లె $\\longleftrightarrow$ లె\*\*\[cite: 5\].

  \* Actual parse: $\\text{రాజనందనులు} \+ \\mathbf{ఎల్లను} \\longleftrightarrow \\text{రథములు} \+ \\mathbf{ఎక్కి}$.

  \* Classification: \*\*స్వరప్రధాన యతి\*\* matching \*\*ఎ $\\longleftrightarrow$ ఎ\*\* (Class 2)\[cite: 5\]\!

\* \*Illusion 4:\* \*...దైత్యుం / డిచ్చఁగొనండయ్యెనింద్రుఁడీశ్వరశిక్షన్...\*

  \* Surface appearance: \*\*డి $\\longleftrightarrow$ డీ\*\*\[cite: 5\].

  \* Actual parse: $\\text{దైత్యుండు} \+ \\mathbf{ఇచ్చన్} \\longleftrightarrow \\text{ఇంద్రుఁడు} \+ \\mathbf{ఈశ్వర}$.

  \* Classification: \*\*స్వరప్రధాన యతి\*\* matching \*\*ఇ $\\longleftrightarrow$ ఈ\*\* (Class 2)\[cite: 5\]\!

&nbsp;

\---

&nbsp;

\#\#\# 6.11 వర్గజ యతులు (Vargaja Yatulu — Class-Stop Homorganic Yatis)

&nbsp;

\* \*\*Structural Definition:\*\* The 25 stops (\*sparśas\*: క through మ) are categorized into five articulatory classes (\*vargas\*)\[cite: 5\]. In each class, the \*\*first four consonants (Unaspirated Voiceless, Aspirated Voiceless, Unaspirated Voiced, Aspirated Voiced)\*\* possess complete, mutual Yati affinity\[cite: 5\]\!

\* \*\*Universal Exclusion of Class 5 (Anunāsikas):\*\* The 5th consonant of every varga (the nasals: \*\*ఙ, ఞ, ణ, న, మ\*\*) is \*\*strictly excluded\*\* from Vargaja Yati\[cite: 5\]. A stop cannot rhyme directly with its homorganic nasal ($\\text{క} \\neq \\text{ఙ}$; $\\text{చ} \\neq \\text{ఞ}$; $\\text{ట} \\neq \\text{ణ}$; $\\text{త} \\neq \\text{న}$; $\\text{ప} \\neq \\text{మ}$)\[cite: 5\]. (These require Bindu/Anunāsika Yati bridges, 6.12)\[cite: 5\].

\* \*\*Combinatorial Topology:\*\*

  Each 4-consonant class yields exactly $\\binom{4}{2} \= 6$ unique pair combinations\[cite: 5\]:

&nbsp;

$$\\mathbf{Class\\ Stop\\ Affinity\\ Sets}$$

$$\\begin{aligned}

\\mathbf{క-Varga\\ (6\\ Pairs):} &\\quad \\{\\text{క-ఖ,\\ క-గ,\\ క-ఘ,\\ ఖ-గ,\\ ఖ-ఘ,\\ గ-ఘ}\\} \\\\

\\mathbf{ట-Varga\\ (6\\ Pairs):} &\\quad \\{\\text{ట-ఠ,\\ ట-డ,\\ ట-ఢ,\\ ఠ-డ,\\ ఠ-ఢ,\\ డ-ఢ}\\} \\\\

\\mathbf{త-Varga\\ (6\\ Pairs):} &\\quad \\{\\text{త-థ,\\ త-ద,\\ త-ధ,\\ థ-ద,\\ థ-ధ,\\ ద-ధ}\\} \\\\

\\mathbf{ప-Varga\\ (6\\ Pairs):} &\\quad \\{\\text{ప-ఫ,\\ ప-బ,\\ ప-భ,\\ ఫ-బ,\\ ఫ-భ,\\ బ-భ}\\}

\\end{aligned}$$\[cite: 5\]

&nbsp;

\#\#\#\# The Expanded Palatal Class: Dantya 'Ca' and 'Ja' (15 Combinations)

In native Telugu phonology, the palatal series incorporates both standard palatals (\*\*చ, జ\*\*) and dental affricates (\*\*ౘ, ౙ\*\*)\[cite: 5\]. By grammatical rule (\*Bāla Vyākaraṇam\*, Samjñā 7: \*"దంత్య తాలవ్యంబులయిన చజలు సవర్ణంబులు"\*), dentals and palatals are homorganic equivalents (\*savarṇas\*)\[cite: 5\].

Thus, the palatal series expands to 6 active consonants: $\\{\\mathbf{చ,\\ ౘ,\\ ఛ,\\ జ,\\ ౙ,\\ ఝ}\\}$\[cite: 5\].

This generates $\\binom{6}{2} \= \\mathbf{15\\ Unique\\ Yati\\ Pairings}$\[cite: 5\]:

$$\\begin{aligned}

\\text{Pairings with 'చ':} &\\quad \\text{చ-ౘ,\\ చ-ఛ,\\ చ-జ,\\ చ-ౙ,\\ చ-ఝ} \\\\

\\text{Pairings with 'ౘ':} &\\quad \\text{ౘ-ఛ,\\ ౘ-జ,\\ ౘ-ౙ,\\ ౘ-ఝ} \\\\

\\text{Pairings with 'ఛ':} &\\quad \\text{ఛ-జ,\\ ఛ-ౙ,\\ ఛ-ఝ} \\\\

\\text{Pairings with 'జ':} &\\quad \\text{జ-ౙ,\\ జ-ఝ} \\\\

\\text{Pairing with 'ౙ':} &\\quad \\text{ౙ-ఝ}

\\end{aligned}$$\[cite: 5\]

&nbsp;

\#\#\#\# Crucial Vowel Constraint on Vargaja Yati

While the consonants within a varga freely substitute for each other, \*\*their attached vowels must still obey the Prāṇi Yati Vowel-Class partition\*\*\[cite: 5\]:

\* \*\*క\*\* may rhyme with \*\*గ, ఖా, ఘౌ\*\* (all Class 1 vowels)\[cite: 5\].

\* \*\*క\*\* \*cannot\* rhyme with \*\*గి, ఘు, భే\*\* (breaches vowel group boundaries)\[cite: 5\].

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### Vargaja Yatulu: Consonant-Vowel Integration & Full Combinatorial Mechanics (6.11.1 – 6.11.2)

* **Combinatorial Total (39 Vargaja Yatis):** The five consonant classes generate exactly 39 standard intra-class pairs: 6 in the *Ka*\-varga, 15 in the *Ca*\-varga (incorporating dental *ౘ, ౙ*), 6 in the *Ṭa*\-varga, 6 in the *Ta*\-varga, and 6 in the *Pa*\-varga.  
* **Phonetic Integration Axiom:** Consonant yatis are stated nominally with short *'a'* (e.g., **క-ఖ**, **క-గ**) purely for vocal ease, but represent pure consonants ($\\text{క్-ఖ్, క్-గ్}$). In actual verse, the consonants combine with vowels, and **their attached vowels must strictly belong to the same Svaramaitri equivalence class** (*Prāṇi Yati* rule 6.10):  
* Class 1 ($A$-varga: *అ, ఆ, ఐ, ఔ*): **క, కా, కై, కౌ $\\longleftrightarrow$ గ, గా, గై, గౌ**.  
* Class 2 ($I$-varga: *ఇ, ఈ, ఋ, ౠ, ఎ, ఏ*): **కి, కీ, కృ, కౄ, కె, కే $\\longleftrightarrow$ గి, గీ, గృ, గౄ, గె, గే**.  
* Class 3 ($U$-varga: *ఉ, ఊ, ఒ, ఓ*): **కు, కూ, కొ, కో $\\longleftrightarrow$ గు, గూ, గొ, గో**.  
* *Negative Rule:* Cross-class vowel pairings invalidate the consonant match (e.g., **కి $\\neq$ గ**, because vowel *'i'* cannot match vowel *'a'* despite the consonant affinity between *k* and *g*).  
* **Demonstrations Across the Three Vowel Classes for Ka-Ga (6.11.1):**  
* *Class 1 ($A$-varga):* **క $\\longleftrightarrow$ గా** (*కలలం బోలెడి... వనితాగారాది...* — *Bhāgavatam* 10-Pūrvabhāga 1233).  
* *Class 2 ($I$-varga):* **కి $\\longleftrightarrow$ గీ** (*కిన్నరీబృంద... సంగీతరీతి...* — *Manu Caritra* 2-7).  
* *Class 3 ($U$-varga):* **కో $\\longleftrightarrow$ గో** (*కోడెవయస్సు... గోటికి...*).  
* **Sandhi-Derived Consonants in Vargaja Yati (6.11.1):** When consonants mutate dynamically via sandhi (such as unvoiced stops softening into voiced stops after a *drutamu*: $\\text{కన్నుల} \\rightarrow \\text{గన్నుల}$), the engine evaluates the rhyme on the final surface consonant, validating it as a Vargaja match (**క $\\longleftrightarrow$ గ**).

                 Vargaja Yati Matrix (Intra-Class Pairs)

┌───────────┬────────────────────────────────────────────────────────┬───────┐

│ Class     │ Permissible Consonant Stop Pairings                    │ Total │

├───────────┼────────────────────────────────────────────────────────┼───────┤

│ Ka-varga  │ క-ఖ, క-గ, క-ఘ, ఖ-గ, ఖ-ఘ, గ-ఘ                           │   6   │

├───────────┼────────────────────────────────────────────────────────┼───────┤

│ Ca-varga  │ చ-ౘ, చ-ఛ, చ-జ, చ-ౙ, చ-ఝ, ౘ-ఛ, ౘ-జ, ౘ-ౙ, ౘ-ఝ,          │  15   │

│           │ ఛ-జ, ఛ-ౙ, ఛ-ఝ, జ-ౙ, జ-ఝ, ౙ-ఝ                           │       │

├───────────┼────────────────────────────────────────────────────────┼───────┤

│ Ṭa-varga  │ ట-ఠ, ట-డ, ట-ఢ, ఠ-డ, ఠ-ఢ, డ-ఢ                           │   6   │

├───────────┼────────────────────────────────────────────────────────┼───────┤

│ Ta-varga  │ త-థ, త-ద, త-ధ, థ-ద, థ-ధ, ద-ధ                           │   6   │

├───────────┼────────────────────────────────────────────────────────┼───────┤

│ Pa-varga  │ ప-ఫ, ప-బ, ప-భ, ఫ-బ, ఫ-భ, బ-భ                           │   6   │

└───────────┴────────────────────────────────────────────────────────┴───────┘

&nbsp;

*(Every combination must strictly preserve internal vowel-class alignment)*.

#### Canonical Provenance Across Vargaja Classes (6.11.2)

* **Ka-Class:** **క $\\longleftrightarrow$ ఖ** (*Bhāskara Rāmāyaṇamu*, Kiṣkindha 88); **క $\\longleftrightarrow$ ఖా** (*Manu Caritra* 4-80); **కై $\\longleftrightarrow$ గ** (*Bhāgavatam* 1-409); **ఘో $\\longleftrightarrow$ కో** (*Bhāratam*, Ādi 2-101); **గ $\\longleftrightarrow$ ఖ** (*Gōpīnātha Rāmāyaṇamu*, Sundara 556); **గృ $\\longleftrightarrow$ ఖే** (*Amuktamālyada* 4-40); **ఖ $\\longleftrightarrow$ ఘ** (*Vēmana Śatakam*); **ఘ $\\longleftrightarrow$ గా** (*Bhāratam*, Ādi 6-79).  
* **Ca-Class (with Dantya Affricates):** **చా $\\longleftrightarrow$ చ** (*Bhāratam*, Ādi 7-5); **ఛ $\\longleftrightarrow$ చ** (*Bhāgavatam* 8-621); **చి $\\longleftrightarrow$ జృ** (*Manu Caritra* 2-38); **చ $\\longleftrightarrow$ జో** (*Manu Caritra* 3-136); **ఝ $\\longleftrightarrow$ చ** (*Bhāskara Rāmāyaṇamu*, Bāla 80); **ఛు $\\longleftrightarrow$ చు** (*Rāmāyaṇa Kalpavṛkṣamu*, Araṇya 166); **జ $\\longleftrightarrow$ చే** (*Bhāratam*, Sabhā 2-315); **జ $\\longleftrightarrow$ చా** (*Amuktamālyada* 4-138); **చ $\\longleftrightarrow$ జే** (*Manu Caritra* 2-29); **జా $\\longleftrightarrow$ చే** (*Manu Caritra* 2-31); **చా $\\longleftrightarrow$ జో** (*Amuktamālyada* 4-163); **జో $\\longleftrightarrow$ చు** (*Bhāgavatam* 8-123); **జా $\\longleftrightarrow$ ఛ** (*Gōpīnātha Rāmāyaṇamu*, Yuddha 2000); **ఛ $\\longleftrightarrow$ జా** (*Bhāgavatam* 10-Pūrvabhāga 136); **జే $\\longleftrightarrow$ ఛా** (*Kavikarṇarasāyanamu* 65); **ఛా $\\longleftrightarrow$ జ** (*Śaśāṅkavijayamu* 3-13); **ఛ $\\longleftrightarrow$ ఝ** (*Amuktamālyada* 5-196); **జ $\\longleftrightarrow$ జౌ** (*Manu Caritra* 2-23); **జు $\\longleftrightarrow$ జు** (*Manu Caritra* 4-36); **జా $\\longleftrightarrow$ ఝ** (*Bhāratam*, Virāṭa 4-134); **జౌ $\\longleftrightarrow$ ఝ** (*Bhāgavatam* 8-131).  
* **Ṭa-Class:** **ఠ $\\longleftrightarrow$ టా** (*Manu Caritra* 1-76); **టి $\\longleftrightarrow$ డె** (*Cārucandrōdayamu* 1-17); **టా $\\longleftrightarrow$ ఢ** (*Bhāratam*, Śānti 1-203); **ఠీ $\\longleftrightarrow$ డి** (*Bhāskara Rāmāyaṇamu*, Yuddha 104); **ఠి $\\longleftrightarrow$ ఢీ** (*Haravilāsam* 2-149); **డ $\\longleftrightarrow$ ఢ** (*Bhāratam*, Udyōga 3-337).  
* **Ta-Class:** **త $\\longleftrightarrow$ థ** (*Amuktamālyada* 4-188); **తా $\\longleftrightarrow$ దా** (*Manu Caritra* 2-22); **ధ $\\longleftrightarrow$ తై** (*Bhāratam*, Sabhā 1-68); **థా $\\longleftrightarrow$ ద** (*Śivarātri Māhātmyamu* 2-2); **దొ $\\longleftrightarrow$ థు** (*Bhāratam*, Sabhā 1-121); **ధ $\\longleftrightarrow$ థ** (*Śivarātri Māhātmyamu* 1-68); **ధీ $\\longleftrightarrow$ దీ** (*Bhāratam*, Udyōga 10-208).  
* **Pa-Class:** **ప $\\longleftrightarrow$ ఫ** (*Bhāratam*, Virāṭa 4-291); **ఫే $\\longleftrightarrow$ పె** (*Bhāskara Rāmāyaṇamu*, Yuddha 755); **ఫీ $\\longleftrightarrow$ పి** (*Bhāskara Rāmāyaṇamu*, Sundara 50); **బ $\\longleftrightarrow$ ప** (*Bhāratam*, Ādi 1-104); **బ $\\longleftrightarrow$ ప** (*Bhāratam*, Udyōga 3324); **పై $\\longleftrightarrow$ బ** (*Bhāratam*, Sabhā 1-108); **భో $\\longleftrightarrow$ పూ** (*Manu Caritra* 4-52); **ఫా $\\longleftrightarrow$ బ** (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 399); **ఫా $\\longleftrightarrow$ భ** (*Bhāgavatam* 1-518); **భి $\\longleftrightarrow$ ఫే** (*Bhāratam*, Udyōga 5-612); **బా $\\longleftrightarrow$ భౌ** (*Manu Caritra* 2-31).  
* **Appakavi's Demonstrative Stanza (3-50):** *కంధి... ఖండిత* (**క-ఖ**); *ఖంజన... గాన* (**ఖ-గా**); *గరుడ... ఘన* (**గ-ఘ**).

---

### Bindu Yatulu: Pre-Stop Anusvāra to Homorganic Nasal (6.12 – 6.12.6)

* **Definition & Mechanics:** When the first four stops of any varga are preceded by a full bindu (*Pūrṇabindu* / *niṇḍusunna* / **ం**), they acquire valid Yati affinity with the **5th consonant (Anunāsika / nasal stop)** of that same class:

$$\\begin{aligned}   \\mathbf{Ka-Class:} &\\quad {\\mathbf{ంక,\\ ంఖ,\\ ంగ,\\ ంఘ}} \\longleftrightarrow \\mathbf{ఙ} \\   \\mathbf{Ca-Class:} &\\quad {\\mathbf{ంచ,\\ ంఛ,\\ ంజ,\\ ంఝ}} \\longleftrightarrow \\mathbf{ఞ} \\   \\mathbf{Ṭa-Class:} &\\quad {\\mathbf{ంట,\\ ంఠ,\\ ండ,\\ ంఢ}} \\longleftrightarrow \\mathbf{ణ} \\   \\mathbf{Ta-Class:} &\\quad {\\mathbf{ంత,\\ ంథ,\\ ంద,\\ ంధ}} \\longleftrightarrow \\mathbf{న} \\   \\mathbf{Pa-Class:} &\\quad {\\mathbf{ంప,\\ ంఫ,\\ ంబ,\\ ంభ}} \\longleftrightarrow \\mathbf{మ}   \\end{aligned}$$

* **Supplementary Function (6.12.1):** A pre-stop bindu does not cancel ordinary consonant rules. In **ంప**, the poet may execute:  
1. *Prāṇi Yati:* **ంప $\\longleftrightarrow$ ప**.  
2. *Vargaja Yati:* **ంప $\\longleftrightarrow$ బ** or **భ**.  
3. *Bindu Yati:* **ంప $\\longleftrightarrow$ మ**.  
* **Etymological & Orthographic Basis (6.12.2):** In Sanskrit manuscripts, pre-consonantal nasals are written with the class anunāsika (e.g., *శఙ్కర, అఞ్చిత, కుణ్డల, శాన్త, స్తమ్భ*). Telugu orthography replaces these conjunct nasals with a zero-symbol bindu (*శంకర, అంచిత, కుండల, శాంత, స్తంబ*). Because Telugu **ంత** is phonologically $\\text{న్} \+ \\text{త}$, the nasal stop **న** is phonemically present and eligible for alliteration. This applies equally to native Telugu roots (e.g., *కుండ $\\longleftrightarrow$ ణ*).  
* **Classical Formulation References (6.12.3):**  
* *Kavijanāśrayamu (Saṁjñā 69):* **ఙా $\\longleftrightarrow$ ంక**, **ఞా $\\longleftrightarrow$ ంఛ**, **ణా $\\longleftrightarrow$ ండ**, **నా $\\longleftrightarrow$ ంధ**, **మా $\\longleftrightarrow$ ంబ**.  
* *Appakavīyamu (3-53):* **జ్ఞా (ఞ) $\\longleftrightarrow$ ంచ**, **ణా $\\longleftrightarrow$ ంఠ**, **న $\\longleftrightarrow$ ంద**, **మ $\\longleftrightarrow$ ంభ**.

#### Canonical Provenance for Bindu Yati (6.12.4)

* **Ṭa-Class with Ṇa:** **ంటా $\\longleftrightarrow$ ణ** (*Bhāskara Rāmāyaṇamu*, Bāla 95); **ణ $\\longleftrightarrow$ ంఠీ** (*Bhāratam*, Udyōga 5-177); **ండ $\\longleftrightarrow$ ణ** (*Bhāgavatam* 10-Pūrvabhāga 341); **ండ $\\longleftrightarrow$ ణె** (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 393); **ండు $\\longleftrightarrow$ ణు** (*Bhāratam*, Virāṭa 6-179).  
* **Ta-Class with Na:** **న $\\longleftrightarrow$ ంత** (*Manu Caritra* 2-12); **నా $\\longleftrightarrow$ ంత** (*Manu Caritra* 2-62); **ంత $\\longleftrightarrow$ నా** (*Bhāratam*, Udyōga 3-253); **నె $\\longleftrightarrow$ ంతే** (*Śivarātri Māhātmyamu* 4-108); **నా $\\longleftrightarrow$ ంథ** (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 37); **ంథ $\\longleftrightarrow$ నా** (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 376); **ంద $\\longleftrightarrow$ నా** (*Bhāgavatam* 10-Pūrvabhāga 1703); **ంది $\\longleftrightarrow$ నీ** (*Amuktamālyada* 4-116); **నా $\\longleftrightarrow$ ంధ** (*Bhāgavatam* 3-174); **ంధ $\\longleftrightarrow$ నా** (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 307); **ంధు $\\longleftrightarrow$ నో** (*Gōpīnātha Rāmāyaṇamu*, Yuddha 2396).  
* **Pa-Class with Ma:** **మ $\\longleftrightarrow$ ంప** (*Vasu Caritra* 1-10); **ంప $\\longleftrightarrow$ మ** (*Śivarātri Māhātmyamu* 1-43); **మో $\\longleftrightarrow$ ంపు** (*Manu Caritra* 4-120); **ంబ $\\longleftrightarrow$ మ** (*Śivarātri Māhātmyamu* 4-210); **ంబా $\\longleftrightarrow$ మా** (*Manu Caritra* 2-54); **ంభా $\\longleftrightarrow$ మై** (*Bhāskara Rāmāyaṇamu*, Bāla 87); **ంభి $\\longleftrightarrow$ మె** (*Manu Caritra* 1-210).

#### Structural Positioning & Boundary Considerations (6.12.5)

1. *Line-Break Bridging:* Bindu Yati is satisfied when the anusvāra sits at the absolute end of the preceding line and the stop opens the subsequent line (e.g., Line 1 ends in **ఘం**, Line 2 opens with **టా** $\\rightarrow$ evaluated as **ంటా $\\longleftrightarrow$ ణ**).  
2. *Druta-Derived Nasal Compounds:* When an inflected drutamu (**న్**) precedes a paruṣa consonant across a line break ($\\text{కోటులన్} \+ \\text{పావను}$), sandhi mutates the cluster into an anusvāra-voiced stop compound (**కోటులంబావను**). This generates a valid Bindu Yati with **మా** (**ంబా $\\longleftrightarrow$ మా**).  
3. *Special Duality for Dental Stops:* When a drutamu encounters an initial dental stop (**త / ద**), the resulting juncture can scan under two distinct metrics:  
* *As Conjunct (Saṁśleṣamu):* **వాడుటన్దేట** $\\rightarrow$ scans via *Saṁyukta Yati* matching **నే $\\longleftrightarrow$ నీ**.  
* *As Pūrṇabindu:* **వాడుటందేట** $\\rightarrow$ scans via *Bindu Yati* matching **ందే $\\longleftrightarrow$ నీ**.  
* Both resolutions are valid because the class nasal for *Ta*\-varga is dental **న**.

---

### 'Na \- Ṇa' Yati / Sarasayati-1: Dental & Retroflex Nasal Affinity (6.13 – 6.13.3)

* **Definition:** Dental **'న'** (*na*) and retroflex **'ణ'** (*ṇa*) possess direct mutual Yati affinity (*Sarasayati*).  
* **Vowel Class Governance:** The pairing must satisfy the tripartite vowel grid:  
* Class 1: **న, నా $\\longleftrightarrow$ ణ, ణా**.  
* Class 2: **ని, నీ, నె, నే $\\longleftrightarrow$ ణి, ణీ, ణె, ణే**.  
* Class 3: **ను, నూ, నొ, నో $\\longleftrightarrow$ ణు, ణూ, ణొ, ణో**.  
* **Neutrality Toward Root Origin (6.13.2):** Classical poetry draws no distinction between radical retroflex *ṇa* (*sahaja*: e.g., *దుర్గుణ* in *Bhāratam*, Sabhā 2-67) and sandhi-derived retroflex *ṇa* (*ādēśa*: e.g., *విదారణ* in *Bhāratam*, Sabhā 2-183); both freely pair with dental **న**.  
* **Canonical Provenance (6.13.3):**  
* **న $\\longleftrightarrow$ ణ** (*Bhāratam*, Ādi 5-253); **న $\\longleftrightarrow$ ణా** (*Manu Caritra* 2-26); **ణ $\\longleftrightarrow$ నా** (*Bhāgavatam* 2-206); **ని $\\longleftrightarrow$ ణీ** (*Manu Caritra* 2-51); **ణి $\\longleftrightarrow$ నీ** (*Bhāskara Rāmāyaṇamu*, Sundara 52); **ణీ $\\longleftrightarrow$ ని** (*Bhāratam*, Ādi 6-17); **నీ $\\longleftrightarrow$ ణీ** (*Bhāratam*, Sabhā 2-80); **నృ $\\longleftrightarrow$ ణి** (*Manu Caritra* 6-23); **నె $\\longleftrightarrow$ ణి** (*Bhāratam*, Sabhā 1-7); **నె $\\longleftrightarrow$ ణీ** (*Manu Caritra* 3-74); **ణీ $\\longleftrightarrow$ నె** (*Bhāratam*, Āraṇya 3-236); **ణు $\\longleftrightarrow$ ను** (*Bhāskara Rāmāyaṇamu*, Sundara 52).  
* *Appakavi's Dual Demonstrative Line (Manu Caritra 8-1):* **ణీ $\\longleftrightarrow$ ని** in Line 2, and **ణా $\\longleftrightarrow$ న** in Line 4\.

---

### Anunāsikākṣara Yati: Cross-Class Nasalized Stop Bridges (6.14 – 6.14.3)

* **Definition:**  
1. Full-bindu-preceded *Ṭa*\-varga stops (**ంట, ంఠ, ండ, ంఢ**) rhyme with dental **న**.  
2. Full-bindu-preceded *Ta*\-varga stops (**ంత, ంథ, ంద, ంధ**) rhyme with retroflex **ణ**.  
* **Derivation Logic (6.14.2):** Formed by intersecting Bindu Yati (6.12) with Na-Ṇa Yati (6.13):

$$\\begin{aligned}   {\\mathbf{ంట,\\ ంఠ,\\ ండ,\\ ంఢ}} &\\xrightarrow{\\text{Bindu Yati}} \\mathbf{ణ} \\xrightarrow{\\text{Na-Ṇa Yati}} \\mathbf{న} \\   {\\mathbf{ంత,\\ ంథ,\\ ంద,\\ ంధ}} &\\xrightarrow{\\text{Bindu Yati}} \\mathbf{న} \\xrightarrow{\\text{Na-Ṇa Yati}} \\mathbf{ణ}   \\end{aligned}$$

* **Strict Class Exclusivity:** This bridge exists **strictly between Ṭa-varga and Ta-varga**. Because the other three class nasals (**ఙ, ఞ, మ**) share no cross-nasal affinity, nasalized *Ka*, *Ca*, and *Pa* stops cannot cross-rhyme with foreign nasals.

                Cross-Class Anunāsikākṣara Architecture

    \[ ంట, ంఠ, ండ, ంఢ \] ──────── Bindu Yati ────────\> \[ ణ (Retroflex Nasal) \]

                                                            │

                                                     Na-Ṇa Yati (6.13)

                                                            │

                                                            ▼

    \[ ంత, ంథ, ంద, ంధ \] ──────── Bindu Yati ────────\> \[ న (Dental Nasal) \]

\`\`\`\[cite: 6\]

&nbsp;

\#\#\#\# Canonical Provenance for Anunāsikākṣara Yati (6.14.3)

\* \*\*Nasalized Ṭa-Stops with Dental Na:\*\*

  \* \*\*న $\\longleftrightarrow$ ంటా:\*\* \*...పురఘంటావీథినేతెంచుచోన్\* (\*Nalacaritra\* 7-21)\[cite: 6\].

  \* \*\*నా $\\longleftrightarrow$ ంట:\*\* \*...మింటం క్రొత్తనానేల నా...\* (\*Amuktamālyada\* 2-42)\[cite: 6\].

  \* \*\*ంట $\\longleftrightarrow$ నా:\*\* \*...పిండివంటలు పాల్తేనియ...\* (\*Appakavīyamu\* 3-65 / \*Amuktamālyada\* 2-127)\[cite: 6\].

  \* \*\*ంటి $\\longleftrightarrow$ నీ:\*\* \*...గెంటినది నిజంబుగాఁ దనువునీడకు...\* (\*Bhāratam\*, Virāṭa 8-96)\[cite: 6\].

  \* \*\*ంటు $\\longleftrightarrow$ ను:\*\* \*...ఒక్కింత ముఖానురాగమును బూనుం...\* (\*Manu Caritra\* 3-95)\[cite: 6\].

  \* \*\*ంఠ $\\longleftrightarrow$ నా:\*\* \*...ఠనములనాడుచును దొంగనాసామీ...\* (\*Manu Caritra\* 4-87)\[cite: 6\].

  \* \*\*ని $\\longleftrightarrow$ ంఠే:\*\* \*నిధులు తొమ్మిదియు కంఠేకాలునకు...\* (\*Bhāgavatam\* 7-152)\[cite: 6\].

  \* \*\*న $\\longleftrightarrow$ ండ:\*\* \*నవమృణాళిక దండఖండంబు...\* (\*Haravilāsam\* 4-39)\[cite: 6\].

  \* \*\*ండ $\\longleftrightarrow$ నా:\*\* \*...మహీమండల మెల్లను జూచినాడ...\* (\*Appakavīyamu\* 3-64 / \*Bhāskara Rāmāyaṇamu\*, Sundara 614)\[cite: 6\].

  \* \*\*ండి $\\longleftrightarrow$ ని:\*\* \*...పండించితివోయి దాసరి వనిందెరు...\* (\*Amuktamālyada\* 6-40)\[cite: 6\].

  \* \*\*ండు $\\longleftrightarrow$ ను:\*\* \*...పరాశరాత్మజుండు మనుజనాథు...\* (\*Bhāratam\*, Virāṭa 4-82)\[cite: 6\].

\* \*\*Nasalized Ta-Stops with Retroflex Ṇa:\*\*

  \* \*\*తా $\\longleftrightarrow$ ణ:\*\* \*...హింతాల ముఖద్రుమంబుల...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 701)\[cite: 6\].

  \* \*\*ంత $\\longleftrightarrow$ ణ:\*\* \*...సంతతమును హస్త కంకణ ఝణత్కరణ...\* (\*Bhāgavatam\* 8-232)\[cite: 6\].

  \* \*\*తే $\\longleftrightarrow$ ణీ:\*\* \*...యెంతే వడి మింటనేగు ధరణీసుతఁ...\* (\*Gōpīnātha Rāmāyaṇamu\*, Araṇya 941)\[cite: 6\].

  \* \*\*ణ $\\longleftrightarrow$ ంద:\*\* \*...దర్పణంబులై ముద్దుచెక్కులందంబునొందె\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 86)\[cite: 6\].

  \* \*\*ంద $\\longleftrightarrow$ ణ:\*\* \*...ధర్మనందనమఖవాహరక్ష చణస్థితి...\* (\*Bhāratam\*, Virāṭa 7-74)\[cite: 6\].

  \* \*\*ంది $\\longleftrightarrow$ ణీ:\*\* \*...మందిరముననక్కుమారుని మణీమయ...\* (\*Amuktamālyada\* 2-74)\[cite: 6\].

  \* \*\*ంధ $\\longleftrightarrow$ ణ:\*\* \*...దశకంధరు తేజంబున విభూషణ...\* (\*Gōpīnātha Rāmāyaṇamu\*, Sundara 242)\[cite: 6\].

  \* \*\*ంధి $\\longleftrightarrow$ ణి:\*\* \*...సంధిల్లఁగ భావిభర్తకు ఫణిప్రభు...\* (\*Kumārasambhavamu\* 3-75)\[cite: 6\].

  \* \*\*ణు $\\longleftrightarrow$ ంధు:\*\* \*...బాణుని భాసున్ భవభూతి భారవి సుబంధున్...\* (\*Manu Caritra\* 1-7)\[cite: 6\].

&nbsp;

\---

&nbsp;

\#\#\# Anusvāra Sambandha Yati: Resonant Bridge Between Ṭa and Ta Classes (6.15 – 6.15.3)

&nbsp;

\* \*\*Definition:\*\* Full-bindu-preceded \*Ṭa\*-varga stops (\*\*ంట, ంఠ, ండ, ంఢ\*\*) possess mutual Yati affinity with full-bindu-preceded \*Ta\*-varga stops (\*\*ంత, ంథ, ంద, ంధ\*\*)\[cite: 6\]:

  $$\\{\\mathbf{ంట,\\ ంఠ,\\ ండ,\\ ంఢ}\\} \\quad\\longleftrightarrow\\quad \\{\\mathbf{ంత,\\ ంథ,\\ ంద,\\ ంధ}\\}$$

\[cite: 6\]

\* \*\*Structural Domain (6.15.1):\*\* Generates 16 direct cluster pairings (\*\*ంట-ంత, ంట-ంథ, ంట-ంద, ంట-ంధ, ంఠ-ంత... ంఢ-ంధ\*\*) across all three vowel classes (e.g., \*\*ంటి $\\longleftrightarrow$ ంతి, ంటు $\\longleftrightarrow$ ంతు\*\*)\[cite: 6\].

\* \*\*Class Limitation (6.15.3):\*\* This bridge operates \*\*exclusively between the Ṭa and Ta classes\*\*\[cite: 6\]. Bindu-preceded stops of \*Ka\*, \*Ca\*, and \*Pa\* cannot participate in Anusvāra Sambandha Yati\[cite: 6\].

&nbsp;

\#\#\#\# Canonical Provenance for Anusvāra Sambandha Yati (6.15.2)

\* \*\*ంద $\\longleftrightarrow$ ంట:\*\* \*...పెక్కు చందాలంబండునొకప్పుడుం దఱుఁగదింటం బాఁడియుం బంటయున్...\* (\*Appakavīyamu\* 3-59 / \*Manu Caritra\* 1-55)\[cite: 6\].

\* \*\*ంద $\\longleftrightarrow$ ండ:\*\* \*...వసుంధర యందొక్కఁడు మంత్రియయ్యె వినుకొండన్...\* (\*Appakavīyamu\* 3-60, Rāvipāṭi Tipparāju Chāṭu)\[cite: 6\].

\* \*\*ంధ $\\longleftrightarrow$ ంట:\*\* \*...పంకేజ బాంధవ భానుప్రతతుల్ హరింపఁగుయి వెంటన్వెళ్ళు...\* (\*Appakavīyamu\* 3-61 / \*Amuktamālyada\* 2-48)\[cite: 6\].

\* \*\*ండ $\\longleftrightarrow$ ంతా:\*\* \*...కోదండలి యారాత్రికముల్ ఘటింప బుధసంతానంబు...\* (\*Śivarātri Māhātmyamu\* 6-57)\[cite: 6\].

\* \*\*ండ $\\longleftrightarrow$ తా:\*\* \*...బాలకాండము నీభక్తుఁడు శోభనాద్రిదగు సంతానంబు...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 298)\[cite: 6\].

\* \*\*ండ $\\longleftrightarrow$ ందా:\*\* \*...ప్రచండ లసద్వైఖరి వీచి రామవిభునిం దాఁకంగ...\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1364)\[cite: 6\].

\* \*\*ండి $\\longleftrightarrow$ దీ:\*\* \*...గాండివ కోదండవినిర్గతప్రబలసందీప్తాస్త్ర...\* (\*Bhāgavatam\* 1-90)\[cite: 6\].

\* \*\*ండి $\\longleftrightarrow$ ంధి:\*\* \*...దోషముండిన నాయందుననుండు ధర్మమగు సంధింజూడుమట్లెంచ...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 131)\[cite: 6\].

&nbsp;

\---

&nbsp;

\#\#\# Analytical Guardrail: The Prohibition of Unauthorized Transitive Chaining (6.15.4)

&nbsp;

\* \*\*The Fallacy of False Transitivity:\*\* An automated engine must \*\*not\*\* infer transitive yati bridges between arbitrary sounds merely because they share a theoretical intermediate link\[cite: 6\].

\* \*\*The Counter-Example:\*\*

  $$\\begin{aligned}   \\text{Fact 1:} &\\quad \\mathbf{ఇ} \\longleftrightarrow \\mathbf{ఋ} \\quad (\\text{Svaramaitri Yati, 6.2.1}) \\\\   \\text{Fact 2:} &\\quad \\mathbf{ఋ} \\longleftrightarrow \\mathbf{రి} \\quad (\\text{R̥ Yati, 6.5})   \\end{aligned}$$

\[cite: 6\]

\* \*\*The Impermissible Deduction:\*\* One cannot deduce that $\\mathbf{ఇ} \\longleftrightarrow \\mathbf{రి}$\[cite: 6\]\! Pairing independent vowel \*\*'ఇ'\*\* with consonant \*\*'రి'\*\* is an ungrammatical, unauthorized violation of classical canon (\*śāstra-viruddhamu\*, \*asaṁpradāyamu\*)\[cite: 6\].

\* \*\*Engine Implementation Rule:\*\* Cross-class and compound yati bridges are valid \*\*only when explicitly sanctioned by classical prosodic treatises and attested in Mahākavi usage\*\*\[cite: 6\]. Synthesized or extrapolated transitive bridges must be rejected as invalid\[cite: 6\].

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.16 ఋజుయతి (R̥ju Yati — Direct 'Ya' and 'Ha' Consonant Affinity)

* **Definition & Mechanics:** Dental/palatal glide **'య'** (*ya*) and glottal aspirate **'హ'** (*ha*) possess mutual, direct Yati affinity.  
* **Etymology & Nomenclature:** Designated **ఋజుయతి** (*R̥ju Yati* \= Straightforward/Direct Yati) because it establishes an unencumbered, linear phonetic bridge between two seemingly distinct consonants without requiring intermediary sandhi or nasal markers.  
* **Vowel-Class Governance (6.11.1 Integration):** Because both elements are consonants, they must strictly align under the tripartite vowel grid (*Svaramaitri Vargamulu*):  
* *Class 1 ($A$-varga: అ, ఆ, ఐ, ఔ):* **య, యా, యై, యౌ $\\longleftrightarrow$ హ, హా, హై, హౌ**.  
* *Class 2 ($I$-varga: ఇ, ఈ, ఋ, ౠ, ఎ, ఏ):* **యి, యీ, యె, యే $\\longleftrightarrow$ హి, హీ, హృ, హె, హే**.  
* *Class 3 ($U$-varga: ఉ, ఊ, ఒ, ఓ):* **యు, యూ, యొ, యో $\\longleftrightarrow$ హు, హూ, హెు, హెూ**.

#### Canonical Provenance for R̥ju Yati (6.16.1)

* **Class 1 ($A$-varga):**  
* **య $\\longleftrightarrow$ హ:** *యజనస్వాధ్యాయకవ్యహవ్యతపో దా...* (*Bhāratam*, Ādi 8-101).  
* **య $\\longleftrightarrow$ హ:** *యజ్జల దేవతాస్ఫటిక హర్మ్యము శేషుఁడు...* (*Kāśīkhaṇḍam* 5-136).  
* **హ $\\longleftrightarrow$ య:** *మహా మనోహరసుచరిత్ర పావన పయః...* (*Bhāratam*, Ādi 1-24).  
* **హ $\\longleftrightarrow$ య:** *హరితనయుండు పార్థుఁడు రయంబుననందఱనాహవక్రియా...* (*Bhāratam*, Ādi 8-201).  
* **హ $\\longleftrightarrow$ య:** *హరి గలుగంగనేటికి భయంబున వచ్చితి...* (*Bhāratam*, Virāṭa 3-65).  
* **హ $\\longleftrightarrow$ యా:** *హరుఁడును సర్వమేధమను యాగమునం బ్రచురప్రకాశతన్...* (*Bhāratam*, Udyōga 1-145).  
* **య $\\longleftrightarrow$ హా:** *యక్ష సిద్ధ సాధ్య ఖేవిహార గరుడ కిన్నరా...* (*Amuktamālyada* 3-202, Utsāha).  
* **హా $\\longleftrightarrow$ యా:** *హాయను ధర్మరాజతనయా యను నన్నెడఁబాయ...* (*Bhāratam*, Drōṇa 2-242).  
* **హ $\\longleftrightarrow$ యౌ:** *...దోహల రుచినొప్పె గౌరి నవయౌవన సంగమలీల...* (*Bhāratam*, Āraṇya 3-40).  
* **యౌ $\\longleftrightarrow$ హా:** *యౌవనాంభోధరోద్భూత హావభావ...* (*Kāśīkhaṇḍam* 3-155).  
* **Class 2 ($I$-varga):**  
* **హృ $\\longleftrightarrow$ యి:** *హృదయసముద్భవుఁడువాఁడయిన యదు...* (*Bhāratam*, Ādi 3-198).  
* **హృ $\\longleftrightarrow$ యి:** *...వికచ హృదయుఁడై తలచీర యాయితము సేసి...* (*Bhāratam*, Sabhā 2-323).  
* **హి $\\longleftrightarrow$ యె:** *హితమతినేఁగుదెంచి కనియెం బ్రభుసంవరణుం...* (*Bhāratam*, Ādi 7-83).  
* **Class 3 ($U$-varga):**  
* **హు $\\longleftrightarrow$ యు:** *...బాహుకునకుఁ బ్రీతితోడ విధియుక్తముగానుపదేశమిచ్చెన...* (*Bhāratam*, Āraṇya 2-177).

---

### 6.17 సరసయతి-2: 'అ-య'ల యతి (Sarasayati-2 — Vowel 'A' to Consonant 'Ya')

* **Definition & Mechanics:** Vowel **'అ'** (*a*) and consonant **'య'** (*ya*) possess mutual Yati affinity (*Sarasayati*).  
* **Cross-Taxonomic Anomaly:** Bridges an independent vocalic sound (అచ్చు) with a consonantal glide (హల్లు).  
* **Vowel-Class Expansion:** Because the consonant 'య' must carry an attached vowel harmonized with the vowel class of the rhyming partner, this rule expands across all three equivalence groups:  
* *Class 1:* ${\\text{అ, ఆ, ఐ, ఔ}} \\longleftrightarrow {\\text{య, యా, యై, యౌ}}$.  
* *Class 2:* ${\\text{ఇ, ఈ, ఋ, ఎ, ఏ}} \\longleftrightarrow {\\text{యి, యీ, యె, యే}}$.  
* *Class 3:* ${\\text{ఉ, ఊ, ఒ, ఓ}} \\longleftrightarrow {\\text{యు, యూ, యొ, యో}}$.

                 Sarasayati-2 Vowel-to-Glide Architecture

     Class 1 Vowels: { అ,  ఆ,  ఐ,  ఔ }  \<───\>  { య,  యా,  యై,  యౌ } (య్ \+ Class 1\)

     Class 2 Vowels: { ఇ,  ఈ,  ఋ,  ఎ,  ఏ } \<───\>  { యి,  యీ,  యె,  యే } (య్ \+ Class 2\)

     Class 3 Vowels: { ఉ,  ఊ,  ఒ,  ఓ }  \<───\>  { యు,  యూ,  యొ,  యో } (య్ \+ Class 3\)

\`\`\`\[cite: 7\]

&nbsp;

\#\#\#\# Engine Disambiguation: Śabda-Siddha vs. Āgama 'Ya' (6.17.1)

An automated parser must strictly isolate the morphological origin of 'య' before applying Sarasayati\[cite: 7\]:

1\. \*\*శబ్దసిద్ధ యకారము (Alaghu Ya-kāra / Lexical Root):\*\* Inherent root consonants (e.g., \*యజ్ఞము, మాయ, కాయ, నూయి, సముదయ\*) execute \*\*true Sarasayati\*\*\[cite: 7\].

   \* \*Example:\* \*అమలిన... సముదయంబుల...\* $\\rightarrow$ root 'య' rhymes with line-start \*\*అ\*\* under Sarasayati\[cite: 7\].

2\. \*\*ఆగమ యకారము (Laghu Ya-kāra / Yaḍāgama Augment):\*\* Glides inserted dynamically via hiatus-prevention sandhi (\*యడాగమము\*, e.g., $\\text{విని} \+ \\text{అల్గి} \\rightarrow \\text{వినియల్గి}$) are phonologically empty markers\[cite: 7\].

   \* \*Resolution:\* The engine must \*\*bypass the augment 'య'\*\* and execute \*\*స్వరప్రధాన యతి (Svara-Pradhāna Yati)\*\* directly to the underlying initial vowel (\*para-padādi svara\*): $\\mathbf{అ \\longleftrightarrow అ}$\[cite: 7\]\!

   \* \*Example:\* \*అమరవిభుండు దానివిని యల్గి...\* $\\rightarrow$ scanned as \*\*అ $\\longleftrightarrow$ అ\*\* via \*Svara-Pradhāna\*, \*\*never\*\* as an \*A-Ya\* Sarasayati match\[cite: 7\]\!

&nbsp;

\#\#\#\# Canonical Provenance for Sarasayati-2 (6.17.2 – 6.17.3)

\* \*\*Vowel-to-Ya (అ $\\rightarrow$ య):\*\*

  \* \*\*అ $\\longleftrightarrow$ య:\*\* \*అమ్మనుజేంద్రుఁడైన నలుయజ్ఞము...\* (\*Bhāratam\*, Āraṇya 2-223)\[cite: 7\]; \*అనఘులు ధారుణీసురులయః ప్రద...\* (\*Amuktamālyada\* 4-156)\[cite: 7\]; \*...దత్తనైతి / నమ్మహీశునకు నయంబుననెయ్యది...\* ($\\text{న్} \+ \\text{అ} \\longleftrightarrow \\text{య}$) (\*Bhāratam\*, Ādi 4-213)\[cite: 7\].

  \* \*\*అ $\\longleftrightarrow$ యా:\*\* \*అంకముఁజేరి శైలతనయాస్తన...\* (\*Manu Caritra\* 1-4)\[cite: 7\]; \*అతఁడట్హౌషధహీనుఁడై నిజపురీ యాత్రా...\* (\*Manu Caritra\* 2-14)\[cite: 7\].

  \* \*\*ఆ $\\longleftrightarrow$ య:\*\* \*ఆదిజుఁడైన బ్రహ్మయుదయంబునకాస్పదమైనవాఁడు...\* (\*Bhāratam\*, Sabhā 2-18)\[cite: 7\]; \*ఆ విపరీతముల్గని భయంపడి...\* (\*Bhāratam\*, Udyōga 5-112)\[cite: 7\]; \*ఆ రమణీయ యౌవనవయః...\* (\*Manu Caritra\* 2-13)\[cite: 7\].

  \* \*\*ఆ $\\longleftrightarrow$ యా:\*\* \*ఆయతకీర్తితో వివిధ యాగములన్...\* (\*Bhāratam\*, Ādi 1-89)\[cite: 7\]; \*ఆ నహుషాత్మజుండగు యయాతి...\* (\*Bhāratam\*, Ādi 3-139)\[cite: 7\].

  \* \*\*ఐ $\\longleftrightarrow$ య:\*\* \*ఐనను దీనిఁబాపఁదగు యత్నము...\* (\*Bhāratam\*, Āraṇya 3-307)\[cite: 7\].

  \* \*\*ఔ $\\longleftrightarrow$ య:\*\* \*ఔరా రాగము బాపురే యొదుగు ఠాయంబుల్...\* (\*Amuktamālyada\* 3-143)\[cite: 7\].

  \* \*\*ఈ $\\longleftrightarrow$ యి:\*\* \*ఈ వసుధాధినాథులు జయించిన యట్టిద...\* (\*Bhāratam\*, Ādi 4-205)\[cite: 7\].

  \* \*\*యి $\\longleftrightarrow$ ఎ (via Sandhi):\*\* \*...పోయితి దుష్టాత్ములఁ గూడి దానికి ఫలంబెట్లయ్యెనో...\* ($\\text{ఫలంబు} \+ \\text{ఎట్లు} \\rightarrow \\mathbf{ఎ} \\longleftrightarrow \\mathbf{యి}$) (\*Bhāratam\*, Ādi 6-61)\[cite: 7\].

  \* \*\*ఉ $\\longleftrightarrow$ యు:\*\* \*ఉద్రేకంబున రారు శస్త్రధరులై యుద్ధావనిన్...\* (\*Bhāratam\*, Udyōga 1-161)\[cite: 7\].

  \* \*\*యు $\\longleftrightarrow$ ఉ (via Sandhi):\*\* \*...చిరాయువు బహుపుత్రలాభ విభవోన్నతియున్...\* ($\\text{విభవ} \+ \\text{ఉన్నతి} \\rightarrow \\mathbf{ఉ} \\longleftrightarrow \\mathbf{యు}$) (\*Bhāratam\*, Ādi 3-72)\[cite: 7\].

  \* \*\*ఉ $\\longleftrightarrow$ యో:\*\* \*ఉండునితండు పద్మజునియోగమునన్...\* (\*Bhāratam\*, Ādi 2-87)\[cite: 7\].

  \* \*\*ఊ $\\longleftrightarrow$ యో:\*\* \*ఊఁచిన కఱ్ఱ వంపని పయోరుహలోచన...\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 163)\[cite: 7\].

  \* \*\*ఒ $\\longleftrightarrow$ యో:\*\* \*ఒంటినిల్చి పురాణ యోగులు యోగమార్గ...\* (\*Bhāgavatam\* 10-Pūrvabhāga 127, Mattakōkila)\[cite: 7\].

\* \*\*Ya-to-Vowel Inversions (య $\\rightarrow$ అ):\*\*

  \* \*\*య $\\longleftrightarrow$ అ:\*\* \*యతి సంఘంబుల సంగతిన్ దురితకర్మాపేతుఁడై...\* ($\\text{కర్మ} \+ \\text{అపేతుఁడై}$) (\*Bhāratam\*, Ādi 5-64)\[cite: 7\]; \*...వైశంపాయనుఁడవితథపుణ్య...\* ($\\text{యనుఁడు} \+ \\text{అవితథ}$) (\*Bhāratam\*, Ādi 4-273)\[cite: 7\]; \*...లోకములా యతిఁ బెక్కులుగలవు నాకుననుభావ్యములై...\* ($\\text{నాకున్} \+ \\text{అనుభావ్యములై}$) (\*Bhāratam\*, Ādi 4-190)\[cite: 7\].

  \* \*\*యా $\\longleftrightarrow$ అ:\*\* \*యావకద్రవముననరుణాంఘ్ర...\* ($\\text{ద్రవమునన్} \+ \\text{అరుణ}$) (\*Amuktamālyada\* 5-128)\[cite: 7\].

  \* \*\*యౌ $\\longleftrightarrow$ అ:\*\* \*యౌవనదర్పమంది జనమంతకునంతకునగ్గలింప...\* ($\\text{జనము} \+ \\text{అంతకున్}$) (\*Bhāratam\*, Anuśāsanika 1-203)\[cite: 7\].

  \* \*\*య $\\longleftrightarrow$ ఆ:\*\* \*యమనియమాదిలభ్య... జరన్మరుదిభ్య సంసృతి...\* (\*Amuktamālyada\* 5-99)\[cite: 7\]; \*యదుకులనాథ యిప్పుడితఁడాగ్రహవృత్తి...\* ($\\text{ఇతఁడు} \+ \\text{ఆగ్రహ}$) (\*Bhāratam\*, Sabhā 4-304)\[cite: 7\]; \*అమ్మంత్రము దనదగు హృదయమ్ముననక్కన్య నిలిపి యాదిత్యునకున్...\* (\*Bhāratam\*, Ādi 5-19)\[cite: 7\].

  \* \*\*యా $\\longleftrightarrow$ ఆ:\*\* \*యాదవ సార్వభౌమ భయదాయత బాహు...\* (\*Amuktamālyada\* 5-7)\[cite: 7\].

  \* \*\*యౌ $\\longleftrightarrow$ ఆ:\*\* \*యౌవనమందు యజ్వయు ధనాఢ్యుఁడునై...\* (\*Manu Caritra\* 1-53)\[cite: 7\].

  \* \*\*య $\\longleftrightarrow$ ఐ:\*\* \*యదువంశంబున లోకరక్షణపరుండై...\* ($\\text{పరుండు} \+ \\text{ఐ}$) (\*Bhāgavatam\* 5-97)\[cite: 7\]; \*...లోయకుఁదలక్రిందుగా మలఁకలై...\* (\*Manu Caritra\* 2-21)\[cite: 7\].

  \* \*\*ఐ $\\longleftrightarrow$ యా:\*\* \*...తనయుండై నెగడెనతండుగనె యయాతినరేంద్రున్...\* (\*Manu Caritra\* 1-20)\[cite: 7\].

  \* \*\*యౌ $\\longleftrightarrow$ ఐ:\*\* \*యౌవనుండనై ధన్యుండనైతి...\* (\*Bhāratam\*, Āraṇya 3-187)\[cite: 7\].

  \* \*\*య $\\longleftrightarrow$ ఔ:\*\* \*యతి రుజఁబొందినం దొఱఁగనౌషధ కృత్యముఁ...\* ($\\text{దొఱఁగన్} \+ \\text{ఔషధ}$) (\*Bhāratam\*, Anuśāsanika 3-294)\[cite: 7\].

  \* \*\*యి $\\longleftrightarrow$ ఇ:\*\* \*...గుప్తమయిన యమృతముదెచ్చి మీకునిచ్చితి...\* ($\\text{మీకున్} \+ \\text{ఇచ్చితి}$) (\*Bhāratam\*, Ādi 2-118)\[cite: 7\].

  \* \*\*యు $\\longleftrightarrow$ ఉ:\*\* \*...సంయుతముగ యజ్ఞశాల సరయూత్తరమందు...\* ($\\text{సరయూ} \+ \\text{ఉత్తర}$) (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 309)\[cite: 7\]; \*...యతియును యోగియుఁ బాత్రములు తదుత్తమ...\* ($\\text{తత్} \+ \\text{ఉత్తమ}$) (\*Bhāskara Rāmāyaṇamu\*, Bāla 145)\[cite: 7\]; \*...నుండె శిష్ట సంప్రయుక్తిఁ జేసి...\* ($\\text{న్} \+ \\text{ఉండె} \\longleftrightarrow \\text{యు}$) (\*Bhāratam\*, Ādi 5-85)\[cite: 7\].

  \* \*\*యో $\\longleftrightarrow$ ఉ:\*\* \*యోధుల సింహనాదము మదోత్కట...\* ($\\text{మద} \+ \\text{ఉత్కట}$) (\*Bhāratam\*, Sabhā 1-266)\[cite: 7\]; \*యోగతంత్రంబు సకల శాస్త్రోదితంబు...\* ($\\text{శాస్త్ర} \+ \\text{ఉదితంబు}$) (\*Bhāgavatam\* 5-598)\[cite: 7\]; \*...భేదించుచుండెడు దుర్జన యోధవరుల...\* ($\\text{చున్} \+ \\text{ఉండెడు} \\longleftrightarrow \\text{యో}$) (\*Bhāratam\*, Āraṇya 3-206)\[cite: 7\].

  \* \*\*యో $\\longleftrightarrow$ ఊ:\*\* \*యోజనగంధినందనుఁడునూర్వశిపట్టియు...\* ($\\text{నందనుఁడున్} \+ \\text{ఊర్వశి}$) (\*Manu Caritra\* 2-84)\[cite: 7\].

  \* \*\*యో $\\longleftrightarrow$ ఒ:\*\* \*యోగీశ్వరులే మహాత్మునొండెఱుఁగక...\* ($\\text{మహాత్మున్} \+ \\text{ఒండు}$) (\*Bhāgavatam\* 8-80)\[cite: 7\].

  \* \*\*యు $\\longleftrightarrow$ ఒ:\*\* \*...భయత్రాత యునుననఁగనింతులకు మువ్వురోగిన గురువులు...\* ($\\text{మువ్వురు} \+ \\text{ఒగిన్}$) (\*Bhāratam\*, Ādi 4-49, Madhurākkara)\[cite: 7\].

  \* \*\*ఓ $\\longleftrightarrow$ యు:\*\* \*...నెమ్మినిటీఁగనోపుదే యనిన శంతనుఁడు గాంగేయు యువరాజుఁ...\* ($\\text{న్} \+ \\text{ఓ} \\longleftrightarrow \\text{యు}$) (\*Bhāratam\*, Ādi 4-177, Madhyākkara)\[cite: 7\].

&nbsp;

\---

&nbsp;

\#\#\# 6.18 సరసయతి-3: 'అ-హ'ల యతి (Sarasayati-3 — Vowel 'A' to Consonant 'Ha')

&nbsp;

\* \*\*Definition & Mechanics:\*\* Vowel \*\*'అ'\*\* (\*a\*) and glottal aspirate \*\*'హ'\*\* (\*ha\*) possess mutual Yati affinity (\*Sarasayati\*)\[cite: 7\].

\* \*\*Cross-Taxonomic Anomaly:\*\* Links pure vowel states with the aspirate fricative consonant\[cite: 7\].

\* \*\*Vowel-Class Expansion:\*\* Harmonizes across the three primary vowel classes\[cite: 7\]:

  \* \*Class 1 ($A$-varga):\* $\\{\\text{అ, ఆ, ఐ, ఔ}\\} \\longleftrightarrow \\{\\text{హ, హా, హై, హౌ}\\}$\[cite: 7\].

  \* \*Class 2 ($I$-varga):\* $\\{\\text{ఇ, ఈ, ఋ, ఎ, ఏ}\\} \\longleftrightarrow \\{\\text{హి, హీ, హృ, హె, హే}\\}$\[cite: 7\].

  \* \*Class 3 ($U$-varga):\* $\\{\\text{ఉ, ఊ, ఒ, ఓ}\\} \\longleftrightarrow \\{\\text{హు, హూ, హెు, హెూ}\\}$\[cite: 7\].

&nbsp;

&nbsp;

             Sarasayati-3 Vowel-to-Aspirate Architecture

 Class 1 Vowels: { అ,  ఆ,  ఐ,  ఔ }  \<───\>  { హ,  హా,  హై,  హౌ } (హ్ \+ Class 1\)

 Class 2 Vowels: { ఇ,  ఈ,  ఋ,  ఎ,  ఏ } \<───\>  { హి,  హీ,  హృ,  హె,  హే } (హ్ \+ Class 2\)

 Class 3 Vowels: { ఉ,  ఊ,  ఒ,  ఓ }  \<───\>  { హు,  హూ,  హెు,  హెూ } (హ్ \+ Class 3\)

&nbsp;

&nbsp;

\#\#\#\# Canonical Provenance for Sarasayati-3 (6.18.1)

\* \*\*Vowel-to-Ha (అ $\\rightarrow$ హ):\*\*

  \* \*\*అ $\\longleftrightarrow$ హ:\*\* \*అనిలజుఁడుగ్రుఁడై ద్రుపద హస్తి ఘటావలినశ్వసంహతిన్...\* (\*Bhāratam\*, Ādi 6-79)\[cite: 7\]; \*అఖిల లోకములకు హరిదైవతము...\* (\*Bhāgavatam\* 7-454)\[cite: 7\].

  \* \*\*అ $\\longleftrightarrow$ హా:\*\* \*అనుచుఁ గ్రమ్మఱువేళ నీహారవారి...\* (\*Manu Caritra\* 2-13)\[cite: 7\].

  \* \*\*అ $\\longleftrightarrow$ హై:\*\* \*అల పతి గాంచెఁజెంత ఘనహైమగుహాగృహ...\* (\*Śivarātri Māhātmyamu\* 1-167)\[cite: 7\].

  \* \*\*ఆ $\\longleftrightarrow$ హ:\*\* \*ఆసమయంబునం గనకహంసము హంసపథంబు...\* (\*Kāśīkhaṇḍam\* 4-105)\[cite: 7\].

  \* \*\*ఆ $\\longleftrightarrow$ హా:\*\* \*ఆలస్యంబొకయింత లేదు శుచి యాహారంబు...\* (\*Bhāratam\*, Udyōga 4-190)\[cite: 7\].

  \* \*\*ఇ $\\longleftrightarrow$ హి:\*\* \*ఇట్లు నారాయణుఁడు దేవహితముకొఱకు...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 388)\[cite: 7\].

  \* \*\*ఇ $\\longleftrightarrow$ హీ:\*\* \*ఇమ్మనుజేంద్రనందనులహీనబలుల్...\* (\*Bhāratam\*, Ādi 7-180)\[cite: 7\].

  \* \*\*ఇ $\\longleftrightarrow$ హృ:\*\* \*ఇవ్విధంబునఁగాంచి హృదయేశు మన్నన...\* (\*Amuktamālyada\* 1-74)\[cite: 7\].

  \* \*\*ఈ $\\longleftrightarrow$ హి:\*\* \*ఈ రఘువంశవర్యుఁడు సహిష్ణుఁడు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 162)\[cite: 7\].

  \* \*\*ఈ $\\longleftrightarrow$ హీ:\*\* \*ఈ నరనాథనందనుఁడహీనపరాక్రమలీల...\* (\*Bhāgavatam\* 8-97)\[cite: 7\]; \*ఈ దురవస్థకడ్డువడి హీనుని విప్రునిఁగాచెనంచునీ...\* (\*Bhāratam\*, Sabhā 6-36)\[cite: 7\].

  \* \*\*ఈ $\\longleftrightarrow$ హె:\*\* \*ఈసునఁబుట్టి డెందమున హెచ్చిన శోకదవానలంబుచే...\* (\*Manu Caritra\* 1-133)\[cite: 7\].

  \* \*\*ఈ $\\longleftrightarrow$ హే:\*\* \*ఈషాదండము సీరతుండముననిన్ హేరాళమై...\* (\*Bhāgavatam\* 6-67)\[cite: 7\].

  \* \*\*ఋ $\\longleftrightarrow$ హి:\*\* \*ఋశ్యశృంగునిఁ బత్నీసహితునిఁజేసి...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 287)\[cite: 7\].

  \* \*\*హి $\\longleftrightarrow$ ఋ:\*\* \*హితమొనర్పఁగబూని ఋశ్యమూకమునకు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 381)\[cite: 7\].

  \* \*\*ఏ $\\longleftrightarrow$ హి:\*\* \*ఏల పార్థుపరాక్రమంబు సహింపనాతనినాహవ...\* (\*Bhāratam\*, Ādi 8-205, Mattakōkila)\[cite: 7\].

  \* \*\*ఏ $\\longleftrightarrow$ హృ:\*\* \*ఏమెఱుంగని పనియని హృదయవీథి...\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 103)\[cite: 7\].

  \* \*\*ఒ $\\longleftrightarrow$ హు:\*\* \*ఒండొరుల సరోషహుంకృతిఁగెరలుచు...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 224)\[cite: 7\].

  \* \*\*ఓ $\\longleftrightarrow$ హెూ:\*\* \*ఓ రఘువర్య రాక్షసుని హెూమము పూర్ణముగాకమున్నె...\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1884)\[cite: 7\].

\* \*\*Ha-to-Vowel Inversions (హ $\\rightarrow$ అ):\*\*

  \* \*\*హ $\\longleftrightarrow$ అ:\*\* \*హరునకుఁ జూడఁగా మహిఁ జరాచర...\* ($\\text{చర} \+ \\text{ఆచర}$) (\*Bhāratam\*, Udyōga 6-162)\[cite: 7\]; \*హరచూడా హరిణాంక... కాలాంతస్ఫురచ్చండికా...\* ($\\text{కాల} \+ \\text{అంత}$) (\*Manu Caritra\* 1-11)\[cite: 7\]; \*...ప్రహస్తుఁడు నీలునిమీఁద...\* ($\\text{దోష} \+ \\text{అట} \\longleftrightarrow \\text{హ}$) (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1051)\[cite: 7\]; \*...హతబలుఁడు హిరణ్యకశిపుఁడనఁ బుట్టె సుతుండు...\* ($\\text{సుతుండు} \+ \\text{అనన్}$) (\*Bhāratam\*, Ādi 3-62)\[cite: 7\]; \*...పుత్రునకయ్యుతథ్యుండు బృహస్పతియును...\* ($\\text{పుత్రునకున్} \+ \\text{అయ్యుతథ్యుండు} \\longleftrightarrow \\text{హ}$) (\*Bhāratam\*, Ādi 3-66)\[cite: 7\]; \*హదను వచ్చుదాఁకనపరాధిపై రోష...\* ($\\text{దాఁకన్} \+ \\text{అపరాధి}$) (\*Bhāskara Rāmāyaṇamu\*, Sundara 246)\[cite: 7\]; \*అమృతముతో నుద్భవమై యమరేశ్వర... హయరత్నము...\* ($\\text{య్} \+ \\text{అమరేశ్వర} \\longleftrightarrow \\text{హ}$) (\*Bhāratam\*, Ādi 2-26)\[cite: 7\].

  \* \*\*హా $\\longleftrightarrow$ అ:\*\* \*...మహా నీతియుతుండు తల్లికప్రియమెసఁగన్...\* ($\\text{తల్లికిన్} \+ \\text{అప్రియ}$) (\*Bhāratam\*, Ādi 2-6)\[cite: 7\]; \*...పాయసాహారము భక్తిఁబెట్టి మఱి యందఱకుం...\* ($\\text{య్} \+ \\text{అందఱకున్}$) (\*Bhāratam\*, Sabhā 1-15)\[cite: 7\].

  \* \*\*హై $\\longleftrightarrow$ అ:\*\* \*హైహయుండు సుమిత్రుఁడనురాజు...\* ($\\text{రాజు} \+ \\text{అను}$) (\*Bhāratam\*, Udyōga 3-151)\[cite: 7\]; \*...గవిసెనంత మూర్ఛదేఱి హైడింబుఁడొక్క...\* ($\\text{గవిసెన్} \+ \\text{అంత} \\longleftrightarrow \\text{హై}$) (\*Bhāratam\*, Udyōga 5-85)\[cite: 7\].

  \* \*\*హ $\\longleftrightarrow$ ఆ:\*\* \*హరిఁ జింతింపక మత్తుఁడై విషయ చింతాయత్తుఁడై...\* ($\\text{చింత} \+ \\text{ఆయత్తుఁడై}$) (\*Bhāgavatam\* 2-24)\[cite: 7\]; \*హరి పూరింపఁ దదాస్య మారుత సుగంధాకృష్టమై...\* ($\\text{సుగంధ} \+ \\text{ఆకృష్టమై}$) (\*Amuktamālyada\* 1-6)\[cite: 7\]; \*హరి హరాజ గజాననార్క షడాస్య...\* ($\\text{షట్} \+ \\text{ఆస్య}$) (\*Bhāratam\*, Ādi 1-21, Taralamu)\[cite: 7\]; \*...హనసముఁ వైనతేయునిఁ దదాస్యగత...\* ($\\text{తత్} \+ \\text{ఆస్య}$) (\*Bhāratam\*, Ādi 2-74)\[cite: 7\]; \*హరు మనమారఁ గొల్చుడరుదాతనిఁ...\* ($\\text{అరుదు} \+ \\text{ఆతనిన్}$) (\*Bhāratam\*, Śānti 12-219)\[cite: 7\]; \*హస్తములను గడిగి యాచమనక్రియా...\* ($\\text{య్} \+ \\text{ఆచమన}$) (\*Nalacaritra\* 2-146)\[cite: 7\].

  \* \*\*హా $\\longleftrightarrow$ ఆ:\*\* \*...మహాభుజుఁడై విహరించుచుండెనాసన...\* ($\\text{ఆసన} \\longleftrightarrow \\text{హా}$) (\*Bhāratam\*, Ādi 5-47)\[cite: 7\]; \*హారి విచిత్ర హేమ కవచావృతుఁడు...\* ($\\text{కవచ} \+ \\text{ఆవృతుఁడు}$) (\*Bhāratam\*, Ādi 6-17)\[cite: 7\]; \*హాటక పానపాత్రయునునారఁగఁ బండిన...\* ($\\text{యునున్} \+ \\text{ఆరఁగన్}$) (\*Amuktamālyada\* 2-57)\[cite: 7\].

  \* \*\*హ $\\longleftrightarrow$ ఐ:\*\* \*హరినెదిరించి నొంచి భువనైకవదాన్యు...\* ($\\text{భువన} \+ \\text{ఏక} \\rightarrow \\mathbf{ఐ}$ via \*Vr̥ddhi Yati\*) (\*Bhāskara Rāmāyaṇamu\*, Yuddha 4-18)\[cite: 7\]; \*హరిహయుఁడాగ్రహోజ్జ్వలితుఁడై...\* ($\\text{ఉజ్జ్వలితుఁడు} \+ \\text{ఐ}$) (\*Manu Caritra\* 5-14)\[cite: 7\].

  \* \*\*హ $\\longleftrightarrow$ ఔ:\*\* \*హరణము సేయుచున్ మదజలౌఘము...\* ($\\text{జల} \+ \\text{ఓఘము} \\rightarrow \\mathbf{ఔ}$ via \*Vr̥ddhi Yati\*) (\*Bhāratam\*, Āraṇya 6-106)\[cite: 7\]; \*హంసానీకము లేదుగాక బకభేకౌఘంబు...\* ($\\text{భేక} \+ \\text{ఓఘంబు} \\rightarrow \\mathbf{ఔ}$ via \*Vr̥ddhi Yati\*) (\*Bhāskara Rāmāyaṇamu\*, Sundara 203)\[cite: 7\].

  \* \*\*హి $\\longleftrightarrow$ ఇ:\*\* \*హితమతినాలకింపుచు జితేంద్రియుఁడై...\* ($\\text{జిత} \+ \\text{ఇంద్రియుఁడై}$) (\*Bhāskara Rāmāyaṇamu\*, Bāla 149)\[cite: 7\]; \*హిమధామార్ధజటాకిరీటుఁడభవుండింద్రేశ్వరుండు...\* ($\\text{అభవుండు} \+ \\text{ఇంద్రేశ్వరుండు}$) (\*Kāśīkhaṇḍam\* 3-104)\[cite: 7\]; \*హితులునునై రాజునెడలనిటు...\* ($\\text{నెడలన్} \+ \\text{ఇటు}$) (\*Śānti\* 4-272)\[cite: 7\].

  \* \*\*హీ $\\longleftrightarrow$ ఇ:\*\* \*హీనాగ్నిబలుండ నాకునిష్టాన్నము...\* ($\\text{నాకున్} \+ \\text{ఇష్టాన్నము}$) (\*Bhāratam\*, Ādi 8-236)\[cite: 7\]; \*...మీకుఁగానిప్పతి గత్తి వట్టునె హిహీ యిటు రండని...\* ($\\text{కాని} \+ \\text{ఇప్పతి} \\longleftrightarrow \\text{హీ}$) (\*Amuktamālyada\* 3-380)\[cite: 7\]; \*హీనుతముగఁ జేయుమిదియ యిష్టము నాకున్...\* ($\\text{య్} \+ \\text{ఇష్టము}$) (\*Bhāratam\*, Ādi 6-51)\[cite: 7\].

  \* \*\*హృ $\\longleftrightarrow$ ఇ:\*\* \*హృత్సరసీరుహంబు వరమిచ్చెదనిష్టముగోరు...\* ($\\text{వరమున్} \+ \\text{ఇచ్చెదన్}$) (\*Manu Caritra\* 2-42)\[cite: 7\]; \*హృదయములనొండొరులదెసనిట్టివార...\* ($\\text{దెసన్} \+ \\text{ఇట్టి}$) (\*Bhāratam\*, Āśramavāsa 1-17)\[cite: 7\]; \*హృదయమునం గలంక యొకయించుకయేనియు...\* ($\\text{యొక} \+ \\text{ఇంచుక}$) (\*Bhāratam\*, Sabhā 1-98)\[cite: 7\].

  \* \*\*హే $\\longleftrightarrow$ ఇ:\*\* \*హేమాభాంగవిభాధరారుణిమ వక్త్రేందుప్రభాశ్రీలఁదత్...\* ($\\text{వక్త్ర} \+ \\text{ఇందు}$) (\*Amuktamālyada\* 5-8)\[cite: 7\].

  \* \*\*హి $\\longleftrightarrow$ ఈ:\*\* \*హిమకరుఁదొట్టి పూరుభరతేశ కురుప్రభు...\* ($\\text{భరత} \+ \\text{ఈశ}$) (\*Bhāratam\*, Ādi 1-14)\[cite: 7\]; \*హిమవద్భూధరసార్వభౌమ వర విశ్వేశోపహారక్రియా...\* ($\\text{విశ్వ} \+ \\text{ఈశ}$) (\*Kāśīkhaṇḍam\* 3-457)\[cite: 7\]; \*హితమతి బహువచనముల హృదీశునిఁ బలుకన్...\* ($\\text{హృత్} \+ \\text{ఈశుని}$) (\*Bhāskara Rāmāyaṇamu\*, Sundara 167)\[cite: 7\].

  \* \*\*హీ $\\longleftrightarrow$ ఈ:\*\* \*...భూషణీకృతాహీనుఁడశేషలోక గురుఁడీశ్వరుఁడెప్పుడు...\* ($\\text{గురుఁడు} \+ \\text{ఈశ్వరుఁడు}$) (\*Bhāratam\*, Sabhā 1-78)\[cite: 7\]; \*...వీరులై యీ నవఖండమండిత... పతులు పయోహీనులై...\* ($\\text{లై} \+ \\text{ఈ} \\longleftrightarrow \\text{హీ}$) (\*Bhāratam\*, Ādi 8-5)\[cite: 7\].

  \* \*\*హి $\\longleftrightarrow$ ఎ:\*\* \*హితముఁ జేయుచుండిరెల్ల జనులు...\* ($\\text{చేయుచుండిరి} \+ \\text{ఎల్ల}$) (\*Bhāratam\*, Ādi 5-3)\[cite: 7\].

  \* \*\*హీ $\\longleftrightarrow$ ఎ:\*\* \*...నెక్కుడు మాటలాడెదవహీనపరాక్రముడర్జునుండు...\* ($\\text{న్} \+ \\text{ఎ} \\longleftrightarrow \\text{హీ}$) (\*Bhāratam\*, Virāṭa 1-253)\[cite: 7\].

  \* \*\*హృ $\\longleftrightarrow$ ఎ:\*\* \*హృద్దర్పోన్నతులు సూచి యెట్లు సహింతున్...\* ($\\text{య్} \+ \\text{ఎట్లు}$) (\*Bhāratam\*, Sabhā 2-141)\[cite: 7\].

  \* \*\*హె $\\longleftrightarrow$ ఎ:\*\* \*హెచ్చినమైత్రి పద్మినులకెల్ల...\* ($\\text{పద్మినులకున్} \+ \\text{ఎల్ల}$) (\*Amuktamālyada\* 4-148)\[cite: 7\].

  \* \*\*హే $\\longleftrightarrow$ ఎ:\*\* \*హేలమెయిన్మహీరమణుఁడెక్కెను...\* ($\\text{రమణుఁడు} \+ \\text{ఎక్కెను}$) (\*Manu Caritra\* 2-230)\[cite: 7\]; \*హేరాళముగఁ జల్లెనెలనాగ...\* ($\\text{న్} \+ \\text{ఎ}$) (\*Manu Caritra\* 5-115)\[cite: 7\]; \*హేలాగతినైనవిన్ననెలమి పఠింపన్...\* ($\\text{న్} \+ \\text{ఎ}$) (\*Bhāgavatam\* 8-250)\[cite: 7\].

  \* \*\*హి $\\longleftrightarrow$ ఏ:\*\* \*ధృతరాష్ట్ర కుమారులునవహితులై పాంచాలుమీఁదనేసిరి...\* ($\\text{మీఁదన్} \+ \\text{ఏసిరి}$) (\*Bhāratam\*, Ādi 6-73)\[cite: 7\]; \*హింసయు నీకు వేడ్కయగునేని...\* ($\\text{అగున్} \+ \\text{ఏని}$) (\*Kāśīkhaṇḍam\* 1-107)\[cite: 7\].

  \* \*\*హృ $\\longleftrightarrow$ ఏ:\*\* \*హృద్గతమైన మోహభరమేమని చెప్ప...\* ($\\text{భరము} \+ \\text{ఏమని}$) (\*Amuktamālyada\* 4-110)\[cite: 7\].

  \* \*\*హు $\\longleftrightarrow$ ఉ:\*\* \*...హుళ్యమెఱింగి వారికి యథోచిత గేహములీవొనర్పఁ...\* ($\\text{యథా} \+ \\text{ఉచిత}$) (\*Bhāskara Rāmāyaṇamu\*, Bāla 237)\[cite: 7\]; \*...బాహుబలంబొక్కఁడ నమ్మి పోఁదలఁచు నీ యుత్సాహమేనీతి...\* ($\\text{య్} \+ \\text{ఉత్సాహము}$) (\*Bhāskara Rāmāyaṇamu\*, Yuddha 902)\[cite: 7\]; \*...రాహుయుతనభంబుఁజొచ్చునల యుత్పలమిత్రుని...\* ($\\text{య్} \+ \\text{ఉత్పల}$) (\*Andhra Vālmīki\*, Araṇya 267)\[cite: 7\].

  \* \*\*హూ $\\longleftrightarrow$ ఉ:\*\* \*...పురుహూత పురస్సర మరుద్గణోత్తములధిక...\* ($\\text{గణ} \+ \\text{ఉత్తములు}$) (\*Bhāratam\*, Ādi 5-79)\[cite: 7\]; \*...తత్కితవాహూతుఁడనై జూదమాడకుండుట...\* ($\\text{కితవ} \+ \\text{ఆహూతుఁడు}$) (\*Bhāratam\*, Sabhā 2-60)\[cite: 7\].

  \* \*\*హెూ $\\longleftrightarrow$ ఉ:\*\* \*హెూమాజ్య గంధోర్మికుద్వేగమొందుచు...\* ($\\text{గంధోర్మికిన్} \+ \\text{ఉద్వేగము}$) (\*Kāśīkhaṇḍam\* 7-123)\[cite: 7\].

  \* \*\*హెూ $\\longleftrightarrow$ ఒ:\*\* \*...రక్కసుఁడగ్నిహోత్రగృహంబునకొయ్య వచ్చి...\* ($\\text{గృహంబునకున్} \+ \\text{ఒయ్య}$) (\*Bhāratam\*, Ādi 1-129)\[cite: 7\]; \*హోమకార్యమొప్పనొనరించి యప్పుడ...\* ($\\text{న్} \+ \\text{ఒప్పన్}$) (\*Bhāratam\*, Ādi 8-128)\[cite: 7\].

  \* \*\*హు $\\longleftrightarrow$ ఓ:\*\* \*...హువిలసనంబు ఘోరముగనోర్వఁగఁ జాలుట...\* ($\\text{ఘోరముగన్} \+ \\text{ఓర్వఁగన్}$) (\*Bhāratam\*, Sabhā 2-108)\[cite: 7\]; \*హుంకారంబొనరించి తుంబురునితోనోరీ దురాచార...\* ($\\text{తోన్} \+ \\text{ఓరీ}$) (\*Bhāratam\*, Sabhā 1-4)\[cite: 7\].

  \* \*\*హె $\\longleftrightarrow$ ఓ:\*\* \*...హెంబట్టుదట్టి పైనోలగింప...\* ($\\text{పైన్} \+ \\text{ఓలగింప}$) (\*Cāṭu\* 1-79)\[cite: 7\].

&nbsp;

\#\#\#\# The Closed Sarasayati Triad Architecture (6.18.2)

The engine integrates Sections 6.16, 6.17, and 6.18 into a single unified triadic equivalence cluster\[cite: 7\]:

1\. \*\*య $\\longleftrightarrow$ హ:\*\* \*R̥ju Yati\* (6.16)\[cite: 7\].

2\. \*\*అ $\\longleftrightarrow$ య:\*\* \*Sarasayati-2\* (6.17)\[cite: 7\].

3\. \*\*అ $\\longleftrightarrow$ హ:\*\* \*Sarasayati-3\* (6.18)\[cite: 7\].

&nbsp;

$$\\mathbf{Sarasayati\\ Triad:} \\quad \\{\\mathbf{అ,\\ య,\\ హ}\\} \\quad \\text{forms a closed, bidirectional alliteration matrix}$$\[cite: 7\]

\*(Subject always to internal Vowel-Class partition across all combinations)\*\[cite: 7\].

&nbsp;

\---

&nbsp;

\#\#\# 6.19 ఊష్మ యతులు (Ūṣma Yatulu — Sibilant Alliteration: Śa, Ṣa, Sa)

&nbsp;

\* \*\*Definition & Mechanics:\*\* The three sibilant fricatives (\*\*శ\*\* \[palatal\], \*\*ష\*\* \[retroflex\], and \*\*స\*\* \[dental\]) possess mutual Yati affinity\[cite: 7\].

\* \*\*Classification & Exclusion:\*\* Designated \*\*ఊష్మ విశ్రాంతులు\*\* (\*Ūṣma Viśrāntulu\*) by Appakavi\[cite: 7\]. While traditional phonetics catalogs four spirants (\*ūṣmamulu\*: \*\*శ, ష, స, హ\*\*), the aspirate \*\*'హ'\*\* is excluded from Ūṣma Yati because its alliterative properties are handled under \*R̥ju Yati\* and \*Sarasayati\*\[cite: 7\].

\* \*\*Combinatorial Sibilant Pairs:\*\*

  $$\\{\\mathbf{శ \- ష,\\ శ \- స,\\ ష \- స}\\}$$\[cite: 7\]

\* \*\*Vowel Governance:\*\* Strict alignment within Class 1, Class 2, or Class 3 vowel groups is required\[cite: 7\]:

  \* \*Class 1:\* \*\*శ, శా, శై, శౌ $\\longleftrightarrow$ ష, షా, షై, షౌ $\\longleftrightarrow$ స, సా, సై, సౌ\*\*\[cite: 7\].

  \* \*Class 2:\* \*\*శి, శీ, శృ, శె, శే $\\longleftrightarrow$ షి, షీ, షె, షే $\\longleftrightarrow$ సి, సీ, సృ, సె, సే\*\*\[cite: 7\].

  \* \*Class 3:\* \*\*శు, శూ, శొ, శో $\\longleftrightarrow$ షు, షూ, షొ, షో $\\longleftrightarrow$ సు, సూ, సొ, సో\*\*\[cite: 7\].

&nbsp;

\#\#\#\# Canonical Provenance for Ūṣma Yatulu (6.19.2)

\* \*\*Appakavi's Dual Demonstrative Stanza (3-104):\*\*

  \* Line 1: \*శతమఖోపల... అనుషంగ\* (\*\*శ $\\longleftrightarrow$ ష\*\*)\[cite: 7\].

  \* Line 2: \*షడ్జయుత... ప్రసంగ\* (\*\*ష $\\longleftrightarrow$ స\*\*)\[cite: 7\].

\* \*\*Śa \- Ṣa Pairings (శ $\\longleftrightarrow$ ష):\*\*

  \* \*\*శ $\\longleftrightarrow$ ష:\*\* \*శరణార్థి రాజన్యషడ్వర్గ...\* (\*Raṅganātha Rāmāyaṇamu\*, Bāla 3)\[cite: 7\]; \*...షభ్రూయుగ్మ... శుభ్రఖ్యాతివి...\* (\*Bhāgavatam\* 7-206)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ ష:\*\* \*శాత్రవునిచేత లేని దోషంబులెవ్వి...\* (\*Bhāratam\*, Sabhā 5-826)\[cite: 7\].

  \* \*\*శీ $\\longleftrightarrow$ షే:\*\* \*శీఘ్రవేగునల సుషేణుఁగాంచి...\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 1030)\[cite: 7\].

\* \*\*Śa \- Sa Pairings (శ $\\longleftrightarrow$ స):\*\*

  \* \*\*శ $\\longleftrightarrow$ స:\*\* \*...వంశమునఁ బ్రసిద్ధులై విమల సద్గుణశోభితులైన...\* (\*Bhāratam\*, Ādi 1-14)\[cite: 7\]; \*సభల విస్తరిల్లి శల్యాదికములైన...\* (\*Bhāratam\*, Ādi 1-52)\[cite: 7\]; \*సముచితంబుగ మృదుశయన... శయనించునిత్తన్వి సమదలాంగి...\* (\*Bhāratam\*, Āraṇya 3-300)\[cite: 7\]; \*...శంబునఁ గట్టికొని సన్మునినాథుఁడు...\* (\*Bhāratam\*, Ādi 7-120)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ సా:\*\* \*శరణ్యులుత్తములు నిత్యసాంగత్యమునన్...\* (\*Bhāratam\*, Sabhā 2-112)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ సౌ:\*\* \*...ద్విజేశతతులు దెల్ప వీటిమణిసౌధములాజిర...\* (\*Śivarātri Māhātmyamu\* 1-101)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ స:\*\* \*శాత్రవజైత్రతేజమున సర్వదిశల్...\* (\*Bhāratam\*, Ādi 5-94)\[cite: 7\]; \*శాపంబునఁబదియు రెండు సంవత్సరముల్...\* (\*Bhāratam\*, Ādi 7-127)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ సా:\*\* \*శారద నీరదేందు ఘనసార పటీర...\* (\*Bhāgavatam\*, Avatārika)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ సై:\*\* \*...దక్షిణాశాముఖవీథినేఁగె మఖసైంధవము...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 59)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ సౌ:\*\* \*శాత్రవశిబిరంబు సౌప్తికవేళఁ...\* (\*Bhāratam\*, Sauptika 1-229)\[cite: 7\]; \*శాంతునకపవర్గ సౌఖ్యసంవేదికి...\* (\*Bhāgavatam\* 8-79)\[cite: 7\].

  \* \*\*శౌ $\\longleftrightarrow$ సా:\*\* \*శౌరి పలికె సవ్యసాచిఁజూచి...\* (\*Jaimini Bhāratamu\* 7-153)\[cite: 7\].

  \* \*\*శౌ $\\longleftrightarrow$ సై:\*\* \*శౌరి పార్థ పార్థ సైంధవుతల యిల...\* (\*Bhāratam\*, Drōṇa 4-321)\[cite: 7\].

  \* \*\*సై $\\longleftrightarrow$ శౌ:\*\* \*సైరణఁగాని తీఱవని శౌర్యముదక్కి...\* (\*Daśakumāra Caritra\* 4-78)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ శి:\*\* \*...ప్రసిద్ధుఁడు మధ్యముఁడ యను విశిష్టస్తవముల్...\* (\*Bhāratam\*, Ādi 6-95)\[cite: 7\].

  \* \*\*శి $\\longleftrightarrow$ సే:\*\* \*శివకరుండు హితోపదేశము సేయగాఁగడు...\* (\*Bhāratam\*, Ādi 8-90, Taralamu)\[cite: 7\].

  \* \*\*సృ $\\longleftrightarrow$ శి:\*\* \*సృజియించి దానికి శింజినీ ప్రముఖంబు...\* (\*Bhāratam\*, Sabhā 2-121)\[cite: 7\].

  \* \*\*శూ $\\longleftrightarrow$ సు:\*\* \*శూరులు ధృతరాష్ట్రసుతులు దుర్యోధనాదులు...\* (\*Bhāratam\*, Ādi 1-269)\[cite: 7\].

  \* \*\*శూ $\\longleftrightarrow$ సూ:\*\* \*శూరాగ్రేసరుఁడైన యా లవునకున్ సూర్యుండు...\* (\*Bhāratam\*, Virāṭa 6-161)\[cite: 7\].

  \* \*\*సూ $\\longleftrightarrow$ శో:\*\* \*సూనుల శరసజ్యచాప శోభితకరులన్...\* (\*Bhāratam\*, Ādi 5-257)\[cite: 7\].

  \* \*\*సో $\\longleftrightarrow$ శు:\*\* \*సోమరసాస్వాదలోల శుంభనిశుంభ...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 7-271)\[cite: 7\].

\* \*\*Ṣa \- Sa Pairings (ష $\\longleftrightarrow$ స):\*\*

  \* \*\*ష $\\longleftrightarrow$ స:\*\* \*...భూషణు వీడ్కొని వేడ్కనవని సంచారమునన్...\* (\*Bhāratam\*, Sabhā 2-41)\[cite: 7\]; \*...సకథల్ శారికలీరికల్ గొను మనీషన్ శేషభాషావిశేష...\* (\*Vasu Caritra\* 1-8)\[cite: 7\]; \*...షణవృత్తిన్ విహరించు దైత్యునొరులే సంధించు...\* (\*Kāśīkhaṇḍam\* 3-222)\[cite: 7\].

  \* \*\*స $\\longleftrightarrow$ షా:\*\* \*సరసత్వంబునఁగేలనూని యల యోషామౌళి...\* (\*Śivarātri Māhātmyamu\* 2-99)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ షి:\*\* \*సిచయాభావనటన్నితంబతట యోషిద్రత్న...\* (\*Manu Caritra\* 3-97)\[cite: 7\].

  \* \*\*షీ $\\longleftrightarrow$ సీ:\*\* \*...భూషితపాదాంబుజు... కుశాసీనున్...\* (\*Jaimini Bhāratamu\* 7-204)\[cite: 7\].

  \* \*\*సీ $\\longleftrightarrow$ షే:\*\* \*సీతయు నీవు తేప యభిషేకము...\* (\*Amuktamālyada\* 5-139)\[cite: 7\].

  \* \*\*సూ $\\longleftrightarrow$ షు:\*\* \*సూర్యకరసహస్రములో సుషుమ్నయనఁగ...\* (\*Bhāgavatam\* 7-102)\[cite: 7\].

&nbsp;

\---

&nbsp;

\#\#\# 6.20 సరసయతి-4: స\-వర్గ మరియు చ-వర్గ యతులు (Sibilants to Palatal Stops)

&nbsp;

\* \*\*Definition & Mechanics:\*\* Sibilants (\*\*శ, ష, స\*\*) possess comprehensive Yati affinity with the Palatal stop series (\*\*చ, ౘ, ఛ, జ, ౙ, ఝ\*\*)\[cite: 7\].

\* \*\*Affricate Ingestion (Dantya/Tālavya 6.20.1):\*\* By grammatical rule (\*Bāla Vyākaraṇam\*, Samjñā 7), native Telugu dental affricates (\*\*ౘ, ౙ\*\*) and classical palatal stops (\*\*చ, జ\*\*) are homogeneous (\*savarṇas\*)\[cite: 7\]. Therefore, the palatal side of this bridge encompasses all 6 active consonants\[cite: 7\].

\* \*\*Combinatorial Matrix (18 Structural Pairings):\*\*

  $$\\begin{aligned}

  \\mathbf{Pairings\\ with\\ ‘శ’:} &\\quad \\{\\text{శ-చ,\\ శ\-ౘ,\\ శ\-ఛ,\\ శ\-జ,\\ శ\-ౙ,\\ శ\-ఝ}\\} \\\\

  \\mathbf{Pairings\\ with\\ ‘ష’:} &\\quad \\{\\text{ష-చ,\\ ష\-ౘ,\\ ష\-ఛ,\\ ష\-జ,\\ ష\-ౙ,\\ ష\-ఝ}\\} \\\\

  \\mathbf{Pairings\\ with\\ ‘స’:} &\\quad \\{\\text{స-చ,\\ స\-ౘ,\\ స\-ఛ,\\ స\-జ,\\ స\-ౙ,\\ స\-ఝ}\\}

  \\end{aligned}$$\[cite: 7\]

\* \*\*Dental Affricate Vowel Restriction:\*\* Because dental \*\*ౘ\*\* and \*\*ౙ\*\* only combine with vowels \*అ, ఆ, ఉ, ఊ, ఒ, ఓ, ఐ, ఔ\* (and never with \*ఇ, ఈ, ఎ, ఏ, ఋ\*), matches involving them are restricted to compatible vowel environments\[cite: 7\].

&nbsp;

\#\#\#\# Canonical Provenance for Sarasayati-4 (6.20.2)

\* \*\*Multi-License Classical Stanzas:\*\*

  \* \*Bhāratam\* (Ādi 5-150): Lines 1 & 2 use \*\*సు $\\longleftrightarrow$ జూ\*\*; Line 4 uses \*\*చి $\\longleftrightarrow$ సి\*\*\[cite: 7\].

  \* \*Bhāratam\* (Ādi 8-232): Line 1 uses \*\*జ $\\longleftrightarrow$ సా\*\*; Line 2 uses \*\*జే $\\longleftrightarrow$ స\*\*\[cite: 7\].

  \* \*Manu Caritra\* (6-104) / \*Amuktamālyada\* (4-16, Kavirājavirājitam): Line 1 uses \*\*జ $\\longleftrightarrow$ శా\*\*; Line 2 uses \*\*జ $\\longleftrightarrow$ సా\*\*; Line 4 uses \*\*జ $\\longleftrightarrow$ శౌ\*\*\[cite: 7\].

  \* \*Manu Caritra\* (3-57): Line 2 uses \*\*జె $\\longleftrightarrow$ సీ\*\*; Line 3 uses \*\*సి $\\longleftrightarrow$ చి\*\*; Line 4 uses \*\*జె $\\longleftrightarrow$ శే\*\*\[cite: 7\].

  \* \*Bhāskara Śatakam\*: Lines 1 & 2 use \*\*చే $\\longleftrightarrow$ స\*\*\[cite: 7\].

\* \*\*Śa with Palatals (శ $\\longleftrightarrow$ చ/ఛ/జ/ఝ):\*\*

  \* \*\*చ $\\longleftrightarrow$ శ:\*\* \*చండపరాక్రమార్జిత యశఃపరిపూర్ణుఁడు...\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1647)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ చా:\*\* \*శమితారాతిబలుండు... పాంచాలప్రభుండు...\* (\*Bhāratam\*, Ādi 8-44)\[cite: 7\].

  \* \*\*చా $\\longleftrightarrow$ శా:\*\* \*...సంచారిత... విశాల శిలోచ్చయ...\* (\*Bhāratam\*, Ādi 6-78)\[cite: 7\].

  \* \*\*చై $\\longleftrightarrow$ శా:\*\* \*చైతన్యములుడుగుఁడనుచు శాపమునిచ్చెన్...\* (\*Haravilāsam\* 2-97)\[cite: 7\].

  \* \*\*శి $\\longleftrightarrow$ చే:\*\* \*శిఖసమక్షమునందు నాచే గ్రహింప...\* (\*Manu Caritra\* 5-369)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ శే:\*\* \*చేడియ రోషభీషణవిశేష...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 335)\[cite: 7\].

  \* \*\*శృ $\\longleftrightarrow$ చి:\*\* \*శృంగార కుసుమంబు చిన్నిచుక్కల రాజు...\* (\*Siṁhāsana Dvātriṁśika\* 1-5)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ చే:\*\* \*శక్తి రాక్షసనిహతుఁడై చేనిన శోక...\* (\*Bhāratam\*, Ādi 7-150)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ చౌ:\*\* \*శత్రుండట వాని బ్రదుకు చౌకౌఁగాదే...\* (\*Kāśīkhaṇḍam\* 3-194)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ శా:\*\* \*చేని విభుఁగాంచి పల్కు బలశాసన...\* (\*Manu Caritra\* 2-28)\[cite: 7\].

  \* \*\*చా $\\longleftrightarrow$ శై:\*\* \*చాలదె కాల్పంగనుగ్ర శైలాటవులన్...\* (\*Bhāratam\*, Ādi 6-117)\[cite: 7\].

  \* \*\*చూ $\\longleftrightarrow$ శు:\*\* \*చూతమె డాసి పక్వతర శుక్తిపుటాంతర...\* (\*Manu Caritra\* 3-80)\[cite: 7\].

  \* \*\*శూ $\\longleftrightarrow$ చూ:\*\* \*శూలికైనఁదమ్మి చూలికైన...\* (\*Bhāgavatam\* 1-17)\[cite: 7\].

  \* \*\*చో $\\longleftrightarrow$ శో:\*\* \*చోద్యంబయ్యెడునింతకాలమరిగెన్ శోధించి...\* (\*Bhāgavatam\* 7-163)\[cite: 7\].

  \* \*\*శో $\\longleftrightarrow$ ఛో:\*\* \*...శోభితభూతి రింఛోళి గాఁగ...\* (\*Amuktamālyada\* 2-5)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ జ:\*\* \*శరణ్యుఁడగు ధర్మజన్ము జన్మదినమునన్...\* (\*Bhāratam\*, Ādi 5-95)\[cite: 7\].

  \* \*\*శా $\\longleftrightarrow$ జ:\*\* \*శాపమిచ్చునాఁడు జననియుత్సంగంబు...\* (\*Bhāratam\*, Ādi 2-133)\[cite: 7\].

  \* \*\*జా $\\longleftrightarrow$ శ:\*\* \*...జాతప్రోద్ధత బాడబానలశిఖాశంకాధికాతంకమై...\* (\*Bhāratam\*, Ādi 1-111)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ శై:\*\* \*...పుంజంబులవోలె వెల్వడియె శైలవిశాల...\* (\*Bhāratam\*, Ādi 6-176)\[cite: 7\].

  \* \*\*జా $\\longleftrightarrow$ శౌ:\*\* \*...రాజన్య భయంకరుండు రణశౌర్యుఁడు...\* (\*Bhāratam\*, Ādi 8-224)\[cite: 7\].

  \* \*\*జా $\\longleftrightarrow$ శై:\*\* \*జాతసుఖప్రీతిఁ దగలి శైలాటవులన్...\* (\*Bhāratam\*, Ādi 7-89)\[cite: 7\].

  \* \*\*శి $\\longleftrightarrow$ జి:\*\* \*...శిబికాసహస్రంబుఁ జిత్రలలిత...\* (\*Bhāratam\*, Ādi 8-221)\[cite: 7\].

  \* \*\*శీ $\\longleftrightarrow$ జీ:\*\* \*శీతాహార్యసుతాళినీ వికచరాజీవంబు...\* (\*Śivarātri Māhātmyamu\* 1-99)\[cite: 7\].

  \* \*\*శీ $\\longleftrightarrow$ జె:\*\* \*శీలంబుంగులమున్ శమంబు దమముం జెల్వంపు...\* (\*Manu Caritra\* 1-55)\[cite: 7\].

  \* \*\*శీ $\\longleftrightarrow$ జే:\*\* \*...నిన్నుఁ బ్రీతిఁ జేకొని...\* (\*Bhāratam\*, Ādi 3-106)\[cite: 7\].

  \* \*\*జె $\\longleftrightarrow$ శృ:\*\* \*...సరోలక్ష్మికిఁ జెలువుగ నీరాడి సహజశృంగారముగన్...\* (\*Kavikarṇarasāyanamu\* 2-135)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ శృ:\*\* \*...జేలచెఱంగు దూలఁగ విశృంఖల వృత్తిఁ...\* (\*Nalacaritra\* 2-144)\[cite: 7\].

  \* \*\*జో $\\longleftrightarrow$ శు:\*\* \*...తేజోజయశాలి శౌర్యుఁడు విశుద్ధ...\* (\*Bhāratam\*, Ādi 1-3)\[cite: 7\].

  \* \*\*శూ $\\longleftrightarrow$ జు:\*\* \*శూరుఁడు రాధేయుఁడింద్రజునకిట్లనియెన్...\* (\*Bhāratam\*, Ādi 7-199)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ జే:\*\* \*శయపూజాంబుజముల్ ఘటిం దడబడం జేన్గోయి...\* (\*Amuktamālyada\* 1-56)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ జా:\*\* \*...శశిరేఖనమృతంబు జాలువాఱ...\* (\*Bhāratam\*, Virāṭa 1-12)\[cite: 7\].

  \* \*\*జా $\\longleftrightarrow$ శా:\*\* \*జాలువా పైఠాణి శాలువుఁ దొలగించి...\* (\*Śivarātri Māhātmyamu\* 1-91)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ శై:\*\* \*...జేరుగునంజనమహాశైలమనఁగ...\* (\*Manu Caritra\* 6-88)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ శౌ:\*\* \*...జెనునె నీకు లేని శౌర్యసంపదఁజెప్పి...\* (\*Bhāratam\*, Ādi 1-308)\[cite: 7\].

  \* \*\*జూ $\\longleftrightarrow$ శు:\*\* \*...జూడ రానియట్టి శుభచరిత్ర...\* (\*Bhāratam\*, Āraṇya 2-91)\[cite: 7\].

  \* \*\*జూ $\\longleftrightarrow$ శో:\*\* \*...జూచిన భక్తి మ్రొక్కుటయె శోభనమీతఁడు...\* (\*Rāghavapāṇḍavīyamu\* 2-12)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ ఝ:\*\* \*శరనిధికా శరధిలోని ఝషకములెక్కన్...\* (\*Bhāratam\*, Udyōga 6-105)\[cite: 7\].

  \* \*\*ఝ $\\longleftrightarrow$ శ:\*\* \*...ఝరవారి శోణితశంకఁ ద్రావ...\* (\*Kāśīkhaṇḍam\* 3-11)\[cite: 7\].

  \* \*\*శ $\\longleftrightarrow$ ఝా:\*\* \*...శర్కరాభీల ఝంఝమరుత్తు...\* (\*Bhāratam\*, Virāṭa 7-44)\[cite: 7\].

  \* \*\*ఝ $\\longleftrightarrow$ శై:\*\* \*ఝంకారాళికులంబులుం గల మహాశైలస్థలుల్...\* (\*Kāśīkhaṇḍam\* 2-78)\[cite: 7\].

\* \*\*Ṣa with Palatals (ష $\\longleftrightarrow$ చ/ఛ/జ/ఝ):\*\*

  \* \*\*చ $\\longleftrightarrow$ షా:\*\* \*చతురుపాయజ్ఞుండు షాడ్గుణ్యశాలి...\* (\*Raṅganātha Rāmāyaṇamu\*, Bāla 9, Dvipada)\[cite: 7\].

  \* \*\*ష $\\longleftrightarrow$ చె:\*\* \*...శోషిత పాథోథిపయస్కుఁడైన ముని దోఁచెం...\* (\*Bhāratam\*, Udyōga 4-145)\[cite: 7\].

  \* \*\*చి $\\longleftrightarrow$ షే:\*\* \*...జనించిన పెనుకిన్క మాని యభిషేక విచారము...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 519)\[cite: 7\].

  \* \*\*చ $\\longleftrightarrow$ ష:\*\* \*...రాచయంచలగమి మానసంబు కలుషంబయి...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Kiṣkindha 183)\[cite: 7\].

  \* \*\*షా $\\longleftrightarrow$ చే:\*\* \*...భవదీయ శుశ్రూషామహమహితుండదేల చేనఁగానలకున్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 321)\[cite: 7\].

  \* \*\*చొ $\\longleftrightarrow$ షు:\*\* \*చొచ్చి పితామహుంగని యిషుప్రచయంబునఁగప్పె...\* (\*Bhāratam\*, Bhīṣma 2-277)\[cite: 7\].

  \* \*\*ఛ $\\longleftrightarrow$ ష:\*\* \*ఛత్రాయమాణ శేషఫణామణిప్రభల్...\* (\*Amuktamālyada\* 4-118)\[cite: 7\].

  \* \*\*ఛ $\\longleftrightarrow$ షా:\*\* \*...బాష్పసంఛన్న ముఖాబ్జుఁడై ఘనవిషాదముఁబొందుచు...\* (\*Bhāratam\*, Virāṭa 6-32)\[cite: 7\].

  \* \*\*ఛే $\\longleftrightarrow$ షి:\*\* \*ఛేద్యమితరంబు సమభిలషితము కాదె...\* (\*Śānti\* 1-205)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ ష:\*\* \*జలము చంద్రుండు గాఁడె యోషధులఁ బ్రోచు...\* (\*Bhāratam\*, Anuśāsanika 2-405)\[cite: 7\].

  \* \*\*ష $\\longleftrightarrow$ జ:\*\* \*...విషశ్రేణులనొసంగు జలధరంబు...\* (\*Haravilāsam\* 5-95)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ షా:\*\* \*జలజసంభవుబోఁటి భాషావధూటి...\* (\*Śivarātri Māhātmyamu\* 1-5)\[cite: 7\].

  \* \*\*జీ $\\longleftrightarrow$ షే:\*\* \*జీవనమెల్ల సత్కవినిషేవితమాశయమెల్ల...\* (\*Manu Caritra\* 2-105)\[cite: 7\].

  \* \*\*జె $\\longleftrightarrow$ షి:\*\* \*...బడసియతనిఁ జెలఁగి సామ్రాజ్యమందభిషిక్తుఁజేసి...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 826)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ షా:\*\* \*జేరపిరి నియతినాషాఢమాసంబున...\* (\*Bhāgavatam\* 5-131)\[cite: 7\].

  \* \*\*జౌ $\\longleftrightarrow$ ష:\*\* \*...నన్నుఁగానఁగాఁజోలవు నీవు కామముఖషట్కము...\* (\*Bhāratam\*, Ādi 1-124)\[cite: 7\].

\* \*\*Sa with Palatals (స $\\longleftrightarrow$ చ/ఛ/జ/ఝ):\*\*

  \* \*\*స $\\longleftrightarrow$ చా:\*\* \*సమధనవంతులకు సమసుచారిత్రులకున్...\* (\*Bhāratam\*, Ādi 5-205)\[cite: 7\].

  \* \*\*చ $\\longleftrightarrow$ సై:\*\* \*...సంచలచ్చటుల సైనిక మత్స్యములన్...\* (\*Bhāratam\*, Sabhā 2-33)\[cite: 7\].

  \* \*\*చ $\\longleftrightarrow$ సౌ:\*\* \*...సాధుసంచయముఖచాతకంబులకు సౌఖ్యమొసంగ...\* (\*Kāśīkhaṇḍam\* 4-8)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ చి:\*\* \*సిగ్గేటికిఁబొడమెనమ్మ చిత్తరుబొమ్మా...\* (\*Manu Caritra\* 3-93)\[cite: 7\].

  \* \*\*చీ $\\longleftrightarrow$ సి:\*\* \*చీటికి ప్రాణంబు వ్రాలు సిద్ధము సుమతీ...\* (\*Sumati Śatakam\*)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ చె:\*\* \*...సిందూరతిలకంబు చెమ్మగిల్ల...\* (\*Manu Caritra\* 1-5)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ చే:\*\* \*...సినజనుఁడల్పుఁడని నమ్మి చేకొని యుండన్...\* (\*Bhāratam\*, Ādi 6-116)\[cite: 7\].

  \* \*\*సృ $\\longleftrightarrow$ చే:\*\* \*సృష్టినింతకుమున్ను నాచేతసృష్టుఁడయ్యె...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 391)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ సే:\*\* \*చేయుమనుగ్రహమవజ్ఞ సేయందగునే...\* (\*Bhāratam\*, Ādi 4-81)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ సా:\*\* \*...చని యొక్క ముదుసలిసానికపుడు...\* (\*Bhāratam\*, Ādi 7-223)\[cite: 7\].

  \* \*\*స $\\longleftrightarrow$ చా:\*\* \*సదమల శరదిందు శంఖనిభమైన చేయయుఁ గలుఁగు...\* (\*Bhāratam\*, Ādi 7-99, Madhyākkara)\[cite: 7\].

  \* \*\*చో $\\longleftrightarrow$ సా:\*\* \*చోఁప కట్టువడియె సామజములు...\* (\*Bhāratam\*, Virāṭa 2-165)\[cite: 7\].

  \* \*\*సై $\\longleftrightarrow$ చా:\*\* \*సైపకుండిననింతియ చాలుఁగాని...\* (\*Bhāratam\*, Sabhā 2-113)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ సౌ:\*\* \*చేనవుగనొద్దనున్నయెడ సౌహృదముంచుట...\* (\*Nalacaritra\* 2-618)\[cite: 7\].

  \* \*\*చే $\\longleftrightarrow$ స / సు $\\longleftrightarrow$ చు:\*\* \*చేని కైలాసముఁజొచ్చి శంకరు నివాస... సున దౌవారికులడ్డవెట్టఁ దలమంచుంజొచ్చి...\* (\*Bhāgavatam\* 8-219)\[cite: 7\].

  \* \*\*చూ $\\longleftrightarrow$ సు:\*\* \*చూచితినిపుడు భూసురవంశపోషకు...\* (\*Bhāratam\*, Sabhā 1-204)\[cite: 7\].

  \* \*\*సు $\\longleftrightarrow$ చూ:\*\* \*సురుచిరంబుగ భార్యయ చూవె యెందు...\* (\*Bhāratam\*, Ādi 2-74)\[cite: 7\].

  \* \*\*చూ $\\longleftrightarrow$ సూ:\*\* \*చూచి ఝళంఝళత్కటక సూచిత వేగ...\* (\*Manu Caritra\* 2-29)\[cite: 7\].

  \* \*\*సొ $\\longleftrightarrow$ చు:\*\* \*...సొంపార ముద్దాడు చుంచు దువ్వు...\* (\*Bhāratam\*, Sabhā 1-114)\[cite: 7\].

  \* \*\*చో $\\longleftrightarrow$ సొ:\*\* \*చొప్పడకున్నట్టి యూరు సొరకుము సుమతీ...\* (\*Sumati Śatakam\*)\[cite: 7\].

  \* \*\*చొ $\\longleftrightarrow$ సో:\*\* \*చొక్కపుఁబ్రాయమున్ మిగుల సోయగమున్...\* (\*Manu Caritra\* 3-7)\[cite: 7\].

  \* \*\*సు $\\longleftrightarrow$ చో:\*\* \*సుఖము దుఃఖము ప్రాప్తించు చోట నరుఁడు...\* (\*Bhāratam\*, Ādi 4-267)\[cite: 7\].

  \* \*\*ఛ $\\longleftrightarrow$ స:\*\* \*ఛందములు ధాతువులు ధర్మసమితి హృదయ...\* (\*Bhāgavatam\* 8-224)\[cite: 7\].

  \* \*\*ఛ $\\longleftrightarrow$ సా:\*\* \*...వాంఛనెనయు చంద్రుఁడౌఁజుము రసావలయాతప...\* (\*Śivarātri Māhātmyamu\* 5-87)\[cite: 7\].

  \* \*\*ఛి $\\longleftrightarrow$ సి:\*\* \*ఛిన్నసుజనార్తి శ్రీనరసింహమూర్తి...\* (\*Bhāgavatam\* 3-26)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ స:\*\* \*జలధి విలోలవీచి విలసత్కలకాంచి సమంచితావనీ...\* (\*Bhāratam\*, Ādi 3-144)\[cite: 7\].

  \* \*\*స $\\longleftrightarrow$ జ:\*\* \*...రాగరసమ్మునఁదన్నెఱుగకుండెఁ జంచలతనుఁడై...\* (\*Bhāratam\*, Ādi 5-186)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ సా:\*\* \*జననమరణాదులైన సంసార దురిత...\* (\*Bhāratam\*, Virāṭa 1-23)\[cite: 7\].

  \* \*\*సా $\\longleftrightarrow$ జా:\*\* \*...సంసార వికార సంతమసజాలవిజృంభము...\* (\*Bhāratam\*, Ādi 1-22)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ సై:\*\* \*జయమొనరింతుగాక యని సైఁతునె దర్పము...\* (\*Bhāratam\*, Virāṭa 4-148)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ సౌ:\*\* \*జనవినుతచరిత్రపాత్ర సౌజన్యనిధీ...\* (\*Bhāratam\*, Ādi 6-310)\[cite: 7\].

  \* \*\*జె $\\longleftrightarrow$ సి:\*\* \*...చేసినం జెడునిహముం బరంబునిది సిద్ధము...\* (\*Bhāratam\*, Ādi 1-138)\[cite: 7\].

  \* \*\*సి $\\longleftrightarrow$ జే:\*\* \*సిద్ధికరుఁడగు గురుఁడగుఁ జేయుఁ బ్రీతి...\* (\*Bhāratam\*, Ādi 2-61)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ సి:\*\* \*జే జే యంచు భజింతునిష్టఫలసంసిద్ధుల్...\* (\*Kāśīkhaṇḍam\* 1-4)\[cite: 7\].

  \* \*\*జి $\\longleftrightarrow$ సృ:\*\* \*జితశత్రుని దివిరథాఖ్యు సృజియించెనతండు...\* (\*Bhāratam\*, Sabhā 3-76)\[cite: 7\].

  \* \*\*సె $\\longleftrightarrow$ జి:\*\* \*సెలవుల ఫేనముట్టిపడ జిట్టలతోడనె...\* (\*Manu Caritra\* 4-18)\[cite: 7\].

  \* \*\*సె $\\longleftrightarrow$ జే:\*\* \*...కడుసెరగైనెడనెఱిఁగి యెడముఁజేయుదురె...\* (\*Bhāratam\*, Ādi 8-119)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ సే:\*\* \*...నిన్నుంజేకొని మాయన్న యెగ్గు సేయక...\* (\*Bhāratam\*, Ādi 6-194)\[cite: 7\].

  \* \*\*సే $\\longleftrightarrow$ జృ:\*\* \*సేనలు రెండునుద్భట విజృంభణతన్...\* (\*Bhāratam\*, Virāṭa 3-193)\[cite: 7\].

  \* \*\*జో $\\longleftrightarrow$ సు:\*\* \*...తేజోనిధి భాగ్యోన్నతుండు సుతుఁడుదయించెన్...\* (\*Amuktamālyada\* 4-60)\[cite: 7\].

  \* \*\*సూ $\\longleftrightarrow$ జో:\*\* \*సూనున్ గర్భమునన్ ధరించి సుతతేజోరాజసంబెట్టిదో...\* (\*Amuktamālyada\* 4-58)\[cite: 7\].

  \* \*\*జే $\\longleftrightarrow$ స:\*\* \*వనకేళీ కౌతుకమునఁ జేనియెను శర్మిష్ఠఁ...\* (\*Bhāratam\*, Ādi 3-154)\[cite: 7\]; \*జీవ్వనమెదిరించె జిగి యెసఁగనా మేనన్...\* (\*Manu Caritra\* 6-42)\[cite: 7\].

  \* \*\*సా $\\longleftrightarrow$ జే:\*\* \*...సారెకు గుండియ జైల్లనంగ...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 83)\[cite: 7\].

  \* \*\*స $\\longleftrightarrow$ జా:\*\* \*సకలబలంబులను గెలువఁజాలుదురుగ్రా...\* (\*Bhāratam\*, Virāṭa 2-24)\[cite: 7\].

  \* \*\*జూ $\\longleftrightarrow$ సు:\*\* \*...పోయిననార్చెం జూచి భవద్బలముఁ బాండుసుత...\* (\*Bhāratam\*, Virāṭa 2-51)\[cite: 7\]; \*జూదమునందుఁజిక్కి విరసుల్నను నవ్వఁగ...\* (\*Bhāratam\*, Sabhā 2-10-92)\[cite: 7\].

  \* \*\*సూ $\\longleftrightarrow$ జో:\*\* \*...దీప్తిసూచి సద్గణములు గడుఁజోద్యమంది...\* (\*Bhāratam\*, Ādi 3-212)\[cite: 7\].

  \* \*\*జ $\\longleftrightarrow$ సొ:\*\* \*...రాజు విలోకించి చలించి కైకొనిన యా సొమ్మెల్ల...\* (\*Manu Caritra\* 5-82)\[cite: 7\].

  \* \*\*సొ $\\longleftrightarrow$ జూ:\*\* \*సొలయక యెల్లదేశములుఁ జూచితినందుఁ...\* (\*Bhāratam\*, Ādi 7-3)\[cite: 7\].

  \* \*\*జో $\\longleftrightarrow$ సొ:\*\* \*...జోతిల మేన బాణములు సాన్పి...\* (\*Bhāratam\*, Virāṭa 4-192)\[cite: 7\].

  \* \*\*సొ $\\longleftrightarrow$ జో:\*\* \*సొలయుచున్నవి కంటివే జోడువాసి...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 689)\[cite: 7\].

  \* \*\*ఝ $\\longleftrightarrow$ స:\*\* \*...సుధా ఝరముల మున్కలాడు... సత్కవినై...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 18)\[cite: 7\].

  \* \*\*స $\\longleftrightarrow$ ఝా:\*\* \*సప్తమాడియరాజ ఝాడియక్ష్మాపాల...\* (\*Śivarātri Māhātmyamu\* 1-29)\[cite: 7\].

  \* \*\*ఝ $\\longleftrightarrow$ సై:\*\* \*ఝంకరణంబు సల్పు మరుసైన్యములట్ల...\* (\*Bhāratam\*, Udyōga 6-23)\[cite: 7\].

  \* \*\*సు $\\longleftrightarrow$ ఝు:\*\* \*సుడియుచు భృంగసంఘముల ఝుమ్మని రేఁపుచు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1361)\[cite: 7\].

&nbsp;

\---

&nbsp;

\#\#\# 6.21 ‘వ-బ’ల యతి / అభేద యతి (Abhēda Yati — Non-Difference of 'Va' and 'Ba')

&nbsp;

\* \*\*Definition & Mechanics:\*\* Labio-dental glide \*\*'వ'\*\* (\*va\*) and voiced bilabial stop \*\*'బ'\*\* (\*ba\*) possess mutual Yati affinity\[cite: 7\].

\* \*\*Grammatical Foundation:\*\* Grounded in the classical Pāṇinian and Prakritic phonetic maxim:

  $$\\mathbf{వబయోరభేదః} \\quad (\\text{Vabayōr Abhēdaḥ} \\implies \\text{Non-distinction between } V \\text{ and } B)$$\[cite: 7\].

\* \*\*Lexical Doublets Supporting the Rule:\*\* Attested widely across Sanskrit, Tadbhava, and native Desya doublets\[cite: 7\]:

  \* \*విభీషికా $\\longleftrightarrow$ బిభీషికా\*\[cite: 7\]

  \* \*వలాహక $\\longleftrightarrow$ బలాహక\*\[cite: 7\]

  \* \*వీరము $\\longleftrightarrow$ బీరము\*\[cite: 7\]

  \* \*వివ్వచ్చుఁడు $\\longleftrightarrow$ బీభత్సుఁడు\*\[cite: 7\]

  \* \*ఆవిడ $\\longleftrightarrow$ ఆబిడ\*\[cite: 7\]

  \* \*సవబు $\\longleftrightarrow$ సబబు\*\[cite: 7\]

\* \*\*Vowel Governance:\*\* Follows the standard vowel-class partition (\*\*వ-బ, వి-బి, వు-బు\*\*, etc.)\[cite: 7\].

&nbsp;

\#\#\#\# Critical Textual Dispute: Śabda-Siddha vs. Ādeśa 'Va' (6.21.1)

\* \*\*Two Classes of 'Va':\*\*

  1\. \*శబ్దసిద్ధ 'వ' (Alaghu / Inherent Radical):\* Root words (\*వరుణ, భావము, నావ, నీవు, వెన్న\*)\[cite: 7\].

  2\. \*ఆదేశ 'వ' (Laghu / Gasadadavādeśa Mutation):\* Mutated consonant derived from unvoiced bilabial stop \*\*'ప'\*\* via \*Gasadadavādeśa Sandhi\* ($\\text{అతఁడు} \+ \\text{పలికె} \\rightarrow \\text{అతఁడు వలికె}$; $\\text{నిదుర} \+ \\text{పోయి} \\rightarrow \\text{నిదురవోయి}$)\[cite: 7, 7\].

\* \*\*Appakavi's Historical Error (\*Appakavīyamu\* 2-249..252):\*\*

  \* Appakavi insisted that only inherent radical 'va' (\*Jāti-vā\*) could participate in Yati with \*\*'బ'\*\* (and later with \*ప, ఫ, భ\*)\[cite: 7\]. He claimed that sandhi-mutated 'va' (\*Lāti-vā\*) was completely forbidden in Yati, asserting that Nannaya never sanctioned it\[cite: 7\].

\* \*\*The Philological Refutation (6.21.3):\*\*

  \* The text systematically refutes Appakavi\[cite: 7\]. Classical poetry demonstrates that \*\*both inherent 'va' (Alaghu) and mutated 'va' (Laghu) are equally valid in Abhēda Yati\*\*\[cite: 7\].

  \* Crucially, Nannaya's \*Mahābhārata\* contains direct, indisputable proof of Ādeśa 'va' rhyming with \*\*'బ'\*\*\[cite: 7\]\!

&nbsp;

\#\#\#\# Canonical Provenance for Abhēda Yati (6.21.2 – 6.21.3)

\* \*\*Group A: Inherent Radical 'Va' (శబ్దసిద్ధ / అలఘు 'వ') with 'బ' (6.21.2):\*\*

  \* \*\*బా $\\longleftrightarrow$ వ:\*\* \*బాధ గావించి కుడిచి శవంబు దొలుచు...\* (\*Bhāratam\*, Śānti 3-182)\[cite: 7\].

  \* \*\*బి $\\longleftrightarrow$ వి:\*\* \*బిసరుహగర్భు వ్రాఁతయును విష్ణుని చక్రము వజ్రవజ్రమున్...\* (\*Vēmulavāḍa Bhīmakavi Chāṭu\* / \*Appakavīyamu\* 3-91)\[cite: 7\].

  \* \*\*బృ $\\longleftrightarrow$ వి:\*\* \*...బృందనుతిన్ సనాతనుఁడు విష్ణువు దోఁచె ధరన్...\* (\*Amuktamālyada\* 1-7)\[cite: 7\].

  \* \*\*బె $\\longleftrightarrow$ వె:\*\* \*...బెనుఁబ్రాపై యుండ నేను వెఱతునె యెట్టై...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 292)\[cite: 7\].

  \* \*\*బు $\\longleftrightarrow$ వు:\*\* \*...బుట్టిన సంతసంబుననువుం బరికించితి...\* (\*Bhāratam\*, Sabhā 2-278)\[cite: 7\].

  \* \*\*వు $\\longleftrightarrow$ బు:\*\* \*...సేకూఱఁబోవుదు నా తృష్ణ ఋభుక్ష యిప్పుడ వెసంబుత్తున్మహావగ్రహా...\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 19)\[cite: 7\].

  \* \*\*వు $\\longleftrightarrow$ బో:\*\* \*...పావులవలెనిట్టటుల్ కదుపుఁ బోవును వచ్చున యాట...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Araṇya 380)\[cite: 7\].

\* \*\*Group B: Mutated Gasadadavādeśa 'Va' (ఆదేశ / లఘు 'వ') with 'బ' (6.21.3 — Corpus Proof):\*\*

  \* \*\*వ $\\longleftrightarrow$ బ (Nannaya):\*\* \*...అభిమతములు వడయుదురు \[= పడయుదురు\]... మేధికంబునాఁబరఁగు తీర్థ...\* (\*Bhāratam\*, Sabhā 2-279)\[cite: 7\].

  \* \*\*వ $\\longleftrightarrow$ బా (Nannaya):\*\* \*...పేదవడినఁ \[= పడిన\] జూచియు దీర్ఘబాహుయుగళు...\* (\*Bhāratam\*, Āraṇya 1-215)\[cite: 7\].

  \* \*\*బు $\\longleftrightarrow$ వొ:\*\* \*బుద్ధి తద్దయు దుఃఖంబువొందె \[= పొందె\] నిపుడు...\* (\*Bhāratam\*, Ādi 5-31)\[cite: 7\].

  \* \*\*బూ $\\longleftrightarrow$ వొ (Nannaya):\*\* \*బూతువొగడినట్లు వొగడెదు \[= పొగడెదు\] పొగడంగ...\* (\*Bhāratam\*, Sabhā 2-48)\[cite: 7\].

  \* \*\*వొ $\\longleftrightarrow$ బొ:\*\* \*...మీరు వొగలనేల \[= పొగడనేల\] వగలఁబొరలనేల...\* (\*Bhāgavatam\* 7-53)\[cite: 7\].

  \* \*\*బు $\\longleftrightarrow$ వో:\*\* \*...నీకునిటువోవుట \[= పోవుట\] ధర్మువుగాదు వైన్య భూ...\* (\*Bhāratam\*, Udyōga 4-193)\[cite: 7\]; \*...రిత్తవోనిచ్చెదనే \[= పోనిచ్చెదనే\]...\* (\*Bhāratam\*, Udyōga 7-62)\[cite: 7\]; \*...నిదురవోయి \[= పోయి\] గరుత్తతి పచ్చఁబాఱినన్...\* (\*Amuktamālyada\* 1-64)\[cite: 7\]; \*...యింటిదెసవోవుట \[= పోవుట\] మాని విభుండు...\* (\*Bhāratam\*, Udyōga 4-89)\[cite: 7\].

  \* \*\*బొ $\\longleftrightarrow$ వు:\*\* \*...కుమారులువుట్టునట్టి \[= పుట్టునట్టి\]...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 236)\[cite: 7\].

  \* \*\*బొ $\\longleftrightarrow$ వో:\*\* \*...నిద్రవోయెడు \[= పోయెడు\] శరమున్...\* (\*Bhāratam\*, Virāṭa 6-54)\[cite: 7\].

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (Part 5 Summary)

&nbsp;

| Rule Type | Primary Alliterative Units | Phonetic / Grammatical Constraint | Status in Engine |

| :--- | :--- | :--- | :--- |

| \*\*ఋజుయతి (6.16)\*\* | \*\*య $\\longleftrightarrow$ హ\*\*\[cite: 7\] | Vowel classes must align ($A, I, U$ series)\[cite: 7\]. | \*\*Canonical\*\*\[cite: 7\] |

| \*\*సరసయతి-2 (6.17)\*\* | \*\*అ $\\longleftrightarrow$ య\*\*\[cite: 7\] | Applies strictly to radical \*\*శబ్దసిద్ధ 'య'\*\*\[cite: 7\]. Mutated \*\*యడాగమము\*\* bypasses to \*Svara-Pradhāna\*\[cite: 7\]. | \*\*Canonical\*\*\[cite: 7\] |

| \*\*సరసయతి-3 (6.18)\*\* | \*\*అ $\\longleftrightarrow$ హ\*\*\[cite: 7\] | Forms closed triad with 6.16 and 6.17 (\*\*{అ \- య \- హ}\*\*)\[cite: 7\]. | \*\*Canonical\*\*\[cite: 7\] |

| \*\*ఊష్మయతి (6.19)\*\* | \*\*శ $\\longleftrightarrow$ ష $\\longleftrightarrow$ స\*\*\[cite: 7\] | Mutual sibilant affinity; glottal 'హ' excluded\[cite: 7\]. | \*\*Canonical\*\*\[cite: 7\] |

| \*\*సరసయతి-4 (6.20)\*\* | \*\*{శ, ష, స} $\\longleftrightarrow$ {చ, ౘ, ఛ, జ, ౙ, ఝ}\*\*\[cite: 7\] | 18 base pairs; dental affricates restricted to compatible vowel sets\[cite: 7\]. | \*\*Canonical\*\*\[cite: 7\] |

| \*\*అభేదయతి (6.21)\*\* | \*\*వ $\\longleftrightarrow$ బ\*\*\[cite: 7\] | Applies to \*\*both\*\* inherent radical 'వ' and mutated \*Gasadadavādeśa\* 'వ'\[cite: 7\]. | \*\*Canonical\*\* (Appakavi's restriction overturned)\[cite: 7\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.22 అభేదవర్గ యతులు (Abhēdavarga Yatulu — 'Va' to Bilabial Stops 'Pa, Pha, Bha')

* **Definition & Mechanics:** Labio-dental glide **'వ'** (*va*) possesses mutual Yati affinity with the voiceless and aspirated stops of the labial class: **'ప'** (*pa*), **'ఫ'** (*pha*), and **'భ'** (*bha*).

$$\\mathbf{‘వ’} \\quad\\longleftrightarrow\\quad {\\mathbf{ప,\\ ఫ,\\ భ}}$$

* **Derivation Tree & Theoretical Mechanics:**  
1. *Abhēda Yati Baseline (6.21):* **'వ'** and **'బ'** share intrinsic non-difference (*vabayōr abhēdaḥ*).  
2. *Vargaja Integration (6.11):* Bilabial stop **'బ'** naturally rhymes with all stops of its own class (**ప, ఫ, బ, భ**).  
3. *The Bridge:* Because **'వ'** is phonetically equated with **'బ'**, it inherits alliterative access to the remaining members of the labial stop series (**ప, ఫ, భ**). Hence, Appakavi designates this structural expansion as **అభేదవర్గ యతి** (*Abhēdavarga Yati*).  
4. *Supplementary Justification:* In native Telugu morphophonemics (*Gasadadavādeśa Sandhi*), initial **'ప'** mutates directly into **'వ'**. Thus, **'వ'** shares direct organic affinity with **'ప'**, which naturally extends to aspirate **'ఫ'** and voiced aspirate **'భ'**.

                 Abhēdavarga Yati Derivation Architecture

                       \[ వ (Labio-dental Glide) \]

                                   │

                 Abhēda Yati (6.21: వబయోరభేదః)

                                   ▼

                       \[ బ (Voiced Bilabial Stop) \]

                                   │

                 Vargaja Yati (6.11: Pa-varga Stops)

                 ┌─────────────────┼─────────────────┐

                 ▼                 ▼                 ▼

          \[ ప (Voiceless) \] \[ ఫ (Aspirate) \] \[ భ (Voiced Asp.) \]

                 │                 │                 │

                 └─────────────────┼─────────────────┘

                                   │

               (Inherited by 'వ' via Abhēda Bridge)

                                   ▼

          { వ \- ప }            { వ \- ఫ }            { వ \- భ }

\`\`\`\[cite: 8\]

&nbsp;

\* \*\*Vowel-Class Governance (6.22.1):\*\* All three pairings (\*\*వ-ప, వ\-ఫ, వ\-భ\*\*) must strictly satisfy the tripartite vowel grid (\*Svaramaitri Vargamulu\* 6.2.1)\[cite: 8\]:

  \* \*Class 1 ($A$-varga: అ, ఆ, ఐ, ఔ):\* \*\*వ, వా, వై, వౌ $\\longleftrightarrow$ ప/ఫ/భ, పా/ఫా/భా, పై/ఫై/భై, పౌ/ఫౌ/భౌ\*\*\[cite: 8\].

  \* \*Class 2 ($I$-varga: ఇ, ఈ, ఋ, ౠ, ఎ, ఏ):\* \*\*వి, వీ, వృ, వె, వే $\\longleftrightarrow$ పి/ఫి/భి, పీ/ఫీ/భీ, పృ/ఫృ/భృ, పె/ఫె/భె, పే/ఫే/భే\*\*\[cite: 8\].

  \* \*Class 3 ($U$-varga: ఉ, ఊ, ఒ, ఓ):\* \*\*వు, వూ, వొ, వో $\\longleftrightarrow$ పు/ఫు/భు, పూ/ఫూ/భూ, పొ/ఫొ/భొ, పో/ఫో/భో\*\*\[cite: 8\].

&nbsp;

\#\#\#\# Dual Nature of 'Va' & Refutation of Appakavi's Restriction (6.22.2, 6.22.6)

\* \*\*The Structural Dichotomy:\*\*

  1\. \*శబ్దసిద్ధ 'వ' (Alaghu / Inherent Radical):\* Foundational root consonant in native or Sanskrit words (\*వనము, వన్నె, విష్ణువు, వారు\*)\[cite: 8\].

  2\. \*ఆదేశ 'వ' (Laghu / Mutated Stop):\* Generated when initial \*\*'ప'\*\* undergoes lenition into \*\*'వ'\*\* via \*Gasadadavādeśa\* (\*ప్రొద్దు \+ పడక \= ప్రొద్దువడక\*; \*నిదుర \+ పోయి \= నిదురవోయి\*)\[cite: 8\].

\* \*\*Appakavi's Arbitrary Limitation:\*\* Appakavi asserted that only inherent \*'va'\* (\*Jāti-vā\*) was eligible for Yati with \*\*ప, ఫ, భ\*\*, claiming mutated \*'va'\* (\*Lāti-vā\*) was banned in Yati and absent in Nannaya\[cite: 8\].

\* \*\*The Classical Evidence (6.22.6):\*\* The text definitively refutes Appakavi\[cite: 8\]. Nannaya's \*Mahābhārata\* and subsequent classical epics consistently employ mutated \*\*ఆదేశ 'వ'\*\* with \*\*ప, ఫ, భ\*\*\[cite: 8\]. Both \*Alaghu\* and \*Laghu\* 'va' forms are fully canonical in the Yati engine\[cite: 8\].

&nbsp;

\#\#\#\# Philological Analysis of Variant Readings (పాఠాంతర విచారము 6.22.3, 6.22.5)

Later commentators who failed to recognize \*Abhēdavarga Yati\* altered classical manuscripts to force standard \*Prāṇi Yati\*\[cite: 8\]:

\* \*Altered Line 1:\* Nannaya's \*మహీవల్లభ తక్షకాధము నెపంబున...\* (\*\*వ $\\longleftrightarrow$ ప\*\*) was altered by scribes to \*నెవంబున\* to manufacture a forced \*\*వ $\\longleftrightarrow$ వ\*\* match\[cite: 8\].

\* \*Altered Line 2:\* \*...ధ్యానోపరతేంద్రియ... వాని శమీకున్\* (\*\*ప $\\longleftrightarrow$ వా\*\*) was corrupted into \*ధ్యానావరతేంద్రియ\*\[cite: 8\].

\* \*Altered Line 3:\* \*...యుగంబుల పార... వారికిఁ బడయన్\* (\*\*పా $\\longleftrightarrow$ వా\*\*) was rewritten to \*యుగంబులవార\*\[cite: 8\].

\* \*Altered Line 4:\* Tikkana's \*వీరు వారనునట్టి బుద్ధివిభేద మెన్నఁడు లేదు...\* (\*\*వీ $\\longleftrightarrow$ భే\*\*) was altered to \*బుద్ధివివేకమెన్నడు\* to force \*\*వీ $\\longleftrightarrow$ వే\*\*\[cite: 8\].

\* \*Altered Line 5:\* Nannaya's \*...వ్రత యొక బావిమేలు మఱి బావులు...\* (\*\*వ్ర \[వ\] $\\longleftrightarrow$ బా\*\*) was altered to \*వావులు\*\[cite: 8\].

\* \*\*Editorial Conclusion:\*\* The original readings (\*నెపంబున, బావులు, విభేదము\*) represent natural, authoritative diction (\*Mahākavi prayōgamu\*)\[cite: 8\]. The variants are artificial copyist interpolations (\*kalpitamulu\*) created by late grammarians unaware of the legitimate \*Abhēdavarga Yati\* rule\[cite: 8\].

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.22.4)

\* \*\*'వ' with 'ప' (Inherent Radical 'Va'):\*\*

  \* \*\*వ $\\longleftrightarrow$ ప:\*\* \*...మహీవల్లభ తక్షకాధము నెపంబున సర్పములెల్లనగ్నిలో...\* (\*Appakavīyamu\* 3-99 / \*Bhāratam\*, Ādi 1-125)\[cite: 8\].

  \* \*\*ప $\\longleftrightarrow$ వ:\*\* \*పండితులైనవారు దిగువం దగనుండగ...\* (\*Bhāskara Śatakam\*)\[cite: 8\].

  \* \*\*ప $\\longleftrightarrow$ వా:\*\* \*...పరమధ్యానోపరతేంద్రియవృత్తినున్నవాని శమీకున్...\* (\*Appakavīyamu\* 3-100 / \*Bhāratam\*, Ādi 2-170)\[cite: 8\].

  \* \*\*వా $\\longleftrightarrow$ ప:\*\* \*...సంవాసనమావహిల్లు జనపంక్తులు...\* (\*Bhāratam\*, Svargārohaṇa 92)\[cite: 8\].

  \* \*\*పా $\\longleftrightarrow$ వా:\*\* \*...నరునియేయునపారశరావలులనడుమ వారింపంగా...\* (\*Bhāratam\*, Ādi 7-199)\[cite: 8\]; \*...యుగంబుల పారతపో యుక్తులైన వారికిఁ...\* (\*Appakavīyamu\* 3-101 / \*Bhāratam\*, Ādi 1-370)\[cite: 8\].

  \* \*\*ప $\\longleftrightarrow$ వై:\*\* \*పరతురగంబులం దునిమివైచుచు వానరయూథనాయకుల్...\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1675)\[cite: 8\].

  \* \*\*వు $\\longleftrightarrow$ పు:\*\* \*...జీవులు నానాఫల కర్మభోక్తలుగనింపుంబొంది పోకారి వా...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Araṇya 384)\[cite: 8\].

  \* \*\*వు $\\longleftrightarrow$ పూ:\*\* \*...వుఁడు చనుచున్నవాఁడురక పూజ్యనిగర్హణనింద...\* (\*Śaśāṅkavijayamu\* 2-37)\[cite: 8\].

  \* \*\*వు $\\longleftrightarrow$ పొ:\*\* \*...కావున రాజ్యక్రమము వారు పొందెదరవనిన్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 192)\[cite: 8\].

  \* \*\*వు $\\longleftrightarrow$ పో:\*\* \*...వుల విధియాటకాఁడు పలుపోకలఁ ద్రిప్పును...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 111)\[cite: 8\].

\* \*\*'వ' with 'ప' (Mutated Ādeśa 'Va' via Gasadadavādeśa):\*\*

  \* \*\*వ $\\longleftrightarrow$ ప:\*\* \*...మహీపతులచేఁ జూడంగఁబడితినింత వడుదునె \[= పడుదునె\]... పలుకులకెవ్వరు...\* (\*Bhāratam\*, Sabhā 2-244)\[cite: 8\]; \*...లోచనంబు లెఱుకవడక \[= పడక\] యుండ వదనపద్మంబు వాంచి...\* (\*Bhāratam\*, Udyōga 2-194)\[cite: 8\].

  \* \*\*ప $\\longleftrightarrow$ వ:\*\* \*పవనగతిం బఱచుఁ బ్రొద్దువడకుండగనే \[= పడకుండఁగనే\]...\* (\*Bhāratam\*, Udyōga 2-168)\[cite: 8\].

  \* \*\*వ $\\longleftrightarrow$ పా:\*\* \*...చిక్కువడిన \[= పడిన\] చూపులు దిగువనుపాయమేది...\* (\*Bhāratam\*, Virāṭa 8-184)\[cite: 8\].

  \* \*\*పా $\\longleftrightarrow$ వ:\*\* \*...పాయంబునుఁబొంది చిక్కువడిరి \[= పడిరి\] నరేంద్రా...\* (\*Bhāratam\*, Virāṭa 8-338)\[cite: 8\].

  \* \*\*వ $\\longleftrightarrow$ పౌ:\*\* \*...పుట్టుగువడసినపుడ \[= పడసినపుడ\] కాదె నాదు పౌరుషమడఁగెన్...\* (\*Bhāratam\*, Āraṇya 3-272)\[cite: 8\].

  \* \*\*పృ $\\longleftrightarrow$ వె:\*\* \*పృథివిఁగల తీర్థముల లెక్కవెట్టి \[= పెట్టి\] చూచి...\* (\*Manu Caritra\* 2-3)\[cite: 8\].

  \* \*\*పు $\\longleftrightarrow$ వొ:\*\* \*పుణ్యకర్మంబులు వొలిసిన \[= పొలిసిన\] నుర్వికి...\* (\*Bhāratam\*, Āraṇya 1-191)\[cite: 8\]; \*పురుషునిఁదడయక ప్రశాంతివొందు \[= పొందు\] నరేంద్రా...\* (\*Bhāratam\*, Udyōga 5-621)\[cite: 8\].

  \* \*\*పూ $\\longleftrightarrow$ వొ:\*\* \*పూన్కితో వీరరసలక్ష్మి వొదలనడచె \[= పొదలనడచె\]...\* (\*Amuktamālyada\* 4-44)\[cite: 8\].

  \* \*\*పూ $\\longleftrightarrow$ వో:\*\* \*పూని యౌదలఁ దలఁబ్రాలువోసి \[= పోసి\] తాళి...\* (\*Manu Caritra\* 1-114)\[cite: 8\].

  \* \*\*వో $\\longleftrightarrow$ పొ:\*\* \*...మండలములు వోలె \[= పోలె\] విమానముల్ పొలిచి వెలుఁగ...\* (\*Bhāratam\*, Virāṭa 4-43)\[cite: 8\].

\* \*\*'వ' with 'ఫ':\*\*

  \* \*\*వ $\\longleftrightarrow$ ఫ:\*\* \*వనవాసంబునఁ గష్టముం దపము సాఫల్యంబునుంజెప్పి...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 20)\[cite: 8\]; \*ఫలియించెనటంచుగాని వదరెదు సుమ్మీ...\* (\*Manu Caritra\* 5-58)\[cite: 8\].

  \* \*\*ఫ $\\longleftrightarrow$ వా:\*\* \*...ఫక్కికి వచ్చినాము కరవాలమె నీకు శరణ్యమన్నిటన్...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Yuddha 140)\[cite: 8\].

  \* \*\*ఫె $\\longleftrightarrow$ వి:\*\* \*ఫెళ్ళున వెన్నెముకలందు విఱుచుచు మెడలన్...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Yuddha 42)\[cite: 8\].

  \* \*\*ఫే $\\longleftrightarrow$ వే:\*\* \*ఫేనఖండమనిలవేగవశము...\* (\*Śivarātri Māhātmyamu\* 5-62)\[cite: 8\].

\* \*\*'వ' with 'భ' (Inherent and Ādeśa Forms):\*\*

  \* \*\*భా $\\longleftrightarrow$ వ:\*\* \*భావించియ వచ్చియుంటి వలదని యనుచో...\* (\*Bhāratam\*, Udyōga 5-21)\[cite: 8\]; \*భారము వన్నెకెక్కు దురవస్థలు నీ కర...\* (\*Bhāratam\*, Virāṭa 3-63)\[cite: 8\].

  \* \*\*వా $\\longleftrightarrow$ భ:\*\* \*వావిరి చూచి నిక్కముగ భర్తలఁదారనురక్తలయ్యునున్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 383)\[cite: 8\].

  \* \*\*వి $\\longleftrightarrow$ భి:\*\* \*విని దనుజ పరిహాసానభిజ్ఞ యగుట...\* (\*Gōpīnātha Rāmāyaṇamu\*, Araṇya 300)\[cite: 8\].

  \* \*\*వీ $\\longleftrightarrow$ భే:\*\* \*వీరు వారనునట్టి బుద్ధివిభేద మెన్నఁడు లేదు...\* (\*Appakavīyamu\* 3-103 / \*Bhāratam\*, Ādi 8-29, Mattakōkila)\[cite: 8\].

  \* \*\*వ $\\longleftrightarrow$ భా (Ādeśa):\*\* \*...లోకంబులు వడసి \[= పడసి\] భాగధేయ భాగులయిరి...\* (\*Bhāratam\*, Sabhā 1-204)\[cite: 8\].

  \* \*\*భూ $\\longleftrightarrow$ వొ (Ādeśa):\*\* \*భూషణ దీప్తులు వొలియంగ \[= పొలియంగ\] వివృత కే...\* (\*Bhāratam\*, Āraṇya 1-191)\[cite: 8\].

  \* \*\*భో $\\longleftrightarrow$ వొ (Ādeśa):\*\* \*భోరున విస్ఫులింగములు వొడ్మఁగఁ \[= పొడ్మఁగ\] దన్ముఖ...\* (\*Bhāratam\*, Virāṭa 4-409)\[cite: 8\].

  \* \*\*భో $\\longleftrightarrow$ వో (Ādeśa):\*\* \*...విడ్వుమెటవోయినఁ \[= పోయిన\] బ్రాణము గొందునింకఁ...\* (\*Bhāratam\*, Virāṭa 5-179)\[cite: 8\].

  \* \*\*వొ $\\longleftrightarrow$ భు (Ādeśa):\*\* \*...శోకము వొదలెడి \[= పొదలెడి\] వామాంకనేత్రభుజములదరెడిన్...\* (\*Gōpīnātha Rāmāyaṇamu\*, Araṇya 1034)\[cite: 8\].

&nbsp;

\---

&nbsp;

\#\#\# 6.23 'ల \- ళ' యతి / అభేద యతి-2 (Abhēda Yati-2 — Non-Difference of 'La' and 'Ḷa')

&nbsp;

\* \*\*Definition & Mechanics:\*\* Dental lateral liquid \*\*'ల'\*\* (\*la\*) and retroflex lateral liquid \*\*'ళ'\*\* (\*ḷa\*) possess mutual Yati affinity across all poetic forms\[cite: 8\].

\* \*\*Phonological & Lexical Domains:\*\*

  1\. \*Sanskrit Loanwords (Tatsamas):\* Sanskrit words formed with dental \*la\* (\*వేలా, కలా, తరల, మంగళ\*) are orthographically and phonologically rendered in Telugu with retroflex \*ḷa\* (\*వేళా, కళా, తరళ, మంగళ\*)\[cite: 8\]. The underlying equivalence ensures complete caesura affinity between lexical \*\*'ల'\*\* and \*\*'ళ'\*\*\[cite: 8\].

  2\. \*Native Telugu Roots (Desyas):\* Inherent, non-Sanskrit words containing retroflex \*ḷa\* (\*తళుకుబెళుకులు, కేళాకూళి, కూళలు, మేళము, కళవళించు, చోళ\*) freely alliterate with standard dental \*\*'ల'\*\*\[cite: 8\].

  3\. \*Mutated Retroflex Augments (Ādeśa Ḷa):\* In plural formations (\*bahuvacana\*), the consonant set \*\*'డ, ల, ర'\*\* optionally mutates into retroflex \*\*'ళ'\*\* (\*త్రాడులు $\\rightarrow$ త్రాళులు\*; \*పాలులు $\\rightarrow$ పాళులు\*; \*ఊరులు $\\rightarrow$ ఊళులు\*; \*కాళ్లు $\\rightarrow$ కాళులు\*)\[cite: 8\]. By \*Bāla Vyākaraṇam\* (Prakīrṇaka 24: \*"య వ ల'లు లఘ్వలఘువులు మైత్రింబొరయు రేఫంబులు పొరయవు"\*), light \*la\* (\*laghu\*) and heavy/mutated \*ḷa\* (\*alaghu\*) share full poetic harmony\[cite: 8\].

\* \*\*Vowel-Class Governance (6.23.1):\*\* Follows the baseline tripartite vowel grid:

  \* Class 1 ($A$-varga): \*\*ల, లా, లై, లౌ $\\longleftrightarrow$ ళ, ళా, ళై, ళౌ\*\*\[cite: 8\].

  \* Class 2 ($I$-varga): \*\*లి, లీ, లె, లే $\\longleftrightarrow$ ళి, ళీ, ళె, ళే\*\*\[cite: 8\].

  \* Class 3 ($U$-varga): \*\*లు, లూ, లొ, లో $\\longleftrightarrow$ ళు, ళూ, ళొ, ళో\*\*\[cite: 8\].

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.23.2 – 6.23.4)

\* \*\*Tatsama / Sanskrit Loanword Forms (6.23.2):\*\*

  \* \*\*ల $\\longleftrightarrow$ ళ:\*\* \*లలిత కృశోదరంబుఁ దరళత్రివళీయుత...\* (\*Bhāratam\*, Ādi 4-44)\[cite: 8\]; \*...తలంచి యుత్తమ గో యుగళంబు నిలిచి...\* (\*Bhāratam\*, Udyōga 4-155)\[cite: 8\]; \*లక్ష్మి యింతొప్పునే మరాళమున కనుచు...\* (\*Kāśīkhaṇḍam\* 1-104)\[cite: 8\].

  \* \*\*ళ $\\longleftrightarrow$ ల:\*\* \*...వేళను జనియించితో యకట లచ్చికినమ్మధు...\* (\*Kāśīkhaṇḍam\* 2-135)\[cite: 8\]; \*...నీ జనన వేళన్ రోదనం బిచ్చుటన్... లాలనముందోఁపఁ...\* (\*Bhāgavatam\* 3-368)\[cite: 8\].

  \* \*\*ల $\\longleftrightarrow$ ళా:\*\* \*...లనవనమునకై చక్రధరకళాకలితుండై...\* (\*Bhāratam\*, Udyōga 4-216)\[cite: 8\].

  \* \*\*లా $\\longleftrightarrow$ ళ:\*\* \*...కైలాసమువోలెఁ బ్రాంశుధవళంబగు...\* (\*Bhāratam\*, Virāṭa 4-19)\[cite: 8\].

  \* \*\*ళ $\\longleftrightarrow$ లా:\*\* \*...వేళ రమింపంగ నిషిద్ధకర్మమగునేలా...\* (\*Bhāratam\*, Sabhā 3-460)\[cite: 8\].

  \* \*\*ళీ $\\longleftrightarrow$ లి:\*\* \*...శీకృత పాణిపయోరుహాళి మాలిక కుటిలాలకాలిక...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 169)\[cite: 8\]; \*...దండుకలభాలిక... పాళివలయంబు లోనఁ... విశాలలోచనన్\* (\*Kāśīkhaṇḍam\* 7-165)\[cite: 8\].

  \* \*\*ళ $\\longleftrightarrow$ లీ:\*\* \*...కబళించుఁ జకోరికలు సమద లీలాలసలై...\* (\*Manu Caritra\* 6-47)\[cite: 8\]; \*...మాలాకలితమై... తరంగ పాళిం దుమికించుచున్ విధుర లీలను...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 392)\[cite: 8\]; \*...కాలంబున వనపాలకులు... వీర కేళీరసికుండు వారినవలీలమెయిం...\* (\*Bhāratam\*, Ādi 7-71)\[cite: 8\]; \*...లలితోత్పలకళికా... దళీపరులై వెడలిరుగ్రలీలలు మెఱయన్...\* (\*Bhāratam\*, Virāṭa 3-68)\[cite: 8\].

  \* \*\*లీ $\\longleftrightarrow$ ళి:\*\* \*...లీలమోవులు కబళించి చెక్కు...\* (\*Bhāratam\*, Udyōga 8-38)\[cite: 8\]; \*...కాళియ దర్పఘ్న... వనమాలీ కృష్ణ...\* (\*Manu Caritra\* 2-56)\[cite: 8\].

  \* \*\*లీ $\\longleftrightarrow$ ళీ:\*\* \*లీలంగానమర్చి మత్తగజ కేళీసుందరోల్లాస...\* (\*Bhāratam\*, Virāṭa 3-210)\[cite: 8\]; \*లీలాస్వీకృత చక్రశూలవినతాళీరక్షణాలోల...\* (\*Bhāratam\*, Sabhā 5-630)\[cite: 8\]; \*...లీలమాణిక్యాంగుళీయకములు...\* (\*Amuktamālyada\* 1-41)\[cite: 8\]; \*కోలాహలశైలాధిప లీలాగతుఁడైన పతి యళీక యతీంద్రున్... కళాలోలతనని...\* (\*Manu Caritra\* 3-64)\[cite: 8\].

  \* \*\*లే $\\longleftrightarrow$ ళీ:\*\* \*లేమయొకర్తు వేడుకనళీకనళీకరణంబు...\* (\*Kāśīkhaṇḍam\* 3-98)\[cite: 8\].

  \* \*\*ళా $\\longleftrightarrow$ లే:\*\* \*...యోగి హృన్నాళాంతర్నిజ నివాస లేఖాధిప...\* (\*Bhāratam\*, Virāṭa 6-1)\[cite: 8\].

\* \*\*Native Telugu Desya Roots (6.23.3):\*\*

  \* \*\*ల $\\longleftrightarrow$ ళ:\*\* \*...లీల మెయిన్ జోళుని భూమిపై నిలిపి చోళస్థాపనాచార్య...\* (\*Manu Caritra\* 1-34)\[cite: 8\].

  \* \*\*ల $\\longleftrightarrow$ ళా:\*\* \*లలితైణాంక శిలాలవాలమను కేళాకూళిలో...\* (\*Manu Caritra\* 1-160)\[cite: 8\].

  \* \*\*లా $\\longleftrightarrow$ ళ:\*\* \*...హేలారతి డాగు రేకుల తళత్తళ కాటుక...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 6)\[cite: 8\].

  \* \*\*ల $\\longleftrightarrow$ ళి:\*\* \*...దూలిన వెసనెంతయుం గళవళించు మనోజ...\* (\*Bhāratam\*, Virāṭa 2-31)\[cite: 8\].

\* \*\*Mutated Ādeśa 'Ḷa' (6.23.4):\*\*

  \* \*\*ళు $\\longleftrightarrow$ లో:\*\* \*...కాళులఁబడి \[= కాలు \+ లు $\\rightarrow$ కాళులు\] గడ్డమంటి యెటులో బతిమాలి యవస్థనంది లో...\* (\*Udayaśrī\*, Bīdapūja)\[cite: 8\].

&nbsp;

\---

&nbsp;

\#\#\# 6.24 ‘ము’ విభక్తి యతి / పోలిక వడి (Mu-Vibhakti Yati / Pōlika Vaḍi)

&nbsp;

\* \*\*Definition & Mechanics:\*\* The nominal affix \*\*'ము'\*\* (\*mu\*)—whether acting as the nominative case suffix (\*mu-varṇakamu\*) or as an inflected stem augment (\*mugāgamamu\*)—possesses direct Yati affinity with the non-nasal stops of the labial class when combined with \*\*Class 3 ($U$-varga) vowels\*\*: \*\*'పు, ఫు, బు, భు'\*\*\[cite: 8\].

\* \*\*Nomenclature:\*\* Designated \*\*'ము'విభక్తి యతి\*\* by Appakavi, and canonicalized in earlier treatises (\*Anantudu, Kavijanāśrayamu, Kāvyālaṅkāra Cūḍāmaṇi, Lakṣaṇa Śirōmaṇi\*) as \*\*పోలిక వడి\*\* (\*Pōlika Vaḍi\*) or \*\*పోలిక యతి\*\* (\*Pōlika Yati\*)\[cite: 8\].

\* \*\*The Structural Paradox & Specialized License:\*\*

  \* Under standard \*Vargaja Yati\* (6.11), stops (ప, ఫ, బ, భ) can \*\*never\*\* rhyme with their class nasal stop (మ)\[cite: 8\].

  \* Under standard \*Bindu Yati\* (6.12), stops can rhyme with a nasal \*\*only if preceded by an anusvāra\*\* (\*\*ంప, ంబ, ంభ $\\longleftrightarrow$ మ\*\*)\[cite: 8\].

  \* \*The Exception:\* \*Pōlika Vaḍi\* breaks this barrier without an anusvāra, granting \*\*'ము'\*\* alliterative compatibility with the four labial stops solely because they share labial articulation (\*ōṣṭhya\*) and Class 3 vowel rounding (\*u-kāra\*)\[cite: 8\].

&nbsp;

&nbsp;

                 Pōlika Vaḍi Permutation Matrix

             \[ Nominal Affix / Augment: 'ము' (Mu) \]

                                │

       (Rhymes bidirectionally with Class 3 Labial Stops)

                                ▼

   ┌───────────────────┬───────────────────┬───────────────────┐

   ▼                   ▼                   ▼                   ▼

&nbsp;

{ ప-Series }        { ఫ-Series }        { బ-Series }        { భ-Series } • పు (Pu)           • ఫు (Phu)          • బు (Bu)           • భు (Bhu) • పూ (Pū)           • ఫూ (Phū)          • బూ (Bū)           • భూ (Bhū) • పొ (Po)           • ఫొ (Pho)          • బొ (Bo)           • భొ (Bho) • పో (Pō)           • ఫో (Phō)          • బో (Bō)           • భో (Bhō)

\*(Generates exactly $4 \\text{ consonants} \\times 4 \\text{ vowels} \= \\mathbf{16\\ Unique\\ Yati\\ Pairings}$ with 'ము')\*\[cite: 8\].

&nbsp;

\#\#\#\# Morphological Duality: Suffix vs. Augment (6.24.1, 6.24.4)

The engine must validate \*\*'ము'\*\* under two distinct grammatical formations:

1\. \*\*ము-వర్ణకము (Mu-varṇakamu / Suffix):\*\*

   \* Nominative singular case marker on Sanskrit Tatsamas (\*వృక్షము, ధనము, కావ్యము\*), native Desyas (\*బియ్యము, నెయ్యము, తెల్లము\*), and Tadbhavas (\*ఆకసము, సంద్రము, నెపము, కంబము\*)\[cite: 8\].

   \* Conjoined forms containing coordinators like \*-nu(n)\* (\*భయమున్, కులమున్\*) retain their status as \*Mu-varṇakamu\*\[cite: 8\].

2\. \*\*ముగాగమము (Mugāgamamu / Inflected Augment):\*\*

   \* By \*Bāla Vyākaraṇam\* (Tatsama 39-40), when non-nominative singular case affixes (plural \*-lu\*, accusative \*-nu\*, dative \*-ku\*, locative \*-na\*) attach to non-human neuter stems ending in short \*'a'\*, the augment \*\*'ము'\*\* (\*Mugāgama\*) is inserted (\*వృక్ష \+ లు $\\rightarrow$ వృక్షములు\*; \*దైవ \+ కు $\\rightarrow$ దైవమునకు\*)\[cite: 8\].

   \* By \*Bāla Vyākaraṇam\* (Tatsama 41: \*"మువర్ణకంబునకు విధించు కార్యము ముగాగమంబునకునగు"\*), \*\*every grammatical and prosodic rule governing the suffix 'ము' applies identically to the augment 'ము'\*\*\[cite: 8\].

   \* Treatise authors (\*Appakavi, Ananta, Lakṣaṇa Śirōmaṇi\*) cited \*Mugāgama\* forms to illustrate \*Mu-vibhakti Yati\* without segregating them into a separate rule\[cite: 8\].

&nbsp;

\#\#\#\# Treatise Attestations & Primary Definitions (6.24.3 – 6.24.4)

\* \*\*Appakavi's Lakṣya-Lakṣaṇa Stanza (3-70):\*\*

  \* Line 1: \*పుష్కరము... మధ్యమముగ\* (\*\*పు $\\longleftrightarrow$ ము\*\*)\[cite: 8\].

  \* Line 2: \*ఫుల్లపంకేరుహము... వక్త్రముగ\* (\*\*ఫు $\\longleftrightarrow$ ము\*\*)\[cite: 8\].

  \* Line 3: \*బొండు మల్లెలు... దరహాసముగ\* (\*\*బొ $\\longleftrightarrow$ ము\*\*)\[cite: 8\].

  \* Line 4: \*భోజ నృపనందనకు... నిక్కముగ\* (\*\*భో $\\longleftrightarrow$ ము\*\*)\[cite: 8\].

\* \*\*Anantudu's Chandodarpaṇamu (1-106):\*\*

  \* \*...హరిచరణసరోరుహములునా హృత్సరసియందుఁ బొదలుననంగన్\* (\*\*ము $\\longleftrightarrow$ బొ\*\* in \*సరోరుహములు\*)\[cite: 8\].

\* \*\*Lakṣaṇa Śirōmaṇi (4-334):\*\*

  \* \*పోలు దేవరలీ దైవమునకు సరియె...\* (\*\*పో $\\longleftrightarrow$ ము\*\* in \*దైవమునకు\*)\[cite: 8\].

  \* \*పోలు పురములు వైకుంఠమునకు సమమె...\* (\*\*పో $\\longleftrightarrow$ ము\*\* in \*వైకుంఠమునకు\*)\[cite: 8\].

  \* \*భువిని మఱి విద్యలు కవిత్వమునకు సరియె...\* (\*\*భు $\\longleftrightarrow$ ము\*\* in \*కవిత్వమునకు\*)\[cite: 8\].

\* \*\*Kavijanāśrayamu (Saṁjñā 73 / Lakṣaṇa Śirōmaṇi 4-335):\*\*

  \* Line 2: \*పోలికవడి శీలముల్లమునకెనయనఁగా...\* (\*\*పో $\\longleftrightarrow$ ము\*\* in \*ఉల్లమునకు\*)\[cite: 8\].

  \* Line 4: \*భూలోకంబమరలోకమునకెనయనఁగన్...\* (\*\*భూ $\\longleftrightarrow$ ము\*\* in \*అమరలోకమునకు\*)\[cite: 8\].

\* \*\*Kāvyālaṅkāra Cūḍāmaṇi (7-46 / Lakṣaṇa Śirōmaṇi 4-339):\*\*

  \* Lines 1–4: \*\*పు $\\longleftrightarrow$ ము\*\* (\*భుజమునకు\*); \*\*ఫు $\\longleftrightarrow$ ము\*\* (\*వితీర్ణమునకు\*); \*\*బు $\\longleftrightarrow$ ము\*\* (\*వివేచనమునకు\*); \*\*భు $\\longleftrightarrow$ ము\*\* (\*నివాసములు\*)\[cite: 8\].

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.24.3, 6.24.5)

\* \*\*Category 1: ము-వర్ణకము (Nominative/Conjoined Suffix Forms 6.24.3):\*\*

  \* \*\*పు $\\longleftrightarrow$ ము:\*\* \*...జాహ్నవీపుత్రుఁడునుండఁగానహితమున్ భయమున్...\* (\*Bhāratam\*, Sabhā 2-133)\[cite: 8\]; \*పురుషునకిత్తెఱఁగు దెల్లముగ వినవలతున్...\* (\*Bhāgavatam\* 4-70)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ బూ:\*\* \*...దర్శనమును జేయుటఁబోలుఁగృష్ణుఁ బూజించుటిలన్...\* (\*Bhāratam\*, Sabhā 2-14)\[cite: 8\].

  \* \*\*బూ $\\longleftrightarrow$ ము:\*\* \*...సీతాపతిపైఁ బూనికనింతైన దోషముం గలదేనిన్...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 792)\[cite: 8\].

  \* \*\*బొ $\\longleftrightarrow$ ము:\*\* \*బొమముడుచుట నిర్వికారమును మును...\* (\*Bhāgavatam\* 7-87)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ బొ:\*\* \*...కామమునునదూష్యంబులై సిద్ధిఁబొందునధిప...\* (\*Bhāratam\*, Udyōga 1-108)\[cite: 8\].

  \* \*\*బో $\\longleftrightarrow$ ము:\*\* \*...పోయిరి సెప్పుమని తెల్లముగనడిగి...\* (\*Bhāratam\*, Āraṇya 3-245)\[cite: 8\].

  \* \*\*భూ $\\longleftrightarrow$ ము:\*\* \*భూసతీశ్వర దీన నీ కులమున్ మహీప్రజయున్...\* (\*Bhāratam\*, Sabhā 2-180, Mattakōkila)\[cite: 8\]; \*భూనుత యది నీకు దృష్టముగనెఱిఁగింతున్...\* (\*Bhāratam\*, Āraṇya 5-113)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ భూ:\*\* \*...ప్రతిగ్రహమునునను షట్కర్మములను భూసురవంశ్యుల్...\* (\*Bhāratam\*, Ādi 8-84)\[cite: 8\]; \*...మహిత లీలముగఁదాల్చి భవదనుభూతి సెల్లించే...\* (\*Bhāratam\*, Svargārohaṇa 58)\[cite: 8\].

\* \*\*Category 2: ముగాగమము (Inflected Augment Forms 6.24.5):\*\*

  \* \*\*పు $\\longleftrightarrow$ ము:\*\* \*పురము వెలి మూఁడహోరాత్రములు \[= రాత్ర \+ ము \+ లు\] వసించి...\* (\*Bhāratam\*, Sabhā 2-66)\[cite: 8\]; \*...పున పున మోవఁగవలయు సమయముం \[= సమయ \+ ము \+ ను\] గనికొని...\* (\*Bhāratam\*, Virāṭa 3-271)\[cite: 8\]; \*పురములు దుర్గముల్ శిబిరముల్ వెలిపేటలు...\* (\*Manu Caritra\* 4-60)\[cite: 8\]; \*పురుషునేఁగోర సమచిత్తమునకు రాదొ...\* (\*Manu Caritra\* 3-95)\[cite: 8\]; \*పుట్టనిసువు సత్కవిత్వములు వర్ణింతున్...\* (\*Manu Caritra\* 1-10)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ పు:\*\* \*...మన్వంతరమున వైవస్వతుఁడు పరమ పుణ్యుండు...\* (\*Bhāratam\*, Āraṇya 4-217)\[cite: 8\]; \*...విధిసంగ్రహమునకై పూజించిరధిక పుణ్యునధర్వున్...\* (\*Bhāratam\*, Āraṇya 5-173)\[cite: 8\]; \*...భవచ్ఛాసనమును గోరెడునానతిమ్ము పురమునకరుగన్...\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 1333)\[cite: 8\].

  \* \*\*పొ $\\longleftrightarrow$ ము:\*\* \*పొలుపుగ ధర్మార్థకామములు సమములుగాన్...\* (\*Bhāratam\*, Ādi 7-144)\[cite: 8\]; \*పొసఁగవు భీతమగు చిత్తమున భయముం బా...\* (\*Bhāratam\*, Sabhā 2-303)\[cite: 8\]; \*పొలమును గాని యట్టి క్రమముం దమ మెచ్చుగ...\* (\*Manu Caritra\* 1-6)\[cite: 8\].

  \* \*\*పో $\\longleftrightarrow$ ము:\*\* \*పోవదే వానరప్రకరముల్ వెసఁ దోడుగనేఁగి...\* (\*Bhāratam\*, Virāṭa 6-266)\[cite: 8\]; \*...తపోరతినున్నతఁడు బ్రహ్మముం బ్రాపించున్...\* (\*Bhāratam\*, Virāṭa 6-284)\[cite: 8\]; \*పోక నిల్చునుపాయములు మతించి...\* (\*Bhāgavatam\* 3-238)\[cite: 8\].

  \* \*\*బు $\\longleftrightarrow$ ము:\*\* \*బుద్ధి నిలిపి మీ యుపదేశమున శుభంబు...\* (\*Bhāratam\*, Sabhā 1-57)\[cite: 8\]; \*బుద్ధి సర్వైకసాక్షిత్వమున వెలుంగు...\* (\*Bhāgavatam\* 5-166)\[cite: 8\]; \*...పుట్టిన సదసద్వివేకములు గలిగినఁ దా...\* (\*Appakavīyamu\* 3-71 / \*Bhāratam\*, Ādi 5-58)\[cite: 8\]; \*...చక్రమునకుఁ బురుహూతతనూజబాణములకనిలోనె...\* (\*Bhāratam\*, Ādi 8-284)\[cite: 8\]; \*...కొనుచుఁ బురికిఁ జనుదెంచి యేకాంతమున హలాంకు...\* (\*Bhāratam\*, Udyōga 3-205)\[cite: 8\].

  \* \*\*బొ $\\longleftrightarrow$ ము:\*\* \*...శౌర్యసంపదం బొలుచు సహస్రబాహుకరముల్...\* (\*Bhāratam\*, Āraṇya 3-150)\[cite: 8\]; \*...బొంక నేరఁడు హాస్యమునకుఁ బలికి...\* (\*Bhāgavatam\* 1-95)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ బొ:\*\* \*...ప్రయోజనములకై లోఁబడుట గల్గుఁ బొలములనేనుంగులు...\* (\*Bhāratam\*, Virāṭa 3-229)\[cite: 8\]; \*...నీ కతముననా చిత్తము ప్రశాంతిఁ బొరసెఁ...\* (\*Bhāratam\*, Āraṇya 5-26)\[cite: 8\]; \*...తత్తఱమునఁగానక వెగడుపడుచుఁబొదల విరాళిన్...\* (\*Bhāgavatam\* 3-16)\[cite: 8\].

  \* \*\*బో $\\longleftrightarrow$ ము:\*\* \*బోరనఁ దానగ్నిసూక్తములతోనెసఁగెన్...\* (\*Lakṣaṇa Śirōmaṇi\* 4-337 / \*Bhāratam\*, Ādi 2-38)\[cite: 8\]; \*...వచ్చుచుఁ బోవుచునున్కిగని చిత్తములనొండుగ...\* (\*Bhāratam\*, Āraṇya 2-201)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ బో:\*\* \*...సాధనములునచటనె యుండఁ బోయె...\* (\*Bhāratam\*, Virāṭa 3-328)\[cite: 8\]; \*చింతాసాగరమున మునిఁగి భయంబు గదురఁ బోవుచునెదురన్...\* (\*Manu Caritra\* 2-18)\[cite: 8\].

  \* \*\*భు $\\longleftrightarrow$ ము:\*\* \*భువనంబులయందు సర్పములు ద్రిమ్మరుటన్...\* (\*Bhāratam\*, Ādi 2-116)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ భు:\*\* \*మునినాథ నీ యనుగ్రహమున నిగ్రహముడిగెనఖిలభువనంబులకీ...\* (\*Bhāratam\*, Sabhā 3-44)\[cite: 8\].

  \* \*\*భూ $\\longleftrightarrow$ ము:\*\* \*భూనుత ధాన్యంబు బీజములు వణిజులకున్...\* (\*Bhāratam\*, Sabhā 1-44)\[cite: 8\]; \*భూమియందర్హమగు తలమున వసించి...\* (\*Bhāratam\*, Udyōga 2-353)\[cite: 8\]; \*భూజన పరమహిత ధర్మముం దెలుపు దయన్...\* (\*Lakṣaṇa Śirōmaṇi\* 4-338 / \*Bhāratam\*, Virāṭa 4-3)\[cite: 8\]; \*భూసురోత్తమ గార్హస్థ్యమునకు సరియె...\* (\*Manu Caritra\* 1-66)\[cite: 8\].

  \* \*\*ము $\\longleftrightarrow$ భూ:\*\* \*జనపతులెవ్వరునివ్విధమున నిర్విఘ్నముగనఖిల భూజన...\* (\*Bhāratam\*, Ādi 6-87)\[cite: 8\]; \*...ముననాత్మనివాసమునకు భూవివరమునన్...\* (\*Bhāratam\*, Virāṭa 5-143)\[cite: 8\].

  \* \*\*భో $\\longleftrightarrow$ ము:\*\* \*భోజనావసానముననున్న యమ్ముని...\* (\*Bhāratam\*, Ādi 8-185)\[cite: 8\]; \*భోగిజనముల మృదుగాత్రములు ముకుంద...\* (\*Bhāratam\*, Sabhā 2-14)\[cite: 8\]; \*భోగాభోగసుఖదుఃఖములు లేవధిపా...\* (\*Bhāratam\*, Udyōga 5-594)\[cite: 8\].

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (Part 6 Summary)

&nbsp;

| Rule Type | Primary Target Coordinates | Grammatical / Phonetic Engine Conditions | Status in Engine |

| :--- | :--- | :--- | :--- |

| \*\*అభేదవర్గ యతులు (6.22)\*\*\[cite: 8\] | \*\*వ $\\longleftrightarrow$ {ప, ఫ, భ}\*\*\[cite: 8\] | Integrates with tripartite vowel grid ($A, I, U$ series)\[cite: 8\]. Valid for \*\*both\*\* inherent root 'వ' and mutated \*Gasadadavādeśa\* 'వ'\[cite: 8\]. Copyist variants rejected\[cite: 8\]. | \*\*Canonical\*\*\[cite: 8\] |

| \*\*అభేద యతి-2 (6.23)\*\*\[cite: 8\] | \*\*ల $\\longleftrightarrow$ ళ\*\*\[cite: 8\] | Vowel classes must align\[cite: 8\]. Valid across Sanskrit loan doublets (\*Tatsamas\*), native roots (\*Desyas\*), and plural mutated augments (\*Ādeśa Ḷa\*)\[cite: 8\]. | \*\*Canonical\*\*\[cite: 8\] |

| \*\*ము విభక్తి యతి / పోలిక వడి (6.24)\*\*\[cite: 8\] | \*\*ము $\\longleftrightarrow$ {పు, ఫు, బు, భు}\*\* & Class 3 Vowel Forms\[cite: 8\] | Target must be the nominal case suffix (\*Mu-varṇakamu\*) or inflected augment (\*Mugāgamamu\*)\[cite: 8\]. Consonants \*\*ప, ఫ, బ, భ\*\* must take Class 3 vowels (\*\*ఉ, ఊ, ఒ, ఓ\*\*)\[cite: 8\]. | \*\*Canonical\*\*\[cite: 8\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**6.26 సంయుక్త యతి (Saṁyukta Yati — Conjunct Consonant Caesura Architecture)**

* **Operational Definition:** *Saṁyukta Yati* is an operational parsing procedure (*yati vidhānamu*), not an independent phonetic class. A conjunct consonant (*saṁyuktākṣaramu* / *saṁyutākṣaramu*) consists of two or more consonants bound to a single terminal vowel ($\\text{C}\_1 \+ \\text{C}\_2 \+ \\dots \+ \\text{V}$).  
* **The Core Structural Axiom:** When executing Yati on a conjunct syllable, **the engine is legally satisfied if ANY SINGLE CONSONANT within the cluster matches the target coordinate in combination with the cluster's terminal vowel**. The poet is never required to match all consonants in the cluster.  
* **Nomenclature:** Designated **సంయుక్త విశ్రామము** (*Saṁyukta Viśrāmamu*) by Appakavi.  
* **Combinatorial Projection:**

$$\\text{Cluster: } \[\\text{C}\_1 \+ \\text{C}\_2 \+ \\text{V}\] \\implies \\begin{cases} \\text{Option 1:} & \[\\text{C}\_1 \+ \\text{V}\] \\text{ matches target coordinate} \\ \\text{Option 2:} & \[\\text{C}\_2 \+ \\text{V}\] \\text{ matches target coordinate} \\end{cases}$$

* *Example with 'శ్రీ' ($\\text{శ్} \+ \\text{ర్} \+ \\text{ఈ}$):*  
* Match via $\\text{C}\_1$: Scans as **శీ**, unlocking Sibilant (*Ūṣma*) or Palatal (*Sarasayati*) matches (e.g., matching **చె** via $\\mathbf{శీ \\longleftrightarrow చె}$).  
* Match via $\\text{C}\_2$: Scans as **రీ**, unlocking Liquid (*Ēkatara*) matches (e.g., matching **రి** via $\\mathbf{రీ \\longleftrightarrow రి}$).

               Saṁyuktākṣara Decomposition at Caesura

                       \[ Cluster: C₁ \+ C₂ \+ V \]

                                  │

         ┌────────────────────────┴────────────────────────┐

         ▼                                                 ▼

   Evaluate C₁ \+ V                                   Evaluate C₂ \+ V

(Bypasses C₂ entirely;                             (Bypasses C₁ entirely;

applies relevant Yati class)                      applies relevant Yati class)

         │                                                 │

  e.g., శ్ \+ ర్ \+ ఈ                                 e.g., శ్ \+ ర్ \+ ఈ

   \= శీ ⟷ చె (Sarasayati)                            \= రీ ⟷ రి (Ēkatara Yati)

\`\`\`\[cite: 9\]

&nbsp;

\* \*\*Structural Origins of Conjuncts (6.26.2):\*\*

  1\. \*శబ్దసిద్ధ సంయుక్తాక్షరములు (Inherent Lexical Roots):\* Natural lexical clusters (\*శ్రీ, వ్రత, స్తుత, న్యాయ\*)\[cite: 9\].

  2\. \*సంధిగత సంయుక్తాక్షరములు (Sandhi-Derived Consonant Clusters):\* Generated across word boundaries by consonant sandhi (\*హల్ సంధి\*, e.g., $\\text{త్రిజగత్} \+ \\text{విఖ్యాత} \= \\text{త్రిజగద్విఖ్యాత}$ \[\*\*ద్వి\*\*\]; $\\text{హృత్} \+ \\text{వన} \= \\text{హృద్వన}$ \[\*\*ద్వ\*\*\])\[cite: 9\].

  \* Both categories are parsed under the identical rule: any constituent consonant can be selected\[cite: 9\].

\* \*\*ద్విత్వాక్షర యతి (Geminate Consonant Scansion 6.26.3):\*\* A doubled/geminate consonant ($\\text{C}\_1 \+ \\text{C}\_1 \+ \\text{V}$) is structurally a conjunct of identical consonants\[cite: 9\]. The engine extracts that single consonant and pairs it under standard consonant classes (e.g., \*\*త్త \[త\] $\\longleftrightarrow$ థా\*\* under \*Vargaja\*; \*\*ట్టి \[టి\] $\\longleftrightarrow$ ఠీ\*\* under \*Vargaja\*)\[cite: 9\].

\* \*\*Disambiguation of Multi-Rule Layering (6.26.4):\*\* \*Saṁyukta Yati\* is the structural mechanism that extracts the active consonant; the actual phonetic rule applied (\*Prāṇi, Vargaja, Sarasayati, Ūṣma, Bindu\*, etc.) is determined by the extracted consonant's class\[cite: 9\].

&nbsp;

\---

&nbsp;

\*\*విశేష సంయుక్తాక్షరము: 'క్ష'కార యతి పరిధి (The 'Kṣa' Permutation Matrix 6.26.5)\*\*

&nbsp;

The compound character \*\*'క్ష'\*\* is a conjunct of velar \*\*'క్'\*\* and retroflex sibilant \*\*'ష్'\*\* ($\\text{క్} \+ \\text{ష్} \+ \\text{V}$)\[cite: 9\]. Because it bridges two completely different phonetic categories, it possesses the widest alliterative range of any consonant in Telugu prosody\[cite: 9\]:

&nbsp;

&nbsp;

                   The 'Kṣa' (క్ష) Alliteration Matrix

                             \[ క్ \+ ష్ \+ V \]

                                    │

    ┌───────────────────────────────┴───────────────────────────────┐

    ▼                                                               ▼

&nbsp;

Path A: Extract 'క్' (Ka)                                       Path B: Extract 'ష్' (Ṣa) │                                                               │

1. Prāṇi Yati: { క }                                            1\. Prāṇi Yati: { ష }  
2. Vargaja Yati: { ఖ, గ, ఘ }                                    2\. Ūṣma Yati: { శ, స }  
3. Sarasayati-4: { చ, ౘ, ఛ, జ, ౙ, ఝ }

&nbsp;

\* \*\*Corpus Provenance for 'క్ష':\*\*

  \* \*Via 'క్' (Prāṇi & Vargaja):\*

    \* \*\*క్ష \[క\] $\\longleftrightarrow$ కా:\*\* \*...బంధమక్షతమయి తూల సంచయ నికాశతనొప్పెననంత...\* (\*Bhāratam\*, Ādi 7-121)\[cite: 9\].

    \* \*\*క్ష \[క\] $\\longleftrightarrow$ గా:\*\* \*క్షత్రియవంశ్యులై ధరణిఁ గావఁగఁ బుట్టినవారు...\* (\*Bhāratam\*, Ādi 2-175)\[cite: 9\].

    \* \*\*క్ష \[క\] $\\longleftrightarrow$ గ:\*\* \*...రావముంగలసెం దచ్చతురర్ణవీరవ సపక్షధ్వానమవ్వీటిలో...\* (\*Bhāgavatam\* 10-Pūrvabhāga 49)\[cite: 9\].

    \* \*\*ర్ఘా \[ఘా\] $\\longleftrightarrow$ క్ష \[క\]:\*\* \*...దీర్ఘనిర్ఘాతక్రూర కుఠార లూన నిఖిలక్షత్రోరుకాంతారుఁడై...\* (\*Bhāratam\*, Ādi 1-78)\[cite: 9\].

    \* \*\*క్షా \[కా\] $\\longleftrightarrow$ ఖా:\*\* \*...లోకరక్షామణి సర్వదైవత శిఖామణి...\* (\*Bhāratam\*, Sabhā 1-16)\[cite: 9\].

    \* \*\*క్షి \[కి\] $\\longleftrightarrow$ కృ:\*\* \*క్షితిదత్తాత్రేయు దయకకృత్యము గలదే...\* (\*Śivarātri Māhātmyamu\* 5-202)\[cite: 9\].

    \* \*\*గృ $\\longleftrightarrow$ క్షిం \[కి\]:\*\* \*...లోఁగొని యాత్మఁగృపపుట్టి మిగులరక్షించెఁ గాన...\* (\*Haravilāsam\* 2-12)\[cite: 9\].

    \* \*\*క్షే \[కే\] $\\longleftrightarrow$ కీ:\*\* \*క్షేమద కరవాల సుజనకీర్తిత గుణలో...\* (\*Bhāratam\*, Virāṭa 2-1)\[cite: 9\].

    \* \*\*క్షు \[కు\] $\\longleftrightarrow$ కో:\*\* \*క్షుధార్తి వివృతాస్యపదవి కోఱ యలుగదే...\* (\*Bhāgavatam\* 5-281)\[cite: 9\].

    \* \*\*గో $\\longleftrightarrow$ క్షో \[కో\]:\*\* \*గోపురాంగణస్థిత జనక్షోభమెసఁగ...\* (\*Amuktamālyada\* 7-19)\[cite: 9\].

    \* \*\*ఖ $\\longleftrightarrow$ క్ష \[క\]:\*\* \*...హేమపుంఖ రుచిస్ఫార మరాళరాజ సితపక్ష...\* (\*Bhāratam\*, Bhīṣma 4-350)\[cite: 9\].

  \* \*Via 'ష్' (Prāṇi, Ūṣma, & Sarasayati):\*

    \* \*\*చ్ఛ \[చ\] $\\longleftrightarrow$ క్ష \[ష\]:\*\* \*...పతచ్ఛర సాహస్రములోలి భీషణ విపక్షశ్రేణిపై...\* (\*Bhāratam\*, Bhīṣma 4-350)\[cite: 9\].

    \* \*\*ష $\\longleftrightarrow$ క్ష \[ష\]:\*\* \*...భూషణ రత్నప్రభతోన పర్వుచు సితాక్షద్యోతులందంద...\* (\*Bhāratam\*, Udyōga 5-67)\[cite: 9\].

    \* \*\*క్ష \[ష\] $\\longleftrightarrow$ స:\*\* \*...తద్వక్షమునందొక హారమిడి యసదృశ ప్రీతిన్...\* (\*Bhāgavatam\* 7-155)\[cite: 9\].

    \* \*\*క్ష \[ష\] $\\longleftrightarrow$ శా:\*\* \*క్షంతకుఁ గాళియోరగ విశాలఫణోపరినర్తనక్రియా...\* (\*Bhāgavatam\* 1-29)\[cite: 9\].

    \* \*\*క్ష \[ష\] $\\longleftrightarrow$ జె:\*\* \*క్షమయ తాల్చియుండఁ జేనదెల్ల ప్రొద్దుఁదే...\* (\*Bhāratam\*, Ādi 1-217)\[cite: 9\].

    \* \*\*క్ష \[ష\] $\\longleftrightarrow$ ఝ:\*\* \*...శరణాగతరక్షణ కంకణకింకిణీక ఝంకృతులారన్...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 80)\[cite: 9\].

    \* \*\*క్షా \[షా\] $\\longleftrightarrow$ శ:\*\* \*...రక్షాముద్రల్దనరారు జక్రధరు శ్రీశయ్యానివాసంబునన్...\* (\*Vasu Caritra\* 1-58)\[cite: 9\].

    \* \*\*క్షా \[షా\] $\\longleftrightarrow$ జ:\*\* \*...రక్షాసక్తుఁడు మనుమసిద్ధి జగతీశుఁడొగిన్...\* (\*Manu Caritra\* 10-1)\[cite: 9\].

    \* \*\*క్షే \[షే\] $\\longleftrightarrow$ చె:\*\* \*మారుతక్షేప విభగ్నమూలమయి చెచ్చెరఁ ద్రెళ్ళు...\* (\*Bhāratam\*, Udyōga 6-190)\[cite: 9\].

    \* \*\*స్థు \[షు\] $\\longleftrightarrow$ క్షో \[షో\]:\*\* \*...సురతరదీర్ఘనిష్ఠుర భల్లప్రవిసార దారుణతరక్షోణీశులం...\* (\*Bhāratam\*, Ādi 1-167)\[cite: 9\].

&nbsp;

\---

&nbsp;

\*\*ఉభయ సంయుక్తాక్షర యతి (Dual Conjunct Matching 6.26.6)\*\*

&nbsp;

When both the initial coordinate (\*vali\*) and the caesura coordinate (\*yati-sthāna\*) are conjunct consonants, the engine tests all combinatorial pairings between the two clusters\[cite: 9\]. A match between \*\*any one consonant of Cluster 1 and any one consonant of Cluster 2\*\* validates the line\[cite: 9\]:

&nbsp;

$$\\text{Cluster}\_1\\ (\\text{C}\_{1\\text{A}} \+ \\text{C}\_{1\\text{B}} \+ \\text{V}\_1) \\quad\\longleftrightarrow\\quad \\text{Cluster}\_2\\ (\\text{C}\_{2\\text{A}} \+ \\text{C}\_{2\\text{B}} \+ \\text{V}\_2)$$\[cite: 9\]

&nbsp;

1\. \*\*$\\text{C}\_1$ of Cluster 1 with $\\text{C}\_1$ of Cluster 2:\*\*

   \* \*\*క్ష \[క\] $\\longleftrightarrow$ ఖ్యా \[ఖ\]:\*\* \*క్షత్రియప్రవరుండ విఖ్యాతబలుఁడ...\* (\*Bhāratam\*, Āraṇya 3-323)\[cite: 9\].

   \* \*\*క్య \[క\] $\\longleftrightarrow$ ఘ్రం \[ఘ\]:\*\* \*...శక్యముగాదు నీవ శీఘ్రంబ చెఱుప...\* (\*Bhāratam\*, Udyōga 1-273)\[cite: 9\].

   \* \*\*ర్చ \[ర\] $\\longleftrightarrow$ ర్గ \[ర\]:\*\* \*...పూర్వకార్చనలర్థిందగనిచ్చి... మార్గక్షేమ...\* (\*Manu Caritra\* 7-144)\[cite: 9\].

2\. \*\*$\\text{C}\_1$ of Cluster 1 with $\\text{C}\_2$ of Cluster 2:\*\*

   \* \*\*ర్బీ \[రీ\] $\\longleftrightarrow$ శ్రీ \[రీ\]:\*\* \*...దుర్బీజశ్రేష్ఠులుగాఁగతంబు కలదే శ్రీకాళహస్తీశ్వరా...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 9\].

3\. \*\*$\\text{C}\_2$ of Cluster 1 with $\\text{C}\_1$ of Cluster 2:\*\*

   \* \*\*ష్టి \[టి\] $\\longleftrightarrow$ డ్కిం \[డి\]:\*\* \*...దృష్టియుతుండై నగుచున్ జనార్దనుని మాడ్కిం...\* (\*Bhāgavatam\* 10-Pūrvabhāga 194)\[cite: 9\].

   \* \*\*ట్త \[త\] $\\longleftrightarrow$ ద్రా \[దా\]:\*\* \*...వార్ధిరాట్తరుణీరత్నము వింటివే యసురచంద్రాయన్న...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 198)\[cite: 9\].

4\. \*\*$\\text{C}\_2$ of Cluster 1 with $\\text{C}\_2$ of Cluster 2:\*\*

   \* \*\*క్రీ \[రీ\] $\\longleftrightarrow$ శ్రీ \[రీ\]:\*\* \*క్రీడాసక్తులనేమి చెప్పవలెనో శ్రీకాళహస్తీశ్వరా...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 9\].

5\. \*\*Geminate matching a Conjunct (ద్విత్వ \- సంయుక్త):\*\*

   \* \*\*త్త \[త\] $\\longleftrightarrow$ ద్వై \[దై\]:\*\* \*...కృష్ణార్జునోత్తమ నానాగుణకీర్తనార్థఫలమై ద్వైపాయనోద్యాన...\* (\*Bhāratam\*, Ādi 1-66)\[cite: 9\].

   \* \*\*ట్టి \[టి\] $\\longleftrightarrow$ డ్కిం \[డి\]:\*\* \*...బెట్టిదమై మ్రోయుచు వచ్చి బల్బిడుగు మాడ్కిం దాఁకుడున్...\* (\*Bhāratam\*, Virāṭa 5-4-150)\[cite: 9\].

   \* \*\*సృ \[తృ\] $\\longleftrightarrow$ ద్దీ \[దీ\]:\*\* \*...విస్తృత సంధ్యాంబుద ధాతు చిత్రిత సముద్దీప్తక్షమాభృద్గతిన్...\* (\*Bhāgavatam\* 3-419)\[cite: 9\].

&nbsp;

\---

&nbsp;

\*\*త్రిహల్లు సంయుక్తాక్షర యతి (Three-Consonant Clusters 6.26.7)\*\*

&nbsp;

When a cluster contains three consonants ($\\text{C}\_1 \+ \\text{C}\_2 \+ \\text{C}\_3 \+ \\text{V}$), the engine retains full multi-path resolution across all three elements\[cite: 9\].

\* \*\*Appakavi's Definitive Stanza (\*Appakavīyamu\* 3-109):\*\*

  Using the base \*\*'క్ష్మా'\*\* ($\\text{క్} \+ \\text{ష్} \+ \\text{మ్} \+ \\text{ఆ}$):

  \* Line 1 matches $\\text{C}\_1$ (\*\*కా $\\longleftrightarrow$ గా\*\* via \*Vargaja\*): \*క్ష్మాధరంబాతపత్రంబుగా ధరించే...\*\[cite: 9\]

  \* Line 2 matches $\\text{C}\_2$ (\*\*షా $\\longleftrightarrow$ స\*\* via \*Ūṣma\*): \*క్ష్మాకుమారుని బోరను సంహరించె...\*\[cite: 9\]

  \* Line 3 matches $\\text{C}\_3$ (\*\*మా $\\longleftrightarrow$ ంప\*\* via \*Bindu\*): \*క్ష్మారుహంబునకై నిలింపపతినొంచెఁ...\*\[cite: 9\]

\* \*\*Extended Tri-Consonant Corpus:\*\*

  \* \*\*క్ష్మా \[షా\] $\\longleftrightarrow$ స:\*\* \*క్ష్మారమణకృపావిశేష సమధిగతైశ్వర్యా...\* (\*Kāśīkhaṇḍam\* 7-1)\[cite: 9\].

  \* \*\*జ $\\longleftrightarrow$ క్ష్మా \[షా\]:\*\* \*జవనాక్షీణబలంబుఁ గంటిమొ వసుక్ష్మామండలాఖండలా...\* (\*Manu Caritra\* 3-6)\[cite: 9\].

  \* \*\*క్ష్మా \[మా\] $\\longleftrightarrow$ మ:\*\* \*క్ష్మానాథుని పుత్రకుఁడసమంజుఁడు...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 390)\[cite: 9\].

  \* \*\*క్ష్మీ \[కీ\] $\\longleftrightarrow$ కి:\*\* \*...లక్ష్మీవిభు మీఁది మచ్చరము కిన్కయుఁ...\* (\*Bhāratam\*, Sabhā 1-89)\[cite: 9\].

  \* \*\*ఖ $\\longleftrightarrow$ క్ష line 6:\*\* \*ఖనటత్పయోబ్ధివీక్ష్యరసాతలాన్యోన్య...\* (\*\*ఖ $\\longleftrightarrow$ క్ష \[క\]\*\*) (\*Bhāgavatam\* 1-3)\[cite: 9\].

  \* \*\*జ్జ్వా \[జా\] $\\longleftrightarrow$ సం:\*\* \*...శశ్వజ్జ్వాలామాలా కరాళ సందీప్తంబై...\* (\*Bhāratam\*, Ādi 4-156)\[cite: 9\].

  \* \*\*ష్ట్రు \[టు\] $\\longleftrightarrow$ టు:\*\* \*...ధార్తరాష్ట్రులు ద్రిజగంబులుం గొని పటుస్ఫురణం...\* (\*Bhāratam\*, Udyōga 5-1-121)\[cite: 9\].

  \* \*\*త్త్వ \[త\] $\\longleftrightarrow$ దా:\*\* \*...ధర్మతత్త్వమ్ములు పాండవేయులును దానును గాని...\* (\*Bhāratam\*, Sabhā 2-2-39)\[cite: 9\].

  \* \*\*ర్త్యు \[తు\] $\\longleftrightarrow$ దూ:\*\* \*...మర్త్యులకవిషయమాతపంబు దూఱదు దీనన్...\* (\*Bhāratam\*, Āraṇya 2-107)\[cite: 9\].

  \* \*\*ర్బ \[బ\] $\\longleftrightarrow$ త్ప్ర \[ప\]:\*\* \*...దోర్బల సంపత్తియు నాకుఁబోలెఁ ద్రిజగత్ప్రఖ్యాతి...\* (\*Bhāratam\*, Virāṭa 5-10)\[cite: 9\].

  \* \*\*ద్రా \[రా\] $\\longleftrightarrow$ రా:\*\* \*...సరిద్గ్రావ మహాటవుల్గడచి రాజత శైలముఁ...\* (\*Bhāratam\*, Virāṭa 4-43)\[cite: 9\].

  \* \*\*క్ష్వా \[వా\] $\\longleftrightarrow$ వం:\*\* \*...ధర్మశీలుఁడిక్ష్వాకు కులోద్భవుండు బలవంతుఁడనంత...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 200)\[cite: 9\].

  \* \*\*ర్వ్య \[వ\] $\\longleftrightarrow$ వ:\*\* \*అవిలంఘనీయ మీదుర్వ్యవసాయంబనుచు...\* (\*Bhāratam\*, Sabhā 2-154)\[cite: 9\].

  \* \*\*క్ష్మీ \[షీ\] $\\longleftrightarrow$ శ్రీ \[శీ\]:\*\* \*...జ్ఞానలక్ష్మీజాగ్రత్పరిణామమిమ్ము దయతో శ్రీకాళహస్తీశ్వరా...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 9\].

&nbsp;

\---

&nbsp;

\*\*6.27 సంయుక్త యతి \- సమగ్ర హల్లు యతులు (Saṁyukta Yati Corpus Demonstrations across 16 Classes)\*\*

&nbsp;

1\. \*\*ప్రాణియతులు (6.27.1):\*\* \*\*కా $\\longleftrightarrow$ ష్క \[క\]\*\* (\*Bhāratam\*, Ādi 2-33)\[cite: 9\]; \*\*ర్గ \[గ\] $\\longleftrightarrow$ గాం\*\* (\*Bhāratam\*, Ādi 1-144)\[cite: 9\]; \*\*ర్థ \[ధ\] $\\longleftrightarrow$ ధ\*\* (\*Bhāratam\*, Ādi 1-123)\[cite: 9\]; \*\*ప $\\longleftrightarrow$ త్పా \[పా\]\*\* (\*Bhāratam\*, Ādi 2-91)\[cite: 9\]; \*\*ర్భ \[భ\] $\\longleftrightarrow$ భా\*\* (\*Bhāratam\*, Ādi 2-127)\[cite: 9\]; \*\*య్యు \[యు\] $\\longleftrightarrow$ యు\*\* (\*Bhāratam\*, Ādi 4-265)\[cite: 9\]; \*\*ఱ్ఱు \[ఱు\] $\\longleftrightarrow$ ఱు\*\* (\*Bhāratam\*, Ādi 4-271)\[cite: 9\]; \*\*వు $\\longleftrightarrow$ వ్వు \[వు\]\*\* (\*Amuktamālyada\* 5-1-65)\[cite: 9\]; \*\*త్సు \[సు\] $\\longleftrightarrow$ సూ\*\* (\*Bhāratam\*, Ādi 4-94)\[cite: 9\].

2\. \*\*వర్గజ యతులు (6.27.2):\*\* \*\*త్క \[క\] $\\longleftrightarrow$ గా\*\* (\*Bhāratam\*, Ādi 2-112)\[cite: 9\]; \*\*చ $\\longleftrightarrow$ జ్ఞా \[జా\]\*\* (\*Bhāratam\*, Udyōga 9-106)\[cite: 9\]; \*\*ఛ $\\longleftrightarrow$ జ్ఞ \[జ\]\*\* (\*Bhāratam\*, Udyōga 9-443)\[cite: 9\]; \*\*జ్వా \[జా\] $\\longleftrightarrow$ చా\*\* (\*Bhāratam\*, Āraṇya 2-127)\[cite: 9\]; \*\*చి $\\longleftrightarrow$ జ్జెం \[జె\]\*\* (\*Amuktamālyada\* 5-6-251)\[cite: 9\]; \*\*చ్యు \[చు\] $\\longleftrightarrow$ చో\*\* (\*Bhāratam\*, Ādi 4-127)\[cite: 9\]; \*\*ష్ఠా \[ఠా\] $\\longleftrightarrow$ ఢ\*\* (\*Bhāratam\*, Ādi 1-157)\[cite: 9\]; \*\*ష్ఠు \[ఠు\] $\\longleftrightarrow$ డొ\*\* (\*Bhāratam\*, Ādi 1-152)\[cite: 9\]; \*\*స్థా \[థా\] $\\longleftrightarrow$ తం\*\* (\*Bhāratam\*, Ādi 2-113)\[cite: 9\]; \*\*ధ $\\longleftrightarrow$ ర్థం \[థ\]\*\* (\*Bhāratam\*, Udyōga 6-112)\[cite: 9\]; \*\*ద్ర \[ద\] $\\longleftrightarrow$ ధీ\*\* (\*Bhāratam\*, Ādi 1-125)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ బొం\*\* (\*Bhāratam\*, Ādi 2-46)\[cite: 9\]; \*\*బ్ర \[బ\] $\\longleftrightarrow$ భ\*\* (\*Bhāratam\*, Ādi 1-140)\[cite: 9\].

3\. \*\*బిందుయతులు (6.27.3):\*\* \*\*ంథ $\\longleftrightarrow$ న్నా \[నా\]\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 335)\[cite: 9\]; \*\*న్ను \[ను\] $\\longleftrightarrow$ ంథు\*\* (\*Amuktamālyada\* 5-4-40)\[cite: 9\]; \*\*ంద్రా \[ందా\] $\\longleftrightarrow$ న\*\* (\*Manu Caritra\* 6-1)\[cite: 9\]; \*\*ంప్రీ \[ంపీ\] $\\longleftrightarrow$ మీ\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1282)\[cite: 9\]; \*\*ంబం \[ంబ\] $\\longleftrightarrow$ మ్రా \[మా\]\*\* (\*Manu Caritra\* 6-99)\[cite: 9\].

4\. \*\*'న-ణ' సరసయతి (6.27.4):\*\* \*\*ర్ణ \[ణ\] $\\longleftrightarrow$ నం\*\* (\*Bhāratam\*, Ādi 6-237)\[cite: 9\]; \*\*ణ $\\longleftrightarrow$ న్న \[న\]\*\* (\*Bhāratam\*, Virāṭa 2-67)\[cite: 9\]; \*\*న $\\longleftrightarrow$ ణ్య \[ణ\]\*\* (\*Manu Caritra\* 2-59)\[cite: 9\].

5\. \*\*అనునాసికాక్షర యతి (6.27.5):\*\* \*\*ంఠ $\\longleftrightarrow$ త్న \[న\]\*\* (\*Amuktamālyada\* 5-6-118)\[cite: 9\]; \*\*ండ $\\longleftrightarrow$ న్మ \[న\]\*\* (\*Manu Caritra\* 1-5)\[cite: 9\]; \*\*న్న \[న\] $\\longleftrightarrow$ ండ\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 332)\[cite: 9\]; \*\*నీ $\\longleftrightarrow$ ండ్రీ \[ండీ\]\*\* (\*Cāṭu\*)\[cite: 9\]; \*\*ంతు $\\longleftrightarrow$ ర్ణో \[ణో\]\*\* (\*Manu Caritra\* 3-120)\[cite: 9\]; \*\*ంద $\\longleftrightarrow$ ర్ణ \[ణ\]\*\* (\*Vidyāvatīvilāsam\* 3-100)\[cite: 9\]; \*\*ంద్ర \[ంద\] $\\longleftrightarrow$ ణం\*\* (\*Ghaṭikācalamu\* 1-10)\[cite: 9\]; \*\*ంద్రు \[ందు\] $\\longleftrightarrow$ ణు\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 1973)\[cite: 9\].

6\. \*\*అనుస్వార సంబంధ యతి (6.27.6):\*\* \*\*ండ $\\longleftrightarrow$ ంద్ర \[ంద\]\*\* (\*Amuktamālyada\* 3-68)\[cite: 9\]; \*\*ండు $\\longleftrightarrow$ ంద్రు \[ందు\]\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Kiṣkindha 426)\[cite: 9\].

7\. \*\*ఋజు యతి (6.27.7):\*\* \*\*య $\\longleftrightarrow$ హ్మ \[హ\]\*\* (\*Bhāratam\*, Udyōga 5-347)\[cite: 9\]; \*\*హ $\\longleftrightarrow$ య్య \[య\]\*\* (\*Bhāratam\*, Ādi 8-128)\[cite: 9\]; \*\*హ $\\longleftrightarrow$ ర్య \[య\]\*\* (\*Bhāratam\*, Virāṭa 5-363)\[cite: 9\]; \*\*హ $\\longleftrightarrow$ ధ్యా \[యా\]\*\* (\*Kāśīkhaṇḍam\* 4-143)\[cite: 9\].

8\. \*\*'అ-య' సరసయతి (6.27.8):\*\* \*\*అ $\\longleftrightarrow$ ద్య \[య\]\*\* (\*Bhāratam\*, Sabhā 1-117)\[cite: 9\]; \*\*అం $\\longleftrightarrow$ ర్యం \[యం\]\*\* (\*Bhāgavatam\* 7-282)\[cite: 9\]; \*\*అ $\\longleftrightarrow$ వ్య \[య\]\*\* (\*Manu Caritra\* 1-77)\[cite: 9\]; \*\*అ $\\longleftrightarrow$ ర్జ్యా \[యా\]\*\* (\*Manu Caritra\* 2-38)\[cite: 9\]; \*\*ఆ $\\longleftrightarrow$ వ్యా \[యా\]\*\* (\*Bhāratam\*, Ādi 5-106)\[cite: 9\]; \*\*ర్య \[య\] $\\longleftrightarrow$ అ\*\* in \*హుతాశన\* (\*Bhāratam\*, Ādi 4-224)\[cite: 9\]; \*\*ఖ్యా \[యా\] $\\longleftrightarrow$ అ\*\* in \*తదర్థ\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 418)\[cite: 9\]; \*\*వ్యో \[యో\] $\\longleftrightarrow$ ఓ\*\* in \*దివ్యౌషధీ\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 3328)\[cite: 9\].

9\. \*\*'అ-హ' సరసయతి (6.27.9):\*\* \*\*హ్ర \[హ\] $\\longleftrightarrow$ అ\*\* in \*అమ్ముని\* (\*Bhāratam\*, Āraṇya 3-86)\[cite: 9\]; \*\*ఇం $\\longleftrightarrow$ హ్నీ \[హీ\]\*\* (\*Kāśīkhaṇḍam\* 2-182)\[cite: 9\].

10\. \*\*ఊష్మ యతులు (6.27.10):\*\* \*\*శ $\\longleftrightarrow$ ష్య \[ష\]\*\* (\*Bhāratam\*, Ādi 1-87)\[cite: 9\]; \*\*ష $\\longleftrightarrow$ శ్లా \[శా\]\*\* (\*Amuktamālyada\* 3-209)\[cite: 9\]; \*\*క్ష \[ష\] $\\longleftrightarrow$ శౌ\*\* (\*Bhāratam\*, Sabhā 2-122)\[cite: 9\]; \*\*శ్రీ \[శీ\] $\\longleftrightarrow$ షే\*\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 157)\[cite: 9\]; \*\*శృ $\\longleftrightarrow$ క్ష్మి \[షి\]\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 13)\[cite: 9\]; \*\*క్ష్మీ \[షీ\] $\\longleftrightarrow$ శ్రీ \[శీ\]\*\* (\*Bhāratam\*, Sabhā 5-155)\[cite: 9\]; \*\*క్షో \[షో\] $\\longleftrightarrow$ శో\*\* (\*Bhāratam\*, Sabhā 5-140)\[cite: 9\]; \*\*శ్వ \[శ\] $\\longleftrightarrow$ స\*\* (\*Bhāratam\*, Ādi 8-167)\[cite: 9\]; \*\*శ $\\longleftrightarrow$ త్స్వా \[సా\]\*\* (\*Bhāratam\*, Ādi 5-4)\[cite: 9\]; \*\*శ్వ \[శ\] $\\longleftrightarrow$ సౌ\*\* (\*Bhāratam\*, Ādi 1-399)\[cite: 9\]; \*\*శై $\\longleftrightarrow$ త్సా \[సా\]\*\* (\*Bhāratam\*, Virāṭa 4-75)\[cite: 9\]; \*\*స్వా \[సా\] $\\longleftrightarrow$ శౌ\*\* (\*Śivarātri Māhātmyamu\* 2-128)\[cite: 9\]; \*\*స్థి \[సి\] $\\longleftrightarrow$ శే\*\* (\*Bhāratam\*, Ādi 2-10)\[cite: 9\]; \*\*శ్లో \[శో\] $\\longleftrightarrow$ సూ\*\* (\*Nalacaritra\* 1-5)\[cite: 9\]; \*\*క్ష్య \[ష\] $\\longleftrightarrow$ స\*\* (\*Manu Caritra\* 9-102)\[cite: 9\]; \*\*ష్ప \[ష\] $\\longleftrightarrow$ సౌ\*\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 250)\[cite: 9\]; \*\*ష్కా \[షా\] $\\longleftrightarrow$ సం\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1018)\[cite: 9\]; \*\*క్షి \[షి\] $\\longleftrightarrow$ సి\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 309)\[cite: 9\]; \*\*ష్టి \[షి\] $\\longleftrightarrow$ స్పీ \[సీ\]\*\* (\*Manu Caritra\* 5-398)\[cite: 9\]; \*\*ష్టి \[షి\] $\\longleftrightarrow$ సె\*\* (\*Śivarātri Māhātmyamu\* 1-54)\[cite: 9\]; \*\*త్సే \[సే\] $\\longleftrightarrow$ క్షి \[షి\]\*\* (\*Bhāratam\*, Āraṇya 5-233)\[cite: 9\]; \*\*క్షీ \[షీ\] $\\longleftrightarrow$ సి\*\* (\*Bhāgavatam\* 5-163)\[cite: 9\]; \*\*సిం $\\longleftrightarrow$ ష్కీ \[షీ\]\*\* (\*Bhāgavatam\* 10-Pūrvabhāga 392)\[cite: 9\]; \*\*ష్ము \[షు\] $\\longleftrightarrow$ సు\*\* (\*Bhāratam\*, Virāṭa 3-168)\[cite: 9\]; \*\*ష్ణు \[షు\] $\\longleftrightarrow$ సూ\*\* (\*Bhāratam\*, Udyōga 2-372)\[cite: 9\]; \*\*ష్ఠు \[షు\] $\\longleftrightarrow$ సా\*\* (\*Bhāratam\*, Virāṭa 3-401)\[cite: 9\]; \*\*ష్ణు \[షు\] $\\longleftrightarrow$ స్తో \[సో\]\*\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 2086)\[cite: 9\].

11\. \*\*సరసయతి-4 (Sibilants with Palatals 6.27.11):\*\* \*\*శ్న \[శ\] $\\longleftrightarrow$ చా\*\* (\*Bhāratam\*, Sabhā 2-235)\[cite: 9\]; \*\*ర్చ \[చ\] $\\longleftrightarrow$ శా\*\* (\*Bhāratam\*, Ādi 5-34)\[cite: 9\]; \*\*చ్చె \[చె\] $\\longleftrightarrow$ శీ\*\* (\*Bhāratam\*, Ādi 5-83)\[cite: 9\]; \*\*శ్రీ \[శీ\] $\\longleftrightarrow$ చిం\*\* (\*Bhāgavatam\* 1-1)\[cite: 9\]; \*\*చ్యు \[చు\] $\\longleftrightarrow$ శో\*\* (\*Bhāratam\*, Ādi 3-118)\[cite: 9\]; \*\*శ్ర \[శ\] $\\longleftrightarrow$ చే\*\* (\*Bhāratam\*, Ādi 8-10)\[cite: 9\]; \*\*శ్రు \[శు\] $\\longleftrightarrow$ చో\*\* (\*Vasu Caritra\* 1-46)\[cite: 9\]; \*\*జ్వ \[జ\] $\\longleftrightarrow$ శ\*\* (\*Bhāratam\*, Ādi 2-97)\[cite: 9\]; \*\*ర్జ \[జ\] $\\longleftrightarrow$ స\*\* (\*Bhāratam\*, Ādi 5-204)\[cite: 9\]; \*\*శ $\\longleftrightarrow$ జే\*\* (\*Bhāratam\*, Sabhā 1-85)\[cite: 9\]; \*\*ర్జు \[జు\] $\\longleftrightarrow$ శో\*\* (\*Bhāratam\*, Ādi 1-50)\[cite: 9\]; \*\*ర్జ \[ఝ\] $\\longleftrightarrow$ శై\*\* (\*Haravilāsam\* 4-50)\[cite: 9\]; \*\*ఝ $\\longleftrightarrow$ శ్చ \[శ\]\*\* (\*Raṅganātha Rāmāyaṇamu\*, Araṇya 118)\[cite: 9\]; \*\*ర్ష \[ష\] $\\longleftrightarrow$ చ\*\* (\*Bhāratam\*, Āraṇya 4-313)\[cite: 9\]; \*\*చ $\\longleftrightarrow$ ష్ట \[ష\]\*\* (\*Amuktamālyada\* 4-207)\[cite: 9\]; \*\*చి $\\longleftrightarrow$ క్ష్వే \[షే\]\*\* (\*Manu Caritra\* 5-18)\[cite: 9\]; \*\*క్షే \[షే\] $\\longleftrightarrow$ చె\*\* (\*Bhāratam\*, Udyōga 6-190)\[cite: 9\]; \*\*ష్ఠ \[ష\] $\\longleftrightarrow$ చే\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Sundara 859)\[cite: 9\]; \*\*క్ష \[ష\] $\\longleftrightarrow$ చా\*\* (\*Bhāratam\*, Virāṭa 1-12)\[cite: 9\]; \*\*ష్ట్ర \[ష\] $\\longleftrightarrow$ చా\*\* (\*Bhāratam\*, Sabhā 1-134)\[cite: 9\]; \*\*ష్ఠు \[షు\] $\\longleftrightarrow$ చో\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 52)\[cite: 9\]; \*\*చో $\\longleftrightarrow$ ష్ఠు \[షు\]\*\* (\*Bhāratam\*, Ādi 2-39)\[cite: 9\]; \*\*ష్ప \[ష\] $\\longleftrightarrow$ ర్భ \[ఛ\]\*\* (\*Bhāratam\*, Virāṭa 7-407)\[cite: 9\]; \*\*క్షి \[షి\] $\\longleftrightarrow$ ఛీ\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1878)\[cite: 9\]; \*\*జ $\\longleftrightarrow$ ష్య \[ష\]\*\* (\*Bhāratam\*, Ādi 3-233)\[cite: 9\]; \*\*జె $\\longleftrightarrow$ క్షే \[షే\]\*\* (\*Śivarātri Māhātmyamu\* 1-5)\[cite: 9\]; \*\*ష్టి \[షి\] $\\longleftrightarrow$ జే\*\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 103)\[cite: 9\]; \*\*ష్ఠీ \[షీ\] $\\longleftrightarrow$ జే\*\* (\*Bhāratam\*, Virāṭa 2-120)\[cite: 9\]; \*\*ష్ఠు \[షు\] $\\longleftrightarrow$ జు\*\* (\*Rāghavapāṇḍavīyamu\* 2024)\[cite: 9\]; \*\*ష్యు \[షు\] $\\longleftrightarrow$ జూ\*\* (\*Manu Caritra\* 2-33)\[cite: 9\]; \*\*ర్థ \[ఝ\] $\\longleftrightarrow$ ష\*\* (\*Manu Caritra\* 1-108)\[cite: 9\]; \*\*సృ $\\longleftrightarrow$ చ్చి \[చి\]\*\* (\*Bhāratam\*, Udyōga 3-377)\[cite: 9\]; \*\*సో $\\longleftrightarrow$ చ్చు \[చు\]\*\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 103)\[cite: 9\]; \*\*సూ $\\longleftrightarrow$ చ్చో \[చో\]\*\* (\*Amuktamālyada\* 3-69)\[cite: 9\]; \*\*ర్జ \[జ\] $\\longleftrightarrow$ స\*\* (\*Bhāratam\*, Ādi 1-118)\[cite: 9\]; \*\*స్థి \[సి\] $\\longleftrightarrow$ జే\*\* (\*Bhāratam\*, Ādi 8-83)\[cite: 9\]; \*\*త్సూ \[సూ\] $\\longleftrightarrow$ జు\*\* (\*Bhāratam\*, Ādi 5-258)\[cite: 9\]; \*\*త్స \[స\] $\\longleftrightarrow$ జే\*\* (\*Bhāratam\*, Ādi 2-13)\[cite: 9\]; \*\*జూ $\\longleftrightarrow$ స్రు \[సు\]\*\* (\*Nalacaritra\* 1-69)\[cite: 9\]; \*\*స $\\longleftrightarrow$ ర్జ \[ఝ\]\*\* (\*Bhāratam\*, Sabhā 1-72)\[cite: 9\]; \*\*ఝం $\\longleftrightarrow$ స్వ \[స\]\*\* (\*Śivarātri Māhātmyamu\* 5-87)\[cite: 9\]; \*\*ర్ఘ \[ఝ\] $\\longleftrightarrow$ స్వా \[సా\]\*\* (\*Bhāratam\*, Sabhā 2-233)\[cite: 9\].

12\. \*\*అభేదయతి ('వ-బ' 6.27.12):\*\* \*\*వ $\\longleftrightarrow$ బ్ర \[బ\]\*\* (\*Bhāratam\*, Sabhā 2-245)\[cite: 9\]; \*\*ల్వ \[వ\] $\\longleftrightarrow$ బా\*\* (\*Bhāratam\*, Ādi 6-230, Padmakamu)\[cite: 9\]; \*\*వ్ర \[వ\] $\\longleftrightarrow$ బా\*\* (\*Bhāratam\*, Ādi 4-94)\[cite: 9\]; \*\*ర్వ \[వ\] $\\longleftrightarrow$ బా\*\* (\*Bhāratam\*, Āraṇya 1-311)\[cite: 9\]; \*\*బ్రో \[బో\] $\\longleftrightarrow$ వొ\*\* in \*సిరివొందఁగ\* (\*Siṁhāsana Dvātriṁśika\* 6-75)\[cite: 9\].

13\. \*\*అభేదవర్గ యతి (6.27.13):\*\* \*\*ప్ర \[ప\] $\\longleftrightarrow$ వ\*\* in \*డీలువఱిచెన్\* (\*Amuktamālyada\* 4-163)\[cite: 9\]; \*\*క్వె \[వె\] $\\longleftrightarrow$ బ\*\* (\*Bhāratam\*, Virāṭa 5-92)\[cite: 9\]; \*\*ప్రే \[పే\] $\\longleftrightarrow$ వె\*\* in \*వెంచుచున్\* (\*Bhāratam\*, Āraṇya 1-206)\[cite: 9\]; \*\*ల్పు \[పు\] $\\longleftrightarrow$ వు\*\* (\*Bhāratam\*, Udyōga 5-92)\[cite: 9\]; \*\*ర్పు \[పు\] $\\longleftrightarrow$ వు\*\* in \*వుచ్చి\* (\*Daśakumāra Caritra\* 2-49)\[cite: 9\]; \*\*వొ $\\longleftrightarrow$ ప్పు \[పు\]\*\* in \*గందవొడి\* (\*Niraṅkuśōpākhyānamu\* 2-20)\[cite: 9\]; \*\*స్ఫీ \[ఫీ\] $\\longleftrightarrow$ వి\*\* (\*Bhāratam\*, Āraṇya 6-103)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ వో\*\* in \*మంచువోలె\* (\*Kāśīkhaṇḍam\* 1-35)\[cite: 9\]; \*\*ఫ $\\longleftrightarrow$ వ్రా \[వా\]\*\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 635)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ వు\*\* (\*Appakavīyamu\* 3-102)\[cite: 9\].

14\. \*\*'ల-ళ' అభేదయతి (6.27.14):\*\* \*\*ళ $\\longleftrightarrow$ లి\*\* in \*బిళ్ళల\* (\*Manu Caritra\* 4-72)\[cite: 9\]; \*\*ళ $\\longleftrightarrow$ ల\*\* (\*Manu Caritra\* 4-100)\[cite: 9\]; \*\*ల్ప \[ల\] $\\longleftrightarrow$ వే\*\* (\*Manu Caritra\* 4-128)\[cite: 9\]; \*\*ల్వ \[ల\] $\\longleftrightarrow$ లా\*\* (\*Manu Caritra\* 5-81)\[cite: 9\]; \*\*ల్ల \[ల\] $\\longleftrightarrow$ ళి\*\* (\*Manu Caritra\* 5-79)\[cite: 9\]; \*\*ళ $\\longleftrightarrow$ ల్లా \[లా\]\*\* (\*Haravilāsam\* 1-60)\[cite: 9\]; \*\*ల్లి \[లి\] $\\longleftrightarrow$ ళి\*\* (\*Bhāratam\*, Ādi 3-109)\[cite: 9\]; \*\*ళీ $\\longleftrightarrow$ ల్మి \[లి\]\*\* (\*Manu Caritra\* 5-25)\[cite: 9\].

15\. \*\*'ము' విభక్తి యతి (6.27.15):\*\* \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ ముం\*\* (\*Śivarātri Māhātmyamu\* 4-8)\[cite: 9\]; \*\*త్పు \[పు\] $\\longleftrightarrow$ ము\*\* in \*సత్యములు\* (\*Bhāratam\*, Udyōga 5-546)\[cite: 9\]; \*\*త్పు \[పు\] $\\longleftrightarrow$ ము\*\* in \*ఫలమున్\* (\*Kāśīkhaṇḍam\* 3-243)\[cite: 9\]; \*\*మ్ము \[ము\] $\\longleftrightarrow$ పు\*\* (\*Bhāratam\*, Udyōga 6-60)\[cite: 9\]; \*\*మ్ము \[ము\] $\\longleftrightarrow$ పొ\*\* (\*Bhāratam\*, Udyōga 5-3-302)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ ము\*\* (\*Bhāratam\*, Āraṇya 5-217, Taralamu)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ ము\*\* (\*Bhāratam\*, Sabhā 2-418)\[cite: 9\]; \*\*స్ఫు \[ఫు\] $\\longleftrightarrow$ ము\*\* (\*Amuktamālyada\* 4-132)\[cite: 9\]; \*\*మ్ము \[ము\] $\\longleftrightarrow$ స్ఫూ \[పూ\]\*\* (\*Bhāgavatam\* 8-250)\[cite: 9\]; \*\*స్ఫో \[ఫో\] $\\longleftrightarrow$ ము\*\* in \*వక్షము\* (\*Bhāratam\*, Āraṇya 7-88)\[cite: 9\]; \*\*ర్బు \[బు\] $\\longleftrightarrow$ ము\*\* (\*Manu Caritra\* 1-41, Mattakōkila)\[cite: 9\]; \*\*న్బొ \[బొ\] $\\longleftrightarrow$ ము\*\* (\*Manu Caritra\* 1-80)\[cite: 9\]; \*\*బ్రో \[బో\] $\\longleftrightarrow$ ము\*\* (\*Bhāratam\*, Anuśāsanika 5-106)\[cite: 9\].

16\. \*\*'ము'కార యతి (6.27.16):\*\* \*\*మ్ము \[ము\] $\\longleftrightarrow$ పు\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 546)\[cite: 9\]; \*\*స్ఫూ \[పూ\] $\\longleftrightarrow$ మూ\*\* (\*Bhāgavatam\* 5-97)\[cite: 9\]; \*\*భూ $\\longleftrightarrow$ మ్రొ \[మొ\]\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Bāla 1158)\[cite: 9\]; \*\*ల్పు \[పు\] $\\longleftrightarrow$ మొ\*\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1169)\[cite: 9\]; \*\*భు $\\longleftrightarrow$ న్మూ \[మూ\]\*\* (\*Bhāratam\*, Virāṭa 3-694)\[cite: 9\]; \*\*భూ $\\longleftrightarrow$ మ్రో \[మో\]\*\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 1952)\[cite: 9\].

&nbsp;

\---

&nbsp;

\*\*6.28 సంయుక్త యతి \- 'న'కార సంశ్లేషము (Druta-Saṁślēṣa Saṁyukta Yati)\*\*

&nbsp;

\* \*\*Operational Definition:\*\* A specialized, uncodified architectural license universally practiced across classical Telugu poetry (\*Mahākavi prayōgamu\*)\[cite: 9\].

\* \*\*The Structural Problem:\*\* In many classical lines, a superficial inspection reveals an apparent, fatal Yati break (\*yati-bhaṅgamu\*)\[cite: 9\]. For example, in \*Manu Caritra\* (1-55), Line 3 opens with \*\*సా\*\* (\*sā\*) and the caesura lands on \*\*న్య\*\* (\*nya\*)\[cite: 9\]. Neither \*sā-na\* nor \*sā-ya\* is a valid match\[cite: 9\].

\* \*\*The Classical Mechanical Resolution:\*\*

  \* Notice that the preceding line (Line 2\) terminates in an inflected nasal \*drutamu\* (\*\*న్\*\*)\[cite: 9\].

  \* In ancient scribal orthography, lines were continuous: the line-ending \*drutamu\* fused directly with the initial consonant of the subsequent line via sandhi / phonemic compounding (\*saṁślēṣamu\*): $\\text{న్} \+ \\text{సా} \= \\text{న్సా}$\[cite: 9\].

  \* The initial coordinate of Line 3 is therefore not a simple consonant, but the conjunct cluster \*\*'న్సా'\*\* (\*nsā\*)\[cite: 9\]\!

  \* Under \*Saṁyukta Yati\* (6.26), the poet extracts the nasal element \*\*'నా'\*\* from \*\*న్సా\*\* to rhyme with \*\*న్య \[న\]\*\* (\*mānya\*), perfectly validating the line under \*\*'న'కార ప్రాణియతి\*\*\[cite: 9\]\!

&nbsp;

&nbsp;

                Druta-Saṁślēṣa Saṁyukta Yati Flow

     \[ Line N-1 terminates in Drutamu: ...న్ \]

                         │

              (Phonemic Line-Bridge Fused)

                         ▼

     \[ Line N opens with Consonant C: సా \]

                         │

             Compound Conjunct Formed:

               \[ న్ \+ సా \= న్సా \]

                         │

        Under Saṁyukta Yati Axiom (6.26):

           Extract constituent 'నా'

                         │

                         ▼

 Matches Caesura on 'న్య' (Evaluated as నా ⟷ న)

               VALID PRĀṆI YATI\!

&nbsp;

&nbsp;

\* \*\*Metric Integrity Guarantee (6.28(1)):\*\* Fusing the drutamu turns it into a conjunct-preceding element, ensuring the final syllable of Line $N-1$ remains prosodically heavy (\*guru\*), preserving identical gaṇa counts\[cite: 9\]. Modern prints separate the drutamu purely for visual readability (\*pāṭhana-saulabhyamu\*), which masks this classical compound\[cite: 9\].

\* \*\*Permissive, Non-Obligatory Status (6.28(4)):\*\* Druta-saṁślēṣa is an \*available license\*, never a mandate\[cite: 9\]. If Line $N$ can satisfy Yati natively on its own initial consonant, the preceding line's drutamu is bypassed entirely\[cite: 9\].

\* \*\*Historical Provenance of the Discovery (6.28(6) – 6.28(8)):\*\*

  \* \*Nannaya:\* Employed this technique uniquely in \*Mahābhārata\* (Ādi 6-200): Line 3 ends in \*...నిచ్చటన్\*; Line 4 opens with \*మెచ్చగు...\* matching caesura \*నిద్రకు...\* (\*\*న్ \+ మె \= న్మె $\\rightarrow$ నె $\\longleftrightarrow$ ని\*\*)\[cite: 9\].

  \* \*Tikkana:\* Extensively utilized this architecture throughout the \*Mahābhārata\* and \*Nirvacanōttara Rāmāyaṇamu\* (e.g., \*...నిర్వహించుచున్ / భేదము... నిర్మల...\* $\\rightarrow$ \*\*న్ \+ భే \= న్భే $\\rightarrow$ నే $\\longleftrightarrow$ ని\*\*)\[cite: 9\].

  \* \*Errana:\* Frequently deployed in \*Harivaṁśamu\* and \*Nr̥siṁha Purāṇamu\*\[cite: 9\].

&nbsp;

\#\#\#\# Three Architectural Sites for Druta-Saṁślēṣa

&nbsp;

\* \*\*Site 1: Line-Start Fusion (పాదాది సంశ్లేషము 6.28.1):\*\*

  A trailing drutamu of the preceding line fuses with the first letter of the active line\[cite: 9\]:

  \* \*\*న్ \+ గ \= న్గ $\\rightarrow$ న $\\longleftrightarrow$ న:\*\* \*...లోపలన్ / గదుర... బహూకృతులాచరించుచున్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 1226)\[cite: 9\].

  \* \*\*న్ \+ గా \= న్గా $\\rightarrow$ నా $\\longleftrightarrow$ నా:\*\* \*...మాంబకున్ / గారమైన... శ్రీనాథాఖ్యునిం...\* (\*Kāśīkhaṇḍam\* 1-12)\[cite: 9\].

  \* \*\*న్ \+ ఘో \= న్ఘో $\\rightarrow$ నో $\\longleftrightarrow$ ంతు:\*\* \*...ప్రేమాంచత్కటాక్షంబులన్ / ఘోరాసూయ... తత్సమాకారున...\* (\*Bhāratam\*, Āraṇya 3-267)\[cite: 9\].

  \* \*\*న్ \+ జ \= న్జ $\\rightarrow$ న $\\longleftrightarrow$ నా:\*\* \*...వానియానతిన్ / జని రథివర్యుఁడైన...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 88)\[cite: 9\].

  \* \*\*న్ \+ డి \= న్డి $\\rightarrow$ ని $\\longleftrightarrow$ నే:\*\* \*...వాహనంబులన్ / డిగ్గి తలంగు సైనికులు నేలకుఁ...\* (\*Bhāratam\*, Āraṇya 2-355)\[cite: 9\].

  \* \*\*న్ \+ ది \= న్ది $\\rightarrow$ ని $\\longleftrightarrow$ ని:\*\* \*...నుఁజేయకెంతయున్ / దిట్టలనంగ విద్యయు వినీతతయున్...\* (\*Bhāratam\*, Ādi 2-207)\[cite: 9\].

  \* \*\*న్ \+ పా \= న్పా $\\rightarrow$ నా $\\longleftrightarrow$ ణ:\*\* \*...నీకున్ / ఫాలనయన...\* (\*Bhāratam\*, Anuśāsanika 4-424)\[cite: 9\].

  \* \*\*న్ \+ బి \= న్బి $\\rightarrow$ ని $\\longleftrightarrow$ ని:\*\* \*...ఖాంకురంబునన్ / బిద్దము చేసె... నిండని...\* (\*Haravilāsam\* 6-21)\[cite: 9\].

  \* \*\*న్ \+ భూ \= న్భూ $\\rightarrow$ నూ $\\longleftrightarrow$ ణు:\*\* \*...ముదితుండగుచున్ / భూవినుతుల రామలక్ష్మణులఁజీరి...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 206)\[cite: 9\].

  \* \*\*న్ \+ మ్రు \= న్మ్రు $\\rightarrow$ ను $\\longleftrightarrow$ నొ:\*\* \*...మదిన్ / మ్రుచ్చుల గిట్టి పట్టుదురు నొంపుదురేమనవచ్చు...\* (\*Kāśīkhaṇḍam\* 8-69)\[cite: 9\].

  \* \*\*న్ \+ మ \= న్మ $\\rightarrow$ న $\\longleftrightarrow$ ంథా:\*\* \*...సంధాతయున్ / మసృణస్నిగ్ధతరక్షు... కంథాభద్రపీఠుండునై...\* (\*Bhāgavatam\* 7-29)\[cite: 9\].

  \* \*\*న్ \+ మా \= న్మా $\\rightarrow$ నా $\\longleftrightarrow$ ంతా:\*\* \*...తీరంబునన్ / మావుల్ క్రోవులునల్లిబిల్లిగొను కాంతారంబునం...\* (\*Manu Caritra\* 2-22)\[cite: 9\].

  \* \*\*న్ \+ య \= న్య $\\rightarrow$ న $\\longleftrightarrow$ నా:\*\* \*...యాదోనాథ సుతాకళత్రు బదరీనారాయణున్ గంటినీ...\* (\*Manu Caritra\* 1-71)\[cite: 9\].

  \* \*\*న్ \+ రా \= న్రా $\\rightarrow$ నా $\\longleftrightarrow$ న:\*\* \*...కన్నుఁ గోనలన్ / రాలఁగనిప్పుడీ త్రిభువనంబులనొక్కట...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 170)\[cite: 9\].

  \* \*\*న్ \+ రా \= న్రా $\\rightarrow$ నా $\\longleftrightarrow$ ండ:\*\* \*...వణిశ్రేష్ఠాన్వయాంభోధికిన్ / రాకాపూర్ణ నిశాకరుండు చిఱుతొండ...\* (\*Kāśīkhaṇḍam\* 7-49)\[cite: 9\].

  \* \*\*న్ \+ ల \= న్ల $\\rightarrow$ న $\\longleftrightarrow$ న:\*\* \*...చేతనంతన్ / లంకకు వేఁగందెనందినన్విని...\* (\*Bhāratam\*, Sabhā 2)\[cite: 9\].

  \* \*\*న్ \+ వ \= న్వ $\\rightarrow$ న $\\longleftrightarrow$ ంద:\*\* \*...దీవ్యద్గాత్రుఁడమ్మాలియున్ / వసుదారిద్ర్యయుతుండు పెన్నిధులఁ జెందన్గోరు...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 250)\[cite: 9\].

  \* \*\*న్ \+ వె \= న్వె $\\rightarrow$ నె $\\longleftrightarrow$ ణీ:\*\* \*...ఘనావరోధమున్ / వెలివడఁ జేయనేర్తురు మణీనిపణీత...\* (\*Manu Caritra\* 1-99)\[cite: 9\].

  \* \*\*న్ \+ శ \= న్శ $\\rightarrow$ న $\\longleftrightarrow$ న:\*\* \*...జడున్ / శరణార్థిన్ ననుఁ గానఁగాఁదగు...\* (\*Manu Caritra\* 6-106)\[cite: 9\].

  \* \*\*న్ \+ శ్ర \= న్శ్ర $\\rightarrow$ న $\\longleftrightarrow$ నం:\*\* \*...భటులు గడున్ / శ్రమమొందిరి తమము గవిసినంగాని సముద్యమ...\* (\*Bhāratam\*, Āraṇya 3-194)\[cite: 9\].

  \* \*\*న్ \+ సై \= న్సై $\\rightarrow$ నై $\\longleftrightarrow$ న:\*\* \*...లీలకున్ / సైరణ గల్గి నిల్వుమనినన్వినియట్టుల...\* (\*Bhāratam\*, Āraṇya 2-288)\[cite: 9\].

  \* \*\*న్ \+ స్వా \= న్స్వా $\\rightarrow$ నా $\\longleftrightarrow$ నా:\*\* \*...చకోరాక్షులున్ / స్వారాజప్రియ వారభామినులు నానాభూషణాలంకృతల్...\* (\*Bhāgavatam\* 3-204)\[cite: 9\].

  \* \*\*న్ \+ హ \= న్హ $\\rightarrow$ న $\\longleftrightarrow$ న:\*\* \*...సితోడుభక్తమున్ / హరిహయదిఙ్నభస్థలమునన్బలిచల్లి...\* (\*Manu Caritra\* 3-21)\[cite: 9\].

&nbsp;

\* \*\*Site 2: Caesura-Site Preceding Fusion (యతిస్థానమున సంశ్లేషము 6.28.2):\*\*

  An internal drutamu preceding the caesura syllable fuses with it to yield an active nasal coordinate\[cite: 9\]:

  \* \*Alliteration on న్మ \[న\]:\* \*...కందళ చూత్కార పరంపరల్ పయిపయిన్ మధ్యాహ్నముం దెల్పెడిన్\* (Line-start \*\*ంద\*\* matches $\\text{పయిపయిన్} \+ \\text{మధ్యాహ్నము} \\rightarrow \\mathbf{న్మ\\ \[న\]}$ under Bindu Yati) (\*Manu Caritra\* 2-12)\[cite: 9\].

  \* \*Alliteration on న్భి \[ని\]:\* \*నీ పంచం బడి యుండఁగాఁ గలిగినన్ భిక్షాన్నమేచాలునిక్షేపంబబ్బిన...\* (Line-start \*\*నీ\*\* matches $\\text{గలిగినన్} \+ \\text{భిక్షాన్నమే} \\rightarrow \\mathbf{న్భి\\ \[ని\]}$ under Prāṇi Yati) (\*Śrīkālahastīśvara Śatakam\*)\[cite: 9\].

  \* \*\*నీ $\\longleftrightarrow$ న్నె \[నె\]:\*\* \*నీతోడ్పాటున నేఁద్రివిష్టపములన్ గెల్వంగనూఁకింతు నా...\* (\*Bhāratam\*, Udyōga 5-3-130)\[cite: 9\].

  \* \*\*ంధ $\\longleftrightarrow$ న్బం \[నం\]:\*\* \*...బంధముతోనా విధుఁడేఁగెఁ బ్రొద్దువొడిచెన్ బంధూక బంధుచ్ఛవిన్...\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 136)\[cite: 9\].

  \* \*\*ష్ణ $\\longleftrightarrow$ న్నే \[నే\]:\*\* \*...నిష్కాసంబులునెల్లనార్పులు వడిన్ భేదింపరాకుండ...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 481)\[cite: 9\].

  \* \*\*ండ $\\longleftrightarrow$ న్మం \[నం\]:\*\* \*...మొగుడుందమ్ముల కొండగడిం దేఱుగడైనపట్లఁ దమమున్ మందేహులం దోలి...\* (\*Manu Caritra\* 1-5)\[cite: 9\].

  \* \*\*నా $\\longleftrightarrow$ న్ర \[న\]:\*\* \*నా శీలంబణువైన మేరువనుచున్ రక్షింపవేనీ కృపా...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 9\].

  \* \*\*ణ $\\longleftrightarrow$ న్వి \[ని\]:\*\* \*...శోణిత పంకాంకిత గండతుండుఁడగుచున్ విష్ణుండు దానొప్పెవిస్తృత...\* (\*Bhāgavatam\* 3-419)\[cite: 9\].

  \* \*\*న్న \[న\] $\\longleftrightarrow$ న్శ \[న\]:\*\* \*...బూజగొన్న విహీనాత్ముని మేము సైపమనుచున్ శక్రాజ్ఞ గోవర్ధనా...\* (\*Harivaṁśamu\* 7-166)\[cite: 9\].

&nbsp;

\* \*\*Site 3: Simultaneous Dual Fusion (ఉభయ సంశ్లేషము 6.28(10)):\*\*

  Both the line-start and the caesura site fuse with preceding drutamus simultaneously\[cite: 9\]:

  \* \*Bhāratam\* (Śalyā 1-278):

    Line ends: \*...శోభిల్లుచున్\* $\\rightarrow$ next line opens with \*మణి...\*\[cite: 9\]

    Caesura lands on: \*...స్ఫురణమున్ సంశోభి...\*\[cite: 9\]

    Resolution: $\\text{న్} \+ \\text{మ} \= \\mathbf{న్మ\\ \[న\]} \\quad\\longleftrightarrow\\quad \\text{న్} \+ \\text{సం} \= \\mathbf{న్సం\\ \[న\]}$\[cite: 9\]

    Evaluates as a flawless \*\*న $\\longleftrightarrow$ న\*\* Prāṇi Yati\[cite: 9\]\!

&nbsp;

\---

&nbsp;

\*\*Algorithmic Engine Logic & Execution Rules for Druta-Saṁślēṣa (6.28(11))\*\*

&nbsp;

&nbsp;

              Automated Engine Verification Logic

&nbsp;

Step 1: Check Standard Yati Does Syllable\_1 match Syllable\_YatiSthāna via native rules? ├── YES ──\> PASS (Standard Resolution, no Saṁślēṣa needed) └── NO  ──\> Proceed to Step 2

Step 2: Check Preceding Drutamu at Line-Start Did Line N-1 terminate in a Drutamu (న్)? ├── YES ──\> Synthesize Cluster: \[ న్ \+ Syllable\_1 \] │           Extract constituent nasal: 'న' \+ Vowel\_1 │           Does this synthesized coordinate match Syllable\_YatiSthāna? │           ├── YES ──\> PASS (Druta-Saṁślēṣa Pādādi Mode) │           └── NO  ──\> Proceed to Step 3 └── NO  ──\> Proceed to Step 3

Step 3: Check Preceding Drutamu at Caesura Site Does a Drutamu (న్) precede Syllable\_YatiSthāna? ├── YES ──\> Synthesize Cluster: \[ న్ \+ Syllable\_YatiSthāna \] │           Extract constituent nasal: 'న' \+ Vowel\_Yati │           Does Syllable\_1 match this synthesized coordinate? │           ├── YES ──\> PASS (Druta-Saṁślēṣa Yati-Sthāna Mode) │           └── NO  ──\> Proceed to Step 4 └── NO  ──\> Proceed to Step 4

Step 4: Check Dual Fusion Mode Did Line N-1 end in న్ AND does a న్ precede Syllable\_YatiSthāna? ├── YES ──\> Synthesize BOTH coordinates to 'న' │           Evaluate: \[ 'న' \+ V₁ \] ⟷ \[ 'న' \+ V\_Yati \] │           ├── YES ──\> PASS (Dual Druta-Saṁślēṣa Mode) │           └── NO  ──\> FAIL (True Metrical Break) └── NO  ──\> FAIL (True Metrical Break)

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.28.3 ఉభయ ద్రుత సంశ్లేషము (Simultaneous Dual-Site Druta-Saṁślēṣa)

When a line exhibits an apparent double caesura failure, it frequently resolves through simultaneous druta fusion at **both** the line onset (*pādādi*) and the internal caesura coordinate (*yati-sthāna*):

$$\\text{Line } N-1\\ (\\dots\\mathbf{న్}) \+ \\text{Line } N\\ (\\mathbf{\\text{C}*1}\\dots\\mathbf{న్} \+ \\mathbf{\\text{C}*{\\text{yati}}}\\dots) \\implies \[\\mathbf{న్} \+ \\text{C}*1\] \\longleftrightarrow \[\\mathbf{న్} \+ \\text{C}*{\\text{yati}}\]$$

Both coordinates extract their synthesized dental nasal (**'న'**), resolving as a flawless **'న'కార ప్రాణియతి**:

* **న్ \+ ఖ \= న్ఖ \[న\] $\\longleftrightarrow$ న్ \+ గ \= న్గ \[న\]:** *...పాతంబులన్ / ఖండీభూతములున్ విదారితములున్ భగ్నంబులుంగా సముద్దండుండై...* (*Bhāskara Rāmāyaṇamu*, Kiṣkindha 4-306).  
* **న్ \+ ము \= న్ము \[ను\] $\\longleftrightarrow$ న్ \+ గో \= న్గో \[నో\]:** *...హారావళిన్ / మునిబృందారక సేవ్యమాన సలిలన్ గోదావరీ వాహినిన్...* (*Bhīmēśvara Purāṇamu* 4-178).  
* **న్ \+ మృ \= న్మృ \[నృ\] $\\longleftrightarrow$ న్ \+ వే \= న్వే \[నే\]:** *...నేనిచ్చెదన్ / మృడుబాణాసనమున్న మందసదగన్ వేతెండు మీరేఁగి...* (*Bhāskara Rāmāyaṇamu*, Kiṣkindha 674).  
* **న్ \+ హృ \= న్హృ \[నృ\] $\\longleftrightarrow$ న్ \+ ని \= న్ని \[ని\]:** *...సంయుక్తంబు గావించుచున్ / హృద్యంబై యది యంతకంతకలరన్ నిల్పెన్ గడున్ జిత్తమున్...* (*Manu Caritra* 2-107).

---

### 6.29 సంయుక్త యతి — 'ల'కార సంశ్లేషము (La-kāra Saṁślēṣa Saṁyukta Yati)

* **Grammatical Foundation:** Grounded in *Bāla Vyākaraṇam* (Prakīrṇaka 16: *"పదాంతంబులయి యసంయుక్తంబులయిన నులురుల యుత్వంబునకు లోపంబు బహుళంబుగనగు"*). When a word terminates in uncombined **'లు'** (*lu*), its final vowel optionally drops (*ukāra lōpamu*) before a pause (*avasāna*) or preceding a consonant, leaving a vowelless liquid: **'ల్'** (*pollu-la*).  
* **Morphological Sources of 'ల్':**  
1. *Plural Nominal Suffix (లు-వర్ణకము):* *రాములు $\\rightarrow$ రాముల్*; *వనములు $\\rightarrow$ వనముల్*.  
2. *Lexical Root Final (శబ్దసిద్ధ 'లు'):* *కాలు $\\rightarrow$ కాల్* (as in *కాల్నిలువక*); *మొగులు $\\rightarrow$ మొగుల్*; *ఒడలు $\\rightarrow$ ఒడల్*.  
* **The Structural Rule:** When a line ends in **'ల్'**, it optionally fuses with the initial consonant of the subsequent line, creating a conjunct cluster ($\\text{ల్} \+ \\text{C}$). Under *Saṁyukta Yati* (6.26), the poet is legally licensed to **extract the constituent 'ల' to satisfy Yati**.  
* **Discovery & Attribution:** First systematically employed in classical verse by Tikkana (*Bhāratam*, Virāṭa 2-55: *మత్పతుల్ / గీర్వాణాకృతులేవురిష్ణు నిను దోర్లీలన్...* $\\rightarrow \\text{ల్} \+ \\text{గీ} \= \\mathbf{ల్గీ\\ \[లీ\]} \\longleftrightarrow \\mathbf{లీ}$).  
* **Permissive Nature (ఐచ్ఛికము):** Druta-like fusion of 'ల' is an optional license, not an absolute mandate. If the line naturally aligns on its native initial consonant, the preceding 'ల్' is ignored (*Śṛṅgāra Śakuntalamu* 5-37).

                    La-kāra Saṁślēṣa Flow

      \[ Line N-1 ends in Pollu-La: ...ల్ \]

                        │

             (Phonemic Fusion Bridge)

                        ▼

      \[ Line N opens with Consonant C \]

                        │

            Compound Cluster Synthesized:

              \[ ల్ \+ C \= ల్C \]

                        │

         Under Saṁyukta Yati Axiom (6.26):

         Extract constituent 'ల' \+ Vowel

                        ▼

     Matches Caesura on Lateral Liquid ('ల' / 'ళ')

              VALID PRĀṆI / ABHĒDA YATI\!

\`\`\`\[cite: 10\]

&nbsp;

\#\#\#\# 1\. పాదాదిలో సంశ్లేషము (Line-Start Fusion 6.29.1)

The trailing 'ల్' of the preceding line fuses with the active line's initial consonant\[cite: 10\]:

\* \*\*ల్ \+ గ \= ల్గ $\\rightarrow$ ల $\\longleftrightarrow$ లా:\*\* \*...వాంఛితార్థముల్ / గలుగునమేయుచేతఁగమలాధవుచే...\* (\*Appakavīyamu\* 4-500)\[cite: 10\].

\* \*\*ల్ \+ గి \= ల్గి $\\rightarrow$ లి $\\longleftrightarrow$ లీ:\*\* \*...మేఘముల్ / గిఱికొననొప్పునాకసములీల...\* (\*Bhāratam\*, Udyōga 5-1-278)\[cite: 10\].

\* \*\*ల్ \+ గౌ \= ల్గౌ $\\rightarrow$ లౌ $\\longleftrightarrow$ ళా (Abhēda):\*\* \*...సప్త సంయముల్ / గౌతమ ముఖ్యులైందవకళాధరు...\* (\*Kāśīkhaṇḍam\* 2-4-24)\[cite: 10\].

\* \*\*ల్ \+ ఘో \= ల్ఘో $\\rightarrow$ లో $\\longleftrightarrow$ లుం:\*\* \*...వివిధాయుధప్రభల్ / ఘోరనిరూఢినెల్లదెసలుం...\* (\*Harivaṁśamu\* 4-5-130)\[cite: 10\].

\* \*\*ల్ \+ చూ \= ల్చూ $\\rightarrow$ లూ $\\longleftrightarrow$ లో:\*\* \*...విలాసవైఖరుల్ / చూడమె నాగకన్యకల లోకమనోహర...\* (\*Manu Caritra\* 2-2-102)\[cite: 10\].

\* \*\*ల్ \+ జ \= ల్జ $\\rightarrow$ ల $\\longleftrightarrow$ ల:\*\* \*...నాభీతలంబంగముల్ / జడనొందెన్ బలిసెంగుచద్వయము...\* (\*Harivaṁśamu\*, Uttara 3-178)\[cite: 10\].

\* \*\*ల్ \+ డా \= ల్డా $\\rightarrow$ లా $\\longleftrightarrow$ ల:\*\* \*...వ్రాతముల్ / డాఁగెన్ బల్వల పంకసీమ బకజాల...\* (\*Śṛṅgāra Śakuntalamu\* 4-20)\[cite: 10\].

\* \*\*ల్ \+ ద \= ల్ద $\\rightarrow$ ల $\\longleftrightarrow$ లా:\*\* \*...జిహ్వికల్ / దనికనఁ బెల్చ మండుచునిలాస్థలి...\* (\*Bhāratam\*, Śānti 5-3-325)\[cite: 10\]; \*...చంద్రికల్ / దనుకన్ జూచెలతాంగి...\* (\*Manu Caritra\* 2-2-30)\[cite: 10\]; \*...దనరన్ గస్తురి రేఖదీర్చె నవకుల్యావైఖరిన్...\* (\*Daśakumāra Caritra\* 2-5-116)\[cite: 10\].

\* \*\*ల్ \+ నా \= ల్నా $\\rightarrow$ లా $\\longleftrightarrow$ ల:\*\* \*...గంధముల్ / నా మెఱుఁగారు క్రొవ్విరులెలర్చిన...\* (\*Nr̥siṁha Purāṇamu\* 2-64)\[cite: 10\].

\* \*\*ల్ \+ ప \= ల్ప $\\rightarrow$ ల $\\longleftrightarrow$ ళం (Abhēda):\*\* \*...పుష్పమాలికల్ / పట్టిరి పేరటాండ్రు ధవళంబులు...\* (\*Manu Caritra\* 2-3-76)\[cite: 10\].

\* \*\*ల్ \+ పా \= ల్పా $\\rightarrow$ లా $\\longleftrightarrow$ లా:\*\* \*...త్రయీ ధర్మముల్ / పాపంబుల్ రతి పుణ్యమంచునిఁక నేలా...\* (\*Manu Caritra\* 2-64)\[cite: 10\].

\* \*\*ల్ \+ మా \= ల్మా $\\rightarrow$ లా $\\longleftrightarrow$ ల:\*\* \*...మీ మహత్త్వముల్ / మానిని దివ్యముల్ మదిఁ దలంచిననెందును...\* (\*Manu Caritra\* 2-2-49)\[cite: 10\].

\* \*\*ల్ \+ వొ \= ల్వొ $\\rightarrow$ లొ $\\longleftrightarrow$ లో:\*\* \*...రాక్షసుల్ / వొదిగొని కావనిన్పవలలోనమృతంబు...\* (\*Bhāratam\*, Anuśāsanika 1-216)\[cite: 10\].

\* \*\*ల్ \+ సు \= ల్సు $\\rightarrow$ లు $\\longleftrightarrow$ లో:\*\* \*...రూపముల్ / సురనర కిన్నరద్యుచర లోకభయంకరముల్...\* (\*Bhāgavatam\* 7-187)\[cite: 10\].

\* \*\*ల్ \+ మ్రో \= ల్మ్రో $\\rightarrow$ లో $\\longleftrightarrow$ లుం:\*\* \*...తుమ్మెదల్ / మ్రోయకుఁడీ శుకంబులునెలుంగులు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 199)\[cite: 10\].

&nbsp;

\#\#\#\# 2\. యతిస్థానమున సంశ్లేషము (Caesura-Site Fusion 6.29.2)

An internal 'ల్' preceding the caesura coordinate fuses with it to yield the matching lateral liquid\[cite: 10\]:

\* \*\*ల $\\longleftrightarrow$ ల్ \+ గా \= ల్గా \[లా\]:\*\* \*...తద్ధూమజాలసమశ్రీల విశాలనీల వలభుల్ గాన్పించెఁ...\* (\*Amuktamālyada\* 4-263)\[cite: 10\].

\* \*\*ల $\\longleftrightarrow$ ల్ \+ న \= ల్న \[ల\]:\*\* \*...లీలంబక్షిరాట్కేతనోల్లసితంబైన రథంబుఁ దెచ్చిరి ప్రభల్ నల్దిక్కులం...\* (\*Kāśīkhaṇḍam\* 3-133)\[cite: 10\].

\* \*\*లు $\\longleftrightarrow$ ల్ \+ ను \= ల్ను \[లు\]:\*\* \*...కాల్వుర మొత్తంబులు రూపడంగె సిడముల్ నుగ్గయ్యెనన్నేల...\* (\*Bhāratam\*, Udyōga 5-2-200)\[cite: 10\].

\* \*\*ల $\\longleftrightarrow$ ల్ \+ పం \= ల్పం \[ల\]:\*\* \*...సిందువారహరీ శ్రీకరమాలికా శిశిరముల్ పంపాసఖుల్...\* (\*Amuktamālyada\* 5-3-14)\[cite: 10\].

\* \*\*లో $\\longleftrightarrow$ ల్ \+ శు \= ల్శు \[లు\]:\*\* \*లోనుగాఁగల్గు వస్తువుల్ శుద్ధ హేమ...\* (\*Harivaṁśamu\*, Pūrva 3-156)\[cite: 10\].

\* \*\*లా $\\longleftrightarrow$ ల్ \+ సం \= ల్సం \[ల\]:\*\* \*...తృణోత్కరంబు హయముల్ సంప్రీతితో మేయఁగన్...\* (\*Harivaṁśamu\*, Pūrva 8-186)\[cite: 10\].

\* \*\*ళ $\\longleftrightarrow$ ల్ \+ సం \= ల్సం \[ల\] (Abhēda):\*\* \*...రోదోంతరాళము ఘూర్ణిల్లఁగఁ జేయునమ్మదకరుల్ సంరంభ...\* (\*Bhāgavatam\* 5-8-84)\[cite: 10\].

&nbsp;

\#\#\#\# 3\. ఉభయ సంశ్లేషము (Simultaneous Dual Fusion 6.29.3)

Both line-start and caesura site fuse with preceding 'ల్' consonants concurrently\[cite: 10\]:

\* \*\*ల్ \+ గ \= ల్గ \[ల\] $\\longleftrightarrow$ ల్ \+ సా \= ల్సా \[లా\]:\*\* \*...పిండాన్నముల్ / గయికోరా ప్రమదంబుతోడఁ బితరుల్ హస్తాబ్జముల్ సాఁచుచున్...\* (\*Kāśīkhaṇḍam\* 6-273)\[cite: 10\].

\* \*\*ల్ \+ మె \= ల్మె \[లె\] $\\longleftrightarrow$ లీ:\*\* \*...రక్షాహాటకాలంకృతుల్ / మెడహారంబులు మట్టెవన్నియరుచుల్ లీలావిలాసంబు...\* (\*Kāśīkhaṇḍam\* 4-197)\[cite: 10\].

\* \*\*ల్ \+ మే \= ల్మే \[లే\] $\\longleftrightarrow$ ల్ \+ హే \= ల్హే \[లే\]:\*\* \*...రూపముల్ / మేలై ధూర్తలు గాక వెండిగొరిజల్ హేమోరు శృంగంబులన్...\* (\*Bhāgavatam\* 9-92)\[cite: 10\].

&nbsp;

\#\#\#\# 4\. శబ్దసిద్ధ 'లు' సంశ్లేషము (Lexical Root Elisions 6.29.4)

Operates identically when 'లు' is an inherent root consonant rather than a plural affix\[cite: 10\]:

\* \*...ఒడల్ \[= ఒడలు\] తిరమే...\* fused as $\\text{ల్} \+ \\text{తి} \= \\mathbf{ల్తి\\ \[లి\]} \\longleftrightarrow \\text{ల్} \+ \\text{తే} \= \\mathbf{ల్తే\\ \[లే\]}$ in \*తేనియల్\* (\*Manu Caritra\* 2-65)\[cite: 10\].

\* \*...మొగుల్ \[= మొగులు\] బలుగమ్మచ్చుల...\* fused as $\\text{ల్} \+ \\text{బ} \= \\mathbf{ల్బ\\ \[ల\]} \\longleftrightarrow \\mathbf{ల}$ (\*Harivaṁśamu\* 3-6)\[cite: 10\].

&nbsp;

\#\#\#\# 5\. Co-existence of Na- and La-Saṁślēṣa in a Single Stanza (6.29.5)

Because line Yatis are strictly independent, poets freely deploy \*Na-saṁślēṣa\* in one line and \*La-saṁślēṣa\* in another within the same four-line stanza (\*Bhāratam\*, Udyōga 4-3-261; Udyōga 5-2-36; Harivaṁśamu 3-74; \*Manu Caritra\* 1-173)\[cite: 10\].

&nbsp;

\---

&nbsp;

\#\#\# 6.30 బహుయతి నియతి (Bahu-Yati Niyati — Multi-Caesura Invariance Constraint)

&nbsp;

\* \*\*Definition of Bahu-Yatulu:\*\* Verse forms mandating two or more internal caesura coordinates within every line\[cite: 10\]:

  \* \*Sragdhara (స్రగ్ధర):\* Coordinates 1 $\\rightarrow$ 8 $\\rightarrow$ 15\[cite: 10\].

  \* \*Mahāsragdhara (మహాస్రగ్ధర):\* Coordinates 1 $\\rightarrow$ 9 $\\rightarrow$ 16\[cite: 10\].

  \* \*Taruvoja (తరువోజ):\* Gaṇas 1 $\\rightarrow$ 3 $\\rightarrow$ 5 $\\rightarrow$ 7\[cite: 10\].

  \* \*Other Affected Meters:\* \*Māninī, Kavirājavirājitamu, Sarasijamu, Krauñcapadamu, Maṅgalamahāśrī, Vijayabhadra Ragaḍa, Vijayamaṅgaḻa Ragaḍa\*\[cite: 10\].

\* \*\*The Structural Invariance Constraint (బహుయతి నియతి):\*\*

  When the initial syllable of a line (\*vali\*) is a conjunct consonant ($\\text{C}\_1 \+ \\text{C}\_2 \+ \\text{V}$), \*\*whichever constituent consonant is selected to satisfy the FIRST internal caesura MUST be strictly maintained across ALL subsequent caesuras in that line\*\*\[cite: 10\]\!

  $$\\text{Line Opening: } \[\\text{C}\_1 \+ \\text{C}\_2 \+ \\text{V}\] \\implies \\text{If Caesura 1 selects } \\text{C}\_1 \\implies \\text{All remaining caesuras MUST match } \\text{C}\_1$$\[cite: 10\]

  A poet is strictly forbidden from matching Caesura 1 against $\\text{C}\_1$ and switching to $\\text{C}\_2$ for Caesura 2 within the same line\[cite: 10\].

\* \*\*Appakavi's Proof Stanza (\*Vijayabhadra Ragaḍa\*, 3-112):\*\*

  \* \*Line 1 (Compliant):\* Opens with \*\*క్ష్మా\*\* ($\\text{క్} \+ \\text{ష్} \+ \\text{మ్} \+ \\text{ఆ}$)\[cite: 10\]. Gaṇa 3 matches $\\text{C}\_1$ (\*\*కా $\\longleftrightarrow$ క\*\*)\[cite: 10\]. Gaṇa 5 matches $\\text{C}\_1$ (\*\*కా $\\longleftrightarrow$ ఘ\*\*)\[cite: 10\]. Gaṇa 7 matches $\\text{C}\_1$ (\*\*కా $\\longleftrightarrow$ గా\*\*)\[cite: 10\]. All caesuras adhere to the single consonant \*\*'క్'\*\*\[cite: 10\].

  \* \*Line 2 (Broken — Niyati-Bhaṅgamu):\* Opens with \*\*క్ష్మా\*\*\[cite: 10\]. Gaṇa 3 matches $\\text{C}\_1$ (\*\*కా $\\longleftrightarrow$ కం\*\* via \*Prāṇi\*)\[cite: 10\]. Gaṇa 5 switches to $\\text{C}\_2$ (\*\*షా $\\longleftrightarrow$ సం\*\* via \*Ūṣma\*)\[cite: 10\]. Gaṇa 7 switches to $\\text{C}\_3$ (\*\*మా $\\longleftrightarrow$ మ\*\* via \*Prāṇi\*)\[cite: 10\]. Even though each individual pair is a valid yati, the line commits \*\*Bahu-Yati Niyati Bhaṅgamu\*\* and is metrically invalid\[cite: 10\]\!

&nbsp;

&nbsp;

             Bahu-Yati Niyati Algorithmic Flow

   Line Opens with Conjunct: \[ C₁ \+ C₂ \+ C₃ \+ V \]

                         │

        Caesura Coordinate 1 Evaluated:

          Selects C\_k (e.g., C₁)

                         │

 ┌───────────────────────┴───────────────────────┐

 ▼                                               ▼

&nbsp;

Caesura Coordinate 2                            Caesura Coordinate 2 Evaluated against C₁                            Switches to C₂ or C₃ │                                               │ \[ PASS \]                                        \[ FAIL \] Adheres to Niyati                               Niyati-Bhaṅgamu\!

&nbsp;

\* \*\*Middle-Cluster Consistency (6.30.1):\*\* If an internal caesura coordinate is a conjunct cluster, the specific consonant chosen to match the line opening establishes the chain; subsequent coordinates cannot alternate to the unused consonants of that cluster (\*Appakavi\* 3-114)\[cite: 10\].

\* \*\*Explicit Exemption of Sēsamu (6.30.2):\*\* Appakavi explicitly codifies: \*"సీస పదములఁ దక్కన్"\* (\*Appakavīyamu\* 3-110)\[cite: 10\]. In a Sēsa padyam, the first half (Gaṇas 1–4) and the second half (Gaṇas 5–8) are structurally independent domains\[cite: 10\]. A poet may match the first half on $\\text{C}\_1$ and the second half on $\\text{C}\_2$ without committing a violation\[cite: 10\].

\* \*\*Canonical Adherence Corpus (6.30.3):\*\*

  \* \*Sragdhara:\* \*\*ధ్వాం \[ధా\] $\\longleftrightarrow$ త్త \[త\] (1-8) $\\longleftrightarrow$ ద (1-15)\*\* (\*Bhāratam\*, Ādi 6-80)\[cite: 10\]; \*\*వ్యా \[వా\] $\\longleftrightarrow$ వ (1-8) $\\longleftrightarrow$ ర్వా \[వా\] (1-15)\*\* (\*Bhāratam\*, Āraṇya 7-16)\[cite: 10\]; \*\*శ్రీ \[శీ\] $\\longleftrightarrow$ స్మి \[సి\] (1-8) $\\longleftrightarrow$ స్ఫీ \[సీ\] (1-15)\*\* (\*Bhāratam\*, Virāṭa 3-78)\[cite: 10\]; \*\*శ్రీ \[రీ\] $\\longleftrightarrow$ ర్చి \[రి\] (1-8) $\\longleftrightarrow$ శ్రే \[రే\] (1-15)\*\* (\*Bhāgavatam\* 1-1)\[cite: 10\]; \*\*జ్యో \[జో\] $\\longleftrightarrow$ శ్రు \[శు\] (1-8) $\\longleftrightarrow$ క్షో \[షో\] (1-15)\*\* (\*Kāśīkhaṇḍam\* 6-69)\[cite: 10\]; \*\*న్వీ \[నీ\] $\\longleftrightarrow$ ంద్రి \[ంది\] (1-8) $\\longleftrightarrow$ నే (1-15)\*\* (\*Bhīmēśvara Purāṇamu\* 3-200)\[cite: 10\]; \*\*శుం $\\longleftrightarrow$ చ్యు \[చు\] (1-8) $\\longleftrightarrow$ క్షో \[షో\] (1-15)\*\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 1-32)\[cite: 10\].

  \* \*Mahāsragdhara:\* \*\*శ్రి \[శి\] $\\longleftrightarrow$ స (1-9) $\\longleftrightarrow$ త్సే \[సే\] (1-16)\*\* (\*Bhāratam\*, Ādi 5-38)\[cite: 10\]; \*\*ఘ $\\longleftrightarrow$ క్వ \[క\] (1-9) $\\longleftrightarrow$ గ (1-16)\*\* (\*Bhāratam\*, Udyōga 5-5-421)\[cite: 10\]; \*\*స్ఫు \[పు\] $\\longleftrightarrow$ ద్భు \[భు\] (1-9) $\\longleftrightarrow$ స్ఫూ \[పూ\] (1-16)\*\* (\*Bhāratam\*, Sauptika 2-2-21)\[cite: 10\]; \*\*డ్కొ \[డొ\] $\\longleftrightarrow$ డు (1-9) $\\longleftrightarrow$ టో (1-16)\*\* (\*Harivaṁśamu\* 2-434)\[cite: 10\]; \*\*స్ఫు \[సు\] $\\longleftrightarrow$ క్షు \[షు\] (1-9) $\\longleftrightarrow$ స్తో \[సో\] (1-16)\*\* (\*Bhāgavatam\* 8-3)\[cite: 10\]; \*\*జ $\\longleftrightarrow$ శం \[శ\] (1-9) $\\longleftrightarrow$ సం \[స\] (1-16)\*\* (\*Harivaṁśamu\* 3-3)\[cite: 10\]; \*\*చ $\\longleftrightarrow$ ప్స \[స\] (1-9) $\\longleftrightarrow$ ర్శ్వ \[శ\] (1-16)\*\* (\*Kāśīkhaṇḍam\* 5-8)\[cite: 10\]; \*\*త్సు \[సు\] $\\longleftrightarrow$ ష్ణు \[షు\] (1-9) $\\longleftrightarrow$ చూ (1-16)\*\* (\*Manu Caritra\* 1-40)\[cite: 10\].

  \* \*Taruvoja:\* \*\*స్రు \[సు\] $\\longleftrightarrow$ శూ (1-3) $\\longleftrightarrow$ సొం (1-5) $\\longleftrightarrow$ సొ (1-7)\*\* (\*Bhāratam\*, Āraṇya 4-302)\[cite: 10\].

\* \*\*Lapses in the Corpus (6.30.4):\*\* Rare manuscript anomalies where poets switched consonants (\*Amuktamālyada\* 6-135; \*Bhāskara Rāmāyaṇamu\* 2-185; \*Amuktamālyada\* 4-238) are cataloged strictly as poetic oversights (\*kavi-prāmādikamu\*) and must be flagged as non-canonical errors by the parsing engine\[cite: 10\].

&nbsp;

\---

&nbsp;

\#\#\# 6.31 తద్భవవ్యాజ యతి (Tadbhavavyāja Yati — 'Jña' to Dental 'Na' & Retroflex 'Ṇa')

&nbsp;

\* \*\*Definition & Mechanics:\*\* The Sanskrit conjunct \*\*'జ్ఞ'\*\* (\*jña\*) possesses direct Yati affinity with both dental \*\*'న'\*\* (\*na\*) and retroflex \*\*'ణ'\*\* (\*ṇa\*)\[cite: 10\]:

  $$\\mathbf{‘జ్ఞ’} \\quad\\longleftrightarrow\\quad \\{\\mathbf{న,\\ ణ}\\}$$\[cite: 10\]

\* \*\*Etymological & Linguistic Rationale:\*\*

  1\. \*The Tadbhava Sound Law:\* In Prakritic evolution, Sanskrit words containing \*\*'జ్ఞ'\*\* systematically mutate into dental nasals (\*\*'న' / 'న్న'\*\*) in Telugu Tadbhavas\[cite: 10\]:

     \* \*యజ్ఞము $\\longrightarrow$ జన్నము\*\[cite: 10\]

     \* \*విజ్ఞానము $\\longrightarrow$ విన్నాణము\*\[cite: 10\]

     \* \*విజ్ఞాపనము $\\longrightarrow$ విన్నపము\*\[cite: 10\]

     \* \*సంజ్ఞ $\\longrightarrow$ సన్న\*\[cite: 10\]

     \* \*ఆజ్ఞ $\\longrightarrow$ ఆన / ఆనతి\*\[cite: 10\]

  2\. \*The Affinity Bridge:\* This pervasive lexical parentage (\*tadbhavavyājamu\*) establishes an acoustic bridge between \*\*'జ్ఞ'\*\* and \*\*'న'\*\*\[cite: 10\].

  3\. \*The Retroflex Extension:\* Under \*Sarasayati-1\* (6.13), dental \*\*'న'\*\* and retroflex \*\*'ణ'\*\* are equivalent; hence, \*\*'జ్ఞ'\*\* inherits full affinity with \*\*'ణ'\*\*\[cite: 10\].

\* \*\*Relation to Saṁyukta Yati:\*\* Standard \*Saṁyukta Yati\* permits matching 'జ్ఞ' via its constituent consonants \*\*'జ'\*\* or \*\*'ఞ'\*\*\[cite: 10\]. \*Tadbhavavyāja Yati\* is an extraordinary supplemental license that allows 'జ్ఞ' as a whole unit to match \*\*'న'\*\* and \*\*'ణ'\*\*\[cite: 10\].

\* \*\*Corpus Provenance (6.31, 6.31.1):\*\*

  \* \*Appakavīyamu Lakṣya-Lakṣaṇa (3-54):\* \*\*జ్ఞా $\\longleftrightarrow$ ణ\*\* in Line 3 (\*జ్ఞాని... శోణకర\*); \*\*జ్ఞా $\\longleftrightarrow$ న\*\* in Line 4 (\*జ్ఞాతి... నృపనాశన\*)\[cite: 10\].

  \* \*Pāvulūri Mallana Gaṇitam (Appakavīyamu 3-55):\* \*\*జ్ఞా $\\longleftrightarrow$ న\*\* (\*జ్ఞానులఁ బద్మగర్భ వదనంబులు నాలుగుఁ...\*)\[cite: 10\].

  \* \*\*జ్ఞా $\\longleftrightarrow$ న:\*\* \*జ్ఞానము గల్గియుండి భువనంబులఁ జూచుచునుండు వారికిన్...\* (\*Bhāratam\*, Udyōga 3-348)\[cite: 10\]; \*...మహోన్నతి దండెత్తి... యాజ్ఞాసిద్ధిఁగావించెఁదాన్...\* (\*Bhāratam\*, Sabhā 2-5-88)\[cite: 10\]; \*...ధనమిచ్చి పంప ముని యాజ్ఞాపించెఁ...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 294)\[cite: 10\].

  \* \*\*జ్ఞా $\\longleftrightarrow$ నా:\*\* \*...ప్రజ్ఞానిధులంచుఁ బేరుగనినారము...\* (\*Tirupati Vēṅkaṭa Kavulu Chāṭu\*)\[cite: 10\].

  \* \*\*జ్ఞ $\\longleftrightarrow$ ని:\*\* \*...యాజ్ఞకుఁడరణిన్ హుతాశనుని నిల్పినకైవడి...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 433)\[cite: 10\].

  \* \*\*ని $\\longleftrightarrow$ జ్ఞీ:\*\* \*నినుఁదానంపెడువేళనేమనియె రాజ్ఞిశ్రేష్ఠ...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 1460)\[cite: 10\].

  \* \*\*నీ $\\longleftrightarrow$ జ్ఞీ:\*\* \*నీమంబున్ మతిశుద్ధియున్ సకల రాజీత్వంబు...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Ayōdhyā 395)\[cite: 10\].

  \* \*\*జ్ఞే $\\longleftrightarrow$ నె:\*\* \*జ్ఞానస్వరూపమై... జ్ఞేయస్వరూపమై నెఱసి యుండు...\* (\*Bhāgavatam\* 7-53)\[cite: 10\].

  \* \*\*జ్ఞా $\\longleftrightarrow$ ణ:\*\* \*...సుజ్ఞానకులొడ్ల జన్మమరణంబులకుం దలకొందరెంతయున్...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 546)\[cite: 10\].

&nbsp;

\---

&nbsp;

\#\#\# 6.32 విశేష యతి (Viśēṣa Yati — 'Jña' to Velar Class Stops 'Ka, Kha, Ga, Gha')

&nbsp;

\* \*\*Definition & Mechanics:\*\* The Sanskrit palatal cluster \*\*'జ్ఞ'\*\* (\*jña\*) possesses licensed Yati affinity with the first four consonants of the \*\*velar class (\*Ka-varga\*)\*\*: \*\*'క, ఖ, గ, ఘ'\*\*\[cite: 10\]:

  $$\\mathbf{‘జ్ఞ’} \\quad\\longleftrightarrow\\quad \\{\\mathbf{క,\\ ఖ,\\ గ,\\ ఘ}\\}$$\[cite: 10\]

\* \*\*Linguistic Rationale & Phonetic Evolution (6.32.1):\*\*

  \* While orthographically $\\text{జ్} \+ \\text{ఞ}$, the cluster 'జ్ఞ' in spoken South Asian phonology and Telugu vernacular speech shifts into a velar glide: articulated as \*\*'గ' / 'గ్య'\*\* (\*jñānamu $\\rightarrow$ gēnamu / gyānamu\*; Hindi \*gyān\*)\[cite: 10\].

  \* In Telugu Tadbhavas, 'జ్ఞ' systematically mutates into velar stops:

    \* \*జ్ఞాపకము $\\longrightarrow$ గేపకము\*\[cite: 10\]

    \* \*ప్రజ్ఞ $\\longrightarrow$ పగ్గియ / పగ్గె\*\[cite: 10\]

    \* \*సంజ్ఞ $\\longrightarrow$ సైగ / సయిగ\*\[cite: 10\]

  \* This phonetic reality connects 'జ్ఞ' directly to \*\*'గ'\*\*\[cite: 10\]. Via \*Vargaja Yati\* (6.11), the affinity inherently expands across the entire velar stop series (\*\*క, ఖ, గ, ఘ\*\*)\[cite: 10\].

\* \*\*Textual Dispute: Tikkana's Stanza (6.32.1):\*\*

  \* Tikkana deployed this in \*Mahābhārata\* (Udyōga 4-255): \*జ్ఞానము గేవల కృపనజ్ఞానికినుపదేశవిధిఁ బ్రకాశము సేయం / గానది...\* (\*\*జ్ఞా $\\longleftrightarrow$ కా\*\*)\[cite: 10\].

  \* Later purists altered \*ప్రకాశము\* to \*ప్రజనితము\* to manufacture a standard \*\*జ్ఞా \[జా\] $\\longleftrightarrow$ జ\*\* match\[cite: 10\]. The text rejects this alteration as a clumsy corruption (\*kṛtaka-pāṭhamu\*); \*prakāśamu\* (illumination) is the authentic reading, and Tikkana's \*Viśēṣa Yati\* is fully canonical\[cite: 10\].

&nbsp;

\#\#\#\# Canonical Provenance for Viśēṣa Yati (6.32.2)

\* \*\*క $\\longleftrightarrow$ జ్ఞ:\*\* \*కనువిందై యభిషిక్తుఁడైన విభునాజ్ఞం గొల్వులో...\* (\*Allasāni Peddana\*, \*Satyāvadhū Praṇayamu\* / \*Lakṣaṇa Śirōmaṇi\* 4-67)\[cite: 10\]; \*కర్మమధర్మమజ్ఞానమాగడము...\* (\*Paṇḍitārādhya Caritra\*, Dvipada)\[cite: 10\].

\* \*\*కా $\\longleftrightarrow$ జ్ఞ:\*\* \*...చేసిన ప్రతిజ్ఞల్దీర్ప భీముండు...\* (\*Pāṇḍavōdyōgamu\*, Act 3)\[cite: 10\]; \*...శంకారాహిత్యముతో శిరోమణి యభిజ్ఞానార్థమర్పించినన్...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 3186)\[cite: 10\].

\* \*\*జ్ఞా $\\longleftrightarrow$ క:\*\* \*జ్ఞానేంద్రియజ్ఞాన కళలౌరుసౌరుగా...\* (\*Śivarātri Māhātmyamu\* 1-139)\[cite: 10\]; \*జ్ఞానపటాలయమ్మునొడికమ్ముగఁ గుట్టు ఖయాము...\* (\*Karuṇaśrī\*, \*Khayyām\* 112)\[cite: 10\]; \*జ్ఞానముగల్గునంత శ్రుతికర్మల సన్న్యసనంబొనర్పనజ్ఞానము...\* (\*Śrīpati Śatakam\* 86)\[cite: 10\].

\* \*\*జ్ఞా $\\longleftrightarrow$ కా:\*\* \*జ్ఞానానందమయుండె శిష్యజనరక్షాదీక్ష...\* (\*\*జ్ఞా $\\longleftrightarrow$ క్షా \[కా\]\*\*) (\*Ghaṭikācalamu\* 3-82)\[cite: 10\]; \*...మఱి కార్యము కర్మను వీడరాదటంచేనియున్...\* (\*Śrīpati Śatakam\* 86)\[cite: 10\].

\* \*\*జ్ఞా $\\longleftrightarrow$ ఖ:\*\* \*...జ్ఞానిక్షేపములీ ద్విజుండు రసవత్కావ్యైక...\* (\*Bhāratam\*, Sabhā 2-4-36)\[cite: 10\]; \*...తదాజ్ఞావిధి సూతుండు సమ్ముఖంబు ఘటించెన్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 1649)\[cite: 10\].

\* \*\*జ్ఞ $\\longleftrightarrow$ గ:\*\* \*...నాకునజ్ఞతయు జడత్వసంపదయుఁ గల్గుట...\* (\*Gōpīnātha Rāmāyaṇamu\*, Yuddha 469)\[cite: 10\].

\* \*\*జ్ఞా $\\longleftrightarrow$ గ:\*\* \*...ప్రజ్ఞానిధులైన పెద్దలు జగంబుల...\* (\*Gōpīnātha Rāmāyaṇamu\*, Sundara 1357)\[cite: 10\].

\* \*\*జ్ఞా $\\longleftrightarrow$ ఘ:\*\* \*జ్ఞాపకంబైనభంగినే ఘనుఁడు మనకు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 1396)\[cite: 10\].

&nbsp;

\---

&nbsp;

\#\#\# 6.33 మవర్ణ యతులు (Mavarṇa Yatulu — Pre-Nasalized Semivowels & Spirants to 'Ma')

&nbsp;

\* \*\*Definition & Mechanics:\*\* When semivowels (\*\*య, ర, ల, వ\*\*) or spirants (\*\*శ, ష, స, హ\*\*) are preceded by a full bindu (\*Pūrṇabindu\* / anusvāra), they acquire licensed Yati affinity with the bilabial nasal \*\*'మ'\*\* (\*ma\*)\[cite: 10\]:

  $$\\{\\mathbf{ంయ,\\ ంర,\\ ంల,\\ ంవ,\\ ంశ,\\ ంష,\\ ంస,\\ ంహ}\\} \\quad\\longleftrightarrow\\quad \\mathbf{మ}$$\[cite: 10\]

\* \*\*Nomenclature:\*\* Termed \*\*మవర్ణ విరామములు\*\* (\*Mavarṇa Virāmamulu\*) by Appakavi, and \*\*మా వడి\*\* (\*Mā-vaḍi\*) in \*Sulakṣaṇasāramu\*\[cite: 10\].

\* \*\*Pāṇinian & Phonetic Rationale (6.33.1):\*\*

  \* By Pāṇini (8-3-23: \*Mō'nusvāraḥ\*), a word-final \*\*'మ్'\*\* transforms into an anusvāra before any consonant ($\\text{హరిమ్} \+ \\text{వన్దే} \= \\text{హరింవన్దే}$)\[cite: 10\].

  \* When an anusvāra precedes semivowels or spirants in Sanskrit pronunciation, it acoustically resonates as a labial nasal nasalization (\*సమ్యమి\* for \*సంయమి\*)\[cite: 10\].

  \* Treating this resonant bindu as an underlying labial nasal ($\\text{మ్}$) licenses the entire cluster to rhyme with consonant \*\*'మ'\*\* under the \*Saṁyukta Yati\* principle\[cite: 10\].

&nbsp;

&nbsp;

             Mavarṇa Yati Permutation Set

Anusvāra-Preceded Semivowels:   { ంయ,  ంర,  ంల,  ంవ } ──┐

                                                       ├──\> Alliterate with 'మ'

Anusvāra-Preceded Spirants:     { ంశ,  ంష,  ంస,  ంహ } ──┘

&nbsp;

&nbsp;

\#\#\#\# Canonical Attestations & Provenance (6.33.2 – 6.33.3)

\* \*\*Appakavi's Complete Lakṣya-Lakṣaṇa Stanza (3-76):\*\*

  \* Line 1: \*\*మ $\\longleftrightarrow$ ంయ\*\* (\*మర్దిత... సంయమి\*); \*\*మ $\\longleftrightarrow$ ంర\*\* (\*మహిత... సంరక్షిత\*)\[cite: 10\].

  \* Line 2: \*\*మా $\\longleftrightarrow$ ంల\*\* (\*మాయా... సంలబ్ధ\*); \*\*మ $\\longleftrightarrow$ ంవ\*\* (\*మణిహార... వశంవద\*)\[cite: 10\].

  \* Line 3: \*\*మ $\\longleftrightarrow$ ంశ\*\* (\*మందర... వంశ\*); \*\*మా $\\longleftrightarrow$ ంష\*\* (\*మాభూప... పుంషండ\*)\[cite: 10\].

  \* Line 4: \*\*మ $\\longleftrightarrow$ ంస\*\* (\*మంజుల... కంస\*); \*\*స్మ \[మ\] $\\longleftrightarrow$ ంహ\*\* (\*స్మర... సింహ\*)\[cite: 10\].

\* \*\*Earlier Treatise Attestations:\*\*

  \* \*Vēmulavāḍa Bhīmakavi Chāṭu (Appakavi 3-77):\* \*\*ంహ $\\longleftrightarrow$ మై\*\* (\*...వీర సంహరణ... మైలము భీమన...\*)\[cite: 10\].

  \* \*Chandodarpaṇamu (1-117 / Appakavi 3-78):\* \*\*మా $\\longleftrightarrow$ ంయ\*\* (\*మారుతాత్మజుఁడరిది సంయమి...\*); \*\*మ $\\longleftrightarrow$ ంహా\*\* (\*మదనజనకుఁడు దనుజసంహరుఁడనంగ...\*)\[cite: 10\].

  \* \*Sulakṣaṇasāramu (Daśakumāra Caritra 2-114):\* \*\*ంయ $\\longleftrightarrow$ మా\*\* (\*...సంయమివర్యులఁ జూచి రాకుమారకులెల్లన్...\*)\[cite: 10\].

\* \*\*Extended Classical Corpus:\*\*

  \* \*\*ంశో $\\longleftrightarrow$ మో (or ంలో $\\longleftrightarrow$ మో):\*\* \*సంశ్లోకింపన్ సతులున్ బతుల్ మిగుల సమ్మోదింప...\* (\*Bhāgavatam\* 8-486)\[cite: 10\].

  \* \*\*మా $\\longleftrightarrow$ ంశ:\*\* \*మాటన్నిల్పఁగఁ దీర్చుచుంటి రఘువంశంబిట్టి...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Ayōdhyā 439)\[cite: 10\].

  \* \*\*మ $\\longleftrightarrow$ ంసా:\*\* \*మర్యాదాప్రియమైన నా యెడఁద హంసా యెప్పుడేనీ...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Yuddha 40)\[cite: 10\].

  \* \*\*మ $\\longleftrightarrow$ ంహ:\*\* \*మణికిరీటము త్రిపుర సంహరుని పాద...\* (\*Bhāgavatam\* 10-4-319)\[cite: 10\]; \*మదకుంభీనస రోషులుజ్జ్వలిత సింహప్రోజ్జ్వలుల్...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 413)\[cite: 10\].

  \* \*\*మ్ \[మ\] $\\longleftrightarrow$ ంహ:\*\* \*...నెమ్మదిలోఁ బాడుకొనంగ నేఁదగుదునంహశ్ఛేదకా...\* (\*Śrīpati Śatakam\* 5)\[cite: 10\].

  \* \*\*మీ $\\longleftrightarrow$ ంహి:\*\* \*మీమాంసాగమ వజ్రపంజరము బంహిష్ఠార్థ నిక్షేపము...\* (\*Haravilāsam\* 4-8)\[cite: 10\].

&nbsp;

\---

&nbsp;

\#\#\# 6.34 అంత్యోష్మసంధి యతి (Antyōṣmasandhi Yati — Word-Boundary Stop \+ 'Ha' Morphophonemic Yati)

&nbsp;

\* \*\*Definition & Mechanics:\*\* When an unvoiced stop (\*\*క్, ట్, త్, ప్\*\*) encounters glottal aspirate \*\*'హ'\*\* (\*ha\* — the final spirant / \*antyōṣmamu\*) across a Sanskrit compound boundary, morphophonemic mutation produces an aspirated media cluster (\*\*గ్ఘ, డ్ఢ, ద్ధ, బ్భ\*\*)\[cite: 10\]. At this compound coordinate, the poet is granted an extraordinary license to \*\*ignore the surface stop cluster and rhyme directly with the underlying original 'హ' (Ha)\*\*\[cite: 10\]\!

\* \*\*Nomenclature:\*\* Named \*\*అంత్యోష్మ సంధి వడి\*\* by Appakavi, and \*\*వికల్పయతి\*\* by Anantudu (\*Chandodarpaṇamu\* 1-124)\[cite: 10\].

\* \*\*Pāṇinian Derivation Architecture (Pūrvasavarṇādēśa 6.34.1):\*\*

  Governed by Pāṇini (8-4-62: \*Jhayō hō'nyatarasyām\*)\[cite: 10\]:

  1\. \*Stop Mutation:\* An unvoiced stop before 'హ' softens into its voiced counterpart (\*\*గ్, డ్, ద్, బ్\*\*)\[cite: 10\].

  2\. \*Spirant Mutation:\* The following 'హ' optionally assimilates into the 4th consonant (aspirated voiced stop) of that class (\*\*ఘ, ఢ, ధ, భ\*\*)\[cite: 10\].

  3\. \*Dual Surface Doublets:\*

     \* $\\text{వాక్} \+ \\text{హరి} \\longrightarrow \\mathbf{వాగ్ఘరి}$ (assimilated) or $\\mathbf{వాగ్హరి}$ (unassimilated)\[cite: 10\].

     \* $\\text{జగత్} \+ \\text{హిత} \\longrightarrow \\mathbf{జగద్ధిత}$ (assimilated) or $\\mathbf{జగద్హిత}$ (unassimilated)\[cite: 10\].

     \* $\\text{ఉద్} \+ \\text{హత} \\longrightarrow \\mathbf{ఉద్ధత}$ (assimilated) or $\\mathbf{ఉద్హత}$ (unassimilated)\[cite: 10\].

     \* $\\text{కకుప్} \+ \\text{హస్తి} \\longrightarrow \\mathbf{కకుబ్భస్తి}$\[cite: 10\].

\* \*\*The Metrical Duality:\*\*

  \* \*Option A (Surface Class Yati):\* Rhyme on the surface dental/labial stop (e.g., in \*\*ఉద్ధతి\*\*, matching \*\*ద\*\* or \*\*ధ\*\* via \*Vargaja\*)\[cite: 10\].

  \* \*Option B (Antyōṣmasandhi License):\* Rhyme on the underlying radical \*\*'హ'\*\* (\*ha\*)\[cite: 10\]. Because \*\*వాగ్హరి\*\* contains a literal 'హ', writing the canonical assimilated form \*\*వాగ్ఘరి\*\* legally preserves alliterative access to \*\*'హ'\*\*\[cite: 10\]\!

&nbsp;

&nbsp;

              Antyōṣmasandhi Dual Yati Parsing

           \[ Compound Site: e.g., ఉద్ \+ హతి \= ఉద్ధతి \]

                                │

    ┌───────────────────────────┴───────────────────────────┐

    ▼                                                       ▼

&nbsp;

Option A: Surface Stop Scansion                 Option B: Antyōṣmasandhi Yati Extracts surface 'ద' or 'ధ'                     Ignores dental stops entirely; • ద్ధ ⟷ ధా (Vargaja Yati)                      reaches underlying radical 'హ' (e.g., Bhāskara Rāmāyaṇa, Araṇya 405\)         • ద్ధ ⟷ ఆ (via A-Ha Sarasayati 6.18) (e.g., Bhāskara Rāmāyaṇa, Kiṣkindha 633\)

&nbsp;

\#\#\#\# Canonical Attestations & Provenance Trail (6.34.2 – 6.34.3)

\* \*\*Appakavi's Complete Lakṣya-Lakṣaṇa Stanza (3-115):\*\*

  \* Line 1: \*\*కై $\\longleftrightarrow$ కామధుగ్ధర\*\* (Option A: \*Vargaja\* via \*\*గ్ఘ\*\*); \*\*హై $\\longleftrightarrow$ వాగ్హంస\*\* (Option B: \*Antyōṣma\* via \*\*హ\*\*)\[cite: 10\].

  \* Line 2: \*\*డి $\\longleftrightarrow$ రాడ్డిమ\*\* (Option A: \*Vargaja\* via \*\*డ్ఢ\*\*); \*\*హ $\\longleftrightarrow$ అంబురుడ్డరి\*\* (Option B: \*Antyōṣma\* via \*\*హ\*\*)\[cite: 10\].

  \* Line 3: \*\*దే $\\longleftrightarrow$ సరిద్ధీర\*\* (Option A: \*Vargaja\* via \*\*ద్ధ\*\*); \*\*హ $\\longleftrightarrow$ ఏణభృద్ధాదినీ\*\* (Option B: \*Antyōṣma\* via \*\*హ\*\*)\[cite: 10\].

  \* Line 4: \*\*పా $\\longleftrightarrow$ కకుబ్బస్తి\*\* (Option A: \*Vargaja\* via \*\*బ్భ\*\*); \*\*హ $\\longleftrightarrow$ శారదాబ్భయ\*\* (Option B: \*Antyōṣma\* via \*\*హ\*\*)\[cite: 10\].

\* \*\*Anantudu's Chandodarpaṇamu (1-124 — "Vikalpa Yati"):\*\*

  \* Line 2 uses Option A: \*\*దే $\\longleftrightarrow$ జగద్ధిత\*\* (\*\*దే $\\longleftrightarrow$ ది/ధి\*\*)\[cite: 10\].

  \* Line 3 uses Option B: \*\*హ $\\longleftrightarrow$ ఉద్ధతుఁడు\*\* (\*\*హ $\\longleftrightarrow$ హ\*\*)\[cite: 10\].

  \* Line 4 uses Option B: \*\*అ $\\longleftrightarrow$ కకుబ్బస్తులు\*\* (\*\*అ $\\longleftrightarrow$ హ\*\* via \*Sarasayati\*)\[cite: 10\].

\* \*\*Extended Classical Corpus for Option B (Underlying 'Ha' Matches):\*\*

  \* \*\*ద్ధ $\\longleftrightarrow$ అ (via A-Ha Sarasayati):\*\* \*...హరిద్ధయు మేనంబొలుచు దీప్తులట్టుల...\* ($\\text{హరిత్} \+ \\text{హయు} \\rightarrow \\mathbf{ద్ధ} \\longleftrightarrow \\mathbf{అ}$ in \*దీప్తులు \+ అట్టుల\*) (\*Bhāgavatam\* 6-10-78)\[cite: 10\].

  \* \*\*ద్ఘ $\\longleftrightarrow$ అ (via A-Ha Sarasayati):\*\* \*...ద్విజుండు దద్ఘాటకమిచ్చి కైకొనియెనద్ది...\* ($\\text{తత్} \+ \\text{హాటకము} \\rightarrow \\mathbf{ద్ఘ} \\longleftrightarrow \\mathbf{అ}$ in \*కైకొనియెన్ \+ అద్ది\*) (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 397)\[cite: 10\].

  \* \*\*ద్ధ $\\longleftrightarrow$ ఆ (via A-Ha Sarasayati):\*\* \*...సముద్ధతులం బర్వత భేదనప్రబల వజ్రాభీల...\* ($\\text{ఉద్} \+ \\text{హతులన్} \\rightarrow \\mathbf{ద్ధ} \\longleftrightarrow \\mathbf{ఆ}$ in \*వజ్ర \+ ఆభీల\*) (\*Bhāskara Rāmāyaṇamu\*, Bāla 406)\[cite: 10\]; \*...ధాత్రినుద్ధరణమొనర్చినట్టి నినునాదివరాహము...\* ($\\text{ఉత్} \+ \\text{హరణ} \\rightarrow \\mathbf{ద్ధ} \\longleftrightarrow \\mathbf{ఆ}$ in \*నినున్ \+ ఆది\*) (\*Manu Caritra\* 6-109)\[cite: 10\].

  \* \*\*ద్ధ $\\longleftrightarrow$ యా (via R̥ju Yati 6.16):\*\* \*...వ్యూహనోద్ధతిమై తాఁకినఁ గృష్ణుఁడుం బటు భుజవ్యాఘాత...\* ($\\text{ఉద్} \+ \\text{హతి} \\rightarrow \\mathbf{ద్ధ\\ \[హ\]} \\longleftrightarrow \\mathbf{యా}$ in \*వ్యాఘాత\*) (\*Harivaṁśamu\* 3-187)\[cite: 10\].

  \* \*\*హ $\\longleftrightarrow$ ద్ధ \[హ\] (Prāṇi Yati):\*\* \*హరివీరభట మహోద్ధతినబ్ధి గంపింప...\* ($\\text{మహా} \+ \\text{ఉద్} \+ \\text{హతిన్}$)\[cite: 10\]; \*...తద్ధాహాకారములెంతగా బలియునో హాస్యంబు...\* ($\\text{తత్} \+ \\text{హాహాకార} \\rightarrow \\mathbf{ద్ధా\\ \[హా\]} \\longleftrightarrow \\mathbf{హ}$)\[cite: 10\].

  \* \*\*గ్ఘ $\\longleftrightarrow$ హా (Prāṇi Yati):\*\* \*...వాగ్ఘైమాలంకరణద్విపోత్సవము ముఖాహ్లాదంబులీఁజేయు...\* ($\\text{వాక్} \+ \\text{హైమ} \\rightarrow \\mathbf{గ్ఘై\\ \[హై\]} \\longleftrightarrow \\mathbf{హా}$ in \*ఆహ్లాద\*) (\*Kopparapu Kavulu\*, p. 293)\[cite: 10\].

  \* \*\*ఏ $\\longleftrightarrow$ ద్ధి \[హి\] (via A-Ha Sarasayati):\*\* \*...దైవమేను వాఙ్మనఃక్రియలఁదద్ధితమ యెపుడు...\* ($\\text{తత్} \+ \\text{హితమ} \\rightarrow \\mathbf{ద్ధి\\ \[హి\]} \\longleftrightarrow \\mathbf{ఏ}$ in \*దైవము \+ ఏను\*) (\*Bhāratam\*, Āraṇya 5-21)\[cite: 10\].

  \* \*\*ఋ $\\longleftrightarrow$ ద్ధ్రీ \[హ్రీ\] (via R̥-Yati / Sarasayati):\*\* \*ఋభులోకంబులు తల్లడిల్లె భయసద్ధ్రీచీనముల్...\* ($\\text{సత్} \+ \\text{హ్రీచీనముల్} \\rightarrow \\mathbf{ద్ధ్రీ\\ \[హ్రీ\]} \\longleftrightarrow \\mathbf{ఋ}$)\[cite: 10\].

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**6.35 వికల్ప యతి (Vikalpa Yati — Optional Sandhi-Derived Caesura)**

* **Definition:** When an unvoiced class stop (**క్, చ్, ట్, త్, ప్**) is followed by a nasal stop (**న్** or **మ్**) across a Sanskrit compound boundary, it optionally assimilates into its class nasal (**ఙ, ఞ, ణ, న, మ**) or its class media (**గ్, జ్, డ్, ద్, బ్**) via *Anunāsika Sandhi*. At this compound junction, the poet is licensed to match the caesura (*yati-sthāna*) in three alternative ways:  
1. **Option A (ఆదేశ అనునాసికాక్షరము):** Match the resulting substituted nasal stop (**ఙ, ఞ, ణ, న, మ**).  
2. **Option B (సంధికి పూర్వమున్న వర్గాక్షరము):** Match the underlying pre-sandhi class stop (**క, చ, ట, త, ప**).  
3. **Option C (సంయుక్త యతి):** Match the initial consonant of the second word (**న** or **మ**) under standard *Saṁyukta Yati* (Section 6.26).  
* **Nomenclature:** Termed **వికల్ప విరమణము** (*Vikalpa Viramaṇamu*) by Appakavi, and **యుక్త వికల్పయతి** (*Yukta Vikalpayati*) by Anantudu (*Chandodarpaṇamu* 1-125).  
* **Grammatical Rationale:** In Sanskrit grammar, Anunāsika Sandhi produces valid alternative doublets (e.g., *సన్మార్గము / సద్మార్గము*; *వాజ్నియమము / వాగ్నియమము*; *దృఙ్మధు / దృగ్మధు*; *గోత్రభిన్మణి / గోత్రభిద్మణి*). In standard usage, the nasal-assimilated form (*సన్మార్గ*) is preferred. Because the unassimilated media form (*సద్మార్గ*) permits rhyming on **'ద'** (and therefore on **'త'** via *Vargaja Yati*), writing the canonical assimilated form **సన్మార్గ** legally preserves alliterative access to **'త'**.

                 Vikalpa Yati Triple-Resolution Logic

          \[ Compound Junction: e.g., సత్ \+ మార్గ \= సన్మార్గ \]

                                   │

      ┌────────────────────────────┼────────────────────────────┐

      ▼                            ▼                            ▼

 Option A: Nasal Match        Option B: Stop Match        Option C: Word-2 Initial

  Extracts surface 'న'       Reaches pre-sandhi 'త'         Extracts surface 'మ'

  • న్మా ⟷ న (Prāṇi)          • న్మా ⟷ ద/ధ (Vargaja)         • న్మా ⟷ మ (Prāṇi)

  (Appakavi 3-117, Line 1\)   (Appakavi 3-117, Line 2\)      (Kāśīkhaṇḍam 5-168)

\`\`\`\[cite: 11\]

&nbsp;

\* \*\*Strict Negative Constraint — Maya(ṭ) & Mātra(c) Suffixes (6.35.5):\*\*

  \* When Anunāsika Sandhi occurs before nominal suffixes like \*-maya(ṭ)\* or \*-mātra(c)\* (\*చిత్ \+ మయ \= చిన్మయ\*; \*తత్ \+ మాత్ర \= తన్మాత్ర\*), sandhi is \*\*obligatory (\*nitya\*)\*\*, producing no optional stop doublets (forms like \*\\\*చిద్మయ\* or \*\\\*తద్మాత్ర\* are ungrammatical)\[cite: 11\].

  \* \*\*Engine Rule:\*\* For words formed with \*-maya\* or \*-mātra\*, \*\*Option B is strictly barred\*\*\[cite: 11\]. The poet cannot rhyme on the pre-sandhi stop (\*\*'త'\*\*)\[cite: 11\]. Caesuras on \*చిన్మయ\* or \*తన్మాత్ర\* must resolve strictly under Option A (\*\*న\*\*) or Option C (\*\*మ\*\*)\[cite: 11\].

&nbsp;

\*\*Corpus Provenance for Vikalpa Yati (6.35.1 – 6.35.6)\*\*

\* \*\*Treatise Benchmark Stanzas:\*\*

  \* \*Appakavīyamu (3-117):\*

    \* Line 1 uses Option A: \*\*న $\\longleftrightarrow$ గూఢపాన్మద\*\* ($\\text{గూఢపాత్} \+ \\text{మద} \\rightarrow \\mathbf{న \\longleftrightarrow న}$)\[cite: 11\].

    \* Line 2 uses Option B: \*\*ద $\\longleftrightarrow$ గోత్రభిన్మణి\*\* ($\\text{గోత్రభిత్} \+ \\text{మణి} \\rightarrow \\mathbf{ద \\longleftrightarrow త}$ via \*Vargaja\*)\[cite: 11\].

    \* Line 3 uses Option A: \*\*నా $\\longleftrightarrow$ సన్మార్గ\*\* ($\\text{సత్} \+ \\text{మార్గ} \\rightarrow \\mathbf{నా \\longleftrightarrow న}$)\[cite: 11\].

    \* Line 4 uses Option B: \*\*ధా $\\longleftrightarrow$ హృన్మధ్య\*\* ($\\text{హృత్} \+ \\text{మధ్య} \\rightarrow \\mathbf{ధా \\longleftrightarrow త}$ via \*Vargaja\*)\[cite: 11\].

  \* \*Chandodarpaṇamu (1-125 — Anantudu):\*

    \* Line 3 uses Option B: \*\*గ $\\longleftrightarrow$ దృఙ్మధు\*\* ($\\text{దృక్} \+ \\text{మధు} \\rightarrow \\mathbf{గ \\longleftrightarrow క}$ via \*Vargaja\*)\[cite: 11\].

    \* Line 4 uses Option B: \*\*గ $\\longleftrightarrow$ దిఙ్మహిత\*\* ($\\text{దిక్} \+ \\text{మహిత} \\rightarrow \\mathbf{గ \\longleftrightarrow క}$ via \*Vargaja\*)\[cite: 11\].

\* \*\*Option B: Pre-Sandhi Radical Stop Matches:\*\*

  \* \*\*క $\\longleftrightarrow$ ద్రాఙ్మద \[క\]:\*\* \*...ద్రాఙ్మదవన్మందేహ దేహక్షరదురుతర...\* ($\\text{ద్రాక్} \+ \\text{మద}$) (\*Vaijayantīvilāsamu\* 2-52)\[cite: 11\].

  \* \*\*గా $\\longleftrightarrow$ వాఙ్మానస \[కా\]:\*\* \*...వాఙ్మానసములు సునియతములు గావింతురు...\* ($\\text{వాక్} \+ \\text{మానస}$) (\*Bhāratam\*, Śānti 5-90)\[cite: 11\].

  \* \*\*గా $\\longleftrightarrow$ దిఙ్నారుల \[కా\]:\*\* \*...దిఙ్నారుల తారహారములుగాఁదలఁపించె...\* ($\\text{దిక్} \+ \\text{నారీ}$) (\*Rāmābhyudayam\* 6-16)\[cite: 11\].

  \* \*\*ధా $\\longleftrightarrow$ భవన్నయన \[త\]:\*\* \*...భవన్నయనజ్వాలలలో జరామరణబాధా...\* ($\\text{భవత్} \+ \\text{నయన}$) (\*Agnidhāra\*, Sandhyālaya Mūrti)\[cite: 11\].

  \* \*\*తే $\\longleftrightarrow$ సరిన్నికట \[తి\]:\*\* \*...సరిన్నికటానేక విహార దేశముల దైతేయేంద్ర...\* ($\\text{సరిత్} \+ \\text{నికట}$) (\*Appakavīyamu\* 3-118 / \*Uttara Harivaṁśamu\* 5-48)\[cite: 11\].

\* \*\*Option A: Substituted Nasal Matches:\*\*

  \* \*\*న $\\longleftrightarrow$ ఉన్మద \[న\]:\*\* \*...రాజన్యుఁడున్మద లీలం బయినట్లు...\* ($\\text{ఉద్/త్} \+ \\text{మద}$) (\*Bhāratam\*, Śalya 2-317)\[cite: 11\].

  \* \*\*నా $\\longleftrightarrow$ తన్మహనీయ \[న\]:\*\* \*...తన్మహనీయస్థితి మూలమై నిలువ శ్రీనాథుండు...\* ($\\text{తత్} \+ \\text{మహనీయ}$) (\*Manu Caritra\* 1-10)\[cite: 11\].

  \* \*\*ండ $\\longleftrightarrow$ ఉన్మాదుల్ \[నా\] (Anunāsikākṣara):\*\* \*...బుద్ధిజాడ్య జనితోన్మాదుల్ గదా శ్రోత్రియుల్...\* ($\\text{ఉద్/త్} \+ \\text{మాద}$) (\*Appakavīyamu\* 3-119 / \*Manu Caritra\* 2-16)\[cite: 11\].

  \* \*\*ని $\\longleftrightarrow$ చరన్మృగ \[న\]:\*\* \*...చరన్మృగనాభి సౌరభ్య నిర్భరములు...\* ($\\text{చరత్} \+ \\text{మృగ}$) (\*Manu Caritra\* 5-102)\[cite: 11\].

\* \*\*Sufﬁx \-Maya Demonstrations (Restricted to Nasals):\*\*

  \* \*\*న $\\longleftrightarrow$ చిన్మయ \[న\]:\*\* \*నలినలోచను మేను చిన్మయమనంగ...\* (\*Appakavīyamu\* 3-120)\[cite: 11\].

  \* \*\*తన్మయుఁడై \[న\] $\\longleftrightarrow$ న్బా \[నా\]:\*\* \*...తన్మయుఁడై బ్రహ్మముభాతి బాలుఁడమరున్...\* (\*Bhāgavatam\* 10-Pūrvabhāga 194)\[cite: 11\].

\* \*\*Option C: Saṁyukta Yati on Second Word's Initial Consonant:\*\*

  \* \*\*న $\\longleftrightarrow$ వాజ్నైపుణ \[నై\]:\*\* \*నగుచు భావించిరతని వాజ్నైపుణములు...\* (\*Kāśīkhaṇḍam\* 3-63)\[cite: 11\].

  \* \*\*మ $\\longleftrightarrow$ ఋఙ్మంత్ర \[మ\]:\*\* \*...సామిధేని ఋఙ్మంత్రములుచ్చరించుచు సమగ్రతర...\* (\*Kāśīkhaṇḍam\* 5-303)\[cite: 11\].

  \* \*\*మ $\\longleftrightarrow$ అసన్మార్గంబు \[మా\]:\*\* \*మలయంబెక్కడ కాశీ యెక్కడ యసన్మార్గంబు...\* (\*Kāśīkhaṇḍam\* 5-168)\[cite: 11\].

  \* \*\*మా $\\longleftrightarrow$ మన్మందిరము \[మ\]:\*\* \*...మన్మందిరము పవిత్రమయ్యె మాన్యుఁడ నైతిన్...\* (\*Haravilāsam\* 1-61)\[cite: 11\].

  \* \*\*మం $\\longleftrightarrow$ దృఙ్మాన్యుఁడు \[మా\]:\*\* \*...దృఙ్మాన్యుఁడు మాన్యకీర్తి మహిమం దనరెం...\* (\*Bhāgavatam\* 9-674)\[cite: 11\].

  \* \*\*సమిద్ధ \[మీ\] $\\longleftrightarrow$ ఉన్మీలిత \[మీ\]:\*\* \*...ఉన్మీలిత బర్హదామము సమిద్ధ మహేంద్ర...\* (\*Harivaṁśamu\*, Pūrva 6-118)\[cite: 11\].

  \* \*\*సమేత \[మే\] $\\longleftrightarrow$ దృజ్మీలన \[మీ\]:\*\* \*...దృజ్మీలనమైందవామృత సమేత...\* (\*Kāśīkhaṇḍam\* 4-64)\[cite: 11\].

&nbsp;

\---

&nbsp;

\*\*6.36 ప్రత్యేక యతి (Pratyēka Yati — Demonstrative Compound Consonant Invariance)\*\*

&nbsp;

\* \*\*Definition:\*\* In Telugu compounding, when demonstrative pronouns \*\*అది\*\* (\*adi\*) or \*\*అవి\*\* (\*avi\*) fuse with an oblique or inflected base ending in \*-i, \-ti, \-ni\* or vowel bases (e.g., \*చేయి \+ యొక్క \+ అది $\\rightarrow$ చేతి \+ అది\*), the initial short vowel \*\*'అ'\*\* of \*అది / అవి\* optionally elides by \*Bāla Vyākaraṇam\* (Sandhi 45: \*"అది అవి శబ్దంబుల యత్తునకు వృత్తిని లోపంబు బహుళంబుగనగు"\*)\[cite: 11\]:

  \* \*\*Form 1 (Elided Compound / వృత్తిలోపము):\*\* $\\text{చేతి} \+ \\text{ది} \= \\mathbf{చేతిది}$; $\\text{నా} \+ \\text{ది} \= \\mathbf{నాది}$; $\\text{నీ} \+ \\text{ది} \= \\mathbf{నీది}$; $\\text{దాని} \+ \\text{ది} \= \\mathbf{దానిది}$; $\\text{అట్టి} \+ \\text{ది} \= \\mathbf{అట్టిది}$; $\\text{మంచి} \+ \\text{ది} \= \\mathbf{మంచిది}$\[cite: 11\].

  \* \*\*Form 2 (Unelided with Hiatus-Glide / యడాగమము):\*\* $\\text{చేతి} \+ \\text{య్} \+ \\text{అది} \= \\mathbf{చేతియది}$; $\\text{నా} \+ \\text{య్} \+ \\text{అది} \= \\mathbf{నాయది}$\[cite: 11\].

\* \*\*The Core Structural Rule:\*\* When the elided form (\*\*చేతిది, నాది, అట్టిది, దానిది\*\*) sits at the caesura, \*\*Yati MUST be executed strictly as a CONSONANT YATI on the resulting surface consonant ('తి', 'ది', 'ట్టి', etc.)\*\*\[cite: 11\]. The poet \*\*CANNOT rhyme with the elided vowel 'అ'\*\*\[cite: 11\]\!

\* \*\*Hiatus Form Handling:\*\* If the poet writes the unelided form (\*\*చేతియది, నాయది\*\*), the glide cluster \*\*'య'\*\* ($\\text{య్} \+ \\text{అ}$) naturally resolves to vowel \*\*'అ'\*\* under \*Svara-Pradhāna\* (Section 6.3) or \*Sarasayati\* (Section 6.17)\[cite: 11\].

\* \*\*Theoretical Rationale (6.36.2):\*\* Unlike \*Svara-Pradhāna\* (where vowels merge into guṇa/vṛddhi and retain alliterative rights), the elision of \*'a'\* in \*చేతిది\* is not a phonetic vowel-sandhi\[cite: 11\]. It is a grammatical compound-formation deletion (\*vṛtti-lōpamu\*)\[cite: 11\]. The vowel \*'a'\* is entirely extinguished; hence, granting it ghost-vowel Yati access is impermissible\[cite: 11\]. Appakavi codified \*Pratyēka Yati\* specifically to prevent poets from erroneously applying \*Svara-Pradhāna Yati\* to these elided forms\[cite: 11\].

&nbsp;

\*\*Corpus Provenance for Pratyēka Yati (6.36, 6.36.3)\*\*

\* \*\*Treatise Formulations:\*\*

  \* \*Appakavīyamu (3-80):\*

    \* Line 3 uses Hiatus Form: \*...హరిచేతియదియు నాఁగ\* ($\\text{న్} \+ \\text{అరయ} \\longleftrightarrow \\text{య్} \+ \\mathbf{అది} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati)\[cite: 11\].

    \* Line 4 uses Elided Form: \*...శూలి చేతిది యనంగ\* (\*\*ది $\\longleftrightarrow$ చేతిది \[తి\]\*\* $\\implies \\mathbf{ది \\longleftrightarrow తి}$ Vargaja Yati on consonant stop)\[cite: 11\].

  \* \*Chandodarpaṇamu (1-123 — Anantudu, under Bhinna Yati):\*

    \* \*దివిజవిభవంబు శౌరిచేతిది యనంగ\* (\*\*ది $\\longleftrightarrow$ తి\*\* Consonant Yati)\[cite: 11\].

    \* \*నసురనాశంబు హరిచేతియది యనంగ\* ($\\text{న్} \+ \\text{అసుర} \\longleftrightarrow \\text{య్} \+ \\text{అది} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati)\[cite: 11\].

\* \*\*Classical Corpus Proof (Surface Consonants Matched):\*\*

  \* \*\*దానిది \[ని\] $\\longleftrightarrow$ నీ:\*\* \*...కలరూపెఱుంగనవనీపతి... దానిది...\* ($\\text{దాని} \+ \\text{అది} \= \\text{దానిది}$; matches \*\*ని $\\longleftrightarrow$ నీ\*\* via \*Prāṇi Yati\*, NOT with 'a'\!) (\*Bhāratam\*, Ādi 4-30)\[cite: 11\].

  \* \*\*అట్టిది \[ట్టి/టి\] $\\longleftrightarrow$ ఘటించిన \[టి\]:\*\* \*...ధర్మము వల్కరేనినట్టిదియును ధర్మువే తగ ఘటించిన...\* ($\\text{అట్టి} \+ \\text{అది} \= \\text{అట్టిది}$; matches \*\*టి $\\longleftrightarrow$ టి\*\* via \*Prāṇi Yati\*, NOT with 'a'\!) (\*Bhāratam\*, Udyōga 2-70)\[cite: 11\].

\* \*\*Disambiguation — 'Unnadi / Unnavi' Stems (6.36.4):\*\* Forms like \*ఉన్నది, ఉన్నవి\* do not fall under \*Pratyēka Yati\*; they are formed via \*Atva Sandhi\* ($\\text{ఉన్న} \+ \\text{అది} \= \\text{ఉన్నది}$) and are governed by \*Dēśya Nitya Samāsa Yati\* (Section 6.49.7)\[cite: 11\].

&nbsp;

\---

&nbsp;

\*\*6.37 ఏకతర యతులు (Ēkatara Yatulu — Strict Solitary Self-Identity for Liquids 'Ra' and 'Ṟa')\*\*

&nbsp;

\* \*\*Definition:\*\*

  1\. Soft liquid \*\*'ర'\*\* (\*Sādhu Rēpha\* / \*Laghu Rēpha\*) alliterates \*\*strictly and exclusively with 'ర'\*\*\[cite: 11\].

  2\. Hard trill \*\*'ఱ'\*\* (\*Śakaṭa Rēpha\* / \*Alaghu Rēpha\*) alliterates \*\*strictly and exclusively with 'ఱ'\*\*\[cite: 11\].

  3\. The two liquids \*\*NEVER rhyme with each other\*\* ($\\mathbf{ర \\neq ఱ}$), nor do they rhyme with any other consonant stop, semivowel, or sibilant\[cite: 11\].

\* \*\*Nomenclature:\*\* Termed \*\*ఏకతర యతులు\*\* (\*Ēkatara Yatulu\* \= Solitary/Single-Option Yatis) by Appakavi\[cite: 11\], and \*\*ఎక్కటియతి\*\* (\*Ekkaṭi Yati\*) by earlier prosodists\[cite: 11\].

\* \*\*Distinction from Standard Prāṇi Yati (6.37.1):\*\*

  \* Under \*Prāṇi Yati\* (Section 6.10), all consonants match themselves (క-క, ప-ప, etc.), but they also participate in broader consonant groupings (e.g., క with ఖ, గ, ఘ; ప with ఫ, బ, భ, వ; శ with ష, స, చ, జ)\[cite: 11\].

  \* \*\*'ర'\*\* and \*\*'ఱ'\*\* are the \*\*only two consonants in Telugu prosody completely devoid of any consonant-class family\*\*\[cite: 11\]. They admit zero cross-consonant bridges\[cite: 11\]. (Soft 'ర' pairs with the vocalic vowel 'ఋ' under \*R̥ Yati\* \[6.5\], but among consonants it remains completely solitary)\[cite: 11\].

\* \*\*Vowel Partitioning Grid:\*\* Alliterations must preserve the tripartite vowel groups\[cite: 11\]:

  \* \*\*ర-Series:\*\* $\\{\\text{ర, రా, రై, రౌ}\\} \\mid \\{\\text{రి, రీ, రె, రే}\\} \\mid \\{\\text{రు, రూ, రొ, రో}\\}$\[cite: 11\].

  \* \*\*ఱ-Series:\*\* $\\{\\text{ఱ, ఱా, ఱై, ఱౌ}\\} \\mid \\{\\text{ఱి, ఱీ, ఱె, ఱే}\\} \\mid \\{\\text{ఱు, ఱూ, ఱొ, ఱో}\\}$\[cite: 11\].

&nbsp;

&nbsp;

             Ēkatara Yati Complete Isolation

 \[ ర (Sādhu Rēpha) \]  \<─── Strict Identity ───\>  \[ ర (Sādhu Rēpha) \]

         ≠                                              ≠

 \[ ఱ (Śakaṭa Rēpha) \] \<─── Strict Identity ───\>  \[ ఱ (Śakaṭa Rēpha) \]

 (No cross-consonant alliteration permitted with any other letter)

&nbsp;

&nbsp;

\*\*Corpus Provenance for Ēkatara Yati (6.37.1 – 6.37.2)\*\*

\* \*\*The First Verse of Classical Telugu Literature (Nannaya, \*Mahābhārata\*, Ādi 1-3):\*\*

  Nannaya opens the entire Telugu classical canon by deploying \*Ēkatara Yati\* across three lines\[cite: 11\]:

  \* Line 1: \*\*రా $\\longleftrightarrow$ రా\*\* (\*రాజకులైక... రాజమనోహరుఁడన్య...\*)\[cite: 11\].

  \* Line 3: \*\*రా $\\longleftrightarrow$ రా\*\* (\*రాజిత... పరాజిత...\*)\[cite: 11\].

  \* Line 4: \*\*రా $\\longleftrightarrow$ రా\*\* (\*రాజల... రాజమహేంద్రుఁడు...\*)\[cite: 11\].

\* \*\*Extended Sādhu Rēpha Corpus (ర $\\longleftrightarrow$ ర):\*\*

  \* \*\*ర $\\longleftrightarrow$ ర:\*\* \*...నగరములను నాశంబునొందు రక్షాచ్యుతులై...\* (\*Bhāratam\*, Udyōga 4-307)\[cite: 11\]; \*...పాదలేపమను పేరన్ గల్గు... నిర్జర...\* (\*Manu Caritra\* 1-75)\[cite: 11\]; \*రక్షోభూత పిశాచగోచరము దుర్గస్థంబునై...\* (\*Bhāratam\*, Virāṭa 1-164)\[cite: 11\]; \*...రక్షోనాయకులార నిర్జరవరవ్రాతంబు...\* (\*Bhāgavatam\* 2-100)\[cite: 11\].

  \* \*\*ర $\\longleftrightarrow$ రై:\*\* \*...వారలుఁ జని చేసిరర్చనలు రైవతకాద్రికినుత్సవంబుతోన్...\* (\*Bhāratam\*, Ādi 8-174)\[cite: 11\].

  \* \*\*రా $\\longleftrightarrow$ ర:\*\* \*రాజునకు విజయమూలము రాజిత మంత్రంబు...\* (\*Bhāratam\*, Sabhā 1-28)\[cite: 11\]; \*...రాగాంబుధులు నిట్ట గ్రమ్ముననుట...\* (\*Amuktamālyada\* 2-50)\[cite: 11\].

  \* \*\*రా $\\longleftrightarrow$ రా:\*\* \*రాజగృహంబుకంటెనభిరామముగానిలుగట్టఁగూడదే...\* (\*Bhāratam\*, Sabhā 1-123)\[cite: 11\]; \*రాజఁట ధర్మజుండు సురరాజసుతుండఁట...\* (\*Bhāratam\*, Sabhā 1-210)\[cite: 11\]; \*రారాజచ్చరణాబ్జసంజనిత గీర్వాణాపగా...\* (\*Bhāgavatam\* 5-197)\[cite: 11\]; \*గ్రావాకల్పిత కాయమాన జటిలద్రాక్షా...\* (\*Manu Caritra\* 2-22)\[cite: 11\]; \*రాజుల్ మత్తులు వారిసేవ నరకప్రాయంబు...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 11\].

  \* \*\*రై $\\longleftrightarrow$ ర:\*\* \*త్రైలోక్యమందిర రత్నతోరణములు...\* (\*Amuktamālyada\* 3-117)\[cite: 11\].

  \* \*\*రౌ $\\longleftrightarrow$ రా:\*\* \*...రౌమహర్షణి సుపౌరాణికుండు...\* (\*Bhāratam\*, Ādi 1-28)\[cite: 11\].

  \* \*\*రి $\\longleftrightarrow$ రీ:\*\* \*...నిర్జితుఁగావింపక... దశగ్రీవుండునుం...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 89)\[cite: 11\]; \*శ్రీవల్లభ యెపుడునవతరింతు నిజేచ్ఛన్...\* (\*Bhāgavatam\* 3-32)\[cite: 11\].

  \* \*\*రె $\\longleftrightarrow$ రీ:\*\* \*రెండును రాజులందు విపరీతము గావున...\* (\*Bhāratam\*, Ādi 1-100)\[cite: 11\].

  \* \*\*రే $\\longleftrightarrow$ రీ:\*\* \*రేవుల్మావు మతంగజంబులు మణిశ్రీఖండ...\* (\*Amuktamālyada\* 4-245)\[cite: 11\].

  \* \*\*రో $\\longleftrightarrow$ రు:\*\* \*...పురోగములై యగ్నియమవరుణ...\* (\*Bhāratam\*, Udyōga 5-3-11)\[cite: 11\]; \*రోషమయ మహాతరువు సుయోధనుఁడురు...\* (\*Bhāratam\*, Udyōga 1-355)\[cite: 11\]; \*శ్రోణీరమ్య ఘనస్తనీ నటన చారుప్రేక్షయున్...\* (\*Amuktamālyada\* 3-64)\[cite: 11\].

\* \*\*Extended Śakaṭa Rēpha Corpus (ఱ $\\longleftrightarrow$ ఱ):\*\*

  \* \*\*ఱ $\\longleftrightarrow$ ఱ:\*\* \*అవికయుఁ బట్టుఁ బుట్టము చెఱంగు మఱుంగయి యున్కిఁజేసి...\* (\*Kāśīkhaṇḍam\* 6-131)\[cite: 11\].

  \* \*\*ఱ $\\longleftrightarrow$ ఱా:\*\* \*అంకెలు గర్జలై యడర జాఁపుఁదనంబుననెందుఁ...\* (\*Bhāgavatam\* 8-44)\[cite: 11\].

  \* \*\*ఱా $\\longleftrightarrow$ ఱ:\*\* \*తాఁగయై మేరమీఱదొకప్పుడును ఘనశ్రీల...\* (\*Manu Caritra\* 6-56)\[cite: 11\].

  \* \*\*ఱి $\\longleftrightarrow$ ఱి:\*\* \*...ఏఱిండితనంబుచేతనిసిఱింతలు వాజెడిఁ...\* (\*Bhāgavatam\* 4-148)\[cite: 11\].

  \* \*\*ఱి $\\longleftrightarrow$ ఱె:\*\* \*ఱిక్కించుకొనియున్న జెక్కమొత్తముతోడి...\* (\*Kāśīkhaṇḍam\* 2-5)\[cite: 11\].

  \* \*\*ఱె $\\longleftrightarrow$ ఱి:\*\* \*జెప్పయుఁబోలె మాటయినెఱిం బనులారసి...\* (\*Bhāratam\*, Virāṭa 4-114)\[cite: 11\].

  \* \*\*ఱే $\\longleftrightarrow$ ఱి:\*\* \*...పోటుగండ్లఁదూతె లలనయౌర యొక్కొక తఱిం...\* (\*Amuktamālyada\* 1-32)\[cite: 11\]; \*తేపులు భీమలింగముగుఱించి జపంబొనరించి...\* (\*Haravilāsam\* 2-81)\[cite: 11\].

  \* \*\*ఱె $\\longleftrightarrow$ ఱే:\*\* \*జెక్కలు రావు పిల్లలకు జేపటినుండియు మేఁత గానమిన్...\* (\*Bhāgavatam\* 7-63)\[cite: 11\]; \*తెప్పల బాష్పముల్గుడిచి జేపె నృపాలుఁడు...\* (\*Daśakumāra Caritra\* 4-53)\[cite: 11\].

  \* \*\*ఱు $\\longleftrightarrow$ ఱు:\*\* \*...తీఱునకొడఁబాటు గల్గిన నెఱుంగమివెట్టరె...\* (\*Bhāratam\*, Udyōga 3-102)\[cite: 11\]; \*...మాఱుదెసల్ గైకొనుచుం గడంగి పలుమాఱుం దాఁకుచుం...\* (\*Bhāratam\*, Udyōga 2-259)\[cite: 11\]; \*...గండాల్పదానమేఱులుగఁ దద్వహుణాల ఱువ్వి ఱువ్వి...\* (\*Kāśīkhaṇḍam\* 2-24)\[cite: 11\].

  \* \*\*ఱు $\\longleftrightarrow$ ఱొ:\*\* \*యెఱిఁగియేనియునునెఱుంగకేని బలిమి తొచ్చు గడిగి...\* (\*Bhāratam\*, Sabhā 2-191)\[cite: 11\].

  \* \*\*ఱో $\\longleftrightarrow$ ఱు:\*\* \*తోలఁగ రోఁజఁగాఁ బలుమఱుం బొరలంబడి...\* (\*Bhāratam\*, Sabhā 1-158)\[cite: 11\]; \*తోలుచుఁబాఱి వనరుచును ఱువ్వునఁగూలెన్...\* (\*Śṛṅgāra Śakuntalamu\* 2-382)\[cite: 11\].

&nbsp;

\---

&nbsp;

\*\*6.38 'ర \- ఱ'ల యతి / ద్విరేఫ యతి (Dvirēpha Yati — The Cross-Repha Reconciliation)\*\*

&nbsp;

\* \*\*Traditional Prohibition:\*\* Early authorities (Appakavi, Nannaya, Tikkana, Errana, Śrīnātha) enforce an absolute prohibition against cross-rhyming soft liquid \*\*'ర'\*\* with hard trill \*\*'ఱ'\*\*, categorizing it as a defect (\*Prāsa Vairamu / Yati-bhaṅgamu\*)\[cite: 11\].

\* \*\*Historical Evolution & Validation:\*\* Over centuries, phonetic convergence, the blurring of manuscript orthography, and the proliferation of lexical doublets (\*chīruṭa/chīṟuṭa, mundaṟa/mundara, kūra/kūṟa\*) led later classical poets to accept \*\*'ర \- ఱ'\*\* alliteration\[cite: 11\].

\* \*\*Sixteenth-Century Codification:\*\* Formally codified in \*Sulakṣaṇa Sāramu\* (2-164) under the name \*\*ఱవడి\*\* (\*Ṟavaḍi\*) or \*\*ద్విరేఫయతి\*\* (\*Dvirēpha Yati\*):

  \> \*క॥ ధారుణి ఱవడి యనఁదగు, ఱరేఫకు రేఫణాకు రహివడిఁ దనరున్\*

  \> \*నీరమ్యకీర్తినగుఁదా, రారాజన్ నలువబలుగు ఱలుననంగన్\*\[cite: 11\]

\* \*\*Engine Parsing Policy:\*\*

  \* \*Strict Early Classical Mode (Nannaya/Tikkana/Appakavi):\* \*\*ర $\\longleftrightarrow$ ఱ\*\* must be flagged as a defect (\*bhaṅgamu\*)\[cite: 11\].

  \* \*Late Classical / Prabandha / Modern Mode:\* Authorized under \*Dvirēpha Yati\*, provided the consonants share matching vowel classes (\*\*ర $\\longleftrightarrow$ ఱ\*\*, \*\*రి $\\longleftrightarrow$ ఱి\*\*, \*\*రు $\\longleftrightarrow$ ఱు\*\*)\[cite: 11\].

&nbsp;

\---

&nbsp;

\*\*Algorithmic Verification Matrix for Engine Ingestion (Part 9 Summary)\*\*

&nbsp;

| Rule Type | Primary Target Coordinates | Grammatical / Phonetic Engine Conditions | Classical Engine Verdict |

| :--- | :--- | :--- | :--- |

| \*\*వికల్ప యతి (6.35)\*\*\[cite: 11\] | Anunāsika Sandhi compounds (\*సన్మార్గ, వాజ్నియమ\*)\[cite: 11\] | Triple resolution: Option A (Nasal), Option B (Pre-sandhi Stop), Option C (Word-2 Initial)\[cite: 11\]. \*\*Option B strictly prohibited on \*-maya\* and \*-mātra\* stems\*\*\[cite: 11\]. | \*\*Canonical\*\*\[cite: 11\] |

| \*\*ప్రత్యేక యతి (6.36)\*\*\[cite: 11\] | Elided demonstrative compounds (\*చేతిది, నాది, అట్టిది\*)\[cite: 11\] | \*\*Must match strictly on the surface consonant\*\*\[cite: 11\]. Reaching back to elided vowel 'అ' is prohibited\[cite: 11\]. | \*\*Canonical\*\*\[cite: 11\] |

| \*\*ఏకతర యతులు (6.37)\*\*\[cite: 11\] | \*\*ర $\\longleftrightarrow$ ర\*\* and \*\*ఱ $\\longleftrightarrow$ ఱ\*\*\[cite: 11\] | Strict self-identity\[cite: 11\]. All cross-consonant bridges prohibited\[cite: 11\]. Governed internally by the tripartite vowel grid\[cite: 11\]. | \*\*Canonical\*\*\[cite: 11\] |

| \*\*ద్విరేఫ యతి (6.38)\*\*\[cite: 11\] | \*\*ర $\\longleftrightarrow$ ఱ\*\*\[cite: 11\] | Cross-liquid bridge between Sādhu and Śakaṭa Rēpha\[cite: 11\]. Rejected by early canon; valid in late/post-16th century poetics\[cite: 11\]. | \*\*Mode-Dependent\*\*\[cite: 11\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.38 'ర \- ఱ'ల యతి పరిశీలనము (Dvirēpha Yati Analysis & Complex Provenance)

* **Philological Problem in Classical Textual Scansion (6.38.1):**  
* Early prosodists prohibited pairing soft liquid **'ర'** (*Sādhu Rēpha*) with hard liquid **'ఱ'** (*Śakaṭa Rēpha*).  
* However, extensive variations exist in classical manuscripts, because numerous native Telugu lexical stems evolved as interchangeable doublets (*dvirūpa-śabdamulu*). When a line pairs apparent *ra* and *ṟa*, modern scansion engines must evaluate whether the stem is an attested doublet before declaring a *Dvirēpha Yati* or a metrical defect.  
* **Prominent Lexical Doublets in the Corpus (Vajzala / Vaiyākaraṇa Pārijātamu 6.38.1):**  
* **రాయి / ఱాయి (Stone):**  
* Tikkana uses *ఱాయి* (*నాయుల్లమరయ... జాయో కాకిట్లు...* — *Bhāratam*, Virāṭa 4-3-420: **ఱ $\\longleftrightarrow$ ఱ**).  
* Tikkana uses *రాయి* (*చేతఁగొని... రాతిపయి...* — *Bhāratam*, Anuśāsanika 4-110: **రా $\\longleftrightarrow$ రా**).  
* Śrīnātha uses *ఱాయి* (*...ఱచట్టు పయిన్...* — *Kāśīkhaṇḍam* 2-154: **ఱ $\\longleftrightarrow$ ఱ**).  
* Occurrences pairing *ర* and *ఱాయి* (e.g., *భ్రాంతులుఁ... జాలు...* \[*Kāśīkhaṇḍam* 2-113\]; *ఱలన్ రువ్వగఁ... రా...* \[*Śrīkālahastīśvara Śatakam*\]; *ఱలకునేడ... ర...* \[*Bhāskara Śatakam*\]; *ఱాకట్టుం... రా...* \[*Amuktamālyada* 4-166\]) can scan either as *Ēkatara Yati* (via doublet *రాయి*) or as *Dvirēpha Yati*.  
* **పాఱు / పారు (To Run / To Flow):** Vajzala proved this verb exists in both *Sādhu* and *Śakaṭa* forms across both semantic definitions. Peddana’s *శ్రేణుల్ గట్టి... పాఱెన్...* (*Manu Caritra* 3-12: **శ్రే \[రే\] $\\longleftrightarrow$ ఱె**) and Kṛṣṇadēvarāya’s *...గుండ్రలునాఁ... పాఱన్...* (*Amuktamālyada* 4-152: **ండ్ర \[ర\] $\\longleftrightarrow$ ఱ**) can scan as standard *Ēkatara Yati* via doublet *పారు*.  
* **రంతు / ఱంతు (Clamor / Noise):** Attested in both forms in Śrīnātha’s corpus (*ఱంతులు మీఱి...* \[*Kāśīkhaṇḍam* 4-96: **ఱ $\\longleftrightarrow$ ఱ**\]; *...రంతులఁ జేసెడి...* \[Chāṭu: **ర $\\longleftrightarrow$ ర**\]; *రంతుల్ సేయకు...* \[Chāṭu: **రం $\\longleftrightarrow$ ర**\]).  
* **Other Attested Doublets:** *చెఱఁగు / చెరఁగు* (*Kāśīkhaṇḍam* 2-17); *ఊఱుఁగాయ / ఊరుఁగాయ* (*Amuktamālyada* 1-82); *రెప్ప / ఱెప్ప*; *రేకు / ఱేకు*; *రొమ్ము / ఱొమ్ము*; *రేవు / ఱేవు*.

#### Canonical Provenance for Definite Dvirēpha Yati (6.38.2)

In verses where words possess no attested *Sādhu Rēpha* doublet (e.g., *క్రమ్మఱు, అంకు, గుఱ్ఱము, మీఱు, మాఱట*), classical and post-classical poets intentionally execute cross-liquid **ర $\\longleftrightarrow$ ఱ** alliteration:

* **ర $\\longleftrightarrow$ ఱ:** *...వీథిఁగాళికార్చనమున కొంటినేఁగెడి మఱందిఁ...* (*Manu Caritra* 8-107); *రజ్జుపరంపరలఁ గ్రమ్మఱన్ సుతుఁ గట్టన్...* (*Bhāgavatam* 10-Pūrvabhāga 383); *ప్రకరప్రాంచిత... మీఱన్...* (*Amuktamālyada* 5-150); *అంకుఁబోతుకునేల రమ్యంపు నిష్ఠలు...* (*Narasimha Śatakam*); *ప్రవసింపంజనువేళనేన్గులును గుఱ్ఱంబుల్...* (*Rāmāyaṇa Kalpavṛkṣamu*, Ayōdhyā 208); *...వృత్తి మీఱన్నిఖిలంబెఱుంగ...* (*Śṛṅgāra Śakuntalamu* 5-72); *...సంజయెఱ్ఱలుపచరించు వేళకొక రమ్యమహీజముఁ...* (*Rāmāyaṇa Kalpavṛkṣamu*, Ayōdhyā 463); *...మాఱట కాసారముఁ బోలి నెమ్మొగము దా రంజిల్లు...* (*Bhāskara Rāmāyaṇamu*, Sundara 38).  
* **రా $\\longleftrightarrow$ ఱ:** *రాచబిడ్డడయిన ఱవ్వ మేలె...* (*Bhāgavatam* 10-Pūrvabhāga 321); *...రాచవేఁటలఁజాల ఱవ్వ దెచ్చె...* (*Bhāgavatam* 10-Pūrvabhāga 375); *...లసన్మహోక్షముల్ రాయుచు గోగణంబులను ఱంకెలువైచెడుఁ...* (*Bhāratam*, Virāṭa 5-758).  
* **రి $\\longleftrightarrow$ ఱి:** *...కోరికలర్థింపక నిద్ర యిమ్మనెడి వెఱిన్...* (*Amuktamālyada* 2-205); *...జాఱిన నునుఁబైటకొంగు సవరించుచు నవ్విన గౌరిఁ...* (*Amuktamālyada* 2-3).  
* **రి $\\longleftrightarrow$ ఱే:** *...సురారివరుండుత్తరభాగవర్తియయి మీఱెన్...* (*Amuktamālyada* 4-343).  
* **ఱి $\\longleftrightarrow$ రే:** *ఱెల్లు పెల్లలు నీటఁ ద్రెళ్ళి ఫేనము వండు... రేచన్...* (*Bhāratam*, Udyōga 4-153).  
* **రు $\\longleftrightarrow$ ఱు:** *...గార్తవీర్యార్జునునురమున గద మిడుంగుఱులు సెదరగ...* (*Amuktamālyada* 3-248); *...పూర్ణచంద్రుండని లోకులందఱునెఱుంగుటకున్...* (*Śṛṅgāra Śakuntalamu* 1-29).  
* **రూ $\\longleftrightarrow$ ఱు:** *రూపము తారతమ్యములెఱుంగు...* (*Manu Caritra* 1-88); *...ఱొమ్ముపై నిల్చెనారూఢి మహిమ...* (*Nalacaritra* 1-6).  
* **రో $\\longleftrightarrow$ ఱు:** *రోయఁగ వత్తుఁ గందువ యెఱుంగుటనాతఁడు...* (*Daśakumāra Caritra* 10-42).

#### R̥-Varṇa Extension via Dvirēpha Yati (6.38.3)

By integrating *R̥ Yati* (Section 6.5: vocalic **'ఋ'** pairs with **రి, రీ, రె, రే**) with *Dvirēpha Yati* (**ర $\\longleftrightarrow$ ఱ**), an extended bridge is formed allowing **'ఋ'** (and consonants bound to *vaṭrasuḍi*) to rhyme directly with **'ఱి, ఱీ, ఱె, ఱే'**:

* **కృ \[ఋ\] $\\longleftrightarrow$ ఱి:** *...కృష్ణుఁడవ్విధమునెఱిఁగియుఁ \[= ఎఱిఁగియు\] దాన...* (*Śṛṅgāra Śakuntalamu* 5-175); *కృశమై కవును పేదఱికము \[= పేదఱికము\] వాయక...* (*Amuktamālyada* 1-134).  
* **నృ \[ఋ\] $\\longleftrightarrow$ ఱి:** *నృపసుతునవ్యవస్థతనెఱింగియు \[= ఎఱింగియు\]...* (*Bhāgavatam* 3-21).  
* **గృ \[ఋ\] $\\longleftrightarrow$ ఱె:** *...గృహిచే శత్రుబలంబు పెంపుసెడి పాఱెన్ \[= పాఱెన్\]...* (*Uttara Rāmāyaṇamu* 2-85).  
* **ఱె $\\longleftrightarrow$ హృ \[ఋ\]:** *ఱెప్పలు మూయరిద్దఱును హృత్సదనంబు కవాటముల్ బలెన్...* (*Rāmāyaṇa Kalpavṛkṣamu*, Bāla 184).  
* **ఱె $\\longleftrightarrow$ బృ \[ఋ\]:** *...ఱెక్కలపైఁ బ్రదుకవలసెఁ బృథ్వీ రాజ్యం...* (*Rāmāyaṇa Kalpavṛkṣamu*, Ayōdhyā 316).  
* **ఱే $\\longleftrightarrow$ నృ \[ఋ\]:** *ఱేఁడు దొర సామియననొప్పు నృపతి పేళ్ళు...* (*Āndhra Nāma Saṅgrahamu*, Mānava 1).

---

### 6.39 ఉభయ యతులు — పరిచయము (Ubhaya Yatulu — Dual-Track Caesura Introduction)

* **Structural Definition:** *Ubhaya Yati* (Dual-Track Caesura) governs compound structures or inflected forms where a morpheme junction forms a single phonetic word (*ēkapadamu*). At this junction, the poet is granted the choice between two independent alliterative tracks:  
1. **Track 1 (Svara Mārga):** Match the underlying junction vowel (*para-padādi svara* or enclitic vowel) under *Svara Yati*.  
2. **Track 2 (Vyañjana Mārga):** Match the resulting surface consonant cluster under *Consonant / Prāṇi Yati*.  
* **Canon Taxonomy (13 Ubhaya Yatis):** Appakavi classified 12 rules, with commentators restoring *Bhinna Yati* into this category to complete the **13 Canonical Ubhaya Yatis**:

                     The 13 Ubhaya Yati Classes

┌────┬─────────────────────────────┬────┬─────────────────────────────┐

│  1 │ భిన్నయతి (6.40)             │  8 │ నిత్యసమాస విశ్రాంతి (6.49) │

├────┼─────────────────────────────┼────┼─────────────────────────────┤

│  2 │ నిత్యయతి (6.41)             │  9 │ దేశ్య నిత్యసమాస (6.49.6)    │

├────┼─────────────────────────────┼────┼─────────────────────────────┤

│  3 │ విభాగ వళి (6.42)            │ 10 │ నామాఖండ విశ్రమము (6.50)     │

├────┼─────────────────────────────┼────┼─────────────────────────────┤

│  4 │ కాకుస్వర వళి (6.43)         │ 11 │ రాగమసంధి వళి (6.51)         │

├────┼─────────────────────────────┼────┼─────────────────────────────┤

│  5 │ ప్లుతయుగ విశ్రామము (6.44)   │ 12 │ పరరూప యతి (6.47)            │

├────┼─────────────────────────────┼────┼─────────────────────────────┤

│  6 │ పంచమీ విభక్తి విరామము (6.45) │ 13 │ ప్రాది యతులు (6.48)          │

├────┼─────────────────────────────┴────┴─────────────────────────────┤

│  7 │ యుష్మదస్మచ్చబ్ద యతి (6.46)                                     │

└────┴────────────────────────────────────────────────────────────────┘

\`\`\`\[cite: 12\]

&nbsp;

\---

&nbsp;

\#\#\# 6.40 భిన్నయతి (Bhinna Yati — 'Iñcu' Verbal Augment Dual Caesura)

&nbsp;

\* \*\*Morphological Environment:\*\* Governs verbs and verbal nouns formed with the Telugu verbalizing suffix/augment \*\*'-iñcu'\*\* (\*iñcuk\* / ఇంచుగాగమము), derived from\[cite: 12\]:

  \* \*Sanskrit Roots:\* $\\text{పచ్} \+ \\text{ఇంచు} \= \\text{పచించు}$; $\\text{హృ} \+ \\text{ఇంచు} \= \\text{హరించు}$; $\\text{ధృ} \+ \\text{ఇంచు} \= \\text{ధరించు}$; $\\text{త్యజ్} \+ \\text{ఇంచు} \= \\text{త్యజించు}$\[cite: 12\].

  \* \*Native Telugu Roots:\* \*అంగలించు, ఆవులించు, తిలకించు, కావించు\*\[cite: 12\].

  \* \*Nominal Bases (Nāmadhātuvulu):\* \*నుతించు, శయనించు, వర్ణించు\*\[cite: 12\].

\* \*\*The Structural Principle:\*\* At the syllable where \*\*'ఇంచు'\*\* fuses with the stem, the poet may rhyme \*\*EITHER with the underlying vowel 'ఇ' (Svara track) OR with the resulting surface consonant (Vyañjana track)\*\*\[cite: 12\]\!

&nbsp;

&nbsp;

              Bhinna Yati Dual Engine Routing

           \[ Verb Stem Junction with \-iñcu(k) \]

                             │

    ┌────────────────────────┴────────────────────────┐

    ▼                                                 ▼

&nbsp;

Track 1: Svara Mārga                             Track 2: Vyañjana Mārga (Matches vowel 'ఇ' of \-iñcu)                    (Matches host consonant \+ vowel) • నుతించు ⟷ ఇ/ఈ/ఎ/ఏ                             • నుతించు ⟷ తి/తీ/తె/తే (Prāṇi) • హరించు ⟷ ఇ/ఈ/ఎ/ఏ                              • హరించు ⟷ రి/రీ/రె/రే (Ēkatara) • పోషించు ⟷ ఇ/ఈ/ఎ/ఏ                             • పోషించు ⟷ షి/షీ/షె/షే (Ūṣma)

&nbsp;

\#\#\#\# The Three Structural Stem Types & 5 Combinatorial Modes (6.40.2)

By \*Bāla Vyākaraṇam\* (Kriyā 50), monosyllabic and disyllabic stems that are light (\*guru-virahita\*) and non-ya-ending (\*ayānta\*) optionally insert the augment \*iyuṭ\* before \*iñcu\* ($\\text{నుతి} \+ \\text{ఇయ్} \+ \\text{ఇంచు} \= \\text{నుతియించు}$)\[cite: 12\]. Stems with heavy vowels (\*పోష్ $\\rightarrow$ పోషించు\*) or multi-syllables (\*పలుకు $\\rightarrow$ పలికించు\*) never take \*iyuṭ\*\[cite: 12\]. This yields three operational word types\[cite: 12\]:

&nbsp;

\* \*\*Type 1: Stems with Explicit Hiatus Doublet (ధరియించు, హరియించు, వచియించు):\*\*

  \* \*Svara Mode (Mode 1):\* Rhymes on the isolated vowel \*\*'ఇ'\*\* of \*య్ \+ ఇంచు\*\[cite: 12\]. (Unanimously accepted by Appakavi, Ananta, and Sulakṣaṇasāra)\[cite: 12\].

\* \*\*Type 2: Roots with Unaugmented Variants in a Doublet Pair (ధరించు, హరించు, నుతించు):\*\*

  \* \*Consonant Mode (Mode 2i):\* Rhyme on the surface consonant (\*\*రి, తి\*\*)\[cite: 12\]. (Termed \*Peṟayati\* by Appakavi, \*Bhinna\* by Ananta)\[cite: 12\].

  \* \*Vowel Mode (Mode 2ii):\* Rhyme on the vowel \*\*'ఇ'\*\* of \*ఇంచు\*\[cite: 12\]. (Omitted in Appakavi's theory, but confirmed by Sulakṣaṇasāra and classical Mahākavi usage)\[cite: 12\].

\* \*\*Type 3: Stems Without Hiatus Doublets (పోషించు, పలికించు, చాలించు, ఉపమించు):\*\*

  \* \*Consonant Mode (Mode 3i):\* Rhyme on the surface consonant (\*\*షి, కి, లి, మి\*\*)\[cite: 12\].

  \* \*Vowel Mode (Mode 3ii):\* Rhyme on the underlying vowel \*\*'ఇ'\*\* of \*ఇంచు\*\[cite: 12\]. (Termed \*Abhinna Yati\* in Sulakṣaṇasāra)\[cite: 12\].

&nbsp;

\#\#\#\# Nannaya's Definitive Benchmark Stanza (\*Mahābhārata\*, Ādi 5-151) (6.40.3)

Nannaya establishes both tracks of \*Bhinna Yati\* in a single verse\[cite: 12\]:

\* \*\*Line 1 (Consonant Mode 3i):\*\* \*\*వీ $\\longleftrightarrow$ ప్రభవించిన \[వి\]\*\* ($\\text{ప్రభవించు} \\implies \\mathbf{వీ \\longleftrightarrow వి}$ Prāṇi Yati)\[cite: 12\].

\* \*\*Line 2 (Vowel Mode 3ii):\*\* \*\*ఈ $\\longleftrightarrow$ ఉపమింపఁగ \[ఇ\]\*\* ($\\text{ఉపమించు} \\implies \\text{ఇంచు} \\text{ vowel } \\mathbf{ఇ} \\longleftrightarrow \\mathbf{ఈ}$ in \*ఈరమణీయ\* Svara Yati)\[cite: 12\]\!

\* \*Corrupt Scribal Variant Overturned:\* Later copyists altered Line 2 to \*...కాంతినుదయించిన...\* to manufacture an ordinary sandhi vowel match\[cite: 12\]. The text rejects this alteration as ungrammatical nonsensical diction; Nannaya's authentic reading is \*ఉపమింపఁగ\*, demonstrating vowel-track \*Bhinna Yati\*\[cite: 12\].

&nbsp;

\#\#\#\# Corpus Provenance Trail for Bhinna Yati (6.40.4 – 6.40.6)

\* \*\*Mode 1: Doublets with 'యించు' (Vowel Track):\*\*

  \* \*\*ఇ $\\longleftrightarrow$ విధియించు \[ఇ\]:\*\* \*ఇమ్ముగనాత్మరక్ష విధియించు విధంబున...\* (\*Bhāratam\*, Ādi 6-111)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ భరియింతున్ \[ఇ\]:\*\* \*...కాననాంతరముననెవ్విధంబున భరియింతునొక్కొ...\* (\*Bhāratam\*, Āraṇya 1-30)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ వచియించెద \[ఇ\]:\*\* \*...ధ్వజంబెత్తిననెత్తనిమ్ము వచియించెదఁ...\* (\*Manu Caritra\* 3-15 / \*Appakavīyamu\* 3-82)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ జనియించిన \[ఇ\]:\*\* \*...నీవెట్టి ప్రదోషవేళ జనియించిన వాఁడవొగాక...\* (\*Appakavīyamu\* 3-83)\[cite: 12\].

\* \*\*Mode 2i: Doublet Stems without 'య' (Consonant Track):\*\*

  \* \*\*సి $\\longleftrightarrow$ వసించి \[సి\]:\*\* \*సిరికిఁదొలంగి కానల వసించి కృశించిన...\* (\*Bhāratam\*, Udyōga 5-342)\[cite: 12\].

  \* \*\*తె $\\longleftrightarrow$ వధింపఁగ \[ధి\] (Vargaja):\*\* \*తెల్లము మిమ్మునందఱ వధింపఁగ...\* (\*Bhāratam\*, Udyōga 1-210)\[cite: 12\].

  \* \*\*మి $\\longleftrightarrow$ శమించునె \[మి\]:\*\* \*...నిలుమన్నఁబూజని శమించునె యొండొరు...\* (\*Bhāratam\*, Śānti 3-252)\[cite: 12\].

  \* \*\*దే $\\longleftrightarrow$ నుతించి \[తి\] (Vargaja):\*\* \*...దేవునినయ్యిరువురును నుతించిరజుఁడు...\* (\*Bhāratam\*, Udyōga 4-170)\[cite: 12\].

  \* \*\*రి $\\longleftrightarrow$ ధరించి \[రి\]:\*\* \*క్రిందుగ దీర్ఘనిద్రలు ధరించి శయించిన...\* (\*Harivaṁśamu\*, Pūrva 3-106)\[cite: 12\].

  \* \*\*ని $\\longleftrightarrow$ నె \[జనించెన్\]:\*\* \*...జనించెనదియొక్క మాటకే నెమ్మనమున...\* (\*Bhāgavatam\* 5-166)\[cite: 12\].

  \* \*\*చి $\\longleftrightarrow$ సృజించు \[జి\] (Vargaja):\*\* \*...వదలక రక్షించిన లోకనికాయముల సృజించుటకును...\* (\*Bhāgavatam\* 3-274)\[cite: 12\].

\* \*\*Mode 3i: Non-Doublet Stems (Consonant Track):\*\*

  \* \*\*మీ $\\longleftrightarrow$ ఉపమింప \[మి\]:\*\* \*...లక్ష్మీవిభవంబుతోడనుపమింప సమంబులుగావశేషరా...\* (\*Bhāratam\*, Sabhā 2-114)\[cite: 12\].

  \* \*\*కి $\\longleftrightarrow$ ఉపేక్షించె \[కి\]:\*\* \*...క్రమ్మఱింపక యుపేక్షించెఁ బూర్వ విహిత...\* (\*Bhāratam\*, Sabhā 2-316)\[cite: 12\].

  \* \*\*వే $\\longleftrightarrow$ కావింపన్ \[వి\]:\*\* \*వేఱవానికిఁ గడుగావింపనేల...\* (\*Bhāratam\*, Āraṇya 5-39)\[cite: 12\].

  \* \*\*కి $\\longleftrightarrow$ స్రుక్కించి \[కి\]; పి $\\longleftrightarrow$ కోపించి \[భీ\] (Vargaja); పి $\\longleftrightarrow$ గుప్పించి \[పీ\]:\*\* (\*Bhāratam\*, Udyōga 1-192)\[cite: 12\].

  \* \*\*ర్షి \[షి\] $\\longleftrightarrow$ హర్షించి \[షే\]; క్షి \[షి\] $\\longleftrightarrow$ వీక్షించి \[చే\] (Sarasayati); జి $\\longleftrightarrow$ లజ్జించి \[చె\] (Vargaja):\*\* (\*Manu Caritra\* 2-87)\[cite: 12\].

  \* \*\*ది $\\longleftrightarrow$ బాధించి \[దిం\]; గి $\\longleftrightarrow$ ఏఁగించెద \[గి\]:\*\* (\*Bhāratam\*, Ādi 6-297)\[cite: 12\].

  \* \*\*చిం $\\longleftrightarrow$ వర్షించున్ \[షి\] (Sarasayati); దె $\\longleftrightarrow$ భేదించున్ \[ది\]:\*\* (\*Bhāgavatam\* 7-296)\[cite: 12\].

\* \*\*Mode 2ii: Doublet Stems without 'య' (Vowel Track on 'ఇ'):\*\*

  \* \*\*ఏ $\\longleftrightarrow$ నటించిన \[ఇ\]:\*\* \*...నేను దియ్యమున నటించిన హరుఁడైన...\* (\*Nr̥siṁha Purāṇamu\* 2-56)\[cite: 12\].

  \* \*\*ఏ $\\longleftrightarrow$ గణింపఁగ \[ఇ\]:\*\* \*తామఁట తలపఁగ దలలఁట యేమట పాదుకలమఁట గణింపఁగ...\* (\*Bhāgavatam\* 10-Uttara 581)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ చరించెడు \[ఇ\]:\*\* \*కన్నిచ్చకు వచ్చినట్టుల చరించెడువారలుగాన...\* (\*Udbhaṭārādhya Caritra\* 1-98)\[cite: 12\].

  \* \*\*ఈ $\\longleftrightarrow$ ధరించెను \[ఇ\]:\*\* \*యీ నిఖిలావనీధుర ధరించెనుదంచితబాహుపీఠికన్...\* (\*Ghaṭikācalamu\* 1-89)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ గణింపరు \[ఇ\]:\*\* \*...కవుంగిలించెనౌనెయ్యెడ మేలె చూతురు గణింపరు...\* (\*Manu Caritra\* 1-172)\[cite: 12\].

  \* \*\*ఈ $\\longleftrightarrow$ చరింతురు \[ఇ\]:\*\* \*...పొగడెడి నీ క్రియ సత్పుత్రకులు చరింతురు పుత్రా...\* (\*Prabandharāja Vēṅkaṭēśvara Vijayavīlāsamu\* 688)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ వరించిన \[ఇ\]:\*\* \*...నన్నెవ్విధి దూఱినన్ నను వరించిన శారద లేచిపోవునే...\* (\*Jāṣuvā\*, \*Khaṇḍakāvyamu\* 4)\[cite: 12\].

  \* \*\*హీ $\\longleftrightarrow$ హరించక \[ఇ\]:\*\* \*...హరించక సత్కీర్తి యీ మహీతలమెల్లన్...\* (\*Sulakṣaṇasāramu\* 126)\[cite: 12\].

\* \*\*Mode 3ii: Non-Doublet Stems (Vowel Track on 'ఇ' — Abhinna Yati):\*\*

  \* \*\*ఇ $\\longleftrightarrow$ శయనించు \[ఎ\]:\*\* \*చంపనచ్చేరువఁజప్పరంబున శయనించు యుధామన్యుఁడెఱిఁగి...\* (\*Bhāratam\*, Sauptika 1-169)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ తోఁపించు \[ఇ\]:\*\* \*...నెయ్యది మిగులఁదోఁపించెఁ దజ్జన్యంబు...\* (\*Bhāratam\*, Aśvamēdha 2-125)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ ఎలుగించుచున్ \[ఇ\]:\*\* \*ఎలమిఁ బికాలితోడనెలుగించుచుఁ జిల్కలతోడఁ...\* (\*Kumārasambhavamu\* 9-110)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ పాటించి \[ఇ\]:\*\* \*పాటించి ధరించి పొందు ఘటియించిననుజ్జ్వల...\* (\*Bhāskara Rāmāyaṇamu\*, Yuddha 2656)\[cite: 12\].

  \* \*\*ఋ $\\longleftrightarrow$ పురుడించు \[ఇ\]:\*\* \*మృత్యుకరాళదంష్ట్రఁ బురుడించు భయంకరశక్తి...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 23)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ హత్తించు \[ఇ\]:\*\* \*...నిష్టఫలసిద్ధిఁదోర హత్తించునింతి...\* (\*Pāṇḍuraṅgamāhātmyamu\* 2-78)\[cite: 12\].

  \* \*\*ఇం $\\longleftrightarrow$ భోగించు \[ఇ\]:\*\* \*ఇంతి నీతోడఁగూడి భోగించునట్టి...\* (\*Molla Rāmāyaṇamu\*, Araṇya 54)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ మ్రోగించి \[ఇ\]:\*\* \*మ్రోగించియుఁ గమ్మతావులొలయించియుఁ...\* (\*Kavikarṇarasāyanamu\* 4-17)\[cite: 12\].

&nbsp;

\---

&nbsp;

\#\#\# 6.41 నిత్యయతి (Nitya Yati — Conditional Enclitic 'Ēni' Dual Caesura)

&nbsp;

\* \*\*Morphological Definition:\*\* In Telugu syntax, the conditional enclitic particle \*\*'ఏని'\*\* (\*ēni\* \= if / whether / even if; equivalent to Sanskrit \*api\*) obligatorily compounds with preceding verb or nominal forms (\*చేసెన్ \+ ఏని \= చేసెనేని\*; \*కలిగెన్ \+ ఏని \= కలిగెనేని\*; \*ఎన్నఁడున్ \+ ఏని \= ఎన్నఁడున్నేని\*; \*కాదు \+ ఏని \= కాదేని\*; \*ఏది \+ ఏని \= ఏదేని\*)\[cite: 12\]. It never occurs as an isolated, standalone word\[cite: 12\].

\* \*\*The Structural Rule (నిత్యయతి):\*\* Because sandhi between the host word and \*'ēni'\* is grammatically obligatory (\*nityamu\*), forming a unified compound word, the caesura coordinate at this junction permits \*\*DUAL-TRACK MATCHING\*\*\[cite: 12\]:

  1\. \*\*Track 1 (Svara Track):\*\* Match vowel \*\*'ఏ'\*\* (\*ē\*) of \*'ēni'\* under Class 2 Svara Yati (\*ఇ, ఈ, ఎ, ఏ\*)\[cite: 12\].

  2\. \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant (\*\*నే, దే, పే\*\*, etc.) under consonant \*Prāṇi\* or \*Vargaja Yati\*\[cite: 12\].

\* \*\*Nomenclature:\*\* Termed \*\*నిత్యయతి\*\* (\*Nitya Yati\*) by Appakavi and Anantudu (\*Chandodarpaṇamu\* 1-103)\[cite: 12\].

&nbsp;

&nbsp;

                Nitya Yati Dual Engine Routing

           \[ Host Word \+ Conditional Enclitic 'ఏని' \]

                              │

     ┌────────────────────────┴────────────────────────┐

     ▼                                                 ▼

&nbsp;

Track 1: Svara Mārga                              Track 2: Vyañjana Mārga (Matches vowel 'ఏ' of ఏని)                        (Matches surface mutated consonant) • కర్ముఁడేని ⟷ ఎ/ఇ/ఈ/ఏ                            • కలిగెనేని ⟷ ని/నీ/నె/నే (Prāṇi) • కాదేని ⟷ ఎ/ఇ/ఈ/ఏ                                • ఎందేనిన్ ⟷ ది/దీ/దె/దే (Prāṇi) (Class 2 Vowel Equivalence)                       (Consonant Class Preserved)

&nbsp;

\#\#\#\# Treatise Attestations & Provenance Trail (6.41, 6.41.1 – 6.41.2)

\* \*\*Treatise Benchmark Stanzas:\*\*

  \* \*Appakavīyamu (3-214, citing Śēṣadharmamulu):\*

    \* Line 2 (Vowel Track): \*\*ఎ $\\longleftrightarrow$ కర్ముఁడేని\*\* ($\\text{కర్ముఁడు} \+ \\mathbf{ఏని} \\implies \\mathbf{ఎ \\longleftrightarrow ఏ}$ Svara Yati)\[cite: 12\].

    \* Line 4 (Consonant Track): \*\*ని $\\longleftrightarrow$ కలిగెనేని\*\* ($\\text{కలిగెన్} \+ \\text{ఏని} \= \\text{కలిగెనేని} \\implies \\mathbf{ని \\longleftrightarrow నే}$ Prāṇi Yati)\[cite: 12\].

  \* \*Chandodarpaṇamu (1-103 — Anantudu):\*

    \* Line 3 (Vowel Track): \*\*ఎ $\\longleftrightarrow$ కర్ముఁడేని\*\* ($\\mathbf{ఎ \\longleftrightarrow ఏ}$)\[cite: 12\].

    \* Line 4 (Consonant Track): \*\*ని $\\longleftrightarrow$ తలఁచెనేని\*\* ($\\mathbf{ని \\longleftrightarrow నే}$)\[cite: 12\].

\* \*\*Track 1: Vowel Matches on 'ఏ' (6.41.1):\*\*

  \* \*\*ఈ $\\longleftrightarrow$ తగఁడేని \[ఏ\]:\*\* \*యీతఁడని సేయఁగాఁ దగఁడేని వీని...\* (\*Bhāratam\*, Ādi 6-48)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ చెప్పకుండిరేని \[ఏ\]:\*\* \*...ధర్మసందేహమడిగిన నెఱిఁగి చెప్పకుండిరేని...\* (\*Bhāratam\*, Sabhā 2-237)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ సహించునేని \[ఏ\]:\*\* \*...గలిగిన నెఱిఁగి యెద సహించునేని భార్య...\* (\*Bhāratam\*, Āraṇya 2-160)\[cite: 12\].

  \* \*\*ఏ $\\longleftrightarrow$ ఇం పేని \[ఏ\]:\*\* \*...యింపేనిఁ దురంగశాలలకునెల్లను...\* (\*Bhāratam\*, Virāṭa 1-272)\[cite: 12\].

  \* \*\*ఈ $\\longleftrightarrow$ జాలితేని \[ఏ\]:\*\* \*...నీ వాక్యము వినఁగజాలితేని...\* (\*Bhāgavatam\* 6-2-94)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ చక్కడిచెనేని \[ఏ\]:\*\* \*యిక్కడిసేనఁ జక్కడిచెనేనియుఁ జూతునకాక...\* (\*Bhāratam\*, Virāṭa 4-3-307)\[cite: 12\].

  \* \*\*ఏ $\\longleftrightarrow$ ఎఱుఁగుదేని \[ఏ\]:\*\* \*నా కొలఁది యిట్లరయనెఱుఁగుదేనినిది లెస్స...\* (\*Bhāratam\*, Udyōga 5-1-308)\[cite: 12\].

  \* \*\*ఏ $\\longleftrightarrow$ వినవేని \[ఏ\]:\*\* \*వినవేని నొచ్చి తలఁచెదిట్టులగుట...\* (\*Bhāratam\*, Udyōga 5-1-62)\[cite: 12\].

  \* \*\*ఎ $\\longleftrightarrow$ ఏమేని \[ఏ\]:\*\* \*...లేకునికినేమేని వికల...\* (\*Bhāratam\*, Udyōga 5-6-576)\[cite: 12\]; \*ఎట్టి యపరాధమొనరించెనేనిఁ దల్లి...\* (\*Bhāratam\*, Śānti 4-269)\[cite: 12\].

  \* \*\*హి $\\longleftrightarrow$ నేర్చితేని \[ఏ\] (Sarasayati):\*\* \*హితము చెప్పితి విననేర్చితేని లెస్స...\* (\*Bhāratam\*, Śānti 6-219)\[cite: 12\].

  \* \*\*ఇ $\\longleftrightarrow$ కాదేని \[ఏ\]:\*\* \*...చెప్పెదరు కాదేనిన్ మదీయాస్యగం...\* (\*Bhāgavatam\* 10-Pūrvabhāga 337)\[cite: 12\].

  \* \*\*ఏ $\\longleftrightarrow$ కీడువుట్టెనేని \[ఏ\]:\*\* \*...కీడువుట్టెనేనిఁ దొలఁగించు...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 184)\[cite: 12\].

  \* \*\*ఈ $\\longleftrightarrow$ విగ్రహమునేని \[ఏ\]:\*\* \*యీ మహి నీదు విగ్రహమునేని...\* (\*Vēṅkaṭēśvara Śatakam\* 53)\[cite: 12\].

\* \*\*Track 2: Consonant Matches on Mutated Stem (6.41.2):\*\*

  \* \*\*నే $\\longleftrightarrow$ ణీ (Nannaya):\*\* \*మదీయ భాషితమెన్నఁడున్నేని \[= ఎన్నఁడున్ \+ ఏని\] మోఘముగాదు దిగ్ధరణీ...\* (\*Bhāratam\*, Ādi 7-142)\[cite: 12\].

  \* \*\*నీ $\\longleftrightarrow$ సభనేని \[నే\] (Tikkana):\*\* \*నీవును జూచితట్టి సభనేని \[= సభన్ \+ ఏని\] వినంబడదే యుగంబులన్...\* (\*Bhāratam\*, Sabhā 2-95)\[cite: 12\].

  \* \*\*నే $\\longleftrightarrow$ నె:\*\* \*చానెత్తికొంటిరక్కలనేనియుఁ \[= అక్కలన్ \+ ఏనియున్\] దలమాసువోని నెత్తురు...\* (\*Bhāgavatam\* 10-166)\[cite: 12\].

  \* \*\*ది $\\longleftrightarrow$ ఎందేనిన్ \[దే\]:\*\* \*...మందిరం జేరి... యెందేనిం \[= ఎందు \+ ఏనిన్\] జనంబోని భంగి...\* (\*Bhāratam\*, Ādi 2-219)\[cite: 12\].

  \* \*\*పే $\\longleftrightarrow$ పె:\*\* \*నీకెంత నేర్పేనింబోవు \[= నేర్పు \+ ఏనిన్\] శిరంబు ప్రక్కలయి తప్పెన్దిప్పె...\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 209)\[cite: 12\].

  \* \*\*ని $\\longleftrightarrow$ విగ్రహమునేని \[నే\]:\*\* \*నినుఁగనలేము విగ్రహమునేనిఁ \[= విగ్రహమున్ \+ ఏనిన్\] గనన్మది బుద్ధి పుట్టినన్...\* (\*Vēṅkaṭēśvara Śatakam\* 57)\[cite: 12\].

&nbsp;

\---

&nbsp;

\#\#\# 6.42 విభాగ యతి (Vibhāga Yati — Distributive Suffix '-ēsi' Dual Caesura)

&nbsp;

\* \*\*Definition:\*\* The native Telugu distributive suffix \*\*'-ēsi'\*\* (ఏసి \= \-each, indicating proportional division or measurement) attaches directly to numerals (\*నాలుగు \+ ఏసి \= నాలుగేసి\*) and quantified measure nouns (\*గంపెఁడు \+ ఏసి \= గంపెఁడేసి\*; \*దోసెఁడు \+ ఏసి \= దోసెఁడేసి\*; \*ఇంతలు \+ ఏసి \= ఇంతలేసి\*; \*అంతలు \+ ఏసి \= అంతేసి\*)\[cite: 12\].

\* \*\*The Dual-Track Rule (విభాగ వళి):\*\* Because sandhi between the numerical base and the suffix \*-ēsi\* is obligatory (\*nityamu\*), forming a unified distributive compound, the caesura at this junction licenses \*\*EITHER Track 1 (Vowel Track on 'ఏ') OR Track 2 (Consonant Track on the surface syllable 'గే', 'డే', 'తే')\*\*\[cite: 12\]:

  \* \*Example with 'నాలుగేసి':\*

    \* \*\*Track 1 (Vowel Track):\*\* Scans as \*నాలుగు \+ ఏసి\*, resolving to \*\*'ఏ'\*\* under \*Svara Yati\*\[cite: 12\].

    \* \*\*Track 2 (Consonant Track):\*\* Scans as integrated compound syllable \*\*'గే'\*\*, resolving via \*Prāṇi\* (\*\*గే\*\*) or \*Vargaja Yati\* (\*\*కృ, క, ఖ, ఘ\*\*)\[cite: 12\].

\* \*\*Nomenclature:\*\* Named \*\*విభాగ వళి\*\* (\*Vibhāga Vaḷi\*) by Appakavi\[cite: 12\].

\* \*\*Extended Morphological Scope (6.42.1):\*\* Beyond \*-ēsi\*, commentators extend \*Vibhāga Yati\* to related measurement and ordinal bound morphemes\[cite: 12\]:

  \* \*Quantitative Measure Suffix:\* \*\*-ఎఁడు\*\* (\*-e'ḍu\*)\[cite: 12\].

  \* \*Ordinal Suffix:\* \*\*-అవ\*\* (\*-ava\*, e.g., \*రెండు \+ అవ \= రెండవ\*)\[cite: 12\].

&nbsp;

&nbsp;

              Vibhāga Yati Dual Engine Routing

        \[ Numeral/Measure Stem \+ Distributive Suffix \-ēsi \]

                                │

     ┌──────────────────────────┴──────────────────────────┐

     ▼                                                     ▼

&nbsp;

Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga (Matches vowel 'ఏ' of \-ēsi)                           (Matches surface compound consonant) • నాలుగేసి ⟷ ఇ/ఈ/ఎ/ఏ                                  • నాలుగేసి \[గే\] ⟷ క/ఖ/గ/ఘ • ఇంతలేసి ⟷ ఇ/ఈ/ఎ/ఏ                                   • దోసెఁడేసి \[డే\] ⟷ ట/ఠ/డ/ఢ (Class 2 Svara Equivalence)                           (Vargaja Stop Class Preserved)

&nbsp;

\#\#\#\# Canonical Attestations & Provenance Trail (6.42)

\* \*\*Appakavi's Complete Demonstrative Stanza (\*Kāvyacintāmaṇi\* / \*Appakavīyamu\* 3-220):\*\*

  \* Line 1 (Consonant Track): \*\*కృ $\\longleftrightarrow$ నాలుగేసి \[గే\]\*\* ($\\mathbf{కృ \\longleftrightarrow గే}$ Vargaja Yati)\[cite: 12\].

  \* Line 2 (Vowel Track): \*\*ఇ $\\longleftrightarrow$ నాలుగేసి \[ఏ\]\*\* ($\\text{కూర్మిన్} \+ \\text{ఇంతులకును} \\implies \\mathbf{ఇ \\longleftrightarrow ఏ}$ Svara Yati)\[cite: 12\].

  \* Line 3 (Consonant Track): \*\*ఠీ $\\longleftrightarrow$ దోసెఁడేసి \[డే\]\*\* ($\\mathbf{ఠీ \\longleftrightarrow డే}$ Vargaja Yati)\[cite: 12\].

  \* Line 4 (Vowel Track): \*\*ఇ $\\longleftrightarrow$ గంపెఁడేసి \[ఏ\]\*\* ($\\text{కడున్} \+ \\text{ఇంపెసంగ} \\implies \\mathbf{ఇ \\longleftrightarrow ఏ}$ Svara Yati)\[cite: 12\].

\* \*\*Extended Corpus Demonstrations:\*\*

  \* \*\*ఋ $\\longleftrightarrow$ ఇంతలేసి \[ఏ\] (Vowel Track):\*\* \*ఋషుల పాలిటివే యింతలేసి పనులు...\* ($\\text{ఇంతలు} \+ \\mathbf{ఏసి} \\implies \\mathbf{ఋ \\longleftrightarrow ఏ}$ Svara Yati) (\*Appakavīyamu\* 3-219 / \*Harivaṁśamu\* 2-104)\[cite: 12\].

  \* \*\*తె $\\longleftrightarrow$ చేరలంతేసి \[తే\] (Consonant Track):\*\* \*తెలివియౌ చేరలంతేసి కన్నులదాని...\* ($\\text{చేరలంత} \+ \\text{ఏసి} \= \\text{చేరలంతేసి} \\implies \\mathbf{తె \\longleftrightarrow తే}$ Prāṇi Yati) (\*Bhāratam\*, Virāṭa 2-128)\[cite: 12\].

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (Part 10 Summary)

&nbsp;

| Rule Type | Primary Target Coordinates | Grammatical / Phonetic Engine Conditions | Classical Engine Verdict |

| :--- | :--- | :--- | :--- |

| \*\*ద్విరేఫ యతి ప్రయోగ పరిశీలన (6.38.1 – 6.38.4)\*\*\[cite: 12\] | \*\*ర $\\longleftrightarrow$ ఱ\*\*\[cite: 12\] | First check if word is an attested doublet (\*రాయి/ఱాయి, పాఱు/పారు\*)\[cite: 12\]. If non-doublet, validate under Dvirēpha Yati\[cite: 12\]. Extends to \*\*ఋ $\\longleftrightarrow$ ఱి/ఱీ/ఱె/ఱే\*\*\[cite: 12\]. | \*\*Canonical (Post-Classical / Modern Mode)\*\*\[cite: 12\] |

| \*\*భిన్నయతి (6.40)\*\*\[cite: 12\] | Verbs formed with suffix \*\*-iñcu\*\*\[cite: 12\] | \*\*Dual Track:\*\* Match vowel \*\*'ఇ'\*\* of \*-iñcu\* OR match host surface consonant\[cite: 12\]. Valid across all 3 root types (doublets, unaugmented, non-doublets)\[cite: 12\]. | \*\*Canonical\*\*\[cite: 12\] |

| \*\*నిత్యయతి (6.41)\*\*\[cite: 12\] | Compounds formed with enclitic \*\*-ēni\*\*\[cite: 12\] | \*\*Dual Track:\*\* Match vowel \*\*'ఏ'\*\* under Class 2 Svara Yati OR match surface consonant (\*\*నే, దే, పే\*\*)\[cite: 12\]. | \*\*Canonical\*\*\[cite: 12\] |

| \*\*విభాగ యతి (6.42)\*\*\[cite: 12\] | Distributive forms with \*\*-ēsi\*\* (also \*-e'ḍu, \-ava\*)\[cite: 12\] | \*\*Dual Track:\*\* Match vowel \*\*'ఏ'\*\* of \*-ēsi\* under Class 2 Svara Yati OR match surface consonant (\*\*గే, డే, తే\*\*)\[cite: 12\]. | \*\*Canonical\*\*\[cite: 12\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.42.2 'ఎఁడు' ప్రత్యయమునకు యతి (Mānārthaka '-e'ḍu' Quantitative Suffix Yati)

* **Grammatical Formation:** Governed by *Bāla Vyākaraṇam* (Taddhita 25: *"మానార్థంబునకేకత్వంబునందెఁడు వర్ణకంబగు"*), the suffix **'-ఎఁడు'** (*\-e'ḍu*) attaches to singular nouns to designate a volumetric measurement (e.g., *తూము \+ ఎఁడు \= తూమెఁడు*; *వీసె \+ ఎఁడు \= వీసెఁడు*; *గంప \+ ఎఁడు \= గంపెఁడు*).  
* **Elision of Base Stems:** By *Bāla Vyākaraṇam* (Taddhita 26), when '-ఎఁడు' attaches to stems ending in *'లి'*, the *'లి'* elides: *దోసిలి \+ ఎఁడు $\\rightarrow$ దోసెఁడు*; *పిడికిలి \+ ఎఁడు $\\rightarrow$ పిడికెఁడు*; *పుడిసిలి \+ ఎఁడు $\\rightarrow$ పుడిసెఁడు*.  
* **Caesura Licensing:** Like the distributive suffix *\-ēsi*, compounding with measurement suffix *\-e'ḍu* is grammatically eligible for dual-track Ubhaya Yati. In classical practice, poets almost universally match the **resulting surface consonant track**.  
* **Critical Engine Disambiguation:**  
* *Volumetric Suffix (-ఎఁడు):* Attaches to nouns to denote capacity (*దోసెఁడు, పుడిసెండు*). Eligible for Ubhaya Yati categorization.  
* *Verbal Suffix / Infix (-ఎడు / \-ఎడున్):* Occurs in finite verbs and habitual participles (*వండెడును, కలిగెడును, పలికెడు, ఉండెడు*). **Does not indicate measurement and has zero Ubhaya Yati license**; it must strictly scan as a standard consonant yati on the surface consonant (Section 6.77).  
* **Provenance (Consonant Track):**  
* **జె $\\longleftrightarrow$ సె \[పుడిసెండు\]:** *చీడపుర్వు దాఁజెడఁదినునింతెకాక పుడిసెండు జలంబిడి పెంపనేర్చునే...* ($\\text{జె} \\longleftrightarrow \\text{సె}$ via *Sarasayati-4*) (*Bhāskara Śatakam*).

---

### 6.42.3 'అవ' ప్రత్యయమునకు ఉభయ యతులు (Pūraṇārthaka '-ava' Ordinal Dual Caesura)

* **Grammatical Formation:** By *Bāla Vyākaraṇam* (Ācchika 25: *"సంఖ్యకుం బూరణార్థమునందవగాగమంబగు"*), the ordinal suffix augment **'-అవ'** (*\-avagāgamamu*) attaches to cardinal numbers to derive ordinal rankings (*రెండు \+ అవ \= రెండవ*; *మూఁడు \+ అవ \= మూఁడవ*; *నాలుగు \+ అవ \= నాలవ*; *పదుమూఁడు \+ అవ \= పదుమూఁడవ*; *ఎనిమిది \+ అవ \= ఎనిమిదవ*).  
* **The Dual-Track Rule:** Because the numerical base fuses obligatorily with *\-ava*, forming an integrated ordinal compound word, the caesura coordinate at this junction licenses **Ubhaya Yati**:  
* **Track 1 (Svara Track):** Disregard the host consonant and match the underlying junction vowel **'అ'** (*a*) of *\-ava* under *Class 1 Svara Yati* (**అ, ఆ, ఐ, ఔ**).  
* **Track 2 (Vyañjana Track):** Match the resulting surface consonant (**డవ, లవ**) under consonant *Prāṇi* or *Vargaja Yati*.

                 Ordinal '-ava' Dual Engine Routing

               \[ Cardinal Stem \+ Ordinal Augment: \-ava \]

                                   │

        ┌──────────────────────────┴──────────────────────────┐

        ▼                                                     ▼

   Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga

  (Matches vowel 'అ' of \-ava)                           (Matches surface compound consonant)

  • మూఁడవ ⟷ అ/ఆ/ఐ/ఔ                                    • రెండవ \[డ\] ⟷ ట/ఠ/డ/ఢ (Vargaja)

  • నాలవ ⟷ అ/ఆ/ఐ/ఔ                                      • నాలవ \[ల\] ⟷ ల/ళ (Abhēda)

  (Class 1 Svara Equivalence)                           (Consonant Class Preserved)

\`\`\`\[cite: 13\]

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.42.3)

\* \*\*Track 1: Vowel Matches on 'అ' (Svara Track):\*\*

  \* \*\*ఆ $\\longleftrightarrow$ నాలవ \[అ\]:\*\* \*సుకరంపుమార్గమాయువు మొదలి నాలవపాలు గురుపాల...\* ($\\text{మార్గము} \+ \\mathbf{ఆయువు} \\longleftrightarrow \\text{నాలుగు} \+ \\mathbf{అవ} \\implies \\mathbf{ఆ \\longleftrightarrow అ}$ Svara Yati) (\*Bhāratam\*, Śānti 5-136)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ మూఁడవ \[అ\]:\*\* \*...మూడవ సవనంబునన్ శ్రుతి సమభ్యధికంబుగఁ...\* ($\\text{మూఁడు} \+ \\mathbf{అవ} \\longleftrightarrow \\text{సమ్} \+ \\mathbf{అభ్యధిక} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati) (\*Bhāratam\*, Āraṇya 3-243)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ రెండవ \[అ\]:\*\* \*...రెండవ కాండంబుఁ దదస్త్రమున్ గొనక డాయన్వచ్చి...\* ($\\text{రెండు} \+ \\mathbf{అవ} \\longleftrightarrow \\mathbf{డాయన్వచ్చి} \\implies \\mathbf{అ \\longleftrightarrow య}$ via \*Sarasayati-2\*) (\*Bhāratam\*, Virāṭa 4-46)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ రెండవ \[అ\]:\*\* \*...రెండవ వినతా తనూభవుని యందమునం గమనీయ...\* ($\\text{రెండు} \+ \\mathbf{అవ} \\longleftrightarrow \\mathbf{య్ \+ అం} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati) (\*Pārijātāpaharaṇamu\* 2-85)\[cite: 13\].

\* \*\*Track 2: Consonant Matches on Surface Stems (Vyañjana Track):\*\*

  \* \*\*ల $\\longleftrightarrow$ నాలవ \[ల\]:\*\* \*...నాలవ వాఁడు నిశరుఁడుల్లఱపు బిరుదు...\* ($\\text{నాలుగు} \+ \\text{అవ} \= \\text{నాలవ} \\implies \\mathbf{ల \\longleftrightarrow ల్ల\\ \[ల\]}$ Prāṇi Yati) (\*Bhāgavatam\* 4-200)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ పదుమూఁడవ \[డ\]:\*\* \*...పదుమూఁడవయెడ విరతిఁబొసఁగిన బెడఁగడరుఁ గనకలతన్...\* ($\\text{పదుమూఁడు} \+ \\text{అవ} \\implies \\mathbf{డ \\longleftrightarrow డ}$ Prāṇi Yati) (\*Appakavīyamu\* 4-345, Kanakalatā Vṛtta)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ రెండవ \[డ\]:\*\* \*...రెండవ కక్ష్యాంతరమున్ రమాధిపుఁడు వేడ్కనొసఁగి...\* ($\\text{రెండు} \+ \\text{అవ} \\implies \\mathbf{డ \\longleftrightarrow డ్క\\ \[డ\]}$ Prāṇi Yati) (\*Uttara Rāmāyaṇamu\* 8-298)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.43 యుష్మదస్మదాది శబ్ద యతి (Yushmadasmadādi Śabda Yati — Pronominal Compound Dual Caesura)

&nbsp;

\* \*\*Morphological Environment:\*\* Governs Sanskrit pronominal bases ending in consonant \*\*'ద్'\*\* (\*d-kārānta prātipadikas\*), primarily \*\*యుష్మద్\*\* (\*yuṣmad\* \= second person / thou) and \*\*అస్మద్\*\* (\*asmad\* \= first person / I), compounding with an initial vowel (\*ajādi śabda\*):

  \* $\\text{యుష్మద్} \+ \\text{ఆగమన} \= \\mathbf{యుష్మదాగమన}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{ఉదర} \= \\mathbf{అస్మదుదర}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{అన్వయ} \= \\mathbf{అస్మదన్వయ}$\[cite: 13\]

  \* $\\text{యుష్మద్} \+ \\text{ఆజ్ఞా} \= \\mathbf{యుష్మదాజ్ఞా}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{ఆది} \= \\mathbf{అస్మదాది}$\[cite: 13\]

\* \*\*The Structural Rule:\*\* At the resulting dental stop juncture (\*\*ద, దా, దు\*\*, etc.), the engine licenses \*\*Ubhaya Yati\*\*\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Disregard the dental stop and match the initial vowel of the second component (\*para-padādi svara\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant (\*\*ద\*\*) under \*Prāṇi\* or \*Vargaja Yati\* (\*\*త, థ, ద, ధ\*\*)\[cite: 13\].

&nbsp;

&nbsp;

             Pronominal Dual Engine Routing

      \[ Pronominal Base (యుష్మద్ / అస్మద్) \+ Vowel Stem \]

                               │

    ┌──────────────────────────┴──────────────────────────┐

    ▼                                                     ▼

&nbsp;

Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga (Matches vowel of second word)                        (Matches surface dental consonant 'ద') • యుష్మదాగమన ⟷ అ/ఆ/ఐ/ఔ                                • యుష్మదాజ్ఞా \[దా\] ⟷ త/థ/ద/ధ (Vargaja) • అస్మదుదర ⟷ ఉ/ఊ/ఒ/ఓ                                  • అస్మదాదులు \[దా\] ⟷ త/థ/ద/ధ (Vargaja) (Svara-Pradhāna Resolution)                           (Dental Stop Class Preserved)

&nbsp;

\* \*\*Class Extension (యుష్మదస్మదాది శబ్దములు 6.43.1):\*\*

  While Appakavi framed this rule around \*yuṣmad\* and \*asmad\*, classical usage extends identical dual-track licensing to all Sanskrit \*d-ending\* and \*t-ending\* pronominal bases: \*\*భవత్\*\* (\*bhavat\*), \*\*తద్\*\* (\*tad\*), \*\*యద్\*\* (\*yad\*), and \*\*ఏతద్\*\* (\*ētad\*)\[cite: 13\]:

  \* $\\text{భవత్} \+ \\text{అగ్రజ} \= \\mathbf{భవదగ్రజ}$\[cite: 13\]

  \* $\\text{భవత్} \+ \\text{అంఘ్రి} \= \\mathbf{భవదంఘ్రి}$\[cite: 13\]

  \* $\\text{భవత్} \+ \\text{ఆత్మ} \= \\mathbf{భవదాత్మ}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{అగ్ర} \= \\mathbf{తదగ్ర}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{ఆశ్రమ} \= \\mathbf{తదాశ్రమ}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{ఆరూఢ} \= \\mathbf{తదారూఢ}$\[cite: 13\]

&nbsp;

\#\#\#\# Philological Defense of Nannaya's Text (\*Mahābhārata\*, Ādi 2-216) (6.43)

\* \*The Stanza:\* \*ప్రస్తుత ఫణిసత్ర భయత్రస్తాత్ములమైన యస్మదాదులకెల్లన్...\* (\*\*త్ర \[త\] $\\longleftrightarrow$ అస్మదాదులు \[దా\]\*\*)\[cite: 13\].

\* \*The Scribal Corruption:\* Purists who rejected consonant matching on \*asmad\* altered Nannaya's line to \*...భయాయస్తాత్ములమైన...\*, claiming \*భయత్రస్త\* created a semantic tautology ("frightened by fear") and forcing a vowel match (\*\*య $\\longleftrightarrow$ ఆ\*\*)\[cite: 13\].

\* \*The Refutation:\* The root \*tras\* denotes torment or agitation (\*pīḍita / udvigna\*); \*భయత్రస్త\* authentically signifies "afflicted by fear," harmonizing with Nannaya’s closing verse in that section (\*జననీ శాప భయప్రపీడిత...\*)\[cite: 13\]. Nannaya's authentic reading confirms consonant-track matching (\*\*త $\\longleftrightarrow$ దా\*\* via \*Vargaja Yati\*)\[cite: 13\].

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.43, 6.43.1)

\* \*\*Primary Yuṣmad / Asmad Stanzas:\*\*

  \* \*\*య $\\longleftrightarrow$ యుష్మదాగమన \[ఆ\] (Svara):\*\* \*...దివ్యతపోధనవర్య యుష్మదాగమనమునన్...\* (\*Sāmbōpākhyānamu\* / \*Appakavīyamu\* 3-123)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ అస్మదన్వయ \[అ\] (Svara):\*\* \*...నతిపావనమయ్యెనస్మదన్వయ మెల్లన్...\* (\*Sāmbōpākhyānamu\* / \*Appakavīyamu\* 3-123)\[cite: 13\].

  \* \*\*ధ $\\longleftrightarrow$ యుష్మదాజ్ఞా \[దా\] (Consonant):\*\* \*ధర్మతనయ యుష్మదాజ్ఞానిగళ వినిబద్ధమగుచు...\* (\*Adharvaṇa Virāṭaparva\* / \*Appakavīyamu\* 3-124)\[cite: 13\].

  \* \*\*త్ర \[త\] $\\longleftrightarrow$ అస్మదాదులు \[దా\] (Consonant):\*\* \*...భయత్రస్తాత్ములమైన యస్మదాదులకెల్లన్...\* (\*Bhāratam\*, Ādi 2-216)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ అస్మదుదర \[ఉ\] (Svara):\*\* \*...విశ్రమమొనరించితె యనఘ యస్మదుదరములోనన్...\* (\*Bhāratam\*, Udyōga 4-259)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ అస్మదాశ్రమ \[ఆ\] (Svara):\*\* \*...పువ్వుబోఁడియనినఁ గలిగెనస్మదాశ్రమంబుననని...\* (\*Bhāratam\*, Sabhā 2-209)\[cite: 13\].

  \* \*\*యుష్మదనుజు \[అ\] $\\longleftrightarrow$ య (Svara):\*\* \*యుష్మదనుజుఁ జంపిన వారలీ యక్షవరులు...\* (\*Bhāratam\*, Virāṭa 4-366)\[cite: 13\].

\* \*\*Bhavat / Tad Pronominal Extension Corpus (6.43.1):\*\*

  \* \*\*అ $\\longleftrightarrow$ భవదగ్రజ \[అ\] (Svara):\*\* \*...యిట్లను హరినాశ్రయించి భవదగ్రజుఁ బుణ్యునజాతశత్రునిన్...\* (\*Bhāratam\*, Udyōga 3-349)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ భవదంఘ్రుల \[ద\] (Consonant):\*\* \*...దావక సేవకుండ భవదంఘ్రుల నేనిటఁగొల్చి వచ్చెదన్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 143)\[cite: 13\].

  \* \*\*ద $\\longleftrightarrow$ భవదాత్మ \[దా\] (Consonant):\*\* \*...దనరనందుపశాఖలై భవదాత్మ దీనికి మూలమై...\* (\*Bhāgavatam\* 3-305)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ తదగ్ర \[అ\] (Svara):\*\* \*ఆతని సమ్ముఖంబునఁ దదగ్రతనూజు కడన్...\* (\*Bhāratam\*, Virāṭa 4-1-39)\[cite: 13\].

  \* \*\*తం \[త\] $\\longleftrightarrow$ తదాశ్రమ \[దా\] (Consonant):\*\* \*...మాతంగమునెక్కి యింద్రుఁడు తదాశ్రమవీథిని వచ్చుచోఁ...\* (\*Ahalya\* 2-119)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ తదారూఢ \[దా\] (Consonant):\*\* \*...భావమునఁ దదారూఢప్రీతి మొగము దగఁ గైసేయన్...\* (\*Rāghavapāṇḍavīyamu\* 3-138)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.44 కాకుస్వర యతి / ప్లుతయతి (Kākusvara Yati / Pluta Yati — Emotional Protraction Dual Caesura)

&nbsp;

\* \*\*Phonological Definition of Kāku & Pluta:\*\*

  \* \*కాకువు (Kāku):\* Modulation or inflection of the voice triggered by intense emotional states (grief, fear, doubt, interrogation, entreaty, anger)\[cite: 13\].

  \* \*ప్లుతము (Pluta):\* The protracted lengthening of a vowel beyond standard long-vowel duration ($1 \\text{ mātrā} \= \\text{hrasva/laghu}$; $2 \\text{ mātrās} \= \\text{dīrgha/guru}$; $3 \\text{ mātrās} \= \\text{pluta/guru}$)\[cite: 13\].

  \* \*Prosodic Weight:\* While a pluta vowel occupies 3 mātrās phonetically, metrical scansion treats it simply as heavy (\*\*Guru / U\*\*)\[cite: 13\].

\* \*\*The Dual-Track Rule (కాకుస్వర యతి):\*\*

  At a syllable marked by emotional protraction (\*kākusvara / pluta\*)\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Disregard the host consonant and match the prolonged vowel sound (\*\*'ఆ', 'ఈ', 'ఏ', 'ఓ'\*\*) under \*Svara Yati\*\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Disregard the vocalic protraction and match the host consonant under standard consonant \*Prāṇi, Vargaja, Ūṣma\*, or \*Sarasayati\*\[cite: 13\].

&nbsp;

&nbsp;

             Kākusvara Dual Engine Routing

           \[ Syllable Modified by Emotional Kāku/Pluta \]

                                │

    ┌───────────────────────────┴───────────────────────────┐

    ▼                                                       ▼

&nbsp;

Track 1: Svara Mārga                                    Track 2: Vyañjana Mārga (Matches the protracted vowel:                          (Matches the surface host consonant: ఆ, ఈ, ఏ, ఓ)                                            ప, త, ద, ర, etc.) │                                                       │ e.g., నాథా\! ⟷ అ/ఆ/ఐ/ఔ                                   e.g., నాథా\! \[థా\] ⟷ త/థ/ద/ధ e.g., రావే\! ⟷ ఇ/ఈ/ఎ/ఏ                                   e.g., రావే\! \[వే\] ⟷ వ/బ/ప/ఫ/భ

&nbsp;

\#\#\#\# The 10 Functional Categories of Pluta (6.44.1)

&nbsp;

| \# | Semantic Category | Typical Markers | Contextual Illustration |

| :-: | :--- | :--- | :--- |

| 1 | \*\*శోకప్లుతము (Grief / Lamentation)\*\*\[cite: 13\] | అకటా\!, అయ్యో\!, హా\!, రావే\!\[cite: 13\] | Crying out in bereavement or intense sorrow\[cite: 13\]. |

| 2 | \*\*తర్కప్లుతము (Deliberation / Logic)\*\*\[cite: 13\] | కాదా\!, లేదా\!, ఏలా\!, పోరో\!\[cite: 13\] | Weighing arguments, moral reasoning, deduction\[cite: 13\]. |

| 3 | \*\*సంబోధనప్లుతము (Vocative / Address)\*\*\[cite: 13\] | తండ్రీ\!, నాథా\!, రాజా\!, వత్సా\!\[cite: 13\] | Direct vocative address with lengthened vowel\[cite: 13\]. |

| 4 | \*\*దూరాహ్వానప్లుతము (Calling from Afar)\*\*\[cite: 13\] | వీరులారా\!, రావే\!, రారమ్మో\!\[cite: 13\] | Projecting voice across distance to call someone\[cite: 13\]. |

| 5 | \*\*సంశయప్లుతము (Doubt / Uncertainty)\*\*\[cite: 13\] | కదా\!, కలదే\!, ఏమో\!, ఎట్లో\!\[cite: 13\] | Hesitation, skepticism, uncertain contemplation\[cite: 13\]. |

| 6 | \*\*ప్రశ్నప్లుతము (Interrogation)\*\*\[cite: 13\] | వింటే?, ఆతఁడా?, రావలదే?\[cite: 13\] | Direct questioning seeking verification\[cite: 13\]. |

| 7 | \*\*ఆశ్చర్యప్లుతము (Wonder / Exclamation)\*\*\[cite: 13\] | అకటా\!, బలే\!, నెగసిరో\!\[cite: 13\] | Astonishment, surprise, sudden realization\[cite: 13\]. |

| 8 | \*\*ప్రార్థనప్లుతము (Supplication / Entreaty)\*\*\[cite: 13\] | ప్రోవవే\!, తెల్పఁగదవే\!, ఈవే\!\[cite: 13\] | Pleading, urgent requests for grace or aid\[cite: 13\]. |

| 9 | \*\*భీతిప్లుతము (Fear / Terror)\*\*\[cite: 13\] | చుండో\!, మూఁడెనో\!, రారక్కసో\!\[cite: 13\] | Shivering alarm or impending catastrophe\[cite: 13\]. |

| 10 | \*\*గానప్లుతము / స్తుతి (Musical Chanting)\*\*\[cite: 13\] | గంగా\!, హరీ\!, ప్రభూ\!\[cite: 13\] | Musical elongation in poetic praise\[cite: 13\]. |

&nbsp;

\#\#\#\# Treatise Formulations & Provenance Trail (6.44.2 – 6.44.4)

\* \*\*Appakavi's Dual Benchmark Demonstrations (3-250, 3-252):\*\*

  \* \*Appakavīyamu (3-250 — Dūrāhvāna):\*

    \* Line 1 (Svara Track): \*\*ఆ $\\longleftrightarrow$ పద్మా\! \[ఆ\]\*\*\[cite: 13\].

    \* Line 2 (Consonant Track): \*\*ద్వా \[దా\] $\\longleftrightarrow$ సద్మా\! \[దా\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

    \* Line 3 (Svara Track): \*\*అ $\\longleftrightarrow$ వీరులారా\! \[ఆ\]\*\*\[cite: 13\].

    \* Line 4 (Consonant Track): \*\*ర $\\longleftrightarrow$ వాసులారా\! \[రా\]\*\* (\*Ēkatara Yati\*)\[cite: 13\].

  \* \*Appakavīyamu (3-252 — Saṁśaya/Praśna):\*

    \* Line 1 (Svara Track): \*\*హ $\\longleftrightarrow$ ఆతఁడా? \[ఆ\]\*\* (\*Sarasayati\*)\[cite: 13\].

    \* Line 2 (Consonant Track): \*\*డం $\\longleftrightarrow$ ఈతఁడా? \[డా\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

    \* Line 3 (Svara Track): \*\*ఎ $\\longleftrightarrow$ అబ్బెనే\! \[ఏ\]\*\* (\*Svara Yati\*)\[cite: 13\].

    \* Line 4 (Consonant Track): \*\*నె $\\longleftrightarrow$ గలుఁగునే? \[నే\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

\* \*\*Track 1 Corpus (Vowel Track Matches 6.44.3):\*\*

  \* \*\*అ $\\longleftrightarrow$ అకటా\! \[ఆ\] (Śōka):\*\* \*యడవులలోన సీత యకటా\! యిఁకఁజూడక...\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 72)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ రావే\! \[ఏ\] (Śōka):\*\* \*హా యనునో నరేంద్ర యను హా\! రఘుకుంజర నీవు వేగ రావే\! యనునెంత...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 112)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ వింటే? \[ఏ\] (Śōka/Praśna):\*\* \*...నాయెలుంగు వింటే? యను విన్న...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 112)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ మొఱ్ఱా\! \[ఓ\] (Śōka):\*\* \*ఒక్క దనుజాధముండు మొఱ్ఱా\! యనంగ...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 177)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ గాదా\! \[ఆ\] (Tarka):\*\* \*...కంటింపన్మఱి రాదె పూజనము గాదా\! ప్రాణిమేల్చక్రికిన్...\* (\*Bhāgavatam\* 6-58)\[cite: 13\].

  \* \*\*ఔ $\\longleftrightarrow$ లేదా\! \[ఆ\] (Tarka):\*\* \*...వాఁడౌనేనౌనొక జాడఁ బోయెదము లేదా\! జీవమింకేటికిన్...\* (\*Haravilāsam\* 2-123)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ దోఁచునే\! \[ఏ\] (Tarka):\*\* \*...మనమునకున్ ఈ విజ్ఞానంబు దోఁచునే\! వెఱపేలా...\* (\*Bhāratam\*, Anuśāsanika 2-192)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ పోరో\! \[ఓ\] (Tarka):\*\* \*...కోహెూ చాలుఁబొ కాలిపోయెదరొ పోరో\! నోటిక్రొవ్వేటికిన్...\* (\*Manu Caritra\* 6-45)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ సిరాలా\! \[ఆ\] (Saṁbōdhana):\*\* \*...నందన సిరాలా\! వీరశైవవ్రతా...\* (\*Haravilāsam\* 2-117)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ వనితా\! \[ఆ\] (Saṁbōdhana):\*\* \*అన మునిరాజు పల్కు వనితా\! జనతావినుతాభిధేయుఁడై...\* (\*Manu Caritra\* 2-91)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ వత్సా\! \[ఆ\] (Saṁbōdhana):\*\* \*...వత్సా\! విను మావంటి తైర్థికావళికెల్లన్...\* (\*Manu Caritra\* 1-65)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ మహాత్మా\! \[ఆ\] (Saṁbōdhana):\*\* \*...వింతలు మహాత్మా\! నాకెఱింగింపవే...\* (\*Manu Caritra\* 1-68)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ రాజా\! \[ఆ\] (Saṁbōdhana):\*\* \*హతశేషుండు నిజాకృతిన్ నిలిచి రాజా\! నిర్నిమిత్తంబునా...\* (\*Amuktamālyada\* 7-88)\[cite: 13\].

  \* \*\*ఇ $\\longleftrightarrow$ మూర్తీ\! \[ఈ\] (Saṁbōdhana):\*\* \*యిలపైనొక్కెడఁ గల్గెనేననఘమూర్తీ\! తెల్పవే...\* (\*Haravilāsam\* 1-96)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ స్వామీ\! \[ఈ\] (Saṁbōdhana):\*\* \*...స్వామీ\! పద్మాసన యార్తులన్ మముఁగృపాదృష్టిన్...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 174)\[cite: 13\].

  \* \*\*ఋ \[పృ\] $\\longleftrightarrow$ స్వామీ\! \[ఈ\] (Saṁbōdhana):\*\* \*పృతనాసాహుఁడు వేయి యేఁడులుగ స్వామీ\! నన్నుఁ...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 538)\[cite: 13\].

  \* \*\*యి $\\longleftrightarrow$ తండ్రీ\! \[ఈ\] (Saṁbōdhana):\*\* \*...ఎందరిగెఁదండ్రీ\! బుద్ధినూహింపుమా...\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 121)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ రావే\! \[ఏ\] (Dūrāhvāna):\*\* \*ప్రోవ రావే\! వసుభూపయంచునెలుఁగెత్తి...\* (\*Haravilāsam\* 2-141)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ గదా\! \[ఆ\] (Saṁśaya):\*\* \*...చూతముగదా\! యని యంపిననాక్షణంబునన్...\* (\*Manu Caritra\* 2-78)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ కదా\! \[ఆ\] (Saṁśaya):\*\* \*హరిహయుఁడేమియయ్యెనొ కదా\! మదనానల...\* (\*Kāśīkhaṇḍam\* 4-65)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ గలదే\! \[ఏ\] (Saṁśaya):\*\* \*ఈ కొఱదీఱు తీరుగలదే\! బలశాలులు...\* (\*Kavitrayam\* 8-17)\[cite: 13\].

  \* \*\*ఉ $\\longleftrightarrow$ చేయుటకునో\! \[ఓ\] (Saṁśaya):\*\* \*...నన్నుత్తలమందఁ జేయుటకునో\! తలపోసి...\* (\*Bhāratam\*, Virāṭa 2-84)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ నగనేలా? \[ఆ\] (Praśna):\*\* \*అని చెప్పన్ విని సిద్ధుఁజూచి నగనేలా? యింత భవ్యాత్మ...\* (\*Appakavīyamu\* 3-53)\[cite: 13\].

  \* \*\*ఇ $\\longleftrightarrow$ రావలదే? \[ఏ\] (Praśna):\*\* \*...సారమేయమిదియట రావలదే? నా మనంబు...\* (\*Bhāratam\*, Mahāprasthānika 52)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ కనుగొంటే? \[ఏ\] (Praśna):\*\* \*ఏణీశాబవిలోలనేత్ర కనుగొంటే? వీరు విద్యాధరుల్...\* (\*Manu Caritra\* 2-91)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ అకటా\! \[ఆ\] (Āścarya):\*\* \*గేహనివహసాత్కరించి యకటా\! కడు రిక్తతనొందునే...\* (\*Amuktamālyada\* 4-32)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ నెగసిరో\! \[ఓ\] (Āścarya):\*\* \*...జలకేళి సల్పఁగానొలసి రయంబునన్నెగసిరో\! యని చూపఱు...\* (\*Bhāgavatam\* 9-83)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ మానవుగదా\! \[ఆ\] (Prārthanā):\*\* \*...నేననియెదనల్కమానవుగదా\! యిఁకనైన...\* (\*Śivarātri Māhātmyamu\* 1-123)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ రావే\! \[ఏ\] (Prārthanā):\*\* \*...ఈ యపమృత్యువుంగడపరావే\! యంచుఁగీర్తింపఁగన్...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 154)\[cite: 13\].

  \* \*\*హీ $\\longleftrightarrow$ బ్రోవవే\! \[ఏ\] (Prārthanā):\*\* \*హీనస్వరమెసఁగఁ బ్రోవవే\! నన్ననుచున్...\* (\*Haravilāsam\* 6-34)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ చేటు మూఁడెనో\! \[ఓ\] (Bhīti):\*\* \*...చేటు మూఁడెనో\! పురిలోనొక్క యుమ్మడినింటింట...\* (\*Bhāratam\*, Drōṇa 3-24)\[cite: 13\].

  \* \*\*ఆ \[గంగా\!\] $\\longleftrightarrow$ య (Gāna/Stuti):\*\* \*...మరందాయిత గంగా\! కాకోదరనగోదయస్థ...\* (\*Kāśīkhaṇḍam\* 6-1)\[cite: 13\].

\* \*\*Track 2 Corpus (Consonant Track Matches 6.44.4):\*\*

  \* \*\*టా \[అకటకటా\!\] $\\longleftrightarrow$ ఢ (Vargaja):\*\* \*చిత్తునకటకటా\! యని పోనిండు నను దృఢవ్రత...\* (\*Bhāratam\*, Śānti 1-203)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ కదా\! \[దా\] (Prāṇi):\*\* \*...రమావలేపముగదా\! యని యోర్తు...\* (\*Manu Caritra\* 3-161)\[cite: 13\].

  \* \*\*మా $\\longleftrightarrow$ మ \[మహిమా\!\]:\*\* \*...విమలతపోమహిమా\! యిన్ని దినంబులేల మసలితి...\* (\*Bhāratam\*, Ādi 1-116)\[cite: 13\].

  \* \*\*మా \[రమ్మా\!\] $\\longleftrightarrow$ మ:\*\* \*...రమ్మా\! చూతముగాని నీ గమన వేగంబున్...\* (\*Bhāratam\*, Virāṭa 2-89)\[cite: 13\].

  \* \*\*రా\! $\\longleftrightarrow$ రా:\*\* \*...జయ నామకంబనను రాజితభంగి...\* (\*Bhāratam\*, Svargārohaṇa 89)\[cite: 13\].

  \* \*\*వి $\\longleftrightarrow$ రావే\! \[వే\] (Prāṇi):\*\* \*వినఁగావచ్చెఁ బ్రియంవదా మగుడి రావే\! యంచు...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 51)\[cite: 13\].

  \* \*\*కు $\\longleftrightarrow$ అగునొకో\! \[కో\] (Prāṇi):\*\* \*కుసుమ సముద్గమంబగునొకో\! పతిలాభము...\* (\*Bhāratam\*, Ādi 3-170)\[cite: 13\].

  \* \*\*మో $\\longleftrightarrow$ ఏమో\! \[మో\] (Prāṇi):\*\* \*మోదింపం గలలోఁ గుమారుఁడొకఁడేమో\! చేసినం...\* (\*Bhāgavatam\* 5-84)\[cite: 13\].

  \* \*\*ధీ $\\longleftrightarrow$ మఱచితే? \[తే\] (Vargaja):\*\* \*ధీయుత అని పలికె మఱచితే? మునినాథా...\* (\*Bhāratam\*, Ādi 8-317)\[cite: 13\].

  \* \*\*ద $\\longleftrightarrow$ మఱచితా? \[తా\] (Vargaja):\*\* \*దనుతల దుంపవే మఱచితా? యిసిరో...\* (\*Bhāratam\*, Mauṣala 44)\[cite: 13\].

  \* \*\*ల $\\longleftrightarrow$ ఏలా? \[లా\] (Prāṇi):\*\* \*లలనా విష్ణుఁడనంగనెవ్వఁడతఁడేలా? శుద్ధ...\* (\*Manu Caritra\* 5-10)\[cite: 13\].

  \* \*\*ని $\\longleftrightarrow$ వింటే? \[ంటే\] (Anunāsikākṣara):\*\* \*నినుఁబోలంగలరబ్జగంధులన వింటే? యెందు...\* (\*Amuktamālyada\* 2-25)\[cite: 13\].

  \* \*\*తీ $\\longleftrightarrow$ ఏదీ? \[దీ\] (Vargaja):\*\* \*...నతీరుండూరక తప్పువట్టెనట యేదీ? లక్షణంబో...\* (\*Appakavīyamu\* 3-167)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ అకటా\! \[టా\] (Vargaja):\*\* \*డక్కెను రాజ్యమంచునకటా\! యిటు దమ్ముని...\* (\*Bhāratam\*, Virāṭa 2-52)\[cite: 13\]; \*...డక్క గొనంగ రాదె యకటా\! నను వీఁడు...\* (\*Haravilāsam\* 2-35)\[cite: 13\].

  \* \*\*లి $\\longleftrightarrow$ బలే\! \[లే\] (Prāṇi):\*\* \*...వాలి రాలి దరికొన్నను దేలిన దెస వ్రాలకుండిన బలే\! మముబోఁటులకుం...\* (\*Bhāratam\*, Virāṭa 2-97)\[cite: 13\].

  \* \*\*ర \[ప్ర\] $\\longleftrightarrow$ ఔరా\! \[రా\] (Ēkatara):\*\* \*ప్రభువేదాద్రి లిఖించు వ్రాయసములౌరా\! పెద్ద...\* (\*Haravilāsam\* 1-81)\[cite: 13\].

  \* \*\*వె $\\longleftrightarrow$ తెల్పఁగదవే\! \[వే\] (Prāṇi):\*\* \*వెలఁది మనంబు తెల్పఁగదవే\! మణిహారమ...\* (\*Manu Caritra\* 4-103)\[cite: 13\].

  \* \*\*వే $\\longleftrightarrow$ ఆనతీవే\! \[వే\] (Prāṇi):\*\* \*...పుట్టువు దీఱెడుదాఁకనానతీవే\! యని విన్నవింప...\* (\*Appakavīyamu\* 4-141)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.45 ప్లుతయుగ యతి (Plutayuga Yati — Symmetrical Double-Pluta Caesura)

&nbsp;

\* \*\*Definition & Structural Principle:\*\* Governs lines where \*\*BOTH coordinates (the line onset and the internal caesura) are emotionally protracted pluta syllables\*\*\[cite: 13\]:

  $$\\text{Line Onset Bearer: } \[\\text{C}\_1 \+ \\mathbf{\\text{Pluta}\_1}\] \\quad\\longleftrightarrow\\quad \\text{Caesura Coordinate: } \[\\text{C}\_2 \+ \\mathbf{\\text{Pluta}\_2}\]$$\[cite: 13\]

\* \*\*The Phonetic License:\*\* Even if Consonant $\\text{C}\_1$ and Consonant $\\text{C}\_2$ have \*\*ZERO consonantal affinity\*\* (e.g., labial \*\*'వ'\*\* and dental \*\*'ద'\*\*), the caesura is metrically valid if their prolonged pluta vowels share mutual Svaramaitri equivalence\[cite: 13\]\!

\* \*\*Nomenclature:\*\* Designated \*\*ప్లుతయుగ విశ్రామము\*\* (\*Plutayuga Viśrāmamu\* \= Twin-Pluta Caesura) by Appakavi\[cite: 13\].

\* \*\*Systemic Verification Prerequisites (6.45):\*\*

  1\. \*Dual Verification:\* Both syllables must carry genuine, contextually attested emotional kākusvaras\[cite: 13\]. If one syllable is an ordinary long vowel (e.g., \*వేగము కావవే...\*), the rule fails\[cite: 13\].

  2\. \*Vowel Class Parity:\* The pluta vowels must belong to the exact same Svaramaitri class\[cite: 13\]. Pairing a Class 2 pluta (\*\*'ఏ'\*\*) with a Class 1 pluta (\*\*'ఆ'\*\*) is an invalid metrical break\[cite: 13\].

  3\. \*Consonant Non-Affinity Domain:\* If $\\text{C}\_1$ and $\\text{C}\_2$ already share natural consonantal affinity (e.g., \*\*థా\! $\\longleftrightarrow$ దా\!\*\*), the line resolves simply under \*Vargaja Yati\*, rendering Plutayuga invocation unnecessary\[cite: 13\].

\* \*\*Independence from Semantic Equivalence:\*\* The two plutas need not express identical emotions; a line may validly pair an entreaty pluta (\*prārthanā\*) with an interrogative pluta (\*praśna\*)\[cite: 13\].

&nbsp;

\#\#\#\# Classical Attestations & Provenance Trail (6.45, 6.45.1)

\* \*\*Appakavi's Definitive Stanza (\*Vajrapañjara Śatakam\* / \*Appakavīyamu\* 3-257):\*\*

  \* \*నీవే\! గతి కావవే రఘుపతీ\! శరణాగత వజ్రపంజరా\* (\*\*నీవే\! \[ఏ\] $\\longleftrightarrow$ రఘుపతీ\! \[ఈ\]\*\*; Class 2 Vowel Class match between non-homorganic consonants \*\*వ\*\* and \*\*ప\*\*)\[cite: 13\].

\* \*\*Corpus Proof Across Pluta Classes:\*\*

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Praśna):\*\* \*మాయరవి యేల క్రుంకఁడొకో\! \[ఓ\] యనునిట్టేల తడసెనో\! \[ఓ\] యనుఁ గ్రుంకన్...\* (\*Haravilāsam\* 2-312)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ ఏ (Double Praśna):\*\* \*...నాదు పల్కు వింటే? \[ఏ\] యను వేగమో యనఁగదే? \[ఏ\]...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 276)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ ఏ (Prārthanā \+ Praśna):\*\* \*...ఈ శుభదర్శనంబునీవే\! \[ఏ\] యను నన్నుఁ బాయఁజనునే? \[ఏ\]...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 276)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Bhīti):\*\* \*...రాముభార్యఁ జుండో\! \[ఓ\] జనులార యడ్డపడరో\! \[ఓ\] సురలార...\* (\*Appakavīyamu\* 3-243 / \*Bhāskara Rāmāyaṇamu\*, Yuddha 41)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Saṁśaya):\*\* \*...క్లిష్టంబె యౌనో\! \[ఓ\] మాటిచ్చిన మీరు రాఘవులు పోరో\! \[ఓ\]...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Ayōdhyā 325)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Saṁśaya):\*\* \*...ఎంతో యిది యెడదఁ బొడమునోకో యనుచున్... ఏదో\! \[ఓ\] యుడుకెత్తుఁగాని కనమో\! \[ఓ\] ప్రభు నిన్మరి వేంకటేశ్వరా...\* (\*Vēṅkaṭēśvara Śatakam\* 104)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.46 పరరూప యతి (Pararūpa Yati — Śakandhvādi Compound Dual Caesura)

&nbsp;

\* \*\*Sanskrit Morphophonemic Engine (\*Śakandhvādi Gaṇa\*):\*\* Governed by the Pāṇinian vārtika on 6-1-94 (\*Śakandhvādiṣu pararūpaṁ vācyam\*)\[cite: 13\]. When nominal bases belonging to the \*Śakandhvādi\* class compound, the standard rules of \*Savarṇadīrgha\* or \*Guṇa Sandhi\* are barred; the terminal syllable marked by the \*\*'టి'\*\* (\*ṭi\*) tag (the final vowel \+ any following consonant of word 1\) obligatorily absorbs into the following vowel of word 2 (\*pararūpamu\*)\[cite: 13\]:

  \* $\\text{శక} \+ \\text{అంధు} \= \\mathbf{శకంధు}$ (not \*\\\*శకాంధు\*)\[cite: 13\].

  \* $\\text{మనస్} \+ \\text{ఈషా} \= \\mathbf{మనీషా}$ ($\\text{అస్} \+ \\text{ఈ} \\rightarrow \\mathbf{ఈ}$)\[cite: 13\].

  \* $\\text{వేద} \+ \\text{అండ} \= \\mathbf{వేదండ}$ (not \*\\\*వేదాండ\*)\[cite: 13\].

  \* $\\text{సార} \+ \\text{అంగ} \= \\mathbf{సారంగ}$ (not \*\\\*సారాంగ\* in animal semantics)\[cite: 13\].

  \* $\\text{మృత} \+ \\text{అండ} \= \\mathbf{మార్తండ}$\[cite: 13\].

  \* $\\text{సీమన్} \+ \\text{అంత} \= \\mathbf{సీమంత}$ ($\\text{అన్} \+ \\text{అ} \\rightarrow \\mathbf{అ}$)\[cite: 13\].

  \* $\\text{మంజు} \+ \\text{ఈర} \= \\mathbf{మంజీర}$ ($\\text{ఉ} \+ \\text{ఈ} \\rightarrow \\mathbf{ఈ}$)\[cite: 13\].

  \* $\\text{కుల} \+ \\text{అటా} \= \\mathbf{కులట}$\[cite: 13\].

  \* $\\text{పతత్} \+ \\text{అంజలి} \= \\mathbf{పతంజలి}$ ($\\text{అత్} \+ \\text{అ} \\rightarrow \\mathbf{అ}$)\[cite: 13\].

  \* $\\text{హల} \+ \\text{ఈషా} \= \\mathbf{హలీషా}$\[cite: 13\].

  \* $\\text{ఉష్ణ} \+ \\text{ఈష} \= \\mathbf{ఉష్ణీష}$\[cite: 13\].

  \* $\\text{మస్త} \+ \\text{ఇష్క} \= \\mathbf{మస్తిష్క}$\[cite: 13\].

\* \*\*The Dual-Track Rule (పరరూప విరతి):\*\* At the syllable resulting from Pararūpa Sandhi, the poet holds full \*\*Ubhaya Yati\*\* licensing\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Match the substituted pararūpa vowel sound (\*\*అ, ఇ, ఈ\*\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant (\*\*ద, ర, న, త, మ, జ, ల, ష\*\*)\[cite: 13\].

&nbsp;

&nbsp;

             Pararūpa Yati Dual Engine Routing

           \[ Śakandhvādi Compound at Caesura Site \]

                              │

    ┌─────────────────────────┴─────────────────────────┐

    ▼                                                   ▼

&nbsp;

Track 1: Svara Mārga                                Track 2: Vyañjana Mārga (Matches the pararūpa vowel)                         (Matches the resulting surface consonant) • వేదండ ⟷ అ/ఆ/ఐ/ఔ                                    • వేదండ \[ద\] ⟷ త/థ/ద/ధ (Vargaja) • సారంగ ⟷ అ/ఆ/ఐ/ఔ                                    • సారంగ \[ర\] ⟷ ర (Ēkatara) • మనీష ⟷ ఇ/ఈ/ఎ/ఏ                                     • మనీష \[న\] ⟷ న/ణ (Sarasayati) • మంజీర ⟷ ఇ/ఈ/ఎ/ఏ                                    • మంజీర \[జ\] ⟷ చ/ఛ/జ/ఝ (Vargaja)

&nbsp;

\#\#\#\# Kūcimanchi Vēṅkaṭarāya's Sīsamālika Benchmark (\*Sukavi Manōrañjanamu\* 2-3-143) (6.46.8)

This classical pedagogical tour-de-force demonstrates both tracks back-to-back across 9 Pararūpa stems\[cite: 13\]:

1\. \*\*శకంధు:\*\* Track 1 matches \*\*అ $\\longleftrightarrow$ అ\*\* (\*అపుడు విప్రుండు శకంధు...\*); Track 2 matches \*\*క $\\longleftrightarrow$ క\*\* in \*క్షత్రియ వరుఁడు శకంధు...\*\[cite: 13\].

2\. \*\*మనీషా:\*\* Track 1 matches \*\*ఇ $\\longleftrightarrow$ ఈ\*\* (\*...మనీషి యొకండు...\*); Track 2 matches \*\*దిం $\\longleftrightarrow$ నీ\*\* (\*...క్రోధంబు మనీష చేత...\*)\[cite: 13\].

3\. \*\*హలీషా:\*\* Track 1 matches \*\*ఎ $\\longleftrightarrow$ ఈ\*\* (\*నెపుడు విప్రునకు హలీష...\*); Track 2 matches \*\*లీ $\\longleftrightarrow$ లి\*\* (\*...హలీషాపరులతోఁ జెలిమియుఁ...\*)\[cite: 13\].

4\. \*\*ఉష్ణీష:\*\* Track 1 matches \*\*ఎ $\\longleftrightarrow$ ఈ\*\* (\*...శిరమునుష్ణీషంబుఁ దాల్చె...\*); Track 2 matches \*\*షీ $\\longleftrightarrow$ జిం\*\* (\*...ఉష్ణీషాధిపతులు పూజించుచుండ...\*)\[cite: 13\].

5\. \*\*మస్తిష్క:\*\* Track 2 matches \*\*దె $\\longleftrightarrow$ తి\*\* (\*దెబ్బతో శిరము మస్తిష్కంబు...\*); Track 1 matches \*\*ఇ $\\longleftrightarrow$ ఇ\*\* (\*...ఇంతింతపైఁబడెను మస్తిష్కమెల్లఁ...\*)\[cite: 13\].

6\. \*\*మంజీర:\*\* Track 2 matches \*\*జె $\\longleftrightarrow$ జీ\*\* (\*జైలుల పాదముల మంజీరంబులలరె...\*); Track 1 matches \*\*ఈ $\\longleftrightarrow$ హె\*\* (\*...మంజీరా రవంబులు హెచ్చు మీఱె...\*)\[cite: 13\].

7\. \*\*కులటా:\*\* Track 1 matches \*\*ఆ $\\longleftrightarrow$ అ\*\* (\*నార్యజనములు కులటలనంటుదురె...\*); Track 2 matches \*\*ల $\\longleftrightarrow$ ల\*\* (\*...కులటలతోఁ జెల్మి ఖల జనులకగు...\*)\[cite: 13\].

8\. \*\*సీమంత:\*\* Track 2 matches \*\*మ $\\longleftrightarrow$ మ\*\* (\*మణిభూషలిడియె సీమంతంబుఁదీర్చి...\*); Track 1 matches \*\*అ $\\longleftrightarrow$ యా\*\* (\*...సీమంతిని యొకతె యొయ్యారమొదవ...\*)\[cite: 13\].

9\. \*\*పతంజలి:\*\* Track 1 matches \*\*అ $\\longleftrightarrow$ అ\*\* (\*నఖిల జనములు మ్రొక్కె పతంజలికిఁ...\*); Track 2 matches \*\*త $\\longleftrightarrow$ త\*\* (\*...పతంజలి యొనర్చె శబ్దశాస్త్రముకు భాష్య...\*)\[cite: 13\].

&nbsp;

\#\#\#\# Corpus Provenance Trail Across Common Pararūpa Stems (6.46.2 – 6.46.7)

\* \*\*వేదండ (Elephant):\*\*

  \* Track 1 (Vowel): \*\*అ $\\longleftrightarrow$ వేదండ \[అ\]:\*\* \*...వైరి వేదండ గండ విదారి ఘోరతరాసి...\* (\*Bhāratam\*, Ādi 3-228, Mattakōkila)\[cite: 13\]; \*...కీటఫణీంద్రపోతమదవేదండోగ్ర హింసావిచారిణి...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 13\].

  \* Track 2 (Consonant): \*\*తా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...వేదండ ముఖాంగముల్ దృణ వితానముగాఁ గొని...\* (\*Bhāratam\*, Udyōga 4-1-234)\[cite: 13\]; \*\*దా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...మత్తవేదండమునెక్కి చాటెదను దాశరథీ...\* (\*Dāśarathī Śatakam\*)\[cite: 13\]; \*\*ధా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...వేదండస్వామి మదంబు సేసెఁ గరిణీధామంబులజ్జాడఁగాన్...\* (\*Kāśīkhaṇḍam\* 1-86)\[cite: 13\].

\* \*\*సారంగ (Deer / Bee / Elephant):\*\*

  \* Track 1 (Vowel): \*\*అ $\\longleftrightarrow$ సారంగ \[అ\]:\*\* \*అలరెన్ జైత్రబలాధినేత మదసారంగాళి...\* (\*Bhāgavatam\* 4-39)\[cite: 13\]; \*\*హ $\\longleftrightarrow$ సారంగ \[అ\]:\*\* \*...భద్ర సారంగ వరేణ్యముల్ పయికి హస్తములించుక...\* (\*Appakavīyamu\* 3-129 / \*Candrikāpariṇayamu\*)\[cite: 13\].

  \* Track 2 (Consonant): \*\*రా $\\longleftrightarrow$ సారంగి \[ర\]:\*\* \*...సారంగియ పోలెనుండెఁ గురురాజ భవత్సుతుసేన...\* (\*Appakavīyamu\* 3-130 / \*Bhāratam\*, Drōṇa 1-17)\[cite: 13\]; \*\*ర $\\longleftrightarrow$ సారంగ \[ర\]:\*\* \*గ్రహణ కాలంబు సుమ్ము సారంగనయన...\* (\*Kāśīkhaṇḍam\* 2-131)\[cite: 13\]; \*...సారంగ మదంబు లేఁజెమటఁ గ్రమ్మె...\* (\*Manu Caritra\* 2-32)\[cite: 13\].

\* \*\*మనీష (Intellect):\*\*

  \* Track 1 (Vowel): \*\*ఎ $\\longleftrightarrow$ మనీష \[ఈ\]:\*\* \*...మనీషమెయింజాలు రామునెదిరి...\* (\*Nirvacanōttara Rāmāyaṇamu\* 1-76)\[cite: 13\]; \*...మెప్పుడు చేరెదమొ యను మనీష దలంకన్...\* (\*Niraṅkuśōpākhyānamu\* 4-68)\[cite: 13\].

  \* Track 2 (Consonant): \*\*నీ $\\longleftrightarrow$ మనీషి \[నీ\]:\*\* \*...మనీషిజనము సెప్పు మాననీయచరిత్రా...\* (\*Bhāratam\*, Āraṇya 5-3-401)\[cite: 13\]; \*\*నె $\\longleftrightarrow$ మనీషిత \[నీ\]:\*\* \*నెఱయఁగఁ బ్రోచు మన్ముఖమనీషిత కావ్యకళా...\* (\*Bhāratam\*, Ādi 1-4)\[cite: 13\]; \*\*ని $\\longleftrightarrow$ మనీష \[నీ\]:\*\* \*నిరసించు విరక్తియుతమనీష జనించెన్...\* (\*Bhāratam\*, Udyōga 4-653)\[cite: 13\].

\* \*\*మార్తండ (Sun):\*\*

  \* Track 2 (Consonant): \*\*త $\\longleftrightarrow$ మార్తండుండు \[త\]:\*\* \*...తర బాహాగ్రపు సంగడంబనఁగ మార్తండుండు దోఁచెన్ దివిన్...\* (\*Manu Caritra\* 3-59)\[cite: 13\].

\* \*\*సీమంత (Parting of Hair / Woman):\*\*

  \* Track 2 (Consonant): \*\*మ $\\longleftrightarrow$ సీమంతిని \[మ\]:\*\* \*...వృద్ధ సీమంతినిఁ గాశికానగర మధ్య నివాసిని...\* (\*Kāśīkhaṇḍam\* 2-111)\[cite: 13\].

\* \*\*మంజీర (Anklet):\*\*

  \* Track 2 (Consonant): \*\*శీ $\\longleftrightarrow$ మంజీర \[జీ\] (Sarasayati):\*\* \*శ్రీ భూపుత్రి వివాహవేళ నిజమంజీరాగ్ర...\* (\*Manu Caritra\* 1-1)\[cite: 13\]; \*\*జే $\\longleftrightarrow$ మంజీర \[జీ\] (Prāṇi):\*\* \*...మంజీర ఝళంఝళధ్వనికిఁ జేరుట గాదు...\* (\*Manu Caritra\* 2-182)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.47 ప్రాది యతులు (Prādi Yatulu — The 22 Sanskrit Prefixes Dual Caesura)

&nbsp;

\* \*\*Definition:\*\* Governs Sanskrit compound words formed by prefixing any of the \*\*22 Sanskrit Upasargas\*\* (\*prādayaḥ / prādulu\*: \*ప్ర, పరా, అప, సమ్, అను, అవ, నిస్, నిర్, దుస్, దుర్, వి, ఆజ్, ని, అధి, అపి, అతి, సు, ఉద్, అభి, ప్రతి, పరి, ఉప\*) to roots or nominal stems beginning with a vowel (\*\*అజాది ధాతువులు / అజాది శబ్దములు\*\*)\[cite: 13\].

\* \*\*The Structural Rule (ప్రాది యతి):\*\* At the compound syllable where the prefix fuses with the vowel stem via sandhi, \*\*Ubhaya Yati\*\* is licensed\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Match the underlying root-initial vowel (\*para-padādi svara\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant cluster under standard consonant rules\[cite: 13\].

\* \*\*Consonant-Initial Roots Barred (హలాది శబ్దములు 6.47):\*\* When an upasarga prefixes to a consonant-initial root (\*ప్ర \+ మాన \= ప్రమాణ\*; \*అభి \+ మాన \= అభిమాన\*; \*వి \+ శేష \= విశేష\*), no vowel sandhi occurs\[cite: 13\]. These stems have \*\*zero Ubhaya Yati access\*\*; they scan solely as standard consonant yatis on the surface consonant\[cite: 13\].

\* \*\*The 22 Upasargas Inventory & Practical Nuances (6.47.1):\*\*

  \* Appakavi lists 20 prefixes, bundling \*nis/nir\* into \*\*నిర్\*\* and \*dus/dur\* into \*\*దుర్\*\* because only the \*repha\* forms participate in vowel compounding\[cite: 13\].

  \* \*Exclusion of 'ఆజ్' (Āṅ):\* The prefix \*āṅ\* sheds \*ṅ\* to leave vowel \*\*'ఆ'\*\*\[cite: 13\]. Compounding with vowel stems yields purely vocalic sandhi (\*ఆ \+ ఉదక \= ఓదక\*), producing no surface consonant to establish a consonant track\[cite: 13\]. It functions strictly under \*Svara-Pradhāna Yati\*\[cite: 13\].

&nbsp;

&nbsp;

             Prādi Yati Dual Engine Routing

           \[ Prefix (Upasarga) \+ Vowel-Initial Root \]

                               │

    ┌──────────────────────────┴──────────────────────────┐

    ▼                                                     ▼

&nbsp;

Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga (Matches root-initial vowel)                          (Matches surface compound consonant) • ప్ర \+ ఆప్తి \= ప్రాప్తి ⟷ అ/ఆ/ఐ/ఔ                     • ప్రాప్తి \[ప\] ⟷ బ/భ/ప/ఫ (Vargaja) • సమ్ \+ ఈక్షా \= సమీక్ష ⟷ ఇ/ఈ/ఎ/ఏ                       • ప్రాప్తి \[ర\] ⟷ ర (Ēkatara via Repha) • అను \+ ఏషణ \= అన్వేషణ ⟷ ఇ/ఈ/ఎ/ఏ                        • సమీక్ష \[మ\] ⟷ మ (Prāṇi Yati)

&nbsp;

\#\#\#\# Appakavi's Complete Lakṣya-Lakṣaṇa Stanza (\*Appakavīyamu\* 3-133) (6.47.3)

Using the compound base \*\*'ప్రాప్తి'\*\* ($\\text{ప్ర} \+ \\text{ఆప్తి}$):

\* \*\*Line 1 (Track 1 — Svara Track):\*\* \*\*అ $\\longleftrightarrow$ ప్రాప్తి \[ఆ\]\*\* ($\\mathbf{అ \\longleftrightarrow ఆ}$ Svara Yati: \*అబ్జయోని రజోగుణప్రాప్తిఁదనరు...\*)\[cite: 13\].

\* \*\*Line 2 (Track 2 — Consonant Track via Stop):\*\* \*\*బ $\\longleftrightarrow$ ప్రాప్తి \[పా\]\*\* ($\\mathbf{బ \\longleftrightarrow ప}$ Vargaja Yati: \*బద్మనాభుఁడు సాత్వికప్రాప్తిఁదనరు...\*)\[cite: 13\].

\* \*\*Line 3 (Track 2 — Consonant Track via Liquid):\*\* \*\*ర $\\longleftrightarrow$ ప్రాప్తి \[రా\]\*\* ($\\mathbf{ర \\longleftrightarrow ర}$ Ēkatara Yati on conjunct repha: \*రజతగిరిమందిరుఁడు తమఃప్రాప్తిఁదనరు...\*)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (Part 11 Summary)

&nbsp;

| Rule Type | Primary Target Coordinates | Grammatical / Phonetic Engine Conditions | Status in Engine |

| :--- | :--- | :--- | :--- |

| \*\*'ఎఁడు' ప్రత్యయ యతి (6.42.2)\*\*\[cite: 13\] | Volumetric suffix \*\*-e'ḍu\*\*\[cite: 13\] | Compounding measurement affix\[cite: 13\]. Resolves on surface consonant\[cite: 13\]. Verbal infix \*-eḍu\* barred\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*'అవ' ప్రత్యయ యతి (6.42.3)\*\*\[cite: 13\] | Ordinal augment \*\*-ava\*\*\[cite: 13\] | \*\*Dual Track:\*\* Match vowel \*\*'అ'\*\* under Class 1 Svara Yati OR match surface consonant (\*\*డ, ల\*\*)\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*యుష్మదస్మదాది యతి (6.43)\*\*\[cite: 13\] | Pronouns ending in 'ద్': \*yuṣmad, asmad, bhavat, tad, yad, ētad\*\[cite: 13\] | \*\*Dual Track:\*\* Match underlying root-initial vowel OR match surface dental stop (\*\*ద, దా, దు\*\*)\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*కాకుస్వర యతి (6.44)\*\*\[cite: 13\] | Syllable bearing emotional protraction (\*pluta\*)\[cite: 13\] | \*\*Dual Track:\*\* Match protracted vowel (\*\*ఆ, ఈ, ఏ, ఓ\*\*) under Svara Yati OR match surface consonant under consonant rules\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*ప్లుతయుగ యతి (6.45)\*\*\[cite: 13\] | Both \*vali\* and \*yati-sthāna\* are pluta syllables\[cite: 13\] | Pure Svara Yati between pluta vowels; validates lines even if host consonants share zero affinity\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*పరరూప యతి (6.46)\*\*\[cite: 13\] | \*Śakandhvādi gaṇa\* compounds (\*వేదండ, సారంగ, మనీషా\*)\[cite: 13\] | \*\*Dual Track:\*\* Match absorbed pararūpa vowel OR match surface compound consonant\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*ప్రాది యతులు (6.47)\*\*\[cite: 13\] | 22 Upasargas \+ Vowel-initial roots (\*అజాది ధాతువులు\*)\[cite: 13\] | \*\*Dual Track:\*\* Match underlying root-initial vowel OR match surface compound consonant\[cite: 13\]. Consonant stems barred\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

### 6.42.2 'ఎఁడు' ప్రత్యయమునకు యతి (Mānārthaka '-e'ḍu' Quantitative Suffix Yati)

* **Grammatical Formation:** Governed by *Bāla Vyākaraṇam* (Taddhita 25: *"మానార్థంబునకేకత్వంబునందెఁడు వర్ణకంబగు"*), the suffix **'-ఎఁడు'** (*\-e'ḍu*) attaches to singular nouns to designate a volumetric measurement (e.g., *తూము \+ ఎఁడు \= తూమెఁడు*; *వీసె \+ ఎఁడు \= వీసెఁడు*; *గంప \+ ఎఁడు \= గంపెఁడు*).  
* **Elision of Base Stems:** By *Bāla Vyākaraṇam* (Taddhita 26), when '-ఎఁడు' attaches to stems ending in *'లి'*, the *'లి'* elides: *దోసిలి \+ ఎఁడు $\\rightarrow$ దోసెఁడు*; *పిడికిలి \+ ఎఁడు $\\rightarrow$ పిడికెఁడు*; *పుడిసిలి \+ ఎఁడు $\\rightarrow$ పుడిసెఁడు*.  
* **Caesura Licensing:** Like the distributive suffix *\-ēsi*, compounding with measurement suffix *\-e'ḍu* is grammatically eligible for dual-track Ubhaya Yati. In classical practice, poets almost universally match the **resulting surface consonant track**.  
* **Critical Engine Disambiguation:**  
* *Volumetric Suffix (-ఎఁడు):* Attaches to nouns to denote capacity (*దోసెఁడు, పుడిసెండు*). Eligible for Ubhaya Yati categorization.  
* *Verbal Suffix / Infix (-ఎడు / \-ఎడున్):* Occurs in finite verbs and habitual participles (*వండెడును, కలిగెడును, పలికెడు, ఉండెడు*). **Does not indicate measurement and has zero Ubhaya Yati license**; it must strictly scan as a standard consonant yati on the surface consonant (Section 6.77).  
* **Provenance (Consonant Track):**  
* **జె $\\longleftrightarrow$ సె \[పుడిసెండు\]:** *చీడపుర్వు దాఁజెడఁదినునింతెకాక పుడిసెండు జలంబిడి పెంపనేర్చునే...* ($\\text{జె} \\longleftrightarrow \\text{సె}$ via *Sarasayati-4*) (*Bhāskara Śatakam*).

---

### 6.42.3 'అవ' ప్రత్యయమునకు ఉభయ యతులు (Pūraṇārthaka '-ava' Ordinal Dual Caesura)

* **Grammatical Formation:** By *Bāla Vyākaraṇam* (Ācchika 25: *"సంఖ్యకుం బూరణార్థమునందవగాగమంబగు"*), the ordinal suffix augment **'-అవ'** (*\-avagāgamamu*) attaches to cardinal numbers to derive ordinal rankings (*రెండు \+ అవ \= రెండవ*; *మూఁడు \+ అవ \= మూఁడవ*; *నాలుగు \+ అవ \= నాలవ*; *పదుమూఁడు \+ అవ \= పదుమూఁడవ*; *ఎనిమిది \+ అవ \= ఎనిమిదవ*).  
* **The Dual-Track Rule:** Because the numerical base fuses obligatorily with *\-ava*, forming an integrated ordinal compound word, the caesura coordinate at this junction licenses **Ubhaya Yati**:  
* **Track 1 (Svara Track):** Disregard the host consonant and match the underlying junction vowel **'అ'** (*a*) of *\-ava* under *Class 1 Svara Yati* (**అ, ఆ, ఐ, ఔ**).  
* **Track 2 (Vyañjana Track):** Match the resulting surface consonant (**డవ, లవ**) under consonant *Prāṇi* or *Vargaja Yati*.

                 Ordinal '-ava' Dual Engine Routing

               \[ Cardinal Stem \+ Ordinal Augment: \-ava \]

                                   │

        ┌──────────────────────────┴──────────────────────────┐

        ▼                                                     ▼

   Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga

  (Matches vowel 'అ' of \-ava)                           (Matches surface compound consonant)

  • మూఁడవ ⟷ అ/ఆ/ఐ/ఔ                                    • రెండవ \[డ\] ⟷ ట/ఠ/డ/ఢ (Vargaja)

  • నాలవ ⟷ అ/ఆ/ఐ/ఔ                                      • నాలవ \[ల\] ⟷ ల/ళ (Abhēda)

  (Class 1 Svara Equivalence)                           (Consonant Class Preserved)

\`\`\`\[cite: 13\]

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.42.3)

\* \*\*Track 1: Vowel Matches on 'అ' (Svara Track):\*\*

  \* \*\*ఆ $\\longleftrightarrow$ నాలవ \[అ\]:\*\* \*సుకరంపుమార్గమాయువు మొదలి నాలవపాలు గురుపాల...\* ($\\text{మార్గము} \+ \\mathbf{ఆయువు} \\longleftrightarrow \\text{నాలుగు} \+ \\mathbf{అవ} \\implies \\mathbf{ఆ \\longleftrightarrow అ}$ Svara Yati) (\*Bhāratam\*, Śānti 5-136)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ మూఁడవ \[అ\]:\*\* \*...మూడవ సవనంబునన్ శ్రుతి సమభ్యధికంబుగఁ...\* ($\\text{మూఁడు} \+ \\mathbf{అవ} \\longleftrightarrow \\text{సమ్} \+ \\mathbf{అభ్యధిక} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati) (\*Bhāratam\*, Āraṇya 3-243)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ రెండవ \[అ\]:\*\* \*...రెండవ కాండంబుఁ దదస్త్రమున్ గొనక డాయన్వచ్చి...\* ($\\text{రెండు} \+ \\mathbf{అవ} \\longleftrightarrow \\mathbf{డాయన్వచ్చి} \\implies \\mathbf{అ \\longleftrightarrow య}$ via \*Sarasayati-2\*) (\*Bhāratam\*, Virāṭa 4-46)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ రెండవ \[అ\]:\*\* \*...రెండవ వినతా తనూభవుని యందమునం గమనీయ...\* ($\\text{రెండు} \+ \\mathbf{అవ} \\longleftrightarrow \\mathbf{య్ \+ అం} \\implies \\mathbf{అ \\longleftrightarrow అ}$ Svara Yati) (\*Pārijātāpaharaṇamu\* 2-85)\[cite: 13\].

\* \*\*Track 2: Consonant Matches on Surface Stems (Vyañjana Track):\*\*

  \* \*\*ల $\\longleftrightarrow$ నాలవ \[ల\]:\*\* \*...నాలవ వాఁడు నిశరుఁడుల్లఱపు బిరుదు...\* ($\\text{నాలుగు} \+ \\text{అవ} \= \\text{నాలవ} \\implies \\mathbf{ల \\longleftrightarrow ల్ల\\ \[ల\]}$ Prāṇi Yati) (\*Bhāgavatam\* 4-200)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ పదుమూఁడవ \[డ\]:\*\* \*...పదుమూఁడవయెడ విరతిఁబొసఁగిన బెడఁగడరుఁ గనకలతన్...\* ($\\text{పదుమూఁడు} \+ \\text{అవ} \\implies \\mathbf{డ \\longleftrightarrow డ}$ Prāṇi Yati) (\*Appakavīyamu\* 4-345, Kanakalatā Vṛtta)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ రెండవ \[డ\]:\*\* \*...రెండవ కక్ష్యాంతరమున్ రమాధిపుఁడు వేడ్కనొసఁగి...\* ($\\text{రెండు} \+ \\text{అవ} \\implies \\mathbf{డ \\longleftrightarrow డ్క\\ \[డ\]}$ Prāṇi Yati) (\*Uttara Rāmāyaṇamu\* 8-298)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.43 యుష్మదస్మదాది శబ్ద యతి (Yushmadasmadādi Śabda Yati — Pronominal Compound Dual Caesura)

&nbsp;

\* \*\*Morphological Environment:\*\* Governs Sanskrit pronominal bases ending in consonant \*\*'ద్'\*\* (\*d-kārānta prātipadikas\*), primarily \*\*యుష్మద్\*\* (\*yuṣmad\* \= second person / thou) and \*\*అస్మద్\*\* (\*asmad\* \= first person / I), compounding with an initial vowel (\*ajādi śabda\*):

  \* $\\text{యుష్మద్} \+ \\text{ఆగమన} \= \\mathbf{యుష్మదాగమన}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{ఉదర} \= \\mathbf{అస్మదుదర}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{అన్వయ} \= \\mathbf{అస్మదన్వయ}$\[cite: 13\]

  \* $\\text{యుష్మద్} \+ \\text{ఆజ్ఞా} \= \\mathbf{యుష్మదాజ్ఞా}$\[cite: 13\]

  \* $\\text{అస్మద్} \+ \\text{ఆది} \= \\mathbf{అస్మదాది}$\[cite: 13\]

\* \*\*The Structural Rule:\*\* At the resulting dental stop juncture (\*\*ద, దా, దు\*\*, etc.), the engine licenses \*\*Ubhaya Yati\*\*\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Disregard the dental stop and match the initial vowel of the second component (\*para-padādi svara\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant (\*\*ద\*\*) under \*Prāṇi\* or \*Vargaja Yati\* (\*\*త, థ, ద, ధ\*\*)\[cite: 13\].

&nbsp;

&nbsp;

             Pronominal Dual Engine Routing

      \[ Pronominal Base (యుష్మద్ / అస్మద్) \+ Vowel Stem \]

                               │

    ┌──────────────────────────┴──────────────────────────┐

    ▼                                                     ▼

&nbsp;

Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga (Matches vowel of second word)                        (Matches surface dental consonant 'ద') • యుష్మదాగమన ⟷ అ/ఆ/ఐ/ఔ                                • యుష్మదాజ్ఞా \[దా\] ⟷ త/థ/ద/ధ (Vargaja) • అస్మదుదర ⟷ ఉ/ఊ/ఒ/ఓ                                  • అస్మదాదులు \[దా\] ⟷ త/థ/ద/ధ (Vargaja) (Svara-Pradhāna Resolution)                           (Dental Stop Class Preserved)

&nbsp;

\* \*\*Class Extension (యుష్మదస్మదాది శబ్దములు 6.43.1):\*\*

  While Appakavi framed this rule around \*yuṣmad\* and \*asmad\*, classical usage extends identical dual-track licensing to all Sanskrit \*d-ending\* and \*t-ending\* pronominal bases: \*\*భవత్\*\* (\*bhavat\*), \*\*తద్\*\* (\*tad\*), \*\*యద్\*\* (\*yad\*), and \*\*ఏతద్\*\* (\*ētad\*)\[cite: 13\]:

  \* $\\text{భవత్} \+ \\text{అగ్రజ} \= \\mathbf{భవదగ్రజ}$\[cite: 13\]

  \* $\\text{భవత్} \+ \\text{అంఘ్రి} \= \\mathbf{భవదంఘ్రి}$\[cite: 13\]

  \* $\\text{భవత్} \+ \\text{ఆత్మ} \= \\mathbf{భవదాత్మ}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{అగ్ర} \= \\mathbf{తదగ్ర}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{ఆశ్రమ} \= \\mathbf{తదాశ్రమ}$\[cite: 13\]

  \* $\\text{తద్} \+ \\text{ఆరూఢ} \= \\mathbf{తదారూఢ}$\[cite: 13\]

&nbsp;

\#\#\#\# Philological Defense of Nannaya's Text (\*Mahābhārata\*, Ādi 2-216) (6.43)

\* \*The Stanza:\* \*ప్రస్తుత ఫణిసత్ర భయత్రస్తాత్ములమైన యస్మదాదులకెల్లన్...\* (\*\*త్ర \[త\] $\\longleftrightarrow$ అస్మదాదులు \[దా\]\*\*)\[cite: 13\].

\* \*The Scribal Corruption:\* Purists who rejected consonant matching on \*asmad\* altered Nannaya's line to \*...భయాయస్తాత్ములమైన...\*, claiming \*భయత్రస్త\* created a semantic tautology ("frightened by fear") and forcing a vowel match (\*\*య $\\longleftrightarrow$ ఆ\*\*)\[cite: 13\].

\* \*The Refutation:\* The root \*tras\* denotes torment or agitation (\*pīḍita / udvigna\*); \*భయత్రస్త\* authentically signifies "afflicted by fear," harmonizing with Nannaya’s closing verse in that section (\*జననీ శాప భయప్రపీడిత...\*)\[cite: 13\]. Nannaya's authentic reading confirms consonant-track matching (\*\*త $\\longleftrightarrow$ దా\*\* via \*Vargaja Yati\*)\[cite: 13\].

&nbsp;

\#\#\#\# Canonical Provenance Trail (6.43, 6.43.1)

\* \*\*Primary Yuṣmad / Asmad Stanzas:\*\*

  \* \*\*య $\\longleftrightarrow$ యుష్మదాగమన \[ఆ\] (Svara):\*\* \*...దివ్యతపోధనవర్య యుష్మదాగమనమునన్...\* (\*Sāmbōpākhyānamu\* / \*Appakavīyamu\* 3-123)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ అస్మదన్వయ \[అ\] (Svara):\*\* \*...నతిపావనమయ్యెనస్మదన్వయ మెల్లన్...\* (\*Sāmbōpākhyānamu\* / \*Appakavīyamu\* 3-123)\[cite: 13\].

  \* \*\*ధ $\\longleftrightarrow$ యుష్మదాజ్ఞా \[దా\] (Consonant):\*\* \*ధర్మతనయ యుష్మదాజ్ఞానిగళ వినిబద్ధమగుచు...\* (\*Adharvaṇa Virāṭaparva\* / \*Appakavīyamu\* 3-124)\[cite: 13\].

  \* \*\*త్ర \[త\] $\\longleftrightarrow$ అస్మదాదులు \[దా\] (Consonant):\*\* \*...భయత్రస్తాత్ములమైన యస్మదాదులకెల్లన్...\* (\*Bhāratam\*, Ādi 2-216)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ అస్మదుదర \[ఉ\] (Svara):\*\* \*...విశ్రమమొనరించితె యనఘ యస్మదుదరములోనన్...\* (\*Bhāratam\*, Udyōga 4-259)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ అస్మదాశ్రమ \[ఆ\] (Svara):\*\* \*...పువ్వుబోఁడియనినఁ గలిగెనస్మదాశ్రమంబుననని...\* (\*Bhāratam\*, Sabhā 2-209)\[cite: 13\].

  \* \*\*యుష్మదనుజు \[అ\] $\\longleftrightarrow$ య (Svara):\*\* \*యుష్మదనుజుఁ జంపిన వారలీ యక్షవరులు...\* (\*Bhāratam\*, Virāṭa 4-366)\[cite: 13\].

\* \*\*Bhavat / Tad Pronominal Extension Corpus (6.43.1):\*\*

  \* \*\*అ $\\longleftrightarrow$ భవదగ్రజ \[అ\] (Svara):\*\* \*...యిట్లను హరినాశ్రయించి భవదగ్రజుఁ బుణ్యునజాతశత్రునిన్...\* (\*Bhāratam\*, Udyōga 3-349)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ భవదంఘ్రుల \[ద\] (Consonant):\*\* \*...దావక సేవకుండ భవదంఘ్రుల నేనిటఁగొల్చి వచ్చెదన్...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 143)\[cite: 13\].

  \* \*\*ద $\\longleftrightarrow$ భవదాత్మ \[దా\] (Consonant):\*\* \*...దనరనందుపశాఖలై భవదాత్మ దీనికి మూలమై...\* (\*Bhāgavatam\* 3-305)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ తదగ్ర \[అ\] (Svara):\*\* \*ఆతని సమ్ముఖంబునఁ దదగ్రతనూజు కడన్...\* (\*Bhāratam\*, Virāṭa 4-1-39)\[cite: 13\].

  \* \*\*తం \[త\] $\\longleftrightarrow$ తదాశ్రమ \[దా\] (Consonant):\*\* \*...మాతంగమునెక్కి యింద్రుఁడు తదాశ్రమవీథిని వచ్చుచోఁ...\* (\*Ahalya\* 2-119)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ తదారూఢ \[దా\] (Consonant):\*\* \*...భావమునఁ దదారూఢప్రీతి మొగము దగఁ గైసేయన్...\* (\*Rāghavapāṇḍavīyamu\* 3-138)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.44 కాకుస్వర యతి / ప్లుతయతి (Kākusvara Yati / Pluta Yati — Emotional Protraction Dual Caesura)

&nbsp;

\* \*\*Phonological Definition of Kāku & Pluta:\*\*

  \* \*కాకువు (Kāku):\* Modulation or inflection of the voice triggered by intense emotional states (grief, fear, doubt, interrogation, entreaty, anger)\[cite: 13\].

  \* \*ప్లుతము (Pluta):\* The protracted lengthening of a vowel beyond standard long-vowel duration ($1 \\text{ mātrā} \= \\text{hrasva/laghu}$; $2 \\text{ mātrās} \= \\text{dīrgha/guru}$; $3 \\text{ mātrās} \= \\text{pluta/guru}$)\[cite: 13\].

  \* \*Prosodic Weight:\* While a pluta vowel occupies 3 mātrās phonetically, metrical scansion treats it simply as heavy (\*\*Guru / U\*\*)\[cite: 13\].

\* \*\*The Dual-Track Rule (కాకుస్వర యతి):\*\*

  At a syllable marked by emotional protraction (\*kākusvara / pluta\*)\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Disregard the host consonant and match the prolonged vowel sound (\*\*'ఆ', 'ఈ', 'ఏ', 'ఓ'\*\*) under \*Svara Yati\*\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Disregard the vocalic protraction and match the host consonant under standard consonant \*Prāṇi, Vargaja, Ūṣma\*, or \*Sarasayati\*\[cite: 13\].

&nbsp;

&nbsp;

             Kākusvara Dual Engine Routing

           \[ Syllable Modified by Emotional Kāku/Pluta \]

                                │

    ┌───────────────────────────┴───────────────────────────┐

    ▼                                                       ▼

&nbsp;

Track 1: Svara Mārga                                    Track 2: Vyañjana Mārga (Matches the protracted vowel:                          (Matches the surface host consonant: ఆ, ఈ, ఏ, ఓ)                                            ప, త, ద, ర, etc.) │                                                       │ e.g., నాథా\! ⟷ అ/ఆ/ఐ/ఔ                                   e.g., నాథా\! \[థా\] ⟷ త/థ/ద/ధ e.g., రావే\! ⟷ ఇ/ఈ/ఎ/ఏ                                   e.g., రావే\! \[వే\] ⟷ వ/బ/ప/ఫ/భ

&nbsp;

\#\#\#\# The 10 Functional Categories of Pluta (6.44.1)

&nbsp;

| \# | Semantic Category | Typical Markers | Contextual Illustration |

| :-: | :--- | :--- | :--- |

| 1 | \*\*శోకప్లుతము (Grief / Lamentation)\*\*\[cite: 13\] | అకటా\!, అయ్యో\!, హా\!, రావే\!\[cite: 13\] | Crying out in bereavement or intense sorrow\[cite: 13\]. |

| 2 | \*\*తర్కప్లుతము (Deliberation / Logic)\*\*\[cite: 13\] | కాదా\!, లేదా\!, ఏలా\!, పోరో\!\[cite: 13\] | Weighing arguments, moral reasoning, deduction\[cite: 13\]. |

| 3 | \*\*సంబోధనప్లుతము (Vocative / Address)\*\*\[cite: 13\] | తండ్రీ\!, నాథా\!, రాజా\!, వత్సా\!\[cite: 13\] | Direct vocative address with lengthened vowel\[cite: 13\]. |

| 4 | \*\*దూరాహ్వానప్లుతము (Calling from Afar)\*\*\[cite: 13\] | వీరులారా\!, రావే\!, రారమ్మో\!\[cite: 13\] | Projecting voice across distance to call someone\[cite: 13\]. |

| 5 | \*\*సంశయప్లుతము (Doubt / Uncertainty)\*\*\[cite: 13\] | కదా\!, కలదే\!, ఏమో\!, ఎట్లో\!\[cite: 13\] | Hesitation, skepticism, uncertain contemplation\[cite: 13\]. |

| 6 | \*\*ప్రశ్నప్లుతము (Interrogation)\*\*\[cite: 13\] | వింటే?, ఆతఁడా?, రావలదే?\[cite: 13\] | Direct questioning seeking verification\[cite: 13\]. |

| 7 | \*\*ఆశ్చర్యప్లుతము (Wonder / Exclamation)\*\*\[cite: 13\] | అకటా\!, బలే\!, నెగసిరో\!\[cite: 13\] | Astonishment, surprise, sudden realization\[cite: 13\]. |

| 8 | \*\*ప్రార్థనప్లుతము (Supplication / Entreaty)\*\*\[cite: 13\] | ప్రోవవే\!, తెల్పఁగదవే\!, ఈవే\!\[cite: 13\] | Pleading, urgent requests for grace or aid\[cite: 13\]. |

| 9 | \*\*భీతిప్లుతము (Fear / Terror)\*\*\[cite: 13\] | చుండో\!, మూఁడెనో\!, రారక్కసో\!\[cite: 13\] | Shivering alarm or impending catastrophe\[cite: 13\]. |

| 10 | \*\*గానప్లుతము / స్తుతి (Musical Chanting)\*\*\[cite: 13\] | గంగా\!, హరీ\!, ప్రభూ\!\[cite: 13\] | Musical elongation in poetic praise\[cite: 13\]. |

&nbsp;

\#\#\#\# Treatise Formulations & Provenance Trail (6.44.2 – 6.44.4)

\* \*\*Appakavi's Dual Benchmark Demonstrations (3-250, 3-252):\*\*

  \* \*Appakavīyamu (3-250 — Dūrāhvāna):\*

    \* Line 1 (Svara Track): \*\*ఆ $\\longleftrightarrow$ పద్మా\! \[ఆ\]\*\*\[cite: 13\].

    \* Line 2 (Consonant Track): \*\*ద్వా \[దా\] $\\longleftrightarrow$ సద్మా\! \[దా\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

    \* Line 3 (Svara Track): \*\*అ $\\longleftrightarrow$ వీరులారా\! \[ఆ\]\*\*\[cite: 13\].

    \* Line 4 (Consonant Track): \*\*ర $\\longleftrightarrow$ వాసులారా\! \[రా\]\*\* (\*Ēkatara Yati\*)\[cite: 13\].

  \* \*Appakavīyamu (3-252 — Saṁśaya/Praśna):\*

    \* Line 1 (Svara Track): \*\*హ $\\longleftrightarrow$ ఆతఁడా? \[ఆ\]\*\* (\*Sarasayati\*)\[cite: 13\].

    \* Line 2 (Consonant Track): \*\*డం $\\longleftrightarrow$ ఈతఁడా? \[డా\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

    \* Line 3 (Svara Track): \*\*ఎ $\\longleftrightarrow$ అబ్బెనే\! \[ఏ\]\*\* (\*Svara Yati\*)\[cite: 13\].

    \* Line 4 (Consonant Track): \*\*నె $\\longleftrightarrow$ గలుఁగునే? \[నే\]\*\* (\*Prāṇi Yati\*)\[cite: 13\].

\* \*\*Track 1 Corpus (Vowel Track Matches 6.44.3):\*\*

  \* \*\*అ $\\longleftrightarrow$ అకటా\! \[ఆ\] (Śōka):\*\* \*యడవులలోన సీత యకటా\! యిఁకఁజూడక...\* (\*Bhāskara Rāmāyaṇamu\*, Araṇya 72)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ రావే\! \[ఏ\] (Śōka):\*\* \*హా యనునో నరేంద్ర యను హా\! రఘుకుంజర నీవు వేగ రావే\! యనునెంత...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 112)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ వింటే? \[ఏ\] (Śōka/Praśna):\*\* \*...నాయెలుంగు వింటే? యను విన్న...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 112)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ మొఱ్ఱా\! \[ఓ\] (Śōka):\*\* \*ఒక్క దనుజాధముండు మొఱ్ఱా\! యనంగ...\* (\*Bhāskara Rāmāyaṇamu\*, Sundara 177)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ గాదా\! \[ఆ\] (Tarka):\*\* \*...కంటింపన్మఱి రాదె పూజనము గాదా\! ప్రాణిమేల్చక్రికిన్...\* (\*Bhāgavatam\* 6-58)\[cite: 13\].

  \* \*\*ఔ $\\longleftrightarrow$ లేదా\! \[ఆ\] (Tarka):\*\* \*...వాఁడౌనేనౌనొక జాడఁ బోయెదము లేదా\! జీవమింకేటికిన్...\* (\*Haravilāsam\* 2-123)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ దోఁచునే\! \[ఏ\] (Tarka):\*\* \*...మనమునకున్ ఈ విజ్ఞానంబు దోఁచునే\! వెఱపేలా...\* (\*Bhāratam\*, Anuśāsanika 2-192)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ పోరో\! \[ఓ\] (Tarka):\*\* \*...కోహెూ చాలుఁబొ కాలిపోయెదరొ పోరో\! నోటిక్రొవ్వేటికిన్...\* (\*Manu Caritra\* 6-45)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ సిరాలా\! \[ఆ\] (Saṁbōdhana):\*\* \*...నందన సిరాలా\! వీరశైవవ్రతా...\* (\*Haravilāsam\* 2-117)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ వనితా\! \[ఆ\] (Saṁbōdhana):\*\* \*అన మునిరాజు పల్కు వనితా\! జనతావినుతాభిధేయుఁడై...\* (\*Manu Caritra\* 2-91)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ వత్సా\! \[ఆ\] (Saṁbōdhana):\*\* \*...వత్సా\! విను మావంటి తైర్థికావళికెల్లన్...\* (\*Manu Caritra\* 1-65)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ మహాత్మా\! \[ఆ\] (Saṁbōdhana):\*\* \*...వింతలు మహాత్మా\! నాకెఱింగింపవే...\* (\*Manu Caritra\* 1-68)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ రాజా\! \[ఆ\] (Saṁbōdhana):\*\* \*హతశేషుండు నిజాకృతిన్ నిలిచి రాజా\! నిర్నిమిత్తంబునా...\* (\*Amuktamālyada\* 7-88)\[cite: 13\].

  \* \*\*ఇ $\\longleftrightarrow$ మూర్తీ\! \[ఈ\] (Saṁbōdhana):\*\* \*యిలపైనొక్కెడఁ గల్గెనేననఘమూర్తీ\! తెల్పవే...\* (\*Haravilāsam\* 1-96)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ స్వామీ\! \[ఈ\] (Saṁbōdhana):\*\* \*...స్వామీ\! పద్మాసన యార్తులన్ మముఁగృపాదృష్టిన్...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 174)\[cite: 13\].

  \* \*\*ఋ \[పృ\] $\\longleftrightarrow$ స్వామీ\! \[ఈ\] (Saṁbōdhana):\*\* \*పృతనాసాహుఁడు వేయి యేఁడులుగ స్వామీ\! నన్నుఁ...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Bāla 538)\[cite: 13\].

  \* \*\*యి $\\longleftrightarrow$ తండ్రీ\! \[ఈ\] (Saṁbōdhana):\*\* \*...ఎందరిగెఁదండ్రీ\! బుద్ధినూహింపుమా...\* (\*Bhāskara Rāmāyaṇamu\*, Kiṣkindha 121)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ రావే\! \[ఏ\] (Dūrāhvāna):\*\* \*ప్రోవ రావే\! వసుభూపయంచునెలుఁగెత్తి...\* (\*Haravilāsam\* 2-141)\[cite: 13\].

  \* \*\*ఆ $\\longleftrightarrow$ గదా\! \[ఆ\] (Saṁśaya):\*\* \*...చూతముగదా\! యని యంపిననాక్షణంబునన్...\* (\*Manu Caritra\* 2-78)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ కదా\! \[ఆ\] (Saṁśaya):\*\* \*హరిహయుఁడేమియయ్యెనొ కదా\! మదనానల...\* (\*Kāśīkhaṇḍam\* 4-65)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ గలదే\! \[ఏ\] (Saṁśaya):\*\* \*ఈ కొఱదీఱు తీరుగలదే\! బలశాలులు...\* (\*Kavitrayam\* 8-17)\[cite: 13\].

  \* \*\*ఉ $\\longleftrightarrow$ చేయుటకునో\! \[ఓ\] (Saṁśaya):\*\* \*...నన్నుత్తలమందఁ జేయుటకునో\! తలపోసి...\* (\*Bhāratam\*, Virāṭa 2-84)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ నగనేలా? \[ఆ\] (Praśna):\*\* \*అని చెప్పన్ విని సిద్ధుఁజూచి నగనేలా? యింత భవ్యాత్మ...\* (\*Appakavīyamu\* 3-53)\[cite: 13\].

  \* \*\*ఇ $\\longleftrightarrow$ రావలదే? \[ఏ\] (Praśna):\*\* \*...సారమేయమిదియట రావలదే? నా మనంబు...\* (\*Bhāratam\*, Mahāprasthānika 52)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ కనుగొంటే? \[ఏ\] (Praśna):\*\* \*ఏణీశాబవిలోలనేత్ర కనుగొంటే? వీరు విద్యాధరుల్...\* (\*Manu Caritra\* 2-91)\[cite: 13\].

  \* \*\*హ $\\longleftrightarrow$ అకటా\! \[ఆ\] (Āścarya):\*\* \*గేహనివహసాత్కరించి యకటా\! కడు రిక్తతనొందునే...\* (\*Amuktamālyada\* 4-32)\[cite: 13\].

  \* \*\*ఒ $\\longleftrightarrow$ నెగసిరో\! \[ఓ\] (Āścarya):\*\* \*...జలకేళి సల్పఁగానొలసి రయంబునన్నెగసిరో\! యని చూపఱు...\* (\*Bhāgavatam\* 9-83)\[cite: 13\].

  \* \*\*అ $\\longleftrightarrow$ మానవుగదా\! \[ఆ\] (Prārthanā):\*\* \*...నేననియెదనల్కమానవుగదా\! యిఁకనైన...\* (\*Śivarātri Māhātmyamu\* 1-123)\[cite: 13\].

  \* \*\*ఈ $\\longleftrightarrow$ రావే\! \[ఏ\] (Prārthanā):\*\* \*...ఈ యపమృత్యువుంగడపరావే\! యంచుఁగీర్తింపఁగన్...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 154)\[cite: 13\].

  \* \*\*హీ $\\longleftrightarrow$ బ్రోవవే\! \[ఏ\] (Prārthanā):\*\* \*హీనస్వరమెసఁగఁ బ్రోవవే\! నన్ననుచున్...\* (\*Haravilāsam\* 6-34)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ చేటు మూఁడెనో\! \[ఓ\] (Bhīti):\*\* \*...చేటు మూఁడెనో\! పురిలోనొక్క యుమ్మడినింటింట...\* (\*Bhāratam\*, Drōṇa 3-24)\[cite: 13\].

  \* \*\*ఆ \[గంగా\!\] $\\longleftrightarrow$ య (Gāna/Stuti):\*\* \*...మరందాయిత గంగా\! కాకోదరనగోదయస్థ...\* (\*Kāśīkhaṇḍam\* 6-1)\[cite: 13\].

\* \*\*Track 2 Corpus (Consonant Track Matches 6.44.4):\*\*

  \* \*\*టా \[అకటకటా\!\] $\\longleftrightarrow$ ఢ (Vargaja):\*\* \*చిత్తునకటకటా\! యని పోనిండు నను దృఢవ్రత...\* (\*Bhāratam\*, Śānti 1-203)\[cite: 13\].

  \* \*\*దా $\\longleftrightarrow$ కదా\! \[దా\] (Prāṇi):\*\* \*...రమావలేపముగదా\! యని యోర్తు...\* (\*Manu Caritra\* 3-161)\[cite: 13\].

  \* \*\*మా $\\longleftrightarrow$ మ \[మహిమా\!\]:\*\* \*...విమలతపోమహిమా\! యిన్ని దినంబులేల మసలితి...\* (\*Bhāratam\*, Ādi 1-116)\[cite: 13\].

  \* \*\*మా \[రమ్మా\!\] $\\longleftrightarrow$ మ:\*\* \*...రమ్మా\! చూతముగాని నీ గమన వేగంబున్...\* (\*Bhāratam\*, Virāṭa 2-89)\[cite: 13\].

  \* \*\*రా\! $\\longleftrightarrow$ రా:\*\* \*...జయ నామకంబనను రాజితభంగి...\* (\*Bhāratam\*, Svargārohaṇa 89)\[cite: 13\].

  \* \*\*వి $\\longleftrightarrow$ రావే\! \[వే\] (Prāṇi):\*\* \*వినఁగావచ్చెఁ బ్రియంవదా మగుడి రావే\! యంచు...\* (\*Bhāskara Rāmāyaṇamu\*, Bāla 51)\[cite: 13\].

  \* \*\*కు $\\longleftrightarrow$ అగునొకో\! \[కో\] (Prāṇi):\*\* \*కుసుమ సముద్గమంబగునొకో\! పతిలాభము...\* (\*Bhāratam\*, Ādi 3-170)\[cite: 13\].

  \* \*\*మో $\\longleftrightarrow$ ఏమో\! \[మో\] (Prāṇi):\*\* \*మోదింపం గలలోఁ గుమారుఁడొకఁడేమో\! చేసినం...\* (\*Bhāgavatam\* 5-84)\[cite: 13\].

  \* \*\*ధీ $\\longleftrightarrow$ మఱచితే? \[తే\] (Vargaja):\*\* \*ధీయుత అని పలికె మఱచితే? మునినాథా...\* (\*Bhāratam\*, Ādi 8-317)\[cite: 13\].

  \* \*\*ద $\\longleftrightarrow$ మఱచితా? \[తా\] (Vargaja):\*\* \*దనుతల దుంపవే మఱచితా? యిసిరో...\* (\*Bhāratam\*, Mauṣala 44)\[cite: 13\].

  \* \*\*ల $\\longleftrightarrow$ ఏలా? \[లా\] (Prāṇi):\*\* \*లలనా విష్ణుఁడనంగనెవ్వఁడతఁడేలా? శుద్ధ...\* (\*Manu Caritra\* 5-10)\[cite: 13\].

  \* \*\*ని $\\longleftrightarrow$ వింటే? \[ంటే\] (Anunāsikākṣara):\*\* \*నినుఁబోలంగలరబ్జగంధులన వింటే? యెందు...\* (\*Amuktamālyada\* 2-25)\[cite: 13\].

  \* \*\*తీ $\\longleftrightarrow$ ఏదీ? \[దీ\] (Vargaja):\*\* \*...నతీరుండూరక తప్పువట్టెనట యేదీ? లక్షణంబో...\* (\*Appakavīyamu\* 3-167)\[cite: 13\].

  \* \*\*డ $\\longleftrightarrow$ అకటా\! \[టా\] (Vargaja):\*\* \*డక్కెను రాజ్యమంచునకటా\! యిటు దమ్ముని...\* (\*Bhāratam\*, Virāṭa 2-52)\[cite: 13\]; \*...డక్క గొనంగ రాదె యకటా\! నను వీఁడు...\* (\*Haravilāsam\* 2-35)\[cite: 13\].

  \* \*\*లి $\\longleftrightarrow$ బలే\! \[లే\] (Prāṇi):\*\* \*...వాలి రాలి దరికొన్నను దేలిన దెస వ్రాలకుండిన బలే\! మముబోఁటులకుం...\* (\*Bhāratam\*, Virāṭa 2-97)\[cite: 13\].

  \* \*\*ర \[ప్ర\] $\\longleftrightarrow$ ఔరా\! \[రా\] (Ēkatara):\*\* \*ప్రభువేదాద్రి లిఖించు వ్రాయసములౌరా\! పెద్ద...\* (\*Haravilāsam\* 1-81)\[cite: 13\].

  \* \*\*వె $\\longleftrightarrow$ తెల్పఁగదవే\! \[వే\] (Prāṇi):\*\* \*వెలఁది మనంబు తెల్పఁగదవే\! మణిహారమ...\* (\*Manu Caritra\* 4-103)\[cite: 13\].

  \* \*\*వే $\\longleftrightarrow$ ఆనతీవే\! \[వే\] (Prāṇi):\*\* \*...పుట్టువు దీఱెడుదాఁకనానతీవే\! యని విన్నవింప...\* (\*Appakavīyamu\* 4-141)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.45 ప్లుతయుగ యతి (Plutayuga Yati — Symmetrical Double-Pluta Caesura)

&nbsp;

\* \*\*Definition & Structural Principle:\*\* Governs lines where \*\*BOTH coordinates (the line onset and the internal caesura) are emotionally protracted pluta syllables\*\*\[cite: 13\]:

  $$\\text{Line Onset Bearer: } \[\\text{C}\_1 \+ \\mathbf{\\text{Pluta}\_1}\] \\quad\\longleftrightarrow\\quad \\text{Caesura Coordinate: } \[\\text{C}\_2 \+ \\mathbf{\\text{Pluta}\_2}\]$$\[cite: 13\]

\* \*\*The Phonetic License:\*\* Even if Consonant $\\text{C}\_1$ and Consonant $\\text{C}\_2$ have \*\*ZERO consonantal affinity\*\* (e.g., labial \*\*'వ'\*\* and dental \*\*'ద'\*\*), the caesura is metrically valid if their prolonged pluta vowels share mutual Svaramaitri equivalence\[cite: 13\]\!

\* \*\*Nomenclature:\*\* Designated \*\*ప్లుతయుగ విశ్రామము\*\* (\*Plutayuga Viśrāmamu\* \= Twin-Pluta Caesura) by Appakavi\[cite: 13\].

\* \*\*Systemic Verification Prerequisites (6.45):\*\*

  1\. \*Dual Verification:\* Both syllables must carry genuine, contextually attested emotional kākusvaras\[cite: 13\]. If one syllable is an ordinary long vowel (e.g., \*వేగము కావవే...\*), the rule fails\[cite: 13\].

  2\. \*Vowel Class Parity:\* The pluta vowels must belong to the exact same Svaramaitri class\[cite: 13\]. Pairing a Class 2 pluta (\*\*'ఏ'\*\*) with a Class 1 pluta (\*\*'ఆ'\*\*) is an invalid metrical break\[cite: 13\].

  3\. \*Consonant Non-Affinity Domain:\* If $\\text{C}\_1$ and $\\text{C}\_2$ already share natural consonantal affinity (e.g., \*\*థా\! $\\longleftrightarrow$ దా\!\*\*), the line resolves simply under \*Vargaja Yati\*, rendering Plutayuga invocation unnecessary\[cite: 13\].

\* \*\*Independence from Semantic Equivalence:\*\* The two plutas need not express identical emotions; a line may validly pair an entreaty pluta (\*prārthanā\*) with an interrogative pluta (\*praśna\*)\[cite: 13\].

&nbsp;

\#\#\#\# Classical Attestations & Provenance Trail (6.45, 6.45.1)

\* \*\*Appakavi's Definitive Stanza (\*Vajrapañjara Śatakam\* / \*Appakavīyamu\* 3-257):\*\*

  \* \*నీవే\! గతి కావవే రఘుపతీ\! శరణాగత వజ్రపంజరా\* (\*\*నీవే\! \[ఏ\] $\\longleftrightarrow$ రఘుపతీ\! \[ఈ\]\*\*; Class 2 Vowel Class match between non-homorganic consonants \*\*వ\*\* and \*\*ప\*\*)\[cite: 13\].

\* \*\*Corpus Proof Across Pluta Classes:\*\*

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Praśna):\*\* \*మాయరవి యేల క్రుంకఁడొకో\! \[ఓ\] యనునిట్టేల తడసెనో\! \[ఓ\] యనుఁ గ్రుంకన్...\* (\*Haravilāsam\* 2-312)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ ఏ (Double Praśna):\*\* \*...నాదు పల్కు వింటే? \[ఏ\] యను వేగమో యనఁగదే? \[ఏ\]...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 276)\[cite: 13\].

  \* \*\*ఏ $\\longleftrightarrow$ ఏ (Prārthanā \+ Praśna):\*\* \*...ఈ శుభదర్శనంబునీవే\! \[ఏ\] యను నన్నుఁ బాయఁజనునే? \[ఏ\]...\* (\*Bhāskara Rāmāyaṇamu\*, Ayōdhyā 276)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Bhīti):\*\* \*...రాముభార్యఁ జుండో\! \[ఓ\] జనులార యడ్డపడరో\! \[ఓ\] సురలార...\* (\*Appakavīyamu\* 3-243 / \*Bhāskara Rāmāyaṇamu\*, Yuddha 41)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Saṁśaya):\*\* \*...క్లిష్టంబె యౌనో\! \[ఓ\] మాటిచ్చిన మీరు రాఘవులు పోరో\! \[ఓ\]...\* (\*Rāmāyaṇa Kalpavṛkṣamu\*, Ayōdhyā 325)\[cite: 13\].

  \* \*\*ఓ $\\longleftrightarrow$ ఓ (Double Saṁśaya):\*\* \*...ఎంతో యిది యెడదఁ బొడమునోకో యనుచున్... ఏదో\! \[ఓ\] యుడుకెత్తుఁగాని కనమో\! \[ఓ\] ప్రభు నిన్మరి వేంకటేశ్వరా...\* (\*Vēṅkaṭēśvara Śatakam\* 104)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.46 పరరూప యతి (Pararūpa Yati — Śakandhvādi Compound Dual Caesura)

&nbsp;

\* \*\*Sanskrit Morphophonemic Engine (\*Śakandhvādi Gaṇa\*):\*\* Governed by the Pāṇinian vārtika on 6-1-94 (\*Śakandhvādiṣu pararūpaṁ vācyam\*)\[cite: 13\]. When nominal bases belonging to the \*Śakandhvādi\* class compound, the standard rules of \*Savarṇadīrgha\* or \*Guṇa Sandhi\* are barred; the terminal syllable marked by the \*\*'టి'\*\* (\*ṭi\*) tag (the final vowel \+ any following consonant of word 1\) obligatorily absorbs into the following vowel of word 2 (\*pararūpamu\*)\[cite: 13\]:

  \* $\\text{శక} \+ \\text{అంధు} \= \\mathbf{శకంధు}$ (not \*\\\*శకాంధు\*)\[cite: 13\].

  \* $\\text{మనస్} \+ \\text{ఈషా} \= \\mathbf{మనీషా}$ ($\\text{అస్} \+ \\text{ఈ} \\rightarrow \\mathbf{ఈ}$)\[cite: 13\].

  \* $\\text{వేద} \+ \\text{అండ} \= \\mathbf{వేదండ}$ (not \*\\\*వేదాండ\*)\[cite: 13\].

  \* $\\text{సార} \+ \\text{అంగ} \= \\mathbf{సారంగ}$ (not \*\\\*సారాంగ\* in animal semantics)\[cite: 13\].

  \* $\\text{మృత} \+ \\text{అండ} \= \\mathbf{మార్తండ}$\[cite: 13\].

  \* $\\text{సీమన్} \+ \\text{అంత} \= \\mathbf{సీమంత}$ ($\\text{అన్} \+ \\text{అ} \\rightarrow \\mathbf{అ}$)\[cite: 13\].

  \* $\\text{మంజు} \+ \\text{ఈర} \= \\mathbf{మంజీర}$ ($\\text{ఉ} \+ \\text{ఈ} \\rightarrow \\mathbf{ఈ}$)\[cite: 13\].

  \* $\\text{కుల} \+ \\text{అటా} \= \\mathbf{కులట}$\[cite: 13\].

  \* $\\text{పతత్} \+ \\text{అంజలి} \= \\mathbf{పతంజలి}$ ($\\text{అత్} \+ \\text{అ} \\rightarrow \\mathbf{అ}$)\[cite: 13\].

  \* $\\text{హల} \+ \\text{ఈషా} \= \\mathbf{హలీషా}$\[cite: 13\].

  \* $\\text{ఉష్ణ} \+ \\text{ఈష} \= \\mathbf{ఉష్ణీష}$\[cite: 13\].

  \* $\\text{మస్త} \+ \\text{ఇష్క} \= \\mathbf{మస్తిష్క}$\[cite: 13\].

\* \*\*The Dual-Track Rule (పరరూప విరతి):\*\* At the syllable resulting from Pararūpa Sandhi, the poet holds full \*\*Ubhaya Yati\*\* licensing\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Match the substituted pararūpa vowel sound (\*\*అ, ఇ, ఈ\*\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant (\*\*ద, ర, న, త, మ, జ, ల, ష\*\*)\[cite: 13\].

&nbsp;

&nbsp;

             Pararūpa Yati Dual Engine Routing

           \[ Śakandhvādi Compound at Caesura Site \]

                              │

    ┌─────────────────────────┴─────────────────────────┐

    ▼                                                   ▼

&nbsp;

Track 1: Svara Mārga                                Track 2: Vyañjana Mārga (Matches the pararūpa vowel)                         (Matches the resulting surface consonant) • వేదండ ⟷ అ/ఆ/ఐ/ఔ                                    • వేదండ \[ద\] ⟷ త/థ/ద/ధ (Vargaja) • సారంగ ⟷ అ/ఆ/ఐ/ఔ                                    • సారంగ \[ర\] ⟷ ర (Ēkatara) • మనీష ⟷ ఇ/ఈ/ఎ/ఏ                                     • మనీష \[న\] ⟷ న/ణ (Sarasayati) • మంజీర ⟷ ఇ/ఈ/ఎ/ఏ                                    • మంజీర \[జ\] ⟷ చ/ఛ/జ/ఝ (Vargaja)

&nbsp;

\#\#\#\# Kūcimanchi Vēṅkaṭarāya's Sīsamālika Benchmark (\*Sukavi Manōrañjanamu\* 2-3-143) (6.46.8)

This classical pedagogical tour-de-force demonstrates both tracks back-to-back across 9 Pararūpa stems\[cite: 13\]:

1\. \*\*శకంధు:\*\* Track 1 matches \*\*అ $\\longleftrightarrow$ అ\*\* (\*అపుడు విప్రుండు శకంధు...\*); Track 2 matches \*\*క $\\longleftrightarrow$ క\*\* in \*క్షత్రియ వరుఁడు శకంధు...\*\[cite: 13\].

2\. \*\*మనీషా:\*\* Track 1 matches \*\*ఇ $\\longleftrightarrow$ ఈ\*\* (\*...మనీషి యొకండు...\*); Track 2 matches \*\*దిం $\\longleftrightarrow$ నీ\*\* (\*...క్రోధంబు మనీష చేత...\*)\[cite: 13\].

3\. \*\*హలీషా:\*\* Track 1 matches \*\*ఎ $\\longleftrightarrow$ ఈ\*\* (\*నెపుడు విప్రునకు హలీష...\*); Track 2 matches \*\*లీ $\\longleftrightarrow$ లి\*\* (\*...హలీషాపరులతోఁ జెలిమియుఁ...\*)\[cite: 13\].

4\. \*\*ఉష్ణీష:\*\* Track 1 matches \*\*ఎ $\\longleftrightarrow$ ఈ\*\* (\*...శిరమునుష్ణీషంబుఁ దాల్చె...\*); Track 2 matches \*\*షీ $\\longleftrightarrow$ జిం\*\* (\*...ఉష్ణీషాధిపతులు పూజించుచుండ...\*)\[cite: 13\].

5\. \*\*మస్తిష్క:\*\* Track 2 matches \*\*దె $\\longleftrightarrow$ తి\*\* (\*దెబ్బతో శిరము మస్తిష్కంబు...\*); Track 1 matches \*\*ఇ $\\longleftrightarrow$ ఇ\*\* (\*...ఇంతింతపైఁబడెను మస్తిష్కమెల్లఁ...\*)\[cite: 13\].

6\. \*\*మంజీర:\*\* Track 2 matches \*\*జె $\\longleftrightarrow$ జీ\*\* (\*జైలుల పాదముల మంజీరంబులలరె...\*); Track 1 matches \*\*ఈ $\\longleftrightarrow$ హె\*\* (\*...మంజీరా రవంబులు హెచ్చు మీఱె...\*)\[cite: 13\].

7\. \*\*కులటా:\*\* Track 1 matches \*\*ఆ $\\longleftrightarrow$ అ\*\* (\*నార్యజనములు కులటలనంటుదురె...\*); Track 2 matches \*\*ల $\\longleftrightarrow$ ల\*\* (\*...కులటలతోఁ జెల్మి ఖల జనులకగు...\*)\[cite: 13\].

8\. \*\*సీమంత:\*\* Track 2 matches \*\*మ $\\longleftrightarrow$ మ\*\* (\*మణిభూషలిడియె సీమంతంబుఁదీర్చి...\*); Track 1 matches \*\*అ $\\longleftrightarrow$ యా\*\* (\*...సీమంతిని యొకతె యొయ్యారమొదవ...\*)\[cite: 13\].

9\. \*\*పతంజలి:\*\* Track 1 matches \*\*అ $\\longleftrightarrow$ అ\*\* (\*నఖిల జనములు మ్రొక్కె పతంజలికిఁ...\*); Track 2 matches \*\*త $\\longleftrightarrow$ త\*\* (\*...పతంజలి యొనర్చె శబ్దశాస్త్రముకు భాష్య...\*)\[cite: 13\].

&nbsp;

\#\#\#\# Corpus Provenance Trail Across Common Pararūpa Stems (6.46.2 – 6.46.7)

\* \*\*వేదండ (Elephant):\*\*

  \* Track 1 (Vowel): \*\*అ $\\longleftrightarrow$ వేదండ \[అ\]:\*\* \*...వైరి వేదండ గండ విదారి ఘోరతరాసి...\* (\*Bhāratam\*, Ādi 3-228, Mattakōkila)\[cite: 13\]; \*...కీటఫణీంద్రపోతమదవేదండోగ్ర హింసావిచారిణి...\* (\*Śrīkālahastīśvara Śatakam\*)\[cite: 13\].

  \* Track 2 (Consonant): \*\*తా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...వేదండ ముఖాంగముల్ దృణ వితానముగాఁ గొని...\* (\*Bhāratam\*, Udyōga 4-1-234)\[cite: 13\]; \*\*దా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...మత్తవేదండమునెక్కి చాటెదను దాశరథీ...\* (\*Dāśarathī Śatakam\*)\[cite: 13\]; \*\*ధా $\\longleftrightarrow$ వేదండ \[ద\]:\*\* \*...వేదండస్వామి మదంబు సేసెఁ గరిణీధామంబులజ్జాడఁగాన్...\* (\*Kāśīkhaṇḍam\* 1-86)\[cite: 13\].

\* \*\*సారంగ (Deer / Bee / Elephant):\*\*

  \* Track 1 (Vowel): \*\*అ $\\longleftrightarrow$ సారంగ \[అ\]:\*\* \*అలరెన్ జైత్రబలాధినేత మదసారంగాళి...\* (\*Bhāgavatam\* 4-39)\[cite: 13\]; \*\*హ $\\longleftrightarrow$ సారంగ \[అ\]:\*\* \*...భద్ర సారంగ వరేణ్యముల్ పయికి హస్తములించుక...\* (\*Appakavīyamu\* 3-129 / \*Candrikāpariṇayamu\*)\[cite: 13\].

  \* Track 2 (Consonant): \*\*రా $\\longleftrightarrow$ సారంగి \[ర\]:\*\* \*...సారంగియ పోలెనుండెఁ గురురాజ భవత్సుతుసేన...\* (\*Appakavīyamu\* 3-130 / \*Bhāratam\*, Drōṇa 1-17)\[cite: 13\]; \*\*ర $\\longleftrightarrow$ సారంగ \[ర\]:\*\* \*గ్రహణ కాలంబు సుమ్ము సారంగనయన...\* (\*Kāśīkhaṇḍam\* 2-131)\[cite: 13\]; \*...సారంగ మదంబు లేఁజెమటఁ గ్రమ్మె...\* (\*Manu Caritra\* 2-32)\[cite: 13\].

\* \*\*మనీష (Intellect):\*\*

  \* Track 1 (Vowel): \*\*ఎ $\\longleftrightarrow$ మనీష \[ఈ\]:\*\* \*...మనీషమెయింజాలు రామునెదిరి...\* (\*Nirvacanōttara Rāmāyaṇamu\* 1-76)\[cite: 13\]; \*...మెప్పుడు చేరెదమొ యను మనీష దలంకన్...\* (\*Niraṅkuśōpākhyānamu\* 4-68)\[cite: 13\].

  \* Track 2 (Consonant): \*\*నీ $\\longleftrightarrow$ మనీషి \[నీ\]:\*\* \*...మనీషిజనము సెప్పు మాననీయచరిత్రా...\* (\*Bhāratam\*, Āraṇya 5-3-401)\[cite: 13\]; \*\*నె $\\longleftrightarrow$ మనీషిత \[నీ\]:\*\* \*నెఱయఁగఁ బ్రోచు మన్ముఖమనీషిత కావ్యకళా...\* (\*Bhāratam\*, Ādi 1-4)\[cite: 13\]; \*\*ని $\\longleftrightarrow$ మనీష \[నీ\]:\*\* \*నిరసించు విరక్తియుతమనీష జనించెన్...\* (\*Bhāratam\*, Udyōga 4-653)\[cite: 13\].

\* \*\*మార్తండ (Sun):\*\*

  \* Track 2 (Consonant): \*\*త $\\longleftrightarrow$ మార్తండుండు \[త\]:\*\* \*...తర బాహాగ్రపు సంగడంబనఁగ మార్తండుండు దోఁచెన్ దివిన్...\* (\*Manu Caritra\* 3-59)\[cite: 13\].

\* \*\*సీమంత (Parting of Hair / Woman):\*\*

  \* Track 2 (Consonant): \*\*మ $\\longleftrightarrow$ సీమంతిని \[మ\]:\*\* \*...వృద్ధ సీమంతినిఁ గాశికానగర మధ్య నివాసిని...\* (\*Kāśīkhaṇḍam\* 2-111)\[cite: 13\].

\* \*\*మంజీర (Anklet):\*\*

  \* Track 2 (Consonant): \*\*శీ $\\longleftrightarrow$ మంజీర \[జీ\] (Sarasayati):\*\* \*శ్రీ భూపుత్రి వివాహవేళ నిజమంజీరాగ్ర...\* (\*Manu Caritra\* 1-1)\[cite: 13\]; \*\*జే $\\longleftrightarrow$ మంజీర \[జీ\] (Prāṇi):\*\* \*...మంజీర ఝళంఝళధ్వనికిఁ జేరుట గాదు...\* (\*Manu Caritra\* 2-182)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# 6.47 ప్రాది యతులు (Prādi Yatulu — The 22 Sanskrit Prefixes Dual Caesura)

&nbsp;

\* \*\*Definition:\*\* Governs Sanskrit compound words formed by prefixing any of the \*\*22 Sanskrit Upasargas\*\* (\*prādayaḥ / prādulu\*: \*ప్ర, పరా, అప, సమ్, అను, అవ, నిస్, నిర్, దుస్, దుర్, వి, ఆజ్, ని, అధి, అపి, అతి, సు, ఉద్, అభి, ప్రతి, పరి, ఉప\*) to roots or nominal stems beginning with a vowel (\*\*అజాది ధాతువులు / అజాది శబ్దములు\*\*)\[cite: 13\].

\* \*\*The Structural Rule (ప్రాది యతి):\*\* At the compound syllable where the prefix fuses with the vowel stem via sandhi, \*\*Ubhaya Yati\*\* is licensed\[cite: 13\]:

  \* \*\*Track 1 (Svara Track):\*\* Match the underlying root-initial vowel (\*para-padādi svara\*)\[cite: 13\].

  \* \*\*Track 2 (Vyañjana Track):\*\* Match the resulting surface consonant cluster under standard consonant rules\[cite: 13\].

\* \*\*Consonant-Initial Roots Barred (హలాది శబ్దములు 6.47):\*\* When an upasarga prefixes to a consonant-initial root (\*ప్ర \+ మాన \= ప్రమాణ\*; \*అభి \+ మాన \= అభిమాన\*; \*వి \+ శేష \= విశేష\*), no vowel sandhi occurs\[cite: 13\]. These stems have \*\*zero Ubhaya Yati access\*\*; they scan solely as standard consonant yatis on the surface consonant\[cite: 13\].

\* \*\*The 22 Upasargas Inventory & Practical Nuances (6.47.1):\*\*

  \* Appakavi lists 20 prefixes, bundling \*nis/nir\* into \*\*నిర్\*\* and \*dus/dur\* into \*\*దుర్\*\* because only the \*repha\* forms participate in vowel compounding\[cite: 13\].

  \* \*Exclusion of 'ఆజ్' (Āṅ):\* The prefix \*āṅ\* sheds \*ṅ\* to leave vowel \*\*'ఆ'\*\*\[cite: 13\]. Compounding with vowel stems yields purely vocalic sandhi (\*ఆ \+ ఉదక \= ఓదక\*), producing no surface consonant to establish a consonant track\[cite: 13\]. It functions strictly under \*Svara-Pradhāna Yati\*\[cite: 13\].

&nbsp;

&nbsp;

             Prādi Yati Dual Engine Routing

           \[ Prefix (Upasarga) \+ Vowel-Initial Root \]

                               │

    ┌──────────────────────────┴──────────────────────────┐

    ▼                                                     ▼

&nbsp;

Track 1: Svara Mārga                                  Track 2: Vyañjana Mārga (Matches root-initial vowel)                          (Matches surface compound consonant) • ప్ర \+ ఆప్తి \= ప్రాప్తి ⟷ అ/ఆ/ఐ/ఔ                     • ప్రాప్తి \[ప\] ⟷ బ/భ/ప/ఫ (Vargaja) • సమ్ \+ ఈక్షా \= సమీక్ష ⟷ ఇ/ఈ/ఎ/ఏ                       • ప్రాప్తి \[ర\] ⟷ ర (Ēkatara via Repha) • అను \+ ఏషణ \= అన్వేషణ ⟷ ఇ/ఈ/ఎ/ఏ                        • సమీక్ష \[మ\] ⟷ మ (Prāṇi Yati)

&nbsp;

\#\#\#\# Appakavi's Complete Lakṣya-Lakṣaṇa Stanza (\*Appakavīyamu\* 3-133) (6.47.3)

Using the compound base \*\*'ప్రాప్తి'\*\* ($\\text{ప్ర} \+ \\text{ఆప్తి}$):

\* \*\*Line 1 (Track 1 — Svara Track):\*\* \*\*అ $\\longleftrightarrow$ ప్రాప్తి \[ఆ\]\*\* ($\\mathbf{అ \\longleftrightarrow ఆ}$ Svara Yati: \*అబ్జయోని రజోగుణప్రాప్తిఁదనరు...\*)\[cite: 13\].

\* \*\*Line 2 (Track 2 — Consonant Track via Stop):\*\* \*\*బ $\\longleftrightarrow$ ప్రాప్తి \[పా\]\*\* ($\\mathbf{బ \\longleftrightarrow ప}$ Vargaja Yati: \*బద్మనాభుఁడు సాత్వికప్రాప్తిఁదనరు...\*)\[cite: 13\].

\* \*\*Line 3 (Track 2 — Consonant Track via Liquid):\*\* \*\*ర $\\longleftrightarrow$ ప్రాప్తి \[రా\]\*\* ($\\mathbf{ర \\longleftrightarrow ర}$ Ēkatara Yati on conjunct repha: \*రజతగిరిమందిరుఁడు తమఃప్రాప్తిఁదనరు...\*)\[cite: 13\].

&nbsp;

\---

&nbsp;

\#\#\# Algorithmic Verification Matrix for Engine Ingestion (Part 11 Summary)

&nbsp;

| Rule Type | Primary Target Coordinates | Grammatical / Phonetic Engine Conditions | Status in Engine |

| :--- | :--- | :--- | :--- |

| \*\*'ఎఁడు' ప్రత్యయ యతి (6.42.2)\*\*\[cite: 13\] | Volumetric suffix \*\*-e'ḍu\*\*\[cite: 13\] | Compounding measurement affix\[cite: 13\]. Resolves on surface consonant\[cite: 13\]. Verbal infix \*-eḍu\* barred\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*'అవ' ప్రత్యయ యతి (6.42.3)\*\*\[cite: 13\] | Ordinal augment \*\*-ava\*\*\[cite: 13\] | \*\*Dual Track:\*\* Match vowel \*\*'అ'\*\* under Class 1 Svara Yati OR match surface consonant (\*\*డ, ల\*\*)\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*యుష్మదస్మదాది యతి (6.43)\*\*\[cite: 13\] | Pronouns ending in 'ద్': \*yuṣmad, asmad, bhavat, tad, yad, ētad\*\[cite: 13\] | \*\*Dual Track:\*\* Match underlying root-initial vowel OR match surface dental stop (\*\*ద, దా, దు\*\*)\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*కాకుస్వర యతి (6.44)\*\*\[cite: 13\] | Syllable bearing emotional protraction (\*pluta\*)\[cite: 13\] | \*\*Dual Track:\*\* Match protracted vowel (\*\*ఆ, ఈ, ఏ, ఓ\*\*) under Svara Yati OR match surface consonant under consonant rules\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*ప్లుతయుగ యతి (6.45)\*\*\[cite: 13\] | Both \*vali\* and \*yati-sthāna\* are pluta syllables\[cite: 13\] | Pure Svara Yati between pluta vowels; validates lines even if host consonants share zero affinity\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*పరరూప యతి (6.46)\*\*\[cite: 13\] | \*Śakandhvādi gaṇa\* compounds (\*వేదండ, సారంగ, మనీషా\*)\[cite: 13\] | \*\*Dual Track:\*\* Match absorbed pararūpa vowel OR match surface compound consonant\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

| \*\*ప్రాది యతులు (6.47)\*\*\[cite: 13\] | 22 Upasargas \+ Vowel-initial roots (\*అజాది ధాతువులు\*)\[cite: 13\] | \*\*Dual Track:\*\* Match underlying root-initial vowel OR match surface compound consonant\[cite: 13\]. Consonant stems barred\[cite: 13\]. | \*\*Canonical\*\*\[cite: 13\] |

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Prādi Yati (ప్రాదియతి)** governs Sandhi-fused syllables formed by Sanskrit prefixes (**ఉపసర్గలు**) attaching to vowel-initial (**అజాది**) stems, conferring **Ubhaya Yati (ఉభయయతి)** status so that the resulting syllable can match either by its constituent vowel or by any of its constituent consonants.

### Core Engine Mechanics

* **Dual-Target Resolution (ఉభయయతి):** At the sandhi-juncture syllable, the matcher must generate two valid candidate sets: a vowel target set (**అచ్చు యతి**) and a consonant target set (**హల్లు యతి**).  
* **Vowel Matching Pathway:** The constituent/resultant vowel of the base morpheme (*పరపదాది స్వరము*) matches via *Svara Yati* or *Sarasa Yati*.  
* **Consonant Matching Pathway:** If the juncture is a single consonant (e.g., *sam \+ a $\\to$ ma*), that consonant matches via *Prāṇi*, *Vargaja*, or *Bindu Yati*. If the juncture forms a conjunct (e.g., *pra \+ a $\\to$ prā*, *anu \+ a $\\to$ nv*), **any constituent consonant** in the cluster is independently eligible for matching (*Ekantara Yati*, *Prāṇi Yati*, *Vargaja Yati*, etc.).  
* **Halādi Root Disqualification:** If an upasarga attaches to a consonant-initial root (e.g., *ni-spashta*, *ni-vrishta*, *ni-krishta*), no internal sandhi vowel release occurs, and **Prādi Yati is strictly disabled**.

---

### Prefix Rules & Target Mapping

| Prefix (ఉపసర్గ) | Sample Token | Fused Akshara | Vowel Matching Options (అచ్చు యతి) | Consonant Matching Options (హల్లు యతి) | Engine Rule & Behavior |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ప్ర (Pra)**&nbsp; | ప్రాంగణ, ప్రాంచత్, ప్రాంత, ప్రాణ, ప్రార్థన |  |  |  |  |

| **ప్రా / ప్రాం**

 | `అ`

 | `ప`, `ర`

 | Conjunct split: allows either `ప` (Prāṇi/Vargaja) or `ర` (Ekantara).

| |  | ప్రాప్తి, ప్రారంభ, ప్రారబ్ధ

| **ప్రా**

 | `ఆ`

 | `ప`, `ర`

 | Vowel shifts to long `ఆ` due to Savarṇa Dīrgha.

| |  | ప్రోద్యత్, ప్రోత్ఫుల్ల, ప్రోర్జిత

| **ప్రో**

 | `ఉ` / `ఊ`

 | `ప` (పో), `ర` (రో)

| Guṇa Sandhi; vowel matches underlying base vowel `ఉ`.

| |  | ప్రేక్ష, ప్రేరణ, ప్రేత

| **ప్రే**

 | `ఇ` / `ఈ`

 | `ప` (పే), `ర` (రే)

| Matches underlying `ఇ` / `ఈ` or conjunct consonants.

| | **పరా (Parā)**

 | పరాఙ్ముఖ

| **రా**

 | `అ`

 | `ర`

 | Resolves to `అ` via base stem *añc*.

| |  | పలాయన

| **లా**

 | `అ`

 | `ల`

 | Morphological rule *'Upasargasyāyatau'*: `ర` shifts to `ల` before root *ay*; matches `ల` or `అ`.

| |  | పరేత

| **రే**

 | `ఇ`

 | `ర` (రే)

| Fuses *parā \+ ita*; vowel matches `ఇ`.

| |  | పరోఢ

| **రో**

 | `ఊ`

 | `ర` (రో)

| Fuses *parā \+ ūḍha*; vowel matches `ఊ`.

| | **అప (Apa)**

 | అపాయ, అపాంగ

| **పా**

 | `అ`

 | `ప`

 | Matches `అ` or single consonant `ప`.

| |  | అపేక్ష, అపేత, అపోహ

| **పే / పో**

 | `ఈ` / `ఇ` / `ఊ`

 | `ప` (పే / పో)

| Matches base vowel (`ఈ`/`ఊ`) or consonant `ప`.

| | **సమ్ (Sam)**

 | సమంచిత, సమక్ష, సమగ్ర, సమర్థ, సమస్త

| **మ / మం**

 | `అ`

 | `మ`

 | Anusvāra-m fusion; matches base `అ` or `మ`.

| |  | సమాఖ్య, సమాగమ, సమాజ, సమాధి, సమాన, సమాప్తి, సమారంభ

| **మా**

 | `ఆ`

 | `మ`

 | Matches long `ఆ` or consonant `మ`.

| |  | సమిద్ధ, సమీర

| **మి / మీ**

 | `ఇ` / `ఈ`

 | `మ` (మి / మీ)

| Matches root vowel `ఇ` / `ఈ` or consonant `మ`.

| |  | సముజ్జ్వల, సముద్ధత, సమూహ

| **ము / మూ**

 | `ఉ` / `ఊ`

 | `మ` (ము / మూ)

| Matches root vowel `ఉ` / `ఊ` or consonant `మ`.

| |  | సమేత

| **మే**

 | `ఏ`

 | `మ` (మే)

| Derives from *sam \+ āb \+ ita $\\to$ sam \+ ēta*; matches `ఏ` or `మ`.

| | **అను (Anu)**

 | అన్వయ, అన్వర్థ

| **న్వ**

 | `అ`

 | `న`, `వ`

 | Yan-sandhi cluster allows `అ` or split consonants `న` / `వ`.

| |  | అన్విత, అన్వీత, అన్వీక్షణ

| **న్వి / న్వీ**

 | `ఇ` / `ఈ`

 | `న` (ని/నీ), `వ` (వి/వీ)

| Matches root vowel `ఇ`/`ఈ` or consonants `న`/`వ`.

| | **అవ (Ava)**

 | అవాప్త, అవాప్తి, అవేక్షణ

| **వా / వే**

 | `ఆ` / `ఈ`

 | `వ`

 | Matches `ఆ`/`ఈ` or consonant `వ`.

| | **నిర్ (Nir)**

 | నిరంకుశ, నిరంతర, నిరంజన

| **రం**

 | `అ`

 | `ర`

 | Single repha fusion; matches `అ` or `ర`.

| |  | నిరాస, నిరామయ, నిరాశ

| **రా**

 | `ఆ`

 | `ర`

 | Matches `ఆ` or `ర`.

| |  | నిరీక్ష, నిరీక్షణ

| **రీ**

 | `ఈ`

 | `ర`

 | Matches `ఈ` or `ర`.

| | **దుర్ (Dur)**

 | దురంత, దురభిమాన, దురాత్మ, దురుక్తి

| **ర / రా / రు**

 | `అ` / `ఆ` / `ఉ`

 | `ర`

 | Matches stem vowels `అ`/`ఆ`/`ఉ` or consonant `ర`.

| | **వి (Vi)**

 | వీక్ష, వీడ్య

| **వీ**

 | `ఈ`

 | `వ` (వీ)

| Savarṇa Dīrgha: clear split between `ఈ` and `వ`.

| |  | వ్యాప్త, వ్యసన, వ్యాకుల

| **వ్యా / వ్య**

 | `ఆ` / `అ`

 | `వ`, `య`

 | Yan-sandhi cluster: matches `ఆ`/`అ` or consonants `వ`/`య`.

| | **ని (Ni)**

 | న్యాస, న్యస్త, న్యాయ

| **న్యా / న్య**

 | `ఆ` / `అ`

 | `న`, `య`

 | Matches `ఆ`/`అ` or consonants `న`/`య`.

| | **అధి (Adhi)**

 | అధీన, అధీశ్వర

| **ధీ**

 | `ఇ` / `ఈ`

 | `ధ` (ధీ)

| Savarṇa Dīrgha: matches `ఇ`/`ఈ` or `ధ`.

| |  | అధ్యాత్మ, అధ్యయన

| **ధ్యా / ధ్య**

 | `ఆ` / `అ`

 | `ధ`, `య`

 | Yan-sandhi cluster: matches `ఆ`/`అ` or `ధ`/`య`.

| | **అపి (Api)**

 | అప్యయ

| **ప్య**

 | `అ`

 | `ప`, `య`

 | Matches `అ` or consonants `ప`/`య`.

| |  | అపీత

| **పీ**

 | `ఇ`

 | `ప` (పీ)

| Savarṇa Dīrgha: matches `ఇ` or `ప`.

| | **అతి (Ati)**

 | అతీత, అతీంద్రియ

| **తీ**

 | `ఇ`

 | `త` (తీ)

| Savarṇa Dīrgha: matches `ఇ` or `త`.

| |  | అత్యంత, అత్యాదర, అత్యుత్తమ

| **త్య / త్యా / త్యు**

 | `అ` / `ఆ` / `ఉ`

 | `త`, `య`

 | Matches base vowel or consonants `త`/`య`.

| | **సు (Su)**

 | సూక్తి, సూక్త

| **సూ**

 | `ఉ`

 | `స` (సూ)

| Savarṇa Dīrgha: matches `ఉ` or `స`.

| |  | స్వాగత, స్వాధ్యాయ, స్వచ్ఛ, స్వస్తి

| **స్వా / స్వ**

 | `ఆ` / `అ`

 | `స`, `వ`

 | Yan-sandhi cluster: matches `ఆ`/`అ` or `స`/`వ`.

|

---

### Disambiguation & Implementation Nuances

* **The Yanādēśa Ambiguity Rule (*ఇ-కారాంత పరిశీలన*):**  
* When prefixes ending in `ఇ` (*vi, ni, adhi, api, ati, abhi, prati, pari*) undergo Yanādēśa with vowels ($i \+ a \\to ya$, $i \+ \\bar{a} \\to y\\bar{a}$, $i \+ u \\to yu$), matching the base vowel ($a, \\bar{a}, u$) is mathematically equivalent to matching the semi-vowel ($ya, y\\bar{a}, yu$) under **Sarasa Yati (సరసయతి)**.  
* *Engine parser note:* In words like **వ్యాప్తి** or **అత్యంత**, an alignment to `అ`/`ఆ` can technically be logged either as Prādi Vowel Yati or as Consonant Yati with `య` under Sarasa Yati.  
* *Unambiguous test cases:* Only **Savarṇa Dīrgha** formations (e.g., *vi \+ īkṣā \= vīkṣā*, *ati \+ ita \= atīta*, *adhi \+ īśvara \= adhīśvara*) yield an indisputable binary division between pure Svara Yati (`ఈ`/`ఇ`) and pure Hal Yati (`వ`/`త`/`ధ`).  
* **Parā Upasarga Viability:**  
* While Appakavi claimed *Parā* has no entry in Telugu poetry, classical usage confirms valid Ubhaya Yati in tokens like **పరాఙ్ముఖ** and **పలాయన**.  
* Appakavi classified *పలాయన* under *Nitya Samāsa Yati*, but because the phonological shift ($r \\to l$) occurs specifically via the grammatical sutra *'Upasargasyāyatau'* on an upasarga, it belongs functionally to **Prādi Yati**.  
* **Nested Prefixes:**  
* In double prefixes (e.g., *sam \+ pra \+ āpaṇa \= samprāpaṇambu*), if yati is executed on `ప్రా`, the engine evaluates the rule against the immediate prefix **ప్ర**, disregarding the preceding **సమ్**.

---

### Provenance Trail

* **Grammatical Sūtras Cited:**  
* Pāṇinian / Sanskrit morphological rule for *Parā* $\\to$ *Palā*: *'ఉపసర్గస్యాయతౌ'* (Pāṇini 8-2-19).  
* **Prosodic Treatises & Commentaries:**  
* *Appakavīyamu* (noted for views on *Prāpti*, absence of *Parā*, and classifying *Palāyana* as *Nitya Samāsa Yati*).  
* *Kāvyālaṅkāra Cūḍāmaṇi* (cited for *Parētanāthuḍu / Parōḍha* under 6.47.5).  
* *Lakshaṇa Śirōmaṇi* (cited for Bhīmana's *Śivastuti* under *Duranta*, 6.47.11).  
* Ranga Kavi's examples from Peddiraju's *Harikathāsudhārasamu* and Nācana Sōmana's *Haravilāsamu* (for *Apyaya*, 6.47.15).  
* **Primary Classical Literature Sources:**  
* *Mahābhāratamu* (Ādi, Sabhā, Vana, Virāṭa, Bhīshma, Śānti, Anuśāsanika, Mauśala parvas).  
* *Śrīmad Bhāgavatamu* (Pōtana).  
* *Āmuktamālyada* (Śrī Krishṇadēvarāya, Maha-sragdharā meter citations).  
* *Kāśīkhaṇḍamu* and *Haravilāsamu* (Śrīnātha).  
* *Ranganātha Rāmāyaṇamu* (Dvipada meter citations) and *Bhāskara Rāmāyaṇamu*.  
* *Śrīkālahastīśvara Śatakamu* and *Bhāskara Śatakamu*.  
* *Kumārasambhavamu* (Nanne Chōḍa, Svāgatā meter citations).

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Prādi Yati (ఉద్, అభి, ప్రతి, పరి, ఉప) and Nitya Samāsa Yati Engine Architecture** expands the Ubhaya Yati (ఉభయయతి) search space for compound and prefixed sandhi junctures while enforcing strict boundary conditions to reject pseudo-Prādi formations.

---

### Core Engine Mechanics

* **Dual-Target Junction State (ఉభయయతి):** When an upasarga (prefix) attaches to an ajādi (vowel-initial) stem, the fused syllable acts as a dual-target matching node. The matcher evaluates both the constituent/resultant vowel of the base stem (**అచ్చు యతి**) and the consonant(s) involved in the sandhi formation (**హల్లు యతి**).  
* **Nested Prefix Recursion (బహుళోపసర్గలు):** In tokens containing layered prefixes (e.g., *sam \+ ud \+ agra $\\to$ samudagra*, *sam \+ upa \+ ita $\\to$ samupēta*), the parser registers **two distinct Prādi Yati nodes**:  
* Node 1 (Outer Prefix *సమ్* at `ము`): Targets vowel `ఉ` or consonant `మ`.  
* Node 2 (Inner Prefix *ఉద్* / *ఉప* at `ద` / `పే`): Targets the base stem vowel (`అ` / `ఇ`) or the respective consonant (`ద` / `ప`).  
* **Nitya Samāsa Ubhaya Yati Principle (నిత్యసమాస యతి):** Sanskrit lexical compounds that are indivisible (*avigrahō svapadavigrahō vā nitya samāsaḥ*) or exhibit an inseparable single-word appearance (*ēkapadavat*) license **Ubhaya Yati** at the sandhi juncture if the second member (*uttara-pada*) is vowel-initial (*ajādi*).

---

### Prefix Rules & Target Mapping Table

| Prefix (ఉపసర్గ) | Target Syllable | Underlying Sandhi | Vowel Candidate Set (అచ్చు యతి) | Consonant Candidate Set (హల్లు యతి) | Engine Rule & Behavior |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **ఉద్ (Ud)**&nbsp; | **దం / ద**&nbsp; | ఉద్ \+ అ... (ఉదంచిత, ఉదగ్ర) |  |  |  |

| `అ` (Svara Yati)

| `ద` (matches `ద`, `తా`, `థై`, `ధ` via Vargaja/Prāṇi)

| Root vowel `అ` is isolated; consonant `ద` matches across dental varga.

| |  | **దా**

 | ఉద్ \+ ఆ... (ఉదాత్త, ఉదార, ఉదాసీన)

| `ఆ` (Svara / Sarasa with `య`)

| `ద` (matches `ద`, `త`, `తా` via Vargaja/Prāṇi)

| Base stem vowel `ఆ` is isolated; consonant `ద` matches dental class.

| |  | **దీ**

 | ఉద్ \+ ఈ... (ఉదీర, ఉదీరణ, ఉదీర్ణ)

| `ఈ` (Svara Yati with `ఇ`, `ఈ`, `ఎ`)

| `ద` (matches `దీ`, `తీ` via Vargaja/Prāṇi)

| Matches base vowel `ఈ` or consonant `ద`.

| | **అభి (Abhi)**

 | **భీ**

 | అభి \+ ఈ... (అభీప్సిత, అభీహిత)

| `ఈ` (Svara Yati with `ఎ`, `ఈ`)

| `భ` (matches `భీ`, `పె`, `భ` via Vargaja)

| Root is *īpsa* / *īhita*; base vowel isolates to long `ఈ`.

| |  | **భీ**

 | అభి \+ ఇ... (అభీష్ట)

| `ఇ` (Svara Yati with `ఇ`, `ఈ`)

| `భ` (matches `భీ`, `పి`, `పీ`, `బె` via Vargaja)

| Root is *iṣṭa*; base vowel isolates to short `ఇ`.

| |  | **భ్యం / భ్య**

 | అభి \+ అ... (అభ్యంతర, అభ్యర్థన, అభ్యుదయ)

| `అ` / `ఉ` (Svara / Sarasa with `య`)

| `భ` or `య` (Prāṇi / Vargaja)

| Yan-sandhi conjunct split: matches base vowel or split consonants `భ` / `య`.

| | **ప్రతి (Prati)**

 | **త్య / త్యే**

 | ప్రతి \+ అ... / ఏ... (ప్రత్యక్ష, ప్రత్యహము, ప్రత్యేక)

| `అ` / `ఏ` (Svara / Sarasa with `య`)

| `త` or `య` (Prāṇi / Vargaja with `ధ`, `త`)

| Conjunct split allows `త` or `య` independently.

| |  | **తీ**

 | ప్రతి \+ ఈ... / ఇ... (ప్రతీక్ష, ప్రతీత)

| `ఈ` / `ఇ` (Svara Yati)

| `త` (తీ)

| Savarṇa Dīrgha: clean split between base vowel `ఈ`/`ఇ` and consonant `త`.

| | **పరి (Pari)**

 | **రీ**

 | పరి \+ ఈ... (పరీక్ష)

| `ఈ` (Svara Yati with `ఇ`, `ఈ`)

| `ర` (రీ)

| Savarṇa Dīrgha juncture.

| |  | **ర్య**

 | పరి \+ అ... / ఆ... (పర్యంత, పర్యాయ)

| `అ` / `ఆ` (Svara / Sarasa with `య`)

| `ర` or `య`

 | Yan-sandhi split licenses either `ర` or `య`.

| | **ఉప (Upa)**

 | **పాం / పా**

 | ఉప \+ అ... (ఉపాంత, ఉపాయ, ఉపాయన)

| `అ` (Svara / Sarasa with `య`, `హ`)

| `ప` (Prāṇi `ప`, Vargaja `భా`)

| Base stem begins with `అ`.

| |  | **పా / పార్**

 | ఉప \+ ఆ... (ఉపార్జన, ఉపాసన, ఉపాఖ్యాన)

| `ఆ` (Svara Yati with `అ`, `ఆ`, `య`)

| `ప` (Prāṇi `పా`, Vargaja `బ`)

| Base stem begins with `ఆ`.

| |  | **పే**

 | ఉప \+ ఈ... (ఉపేక్ష)

| `ఈ` (Svara Yati with `ఇ`, `ఎ`, `ఈ`)

| `ప` (Prāṇi `పి`, Vargaja `బె`)

| Guṇa sandhi; isolates to base vowel `ఈ`.

| |  | **పే**

 | ఉప \+ ఇ... (ఉపేత, ఉపేంద్ర)

| `ఇ` (Svara / Sarasa with `హృ`, `ఇ`)

| `ప` (Vargaja `బి`, `భీ`)

| Guṇa sandhi; isolates to base vowel `ఇ`.

|

---

### Disqualification & Boundary Rules (ప్రాదులతో యతులు vs. ప్రాదియతులు)

The engine must strictly distinguish between **True Prādi Yati** and **Ordinary Yati on Prefix Tokens**. A prefix occurring in a word does not inherently trigger Ubhaya Yati.

Is word prefixed by Upasarga?

  ├── NO  ──\> Standard Yati Engine

  └── YES ──\> Is stem Ajādi (Vowel-Initial) with Sandhi?

                ├── NO (Halādi Stem: e.g., anu+rāga, su+mahat) 

                │     └── DISQUALIFIED from Prādi Yati. (Evaluated strictly as standard Svara or Vyañjana Yati)

                └── YES (Ajādi Stem: e.g., ud+agra, upa+īkṣā)

                      └── Is alignment on the fused sandhi syllable?

                            ├── NO (Alignment on prefix head: e.g., 'ni' in niratiśaya)

                            │     └── DISQUALIFIED from Prādi Yati. (Standard Vyañjana Yati only)

                            └── YES ──\> VALID PRĀDI YATI (License Ubhaya Yati)

&nbsp;

* **Halādi Root Disqualification:** If an upasarga precedes a consonant-initial root, sandhi does not release a root vowel. The token is disqualified from Ubhaya Yati:  
* *అనురాగము (anu \+ rāga):* Sandhi with a consonant. Alignment at `అ` is an ordinary **Svara Yati**, not Prādi Yati.  
* *సుమహత్ (su \+ mahat):* Fused with consonant `మ`. Matching `సు-శో` is ordinary **Ūṣma Yati**, not Prādi Yati.  
* *నిస్తరించి (nis \+ tariñci), నిర్ధూత (nir \+ dhūta), విఖ్యాత (vi \+ khyāta), సంతోష (sam \+ tōṣa):* Ordinary **Vyañjana Yati**.  
* **Target Position Error Disqualification:** In *నిరతిశయ (nir \+ atiśaya)*, the Prādi node is at `ర` (`అ` or `ర`). If the poet aligns the initial `ని` (`ని-ని`), it is an ordinary **Vyañjana/Prāṇi Yati**, not Prādi Yati.  
* **Upasarga "Āṅ" (ఆఙ్) Exception:** The prefix *ఆఙ్* drops `ఙ్` to become `ఆ` (e.g., *ā \+ kalita \= ākalita*). Because it attaches to consonant roots without an internal vowel-releasing sandhi, it provides no dual consonant/vowel choice; hence **Prādi Yati is invalid** (evaluated solely as Svara Yati `ఆ`).  
* **Treatise Errata Guardrail:** *Lakshaṇa Śirōmaṇi* erroneously classified *anurāga*, *sumahat*, *nistarinci*, and *ākalita* as Prādi Yati. The engine parser must reject these classifications.

---

### Provenance Trail

* **Prosodic & Grammatical Treatises:**  
* *Kāvyālaṅkāra Cūḍāmaṇi* (Vinnakōta Peddana, Ullāsa 7, verses 48–52): Complete illustrative framework demonstrating Prādi Yatis systematically for *Pra, Parā, Apa, Sam, Anu, Su, Prati, Nir, Dur, Adhi, Ni, Upa,* and *Abhi*.  
* *Lakshaṇa Śirōmaṇi*: Cited for analytical critique and correction of false Prādi classifications.  
* *Appakavīyamu*: Baseline lakshya-lakshaṇa references.  
* Sanskrit Sūtra: *'అవిగ్రహో స్వపదవిగ్రహో వా నిత్యసమాసః'* governing Nitya Samāsa criteria.  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-10) *udātta*, (2-225) *vikhyāta*, (3-83) *abhīṣṭa*, (4-68) *anurāga*.  
* *Vana Parva (Āraṇya):* (5-121) *udagra*, (5-227) *udīrṇa*.  
* *Virāṭa Parva:* (1-168) *samudagra*, (2-234) *nistarinci*.  
* *Bhīṣma Parva:* (2-210) *upēkṣa*.  
* *Śānti Parva:* (6-28) *upēkṣa*.  
* *Anuśāsanika Parva:* (5-424) *upārjita / upāsana* (illustrating both vowel and consonant yati within the same verse by Tikkana).  
* *Āśramavāsa Parva:* (2-82) *abhīṣṭa*.  
* *Aśvamēdha Parva:* (2-190) *upāya*.  
* *Svargārōhaṇa Parva:* (62) *upānta*.  
* *Śrīmad Bhāgavatamu* (Pōtana): (7-111) *upānta*, (7-181) *upāya*, (8-116) *nirdhūta*, (10-uttara-955) *udāra*.  
* *Bhāskara Rāmāyaṇamu*: Bāla Kāṇḍa (107) *upāyana*.  
* *Rāmābhyudayamu*: (6-26) *udāra*.  
* *Kavikarṇa Rasāyanamu*: (1-119) *upēta*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Nitya Samāsa Yati (నిత్యసమాస యతి)** expands the **Ubhaya Yati (ఉభయయతి)** engine to Sanskrit indivisible compounds (*avigrahō svapadavigrahō vā nitya samāsaḥ*) and words presenting an inseparable single-word appearance (*ēkapadavat*) where an ajādi (vowel-initial) second element fuses with the first element via sandhi. The fused sandhi syllable permits matching either through its constituent/resultant vowel (**అచ్చు యతి**) or through any of its constituent consonants (**హల్లు యతి**).

---

### Core Engine Mechanics

* **Dual-Track Target Evaluation (ఉభయయతి):** When a lexical token qualifies as a Nitya Samāsa or fused compound, the engine exposes both the vowel match space and consonant match space at the sandhi junction.  
* **Vowel Matching Pathway (అచ్చు యతి):**  
* The constituent base vowel (*parapadādi svaramu*) matches via *Svara Yati* or *Sarasa Yati*.  
* Where vowel modifications occur (e.g., *Vṛddhi* or *Gūḍha Svara*), both the underlying root vowel and the resulting morphed vowel can become eligible.  
* **Consonant Matching Pathway (హల్లు యతి):**  
* If the junction is a single consonant (e.g., `మా`, `సా`, `వా`), it matches its varga/class equivalents via *Prāṇi*, *Vargaja*, *Sarasa*, or *Ūṣma Yati*.  
* If the junction is a conjunct cluster (e.g., `ర్ణా`, `ద్వీ`, `స్వాం`, `ద్ధాం`, `త్తాం`, `న్యో`, `ద్వా`, `క్షౌ`), **every constituent consonant in the cluster is independently licensed** to match.

---

### Lexical Junction & Target Mapping Table

| Compound Token | Juncture Syllable | Underlying Sandhi | Vowel Candidate Set (అచ్చు యతి) | Consonant Candidate Set (హల్లు యతి) | Engine Rule & Verification Notes |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **కర్ణాట (Karṇāṭa)**&nbsp; | **ర్ణా**&nbsp; | కర్ణ \+ అట |  |  |  |

| `అ`

 | `ర`, `ణ`

 | Conjunct split allows `ర` (Ekantara) or `ణ` (Sarasa with `న`, `నా`).

| | **వనౌకస్ (Vanaukas)**

 | **నౌ**

 | వన \+ ఓకస్

| `ఓ` or `ఔ`

 | `న` (నౌ)

| Vṛddhi Sandhi: licenses base `ఓ` or ādeśa `ఔ` (matches `అ` via Svara Yati); consonant `న` matches via Prāṇi Yati.

| | **ద్వీప (Dvīpa)**

 | **ద్వీ**

 | ద్వి \+ అప

| `అ` (gūḍha) or `ఈ`

 | `ద` (దీ), `వ` (వీ)

| Pāṇini 6-3-97 replaces `అ` with `ఈ`; licenses both underlying `అ` and resultant `ఈ`; cluster splits to `ద` or `వ`.

| | **అంతరీప (Antarīpa)**

 | **రీ**

 | అంతర్ \+ అప

| `అ` or `ఈ`

 | `ర` (రీ)

| Same Pāṇinian formation; licenses `అ`, `ఈ`, or consonant `ర`.

| | **ప్రతీప (Pratīpa)**

 | **తీ**

 | ప్రతి \+ అప

| `అ` or `ఈ`

 | `త` (తీ)

| Upasarga-based Nitya Samāsa; licenses `అ`, `ఈ`, or consonant `త`.

| | **సమీప (Samīpa)**

 | **మీ**

 | సమ్ \+ అప

| `అ` or `ఈ`

 | `మ` (మీ)

| Classical poets match either base `అ` or resultant `ఈ`; consonant matches `మ` via Prāṇi Yati.

| | **ఆపోశన (Āpōśana)**

 | **పో**

 | ఆప \+ అశన

| `అ`

 | `ప` (పో)

| Pṛṣōdarādi formation; matches base vowel `అ` or consonant `ప` (matches `భూ` via Vargaja).

| | **స్వాంత (Svānta)**

 | **స్వాం**

 | స్వ \+ అంత

| `అ`

 | `స`, `వ`

 | Conjunct split licenses `స` (Prāṇi/Sarasa/Ūṣma) or `వ` independently.

| | **ఏకాంత (Ēkānta)**

 | **కాం**

 | ఏక \+ అంత

| `అ`

 | `క` (కా)

| Matches base vowel `అ` or consonant `క` (Prāṇi `క`/`కా`, Vargaja `గ`/`గా`).

| | **అన్యోన్య (Anyōnya)**

 | **న్యో**

 | అన్య \+ అన్య

| `అ`

 | `న` (నో), `య` (యో)

| Cluster split licenses `న` (Prāṇi with `ను`, `నో`) or `య` (Sarasa with `ఒ`, `ఉ`).

| | **ద్వార (Dvāra)**

 | **ద్వా**

 | ద్వి \+ అర $\\to$ ద్వ \+ అర

| `అ`

 | `ద` (దా), `వ` (వా)

| Pṛṣōdarādi nipātana; cluster splits to `ద` (Prāṇi/Vargaja with `త`, `ధ`) or `వ` (Prāṇi/Abhēda with `ప`).

| | **గవాక్ష (Gavākṣa)**

 | **వా**

 | గో \+ అక్ష

| `అ`

 | `వ` (వా)

| Avaṅ-ādēśa followed by Savarṇa Dīrgha; matches base vowel `అ` or consonant `వ`.

|

---

### Special Compound Classes

**The \-అంత (-anta) Suffix Class**

* **సిద్ధాంత (Siddhānta) & రాద్ధాంత (Rāddhānta):** Junction at `ద్ధాం` fuses *siddha/rāddha \+ anta*. Vowel targets `అ`; consonant cluster independently licenses either `ద` or `ధ` via Prāṇi or Vargaja Yati. *(Note: In classical Telugu kāvya, "rāddhānta" means established truth/siddhānta, not commotion)*.  
* **శుద్ధాంత (Śuddhānta):** Junction at `ద్ధాం` (*śuddha \+ anta*). Vowel targets `అ`; consonant cluster licenses `ద` or `ధ`.  
* **వృత్తాంత (Vṛttānta):** Junction at `త్తాం` (*vṛtta \+ anta*). Vowel targets `అ`; consonant cluster licenses `త` (matches `తా`, `ద`, `ధా` via Prāṇi and Vargaja Yati).  
* **లతాంత (Latānta):** Junction at `తాం` (*latā \+ anta*) targets vowel `అ` or consonant `త`.

**The \-అయన (-ayana) Suffix Class**

Compounds ending with the root *ayana* (abode/path/motion) induce Ubhaya Yati at the sandhi syllable, with secondary phonological retroflexion ($n \\to ṇ$) triggered by preceding rēpha:

* **వాతాయన (Vātāyana):** *vāta \+ ayana*; juncture `తా` matches vowel `అ` or consonant `త`.  
* **రసాయన (Rasāyana):** *rasa \+ ayana*; juncture `సా` matches vowel `అ` or consonant `స`.  
* **రామాయణ (Rāmāyaṇa):** *rāma \+ ayana*; juncture `మా` matches vowel `అ` or consonant `మ` (demonstrated by Tikkana executing both matches in a single verse).  
* **బాదరాయణ (Bādarāyaṇa) & బాదరాయణి (Bādarāyaṇi):** *badara \+ ayana*; juncture `రా` matches vowel `అ` or consonant `ర`.  
* **పరాయణ (Parāyaṇa) & పారాయణ (Pārāyaṇa):** *para/pāra \+ ayana*; juncture `రా` matches vowel `అ` or consonant `ర`.  
* **Astronomical & Gotra Patronymics:** *ఉత్తరాయణ*, *దక్షిణాయన*, *సాంఖ్యాయన*, *శాకటాయన*, *కాత్యాయన*, *వాత్స్యాయన*, and *బోధాయన* all adhere strictly to Ubhaya Yati at the sandhi juncture.

**The \-అండ (-aṇḍa) Suffix Class**

* **మార్తాండ (Mārtāṇḍa):** Fused juncture `ర్తాం` (*mārta \+ aṇḍa*) licenses vowel `అ` or conjunct split consonants `ర` and `త` (Vargaja with `ద`, `ధ`). *(Note: Mārtāṇḍa falls under Nitya Samāsa Yati, whereas its variant Mārtaṇḍa falls under Pararūpa Yati)*.  
* **బ్రహ్మాండ (Brahmāṇḍa):** Juncture `హ్మాం` (*brahma \+ aṇḍa*) licenses vowel `అ` (or Sarasa with `హ`) and consonant `మ`.  
* **అజాండ (Ajāṇḍa):** Juncture `జాం` (*aja \+ aṇḍa*) licenses vowel `అ` or consonant `జ`.

**Akṣauhiṇi vs. Akṣōhiṇi Dual Formations**

Both lexical variants represent valid Nitya Samāsa army divisions and provide dual-track licensing at the conjunct junction:

| Lexical Form | Fused Syllable | Grammatical Process | Vowel Matching Options (అచ్చు యతి) | Consonant Matching Options (హల్లు యతి) |
| :---- | :---- | :---- | :---- | :---- |
| **అక్షౌహిణి (Akṣauhiṇi)**&nbsp; | **క్షౌ**&nbsp; | Vṛddhi by Vārtika: *Akṣādūhinyāmupasaṁkhyānam*&nbsp; | Underlying base `ఊ` or resultant `ఔ`&nbsp; | `క` (కౌ via Vargaja with `గ`) or `ష` (షౌ via Ūṣma with `స`) |

| | **అక్షోహిణి (Akṣōhiṇi)**

 | **క్షో**

 | Guṇa formation validated by Chellapilla via *akṣa \+ ūhin \+ ṅīp*

 | Underlying base `ఊ`

 | `క` (కో via Prāṇi with `కొ`, `కూ`) or `ష` (షో via Ūṣma with `సు`)

|

---

### Semantic Conditioning & Disambiguation Rules

The engine must conditionally evaluate token semantics and morphological boundaries before opening the Ubhaya Yati search space:

* **పదార్థ (Padārtha) Ambiguity Gate:**  
* If used in the sense of **"word meaning"** (*padasya arthaḥ*), it is an ordinary Ṣaṣṭhī Tatpuruṣa compound. **Ubhaya Yati is disabled**; only regular Svara Yati on `అ` is valid.  
* If used in the philosophical sense of **"entity / object / substance"** (*pada-bōdhyō'rthaḥ \= vastuvu*), it is an indivisible Nitya Samāsa. **Ubhaya Yati is enabled** at `దా`: matches vowel `అ` or consonant `ద` (Prāṇi `ద`, Vargaja `ధ`).  
* **నిశాంత (Niśānta) Ambiguity Gate:**  
* If used in the sense of **"dwelling / house"** (*niśāyām avaśyam amyatē \= gṛhamu*), it functions as a Nitya Samāsa. **Ubhaya Yati is enabled** at `శాం`: matches vowel `అ` or consonant `శ`.  
* If used in the temporal sense of **"end of night / dawn"** (*niśāyāḥ antaḥ \= vēkuva*), it is an ordinary Tatpuruṣa. **Ubhaya Yati is disabled**; only standard Svara Yati on `అ` is permitted.  
* **Sahārthaka Prefix "స" (Sa-) Boundaries:**  
* When prefix *sa-* (with/together) attaches to an **ajādi (vowel-initial) stem**, it fuses into an inseparable single-word appearance (*ēkapadavat*) and **licenses Ubhaya Yati**:  
* *సాంగ (sa \+ aṅga):* Juncture `సాం` matches vowel `అ` or consonant `స` (Prāṇi `స`, Ūṣma `శ`).  
* *సాదర (sa \+ ādara):* Juncture `సా` matches vowel `ఆ` or consonant `స`.  
* *సార్థ / సార్థక (sa \+ artha):* Juncture `సా` matches vowel `అ` or consonant `స`.  
* When prefix *sa-* attaches to a **halādi (consonant-initial) stem** (e.g., *sa-kuṭumba, sa-vinaya, sa-karuṇa*), **Ubhaya Yati is strictly disabled** because no internal vowel sandhi occurs.  
* **The విశ్వామిత్ర (Viśvāmitra) Anomaly:**  
* *Grammatical Reality:* Pāṇini sūtra *'Mitrēcarṣau'* (6-3-130) lengthens the vowel of *viśva* preceding *mitra* specifically when naming a sage (*viśvaṁ mitraṁ yasya \= Viśvāmitraḥ*). There is **no underlying vowel sandhi** (it is not *viśva \+ amitra*, which would mean "enemy of the world"). Strictly speaking, only consonant matches on `శా` or `వా` are grammatically sound.  
* *Engine Emulation:* Because major poets (Pōtana, Ranganaatha Ramayanam, Errapragada in Śṛṅgāra Śākuntalamu, Gōpīnātha Rāmāyaṇamu, Hariścandrōpākhyānamu) explicitly employed vowel matches on `అ`, the engine must support **both Acchu Yati (`అ`) and Hal Yati (`శ`, `వ`)**, while flagging the vowel match as a poetically licensed anomaly.

---

### Provenance Trail

* **Pāṇinian & Sanskrit Grammatical Authorities:**  
* *Pāṇini Aṣṭādhyāyī:* Sūtra 6-3-97 (*'ద్వ్యంతరుపసర్గేభ్యో ప ఈత్'* for *dvīpa, antarīpa, pratīpa, samīpa*); Sūtra 6-3-130 (*'మిత్రేచర్షా'* for *viśvāmitra*).  
* *Kātyāyana Vārtika:* *'అక్షాదూహిన్యాముపసంఖ్యానమ్'* (governing vṛddhi in *akṣauhiṇi*).  
* *Siddhānta Kaumudī* & *Tattvabodhinī* (Chelapilla Venkata Sastri's defense of *akṣōhiṇi* via *akṣa \+ ūhin \+ ṅīp*).  
* *Amarakośamu*: Canonical semantic definitions (*Samau siddhānta rāddhāntau*, *Vātāyanaṁ gavākṣaḥ*, *Dvīpō'stryāmarṇavāntardvīpaḥ*).  
* **Prosodic Treatises & Commentaries:**  
* *Appakavīyamu* (Kāṇḍa 3: 138–186): Foundation verses and groupings for Nitya Samāsa, \-anta, \-ayana, \-aṇḍa, and Viśvāmitra.  
* *Chandōdarpaṇamu* (Ananta Mātya, Ullāsa 1-99): Benchmark lakṣya verse for *Rasāyana*.  
* *Kāvyālaṅkāra Cūḍāmaṇi* (Vinnakōta Peddana, 7-68): Quadruple demonstration verse for *Anyōnya*.  
* *Lakshaṇa Sāra Saṅgrahamu* (2-267–295): Primary source verifying *Gavākṣa*, *Sāṅga*, *Sādara*, and *Viśvāmitra* variants.  
* *Sarvalakshaṇa Sāra Saṅgrahamu* and *Sulakshaṇa Sāramu* (validating *akṣauhiṇi / akṣōhiṇi*).  
* *Rangarāṭ Chandamu* (Ranga Kavi, 3-220): Illustrative verse for *Dvīpa*.  
* **Classical Telugu Kāvya Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (6-302) *dvāra*, (8-74) *ēkānta*, (4-169) *sāṅga*, (7-95) *viśvāmitra*.  
* *Sabhā Parva:* (1-73) *karṇāṭa*, (2-238) *vātāyana*.  
* *Vana (Āraṇya) Parva:* (5-120) *ēkānta*, (4-182) *mārtāṇḍa*.  
* *Virāṭa Parva:* (2-97) *sādara*, Atharvaṇācārya Virāṭa verses (3-141, 3-142) *vanaukas*.  
* *Udyōga Parva:* (2-44) *udāra*.  
* *Śānti Parva:* (5-54) *vṛttānta*, (5-100) *ajāṇḍa*, (5-148) *padārtha*, (5-154) *siddhānta*, (6-503) *ēkānta*.  
* *Anuśāsanika Parva:* (5-23, 5-297, 5-438) *parāyaṇa*, (5-326) *ēkānta*, (5-499) *padārtha*.  
* *Mauśala Parva:* (207) *ēkānta*.  
* *Mahāprasthānika Parva:* (4) *vṛttānta*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (1-372) *śuddhānta*, (3-202) *brahmāṇḍa*, (7-132) *bādarāyaṇa*, (7-136) *svānta*, (7-218) *ēkānta*, (8-571) *brahmāṇḍa*, (9-617) *viśvāmitra*.  
* *Ranganātha Rāmāyaṇamu*: Bāla Kāṇḍa (pages 40, 51, 60, 64, 75\) for *rasāyana* and *viśvāmitra*.  
* *Bhāskara Rāmāyaṇamu*: Sundara (305) *dvīpa*, Bāla (639, 690\) *svānta* and *viśvāmitra*, Yuddha (708) *anyōnya*.  
* *Kāśīkhaṇḍamu* (Śrīnātha): (2-111) *śuddhānta*, (3-141) *karṇāṭa*, (5-319) *ēkānta*.  
* *Haravilāsamu* (Śrīnātha): (1-15) *karṇāṭa*, (3-6) *mārtāṇḍa*.  
* *Kalaāpūrṇōdayamu* (Piṅgaḷi Sūrana): (2-18) *śuddhānta*, (2-70) *viśvāmitra*.  
* *Rāmacaritamānasa / Rāmābhyudayamu / Rāmāyaṇakalpavṛkṣamu*: Cited for *gavākṣa*, *samīpa*, and *sādara*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Nitya Samāsa Yati (Part 2: Proper Names, Nañ-Samāsa, Kyaj-Pratyaya Guardrails, and Upasarga-Sandhi)** extends the Ubhaya Yati (ఉభయయతి) engine to divine compound proper nouns, negative prefix compounds, and reverse prefix sandhis, while imposing a strict ban on denominative suffix lengthenings.

---

### Core Engine Mechanics

* **Dual-Track Target Resolution (ఉభయయతి):** At qualified sandhi junctures, the engine exposes both the base vowel target set (**అచ్చు యతి**) and the consonant target set (**హల్లు యతి**).  
* **Nañ-Samāsa Dichotomy:**  
* If the negative particle *nañ* (నఞ్) attaches to a **consonant-initial (halādi)** stem, *nañ* reduces to `అ-` (e.g., *na \+ bhāva \= abhāva*). Because no vowel-sandhi junction is formed, **Ubhaya Yati is strictly disabled** (evaluated only as ordinary single-letter Svara or Hal Yati).  
* If *nañ* attaches to a **vowel-initial (ajādi)** stem, *nañ* converts to `అన్-` (e.g., *an \+ anta \= ananta*). The resulting syllable (`న / నా / ని / నీ / ను / నూ / నె / నే`) fuses the negative particle to the base root, **licensing Ubhaya Yati**.  
* **Kyaj-Pratyayānta Prohibition (Negative Guardrail):** Secondary suffixation using *kyac* (*\-yita, \-yamāna, \-yiṣyamāṇa*) lengthens the stem-final vowel morphologically (e.g., *kumāra \+ yita $\\to$ kumārāyita*). Because this lengthening is not a sandhi fusion with an independent ajādi root (i.e., it is not *kumāra \+ āyata*), **vowel matching is prohibited; only consonant (Hal) yati is licensed**.  
* **Upasarga-Sandhi Yati vs. Prādi Yati Distinction:**  
* **Prādi Yati:** $\\text{\[Ajādi/Any Upasarga\]} \+ \\text{\[Ajādi Stem\]}$ (e.g., *pra \+ aṅgaṇa \= prāṅgaṇa*).  
* **Upasarga-Sandhi Yati:** $\\text{\[Noun/Base Stem\]} \+ \\text{\[Ajādi Upasarga\]}$ (e.g., *vasudhā \+ adhipa \= vasudhādhipa*).

---

### Lexical & Morphological Mapping Table

| Compound Category | Representative Tokens | Fused Juncture | Vowel Candidate Set (అచ్చు యతి) | Consonant Candidate Set (హల్లు యతి) | Engine Rule & Behavior |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **నిత్యసమాస నామములు (Deity & Proper Names)**&nbsp; | నారాయణ (Nārāyaṇa) |  |  |  |  |

| **రా**

 | `అ`

 | `ర` (రా / ర via Ekantara)

| Underlying *nāra \+ ayana*; valid for deities and mortals alike.

| |  | జనార్దన (Janārdana)

| **నా**

 | `అ` (Svara/Sarasa with `య`)

| `న` (నా / న via Prāṇi)

| Underlying *jana \+ ardana*; valid for Kṛṣṇa or historical persons.

| |  | దామోదర (Dāmōdara)

| **మో**

 | `ఉ` (Svara with `ఉ`, Sarasa with `యు`)

| `మ` (మో / మొ via Prāṇi)

| Guṇa sandhi (*dāma \+ udara*); targets base vowel `ఉ` or consonant `మ`.

| |  | సాంబ (Sāmba)

| **సాం**

 | `అ`

 | `స` (సా via Prāṇi, జా via Sarasa)

| Underlying *sa \+ ambā*; applies to Śiva or Kṛṣṇa's son Sāmba.

| |  | మురారి, పురారి, లంబోదర

| **రా / మో**

 | `అ` / `ఉ`

 | `ర` / `మ`

 | Underlying *mura/pura \+ ari*, *lamba \+ udara*.

| |  | మందార, నారికేళ (నాళికేర)

| **దా / కే**

 | `అ` / `ఈ`

 | `ద` / `క`

 | *manda \+ ara*, *nārika \+ īḷa*; Ubhaya yati licensed per Appakavi.

| | **నఞ్ సమాసములు (Negative Compounds)**

 | అనంత, అనన్య, అనర్గళ, అనర్ఘ, అనర్హ

| **న / నం**

 | `అ` (Svara/Sarasa with `య`, `హ`)

| `న` (Prāṇi `న`, Bindu `ంత`, Sarasa `ణ`)

| *an \+ anta/anya/argaḷa/argha/arha*; fused `న` exposes base vowel `అ` or consonant `న`.

| |  | అనారత (Anārata)

| **నా**

 | `ఆ`

 | `న` (నా via Prāṇi, ణ via Sarasa)

| *an \+ ārata*; exposes long `ఆ` or consonant `న`.

| |  | అనూన (Anūna)

| **నూ**

 | `ఊ` (Svara with `ఉ`, `ఓ`)

| `న` (ను via Prāṇi, ండో via Anunāsika)

| *an \+ ūna*; exposes root `ఊ` or consonant `న`.

| |  | అనేక, అనేకప (Anēka, Anēkapa)

| **నే**

 | `ఏ` (Svara with `ఇ`, `ఈ`, `ఎ`)

| `న` (ని / నే via Prāṇi)

| *an \+ ēka*; exposes root `ఏ` or consonant `న`.

| | **నఞ్ అపవాదములు (Pāṇinian Nañ Invariables)**

 | నాక (Nāka \= Heaven)

| **నా**

 | `అ` (Svara with `అ`, `ఐ`, Sarasa with `హ`)

| `న` (న / నా via Prāṇi)

| Pāṇini 6-3-75 retains `న`: *na \+ aka $\\to$ nāka*; licenses base `అ` or `న`.

| |  | నాసత్య (Nāsatya \= Aśvins)

| **నా**

 | `ఆ`

 | `న` (నా)

| Pāṇini 6-3-75 retains `న`: *na \+ asatya $\\to$ nāsatya*; licenses `ఆ` or `న`.

| |  | నాస్తి (Nāsti)

| **నా**

 | `అ`

 | `న` (Bindu with `సం`)

| *na \+ asti*; single-word appearance licenses base `అ` or consonant `న`.

| |  | నైక (Naika \= Many)

| **నై**

 | `ఏ`

 | `న` (నై via Prāṇi with `న`)

| Vṛddhi fusion *na \+ ēka*; licenses base `ఏ` or consonant `న`.

| | **క్యజ్ ప్రత్యయాంతములు (Denominative Suffixes)**

 | కుమారాయిత, ఇంద్రాయిత, భద్రాయిత, భృంగాయిత, శబ్దాయమాన, మూర్ఖాయిష్యమాణ

| **రా / ద్రా / గా / బ్దా**

 | **DISQUALIFIED** (Matching vowel `ఆ` is illegal)

| **Consonants ONLY** (`ర`, `ద`, `గ`, `బ` via Prāṇi/Vargaja/Ekantara)

| Suffixes *\-yita*, *\-yamāna*, *\-yiṣyamāṇa* induce lengthening without vowel sandhi; strictly consonant matching.

| | **ఉపసర్గ సంధి (Reverse Prefix Sandhi)**

 | వసుధాధిప, వృషభాధిప, లోకాధిప, సురగణాధిప, రమాధిప

| **ధా / భా / ణా / మా**

 | `అ` (matches `అ`, `ఆ`, Sarasa `య`, `హ`)

| **Sandhi Consonant** (`ధా`, `భా`, `మా` via Prāṇi/Vargaja)

| Compound member fusions with ajādi prefix **అధి** (*adhi-pa*); licenses base prefix vowel `అ` or consonant.

| |  | యాత్రాభివృద్ధి (Yātrābhivṛddhi)

| **త్రా**

 | `అ`

 | `త` (త్ర via Vargaja with `ద`)

| Fusion with ajādi prefix **అభి** (*abhi-vṛddhi*).

|

---

### Special Engine Constraints & Guardrails

* **The Deity vs. Human Anthroponym Gate:**  
* In Nannaya's *Mahābhāratamu* (Ādi 1-25), line 2 pairs *Nārāyaṇunaṭlu* (referring to Kṛṣṇa) with vowel yati `అ-అ`, while line 3 pairs *Nārāyaṇabhaṭṭu* (a human companion) with consonant yati `రా-ర`.  
* *Engine Verdict:* Although early commentators theorized that etymological decomposition (*nāra \+ ayana*) is valid only for the deity and invalid for human namesakes, usage confirms that proper nouns borrowed from divine epithets carry their structural Nitya Samāsa status into human naming. Thus, both vowel and consonant yati are licensed for *Nārāyaṇa, Janārdana,* etc., regardless of human or divine referent.  
* **Halādi Nañ Disqualification:**  
* When *nañ* precedes a consonant (e.g., *a-kārya, a-vinaya, a-dharma*), the initial `అ-` is an ordinary short vowel. The engine must **reject Ubhaya Yati** here; it matches purely through regular Svara Yati (`అ`) without granting access to the stem consonant.  
* **Sanskrit-Only Boundary on Upasarga-Sandhi:**  
* Upasarga-Sandhi Yati requires a genuine **Sanskrit Sandhi**.  
* If an ajādi prefix combines via Telugu Sandhi (e.g., *ataḍu \+ adhipati $\\to$ ataḍadhipati* via Telugu Utva Sandhi), **Ubhaya Yati is disabled**. The syllable `డ` cannot match as a consonant; it must be resolved strictly as Svara-pradhāna Yati targeting the base initial vowel `అ`.  
* **The Viśvāmitra Resolution:**  
* Pāṇini sūtra *Mitrē carṣau* (6-3-130) establishes that the lengthening in *Viśvāmitra* is an elongation of the vowel of *viśva*, not sandhi with *amitra* ("enemy").  
* *Engine Rule:* Commentators strongly condemn Acchu yati on *Viśvāmitra* as ungrammatical. Consonant yati on `శా` or `వా` is the standard rule, while vowel yati on `అ` is restricted to permissive emulation of classical poetic deviance (*pramāda prayōga*).

---

### Provenance Trail

* **Pāṇinian Grammatical Authorities:**  
* *Aṣṭādhyāyī 6-3-75:* *'నభ్రాణ్ణపాన్నవేదా నాసత్యా నముచి నకుల నఖ నపుంసక నక్షత్ర నక్ర నాకేషు ప్రకృత్యా'* (preserving initial *na* in *nāka* and *nāsatya*).  
* *Aṣṭādhyāyī 6-3-130:* *'మిత్రేచర్షా'* (elongation of *viśva* before *mitra*).  
* Sanskrit lexicons: *Amarakośamu* (*Svarvaidyāvaśvinīsutau nāsatyāvaśvinau...*).  
* Telugu grammars: *Prauḍha Vyākaraṇamu* (Śabda-92, Samāsa-22 cited for numeral declensions like *padunenamaṇḍru* in *anēkapa* analysis).  
* **Prosodic Treatises & Commentaries:**  
* *Appakavīyamu* (Kāṇḍa 3: 146–188): Source for Nañ compounds (*anēka* 3-150–153, *janārdana* 3-156–157, *nāka* 3-158–160, *nāsti* 3-146–147, *upasarga-sandhi* 3-183–184, and *kyac* prohibitions 3-187–188).  
* *Kāvyālaṅkāra Cūḍāmaṇi* (Vinnakōta Peddana, 7-66): Benchmark verse demonstrating dual vowel/consonant yati in *nāka*.  
* *Lakshaṇa Sāra Saṅgrahamu*: Citations for *sādara*, *nāka*, and *upasarga-sandhi*.  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-25) *nārāyaṇa*, (1-6) *ananta*, (2-24) *nāka*, (2-203, 2-214) *adhipa*, (3-161) *anēka*, (4-185) *ananta*, (5-6) *kumārāyita*, (7-372) *nārāyaṇa*, (8-71) *anārata*, (8-141) *ananya*.  
* *Sabhā Parva:* (1-44) *anūna*, (2-18) *dāmōdara*, (2-162) *anargha*.  
* *Vana (Āraṇya) Parva:* (4-160) *anargaḷa*, (5-105) *ananya*, (5-193) *ananta*.  
* *Virāṭa Parva:* (1-1) *bhadrāyita*.  
* *Udyōga Parva:* (1-92) *indrāyita*, (1-159) *sāmba*.  
* *Karṇa Parva:* (2-355) *anēka*.  
* *Śānti Parva:* (1-68) *ananta*, (1-170) *anarha*, (5-46) *adhipa*, (6-531) *nārāyaṇa*.  
* *Mauśala Parva:* (9, 61\) *sāmba*.  
* *Svargārōhaṇa Parva:* (71) *ananta*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (1-125, 4-149) *janārdana*, (1-136) *nāka*, (2-209) *ananta*, (4-30, 6-7) *sāmba*, (4-194) *bhadrāyita*, (5-75) *anārata*, (7-158) *ananta*, (8-170) *anūna*, (10-4-159) *nāka*.  
* *Āmuktamālyada* (Śrī Krishṇadēvarāya): (1-35) *anēkapa*.  
* *Candrabhānu Caritramu*: (1-66) *vṛṣabhādhipa*.  
* *Uttararāmāyaṇamu*: (5-30) *anūna*.  
* *Ghaṭikācala Māhātmyamu*: (Avatārika-3) *anūna*.  
* *Vēṅkaṭēśvara Śatakamu*: (1) *bhṛṅgāyita*.  
* *Śṛṅgāra Śākuntalamu*: (1-84) *nāsti*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Dēśya Nitya Samāsa Yati, Nāmākhaṇḍa Yati, Rāgama Sandhi Yati, and Prāsa Yati** establish the dual-target (Ubhaya Yati) matching logic for native Telugu compounds, personal names, and augment junctures, while defining the substitution mechanics of secondary rhyme matching (Prāsa Yati) across specific metres.

---

### Dēśya Nitya Samāsa Yati (దేశ్య నిత్యసమాస యతులు)

When native Telugu words (*dēśyamulu*) undergo vowel sandhi and appear as fused, indivisible single-word units (*ēkapadavat*), the resulting sandhi-junction syllable is licensed for **Ubhaya Yati (ఉభయయతి)**: matching either via its constituent vowel (**అచ్చు యతి**) or via its consonant (**హల్లు యతి**).

| Compound Class | Sample Tokens | Juncture Syllable | Vowel Candidate Set (అచ్చు యతి) | Consonant Candidate Set (హల్లు యతి) | Engine Rule & Behavior |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **అఱు ధాతువు (Root *aṟu* \= to perish)**&nbsp; | ఉక్కఱు, క్రచ్చఱు, పెంపఱు, పెల్లఱు, చూపఱు |  |  |  |  |

| **క్క / చ్చే / ప**

 | `అ`

 | `క`, `చ`, `ప`

 | Base verb *aṟu* is non-independent; sandhi junction splits into vowel `అ` or root-final consonant.

| | **ఆరు ధాతువు (Root *āru* \= to abound/fill)**

 | ఏపారు, సొంపారు, అలరారు, ఒప్పారు, కన్నారు, పెంపారు

| **పా / రా**

 | `ఆ`

 | `ప`, `ర`

 | Base verb *āru* forms intensive verbs; junction splits into vowel `ఆ` or consonant.

| | **ఇఱియు ధాతువు (Root *iṟiyu* \= to become tight)**

 | క్రిక్కిఱియు (క్రిక్కిఱిసి, క్రిక్కిఱియన్)

| **క్కి**

 | `ఇ`

 | `క` (క్కి via Vargaja with `గ`, `గీ`)

| Fused stem *krikku \+ iṟiyu*; licenses base vowel `ఇ` or consonant `క`.

| | **ఒకొండు / సంఖ్యావాచకములు (Numeral compounds)**

 | ఒకొండు, ఒక్కొండు, పదునొకొండు, పదునొక్కొండు

| **కొం / క్కొం**

 | `ఒ` (matches `ఒ`, `ఉ`)

| `క` (కొ via Prāṇi with `కొ`, `కు`)

| Evaluates oblique forms (*okoṇṭiki*, *padunokoṇṭiki*) equally.

| | **స్థిర ప్రయోగార్థకములు (Fixed Lexical Idioms)**

 | ఇల్లాలు, ఓలమాసగొను, కూర్చుండు, గ్రక్కన, బోరన

| **ల్లా / మా / ర్చు / క్క / ర**

 | `ఆ`, `ఉ`, `అ`

 | `ల`, `మ`, `ర`/`చ`, `క`, `ర`

 | Sandhi junctures (*illu \+ ālu*, *kūrucu \+ uṇḍu*, etc.) expose dual targets.

| | **అది/అవి అత్వసంధి రూపములు (Participles with *adi/avi*)**

 | ఉన్నది, ఉన్నవి, కన్నది, చెప్పినవి, పిన్నది

| **న్న / న**

 | `అ`

 | `న` (Prāṇi `న`, Bindu `ంత`)

| Sandhied forms license dual matching; unsandhied forms (*unnayadi*) permit only Acchu Yati.

|

* **Atva Sandhi Negative Disqualification Guardrail:**  
* Ubhaya Yati is **strictly restricted to *adi* and *avi* fusions**.  
* All other regular Atva Sandhi formations—such as *unnapuḍu* (*unna \+ apuḍu*), *ācarinciñaṭṭi* (*ācarincina \+ aṭṭi*), *vinnanta* (*vinna \+ anta*), and *kannanta* (*kanna \+ anta*)—are **disqualified from Ubhaya Yati**. The engine must restrict them strictly to Svara-pradhāna Yati matching the base initial vowel `అ`; matching consonant `న` is forbidden.  
* **Numeral Boundary Exclusion:**  
* Forms without internal vowel sandhi (*okaḍu, okaṇḍu, okkaḍu, okkaṇḍu*) do not form sandhi junctures and are **disqualified from Ubhaya Yati**.

---

### Nāmākhaṇḍa / Prabhu Yati (నామాఖండ యతులు)

Governs Telugu proper personal names (*vyakti-pērlu*) where a Sanskrit or Telugu nominal base fuses with honorific/kinship suffixes (*śrēṣṭhatā-vācakamulu*) via obligatory sandhi (*Prauḍha Vyākaraṇamu*, Sandhi-1).

$$\\text{Prakṛti / Nominal Base} \+ {\\text{అయ్య, అమ్మ, అన్న, అక్క, అప్ప, అరుసు, ఆయి}} \\implies \\text{Ubhaya Yati at Juncture}$$

* **Valid Suffix Nodes:**  
* Geminate forms: *ayya, amma, anna, akka, appa*.  
* Degeminate variants (*dvitva-rahita*): *aya, ama, ana, apa*.  
* Regional/feudal titles: *arusu* (king/lord) and *āyi* (mother/lady).  
* **Target Mapping:**  
* **అక్క (Akka):** *Ambakka* (*amba \+ akka*) $\\to$ `బ` matches vowel `అ` or consonant `బ` (Vargaja with `భ`).  
* **అన్న / అన (Anna / Ana):** *Nārana*, *Kēsana*, *Kommana*, *Cinnanna*, *Māmiḍanna*, *Peddanna*, *Narasiṅganna*, *Vallabhanna* $\\to$ juncture syllable matches vowel `అ` or base consonant (`ర`, `స`, `మ`, `న`, `డ`, `ద`, `గ`, `భ`).  
* **అప్ప (Appa):** *Veṅkappa*, *Mārappa* $\\to$ matches vowel `అ` or consonant `క` / `ర`.  
* **అమ్మ / అమ (Amma / Ama):** *Sītamma*, *Sītama*, *Annama* $\\to$ matches vowel `అ` or consonant `త` (Vargaja with `ద`) / `న`.  
* **అయ్య / అయ (Ayya / Aya):** *Rāmayya*, *Rāmaya*, *Vīrabhaddrayya*, *Liṅgayya*, *Rāmānujayya*, *Tirumalayya* $\\to$ matches vowel `అ` or base consonant (`మ`, `ద`/`ర`, `గ`, `జ`, `ల`).  
* **అరుసు (Arusu):** *Kōnamarusu*, *Bācamarusu*, *Timmarusu* $\\to$ `మ` matches vowel `అ` or consonant `మ`.  
* **ఆయి (Āyi):** *Gaṅgāyi*, *Sītāyi* $\\to$ matches vowel `ఆ` or base consonant `గ` / `త`.  
* **Dispute Resolution (Ananta vs. Appakavi):** Ananta (*Chandōdarpaṇamu*) claimed that Prabhu Nāmānta Viramaṇamu applies only to ungeminated stems (*aya, ama*). Appakavi proved through extensive usage that both geminated (*ayya, amma*) and ungeminated forms are equally valid. The engine must accept both configurations.

---

### Rāgama Sandhi Yati (రాగమ సంధి యతి)

Applies to Karmadhāraya compounds where the feminine noun **ఆలు (ālu)** attaches to qualitative stems, triggering *rugāgama* (*Bāla Vyākaraṇamu*, Sandhi-30, 31):

$$\\text{Stem} \+ \\text{ర్ (Rugāgama)} \+ \\text{ఆలు} \\implies \\text{Juncture Syllable is strictly } \\mathbf{\\sigma}^{\\circ} \\ (\\text{rā})$$

* **Eligible Lexical Stems:**  
* Native Telugu bases: *pēdarālu*, *muddarālu*, *bālentarālu*, *bīdarālu*, *komarālu*, *ayiduvarālu*, *manumarālu*, *goḍḍurālu*.  
* Sanskrit Tatsama bases: *dhīrurālu*, *dharmātmurālu*, *priyurālu*, *dayāvihīnurālu*, *guṇavanturālu*.  
* Irregular substitution: *javvani \+ ālu* undergoes *jēva*\-ādēśa $\\to$ *jēvarālu* (plural: *jēvarāṇḍru*).  
* **Dual Target Execution at `రా`:**  
* **Acchu Yati:** Matches underlying/resultant vowel `ఆ` via Svara Yati (e.g., matching `అ`, `ఆ`, or Sarasa `యా`).  
* **Hal Yati:** Matches consonant `ర` (rēpha) via Ekantara Yati.

---

### Pañcamī Vibhakti Yati — Engine Disqualification (నిషేధ విధి)

Appakavi asserted that fifth-case postpositions **కంటెన్ (kaṇṭen)** and **కన్నన్ (kannan)** split artificially (*rāmuniki \+ aṇṭen / annan*) to allow Ubhaya Yati on `క` (vowel `అ` or consonant `క`).

* **Grammatical Evaluation:**  
* *Kanna* is an informal vernacular marker, not an acknowledged vibhakti suffix.  
* Splitting *kaṇṭen* into *ki \+ aṇṭen* is ungrammatical (*vyākaraṇa asādhyamu*).  
* No classical poet outside of a solitary instance in *Camatkāra Rāmāyaṇamu* (treated as *kavi-prāmādikamu*) validates vowel matching on *kannan* / *kaṇṭen*.  
* **Engine Rule:** **Ubhaya Yati is rejected on 5th vibhakti suffixes**. In tokens like *rāmunikaṇṭen*, *rāmunikannan*, *vānikaṇṭen*, and *vānikannan*, the parser must evaluate `క` **strictly as standard Hal Yati (`క`)**; vowel extraction (`అ`) is disabled.

---

### Prāsa Yati Engine Architecture (ప్రాసయతి)

Prāsa Yati substitutes the primary yati check by shifting rhyme verification to the **second akṣara of the line (or hemistich)** and the **akṣara immediately following the designated yati position**.

Line Layout:

Index:          1              2         ...        Y               Y+1        ...

Element:    \[Pādādi\]       \[Prāsa 1\]            \[Yati-Sthāna\]   \[Prāsa 2\]

                │              │                      │             │

                └── NO MATCH ──┘                      └── NO MATCH ─┘

                (Yati Failure)                        (Yati Failure)

                               │                                    │

                               └───────── MUST MATCH ───────────────┘

                                     (Strict Prāsa Rules)

&nbsp;

**Permitted Metres Engine Gate** Prāsa Yati is strictly prohibited in major Sanskrit vṛttas (Utpalamāla, Campakamāla, Śārdūlamu, Mattēbhamu) and Kanda. It is legal only in the following metres:

* **Upajātis:** *Sīsamu*, *Tēṭagīti*, *Āṭaveladi*.  
* **Special Vṛttas:** *Sarasijamu*, *Krauñcapadamu*.  
* **Mālikā Vṛttas:** *Layagrāhi*, *Layavibhāti*, *Layahāri*, *Tribhaṅgi*.

**Mandatory Prāsa-Pūrvākṣara Invariant (ప్రాసపూర్వాక్షర నియమము)** The akṣara preceding Prāsa 1 (i.e., Position 1\) and the akṣara preceding Prāsa 2 (i.e., the Yati-sthāna syllable) **must have identical metrical weight**:

* $\\text{Weight}(\\text{Position 1}) \== \\text{Weight}(\\text{Yati-Sthāna}) \\in {\\text{Laghu}, \\text{Guru}}$.  
* An alignment between a Laghu-preceded Prāsa and a Guru-preceded Prāsa is a fatal engine failure.

**Matching Constraints & Independence**

* **Consonantal Match Only:** The vowels attached to Prāsa 1 and Prāsa 2 are irrelevant (e.g., `లు - ల`, `ద - దు`, `ని - నో` are valid matches).  
* **Weight Independence of Rhyme Syllables:** Prāsa 1 and Prāsa 2 themselves do not need to share metrical weight; one may be Guru and the other Laghu as permitted by the metre's gaṇa structure.  
* **Hemistich & Line Autonomy:** In Sīsamu (8 yati nodes) and Gīti metres, each line or hemistich is completely autonomous. A poet may mix standard Yati and Prāsa Yati in the same verse, and adjacent Prāsa Yatis may target entirely different consonants.  
* **Dental/Palatal Equivalence:** Dental and palatal *ca/ja* variants (`చ/చే`, `జ/జే`) function as valid Sama Prāsa matches under Bālasarasvati / Bāla Vyākaraṇamu conventions (*dantya-tālavyambulaina ca-ja-lu savarṇambulu*).

---

### Provenance Trail

* **Grammatical Treatises & Sūtras:**  
* *Bāla Vyākaraṇamu* (Paravastu Cinnaya Sūri):  
* Sandhi-30: *Pēdādi śabdaṁbulak-āluśabdamu paraṁbagunapuḍu karmadhārayaṁbunandu rugāgamambagu*.  
* Sandhi-31: *Karmadhārayaṁbunam tatsamaṁbulak-āluśabdamu paraṁbagunapuḍatvaṁbunakutvaṁbunu rugāgamambunagu*.  
* Saṁjñā-7: Dental/palatal identity for *ca* and *ja*.  
* *Prauḍha Vyākaraṇamu* (Bahujanapalli Sītārāmācāryulu):  
* Sandhi-1: *Śrēṣṭhatā-vācakamulagun-āryāmbādyarthaka śabdaṁbulu paraṁbagucō nanni yacculaku sandhi nityamu* (governing Nāmākhaṇḍa Yati).  
* Samāsa-22: Numeral augment rules for *padunokoṇḍu*.  
* *Sūryarāyāndhra Nighaṇṭuvu*: Derivational analysis of *okoṇḍu* (*oka \+ oṇḍu*).  
* **Prosodic Treatises:**  
* *Appakavīyamu* (Kāṇḍa 3):  
* Verses 194–201: Dēśya compounds in *\-aṟu* (*ukkaṟu, kraccaṟu, pempaṟu*).  
* Verse 211: Numeral compounds (*padunokoṇṭiki*).  
* Verses 215–217: *Rāgamasandhi Vaḷi* (*jēvarālu, balentarālu, muddarālu*).  
* Verses 222–237: *Nāmākhaṇḍa Vaḷulu* (*Venkanna, Sītamma, Rāmānuja, Bācamarusu, Sītāyi*).  
* Verses 239–240: *Pañcamī Vibhakti Virāmamu* (critiqued and rejected).  
* *Chandōdarpaṇamu* (Anantāmātya, 1-120): Definition of *Prabhu-nāmānta Viramaṇamu*.  
* *Lakṣaṇasāra Saṅgrahamu* (Citrakavi Peddana): Benchmark lakṣya verses for *kraccaṟan* and *krikkiṟisen*.  
* **Classical Telugu Kāvya Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-9) *lōkajñu*, (2-224) *yajakōttamula*, (3-156) *vāriva*, (5-166) *vaḍi*, (5-207) *rācē*, (6-267) *ēnēmi*, (8-125) *rājavaṁśa*.  
* *Sabhā Parva:* (1-186) *munnahitamu*, (1-215) *pūjituṇḍayi*, (2-53) *vīninorulu*, (2-302) *bhūrēṇu*.  
* *Vana (Āraṇya) Parva:* (1-188) *śastramul*, (2-29) *bōrana*, (6-345) *ukkaṟa*, (7-367) *kraccaṟa*.  
* *Virāṭa Parva:* (1-10) *kommana*, (1-12) *harinīla*, (3-216) *krikkiṟiyaga*, (5-143) *sēnalukkaṟa*, (5-204) *jūdamu*.  
* *Udyōga Parva:* (2-66) *vinumu*.  
* *Strī Parva:* (2-74) *vadana-kamalamandanda*.  
* *Śānti Parva:* (1-126) *ceppinavi*.  
* *Anuśāsanika Parva:* (1-68) *ōlamāsagonaka*.  
* *Svargārōhaṇa Parva:* (5) *nikhila*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (1-177) *vaccucunnadi*, (10-uttara-342) *bālamātruṇḍu*, (10-4-575) *ēpāragan*, (10-4-1271) *kūrcuṇḍu*.  
* *Manucaritramu* (Allasāni Peddana): (1-5) *nalluvāṟāṇi*, (2-43) *sāmu*, (2-94) *teṟagulella*.  
* *Ranganātha Rāmāyaṇamu* & *Bhāskara Rāmāyaṇamu*: Bāla (139, 184, 369, 756), Yuddha (650, 783).  
* *Śrīnātha Chatuvulu* & *Kāśīkhaṇḍamu*: (1-13) *vīrabhadrayya*, (4-97) *ōlamāsagoniye*.

&nbsp;

&nbsp;

&nbsp;

**Prāsa Yati (ప్రాసయతి — Part 2\)** extends the substitution mechanics of Yati to incorporate the entire spectrum of rhyming classifications established in classical prosody. In permitted metres (Sīsamu, Tēṭagīti, Āṭaveladi, and designated vṛttas), whenever a verse line foregoes head-syllable Yati, the engine verifies that the second syllable of the line (**Prāsa 1**) and the syllable immediately following the Yati position (**Prāsa 2**) satisfy both consonantal rhyme matching and strict metrical weight parity in their preceding syllables (**Prāsa-Pūrvākṣara Niyama**).

---

### Core Prāsa Yati Typology & Verification Rules

| Prāsa Yati Category | Engine Rhyme Condition | Phonetic / Structural Match Pairs | Weight Constraint on Preceding Syllable | Verification Status & Engine Behavior |
| :---- | :---- | :---- | :---- | :---- |
| **Sama Prāsa (సమప్రాసము)**&nbsp; | Consonants must be phonetically identical. |  |  |  |

| Matches across all stops, sonorants, and sibilants (`ఢ-ఢ`, `ణ-ణ`, `త-త`, `థ-థ`, `ద-ద`, `ధ-ధ`, `న-న`, `ప-ప`, `బ-బ`, `భ-భ`, `మ-మ`, `య-య`, `ర-ర`, `ఱ-ఱ`, `ల-ల`, `ళ-ళ`, `వ-వ`, `శ-శ`, `ష-ష`, `స-స`, `హ-హ`).

| Must be uniformly Guru or uniformly Laghu.

| **Canonical**: Standard rhyme validation; vowels on consonants are ignored.

| | **Ṛtva-sahita Prāsa (ఋత్వసహిత ప్రాసము)**

 | Consonant fused with vocalic `ఋ` matches the same consonant with any other vowel.

| `క - కృ`, `గి - గృ`, `తృ - త`, `న - నృ`, `మ - మృ`.

| Preceding syllable must maintain weight parity.

| **Canonical**: Treated as pure Sama Prāsa; vocalic `ఋ` does not break consonantal identity.

| | **Pūrṇa-bindu Prāsa (పూర్ణబిందు ప్రాసము)**

 | Rhyming consonants must both be preceded by a full anusvāra (Pūrṇa-bindu).

| `ంక - ంక`, `ంగ - ంగు`, `ంచ - ంచ`, `ంజ - ంజే`, `ంఠ - ంఠి`, `ండ - ండు`, `ంత - ంత`, `ంద - ంద`, `ంధ - ంధ`, `ంబ - ంబ`, `ంభ - ంభ`.

| Preceding syllables are inherently **Guru** due to the anusvāra.

| **Canonical**: Both sides must contain an anusvāra; a single-sided bindu causes immediate failure.

| | **Saṁyuktākṣara & Dvitva Prāsa (సంయుక్తాక్షర ప్రాసము)**

 | Identical conjunct clusters or geminates in identical consonant sequence.

| Geminates: `క్క`, `గ్గ`, `చ్చ`, `జ్జ`, `ట్ట`, `డ్డ`, `త్త`, `ద్ద`, `న్న`, `ప్ప`, `బ్బ`, `మ్మ`, `య్య`, `ఱ్ఱ`, `ల్ల`, `ళ్ళ`, `వ్వ`. Clusters: `క్య`, `క్ష`, `గ్ర`, `డ్క`, `త్క`, `త్న`, `త్య`, `త్స`, `ద్ధ`, `ధ్య`, `ప్ర`, `ర్గ`, `ర్ఘ`, `ర్చ`, `ర్జ`, `ర్ణ`, `ర్త`, `ర్ద`, `ర్భ`, `ర్మ`, `ర్య`, `ర్వ`, `వ్య`, `శ్వ`, `ష్ట`, `ష్ఠ`, `ష్ణ`, `స్త`.

| Preceding syllables are inherently **Guru** before conjuncts.

| **Canonical**: Order of consonants within the cluster must match identically. Clustering with `ఋ` (e.g., `ర్ఘ` vs `ర్ఘృ`) remains valid.

| | **Ardha-bindu Prāsa (అర్ధబిందు ప్రాసము)**

 | Both rhyming consonants must be preceded by an arasunna (half-nasal).

| `ఁకు - ఁక`, `ఁగి - ఁగ`, `ఁటి - ఁటు`, `ఁడు - ఁడె`, `ఁత - ఁత`, `ఁద - ఁది`.

| Preceding syllables must share identical metrical weight.

| **Canonical**: Confined to native Telugu lexical forms containing natural historical nasals.

| | **Khaṇḍākhaṇḍa Prāsa (ఖండాఖండ ప్రాసము)**

 | An ardhabindu-preceded consonant matches an uninflected/plain consonant.

| `ఁక - క`, `గ - ఁగు`, `టె - ఁట`, `ఁజి - జె`, `ఁది - ది`.

| Preceding syllables must share identical metrical weight.

| **Canonical**: Asymmetric half-nasal allowance licensed across classical poetry.

| | **Laghu Ya-kāra Prāsa (లఘు 'య'కార ప్రాసము)**

 | Euphonic glide (yaḍāgama `య`) matches inherent root semi-vowel (alaghu `య`).

| `య్+అ - య`, `య్+ఒ - య`, `య్+ఆ - య`, `య - య్+అ`, `య్+ఇ - య`.

| Preceding syllables must share identical metrical weight.

| **Canonical**: Resolves secondary phonetic glide insertion against etymological `య`.

| | **Sva-vargaja Prāsa (స్వవర్గజ ప్రాసము)**

 | Intra-varga cognate consonants match (specifically dental stops).

| `ధ - థ` (e.g., *śōdhiñci \- dvīthulandu*, *vidhi \- madhura*, *bādha \- nātha*).

| Preceding syllables must share identical metrical weight.

| **Permissible**: Valid intra-class aspirate rhyming.

| | **Na \- Ṇa Ubhaya Prāsa (న \- ణ ప్రాసము)**

 | Dental nasal `న` matches retroflex nasal `ణ`.

| `న - ణ` (across both derived/ādeśa `ణ` and etymological/śabda-siddha `ణ`).

| Preceding syllables must share identical metrical weight.

| **Canonical**: Fully validated from Nannaya onwards despite medieval copyist attempts to regularize text.

| | **Sa \- Śa Ubhaya Prāsa (స \- శ ప్రాసము)**

 | Dental sibilant `స` matches palatal sibilant `శ`.

| `స - శ` (e.g., *kāśa \- kōsala*, *nēśikhaṇḍi \- yēsena*, *nāsikā \- dṛgrūśirōja*, *śaśikānti \- dasili*).

| Preceding syllables must share identical metrical weight.

| **Canonical**: Sibilant class equivalence.

| | **La \- Ḷa Abhēda Prāsa (ల \- ళ ప్రాసము)**

 | Dental lateral `ల` matches retroflex lateral `ళ`.

| (1) Tatsama loanwords (`నళి - నీల`, `నలు - దళ`, `శైల - ధూళి`, `కాళి - శాల`).

&nbsp;

&nbsp;

(2) Native Telugu words (`వొల - తళు`, `జాళు - న్నేల`).

&nbsp;

&nbsp;

(3) Geminates (`తల్లి - ద్రెళ్ళి`, `వల్లీ - గిళ్ళ`, `నాళ్ళు - ర్తిల్లు`).

| Preceding syllables must share identical metrical weight.

| **Canonical**: Applies across simplex and geminate lateral formations.

| | **Ṛ-Prāsa (ఋప్రాసము)**

 | Word-initial vocalic vowel `ఋ` matches consonant `ర` (rēpha).

| `ర - ఋ` (e.g., *gāravamunan-icci yā ṛṣitōḍan*).

| Preceding syllables must share identical metrical weight.

| **Canonical**: Validated because word-initial `ఋ` phonetically functions as `ri` / `rēpha`.

| | **Laghu-dvitva Prāsa (లఘుద్విత్వ ప్రాసము)**

 | Native Telugu light-weighting conjuncts (`ద్రు / ద్రి`) rhyme together.

| `విద్రు - లద్రు`, `విద్రి - లద్రు` (*vidrucu / adrucu*).

| **Must both be Laghu** (conjunct fails to induce Guru weight on preceding short vowel).

| **Specialised**: Also termed *Sama-laghu Prāsa* by Anantāmātya. Preceding vowels remain light.

|

---

### Non-Standard Variants & Rejection Guardrails

Prosodists (including Appakavi) record certain variant formations that authoritative treatises reject as non-standard (**అనుసరణీయములు కావు**). The engine must flag or disallow these forms:

* **Saṁyuktāsaṁyukta Prāsa Guardrail (సంయుక్తాసంయుత ప్రాస నిషేధము):**  
* *Rēpha Cluster Asymmetry:* Rhyming an unclustered consonant against a rēpha conjunct (`C` vs `ర్C` / `C్ర`, such as `డ - ండ్ర`, `క్త - క్త్`, `భ - ంభ్ర`, `ద - ంద్రు`, `మ - మ్ర`).  
* *La-kāra Cluster Asymmetry:* Rhyming an unclustered consonant against a lateral conjunct (`C` vs `ల్C`, such as `ండు - ండ్లు`).  
* *Engine Action:* **Reject / Restrict**. Classical usage does not recognize this as standard practice; it is considered an irregular poetic defect (*aprayōga-yōgyamu*).  
* **Pūrṇārdha-bindu Prāsa Guardrail (పూర్ణార్ధబిందు ప్రాస నిషేధము):**  
* Pairing an ardhabindu-supported syllable with a pūrṇabindu-supported syllable (e.g., `పాఁడి - తండ్రి` where `ఁడి` pairs with `ండ్రి`, or `వేఁడు - బండ్లు` where `ఁడు` pairs with `ండ్లు`).  
* *Engine Action:* **Reject / Restrict**. Although Appakavi authored an illustrative verse containing this construction, he failed to define it as a recognized prosodic class, and broader authorities reject it as defective.  
* **Textual Corruption / Scribal Tampering Defense:**  
* In instances of `న - ణ` rhyme (such as Nannaya's *Ādi 1-80* `యౌని - మాణ` and *Sabhā 4-127* `యని - గుణ`), later scribes altered readings to `ప్రమానుసంఖ్య` or `యగ్గుణములు` to eliminate the `న-ణ` pairing.  
* *Engine Action:* The engine must reject scribal regularizations. Nannaya's undisputed usage in *Āraṇya 1-49* (`దుర్నిమిత్తముల్ - నిర్ణయించి`) confirms that `న - ణ` constitutes an authentic, approved rhyme.

---

### Provenance Trail

* **Prosodic & Grammatical Treatises:**  
* *Appakavīyamu* (Kāṇḍa 3):  
* Verses 315, 320: Illustrations of Saṁyuktāsaṁyukta and Pūrṇārdhabindu (critiqued).  
* Verse 326: Illustration of Laghu-dvitva Prāsa Yati (*vidruce vinatātmajuḍu dikkuladruvananaga*).  
* Verse 35: Khaṇḍākhaṇḍa Prāsa Yati demonstration (*mīdi śabdambulakun-ādi varṇaṁbulu*).  
* *Chandōdarpaṇamu* (Anantāmātya, 1-49): Defines Laghu-dvitva rhyming as *Sama-laghu Prāsamu* (*vidricen-asura kṛṣṇuḍu dikkuladruvananaga*).  
* *Dēvī Vijayamu*: Cited by Appakavi for cluster rhyming (*vāk-trinētrāṅganā*).  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-80) *akṣauhiṇi / pramāṇa*, (1-94) *limmu*, (2-83) *vīgi*, (2-98) *kriya*, (3-27) *naḷinīla*, (3-140) *tatkūpamu*, (4-66) *satulaku*, (4-66) *eṭṭi*, (4-127) *duḥkhambu*, (4-161) *kōpamaḍara*, (4-261) *sakala*, (5-31) *ratnapuñja*, (5-60) *santōṣa*, (5-60) *cēsedanu*, (5-136) *bhūṣaṇāvaḷi*, (5-136) *patnī*, (6-5) *andu*, (6-202) *veṟaci*, (6-218) *lāvu*, (6-267) *yamunā*, (7-87) *yā ṛṣitōḍa*, (7-209) *vedavyāsu*, (7-276) *caṇḍamayūkhamul*.  
* *Sabhā Parva:* (1-108) *pitṛ*, (1-215) *mogi*, (1-287) *mī yanugrahamuna*, (2-37) *beggalambu*, (2-189) *nityavrata*, (2-282) *adhyātma*.  
* *Vana (Āraṇya) Parva:* (1-49) *durnimittamul*, (2-52) *naluni kāni*, (3-122) *nandu*, (3-312) *mrākulu*, (4-101) *kenjaḍalugā*, (4-188) *mīda*, (5-25) *vargambu*, (5-464) *nīgi*, (6-85) *lālintunē*.  
* *Virāṭa Parva:* (2-37) *beggalambu*, (2-52) *nettammirēkula*, (2-76) *śaśikānti*, (2-140) *durdamaprati*, (2-294) *nalagi*, (3-85) *debba*, (3-256) *bhallamuna*.  
* *Udyōga Parva:* (2-325) *nē śikhaṇḍi*, (4-127) *anina nī ceppina guṇamul*.  
* *Bhīṣma Parva:* (3-275) *śakyameddi*.  
* *Śānti Parva:* (1-111) *viśvalōka*, (2-192) *lajjā*, (2-344) *matsamuṇḍavu*, (2-390) *siddhi*, (4-153) *viprayōgōṣṇa*, (5-56) *śōbhana*, (5-223) *kṛṣṇulādigā*, (6-99) *mēdinī*, (7-12) *niṣṭhatō*, (7-120) *dhānya*.  
* *Anuśāsanika Parva:* (4-8) *nalupu*, (4-23) *bāṇa*.  
* *Svargārōhaṇa Parva:* (32) *viśadabhāvambu*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (1-54) *gandhasāra*, (1-177) *vaccucunnadi*, (2-159) *nāsikā*, (3-144) *sādhu*, (4-37) *dīrgha*, (4-80) *talli*, (4-88) *nirjāḍya*, (4-202) *durvāra*, (5-94) *naḷlu*, (6-96) *kaṇṭha*, (8-135) *nēṭiki*.  
* *Manucaritramu* (Allasāni Peddana): (1-50) *binkāna*, (1-54) *vaccu niṇṭiki*, (2-7) *naḍḍambu*, (2-9) *munnu*, (2-11) *nappaṭappaṭiki*, (2-23) *vallī*, (2-27) *yanga*, (2-73) *gādhipaṭṭiki*, (2-195) *mēdinīśvaruṇḍu*.  
* *Haravilāsamu* & *Kāśīkhaṇḍamu* (Śrīnātha): (1-54) *varaṇa*, (4-158) *nā yoppidamuna*, (5-3) *śōdhiñciri*.  
* *Bhīmēśvara Purāṇamu* (Śrīnātha): (5-88) *nāṭe mandāra*.  
* *Kumārasambhavamu* (Nanne Cōḍa): (10-38) *muttaraṅgalāru*.  
* *Bhāskara Rāmāyaṇamu* & *Molla Rāmāyaṇamu*: Sundara (130) *cūcirā*, Yuddha (34) *śailadhātu*, Araṇya (56) *yē mrānu*.  
* *Ghaṭikācala Māhātmyamu*: (2-111) *lēñjiguḷḷaku*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Prosodic Extraction & Engine Logic Specification (Part 18\)**

---

### Additional Prāsa Yati Classes (ప్రాసయతి విశేష భేదములు)

When standard head Yati fails in permitted metres, Prāsa Yati substitutes the match by validating rhyme between Position 2 (**Prāsa 1**) and the position immediately following the Yati node (**Prāsa 2**), adhering to **Prāsa-Pūrvākṣara Niyama**.

| Prāsa Yati Class | Rhyming Mechanism & Canonical Target Pairs | Weight Invariant on Preceding Akṣara | Engine Logic & Behavior |
| :---- | :---- | :---- | :---- |
| **Vikalpa Prāsa Yati (వికల్పప్రాసము)**&nbsp; | Sanskrit Anunāsika Sandhi optional forms: Class 5 nasal conjuncts (`ఙ్న`, `ఙ్మ`) pair with Class 3 stop conjuncts (`గ్న`, `గ్మ`, `గ్ని`, `గ్మి`). |  |  |

&nbsp;

&nbsp;

Pairs: `ఙ్న - గ్ని`, `ఙ్మ - గ్మ`, `ఙ్ము - గ్మి`.

| Must be strictly **Guru** (inherent before conjuncts).

| Matches across optional sandhi doubles (e.g., *prāṅnaga / prāgnaga*, *vāṅmanōhara / vāgmanōhara*, *diṅmahita / digmahita*, *srajnīcaya / sragnicaya*).

| | **Prāsamaitrī Prāsa Yati (ప్రాసమైత్రి ప్రాసము)**

 | Rigid full nasal \+ ba (`ంబు`, `ంబ`) pairs with geminate ma (`మ్ము`, `మ్మ`).

&nbsp;

&nbsp;

Pairs: `మ్మ - ంబు`, `ంబ - మ్ము`.

| Must be strictly **Guru** (conditioned by anusvāra or gemination).

| Canonical Appakavi license: *gatti-binduvu mīdi ba-kāramunaku jamili-mā prāsamaitri*.

| | **Sādhu-Śakaṭa Rēpha Prāsa Yati (ర \- ఱ ప్రాసము)**

 | Sādhu Rēpha (`ర`) rhyming with Śakaṭa Rēpha (`ఱ`).

&nbsp;

&nbsp;

Pairs: `దరు - మఱ`, `పెఱి - నొర`, `తరు - మెఱి`, `చోర - జూఱ`, `కొఱ - పురు`, `సర - పఱ`, `నెఱు - కురు`, `వైర - దీఱి`.

| Both must be uniformly **Laghu** or uniformly **Guru**.

| Classically deemed *Prāsavairamu* by Appakavi, but fully validated in later Kāvya usage (Tikkana, Errapragada, Śrīkṛṣṇadēvarāya, Molla).

| | **Sandhigata Prāsa Yati (సంధిగత ప్రాసము)**

 | Rhyme evaluated on consonants produced post-sandhi via Ādēśa, Āgama, or Trika sandhi operations.

&nbsp;

&nbsp;

Pairs: Post-druta `ంగ - ంగ` (*tōḍaṅgaḍaṅgi*), Trika geminates `మ్మ - మ్మ` (*immahā*), `క్క - క్క` (*akkanyaka*), `య్య - య్య` (*iyyinti / ayyanaṅguḍu*), `గ్గ - గ్గ` (*agguruḍu*).

| Governed by post-sandhi structural weight (Guru for geminates/anusvāra).

| The parser must analyze the surface sandhi-realized consonant, not the underlying morpheme base.

| | **Adhika Prāsa Yati (అధికప్రాసము)**

 | A geminated-plus-consonant conjunct matches a non-geminated conjunct sharing the same consonants.

&nbsp;

&nbsp;

Pairs: `జ్జ్వ - జ్వా` (*ujjvala \- tāpajvāla*), `త్త్ర - త్ర` (*putra \- citra*, *dhātri \- putra*), `త్త్వ - త్వ` (*tattva \- satva*), `శ్శ్రీ - శ్రీ` (*viśravassunaku \- tapaśrī*). | Must be strictly **Guru**. | Licenses asymmetric geminate clustering over identical consonant bases.

|

---

### Prāsa Yati Precedence Resolution (యతి-ప్రాసయతి వివేచన)

* **Dual-Match Priority Gate:** In metres where Prāsa Yati is allowed (*Sīsamu, Tēṭagīti, Āṭaveladi*), if a line fulfills both standard head Yati (Position 1 $\\leftrightarrow$ Yati node) and Prāsa Yati (Position 2 $\\leftrightarrow$ Yati+1 node), **Standard Yati takes absolute precedence**.  
* *Example:* *bhūṣaṇambiṭṭivē peṟabhūṣaṇamulu* fulfills both Prāṇi Yati (`భూ - భూ`) and Prāsa Yati (`ష - ష`). The engine logs this strictly as **Prāṇi Yati**; Prāsa Yati is not invoked.  
* *Exception (Avakaliprāsa Sīsamu):* In constrained forms specifically requiring all-line Prāsa Yati, Prāsa Yati classification is enforced over regular Yati.  
* **Disallowed Rhyme Categories in Prāsa Yati:**  
* `ద - ధ`, `డ - ఢ`, `ల - డ`, `ళ - డ`, `స - ష` are deemed uncanonical or disputed in Prāsa Yati contexts.  
* Textual instances of `డ - ఢ` (e.g., *lēḍu \- rūḍhiki*) are scribal corruptions for `రూడి` (Sama Prāsa `డ - డ`) and should not be generalized.

---

### ఌ-kāra Yati (ఌకార యతి)

Addresses vocalic Sanskrit $\\text{\\fontencoding{LTL}\\selectfont\\char14}$ ($\\text{\\fontencoding{LTL}\\selectfont\\char14}$ / $\\text{\\fontencoding{LTL}\\selectfont\\char15}$) surviving in the solitary Tatsama loan root **కౄప్త** (*kḷpta* \= arranged) and its derivatives (*kḷpti, kḷptamu*).

* **Phonetic & Sāvarṇya Foundation:**  
* Pāṇinian Vārtika: *'Ṛ-ḷ varṇayōr mithas sāvarṇyaṁ vācyam'* establishes mutual savarṇa identity between `ఋ` and `ఌ`.  
* In Telugu phonological yati grouping, vocalic `ఋ` belongs to the **I-varga vowel group** (`ఇ, ఈ, ఎ, ఏ, ఋ, ౠ`). Consequently, `ఌ` integrates into this same group.  
* **Matrix of Licensed Yati Matches for `కౄ` (*kḷ*):**  
1. **Prāṇi Yati:** `కౄ` matches `కి, కీ, కె, కే, కృ, కౄ`.  
2. **Vargaja Yati:** `కౄ` matches velar stops combined with I-varga vowels:  
* With `ఖ`: `ఖి, ఖీ, ఖె, ఖే, ఖృ, ఖౄ`  
* With `గ`: `గి, గీ, గె, గే, గృ, గౄ` (e.g., *kṛtavīryu dhanamella kḷptisēsi* pairing `కృ - గౄ`; Campū Rāmāyaṇamu pairing `కౄ - గీ`)  
* With `ఘ`: `ఘి, ఘీ, ఘె, ఘే, ఘృ, ఘౄ` (e.g., Bhāgavatamu pairing `ఘృ - కౄ`)  
3. **Consonant Release (*ḷa-kāra sambandha*):** Parallel to `కృ` matching `రి, రీ, రె, రే`, `కౄ` matches dental/retroflex lateral liquids:  
* Matches `లి, లీ, లె, లే` (e.g., *kḷpta dhammillamu* pairing `కౄ - లీ`).  
* Via *la-ḷa abhēda*, matches `ళి, ళీ, ళె, ళే` (Anantāmātya's core definition: *kḷpti lēdu śauriguṇāvaḷikin-anaṅga* pairing `కౄ - ళి`).  
4. **Pure Vowel Release (*svara-sambandha*):** `కౄ` matching independent vowels `ఇ, ఈ, ఎ, ఏ, ఋ, ౠ` (theoretically valid under Ṛtva-sambandha logic, though lacks kāvya attestations).

---

### Rēpha-La / Rēpha-Ḷa Yati (ర \- ల, ర \- ళ యతులు)

* **ర \- ల Yati Status (Disputed vs. Established):**  
* *Appakavi's Stance:* Condemned as an inadmissible non-cognate match (*Agrāhya Abhēda Varga Yati*). Appakavi systematically emended classical verses containing `ర - ల` (reading *candralēkha* for *candra-rēkha*, *lōlambālaka* for *rōlambālaka*, etc.).  
* *Engine Ruling:* **Validated and Accepted**. Classical texts confirm broad, deliberate usage:  
* Errapragada (*Uttara Harivaṁśamu* 7-181): *Citrarēkha* pairing `రే - లీ`.  
* Śrīnātha (*Kāśīkhaṇḍamu* 6-210): *udrēkin̄ci* pairing `లీ - రే`.  
* Rāmarājabhūṣaṇa (*Vasucaritramu* 3-162): *rōlambālaka* pairing `రో - లు`.  
* Gōpīnātha Rāmāyaṇamu: Dozens of occurrences pairing `ర - ల`, `రో - లో`, `రా - లా`, `రా - ల`.  
* **ర \- ళ Yati (Derived Abhēda):**  
* Since `ర - ల` is established, and `ల - ళ` is canonical Abhēda, classical poets derive `ర - ళ` as an authentic secondary alliance.  
* *Attestations:* *Hariścandrakatha* (`రే - ళ`), *Nārikēḷa* (`ర - ళ`), *bhaḷā* (`ర - ళ`).  
* **Disqualification of ఋ \- లి (Ṛ \- Li) Pseudo-Deduction:**  
* Certain late texts argued: if `ఋ $\leftrightarrow$ రి` and `రి $\leftrightarrow$ లి`, then `ఋ $\leftrightarrow$ లి` must hold (e.g., Gōpīnātha Rāmāyaṇamu pairing *salilamu* `లి` with *anāvṛṣṭi* `వృ`).  
* *Engine Ruling:* **Strictly Invalid / Prohibited**. `ఋ - రి` Yati exists solely because vocalic `ఋ` has the phonetic pronunciation \[ri\]. There is no phonetic justification for rhyming an independent vowel with an arbitrary liquid consonant; transitivity across vocalic/consonantal boundaries is rejected.

---

### Caturthī Vibhakti Yati (చతుర్థీవిభక్తి యతి)

Addresses Dative case postpositions **కయి (kayi)** and **కై (kai)**.

$$\\text{Stem} \+ \\text{కున్} \+ \\text{అయి / ఐ} \\implies \\text{కున్-లోపము} \\implies \\mathbf{కయి / కై} \\quad (\\text{Ubhaya Yati Node})$$

* **Theoretical Basis:** Sūkavi Manōran̄janamu formalizes Caturthī Vibhakti Yati where Appakavi failed. Because *kai* derives from *kun \+ ai*, the syllable `కై` preserves both base morpheme boundaries, operating as an authentic **Ubhaya Yati (ఉభయయతి)**:  
* **Acchu Yati:** Matches the underlying dative vowel `ఐ` / `అ` via Svara Yati (e.g., *śivamauḷikai* matching `అ - ఐ`, *nākai* matching `అ - ఐ`, *vṛkṣadēśamunakai* matching `హ - ఐ`).  
* **Hal Yati:** Matches consonant `క` / `కై` via Prāṇi Yati or Vargaja Yati (e.g., *murārikai* matching `కై - గ`, *muktikai* matching `గ - కై`, *puṇyamulakai* matching `కా - కై`, *āstikai* matching `కై - గ`).  
* *Engine Contrast:* Unlike the rejected Pañcamī *kaṇṭen* split, **Caturthī *kai* has extensive classical backing** in Nannaya, Tikkana, Errapragada, and Śrīnātha.

---

### Nitya Sandhi Yati (నిత్యసంధి యతి)

Governs Sanskrit compulsory assimilation sandhis where an underlying dental stop (`త, థ, ద, ధ` in stem final position) assimilates entirely into the succeeding consonant. The engine licenses **pre-sandhi dental stop Yati** on the surface assimilated consonant.

* **Parasavarṇa Sandhi (Torli Sūtra: *tat-varga \+ la $\\to$ lla*):**  
* Sanskrit rule: *'Tōrli'* (Pāṇini 8-4-60).  
* *Underlying:* `త / ద` \+ `ల` $\\to$ `ల్ల`.  
* *Engine Matching:* At the resulting geminate `ల్ల / ల్లా / ల్లీ / ల్లో`, the poet may match either:  
1. **Surface Consonant (Saṁyukta Yati):** Match consonant `ల` (`ల్లా - లా`, `ల్లీ - లీ`, `ల్లో - లో`).  
2. **Pre-Sandhi Dental Stop (Nitya Sandhi Yati):** Restore underlying dental `త / ద` merged with the succeeding vowel:  
* *ullāsamu* (*ud \+ lāsa*): Juncture `ల్లా` $\\to$ matches `దా` (e.g., *kutūhalōllāsamunan* pairing `దా - థ`).  
* *sancarallīlā* (*sancarat \+ līlā*): Juncture `ల్లీ` $\\to$ matches `తీ` (pairing `తీ - తే`).  
* *visphurallīlan* (*visphurat \+ līla*): Juncture `ల్లీ` $\\to$ matches `తీ` (pairing `తీ - తే`).  
* **Ścutva Sandhi (*tat-varga \+ ś/ca-varga $\\to$ ca/ja-varga*):**  
* *Underlying:* `త్ / ద్` \+ `చ / జ` $\\to$ `చ్చ / జ్జ`.  
* *Engine Matching:* At surface `చ్చ / జ్జ`, poets may target underlying dental `త / ద`:  
* *udval-līla / udvaccuraṇa* (*udvat \+ caraṇa*): Juncture `చ్చ` matches `త`.  
* *mad-janaka* (*mat \+ janaka*): Juncture `జ్జ` matches `త`.  
* *bhavac-carita* (*bhavat \+ carita*): Juncture `చ్చ` matches `త`.  
* *dvac-caraṇa* (*tvat \+ caraṇa*): Juncture `చ్చ` matches `త`.  
* *roccalita* (*ud \+ calita*): Juncture `చ్చ` matches `ద` (pairing `ద - ధా`).  
* **Chatva Sandhi (*tat-varga \+ śa $\\to$ ccha*):**  
* *Underlying:* `త్ / ద్` \+ `శ` $\\to$ `చ్ఛ`.  
* *Engine Matching:* At surface `చ్ఛ`, poets may target underlying dental stop `త / ద`:  
* *tacchailanibhāṅga* (*tad \+ śaila*): Juncture `చ్ఛై` matches underlying `దై` (pairing `దై - దా`).  
* *vilasacchilpa* (*vilasat \+ śilpa*): Juncture `చ్ఛి` licenses `తి` via Nitya Sandhi Yati, or `చి` via Saṁyukta Yati.  
* **Ṣṭutva Sandhi (*tat-varga \+ ṭa-varga $\\to$ ṭṭa/ḍḍa*):**  
* *tat \+ ṭīkā \= taṭṭīkā*; *lasat \+ ḍhakkā \= lasaḍḍhakkā* $\\to$ licenses underlying dental stop matching.

---

### Liquid-Retroflex & Dental-Retroflex Yati Logic

                    ┌─────────────────────────┐

                    │      ల  \<═════\>  డ      │  (Abhēda Yati: Sanskrit & Telugu Roots)

                    └────────────┬────────────┘

                                 │

                 Derived via     │     Derived via

                 Abhēda:         │     Allophonic Interchange:

                                 ▼

                    ┌─────────────────────────┐

                    │      ళ  \<═════\>  డ      │  (vāḍi-vaḷi, pavvaḍin̄cu-pavvaḷin̄cu)

                    ├─────────────────────────┤

                    │      ద  \<═════\>  డ      │  (Sāvarṇya Yati: dambha-ḍambha, dāka-ḍāka)

                    └─────────────────────────┘

                                 │

                   Strictly Prohibited Extensions:

                     \* ల \- ఢ   (REJECT)

                     \* ళ \- ఢ   (REJECT)

                     \* ధ \- డ   (REJECT)

                     \* ద \- ఢ   (REJECT)

                     \* త \- డ   (REJECT)

&nbsp;

**1\. ల \- డ (La \- Ḍa) & ళ \- డ (Ḷa \- Ḍa) Abhēda Yati**

* **Sanskrit/Telugu Etymological Basis:** Rooted in the Pāṇinian maxim *'La-ḍayōr abhēdaḥ'* (e.g., *jaladhi / jaḍadhi*, *vīḍā / vrēḷā*, *vaḍi / vaḷi*, *pavvaḍin̄cu / pavvaḷin̄cu*).  
* **Engine Scope:** Both `ల - డ` and `ళ - డ` are canonical Abhēda matches.  
* *Examples:* *kalā-lasat* pairing `లా - డ`; *Bhāgavatamu* pairing `ల - డ`; Nannaya (*Ādi 8-148*) pairing `డు - ళు` (*kōl-mosaḷul*).  
* **Aspirate Disqualification:** `ల - ఢ` and `ళ - ఢ` are **strictly rejected**. They lack phonetic equivalence and have zero kāvya support; Appakavi places `ల - ఢ` under *Agrāhya Yati*.

**2\. ద \- డ (Da \- Ḍa) Sāvarṇya Yati**

* **Double-Form (*Dvirūpa*) Foundations:** Sanskrit and Telugu lexicons record identical words alternating initial dental `ద` and retroflex `డ`:  
* *Sanskrit:* *dambha / ḍambha*, *diṇḍīra / ḍiṇḍīra*, *dōlikā / ḍōlikā*, *dāḍima / ḍāḍima*.  
* *Telugu:* *dāka / ḍāka*, *daggaṟa / ḍaggaṟa*, *diggiya / ḍiggiya*, *dāya / ḍāya*, *dōya / ḍōya*, *dāpala / ḍāpala*, *diggu / ḍiggu*, *dancu / ḍancu*, *doppa / ḍoppa*.  
* **Appakavi's Restriction vs. Broad Implementation:** Appakavi restricted `ద - డ` Yati to alternating double-form lexical items under the label *Ādēśa Yati*. *Lakṣaṇa Śirōmaṇi* and classical usage establish that because `ద` and `డ` are proven phonetic interchanges, **`ద - డ` functions as a generalized cross-class Sāvarṇya Yati**.  
* *Attestations:* *ḍagguttika \- dayitayu* (`డ - ద`); *Dāśarathī Śatakamu* (`డా - దా`); *ḍīkoni \- daṇḍadhara* (`డీ - ది`); *gāṇḍīvamu \- depparamaina* (`డీ - దె`); *Dāśarathī Śatakamu* (*ḍāṇḍa \- aṇḍamu* pairing `డా - ద`); Errapragada (*Harivaṁśamu* pairing `దై - డా` where editors falsely altered *ḍākinī* to *tāmasa*).  
* **Cross-Varga Derivative Disqualifications:** Rhyming other members of the dental and retroflex vargas (`ధ - డ`, `ద - ఢ`, `త - డ`) is **strictly rejected as defective** (*kavi-prāmādikamu / anūsaraṇīyamu kādu*). The interchangeability exists exclusively between unaspirated voiced stops `ద` and `డ`.

---

### Provenance Trail

* **Pāṇinian & Sanskrit Grammatical Authorities:**  
* *Pāṇini Aṣṭādhyāyī:* Sūtra 8-4-60 (*Tōrli* for Parasavarṇa Sandhi); Sūtra 8-4-40, 41 (*Ścutva* and *Ṣṭutva* Sandhi).  
* *Siddhānta Kaumudī:* Sūtra 12 citing Vārtika *'Ṛ-ḷ varṇayōr mithas sāvarṇyaṁ vācyam'*; Maxim *'La-ḍayōr abhēdaḥ'*.  
* **Telugu Prosodic & Grammatical Treatises:**  
* *Appakavīyamu* (Kāṇḍa 3):  
* Verse 328: *Vikalpa Prāsa Yati* in Anunāsika Sandhi.  
* Verse 343: *Prāsamaitrī Prāsa Yati* (`ంబు - మ్మ`).  
* Verses 88, 94, 270: Treatment of `ల-డ`, `ళ-డ`, and rejection of `ల-ఢ`.  
* Verse 265: Formulation of `ద-డ` under *Ādēśa Yati*.  
* Verse 270: Condemnation of `ర-ల` as *Agrāhya Abhēda Varga Yati*.  
* *Chandōdarpaṇamu* (Anantāmātya):  
* 1-50: Formulation of *Vikalpa Prāsa Yati*.  
* 1-90: Definition of *ఌ-kāra Yati*.  
* 1-95: Demonstration of *Kāku-svara / ళ\-డ Yati* in *pavvaḷin̄ce*.  
* *Sukavi Manōran̄janamu* (Kūcimanci Timmakavi):  
* 3-10, 3-12: Primary codification of *Nitya Sandhi Yati* (*Torli, Ścutva, Chatva*).  
* 3-78, 3-86: Codification of *Caturthī Vibhakti Yati* on `కై`.  
* 2-285–301: Detailed defense of `ద-డ` against corrupt editorial regularizations.  
* *Lakṣaṇa Śirōmaṇi*: Formulation of *Cutvā-nunāsika Yati* (4-271) and *Sāvarṇya Yati* for `ద-డ` (4-158).  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-71) *immahābhārata*, (6-214) *tōḍaṅgaḍaṅgi*, (7-160) *akkanyaka*, (7-173) *janulakuṅgaḍu*, (8-148) *kōl-mosaḷul*.  
* *Sabhā Parva:* (2-157) *putravatsaluḍu*, (2-174) *nākai*.  
* *Vana (Āraṇya) Parva:* (2-143) *bhūṣaṇambiṭṭivē*.  
* *Virāṭa Parva:* (2-27) *iyyinti*.  
* *Udyōga Parva:* (2-33) *gāṇḍīvamu \- depparamaina*.  
* *Bhīṣma Parva:* (2-1394) *kutūhalōllāsamunan*.  
* *Śānti Parva:* (5-108) *guṇatva-rahitamaina tattvamanagha*, (6-30) *padupuliviyuṅga*, (7-133) *kṛtavīryu dhanamella kḷptisēsi*.  
* *Anuśāsanika Parva:* (2-245) *kṣētrajūṅḍanagā*, (5-245) *tattva-santānambu satvamunu*.  
* *Āśramavāsa Parva:* (1-85) *tapaścaraṇambunakai*.  
* *Mauśala Parva:* (86) *dharmarakṣaṇamunakai*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (1-17) *śūlikaina*, (3-70) *taruṇi*, (4-112) *cōrabādhā*, (5-281) *ghṛtapayōrāśi saṅkḷptā*, (6-208) *sancarallīlā*, (7-219) *ḍāmbikunaku*, (10-uttara-540) *tallīlā*, (10-4-86) *samuccandamu*.  
* *Kāśīkhaṇḍamu* (Śrīnātha): (6-210) *udrēkin̄ci*, (7-34) *dampudumē*, (7-80) *dantunō*.  
* *Uttara Harivaṁśamu* (Errapragada): (7-181) *citrarēkha*.  
* *Vasucaritramu* (Rāmarājabhūṣaṇa): (3-162) *rōlambālaka*, (4-25) *rāyan̄ca*.  
* *Āmuktamālyada* (Śrīkṛṣṇadēvarāya): (4-92) *tallōlēndra*.  
* *Gōpīnātha Rāmāyaṇamu*: Bāla (205, 243, 257, 356, 500, 585, 661, 779); Yuddha (36) *roccalita*.  
* *Molla Rāmāyaṇamu*: Yuddha (1-57) *vairamellanu*, (3-40) *dēlucu \- ḍīkoni*.  
* *Dāśarathī Śatakamu* (Kan̄cerla Gōpanna): (2-1500) *tīkṣṇa-nakhatuṇḍambai*, and *ḍāṇḍa-ninadamu*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Yati Engine Rules & Architectural Specification (Part 19\)**

---

### Non-Standard, Defective & Rejected Yati Classes (అగ్రాహ్య యతులు)

Prosodic engines must distinguish between authentic poetic licenses and defective formations (*kavi-prāmādikamu* / *agrāhya-vadhulu*) that violate core phonological principles.

| Rejected Yati Class | Description & Theoretical Claim | Structural Reason for Invalidation / Engine Flag | Engine Status & Action |
| :---- | :---- | :---- | :---- |
| **Ya-Śa Varga-dvaya Yati (యశ వర్గద్వయ యతి)**&nbsp; | Claims mutual internal yati within the semi-vowel set `య, ర, ల, వ` and sibilant/aspirate set `శ, ష, స, హ` (*Sulakṣaṇa Sāramu*). |  |  |

| Lacks phonetic justification (*hētu-rahitamu*). Except for the independently established `ర - ల` license, pairing `య-ర`, `య-ల`, `య-వ`, `ర-వ`, `ల-వ`, `శ-హ`, `ష-హ`, `స-హ` is strictly uncanonical.

| **REJECTED** (*Agrāhya Varṇa-catuṣṭaya Vaḷulu*). Classical poets do not systematically endorse these.

| | **Plain Vargāntya Yati (బిందురహిత వర్గపంచమాక్షర యతి)**

 | Purports that stops 1–4 of a varga may match the 5th nasal stop without an anusvāra (e.g., `త - న`, `థ - న`, `ద - న`, `ధ - న`).

| Violates the core definition of **Bindu Yati**. Stops 1–4 require an immediately preceding anusvāra (`ంత, ంథ, ంద, ంధ`) to rhyme with nasal `న`. Early interpolations into *Kavijanāśrayamu* claiming otherwise are spurious.

| **STRICTLY REJECTED**.

| | **Sambhāvana Yati (సంభావన వడి — మ-వ యతి)**

 | Claims direct consonantal matching between bilabial nasal `మ` and labio-dental semi-vowel `వ` (*Lakṣaṇa Dīpikā*, *Lakṣaṇa Rājīyamu*).

| False transitivity assumption (`ప, ఫ, బ, భ $\leftrightarrow$ మ` and `ప, ఫ, బ, భ $\leftrightarrow$ వ` $\\implies$ `మ $\leftrightarrow$ వ`). Matching `మ` with `వ` across A-varga (`మ/మా $\leftrightarrow$ వ/వా`) or I-varga (`మి/మీ $\leftrightarrow$ వి/వీ`) is totally invalid.

| **REJECTED** (*Agrāhyābhēda Varga Yati*). Stray treatise citations are erroneous errata.

| | **U \- Vu Yati (ఉ \- వు యతి)**

 | Rhyming independent initial vowels `ఉ, ఊ, ఒ, ఓ` with syllables containing consonant `వ` (`వు, వూ, వొ, వో`).

| Folk-speech confusion (colloquial *ūru/vūru*, *unna/vunna*). In written classical Telugu, `వు/వో` never occurs word-initially, and internal medial `వు` has no phonetic equivalence to independent `ఉ`.

| **STRICTLY REJECTED**. Classical occurrences are defective.

| | **U \- Ṛ Yati (ఉ \- ఋ యతి)**

 | Rhyming U-varga syllables (`కు, బు, బొ, ము, భూ`) with vocalic Ṛ-varga syllables (`కృ, బృ, మృ`).

| Cross-class category error. `ఋ` belongs strictly to the **I-varga vowel group** (`ఇ, ఈ, ఎ, ఏ, ఋ, ౠ`); it cannot rhyme with the **U-varga group** (`ఉ, ఊ, ఒ, ఓ`). Caused by phonetic confusion between `ఋ` and spoken `రు`.

| **STRICTLY REJECTED**.

| | **Ṛ \- Ru Yati (ఋ \- రు యతి)**

 | Rhyming vocalic vowel `ఋ` (or consonants bearing vatrasuḍi `కృ, మృ, భృ`) with consonant rēpha plus u-kāra (`రు, రూ, త్రు, గ్రూ`).

| Vocalic `ఋ` matches only with `రి, రీ, రె, రే` (**Ṛ-yati**), never with rounded `రు/రూ`. Conflating Sanskrit vocalic vatrasuḍi with Telugu consonant cluster `ర్+ఉ` is a prosodic defect.

| **STRICTLY REJECTED**.

| | **Ghañ Yati (ఘఞ్ యతి)**

 | Claims Ubhaya Yati on `లా` in *ālapa* (*ā \+ lap \+ ghañ $\\to$ ālāpa*), matching base vowel `ఆ` or consonant `ల` (*Ānanda Raṅgarāṭchandamu*).

| Morphological error. Suffix *ghañ* induces root vowel lengthening (*ādi-vṛddhi*) on *lap*; it does **not** involve vowel sandhi (*āla \+ apa* does not exist). If allowed, it would force Ubhaya Yati on all *ghañ* forms (*pāka, pāda*), which is absurd.

| **REJECTED**. `లా` in *ālāpa* matches \*\*strictly as consonant `ల**` via Prāṇi Yati. Vowel matching on `ఆ` is discarded.

|

---

### Verified Specialized Yati Rules

                      SPECIALIZED YATI RESOLUTIONS

                                   │

         ┌─────────────────────────┼─────────────────────────┐

         ▼                         ▼                         ▼

   Mu \- Vu Yati             Matubādēśa Yati              Ēvārthaka Yati

 (ము/మూ/మొ/మో \<==\>         (Stem-Final 'va'             (Avadhāraṇa Suffixes:

   వు/వూ/వొ/వో)            licenses pre-sandhi          'a, e, ē' match via

                           original 'ma')               CONSONANT ONLY)

&nbsp;

**1\. Mu \- Vu Yati (ము \- వు యతి)**

* **Phonological Derivation:** While generalized `మ - వ` is prohibited, combining them with rounded **U-varga vowels** (`ఉ, ఊ, ఒ, ఓ`) creates a valid phonetic nexus:  
1. `పు, ఫు, బు, భు $\leftrightarrow$ ము` (validated by *Mu-vibhakti / Mu-kāra Yati*).  
2. `పు, ఫు, బు, భు $\leftrightarrow$ వు` (validated by *Abhēda / Abhēda-varga Yati*).  
3. Consequently: `ము, మూ, మొ, మో $\longleftrightarrow$ వు, వూ, వొ, వో`.  
* **Engine Matching Matrix:** Syllables in `{ము, మూ, మొ, మో}` match freely with `{వు, వూ, వొ, వో}`.  
* **Variant Status:** Valid across both derived soft/glide `వ` (Laghu va-kāra via gasaḍadavādēśa, e.g., *mīru vogadaṅga*, *śalyamul vōle*) and etymological radical `వ` (Alaghu va-kāra, e.g., *dēvuṇḍu*, *bhairavuṇḍu*, *rāvo*).

**2\. Matubādēśa Yati (మతుబాదేశ యతి)**

* **Morphological Process:** In Sanskrit, possessive suffix *matup* (*\-mat*) converts phonologically to *\-vat* following stems ending in `అ, ఆ` (Pāṇini 8-2-9: *Mādupadhāyāśca matōrvō yavādibhyaḥ*). Example: *bala \+ mat $\\to$ balavat $\\to$ balavantuḍu*; *dhana \+ mat $\\to$ dhanavantuḍu*.  
* **Engine Rule:** At the surface suffix syllable `వ` (*va*), the engine exposes **two alternative matching pathways**:  
* *Surface Consonant (Standard):* Matches consonant `వ` via regular Prāṇi Yati.  
* *Underlying Sthānin (Matubādēśa License):* Matches the original underlying Sanskrit morpheme nasal `మ` (*ma*).  
* *Canonical Attestation:* Errapragada (*Mahābhāratamu*, Śānti 6-199): *madi madinuṇḍiyēnu balavantuḍanai* pairing `మ` with the `వ` of *balavantuḍu* via underlying `మ-మ` Prāṇi Yati.

**3\. Ēvārthaka Suffix Handling (ఏవార్థకములు)**

* **Semantic Target:** Emphatic and restrictive postpositional clitics `అ`, `ఎ`, `ఏ` attaching to nominals and verbs (cognate to Sanskrit *ēva*: *nēna, nēne, nēnē; atanḍa, atanḍe, atanḍē; palla-ṭanba; tān-a; aṭl-a*).  
* **Engine Constraint:** These clitics fuse via standard Telugu vowel elision or glide assimilation. Classical usage universally treats the fused juncture as **consonantal only**.  
* *Engine Matching:* The engine evaluates the juncture syllable **strictly by its surface consonant** (e.g., matching `బ` in *parvamba*, `న` in *tāna*, `ల` in *aṭla*, `డ` in *atanḍē*). Matching the underlying clitic vowel (`అ, ఎ, ఏ`) is unsupported and disallowed.

---

### Treatise Clarification & Pseudo-Yati Deconstructions

* **Rēphayuta Yati (రేఫయుత యతి):** Formulated by Anantāmātya (*Chandōdarpaṇamu*) as an orthographic disambiguation rule rather than a new yati class. Pure native Telugu (*Acca-Tenugu*) words cannot contain vocalic `ఋ`. Any pronunciation sounding like \[ru\] in native roots is purely rēpha combined with u-kāra (`ర్+ఉ = రు`, as in *mruccimi, srukkanḍu, krummu*). These must be processed strictly via \*\*Saṁyukta / Ēkāntara Yati targeting `ర` or `మ/స/క**`, completely barring Ṛ-yati.  
* **Saubhāgya Yati (సౌభాగ్య యతి):** Formulated in *Sulakṣaṇa Sāramu* to label instances where both Position 1 and the Yati Position happen to be Ubhaya Yati nodes (e.g., two Prādi tokens or two Nitya Samāsa tokens in the same line). The engine must **reject this as a distinct structural category**; it represents an emergent artifact of existing Ubhaya Yati nodes, not a discrete functional rule.  
* **Yā-Yati (యాయతి):** *Bāla Vyākaraṇamu* (*Prakīrṇaka-3*) specifies that native Telugu nominals admit the palatal vowel combination `యె, యే` in only three root families: **ఊయేల (ūyēla)**, **పయ్యెద (payyeda)**, and **తాయెతు (tāyetu)** (along with their geminate and variant dialect forms: *uyyela, payyada, tāyettu*). In verb inflections, it occurs naturally (*kaniyen, viniyen, pōyen*). Yā-yati simply reminds the parser to verify whether the poet scanned the token with `యె` (matching I-varga vowels/semi-vowels) or alternate historical `య` (matching A-varga vowels). It introduces no novel matching logic.  
* **Ekkaṭi Yati Obsolescence (ఎక్కటి యతులు):** Pre-Appakavi prosodists grouped `మ, ర, ఱ, ల, వ` as isolated consonants (*ekkaṭi*) possessing no cross-class matches. Comprehensive classical evidence renders this taxonomy obsolete:  
* `మ` matches class stops via *Bindu Yati*, sibilants via *Ma-varṇa Yati*, and labials via *Mu-kāra / Mu-vu Yati*.  
* `ర` and `ఱ` match each other in extensive classical usage.  
* `ల` matches `ళ` and `డ` via *Abhēda Yati*.  
* `వ` matches `బ, ప, ఫ, భ` via *Abhēda / Abhēda-varga Yati*.  
* *Engine Architecture:* The engine completely dissolves the *Ekkaṭi* isolation class.

---

### Provenance Trail

* **Prosodic & Grammatical Treatises:**  
* *Sulakṣaṇa Sāramu*: Formulation of *Ya-Śa Varga-dvaya Yati*, *Saubhāgya Yati*, and *Yā-Yati*.  
* *Appakavīyamu* (Kāṇḍa 3):  
* Verse 262: Condemnation of non-anusvāra *Vargāntya Yati*.  
* Verse 266: Denunciation of *Agrāhya Varṇa-catuṣṭaya Vaḷulu* (`య-ర-ల-వ`, `శ-ష-స-హ`).  
* Verse 268: Categorization of *Sambhāvana Yati* (`మ - వ`) under *Agrāhyābhēda Varga Yati*.  
* *Chandōdarpaṇamu* (Anantāmātya):  
* 1-115: Formulation of *Rēphayuta Yati* distinguishing `ఋ` from `రు` in native Telugu roots.  
* 2-208: Attestation for cross-class errata.  
* *Ānanda Raṅgarāṭchandamu*:  
* 3-232–237: Presentation and critique of *Ghañ Yati* on *ālapa*.  
* *Bāla Vyākaraṇamu* (Paravastu Cinnaya Sūri): *Prakīrṇaka-3* on the distribution of `యె/యే` in native nominals.  
* *Vyākaraṇa Saṁhitā Sarvasvamu* (Vajjhala Cinasītārāmasvāmi Śāstri): Proof of regular *gasaḍadavādēśa* in Kavitraya usage validating *Mu \- Vu Yati*.  
* Pāṇini *Aṣṭādhyāyī*: Sūtra 8-2-9 (*Mādupadhāyāśca matōrvō yavādibhyaḥ*) for *Matubādēśa Yati*.  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (1-58) *pandraṇḍava parvamba* (`బ - ప`).  
* *Āraṇya Parva:* (2-79) *uyyela* (`యె - ఎ`), (5-335) *śalyamul vōle* (`ము - వో`).  
* *Virāṭa Parva:* (5-15) *samagra*.  
* *Udyōga Parva:* (4-313) *harṣambuna* (`ర - వ`).  
* *Karṇa Parva:* (2-30) *mīru vogadaṅga* (`వొ - ము`).  
* *Śānti Parva:* (6-199) *balavantuḍanai* (`మ - వ/మ`).  
* *Anuśāsanika Parva:* (1-311) *balavantuḍu* (`వ - వ`), (4-108) *bhairavuṇḍu* (`ము - వు`), (5-141) *santōṣavantulu*.  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (6-245) *vikramāṭōpamuna*, (10-4-458) *gōvula* (`వు - ఓ`), (10-4-560) *śitavāyavālina*, (10-4-896) *mahōgruḍai* (`ఉ - వు`), (10-4-1313) *puṇḍarīkanētru* (`రు - ఋ`), (11-74) *mṛdula* (`మృ - ము`).  
* *Palnāṭi Vīracaritramu* (Śrīnātha): (p. 34\) *mudamuna brāci dēvuṇḍu* (`ము - వు`).  
* *Āmuktamālyada* (Śrīkṛṣṇadēvarāya): (6-95) *kiṅkiṇīkalālāpamulan*.  
* *Uttara Harivaṁśamu* (Errapragada): (9-18) *aṭla* (`ల - ల`).  
* *Nṛsiṁha Purāṇamu*: (5-37) *tāna* (`న - నా`).  
* *Rāmāyaña Kalpavṛkṣamu* (Viśvanātha Satyanārāyaṇa): Bāla (38) *mātlaḍukavaḍi*, Ayōdhyā (506) *mālābaddhākhiḷa*.  
* *Dāśarathī Śatakamu* & *Sarvēśvara Śatakamu*: Attestations for *U-Ṛ* and *Ṛ-Ru* variant occurrences.

&nbsp;

&nbsp;

&nbsp;

**Yati Engine Rules & Architectural Specification (Part 20\)**

---

### ‘స్నాన' (Snāna) Special Yati Rule

In classical prosody, the Sanskrit loanword **స్నాన** (*snāna*) exhibits an exceptional three-way consonant matching behavior at its conjunct node `స్నా` (*snā*):

$$\\mathbf{స్నాన} \\implies \\text{Eligible Match Targets at } \\mathbf{స్నా}: \\quad {\\mathbf{స}, \\mathbf{న}, \\mathbf{త}}$$

* **Surface Saṁyukta Yati (Standard):** The surface cluster `స్నా` splits per standard Saṁyukta Yati rules into `స` or `న`:  
* *Matching `స`:* `స్నా - సం` (*snānamāḍene \- sandhyana*), `స్నా - సాం` (*snānānukrama \- sāndrāmbuvul*), `స్నా - జం` (*snānīya \- vastuvrajaṁbu* via Sarasa Yati).  
* *Matching `న`:* `స్నా - నం` (*snānaṁbulana \- tirthadānaṁbula*), `స్నా - న` (*snānamonarsi \- śubhravasanaṁbula*).  
* **The Exceptional Dental (`త`) Target License:**  
* Kūcimanci Timmakavi (*Lakṣaṇasāra Saṅgrahamu*) codifies that `స్నా` additionally matches dental `త` (*ta / tā*) or aspirated/voiced dental cognates (`ధ / ధా` via Vargaja Yati).  
* *Morphological Foundations:*  
1. **Tadbhavīkāra Perspective:** The Telugu tadbhava of *snānamu* is *tānamu*. Poets mentally invoke the native *tānamu* root even when writing the formal Tatsama *snāna*, matching `తా`.  
2. **Sanskrit Stnā Alternative Form:** Grammatically, *snāna* possesses a recognized Sanskrit phonological variant containing an epenthetic dental stop: **స్త్నాన** (*stnāna*). Under Saṁyukta Yati rules on the cluster `స్త్నా` (`స్ + త్ + న్ + ఆ`), the internal dental consonant `త్` is a legal constituent, licensing `తా`.  
* **Canonical Attestations for `తా` Matching:**  
* *Bhāgavatamu* (7-115): `స్నా - త్ప/త` (*snānamahimaṁbu \- tātparya*).  
* *Palnāṭi Vīracaritramu* (2715): `స్నా - త` (*snānamul cēsiyu \- tama pēru*).  
* *Bhāgavatamu* (8-269): `త - స్నా` (*taruṇiki maṅgaḷasnānaṁbu*).  
* *Lakṣaṇasāra Saṅgrahamu* (citations from *Viṣṇubhajanānandamu* and *Matsya Purāṇamu*): `స్త్నా - త` (*stnānaṁbu \- tarpaṇaṁbu*; *stnānaṁbu dīrci \- dhavutamulaina*).  
* *Paṇḍitārādhya Caritra*: `ధా - స్నా/తా` (*dhārāmbuvula \- kṛtasnānulai* via Vargaja Yati).  
* *Haravilāsamu* (2-37): `స్నా/తా - ధా` (*maṅgaḷasnānamu cēsi \- dhavuta* via Vargaja Yati).

---

### Āgama (Augment) Sandhi Invariants

In Dravidian augments (*āgamamulu*), an epenthetic consonant attaches between compounding stems. Unlike *rugāgama* (which Appakavi explicitly elevated to Ubhaya Yati under *Rāgama Sandhi Yati*), all other augments enforce **strict Svara-pradhāna (Acchu) Yati**; the surface augment consonant **never** participates in Hal Yati.

Morphological Sandhi Input:

  \[Pūrva Pada\]  \+  \[Āgama Consonant\]  \+  \[Uttara Pada (Vowel-Initial)\]

                           │

                           ▼

                  SURFACE AUGMENT NODE

         (టుగాగమ 'ట' / నుగాగమ 'న' / ఆరగాగమ 'ఆ')

                           │

         ┌─────────────────┴─────────────────┐

         ▼                                   ▼

   ACCHU YATI (Target: Base Vowel)     HAL YATI (Target: Consonant)

       \===\> CANONICAL & REQUIRED \<===     \===\> STRICTLY DISQUALIFIED \<===

&nbsp;

* **1\. Ṭugāgama (టుగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Sandhi-28 (*karmadhārayambunand-uttunak-accu paraṁbagunapuḍu ṭugāgamaṁbagu*); Sandhi-29 (*pērvādi śabdambulaku*).  
* *Process:* `ట్` is inserted before the second vowel (*karaku \+ accu $\\to$ karaku-ṭ-ammu*; *cūru \+ āku $\\to$ cūru-ṭ-āku*).  
* *Engine Matching:* **Must match the root initial vowel of the second stem.** Matching consonant `ట` is an engine failure.  
* *Attestations:* *Bhāskara Rāmāyaṇamu* (`ఐ - అ` in *puvvuṭammula*); *Śṛṅgāra Śākuntalamu* (`ఏ - యి` in *vēlpuṭēlikalu*); *Bhāgavatamu* (`ఊ - ఓ` in *jīvanapuṭōlamunan*).  
* **2\. Nugāgama (నుగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Sandhi-34 (Ṣaṣṭhī compounds of u/ṛ stems); Tatsama-29, 30 (*andu* case suffix); Sandhi-33 (taddharmārtha u-ending participles).  
* *Process:* `న్` is inserted (*viṣṇu \+ ājña $\\to$ viṣṇun-ājña*; *kalaśambu \+ andu $\\to$ kalaśambun-andu*; *tirugu \+ aṭṭi $\\to$ tirugun-aṭṭi*).  
* *Engine Matching:* **Must match the base initial vowel of the second morpheme (`ఆ`, `అ`, `ఇ`).** Never matches consonant `న`.  
* *Attestations:* *Bhāgavatamu* (`అ - ఆ` in *viṣṇunājña*); *Mahābhāratamu* (`ఆ - ఆ` in *jamunākṛti*); *Mahābhāratamu* (`ఇ - ఇ` in *vallabhuniṣṭamunakun*); *Āmuktamālyada* (`అ - అ` in *kalaśambunandu*); *Mahābhāratamu* (`హ - అ` in *tirugunaṭṭi*).  
* **3\. Āragāgama (ఆరగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Tatsama-36, 37 (Vocative plural marker *\-āra* attaching to stems: *asuralāra*, *kapulāra*, *surōttamulāra*).  
* *Engine Matching:* **Must match the augment's initial vowel `ఆ`.** Never matches liquid `ర` or preceding lateral `ల` (`ల-ర` matching is an engine error).  
* *Attestations:* *Mārkaṇḍēya Purāṇamu* (`ఆ - అ` in *asuralāra*); *Śrīkālahastīśvara Māhātmyamu* (`అ - ఆ` in *surōttamulāra*); *Molla Rāmāyaṇamu* (`అ - ఆ` in *kapulāra*).

---

### Dvirukta Ṭa-kāra & \-Eḍi / \-Eḍu Suffix Logic

**Dvirukta Ṭa-kāra Invariant (ద్విరుక్త టకారము)**

* *Grammatical Rule:* *Bāla Vyākaraṇamu*, Sandhi-12 (*kuṟu, ciṟu, kaḍu, niḍu, naḍu* roots undergo geminate retroflex stop substitution when followed by vowels: *kaḍu \+ aluka $\\to$ kaṭṭaluka*; *kaḍu \+ eduru $\\to$ kaṭṭeduru*; *niḍu \+ ūrupu $\\to$ niṭṭūrupu*; *naḍu \+ illu $\\to$ naṭṭillu*).  
* *Phonological Reality:* The morphological resolution is $kaḍu \+ eduru \\to kaṭṭ \+ u \+ eduru \\to kaṭṭeduru$ via regular Utva Sandhi.  
* *Engine Rule:* **Must match the base initial vowel of the second stem via Svara-pradhāna Yati.** The surface geminate consonant `ట్ట` is disqualified from Hal Yati.  
* *Attestations:* *kaṭṭalukan* matching `అ - అ`; *kaṭṭāyitaṁbu* matching `అ - ఆ`; *kaṭṭāṇi* matching `ఆ - ఆ`; *naṭṭenḍal* matching `ఇ - ఎ`; *kaṭṭedura* matching `ఎ - ఇ`; *niṭṭūrpu* matching `ఉ - ఊ` and `ఊ - ఉ`.

**Taddharmārtha Suffixes \-Eḍi / \-Eḍu (-ఎడి, \-ఎడు ప్రత్యయములు)**

* *Grammatical Rule:* *Bāla Vyākaraṇamu*, Kriyā-44 (Adjectival agentive suffixes *\-eḍi, \-eḍu* attaching to verb bases: *paluku \+ eḍu $\\to$ palikeḍu*; *undu \+ eḍu $\\to$ undeḍu*; *cēyu \+ eḍi $\\to$ cēseḍi*).  
* *Engine Rule:* Unlike nominal sandhi where vowel yati is primary, verbal forms bearing *\-eḍi / \-eḍu* **exclusively license Consonant (Hal) Yati on the fused syllable**. The engine evaluates the surface consonant (`కె, డె, లె, గె`); extracting underlying vowel `ఎ` is invalid.  
* *Attestations:* *palikeḍu* matching `కి - కి` via Prāṇi Yati; *olkeḍu* matching `లె - లీ` via Prāṇi Yati; *pōreḍu* matching `రె - రె` via Ēkāntara Yati; *undeḍu* matching `డె - డె` and `డె - డే` via Prāṇi Yati; *vardhileḍu* matching `లీ - లె` via Prāṇi Yati; *celaṅgeḍu* matching `గీ - గె` via Prāṇi Yati.

---

### Akhaṇḍa Yati Rejection Engine Architecture (అఖండ యతి నిషేధము)

**Akhaṇḍa Yati (అఖండ యతి)** occurs when a poet ignores the fundamental Svara-pradhāna rule across an obvious vowel sandhi juncture, treating two distinct compound words as an indivisible whole (*akhaṇḍamu*) to rhyme on the **fused surface consonant** instead of the second stem's initial vowel.

* *Examples of the Violation:*  
* *vēda \+ artha \= vēdārtha* $\\to$ rhyming on `దా` (Hal Yati) instead of base vowel `అ`.  
* *parama \+ īśvara \= paramēśvara* $\\to$ rhyming on `మే` (Hal Yati) instead of base vowel `ఈ`.  
* *catura \+ ukti \= caturōkti* $\\to$ rhyming on `రో` (Hal Yati) instead of base vowel `ఉ`.  
* *telupucu(n) \+ uṇḍa \= telupucuṇḍa* $\\to$ rhyming `చు - సొ` (Hal Yati) instead of base vowel `ఉ`.  
* *kavi \+ indra \= kavīndra* $\\to$ rhyming `వె - వీ` (Hal Yati) instead of base vowel `ఇ`.  
* *vīṇe yēmayye(n) tēv-iccaṭikini* $\\to$ rhyming `వీ - వీ` (Hal Yati) instead of base vowel `ఇ`.  
* *nīvu \+ ārōhiṁpumu \= nīvārōhiṁpumu* $\\to$ rhyming `వా - వా` (Hal Yati) instead of base vowel `ఆ`.  
* **Engine Rule & Verdict:**  
* Strictly Prohibited & Flagged as Defective (*Agrāhyamu / Kavi-prāmādikamu*).  
* Appakavi completely rejected Akhaṇḍa Yati. Although late medieval commentators (such as Kūcimanci Vēṅkaṭarāya in *Sukavi Manōran̄janamu*) collected sporadic classical attestations to rationalize it, textual criticism proves these are scribal corruptions (*lēkhana-pramādamulu*), poet oversights during compositional flow (*sthālityamulu*), or misclassified Nitya Samāsas.  
* In genuine classical kāvya, Svara-pradhāna Yati outnumbers Akhaṇḍa Yati by thousands to one. The engine must mandate **Svara-pradhāna Yati** on all transparent sandhi junctures and flag Akhaṇḍa Yati attempts as prosodic errors.

---

### Grand Taxonomy: Yati-Bhēdālu vs. Yati-Vidhānamulu

The treatise establishes a macro-architectural division synthesizing all Telugu yati mechanics into two mutually exclusive system layers:

                                TELUGU YATI ENGINE

                                        │

             ┌──────────────────────────┴──────────────────────────┐

             ▼                                                     ▼

     YATI-BHĒDĀLU (యతిభేదములు)                            YATI-VIDHĀNAMULU (యతివిధానములు)

 \[Phonological Alliances & Equivalence\]                 \[Structural, Positional & Morphological\]

 "WHICH characters are eligible to match?"             "HOW & WHERE in the word is matching applied?"

             │                                                     │

 ├── Svara-maitrī Yati (6.2.1)                         ├── Svara-pradhāna Yati (6.3)

 ├── Ṛ-yati (6.5)                                      ├── Lupta-visargaka Svara Yati (6.4)

 ├── Prāṇi Yati (6.10)                                 ├── Ṛtva-sambandha / Ṛtva-sāmya (6.6, 6.7)

 ├── Vargaja Yati (6.11)                               ├── Vṛddhi Yati (6.8)

 ├── Bindu Yati (6.12)                                 ├── Saṁyukta Yati (6.26 \- 6.29)

 ├── Anusvāra-sambandha Yati (6.15)                    ├── Bahu-yati Niyati (6.30)

 ├── Ṛju Yati (6.16)                                   ├── Antyōṣma-sandhi Yati (6.34)

 ├── Sarasa Yati (6.17, 6.18, 6.20)                    ├── Vikalpa Yati (6.35)

 ├── Ūṣma Yati (6.19)                                  ├── Prāsa Yati (6.53)

 ├── Abhēda / Abhēda-varga (6.21, 6.22, 6.23)          ├── Nitya Sandhi Yati (6.57)

 ├── Mu-vibhakti / Mu-kāra Yati (6.24, 6.25)           ├── Matubādēśa Yati (6.64)

 ├── Tadhbava-vyāja Yati (6.31)                        ├── Ēvārthaka Rules (6.66)

 ├── Viśēṣa Yati (6.32)                                ├── Snāna Yati (6.74)

 ├── Ma-varṇa Yati (6.33)                              ├── Āgama Sandhi Rules (6.75)

 ├── Ēkāntara / Ēkatara Yati (6.37, 6.38)              ├── Dvirukta Ṭa-kāra Rules (6.76)

 ├── ఌ-kāra Yati (6.54)                                └── \-Eḍi / \-Eḍu Suffix Rules (6.77)

 ├── Ra-La & Ra-Ḷa Yati (6.55)                                     │

 ├── La-Ḍa & Ḷa-Ḍa Abhēda (6.58)                       └── ALL UBHAYA YATI CLASSES:

 ├── Da-Ḍa Sāvarṇya Yati (6.59)                              ├── Bhinna Yati (6.40)

 └── Mu-Vu Yati (6.63)                                       ├── Nitya Yati (6.41)

                                                             ├── Vibhāga Yati (6.42)

                                                             ├── Yuṣmad-Asmad Yati (6.43)

                                                             ├── Kāku-svara Yati (6.44)

                                                             ├── Pluta-yuga Yati (6.45)

                                                             ├── Pararūpa Yati (6.46)

                                                             ├── Prādi Yati (6.47)

                                                             ├── Nitya Samāsa Yati (6.48)

                                                             ├── Dēśya Nitya Samāsa Yati (6.49)

                                                             ├── Nāmākhaṇḍa / Prabhu (6.50)

                                                             ├── Rāgama Sandhi Yati (6.51)

                                                             └── Caturthī Vibhakti Yati (6.56)

&nbsp;

---

### Provenance Trail

* **Grammatical Treatises & Sūtras:**  
* *Bāla Vyākaraṇamu* (Paravastu Cinnaya Sūri):  
* Sandhi-12: *Dvirukta ṭa-kāra sandhi* (*kuṟu, ciṟu, kaḍu, niḍu, naḍu*).  
* Sandhi-28, 29: *Ṭugāgama sūtras* (Karmadhāraya and *pērvādi* stems).  
* Sandhi-33, 34 & Tatsama-29, 30: *Nugāgama sūtras* (Ṣaṣṭhī compounds, *andu* marker, taddharmārtha participles).  
* Tatsama-36, 37: *Āragāgama sūtras* (Vocative plural inflection).  
* Kriyā-44: *Tṛ-varṇakārthambunand-eḍi-yeḍu vanniyalagu* (Agentive participles).  
* **Prosodic Authorities & Treatises:**  
* *Lakṣaṇasāra Saṅgrahamu* (Citrakavi Peddana / Kūcimanci Timmakavi): 2-160–162 defining and establishing *Snāna* yati on `తా`.  
* *Sukavi Manōran̄janamu* (Kūcimanci Vēṅkaṭarāya): Detailed historical surveys of *Akhaṇḍa Yati* and augment exceptions.  
* *Appakavīyamu*: Codification of *Rāgama Sandhi Yati* (3-215) and total rejection of *Akhaṇḍa Yati*.  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (6-101) *nugāgama*, (7-5) *nugāgama*, (8-40) *palikeḍu*.  
* *Sabhā Parva:* (2-237) *nugāgama*.  
* *Vana (Āraṇya) Parva:* (3-355) *nugāgama*, (5-172) *niṭṭūrpulu*.  
* *Virāṭa Parva:* (2-188) *vēlpuṭēlikalu*.  
* *Udyōga Parva:* (2-5-193) *nugāgama*.  
* *Drōṇa Parva:* (3-131) *olkeḍu / pōreḍu*.  
* *Śānti Parva:* (4-175) *tirugunaṭṭi*, (5-523) *snānaṁbulan* (`స్నా - న`).  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (3-783) *viṣṇunājña*, (4-86) *snānamāḍene* (`స్నా - స`), (5-152) *snānānukrama* (`స్నా - స`), (7-115) *snānamahimaṁbu* (`స్నా - త`), (8-67) *jīvanapuṭōlamunan*, (8-269) *maṅgaḷasnānaṁbu* (`త - స్నా`), (10-uttara-1701) *Akhaṇḍa Yati citation*.  
* *Haravilāsamu* (Śrīnātha): (2-37) *maṅgaḷasnānamu* (`స్నా/తా - ధా`).  
* *Paṇḍitārādhya Caritra* (Pālkuriki Sōmanātha): *dhārāmbuvula kṛtasnānulai* (`ధా - స్నా/తా`).  
* *Palnāṭi Vīracaritramu* (Śrīnātha): (line 2715\) *snānamul cēsiyu* (`స్నా - త`).  
* *Āmuktamālyada* (Śrīkṛṣṇadēvarāya): (1-4) *nugāgama*, (5-87) *kaṭṭāṇi*, (5-89) *snānīya* (`స్నా - జ`).  
* *Bhāskara Rāmāyaṇamu*: Bāla (228) *kaṭṭalukan*, Yuddha (1276) *Akhaṇḍa Yati citation*.  
* *Molla Rāmāyaṇamu*: Yuddha (2-86) *kapulāra*, Sundara (95, 140\) *Akhaṇḍa Yati citations*.  
* *Rāmāyaña Kalpavṛkṣamu* (Viśvanātha Satyanārāyaṇa): Bāla (29, 38), Ayōdhyā (250, 446, 506\) *Akhaṇḍa Yati attestations*.

&nbsp;

&nbsp;

&nbsp;

&nbsp;

**Yati Engine Rules & Architectural Specification (Part 20\)**

---

### ‘స్నాన' (Snāna) Special Yati Rule

In classical prosody, the Sanskrit loanword **స్నాన** (*snāna*) exhibits an exceptional three-way consonant matching behavior at its conjunct node `స్నా` (*snā*):

$$\\mathbf{స్నాన} \\implies \\text{Eligible Match Targets at } \\mathbf{స్నా}: \\quad {\\mathbf{స}, \\mathbf{న}, \\mathbf{త}}$$

* **Surface Saṁyukta Yati (Standard):** The surface cluster `స్నా` splits per standard Saṁyukta Yati rules into `స` or `న`:  
* *Matching `స`:* `స్నా - సం` (*snānamāḍene \- sandhyana*), `స్నా - సాం` (*snānānukrama \- sāndrāmbuvul*), `స్నా - జం` (*snānīya \- vastuvrajaṁbu* via Sarasa Yati).  
* *Matching `న`:* `స్నా - నం` (*snānaṁbulana \- tirthadānaṁbula*), `స్నా - న` (*snānamonarsi \- śubhravasanaṁbula*).  
* **The Exceptional Dental (`త`) Target License:**  
* Kūcimanci Timmakavi (*Lakṣaṇasāra Saṅgrahamu*) codifies that `స్నా` additionally matches dental `త` (*ta / tā*) or aspirated/voiced dental cognates (`ధ / ధా` via Vargaja Yati).  
* *Morphological Foundations:*  
1. **Tadbhavīkāra Perspective:** The Telugu tadbhava of *snānamu* is *tānamu*. Poets mentally invoke the native *tānamu* root even when writing the formal Tatsama *snāna*, matching `తా`.  
2. **Sanskrit Stnā Alternative Form:** Grammatically, *snāna* possesses a recognized Sanskrit phonological variant containing an epenthetic dental stop: **స్త్నాన** (*stnāna*). Under Saṁyukta Yati rules on the cluster `స్త్నా` (`స్ + త్ + న్ + ఆ`), the internal dental consonant `త్` is a legal constituent, licensing `తా`.  
* **Canonical Attestations for `తా` Matching:**  
* *Bhāgavatamu* (7-115): `స్నా - త్ప/త` (*snānamahimaṁbu \- tātparya*).  
* *Palnāṭi Vīracaritramu* (2715): `స్నా - త` (*snānamul cēsiyu \- tama pēru*).  
* *Bhāgavatamu* (8-269): `త - స్నా` (*taruṇiki maṅgaḷasnānaṁbu*).  
* *Lakṣaṇasāra Saṅgrahamu* (citations from *Viṣṇubhajanānandamu* and *Matsya Purāṇamu*): `స్త్నా - త` (*stnānaṁbu \- tarpaṇaṁbu*; *stnānaṁbu dīrci \- dhavutamulaina*).  
* *Paṇḍitārādhya Caritra*: `ధా - స్నా/తా` (*dhārāmbuvula \- kṛtasnānulai* via Vargaja Yati).  
* *Haravilāsamu* (2-37): `స్నా/తా - ధా` (*maṅgaḷasnānamu cēsi \- dhavuta* via Vargaja Yati).

---

### Āgama (Augment) Sandhi Invariants

In Dravidian augments (*āgamamulu*), an epenthetic consonant attaches between compounding stems. Unlike *rugāgama* (which Appakavi explicitly elevated to Ubhaya Yati under *Rāgama Sandhi Yati*), all other augments enforce **strict Svara-pradhāna (Acchu) Yati**; the surface augment consonant **never** participates in Hal Yati.

Morphological Sandhi Input:

  \[Pūrva Pada\]  \+  \[Āgama Consonant\]  \+  \[Uttara Pada (Vowel-Initial)\]

                           │

                           ▼

                  SURFACE AUGMENT NODE

         (టుగాగమ 'ట' / నుగాగమ 'న' / ఆరగాగమ 'ఆ')

                           │

         ┌─────────────────┴─────────────────┐

         ▼                                   ▼

   ACCHU YATI (Target: Base Vowel)     HAL YATI (Target: Consonant)

       \===\> CANONICAL & REQUIRED \<===     \===\> STRICTLY DISQUALIFIED \<===

&nbsp;

* **1\. Ṭugāgama (టుగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Sandhi-28 (*karmadhārayambunand-uttunak-accu paraṁbagunapuḍu ṭugāgamaṁbagu*); Sandhi-29 (*pērvādi śabdambulaku*).  
* *Process:* `ట్` is inserted before the second vowel (*karaku \+ accu $\\to$ karaku-ṭ-ammu*; *cūru \+ āku $\\to$ cūru-ṭ-āku*).  
* *Engine Matching:* **Must match the root initial vowel of the second stem.** Matching consonant `ట` is an engine failure.  
* *Attestations:* *Bhāskara Rāmāyaṇamu* (`ఐ - అ` in *puvvuṭammula*); *Śṛṅgāra Śākuntalamu* (`ఏ - యి` in *vēlpuṭēlikalu*); *Bhāgavatamu* (`ఊ - ఓ` in *jīvanapuṭōlamunan*).  
* **2\. Nugāgama (నుగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Sandhi-34 (Ṣaṣṭhī compounds of u/ṛ stems); Tatsama-29, 30 (*andu* case suffix); Sandhi-33 (taddharmārtha u-ending participles).  
* *Process:* `న్` is inserted (*viṣṇu \+ ājña $\\to$ viṣṇun-ājña*; *kalaśambu \+ andu $\\to$ kalaśambun-andu*; *tirugu \+ aṭṭi $\\to$ tirugun-aṭṭi*).  
* *Engine Matching:* **Must match the base initial vowel of the second morpheme (`ఆ`, `అ`, `ఇ`).** Never matches consonant `న`.  
* *Attestations:* *Bhāgavatamu* (`అ - ఆ` in *viṣṇunājña*); *Mahābhāratamu* (`ఆ - ఆ` in *jamunākṛti*); *Mahābhāratamu* (`ఇ - ఇ` in *vallabhuniṣṭamunakun*); *Āmuktamālyada* (`అ - అ` in *kalaśambunandu*); *Mahābhāratamu* (`హ - అ` in *tirugunaṭṭi*).  
* **3\. Āragāgama (ఆరగాగమము):**  
* *Sūtras:* *Bāla Vyākaraṇamu*, Tatsama-36, 37 (Vocative plural marker *\-āra* attaching to stems: *asuralāra*, *kapulāra*, *surōttamulāra*).  
* *Engine Matching:* **Must match the augment's initial vowel `ఆ`.** Never matches liquid `ర` or preceding lateral `ల` (`ల-ర` matching is an engine error).  
* *Attestations:* *Mārkaṇḍēya Purāṇamu* (`ఆ - అ` in *asuralāra*); *Śrīkālahastīśvara Māhātmyamu* (`అ - ఆ` in *surōttamulāra*); *Molla Rāmāyaṇamu* (`అ - ఆ` in *kapulāra*).

---

### Dvirukta Ṭa-kāra & \-Eḍi / \-Eḍu Suffix Logic

**Dvirukta Ṭa-kāra Invariant (ద్విరుక్త టకారము)**

* *Grammatical Rule:* *Bāla Vyākaraṇamu*, Sandhi-12 (*kuṟu, ciṟu, kaḍu, niḍu, naḍu* roots undergo geminate retroflex stop substitution when followed by vowels: *kaḍu \+ aluka $\\to$ kaṭṭaluka*; *kaḍu \+ eduru $\\to$ kaṭṭeduru*; *niḍu \+ ūrupu $\\to$ niṭṭūrupu*; *naḍu \+ illu $\\to$ naṭṭillu*).  
* *Phonological Reality:* The morphological resolution is $kaḍu \+ eduru \\to kaṭṭ \+ u \+ eduru \\to kaṭṭeduru$ via regular Utva Sandhi.  
* *Engine Rule:* **Must match the base initial vowel of the second stem via Svara-pradhāna Yati.** The surface geminate consonant `ట్ట` is disqualified from Hal Yati.  
* *Attestations:* *kaṭṭalukan* matching `అ - అ`; *kaṭṭāyitaṁbu* matching `అ - ఆ`; *kaṭṭāṇi* matching `ఆ - ఆ`; *naṭṭenḍal* matching `ఇ - ఎ`; *kaṭṭedura* matching `ఎ - ఇ`; *niṭṭūrpu* matching `ఉ - ఊ` and `ఊ - ఉ`.

**Taddharmārtha Suffixes \-Eḍi / \-Eḍu (-ఎడి, \-ఎడు ప్రత్యయములు)**

* *Grammatical Rule:* *Bāla Vyākaraṇamu*, Kriyā-44 (Adjectival agentive suffixes *\-eḍi, \-eḍu* attaching to verb bases: *paluku \+ eḍu $\\to$ palikeḍu*; *undu \+ eḍu $\\to$ undeḍu*; *cēyu \+ eḍi $\\to$ cēseḍi*).  
* *Engine Rule:* Unlike nominal sandhi where vowel yati is primary, verbal forms bearing *\-eḍi / \-eḍu* **exclusively license Consonant (Hal) Yati on the fused syllable**. The engine evaluates the surface consonant (`కె, డె, లె, గె`); extracting underlying vowel `ఎ` is invalid.  
* *Attestations:* *palikeḍu* matching `కి - కి` via Prāṇi Yati; *olkeḍu* matching `లె - లీ` via Prāṇi Yati; *pōreḍu* matching `రె - రె` via Ēkāntara Yati; *undeḍu* matching `డె - డె` and `డె - డే` via Prāṇi Yati; *vardhileḍu* matching `లీ - లె` via Prāṇi Yati; *celaṅgeḍu* matching `గీ - గె` via Prāṇi Yati.

---

### Akhaṇḍa Yati Rejection Engine Architecture (అఖండ యతి నిషేధము)

**Akhaṇḍa Yati (అఖండ యతి)** occurs when a poet ignores the fundamental Svara-pradhāna rule across an obvious vowel sandhi juncture, treating two distinct compound words as an indivisible whole (*akhaṇḍamu*) to rhyme on the **fused surface consonant** instead of the second stem's initial vowel.

* *Examples of the Violation:*  
* *vēda \+ artha \= vēdārtha* $\\to$ rhyming on `దా` (Hal Yati) instead of base vowel `అ`.  
* *parama \+ īśvara \= paramēśvara* $\\to$ rhyming on `మే` (Hal Yati) instead of base vowel `ఈ`.  
* *catura \+ ukti \= caturōkti* $\\to$ rhyming on `రో` (Hal Yati) instead of base vowel `ఉ`.  
* *telupucu(n) \+ uṇḍa \= telupucuṇḍa* $\\to$ rhyming `చు - సొ` (Hal Yati) instead of base vowel `ఉ`.  
* *kavi \+ indra \= kavīndra* $\\to$ rhyming `వె - వీ` (Hal Yati) instead of base vowel `ఇ`.  
* *vīṇe yēmayye(n) tēv-iccaṭikini* $\\to$ rhyming `వీ - వీ` (Hal Yati) instead of base vowel `ఇ`.  
* *nīvu \+ ārōhiṁpumu \= nīvārōhiṁpumu* $\\to$ rhyming `వా - వా` (Hal Yati) instead of base vowel `ఆ`.  
* **Engine Rule & Verdict:**  
* Strictly Prohibited & Flagged as Defective (*Agrāhyamu / Kavi-prāmādikamu*).  
* Appakavi completely rejected Akhaṇḍa Yati. Although late medieval commentators (such as Kūcimanci Vēṅkaṭarāya in *Sukavi Manōran̄janamu*) collected sporadic classical attestations to rationalize it, textual criticism proves these are scribal corruptions (*lēkhana-pramādamulu*), poet oversights during compositional flow (*sthālityamulu*), or misclassified Nitya Samāsas.  
* In genuine classical kāvya, Svara-pradhāna Yati outnumbers Akhaṇḍa Yati by thousands to one. The engine must mandate **Svara-pradhāna Yati** on all transparent sandhi junctures and flag Akhaṇḍa Yati attempts as prosodic errors.

---

### Grand Taxonomy: Yati-Bhēdālu vs. Yati-Vidhānamulu

The treatise establishes a macro-architectural division synthesizing all Telugu yati mechanics into two mutually exclusive system layers:

                                TELUGU YATI ENGINE

                                        │

             ┌──────────────────────────┴──────────────────────────┐

             ▼                                                     ▼

     YATI-BHĒDĀLU (యతిభేదములు)                            YATI-VIDHĀNAMULU (యతివిధానములు)

 \[Phonological Alliances & Equivalence\]                 \[Structural, Positional & Morphological\]

 "WHICH characters are eligible to match?"             "HOW & WHERE in the word is matching applied?"

             │                                                     │

 ├── Svara-maitrī Yati (6.2.1)                         ├── Svara-pradhāna Yati (6.3)

 ├── Ṛ-yati (6.5)                                      ├── Lupta-visargaka Svara Yati (6.4)

 ├── Prāṇi Yati (6.10)                                 ├── Ṛtva-sambandha / Ṛtva-sāmya (6.6, 6.7)

 ├── Vargaja Yati (6.11)                               ├── Vṛddhi Yati (6.8)

 ├── Bindu Yati (6.12)                                 ├── Saṁyukta Yati (6.26 \- 6.29)

 ├── Anusvāra-sambandha Yati (6.15)                    ├── Bahu-yati Niyati (6.30)

 ├── Ṛju Yati (6.16)                                   ├── Antyōṣma-sandhi Yati (6.34)

 ├── Sarasa Yati (6.17, 6.18, 6.20)                    ├── Vikalpa Yati (6.35)

 ├── Ūṣma Yati (6.19)                                  ├── Prāsa Yati (6.53)

 ├── Abhēda / Abhēda-varga (6.21, 6.22, 6.23)          ├── Nitya Sandhi Yati (6.57)

 ├── Mu-vibhakti / Mu-kāra Yati (6.24, 6.25)           ├── Matubādēśa Yati (6.64)

 ├── Tadhbava-vyāja Yati (6.31)                        ├── Ēvārthaka Rules (6.66)

 ├── Viśēṣa Yati (6.32)                                ├── Snāna Yati (6.74)

 ├── Ma-varṇa Yati (6.33)                              ├── Āgama Sandhi Rules (6.75)

 ├── Ēkāntara / Ēkatara Yati (6.37, 6.38)              ├── Dvirukta Ṭa-kāra Rules (6.76)

 ├── ఌ-kāra Yati (6.54)                                └── \-Eḍi / \-Eḍu Suffix Rules (6.77)

 ├── Ra-La & Ra-Ḷa Yati (6.55)                                     │

 ├── La-Ḍa & Ḷa-Ḍa Abhēda (6.58)                       └── ALL UBHAYA YATI CLASSES:

 ├── Da-Ḍa Sāvarṇya Yati (6.59)                              ├── Bhinna Yati (6.40)

 └── Mu-Vu Yati (6.63)                                       ├── Nitya Yati (6.41)

                                                             ├── Vibhāga Yati (6.42)

                                                             ├── Yuṣmad-Asmad Yati (6.43)

                                                             ├── Kāku-svara Yati (6.44)

                                                             ├── Pluta-yuga Yati (6.45)

                                                             ├── Pararūpa Yati (6.46)

                                                             ├── Prādi Yati (6.47)

                                                             ├── Nitya Samāsa Yati (6.48)

                                                             ├── Dēśya Nitya Samāsa Yati (6.49)

                                                             ├── Nāmākhaṇḍa / Prabhu (6.50)

                                                             ├── Rāgama Sandhi Yati (6.51)

                                                             └── Caturthī Vibhakti Yati (6.56)

&nbsp;

---

### Provenance Trail

* **Grammatical Treatises & Sūtras:**  
* *Bāla Vyākaraṇamu* (Paravastu Cinnaya Sūri):  
* Sandhi-12: *Dvirukta ṭa-kāra sandhi* (*kuṟu, ciṟu, kaḍu, niḍu, naḍu*).  
* Sandhi-28, 29: *Ṭugāgama sūtras* (Karmadhāraya and *pērvādi* stems).  
* Sandhi-33, 34 & Tatsama-29, 30: *Nugāgama sūtras* (Ṣaṣṭhī compounds, *andu* marker, taddharmārtha participles).  
* Tatsama-36, 37: *Āragāgama sūtras* (Vocative plural inflection).  
* Kriyā-44: *Tṛ-varṇakārthambunand-eḍi-yeḍu vanniyalagu* (Agentive participles).  
* **Prosodic Authorities & Treatises:**  
* *Lakṣaṇasāra Saṅgrahamu* (Citrakavi Peddana / Kūcimanci Timmakavi): 2-160–162 defining and establishing *Snāna* yati on `తా`.  
* *Sukavi Manōran̄janamu* (Kūcimanci Vēṅkaṭarāya): Detailed historical surveys of *Akhaṇḍa Yati* and augment exceptions.  
* *Appakavīyamu*: Codification of *Rāgama Sandhi Yati* (3-215) and total rejection of *Akhaṇḍa Yati*.  
* **Classical Literature Citations:**  
* *Andhra Mahābhāratamu* (Nannaya, Tikkana, Errapragada):  
* *Ādi Parva:* (6-101) *nugāgama*, (7-5) *nugāgama*, (8-40) *palikeḍu*.  
* *Sabhā Parva:* (2-237) *nugāgama*.  
* *Vana (Āraṇya) Parva:* (3-355) *nugāgama*, (5-172) *niṭṭūrpulu*.  
* *Virāṭa Parva:* (2-188) *vēlpuṭēlikalu*.  
* *Udyōga Parva:* (2-5-193) *nugāgama*.  
* *Drōṇa Parva:* (3-131) *olkeḍu / pōreḍu*.  
* *Śānti Parva:* (4-175) *tirugunaṭṭi*, (5-523) *snānaṁbulan* (`స్నా - న`).  
* *Śrīmad Bhāgavatamu* (Pōtana et al.): (3-783) *viṣṇunājña*, (4-86) *snānamāḍene* (`స్నా - స`), (5-152) *snānānukrama* (`స్నా - స`), (7-115) *snānamahimaṁbu* (`స్నా - త`), (8-67) *jīvanapuṭōlamunan*, (8-269) *maṅgaḷasnānaṁbu* (`త - స్నా`), (10-uttara-1701) *Akhaṇḍa Yati citation*.  
* *Haravilāsamu* (Śrīnātha): (2-37) *maṅgaḷasnānamu* (`స్నా/తా - ధా`).  
* *Paṇḍitārādhya Caritra* (Pālkuriki Sōmanātha): *dhārāmbuvula kṛtasnānulai* (`ధా - స్నా/తా`).  
* *Palnāṭi Vīracaritramu* (Śrīnātha): (line 2715\) *snānamul cēsiyu* (`స్నా - త`).  
* *Āmuktamālyada* (Śrīkṛṣṇadēvarāya): (1-4) *nugāgama*, (5-87) *kaṭṭāṇi*, (5-89) *snānīya* (`స్నా - జ`).  
* *Bhāskara Rāmāyaṇamu*: Bāla (228) *kaṭṭalukan*, Yuddha (1276) *Akhaṇḍa Yati citation*.  
* *Molla Rāmāyaṇamu*: Yuddha (2-86) *kapulāra*, Sundara (95, 140\) *Akhaṇḍa Yati citations*.  
* *Rāmāyaña Kalpavṛkṣamu* (Viśvanātha Satyanārāyaṇa): Bāla (29, 38), Ayōdhyā (250, 446, 506\) *Akhaṇḍa Yati attestations*.

&nbsp;