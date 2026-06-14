# DMCA × Hongdian — Pilot Proposal and Case Study (v1, draft)

> **Document purpose.** A working proposal to discuss with Hongdian
> Corporation (Shenzhen) the integration of the **Dynamic Model-Context
> Alignment (DMCA)** framework — developed within the master's thesis at
> Politecnico di Torino × Beihang — into the Hongdian Edge AI product line.
> This document is based exclusively on public information about Hongdian
> and on the canonical experimental data of the DMCA project. Sections 7
> and 8 are intentionally left as placeholders to be co-authored with
> Hongdian after the first technical conversation.
>
> **Author:** Kevin Omede · **Affiliation:** Politecnico di Torino /
> Beihang University, M.Sc. thesis on DMCA · **Version:** v1 · **Date:** 2026-04-28
> **Confidentiality:** SHARED-DRAFT — pre-NDA. No proprietary Hongdian or
> third-party data is contained.

---

## Executive Summary

Industrial AI projects fail at a documented 76.4% rate in manufacturing
(RAND/Gartner 2025), and 91% of ML models that do reach production degrade
silently over time (Vela et al., *Scientific Reports* 2022). The economic
cost of these failures is no longer hypothetical: Zillow's Offers division
recorded over $500 million in write-downs in 2021 because a deployed model
continued to produce predictions while the underlying data distribution
shifted, and the organization had no structural mechanism to detect or
react to that shift.

Hongdian Corporation has built one of the most credible hardware platforms
for industrial edge AI in China — including the Smart3000 Edge AI Box
(Rockchip RK3588), the X2 Industrial Computing Gateway, and the H-series
4G/5G cellular routers — and is actively expanding into AI-enabled
predictive maintenance, smart power distribution, and industrial robotics.

The DMCA framework provides what existing industrial AI platforms (Siemens
Senseye, GE Predix, IBM Maximo) systematically lack: an **adaptive,
Digital-Twin-driven model lifecycle layer** that selects, deploys,
monitors, and re-aligns time-series and forecasting models on edge devices
based on changing operational constraints. DMCA reads the asset profile
in standardized AAS format (IEC 63278-1), ranks candidate Hugging Face
models against deployment constraints (latency, RAM, accuracy, license)
using TOPSIS, monitors live sensor streams for drift using a 7-feature
v3 detector, and proposes model swaps through a conversational copilot
that keeps a human operator in the loop.

This document proposes a **3-to-6 month joint pilot** between Hongdian and
the DMCA research team, anchored on a single representative customer in
the smart power distribution segment, with a clear set of measurable KPIs
(detection latency, false alarm rate, MAE containment under drift,
operator override rate) and an explicit go/no-go decision point at the
end of the pilot.

---

## 1. Why Hongdian, Why Now

Hongdian, founded in 1997 in Shenzhen, has historically been a hardware
specialist for M2M and IoT connectivity. Over the last 24 months, the
company has executed a credible transition into the edge-AI segment with
three flagship product moves:

- **Smart3000 Edge AI Box.** A Rockchip RK3588-based edge device with a
  6 TOPS NPU, 16-channel 1080p video analytics, support for over 300
  industrial protocols, and explicit support for hosting AI models — the
  Hongdian engineering blog has publicly demonstrated the deployment of
  a DeepSeek model on the Smart3000.
- **X2 Industrial Computing Gateway with Wedora management platform.**
  Used in industrial robot and precision-machine monitoring with a
  predictive maintenance posture: real-time sensor data is compared to
  historical normal-operation profiles to anticipate failures.
- **H-series 4G/5G cellular gateways** (H6131, H8951, H8959, H8871).
  The connectivity backbone Hongdian deploys to thousands of customers
  in industrial automation, grid & energy, gas station safety, retail,
  and self-service.

This trajectory — hardware-first, then AI-enabled, with an installed base
of customers across regulated industrial verticals — is exactly the
profile that can absorb a software lifecycle layer. **What Hongdian
currently does not provide its customers is a way to manage the lifecycle
of the AI models that run on the gateways it sells.** Once a model is
deployed on a Smart3000 or X2, no integrated mechanism exists to:

- Verify that the model remains the best fit when the customer's
  operational context changes (new equipment, new process, new sensor
  supplier, seasonal load patterns, energy mix changes);
- Detect model degradation in production based on residuals and
  distribution shifts;
- Re-rank and propose alternative models from the open Hugging Face catalog
  given updated constraints;
- Maintain an audit trail of model decisions for safety and regulatory
  reviews.

DMCA fills exactly this gap. **Strategically, integrating DMCA does not
ask Hongdian to compete with vertical AI platforms — it gives Hongdian a
horizontal differentiator that no competitor in the industrial gateway
market currently offers**, and creates a path to recurring software
revenue on top of hardware sales.

## 2. The Pain Point, with Numbers

The pain DMCA addresses is documented at three converging levels:

**Industry-wide failure rate.** Manufacturing reports a 76.4% AI project
failure rate, the highest of any sector (RAND/Gartner 2025). Only 33-48%
of AI proofs-of-concept reach production; the average prototype-to-
production transition takes 8 months; 46% of POCs are scrapped before
production; 58% of project resources are consumed by OT/IT integration
rather than ML modeling.

**Model staleness in production.** Vela et al. (2022, *Scientific Reports*
12:11654, DOI 10.1038/s41598-022-15245-z) experimentally demonstrated
that 91% of (model, dataset) pairs degrade over time across 128 cases in
healthcare, transportation, finance, and weather. Critically, the authors
showed that data drift alone does not explain the degradation —
**temporal model decay is a distinct phenomenon that requires its own
detection and re-alignment mechanism**, not just input monitoring.

**Catastrophic single-incident cost.** The 2021 Zillow Offers shutdown is
the cleanest publicly documented case of model decay leading to direct
financial loss: $304M in Q3 losses, over $500M in total write-downs,
closure of an entire business unit, and a 25% workforce reduction. The
mechanism was exactly the one DMCA addresses: a deployed neural-network
pricing model continued to produce confident predictions while the
underlying market structure shifted, and the organizational layer that
should have caught the discrepancy had been actively disabled.

**Implication for Hongdian's customers.** Hongdian sells gateways into
electrical utilities, manufacturing plants, and industrial automation
customers. These customers are the precise target population of the
above statistics: their AI deployments fail silently, their operational
context changes regularly (energy mix, process changes, equipment
replacement), and they currently do not have access to a lifecycle
management layer that can be run on the very edge gateways they have
already purchased.

## 3. Target Segment: Smart Power Distribution

Of Hongdian's publicly disclosed verticals, smart power distribution
emerges as the strongest first-pilot candidate for four reasons:

1. **Pain density.** A medium-voltage transformer that fails undetected
   typically incurs €50k-€200k in downtime, repair, and load-rerouting
   costs; a high-voltage substation incident is materially larger. The
   per-unit value of preventing a single missed detection is high enough
   to justify a software subscription.
2. **Drift is structural, not exceptional.** Smart power distribution
   experiences continuous distributional shifts: the renewable energy
   transition is changing intermittency patterns, electric-vehicle
   charging is reshaping load curves, data-center co-location creates
   new flat-baseline customers, and seasonal extremes (peak summer
   cooling load) are themselves drifting.
3. **Regulatory pressure aligns with audit requirements.** State Grid
   Corporation of China and provincial utilities increasingly require
   traceability for asset-condition decisions. DMCA's append-only
   audit trail and explicit confidence calibration map naturally onto
   these requirements.
4. **Dataset alignment.** The DMCA project's secondary canonical dataset
   is **ETT-h1 (Electrical Transformer Temperature)**, originally
   curated for forecasting transformer thermal load. The framework's
   benchmarks therefore transfer directly, without needing a synthetic
   adapter.

Hongdian already markets gateway products into smart power distribution
rooms — the same hardware that would host DMCA-orchestrated models in
this pilot.

## 4. Hardware Mapping: Hongdian Gateway → DMCA AAS Profile

The DMCA framework uses three reference Asset Administration Shell
profiles (IEC 63278-1 conformant) to model the deployment-target
constraints. The mapping to Hongdian's product line is direct:

| DMCA AAS profile | Equivalent Hongdian product | Suggested deployment tier |
|---|---|---|
| `raspberry_pi_4` (ARM, 2 GB RAM, no AI accelerator, 100 ms SLA, SIL 1) | **H6131 / H-series 4G LTE gateway** | Peripheral cabinets, low-criticality monitoring, basic anomaly detection |
| `jetson_nano` (ARM + 128-core GPU, 4 GB unified, 50 ms SLA, SIL 1) | **X2 Industrial Computing Gateway** | Medium-voltage cabinets with on-edge ML, predictive maintenance for transformers and switches |
| `jetson_orin_nx` (ARM + 1024-core GPU, 16 GB, 30 ms SLA, SIL 2) | **Smart3000 Edge AI Box (RK3588)** | High-voltage substations, critical assets, multi-stream sensor fusion, near-real-time forecasting |

The Rockchip RK3588 NPU performance profile is sufficiently close to the
Jetson Nano class that the DMCA latency benchmarks (measured on NVIDIA T4
with a conservative ARM/edge penalty applied) transfer with controlled
adaptation. A short adaptation campaign would be performed in the pilot
to re-measure on actual Hongdian hardware.

## 5. Reapplying Stage 2 Model Selection on the Hongdian Stack

Using the canonical DMCA benchmark data (8 Hugging Face time-series
models, CMAPSS FD001, completion run 2026-04-27, real MAE values), TOPSIS
ranking with the standard weights `(MAE 0.5, latency 0.3, params 0.1,
license 0.1)` produces the following expected admissible set per
Hongdian deployment tier:

**Peripheral cabinets (H6131-class, no AI accelerator).**
Lag-Llama emerges as the rank-1 candidate with measured MAE 0.013336 and
estimated CPU-penalized latency within the 100 ms SLA. PatchTST-base
(0.67M parameters) ranks second. Larger foundation models (Moirai
families, Chronos-large, TimesFM, MOMENT-1-large) are filtered out by
the latency or RAM constraints — DMCA logs each rejection with the
specific constraint that triggered it, providing engineers with a clear
explanation of why a candidate was excluded.

**Medium-voltage cabinets (X2-class).**
Three admissible candidates: Lag-Llama (TOPSIS score 0.951, dominant on
all three criteria with the real MAE), MOMENT-1-large (0.591), PatchTST
(0.387). The accuracy gap between Lag-Llama and MOMENT is now decisive
post-completion-run.

**High-voltage substations (Smart3000-class, 30 ms SLA).**
Two admissible candidates after the strict latency filter: Lag-Llama
(0.613) and PatchTST (0.387). MOMENT-1-large (33 ms p95) is filtered
out for a 3 ms overshoot — a borderline rejection that DMCA flags
explicitly for a sensitivity-analysis review by the operator.

**Insight surfacing automatically.** The same canonical model
(Lag-Llama) wins in all three deployment tiers, but for different
reasons: in the lowest tier because alternatives are rejected by RAM/
latency filters, and in the highest tier because the strict 30 ms SLA
becomes more discriminating than raw compute. This is exactly the type
of context-sensitive trade-off that a manual MLOps team often misses
when evaluating models in isolation, and it surfaces naturally in the
DMCA pipeline.

## 6. Drift Detection Scenario in the Power Distribution Domain

The DMCA-Drift v3 detector — combining ADWIN (River, δ = 0.002) at
Layer 1, a 7-feature decision tree at Layer 2, and AAS context
enrichment at Layer 3 — was validated on the canonical drift cycle
experiment (2026-04-22, validated accuracy 80%, false alarm rate 0.0).
Translating that validation into the smart power distribution context,
representative drift triggers a Hongdian customer would see include:

- **Renewable energy mix shift.** A growing fraction of intermittent
  generation produces gradually changing load variance, classified by
  the v3 tree as `gradual` or `variance_shift` depending on rate.
- **Aging transformer thermal envelope.** Slow upward drift of
  baseline temperature classified as `incremental` (slope 0.1-0.5,
  monotonicity > 0.50).
- **Data center commissioning on-feeder.** New high-baseline constant
  load classified as `distribution_shift` (KS statistic > 0.40,
  outlier density low).
- **Sensor supplier change.** Calibration-driven systematic bias
  classified as `abrupt` if rapid, `gradual` if phased rollout.

Each classification is mapped to a specific DMCA Stage 5 strategy:
`abrupt` and `distribution_shift` typically trigger model re-ranking and
a swap proposal; `variance_shift` and `outlier_driven` are explicitly
classified as `no_swap` events to prevent reactive swaps from noise
spikes; `gradual` and `incremental` go through shadow-deployment
validation before any swap.

The Stage 5 conversational copilot delivers the alert to the field
operator in natural language — for the Hongdian deployment context this
should be available in **both Mandarin and English**, which is a minor
extension of the existing `pipeline/llm_router.py` infrastructure.

## 7. Hongdian-Specific Value Proposition

Three distinct value pools accrue to Hongdian if DMCA is integrated:

**Hardware uplift.** A Smart3000 + DMCA bundled offering can sustain a
20-40% premium over a Smart3000-only configuration, because the buyer
is paying for the AI-orchestration layer that converts the gateway
from a programmable platform into a managed service. The exact uplift
should be co-determined with Hongdian's commercial team based on
internal pricing data.

**Recurring software revenue.** Subscription pricing for the DMCA
orchestration layer can be tiered by gateway count, by criticality
(SIL level), or by number of monitored assets, producing a recurring
ARR stream on top of the historically one-shot hardware revenue.
Industry comparables (Siemens Senseye, GE Predix) suggest a per-asset
subscription range of $50-200/month at the mid-market segment.

**Customer retention and churn reduction.** Hongdian's edge-AI customers
who today abandon AI-on-gateway after 6-12 months — because their
deployed models silently degrade and nobody notices — become recurrent
under DMCA, since the lifecycle layer keeps the AI value pool intact
and visible. This is harder to quantify pre-pilot but is the most
strategically important benefit: it converts AI from a one-off project
into a continuous service relationship.

**Addressable market sizing (rough order-of-magnitude estimate).**
State Grid Corporation of China and China Southern Power Grid jointly
operate millions of distribution cabinets; even 1% adoption of an
intelligent monitoring solution corresponds to tens of thousands of
deployed gateways, before considering the broader manufacturing,
gas-station safety, and industrial automation verticals that Hongdian
already addresses.

## 8. Pilot Proposal — placeholder, to be co-authored

> *This section will be completed jointly with Hongdian after the first
> technical alignment meeting. The placeholder below describes the
> proposed shape of the pilot.*

**Duration.** 3-6 months, with a clear go/no-go review at the midpoint.

**Scope.** One representative end customer (proposed by Hongdian),
2-3 cabinets or assets, one Hongdian gateway tier (recommended:
Smart3000 in a substation context, given the dataset alignment with
ETT-h1), with DMCA running in parallel to existing monitoring.

**Roles.**
- *Hongdian:* customer access, gateway hardware, deployment integration,
  Mandarin operator UX validation, commercial decisioning.
- *DMCA team (Politecnico di Torino / Beihang):* framework adaptation,
  AAS profile authoring, drift-detector tuning, copilot LLM tuning,
  scientific publication.
- *Joint:* KPI definition, intellectual property allocation, pilot
  governance.

**KPIs to be measured.**

- Drift detection latency in real deployment (target: <50 timesteps
  from drift onset, baseline canonical: 20 timesteps).
- False alarm rate over 90 days continuous operation (target: ≤0.05).
- MAE containment during transition (target: degradation contained to
  <2× baseline for the duration of the swap process).
- Operator override / rejection rate of copilot proposals (target:
  >80% acceptance for SIL 1, >60% for SIL 2).
- Per-asset cost of operating DMCA on Smart3000 (target: <2% of asset
  monitoring revenue).

**Decision criteria at end of pilot.** A jointly defined threshold on
the KPIs above triggers either commercial integration or a pivot.

## 9. Intellectual Property and Risk Framework — placeholder, to be co-authored

> *This section will be completed jointly with the Politecnico di Torino
> Tech Transfer Office, Beihang University, and Hongdian's legal
> function. The placeholder below identifies the topics that must be
> resolved before deeper technical exchange.*

**Topics to resolve before code exchange.**

1. Ownership of the DMCA core framework (existing thesis IP), its
   adaptations developed during the pilot, and any joint inventions
   that emerge.
2. License model for the DMCA software during the pilot (research
   license vs. evaluation license vs. open-source release).
3. Joint publication policy: target venues (IEEE Transactions on
   Industrial Informatics, IEEE INDIN, IEEE IECON), authorship,
   embargo periods, and whether Hongdian customer data appears in
   the publication.
4. Confidentiality of customer data accessed during the pilot (NDA
   structure, anonymization protocol).
5. Export control review (EU Dual-Use Regulation 2021/821) for any
   technology transfer in either direction. A compliance check via
   the Politecnico di Torino Tech Transfer Office is recommended
   prior to first code share.
6. Provisional-patent options on key claims (DT-driven dynamic model
   selection with AAS-typed constraints, conversational re-alignment
   with calibrated confidence).

## 10. Next Steps

1. First technical alignment call (DMCA team ↔ Hongdian engineering
   contact) — recommended duration 60 minutes, agenda: confirm pain
   point fit, identify candidate customer segment, agree on shared NDA
   template.
2. Sign mutual NDA before any code or proprietary technical detail
   is exchanged.
3. Update Sections 8 and 9 of this document jointly.
4. Submit the proposal for endorsement by Politecnico di Torino relator
   and Beihang relator.
5. Kick off the pilot.

---

## Appendix A — Public references for the pain-point claims

- Vela, D., Sharp, A., Zhang, R., et al. (2022). *Temporal quality
  degradation in AI models.* Scientific Reports 12:11654.
  DOI: 10.1038/s41598-022-15245-z.
- Sculley, D., Holt, G., Golovin, D., et al. (2015). *Hidden Technical
  Debt in Machine Learning Systems.* NeurIPS 2015.
- Stanton, K. (2023). *Predictive maintenance analytics and
  implementation for aircraft: Challenges and opportunities.*
  Wiley Systems Engineering.
- Asset Administration Shell — IEC 63278-1, IDTA submodel templates.
- Zillow Offers shutdown public coverage: CNBC (2021-11-02), Stanford
  GSB analysis, AI Incident Database #149.

## Appendix B — DMCA project artifacts referenced in this proposal

- `assets/raspberry_pi_4.aas.json`, `assets/jetson_nano.aas.json`,
  `assets/jetson_orin_nx.aas.json` — IEC 63278-1 conformant AAS
  profiles used as reference deployment targets.
- `results/benchmarks/2026-04-07/benchmark_results_modal.csv` —
  canonical 8-model benchmark on CMAPSS FD001 and ETT-h1 (NVIDIA T4,
  $0.30 total).
- `results/benchmarks/2026-04-27/benchmark_mae_completion.csv` —
  completion run with the 5 missing MAE values, including the real
  Lag-Llama MAE = 0.013336 used in Section 5.
- `results/drift_experiments/drift_cycle_results.json` — canonical
  drift cycle experiment (detection at t=1380, recovery at t=1400,
  20-timestep latency).
- `results/drift_experiments/drift_validation_2026-04-22.json` —
  DMCA-Drift v3 validation (accuracy 80%, FAR 0.0).
- `pipeline/dmca_drift.py` — drift detector v3 implementation.
- `pipeline/llm_router.py` — copilot tier-0/1/2/3 routing logic.

## Appendix C — Document status

| Section | Status |
|---|---|
| 1. Why Hongdian, Why Now | Complete (public info only) |
| 2. The Pain Point, with Numbers | Complete (referenced) |
| 3. Target Segment: Smart Power Distribution | Complete (public info only) |
| 4. Hardware Mapping | Complete pending RK3588 latency re-measurement |
| 5. Stage 2 Model Selection on Hongdian Stack | Complete (canonical data) |
| 6. Drift Detection Scenario | Complete (translated from canonical experiment) |
| 7. Hongdian-Specific Value Proposition | Complete pending Hongdian commercial validation |
| 8. Pilot Proposal | Placeholder — to be co-authored post-NDA |
| 9. IP and Risk Framework | Placeholder — to be co-authored with Tech Transfer Office |
| 10. Next Steps | Complete (action list) |
