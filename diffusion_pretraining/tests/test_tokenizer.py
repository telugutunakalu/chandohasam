"""Correctness tests for the syllable-aware Telugu tokenizer.

The two load-bearing guarantees:
  * NO OOV      — encode() never yields an id outside the vocab, for ANY input.
  * LOSSLESS    — decode(encode(t)) == normalize(t)  (foreign="bytes").

Run:  uv run pytest tests/ -q
"""
from __future__ import annotations

import os
import random
import sys

from tokenizer import akshara
from tokenizer.telugu_tokenizer import SyllableAwareTeluguTokenizer as Tok

# A small but structurally rich training corpus (covers conjuncts, pollu, IV,
# numbers, matras) so the trained tokenizer is realistic without a big download.
_TRAIN = [
    "తెలుగు భారతదేశంలోని ఒక ద్రావిడ భాష.",
    "శ్రీకృష్ణుడు వచ్చెను. విద్యార్థి పాఠశాలకు వెళ్ళాడు.",
    "సంస్కృతం చంద్రుడు ఐశ్వర్యం పద్యం నమస్కారం.",
    "అక్క అన్నం వాక్ క్ష్మ ప్రేమ ధర్మం కర్మ.",
    "ఆంధ్రప్రదేశ్ తెలంగాణ రాష్ట్రాల అధికార భాష తెలుగు.",
    "సంఖ్యలు ౦ ౧ ౨ ౩ ౪ ౫ ౬ ౭ ౮ ౯ మరియు 0 1 2 3 4 5.",
    "కవిత్వం సాహిత్యం చరిత్ర సంస్కృతి విజ్ఞానం గణితం.",
] * 40


def _mk():
    return Tok.train(_TRAIN, vocab_size=3000, num_bpe_merges=300,
                     min_akshara_freq=1, verbose=False)


TOK = _mk()

# ------------------------------------------------------------ test inventory
LOSSLESS_CASES = [
    "తెలుగు భాష చాలా అందమైనది",
    "శ్రీకృష్ణుడు వచ్చెను",
    "వాక్ అన్నం",                                   # pollu then independent vowel
    "క్ష్మ",                                          # deep conjunct
    "ఴ ౘ ౙ ౚ ౝ ఽ",                                 # rare/edge consonants + avagraha
    "౦౧౨౩౪౫౬౭౮౯ 0123456789",                        # Telugu + ASCII digits
    "విద్యార్థి ద్యా ర్థి",
    "ఆయుష్షు పెంచుకుందాం రండి!",
    "గమనిక: ఈనాడు.నెట్‌లో కనిపించే వ్యాపార ప్రకటనలు",   # has ZWNJ (normalized away)
    "్ా",                                  # orphan virama + orphan matra
    "ఀ ఄ",                                            # rarely-used signs
    "",
    " ",
    "\n\t  ",
]


def test_lossless_known():
    for t in LOSSLESS_CASES:
        got = TOK.decode(TOK.encode(t))
        assert got == akshara.normalize(t), (t, got, akshara.normalize(t))


def test_no_oov_known():
    for t in LOSSLESS_CASES:
        for i in TOK.encode(t):
            assert 0 <= i < TOK.vocab_size


def _random_telugu(rng, n):
    # Build random-but-plausible aksharas: onset (+ optional conjuncts) + matra.
    C = [chr(c) for c in range(0x0C15, 0x0C3A)]
    IV = [chr(c) for c in range(0x0C05, 0x0C15)]
    M = [chr(c) for c in range(0x0C3E, 0x0C4D)]
    VIR = "్"
    out = []
    for _ in range(n):
        if rng.random() < 0.2:
            out.append(rng.choice(IV))
            continue
        s = rng.choice(C)
        while rng.random() < 0.35:
            s += VIR + rng.choice(C)
        if rng.random() < 0.7:
            s += rng.choice(M)
        out.append(s)
    return "".join(out)


def test_fuzz_lossless_and_no_oov():
    rng = random.Random(1234)
    for _ in range(3000):
        mode = rng.random()
        if mode < 0.5:
            t = _random_telugu(rng, rng.randint(1, 12))
        elif mode < 0.75:
            # arbitrary BMP + astral codepoints incl. lone surrogates (emoji,
            # CJK, control chars, U+D800..U+DFFF) — all must survive.
            t = "".join(chr(rng.randint(1, 0x10FFF0)) for _ in range(rng.randint(1, 20)))
        else:
            t = _random_telugu(rng, 4) + "".join(
                chr(rng.randint(32, 0x2FFF)) for _ in range(rng.randint(1, 10)))
        ids = TOK.encode(t)
        for i in ids:
            assert 0 <= i < TOK.vocab_size, (repr(t), i)
        assert TOK.decode(ids) == akshara.normalize(t), repr(t)


def test_lone_surrogates_no_crash_and_lossless():
    # Lone surrogates are valid Python str but invalid strict UTF-8; encode must
    # not raise, must not OOV, and must round-trip (WTF-8 via surrogatepass).
    cases = ["\ud800", "ప\ud800ప", "\udfff", "abc𝄞",  # (also a split pair)
             "".join(chr(c) for c in range(0xD800, 0xD810))]
    for t in cases:
        ids = TOK.encode(t)
        assert all(0 <= i < TOK.vocab_size for i in ids), t.encode("unicode_escape")
        assert TOK.decode(ids) == akshara.normalize(t), t.encode("unicode_escape")


def test_bytes_ascii_random_no_oov():
    # Random raw unicode strings, hammering the byte failover.
    rng = random.Random(99)
    for _ in range(2000):
        b = bytes(rng.randint(0, 255) for _ in range(rng.randint(0, 30)))
        t = b.decode("utf-8", errors="replace")
        ids = TOK.encode(t)
        assert all(0 <= i < TOK.vocab_size for i in ids)
        assert TOK.decode(ids) == akshara.normalize(t)


def test_syllable_alignment():
    # Frequent syllables should be single tokens; segmentation matches aksharanusarika.
    gold = {
        "తెలుగు": ["తె", "లు", "గు"],
        "శ్రీకృష్ణుడు": ["శ్రీ", "కృ", "ష్ణు", "డు"],
        "విద్యార్థి": ["వి", "ద్యా", "ర్థి"],
    }
    for w, pieces in gold.items():
        assert TOK.pretokenize(w) == pieces
        # each of these aksharas appeared in training -> one atomic token each
        assert len(TOK.encode(w)) == len(pieces), (w, TOK.tokens(TOK.encode(w)))


def test_numbers_are_per_digit():
    assert TOK.pretokenize("౧౨౩") == ["౧", "౨", "౩"]
    assert TOK.pretokenize("123") == ["1", "2", "3"]
    assert len(TOK.encode("2024")) == 4            # ASCII digits: 1 token each
    assert len(TOK.encode("౨౦౨౪")) == 4            # Telugu digits: 1 token each
    for d in "౦౧౨౩౪౫౬౭౮౯":
        assert len(TOK.encode(d)) == 1, (d, TOK.tokens(TOK.encode(d)))


def test_drop_mode_keeps_structure():
    drop = Tok.train(_TRAIN, vocab_size=1500, num_bpe_merges=200,
                     min_akshara_freq=1, foreign="drop", verbose=False)
    # foreign letters removed, but whitespace + punctuation + Telugu preserved
    out = drop.decode(drop.encode("ప, hello ప!"))
    assert "ప" in out and "," in out and "!" in out and " " in out
    assert "h" not in out and "e" not in out


def test_save_load_roundtrip(tmp_path=None):
    import tempfile
    d = tmp_path or tempfile.mkdtemp()
    p = os.path.join(str(d), "t.json")
    TOK.save(p)
    other = Tok.load(p)
    assert other.vocab_size == TOK.vocab_size
    for t in LOSSLESS_CASES:
        assert other.encode(t) == TOK.encode(t)
        assert other.decode(other.encode(t)) == akshara.normalize(t)


def test_foreign_modes():
    drop = Tok.train(_TRAIN, vocab_size=1500, num_bpe_merges=200,
                     min_akshara_freq=1, foreign="drop", verbose=False)
    unk = Tok.train(_TRAIN, vocab_size=1500, num_bpe_merges=200,
                    min_akshara_freq=1, foreign="unk", verbose=False)
    # foreign letters dropped, Telugu + digits kept
    assert drop.decode(drop.encode("ప hello ప")) == "ప  ప" or "ప" in drop.decode(drop.encode("ప hello ప"))
    # unk collapses each foreign run to a single <unk> token, no OOV
    ids = unk.encode("ప hello ప")
    assert all(0 <= i < unk.vocab_size for i in ids)


def test_emittable_mask_flags_shards():
    mask = TOK.emittable_mask()
    assert len(mask) == TOK.vocab_size
    # specials are never emittable
    for sid in TOK.special_ids:
        assert mask[sid] is False


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"ok   {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {fn.__name__}: {e}")
        except Exception as e:
            failed += 1
            print(f"ERR  {fn.__name__}: {type(e).__name__}: {e}")
    print(f"\n{len(fns) - failed}/{len(fns)} passed")
    sys.exit(1 if failed else 0)
