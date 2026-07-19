"""
scripts/generate_synthetic_pronostia.py
========================================

Generate a synthetic PRONOSTIA-compatible bearing dataset for smoke testing
the pipeline/missed_alarm_simulation.py module without requiring the multi-GB
real download.

The synthetic bearings follow the real PRONOSTIA file layout:
  data/datasets/pronostia/Learning_set/Bearing<X>_<Y>/acc_NNNNN.csv
with 6 columns per file (hour, min, sec, microsec, h_acc, v_acc) and 2560
rows per acquisition (the canonical 0.1s @ 25.6kHz window).

Each synthetic bearing has a realistic degradation profile: long healthy
baseline + sigmoidal rise to a failure regime. Physical units are in g.

Usage
-----
    python scripts/generate_synthetic_pronostia.py
    python scripts/generate_synthetic_pronostia.py --bearing Bearing1_1 --n-acq 300

This is for **pipeline validation only** — for canonical scientific results,
the real FEMTO-ST PRONOSTIA dataset must be downloaded and used.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd

# Synthetic bearing profiles: (n_acquisitions, baseline_g, peak_g, rise_start_frac)
# Tuned to roughly match real PRONOSTIA Bearing 1_1..3_2 lifetimes.
SYNTHETIC_PROFILES = {
    "Bearing1_1": dict(n_acq=300, baseline_g=0.65, peak_g=22.0, rise_frac=0.78, seed=11),
    "Bearing1_2": dict(n_acq=200, baseline_g=0.70, peak_g=21.5, rise_frac=0.75, seed=12),
    "Bearing2_1": dict(n_acq=220, baseline_g=0.80, peak_g=21.0, rise_frac=0.74, seed=21),
    "Bearing2_2": dict(n_acq=180, baseline_g=0.75, peak_g=22.5, rise_frac=0.72, seed=22),
    "Bearing3_1": dict(n_acq=120, baseline_g=0.85, peak_g=21.8, rise_frac=0.70, seed=31),
    "Bearing3_2": dict(n_acq=60,  baseline_g=0.90, peak_g=22.2, rise_frac=0.65, seed=32),
}

SAMPLES_PER_ACQ = 2560              # 0.1 s @ 25.6 kHz
ACQUISITION_PERIOD_S = 10           # 1 acquisition per 10 s


def rms_profile(n: int, baseline_g: float, peak_g: float,
                rise_frac: float, seed: int) -> np.ndarray:
    """Build the RMS-vs-time profile for one bearing.

    - Healthy phase: small Gaussian noise around ``baseline_g`` (first ~rise_frac
      of the trace).
    - Degradation: smooth sigmoid rise from baseline to ``peak_g`` in the last
      ``(1 - rise_frac)`` of the trace.
    """
    rng = np.random.default_rng(seed)
    rms = np.full(n, baseline_g, dtype=float)

    # Healthy noise
    rms += rng.normal(0, baseline_g * 0.05, size=n)

    # Degradation rise
    rise_start = int(rise_frac * n)
    rise_len = n - rise_start
    if rise_len > 1:
        t = np.linspace(-6, 6, rise_len)               # sigmoid x-axis
        sigmoid = 1.0 / (1.0 + np.exp(-t))
        rise = baseline_g + (peak_g - baseline_g) * sigmoid
        # Add some heteroscedastic noise (variance grows with amplitude)
        rise = rise + rng.normal(0, 0.02 * rise, size=rise_len)
        rms[rise_start:] = rise

    rms = np.clip(rms, 0.1, None)
    return rms


def synthesize_raw_window(rms_target: float, seed: int) -> np.ndarray:
    """Generate a 2560-sample h_acc window whose RMS equals ``rms_target`` (g).

    Uses zero-mean Gaussian noise with sigma = rms_target (sigma == RMS for
    zero-mean Gaussian).
    """
    rng = np.random.default_rng(seed)
    sigma = float(rms_target)
    return rng.normal(0, sigma, size=SAMPLES_PER_ACQ)


def write_acquisition(out_dir: Path, idx: int,
                      h_acc: np.ndarray, v_acc: np.ndarray) -> None:
    """Write one acc_NNNNN.csv with PRONOSTIA's 6-column format."""
    # Compose synthetic timestamps just to match the column structure
    base_seconds = idx * ACQUISITION_PERIOD_S
    hours   = (base_seconds // 3600) % 24
    minutes = (base_seconds // 60) % 60
    seconds = base_seconds % 60
    microsec = (np.arange(SAMPLES_PER_ACQ) * (1_000_000 // SAMPLES_PER_ACQ)
                ).astype(int)

    df = pd.DataFrame({
        "hour":     np.full(SAMPLES_PER_ACQ, hours, dtype=int),
        "min":      np.full(SAMPLES_PER_ACQ, minutes, dtype=int),
        "sec":      np.full(SAMPLES_PER_ACQ, seconds, dtype=int),
        "microsec": microsec,
        "h_acc":    h_acc.round(4),
        "v_acc":    v_acc.round(4),
    })
    fname = out_dir / f"acc_{idx + 1:05d}.csv"
    df.to_csv(fname, header=False, index=False)


def generate_bearing(bearing_id: str, out_root: Path,
                     profile_override: dict | None = None) -> Path:
    """Generate one synthetic bearing's full acquisition folder."""
    if bearing_id not in SYNTHETIC_PROFILES and profile_override is None:
        raise ValueError(f"Unknown bearing {bearing_id} and no profile override")

    profile = profile_override or SYNTHETIC_PROFILES[bearing_id]
    n = profile["n_acq"]
    seed = profile["seed"]

    rms_target = rms_profile(
        n=n,
        baseline_g=profile["baseline_g"],
        peak_g=profile["peak_g"],
        rise_frac=profile["rise_frac"],
        seed=seed,
    )

    bearing_dir = out_root / bearing_id
    bearing_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Generating %s — %d acquisitions, baseline %.2fg, peak %.2fg",
                 bearing_id, n, profile["baseline_g"], profile["peak_g"])

    for idx in range(n):
        h_acc = synthesize_raw_window(rms_target[idx], seed=seed * 1000 + idx)
        # Vertical accel: independent, similar scale, for column-format fidelity
        v_acc = synthesize_raw_window(rms_target[idx] * 0.7,
                                      seed=seed * 1000 + idx + 500_000)
        write_acquisition(bearing_dir, idx, h_acc, v_acc)

    logging.info("  Wrote %d files to %s", n, bearing_dir)
    return bearing_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-root",
                        type=Path,
                        default=Path("data/datasets/pronostia/Learning_set"),
                        help="Output Learning_set root")
    parser.add_argument("--bearing",
                        action="append",
                        choices=list(SYNTHETIC_PROFILES.keys()),
                        help="Specific bearing to generate (repeatable). "
                             "Default: all 6 training bearings.")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level,
                        format="%(asctime)s %(levelname)s  %(message)s")

    bearings = args.bearing or list(SYNTHETIC_PROFILES.keys())
    args.out_root.mkdir(parents=True, exist_ok=True)

    for b in bearings:
        generate_bearing(b, args.out_root)

    logging.info("Done. Output: %s", args.out_root)
    print("\n*** SYNTHETIC DATA — for pipeline validation only ***")
    print("*** Real PRONOSTIA needed for canonical results.   ***\n")


if __name__ == "__main__":
    main()
