# Call prep — Dr. Abdelhadi Belfadel (IRT SystemX)

**Data call:** 2026-06-26 (domani)
**Contesto:** Allineamento sulla joint collaboration outline `DMCA_joint_collaboration_outline.pdf` del 2026-06-09.
**Scopo dichiarato:** Confermare scope, ruoli, deliverable e timeline della collaborazione su *distributed AAS extension* di DMCA Stage 1.
**Scopo implicito tuo:** Capire (a) il programma quadro sotto cui SystemX inquadra la collaborazione, (b) framework IP, (c) accesso ai partner industriali (Valeo prima di tutti). **NON** dichiarare AlignEdge come entità commerciale ancora — vedi `alignedge/00_IP_strategy_memo.md` §6.

---

## 1 · Chi è Belfadel, in 60 secondi

- **Researcher PhD** all'IRT SystemX, Palaiseau (sede principale Paris-Saclay).
- **Focus:** Information Systems, Ontology Engineering, Software Engineering, AI applicata al Digital Twin industriale.
- **Track record AAS:** lavora attivamente sullo standard IEC 63278 (Asset Administration Shell). Co-autore di **XRTwin4Industry** (framework open-source IRT-SystemX/XRTwin4Industry, GitHub), pubblicato su *Future Generation Computer Systems* (Elsevier).
- **Paper recente da conoscere:** *Advancing Industrial Digital Twins: Towards an Open Platform Aligned with Standards*, Belfadel A., Creff S., Ben Hamida A., PLM 2024 / Springer IFIP AICT vol. 741, 2025. Tesi del paper: non esiste *un* reference architecture per Digital Twin che copra le capabilities industriali — serve una piattaforma aperta allineata agli standard.
- **Background tecnico precedente:** ontology engineering, enterprise architecture-based software discovery, security impact analysis (MITRE ATT&CK), electricity grid ontology.
- **Citation count:** ~94 citazioni (Google Scholar). Profilo solido senior researcher, non senior PI.

**Lettura strategica:** il suo paper 2025 e la sua proposta di *distributed AAS* per la collaborazione sono il *naturale prossimo passo* del suo lavoro. Lui non sta facendo solo un favore — sta cercando *il suo* contributo originale sulla parte distribuita. Il tuo Stage 1 attuale (Type 1 file statico) è il punto di partenza ideale per quel contributo. **Allineamento naturale di incentivi.**

---

## 2 · Chi è IRT SystemX, in 60 secondi

- **Institut de Recherche Technologique** francese, sede Palaiseau (Paris-Saclay).
- **Status:** RTO (Research and Technology Organization) — non università, non aziendalprivata. Pubblico-privato.
- **Partner industriali storici:** Renault, Valeo, Airbus, Safran, Thales, Air Liquide, Atos, Naval Group, Sopra Steria, IRT Saint Exupéry. + CEA, Inria.
- **Programmi principali:**
  - **Confiance.ai** — flagship trustworthy AI program, fondato da France 2030. *Concluso settembre 2024.*
  - **European Trustworthy AI Association** — continuazione europea, lanciata post Confiance.ai.
  - **Industrial and Trustworthy AI Challenge** (con DATAIA / Paris-Saclay) — challenge industriali, es. welding quality detection.
- **Rilevanza per AlignEdge:**
  - Mercato target perfetto (automotive, aerospace, energy = i tuoi vertical).
  - Canale di accesso a Valeo (che è già il tuo first design-partner target via V-Max).
  - Posizionamento perfetto per EU AI Act / trustworthy-AI compliance, che è uno dei tuoi pillar di vendita.

---

## 3 · I 4 partecipanti del joint outline e cosa portano

| Persona | Affiliazione | Ruolo proposto | Cosa porta | Cosa vuole probabilmente |
|---|---|---|---|---|
| **Kevin Omede** | Polito × Beihang | Lead author, executor, DMCA core | Tesi validata, codice, benchmark, drift v3.1.1 | Difesa tesi luglio 2026 + paper pubblicato + porta aperta a SystemX |
| **Prof. A. Simeone** | Polito | Senior supervision IT, framing metodologico, industrial validation context | Affiliazione Polito, network industriale italiano | Pubblicazione di qualità con suo nome, prossimo PhD candidate? |
| **Dr. A. Belfadel** | IRT SystemX | Technical collab, distributed AAS, submodel design, IRT industrial use case | Expertise AAS standards, infrastruttura SystemX, possibile use case industriale | Suo contributo distribuited AAS originale, paper su IEEE TII, possibile estensione progetto SystemX |
| **Prof. N. Anwer** | Paris-Saclay / LURPA | Senior supervision FR, standards positioning, venue access | CIRP membership, ISO TC 213 expert, network venue | Continuazione collaborazione FR-IT, paper su tema standards-aligned |

**Punto cruciale:** **Anwer è probabilmente la chiave per la qualità della pubblicazione e per il venue.** È full prof, CIRP fellow, expert ISO. La sua presenza in autori = paper accettato più facilmente, soprattutto su IEEE TII. Belfadel è il tuo daily collaborator, Anwer è il senior signal.

**Da capire dalla call di domani:** Anwer è davvero on-board o è una proposal di Belfadel ancora da confermare? Fa differenza.

---

## 4 · Lo scope tecnico in chiaro

Quello che Belfadel propone (ripreso letteralmente dall'outline che gli hai mandato):

> *"As AAS follows a distributed architecture, different parts of the AAS-based DT can be deployed across cloud, fog, and edge nodes. We could implement a constraint-driven ML model selection through a multi-criteria selection approach based on specific submodels holding the actual status of each node or device."*

In altre parole, sostituire il tuo **AAS Type 1 statico JSON** (Phase 1 thesis) con **AAS distribuita dinamica** dove:

- I submodel sono *popolati in runtime* con stato di latency, load, memory headroom, drift indicator per ogni nodo cloud/fog/edge.
- Il MCDA (TOPSIS) non è più un calcolo offline, ma diventa **un servizio del DT** che consuma quei submodel.
- Il framework è inquadrato in IEC 63278 (CDV), ISO 23247, ISO/IEC 30173.

**Importante:** questa è una *generalizzazione*, non una sostituzione. La tua tesi Phase 1 single-asset / static AAS resta valida; il joint paper aggiunge il caso multi-nodo / dynamic AAS.

---

## 5 · I 4 atti della call (~30-45 min)

### Atto 1 — Allineamento sociale (3 min)

*Saluti, presentazioni veloci, conferma agenda.*
Tono: rispettoso ma non sottomesso. Lui sa che sei lo studente; tu sai che hai validato empiricamente quello che lui ha proposto in concept paper. Pari livello tecnico, differenza di seniority — comportati di conseguenza.

Frase di apertura:
*"Grazie del tempo. Ho riletto il tuo paper PLM 2024 e la nostra outline. L'idea è che ci allineamo sullo scope tecnico, poi vediamo deliverable e timeline, e chiudo con tre domande aperte. Se serve, ho preparato uno share screen del framework. Va bene?"*

### Atto 2 — Allineamento scope tecnico (12-15 min)

**Da confermare con lui:**

1. **L'estensione Stage 1 è chiara così:** Phase 1 thesis = AAS Type 1 statico; joint paper = AAS distribuita con submodel runtime-populated.
2. **TOPSIS-as-DT-service:** il selettore multi-criteria diventa un servizio esposto sui submodel. *Domanda:* lui ha già qualcosa di prototipale in mente (es. XRTwin4Industry come base infrastruttura)?
3. **Submodel design:** chi disegna lo schema dei nuovi submodel (status, latency, drift indicator)? Tu, lui, joint?
4. **Standards positioning:** IEC 63278 CDV è in evoluzione. La conformità è solo di posizionamento (paper dice "compliant with") o c'è un contributo allo standard stesso (es. proposta di submodel template)?

**Cosa offri tu (gli rendi facile dire sì):**
- Codice DMCA pipeline già funzionante, 10 moduli, testato (`pipeline/aas_parser.py`, `pipeline/topsis_ranker.py`, ecc.).
- Drift detection v3.1.1 con 92% held-out, FAR 0.000 — risultato che dà sostanza al paper.
- Benchmark canonical T4 ($0.30) — dataset riutilizzabile.
- Live demo (`demo/factory_v4.html`) per visualizzare il loop.

### Atto 3 — Deliverable, timeline e role split (10 min)

**Da confermare:**

| Item | Tua proposta | Da chiedere a lui |
|---|---|---|
| Target venue primary | IEEE TII (come da outline) | Conferma o alternativa? *Suggerimento alternativo: IEEE Trans. Automation Science and Engineering* |
| Submission window | Q4 2026 / Q1 2027 | Realistic? |
| Workshop secondary | CIRP-affiliated (suggestion Anwer) | Quale specifico? |
| Phase 2 tertiary | Continuazione opzionale | Da escludere o tenere aperto? |
| First milestone | Confirmation of scope (oggi) | OK |
| Second milestone | Submodel design draft | Quando, chi led? Suggerisco *fine luglio 2026* (post-tesi) |
| Third milestone | Prototype implementation | Suggerisco *settembre-ottobre 2026* |
| Fourth milestone | Paper draft | Suggerisco *novembre 2026* |

**Sulla tua disponibilità:** difesa tesi luglio 2026, poi disponibile full-time fino a [data inizio venture builder = 29 giugno 2026 → quanto dura?]. **Verifica e dichiara timeline realistica.** Non promettere quello che non puoi mantenere.

### Atto 4 — Le 3 domande aperte (8-10 min)

Le tieni in tasca, le tiri fuori una alla volta.

---

#### Q1 — Programma quadro (priorità massima, va chiesta SUBITO)

*"Una domanda di inquadramento prima di proseguire: sotto quale programma o framework SystemX inquadrate questa collaborazione? È nella scia di Confiance.ai, in qualcosa di legato alla European Trustworthy AI Association, o è un'iniziativa research di tuo dipartimento? Te lo chiedo perché può avere implicazioni su pubblicazione, IP e funding che voglio capire da subito."*

**Cosa ascolti:**
- Se dice "Confiance.ai legacy" o "European Trustworthy AI Association" → possibili obblighi France 2030 su open-source / IP. Buono saperlo prima.
- Se dice "iniziativa interna SystemX" → più flessibilità su IP framework.
- Se dice "challenge industriale specifico" (es. con Valeo, Renault, Safran) → c'è già un partner industriale identificato. **Questo è oro.** Apre porta al design-partner channel.

**Follow-up se serve:** *"C'è un industrial partner specifico che SystemX ha in mente per validare l'estensione? Anche solo per orientare il dataset di validazione."*

---

#### Q2 — IRT industrial use case

*"Nell'outline hai indicato 'possible IRT industrial use case (to be discussed)'. È rimasta una buona idea o l'avete chiarito? Te lo chiedo perché un dataset industriale reale, oltre a CMAPSS, sarebbe un valore enorme per la Case Study B della tesi e per il paper congiunto."*

**Cosa ascolti:**
- Se ha un use case identificato → fantastico, chiedi vertical e partner.
- Se nessun use case → pondera tu se vale la pena spingere su un public dataset (PHM Society, IEEE DataPort) o aspettare.
- **Bonus se nomina Valeo, Renault, Safran, Airbus:** porta aperta al design-partner channel di AlignEdge per il post-tesi. Non dichiararlo ora.

---

#### Q3 — IP framework

*"Ultima domanda operativa: avete uno standard IP framework che SystemX usa per le collaborazioni con dottorandi e magistrandi esterni? Voglio essere preparato quando lo presento al TTO del Polito — è una cosa che richiedono sempre e mi rende molto più veloce nei prossimi passi."*

**Perché è formulata così:**
- Inquadra il TTO Polito come *processo standard* tuo, non come segnale di diffidenza verso di lui.
- Inquadra la richiesta come *velocità operativa*, non come negoziazione.
- Lo costringe a darti almeno il nome del documento (es. "convenzione SystemX-università X") che puoi poi cercare/condividere con TTO.

**Cosa ascolti:**
- Se dice "non c'è uno standard, lo facciamo caso per caso" → bandiera arancione. Significa che tutte le clausole saranno negoziate. Aumenta urgenza appuntamento TTO Polito.
- Se nomina un framework (es. "abbiamo template convenzione che ti mando") → eccellente, lo passi al TTO.
- Se evade → richiedi gentilmente: *"Anche solo per orientarmi, c'è qualcuno della parte legal/admin di SystemX a cui far sentire il TTO Polito?"*

---

## 6 · Watch-outs durante la call

### A. Pressione a iniziare prima del contratto

Se Belfadel dice "intanto cominciamo a lavorare, l'admin lo sistemiamo dopo": **No.** Rispondi:
*"Sono d'accordo a fare un kick-off tecnico ma vorrei prima un memorandum minimale di scope e IP prima di committarmi su delivery. Non è sfiducia, è procedura standard che il TTO Polito mi chiederà comunque. Posso farti avere un draft semplice entro la prossima settimana?"*

### B. Allargamento dello scope durante la call

Se durante la conversazione lo scope si allarga ("potremmo anche fare X, e poi anche Y"): **freno cortese**. Rispondi:
*"Interessante. La tengo come parking-lot e ne riparliamo dopo che abbiamo consolidato Stage 1 extension. Voglio evitare di committarmi a deliverable che mettono a rischio la difesa di luglio."*

### C. Pressione a usare infrastruttura SystemX

Se ti chiede di usare il loro repo, server, account: **chiarezza in tempo reale**. *"Se il codice gira su loro infrastruttura, potrebbe diventare loro IP per default."* Risposta:
*"Sì, per la parte distributed AAS in collaborazione possiamo usare la vostra infra; per la parte DMCA core che è già nel mio repo Polito lo tengo lì. Possiamo definirlo nel memorandum?"*

### D. Domanda diretta sui piani commerciali

Se chiede esplicitamente "hai piani di commercializzazione?": vedi `alignedge/00_IP_strategy_memo.md` §6. Risposta:
*"Sto valutando un percorso post-tesi che potrebbe includere componente commerciale, ma non ho ancora struttura legale. Posso aggiornarti dopo aver parlato con il TTO Polito e con l'incubatore I3P. Mi sembra corretto allinearci anche su questo aspetto prima di firmare la collaborazione."*

Non è bugia. È trasparenza con timing.

---

## 7 · Cose da AVERE pronte sullo schermo (share screen all'occorrenza)

- `DMCA_joint_collaboration_outline.pdf` — l'outline che ha già visto
- `thesis_draft.tex` Cap 5.1 e 5.2 — Stage 1 attuale
- `pipeline/aas_parser.py` (se gli chiede di vedere il codice) — non insistere se non lo chiede
- `demo/factory_v4.html` — solo se la conversazione va sul "fammi capire bene cosa hai"
- `results/benchmarks/2026-04-07/benchmark_results_modal.csv` — credibilità empirica

---

## 8 · Checklist 30 min prima

- [ ] PDF outline aperto in tab visibile
- [ ] `thesis_draft.tex` aperto a sezione 5.1
- [ ] Questo file aperto **NON condiviso** (tienilo come gobbo)
- [ ] `alignedge/00_IP_strategy_memo.md` aperto come gobbo IP
- [ ] Microfono e camera testati
- [ ] Bicchiere d'acqua
- [ ] Notifiche off (Slack, email, telefono)
- [ ] Bookmark Researchgate profile Belfadel + Springer paper PLM 2024 (in caso ti chieda di riferimenti specifici)
- [ ] Block di note vuoto pronto per *quotare* quello che dice (vedi prossimo punto)

---

## 9 · Cosa appuntare DURANTE la call

Una pagina di note essenziali, perché poi serve per il TTO e per il memo post-call:

1. **Programma quadro / funding source** (Confiance.ai legacy? Iniziativa interna? Challenge industriale?)
2. **Industrial use case** (c'è? quale? con chi?)
3. **IP framework** (template? caso per caso? Chi è il contatto legal/admin SystemX?)
4. **Anwer status** (confermato? Da contattare? Quando?)
5. **Submission target rivisto** (TII confermato o altra opzione?)
6. **Prossimo milestone concordato** (deliverable + data)
7. **Punti aperti / parking-lot** (cose discusse ma non risolte)
8. **Tone read** — è entusiasta? cauto? sotto pressione per ottenere il commit?

---

## 10 · Dopo la call (entro 24 ore)

1. **Email di follow-up a Belfadel** con riassunto in 5-6 bullet di quello che avete concordato. È quello che il TTO Polito ti chiederà di esibire.
2. **Memo interno** in `systemX/02_call_recap_2026-06-26.md` — versione lunga di quello che hai appuntato.
3. **Email a RIMIN / TTO Polito** richiesta appuntamento, in allegato il joint outline + bullet della call. Obiettivo: appuntamento *entro lunedì 29 giugno*, prima del kickoff venture builder.
4. **Aggiorna `alignedge/00_IP_strategy_memo.md`** §7 checklist con quello che hai imparato.

---

## 11 · Risorse di riferimento (per orientarti, non da citare)

- Belfadel ResearchGate: `https://www.researchgate.net/profile/Abdelhadi-Belfadel`
- Belfadel Google Scholar: `https://scholar.google.com/citations?user=btU0Y3YAAAAJ`
- Belfadel DBLP: `https://dblp.org/pid/214/5413.html`
- *Advancing Industrial Digital Twins* (Belfadel et al. 2025): `https://link.springer.com/chapter/10.1007/978-3-031-93323-3_9`
- XRTwin4Industry GitHub: `https://github.com/IRT-SystemX/XRTwin4Industry`
- XRTwin4Industry paper (FGCS): `https://www.sciencedirect.com/science/article/abs/pii/S0167739X2600110X`
- IRT SystemX Trustworthy AI: `https://www.irt-systemx.fr/en/trustworthy-ai/`
- Confiance.ai program: `https://www.irt-systemx.fr/en/research-programs/confiance-ai/`
- Anwer ResearchGate: `https://www.researchgate.net/profile/Nabil-Anwer`
- Anwer Google Scholar: `https://scholar.google.com/citations?user=cbtZ5MQAAAAJ&hl=fr`
- Polito TTO: `https://www.polito.it/en/innovation/technology-transfer-system`
- I3P incubator: `https://www.i3p.it`

---

*Buona call. Ricorda: lui sta cercando il suo contributo originale tanto quanto tu il tuo. Allineamento di incentivi naturale. Non hai bisogno di vendere, hai bisogno di chiarire.*
