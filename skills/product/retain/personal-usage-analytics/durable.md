---
name: personal-usage-analytics-durable
description: >
  Personal Usage Analytics — Durable Intelligence. Always-on AI agent autonomously optimizes the
  analytics surface: detects engagement anomalies, generates hypotheses, runs experiments, and
  auto-implements winners. Converges to local maximum retention lift.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "30 hours setup + continuous autonomous operation over 6 months"
outcome: "Sustained or improving retention lift ≥5pp over 6 months, with autonomous optimization producing <2% improvement in 3 consecutive experiments (convergence)"
kpis: ["Retention lift (causal, rolling 30-day)", "Experiment velocity (experiments completed per month)", "Autonomous win rate (% of experiments that produced ≥2% improvement)", "View rate stability", "Convergence status"]
slug: "personal-usage-analytics"
install: "npx gtm-skills add product/retain/personal-usage-analytics"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Personal Usage Analytics — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Pass threshold: the analytics surface sustains or improves its ≥5pp retention lift over 6 months with no manual intervention. The autonomous optimization agent runs the detect-diagnose-experiment-evaluate-implement loop continuously. The play reaches convergence when 3 consecutive experiments produce <2% improvement — indicating the local maximum has been found.

## Leading Indicators

- Autonomous optimization loop running without human intervention for 4+ consecutive weeks
- At least 2 experiments completed per month
- Win rate ≥40% (at least 40% of experiments produce a measurable improvement)
- No guardrail breaches (support ticket rate, view rate floor) triggering auto-reverts
- Weekly optimization briefs generated and logged in Attio without gaps
- Retention lift holding within ±2pp of the Scalable level result

## Instructions

### 1. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill targeting the analytics surface. Configure the optimization loop with these play-specific parameters:

**Monitoring targets (Phase 1 of the drill):**
- Primary KPI: 30-day retention rate for analytics viewers
- Secondary KPIs: weekly analytics view rate, engagement depth (metric click rate), CTA conversion rate, feature adoption from CTAs
- Anomaly thresholds: plateau = ±2% for 3+ weeks, drop = >10% decline in any KPI, spike = >30% increase

**Hypothesis generation context (Phase 2 of the drill):**

Provide the agent with the play's optimization surface — the variables it is allowed to change:

- **Metrics displayed**: which 3-5 stats appear on the analytics surface per segment
- **Metric presentation**: chart type (sparkline, bar, number), time window (7-day vs. 30-day), comparison format (vs. last period, vs. peers, absolute)
- **Insight copy**: the headline insight text (e.g., "You saved 4.2 hours this week" vs. "Your automation usage is up 34%")
- **CTA type and copy**: feature suggestion, resume-work, milestone-chase, social-proof
- **Discovery prompt timing**: trigger conditions for Intercom in-app messages
- **Email digest content**: which stats to include, subject line, send time
- **Segment thresholds**: the activity level cutoffs that define power/regular/light/declining segments

The agent must NOT change: core product functionality, pricing, plan limits, or analytics surface layout/position in the product navigation.

**Experiment parameters (Phase 3 of the drill):**
- Use PostHog feature flags to split analytics viewers between control (current config) and variant (hypothesis change)
- Minimum sample: 200 per variant
- Minimum duration: 14 days (to capture weekly usage patterns)
- Maximum 1 active experiment at a time
- Auto-revert if any guardrail metric drops >20% during the experiment

**Guardrails (critical):**
- If analytics view rate drops below 25% for any week during an experiment, auto-revert immediately
- If support tickets mentioning "stats," "analytics," or "usage data" increase >2x baseline, auto-revert and flag for human review
- If retention lift drops below 3pp at any point, pause experiments and trigger human strategic review
- Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review
- Budget changes (e.g., increased n8n compute for more frequent aggregation) require human approval if >20% increase

### 2. Set up the play-specific health dashboard

Run the `dashboard-builder` drill to create a dashboard dedicated to the analytics surface's long-term health:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Retention lift trend (rolling 30-day) | Line chart | Is the causal retention impact holding? |
| View rate by segment | Stacked area chart | Are all segments engaging or is one dropping off? |
| Experiment timeline | Gantt chart / table | What experiments have run, what was decided? |
| Win rate (trailing 90 days) | Number + trend | Is the optimization loop still finding improvements? |
| Convergence tracker | Line chart | How much did each successive experiment improve the primary KPI? |
| Autonomous loop health | Status indicator | Is the n8n optimization workflow running on schedule? |
| Guardrail status | Traffic light | Are all guardrails green? |

Set alerts:
- Retention lift trend declining for 3+ consecutive weeks
- Win rate drops below 20% over a 90-day window (the agent is running experiments but not finding improvements — possible convergence or staleness)
- Autonomous loop missed a scheduled run

### 3. Run the engagement monitor as a continuous health check

Run the `autonomous-optimization` drill in continuous mode. The weekly health report it generates feeds into the autonomous optimization loop as input. When the health report flags WARNING or CRITICAL status, the optimization agent prioritizes that metric for its next hypothesis.

Specifically:
- If view rate declining: the agent hypothesizes and tests new discovery prompts or analytics surface changes
- If engagement depth declining: the agent tests new metric selections or presentation formats
- If CTA conversion declining: the agent tests new CTA types or personalization logic
- If retention lift narrowing: the agent tests more aggressive personalization or new insight types

### 4. Weekly optimization brief review

The `autonomous-optimization` drill generates a weekly brief. Review it for:

- Net impact of adopted changes: is cumulative retention lift growing or flat?
- Experiment quality: are hypotheses getting more specific and targeted over time?
- Convergence signal: are the last 3 experiments each producing <2% improvement? If yes, the play is converging.
- Anomaly patterns: are the same anomalies recurring? This may indicate an external factor (seasonal usage changes, product updates) rather than an analytics surface problem.

**Human action required (monthly):** Review the monthly summary of all experiments, their outcomes, and the agent's recommended strategic direction. Approve or override the agent's plan for the next month. This 30-minute monthly review is the only ongoing human involvement.

### 5. Handle convergence

When the agent detects convergence (3 consecutive experiments each producing <2% improvement on the primary KPI):

1. The agent logs convergence in Attio with the final optimized configuration
2. Monitoring frequency reduces from daily to weekly
3. Experiment frequency reduces to 1 per month (maintenance experiments to detect drift)
4. The agent generates a convergence report: "Personal Usage Analytics has reached its local maximum. Current 30-day retention lift: [X]pp. View rate: [Y]%. Further gains require strategic changes (new metric types, product changes, or fundamentally different analytics experiences) rather than tactical optimization."

If after convergence a metric drops significantly (>15% below converged baseline for 2+ weeks), the agent re-enters active optimization mode automatically.

## Time Estimate

- 8 hours: autonomous optimization loop configuration and testing
- 6 hours: play-specific health dashboard build
- 4 hours: engagement monitor continuous mode setup
- 2 hours: first week monitoring to ensure the loop runs correctly
- 10 hours: monthly reviews over 6 months (30 minutes per week x 20 weeks, rounded up)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free up to 1M events/mo — https://posthog.com/pricing |
| Anthropic API (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$20-50/mo at 4 experiments/mo — https://www.anthropic.com/pricing |
| n8n | Optimization loop scheduling, aggregation pipeline | Free self-hosted or from $24/mo cloud — https://n8n.io/pricing |
| Attio | Experiment logging, convergence tracking, play health | From $29/seat/mo — https://attio.com/pricing |

**Estimated play-specific cost:** ~$100-200/mo (Anthropic API for hypothesis generation + increased n8n compute for the optimization loop)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly briefs
- `autonomous-optimization` — continuous health monitoring feeding engagement data into the optimization loop
- `dashboard-builder` — builds the long-term health dashboard tracking retention lift, experiment outcomes, and convergence
