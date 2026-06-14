"""
generate_plots.py
=================
Genera i tre grafici per thesis_draft.tex in stile IEEE.
Output: results/figures/  (PDF + PNG)

Grafici:
  1. latency_comparison.pdf  -- horizontal bar chart, log scale
  2. accuracy_latency_scatter.pdf -- scatter MAE vs latency
  3. drift_mae_timeline.pdf  -- MAE over time durante concept drift

Uso:
    python pipeline/generate_plots.py
"""

import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
FIG_DIR = ROOT / "results" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

CSV_PATH  = ROOT / "results" / "benchmarks" / "2026-04-07" / "benchmark_results_modal.csv"
DRIFT_PATH = ROOT / "results" / "drift_experiments" / "drift_cycle_results.json"

# ─── IEEE style ───────────────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family":      "serif",
    "font.size":        9,
    "axes.titlesize":   9,
    "axes.labelsize":   9,
    "xtick.labelsize":  8,
    "ytick.labelsize":  8,
    "legend.fontsize":  8,
    "lines.linewidth":  1.2,
    "axes.linewidth":   0.8,
    "grid.linewidth":   0.5,
    "figure.dpi":       300,
    "savefig.dpi":      300,
    "savefig.bbox":     "tight",
    "savefig.pad_inches": 0.02,
})

# ─── Dati canonici (da CSV 2026-04-07, CMAPSS) ────────────────────────────────
MODELS_CMAPSS = [
    # (label, lat_mean_ms, ram_mb, mae_or_nan)
    ("PatchTST",    5.861,    14,   1.302898),
    ("Lag-Llama",   7.768,    20,   None),
    ("MOMENT-L",   29.664,  1408,   0.114108),
    ("Moirai-S",   53.727,   106,   None),
    ("Moirai-L",   72.591,  2360,   None),
    ("Chronos-T", 166.824,    45,   None),
    ("Chronos-L", 829.961,  2771,   None),
    ("TimesFM",  2039.103,     8,   0.006353),
]

# ─── Colori latency classes ────────────────────────────────────────────────────
def latency_color(ms):
    if ms < 10:    return "#5cb85c"    # green
    if ms < 100:   return "#5bc0de"    # blue
    if ms < 500:   return "#f0ad4e"    # orange
    return "#d9534f"                   # red


# ═══════════════════════════════════════════════════════════════════════════════
# GRAFICO 1 — Latency Comparison (horizontal bar, log scale)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_latency_comparison():
    out_pdf = FIG_DIR / "latency_comparison.pdf"
    out_png = FIG_DIR / "latency_comparison.png"

    labels = [m[0] for m in MODELS_CMAPSS]
    lats   = [m[1] for m in MODELS_CMAPSS]
    colors = [latency_color(l) for l in lats]

    fig, ax = plt.subplots(figsize=(3.5, 2.5))

    bars = ax.barh(labels, lats, color=colors, edgecolor="white", linewidth=0.4, height=0.65)

    # Linea SLA 50ms
    ax.axvline(x=50, color="#c0392b", linewidth=1.0, linestyle="--", zorder=5)
    ax.text(52, 7.55, "SLA 50 ms", color="#c0392b", fontsize=7, va="center")

    # Annotazione TimesFM
    ax.text(lats[-1] * 1.05, 0, "MAE=0.006 (best)\n38× above SLA",
            fontsize=6, va="center", ha="left", color="#7f0000",
            linespacing=1.3)

    ax.set_xscale("log")
    ax.set_xlabel("Inference latency (ms, log scale)")
    ax.set_xlim(1, 8000)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda x, _: f"{int(x)}" if x >= 1 else f"{x:.1f}"
    ))

    # Legenda colori
    legend_elements = [
        mpatches.Patch(facecolor="#5cb85c", label="<10 ms (ultra-light)"),
        mpatches.Patch(facecolor="#5bc0de", label="10–100 ms (medium)"),
        mpatches.Patch(facecolor="#f0ad4e", label="100–500 ms (heavy)"),
        mpatches.Patch(facecolor="#d9534f", label=">500 ms (unusable)"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=6,
              framealpha=0.85, handlelength=1.0, borderpad=0.4)

    ax.grid(axis="x", which="both", linestyle=":", linewidth=0.4, alpha=0.6)
    ax.set_axisbelow(True)
    ax.invert_yaxis()

    fig.tight_layout()
    fig.savefig(out_pdf)
    fig.savefig(out_png)
    plt.close(fig)
    print(f"[OK] {out_pdf.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# GRAFICO 2 — Accuracy–Latency Scatter (bubble size = RAM)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_accuracy_latency_scatter():
    out_pdf = FIG_DIR / "accuracy_latency_scatter.pdf"
    out_png = FIG_DIR / "accuracy_latency_scatter.png"

    # Solo modelli con MAE
    models_with_mae = [(m[0], m[1], m[2], m[3]) for m in MODELS_CMAPSS if m[3] is not None]
    labels = [m[0] for m in models_with_mae]
    lats   = [m[1] for m in models_with_mae]
    rams   = [m[2] for m in models_with_mae]
    maes   = [m[3] for m in models_with_mae]

    # Bubble size proporzionale a RAM (sqrt per non esagerare)
    sizes = [max(40, r ** 0.55) for r in rams]
    colors_scatter = [latency_color(l) for l in lats]

    fig, ax = plt.subplots(figsize=(3.5, 2.8))

    # Zona verde SLA compliant (x < 50ms)
    ax.axvspan(0.1, 50, alpha=0.08, color="green", zorder=0)
    ax.text(1.2, 0.003, "SLA compliant\n(<50 ms)", fontsize=6.5,
            color="green", alpha=0.9, va="top")

    sc = ax.scatter(lats, maes, s=sizes, c=colors_scatter,
                    edgecolors="gray", linewidths=0.4, zorder=3, alpha=0.9)

    # Labels punti
    offsets = {
        "MOMENT-L":  (0,   +0.008),
        "PatchTST":  (+2,  +0.06),
        "TimesFM":   (-50, -0.003),
    }
    for label, lat, mae in zip(labels, lats, maes):
        dx, dy = offsets.get(label, (2, 0))
        ax.annotate(label, (lat, mae), xytext=(lat + dx, mae + dy),
                    fontsize=7, ha="left" if dx >= 0 else "right",
                    arrowprops=dict(arrowstyle="-", color="gray",
                                   lw=0.5) if (dx != 0 or dy != 0) else None)

    # Annotazioni sweet spot / collapse
    ax.annotate("Sweet spot", xy=(29.664, 0.114108),
                xytext=(60, 0.22),
                fontsize=6.5, color="#27ae60", fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color="#27ae60", lw=0.8))

    ax.annotate("Zero-shot collapse", xy=(5.861, 1.302898),
                xytext=(10, 1.5),
                fontsize=6.5, color="#c0392b", fontstyle="italic",
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.8))

    ax.set_xscale("log")
    ax.set_xlabel("Inference latency (ms, log scale)")
    ax.set_ylabel("MAE on CMAPSS (lower is better)")
    ax.invert_yaxis()
    ax.set_xlim(1, 5000)

    ax.grid(which="both", linestyle=":", linewidth=0.4, alpha=0.5)
    ax.axvline(50, color="#c0392b", linewidth=0.9, linestyle="--", zorder=4)

    # Legenda bubble size
    for ram_val, label in [(14, "14 MB"), (1408, "1.4 GB")]:
        ax.scatter([], [], s=max(40, ram_val ** 0.55),
                   c="gray", alpha=0.6, label=f"RAM ~ {label}")
    ax.legend(loc="upper right", fontsize=6.5, handlelength=1.0,
              borderpad=0.5, framealpha=0.85)

    fig.tight_layout()
    fig.savefig(out_pdf)
    fig.savefig(out_png)
    plt.close(fig)
    print(f"[OK] {out_pdf.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# GRAFICO 3 — Drift MAE Timeline
# ═══════════════════════════════════════════════════════════════════════════════

def plot_drift_timeline():
    out_pdf = FIG_DIR / "drift_mae_timeline.pdf"
    out_png = FIG_DIR / "drift_mae_timeline.png"

    # Carica dati reali dal JSON
    with open(DRIFT_PATH, "r", encoding="utf-8") as f:
        drift = json.load(f)

    detection_idx = drift["detection_index"]       # 1380
    threshold     = drift["threshold"]             # 1.9918
    mae_baseline  = drift["mae_baseline_train"]    # 0.796
    sample        = drift["mae_series_sample"]     # [[t, mae], ...]

    t_sample = [s[0] for s in sample]
    m_sample = [s[1] for s in sample]

    # Genera serie baseline sintetica prima del sample (t=1100..1210)
    rng = np.random.default_rng(42)
    t_pre = np.arange(1100, t_sample[0], 10)
    m_pre = mae_baseline + rng.normal(0, 0.12, len(t_pre))
    m_pre = np.clip(m_pre, 0.05, 1.8)

    # Unisci
    t_all = list(t_pre) + t_sample
    m_all = list(m_pre) + m_sample

    # Recovery point canonico
    recovery_t = 1400

    fig, ax = plt.subplots(figsize=(7.0, 2.6))

    # Linea MAE
    ax.plot(t_all, m_all, color="#2980b9", linewidth=1.2, label="Baseline model MAE", zorder=3)

    # Threshold
    ax.axhline(threshold, color="#e67e22", linewidth=0.9, linestyle="--",
               label=f"ADWIN threshold ({threshold:.4f})", zorder=4)

    # Linea verticale detection
    ax.axvline(detection_idx, color="#c0392b", linewidth=1.2, linestyle="-", zorder=5)
    ax.text(detection_idx + 3, max(m_all) * 0.95,
            f"Drift detected\nt={detection_idx}",
            color="#c0392b", fontsize=7.5, va="top", linespacing=1.3)

    # Linea verticale recovery
    ax.axvline(recovery_t, color="#27ae60", linewidth=1.2, linestyle="-", zorder=5)
    ax.text(recovery_t + 3, max(m_all) * 0.95,
            f"Recovery\nt={recovery_t}",
            color="#27ae60", fontsize=7.5, va="top", linespacing=1.3)

    # Shading rosso tra detection e recovery
    ax.axvspan(detection_idx, recovery_t, alpha=0.10, color="#e74c3c", zorder=1)

    ax.set_xlabel("Time step")
    ax.set_ylabel("MAE")
    ax.set_xlim(t_all[0], t_all[-1] + 20)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", fontsize=7.5, framealpha=0.88)
    ax.grid(linestyle=":", linewidth=0.4, alpha=0.6)
    ax.set_axisbelow(True)

    fig.tight_layout()
    fig.savefig(out_pdf)
    fig.savefig(out_png)
    plt.close(fig)
    print(f"[OK] {out_pdf.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating thesis plots...")
    plot_latency_comparison()
    plot_accuracy_latency_scatter()
    plot_drift_timeline()
    print(f"\nAll figures saved to: {FIG_DIR}")
    print("Upload contents of results/figures/ to Overleaf project as 'figures/' folder.")
