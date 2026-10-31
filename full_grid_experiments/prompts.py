"""The grid's prompts (PLAN.md §1): P1, each source poem's bhāvam re-told by Gemma-4 26B-A4B-it, with automatic checks.

    ../.venv/bin/python -u prompts.py                                   # the 183 source poems → prompts/p1.jsonl
    ../.venv/bin/python -u prompts.py --model google/gemma-4-E2B-it --device cpu --limit 2 --out smoke   # a smoke run
    ../.venv/bin/python -u prompts.py --reference grid100_new_test --ids prompts/grid100/p1_todo.json \
        --out prompts/grid100/p1                                      # the 100-prompt grid's 10 new Vemana poems

- **Source poems:** the 183 (metre, poem id) pairs of the E6 test evaluation (../diffusion_finetuning/runs/
  e6_120m_t1_test): held-out Padyarchana poems (../dataset), with their edition bhāvams (E6 records, test split).
- **Generation:** the user message is INSTRUCTION + the bhāvam, in the chat template with thinking off and the reply
  prefilled with the answer tag (a small model otherwise wrote an analysis and the rules first); sampling at
  temperature 0.3 (top-p 0.95), seed 42; a poem whose attempt fails a check gets up to two more attempts (seeds 43,
  44, temperature 0.7). Batches of --batch prompts, left-padded.
- **Checks** (every one must pass):
  1. telugu: no letter outside the Telugu block (no English, no transliteration);
  2. meaning: LaBSE similarity to the own bhāvam is the highest among all 183 bhāvams and at least the 99th
     percentile of the similarities between different source bhāvams (the threshold is in the summary);
  3. copy: at most 40% of the retelling's words of 2+ aksharas occur in the source bhāvam;
  4. gold: no run of 12 aksharas shared with the gold poem (spaces and line breaks ignored, as the memorisation
     measure);
  5. length: 0.6–1.4 × the source bhāvam's aksharas (the instruction asks for no longer than the source);
  6. fits: the MDLMs' T1 prefix with the retelling leaves room for 1.5 × the gold poem in their 512-token canvas
     (the rule by which ../diffusion_finetuning/constrained_sample.e6_prompts chose the source poems).
  The longest akshara run shared with the source bhāvam is reported as well (not a check: names repeat).
- **Kept:** the first attempt that passes every check, else the attempt with the fewest failed checks (flagged).

Writes prompts/p1.jsonl (one row per source poem), prompts/p1_attempts.jsonl (every attempt), prompts/summary.json
and prompts/p1_review.md (the summary and 30 seeded random prompts beside their sources, for the user's review).
Resumable: poems already in p1.jsonl are skipped. With --reference/--ids (the 100-prompt grid's new poems), the
meaning check ranks among the 183 and the new sources together; its threshold stays the 183's.
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import unicodedata
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "meter_engine"))
from metrical_decoder.diffusion.canvas import EMPTY_THOUGHT      # noqa: E402
from metrical_decoder.registers import _syllables                # noqa: E402

RUNS = REPO / "diffusion_finetuning" / "runs"
REFERENCE = "e6_120m_t1_test"
RECORDS = REPO / "diffusion_finetuning" / "data" / "e6" / "records" / "test.jsonl"
TELUGU = ("ఀ", "౿")
INSTRUCTION = """క్రింది భావాన్ని మీ సొంత మాటల్లో తిరిగి చెప్పండి.
నియమాలు:
1. అదే అర్థం, అవే సంఘటనలు, అవే పాత్రలు ఉండాలి. కొత్తగా ఏదీ చేర్చవద్దు, ఏదీ వదలవద్దు.
2. మూలంలోని వాక్యాలను, పదబంధాలను యథాతథంగా తీసుకోవద్దు. వేరే పదాలు వాడండి, వాక్యాల క్రమం మార్చవచ్చు. పాత్రల పేర్లు అలాగే ఉండవచ్చు.
3. సరళమైన తెలుగు వచనంలో, తెలుగు లిపిలో మాత్రమే వ్రాయండి. ఆంగ్ల పదాలు, రోమన్ అక్షరాలు వద్దు.
4. పొడవు మూలానికి సమానంగా లేదా కొంచెం తక్కువగా ఉండాలి; మూలం కంటే పొడవుగా వ్రాయవద్దు.
5. తిరిగి చెప్పిన భావాన్ని మాత్రమే ఇవ్వండి: శీర్షిక, విశ్లేషణ, వివరణ, ఉపోద్ఘాతం వద్దు.
6. జవాబును <భావం> మరియు </భావం> గుర్తుల మధ్య వ్రాయండి."""
OPEN, CLOSE = "<భావం>", "</భావం>"           # the reply is prefilled with OPEN and cut at CLOSE
COPY_MAX, GOLD_RUN, LENGTH = 0.40, 12, (0.6, 1.4)
MDLM_CANVAS = 512                    # ../diffusion_finetuning/constrained_sample.CANVAS
SEEDS, TEMPS = (42, 43, 44), (0.3, 0.7, 0.7)


# --------------------------------------------------------------------------- text measures
def aksharas(text: str) -> list[str]:
    """The text's aksharas, spaces, punctuation and line breaks ignored."""
    out = []
    for w in unicodedata.normalize("NFC", text).split():
        w = "".join(ch for ch in w if TELUGU[0] <= ch <= TELUGU[1])
        if w:
            out += _syllables(w)
    return out


def words(text: str) -> list[str]:
    out = []
    for w in unicodedata.normalize("NFC", text).split():
        w = "".join(ch for ch in w if TELUGU[0] <= ch <= TELUGU[1])
        if len(_syllables(w)) >= 2:
            out.append(w)
    return out


def longest_run(a: list[str], b: list[str]) -> int:
    """The longest run of aksharas shared by a and b (longest common substring)."""
    best, prev = 0, [0] * (len(b) + 1)
    for x in a:
        cur = [0] * (len(b) + 1)
        for j, y in enumerate(b, 1):
            if x == y:
                cur[j] = prev[j - 1] + 1
                best = max(best, cur[j])
        prev = cur
    return best


def foreign_letters(text: str) -> list[str]:
    return sorted({ch for ch in text if unicodedata.category(ch).startswith("L") and not TELUGU[0] <= ch <= TELUGU[1]})


def clean_reply(text: str) -> str:
    """The reply up to CLOSE (it starts after the prefilled OPEN), without a thinking channel, markdown emphasis or a
    leading label."""
    text = re.sub(r"<\|channel>.*?<channel\|>", "", text, flags=re.S)
    text = text.split(CLOSE)[0].replace(OPEN, "")
    text = text.replace("**", "").strip()
    return re.sub(r"^(తిరిగి చెప్పిన భావం|భావం)\s*[:：]\s*", "", text).strip()


def evict_page_cache(need_gb: float = 70) -> None:
    """On the GB10 CUDA counts cached file pages as used (its free memory is MemFree): when it reports less than
    ``need_gb`` free, drop the page cache of large files (../diffusion_pretraining/mdlm/checkpoint_eval.py)."""
    import torch
    if torch.cuda.is_available() and torch.cuda.mem_get_info()[0] / 2**30 < need_gb:
        sys.path.insert(0, str(REPO / "diffusion_pretraining"))
        from mdlm.checkpoint_eval import _evict_large_files
        _evict_large_files()


# --------------------------------------------------------------------------- generation
class Generator:
    def __init__(self, model_id: str, device: str):
        import transformers
        from transformers import AutoConfig, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model_id, local_files_only=True)
        self.tok.padding_side = "left"
        arch = (AutoConfig.from_pretrained(model_id, local_files_only=True).architectures or [None])[0]
        cls = getattr(transformers, arch)            # Gemma-4-it: Gemma4ForConditionalGeneration (all weights loaded)
        if device == "cuda":
            evict_page_cache()
        self.model = cls.from_pretrained(model_id, dtype=torch.bfloat16, device_map=device, local_files_only=True)
        self.model.eval()
        self.device = device

    def prompt(self, meaning: str) -> str:
        msgs = [{"role": "user", "content": f"{INSTRUCTION}\n\nభావం:\n{meaning}"}]
        text = self.tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        return (text if text.endswith(EMPTY_THOUGHT) else text + EMPTY_THOUGHT) + OPEN + "\n"

    @torch.no_grad()
    def __call__(self, meanings: list[str], seed: int, temperature: float) -> list[str]:
        enc = self.tok([self.prompt(m) for m in meanings], return_tensors="pt", padding=True,
                       add_special_tokens=False).to(self.device)
        longest = max(len(self.tok(m, add_special_tokens=False).input_ids) for m in meanings)
        torch.manual_seed(seed)
        out = self.model.generate(**enc, max_new_tokens=min(1024, 2 * longest + 64), do_sample=True,
                                  temperature=temperature, top_p=0.95, top_k=0)
        return [clean_reply(self.tok.decode(o[enc.input_ids.shape[1]:], skip_special_tokens=True)) for o in out]


# --------------------------------------------------------------------------- checks
class MDLMFit:
    """Tokens by which a T1 prompt with ``meaning`` overflows the MDLM canvas (≤ 0: it fits), by e6_prompts' rule."""

    def __init__(self):
        sys.path.insert(0, str(REPO / "diffusion_finetuning"))
        from common import tokenizer                              # ../diffusion_finetuning/common.py
        from ft.canvas import Vocab
        self.v = Vocab(tokenizer())
        self.records = {}
        for l in open(RECORDS, encoding="utf-8"):
            r = json.loads(l)
            self.records[r["id"]] = r

    def __call__(self, pid: str, meaning: str) -> float:
        from ft.canvas import tokenise_record
        rec = tokenise_record(self.v, {**self.records[pid], "meaning": meaning})
        prefix = 1 + sum(len(part) for part in (rec.metre_head, rec.style_head, rec.samasya_head, rec.meaning_line,
                                                self.v.poem_head) if part is not None)
        gold = sum(len(ln) for ln in rec.lines) + len(rec.lines)
        return prefix + 1.5 * gold - MDLM_CANVAS


class Checker:
    def __init__(self, sources: list[dict], n_threshold: int | None = None):
        from sentence_transformers import SentenceTransformer
        self.emb = SentenceTransformer("sentence-transformers/LaBSE", device="cpu", local_files_only=True)
        self.sources = sources
        self.src_vecs = self.emb.encode([s["meaning"] for s in sources], normalize_embeddings=True)
        sims = self.src_vecs @ self.src_vecs.T
        n = n_threshold or len(sources)                    # the threshold from the first n sources (the 183)
        self.threshold = float(np.percentile(sims[:n, :n][~np.eye(n, dtype=bool)], 99))
        self.index = {s["id"]: i for i, s in enumerate(sources)}
        self.fit = MDLMFit()

    def __call__(self, sid: str, text: str) -> dict:
        s = self.sources[self.index[sid]]
        v = self.emb.encode([text], normalize_embeddings=True)[0]
        sims = self.src_vecs @ v
        own = float(sims[self.index[sid]])
        rank = int((sims > own).sum()) + 1
        ws, src_words = words(text), set(words(s["meaning"]))
        copy = sum(w in src_words for w in ws) / max(1, len(ws))
        a, a_src, a_gold = aksharas(text), aksharas(s["meaning"]), aksharas("\n".join(s["lines"]))
        ratio = len(a) / max(1, len(a_src))
        gold_run = longest_run(a, a_gold)
        foreign = foreign_letters(text)
        over = self.fit(sid, text)
        checks = {"telugu": not foreign, "meaning": rank == 1 and own >= self.threshold, "copy": copy <= COPY_MAX,
                  "gold": gold_run < GOLD_RUN, "length": LENGTH[0] <= ratio <= LENGTH[1], "fits": over <= 0}
        return {"checks": checks, "passed": all(checks.values()), "failed": [k for k, ok in checks.items() if not ok],
                "similarity": round(own, 4), "rank": rank, "copy_share": round(copy, 3), "gold_run": gold_run,
                "source_run": longest_run(a, a_src), "length_ratio": round(ratio, 3), "foreign": foreign,
                "aksharas": len(a), "mdlm_overflow": over}


# --------------------------------------------------------------------------- main
def sources(reference: str = REFERENCE, ids: set[str] | None = None) -> list[dict]:
    path = RUNS / reference / "results.jsonl"
    pairs = sorted({(json.loads(l)["meter"], json.loads(l)["topic"]) for l in open(path, encoding="utf-8")})
    pairs = [(m, pid) for m, pid in pairs if ids is None or pid in ids]
    recs = {}
    for l in open(RECORDS, encoding="utf-8"):
        r = json.loads(l)
        recs[r["id"]] = r
    out = []
    for m, pid in pairs:
        r = recs[pid]
        out.append({"id": pid, "meter": m, "meter_te": r["meter_te"], "register": r["register"],
                    "samasya": r.get("samasya"), "meaning": r["meaning"], "lines": r["lines"]})
    return out


def review(rows: list[dict], summary: dict, path: Path) -> None:
    pick = random.Random(20261021).sample(rows, min(30, len(rows)))
    out = ["# P1 retold prompts: review sample", "",
           f"{summary['sources']} source poems; every check passed: **{summary['passed']}** "
           f"({summary['passed'] / summary['sources']:.0%}); kept with a failed check (flagged): {summary['flagged']}.",
           f"Meaning threshold (LaBSE, the 99th percentile between different sources): {summary['threshold']:.3f}.",
           "", "| check | failed (kept prompts) |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in summary["failed_by_check"].items()]
    out += ["", "Medians over the kept prompts: similarity {similarity}, copy share {copy_share}, length ratio "
            "{length_ratio}, longest run shared with the source {source_run} aksharas, with the gold poem {gold_run}."
            .format(**summary["medians"]), "",
            "30 prompts drawn with a fixed seed, then every other flagged prompt. Mark any prompt that changes the "
            "meaning, adds or drops an event, or is not natural Telugu: the automatic checks cannot see a changed "
            "meaning (a smoke run's retelling with two wrong events had LaBSE similarity 0.88). All 183: p1.jsonl.", ""]
    def entry(head: str, r: dict) -> list[str]:
        c = r["result"]
        flag = "" if c["passed"] else f" — **flagged: {', '.join(c['failed'])}**"
        return [f"## {head}. {r['meter_te']} · `{r['id']}`{flag}", "",
                f"similarity {c['similarity']} (rank {c['rank']}), copy {c['copy_share']:.0%}, length "
                f"{c['length_ratio']}×, shared run with source {c['source_run']} / gold {c['gold_run']} aksharas", "",
                "**Source bhāvam (P0):**", "", r["meaning"], "", "**Retold (P1):**", "", r["p1"], ""]
    for k, r in enumerate(pick, 1):
        out += entry(str(k), r)
    flagged = [r for r in rows if not r["result"]["passed"] and r not in pick]
    if flagged:
        out += ["# Every other flagged prompt (edit in p1_edits.jsonl, or accept with build_records.py --allow-flagged)",
                ""]
        for k, r in enumerate(flagged, 1):
            out += entry(f"F{k}", r)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="google/gemma-4-26B-A4B-it")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--limit", type=int, default=0, help="only the first N source poems (a smoke run)")
    ap.add_argument("--out", default="prompts")
    ap.add_argument("--reference", default=REFERENCE, help="the run (under ../diffusion_finetuning/runs) whose "
                    "(metre, poem id) pairs are the source poems")
    ap.add_argument("--ids", help="a JSON list of poem ids: only these of the reference's poems")
    args = ap.parse_args()
    out = HERE / args.out
    out.mkdir(parents=True, exist_ok=True)
    base = sources()
    src = sources(args.reference, set(json.loads(Path(args.ids).read_text(encoding="utf-8"))) if args.ids else None)
    known = {s["id"] for s in base}
    checker = Checker(base + [s for s in src if s["id"] not in known], len(base))   # threshold: always the 183's
    if args.limit:
        src = src[: args.limit]
    path = out / "p1.jsonl"
    done = {json.loads(l)["id"] for l in open(path, encoding="utf-8")} if path.exists() else set()
    todo = [s for s in src if s["id"] not in done]
    print(f"{len(src)} source poems, {len(todo)} to do; meaning threshold {checker.threshold:.3f}", flush=True)
    gen = Generator(args.model, args.device) if todo else None
    t0 = time.time()
    with open(path, "a", encoding="utf-8") as fh, open(out / "p1_attempts.jsonl", "a", encoding="utf-8") as fa:
        for b in range(0, len(todo), args.batch):
            group, best = todo[b: b + args.batch], {}
            for attempt, (seed, temp) in enumerate(zip(SEEDS, TEMPS)):
                pending = [s for s in group if s["id"] not in best or not best[s["id"]][1]["passed"]]
                if not pending:
                    break
                texts = gen([s["meaning"] for s in pending], seed, temp)
                for s, text in zip(pending, texts):
                    res = checker(s["id"], text)
                    fa.write(json.dumps({"id": s["id"], "attempt": attempt, "seed": seed, "temperature": temp,
                                         "p1": text, "result": res}, ensure_ascii=False) + "\n")
                    if s["id"] not in best or len(res["failed"]) < len(best[s["id"]][1]["failed"]):
                        best[s["id"]] = (text, res, attempt)
            for s in group:
                text, res, attempt = best[s["id"]]
                fh.write(json.dumps({**s, "p1": text, "attempt": attempt, "result": res}, ensure_ascii=False) + "\n")
            fh.flush()
            fa.flush()
            print(f"{min(b + args.batch, len(todo))}/{len(todo)} poems, {time.time() - t0:.0f} s; this batch: "
                  f"{sum(best[s['id']][1]['passed'] for s in group)}/{len(group)} pass", flush=True)

    rows = [json.loads(l) for l in open(path, encoding="utf-8")]
    failed = {k: sum(not r["result"]["checks"][k] for r in rows)
              for k in ("telugu", "meaning", "copy", "gold", "length", "fits")}
    med = {k: float(np.median([r["result"][k] for r in rows]))
           for k in ("similarity", "copy_share", "length_ratio", "source_run", "gold_run")}
    summary = {"model": args.model, "sources": len(rows), "passed": sum(r["result"]["passed"] for r in rows),
               "flagged": sum(not r["result"]["passed"] for r in rows), "threshold": checker.threshold,
               "failed_by_check": failed, "attempts": dict(sorted(
                   {a: sum(r["attempt"] == a for r in rows) for a in range(len(SEEDS))}.items())),
               "medians": {k: round(v, 3) for k, v in med.items()}}
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    review(rows, summary, out / "p1_review.md")
    print(json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
