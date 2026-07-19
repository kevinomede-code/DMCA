import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker
from pathlib import Path

plt.rcParams.update({
    "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
    "xtick.labelsize": 7, "ytick.labelsize": 7, "figure.dpi": 130,
    "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
})

FIG = Path("results/figures"); FIG.mkdir(parents=True, exist_ok=True)

# (label, lat_mean_ms T4, ram_mb, mae_or_None)
MODELS = [
    ("PatchTST",    5.861,    14,   1.302898),
    ("Lag-Llama",   7.768,    20,   None),
    ("MOMENT-L",   29.664,  1408,   0.114108),
    ("Moirai-S",   53.727,   106,   None),
    ("Moirai-L",   72.591,  2360,   None),
    ("Chronos-T", 166.824,    45,   None),
    ("Chronos-L", 829.961,  2771,   None),
    ("TimesFM",  2039.103,     8,   0.006353),
]

def lat_color(ms):
    if ms < 10:  return "#5cb85c"
    if ms < 100: return "#5bc0de"
    if ms < 500: return "#f0ad4e"
    return "#d9534f"

# ---------- BAR CHART ----------
def bar():
    labels=[m[0] for m in MODELS]; lats=[m[1] for m in MODELS]
    colors=[lat_color(l) for l in lats]
    fig,ax=plt.subplots(figsize=(3.6,2.6))
    ax.barh(labels,lats,color=colors,edgecolor="white",linewidth=0.4,height=0.65)
    ax.axvline(100,color="#c0392b",lw=1.0,ls="--",zorder=5)
    ax.text(112,0.35,"soft-SLA\n100 ms (T4)",color="#c0392b",fontsize=6.2,va="top",ha="left",linespacing=1.2)
    ax.text(150,2.7,"Jetson Nano: x10 ->\nonly PatchTST, Lag-Llama\nwithin 100 ms edge SLA",
            fontsize=5.8,va="center",ha="left",color="#333")
    ax.text(2200,0.15,"MAE=0.006\n(best), 20x\nabove ref.",fontsize=5.9,
            va="top",ha="left",color="#7f0000",linespacing=1.25)
    ax.set_xscale("log"); ax.set_xlim(1,8000)
    ax.set_xlabel("Benchmark latency (GPU T4, ms, log scale)")
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_:f"{int(x)}"))
    leg=[mpatches.Patch(facecolor="#5cb85c",label="<10 ms (ultra-light)"),
         mpatches.Patch(facecolor="#5bc0de",label="10-100 ms (medium)"),
         mpatches.Patch(facecolor="#f0ad4e",label="100-500 ms (heavy)"),
         mpatches.Patch(facecolor="#d9534f",label=">500 ms (unusable)")]
    ax.legend(handles=leg,loc="lower right",fontsize=6,framealpha=0.9,handlelength=1.0,borderpad=0.4)
    ax.grid(axis="x",which="both",ls=":",lw=0.4,alpha=0.6); ax.set_axisbelow(True); ax.invert_yaxis()
    fig.tight_layout()
    fig.savefig(FIG/"latency_comparison.pdf"); fig.savefig(FIG/"latency_comparison.png"); plt.close(fig)
    print("[OK] latency_comparison")

# ---------- SCATTER ----------
def scatter():
    mm=[m for m in MODELS if m[3] is not None]
    labels=[m[0] for m in mm]; lats=[m[1] for m in mm]; rams=[m[2] for m in mm]; maes=[m[3] for m in mm]
    sizes=[max(45,r**0.55) for r in rams]; colors=[lat_color(l) for l in lats]
    fig,ax=plt.subplots(figsize=(4.3,3.3))
    ax.set_xscale("log"); ax.set_xlim(1.5,9000); ax.invert_yaxis(); ax.set_ylim(1.78,-0.20)
    ax.axvspan(1.5,100,alpha=0.08,color="green",zorder=0)
    ax.text(2.0,-0.15,"soft real-time\n(<100 ms, T4)",fontsize=6.5,color="#1e7d1e",va="top",ha="left")
    ax.axvline(100,color="#c0392b",lw=0.9,ls="--",zorder=1)
    ax.scatter(lats,maes,s=sizes,c=colors,edgecolors="gray",linewidths=0.4,zorder=3,alpha=0.9)
    lpos={"PatchTST":(9,1.30,"left"),"MOMENT-L":(33,0.02,"center"),"TimesFM":(2039,0.11,"center")}
    for lab,la,ma in zip(labels,lats,maes):
        tx,ty,ha=lpos.get(lab,(la*1.2,ma,"left"))
        ax.annotate(lab,(la,ma),xytext=(tx,ty),fontsize=7,ha=ha,va="center",zorder=5,
                    arrowprops=dict(arrowstyle="-",color="gray",lw=0.5))
    ax.annotate("Sweet spot\n(Orin-class)",xy=(29.664,0.114108),xytext=(230,0.36),
                fontsize=6.5,color="#27ae60",fontstyle="italic",ha="center",va="center",
                arrowprops=dict(arrowstyle="->",color="#27ae60",lw=0.8))
    ax.annotate("Zero-shot\ncollapse",xy=(5.861,1.302898),xytext=(24,1.60),
                fontsize=6.5,color="#c0392b",fontstyle="italic",ha="center",va="center",
                arrowprops=dict(arrowstyle="->",color="#c0392b",lw=0.8))
    ax.set_xlabel("Benchmark latency (GPU T4, ms, log scale)")
    ax.set_ylabel("MAE on CMAPSS (lower is better)")
    ax.grid(which="both",ls=":",lw=0.4,alpha=0.5); ax.set_axisbelow(True)
    for rv,l in [(14,"14 MB"),(1408,"1.4 GB")]:
        ax.scatter([],[],s=max(45,rv**0.55),c="gray",alpha=0.6,label=f"RAM ~ {l}")
    ax.legend(loc="lower right",fontsize=6.5,handlelength=1.0,borderpad=0.5,labelspacing=0.7,framealpha=0.9)
    fig.tight_layout()
    fig.savefig(FIG/"accuracy_latency_scatter.pdf"); fig.savefig(FIG/"accuracy_latency_scatter.png"); plt.close(fig)
    print("[OK] accuracy_latency_scatter")

bar(); scatter()
import os; os.sync()
