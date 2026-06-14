"""
generate_benchmark_heatmap.py
Genera figures/benchmark_heatmap.pdf dal CSV canonico.
Esegui: python3 pipeline/generate_benchmark_heatmap.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, LogNorm

# ── Dati dal CSV canonico (2026-04-07) ───────────────────────────────────────
MODELS = [
    ("Moirai-S",       11.6,   53.7,  57.9,  np.nan, np.nan),
    ("Moirai-L",      305.1,   72.6,  65.1,  np.nan, np.nan),
    ("Chronos-tiny",    8.4,  166.8, 154.0,  np.nan, np.nan),
    ("Chronos-large", 709.0,  830.0, 736.3,  np.nan, np.nan),
    ("TimesFM†",      200.0, 2039.1,1907.3,  0.006,  1.817),   # SLA-excluded
    ("PatchTST",        0.7,    5.9,   3.0,  1.303,  7.172),
    ("MOMENT",        341.3,   29.7,  26.8,  0.114,  1.710),
    ("Lag-Llama",       2.5,    7.8,   7.0,  np.nan, np.nan),
]

DATASETS  = ["CMAPSS FD001", "ETT-h1"]
SLA_MS    = 150.0   # SLA × 1.5 threshold (100 ms × 1.5)
SLA_ROW   = 4       # index of TimesFM in MODELS list (0-based)

model_names = [m[0] for m in MODELS]
params_m    = [m[1] for m in MODELS]
lat  = np.array([[m[2], m[3]] for m in MODELS], dtype=float)
mae  = np.array([[m[4], m[5]] for m in MODELS], dtype=float)

# ── Colormaps ─────────────────────────────────────────────────────────────────
cmap_mae = LinearSegmentedColormap.from_list(
    "mae", ["#deedf7", "#1565a0"])
cmap_mae.set_bad("#e0e0e0")   # NaN → light gray

cmap_lat = LinearSegmentedColormap.from_list(
    "lat", ["#e8f5e9", "#b71c1c"])

# ── Figure layout ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.2),
                         gridspec_kw={"width_ratios": [1, 1], "wspace": 0.08})
fig.patch.set_facecolor("white")

# ────────────────────────────────── Panel 1: MAE ──────────────────────────────
ax = axes[0]
mae_masked = np.ma.masked_invalid(mae)

im1 = ax.imshow(mae_masked, cmap=cmap_mae, aspect="auto",
                vmin=0.0, vmax=8.0)

for i, row in enumerate(mae):
    for j, val in enumerate(row):
        if np.isnan(val):
            ax.text(j, i, "—", ha="center", va="center",
                    fontsize=9, color="#999999", fontstyle="italic")
        else:
            clr = "white" if val < 4.0 else "#1a1a1a"
            ax.text(j, i, f"{val:.3f}", ha="center", va="center",
                    fontsize=9.5, fontweight="bold", color=clr)

ax.set_xticks(range(2)); ax.set_xticklabels(DATASETS, fontsize=9)
ax.set_yticks(range(len(MODELS)))
ylabels = [f"{n}  ({p:.0f} M)" for n, p in zip(model_names, params_m)]
ax.set_yticklabels(ylabels, fontsize=8)
ax.set_title("MAE   (↓ better)", fontsize=10, fontweight="bold", pad=9)
ax.tick_params(length=0)

# SLA-excluded row frame
for j in range(2):
    ax.add_patch(mpatches.FancyBboxPatch(
        (j - 0.48, SLA_ROW - 0.48), 0.96, 0.96,
        boxstyle="round,pad=0.02", linewidth=1.6,
        edgecolor="#cc2200", fill=False, linestyle="--", zorder=3))

# Horizontal separators
for i in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]:
    ax.axhline(i, color="white", linewidth=0.8)

cb1 = fig.colorbar(im1, ax=ax, fraction=0.046, pad=0.03)
cb1.ax.tick_params(labelsize=7)

# ────────────────────────────────── Panel 2: Latency ─────────────────────────
ax2 = axes[1]

im2 = ax2.imshow(lat, cmap=cmap_lat, aspect="auto",
                 norm=LogNorm(vmin=3.0, vmax=2500.0))

for i, row in enumerate(lat):
    for j, val in enumerate(row):
        clr = "white" if val > 250 else "#1a1a1a"
        txt = f"{val/1000:.1f} s" if val >= 1000 else f"{val:.0f} ms"
        ax2.text(j, i, txt, ha="center", va="center",
                 fontsize=9.5, fontweight="bold", color=clr)

ax2.set_xticks(range(2)); ax2.set_xticklabels(DATASETS, fontsize=9)
ax2.set_yticks(range(len(MODELS))); ax2.set_yticklabels([], fontsize=8)
ax2.set_title("Latency P95   (↓ better)", fontsize=10, fontweight="bold", pad=9)
ax2.tick_params(length=0)

# SLA threshold line
ax2.axhline(SLA_ROW - 0.5, color="#cc2200", linewidth=1.2,
            linestyle=":", alpha=0.85)
ax2.text(1.49, SLA_ROW - 0.52, "SLA×1.5", fontsize=7,
         color="#cc2200", ha="right", va="bottom")

for j in range(2):
    ax2.add_patch(mpatches.FancyBboxPatch(
        (j - 0.48, SLA_ROW - 0.48), 0.96, 0.96,
        boxstyle="round,pad=0.02", linewidth=1.6,
        edgecolor="#cc2200", fill=False, linestyle="--", zorder=3))

for i in [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]:
    ax2.axhline(i, color="white", linewidth=0.8)

cb2 = fig.colorbar(im2, ax=ax2, fraction=0.046, pad=0.03)
cb2.ax.tick_params(labelsize=7)

# ── Footer note ───────────────────────────────────────────────────────────────
fig.text(0.5, -0.03,
         "† TimesFM P95 > SLA×1.5 → excluded from TOPSIS admissibility filter."
         "   Gray (—) = MAE not available (zero-shot / probabilistic output)."
         "   GPU T4 · 20 runs · seed 42.",
         ha="center", fontsize=7, color="#555555", style="italic")

# ── Save ──────────────────────────────────────────────────────────────────────
out_pdf = "benchmark_heatmap.pdf"
out_png = "benchmark_heatmap.png"
plt.savefig(out_pdf, bbox_inches="tight", dpi=150, facecolor="white")
plt.savefig(out_png, bbox_inches="tight", dpi=150, facecolor="white")
print(f"Saved → {out_pdf}")
print(f"Saved → {out_png}")
