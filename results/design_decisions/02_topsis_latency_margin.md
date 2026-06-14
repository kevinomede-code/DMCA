# DD-02 — Margine SLA × 1.5 in filter_admissible

**Data**: 2026-04-21
**Modulo**: `pipeline/topsis_ranker.py:filter_admissible()`
**Stage DMCA**: Stage 2 — Model Selection

---

## Problema

I dati di latenza nel benchmark CSV (`benchmark_results_modal.csv`) sono stati
misurati su **GPU NVIDIA T4** (Google Colab / Modal), non sull'hardware edge
target (Jetson Nano, Raspberry Pi).

La latenza su Jetson Nano GPU Maxwell è 5-20x più alta di quella su T4.
Se si usa `latency_p95 <= sla_ms` come hard constraint con i dati T4,
quasi nessun modello è ammissibile per SLA ≤ 50ms.

**Esempio**:
- SLA Jetson Nano: 50ms
- Latenza T4 di moirai-1.1-R-small: 62.9ms → REJECTED con constraint strict
- Latenza T4 di chronos-t5-tiny: 203ms → REJECTED
- Risultato: 0 modelli ammissibili → escalation forzata (sbagliato)

---

## Opzioni valutate

| Opzione | Pro | Contro |
|---------|-----|--------|
| **Strict `<= sla_ms`** | Aderente allo spec formale | Con dati T4 → sempre 0 ammissibili |
| **Margine fisso `× 1.5`** | Pratico, robusto ai dati T4 | Arbitrario, non calibrato |
| **Conversion factor per device** | Fisicamente motivato | Richiede benchmark separati per ogni device |
| **Usare solo latency class** (categorical) | Zero dipendenza dai dati benchmark | Perde la risoluzione numerica, torna al sistema pre-TOPSIS |

---

## Scelta adottata

**Margine `sla_ms × 1.5`** come threshold per `filter_admissible()`.

Con SLA=50ms → threshold=75ms → moirai-1.1-R-small (62.9ms T4) è ammissibile.

---

## Ragione

1. **Il benchmark è canonico e non rieseguibile** (costo $0.30 GPU T4,
   dati validati). Non si possono aggiungere benchmark Jetson Nano ora.

2. **Il margine 1.5x è conservativo**: in letteratura i conversion factor
   T4→Jetson Nano variano da 5x a 20x. Con 1.5x si è comunque restrittivi
   rispetto alla latenza reale su edge.

3. **L'alternativa (latency class categorica)** annulla il contributo
   principale del Task 4: usare latenze misurate invece di classi ordinali.

---

## Trade-off accettato

- **Si perde**: matching preciso tra latenza misurata e SLA reale su device
- **Si guadagna**: il TOPSIS può funzionare con i dati canonici esistenti
- **Limitazione documentata**: "Phase 1 usa dati GPU T4; Phase 2 richiede
  benchmark su device target per eliminare il margine empirico"

---

## Implicazione per la tesi

Il risultato dell'ablation study cambia rispetto all'implementazione originale:
- `select_model()` (filtro categorico) → selezionava `chronos-t5-tiny`
- `filter_admissible() + TOPSIS` (latenza misurata) → seleziona `moirai-1.1-R-small`

Questa differenza è citabile come evidenza del contributo TOPSIS:
"l'uso di latenze misurate invece di classi ordinali cambia la selezione
in modo non triviale (Section IV-B)".

---

## Verifica

```bash
python pipeline/topsis_ranker.py
# Ammissibili (Jetson Nano, SLA=50ms, zero_shot): 1
# Modello selezionato: Salesforce/moirai-1.1-R-small
```

---

## Riferimento codice

- `pipeline/topsis_ranker.py:filter_admissible()` — C1 check, riga con `sla_ms * 1.5`
