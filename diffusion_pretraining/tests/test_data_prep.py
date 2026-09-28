from __future__ import annotations

import numpy as np

from data_prep.cleaning import Thresholds, clean_doc, normalize, stable_hash, telugu_share
from data_prep.fingerprints import content_mask, minhash, near_duplicate_clusters, window_hashes
from data_prep.sources import Shard, iter_docs
from tokenizer import load_default

TOK = load_default()
PROSE = ("తెలుగు భారతదేశంలోని ద్రావిడ భాషలలో ఒకటి. ఆంధ్రప్రదేశ్ తెలంగాణ రాష్ట్రాల అధికార భాష తెలుగు. "
         "ఈ భాషకు సుదీర్ఘమైన సాహిత్య చరిత్ర ఉంది.")


def test_normalize():
    assert normalize("  తెలుగు‌  భాష \r\n\n\t కవిత  ") == "తెలుగు భాష\nకవిత"
    assert normalize("") == ""


def test_stable_hash_is_deterministic():
    assert stable_hash("తెలుగు") == stable_hash("తెలుగు") != stable_hash("తెలుగు.")
    assert 0 <= stable_hash("x") < 2**64


def test_telugu_share():
    assert telugu_share("తెలుగు") == 1.0
    assert telugu_share("hello") == 0.0
    assert telugu_share("123 !!") == 0.0


def test_clean_doc_drops_boilerplate_urls_and_foreign_lines():
    boiler = "Don't Miss! - వార్తలు"
    text = normalize(f"{boiler}\n{PROSE}\nhttps://example.com చూడండి\nThis line is English only")
    frequent = np.array(sorted([stable_hash(boiler)]), dtype=np.uint64)
    out, why = clean_doc(text, frequent)
    assert why == "" and out == PROSE + "\nచూడండి"          # the URL is cut out, the rest of its line kept


def test_normalize_turns_literal_backslash_n_into_newlines():
    assert normalize("మొదటి వాక్యం\\nరెండవ వాక్యం") == "మొదటి వాక్యం\nరెండవ వాక్యం"


def test_encode_with_stats_counts_rare_telugu_pieces():
    ids, telugu, rare = TOK.encode_with_stats("తెలుగు “quote” सत्य విూరు")
    assert ids == TOK.encode("తెలుగు “quote” सत्य విూరు")
    assert (telugu, rare) == (5, 1)                     # తె లు గు విూ రు; only విూ has no atomic token


def test_clean_doc_rejections():
    assert clean_doc("తెలుగు", None)[1] == "too_short"
    assert clean_doc("English only text here", None)[1] == "no_telugu_lines"
    mostly_english = PROSE + "\n" + "an English sentence that is long enough to dominate " * 3 + "తె"
    assert clean_doc(normalize(mostly_english), None, Thresholds(min_line_telugu_share=0.0))[1] == "low_telugu_share"
    assert clean_doc("\n".join([PROSE] * 5 + ["వేరే వాక్యం ఇక్కడ ఉంది"]), None)[1] == "repeated_lines"


def test_content_mask():
    mask = content_mask(TOK)
    assert not mask[TOK.encode(" ")[0]] and not mask[TOK.encode(".")[0]] and not mask[TOK.encode("7")[0]]
    assert mask[TOK.encode("తె")[0]] and mask[TOK.encode("a")[0]]
    assert not mask[TOK.bos_id]


def test_window_hashes_depend_only_on_content():
    a = np.array([5, 6, 7, 8, 9], dtype=np.uint16)
    b = np.array([1, 5, 6, 7, 2], dtype=np.uint16)
    assert len(window_hashes(a, 3)) == 3 and len(window_hashes(a, 6)) == 0
    assert window_hashes(a, 3)[0] == window_hashes(b, 3)[1]


def _sig(text: str) -> np.ndarray:
    ids = np.asarray(TOK.encode(text), dtype=np.uint16)
    return minhash(window_hashes(ids[content_mask(TOK)[ids]], 8))


def test_minhash_and_near_duplicate_clusters():
    other = ("క్రికెట్ ఒక క్రీడ. ఈ ఆటలో రెండు జట్లు ఉంటాయి. ప్రతి జట్టులో పదకొండు మంది ఆటగాళ్లు ఆడుతారు. "
             "బంతిని బ్యాటుతో కొడతారు.")
    a, a2, b = _sig(PROSE * 3), _sig(PROSE * 3 + " కొత్త పదం"), _sig(other * 3)
    assert (a == a2).mean() > 0.8 and (a == b).mean() < 0.2
    roots = near_duplicate_clusters(np.stack([a, b, a2]))
    assert roots[0] == roots[2] != roots[1]


def test_indiccorp_chunks_cover_every_line_once(tmp_path):
    lines = [f"పేరా {i} " + "అ" * (i % 7) for i in range(200)]
    path = tmp_path / "te.txt"
    path.write_text("\n\n".join(lines) + "\n", encoding="utf-8")
    size = path.stat().st_size
    bounds = [size * i // 7 for i in range(8)]
    got = [d.text for a, b in zip(bounds, bounds[1:]) for d in iter_docs(Shard("indiccorp", str(path), a, b))]
    assert got == [ln.strip() for ln in lines]
