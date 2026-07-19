# Changelog & decisioni — DMCA thesis

> Pipeline dei cambiamenti e delle decisioni prese sulla tesi.
> Periodo: 2026-07-17 → 2026-07-18. File toccati: `thesis_draft.tex`,
> `references_master.bib`, `pipeline/generate_plots.py`,
> `pipeline/missed_alarm_simulation.py`, figure PDF.
> Verificato sul PDF compilato **tesi (40).pdf** (101 pagine).

---

## 1. Migrazione SLA 50 ms → 100 ms (Jetson Nano)

**Decisione finale: SLA = 100 ms ovunque.** (Percorso: 50 → tentato 100 → tornato a 50 → **definitivo 100**.)

**Perché 100 e non 50 (il punto che ha chiuso il dibattito):**
la figura di scheduling faceva "stare" PatchTST dentro la finestra da 50 ms usando
un fattore T4→edge di **×5** solo per PatchTST, mentre Moirai usava ×10 — indifendibile.
Al fattore onesto **×10**, PatchTST reale è 58.6 ms → **sfora** 50 ms ma **rientra** in 100 ms.
Quindi 100 ms è l'unica soglia che non richiede trucchi. Giustificata come budget
end-to-end di **3GPP TS 22.104** (voce bib `3GPP22104` aggiunta, `\cite` funzionante → `[108]`).

**Conseguenze numeriche propagate (verificate nel PDF):**

| Grandezza | Prima (50 ms) | Dopo (100 ms) |
|---|---|---|
| Formula coverage | `round(ℓ/SLA)` | `ceil(ℓ/SLA)` |
| Step Moirai-S | s = 11 | **s = 6** |
| Step Lag-Llama | s = 2 | **s = 1** |
| Coverage Moirai-S | 9.1 % | **16.7 %** (1/6) |
| Finestre non osservate | 94.5 % | **83.3 %** |
| Lead Moirai-S Bearing1_1 | 280 s | **350 s** |
| Lead Moirai-S Bearing3_2 | −20 s (miss) | **+50 s** (actionable) |
| Gap PatchTST↔Moirai | 150 s | **80 s** |
| Bound Eq.11 Δt_max (s=6) | 210 s | **110 s** (80 ≤ 110 regge) |

**Riscrittura safety story:** da "veloce prende / lento manca (−20 s)" a
"coverage 1/6 + margine eroso di 80 s". Corretto claim falso "safety standards
impose ≤ 50 ms" → "sub-100 ms real-time budget (3GPP)".

**50 ms legittimi rimasti** (NON sono l'SLA Nano, verificati): ciclo OPC-UA Case A
(≈1000 ms = 20 cicli × 50 ms), overhead di misura < 50 ms, lead = 50 **secondi**.

---

## 2. I due "100 ms" — disambiguazione T4 vs edge (3 figure)

**Problema individuato da Kevin:** nel bar chart Moirai-S (54 ms) stava sotto la
linea "SLA 100 ms" → sembrava ammissibile e più accurate, contro il testo che lo esclude.

**Causa reale:** "100 ms" è usato in **due frame diversi**:
- **Capitolo benchmark** → latenze **GPU T4**, soglia soft-real-time di **classe Jetson Orin / entry-GPU** (lì MOMENT-L a 29.7 ms è il "sweet spot", coerente col testo).
- **Case Study B** → target **Jetson Nano**, SLA hard 100 ms edge; tutto ×10 → Moirai-S = 537 ms **inammissibile**, restano solo PatchTST (58.6) e Lag-Llama (77.7).

**Decisione:** NON riscalare le figure benchmark a ×10 (contraddirebbe cluster e
sweet-spot del loro capitolo). Tenere le latenze **T4 canoniche** e **disambiguare**
asse + didascalia. Applicato a tutte e 3 le figure:
- `latency_comparison` (fig. eq. 16) — asse "GPU T4", linea "soft-SLA 100 ms (T4)", nota "sul Nano ×10 → solo PatchTST/Lag-Llama".
- `accuracy_latency_scatter` (fig. 17) — "Sweet spot (Orin-class)", nota T4, layout ripulito.
- `fig1_benchmark_scatter` (fig. 18) — didascalia aggiornata: zona ammissibile è a scala T4/Orin, sul Nano ×10 solo PatchTST/Lag-Llama.

Nota: il MAE Moirai-S = 0.228 (righe 320/5113) **è reale** — in tabella con footnote †
(misurato a parte, fuori dal run modal da $0.30). Non inventato.

---

## 3. Storia PatchTST resa task-aware (abstract + contributi)

PatchTST ha **due destini legittimi** perché sono due task diversi:
- **Case A (ETT-h1, forecasting):** TOPSIS #1 ma **bloccato dal quality gate Stage 3**
  (zero-shot collapse MAE = RMSE) → deploy di **Lag-Llama** via cascading fallback.
- **Case B (PRONOSTIA, allarme a soglia RMS):** il criterio è **coverage**, non MAE →
  il profilo ultra-leggero di PatchTST tiene coverage piena (lead 430 s).

Rimosso il MAE **0.019 fabbricato** dall'abstract (valore reale 1.303 con collapse);
descrittore riscritto task-aware. Aggiunto Future Work "Joint accuracy–coverage
selection objective".

---

## 4. Bibliografia

- **C1** (note→annote): campi `note` non citabili convertiti in `annote`; corretti
  entry malformate (doi "mangiato" in simon1957bounded, Pfeiffer2025).
- **C2** (dedup): union deduplicata **234 → 164 entry**. `references_master.bib` è
  l'**unico file caricato su Overleaf** (i .bib per-gap sono organizzazione locale).
- Aggiunta voce `@techreport{3GPP22104}` (ETSI TS 122 104, v17.7.0).
- Backlog **C3**: 4 citazioni rotte residue **solo in `paper_draft.tex`** (Bifet2007ADWIN,
  IDTA_AAS, IEC62890_2020, Shi2016EdgeComputing) + 3 occorrenze di 0.019 — non nella tesi.

---

## 5. Figure rigenerate (tutte a 100 ms)

| Figura | Come | Note |
|---|---|---|
| `fig8_scheduling_windows` | TikZ inline nel .tex | ×10 onesto, niente PDF |
| `fig_coverage_concept` | matplotlib, dati reali Bearing1_1 | 3 pannelli, soglia µ+3σ=0.737 g, allarmi 430/350 s |
| `latency_comparison` | `generate_plots.py` (fixato) | T4 + disambiguazione |
| `accuracy_latency_scatter` | `generate_plots.py` (fixato) | T4, layout ripulito |
| `fig1_benchmark_scatter` | (esistente) | didascalia disambiguata |
| `fig_csb_pronostia` + per-bearing | `missed_alarm_simulation.py` (fixato) | SLA_MS=100, step=ceil |

**Gotcha tecnico:** il mount Linux serviva una copia **troncata** di `generate_plots.py`
e Python usava un `.pyc` in cache col codice vecchio (×10). Risolto con lo script
standalone `pipeline/_regen_figs.py` (scrive diretto sul mount, niente cache stale).
Backup pre-100 in `remediation/bib_backup_C2/` e `pipeline/*_PRE100.py`.

---

## 6. Esito full-check sul PDF compilato (tesi 40)

- ✅ Nessun "SLA = 50 ms" Nano residuo (i "50" rimasti sono legittimi).
- ✅ Coverage 16.7 % / 83.3 % / 1-in-6 coerenti; nessun 9.1 % / 94.5 % / 1-in-11.
- ✅ Lead 430 / 350 / gap 80 s; nessun 280 / −20 residuo.
- ✅ Eq.11 = (2s−1)×10 s → Δt_max = 110 s; 80 ≤ 110 regge.
- ✅ **Nessun fattore ×5** (solo ×10 T4→edge e 1.5× margine SLA).
- ✅ **Nessuna citazione rotta** ("?" / "[?]" assenti); 3GPP = [108].
- ✅ Abstract task-aware, senza MAE 0.019 fabbricato.
- ✅ Tutte e 3 le scatter/bar disambiguate T4 vs Nano.

---

## 7. Da fare (Kevin)

1. Caricare su Overleaf: `thesis_draft.tex`, `references_master.bib`, i PDF figure
   rigenerati (`latency_comparison`, `accuracy_latency_scatter`, `fig1_benchmark_scatter`,
   `fig_coverage_concept`, `fig_csb_pronostia`, per-bearing). Ricompilare da zero.
2. Backlog `paper_draft.tex` (fuori tesi): 4 citazioni rotte + 3× 0.019.

---

## 8. DD-04 risolto — la selezione ora riproduce la tesi (2026-07-18)

**Problema:** eseguendo `topsis_ranker.py` su `gaps.json` per il profilo Jetson Nano
usciva **solo Moirai-Small** ammissibile — l'esatto opposto della Table 16 e del
Case Study B. La Table 16 non era riproducibile e non esisteva un file di risultati.

**Tre cause, tutte corrette ancorandosi ai dati misurati** (backup in `remediation/dd04_backup/`):

1. **`min_hw` non fondati.** PatchTST (0.67 M par, 14 MB) era `pc_cpu_only`;
   Moirai-S (11.6 M, 106 MB) era `jetson_nano` — rovesciato. Rifondati su
   `max(RAM misurata, params×4 MB)` contro il budget di memoria di ogni tier.
   Esito: tutti scendono a tier ≤ jetson_nano → **la memoria non è mai stata il
   vincolo, lo è la latenza** (conferma del DD-04).
2. **Filtro latenza in scala sbagliata.** Confrontava la latenza **T4** con l'SLA
   **edge**, senza il ×10 usato dal testo e da `missed_alarm_simulation.py`.
   Ora `filter_admissible` applica `constraints["latency_factor"]` (proprietà del
   dispositivo, non del modello).
3. **`task` di Lag-Llama** era `rul_prediction` (il caso d'uso su CMAPSS) invece di
   `forecasting` (la capacità del modello). Corretto.

**Semantica C3 (decisione utente — lettura B).** `zero_shot: False` significa
"non progettato per zero-shot", non "non eseguibile". Un modello è ammissibile su
un asset zero-shot se è **nativamente zero-shot OPPURE ha un benchmark zero-shot
misurato** (`has_measured_mae`). Questo ammette PatchTST — il cui MAE 1.303 *è* una
misura zero-shot — e lascia il collapse al **Stage 3 quality gate**, che è
esattamente ciò che motiva l'esistenza del gate: il ranking non può prevedere il
collapse dalle sue feature.

**Risultato verificato** (`results/ablation/ablation_jetson_nano_sla100.json`),
profilo Jetson Nano / SLA 100 ms / ×10 / zero-shot / forecasting:

```
#1  ibm/patchtst-base-etth1   score=0.9856  lat_edge= 61.9 ms  mae=1.303
#2  Lag-Llama                 score=0.0144  lat_edge= 88.8 ms  mae=999.0
esclusi: Moirai-S 629ms · Moirai-L 739ms · Chronos-T 2031ms
         Chronos-L 9029ms · TimesFM 21095ms · MOMENT-L 332ms+task
```

Riproduce la **Table 16 esattamente** (PatchTST rank-1 → gate → Lag-Llama operativo)
col profilo zero-shot già dichiarato in didascalia, e mantiene Moirai-S inammissibile
come richiede il Case Study B. **Nessuna modifica al testo della tesi necessaria.**

**Resta aperto — doppia implementazione della selezione.** `simulation_agent.py`
(workflow W2) contiene un selettore inline proprio: filtro su classi categoriche
(`hard_realtime`/`batch`) e scelta finale con `min(params_M)`, **non** TOPSIS.
La tesi descrive TOPSIS a 4 criteri (0.5/0.3/0.1/0.1). Va fatto delegare W2 a
`topsis_ranker.filter_admissible` + `TopsisRanker.rank` — è il punto 10 della lista
"moduli DA CREARE" di CLAUDE.md (refactoring `simulation_agent`), mai eseguito.

### 8b. Refactoring `simulation_agent.select_model` — un solo selettore

**Problema:** `simulation_agent.py` (workflow W2, quello che genera l'ablation)
conteneva un **secondo selettore** indipendente da `topsis_ranker.py`:
filtro su classi categoriche (`hard_realtime`/`soft_realtime`/`batch`) e scelta
finale con `min(params_M)` — non TOPSIS. Sullo stesso profilo i due divergevano:

```
A) simulation_agent (W2)  -> chronos-t5-tiny   2031 ms edge  (20x sopra l'SLA!)
B) topsis_ranker (tesi)   -> PatchTST 61.9 ms  poi Lag-Llama 88.8 ms
```

Tre difetti in A: (i) le etichette `latency` categoriche non corrispondono alle
misure — chronos-t5-tiny è `soft_realtime` ma misura 203 ms T4 / 2031 ms edge;
(ii) `min(params_M)` è un'euristica, non il TOPSIS a 4 criteri documentato;
(iii) il campo `params_M` diverge dai valori misurati (Lag-Llama 50 vs 2.45,
PatchTST 5 vs 0.67, Moirai-S 91 vs 11.61).

**Fatto:** `select_model()` ora delega a `filter_admissible` + `TopsisRanker`,
mantenendo firma e semantica dei flag dell'ablation (realizzati rilassando i
constraint, non duplicando la logica). Aggiunto `_device_latency_factor()`:
×10 per le classi edge, 1.0 per PC/GPU. Backup:
`remediation/dd04_backup/simulation_agent_PRE_REFACTOR.py`.

**Risultato ablation** (`results/ablation/ablation_jetson_nano_sla100.json`):

| configurazione | ammissibili | #1 |
|---|---|---|
| tutti i filtri | 2 | PatchTST → gate → Lag-Llama |
| ignore_latency | **7** | PatchTST |
| ignore_hardware | 2 | PatchTST |
| training_data_available | 2 | PatchTST |

**Due osservazioni emerse, da valutare:**

1. **Il filtro latenza è l'unico che lavora** (2 → 7 candidati se disattivato).
   Conferma quantitativamente la tesi centrale: la latenza è il vincolo
   vincolante, non la memoria né l'hardware.
2. **Il filtro hardware è ora inerte** — dopo aver fondato i `min_hw` sulla
   memoria misurata, tutti gli 8 modelli stanno nei 4 GB del Nano, quindi
   disattivarlo non cambia nulla. È un risultato onesto (la memoria non vincola),
   ma la riga corrispondente della Table 16 non mostra più variazione.
3. **Il sentinella 999 distorce la normalizzazione TOPSIS del MAE.** Con range
   [0.006, 999], la differenza reale fra 0.006 e 1.303 si comprime a quasi zero:
   il criterio MAE (peso 0.5, il dominante) si comporta di fatto come un flag
   binario "ha misura / non ha misura". Da dichiarare in Limitations o da
   trattare con un'imputazione esplicita.

### 8c. Stato finale riproducibilità Table 16 (non impatta la tesi)

Dopo il refactor, correzione `task` di Lag-Llama e MOMENT-L (capacità del modello,
non caso d'uso) e implementazione di `task_only` come baseline solo-accuratezza:

| Config | Table 16 | Codice | |
|---|---|---|---|
| C1 — Full DMCA | Lag-Llama | PatchTST #1 → gate → Lag-Llama | ✅ |
| C2 — No HW filter | Lag-Llama | idem | ✅ |
| C3 — No latency filter | MOMENT-Large | PatchTST → gate → Lag-Llama | ❌ |
| C4 — Task-only | TimesFM | TimesFM | ✅ |

**C4** ora riproduce perché `task_only` è stato implementato per ciò che
rappresenta: il **selettore naive accuracy-only**, il termine di paragone del
"TimesFM paradox" — non una configurazione DMCA, quindi giustamente non usa TOPSIS.

**C3 resta diverso**, e la causa è nota e documentata: il sentinella
`topsis_mae = 999.0` (**DD-03**, scelta deliberata per i modelli probabilistici
senza MAE puntuale confrontabile) comprime la normalizzazione min-max del criterio
MAE. Sulla scala [0.006, 999] il vantaggio di accuratezza di MOMENT-L (0.114 vs
1.303) diventa trascurabile, mentre il suo svantaggio sui parametri (341 M vs
0.67 M) pesa pieno → vince PatchTST.

**Non corretto di proposito.** Allinearlo richiederebbe di cambiare il trattamento
del sentinella nella normalizzazione o i pesi TOPSIS: una modifica metodologica che
si propagherebbe alle righe che oggi tornano, non un ritocco di chiusura. E **non ha
alcun effetto sulla tesi**: la Table 16 nel PDF è autoconsistente, il codice non
viene consegnato. Registrato qui come limite noto della riproducibilità.
