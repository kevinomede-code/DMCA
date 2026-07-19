# Remediation DMCA — Parte A (chiusa) + Prompt Parte B pronti per Claude Code

> Documento operativo generato dal re-run + audit incrociato sul sorgente `thesis_draft.tex`.
> Ogni voce B è un **prompt isolato** già compilato col template §F.2. Copia-incolla in Claude Code, uno alla volta.
> Righe e chiavi `\cite{}` verificate sul sorgente reale (luglio 2026).

---

## PARTE A — stato: COMPLETA ✅

| # | Esito |
|---|---|
| A1, A2, A4–A12 | ✅ chiuse in audit (v3) |
| **A3** | ✅ **CHIUSA — decisione: citare Benmeziane diretto.** Si toglie il dettaglio della catena (la sua ref [28] + eq.1 ispirata a MnasNet). Confluisce in **B10**. |
| **A13** | ✅ **CHIUSA — re-run eseguito** (`pipeline/sla_rerun.py`, SLA=100ms+ceiling). Table 12: PatchTST/Lag-Llama s=1/100%, Moirai s=6/16.7%. Eq.11 **regge** (bound 110s ⊇ gap empirico ≤80s). Output in `results/missed_alarm/`. |

**Decisione dati Case Study B (scelta A):** la traccia PRONOSTIA usata è downsampled; nel testo si dichiara e si sposta l'argomento sul *rapporto* (Moirai 6× peggio, gap contenuto dal bound), non sui secondi assoluti. Questo entra negli edit D (non in Parte B).

---

## Come usare i prompt

Ordine consigliato (F.1): **B16 → B17** (priorità massima), poi B1–B15. Le voci ⚠️ toccano più punti: il prompt elenca **tutte** le righe.

Regola d'oro: lo **scope negativo** ("NON toccare") è ciò che più riduce il drift quando deleghi a un agente.

---

## B16 · [3] Maryanskyy — MISATTRIBUZIONE GRAVE ⚠️ — PRIORITÀ MASSIMA · (a)

Il paper è di terzi (Artem Maryanskyy, Uber, autore unico, arXiv:2603.20324) e riguarda l'**aggregazione di output** in pipeline multi-agente LLM (quale output tenere), **non** la selezione di modelli né Industry 4.0. Va rimosso dalla fondazione del gap e degradato ad analogia dichiarata.

```
Contesto: tesi LaTeX DMCA, file thesis_draft.tex. Intervento B16 — citazione [3] maryanskyy2026.
Problema: il paper (aggregazione di output in MAS di LLM) è citato come se formalizzasse
  il "selection bottleneck" per la selezione di modelli in Industry 4.0. Dice il contrario.

Modifica (5 punti):
  1) Righe 284-287: rimuovere l'aggancio "address it at the protocol level ... \cite{maryanskyy2026}".
     Riscrivere senza [3]: le architetture agentiche identificano la model selection come problema
     aperto di orchestrazione, ma non la ancorano a vincoli DT strutturati.
  2) Righe 293-297: la frase "the selection bottleneck ... lacks a structured ... description ...
     forcing it to rely on static configuration files~\cite{maryanskyy2026}" NON è nel paper.
     Rimuovere [3] e riformulare come osservazione propria/da fonti verificate (Lu, Shankar).
  3) Riga ~1773 (Gap Matrix): "Selection bottleneck formalisation in MAS for Industry 4.0"
     con \cite{maryanskyy2026} → togliere "Industry 4.0" e la citazione; il gap regge su Lu[67]/Shankar[68]/Abbasi[71].
  4) Righe 1977-1980: "As \cite{maryanskyy2026} documents, model selection has become a bottleneck..."
     → non è model selection. Sostituire con l'argomento reale (spread di parametri/latenza/licenza
     dei TSFM misurato dal nostro benchmark) senza [3].
  5) Riga ~5600 (C1/contributo): "...bottleneck identified by \cite{maryanskyy2026}" → rimuovere
     l'aggancio del contributo principale a [3].

Dove [3] PUÒ restare (una sola occorrenza, come analogia dichiarata in §2):
  "In the adjacent setting of multi-agent LLM output aggregation, Maryanskyy [3] finds that
   selector quality dominates generator diversity; an analogous result for model selection under
   deployment constraints has not been established." + marcare "(preprint, non peer-reviewed)".

Punti da toccare: righe 284-287, 293-297, ~1773, 1977-1980, ~5600, e ogni riga 2071 dove
  compare \cite{maryanskyy2026} in tabella.
NON toccare: numeri di benchmark, altre citazioni, la struttura del Problem Statement.
Dopo la modifica: ricompila e mostrami il diff dei soli punti toccati + la lista delle occorrenze
  residue di maryanskyy2026 (grep).
```

**Bib:** entry `maryanskyy2026` → autore **unico** Artem Maryanskyy; arXiv:2603.20324; DOI `10.48550/arXiv.2603.20324`; aggiungere `note = {Preprint, not peer-reviewed}`.

---

## B17 · [53] Jin — entry bib: 4 errori ⚠️ · (a)

```
Contesto: tesi LaTeX DMCA, bib. Intervento B17 — entry jin2023surveyts (references_master.bib).
Problema: venue inventata (IEEE TKDE), DOI che punta a un ALTRO paper, anno sbagliato, autore mancante.
Modifica (tieni la chiave jin2023surveyts per non rompere i \cite):
  journal → {arXiv preprint arXiv:2310.10196}
  year    → {2026}
  note    → {Version 3, 8 June 2026. Manuscript submitted to ACM.}
  doi     → {10.48550/arXiv.2310.10196}
  author  → aggiungere "Yaxuan Kong" in SECONDA posizione.
Punti da toccare: solo l'entry @...{jin2023surveyts} in references_master.bib
  (verifica se è duplicata anche in literature/bibtex/references_master.bib — se sì, allineare entrambe).
NON toccare: la chiave di citazione, altre entry.
Dopo la modifica: mostrami l'entry prima/dopo e conferma che il DOI risolve ad arXiv 2310.10196.
```

---

## B1 · [40] Banbury — due claim fabbricati ⚠️ · (a)

```
Contesto: tesi LaTeX DMCA, thesis_draft.tex. Intervento B1 — banbury2021mlperftiny.
Problema: due numeri attribuiti a Banbury sono errati.
Modifica:
  1) Riga 929 ("reporting up to $10{,}000\times$ latency variation" con MLPerf Tiny):
     il 10,000× è un power budget di un ALTRO lavoro (Banbury 2020), non latenza. Riscrivere:
     MLPerf Inference "precludes MCUs and resource-constrained platforms"; l'eterogeneità hardware
     (µW–W) motiva benchmark dedicati e misura per-device → DMCA usa proiezioni conservative in Fase 1
     e misura on-device in Fase 2.
  2) Righe 1474-1475 ("sub-1\,MB neural networks saturate ..."): distorto (MLPerf Tiny mostra il
     contrario: modelli 96–325KB girano su MCU) e misapplicato (le tue board sono SBC Linux 4GB).
     SGANCIARE da Banbury: l'argomento "Jetson/RPi = inferenza, retraining infattibile" regge da solo
     (memoria backprop ≈3–4× inferenza, no GPU adeguata su RPi4).
Punti da toccare: righe 928-930 e 1474-1476.
NON toccare: le occorrenze di banbury2021mlperftiny in tabelle (984, 1787) se solo descrittive.
Dopo la modifica: diff dei soli punti toccati.
```
**Bib:** DOI `10.48550/arXiv.2106.07597`.

---

## B2 · [67] Lu — fabbricazione, pezza portante GAP 1 · (a)

```
Contesto: thesis_draft.tex. Intervento B2 — lu2020drift.
Problema: riga ~1413 "Section~VII explicitly flags 'multi-model catalog drift response'" → sezione
  e frase inesistenti (Section VII = "Concept Drift in Other Research Areas").
Modifica: sostituire con l'inferenza onesta sulla tassonomia (loro Section 5): retraining / ensemble /
  adjustment sono tutte INTERNE al modello incumbente; la selezione da catalogo esterno non compare
  come classe → "DMCA introduce questa quarta classe".
Punti da toccare: righe 1411-1414 (e 1428 se ripete il claim).
NON toccare: altre citazioni di lu2020drift descrittive (1528).
Dopo la modifica: diff + verifica manuale che Section 5 elenchi le tre classi (DOI 10.1109/TKDE.2018.2876857).
```

---

## B3 · [68] Shankar — regge, 1 correzione · (a)

```
Contesto: thesis_draft.tex. Intervento B3 — shankar2022operationalizing (righe 1418+).
Problema: le due quote §4.2/§4.5.1 sono verificate ✓. Solo il terzo riferimento sbaglia oggetto:
  §5.1.2 inquadra il "Goldilocks alert problem" (quando allertare), NON il model replacement.
Modifica: correggere il terzo riferimento; riformulare l'inferenza su §4.5.2 (fallback models):
  replacement osservato = versioni più semplici/storiche/retrainate, nessuna selezione constraint-aware.
Punti da toccare: la frase attorno a riga 1418 che cita §5.1.2 / model replacement.
NON toccare: le due quote verbatim §4.2 e §4.5.1.
Dopo la modifica: diff dei soli punti toccati.
```

---

## B4 · [84] datasheet — stima propria spacciata per fonte · (a)

```
Contesto: thesis_draft.tex. Intervento B4 — "manufacturer datasheets ... conversion factor 5-20x".
Problema: una scheda prodotto non pubblica fattori di conversione. Righe 3810 e 5216-5218.
Modifica: riscrivere come ASSUNZIONE dichiarata con derivazione fisica:
  "In absence of published cross-device profiling for these model families, we assume a T4->Jetson Nano
   slowdown of 5-20x (midpoint x10), motivated by the memory-bandwidth ratio between the two devices
   (~320 vs 25.6 GB/s ~= 12.5x), the first-order predictor for batch-1 memory-bound inference;
   robustness to k is analysed in [sensitivity]."
  Sganciare o supportare altrove il claim "Jetson/RPi de-facto hosts for SMEs" (§2.12): NVIDIA non lo fa.
Punti da toccare: righe 3810-3812 e 5216-5219 (e ogni "conversion factor" a 4456, 5261, 5411, 5420, 5493
  va reso coerente con l'assunzione dichiarata, non con "datasheet").
NON toccare: i valori numerici di banda (320 / 25.6 GB/s) — verificali sulle schede NVIDIA prima.
Dopo la modifica: diff + conferma banda T4=320 GB/s e Nano=25.6 GB/s.
```

---

## B5 · [65/93] Sculley — 3 problemi + DUPLICATO ⚠️ · (a)

Nel sorgente esistono **due chiavi** per lo stesso paper: `sculley2015debt` (righe 1397, 1524, 1854) e `Sculley2015TechnicalDebt` (righe 1980, 2026, 4050) → doppia numerazione [65]/[93].

```
Contesto: thesis_draft.tex + bib. Intervento B5 — Sculley (dedup + 3 claim).
Problema:
  (a) riga ~4049-4050: "10% threshold consistent with the operational guidance of Sculley" → fabbricato
      (il paper tratta le soglie fisse come debito da EVITARE).
  (b) righe 1398-1401: "DMCA ... avoids CACE by design" → fianco scoperto (lo swap è il cambiamento
      CACE-massimale a valle).
  (c) "distribution shift as the principal source" → sovradichiarato.
  (d) duplicato chiavi sculley2015debt / Sculley2015TechnicalDebt.
Modifica:
  (a) il 10% è SCELTA DI DESIGN propria: soglia conservativa oltre la banda di rumore del surrogato
      (+-5%), configurabile via AAS DeploymentPolicy, calibrazione empirica = Fase 2. Citare la sezione
      "Fixed Thresholds in Dynamic Systems" come motivazione del "dichiarata configurabile, non hardcoded".
  (b) versione difendibile: DMCA evita il BURDEN del retraining; impatto a valle mitigato — non eliminato —
      da quality gate / shadow / grace / rollback.
  (c) "the principal source" → "among the sources".
  (d) UNIFICARE su una sola chiave (sculley2015debt) in tutte le occorrenze e rimuovere l'entry duplicata.
Punti da toccare: righe 1397-1401, ~1980, 2026, 4049-4050 (testo) + tutte le \cite{Sculley2015TechnicalDebt}
  → \cite{sculley2015debt} + rimozione entry duplicata nel bib.
NON toccare: la quote verificata "Changing Anything Changes Everything" (riga 1398).
Dopo la modifica: diff + grep che confermi zero occorrenze residue di Sculley2015TechnicalDebt.
```
**Bib:** DOI `10.5555/2969442.2969519`.

---

## B6 · [54] Liang — fabbricazione quantitativa ⚠️ · (a)

```
Contesto: thesis_draft.tex. Intervento B6 — liang2024tsfmkdd (survey metodologico, ZERO esperimenti).
Problema: numeri inventati in 3 punti.
  - Righe 1080-1082: "15--40\% performance degradation ... (Chronos-tiny, PatchTST-small) recover within
    5\% at one-tenth the cost" → nessuno di questi numeri esiste; "PatchTST-small" non esiste.
  - Riga 1123: riga tabella "Survey: 15--40\% zero-shot degradation on sensor data" con \yes.
Modifica:
  - Righe 1080-1082 → da citazione falsa a CLAIM DI CONTRIBUTO: "While methodological surveys [54] map
    the TSFM landscape, quantitative evidence of the zero-shot deployment gap on industrial sensor data
    remains scarce — a gap our benchmark addresses directly (Section 5)."
  - Riga 1123 → "Survey metodologico; flagga distribution shift come direzione aperta" e sostituire \yes con ~.
  - Correggere anche la nota bib dell'entry (o l'errore risorge in lavori futuri).
Punti da toccare: righe 1080-1082, 1123, entry liang2024tsfmkdd nel bib.
NON toccare: le altre righe della stessa tabella.
Dopo la modifica: diff + verifica che l'appendice "future directions" del survey citi "distribution shift"
  (DOI 10.48550/arXiv.2403.14735).
```

---

## B7 · [34] He — numero fabbricato + metrica sbagliata + doppio uso ⚠️ · (a)

```
Contesto: thesis_draft.tex + bib. Intervento B7 — he2025xai.
Problema:
  - Riga 788: "reduce appropriate switch rate (RSR) from 0.57 to 0.11" → numeri inventati; e RSR =
    "Relative positive Self-Reliance", NON "appropriate switch rate".
  - il nesso "fluent but poorly calibrated" → il meccanismo reale è "illusion of explanatory depth".
  - eventuale doppio uso di [34] per "XAI in manufacturing operator contexts" → è uno studio su loan
    approval con laypeople (N~306), zero manifatturiero.
Modifica righe 786-798: ancorare al finding reale:
  "He et al. [34] show that conversational and LLM-powered XAI can amplify over-reliance through an
   illusion of explanatory depth, even while improving subjective understanding and trust. This constrains
   the DMCA copilot: explanation confidence must track the quality-gate outcome, not the fluency of the
   generated text."
  Numeri reali se servono: switching fraction 0.522; accuracy umana 64.5% < 70% AI.
Punti da toccare: righe 786-798 + qualsiasi \cite{he2025xai} usato per contesto manifatturiero.
NON toccare: la citazione di Schemmer (righe 799-807).
Dopo la modifica: diff.
```
**Bib:** autori **Gaole He, Nilay Aishwarya, Ujwal Gadiraju**; DOI `10.1145/3708359.3712133` (arXiv 2501.17546); unificare eventuali chiavi doppie.

---

## B8 · [53] Jin — quote OK, soggetto sbagliato + prove nuove · (a)

(Coordinare con **B17** per il bib.)

```
Contesto: thesis_draft.tex. Intervento B8 — jin2023surveyts (prosa).
Problema:
  - Riga 1067: "review more than 150 works" → non verificabile (Tab.2 = 87 metodi, biblio = 296).
  - il gap va attribuito al soggetto giusto: NON "drift adaptation under-explored" (il paper lo dà per
    studiato) ma "integration of drift adaptation with large temporal models under-explored".
Modifica (riscrivere il blocco prosa su Jin, ~righe 1060-1070):
  "Jin et al. [53] survey large models for time series and spatio-temporal data. Their resource
   compilation (Table 3) lists 32 benchmark datasets spanning traffic, healthcare, weather, finance,
   video and event prediction; none is a manufacturing or prognostics benchmark — neither CMAPSS nor
   PRONOSTIA nor any analogous run-to-failure dataset appears. Their domain-specific taxonomy (Figure 3)
   covers transportation, finance and healthcare; manufacturing appears in neither the LLM- nor the
   PFM-based branch. Their outlook (Sec. 7.3) notes that while concept drift adaptation is established in
   conventional machine learning, 'their integration with large temporal models remains under-explored',
   and identifies domain-adaptive foundation models for industrial applications as a promising direction."
  Nella Gap Matrix: "Jin et al. 2023" → 2026; "zero industrial datasets" → "no manufacturing/prognostics
   benchmark among 32 datasets"; "drift adaptation under-explored" → "integration of drift adaptation with
   large temporal models under-explored".
  Togliere "more than 150 works" (riga 1067) o sostituire con conteggio dichiarato (87 metodi in Tab.2).
Punti da toccare: righe ~1060-1070 (prosa) + riga Gap Matrix su Jin.
NON toccare: il resto della sezione survey.
Dopo la modifica: diff.
```

---

## B9 · [59] Menghani — numeri decorativi · (a)

```
Contesto: thesis_draft.tex. Intervento B9 — menghani2023efficient (righe 1283-1287).
Problema: "INT8 delivers 2--4x latency improvement with <1% accuracy degradation on models above 10M
  parameters" → confonde size con latency; "<1%" non è claim generale; ">10M parameters" inventato.
Modifica righe 1283-1287:
  "INT8 quantisation is the standard post-training compression step for edge deployment, reducing model
   size ~4x and, with activation quantisation, inference latency [59]. The realised latency gain is
   hardware-dependent — integer-operator support on the target governs the actual speedup — which is why
   DMCA measures post-quantisation P95 latency on the target class rather than assuming a fixed factor."
Punti da toccare: righe 1283-1287.
NON toccare: righe 1279-1282 (descrizione del survey, corretta).
Dopo la modifica: diff + verifica che "2--8x"/"4x" nel survey siano riferiti a model SIZE (DOI 10.1145/3578938).
```

---

## B10 · [55] Benmeziane — regge, ritocchi + chiusura A3 · (a)

```
Contesto: thesis_draft.tex. Intervento B10 — benmeziane2021hwnas (righe 1164-1174).
Problema: etichette dei quattro assi imprecise; e (A3) il dettaglio della catena ref[28]/eq.1-MnasNet
  è fragile.
Modifica:
  - Righe 1167-1170: i quattro assi reali sono "search space, search strategy, acceleration technique,
    hardware cost estimation" (non "hardware performance estimation, target platform").
  - "dynamically changing hardware targets" (riga 1170): è parafrasi legittima di Sec. XI-C; se è tra
    virgolette, togliere le virgolette e citare Sec. XI-C.
  - A3: RIMUOVERE il dettaglio della catena (ref [28] + eq.1 ispirata a MnasNet) e citare Benmeziane
    diretto. Rimuovere anche il commento MnasNet a riga ~1250 se orfano.
Punti da toccare: righe 1164-1174 (+ commento 1250).
NON toccare: il framing "re-run per ogni nuovo hardware = problema aperto" (aggancio utile: DMCA lo evita).
Dopo la modifica: diff.
```
**Bib:** DOI `10.48550/arXiv.2101.09336`.

---

## B11 · [88, 89] — costo asimmetrico ⚠️ — fix ad alto rendimento · (a)

```
Contesto: thesis_draft.tex. Intervento B11 — "missed alarm order of magnitude more costly [88,89]".
Problema: riga 1927 "a missed alarm is typically an order of magnitude more costly than a false alarm
  [88,89]" → nessuna delle due fonti lo dice. Contraddizione: la tua nota bib per [89] dice "no missing
  alarm rate metric".
Modifica: ancorare l'asimmetria REALE alla scoring function PHM 2012 Challenge (dentro PRONOSTIA):
  "This asymmetry is institutionalised in PHM evaluation practice: the IEEE PHM 2012 Challenge scoring
   function [88] halves the score for every 5% of late RUL error but only every 20% of early error — a 4x
   steeper penalty for late predictions, reflecting the operational consensus that a missed alarm is more
   consequential than a premature one. Standard ML benchmarks instead report symmetric losses (MAE, RMSE)."
Punti da toccare: riga 1927 (prosa) + riga 2085 (tabella, "missed alarm cost is ignored").
NON toccare: il valore economico in EUR (voce D10, fonte diversa).
Dopo la modifica: diff + verifica costanti 5 (late) / 20 (early) nella §5 di PRONOSTIA.
```
**Bib [89]:** autori **Ayan Das, Dhaval Patel**; arXiv `2604.01532`.

---

## B12 · [71] Abbasi — tassonomia sbagliata + [72] da eliminare + regalo ✅ · (a)

Nel sorgente: `SemanticDriftModelDrivenDT2024` (= [71], due autori, tassonomia sbagliata, righe 1548-1552) e `SemanticDriftEvalFGCS2025` (= [72], riga 1553).

```
Contesto: thesis_draft.tex + bib. Intervento B12 — Abbasi (righe 1548-1567).
Problema: la tassonomia "model evolution / schema / concept drift" (righe 1549-1552) è INVENTATA.
  Le varianti reali sono quattro: data-driven drift, technical conceptual drift, knowledge conceptual
  drift, interpretation drift. Anche "first formal taxonomy" (riga 1549) non è rivendicato dagli autori.
Modifica righe 1548-1567:
  "Abbasi et al. [71] propose a formal classification of semantic drift across the modelling layers of a
   digital twin: data-driven drift (feature, label, concept and structural drift at the data layer),
   technical conceptual drift (models and metamodels diverging from the evolving system), knowledge
   conceptual drift (ontologies becoming outdated), and interpretation drift. They formalise vertical
   drift propagating across layers and horizontal drift within a layer. They identify four phases in
   managing semantic drift — identification, characterisation, maintenance and propagation — and
   explicitly scope their contribution to the first two. DMCA addresses the maintenance phase: given a
   detected and characterised drift, which model should replace the incumbent under deployment constraints."
  Togliere "first formal taxonomy". Autori [71] = Abbasi, Brimont, Pruski, Sottet (quattro).
  [72] SemanticDriftEvalFGCS2025: la valutazione piattaforme è già in [71] §5 (AzureDT + FIWARE NGSI-LD).
   Sostituire il claim "four DT frameworks" con: "[71, §5] evaluate AzureDT and FIWARE NGSI-LD ...".
   RIMUOVERE l'entry [72] dal bib e la sua \cite (riga 1553).
Punti da toccare: righe 1548-1567 + entry SemanticDriftEvalFGCS2025 nel bib.
NON toccare: la citazione Abdoune (righe 1556-1560) — ma vedi C2 (Farah vs Farid).
Dopo la modifica: diff + grep zero occorrenze di SemanticDriftEvalFGCS2025.
```
**Bib:** [71] DOI `10.1145/3652620.3688256`; [72] da rimuovere.

---

## B13 · [92] FactoryNet — autore fabbricato ⚠️ · (a)

```
Contesto: thesis_draft.tex + bib. Intervento B13 — FactoryNet2026 (righe 1970-1973).
Problema:
  - Autore INVENTATO nel bib ("Hao Zhang et al."); reali: Karim Othman, Jonas Petersen, Matei
    Ignuta-Ciuncanu, Camilla Mazzoleni, Federico Martelli, Alessandro Lombardi, Riccardo Maggioni,
    Philipp Petersen.
  - Riga 1973: "validates zero-shot cross-domain transfer ... in production cells" → sovradichiarato;
    il paper riporta FAIR cross-embodiment transfer su UNA coppia; dominio = manipolazione robotica +
    machining, non "production cells".
Modifica righe 1970-1973:
  "The recent FactoryNet corpus [92] — introduced by its authors as the first universal pretraining
   corpus for industrial time-series (51M datapoints, 23k task executions, six embodiments) — reports
   fair cross-embodiment transfer on a single evaluated source-target pair, and competitive anomaly
   detection from 24 schema-aligned signals. Its scope is robotic manipulation and machining; prognostics
   corpora such as CMAPSS and PRONOSTIA remain outside industrial pretraining efforts."
Punti da toccare: righe 1970-1973 + entry FactoryNet2026 (correggere autori) + rimuovere il duplicato
  presente in manufacturing_refs.bib.
NON toccare: i numeri 51M/23k/6 embodiments (esatti).
Dopo la modifica: diff + grep una sola entry FactoryNet2026.
```
**Bib:** DOI `10.48550/arXiv.2605.09081`.

---

## B14 · [52] Zeng — bib OK, due errori tecnici · (a)

```
Contesto: thesis_draft.tex. Intervento B14 — zeng2023dlinear (righe 1057-1059).
Problema:
  - "outperforms all Transformer variants on five of six tested benchmarks" → sono NOVE dataset;
    l'abstract dice "in all cases" (il corpo "in most cases").
  - "two-layer linear decomposition" → sono due rami paralleli da UN layer ("one-layer linear model").
  - "the strongest counter-argument" → valutazione contestata (PatchTST supera DLinear su molti dataset).
Modifica righe 1057-1059:
  "Zeng et al. [52] opened a still-unresolved debate on whether Transformer complexity is justified for
   time series (a one-layer linear model competitive across nine benchmarks). This contested picture is
   precisely why DMCA ranks on measured performance rather than architectural priors."
Punti da toccare: righe 1057-1059.
NON toccare: l'entry bib (corretta).
Dopo la modifica: diff.
```

---

## B15 · [51] TimeMixer — "first 2024" falso · (a)

```
Contesto: thesis_draft.tex. Intervento B15 — TimeMixer (riga 1055).
Problema: "the first 2024 architecture to treat inference efficiency as a first-class design goal" →
  tautologia difensiva ("first 2024") e falso (SparseTSF, FITS sono 2024 e progettati per l'efficienza).
Modifica riga 1053-1055:
  "TimeMixer [51] achieves competitive accuracy at significantly lower FLOPs, part of a 2024 wave treating
   inference efficiency as a first-class design goal (alongside FITS, SparseTSF)."
Punti da toccare: righe 1053-1055.
NON toccare: il resto del paragrafo sui modelli efficienti.
Dopo la modifica: diff.
```

---

## Nota igiene (Parte C) — da fare subito dopo B

Molti bib fix qui sopra si intrecciano con **C1** (campi `note` stampati), **C2** (dedup cross-file: Sculley, He, FactoryNet, Abdoune Farah/Farid), **C3** (autori placeholder), **C5** (refuso riga ~1480 "seven drift types" → cinque). Consiglio: chiudere B, poi un unico giro C1–C5 meccanico.
