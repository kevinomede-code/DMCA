"""
pipeline/sla_rerun.py
=====================

Non-destructive re-run driver for the missed-alarm / SLA-coverage experiment.

Purpose (remediation pipeline D1+D2 / A13)
------------------------------------------
The canonical simulation in ``missed_alarm_simulation.py`` hardcodes
``SLA_MS = 50`` and uses ``round()`` for the sampling step. The remediation
requires:
  * SLA = 100 ms  (anchored to 3GPP TS 22.104 Table 5.2-2, "vibration sensor"
    asset-monitoring class: E2E latency < 100 ms), not to hardware.
  * step = ceil(l_nano / SLA)   (Eq. 10 fix — no rounding that rescues the
    boundary model).
  * a sensitivity sweep on the ratio k/SLA (k = T4->Nano factor).

This driver REUSES the data loaders and alarm logic from the canonical module
(so nothing there is touched) but recomputes coverage/step with parametric
SLA, k and rounding mode. It regenerates Table 12 numbers, per-bearing
lead-time, and the sensitivity table.

Latencies come from the canonical T4 benchmark
(results/benchmarks/2026-04-07/benchmark_results_modal.csv) — no GPU needed.

Usage
-----
    python pipeline/sla_rerun.py \
        --pronostia-root data/datasets/pronostia_real/ieee-phm-2012-data-challenge-dataset-master/Learning_set \
        --output-dir results/missed_alarm

Author: Kevin Omede — DMCA remediation
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

import missed_alarm_simulation as base


# T4 latencies (ms) — canonical benchmark, FD001 split (as used in thesis §7.5)
MODEL_LAT_T4 = {
    "PatchTST":  5.86,
    "Lag-Llama": 7.77,
    "Moirai-S":  53.73,
}
MODEL_LABEL = {
    "PatchTST":  "Admissible (point predictor — §9.2 collapse)",
    "Lag-Llama": "Admissible (probabilistic, no collapse)",
    "Moirai-S":  "Non-admissible (SLA-violating)",
}


def coverage_step(lat_t4_ms: float, sla_ms: float, k: float,
                  mode: str = "ceil") -> tuple[float, int, float]:
    """Return (lat_nano_ms, sampling_step s, effective coverage c_eff=1/s).

    s = ceil(l_nano / SLA)  (mode='ceil', canonical fix Eq.10)
    s = round(l_nano / SLA) (mode='round', legacy behaviour for comparison)
    """
    lat_nano = lat_t4_ms * k
    ratio = lat_nano / sla_ms
    if mode == "ceil":
        s = max(1, math.ceil(ratio))
    elif mode == "round":
        s = max(1, int(round(ratio)))
    else:
        raise ValueError(f"unknown rounding mode: {mode}")
    c_eff = 1.0 / s
    return lat_nano, s, c_eff


def lead_time_for_step(rms: pd.Series, step: int,
                       sigma: float = base.THRESHOLD_SIGMA_PRIMARY,
                       period_s: int = base.PRONOSTIA_ACQUISITION_PERIOD_S,
                       k_persist: int = base.PERSISTENCE_K) -> dict:
    """Coverage-only lead-time for a given integer sampling step on one bearing.

    Reuses the canonical baseline/threshold/persistence logic; only the
    subsampling step is injected from outside (so SLA/k drive it).
    """
    n = len(rms)
    n_baseline = max(int(base.BASELINE_FRAC * n), 10)
    baseline = rms.iloc[:n_baseline]
    threshold = float(baseline.mean() + sigma * baseline.std())

    sampled_idx = np.arange(0, n, step)
    sampled_values = rms.iloc[sampled_idx].values
    alarm_indices = base.apply_persistence(sampled_idx, sampled_values,
                                           threshold, k=k_persist)
    failure_idx = base.find_failure_index(rms)

    if alarm_indices:
        first_alarm = alarm_indices[0]
        lead_s = max(0, (failure_idx - first_alarm) * period_s)
    else:
        first_alarm = None
        lead_s = 0

    return {
        "n_acquisitions": n,
        "n_processed": len(sampled_idx),
        "threshold_g": round(threshold, 4),
        "n_alarms": len(alarm_indices),
        "first_alarm_idx": first_alarm,
        "first_alarm_lead_s": int(lead_s),
        "failure_idx": failure_idx,
        "actionable": bool(lead_s >= base.ACTION_WINDOW_S_PRONOSTIA),
    }


def load_bearings(root: Path) -> list[tuple[str, pd.Series]]:
    out = []
    for bp in sorted(root.glob("Bearing*")):
        if bp.is_dir():
            try:
                out.append((bp.name, base.load_bearing_rms(bp)))
            except Exception as exc:  # pragma: no cover
                print(f"  ! skip {bp.name}: {exc}")
    return out


def run_canonical(bearings, sla_ms, k, mode) -> pd.DataFrame:
    rows = []
    for bname, rms in bearings:
        for model, lat_t4 in MODEL_LAT_T4.items():
            lat_nano, s, c_eff = coverage_step(lat_t4, sla_ms, k, mode)
            lt = lead_time_for_step(rms, s)
            rows.append({
                "bearing": bname, "model": model,
                "lat_t4_ms": lat_t4, "lat_nano_ms": round(lat_nano, 1),
                "sla_ms": sla_ms, "k": k, "rounding": mode,
                "s": s, "c_eff": round(c_eff, 4),
                **lt,
            })
    return pd.DataFrame(rows)


def run_sensitivity(bearings, sla_values, k, mode) -> pd.DataFrame:
    rows = []
    for sla in sla_values:
        for bname, rms in bearings:
            for model, lat_t4 in MODEL_LAT_T4.items():
                lat_nano, s, c_eff = coverage_step(lat_t4, sla, k, mode)
                lt = lead_time_for_step(rms, s)
                rows.append({
                    "sla_ms": sla, "k_equiv_at_sla100": round(k * 100.0 / sla, 2),
                    "bearing": bname, "model": model,
                    "lat_nano_ms": round(lat_nano, 1),
                    "s": s, "c_eff": round(c_eff, 4),
                    "first_alarm_lead_s": lt["first_alarm_lead_s"],
                    "n_alarms": lt["n_alarms"],
                    "actionable": lt["actionable"],
                })
    return pd.DataFrame(rows)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pronostia-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path,
                    default=Path("results/missed_alarm"))
    ap.add_argument("--sla-ms", type=float, default=100.0)
    ap.add_argument("--k", type=float, default=10.0)
    ap.add_argument("--rounding", choices=["ceil", "round"], default="ceil")
    ap.add_argument("--sla-sweep", type=float, nargs="+",
                    default=[10, 50, 100, 250, 500])
    args = ap.parse_args()

    bearings = load_bearings(args.pronostia_root)
    if not bearings:
        raise SystemExit(f"No bearings under {args.pronostia_root}")
    print(f"Loaded {len(bearings)} bearing(s): "
          f"{', '.join(b for b, _ in bearings)}")

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # --- Canonical Table 12 @ SLA=100, ceiling ---
    canon = run_canonical(bearings, args.sla_ms, args.k, args.rounding)
    canon.to_csv(args.output_dir / "results_sla100_ceil.csv", index=False)

    # --- Legacy comparison @ SLA=50, round (what the thesis currently reports) ---
    legacy = run_canonical(bearings, 50.0, args.k, "round")
    legacy.to_csv(args.output_dir / "results_sla50_round_LEGACY.csv", index=False)

    # --- Sensitivity sweep on k/SLA ---
    sens = run_sensitivity(bearings, args.sla_sweep, args.k, args.rounding)
    sens.to_csv(args.output_dir / "sla_sensitivity.csv", index=False)

    # --- Eq.11 bound vs empirical gap (per model, canonical SLA) ---
    #   bound Δt_max = (2s - 1) * Tarr   (Tarr = 10 s on PRONOSTIA)
    tarr = base.PRONOSTIA_ACQUISITION_PERIOD_S
    eq11 = []
    for _, r in canon.iterrows():
        bound = (2 * r["s"] - 1) * tarr
        eq11.append({"bearing": r["bearing"], "model": r["model"],
                     "s": int(r["s"]), "bound_dtmax_s": bound,
                     "lead_s": int(r["first_alarm_lead_s"]),
                     "n_alarms": int(r["n_alarms"])})
    eq11_df = pd.DataFrame(eq11)

    summary = {
        "config": {"sla_ms": args.sla_ms, "k": args.k,
                   "rounding": args.rounding, "tarr_s": tarr,
                   "sigma": base.THRESHOLD_SIGMA_PRIMARY,
                   "persistence_k": base.PERSISTENCE_K,
                   "baseline_frac": base.BASELINE_FRAC},
        "table12_canonical": canon[["model", "lat_t4_ms", "lat_nano_ms",
                                    "s", "c_eff"]].drop_duplicates(
                                        "model").to_dict("records"),
        "legacy_sla50_round": legacy[["model", "s", "c_eff"]].drop_duplicates(
            "model").to_dict("records"),
        "eq11_bound_vs_empirical": eq11,
    }
    with open(args.output_dir / "summary_sla100.json", "w") as f:
        json.dump(summary, f, indent=2)

    # ---- console report ----
    def show(df, cols, title):
        print("\n" + "=" * 64 + f"\n  {title}\n" + "=" * 64)
        print(df[cols].to_string(index=False))

    show(canon.drop_duplicates("model"),
         ["model", "lat_t4_ms", "lat_nano_ms", "s", "c_eff"],
         "TABLE 12 — canonical  (SLA=100ms, k=10, CEIL)")
    show(legacy.drop_duplicates("model"),
         ["model", "s", "c_eff"],
         "LEGACY (what thesis reports now: SLA=50ms, ROUND)")
    show(canon, ["bearing", "model", "s", "c_eff", "n_alarms",
                 "first_alarm_lead_s", "actionable"],
         "LEAD TIME @ SLA=100ms (per bearing)")
    show(eq11_df, ["bearing", "model", "s", "bound_dtmax_s", "lead_s"],
         "Eq.11 bound (2s-1)*Tarr  vs  empirical lead")
    show(sens.drop_duplicates(["sla_ms", "model"]),
         ["sla_ms", "k_equiv_at_sla100", "model", "s", "c_eff"],
         "SENSITIVITY sweep k/SLA")
    print(f"\nOutputs written to {args.output_dir}\n")


if __name__ == "__main__":
    main()
