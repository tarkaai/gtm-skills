---
name: net-retention-optimization-scalable
description: >
  Net Retention Optimization — Scalable. Build segment-level NDR tracking, deploy composite
  health scores, run systematic A/B tests on retention and expansion tactics, and
  scale interventions across all customer segments.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "NDR >=110% sustained for 4+ consecutive weeks"
kpis: ["Net dollar retention", "Gross retention rate", "Churn save rate", "Expansion conversion rate", "Health score accuracy", "Experiment win rate"]
slug: "net-retention-optimization"
install: "npx gtm-skills add product/retain/net-retention-optimization"
drills:
  - ndr-cohort-tracking
  - health-score-model-design
  - health-score-alerting
  - ab-test-orchestrator
---

# Net Retention Optimization — Scalable Automation

> **Stage:** Product -> Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Find the 10x multiplier. Move from individual interventions to systematic, segment-level NDR optimization. Deploy composite health scores that predict churn and expansion at the account level, build always-on NDR dashboards that decompose performance by cohort and segment, and run A/B tests to find the highest-impact retention and expansion tactics. Scale interventions across all customer segments without proportional manual effort.

The pass threshold is NDR >=110% sustained for 4+ consecutive weeks. This proves the system works at scale, not just with a few accounts.

## Leading Indicators

- NDR dashboard shows all 6 panels with live data updating weekly
- Health scores compute daily for all accounts with risk level distribution matching intuition (not all in one tier)
- Health-based interventions fire automatically for all tier transitions (not just critical)
- At least 2 A/B tests completed with statistically significant results
- Save rate on health-based interventions exceeds 25% across all tiers

## Instructions

### 1. Deploy segment-level NDR tracking

Run the `ndr-cohort-tracking` drill to build always-on NDR monitoring. This creates:

1. A PostHog dashboard with 6 panels: NDR trend, NDR decomposition, NDR by signup cohort (heatmap), NDR by plan tier, expansion funnel, and churn reason distribution
2. A weekly n8n workflow that detects NDR anomalies: churn spikes (weekly churned MRR >150% of 4-week average), contraction surges (>200%), and expansion stalls (<50%)
3. Anomaly diagnostic reports that identify which accounts, cohorts, and segments are driving the anomaly
4. Segment-level early warning cohorts: new accounts (0-90 days), mid-lifecycle (91-365 days), mature (365+), and high-value (top 20% by MRR)
5. A monthly executive NDR report with component trends, cohort performance, and recommended focus areas

Review the dashboard after 2 weeks of data flow. Verify that the NDR numbers match your billing system. Fix any data gaps before proceeding.

### 2. Build composite health scores

Run the `health-score-model-design` drill to create a 4-dimension account health model:

- **Usage (35%):** Weekly active users, session frequency, usage trend, login gap
- **Engagement (25%):** Feature breadth, depth of use, collaboration signals, content consumption
- **Support (20%):** Ticket volume, sentiment, resolution satisfaction, escalation rate
- **Adoption (20%):** Core feature adoption, integration status, team penetration, milestone completion

The drill:
1. Defines scoring functions for each dimension using percentile ranking against your customer base
2. Computes a composite 0-100 health score per account daily via n8n
3. Classifies risk levels: Healthy (80-100), Monitor (60-79), At Risk (40-59), Critical (0-39)
4. Tracks score trends: Improving (+5 pts), Stable, Declining (-5 pts)
5. Back-tests the model against historical churn — target: >70% of churned accounts would have been flagged At Risk or Critical 30 days before churn

**Human action required:** Review the back-test results. If prediction accuracy is below 70%, adjust dimension weights. Common fix: increase the weight of the usage dimension if it correlates most with churn.

### 3. Activate health-score-based interventions

Run the `health-score-alerting` drill to connect health scores to automated actions:

- **Tier 1 (Nudge):** Score drops from Healthy to Monitor, or any dimension drops >15 points in a week. Intercom in-app message targeting the declining dimension.
- **Tier 2 (Outreach):** Score drops to At Risk, or stuck in Monitor for 3+ weeks. Loops email from the account owner with personalized usage data.
- **Tier 3 (Urgent):** Score drops to Critical, or drops >20 points in a single week. Attio task for human outreach within 48 hours.
- **Tier 4 (Expansion):** Score is Healthy AND usage in top 20th percentile AND team penetration >80%. In-app upgrade prompt + Attio expansion flag.

The drill also builds:
- Rate limiting: max 1 in-app/7 days, 1 email/14 days, no limit on urgent, 1 expansion/30 days
- 14-day follow-up tracking: did the account recover, stabilize, continue declining, or churn?
- Weekly intervention summary with recovery rates by tier

### 4. Run systematic A/B tests

Run the `ab-test-orchestrator` drill to test retention and expansion tactics:

**Test 1 — Churn intervention messaging:**
- Hypothesis: "If we include the user's specific declining metric in the intervention message (e.g., 'Your team's usage dropped 40% this week'), save rate will increase by 5+ percentage points vs. generic re-engagement copy, because specific data creates urgency."
- Control: Current intervention message template
- Variant: Message with specific metric data pulled from PostHog
- Metric: 30-day save rate for High/Critical risk accounts

**Test 2 — Expansion prompt timing:**
- Hypothesis: "If we show upgrade prompts immediately when users hit a feature gate (vs. 24 hours later via email), upgrade conversion will increase by 3+ percentage points, because the need is freshest at the moment of the gate."
- Control: Email 24 hours after feature gate hit
- Variant: In-app prompt at the moment of feature gate
- Metric: Upgrade started rate within 7 days

**Test 3 — Contraction prevention:**
- Hypothesis: "If we offer a personalized alternative when a user initiates a downgrade (e.g., a custom plan at a reduced price that keeps their most-used features), contraction MRR will decrease by 20%+ vs. the standard downgrade flow, because users want to pay less, not necessarily lose features."
- Control: Standard downgrade confirmation
- Variant: Personalized alternative plan offer during downgrade flow
- Metric: Contraction MRR and logo retention for downgrade-intent accounts

Run each test for minimum 2 weeks or until 200+ samples per variant, whichever is longer. Do not peek early. Implement winners immediately.

### 5. Evaluate against threshold

At the 2-month mark, compute trailing 4-week NDR from the `ndr-cohort-tracking` dashboard.

If PASS (NDR >=110% for 4+ consecutive weeks): the system is working at scale. Document: which interventions have the highest save rates, which expansion triggers convert best, which A/B test winners were implemented, and which customer segments still lag. Proceed to Durable.
If FAIL: identify the weakest NDR component (churn, contraction, expansion) from the dashboard decomposition. Focus A/B testing on that component. Re-evaluate in 4 weeks.

## Time Estimate

- 12 hours: deploy NDR cohort tracking dashboard and anomaly monitoring
- 12 hours: build and validate composite health score model
- 8 hours: configure health-score-based interventions and rate limiting
- 10 hours: design, launch, and analyze 3 A/B tests
- 8 hours: monitor, tune, and document over weeks 4-8

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | NDR dashboards, health scoring, cohort analysis, A/B experiments | Free up to 1M events/mo; paid from $0.00031/event — [posthog.com/pricing](https://posthog.com/pricing) |
| Intercom | In-app nudges, health-based messages, expansion prompts | From $39/mo (Essential); $99/mo (Advanced) — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Triggered retention and expansion emails | Free up to 1,000 contacts; paid from $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Estimated cost for Scalable: $100-300/mo** (Intercom Advanced for targeting + Loops paid tier for volume)

## Drills Referenced

- `ndr-cohort-tracking` — builds always-on NDR dashboards, anomaly detection, segment-level early warning, and monthly executive reports
- `health-score-model-design` — creates a composite 4-dimension account health score computed daily
- `health-score-alerting` — routes health score transitions to tiered interventions with rate limiting and effectiveness tracking
- `ab-test-orchestrator` — designs, runs, and analyzes A/B tests on retention and expansion tactics
