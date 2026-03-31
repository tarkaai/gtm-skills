---
name: email-reengagement-inactive-durable
description: >
  Inactive User Re-engagement — Durable Intelligence. The autonomous-optimization
  drill runs the core loop: detect metric anomalies in reengagement performance,
  generate hypotheses for email/timing/cohort improvements, run A/B experiments,
  evaluate results, and auto-implement winners. Weekly optimization briefs.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Durable Intelligence"
time: "8 hours setup + ongoing autonomous operation over 6 months"
outcome: "Sustained or improving >=18% return rate over 6 months via autonomous optimization"
kpis: ["Return rate per cohort (weekly trend)", "Reactivation rate per cohort", "Experiment velocity (tests/month)", "Cumulative optimization lift", "Convergence status", "Optimization brief cadence"]
slug: "email-reengagement-inactive"
install: "npx gtm-skills add product/winback/email-reengagement-inactive"
drills:
  - autonomous-optimization
  - inactive-reengagement-health-monitor
---

# Inactive User Re-engagement — Durable Intelligence

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

The reengagement system runs autonomously with AI agents detecting metric anomalies, generating improvement hypotheses, running experiments, and auto-implementing winners. Return rate sustains at >=18% or improves over 6 months. The system finds its local maximum — the best possible reengagement performance given the current product, audience, and competitive landscape — and maintains it as conditions change. Weekly optimization briefs document every change and its impact.

## Leading Indicators

- The `autonomous-optimization` loop fires at least once per week (daily monitor detects anomalies or opportunities)
- Experiments complete within 2-week cycles with statistical significance
- Cumulative optimization lift trends upward (each winning experiment adds measurable return rate improvement)
- Weekly optimization briefs are generated on schedule with actionable recommendations
- No manual intervention required for routine operations for 4+ consecutive weeks

## Instructions

### 1. Deploy the reengagement health monitor

Run the `inactive-reengagement-health-monitor` drill to set up the monitoring layer:

1. Build the PostHog "Reengagement Health" dashboard with 6 panels: sequence funnel waterfall, return rate trend by cohort, email performance heatmap, reactivation quality, unsubscribe rate trend, and cohort volume tracker.
2. Deploy the daily n8n check workflow (09:00 UTC) that queries PostHog for reengagement metrics, compares against 4-week rolling averages, and classifies each metric as normal, warning, or critical.
3. Deploy the weekly n8n brief workflow (Monday 09:00 UTC) that aggregates weekly data and generates a structured health brief via Claude API.
4. Configure regression trip-wires: return rate below threshold for 3 consecutive days, open rate collapse, unsubscribe spike, or sequence entry gap.

This monitor feeds signals directly into the `autonomous-optimization` drill's Phase 1.

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for this play's specific context:

**Phase 1 — Monitor (daily via n8n cron):**
- The `inactive-reengagement-health-monitor` provides daily anomaly classifications
- The optimization loop reads these from Attio notes on the play's campaign record
- Anomaly triggers: any cohort's return rate drops >10% below 4-week average, any email step's open rate drops >15% below average, reactivation rate drops below 8%, or an experiment opportunity is detected (a metric has been flat for 3+ weeks)

**Phase 2 — Diagnose (triggered by anomaly or opportunity):**
- Pull context from Attio: current sequence configuration per cohort (subject lines, CTAs, send timing, conditional branches), past experiment results, current A/B test learnings from Scalable level
- Pull 8-week metric history from the reengagement health dashboard
- Run `hypothesis-generation` with the anomaly data + context
- Receive 3 ranked hypotheses. Examples of hypothesis categories for this play:
  - **Subject line hypothesis:** "Changing the 14-30d cohort Email 1 subject from [current] to [proposed] will increase open rate by X% because [reasoning from past test data]"
  - **Send timing hypothesis:** "Shifting the 60-90d cohort send time from morning to evening will increase open rate by X% because this cohort's last active sessions were predominantly evening"
  - **CTA hypothesis:** "Replacing the 'What's New' landing page CTA with a direct deep-link to the user's most-used feature will increase click rate by X% because Scalable A/B test showed deep-links outperform landing pages by Y%"
  - **Cohort boundary hypothesis:** "Splitting the 14-30d cohort into 14-21d and 21-30d with different messaging urgency will increase overall return rate by X%"
  - **Sequence length hypothesis:** "Adding a 4th email to the 7-14d cohort at day 10 will increase return rate by X% because this cohort's return curve shows late responders"

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use `posthog-experiments` to create a feature flag splitting the target cohort: 50% control (current sequence), 50% variant (hypothesis change)
- Implement the variant in Loops: create a parallel sequence variant or modify send timing via n8n
- Minimum experiment duration: 14 days or 200 users per variant, whichever is longer
- Log experiment start in Attio: hypothesis, cohort, variant description, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run `experiment-evaluation`:
  - **Adopt:** Variant beat control with >=95% confidence AND >=2% absolute improvement in the target metric. Update the live Loops sequence to use the winning variant. Log the change in Attio.
  - **Iterate:** Result was directionally positive but not significant. Generate a refined hypothesis building on this result. Return to Phase 2.
  - **Revert:** Variant performed worse than control. Disable the variant, restore control. Log the failure with reasoning. Return to Phase 1.
  - **Extend:** Insufficient sample size. Extend the experiment for another 7 days. Set a reminder.

**Phase 5 — Report (weekly via n8n cron):**
- The weekly optimization brief aggregates: anomalies detected, hypotheses generated, experiments run, decisions made, net metric change from adopted changes
- Calculate cumulative optimization lift: total return rate improvement from all adopted experiments since Durable began
- Assess convergence: if the last 3 experiments each produced <2% improvement, the play has reached its local maximum
- Post the brief to Slack and store in Attio

### 3. Configure guardrails

Apply the standard `autonomous-optimization` guardrails plus play-specific ones:

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments across cohorts simultaneously (cross-contamination risk).
- **Revert threshold:** If any cohort's return rate drops >30% during an experiment, auto-revert immediately.
- **Unsubscribe guardrail:** If any experiment causes unsubscribe rate to exceed 1% on any email step, auto-revert and flag for human review.
- **Human approval required for:**
  - Adding or removing entire cohorts (changes the addressable population)
  - Adding emails to a sequence beyond 4 steps (frequency risk)
  - Any hypothesis that changes the incentive structure (adding discounts, extending trials)
  - Any experiment the hypothesis generator flags as "high risk"
- **Cooldown:** After a reverted experiment, wait 7 days before testing the same variable on the same cohort.
- **Monthly experiment cap:** 4 experiments per month. If all 4 fail in a month, pause optimization and flag for human strategic review: the play may need a product-level change (better re-entry UX, new features to highlight) rather than email optimization.
- **Deliverability guardrail:** If Loops bounce rate exceeds 3% or spam complaint rate exceeds 0.1%, pause all sequences immediately and run list hygiene before resuming.

### 4. Handle convergence

When the optimization loop detects convergence (<2% improvement for 3 consecutive experiments):

1. The play has reached its local maximum for email-based reengagement
2. Reduce the daily monitor to weekly checks
3. Keep the sequences running — they are optimized and generating returns
4. Generate a convergence report:
   - Final optimized configuration per cohort (subject lines, CTAs, timing, sequence length)
   - Return rate at convergence vs. return rate at start of Durable
   - Total cumulative lift from all experiments
   - Recommended next frontier: to improve further, the play would need strategic changes beyond email optimization — better product re-entry UX, in-app reengagement flows, push notifications, or addressing the root causes of inactivity
5. The agent shifts optimization effort to other plays while maintaining this one on autopilot

### 5. Evaluate sustainability

After 6 months, measure:
- Primary: return rate sustained at >=18% (or improved) across all cohorts
- Experiment velocity: at least 2 experiments per month were run and evaluated
- Cumulative optimization lift: total improvement from Durable experiments documented
- Convergence: did the play reach its local maximum? If so, at what return rate?
- Autonomous operation: how many weeks ran without human intervention?

This level runs continuously. If return rate decays below threshold, the optimization loop auto-detects and triggers a new cycle of hypotheses and experiments.

## Time Estimate

- 3 hours: Deploy reengagement health monitor (dashboard + daily/weekly n8n workflows)
- 3 hours: Configure autonomous optimization loop (n8n workflows, Attio records, guardrails)
- 2 hours: Validate end-to-end: trigger a test anomaly, verify hypothesis generation fires, verify experiment setup works
- Ongoing: autonomous operation. Human reviews weekly briefs (~30 min/week) and approves high-risk experiments when flagged

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments/feature flags, dashboards, funnels | Free up to 1M events/mo; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Reengagement sequences (4+ cohort variants, A/B experiment variants) | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Daily monitor, weekly brief, optimization loop orchestration | Self-hosted free; Cloud from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Intercom | In-app welcome-back messages (carried from Scalable) | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation, weekly brief generation | Usage-based ~$15-30/mo at this volume ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated play-specific cost:** $117-182/mo (Loops + n8n + Intercom + Anthropic API)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: detect metric anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly optimization briefs. This is what makes Durable fundamentally different from Scalable.
- `inactive-reengagement-health-monitor` — play-specific monitoring that feeds signals to the optimization loop: daily metric checks, weekly health briefs, regression trip-wires, and structured signal data in Attio
