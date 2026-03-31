---
name: newsletter-sponsorships-durable
description: >
  Newsletter Sponsorship — Durable Intelligence. Autonomous agent-driven optimization
  of the newsletter sponsorship portfolio. The agent monitors placement performance,
  detects anomalies, generates hypotheses, runs experiments, and auto-implements winners
  to find and maintain the local maximum for cost-per-lead.
stage: "Marketing > Problem Aware"
motion: "LightweightPaid"
channels: "Email"
level: "Durable Intelligence"
time: "8 hours/month ongoing"
outcome: "CPL at or below Scalable baseline for 6 consecutive months, with successive optimization experiments producing <2% improvement (convergence reached)"
kpis: ["Blended CPL (rolling 30-day)", "CPL convergence rate", "Newsletter portfolio churn rate", "Optimization experiment win rate", "Total leads per month"]
slug: "newsletter-sponsorships"
install: "npx gtm-skills add marketing/problem-aware/newsletter-sponsorships"
drills:
  - autonomous-optimization
  - newsletter-sponsor-performance-monitor
  - newsletter-sponsor-research
---

# Newsletter Sponsorship — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** LightweightPaid | **Channels:** Email

## Outcomes

The newsletter sponsorship channel runs autonomously with agent-driven optimization. The agent monitors all placement performance, detects when CPL drifts upward or a newsletter's audience fatigues, generates hypotheses for improvement, runs experiments (new blurb angles, new newsletters, adjusted frequency, landing page variants), evaluates results, and auto-implements winners. The goal is to find the local maximum — the best possible CPL given current newsletters, audiences, and competitive landscape — and maintain it as conditions change. Convergence is reached when successive experiments produce less than 2% CPL improvement.

## Leading Indicators

- Anomaly detection triggers within 24 hours of a metric shift (signal: the monitoring loop is responsive)
- At least 2 optimization experiments run per month (signal: the agent is actively seeking improvements)
- Experiment win rate above 30% (signal: hypotheses are well-informed, not random)
- Newsletter portfolio refreshes at least 1 newsletter per quarter (signal: the agent is preventing audience fatigue)
- Weekly optimization briefs are generated on schedule (signal: the reporting loop is reliable)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the newsletter sponsorship play. This is the core of Durable — it creates the always-on monitor, diagnose, experiment, evaluate, implement cycle.

**Phase 1 — Monitor (daily via n8n cron):**
- Query PostHog for the newsletter sponsorship KPIs: blended CPL (rolling 7-day), click volume, lead volume, conversion rate by newsletter
- Compare last 7 days against the 4-week rolling average
- Classify each newsletter as: **normal** (within 10% of average), **plateau** (within 2% for 3+ weeks), **fatiguing** (CPL rising >15%), or **overperforming** (CPL dropping >20%)
- If all newsletters are normal: log to Attio, no action
- If anomaly detected on any newsletter: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull the anomalous newsletter's history: last 8 placements, blurb angles used, click trends, conversion trends
- Pull competitive context: are other sponsors increasing in this newsletter? Has the newsletter changed format?
- Generate 3 hypotheses for the anomaly using Claude:
  - Example: "Audience fatigue — the same readers have seen our blurb 4 times. Hypothesis: rotate to a fresh angle or pause for 4 weeks."
  - Example: "Landing page decay — CTR is stable but conversion dropped. Hypothesis: update the landing page social proof with newer case studies."
  - Example: "Newsletter quality decline — open rates dropping. Hypothesis: replace this newsletter with a higher-performing alternative."
- Store hypotheses in Attio. If the top hypothesis involves budget changes >20% or dropping a Tier 1 newsletter, send a Slack alert for human approval.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Design the experiment based on the hypothesis:
  - **Blurb angle test**: book 2 placements in the same newsletter close together, each with a different angle. Compare CTR and CPL.
  - **Newsletter replacement test**: redirect budget from the fatiguing newsletter to a new test newsletter. Compare CPL over 2 placement cycles.
  - **Frequency test**: change placement frequency (weekly vs. biweekly) and measure CPL impact.
  - **Landing page test**: use PostHog feature flags to show newsletter visitors a variant landing page.
- Set experiment duration: minimum 2 placement cycles or 14 days, whichever is longer.
- Log the experiment in Attio: hypothesis, variant, start date, expected duration, success metric.

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull results from PostHog and compare control vs. variant CPL
- Decision:
  - **Adopt**: Variant CPL is significantly better (>10% improvement with 95% confidence). Update the live configuration. Log the change.
  - **Iterate**: Inconclusive or marginal. Generate a refined hypothesis and return to Phase 2.
  - **Revert**: Variant CPL is worse. Restore the previous configuration. Log the failure with reasoning.
- Store the full evaluation in Attio.

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net CPL change from all adopted changes this week
- Generate a weekly optimization brief:
  - Current blended CPL vs. Scalable baseline
  - Active experiments and their status
  - Newsletter portfolio changes (added, dropped, tier changes)
  - Distance from estimated convergence
  - Recommended focus for next week
- Post to Slack and store in Attio

### 2. Run the newsletter portfolio health monitor

Run the `newsletter-sponsor-performance-monitor` drill on an enhanced cadence for Durable:

- Daily: check for click anomalies (zero clicks from a scheduled placement = investigate immediately)
- Weekly: update newsletter tier assignments based on rolling 30-day CPL
- Monthly: compare portfolio-level metrics against Scalable baseline
- Quarterly: run `newsletter-sponsor-research` to discover new newsletters and retire fatigued ones

Portfolio management rules:
- **Tier 1 rotation**: Even top-performing newsletters should cycle through 4-6 week "rest periods" to prevent audience fatigue. During rest, redirect budget to Tier 2 or test newsletters.
- **Minimum portfolio size**: Maintain at least 6 active newsletters at all times to avoid concentration risk. If fewer than 6 are active, trigger an emergency research cycle.
- **Maximum per-newsletter spend**: No single newsletter should receive more than 25% of total budget. This prevents over-dependence on any one publisher.

### 3. Maintain the autonomous system

**Guardrails (CRITICAL):**
- Maximum 1 active experiment per newsletter at a time. Never stack experiments on the same newsletter.
- If blended CPL exceeds 150% of the Scalable baseline for 2 consecutive weeks, pause all new bookings and trigger a full portfolio review.
- Human approval required for: dropping a Tier 1 newsletter, increasing total monthly budget by >20%, adding a newsletter in a category you have not tested before.
- After a failed experiment, wait 2 placement cycles before testing the same variable on the same newsletter.
- Maximum 4 experiments per month across the portfolio. If all 4 fail, pause optimization and flag for human strategic review.

**Convergence detection:**
When 3 consecutive experiments produce less than 2% CPL improvement:
1. The newsletter sponsorship channel has reached its local maximum
2. Reduce the optimization loop from daily monitoring to weekly
3. Report to the team: "Newsletter sponsorships are optimized. Current CPL is {X}. Monthly lead volume is {Y}. Further gains require strategic changes (new audience segments, product changes, or new adjacent channels) rather than tactical optimization."
4. Continue monitoring for regression — if CPL rises >15% from the converged level, reactivate daily optimization

## Time Estimate

- Autonomous optimization loop maintenance: 2 hours/month (reviewing experiments, approving high-risk changes)
- Portfolio health review: 2 hours/month
- Weekly brief review and strategic decisions: 2 hours/month
- Quarterly newsletter discovery cycle: 2 hours/quarter

Total: ~8 hours/month of human oversight (the agent handles the rest autonomously)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Paved | Newsletter marketplace | Free for advertisers ([paved.com](https://www.paved.com)) |
| Clay | Quarterly newsletter discovery | Launch: $185/mo ([clay.com/pricing](https://www.clay.com/pricing)) |
| Attio | Portfolio CRM, experiment tracking, audit trail | Free up to 3 users ([attio.com/pricing](https://attio.com/pricing)) |
| PostHog | Analytics, experiments, anomaly detection | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop automation, reporting workflows | Free self-hosted; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, blurb iteration | Pay-per-use, ~$10-30/mo ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Newsletter placements | Ongoing portfolio of 10-20 placements/month | $2,000-8,000/mo |

**Estimated cost for this level: $2,400-8,500/mo** (placement spend + small increase in AI compute for optimization)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners
- `newsletter-sponsor-performance-monitor` — enhanced daily/weekly/monthly portfolio monitoring and tier management
- `newsletter-sponsor-research` — quarterly pipeline refresh to discover new newsletters and prevent portfolio stagnation
