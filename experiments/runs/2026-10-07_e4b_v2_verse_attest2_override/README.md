# Layer B, first scoring — failed (kept for the record)

E4B, 111 poems (37 meters × 3 strategies, T1, seed 42), verse inventory + Layer B (attestation preference,
weight 2, only where the model's first choice was not allowed), with the FIRST scoring rule: every finished
corpus word scored 2 and every word begun scored again. Single aksharas are words of the corpus (త, గ …), so
ending a word after almost every akshara paid best: single-akshara words rose from 3–6% to 37–46%, real words
of two aksharas or more fell (23–25% → 21–22.5%), 6–9 of 37 poems per strategy were filler (త మ్మ త్త గ …).
The scoring was fixed (only words of 2+ aksharas count; a token that ends a word is judged by that word alone)
and rerun as `2026-10-07_e4b_v2_verse_attestB_*`. The every-step arm of this version was stopped at its start.
