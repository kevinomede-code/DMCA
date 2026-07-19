# Next Session Brief — AlignEdge Technical Deep-Dive

**Purpose:** hand-off prompt per la prossima sessione Claude. Da copiare interamente all'inizio della chat successiva.

---

## PROMPT DA COPIARE (inizio)

```
Sono Kevin Omede, sto costruendo AlignEdge — startup che offre audit
on-hardware per modelli AI edge industriali. Framework tecnico chiamato
DMCA (Dynamic Model-Context Alignment), 5-stage closed-loop, validato
nella mia tesi Polito × UIC × Beihang.

Nella sessione precedente ho finalizzato deck v3, pitch script,
Q&A prep, briefing per meeting EdgeNext (venerdì). Ora shift completo:
da modalità sales/pitch a modalità technical research + product build.

## Mission di questa sessione

Voglio approfondire in modo RIGOROSO il technical space AI Edge in cui
mi sto muovendo. Meno tempo su "come vendere", più tempo su:
- Cosa dice la letteratura recente su edge AI deployment challenges
- Dove sta esattamente il mio contributo tecnico originale
- Cosa fa Riskify (mi è stato detto che "in una piccola parte" fa
  qualcosa simile — voglio verificare esattamente cosa)
- Che gap tecnici mancano per portare il framework research-grade a
  product-grade

## Contesto necessario — leggere PRIMA di procedere

Leggi questi file in ordine, in profondità:

1. `C:/Users/011ke/Desktop/thesis-research/CLAUDE.md`
   → contesto tesi, decisioni architetturali DMCA, dati canonici

2. `C:/Users/011ke/Desktop/thesis-research/alignedge/README.md`
   → mappa cartella startup, stato attuale

3. `C:/Users/011ke/Desktop/thesis-research/alignedge/00_IP_strategy_memo.md`
   → strategia IP 3-layer (importante: framework è Layer 1 pubblico)

4. `C:/Users/011ke/Desktop/thesis-research/alignedge/why_me/00_working_draft.md`
   → l'insight coverage > accuracy che voglio approfondire

5. `C:/Users/011ke/Desktop/thesis-research/alignedge/pitch/content_skeleton.md`
   → il framing tecnico corrente del prodotto

6. `C:/Users/011ke/Desktop/thesis-research/graphify-out/GRAPH_REPORT.md`
   → knowledge graph strutturato della literature tesi

7. `C:/Users/011ke/Desktop/thesis-research/AutoResearchClaw/README.md`
   → skill per literature search automation

## Pipeline di lavoro

### Fase 1 · Literature landscape (60-90 min)

Usa AutoResearchClaw skill + graphify knowledge graph per costruire
literature landscape rigoroso su:

- **Edge AI deployment challenges 2024-2026**: bandwidth constraints,
  fleet fragility, cross-vendor optimization, model drift on-device
- **Coverage-driven metrics vs accuracy-only**: c'è literature che
  distingue coverage rate da accuracy? Chi ha pubblicato su questo?
- **Multi-model orchestration edge**: MLC AI, Modular, MLOps observability
  on edge — chi c'è, cosa pubblicano
- **AI Act compliance layer emerging**: quali paper/reports 2025-2026
  discutono strumenti per compliance industriale
- **Missed-alarm cascade in industrial PdM**: literature specifica?

Interroga graphify per papers già ingested. Estendi con literature-search
skill per papers 2025-2026 non ancora ingestiti.

**Deliverable Fase 1**: `alignedge/research/literature_landscape.md`
- 20-30 paper chiave con 1-line insight ciascuno
- 3-5 gap identificati dove AlignEdge contribuisce
- Citation graph delle key papers

### Fase 2 · Riskify deep verification (30-45 min)

Mi è stato detto che Riskify (riskify.net) "in una piccola parte" fa
qualcosa simile ad AlignEdge. Nella sessione precedente ho fatto un check
superficiale — hanno detto essere non-financial risk intelligence (news,
ESG, cyber). Ora voglio verifica RIGOROSA:

- Vai su riskify.net, riskify.ai
- Cerca prodotti/moduli specifici che toccano AI model risk
- Cerca API docs, product pages, technical docs
- Se hanno un "AI model monitoring" o "model risk assessment" component,
  documenta esattamente cosa fa
- Confronta feature-by-feature con AlignEdge audit

**Deliverable Fase 2**: `alignedge/research/riskify_comparison.md`
- Tabella feature comparison (Riskify component X vs AlignEdge audit)
- Verdict: overlap reale, overlap superficiale, o zero overlap
- Se overlap reale: come positioning differ

### Fase 3 · Technical contribution formalization (60 min)

Con literature landscape + Riskify verification, formalizza:

- Cosa esattamente è NUOVO nel mio contributo (drift classifier v3.1.1,
  coverage measurement on real HW, cross-vendor decision layer, missed-alarm
  cascade simulation)
- Cosa è well-known e sto solo applicando (ADWIN, TOPSIS, ISO 26262)
- Cosa è in ricerca open dove potrei collaborare con academic partners

**Deliverable Fase 3**: `alignedge/research/technical_contribution.md`
- Novelty statement chiaro
- Prior art table
- Research collaboration opportunities

### Fase 4 · Product engineering setup (2 ore)

Costruisci la struttura del monorepo `alignedge-product`:

- Repo GitHub privato (mi guiderai nel setup se serve)
- Monorepo: Python (audit harness) + TypeScript (eventual dashboard/landing)
- Struttura suggerita:
  ```
  alignedge-product/
  ├── packages/
  │   ├── audit-core/          # Python — framework wrappers
  │   ├── audit-cli/           # Python — orchestrator
  │   ├── audit-report/        # Python — report generation
  │   ├── landing/             # TypeScript — Netlify landing
  │   └── simulator-demo/      # TS/Python — dashboard live
  ├── data/
  │   └── canonical/           # copia canonical benchmark/drift results
  ├── docs/
  │   ├── customer_input_spec.md
  │   ├── audit_playbook.md
  │   └── report_template.md
  └── README.md
  ```
- Genera skeleton di ogni packages/ con README + package.json/pyproject.toml
- Genera `customer_input_spec.md` v0 (1 pagina, cosa il customer manda)
- Genera `audit_playbook.md` v0 (le 5 fasi audit già discusse)

**Deliverable Fase 4**: struttura repo creata + template docs iniziali

### Fase 5 · Brainstorming aperto (30-45 min, alla fine)

Argomenti su cui voglio ragionare LIBERAMENTE (senza doc formale, chat mode):

1. **Coverage > accuracy come tesi accademica**: ha senso pubblicare un
   working paper su questo? Su quale journal/conference (NeurIPS Applied,
   MLSys, IEEE TII)? Chi sono i reviewer che potrebbero apprezzare?

2. **Riskify come possibile competitor futuro**: se pivotano verso AI
   model monitoring, quanto veloce potrebbero arrivare al nostro spazio?
   Vale la pena avere una risposta preparata pre-emptive?

3. **AutoResearchClaw come tool interno AlignEdge**: la skill di
   literature search automatizzata potrebbe diventare un feature del
   nostro audit report ("le vostre model choices contro state-of-the-art
   2026")? O è overkill?

4. **Startup Alliance program help — cosa chiedere concretamente**: legal
   review NDA + scope letter, sicuro. Ma anche office space? Introductions
   ai loro portfolio company AI? Grant / funding non-dilutive attraverso
   il programma?

5. **EdgeNext meeting venerdì — refine dopo research**: se la literature
   revela che c'è forte pain sul deployment fragility cross-vendor negli
   edge cloud (che è esattamente il business EdgeNext), la conversazione
   di venerdì si arma tecnicamente. Come impacchettarla?

## Constraint operativi

- **Tempo**: 60 giorni full-time da adesso. Ma questa sessione ha budget
  ~4-5 ore focus.
- **Budget**: ~€150 totali next 60 giorni (dominio alignedge.com, Netlify
  free, GitHub private free, Modal ~€30). Niente hardware acquistato ora
  — profiling via Qualcomm AI Hub free tier.
- **Help disponibile**: Startup Alliance (legal, mentors, potentially
  intros). Yi Li (Beihang) per academic questions. Simeone (Polito)
  per thesis/paper.
- **Priorità immediata**: Fase 1 e 2 (literature + Riskify) sono time-
  sensitive perché servono per calibrare pitch venerdì EdgeNext.
- **Priorità Sprint 1 subito dopo**: Fase 4 (repo setup + skeleton)
  perché il product build parte lì.

## Cosa NON fare in questa sessione

- Non tornare su sales/positioning/deck copy (deck v3 è locked)
- Non riscrivere IP memo (è consolidato)
- Non ri-discutere "solo founder vs co-founder" (Kevin ha deciso: cerca
  commercial co-founder Q4 2026, solo build fino ad allora)
- Non ri-discutere naming (alignedge.com si compra ora, rebrand eventuale
  post-EdgeNext deal)

## Come procedere

Inizia leggendo i 7 file listati in "Contesto necessario". Poi conferma
di aver capito lo stato attuale con un summary in 5-6 righe. Poi parti
con Fase 1 (literature landscape via AutoResearchClaw + graphify).

Se ti mancano dettagli operativi che il briefing non ha coperto, fammi
domande specifiche prima di procedere. Non partire cieco.

Grazie. Andiamo.
```

## PROMPT DA COPIARE (fine)

---

## Note per Kevin — come usare questo prompt

**Quando usarlo**: all'inizio della prossima chat che apri (nuovo file/sessione).

**Come usarlo**: copia interamente il blocco tra "PROMPT DA COPIARE (inizio)"
e "PROMPT DA COPIARE (fine)". Inseriscilo come primo messaggio.

**Cosa aspettarti dal prossimo Claude**:
- Prima cosa: legge i 7 file di contesto
- Seconda: fa un summary per confermare comprensione
- Terza: parte con Fase 1 (literature landscape)
- Se serve, ti fa domande operative prima di procedere

## Deliverable expected dalla prossima sessione

Al termine dei ~4-5 ore, dovresti avere:

1. `alignedge/research/literature_landscape.md` — mappa strutturata
2. `alignedge/research/riskify_comparison.md` — verdict overlap
3. `alignedge/research/technical_contribution.md` — novelty statement
4. Struttura repo `alignedge-product` creata
5. Template `customer_input_spec.md` + `audit_playbook.md` v0
6. Brainstorm notes su 5 argomenti aperti (Coverage as paper, Riskify future,
   AutoResearchClaw internal use, Startup Alliance asks, EdgeNext refined)

## Pre-requisiti da verificare prima di avviare la prossima sessione

- [ ] Verifica che `thesis-research/AutoResearchClaw/` sia funzionante
      (skill discovery non broken)
- [ ] Verifica che `thesis-research/graphify-out/GRAPH_REPORT.md` esista
      e sia leggibile
- [ ] Se possibile, compra alignedge.com **prima** della prossima sessione
      (10 min via Namecheap/Cloudflare). Costo $12-15. Toglie un decision
      point strategico dalla sessione tecnica.
- [ ] Genera GitHub PAT (personal access token) o autorizza gh CLI —
      per creare repo alignedge-product privato durante Fase 4

## Version log

- 2026-07-05: initial handoff brief creato dopo sessione deck v3
