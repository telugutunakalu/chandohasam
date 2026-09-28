"""Level 4b — Subword coverage under the Gemma 3 tokenizer (§5.4, Table 18).

Paper's metrics:
    "Gemma 3 Telugu coverage" 74.4% = 1,328 of the 1,784 Telugu tokens in the
    Gemma 3 vocabulary appear when the corpus is tokenised (804,671 tokens)
    per-poem subword TTR (mean) 0.897

What the first number measures is how much of the tokenizer's Telugu inventory
the corpus *uses*, not how well the tokenizer covers the corpus (every string
is covered by a byte-fallback tokenizer). For the question the paper raises in
§1 (subword tokenizers fragment aksharas) two direct measures are added:
    * fertility: subword tokens per word and per akshara
    * akshara-split rate: share of token boundaries that fall *inside* an akshara
Both are measured on the verse and on the Telugu prose meanings.

Writes outputs/level4_subword_coverage.json

Run:  python level4_subword_coverage.py
"""
import statistics

from transformers import AutoTokenizer

import config
from common.dataset import clean_meaning, load_subset
from common.io import pct, print_table, save_result
from common.telugu import akshara_spans, aksharas, words


def is_telugu_char(ch):
    return "ఀ" <= ch <= "౿"


def telugu_vocab(tok):
    """Token ids whose surface contains Telugu, under two definitions."""
    any_te, pure_te = set(), set()
    for tid in range(len(tok)):
        s = tok.convert_ids_to_tokens(tid)
        if not isinstance(s, str):
            continue
        s = s.replace("▁", " ")
        body = s.replace(" ", "")
        if any(is_telugu_char(c) for c in s):
            any_te.add(tid)
            if body and all(is_telugu_char(c) or c in "‌‍" for c in body):
                pure_te.add(tid)
    return any_te, pure_te


def encode(tok, texts):
    return tok(texts, add_special_tokens=False, return_offsets_mapping=True)


def akshara_split_rate(text, offsets):
    """Share of internal token boundaries that fall strictly inside an akshara."""
    interior = set()
    for s, e in akshara_spans(text):
        interior.update(range(s + 1, e))
    bounds = [end for (_, end) in offsets[:-1]]
    return sum(b in interior for b in bounds), len(bounds)


def profile(tok, texts):
    enc = encode(tok, texts)
    ids = enc["input_ids"]
    n_tok = sum(len(x) for x in ids)
    n_words = sum(len(words(t)) for t in texts)
    n_aks = sum(len(aksharas(t)) for t in texts)
    split = [akshara_split_rate(t, o) for t, o in zip(texts, enc["offset_mapping"])]
    inside, total = sum(s for s, _ in split), sum(t for _, t in split)
    return ids, {
        "texts": len(texts), "subword_tokens": n_tok,
        "tokens_per_word": n_tok / n_words, "tokens_per_akshara": n_tok / n_aks,
        "akshara_split_rate_pct": pct(inside, total),
        "per_text_subword_ttr_mean": statistics.fmean(len(set(x)) / len(x) for x in ids if x),
    }


def main():
    master = load_subset("master")
    tok = AutoTokenizer.from_pretrained(config.GEMMA3_TOKENIZER)
    any_te, pure_te = telugu_vocab(tok)
    print(f"Gemma 3 vocab {len(tok):,}; tokens containing Telugu: {len(any_te):,}; "
          f"purely Telugu: {len(pure_te):,}   (paper: 1,784)")

    poems = [r["poem"] for r in master]
    prose = [clean_meaning(r["telugu_meaning"]) for r in master]
    poem_ids, poem_prof = profile(tok, poems)
    _, prose_prof = profile(tok, prose)

    used = {t for x in poem_ids for t in x}
    coverage = {
        "vocab_any_telugu": len(any_te), "vocab_pure_telugu": len(pure_te),
        "used_any_telugu": len(used & any_te), "used_pure_telugu": len(used & pure_te),
        "coverage_any_pct": pct(len(used & any_te), len(any_te)),
        "coverage_pure_pct": pct(len(used & pure_te), len(pure_te)),
        "distinct_ids_used": len(used),
    }
    print("\nVocabulary utilisation by the verse corpus (paper: 1,328 / 1,784 = 74.4%)")
    print_table(["definition", "in vocab", "used", "%"],
                [["any Telugu char", len(any_te), coverage["used_any_telugu"], coverage["coverage_any_pct"]],
                 ["purely Telugu", len(pure_te), coverage["used_pure_telugu"], coverage["coverage_pure_pct"]]])

    print("\nTokenisation profile (paper: 804,671 corpus tokens; per-poem subword TTR 0.897)")
    keys = list(poem_prof)
    print_table(["measure", "verse", "telugu prose"], [[k, poem_prof[k], prose_prof[k]] for k in keys])

    save_result("level4_subword_coverage", {
        "tokenizer": config.GEMMA3_TOKENIZER,
        "paper_reported": {k: v for k, v in config.PAPER["level4"].items()
                           if k.startswith(("gemma", "poem_subword"))},
        "coverage": coverage, "verse": poem_prof, "telugu_prose": prose_prof,
    })


if __name__ == "__main__":
    main()
