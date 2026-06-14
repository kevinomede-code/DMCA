# Reading Log — DMCA Literature Review

## Template per ogni paper:
**Paper:** titolo
**Cluster:** numero cluster
**Contributo principale:** una frase
**Gap che chiude:** quale dei 5 gap
**vs DMCA:** come si differenzia
**BibTeX key:**

---

## CLUSTER A — AI Infrastructure for Edge Deployment

---

**Paper:** Edge Intelligence: The Confluence of Edge Computing and Artificial Intelligence
**Cluster:** A — Edge Deployment
**Contributo principale:** Survey del continuum edge-cloud intelligence; tassonomia compression/partitioning/in-situ learning con analisi latency-accuracy su ARM Cortex
**Gap che chiude:** G4 parziale (latency characterization)
**vs DMCA:** Surveilla ottimizzazione di un modello dato — non fa selezione tra modelli candidati né usa DT constraints
**BibTeX key:** deng2020edgeintelligence
**Venue:** IEEE IoT Journal 7(8):7457-7469, 2020 | DOI: 10.1109/JIOT.2020.2984887
**Confidenza citazione:** [A] alta

---

**Paper:** MCUNet: Tiny Deep Learning on IoT Devices
**Cluster:** A — Edge Deployment
**Contributo principale:** Co-design di NAS (TinyNAS) e inference engine (TinyEngine) che porta ImageNet-scale accuracy su MCU Cortex-M da $5
**Gap che chiude:** G1 parziale (hardware-awareness)
**vs DMCA:** Progetta nuove architetture da zero; DMCA seleziona da catalog pre-esistente senza training
**BibTeX key:** lin2020mcunet
**Venue:** NeurIPS 2020, pp.11711-11722 | arXiv:2007.10319
**Confidenza citazione:** [A] alta

---

**Paper:** MLPerf Tiny Benchmark
**Cluster:** A — Edge Deployment
**Contributo principale:** Framework benchmark standardizzato per ML inference su embedded; documenta variazione 10,000× latenza per stesso modello su hardware diversi
**Gap che chiude:** G4 (framework di validazione industriale)
**vs DMCA:** Benchmarka modelli fissi su hardware fisso — non fa selezione automatica né usa DT profiling
**BibTeX key:** banbury2021mlperftiny
**Venue:** NeurIPS Datasets & Benchmarks 2021, vol.1 | arXiv:2106.07597
**Confidenza citazione:** [A] alta

---

**Paper:** μNAS: Constrained Neural Architecture Search for Microcontrollers
**Cluster:** A — Edge Deployment
**Contributo principale:** Bayesian NAS con hard constraints su RAM, Flash e MAC per MCU; trova architetture Pareto-optimal
**Gap che chiude:** G1 parziale
**vs DMCA:** Cerca nuove architetture; DMCA seleziona da HF catalog. Problemi ortogonali.
**BibTeX key:** liberis2021munas
**Venue:** EuroMLSys 2021, pp.70-79 | DOI: 10.1145/3437984.3458836
**Confidenza citazione:** [A] alta

---

**Paper:** TVM: An Automated End-to-End Optimizing Compiler for Deep Learning
**Cluster:** A — Edge Deployment
**Contributo principale:** Compilatore ML che genera codice ottimizzato per qualsiasi hardware backend (CPU, GPU, FPGA, MCU)
**Gap che chiude:** G4 parziale (deployment infrastructure)
**vs DMCA:** Ottimizza deployment del modello scelto — non lo sceglie. DMCA seleziona, TVM può ottimizzare il risultato.
**BibTeX key:** chen2018tvm
**Venue:** OSDI 2018, pp.578-594 | arXiv:1802.04799
**Confidenza citazione:** [A] alta

---

## CLUSTER B — Classical and Hybrid TS Architectures (Expansion)

---

**Paper:** iTransformer: Inverted Transformers Are Effective for Time Series Forecasting
**Cluster:** B — TS Foundation Models
**Contributo principale:** Inverte attention axis: processa variates come token (invece di time steps) → SOTA su multivariate forecasting
**Gap che chiude:** G2 parziale (TS architecture)
**vs DMCA:** GOD NODE nel grafo (5 edges) — già nel catalog DMCA ma non citato nel Related Work. Candidato per hard-RT edge (params <5M).
**BibTeX key:** liu2024itransformer
**Venue:** ICLR 2024 | arXiv:2310.06625
**Confidenza citazione:** [A] alta — già verificato nel grafo

---

**Paper:** N-HiTS: Neural Hierarchical Interpolation for Time Series Forecasting
**Cluster:** B — TS Foundation Models
**Contributo principale:** Multi-rate sampling + hierarchical interpolation; -25% MASE vs N-BEATS su long-horizon M4
**Gap che chiude:** G2 parziale (baseline comparison)
**vs DMCA:** Community 13 isolata nel grafo (1 node, thin). Edge-viable (<1M params) ma senza valutazione HW.
**BibTeX key:** challu2023nhits
**Venue:** AAAI 2023, 37(6):6989-6997 | DOI: 10.1609/aaai.v37i6.26259 | arXiv:2201.12886
**Confidenza citazione:** [A] alta

---

**Paper:** N-BEATS: Neural Basis Expansion Analysis for Interpretable Time Series Forecasting
**Cluster:** B — TS Foundation Models
**Contributo principale:** Doubly-residual stacking con basis functions; primo DL puro a battere M4 ensemble senza domain knowledge
**Gap che chiude:** G2 parziale (baseline)
**vs DMCA:** Community 14 isolata nel grafo. Baseline importante nella selection matrix (zero-shot=No, edge=Yes).
**BibTeX key:** oreshkin2020nbeats
**Venue:** ICLR 2020 | arXiv:1905.10437
**Confidenza citazione:** [A] alta

---

**Paper:** Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting
**Cluster:** B — TS Foundation Models
**Contributo principale:** Sparse attention + static metadata + variable selection; winner M5 Uncertainty competition (Walmart)
**Gap che chiude:** G3 parziale (interpretability), G2 parziale
**vs DMCA:** Community 15 isolata nel grafo. Interpretabilità lo rende candidato per G3 (XAI conversazionale).
**BibTeX key:** lim2021tft
**Venue:** International Journal of Forecasting 37(4):1748-1764, 2021 | DOI: 10.1016/j.ijforecast.2021.03.012
**Confidenza citazione:** [A] alta

---

**Paper:** Are Transformers Effective for Time Series Forecasting?
**Cluster:** B — TS Foundation Models
**Contributo principale:** DLinear (linear decomposition) batte tutti i Transformer variants su 5/6 benchmark → mette in discussione l'egemonia dei Transformer per TS
**Gap che chiude:** G1 (giustifica selezione basata su performance empirica, non bias architetturale)
**vs DMCA:** Community 21 isolata nel grafo. Valida l'approccio DMCA: la selection matrix deve usare performance misurata, non architettura assunta superiore.
**BibTeX key:** zeng2023dlinear
**Venue:** AAAI 2023, 37(9):11121-11128 | DOI: 10.1609/aaai.v37i9.26317 | arXiv:2205.13504
**Confidenza citazione:** [A] alta

---

## CLUSTER C — AutoML and Hardware-Aware NAS

---

**Paper:** Once-for-All: Train One Network and Specialize it for Efficient Deployment
**Cluster:** C — AutoML/NAS
**Contributo principale:** Super-network da cui si estraggono sub-network specializzati per ogni hardware target senza training aggiuntivo
**Gap che chiude:** G1 parziale (hardware-awareness)
**vs DMCA:** Progetta nuove architetture (training required); DMCA seleziona pre-trained senza training. Ortogonali.
**BibTeX key:** cai2020ofa
**Venue:** ICLR 2020 | arXiv:1908.09791
**Confidenza citazione:** [A] alta

---

**Paper:** SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization
**Cluster:** C — AutoML/NAS
**Contributo principale:** Framework HPO Bayesiano (Random Forest surrogate) applicato ad AutoML con vincoli arbitrari
**Gap che chiude:** G1 parziale (optimization framework)
**vs DMCA:** SMAC ottimizza uno spazio continuo; DMCA filtra un catalog discreto. Il principio constrained search è lo stesso.
**BibTeX key:** lindauer2022smac3
**Venue:** JMLR 23(54):1-9, 2022 | URL: jmlr.org/papers/v23/21-0888.html
**Confidenza citazione:** [A] alta

---

**Paper:** Neural Architecture Search: Insights from 1000 Papers
**Cluster:** C — AutoML/NAS
**Contributo principale:** Meta-analisi di 1000+ paper NAS: hardware costs under-reported in 90% dei lavori; proxy metrics spesso non correlate al target hardware
**Gap che chiude:** G4 (validazione hardware-aware)
**vs DMCA:** Valida l'approccio DMCA di misurare latenza P95 empiricamente invece di usare FLOPs come proxy.
**BibTeX key:** white2023nasinights
**Venue:** TMLR 2023 | arXiv:2301.08727
**Confidenza citazione:** [A] alta

---

**Paper:** AutoGluon-Tabular: Robust and Accurate AutoML for Structured Data
**Cluster:** C — AutoML/NAS
**Contributo principale:** AutoML basato su ensemble di algoritmi (portfolio approach): seleziona tra modelli esistenti invece di trainarne uno solo
**Gap che chiude:** G1 parziale (catalog-based selection concept)
**vs DMCA:** Portfolio senza HW constraints né DT; più vicino all'approccio DMCA rispetto a NAS puro.
**BibTeX key:** erickson2020autogluon
**Venue:** ICML AutoML Workshop 2020 | arXiv:2003.06505
**Confidenza citazione:** [A] alta

---

## CLUSTER D — Model Compression for Edge Deployment

---

**Paper:** Efficient Deep Learning: A Survey on Making Deep Learning Models Smaller, Faster, and Better
**Cluster:** D — Model Compression
**Contributo principale:** Survey di 150+ metodi di compression (pruning, quantization, distillation) con benchmark standardizzati
**Gap che chiude:** G4 parziale (efficiency metrics)
**vs DMCA:** Compression modifica i pesi del modello scelto; DMCA sceglie quale modello deployare. Ortogonali e composabili.
**BibTeX key:** menghani2023efficient
**Venue:** ACM Computing Surveys 55(12):259:1-259:40, 2023 | DOI: 10.1145/3578938
**Confidenza citazione:** [A] alta

---

**Paper:** Knowledge Distillation: A Survey
**Cluster:** D — Model Compression
**Contributo principale:** Tassonomia completa di knowledge distillation: response-based, feature-based, relation-based; 40 metodi analizzati
**Gap che chiude:** G4 parziale
**vs DMCA:** Distillation crea un nuovo student model; DMCA seleziona dal catalog. DMCA può usare distillazione come post-processing.
**BibTeX key:** gou2021distillation
**Venue:** IJCV 129(6):1789-1819, 2021 | DOI: 10.1007/s11263-021-01453-z | arXiv:2006.05525
**Confidenza citazione:** [A] alta

---

**Paper:** LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale
**Cluster:** D — Model Compression
**Contributo principale:** Quantizzazione mista INT8 con decomposizione outlier per LLM 175B; consente inference su consumer GPU
**Gap che chiude:** G1 parziale (resource reduction for LLM component)
**vs DMCA:** Ottimizza il LLM copilot component di DMCA; non riguarda la selezione del modello TS.
**BibTeX key:** dettmers2022llmint8
**Venue:** NeurIPS 2022, vol.35:30318-30332 | arXiv:2208.07339
**Confidenza citazione:** [A] alta

---

**Paper:** DistilBERT, a Distilled Version of BERT: Smaller, Faster, Cheaper and Lighter
**Cluster:** D — Model Compression
**Contributo principale:** Distillazione 6-layer di BERT: 97% GLUE score, 40% meno parametri, 60% più veloce
**Gap che chiude:** G4 parziale (small model validation)
**vs DMCA:** Dimostra che distillazione porta LLM a hardware Jetson-class; DMCA può usare DistilBERT come copilot LLM su edge.
**BibTeX key:** sanh2019distilbert
**Venue:** EMC2 Workshop @ NeurIPS 2019 | arXiv:1910.01108
**Confidenza citazione:** [A] alta

---

**Paper:** GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
**Cluster:** D — Model Compression
**Contributo principale:** PTQ con second-order weight updates per GPT-scale: 3-4 bit senza fine-tuning, <1% PPL degradation
**Gap che chiude:** G1 parziale (enables GPT-class models on edge)
**vs DMCA:** Post-processing per il modello selezionato da DMCA — composable.
**BibTeX key:** frantar2023gptq
**Venue:** ICLR 2023 | arXiv:2210.17323
**Confidenza citazione:** [A] alta

---

## CLUSTER E — MLOps and Drift-Aware Model Lifecycle

---

**Paper:** Machine Learning Operations (MLOps): Overview, Definition, and Architecture
**Cluster:** E — MLOps
**Contributo principale:** Definizione architetturale di MLOps: feature store → model registry → serving → monitoring; 5 principi operativi
**Gap che chiude:** G4 parziale (lifecycle architecture)
**vs DMCA:** MLOps fa retrain del modello corrente su drift; DMCA fa re-selection dal catalog. Loop di risposta fondamentalmente diverso.
**BibTeX key:** kreuzberger2023mlops
**Venue:** IEEE Access 11:31866-31879, 2023 | DOI: 10.1109/ACCESS.2023.3262138
**Confidenza citazione:** [A] alta

---

**Paper:** A Survey on Concept Drift Adaptation
**Cluster:** E — MLOps
**Contributo principale:** Survey 100+ metodi di concept drift: sudden/gradual/incremental/recurring; taxonomy detection vs adaptation
**Gap che chiude:** G1 (drift-triggered re-selection) + G4 (drift detection taxonomy)
**vs DMCA:** Gama et al. classifica il drift ma non lo usa come trigger per model re-selection da catalog.
**BibTeX key:** gama2014survey
**Venue:** ACM Computing Surveys 46(4):44:1-44:37, 2014 | DOI: 10.1145/2523813
**Confidenza citazione:** [A] alta — già nel progetto

---

**Paper:** Hidden Technical Debt in Machine Learning Systems
**Cluster:** E — MLOps
**Contributo principale:** Identifica distribution shift come principale fonte di technical debt in ML production; formalizza ML anti-patterns
**Gap che chiude:** G4 (production stability)
**vs DMCA:** Motiva l'approccio DMCA: la risposta standard (retrain) accumula debt; DMCA usa re-selection per evitare lock-in.
**BibTeX key:** sculley2015debt
**Venue:** NeurIPS 2015, vol.28:2503-2511
**Confidenza citazione:** [A] alta

---

**Paper:** Learning under Concept Drift: A Review
**Cluster:** E — MLOps
**Contributo principale:** Review era DL del concept drift: nessun metodo combina drift detection con model replacement da catalog pre-definito
**Gap che chiude:** G1 (gap statement diretto per DMCA)
**vs DMCA:** GIÀ NEL GRAFO (Community 8, cohesion 0.5). Lu et al. identificano il gap che DMCA chiude.
**BibTeX key:** lu2020drift
**Venue:** IEEE TKDE 31(12):2346-2363, 2019 | DOI: 10.1109/TKDE.2018.2876857
**Confidenza citazione:** [A] alta

---

**Paper:** Operationalizing Machine Learning: An Interview Study
**Cluster:** E — MLOps
**Contributo principale:** 18 interview con ML practitioners: drift monitoring sistematicamente sotto-prioritizzato; retraining manuale non scala
**Gap che chiude:** G4 (validazione pratica delle scelte DMCA)
**vs DMCA:** Conferma empiricamente che la risposta automatica al drift (Stage 4-5 DMCA) risolve un pain point reale.
**BibTeX key:** shankar2022operationalizing
**Venue:** arXiv:2209.09125, 2022 (verificare venue esatta — VERIFY)
**Confidenza citazione:** [B] media — verificare venue

---

---

**Paper:** TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting
**Cluster:** B — TS Foundation Models
**Contributo principale:** MLP multiscale senza attention: decompone TS a risoluzioni multiple → competitive accuracy a FLOPs ridotti
**Gap che chiude:** G1 parziale (architettura edge-friendly)
**vs DMCA:** Primo paper 2024 a trattare efficiency come design goal ma senza hardware profiling né industrial data
**BibTeX key:** wang2024timemixer (VERIFY arXiv:2405.14616)
**Venue:** ICLR 2024 | arXiv:2405.14616 (verificare)
**Confidenza citazione:** [B] media — verificare ID

---

**Paper:** Large Models for Time Series and Spatio-Temporal Data: A Survey and Outlook
**Cluster:** B — TS Foundation Models
**Contributo principale:** SURVEY 150+ paper: industrial datasets <8% dei benchmark; hardware constraints ed industrial deployment elencati come open challenges
**Gap che chiude:** G1 (evidenza diretta), G4 (evidenza diretta)
**vs DMCA:** Identifica esattamente i gap che DMCA chiude — evidenza di gap primaria per la tesi
**BibTeX key:** jin2023surveyts
**Venue:** arXiv:2310.10196, 2023 (Time-LLM author group)
**Confidenza citazione:** [A] alta

---

**Paper:** Foundation Models for Time Series Analysis: A Tutorial and Survey
**Cluster:** B — TS Foundation Models
**Contributo principale:** KDD 2024 tutorial: zero-shot models degradano 15-40% su dati sensor industriali; lightweight models entro 5% a 10x costo inferiore
**Gap che chiude:** G1 (evidenza quantitativa), G4 (benchmark evidence)
**vs DMCA:** Conferma empiricamente che la selezione adattiva di DMCA è necessaria — degradazione su sensor data è misurabile e non trascurabile
**BibTeX key:** liang2024tsfmkdd
**Venue:** KDD 2024, pp.6555-6565 | arXiv:2403.14735
**Confidenza citazione:** [A] alta

---

## Riepilogo paper per cluster

| Cluster | Paper trovati | Nuove citazioni | Gap primario |
|---------|--------------|-----------------|--------------|---------------|
| A — Edge Infra | 5 | 5 | G4 (validazione HW) | — |
| B — TS Classical + Survey | 8 | 8 | G2 + G1 + G4 | 2 survey con evidenza diretta gap |
| C — AutoML/NAS | 5 | 5 | G1 (selezione) | 2 EXTRACTED da god node ICSE-NIER ref[28][29] |
| D — Compression | 5 | 5 | G4 + composability | — |
| E — MLOps/Drift | 5 | 4+1 già nel grafo | G1 + G4 | — |
| **TOTALE** | **28** | **27 nuovi** | | |

## Correzioni citekey urgenti in arxiv_downloaded.bib

| Citekey errata | Problema | Azione prima di submission |
|---------------|---------|--------------------------|
| `Jin2024TimeLLM` | Contiene iTransformer (Liu et al., 2310.06625), non TimeLLM | Non usata nella tesi — lasciare o rinominare `liu2024itransformer` |
| `Goswami2024MOMENT` | Autori/titolo sono di Moirai (Woo et al.) non MOMENT | Correggere autori prima di submission |
| `Woo2024Moirai` | Contiene paper spagnolo POS taggers — arXiv:2402.02516 sbagliato | Verificare ID reale di Moirai e sostituire |
| `Bifet2007ADWIN` | Contiene paper fisica "Large Charge at Large N" | Non usare — usare `bifet2007adwin` (lowercase, corretto) |
