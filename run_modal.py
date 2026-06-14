"""
run_modal.py
============
Script locale per lanciare gli esperimenti su Modal GPU cloud.
Chiama le funzioni remote definite in pipeline/modal_jobs.py.

Uso (PowerShell / terminale Windows):
    python run_modal.py --job benchmark
    python run_modal.py --job drift
    python run_modal.py --job dmca
    python run_modal.py --job all

Prerequisiti:
    pip install modal
    python -m modal setup          # autentica l'account Modal
    python -m modal secret create thesis-secrets \
        ANTHROPIC_API_KEY=sk-ant-... \
        HF_TOKEN=hf_...
    python -m modal deploy pipeline/modal_jobs.py
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# ─── Setup path per importare dal progetto ────────────────────────────────────
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

# ─── Loguru ───────────────────────────────────────────────────────────────────
from loguru import logger

TODAY = datetime.now().strftime("%Y-%m-%d")
LOG_DIR = ROOT / "results" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", colorize=True,
           format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}")
logger.add(str(LOG_DIR / f"modal_jobs_{TODAY}.log"), level="DEBUG")

# ─── Cartelle output locali ───────────────────────────────────────────────────
BENCH_DIR = ROOT / "results" / "benchmarks" / TODAY
DRIFT_DIR = ROOT / "results" / "drift_experiments"
BENCH_DIR.mkdir(parents=True, exist_ok=True)
DRIFT_DIR.mkdir(parents=True, exist_ok=True)


# ─── Leggi modelli da gaps.json ───────────────────────────────────────────────

def load_models_from_gaps() -> list[str]:
    """Estrae tutti i model_id dal catalog time_series in gaps.json."""
    gaps_path = ROOT / "gaps.json"
    try:
        with open(gaps_path, encoding="utf-8") as f:
            gaps = json.load(f)
        ts_models = gaps["selection_matrix"]["model_catalog"]["time_series"]
        model_ids = [m["id"] for m in ts_models]
        logger.info(f"Modelli da gaps.json: {model_ids}")
        return model_ids
    except Exception as e:
        logger.error(f"Impossibile leggere gaps.json: {e}")
        return [
            "amazon/chronos-t5-tiny",
            "amazon/chronos-t5-large",
            "ibm/patchtst-base-etth1",
            "Salesforce/moirai-1.1-R-small",
        ]


# ─── Stima costi ─────────────────────────────────────────────────────────────

def estimate_cost(job: str, duration_s: float) -> str:
    """Stima costo Modal basandosi su durata effettiva."""
    rates = {"t4": 0.59 / 3600, "a10g": 1.10 / 3600, "cpu": 0.05 / 3600}
    gpu_map = {"benchmark": "t4", "drift": "t4", "dmca": "t4", "finetune": "a10g", "all": "t4"}
    gpu  = gpu_map.get(job, "t4")
    cost = rates[gpu] * duration_s
    return f"~${cost:.4f} (GPU {gpu.upper()}, {duration_s:.1f}s)"


# ══════════════════════════════════════════════════════════════════════════════
# JOB: benchmark
# ══════════════════════════════════════════════════════════════════════════════

def job_benchmark() -> bool:
    """Lancia run_benchmark_suite su Modal e scarica i risultati."""
    logger.info("=" * 60)
    logger.info("JOB: Benchmark suite su Modal GPU T4")
    logger.info("=" * 60)

    try:
        import modal
    except ImportError as e:
        logger.error(f"Import Modal fallito: {e}")
        return False

    run_benchmark_suite = modal.Function.from_name("thesis-research", "run_benchmark_suite")

    models   = load_models_from_gaps()
    datasets = [
        "LucasThil/nasa_turbofan_degradation_FD001",
        "ETDataset/ett",
    ]

    logger.info(f"Modelli: {models}")
    logger.info(f"Dataset: {datasets}")
    logger.info(f"Job paralleli: {len(models) * len(datasets)}")

    t0 = time.perf_counter()
    try:
        result = run_benchmark_suite.remote(models=models, datasets=datasets)
    except Exception as e:
        logger.error(f"run_benchmark_suite.remote() fallito: {e}")
        return False

    elapsed  = time.perf_counter() - t0
    cost_str = estimate_cost("benchmark", elapsed)
    logger.info(f"Suite completata in {elapsed:.1f}s | Costo stimato: {cost_str}")

    try:
        import pandas as pd
        records = result.get("dataframe_dict") or result.get("results", [])
        if records:
            df = pd.DataFrame(records)
            csv_path = BENCH_DIR / "benchmark_results_modal.csv"
            df.to_csv(csv_path, index=False)
            logger.info(f"CSV salvato: {csv_path}")
            print(f"\n{'='*55}\nBENCHMARK COMPLETATO\n{'='*55}")
            print(f"  Successi      : {result.get('successful', '?')}/{result.get('total_jobs', '?')}")
            print(f"  CSV locale    : {csv_path}")
            print(f"  Costo stimato : {cost_str}\n{'='*55}\n")
            ok = df[df.get("status") == "ok"] if "status" in df.columns else df
            if not ok.empty:
                cols = ["model_id", "dataset_name", "latency_mean_ms", "latency_p95_ms",
                        "ram_gpu_mb", "params_M"]
                print(ok[[c for c in cols if c in ok.columns]].to_string(index=False))

        json_path = BENCH_DIR / "benchmark_results_modal.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"JSON completo salvato: {json_path}")
    except Exception as e:
        logger.error(f"Salvataggio risultati fallito: {e}")
        return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
# JOB: drift
# ══════════════════════════════════════════════════════════════════════════════

def job_drift() -> bool:
    """Lancia run_drift_simulation su Modal e scarica risultati."""
    logger.info("=" * 60)
    logger.info("JOB: Drift simulation su Modal GPU T4")
    logger.info("=" * 60)

    try:
        import modal
    except ImportError:
        return False

    run_drift_simulation = modal.Function.from_name("thesis-research", "run_drift_simulation")

    t0 = time.perf_counter()
    try:
        result = run_drift_simulation.remote(
            dataset_name="LucasThil/nasa_turbofan_degradation_FD001",
            subset="train",
            drift_factor_max=2.0,
            detection_threshold_sigma=2.0,
        )
    except Exception as e:
        logger.error(f"run_drift_simulation.remote() fallito: {e}")
        return False

    elapsed  = time.perf_counter() - t0
    cost_str = estimate_cost("drift", elapsed)

    try:
        json_path = DRIFT_DIR / f"drift_cycle_results_modal_{TODAY}.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Drift results: {json_path}")

        print(f"\n{'='*55}\nDRIFT SIMULATION COMPLETATA\n{'='*55}")
        print(f"  MAE baseline    : {result.get('accuracy_baseline')}")
        print(f"  MAE drift       : {result.get('accuracy_drift')}")
        print(f"  MAE post-rec.   : {result.get('accuracy_post_recovery')}")
        print(f"  Detection step  : {result.get('detection_timestep')}")
        print(f"  Recovery time   : {result.get('recovery_time_ms')} ms")
        print(f"  Improvement     : {result.get('accuracy_improvement_pct')} %")
        print(f"  Costo stimato   : {cost_str}\n{'='*55}\n")
    except Exception as e:
        logger.error(f"Salvataggio drift results fallito: {e}")
        return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
# JOB: dmca — ciclo DMCA integration test completo (Stage 1-5)
# ══════════════════════════════════════════════════════════════════════════════

def job_dmca() -> bool:
    """
    Lancia run_dmca_integration_test su Modal GPU T4.
    Dataset: ETDataset/ett (ETT-h1, 17420 pt, serie OT continua).
    MOMENT baseline MAE canonico = 1.710 (benchmark T4 2026-04-07).
    Salva: results/drift_experiments/dmca_integration_ett_<today>.json
    Costo stimato: ~$0.20–0.25
    """
    logger.info("=" * 60)
    logger.info("JOB: DMCA Integration Test su Modal GPU T4 — ETT-h1")
    logger.info("=" * 60)

    try:
        import modal
    except ImportError as e:
        logger.error(f"Import Modal fallito: {e}")
        return False

    run_dmca = modal.Function.from_name(
        "thesis-research", "run_dmca_integration_test"
    )

    t0 = time.perf_counter()
    try:
        result = run_dmca.remote(
            dataset_name="ETDataset/ett",
            drift_factor=1.5,
            sla_ms=100.0,
            improvement_threshold=0.05,
            enable_copilot=True,
        )
    except Exception as e:
        logger.error(f"run_dmca_integration_test.remote() fallito: {e}")
        return False

    elapsed  = time.perf_counter() - t0
    cost_str = estimate_cost("dmca", elapsed)
    logger.info(f"DMCA integration test in {elapsed:.1f}s | Costo: {cost_str}")

    try:
        out_path = DRIFT_DIR / f"dmca_integration_ett_{TODAY}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Risultati DMCA (ETT): {out_path}")

        # ── Riepilogo sintetico ───────────────────────────────────────────────
        print(f"\n{'='*60}")
        print("DMCA INTEGRATION TEST (ETT-h1) — RISULTATI")
        print(f"{'='*60}")
        print(f"  Status           : {result.get('status')}")
        print(f"  Swap eseguito    : {result.get('swap_executed')}")
        print(f"  M_curr iniziale  : {result.get('m_curr_initial','').split('/')[-1]}")
        print(f"  M_new selezionato: {result.get('m_new_selected','').split('/')[-1]}")
        print(f"  Drift type       : {result.get('drift_type')}")
        print(f"  Detection idx    : {result.get('detection_idx')}")
        print(f"  MAE baseline     : {result.get('mae_baseline')}")
        print(f"  MAE at detection : {result.get('mae_at_detection')}")
        print(f"  MAE shadow       : {result.get('mae_shadow')}")
        print(f"  ΔΔ MAE           : {result.get('delta_mae_pct')} %")
        print(f"  Lat shadow mean  : {result.get('latency_shadow_mean_ms')} ms")
        print(f"  TOPSIS scores    : {result.get('topsis_scores')}")
        print(f"  Quality Gate     : {result.get('quality_gate')}")
        print(f"  Copilot confirm  : {result.get('copilot_confirm')} (SIL={result.get('sil_level')})")
        print(f"  Durata ciclo     : {elapsed:.1f}s")
        print(f"  Costo stimato    : {cost_str}")
        print(f"  JSON locale      : {out_path}")

        # ── Copilot alert verbatim ────────────────────────────────────────────
        if result.get("copilot_alert"):
            print(f"\n  --- COPILOT ALERT (L1/Haiku) VERBATIM ---")
            print(f"  {result['copilot_alert']}")
            print(f"  -----------------------------------------")
        else:
            print(f"\n  [Copilot alert: N/A o credito esaurito]")

        # ── Timestamp swap dall'audit entry ──────────────────────────────────
        ae = result.get("audit_entry", {})
        print(f"\n  --- AUDIT ENTRY ---")
        print(f"  Event            : {ae.get('event')}")
        print(f"  Swap timestamp   : {ae.get('timestamp')}")
        print(f"  M_curr → M_new   : {ae.get('m_curr','').split('/')[-1]} → {ae.get('m_new','').split('/')[-1]}")
        print(f"  Drift type       : {ae.get('drift_type')}")
        print(f"  MAE baseline     : {ae.get('mae_baseline')}")
        print(f"  MAE at detection : {ae.get('mae_at_detection')}")
        print(f"  MAE shadow       : {ae.get('mae_shadow')}")
        print(f"  Delta MAE        : {ae.get('delta_mae')}")
        print(f"  TOPSIS scores    : {ae.get('topsis_scores')}")
        print(f"  QG pass          : {ae.get('qg_pass')}")
        print(f"  SIL level        : {ae.get('sil_level')}")
        print(f"  -------------------")

        print(f"{'='*60}\n")

        # ── Log Stage-by-Stage completo ───────────────────────────────────────
        if result.get("log"):
            print("  --- DMCA AUDIT LOG (Stage-by-Stage) ---")
            for entry in result["log"]:
                print(f"  {entry}")
            print("  ----------------------------------------\n")

    except Exception as e:
        logger.error(f"Salvataggio DMCA results fallito: {e}")
        return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
# JOB: dmca-seeds — 3 run sequenziali seed=0,1,2 su ETT-h1
# ══════════════════════════════════════════════════════════════════════════════

def job_dmca_seeds() -> bool:
    """
    Lancia run_dmca_integration_test × 3 su ETT-h1 con seed=0,1,2.
    Sequenziale (non parallelo) per evitare conflitti T4 concorrenti.

    Output per-seed:
      results/drift_experiments/dmca_ett_seed{s}_<date>.json

    Output summary:
      results/drift_experiments/dmca_ett_summary_<date>.json
      Campi: detection_idx, drift_type, mae_baseline, mae_at_detection,
             swap_executed, swap_trigger per ciascun seed + varianza MAE baseline.
    """
    logger.info("=" * 60)
    logger.info("JOB: DMCA multi-seed (seed=0,1,2) su ETT-h1")
    logger.info("=" * 60)

    try:
        import modal
    except ImportError as e:
        logger.error(f"Import Modal fallito: {e}")
        return False

    run_dmca = modal.Function.from_name(
        "thesis-research", "run_dmca_integration_test"
    )

    SEEDS      = [0, 1, 2]
    per_seed:  list[dict] = []
    all_ok     = True

    for s in SEEDS:
        logger.info(f"--- Lancio seed={s} ---")
        t0 = time.perf_counter()
        try:
            result = run_dmca.remote(
                dataset_name="ETDataset/ett",
                drift_factor=1.5,
                sla_ms=100.0,
                improvement_threshold=0.05,
                enable_copilot=True,
                seed=s,
            )
        except Exception as e:
            logger.error(f"seed={s} fallito: {e}")
            all_ok = False
            per_seed.append({"seed": s, "error": str(e)})
            continue

        elapsed  = time.perf_counter() - t0
        cost_str = estimate_cost("dmca", elapsed)
        logger.info(f"seed={s} completato in {elapsed:.1f}s | {cost_str}")

        # ── Salva JSON per-seed ───────────────────────────────────────────────
        seed_path = DRIFT_DIR / f"dmca_ett_seed{s}_{TODAY}.json"
        try:
            with open(seed_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Salvato: {seed_path}")
        except Exception as e:
            logger.error(f"Salvataggio seed={s} fallito: {e}")
            all_ok = False

        # ── Stampa risultati seed ─────────────────────────────────────────────
        ae = result.get("audit_entry", {})
        print(f"\n{'='*55}")
        print(f"SEED {s} — {result.get('status', 'unknown').upper()}")
        print(f"{'='*55}")
        print(f"  Drift type       : {result.get('drift_type')}")
        print(f"  Detection idx    : {result.get('detection_idx')}")
        print(f"  MAE baseline     : {result.get('mae_baseline')}")
        print(f"  MAE at detection : {result.get('mae_at_detection')}")
        print(f"  Swap trigger     : {result.get('swap_trigger')}")
        print(f"  Swap eseguito    : {result.get('swap_executed')}")
        print(f"  M_new            : {result.get('m_new_selected','').split('/')[-1]}")
        print(f"  Lat shadow ms    : {result.get('latency_shadow_mean_ms')}")
        print(f"  Durata           : {elapsed:.1f}s | {cost_str}")
        if result.get("copilot_alert"):
            print(f"  Copilot alert    : {result['copilot_alert'][:120]}...")
        if result.get("log"):
            print(f"  --- Stage log ---")
            for entry in result["log"]:
                print(f"  {entry}")
        print(f"{'='*55}")

        # ── Accumula per summary ──────────────────────────────────────────────
        per_seed.append({
            "seed":             s,
            "status":           result.get("status"),
            "drift_type":       result.get("drift_type"),
            "detection_idx":    result.get("detection_idx"),
            "mae_baseline":     result.get("mae_baseline"),
            "mae_at_detection": result.get("mae_at_detection"),
            "swap_executed":    result.get("swap_executed"),
            "swap_trigger":     result.get("swap_trigger"),
            "m_new_selected":   result.get("m_new_selected"),
            "latency_shadow_ms": result.get("latency_shadow_mean_ms"),
            "elapsed_s":        round(elapsed, 1),
        })

    # ── Summary cross-seed ────────────────────────────────────────────────────
    import numpy as _np_sum
    mae_baselines   = [r["mae_baseline"]     for r in per_seed if r.get("mae_baseline")     is not None]
    mae_detections  = [r["mae_at_detection"] for r in per_seed if r.get("mae_at_detection") is not None]
    det_idxs        = [r["detection_idx"]    for r in per_seed if r.get("detection_idx")    is not None]

    summary = {
        "date":                TODAY,
        "dataset":             "ETDataset/ett (ETT-h1)",
        "drift_factor":        1.5,
        "seeds":               SEEDS,
        "per_seed":            per_seed,
        "variance": {
            "mae_baseline_mean":  round(float(_np_sum.mean(mae_baselines)),  6) if mae_baselines  else None,
            "mae_baseline_std":   round(float(_np_sum.std(mae_baselines)),   6) if mae_baselines  else None,
            "mae_detection_mean": round(float(_np_sum.mean(mae_detections)), 6) if mae_detections else None,
            "mae_detection_std":  round(float(_np_sum.std(mae_detections)),  6) if mae_detections else None,
            "detection_idx_mean": round(float(_np_sum.mean(det_idxs)),       1) if det_idxs       else None,
            "detection_idx_std":  round(float(_np_sum.std(det_idxs)),        1) if det_idxs       else None,
        },
        "swap_triggers":       [r.get("swap_trigger") for r in per_seed],
        "drift_types":         [r.get("drift_type")   for r in per_seed],
        "all_swapped":         all(r.get("swap_executed") for r in per_seed if "swap_executed" in r),
    }

    summary_path = DRIFT_DIR / f"dmca_ett_summary_{TODAY}.json"
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Summary salvato: {summary_path}")
    except Exception as e:
        logger.error(f"Salvataggio summary fallito: {e}")
        all_ok = False

    # ── Stampa summary finale ─────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("DMCA MULTI-SEED SUMMARY (seed=0,1,2 — ETT-h1)")
    print(f"{'='*60}")
    print(f"  {'Seed':<6} {'DriftType':<22} {'DetIdx':<10} {'MAE_base':<12} {'MAE_det':<12} {'Trigger':<32} {'Swap'}")
    print(f"  {'-'*6} {'-'*22} {'-'*10} {'-'*12} {'-'*12} {'-'*32} {'-'*5}")
    for r in per_seed:
        if "error" in r:
            print(f"  {r['seed']:<6} ERROR: {r['error']}")
            continue
        print(
            f"  {r['seed']:<6} "
            f"{str(r.get('drift_type','?')):<22} "
            f"{str(r.get('detection_idx','?')):<10} "
            f"{str(r.get('mae_baseline','?')):<12} "
            f"{str(r.get('mae_at_detection','?')):<12} "
            f"{str(r.get('swap_trigger','?')):<32} "
            f"{str(r.get('swap_executed','?'))}"
        )
    v = summary["variance"]
    print(f"\n  MAE baseline : {v['mae_baseline_mean']} ± {v['mae_baseline_std']}")
    print(f"  MAE detect.  : {v['mae_detection_mean']} ± {v['mae_detection_std']}")
    print(f"  Detect. idx  : {v['detection_idx_mean']} ± {v['detection_idx_std']}")
    print(f"  All swapped  : {summary['all_swapped']}")
    print(f"  Summary JSON : {summary_path}")
    print(f"{'='*60}\n")

    return all_ok


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lancia esperimenti GPU su Modal per thesis-research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi:
  python run_modal.py --job benchmark    # benchmark tutti i modelli su T4
  python run_modal.py --job drift        # simulazione drift (Ridge) su T4
  python run_modal.py --job dmca         # ciclo DMCA completo Stage 1-5
  python run_modal.py --job dmca-seeds   # 3 run seed=0,1,2 su ETT-h1 + summary
  python run_modal.py --job all          # benchmark + drift in sequenza

Prerequisiti:
  pip install modal
  python -m modal setup
  python -m modal secret create thesis-secrets ANTHROPIC_API_KEY=... HF_TOKEN=...
  python -m modal deploy pipeline/modal_jobs.py
        """,
    )
    parser.add_argument(
        "--job",
        choices=["benchmark", "drift", "dmca", "dmca-seeds", "all"],
        default="all",
        help="Job da eseguire (default: all)",
    )
    args = parser.parse_args()

    try:
        import modal
        logger.info(f"Modal SDK: {modal.__version__}")
    except ImportError:
        logger.error("Modal non installato. Esegui: pip install modal")
        sys.exit(1)

    t_total = time.perf_counter()
    results: dict[str, bool] = {}

    if args.job in ("benchmark", "all"):
        results["benchmark"] = job_benchmark()

    if args.job in ("drift", "all"):
        results["drift"] = job_drift()

    if args.job in ("dmca",):
        results["dmca"] = job_dmca()

    if args.job in ("dmca-seeds",):
        results["dmca-seeds"] = job_dmca_seeds()

    elapsed_total = time.perf_counter() - t_total
    print(f"\n{'='*55}\nRIEPILOGO FINALE\n{'='*55}")
    for job_name, ok in results.items():
        print(f"  {job_name:15} : {'OK' if ok else 'FALLITO'}")
    print(f"  Tempo totale   : {elapsed_total:.1f}s")
    print(f"  Log completo   : {LOG_DIR}/modal_jobs_{TODAY}.log")
    print(f"{'='*55}\n")

    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
