"""E1 (and the evaluations of E2): NELBO of a model on held-out poems and on their bhavams.

    ../.venv/bin/python eval_nelbo.py --model pilot --name e1_pilot
    ../.venv/bin/python eval_nelbo.py --model runs/<run>/final.pt --name e2_<run>

Protocol: exactly stage 1's (`mdlm.train.evaluate`, as used by `mdlm.final_eval`):
  - fixed canvases: the first N non-overlapping 512-token windows of a split; poems are short, so a
    window holds several, each as <bos> … <eos> (MDLM's wrapped setting, as in stage 1);
  - fixed times t spread evenly over (eps, 1) and fixed masks, so numbers compare across models;
  - NELBO in nats per token (exp(NELBO) bounds the perplexity), cross-entropy by mask-rate bin and
    masked-token accuracy at 15 / 50 / 85 % masking.

Sources, from prepare_poems.py:
  poems    held-out verse
  bhavam   the bhavams of the same held-out poems: modern prose with the same content

Reference: stage 1's own test split under the same protocol, 512 canvases per source (pilot report
§10.5): Sangraha 1.846, IndicCorp 1.729, Wikipedia 1.053, 1.783 weighted like the training mix.

Writes results/<name>.json (numbers only, no text).
"""
from __future__ import annotations

import argparse
import json
import time

import torch

from common import HERE, TOKENS, load_model, output_bias, special_ids, tokenizer, wait_for_memory
from mdlm.data import fixed_canvases
from mdlm.train import evaluate

STAGE1_TEST = {"sangraha": 1.846, "indiccorp": 1.729, "wikipedia": 1.053, "weighted_like_training": 1.783}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="pilot", help="'pilot' or a checkpoint written by finetune.py")
    ap.add_argument("--name", required=True, help="results/<name>.json")
    ap.add_argument("--split", default="test", choices=("val", "test"))
    ap.add_argument("--sources", nargs="+", default=["poems", "bhavam"])
    ap.add_argument("--canvases", type=int, default=512, help="fixed canvases per source")
    ap.add_argument("--micro", type=int, default=16)
    args = ap.parse_args(argv)

    wait_for_memory(8, "eval_nelbo")
    device = torch.device("cuda")
    torch.backends.cuda.matmul.allow_tf32 = True
    t0 = time.time()
    model, weights = load_model(args.model, device)
    model.eval()
    tok = tokenizer()
    bias = output_bias(model.cfg, tok, device)
    canvases = {s: fixed_canvases(TOKENS, s, args.split, args.canvases, model.cfg.max_len) for s in args.sources}
    res = evaluate(model, canvases, special_ids(tok)["mask"], bias, args.micro, device)
    out = {"model": args.model, "weights": weights, "split": args.split,
           "canvases": {s: len(c) for s, c in canvases.items()}, "seconds": round(time.time() - t0, 1),
           "results": res, "stage1_test_reference": STAGE1_TEST}
    path = HERE / "results" / f"{args.name}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    for s in args.sources:
        print(f"{s:7s} NELBO {res[f'val_nelbo/{s}']:.4f}  (bound on perplexity {res[f'val_ppl_bound/{s}']:.2f})")
    print(f"masked accuracy 15/50/85%: {res['masked_acc/15pct']:.3f} / {res['masked_acc/50pct']:.3f} / "
          f"{res['masked_acc/85pct']:.3f}  (all sources pooled)")
    print(f"-> {path} ({out['seconds']} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
