# DD-03 — topsis_mae=999.0 per modelli probabilistici

**Data**: 2026-04-21
**Modulo**: `gaps.json`, `pipeline/topsis_ranker.py`
**Stage DMCA**: Stage 2 — Model Selection

---

## Problema

I modelli Moirai, Chronos, Lag-Llama producono output probabilistici
(distribuzioni di quantili, campioni da distribuzioni). Il benchmark GPU T4
ha misurato latenza e RAM per questi modelli, ma non MAE, perché il codice
`modal_jobs.py` non implementa l'estrazione del punto mediano dall'output
probabilistico per calcolare MAE standard.

Il TOPSIS richiede un valore numerico per il criterio MAE (peso 0.5).
Con MAE=None/NaN, il ranker crasha o produce NaN nel score.

---

## Opzioni valutate

| Opzione | Pro | Contro |
|---------|-----|--------|
| **Sentinel 999.0** | Semplice, penalizza appropriatamente | Arbitrario; potrebbe escludere modelli buoni |
| **MAE da letteratura** | Motivato fisicamente | Valori da paper diversi, dataset diversi → non confrontabili |
| **Re-run benchmark con post-processing** | Valore reale | Richiede accesso GPU, costo aggiuntivo |
| **Escludere i modelli senza MAE** | Pulito | Rimuove chronos-t5-tiny dal catalog, impossibile |
| **Usare CRPS al posto di MAE** | Metrica corretta per probabilistici | Richiede ground truth e post-processing; dati non disponibili |

---

## Scelta adottata

**Sentinel 999.0** con flag documentata per ogni modello in `gaps.json`:

```json
{
  "topsis_mae": 999.0,
  "has_measured_mae": false,
  "mae_note": "Probabilistic output. To fix: extract median quantile → mae = np.mean(np.abs(np.median(samples, axis=-1) - actuals)). Re-run modal_jobs.py with post-processing."
}
```

---

## Ragione

1. **I dati benchmark sono canonici e non rigenerabili** (costo GPU già speso,
   validati il 2026-04-07). La policy del progetto vieta di rigenerare.

2. **999.0 è una penalità conservativa corretta**: con peso MAE=0.5, un modello
   con mae=999 perderà sempre sul criterio accuracy nel TOPSIS. Questo è
   corretto: se non abbiamo misurato la MAE non possiamo fidarci del modello.

3. **La flag `has_measured_mae`** permette di identificare rapidamente i modelli
   da ri-misurare quando sarà disponibile accesso GPU.

---

## Come ottenere il valore reale (istruzioni per Phase 2)

```python
# Per Chronos: usare ChronosPipeline
from chronos import ChronosPipeline
pipe = ChronosPipeline.from_pretrained("amazon/chronos-t5-tiny")
forecast = pipe.predict(context, prediction_length=24)
# forecast.shape = (n_samples, n_series, prediction_length)
median_forecast = np.median(forecast[0].numpy(), axis=0)
mae = np.mean(np.abs(median_forecast - actuals))

# Per Moirai: estrarre dalla distribuzione
# Per Lag-Llama: usare distribution.mean
```

Aggiornare poi `gaps.json`:
```json
"topsis_mae": <valore_reale>,
"has_measured_mae": true,
"mae_note": "Misurato su CMAPSS FD001, split=train, Phase 2."
```

---

## Trade-off accettato

- **Si perde**: ranking accurato dei modelli probabilistici per il criterio MAE
- **Si guadagna**: il TOPSIS non crasha e produce ranking deterministico
- **Effetto pratico**: chronos-t5-tiny (MAE=999) perderà sempre contro
  timesfm (MAE=0.006) sul criterio accuracy, anche se nella realtà chronos
  potrebbe avere MAE comparabile

---

## Riferimento codice

- `gaps.json:selection_matrix.model_catalog.time_series` — tutti i modelli
  probabilistici hanno `has_measured_mae: false` e `mae_note` con istruzioni
- `pipeline/topsis_ranker.py:TopsisRanker._extract_row()` — legge `topsis_mae`
