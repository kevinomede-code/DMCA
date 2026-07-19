# DD-04 — Incoerenza `min_hw` / ammissibilità e impatto sulla sensitivity TOPSIS

**Data:** 2026-07-17
**Stato:** DIAGNOSI — nessuna modifica ai dati canonici effettuata. In attesa di decisione.
**Origine:** emerso mentre si costruiva la sensitivity analysis sui pesi TOPSIS (a supporto della frase a `thesis_draft.tex` riga 2438).

---

## 1. Sintesi in una frase

I valori `min_hw` in `gaps.json` **non riflettono né la memoria misurata né la latenza né i parametri** dei modelli: escludono da Jetson Nano modelli che fisicamente ci girano (PatchTST, Lag-Llama), lasciando **un solo** modello ammissibile su Nano. Questo rende impossibile una sensitivity sui pesi su quel profilo e **contraddice l'ablation** della tesi.

---

## 2. Come funziona il filtro (codice reale)

`pipeline/topsis_ranker.py`:

```
_HW_ORDER = [plc_embedded, raspberry_arm, jetson_nano, jetson_orin, pc_cpu_only, pc_gpu_entry]
```

Un modello è ammissibile su un asset se `rank(min_hw) <= rank(asset.hw_class)`.
→ Su **jetson_nano** (rank 2) passano solo i modelli con `min_hw ∈ {plc_embedded, raspberry_arm, jetson_nano}`.

Altri filtri: C1 latenza `topsis_latency_ms <= SLA*1.5`; C3 zero-shot (se l'asset è zero-shot, il modello deve essere zero-shot).

---

## 3. I dati (verificati)

| modello | params_M | lat_T4 (ms) | RAM picco (MB) | `min_hw` | zero_shot |
|---|---:|---:|---:|---|---|
| patchtst-base-etth1 | 5 | 6.2 | 14 | **pc_cpu_only** | False |
| chronos-t5-tiny | 8 | 203.1 | 45 | raspberry_arm | True |
| Lag-Llama | 50 | 8.9 | 20 | **jetson_orin** | True |
| moirai-1.1-R-small | 91 | 62.9 | 106 | jetson_nano | True |
| timesfm-1.0-200m | 200 | 2109.5 | 8 | pc_gpu_entry | True |
| moirai-1.1-R-large | 311 | 73.9 | 2360 | pc_gpu_entry | True |
| MOMENT-1-large | 385 | 33.2 | 1408 | pc_gpu_entry | True |
| chronos-t5-large | 710 | 902.9 | 2773 | jetson_orin | True |

RAM misurata dal benchmark canonico `results/benchmarks/2026-04-07/benchmark_results_modal.csv`.
Jetson Nano ha 4 GB: **tutti gli 8 modelli entrano in memoria su Nano** (max 2773 MB < 4096).

---

## 4. Le incoerenze

**A. `min_hw` non monotòno con dimensione/memoria/latenza.**
- PatchTST è il modello **più piccolo e veloce** (5M, 14 MB, 6 ms) ma ha `min_hw=pc_cpu_only` → **escluso da Nano**. Illogico.
- Lag-Llama (50M, 20 MB) richiede `jetson_orin`, ma Moirai-Small (91M, 106 MB, **più grande e lento**) richiede solo `jetson_nano`. Un modello più piccolo che pretende hardware più potente.
- MOMENT-L (385M, 1408 MB) → `pc_gpu_entry`, ma Chronos-large (710M, 2773 MB, **più grande**) → `jetson_orin` (meno esigente). Invertito.

**B. La memoria non è il vincolo.** Tutti entrano in 4 GB. Il vero discriminante su edge è la **latenza**, non `min_hw`. Il gate `min_hw` così com'è è in gran parte spurio.

**C. Incoerenza zero-shot con l'ablation.** `tab:ablation` dichiara profilo "zero-shot" ma dà **PatchTST** come top-TOPSIS; PatchTST ha `zero_shot=False` → non potrebbe mai essere ammissibile in un profilo zero-shot. Problema indipendente da `min_hw`.

**D. (secondario) `params_M` vs `topsis_params_m` divergono** per i modelli piccoli (es. PatchTST 5 vs 0.67; Lag-Llama 50 vs 2.45; Moirai-Small 91 vs 11.6). Due campi di parametri in disaccordo.

---

## 5. Conseguenze

- **Ammissibili su Jetson Nano (SLA 50, zero-shot), filtro reale:** solo **Moirai-Small**.
- Con **un solo** candidato, la sensitivity sui pesi TOPSIS è **indefinita** (nessun ri-ordinamento possibile). ⇒ la frase a riga 2438 (*"top-1 stabile per w1∈[0.35,0.65], w2∈[0.20,0.45]"*) **non è supportata**: è un placeholder.
- **Contraddizione narrativa:** l'ablation dice PatchTST top / Lag-Llama operativo su Nano; i dati dicono **solo Moirai-Small**. Coerente invece con la riga 314 ("Moirai-Small on a Jetson Nano") e la riga 220. ⇒ ablation vs case study si contraddicono, **a prescindere dalla sensitivity**.

Ammissibili per profilo (filtro reale, latenze T4), per riferimento:

| profilo | ammissibili | N |
|---|---|---:|
| Jetson Nano, SLA 50, zero-shot | Moirai-Small | 1 |
| Jetson Orin, SLA 100 | Moirai-Small, Lag-Llama | 2 |
| PC CPU, SLA 100 (supervised) | Moirai-Small, PatchTST, Lag-Llama | 3 |
| PC GPU, SLA 200 | Moirai-S/L, Chronos-tiny, MOMENT-L, Lag-Llama | 5 |

---

## 6. Opzioni di risoluzione

**Opzione 1 — Correggere `min_hw` (memory-grounded).**
Riassegnare `min_hw` in base alla memoria misurata (quasi tutti → classe Nano; la latenza diventa il discriminante). Su Nano l'ammissibile diventa ~5 modelli → sensitivity sensata + ablation plausibile.
*Costi:* modifica dato canonico; cambia gli esiti di selezione; va ri-verificata la coerenza di ablation e case study; va risolto anche il nodo zero-shot (il profilo dell'ablation dovrebbe essere "supervised/data-available" perché PatchTST sia eleggibile, oppure PatchTST va tolto e la sensitivity si fa tra i modelli zero-shot).

**Opzione 2 — Non toccare i dati canonici.**
Fare la sensitivity sul **pool completo** (profilo PC-GPU, 5 modelli) come studio di *robustezza della matrice di selezione*, non Nano-specifico; sostituire la frase 2438 con questo risultato reale.
*Costi:* meno legata al profilo edge; ma zero rischi sui dati validati.

**Opzione 3 — Ricalcolare `min_hw` con una regola documentata** (tier memoria + soglia latenza) come nuovo DD, e allineare tutto una volta sola.

---

## 7. Raccomandazione

Indipendentemente dalla sensitivity, **la contraddizione ablation ↔ case study (punto 5) va sanata** — è il tipo di incoerenza che una commissione nota.

Per la sensitivity in sé, il percorso a **rischio minimo** è l'**Opzione 2** (pool completo, nessun tocco ai dati). L'**Opzione 1** è la correzione "alla radice" ma è una revisione sostanziale della selezione: da fare solo se si è disposti a ri-controllare ablation e case study.

Nota: qualunque strada, la frase 2438 va **sostituita coi risultati veri** (decisione già presa).
