"""Generative perplexity of Telugu text under an external causal LM (default google/gemma-3-1b-pt).

    uv run python -m mdlm.judge --samples runs/<run>/samples/step_0010000.txt
    uv run python -m mdlm.judge --calibrate --token-dir ../pretraining_datasets/tokens

Gen-PPL only means something next to the judge's perplexity on real Telugu and on
the same text with its words shuffled; --calibrate prints both (the judge is
useful only if shuffling clearly raises its perplexity). The judge is loaded from
the local Hugging Face cache and never downloads anything.
"""
from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

import torch

from tokenizer import load_default

from .data import fixed_canvases

JUDGE = "google/gemma-3-1b-pt"


def load_judge(model_id: str = JUDGE, device: str = "cuda"):
    """On "cpu" the judge runs in float32 and leaves the GPU to a training run."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
    dtype = torch.bfloat16 if device == "cuda" else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_id, local_files_only=True, dtype=dtype).to(device).eval()
    return tok, model


@torch.no_grad()
def perplexity(texts: list[str], tok, model) -> float:
    """exp(mean NLL per judge token) over all texts; one text at a time, and the
    262k-wide log-softmax in chunks of positions, so it fits next to training on 8 GB."""
    nll, count = 0.0, 0
    for text in texts:
        ids = tok(text, return_tensors="pt")["input_ids"].to(model.device)
        logits = model(input_ids=ids).logits[0, :-1]
        target = ids[0, 1:]
        for lg, tg in zip(logits.split(256), target.split(256)):
            nll += float(torch.nn.functional.cross_entropy(lg.float(), tg, reduction="sum"))
        count += target.numel()
    return math.exp(nll / count)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--samples", type=Path, help="a samples/step_*.txt file written by mdlm.train")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--token-dir", type=Path)
    ap.add_argument("--n", type=int, default=64)
    ap.add_argument("--judge", default=JUDGE)
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    ap.add_argument("--threads", type=int, default=8, help="CPU threads when --device cpu")
    args = ap.parse_args(argv)
    torch.set_num_threads(args.threads)
    jtok, judge = load_judge(args.judge, args.device)
    if args.calibrate:
        ours = load_default()
        real = []
        for src in ("sangraha", "indiccorp", "wikipedia"):
            real += [ours.decode(c.tolist()) for c in fixed_canvases(args.token_dir, src, "val", args.n // 3)]
        rng = random.Random(0)
        shuffled = [" ".join(rng.sample(t.split(), len(t.split()))) for t in real]
        print(f"judge {args.judge}: real Telugu PPL {perplexity(real, jtok, judge):.1f}, "
              f"word-shuffled PPL {perplexity(shuffled, jtok, judge):.1f}  ({len(real)} texts)")
    if args.samples:
        texts = [t.replace("<bos>", "").replace("<eos>", "\n").strip()
                 for t in args.samples.read_text(encoding="utf-8").split("\n\n==========\n\n")]
        print(f"{args.samples}: gen-PPL {perplexity(texts, jtok, judge):.1f} ({len(texts)} samples)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
