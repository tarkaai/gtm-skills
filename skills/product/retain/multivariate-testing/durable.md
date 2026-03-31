---
name: multivariate-testing-durable
description: >
  Multivariate Experiments — Durable Intelligence. Autonomous agent continuously
  generates MVT hypotheses from metric anomalies, runs experiments, evaluates
  interaction effects, and auto-implements winners to find the local maximum
  of every retention surface.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving MVT win rate and retention lift over 6 months via autonomous optimization"
kpis: ["MVT velocity", "Win rate", "Combination insights", "Experiment velocity", "AI lift"]
slug: "multivariate-testing"
install: "npx gtm-skills add product/retain/multivariate-testing"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Multivariate Experiments — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

The autonomous optimization loop runs continuously, detecting retention metric anomalies, generating MVT hypotheses, designing and running experiments, evaluating results (including interaction effects), and auto-implementing winners. The agent finds the local maximum of each retention surface and maintains it as user behavior shifts. Weekly optimization briefs summarize what changed, why, and what is next. The system converges when successive experiments produce <2% improvement for 3 consecutive experiments on a given surface.

## Leading Indicators

- Autonomous optimization loop running daily anomaly detection within the first week
- First agent-generated MVT hypothesis produced within 2 weeks
- At least 1 agent-designed experiment running by week 3
- Weekly optimization briefs generated without human intervention
- Experiment learning database growing with each completed test
- At least 1 surface declared "converged" (local maximum reached) within 3 months
- Overall retention metrics stable or improving month over month

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill configured for multivariate experiments. The core loop:

**Monitor (daily via n8n cron):**
- Use PostHog anomaly detection to check all retention surface metrics: conversion rate, engagement rate, retention rate, churn rate
- Compare last 2 weeks against 4-week rolling average
- Classify each surface: **normal** (within ±10%), **plateau** (±2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If normal, log to Attio and take no action
- If anomaly detected, trigger the diagnosis phase

**Diagnose (triggered by anomaly):**
- Pull the surface's historical experiment data from the learning database (built at Scalable level)
- Identify which variables have been tested on this surface and their measured effects
- Use Claude (Anthropic API) to generate 3 ranked MVT hypotheses: which variables to test next, predicted lift, risk level
- Prioritize: untested variable combinations first, then re-tests of variables where conditions may have changed (new user cohort, product changes)
- If top hypothesis is high risk, alert for human review and stop. Otherwise, proceed

**Experiment (triggered by hypothesis acceptance):**
- Design the MVT matrix using the the mvt experiment design workflow (see instructions below) drill (agent executes this autonomously)
- Configure PostHog feature flags and launch the experiment
- The `autonomous-optimization` drill handles ongoing monitoring

**Evaluate (triggered by experiment completion):**
- Analyze results using the MVT-specific analysis from the learning database: per-cell conversion, main effects, interaction effects
- Decision tree:
  - **Adopt**: winning combination is statistically significant and interaction effects are favorable. Auto-deploy to 100% via feature flags. Log the change.
  - **Iterate**: results suggest a promising direction but did not reach significance. Generate a follow-up hypothesis with tighter variable selection. Return to Diagnose.
  - **Revert**: no combination outperforms baseline, or guardrail metrics degraded. Restore original configuration. Log the failure. Return to Monitor.
  - **Extend**: results trending positive but experiment needs more data. Extend duration. Set reminder.
- Store the full evaluation in Attio: decision, confidence, reasoning, interaction effects discovered

**Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate: net retention lift from all changes adopted this week
- Produce a weekly optimization brief:
  - Surfaces optimized and current performance vs. baseline
  - Active experiments and projected completion dates
  - Surfaces approaching convergence (diminishing returns)
  - Recommended strategic shifts for surfaces that have converged
- Post to Slack and store in Attio

### 2. Deploy the MVT-specific monitoring layer

Run the `autonomous-optimization` drill in always-on mode. At Durable level, the monitor handles:

- All agent-generated experiments (no human setup required)
- Automatic cell-level pausing when guardrails trigger
- Completion detection feeding directly back into the optimization loop's Evaluate phase
- Historical health data feeding into hypothesis quality scoring (experiments that had traffic issues get flagged so the agent avoids similar designs)

### 3. Build the Durable experiment dashboard

Run the `dashboard-builder` drill to create a PostHog dashboard for the full MVT program:

**Program-level metrics:**
- Total experiments run (cumulative and monthly)
- Win rate: percentage of experiments that produced a statistically significant winner
- Average lift per winning experiment
- Cumulative retention impact: total lift from all implemented winners vs. original baseline
- Time to convergence per surface

**Per-surface metrics:**
- Current conversion/retention rate vs. pre-optimization baseline
- Number of experiments completed on this surface
- Last experiment date and result
- Convergence status: optimizing, converging, converged

**Agent performance metrics:**
- Hypothesis quality score: percentage of agent-generated hypotheses that led to significant results
- False positive rate: percentage of "winners" that reverted within 7 days
- Optimization velocity: time from anomaly detection to winner deployment

Set alerts for: any surface where retention drops >15% from its post-optimization peak, any experiment that runs >2x its planned duration, and convergence events (a surface reaching local maximum).

### 4. Handle convergence

When a surface reaches convergence (3 consecutive experiments with <2% improvement):

1. Reduce monitoring frequency for that surface from daily to weekly
2. Lock the current configuration as the optimized baseline
3. Generate a convergence report: what the surface started at, what it optimized to, how many experiments it took, which variables mattered most, and which interaction effects were discovered
4. Shift agent focus to surfaces that have more optimization headroom
5. Re-check converged surfaces monthly -- if user behavior shifts (seasonal changes, product updates, new user cohorts), the surface may need re-optimization

### 5. Evaluate sustainability

Measure against: sustained or improving MVT win rate and retention lift over 6 months. This level runs continuously. The system is durable when:

- The agent runs experiments without human intervention for routine operations
- Weekly optimization briefs are generated and accurate
- Retention metrics across optimized surfaces are stable or improving
- Converged surfaces maintain their optimized performance
- The learning database grows and improves hypothesis quality over time

If metrics decay, the agent diagnoses the cause (user behavior shift, product changes, competitive pressure) and generates new hypotheses targeting the decay.

## Time Estimate

- 20 hours: autonomous optimization loop setup and integration testing
- 10 hours: MVT-specific monitoring configuration
- 15 hours: dashboard build and alert configuration
- 80 hours: ongoing agent operation and monitoring (largely autonomous, 3-4 hours/week human oversight)
- 15 hours: convergence analysis and strategic reviews
- 10 hours: learning database maintenance and hypothesis quality tuning

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, anomaly detection, dashboards | Free tier: 1M requests/mo. Paid: starts at $0.0001/request ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop scheduling, health monitoring, reporting | Self-hosted free; Cloud Pro ~$60/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, report writing | Sonnet 4.6: $3/$15 per 1M tokens. Estimated ~$20-50/mo at weekly cadence ([claude.com/pricing](https://claude.com/pricing)) |
| Attio | Experiment records, hypothesis queue, convergence tracking | Included in standard stack |
| Intercom | In-app message and tooltip variants for MVTs | ~$75-300/mo depending on contacts ([intercom.com/pricing](https://www.intercom.com/pricing)) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor metric anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, produce weekly briefs
- `autonomous-optimization` — continuous health monitoring for all agent-generated experiments with automatic guardrail enforcement
- `dashboard-builder` — builds the program-level and per-surface dashboards that track optimization progress and convergence
