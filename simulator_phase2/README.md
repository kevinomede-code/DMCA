# DMCA Simulator — Phase 2

**Status**: Planned (Phase 1 complete — see `pipeline/`)
**Target**: Post-thesis, GPU access via Prof. Yi Li

---

## Panoramica

Phase 2 sostituisce la simulazione batch di Phase 1 con un simulatore
dinamico streaming che riproduce fedelmente un deployment industriale
OPC-UA reale.

La differenza fondamentale con Phase 1:

| Aspetto | Phase 1 (attuale) | Phase 2 (pianificato) |
|---------|-------------------|----------------------|
| Ingestion | Batch (file CSV) | Streaming asyncio (OPC-UA simulato) |
| Inferenza | Surrogate (Ridge/mock) | Modelli HF reali via HuggingFace Hub |
| Shadow deployment | Post-hoc (MAE ratio surrogato) | Parallelo (doppia inferenza live) |
| COPILOTCONFIRM | Sincrono simulato | Async MQTT con timeout reale |
| AAS server | File JSON locale | FastAPI REST server (BaSyx-compatible) |
| Drift detection | Finestra fissa | ADWIN-U (varianza) + ADWIN (media) |

---

## Architettura pianificata

```
simulator_phase2/
├── README.md                  ← questo file
├── stream_ingestor.py         ← asyncio producer: OPC-UA simulato → queue
├── inference_engine.py        ← worker asyncio: HF model → MAE stream
├── shadow_manager.py          ← doppia inferenza: active + candidate in parallelo
├── aas_server.py              ← FastAPI: AAS REST API (BaSyx Type 2 compatible)
├── copilot_gate.py            ← async COPILOTCONFIRM con MQTT + timeout
├── adwin_u.py                 ← ADWIN-U: rilevazione cambiamento varianza
└── integration_test.py        ← test end-to-end streaming
```

---

## Prerequisiti Phase 2

### Hardware
- GPU NVIDIA A100/H100 del Prof. Yi Li (Beihang)
- O GPU T4 via Modal (budget separato, ~$5-10 per run completo)

### Modelli reali da testare
- `google/timesfm-1.0-200m` — state-of-the-art zero-shot
- `ibm/patchtst-base-etth1` — fine-tuning su CMAPSS
- `Salesforce/moirai-1.1-R-base` — versione base (non small)
- `amazon/chronos-t5-small` — probabilistico con MAE reale

### Dipendenze aggiuntive
```
fastapi>=0.110
uvicorn
asyncua          # OPC-UA client/server Python
paho-mqtt        # MQTT per COPILOTCONFIRM
adwinU           # ADWIN-U per varianza (custom o fork di river)
```

---

## Roadmap Phase 2

### Milestone 1 — Streaming MAE pipeline
- [ ] `stream_ingestor.py`: genera MAE stream da CMAPSS FD001 con drift injection
- [ ] `inference_engine.py`: asyncio wrapper per HF model.predict()
- [ ] Validare latenza end-to-end: ingestion → inference → drift detection ≤ SLA

### Milestone 2 — True parallel shadow deployment
- [ ] `shadow_manager.py`: doppia coda asyncio (active + candidate)
- [ ] Confronto MAE live su finestra scorrevole (non più surrogate ratio)
- [ ] Confidence interval sul miglioramento (bootstrap, n=100 finestre)

### Milestone 3 — AAS server REST
- [ ] `aas_server.py`: FastAPI che serve AAS JSON via GET/PATCH
- [ ] Integrazione con BaSyx Python SDK per AAS Type 2 compliance
- [ ] WebSocket per push notification delle drift events

### Milestone 4 — COPILOTCONFIRM async reale
- [ ] `copilot_gate.py`: MQTT publish/subscribe con topic `dmca/confirm/{asset_id}`
- [ ] Timeout configurabile (default 30s), callback per risposta operatore
- [ ] Dashboard minimale (Streamlit) per conferma swap in browser

### Milestone 5 — ADWIN-U per VARIANCE_SHIFT
- [ ] Implementare o wrappare ADWIN-U (Bifet 2010, estensione per varianza)
- [ ] Risolvere la limitazione nota di Phase 1: INCREMENTAL misclassification
- [ ] Validazione: 5 scenari × 10 seed → target accuracy ≥ 90%

### Milestone 6 — Integration test streaming
- [ ] `integration_test.py`: simula 3000 timestep con tutti i tipi di drift
- [ ] Misura: detection latency, FAR, swap accuracy, grace period stability
- [ ] Output: paper-ready figures per Capitolo 7 thesis

---

## Note implementative Phase 1 → Phase 2

### Cosa è già pronto (Phase 1)
- AAS schema JSON validato (`assets/*.aas.json`)
- TOPSIS ranker con sensitivity analysis (`pipeline/topsis_ranker.py`)
- Quality gate 4-check (`pipeline/quality_gate.py`)
- Drift detector Layer 1/2/3 (`pipeline/dmca_drift.py`) — accuracy 80%
- Re-alignment engine con audit trail JSONL (`pipeline/realignment.py`)
- Design decision log completo (`results/design_decisions/`)

### Breaking changes Phase 1 → Phase 2
- `aas_parser.update_aas_deployment_state()` → diventa PUT /aas/{asset_id}/state
- `DMCADriftDetector.update()` → accetta stream di tuple (mae, timestamp_utc)
- `RealignmentEngine._copilotconfirm()` → diventa async con MQTT callback
- `simulation_agent.py` → sostituito da `simulator_phase2/integration_test.py`

---

## Riferimento

- Phase 1 implementazione: `pipeline/`
- Benchmark canonici (NON rigenerare): `results/benchmarks/2026-04-07/`
- Drift experiment canonici: `results/drift_experiments/drift_cycle_results.json`
- Design decisions: `results/design_decisions/`
