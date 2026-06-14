# Caso studio illustrativo — Avio Aero MRO turbofan

> **Scopo del documento.** Far vedere, con i dati reali del progetto DMCA
> (benchmark canonico 2026-04-07, drift cycle 2026-04-22, AAS dei 3 asset),
> *cosa cambia davvero* applicando il framework Dynamic Model-Context Alignment
> a un'azienda industriale plausibile. Non è una conferma da Avio Aero — è una
> ricostruzione narrativa pensata per stress-testare la value proposition.
>
> **Versione:** 2026-04-27 (tabelle TOPSIS aggiornate 2026-04-27 con run Modal di completamento) · **Asset coinvolti:** 3 · **Modelli HF candidati:** 8

---

## 1. Perché Avio Aero come caso illustrativo

Avio Aero (GE Aerospace Italia) opera tre principali siti italiani — Pomigliano
d'Arco, Brindisi e Cameri — su attività di MRO (Maintenance, Repair, Overhaul)
e produzione additive di componenti per turbofan civili e militari (CFM56, LEAP,
GE9X, Catalyst). I tre siti hanno realtà operative molto diverse: prove al banco,
ispezione in hangar, additive manufacturing in clean room.

Tre fatti rendono questo profilo ideale per illustrare DMCA:

1. **I dati che ho già coincidono con il dominio.** Il benchmark canonico è su
   CMAPSS FD001 (NASA turbofan degradation), che è esattamente il tipo di
   segnale che si vorrebbe modellare in MRO per Remaining Useful Life (RUL)
   dei moduli del motore.
2. **Hardware eterogeneo e stratificato.** Avio dichiara pubblicamente di usare
   edge computing diffuso e progetti di "smart MRO": uno scenario realistico
   prevede dispositivi a costo basso negli hangar di prima ispezione e
   piattaforme più potenti nei test cell critici. I tre AAS già modellati
   (`raspberry_pi_4`, `jetson_nano`, `jetson_orin_nx`) coprono bene questo gradiente.
3. **Drift di contesto è certo.** I motori in fila per la revisione cambiano
   famiglia (CFM56 in dismissione, LEAP in piena diffusione, GE9X in ramp-up),
   cambia il mix di carburante (ingresso del SAF — Sustainable Aviation Fuel),
   cambia la geografia delle missioni dopo la revisione, cambia il fornitore
   di sensori. Ogni questione di queste rompe l'assunzione i.i.d. che giustificava
   il modello scelto inizialmente. È il caso d'uso archetipo di DMCA.

> **Cosa NON sto affermando.** Non sto sostenendo che Avio Aero usi oggi
> HuggingFace TS models né che soffra del problema così come descritto.
> Sto costruendo uno scenario plausibile, basato su informazioni pubbliche,
> per misurare quanto valore DMCA aggiunge se *qualcuno come Avio* decidesse
> di adottarlo.

---

## 2. Mappa dei tre siti sui tre AAS

| Sito Avio | Profilo operativo plausibile | AAS asset | Hardware | Latenza SLA | SIL |
|---|---|---|---|---|---|
| **Pomigliano d'Arco** | Hangar ispezione visiva e RUL preliminare su CFM56 a fine vita | `raspberry_pi_4` | ARM Cortex-A72, 2 GB RAM, no GPU | 100 ms | 1 |
| **Brindisi** | Test cell LEAP, telemetria multivariata sui banchi prova | `jetson_nano` | Maxwell 128-core GPU, 4 GB unified | 50 ms | 1 |
| **Cameri** | Additive manufacturing GE9X / Catalyst, monitoraggio in-process critico | `jetson_orin_nx` | Ampere 1024-core GPU, 16 GB | 30 ms | 2 |

I tre profili AAS sono già committati nel repo (`assets/*.aas.json`).
Note: nelle deployment AAS sintetiche c'è già una `drift_history` con tre
eventi precedenti (abrupt, variance_shift, gradual) che dimostrano che il loop
DMCA è stato esercitato in passato sul Jetson Nano — utile per la narrativa
"sistema in produzione da mesi".

---

## 3. Stage 1 — DT Profiling: cosa il sistema "vede"

All'avvio della pianificazione, l'orchestratore legge i tre AAS e li converte
in tre vettori vincolo:

```
Pomigliano  → constraint = (hw="raspberry_arm", ram_max=2048MB, lat_sla=100ms,
                            gpu=False, license="apache_2.0", task="forecasting")
Brindisi    → constraint = (hw="jetson_nano",  ram_max=4096MB, lat_sla=50ms,
                            gpu=True, license="apache_2.0", task="forecasting")
Cameri      → constraint = (hw="jetson_orin",  ram_max=16384MB, lat_sla=30ms,
                            gpu=True, license="apache_2.0", task="forecasting")
```

Questo è il punto in cui un MLOps team tradizionale comincerebbe a fare
analisi a mano: leggere datasheet, escludere modelli che non ci stanno,
tradurre i requisiti business in vincoli di deploy. DMCA lo fa
automaticamente leggendo l'AAS — *senza azione umana*.

---

## 4. Stage 2 — Model Selection (TOPSIS) sui dati canonici

Filtro di ammissibilità + TOPSIS pesi `(MAE 0.5, latency 0.3, params 0.1, license 0.1)`
applicati agli 8 modelli del benchmark CMAPSS FD001 del 2026-04-07.

Per i siti senza GPU la latenza p95 misurata su T4 viene penalizzata ×8
(stima conservativa del costo CPU). I valori MAE sono quelli reali misurati
sul run di completamento Modal 2026-04-27 (`benchmark_mae_completion.csv`) —
i proxy originali sono stati sostituiti con i valori effettivi.

> **MAE aggiornate 2026-04-27 con run Modal di completamento.**
> Run: `thesis-mae-completion` su GPU T4, CMAPSS FD001 sensor s2,
> context=128, pred=24, seed=42, n_reps=20. Costo effettivo: ~$0.0126.
> Per dettagli e deviazioni di protocollo: `results/benchmarks/2026-04-27/MERGE_NOTES.md`.

### 4.1 Pomigliano (Pi 4)

| Rank | Modello | MAE | Latency eff. (ms) | Params M | TOPSIS score |
|------|---------|-----|--------------------|----------|--------------|
| 1 | **Lag-Llama** | **0.013336** | 71.06 | 2.45 | **0.613** |
| 2 | patchtst-base-etth1 | 1.30 | 49.53 | 0.67 | 0.387 |

**Esclusi:** moirai-small/large, chronos-tiny/large, timesfm-200m, MOMENT-1-large
(latenza CPU stimata > 100 ms o RAM richiesta non sufficiente).

> **INSIGHT MAE reale.** La MAE di Lag-Llama era stimata con proxy 0.45; il
> valore reale è 0.013336 (34× migliore). Il ranking non cambia — Lag-Llama
> era già il solo candidato a passare il filtro SLA su Pomigliano — ma il
> margine di accuracy sul secondo modello è ora schiacciante.

### 4.2 Brindisi (Jetson Nano)

| Rank | Modello | MAE | Latency p95 (ms) | Params M | TOPSIS score |
|------|---------|-----|-------------------|----------|--------------|
| 1 | **Lag-Llama** | **0.013336** | 8.88 | 2.45 | **0.951** |
| 2 | MOMENT-1-large | 0.114 | 33.21 | 341.25 | 0.591 |
| 3 | patchtst-base-etth1 | 1.30 | 6.19 | 0.67 | 0.387 |

> **INSIGHT MAE reale — score Brindisi 0.761 → 0.951.** Con la MAE reale di
> Lag-Llama (0.013336), il modello raggiunge il valore normalizzato MAE = 1.0
> (miglior assoluto su tutti e 3 i candidati del sito). Il salto di score da
> 0.761 a 0.951 riflette che Lag-Llama domina ora anche sul criterio accuracy,
> non solo su latency e params. MOMENT scende da 0.613 a 0.591 perché il range
> MAE si è allargato (min=0.013 vs ex-min=0.114). Il ranking è invariato.

### 4.3 Cameri (Jetson Orin NX)

| Rank | Modello | MAE | Latency p95 (ms) | Params M | TOPSIS score |
|------|---------|-----|-------------------|----------|--------------|
| 1 | **Lag-Llama** | **0.013336** | 8.88 | 2.45 | **0.613** |
| 2 | patchtst-base-etth1 | 1.30 | 6.19 | 0.67 | 0.387 |

> **INSIGHT MAE reale.** Pool a 2 candidati: il ranking relativo è invariato
> per costruzione TOPSIS (normalizzazione min-max su 2 alternative). MAE
> proxy 0.45 → reale 0.013336, ma lo score rimane 0.613/0.387 perché le
> posizioni ordinate non cambiano.

> **Insight inatteso #1.** Anche su Orin NX (l'hardware più potente)
> il vincolo `latency_sla=30ms` esclude MOMENT-1-large (lat_p95 = 33 ms).
> Questo è esattamente il tipo di trade-off che un ingegnere umano farebbe
> fatica a notare guardando solo le metriche di accuracy: il modello con
> MAE migliore (0.114) viene scartato per 3 ms di overshoot. DMCA lo segnala
> come **borderline** e lo include nel ranking di sensitivity analysis (α/β).

> **Insight inatteso #2.** Il sito più potente (Cameri) e il sito meno potente
> (Pomigliano) finiscono con lo stesso modello (Lag-Llama). Con la MAE reale
> (0.013336) questo è ancora più solido: Lag-Llama è l'unico modello *piccolo,
> veloce e accurato* che supera il filtro SLA su tutti e 3 i siti. Quando
> applichi un filtro stringente di latenza, la dimensione del modello diventa
> più discriminante della potenza dell'hardware.
>
> **Insight inatteso #3 (emerso dai dati reali).** Chronos-tiny ha la MAE
> migliore in assoluto (0.001784 — 7× meglio di Lag-Llama), ma viene escluso
> da tutti i siti perché la sua latenza GPU p95=179ms produce una stima CPU
> ≈1436ms, ben oltre qualsiasi SLA. Se uno dei siti aggiornasse l'SLA a 250ms
> (o acquisisse hardware GPU dedicato), Chronos-tiny salirebbe al rank 1
> scalzando Lag-Llama con un margine netto. Questo è l'ablation naturale da
> fare sulla sensitivity analysis dei vincoli AAS (sezione 10).

---

## 5. Stage 3 — Edge Deployment + Quality Gate

Per ciascun sito, dopo il deploy, il quality gate 4-check:

| Check | Pomigliano | Brindisi | Cameri |
|-------|-----------|----------|--------|
| Latency p95 ≤ SLA | PASS (71 ms ≤ 100) | PASS (9 ms ≤ 50) | PASS (9 ms ≤ 30) |
| Output shape correct | PASS | PASS | PASS |
| Validity (no MAE==RMSE collapse) | PASS | PASS | PASS |
| Memory peak ≤ budget | PASS (~50 MB) | PASS (~20 MB) | PASS (~20 MB) |

DeploymentState aggiornato nei tre AAS con baseline_mae, baseline_latency_p95,
baseline_memory_peak, formato (ONNX status: Lag-Llama → partial). Da questo
momento il sistema è "live".

---

## 6. Stage 4 — Drift Detection (DMCA-Drift v3)

**Scenario operativo (mese 6 dal deploy):** nuovo lotto di motori CFM56
arriva a Pomigliano dopo missioni con miscela SAF crescente. La curva di
degradazione del sensore di temperatura (`s2`) si scosta progressivamente
dalla baseline su cui Lag-Llama era stato profilato.

Riprendo i numeri canonici dell'esperimento `drift_cycle_results.json`:

```
Dataset:           CMAPSS_FD001 (sensor s2)
Drift type:        linear scale 1.0 → 2.0 (proxy del SAF effect)
ADWIN δ:           0.002
ADWIN threshold:   1.9918
Detection index:   t = 1380   (≈ 20 timestep dopo l'inizio della rampa)
MAE baseline:      0.796
MAE alla detection: 3.121     (degrado ~4×)
```

DMCA-Drift v3 non si limita a flaggare "drift sì/no": calcola le 7 feature,
esegue il decision tree e classifica il drift. Per questa rampa lineare
graduale il classificatore attribuisce verosimilmente `incremental` o
`distribution_shift` (in base alla rapidità della rampa nella finestra recente).

L'evento drift viene scritto sull'AAS di Pomigliano (`drift_history.append(...)`)
con campi `severity`, `recommended_action` e `stage_5_strategy` arricchiti
dal contesto AAS. **Il copilot conversazionale notifica il responsabile MRO
del sito con un messaggio in linguaggio naturale**, non con un alert grezzo:

> *"Sul motore #CFM56-1240 ho rilevato un drift incrementale del sensore s2
> nelle ultime 200 osservazioni. L'errore di previsione RUL è cresciuto da
> 0.8 a 3.1 (≈4× sopra baseline). Posso valutare un modello alternativo in
> shadow deployment per le prossime 50 ore prima di proporre uno swap.
> Vuoi procedere?"*

---

## 7. Stage 5 — Re-alignment

Risposta dell'operatore: "sì, procedi". Il sistema:

1. **Riapplica TOPSIS** sui modelli candidati per Pomigliano, ma questa volta
   con la nuova MAE rilevata sui dati post-drift come elemento di valutazione.
   Il ranking cambia: `chronos-t5-tiny` (penalizzato in deploy iniziale dalla
   latenza CPU) sale come candidato perché il suo profilo zero-shot regge meglio
   il cambio distribuzionale.
2. **Shadow deployment in parallelo per 20 timestep** (corrispondenti a 20
   osservazioni nel ciclo di acquisizione, ~ 2 secondi a 10 Hz).
   Numero canonico misurato: MAE chronos-tiny = **1.256**, MAE Lag-Llama
   degradato = **3.121**. Improvement = 60% — sopra la threshold di accettazione.
3. **Copilot L2** (perché SIL=1 ma swap su sistema in produzione) chiede
   conferma. Timeout default = 5 minuti, action di default = `reject`
   (conservativo su SIL≥1).
4. **Operatore conferma**. Atomic swap, grace period 10 tick. AAS aggiornato
   con il nuovo `active_model = "amazon/chronos-t5-tiny"`. Audit JSONL
   append-only.

Tempo recovery canonico misurato: **20 timestep** dalla detection allo swap effettivo.

---

## 8. Tabella "vero apporto" — DMCA vs baseline manuale

Questa è la sezione che ti interessa di più. Confronto onesto, basato sui
numeri canonici dove disponibili, su stime informate altrove.

| Dimensione | **Senza DMCA** (workflow MLOps tradizionale) | **Con DMCA** (numeri canonici) | Apporto reale |
|---|---|---|---|
| Tempo selezione iniziale modelli (3 siti) | 2-5 giorni-uomo (analisi datasheet, profiling, prove a mano) | minuti (lettura AAS + TOPSIS) | **Ordini di grandezza** |
| Tempo detection drift | giorni-settimane (scoperta da KPI o reclamo cliente) | **20 timestep** dopo onset | Da O(giorni) a O(minuti) |
| MAE durante la transizione | runaway: il modello sbagliato continua a predire fino al fix manuale | contenuto: shadow deploy in 20 tick, swap se >threshold | Errore residuo limitato |
| Effort operatore per re-allineamento | retrain pipeline + validazione + deploy: 1-3 giorni-uomo | **1 conferma** sul copilot | ~95% di riduzione |
| Costo per ciclo di benchmark/re-eval | n.d. (di solito on-prem con licenze enterprise) | $0.30 misurati su Modal T4 | Economicamente trascurabile |
| Tracciabilità per audit (ISO/IEC, EASA Part 145) | log frammentati, dipendono dal team | audit JSONL append-only + AAS history | Decisione firmata, ricostruibile |
| Numero modelli mantenibili in parallelo | tipicamente 1-3 per persona MLOps | scala con N siti senza scalare il team | **Scalabilità lineare** |

**Cosa DMCA non fa (limiti onesti):**

- Non rimpiazza la validazione di sicurezza umana per SIL≥2 — la richiede,
  con copilot L3.
- Non *garantisce* che il nuovo modello sia migliore — applica una soglia
  di improvement minima e in caso contrario fa `reject`.
- Per ora (Phase 1) è batch / post-hoc shadow deployment: lo streaming
  parallelo è Phase 2.

---

## 9. Cosa il caso studio dimostra (il "vero apporto")

Distillando in 4 punti, dopo aver fatto girare i tuoi numeri reali:

1. **Il valore non è "saper scegliere un modello"**, è il *loop chiuso*.
   La selezione iniziale (Stage 2) è già un commodity utile, ma da sola la
   risolverebbero un Excel con 4 colonne e una pesatura. Il valore vero è
   che il sistema *si rivaluta da solo* quando il contesto cambia (Stage 4-5),
   e questo lo distingue da AutoML o da semplici model registries.
2. **L'AAS è la moneta che paga la generalizzazione.** Senza un Digital Twin
   strutturato, ogni cliente nuovo richiederebbe codice custom per leggere i
   suoi vincoli. Con AAS standardizzato, lo stesso orchestratore funziona
   su Pomigliano, Brindisi e Cameri senza una riga modificata. Questo è il
   pezzo che la letteratura (anche Yuchen Xia) non ha ancora coperto bene.
3. **Il copilot conversazionale non è cosmetico.** È quello che rende
   accettabile delegare swap di modelli a un sistema autonomo: il responsabile
   MRO riceve un messaggio in italiano comprensibile, non un alert
   `drift_score=3.121, action=swap`. Senza questo strato, in un ambiente
   safety-critical il sistema non passerebbe nemmeno la valutazione interna.
4. **Una contraddizione utile emerge dai dati.** I tuoi benchmark mostrano
   che il vincolo latenza è più discriminante di quanto pensassi: Lag-Llama
   vince in 3 siti su 3 perché *gli altri vengono esclusi prima del ranking*.
   Questo suggerisce un'estensione naturale per la tesi: aggiungere un
   *sensitivity analysis sui vincoli AAS stessi* — "cosa succederebbe al
   ranking se rilassassi `latency_sla` da 30 a 40 ms a Cameri?". Sarebbe
   un'ablation potente per il cap. 4.

---

## 10. Prossimi passi suggeriti per consolidare il caso studio

- [ ] Cercare 2-3 fonti pubbliche su Avio Aero / GE Aerospace digital
  transformation (white paper, articoli IEEE Spectrum, comunicati stampa)
  e citarle nel cap. 5 della tesi come "industry alignment".
- [x] **COMPLETATO 2026-04-27** — MAE calcolati per 5 modelli su run Modal T4
  (`benchmark_mae_completion.csv`, costo ~$0.0126). Tabelle TOPSIS aggiornate
  con valori reali. Dettagli: `results/benchmarks/2026-04-27/MERGE_NOTES.md`.
- [ ] Aggiungere al `simulator_phase2/` un mini-scenario "Avio multi-site"
  che fa partire i 3 siti in parallelo e simula il drift su Pomigliano
  → utilissimo per la demo video.
- [ ] Ablation: ripetere il TOPSIS spostando `latency_sla` di Cameri da
  30 a 40 ms. Probabilmente MOMENT-1-large entra al rank 1 su quel sito.
  Mostra che il sistema è sensibile al DT e non al "default ML wisdom".
