---
name: co-marketing-shoutouts-durable
description: >
  Partner Newsletter Shoutout — Durable Intelligence. Always-on AI agents monitor
  per-partner performance, generate optimization hypotheses, run blurb A/B tests,
  and auto-implement winners. Weekly optimization briefs. Converges when successive
  experiments produce <2% improvement.
stage: "Marketing > Problem Aware"
motion: "Partnerships & Warm Intros"
channels: "Email"
level: "Durable Intelligence"
time: "200 hours over 6 months"
outcome: "Sustained or improving click and lead volume over 6 months; click-to-lead conversion at or above Scalable peak; agents detect partner fatigue, blurb decay, and seasonal patterns, adapting automatically."
kpis: ["Impressions", "Click-through rate", "Leads per partner", "Click-to-lead conversion rate", "Partner retention rate", "Experiment win rate"]
slug: "co-marketing-shoutouts"
install: "npx gtm-skills add marketing/problem-aware/co-marketing-shoutouts"
drills:
  - autonomous-optimization
  - partner-performance-reporting
---

# Partner Newsletter Shoutout — Durable Intelligence

> **Stage:** Marketing → Problem Aware | **Motion:** Partnerships & Warm Intros | **Channels:** Email

## Outcomes

An always-on optimization system that manages the co-marketing partner portfolio autonomously. The `autonomous-optimization` drill runs the core loop: detect metric anomalies across partners and blurbs, generate improvement hypotheses, run A/B experiments on blurb copy and landing pages, evaluate results, and auto-implement winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement — the play has reached its local maximum.

Sustained or improving click and lead volume over 6 months. Click-to-lead conversion rate at or above the Scalable peak. The agent detects and adapts to partner fatigue (declining clicks from a partner's audience over repeated placements), blurb decay (a once-effective copy angle losing impact), and seasonal patterns (conference season, holiday lulls).

## Leading Indicators

- Anomaly detection fires within 24 hours of a metric shift (signal: monitoring is working)
- At least 1 experiment runs per 2-week period (signal: optimization loop is active)
- Experiment win rate ≥30% (signal: hypotheses are well-targeted)
- No partner drops below 50% of their historical average for 3+ consecutive placements without a corrective action firing (signal: partner fatigue detection works)
- Weekly optimization brief posts on time every Friday (signal: reporting pipeline is stable)
- Time between anomaly detection and experiment launch <72 hours (signal: the loop is tight)

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific metrics and levers:

**Monitor phase (daily via n8n cron):**
- Pull co-marketing KPIs from PostHog: clicks, leads, click-to-lead CVR, per-partner performance
- Compare last 2 weeks against 4-week rolling average
- Classify each metric as: normal (±10%), plateau (±2% for 3+ weeks), drop (>20% decline), or spike (>50% increase)
- Per-partner anomaly detection: flag any partner whose clicks dropped >30% from their rolling average
- If anomaly detected, trigger the Diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather context: which partners are affected, which blurb variants were used, when was the last placement, what is the partner's historical trend
- Pull 8-week per-partner metric history from PostHog
- Run hypothesis generation with the anomaly data. Common hypotheses for this play:
  - "Partner X's audience is fatigued — same audience seeing similar blurbs for 3+ months"
  - "Blurb variant Y has decayed — CTR dropped 40% over 4 placements"
  - "Landing page conversion dropped — A/B test a new headline or CTA"
  - "Partner Z's newsletter engagement is declining overall — not specific to our blurb"
  - "Seasonal effect — conference season / holiday lull affecting email open rates"
- Store hypotheses in Attio. If risk = "high" (e.g., changing the landing page for all traffic), alert for human review.

**Experiment phase (triggered by hypothesis acceptance):**
- Design the experiment. For this play, the primary experiment types are:
  1. **Blurb A/B test**: Send variant A to half the partner portfolio, variant B to the other half. Measure click-to-lead CVR per variant after 2 weeks.
  2. **Landing page A/B test**: Use PostHog feature flags to show different landing page variants to co-marketing traffic. Measure conversion rate per variant.
  3. **Placement timing test**: Test different days/positions in partner newsletters across similar partners.
  4. **Partner rotation test**: Replace an underperforming partner with a new prospect and compare results.
- Use PostHog experiments for landing page and CTA tests. For blurb tests, track by `utm_content` variant.
- Minimum experiment duration: 7 days or 50+ clicks per variant, whichever is longer.

**Evaluate phase (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation:
  - **Adopt**: Winning variant becomes the new default. Update blurb templates or landing page. Log the change.
  - **Iterate**: Result was inconclusive or showed a promising direction. Generate a refined hypothesis and re-test.
  - **Revert**: Variant performed worse. Restore the control. Wait 7 days before testing the same variable.
- Store the full evaluation in Attio with decision, confidence, and reasoning.

**Report phase (weekly, Friday 3pm via n8n cron):**
- Aggregate all optimization activity for the week
- Calculate net metric change from adopted experiments
- Generate the weekly optimization brief (see step 2)

### 2. Deploy play-specific monitoring and reporting

Run the `partner-performance-reporting` drill to build the monitoring layer specific to this play:

**Partnership dashboard in PostHog:**
- Clicks by partner (bar chart, last 30 days)
- Leads by partner (bar chart, last 30 days)
- Click-to-lead CVR by partner (table, sorted descending)
- Clicks over time (trend line, last 90 days)
- Blurb variant performance (table, clicks and leads by utm_content)
- Landing page conversion funnel for co-marketing traffic

**Weekly partnership brief (automated, Friday 3pm):**
```
## Co-Marketing Weekly Brief — {date}

**This week**: {total_clicks} clicks, {total_leads} leads ({cvr}% CVR)
**vs 4-week avg**: {change_pct}% {up/down}
**Active experiments**: {count} ({status summary})

### Top partners
1. {partner_1}: {clicks} clicks, {leads} leads
2. {partner_2}: {clicks} clicks, {leads} leads

### Anomalies detected
- {partner/metric}: {description} — {hypothesis generated}

### Experiments this week
- {experiment}: {status} — {result or ETA}

### Adopted changes
- {change}: {impact on metrics}

### Convergence status
{distance from local maximum estimate}
{recommended focus for next week}
```

**Per-partner ROI tracking in Attio:**
- Total placements, clicks, leads, cost per lead, best blurb variant, partner health score
- Updated weekly by n8n automation

**Performance alerts:**
- Partner clicks drop >50% week-over-week → investigate in Slack
- New partner's first placement exceeds 50 clicks → flag for fast-track repeat
- Total leads drop below Scalable baseline for 2 consecutive weeks → trigger autonomous optimization investigation
- Blurb variant achieves >5% CTR → mark as "proven template"

### 3. Manage partner portfolio health

The agent autonomously manages the partner portfolio:

- **Partner fatigue detection**: If a partner's click rate declines for 3 consecutive placements, the agent pauses placements with that partner for 4 weeks (cooldown period). After cooldown, test with a completely new blurb angle.
- **Partner graduation**: Partners consistently generating >10 leads/month get escalated to deeper partnerships (joint webinars, content collaborations, referral agreements). Log the recommendation in Attio for human review.
- **Partner replacement**: When a partner is retired (fatigue, declining newsletter, or low ROI), the agent triggers the `partner-prospect-research` drill to source a replacement candidate from the pipeline.
- **Seasonal adjustment**: The agent learns seasonal patterns (e.g., lower engagement in December, higher in January/September) and adjusts placement cadence accordingly rather than flagging expected dips as anomalies.

### 4. Guardrails

- **Maximum 1 active experiment at a time.** Never stack blurb tests with landing page tests simultaneously.
- **Revert threshold**: If total clicks drop >30% during an experiment, auto-revert immediately.
- **Human approval required for**: Partner fees or budget changes, landing page changes affecting non-co-marketing traffic, retiring a partner that generates >20% of total leads.
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable.
- **Maximum 4 experiments per month.** If all 4 fail, pause optimization and flag for human strategic review.
- **Never retire more than 2 partners in the same month** without human approval (prevents portfolio collapse).

### 5. Convergence detection

The optimization loop runs continuously. It detects convergence when:
- 3 consecutive experiments produce <2% improvement in the primary metric (clicks or leads)
- The play has reached its local maximum

At convergence:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment frequency to 1 per month (maintenance mode)
3. Report: "Co-marketing shoutouts has converged. Current performance: {metrics}. Further gains require strategic changes (new partner categories, different offer types, new channels) rather than tactical blurb/landing page optimization."

## Time Estimate

- Autonomous optimization setup: 20 hours
- Partner performance reporting setup: 10 hours
- Initial monitoring and tuning (month 1): 20 hours
- Ongoing oversight (months 2-6, ~6 hours/month): 30 hours
- Experiment design and evaluation: 40 hours
- Partner portfolio management: 30 hours
- Strategic reviews and course corrections: 50 hours

Total: ~200 hours over 6 months (heavily front-loaded; agent handles most ongoing work)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Analytics, experiments, anomaly detection, dashboards | Free up to 1M events; paid from $0.00031/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop orchestration, scheduling, alerts | Cloud Pro: ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Partner CRM, experiment logs, ROI tracking | Plus: $34/user/mo ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude | Hypothesis generation, experiment evaluation, briefs | API: ~$15-30/mo at this usage level ([anthropic.com/pricing](https://anthropic.com/pricing)) |
| Crossbeam | Partner account overlap (ongoing) | Free tier for basic use; Connector from $400/mo ([crossbeam.com](https://www.crossbeam.com)) |

**Estimated cost for this level: ~$110-330/mo** (n8n Pro + Attio + Anthropic API required; Crossbeam and PostHog within free tiers for most usage)

## Drills Referenced

- `autonomous-optimization` — the core monitor → diagnose → experiment → evaluate → implement loop that finds the local maximum
- `partner-performance-reporting` — per-partner dashboards, weekly briefs, ROI tracking, and alerts specific to this play
