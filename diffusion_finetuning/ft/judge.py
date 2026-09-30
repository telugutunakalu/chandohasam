"""Meaning judge (PLAN §8.2), local models only (no API calls).

    # is the judge any good? matched vs mismatched meanings of real val poems must separate (AUC >= 0.9)
    python -m ft.judge validate --split val --n 100 [--llm google/gemma-3-12b-it]
    # judge a prediction file (ft.evaluate decode / retrieval / reference output)
    python -m ft.judge score --pred runs/s2-.../eval/val.jsonl [--llm google/gemma-3-12b-it]

Round trip: the local LLM writes a plain-Telugu meaning for the poem; that meaning is compared
with the input meaning by LaBSE cosine (and with the English meaning, cross-lingually), and, with
--llm, rated 1-5 by the same LLM. Without --llm only the direct LaBSE similarity of the poem to
the meaning is reported (a weak signal; validate it before relying on it).

Hardware: LaBSE runs on the laptop. gemma-3-12b-it needs ~24 GB (bf16): run it on the DGX Spark
(or pass a smaller --llm and check its AUC first).
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np

from . import DATA_DIR

EMBEDDER = "sentence-transformers/LaBSE"
EXPLAIN = ("కింది తెలుగు పద్యానికి భావాన్ని సరళమైన తెలుగు గద్యంలో రాయండి. భావం మాత్రమే రాయండి.\n\n"
           "పద్యం:\n{poem}\n\nభావం:")
RATE = ("Here are two Telugu passages.\nA: {a}\nB: {b}\n"
        "On a scale of 1 to 5, how closely does B convey the same meaning as A? "
        "(1 = unrelated, 5 = the same meaning). Answer with one digit only.")


class Embedder:
    def __init__(self, name: str = EMBEDDER, device: str | None = None):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(name, local_files_only=True)
        self.model = AutoModel.from_pretrained(name, local_files_only=True).to(self.device).eval()

    def __call__(self, texts: list[str], batch: int = 32) -> np.ndarray:
        out = []
        with self.torch.no_grad():
            for i in range(0, len(texts), batch):
                enc = self.tok(texts[i:i + batch], padding=True, truncation=True, max_length=256, return_tensors="pt").to(self.device)
                v = self.model(**enc).pooler_output
                out.append(self.torch.nn.functional.normalize(v, dim=-1).float().cpu().numpy())
        return np.concatenate(out) if out else np.zeros((0, 768), np.float32)


class LLM:
    def __init__(self, name: str, device: str | None = None):
        import torch
        from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
        self.torch = torch
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(name, local_files_only=True)
        cfg = AutoConfig.from_pretrained(name, local_files_only=True)
        if hasattr(cfg, "vision_config"):                     # gemma-3 4b/12b/27b-it: text generation through the VLM class
            from transformers import AutoModelForImageTextToText as Auto
        else:
            Auto = AutoModelForCausalLM
        self.model = Auto.from_pretrained(name, local_files_only=True, dtype=torch.bfloat16).to(device).eval()

    def __call__(self, prompt: str, max_new_tokens: int = 400) -> str:
        if getattr(self.tok, "chat_template", None):
            text = self.tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False,
                                                add_generation_prompt=True)
        else:
            text = prompt
        enc = self.tok(text, return_tensors="pt").to(self.model.device)
        with self.torch.no_grad():
            out = self.model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False)
        return self.tok.decode(out[0, enc["input_ids"].shape[1]:], skip_special_tokens=True).strip()

    def rate(self, a: str, b: str) -> float:
        m = re.search(r"[1-5]", self(RATE.format(a=a, b=b), max_new_tokens=5))
        return float(m.group(0)) if m else float("nan")


def auc(pos: list[float], neg: list[float]) -> float:
    """P(score of a matched pair > score of a mismatched pair), ties counted half."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if not len(pos) or not len(neg):
        return float("nan")
    return float(((pos[:, None] > neg[None]).sum() + 0.5 * (pos[:, None] == neg[None]).sum()) / (len(pos) * len(neg)))


def cmd_validate(args) -> int:
    from .evaluate import eval_items
    items = eval_items(args.split, args.n, args.data_dir)
    emb = Embedder()
    poems = ["\n".join(r["lines"]) for r in items]
    meanings = [r["meaning"] for r in items]
    shift = meanings[1:] + meanings[:1]                           # every poem paired with another poem's meaning
    rep = {"items": len(items)}
    P, M, S = emb(poems), emb(meanings), emb(shift)
    rep["direct_labse_auc"] = auc(list((P * M).sum(1)), list((P * S).sum(1)))
    if args.llm:
        llm = LLM(args.llm)
        expl = [llm(EXPLAIN.format(poem=p)) for p in poems]
        E = emb(expl)
        rep["roundtrip_labse_auc"] = auc(list((E * M).sum(1)), list((E * S).sum(1)))
        rep["llm_rating_auc"] = auc([llm.rate(m, e) for m, e in zip(meanings, expl)],
                                    [llm.rate(s, e) for s, e in zip(shift, expl)])
        rep["llm"] = args.llm
        rep["examples"] = [{"poem": p, "meaning": m, "llm_meaning": e} for p, m, e in list(zip(poems, meanings, expl))[:5]]
    out = args.data_dir / f"judge_validate_{args.split}.json"
    out.write_text(json.dumps(rep, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k != "examples"}, indent=2))
    return 0


def cmd_score(args) -> int:
    rows = [json.loads(l) for l in args.pred.open(encoding="utf-8")]
    emb = Embedder()
    poems = ["\n".join(r["poem"]) for r in rows]
    M = emb([r["meaning"] for r in rows])
    P = emb(poems)
    for r, s in zip(rows, (P * M).sum(1)):
        r["judge"] = {"direct_labse": float(s)}
    if args.llm:
        llm = LLM(args.llm)
        expl = [llm(EXPLAIN.format(poem=p)) if p.strip() else "" for p in poems]
        E = emb(expl)
        en = [r.get("meaning_en") or "" for r in rows]
        EN = emb(en)
        for r, e, sm, se in zip(rows, expl, (E * M).sum(1), (E * EN).sum(1)):
            r["judge"] |= {"llm_meaning": e, "roundtrip_labse": float(sm),
                           "roundtrip_labse_en": float(se) if r.get("meaning_en") else None,
                           "llm_rating": llm.rate(r["meaning"], e) if e else float("nan")}
    out = args.pred.with_suffix(".judged.jsonl")
    with out.open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    keys = sorted({k for r in rows for k, v in r["judge"].items() if isinstance(v, (int, float)) and v is not None})
    summary = {k: float(np.nanmean([r["judge"][k] for r in rows if r["judge"].get(k) is not None])) for k in keys}
    print(json.dumps(summary, indent=2))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate")
    v.add_argument("--split", default="val")
    v.add_argument("--n", type=int, default=100)
    s = sub.add_parser("score")
    s.add_argument("--pred", type=Path, required=True)
    for p in (v, s):
        p.add_argument("--llm", default="", help="local instruction model id, e.g. google/gemma-3-12b-it")
        p.add_argument("--data-dir", type=Path, default=DATA_DIR)
    args = ap.parse_args(argv)
    return cmd_validate(args) if args.cmd == "validate" else cmd_score(args)


if __name__ == "__main__":
    raise SystemExit(main())
