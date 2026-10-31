"""Step 1 of PLAN.md: load DiffusionGemma, read its reply format, and run gates 1 and 2 before any training.

    ../.venv/bin/python -u check_model.py         # → runs/check_model.json (numbers only)

1. Load (experts resident in BF16): memory, canvas length, vocabulary, end and pad ids, the attention projections and
   which of them are tied between encoder and decoder.
2. The model's own generations (its sampler, `generate`) for 2 E6 val prompts: the reply and the token ids after it,
   which fix the end-of-reply fill of the training canvas.
   Their replies run past one canvas, so the end of a reply is read from a one-word answer (our canvas sampler with end
   tokens allowed, passes until the draft settles): the token after the reply and the fill after it.
3. Gate 2: the training forward (common.encode + denoise, gradients on) against the decoder's encode-then-denoise path
   (metrical_decoder.diffusion.canvas), on the same noisy canvas: max |logit difference|. (The first version called
   the model with the prompt and the canvas together: transformers' encoder then discards its causal masks; max
   difference 6.8, argmax agreement 90%.)
4. Gate 1: on 24 E6 val poems, the loss at t = 0.25, 0.5, 0.75 with the matching prompt, with another poem's prompt
   (same metre when possible), and on the poem with its words shuffled; poem positions and all positions.
5. LoRA (rank 16 on q, k, v, o): one training step with self-conditioning and gradient checkpointing: which
   parameters get gradients, time, peak memory.
"""
from __future__ import annotations

import json
import random

import torch

import common as C


def main() -> None:
    clock = C.timer()
    res = {}
    model, tok = C.load(resident=True)
    cfg = model.config
    L, V = cfg.canvas_length, cfg.text_config.vocab_size
    gc = model.generation_config
    eos = gc.eos_token_id if isinstance(gc.eos_token_id, (list, tuple)) else [gc.eos_token_id]
    special = {t: tok.convert_tokens_to_ids(t) for t in ("<eos>", "<pad>", "<turn|>", "<|turn>", "<bos>")}
    res["model"] = {"canvas_length": L, "vocab": V, "eos_ids": eos, "pad": cfg.text_config.pad_token_id,
                    "special": special, "gpu_gb_after_load": torch.cuda.memory_allocated() / 1e9,
                    "load_s": round(clock())}
    print(json.dumps(res["model"], ensure_ascii=False), flush=True)

    lins = C._linear_children(model)
    ptrs = {}
    for _, _, lin, name in lins:
        ptrs.setdefault(lin.weight.data_ptr(), []).append(name)
    res["projections"] = {"modules": len(lins), "distinct_weights": len(ptrs),
                          "example_tied_group": next(iter(ptrs.values()))}
    print(json.dumps(res["projections"], ensure_ascii=False), flush=True)

    val = [r for r in C.read_records("val") if C.t1_pool(r)]
    rng = random.Random(0)
    rng.shuffle(val)

    # 2. the model's own generations
    gens = []
    for r in val[:2]:
        ids = torch.tensor([C.prompt_ids(tok, r)], device="cuda")
        torch.manual_seed(0)
        with torch.no_grad():
            out = model.generate(input_ids=ids, max_new_tokens=L)
        seq = out.sequences[0] if hasattr(out, "sequences") else out[0]
        new = seq[ids.shape[1]:].tolist()
        gens.append({"metre": r["meter"], "reply": tok.decode(new, skip_special_tokens=False)[:600],
                     "tail_ids": new[-12:], "n_new": len(new),
                     "tail_tokens": tok.convert_ids_to_tokens(new[-12:])})
        print(json.dumps(gens[-1], ensure_ascii=False), flush=True)
    res["generations"] = gens

    # the canvas end convention, read from a reply that ends inside the block: a one-word answer, the model's own
    # passes (our canvas, end tokens allowed) until the draft settles, then the block's argmax
    from collections import Counter
    from metrical_decoder.diffusion.canvas import DiffusionGemmaCanvas
    cv = DiffusionGemmaCanvas(model, tok, forbid_end=False)
    probe = cv.prompt_ids([{"role": "user", "content": "నమస్కారం అని ఒకే పదంలో జవాబు ఇవ్వండి."}])
    cv.start(probe, seed=0)
    prev = None
    for k in range(48):
        ps = cv.denoise([], temperature=0.7)
        cur = ps.logits.argmax(-1).tolist()
        if cur == prev:
            break
        prev = cur
    block = prev
    first_end = next((i for i, x in enumerate(block) if x in eos + [special["<pad>"]]), len(block))
    after = block[first_end:]
    res["end_probe"] = {"passes": k + 1, "reply": tok.decode(block[:first_end]), "first_end_pos": first_end,
                        "end_tokens": tok.convert_ids_to_tokens(after[:4]),
                        "fill_counts": {tok.convert_ids_to_tokens(i): n for i, n in Counter(after[1:]).most_common(4)}}
    print("end probe:", json.dumps(res["end_probe"], ensure_ascii=False), flush=True)
    end_ids = [after[0]] if after else [special["<turn|>"]]
    fill = Counter(after[1:]).most_common(1)[0][0] if len(after) > 1 else special["<eos>"]
    res["canvas_rule"] = {"end_ids": end_ids, "fill_id": fill, "fill_token": tok.convert_ids_to_tokens(fill)}
    print("canvas rule", res["canvas_rule"], flush=True)

    # 3. gate 2: the training forward vs the decoder's path
    r = val[0]
    p = C.prompt_ids(tok, r)
    clean = torch.tensor([C.canvas_ids(tok, r, end_ids, fill, L)], device="cuda")
    g = torch.Generator(device="cuda").manual_seed(1)
    noisy = C.corrupt(clean, 0.5, V, g)
    with torch.no_grad():
        a = C.forward(model, torch.tensor([p], device="cuda"), noisy)[0]
        cv = DiffusionGemmaCanvas(model, tok)          # the decoder's own path (its masks, positions, cache)
        cv.start(p, seed=0)
        b = model(decoder_input_ids=noisy, self_conditioning_logits=None, decoder_attention_mask=cv.block_masks,
                  past_key_values=cv.cache, decoder_position_ids=cv.positions).logits[0]
    res["gate2_max_abs_logit_diff"] = float((a - b).abs().max())
    res["gate2_argmax_agreement"] = float((a.argmax(-1) == b.argmax(-1)).float().mean())
    print("gate 2:", res["gate2_max_abs_logit_diff"], res["gate2_argmax_agreement"], flush=True)

    # 4. gate 1: matching prompt vs another poem's prompt vs shuffled words
    items = []
    for r in val:
        c = C.canvas_ids(tok, r, end_ids, fill, L)
        if c is not None:
            items.append((r, c))
        if len(items) == 24:
            break
    by_m = {}
    for r, _ in items:
        by_m.setdefault(r["meter"], []).append(r)
    rows = {}
    for t in (0.25, 0.5, 0.75):
        acc = {"matched": [], "other_prompt": [], "shuffled_words": []}
        for k, (r, c) in enumerate(items):
            same = [o for o in by_m[r["meter"]] if o["id"] != r["id"]] or [o for o, _ in items if o["id"] != r["id"]]
            other = same[k % len(same)]
            words = " ".join(r["lines"]).split()
            random.Random(k).shuffle(words)
            n = len(r["lines"])
            per = max(1, len(words) // n)
            sh = dict(r, lines=[" ".join(words[i * per:(i + 1) * per if i < n - 1 else None]) for i in range(n)])
            csh = C.canvas_ids(tok, sh, end_ids, fill, L) or c
            n_poem = len(tok(C.to_model("\n".join(r["lines"])), add_special_tokens=False).input_ids)
            for key, prompt_rec, canvas in (("matched", r, c), ("other_prompt", other, c), ("shuffled_words", r, csh)):
                g = torch.Generator(device="cuda").manual_seed(1000 + k)
                with torch.no_grad():
                    ce = C.diffusion_loss(model, torch.tensor([C.prompt_ids(tok, prompt_rec)], device="cuda"),
                                          torch.tensor([canvas], device="cuda"), t, False, g, reduce=False)[0]
                acc[key].append((float(ce[:n_poem].mean()), float(ce.mean())))
        rows[str(t)] = {k: {"poem_positions": sum(x for x, _ in v) / len(v), "all_positions": sum(y for _, y in v) / len(v)}
                        for k, v in acc.items()}
        print(f"gate 1, t={t}:", json.dumps(rows[str(t)]), flush=True)
    res["gate1"] = rows

    # 5. LoRA: one training step
    adapters = C.inject_lora(model, r=16, alpha=32)
    params = [p for m in {id(a): a for a in adapters.values()}.values() for p in (m.A, m.B)]
    res["lora"] = {"adapters": len({id(a) for a in adapters.values()}), "wrapped_sites": len(C._linear_children(model)),
                   "params_M": sum(p.numel() for p in params) / 1e6}
    model.gradient_checkpointing_enable()
    model.train()
    torch.cuda.reset_peak_memory_stats()
    times = []
    for step in range(3):
        r, c = items[step]
        tt = C.timer()
        g = torch.Generator(device="cuda").manual_seed(step)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = C.diffusion_loss(model, torch.tensor([C.prompt_ids(tok, r)], device="cuda"),
                                    torch.tensor([c], device="cuda"), 0.5, step % 2 == 0, g)
        loss.backward()
        torch.cuda.synchronize()
        times.append(round(tt(), 2))
    with_grad = sum(p.grad is not None and float(p.grad.abs().sum()) > 0 for p in params)
    frozen_grads = sum(p.grad is not None for p in model.parameters() if not any(p is q for q in params))
    res["lora"].update(step_seconds=times, peak_gpu_gb=torch.cuda.max_memory_allocated() / 1e9,
                       params_with_gradient=f"{with_grad}/{len(params)}", frozen_params_with_grad=frozen_grads)
    print("lora:", json.dumps(res["lora"]), flush=True)
    res["seconds"] = round(clock())
    C.RUNS.mkdir(exist_ok=True)
    (C.RUNS / "check_model.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"done in {res['seconds']} s", flush=True)


if __name__ == "__main__":
    main()
