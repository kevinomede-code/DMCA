"""
pipeline/aas_parser.py
======================
Stage 1 — AAS Type 1 parser (file-based JSON, no BaSyx SDK).

Carica, valida e aggiorna i file AAS JSON in assets/.
Il Digital Twin è rappresentato come file JSON statico (Phase 1).
Phase 2 prevede un AAS Type 2 servito via FastAPI REST (BaSyx planned).

Schema IEC 63278 semplificato:
    asset_id, asset_type, submodels → {TechnicalData, OperationalData,
    Capabilities, DeploymentState, SafetyClassification}
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Root del progetto: due livelli sopra pipeline/
_ROOT = Path(__file__).resolve().parent.parent
_ASSETS_DIR = _ROOT / "assets"


# ─────────────────────────────────────────────────────────────────────────────
# Caricamento
# ─────────────────────────────────────────────────────────────────────────────

def load_aas(asset_id: str) -> dict[str, Any]:
    """Carica e valida l'AAS JSON per l'asset indicato.

    Args:
        asset_id: Identificatore dell'asset (es. "jetson_nano").
                  Il file cercato sarà assets/{asset_id}.aas.json.

    Returns:
        Dizionario AAS completo.

    Raises:
        FileNotFoundError: Se il file AAS non esiste.
        ValueError: Se la struttura JSON è incompleta o malformata.
    """
    path = _ASSETS_DIR / f"{asset_id}.aas.json"
    if not path.exists():
        raise FileNotFoundError(
            f"AAS non trovato: {path}. "
            f"Verifica che assets/{asset_id}.aas.json esista."
        )

    with open(path, encoding="utf-8") as f:
        try:
            aas = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"AAS malformato ({path}): {exc}") from exc

    _validate_aas(aas, asset_id)
    logger.debug("AAS caricato: %s", asset_id)
    return aas


def _validate_aas(aas: dict, asset_id: str) -> None:
    """Verifica che i submodel obbligatori siano presenti."""
    required_submodels = {
        "TechnicalData", "OperationalData", "Capabilities",
        "DeploymentState", "SafetyClassification",
    }
    submodels = aas.get("submodels", {})
    missing = required_submodels - set(submodels.keys())
    if missing:
        raise ValueError(
            f"AAS {asset_id}: submodel mancanti → {missing}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# Estrazione constraint vector
# ─────────────────────────────────────────────────────────────────────────────

def extract_constraint_vector(aas: dict[str, Any]) -> dict[str, Any]:
    """Estrae il constraint vector dai submodel dell'AAS.

    Il constraint vector è l'input della Stage 2 (TOPSIS ranker).
    Aggrega i campi rilevanti da TechnicalData, OperationalData,
    Capabilities e SafetyClassification.

    Args:
        aas: Dizionario AAS completo (output di load_aas).

    Returns:
        Dizionario con le chiavi:
            hw_class          (str)  — classe hardware per HW_ORDER
            ram_mb            (int)  — budget RAM in MB
            has_gpu           (bool)
            gpu_vram_mb       (int)  — 0 se no GPU
            latency_sla_ms    (float)— SLA latenza in ms
            data_available    (str)  — "zero_shot" | "few_shot_10_100" | ...
            task              (str)  — tipo task
            license           (str)  — requisito licenza
            sil_level         (int)  — Safety Integrity Level
            requires_approval (bool) — se serve approvazione operatore
    """
    sub = aas["submodels"]
    td  = sub["TechnicalData"]
    od  = sub["OperationalData"]
    cap = sub["Capabilities"]
    saf = sub["SafetyClassification"]

    return {
        "hw_class":          td.get("hw_class", "pc_cpu_only"),
        "ram_mb":            int(td.get("ram_budget_mb", 0)),
        "has_gpu":           bool(td.get("has_gpu", False)),
        "gpu_vram_mb":       int(td.get("gpu_vram_mb", 0)),
        "latency_sla_ms":    float(od.get("latency_sla_ms", 500)),
        "data_available":    cap.get("data_available", "zero_shot"),
        "task":              cap.get("task", "time_series_forecasting"),
        "license":           cap.get("license_requirement", "apache_2.0"),
        "sil_level":         int(saf.get("SIL_level", 1)),
        "requires_approval": bool(saf.get("requires_human_approval", True)),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Aggiornamento DeploymentState
# ─────────────────────────────────────────────────────────────────────────────

def update_aas_deployment_state(asset_id: str, updates: dict[str, Any]) -> None:
    """Aggiorna i campi di DeploymentState nel file AAS JSON.

    Operazione atomica: legge → modifica in memoria → riscrive.
    Se `updates` contiene la chiave "drift_event", quella viene
    appesa a drift_history invece di sovrascrivere il campo.

    Args:
        asset_id: Identificatore asset (es. "jetson_nano").
        updates:  Dizionario con i campi da aggiornare in DeploymentState.
                  Chiave speciale "drift_event" → appende a drift_history.

    Raises:
        FileNotFoundError: Se l'AAS non esiste.
        ValueError: Se l'AAS è malformato.
    """
    aas = load_aas(asset_id)
    ds  = aas["submodels"]["DeploymentState"]

    drift_event = updates.pop("drift_event", None)

    for key, value in updates.items():
        ds[key] = value

    if drift_event is not None:
        if not isinstance(ds.get("drift_history"), list):
            ds["drift_history"] = []
        drift_event.setdefault(
            "timestamp", datetime.now(timezone.utc).isoformat()
        )
        ds["drift_history"].append(drift_event)

    _write_aas(asset_id, aas)
    logger.info("DeploymentState aggiornato: %s → %s", asset_id, list(updates.keys()))


def update_aas_drift_history(asset_id: str, drift_event: dict[str, Any]) -> None:
    """Appende un drift event a DeploymentState.drift_history.

    Il campo timestamp viene aggiunto automaticamente se assente.

    Args:
        asset_id:    Identificatore asset.
        drift_event: Dizionario con i campi dell'evento di drift.
                     Campi raccomandati: type, severity, mae_at_detection,
                     detected_at_timestep, new_model_candidate.
    """
    aas = load_aas(asset_id)
    ds  = aas["submodels"]["DeploymentState"]

    if not isinstance(ds.get("drift_history"), list):
        ds["drift_history"] = []

    drift_event.setdefault(
        "timestamp", datetime.now(timezone.utc).isoformat()
    )
    ds["drift_history"].append(drift_event)

    _write_aas(asset_id, aas)
    logger.info(
        "drift_history aggiornata: %s — tipo=%s",
        asset_id, drift_event.get("type", "unknown"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# I/O helper
# ─────────────────────────────────────────────────────────────────────────────

def _write_aas(asset_id: str, aas: dict[str, Any]) -> None:
    """Riscrive il file AAS JSON in modo atomico (write + rename)."""
    path = _ASSETS_DIR / f"{asset_id}.aas.json"
    tmp  = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(aas, f, indent=2, ensure_ascii=False)
    tmp.replace(path)


# ─────────────────────────────────────────────────────────────────────────────
# Utility: lista asset disponibili
# ─────────────────────────────────────────────────────────────────────────────

def list_assets() -> list[str]:
    """Ritorna la lista degli asset_id disponibili in assets/."""
    return [p.stem.replace(".aas", "") for p in _ASSETS_DIR.glob("*.aas.json")]


# ─────────────────────────────────────────────────────────────────────────────
# Test rapido
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s | %(message)s")

    print("=" * 55)
    print("AAS Parser — test rapido (Phase 1)")
    print("=" * 55)

    assets = list_assets()
    print(f"Asset disponibili: {assets}\n")

    # Test su jetson_nano
    aas = load_aas("jetson_nano")
    cv  = extract_constraint_vector(aas)

    print("Constraint vector — jetson_nano:")
    for k, v in cv.items():
        print(f"  {k:<22} = {v}")

    # Test update DeploymentState
    print("\nTest update_aas_deployment_state...")
    update_aas_deployment_state("jetson_nano", {
        "active_model": "amazon/chronos-t5-tiny",
        "deployed_at":  datetime.now(timezone.utc).isoformat(),
        "format_used":  "pytorch",
        "quality_gate_passed": True,
        "baseline_mae": 0.796,
        "baseline_latency_p95_ms": 203.1,
        "baseline_memory_peak_mb": 45.0,
    })
    print("  DeploymentState aggiornato. Verifica assets/jetson_nano.aas.json")

    # Test append drift_history
    print("\nTest update_aas_drift_history...")
    update_aas_drift_history("jetson_nano", {
        "type":                  "gradual",
        "severity":              "HIGH",
        "mae_at_detection":      3.121,
        "detected_at_timestep":  1380,
        "new_model_candidate":   "amazon/chronos-t5-tiny",
    })

    aas2 = load_aas("jetson_nano")
    hist = aas2["submodels"]["DeploymentState"]["drift_history"]
    print(f"  drift_history entries: {len(hist)}")
    print(f"  Ultimo evento: {hist[-1]}")

    # Reset per non sporcare il file AAS con dati di test
    update_aas_deployment_state("jetson_nano", {
        "active_model": None,
        "deployed_at": None,
        "format_used": None,
        "quality_gate_passed": False,
        "baseline_mae": None,
        "baseline_latency_p95_ms": None,
        "baseline_memory_peak_mb": None,
    })
    aas3 = load_aas("jetson_nano")
    aas3["submodels"]["DeploymentState"]["drift_history"] = []
    _write_aas("jetson_nano", aas3)
    print("\nReset AAS completato. File ripristinato allo stato iniziale.")
    print("=" * 55)
    print("Test PASSATO.")
