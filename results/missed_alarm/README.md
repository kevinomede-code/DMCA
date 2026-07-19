# Missed-alarm cascade simulation — PRONOSTIA

Phase-1 empirical demonstration of the SLA paradox principle (thesis §7.5)
on real manufacturing data: FEMTO-ST PRONOSTIA bearing degradation traces
(IEEE PHM 2012 Challenge).

## What this folder contains (after running the simulation)

- `results.csv` — per-bearing × per-model × per-sigma results
- `sensitivity.csv` — sigma sweep (σ=2, 4) for robustness check
- `summary.json` — headline numbers for paper/thesis
- (figures live in `figures/missed_alarm/`)

## How the simulation works

**Coverage-only framing**: we isolate the temporal-coverage variable from
model accuracy. Both models are assumed to perfectly detect anomalies in
the windows they process. The differentiator is *how many windows each
model serves within the SLA budget*.

For each bearing:

1. Load all PRONOSTIA acquisition CSVs, compute RMS per acquisition
   (1 RMS scalar per 10 s, derived from 2560 samples @ 25.6 kHz).
2. Establish healthy baseline = first 10% of trace.
3. Threshold = baseline_mean + 3σ (with sensitivity at 2σ and 4σ).
4. Failure point = first index where RMS > 20 g (PRONOSTIA stop criterion).
5. For each model, compute coverage rate = SLA_MS / latency_nano:
   - PatchTST (58.6 ms on Nano):   85% coverage — admissible, point predictor (see §9.2 collapse caveat)
   - Lag-Llama (77.7 ms on Nano):  64% coverage — admissible, probabilistic (no collapse risk)
   - Moirai-S (537 ms on Nano):    9.3% coverage — non-admissible
6. Alarm raised when RMS > threshold AND the window is processed.
7. Measure first-alarm lead time vs failure; flag actionable if ≥ 5 min.

**Why two admissible models?** Including both PatchTST and Lag-Llama addresses
the zero-shot collapse caveat documented in thesis §9.2. The conclusion holds
regardless of which admissible model is chosen — what matters is SLA
compliance, not single-model accuracy. PatchTST maintains continuity with the
case study (§8.1.3); Lag-Llama serves as a collapse-free validation.

## How to run

```bash
# Prerequisite: PRONOSTIA Learning_set extracted to
# data/datasets/pronostia/Learning_set/Bearing1_1, etc.

# Smoke test on one bearing
python pipeline/missed_alarm_simulation.py \
    --bearings Bearing1_1 \
    --log-level INFO

# Full run on all 6 training bearings
python pipeline/missed_alarm_simulation.py
```

## Reproducibility

- Deterministic subsampling (no random seed needed)
- T4 latencies frozen from `results/benchmarks/2026-04-07/benchmark_results_modal.csv`
- T4 → Nano conversion factor: 10× (midpoint of [5×, 20×] datasheet range)
- SLA: 50 ms (Jetson Nano canonical)
- Baseline: first 10% of trace
- Action window: 300 s

## What the result tells us

If results match the expected pattern:

- **Zone A** (long bearings, 4-8h): both models actionable, PatchTST better lead time
- **Zone B** (medium bearings, 1.5-2.5h): Moirai-S marginal or non-actionable
- **Zone C** (short bearings, <1h): Moirai-S MISSES the actionable window

The principle scales from PRONOSTIA accelerated to industrial bearings via
ISO 10816 vibration severity zones — pre-failure detection envelope of
48-96 h (rapid-onset contamination, Senseye/Siemens 2024) shrinks
proportionally to actionable-action ratio under coverage constraint.

## Citations to add in thesis bibliography

- Nectoux et al. 2012 — *PRONOSTIA: An Experimental Platform for Bearings
  Accelerated Degradation Tests*, IEEE PHM 2012 Challenge
- ISO 10816-3:2009 (rev. ISO 20816-3:2022) — Vibration severity zones
- Lee, Lapira, Bagheri, Kao 2013 — *Recent advances in predictive
  manufacturing systems*, Manufacturing Letters
- Randall, Antoni 2011 — *Rolling element bearing diagnostics — A tutorial*,
  MSSP
- Senseye/Siemens 2024 — *True Cost of Downtime* report
