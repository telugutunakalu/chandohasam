"""Apply the NaN-entropy fix to the shared decoder (user decision 2026-10-21) and add its regression test.

    ../.venv/bin/python fix_canvas_entropy.py        # idempotent; only when no constrained run is using the package

metrical_decoder/diffusion/canvas.py, CanvasPass: with ``forbid_end`` the end tokens' scaled logits are −inf, so
−Σ p log p was NaN at every position (0 · −inf); every entropy comparison then failed (the canvas kept no prediction
and the decoder's entropy bound never stopped a run of proposals). torch.special.entr defines entr(0) = 0.
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "meter_engine"
canvas = ROOT / "metrical_decoder" / "diffusion" / "canvas.py"
tests = ROOT / "tests" / "test_dec_diffusion.py"

old = "        self._entropy = (-(probs * log_probs).sum(-1)).tolist()\n"
new = ("        # entr(p) = −p log p with entr(0) = 0. With ``forbid_end`` the end tokens' scaled logits are −inf and\n"
       "        # −Σ p log p was NaN (0 · −inf) at every position: every entropy comparison failed, so the canvas kept\n"
       "        # no prediction and the entropy bound never stopped a run of proposals (fixed 2026-10-21).\n"
       "        self._entropy = torch.special.entr(probs).sum(-1).tolist()\n")
s = canvas.read_text(encoding="utf-8")
if new not in s:
    assert s.count(old) == 1, "CanvasPass entropy line not found"
    tmp = canvas.with_suffix(".py.tmp"); tmp.write_text(s.replace(old, new), encoding="utf-8"); os.replace(tmp, canvas)
    print("canvas.py: fixed")
else:
    print("canvas.py: already fixed")

test = '''

class TestCanvasPassEntropy(unittest.TestCase):
    """CanvasPass entropies stay finite when end tokens are removed (forbid_end: −inf logits); 2026-10-21."""

    def test_finite_with_forbidden_tokens(self):
        import math
        from metrical_decoder.diffusion.canvas import CanvasPass
        g = torch.Generator().manual_seed(0)
        logits = torch.randn(6, 50, generator=g)
        scaled = logits / 0.8
        banned = (0, 3, 7)
        scaled[:, list(banned)] = float("-inf")
        fake = types.SimpleNamespace(torch=torch, generator=torch.Generator().manual_seed(1), slice=torch.arange(10),
                                     top_k=3)
        p = CanvasPass(fake, logits, scaled, first=0)
        keep = [i for i in range(50) if i not in banned]
        ref = torch.distributions.Categorical(logits=scaled[:, keep]).entropy()
        for pos in range(6):
            self.assertTrue(math.isfinite(p.entropy(pos)))
            self.assertAlmostEqual(p.entropy(pos), float(ref[pos]), places=4)
'''
t = tests.read_text(encoding="utf-8")
if "class TestCanvasPassEntropy" not in t:
    marker = "\n\nif __name__ == \"__main__\":"
    t = t.replace(marker, test + marker, 1) if marker in t else t.rstrip("\n") + test
    tmp = tests.with_suffix(".py.tmp"); tmp.write_text(t, encoding="utf-8"); os.replace(tmp, tests)
    print("test_dec_diffusion.py: test added")
else:
    print("test_dec_diffusion.py: test already present")
