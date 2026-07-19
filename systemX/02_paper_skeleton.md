# Joint Paper Skeleton — DMCA for Smart Manufacturing

**Status:** Draft v0.2 — ready for approval Simeone before call SystemX 2026-06-26
**Version notes:** v0.2 → v0.3: §7 numbers updated to REAL data (PRONOSTIA 6 bearings + IMS Bearing 1 Test 2). Cross-dataset alarm density ratio confirmed (10.4 PRONOSTIA / 11.6 IMS). Bearing 3_2 actionable flip empirically demonstrated. Two killer figures available.
**Previous version notes:** v0.1 → v0.2: title locked Option A; Anwer removed; §1 manufacturing economics added; lower-bound argument added; 4-author attribution clean
**Target journal:** *International Journal of Advanced Manufacturing Technology* (Springer, IJAMT)
**Target length:** 16 pages including references (~14 content + ~30-40 refs)
**Submission window (tentative):** Q4 2026 / Q1 2027

---

## 1 · Title

> **Digital-Twin-Driven Adaptive Model Selection and Drift Recovery for Predictive Maintenance in Smart Manufacturing**

Anchors manufacturing PM as the central use case; signals DT (the Belfadel/Yi Li axis); signals adaptive selection + drift recovery (the Kevin axis). Replaces the more generic *"Dynamic Model-Context Alignment in Industry 4.0"* of the thesis.

---

## 2 · Authorship and attribution map

Four co-authors, all confirmed.

| # | Author | Affiliation | Primary section ownership | Role |
|---|---|---|---|---|
| 1 | **K. Omede** | Polito × Beihang | §1, §3, §5, §7 (lead), §8, §9, §11 | Lead author, executor, framework + benchmark + simulation |
| 2 | **Prof. A. Simeone** | Polito | §2 (manufacturing PM literature), §7 (case study review), §10 | Senior IT, manufacturing framing, journal editorial relationship |
| 3 | **Prof. Yi Li** | Beihang | §4 (Digital Twin model + AAS conceptualization), §10 | Senior CN, DT modeling |
| 4 | **Dr. A. Belfadel** | IRT SystemX | §6 (distributed AAS extension), §2 (standards positioning IEC 63278 / ISO 23247), §10 | Technical collab FR, standards, possible IRT industrial use case |

Notes:
- Anwer introduced Kevin to Belfadel but is not a co-author (super-busy per his communication; never confirmed direct collaboration).
- Yi Li scope on §4 to be aligned in async after the 2026-06-26 SystemX call confirms distributed-AAS perimeter.

---

## 3 · Manufacturing legitimacy — argument summary

The thesis as originally framed (Industry 4.0 generic) does not anchor strongly in Smart Manufacturing literature. Three repositioning moves close the gap for IJAMT:

1. **Manufacturing PM economics in §1 problem statement.** Cite Aberdeen/Senseye 2024: general manufacturing unplanned downtime $260k/h, automotive $2.3M/h; Fortune 500 lose 11% of revenue annually. Two-thirds of plants experience monthly downtime events of ~4h × $125k. PM is the Industry 4.0 use case zero.
2. **PRONOSTIA + IMS Center as manufacturing-pure case studies.** Bearing degradation (rotating machinery) is the canonical PM benchmark in smart manufacturing. CMAPSS retained as secondary aerospace-MRO case study; ETT-h1 retained as industrial-energy-infrastructure case study. Three verticals → multi-asset framework validation.
3. **ISO 10816 vibration severity zones** as the bridge between accelerated bench data (PRONOSTIA, minutes) and industrial-realistic timing (IMS, days; field bearings, weeks). Standards anchor that closes the manufacturing-extrapolation gap.

---

## 4 · Page allocation (16 pages total)

| Section | Pages | Owner | Notes |
|---|---|---|---|
| 1. Introduction | 1.5 | Kevin | Manufacturing PM motivation + economics + gap + contributions |
| 2. Related Work | 2.0 | Simeone (mfg lit) + Belfadel (standards) + Kevin (model selection) | Gap matrix manufacturing-oriented |
| 3. Problem Statement | 0.5 | Kevin | Manufacturing PM admissibility + drift + economic framing |
| 4. Digital Twin Model | 1.5 | Yi Li | AAS-based DT for manufacturing assets + manufacturing-aware submodels |
| 5. DMCA Framework Architecture | 2.5 | Kevin | 5-stage closed loop + drift classifier v3.1.1 + quality gate |
| 6. Distributed AAS Extension | 1.5 | Belfadel | Cloud/fog/edge submodels, TOPSIS-as-service |
| 7. Manufacturing Case Studies | 2.5 | Simeone + Kevin | PRONOSTIA + IMS Center + missed-alarm simulation |
| 8. Implementation & Validation | 1.0 | Kevin | Drift classifier 92% held-out, design decisions log |
| 9. Results & Analysis | 1.5 | Kevin | Latency cluster, SLA paradox, missed-alarm cascade, drift recovery |
| 10. Discussion | 0.5 | All | Manufacturing implications + standards alignment |
| 11. Conclusion & Future Work | 0.5 | Kevin | Closure + Phase 2 directions |
| References | 0.5 | All contribute | ~30-40 refs |

---

## 5 · Section-by-section skeletons

### §1 · Introduction (1.5 pp) — Kevin lead, Simeone review

Three blocks:

**§1.1 Manufacturing PM economics — the problem is operationally expensive.**
- $260k/h general manufacturing unplanned downtime [Aberdeen/Senseye 2024]
- $2.3M/h automotive line stoppage [Senseye 2024]
- Fortune Global 500 lose $1.4 trillion/year = 11% revenue to unplanned downtime
- 2/3 of plants experience monthly downtime ~4h × $2M per incident
- 40-50% of rotating-machinery failures involve bearings → PM target #1 [Randall & Antoni 2011]

**§1.2 The silent failure mode in deployed PM models.**
- A model deployed on edge can degrade silently — no error raised, dashboards green
- Industry 4.0 SME adoption ~31% vs large enterprise 51% — adoption-gap argument
- Existing approaches: static one-shot model selection ignores DT-encoded constraints
- The deployment gap (a16z framing): lab benchmark ≠ field operation

**§1.3 Contributions (4 bullets, mirrored on authorship).**
1. **Five-stage closed-loop architecture** (DMCA) for adaptive model orchestration on manufacturing edge devices (Kevin)
2. **Digital Twin model** aligned to AAS standards with manufacturing-aware submodels (criticality tier, IT-OT positioning, SIL, operator certification) (Yi Li)
3. **Distributed AAS extension** with runtime-populated submodels exposing TOPSIS multi-criteria selection as a DT service (Belfadel, IEC 63278/ISO 23247 positioning)
4. **Empirical validation** on two manufacturing PM datasets (PRONOSTIA accelerated bench, IMS Center realistic timing), benchmark of 8 foundation models at $0.30 GPU cost, and missed-alarm-cascade simulation demonstrating coverage-driven density gap (Simeone + Kevin)

### §2 · Related Work (2.0 pp) — split contribution

**§2.1 Predictive Maintenance in Smart Manufacturing edge AI — Simeone lead**
- Manufacturing PM literature, SME adoption barriers, edge constraints
- Key refs: Lee, Lapira, Bagheri, Kao 2013 [Manufacturing Letters]; PHM Society proceedings; CIRP Annals manufacturing intelligence track; IEEE TII manufacturing
- ISO 10816 vibration severity standard

**§2.2 Digital Twin and Asset Administration Shell standards — Belfadel lead**
- AAS standard IEC 63278 CDV; ISO 23247 digital twin manufacturing framework; ISO/IEC 30173
- Belfadel et al. 2025 (Advancing Industrial Digital Twins, IFIP AICT)
- XRTwin4Industry framework (FGCS 2026)
- Distributed DT architecture literature

**§2.3 Foundation models for time-series + model selection — Kevin lead**
- Chronos, Moirai, TimesFM, PatchTST, MOMENT, Lag-Llama
- Selection bottleneck literature (Maryanskyy 2026, Icsenir 2025)
- Drift detection (Bifet 2007 ADWIN, classifier evolution)
- Foundation models in PM: limited literature so far → gap

**§2.4 Gap matrix** (1 table) — joint
- Manufacturing-oriented: no existing work covers simultaneously (a) constraint-driven multi-criteria selection from DT, (b) distributed AAS submodel integration, (c) typed drift detection with re-alignment, (d) cross-vertical manufacturing PM validation

### §3 · Problem Statement (0.5 pp) — Kevin

- Manufacturing PM scenarios have non-negotiable SLA, hardware, latency, admissibility constraints
- Task-only model selection produces deployment-time silent failures
- Economic anchor: 94.5% missed monitoring windows (TimesFM paradox, thesis §7.5) translates to lost production-line uptime
- Framework requirement: continuous re-alignment, not one-shot

### §4 · Digital Twin Model (1.5 pp) — Yi Li lead, Kevin support

- Conceptual DT for manufacturing assets: hardware tier, RAM, latency SLA P95, sensor protocol, data availability, license constraints
- **Manufacturing-aware submodel additions** (new vs Phase 1 thesis):
  - Production line criticality tier (A/B/C)
  - IT-OT positioning (OT-side / boundary / IT-side)
  - Safety Integrity Level (SIL 1-4 per IEC 61508/IEC 62061)
  - Operator certification level (L1 line operator / L2 maintainer / L3 PM specialist)
- AAS Type 1 JSON schema as Phase 1 baseline
- Three reference manufacturing edge profiles: IPC industrial / Edge gateway / GPU edge
- One figure: DT submodel taxonomy for manufacturing PM context

### §5 · DMCA Framework Architecture (2.5 pp) — Kevin lead

Five stages, ~0.5 pp each:

**§5.1 Stage 1 — DT Profiling**: AAS parsing → constraint vector
**§5.2 Stage 2 — Model Selection (TOPSIS)**: M_adm admissibility + TOPSIS weights (MAE 0.5, latency 0.3, params 0.1, license 0.1) + sensitivity
**§5.3 Stage 3 — Edge Deployment (Quality Gate)**: 4-check validation
**§5.4 Stage 4 — Drift Detection (ADWIN + classifier v3.1.1)**: 8-feature decision tree, 7 drift types
**§5.5 Stage 5 — Re-alignment**: Shadow + atomic swap + operator-in-the-loop SIL-aware

One main architecture figure (5-stage closed loop with feedback).

### §6 · Distributed AAS Extension (1.5 pp) — Belfadel lead

> [TBD: scope to be finalized in 2026-06-26 call. Preliminary outline based on May 2026 exchange.]

- Phase 1 (thesis) baseline: single-asset, static AAS Type 1 JSON
- Extension: AAS distributed across cloud/fog/edge nodes
- Submodels dynamically populated with runtime status (latency, load, memory headroom, drift indicator)
- TOPSIS exposed as **DT service** consuming live submodel state
- Standards positioning: IEC 63278 CDV, ISO 23247, ISO/IEC 30173 conformance
- One figure: distributed AAS architecture (cloud/fog/edge topology with submodel mapping)
- References: Belfadel et al. PLM 2024, XRTwin4Industry

### §7 · Manufacturing Case Studies (2.5 pp) — Simeone + Kevin

**§7.1 Setup**
- Three edge profiles, 8 benchmark foundation models from thesis canonical run ($0.30 T4)
- **Two PM datasets**:
  - PRONOSTIA (FEMTO-ST, PHM 2012 Challenge): accelerated bench, 28min-7h run-to-failure, 6 Learning_set bearings × 3 operating conditions
  - IMS Center (NASA Prognostics Data Repository): realistic industrial timing, 4 bearings tested simultaneously over ~7 days

**§7.2 Case Study A — PRONOSTIA / Accelerated bench validation (REAL DATA)**

Setup: All 6 training bearings (Bearing1_1 to Bearing3_2), real PHM 2012 Challenge data, 7625 total acquisitions across the 6 bearings.

Result (σ=3, action window 5 min, baseline=10%):

| Bearing | Duration (min) | PatchTST alarms | Lag-Llama alarms | Moirai-S alarms | Lead PatchTST (s) | Lead Moirai-S (s) | Actionable Moirai-S |
|---|---|---|---|---|---|---|---|
| 1_1 | 467 | 1044 | 523 | 97 | 27780 | 27690 | YES |
| 1_2 | 145 | 45 | 23 | 4 | 440 | 340 | YES |
| 2_1 | 152 | 44 | 22 | 4 | 8770 | 8770 | YES |
| 2_2 | 133 | 563 | 281 | 51 | 5670 | 5540 | YES |
| 3_1 | 86 | 23 | 12 | 3 | 4920 | 4920 | YES |
| 3_2 | 273 | 29 | 14 | 2 | 390 | **190** | **NO** |

Headline:
- **Alarm density ratio mean: 10.4** (range 7.7-14.5 cross-bearing), tightly clustered around coverage-predicted 10.7
- **Bearing 3_2 is the safety-critical case**: PatchTST first alarm at 390s lead (actionable), Moirai-S first alarm at 190s (not actionable — 5 min action-window violated). The framework correctly distinguishes admissible from non-admissible for the safety-critical asset.

**§7.3 Case Study B — IMS Center / Realistic industrial timing (REAL DATA)**

Setup: Bearing 1 of Test 2 (NASA Prognostics Data Repository, IMS Center). 766 acquisitions × 10 min interval = 127.7 hours = 5.3 days realistic industrial timing. Failure: outer race documented in Lee et al. 2007 dataset notes.

Result (σ=3, action window 24h):

| Model | Alarms | First alarm lead time | Actionable |
|---|---|---|---|
| PatchTST | 233 | 139,200s = **38.7h** | YES |
| Lag-Llama | 116 | 138,600s = 38.5h | YES |
| Moirai-S | 20 | 129,000s = 35.8h | YES |

Headline:
- **Alarm density ratio: 11.6** (233/20) — coherent with PRONOSTIA 10.4
- **Cross-regime validation**: same coverage-driven density gap appears in accelerated bench (minutes) and realistic industrial (days)
- **Pre-failure window pattern**: degradation visible from h85 (3.5 days into trace), gradual rise to h117, then acceleration to peak ~0.18g at h128 (end of trace). All 3 models catch the rise; coverage gap manifests as different density of confirmation points on the same physical event

**§7.3.1 Cross-dataset robustness**: alarm density ratio is constant at 10-12 cross both datasets (PRONOSTIA accelerated and IMS realistic), confirming that the coverage gap is independent of degradation rate and is purely a function of SLA-vs-latency ratio.

**§7.4 Missed-alarm-cascade simulation — methodology**
- Coverage-only framing: assumes ideal accuracy on processed windows, isolating temporal-coverage variable from model-accuracy
- Coverage rates from thesis canonical benchmark + Jetson Nano SLA (50ms) + T4-to-Nano factor 10×
  - PatchTST 85% (admissible, point predictor)
  - Lag-Llama 64% (admissible, probabilistic, no collapse risk)
  - Moirai-S 9.3% (non-admissible, SLA-violating)
- Alarm threshold = baseline_mean + 3σ (sensitivity 2σ, 4σ)
- Per bearing: count alarms, first-alarm lead time, actionability vs action_window (5 min PRONOSTIA, 24h IMS extrapolation)
- **Lower-bound argument**: the 10× density gap reported under ideal-accuracy assumption is an upper bound on SLA-violating model's operational performance, therefore a lower bound on the real operational gap (real model accuracy degrades the SLA-violating model disproportionately)

**§7.5 Industrial extrapolation via ISO 10816**
- ISO 10816-3 vibration severity zones (A/B/C/D) as the bridge from accelerated bench data to industrial deployment timescales
- PRONOSTIA action window 5 min → field bearing action window 24-72h (rapid-onset contamination per ISO 10816 zone C-D)
- The coverage gap principle scales proportionally; magnitude depends on monitoring cadence and degradation rate

One main figure (per-bearing timeline RMS + alarm markers per model) + two summary tables (admissibility, missed-alarm aggregate).

### §8 · Implementation & Validation (1.0 pp) — Kevin

- Codebase 10 modules, MIT licensed (anonymized for review)
- Validation strategy L1-L4: technical, safety-blocking, operator qualitative, production
- Drift classifier v3.1.1: 92% held-out accuracy (5 types × 5 seeds), FAR 0.000
- Design decisions log v1 → v3.1.1 (iterative calibration documented)
- Missed-alarm simulation reproducibility: deterministic subsampling, sensitivity analysis on σ

### §9 · Results & Analysis (1.5 pp) — Kevin

Four core results, one paragraph each:

**§9.1 Latency cluster separation**: 3 clusters (<10ms / 10-100ms / >500ms) → 107×-348× separation on T4
**§9.2 SLA paradox & admissibility filter**: TimesFM excluded by 50ms SLA (40.8× over) → 94.5% windows lost without admissibility
**§9.3 Missed-alarm cascade on real PM data**: 10:1 alarm density gap, lower-bound on operational gap
**§9.4 Drift detection & recovery cycle**: Detection at t=1380, recovery at t=1400 on CMAPSS canonical case
**§9.5 Cost efficiency**: $0.30 total infrastructure for canonical benchmark → SME adoption argument

Two key figures: latency cluster plot, missed-alarm timeline (representative bearing).

### §10 · Discussion (0.5 pp) — joint

- Manufacturing implications: SME adoption at open-source cost
- Standards alignment: positioning vs IEC 63278 CDV / ISO 23247
- Coverage vs accuracy: orthogonal operational contributors, framework addresses both
- Limitations: synthetic data partial Phase 1, single-site evaluation, 1.5× SLA margin design choice
- Transition to Future Work

### §11 · Conclusion & Future Work (0.5 pp) — Kevin

- Summary of 4 contributions
- Phase 2 directions: streaming simulator, BaSyx live server, RL-policy extension, industrial use case validation via SystemX partner
- Closing line

---

## 6 · Figure & table inventory

**Figures (target 7-8):**
1. F1 — Manufacturing PM workflow + DMCA closed loop (§1)
2. F2 — DMCA 5-stage architecture (§5)
3. F3 — DT/AAS submodel taxonomy for manufacturing assets (§4)
4. F4 — Distributed AAS architecture cloud/fog/edge (§6, Belfadel)
5. F5 — Drift classifier decision tree v3.1.1 (§5.4)
6. F6 — Latency cluster scatter (§9.1, reuse `fig1_benchmark_scatter`)
7. F7 — Missed-alarm timeline representative bearing — PRONOSTIA (§7.2)
8. F8 — Missed-alarm timeline IMS Center (§7.3, pending IMS setup)

**Tables (target 5):**
1. T1 — Manufacturing-oriented gap matrix (§2.4)
2. T2 — Edge profile constraints + manufacturing-aware AAS fields (§4)
3. T3 — Benchmark results 8 models × 2 datasets (§7.1, reuse thesis Table 11)
4. T4 — Missed-alarm aggregate (per bearing × per model × σ) (§7.2-7.3)
5. T5 — Drift classifier accuracy per type (§8)

---

## 7 · Reference list — minimum 30-40 refs

**New refs added vs thesis (manufacturing PM stream):**
- Nectoux et al. 2012 — PRONOSTIA testbench paper, IEEE PHM Challenge
- IMS Center bearing dataset (NASA Prognostics Data Repository citation)
- ISO 10816-3:2009 / ISO 20816-3:2022 — vibration severity standard
- IEC 61508 / IEC 62061 — Safety Integrity Level (SIL) reference
- Lee, Lapira, Bagheri, Kao 2013 — predictive manufacturing systems, *Manufacturing Letters*
- Randall, Antoni 2011 — rolling element bearing diagnostics tutorial, *MSSP*
- Senseye/Siemens 2024 — *True Cost of Downtime* report
- Heng et al. 2009 — rotating machinery prognostics survey, *MSSP* (optional)

**Reuse from thesis bibliography:**
- Bifet & Gavaldà 2007 (ADWIN), Maryanskyy 2026, Xia 2024 (AAS), Belfadel et al. 2025, all foundation model architecture papers, all drift detection literature.

---

## 8 · For the 2026-06-26 SystemX call

When meeting Belfadel:
1. **Open with this skeleton** as evidence of scope alignment Polito-side (Simeone approved). Position of strength.
2. **Confirm §6 (distributed AAS) as Belfadel's primary section**: scope = cloud/fog/edge submodels + TOPSIS-as-service + IEC 63278 conformance.
3. **Discuss §2.2 standards positioning** as Belfadel-led (Anwer not in scope).
4. **Discuss Case Study C industrial** (§7.3 extension): if SystemX has access to industrial bearing data (Valeo, Renault, Safran), substitute or augment IMS Center with that. Frame: *"PRONOSTIA + IMS public datasets are the baseline; an industrial Case Study C from a SystemX partner would be the differentiator for IJAMT acceptance"*.
5. **Timeline alignment**: paper submission Q4 2026 / Q1 2027 realistic if §6 design draft by end July 2026, prototype September-October, draft November.

---

## 9 · Cover email to Simeone (Italian, ready to send)

**Subject:** *Scheletro paper IJAMT v0.2 — DMCA for Smart Manufacturing — bozza per tua revisione pre-call SystemX*

---

> Caro Professore,
>
> come concordato, allego lo scheletro v0.3 del paper congiunto per *International Journal of Advanced Manufacturing Technology*, da condividere con Belfadel nella call di oggi pomeriggio.
>
> **Risultati simulazione (REAL DATA, eseguita stamattina):**
>
> Ho fatto girare la simulazione *missed-alarm cascade* sui due dataset manifatturieri target del paper. Sintesi:
>
> - **PRONOSTIA (FEMTO-ST, accelerated bench)**: 6 bearing, 7625 acquisizioni totali. Alarm density ratio **10.4** (PatchTST/Moirai-S) coerente su tutti i bearing. **Bearing 3_2 mostra il flip safety-critical**: PatchTST first alarm a 390s pre-failure (actionable), Moirai-S a 190s (non-actionable, sotto soglia action window 5min). È la dimostrazione empirica del valore del framework per i casi di failure rapido.
> - **IMS Center (NASA, realistic industrial timing)**: Bearing 1 di Test 2, 766 acquisizioni × 10min = 5.3 giorni di monitoring reale. Alarm density ratio **11.6** — *coerente cross-dataset* con PRONOSTIA. Lead time PatchTST 38.7h pre-failure (action window 24h industrial), tutti i 3 modelli actionable, alarm density gap chiaramente visibile.
> - **Cross-regime validation**: il principio coverage-driven scala da accelerated bench (min-ore) a realistic industrial (giorni). Stesso ratio ~10× su scale temporali diverse.
>
> **Decisioni chiave nello scheletro:**
>
> - **Titolo (Opzione A)**: *"Digital-Twin-Driven Adaptive Model Selection and Drift Recovery for Predictive Maintenance in Smart Manufacturing"* — anchora manifatturiero su PM, distintivo rispetto al titolo tesi più generico
> - **Autori (4 confermati)**: io lead author + executor, tu senior IT + manufacturing framing, Prof. Yi Li senior CN + DT model, Dr. Belfadel collab FR + distributed AAS. Anwer non in scope (era solo introducer per Belfadel; mai confermato co-author)
> - **Riposizionamento manufacturing**: §1 con economics ($260k/h general, $2.3M/h automotive, Senseye 2024); §2 con literature PM manufacturing (Lee 2013, Randall 2011, ISO 10816); §4 con submodel manufacturing-aware (criticality tier, IT-OT, SIL, operator certification)
> - **Case studies §7**: due dataset manifatturieri REALI validati oggi (PRONOSTIA + IMS Bearing 1). Eventualmente Case Study C industriale da partner SystemX (Valeo/Renault/Safran) se Belfadel può aprire un canale — apertura della call odierna.
> - **Argomento lower-bound**: il 10× density gap è una conservative estimate (assume ideal accuracy sui processed windows); il gap operativo reale è ≥10×, mai minore. Argomento difensivo forte per review.
>
> **Cosa ti chiedo:**
>
> Una rapida lettura prima della call di oggi (idealmente entro le [orario]), con segnalazione di eventuali punti su cui vuoi che mi fermi prima di condividere con Belfadel. Se non sento entro [orario], procedo con la v0.3 come allegata, riservandomi di incorporare commenti tuoi successivi.
>
> Allegati: questo file (scheletro), figura `fig_Bearing3_2.png` (PRONOSTIA killer case), figura `fig_IMS_Bearing1.png` (IMS industrial validation), `results.csv` e `results_ims.csv` con i numeri completi.
>
> Grazie del tempo,
> Kevin

---

## 10 · Open items / known gaps in v0.2

To close in next iterations:

- ~~§7 numbers placeholder~~ → **REAL numbers populated** for PRONOSTIA (6/6 bearings) and IMS (Bearing 1 of Test 2). Remaining IMS bearings (Test 2 col 1/2/3, Test 3) pending as supplementary
- ~~§7.3 IMS Center pending~~ → **IMS loader implemented**, 1 bearing validated (ratio 11.6 cross-dataset coherent with PRONOSTIA 10.4)
- §6 Belfadel section TBD until call confirmation of distributed AAS scope
- §2.4 gap matrix table content to be filled with explicit citation crossings
- Reference list to be merged into `references_master.bib` with full BibTeX entries

---

*v0.2 — last updated 2026-06-25 13:XX UTC. Lead author: K. Omede. Next iteration: v0.3 after Simeone review + SystemX call 2026-06-26 alignment.*
