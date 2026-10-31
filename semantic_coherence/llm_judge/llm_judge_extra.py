import csv
import json
import sys
import time
from pathlib import Path

from mlx_lm import load, generate
from mlx_lm.sample_utils import make_sampler

GREEDY_SAMPLER = make_sampler(temp=0.0)

HERE = Path(__file__).resolve().parent
SEMANTIC_DIR = HERE.parent  # semantic_coherence/
RESULTS_DIR = HERE / "results"
RESULTS_DIR.mkdir(exist_ok=True)

KEYS = ["classical_register", "ai_generated_guess"]


def build_prompt(poem_text, meter):
    return f"""You are an expert judge of Telugu poetry, able to tell classical literary diction from modern/colloquial diction, and able to tell AI-generated verse from human-authored verse.

You will be shown a Telugu poem written in the "{meter}" meter. Judging the text alone, answer:
- classical_register (0 or 1): Is the poem written in a classical/elevated literary register (dense Sanskritized compounds, ornate classical Telugu diction, archaic vocabulary), as opposed to a modern or colloquial register (simpler, more contemporary word choices)? 1 = classical/elevated register, 0 = modern/colloquial register.
- ai_generated_guess (0 or 1): Does this poem read as machine/AI-generated verse, as opposed to being composed by a human poet? Consider things like unnatural phrasing, generic imagery, or overly mechanical adherence to the meter as signs of AI generation; natural idiom, distinctive voice, and idiosyncrasy as signs of human authorship. 1 = AI-generated, 0 = human-authored.

POEM:
{poem_text}

Respond with ONLY a single JSON object, no explanation, no markdown code fences, exactly these keys:
{{
  "classical_register": <0 or 1>,
  "ai_generated_guess": <0 or 1>
}}"""


def parse_json_response(text):
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return None


def main():
    model_id = sys.argv[1]
    out_key = sys.argv[2]
    limit = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3] else None
    max_tokens = int(sys.argv[4]) if len(sys.argv) > 4 else 500

    rows = []
    with open(SEMANTIC_DIR / "data" / "pooled_study1.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        seen = set()
        for r in reader:
            if r["eval_id"] in seen:
                continue
            seen.add(r["eval_id"])
            rows.append(r)
    if limit:
        rows = rows[:limit]
    print(f"{len(rows)} unique poems to judge (extra: register/ai_generated) with {model_id}", flush=True)

    t0 = time.time()
    model, tokenizer = load(model_id)
    print(f"Model loaded in {time.time() - t0:.1f}s", flush=True)

    out_path = RESULTS_DIR / f"llm_judge_extra_{out_key}.csv"
    fieldnames = ["eval_id", "source_dataset", "meter"] + KEYS + ["parse_ok", "raw_response"]
    with open(out_path, "w", encoding="utf-8", newline="") as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, r in enumerate(rows):
            meter = r["meter"]
            prompt_text = build_prompt(r["poem_text"], meter)
            messages = [{"role": "user", "content": prompt_text}]
            prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

            t1 = time.time()
            response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False, sampler=GREEDY_SAMPLER)
            parsed = parse_json_response(response)
            if parsed is None and "<channel|>" in response:
                parsed = parse_json_response(response.split("<channel|>")[-1])

            out_row = {"eval_id": r["eval_id"], "source_dataset": r["source_dataset"], "meter": meter,
                       "parse_ok": parsed is not None, "raw_response": response.replace("\n", " ")[:2000]}
            for k in KEYS:
                out_row[k] = (parsed or {}).get(k)
            writer.writerow(out_row)
            outf.flush()

            if (i + 1) % 10 == 0 or i == len(rows) - 1:
                print(f"  [{i+1}/{len(rows)}] eval_id={r['eval_id']} parse_ok={parsed is not None} "
                      f"({time.time()-t1:.1f}s/poem)", flush=True)

    print(f"DONE {model_id} -> {out_path} ({time.time()-t0:.1f}s total)", flush=True)


if __name__ == "__main__":
    main()
