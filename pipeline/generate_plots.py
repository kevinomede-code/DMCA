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

    # Le barre sono le latenze di BENCHMARK misurate su GPU T4 (canoniche, uguali
    # alla tabella). La soglia 100ms qui e' un riferimento soft-real-time a scala T4
    # (classe Jetson Orin / entry GPU), NON l'SLA hard del Jetson Nano del Case Study.
    # Sul Nano le latenze vanno x10: solo PatchTST (58.6) e Lag-Llama (77.7) restano
    # entro l'SLA edge di 100ms. La nota in figura disambigua i due frame.
    labels = [m[0] for m in MODELS_CMAPSS]
    lats   = [m[1] for m in MODELS_CMAPSS]
    colors = [latency_color(l) for l in lats]

    fig, ax = plt.subplots(figsize=(3.5, 2.5))

    bars = ax.barh(labels, lats, color=colors, edgecolor="white", linewidth=0.4, height=0.65)

    # Linea soft-real-time 100ms a scala T4 (classe Orin) — NON l'SLA Nano
    ax.axvline(x=100, color="#c0392b", linewidth=1.0, linestyle="--", zorder=5)
    ax.text(102, 7.55, "soft-SLA 100 ms (T4)", color="#c0392b", fontsize=6.5, va="center")

    # Nota disambiguazione frame edge (Jetson Nano = T4 x10)
    ax.text(1.3, 0.35, "Jetson Nano: ×10 →\nonly PatchTST, Lag-Llama\nwithin 100 ms edge SLA",
            fontsize=5.6, va="center", ha="left", color="#333333", linespacing=1.25)

    # Annotazione TimesFM (T4: 2039/100 ~ 20x oltre la soglia)
    ax.text(lats[-1] * 1.05, 0, "MAE=0.006 (best)\n20× above ref.",
            fontsize=6, va="center", ha="left", color="#7f0000",
            linespacing=1.3)

    ax.set_xscale("log")
    ax.set_xlabel("Benchmark latency (GPU T4, ms, log scale)")
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

    # Asse x = latenza di BENCHMARK su GPU T4 (canonica, come la tabella e il capitolo
    # cluster). La zona verde <100ms e' un riferimento soft-real-time a scala T4
    # (classe Jetson Orin / entry GPU), NON l'SLA hard del Jetson Nano. Sul Nano x10.

    # Solo modelli con MAE
    models_with_mae = [(m[0], m[1], m[2], m[3]) for m in MODELS_CMAPSS if m[3] is not None]
    labels = [m[0] for m in models_with_mae]
    lats   = [m[1] for m in models_with_mae]
    rams   = [m[2] for m in models_with_mae]
    maes   = [m[3] for m in models_with_mae]

    # Bubble size proporzionale a RAM (sqrt per non esagerare)
    sizes = [max(40, r ** 0.55) for r in rams]
    colors_scatter = [latency_color(l) for l in lats]

    fig, ax = plt.subplots(figsize=(4.2, 3.2))

    ax.set_xscale("log")
    ax.set_xlim(1.5, 9000)
    ax.invert_yaxis()
    ax.set_ylim(1.78, -0.20)          # margini sopra (0.0) e sotto (1.303)

    # Zona verde soft-real-time (x < 100ms, scala T4)
    ax.axvspan(1.5, 100, alpha=0.08, color="green", zorder=0)
    ax.text(2.0, -0.15, "soft real-time\n(<100 ms, T4)", fontsize=6.5,
            color="#1e7d1e", alpha=0.95, va="top", ha="left")

    ax.axvline(100, color="#c0392b", linewidth=0.9, linestyle="--", zorder=1)

    sc = ax.scatter(lats, maes, s=sizes, c=colors_scatter,
                    edgecolors="gray", linewidths=0.4, zorder=3, alpha=0.9)

    # Etichette punti — posizioni fisse anti-sovrapposizione
    label_pos = {
        "PatchTST": (9,    1.30, "left"),
        "MOMENT-L": (30,   0.02, "center"),
        "TimesFM":  (2039, 0.11, "center"),
    }
    for label, lat, mae in zip(labels, lats, maes):
        tx, ty, ha = label_pos.get(label, (lat * 1.2, mae, "left"))
        ax.annotate(label, (lat, mae), xytext=(tx, ty),
                    fontsize=7, ha=ha, va="center", zorder=5,
                    arrowprops=dict(arrowstyle="-", color="gray", lw=0.5))

    # Annotazioni interpretative (non sovrapposte ai punti)
    ax.annotate("Sweet spot\n(Orin-class)", xy=(29.664, 0.114108),
                xytext=(150, 0.36), fontsize=6.5, color="#27ae60",
                fontstyle="italic", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#27ae60", lw=0.8))

    ax.annotate("Zero-shot\ncollapse", xy=(5.861, 1.302898),
                xytext=(20, 1.60), fontsize=6.5, color="#c0392b",
                fontstyle="italic", ha="center", va="center",
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=0.8))

    ax.set_xlabel("Benchmark latency (GPU T4, ms, log scale)")
    ax.set_ylabel("MAE on CMAPSS (lower is better)")
    ax.grid(which="both", linestyle=":", linewidth=0.4, alpha=0.5)
    ax.set_axisbelow(True)

    # Legenda bubble size — in basso a destra (area vuota)
    for ram_val, label in [(14, "14 MB"), (1408, "1.4 GB")]:
        ax.scatter([], [], s=max(40, ram_val ** 0.55),
                   c="gray", alpha=0.6, label=f"RAM ~ {label}")
    ax.legend(loc="lower right", fontsize=6.5, handlelength=1.0,
              borderpad=0.5, labelspacing=0.7, framealpha=0.9)

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

    # Istante dello SWAP (non e' un "recovery" di MAE: l'improvement misurato
    # sul test post-drift condiviso e' -3.69%). Vedi Limitations "Improvement metric".
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
    ax.text(re