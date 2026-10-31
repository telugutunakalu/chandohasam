"""Training-curve figures: the MDLMs' E6 fine-tuning against Nandi's meaning → poem fine-tuning.

    ../.venv/bin/python plot_curves.py

Reads the runs' metrics.jsonl (../diffusion_finetuning/runs/e6-*, runs/nandi-t1*) and results/exposure_probe.json, and
writes SVG figures with svgplot.py (standard library only: matplotlib could not be installed):
- comparison figures (fig1–fig5) to plots/ here and to ../diffusion_finetuning/plots/;
- the MDLMs' own figures (per-task losses and validation of E6) to ../diffusion_finetuning/plots/;
- Nandi's own figures (its sweep, train against val) to plots/ here.
Each plots/ folder gets a README.md listing its figures. Numbers only: no generated text.

x axis of the comparisons: passes over the meaning → poem (T1) pool of 300,763 poems. E6 stage 2 draws 64 T1 examples
per step (half of each 128-example batch, 11,748 steps = 2.5 passes); the MDLMs' T1 phase and Nandi draw 128.
Levels: the MDLM's loss is a NELBO (an upper bound on its NLL), Nandi's an exact NLL, both per MDLM target token;
compare the shapes and gaps, not the levels.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from svgplot import subplots

HERE = Path(__file__).resolve().parent
DF = HERE.parent / "diffusion_finetuning"
T1_POOL = 300_763
OUT_AR, OUT_DF = HERE / "plots", DF / "plots"
COLORS = {"120m": "#1f77b4", "523m": "#d62728", "nandi": "#2ca02c"}
LABELS = {"120m": "MDLM 120M (E6 + T1 phase)", "523m": "MDLM 523M (E6 + T1 phase)", "nandi": "Nandi-Mini-150M (AR)"}
NOTE = "MDLM: NELBO (upper bound); Nandi: exact NLL. Compare shapes, not levels."
written: dict[Path, list[tuple[str, str]]] = {OUT_AR: [], OUT_DF: []}


def rows(path: Path) -> list[dict]:
    return [json.loads(l) for l in open(path, encoding="utf-8")] if path.exists() else []


def series(rs: list[dict], key: str, x_of) -> tuple[np.ndarray, np.ndarray]:
    pts = [(x_of(r["step"]), r[key]) for r in rs if key in r]
    return (np.array([p[0] for p in pts]), np.array([p[1] for p in pts])) if pts else (np.array([]), np.array([]))


def smooth(y: np.ndarray, k: int) -> np.ndarray:
    if len(y) < k:
        return y
    return np.convolve(y, np.ones(k) / k, mode="valid")


def mdlm_curve(tag: str, key: str):
    """(x in T1 passes, y) over E6 stage 2 then the T1 phase."""
    s2 = rows(DF / "runs" / f"e6-s2-{tag}" / "metrics.jsonl")
    t1 = rows(DF / "runs" / f"e6-t1-{tag}" / "metrics.jsonl")
    x1, y1 = series(s2, key, lambda s: s * 64 / T1_POOL)
    x2, y2 = series([r for r in t1 if r["step"] > 0], key, lambda s: 11748 * 64 / T1_POOL + s * 128 / T1_POOL)
    return np.concatenate([x1, x2]), np.concatenate([y1, y2])


def nandi_curve(key: str, run: str = "nandi-t1"):
    return series(rows(HERE / "runs" / run / "metrics.jsonl"), key, lambda s: s * 128 / T1_POOL)


def save(fig, name: str, folders, caption: str) -> None:
    for d in folders:
        d.mkdir(parents=True, exist_ok=True)
        fig.save(d / f"{name}.svg")
        written[d].append((name, caption))


BOTH = (OUT_AR, OUT_DF)


def fig1_val() -> None:
    fig, axes = subplots(1, 2, size=(1200, 430))
    for ax, key, title in ((axes[0], "T1", "poem | metre + meaning (T1)"), (axes[1], "T0", "poem | metre only (T0)")):
        for tag in ("120m", "523m"):
            x, y = mdlm_curve(tag, f"val_nelbo/{key}")
            ax.plot(x, y, color=COLORS[tag], label=LABELS[tag])
        x, y = nandi_curve(f"val_nll/{key}")
        ax.plot(x, y, color=COLORS["nandi"], label=LABELS["nandi"])
        if len(y):
            i = int(np.argmin(y))
            ax.plot([x[i]], [y[i]], color=COLORS["nandi"], marker="o", ms=4, line=False)
            ax.annotate(f"min {y[i]:.3f}", (x[i], y[i]), offset=(5, -14), color=COLORS["nandi"], size=9)
        ax.axvline(11748 * 64 / T1_POOL, color="grey", ls=":", lw=1)
        ax.set_title(f"held-out val: {title}")
        ax.set_xlabel("passes over the meaning → poem pool")
        ax.set_ylabel("nats per MDLM target token")
        ax.grid()
    axes[0].legend()
    fig.suptitle("Validation loss during fine-tuning (dotted: the MDLMs' T1 phase starts)")
    fig.text(NOTE)
    save(fig, "fig1_val_loss_vs_passes", BOTH,
         "Val loss (T1, T0) against passes over the meaning → poem pool, the three models. The MDLMs improve to the "
         "end; Nandi reaches its minimum near 1.9 passes and then rises (overfitting).")


def fig2_gap() -> None:
    fig, ax = subplots(1, 1, size=(680, 430))
    for tag in ("120m", "523m"):
        x1, y1 = mdlm_curve(tag, "val_nelbo/T1")
        x0, y0 = mdlm_curve(tag, "val_nelbo/T0")
        n = min(len(y0), len(y1))
        ax.plot(x1[:n], y0[:n] - y1[:n], color=COLORS[tag], label=LABELS[tag])
    x1, y1 = nandi_curve("val_nll/T1")
    x0, y0 = nandi_curve("val_nll/T0")
    n = min(len(y0), len(y1))
    ax.plot(x1[:n], y0[:n] - y1[:n], color=COLORS["nandi"], label=LABELS["nandi"])
    ax.set_xlabel("passes over the meaning → poem pool")
    ax.set_ylabel("T0 − T1 (nats per MDLM target token)")
    ax.set_title("How much the model uses the meaning (val)")
    ax.grid()
    ax.legend()
    save(fig, "fig2_meaning_gap", BOTH,
         "The meaning's value: val loss without the meaning minus with it, against passes. Larger = the poem "
         "depends more on the bhāvam.")


def fig3_train_val() -> None:
    fig, axes = subplots(1, 3, size=(1500, 430))
    for ax, tag in zip(axes[:2], ("120m", "523m")):
        x, y = mdlm_curve(tag, "loss/T1")
        k = 25
        ax.plot(x[k - 1:], smooth(y, k), color=COLORS[tag], alpha=0.6, label="train (T1 task, smoothed)")
        x, y = mdlm_curve(tag, "val_nelbo/T1")
        ax.plot(x, y, color=COLORS[tag], lw=2, label="val T1")
        ax.set_title(f"{LABELS[tag]}: NELBO per target token")
    x, y = nandi_curve("loss")
    k = 25
    axes[2].plot(x[k - 1:], smooth(y, k), color=COLORS["nandi"], alpha=0.6, label="train (smoothed)")
    x, y = nandi_curve("val_nll_tok/T1")
    axes[2].plot(x, y, color=COLORS["nandi"], lw=2, label="val T1")
    axes[2].set_title(f"{LABELS['nandi']}: NLL per Nandi token")
    for ax in axes:
        ax.set_xlabel("passes over the meaning → poem pool")
        ax.grid()
        ax.legend()
    fig.suptitle("Training against validation loss, per model (each panel in its own unit)")
    save(fig, "fig3_train_vs_val", BOTH,
         "Training loss (smoothed) and val loss of the meaning → poem task, per model. Nandi's training loss pulls "
         "away from its val loss in the second pass; the MDLMs' does not.")


def sweep_points(family: str) -> list[tuple[float, float]]:
    out = []
    if family == "nandi":
        for d in sorted(d for d in (HERE / "runs").glob("nandi-t1-lr*") if d.is_dir()):
            v = [r["val_nll/T1"] for r in rows(d / "metrics.jsonl") if "val_nll/T1" in r]
            if v:
                out.append((float(d.name.split("lr")[-1]), v[-1]))
    else:
        for d in sorted(d for d in (DF / "runs").glob(f"e6-s2-{family}-lr*") if d.is_dir()):
            v = [r["val_nelbo/T1"] for r in rows(d / "metrics.jsonl") if "val_nelbo/T1" in r]
            if v:
                out.append((float(d.name.split("lr")[-1]), v[-1]))
    return sorted(out)


def fig4_sweeps() -> None:
    fig, axes = subplots(1, 2, size=(1200, 430))
    for fam in ("120m", "523m", "nandi"):
        p = sweep_points(fam)
        if p:
            axes[0].plot([a for a, _ in p], [b for _, b in p], color=COLORS[fam], marker="o", ms=3.5,
                         label=LABELS[fam].split(" (")[0])
            j = int(np.argmin([b for _, b in p]))
            axes[0].plot([p[j][0]], [p[j][1]], color=COLORS[fam], marker="*", ms=5, line=False)
    axes[0].set_xscale("log")
    axes[0].set_xlabel("learning rate")
    axes[0].set_ylabel("val T1 after 1 epoch (nats per MDLM token)")
    axes[0].set_title("Learning-rate sweeps (★ chosen)")
    axes[0].grid()
    axes[0].legend()
    shades = ("#a1d99b", "#74c476", "#31a354", "#006d2c", "#00441b")
    runs = sorted((d for d in (HERE / "runs").glob("nandi-t1-lr*") if d.is_dir()), key=lambda d: float(d.name.split("lr")[-1]))
    for d, c in zip(runs, shades):
        x, y = series(rows(d / "metrics.jsonl"), "val_nll/T1", lambda s: s)
        axes[1].plot(x, y, color=c, label=f"lr {d.name.split('lr')[-1]}")
    axes[1].set_xlabel("step (1 epoch = 2,350)")
    axes[1].set_ylabel("val T1 (nats per MDLM token)")
    axes[1].set_title("Nandi's sweep runs")
    axes[1].grid()
    axes[1].legend()
    fig.text("MDLM sweeps: 1 epoch of E6 stage 2 (six tasks); Nandi: 1 epoch of meaning → poem. "
             "Each family's best rate was the highest tried.")
    save(fig, "fig4_lr_sweeps", BOTH, "The learning-rate sweeps of the three models, and Nandi's sweep curves.")


def fig5_memorisation() -> None:
    p = HERE / "results" / "exposure_probe.json"
    if not p.exists():
        print("results/exposure_probe.json missing: fig5 skipped")
        return
    pts = json.loads(p.read_text(encoding="utf-8"))["points"]
    fig, axes = subplots(1, 3, size=(1600, 450))
    for fam, key in (("120m", "mdlm-120m"), ("523m", "mdlm-523m"), ("nandi", "nandi")):
        q = sorted((r for r in pts if r["model"] == key), key=lambda r: r["passes"])
        if not q:
            continue
        x = [r["passes"] for r in q]
        axes[0].plot(x, [r["T1_val"] for r in q], color=COLORS[fam], marker="o", ms=2.5,
                     label=f"{LABELS[fam].split(' (')[0]} val")
        axes[0].plot(x, [r["T1_train"] for r in q], color=COLORS[fam], marker="o", ms=2.5, ls="--", alpha=0.7,
                     label=f"{LABELS[fam].split(' (')[0]} train")
        axes[1].plot(x, [r["gap"] for r in q], color=COLORS[fam], marker="o", ms=2.5, label=LABELS[fam].split(" (")[0])
    q = sorted((r for r in pts if r["model"] == "nandi"), key=lambda r: r["passes"])
    if q:
        x = [r["passes"] for r in q]
        axes[2].plot(x, [r["unseen_nll_tok"] for r in q], color=COLORS["nandi"], marker="o", ms=2.5, label="never drawn yet")
        axes[2].plot(x, [r["seen_nll_tok"] for r in q], color=COLORS["nandi"], marker="o", ms=2.5, ls="--",
                     label="drawn ≥ 1 time")
    axes[0].set_title("T1 loss: training poems vs held-out val")
    axes[0].set_ylabel("nats per MDLM target token")
    axes[1].set_title("Generalisation gap (val − train)")
    axes[1].set_ylabel("nats per MDLM target token")
    axes[2].set_title("Nandi: seen vs never-seen training poems (metre-matched)")
    axes[2].set_ylabel("nats per Nandi token")
    for ax in axes:
        ax.set_xlabel("passes over the meaning → poem pool")
        ax.grid()
        ax.legend()
    fig.text("Same 900 training and val records for every model (exposure_probe.py). The MDLMs' stage 1 had shown "
             "every training poem 3 times, so no poem is unseen for them. " + NOTE)
    save(fig, "fig5_memorisation", BOTH,
         "Memorisation over training: T1 loss on training vs val poems at every snapshot, the gap, and (Nandi) seen "
         "vs never-seen training poems.")


def mdlm_own(tag: str) -> None:
    s2 = rows(DF / "runs" / f"e6-s2-{tag}" / "metrics.jsonl")
    fig, axes = subplots(1, 2, size=(1200, 430))
    palette = dict(zip(("T1", "T0", "T2", "T3", "T4", "T5"),
                       ("#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd", "#8c564b", "#d62728")))
    for task in ("T1", "T0", "T2", "T3", "T4", "T5"):
        x, y = series(s2, f"loss/{task}", lambda s: s)
        if len(y):
            axes[0].plot(x[24:], smooth(y, 25), color=palette[task], label=task)
    for task in ("T1", "T0", "T2"):
        x, y = series(s2, f"val_nelbo/{task}", lambda s: s)
        axes[1].plot(x, y, color=palette[task], label=task)
    axes[0].set_title(f"MDLM {tag.upper()} E6 stage 2: training loss per task (smoothed)")
    axes[1].set_title(f"MDLM {tag.upper()} E6 stage 2: val NELBO per task")
    for ax in axes:
        ax.set_xlabel("step (11,748 = 2.5 passes over the T1 pool)")
        ax.set_ylabel("NELBO per target token")
        ax.grid()
        ax.legend()
    save(fig, f"e6_tasks_{tag}", (OUT_DF,), f"E6 stage 2 of the {tag.upper()}: training loss per task and val NELBO "
         f"of T1 (metre + meaning → poem), T0 (metre → poem), T2 (poem → meaning).")


def nandi_own() -> None:
    fig, ax = subplots(1, 1, size=(720, 430))
    x, y = nandi_curve("loss")
    ax.plot(x[24:], smooth(y, 25), color=COLORS["nandi"], alpha=0.6, label="train (smoothed)")
    for key, ls in (("val_nll_tok/T1", "-"), ("val_nll_tok/T0", "--")):
        x, y = nandi_curve(key)
        ax.plot(x, y, ls=ls, color="black", label=key.split("/")[-1] + " val")
    ax.set_xlabel("passes over the meaning → poem pool (8,225 steps = 3.5)")
    ax.set_ylabel("NLL per Nandi token")
    ax.set_title("Nandi-Mini-150M final run (lr 1.35e-3)")
    ax.grid()
    ax.legend()
    save(fig, "nandi_final_run", (OUT_AR,), "Nandi's final run: training loss and val loss (T1, T0) per Nandi token.")


def readme(folder: Path) -> None:
    lines = ["# Plots", "", "Written by `autoregressive_finetuning/plot_curves.py` (SVG, via svgplot.py). Data: the runs' "
             "`metrics.jsonl` and `autoregressive_finetuning/results/exposure_probe.json`.", ""]
    lines += [f"- `{n}.svg`: {c}" for n, c in written[folder]]
    (folder / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    fig1_val()
    fig2_gap()
    fig3_train_val()
    fig4_sweeps()
    fig5_memorisation()
    for tag in ("120m", "523m"):
        mdlm_own(tag)
    nandi_own()
    for d in BOTH:
        readme(d)
        print(f"{d}: {len(written[d])} figures")


if __name__ == "__main__":
    main()
