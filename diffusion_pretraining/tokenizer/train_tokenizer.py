#!/usr/bin/env python3
"""Train the syllable-aware Telugu tokenizer from a corpus.

Examples
--------
  # Train on the local Telugu corpus (TSV export is auto-detected):
  python train_tokenizer.py \
      --input /home/samvaran/phd_workspace/indic_nuerosym/telugu_corpus/pure_telugu_sentences.txt \
      --out telugu_syllable.tokenizer.json --vocab-size 32000

  # Train on the Kaggle datasets after `python download_data.py`:
  python train_tokenizer.py --input data/ --out telugu_syllable.tokenizer.json
"""
from __future__ import annotations

import argparse
import sys
import time

from .corpus import iter_corpus
from .telugu_tokenizer import SyllableAwareTeluguTokenizer


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", "-i", nargs="+", required=True,
                    help="corpus file(s) or dir(s): .txt/.tsv, .json, .csv")
    ap.add_argument("--out", "-o", default="telugu_syllable.tokenizer.json",
                    help="output tokenizer json path")
    ap.add_argument("--vocab-size", type=int, default=32000,
                    help="soft target total vocabulary size")
    ap.add_argument("--bpe-merges", type=int, default=4000,
                    help="size of the Telugu byte-BPE failover")
    ap.add_argument("--min-akshara-freq", type=int, default=2,
                    help="min occurrences for a syllable to get its own token")
    ap.add_argument("--min-pair-freq", type=int, default=2,
                    help="min pair frequency for a BPE merge")
    ap.add_argument("--foreign", choices=["bytes", "drop", "unk"], default="bytes",
                    help="non-Telugu handling: bytes=lossless failover (default), "
                         "drop=discard, unk=collapse to <unk>")
    ap.add_argument("--extra-aksharas", default=None,
                    help="file with one akshara per line to FORCE into the atomic "
                         "vocab (guaranteed 1 token each), even if unseen/rare. "
                         "e.g. the file produced by `eval_tokenizer.py --dump-unseen`")
    ap.add_argument("--max-lines", type=int, default=0,
                    help="cap number of lines (0 = all); useful for a quick run")
    args = ap.parse_args(argv)

    extra = None
    if args.extra_aksharas:
        with open(args.extra_aksharas, encoding="utf-8") as fh:
            extra = [ln.rstrip("\n") for ln in fh if ln.strip()]
        print(f"[extra] forcing {len(extra):,} aksharas into the atomic vocab")

    def lines():
        n = 0
        for line in iter_corpus(args.input):
            yield line
            n += 1
            if args.max_lines and n >= args.max_lines:
                break

    t0 = time.time()
    tok = SyllableAwareTeluguTokenizer.train(
        lines(),
        vocab_size=args.vocab_size,
        num_bpe_merges=args.bpe_merges,
        min_akshara_freq=args.min_akshara_freq,
        min_pair_freq=args.min_pair_freq,
        foreign=args.foreign,
        extra_aksharas=extra,
        verbose=True,
    )
    tok.save(args.out)
    print(f"[done] vocab_size={tok.vocab_size} saved -> {args.out} "
          f"({time.time() - t0:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
