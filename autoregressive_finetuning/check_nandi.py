"""Step 1 of PLAN.md: the checks on the downloaded Nandi-Mini-150M, on the CPU.

    ../.venv/bin/python check_nandi.py                 # all checks
    ../.venv/bin/python check_nandi.py --no-model      # tokenizer and code checks only

1. Code: a scan of the three custom files for network, file, process and eval calls (the reading itself is in
   results/step1_checks.md).
2. Tokenizer: the wrapper's `<|im_start|> ` prefix against nandi.encode; newline and space ids; round trip of
   10k training poems; which Telugu characters whole tokens can spell; how many canonical tokens of the poems
   fall outside the decoder's slice (partial UTF-8 ids); token boundaries of the T1 layout.
3. Model (bf16 and fp32): parameter count, tied and shared weights, finite logits on 10 prompts, bf16 against
   fp32, right padding against no padding, one backward pass, and greedy continuations of a few first lines.

Writes results/step1_checks.json (numbers only; the reading notes are in results/step1_checks.md) and
runs/step1/samples.txt (generated text, not committed).
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import re
import time

import nandi
from nandi import BOS, E6_RECORDS, EOS, HERE, NEWLINE_ID, SPACE_ID

SEED = 20261018
RISKY = re.compile(r"requests|urllib|http[s]?://(?!www\.apache\.org)|socket|subprocess|os\.system|open\(|exec\(|"
                   r"eval\(|torch\.load|pickle|download|hf_hub|__import__|getenv|environ")


def sample_records(split: str, n: int, seed: int = SEED) -> list[dict]:
    """A uniform sample of n records with poem lines (reservoir), or all of a small split."""
    rng, keep, seen = random.Random(seed), [], 0
    with open(E6_RECORDS / f"{split}.jsonl", encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            if not r.get("lines"):
                continue
            seen += 1
            if len(keep) < n:
                keep.append(r)
            elif rng.random() < n / seen:
                keep[rng.randrange(n)] = r
    return keep


def check_code() -> dict:
    out = {}
    for name in ("modeling_nandi.py", "configuration_nandi.py", "tokenization_nandi.py"):
        text = (nandi.snapshot() / name).read_text(encoding="utf-8")
        hits = [f"{i}: {ln.strip()}" for i, ln in enumerate(text.splitlines(), 1) if RISKY.search(ln)]
        out[name] = {"lines": len(text.splitlines()), "risky_lines": hits}
    return out


def check_tokenizer(train: list[dict], held: list[dict]) -> dict:
    from transformers import AutoTokenizer
    tok = nandi.load_tokenizer()
    out: dict = {}
    wrapper = AutoTokenizer.from_pretrained(str(nandi.snapshot()), trust_remote_code=True, local_files_only=True)
    texts = ["\n".join(r["lines"]) for r in train[:200]]
    out["wrapper_encode_equal"] = sum(wrapper.encode(t) == nandi.encode(t, tok) for t in texts)
    out["wrapper_call_equal"] = sum(wrapper(t)["input_ids"] == nandi.encode(t, tok) for t in texts)
    out["wrapper_n"] = len(texts)
    out["wrapper_decode_keeps_space"] = wrapper.decode(nandi.encode(texts[0], tok), skip_special_tokens=True) == " " + texts[0]
    out["newline_id"], out["space_id"] = tok.encode("\n", add_special_tokens=False).ids, tok.encode(" ", add_special_tokens=False).ids
    assert out["newline_id"] == [NEWLINE_ID] and out["space_id"] == [SPACE_ID]

    ok = sum(nandi.decode(nandi.encode(t, tok), tok) == t for t in ("\n".join(r["lines"]) for r in train))
    out["round_trip"] = [ok, len(train)]

    V = tok.get_vocab_size()
    texts_by_id = [tok.decode([i]) for i in range(V)]
    partial = {i for i, s in enumerate(texts_by_id) if "�" in s}
    index = nandi.token_index(tok)
    slice_ids = set(index.ids)
    spellable = set("".join(index.texts))
    out["vocab"], out["partial_ids"], out["slice_size"] = V, len(partial), index.size

    def corpus(recs, name):
        chars = unspell = tokens = outside = poems_out = poems_unspell = 0
        missing = collections.Counter()
        for r in recs:
            text = "\n".join(r["lines"])
            cs = [c for c in text if "ఀ" <= c <= "౿"]
            bad = [c for c in cs if c not in spellable]
            ids = tok.encode(text, add_special_tokens=False).ids
            o = sum(i not in slice_ids for i in ids)
            chars += len(cs); unspell += len(bad); missing.update(bad); poems_unspell += bool(bad)
            tokens += len(ids); outside += o; poems_out += bool(o)
        out[name] = {"poems": len(recs), "telugu_chars": chars, "chars_spellable_pct": 100 * (1 - unspell / chars),
                     "poems_with_unspellable_char": poems_unspell, "unspellable": dict(missing.most_common()),
                     "tokens": tokens, "tokens_outside_slice_pct": 100 * outside / tokens,
                     "poems_with_token_outside_slice": poems_out,
                     "poems_with_token_outside_slice_pct": 100 * poems_out / len(recs)}
    corpus(train, "coverage_train_sample")
    corpus(held, "coverage_held_out")

    crossed = 0
    lengths = []
    for r in held + train:
        if not r.get("meaning"):
            continue
        ids, loss = nandi.encode_t1(r, tok=tok)
        p = nandi.prompt_ids(r, tok=tok)
        crossed += ids[:len(p)] != p or loss[len(p) - 1] or not loss[len(p)]
        lengths.append(len(ids))
    lengths.sort()
    out["t1_prefix_mismatch"] = [crossed, len(lengths)]
    out["t1_tokens"] = {"p50": lengths[len(lengths) // 2], "p99": lengths[int(0.99 * len(lengths))],
                        "max": lengths[-1], "over_1024": sum(n > 1024 for n in lengths)}
    return out


def check_model(held: list[dict], samples_path) -> dict:
    import torch
    torch.manual_seed(SEED)
    out: dict = {}
    t0 = time.time()
    m32 = nandi.load_model("float32").eval()
    out["load_s"] = round(time.time() - t0, 1)
    out["class"] = type(m32).__name__
    out["attn_implementation"] = m32.config._attn_implementation
    out["params"] = sum(p.numel() for p in m32.parameters())
    out["params_embedding"] = m32.model.embed_tokens.weight.numel()
    out["lm_head_tied"] = m32.lm_head.weight.data_ptr() == m32.model.embed_tokens.weight.data_ptr()
    out["unique_layers"] = len(m32.model.layers)
    out["layer_applications"] = len(m32.model.layers) * m32.config.layer_sharing_repeats
    out["weights_dtype_on_disk"] = str(nandi.load_model("bfloat16").model.layers[0].mlp.up_proj.weight.dtype)

    recs = [r for r in held if r.get("meaning")][:10]
    prompts = [nandi.prompt_ids(r) for r in recs]
    finite, max_abs_diff, top1_agree = 0, 0.0, 0
    m16 = nandi.load_model("bfloat16").eval()
    with torch.no_grad():
        for p in prompts:
            x = torch.tensor([p])
            a, b = m32(x).logits[0, -1], m16(x).logits[0, -1].float()
            finite += bool(torch.isfinite(a).all() and torch.isfinite(b).all())
            max_abs_diff = max(max_abs_diff, (a - b).abs().max().item())
            top1_agree += int(a.argmax() == b.argmax())
    out["finite_logits"] = [finite, len(prompts)]
    out["bf16_vs_fp32"] = {"max_abs_logit_diff": round(max_abs_diff, 3), "top1_agree": top1_agree}

    # right padding with an attention mask gives the same logits on the real tokens
    a, b = prompts[0], prompts[1]
    L = max(len(a), len(b))
    ids = torch.full((2, L), nandi.PAD)
    mask = torch.zeros((2, L), dtype=torch.long)
    for k, p in enumerate((a, b)):
        ids[k, :len(p)] = torch.tensor(p); mask[k, :len(p)] = 1
    with torch.no_grad():
        batched = m32(ids, attention_mask=mask).logits
        single = [m32(torch.tensor([p])).logits[0] for p in (a, b)]
    out["right_padding_max_diff"] = max((batched[k, :len(p)] - single[k]).abs().max().item()
                                        for k, p in enumerate((a, b)))

    # one training step's backward: loss on the poem only, gradients finite on every parameter
    m32.train()
    seq, loss_mask = nandi.encode_t1(recs[0])
    x = torch.tensor([seq])
    labels = torch.tensor([[t if keep else -100 for t, keep in zip(seq, loss_mask)]])
    loss = m32(x, labels=labels).loss
    loss.backward()
    grads = [p.grad for p in m32.parameters() if p.requires_grad]
    out["backward"] = {"loss_nats_per_token": round(loss.item(), 3),
                       "params_with_grad": sum(g is not None for g in grads), "params": len(grads),
                       "all_finite": all(g is None or bool(torch.isfinite(g).all()) for g in grads)}
    m32.zero_grad(set_to_none=True)
    m32.eval()

    # greedy continuations of first lines (zero-shot, plain text: no header)
    with open(samples_path, "w", encoding="utf-8") as fh:
        for r in held[:5]:
            p = nandi.encode(r["lines"][0] + "\n")
            with torch.no_grad():
                g = m16.generate(torch.tensor([p]), max_new_tokens=60, do_sample=False, eos_token_id=EOS,
                                 pad_token_id=nandi.PAD)
            fh.write(f"## {r['id']} ({r.get('meter')})\nprompt: {r['lines'][0]}\n"
                     f"model:  {nandi.decode(g[0, len(p):].tolist())}\ngold:   {' / '.join(r['lines'][1:])}\n\n")
        for r in recs[:3]:
            p = nandi.prompt_ids(r)
            with torch.no_grad():
                g = m16.generate(torch.tensor([p]), max_new_tokens=80, do_sample=True, temperature=0.7, top_p=0.9,
                                 eos_token_id=EOS, pad_token_id=nandi.PAD)
            fh.write(f"## T1 prompt {r['id']} (sampled 0.7 / 0.9)\n{nandi.t1_header(r)}"
                     f"{nandi.decode(g[0, len(p):].tolist())}\n\n")
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-model", action="store_true", help="skip the model checks (no weights needed)")
    ap.add_argument("--train-sample", type=int, default=10_000)
    args = ap.parse_args()
    import torch
    torch.set_num_threads(4)                     # the GPU jobs' CPU workers share the cores

    train = sample_records("train", args.train_sample)
    held = sample_records("val", 10**9) + sample_records("test", 10**9)
    res = {"model": nandi.MODEL_ID, "revision": nandi.REVISION, "seed": SEED, "code": check_code(),
           "tokenizer": check_tokenizer(train, held)}
    weights = nandi.snapshot() / "model.safetensors"
    res["weights_bytes"] = weights.stat().st_size if weights.exists() else None
    if not args.no_model:
        assert res["weights_bytes"] == nandi.WEIGHTS_BYTES, "model.safetensors missing or incomplete"
        (HERE / "runs" / "step1").mkdir(parents=True, exist_ok=True)
        res["model_checks"] = check_model(held, HERE / "runs" / "step1" / "samples.txt")

    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / "step1_checks.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                                                        encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
