# DD-06 — Decision Tree Layer 2: ordine, soglie, e iterazioni v1→v3

**Data**: 2026-04-21 → aggiornato 2026-04-22
**Modulo**: `pipeline/dmca_drift.py:DMCADriftDetector._layer2_classify()`
**Stage DMCA**: Stage 4 — Drift Detection

---

## Storia delle versioni

| Versione | Accuracy | FAR | Problema principale |
|----------|---------|-----|---------------------|
| v1 (single window) | 40% | 0.000 | Straddle problem (→ DD-05) |
| v2 (baseline+recent, var trigger) | 60% | 0.000 | GRADUAL→ABRUPT, INCREMENTAL→VARIANCE_SHIFT |
| v3 (base_elevation + slope guard) | **80%** | **0.000** | INCREMENTAL irrisolvibile (limitazione nota) |

---

## Percorso di debug v2→v3

### Problema 1: secondary trigger faux-positif su ABRUPT (v2 → v2.1)

Il secondary trigger originale usava `var_ratio > 4.0 AND mean_shift < 15%`.
Al timestep esatto del drift (t=400), la finestra recente contiene 1 solo punto drift
a 2.5: var(recent) = 60× var(baseline) → trigger fires → ABRUPT classificato come VARIANCE_SHIFT.

**Tentativo 1**: trimmed variance (5% top removed) → ratio still 174 with 3 drift values.
**Tentativo 2**: IQR instead of variance → fires for INCREMENTAL (bimodal window has IQR spanning both levels).
**Soluzione adottata (v3)**: MAD + slope guard in Layer 2 shortcut (vedi sotto).

### Problema 2: GRADUAL → ABRUPT (40% → 80%)

Al momento della detection ADWIN (t=255, drift_start=100), la storia lunga 150 campioni
contiene dati già nella rampa sia per baseline_window che per recent_window:

```
history = [t=106..155=ramp_level_1.05, ... , t=206..255=ramp_level_1.26]
baseline_window: mean=1.054, std=0.042
recent_window:   mean=1.265, std=0.035
ks_stat = 1.0 (distribuzioni completamente disgiunte)
outlier_density = 1.0 (tutti i recenti fuori da baseline ± 3σ)
```

Con il decision tree v2 (Rule 1: od>0.25 AND ks>0.25 → ABRUPT), GRADUAL triggera
la regola ABRUPT perché ks=1.0 e od=1.0.

**Diagnosi root cause**: GRADUAL è rilevabile solo quando la media è aumentata abbastanza
da triggerare ADWIN. A quel punto la baseline_window è già profonda nella rampa. Le
due finestre sembrano due popolazioni distinte → sembrano ABRUPT.

**Feature diagnostica**: `base_elevation = (mean(baseline_window) - baseline_mae) / baseline_mae`
- GRADUAL al tempo di detection: base_elevation = 0.054 (5.4% sopra il baseline originale)
- ABRUPT: base_elevation ≈ 0.001 (baseline_window è ancora alla distribuzione originale)

**Soluzione v3**: nuova Rule 1 GRADUAL prima di ABRUPT:
```
if ks_stat > 0.50 AND base_elevation > 0.03 → GRADUAL
```
Rationale: se la baseline_window è già elevata, il drift ha iniziato prima della finestra
→ è una rampa lenta. Un cambiamento abrupt avrebbe baseline_window alla distribuzione
originale (base_elevation ≈ 0).

### Problema 3: INCREMENTAL → VARIANCE_SHIFT (0% — limitazione nota)

**Causa**: ADWIN con δ=0.002 richiede ~295 campioni al nuovo livello per rilevare un
cambio di media di 0.15 (5σ con noise=0.03). Il calcolo:

```
Hoeffding bound: ε_cut ≈ sqrt(ln(4N/δ) / (2 * m_new))
Con δ=0.002, N=300, m_new=17: ε_cut ≈ 0.67 >> 0.15 → non triggera
Soluzione per ADWIN: m_new > 295 campioni per ε_cut = 0.15
```

Il secondary trigger (MAD-based) rileva la variabilità della finestra bimodale (28 campioni
a livello 1.0 + 22 campioni a livello 1.15 → median scende fra i due cluster, MAD elevato).

**Tentativi per separare INCREMENTAL da VARIANCE_SHIFT nel secondary trigger**:
- IQR: fallisce (bimodale ha IQR ampio come VARIANCE_SHIFT)
- MAD: fallisce (median fra due cluster → deviazioni uniformemente elevate)

**Soluzione parziale v3**: slope guard nel shortcut di _layer2_classify
```python
if abs(slope_raw_chk) < 0.003:
    return VARIANCE_SHIFT shortcut
# else: ha trend → run full decision tree
```
Il trigger MAD ancora fira per INCREMENTAL (mad_ratio=3.3), ma Layer 2 non fa shortcut
e classifica INCREMENTAL come ABRUPT (od=0.42, ks=0.32, base_elevation≈0 → Rule 2).

**Risultato**: INCREMENTAL è classificato come ABRUPT (wrong type, right action: model swap).
Accuracy su INCREMENTAL = 0%, ma l'azione è corretta (non VARIANCE_SHIFT = no-swap).

**Limitazione documentata**: INCREMENTAL richiede tracking di detection multiple
(prima detection=ABRUPT, poi ABRUPT di nuovo → reclassifica INCREMENTAL). Phase 2.

---

## Feature aggiuntiva v3: base_elevation (F7)

```python
base_elevation = (float(np.mean(baseline_arr)) - self._baseline_mae) / self._baseline_mae
```

- GRADUAL al detection time: ~0.04-0.08 (4-8% sopra baseline originale)
- ABRUPT, INCREMENTAL, VARIANCE_SHIFT, OUTLIER_DRIVEN: ~0.0-0.01

---

## Decision tree v3 (adottato — accuracy 80%, FAR 0.000)

```
SHORTCUT: variance_trigger AND |slope_raw| < 0.003 → VARIANCE_SHIFT
   Rationale: secondary trigger (MAD) + no trend → vera varianza elevata.
   slope_raw > 0.003 → finestra straddla uno step → vai al decision tree.

1. ks_stat > 0.50 AND base_elevation > 0.03 → GRADUAL
   Rationale: KS alto (due distribuzioni diverse) + baseline già drifted
   → la rampa è iniziata prima della baseline_window → rilevazione tardiva.

2. outlier_density > 0.25 AND ks_stat > 0.25 AND base_elevation < 0.03 → ABRUPT
   Rationale: molti recenti fuori distribuzione baseline + shift distribuzionale
   + baseline window ancora vicina al baseline originale → step improvviso.
   Nota: ks threshold abbassato da 0.50 a 0.25 perché ADWIN rileva a ~15 campioni
   post-step, quando la recent_window ha solo 15/50 valori drift (ks≈0.34, non 0.50).

3. outlier_density > 0.10 AND ks_stat < 0.25 AND |slope| < 0.10 → OUTLIER_DRIVEN
   Rationale: spike sparsi → outlier moderati, nessun shift distribuzionale,
   nessuna tendenza. ks < 0.25 separa da ABRUPT (dove ks > 0.25).

4. var_ratio > 3.0 AND |slope| < 0.08 → VARIANCE_SHIFT (fallback)
   Rationale: varianza alta, media stabile, nessun trend → VARIANCE_SHIFT
   anche se il secondary trigger non ha firedato (fallthrough del shortcut).

5. monotonicity > 0.65 AND slope > 0.02 → GRADUAL (fallback)
   Rationale: rampa con monotonicity elevata al momento della detection.

6. monotonicity > 0.50 AND slope > 0.01 AND plateau_ratio > 0.25 → INCREMENTAL
   Rationale: catch-all per step incrementali con plateau.

7. ks_stat > 0.30 → DISTRIBUTION_SHIFT
   Rationale: distribuzione cambiata, ma non ABRUPT (outlier_density basso).

8. default → UNCLASSIFIED
```

---

## Secondary trigger v3 — MAD-based

Sostituisce la var_ratio v2 e la IQR v2.1.

**WHY MAD instead of variance/IQR**:
- Variance: dominata da singoli punti drift al t=drift_start (1 valore a 2.5 → ratio=60)
- IQR: elevato per finestre bimodali (Q1-Q3 span entrambi i livelli)
- MAD: robusto se la maggior parte dei punti è vicina alla mediana. Tuttavia fallisce
  se la mediana scende tra due cluster (bimodal → MAD elevato). Vedi slope guard.

```python
mad_b = median(|base - median(base)|)
mad_r = median(|recent - median(recent)|)
if mad_b > 1e-6 and (mad_r / mad_b) > 3.0:
    mean_shift = |mean(recent) - baseline_mae|
    if mean_shift < 0.08 * baseline_mae:    # 8% guard (era 15% in v2)
        drift_detected = True; variance_trigger = True
```

**Calibrazione soglie**:
- `mad_ratio > 3.0`: VARIANCE_SHIFT con σ_drift=4σ_noise → ratio ≈ 4.0 ✓
  INCREMENTAL bimodal → ratio ≈ 3.3 (passes, but blocked by slope guard in Layer 2)
- `mean_shift < 8%`: ABRUPT con 3 punti drift → mean_shift = 3σ_drift/50 = 9% → blocked ✓
  VARIANCE_SHIFT → mean_shift ≈ 0 ✓

---

## Limitazione nota: INCREMENTAL non rilevabile con ADWIN δ=0.002

ADWIN con δ=0.002 richiede ~295 nuovi campioni per rilevare un cambiamento medio di 0.15
con noise σ=0.03. Ogni step INCREMENTAL dura 100 campioni → ADWIN non triggera.

**Classificazione risultante v3**: INCREMENTAL → ABRUPT (wrong type, right action).

**Fix Phase 2**: usar ADWIN con δ più alto (0.05-0.10) in parallelo con δ=0.002, o un
detector dedicato per mean-shift piccoli (sequential probability ratio test, SPRT).
Alternativa: tracking cross-detection (se ABRUPT multipli con piccoli step → reclassify INCREMENTAL).

---

## Confusion matrix v3 (n_seeds=3)

| GT \ Pred     | ABRUPT | GRADUAL | INCREMENTAL | VAR_SHIFT | OUTLIER |
|---------------|--------|---------|-------------|-----------|---------|
| ABRUPT        | 3      | 0       | 0           | 0         | 0       |
| GRADUAL       | 0      | 3       | 0           | 0         | 0       |
| INCREMENTAL   | 3      | 0       | 0           | 0         | 0       |
| VARIANCE_SHIFT| 0      | 0       | 0           | 3         | 0       |
| OUTLIER_DRIVEN| 0      | 0       | 0           | 0         | 3       |

Overall accuracy: **80%** | FAR: **0.000**

---

## Riferimento codice

- `pipeline/dmca_drift.py:_layer2_classify()` — decision tree v3 + shortcut
- `pipeline/dmca_drift.py:update()` — secondary MAD trigger
- `pipeline/dmca_drift.py:_generate_scenario_mae()` — 5 scenari sintetici CMAPSS
