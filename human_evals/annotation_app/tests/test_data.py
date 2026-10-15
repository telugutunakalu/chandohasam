# -*- coding: utf-8 -*-
"""The precomputed data: complete, lossless, consistent with the engine and with the pool file."""
import json
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pytest

from conftest import APP_DIR, DATA_DIR

sys.path.insert(0, str(APP_DIR))
import build_data  # noqa: E402

POOL = json.loads((APP_DIR.parent / "human_eval_poems_strict.json").read_text(encoding="utf-8"))


def telugu_letters(s: str) -> str:
    return unicodedata.normalize("NFD", "".join(ch for ch in s if build_data.is_telugu(ch)))


def test_every_pool_poem_is_present_once(store):
    assert store.meta["pool"] == "strict"
    assert len(store) == len(POOL["poems"]) == 500
    assert store.ids == [p["eval_id"] for p in POOL["poems"]]


def test_display_tokens_rejoin_to_the_printed_lines(store):
    pool = {p["eval_id"]: p for p in POOL["poems"]}
    for poem in store.poems:
        assert poem.plain_lines == pool[poem.id]["lines"], poem.id


def test_aksharas_cover_the_text_in_order(store):
    for poem in store.poems:
        aks = "".join(a["t"] for u in poem.units for p in u["padas"] for g in p["ganas"] for a in g["ak"])
        assert telugu_letters(aks) == telugu_letters("".join(poem.plain_lines)), poem.id


def test_gana_patterns_and_readings_agree(store):
    for poem in store.poems:
        for u in poem.units:
            for p in u["padas"]:
                n = sum(len(g["ak"]) for g in p["ganas"])
                assert [a["i"] for g in p["ganas"] for a in g["ak"]] == list(range(1, n + 1)), poem.id
                for g in p["ganas"]:
                    assert g["pat"] == "".join(a["w"] for a in g["ak"])
                    for a in g["ak"]:
                        assert a["w"] in "UI" and a["cw"] in "UI"
                        assert bool(a["alt"]) == (a["w"] != a["cw"]), (poem.id, a)
                        if a["alt"] == "padanta":
                            assert a["i"] == n and a["cw"] == "I" and a["w"] == "U"


def test_yati_and_prasa_marks(store):
    for poem in store.poems:
        for u in poem.units:
            for p in u["padas"]:
                n = sum(len(g["ak"]) for g in p["ganas"])
                marks = {a["i"]: a["m"] for g in p["ganas"] for a in g["ak"]}
                for seat in p["yati"]:
                    group = seat["pos"]
                    assert all(1 <= i <= n for i in group) and group == sorted(group) and len(group) >= 2
                    assert all("y" in marks[i] for i in group)
                    assert len(seat["ak"]) == len(group) and seat["rule"].startswith("YATI-") and seat["te"]
                if u["prasa_applicable"]:
                    assert p["prasa"] == 2 and "p" in marks[2], poem.id
                else:
                    assert p["prasa"] is None
                    assert not any("p" in m for m in marks.values())
        line_marks = Counter(c for line in poem.lines for t in line for c in t.get("c", ""))
        grid_marks = Counter(c for u in poem.units for p in u["padas"] for g in p["ganas"] for a in g["ak"] for c in a["m"])
        assert line_marks == grid_marks, poem.id


def test_every_pada_passes_in_the_strict_pool(store):
    assert all(p["ok"] for poem in store.poems for u in poem.units for p in u["padas"])


def test_meters_and_reference_cards(store):
    ref = store.reference
    for poem in store.poems:
        assert poem.units[0]["meter"] == poem.hidden["meter_id"]
        assert all(m in ref["meters"] for m in poem.meters)
        assert store.meter_cards(poem)
    assert {r["id"] for r in ref["guru_rules"]} == {"deergha", "sandhyakshara", "anusvara", "visarga", "pollu", "samyukta"}
    assert ref["meters"]["sardulavikriditamu"]["yati"] == ["1వ అక్షరం ↔ 13వ అక్షరం"]
    assert ref["meters"]["kandamu"]["prasa"] is True and ref["meters"]["seesamu"]["prasa"] is False
    assert len(ref["prasa"]["rules"]) > 50 and len(ref["yati"]["families"]) == 10


def test_bhavam_shapes(store):
    sources = Counter((p.bhavam or {}).get("source", "none").split(":")[0] for p in store.poems)
    assert sources["corpus_bhavam"] > 150 and sources["generation_meaning"] > 50
    for p in store.poems:
        if p.bhavam:
            assert p.bhavam.get("te") or p.bhavam.get("en")
        if p.hidden["source_dataset"] == "reference" and p.bhavam:
            assert p.bhavam["source"].startswith(("padyarchana_", "manual"))


def test_padyarchana_backfill(store):
    """A Bhāgavatam సీసము head gets the model gloss of the head alone: the edition's bhavam
    also covers the గీతి trailer, which the pool poem does not print."""
    heads = [p for p in store.poems if p.hidden["source_dataset"] == "bhagavatam" and p.meters == ["seesamu"]]
    assert heads and all(p.bhavam["source"].startswith("padyarchana_llm_gloss:") for p in heads)
    assert all(p.has_bhavam for p in store.poems)
    assert {p.id for p in store.poems if p.bhavam["source"] == "manual"} == {"he_0204", "he_0221", "he_0353"}


def test_user_example_bhagavatam_1_1(store):
    """శ్రీకైవల్య…: శార్దూలము మ స జ స త త గ, yati at akshara 13, prāsa on క."""
    poem = store.get("he_0099")
    assert poem.hidden["source_id"] == "1-1-శా."
    pada1 = poem.units[0]["padas"][0]
    assert [g["n"] for g in pada1["ganas"]] == ["మ", "స", "జ", "స", "త", "త", "గ"]
    assert [" ".join(a["t"] for a in g["ak"]) for g in pada1["ganas"]] == [
        "శ్రీ కై వ", "ల్య ప దం", "బుఁ జే రు", "ట కు నై", "చిం తిం చె", "దన్ లో క", "ర"]
    assert [[seat["pos"] for seat in p["yati"]] for p in poem.units[0]["padas"]] == [[[1, 13]]] * 4
    assert [g["ak"][0]["t"] for g in [p["ganas"][4] for p in poem.units[0]["padas"]]] == ["చిం", "సం", "ద్దృ", "నం"]
    assert [p["ganas"][0]["ak"][1]["t"] for p in poem.units[0]["padas"]] == ["కై", "కా", "క", "కం"]


# -----------------------------------------------------------------------------
# build helpers
# -----------------------------------------------------------------------------
def _units(*aksharas_marks):
    aks = [{"i": i, "t": t, "m": m} for i, (t, m) in enumerate(aksharas_marks, 1)]
    return [{"padas": [{"ganas": [{"ak": aks}]}]}]


def test_display_lines_keeps_separators_and_marks():
    lines = build_data.display_lines(["కా వు, నఁ."], _units(("కా", "y"), ("వు", "p"), ("నఁ", "")))
    assert lines == [[{"t": "కా", "c": "y"}, {"t": " ", "s": 1}, {"t": "వు", "c": "p"}, {"t": ", ", "s": 1},
                      {"t": "నఁ"}, {"t": ".", "s": 1}]]


def test_display_lines_matches_decomposed_vowel_signs_and_zero_width():
    decomposed = "మై"            # ె + ౖ, which NFC turns into ై
    lines = build_data.display_lines([decomposed + "ల్‌"], _units(("మై", ""), ("ల్", "")))
    assert "".join(t["t"] for t in lines[0]) == decomposed + "ల్‌"


def test_display_lines_rejects_mismatches():
    with pytest.raises(build_data.BuildError):
        build_data.display_lines(["కాలు"], _units(("కా", ""), ("వు", "")))
    with pytest.raises(build_data.BuildError):
        build_data.display_lines(["కా"], _units(("కా", ""), ("వు", "")))
    with pytest.raises(build_data.BuildError):
        build_data.display_lines(["కావు"], _units(("కా", "")))


@pytest.fixture(scope="module")
def engine():
    try:
        return build_data.load_engine()
    except Exception as exc:                  # noqa: BLE001
        pytest.skip(f"meter_engine not importable: {exc}")


def test_stored_data_matches_a_fresh_engine_run(store, engine):
    """Rebuild a random sample with meter_engine; the shipped JSON must be identical (not stale)."""
    analyze, catalogue, _ = engine
    sources = build_data.load_bhavam_sources()
    pool = {p["eval_id"]: p for p in POOL["poems"]}
    sample = random.Random(0).sample(store.ids, 25) + ["he_0099"]
    sample += [p.id for p in store.poems if len(p.units) > 1][:3]
    for eval_id in sample:
        fresh = build_data.build_poem(pool[eval_id], "strict", analyze, catalogue, sources, {})
        assert fresh == store.get(eval_id).raw, eval_id


def test_line_notes_for_the_upendravajra_example(store):
    """he_0449 (తపస్వివాక్యంబు…): prāsa ప పం పం ప and one yati seat per line, as the user described."""
    poem = store.get("he_0449")
    notes = poem.raw["notes"]
    assert [n["prasa"] for n in notes] == ["ప", "పం", "పం", "ప"]
    assert [[(y["ak"], y["te"]) for y in n["yati"]] for n in notes] == [
        [(["త", "ద"], "వర్గజ యతి")], [(["నె", "ని"], "ప్రాణి యతి")],
        [(["ద", "దా"], "ప్రాణి యతి")], [(["ప్ర", "భ"], "వర్గజ యతి")]]
    assert poem.raw["prasa_summary"] == [{"label": "'ప'కార ప్రాస", "ak": ["ప", "పం", "పం", "ప"]}]


def test_line_notes_cover_every_seat(store):
    for poem in store.poems:
        notes = poem.raw["notes"]
        assert len(notes) == len(poem.lines)
        seats = sum(len(p["yati"]) for u in poem.units for p in u["padas"])
        assert sum(len(n["yati"]) for n in notes) == seats, poem.id
        prasa = sum(1 for u in poem.units for p in u["padas"] if p["prasa"])
        assert sum(1 for n in notes if n["prasa"]) == prasa, poem.id
        for n in notes:
            for y in n["yati"]:
                if y["py"]:                            # prāsa-yati shows the rhyming akshara too
                    assert all(len(a) > 1 for a in y["ak"])


def test_seesamu_seats_go_beside_their_half_line(store):
    poem = store.get("he_0105")                        # సీసము + తేటగీతి, 12 printed lines
    assert [len(n["yati"]) for n in poem.raw["notes"]] == [1] * 12
    assert poem.raw["notes"][4]["yati"][0]["ak"] == ["గిత్త", "బుత్తి"]
