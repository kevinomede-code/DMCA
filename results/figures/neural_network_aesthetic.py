"""
Generates an aesthetic neural network diagram for IEEE thesis.
Output: results/figures/neural_network_aesthetic.png
Size: 800×500 px at 150 DPI
"""

import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Output path ────────────────────────────────────────────────────────────────
OUT_PATH = pathlib.Path(__file__).parent / "neural_network_aesthetic.png"

# ── Architecture ───────────────────────────────────────────────────────────────
LAYER_SIZES  = [4, 6, 6, 6, 3]
LAYER_LABELS = ["Input", "Hidden 1", "Hidden 2", "Hidden 3", "Output"]
LAYER_COLORS = ["#3B82F6", "#6366F1", "#8B5CF6", "#A855F7", "#EC4899"]

N_LAYERS = len(LAYER_SIZES)

# ── Figure setup ───────────────────────────────────────────────────────────────
DPI    = 150
WIDTH  = 800 / DPI
HEIGHT = 500 / DPI

fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT), dpi=DPI)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# ── Layout helpers ─────────────────────────────────────────────────────────────
# x positions of each layer, evenly spaced with margin
X_MARGIN = 0.08
x_positions = np.linspace(X_MARGIN, 1 - X_MARGIN, N_LAYERS)

# Base node radius in axes-fraction units
BASE_RADIUS = 0.030
SHADOW_OFFSET = (0.004, -0.004)
SHADOW_ALPHA  = 0.18
SHADOW_COLOR  = "#94A3B8"

# Store node centres for drawing edges
node_centres = []   # list of lists: node_centres[layer][node] = (x, y)

for li, (n_nodes, color) in enumerate(zip(LAYER_SIZES, LAYER_COLORS)):
    x = x_positions[li]
    # y positions: centred vertically
    y_positions = np.linspace(0.5 - (n_nodes - 1) * 0.09 / 2,
                               0.5 + (n_nodes - 1) * 0.09 / 2,
                               n_nodes)
    # Middle layer gets slightly larger nodes
    radius = BASE_RADIUS * (1.15 if li == 2 else 1.0)

    layer_centres = []
    for y in y_positions:
        layer_centres.append((x, y))
    node_centres.append(layer_centres)

# ── Draw edges first (behind nodes) ───────────────────────────────────────────
for li in range(N_LAYERS - 1):
    for (x1, y1) in node_centres[li]:
        for (x2, y2) in node_centres[li + 1]:
            ax.plot([x1, x2], [y1, y2],
                    color="#CBD5E1", alpha=0.35, linewidth=0.6,
                    zorder=1, solid_capstyle="round")

# ── Draw nodes ─────────────────────────────────────────────────────────────────
for li, (n_nodes, color) in enumerate(zip(LAYER_SIZES, LAYER_COLORS)):
    radius = BASE_RADIUS * (1.15 if li == 2 else 1.0)
    for (x, y) in node_centres[li]:
        # Drop shadow
        shadow = mpatches.Circle(
            (x + SHADOW_OFFSET[0], y + SHADOW_OFFSET[1]),
            radius,
            transform=ax.transData,
            color=SHADOW_COLOR,
            alpha=SHADOW_ALPHA,
            zorder=2
        )
        ax.add_patch(shadow)

        # Main filled circle
        circle = mpatches.Circle(
            (x, y),
            radius,
            transform=ax.transData,
            color=color,
            zorder=3
        )
        ax.add_patch(circle)

        # White border
        border = mpatches.Circle(
            (x, y),
            radius,
            transform=ax.transData,
            fill=False,
            edgecolor="white",
            linewidth=2.5,
            zorder=4
        )
        ax.add_patch(border)

# ── Layer labels ───────────────────────────────────────────────────────────────
LABEL_Y = 0.90
for li, (label, color) in enumerate(zip(LAYER_LABELS, LAYER_COLORS)):
    x = x_positions[li]
    ax.text(x, LABEL_Y, label,
            ha="center", va="center",
            fontsize=6.5, color="#374151",
            fontfamily="DejaVu Sans",
            zorder=5)

# ── Save ───────────────────────────────────────────────────────────────────────
plt.tight_layout(pad=0.2)
fig.savefig(OUT_PATH, dpi=DPI, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close(fig)
print(f"[OK] Saved: {OUT_PATH.resolve()}")
print(f"     Size: 800x500px @ 150 DPI")
