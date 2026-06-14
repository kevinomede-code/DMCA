"""
Regenerate the accuracy-vs-latency scatter (Fig. 3 of the thesis) with all 8
benchmarked models.

Sources:
- Deterministic raw-input models (PatchTST, MOMENT-L, TimesFM): canonical
  benchmark results/benchmarks/2026-04-07/benchmark_results_modal.csv
- Probabilistic / non-comparable-unit models (Lag-Llama, Moirai-S/L,
  Chronos-T/L): completion run results/benchmarks/2026-04-27/
  benchmark_mae_completion.csv (CMAPSS only, see MERGE_NOTES.md §2 for the
  comparability caveats)

Output:
- results/figures/accuracy_latency_scatter.png
- results/figures/accuracy_latency_scatter.pdf
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "results/benchmarks/2026-04-07/benchmark_results_modal.csv"
COMPLETION = ROOT / "results/benchmarks/2026-04-27/benchmark_mae_completion.csv"
OUT_DIR = ROOT / "results/figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Load and filter to CMAPSS rows
# ---------------------------------------------------------------------------
DATASET = "LucasThil/nasa_turbofan_degradation_FD001"

df_can = pd.read_csv(CANONICAL)
df_cmp = pd.read_csv(COMPLETION)

df_can = df_can[df_can["dataset_name"] == DATASET].copy()
df_cmp = df_cmp[df_cmp["dataset_name"] == DATASET].copy()

# Models with deterministic raw-input MAE/RMSE in the canonical run
DETERMINISTIC = {
    "ibm/patchtst-base-etth1": "PatchTST",
    "AutonLab/MOMENT-1-large": "MOMENT-L",
    "google/timesfm-1.0-200m": "TimesFM",
}
# Models populated by the 2026-04-27 completion run (probabilistic / rescaled)
PROBABILISTIC = {
    "time-series-foundation-models/Lag-Llama": "Lag-Llama",
    "Salesforce/moirai-1.1-R-small": "Moirai-S",
    "Salesforce/moirai-1.1-R-large": "Moirai-L",
    "amazon/chronos-t5-tiny": "Chronos-T",
    "amazon/chronos-t5-large": "Chronos-L",
}

records = []
for mid, label in DETERMINISTIC.items():
    row = df_can[df_can["model_id"] == mid].iloc[0]
    records.append(
        dict(
            label=label,
            latency=float(row["latency_mean_ms"]),
            mae=float(row["mae"]),
            ram=float(row["ram_gpu_mb"]),
            family="deterministic",
        )
    )
for mid, label in PROBABILISTIC.items():
    row = df_cmp[df_cmp["model_id"] == mid].iloc[0]
    # use canonical latency / RAM (those are the reference values)
    can_row = df_can[df_can["model_id"] == mid].iloc[0]
    records.append(
        dict(
            label=label,
            latency=float(can_row["latency_mean_ms"]),
            mae=float(row["mae"]),
            ram=float(can_row["ram_gpu_mb"]),
            family="probabilistic",
        )
    )

data = pd.DataFrame(records)
print(data.to_string(index=False))

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

fig, ax = plt.subplots(figsize=(8.6, 6.4))

# Colour by latency cluster (consistent with Fig. 1 / latency_comparison)
def cluster_color(lat_ms):
    if lat_ms < 10:
        return "#2ca02c"   # green
    if lat_ms < 100:
        return "#1f77b4"   # blue
    if lat_ms < 500:
        return "#ff7f0e"   # orange
    return "#d62728"        # red

# Bubble size proportional to RAM (clipped — keeps MOMENT-L from swallowing
# its neighbours)
def bubble_size(ram_mb):
    return float(np.clip(40 + ram_mb * 0.08, 50, 320))

# SLA-compliant zone (latency < 50 ms)
ax.axvspan(0, 50, color="#d6f5d6", alpha=0.55, zorder=0)
ax.axvline(50, color="#d62728", linestyle="--", linewidth=1.3, zorder=1)

for _, r in data.iterrows():
    color = cluster_color(r.latency)
    size = bubble_size(r.ram)
    if r.family == "deterministic":
        ax.scatter(
            r.latency,
            r.mae,
            s=size,
            color=color,
            edgecolor="black",
            linewidth=1.0,
            marker="o",
            zorder=3,
            label="_nolegend_",
        )
    else:
        ax.scatter(
            r.latency,
            r.mae,
            s=size,
            facecolor="white",
            edgecolor=color,
            linewidth=2.0,
            marker="s",
            zorder=3,
            label="_nolegend_",
        )

# Annotate each point
ANNOT = {
    # label: (dx, dy, ha, va) in points
    "PatchTST":    (12,   0, "left",  "center"),
    "MOMENT-L":    (-12, -18, "right", "top"),
    "TimesFM":     (-14,  0, "right", "center"),
    "Lag-Llama":   (12,  -8, "left",  "top"),
    "Moirai-S":    (-12,  12, "right", "bottom"),
    "Moirai-L":    (14,   12, "left",  "bottom"),
    "Chronos-T":   (-14, 14, "right", "bottom"),
    "Chronos-L":   (-14, 14, "right", "bottom"),
}
DAGGER = {"Lag-Llama", "Moirai-S", "Moirai-L"}
DOUBLE = {"Chronos-T", "Chronos-L"}

for _, r in data.iterrows():
    suffix = ""
    if r.label in DAGGER:
        suffix = "$^{\\dagger}$"
    elif r.label in DOUBLE:
        suffix = "$^{\\dagger\\ddagger}$"
    dx, dy, ha, va = ANNOT[r.label]
    ax.annotate(
        f"{r.label}{suffix}",
        xy=(r.latency, r.mae),
        xytext=(dx, dy),
        textcoords="offset points",
        ha=ha,
        va=va,
        fontsize=10,
        fontweight="bold",
    )

# Axes
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, 5000)
ax.set_ylim(5e-4, 5)
ax.set_xlabel("Inference latency (ms, log scale)")
ax.set_ylabel("MAE on CMAPSS, log scale  (lower is better)")
ax.grid(True, which="both", linestyle=":", linewidth=0.5, color="0.7", zorder=0)

# SLA zone label
ax.text(
    1.3, 2.0,
    "SLA compliant\n($<$50 ms)",
    color="#1a7c1a", fontsize=9, fontweight="bold",
    va="top", ha="left",
)
ax.text(
    55, 2.0,
    "SLA 50 ms",
    color="#a01a1a", fontsize=9, rotation=0, va="top", ha="left",
)

# Legend (markers + clusters + caveat)
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], marker="o", color="w", label="Deterministic (raw-input MAE)",
           markerfacecolor="#888", markeredgecolor="black", markersize=10),
    Line2D([0], [0], marker="s", color="w",
           label="Probabilistic / rescaled output (not directly comparable)",
           markerfacecolor="white", markeredgecolor="#888", markeredgewidth=2,
           markersize=10),
]
leg = ax.legend(
    handles=legend_handles,
    loc="upper right",
    fontsize=9,
    frameon=True,
    framealpha=0.95,
    title="Model output family",
    title_fontsize=9,
)

ax.set_title(
    "Accuracy vs. latency on CMAPSS -- all 8 benchmarked models\n"
    "(bubble size $\\propto$ GPU RAM; canonical 2026-04-07 + completion 2026-04-27)",
    fontsize=11,
)

# Caveat box as a footer (figtext, not inside axes -> no overlap with points)
caveat = (
    r"$^{\dagger}$ Native output unit (Moirai: input normalised to $[0,1]$; "
    r"Lag-Llama: 1-step sliding-window backbone, not GluonTS predictor)." + "\n"
    r"$^{\ddagger}$ Chronos MAE is in its internal rescaled token-space "
    r"($\sim\!10^{-3}$): NOT directly comparable to raw-signal MAE of PatchTST/MOMENT/TimesFM."
)

plt.tight_layout(rect=(0, 0.10, 1, 1))
fig.text(
    0.02, 0.01, caveat,
    ha="left", va="bottom",
    fontsize=8, color="#333",
    bbox=dict(facecolor="#fffbe6", edgecolor="#cccc88",
              boxstyle="round,pad=0.4"),
)

png_path = OUT_DIR / "accuracy_latency_scatter.png"
pdf_path = OUT_DIR / "accuracy_latency_scatter.pdf"
plt.savefig(png_path, dpi=200, bbox_inches="tight")
plt.savefig(pdf_path, bbox_inches="tight")
print(f"Saved: {png_path}")
print(f"Saved: {pdf_path}")
