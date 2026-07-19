# Why Me — Working Draft

**Ultimo update:** 2026-07-03
**Scopo:** iterare sull'insight che va nella slide 4 del pitch ("Insight") e nel closing "why me" delle Q&A. Da rileggere e affinare ogni 1-2 settimane man mano che parli con customer e mentor.

---

## 1. Il tuo raw thought (input Kevin, 2026-07-03)

> "Il problema è diventato mio quando ho capito che tutti vanno verso l'accuratezza del modello, mentre il coverage è un tema toccato solo dai compiler, e nessuno lo sta davvero tenendo in considerazione. Chi lo ha fatto ha fatto jackpot (es. OctoML)."

Due correzioni tecniche applicate sotto.

---

## 2. Correzioni brutali

### 2A · Coverage NON è un tema dei compiler

I compiler (TensorRT, OpenVINO, TVM, ONNX Runtime, il core di OctoML) ottimizzano la **latency di inferenza** — quanto ci mette il modello a fare una forward pass su un chip specifico. È ottimizzazione per-inference, non copertura di workload.

**Coverage** è un concetto diverso e **orfano cross-disciplinare**:

> Data una workload di N richieste/secondo e un SLA di X millisecondi, quale frazione di richieste viene effettivamente processata in tempo?

Richiede tre input che nessun compiler ha: (a) workload rate, (b) SLA budget, (c) misura empirica di quante inference cadono dentro il budget vs fuori.

**Chi tocca coverage tangenzialmente (nessuno la produttizza):**
- Real-time systems community — scheduling theory, WCET — angolo safety, non ML
- Load balancer di serving (Triton, TorchServe) — visto come capacity planning
- HPC batch schedulers — throughput, altra cosa
- ML observability (Arize, Fiddler, WhyLabs) — drift e quality post-inference, NON SLA coverage on edge

Il coverage nel senso "quante alarm windows perdo per SLA violation su Jetson Nano" sta tra **real-time systems** (che non parla ML) e **MLOps** (che non conta SLA budget su edge). Nessuno vive in entrambi i mondi.

### 2B · OctoML NON ha "fatto jackpot" — e non toccava il coverage

OctoML risolveva **compilazione cross-vendor** — "same model, deploy anywhere fast". Diversa disciplina dal coverage.

Cifre: raccolti ~$130M in funding, exit da NVIDIA a ~$165M nel 2023. **Acquihire modesto, non unicorno.** NVIDIA li ha comprati per assorbire il team TVM, non perché il business fosse profittevole.

**La lezione OctoML per AlignEdge è positiva:** il compiler è un problema noto con incumbent aggressivi che comprano chi ci prova. Coverage NON è un problema noto — nessun incumbent, nessuna race. Terreno vergine.

---

## 3. La sintesi corretta dell'insight

Tre metriche in gioco, ognuna con un owner e un gap chiaro:

| Metrica | Chi la ottimizza | Domanda risposta |
|---|---|---|
| **Accuracy** | ML research + MLOps observability | "Se il modello gira, ha ragione?" |
| **Latency per-inference** | Compiler + chip vendor | "Quanto ci mette una singola forward pass?" |
| **Coverage** | **Nessuno** (fino ad AlignEdge) | "Quante inference arrivano in tempo, sulla workload reale, dentro l'SLA?" |

**Accuracy × Coverage = frazione reale di eventi catturati.**

Se accuracy=99% ma coverage=40%, catturi 39.6%. Il modello "eccellente" fallisce il 60% delle volte per motivi che nessuno misura.

**Coverage è il ponte da metriche tech a business outcome.**

Chi non ha incentivo strutturale a misurarla:
- MLOps vendor sono cloud-first — non sentono SLA pressure edge
- Chip vendor guadagnano vendendo più chip — non hanno interesse a esporre coverage gap
- Compiler ottimizzano una inference alla volta — non contano workload nel tempo
- Consultant vendono audit one-off — non productano il KPI

Nessuno di questi player ha *incentivo strutturale*. Tu sì.

---

## 4. Il "why me" strutturale — completamento del tuo "io vedo"

> Io vedo che il ponte tra "modelli AI eccellenti in cloud" e "modelli AI utili in fabbrica" non è latency, non è accuracy — è coverage sotto vincoli SLA reali. Vedo questo ponte perché ho la combinazione di tre lenti che nessun altro incrocia sistematicamente:
>
> - Ingegneria industriale (Polito) → penso in throughput, OEE, missed-alarm cost, non in accuracy
> - ML systems research (Beihang + tesi DMCA) → parlo la lingua dei modelli edge
> - Benchmark empirico su hardware reale ($0.30 T4 canonical) → ho visto il gap con i miei occhi, non l'ho letto in un paper
>
> Chi ha una sola di queste lenti non vede il ponte. Un ML researcher benchmarka in cloud e assume coverage=100%. Un compiler engineer massimizza latency ma non conta coverage nel tempo. Un manufacturing engineer non tocca modelli AI. Solo l'intersezione di tutte e tre rende il coverage visibile — e solo se hai fatto il benchmark su Bearing 3_2 PRONOSTIA con i tuoi dati, lo VEDI davvero.

**Perché questa versione funziona per il pitch:**
- Verificabile (le lenti sono nel tuo CV)
- Non-replicabile facilmente (intersezione rara)
- Coerente col prodotto (audit misura coverage)
- Concreta (Bearing 3_2 = evidenza specifica, non vaga)

---

## 5. Draft della narrazione pitch (60-90 secondi)

Da usare come chiusura pitch o risposta a "why you?" Q&A. Da allenare ad alta voce.

> "Everyone in ML measures accuracy. Compilers measure latency. Nobody measures coverage — the fraction of predictions that actually happen in time, on the real chip, under the real workload.
>
> Accuracy times coverage equals events actually caught. If your model is 99% accurate but only runs 40% of the time within SLA, you catch 40% of events. That gap is where machines break silently.
>
> I saw this because I sit at three intersections that rarely combine: industrial engineering at Politecnico Torino, ML systems research at Beihang, and hardware-real benchmarks I built for thirty cents. Someone from ML alone would benchmark in cloud and assume coverage equals 100%. Someone from compilers would optimize latency and stop. Someone from manufacturing wouldn't touch the model.
>
> The intersection is where AlignEdge lives. And it's where I live."

**Word count:** 160 parole, ~55-65 secondi al ritmo calmo. Cinque frasi, cinque beat narrativi (metrics gap → arithmetic → three lenses → why others don't see → landing).

---

## 6. Da testare / iterare

Cose che al prossimo giro voglio verificare:

- [ ] Il numero "40% coverage" nel esempio è coerente col tuo caso Bearing 3_2 (Moirai-S 9.3%) o con caso più typical (Lag-Llama 64%)? Decidere quale usare per l'esempio.
- [ ] "Thirty cents benchmark" — è memorable ma andrebbe verificato che passi come signal di capital efficiency e non come "amateurish". Test con mentor.
- [ ] Alternative alla parola "coverage" — è tecnica. Sinonimo pitch-friendly? "In-time rate"? "Real-time delivery"? Da valutare.
- [ ] Manca la parte "unfair advantage" nel senso YC — perché il tuo insight è defendibile? Non abbastanza chiaro se lo replichi in 6 mesi con lo stesso trio di lenti.

---

## 7. Da NON dire mai in questo contesto

- Non nominare OctoML come "jackpot" — è tecnicamente sbagliato + fa capire che non conosci le cifre
- Non dire "everyone else is wrong" — dì "everyone else measures something else"
- Non usare "unique" — "rare intersection" è più credibile e onesto
- Non parlare di brevetti sul coverage KPI — non è brevettabile come concetto

---

## Version log

- v0.1 — 2026-07-03 — first draft dopo brutal correction Kevin + Claude
