# AlignEdge — Pitch Deck Content Skeleton

**Version:** v1.0
**Date:** 2026-07-03
**Program:** Beijing Founder Program 2026
**Constraint:** 10 slides · PDF only · No contact info · No fundraising ask · China focus required

**Design principles (Y Combinator):**
- 1 idea per slide · huge text (60-80pt headlines) · high contrast · numbers > words · 3-second test

---

## Slide 1 — Cover

**Layout:** template cover (left column + right column)

**Content:**
- **Headline (huge):** AlignEdge — Runtime maintenance layer for edge AI
- **One-line description:** The right-sized AI model, on the right chip, at the right time
- **Signature tag (smaller, italic, below):** The Haiku-not-Opus moment for industrial AI
- **Presenter block:**
  - Kevin Omede
  - MSc, Politecnico di Torino × Universitat Internacional de Catalunya
  - Visiting Researcher, Beihang University
  - Beijing Founder Program · July 2026

**Visual:** typography only. 2-color palette. AlignEdge brand accent + neutral.

---

## Slide 2 — Problem

**Layout:** template problem — headline + 3-column body

**Content:**
- **Headline (huge):** Factories lose $2.3M every hour when AI models miss the alarm

- **Column 1 — The Core Problem:**
  > "AI models deployed on factory hardware silently degrade — too slow for the SLA budget, sensor signals drift, chip and model don't match. No one notices until a machine fails."

- **Column 2 — Quantifying the Pain:**
  > "**$2.3M per hour in automotive downtime** · 3–6 months average detection delay · Missed alarms invisible to cloud-side monitoring because the cloud never sees SLA-violating requests."

- **Column 3 — Why the Status Quo Fails:**
  > "MLOps tools monitor cloud performance. Compilers optimize per-inference latency. Nobody measures whether the model actually runs in time on the real chip, under the real workload."

**Source citation (small, bottom):** Aberdeen Research · Siemens True Cost of Downtime 2024

**Visual:** none — the number $2.3M is the visual.

---

## Slide 3 — Solution

**Layout:** template 3-step workflow (01/02/03)

**Content:**
- **Headline (huge):** AlignEdge tests your AI on real edge hardware — then keeps it working

- **Step 01 — You send:**
  > "Your model in any format, a representative data sample, and your target hardware spec with SLA budget."

- **Step 02 — We test:**
  > "Real-hardware profiling on **Jetson Nano, Raspberry Pi 4, and Jetson Orin NX**. Drift injection across 5 failure modes. Coverage analysis against your SLA. Multi-criteria comparison against 8 benchmarked foundation models."

- **Step 03 — You know:**
  > "15-page report with per-model verdict — keep, optimize, or swap. Concrete deployment recommendations. AI Act-aligned audit trail."

**Visual:** 3 numbered blocks with light icons. Redraw from `figures/dmca_framework.tikz` simplified.

---

## Slide 4 — Insight (embeds the "why me")

**Layout:** headline + central killer chart + 3-column body

**Content:**
- **Headline (huge):** Everyone measures accuracy. Nobody measures coverage. That's where machines break.

- **Central killer chart:**
  ```
  LEAD TIME TO FAILURE — BEARING 3_2

  █████████████████████████ 290s  PatchTST     [green]
  █████████████████████     240s  Lag-Llama    [green]
  ██████                     80s  Moirai-S     [red]

                       ┃ 5-minute action window
                       ▼

  Real bearing data · PHM 2012 Challenge · Public dataset
  ```

- **Column 1 — The Core Insight:**
  > "Accuracy × Coverage = events actually caught. Compilers optimize latency, MLOps monitors drift, nobody measures coverage — the fraction of predictions that arrive in time on real hardware, under real workload. A 99%-accurate model with 40% coverage catches 40% of events. The missing 60% is the missed alarm."

- **Column 2 — How We Know It:**
  > "8 months of hardware-real benchmarks — 8 foundation models on real GPU for $0.30 canonical cost. Validated on PHM 2012 Challenge bearings and IMS Center. Same task, same data — 10× gap in coverage between the right model and the wrong one."

- **Column 3 — The Unfair Advantage:**
  > "Coverage lives orphaned between real-time systems and MLOps — an unowned cross-discipline. My triple background — industrial engineering (Polito), ML systems research (Beihang), and hardware-real benchmarks — makes visible what specialists miss."

**Data source:** `results/missed_alarm/results.csv` — Bearing3_2 rows

---

## Slide 5 — Why Now

**Layout:** template why-now 3-column

**Content:**
- **Headline (huge):** Three converging shifts open a 24-month window

- **Column 1 — Regulatory Shift (label: MANDATORY COMPLIANCE):**
  > "EU AI Act enters high-risk enforcement August 2026. Industrial AI requires documented drift monitoring and audit trails. **Penalties up to 3% of global turnover or €15M** — Article 99 non-compliance tier."

- **Column 2 — Technology Shift (label: FOUNDATION MODEL EXPLOSION):**
  > "HuggingFace grew from ~1M to **2.4M+ models** in 2 years — the second million took only 335 days. Manual model selection for edge deployment is now combinatorially impossible."

- **Column 3 — Market Shift (label: INFRASTRUCTURE VACUUM):**
  - **Big anchor (huge):** LOCK-IN
  - **Body text (two lines):**
    > "Every chip vendor locks you in.
    > No vendor has incentive to build the agnostic decision layer."

**Visual:** 3-column layout, gold labels + navy body text.

---

## Slide 6 — Business Model

**Layout:** ladder 3-step — verb label small on top, product name huge below

**Content:**
- **Headline (huge):** Three products in sequence — one wedge, one core, one platform

- **Column 1:**
  - `LAND` (small, uppercase, gold/accent color)
  - **AUDIT** (HUGE, primary heading)
  - > "On-hardware validation. Our first market entry."
  - *[Note: specific "4 weeks" commitment lives on Slide 3, not here — Slide 6 is strategic overview]*

- **Column 2:**
  - `EXPAND` (small, uppercase, gold/accent color)
  - **RUNTIME** (HUGE, primary heading)
  - > "Continuous drift detection + automatic swap. Enterprise subscription."

- **Column 3:**
  - `DEEPEN` (small, uppercase, gold/accent color)
  - **OPTIMIZATION** (HUGE, primary heading)
  - > "Fleet-wide cross-vendor orchestration. Platform-scale integration."

- **Footer strip (below the 3 columns):**
  - > "LAND · EXPAND · DEEPEN — Same customer, growing footprint over time."

**Visual:** ladder diagram — 3 rising steps. Each step: small gold verb label on top → huge product name below → description. Creates typographic hierarchy that reads at multiple scales (3s glance vs full read).

---

## Slide 7 — Competition

**Layout:** template competition — 2×2 matrix + differentiator list

**Content:**
- **Headline (huge):** Three reasons no one else can catch up

- **Matrix 2×2:**
  - Y-axis: `Coverage / drift aware ↑`
  - X-axis: `Hardware-aware →`
  - Bottom-left: `Status quo (manual audits, one-off)` — small gray box
  - Top-left: `Arize · Fiddler · WhyLabs` — ML observability, cloud-only
  - Bottom-right: `TensorRT · OpenVINO · MLPerf` — HW-optimized, no drift
  - Top-right: `AlignEdge` — brand accent color, highlighted

- **Key Differentiators (right column) — reordered for narrative impact:**
  1. "Cross-vendor by design. No chip vendor will cannibalize their own lock-in."
  2. "Productized audit measuring SLA coverage on your hardware, with your data."
  3. "A dataset that compounds — every audit adds proprietary customer × model × hardware × drift data no competitor can replicate."

**Visual:** 2×2 matrix redraw from scratch. Solid palette. AlignEdge box highlighted.

---

## Slide 8 — China Strategy

**Layout:** simplified — bilingual title + map + big number + statement

**Content:**
- **Headline (huge, bilingual):** CHINA · 中国

- **Map visual:** outline of China with single pin — Chaoyang, Beijing

- **Sub-caption under map:**
  > "Chaoyang HQ · Wangjing automotive AI cluster · 20 min from Capital Airport"

- **Big number (huge, center):** 75%

- **Big number caption:**
  > "of the world's EVs are produced in China"

- **Market context (secondary numbers):**
  > "$318B — global automotive electronics market (2026) · 43.6% Asia Pacific share"

- **Statement:**
  > "This is the largest edge AI deployment testbed on Earth."

- **Source (small, bottom):** IEA Global EV Outlook · 2026 · Fortune Business Insights · 2026

**Visual:** China outline SVG + red pin at Chaoyang.

---

## Slide 9 — Team + Traction

**Layout:** founder card + institution row + validated tech card

**Content:**
- **Headline (huge):** One founder, three institutions, validated technology

- **Founder card (center):**
  - Photo: Kevin Omede (profile photo)
  - Name: **Kevin Omede**
  - Role: Founder
  - Bullets:
    - "MSc student, Politecnico di Torino × Universitat Internacional de Catalunya"
    - "Visiting Researcher, Beihang University"
    - "Thesis: Dynamic Model-Context Alignment in Industry 4.0"

- **Institution row (3 logos):**
  - Politecnico di Torino
  - Universitat Internacional de Catalunya
  - Beihang University

- **Program selection callout:**
  - Beijing Founder Program 2026 · Selected

- **Validated technology card:**
  - "5-stage DMCA closed-loop framework"
  - "Drift classifier: 92% accuracy held-out · 0% false alarms"
  - "Benchmark: 8 foundation models on real GPU · $0.30 canonical cost"
  - "PHM 2012 + IMS Center validation · 10× coverage gap demonstrated"

**Note IP discipline:** IRT SystemX intentionally omitted from this deck (per IP memo §6, pre-RIMIN/TRIN advice).

---

## Slide 10 — Vision

**Layout:** big statement + closing signature

**Content:**
- **Headline (huge, 10-word vision):** Every industrial AI model, always in its optimal deployment state

- **Future State body:**
  > "AI-on-edge becomes a maintained asset, not a one-shot deployment. Every model in every factory continuously right-sized to its hardware, its drift signature, its SLA. Missed alarms — the most expensive failure mode in industrial AI — eliminated."

- **Scale of Impact:**
  > "By 2030: millions of models continuously maintained. Hundreds of billions of dollars in industrial downtime prevented."

- **Closing signature (large italic):**
  > *The Haiku-not-Opus moment for industrial AI.*

**Visual:** text-only, palette dark-inverted for closing impact.

---

## Design System (apply consistently across all 5 visuals)

**Palette** (6 colors, no gradients, no shadows)
- Primary dark: navy `#0A2540` — hero text, box fills, key elements
- Accent gold: amber-ochre `#D4A017` — small labels, key numbers, highlights
- Background: off-white `#F5F7FA`
- Neutral gray: `#8B95A0` — secondary text, competitor boxes
- Signal green: emerald `#2E9B58` — actionable, success
- Signal red: coral `#D64545` — missed, risk

**Typography**
- Serif for hero headlines and big numbers (Playfair Display / Merriweather / template default)
- Sans-serif for body, labels, axis labels (Inter / IBM Plex Sans)
- Monospace only for raw data captions if needed (JetBrains Mono)

**Style rules**
- Stroke uniform 2px on all lines/borders
- Border-radius 4px on box corners
- Arrow heads simple filled triangle, single layer
- No shadows, no gradients, no glass/blur effects
- Generous whitespace — every element must earn its pixels
- Mood: engineered-precise, industrial (NYT/FT graphics style, not marketing-corporate)

**Consistency rule:** across all 5 visuals, same palette + same stroke weight + same typography hierarchy = same brand.

---

## Visual Asset Specifications

Detailed specs below — one per asset. Design tool executes these however native to it (PPT shapes, native charts, custom svg — irrelevant). What matters is the final composition matching the spec.

---

### Visual #1 — Bar chart Bearing 3_2 (slide 4)

**Purpose:** convey in 3 seconds that the same task on the same data has a 10× gap in "how much warning you get" between the right model and the wrong one — the killer proof of the coverage insight.

**Layout:** horizontal bar chart, 3 bars, one vertical dashed reference line.

**Data (exact values) — CORRECTED to show COVERAGE %, aligned to 10× headline:**
- PatchTST: 85% SLA coverage
- Lag-Llama: 64% SLA coverage
- Moirai-S: 9.3% SLA coverage
- Sub-annotation (small): "Warning time on this bearing: 290s / 240s / 80s — 3.6× ratio"

*Note: the chart shows COVERAGE %, not warning time. Coverage is the insight — the "10× gap" refers to 85% vs 9.3%. Warning time is secondary detail. This alignment fixes the mismatch a VC analyst would spot.*

**Elements & positions:**
- Title above chart: "LEAD TIME TO FAILURE — BEARING 3_2" (serif, small caps, navy)
- 3 horizontal bars, aligned left, each on its own row
- Bar labels on the left (model name in sans-serif, navy)
- Value labels on the right end of each bar (large sans-serif, matching bar color)
- Vertical dashed reference line at 300s with label "5-min action window" (small, gray, italic)
- Below chart caption: "Same task · same data · 10× gap in coverage. Real bearing data · PHM 2012 Challenge · Public dataset." (small gray sans-serif)

**Colors:**
- PatchTST bar: signal green `#2E9B58` (actionable — inside window)
- Lag-Llama bar: signal green `#2E9B58` (actionable — inside window)
- Moirai-S bar: signal red `#D64545` (missed — outside window)
- Reference line: neutral gray `#8B95A0`, dashed

**Do:** big numbers on bar ends, no gridlines, no axes ticks except x-scale minimum
**Don't:** legend (redundant), error bars, secondary chart, title in bold

---

### Visual #2 — China map + Chaoyang pin (slide 8)

**Purpose:** anchor "China" geographically in a single visual moment — the viewer sees the country, one pin, one district name, and moves on to the 75% number.

**Layout:** simplified China outline (single polygon fill), one pin, one labeled callout.

**Elements & positions:**
- China country outline, solid navy fill at 60% opacity, no internal provincial borders
- Single pin at Beijing coordinates (approx. 39.9°N, 116.4°E)
- Pin: gold `#D4A017` filled circle, 12–16px diameter, with 2px navy border
- Callout to the right of pin: 2 lines of text
  - Line 1 (larger, navy bold): "Chaoyang, Beijing"
  - Line 2 (smaller, gray): "Wangjing automotive AI cluster · 20 min from Capital Airport"
- Optional: thin gold line connecting pin to callout, 1px

**Colors:**
- China outline: navy `#0A2540` at 60% opacity fill, 2px navy border
- Pin: gold `#D4A017`
- Callout text: navy `#0A2540` for name, gray `#8B95A0` for description

**Do:** minimal outline (simplified, no coastline detail), single pin, generous whitespace around the map
**Don't:** other cities, provincial borders, latitude/longitude grid, other pins, decorative elements

---

### Visual #3 — 2×2 Competitive matrix (slide 7)

**Purpose:** show in 3 seconds that AlignEdge occupies a quadrant no competitor is in — the top-right (hardware-aware AND coverage-aware).

**Layout:** 2×2 grid with labeled axes, 4 quadrants containing competitor boxes, one highlighted box for AlignEdge.

**Axes:**
- X-axis (horizontal): "Hardware-aware →"
- Y-axis (vertical): "Coverage / drift aware ↑"
- Axis labels in small sans-serif, gray

**Quadrant contents:**
- Top-left quadrant (coverage-aware, NOT hardware-aware): box labeled "Arize · Fiddler · WhyLabs"
  - Sub-label: "ML observability, cloud-only"
- Top-right quadrant (both hardware-aware AND coverage-aware): box labeled "AlignEdge"
  - Sub-label: "[YOU ARE HERE]" or "This is us"
- Bottom-left quadrant (neither): box labeled "Status quo"
  - Sub-label: "Manual audits, one-off"
- Bottom-right quadrant (hardware-aware, NOT coverage-aware): box labeled "TensorRT · OpenVINO · MLPerf"
  - Sub-label: "HW-optimized, no drift"

**Colors:**
- AlignEdge box (top-right): navy `#0A2540` fill, gold `#D4A017` 2px border, white text
- All other competitor boxes: off-white fill, neutral gray `#8B95A0` 2px border, dark gray text
- Axes: thin gray lines with small arrow heads

**Size hint:** AlignEdge box slightly larger than competitor boxes (15–20% bigger) to draw eye

**Do:** clean grid, AlignEdge visually dominant, all boxes same rounded style
**Don't:** logos of competitors (typographic names only), scores or percentages, bullet lists inside boxes

---

### Visual #4 — Ladder business model (slide 6)

**Purpose:** show 3 products as a progression of increasing depth — LAND → EXPAND → DEEPEN — with product names dominant and verb labels subordinate.

**Layout:** 3 rising rectangular steps left-to-right, like a staircase seen from the side. Each step contains stacked text.

**Step 1 (leftmost, shortest):**
- Small gold uppercase label at top: `LAND`
- Huge navy heading below: `AUDIT`
- Small gray description below: "On-hardware test, 4 weeks. Broad market entry."

**Step 2 (middle, taller than step 1):**
- Small gold uppercase label at top: `EXPAND`
- Huge navy heading below: `RUNTIME`
- Small gray description below: "Continuous drift detection + automatic swap. Enterprise subscription."

**Step 3 (rightmost, tallest):**
- Small gold uppercase label at top: `DEEPEN`
- Huge navy heading below: `OPTIMIZATION`
- Small gray description below: "Fleet-wide cross-vendor orchestration. Platform play."

**Visual metaphor:** each step is taller than the previous → conveys progression, deepening engagement, growing ACV.

**Colors:**
- Step fill: navy `#0A2540` solid
- Gold labels: `#D4A017`
- Product name (huge): white on navy fill
- Descriptions: light gray `#B8C0CA` on navy fill (readable but subordinate)

**Do:** typographic hierarchy at 3 scales (label → name → description), consistent step spacing
**Don't:** icons on steps, pricing, arrows between steps (implied by progression), decorative connectors

---

### Visual #5 — 3-step workflow diagram (slide 3)

**Purpose:** show the audit process is short and self-contained — customer sends, we test, customer receives. Three boxes, two arrows, done.

**Layout:** 3 rectangular boxes in horizontal row, connected by 2 arrows.

**Box 1 (leftmost):**
- Big gold number top-left: `01`
- Heading (navy): "You send"
- Icon (simple geometric flat): upload/arrow-up or file icon
- Description below: "Your model, a data sample, hardware spec, SLA target."

**Box 2 (middle):**
- Big gold number top-left: `02`
- Heading (navy): "We test"
- Icon (simple geometric flat): chip/processor or gear icon
- Description below: "Real-hardware profiling on Jetson Nano, Raspberry Pi 4, Jetson Orin NX. Drift injection. Coverage analysis. TOPSIS comparison."

**Box 3 (rightmost):**
- Big gold number top-left: `03`
- Heading (navy): "You know"
- Icon (simple geometric flat): document/checkmark
- Description below: "15-page report with per-model verdict — keep, optimize, or swap. AI Act-aligned audit trail."

**Arrows between boxes:** thin navy, single filled arrowhead, horizontal

**Colors:**
- Box fill: off-white `#F5F7FA` or transparent
- Box border: navy `#0A2540` 2px
- Number: gold `#D4A017`, huge
- Heading: navy
- Icon: navy or gold monochrome, simple line style
- Description: neutral gray

**Do:** equal box sizes, equal spacing, minimal icon complexity
**Don't:** 3D effects, gradient fills, complex icons with multiple colors, sub-steps inside boxes

---

## Non-visual assets Kevin provides separately

- **Kevin profile photo** (slide 9) — his profile photo, insert directly
- **Institution logos** (slide 9) — Politecnico di Torino, Universitat Internacional de Catalunya, Beihang University — official brand-kit versions

**IP discipline reminder:** no IRT SystemX logo anywhere in this deck (per §6 IP memo, pre-RIMIN/TRIN advice).

---

## Post-Design Checklist

Before considering deck finished:
- [ ] All 10 slides pass the 3-second test (idea comprehensible in 3s from cold view)
- [ ] No slide has more than 40 words of body copy
- [ ] Every claim has a source citation OR is a self-verified metric from your thesis
- [ ] No slide names customer targets (per Kevin's positioning decision)
- [ ] No slide contains "raising X" or contact information
- [ ] PDF export ≤ 50MB
- [ ] Rehearsed cold at least 3 times start-to-finish under 7 minutes

---

## Version log

- v1.0 — 2026-07-03 — first complete draft locked, ready for design phase
