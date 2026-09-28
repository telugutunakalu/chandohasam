#!/usr/bin/env python3
"""Evaluate a trained tokenizer on held-out text.

Checks the two guarantees on data the tokenizer never saw, and reports
efficiency (tokens/piece, per-syllable fertility, atomic coverage).

    python eval_tokenizer.py \
        --tokenizer telugu_wikipedia.tokenizer.json \
        --input data/telugu-wikipedia-articles__disisbig/valid \
                data/telugu-wikipedia-articles__shubhamjain27/telugu_wiki_test.parquet
"""
from __future__ import annotations

import argparse
import sys
import time

from . import akshara
from .corpus import iter_corpus
from .telugu_tokenizer import SyllableAwareTeluguTokenizer, _is_syllabic_akshara


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokenizer", "-t", required=True)
    ap.add_argument("--input", "-i", nargs="+", required=True)
    ap.add_argument("--max-lines", type=int, default=0)
    ap.add_argument("--dump-unseen", default=None,
                    help="write the distinct failover (non-atomic) aksharas here, "
                         "one per line — feed to train_tokenizer.py --extra-aksharas "
                         "to make them atomic on the next run")
    args = ap.parse_args(argv)

    tok = SyllableAwareTeluguTokenizer.load(args.tokenizer)
    V = tok.vocab_size

    n_lines = n_pieces = n_tokens = 0
    lossless_fail = oov = 0
    syl_pieces = syl_tokens = 0
    atomic = failover = 0
    from collections import Counter
    unseen_aksharas: Counter = Counter()
    t0 = time.time()

    for line in iter_corpus(args.input):
        n_lines += 1
        norm = akshara.normalize(line)
        ids = tok.encode(line)
        if any(not 0 <= i < V for i in ids):
            oov += sum(1 for i in ids if not 0 <= i < V)
        if tok.decode(ids) != norm:
            lossless_fail += 1
        pieces = tok.pretokenize(line)
        n_pieces += len(pieces)
        n_tokens += len(ids)
        for p in pieces:
            if _is_syllabic_akshara(p):
                syl_pieces += 1
                if p in tok.akshara_to_id:
                    atomic += 1
                    syl_tokens += 1
                else:
                    failover += 1
                    unseen_aksharas[p] += 1
                    syl_tokens += len(tok.bpe.encode(p.encode("utf-8", "surrogatepass")))
        if args.max_lines and n_lines >= args.max_lines:
            break

    dt = time.time() - t0
    print(f"tokenizer      : {args.tokenizer}  (vocab {V:,})")
    print(f"held-out lines : {n_lines:,}   ({dt:.1f}s)")
    print("-" * 56)
    print(f"LOSSLESS failures : {lossless_fail:,}      (must be 0)")
    print(f"OOV tokens        : {oov:,}      (must be 0)")
    print("-" * 56)
    print(f"pieces / tokens   : {n_pieces:,} / {n_tokens:,}")
    print(f"tokens per piece  : {n_tokens / max(1, n_pieces):.4f}")
    if syl_pieces:
        print(f"Telugu syllables  : {syl_pieces:,}")
        print(f"  one-token (atomic): {100 * atomic / syl_pieces:.2f}%")
        print(f"  via failover      : {100 * failover / syl_pieces:.2f}%  "
              f"({len(unseen_aksharas):,} distinct unseen aksharas, all 0-OOV)")
        print(f"  tokens per syllable: {syl_tokens / syl_pieces:.4f}")
    if args.dump_unseen and unseen_aksharas:
        with open(args.dump_unseen, "w", encoding="utf-8") as fh:
            for ak, _ in unseen_aksharas.most_common():   # most-impactful first
                fh.write(ak + "\n")
        print(f"[dump] {len(unseen_aksharas):,} failover aksharas -> {args.dump_unseen}")
        print("       re-train with:  --extra-aksharas " + args.dump_unseen)

    ok = (lossless_fail == 0 and oov == 0)
    print("-" * 56)
    print("RESULT:", "PASS — no OOV, fully lossless on held-out data" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
