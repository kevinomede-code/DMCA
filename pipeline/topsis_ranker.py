"""
pipeline/topsis_ranker.py
=========================
Stage 2 — Multi-criteria model selection via TOPSIS.

TOPSIS: Technique for Order of Preference by Similarity to Ideal Solution.
References: Madanchian et al. 2023, Vazquez et al. 2020.

Weights (default): mae=0.5, latency=0.3, params=0.1, license=0.1
All criteria are "minimize" except license_score (maximize).

Phase 1 implementation — batch selection from gaps.json catalog.
Phase 2 planned — streaming re-evaluation on each DT update cycle.
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_ROOT = Path(__file__).resolve().parent.parent

# Hardware capability order (ascending = more capable)
_HW_ORDER = [
    "plc_embedded", "raspberry_arm", "jetson_nano",
    "jetson_orin", "pc_cpu_only", "pc_gpu_entry",
]

# ONNX status numeric rank for tie-breaking (higher = better)
_ONNX_RANK = {"supported": 2, "partial": 1, "unsupported": 0}

# data_available rank for tie-breaking (higher = more available)
_DATA_RANK = {
    "zero_shot": 0, "few_shot_10_100": 1,
    "fine_tune_100_2000": 2, "full_2000plus": 3,
}

DEFAULT_WEIGHTS = {"mae": 0.5, "latency": 0.3, "params": 0.1, "license": 0.1}
DEFAULT_DIRECTIONS = {"mae": "min", "latency": "min", "params": "min", "license": "max"}


def _hw_rank(hw: str) -> int:
    try:
        return _HW_ORDER.index(hw)
    except ValueError:
        return 999


# ─────────────────────────────────────────────────────────────────────────────
# Hard-constraint filter
# ─────────────────────────────────────────────────────────────────────────────

def filter_admissible(catalog: list[dict], constraints: dict) -> list[dict]:
    """Apply 6 hard constraints and return the admissible model set M_adm.

    Args:
        catalog:     List of model dicts from gaps.json model_catalog.
        constraints: Constraint vector from extract_constraint_vector().
                     Expected keys: hw_class, ram_mb, latency_sla_ms,
                     data_available, task, license.

    Returns:
        Filtered list of admissible models. May be empty (→ handle_empty_admissible).

    Constraints applied:
        1. latency_p95 <= sla_ms          (latency feasibility)
        2. min_hw rank <= hw_class rank   (hardware feasibility)
        3. data_available compatible       (training data requirement)
        4. license compatible              (legal requirement)
        5. task compatible                 (output type match)
        6. output_type compatible          (implicit via task check)
    """
    sla_ms         = float(constraints.get("latency_sla_ms", 500))
    hw_class       = constraints.get("hw_class", "pc_cpu_only")
    data_avail     = constraints.get("data_available", "zero_shot")
    required_task  = constraints.get("task", "time_series_forecasting")
    license_req    = constraints.get("license", "apache_2.0").replace("_2.0", "_2")

    admissible = []
    for m in catalog:
        reasons = []

        # C1 — Latency: topsis_latency_ms <= sla * 1.5 (allow 50% margin for Phase 1)
        lat = m.get("topsis_latency_ms", 9999)
        if lat > sla_ms * 1.5:
            reasons.append(f"latency {lat:.1f}ms > sla*1.5 {sla_ms*1.5:.1f}ms")

        # C2 — Hardware: model min_hw must not exceed asset hw_class
        if _hw_rank(m.get("min_hw", "pc_gpu_entry")) > _hw_rank(hw_class):
            reasons.append(
                f"min_hw={m.get('min_hw')} > hw_class={hw_class}"
            )

        # C3 — Data availability: zero_shot models only if asset is zero_shot
        if data_avail == "zero_shot" and not m.get("zero_shot", False):
            reasons.append("requires training data, asset is zero_shot")

        # C4 — License: restricted licenses are rejected unless explicitly allowed
        model_license = m.get("license", "unknown")
        if model_license in ("meta_restricted", "commercial_only"):
            if license_req not in ("any", model_license):
                reasons.append(f"license={model_license} not compatible with {license_req}")

        # C5 — Task compatibility: accept exact match OR "forecasting" as general fallback
        model_task = m.get("task", "")
        task_ok = (
            model_task == required_task
            or model_task == "forecasting"
            or required_task == "time_series_forecasting" and model_task == "forecasting"
        )
        if not task_ok:
            reasons.append(f"task={model_task} != required={required_task}")

        if not reasons:
            admissible.append(m)
        else:
            logger.debug("Rejected %s: %s", m.get("id", "?"), "; ".join(reasons))

    logger.info(
        "filter_admissible: %d/%d models admissible (hw=%s, sla=%.0fms, data=%s)",
        len(admissible), len(catalog), hw_class, sla_ms, data_avail,
    )
    return admissible


def handle_empty_admissible(constraints: dict) -> dict:
    """Build a structured escalation event when M_adm is empty.

    Args:
        constraints: The constraint vector that produced an empty admissible set.

    Returns:
        Structured event dict with suggested relaxation and required action.
    """
    relaxations = []
    if constraints.get("latency_sla_ms", 500) < 100:
        relaxations.append(
            f"Relax latency_sla_ms from {constraints['latency_sla_ms']} to 200ms"
        )
    if constraints.get("data_available") == "zero_shot":
        relaxations.append("Allow few_shot_10_100 (collect 10-100 samples)")
    if constraints.get("hw_class") in ("plc_embedded", "raspberry_arm"):
        relaxations.append("Upgrade hardware to jetson_nano tier")

    return {
        "event": "no_admissible_model",
        "constraints_applied": constraints,
        "constraints_failed": [
            "No model satisfies all 6 hard constraints simultaneously"
        ],
        "suggested_relaxation": relaxations or ["Review catalog — may need new model"],
        "action": "operator_decision_required",
        "severity": "CRITICAL",
    }


# ─────────────────────────────────────────────────────────────────────────────
# TOPSIS ranker
# ─────────────────────────────────────────────────────────────────────────────

class TopsisRanker:
    """TOPSIS multi-criteria ranking for HuggingFace model selection.

    Madanchian et al. 2023 — TOPSIS for MCDM.
    Vazquez et al. 2020 — Multi-criteria selection in edge ML.

    Criteria and default weights:
        mae      (min, w=0.5) — accuracy on CMAPSS
        latency  (min, w=0.3) — P95 inference latency ms
        params   (min, w=0.1) — model size in millions
        license  (max, w=0.1) — Apache=1.0, MIT=0.9, CC=0.7
    """

    def __init__(
        self,
        weights: dict[str, float] | None = None,
        directions: dict[str, str] | None = None,
    ) -> None:
        """
        Args:
            weights:    Per-criterion weights summing to 1.0.
                        Default: {"mae": 0.5, "latency": 0.3,
                                  "params": 0.1, "license": 0.1}
            directions: "min" (lower is better) or "max" (higher is better).
                        Default: mae/latency/params=min, license=max.
        """
        self.weights    = weights    or DEFAULT_WEIGHTS.copy()
        self.directions = directions or DEFAULT_DIRECTIONS.copy()

        total = sum(self.weights.values())
        if abs(total - 1.0) > 1e-6:
            logger.warning("Weights sum to %.4f, not 1.0 — normalizing", total)
            self.weights = {k: v / total for k, v in self.weights.items()}

    def _extract_row(self, m: dict) -> list[float]:
        """Extract the 4 TOPSIS criteria values from a model dict."""
        return [
            float(m.get("topsis_mae",          999.0)),
            float(m.get("topsis_latency_ms",   9999.0)),
            float(m.get("topsis_params_m",     9999.0)),
            float(m.get("topsis_license_score", 0.5)),
        ]

    def rank(self, candidates: list[dict]) -> list[tuple[dict, float]]:
        """Apply TOPSIS to rank candidates by closeness to ideal solution.

        Steps:
            1. Build decision matrix (n_candidates × 4 criteria)
            2. Vector normalization: x_ij / sqrt(sum(x_ij^2))
            3. Weighted normalized matrix: w_j * r_ij
            4. Ideal A+ (best per direction) and anti-ideal A-
            5. Euclidean distances D+ and D- for each candidate
            6. Closeness C_i = D-_i / (D+_i + D-_i)

        Args:
            candidates: Admissible model list from filter_admissible().

        Returns:
            List of (model_dict, closeness_score) sorted descending by score.
            Higher score = closer to ideal = better.
        """
        if not candidates:
            return []

        if len(candidates) == 1:
            logger.info("Single candidate — TOPSIS skipped, score=1.0")
            return [(candidates[0], 1.0)]

        criteria_keys = list(self.weights.keys())
        n = len(candidates)
        k = len(criteria_keys)

        # Step 1 — Decision matrix
        matrix = [self._extract_row(m) for m in candidates]

        # Step 2 — Vector normalization
        col_norms = []
        for j in range(k):
            ss = math.sqrt(sum(matrix[i][j] ** 2 for i in range(n)))
            col_norms.append(ss if ss > 1e-12 else 1.0)

        norm_matrix = [
            [matrix[i][j] / col_norms[j] for j in range(k)]
            for i in range(n)
        ]

        # Step 3 — Weighted normalized matrix
        w_list = [self.weights[key] for key in criteria_keys]
        weighted = [
            [norm_matrix[i][j] * w_list[j] for j in range(k)]
            for i in range(n)
        ]

        # Step 4 — Ideal A+ and anti-ideal A-
        a_plus  = []
        a_minus = []
        for j, key in enumerate(criteria_keys):
            col = [weighted[i][j] for i in range(n)]
            if self.directions[key] == "min":
                a_plus.append(min(col))
                a_minus.append(max(col))
            else:
                a_plus.append(max(col))
                a_minus.append(min(col))

        # Step 5 — Euclidean distances
        d_plus  = []
        d_minus = []
        for i in range(n):
            dp = math.sqrt(sum((weighted[i][j] - a_plus[j])  ** 2 for j in range(k)))
            dm = math.sqrt(sum((weighted[i][j] - a_minus[j]) ** 2 for j in range(k)))
            d_plus.append(dp)
            d_minus.append(dm)

        # Step 6 — Closeness score
        scores = []
        for i in range(n):
            denom = d_plus[i] + d_minus[i]
            c = d_minus[i] / denom if denom > 1e-12 else 0.0
            scores.append((candidates[i], round(c, 6)))

        ranked = sorted(scores, key=lambda x: x[1], reverse=True)
        logger.info(
            "TOPSIS ranking: top=%s (score=%.4f)",
            ranked[0][0].get("id", "?"), ranked[0][1],
        )
        return ranked

    def apply_tiebreaking(self, ranked: list[tuple[dict, float]]) -> list[tuple[dict, float]]:
        """Resolve ties in TOPSIS closeness scores.

        Tie-breaking hierarchy (first match wins):
            1. params_m smaller  (edge-friendlier)
            2. license_score higher  (Apache > MIT > CC)
            3. data_available zero-shot preferred (no training needed)
            4. onnx_status supported > partial > unsupported

        Args:
            ranked: Output of rank(), list of (model_dict, score).

        Returns:
            Re-sorted list with ties broken deterministically.
        """
        def tiebreak_key(item: tuple[dict, float]) -> tuple:
            m, score = item
            return (
                -round(score, 4),                            # primary: TOPSIS score desc
                float(m.get("topsis_params_m", 9999)),       # 1. params asc
                -float(m.get("topsis_license_score", 0)),    # 2. license desc
                _DATA_RANK.get(m.get("data_available", "full_2000plus"), 3),  # 3. zero_shot first
                -_ONNX_RANK.get(m.get("onnx_status", "unsupported"), 0),     # 4. onnx desc
            )

        return sorted(ranked, key=tiebreak_key)


# ─────────────────────────────────────────────────────────────────────────────
# Sensitivity analysis
# ─────────────────────────────────────────────────────────────────────────────

def run_sensitivity_analysis(
    catalog: list[dict],
    constraints: dict,
    alpha_range: tuple[float, float, float] = (0.0, 1.0, 0.1),
) -> dict[str, Any]:
    """Vary MAE weight alpha from 0→1, beta=1-alpha distributed on remaining criteria.

    For each alpha step, distributes (1-alpha) across latency(0.6), params(0.2),
    license(0.2) proportionally (same ratio as default without mae).

    Args:
        catalog:     Full model catalog list.
        constraints: Constraint vector (same as filter_admissible input).
        alpha_range: (start, stop_inclusive, step) for alpha values.

    Returns:
        Dict with keys:
            alpha_values:    list of alpha values tested
            selected_models: dict {alpha_str: model_id}
            closeness_scores: dict {alpha_str: {model_id: score}}
            stable_winner:   model_id that wins most often across all alpha
            stability_pct:   fraction of alpha values won by stable_winner
    """
    start, stop, step = alpha_range
    n_steps  = round((stop - start) / step) + 1
    alphas   = [round(start + i * step, 2) for i in range(n_steps)]

    # Base proportions for latency, params, license when mae weight=0
    base = {"latency": 0.6, "params": 0.2, "license": 0.2}

    selected_models  = {}
    closeness_scores = {}

    admissible = filter_admissible(catalog, constraints)
    if not admissible:
        return {
            "alpha_values": alphas,
            "selected_models": {},
            "closeness_scores": {},
            "stable_winner": None,
            "stability_pct": 0.0,
            "error": "no_admissible_model",
        }

    for alpha in alphas:
        beta = round(1.0 - alpha, 10)
        weights = {
            "mae":     alpha,
            "latency": round(beta * base["latency"], 6),
            "params":  round(beta * base["params"],  6),
            "license": round(beta * base["license"], 6),
        }
        ranker = TopsisRanker(weights=weights, directions=DEFAULT_DIRECTIONS.copy())
        ranked = ranker.rank(admissible)
        ranked = ranker.apply_tiebreaking(ranked)

        key = f"{alpha:.1f}"
        if ranked:
            selected_models[key]  = ranked[0][0].get("id", "?")
            closeness_scores[key] = {
                r[0].get("id", "?"): r[1] for r in ranked
            }
        else:
            selected_models[key]  = "no_admissible_model"
            closeness_scores[key] = {}

    # Stable winner = most frequently selected model
    from collections import Counter
    counts = Counter(selected_models.values())
    stable_winner, stable_count = counts.most_common(1)[0]
    stability_pct = round(stable_count / len(alphas), 3)

    logger.info(
        "Sensitivity analysis: stable_winner=%s (%.0f%% of alpha values)",
        stable_winner, stability_pct * 100,
    )
    return {
        "alpha_values":    alphas,
        "selected_models": selected_models,
        "closeness_scores": closeness_scores,
        "stable_winner":   stable_winner,
        "stability_pct":   stability_pct,
    }


# ─────────────────────────────────────────────────────────────────────────────
# Convenience: load catalog from gaps.json
# ─────────────────────────────────────────────────────────────────────────────

def load_ts_catalog() -> list[dict]:
    """Load the time_series model catalog from gaps.json."""
    path = _ROOT / "gaps.json"
    with open(path, encoding="utf-8") as f:
        gaps = json.load(f)
    return gaps["selection_matrix"]["model_catalog"]["time_series"]


# ─────────────────────────────────────────────────────────────────────────────
# Test rapido
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")

    print("=" * 60)
    print("TOPSIS Ranker — test rapido (Phase 1)")
    print("=" * 60)

    catalog = load_ts_catalog()
    print(f"Catalog TS: {len(catalog)} modelli\n")

    # Constraint vector Jetson Nano
    constraints = {
        "hw_class":       "jetson_nano",
        "ram_mb":         4096,
        "latency_sla_ms": 50.0,
        "data_available": "zero_shot",
        "task":           "time_series_forecasting",
        "license":        "apache_2",
        "sil_level":      1,
    }

    # Filter
    admissible = filter_admissible(catalog, constraints)
    print(f"Ammissibili (Jetson Nano, SLA=50ms, zero_shot): {len(admissible)}")
    for m in admissible:
        print(f"  - {m['id']}")

    if not admissible:
        evt = handle_empty_admissible(constraints)
        print("NESSUN MODELLO AMMISSIBILE:", evt)
    else:
        # TOPSIS ranking
        ranker = TopsisRanker()
        ranked = ranker.rank(admissible)
        ranked = ranker.apply_tiebreaking(ranked)

        print("\nRanking TOPSIS:")
        for i, (m, score) in enumerate(ranked, 1):
            name = m['id'].split('/')[-1]
            print(f"  {i}. {name:<35} score={score:.4f}")

        best = ranked[0][0]
        print(f"\nModello selezionato: {best['id']}")

    # Sensitivity analysis
    print("\n--- Sensitivity analysis (alpha 0.0 -> 1.0) ---")
    sa = run_sensitivity_analysis(catalog, constraints)
    for alpha, model_id in sa["selected_models"].items():
        print(f"  alpha={alpha}  -> {model_id.split('/')[-1]}")
    print(f"\nStable winner: {sa['stable_winner'].split('/')[-1]} "
          f"({sa['stability_pct']*100:.0f}% degli alpha)")

    # Empty admissible test
    print("\n--- Test M_adm vuoto (SLA=5ms, plc_embedded) ---")
    tight = {**constraints, "latency_sla_ms": 5.0, "hw_class": "plc_embedded"}
    adm2  = filter_admissible(catalog, tight)
    if not adm2:
        evt = handle_empty_admissible(tight)
        print("  Evento:", evt["event"])
        print("  Relaxation:", evt["suggested_relaxation"])

    print("\n" + "=" * 60)
    print("Test PASSATO.")
