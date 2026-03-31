---
name: funnel-optimization-baseline
description: >
  Conversion Funnel Optimization — Baseline Run. First always-on funnel optimization system
  with automated monitoring, feature-flagged A/B tests on top friction points, and
  continuous tracking across signup, activation, and upgrade funnels.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: ">=20% cumulative funnel improvement across all monitored funnels, sustained over 2 weeks with always-on monitoring"
kpis: ["Funnel conversion rate per step", "Drop-off reduction", "Test velocity (experiments per month)", "Monitoring uptime"]
slug: "funnel-optimization"
install: "npx gtm-skills add product/retain/funnel-optimization"
drills:
  - signup-friction-reduction
  - activation-optimization
  - funnel-optimization-health-monitor
  - threshold-engine
---

# Conversion Funnel Optimization — Baseline Run

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Move from a one-time funnel fix to an always-on optimization system. At this level, you instrument all three key funnels (signup, activation, upgrade), deploy friction fixes behind PostHog feature flags for proper A/B testing, set up automated daily monitoring with alerting, and run 2-3 experiments per funnel. The system runs continuously without manual intervention.

**Pass threshold:** >=20% cumulative conversion improvement across all monitored funnels, sustained over 2 weeks with always-on monitoring confirmed operational.

## Leading Indicators

- All 3 funnels (signup, activation, upgrade) instrumented with PostHog events and baseline metrics recorded
- Daily health monitoring workflow running without failures for 7+ consecutive days
- At least 2 A/B experiments deployed behind feature flags with proper control/treatment split
- Intercom help triggers active for users showing friction signals
- Weekly health reports being generated and posted to Slack automatically

## Instructions

### 1. Extend instrumentation to all key funnels

At Smoke you instrumented one funnel. Now instrument the remaining two. For each funnel, repeat the `signup-funnel-audit` drill pattern:

- Define events for every step in the funnel
- Build the PostHog funnel insight
- Record baseline conversion rates with dates
- Identify the primary bottleneck per funnel

Three funnels to have fully instrumented:
1. **Signup funnel:** landing page > form start > form submit > account created > email verified
2. **Activation funnel:** account created > key action 1 > key action 2 > aha moment reached
3. **Upgrade funnel:** feature gate hit > pricing page viewed > checkout started > payment completed

### 2. Deploy friction fixes with feature flags

Run the `signup-friction-reduction` drill for each funnel's primary bottleneck. This deploys fixes behind PostHog feature flags with 50/50 control/treatment splits. Each fix gets:

- A PostHog feature flag gating the change
- Tracking events for the specific fix (so you can measure its individual impact)
- A planned experiment duration (7 days minimum or 200+ users per variant)
- An automated n8n monitor comparing variant conversion rates daily

Prioritize fixes by expected impact. Run no more than 1 experiment per funnel at a time to avoid interaction effects.

### 3. Optimize activation flow

Run the `activation-optimization` drill to find and improve your product's activation metric. This produces:

- A validated activation metric (the action that predicts 30-day retention)
- A measured activation rate with cohort breakdown
- Intercom product tours targeting drop-off points
- n8n workflows nudging inactive users toward activation

The activation funnel optimization is the highest-leverage work at Baseline because activation improvements compound: every additional activated user has higher retention, higher upgrade probability, and higher referral likelihood.

### 4. Set up always-on monitoring

Run the `funnel-optimization-health-monitor` drill. This creates:

- Daily n8n workflow checking all funnel metrics against baselines
- Health classification (healthy/warning/critical) for each funnel step
- Regression detection for trend reversals
- Automated Slack alerts for warnings and criticals
- Weekly health report with cumulative optimization impact

Verify the monitoring is working by checking that the first 3 daily health events appear in PostHog. Confirm the Slack alerts fire by temporarily lowering a threshold.

### 5. Run experiments and evaluate

Over the 2-week Baseline period, run at least 2 experiments per funnel (6 total). For each experiment:

1. Hypothesis documented before launch
2. Feature flag created with 50/50 split
3. Primary metric and sample size defined
4. Results evaluated after reaching sample size or 7 days
5. Winner rolled out to 100% or loser reverted

Track experiment results in Attio. Calculate cumulative impact: sum of all winning experiments' lifts.

### 6. Evaluate against threshold

Run the `threshold-engine` drill: is the cumulative conversion improvement across all funnels >=20%, sustained for 2 weeks with monitoring confirmed operational?

"Cumulative improvement" means: if signup went from 30% to 33% (10% lift), activation from 50% to 58% (16% lift), and upgrade from 8% to 10% (25% lift), the cumulative improvement is the weighted average by traffic volume.

If PASS: Proceed to Scalable. The always-on system is working and producing measurable gains.
If FAIL: Diagnose — is the issue insufficient experiment volume (need more tests), wrong hypotheses (need better diagnosis), or insufficient traffic (need more time)?

## Time Estimate

- 3 hours: Instrument remaining 2 funnels, establish baselines
- 3 hours: Configure feature-flagged friction fixes across all 3 funnels
- 3 hours: Run activation-optimization drill (find metric, build nudges)
- 3 hours: Set up monitoring infrastructure (n8n workflows, dashboard, alerts)
- 2 hours: Run and evaluate experiments over 2 weeks
- 2 hours: Measure cumulative impact, evaluate threshold, document results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Funnel analytics, feature flags, experiments, session recordings | Free tier or Growth from $0 (usage-based) — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Daily monitoring workflows, experiment automation | Starter from EUR36/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Intercom | In-app help triggers for friction signals, product tours | Starter $39/seat/mo — [intercom.com/pricing](https://www.intercom.com/pricing) |
| Loops | Lifecycle emails for activation nudges | Starter from $49/mo — [loops.so/pricing](https://loops.so/pricing) |

**Estimated play-specific cost:** ~$75-175/mo (n8n + Intercom + Loops beyond free tiers)

## Drills Referenced

- `signup-friction-reduction` — Deploys feature-flagged friction fixes with A/B tracking and automated monitoring
- `activation-optimization` — Finds the activation metric, measures it, and systematically improves it
- `funnel-optimization-health-monitor` — Always-on daily monitoring with alerting and weekly health reports
- `threshold-engine` — Evaluates cumulative improvement against the >=20% threshold
