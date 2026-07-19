# Cover email per Simeone — pre-call SystemX 2026-06-26

**A:** [email Simeone]
**Oggetto:** Scheletro paper IJAMT v0.3 — pre-call SystemX di oggi

---

Caro Professore,

allego scheletro v0.3 in inglese del paper congiunto per IJAMT, da rivedere prima della call con Belfadel di oggi pomeriggio.

**Decisioni chiave:**

- **Titolo (Opzione A):** *Digital-Twin-Driven Adaptive Model Selection and Drift Recovery for Predictive Maintenance in Smart Manufacturing*
- **4 autori:** io (lead), tu (senior IT + manufacturing framing), Yi Li (DT), Belfadel (distributed AAS). Anwer fuori scope (super impegnato per sua comunicazione).
- **Riposizionamento manufacturing** ancorato su PM bearing + economics Aberdeen/Senseye 2024 + standard ISO 10816.

**Risultati simulazione eseguita oggi (REAL DATA):**

- **PRONOSTIA** (6 bearing, 7625 acquisizioni reali): ratio alarm density **10.4** cross-bearing. **Bearing 3_2 = caso safety-critical empirico**: PatchTST actionable a 390s pre-failure, Moirai-S non-actionable a 190s. Dimostra Stage 2 admissibility su dato manifatturiero.
- **IMS Center** (NASA, 5.3 giorni industriale): ratio **11.6** coerente cross-dataset. Cross-regime validation completata.
- Il 10× è una *conservative estimate* (assumiamo ideal accuracy, il gap reale è ≥10).

**Novità importante nello scheletro v0.3:**

§6 design Phase 2 — **full DMCA lifecycle loop su scenario bearing-replacement**. Quello che ho dimostrato oggi è Stage 2 (admissibility) puro. Il **valore unico di DMCA è il loop adaptive**: monitor → alarm → manutenzione fisica → hot model swap → bearing nuovo → re-selezione modello. Questo è il contributo originale principale del joint paper, da costruire post-tesi insieme a Belfadel (~5 giorni lavoro). Include un'estensione semantica del classifier v3.1.1 per distinguere *degradation drift* (no swap, alarm fisico) da *context-shift drift* (swap modello), che è una novità metodologica forte.

**Per la call di oggi:**

Porto lo scheletro come baseline allineata Polito-side. Domando a Belfadel: conferma §6 distributed AAS come suo perimetro, conferma Phase 2 lifecycle loop come deliverable joint, eventuale Case Study C industriale via partner SystemX (Valeo / Renault / Safran).

**Cosa ti chiedo:**

Rapida lettura entro [orario] e segnalazione di eventuali punti su cui vuoi fermarmi. Se non sento entro [orario], procedo con la v0.3.

**Allegati:**

1. `paper_design_v0.3.docx` — scheletro completo (inglese, sharing-ready)
2. `fig_Bearing3_2.png` — figura killer PRONOSTIA (safety-critical actionable flip)
3. `fig_IMS_Bearing1.png` — figura validazione cross-regime industriale
4. `results.csv` + `results_ims.csv` — numeri completi simulazione

Grazie,
Kevin
