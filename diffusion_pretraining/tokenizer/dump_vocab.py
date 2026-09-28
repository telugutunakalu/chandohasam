#!/usr/bin/env python3
"""Dump a trained tokenizer's full vocabulary to a human-readable TSV.

    python dump_vocab.py telugu_wikipedia.tokenizer.json          # -> *.vocab.tsv
    python dump_vocab.py telugu_wikipedia.tokenizer.json -o v.tsv

Columns: id <tab> kind <tab> token <tab> bytes_hex
  kind ∈ {special, syllable, digit, byte, subword}
    syllable = a whole akshara that is one token  ("every syllable its own token")
    subword  = a byte-BPE piece used by the failover for rare/unseen aksharas
    byte     = one of the 256 base bytes (the no-OOV floor)
"""
from __future__ import annotations

import sys
from collections import Counter

from .telugu_tokenizer import SyllableAwareTeluguTokenizer as Tok


def kind_of(tok: Tok, i: int) -> str:
    if i in tok.special_ids:
        return "special"
    b = tok.id_to_bytes[i]
    if i in set(tok.akshara_to_id.values()):
        return "syllable"
    if i in set(tok.digit_to_id.values()):
        return "digit"
    if b is not None and len(b) == 1:
        return "byte"
    return "subword"


def main(argv=None) -> int:
    args = argv or sys.argv[1:]
    if not args:
        print(__doc__)
        return 1
    path = args[0]
    out = "vocab.tsv"
    if "-o" in args:
        out = args[args.index("-o") + 1]
    else:
        out = path.rsplit(".", 1)[0].replace(".tokenizer", "") + ".vocab.tsv"

    tok = Tok.load(path)
    akset = set(tok.akshara_to_id.values())
    digset = set(tok.digit_to_id.values())
    counts: Counter = Counter()
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("id\tkind\ttoken\tbytes_hex\n")
        for i in range(tok.vocab_size):
            b = tok.id_to_bytes[i]
            if i in tok.special_ids:
                k = "special"
            elif i in akset:
                k = "syllable"
            elif i in digset:
                k = "digit"
            elif b is not None and len(b) == 1:
                k = "byte"
            else:
                k = "subword"
            counts[k] += 1
            hexs = b.hex() if b is not None else ""
            # keep the token cell single-line and tab-free
            disp = tok.id_to_str[i].replace("\t", "\\t").replace("\n", "\\n")
            fh.write(f"{i}\t{k}\t{disp}\t{hexs}\n")

    print(f"wrote {tok.vocab_size:,} tokens -> {out}")
    for k, n in counts.most_common():
        print(f"  {k:9} {n:>7,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
