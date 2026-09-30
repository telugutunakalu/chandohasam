# Inference ablations — every poem, as JSON

All poems generated in the inference ablations, four files per model: the free baseline and the
three constrained strategies (masking only, masking + backtracking, hybrid), 37 meters × 3 topics ×
5 seeds each — **2,220 poems per model** — with every field the runs recorded.

Each model is split at the same meters into four parts, so that every file stays under 50 MB and a
given meter is in the same part for every model (all its ablations together). Each part is a complete
JSON document with the same header.

| part | meters | poems | Gemma-4 E4B | Gemma-4 26B-A4B | DiffusionGemma 26B-A4B |
|---|---|---|---|---|---|
| 1 | 1–8: ఉత్పలమాల … భుజంగప్రయాతము | 480 | `gemma-4-E4B-it.part1.json` | `gemma-4-26B-A4B-it.part1.json` | `diffusiongemma-26B-A4B-it.part1.json` |
| 2 | 9–19: మత్తకోకిలము … కందము | 660 | `gemma-4-E4B-it.part2.json` | `gemma-4-26B-A4B-it.part2.json` | `diffusiongemma-26B-A4B-it.part2.json` |
| 3 | 20–30: ఉత్సాహము … తరళము | 660 | `gemma-4-E4B-it.part3.json` | `gemma-4-26B-A4B-it.part3.json` | `diffusiongemma-26B-A4B-it.part3.json` |
| 4 | 31–37: మాలిని … లయవిభాతి | 420 | `gemma-4-E4B-it.part4.json` | `gemma-4-26B-A4B-it.part4.json` | `diffusiongemma-26B-A4B-it.part4.json` |

The files are 38–45 MB each.

## Structure

```text
{
  "format", "created",
  "model":      id, label, precision, decoding, sampling, prefill, prompt
  "experiment": ablations, meters, topics, seeds, constraint, poem counts, poems in meter per ablation
  "runs":       the exact configuration of each source run (run.json)
  "fields":     a description of every field below
  "meters":     per meter: Telugu name, class, the rules given in the prompt, token budget
  "prompts":    per prompt hash: meter, topic, messages, prefill, prompt token ids
  "part":       index, of, meters, poems
  "poems": [    one poem per line
    {
      "id", "run", "meter", "meter_name", "meter_class", "topic", "topic_text", "ablation", "seed",
      "prompt_sha", "prompt": {system, user, prefill},
      "status",
      "poem":       {text, lines, gana_patterns},
      "evaluation": the engines' verdicts (gana_strict, prasa_strict, yati_strict, relaxed variants, …),
      "generation": model settings, token ids, n_tokens, seconds, backtracks, masks, passes, …,
      "tokens":     the poem's tokens in order: {text, prob, overridden},
      "trace":      the full decoding log: every chosen token with logp, prob, rank, p_pick, the allowed
                    set's size and mass, entropy, temperature, the model's top 5 (with prob and whether
                    each was allowed), line / akshara position, whether it stayed in the poem; and every
                    backtrack with its reason
    }, …
  ]
}
```

`prob` is the model's probability of the token over its whole vocabulary at temperature 1, recorded
when the token was chosen; `overridden` is true when the model's own first choice was not allowed by
the meter. The field names are those of the run files, so the repository's analysis code applies.

## Loading

```python
import json

poems = []
for part in (1, 2, 3, 4):
    with open(f"gemma-4-E4B-it.part{part}.json", encoding="utf-8") as f:
        poems += json.load(f)["poems"]

hybrid_kandam = [p for p in poems if p["meter"] == "kandamu" and p["ablation"] == "hybrid"]
print(hybrid_kandam[0]["poem"]["text"])
print([(t["text"], t["prob"]) for t in hybrid_kandam[0]["tokens"]][:10])
```

Generated on 2026-09-26 by `experiments/scripts/export_inference_json.py` from the final run
directories (rows superseded by reruns are not included).
