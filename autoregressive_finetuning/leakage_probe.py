"""Step 2 of PLAN.md: does the base Nandi already know our held-out poems? And its zero-shot likelihoods.

    ../.venv/bin/python leakage_probe.py                       # the base model
    ../.venv/bin/python leakage_probe.py --weights runs/nandi-t1/snapshots/ema_step_0008225.pt --name ft

1. **Leakage.** Every val and test poem with at least two lines: the model continues its first line greedily
   (plain text, `<|im_start|> line1⏎`, no header; fp32, batches of equal prompt length, so the result does not
   depend on batching). Measure: the longest run of aksharas (our akshara tokenizer,
   spaces and newlines dropped) shared by the continuation and the rest of the real poem. Reported by corpus as the
   share of poems with a run of ≥ 12 and ≥ 24 aksharas (a vṛtta line is ~20). The poems of
   ../diffusion_finetuning/data/e6/leakage.json with a poem hit in our pretraining corpora are on the web, so they
   are the positive control. Poems with a run of ≥ 24 go to results/nandi_leakage_exclude.json, which every model's
   evaluation then leaves out.
2. **Zero-shot likelihood** (the "before" row): val poems given their T1 prompt, and given the metre only (T0), in
   nats per MDLM token (E6's unit); val bhāvams as plain prose, per MDLM token of the bhāvam.

Writes results/step2_leakage{_<name>}.{md,json} (numbers and ids only) and runs/step2/generations{_<name>}.jsonl
(the continuations; not committed).
"""
from __future__ import annotations

import argparse
import collections
import difflib
import json
import time

import torch

import nandi
from nandi import E6_RECORDS, EOS, HERE, PAD

LEAKAGE = E6_RECORDS.parent / "leakage.json"
THRESHOLDS = (12, 24)
EXCLUDE_AT = 24


def aksharas(text: str) -> list[int]:
    tok = nandi.mdlm_tokenizer()
    drop = {tok.bos_id, tok.eos_id, tok.encode(" ")[0], tok.encode("\n")[0]}
    return [i for i in tok.encode(text) if i not in drop]


def longest_shared_run(a: list[int], b: list[int]) -> int:
    if not a or not b:
        return 0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b)).size


def corpus(rec_id: str) -> str:
    return rec_id.split(":")[0].replace("dataset/", "")


@torch.no_grad()
def continuations(model, recs: list[dict], device, batch: int, log_every: int = 20) -> list[str]:
    """Greedy continuation of each poem's first line. A batch holds prompts of one token length only, so nothing is
    padded (left padding changed the output of this model's generate: 2 of 8 rows differed from unbatched)."""
    tok = nandi.load_tokenizer()
    prompts = [nandi.encode(r["lines"][0] + "\n", tok) for r in recs]
    budget = [min(320, int(1.5 * len(tok.encode("\n".join(r["lines"][1:]), add_special_tokens=False).ids)) + 8)
              for r in recs]
    by_len = collections.defaultdict(list)
    for i in sorted(range(len(recs)), key=lambda i: budget[i]):
        by_len[len(prompts[i])].append(i)
    batches = [rows[s:s + batch] for _, rows in sorted(by_len.items()) for s in range(0, len(rows), batch)]
    out: list = [None] * len(recs)
    t0, done = time.time(), 0
    for n, rows in enumerate(batches):
        ids = torch.tensor([prompts[i] for i in rows], device=device)
        g = model.generate(input_ids=ids, attention_mask=torch.ones_like(ids), do_sample=False,
                           max_new_tokens=max(budget[i] for i in rows), eos_token_id=EOS, pad_token_id=PAD)
        for k, i in enumerate(rows):
            new = g[k, ids.shape[1]:].tolist()[:budget[i]]
            out[i] = nandi.decode(new[:new.index(EOS)] if EOS in new else new, tok)
        done += len(rows)
        if n % log_every == 0:
            print(f"  continuations {done}/{len(recs)} ({time.time() - t0:.0f} s)", flush=True)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--weights", default="", help="a finetune.py EMA snapshot or checkpoint, or a downloaded Hugging "
                    "Face folder (default: the base model)")
    ap.add_argument("--name", default="", help="suffix of the output names")
    ap.add_argument("--batch", type=int, default=96)
    ap.add_argument("--limit", type=int, default=0, help="only the first N poems (a smoke test)")
    args = ap.parse_args()
    device = torch.device("cuda")
    sfx = f"_{args.name}" if args.name else ""
    torch.backends.cuda.matmul.allow_tf32 = False              # fp32 throughout: in bf16, 4 of 16 greedy continuations
    torch.backends.cudnn.allow_tf32 = False                    # changed with the batch size (near-ties); in fp32, none
    model = nandi.load_model("float32", "cuda", args.weights or None).eval()
    tok = nandi.load_tokenizer()

    recs = [json.loads(l) for split in ("val", "test") for l in open(E6_RECORDS / f"{split}.jsonl", encoding="utf-8")]
    recs = [r for r in recs if len(r.get("lines") or []) >= 2]
    if args.limit:
        recs = recs[:args.limit]
    leak = json.loads(LEAKAGE.read_text(encoding="utf-8"))["items"]
    control = {k for k, v in leak.items() if v.get("poem")}

    print(f"leakage probe: {len(recs)} poems ({len(control & {r['id'] for r in recs})} positive controls)", flush=True)
    t0 = time.time()
    gens = continuations(model, recs, device, args.batch)
    runs = [longest_shared_run(aksharas(g), aksharas("\n".join(r["lines"][1:]))) for r, g in zip(recs, gens)]
    t_probe = time.time() - t0

    groups = collections.defaultdict(list)
    for r, n in zip(recs, runs):
        groups[corpus(r["id"])].append(n)
        groups["all"].append(n)
        if r["id"] in control:
            groups["positive control (leakage.json poem hits)"].append(n)
    table = {g: {"poems": len(v), **{f"run_ge_{t}_pct": 100 * sum(x >= t for x in v) / len(v) for t in THRESHOLDS},
                 "max_run": max(v), "mean_run": sum(v) / len(v)} for g, v in groups.items()}
    exclude = sorted(r["id"] for r, n in zip(recs, runs) if n >= EXCLUDE_AT)

    # zero-shot likelihoods on val (the "before" row)
    val = [json.loads(l) for l in open(E6_RECORDS / "val.jsonl", encoding="utf-8")]
    items = nandi.val_items(val, tok)
    lik = nandi.evaluate_t1(model, items, device)
    prose = [r for r in val if r.get("meaning")]
    sums = nandi.nll_sums(model, [(nandi.encode(r["meaning"], tok) + [EOS], [False] + [True] * (len(nandi.encode(r["meaning"], tok))))
                                  for r in prose], device)
    lik["val_nll/bhavam_prose"] = sum(s for s, _ in sums) / sum(len(nandi.mdlm_tokenizer().encode(r["meaning"])) for r in prose)
    lik["val_items"], lik["bhavam_items"] = len(items), len(prose)

    res = {"weights": args.weights or f"{nandi.MODEL_ID}@{nandi.REVISION[:7]} (base)", "poems": len(recs),
           "probe_seconds": round(t_probe), "by_corpus": table, "excluded_at": EXCLUDE_AT, "excluded": exclude,
           "likelihood": lik}
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "runs" / "step2").mkdir(parents=True, exist_ok=True)
    with open(HERE / "runs" / "step2" / f"generations{sfx}.jsonl", "w", encoding="utf-8") as fh:
        for r, g, n in zip(recs, gens, runs):
            fh.write(json.dumps({"id": r["id"], "run": n, "prompt": r["lines"][0], "continuation": g}, ensure_ascii=False) + "\n")
    (HERE / "results" / f"step2_leakage{sfx}.json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n",
                                                                encoding="utf-8")
    if not args.name and not args.limit:
        (HERE / "results" / "nandi_leakage_exclude.json").write_text(
            json.dumps({"rule": f"longest shared akshara run >= {EXCLUDE_AT} (leakage_probe.py, base model)",
                        "ids": exclude}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    md = [f"# Step 2: leakage probe and zero-shot likelihood ({res['weights']})", "",
          f"{len(recs)} val + test poems; greedy continuation of the first line; longest akshara run shared with the "
          f"rest of the real poem. {t_probe:.0f} s.", "",
          "| corpus | poems | run ≥ 12 % | run ≥ 24 % | mean run | max run |", "|---|---|---|---|---|---|"]
    for g, d in sorted(table.items(), key=lambda kv: (kv[0] == "all", kv[0])):
        md.append(f"| {g} | {d['poems']} | {d['run_ge_12_pct']:.1f} | {d['run_ge_24_pct']:.1f} | {d['mean_run']:.1f} | {d['max_run']} |")
    md += ["", f"Excluded from every model's evaluation (run ≥ {EXCLUDE_AT}): **{len(exclude)}** poems.", "",
           "| zero-shot likelihood (val) | nats |", "|---|---|"]
    for k in ("val_nll/T1", "val_nll/T0", "val_nll_tok/T1", "val_nll_tok/T0", "val_nll/bhavam_prose"):
        md.append(f"| {k} | {lik[k]:.3f} |")
    md += ["", "val_nll/*: per MDLM target token (E6's unit); val_nll_tok/*: per Nandi token. Not comparable as levels "
           "with the MDLM's NELBO (an upper bound); the T1-T0 gap is."]
    (HERE / "results" / f"step2_leakage{sfx}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md), flush=True)


if __name__ == "__main__":
    main()
