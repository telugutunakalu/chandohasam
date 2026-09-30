# EXP-23: activation steering with controls — summary

Full specification: [`../EXP-23-activation-steering-with-controls.md`](../EXP-23-activation-steering-with-controls.md).
**Status:** blocked (2026-09-29). Not run.

## Question
Does adding a chandas direction to the hidden states during generation improve metrical compliance
without damaging meaning?

## Planned design
- Inject `h ← h + α·d` at every generated token, sweeping α and the layer.
- Use a metre-vs-metre direction as the primary arm and the coarse poem − bhavam direction as the
  secondary one.
- A random direction of matched norm serves as the control.
- Measure compliance (the validator) and meaning (a round-trip paraphrase compared with the bhavam)
  together.

## Why it is blocked
- **No direction qualifies.** With `<bos>`, all 28 metre pairs in EXP-22 fall below the coherence
  threshold of 0.322 (max 0.158). The kandamu/mattakokila pair gives 0.03–0.07, not the 0.5–0.65 the
  design relied on.
- **No fallback.** EXP-38's tight contrast gives no metre-specific direction either (coherence ≤ 0.011).
- **Only the secondary arm remains.** The coarse direction is register-dominated: EXP-07 separates verse
  from prose from L1 on.

## Unblock when
A direction passes the coherence check. One route is a model that complies with the metre (the EXP-26
realiser, or a fine-tuned checkpoint); EXP-22 and EXP-38 would then be rerun on it.

## Evidence
No results. The blocking evidence is in [`../exp22/summary.md`](../exp22/summary.md) and
[`../exp38/summary.md`](../exp38/summary.md).
