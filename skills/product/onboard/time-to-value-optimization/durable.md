---
name: time-to-value-optimization-durable
description: >
  Time-to-Value Acceleration — Durable Intelligence. Always-on AI agents running the
  autonomous optimization loop: detect TTV regressions, generate hypotheses, run A/B
  experiments, evaluate results, auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% TTV improvement.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "Ongoing — 10 hours setup, then 2-3 hours/week agent-managed"
outcome: "Sustained or improving activation >=55% and TTV <8 minutes over 6+ months via autonomous optimization"
kpis: ["Median time to first value (minutes)", "Activation rate (%)", "Experiment velocity (experiments/month)", "Experiment win rate (%)", "Optimization convergence (% improvement per experiment)"]
slug: "time-to-value-optimization"
install: "npx gtm-skills add product/onboard/time-to-value-optimization"
drills:
  - autonomous-optimization
  - ttv-health-monitor
  - nps-feedback-loop
---

# Time-to-Value Acceleration — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The activation funnel maintains or improves its 55%+ activation rate and sub-8-minute median TTV for 6+ months without manual intervention. An always-on AI agent runs the monitor-diagnose-experiment-evaluate-implement loop. Weekly optimization briefs report what changed, what impact it had, and what the agent plans to test next. The system converges toward the local maximum — when 3 consecutive experiments produce less than 2% improvement, the agent reduces monitoring frequency and reports that tactical optimization has plateaued.

## Leading Indicators

- Autonomous optimization loop running: daily anomaly checks and at least 1 experiment per month
- Weekly TTV health briefs delivered on schedule with actionable content
- NPS survey data flowing and feeding back into hypothesis generation
- No manual intervention required for routine metric fluctuations
- Experiment velocity of 2-4 experiments per month in the first 3 months

## Instructions

### 1. Deploy the TTV health monitor

Run the `ttv-health-monitor` drill. Build the full monitoring infrastructure:

**Daily check workflow (n8n cron at 08:00 UTC):**
1. Query PostHog for yesterday's activation metrics: new signups, activations, median TTV, funnel step conversion rates
2. Compare against the 4-week rolling average using `posthog-anomaly-detection`
3. Classify each metric: normal (within +/-10%), warning (10-25% deviation), alert (>25% deviation)
4. For warnings and alerts, include context: which funnel step changed most, which segment was affected, any correlated product events (deploys, feature flag changes, traffic source shifts)
5. Log the daily check result to Attio on the play's campaign record

**Weekly health brief (n8n cron at Monday 09:00 UTC):**
1. Aggregate the week's metrics: total signups, activations, activation rate, median TTV with week-over-week comparison
2. Identify the best and worst performing segments
3. Call the funnel step with the biggest drop-off
4. List any anomalies detected during the week
5. Note any experiments currently running and their interim status
6. Generate the brief via Claude API with structured sections: Summary, Key Metrics, Biggest Opportunity, Segment Spotlight, Recommendations
7. Post to Slack and store in Attio

**Regression trip-wires:**
- Activation rate < 40% for 3 consecutive days: immediate alert
- Median TTV > 2x baseline for 2 consecutive days: immediate alert
- Any funnel step drops below 50% conversion when previously above 70%: immediate alert

These alerts bypass the daily summary and go directly to the team with a link to the PostHog dashboard and recent session recordings.

### 2. Launch the autonomous optimization loop

Run the `autonomous-optimization` drill. Configure it for this play's specific metrics:

**Phase 1 — Monitor (daily via n8n cron, fed by ttv-health-monitor):**
- Primary KPIs to watch: median TTV, activation rate, step completion rates
- Classification thresholds: normal (+/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, proceed to Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context from Attio: current onboarding configuration (which segments, which email variants, which product tour variants, which feature flags are active)
2. Pull 8-week metric history from PostHog dashboards
3. Run hypothesis generation via Claude API. Provide: the anomaly data, the current configuration, experiment history (what was already tested and what worked/failed), and NPS feedback themes
4. Receive 3 ranked hypotheses. Each hypothesis specifies: what to change, the expected impact on TTV or activation rate, the risk level, and the implementation mechanism (which tool to modify)
5. Store hypotheses in Attio as notes
6. If top hypothesis is "high risk" (affects >50% of users or changes the activation metric itself): send Slack alert for human approval and STOP
7. If "low" or "medium" risk: proceed to Phase 3

**Example hypotheses for this play:**
- "Shorten the product tour from 5 steps to 3 steps. Expected: TTV decreases 15% because users reach the core action faster. Risk: low. Implement via: PostHog feature flag toggling Intercom tour variant."
- "Change the Day-5 email from social proof to a personalized walkthrough video link. Expected: activation rate increases 8% for non-activated users. Risk: low. Implement via: Loops sequence variant."
- "Remove the profile completion step from the required onboarding path. Expected: TTV decreases 25% but activation quality may drop. Risk: medium. Implement via: PostHog feature flag skipping milestone_2."

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment using PostHog feature flags: control = current configuration, variant = hypothesis change
2. Implement the variant:
   - For email changes: create a variant sequence in Loops, route via feature flag
   - For product tour changes: create a variant tour in Intercom, trigger based on feature flag
   - For flow changes: toggle the feature flag in PostHog
3. Set minimum duration: 7 days or 100+ users per variant, whichever is longer
4. Log experiment start in Attio: hypothesis, start date, expected duration, success criteria, risk level

**Phase 4 — Evaluate (triggered by experiment reaching sample size or duration):**
1. Pull experiment results from PostHog: conversion rates, TTV distributions, and confidence intervals for control vs. variant
2. Run evaluation via Claude API with the experiment data
3. Decision tree:
   - **Adopt (p < 0.05, practical improvement >= 3%):** Update live configuration to use the winning variant. Disable the feature flag rollout. Log the change and its impact.
   - **Iterate (p < 0.05 but improvement < 3%):** The change works but impact is small. Generate a new hypothesis that builds on this result to find a bigger improvement. Return to Phase 2.
   - **Revert (p >= 0.05 or variant is worse):** Disable the variant, restore control. Log the failure and the learning. Return to Phase 1 monitoring.
   - **Extend (sample size insufficient after planned duration):** Keep running for another 7 days. If still insufficient after extension, revert and note insufficient traffic for this test.
4. Store the full evaluation in Attio: decision, confidence, reasoning, metric changes

**Phase 5 — Report (weekly via n8n cron, included in the TTV health brief):**
1. Add optimization activity to the weekly brief: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from all adopted changes this week
3. Estimate distance from local maximum based on the trend of experiment improvements
4. If the last 3 experiments produced <2% improvement each, flag convergence: "TTV optimization has reached its local maximum. Current performance: [metrics]. Further gains require strategic changes (new onboarding modality, product changes, different activation metric) rather than tactical optimization."

**Guardrails (critical):**
- Maximum 1 active experiment at a time for this play
- Auto-revert if activation rate drops >30% during an experiment
- Human approval required for: changes affecting >50% of traffic, changes to the activation metric definition, budget changes >20%
- 7-day cooldown after a failed experiment before testing the same variable
- Maximum 4 experiments per month. If all 4 fail, pause optimization and flag for human strategic review

### 3. Connect NPS feedback to the optimization loop

Run the `nps-feedback-loop` drill. Configure NPS surveys to fire at key onboarding moments:

- **Survey 1:** 30 days after activation — "How likely are you to recommend [product]? What was the hardest part of getting started?"
- **Survey 2:** Quarterly for retained users — "How likely are you to recommend [product]? What would make your experience better?"

Route NPS data into the optimization loop:
1. Aggregate open-text responses by theme (using Claude API for categorization): onboarding friction, missing features, confusion, value unclear, technical issues
2. Store themed summaries in Attio
3. The hypothesis generation step in Phase 2 receives NPS themes as input. If detractors consistently cite "too many steps to get started," this becomes a high-confidence hypothesis for the optimization loop to test.

For promoters: feed into the referral program. For detractors: trigger personal outreach (CSM or founder email within 48 hours).

### 4. Monitor convergence and long-term sustainability

The Durable level runs indefinitely. However, track the optimization trajectory:

- **Months 1-3:** Expect 2-4 experiments/month with several producing 5-15% improvements. Active optimization phase.
- **Months 3-6:** Expect experiment win rate to decline as easy wins are captured. Improvements per experiment decrease to 2-5%. Refinement phase.
- **Month 6+:** If 3 consecutive experiments produce <2% improvement, the play has reached its local maximum. Reduce daily checks to weekly. Report convergence to the team with the current performance level and what strategic changes (not tactical) could unlock the next level.

If external conditions change (product redesign, new market segment, competitor shift), reset the convergence counter and resume active optimization.

## Time Estimate

- 4 hours: Deploy ttv-health-monitor (daily checks, weekly brief, trip-wires)
- 4 hours: Configure autonomous-optimization loop (5 phases, guardrails, Attio logging)
- 2 hours: Set up NPS surveys and connect feedback to hypothesis generation
- 2-3 hours/week ongoing: Agent runs the loop; human reviews weekly briefs and approves high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Free up to 1M events/mo; usage-based after — https://posthog.com/pricing |
| Intercom | In-app NPS surveys, contextual messages, product tours | Advanced $85/seat/mo (annual) — https://www.intercom.com/pricing |
| Loops | Behavioral email sequences with variant support | Paid from $49/mo, scales with contacts — https://loops.so/pricing |
| Anthropic API | Hypothesis generation, experiment evaluation, brief generation | Sonnet 4.6: $3/M input, $15/M output tokens — https://platform.claude.com/docs/en/about-claude/pricing |
| n8n | Orchestration of all automation workflows | Self-hosted free; Cloud Starter EUR 24/mo — https://n8n.io/pricing |

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `ttv-health-monitor` — play-specific monitoring of TTV cohort trends, daily anomaly checks, and weekly health briefs
- `nps-feedback-loop` — qualitative feedback collection that feeds themes into hypothesis generation
