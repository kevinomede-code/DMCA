# EdgeNext — Cheat sheet (da rileggere 30 min prima)

## LORO — cosa sapere
- Edge cloud provider (da BaishanCloud + PoP ChinaCache): **1.500+ PoP, 70+ paesi, <30ms**, 90+ Tbps
- Clienti: Microsoft, Sony, TikTok, Audi, iQIYI · assignment programma: espansione N.Africa/SEA/ME
- Offrono: acceleration, security, **edge computing con GPU server + MaaS** (modelli voice/image/chatbot)
- Il loro "edge" = edge cloud (PoP con Xeon + GPU inference classe T4/L4), non device edge
- Pain strutturali: blame asymmetry (modello cliente sfora → colpa loro), onboarding MaaS senza gate
  (analogo Cloudflare = form manuale), eterogeneità flotta, overprovisioning GPU
- **Hanno chiesto loro il deck** → leverage tuo

## IO — cosa avere chiaro
- Vendo UNA cosa: **POC 30 giorni** — 1 modello loro, 1 classe nodo, report alla settimana 4, decisione binaria
- Il mio T4 canonico = esattamente la loro classe hardware (carta tecnica più forte)
- Asset in ordine di profondità: deck → sample report PDF → console v1 → demo v2 live (slider SLA)
- Numeri: 10× coverage gap (Bearing 3_2: 85% vs 9.3%) · TimesFM MAE 0.006 ma 2039ms ·
  drift 92% held-out FAR 0 · $0.30 benchmark · 85% modelli mai in prod · missed $25k vs false $500 (20-100:1) ·
  ~70% progetti edge AI muore in pilot · Google 2026: FM gap ~1000×, "serve shadow deployment" (= mia Stage 5)
- Se citano SageMaker IR / Triton MA: "i due migliori — vendor-locked, one-off, dimensionano istanze/config,
  non selezionano modelli né misurano coverage nel tempo. Voi siete cross-vendor: il layer agnostico non esiste."
- Se citano Riskify: "valuta rischio di un'azienda, io di un modello AI su un chip. Solo la parola 'risk' in comune."
- Onestà pronte: fattori RPi/Orin = stime (solo ×10 T4→Nano è canonico) · demo = distribuzioni ricostruite,
  l'audit vero misura on-device · dominio oggi = time-series (estensione ad altri modelli = lavoro POC)

## DOMANDE — sequenza
**Blocco A · identifica scenario (primi 15 min):**
1. Esclusiva o vendo anche ad altri verticali? → esitazione = C/D, rallenta
2. Contribuite engineering? Come funziona l'IP? → joint IP = B, "prima i miei 90 giorni"
3. Partnership commerciale o discorso investimento? → investimento = D possibile, solo ascolto
4. Timeline per accordo formale? → "settimane" = pressione, "mesi" = comfort A

**Blocco B · scala del pain:**
5. "Come validano i modelli i vostri clienti prima del deploy sui vostri nodi?"
6. "Quando un modello sfora l'SLA in produzione, il ticket arriva a voi o al cliente?"
7. "E nel tempo — traffico che cambia, dati che cambiano — chi se ne accorge?"
8. CHIUSURA: "Scegliete un modello reale e una classe di nodo: 30 giorni, audit pilota, report.
   Se non vi dice niente di nuovo, finisce lì."

## DECISIONI GIÀ PRESE (non rinegoziare in stanza)
- No esclusiva · No joint IP sul motore (adapter sì) · Co-branded prima di white-label
- Dati/telemetria audit = miei (Layer 3), anche nel POC
- POC gratis SOLO con: modello reale + nodo reale + referral scritto se utile
- Qualsiasi carta: "legal review, 10 giorni lavorativi, standard"
- Niente firma oggi, qualunque pressione

## MINIMUM WINS (portane a casa 2 su 3)
1. Design partner status (anche informale via email)
2. Warm intro a 1-2 loro clienti con edge AI pain
3. Follow-up fissato con agenda specifica entro 2-4 settimane

## Dopo il meeting
30 min da solo → domanda chiave: "questa collaborazione mi rende founder più forte o dipendente strategico?"
→ compila log template in friday_briefing.md → follow-up email entro 48h
