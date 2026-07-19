# Riskify — Deep Verification vs AlignEdge

**Data verifica:** 2026-07-09
**Metodo:** fetch diretto riskify.net (homepage + documentation API completa), riskify.ai (homepage completa), web search mirata su "Riskify model risk / AI model monitoring".
**Verdict anticipato: ZERO overlap reale.** L'overlap suggerito ("in una piccola parte fa qualcosa di simile") è puramente lessicale.

---

## Attenzione: sono DUE aziende diverse

| | riskify.net | riskify.ai |
|---|---|---|
| Cosa fa | API di **non-financial risk intelligence** su aziende (entità societarie) | Marketplace **riassicurativo** su blockchain (catastrofi naturali, ILS) |
| Cliente | Team compliance / due diligence / GRC | (Ri)assicuratori, broker, ILS manager |
| Prodotto | 2 endpoint REST: `create_scan_company_task` / `get_scan_company_result` — scansiona un'azienda e restituisce profilo rischio | Tokenizzazione del rischio catastrofale, pool, AMM, smart contract (mainnet previsto 2028) |
| C'entra con modelli AI deployati? | **No** | **No** |

Chiunque abbia detto "fa qualcosa di simile" ha quasi certamente visto riskify.net.

---

## riskify.net — cosa fa esattamente (da API docs, verificato)

Input: **un'azienda** (nome/LinkedIn ID). Output: profilo JSON con 6 dimensioni di rischio:

1. **News & Media** — articoli taggati (lawsuit, layoff, sanzioni...) con sentiment ±1
2. **Employees** — turnover, tenure media, cambi di leadership (fonte LinkedIn)
3. **ESG** — certificazioni possedute sì/no
4. **Cybersecurity** — standard ISO posseduti, traffico web, variazione staff IT
5. **Regulatory** — presenza in sanction list
6. **Operational** — disastri naturali e guerre nella regione dell'azienda

L'"AI" nel loro pitch è **interna al loro pipeline** (classificazione news, NER, sentiment). Non monitorano, non valutano, non testano **modelli AI del cliente**. Non esiste alcun modulo "model risk", "model monitoring", "drift", "edge", "hardware" in tutta la documentazione API (verificata integralmente: ogni data structure è su entità societarie).

## Feature comparison

| Feature | Riskify (.net) | AlignEdge |
|---|---|---|
| Oggetto analizzato | Azienda (entità legale) | Modello AI su hardware edge |
| Rischio misurato | Reputazionale/ESG/sanzioni | Missed alarm da SLA coverage + drift |
| Dati di input | News, LinkedIn, sanction list | Latenze misurate, dati sensore cliente |
| On-hardware | No (cloud API) | Sì (Jetson/RPi, cuore del prodotto) |
| Drift detection | No | DMCA-Drift v3.1.1 (92% held-out, FAR 0) |
| Coverage SLA | No | KPI centrale |
| Verticale | Compliance/procurement | Industria 4.0 / PdM |

**Overlap reale: 0 feature su 7.** L'unico punto di contatto: entrambi vendono "AI-powered risk monitoring via API" come *frase di marketing*. Un buyer distratto può confonderli; un buyer tecnico no.

---

## Il competitor adjacent REALE (emerso dalla verifica)

Lo spazio "AI model risk management" esiste ma è presidiato da altri, tutti cloud-side e governance-oriented:

- **Yields.io** — model risk management / validazione per banche; workflow di governance, non misure on-hardware
- **IBM watsonx.governance / Watson Studio MRM** — fairness, quality, drift monitoring cloud
- **Citrusx** — risk assessment framework per modelli AI

Nessuno misura coverage SLA su hardware edge reale. Restano nel quadrante top-left della matrice competitiva (slide 7: coverage/drift-aware ma NON hardware-aware). La matrice del deck resta valida senza modifiche.

## Positioning takeaway (per venerdì EdgeNext)

1. Se qualcuno cita Riskify: *"Riskify valuta il rischio di un'azienda — noi il rischio di un modello AI su un chip. Condividiamo solo la parola 'risk'."* Una frase, chiuso.
2. Il rischio competitivo vero non è Riskify: è che un player MLOps observability (Arize/Fiddler/WhyLabs) o un chip vendor scenda verso l'edge coverage. Preparata risposta in Fase 5 brainstorm (punto 2 del brief).
3. Nessuna modifica necessaria a deck v3 (locked) né alla matrice 2×2.

## Fonti

- [riskify.net homepage](https://www.riskify.net/) · [API documentation](https://www.riskify.net/documentation) (fetch integrale 2026-07-09)
- [riskify.ai homepage](https://www.riskify.ai/) (fetch integrale 2026-07-09)
- Adjacent: [Yields.io](https://www.yields.io/) · [IBM Watson Studio MRM](https://www.ibm.com/products/watson-studio/model-risk-management) · [Citrusx](https://www.citrusx.ai/post/11-commonly-used-risk-assessment-models-for-ai)
