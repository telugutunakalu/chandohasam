from __future__ import annotations

import dataclasses

import pytest
import torch

from mdlm.grow import grow, plan
from mdlm.model import PRESETS, Denoiser, ModelConfig

SRC = ModelConfig(vocab_size=300, d_model=128, n_layers=3, n_heads=2, mlp_hidden=256, max_len=32)


def _trained_looking(cfg: ModelConfig, seed: int) -> Denoiser:
    """A float64 model whose weights, RMSNorm gains included, are not at their init values."""
    torch.manual_seed(seed)
    model = Denoiser(cfg).double()
    with torch.no_grad():
        for p in model.parameters():
            p.add_(torch.randn_like(p) * 0.05)
    return model.eval()


def _grown(small: Denoiser, dst: ModelConfig, noise: float) -> Denoiser:
    big = Denoiser(dst).double().eval()
    big.load_state_dict(grow(small.state_dict(), small.cfg, dst, noise=noise, seed=1, dtype=torch.float64))
    return big


@pytest.mark.parametrize("dst", [
    dataclasses.replace(SRC, d_model=256, n_heads=4, mlp_hidden=512),                     # width x2
    dataclasses.replace(SRC, n_layers=7),                                                   # depth only
    dataclasses.replace(SRC, d_model=384, n_heads=6, mlp_hidden=768, n_layers=5),           # width x3 and depth
], ids=["width", "depth", "width+depth"])
def test_grown_model_computes_the_same_logits(dst):
    small = _trained_looking(SRC, 0)
    big = _grown(small, dst, noise=0.5)
    x = torch.randint(0, SRC.vocab_size, (3, SRC.max_len), generator=torch.Generator().manual_seed(2))
    with torch.no_grad():
        torch.testing.assert_close(big(x), small(x), rtol=1e-9, atol=1e-9)


def test_noise_makes_the_copies_learn_differently():
    dst = dataclasses.replace(SRC, d_model=256, n_heads=4, mlp_hidden=512)
    x = torch.randint(0, SRC.vocab_size, (2, SRC.max_len), generator=torch.Generator().manual_seed(3))
    small = _trained_looking(SRC, 0)
    grads = {}
    for noise in (0.0, 0.1):
        big = _grown(small, dst, noise)
        big(x).logsumexp(-1).sum().backward()
        g = big.embed.weight.grad
        grads[noise] = (g[:, :SRC.d_model], g[:, SRC.d_model:])
    torch.testing.assert_close(*grads[0.0])              # exact clones stay clones forever
    assert not torch.allclose(*grads[0.1])               # the noise lets them drift apart


def test_new_blocks_start_as_zero_output_copies():
    dst = dataclasses.replace(SRC, n_layers=6)
    small = _trained_looking(SRC, 0)
    sd = grow(small.state_dict(), SRC, dst, dtype=torch.float64)
    for new, old in ((1, 0), (3, 1), (5, 2)):             # one new block after each old one
        assert torch.equal(sd[f"blocks.{new}.qkv.weight"], small.state_dict()[f"blocks.{old}.qkv.weight"])
        assert not sd[f"blocks.{new}.proj.weight"].any() and not sd[f"blocks.{new}.down.weight"].any()


def test_growth_ladder_presets_are_reachable():
    assert plan(PRESETS["small-768"], PRESETS["grow-1536x16"]) == (2, [2, 5, 8, 11])
    assert plan(PRESETS["grow-1536x16"], PRESETS["grow-1536x32"]) == (1, list(range(16)))
    assert plan(PRESETS["small-768"], PRESETS["grow-2304x16"])[0] == 3
    with pytest.raises(ValueError):
        plan(PRESETS["small-768"], PRESETS["small-512"])     # 512 is not a multiple of 768
    with pytest.raises(ValueError):
        plan(PRESETS["grow-1536x32"], PRESETS["grow-1536x16"])   # layers cannot be removed
