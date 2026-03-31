---
name: usage-milestones-durable
description: >
  Usage Milestone Celebrations — Durable Intelligence. An always-on AI agent monitors celebration
  effectiveness, detects engagement decay and celebration fatigue, generates improvement hypotheses,
  runs A/B experiments, and auto-implements winners. Sustains or improves ≥65% celebration engagement
  over 6 months with no manual intervention.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving celebration engagement ≥65% over 6 months via autonomous optimization"
kpis: ["Celebration engagement rate (6-month trend)", "Retention lift stability", "Experiment velocity", "Autonomous improvement magnitude", "Celebration fatigue index"]
slug: "usage-milestones"
install: "npx gtm-skills add product/retain/usage-milestones"
drills:
  - autonomous-optimization
  - dashboard-builder
---

# Usage Milestone Celebrations — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

An autonomous agent loop monitors milestone celebration performance, detects when engagement decays or fatigue sets in, generates hypotheses for improvement, runs experiments, and implements winners — all without human intervention. Celebration engagement sustains at or above 65% for 6 consecutive months. The agent converges when successive experiments yield less than 2% improvement, signaling the local maximum has been reached.

## Leading Indicators

- The autonomous optimization loop runs at least 2 experiments per month
- No single month shows a celebration engagement rate below 60%
- Celebration fatigue index (from `autonomous-optimization`) stays below 0.4 across all persona segments
- Retention lift (celebrated vs. uncelebrated historical baseline) is stable or improving
- Weekly optimization briefs are generated and posted automatically

## Instructions

### 1. Deploy the milestone retention monitor

Run the `autonomous-optimization` drill to build the always-on measurement layer:

- Build milestone-retention cohort comparisons for every tier (celebrated vs. uncelebrated, 7/14/30-day retention)
- Create the 7-panel effectiveness dashboard in PostHog (milestone funnel, engagement by tier, retention lift trend, CTA conversion, milestone velocity, churned-despite-milestone, celebration fatigue index)
- Deploy the weekly decay detection workflow in n8n that compares engagement rates against 8-week rolling averages and flags tiers decaying beyond 15%
- Activate the churned-despite-milestone analysis that identifies users who invested in the product (reached tier 2+) but still disengaged
- Enable celebration fatigue scoring as a PostHog person property

This drill produces the data feeds the autonomous optimization loop consumes.

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill with milestone-specific configuration:

**Monitoring (daily via n8n):**
- Primary KPIs to watch: celebration engagement rate (per tier, per persona), 14-day retention lift, CTA conversion rate, celebration fatigue index
- Anomaly classification thresholds: plateau = ±2% for 3+ weeks, drop = >15% decline, spike = >25% increase
- Data sources: PostHog events (`celebration_shown`, `celebration_engaged`, `celebration_dismissed`, `celebration_cta_clicked`), PostHog person properties (`celebration_fatigue_score`, `highest_milestone_tier`), milestone retention dashboard

**Diagnosis (triggered by anomaly):**
- Context to pull: current celebration copy per tier per persona, current CTA configuration, current milestone spacing, recent A/B test history (from Scalable level), fatigue scores by persona
- Hypothesis categories to explore: (1) copy refresh for fatigued tiers, (2) CTA variant for low-converting tiers, (3) milestone spacing adjustment for tiers with drop-off, (4) channel mix change (shift in-app vs. email ratio), (5) timing adjustment (delay between milestone and celebration)
- Risk classification: copy changes = low risk, milestone spacing changes = medium risk (affects the core ladder), audience targeting changes affecting >50% of users = high risk (requires human approval)

**Experimentation (triggered by hypothesis acceptance):**
- Use PostHog feature flags to split traffic between control (current celebration) and variant (proposed change)
- Minimum experiment duration: 7 days or 100+ milestone events in each variant, whichever is longer
- Maximum 1 active experiment per milestone tier at a time
- Log experiment start to Attio: hypothesis, tier affected, expected duration, success criteria

**Evaluation (triggered by experiment completion):**
- Adopt: variant engagement rate is statistically significantly higher (95% confidence) AND no degradation in retention lift or CTA conversion. Auto-update the celebration configuration.
- Iterate: result is directionally positive but not significant. Generate a refined hypothesis and re-test.
- Revert: variant performed worse. Disable and restore control. Wait 7 days before testing the same tier again.
- Extend: variance is high. Run for another period.

**Reporting (weekly via n8n):**
- Generate a weekly optimization brief: experiments run, decisions made, net engagement change, distance from estimated local maximum, celebration fatigue trend, recommended focus for next week
- Post to Slack and store in Attio

### 3. Build the Durable executive dashboard

Run the `dashboard-builder` drill to create a single executive-facing PostHog dashboard:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Celebration engagement (6-month trend) | Line chart | Is the play sustaining above 65%? |
| Retention lift (celebrated vs. historical baseline) | Line chart | Is the retention impact stable? |
| Experiment log | Table | What has the agent tested, decided, and implemented? |
| Fatigue index by persona | Line chart | Are any segments tuning out celebrations? |
| Autonomous improvement cumulative | Counter | Total percentage points of engagement gained by agent experiments |
| Convergence indicator | Status | Green = still optimizing, Yellow = diminishing returns, Red = converged |

Set alerts:
- Celebration engagement drops below 60% for 2 consecutive weeks → escalate to human review
- Celebration fatigue index exceeds 0.5 for any persona → pause celebrations for that persona and alert
- 4 consecutive failed experiments → pause autonomous optimization and flag for strategic review
- Retention lift drops below 5pp → the play may be losing effectiveness, trigger a full audit

### 4. Configure guardrails

Apply the standard `autonomous-optimization` guardrails plus milestone-specific protections:

- **Celebration frequency cap:** No user sees more than 1 celebration per week, regardless of how many milestones they hit. Queue excess celebrations.
- **Fatigue circuit breaker:** If a user's celebration fatigue score exceeds 0.7, suppress all celebrations for 30 days. Resume with a fresh format.
- **Milestone ladder stability:** The autonomous loop may NOT add or remove milestone tiers without human approval. It may adjust copy, timing, CTA, and format, but the ladder structure is human-owned.
- **Budget guardrail:** If Intercom or Loops costs exceed 150% of Scalable-level spend, pause new experiments and alert.

### 5. Evaluate sustainability

This level runs continuously. Monthly, the agent generates a sustainability report:

- Is celebration engagement >=65%? (target: yes for every month)
- Is the optimization loop still finding improvements? (experiment win rate, magnitude of wins)
- Has convergence been reached? (3 consecutive experiments with <2% improvement)

At convergence:
1. Reduce monitoring from daily to weekly
2. Reduce experiment frequency from 2/month to 1/month
3. Generate a final report: "Milestone celebrations have reached their local maximum. Current engagement: [X%]. Retention lift: [Y]pp. Further gains require product changes (new milestone types, new celebration channels) rather than tactical optimization."

**Human action required:** Review the convergence report and decide whether to invest in structural changes (new milestone types, gamification features, social sharing) or accept the local maximum.

## Time Estimate

- 20 hours: deploy milestone retention monitor (dashboard, workflows, fatigue scoring)
- 30 hours: configure and tune the autonomous optimization loop
- 10 hours: build the Durable executive dashboard
- 10 hours: implement guardrails and circuit breakers
- 80 hours: ongoing monitoring, experiment cycles, brief reviews (over 6 months, ~3 hours/week agent compute + human review)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, experiments, cohorts, dashboards, anomaly detection | Growth: $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app celebrations with persona/tier variants | Pro: ~$150-300/mo — https://www.intercom.com/pricing |
| Loops | Milestone follow-up emails | Starter: $49/mo — https://loops.so/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, brief writing | Claude Sonnet: $3/MTok in, $15/MTok out — https://www.anthropic.com/pricing |
| n8n | Scheduling optimization loop, decay detection, alerting | Starter: $24/mo — https://n8n.io/pricing |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop that monitors, diagnoses, experiments, evaluates, and reports on celebration performance
- `autonomous-optimization` — tracks celebration-to-retention causality, detects engagement decay, surfaces churned-despite-milestone users, and computes celebration fatigue scores
- `dashboard-builder` — creates the Durable executive dashboard with 6-month trend visibility and convergence tracking
