---
name: integration-partnerships-durable
description: >
  Integration Partnerships — Durable Intelligence. Autonomous optimization loop monitors partner
  portfolio health, experiments with co-marketing tactics, and auto-implements winners to sustain
  ≥50 qualified leads/quarter from integration partnerships.
stage: "Marketing > SolutionAware"
motion: "PartnershipsWarmIntros"
channels: "Product, Content, Email"
level: "Durable Intelligence"
time: "180 hours over 12 months"
outcome: "Sustained integration pipeline and ≥50 qualified leads/quarter over 12 months via AI-driven partner prioritization"
kpis: ["Sustained partner-sourced lead volume", "AI experiment win rate", "Partner portfolio ROI", "Integration usage retention", "Co-marketing conversion rate trend"]
slug: "integration-partnerships"
install: "npx gtm-skills add marketing/solution-aware/integration-partnerships"
drills:
  - autonomous-optimization
  - integration-pipeline-health-monitor
  - partner-relationship-scoring
---

# Integration Partnerships — Durable Intelligence

> **Stage:** Marketing → SolutionAware | **Motion:** PartnershipsWarmIntros | **Channels:** Product, Content, Email

## Outcomes

Sustained integration pipeline generating ≥50 qualified leads per quarter over 12 months. An always-on AI agent monitors partner portfolio health, detects when specific partners or co-marketing tactics underperform, generates hypotheses for improvement, runs experiments, and auto-implements winners. The partnership motion reaches its local maximum and maintains it as market conditions change.

## Leading Indicators

- Autonomous optimization loop runs daily without errors
- At least 1 experiment completes per month with a clear adopt/revert decision
- Partner portfolio ROI improves or holds steady quarter over quarter
- No partner drops from "Active" to "Dormant" without the agent detecting and flagging it first
- Weekly optimization briefs consistently surface actionable insights (not just metric dumps)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the integration partnerships play. The agent executes the five-phase loop:

**Monitor (daily):** Check integration partnership KPIs against 4-week rolling averages:
- Total partner-sourced leads this week vs average
- Per-partner activation rates vs per-partner averages
- Integration usage retention (week-over-week active integration users)
- Co-marketing email performance (open rates, click rates per partner campaign)

Classify each metric as normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). Log classification to Attio.

**Diagnose (triggered by anomaly):** When a metric anomaly is detected, gather context:
- Which partner(s) changed? Pull per-partner breakdowns from PostHog
- What changed in the co-marketing? Check if a partner stopped distributing, changed their audience, or launched a competing integration
- External factors? Check if competitor integrations launched, partner had a product outage, or seasonal patterns apply

Generate 3 ranked hypotheses with expected impact. Store in Attio.

**Experiment (triggered by hypothesis):** Run the top hypothesis as a PostHog feature-flagged experiment:
- Co-marketing messaging variants: test different integration value propositions in partner emails
- Launch timing experiments: test different days/times for co-marketing sends
- Partner tier experiments: test whether increasing co-marketing frequency with top partners yields diminishing returns
- Integration onboarding experiments: test different activation flows (3-step vs 1-click setup)

Minimum 7 days or 100 samples per variant, whichever is longer.

**Evaluate (triggered by experiment completion):** Pull results, run statistical evaluation, decide:
- Adopt: implement the winning variant across all partners (or the specific partner it tested on)
- Iterate: generate a refined hypothesis building on results
- Revert: restore control, log the failure, return to monitoring

**Report (weekly):** Generate optimization brief covering anomalies detected, hypotheses tested, experiments running, decisions made, and net metric change from adopted changes.

### 2. Monitor integration pipeline health

Run the `integration-pipeline-health-monitor` drill at Durable configuration:
- All dashboards and alerts from Scalable level remain active
- Add `posthog-anomaly-detection` integration for automated partner performance anomaly detection
- Weekly briefs now include the autonomous optimization report alongside the standard metrics
- Dormant integration alerts now trigger the optimization loop's diagnosis phase automatically

### 3. Score and optimize the partner portfolio

Run the `partner-relationship-scoring` drill adapted for integration partnerships. Score each partner monthly on:

- **Lead volume (1-10):** How many leads does this partner generate per month?
- **Lead quality (1-10):** What percentage of partner-sourced leads convert to paid?
- **Distribution reliability (1-10):** Does the partner consistently distribute co-marketing content when agreed?
- **Integration engagement (1-10):** Are the partner's users actively using the integration (not just activating and abandoning)?
- **Relationship health (1-10):** Is the partner responsive, enthusiastic about co-marketing, and growing their own user base?

Tier partners:
- **Tier 1 (40-50):** Invest heavily. Deeper integrations, more frequent co-marketing, joint webinars, co-branded content.
- **Tier 2 (25-39):** Maintain. Standard co-marketing cadence. Investigate which dimension to improve.
- **Tier 3 (10-24):** Reduce investment. Quarterly co-marketing only. Evaluate whether the integration is worth maintaining.
- **Tier 4 (1-9):** Sunset. Stop co-marketing. Consider deprecating the integration if maintenance cost exceeds lead value.

The agent automatically adjusts co-marketing frequency and investment based on tier changes.

### 4. Guardrails

- **Rate limit:** Maximum 1 active experiment per partner at a time. Never test multiple variables on the same partner simultaneously.
- **Revert threshold:** If partner-sourced leads drop >30% during any experiment, auto-revert immediately.
- **Human approval required for:**
  - Deprecating an integration (Tier 4 sunset decision)
  - Changing co-marketing messaging that the partner has approved
  - Budget changes >20% for paid co-marketing promotions
- **Cooldown:** After a failed experiment, wait 7 days before testing a new hypothesis on the same partner.
- **Maximum experiments per month:** 4 across the entire partner portfolio. If all 4 fail, pause optimization and flag for strategic review.

### 5. Convergence detection

The optimization loop runs indefinitely. It detects convergence when:
- 3 consecutive experiments across different optimization levers all produce <2% improvement
- Partner portfolio composition has been stable for 2+ months (no tier changes)
- Weekly lead volume variance is <5% for 4+ consecutive weeks

At convergence:
1. The integration partnerships play has reached its local maximum
2. Reduce monitoring from daily to weekly
3. Report: "Integration partnerships are optimized. Current performance: {metrics}. Further gains require strategic changes (new partner categories, new integration types, product changes) rather than tactical optimization."

## Time Estimate

- Autonomous optimization setup and configuration: 12 hours (one-time)
- Integration pipeline health monitor (Durable config): 6 hours (one-time)
- Partner relationship scoring setup: 4 hours (one-time)
- Monthly monitoring and maintenance: 8 hours/month (ongoing)
- Experiment design and evaluation review: 4 hours/month (ongoing)
- Quarterly strategic review: 6 hours/quarter

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Crossbeam | Partner account mapping and overlap intelligence | Growth: $0-200/mo (https://www.crossbeam.com/pricing) |
| PostHog | Anomaly detection, experiments, dashboards | Free tier: 1M events/mo; Growth: usage-based (https://posthog.com/pricing) |
| n8n | Optimization loop scheduling and automation | Free (self-hosted); Cloud: $24/mo (https://n8n.io/pricing) |
| Anthropic | Hypothesis generation and experiment evaluation | API: ~$3-15/1M tokens (https://www.anthropic.com/pricing) |
| Attio | Partner portfolio scoring and pipeline tracking | Plus: $29/user/mo (https://attio.com/pricing) |
| Loops | Co-marketing email experiments | Starter: $49/mo (https://loops.so/pricing) |

## Drills Referenced

- `autonomous-optimization` — the always-on monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `integration-pipeline-health-monitor` — dashboards, weekly briefs, per-partner ROI, anomaly detection, and reliability monitoring
- `partner-relationship-scoring` — monthly partner scoring and tiering to optimize portfolio investment allocation
