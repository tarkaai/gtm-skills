---
name: roi-calculator-scalable
description: >
  ROI Calculator & Business Case — Scalable Automation. Auto-generate ROI
  calculators and business cases when deals reach Proposed stage, deploy a
  self-service web calculator, A/B test ROI framing, and scale to 50+ deals
  per quarter without manual model building.
stage: "Sales > Proposed"
motion: "Outbound Founder-Led"
channels: "Direct, Email, Website"
level: "Scalable Automation"
time: "80 hours over 2 months"
outcome: ">=70% of prospects with >=5x ROI and >=60% calculator completion rate over 2 months"
kpis: ["ROI distribution", "Calculator completion rate", "ROI prediction accuracy", "Self-service calculator conversion"]
slug: "roi-calculator"
install: "npx gtm-skills add sales/proposed/roi-calculator"
drills:
  - roi-auto-generation
  - ab-test-orchestrator
  - roi-prediction-accuracy
---

# ROI Calculator & Business Case — Scalable Automation

> **Stage:** Sales > Proposed | **Motion:** Outbound Founder-Led | **Channels:** Direct, Email, Website

## Outcomes

Remove manual ROI calculator building entirely. Every deal reaching Proposed stage with sufficient pain data gets an auto-generated ROI calculator and business case within minutes. Deploy a self-service web calculator for inbound prospects. A/B test ROI framing to find the 10x multiplier: the optimal combination of value drivers, sensitivity scenarios, and delivery format. Scale to 50+ deals per quarter. Target: >=70% of prospects achieve >=5x ROI AND >=60% of prospects complete the calculator (self-service or seller-assisted).

## Leading Indicators

- Auto-generation trigger latency: <=5 minutes from deal stage change to calculator ready
- Auto-generation success rate: >=90% of qualifying deals get a calculator without errors
- Self-service calculator started-to-completed ratio: >=60%
- A/B test velocity: at least 2 experiments completed per month on ROI framing
- ROI model generation time: <=2 minutes per deal (API call + artifact creation)
- Seller review-to-send time: <=4 hours after auto-generation notification

## Instructions

### 1. Deploy auto-generation pipeline

Run the `roi-auto-generation` drill to build the always-on n8n workflow:

**Trigger configuration:**
- Attio webhook fires when a deal's stage changes to "Proposed"
- Secondary trigger: Attio webhook fires when `pain_count` is updated on a deal already in Proposed
- Filter: only proceed if `pain_count >= 2` AND `pain_quantification_rate >= 0.5` AND `roi_model_status != "generated"`
- Rate limit: maximum 10 auto-generations per day to control API costs

**Auto-generation flow:**
1. Pull full deal data from Attio (pain records, champion info, enrichment data)
2. Re-quantify low-confidence pains via `pain-quantification-prompt`
3. Validate pain-to-price ratio >=3 (if below, skip and alert seller)
4. Generate ROI model via `roi-model-generation`
5. Generate business case via `business-case-generation`
6. Create Google Sheet calculator pre-populated with prospect inputs
7. Attach both artifacts to the Attio deal record
8. Notify seller via Slack: "ROI calculator and business case ready for {company}. ROI: {X}x, payback: {Y} months. Review and send: {link}"

The seller's only job is to review the auto-generated materials and send them. No manual model building.

### 2. Build a self-service web calculator

Deploy an interactive ROI calculator on your website for inbound prospects:

1. Build a web form with input fields for the key value drivers identified in Baseline (e.g., team size, hours spent on manual process, current tool cost, deal volume)
2. On form completion, run `roi-model-generation` via API to compute ROI in real time
3. Display results: projected annual savings, ROI percentage, payback period, with conservative/moderate/optimistic scenarios
4. Capture the prospect's email and company name before showing detailed results
5. Auto-create an Attio deal with the calculator inputs and results
6. If ROI >=5x: trigger an instant sales alert and fast-track to a call
7. If ROI <3x: route to nurture sequence instead of sales

Track in PostHog: `calculator_started`, `calculator_completed`, `calculator_lead_captured`, `calculator_high_roi_alert`.

### 3. A/B test ROI framing and delivery

Run the `ab-test-orchestrator` drill to systematically test what produces the highest calculator completion rate and strongest deal progression:

**Month 1 experiments (pick 2):**
- **ROI presentation format:** Full spreadsheet vs one-page executive summary. Hypothesis: "A one-page summary with key numbers produces faster internal sharing and higher reference rate than a detailed spreadsheet." Minimum sample: 15 deals per variant.
- **Value driver emphasis:** Lead with time savings vs lead with cost reduction. Hypothesis: "Leading with time savings (relatable to the champion's daily experience) produces higher ROI validation rates than leading with cost reduction (abstract dollar figures)." Minimum sample: 15 deals per variant.

**Month 2 experiments:**
- **Sensitivity framing:** Show all 3 scenarios (conservative/moderate/optimistic) vs show only the conservative scenario. Hypothesis: "Showing only the conservative number builds more trust and produces higher reference rates."
- **Delivery timing:** Send calculator before the proposal call vs present live on the call. Hypothesis: "Sending in advance gives the champion time to review and prepare questions, resulting in more productive proposal calls."

For each experiment:
1. Use PostHog feature flags to randomly assign incoming deals to control or variant
2. Run for minimum 14 days or until 15+ deals per variant
3. Measure primary metric: `roi_referenced_in_decision` rate. Secondary: deal velocity, calculator completion rate.
4. Auto-promote winners using `ab-test-orchestrator` evaluation logic

### 4. Build industry benchmarks from accumulated data

After 50+ ROI models, aggregate across deals to build benchmarks:
- Average ROI by industry ("Companies in B2B SaaS typically see 8-12x ROI")
- Average savings per value driver by company size
- Most common value driver by persona (VP Sales → revenue increase; VP Ops → time savings)
- Payback period distribution

Inject these benchmarks into the `roi-model-generation` prompt as validation anchors. Use them in the self-service calculator: "Companies like yours typically save 30-40% on [cost category] — you're projecting 35%, which aligns with peers."

### 5. Begin accuracy tracking

Run the `roi-prediction-accuracy` drill to establish the feedback loop:

1. Set up the monthly n8n cron to identify closed-won deals that are 90+ days post-close
2. For each qualifying deal, compare projected ROI against actual customer outcomes
3. Compute accuracy per value driver and overall
4. Generate the first calibration report
5. Apply calibrations to future ROI model generation

This data becomes critical at Durable level. Start collecting now so you have a baseline when you get there.

### 6. Scale and evaluate

Increase deal volume to 50+ per quarter using the auto-generation pipeline. Monitor:
- Auto-generation success rate (target >=90%)
- Seller review-to-send time (target <=4 hours)
- Calculator completion rate for self-service (target >=60%)
- ROI distribution (target >=70% at >=5x)
- A/B test results and winning variants

After 2 months, evaluate:
- If >=70% of deals have >=5x ROI AND >=60% calculator completion rate: proceed to Durable
- If ROI distribution is strong but completion rate is low: the calculator UX needs improvement (simplify inputs, reduce friction, add progress indicators)
- If completion rate is high but ROI is weak: discovery is not producing enough pain data. Tighten the qualification bar before deals enter Proposed stage.
- If A/B tests show no clear winners: run longer experiments or test more dramatic variations

## Time Estimate

- 20 hours: deploying auto-generation pipeline (n8n workflows, Attio webhooks, Slack notifications, error handling)
- 15 hours: building self-service web calculator (form, API integration, PostHog tracking, Attio sync)
- 10 hours: setting up A/B test infrastructure and first experiments
- 10 hours: building industry benchmarks and integrating into model generation
- 5 hours: setting up roi-prediction-accuracy pipeline
- 20 hours: monitoring, iterating on experiments, and adjusting over 2 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | Deal records, webhooks, pain data, ROI tracking | Standard stack (excluded) |
| PostHog | Event tracking, funnels, feature flags, experiments | Standard stack (excluded) |
| n8n | Auto-generation pipeline, cron jobs, workflow orchestration | Standard stack (excluded) |
| Anthropic Claude API | ROI model generation + business case at scale | ~$30-80/mo at 50+ deals/quarter — [pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Clay | Company enrichment for benchmark building | Launch: $185/mo — [pricing](https://www.clay.com/pricing) |
| Google Sheets API | Calculator artifact creation | Free with Google Workspace |

**Play-specific cost:** ~$215-265/mo (Claude API + Clay)

## Drills Referenced

- `roi-auto-generation` — always-on pipeline that auto-generates ROI calculators and business cases when deals reach Proposed stage with sufficient pain data
- `ab-test-orchestrator` — designs, runs, and evaluates A/B tests on ROI framing, delivery format, and value driver emphasis
- `roi-prediction-accuracy` — establishes the projected vs realized ROI feedback loop and begins collecting accuracy data for calibration
