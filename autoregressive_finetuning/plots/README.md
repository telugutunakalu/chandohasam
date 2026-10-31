# Plots

Written by `autoregressive_finetuning/plot_curves.py` (SVG, via svgplot.py). Data: the runs' `metrics.jsonl` and `autoregressive_finetuning/results/exposure_probe.json`.

- `fig1_val_loss_vs_passes.svg`: Val loss (T1, T0) against passes over the meaning → poem pool, the three models. The MDLMs improve to the end; Nandi reaches its minimum near 1.9 passes and then rises (overfitting).
- `fig2_meaning_gap.svg`: The meaning's value: val loss without the meaning minus with it, against passes. Larger = the poem depends more on the bhāvam.
- `fig3_train_vs_val.svg`: Training loss (smoothed) and val loss of the meaning → poem task, per model. Nandi's training loss pulls away from its val loss in the second pass; the MDLMs' does not.
- `fig4_lr_sweeps.svg`: The learning-rate sweeps of the three models, and Nandi's sweep curves.
- `fig5_memorisation.svg`: Memorisation over training: T1 loss on training vs val poems at every snapshot, the gap, and (Nandi) seen vs never-seen training poems.
- `nandi_final_run.svg`: Nandi's final run: training loss and val loss (T1, T0) per Nandi token.
