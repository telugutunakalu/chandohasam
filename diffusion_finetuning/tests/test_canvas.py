"""Stage 2 canvases, pools, batches and the role-restricted loss."""
import numpy as np
import pytest
import torch

from ft.batches import Stage2Batches, group_by_length
from ft.canvas import BUCKETS, FILL, GIVEN, TARGET, Pools, Vocab, build, tokenise_record
from ft.loss import role_nelbo
from ft.text import CLASSICAL, MAKUTAM_KEY
from tokenizer import load_default


@pytest.fixture(scope="module")
def v():
    return Vocab(load_default())


def record(i=0, meter="ataveladi", samasya=True, lines=None):
    lines = lines or ["ఉప్పు కప్పురంబు నొక్కపోలికనుండు", "చూడ చూడ రుచుల జాడ వేరు",
                      "పురుషులందు పుణ్య పురుషులు వేరయా", "విశ్వదాభిరామ వినర వేమ"]
    return {"id": f"r{i}", "status": "agree", "meter": meter, "meter_te": "ఆటవెలది", "register": CLASSICAL,
            "lines": lines, "meaning": "ఉప్పు కర్పూరం ఒకేలా ఉంటాయి, రుచి వేరు.", "meaning_src": "గ్రంథం",
            "glosses": [["ఉప్పు", "లవణము", ""], ["కప్పురంబు", "కర్పూరము", ""]],
            "samasya": {"kind": MAKUTAM_KEY, "line": lines[-1]} if samasya else None}


def text_of(v, ids, roles, role):
    return v.tok.decode([int(i) for i, r in zip(ids, roles) if r == role])


def test_T1_roles(v):
    r = tokenise_record(v, record())
    ids, roles = build("T1", v, r, np.random.default_rng(0))
    assert len(ids) in BUCKETS and roles[0] == GIVEN
    target = text_of(v, ids, roles, TARGET)
    assert "ఉప్పు కప్పురంబు" in target and "విశ్వదాభిరామ" not in target     # the makuṭam line is given
    assert "భావం" in text_of(v, ids, roles, GIVEN)
    assert (roles == FILL).sum() >= 1 and all(ids[roles == FILL] == v.eos)


def test_T0_has_no_meaning(v):
    ids, roles = build("T0", v, tokenise_record(v, record()), np.random.default_rng(0))
    assert "కర్పూరం" not in v.tok.decode(ids.tolist())


def test_T2_targets_only_the_meaning(v):
    ids, roles = build("T2", v, tokenise_record(v, record()), np.random.default_rng(0))
    assert text_of(v, ids, roles, TARGET) == "ఉప్పు కర్పూరం ఒకేలా ఉంటాయి, రుచి వేరు."


def test_T3_T4_swap_the_gloss_columns(v):
    r = tokenise_record(v, record())
    ids, roles = build("T3", v, r, np.random.default_rng(0))
    assert text_of(v, ids, roles, TARGET) == "లవణముకర్పూరము"
    ids, roles = build("T4", v, r, np.random.default_rng(0))
    assert text_of(v, ids, roles, TARGET) == "ఉప్పుకప్పురంబు"
    assert (roles == FILL).sum() == 0                     # known length: the <eos> run is given


def test_T5_targets_are_inside_the_free_lines(v):
    r = tokenise_record(v, record())
    for seed in range(20):
        ids, roles = build("T5", v, r, np.random.default_rng(seed))
        target = text_of(v, ids, roles, TARGET)
        assert target and "విశ్వదాభిరామ" not in target and (roles == FILL).sum() == 0


def test_too_long_is_dropped(v):
    r = tokenise_record(v, record(lines=["అ" * 600]))
    assert build("T1", v, r, np.random.default_rng(0)) is None


def test_pools_cap_dvipada_and_upsample_rare_metres(v):
    recs = [tokenise_record(v, record(i, "dvipada", False)) for i in range(900)]
    recs += [tokenise_record(v, record(900 + i, "kandamu", False)) for i in range(600)]
    recs += [tokenise_record(v, record(2000 + i, "malini", False)) for i in range(10)]
    p = Pools(recs)
    probs = np.diff(np.concatenate([[0.0], p.cdf["T1"]]))
    meters = np.asarray([recs[i].meter for i in p.index["T1"]])
    assert abs(probs[meters == "dvipada"].sum() - 0.10) < 1e-6
    kanda, malini = probs[meters == "kandamu"][0], probs[meters == "malini"][0]
    assert abs(malini / kanda - 5.0) < 1e-6


def test_batches_are_deterministic_and_grouped(v):
    recs = [tokenise_record(v, record(i)) for i in range(50)]
    b = Stage2Batches(recs, v, {"T1": 0.4, "T2": 0.2, "T3": 0.1, "T4": 0.05, "T5": 0.15, "T0": 0.1})
    a1, a2 = b.batch(3, 32, seed=1), b.batch(3, 32, seed=1)
    assert [x[0] for x in a1] == [x[0] for x in a2] and all((x[1] == y[1]).all() for x, y in zip(a1, a2))
    for tasks, ids, roles in group_by_length(a1, 4096):
        assert ids.shape == roles.shape and ids.shape[0] * ids.shape[1] <= 4096


def test_role_nelbo_never_masks_given_positions():
    class Toy(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.emb = torch.nn.Embedding(50, 8)

        def hidden(self, x):
            assert not ((x == 49) & (roles == GIVEN)).any()          # <mask> only where maskable
            return self.emb(x)

        def logits(self, h):
            return h @ self.emb.weight.t()

    roles = torch.tensor([[GIVEN, GIVEN, TARGET, TARGET, FILL]])
    x = torch.tensor([[1, 2, 3, 4, 5]])
    out = role_nelbo(Toy(), x, roles, 49, torch.zeros(50), t=torch.ones(1))
    assert len(out["ce"]) == 3 and out["n_target"] == 2 and out["fill"].sum() == 1
    assert torch.allclose(out["row_sum"].sum(), out["sum"].detach())
