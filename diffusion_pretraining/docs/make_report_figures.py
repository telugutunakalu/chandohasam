"""Figures for docs/pilot120m_training_report.md, drawn from runs/pilot120m/{metrics,judge,config}.

    uv run --with matplotlib python docs/make_report_figures.py

Writes docs/figures/: the architecture diagram, loss curves, masked-token accuracy,
sample quality, and the learning-rate schedule with the gradient norm. Reference
values for real Telugu come from mdlm.judge --calibrate on 30 validation canvases
(CPU, float32, the setting the run's judge uses) and from sample_metrics on real
validation text.
"""
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs" / "pilot120m"
OUT = ROOT / "docs" / "figures"


def architecture():
    EDGE = "#34495e"
    fig, ax = plt.subplots(figsize=(10, 9.6))
    ax.set_xlim(0, 10); ax.set_ylim(1.7, 14.4); ax.axis("off")

    def box(cx, cy, w, h, text, fc, fs=8.5, ec=EDGE, lw=1.0, weight="normal"):
        ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc=fc, ec=ec, lw=lw))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, weight=weight, linespacing=1.35)
        return cx, cy, w, h

    def down(a, b):
        ax.annotate("", xy=(b[0], b[1] + b[3] / 2), xytext=(a[0], a[1] - a[3] / 2),
                    arrowprops=dict(arrowstyle="-|>", color=EDGE, lw=1.1, shrinkA=1, shrinkB=1))

    def skip(a, b, x_side):
        """residual path: from the right edge of box a, down the side, into the right edge of box b"""
        y1, y2 = a[1], b[1]
        ax.plot([a[0] + a[2] / 2, x_side, x_side], [y1, y1, y2], color="#7f8c8d", lw=1.1)
        ax.annotate("", xy=(b[0] + b[2] / 2, y2), xytext=(x_side, y2),
                    arrowprops=dict(arrowstyle="-|>", color="#7f8c8d", lw=1.1, shrinkA=0, shrinkB=1))

    ax.text(5, 14.15, "pilot120m (small-768): bidirectional transformer denoiser for masked diffusion (MDLM)",
            ha="center", va="center", fontsize=11.5, weight="bold")

    # ---- left: the whole model ----
    L = 2.55; W = 4.3
    b_in = box(L, 13.2, W, 0.8, "Noisy canvas $x_t$: 512 tokens\n(each token replaced by [MASK] with probability t)", "#eceff1")
    b_emb = box(L, 11.95, W, 0.8, "Token embedding E (tied with the output)\n45,696 × 768  ·  35.1M parameters", "#d6e4f0")
    b_blk = box(L, 10.35, W, 1.25, "Transformer block  × 12\n\npre-norm · bidirectional attention · SwiGLU\n7.08M parameters each  ·  85.0M in total",
                "#aec9e3", lw=1.6, weight="normal")
    b_norm = box(L, 8.8, W, 0.6, "Final RMSNorm", "#d6e4f0")
    b_out = box(L, 7.65, W, 0.8, "Logits = h · Eᵀ  (the same matrix E)\n45,696 scores per position", "#d6e4f0")
    b_subs = box(L, 6.3, W, 1.0, "SUBS parameterisation\n[MASK], <pad>, <unk>, padding rows → −∞\nunmasked positions are copied unchanged", "#fdebd0")
    b_loss = box(L, 4.85, W, 1.0, "Training loss (NELBO)\nΣ over masked positions of cross-entropy / t\n÷ (batch × 512)  →  nats per token", "#fadbd8")
    b_samp = box(L, 3.35, W, 1.1, "Generation\nstart from 512 × [MASK]; 256 ancestral steps\neach step unmasks some positions with\ntokens drawn from the model", "#e8f5e9")
    for a, b in ((b_in, b_emb), (b_emb, b_blk), (b_blk, b_norm), (b_norm, b_out), (b_out, b_subs), (b_subs, b_loss)):
        down(a, b)
    # training uses the SUBS output in the loss; inference samples from it instead
    ax.text(L + 0.1, (b_subs[1] - b_subs[3] / 2 + b_loss[1] + b_loss[3] / 2) / 2, "training", fontsize=7.5, color=EDGE, va="center")
    xs = L - W / 2 - 0.22
    ax.plot([L - W / 2, xs, xs], [b_subs[1], b_subs[1], b_samp[1]], color="#2e7d32", lw=1.1, ls="--")
    ax.annotate("", xy=(L - W / 2, b_samp[1]), xytext=(xs, b_samp[1]),
                arrowprops=dict(arrowstyle="-|>", color="#2e7d32", lw=1.1, shrinkA=0, shrinkB=1))
    ax.text(xs - 0.08, (b_subs[1] + b_samp[1]) / 2, "inference", fontsize=7.5, color="#2e7d32", va="center", ha="right", rotation=90)

    # ---- right: inside one block ----
    R = 7.45; RW = 3.6
    ax.add_patch(FancyBboxPatch((5.35, 4.05), 4.45, 9.55, boxstyle="round,pad=0.02,rounding_size=0.2",
                                fc="#f7f9fb", ec="#9aa5b1", lw=1.0, ls="--"))
    ax.text(7.55, 13.35, "inside one block", ha="center", fontsize=9.5, style="italic", color="#34495e")
    r_x = box(R, 12.75, RW, 0.55, "h  (batch × 512 × 768)", "#eceff1", fs=8)
    r_n1 = box(R, 11.9, RW, 0.5, "RMSNorm", "#d6e4f0", fs=8)
    r_att = box(R, 10.75, RW, 1.3, "Multi-head self-attention, no causal mask\n12 heads × 64 dims, RoPE on q and k\nfused QKV 768 → 2,304 · output 768 → 768\n2.36M parameters", "#aec9e3", fs=8)
    r_a1 = box(R, 9.55, RW, 0.45, "⊕  add residual", "#ffffff", fs=8)
    r_n2 = box(R, 8.8, RW, 0.5, "RMSNorm", "#d6e4f0", fs=8)
    r_mlp = box(R, 7.6, RW, 1.3, "SwiGLU MLP\ngate, up: 768 → 2 × 2,048\nSiLU(gate) ⊙ up, then down: 2,048 → 768\n4.72M parameters", "#aec9e3", fs=8)
    r_a2 = box(R, 6.4, RW, 0.45, "⊕  add residual", "#ffffff", fs=8)
    r_o = box(R, 5.55, RW, 0.55, "h′  (batch × 512 × 768)", "#eceff1", fs=8)
    for a, b in ((r_x, r_n1), (r_n1, r_att), (r_att, r_a1), (r_a1, r_n2), (r_n2, r_mlp), (r_mlp, r_a2), (r_a2, r_o)):
        down(a, b)
    skip(r_x, r_a1, 9.55)
    skip(r_a1, r_a2, 9.55)
    ax.text(7.55, 4.6, "no timestep input · no biases · no dropout\nbf16 autocast, fp32 master weights",
            ha="center", fontsize=7.8, color="#34495e", linespacing=1.4)

    # zoom lines from the ×12 box to the detail panel
    for yb, yp in ((b_blk[1] + b_blk[3] / 2, 13.6), (b_blk[1] - b_blk[3] / 2, 4.05)):
        ax.plot([L + W / 2, 5.35], [yb, yp], color="#9aa5b1", lw=0.9, ls="--")

    ax.text(5, 2.05, "120,048,384 parameters = 35,094,528 (tied embedding) + 12 × 7,079,424 (blocks) + 768 (final norm)  ·  canvas 512 tokens  ·  vocabulary 45,591 (padded to 45,696)",
            ha="center", fontsize=7.8, color="#34495e")
    fig.savefig(OUT / "pilot120m_architecture.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def results():
    rows = [json.loads(l) for l in open(RUN / "metrics.jsonl")]
    judge = [json.loads(l) for l in open(RUN / "judge.jsonl")]
    cfg = json.load(open(RUN / "config.json"))["train"]
    tr = [r for r in rows if "loss" in r]
    ev = [r for r in rows if "val_nelbo" in r]
    sm = [r for r in rows if "sample/known_word_share" in r]
    REAL_PPL, SHUF_PPL, REAL_KNOWN = 16.9, 64.9, 0.887           # judge on real / word-shuffled text; real-word share
    plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3, "axes.spines.top": False, "axes.spines.right": False})

    def lr_at(step):
        lr, wu, total, m = cfg["lr"], cfg["warmup_steps"], cfg["total_steps"], cfg["min_lr_ratio"]
        if step < wu: return lr * (step + 1) / wu
        frac = min(1.0, (step - wu) / max(1, total - wu))
        return lr * (m + (1 - m) * 0.5 * (1 + math.cos(math.pi * frac)))

    # 1. losses
    fig, ax = plt.subplots(figsize=(8, 4.2))
    win = 25
    xs = [r["step"] for r in tr]; ys = [r["loss"] for r in tr]
    sm_y = [sum(ys[max(0, i - win + 1): i + 1]) / len(ys[max(0, i - win + 1): i + 1]) for i in range(len(ys))]
    ax.plot(xs, sm_y, color="#9aa5b1", lw=1, label="train loss (moving avg of 25 logs = 500 steps)")
    ax.plot([r["step"] for r in ev], [r["val_nelbo"] for r in ev], color="#1f4e79", lw=2, label="validation NELBO (all sources)")
    for src, c in (("sangraha", "#c0504d"), ("indiccorp", "#4f8a3c"), ("wikipedia", "#e29f2d")):
        ax.plot([r["step"] for r in ev], [r[f"val_nelbo/{src}"] for r in ev], color=c, lw=1, ls="--", label=f"validation NELBO — {src}")
    ax.set_ylim(1.6, 3.2); ax.set_xlim(0, cfg["total_steps"])
    ax.set_xlabel("optimizer step (65,536 tokens each)"); ax.set_ylabel("nats per token (upper bound)")
    ax.set_title("pilot120m: training and validation loss")
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout(); fig.savefig(OUT / "pilot120m_loss.png", dpi=150); plt.close(fig)

    # 2. masked-token accuracy + CE by t
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8))
    for key, lab, c in (("masked_acc/15pct", "15% masked", "#1f4e79"), ("masked_acc/50pct", "50% masked", "#4f8a3c"), ("masked_acc/85pct", "85% masked", "#c0504d")):
        a1.plot([r["step"] for r in ev], [100 * r[key] for r in ev], color=c, lw=1.6, label=lab)
    a1.set_xlabel("step"); a1.set_ylabel("top-1 accuracy on masked tokens (%)"); a1.set_title("masked-token accuracy (validation)")
    a1.legend(fontsize=8); a1.set_xlim(0, cfg["total_steps"])
    bins = [k for k in ev[-1] if k.startswith("val_ce_by_t/")]
    bins = sorted(bins, key=lambda k: float(k.split("/")[1].split("-")[0]))
    for step, c in ((1000, "#c7d4e2"), (5000, "#8faacc"), (20000, "#4f7fb3"), (ev[-1]["step"], "#1f4e79")):
        r = next(x for x in ev if x["step"] == step)
        a2.plot([float(k.split("/")[1].split("-")[0]) + 0.05 for k in bins], [r[k] for k in bins], marker="o", ms=3, color=c, label=f"step {step:,}")
    a2.set_xlabel("mask rate t (bin centre)"); a2.set_ylabel("cross-entropy per masked token (nats)"); a2.set_title("difficulty by mask rate")
    a2.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "pilot120m_masked_accuracy.png", dpi=150); plt.close(fig)

    # 3. samples: judge gen-PPL + known-word share
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8))
    a1.plot([j["step"] for j in judge], [j["gen_ppl"] for j in judge], marker="o", color="#1f4e79", lw=1.6, label="samples (16 × 512 tokens)")
    a1.axhline(REAL_PPL, color="#4f8a3c", ls="--", lw=1, label=f"real Telugu ({REAL_PPL})")
    a1.axhline(SHUF_PPL, color="#c0504d", ls="--", lw=1, label=f"real, words shuffled ({SHUF_PPL})")
    a1.set_xlabel("step"); a1.set_ylabel("perplexity under gemma-3-1b-pt"); a1.set_title("generative perplexity (lower is better)")
    a1.set_ylim(0, 135); a1.set_xlim(0, cfg["total_steps"]); a1.legend(fontsize=8)
    a2.plot([r["step"] for r in sm], [100 * r["sample/known_word_share"] for r in sm], marker="o", color="#1f4e79", lw=1.6, label="samples")
    a2.axhline(100 * REAL_KNOWN, color="#4f8a3c", ls="--", lw=1, label=f"real Telugu ({100 * REAL_KNOWN:.1f}%)")
    a2.set_xlabel("step"); a2.set_ylabel("words attested in validation text (%)"); a2.set_title("real-word share of samples")
    a2.set_ylim(50, 100); a2.set_xlim(0, cfg["total_steps"]); a2.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "pilot120m_samples.png", dpi=150); plt.close(fig)

    # 4. schedule + grad norm
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.4))
    steps = list(range(0, cfg["total_steps"] + 1, 100))
    a1.plot(steps, [lr_at(s) * 1e4 for s in steps], color="#9aa5b1", lw=1.5, label="planned")
    done = [s for s in steps if s <= tr[-1]["step"]]
    a1.plot(done, [lr_at(s) * 1e4 for s in done], color="#1f4e79", lw=2, label=f"done (to step {tr[-1]['step']:,})")
    a1.set_xlabel("step"); a1.set_ylabel("learning rate (×1e-4)"); a1.set_title("learning-rate schedule"); a1.legend(fontsize=8)
    g = [r["grad_norm"] for r in tr]
    gs = [sum(g[max(0, i - win + 1): i + 1]) / len(g[max(0, i - win + 1): i + 1]) for i in range(len(g))]
    a2.plot(xs, g, color="#c7d4e2", lw=0.6, label="logged every 20 steps")
    a2.plot(xs, gs, color="#1f4e79", lw=1.4, label="moving average (500 steps)")
    a2.axhline(cfg["grad_clip"], color="#c0504d", ls="--", lw=1, label="clip threshold (1.0)")
    a2.set_yscale("log"); a2.set_xlabel("step"); a2.set_ylabel("global gradient norm (pre-clip)"); a2.set_title("gradient norm"); a2.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(OUT / "pilot120m_schedule_gradnorm.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    architecture()
    results()
    print(f"figures written to {OUT}")
