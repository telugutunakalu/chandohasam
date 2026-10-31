# Grid checks and breakdowns

Written by `analyse_grid.py` from `grid_poems.jsonl`, the raw cell files and the prompt selection. Numbers only.

## 1. The prompts

100 prompts in 24 metres; 47 in the 7 common vṛttas whose line pattern the scorer checks, 53 in other metres (other fixed-pattern vṛttas among them). 56 are phase-1 poems of the human evaluation.

| source | prompts |
|---|---|
| Bhāgavatam | 50 |
| Kūcimañci | 20 |
| Vemana | 20 |
| Gemini | 10 |

| how the prompt was obtained | prompts |
|---|---|
| phase 1, Gemini bhāvam as is | 10 |
| phase 1, new P1 | 33 |
| phase 1, the 183 | 13 |
| pool → phase 2, new P1 | 23 |
| pool → phase 2, the 183 | 21 |

| metre | prompts |
|---|---|
| kandamu | 11 |
| ataveladi | 11 |
| mattebhavikriditamu | 10 |
| champakamala | 10 |
| tetagiti | 10 |
| utpalamala | 8 |
| mattakokilamu | 7 |
| sardulavikriditamu | 7 |
| malini | 4 |
| pamcacamaramu | 2 |
| layagrahi | 2 |
| sragdhara | 2 |
| utsahamu | 2 |
| sragvini | 2 |
| totakamu | 2 |
| madhuragati_ragada | 2 |
| indravajra | 1 |
| manini | 1 |
| upendravajra | 1 |
| layavibhati | 1 |
| mahasragdhara | 1 |
| seesamu | 1 |
| vanamayuramu | 1 |
| bhujangaprayatamu | 1 |

## 2. Integrity of every cell

Poems on the 100 prompts (34 for the extra strategies), from the raw files; `scored` = rows in grid_poems.jsonl.

| cell | poems | distinct prompts | duplicates | empty | scored | decoder end status |
|---|---|---|---|---|---|---|
| Nandi-Mini-150M · base · baseline | 100 | 100 | 0 | 0 | 100 | budget 92, eos 8 |
| Nandi-Mini-150M · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Nandi-Mini-150M · FT (bhāvam → poem) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Gemma-4 E4B-it · base · baseline | 100 | 100 | 0 | 0 | 100 | budget 1, eos 99 |
| Gemma-4 E4B-it · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Gemma-4 26B-A4B-it · base · baseline | 100 | 100 | 0 | 0 | 100 | budget 3, eos 97 |
| Gemma-4 26B-A4B-it · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 270M · base · baseline | 100 | 100 | 0 | 16 | 100 | budget 80, eos 20 |
| T5Gemma 2 270M · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 270M · FT (full) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| T5Gemma 2 270M · FT (full) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 1B · base · baseline | 100 | 100 | 0 | 19 | 100 | budget 66, eos 34 |
| T5Gemma 2 1B · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 1B · FT (full) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| T5Gemma 2 1B · FT (full) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 4B · base · baseline | 100 | 100 | 0 | 66 | 100 | budget 12, eos 88 |
| T5Gemma 2 4B · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 4B · FT (LoRA r 128) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | budget 1, complete 99 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · baseline | 100 | 100 | 0 | 0 | 100 | budget 1, eos 99 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 120M · base (pre-trained) · baseline | 100 | 100 | 0 | 0 | 100 | budget 100 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | budget 7, complete 93 |
| chandohasam MDLM 120M · FT (E6 + T1) · baseline | 100 | 100 | 0 | 0 | 100 | budget 2, eos 98 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 523M · base (pre-trained) · baseline | 100 | 100 | 0 | 0 | 100 | budget 91, eos 9 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | budget 15, complete 85 |
| chandohasam MDLM 523M · FT (E6 + T1) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | budget 1, complete 99 |
| DiffusionGemma 26B-A4B · base · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| DiffusionGemma 26B-A4B · base · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · baseline | 100 | 100 | 0 | 0 | 100 | eos 100 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Nandi-Mini-150M · base · masking_only | 34 | 34 | 0 | 0 | 34 | budget 1, complete 33 |
| Nandi-Mini-150M · base · hybrid | 34 | 34 | 0 | 0 | 34 | budget 4, complete 30 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_only | 34 | 34 | 0 | 0 | 34 | complete 34 |
| Nandi-Mini-150M · FT (bhāvam → poem) · hybrid | 34 | 34 | 0 | 0 | 34 | complete 34 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | 34 | 34 | 0 | 0 | 34 | budget 7, complete 27 |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | 34 | 34 | 0 | 0 | 34 | budget 3, complete 31 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_only | 34 | 34 | 0 | 0 | 34 | budget 2, complete 32 |
| chandohasam MDLM 523M · FT (E6 + T1) · hybrid | 34 | 34 | 0 | 0 | 34 | complete 34 |
| Nandi-Mini-150M · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Gemma-4 E4B-it · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| Gemma-4 26B-A4B-it · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 270M · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 270M · FT (full) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 1B · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 1B · FT (full) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 4B · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| DiffusionGemma 26B-A4B · base · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack · v2 A+B | 100 | 100 | 0 | 0 | 100 | complete 100 |

## 3. Constrained poems the scorer does not count as in metre

41 poems. The decoder's own verdicts at generation (strict) beside the scorer's.

| cell | prompt | end status | gaṇa | prāsa | yati | lines |
|---|---|---|---|---|---|---|
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-940-మస్ర. | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-876-మ. | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/kuchimanchi_timmakavi:kuchimanchi-28 | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/kuchimanchi_timmakavi:kuchimanchi-99 | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-739-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-1185-శా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-883-స్రగ్ద. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:6-272-స్రగ్ద. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-214-మాని. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:6-399-చ. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-940-మస్ర. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-739-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-1074-మ. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.2-627-మ. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:8-437-మ. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/kuchimanchi_timmakavi:kuchimanchi-87 | budget | False | True | True | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | gemini:poem_0051 | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:3-277-చ. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-1185-శా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | dataset/bhagavatam:10.1-1597-శా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack | dataset/bhagavatam:10.2-739-లగ్రా. | budget | False | False | False | 3 |
| Nandi-Mini-150M · base · masking_only | dataset/bhagavatam:10.1-214-మాని. | budget | False | False | False | 4 |
| Nandi-Mini-150M · base · hybrid | dataset/bhagavatam:6-272-స్రగ్ద. | budget | False | False | False | 4 |
| Nandi-Mini-150M · base · hybrid | dataset/bhagavatam:10.1-739-మత్త. | budget | False | False | False | 4 |
| Nandi-Mini-150M · base · hybrid | dataset/bhagavatam:6-399-చ. | budget | False | False | False | 4 |
| Nandi-Mini-150M · base · hybrid | dataset/kuchimanchi_timmakavi:kuchimanchi-1197 | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/kuchimanchi_timmakavi:kuchimanchi-28 | budget | False | True | True | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/bhagavatam:10.2-883-స్రగ్ద. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/bhagavatam:6-272-స్రగ్ద. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/kuchimanchi_timmakavi:kuchimanchi-99 | budget | False | False | False | 3 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/bhagavatam:10.2-940-మస్ర. | budget | False | False | False | 3 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/bhagavatam:10.2-739-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | dataset/kuchimanchi_timmakavi:kuchimanchi-99 | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | dataset/bhagavatam:10.2-940-మస్ర. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_only | dataset/bhagavatam:10.1-214-మాని. | budget | False | False | False | 4 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_only | dataset/bhagavatam:6-385-లగ్రా. | budget | False | False | False | 4 |

## 4. By source

In metre % / real words % / recognised % per group (n poems in the header).

| cell | Bhāgavatam (n 50) | Vemana (n 20) | Kūcimañci (n 20) | Gemini (n 10) |
|---|---|---|---|---|
| gold (the source poems) | 34.0 / 81.4 / 58.0 | 80.0 / 95.4 / 80.0 | 50.0 / 82.1 / 50.0 | 100.0 / 95.0 / 80.0 |
| Nandi-Mini-150M · base · baseline | 0.0 / 96.9 / 46.0 | 0.0 / 97.6 / 45.0 | 0.0 / 90.3 / 25.0 | 0.0 / 96.2 / 60.0 |
| Nandi-Mini-150M · base · masking_backtrack | 100.0 / 33.4 / 14.0 | 100.0 / 63.6 / 35.0 | 100.0 / 30.8 / 10.0 | 100.0 / 46.7 / 10.0 |
| Nandi-Mini-150M · FT (bhāvam → poem) · baseline | 4.0 / 75.3 / 60.0 | 15.0 / 94.0 / 70.0 | 0.0 / 75.9 / 60.0 | 0.0 / 87.7 / 90.0 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack | 100.0 / 68.7 / 56.0 | 100.0 / 87.2 / 90.0 | 100.0 / 61.8 / 50.0 | 100.0 / 89.0 / 80.0 |
| Gemma-4 E4B-it · base · baseline | 0.0 / 96.1 / 94.0 | 0.0 / 95.7 / 95.0 | 0.0 / 93.3 / 95.0 | 0.0 / 93.2 / 90.0 |
| Gemma-4 E4B-it · base · masking_backtrack | 100.0 / 33.0 / 52.0 | 100.0 / 68.6 / 80.0 | 100.0 / 37.1 / 50.0 | 100.0 / 43.3 / 80.0 |
| Gemma-4 26B-A4B-it · base · baseline | 0.0 / 97.6 / 92.0 | 0.0 / 97.6 / 95.0 | 0.0 / 94.5 / 90.0 | 0.0 / 96.6 / 90.0 |
| Gemma-4 26B-A4B-it · base · masking_backtrack | 100.0 / 41.2 / 52.0 | 100.0 / 79.2 / 80.0 | 100.0 / 50.8 / 65.0 | 100.0 / 64.9 / 80.0 |
| T5Gemma 2 270M · base · baseline | 0.0 / 84.9 / 30.0 | 0.0 / 88.2 / 35.0 | 0.0 / 79.4 / 40.0 | 0.0 / 85.0 / 30.0 |
| T5Gemma 2 270M · base · masking_backtrack | 100.0 / 32.8 / 18.0 | 100.0 / 60.1 / 55.0 | 100.0 / 34.1 / 20.0 | 100.0 / 37.6 / 10.0 |
| T5Gemma 2 270M · FT (full) · baseline | 8.0 / 74.5 / 72.0 | 10.0 / 94.6 / 85.0 | 5.0 / 75.0 / 65.0 | 10.0 / 83.1 / 90.0 |
| T5Gemma 2 270M · FT (full) · masking_backtrack | 100.0 / 69.7 / 58.0 | 100.0 / 91.3 / 75.0 | 100.0 / 69.1 / 55.0 | 100.0 / 83.4 / 90.0 |
| T5Gemma 2 1B · base · baseline | 0.0 / 93.4 / 44.0 | 0.0 / 76.8 / 25.0 | 0.0 / 88.8 / 45.0 | 0.0 / 93.7 / 20.0 |
| T5Gemma 2 1B · base · masking_backtrack | 100.0 / 29.5 / 32.0 | 100.0 / 61.9 / 30.0 | 100.0 / 37.6 / 30.0 | 100.0 / 44.4 / 30.0 |
| T5Gemma 2 1B · FT (full) · baseline | 2.0 / 77.1 / 70.0 | 20.0 / 93.9 / 85.0 | 5.0 / 83.4 / 70.0 | 20.0 / 87.6 / 90.0 |
| T5Gemma 2 1B · FT (full) · masking_backtrack | 100.0 / 65.9 / 60.0 | 100.0 / 92.5 / 95.0 | 100.0 / 74.2 / 45.0 | 100.0 / 78.3 / 80.0 |
| T5Gemma 2 4B · base · baseline | 0.0 / 95.5 / 30.0 | 0.0 / 96.7 / 20.0 | 0.0 / 93.2 / 30.0 | 0.0 / – / 10.0 |
| T5Gemma 2 4B · base · masking_backtrack | 100.0 / 26.8 / 22.0 | 100.0 / 59.8 / 25.0 | 100.0 / 37.6 / 55.0 | 100.0 / 51.4 / 10.0 |
| T5Gemma 2 4B · FT (LoRA r 128) · baseline | 0.0 / 77.8 / 70.0 | 20.0 / 91.5 / 75.0 | 10.0 / 78.1 / 65.0 | 10.0 / 77.5 / 80.0 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack | 98.0 / 62.8 / 56.0 | 100.0 / 93.6 / 85.0 | 100.0 / 72.4 / 45.0 | 100.0 / 81.4 / 90.0 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · baseline | 0.0 / 74.1 / 56.0 | 0.0 / 87.1 / 85.0 | 0.0 / 76.4 / 65.0 | 0.0 / 76.7 / 70.0 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack | 100.0 / 52.9 / 36.0 | 100.0 / 89.2 / 55.0 | 100.0 / 56.3 / 40.0 | 100.0 / 75.5 / 50.0 |
| chandohasam MDLM 120M · base (pre-trained) · baseline | 0.0 / 97.8 / 38.0 | 0.0 / 98.6 / 45.0 | 0.0 / 98.5 / 50.0 | 0.0 / 98.9 / 60.0 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | 90.0 / 48.7 / 18.0 | 100.0 / 87.7 / 15.0 | 90.0 / 50.7 / 20.0 | 100.0 / 59.9 / 40.0 |
| chandohasam MDLM 120M · FT (E6 + T1) · baseline | 0.0 / 90.0 / 82.0 | 0.0 / 96.6 / 90.0 | 0.0 / 89.0 / 75.0 | 0.0 / 95.1 / 90.0 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack | 100.0 / 70.3 / 66.0 | 100.0 / 94.4 / 90.0 | 100.0 / 74.0 / 60.0 | 100.0 / 89.3 / 100.0 |
| chandohasam MDLM 523M · base (pre-trained) · baseline | 0.0 / 99.1 / 50.0 | 0.0 / 99.5 / 65.0 | 0.0 / 97.2 / 35.0 | 0.0 / 98.3 / 0.0 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | 74.0 / 46.2 / 16.0 | 100.0 / 86.9 / 25.0 | 95.0 / 61.8 / 15.0 | 90.0 / 67.5 / 30.0 |
| chandohasam MDLM 523M · FT (E6 + T1) · baseline | 0.0 / 87.4 / 76.0 | 5.0 / 95.2 / 85.0 | 0.0 / 82.9 / 80.0 | 0.0 / 96.9 / 90.0 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack | 98.0 / 69.2 / 76.0 | 100.0 / 93.4 / 85.0 | 100.0 / 75.6 / 65.0 | 100.0 / 91.3 / 90.0 |
| DiffusionGemma 26B-A4B · base · baseline | 0.0 / 87.7 / 100.0 | 0.0 / 89.6 / 100.0 | 0.0 / 84.7 / 100.0 | 0.0 / 84.8 / 100.0 |
| DiffusionGemma 26B-A4B · base · masking_backtrack | 100.0 / 26.3 / 52.0 | 100.0 / 54.4 / 90.0 | 100.0 / 29.1 / 55.0 | 100.0 / 36.8 / 90.0 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · baseline | 0.0 / 74.7 / 84.0 | 0.0 / 92.6 / 100.0 | 0.0 / 74.0 / 90.0 | 0.0 / 90.8 / 100.0 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack | 100.0 / 22.6 / 38.0 | 100.0 / 52.4 / 60.0 | 100.0 / 23.4 / 45.0 | 100.0 / 31.6 / 70.0 |
| Nandi-Mini-150M · base · masking_backtrack · v2 A+B | 100.0 / 45.5 / 18.0 | 100.0 / 81.0 / 10.0 | 100.0 / 44.5 / 30.0 | 100.0 / 54.4 / 20.0 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack · v2 A+B | 100.0 / 75.5 / 62.0 | 100.0 / 90.5 / 75.0 | 100.0 / 71.1 / 40.0 | 100.0 / 90.4 / 70.0 |
| Gemma-4 E4B-it · base · masking_backtrack · v2 A+B | 100.0 / 38.3 / 58.0 | 100.0 / 77.5 / 65.0 | 100.0 / 51.9 / 50.0 | 100.0 / 55.0 / 70.0 |
| Gemma-4 26B-A4B-it · base · masking_backtrack · v2 A+B | 100.0 / 52.7 / 46.0 | 100.0 / 84.0 / 80.0 | 100.0 / 60.0 / 65.0 | 100.0 / 69.1 / 80.0 |
| T5Gemma 2 270M · base · masking_backtrack · v2 A+B | 100.0 / 39.5 / 18.0 | 100.0 / 69.2 / 50.0 | 100.0 / 53.7 / 25.0 | 100.0 / 55.9 / 30.0 |
| T5Gemma 2 270M · FT (full) · masking_backtrack · v2 A+B | 100.0 / 78.0 / 56.0 | 100.0 / 96.2 / 85.0 | 100.0 / 78.8 / 60.0 | 100.0 / 89.0 / 90.0 |
| T5Gemma 2 1B · base · masking_backtrack · v2 A+B | 100.0 / 38.7 / 22.0 | 100.0 / 74.1 / 25.0 | 100.0 / 47.0 / 15.0 | 100.0 / 66.4 / 30.0 |
| T5Gemma 2 1B · FT (full) · masking_backtrack · v2 A+B | 100.0 / 75.7 / 60.0 | 100.0 / 96.7 / 95.0 | 100.0 / 81.1 / 65.0 | 100.0 / 88.6 / 100.0 |
| T5Gemma 2 4B · base · masking_backtrack · v2 A+B | 100.0 / 35.6 / 22.0 | 100.0 / 71.3 / 35.0 | 100.0 / 41.4 / 30.0 | 100.0 / 48.3 / 10.0 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack · v2 A+B | 100.0 / 72.1 / 64.0 | 100.0 / 95.6 / 85.0 | 100.0 / 78.3 / 60.0 | 100.0 / 89.1 / 90.0 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack · v2 A+B | 100.0 / 62.6 / 40.0 | 100.0 / 92.4 / 55.0 | 100.0 / 67.3 / 45.0 | 100.0 / 83.1 / 40.0 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack · v2 A+B | 100.0 / 54.8 / 18.0 | 100.0 / 90.4 / 25.0 | 100.0 / 64.9 / 30.0 | 100.0 / 75.5 / 40.0 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100.0 / 74.9 / 50.0 | 100.0 / 97.7 / 85.0 | 100.0 / 78.6 / 60.0 | 100.0 / 89.5 / 90.0 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack · v2 A+B | 100.0 / 55.8 / 22.0 | 100.0 / 93.0 / 40.0 | 100.0 / 68.3 / 15.0 | 100.0 / 68.3 / 0.0 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100.0 / 80.2 / 74.0 | 100.0 / 95.7 / 80.0 | 100.0 / 83.6 / 65.0 | 100.0 / 94.1 / 100.0 |
| DiffusionGemma 26B-A4B · base · masking_backtrack · v2 A+B | 100.0 / 33.4 / 54.0 | 100.0 / 60.8 / 75.0 | 100.0 / 34.0 / 50.0 | 100.0 / 43.5 / 70.0 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack · v2 A+B | 100.0 / 31.0 / 34.0 | 100.0 / 64.7 / 60.0 | 100.0 / 28.4 / 20.0 | 100.0 / 44.9 / 80.0 |

## 5. By metre type

In metre % / real words % / recognised % per group (n poems in the header).

| cell | 7 common vṛttas (n 47) | other metres (n 53) |
|---|---|---|
| gold (the source poems) | 40.4 / 82.1 / 59.6 | 64.2 / 89.0 / 66.0 |
| Nandi-Mini-150M · base · baseline | 0.0 / 94.5 / 51.1 | 0.0 / 96.6 / 35.8 |
| Nandi-Mini-150M · base · masking_backtrack | 100.0 / 23.8 / 17.0 | 100.0 / 54.8 / 17.0 |
| Nandi-Mini-150M · FT (bhāvam → poem) · baseline | 2.1 / 75.9 / 63.8 | 7.5 / 84.5 / 66.0 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack | 100.0 / 70.9 / 59.6 | 100.0 / 74.9 / 67.9 |
| Gemma-4 E4B-it · base · baseline | 0.0 / 94.5 / 93.6 | 0.0 / 95.7 / 94.3 |
| Gemma-4 E4B-it · base · masking_backtrack | 100.0 / 22.9 / 40.4 | 100.0 / 58.9 / 77.4 |
| Gemma-4 26B-A4B-it · base · baseline | 0.0 / 96.5 / 89.4 | 0.0 / 97.2 / 94.3 |
| Gemma-4 26B-A4B-it · base · masking_backtrack | 100.0 / 36.1 / 57.4 | 100.0 / 68.2 / 67.9 |
| T5Gemma 2 270M · base · baseline | 0.0 / 79.0 / 25.5 | 0.0 / 88.4 / 39.6 |
| T5Gemma 2 270M · base · masking_backtrack | 100.0 / 25.5 / 14.9 | 100.0 / 50.9 / 34.0 |
| T5Gemma 2 270M · FT (full) · baseline | 8.5 / 72.0 / 70.2 | 7.5 / 86.1 / 79.2 |
| T5Gemma 2 270M · FT (full) · masking_backtrack | 100.0 / 72.2 / 63.8 | 100.0 / 78.0 / 64.2 |
| T5Gemma 2 1B · base · baseline | 0.0 / 88.3 / 36.2 | 0.0 / 89.1 / 39.6 |
| T5Gemma 2 1B · base · masking_backtrack | 100.0 / 25.0 / 31.9 | 100.0 / 51.6 / 30.2 |
| T5Gemma 2 1B · FT (full) · baseline | 2.1 / 77.3 / 74.5 | 13.2 / 87.6 / 75.5 |
| T5Gemma 2 1B · FT (full) · masking_backtrack | 100.0 / 72.6 / 63.8 | 100.0 / 75.5 / 67.9 |
| T5Gemma 2 4B · base · baseline | 0.0 / 95.2 / 25.5 | 0.0 / 94.9 / 26.4 |
| T5Gemma 2 4B · base · masking_backtrack | 100.0 / 22.1 / 25.5 | 100.0 / 52.2 / 30.2 |
| T5Gemma 2 4B · FT (LoRA r 128) · baseline | 2.1 / 73.6 / 68.1 | 11.3 / 86.7 / 73.6 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack | 100.0 / 70.7 / 59.6 | 98.1 / 74.5 / 66.0 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · baseline | 0.0 / 68.4 / 55.3 | 0.0 / 85.4 / 73.6 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack | 100.0 / 58.6 / 40.4 | 100.0 / 67.1 / 43.4 |
| chandohasam MDLM 120M · base (pre-trained) · baseline | 0.0 / 98.9 / 46.8 | 0.0 / 97.6 / 41.5 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | 91.5 / 37.1 / 21.3 | 94.3 / 76.5 / 18.9 |
| chandohasam MDLM 120M · FT (E6 + T1) · baseline | 0.0 / 88.0 / 80.9 | 0.0 / 94.9 / 84.9 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack | 100.0 / 75.1 / 68.1 | 100.0 / 80.1 / 77.4 |
| chandohasam MDLM 523M · base (pre-trained) · baseline | 0.0 / 98.3 / 42.6 | 0.0 / 99.1 / 47.2 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | 80.9 / 42.3 / 17.0 | 88.7 / 74.9 / 20.8 |
| chandohasam MDLM 523M · FT (E6 + T1) · baseline | 2.1 / 82.6 / 74.5 | 0.0 / 94.6 / 84.9 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack | 100.0 / 70.6 / 66.0 | 98.1 / 83.7 / 86.8 |
| DiffusionGemma 26B-A4B · base · baseline | 0.0 / 85.7 / 100.0 | 0.0 / 88.6 / 100.0 |
| DiffusionGemma 26B-A4B · base · masking_backtrack | 100.0 / 22.7 / 55.3 | 100.0 / 43.1 / 71.7 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · baseline | 0.0 / 73.8 / 87.2 | 0.0 / 85.0 / 92.5 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack | 100.0 / 16.8 / 40.4 | 100.0 / 41.0 / 52.8 |
| Nandi-Mini-150M · base · masking_backtrack · v2 A+B | 100.0 / 35.5 / 23.4 | 100.0 / 69.1 / 15.1 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack · v2 A+B | 100.0 / 76.2 / 63.8 | 100.0 / 81.7 / 58.5 |
| Gemma-4 E4B-it · base · masking_backtrack · v2 A+B | 100.0 / 31.3 / 53.2 | 100.0 / 67.5 / 64.2 |
| Gemma-4 26B-A4B-it · base · masking_backtrack · v2 A+B | 100.0 / 47.8 / 51.1 | 100.0 / 74.7 / 67.9 |
| T5Gemma 2 270M · base · masking_backtrack · v2 A+B | 100.0 / 34.5 / 21.3 | 100.0 / 63.6 / 32.1 |
| T5Gemma 2 270M · FT (full) · masking_backtrack · v2 A+B | 100.0 / 80.7 / 61.7 | 100.0 / 84.9 / 69.8 |
| T5Gemma 2 1B · base · masking_backtrack · v2 A+B | 100.0 / 34.6 / 19.1 | 100.0 / 64.1 / 24.5 |
| T5Gemma 2 1B · FT (full) · masking_backtrack · v2 A+B | 100.0 / 80.9 / 74.5 | 100.0 / 83.5 / 69.8 |
| T5Gemma 2 4B · base · masking_backtrack · v2 A+B | 100.0 / 28.2 / 19.1 | 100.0 / 60.2 / 30.2 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack · v2 A+B | 100.0 / 78.4 / 70.2 | 100.0 / 80.9 / 69.8 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack · v2 A+B | 100.0 / 67.3 / 40.4 | 100.0 / 75.4 / 47.2 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack · v2 A+B | 100.0 / 48.7 / 21.3 | 100.0 / 81.4 / 26.4 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100.0 / 76.8 / 63.8 | 100.0 / 85.9 / 62.3 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack · v2 A+B | 100.0 / 48.3 / 19.1 | 100.0 / 83.6 / 24.5 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack · v2 A+B | 100.0 / 82.1 / 72.3 | 100.0 / 88.3 / 79.2 |
| DiffusionGemma 26B-A4B · base · masking_backtrack · v2 A+B | 100.0 / 26.1 / 51.1 | 100.0 / 52.4 / 66.0 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack · v2 A+B | 100.0 / 27.0 / 27.7 | 100.0 / 48.9 / 52.8 |

## 6. The extra strategies on the same 34 prompts

Masking only and hybrid ran on the 34 earlier prompts; masking + backtracking (MB) on the same 34 beside them.

| cell | in metre % (MB) | real words % (MB) | recognised % (MB) | one-akshara % (MB) | repeating a line % (MB) |
|---|---|---|---|---|---|
| Nandi-Mini-150M · base · masking_only | 97.1 (100.0) | 21.0 (26.5) | 11.8 (8.8) | 20.3 (19.4) | 50.0 (41.2) |
| Nandi-Mini-150M · base · hybrid | 88.2 (100.0) | 22.5 (26.5) | 8.8 (8.8) | 32.9 (19.4) | 29.4 (41.2) |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_only | 100.0 (100.0) | 57.2 (57.7) | 52.9 (50.0) | 8.7 (7.6) | 0.0 (0.0) |
| Nandi-Mini-150M · FT (bhāvam → poem) · hybrid | 100.0 (100.0) | 60.6 (57.7) | 47.1 (50.0) | 6.2 (7.6) | 0.0 (0.0) |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | 79.4 (79.4) | 42.1 (46.0) | 8.8 (11.8) | 19.9 (17.5) | 29.4 (14.7) |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | 91.2 (79.4) | 42.4 (46.0) | 17.6 (11.8) | 16.1 (17.5) | 17.6 (14.7) |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_only | 94.1 (97.1) | 56.6 (62.0) | 70.6 (64.7) | 25.7 (13.0) | 2.9 (2.9) |
| chandohasam MDLM 523M · FT (E6 + T1) · hybrid | 100.0 (97.1) | 58.9 (62.0) | 67.6 (64.7) | 15.1 (13.0) | 0.0 (2.9) |

## 7. Seconds per poem

The decoder's own timing per poem (mean / median). Some cells ran beside other jobs on the shared GB10, so read these as a guide.

| cell | mean s | median s |
|---|---|---|
| Nandi-Mini-150M · base · baseline | 9.7 | 8.9 |
| Nandi-Mini-150M · base · masking_backtrack | 20.8 | 19.9 |
| Nandi-Mini-150M · FT (bhāvam → poem) · baseline | 5.1 | 4.7 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack | 14.7 | 12.6 |
| Gemma-4 E4B-it · base · baseline | 5.4 | 5.2 |
| Gemma-4 E4B-it · base · masking_backtrack | 14.8 | 15.2 |
| Gemma-4 26B-A4B-it · base · baseline | 5.2 | 4.7 |
| Gemma-4 26B-A4B-it · base · masking_backtrack | 14.8 | 15.3 |
| T5Gemma 2 270M · base · baseline | 4.3 | 3.8 |
| T5Gemma 2 270M · base · masking_backtrack | 7.8 | 7.5 |
| T5Gemma 2 270M · FT (full) · baseline | 2.7 | 2.4 |
| T5Gemma 2 270M · FT (full) · masking_backtrack | 5.4 | 4.4 |
| T5Gemma 2 1B · base · baseline | 6.1 | 5.5 |
| T5Gemma 2 1B · base · masking_backtrack | 9.7 | 9.1 |
| T5Gemma 2 1B · FT (full) · baseline | 3.5 | 3.2 |
| T5Gemma 2 1B · FT (full) · masking_backtrack | 6.1 | 4.8 |
| T5Gemma 2 4B · base · baseline | 3.1 | 0.3 |
| T5Gemma 2 4B · base · masking_backtrack | 13.4 | 13.2 |
| T5Gemma 2 4B · FT (LoRA r 128) · baseline | 6.5 | 6.3 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack | 10.3 | 9.1 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · baseline | 9.6 | 8.2 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack | 16.0 | 15.2 |
| chandohasam MDLM 120M · base (pre-trained) · baseline | 8.6 | 8.8 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack | 33.3 | 25.8 |
| chandohasam MDLM 120M · FT (E6 + T1) · baseline | 3.0 | 2.7 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack | 25.6 | 21.8 |
| chandohasam MDLM 523M · base (pre-trained) · baseline | 9.6 | 9.0 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack | 35.2 | 26.2 |
| chandohasam MDLM 523M · FT (E6 + T1) · baseline | 5.2 | 4.8 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack | 23.0 | 20.6 |
| DiffusionGemma 26B-A4B · base · baseline | 7.4 | 6.5 |
| DiffusionGemma 26B-A4B · base · masking_backtrack | 179.3 | 176.6 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · baseline | 14.6 | 14.3 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack | 179.1 | 192.4 |
| Nandi-Mini-150M · base · masking_only | 17.8 | 16.3 |
| Nandi-Mini-150M · base · hybrid | 17.1 | 16.6 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_only | 19.1 | 17.7 |
| Nandi-Mini-150M · FT (bhāvam → poem) · hybrid | 14.4 | 13.4 |
| chandohasam MDLM 523M · base (pre-trained) · masking_only | 36.6 | 30.4 |
| chandohasam MDLM 523M · base (pre-trained) · hybrid | 35.9 | 26.7 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_only | 32.2 | 30.4 |
| chandohasam MDLM 523M · FT (E6 + T1) · hybrid | 28.6 | 22.6 |
| Nandi-Mini-150M · base · masking_backtrack · v2 A+B | 27.7 | 25.4 |
| Nandi-Mini-150M · FT (bhāvam → poem) · masking_backtrack · v2 A+B | 22.6 | 21.8 |
| Gemma-4 E4B-it · base · masking_backtrack · v2 A+B | 25.1 | 25.0 |
| Gemma-4 26B-A4B-it · base · masking_backtrack · v2 A+B | 15.0 | 15.3 |
| T5Gemma 2 270M · base · masking_backtrack · v2 A+B | 8.4 | 8.0 |
| T5Gemma 2 270M · FT (full) · masking_backtrack · v2 A+B | 7.2 | 6.8 |
| T5Gemma 2 1B · base · masking_backtrack · v2 A+B | 10.1 | 9.6 |
| T5Gemma 2 1B · FT (full) · masking_backtrack · v2 A+B | 7.1 | 6.9 |
| T5Gemma 2 4B · base · masking_backtrack · v2 A+B | 23.7 | 22.5 |
| T5Gemma 2 4B · FT (LoRA r 128) · masking_backtrack · v2 A+B | 18.3 | 17.4 |
| T5Gemma 2 4B · FT (LoRA r 128), first 48k · masking_backtrack · v2 A+B | 22.9 | 20.5 |
| chandohasam MDLM 120M · base (pre-trained) · masking_backtrack · v2 A+B | 40.9 | 37.4 |
| chandohasam MDLM 120M · FT (E6 + T1) · masking_backtrack · v2 A+B | 40.4 | 36.5 |
| chandohasam MDLM 523M · base (pre-trained) · masking_backtrack · v2 A+B | 39.9 | 36.3 |
| chandohasam MDLM 523M · FT (E6 + T1) · masking_backtrack · v2 A+B | 35.9 | 34.9 |
| DiffusionGemma 26B-A4B · base · masking_backtrack · v2 A+B | 148.2 | 154.7 |
| DiffusionGemma 26B-A4B · FT (LoRA r 16) · masking_backtrack · v2 A+B | 176.3 | 192.9 |

## 8. The table against the per-poem scores

Every cell's means in grid.json equal the means of its rows in grid_poems.jsonl.
