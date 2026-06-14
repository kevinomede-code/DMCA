# DD-08 — Stage 5: Shadow Deployment e COPILOTCONFIRM

**Data**: 2026-04-22
**Modulo**: `pipeline/realignment.py:RealignmentEngine`
**Stage DMCA**: Stage 5 — Re-alignment

---

## Problema

Stage 5 deve decidere se e quando swappare il modello attivo con un candidato,
dopo che Stage 4 ha rilevato un drift. Le sfide:

1. **Come valutare il candidato senza GPU?** (Phase 1 = no budget GPU)
2. **Chi approva lo swap?** (operatore umano vs automatico)
3. **Cosa succede se l'approvazione non arriva?** (timeout policy)
4. **Come garantire atomicità e rollback?**

---

## Scelta 1: Shadow deployment post-hoc surrogato (Phase 1)

### Problema

Un vero shadow deployment richiede che il candidato giri in parallelo al modello
attivo per N timestep, confrontando le predizioni su dati reali in streaming.
Phase 1 è batch: non c'è streaming reale, e ri-invocare HuggingFace per inferenza
costerebbe GPU budget aggiuntivo (vietato per dati canonici).

### Opzioni valutate

| Opzione | Pro | Contro |
|---------|-----|--------|
| **Surrogate MAE ratio** (adottato) | Zero costo GPU, deterministico | Approssimazione |
| Re-run inference su finestra storica | MAE reale | Costo GPU, lentezza |
| MAE da letteratura per candidato | Motivato | Dataset diversi, non comparabile |
| Skip shadow, swap diretto | Semplice | Nessuna validazione pre-swap |

### Scelta adottata

Surrogate shadow: `candidate_mae_surrogate = active_mae × (topsis_mae_candidate / topsis_mae_active)`
calibrato dai dati benchmark canonici (2026-04-07, GPU T4).

```python
mae_ratio = candidate_topsis_mae / active_topsis_mae
candidate_window = active_window * mae_ratio * rng.uniform(0.95, 1.05, n)
```

Il fattore `uniform(0.95, 1.05)` simula l'incertezza della surrogata (±5%).

**Casi speciali:**
- stesso modello attivo/candidato → ratio = 1.0 (nessun miglioramento)
- uno dei due ha MAE sentinella 999.0 → ratio = 0.80 (default conservativo)

**Limitazione documentata**: Phase 2 eseguirà inferenza parallela reale con
asyncio + streaming MAE. La surrogate è sufficiente per dimostrare il ciclo DMCA.

---

## Scelta 2: Soglia di miglioramento 10%

Il miglioramento minimo richiesto per triggerare lo swap è 10% di riduzione MAE.

### Razionale

- **< 5%**: potrebbe essere variabilità statistica nel surrogate (±5% di rumore)
- **10%**: threshold standard in letteratura per model selection operazionale
  (Sculley et al. 2015 — "Machine Learning: The High Interest Credit Card")
- **> 20%**: troppo restrittivo — perderemmo swap vantaggiosi in scenari reali

Il 10% è una scelta conservativa appropriata per Phase 1 dove non abbiamo
validazione statistica rigorosa del miglioramento.

---

## Scelta 3: COPILOTCONFIRM — timeout policy per SIL

### Problema

Lo swap del modello richiede approvazione dell'operatore per asset safety-critical.
Se l'operatore non risponde (timeout), quale è la policy corretta?

### Analisi

| SIL | Failure mode | Policy corretta |
|-----|-------------|-----------------|
| SIL < 2 | Uptime loss > safety risk | Timeout → **approve** (keep running) |
| SIL ≥ 2 | Safety > uptime | Timeout → **reject** (keep known model) |

Per SIL ≥ 2 (es. jetson_orin_nx), il principio fail-safe impone di mantenere
il modello attivo (comportamento noto) se non possiamo confermare la sicurezza
del nuovo modello. Questo segue IEC 61508 per sistemi safety-related.

### Scelta adottata (Phase 1)

Phase 1 non ha async/MQTT, quindi il timeout è simulato:
- SIL < 2: auto-approve (operatore non-critico, uptime preference)
- SIL ≥ 2: auto-reject (operatore critico, safety preference)

**Phase 2**: gate real-time via WebSocket/MQTT con timeout configurabile (default 30s).

---

## Scelta 4: Audit trail JSONL append-only

Ogni evento del ciclo 5A→5C viene appeso a `results/audit/realignment_audit.jsonl`.

### Razionale

- **Append-only**: garantisce integrità — nessun evento può essere cancellato
- **JSONL** (JSON Lines): ogni riga è un JSON autonomo → leggibile riga per riga,
  compatibile con `jq`, spark, pandas senza caricare tutto in memoria
- **Nessuna foreign key**: ogni record è auto-contenuto (audit_id, timestamp, asset_id)
  per semplificare l'analisi forense

### Schema evento esempio

```json
{
  "ts": "2026-04-22T10:15:30Z",
  "event": "swap_executed",
  "asset_id": "jetson_nano",
  "action": "swap",
  "active_model_id": "Salesforce/moirai-1.1-R-small",
  "new_model_id": "ibm/patchtst-base-etth1",
  "audit_id": "a3f7b2c1",
  "improvement_pct": 19.3,
  "grace_period_t": 10
}
```

---

## Test verificati (Phase 1)

| Test | Scenario | Expected | Result |
|------|---------|---------|--------|
| T1 | ABRUPT, SIL=1, moirai→patchtst | swap | PASS |
| T2 | VARIANCE_SHIFT (no_swap=True) | no_swap | PASS |
| T3 | ABRUPT, SIL=2 → timeout | reject | PASS |
| T4 | Stesso modello candidato | reject (improvement=-0.7%) | PASS |

---

## Riferimento codice

- `pipeline/realignment.py:RealignmentEngine.run()` — entry point Stage 5
- `pipeline/realignment.py:_stage5a_shadow()` — shadow deployment surrogato
- `pipeline/realignment.py:_copilotconfirm()` — gate SIL
- `pipeline/realignment.py:_log_event()` — audit trail JSONL
- `results/audit/realignment_audit.jsonl` — file audit
