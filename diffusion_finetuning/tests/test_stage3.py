"""Stage 3: the constraint compiler and the word lexicon (CPU only)."""
import numpy as np
import pytest

from ft.constraints import Constraint, accepts, build_token_table, poem_budget
from ft.lexicon import LexiconScorer, Trie
from ft.yati_oracle import YatiOracle, check_like_engine
from tokenizer import load_default

GOLD = {
    "utpalamala": ["వాలిన భక్తి మ్రొక్కెద నవారిత తాండవ కేళికిన్ దయా",
                   "శాలికి శూలికిన్ శిఖరిజా ముఖ పద్మ మయూఖ మాలికిన్",
                   "బాల శశాంక మౌళికిఁ గపాలికి మన్మథ గర్వ పర్వతో",
                   "న్మూలికి నారదాది మునిముఖ్య మనస్సరసీరుహాలికిన్"],
    "kandamu": ["పలికెడిది భాగవత మఁట", "పలికించెడివాడు రామభద్రుం డఁట నేఁ",
                "బలికిన భవహర మగునఁట", "పలికెద వేఱొండు గాథ బలుకఁగ నేలా"],
    "seesamu+ataveladi": ["మెఱుఁగు చెంగటనున్నమేఘంబు కైవడి", "నువిద చెంగట నుండనొప్పువాఁడు",
                          "చంద్రమండల సుధాసారంబు పోలిక", "ముఖమునఁ జిఱునవ్వుమొలచువాఁడు",
                          "వల్లీయుత తమాలవసుమతీజము భంగిఁ", "బలువిల్లు మూఁపునఁబరఁగువాఁడు",
                          "నీలనగాగ్ర సన్నిహిత భానుని భంగి", "ఘన కిరీటము దలఁగలుగువాఁడు",
                          "పుండరీకయుగముఁబోలు కన్నుల వాఁడు", "వెడఁద యురమువాఁడు విపులభద్ర",
                          "మూర్తివాఁడు రాజముఖ్యుఁ డొక్కరుఁడు నా", "కన్నుఁగవకు నెదురఁగానఁబడియె"],
}


@pytest.fixture(scope="module")
def tok():
    return load_default()


@pytest.fixture(scope="module")
def tt(tok):
    return build_token_table(tok)


def ids_of(tok, lines):
    return tok.encode("\n".join(lines)) + [tok.eos_id]


@pytest.mark.parametrize("label", sorted(GOLD))
def test_gold_poems_are_accepted(tok, tt, label):
    ok, at = accepts(Constraint(label, tt), ids_of(tok, GOLD[label]))
    assert ok, f"rejected at token {at}"


def test_a_line_too_short_is_rejected(tok, tt):
    lines = list(GOLD["utpalamala"])
    lines[1] = lines[1].rsplit(" ", 1)[0]                 # drop the last word of line 2
    assert not accepts(Constraint("utpalamala", tt), ids_of(tok, lines))[0]


def test_prasa_is_enforced(tok, tt):
    lines = list(GOLD["utpalamala"])
    lines[2] = "బాణ" + lines[2][2:]                        # line 3's prāsa letter ల -> ణ
    assert not accepts(Constraint("utpalamala", tt), ids_of(tok, lines))[0]


def test_eos_only_after_the_last_line(tok, tt):
    con = Constraint("kandamu", tt)
    st = con.initial()
    for t in tok.encode("\n".join(GOLD["kandamu"][:3])):
        st = con.advance(st, t)
    assert not con.allowed(st)[0][tok.eos_id]


@pytest.mark.parametrize("label", ["kandamu", "utpalamala", "seesamu+tetagiti", "dvipada", "ataveladi",
                                   "hayapracara_ragada", "turagagati_ragada"])
@pytest.mark.parametrize("vikalpa", [True, False])
def test_random_walks_never_dead_end(tt, label, vikalpa):
    rng = np.random.default_rng(0)
    for _ in range(5):
        con = Constraint(label, tt, vikalpa=vikalpa)
        st = con.initial()
        for _ in range(poem_budget(label) + 50):
            mask, _ = con.allowed(st)
            idx = np.flatnonzero(mask)
            assert len(idx), "dead end"
            special = [i for i in idx if i in (tt.space, tt.newline, tt.eos)]
            t = tt.eos if tt.eos in idx else int(rng.choice(special)) if special and rng.random() < 0.3 else \
                int(rng.choice([i for i in idx if i not in special] or special))
            st = con.advance(st, t)
            if t == tt.eos:
                break
        assert st.done


def test_trie_and_lexicon_penalties(tt):
    a, b, c, d, e = (int(x) for x in np.flatnonzero(tt.is_syl)[:5])       # five syllable tokens
    trie = Trie.build([[a, b], [a, c, d], [e]])
    assert trie.contains([a, b]) and trie.contains([e]) and not trie.contains([a]) and not trie.contains([a, c])
    scorer = LexiconScorer(trie, tt, lam=2.0, lam2=0.5)
    node = scorer.advance(0, a)
    pen = scorer.penalty(node)
    assert pen[b] == 0 and pen[c] == 0 and pen[e] == -2.0 and pen[tt.space] == -2.0      # inside a word
    node = scorer.advance(node, b)                                                        # a complete word
    pen = scorer.penalty(node)
    assert pen[tt.space] == 0 and pen[e] == -0.5 and pen[d] == -2.0                       # compound restart
    assert scorer.advance(node, e) >= 0 and scorer.advance(scorer.advance(0, d), b) == -1


# ---- the rule gaps found on the pilot grid (experiments/pilot_grid/README.md) ----------------------
def walk(con, tok, text):
    st = con.initial()
    for t in tok.encode(text):
        st = con.advance(st, t)
    return st


@pytest.fixture(scope="module")
def strict_oracle(tok, tt):
    return YatiOracle(tok, tt, "strict", "off")


@pytest.mark.parametrize("profile,sandhi", [("relaxed", "hypothesis"), ("strict", "off")])
def test_yati_oracle_equals_the_engine(tok, tt, profile, sandhi):
    """The oracle's verdict is yati.check's, in every context the decoder builds."""
    o = YatiOracle(tok, tt, profile, sandhi)
    rng = np.random.default_rng(0)
    feat = o.feat
    pick = lambda cond: int(rng.choice([t for t, f in feat.items() if cond(f)]))       # noqa: E731
    prevs = [pick(lambda f: f[3]),                                  # ends in ఁ (evidence for a word-initial seat)
             pick(lambda f: f[1] == "ఉ" and not f[2]),              # vowel ఉ without anusvara (augment evidence)
             pick(lambda f: f[2]),                                  # anusvara (a bindu before the seat)
             pick(lambda f: "న" in f[4])]                           # a pollu న (drutam fuses into the seat)
    seat_ctxs = [o.after_ctx(p, wi) for p in prevs for wi in (True, False)]
    head_ctxs = [o.line_head_ctx(-1, True), o.line_head_ctx(prevs[3], False), o.after_ctx(prevs[0], True)]
    heads = [tok.piece_to_id[x] for x in ("న", "య", "త", "కా", "స్త్రీ", "అ")]
    seats = [tok.piece_to_id[x] for x in ("న", "య", "ట", "ని", "యా", "త", "ద", "హ", "బ", "అ", "ఇ", "క్ష")]
    seats += [int(t) for t in rng.choice(list(feat), 20, replace=False)]
    n = 0
    for h in heads:
        for hc in head_ctxs:
            for sc_ in seat_ctxs[::2] + seat_ctxs[1::3]:
                row = o.row(h, hc, sc_)
                for t in seats:
                    assert bool(row[t]) == check_like_engine(o, h, hc, t, sc_), (o.text[h], hc, o.text[t], sc_)
                    n += 1
    assert n > 1000


def test_yati_seat_verdict_follows_its_context(tok, tt, strict_oracle):
    """A word-initial న at the head (not the first pāda) carries the drutam evidence that makes న~య a yati."""
    o, na, ya = strict_oracle, tok.piece_to_id["న"], tok.piece_to_id["య"]
    seat = o.after_ctx(tok.piece_to_id["క"], True)
    assert o.row(na, o.line_head_ctx(-1, False), seat)[ya]
    assert not o.row(na, o.line_head_ctx(-1, True), seat)[ya]
    assert not o.row(tok.piece_to_id["త"], o.line_head_ctx(-1, False), seat)[ya]      # త~య: no maitri


def test_yati_is_penalised_at_the_seat(tok, tt, strict_oracle):
    """utpalamala: akshara 10 must be in maitri with akshara 1 (వా): వా passes, క does not."""
    con = Constraint("utpalamala", tt, strict_oracle)
    st = walk(con, tok, "వాలిన భక్తి మ్రొక్కెద న")                 # the gold line's first nine aksharas
    sp = con.spec(st)
    assert sp.yati is not None and sp.yati[0] == tok.piece_to_id["వా"]
    _, pen = con.mask_of(sp)
    assert pen[tok.piece_to_id["వా"]] == 0 and pen[tok.piece_to_id["క"]] < 0


def test_seesa_half_break_is_required(tok, tt):
    """A sīsa pāda cannot run on into its second half without the half-break."""
    gold = GOLD["seesamu+ataveladi"]
    joined = [gold[0] + " " + gold[1]] + gold[2:]
    assert not accepts(Constraint("seesamu+ataveladi", tt), ids_of(tok, joined))[0]
    assert accepts(Constraint("seesamu+ataveladi", tt), ids_of(tok, gold))[0]


def test_seesa_second_half_has_its_own_yati_head(tok, tt, strict_oracle):
    gold = GOLD["seesamu+ataveladi"]
    con = Constraint("seesamu+ataveladi", tt, strict_oracle)
    st = walk(con, tok, gold[0] + "\n")
    first = tok.encode(gold[1])[0]
    st = con.advance(st, first)
    assert st.head == first and st.syl_in_half == 1


def test_no_pada_after_the_last(tok, tt):
    """The couplet metres chain couplets in the grammar; the poem still ends after its pādas."""
    rng = np.random.default_rng(1)
    for label in ("dvipada", "hayapracara_ragada", "madhuragati_ragada"):
        con = Constraint(label, tt)
        st, lines = con.initial(), 0
        for _ in range(poem_budget(label) + 50):
            mask, _ = con.allowed(st)
            idx = np.flatnonzero(mask)
            if mask[tt.eos]:
                break
            t = tt.newline if mask[tt.newline] else int(rng.choice([i for i in idx if i != tt.space] or idx))
            lines += t == tt.newline
            st = con.advance(st, t)
        assert mask[tt.eos] and lines == con.nfa.padalu[-1] - 1


def test_prasa_akshara_is_not_a_bare_vowel(tok, tt):
    con = Constraint("kandamu", tt)
    st = walk(con, tok, "ప")                                     # line 1, after the pre-prāsa akshara
    mask, _ = con.allowed(st)
    assert not mask[tt.vowel_onset].any() and mask[tok.piece_to_id["లి"]]


def test_pre_prasa_weight_is_uniform(tok, tt):
    """PRASA-PURVAKSHARA-01: kandamu line 1 starts laghu (ప), so line 2 may not start guru (పా);
    utpalamala line 1 starts guru (వా) with a single-consonant prāsa (లి), so a light head is out."""
    con = Constraint("kandamu", tt)
    st = walk(con, tok, GOLD["kandamu"][0] + "\n")
    mask, _ = con.allowed(st)
    assert mask[tok.piece_to_id["ప"]] and not mask[tok.piece_to_id["పా"]]
    con = Constraint("utpalamala", tt)
    st = walk(con, tok, GOLD["utpalamala"][0] + "\n")
    mask, _ = con.allowed(st)
    assert mask[tok.piece_to_id["శా"]] and not mask[tok.piece_to_id["శ"]]


def test_bahuyati_one_constituent_serves_every_seat(tok, tt, strict_oracle):
    """YATI-SY-11: once శ్రీ's ర has served a seat, a later seat cannot rely on its శ alone."""
    o = strict_oracle
    h = tok.piece_to_id["శ్రీ"]
    hc = o.line_head_ctx(-1, True)
    sc_ = o.after_ctx(tok.piece_to_id["క"], True)
    ri, si = tok.piece_to_id["రి"], tok.piece_to_id["శి"]
    by_ra, by_sa = o.served(h, hc, ri, sc_), o.served(h, hc, si, sc_)
    assert by_ra and by_sa and not (by_ra & by_sa)
    assert o.row(h, hc, sc_)[si] and not o.row(h, hc, sc_, by_ra)[si] and o.row(h, hc, sc_, by_ra)[ri]


def test_seat_grouping_follows_the_stanza_planner(tok, tt, strict_oracle):
    """సీసము (two yati points) re-heads its second half; మానిని (three, one బహుయతి group) keeps the pāda head."""
    gold = GOLD["seesamu+ataveladi"]
    con = Constraint("seesamu+ataveladi", tt, strict_oracle)
    st = walk(con, tok, gold[0] + "\n")
    first = tok.encode(gold[1])[0]
    assert con.advance(st, first).head == first
    con = Constraint("manini", tt, strict_oracle)
    assert con.nfa.yati_group == ("bahu",) and con.nfa.half_gana == (5,)
    rng = np.random.default_rng(3)
    st = con.initial()
    while not st.half_open:                       # write the first half, then its half-break
        mask, _ = con.allowed(st)
        t = tt.newline if mask[tt.newline] and st.syl_in_line > 0 else int(rng.choice(
            [i for i in np.flatnonzero(mask) if i not in (tt.space, tt.newline, tt.eos)]))
        st = con.advance(st, t)
    head = st.head
    mask, _ = con.allowed(st)
    st = con.advance(st, int(rng.choice([i for i in np.flatnonzero(mask) if tt.is_syl[i]])))
    assert st.head == head


def test_a_pollu_on_the_head_fuses_into_the_prasa(tok, tt):
    """PRASA-POS-06: line 1 rhymes on లి (plain ల), so a later head may not end in a pollu that would fuse
    into it (తమ్ + లి reads మ్ల); and after a pollu head, a bare vowel can carry line 1's prāsa."""
    con = Constraint("kandamu", tt)
    st = walk(con, tok, GOLD["kandamu"][0] + "\n")
    mask, _ = con.allowed(st)
    polluted = [i for i in np.flatnonzero(mask) if tt.is_syl[i] and tt.pollu[i] != 0]
    assert not polluted and mask[tok.piece_to_id["ప"]]
    head = tok.piece_to_id["కన్"]                                 # guru by its pollu న: gaṇa భ or గా
    assert tt.pollu_tuples[tt.pollu[head]] == ("న",)
    mask, _ = con.allowed(con.advance(con.initial(), head))
    assert mask[tt.vowel_onset].any()                            # న + a bare vowel still rhymes on న
    mask, _ = con.allowed(con.advance(con.initial(), tok.piece_to_id["క"]))
    assert not mask[tt.vowel_onset].any()
