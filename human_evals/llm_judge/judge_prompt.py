#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The LLM-as-judge prompt: the human-evaluation rubric, put to a model the way the annotation app puts it to a person.

    python3 judge_prompt.py he2_0005                       # print one poem's prompt (study 2's data)
    python3 judge_prompt.py he_0001 --data ../annotation_app/data
    python3 judge_prompt.py --all --out prompts_study2.jsonl   # every poem, one JSON line each, for a batch run
    python3 judge_prompt.py he2_0005 --check reply1.json reply2.json   # validate a judge's two replies

What the judge gets, matched to the annotator's screen (annotation_app/padya_eval/templates/poem.html):
- **The rubric, word for word.** Questions, Telugu text, scale anchors and guides are read from
  ../annotation_app/padya_eval/rubric.py (RUBRIC_VERSION), so the prompt cannot drift from the form.
- **Two turns, as the form does it.** Turn 1: the poem with its metre, and questions 1–3 only. Turn 2: the bhāvam is
  revealed, and questions 4–12; the turn-1 answers stand (the guide: "Answer 1–3 before revealing it").
- **The same aids.** The metre's card and the rules (the app's Rules dialog: guru/laghu, gaṇas, yati maitri,
  prāsa), and the engine's reading of the poem (gaṇa division, guru/laghu of every akshara, yati and prāsa aksharas),
  which the annotator sees as the gaṇa table and underlines. The engine's verdicts (the ✔ and rule names) are left
  out, as in study 2 (HE_SHOW_ENGINE_CHECKS=0); --show-checks adds them, as study 1 showed them.
- **Not applicable** questions as in the app: prāsa when the metre has none, bhāvam when the poem has none.
- **Added for a model only:** a one-sentence reason before each answer (--no-reasons drops it), and a JSON reply.

Nothing hidden is shown: no poem id, source, author or model.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = HERE.parent / "annotation_app"
_spec = importlib.util.spec_from_file_location("rubric", APP / "padya_eval" / "rubric.py")
rubric = sys.modules["rubric"] = importlib.util.module_from_spec(_spec)     # dataclasses look the module up
_spec.loader.exec_module(rubric)                     # rubric.py alone: no Flask needed

TURN1 = ("readability", "comprehension", "lexical")
TURN2 = tuple(q.key for q in rubric.QUESTIONS if q.key not in TURN1)

SYSTEM = """\
You are an expert reader of Telugu poetry, trained in chandassu (prosody) and alaṅkāraśāstra, taking part in a \
research study as one of its annotators. You rate one padyam at a time on the study's rubric, exactly as its human \
annotators do.

The study's instructions (the same as the annotators'):
- Rate the poem as it is printed. Read and answer 1–3 before opening the bhavam. Use the whole scale.
- The gaṇa division and the yati/prāsa marks are an automatic reading to help you check; your judgement decides 5–7.

How this works: in the first message you get the poem and questions 1–3. In the second you get the bhāvam (the \
meaning the poem was written for) and questions 4–12; your answers to 1–3 stand. Judge the poem itself: do not guess \
who wrote it, and do not correct it in your head.

Reply with one JSON object and nothing else.{reasons}"""

REASONS = (" For every question write one short reason (one sentence at most) in \"reasons\" before its answer in "
           "\"answers\".")


def question_block(q, poem) -> str:
    head = f"Q{q.number}. {q.text} ({q.text_te})"
    if not rubric.applicable(q, poem):
        return f"{head}\n    Not applicable: {q.na_reason} Answer null."
    if q.kind == "likert":
        scale = f"Answer 1–5: 1 = {q.low} … 5 = {q.high}."
    else:
        scale = f"Answer 0 or 1: 0 = {q.label(0)}, 1 = {q.label(1)}."
    return f"{head}\n    {scale}\n    Guide: {q.guide}"


def schema(keys, reasons: bool) -> str:
    ans = ", ".join(f'"{k}": <answer>' for k in keys)
    if not reasons:
        return f'{{"answers": {{{ans}}}}}'
    why = ", ".join(f'"{k}": "<one sentence>"' for k in keys)
    return f'{{"reasons": {{{why}}}, "answers": {{{ans}}}}}'


class PoemView:
    """What the annotation form knows about a poem (a poems.json entry), as rubric.applicable expects."""

    def __init__(self, raw: dict):
        self.raw = raw

    @property
    def has_bhavam(self) -> bool:
        b = self.raw.get("bhavam") or {}
        return bool(b.get("te") or b.get("en"))

    @property
    def prasa_applicable(self) -> bool:
        return bool(self.raw.get("prasa_applicable"))

    @property
    def plain_lines(self) -> list[str]:
        return ["".join(t["t"] for t in line) for line in self.raw["lines"]]


# the Rules dialog's own wording (annotation_app/padya_eval/templates/_reference_body.html)
GANA_TABLES = {"ekakshara_ganas": "ఏకాక్షర గణాలు", "dvyakshara_ganas": "ద్వ్యక్షర గణాలు",
               "trika_ganas": "త్ర్యక్షర (వృత్త) గణాలు", "surya_ganas": "సూర్య గణాలు", "indra_ganas": "ఇంద్ర గణాలు",
               "chandra_ganas": "చంద్ర గణాలు", "kanda_ganas": "కంద గణాలు"}
GURU_NOTES = ("అర్ధానుస్వారం (ఁ) బరువు పెంచదు · the arasunna ఁ adds no weight.",
              "పాదాంత లఘువును ఛందస్సు కోరితే గురువుగా చదవవచ్చు · a pāda-final laghu may be read as guru where the "
              "meter needs it.",
              "వికల్పం: తరువాతి పదం సంయుక్తాక్షరంతో మొదలైతే ముందటి లఘువు గురువు కావచ్చు; ర-వత్తు సంయుక్తానికి ముందటి అక్షరం "
              "లఘువుగా ఉండవచ్చు · vikalpa: a laghu before a word-initial conjunct may be guru; a syllable before a "
              "ర-vattu conjunct may stay laghu.")
YATI_INTRO = ("ప్రతి పాదంలో మొదటి అక్షరం (వళి) యతిస్థానంలోని అక్షరంతో మైత్రి కలిగి ఉండాలి. హల్లులు మైత్రి కలిగి ఉండాలి, "
              "అచ్చులు కూడా ఒకే వర్గంలో ఉండాలి. ఁ, ం, ః, పొల్లు మైత్రిని మార్చవు. యతిస్థానం ఛందస్సును బట్టి.")
PRASA_INTRO = ("ప్రతి పాదంలో 2వ అక్షరంలోని హల్లు(లు) అన్ని పాదాల్లో ఒకటే కావాలి; అచ్చు మారవచ్చు. ప్రాసకు ముందటి (1వ) "
               "అక్షరం అన్ని పాదాల్లో గురువు లేదా అన్నిటిలో లఘువు కావాలి.")
PRASA_GROUPS = (("ప్రామాణిక నియమాలు · canonical and mandatory", ("canonical", "canonical_subtype", "mandatory")),
                ("ప్రాసమైత్రి / సడలింపులు · relaxations", ("accepted_relaxation", "orthographic_relaxation",
                                                           "deprecated")),
                ("నిషిద్ధం · never a prāsa", ("forbidden",)))


def meter_card(ref: dict, c: dict) -> str:
    """The Rules dialog's card of one metre."""
    ak = c["aksharalu"]
    head = f"{c['name_te']} ({c['name']} · {c['family_te']} · {c['padalu']} పాదాలు"
    if ak[0]:
        head += f" · {ak[0] if ak[0] == ak[1] else f'{ak[0]}–{ak[1]}'} అక్షరాలు/పాదం"
    rows = [head + ")"]
    for row in c["slots"]:
        lead = f"పాదాలు {', '.join(map(str, row['lines']))}: " if len(c["slots"]) > 1 else ""
        alt = "ప్రత్యామ్నాయం · " if row.get("alt") else ""
        rows.append(f"గణాలు: {alt}{lead}" + " ".join(
            g["t"] + (f" {g['pat']}" if g.get("pat") else "") + (f" ({ref['class_names'].get(g['cls'], g['cls'])})"
                                                               if g.get("cls") else "") for g in row["ganas"]))
    if c.get("ganalu_text"):
        rows.append(f"  {c['ganalu_text']}")
    rows.append("యతి: " + ("; ".join(c["yati"]) if c["yati"] else "—")
                + (" (ప్రాసయతి కూడా చెల్లుతుంది · prāsa-yati is allowed)" if c.get("prasa_yati") else ""))
    rows.append("ప్రాస: " + ("ఉంది — ప్రతి పాదంలో 2వ అక్షరం · every pāda's 2nd akshara" if c["prasa"]
                            else "లేదు · not required"))
    rows += [f"నియమం: {x}" for x in dict.fromkeys(c.get("constraints") or [])]
    if c.get("followed_by"):
        rows.append("తరువాత: " + " / ".join(ref["meters"][f]["name_te"] if f in ref["meters"] else f
                                             for f in c["followed_by"]) + " (గీతి)")
    if c.get("halves_per_line", 1) > 1:
        rows.append(f"ముద్రణ: each pāda printed as {c['halves_per_line']} lines")
    if c.get("notes"):
        rows.append(f"గమనిక: {c['notes']}")
    return "\n  ".join(rows)


def rules_text(ref: dict, poem: dict) -> str:
    """The Rules dialog as text: this poem's metre, guru/laghu, gaṇas, yati, prāsa."""
    st = ref["status_te"]
    out = ["ఈ పద్యం ఛందస్సు · this poem's meter:"] + ["  " + meter_card(ref, ref["meters"][m]) for m in poem["meters"]]
    out += ["", "గురు లఘు నియమాలు · guru / laghu: any of these makes an akshara guru (U); otherwise laghu (I)."]
    out += [f"  {r['te']}: {r['when']}" for r in ref["guru_rules"]] + [f"  - {n}" for n in GURU_NOTES]
    out += ["", "గణాలు · gaṇas:"] + [f"  {GANA_TABLES.get(t['key'], t['key'])}: "
                                       + ", ".join(f"{g['telugu']} {g['pattern']}" for g in t["ganas"])
                                       for t in ref["gana_tables"]]
    y = ref["yati"]
    out += ["", f"యతి · yati (వళి): {YATI_INTRO}",
            "  స్వరమైత్రి · vowel classes: " + "; ".join(" ".join(v) for v in y["vowel_classes"].values())]
    maitri: dict[tuple, list[str]] = {}                  # rows of the same rule merged (ము విభక్తి యతి: 4 rows)
    for m in y["maitri"]:
        pairs = [" ".join(v) for v in m.get("vargas") or []] or [" – ".join(p) for p in m.get("pairs") or []]
        maitri.setdefault((m["te"].strip(), m.get("en", ""), m["status"]), []).extend(pairs)
    out += [f"  {te} ({en}): {', '.join(pairs)} [{st.get(s, s)}]" for (te, en, s), pairs in maitri.items()]
    out += ["", f"ప్రాస · prāsa: {PRASA_INTRO}"]
    for name, keep in PRASA_GROUPS:
        rules = [r for r in ref["prasa"]["rules"] if r["status"] in keep]
        out.append(f"  {name}: " + "; ".join(f"{r['te']} ({r['en']}) [{st.get(r['status'], r['status'])}]"
                                             for r in rules))
    return "\n".join(out)


def reading_text(ref: dict, poem: dict, show_checks: bool) -> str:
    """The gaṇa table and the yati/prāsa marks, as text."""
    rows = []
    for unit in poem["units"]:
        for pada in unit["padas"]:
            ganas = " | ".join(
                f"{ref['class_names'].get(g['cls'], g['n']) if g.get('cls') else g['n']} {g['pat']}: "
                + " ".join(f"{a['t']}({a['w']})" for a in g["ak"]) for g in pada["ganas"])
            rows.append(f"pāda {pada['no']}: {ganas}")
    for i, n in enumerate(poem["notes"], 1):
        bits = []
        if n.get("prasa"):
            bits.append(f"prāsa akshara {n['prasa']}")
        for y in n.get("yati") or []:
            seat = f"yati {y['ak'][0]} ↔ {y['ak'][1]} (aksharas {y['pos'][0]} and {y['pos'][1]})"
            if show_checks and y.get("te"):
                seat += f" — engine: {y['te']}{'' if y.get('ok') else ' (not matched)'}"
            bits.append(seat)
        if n.get("no_yati"):
            bits.append("no yati in this line")
        if bits:
            rows.append(f"line {i}: " + "; ".join(bits))
    if show_checks:
        for ps in poem.get("prasa_summary") or []:
            if ps.get("label"):
                rows.append(f"prāsa — engine: {ps['label']}")
    return "\n".join(rows)


def build(poem: dict, ref: dict, reasons: bool = True, show_checks: bool = False) -> dict:
    """The judge's conversation for one poem: system, turn 1 (Q1–3), turn 2 (bhāvam, Q4–12)."""
    view = PoemView(poem)
    qs = {q.key: q for q in rubric.QUESTIONS}
    text = "\n".join(view.plain_lines)
    turn1 = (f"Metre (ఛందస్సు): {poem['meter_te']}\n\nThe poem:\n{text}\n\n"
             f"The automatic reading (gaṇa division; U = guru, I = laghu):\n{reading_text(ref, poem, show_checks)}\n\n"
             f"The rules (as in the study's Rules page):\n{rules_text(ref, poem)}\n\n"
             f"Answer questions 1–3 now. The bhāvam comes in the next message.\n\n"
             + "\n\n".join(question_block(qs[k], view) for k in TURN1)
             + f"\n\nReply with JSON only: {schema(TURN1, reasons)}")
    b = poem.get("bhavam") or {}
    bh = "\n".join(x for x in (b.get("te"), b.get("en")) if x) if view.has_bhavam else "(no bhāvam for this poem)"
    turn2 = (f"The bhāvam (భావం):\n{bh}\n\nYour answers to 1–3 stand. Now answer questions 4–12 about the same "
             f"poem.\n\n" + "\n\n".join(question_block(qs[k], view) for k in TURN2)
             + f"\n\nReply with JSON only: {schema(TURN2, reasons)}")
    return {"system": SYSTEM.format(reasons=REASONS if reasons else ""), "turn1": turn1, "turn2": turn2,
            "rubric_version": rubric.RUBRIC_VERSION}


def check(reply: dict, poem: dict, keys) -> list[str]:
    """Problems with one parsed reply (an empty list when it is valid)."""
    view, errors = PoemView(poem), []
    ans = reply.get("answers")
    if not isinstance(ans, dict):
        return ['no "answers" object']
    for k in keys:
        q = rubric.BY_KEY[k]
        v = ans.get(k, "missing")
        if not rubric.applicable(q, view):
            if v is not None:
                errors.append(f"{k}: not applicable, must be null (got {v!r})")
        elif v not in q.choices:
            errors.append(f"{k}: {v!r} is not one of {q.choices}")
    extra = set(ans) - set(keys)
    if extra:
        errors.append(f"unexpected keys {sorted(extra)}")
    return errors


def load(data: Path) -> tuple[dict, dict]:
    poems = {p["id"]: p for p in json.loads((data / "poems.json").read_text(encoding="utf-8"))["poems"]}
    return poems, json.loads((data / "reference.json").read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("eval_id", nargs="?")
    ap.add_argument("--data", type=Path, default=APP / "data_study2", help="the app's data dir (study 1: ../annotation_app/data)")
    ap.add_argument("--all", action="store_true", help="every poem of the data dir")
    ap.add_argument("--out", type=Path, help="with --all: write JSONL here")
    ap.add_argument("--no-reasons", action="store_true", help="answers only, no one-sentence reasons")
    ap.add_argument("--show-checks", action="store_true", help="include the engine's verdicts, as study 1 showed them")
    ap.add_argument("--check", nargs=2, type=Path, metavar=("REPLY1", "REPLY2"), help="validate the two JSON replies")
    a = ap.parse_args()
    poems, ref = load(a.data)
    kw = {"reasons": not a.no_reasons, "show_checks": a.show_checks}
    if a.check:
        p = poems[a.eval_id]
        errs = [f"turn 1: {e}" for e in check(json.loads(a.check[0].read_text(encoding="utf-8")), p, TURN1)]
        errs += [f"turn 2: {e}" for e in check(json.loads(a.check[1].read_text(encoding="utf-8")), p, TURN2)]
        print("\n".join(errs) or "valid")
        return 1 if errs else 0
    if a.all:
        rows = [{"eval_id": e, **build(p, ref, **kw)} for e, p in poems.items()]
        out = open(a.out, "w", encoding="utf-8") if a.out else sys.stdout
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
        if a.out:
            out.close()
            print(f"wrote {len(rows)} prompts to {a.out}")
        return 0
    if not a.eval_id:
        ap.error("give an eval id, or --all")
    m = build(poems[a.eval_id], ref, **kw)
    print(f"=== SYSTEM ===\n{m['system']}\n\n=== TURN 1 (user) ===\n{m['turn1']}\n\n=== TURN 2 (user) ===\n{m['turn2']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
