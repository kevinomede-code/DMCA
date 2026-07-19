# Checklist — Migrazione SLA Jetson Nano: 50 ms → 100 ms

> ⛔ **SUPERATA (17/07/2026).** Decisione finale: **TENERE 50 ms**, NON migrare a 100.
> Motivo: a 100 ms tutti i modelli diventano 1/5 actionable → si perde il contrasto
> "veloce prende / lento manca" (cuore di Case B) e sparisce il −20 s.
> Al posto della migrazione: SLA unificato a 50 ms ovunque + giustificazione OPC-UA/3GPP
> in Stage 1 (§ profili). Questo file resta solo come riferimento storico.

**Data mappa:** 2026-07-17 · **Stato:** ~~DA DECIDERE / DA ESEGUIRE~~ → SUPERATA (tenuto 50 ms)
**File:** `thesis_draft.tex` · **Numeri di riga:** riferiti allo stato del 17/07 (possono slittare di poche righe dopo ogni modifica — verifica sempre col testo, non solo col numero).

---

## ⚠️ Prima di iniziare — leggi questo

1. **Il benchmark canonico NON si tocca.** Misura solo latenza/MAE, non ha SLA dentro. Cambiare l'SLA non lo modifica.
2. **Il re-run SLA=100 + ceiling È GIÀ FATTO.** File: `results/missed_alarm/summary_sla100.json` e `results_sla100_ceil.csv`. **NON rifarlo** — usa questi.
3. **Conseguenza da accettare consapevolmente:** a 100 ms, Moirai-Small passa da "0/5 bearing in tempo, lead −20 s" a "1/5 in tempo, lead +50 s". Il messaggio "modello lento sotto-performa" regge, ma **perdi il numero scenografico del −20 s**.
4. **Perché è coerente:** il Case Study A usa GIÀ SLA=100 ms. Il "50 ms" sparso è colato dal ciclo OPC-UA di Case A (50 ms) confuso con l'SLA. Portare tutto a 100 allinea al Case A.

---

## 🟢 RESTANO 50 ms — NON TOCCARE (è il ciclo OPC-UA di Case A / latenze, non l'SLA)

- [ ] **riga 5379** — "fault window ≈1000 ms (20 OPC-UA cycles at **50 ms**)" → ciclo OPC-UA di Case A. RESTA.
- [ ] **riga 5399** — didascalia figura "scheduling across SLA windows (**50 ms** each)" → legata al ciclo OPC-UA. *Verifica il contesto*; probabilmente RESTA.
- [ ] **riga 4617** — "0.5 s (**50 ms** × 10 for Jetson Nano)" → 50 ms è una latenza d'esempio, non l'SLA. RESTA.

---

## 🔴 DIVENTANO 100 ms — modifica di testo (sono l'SLA del Jetson Nano)

- [ ] **riga 318** — "Moirai-Small on a Jetson Nano edge controller (**50 ms** SLA)"
- [ ] **riga 2785** — "**50 ms** SLA, GPU Maxwell 128 CUDA cores" (profilo Stage 1)
- [ ] **riga 3955** — "**50 ms** Jetson Nano profile, making the selection stage vacuous"
- [ ] **riga 4250** — "correctly excludes models violating the Jetson Nano SLA = **50 ms**"
- [ ] **riga 4594** — "The same Jetson Nano edge profile … (SLA = **50 ms**)" — setup Case Study B / PRONOSTIA
- [ ] **riga 5344** — "on a Jetson Nano with SLA = **50 ms**" — sezione Tangible Effect
- [ ] **riga 5493** — "(SLA = **50 ms**, zero-shot, forecasting task)" — ablation
- [ ] **riga 5499** — "Profile: Jetson Nano, SLA = **50 ms**, zero-shot" — didascalia tabella ablation
- [ ] **riga 5564** — "The ablation above fixes the latency budget at SLA = **50 ms**" — paragrafo sensitivity

### ⚠️ Caso speciale — non basta 50→100
- [ ] **riga 1963** — "real-time alarm thresholds (SLA ≤ **50 ms**) that safety standards impose"
  → **FALSO**: lo standard (3GPP TS 22.104, sensori vibrazione) dice **< 100 ms**, non ≤ 50 ms.
  → Cambia 50→100 **E** correggi l'affermazione + cita lo standard.
  → **NON scrivere "0.5–500 ms"** (viene da fonte secondaria sbagliata).

---

## 🟠 FIGURE con "50 ms" stampato DENTRO l'immagine — didascalia + RIGENERAZIONE

Queste **non si correggono in LaTeX**: la didascalia sì, ma il "50 ms" disegnato nell'immagine va rigenerato dallo **script matplotlib** (lo fai tu, è il tuo codice).

- [ ] **riga 5141** — didascalia "Dashed red line: **50 ms** industrial SLA threshold" + rigenera figura
- [ ] **riga 5194** — didascalia "Green shaded region: SLA-compliant zone (< **50 ms**)" + rigenera figura
- [ ] **riga 5203** — didascalia "SLA = **50 ms** boundary divides admissible…" + rigenera figura
- [ ] (verificare anche la figura del Bearing1_1 se ha "50 ms" disegnato)

---

## ⚪ GIÀ 100 ms o NON-SLA — NON TOCCARE

- Case Study A: righe 4292, 4347 (SLA = 100 ms) → già corretto, è il riferimento.
- Profilo Raspberry/CPU: riga 2787 (100 ms) → suo di default.
- Range cluster di latenza "10–100 ms": righe 212, 5036, 5052, 5138, 5168 → non sono SLA.
- Figura/tabella sensitivity: righe 5582, 5609, 5619 → 100 ms è un punto dello sweep, ok.

---

## 🔢 NUMERI da aggiornare dopo (dal re-run già fatto — `summary_sla100.json`)

- [ ] Lead time PRONOSTIA a **s=1** (Lag-Llama) e **s=6** (Moirai) — sostituire i vecchi a s=2/s=11
- [ ] Nuovo gap empirico su Bearing1_1
- [ ] **Eq. 11**: Δt_max = (2·6 − 1)×10 = **110 s**. Se il gap empirico > 110 s → il bound non lo contiene: scriverlo esplicitamente (vale solo sotto l'ipotesi dichiarata) e spostare il residuo in Limitations. **Non aggiustare a tavolino.**
- [ ] **Tabella 12**: nuovi valori s/c_eff a SLA=100 (togliere la colonna K = ⌊Tarr/ℓ⌋)
- [ ] Aggiornare i due numeri scenografici che cambiano: Moirai lead −20 s → +50 s (Bearing3_2); Bearing1_1 280 s → 350 s (ora actionable)

---

## Ordine consigliato
1. Testo (🔴) — un blocco alla volta, verificando `grep "SLA = 50"` → 0 alla fine.
2. Claim 1963 + ancora normativa.
3. Numeri dal re-run (🔢).
4. Figure (🟠) — rigenerazione matplotlib.
5. Ricompila e rileggi le sezioni PRONOSTIA/ablation per coerenza.

**Verifica finale:** `grep "50\,ms" thesis_draft.tex` deve restituire SOLO le righe 🟢 (5379, 5399, 4617).
