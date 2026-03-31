---
name: usage-monitoring-alerts-scalable
description: >
  Usage Drop Alerting — Scalable Automation. Scale detection to segment-specific thresholds,
  multi-step re-engagement sequences, and A/B tested interventions across the full user base.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Scalable Automation"
time: "50 hours over 2 months"
outcome: "≥35% re-engagement rate sustained at 500+ flagged accounts/month with intervention type optimized per segment"
kpis: ["Monthly flagged accounts processed", "Re-engagement rate by segment", "Best intervention type per segment", "Net churn reduction vs. pre-play baseline", "Cost per save"]
slug: "usage-monitoring-alerts"
install: "npx gtm-skills add product/retain/usage-monitoring-alerts"
drills:
  - ab-test-orchestrator
  - churn-prevention
  - engagement-alert-routing
  - usage-drop-detection
---

# Usage Drop Alerting — Scalable Automation

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Scale the detection and intervention system to handle hundreds of flagged accounts per month without proportional effort. The 10x multiplier comes from three sources: segment-specific detection thresholds that reduce false positives, multi-step re-engagement sequences that persist past the first touchpoint, and A/B tested interventions that improve conversion rates per segment.

## Leading Indicators

- False positive rate drops below 15% (from segment-specific thresholds)
- Multi-step sequences convert accounts that single-touch interventions missed
- A/B tests produce statistically significant winners for at least 2 segments
- Human intervention needed for fewer than 10% of flagged accounts
- Net churn rate decreases measurably compared to pre-play baseline

## Instructions

### 1. Segment detection thresholds

The Baseline system used a single -30% threshold for everyone. At scale, this creates noise — a power user dropping from 100 to 65 actions/week is different from a light user dropping from 5 to 3.

Extend the `usage-drop-detection` drill with segment-specific thresholds:

**By usage tier:**
- Power users (top 20% by activity): Flag at -25% drop — these users churn fastest
- Standard users (middle 60%): Flag at -40% drop — some variation is normal
- Light users (bottom 20%): Flag at -60% drop — they were barely active, small drops are noise

**By plan tier:**
- Enterprise/Pro: Flag at -20% — high value, intervene early
- Starter: Flag at -35% — standard sensitivity
- Free: Flag at -50% — only intervene on dramatic drops

**By account age:**
- Under 30 days: Use the `churn-prevention` drill instead — these are onboarding problems, not engagement drops
- 30-90 days: Flag at -30% — still establishing habits
- 90+ days: Flag at -40% — established users have more natural variation

Update the n8n detection workflow to apply segment-specific thresholds. Store the applicable threshold alongside each detection event.

### 2. Build multi-step re-engagement sequences

Extend the `engagement-alert-routing` drill's single-touch interventions into multi-step sequences:

**Alert tier sequence (7 days):**
- Day 0: In-app message on next login + email (gentle template)
- Day 3: If no re-engagement → second email with product updates relevant to their feature usage
- Day 7: If still no re-engagement → email from account owner (or founder for high-value) with direct question

**Critical tier sequence (5 days, faster cadence):**
- Day 0: In-app message + urgent email + Attio task for human review
- Day 2: If no re-engagement → second email with "what changed?" framing
- Day 5: If still no re-engagement → escalate to personal call attempt via Attio task

Configure these in Loops as sequences with skip conditions: if the user re-engages (fires a core engagement event in PostHog), immediately exit the sequence and fire `engagement_intervention_converted`.

### 3. Run A/B tests on interventions

Run the `ab-test-orchestrator` drill to test intervention variations. Run one test at a time, minimum 100 accounts per variant, 2 weeks per test.

**Test 1: Email subject lines**
- Control: "Need a hand with {{productName}}?"
- Variant A: "{{firstName}}, your {{featureName}} data is waiting"
- Variant B: "Quick question about your {{productName}} account"
- Metric: email open rate + re-engagement within 14 days

**Test 2: In-app message placement**
- Control: Banner at top of dashboard
- Variant A: Tooltip on the feature they used most
- Variant B: Chat-style message in Intercom Messenger
- Metric: message engagement rate + re-engagement within 7 days

**Test 3: Intervention timing**
- Control: Same day as detection (Day 0)
- Variant A: 48 hours after detection (give natural recovery time)
- Variant B: Only after 2 consecutive weekly drops (higher confidence)
- Metric: re-engagement rate + false positive rate

Implement winners permanently after each test.

### 4. Integrate with churn prevention

Run the `churn-prevention` drill to layer additional churn signals on top of engagement drops. When an account has both engagement drops AND other churn signals (billing page visits, support ticket spikes, team member removals), classify them as "multi-signal critical" — these accounts get the highest-priority intervention regardless of MRR.

Build a composite risk score in Attio:
- Engagement drop alone: risk_score += 30
- Engagement drop + support tickets: risk_score += 50
- Engagement drop + billing page visit: risk_score += 70
- Engagement drop + team shrinkage: risk_score += 60

Accounts with risk_score > 80 get immediate human outreach.

### 5. Build scaling metrics dashboard

Create a PostHog dashboard tracking the full system at scale:

| Panel | Metric | Purpose |
|-------|--------|---------|
| Monthly flagged accounts | Count by tier | Volume trend |
| Re-engagement rate by segment | % by plan, usage tier, age | Find best/worst segments |
| Intervention conversion by type | % by email, in-app, human | Find best channel |
| Time to re-engage | Median days by intervention type | Speed of recovery |
| False positive rate | % by segment | Threshold calibration |
| Net churn impact | Churn rate now vs. pre-play baseline | Business impact |
| Cost per save | Total intervention cost / saves | Unit economics |

### 6. Evaluate against threshold

Measure against: **≥35% re-engagement rate sustained at 500+ flagged accounts/month with intervention type optimized per segment.**

If PASS: Move to Durable. The system handles volume and produces consistent results.

If FAIL: Focus on the weakest segment. If a specific plan tier or usage tier has low re-engagement, that segment may need a different intervention approach entirely (e.g., product changes, not just messaging).

## Time Estimate

- 10 hours: Implement segment-specific detection thresholds
- 12 hours: Build multi-step re-engagement sequences in Loops
- 15 hours: Run 3 A/B tests (design, implement, monitor, analyze)
- 8 hours: Integrate with churn prevention signals, build composite scoring
- 5 hours: Build dashboard, evaluate results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Segmented detection queries, A/B test infrastructure, dashboards | Free up to 1M events/mo; Growth from $0.00045/event; https://posthog.com/pricing |
| n8n | Segment-specific detection workflows, routing logic | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Loops | Multi-step re-engagement sequences, A/B email variants | Starter from $49/mo at scale; https://loops.so/pricing |
| Intercom | In-app message variants for A/B testing | Starter from $39/mo; https://www.intercom.com/pricing |
| Attio | Composite risk scoring, human routing | Free for small teams; Pro from $34/seat/mo; https://attio.com/pricing |

## Drills Referenced

- `ab-test-orchestrator` — A/B test email subjects, in-app placements, and intervention timing
- `churn-prevention` — Layer additional churn signals for composite risk scoring
- `engagement-alert-routing` — Extend to multi-step sequences and segment-specific routing
- `usage-drop-detection` — Upgrade to segment-specific thresholds
