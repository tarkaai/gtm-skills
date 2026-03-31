---
name: feature-spotlight-series-durable
description: >
  Weekly Feature Spotlights — Durable Intelligence. Autonomous optimization loop that detects
  spotlight performance changes, generates improvement hypotheses, runs experiments, and
  auto-implements winners to sustain and improve feature discovery across all segments.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving trial rate ≥25% and adoption rate ≥15% over 6 months via autonomous optimization"
kpis: ["Overall trial rate", "Adoption rate", "Experiment velocity", "Optimization lift", "Series fatigue index", "Distance from local maximum"]
slug: "feature-spotlight-series"
install: "npx gtm-skills add product/retain/feature-spotlight-series"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# Weekly Feature Spotlights — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Feature spotlight trial rate sustained at or above 25% and 7-day adoption rate sustained at or above 15% for 6 consecutive months. The autonomous optimization loop continuously detects performance changes, generates improvement hypotheses, runs A/B experiments, and auto-implements winners. Weekly health reports track progress toward the local maximum. When successive experiments produce less than 2% improvement, the series has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is working)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>3% improvement in targeted metric)
- Series fatigue index stable or declining (spotlights are not wearing out)
- NPS feedback from feature adopters trending positive (the features being spotlighted deliver real value)
- Feature coverage approaching 100% of product features spotlighted at least once

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for the spotlight series:

**Monitor (daily via n8n cron):**
- Query PostHog for the series' primary KPIs: overall trial rate, per-spotlight trial rate, adoption rate, open rate, CTR, dismiss rate, per-segment performance
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the series' current configuration from Attio: active segments, content templates, channel mix, delivery timing, experiment history
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Examples of hypotheses the agent might generate:
  - "Trial rate dropped 15% because the last 3 spotlights targeted low-value features — prioritize features with the highest retention correlation for the next 4 weeks"
  - "Open rate is plateauing at 22% on email because the subject line format has been the same for 8 weeks — test a curiosity-gap format instead of benefit-led"
  - "Adoption rate is declining despite stable trial rate, suggesting spotlighted features are interesting to try but not sticky — add a follow-up nudge 3 days after first try showing an advanced use case"
  - "Per-segment data shows at-risk users have 2x the trial rate of power users on the same spotlight — increase allocation to at-risk users and reduce spotlight frequency for power users"
- Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of traffic or changes the core series format), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected segment between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets content, update the spotlight template; if it targets timing, adjust the n8n delivery schedule; if it targets audience, modify the PostHog cohort; if it targets format, configure the alternative content type in Intercom or Loops
- Run for minimum 7 days or 2 complete spotlight cycles, whichever is longer (spotlight experiments need multiple spotlights to detect patterns, not just one)
- Log experiment start in Attio: hypothesis, segment, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >3% improvement. Update the live series configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another spotlight cycle.

**Guardrails:**
- Maximum 1 active experiment at a time for the spotlight series
- If trial rate drops >30% during any experiment, auto-revert immediately
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review
- Never experiment on what is not measured — if a KPI lacks PostHog tracking, fix tracking first

### 2. Generate weekly health reports with series-specific signals

Run the `autonomous-optimization` drill at Durable depth. In addition to the standard series dashboard and fatigue detection, configure these Durable-specific monitors:

**Optimization progress tracking:**
- Log every experiment result with its net impact on the primary KPI
- Calculate cumulative optimization lift: total improvement in trial rate and adoption rate since the autonomous loop started
- Track distance from local maximum: if the last 3 experiments each produced <2% improvement, the series is converging

**Series longevity signals:**
- **Feature backlog health**: Are there enough unspotlighted features to sustain the series? If the backlog is exhausted, the agent should recommend: (a) re-spotlighting features to new user cohorts, (b) spotlighting feature combinations, or (c) shifting to a "tips and workflows" format that goes deeper on already-spotlighted features
- **Audience renewal rate**: What percentage of the target audience for each spotlight is new users who joined after the last time this feature was spotlighted? High renewal means the series can sustain; low renewal means the audience is saturated
- **Cross-feature discovery chains**: Are users who try one spotlighted feature more likely to try the next spotlighted feature? If yes, the series is building a discovery habit. Track the chain length.

The weekly report includes:
```
SPOTLIGHT SERIES — DURABLE INTELLIGENCE REPORT — WEEK OF {date}

OPTIMIZATION STATUS:
  Active experiment: {description or "none"}
  Experiments this month: {N}/4
  Cumulative optimization lift: +{X}% trial, +{Y}% adoption since loop started
  Distance from local maximum: {far|approaching|converged}

SERIES HEALTH:
  Trail rate (4-week avg): {X}%
  Adoption rate (4-week avg): {X}%
  Engagement trend: {stable|declining|improving}
  Feature backlog: {N} features remaining / {N} total
  Audience renewal rate: {X}%

ANOMALIES DETECTED: {list or "none"}
NEXT EXPERIMENT: {hypothesis and expected impact}
```

### 3. Close the feedback loop with feature adopters

Run the `nps-feedback-loop` drill targeted at users who adopted features through spotlights:

- Survey users who adopted a spotlighted feature 30+ days ago: "How useful is [feature] to your workflow?" (1-10 scale) + open text
- Route responses:
  - **Promoters (9-10):** Their success story becomes social proof in future spotlights for the same feature. "Join [N] users who discovered [feature] this month." Also feed into the the spotlight content pipeline workflow (see instructions below) as testimonial content for that feature.
  - **Passives (7-8):** Ask what would make the feature a 10. Feed responses to the product team and into the optimization loop as hypothesis inputs (e.g., "passives say the feature is hard to find after initial use — test adding a persistent shortcut after first try").
  - **Detractors (0-6):** Personal outreach. If a feature is not delivering value after adoption, the spotlight is driving trial of something that does not stick. Flag for product team review. If a feature consistently produces detractors, deprioritize it in the spotlight backlog.

- Track NPS by feature: features with high adopter NPS should be spotlighted more aggressively to remaining non-adopters. Features with low adopter NPS should be improved before being re-spotlighted.

### 4. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The spotlight series has found its local maximum for the current product, format, and audience
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for environmental changes: new user cohorts, product updates, seasonal patterns)
4. Generate a convergence report: "Feature Spotlight Series optimized. Current trial rate: [X]%. Adoption rate: [Y]%. Estimated ceiling: [Z]%. Further gains require strategic changes: new product features to spotlight, new user segments from growth, or product improvements to spotlighted features."
5. Shift agent resources to other plays that have not yet converged

### 5. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is trial rate holding at or above 25%?
- Is adoption rate holding at or above 15%?
- Is the optimization loop producing at least one experiment per month?
- Are weekly health reports being generated?
- Is feature backlog sustaining the series, or is intervention needed?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The series may have hit external limits (product maturity, audience saturation, competitive dynamics) that require strategic intervention, not tactical optimization.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiment infrastructure, Claude integration)
- 10 hours: Durable-depth health monitor with optimization tracking and longevity signals
- 10 hours: NPS feedback loop configuration for spotlight adopters
- 110 hours: Ongoing optimization cycles, experiment management, and reporting over 6 months (~4.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app spotlight variants for experiments, NPS surveys | ~$150-500/mo at scale — https://www.intercom.com/pricing |
| Loops | Email spotlight variants for experiments | Starter $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, pipeline automation | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report generation | ~$20-50/mo based on usage — https://www.anthropic.com/pricing |
| Attio | Series records, experiment audit trail, NPS data, spotlight backlog | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$250-600/mo (Intercom at scale + Anthropic API usage + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum for the spotlight series
- `autonomous-optimization` — series-level dashboard with optimization tracking, fatigue detection, and longevity signals
- `nps-feedback-loop` — collect and act on feedback from spotlight adopters to validate the series is driving real feature value
