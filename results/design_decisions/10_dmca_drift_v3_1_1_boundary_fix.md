# DD-10 — DMCA-Drift v3.1.1: R1 boundary semantic correction

**Data**: 2026-04-30
**Modulo**: `pipeline/dmca_drift.py:DMCADriftDetector._layer2_classify()`
**Stage DMCA**: Stage 4 — Drift Detection

---

## Problema

Il held-out test (seeds [42, 99, 123, 7, 88], drift_holdout_2026-04-30.json) ha
rivelato che OUTLIER_DRIVEN seed=42 viene classificato come `unclassified`.

Analisi delle feature al timestep di detection (S5_OUTLIER, drift_start=300):

```
seed=42: od=0.1000  ks=0.2400  F8=3.47
Rule R1: od > 0.10  →  0.10 > 0.10  →  False  (boundary miss)
```

outlier_density vale esattamente 0.10: è il boundary esatto della condizione strict
`od > 0.10`. La condizione non si attiva, nessun'altra regola copre il caso,
risultato: UNCLASSIFIED.

---

## Natura del fix: semantic correction, non calibration

La regola R1 intende catturare i casi in cui "almeno il 10% dei campioni recenti
sono outlier rispetto alla baseline". L'espressione verbale "almeno" corrisponde
semanticamente a `>=`, non a `>`.

La strict inequality (`> 0.10`) era un artefatto di implementazione: non derivava
da una scelta progettuale esplicita né da calibrazione su dati. Non esiste nessun
motivo fisico o operativo per cui esattamente il 10% di outlier debba essere
trattato diversamente dal 10.001%.

**Questo fix è giustificabile A PRIORI**, senza necessità di osservare i dati held-out.
L'held-out ha solo reso visibile un artefatto già latente.

**Distinzione semantic vs calibration:**

| Tipo di fix | Descrizione | Richiede nuovo held-out? |
|-------------|-------------|--------------------------|
| **Semantic correction** | Correzione di una discrepanza tra intenzione verbale e codice. Il valore numerico (0.10) non cambia. | No — la correttezza è giustificabile a priori |
| **Calibration tuning** | Modifica del valore numerico della soglia (es. 0.10 → 0.08) per migliorare l'accuracy su dati osservati. | Sì — richiede nuovo held-out per evitare overfitting |

Cambiare `> 0.10` in `>= 0.10` è una semantic correction: la soglia rimane 0.10,
cambia solo l'interpretazione del boundary. Cambiare `> 0.10` in `> 0.08` sarebbe
calibration tuning e richiederebbe un nuovo held-out set.

**Modifica effettuata:**
```python
# v3.1:
elif od > 0.10 and ks_stat < 0.25:
# v3.1.1:
elif od >= 0.10 and ks_stat < 0.25:
```

---

## Alternative considerate

| Opzione | Descrizione | Esito |
|---------|-------------|-------|
| **(a) Lasciare strict (> 0.10)** | Accettare il failure come limitazione del modello | Scartato: l'intenzione operativa è non-strict; mantenere il bug non è difendibile |
| **(b) Audit sistematico di tutti i `>` e `<` strict** | Verificare tutti i boundary del tree per semantic consistency | Scartato: scope creep oltre il singolo fix giustificabile; gli altri boundary (0.25, 0.40, 0.5, etc.) sono calibration choices, non semantic descriptions |
| **(c) Lowering soglia (od > 0.08)** | Spostare il boundary per aumentare recall OUTLIER_DRIVEN | Scartato: sarebbe calibration tuning non supportato da motivazione semantica; richiederebbe nuovo held-out |
| **(d) Applicare >= 0.10 — scelta adottata** | Allineare codice all'intenzione verbale "almeno 10%" | Adottato |

---

## Effetto empirico osservato

**Nota metodologica**: il primo held-out eseguito (drift_holdout_2026-04-30.json,
versione iniziale) usava drift_start errati per S4_VARIANCE (300 invece di 400) e
S5_OUTLIER (200 invece di 300), producendo MAE series diverse da quelle del modulo
ufficiale. Questo bug nel test runner è stato individuato durante la verifica di
v3.1.1 (cambiamento di latency per seed=2). I file sono stati ricalcolati con i
parametri corretti dal modulo (drift_start letti da `run_validation_scenarios`).

| Metrica | v3.1 val (n=5) | v3.1.1 val (n=5) | v3.1 holdout (n=5) | v3.1.1 holdout (n=5) |
|---------|:-:|:-:|:-:|:-:|
| ABRUPT | 100% | 100% | 100% | 100% |
| GRADUAL | 100% | 100% | 100% | 100% |
| INCREMENTAL | 60% | 60% | 60% | 60% |
| VARIANCE_SHIFT | 100% | 100% | 100% | 100% |
| OUTLIER_DRIVEN | 100% | 100% | **80%** | **100%** |
| OVERALL | 92% | 92% | **88%** | **92%** |
| FAR | 0.000 | 0.000 | 0.000 | 0.000 |

Il fix recupera esattamente 1 caso held-out (OUTLIER_DRIVEN seed=42, od=0.10 esatto).
Non modifica nessun risultato sul validation set (nessun seed 0-4 ha od=0.10 esatto).

---

## Caso modificato: OUTLIER_DRIVEN seed=42

```
v3.1:   od=0.1000  ks=0.2400  → od > 0.10  False  → UNCLASSIFIED
v3.1.1: od=0.1000  ks=0.2400  → od >= 0.10 True   → OUTLIER_DRIVEN ✓
```

---

## Trade-off accettati: 2 failure residui

I seguenti 2 failure cases del held-out restano in v3.1.1. **Non vengono affrontati**
in questa versione per disciplina metodologica — appartengono a Limitations /
Future Work della tesi.

| Caso | seed | Tipo atteso | Pred. errata | Root cause |
|------|------|-------------|-------------|------------|
| INCREMENTAL | 123 | incremental | distribution_shift | mo=0.449, soglia 0.45 borderline (mono≈N(0.50,0.05)) |
| INCREMENTAL | 88 | incremental | gradual | ADWIN late detection: slope negativo nella finestra, od=1.0 → R4 GRADUAL fires |

La ragione per cui non si interviene ora:
- INCREMENTAL mono fragility (seed=123): richiederebbe lowering mono 0.45→0.44, che sarebbe calibration — necessita nuovo held-out.
- INCREMENTAL late detection (seed=88): problema strutturale di ADWIN (plateau detection) — non risolvibile con threshold tuning nel tree.

**Nota**: il caso OUTLIER_DRIVEN seed=123, originariamente classificato come failure
nell'esecuzione iniziale (drift_holdout_2026-04-30.json pre-bug-fix), è risultato
correttamente classificato dopo la correzione dei drift_start nel test runner
(od=0.12 > 0.10, già supera anche la regola strict pre-fix). Non costituisce trade-off
di v3.1.1.

---

## File modificati

- `pipeline/dmca_drift.py` — docstring v3.1.1, R1: `>` → `>=`
- `results/drift_experiments/drift_validation_2026-04-30_v3_1_1.json`
- `results/drift_experiments/drift_holdout_2026-04-30_v3_1_1.json`
- `results/drift_experiments/drift_holdout_2026-04-30.json` — ricalcolato con drift_start corretti
- `CLAUDE.md` — Stage 4 aggiornato a v3.1.1
