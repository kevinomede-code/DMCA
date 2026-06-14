# DD-04 — Constant Prediction Check: arr.size > 1

**Data**: 2026-04-21
**Modulo**: `pipeline/quality_gate.py:_check_validity()`
**Stage DMCA**: Stage 3 — Edge Deployment

---

## Problema

Il check di "zero-shot collapse" (constant prediction) usa la proprietà
matematica: se un modello predice sempre lo stesso valore costante k, allora:

```
MAE = mean(|k - y|) = |k - mean(y)|   (costante)
RMSE = sqrt(mean((k - y)^2))          (costante)
```

Ma la condizione `abs(MAE - RMSE) < 0.001` è **trivialmente vera** per qualsiasi
output scalare (1 elemento), perché:

```
arr = [v]   →   MAE = |v|   →   RMSE = sqrt(v^2) = |v|   →   MAE == RMSE sempre
```

In questo caso il check produce falsi positivi per qualsiasi modello che
produca previsioni step-1 (orizzonte = 1 timestep).

**Bug osservato**: Ridge surrogate con output shape (1,) — gate falliva
con `constant_prediction=True` anche per previsioni valide e variabili.

---

## Opzioni valutate

| Opzione | Pro | Contro |
|---------|-----|--------|
| **`arr.size > 1`** come guard | Semplice, corregge il bug | Non rileva collapse su horizon=1 |
| **Confrontare output su input diversi** | Rileva anche horizon=1 | Richiede 2 inferenze extra, più lento |
| **Usare std(arr) > threshold** | Rileva valori costanti | std=0 è l'unica condizione, MAE==RMSE è più stabile |
| **Rimuovere il check** | Semplice | Perde un segnale utile per modelli horizon>1 |

---

## Scelta adottata

**Guard `arr.size > 1`**: il check MAE≈RMSE si attiva solo per output
con più di 1 elemento (horizon > 1).

```python
constant_pred = arr.size > 1 and abs(mae - rmse) < 0.001 and mae > 0
```

---

## Ragione

1. **Il collapse è rilevante solo per horizon > 1**: un modello che produce
   sempre lo stesso valore per previsioni multi-step è chiaramente degenere.
   Per horizon=1, non c'è modo di distinguere collapse da previsione corretta
   con un solo campione.

2. **La condizione MAE==RMSE è matematicamente stabile**: `abs(MAE - RMSE) < 0.001`
   funziona bene per array numerici float32/float64 senza problemi di precision.

3. **Il caso horizon=1** (come Ridge surrogate) è il caso normale per modelli
   step-ahead classici. Non va penalizzato.

---

## Trade-off accettato

- **Si perde**: rilevazione di collapse su horizon=1 (non rilevante in DMCA
  perché i modelli fondazionali producono sempre horizon > 1)
- **Si guadagna**: zero falsi positivi per modelli step-ahead e surrogate

---

## Esempio che triggera correttamente il check

```python
class ConstantModel:
    def predict(self, x):
        return np.full((x.shape[0], 24), 3.14)  # horizon=24, sempre 3.14

# arr = [3.14, 3.14, ..., 3.14]  (24 elementi)
# MAE = 3.14, RMSE = 3.14 → abs(3.14 - 3.14) < 0.001 → True → FAIL
```

---

## Riferimento codice

- `pipeline/quality_gate.py:_check_validity()` — riga `constant_pred = arr.size > 1 and ...`
