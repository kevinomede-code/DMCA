# Thesis Autoresearch — AI Conversational Copilot for Complex Systems

## Contesto della ricerca

Tesi magistrale su un orchestratore MAS (Multi-Agent System) per Industry 4.0
che seleziona e adatta dinamicamente modelli open-source da HuggingFace in base
ai vincoli descritti dal Digital Twin aziendale, con interfaccia conversazionale
per operatori non tecnici e XAI integrata nel dialogo.

**Contributo originale centrale:**
"Dynamic Model-Context Alignment" — il sistema non sceglie il modello una sola
volta, ma lo rivaluta continuamente man mano che il Digital Twin aggiorna i
vincoli aziendali (nuovo hardware, cambio processo, drift del segnale).
Il copilot conversazionale è il meccanismo con cui l'operatore partecipa
a questo ciclo di riallineamento.

---

## I 5 Gap della tesi (riferimento sempre gaps.json)

- **GAP 1** — Selezione adattiva multi-criterio guidata da DT constraints
- **GAP 2** — Integrazione time-series + LLM nello stesso orchestratore
- **GAP 3** — XAI conversazionale integrata nel dialogo
- **GAP 4** — Framework di validazione industriale (safety, latenza, missing alarm)
- **GAP 5** — Fiducia calibrata nel tempo come obiettivo esplicito

---

## Architettura del sistema

```
Layer 1A — Stream ingestion    : OPC-UA → sliding window → quality gate
Layer 1B — Batch ingestion     : PDF/CSV → chunking → embedding → vector store
Orchestratore                  : retrieval + model inference + confidence scoring
Layer 2   — Communication      : result formatter → dispatcher → canali output
```

Il Digital Twin (formato AAS, standard IEC/Industry 4.0) è il profilo
strutturato dell'azienda che alimenta la matrice di selezione del modello.

---

## Workflow: gestione paper e bibliografia

I paper NON vengono aggiunti via API — vengono gestiti tramite file BibTeX
che Claude.ai genera e tu importi manualmente in Zotero.

**Struttura cartelle bibliography:**
```
bibliography/
├── gap1_model_selection.bib
├── gap2_ts_llm_integration.bib
├── gap3_conversational_xai.bib
├── gap4_industrial_validation.bib
├── gap5_trust_calibration.bib
├── foundamenta_dt.bib
└── foundamenta_hf_models.bib
```

**Workflow:**
1. Claude.ai (conversazione) trova e analizza i paper
2. Genera file .bib pronti per importazione Zotero
3. Tu scarichi il .bib e lo importi in Zotero (File → Import)
4. Aggiorna `results/paper_log.md` con i nuovi paper

**paper_log.md — formato riga:**
```
| data | titolo breve | gap | ruolo | score | implicazione |
```
dove ruolo = foundamenta | gap-evidence | future

---

## Workflow: benchmark modelli HuggingFace

**Dataset da usare (già in data/datasets/ dopo setup):**
- `CMAPSS` FD001-FD004 — RUL prediction turbofan NASA
- `ETT-h1` — forecasting elettrico
- `PRONOSTIA` — predictive maintenance cuscinetti

**Modelli baseline obbligatori in ogni benchmark:**
- `ibm/patchtst-base-etth1` — edge leggero ~5M params
- `Salesforce/moirai-1.1-R-small` — zero-shot
- `amazon/chronos-t5-tiny` — zero-shot univariato
- N-HiTS — baseline classica CPU

**Metriche da misurare sempre:**
- MAE, RMSE
- Latenza media CPU ms (100 inferenze)
- Latenza ONNX CPU ms (se convertito)
- RAM peak MB
- Params M

**Output:** `results/benchmarks/YYYY-MM-DD/nome_esperimento.csv`

---

## Workflow: concept drift simulation

1. Carica CMAPSS o ETT
2. Split: 60% baseline / 40% drift period
3. Inietta drift: scala valori × [1.2–2.0] o aggiungi rumore gaussiano crescente
4. Misura performance modello baseline nel periodo drift
5. Rileva drift con `river` o `alibi-detect`
6. Alla detection: seleziona nuovo modello dalla matrice in gaps.json
7. Misura: detection time, accuracy degradation, recovery time post-switch
8. Output grafici: `results/drift_experiments/`

---

## Workflow: AAS generation e constraint extraction

1. Crea AAS JSON sintetici in `data/aas/` (o usa AASbyLLM su PDF reali)
2. L'AAS deve contenere: hardware, latenza SLA, sensori, range operativi, protocollo
3. Parsa con `basyx-python-sdk`
4. Estrai vincoli → matrice di selezione in gaps.json → campo `selection_matrix`
5. Verifica compatibilità modello selezionato con i vincoli

---

## Ricercatori chiave da seguire

- **Yuchen Xia** (Univ. Stuttgart) — LLM + Digital Twin industriale
  github.com/YuchenXia — dissertazione completata, NO model selection da HF
- **Gaole He** (TU Delft) — Conversational XAI, over-reliance, trust
- **Maryanskyy** 2026 — Selection bottleneck in MAS (GAP 1 fondamenta)

---

## Struttura cartelle

```
thesis-research/
├── CLAUDE.md                  ← questo file
├── .env                       ← API keys (mai su git)
├── gaps.json                  ← definizione 5 gap + matrice selezione
├── bibliography/              ← file .bib per gap (importati in Zotero)
├── pipeline/
│   ├── hf_benchmark.py        ← benchmark modelli su CMAPSS/ETT
│   ├── drift_inject.py        ← simulazione concept drift
│   ├── aas_parser.py          ← lettura AAS e constraint extraction
│   └── report_gen.py          ← genera markdown risultati
├── data/
│   ├── datasets/              ← CMAPSS, ETT, PRONOSTIA
│   └── aas/                   ← AAS sintetici JSON
└── results/
    ├── paper_log.md           ← log paper trovati
    ├── benchmarks/
    └── drift_experiments/
```

---

## API Keys necessarie (da .env)

- `HF_TOKEN` — HuggingFace (per scaricare modelli privati o aumentare rate limit)
- `ANTHROPIC_API_KEY` — per autoresearch con Claude API
- `SEMANTIC_SCHOLAR_API_KEY` — opzionale, aumenta rate limit ricerca paper

**NON serve Zotero API** — i paper vengono gestiti tramite file .bib.

---

## Regole generali

- Non hardcodare mai API key — usa sempre `python-dotenv`
- Ogni script: logging su `results/logs/YYYY-MM-DD.log`
- Ogni risultato numerico: includi seed per riproducibilità
- Prima di fine-tuning pesante: chiedi conferma (potrebbe richiedere GPU)
- Nuova scoperta importante: aggiungi riga `[NEW-DISCOVERY]` in paper_log.md

---

## Fase corrente: Fase 1 — Simulazione pura (zero GPU)

**Tasks attivi:**
1. Benchmark zero-shot modelli HF su CMAPSS/ETT
2. Ablation study matrice multi-criterio
3. Concept drift simulation e recovery cycle
4. AAS constraint extraction testing

**Criterio per passare a Fase 2 (GPU):**
- Risultati stabili su almeno 3 dataset
- Architettura cap. 3 e cap. 4 della tesi fissata
- Codice training pronto per girare senza supervisione

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current

# DMCA Thesis — Claude Code Context File
# Aggiornato: 2026-04-21
# Leggi questo file PRIMA di qualsiasi operazione

## Chi sono e cosa sto facendo
Sono Kevin Omede, studente magistrale Politecnico di Torino × Beihang.
Sto completando la tesi "Dynamic Model-Context Alignment in Industry 4.0"
(DMCA) — un framework closed-loop a 5 stage per selezione automatica
di modelli HuggingFace guidata dal Digital Twin.

## Stack del progetto
- thesis_draft.tex — tesi in formato IEEE Transactions
- simulation_agent.py — agente Python con 5 workflow (W1 benchmark, W2 ablation, W3 drift, W4 report, W5 full DMCA cycle)
- pipeline/ — moduli Python del framework
- results/benchmarks/2026-04-07/ — benchmark GPU T4 CANONICI ($0.30)
- gaps.json — catalogo modelli e gap formali
- graphify-out/GRAPH_REPORT.md — knowledge graph (leggi sempre questo prima)
- assets/ — file AAS JSON per i 3 asset (DA CREARE)
- literature/ — paper e BibTeX (DA POPOLATE)

## Decisioni architetturali consolidate (NON modificare)

### Stage 1 — DT Profiling
- AAS Type 1 dinamico (file JSON, no BaSyx SDK)
- 3 asset: jetson_nano, raspberry_pi_4, jetson_orin_nx
- Modulo: pipeline/aas_parser.py (DA CREARE)
- BaSyx SDK = Future Work Phase 2

### Stage 2 — Model Selection
- TOPSIS con 4 criteri: MAE(0.5), latency(0.3), params(0.1), license(0.1)
- Normalizzazione min-max obbligatoria
- Tie-breaking: params_M → license → data_available → onnx_status
- Fallback M_adm=∅: evento strutturato + copilot alert
- Sensitivity analysis α/β come ablation aggiuntivo
- Modulo: pipeline/topsis_ranker.py (DA CREARE)

### Stage 3 — Edge Deployment
- Quality gate 4-check: latency, shape, validity, memory
- Validity include zero-shot collapse detection (MAE==RMSE)
- ONNX: supported/partial/unsupported per modello
- DeploymentState write nel file AAS dopo PASS
- Modulo: pipeline/quality_gate.py (DA CREARE)

### Stage 4 — Drift Detection (DMCA-Drift v3.1.1) — SOGLIE FINALI 2026-04-30
- Layer 1: ADWIN (River, δ=0.002) + secondary MAD-based variance trigger
- Layer 2: 8 feature + decision tree v3.1.1 (vedi sotto)
- Layer 3: AAS Context enrichment (severity, recommended_action, stage_5_strategy)
- 7 tipi: abrupt, gradual, incremental, variance_shift,
           distribution_shift, outlier_driven, unclassified
- NO SWAP per variance_shift e outlier_driven
- Modulo: pipeline/dmca_drift.py (COMPLETATO — versione v3.1.1)

**Feature v3.1.1 (NON modificare senza conferma):**
```
F1 slope_recent   = slope_raw × window_size  (delta totale finestra, NON normalizzato per range)
F2 iqr_ratio      = iqr(recent) / (iqr(baseline) + 1e-6), cap=10.0  (NON var_ratio)
F3 monotonicity   = fraction of positive diffs in recent_window
F4 ks_stat        = KS statistic baseline vs recent
F5 outlier_density= fraction of recent values outside baseline mean±3σ
F6 plateau_ratio  = fraction of recent diffs near-zero (diagnostico, non nel tree)
F7 base_elevation = (mean(baseline_window) - baseline_mae) / baseline_mae (diagnostico)
F8 max_delta_sigma= max(|diff(recent_window)|) / b_std  [NEW v3.1 — pre-check ABRUPT]
```

**Decision tree v3.1.1 — first match wins (NON modificare senza conferma):**
```
0. ABRUPT (pre-check): max_delta_sigma > 8.0 AND ks_stat > 0.25 AND slope > 0.3
   [NEW v3.1 — bypassa OUTLIER_DRIVEN quando mono < 0.50 per rumore di straddling]
1. OUTLIER_DRIVEN:      outlier_density >= 0.10  AND  ks_stat < 0.25
   [v3.1.1: >= invece di > — semantic correction, "almeno 10%" (DD-10)]
2. ABRUPT:              slope > 0.5   AND  monotonicity > 0.50  AND  ks_stat > 0.25
3. VARIANCE_SHIFT:      iqr_ratio > 1.5  AND  slope < 0.2
4. GRADUAL:             slope < 0.15  AND  outlier_density > 0.50
5. INCREMENTAL:         0.1 ≤ slope ≤ 0.5  AND  monotonicity > 0.45  [v3.1: 0.50→0.45]
6. DISTRIBUTION_SHIFT:  ks_stat > 0.40
7. UNCLASSIFIED:        default
```

**Deviazioni tracciate rispetto allo spec v3 originale (confermate 2026-04-22 → aggiornato 2026-04-30):**
- ABRUPT mono: 0.70→0.50 (finestra straddling ha mono≈0.53 strutturalmente per rumore)
- GRADUAL: slope<0.10 AND mono>0.60 → slope<0.15 AND od>0.50 (mono≈0.49 con rampa lenta σ=0.03)
- INCREMENTAL mono: 0.60→0.45 (v3.1: seed=1 mono=0.489 empiricamente; DD-09)
- F1: slope_norm(range) → slope_total(×n_r) [Opzione A confermata]
- Ordine regole: GRADUAL/INCREMENTAL precedono DISTRIBUTION_SHIFT (previene falso ks>0.40)
- F8 pre-check (v3.1): separazione ABRUPT da OUTLIER_DRIVEN con gradino fisico >>8σ (DD-09)
- R1 boundary (v3.1.1): od>0.10 → od>=0.10 — semantic correction (DD-10)

**Risultati canonici v3.1 validation (seeds 0-2, drift_validation_2026-04-30.json):**
```
Overall accuracy: 100%  FAR: 0.000  (n=3 seeds, usati per calibrazione)
ABRUPT/GRADUAL/INCREMENTAL/VARIANCE_SHIFT/OUTLIER_DRIVEN: 100%
```

**Risultati held-out v3.1.1 (5 tipi × 5 seed, drift_holdout_2026-04-30_v3_1_1.json):**
```
Overall accuracy: 92%   FAR: 0.000
ABRUPT:          100%
GRADUAL:         100%
INCREMENTAL:      60%   (2 failure residui — Limitations)
VARIANCE_SHIFT:  100%
OUTLIER_DRIVEN:  100%   (v3.1.1: boundary fix recupera seed=42 od=0.10 esatto)
Detection latency (mean): abrupt=15t, gradual=155t, incremental=132t,
                          variance_shift=38t, outlier_driven=57t
Percorso iterativo: v1→40% → v2→60% → v3→80% (iqr_ratio) → v3.1→100% val(n=3)
                    → v3.1.1→92% holdout (n=5) post boundary fix
```

**Failure residui held-out (Limitations, non affrontati):**
- INCREMENTAL seed=123: mono=0.449 < 0.45 (borderline; calibration, non semantic)
- INCREMENTAL seed=88: late detection ADWIN, slope negativo → GRADUAL rule fires
- (OUTLIER_DRIVEN seed=123 era unclassified in v3.1; risolto implicitamente in v3.1.1
  perché con drift_start corretti od=0.12 > 0.10 — già passava anche con strict rule)

### Stage 5 — Re-alignment
- Shadow deployment post-hoc (Phase 1), parallelo (Phase 2)
- Improvement threshold check prima di chiamare copilot
- Copilot L1/L2/L3 via llm_router.py (Haiku/Sonnet)
- COPILOTCONFIRM: timeout → reject se SIL>=2, approve se SIL<2
- Atomic swap + grace period 10 tick
- Audit trail JSONL append-only
- Modulo: pipeline/realignment.py (DA CREARE)

## Dati canonici benchmark (NON toccare)
File: results/benchmarks/2026-04-07/benchmark_results_modal.csv
Costo totale: $0.30 su GPU NVIDIA T4
8 modelli × 2 dataset (CMAPSS FD001, ETT-h1)
Risultato chiave: TimesFM MAE=0.006 ma latency=2039ms → escluso da SLA

## Risultati drift experiment (canonici)
File: results/drift_experiments/drift_cycle_results.json
Detection t=1380, Recovery t=1400, 20 timestep
ADWIN threshold=1.9918, δ=0.002
MAE baseline=0.796 → detection=3.121 → post-recovery=0.174
New model: chronos-t5-tiny

## Moduli DA CREARE (Categoria 1 — priorità massima)
1. assets/jetson_nano.aas.json
2. assets/raspberry_pi_4.aas.json
3. assets/jetson_orin_nx.aas.json
4. pipeline/aas_parser.py
5. pipeline/topsis_ranker.py
6. pipeline/quality_gate.py
7. pipeline/dmca_drift.py
8. pipeline/realignment.py
9. gaps.json — aggiornamento campi TOPSIS
10. simulation_agent.py — refactoring per usare nuovi moduli
11. simulator_phase2/README.md

## Moduli esistenti (NON rompere)
- pipeline/llm_router.py — router Tier 0-3 (funzionante)
- pipeline/simulation_agent.py — 5 workflow (funzionante): W1 benchmark, W2 ablation, W3 drift, W4 report, W5 full DMCA cycle
- pipeline/modal_jobs.py — benchmark GPU Modal (non toccare)

## Obiettivo finale
1. Completare Categoria 1
2. Aggiornare thesis_draft.tex con le nuove sezioni
3. Costruire simulator_phase2/ (sessioni successive)
4. Fine-tuning modelli su GPU del prof Yi Li
5. Demo video del ciclo DMCA completo

## Note importanti
- I dati in results/benchmarks/2026-04-07/ sono CANONICI
- NON rigenerare benchmark — sono già validati
- Phase 1 = implementazione attuale (batch, simulata)
- Phase 2 = simulatore dinamico streaming (futuro)
- BaSyx, OPTWIN, ADWIN-U = Future Work (non implementare)
- NEXUS non va menzionato

## Subcapitolo ADWIN — III-D-1 (DA AGGIUNGERE)
- Posizione: nuova sottosezione PRIMA di Layer 1
  nella sezione III-D del thesis_draft.tex
- Struttura: problema finestre fisse → bucket →
  Hoeffding bound → δ e FAR → implementazione
  batch vs streaming → garanzie teoriche
- Equazioni: eq:adwin-threshold, eq:adwin-far
- Figura: figures/adwin_explanation.tex (3 panel TikZ)
- δ=0.002: giustificato come default River/scikit-multiflow
  + paper originale Bifet 2007 + FAR=0 validato empiricamente
- Paper chiave: Bifet2007ADWIN (DOI confermato),
  Moharram2022ADWINpp, Tosi2023OPTWIN,
  NowakAssis2025ADWINU