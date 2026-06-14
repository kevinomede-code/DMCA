"""
Pipeline smoke tests
====================
Defensive checks that every DMCA pipeline module imports cleanly and that the
core public API answers consistently with the canonical results. Intentionally
"smoke + reproducibility" — not exhaustive unit coverage.

Run with:    pytest tests/ -q
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

PIPELINE_MODULES = [
    "aas_parser",
    "topsis_ranker",
    "quality_gate",
    "dmca_drift",
    "realignment",
    "llm_router",
    "generate_plots",
    "modal_jobs",
    "modal_mae_completion",
    "simulation_agent",
]

# Modules that pull in optional heavy stacks (torch, transformers, modal,
# matplotlib, anthropic SDK). When those packages are missing we skip the
# import smoke for that module rather than fail; the goal of the smoke
# suite is to catch *our* SyntaxError / NameError, not missing wheels.
HEAVY_DEPS = {
    "llm_router":            "requests / anthropic",
    "generate_plots":        "matplotlib",
    "modal_jobs":            "modal",
    "modal_mae_completion":  "modal",
    "simulation_agent":      "torch / transformers / huggingface-hub",
}


# ─────────────────────────────────────────────────────────────────────────────
# 1. Import smoke — every module loads without ImportError / SyntaxError
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("modname", PIPELINE_MODULES)
def test_module_imports(modname):
    """Every pipeline module must import cleanly (heavy-dep modules may skip)."""
    try:
        importlib.import_module(f"pipeline.{modname}")
    except ImportError as e:
        if modname in HEAVY_DEPS:
            pytest.skip(
                f"Heavy dependency missing for {modname} "
                f"({HEAVY_DEPS[modname]}): {e}"
            )
        raise


# ─────────────────────────────────────────────────────────────────────────────
# 2. AAS parser (Stage 1)
# ─────────────────────────────────────────────────────────────────────────────

def test_aas_list_assets_has_three_devices():
    from pipeline import aas_parser
    assets = set(aas_parser.list_assets())
    expected = {"jetson_nano", "raspberry_pi_4", "jetson_orin_nx"}
    assert expected.issubset(assets), (
        f"Expected the 3 canonical assets {expected}, got {assets}"
    )


def test_aas_load_and_constraint_vector_jetson_nano():
    """Loading the Jetson Nano AAS and extracting constraints must succeed."""
    from pipeline import aas_parser

    aas = aas_parser.load_aas("jetson_nano")
    assert isinstance(aas, dict) and "submodels" in aas

    cv = aas_parser.extract_constraint_vector(aas)
    expected_keys = {
        "hw_class", "ram_mb", "latency_sla_ms",
        "data_available", "task", "license",
        "sil_level", "requires_approval",
    }
    missing = expected_keys - set(cv.keys())
    assert not missing, f"Constraint vector missing keys: {missing}"
    assert cv["hw_class"] == "jetson_nano"
    assert cv["latency_sla_ms"] > 0
    assert cv["ram_mb"] > 0


# ─────────────────────────────────────────────────────────────────────────────
# 3. TOPSIS — SLA-coherent selection (Stage 2)
# ─────────────────────────────────────────────────────────────────────────────

def test_topsis_catalog_loaded_from_gaps_json():
    from pipeline import topsis_ranker

    catalog = topsis_ranker.load_ts_catalog()
    assert len(catalog) >= 6, f"Expected >=6 TS models, got {len(catalog)}"
    ids = {m["id"] for m in catalog}
    assert "AutonLab/MOMENT-1-large" in ids
    assert "google/timesfm-1.0-200m" in ids
    assert "ibm/patchtst-base-etth1" in ids


def test_topsis_timesfm_excluded_under_nano_sla():
    """TimesFM (2039 ms) must be excluded under a 50 ms SLA — the paradox."""
    from pipeline import aas_parser, topsis_ranker

    cv = aas_parser.extract_constraint_vector(
        aas_parser.load_aas("jetson_nano")
    )
    catalog = topsis_ranker.load_ts_catalog()
    admissible_ids = {m["id"] for m in topsis_ranker.filter_admissible(catalog, cv)}

    assert "google/timesfm-1.0-200m" not in admissible_ids, (
        "TimesFM (2039 ms) must be excluded under the 50 ms Nano SLA"
    )


def test_topsis_ranking_produces_a_top_model():
    """TOPSIS ranking on Nano must produce a non-empty, normalised ranking."""
    from pipeline import aas_parser, topsis_ranker

    cv = aas_parser.extract_constraint_vector(
        aas_parser.load_aas("jetson_nano")
    )
    catalog = topsis_ranker.load_ts_catalog()
    admissible = topsis_ranker.filter_admissible(catalog, cv)

    if not admissible:
        pytest.skip("Empty admissible set — see handle_empty_admissible")

    ranker = topsis_ranker.TopsisRanker()
    ranked = ranker.rank(admissible)
    assert ranked, "TOPSIS rank() returned an empty list on a non-empty input"

    top_model, top_score = ranked[0]
    assert 0.0 <= top_score <= 1.0, f"Closeness {top_score} out of [0,1]"
    assert top_model["id"] in {m["id"] for m in admissible}


# ─────────────────────────────────────────────────────────────────────────────
# 4. DMCA-Drift classifier (Stage 4, v3.1.1)
# ─────────────────────────────────────────────────────────────────────────────

def test_dmca_drift_detector_instantiates_with_default_delta():
    from pipeline import dmca_drift

    det = dmca_drift.DMCADriftDetector(delta=0.002)
    assert det.delta == 0.002
    assert det.window_size > 0


def test_dmca_drift_defines_seven_drift_types():
    from pipeline import dmca_drift

    types = {
        dmca_drift.ABRUPT, dmca_drift.GRADUAL, dmca_drift.INCREMENTAL,
        dmca_drift.VARIANCE_SHIFT, dmca_drift.DISTRIBUTION_SHIFT,
        dmca_drift.OUTLIER_DRIVEN, dmca_drift.UNCLASSIFIED,
    }
    assert len(types) == 7, "Drift classifier must expose exactly 7 types"


def test_dmca_drift_no_swap_set_is_correct():
    """variance_shift and outlier_driven are the documented no-swap types."""
    from pipeline import dmca_drift

    assert dmca_drift.VARIANCE_SHIFT in dmca_drift.NO_SWAP_TYPES
    assert dmca_drift.OUTLIER_DRIVEN in dmca_drift.NO_SWAP_TYPES
    assert dmca_drift.GRADUAL not in dmca_drift.NO_SWAP_TYPES
    assert dmca_drift.ABRUPT not in dmca_drift.NO_SWAP_TYPES


# ─────────────────────────────────────────────────────────────────────────────
# 5. Canonical results — regression guards
#    These files must stay byte-stable; tests fail loudly if anyone edits them.
# ─────────────────────────────────────────────────────────────────────────────

def test_canonical_drift_cycle_results_intact():
    """The canonical drift_cycle_results.json keeps its key invariants."""
    p = ROOT / "results" / "drift_experiments" / "drift_cycle_results.json"
    assert p.is_file(), f"Canonical drift cycle file missing: {p}"
    data = json.loads(p.read_text(encoding="utf-8"))

    assert data["dataset"] == "CMAPSS_FD001"
    assert data["sensor_channel"] == "s2"
    assert data["detection_index"] == 1380
    assert abs(data["threshold"] - 1.991843) < 1e-5
    assert data["new_model_selected"] == "amazon/chronos-t5-tiny"
    assert len(data["mae_series_sample"]) == 20


def test_canonical_benchmark_csv_intact():
    """The canonical benchmark CSV keeps its 8 models."""
    p = ROOT / "results" / "benchmarks" / "2026-04-07" / "benchmark_results_modal.csv"
    assert p.is_file(), f"Canonical benchmark CSV missing: {p}"
    text = p.read_text(encoding="utf-8")
    for must_contain in (
        "google/timesfm-1.0-200m",
        "AutonLab/MOMENT-1-large",
        "ibm/patchtst-base-etth1",
        "amazon/chronos-t5-tiny",
        "Salesforce/moirai-1.1-R-small",
        "Salesforce/moirai-1.1-R-large",
        "amazon/chronos-t5-large",
        "time-series-foundation-models/Lag-Llama",
    ):
        assert must_contain in text, f"Canonical row missing: {must_contain}"
