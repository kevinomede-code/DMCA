# DD-01 — AAS Type 1 (file JSON) vs BaSyx SDK

**Data**: 2026-04-21
**Modulo**: `pipeline/aas_parser.py`, `assets/*.aas.json`
**Stage DMCA**: Stage 1 — DT Profiling

---

## Problema

Lo standard IEC 63278 (Asset Administration Shell) prevede due modalità:
- **Type 1**: AAS come file statico (JSON/XML), leggibile offline
- **Type 2**: AAS servito via REST API (server BaSyx o equivalente)

Il framework DMCA richiede di leggere i vincoli del Digital Twin a ogni ciclo
di riallineamento. Bisognava scegliere quale tipo implementare in Phase 1.

---

## Opzioni valutate

| Opzione | Pro | Contro |
|---------|-----|--------|
| **Type 1 — file JSON** | Zero dipendenze server, riproducibile offline, testabile in CI | Non aggiornabile in real-time senza riscrivere il file |
| **Type 2 — BaSyx SDK** | Aggiornamento real-time, standard completo IEC | Richiede server Java, dipendenza esterna pesante, complessità per Phase 1 |
| **Type 2 — FastAPI custom** | Lightweight, pythonic | Duplica lo standard, non citabile come IEC-compliant |

---

## Scelta adottata

**Type 1 — file JSON con write atomico** (`assets/{asset_id}.aas.json`)

Il parser legge il file a ogni chiamata (`load_aas()`). Le scritture usano
il pattern `write-to-tmp → rename` per garantire atomicità senza lock.

---

## Ragione

1. **Riproducibilità**: la tesi deve essere riproducibile da un revisore
   senza server BaSyx installato. Type 1 funziona con `python aas_parser.py`.

2. **Scope Phase 1**: il contributo originale è il ciclo DMCA (selezione,
   drift, riallineamento), non l'infrastruttura AAS. BaSyx è Future Work
   documentato in CLAUDE.md.

3. **Testabilità**: i file JSON possono essere versionati in git e usati
   come fixture di test. Un server BaSyx richiederebbe test di integrazione
   non portabili.

---

## Trade-off accettato

- **Si perde**: aggiornamento real-time del DT (Type 2 lo supporta)
- **Si guadagna**: zero dipendenze, portabilità, testabilità immediata

Il trade-off è documentato come "Phase 1 implementation" nei commenti del
codice e nella sezione Future Work della tesi.

---

## Verifica

```bash
python pipeline/aas_parser.py
# Output atteso: constraint vector stampato, drift_history aggiornata, reset OK
```

---

## Riferimento codice

- `pipeline/aas_parser.py:_write_aas()` — write atomico
- `pipeline/aas_parser.py:load_aas()` — lettura con validazione submodel
- `assets/jetson_nano.aas.json` — esempio schema
