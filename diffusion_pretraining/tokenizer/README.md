# Syllable-aware Telugu tokenizer

A tokenizer that gives **every Telugu syllable (akshara) its own token**, with a
**byte-level BPE failover** so it **can never emit an OOV token** — for any input
whatsoever. Numbers are first-class (one token per digit). Other languages are
*not modelled* (no dedicated tokens, no merges spent on them) but are still
preserved losslessly through the byte failover, so nothing ever falls off.

Built on [`akshara.py`](akshara.py) (dependency-free Telugu syllable
segmentation). The core tokenizer is **pure standard library** — no
`tokenizers`, no `sentencepiece`.

---

## Why

Sub-word BPE trained directly on Telugu shreds syllables: a single akshara like
`ష్ణు` can split across several unrelated tokens, and the boundaries drift with
the corpus. Telugu is an *abugina* — the akshara (orthographic syllable) is the
natural cognitive and phonological unit. This tokenizer makes the akshara the
primary token and only decomposes when it has to.

## How it works — two levels

```
text ──normalize (NFC + strip ZWJ/ZWNJ)──▶ akshara segmentation ──▶ pieces
                                                                      │
                    ┌─────────────────────────────────────────────────┤
                    ▼                                                   ▼
        piece is a known syllable / digit?                    everything else
                    │ yes                                             │
                    ▼                                                 ▼
          one atomic token  ◀── "every syllable its own token"   byte-level BPE
                                                             (base = 256 bytes)
                                                                     │
                                                          always bottoms out
                                                          ⇒ **OOV impossible**
```

1. **Segment** with `akshara.py`. Segmentation is *lossless*:
   `"".join(pieces) == normalize(text)`. A conjunct such as `ష్ణు` is one piece.
2. **Primary — one token per syllable.** Every akshara seen often enough in
   training (`--min-akshara-freq`) gets a dedicated atomic token. Digits (ASCII
   `0-9` and Telugu `౦-౯`) are one token each.
3. **Failover — byte-level BPE (Telugu-trained).** A rare or *unseen* akshara
   with no atomic token is encoded by a byte-level BPE whose base alphabet is the
   **256 raw bytes**. It therefore *always* encodes — there is no `<unk>` path.
   Merges only make the failover shorter; they never decide whether it succeeds.

### The no-OOV guarantee, precisely

OOV is impossible **by construction**, and it does not depend on how well BPE was
trained: the 256 single-byte tokens are always in the vocabulary, and every
`bytes` value decomposes into them. The failover BPE is an *efficiency* layer on
top of that floor, not a correctness dependency.

### Scope: Telugu + numbers only

Only Telugu and numbers are *modelled*. Text in other scripts (English, …) gets
no atomic tokens and no BPE merges — it is "ignored" in the modelling sense. By
default (`foreign="bytes"`) it is still encoded via the byte floor, so the round
trip stays lossless and OOV-free. Two opt-in alternatives:

| `foreign=` | non-Telugu **letters** | standalone whitespace / punctuation / digits | lossless | OOV |
|------------|------------------------|----------------------------------------------|----------|-----|
| `bytes` (default) | kept as raw bytes | kept | ✅ | never |
| `drop`     | discarded              | kept                              | Telugu-only | never |
| `unk`      | one `<unk>` per run    | kept                              | Telugu-only | never |

In `drop`/`unk`, a "foreign run" is a whole pre-token piece that contains a
non-Telugu letter, so punctuation *fused* to a foreign word (`COVID-19`,
`www.site.com`) is dropped/collapsed with it; whitespace, digits, and punctuation
that stand on their own are always preserved. The default `bytes` mode keeps
everything and is the only fully lossless mode.

## Guarantees (all covered by `tests/`)

- **No OOV** — `encode(x)` never raises and never yields an id outside
  `[0, vocab_size)`, for *any* Unicode `x` (fuzzed over random bytes, astral
  planes, lone-surrogate-cleaned input, control chars, all-combining strings).
- **Lossless** — with `foreign="bytes"`, `decode(encode(x)) == normalize(x)` for
  any `x`. (`normalize` = NFC + stripping zero-width joiners, per `akshara.py`;
  the tokenizer is lossless with respect to *normalized* text.)
- **Syllable alignment** — pieces match `akshara.py`; frequent syllables are a
  single token.

## Measured on the cited Kaggle datasets

Trained in **180 s** on the *train* splits of both cited datasets (~1.2 GB:
`disisbig` 78,874 articles + `shubhamjain27` 67,162 articles), then evaluated on
the **held-out** valid/test splits it never saw — the real test of the failover:

| metric (held-out valid + test) | value |
|---|---|
| held-out lines / tokens | 226,772 / 66,874,622 |
| **lossless failures** | **0** |
| **OOV tokens** | **0** |
| Telugu syllables that are exactly one token | **99.98 %** (fertility 1.0003) |
| **distinct *unseen* aksharas — all 0-OOV via failover** | **5,783** |
| vocab: syllable / subword / byte / digit / special | 27,933 / 509 / 256 / 10 / 5 = **28,713** |

The 5,783 aksharas that never appeared in training — rare conjuncts,
transliterated names — every one encoded losslessly with zero OOV. Reproduce:

```bash
python train_tokenizer.py \
  --input data/telugu-wikipedia-articles__disisbig/train \
          data/telugu-wikipedia-articles__shubhamjain27/telugu_wiki_train.parquet \
  --out telugu_wikipedia.tokenizer.json --vocab-size 48000 --bpe-merges 8000 --min-akshara-freq 3
python eval_tokenizer.py --tokenizer telugu_wikipedia.tokenizer.json \
  --input data/telugu-wikipedia-articles__disisbig/valid \
          data/telugu-wikipedia-articles__shubhamjain27/telugu_wiki_test.parquet
```

## Usage

### 1. Get data

The tokenizer trains on any Telugu text. The cited Kaggle datasets:

```bash
pip install kaggle                       # + put kaggle.json at ~/.kaggle/ (chmod 600)
python download_data.py                  # -> ./data/
```

Or point it at any local `.txt` / `.tsv` (`Sentence<TAB>Frequency` auto-detected)
/ `.json` / `.csv` corpus.

### 2. Train

```bash
python train_tokenizer.py \
  --input data/ \
  --out telugu_syllable.tokenizer.json \
  --vocab-size 32000 --bpe-merges 4000 --min-akshara-freq 2
```

### 3. Use

```python
from telugu_tokenizer import SyllableAwareTeluguTokenizer as Tok

tok = Tok.load("telugu_syllable.tokenizer.json")

ids = tok.encode("శ్రీకృష్ణుడు వచ్చెను 2024", add_bos=True, add_eos=True)
tok.decode(ids)                 # -> 'శ్రీకృష్ణుడు వచ్చెను 2024'   (round-trips)
tok.pretokenize("శ్రీకృష్ణుడు") # -> ['శ్రీ', 'కృ', 'ష్ణు', 'డు']
tok.tokens(ids)                 # human-readable token strings
tok.coverage("...")             # per-piece diagnostic breakdown
```

`python demo.py` prints a full worked tour.

## Files

| file | role |
|---|---|
| `telugu_tokenizer.py` | the tokenizer: segmentation, atomic vocab, failover, encode/decode, save/load |
| `bpe.py`              | byte-level BPE trainer + encoder (the OOV-proof failover) |
| `akshara.py`         | Telugu syllable segmentation (given) |
| `corpus.py`          | streaming loaders: txt / TSV / json / csv |
| `train_tokenizer.py` | training CLI |
| `eval_tokenizer.py`  | held-out evaluation (0-OOV / lossless / fertility) |
| `dump_vocab.py`      | export the full vocab to a browsable TSV |
| `download_data.py`   | Kaggle dataset downloader (2.x token auth) |
| `demo.py`            | worked examples |
| `tests/test_tokenizer.py` | losslessness + no-OOV fuzzing + alignment + save/load |

## Inspecting the vocabulary

```bash
python dump_vocab.py telugu_wikipedia.tokenizer.json   # -> telugu_wikipedia.vocab.tsv
```

`telugu_wikipedia.vocab.tsv` has one row per token: `id · kind · token · bytes_hex`,
where `kind` is `syllable` (a whole akshara = one token), `subword` (a failover
byte-BPE piece), `byte` (one of the 256 base bytes), `digit`, or `special`.

## Decode-time masks (advisory, for generation)

`akshara.py` distinguishes "emittable" syllables from failover shards (an orphan
matra, a bare virama). The tokenizer surfaces this at the token level:

- `tok.emittable_mask()` → `bool` per id; `False` for specials, mid-codepoint
  byte fragments, and orphan-combining shards. Mask these out of the logits at
  generation while keeping them available for *encoding* (that asymmetry is what
  makes the tokenizer lossless on unseen aksharas).
- `tok.blocks_next(i, j)` → `True` for an invalid Telugu transition (a
  pollu-final token followed by an independent-vowel token = dangling virama).

## Tests

```bash
python tests/test_tokenizer.py        # or: python -m pytest tests/ -q
```
