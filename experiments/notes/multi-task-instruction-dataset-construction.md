# Multi-task instruction dataset construction (formerly EXP-34)

| | |
|---|---|
| **Category** | J. Data |
| **Origin** | ours (E20) |
| **Depends on** | EXP-25,32 |
| **Status** | built, not yet trained |
| **Cost** | 41 s |

## Question
Can one corpus supply several inverse tasks that reinforce each other?

## Why it matters
Instruction tuning a diffusion model needs no new objective — protect the instruction from corruption, corrupt the response. Seeing the same poem as something to compose, explain, scan and repair forces a representation supporting all four rather than one memorised mapping.

## Methodology
1. Partition each sequence into an instruction (never corrupted) and a response (corrupted at rate t); compute loss only on the response.
2. Derive several tasks from the same records, including **inverse pairs** (compose ↔ explain).
3. Mark tasks explicitly so the model conditions from the first token.
4. Synthesise a repair task by **swapping** syllables rather than deleting — this preserves length, forcing the model to fix weight rather than restore a count.
5. Cap per task to control the mixture.

## Inputs
Corpus with meanings, glosses and metre labels; the EXP-25 tokenizer.

## Metrics
Examples per task; instruction and response length distributions.

## Expected result / baseline
Auxiliary tasks will outnumber the target task, since the target needs the most annotation.

## Observed
**491,100 examples across seven tasks**, built in 41 s: gloss 180,000 · split 120,000 · explain 60,000 · meter 60,000 · **compose 23,700** · fill 23,700 · repair 23,700.

`compose` — the target task — is the thinnest slice, needing both a prose meaning and a supported metre. That is the 37.8% annotation coverage gap appearing where it hurts most.

## Replication notes
Needs no change to a masked-diffusion trainer that already supports a protected prompt. Watch the target-task share; transfer from auxiliary tasks is the assumption being made.

## Artifacts
`padyam/data/instruct.py`, `data/instruct.npz`
