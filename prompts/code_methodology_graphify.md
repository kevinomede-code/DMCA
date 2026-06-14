# Task: Cap 2.1 "Research Methodology" — merge `graphify-out/` + protocollo classico esistente

## Contesto generale (leggi tutto prima di iniziare)

Sto scrivendo la tesi DMCA in `thesis_draft.tex`. Il Cap 2 si chiama
"Literature Review" e contiene una subsection 2.1 "Research Methodology"
(label `subsec:research-methodology`). Quel placeholder è già scritto
in modo parziale: descrive un protocollo classico a 3 stadi (broad
search → relevance filter → core extraction) ma usa **numeri vecchi
del knowledge graph** (49 community, 862 nodi, 1246 edge) che non
corrispondono più al graph attuale.

**Obiettivo della subsection finale:** un'unica narrativa che fonda
- la **parte classica** (autoresearch su Semantic Scholar/arXiv del
  2026-04-07, criteri di filtro per gap, struttura della bibliografia
  in cluster `.bib`),
- la **parte graphify** (knowledge graph del codebase+letteratura,
  community structure Leiden, evidenza graph-theoretic della
  novità DMCA come bridge tra Community 1 e Community 8),

con **numeri 100% verificabili** contro le sorgenti. Niente cifre
inventate.

**Grafica:** NON generare figure TikZ/PGFPlots. L'utente metterà a
mano (a) uno screenshot di `graphify-out/graph.html` come "Fig. 2.1
Knowledge graph overview", (b) un draw.io semplice con la funnel
papers come "Fig. 2.2 Corpus assembly funnel". Tu produci solo i
**placeholder LaTeX** con caption pronta e label corretti.

---

## File da leggere PRIMA di scrivere qualunque cosa

1. `graphify-out/GRAPH_REPORT.md` — nodi, edge, community, hyperedges,
   god nodes, surprising connections. **Source of truth per i numeri
   graphify.**
2. `results/paper_log.md` — log dell'autoresearch 2026-04-07: paper
   per gap, score, ruolo (foundamenta / gap-evidence / future).
   **Source of truth per il conteggio papers per gap.**
3. `bibliography/` — 8 file `.bib` (`foundamenta_dt`, `foundamenta_hf_models`,
   `gap1_model_selection` … `gap5_trust_calibration`,
   `cluster_e_mlops`). Conta entry per file.
4. `references_master.bib` — bibliografia consolidata della tesi
   (76 entry al momento). Conta `^@`.
5. `thesis_draft.tex` — leggi solo le righe 316–345 (placeholder
   attuale di 2.1) per capire cosa va sostituito.
6. `CLAUDE.md` — sezione "I 5 Gap della tesi" e regole di
   `graphify`. Non aggiungere paper nuovi a meno che essenziali
   (Bifet 2007 ADWIN, Xia 2024 AAS, Shankar 2022 ops sono già
   nel `.bib`; controlla con `grep ^@.*[bifet|xia|shankar]
   references_master.bib` prima di citarli).

---

## Output atteso (3 file in `outputs/methodology_chapter/`)

### 1. `research_methodology.tex`

Subsection LaTeX standalone, ~350-450 parole, prosa IEEE technical
English, in **terza persona presente narrativo**, NO bullet point.
Struttura interna obbligatoria (in ordine):

**Paragrafo 1 — Inquadramento metodologico (~60 parole).**
Dichiarare che il corpus è stato costruito in due fasi
complementari: (i) ricerca sistematica top-down sui database
accademici, (ii) audit bottom-up tramite un knowledge graph del
codebase e della letteratura allegata, per validare la copertura
e identificare connessioni non ovvie. Posizionare il metodo come
"engineering-grade literature audit", non come revisione
sistematica formale (PRISMA/Kitchenham): la tesi è un artefatto
costruttivo (DSR) e la metodologia bibliografica è strumentale
alla giustificazione dei 5 gap.

**Paragrafo 2 — Stadio 1 (broad search) (~80 parole).**
Riportare: data della query (2026-04-07), database (Semantic
Scholar Graph API v1 + arXiv + IEEE Xplore + ACM DL), 5 assi
keyword corrispondenti ai 5 gap (DT model selection,
TS+LLM orchestration, conversational XAI, industrial validation,
calibrated trust) + 2 assi foundamenta (DT/AAS,
HF time-series models). **Numero papers retrieved**: NON usare
"847". Usa il numero che derivi sommando le righe del
paper_log.md per gap; se il log riporta solo i top-N per gap
(9-10 each), dichiaralo esplicitamente come "78 candidate papers
ranked by Semantic Scholar relevance score, top-10 per axis"
invece di gonfiare a 847.

**Paragrafo 3 — Stadio 2 (relevance filter) (~70 parole).**
Riportare i criteri di filtro: score Semantic Scholar ≥ X (estrai
soglia minima da paper_log), co-occurrence di almeno due assi
gap, full-text disponibile, anno ≥ 2020 (o motivare eccezioni
foundational come Bifet2007ADWIN). Numero che passa il filtro:
estrarlo dai `.bib` cluster (somma `^@` su tutti i file in
`bibliography/` meno duplicati di chiave).

**Paragrafo 4 — Stadio 3 (graph augmentation) (~120 parole).**
Qui è dove il merge graphify entra. Riportare numeri ESATTI da
`GRAPH_REPORT.md`:
- nodi totali (1134), edge totali (1752), community Leiden (73),
  estrazione 84% EXTRACTED / 14% INFERRED
- **god nodes** della top-5: nominare quelli che corrispondono
  a concetti DMCA (Config, ContextType, DigitalTwin,
  ConversationalModel, MultiAgentOrchestrator)
- **Community 1** = blocco MAS / Orchestrator (51 nodi);
  **Community 8** = blocco ADWIN/drift detection (48 nodi).
  Il graph mostra che **non esiste arco diretto** tra le due
  community, e questo motiva la formulazione DMCA come bridge
  closed-loop. Citare come "graph-theoretic evidence of the
  contribution's novelty".
- Hyperedge "Core DMCA Research Gaps" (vedi sezione Hyperedges
  di GRAPH_REPORT.md) come conferma indipendente che la
  partizione in 5 gap della tesi non è ad-hoc ma emerge dalla
  struttura del corpus.

**Paragrafo 5 — Output e ricaduta sui capitoli successivi (~50 parole).**
Concludere: il corpus consolidato in `references_master.bib`
contiene **N entry** (sostituisci N con il valore esatto da
`grep -c "^@" references_master.bib`); le 5 community più dense
diventano le 5 sotto-sezioni 2.2-2.9 del literature review; la
matrice dei 5 gap (Table 2.1, Sec.~\ref{tab:gapmatrix}) sintetizza
la copertura.

**Figure placeholders (in coda, dopo il testo):**
```latex
\begin{figure}[!t]
  \centering
  % TODO Kevin: inserire screenshot da graphify-out/graph.html
  \includegraphics[width=\columnwidth]{figures/graphify_overview.png}
  \caption{Knowledge graph of the thesis corpus (1{,}134 nodes,
    1{,}752 edges, 73 Leiden communities). Node colour encodes
    community membership; node size is proportional to degree.
    The two highlighted clusters --- Community~1 (multi-agent
    orchestration, 51 nodes) and Community~8 (ADWIN and drift
    detection, 48 nodes) --- have no direct edge between them
    in the extracted graph, which is the graph-theoretic
    motivation for the DMCA bridge contribution.}
  \label{fig:graphify-overview}
\end{figure}

\begin{figure}[!t]
  \centering
  % TODO Kevin: draw.io con funnel 78 -> N_filtered -> 76
  \includegraphics[width=\columnwidth]{figures/corpus_funnel.pdf}
  \caption{Corpus assembly funnel. Stage~1 retrieves
    \textit{X}~candidate papers from Semantic Scholar/arXiv across
    seven thematic axes; Stage~2 applies relevance and coverage
    filters reducing the corpus to \textit{Y}~entries; Stage~3
    augments with foundational citations identified by the
    knowledge-graph audit, yielding the \textit{Z}~entries
    consolidated in \texttt{references\_master.bib}.}
  \label{fig:corpus-funnel}
\end{figure}
```
Sostituisci X/Y/Z con i numeri reali estratti.

**Vincoli LaTeX:**
- nessun bullet point, nessun `itemize`/`enumerate`
- usare `\cite{}` solo per chiavi che esistono già in
  `references_master.bib` (verifica con grep prima di scrivere)
- `\ref{}` permessi: `tab:gapmatrix`, `sec:related`, `sec:framework`,
  `sec:methodology`, `subsec:cxai`, `subsec:mlops`,
  `fig:graphify-overview`, `fig:corpus-funnel`
- niente `\input{}` esterni
- nessun pacchetto LaTeX nuovo

---

### 2. `numbers_used.md`

Tabella Markdown con una riga per ogni numero che hai citato in
`research_methodology.tex`. Colonne:

```
| Numero | Dove appare nella subsection | Sorgente file:linea | Valore verificato |
```

Esempio di riga:

```
| 1,134 nodes | Paragrafo 4, frase 1 | graphify-out/GRAPH_REPORT.md:8 | ✓ |
```

Ogni numero della subsection deve avere una riga. Se non riesci a
verificare un numero, **non scriverlo** nella subsection; sostituiscilo
con `\textit{[TBD]}` e segnala la cosa nel summary finale.

---

### 3. `audit_notes.md`

Note brevi (max 1 pagina) su:
- discrepanze trovate tra il placeholder vecchio e i dati reali
  (es: "vecchio testo dice 49 community, graph attuale ha 73 →
  fixed");
- hyperedge graphify che hai usato per conferma del 5-gap framing;
- chiavi `\cite` che il vecchio placeholder NON aveva ma che
  diventano rilevanti dato il knowledge graph (es:
  Bifet2007ADWIN come ponte tra Community 8 e gap 4);
- eventuali numeri che hai dovuto stimare invece di verificare,
  con la giustificazione.

---

## Step di esecuzione (segui in ordine, non saltare)

**STEP 1 — Audit numerico (read-only, niente file di output ancora)**
- conta `^@` in ogni `bibliography/*.bib` e in `references_master.bib`
- estrai da `GRAPH_REPORT.md`: nodi, edge, community, %extracted,
  god nodes top-5, dimensione Community 1 e Community 8, hyperedge
  "Core DMCA Research Gaps"
- da `paper_log.md` estrai: papers per gap, score minimo per gap,
  totale candidati
- riporta i numeri trovati come bullet list nel chat (non come
  file). Aspetta che io confermi prima di andare a STEP 2.

**STEP 2 — Bozza prosa**
- scrivi `outputs/methodology_chapter/research_methodology.tex`
  seguendo la struttura sopra
- mentre scrivi, mantieni un dizionario dei numeri usati per
  generare `numbers_used.md` in parallelo

**STEP 3 — Verifica traceability**
- esegui:
  ```bash
  grep -oP '[0-9]{2,}(?:[,.][0-9]+)*' outputs/methodology_chapter/research_methodology.tex \
    | sort -u
  ```
  e confronta che ogni numero abbia una riga in `numbers_used.md`
- esegui sanity check sulle citazioni:
  ```bash
  grep -oP '\\cite\{[^}]+\}' outputs/methodology_chapter/research_methodology.tex \
    | grep -oP '\{[^}]+\}' | tr -d '{}' | tr ',' '\n' | sort -u \
    | while read k; do grep -q "@.*{$k," references_master.bib \
      && echo "✓ $k" || echo "✗ $k MISSING"; done
  ```
  zero `✗ MISSING` ammessi

**STEP 4 — Audit notes**
- compila `audit_notes.md` con le discrepanze trovate

**STEP 5 — Summary finale**
- un singolo messaggio in chat, max 200 parole, con:
  (a) numeri chiave finali (X/Y/Z corpus funnel, nodi/edge/community
  graphify),
  (b) chiavi `.cite` aggiunte/rimosse rispetto al placeholder vecchio,
  (c) percorso esatto dei 3 file di output,
  (d) eventuali `[TBD]` lasciati nel testo che richiedono il mio
  intervento manuale.

---

## Cosa NON fare

- NON modificare `thesis_draft.tex`. Produci solo i file in
  `outputs/methodology_chapter/`. Io faccio il merge nel draft
  manualmente dopo review.
- NON aggiungere paper nuovi a `references_master.bib` a meno che
  manchino chiavi essenziali per la prosa (Bifet 2007, Leiden
  Traag 2019). Se aggiungi, segnala in `audit_notes.md`.
- NON generare figure TikZ. Solo placeholder `\includegraphics{}`.
- NON usare il numero 847 / 49 community / 862 nodes del placeholder
  vecchio: sono stale. Usa i numeri current.
- NON inventare paper count. Se paper_log.md non ti dà un totale,
  scrivi "78 candidate papers (top-10 per axis × 7 axes + 8
  duplicates removed)" o similare derivabile.
