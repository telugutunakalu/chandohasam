import csv
import json
import re
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

LIKERT_KEYS = ["readability", "comprehension", "lexical", "poetic", "bhavam"]
BINARY_KEYS = ["chandassu", "prasa", "yati", "shabdalankara", "arthalankara"]
ALL_KEYS = ["readability", "comprehension", "lexical", "bhavam", "chandassu", "prasa", "yati", "shabdalankara", "arthalankara", "poetic"]

APPLIES_PRASA = {
    "bhujangaprayatamu", "champakamala", "dvipada", "hayapracara_ragada", "indravajra",
    "kandamu", "kavirajavirajitamu", "lalita", "layagrahi", "layavibhati",
    "madhuragati_ragada", "madhyakkara", "mahasragdhara", "malini", "mangalamahasri",
    "manini", "mattakokilamu", "mattebhavikriditamu", "pamcacamaramu", "rathoddhata",
    "salini", "sardulavikriditamu", "sragdhara", "sragvini", "taralamu", "taruvoja",
    "totakamu", "upendravajra", "utpalamala", "utsahamu", "vanamayuramu", "vasamtatilakamu",
}


def build_prompt(poem_text, bhavam_text, meter, prasa_applies):
    prasa_line = (
        '  "prasa": <0 or 1>,\n'
        if prasa_applies
        else '  "prasa": null,\n'
    )
    prasa_note = (
        "- prasa: the second akshara of every pada (line) must rhyme by the prasa rule for this meter. "
        "Score 1 if satisfied, 0 if not."
        if prasa_applies
        else "This meter has no prasa rule, so prasa is always null — do not score it."
    )
    return f"""You are an expert judge of classical Telugu metrical poetry (padyam), fluent in Telugu, familiar with chandassu (meter), prasa/yati rules, and alankaras (rhetorical figures).

You will be shown a Telugu poem written in the "{meter}" meter. First, judging the poem TEXT ALONE (do not look ahead at the bhavam below), answer these four questions on a 1-5 scale:
- readability (1=Very difficult to read, 5=Very easy to read): fluency of reading the poem aloud or silently.
- comprehension (1=Not understood, 5=Understood at once): your own first-pass understanding of the poem's meaning from the text alone, before considering any stated meaning.
- lexical (1=Most words unclear, 5=Every word clear): word level only — can you split the sandhi and recognize each word as real Telugu/Sanskrit?
- poetic (1=Prose in metre, 5=Highly poetic): overall poetic quality — imagery, diction, rasa, craft, beyond correctness.

Then also judge, from the text alone, these five binary (0/1) structural and rhetorical properties:
- chandassu: are the ganas, guru/laghu pattern, and number of padas correct for the named meter named above? 1 if correct, 0 if not.
{prasa_note}
- yati: the first akshara of each pada and its yati-sthana akshara must be yati-maitri (matching per yati rules). 1 if correct, 0 if not.
- shabdalankara: can you identify any sound figures (anuprasa, vrttyanuprasa, yamaka, etc.)? 1 if yes, 0 if no.
- arthalankara: can you identify any figures of meaning (upama, rupaka, utpreksha, slesha, etc.)? 1 if yes, 0 if no.

Finally, you are shown the poem's intended meaning (bhavam) below. Judge:
- bhavam (1=Unrelated, 5=Conveys it fully): how faithfully the poem expresses that stated meaning.

POEM:
{poem_text}

BHAVAM (intended meaning):
{bhavam_text}

Respond with ONLY a single JSON object, no explanation, no markdown code fences, exactly these keys:
{{
  "readability": <1-5>,
  "comprehension": <1-5>,
  "lexical": <1-5>,
  "bhavam": <1-5>,
  "chandassu": <0 or 1>,
{prasa_line}  "yati": <0 or 1>,
  "shabdalankara": <0 or 1>,
  "arthalankara": <0 or 1>,
  "poetic": <1-5>
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
    print(f"{len(rows)} unique poems to judge with {model_id}", flush=True)

    t0 = time.time()
    model, tokenizer = load(model_id)
    print(f"Model loaded in {time.time() - t0:.1f}s", flush=True)

    out_path = RESULTS_DIR / f"llm_judge_{out_key}.csv"
    fieldnames = ["eval_id", "source_dataset", "meter"] + ALL_KEYS + ["parse_ok", "raw_response"]
    with open(out_path, "w", encoding="utf-8", newline="") as outf:
        writer = csv.DictWriter(outf, fieldnames=fieldnames)
        writer.writeheader()

        for i, r in enumerate(rows):
            meter = r["meter"]
            prasa_applies = meter in APPLIES_PRASA
            prompt_text = build_prompt(r["poem_text"], r["bhavam_text"], meter, prasa_applies)
            messages = [{"role": "user", "content": prompt_text}]
            prompt = tokenizer.apply_chat_template(messages, add_generation_prompt=True)

            t1 = time.time()
            response = generate(model, tokenizer, prompt=prompt, max_tokens=max_tokens, verbose=False, sampler=GREEDY_SAMPLER)
            parsed = parse_json_response(response)
            if parsed is None and "<channel|>" in response:
                tail = response.split("<channel|>")[-1]
                parsed = parse_json_response(tail)

            out_row = {"eval_id": r["eval_id"], "source_dataset": r["source_dataset"], "meter": meter,
                       "parse_ok": parsed is not None, "raw_response": response.replace("\n", " ")[:2000]}
            for k in ALL_KEYS:
                out_row[k] = (parsed or {}).get(k)
            writer.writerow(out_row)
            outf.flush()

            if (i + 1) % 10 == 0 or i == len(rows) - 1:
                print(f"  [{i+1}/{len(rows)}] eval_id={r['eval_id']} parse_ok={parsed is not None} "
                      f"({time.time()-t1:.1f}s/poem)", flush=True)

    print(f"DONE {model_id} -> {out_path} ({time.time()-t0:.1f}s total)", flush=True)


if __name__ == "__main__":
    main()
