"""Evaluate a finished run: validation and test NELBO on more canvases, and a sampling study.

    uv run python -m mdlm.final_eval --run pilot120m

Loads the EMA weights of the run's newest checkpoint and writes runs/<run>/final_eval/:

  eval.json             NELBO, perplexity bound, CE by mask rate and masked-token accuracy on the
                        validation split and on the untouched test split (512 fixed canvases per source)
  sampling_study.json   per sampler setting: judge gen-PPL and the sample metrics of 64 samples, plus
                        the judge's reference values on real and word-shuffled validation text
  samples/<setting>.txt the samples themselves

The settings vary the number of denoising steps (256, 512, 1,024), the unmasking order (ancestral,
confidence) and the temperature (1.0, 0.9), to tell whether sample quality is limited by the sampler
or by the model. The judge (google/gemma-3-1b-pt) runs on the GPU in float32, the precision of the
training-time judge on the CPU, so its numbers stay comparable with judge.jsonl.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path

import torch

from tokenizer import load_default

from .checkpoint import load_latest
from .data import fixed_canvases
from .diffusion import invalid_bias
from .judge import JUDGE, perplexity
from .metrics import sample_metrics
from .model import Denoiser, ModelConfig
from .sampling import sample
from .train import ROOT, _known_words, evaluate

SETTINGS = [                        # (name, unmasking order, denoising steps, temperature)
    ("ancestral-256", "ancestral", 256, 1.0),      # the setting used during training
    ("ancestral-512", "ancestral", 512, 1.0),
    ("ancestral-1024", "ancestral", 1024, 1.0),
    ("confidence-256", "confidence", 256, 1.0),
    ("confidence-512", "confidence", 512, 1.0),
    ("ancestral-512-t0.9", "ancestral", 512, 0.9),
]
SOURCES = ("sangraha", "indiccorp", "wikipedia")


class Tempered:
    """The sampler's view of a Denoiser whose logits are divided by a temperature."""

    def __init__(self, model: Denoiser, temperature: float):
        self.model, self.temperature = model, temperature

    def hidden(self, x):
        return self.model.hidden(x)

    def logits(self, h):
        return self.model.logits(h) / self.temperature


def judge_texts(ids: list[list[int]], tok) -> list[str]:
    """What the training-time judge scores: <bos> dropped, <eos> as a line break."""
    return [tok.decode(s, skip_special=False).replace("<bos>", "").replace("<eos>", "\n").strip() for s in ids]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--token-dir", type=Path, default=ROOT.parent / "pretraining_datasets" / "tokens")
    ap.add_argument("--canvases", type=int, default=512, help="fixed canvases per source for val and test")
    ap.add_argument("--samples", type=int, default=64, help="samples per sampler setting")
    ap.add_argument("--batch", type=int, default=32, help="samples generated per call")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    device = torch.device("cuda")
    torch.backends.cuda.matmul.allow_tf32 = True
    run_dir = ROOT / "runs" / args.run
    out = run_dir / "final_eval"
    (out / "samples").mkdir(parents=True, exist_ok=True)
    state = load_latest(run_dir, "cpu")
    step = state["step"]
    cfg = ModelConfig(**state["model_config"])
    model = Denoiser(cfg).to(device)
    model.load_state_dict(state["ema"])
    model.eval()
    del state
    tok = load_default()
    mask_id = tok.special_to_id["<mask>"]
    bias = invalid_bias(cfg.padded_vocab, tok.vocab_size, [mask_id, tok.pad_id, tok.unk_id], device)

    t0 = time.time()
    report = {"run": args.run, "step": step, "weights": "ema", "canvases_per_source": args.canvases}
    for split in ("val", "test"):
        canvases = {s: fixed_canvases(args.token_dir, s, split, args.canvases, cfg.max_len) for s in SOURCES}
        res = evaluate(model, canvases, mask_id, bias, 8, device)
        report[split] = {k.replace("val_", ""): v for k, v in res.items()}
        print(f"{split}: NELBO {report[split]['nelbo']:.4f} ({time.time() - t0:.0f} s)", flush=True)
    model.eval()
    (out / "eval.json").write_text(json.dumps(report, indent=2))

    known = _known_words(args.token_dir, tok)
    study, generated = {"step": step, "samples_per_setting": args.samples, "settings": {}}, {}
    for n, (name, strategy, steps, temperature) in enumerate(SETTINGS):
        gen = torch.Generator(device).manual_seed(args.seed * 1000 + n)
        net = model if temperature == 1.0 else Tempered(model, temperature)
        ids, nfe = [], 0
        t1 = time.time()
        for _ in range(0, args.samples, args.batch):
            x, f = sample(net, min(args.batch, args.samples - len(ids)), cfg.max_len, steps, mask_id, bias,
                          strategy=strategy, generator=gen)
            ids += x.tolist()
            nfe += f
        texts = [tok.decode(s) for s in ids]
        generated[name] = judge_texts(ids, tok)
        (out / "samples" / f"{name}.txt").write_text("\n\n==========\n\n".join(
            tok.decode(s, skip_special=False) for s in ids), encoding="utf-8")
        study["settings"][name] = {"strategy": strategy, "steps": steps, "temperature": temperature,
                                   "forward_passes": nfe, "seconds": round(time.time() - t1, 1),
                                   **sample_metrics(texts, ids, tok, known)}
        print(f"{name}: {time.time() - t1:.0f} s", flush=True)

    del model
    torch.cuda.empty_cache()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    jtok = AutoTokenizer.from_pretrained(JUDGE, local_files_only=True)
    judge = AutoModelForCausalLM.from_pretrained(JUDGE, local_files_only=True, dtype=torch.float32).to(device).eval()
    real = []
    for src in SOURCES:
        real += [tok.decode(c.tolist()) for c in fixed_canvases(args.token_dir, src, "val", 10)]
    rng = random.Random(0)
    shuffled = [" ".join(rng.sample(t.split(), len(t.split()))) for t in real]
    study["reference"] = {"judge": JUDGE, "real_telugu": perplexity(real, jtok, judge),
                          "word_shuffled": perplexity(shuffled, jtok, judge), "texts": len(real)}
    for name, texts in generated.items():
        study["settings"][name]["gen_ppl"] = perplexity(texts, jtok, judge)
        print(f"{name}: gen-PPL {study['settings'][name]['gen_ppl']:.1f}", flush=True)
    (out / "sampling_study.json").write_text(json.dumps(study, indent=2))
    print(f"done in {time.time() - t0:.0f} s -> {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
