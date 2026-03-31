---
name: success-criteria-definition-scalable
description: >
  Success Criteria Definition — Scalable Automation. The 10x multiplier is AI-powered criteria
  intelligence: the system recommends optimal success criteria for each deal based on historical
  achievement data from similar deals. A/B testing optimizes workshop scheduling, criteria
  framing, and success plan format. Post-sale tracking validates whether defined criteria
  predict retention and expansion.
stage: "Sales > Connected"
motion: "OutboundFounderLed"
channels: "Direct, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=75% of deals with defined criteria at scale, deals with criteria close at >=20% higher rate than those without, and criteria achievability model calibrated to within +-15% accuracy"
kpis: ["Success criteria definition rate at scale", "Close rate lift (criteria vs no-criteria)", "Post-sale achievement rate", "Achievability model accuracy", "Deal velocity with defined criteria"]
slug: "success-criteria-definition"
install: "npx gtm-skills add sales/connected/success-criteria-definition"
drills:
  - success-criteria-intelligence
  - ab-test-orchestrator
  - success-criteria-reporting
---

# Success Criteria Definition — Scalable Automation

> **Stage:** Sales → Connected | **Motion:** OutboundFounderLed | **Channels:** Direct, Email

## Outcomes

Find the 10x multiplier. At Baseline, the agent extracts criteria from transcripts and the founder conducts workshops. At Scalable, the system learns from every deal's outcome to recommend better criteria for future deals. AI-powered intelligence tells the founder: "For companies like this, these criteria have an 85% achievement rate and correlate with 2x higher retention." A/B testing optimizes every touchpoint — scheduling messages, criteria framing, success plan format. Post-sale tracking closes the loop.

**Pass threshold:** >=75% of deals with defined criteria at scale, deals with criteria close at >=20% higher rate than those without, and criteria achievability model calibrated to within +-15% accuracy.

## Leading Indicators

- AI recommendations are generated for >=90% of new Connected deals
- Recommendation acceptance rate >=60% (prospects adopt the suggested criteria)
- A/B tests produce statistically significant winners within 4 weeks
- Post-sale achievement rate tracks within +-15% of predicted achievability scores
- Deals with AI-recommended criteria close faster than deals with manually defined criteria

## Instructions

### 1. Deploy Success Criteria Intelligence

Run the `success-criteria-intelligence` drill:

**Build the historical dataset:**
- Export all deals from Attio where `success_criteria_status` = "defined" or "agreed"
- For closed deals, pull: outcome (won/lost), retention months, expansion status, NPS
- For each criterion on each deal: was it achieved post-sale? What was the actual value vs target?
- Minimum viable dataset: 20 closed deals with criteria. If you don't have 20 yet, start building the dataset while running Baseline in parallel — Scalable intelligence improves with every new closed deal.

**Compute achievement statistics (weekly via n8n):**
- Achievement rate by category (efficiency criteria achieve at X%, revenue criteria at Y%)
- Achievement rate by industry (SaaS companies achieve efficiency criteria at higher rates than agencies)
- Close rate correlation: deals with criteria close at X% vs Y% for those without
- Retention correlation: deals where >=80% of criteria were achieved retain Z months longer

**Generate recommendations for new deals:**
- When a new deal enters Connected, the n8n workflow auto-triggers
- Pull prospect characteristics from Attio
- Match against the 10 most similar closed-won deals
- Generate recommended criteria ranked by: `(achievement_rate * close_rate_correlation * retention_impact)`
- Store recommendations in Attio note tagged `criteria-recommendations`
- Include in the workshop briefing: "For {industry} companies with {headcount} employees, these criteria have the highest success rates"

### 2. A/B Test the Full Funnel

Run the `ab-test-orchestrator` drill to set up experiments on the success criteria program:

**Experiment 1 — Workshop Scheduling Message (weeks 1-4):**
- Control: Current message ("I'd like to spend 30 minutes making sure we're aligned on what success looks like")
- Variant A: Lead with social proof ("Other {industry} companies defined 4 criteria that predicted 90-day success with 85% accuracy")
- Variant B: Lead with specificity ("Based on your goals around {primary_pain}, I've drafted 3 measurable targets for us to refine together")
- Measure: Workshop booking rate. Minimum 30 sends per variant.

**Experiment 2 — Criteria Framing (weeks 3-6):**
- Control: Present all criteria at once in the workshop
- Variant: Present one category at a time (efficiency first, then revenue, then adoption) and let the prospect choose which matter most
- Measure: Prospect agreement rate and number of criteria agreed. Minimum 15 workshops per variant.

**Experiment 3 — Success Plan Format (weeks 5-8):**
- Control: Text-based mutual success plan stored as Attio note
- Variant A: Structured table with RAG status indicators (Red/Amber/Green for each criterion)
- Variant B: One-page visual summary with the 3 most important criteria highlighted
- Measure: Prospect reference rate (how often they bring up the plan in subsequent conversations). Minimum 20 plans per variant.

Log all experiments in PostHog using feature flags. Auto-promote winners after statistical significance is reached.

### 3. Build Comprehensive Reporting

Run the `success-criteria-reporting` drill:

- Build the 6-panel PostHog dashboard: definition rate trend, criteria quality distribution, close rate comparison, achievement rate by category, deal velocity comparison, stakeholder alignment
- Create 3 Attio saved views: deals missing criteria, at-risk criteria (low achievability), criteria lifecycle funnel
- Set up the weekly digest (Slack + Attio)
- Set up the monthly ROI report calculating the revenue impact of the success criteria program

### 4. Close the Post-Sale Loop

Connect success criteria to customer outcomes:

- When a deal moves to Won, auto-transfer the mutual success plan to the customer success workflow
- Set n8n reminders at each review checkpoint defined in the mutual plan
- At each checkpoint: query product analytics to determine whether each criterion is being met
- Update Attio: mark each criterion as "on_track", "at_risk", or "achieved" / "missed"
- Fire PostHog events: `success_criteria_achieved` or `success_criteria_missed` with the criterion details

Feed achievement data back into the intelligence engine:
- Every "achieved" or "missed" data point improves future recommendations
- Recalculate achievability scores monthly based on actual outcomes

### 5. Scale Volume

With intelligence and automation in place, increase throughput:
- Run criteria extraction for ALL Connected deals, not just new ones — backfill any deals that missed the Baseline automation
- Target: zero deals should reach Qualified stage without defined success criteria
- The founder's workshop time is the bottleneck — prioritize by deal value. For smaller deals, consider sending the mutual success plan asynchronously and asking for async feedback.

### 6. Evaluate Against Threshold

After 2 months, measure:
- Definition rate: % of Connected+ deals with defined criteria (target >=75%)
- Close rate lift: close rate for deals WITH criteria vs WITHOUT (target >=20% improvement)
- Achievability calibration: compare predicted achievability scores against actual achievement rates (target within +-15%)
- Post-sale achievement rate: what % of defined criteria are being met? (track but no threshold — this is a leading indicator for Durable)

If all pass: proceed to Durable for autonomous optimization.
If definition rate fails: the scheduling or extraction pipeline has gaps. Check n8n workflow execution logs.
If close rate lift is not significant: the criteria may not be influencing deals. Run qualitative analysis — are prospects actually using the success plans in their decision process?
If achievability calibration is off: the scoring model needs recalibration. Use the `success-criteria-intelligence` monthly calibration workflow.

## Time Estimate

- 10 hours: Intelligence engine setup (historical dataset, statistics computation, recommendation workflow)
- 8 hours: A/B test design and orchestrator configuration
- 6 hours: Reporting dashboard and automation setup
- 4 hours: Post-sale tracking workflow build
- 20 hours: Ongoing workshop calls (~30 min each, ~40 calls over 2 months, founder time)
- 8 hours: Experiment analysis, model calibration, and weekly review
- 4 hours: Volume scaling and backfill

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — deal tracking, criteria attributes, automations, reporting | $29/user/mo (Plus) or $59/user/mo (Pro) — [attio.com/pricing](https://attio.com/pricing) |
| Fireflies | Transcription — discovery and workshop calls at volume | $18/user/mo (Pro) — [fireflies.ai/pricing](https://fireflies.ai/pricing) |
| PostHog | Analytics — dashboards, experiments, A/B testing | Free up to 1M events, then usage-based — [posthog.com/pricing](https://posthog.com/pricing) |
| Cal.com | Scheduling — workshop booking | Free or $12/user/mo — [cal.com/pricing](https://cal.com/pricing) |
| n8n | Automation — intelligence workflows, post-sale tracking, scheduling | $60/mo (Pro, 10K executions) — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | AI — criteria extraction, intelligence recommendations | ~$15-30/mo at scale — [anthropic.com/pricing](https://www.anthropic.com/pricing) |

**Estimated play-specific cost this level:** ~$150-300/mo. Primary cost drivers: Attio Pro ($59/user/mo for advanced automations), n8n Pro ($60/mo), Fireflies Pro ($18/mo), Anthropic API (~$15-30/mo at higher volume).

## Drills Referenced

- `success-criteria-intelligence` — AI-powered recommendation engine that suggests optimal criteria based on historical achievement data and prospect similarity
- `ab-test-orchestrator` — run controlled experiments on workshop scheduling, criteria framing, and success plan format
- `success-criteria-reporting` — dashboards, weekly digests, and monthly ROI reports tracking the success criteria program
