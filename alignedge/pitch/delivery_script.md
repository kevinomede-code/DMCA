# AlignEdge Pitch — Delivery Script

**Version:** v3 (post-visualization + LOCK-IN + Slide 7 revision)
**Target duration:** 6:20 with 6 key pauses
**Audience:** Beijing Founder Program 2026 · ~90% Chinese investors, mentors, partners
**Language:** English

---

## Format

- **SAY** = verbatim script (memorize)
- **[pause Ns]** = intentional silence markers
- **Emphasis** = words to hit
- **AVOID** = what NOT to say

---

## SLIDE 1 — Cover · 15s

> *"I'm Kevin. I built AlignEdge — the runtime maintenance layer for edge AI. The right-sized AI model, on the right chip, at the right time."*

[Pause 2s. Look up. Advance.]

**AVOID:** "Nice to be here" filler · personal bio (they read it)

---

## SLIDE 2 — Problem · 40s

> *"Here's the problem.*
>
> *Factories deploy AI models to catch failures before they happen. On the factory chip — a Jetson, an ARM, an edge processor — most of these models silently break in production.*
>
> *They miss alarms. Nobody notices for three to six months.*
>
> *In automotive, one hour of downtime costs 2.3 million dollars.*
>
> [Pause 2s]
>
> *The missed alarms are invisible because the cloud never sees SLA-violating requests. They just don't exist in monitoring."*

**Emphasis:** "silently break" · "**2.3 million dollars per hour**" · "invisible"

**AVOID:** explaining SLA · long failure-mode list

---

## SLIDE 3 — Solution · 45s (dashboard slide)

> *"AlignEdge tests your AI on real edge hardware — then keeps it working.*
>
> [Gesture toward dashboard on screen]
>
> *What you're looking at is our simulator running on real NASA turbofan data on a Jetson Nano. Five sensor stations, live drift monitoring, five-stage pipeline running underneath.*
>
> *Three steps operationally. You send us your model, your data sample, your hardware spec, your latency budget. We test it — real hardware profiling, drift injection across five failure modes, coverage against your SLA, multi-criteria comparison against eight benchmarked foundation models. You get a 15-page report in four weeks. Keep, optimize, or swap. AI Act-aligned audit trail.*
>
> *This is not a slide of what we plan to build. Live demo available on request."*

[Pause 2s after "live demo available on request"]

**Emphasis:** "real edge hardware" · "four weeks" · "live demo available on request"

**Delivery tip:** hand gesture toward dashboard, hold 3 seconds. Don't look at slide.

---

## SLIDE 4 — Insight · 60s ⭐ CRITICAL

> *"Here's the insight nobody talks about.*
>
> *Everyone in ML measures accuracy. Everyone in compilers measures latency. Nobody measures coverage — the fraction of predictions that actually arrive within the SLA.*
>
> *Look at this bearing.*
>
> [Point to chart]
>
> *Public dataset. Same task. Same hardware — Jetson Nano. Same 50-millisecond SLA.*
>
> *PatchTST: 85 percent coverage. Lag-Llama: 64 percent. Moirai-S: 9.3 percent.*
>
> *Same task, different models — ten-times gap in coverage.*
>
> [Pause 3s — let math sink]
>
> *The math is simple. 99 percent accuracy times 40 percent coverage equals 60 percent of alarms missed.*
>
> *Coverage is where machines break silently."*

**Emphasis:** "nobody measures coverage" · "**10× gap**" · "**60% missed**"

---

## SLIDE 5 — Why Now · 45s

> *"Three converging shifts open a 24-month window.*
>
> *First — mandatory compliance. EU AI Act starts high-risk enforcement August 2026. Industrial AI needs documented drift monitoring. Penalties: 3 percent of global turnover, or 15 million euros.*
>
> *Second — foundation model explosion. HuggingFace grew to 2.4 million models. The second million took only 335 days. Manual model selection for edge is impossible.*
>
> *Third — closed ecosystems. Vendor lock-in is now structural. Every chip vendor locks you in — NVIDIA CUDA, Qualcomm QNN, Intel oneAPI. No vendor has incentive to build the agnostic decision layer."*

**Emphasis:** "August 2026" · "2.4 million" · "**locks you in**" · "**agnostic decision layer**"

---

## SLIDE 6 — Business Model · 30s

> *"Three products, in sequence.*
>
> *Audit — the wedge. On-hardware validation. Our first market entry.*
>
> *Runtime — the core. Continuous drift detection plus automatic swap. Enterprise subscription.*
>
> *Optimization — the platform. Fleet-wide cross-vendor orchestration. Platform-scale integration.*
>
> *Land, expand, deepen. Same customer, growing footprint over time."*

**Emphasis:** "wedge" · "core" · "platform" · "growing footprint"

---

## SLIDE 7 — Competition · 40s

> *"The competitive landscape.*
>
> *ML observability — Arize, Fiddler, WhyLabs — top-left. Cloud-side, no HW context.*
>
> *Consulting audits — Big Four, boutique — bottom-left. Manual, one-off, not scalable.*
>
> *Compiler benchmarks — TensorRT, OpenVINO, MLPerf — bottom-right. Hardware-optimized, no drift.*
>
> *AlignEdge — top-right.*
>
> [Pause 2s]
>
> *Three reasons no one else can catch up.*
>
> *One — cross-vendor by design. No chip vendor will cannibalize their own lock-in.*
>
> *Two — productized audit measuring SLA coverage on your hardware, with your data.*
>
> *Three — a dataset that compounds. Every audit adds proprietary customer × model × hardware × drift data no competitor can replicate."*

**Emphasis:** "top-right" · "**cannibalize their own lock-in**" · "**compounds**"

---

## SLIDE 8 — China · 30s

> *"A few words on China.*
>
> *We're founded here — in Chaoyang, Beijing.*
>
> *75 percent of the world's EVs are produced in China. The global automotive electronics market is 318 billion dollars. Asia Pacific is 43.6 percent of that.*
>
> *This is the largest edge AI deployment testbed on Earth."*

**Emphasis:** "founded here" · "**75 percent**" · "**largest edge AI testbed**"

---

## SLIDE 9 — Team + Traction · 25s (compressed)

> *"I'm Kevin. Dual master's — Industrial Engineering at Politecnico Torino, Business Administration at UIC Barcelona. Visiting Researcher at Beihang.*
>
> *Validated: drift classifier 92 percent accuracy, zero false alarms. Eight foundation models benchmarked for 30 cents. Ten-times coverage gap on public bearing data.*
>
> *Selection to this program is our current traction."*

**Emphasis:** "**92 percent**" · "**zero false alarms**" · "**30 cents**" · "**10×**"

---

## SLIDE 10 — Vision · 30s

> *"Where we're going.*
>
> *Every industrial AI model, always in its optimal deployment state.*
>
> *AI-on-edge becomes a maintained asset, not a one-shot deployment. By 2030: millions of models continuously maintained. Hundreds of billions of dollars in industrial downtime prevented.*
>
> *The Haiku-not-Opus moment for industrial AI.*
>
> *Thank you."*

[Pause 2s before "Thank you"]
[Silence 3s after "Thank you" — don't fill]

---

## 6 pause chiave (NON saltarle)

1. After **$2.3M** (Slide 2) — 2s
2. After dashboard gesture (Slide 3) — 3s
3. After **10× gap** (Slide 4) — 3s
4. After **top-right quadrant** (Slide 7) — 2s
5. After **75%** (Slide 8) — 2s
6. After **Haiku-not-Opus** (Slide 10) — 2s before Thank you

---

## Timing breakdown

| Slide | Duration | Cumulative |
|---|---|---|
| 1 Cover | 15s | 0:15 |
| 2 Problem | 40s | 0:55 |
| 3 Solution | 45s | 1:40 |
| 4 Insight | 60s | 2:40 |
| 5 Why Now | 45s | 3:25 |
| 6 Business | 30s | 3:55 |
| 7 Competition | 40s | 4:35 |
| 8 China | 30s | 5:05 |
| 9 Team | 25s | 5:30 |
| 10 Vision | 30s | 6:00 |

With pauses: ~6:20. Well within 5-7 min program window.

---

## Version log

- v1 (2026-07-05): initial 6:20 script
- v2: added dashboard gesture Slide 3
- v3 (current): LOCK-IN anchor Slide 5, Slide 6 "Our first market entry", Slide 7 "3 reasons no one else can catch up"
