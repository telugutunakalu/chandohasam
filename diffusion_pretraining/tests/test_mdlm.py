from __future__ import annotations

import math

import numpy as np
import torch

from mdlm.data import TokenMixture
from mdlm.diffusion import forward_mask, invalid_bias, nelbo, sample_t
from mdlm.model import Denoiser, ModelConfig
from mdlm.sampling import sample
from mdlm.train import TrainConfig, lr_at

V, MASK, PAD, UNK = 45591, 4, 0, 1
CFG = ModelConfig(vocab_size=V, d_model=64, n_layers=2, n_heads=4, mlp_hidden=128, max_len=64)


def _model(seed: int = 0) -> Denoiser:
    torch.manual_seed(seed)
    return Denoiser(CFG)


def _bias() -> torch.Tensor:
    return invalid_bias(CFG.padded_vocab, V, [MASK, PAD, UNK])


def test_invalid_bias_blocks_specials_and_padding():
    b = _bias()
    assert CFG.padded_vocab % 128 == 0 and CFG.padded_vocab >= V
    assert torch.isinf(b[[MASK, PAD, UNK]]).all() and torch.isinf(b[V:]).all()
    assert b[2] == 0 and b[3] == 0 and b[1000] == 0          # <bos>, <eos>, ordinary tokens


def test_sample_t_is_spread_over_the_batch():
    t = sample_t(8, "cpu", torch.Generator().manual_seed(0))
    assert t.min() > 0 and t.max() <= 1
    gaps = torch.sort(t).values.diff()
    assert torch.allclose(gaps, torch.full_like(gaps, (1 - 1e-3) / 8), atol=1e-5)


def test_forward_mask_rate():
    x0 = torch.randint(10, V, (4, 4000))
    t = torch.tensor([0.1, 0.4, 0.7, 0.95])
    xt, m = forward_mask(x0, t, MASK, torch.Generator().manual_seed(0))
    assert torch.allclose(m.float().mean(1), t, atol=0.03)
    assert (xt[m] == MASK).all() and (xt[~m] == x0[~m]).all()


def test_initial_loss_is_log_vocab_and_only_masked_positions_count():
    x0 = torch.randint(10, V, (16, 64))
    out = nelbo(_model(), x0, MASK, _bias(), generator=torch.Generator().manual_seed(1))
    assert abs(out["loss"].item() - math.log(V - 3)) < 0.5
    t = torch.full((16,), 0.5)
    out = nelbo(_model(), x0, MASK, _bias(), t=t, generator=torch.Generator().manual_seed(2))
    _, m = forward_mask(x0, t, MASK, torch.Generator().manual_seed(2))
    assert out["ce"].numel() == int(m.sum())


def test_model_overfits_one_batch():
    model = _model()
    opt = torch.optim.AdamW(model.parameters(), lr=3e-3)
    x0 = torch.randint(10, 60, (8, 64))                     # a small alphabet, learnable quickly
    t = torch.full((8,), 0.5)
    losses = []
    for step in range(60):
        out = nelbo(model, x0, MASK, _bias(), t=t, generator=torch.Generator().manual_seed(step))
        opt.zero_grad()
        out["loss"].backward()
        opt.step()
        losses.append(out["loss"].item())
    assert losses[-1] < 0.5 * losses[0]


def test_samplers_reveal_every_position_and_never_emit_mask():
    for strategy in ("ancestral", "confidence"):
        ids, nfe = sample(_model(), 2, 32, 8, MASK, _bias(), strategy=strategy,
                          generator=torch.Generator().manual_seed(0))
        assert ids.shape == (2, 32) and not (ids == MASK).any() and not (ids >= V).any()
        assert 1 <= nfe <= 8


def test_sampler_keeps_the_prefix():
    prefix = torch.tensor([[2, 100, 200], [2, 300, 400]])
    ids, _ = sample(_model(), 2, 16, 4, MASK, _bias(), prefix=prefix, generator=torch.Generator().manual_seed(0))
    assert (ids[:, :3] == prefix).all()


def test_batches_are_a_pure_function_of_seed_and_step(tmp_path):
    for src, n in (("a", 5000), ("b", 3000)):
        (tmp_path / src).mkdir()
        np.arange(n, dtype=np.uint16).tofile(tmp_path / src / "train.bin")
    mix = TokenMixture(tmp_path, {"a": 0.7, "b": 0.3}, seq_len=64)
    assert torch.equal(mix.batch(5, 4, seed=1), mix.batch(5, 4, seed=1))
    assert not torch.equal(mix.batch(5, 4, seed=1), mix.batch(6, 4, seed=1))
    b = mix.batch(0, 32)
    assert (b[:, 1:] - b[:, :-1] == 1).all()                  # contiguous windows


def test_lr_schedule():
    cfg = TrainConfig(lr=1e-3, warmup_steps=100, total_steps=1100, min_lr_ratio=0.1)
    assert lr_at(0, cfg) == 1e-5 and abs(lr_at(99, cfg) - 1e-3) < 1e-12
    assert abs(lr_at(1100, cfg) - 1e-4) < 1e-12 and abs(lr_at(600, cfg) - 5.5e-4) < 1e-9


def test_step_survives_out_of_memory_by_halving_the_micro_batch():
    from mdlm.train import accumulate_step
    model = _model()

    class Flaky:                                            # "runs out of memory" above 4 sequences
        logits = model.logits

        def hidden(self, x):
            if x.shape[0] > 4:
                raise torch.OutOfMemoryError("simulated")
            return model.hidden(x)

    x = torch.randint(10, V, (16, 64))
    loss, micro = accumulate_step(Flaky(), model, x, 16, MASK, _bias(), seed=0, device=torch.device("cpu"))
    assert micro == 4 and torch.isfinite(loss)
    grads = [p.grad for p in model.parameters()]
    model.zero_grad(set_to_none=True)
    ref, _ = accumulate_step(model, model, x, 4, MASK, _bias(), seed=0, device=torch.device("cpu"))
    assert torch.allclose(loss, ref)                        # the retried step is the same computation
    assert all(torch.allclose(a, p.grad) for a, p in zip(grads, model.parameters()))
