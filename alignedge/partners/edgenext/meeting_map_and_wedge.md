# EdgeNext — Mappa domande→decisioni · Pain→Soluzione · Wedge 30 giorni

**Data:** 2026-07-09 (pre-meeting venerdì) · Complementa `friday_briefing.md` (scenari A-D, red flags, minimum wins — restano validi)
**Fondazioni:** `research/model_validation_practices.md` · `research/literature_landscape.md` · `research/riskify_comparison.md`

---

## 1 · Pipeline domande → decisioni

Sequenza operativa. Ogni blocco: domanda → cosa rivela la risposta → decisione che prendi in tempo reale.

### Blocco A — Identificazione scenario (primi 10-15 min, dal briefing)

```
Q1 "Esclusiva o posso vendere ad altri verticali?"
   ├─ non-esclusiva OK ────────────→ scenario A vivo → prosegui
   └─ esitazione/esclusiva ────────→ C/D → DECISIONE: nessun impegno oggi, frase optionality (§briefing)

Q2 "Contribuite engineering? Come funziona l'IP?"
   ├─ no engineering ──────────────→ A puro
   └─ sì + joint IP ───────────────→ B → DECISIONE: "prima 90 giorni miei, poi strutturiamo"

Q3 "Partnership commerciale o discorso investimento?"
   └─ investimento menzionato ─────→ D possibile → DECISIONE: solo ascolto, zero numeri oggi

Q4 "Timeline ideale per accordo formale?"
   ├─ "settimane" ─────────────────→ B/C pressure → rallenta
   └─ "mesi, esploriamo" ──────────→ A comfort → accelera sul POC
```

### Blocco B — Scala del pain (la parte nuova, dopo identificazione)

```
Q5 "Come validano i modelli i vostri clienti prima del deploy sui vostri nodi?"
   ├─ "testano loro / non so" ─────→ piattaforma cieca → vai a Q6 (chi paga)
   ├─ "staging/load test" ─────────→ Q5b "Su quale classe di nodo? Uno solo?"
   │                                  → buco eterogeneità 1.500 PoP → vai a Q7
   ├─ "canary" ────────────────────→ "quindi lo scoprite in produzione, con utenti veri"
   │                                  → riframe: audit = scoperta PRIMA del go-live → Q7
   └─ "SageMaker IR / Triton MA" ──→ risposta pronta: "i due migliori, vendor-locked,
                                      one-off. Voi siete cross-vendor. Il layer agnostico
                                      e continuo non esiste — lo costruisco io."

Q6 "Quando un modello sfora l'SLA in produzione, il ticket arriva a voi o al cliente?"
   → li porta a nominare il costo che assorbono LORO (blame asymmetry)

Q7 "Cosa succede nel tempo — traffico che cambia, dati che cambiano?"
   → apre il drift senza forzare → semina il runtime (EXPAND) senza venderlo oggi

Q8 (chiusura) "Scegliete un modello reale di un vostro cliente MaaS e una classe
   di nodo. Ci faccio un audit pilota in 30 giorni col mio protocollo."
   → converte qualsiasi risposta precedente nel wedge
```

### Decisioni pre-prese (non rinegoziare in stanza)

| Situazione | Decisione già presa |
|---|---|
| Chiedono esclusiva | No. Frase optionality del briefing |
| Chiedono joint IP sul motore | No. Adapter di integrazione sì, `audit-core`/drift/metodologia no |
| Chiedono white label | Co-branded di default; white label solo per volumi garantiti |
| Telemetria/dati degli audit | Restano AlignEdge (Layer 3) — nero su bianco anche nel POC |
| Pressione a firmare | "Legal review, 10 giorni lavorativi, standard" |
| POC gratis o pagato? | Gratis SOLO se: modello reale + nodo reale + referral scritto se il report è utile. Altrimenti pilot fee simbolica |

---

## 2 · Pain → Soluzione (mappa completa)

| # | Pain EdgeNext | Evidenza | Componente AlignEdge | Cosa dici in stanza |
|---|---|---|---|---|
| P1 | **Blame asymmetry**: modello del cliente sfora → il cliente incolpa la piattaforma "<30ms" | Struttura MaaS; Q6 glielo fa dire | Audit pre-go-live con verdict per-modello | "Ogni modello mal dimensionato erode la vostra promessa di latenza senza che sia colpa vostra" |
| P2 | **Onboarding opaco**: modelli custom accettati senza gate (analogo Cloudflare = form manuale) | `model_validation_practices.md` §3 | Audit come gate di onboarding MaaS | "Cloudflare onboarda con un form. Voi potete onboardare con un certificato" |
| P3 | **Eterogeneità flotta**: 1.500 PoP, generazioni HW diverse → stesso modello, coverage diversa per nodo | Struttura PoP, acquisizione ChinaCache | Coverage per-nodo; roadmap fleet (DEEPEN) | "Lo stesso modello su Singapore e Johannesburg non ha la stessa coverage. Chi lo dice al cliente?" |
| P4 | **Overprovisioning difensivo**: non sapendo cosa regge, si compra GPU in eccesso | Economia edge: no elasticità locale | Verdict OPTIMIZE (quantizza) / SWAP (modello più piccolo) | "Ogni modello right-sized è margine GPU recuperato su 1.500 siti" |
| P5 | **Support cost**: SRE loro che debugga modelli altrui | Q6 | Report self-contained: il debug l'ha già fatto l'audit | "Il ticket 'è lento' arriva già risolto: keep, optimize o swap, con i numeri" |
| P6 | **Drift silenzioso**: modello OK al deploy, degrada nel tempo, nessuno guarda | Google 2026: FM "frozen", serve shadow deployment | Runtime DMCA (Stage 4+5) — fase 2, non oggi | Semina con Q7, non vendere. "Il certificato ha una data di scadenza — il runtime la rinnova" |
| P7 | **Compliance clienti EU**: AI Act logging/post-market per deployment high-risk | AI Act ago 2026 (⚠ verifica categoria) | Audit trail AI Act-aligned nel report | Solo se emergono clienti EU/industriali. Non aprire tu |

Numeri pronti: 85% dei modelli mai in produzione (QCon 2024) · FM throughput gap ~1000× (Google 2026) · missed failure $25k vs false alarm $500, 20:1-100:1 (arXiv 2512.01149) · 10× coverage gap stesso task stessi dati (tuo, Bearing 3_2) · ~70% progetti edge AI muore in pilot.

---

## 3 · Wedge a 30 giorni (il POC — l'unica cosa da vendere venerdì)

**Principio:** venerdì non vendi l'audit, non vendi il runtime, non firmi partnership. Vendi UNA cosa: il pilota a 30 giorni. Tutto il resto è conseguenza del report.

### Struttura (mappa il playbook 5 fasi su 4 settimane)

```
Settimana 0 (questa)  → scope letter 1 pagina: 1 modello, 1 classe nodo, 1 SLA, criteri
                        di successo, proprietà dati audit = AlignEdge, NDA standard
Settimana 1  → Fase 1-2: intake (customer_input_spec) + profiling on-node
               [serve da loro: accesso a 1 nodo PoP o specs esatte + modello + sample dati]
Settimana 2  → Fase 3: drift injection (5 failure mode) + quality gate
Settimana 3  → Fase 4: coverage vs SLA + confronto candidati (quantizzato/distillato/size)
Settimana 4  → Fase 5: report 15 pagine + debrief call → PROPOSTA: channel agreement
```

### Cosa chiedi a loro (poco, di proposito)
1. Un modello reale di un cliente MaaS (o loro interno se il cliente è sensibile)
2. Accesso a una classe di nodo (anche solo specs esatte + istanza equivalente — il mio T4 canonico è già classe giusta)
3. Un contatto tecnico per 2 call da 30 min (kickoff + debrief)

### Criteri di successo del POC (dichiarali nella scope letter)
- Report consegnato entro 30 giorni con coverage % misurata e verdict motivato
- Almeno 1 finding actionable (config, quantizzazione o swap) con impatto quantificato
- Decisione binaria al debrief: channel agreement sì/no entro 2 settimane

### Costo per te (budget check)
Compute: nodo loro (gratis) o Modal ~€10-20. Tempo: compatibile coi 60 giorni. Rischio principale: modello fuori dal dominio TS → harness extension (Sprint 2) — accettato, è lavoro pagato in distribuzione.

### Kill criteria (onestà con te stesso)
- Se al debrief chiedono un secondo POC gratis senza agreement → non è un buyer, è ricerca gratis
- Se durante il POC spingono joint IP sul motore → stop, frase legal review
- Se il modello che propongono richiede >2 settimane di harness extension → riscopa il POC su un modello più vicino, non sforare i 30 giorni

---

## 4 · Il one-liner di chiusura

> "Non vi chiedo di credermi. Vi chiedo un modello e un nodo: in 30 giorni vi mostro
> quanta coverage state promettendo senza saperlo. Se il report non vi dice niente
> che non sapevate, ci stringiamo la mano e finisce lì."
