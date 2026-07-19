# Come si validano davvero i modelli prima del deploy — deep research

**Data:** 2026-07-09 · **Scopo:** fondare la discovery question EdgeNext ("come validano i modelli i vostri clienti?") su fatti verificati, non ipotesi. Mappa dello stato dell'arte in 3 livelli + gap analysis.

---

## Livello 1 — Cosa fa il team ML medio (la maggioranza)

Pratica standard documentata (2024-2026):

1. **Eval offline** — accuracy/quality su test set, in cloud, su hardware irrilevante rispetto alla produzione
2. **Shadow deployment** — il candidato gira in parallelo al modello live sugli stessi input, output invisibili agli utenti; misura skew, differenze numeriche, tail latency
3. **Canary rollout** — 1-5% di traffico reale per 24-48h, monitoring, rollback se regressione

Dati di contesto: **~85% dei modelli ML non esce mai dal lab** (QCon SF 2024). La sequenza shadow→canary è considerata best practice *avanzata* — la maggioranza fa solo eval offline + deploy diretto con monitoring.

**Punto chiave per AlignEdge:** shadow e canary sono validazione *in produzione, reattiva, a livello di sistema*. La domanda "questo modello regge l'SLA su questo hardware a questo workload?" non riceve mai risposta *prima* del go-live. Il canary è l'ammissione del gap: scopri i problemi facendoli subire a utenti veri.

## Livello 2 — Il tooling sofisticato che ESISTE (prior art da conoscere)

Due strumenti fanno qualcosa di genuinamente vicino all'audit AlignEdge. Vanno citati con rispetto e posizionati con precisione.

### AWS SageMaker Inference Recommender
- Load test del modello su fino a 10 instance type AWS, traffic pattern custom
- Supporta `ModelLatencyThresholds` (percentile + ms) = SLA dichiarato nel test
- Output: per ogni instance → ModelLatency, MaxInvocations, CostPerInference, CPU/Memory utilization
- **Limiti strutturali:** solo istanze AWS (lock-in), one-off al deploy (no drift, no continuità), nessun concetto di coverage su workload nel tempo, nessun verdict/certificato, zero edge on-prem/device

### NVIDIA Triton Model Analyzer
- Sweep automatico delle configurazioni di serving (batch size, instance group, dynamic batching) su GPU target
- `--latency-budget`: trova la config a throughput massimo dentro il budget di latenza
- **Limiti strutturali:** ottimizza la config di UN modello su UN hardware già scelto (non seleziona il modello), stack NVIDIA (lock-in), one-off, nessun drift, nessuna metrica business

**Lettura competitiva:** entrambi confermano che "hardware profiling contro SLA" è un bisogno riconosciuto dai big. Ed entrambi sono *vendor tool con incentivo al lock-in* — AWS ti dimensiona su istanze AWS, NVIDIA ti ottimizza sul suo stack. Nessuno dei due può essere il decision layer agnostico (la tesi slide 5: "no vendor has incentive to build the agnostic decision layer" — verificata, regge).

## Livello 3 — Cosa fanno le piattaforme edge-cloud MaaS (gli analoghi di EdgeNext)

Analogo occidentale verificato: **Cloudflare Workers AI** (300+ edge location, modelli pre-caricati, "risposte tipicamente <100ms"):
- La piattaforma gestisce provisioning/scaling/latency "automaticamente" — promessa di piattaforma, non certificazione per-modello
- Onboarding di modelli custom privati: **"Custom Requirements Form"** → ti ricontattano. Cioè: processo manuale, opaco, nessun gate di validazione pubblico/documentato
- Nessuna certificazione per-nodo o per-modello pubblicata

Se Cloudflare — molto più grande e più software-mature di EdgeNext — gestisce l'onboarding di modelli custom con un form manuale, la probabilità che EdgeNext abbia un gate di validazione per-nodo sistematico è bassa. La discovery question ha ottime chance di colpire il vuoto.

## Gap analysis — la matrice

| Capacità | Eval offline | Shadow/Canary | SageMaker IR | Triton MA | **AlignEdge audit** |
|---|---|---|---|---|---|
| Misura latenza su HW target | ✗ | in prod | ✓ (solo AWS) | ✓ (solo NVIDIA) | ✓ cross-vendor |
| Prima del go-live | ✓ (solo accuracy) | ✗ | ✓ | ✓ | ✓ |
| SLA coverage su workload | ✗ | parziale, reattiva | parziale (soglie) | parziale (budget) | ✓ KPI centrale |
| Confronto/selezione tra modelli | ✗ | A/B a valle | ✗ (istanze, non modelli) | ✗ (config, non modelli) | ✓ TOPSIS |
| Drift / continuità nel tempo | ✗ | ✗ | ✗ | ✗ | ✓ DMCA loop |
| Mappa su costo business (missed alarm) | ✗ | ✗ | ✗ (costo infra sì) | ✗ | ✓ |
| Artefatto certificabile (AI Act) | ✗ | ✗ | ✗ | ✗ | ✓ report |
| Fleet eterogenea multi-nodo | ✗ | ✗ | ✗ | ✗ | ✓ (roadmap) |

## Implicazioni per venerdì

1. **La risposta più probabile di EdgeNext** è Livello 1 ("i clienti testano per conto loro / facciamo load test") o un form manuale alla Cloudflare. Il gate sistematico per-nodo quasi certamente non esiste.
2. **Se un tecnico cita SageMaker IR o Triton MA:** "esatto, sono i due migliori — e sono la prova che il bisogno è reale. Uno funziona solo su AWS, l'altro solo su stack NVIDIA, entrambi one-off. Voi siete cross-vendor per costruzione e i vostri clienti hanno bisogno di continuità. Quel decision layer agnostico e continuo non esiste — è quello che costruisco."
3. **Il numero da usare:** ~85% dei modelli non arriva in produzione; di quelli che arrivano, la validazione hardware è affidata a canary = utenti reali come test bench.
4. **Aggiornamento matrice competitiva (deck slide 7):** SageMaker IR e Triton MA entrano nel quadrante bottom-right (hardware-aware, non coverage/drift-aware) accanto a TensorRT/OpenVINO. Non serve modificare il deck (locked), ma tienili pronti in Q&A.

## Fonti

- [SageMaker Inference Recommender — docs](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-recommender.html) · [custom load test](https://docs.aws.amazon.com/sagemaker/latest/dg/inference-recommender-load-test.html) · [AWS blog](https://aws.amazon.com/blogs/machine-learning/improved-ml-model-deployment-using-amazon-sagemaker-inference-recommender/)
- [Triton Model Analyzer — docs](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/model_analyzer/README.html) · [GitHub](https://github.com/triton-inference-server/model_analyzer) · [NVIDIA blog](https://developer.nvidia.com/blog/identifying-the-best-ai-model-serving-configurations-at-scale-with-triton-model-analyzer/)
- [Shadow/canary patterns](https://www.marktechpost.com/2026/03/21/safely-deploying-ml-models-to-production-four-controlled-strategies-a-b-canary-interleaved-shadow-testing/) · [LLM rollout 2026](https://tianpan.co/blog/2026-04-09-llm-gradual-rollout-shadow-canary-ab-testing/) · [Galileo MLOps](https://galileo.ai/blog/mlops-operationalizing-machine-learning)
- [Cloudflare Workers AI](https://www.cloudflare.com/products/workers-ai/) · [docs](https://developers.cloudflare.com/workers-ai/)
