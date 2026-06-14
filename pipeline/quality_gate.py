"""
pipeline/quality_gate.py
========================
Stage 3 — Pre-deployment quality gate for edge model validation.

Runs 4 sequential checks before a candidate model is deployed to an asset.
Fail-fast: first failing check aborts remaining checks.

Checks:
    1. LATENCY  — P95 inference time <= sla_ms * 1.5
    2. SHAPE    — output tensor shape matches expected
    3. VALIDITY — no NaN/Inf/zeros, no zero-shot collapse (MAE==RMSE)
    4. MEMORY   — peak RAM/VRAM <= ram_budget_mb * 0.85

Phase 1 implementation — synchronous, surrogate model compatible.
Phase 2 planned — async streaming, real HF model inference.
"""

from __future__ import annotations

import logging
import math
import time
from datetime import datetime, timezone
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────────────
# Individual check functions
# ─────────────────────────────────────────────────────────────────────────────

def _check_latency(
    model: Any,
    sample_input: Any,
    sla_ms: float,
    warmup_runs: int,
    test_runs: int,
) -> dict[str, Any]:
    """CHECK 1 — Latency.

    Runs warmup_runs discarded inferences, then test_runs timed ones.
    P95 must be <= sla_ms * 1.5.

    Returns:
        passed, p95_ms, mean_ms, threshold_ms, margin_pct, latencies_ms
    """
    # Warmup
    for _ in range(warmup_runs):
        try:
            _infer(model, sample_input)
        except Exception:
            pass

    latencies = []
    last_err  = None
    for _ in range(test_runs):
        t0 = time.perf_counter()
        try:
            _infer(model, sample_input)
        except Exception as e:
            last_err = e
        latencies.append((time.perf_counter() - t0) * 1000)

    if not latencies:
        return {
            "passed": False,
            "error": f"All inference calls failed: {last_err}",
            "p95_ms": None, "mean_ms": None,
            "threshold_ms": sla_ms * 1.5, "margin_pct": None,
            "latencies_ms": [],
        }

    latencies_sorted = sorted(latencies)
    p95_idx = max(0, int(math.ceil(0.95 * len(latencies_sorted))) - 1)
    p95_ms  = latencies_sorted[p95_idx]
    mean_ms = float(np.mean(latencies))
    threshold_ms = sla_ms * 1.5
    passed   = p95_ms <= threshold_ms
    margin   = round((threshold_ms - p95_ms) / threshold_ms * 100, 2)

    return {
        "passed":       passed,
        "p95_ms":       round(p95_ms, 3),
        "mean_ms":      round(mean_ms, 3),
        "threshold_ms": round(threshold_ms, 3),
        "margin_pct":   margin,
        "latencies_ms": [round(l, 3) for l in latencies],
    }


def _check_shape(
    model: Any,
    sample_input: Any,
    expected_shape: tuple,
) -> dict[str, Any]:
    """CHECK 2 — Output shape.

    Compares actual output shape against expected_shape.
    Tolerates None dimensions (treated as wildcard).

    Returns:
        passed, expected, actual, shape_match_detail
    """
    try:
        output = _infer(model, sample_input)
        actual_shape = _get_shape(output)
    except Exception as e:
        return {
            "passed": False,
            "error": str(e),
            "expected": expected_shape,
            "actual": None,
        }

    # Dimension-wise match (None = wildcard)
    if len(actual_shape) != len(expected_shape):
        passed = False
    else:
        passed = all(
            e is None or a == e
            for a, e in zip(actual_shape, expected_shape)
        )

    return {
        "passed":   passed,
        "expected": expected_shape,
        "actual":   actual_shape,
    }


def _check_validity(
    model: Any,
    sample_input: Any,
) -> dict[str, Any]:
    """CHECK 3 — Output validity.

    Detects:
        - NaN values in output
        - Inf values in output
        - All-zero output (model not predicting)
        - Zero-shot collapse: abs(mae - rmse) < 0.001 (constant prediction)
          This is the DMCA-specific collapse detector for probabilistic models.

    Returns:
        passed, has_nan, has_inf, all_zeros, constant_prediction, values_sample
    """
    try:
        output = _infer(model, sample_input)
        arr    = _to_array(output)
    except Exception as e:
        return {
            "passed": False,
            "error":  str(e),
            "has_nan": None, "has_inf": None,
            "all_zeros": None, "constant_prediction": None,
        }

    has_nan  = bool(np.any(np.isnan(arr)))
    has_inf  = bool(np.any(np.isinf(arr)))
    all_zero = bool(np.all(arr == 0))

    # Zero-shot collapse: MAE≈RMSE on multi-element output → constant prediction.
    # Only meaningful for horizon>1 outputs; single-element outputs are skipped
    # because MAE==RMSE is trivially true for any scalar (not a collapse signal).
    mae  = float(np.mean(np.abs(arr)))
    rmse = float(np.sqrt(np.mean(arr ** 2)))
    constant_pred = arr.size > 1 and abs(mae - rmse) < 0.001 and mae > 0

    passed = not has_nan and not has_inf and not all_zero and not constant_pred

    return {
        "passed":              passed,
        "has_nan":             has_nan,
        "has_inf":             has_inf,
        "all_zeros":           all_zero,
        "constant_prediction": constant_pred,
        "mae":                 round(mae, 6),
        "rmse":                round(rmse, 6),
        "values_sample":       arr.flatten()[:5].tolist(),
    }


def _check_memory(
    ram_budget_mb: float,
    peak_mb_before: float,
    peak_mb_after: float,
) -> dict[str, Any]:
    """CHECK 4 — Peak memory usage.

    Compares peak RAM delta against 85% of budget.
    Phase 1: measures RSS process memory (CPU RAM proxy).
    Phase 2: will use torch.cuda.max_memory_allocated() for GPU VRAM.

    Returns:
        passed, peak_mb, budget_mb, utilization, threshold_mb
    """
    peak_mb      = max(peak_mb_after - peak_mb_before, 0.0)
    threshold_mb = ram_budget_mb * 0.85
    passed       = peak_mb <= threshold_mb
    utilization  = round(peak_mb / ram_budget_mb, 4) if ram_budget_mb > 0 else 0.0

    return {
        "passed":        passed,
        "peak_mb":       round(peak_mb, 2),
        "budget_mb":     round(ram_budget_mb, 2),
        "threshold_mb":  round(threshold_mb, 2),
        "utilization":   utilization,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Main gate function
# ─────────────────────────────────────────────────────────────────────────────

def run_quality_gate(
    model: Any,
    sample_input: Any,
    sla_ms: float,
    expected_shape: tuple,
    ram_budget_mb: float,
    warmup_runs: int = 5,
    test_runs: int = 20,
) -> dict[str, Any]:
    """Run the 4-check quality gate. Fail-fast: stops at first failed check.

    Args:
        model:          Callable model (sklearn, torch.nn.Module, or any with
                        predict/forward/__call__). Must accept sample_input.
        sample_input:   Representative input tensor/array for one inference.
        sla_ms:         Latency SLA in milliseconds (from AAS OperationalData).
        expected_shape: Expected output shape tuple. Use None for wildcard dims.
        ram_budget_mb:  RAM budget in MB (from AAS TechnicalData.ram_budget_mb).
        warmup_runs:    Discarded warm-up inference count (default 5).
        test_runs:      Timed inference count for P95 calculation (default 20).

    Returns:
        {
            gate_passed:       bool,
            failed_checks:     list[str],
            individual_checks: {latency, shape, validity, memory},
            audit_entry:       dict  # append-ready for JSONL audit trail
        }
    """
    failed_checks      = []
    individual_checks  = {}
    ram_before         = _get_ram_mb()

    # ── CHECK 1 — LATENCY ────────────────────────────────────────────────────
    lat = _check_latency(model, sample_input, sla_ms, warmup_runs, test_runs)
    individual_checks["latency"] = lat
    if not lat["passed"]:
        failed_checks.append("latency")
        logger.warning(
            "Quality gate FAIL [LATENCY]: P95=%.1fms > threshold=%.1fms",
            lat.get("p95_ms", -1), lat.get("threshold_ms", -1),
        )
        return _build_result(False, failed_checks, individual_checks, ram_before)

    logger.debug("Quality gate CHECK 1 LATENCY: P95=%.1fms OK", lat["p95_ms"])

    # ── CHECK 2 — SHAPE ──────────────────────────────────────────────────────
    shp = _check_shape(model, sample_input, expected_shape)
    individual_checks["shape"] = shp
    if not shp["passed"]:
        failed_checks.append("shape")
        logger.warning(
            "Quality gate FAIL [SHAPE]: expected=%s actual=%s",
            expected_shape, shp.get("actual"),
        )
        return _build_result(False, failed_checks, individual_checks, ram_before)

    logger.debug("Quality gate CHECK 2 SHAPE: %s OK", shp["actual"])

    # ── CHECK 3 — VALIDITY ───────────────────────────────────────────────────
    val = _check_validity(model, sample_input)
    individual_checks["validity"] = val
    if not val["passed"]:
        reasons = [k for k in ("has_nan", "has_inf", "all_zeros", "constant_prediction")
                   if val.get(k)]
        failed_checks.append("validity")
        logger.warning("Quality gate FAIL [VALIDITY]: %s", reasons)
        return _build_result(False, failed_checks, individual_checks, ram_before)

    logger.debug("Quality gate CHECK 3 VALIDITY: OK")

    # ── CHECK 4 — MEMORY ─────────────────────────────────────────────────────
    ram_after = _get_ram_mb()
    mem = _check_memory(ram_budget_mb, ram_before, ram_after)
    individual_checks["memory"] = mem
    if not mem["passed"]:
        failed_checks.append("memory")
        logger.warning(
            "Quality gate FAIL [MEMORY]: peak=%.1fMB > threshold=%.1fMB",
            mem["peak_mb"], mem["threshold_mb"],
        )
        return _build_result(False, failed_checks, individual_checks, ram_before)

    logger.debug("Quality gate CHECK 4 MEMORY: peak=%.1fMB OK", mem["peak_mb"])
    logger.info("Quality gate PASSED (latency P95=%.1fms, memory=%.1fMB)",
                lat["p95_ms"], mem["peak_mb"])

    return _build_result(True, [], individual_checks, ram_before)


def _build_result(
    passed: bool,
    failed_checks: list[str],
    individual_checks: dict,
    ram_before: float,
) -> dict[str, Any]:
    """Build the standardized gate result dict with audit entry."""
    lat = individual_checks.get("latency", {})
    mem = individual_checks.get("memory", {})

    audit_entry = {
        "timestamp":       datetime.now(timezone.utc).isoformat(),
        "gate_passed":     passed,
        "failed_checks":   failed_checks,
        "p95_latency_ms":  lat.get("p95_ms"),
        "peak_memory_mb":  mem.get("peak_mb"),
        "checks_run":      list(individual_checks.keys()),
    }

    return {
        "gate_passed":      passed,
        "failed_checks":    failed_checks,
        "individual_checks": individual_checks,
        "audit_entry":      audit_entry,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Failure handler
# ─────────────────────────────────────────────────────────────────────────────

def handle_gate_failure(
    candidate_id: str,
    gate_result: dict[str, Any],
    next_candidate: dict | None = None,
) -> dict[str, Any]:
    """Handle a quality gate failure.

    Args:
        candidate_id:   HuggingFace model ID of the failed candidate.
        gate_result:    Output of run_quality_gate().
        next_candidate: Next model dict to try, or None if catalog exhausted.

    Returns:
        {action: "try_next" | "escalate_operator", ...}
    """
    failed = gate_result.get("failed_checks", [])

    if next_candidate is not None:
        logger.info(
            "Gate failure for %s [%s] — trying next candidate: %s",
            candidate_id, failed, next_candidate.get("id", "?"),
        )
        return {
            "action":           "try_next",
            "failed_candidate": candidate_id,
            "failed_checks":    failed,
            "next_candidate":   next_candidate,
            "audit_entry":      gate_result.get("audit_entry"),
        }

    logger.warning(
        "Gate failure for %s [%s] — catalog exhausted, escalating to operator",
        candidate_id, failed,
    )
    return {
        "action":           "escalate_operator",
        "failed_candidate": candidate_id,
        "failed_checks":    failed,
        "reason":           "All candidates failed quality gate",
        "recommended_action": (
            "Review SLA constraints or expand model catalog. "
            "Consider relaxing latency_sla_ms or upgrading hardware tier."
        ),
        "audit_entry": gate_result.get("audit_entry"),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _infer(model: Any, x: Any) -> Any:
    """Call model with x, trying predict → forward → __call__."""
    if hasattr(model, "predict"):
        return model.predict(x)
    if hasattr(model, "forward"):
        import torch
        with torch.no_grad():
            return model.forward(x)
    return model(x)


def _get_shape(output: Any) -> tuple:
    """Extract shape from numpy array, torch tensor, or list."""
    if hasattr(output, "shape"):
        return tuple(output.shape)
    if isinstance(output, (list, tuple)):
        return (len(output),)
    return (1,)


def _to_array(output: Any) -> np.ndarray:
    """Convert model output to flat numpy array for validity checks."""
    if isinstance(output, np.ndarray):
        return output.astype(float)
    try:
        import torch
        if isinstance(output, torch.Tensor):
            return output.detach().cpu().numpy().astype(float)
    except ImportError:
        pass
    return np.array(output, dtype=float)


def _get_ram_mb() -> float:
    """Current process RSS in MB."""
    try:
        import psutil, os
        return psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    except ImportError:
        return 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Test rapido
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
    import json
    from pathlib import Path

    print("=" * 60)
    print("Quality Gate — test rapido (Phase 1)")
    print("=" * 60)

    # ── Build surrogate models for testing ───────────────────────────────────
    from sklearn.linear_model import Ridge
    import numpy as np

    np.random.seed(42)
    X = np.random.randn(200, 20)
    y = np.random.randn(200, 1)
    good_model = Ridge().fit(X, y)

    sample_x   = np.random.randn(1, 20)
    sla_ms     = 50.0
    ram_budget = 4096.0

    # TEST 1 — Gate should PASS
    # Ridge with 1D y returns shape (n_samples,) → expected (1,)
    print("\n[TEST 1] Good surrogate model — expect PASS")
    result = run_quality_gate(
        model=good_model,
        sample_input=sample_x,
        sla_ms=sla_ms,
        expected_shape=(1,),
        ram_budget_mb=ram_budget,
    )
    print(f"  gate_passed={result['gate_passed']}")
    print(f"  latency P95={result['individual_checks']['latency'].get('p95_ms')}ms")
    print(f"  shape actual={result['individual_checks']['shape'].get('actual')}")
    assert result["gate_passed"], "TEST 1 FAILED"
    print("  -> PASS")

    # TEST 2 — Wrong shape
    print("\n[TEST 2] Wrong expected_shape — expect FAIL [shape]")
    result2 = run_quality_gate(
        model=good_model,
        sample_input=sample_x,
        sla_ms=sla_ms,
        expected_shape=(1, 99),   # wrong — Ridge returns (1,) not (1, 99)
        ram_budget_mb=ram_budget,
    )
    print(f"  gate_passed={result2['gate_passed']}, failed={result2['failed_checks']}")
    assert not result2["gate_passed"] and "shape" in result2["failed_checks"]
    print("  -> PASS")

    # TEST 3 — Constant prediction (zero-shot collapse)
    # ConstantModel returns horizon=24 all-same values → MAE==RMSE → collapse
    print("\n[TEST 3] Constant-output model (horizon=24) — expect FAIL [validity]")

    class ConstantModel:
        def predict(self, x):
            return np.full((x.shape[0], 24), 3.14)

    result3 = run_quality_gate(
        model=ConstantModel(),
        sample_input=sample_x,
        sla_ms=sla_ms,
        expected_shape=(1, 24),
        ram_budget_mb=ram_budget,
    )
    print(f"  gate_passed={result3['gate_passed']}, failed={result3['failed_checks']}")
    print(f"  constant_prediction={result3['individual_checks'].get('validity', {}).get('constant_prediction')}")
    assert not result3["gate_passed"] and "validity" in result3["failed_checks"]
    print("  -> PASS")

    # TEST 4 — handle_gate_failure with next candidate
    print("\n[TEST 4] handle_gate_failure with next_candidate")
    next_m = {"id": "amazon/chronos-t5-tiny"}
    failure_resp = handle_gate_failure("ibm/patchtst", result2, next_candidate=next_m)
    print(f"  action={failure_resp['action']}")
    assert failure_resp["action"] == "try_next"
    print("  -> PASS")

    # TEST 5 — handle_gate_failure catalog exhausted
    print("\n[TEST 5] handle_gate_failure catalog exhausted")
    escalate = handle_gate_failure("ibm/patchtst", result2, next_candidate=None)
    print(f"  action={escalate['action']}")
    assert escalate["action"] == "escalate_operator"
    print("  -> PASS")

    print("\n" + "=" * 60)
    print("Tutti i test PASSATI.")
