"""Charts for the word-resolution report (static PNG/SVG, validated reference palette, one axis per panel)."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
OUT = os.path.dirname(os.path.abspath(__file__))   # this folder
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                 "axes.spines.top": False, "axes.spines.right": False, "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})
def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=170, bbox_inches="tight"); fig.savefig(f"{OUT}/{name}.svg", bbox_inches="tight"); plt.close(fig)

# 1. class shares (v28), grouped by what they count as
classes = [("inflected", 33.53, "resolved"), ("split-all-known", 20.80, "resolved"), ("headword", 20.49, "resolved"), ("resolved-by-byt5", 10.08, "resolved"),
           ("annotated-all-known", 5.57, "resolved"), ("resolved-by-resolver", 0.22, "resolved"), ("split-parts-resolved", 0.10, "resolved"),
           ("split-parts-attested", 2.47, "attested"), ("fragment+known", 1.22, "gloss"), ("attested-in-text", 0.81, "attested"), ("split-attested+gloss", 0.75, "gloss"),
           ("joined-with-context", 0.23, "gloss"), ("resolved-by-gloss", 0.01, "gloss"), ("partial", 2.29, "open"), ("unresolved", 1.26, "open"), ("resolver-guess", 0.16, "open")]
col = {"resolved": BLUE, "gloss": AQUA, "attested": YELLOW, "open": "#9a9a95"}
fig, ax = plt.subplots(figsize=(8.2, 5.6))
names = [c[0] for c in classes][::-1]; vals = [c[1] for c in classes][::-1]; cols = [col[c[2]] for c in classes][::-1]
bars = ax.barh(names, vals, color=cols, height=0.62)
for b, v in zip(bars, vals):
    ax.text(b.get_width() + 0.4, b.get_y() + b.get_height() / 2, f"{v:.2f}%" if v < 1 else f"{v:.1f}%", va="center", fontsize=8.5, color=INK2)
ax.set_xlabel("share of the 5,483,449 word occurrences (%)"); ax.set_xlim(0, 40); ax.grid(axis="x", color=GRID, linewidth=0.8); ax.set_axisbelow(True)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=BLUE, label="resolved to a headword (90.8%)"), Patch(color=AQUA, label="headword by weaker evidence (2.2%)"), Patch(color=YELLOW, label="attested form, no headword (3.3%)"), Patch(color="#9a9a95", label="open (3.7%)")], loc="lower right", frameon=False, fontsize=8.5)
ax.set_title("v28: occurrences by class", loc="left", color=INK, fontsize=11)
save(fig, "class_shares")

# 2. history: two panels, one axis each (no dual axis)
vers = ["v19", "v20", "v22", "v23", "v26", "v27", "v28"]
cov = [89.72, 90.37, 90.67, 90.71, 90.74, 90.75, 90.78]; att = [94.73, 94.98, 95.11, 95.12, 96.26, 96.26, 96.27]
prec = [0.677, 0.674, 0.677, 0.676, 0.678, 0.677, 0.678]
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
a1.plot(vers, cov, color=BLUE, linewidth=2, marker="o", markersize=5, label="resolved to a headword"); a1.plot(vers, att, color=AQUA, linewidth=2, marker="o", markersize=5, label="or attested")
a1.axhline(83.71, color="#9a9a95", linewidth=1.4, linestyle="--"); a1.text(0.02, 83.71 + 0.3, "symbolic baseline 83.7", color=INK2, fontsize=8.5)
a1.set_ylim(82, 98); a1.set_ylabel("% of occurrences"); a1.grid(axis="y", color=GRID); a1.set_axisbelow(True); a1.legend(frameon=False, fontsize=8.5, loc="center", bbox_to_anchor=(0.45, 0.55))
a1.text(len(vers) - 1, cov[-1] + 0.4, f"{cov[-1]:.1f}", ha="center", fontsize=8.5, color=INK2); a1.text(len(vers) - 1, att[-1] + 0.4, f"{att[-1]:.1f}", ha="center", fontsize=8.5, color=INK2)
a1.set_title("Coverage over the whole corpus", loc="left", color=INK, fontsize=11)
a2.plot(vers, prec, color=BLUE, linewidth=2, marker="o", markersize=5, label="pipeline"); a2.axhline(0.410, color="#9a9a95", linewidth=1.4, linestyle="--"); a2.text(0.02, 0.418, "symbolic baseline 0.410", color=INK2, fontsize=8.5)
a2.set_ylim(0.35, 0.75); a2.set_ylabel("precision on the fair held-out judged words"); a2.grid(axis="y", color=GRID); a2.set_axisbelow(True)
a2.text(len(vers) - 1, prec[-1] + 0.012, f"{prec[-1]:.3f}", ha="center", fontsize=8.5, color=INK2)
a2.set_title("Held-out precision (full-word rule, n=1,309)", loc="left", color=INK, fontsize=11)
fig.tight_layout(); save(fig, "history")

# 3. word shapes
fig, ax = plt.subplots(figsize=(7.2, 2.8))
shapes = [("single word (headword or inflected form)", 58.3), ("split, letters changed at a seam (sandhi)", 20.6), ("split, plain concatenation", 11.8), ("not resolved", 9.2)]
left = 0
for (lab, v), c in zip(shapes, [BLUE, ORANGE, AQUA, "#9a9a95"]):
    ax.barh([0], [v], left=left, color=c, height=0.5, edgecolor=SURF, linewidth=2)
    ax.text(left + v / 2, 0, f"{v:.1f}%", ha="center", va="center", color="white" if c != "#9a9a95" else INK, fontsize=9.5)
    left += v
ax.set_xlim(0, 100); ax.set_yticks([]); ax.set_xlabel("share of all occurrences (%)"); ax.spines["left"].set_visible(False)
ax.legend([plt.Rectangle((0, 0), 1, 1, color=c) for c in [BLUE, ORANGE, AQUA, "#9a9a95"]], [s[0] for s in shapes], loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=2, frameon=False, fontsize=8.5)
ax.set_title("What a resolved occurrence is (v28)", loc="left", color=INK, fontsize=11)
save(fig, "word_shapes")

# 4. per poem
fig, ax = plt.subplots(figsize=(7.2, 3.4))
cats = ["poems fully resolved", "poems at 90%+", "poems below 50%"]; res = [36.3, 62.1, 0.7]; attp = [67.0, 86.7, 0.4]
import numpy as np
x = np.arange(len(cats)); w = 0.36
b1 = ax.bar(x - w / 2, res, w, color=BLUE, label="resolved (macro mean 0.903, median 0.929)"); b2 = ax.bar(x + w / 2, attp, w, color=AQUA, label="attested (macro mean 0.960, median 1.000)")
for b in list(b1) + list(b2): ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1, f"{b.get_height():.1f}%", ha="center", fontsize=8.5, color=INK2)
ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_ylim(0, 100); ax.set_ylabel("% of 382,049 poems"); ax.grid(axis="y", color=GRID); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=8.5)
ax.set_title("Per poem (v28)", loc="left", color=INK, fontsize=11)
save(fig, "per_poem")

# 5. random sample by class (headword level)
fig, ax = plt.subplots(figsize=(7.2, 3.2))
cls = ["inflected (133)", "headword (75)", "resolved-by-byt5 (52)", "annotated-all-known (25)", "split-all-known (104)"]; pv = [0.79, 0.77, 0.67, 0.56, 0.53]
bars = ax.barh(cls[::-1], pv[::-1], color=BLUE, height=0.55)
for b, v in zip(bars, pv[::-1]): ax.text(v + 0.01, b.get_y() + b.get_height() / 2, f"{v:.2f}", va="center", fontsize=8.5, color=INK2)
ax.axvline(0.696, color="#9a9a95", linewidth=1.2, linestyle="--"); ax.text(0.70, 4.45, "all classes 0.696", fontsize=8.5, color=INK2)
ax.set_xlim(0, 1); ax.set_xlabel("headword-level precision on the random sample (judge's second reading; occurrences in brackets)"); ax.grid(axis="x", color=GRID); ax.set_axisbelow(True)
ax.set_title("Corpus-wide precision by class", loc="left", color=INK, fontsize=11)
save(fig, "sample_by_class")
print("charts written")
