"""Text cleaning, layout canonicalisation and the Stage 1 documents."""
from ft.build_data import encode_pieces, stage1_pieces
from ft.metres import canonicalise, parse_label
from ft.text import CLASSICAL, MAKUTAM_KEY, clean_poem_line, raw_lines, split_pieces
from tokenizer import load_default

SEESA_HALVES = [  # Bhagavatam 1-16 style: a sīsa printed in half-lines, then its āṭaveladi
    "మెఱుఁగు చెంగటనున్నమేఘంబు కైవడి-", "నువిద చెంగట నుండనొప్పువాఁడు,",
    "చంద్రమండల సుధాసారంబు పోలిక-", "ముఖమునఁ జిఱునవ్వుమొలచువాఁడు,",
    "వల్లీయుత తమాలవసుమతీజము భంగిఁ-", "బలువిల్లు మూఁపునఁబరఁగువాఁడు,",
    "నీలనగాగ్ర సన్నిహిత భానుని భంగి-", "ఘన కిరీటము దలఁగలుగువాఁడు,",
]


def test_clean_poem_line_keeps_only_telugu_and_single_spaces():
    assert clean_poem_line("కనుగొంటిన్‌ రఘురామపత్ని, నల!  లంక-") == "కనుగొంటిన్ రఘురామపత్ని నల లంక"
    assert clean_poem_line("౧౨ | ।") == ""


def test_raw_lines_strips_zwnj_so_separators_are_seen():
    lines = raw_lines(["ముందు జానకి లంక మూర్ఖించి చొచ్చి నిన్‌- దెచ్చినరిపుల సాధించినావు"])
    assert split_pieces(lines) == ["ముందు జానకి లంక మూర్ఖించి చొచ్చి నిన్", "దెచ్చినరిపుల సాధించినావు"]


def test_split_pieces_keeps_a_line_final_hyphen():
    assert split_pieces(["అ ఆ | ఇ ఈ", "ఉ ఊ-"]) == ["అ ఆ", "ఇ ఈ", "ఉ ఊ-"]


def test_parse_label():
    assert parse_label("సీసము + తేటగీతి") == (frozenset({"seesamu"}), "tetagiti")
    assert parse_label("ఆటవెలది/తేటగీతి")[0] == frozenset({"ataveladi", "tetagiti"})
    assert parse_label("వచనము") == (frozenset(), None)
    assert parse_label("మత్తకోకిల")[0] == frozenset({"mattakokilamu"})
    assert parse_label("కందం")[0] == frozenset({"kandamu"})
    assert parse_label("స్రగ్విణీ")[0] == frozenset({"sragvini"})


def test_kanda_printed_two_padas_per_line_is_split_by_search():
    printed = ["ఎంతటి విద్యల నేర్చిన సంతసముగ వస్తుతతులు సంపాదింపన్‌",
               "జింతించి చూడ నన్నియు గొంతుకఁ తడుపుకొను కొఱకె గువ్వలచెన్నా!"]
    c = canonicalise(raw_lines(printed), "కందము")
    assert c.status == "agree" and c.meter == "kandamu" and c.layout == "search"
    assert len(c.lines) == 4 and c.roundtrip


def test_seesa_stays_in_half_lines():
    c = canonicalise(raw_lines(SEESA_HALVES), "సీసము")
    assert c.meter == "seesamu"
    assert len(c.lines) == 8                        # the halves are kept (yati needs them)
    assert c.lines[0] == "మెఱుఁగు చెంగటనున్నమేఘంబు కైవడి"


def test_stage1_document_fixes_the_shared_last_line():
    tok = load_default()
    rec = {"id": "x1", "status": "agree", "meter_te": "ఆటవెలది", "register": CLASSICAL,
           "samasya": {"kind": MAKUTAM_KEY, "line": "విశ్వదాభిరామ వినర వేమ"},
           "lines": ["ఒకటి", "విశ్వదాభిరామ వినర వేమ"], "meaning": "అర్థం", "meaning_src": "గ్రంథం"}
    ids, flags = encode_pieces(tok, stage1_pieces(rec, seed=0))
    assert ids[0] == tok.bos_id and ids[-1] == tok.eos_id and len(ids) == len(flags)
    fixed = tok.decode([i for i, f in zip(ids, flags) if f == 0])
    assert fixed == "విశ్వదాభిరామ వినర వేమ" * 2      # the header copy and the poem's last line
    assert "ఒకటి" in tok.decode([i for i, f in zip(ids, flags) if f == 1])
