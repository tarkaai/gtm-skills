---
name: multiyear-commitment-durable
description: >
  Multi-Year Deal Incentives — Durable Intelligence. Autonomous agent monitors commitment
  program health, detects anomalies, generates optimization hypotheses, runs experiments,
  and auto-implements winners. Finds and maintains the local maximum for committed ARR
  penetration and retention lift.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Durable Intelligence"
time: "Ongoing — 4 hours/week agent compute + 1 hour/week human review"
outcome: "Committed ARR penetration ≥20% sustained over 6 months; retention lift ≥15pp vs. monthly"
kpis: ["Committed ARR penetration", "Retention lift (committed vs. monthly)", "Offer conversion rate", "Program ROI", "Experiment velocity", "Convergence distance"]
slug: "multiyear-commitment"
install: "npx gtm-skills add product/upsell/multiyear-commitment"
drills:
  - autonomous-optimization
  - commitment-health-monitor
  - pricing-experiment-runner
---

# Multi-Year Deal Incentives — Durable Intelligence

> **Stage:** Product → Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

The commitment program runs on autopilot. An autonomous agent continuously monitors program health, detects when conversion rates plateau or retention lifts erode, generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The agent finds the local maximum — the highest achievable committed ARR penetration and retention lift given the current customer base, pricing, and competitive landscape — and maintains it as conditions change.

Human involvement reduces to weekly review of the optimization brief and approval of high-risk changes (budget shifts >20%, new discount tiers, audience targeting changes affecting >50% of accounts).

## Leading Indicators

- Anomaly detection firing appropriately (not too noisy, not missing real shifts)
- Hypothesis quality: >50% of generated hypotheses produce positive or neutral experiment results
- Experiment throughput: 2-4 experiments per month completing with statistical significance
- Convergence signal: successive experiments producing smaller improvements (<2% for 3+ consecutive tests = approaching local max)
- No manual intervention required for 4+ consecutive weeks (the agent is self-sufficient)

## Instructions

### 1. Deploy the commitment health monitor

Run the `commitment-health-monitor` drill to build the continuous monitoring layer:

1. **PostHog dashboard** with funnel, retention, revenue, and pipeline panels
2. **Anomaly thresholds** for: offer conversion rate drops, committed account churn events, discount-to-retention ratio degradation, Ready-tier volume drops, renewal pipeline gaps, offer dismiss rate spikes
3. **Weekly health report** generated automatically with funnel performance, retention impact, revenue impact, pipeline status, and anomaly alerts
4. **Renewal pipeline tracking** with 90-day advance warning for upcoming commitment renewals
5. **Monthly ROI calculation** that validates the program is generating net positive value (revenue retained > discount cost)

The health monitor feeds anomaly events to the autonomous optimization loop. Every `commitment_anomaly_detected` event becomes an input signal for hypothesis generation.

### 2. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the commitment program. This is the core Durable loop:

**Phase 1 — Monitor (daily):**
The n8n cron workflow checks commitment program KPIs against 4-week rolling averages:
- Offer conversion rate (overall and by channel/segment/tier)
- Committed ARR penetration
- Committed account retention vs. monthly
- Ready-tier population size
- Funnel step conversion rates

Classify each metric: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase). If normal, log and continue. If anomaly detected, trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
Pull 8-week history for the anomalous metric. Gather context: current offer configuration (tier, discount, channels, segments), recent changes, competitive landscape signals. Run `hypothesis-generation`:

Example hypotheses the agent might produce:
- "Conversion rate dropped because the Enhanced tier's priority support perk has not been visibly differentiated. Test adding a 'Priority Support' badge in the product UI for committed accounts."
- "Ready-tier volume is shrinking because the 6-month tenure requirement excludes a growing cohort of fast-adopting 3-month accounts. Test lowering tenure to 4 months with a usage-intensity gate."
- "In-app dismiss rate spiked because the offer modal triggers on every billing page visit. Test limiting to once per 14 days."

Score each hypothesis by expected impact and risk. Store in Attio.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
For the top-ranked low/medium-risk hypothesis:
- Create a PostHog feature flag to split Ready-tier accounts between control and variant
- Implement the variant (adjust Intercom message, modify Loops sequence, change readiness threshold, etc.)
- Set experiment duration: minimum 14 days or 50+ accounts per variant
- Log experiment start in Attio

For pricing-specific hypotheses (new discount levels, new term structures), use the `pricing-experiment-runner` drill which includes additional guardrails for billing changes.

**Phase 4 — Evaluate (triggered by experiment completion):**
Pull experiment results from PostHog. Run `experiment-evaluation`:
- **Adopt:** implement the winning variant for all accounts. Update the live configuration. Log the change.
- **Iterate:** the result was directionally positive but not significant. Generate a refined hypothesis.
- **Revert:** the variant underperformed. Restore control. Log the failure with reasoning.
- **Extend:** insufficient sample size. Continue the experiment for another period.

**Phase 5 — Report (weekly):**
Generate the weekly optimization brief:

```
## Commitment Program Optimization — Week of {date}

### What Changed
- {experiment name}: {result}. {Decision: adopted/reverted/extended}. Impact: {metric change}.

### Current Performance
- Committed ARR penetration: {X}% (target: ≥20%)
- Offer conversion rate: {X}% (4-week avg)
- Retention lift: {X}pp (committed vs. monthly)
- Program ROI: {X}x

### Convergence Status
- Last 3 experiments average improvement: {X}%
- Estimated distance from local maximum: {qualitative assessment}
- {If converged: "Program has reached local maximum. Monitoring only."}

### Next Experiment
- Hypothesis: {description}
- Expected impact: {metric} +{X}%
- Risk: {low/medium}
- Start date: {date}

### Human Review Required
- {List any high-risk hypotheses needing approval}
- {List any anomalies the agent could not diagnose}
```

Post to Slack and store in Attio.

### 3. Manage the renewal optimization sub-loop

The `commitment-health-monitor` drill surfaces accounts approaching commitment renewal. The autonomous agent manages renewals as a secondary optimization target:

1. **90 days before renewal:** score the account's current health. If healthy and usage has grown, prepare an upsell renewal offer (commit at a higher tier or longer term). If health is declining, flag for human intervention.
2. **60 days before renewal:** deliver the renewal offer via the winning channel from Scalable testing. For accounts that expanded, offer rate lock on the higher usage.
3. **30 days before renewal:** if no action taken, escalate. In-app: show a countdown banner. Email: send urgency email. Sales-routed accounts: create a task for the AE.
4. **Track renewal rate:** target >85% of committed accounts renewing their commitment (vs. reverting to monthly).

The agent optimizes renewal timing, messaging, and offer terms the same way it optimizes initial conversion — detect, hypothesize, experiment, evaluate.

### 4. Detect convergence and shift to maintenance

The optimization loop runs until convergence. Convergence is detected when:

- 3 consecutive experiments produce <2% improvement on the primary metric (committed ARR penetration)
- The current performance is within the target range (≥20% penetration, ≥15pp retention lift)
- No anomalies detected for 4+ consecutive weeks

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency from 2-4/month to 1/month (exploratory only)
3. Generate a convergence report: "The commitment program has reached its local maximum. Current committed ARR penetration is {X}%, retention lift is {Y}pp, program ROI is {Z}x. Further gains require strategic changes — new pricing model, new customer segment, or product changes — not tactical optimization."
4. Continue renewal management and anomaly detection at reduced frequency

If conditions change (new competitor, market shift, product launch), the agent detects the disruption via anomaly detection and automatically re-enters the active optimization loop.

### 5. Evaluate sustainability

This level runs continuously. Monthly, verify:

1. Committed ARR penetration ≥20% of total ARR
2. Retention lift ≥15 percentage points (committed vs. monthly accounts)
3. Program ROI > 2.0x (revenue retained exceeds discount cost by 2x)
4. No degradation trend in any primary metric over 3 consecutive months

Pass threshold: **All 4 conditions sustained for 6 consecutive months.**

If any condition degrades for 2+ consecutive months and the autonomous agent has not self-corrected, escalate for human strategic review. The play may need a structural change that optimization cannot solve.

## Time Estimate

- Agent compute: ~4 hours/week (daily monitoring, weekly reporting, experiment management)
- Human review: ~1 hour/week (read optimization brief, approve/reject high-risk hypotheses)
- Experiment setup: automated by the agent
- Monthly: 2 hours for strategic review of convergence status and program ROI

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards | $0.00045/event after 1M; Experiments included |
| Stripe | Subscription management, pricing experiments | 2.9% + $0.30/txn |
| Intercom | In-app offer variants, renewal prompts | Starter $74/mo; https://www.intercom.com/pricing |
| Loops | Email sequence variants, renewal emails | $49/mo for 5K; https://loops.so/pricing |
| n8n | Optimization loop orchestration, cron jobs | Free self-hosted; Cloud from $24/mo; https://n8n.io/pricing |
| Attio | Deal tracking, experiment logging, reporting | $29/seat/mo; https://attio.com/pricing |
| Anthropic API | Hypothesis generation + experiment evaluation | ~$15-30/mo at this experiment volume; https://www.anthropic.com/pricing |

## Drills Referenced

- `autonomous-optimization` — the core optimization loop: monitor → diagnose → experiment → evaluate → implement. Makes Durable fundamentally different from Scalable.
- `commitment-health-monitor` — continuous monitoring layer that feeds anomaly events to the optimization loop and generates weekly health reports
- `pricing-experiment-runner` — manages pricing-specific experiments (new discount tiers, term structures) with Stripe guardrails and auto-revert
