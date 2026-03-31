---
name: outbound-with-value-asset-durable
description: >
  Outbound With Value Asset — Durable Intelligence. Deploy autonomous optimization
  that continuously monitors, diagnoses, experiments, and adapts the asset-led
  outbound play to find and maintain its local maximum performance.
stage: "Marketing > ProblemAware"
motion: "OutboundFounderLed"
channels: "Email"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Reply rate and meeting rate sustained at or above Scalable baseline for 6 months; autonomous optimization loop running with <=2% improvement between successive experiments (convergence reached)"
kpis: ["Reply rate", "Asset-referencing reply rate", "Meeting rate", "Cost per meeting", "Experiment win rate", "Pipeline value sourced"]
slug: "outbound-with-value-asset"
install: "npx gtm-skills add marketing/problem-aware/outbound-with-value-asset"
drills:
  - autonomous-optimization
  - value-asset-performance-monitor
  - signal-detection
---

# Outbound With Value Asset — Durable Intelligence

> **Stage:** Marketing > ProblemAware | **Motion:** OutboundFounderLed | **Channels:** Email

## Outcomes

Durable is where the play runs itself. An always-on AI agent loop monitors metrics, detects anomalies, generates improvement hypotheses, runs experiments, evaluates results, and auto-implements winners. The goal is not just maintaining performance — it is finding the local maximum and staying there as the market shifts.

**Pass threshold:** Reply rate and meeting rate sustained at or above the Scalable-level baseline for 6 continuous months. The autonomous optimization loop has run at least 12 experiments and reached convergence (successive experiments produce <2% improvement).

## Leading Indicators

- Anomaly detection catches metric changes within 24 hours
- Hypothesis generation produces actionable experiments (not vague suggestions)
- At least 2 out of every 4 experiments produce positive results
- Weekly optimization briefs generate no "critical" alerts for 4+ consecutive weeks
- Cost per meeting trends flat or downward over 3+ months
- Pipeline value from this play grows quarter-over-quarter
- Asset library grows to 3+ assets with data-driven routing

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill. This creates the core agent loop:

**Monitor (daily via n8n cron):**
The optimization agent checks all play KPIs against the 4-week rolling average using PostHog anomaly detection. It classifies the current state:
- **Normal** (within +/-10%): No action. Log to Attio.
- **Plateau** (+/-2% for 3+ weeks): Trigger hypothesis generation. The play has stopped improving.
- **Drop** (>20% decline): Urgent. Trigger hypothesis generation with high priority.
- **Spike** (>50% increase): Investigate cause. If attributable, document and replicate.

**Diagnose (triggered by anomaly):**
The agent pulls 8 weeks of PostHog data plus the play's current configuration from Attio (active asset versions, segments, sequence variants, send timing). It runs Claude to generate 3 ranked hypotheses for what to change. Each hypothesis includes expected impact and risk level.

- Low/medium risk hypotheses proceed automatically to experiment
- High risk hypotheses (budget changes >20%, audience changes >50%) trigger a Slack alert for human review

**Experiment (triggered by hypothesis acceptance):**
The agent creates a PostHog experiment with feature flag to split traffic between control and variant. It implements the variant using the appropriate tool (Instantly for email copy, Clay for targeting, n8n for timing). Minimum experiment duration: 7 days or 100 samples per variant.

**Evaluate (triggered by experiment completion):**
The agent pulls results, runs statistical evaluation, and decides:
- **Adopt:** Implement the winner permanently. Log the change.
- **Iterate:** Generate a follow-on hypothesis. Return to Diagnose.
- **Revert:** Roll back. Log the failure. Return to Monitor.

**Report (weekly via n8n cron):**
Generate a weekly optimization brief summarizing: anomalies detected, experiments run, decisions made, net KPI impact, and recommended focus areas.

### 2. Deploy the performance monitoring layer

Run the `value-asset-performance-monitor` drill. This builds:

- **Master dashboard** in PostHog with 6 panels: weekly funnel trend, click-through rate, asset-referencing reply rate, reply sentiment breakdown, meeting rate by segment, and cost per meeting.
- **Automated anomaly alerts** for: reply rate drops, deliverability decay, negative reply spikes, and click-through anomalies.
- **Weekly AI-generated briefs** posted to Slack every Monday: headline verdict, what changed, recommended actions.
- **Monthly attribution reports** tracking: total meetings, pipeline value, win rate, deal size, and velocity from this play vs. other sources.

The performance monitor feeds data into the autonomous optimization loop. When the monitor detects an anomaly, the optimizer generates a hypothesis and runs an experiment.

### 3. Deploy signal-triggered outreach

Run the `signal-detection` drill to configure always-on buying signal monitoring:

- **Job changes:** New VP/C-level hire at target accounts (via Clay + LinkedIn monitoring). When detected, auto-assign the most relevant asset and add to the next outreach batch with a personalized opening referencing their new role.
- **Funding events:** Series A/B/C closed in last 90 days. Asset framing shifts to "here is how to spend that money wisely on [topic]."
- **Hiring signals:** 3+ open roles in your product's domain. Asset framing shifts to "before you build the team, here is what the top teams do differently."
- **Content signals:** Prospect published or engaged with content about your domain on LinkedIn. Asset framing references their specific interest.

Signal-triggered prospects skip the generic sequence — each gets a custom Email 1 that references their signal plus the asset. Emails 2-3 follow the standard cadence.

### 4. Establish guardrails for autonomous operation

**Critical guardrails that the agent must never override:**

- Maximum 1 active experiment per play at any time. Never stack experiments.
- If primary metric drops >30% during any experiment, auto-revert immediately.
- Human approval required for: budget changes >20%, audience targeting changes affecting >50% of traffic, any hypothesis flagged as high risk.
- Cooldown: after a failed experiment (revert), wait 7 days before testing the same variable.
- Maximum 4 experiments per month. If all 4 fail, pause optimization and alert the founder for strategic review.
- Never send more than 50 emails/day per sending account.
- Total outreach volume never exceeds 150% of last month's volume without human approval.

### 5. Monitor for convergence

The autonomous loop runs indefinitely. Watch for convergence signals:

- 3 consecutive experiments produce <2% improvement on the primary metric
- Weekly optimization briefs show "no anomalies" for 4+ consecutive weeks
- Cost per meeting has been flat (+/-5%) for 8+ weeks

At convergence:
1. The play has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Reduce experiment frequency from 4/month to 1/month (maintenance mode)
4. Report to the team: "This play is optimized at [current metrics]. Further gains require strategic changes — new asset topics, new ICP segments, or new channels — not tactical optimization."

The agent continues monitoring to detect market shifts (competitor launches, industry changes, seasonal patterns) that may disrupt convergence and require a new optimization cycle.

## Time Estimate

- Autonomous optimization setup: 10 hours
- Performance monitor setup: 8 hours
- Signal detection configuration: 6 hours
- Guardrail implementation: 4 hours
- Monthly review and adjustment (4 hrs/month x 6 months): 24 hours
- Experiment review and human approvals (2 hrs/month x 6 months): 12 hours
- Quarterly strategic reviews (3 hrs x 2): 6 hours
- Asset library expansion (5 hrs/quarter x 2): 10 hours
- **Total: ~80 hours over 6 months** (front-loaded: 28 hours in month 1, then ~10 hrs/month)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Instantly | Cold email at scale | Hypergrowth: $78/mo annual ([instantly.ai/pricing](https://instantly.ai/pricing)) |
| Clay | Enrichment, signals, and segmentation | Growth: $495/mo — CRM integrations, higher volume ([clay.com/pricing](https://www.clay.com/pricing)) |
| Apollo | Prospect sourcing | Basic: $49/user/mo ([apollo.io/pricing](https://www.apollo.io/pricing)) |
| Attio | CRM, pipeline tracking, experiment logging | Pro: $59/user/mo — advanced permissions ([attio.com](https://attio.com)) |
| PostHog | Analytics, experiments, anomaly detection | Free tier up to 1M events; ~$50/mo for 2M events ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Automation (optimization loop, monitoring, signals) | Pro: ~$60/mo — 10,000 executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, briefs, evaluation | ~$10-20/mo for weekly optimization cycles ([anthropic.com](https://www.anthropic.com)) |

**Estimated monthly cost: ~$800-900/mo** (Clay Growth + Instantly Hypergrowth + Apollo + Attio Pro + PostHog + n8n Pro + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-report loop that finds the local maximum
- `value-asset-performance-monitor` — dashboard, anomaly detection, weekly briefs, and pipeline attribution
- `signal-detection` — always-on buying signal monitoring that triggers personalized asset outreach
