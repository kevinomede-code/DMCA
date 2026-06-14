# Scaletta call prof — 30 minuti — copione completo

> Aperto a fianco del PDF e del demo. PDF page = thesis page **+1** (offset cover/abstract).
> Tutto in italiano informale. Le frasi tra "" sono pronte da paraphrasare a voce.

---

## Atto 1 — Apertura (~2 min)

*"Ti faccio vedere a che punto sono. Parto dal demo perché dà l'idea visiva di tutto il framework in 4 minuti, poi entriamo nella tesi — sezione per sezione, vado veloce nell'introduzione e mi fermo dove c'è la sostanza. Ho tre domande mirate da farti in chiusura."*

Niente intro accademica. Sa già il contesto.

---

## Atto 2 — Demo live (~4 min)

1. Apri `factory_v4.html`, scenario **"Nano · GRADUAL (canonical, no-swap)"** già selezionato. Premi **Play**.
2. Mentre gira, parla:
   *"Quello che vedi sullo schermo è la traccia reale del drift cycle canonico — sensore s2 del CMAPSS FD001, finestra di 200 timestep da t=1220 a t=1410, con soglia ADWIN a 1.9918. Non sono dati simulati al volo, è la replay del file `drift_cycle_results.json` che produce il workflow W3."*
3. Quando ADWIN scatta e il **drawer Stage 4 si apre da solo**:
   *"Qui automaticamente si apre il drawer dello Stage 4 con le 8 feature calcolate (slope, iqr_ratio, ks_stat, outlier_density, monotonicity, max_delta_sigma...) e l'albero di decisione v3.1.1. La regola che ha matchato è evidenziata in blu — questa è la XAI integrata nel dialogo, GAP 3 della tesi."*
4. Clicca tessera **Stage 5** → mostri il counterfactual:
   *"Qui c'è il controfattuale: DMCA sotto SLA serve il 100% delle finestre di fault detection; un task-only selector che sceglie il modello più accurato cade a una percentuale minima perché supera lo SLA. Questo è il **paradosso SLA** che caratterizza tutto il framework."*
5. **Stop a 4 min.** Se vuole approfondire, *"ne riparliamo subito nel walkthrough"*. Il demo è esca, non l'evento.

---

## Atto 3 — Walkthrough tesi (~18 min)

### 3.1 — Capitolo 1: Introduzione e contributi (1 min · thesis p.9 · PDF p.10)

*"Vado dritto ai contributi a pag. 9. Tre cose principali: primo, l'architettura closed-loop a 5 stage che è il framework DMCA — guida la selezione del modello dal DT, deploya su edge, rileva drift e si riallinea automaticamente. Secondo, il benchmark empirico di 8 modelli foundation time-series su 2 dataset, totale 0.30$ di GPU T4. Terzo, il classificatore di drift v3.1.1 con calibrazione iterativa documentata."*

Sopra ci sono le 4 RQ — *menzionale di passaggio*:
*"RQ1 su come l'AAS struttura la selezione, RQ2 sulla robustezza dei pesi multi-criterio, RQ3 sull'accuracy del classificatore drift, RQ4 sui pattern di explainability conversazionale per fiducia calibrata. Non le leggo, ci torniamo se vuoi."*

### 3.2 — Capitolo 2: Literature Review (1.5 min · thesis p.23 · PDF p.24)

*"Pago 23, gap matrix. La parte importante non è la matrice in sé ma il **processo** di selezione del corpus: 847 paper iniziali, screen su due assi tematici per arrivare a 127, poi citation network analysis tramite Graphify — 496 nodi, 595 edge, community detection Leiden — che ha identificato 23 paper core la cui rimozione disconnetterebbe il grafo. Tutti e 23 sono citati. Non è una literature a tentoni, ha un protocollo replicabile."*

Punta alla matrice:
*"Il punto della tabella: nessun paper esistente copre più di 2 dei 5 gap simultaneamente. DMCA è il primo che li copre tutti e 5 nello stesso framework. Sono G1 selezione multi-criteria driven da DT, G2 integrazione TS + LLM, G3 conversational XAI, G4 framework di validazione industriale, G5 trust calibrato nel tempo."*

### 3.3 — Capitolo 3 e 4: Methodology + Design Decisions (30 sec totali · skip)

*"Cap 3 è la metodologia — uso MCDA come paradigma decisionale, validation strategy a quattro livelli L1-L4 (technical, safety-blocking, operator qualitativa, production), reproducibility ed ethics dichiarati. Cap 4 raccoglie le 10 design decisions DD-01 a DD-10 sui dettagli di implementazione. Salto e prendiamo quelle che servono dentro Cap 5."*

### 3.4 — Capitolo 5.1: Framework architecture overview (2 min · thesis p.36 · PDF p.37)

*"Pago 36, Tabella 8 — l'architettura a 5 stage. Stage 1 prende l'AAS e produce un constraint vector. Stage 2 con TOPSIS produce una ranked model list. Stage 3 è il quality gate che fa partire il predictor in run. Stage 4 monitora il residuo e emette drift alarm. Stage 5 fa re-alignment e — questo è il punto chiave — aggiorna l'AAS, che riparte da Stage 1. **Il loop è chiuso**: il DT è sia l'input iniziale sia il target finale dell'update."*

Indica Figura 2:
*"La novità rispetto alla letteratura è proprio questa: la maggior parte dei sistemi esistenti fa selection una volta e poi si dimentica. DMCA tratta selection come un problema da risolvere continuamente, guidato dal DT che evolve nel tempo."*

### 3.5 — Capitolo 5.2: Stage 1 DT Profiling (1 min · thesis p.37 · PDF p.38)

*"Stage 1 è il parser AAS. Schema IEC 63278-1:2023 Type 1, file JSON. Estraggo un constraint vector con hardware class, RAM budget, latency SLA P95, data availability, sensor protocol, license. Tre profili di riferimento per la tesi: Jetson Nano 50ms SLA 4GB, Raspberry Pi 4 100ms 4GB CPU-only, Jetson Orin NX 20ms 16GB Ampere GPU."*

*"Scope note importante (pag 38): uso un parser custom file-based compatibile con basyx-python-sdk, non un live BaSyx Server. Quello è Future Work — connessione OPC-UA 10000 a un server BaSyx vero. Va dichiarato."*

### 3.6 — Capitolo 5.3: Stage 2 TOPSIS (1.5 min · thesis p.38 · PDF p.39)

*"Stage 2 è il MCDA. M_adm — l'insieme ammissibile — è definito dall'eq. 1 a pag 38: lat_p95 ≤ 1.5× SLA, RAM ≤ B_ram, data e license compatibili. Cinque vincoli hard, niente sfumature. Sui modelli che passano, TOPSIS ranka per 4 criteri pesati: MAE 0.5, latency 0.3, params 0.1, license 0.1."*

*"Nota di onestà: il margine **1.5× SLA** è una scelta Phase 1 — lascia slack alla selezione, e poi lo Stage 3 fa enforcement stretto a 1.0×. In Future Work sarebbe da stringere a 1.0× ovunque. Lo dichiaro nei Limitations a pag 59."*

*"Sul copilot conversazionale: l'XAI ha 3 livelli — L1 fonte ed evidenza, L2 razionale del modello, L3 metriche storiche. È citato qui ma non implementato in Phase 1 — anche questo Future Work."*

### 3.7 — Capitolo 5.5: Stage 4 Drift Detection v3.1.1 (4 min · thesis p.40-43 · PDF p.41-44)

**QUESTO è il punto centrale, dove ti fermi più tempo.** Sezione 5.5.1 è una vera mini-thesis dentro la thesis.

*"Pago 40, Stage 4. Tre layer: Layer 1 trigger (ADWIN + variance trigger MAD-based), Layer 2 classifier (7 feature + decision tree first-match v3.1.1), Layer 3 AAS context enrichment (severity, recommended_action, Stage 5 strategy)."*

**Su ADWIN (sezione 5.5.1):**
*"Sezione 5.5.1 è la prima parte didatticamente importante: spiego ADWIN da zero perché il classificatore poggia su quello. Il problema teorico delle finestre fisse — Bifet & Gavaldà 2007 — è che troppo corte generano falsi allarmi, troppo lunghe ritardano la detection. ADWIN adatta dinamicamente la finestra W, comprimendola in O(log|W|) bucket di capacità geometricamente crescente. Ogni bucket memorizza solo (sum, count), memoria limitata a O(log|W|) indipendentemente dalla lunghezza."*

*"Il test statistico (Figura 3 pag 42): confronta le medie dei sotto-finestra W0 (passato) e W1 (recente), e dichiara drift quando la loro differenza supera ε_cut derivato da Hoeffding. δ = 0.002 è il default di River e del paper originale — corrisponde a FAR teorico 0.2%, cioè circa 1 falso allarme ogni 500 finestre di monitoraggio. Per sensori a 0.1-1 secondo, è operativamente accettabile."*

*"Sezione operational trade-off: in DMCA, ogni falso allarme triggera uno Stage 5 cycle che richiede operator confirmation. Troppi falsi allarmi → approval fatigue → l'operatore approva senza guardare, e la human-in-the-loop si annulla. Empiricamente FAR = 0.000 nei miei test (oltre la garanzia teorica). Per asset SIL ≥ 3 raccomando δ = 0.0001 — più conservativo, tunabile via AAS DeploymentPolicy submodel."*

**Sul Layer 2 (pag 42-43):**
*"Layer 2 estrae 8 feature sulla baseline_window vs recent_window: F1 slope_total, F2 iqr_ratio (robust con cap a 10), F3 monotonicity, F4 KS statistic, F5 outlier_density, F6 plateau_ratio, F7 base_elevation, F8 max_delta_sigma (introdotta in v3.1). Le prime due sono difensive — F2 IQR invece di varianza perché gli spike non fanno esplodere la mediana dei quartili."*

*"L'albero di decisione (Eq. 7 a pag 43, Figura 4) è first-match wins con 8 regole. La numero 0 è il pre-check ABRUPT su F8 — se max_delta_sigma > 8σ e ks > 0.25, riconosci subito uno step gigante senza guardare la monotonicity (che è inaffidabile su finestre straddling). Le altre regole separano OUTLIER_DRIVEN, VARIANCE_SHIFT, GRADUAL, INCREMENTAL, DISTRIBUTION_SHIFT."*

**Sulla calibrazione iterativa:**
*"Il punto di onestà metodologica: l'albero non è uscito così, è il risultato di 5 versioni — v1 spec teorica, v2 introduzione della finestra split (straddle problem), v3 sostituzione var_ratio con iqr_ratio, v3.1 aggiunta F8 pre-check + abbassamento mono INCREMENTAL da 0.50 a 0.45, v3.1.1 correzione semantica del confine OUTLIER_DRIVEN da `>` a `≥`. Ogni cambio è tracciato — seed, osservazione empirica, nuovo accuracy. Documenti in `results/design_decisions/`."*

### 3.8 — Capitolo 5.6: Stage 5 Re-alignment (1 min · thesis p.44 · PDF p.45)

*"Stage 5 fa shadow deployment, improvement check, atomic swap con COPILOTCONFIRM. La policy SWAP/NO_SWAP dipende dal tipo di drift — Tabella 17 a pag 57: ABRUPT, GRADUAL, INCREMENTAL, DISTRIBUTION_SHIFT triggerano swap; **VARIANCE_SHIFT e OUTLIER_DRIVEN sono NO-SWAP** perché segnalano rumore di sensore o spike ambientali, non degrado del modello — alert al DS team o HW team senza model change."*

### 3.9 — Capitolo 7: Risultati (3 min · thesis p.48-52 · PDF p.49-53)

*"Pago 49 Tabella 11: benchmark completo. 8 modelli × 2 dataset, 20 run, GPU T4. Latency mean + P95, RAM peak, MAE, RMSE. Codice colore: green sotto 10ms (PatchTST 5.86ms, Lag-Llama 7.77ms), blue 10-100ms (MOMENT-L 29.66ms, Moirai-S 53.73ms, Moirai-L 72.59ms), orange 100-500ms (Chronos-T 166.82ms), red sopra 500ms (Chronos-L 829.96ms, TimesFM 2039.10ms)."*

*"Footnote importante: i modelli probabilistici (Moirai, Chronos, Lag-Llama) avevano MAE/RMSE come N/A nel canonical run del 7 aprile. Ho fatto un completion follow-up il 27 aprile che estrae point estimate dalla mediana del quantile — costo 0.013$. Valori marcati con † non sono direttamente comparabili a quelli raw-input. Lo dichiaro nei Limitations."*

**Sul paradosso SLA (sezione 7.5 a pag 52):**
*"Sezione 7.5 è il cuore quantitativo della tesi. Scenario: Jetson Nano SLA 50ms. Task-only TOPSIS senza filtro di ammissibilità ranka Moirai-Small come modello migliore perché ha MAE 0.228 e latenza T4 53.73ms. Ma proiettando T4 → Nano con conversion factor 10× (5-20× per datasheet manufacturer, prendo midpoint), Moirai-S diventa 537ms — **10.7× lo SLA**. PatchTST a 5.86ms × 10 = 58.6ms resta tollerabile."*

*"Calcolo missed alarm windows in un'ora di operation: PatchTST processa 122,900 finestre, Moirai-S ne processa 6,704. **94.5% delle finestre di monitoring sono silenziosamente perse** — senza che il sistema sollevi errori. Questo è il costo nascosto di selezionare per MAE soltanto."*

**Sull'ablation (sezione 7.6):**
*"Tabella 12 ablation: senza filtro zero-shot (task-only) il sistema sceglie PatchTST. Con tutti i constraint attivi, switch a Chronos-T. Risultato: il **zero-shot constraint è il filtro decisivo** — PatchTST è supervised e richiede fine-tuning, sotto zero-shot regime collassa (MAE = RMSE che vediamo in pag 49 e in 9.2)."*

### 3.10 — Capitolo 8: Case Study CMAPSS A (3 min · thesis p.53-56 · PDF p.54-57)

*"Cap 8.1 è la validation end-to-end del cycle completo. CMAPSS FD001 sensor s2, profilo Jetson Nano."*

**Stage 1+2 (Tabella 13 pag 54):**
*"Admissibility table 13: PatchTST, Lag-Llama, MOMENT-L passano lat + RAM sul Nano. Moirai-S (53.73ms) e tutti i Chronos sono esclusi. Sotto TOPSIS sensitivity (Tabella 14) il selettore sceglie PatchTST come deployable iniziale."*

**Stage 3 (8.1.3 pag 55):**
*"Quality gate 4-check: PatchTST con margin-adjusted latency 8.8ms passa, Moirai-S a 80.6ms è rejected. Costo di override: il 94.5% di sezione 7.5."*

**Stage 4 (8.1.4 pag 55):**
*"Drift sintetico: scaling lineare 1.0× → 2.0× sul 40% finale della serie. ADWIN δ=0.002 monitora rolling MAE. **Detection a t=1380**, MAE spike a 3.121 vs threshold 1.9918. Figura 7 mostra la timeline."*

*"Validation completa del classifier nella Tabella 16: calibration accuracy 100% su 15 trial (5 tipi × 3 seed), **held-out 92% su 25 trial** (5 seed mai usati per calibrare). FAR 0.000 in entrambi cohort. I 2 fallimenti residui sono INCREMENTAL borderline — seed 123 mono = 0.449 sotto soglia 0.45 di un soffio; seed 88 detection ADWIN tardiva con slope negativo che fa scattare la regola GRADUAL. Dichiarati nei Limitations."*

**Stage 5 (8.1.5 pag 56):**
*"Orchestrator seleziona **Chronos-T come replacement** (lightest zero-shot ammissibile). Re-alignment completato in **20 timestep**, MAE recovery a 0.174 a t=1400. Il cycle è girato end-to-end e validato."*

**Case Study B:**
*"Pag 57 Cap 8.2: dichiaratamente Future Work. Validation su dataset industriale reale è scope futuro — PHM Society / IEEE DataPort sono i candidati naturali. È una delle mie domande in chiusura."*

### 3.11 — Capitolo 9 + 10: Discussion e Limitations (1 min · thesis p.57-59 · PDF p.58-60)

*"Cap 9 ha 4 sottosezioni: 9.1 implicazioni pratiche per le PMI — 0.30$ di GPU per il benchmark significa adoption realistica per realtà non Fortune 500. 9.2 zero-shot collapse come signal diagnostico — il fatto che PatchTST e Lag-Llama mostrano MAE = RMSE è un segnale utile, non un bug; il quality gate validity-check lo intercetta. 9.3 il drift event come interfaccia MAS — l'evento strutturato è l'API tra Stage 4 e Stage 5, GAP 2. 9.4 vantaggio open-source su piattaforme vendor."*

*"Cap 10.3 Limitations a pag 59: aviation-adjacent dataset (CMAPSS non è manifatturiero nativo), single-site evaluation (solo T4, edge profile è proxy), modelli probabilistici con metriche incomplete, **1.5× SLA margin come Phase 1 design choice**. Tutto dichiarato esplicitamente."*

---

## Atto 4 — Le tue 3 domande (~5 min)

Le tieni nelle parole tue, non leggi. Le tre domande sono in `call_agenda.md`:

1. **Validation drift classifier** sufficiente al 92% held-out, o vuole espansione (DISTRIBUTION_SHIFT con scenario sintetico, più seed)?

2. **Surrogati Stage 3 (Ridge su rumore) e 5A (improvement factor da benchmark ratio)** vanno dichiarati nei Limitations come Phase 1, o vuole inferenza vera prima della consegna (e dove troviamo GPU)?

3. **Dashboard**: statica come ora (deterministica, sicura, GitHub Pages-ready), o backend FastAPI vero che chiama `pipeline/*.py` su input utente (più impressionante, 2-3 giorni di lavoro, server da gestire)?

---

## Watch-outs — se il prof "punzecchia"

**A. Tensione interna tra sezioni 7.5 / 7.6 / 8.1**: 7.5 usa **Moirai-S vs PatchTST** per il 94.5% windows. 7.6 ablation dice task-only → PatchTST, all-constraints → Chronos-T. 8.1.3 deploya PatchTST come quality-gate output. 8.1.5 re-aligna a Chronos-T. Sono **scenari diversi nello stesso capitolo**: 7.5 è "cosa succederebbe se TOPSIS task-only" (Moirai-S vince), 7.6 è ablation degli enforcing constraints, 8.1 è il cycle end-to-end vero. Se chiede, distingui chiaramente: *"7.5 è un controfattuale di selezione, 7.6 è ablation, 8.1 è il cycle reale"*.

**B. PatchTST collapse vs PatchTST deployable**: PatchTST ha MAE = RMSE = 1.303 (zero-shot collapse). Nel case study A 8.1.3 dici che passa il quality gate. Sembra contraddittorio. La risposta: *"PatchTST in CMAPSS modalità raw-input collassa, ma il quality gate Phase 1 verifica solo l'esecuzione meccanica del check; la validity-check più stretta che rileva MAE=RMSE è nei Future Work — è un caso noto, lo cito in 9.2"*.

**C. La conversion factor 10× T4→Nano** in sezione 7.5 è una stima da datasheet manufacturer (range 5-20×), non misurata su device. Se chiede, dici: *"è un proxy esplicitato — la calibration per-device è nel Future Work item 1 di 10.2"*.

**D. Il demo semplifica con TimesFM, la tesi usa Moirai-S** per il 94.5%. Sono scenari diversi: il demo prende TimesFM perché è il caso più estremo (2039ms vs 50ms = 40.8× SLA) ed è visivamente dirompente; la tesi prende Moirai-S perché è il caso *marginale* (53.73ms vs 50ms = 1.07× SLA) e quindi più realistico per dimostrare il valore della discriminazione. Se chiede: *"il demo enfatizza il caso estremo per chiarezza visiva, la tesi misura il caso marginale per realismo"*.

---

## Checklist 5 min prima

- [ ] PDF tesi aperto a pag 1 (uso Ctrl+G per salti)
- [ ] `factory_v4.html` aperto, scenario `nano_gradual` selezionato, NON in Play
- [ ] Questo file aperto in finestra di lato, non condivisa
- [ ] `call_agenda.md` aperto come backup (versione skim)
- [ ] Audio testato, share screen provato
- [ ] Acqua, notifiche off

**Se vai in panico, torna al demo. Premere Play su `factory_v4` è sempre una buona uscita.**
