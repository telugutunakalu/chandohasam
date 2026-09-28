"""Level 4b — Subword coverage under the Gemma tokenizer.

Metrics, per corpus:
    Telugu vocabulary coverage   of the tokenizer's Telugu tokens, the share
                                 that the verse corpus uses when tokenised
                                 ("any": token contains a Telugu character;
                                 "pure": token is Telugu characters only)
    per-poem subword TTR         distinct tokens / tokens, averaged over poems

The default tokenizer is Gemma 4's (config.TOKENIZER). Gemma 3's is the same
text tokenizer: the same 1,784 Telugu tokens and identical token ids for every
verse and bhavam of the four files; only their special tokens differ.

What coverage measures is how much of the tokenizer's Telugu inventory a corpus
USES, not how well the tokenizer fits the corpus (a byte-fallback tokenizer
covers every string). Two direct measures of fit are added, for the verse and
for its Telugu bhavam:
    fertility            subword tokens per word and per akshara
    akshara-split rate   share of token boundaries that fall INSIDE an akshara
                         (a token that splits an akshara hides its guru/laghu
                         weight from the model)

Writes outputs/level4_subword_coverage.json

Run:  python level4_subword_coverage.py [--tokenizer google/gemma-4-E2B-it] [--datasets ...]
"""
import argparse
import statistics

from transformers import AutoTokenizer

import config
from common.dataset import add_dataset_argument, by_corpus, load_poems
from common.io import pct, print_table, save_result
from common.telugu import akshara_spans, aksharas, words


def is_telugu_char(ch) -> bool:
    return "ఀ" <= ch <= "౿"


def telugu_vocab(tok) -> tuple:
    """Token ids that contain Telugu ("any") and that are only Telugu ("pure")."""
    any_te, pure_te = set(), set()
    for tid in range(len(tok)):
        s = tok.convert_ids_to_tokens(tid)
        if not isinstance(s, str):
            continue
        body = s.replace("▁", "").replace(" ", "")
        if any(is_telugu_char(c) for c in s):
            any_te.add(tid)
            if body and all(is_telugu_char(c) or c in "‌‍" for c in body):
                pure_te.add(tid)
    return any_te, pure_te


def akshara_splits(text, offsets) -> tuple:
    """(token boundaries inside an akshara, all internal token boundaries) of one text."""
    inside = set()
    for start, end in akshara_spans(text):
        inside.update(range(start + 1, end))
    bounds = [end for _, end in offsets[:-1]]
    return sum(b in inside for b in bounds), len(bounds)


def profile(tok, texts) -> tuple:
    """Token ids of each text, and the fertility / split / TTR profile of the texts."""
    enc = tok(texts, add_special_tokens=False, return_offsets_mapping=True)
    ids = enc["input_ids"]
    n_tok = sum(len(x) for x in ids)
    splits = [akshara_splits(t, o) for t, o in zip(texts, enc["offset_mapping"])]
    return ids, {
        "texts": len(texts),
        "subword_tokens": n_tok,
        "tokens_per_word": n_tok / max(1, sum(len(words(t)) for t in texts)),
        "tokens_per_akshara": n_tok / max(1, sum(len(aksharas(t)) for t in texts)),
        "akshara_split_rate_pct": pct(sum(s for s, _ in splits), sum(n for _, n in splits)),
        "per_text_subword_ttr_mean": statistics.fmean(len(set(x)) / len(x) for x in ids if x),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenizer", default=config.TOKENIZER)
    add_dataset_argument(ap)
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    any_te, pure_te = telugu_vocab(tok)
    print(f"{args.tokenizer}: vocabulary {len(tok):,}; tokens containing Telugu {len(any_te):,}; "
          f"purely Telugu {len(pure_te):,}")

    result = {"tokenizer": args.tokenizer, "vocab_any_telugu": len(any_te), "vocab_pure_telugu": len(pure_te),
              "corpora": {}}
    cov_rows, prof_rows = [], []
    for corpus, group in by_corpus(load_poems(tuple(args.datasets))).items():
        verse_ids, verse = profile(tok, [p.text for p in group])
        _, bhavam = profile(tok, [p.bhavam for p in group if p.bhavam])
        used = {t for x in verse_ids for t in x}
        coverage = {"used_any_telugu": len(used & any_te), "used_pure_telugu": len(used & pure_te),
                    "coverage_any_pct": pct(len(used & any_te), len(any_te)),
                    "coverage_pure_pct": pct(len(used & pure_te), len(pure_te))}
        result["corpora"][corpus] = {"coverage": coverage, "verse": verse, "telugu_bhavam": bhavam}
        cov_rows.append([corpus, coverage["used_any_telugu"], coverage["coverage_any_pct"],
                         coverage["used_pure_telugu"], coverage["coverage_pure_pct"],
                         verse["per_text_subword_ttr_mean"]])
        for kind, prof in (("verse", verse), ("telugu bhavam", bhavam)):
            prof_rows.append([corpus, kind, prof["subword_tokens"], prof["tokens_per_word"],
                              prof["tokens_per_akshara"], prof["akshara_split_rate_pct"]])

    print_table(["corpus", "Telugu tokens used (any)", "coverage % (any)", "used (pure)", "coverage % (pure)",
                 "per-poem subword TTR"], cov_rows, "Level 4b — Telugu vocabulary coverage by the verse")
    print_table(["corpus", "text", "subword tokens", "tokens / word", "tokens / akshara",
                 "akshara-split rate %"], prof_rows, "Sense check — how well the tokenizer fits the text")
    save_result("level4_subword_coverage", result)


if __name__ == "__main__":
    main()
