"""The tokenizer must split exactly where aksharanusarika (the meter engine's splitter) does,
and the frozen telugu_alldomain vocabulary must give one token per common akshara."""
from __future__ import annotations

from tokenizer import akshara, load_default
from tokenizer.aksharanusarika_split import _aksharanusarika

TOK = load_default()

LINES = [
    "వేమననగ యోగి వెలసె లోకములోనఁ",                 # ఁ attaches to its akshara
    "పూజలిడుఁడు, పుణ్య పురుషులార",
    "పలికెడిది భాగవత మఁట, పలికించెడివాడు రామభద్రుం డఁట",
    "గమనిక: ఈనాడు.నెట్‌లో కనిపించే ప్రకటనలు",          # ZWNJ (normalized away)
    "ఫ్రాన్‌క్స్ రాజ్యం, పోస్ట్ ఆఫీస్",                      # dead-consonant clusters
    "ఎ.ట్. రామారావ్ (1923) - ౧౯౨౩",                    # dead consonant after punctuation, digits
    "విూరు యెుక్క",                                    # stacked vowel signs stay together
    "Telugu తెలుగు mixed 🙂 text",
]


def _telugu(pieces):
    return [p for p in pieces if "ఀ" <= p[0] <= "౿"]


def test_pieces_are_aksharanusarika_aksharas():
    ak = _aksharanusarika()
    for line in LINES:
        norm = akshara.normalize(line)
        assert _telugu(TOK.pretokenize(line)) == _telugu(ak.split_aksharalu(norm)), line


def test_splitting_rules():
    assert TOK.pretokenize("తెలుఁగు") == ["తె", "లుఁ", "గు"]
    assert TOK.pretokenize("ఫ్రాన్‌క్స్") == ["ఫ్రాన్క్స్"]
    assert TOK.pretokenize("విూరు") == ["విూ", "రు"]
    assert TOK.pretokenize(".ట్.") == [".", "ట్", "."]


def test_lossless_and_no_oov_with_default_vocab():
    for line in LINES:
        ids = TOK.encode(line)
        assert all(0 <= i < TOK.vocab_size for i in ids)
        assert TOK.decode(ids) == akshara.normalize(line)


def test_common_aksharas_are_single_tokens():
    for word, n in [("తెలుగు", 3), ("తెలుఁగు", 3), ("పూజలిడుఁడు", 5), ("శ్రీకృష్ణుడు", 4)]:
        assert len(TOK.encode(word)) == n, (word, TOK.tokens(TOK.encode(word)))


def test_special_tokens_for_mdlm():
    assert TOK.vocab_size == 45591
    assert (TOK.pad_id, TOK.bos_id, TOK.eos_id) == (0, 2, 3)
    assert TOK.special_to_id["<mask>"] == 4
