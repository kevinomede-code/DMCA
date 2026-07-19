# Pipeline di Remediation — Tesi DMCA · v3

> **Stato audit: 19 riferimenti verificati su 116. PARTE A chiusa tranne A3 e A13.**
### "Dynamic Model-Context Alignment for Smart Manufacturing" — K. Omede
**Difesa: settembre 2026 · PoliTo · Documento di lavoro, non consegnabile**

> **v2 — cosa è cambiato rispetto a v1:** l'audit citazioni è **CHIUSO** (18 riferimenti verificati). Le vecchie Fase 0 e Fase 1 (decisione + audit) sono completate e rimosse. Aggiunti: tutti gli esiti Tier 2, gli 8 autori placeholder recuperati, 2 voci sistemiche nuove, 3 aggiunte candidate verificate.

---

## Come si legge

Ogni intervento = **un prompt isolato per Claude Code sul sorgente LaTeX**. Questo `.md` **non va dato a Claude Code**: è la tua mappa. Tu prendi una voce, scrivi il prompt col template (§F.2), Claude Code tocca i `.tex`/`.bib`.

**Categorie:** **(a)** risolvibile pre-difesa · **(b)** mitigabile a voce · **(c)** limite strutturale da dichiarare.

**Marcatori:** 🔧 semplifica/rimuovi (default) · ➕ aggiungi (solo con DOI + parola da verificare) · ✋ azione tua · ⚠️ tocca più punti (rischio residuo incoerente) · 🧮 richiede rieseguire codice.

**Principio guida:** *prima semplificare, poi — solo se serve — aggiungere. Mai aggiustare la fonte per schivare un'obiezione: o si ridimensiona l'inferenza propria, o si riporta la fonte fedelmente e si risponde nel merito.*

**Il pattern diagnostico emerso dall'audit — è anche la tua difesa orale:**
> Ogni citazione con un **numero puntuale** o un **superlativo** attribuito alla fonte è risultata inventata o distorta. Ogni citazione basata su **quote verificabile** o **fatto strutturale** ha retto.
> *In difesa:* i fatti strutturali del lavoro sono solidi; le cifre prese dalla letteratura altrui erano il punto debole, e sono state sistemate prima della difesa.

---

# PARTE A — Azioni a carico tuo (bloccanti)

Nessuna richiede LaTeX. Richiedono i tuoi PDF o una tua decisione. **Da chiudere prima di aprire il sorgente**, perché alcune cambiano il testo da scrivere.

| # | Azione | Cosa cercare |
|---|---|---|
| ~~**A1**~~ ✅ | ~~[53] Jin §7.3~~ **CHIUSA** — è la **v3, 8 giugno 2026** (non la v2). Quote **verbatim** in **§7.3** (p. 23), sezione corretta: *"their integration with large temporal models remains under-explored"* (9 parole). ⚠️ Il soggetto è **l'integrazione con i large temporal models**, NON il drift adaptation (che il paper dice già studiato) → vedi **B8** | — |
| ~~**A2**~~ ✅ | ~~[53] Jin Tab. 3~~ **CHIUSA** — **"30+" è GIUSTO**: 32 dataset (traffic 5, healthcare 4, weather 4, finance 4, video 4, event pred. 5, others 6). **L'unico numero puntuale che regge in tutto l'audit.** ⚠️ Ma **non scrivere "zero industrial"**: ci sono ETT e Alibaba Cluster Trace → usa **"no manufacturing or prognostics benchmark"** | — |
| **A3** ⏳ | **[55] Benmeziane catena** — apri il PDF ICSE-NIER [1] | che la sua ref **[28]** sia Benmeziane et al. + che la sua eq.1 sia ispirata a MnasNet. **Consigliato: togliere il dettaglio e citare Benmeziane diretto.** ← **unica azione ✋ rimasta oltre A13** |
| ~~**A4**~~ ✅ | ~~[71] Abbasi tre tipi~~ **CHIUSA — sono QUATTRO, e nessun nome coincide.** Reali: **Data Driven Drift** (§3.1, Def. 3.2 — sotto-tipi Label/Feature/Concept + **Structural**), **Technical Conceptual Drift** (§3.2, Def. 3.3, Δη), **Knowledge Conceptual Drift** (§3.3, Def. 3.4, Δη), **Interpretation Drift** (§3.4, Def. 3.5 — orizzontale Δγ + verticale Δη) → vedi **B12** | — |
| ~~**A5**~~ ✅ | ~~[72] Abbasi numeri~~ **CHIUSA — [72] NON SERVE.** **[71] §5 contiene già la valutazione piattaforme**: tre tool considerati (AzureDT, Fiware NGSI-LD, AWS IoT TwinMaker), **due valutati**. Hai già il PDF. Il "four frameworks" era comunque sbagliato → vedi **B12** | — |
| ~~**A6**~~ ✅ | ~~[94] autori~~ **CHIUSA** — **Shanhe Lou, Mengchu Zhou, Runjia Tan, Chen Lv**. ICHMS 2025, pp. 223–228, DOI `10.1109/ICHMS65439.2025.11154278` | — |
| ~~**A7**~~ ✅ | ~~[97] forma nome~~ **CHIUSA** — **Lucas Giusti Tavares** (+ Janio Lima, Matheus Melo, Chao Chen, Jonathan M. Garibaldi, …) | — |
| ~~**A8**~~ ✅ | ~~[3] Maryanskyy status~~ **CHIUSA — NON è tuo.** Preprint di terzi: **Artem Maryanskyy** (Uber), autore unico, arXiv:2603.20324v1, 20 mar 2026. Autocitazione **morta**. ⚠️ **Ma apre B16: misattribuzione grave** | — |
| ~~**A9**~~ ✅ | ~~FAR = 0.000~~ **CHIUSA** — dalle tue simulazioni, confermato. **I "sette tipi" sono spiegati dai DD docs**: il tree emette **7 label** (ABRUPT, GRADUAL, INCREMENTAL, VARIANCE_SHIFT, OUTLIER_DRIVEN, DISTRIBUTION_SHIFT, UNCLASSIFIED), gli scenari sono **5**. Nessuna contraddizione. ⚠️ **La tesi è già a 92% held-out v3.1.1** (l'80% era mio errore: è la tappa v3). **Resta il refuso riga 1480** → **C5** | — |
| ~~**A10**~~ ✅ | ~~[102] pagine~~ **CHIUSA** — non controllare: usa **arXiv `2508.00399`** e togli le pagine | — |
| **A13** 🆕 | 🧮 **Re-run simulazione a SLA=100ms** | I lead time (410s / 280s / −20s) sono misurati a s=2 e s=11. Con SLA=100ms → **s=1 e s=6**: vanno rieseguiti. Anche Eq.11: ∆tmax = (2·6−1)×10 = **110 s**, che **non contiene più** il gap empirico di 150 s → verificare |

---

# PARTE B — Correzioni citazioni (audit chiuso)

## B1 · [40] Banbury — DUE punti ⚠️ · (a)
**Problema:** entrambi i claim sono errati.
- **riga ~866:** "up to 10,000× latency variation for the same model" → **fabbricato**. Il numero viene da Banbury 2020 (arXiv 2003.04821) ed è *power budget* (4 ordini di grandezza), non latenza.
- **riga ~1152:** "sub-1MB NN saturates memory/power of MCU-class devices" → **distorto** (MLPerf Tiny dimostra il contrario: modelli 96–325KB che girano su MCU) **e misapplicato** (parla di MCU sub-MB; le tue board sono SBC Linux 4GB).

**Azione:**
- riga ~866 → riscrivere: MLPerf Inference *"precludes MCUs and resource-constrained platforms"*; l'eterogeneità hardware (µW–W) motiva benchmark dedicati → misura per-device necessaria → DMCA usa proiezioni conservative in Fase 1 + on-device in Fase 2. **Bonus:** sparendo "useless" cade l'auto-accusa contro la tua proiezione T4→Jetson.
- riga ~1152 → **sganciare da Banbury**. Il tuo argomento ("Jetson/RPi = inferenza, retraining infattibile") sta in piedi da solo: memoria backprop ≈3–4× inferenza, no GPU adeguata su RPi4, ore di CPU-time.

**DOI:** `10.48550/arXiv.2106.07597`

## B2 · [67] Lu — fabbricazione, pezza portante GAP 1 · (a)
**Problema:** "Section VII explicitly flags 'multi-model catalog drift response' as an open research direction" → **sezione e frase inesistenti**. Section VII = "Concept Drift in Other Research Areas"; le future directions sono in Section 8 e sono altre quattro.

**Azione:** 🔧 sostituire con l'inferenza onesta sulla loro tassonomia (**Section 5**): retraining / ensemble / adjustment sono **tutte interne al modello incumbente**; la selezione da catalogo esterno **non compare come classe** → "DMCA introduce questa quarta classe". Stessa mossa già fatta correttamente per Gama et al. nella frase precedente.
**DOI:** `10.1109/TKDE.2018.2876857` · **verifica manuale:** che Section 5 elenchi le tre classi.

## B3 · [68] Shankar — REGGE, 1 correzione · (a)
**Problema:** le due quote (§4.2, §4.5.1) sono **verificate verbatim** ✓. Solo il terzo claim sbaglia oggetto: §5.1.2 inquadra il **"Goldilocks alert problem"** (quando allertare), non il "drift-triggered model replacement".

**Azione:** 🔧 correggere il terzo riferimento. Riformulare l'inferenza su **§4.5.2** (fallback models): replacement osservato = versioni più semplici/storiche/retrainate, nessuna selezione constraint-aware → inferenza tua legittima.

## B4 · [84] datasheet — stima tua spacciata per fonte · (a)
**Problema:** "manufacturer datasheets suggest a conversion factor of 5–20×" → una scheda prodotto non pubblica fattori di conversione (la tua nota bib ammette "used to **estimate**"). Rischio: FLOPS picco T4/Nano ≈34× > range dichiarato. Aggravante: §2.12 la cita anche per "Jetson/RPi de-facto hosts for SMEs" — claim di mercato che NVIDIA non fa (men che meno sul RPi).

**Azione:** 🔧 riscrivere come **assunzione dichiarata con derivazione fisica**:
> *"In absence of published cross-device profiling for these model families, we assume a T4→Jetson Nano slowdown of 5–20× (midpoint ×10). The range is motivated by the memory-bandwidth ratio between the two devices (≈320 vs 25.6 GB/s ≈ 12.5×), the first-order predictor for batch-1 memory-bound inference; robustness to k is analysed in [sensitivity]."*

**Verifica manuale:** banda T4 = **320 GB/s**, Jetson Nano = **25.6 GB/s** sulle schede NVIDIA (conferma i due numeri prima di scriverli). Il claim SME va sganciato o supportato altrove.

## B5 · [65/93] Sculley — 3 problemi + duplicato ⚠️ · (a)
**Problemi:**
- (a) "10% threshold consistent with the operational guidance of Sculley" (§3.17) → **fabbricato**. **Ironia pericolosa:** il paper ha una sezione *"Fixed Thresholds in Dynamic Systems"* che tratta le soglie fisse come **debito da evitare** → citazione ribaltabile contro di te.
- (b) "DMCA avoids CACE by design" → **fianco scoperto**: lo swap di modello è il cambiamento CACE-**massimale** a valle (undeclared consumers).
- (c) "distribution shift as **the principal** source" → sovradichiarato.
- (d) **Duplicato** in 3 file bib → doppia numerazione [65]/[93].

**Azione:**
- 🔧 (a) il 10% è **scelta di design tua**: soglia conservativa oltre la banda di rumore del surrogato (±5%), configurabile via AAS DeploymentPolicy, calibrazione empirica = Fase 2. *"Fixed Thresholds" diventa alleato*: motiva perché la soglia è dichiarata configurabile, non hardcoded.
- 🔧 (b) versione difendibile: DMCA evita il **burden del retraining** (nessuna pipeline di training da rivalidare, feature ingestion invariata); impatto a valle **mitigato — non eliminato** — da quality gate / shadow / grace / rollback.
- 🔧 (c) una parola: **"among the sources"**.
- 🔧 (d) deduplicare → vedi C2.

**Quote da tenere (verificata):** *"Changing Anything Changes Everything"* ✓ · **DOI:** `10.5555/2969442.2969519`

## B6 · [54] Liang — fabbricazione quantitativa, TRE punti ⚠️ · (a)
**Problema:** "15–40% zero-shot degradation / recover within 5% / one-tenth cost" → **nessuno di questi numeri esiste**. Il survey (KDD'24) è puramente metodologico, **zero esperimenti**. "PatchTST-small" non esiste. Presente in **3 punti**: prosa (~941–943), **riga tabella con ✓** (~967), **nota bib** (~4599) → l'errore nasce nella schedatura.

**Azione:**
- 🔧 sostituire con **evidenza tua**: *"While methodological surveys [54] map the TSFM landscape, quantitative evidence of the zero-shot deployment gap on industrial sensor data remains scarce — a gap our benchmark addresses directly (Section 5)."* → da citazione falsa a **claim di contributo**.
- 🔧 riga tabella (~967): da "15–40% degradation ✓" → *"Survey metodologico; flagga distribution shift come direzione aperta — ∼"*.
- 🔧 **nota bib** (~4599): correggerla, o l'errore risorge in paper futuri.

**DOI:** `10.48550/arXiv.2403.14735` · **verifica manuale:** che l'appendice "future directions" citi **"distribution shift"** (mattone autentico per il gap).

## B7 · [34] He — numero fabbricato + metrica sbagliata + doppio uso ⚠️ · (a)
**Problemi:**
- "RSR drops from 0.57 to 0.11" → **inventato**.
- "RSR = appropriate switch rate" → **sbagliato**: RSR = **Relative positive Self-Reliance**. Confuso con *switching fraction* (0.522).
- nesso causale "fluent but poorly calibrated" → il meccanismo reale è **illusion of explanatory depth**.
- **doppio uso** (riga ~801): citato per "XAI in manufacturing operator contexts" — ma è uno studio su **loan approval con laypeople** (N≈306), zero manifatturiero.
- **bib:** DOI **placeholder inventato** (`10.48550/arXiv.2502.12345`); autore discordante (master "Aishwarya" vs gap3 "Aarts"); 3 chiavi diverse.

**Azione:**
- 🔧 togliere 0.57→0.11; ancorare al finding reale: *"He et al. [34] show that conversational and LLM-powered XAI can amplify over-reliance through an illusion of explanatory depth, even while improving subjective understanding and trust. This constrains the DMCA copilot: explanation confidence must track the quality-gate outcome, not the fluency of the generated text."*
- 🔧 numeri reali se ti servono: switching fraction **0.522**; accuracy umana **64.5%** < **70%** AI.
- 🔧 riga ~801: serve **altra fonte**, o riformulare l'assenza come gap.
- 🔧 **bib corretto:** autori **Gaole He, Nilay Aishwarya, Ujwal Gadiraju** · DOI **`10.1145/3708359.3712133`** (arXiv 2501.17546) · unificare le 3 chiavi.

**Verifica manuale:** che nel paper la metrica sia scritta **"Relative positive Self-Reliance"**.

## B8 · [53] Jin — quote OK, soggetto sbagliato + due prove nuove ✅ · (a)
**Verificato sul primario: arXiv 2310.10196 v3, 8 giugno 2026** (NON la v2 di ott. 2023).

**1. Il quote REGGE** — §7.3 "Continuous Learning and Adaptation" (p. 23), verbatim:
> *"While online learning, concept drift adaptation, and evolving-pattern modeling **have been studied** in conventional machine learning, **their integration with large temporal models remains under-explored**."*

⚠️ **Ma il soggetto è un altro.** Il drift adaptation il paper lo dà per **già studiato**; under-explored è **la sua integrazione con i large temporal models**. Stesso errore di Shankar §5.1.2: paper giusto, oggetto sbagliato. **La versione vera è migliore** — è letteralmente il tuo gap.

**2. "30+" è GIUSTO** ✅ — Tabella 3 (p. 21) ha **32 dataset**. ⚠️ **Non scrivere "zero industrial"**: ci sono **ETT** (Electricity Transformer Temperature) e **Alibaba Cluster Trace** (workload cloud) — industriale-adiacenti, contestabili in un secondo.

**3. ➕ PROVA NUOVA, più forte — Figura 3 (p. 10):** la tassonomia domain-specific copre **Transportation, Finance, Healthcare** per gli LLM4TS e **Finance, Healthcare** per i PFM4TS. **Il manufacturing non compare in nessuno dei due rami.** Non è un'assenza tra i dataset: è un'assenza nella tassonomia stessa. Si verifica guardando una figura.

**4. ➕ PROVA NUOVA — §7.3 stessa:** chiude indicando i PFM domain-adaptive per **"industrial applications"** come *direzione promettente*. **Il paper classifica il tuo territorio come direzione futura, non terreno coperto.**

**5. 🔧 "review more than 150 works"** (riga 934) → **non verificabile**: la Tabella 2 elenca **87 metodi**, la bibliografia ne ha 296. Nessuno dei due fa 150. Togliere il numero o sostituirlo con un conteggio tuo a base dichiarata.

**Azione — riscrittura righe 933–936:**
> *"Jin et al. [53] survey large models for time series and spatio-temporal data. Their resource compilation (Table 3) lists 32 benchmark datasets spanning traffic, healthcare, weather, finance, video and event prediction; none is a manufacturing or prognostics benchmark — neither CMAPSS nor PRONOSTIA nor any analogous run-to-failure dataset appears. Their domain-specific taxonomy (Figure 3) covers transportation, finance and healthcare; manufacturing appears in neither the LLM- nor the PFM-based branch. Their outlook (§7.3) notes that while concept drift adaptation is established in conventional machine learning, 'their integration with large temporal models remains under-explored', and identifies domain-adaptive foundation models for industrial applications as a promising direction."*

**Azione — Gap Matrix riga 966:** *"Jin et al. **2023**"* → **2026**; *"zero industrial datasets"* → *"no manufacturing/prognostics benchmark among 32 datasets"*; *"drift adaptation under-explored"* → *"integration of drift adaptation with large temporal models under-explored"*.

➕ **Bonus gratis:** la lista **PFM4TS general-purpose** della survey (PatchTST, Lag-llama, MOIRAI, TimesFM, MOMENT, Chronos, TimeMixer++) **è il tuo catalogo**. Ancora la tua selezione alla tassonomia di riferimento del campo: *"The catalog benchmarked here corresponds to the general-purpose PFM4TS branch of Jin et al.'s taxonomy [53]."*

**Bib → vedi B17** (venue, DOI, anno, autori: quattro errori separati).

## B9 · [59] Menghani — numeri decorativi · (a)
**Problema:** "INT8 delivers 2–4× **latency** improvement with **<1%** accuracy degradation on models above **10M** parameters".
- "2–4× latency" → **confonde size con latency** (il survey dà 2–8× **size**; 4× **size** per INT8; la latenza INT8 è spesso marginale e hardware-dipendente).
- "<1% accuracy" → non è claim generale del survey.
- ">10M parameters" → **inventato**.

**Azione:** 🔧 *"INT8 quantisation is the standard post-training compression step for edge deployment, reducing model size ~4× and, with activation quantisation, inference latency [59]. The realised latency gain is hardware-dependent — integer-operator support on the target governs the actual speedup — which is why DMCA measures post-quantisation P95 latency on the target class rather than assuming a fixed factor."*
**Più forte in difesa:** trasforma la dipendenza HW in **motivazione** del measure-don't-assume.
**DOI:** `10.1145/3578938` · **verifica manuale:** che "2–8×" / "4×" siano riferiti a *model size*.
➕ *opzionale:* Krishnamoorthi 2018 (citato da Menghani) ha misure INT8 specifiche — verificare prima di aggiungere.

## B10 · [55] Benmeziane — REGGE, ritocchi · (a)
**Problema:** solo etichette. I quattro assi reali: **search space, search strategy, acceleration technique, hardware cost estimation** (non "hardware performance estimation, target platform"). "dynamically changing hardware targets" è parafrasi **legittima** di §XI-C (Transferability over HW Platforms) — **ma se è tra virgolette vanno tolte**.

**Azione:** 🔧 correggere le etichette; de-virgolettare e citare §XI-C. ✋A3 per la catena [28].
**Nota di framing (tienila):** che Benmeziane inquadri il *re-run per ogni nuovo hardware* come problema aperto è un ottimo aggancio — tu non risolvi HW-NAS, lo **eviti** selezionando da catalogo.
**DOI:** `10.48550/arXiv.2101.09336`

## B11 · [88, 89] — costo asimmetrico ⚠️ · (a) — **fix ad alto rendimento**
**Problema:** *"a missed alarm is typically an order of magnitude more costly than a false alarm [88, 89]"* → **nessuna delle due fonti lo dice**. [88] PRONOSTIA è un paper di **testbench** (nessuna analisi economica); [89] PHMForge dice solo che le decisioni errate hanno "significant safety and financial consequences" — nessun rapporto. **Contraddizione interna:** la tua nota bib per [89] dice *"Confirms gap: no missing alarm rate metric"* — citi per il costo del missed alarm un paper che (per tua stessa ammissione) non ha la metrica.

**Azione:** 🔧 **l'asimmetria è reale ed è dentro PRONOSTIA** — la scoring function della PHM 2012 Challenge:

$$A_i = \begin{cases} e^{-\ln(0.5)\cdot(Er_i/5)} & Er_i \leq 0 \text{ (late)} \\ e^{+\ln(0.5)\cdot(Er_i/20)} & Er_i > 0 \text{ (early)} \end{cases}$$

Il punteggio **si dimezza ogni 5% di errore tardivo, ma ogni 20% di errore anticipato → asimmetria 4× nell'emivita della penalità** (a ±20%: 0.0625 vs 0.5 = 8× di divario). Riscrittura:
> *"This asymmetry is institutionalised in PHM evaluation practice: the IEEE PHM 2012 Challenge scoring function [88] halves the score for every 5% of late RUL error but only every 20% of early error — a 4× steeper penalty for late predictions, reflecting the operational consensus that a missed alarm is more consequential than a premature one. Standard ML benchmarks instead report symmetric losses (MAE, RMSE)."*

**Più forte dell'originale:** preciso, verificabile, ed è il ponte esatto verso la tua metrica di coverage.
**Nota utile:** i tuoi due dataset hanno convenzioni **diverse** — PRONOSTIA 5/20 (forte); C-MAPSS `e^(−d/13)` early / `e^(d/10)` late (mite, ≈1.75× a 20 cicli). Entrambe dicono "tardivo = peggio", **nessuna** dice "ordine di grandezza in costo".
**Il numero economico in €** resta la voce **D10** (fonte diversa).
**Bib [89] corretto:** **Ayan Das, Dhaval Patel** · arXiv **2604.01532**

## B12 · [71] Abbasi — tassonomia sbagliata + [72] eliminato + **regalo grosso** ✅ · (a)
**Verificato sul PDF integrale (MODELS Companion '24).**

**1. ✗ La tassonomia è tutta sbagliata — sono QUATTRO varianti, e nessun nome coincide:**

| § | Variante reale | Contenuto |
|---|---|---|
| 3.1 | **Data Driven Drift** (Def. 3.2) | sotto-tipi: *Label/Feature/Concept Drift* + ***Structural Drift*** |
| 3.2 | **Technical Conceptual Drift** (Def. 3.3) | modelli/metamodelli divergono (Δη) |
| 3.3 | **Knowledge Conceptual Drift** (Def. 3.4) | ontologie obsolete (Δη) |
| 3.4 | **Interpretation Drift** (Def. 3.5) | orizzontale (Δγ) + verticale (Δη) |

La tesi dice *"model evolution / schema / concept drift"*: **nessuno dei tre nomi esiste**, mancano il drift ontologico **e** l'interpretation drift, e "schema drift" è in realtà **Structural Drift**, sotto-tipo del primo.

**Riscrittura:**
> *"Abbasi et al. [71] propose a formal classification of semantic drift across the modelling layers of a digital twin: **data-driven drift** (feature, label, concept and structural drift at the data layer), **technical conceptual drift** (models and metamodels diverging from the evolving system), **knowledge conceptual drift** (ontologies becoming outdated), and **interpretation drift**. They formalise vertical drift (Δη) propagating across layers and horizontal drift (Δγ) within a layer."*

**2. 🔧 Togliere "the first"** — gli autori non lo rivendicano (*"we propose a classification and formalization"*). **Sostituto migliore, verbatim-adiacente:** il paper dice che i contributi esistenti in ML, software architecture e semantic web **non affrontano come identificare, caratterizzare e mappare i cambiamenti in modelli eterogenei**. Usa quello.

**3. ➕ IL REGALO — le quattro fasi.** Abbasi elenca **quattro fasi** per gestire il semantic drift — (i) identification, (ii) characterisation, (iii) **maintenance**, (iv) **propagation** — e dichiara di affrontare **solo le prime due**.
**La fase maintenance È DMCA.** Non è argomento per assenza: è **scope dichiarato dagli autori**.
> *"Abbasi et al. [71] identify four phases in managing semantic drift — identification, characterisation, maintenance and propagation — and explicitly scope their contribution to the first two. DMCA addresses the maintenance phase: given a detected and characterised drift, which model should replace the incumbent under deployment constraints."*

**Questo sostituisce sia il "first formal taxonomy" sia il gap statement di D16.** È più forte di entrambi, e la fonte ce l'hai in mano.

**4. ✅ [72] ELIMINATO — non serve.** **[71] §5 contiene già la valutazione piattaforme**: tre tool considerati (AzureDT, Fiware NGSI-LD, AWS IoT TwinMaker), **due valutati**.
- **AzureDT**: il drift da aggiunta di un componente **non è propagabile al model graph/metamodel** per i limiti di `get_model()`.
- **Fiware NGSI-LD**: **non separa i dati dal metamodello** → preclude structural, technical e knowledge conceptual drift.
- **AWS IoT TwinMaker**: **non valutato**.
> *"Abbasi et al. [71, §5] evaluate AzureDT and FIWARE NGSI-LD for semantic drift detection: AzureDT cannot propagate component-addition drift to the metamodel level due to API limitations, while FIWARE NGSI-LD does not separate data from metamodel, precluding structural, technical and knowledge conceptual drift."*

**5. 🔧 Autori [71]: quattro** — Abbasi, **Brimont**, Pruski, **Sottet**. Tu ne citi due.

**DOI:** [71] `10.1145/3652620.3688256` · [72] **da rimuovere dal bib**
**Nota:** i quattro tipi canonici (sudden, gradual, incremental, reoccurring) Abbasi li attribuisce al suo rif. **[36] = Lu et al. 2018 = il tuo [67]** → ancora per **C5/tassonomia**, fonte che hai già.

## B13 · [92] FactoryNet — autore fabbricato ⚠️ · (a)
**Problemi:**
- ✗✗ **AUTORE INVENTATO**: citi *"Hao Zhang et al."*; i reali sono **Karim Othman, Jonas Petersen, Matei Ignuta-Ciuncanu, Camilla Mazzoleni, Federico Martelli, Alessandro Lombardi, Riccardo Maggioni, Philipp Petersen**. **L'arXiv ID nel tuo bib è corretto** → chi ha compilato aveva l'identificativo giusto e ha inventato il nome. Pattern di allucinazione puro.
- ✗ **risultati sovradichiarati**: dici *"validates zero-shot cross-domain transfer"*; il paper dice **"fair cross-embodiment transfer on the evaluated source-target pair"** (una sola coppia). L'altro risultato è **efficienza parametrica** (24 segnali, MLP, 83.2% AUROC su voraus-AD vs 130 canali).
- ✗ **dominio impreciso**: dici "production cells"; il corpus è **manipolazione robotica + machining** (UR3, KUKA KR10, voraus-AD, AURSAD, UMich CNC, sintetico Isaac Sim).
- ⚠️ **duplicato** in `gap4_industrial_validation.bib` + `manufacturing_refs.bib`.

**Cosa REGGE:** numeri **tutti esatti** (51M, 23k, 6 embodiments, S-E-F-C) ✓ · il **"first" è degli autori** ("We introduce the first universal pretraining corpus") ✓ — allinea solo la parola (loro "universal", tu "large-scale").

**Azione:** 🔧 correggere autori; ridimensionare al vero:
> *"The recent FactoryNet corpus [92] — introduced by its authors as the first universal pretraining corpus for industrial time-series (51M datapoints, 23k task executions, six embodiments) — reports fair cross-embodiment transfer on a single evaluated source-target pair, and competitive anomaly detection from 24 schema-aligned signals. Its scope is robotic manipulation and machining; prognostics corpora such as CMAPSS and PRONOSTIA remain outside industrial pretraining efforts."*

**L'ultima frase RAFFORZA il tuo gap.** **DOI:** `10.48550/arXiv.2605.09081`

## B14 · [52] Zeng — bib ✓, due errori tecnici · (a)
**Il bib è CORRETTO** ✓ (autori, AAAI 2023, vol. 37(9), pp. 11121–11128, DOI `10.1609/aaai.v37i9.26317`).
**Problemi:**
- **"five of six tested benchmarks"** → **entrambi i numeri sbagliati**: sono **nove** dataset e l'abstract dice **"in all cases"**. *È il primo errore che ti **sfavorisce**.* (Tensione interna al paper: il corpo dice "in most cases" — formulazione sicura: *"nine benchmarks, outperforming in most cases (the abstract claims all)"*.)
- **"two-layer linear decomposition"** → **sbagliato**: sono **due rami paralleli da UN layer** ("two one-layer linear networks"). Tutta la letteratura lo chiama *one-layer linear model*.
- **"the strongest counter-argument"** → tua valutazione, difendibile ma **contestata**: HuggingFace ha replicato ("Yes, Transformers are Effective...", Autoformer batte DLinear a parità di size) e **PatchTST supera DLinear** sulla maggior parte dei dataset.

**Azione:** 🔧 correggere i due errori. Per il terzo, la formulazione che ti protegge — **e ti serve, dato che PatchTST è nel tuo catalogo**:
> *"Zeng et al. [52] opened a still-unresolved debate on whether Transformer complexity is justified for time series. This contested picture is precisely why DMCA ranks on measured performance rather than architectural priors."*

## B15 · [51] TimeMixer — "first 2024" falso · (a)
**Problema:** *"the first 2024 architecture to treat inference efficiency as a first-class design goal"*. (a) Il qualificatore **"first 2024"** è la stessa tautologia difensiva di *"for HuggingFace models"* in §1.1 — restringere l'anno per salvare il primato è una mossa leggibile. (b) **È falso**: **SparseTSF** (2024) e **FITS** sono esplicitamente progettati per l'efficienza.

**Azione:** 🔧 *"TimeMixer [51] achieves competitive accuracy at significantly lower FLOPs, part of a 2024 wave treating inference efficiency as a first-class design goal (alongside FITS, SparseTSF)."*

---

## B16 · [3] Maryanskyy — **MISATTRIBUZIONE GRAVE, 5 punti** ⚠️⚠️ · (a) — **PRIORITÀ MASSIMA**
**Il paper è reale e di terzi**: Artem Maryanskyy (Uber), autore **unico**, arXiv:2603.20324v1, 20 mar 2026. *"When Agents Disagree: The Selection Bottleneck in Multi-Agent LLM Pipelines"*.

**Il problema: il paper dice il CONTRARIO di ciò che gli attribuisci.**
Il suo "selection bottleneck" è l'**aggregazione di output** prodotti da un team di LLM (judge-based selection vs sintesi MoA vs majority vote), su compiti di coding, scrittura, etica, matematica. **Zero industriale, zero digital twin, zero deployment, zero Industry 4.0.**

**La frase che chiude il caso** — nella sua related work §2.3, Maryanskyy **distingue esplicitamente** il proprio lavoro dalla selezione di modelli: *loro selezionano quale modello chiamare, lui seleziona quale output tenere.*

**I 5 punti da correggere:**
| Riga | Cosa dice ora | Problema |
|---|---|---|
| **452** | *"agentic architectures... address it at the protocol level"* | "protocol level" non c'è |
| **458–460** | *"the agent choosing among candidate **models** lacks a structured description of the **deployment environment**, forcing it to rely on **static configuration files**"* | **niente di tutto questo è nel paper** |
| **1314** (Gap Matrix) | *"Selection bottleneck formalisation in MAS for **Industry 4.0**"* | **non c'è Industry 4.0** |
| **1441** | *"As [3] documents, model selection has become a bottleneck in multi-agent AI pipelines"* | non è model selection |
| **4152** (**C1**) | *"directly addressing the selection bottleneck identified by [3]"* | **il tuo contributo principale agganciato a un paper che dichiara di non occuparsene** |

**Azione: 🔧 rimuovere [3] dalla fondazione del gap (§1.1, §1.2, Gap Matrix, C1).** Il gap regge — meglio — su fonti già verificate:

| Fonte | Cosa dà | Stato |
|---|---|---|
| **Lu [67]** §5 | retraining/ensemble/adjustment **tutte interne al modello incumbente** → selezione da catalogo assente come classe | ✅ |
| **Shankar [68]** §4.5.2 | replacement limitato a versioni semplici/storiche/riaddestrate, **nessuna selezione constraint-aware** | ✅ quote verbatim |
| **Abbasi [71]** | fase **maintenance fuori dal loro scope dichiarato** | ✅ |
| **Il tuo benchmark** | spread 348:1 | 📏 misurato |

**Dove resta (§2, analogia dichiarata):**
> *"In the adjacent setting of multi-agent LLM output aggregation, Maryanskyy [3] finds that selector quality dominates generator diversity (judge-based selection WR 0.810 vs MoA synthesis 0.179); an analogous result for model selection under deployment constraints has not been established."*

**Bib:** autore **unico** Artem Maryanskyy · arXiv:2603.20324 · DOI `10.48550/arXiv.2603.20324` · **dichiarare "preprint"** (non peer-reviewed).

---

## B17 · [53] Jin — **entry bib: 4 errori separati** ⚠️ · (a)
```bibtex
journal = {IEEE Transactions on Knowledge and Data Engineering}   ← VENUE INVENTATA
year    = {2024}                                                   ← è 2026 (v3)
doi     = {10.48550/arXiv.2308.10278}                              ← DOI DI UN ALTRO PAPER
author  = {Jin, Wen, Liang, ...}                                   ← manca Yaxuan Kong (2° autore)
```
1. **✗ Venue fabbricata**: il PDF dice *"Manuscript submitted to **ACM**"*, copyright ACM 2026, ACM Reference Format con DOI **segnaposto** `10.1145/nnnnnnn.nnnnnnn` → **non pubblicato**, **non è su IEEE TKDE**.
2. **✗✗ DOI sbagliato — il peggiore**: l'arXiv ID è **2310.10196**, il DOI dice **2308.10278** = **un altro paper**. Un click e il commissario atterra altrove.
3. **✗ Anno**: chiave `jin2023`, campo `year=2024`, nota `arXiv ott. 2023`, versione letta **v3 giugno 2026**. Quattro anni in gioco.
4. **✗ Autori**: la v3 ne ha **16**, l'ordine è Jin, **Kong**, Liang, Zhang, Xue, Wang, Zhang, Wang, Chen, Li, Tseng, Zheng, Chen, Xiong, Pan, **Wen**. Il bib segue una versione precedente.
5. **✗ Nota**: il quote `"still an under-explored problem"` **non esiste in nessuna forma**; le pagine sono di un'altra versione (Tab. 3 è **p. 21** non p. 14; §7.3 è **p. 23** non p. 16).

**Azione — tieni la chiave** `jin2023surveyts` (non rompere i `\cite`), correggi i campi:
```bibtex
journal = {arXiv preprint arXiv:2310.10196},
year    = {2026},
note    = {Version 3, 8 June 2026. Manuscript submitted to ACM.},
doi     = {10.48550/arXiv.2310.10196}
```
+ aggiungere **Yaxuan Kong** in seconda posizione.

⚠️ **Conseguenza strategica del 2023 → 2026:** se il framing era *"già notato nel 2023 e ancora aperto"*, quello muore. Ma una survey di **giugno 2026** a una difesa di **settembre 2026** dice che il gap è vivo **da tre mesi** — non un'osservazione stantia che qualcuno potrebbe aver colmato. **Ti conviene.**

---

# PARTE C — Igiene bibliografica (meccanica, basso rischio, alto guadagno)

## C1 · 🔧 Campi `note` stampati nel PDF · (a) — **1 solo prompt**
**Problema:** **113 campi `note`** nel master contengono annotazioni italiane, path locali (`literature/papers/...`), email (`artem.maryanskyy@uber.com`). Lo stile LaTeX **li stampa**. Confermato: in bibliografia si leggono "Key related work:", "Gap evidence:", "Confirms gap:"...
**Azione:** spostare in campo `annotation` (non stampato) o strippare i `note` pre-build.

## C2 · 🔧 Deduplica cross-file · (a)
**Problema:** stessa opera in più `.bib` → doppie numerazioni. **Confermati:** Sculley (3 file → [65]/[93]), He (3 chiavi), FactoryNet (2 file, identica).
**Da verificare:** [73] "**Farah** Abdoune" vs [75] "**Farid** Abdoune" — titoli simili: stesso paper con nome sbagliato?
**Azione:** una chiave canonica per autore-anno; consolidare o deduplicare i file caricati dalla build.

## C3 · 🔧 8 autori PLACEHOLDER stampati in bibliografia · (a) — **ALTA PRIORITÀ**
**Problema:** la bibliografia stampa autori-segnaposto. Un commissario che legge *"PHMForge Authors"* capisce che la voce è stata compilata **da una descrizione, non dal paper** — e questo mette in dubbio retroattivamente anche le citazioni buone. (Nei `.bib` ce ne sono **51**; 8 nel master → stampate.)

**✅ NOTIZIA BUONA: tutti e 8 i paper ESISTONO.** Nessuno allucinato: titoli, anni e contenuti corretti. Era **sciatteria, non fabbricazione** (l'opposto di FactoryNet, dove l'autore è stato *inventato*).

| Rif | Placeholder → **Autori reali** | Sede / ID |
|---|---|---|
| **[89]** | **Ayan Das, Dhaval Patel** | arXiv `2604.01532` |
| **[94]** | ✋**A6 — da recuperare** | IEEE Xplore `11154278` |
| **[95]** | **Rong Zhou, Dongping Chen, Zihan Jia, Yao Su** + ~23 (usa "and others") | arXiv `2601.01321` |
| **[97]** | **Tavares/Giusti L.G., Lima J., Melo M., … Ogasawara E.** (~16) ✋A7 | IJCNN 2025 · Xplore `11228919` |
| **[98]** | **Dong-Hyuk Yang** + al. | dic. 2025 |
| **[101]** | **Ali Şenol** + 2 | **Electronics 2026, 15(3), 534** · `10.3390/electronics15030534` |
| **[102]** | **Raiyaan Abdullah, Yogesh Singh Rawat, Shruti Vyas** | arXiv `2508.00399` · **ICCV 2025 WS** ✋A10 |
| **[103]** | **Hanjun Luo, Shenyu Dai, Chiming Ni, Xinfeng Li, Guibin Zhang, Kun Wang, Tongliang Liu, Hanan Salam** | arXiv `2506.00641` · **NeurIPS 2025** |

**Due UPGRADE gratuiti:**
- **[103] non è un preprint: è NeurIPS 2025** (proceedings vol. 38, pp. 43241–43298). Citare NeurIPS rafforza la tua fondazione sulla safety evaluation.
- **[102]** è **ICCV 2025 Workshops (VISION'25)**, non solo arXiv.

**⚠️ ERRORE FATTUALE nella nota [97]:** scrivi *"no industrial validation framework"* — ma FEDD **è validato su dati industriali reali** (dataset **3W**, pozzi petroliferi) ed è motivato da oil & gas (perdite finanziarie, sicurezza personale, rischio ambientale). Un commissario apre il paper e ti smentisce.
🔧 **Riformulare:** *"validated on oil & gas process data (3W), not on manufacturing prognostics; no edge latency budget, no model selection component"* — resta gap evidence, inattaccabile.

## C4 · 🔧 Check autori su TUTTE le 116 · (a) — **voce sistemica, lezione FactoryNet**
**Perché:** il campo autore può essere **allucinato anche quando l'arXiv ID è corretto**. Non basta controllare le 8 con placeholder.
**Azione:** passata meccanica — per ogni entry con DOI/arXiv, confrontare la lista autori con la fonte. Veloce e automatizzabile.
**Già trovati:** [92] autore inventato · [71]/[72] autori incompleti · [34] autore discordante tra file · [53] DOI→paper sbagliato · [34] DOI placeholder.

## C5 · 🔧 Refusi residui · (a)
"Section V-G" (residuo template IEEE) · riferimento errato a Table 11 · "seven-type classifier" testato su 5 tipi · cohort held-out §3.3 ("seeds 0-4 plus 42,88,123") vs §3.9 ({42,99,123,7,88}) · "god node" mai definito · "23 core papers" vs 110+ voci.


**🆕 Riga 1480 — refuso da correggere:** *"FAR of 0.000 across all **seven drift types evaluated** in this work"* → **falso**: ne valuti **cinque**. Le righe 1692 e 2402 dicono correttamente *"five types × five seeds"*.
→ *"FAR of 0.000 across the 25 held-out scenarios (five drift types × five seeds)"*.

**🆕 Framing tassonomia (non è un refuso, è un'occasione).** I DD docs spiegano i sette: il tree emette **7 label**, gli scenari sono **5**. Ancoralo al canone — Abbasi attribuisce i quattro tipi canonici al suo rif. [36] = **Lu et al. 2018 = il tuo [67]**:
> *"The canonical taxonomy distinguishes four drift types — sudden, gradual, incremental, reoccurring [67]. DMCA-Drift implements three (ABRUPT, GRADUAL, INCREMENTAL) and adds two classes absent from the canonical taxonomy but operationally decisive: VARIANCE_SHIFT and OUTLIER_DRIVEN, which do **not** warrant a model swap. The taxonomy is action-oriented rather than phenomenological. Reoccurring drift is not evaluated (Limitations)."*

**Diventa un contributo, non un'anomalia da giustificare.** Il tuo DD-06 lo motiva già: *"INCREMENTAL classificato come ABRUPT — wrong type, right action"*.

## C6 · 🔧/✋ Risultati propri dentro la lit review · (a/b)
**Problema:** §2.12.4 riporta risultati tuoi (FAR=0.000 "seven types") **dentro la rassegna della letteratura**, via [3] Maryanskyy. Confonde il confine stato-dell'arte / contributo.
**Azione:** spostare i risultati propri nel capitolo esperimenti. ✅ **[3] NON è tuo** (Maryanskyy/Uber, autore unico) → **l'autocitazione non esiste**. ✅ **FAR = tue simulazioni** (A9 chiusa). Resta valida la regola: i risultati propri non stanno nella lit review. → per [3] vedi **B16**.

---

# PARTE D — Vulnerabilità di contenuto

> **D1+D2 sono il cuore tecnico e ora sono UNA SOLA voce** (vedi sotto: k e SLA entrano solo come rapporto). È l'unico blocco che richiede di **rieseguire codice**, non editare prosa.

## D1+D2 · 🧮🔧➕ SLA come parametro + sensitivity su k/SLA ⚠️ · (a) — **PRIORITÀ MASSIMA**

### Il problema, in tre strati

**Strato 1 — la frase auto-confutante (righe 3442–3443, §5.6).** Il testo dichiara:
> *"a model with ℓnano = 537 ms can sustain at most ⌊10,000/537⌋ = 18 evaluations per 10 s inter-arrival interval; **the pipeline commits exactly one inference per cycle, leaving the remaining capacity idle**."*

Se il pipeline fa **1 inferenza per ciclo** e Moirai ne regge **18**, allora **Moirai non perde nessuna finestra** → coverage 100%, non 9.1%. Questa singola frase **distrugge C4, il gap 150s e C6**. È la frase più pericolosa della tesi.

**Strato 2 — narrativa e analogia incompatibili con Tabella 12.**
- Righe 153–157: *"If inference takes 5.4 s (537 ms × 10)"* → **applica il ×10 due volte** (537ms è già la latenza Jetson in Tab. 12).
- Analogia della guardia: *"110 s per photo"* → assume che Moirai impieghi **110 secondi**, cioè **200×** la latenza della tua stessa tabella.

**Strato 3 — l'errore di categoria all'origine: un SLA non è una proprietà dell'hardware.**
Un Jetson Nano **non ha** un SLA: ha 4GB di RAM, 25.6 GB/s di banda, 472 GFLOPS. "Rispondere entro 50ms" è un **requisito dell'applicazione**. È lo stesso errore di **B4** (chiedere a una scheda tecnica un fattore di conversione): il numero è tuo, non della fonte.
Origine reale del 50ms: **il ciclo OPC-UA del Case Study A** (riga 3905: *"20 OPC-UA cycles at 50 ms"*) — lì il dato arriva ogni 50ms, quindi l'SLA **è** il periodo di acquisizione ed è fisicamente vincolante. Poi è diventato *"50 ms industrial SLA threshold"* (Fig. 15) e applicato a **PRONOSTIA, dove il dato arriva ogni 10 s: 200× più lento**.

**La tesi ha tre SLA diversi:**
| Dove | Significato |
|---|---|
| Narrativa Tab. 12 | scadenza entro l'arrivo del prossimo dato |
| **Fig. 18** | **cadenza**: una risposta ogni 50ms ("SLA windows (50 ms each)") |
| Riga 226 | solo gate di ammissibilità TOPSIS |

**Perché la logica Tarr è esclusa:** a Tarr = 10s **tutti** i modelli passano (100/100/100) → la metrica di coverage diventa **vacua** su PRONOSTIA → **C4 muore**. Non è un'opzione.

### La soluzione: SLA = 100 ms da TS 22.104 **Table 5.2-2**, riga *"vibration sensor"* ✅ VERIFICATO SUL PRIMARIO

**⚠️ CORREZIONE — il range "0.5–500 ms" era SBAGLIATO.** Veniva da una fonte che *citava* **TR 22.804 §8.1.2** (il Technical Report di studio, un altro documento). Nella **TS 22.104 Table 5.2-1** i transfer interval vanno da **500 μs** (motion control) a **60 s** (plant asset management). **Non citare "0.5–500 ms".** Se serve un range da 5.2-1 è **500 μs – 60 s**, ed è **osservazione tua sui valori tabulati**, non citazione.

**LA tabella: 5.2-2 — "Communication service performance requirements for industrial wireless sensors".** Contiene la tua applicazione **nominata**:

| Availability | Reliability | **E2E latency** | **Transfer interval** | Remarks |
|---|---|---|---|---|
| 99.99 % | ≥ 1 week | **< 100 ms** | 100 ms to 60 s | Process monitoring, e.g. temperature sensor (A.2.3.2) |
| 99.99 % | ≥ 1 week | **< 100 ms** | **≤ 1 s** | **Asset monitoring, e.g. vibration sensor (A.2.3.2)** ← **PRONOSTIA** |
| 99.99 % | ≥ 1 week | < 100 ms | ≤ 1 s | Asset monitoring, e.g. thermal camera (A.2.3.2) |

**Il colpo: lo standard DISACCOPPIA latenza e transfer interval.**
- **Table 5.2-1** (periodic deterministic): colonna "End-to-end latency: maximum" = **"< transfer interval value"** riga dopo riga → latenza legata al periodo.
- **Table 5.2-2** (industrial wireless sensors): latenza **< 100 ms assoluti** con transfer interval **≤ 1 s** → **fattore 10 tra requisito e periodo, scritto senza giustificazione**.

**Questo legittima esattamente la tua struttura.** Un SLA molto più stretto del periodo di acquisizione **è la forma normale della classe asset-monitoring nello standard**. → **Il multi-asset non serve più. N=200 è morto. A12 si chiude.**

**Il tuo 50 ms non sparisce:** resta valido per altre classi — *process automation closed-loop* (A.2.3.1, transfer interval ≥ 10 ms, latenza < transfer interval) e *primary frequency control* (A.4.2, ~50 ms). Diventa il **caso stretto della sensitivity**, non il default. **100 ms è già nel tuo §3.6** (profilo RPi).

**Formulazione da scrivere:**
> *"The SLA is not a hardware property but a deployment requirement, declared in the AAS DeploymentPolicy (Table 11, latency class). 3GPP TS 22.104 Table 5.2-2 specifies, for industrial wireless sensors performing asset monitoring (e.g. vibration sensors, clause A.2.3.2), an end-to-end latency requirement below 100 ms with a transfer interval of up to 1 s — a latency budget deliberately tighter than the acquisition period. We adopt 100 ms as the reference SLA for the bearing-monitoring scenario, and report sensitivity across SLA ∈ {10, 50, 100, 500, 1000} ms, spanning the adjacent classes tabulated in TS 22.104 (closed-loop control, A.2.3.1; plant asset management, A.2.3.3)."*

### Il regalo: la sensitivity resta a UNA dimensione

$$s = \left\lceil \frac{\ell_{nano}}{SLA} \right\rceil = \left\lceil \frac{k \cdot \ell_{T4}}{SLA} \right\rceil$$

**k e SLA entrano solo come rapporto k/SLA.** Una sola tabella copre **entrambe** le incertezze: sweep su SLA ∈ {10, 50, 100, 500, 1000} ms a k=10 è matematicamente identico a sweep su k a SLA fisso. **Il range te lo danno le classi di TS 22.104, non la tua fantasia.**

### Modifiche concrete

1. 🔧 **Eq.10: `round()` → `⌈⌉`.** L'arrotondamento è il trucco che salva PatchTST al confine. Ceiling = uniforme per tutti, nessuna eccezione per l'eroe.
2. 🔧 **Cancellare la frase "18 evaluations"** (Strato 1). Senza il multi-asset non ha più alcuna funzione: era l'ammissione che la capacità resta idle, cioè l'auto-confutazione del 9.1%. **Va via e basta.**
3. 🔧 **Riscrivere l'analogia della guardia** (Strato 2): oggi è numericamente incompatibile con Tab. 12 (110 s/foto vs 537 ms reali). Riscriverla sulla **cadenza SLA**: *"il requisito è una risposta entro 100 ms; un modello a 537 ms non può rispondere in tempo e la finestra viene saltata — 1 su 6."*
4. 🧮 **Rifare Tabella 12** con SLA = 100 ms e ceiling:

| Modello | ℓT4 | ℓnano (k=10) | s = ⌈ℓ/100⌉ | c_eff |
|---|---|---|---|---|
| PatchTST | 5.9 ms | 58.6 ms | **1** | **100%** |
| Lag-Llama | 7.8 ms | 77.7 ms | **1** | **100%** |
| **Moirai-S** | 53.7 ms | 537.3 ms | **6** | **16.7%** |

**Lag-Llama 100% vs Moirai 16.7% = 6× di differenza.** La storia qualitativa regge intatta — e stavolta con un SLA che viene da una riga di standard che **nomina i sensori di vibrazione**, non dal ciclo OPC-UA di un altro caso studio.
⚠️ **La colonna K = ⌊Tarr/ℓ⌋ va tolta dalla tabella**: senza il multi-asset non ha significato, ed è la porta da cui rientra l'auto-confutazione.

5. 🧮 **Sensitivity su k/SLA** (fonde la vecchia D1). ⚠️ Correggere anche i **fattori asimmetrici**: §5.5/Fig.18 usa PatchTST a **×5** (29.3ms) e Moirai a **×10** (537ms) **nella stessa formula**.
6. 🧮 **Eq.11 va ricalcolata:** con s=6 → ∆tmax = (2·6−1)×10s = **110 s**. ⚠️ **Il gap empirico di 150 s NON è più contenuto dal bound.** Due possibilità: (a) rieseguire la simulazione a s=6 e riportare il nuovo gap; (b) verificare che il bound valga solo sotto l'ipotesi dichiarata ("ampiezza sopra soglia per tutta la finestra"). **Da chiudere con il re-run, non a tavolino.**

### Cosa cambia nella storia

**L'eroe resta Lag-Llama** (coerente con **D3**: PatchTST è bloccato dal Quality Gate, non dalla latenza).
> **Lag-Llama** (selezione operativa reale, **100%** coverage): allarme azionabile con margine sulla action window di 300s.
> **Moirai-S** (violazione SLA, **16.7%**): allarme in ritardo → sotto la soglia di azionabilità.

⚠️ **I numeri di lead time (410s / 280s / −20s) sono stati misurati a s=2 e s=11: vanno rieseguiti a s=1 e s=6.** La direzione qualitativa è robusta (Moirai 6× peggio), i valori a titolo no.

### Il residuo onesto da dichiarare
PRONOSTIA ha transfer interval = **10 s**. La classe *"asset monitoring, vibration sensor"* di Table 5.2-2 prevede transfer interval **≤ 1 s** → PRONOSTIA è **10× più lento** anche della classe che lo nomina. Ma il requisito di latenza (**< 100 ms**) nella 5.2-2 è **assoluto e disaccoppiato** dal transfer interval: resta valido.
> *"PRONOSTIA provides run-to-failure ground truth at Tarr = 10 s, an order of magnitude slower than the ≤ 1 s transfer interval tabulated for vibration-sensor asset monitoring (TS 22.104, Table 5.2-2, clause A.2.3.2). The latency requirement for that class (< 100 ms) is however specified independently of the transfer interval, and we adopt it as the deployment SLA. Case Study B validates the coverage metric and the missed-alarm chain under this declared requirement."*

**✅ A11 CHIUSA — verificato sul primario.** Table 5.2-2 esiste e nomina *"Asset monitoring, e.g. vibration sensor (A.2.3.2)"*: latency < 100 ms, transfer interval ≤ 1 s, availability 99.99%, reliability ≥ 1 week, densità ≤ 0.05 UE/m², range < 500 m.
**✅ A12 CHIUSA — il multi-asset non serve.** Lo standard disaccoppia già latenza e transfer interval per questa classe. **N=200 eliminato.**
**✋ Resta da leggere (basso rischio):** **clause A.2.3.2** (p. 37, "Process and asset monitoring") — il testo che descrive il caso d'uso, utile per dire *perché* < 100 ms.

## D3 · 🔧 Storia del modello selezionato ⚠️ · (a)
**Problema:** **tre** modelli indicati come "selezionato": PatchTST (abstract, MAE 0.019), Lag-Llama (ablation/Fig.17/Case Study A), chronos-t5-tiny (§3.10). Il MAE **0.019 è orfano** (in nessuna tabella).
**Azione:** 🔧 riscrivere abstract/C1 con la **storia vera**: TOPSIS ranka PatchTST #1 → **Quality Gate lo blocca** (zero-shot collapse) → **Lag-Llama operativo**. **È una storia migliore: dimostra che il gate funziona.** Tracciare/eliminare lo 0.019.

## D4 · 🔧 Abstract attribuisce a ETT-h1 i numeri di CMAPSS ⚠️ · (a) — **PRIORITÀ ALTA**
**Problema:** due esperimenti drift distinti — **Case Study A vero (ETT-h1):** detection t=12.362, MOMENT→Lag-Llama, drift = *miglioramento* (MAE ×0.46 per instance normalization). **Esperimento CMAPSS (calibrazione):** t=1380, chronos-t5-tiny, 78% reduction. **L'abstract attribuisce a ETT-h1 i numeri di CMAPSS** — dataset che §3.18 dichiara di **sola calibrazione**.
**Azione:** 🔧 correggere l'attribuzione. Etichettare i dataset ovunque (5.86 = CMAPSS, 3.02 = ETT-h1).

## D5 · 🔧 Diagnosi PatchTST MAE=RMSE ⚠️ · (a)
**Problema:** Cap.4 dice **"artefatto n=1"**; Cap.5 dice **"collasso zero-shot genuino"**. Incompatibili — e se fosse n=1, MAE=RMSE varrebbe per **tutti** (MOMENT 0.114 ≠ 0.172 lo smentisce).
**Azione:** 🧮 verificare empiricamente (re-run 24 step) e 🔧 allineare. Probabile: **collasso genuino** (coerente con D3).

## D6 · 🔧 Tabella 15 — MAE cross-family · (a/b)
**Problema:** la nota † dichiara i MAE probabilistici *"not directly comparable"*, ma §5.5 e §1.2 li confrontano ("Moirai 6.1× more accurate"). **TOPSIS pesa MAE 0.50 su colonna a unità miste.**
**Azione:** 🔧 rimuovere i confronti cross-family nel testo; appoggiarsi a `has_measured_mae` (DD-03), **dominanza latenza**, CRPS (§6.2). (b) preparare la risposta orale: TOPSIS regge per dominanza latenza.

## D7 · 🔧 Esempio motivante §1.2 — sostituire · (a) — **ALTO RENDIMENTO**
**Problema:** l'esempio Moirai-vs-PatchTST somma **tutte** le patologie: unità non comparabili, MAE 1.303 conteso, fattori ×5/×10 asimmetrici, **terza logica di scheduling** (saturazione continua, 122.900 checks/h).
**Azione:** 🔧 sostituire con il **paradosso TimesFM vs MOMENT**: 0.0064 vs 0.114 **stesse unità**, 2039 vs 29.7ms **stesso hardware**, **69× latenza che sopravvive a ogni conversione**. Un esempio pulito che non espone nessun fianco.

## D8 · 🔧 Gap §1.1 sovradichiarato · (a)
**Problema:** "AAS as **live** input" e "re-triggers when DT detects **profile change**" → nemmeno DMCA lo fa (JSON statici DD-01; re-trigger su **drift dati**, non su cambi AAS; BaSyx è future work). Il qualificatore "for HuggingFace models" restringe il gap a **tautologia**.
**Azione:** 🔧 *"vincoli DT strutturati → selezione multi-criterio + ri-selezione da catalogo su drift"*.

## D9 · 🔧 Gap Matrix (Tab. 7) vs §6.2 ⚠️ · (a)
**Problema:** assegna **✓ a G5** (trust calibration) contraddicendo §6.2 che lo elenca come non risolto.
**Azione:** 🔧 **✓ → ∼**. Coerenza con le honest limitations.

## D10 · ➕ Costo economico del downtime · (a)
**Problema:** il pain economico è **asserito, mai quantificato** (manca €/ora).
**Azione:** ➕ mezza pagina con dati di letteratura.
**DOI:** ✋ da identificare · **verifica manuale:** cifra €/ora o $/ora **con settore specificato**. Candidati: report Deloitte/McKinsey su unplanned downtime, o paper PdM con costi. *Distinto da B11* (che copre l'asimmetria metodologica, non il valore economico).

## D11 · 🔧 Case Study B — da "limite" a CONFORMITÀ ISO 13374 · (a/b) — **RIBALTAMENTO**
**Vecchia diagnosi:** *"nessun modello ML fa inferenza — l'allarme è una soglia RMS (µb+3σb, k=2); i modelli sono solo donatori di latenza"* → sembrava una scorciatoia da confessare.

**Nuova lettura — è il blocco SD dello standard.** ISO 13374 definisce il reference processing model a sei blocchi: **DA** (data acquisition) → **DM** (data manipulation) → **SD** (state detection) → **HA** (health assessment) → **PA** (prognostics assessment) → **AG** (advisory generation). Il blocco SD fa esattamente *threshold checking contro setpoint predefiniti — zone ISO 10816 o variazioni dal baseline — assegnando uno stato discreto* (Normal / Acceptable / Alert / Danger).

Quindi: **RMS = blocco DM** (feature extraction) · **soglia µb+3σb = blocco SD** (state detection) · **catalogo TSFM = livello PA**. Il tuo Case Study B **non salta l'ML: implementa i blocchi DM+SD dell'architettura ISO standard**, e valida il vincolo di scheduling sul percorso DM→SD — che è **dove si decide la tempestività dell'allarme**.

**Azione:** 🔧 riformulare C6:
> *"Case Study B instantiates the DM (RMS feature extraction) and SD (state detection against a per-bearing baseline) blocks of the ISO 13374 reference processing model. The TSFM catalog operates at the PA layer. The experiment validates the scheduling constraint on the DM→SD path — the block where alarm timeliness is determined."*

**Nota da aggiungere:** ISO 10816 (oggi **ISO 20816**) definisce zone di severità vibrazionale **assolute**; il tuo µb+3σb è un baseline **statistico per-cuscinetto**. Entrambi legittimi — **dichiara la differenza** invece di ignorarla.

**La storia sopravvive onesta:** Lag-Llama (selezione operativa vera, 50% coverage) → allarme azionabile **410s** vs **280s (−20s di margine)** di Moirai. Eq.11 `∆tmax=(2s−1)×10s` regge (bound 210s contiene il gap empirico 150s).

**⚠️ Resta (c):** valida la **metrica coverage** e la catena missed-alarm, **non** il re-alignment end-to-end. Dichiararlo.

## D12 · 🔧 RQ4 senza risposta empirica · (a/b)
**Azione:** 🔧 riformulare come **design question** (a), oppure (b) difesa orale che la inquadra come contributo architetturale.

## D13 · 🔧 Auto-approve / invariante τ bypassato · (a/b/c)
**Problema:** Case Study A **bypassa l'invariante τ=10%** (`mae_shadow=null`, "improvement assumed OK"); swap verso candidato **mai misurato** dopo un miglioramento del 54%; auto-approve timeout 30s SIL=1 (vs 60s in C5). Profilo *"Jetson Nano SLA=100ms"* contraddice §3.6 (Jetson=50ms, RPi=100ms).
**Azione:** 🔧 correggere profilo e timeout; (b) difendere l'auto-approve come scelta esplicita per SIL basso, con rollback come rete.
**Nota:** shadow deployment surrogato quasi-circolare (MAE candidato = rapporto benchmark × Uniform(0.95,1.05)) → il "78% reduction" **non è misurato**. Riproducibilità 3 seed = test di **determinismo** (σ=0), non di robustezza. Dichiararlo.

## D14 · 🔧 Incoerenze numeriche sparse ⚠️ · (a)
PatchTST 5.86 vs 3.1 ms (→ etichettare dataset, vedi D4) · "10:1" ma 0.006→0.114 = **19:1** · "107×–348×" vs "348:1" · Chronos-L "940ms/3302MB" vs tabella **830/2771** · "203×" vs "348×" · "90% of real edge devices" **senza fonte** · "30-100ms SLA bands" vs profilo Orin 20ms.
**Azione:** 🔧 passata dedicata, **un numero alla volta**, verificando contro le tabelle sorgente.

## D15 · 🔧 Tassonomia L1/L2/L3 — unificare · (a)
**Problema:** **tre definizioni di L3** ("historical metrics" §3.7, "historical context" §3.10, "counterfactual" C5+§6.1) e **due meccanismi** (§2.4 SIL-driven; §3.10 esitazione temporale).
**Azione:** 🔧 dichiararli **complementari**, unificare L3 in **una** definizione.

## D16 · ➕ Gap statement — **ora ancorato ad Abbasi [71], non a ISO** · (a) — 🆕 **RIVISTO**
⚠️ **L'ancora migliore non è più ISO.** Abbasi [71] elenca le **quattro fasi** del semantic drift management — identification, characterisation, **maintenance**, propagation — e dichiara di affrontare **solo le prime due**. **La fase maintenance è DMCA.** Fonte peer-reviewed (MODELS'24), che hai in mano, e che ti dà lo spazio **per scope dichiarato degli autori** invece che per assenza.
→ **Usa la formulazione di B12 punto 3.** ISO 13374 resta utile per **D11** (i sei blocchi che legittimano Case Study B), non per il gap statement.

## D17 · ➕ OSA-CBM "Human Interface" come ancora per GAP 3 · (a) — 🆕
**Cosa ti dà:** OSA-CBM (MIMOSA) **estende ISO 13374 aggiungendo strutture dati e definendo lo "Human Interface" come funzionalità**. Esiste quindi un **blocco Human Interface standardizzato** nell'architettura di riferimento del condition monitoring.

**Azione:** ➕ ancorare il copilot: non stai inventando un'interfaccia — stai **istanziando una funzionalità prevista da OSA-CBM**, che nessuno ha però implementato come **XAI conversazionale a livelli L1–L3**. Rinforza GAP 3 senza inventare nulla.
**Si aggancia a:** D15 (unificare L3) e B7 (He: la confidence deve seguire il quality gate, non la fluency).

---

# PARTE E — Aggiunte candidate (verificate, opzionali)

> Solo se aggiungono valore reale. Ognuna con DOI + parola da verificare a mano.

| # | Cosa | Perché | DOI | ✋ Verifica manuale |
|---|---|---|---|---|
| **E1** | **Scoring PHM 2012** (dentro [88]) | Rimpiazza il claim "10×" con un numero **vero e preciso** (4× emivita) | vedi B11 | costanti **5** (late) / **20** (early) nella §5 di PRONOSTIA |
| **E2** | **FactoryBench** | **Materiale forte e reale per GAP 4 e per L3 counterfactual**: Q&A su 4 livelli causali (state, intervention, counterfactual, decision) su telemetria robotica industriale; **nessun LLM frontier supera 50% sui livelli strutturati né 18% sul decision-making** | arXiv `2605.07675` | cifra **"18% decision-making"** |
| **E3** | **FITS** | **Oro per l'argomento edge**: eguaglia PatchTST con **~10k–50k parametri** (un layer lineare complex-valued in frequenza) — 2 ordini di grandezza sotto i transformer, 1 sotto DLinear. È il caso limite della tua tesi | arXiv `2307.03756` **⚠️ da confermare** | cifra **"10k–50k parametri"** + ID arXiv |
| **E4** | Krishnamoorthi 2018 (INT8) | Solo se ti serve un numero INT8 reale (vedi B9) | ✋ da identificare | misure INT8 specifiche |
| **E5** | Fonte costo downtime | Vedi D10 | ✋ da identificare | €/ora con settore |
| **E6** 🆕 ✅ | **3GPP TS 22.104** (via **ETSI TS 122 104 v17.7.0**, PDF **gratuita**) — **VERIFICATA SUL PRIMARIO** | **L'ancora dell'SLA** (D1+D2). **Table 5.2-2**, riga *"Asset monitoring, e.g. vibration sensor (A.2.3.2)"*: **E2E latency < 100 ms**, transfer interval ≤ 1 s, availability 99.99%. **Table 5.2-1**: colonna E2E latency = *"< transfer interval value"*. Classi adiacenti per la sensitivity: A.2.3.1 (closed-loop, ≥10 ms), A.2.3.3 (plant asset mgmt, 100 ms–60 s) | `etsi.org/deliver/etsi_ts/122100_122199/122104/17.07.00_60/ts_122104v170700p.pdf` | ✅ fatto. ⚠️ **NON citare "0.5–500 ms"** (era TR 22.804 via fonte secondaria). Range reale Tab. 5.2-1: **500 μs – 60 s**, e come **osservazione tua** |
| **E7** 🆕 | **ISO 13374** (parti 1–4) | **NON dà l'SLA.** Dà: (a) l'architettura a 6 blocchi che **legittima Case Study B** (D11); (b) il **gap statement da scope** (D16) | ISO 13374-1:2003 · -2:2007 · -3:2012 · -4:2015 | scope dichiarato (**sample gratuito** su `cdn.standards.iteh.ai`; testo integrale a pagamento) |
| **E8** 🆕 | **OSA-CBM** (MIMOSA) · **ISO 10816/20816** | OSA-CBM: blocco **Human Interface** → ancora GAP 3 (D17). ISO 10816/20816: **zone di severità vibrazionale assolute** → confronto col tuo µb+3σb (D11) | — | che OSA-CBM definisca Human Interface come funzionalità; zone ISO 10816 |

---

# PARTE F — Esecuzione LaTeX su Claude Code

## F.1 Ordine consigliato
1. **✋ PARTE A** — ✅ **A1, A2, A4–A12 chiuse.** Restano **due** voci:
   - **A3** (catena ICSE-NIER — 5 minuti, apri la bibliografia del PDF)
   - **A13** 🧮 **il re-run a SLA=100ms — blocca il cuore tecnico.** Fallo per primo.
2. **Meccanici** (rischio zero, alto guadagno): **C1** (note bib) → **C3** (autori placeholder) → **C2** (dedup) → **C4** (check autori) → **C5** (refusi + riga 1480).
3. **Citazioni**: **B1→B17**, una per prompt. Le ⚠️ toccano più punti — **elenca TUTTE le righe nel prompt**.
   → **Priorità: B16** (Maryanskyy, tocca C1) e **B17** (DOI Jin che punta a un altro paper).
4. **🧮 Cuore tecnico** (un blocco solo, con verifica in mezzo): **D1+D2** (SLA=100ms da Table 5.2-2 + ceiling + Tab. 12 + sensitivity k/SLA) → **D3** (storia modello: Lag-Llama eroe) → **D4** (abstract/dataset).
5. **Ancore** (basso rischio, alto rendimento): **B12 punto 3** (le quattro fasi di Abbasi = gap statement) → **D11** (ISO 13374 → Case Study B) → **D17** (OSA-CBM → GAP 3).
6. **Contenuto restante**: D5→D10, D12→D15.
7. **Semplificazione**: vedi F.3.
8. **Polish**: rilettura abstract / §1.2 / §6.2.

## F.2 Template di prompt (riusabile)
```
Contesto: tesi LaTeX DMCA. Intervento [ID pipeline, es. B5].
Problema: [una frase].
Modifica: [testo esatto vecchio → nuovo].
Punti da toccare: [TUTTE le righe/sezioni — critico per i ⚠️].
NON toccare: [scope negativo — evita il drift].
Dopo la modifica: ricompila e mostrami il diff dei soli punti toccati.
```
> Lo **scope negativo** ("NON toccare") è l'accorgimento che più riduce il drift quando deleghi modifiche LaTeX a un agente.

## F.3 Semplificazione (dopo la stabilizzazione)
**Principio: ogni claim rimosso è un fianco chiuso.** Non è cosmesi — è riduzione della superficie d'attacco.
- Confronti cross-family che non reggono (D6) → **rimuovere**, non puntellare.
- Terza/quarta logica di scheduling (§1.2, 122.900 checks/h) → **eliminare** con D7.
- Claim di novità non verificati ("first", "no existing method", "the strongest") → **ammorbidire o rimuovere** (B12, B15, B13, B14).
- Tassonomia L3 con tre definizioni → **unificare** (D15).
- Numeri orfani (0.019 MAE) → **tracciare o eliminare** (D3).
- Ogni tabella: **una sola fonte di verità per ogni numero**.

## F.4 Double-check finale
- [ ] ✋ Tutte le azioni PARTE A chiuse (A1–A10)
- [ ] Nessun numero con due valori diversi in punti diversi (grep dei numeri chiave)
- [ ] Abstract, §1.2, C1 raccontano **la stessa storia** (Lag-Llama operativo, gate che funziona)
- [ ] **Una sola** logica di scheduling in tutta la tesi
- [ ] Sensitivity su k presente e citata dove serve (C4/C6/§5.5/§5.6)
- [ ] Gap Matrix coerente con §6.2 (**G5 = ∼**)
- [ ] Nessun campo `note` stampato; nessun path/email locale
- [ ] Nessun autore placeholder; **nessuna doppia numerazione**
- [ ] Autori verificati contro DOI/arXiv su tutte le entry (C4)
- [ ] Ogni ➕ ha DOI verificato e parola-chiave controllata a mano
- [ ] Nessuna quote tra virgolette senza riscontro diretto sul PDF

---

# APPENDICE — Scoreboard audit (18 riferimenti, CHIUSO)

| Rif | Claim | Esito |
|---|---|---|
| [40] Banbury | "10.000× latency" + "sub-1MB saturates" | ✗✗ due punti |
| [67] Lu | "Section VII flags catalog drift response" | ✗ fabbricazione |
| **[68] Shankar** | 2 quote §4.2/§4.5.1 | **✓ verbatim** (1 fix §5.1.2) |
| [84] datasheet | fattore 5–20× | ✗ stima→fonte |
| [65/93] Sculley | "10% operational guidance" + CACE + dup | ✗ |
| [54] Liang | "15–40% / 5% / one-tenth" | ✗ fabbricazione quant. |
| [34] He | "RSR 0.57→0.11" + metrica + DOI | ✗ |
| [53] Jin | Tab.3 / §7.3 / DOI | ~ (fatto OK, quote ✋) |
| [59] Menghani | "2–4× / <1% / >10M" | ~ numeri decorativi |
| **[55] Benmeziane** | tassonomia + open problems | **✓** (etichette) |
| [88,89] | "missed alarm 10× costlier" | ✗ (**ancora 4× trovata**) |
| [71] Abbasi | "the first formal taxonomy" | ~ ("first" tuo; autori ×2) |
| [92] FactoryNet | numeri ✓, "first" ✓, **autore ✗✗** | ~ |
| **[52] Zeng bib** | autori/sede/DOI | **✓** |
| [52] Zeng claim | "5 of 6" / "two-layer" | ~ (nove/tutti; un layer) |
| [51] TimeMixer | "first 2024 architecture" | ✗ |
| **[89,94,95,97,98,101,102,103]** | esistenza | **✓ tutti reali** (autori da compilare) |

**Sintesi:** 5 fabbricazioni · 3 misattribuzioni · 3 superlativi indifendibili · 2 numeri decorativi · **3 reggono** · 2 voci sistemiche (C3, C4).
