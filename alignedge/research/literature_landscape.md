# Literature Landscape — AI Edge Deployment × Coverage × AlignEdge

**Data:** 2026-07-09 · **Metodo:** graphify knowledge graph (95 file tesi, 40 community) + web search mirata 2025-2026 sui 5 filoni del brief.
**Uso:** base per `technical_contribution.md` (Fase 3) e per armare tecnicamente la conversazione EdgeNext.

---

## A · Corpus già ingested (tesi, da graphify) — fondamenta consolidate

### Drift & MLOps
| Paper | Insight 1-line |
|---|---|
| Bifet 2007 (ADWIN) | Finestra adattiva con Hoeffding bound: garanzia formale su FAR — base di DMCA Layer 1 |
| Gama 2014 (drift survey) | Tassonomia drift canonica (abrupt/gradual/incremental) — DMCA la estende a 7 tipi |
| Lu 2020 (drift under DL) | Detection→understanding→adaptation: il ciclo che DMCA chiude automaticamente |
| Shankar 2022 (MLOps practices) | Retraining cadence in produzione è "unscientific" — evidenza del vuoto operativo |
| Kreuzberger 2023 (MLOps) | Pipeline MLOps standard non contempla constraint hardware edge |
| Omar 2024 (detector comparison) | Confronto detector con trade-off energetici — rilevante per edge budget |

### Hardware-aware selection & TinyML
| Paper | Insight 1-line |
|---|---|
| Benmeziane 2021 (HW-NAS survey) | Diversità piattaforme hardware = motivazione diretta di GAP 1 |
| White 2023 (NAS survey) | Constraint hardware sistematicamente under-reported nei benchmark NAS |
| Tan 2019 / Lin 2020 / Cai 2020 (MnasNet, MCUNet, OFA) | Famiglia HW-aware NAS: ottimizzano il *design*, non la *selezione a runtime* |
| Banbury 2021 (MLPerf Tiny) | Metriche accuracy+latency+energy standard — ma per-inference, mai coverage su workload |
| David 2021 (TFLite Micro) | Vincolo memoria come first-class constraint |
| Dettmers 2022 / Frantar 2023 / Lin 2024 (int8, GPTQ, AWQ) | Quantizzazione = leva di OPTIMIZE nel verdict audit |

### Time-series foundation models
| Paper | Insight 1-line |
|---|---|
| Nie 2023 (PatchTST) | Il vincitore coverage su Bearing 3_2 (85%) — edge-friendly by design |
| Ansari 2024 (Chronos) · Das 2024 (TimesFM) · Rasul 2023 (Lag-Llama) · Goswami 2024 (MOMENT) · Woo 2024 (Moirai) | Zero-shot TSFM: accuracy portabile, coverage NO — TimesFM MAE 0.006 ma 2039ms latency (escluso da SLA) |
| Jin 2023 (survey, Table 3) | Nessun benchmark industriale nei TSFM survey — evidenza GAP 4 |

### DT, AAS, XAI, MAS
| Paper | Insight 1-line |
|---|---|
| Xia 2023-2025 (Stuttgart, serie DT+LLM) | LLM+DT industriale maturo, ma zero model selection da HF — spazio DMCA intatto |
| Shi 2024 (ZDM AAS) | AAS come vocabolario standard per constraint — valida Stage 1 |
| He 2025 (conversational XAI) · Schemmer 2023 (appropriate reliance) | Fiducia calibrata = requisito del copilot L1/L2/L3 |
| Maryanskyy 2026 (selection bottleneck MAS) | Il collo di bottiglia della selezione in MAS — fondamenta GAP 1 |

---

## B · Literature nuova 2025-2026 (non ancora ingested) — i 5 filoni del brief

### B1 · Edge AI deployment challenges
| Paper/Report | Insight 1-line |
|---|---|
| [On-Device AI survey, ACM CSUR 2025 (arXiv 2503.06027)](https://arxiv.org/abs/2503.06027) | Survey di riferimento su-device: drift, heterogeneity, OTA come challenge aperti |
| [Edge AI Vision Alliance — "The Deployment Problem" (2025-12)](https://www.edge-ai-vision.com/2025/12/why-edge-ai-struggles-towards-production-the-deployment-problem/) | ~70% dei progetti Industry 4.0 muore in pilot; <1/3 org con edge AI deployed — il pain è il deployment, non il modello |
| [Generative AI at the Edge, ACM Queue](https://queue.acm.org/detail.cfm?id=3733702) | GenAI su edge amplifica il mismatch modello-hardware |
| [Embodied FMs at the Edge survey (arXiv 2603.16952)](https://arxiv.org/html/2603.16952v1) | Constraint di deployment e mitigazioni per FM embodied — conferma fleet fragility cross-vendor |

### B2 · SLA coverage vs accuracy (il filone più vicino ad AlignEdge)
| Paper | Insight 1-line |
|---|---|
| [SneakPeek (arXiv 2505.06641)](https://arxiv.org/pdf/2505.06641) | **⚠ PRIOR ART PIÙ VICINO**: model selection data-aware + scheduling per inference serving su edge — accademico, scheduler runtime, non audit on-HW |
| [EdgeServing (arXiv 2605.05527)](https://arxiv.org/pdf/2605.05527) | Deadline-aware multi-DNN serving: ottimizza SLO violation ratio — il KPI cugino del coverage, ma a livello serving-system |
| [ML Inference Scheduling with Predictable Latency (arXiv 2512.18725)](https://arxiv.org/abs/2512.18725) | Latency predicibility come obiettivo di scheduling GPU |
| [Jellyfish (Springer RTS 2024)](https://link.springer.com/article/10.1007/s11241-024-09418-4) | Soft guarantee su SLO end-to-end su reti edge dinamiche |
| DeepRT (arXiv 2105.01803) | Real-time scheduler per CV su edge — la real-time community tocca ML ma non misura coverage per-model |

**Lettura:** la serving/scheduling community *ottimizza* il rispetto degli SLO dentro un sistema che controlla. Nessuno *misura e certifica* la coverage di un modello del cliente sul suo hardware come servizio — è la differenza tra costruire lo scheduler e fare l'audit.

### B3 · TSFM: valutazione operativa e selezione
| Paper | Insight 1-line |
|---|---|
| [Operational Viability of TSFMs (arXiv 2605.24381)](https://arxiv.org/html/2605.24381) | Primo paper che valuta TSFM su vincoli operativi (latency, privacy) — accademia sta arrivando sul nostro terreno, senza HW reale |
| [TSFM benchmarking challenges (arXiv 2510.13654)](https://arxiv.org/pdf/2510.13654) | GIFT-Eval/FoundTS/TSFM-Bench: benchmark accuracy-centric, leakage issues — zero on-hardware |
| [MONAQ (arXiv 2505.10607)](https://arxiv.org/pdf/2505.10607) | Multi-objective NAS per TS su device constrained — design-time, non runtime re-selection |
| [APEX (arXiv 2606.11553)](https://arxiv.org/pdf/2606.11553) | TSFM nativo per wireless edge ops — un vendor-model in più da benchmarkare nel catalogo |

### B4 · AI Act compliance layer
| Fonte | Insight 1-line |
|---|---|
| [CSA — EU AI Act High-Risk Readiness Gap](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-compliance-deadline-20/) | Enterprise impreparate sulla deadline high-risk ago 2026: gap di readiness documentato |
| [Raconteur — technical audit guide 2026](https://www.raconteur.net/global-business/eu-ai-act-compliance-a-technical-audit-guide-for-the-2026-deadline) | L'audit tecnico (non paperwork) è la parte dura: logging Art. 12, post-market monitoring |
| [Legalnodes — AI Act 2026 updates](https://www.legalnodes.com/article/eu-ai-act-2026-updates-compliance-requirements-and-business-risks) | Update mag 2026: alcune categorie high-risk slittano a dic 2027, le altre restano ago 2026 — **verificare quale categoria copre PdM industriale prima di usarlo nel pitch** |
| Nota trasversale | Il tooling compliance esistente è LLM/enterprise-oriented (governance, prompt logging); nessuno copre logging + drift monitoring **on-device industriale** |

### B5 · Missed-alarm cascade in PdM
| Fonte | Insight 1-line |
|---|---|
| [Causal vs Correlation AI for PdM (arXiv 2512.01149)](https://arxiv.org/pdf/2512.01149) | Asimmetria costi quantificata: missed failure $25k vs false alarm $500 (CNC), ratio 20:1–100:1 — numeri citabili per slide 2 |
| Letteratura PdM industriale (Stage 1-2 bearing detection) | Lead time ultrasonic/vibration = settimane; con SLA violata su edge il lead time crolla a secondi — il collegamento coverage→lead time è NOSTRO, non in letteratura |

---

## C · I gap dove AlignEdge contribuisce (5)

1. **Coverage come metrica di primo livello misurata on-hardware.** Serving papers ottimizzano SLO violation dentro sistemi propri; benchmark TSFM sono accuracy-centric; MLPerf misura latency per-inference. Nessuno misura/certifica la frazione di predizioni in-tempo di un modello cliente sul suo chip sotto il suo workload. *(= slide 4, validato dalla literature)*
2. **Loop chiuso drift→re-selection sotto vincoli hardware.** Drift literature è data-side, serving literature è latency-side: DMCA è l'unico framework che classifica il drift E ri-seleziona il modello dentro i constraint AAS. SneakPeek si ferma allo scheduling.
3. **Valutazione operativa TSFM su hardware reale.** arXiv 2605.24381 apre il tema ma senza device fisici; GIFT-Eval non ha né hardware né industriale. Il benchmark T4+edge canonico è un asset che l'accademia sta appena iniziando a chiedere.
4. **Compliance AI Act per edge industriale.** Art. 12 logging + post-market monitoring esistono come requisito, il tooling è cloud/LLM-oriented: l'audit trail on-device di AlignEdge è il pezzo mancante. (⚠ verificare categoria Annex III per PdM prima di venderlo come mandatory.)
5. **Quantificazione missed-alarm cascade da SLA coverage.** Il costo del missed alarm è noto (20:1–100:1); il *legame causale* coverage→missed alarm→cascade non è in letteratura. `missed_alarm_simulation.py` + PHM 2012 è contributo originale pubblicabile.

## D · Citation graph (cluster → dove alimenta AlignEdge)

```
ADWIN/drift (Bifet→Gama→Lu→Omar) ──────────┐
                                            ├─→ DMCA Stage 4 (drift classifier v3.1.1)
Shankar/Kreuzberger (MLOps ops gap) ────────┘
HW-NAS (Benmeziane→White→MCUNet/OFA) ──────→ DMCA Stage 2 (TOPSIS) ←── ⚠ SneakPeek 2025 (prior art vicino)
TSFM (PatchTST/Chronos/TimesFM/Moirai...) ──→ catalogo modelli audit ←── GIFT-Eval (accuracy-only)
Serving SLO (Jellyfish→EdgeServing→2512.18725) → definizione coverage (loro: sistema; noi: audit per-model)
PdM cost asymmetry (2512.01149) ────────────→ missed-alarm cascade (contributo nostro)
AI Act (CSA/Raconteur 2026) ────────────────→ compliance annex del report audit
Xia DT+LLM / Shi AAS ───────────────────────→ Stage 1 constraint extraction
```

## D-bis · Deep-read notes sui due prior art (2026-07-09)

**SneakPeek (Wolfrath/Frink/Chandra, UMN, arXiv 2505.06641, mag 2025 — cs.DC).**
Scheduler per inference serving su edge: quando l'hardware non scala, degrada l'accuracy scegliendo dinamicamente il modello ("accuracy scaling"). Contributi: (1) dimostra che gli scheduler che usano accuracy profilata sono biased verso la label distribution del test set; (2) "SneakPeek models" = modelli ML che stimano l'accuracy attesa *sul dato corrente*; (3) priority che bilancia accuracy vs deadline, con batching greedy per evitare swap in/out dalla GPU. Task: classificazione (3 app real-world), non time-series forecasting/PdM. Vicinanza a DMCA: seleziona modelli sotto deadline su edge. Distanze: è un runtime dentro un sistema che controlli, non un audit di modelli del cliente; non misura né riporta coverage come KPI; nessun drift detection (la "data-awareness" è per-request, non temporale); nessun vincolo AAS/hardware dichiarativo; nessun costo missed-alarm.

**Operational Viability of TSFMs (Soni/Das/Guduguntla, Google, arXiv 2605.24381, mag 2026).**
Valuta TimesFM 2.0/2.5, Chronos vs XGBoost/LSTM/PatchTST/DLinear su 4 regimi (Traffic, ETTh1, Exchange, M4). Risultati chiave: (1) "Throughput Gap" strutturale — FM su GPU 200–1764ms vs specialisti su CPU <120ms (XGBoost 0.18ms), costo ~1000×; (2) "Inference Rigidity" — gli FM zero-shot sono congelati, il drift locale non è correggibile con retraining → servono shadow deployment (= esattamente la nostra Stage 5); (3) regime map generalist vs specialist; (4) propone **Complexity Router**: 4 feature statistiche per-serie (spectral entropy ≥0.24, CoV ≥0.22, seasonal autocorr ≥0.72 o <0.50, trend R²<0.05), route-to-FM se ≥2 soglie. Vicinanza a DMCA: routing multi-criterio tra classi di modelli, motivato da vincoli operativi. Distanze: routing per *caratteristiche statistiche della serie*, non per *vincoli hardware/SLA del deployment*; nessun hardware edge fisico (loro stessi dicono che su edge il footprint FM è "prohibitive" — e si fermano lì); statico (nessun re-alignment loop); nessuna metrica coverage; niente industriale/PdM. Conferma indipendente di 2 nostri claim: TimesFM escluso da SLA (loro: throughput gap; noi: 2039ms su T4) e necessità di shadow deployment per FM drift.

**Sintesi per il novelty statement:** entrambi validano il problema (selezione modello sotto vincoli operativi è reale e attuale) e nessuno dei due occupa la posizione AlignEdge: audit on-hardware per-model di coverage SLA + drift classification + re-selection loop chiuso su edge industriale. SneakPeek = scheduler senza drift né audit; Google = analisi cloud senza hardware né loop.

## E · Azioni

- [x] ~~Leggere per intero **SneakPeek** e **arXiv 2605.24381**~~ → fatto, vedi D-bis
- [ ] Verificare classificazione Annex III del PdM industriale (impatta claim slide 5)
- [ ] Ingest dei paper B1-B5 in graphify + .bib per Zotero (prossima sessione AutoResearchClaw)
- [ ] Citare 2512.01149 per l'asimmetria costi al posto di fonti vendor
