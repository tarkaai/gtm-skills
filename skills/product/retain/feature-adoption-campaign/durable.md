---
name: feature-adoption-campaign-durable
description: >
  Targeted Adoption Campaigns — Durable Intelligence. Autonomous optimization loop that detects
  adoption anomalies, generates hypotheses, runs experiments, and auto-implements winners to
  sustain and improve feature adoption across all segments.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving CTR ≥35% and adoption ≥25% over 6 months via autonomous optimization"
kpis: ["Overall adoption rate", "Experiment velocity", "Optimization lift", "Campaign fatigue index", "Distance from local maximum"]
slug: "feature-adoption-campaign"
install: "npx gtm-skills add product/retain/feature-adoption-campaign"
drills:
  - autonomous-optimization
  - adoption-campaign-health-report
  - nps-feedback-loop
---

# Targeted Adoption Campaigns — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Feature adoption rate sustained at or above 25% and campaign CTR sustained at or above 35% for 6 consecutive months. The autonomous optimization loop continuously detects performance changes, generates improvement hypotheses, runs A/B experiments, and auto-implements winners. Weekly health reports track progress toward the local maximum. When successive experiments produce less than 2% improvement, the campaign has converged and shifts to maintenance mode.

## Leading Indicators

- Anomaly detection catching metric shifts within 24 hours (the monitoring loop is working)
- At least 2 experiments completed per month with documented outcomes
- Winning experiments producing measurable lift (>3% improvement in targeted metric)
- Campaign fatigue index stable or declining (messages are not wearing out)
- NPS feedback from feature adopters trending positive (the feature delivers real value)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on monitor-diagnose-experiment-evaluate-implement cycle for this campaign:

**Monitor (daily via n8n cron):**
- Query PostHog for the campaign's primary KPIs: overall adoption rate, per-segment adoption rates, campaign CTR, dismissal rate, 7-day retention
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: **normal** (within +/-10%), **plateau** (+/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
- If all metrics normal, log to Attio and take no action
- If any anomaly detected, proceed to diagnosis

**Diagnose (triggered by anomaly):**
- Pull the campaign's current configuration from Attio: active segments, messaging variants, channel mix, experiment history
- Pull 8-week metric history from PostHog
- Generate 3 ranked hypotheses using Claude. Examples of hypotheses the agent might generate:
  - "Adoption rate dropped 18% in the power-user segment because the current message has been shown for 6 weeks — test a new value proposition focusing on the feature's latest improvements"
  - "CTR is plateauing because in-app tooltips are shown on page load — test triggering the message after the user completes a related action instead"
  - "Retention decay in the new-signups segment suggests the feature's first-run experience is confusing — test adding a 30-second product tour before the first use"
- Store hypotheses in Attio. If top hypothesis is high-risk (affects >50% of traffic or requires budget change >20%), send Slack alert for human review and stop.

**Experiment (triggered by hypothesis acceptance):**
- Create a PostHog feature flag splitting the affected segment between control (current) and variant (hypothesis change)
- Implement the variant: if the hypothesis targets message copy, update the Intercom message or Loops email; if the hypothesis targets timing, adjust the n8n trigger; if the hypothesis targets channel, configure the new channel
- Run for minimum 7 days or until 100+ samples per variant
- Log experiment start in Attio: hypothesis, segment, start date, expected duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog experiments API
- Decision tree:
  - **Adopt:** Variant outperforms control with >95% confidence and >3% improvement. Update the live campaign configuration. Log the change.
  - **Iterate:** Results inconclusive or marginal. Generate a refined hypothesis building on this result. Return to diagnosis.
  - **Revert:** Variant underperforms control. Disable the variant, restore control. Log the failure. Wait 7 days before testing the same variable.
  - **Extend:** Insufficient sample size. Continue for another period.

**Guardrails:**
- Maximum 1 active experiment per segment at a time
- If primary metric drops >30% during any experiment, auto-revert immediately
- Maximum 4 experiments per month per play. If all 4 fail, pause optimization and flag for human strategic review
- Never experiment on what is not measured — if a KPI lacks PostHog tracking, fix tracking first

### 2. Generate weekly health reports

Run the `adoption-campaign-health-report` drill to produce a structured weekly brief every Monday:

The report covers:
- **Per-segment performance table:** reach, engagement, conversion, retention, and trend vs. 4-week average for each active segment
- **Experiment outcomes:** what was tested, what happened, what was decided, and net impact
- **Signal detection:** campaign fatigue (engagement declining 3+ weeks), adoption plateau (rate flat 3+ weeks), retention decay (adopters dropping off), segment exhaustion (addressable population depleted)
- **AI-generated recommendation:** one specific experiment to run next week, with hypothesis and expected impact
- **Distance from local maximum:** current adoption rate vs. estimated ceiling based on diminishing experiment returns

The report is posted to Slack and stored in Attio. "Act"-severity signals automatically feed into the optimization loop as the next hypothesis to test.

### 3. Close the feedback loop with adopters

Run the `nps-feedback-loop` drill targeted specifically at feature adopters:

- Survey users who adopted the feature 30+ days ago: "How useful is [feature] to your workflow?" (1-10 scale) + open text
- Route responses:
  - **Promoters (9-10):** Ask for a testimonial or case study. Their quotes become social proof in campaign messages for other segments.
  - **Passives (7-8):** Ask what would make the feature a 10. Feed responses to the product team and into the optimization loop as hypothesis inputs.
  - **Detractors (0-6):** Personal outreach. If the feature is not delivering value for adopters, the campaign is driving adoption of something that does not stick. Flag for product review.
- Track NPS by segment: if one segment's adopters score consistently lower, the campaign messaging may be over-promising for that segment.

### 4. Detect convergence and shift to maintenance

The optimization loop runs indefinitely until it detects convergence: 3 consecutive experiments producing less than 2% improvement. At convergence:

1. The campaign has found its local maximum for the current feature, messaging, and audience
2. Reduce monitoring frequency from daily to weekly
3. Reduce experiment velocity to 1 per month (maintenance testing for environmental changes)
4. Generate a convergence report: "Feature adoption campaign optimized. Current adoption rate: [X]%. Estimated ceiling: [Y]%. Further gains require strategic changes: new features to campaign for, new user segments to target, or product improvements to the feature itself."
5. Shift agent resources to other campaigns that have not yet converged

### 5. Continuous evaluation

This level runs continuously. Monthly check-in metrics:
- Is overall adoption rate holding at or above 25%?
- Is CTR holding at or above 35%?
- Is the optimization loop producing at least one experiment per month?
- Are weekly health reports being generated and reviewed?

If any metric degrades for 2 consecutive months despite optimization, escalate to human review. The campaign may have hit external limits (market changes, competitive dynamics, feature staleness) that require strategic intervention, not tactical optimization.

## Time Estimate

- 20 hours: Autonomous optimization loop setup (n8n workflows, PostHog experiment infrastructure, Claude integration)
- 10 hours: Weekly health report automation setup
- 10 hours: NPS feedback loop configuration for feature adopters
- 110 hours: Ongoing optimization cycles, experiment management, and reporting over 6 months (~4.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, funnels, dashboards | Growth from $0.00045/event — https://posthog.com/pricing |
| Intercom | In-app message variants for experiments, NPS surveys | ~$150-500/mo at scale — https://www.intercom.com/pricing |
| Loops | Email sequence variants for experiments | Starter $49/mo — https://loops.so/pricing |
| n8n | Optimization loop scheduling, webhook orchestration | Free self-hosted; Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, report summarization | ~$20-50/mo based on usage — https://www.anthropic.com/pricing |
| Attio | Campaign records, experiment audit trail, NPS data | From $0/mo (free tier) — https://attio.com/pricing |

**Play-specific cost:** ~$250-600/mo (Intercom at scale + Anthropic API usage + PostHog Growth tier)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate loop that finds the local maximum
- `adoption-campaign-health-report` — weekly structured report with per-segment performance, experiment outcomes, and signal detection
- `nps-feedback-loop` — collect and act on feedback from feature adopters to validate the campaign is driving real value
