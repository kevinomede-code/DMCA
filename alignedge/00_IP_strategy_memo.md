# IP Strategy Memo — Tesi · Collaborazione SystemX · Startup AlignEdge

**Autore:** Kevin Omede
**Data:** 2026-06-25
**Stato:** Working draft, da rivedere prima di firmare qualunque accordo

---

## TL;DR (4 punti)

1. **NON sanitizzare la tesi.** È il peggior compromesso possibile: indebolisce il contributo accademico, segnala diffidenza ai collaboratori, e *non* protegge davvero la startup perché il vero moat di AlignEdge non è l'algoritmo.
2. **Il moat di AlignEdge sta nell'esecuzione e nei dati**, non nel framework DMCA pubblicato. Pubblicare apertamente la ricerca *rafforza* la startup (credibilità, sales, hiring, investor signal) invece di danneggiarla.
3. **Tesi, collaborazione SystemX e startup devono essere tre layer separati ma allineati.** Layer 1 (tesi pubblica) = fondamenta accademiche; Layer 2 (joint paper con SystemX) = estensione standardizzata, co-owned; Layer 3 (startup) = runtime di produzione, dati di deployment, integrazioni — sempre privato.
4. **Prima di firmare con SystemX serve un passaggio dal TTO Polito (RIMIN/I3P).** Standard practice nel deep-tech, gratuito, e ti protegge dalle clausole più problematiche dei contratti di RTO francesi.

---

## 1 · Il framing sbagliato vs quello giusto

**Domanda sbagliata:**
*"Devo creare una versione 'sanitized' della tesi che nasconde i dettagli tecnici che diventeranno secret sauce della startup?"*

Risposta: no. Tre motivi.

- **Indebolisce il contributo accademico.** Una tesi più povera di dettaglio è più difficile da difendere alla commissione, viene citata di meno, e — se mai pubblicata su IEEE TII come da outline — viene rifiutata in revisione perché non riproducibile.
- **Segnala diffidenza.** Simeone, Belfadel e Anwer si accorgono subito che il working draft pubblico è una versione depurata. Anwer (CIRP, ISO TC 213) è esattamente il tipo di reviewer che pretende riproducibilità. Sospetti sulla buona fede danneggiano la collaborazione.
- **Non protegge niente di reale.** Il framework DMCA descritto in tesi (5-stage loop, ADWIN+v3.1.1, TOPSIS, AAS Type 1, benchmark T4) è già descrivibile in 2 paragrafi del tuo positioning AlignEdge pubblico — non c'è nulla da "nascondere" che cambi il vantaggio competitivo.

**Domanda giusta:**
*"Dove sta davvero il moat di AlignEdge, e come faccio in modo che tesi + collaborazione + startup si rafforzino a vicenda invece di farsi concorrenza?"*

---

## 2 · Dove sta davvero il moat di una deep-tech come AlignEdge

Il moat in un infrastructure-layer software per AI deployment **non è mai un singolo algoritmo**. È la composizione di quattro livelli:

| Livello | Cos'è | Difendibile? | Pubblicabile? |
|---|---|---|---|
| **Algoritmo** (DMCA framework, ADWIN+v3.1.1, TOPSIS) | Idea + risultati | Debolmente: chiunque può reimplementare in 2-3 mesi | Sì — diventa credibilità |
| **Implementazione** (runtime on-device, calibrazione HW, security, OTA) | Codice + ingegneria | Mediamente: 6-18 mesi di replication time per un competitor | No — privato |
| **Dati** (multi-site deployment dataset, drift signatures per vertical, T4→edge calibration table reale) | Asset proprietario | Fortemente: cresce col tempo, non replicabile senza customer | No — privato |
| **Distribuzione** (design partner relationships, certificazioni CE, conformità AI Act, brand) | Network + compliance | Fortemente difendibile in mercati regolati | Parzialmente (case study sì, contratti no) |

**Implicazione:** il livello 1 — l'algoritmo — è il *meno* difendibile. Pubblicarlo apertamente ti costa zero in termini di moat e ti dà credibilità che gli altri tre livelli non possono comprare.

Esempi nel settore: Anthropic pubblica i paper su Constitutional AI, Hugging Face pubblica i transformer architectures, Databricks pubblica MLflow — l'algoritmo è il loss leader, il moat è altrove.

---

## 3 · La separazione a tre layer da adottare

| Asset / Componente | Layer 1 (tesi pubblica + open paper) | Layer 2 (joint con SystemX) | Layer 3 (AlignEdge privato) |
|---|---|---|---|
| DMCA 5-stage architecture | **SÌ** | — | — |
| ADWIN + classificatore drift v3.1.1 | **SÌ** | — | — |
| TOPSIS multi-criteria selection | **SÌ** | — | — |
| Quality gate 4-check | **SÌ** | — | — |
| Benchmark 8 modelli su T4 ($0.30) | **SÌ** | — | — |
| AAS Type 1 statico JSON (Phase 1) | **SÌ** | — | — |
| **AAS distribuita cloud/fog/edge** (Stage 1 extension) | — | **SÌ** | — |
| Posizionamento IEC 63278 / ISO 23247 / 30173 | — | **SÌ** (Anwer scope) | — |
| Submodel design come DT service | — | **SÌ** | — |
| Production runtime engine (edge agent reale) | — | — | **SÌ** |
| HW calibration database (T4→Nano misurato per device reale) | — | — | **SÌ** |
| Drift signatures per vertical (automotive, robotics) | — | — | **SÌ** |
| On-device security, OTA, telemetry | — | — | **SÌ** |
| Customer deployment dataset (multi-site) | — | — | **SÌ** |
| Integrazioni con sistemi customer specifici | — | — | **SÌ** |
| Conformità CE / AI Act / certification test suite | — | — | **SÌ** |
| Vision-Language-Action policy extension | — | (decidi caso per caso) | (decidi caso per caso) |

**Regola operativa:** quello che è già nella tesi al `2026-06-25` è il tuo *background IP*. Qualunque cosa sviluppi *successivamente* va etichettata e categorizzata prima di iniziarla.

---

## 4 · Cosa fare PRIMA di firmare la collaborazione SystemX

Lo dico in ordine:

1. **Vai al TTO Polito.** Mappa precisa degli uffici e contatti email (verificati 2026-06-25):

   | Ufficio | Cosa gestisce | Per quale tuo problema | Email |
   |---|---|---|---|
   | **RIMIN — Corporate Relations Office** | Framework Agreements con enti pubblici/RTO; IP management su joint research | **Accordo collaborazione SystemX** (background/foreground IP, clausole France 2030) | `RIMIN@polito.it` + cc `innovazione@polito.it` |
   | **Area TRIN** (Trasferimento Tecnologico e Relazioni con l'Industria) | Brevetti, proposte spin-off, commissione spin-off | **Costituzione AlignEdge** (spin-off Polito vs startup indipendente, regolamento 2024) | `brevetti.spinoff@polito.it` |
   | **I3P** | Incubatore Polito, post-costituzione (mentoring, fundraising, spazi) | **Setup operativo startup** dopo decisione TRIN | Via sito `i3p.it` o tramite TRIN |
   | **LabTT** (Laboratorio Interdipartimentale) | Supporto trasversale a tutti i dipartimenti | Backup se i singoli uffici ti rimbalzano | Via RIMIN |

   Tempo: 2 appuntamenti da 30 min (RIMIN + TRIN) in parallelo. Costo: zero. Fanno questo tutti i giorni.

   **Documento da scaricare e leggere PRIMA degli incontri:**
   *Regolamento Spin Off e Start Up del Politecnico di Torino* (versione dicembre 2024) — disponibile su `polito.it/sites/default/files/2024-12/Regolamento%20spin%20off%202024_0.pdf`. Determina se ti conviene qualificare AlignEdge come *spin-off Polito riconosciuto* (con benefici di network/credibilità/I3P ma possibili equity claim del Polito) o come *startup indipendente che nasce da una tesi* (più libertà, meno supporto istituzionale). Decisione da prendere con TRIN.

   **Draft email A (a RIMIN) e B (a TRIN)** sono salvati separatamente in `alignedge/email_drafts_polito.md` — vedi quella nota.

2. **Fai dichiarare formalmente il "background IP" prima della firma.** Liste cose come:
   - "DMCA framework as described in thesis_draft.tex commit `<hash>` of `2026-06-25` is K. Omede's background IP."
   - "Code in repository `<URL>` as of `<hash>` is K. Omede's background IP under MIT license."
   - "Benchmark results in `results/benchmarks/2026-04-07/` are K. Omede's background IP."

3. **Definisci foreground IP come co-owned con commercial-use rights non-esclusivi.**
   Formula tipo:
   *"Foreground IP generated jointly under the present collaboration is co-owned by the contributing parties. Each party retains non-exclusive, royalty-free, worldwide rights to use the foreground IP for both academic and commercial purposes, including incorporation into products or services."*

4. **Evita assolutamente queste clausole:**
   - Cessione esclusiva di IP a IRT SystemX (anche solo "su richiesta")
   - Patent joint filing senza commercial-use clause per Kevin
   - NDA che impedisce uso commerciale dei risultati joint
   - Obbligo di pubblicare *tutto* il codice prodotto durante la collaborazione (alcuni programmi France 2030 lo richiedono — verifica)
   - "Right of first refusal" di SystemX su qualunque commercializzazione

5. **Chiedi esplicitamente:**
   - Diritti di pubblicazione chiari (chi può pubblicare cosa, quando)
   - Diritto di citare la collaborazione come credibility signal per la startup
   - Diritto di sottoporre i risultati a EIC Advanced Innovation Challenges (è esattamente il programma su cui poggia la tua funding strategy)

---

## 5 · Rischio specifico: IRT SystemX è un RTO francese, Confiance.ai era France 2030

IRT SystemX ha gestito il programma Confiance.ai (concluso settembre 2024), finanziato da France 2030, con Renault, Valeo, Airbus, Safran, Thales come partner. Questo significa:

- **Cultura pro-publication.** Gli RTO francesi spesso *richiedono* pubblicazione aperta dei risultati joint. Buono per te (rafforza Layer 1). Da chiarire se ci sono obblighi sul codice.
- **Possibili obblighi residui France 2030.** Se la collaborazione viene inquadrata come continuazione di Confiance.ai o sotto la European Trustworthy AI Association, possono esserci clausole su open-source obbligatorio o restrizioni su exclusive licensing. **Domanda esplicita da fare:** *"Sotto quale programma quadro inquadrate la collaborazione? Ci sono obblighi di OS o di IP che derivano dal funding?"*
- **Channel a partner industriali enorme.** Renault, Valeo, Airbus, Safran, Thales sono *esattamente* i tipi di design partner che AlignEdge vuole. La collaborazione SystemX è un canale di accesso, non una minaccia. **Valeo** in particolare è già il tuo first target dichiarato (V-Max, Valeo Brain) — passare attraverso SystemX può essere più veloce della cold outreach.

---

## 6 · Cosa NON disclosure-are alla call di domani

Tieni separati i tempi:

- **Domani (call Belfadel):** allinea su *collaborazione di ricerca*. Non parlare di AlignEdge come entità commerciale ancora. Se ti chiede del futuro, di' che dopo tesi vuoi continuare a lavorare sul tema in industria, senza specificare struttura.
- **Lunedì (venture builder):** lì sì, parli di startup. AlignEdge come pitch.
- **Dopo il venture builder + check con TTO Polito:** decidi se/come comunicare a Belfadel che la collaborazione si interseca con un'attività commerciale. A quel punto sei in posizione di forza perché:
  - Hai TTO advice
  - Hai capito il programma quadro SystemX
  - Hai un framework legale per separare i tre layer

**Perché non parlare di startup domani:** non hai ancora i fatti per inquadrarla bene. Aprire la conversazione "fra l'altro sto facendo una startup su questo" senza struttura legale ti mette in posizione debole nelle clausole future. Meglio: fai partire la collaborazione su un perimetro chiaro (Stage 1 extension), e solo dopo allarghi.

**Eccezione:** se Belfadel ti chiede *esplicitamente* "hai piani commerciali?", non mentire. Rispondi sinceramente e in modo neutro: *"Sì, sto valutando un percorso post-tesi che includa anche componente commerciale. Posso tornarti con un quadro più chiaro dopo aver parlato con il TTO del Polito."* Onestà + rimando = buona fede senza esposizione.

---

## 7 · Checklist decisioni concrete

- [ ] Lasciare la tesi così com'è, defendere a luglio 2026 come pianificato.
- [ ] Lasciare il repo MIT + thesis CC BY 4.0 come dichiarato nel README.
- [ ] Procedere con joint paper SystemX su *distributed AAS extension* come outline esistente.
- [ ] Bookare incontro RIMIN (Polito) entro **lunedì 29 giugno** prima del venture builder.
- [ ] Bookare incontro I3P entro **fine settimana 5 luglio** per orientamento incorporation.
- [ ] Preparare draft contratto collaborazione con TTO PRIMA di firmare con SystemX.
- [ ] Domani: NON disclosure-are AlignEdge come entità commerciale. Stare sulla collaborazione di ricerca.
- [ ] Dopo TTO: tornare a Belfadel con quadro chiaro di separazione background/foreground IP.

---

## 8 · Come gestire Simeone (relatore Polito)

Status: pro-collaborazione SystemX, ha esplicitato che *"main sei tu"* sulla tesi. Operativamente: poco aiuto sui dettagli IP/startup.

**Cosa significa:**
- *"Main sei tu"* è il suo riconoscimento implicito che il background IP della tesi è tuo. Importante — mettilo nero su bianco in qualunque draft di collaboration agreement.
- *"Pro-collaborazione"* significa che non bloccherà il joint paper SystemX. Buono.
- *"Inutile su aiuto operativo"* significa che NON è la persona giusta a cui chiedere consigli su IP, struttura startup, term sheets. Le decisioni operative vanno al TTO/RIMIN/I3P, NON a lui.

**Regola operativa:**
- Lui resta stakeholder della **tesi**, non della **startup**. Sono due track distinti.
- Lo informi *ad alto livello* dell'esistenza della collaborazione SystemX (lo sa già) e del fatto che ti interessa il post-tesi industriale (verbi neutri: "valutare opportunità", "continuare ricerca applicata"). Niente di più, niente di meno.
- **NON gli chiedi** "Posso farci una startup?" o "Cosa pensi della struttura?". Non è il suo dominio. Una risposta improvvisata da lui rimane comunque nel record relazionale.
- **NON gli mostri** materiali AlignEdge (pitch deck, IP memo, term sheet). Quelli sono dominio TTO/I3P.
- Prima della difesa luglio 2026: continui a presentargli avanzamento *tesi*, niente *startup*.

**Cosa potrebbe diventare utile in seguito:**
- Se accetta di sedere come advisor della startup post-tesi, ben venga (network industriale italiano, credibilità Polito). Ma è una conversazione *post*-difesa, non *pre*.
- Se invece preferisce restare puramente accademico, anche bene. La separazione è più pulita.

---

## 9 · È "scorretto" validare la tesi con SystemX e poi fare startup a parte?

**Risposta breve: no, non è scorretto. È il modello più diffuso nel deep-tech mondiale.**

Esempi noti: Hugging Face (uscita da NLP accademico), Databricks (Spark da Berkeley), MongoDB (10gen da NYU), Snowflake, e praticamente ogni AI/ML startup uscita da PhD/MSc negli ultimi 15 anni. Il pattern è universale: ricerca in pubblico (paper, repo open-source) + prodotto in privato (runtime, customer integrations, dataset proprietario).

**Il principio chiaro:**

> Ricerca in pubblico e prodotto in privato non sono in contraddizione. Sono complementari. La ricerca pubblica crea credibilità, ecosistema, hiring funnel, investor signal. Il prodotto privato crea valore catturabile per i clienti. I due si rafforzano se l'IP è separato bene.

**Quando invece DIVENTA scorretto (da NON fare):**

1. Usare risorse/dati/codice di SystemX per validare *qualcosa che hai già deciso di commercializzare* senza dirglielo. → Trasparenza con timing, vedi sotto.
2. Firmare un IP framework dicendo "uso accademico only" e poi commercializzare gli stessi output senza licenza. → Negozia in apertura il "non-exclusive commercial-use right" sul foreground IP.
3. Pubblicare un paper joint dove il tuo contributo è in realtà product code che hai sviluppato per AlignEdge mentre dichiari di farlo come ricerca. → Tieni separati i tempi e i repository.
4. Far credere a Belfadel/Anwer che il loro lavoro li porterà a co-fondatori o equity quando in realtà non è il piano. → Sii esplicito.

**Il "timing of disclosure":**

- **Domani (call Belfadel):** non disclosure-i AlignEdge come entità commerciale. Motivo onesto: **non hai ancora struttura legale**, quindi non c'è niente di concreto da dichiarare. Se ti chiede, rispondi onestamente: *"Valuto un percorso post-tesi con componente commerciale, ti aggiorno appena ho quadro più chiaro."* (Vedi §6.)
- **Lunedì (venture builder kickoff):** lì sì, AlignEdge è il pitch.
- **Dopo venture builder + appuntamento TTO/I3P:** quando hai (a) struttura legale chiara, (b) advice TTO su collaboration agreement, **DEVI** scrivere a Belfadel un'email di follow-up trasparente, *prima* che il joint paper sia sottomesso. Esempio:

  > *"Update operativo: dopo la nostra call ho iniziato un percorso con [venture builder name] / [I3P Polito] per costruire una componente commerciale di runtime maintenance edge AI. È un layer di prodotto distinto dal contributo accademico della collaborazione (production runtime, deployment data, customer integrations) e non incide sullo scope del joint paper. Voglio segnalartelo prima di proseguire con la sottomissione, così possiamo verificare che il framework IP che concorderemo nel memorandum sia coerente. Felice di una call rapida se utile."*

  Questo è il momento più importante. Trasparenza adesso = problema risolto. Trasparenza dopo paper submission = problema diplomatico.

**Inquadramento per SystemX:** SystemX *non è* un puro mondo accademico. Lavora costantemente con Renault, Valeo, Airbus, Safran, Thales — partner industriali commerciali. Una collaborazione con uno studente che apre una startup post-tesi NON è una cosa anomala per loro. È normale. **Quello che si aspettano è la trasparenza, non l'assenza di interesse commerciale.**

---

## 10 · Scenario: premio in denaro + offerta incubazione al Founder Program di Startup Alliance (Pechino)

Tre scenari da separare nettamente. Trattali in ordine di rischio crescente.

### 10A · Solo premio in denaro, no strings

- Lo prendi. Lo dichiari per tassazione.
- **Verifica tassazione:** sei studente italiano in Cina (visto studente Beihang). I premi cash possono essere tassati in Cina (5-45% scaglioni IRPEF cinesi) e/o in Italia (residenza fiscale). Esistono trattati IT-CN contro doppia imposizione, ma vanno applicati correttamente. **Consulta un commercialista cross-border** (Polito I3P ne suggerisce, o cerca uno con clienti tech IT/CN).
- Lo metti da parte come **runway personale** (non capitale startup ancora, perché non c'è entità) — diventerà capitale al momento dell'incorporazione.

**Azione:** prendi, dichiara, accantona. Zero ulteriori complicazioni.

### 10B · Premio + incubazione "soft" (mentoring, spazio, network, NO equity, NO IP assignment)

- Valuti tranquillamente in base al valore (network cinese? mentor qualificati? accesso a partner industriali?).
- Niente da firmare al volo. Mai pressione.
- Compatibile con tutto il resto (tesi, SystemX, venture builder) — non c'è asset legale in gioco.

**Azione:** valuti su merito, decidi se ti porta valore reale. Default: accetti se gratis e flessibile.

### 10C · Premio + incubazione "hard" (equity, board seat, IP assignment, China-incorporation requirement)

**Regola d'oro: NON firmare nulla sul posto, neanche sotto pressione.**

I veri incubatori ti danno **2-4 settimane** per valutare. Quelli che pressano per firmare in 24-48h sono **red flag** o non sono incubator ma deal-flow capture. Se ti dicono "must sign tonight or offer rescinded", rispondi: *"Voglio prendere il tempo standard per una valutazione informata. Se non è possibile, capisco e declino con gratitudine."* Un buon incubatore rispetta questo. Uno cattivo si rivela.

**Cose specifiche da chiedere/leggere PRIMA di qualsiasi firma:**

| Termine | Cosa cercare | Cosa evitare |
|---|---|---|
| **Equity %** | 5-7% per $25-150K = standard accelerator; 5-10% in incubator cinesi | >10% per <$200K = cattivo deal |
| **Board seat** | Solo equity (non-board) per <10% | Board seat per equity sotto 10% = no |
| **IP assignment** | Licenza non-esclusiva all'incubatore per marketing/promozione, max | "All IP assigned to incubator" o "first refusal on all IP" = no |
| **Geographic requirement** | Flessibilità su sede, full-time relocation negoziabile | "Must incorporate in Beijing within X days" = problema (vedi sotto) |
| **Exclusivity / ROFR sui prossimi round** | None | Right of first refusal su round successivi = lock-in |
| **Tenure di programma** | 3-6 mesi tipicamente | Open-ended o >12 mesi = forma di control non sano |
| **Reporting / control rights** | Standard (monthly reports OK) | Veto power su decisioni operative = no |

**Sul punto China-incorporation specifico:**

Se l'incubator richiede di incorporare in Cina come condizione, **conflitto diretto col tuo positioning "Build in China, sell in Europe"**. Vendere a Valeo, Renault, Airbus, Safran con entità China-domiciled è molto più difficile per:
- **Data sovereignty** (regulator europei diffidano del data flow IT/EU → CN)
- **AI Act compliance** (entità extra-UE deve avere rappresentante UE, e in settori safety-critical la due diligence diventa esponenziale)
- **Geopolitical risk** (industrial customers EU hanno spesso linee guida che escludono o restringono fornitori CN-domiciled)
- **Investor base** (VC EU/US hesitant a investire in entità CN-domiciled deep-tech)

**La struttura corretta per "build CN, sell EU"** è normalmente:
- Holding entity in giurisdizione neutra (Cayman, BVI, o EU)
- Operating entity EU (sales, IP holding, contracting con customer EU)
- Sussidiaria CN (engineering, compute, talento)

Non l'inverso. Se l'incubator chiede l'inverso, valuta molto duramente se il valore aggiunto compensa la frizione commerciale futura.

**Compatibilità con la collaborazione SystemX:**

- Se l'incubator chiede **IP assignment**, conflitto diretto col background IP che porti in SystemX e col foreground IP co-owned.
- **Disclosure obbligatoria** all'incubator del joint paper SystemX. Chiedi conferma scritta che riconoscono e accettano:
  - Background IP esistente di Kevin (tesi, codice repo)
  - Foreground IP co-owned dalla collaborazione SystemX (distributed AAS extension)
- Se l'incubator non accetta questo, è incompatibile.

**Compatibilità con difesa tesi luglio 2026:**

- Se ti chiedono full-time presence immediata (ora a giugno 2026), incompatibile. Non rinunciare a difesa.
- Se accettano part-time fino a luglio + full-time post-difesa, OK.

### 10D · Chi consultare PRIMA di firmare scenario 10C

In ordine di urgenza:

1. **I3P Polito** — negoziano term sheets ogni settimana. Sanno cosa è standard e cosa è capestro. Email/chiamata diretta. Free.
2. **Avvocato cross-border IT/CN tech** — non un generalista. Polito I3P o il venture builder di Milano ti indica un nome.
3. **Yi Li (Beihang co-supervisor)** — ha contesto sull'ecosistema startup cinese che né tu né I3P avete. Una telefonata di 30 min può cambiare la lettura del term sheet.
4. **Persone che hanno fatto il programma negli anni precedenti** — chiedi nomi al programma, scrivi loro su LinkedIn, chiedi onestamente: "Com'è andata? Cosa avresti negoziato diversamente?"

### 10E · Parallel paths: prendere premio ma declinare incubazione

Spesso il vincolo "premio = incubazione" è negoziabile. Puoi:
1. Prendere il premio in denaro (riconoscimento + cash).
2. Declinare l'incubazione (con gratitudine, motivando: "incompatibilità con percorso esistente con [venture builder Milano] / [collaborazione SystemX]").
3. Mantenere il rapporto come network/mentor informale.

Questo è perfettamente accettabile in molti programmi. Chiedi esplicitamente: *"Posso accettare il premio senza accettare l'incubazione?"* Se la risposta è no, sai che il premio è un veicolo per il deal — e lo valuti come deal.

---

## 11 · Cosa ho lasciato fuori

Cose che vanno discusse ma non in questo memo:

- **Patent strategy.** Probabilmente *non* serve patent su DMCA per ora (algorithm-level, weak protection in EU). Patent eventualmente su *implementation-level innovations* del Layer 3 (es. hardware calibration method specifico). Da rivedere con TTO.
- **Trademark AlignEdge.** Da depositare quando incorpori — non ora.
- **Co-founder structure / cap table.** Decisione separata dal venture builder.
- **Polito ownership su tesi-as-IP.** Generalmente le tesi MSc Polito sono dello studente. Ma se hai usato risorse Polito (compute, lab) per parti specifiche, verificare. Documenta cosa è stato fatto su risorse proprie (Modal $0.30) vs Polito.

---

*Da rivedere dopo: (a) la call SystemX di domani, (b) il primo incontro TTO, (c) il kickoff venture builder lunedì, (d) eventuale Founder Program Pechino se si materializza premio/incubazione.*
