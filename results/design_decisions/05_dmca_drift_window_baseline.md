# DD-05 — Finestra di analisi: single window vs baseline+recent

**Data**: 2026-04-21
**Modulo**: `pipeline/dmca_drift.py:DMCADriftDetector`
**Stage DMCA**: Stage 4 — Drift Detection

---

## Problema (versione 1 — single window)

La versione originale del Layer 2 usava un'unica finestra scorrevole
di 50 campioni per estrarre le 5 feature. Al momento della detection
(es. t=511 per drift abrupt a t=500), la finestra contiene:

```
[t=461..499] = 39 campioni baseline (mean≈1.0, std≈0.05)
[t=500..511] = 12 campioni drifted  (mean≈2.5, std≈0.05)
```

**Effetti patologici osservati:**

| Tipo drift | Feature critica | Valore | Causa errore |
|------------|----------------|--------|--------------|
| GRADUAL | monotonicity | 0.47 | Noise σ=0.02 > gradient 0.002/step → diff spesso negative |
| GRADUAL | slope (norm) | 0.002 | Normalizzato su baseline_mae=1.0, rampa lenta → slope irrilevante |
| INCREMENTAL | outlier_density | 0.22 | Step-changes nella finestra → nuovi valori sembrano outlier |
| ABRUPT | outlier_density | 0.24 | Valori post-step sembrano outlier rispetto a baseline-dominated window |

**Risultato**: GRADUAL→DISTRIBUTION_SHIFT (0% accuracy), INCREMENTAL→ABRUPT (0%), overall=40%

---

## Analisi della causa radice

La finestra singola al momento della detection ha un **problema strutturale**:
straddla il punto di cambiamento (straddle problem). Di conseguenza:

1. **Monotonicity** non è informativa: un abrupt change ha un solo salto (mono≈0.02), una
   gradual ramp con rumore ha mono≈0.47 — quasi identici, non discriminanti.

2. **Slope normalizzato su baseline_mae** perde la scala: slope_raw=0.002/step,
   baseline_mae=1.0 → slope_norm=0.002. Soglia originale: slope>0.5. Mai raggiunta.

3. **Outlier_density usa la mediana della finestra mista** (straddled): la mediana
   è circa 1.2 (mix 39×1.0 + 12×2.5), MAD≈0.1, soglia 3×MAD=0.3. Tutti i valori
   a 2.5 sembrano outlier → densità alta anche per ABRUPT (non solo OUTLIER_DRIVEN).

---

## Soluzione: finestra lunga con separazione baseline/recent

**Approccio adottato (versione 2)**:

Mantieni una storia più lunga (`3 × window_size`). Layer 2 estrae le feature
confrontando esplicitamente due sottofinestre:
- **baseline_window**: i primi `window_size` campioni della storia (pre-drift)
- **recent_window**: gli ultimi `window_size` campioni (post-drift)

```
history = [...baseline_window...][...middle...][...recent_window...]
           first window_size                    last window_size
```

**Effetti sul calcolo delle feature:**

| Feature | V1 (single window) | V2 (baseline vs recent) |
|---------|--------------------|------------------------|
| slope | slope(mixed_window) / baseline_mae | slope(recent_window) / range(recent) |
| var_ratio | var(second_half) / var(first_half) | var(recent) / var(baseline) |
| monotonicity | on mixed window | on recent window only |
| ks_stat | first_half vs second_half of mixed | baseline_window vs recent_window |
| outlier_density | outliers vs median(mixed) | outliers vs baseline distribution (mean±3σ) |

**Risultato**: le feature sono ora calcolate su popolazioni "pure" (baseline vs drift)
invece che su finestre miste che straddlano il punto di cambiamento.

---

## Trade-off accettato

- **Si perde**: reattività immediata (la storia lunga richiede più campioni prima
  di poter fare analisi affidabile). Latenza aumenta di ~window_size timestep.
- **Si guadagna**: feature molto più discriminanti, accuratezza classification attesa >70%.

---

## Riferimento codice

- `pipeline/dmca_drift.py:DMCADriftDetector.__init__()` — `_history`, `_history_maxlen`
- `pipeline/dmca_drift.py:DMCADriftDetector._layer2_classify()` — separazione baseline/recent
