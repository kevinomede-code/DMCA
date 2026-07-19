# Call prof — 30 min — gobbo personale

> Tieni APERTI prima di entrare: tesi PDF · `factory_v4.html` (Play una volta per testare) · questo file.
> Lui guida, io seguo. Demo prima, PDF dopo, domande in chiusura.

---

## Atto 1 — Riallineamento (2 min)

Apertura, una frase:
*"Ti faccio vedere a che punto sono. Parto dal demo che dà l'idea visiva del framework, poi entriamo nei punti che mi interessa che tu veda. Ho 3 domande mirate alla fine."*

Non rifare l'introduzione accademica — la sa.

---

## Atto 2 — Demo live (4 min)

1. Apri `factory_v4.html` → scenario **"Nano · GRADUAL (canonical, no-swap)"** → **Play**.
2. Mentre gira, una riga sola: *"questo rigioca la traccia reale del cycle canonico, sensore S2 di CMAPSS FD001, detection a t=1380 con soglia ADWIN 1.99"*.
3. Quando ADWIN scatta e il drawer si apre da solo → *"qui vedi le 8 feature e la regola dell'albero v3.1.1 che ha fatto match"*.
4. Clicca tessera **Stage 5** → mostri il controfattuale TimesFM (2039ms = 2.5% finestre servite). *"Il colpo centrale della discipline of selection."*
5. **Stop dopo 4 min anche se lui chiede approfondimenti** — gli dici "ne parliamo nel walkthrough della tesi". Il demo è un'esca, non l'evento.

---

## Atto 3 — Walkthrough PDF (18 min)

Salti mirati. Apri il PDF, vai alle pagine sotto. PDF page = thesis page **+1** (offset cover/abstract).

| Quando | Sezione | Thesis p. | PDF p. | Cosa dire (~30 sec/punto) |
|---|---|---|---|---|
| 0-2 min | **1.4 Contributions** | 9 | 10 | "Qui ho i 4 contributi nuovi. Il principale è il loop closed-loop con re-allineamento, gli altri sono il classificatore drift, la conversational XAI e il framework di validazione." |
| 2-4 min | **2.11 Literature Gap Matrix** | 23 | 24 | "Qui faccio vedere come DMCA copre i 5 gap che ho identificato nella literature review. Tabella di compare-and-contrast con i lavori esistenti." |
| 4-7 min | **5.1 Framework Architecture** | 36 | 37 | "Overview del loop a 5 stage. Le frecce mostrano il dato che passa da uno all'altro. La novità è che è *closed-loop*: Stage 5 aggiorna l'AAS che rialimenta Stage 1." |
| 7-11 min | **4.5 + 5.5 Drift classifier v3.1.1** | 33, 40 | 34, 41 | "Questo è il pezzo intellettualmente più denso. Le 4 design decisions DD-05/06/09/10 sono l'evoluzione iterativa dell'albero. Sezione 5.5.1 spiega ADWIN teorico (Bifet 2007, δ=0.002). Tengo il 92% held-out come prova che non ho overfittato sui seed di calibrazione." |
| 11-13 min | **7.5 SLA Violation Effect** | 52 | 53 | "Qui c'è il numero che caratterizza tutto: TimesFM ha MAE 0.006 ma latenza 2039ms = 40.8× lo SLA Nano. Un selettore task-only lo deploierebbe; DMCA lo esclude per vincolo. È il *raison d'être* del framework." |
| 13-16 min | **8.1 Case Study CMAPSS end-to-end** | 53-56 | 54-57 | "Validazione end-to-end del cycle completo sul CMAPSS. Tutti e 5 gli stage girano davvero. Risultato canonico in `results/drift_experiments/drift_cycle_results.json`." |
| 16-17 min | **10.3 Limitations** | 59 | 60 | "Quello che NON ho fatto: BaSyx vero (uso Type 1 file), Phase 2 streaming, validazione su dataset industriale reale (8.2 è Future Work)." |
| 17-18 min | **10.1 Conclusions** | 58 | 59 | Una frase di chiusura, niente di più. |

**Regola d'oro**: se lui interrompe, *lascialo parlare e prendi nota*. Le sue interruzioni sono la call. Non difendere il testo, ascolta.

---

## Atto 4 — Le 3 domande mirate (6 min)

Arrivare con domande specifiche segnala maturità e ti orienta. Chiedi a lui, una per volta:

**Q1 — Validazione drift sufficiente?**
*"Il classificatore di drift è calibrato su 5 tipi × 3 seed e validato su 5 × 5 held-out al 92%. Pensi che basti come evidenza per la tesi, o vuoi che ampli con un sesto tipo (DISTRIBUTION_SHIFT) e più seed?"*

**Q2 — Surrogati nello Stage 3 e 5A da dichiarare o sostituire?**
*"Il workflow W5 usa un modello Ridge surrogato nello Stage 3 e un fattore di miglioramento surrogato nello Stage 5A invece di inferenza reale. Sono coerenti con l'approccio Phase 1. Preferisci che li dichiari nei Limitations o vuoi che mi muova verso inferenza vera prima della consegna?"*

**Q3 — Case study B (8.2)?**
*"La Case Study B è marcata Future Work. Una sola case study (CMAPSS A) ti basta per la consegna, o pensi che convenga aggiungerne una seconda? E nel caso, hai un suggerimento di dataset industriale che potrei usare?"*

Le tre domande in totale dovrebbero portare via 5-6 min se lui risponde sintetico. Se va più lungo, va benissimo — è il segnale che le domande erano buone.

---

## Checklist pre-call (5 min prima)

- [ ] Tesi PDF aperto, vai a pagina 1 con CMD+G / Vai-a-pagina
- [ ] `factory_v4.html` aperto in browser, scenario `nano_gradual` selezionato, **NON** in Play
- [ ] Questo file aperto in una finestra di scratch (non condivisa)
- [ ] Audio testato, condivisione schermo provata su un'altra finestra
- [ ] Bicchiere d'acqua, niente notifiche

**Se vai in panico**: torna al demo. Cliccare Play su `factory_v4` è sempre una buona uscita.

---

## Cosa NON fare

- Non leggere il PDF capitolo per capitolo — *salta* alle pagine sopra.
- Non difendere ogni scelta — se ti chiede "perché X?" e non hai la risposta a portata di mano, di' "è una buona osservazione, devo controllare e te la mando dopo". Onestà > improvvisazione.
- Non aprire il codice (`pipeline/*.py`). Se vuole vederlo, lui lo chiede.
- Non mostrare gli smoke test / README / scaffolding GitHub. È infrastruttura, non contenuto della tesi.
