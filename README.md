# DMCA — Dynamic Model-Context Alignment in Industry 4.0

> A Digital-Twin-driven closed-loop framework for continuous selection and
> adaptation of open-source AI models on industrial edge devices.

**MSc Thesis** · Politecnico di Torino × Beihang University · 2025/2026
**Author:** Kevin Omede ·
**Supervisor:** Prof. Alessandro Simeone ·
**Co-supervisor:** Prof. Yi Li

[**▶ Open the live HMI demo**](demo/factory_v4.html)

---

## TL;DR

Industrial deployments of AI models break the moment the plant changes — a new
sensor, a software update, a slow drift in the signal — and a model picked once
for "best accuracy" is rarely the one that survives the SLA, the hardware, or
the safety envelope. **DMCA** treats model selection as an *alignment* problem
to keep solved over time, driven by the plant's Digital Twin (AAS), and made
auditable through a conversational copilot with built-in XAI.

The framework closes the loop in five stages: profile the device, rank
candidate models against the constraints, gate-check before deploy, watch for
drift with an explainable classifier, then re-align with operator-in-the-loop
approval.

## The DMCA loop (five stages)

1. **DT Profiling** — parse the device's Asset Administration Shell (AAS) and
   extract the operational constraints (latency SLA, memory, hardware tier,
   protocol).
2. **Model Selection (TOPSIS)** — multi-criteria ranking of HuggingFace models
   weighted on MAE (0.5), latency (0.3), parameter count (0.1) and license
   (0.1). SLA-coherent: out-of-budget candidates are excluded with explicit
   reason.
3. **Edge Deployment (Quality Gate)** — four-check validation before the
   model goes live: latency, output shape, validity (zero-shot collapse
   detection), memory.
4. **Drift Detection (ADWIN + XAI)** — Bifet 2007 ADWIN with δ = 0.002,
   followed by an eight-feature classifier (decision tree v3.1.1) that labels
   the drift as ABRUPT / GRADUAL / INCREMENTAL / VARIANCE_SHIFT /
   OUTLIER_DRIVEN / DISTRIBUTION / UNCLASSIFIED.
5. **Re-alignment** — SIL-aware operator confirmation. On Jetson Nano the
   discipline of *no-swap-when-no-SLA-coherent-improvement* is enforced
   explicitly; SLA-coherent swaps (e.g., to Chronos-T5-tiny on Raspberry Pi 4)
   are deployed in shadow mode for validation.

## Key results (canonical, GPU NVIDIA T4)

8 zero-shot time-series foundation models benchmarked on CMAPSS FD001 and
ETT-h1, total infrastructure cost **0.30 USD**. The selection-discipline story
is summarised by the *TimesFM paradox*: TimesFM has the **best** MAE of any
model (0.006353), but its 2039 ms latency is 40.8× over a 50 ms SLA — it would
serve only ~2.5% of fault-detection windows on a Jetson Nano. DMCA correctly
excludes it on the latency constraint and selects MOMENT-Large (MAE 0.114, 29.7
ms) instead.

ADWIN-v3.1.1 drift classifier reaches **92% held-out accuracy** (5 drift types
× 5 seeds, FAR = 0.000).

Canonical data:
- `results/benchmarks/2026-04-07/benchmark_results_modal.csv`
- `results/drift_experiments/drift_cycle_results.json`

## Live demo

A self-contained HMI console (HTML + Chart.js, no build step) walks through
the whole loop with progressive disclosure: a calm at-rest canvas, glass
side-drawers per stage, real canonical data, and an honest counterfactual
against the TimesFM trap.

Open `demo/factory_v4.html` in any modern browser, or — once the repository is
published — via GitHub Pages.

## Repository structure

```
.
├── README.md              this file
├── LICENSE                MIT for the code (CC BY 4.0 for thesis content)
├── .gitignore             excludes thesis sources, secrets, heavy data
├── .env.template          required environment variables
├── requirements.txt       Python dependencies
├── CLAUDE.md              project-wide engineering notes
├── gaps.json              the 5 research gaps + model catalogue
├── references_master.bib  bibliography (BibTeX)
│
├── pipeline/              the DMCA framework (10 modules)
├── demo/                  HMI demonstration (HTML)
├── assets/                synthetic AAS files (3 edge devices)
├── results/               canonical benchmarks & drift experiments
├── figures/               figures used in the thesis
├── bibliography/          per-gap BibTeX files
├── case_studies/          Avio Aero & Hongdian pilot proposals
├── scripts/               helper scripts (sanity checks, plotting)
├── simulator_phase2/      future-work simulator notes
└── tests/                 pytest smoke tests for the pipeline
```

## Reproducing the canonical results

```bash
# 1 — clone & set up
git clone <your-fork>
cd thesis-research
python -m venv .venv && . .venv/Scripts/activate   # Windows
pip install -r requirements.txt

# 2 — fill in secrets
cp .env.template .env
# edit .env: HF_TOKEN, ANTHROPIC_API_KEY, SEMANTIC_SCHOLAR_API_KEY (optional)

# 3 — smoke tests
pytest tests/ -q

# 4 — replay the canonical drift cycle (no GPU needed)
python pipeline/simulation_agent.py --workflow W3
```

The benchmark CSV at `results/benchmarks/2026-04-07/` is the canonical output
of a one-shot run on a Modal NVIDIA T4 (0.30 USD). It is intentionally
**not** regenerated by the smoke tests.

## Citation

When the thesis is officially defended, please cite as:

```bibtex
@mastersthesis{omede2026dmca,
  author       = {Kevin Omede},
  title        = {Dynamic Model-Context Alignment in Industry 4.0},
  school       = {Politecnico di Torino × Beihang University},
  year         = {2026},
  type         = {{MSc} thesis}
}
```

## Acknowledgements

Literature search and parts of the bibliographic curation in this work were
assisted by **[AutoResearchClaw](https://github.com/)** — a
research-automation agent maintained by the author as a separate, standalone
project. AutoResearchClaw is intentionally *not* included in this repository;
its source is published at its own URL.

Supervision: Prof. Alessandro Simeone (Politecnico di Torino) and
Prof. Yi Li (Beihang University). The author also thanks the Modal team for
the serverless GPU credits used to benchmark the eight models.

## License

The **code** in this repository is released under the **MIT License**
(see `LICENSE`). The **thesis text**, figures and results, once publicly
released, are licensed under **CC BY 4.0** unless noted otherwise on a
per-file basis.

---

*Status — May 2026: Phase 1 (pure simulation, no GPU) complete. Canonical
benchmarks frozen. Demo v4 ready. Phase 2 (dynamic streaming simulator)
documented in `simulator_phase2/`.*
