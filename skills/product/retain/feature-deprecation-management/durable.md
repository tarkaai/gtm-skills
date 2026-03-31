---
name: feature-deprecation-management-durable
description: >
  Feature Sunset Communication — Durable Intelligence. Autonomous AI agents continuously
  optimize deprecation communication, migration routing, and intervention timing.
  The system detects metric anomalies, generates improvement hypotheses, runs A/B
  experiments, and auto-implements winners to sustain ≥85% migration rates.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving migration ≥85% over 6 months via autonomous optimization"
kpis: ["Migration completion rate (sustained)", "Churn from sunset (trending)", "Experiment velocity (experiments/month)", "AI lift (improvement from autonomous changes)", "Cost per migration (trending down)", "Post-sunset orphan rate"]
slug: "feature-deprecation-management"
install: "npx gtm-skills add product/retain/feature-deprecation-management"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# Feature Sunset Communication — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The deprecation management system runs itself. An autonomous optimization loop monitors migration metrics, detects when performance degrades, generates hypotheses for improvement, runs experiments, evaluates results, and auto-implements winners. The system gets better over time without human intervention. Every new deprecation benefits from learnings accumulated across all previous sunsets. The human role shifts from operating the system to reviewing weekly optimization briefs and approving high-risk changes.

## Leading Indicators

- Autonomous optimization loop running daily with anomaly detection active
- At least 1 experiment per active deprecation per month
- Successive deprecations achieving target migration rate faster than previous ones (institutional learning)
- Cost per migration decreasing quarter-over-quarter
- Post-sunset orphan rate below 2% (near-zero users surprised by feature removal)
- Convergence signal: optimization experiments producing less than 2% improvement for 3 consecutive cycles (local maximum reached)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for deprecation management. This creates the always-on agent loop:

**Monitor (daily via n8n cron):**
- Pull migration completion rate, stall rate, communication engagement, and churn rate from PostHog
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger the diagnosis phase

**Diagnose (triggered by anomaly):**
- Gather context: current routing rules, message variants in use, active A/B tests, recent changes
- Pull 8-week metric history from PostHog dashboards
- Run hypothesis generation with the anomaly data. Example hypotheses for deprecation:
  - "Migration velocity dropped because the latest cohort of affected users has a different workflow pattern than previous cohorts — the current migration guide does not cover their use case"
  - "Stall rate increased because the in-app banner was displaced by a product update notification — users are not seeing the deprecation notice"
  - "Communication engagement dropped because email sequence fatigue — users who received deprecation emails for a previous sunset are ignoring this one"
- Rank hypotheses by expected impact and risk level
- If risk is high (e.g., changing routing rules for critical-tier users), send alert for human approval and pause

**Experiment (triggered by hypothesis acceptance):**
- Design the experiment using PostHog feature flags: split traffic between control (current) and variant (hypothesis change)
- Example experiments:
  - New migration guide variant tailored to the underserved workflow pattern
  - In-app notice redesigned as a modal instead of a banner
  - Email sequence replaced with a single high-impact email for users who have seen deprecation emails before
- Run for minimum 7 days or 100+ samples per variant

**Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Decide: adopt (implement winner permanently), iterate (refine hypothesis), revert (restore control), or extend (keep running)
- Store the full evaluation with decision, confidence, and reasoning in Attio

**Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on migration rate, stall rate, churn rate
  - Current performance vs. estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

**Guardrails:**
- Maximum 1 active experiment per deprecation at a time
- Auto-revert if migration rate drops >30% during any experiment
- Human approval required for: routing changes affecting critical-tier users, communication changes reaching >50% of affected users, any change flagged as high risk
- Cooldown: 7 days between failed experiments on the same variable
- Maximum 4 experiments per deprecation per month

### 2. Deploy the deprecation health monitor

Run the `autonomous-optimization` drill. This builds the monitoring layer that feeds the autonomous optimization loop:

- Master dashboard aggregating all active deprecations: feature, sunset date, days remaining, migration %, risk level
- Anomaly detection for: migration velocity drops, stall rate spikes, regression surges
- Daily health check events logged to PostHog with consistent property names for the optimization loop to consume
- Weekly deprecation health reports stored in Attio
- Lifecycle metrics tracking: time to 50% migration, communication touchpoints per migration, cost per migration, post-sunset orphan rate

The health monitor and autonomous optimization loop work together: the monitor detects problems, the optimization loop fixes them.

### 3. Launch NPS feedback loops for deprecation

Run the `nps-feedback-loop` drill, targeted specifically at users who have completed migration:

- Deploy an NPS survey 14 days after migration completion: "How would you rate the migration experience from [old feature] to [replacement]?"
- Route promoters (9-10) to a follow-up: "Glad the migration went smoothly. Would you share a quick testimonial about [replacement]?"
- Route detractors (0-6) to a feedback form: "What could we have done better? We want to improve this for future feature changes." Include specific questions: Was the timeline adequate? Was the migration guide clear? Does the replacement meet your needs?
- Route passives (7-8) to a single question: "What one thing would have made the migration easier?"

Feed NPS data into the autonomous optimization loop as a signal. If NPS for a deprecation's migration experience drops below 30, the optimization loop should prioritize "migration experience quality" in its next hypothesis generation cycle.

### 4. Build institutional learning across deprecations

Configure the system to accumulate learnings:

- After each deprecation completes, log a `deprecation_lifecycle_complete` event in PostHog with properties: `feature_slug`, `total_affected_users`, `final_migration_rate`, `total_days`, `cost_per_migration`, `post_sunset_orphan_rate`, `experiments_run`, `nps_score`
- Maintain an Attio record per completed deprecation as a knowledge base entry
- When a new deprecation begins, the optimization loop queries past deprecation outcomes to set baseline expectations: "Similar deprecations (same tier distribution, same complexity score) achieved 92% migration in 45 days — use this as the starting target"
- A/B test winners from past deprecations become the default starting configuration for new ones (e.g., if social proof messaging won 3 times, it becomes the default, not the experiment)

### 5. Evaluate sustainability

This level runs continuously. Monthly review:

- **Sustained performance:** Migration rate ≥85% across all deprecations for 6 consecutive months
- **Improving efficiency:** Cost per migration decreasing or stable. Time to target migration rate decreasing.
- **Autonomous operation:** The system requires less than 2 hours/week of human attention (reviewing briefs, approving high-risk changes)
- **Convergence detection:** When the optimization loop reports convergence (3 consecutive experiments with <2% improvement), the deprecation system has reached its local maximum. Reduce monitoring to weekly. Further gains require strategic changes (better replacement features, different migration paradigm) rather than tactical optimization.

## Time Estimate

- 30 hours: Autonomous optimization loop setup and configuration
- 20 hours: Deprecation health monitor build and dashboard creation
- 10 hours: NPS feedback loop configuration and routing
- 15 hours: Institutional learning system and cross-deprecation knowledge base
- 75 hours: 6-month monitoring — weekly brief review (1h/week), monthly deep review (3h/month), quarterly strategic assessment (5h/quarter)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, anomaly detection, dashboards, feature flags, NPS | Free tier for most usage; paid at $0.00005/event above 1M; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, checklists, tours, NPS surveys | Advanced $85/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences, transactional, broadcasts | $49/mo+ based on contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, optimization briefs | ~$15-50/mo depending on experiment volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Attio | Migration data, optimization audit trail, knowledge base | Standard stack — excluded from play budget |
| n8n | Optimization loop scheduling, health monitor workflows | Standard stack — excluded from play budget |

**Estimated play-specific cost:** $149-285/mo (Intercom Advanced + Loops + Anthropic API for the AI optimization loop)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that monitors metrics, generates hypotheses, runs experiments, evaluates results, and auto-implements winners to find the local maximum
- `autonomous-optimization` — continuous monitoring of migration health across all active sunsets with anomaly detection, alerting, and lifecycle metrics that feed the optimization loop
- `nps-feedback-loop` — collects and routes post-migration NPS feedback to measure migration experience quality and feed detractor insights into the optimization loop
