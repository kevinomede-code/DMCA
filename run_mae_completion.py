"""
run_mae_completion.py
=====================
Lancia la MAE completion suite su Modal GPU T4 e salva i risultati.

Output:
  results/benchmarks/2026-04-27/benchmark_mae_completion.csv
  results/benchmarks/2026-04-27/MERGE_NOTES.md  (aggiornato con costo reale)

Prerequisiti:
  python -m modal deploy pipeline/modal_mae_completion.py
  python run_mae_completion.py
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from loguru import logger

TODAY = "2026-04-27"
OUT_DIR = ROOT / "results" / "benchmarks" / TODAY
LOG_DIR = ROOT / "results" / "logs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")
logger.add(str(LOG_DIR / f"mae_completion_{TODAY}.log"), level="DEBUG")

# Stima costo T4
T4_RATE = 0.59 / 3600   # $/sec

CANONICAL_CSV = ROOT / "results" / "benchmarks" / "2026-04-07" / "benchmark_results_modal.csv"

# Latenza p95 canonical (per verifica ±20%)
CANONICAL_P95 = {
    "Salesforce/moirai-1.1-R-small":                  62.915,
    "Salesforce/moirai-1.1-R-large":                  73.914,
    "amazon/chronos-t5-tiny":                         203.102,
    "amazon/chronos-t5-large":                        902.932,
    "time-series-foundation-models/Lag-Llama":          8.882,
}


def check_validity(results: list[dict]) -> list[str]:
    """Controlla criteri di successo della task."""
    issues: list[str] = []
    ok_results = [r for r in results if r.get("status") == "ok"]

    for r in ok_results:
        mid = r["model_id"]
        mae  = r.get("mae")
        rmse = r.get("rmse")

        if mae is None or (isinstance(mae, float) and (mae != mae)):  # NaN check
            issues.append(f"FAIL {mid}: MAE è None o NaN")
            continue

        if rmse is None or (isinstance(rmse, float) and (rmse != rmse)):
            issues.append(f"FAIL {mid}: RMSE è None o NaN")
            continue

        # Validity check: MAE != RMSE (no zero-shot collapse)
        if abs(mae - rmse) < 1e-9:
            issues.append(f"WARN {mid}: MAE == RMSE ({mae:.6f}) — possibile collapse")

        # Latenza p95 coerente col canonico (±20%)
        canon_p95 = CANONICAL_P95.get(mid)
        if canon_p95:
            p95_new = r.get("latency_p95_ms", 0)
            lo, hi = canon_p95 * 0.80, canon_p95 * 1.20
            if not (lo <= p95_new <= hi):
                issues.append(
                    f"WARN {mid}: p95={p95_new:.1f}ms fuori ±20% del canonico ({canon_p95:.1f}ms)"
                )

    missing = [
        mid for mid in CANONICAL_P95
        if not any(r.get("model_id") == mid and r.get("status") == "ok" for r in results)
    ]
    if missing:
        issues.append(f"FAIL: modelli mancanti o in errore: {missing}")

    return issues


def main() -> None:
    logger.info("=" * 60)
    logger.info("MAE Completion Suite — Modal GPU T4")
    logger.info("=" * 60)

    try:
        import modal
    except ImportError:
        logger.error("Modal non installato. pip install modal")
        sys.exit(1)

    run_mae_suite = modal.Function.from_name("thesis-mae-completion", "run_mae_suite")

    t0 = time.perf_counter()
    try:
        result = run_mae_suite.remote()
    except Exception as e:
        logger.error(f"run_mae_suite.remote() fallito: {e}")
        sys.exit(1)

    elapsed = time.perf_counter() - t0
    cost_usd = T4_RATE * elapsed

    logger.info(f"Suite completata in {elapsed:.1f}s | Costo stimato: ~${cost_usd:.4f}")

    # ── Salva CSV ─────────────────────────────────────────────────────────────
    try:
        import pandas as pd
        records = result.get("dataframe_dict") or result.get("results", [])
        df = pd.DataFrame(records)

        # Ordine colonne identico al canonico
        CANONICAL_COLS = [
            "model_id", "dataset_name", "split", "params_M",
            "load_time_s", "latency_mean_ms", "latency_p95_ms", "latency_min_ms",
            "ram_gpu_mb", "mae", "rmse", "device", "dtype", "n_reps",
            "timestamp", "status",
        ]
        for col in CANONICAL_COLS:
            if col not in df.columns:
                df[col] = None
        df = df[CANONICAL_COLS]

        csv_path = OUT_DIR / "benchmark_mae_completion.csv"
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV salvato: {csv_path}")
    except Exception as e:
        logger.error(f"Salvataggio CSV fallito: {e}")
        df = pd.DataFrame()
        csv_path = OUT_DIR / "benchmark_mae_completion.csv"

    # Salva JSON completo
    json_path = OUT_DIR / "benchmark_mae_completion.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)

    # ── Verifica criteri di successo ──────────────────────────────────────────
    all_results = result.get("results", [])
    issues = check_validity(all_results)

    # ── Stampa tabella riassuntiva ────────────────────────────────────────────
    print(f"\n{'='*65}")
    print("MAE COMPLETION — RISULTATI")
    print(f"{'='*65}")
    print(f"  Totale modelli  : {result.get('total', '?')}")
    print(f"  Completati      : {result.get('completed', '?')}")
    print(f"  Successi        : {result.get('successful', '?')}")
    print(f"  Falliti         : {result.get('failed', '?')}")
    print(f"  Tempo run       : {elapsed:.1f}s")
    print(f"  Costo Modal     : ~${cost_usd:.4f}")
    print(f"  CSV             : {csv_path}")

    if not df.empty:
        ok_df = df[df["status"] == "ok"] if "status" in df.columns else df
        print("\n  Risultati MAE:")
        print(f"  {'Modello':<45} {'MAE':>10} {'RMSE':>10} {'p95 ms':>10}")
        print("  " + "-"*80)
        for _, row in ok_df.iterrows():
            mid_short = row["model_id"].split("/")[-1]
            print(f"  {mid_short:<45} {str(row.get('mae','?')):>10} "
                  f"{str(row.get('rmse','?')):>10} {str(row.get('latency_p95_ms','?')):>10}")

    print(f"\n  Verifica criteri:")
    if not issues:
        print("  [OK] Tutti i criteri superati")
    else:
        for iss in issues:
            print(f"  [!!] {iss}")
    print(f"{'='*65}\n")

    # ── Aggiorna MERGE_NOTES con costo reale ─────────────────────────────────
    notes_path = OUT_DIR / "MERGE_NOTES.md"
    if notes_path.exists():
        txt = notes_path.read_text(encoding="utf-8")
        # Sostituisce placeholder costo con valore reale
        txt = txt.replace("COSTO_PLACEHOLDER", f"~${cost_usd:.4f}")
        notes_path.write_text(txt, encoding="utf-8")
        logger.info(f"MERGE_NOTES aggiornato con costo reale: ~${cost_usd:.4f}")

    if issues:
        logger.warning(f"Attenzione: {len(issues)} avviso/i. Verifica MERGE_NOTES.")
        sys.exit(0)   # non fatal — lascia decidere all'utente


if __name__ == "__main__":
    main()
