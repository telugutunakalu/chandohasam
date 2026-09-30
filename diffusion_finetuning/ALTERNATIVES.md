# Alternative: train Stage 2 on T1 and T2 only

This is an option we discussed on 2026-09-29 and did **not** adopt. The plan
([PLAN.md](PLAN.md)) keeps the six-task mix. This file records the reasoning, so
the alternative can be run later as a single comparison: one Stage 2 run,
about 3–4 hours on the laptop.

## The idea

Drop T0, T3, T4 and T5, and spend all of Stage 2 on:

- **T1**: metre + meaning → poem;
- **T2**: poem → meaning.

## What it would keep

- **More signal for the main task.** T1 gets more training for the same compute,
  so meaning → poem likely improves slightly per unit of compute.
- **The explainer and the reranker.** Both come from T2. Training both
  directions tends to help each, because the model links poem and meaning both
  ways.
- **The metre.** It does not depend on the task mix. It is guaranteed at
  decoding time by the engine constraints (§6), and the model's own sense of
  metre comes from Stage 1 and T1.

## What it would lose, and how to get it back

**T0: classifier-free guidance.**
- Guidance needs the same model to predict without the meaning. T0 is where it
  learns that.
- Substitute: use the **Stage 1 checkpoint** as the "no meaning" model. It can
  write poems from a metre header alone.
- Cost: guidance needs a second forward pass anyway. The substitute adds only a
  second 120M model in memory.

**T5: infill and repair.**
- T1 already does scattered infill, because its target is masked at a random
  rate. At a low rate the model sees most of the poem and fills a few gaps.
- Random masking rarely makes **contiguous** gaps: a word, a line, or everything
  after position k.
- That last pattern is exactly what the left-to-right, line-by-line decoding in
  §6 produces. T5's span masks are where the model practises it.
- Substitute: if T5 is dropped, T1's masking should sometimes mask a random span
  or the whole suffix, so training still matches decoding.

**T3 / T4: glosses.** The smallest loss.
- 380k meaning → poem pairs already teach the modern → archaic word mapping
  implicitly.
- Stage 1's poem + meaning documents reinforce it.
- The glosses still feed the decoding lexicon (§6.3), which needs no training.
- They would mostly matter for rare words.

## Assessment

Stage 1 now trains on poem + meaning documents, so much of what T0, T3, T4 and T5
add is already partly covered. A T1 + T2 model could plausibly match the full
mix, provided that:

- T1 carries span and suffix masks;
- the Stage 1 checkpoint serves as the guidance model.

What it would certainly give up is a built-in repair tool and some rare-word
vocabulary.

## How to test it

Run one extra Stage 2 configuration and compare it with the chosen mix on val,
using the §8 metrics:

- **Tasks:** T1 70% and T2 30%.
- **T1 masking:** in 30% of T1 examples, mask a contiguous span or a whole suffix
  of the poem instead of scattered tokens.
- **Guidance:** from the Stage 1 checkpoint.
