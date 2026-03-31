---
name: multivariate-testing-scalable
description: >
  Multivariate Experiments — Scalable Automation. Automate the full MVT lifecycle:
  experiment design, traffic monitoring, results analysis, and winner deployment
  to sustain ≥5 MVTs per 2-month cycle across multiple product surfaces.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥5 MVTs completed per 2-month cycle with automated monitoring"
kpis: ["MVT velocity", "Win rate", "Combination insights", "Segment metrics"]
slug: "multivariate-testing"
install: "npx gtm-skills add product/retain/multivariate-testing"
drills:
  - ab-test-orchestrator
  - dashboard-builder
---

# Multivariate Experiments — Scalable Automation

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

Run at least 5 multivariate experiments per 2-month cycle with automated traffic monitoring, health checks, and results analysis. Expand testing to multiple product surfaces and user segments simultaneously. The agent handles experiment lifecycle management end-to-end; human involvement is limited to reviewing high-risk experiment proposals and strategic prioritization.

## Leading Indicators

- Automated health monitor running daily for all active experiments within the first week
- At least 2 experiments running concurrently on different surfaces by week 2
- Average time from experiment design to launch under 4 hours
- Automated results analysis producing combination rankings within 48 hours of experiment completion
- At least 2 experiments segmented by user cohort (plan, tenure, engagement level)

## Instructions

### 1. Build the automated experiment pipeline

Run the `ab-test-orchestrator` drill adapted for multivariate tests. Create an n8n workflow that manages the experiment lifecycle:

**Experiment queue:** Maintain a prioritized backlog of MVT hypotheses in Attio. Each entry includes: surface, variables to test, expected impact, required traffic, and priority score. The agent pulls the next highest-priority experiment when a slot opens.

**Concurrent experiment management:** Run up to 3 experiments simultaneously, provided they target different product surfaces and different user populations. Use PostHog cohorts to ensure no user is enrolled in more than 1 active experiment at a time. The agent checks for overlap before launching each new experiment.

**Automated launch:** When an experiment slot opens, the agent:
1. Pulls the next hypothesis from the queue
2. Runs the mvt experiment design workflow (see instructions below) to configure the matrix and feature flags
3. Verifies implementation by checking that all cell experiences render correctly (via PostHog flag evaluation)
4. Launches and logs the start in Attio

### 2. Deploy continuous health monitoring

Run the `dashboard-builder` drill. Configure:

- Daily traffic balance checks for all active experiments
- Real-time guardrail monitoring with automatic cell-level pausing if harm is detected
- Weekly status reports aggregating all running experiments
- Automated completion detection when all cells reach target sample size

The health monitor should require zero human intervention for normal experiment operation. Humans are only alerted when: a guardrail triggers, traffic imbalance persists for 3+ days, or projected completion exceeds planned duration by >2 weeks.

### 3. Scale across surfaces and segments

Expand MVT beyond the initial retention surfaces tested at Baseline. Target:

- **Onboarding flows**: test checklist order x default template x welcome message tone
- **Lifecycle emails**: test send timing x subject framing x CTA design
- **Feature gates**: test gate copy x unlock threshold x visual treatment
- **Usage alerts**: test alert threshold x message urgency x suggested action

For each surface, run segment-specific MVTs using PostHog cohorts:
- By plan tier (free vs. paid)
- By user tenure (first 30 days vs. 30-90 days vs. 90+ days)
- By engagement level (power users vs. casual users)

The same variable combination may perform differently across segments. Segment-level MVTs identify which combinations to personalize.

### 4. Automate results analysis and winner deployment

Run the the mvt results analysis workflow (see instructions below) drill as an automated workflow:

1. When the health monitor detects experiment completion, trigger analysis automatically
2. Compute per-cell conversion, main effects, and interaction effects
3. If a winner is statistically significant (95% confidence), generate an implementation plan
4. For low-risk winners (lift <20% and no guardrail concerns), auto-deploy by updating feature flags to 100% on the winning levels
5. For high-risk winners (lift >20% or guardrail flag), alert for human review before deployment
6. Post-deployment: monitor the primary metric for 7 days and auto-revert if lift decays >50%

### 5. Build the experiment learning database

Create a structured record in Attio for every completed experiment:

```json
{
  "experiment_slug": "...",
  "surface": "upgrade-prompt",
  "variables": ["copy_framing", "trigger_timing"],
  "cells": 4,
  "users_per_cell": 450,
  "duration_days": 12,
  "winner": "loss-aversion + usage-threshold",
  "lift": "+3.8pp",
  "main_effects": {"copy_framing": "+2.1pp", "trigger_timing": "+1.2pp"},
  "interactions": [{"type": "synergy", "magnitude": "+0.5pp"}],
  "segments_tested": ["free", "paid"],
  "segment_differences": "Paid users respond 2x to loss-aversion framing"
}
```

This database feeds the autonomous optimization loop at Durable level. Over time, it reveals: which variables have the largest main effects (test those first), which variables interact (always test them together), and which surfaces have the most optimization headroom.

### 6. Evaluate against threshold

Measure against: at least 5 MVTs completed per 2-month cycle with automated monitoring. If PASS, proceed to Durable. If FAIL, diagnose: is the experiment queue running dry (broaden the hypothesis generation process), is traffic insufficient for concurrent experiments (consolidate to fewer surfaces), or is automation unreliable (fix the n8n workflows before adding more experiments).

## Time Estimate

- 12 hours: pipeline automation setup (n8n workflows, experiment queue, health monitor)
- 8 hours: segment-specific experiment design across surfaces
- 20 hours: experiment execution and monitoring (largely automated, with spot checks)
- 12 hours: results analysis and winner deployment
- 8 hours: learning database maintenance and hypothesis generation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, experiments, cohorts, funnels | Free tier: 1M requests/mo. Paid: starts at $0.0001/request ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Experiment lifecycle automation and health monitoring | Self-hosted free; Cloud Pro ~$60/mo for 10K executions ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Experiment records, hypothesis queue, audit trail | Included in standard stack |
| Intercom | In-app message variants for MVTs | ~$75-300/mo depending on contacts ([intercom.com/pricing](https://www.intercom.com/pricing)) |

## Drills Referenced

- `ab-test-orchestrator` — manages experiment lifecycle, concurrent scheduling, and statistical rigor
- the mvt experiment design workflow (see instructions below) — designs test matrices and configures PostHog feature flags for each experiment
- the mvt results analysis workflow (see instructions below) — computes main effects, interaction effects, and combination rankings
- `dashboard-builder` — daily health checks, guardrail monitoring, and completion detection
