---
name: lead-scoring-system-durable
description: >
  Lead Scoring System — Durable Intelligence. AI agent continuously monitors scoring model accuracy,
  generates improvement hypotheses, runs A/B experiments on scoring weights and criteria,
  auto-implements winners, and adapts to market drift. Converges when successive experiments
  produce <2% improvement.
stage: "Sales > Qualified"
motion: "Outbound Founder-Led"
channels: "Product, Email, Website"
level: "Durable Intelligence"
time: "130 hours over 6 months"
outcome: "Sustained or improving lead score accuracy (>=4x Hot vs Cold conversion) over 6 months via continuous agent-driven scoring optimization and market adaptation"
kpis: ["Conversion rate by tier (sustained >=4x)", "Scoring model accuracy trend", "Agent experiment win rate", "Predictive score vs actual close rate correlation"]
slug: "lead-scoring-system"
install: "npx gtm-skills add sales/qualified/lead-scoring-system"
drills:
  - autonomous-optimization
  - scoring-model-performance-monitor
---

# Lead Scoring System — Durable Intelligence

> **Stage:** Sales > Qualified | **Motion:** Outbound Founder-Led | **Channels:** Product, Email, Website

## Outcomes

The lead scoring system runs autonomously with an AI agent that monitors model accuracy, detects when the scoring model drifts out of calibration (due to market changes, competitor shifts, or product evolution), generates hypotheses for improvement, runs controlled experiments, and auto-implements winners. The Hot-to-Cold conversion ratio stays at >=4x for 6 continuous months. The agent converges when successive experiments produce <2% improvement — the model has found its local maximum.

## Leading Indicators

- Weekly scoring accuracy report shows stable or improving Hot/Cold conversion ratio
- Agent-generated experiments have a >30% win rate (at least 1 in 3 experiments improves the model)
- False negative rate trends downward month over month (<5% target)
- Scoring model weight changes correlate with closed-won deal pattern shifts (model adapts to market)
- Time between anomaly detection and corrective experiment launch is <7 days

## Instructions

### 1. Deploy the scoring model performance monitor

Run the `scoring-model-performance-monitor` drill. Build:

**PostHog dashboard — "Lead Scoring Model Health":**
- Conversion rate by tier (primary accuracy metric, target: Hot >=4x Cold)
- Score distribution histogram (target: 15-25% Hot)
- False negative rate (Cold leads that converted, target: <10%)
- False positive rate (Hot leads that never engaged, target: <20%)
- Score-to-close correlation scatter (higher score should predict faster close)
- Model drift indicator (week-over-week Hot conversion change)

**Weekly automated report (n8n cron, Mondays 9 AM):**
- Model accuracy this week vs 4-week rolling average
- Score distribution changes
- False negatives and false positives identified
- Criteria contribution analysis (which scoring dimensions are most predictive)
- Drift status: Healthy / Degrading / Broken

**Drift alerts:**
- Amber: Hot conversion drops below 3x Cold for 1 week (flag for review)
- Red: Hot conversion drops below 2x Cold for 2+ weeks (trigger autonomous optimization)

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with the lead scoring system as the target play. Configure the 5-phase loop:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the scoring model's primary KPI: Hot-tier conversion rate
2. Compare last 2 weeks against 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If normal: log to Attio, continue monitoring
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull 8-week scoring metric history from PostHog
2. Pull current scoring model configuration from Attio (criteria, weights, thresholds)
3. Run `hypothesis-generation` with anomaly data + model config. Example hypotheses:
   - "Reduce pricing_page_viewed weight from 10 to 5 points — recent bot traffic inflating intent scores"
   - "Add 'contract_renewal_window' as a new intent signal — 3 recent closed-won deals had expiring competitor contracts"
   - "Increase company_size weight from 10 to 15 points — small companies (<20 employees) producing 80% of false positives"
4. Store 3 ranked hypotheses in Attio with risk levels
5. If top hypothesis is high-risk: send Slack alert for human review, STOP
6. If low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Use `posthog-experiments` to create a feature flag splitting new leads between:
   - Control (A): current scoring model weights
   - Variant (B): modified weights per the hypothesis
2. Both groups get scored and routed. Track conversion by tier separately for A and B.
3. Minimum experiment duration: 14 days or 50+ leads scored per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` to compare control vs variant:
   - **Adopt:** Variant improves Hot/Cold conversion ratio by >=10% with confidence >=0.9. Update all scoring weights to variant values. Log the change.
   - **Iterate:** Improvement <10% or confidence 0.7-0.9. Generate a refined hypothesis and return to Phase 2.
   - **Revert:** Variant performed worse. Disable variant, restore control. Log failure. Return to Phase 1.
   - **Extend:** Insufficient sample size. Keep running for another 14 days.
3. Store full evaluation in Attio: decision, confidence, primary lift, secondary impact

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity for the week: anomalies detected, hypotheses generated, experiments running, decisions made
2. Calculate net impact: how much has the scoring model improved since the last report?
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on Hot/Cold conversion ratio
   - Current distance from estimated local maximum
   - Active experiments and expected completion dates
   - Recommended focus for next week
4. Post brief to Slack, store in Attio

### 3. Configure scoring-specific optimization targets

The autonomous optimization loop needs play-specific targets for the lead scoring system:

**Primary metric:** Hot-tier meeting conversion rate / Cold-tier meeting conversion rate (target: >=4x, local maximum TBD)

**Experiment variables the agent can modify:**
- Point values for any fit or intent criterion (within +/-50% of current value)
- Tier thresholds (Hot cutoff between 70-90, Warm floor between 40-60)
- Score decay rate (between 25%-75% reduction per 14-day period)
- Score decay timing (between 7-30 days of inactivity)
- Addition of new intent signals from Clay enrichment columns
- Removal of criteria that contribute <2% to predictive accuracy

**Variables requiring human approval:**
- Adding or removing entire scoring dimensions (fit vs intent weighting)
- Changing routing SLAs (contacting Hot leads within 4 hours is a human capacity constraint)
- Model architecture changes (e.g., switching from additive to multiplicative scoring)

### 4. Deploy closed-deal feedback loop

Build an n8n workflow triggered by `deal_won` and `deal_lost` events in Attio:

**On deal_won:**
1. Pull the lead's original scoring data (fit_score, intent_score, lead_score, lead_tier at time of first scoring)
2. Pull the deal's properties: deal value, time to close, products purchased
3. Store as a `scoring_feedback_positive` event in PostHog
4. If the lead scored Cold or Warm at first scoring, flag as a learning opportunity — what signals emerged after scoring that the model should have captured earlier?

**On deal_lost:**
1. Pull original scoring data
2. Pull loss reason from Attio
3. Store as a `scoring_feedback_negative` event in PostHog
4. If the lead scored Hot at first scoring, flag as a false positive learning — what inflated the score?

This feedback data feeds directly into the hypothesis generation in Phase 2.

### 5. Implement market adaptation monitoring

Build an n8n workflow that runs monthly:

1. Query PostHog for the last 90 days of `scoring_feedback_positive` events
2. Cluster won deals by fit profile (company size, industry, role)
3. Compare this month's won-deal profile to last quarter's
4. If the profile is shifting (e.g., different industries converting, different company sizes winning), flag for the agent: "Market shift detected — won-deal profile changing. Consider re-weighting fit criteria."
5. Feed the shift data into the next Phase 2 hypothesis generation cycle

### 6. Track convergence

The optimization loop runs until convergence:

- After each experiment, log the % improvement (positive or negative) in the primary metric
- Track a rolling window of the last 3 experiments
- **Convergence reached** when 3 consecutive experiments produce <2% improvement
- At convergence:
  1. Reduce monitoring from daily to weekly
  2. Reduce experiment cadence from continuous to monthly spot-checks
  3. Generate a convergence report: "Lead scoring model has reached its local maximum. Current Hot/Cold ratio: {X}x. Further gains require strategic changes (new channels, new ICP segments, product changes)."
  4. Post convergence report to Slack, store in Attio

### 7. Ongoing evaluation

This level runs continuously for 6+ months. Monthly check:
- Is Hot/Cold conversion ratio still >=4x? If not, the agent should already be addressing it via the optimization loop.
- Is experiment win rate >30%? If not, the model may be near convergence.
- Has the agent flagged any market adaptation needs?
- Review the weekly optimization briefs for any patterns the agent cannot address (product changes, competitor moves, market shifts that require strategic decisions).

**Human action required:** Review weekly optimization briefs. Approve high-risk experiments. Make strategic decisions the agent flags but cannot execute (ICP changes, new channel launches, pricing changes).

## Time Estimate

- Performance monitor setup: 10 hours
- Autonomous optimization loop configuration: 15 hours
- Scoring-specific optimization targets: 5 hours
- Closed-deal feedback loop: 8 hours
- Market adaptation monitoring: 5 hours
- Weekly brief review (24 weeks): 24 hours (1 hr/week)
- Experiment design and review: 30 hours
- Monthly calibration reviews: 18 hours (3 hrs/month)
- Convergence analysis: 5 hours
- Buffer for iteration: 10 hours
- Total: ~130 hours over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Attio | CRM — scoring fields, deal feedback, experiment logs | Standard stack (excluded) |
| PostHog | Analytics — funnels, experiments, anomaly detection, dashboards | Standard stack (excluded) |
| n8n | Automation — optimization loop, monitoring, decay, feedback workflows | Standard stack (excluded) |
| Clay | Enrichment — intent signals, new criteria testing | Explorer: $314/mo for 120K credits/year ([clay.com/pricing](https://www.clay.com/pricing)) |
| Instantly | Cold email — outreach at scale | Hypergrowth: $97/mo for 100K emails ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Anthropic API | AI — hypothesis generation, experiment evaluation | Sonnet 4.6: $3/$15 per M tokens; ~$10-30/mo at weekly cadence ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |

**Play-specific cost: ~$430-460/mo** (Clay Explorer + Instantly Hypergrowth + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs
- `scoring-model-performance-monitor` — builds the accuracy dashboard, weekly reports, drift detection, and criteria contribution analysis specific to lead scoring
