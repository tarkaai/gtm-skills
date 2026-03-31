---
name: public-sharing-durable
description: >
  Branded Public Sharing — Durable Intelligence. Autonomous AI agent monitors the
  share funnel, detects anomalies, generates improvement hypotheses, runs A/B
  experiments, auto-implements winners, and produces weekly optimization briefs.
  Converges when successive experiments yield <2% improvement.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Social"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Share rate sustained or improving >=30% over 6 months via autonomous optimization"
kpis: ["Public share rate", "Viewer-to-signup conversion", "Viral coefficient (K-factor)", "Experiment velocity (experiments/month)", "Cumulative AI lift (%)", "Share-acquired user 30-day retention"]
slug: "public-sharing"
install: "npx gtm-skills add product/referrals/public-sharing"
drills:
  - autonomous-optimization
---

# Branded Public Sharing — Durable Intelligence

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Social

## Outcomes

The public sharing funnel runs autonomously. An AI agent monitors all share metrics daily, detects when any metric deviates from baseline, generates hypotheses for improvement, runs A/B experiments via PostHog feature flags, evaluates results, and auto-implements winners. The share rate sustains or improves above 30% for 6 continuous months without manual intervention. The agent produces weekly optimization briefs documenting what changed, why, and what impact it had. The loop converges when 3 consecutive experiments produce less than 2% improvement — the play has reached its local maximum.

## Leading Indicators

- Daily anomaly detection runs without errors (the monitoring pipeline is healthy)
- At least 2 experiments per month are running (the optimization loop is active, not stalled)
- Weekly optimization briefs are generated on schedule (the reporting pipeline is healthy)
- No metric in critical status for more than 3 consecutive days (interventions are working)
- Cumulative AI lift trending positive month-over-month (experiments are producing improvements)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the core monitor-diagnose-experiment-evaluate-implement cycle for public sharing:

**Phase 1 — Monitor (daily via n8n cron):**
1. Use `posthog-anomaly-detection` to check the 6 primary KPIs: share rate, viewer-to-signup conversion, viral coefficient, share page views per share, CTA click-through rate, share-acquired user activation rate
2. Compare last 2 weeks against 4-week rolling average
3. Classify each KPI: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (>20% decline), **spike** (>50% increase)
4. If all normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Pull 8-week metric history from PostHog dashboards
2. Pull current share funnel configuration from Attio: active share surfaces, CTA variant, prompt timing, incentive structure, audience segments
3. Run `hypothesis-generation` with the anomaly data + configuration context
4. Receive 3 ranked hypotheses. Example hypotheses for share-specific anomalies:
   - Share rate plateau: "Prompt fatigue — users have seen the same share prompt too many times. Rotate to a new variant."
   - CTA decline: "Seasonal content shift — share content has changed character and the CTA no longer matches viewer expectations. Test a new CTA aligned to current content types."
   - Viral coefficient drop: "Share-acquired users are not reaching the share feature during onboarding. Add a share prompt to the onboarding flow for users with `acquisition_source=public-share`."
5. Store hypotheses in Attio
6. If top hypothesis is high-risk (audience change >50% or incentive change): send Slack alert and STOP for human review
7. If low or medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment: use `posthog-experiments` to create a feature flag splitting traffic between control (current) and variant (hypothesis change)
2. Implement the variant. Examples:
   - For CTA copy change: update the share page CTA text for the variant group via feature flag
   - For prompt timing change: adjust the Intercom trigger conditions for the variant group
   - For share surface addition: enable a new share surface via feature flag for the variant group only
3. Set duration: minimum 7 days or 200+ observations per variant, whichever is longer
4. Log in Attio: hypothesis, start date, expected duration, success criteria
5. **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments.

**Phase 4 — Evaluate (triggered by experiment end):**
1. Pull results from PostHog
2. Run `experiment-evaluation` with control vs. variant data
3. Decision:
   - **Adopt:** Variant wins with statistical significance. Roll out to 100%. Log the change and measured lift in Attio. Move to Phase 5.
   - **Iterate:** Results inconclusive or partially positive. Generate a refined hypothesis building on this result. Return to Phase 2.
   - **Revert:** Variant lost. Disable variant, restore control. Log the failure. Return to Phase 1.
4. **Revert threshold:** If share rate drops >30% at any point during an experiment, auto-revert immediately without waiting for the planned end date.

**Phase 5 — Report (weekly via n8n cron):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate cumulative AI lift: net change in each KPI from all adopted experiments since Durable start
3. Generate weekly brief:
   - What changed this week and why
   - Net impact on primary KPIs (share rate, conversion, viral coefficient)
   - Active experiments and expected completion dates
   - Distance from estimated local maximum (based on diminishing returns trend)
   - Recommended focus for next cycle
4. Post to Slack and store in Attio

### 2. Deploy share-specific health monitoring

Run the `autonomous-optimization` drill to layer play-specific monitoring on top of the autonomous optimization loop:

This drill monitors 8 share-specific metrics (share initiation rate, completion rate, page view rate, CTA CTR, signup conversion, activation rate, viral coefficient, content freshness) and triggers automated interventions for common failure modes:

- **Share prompt fatigue:** If share initiation rate declines for 2 weeks, auto-rotate the Intercom share prompt to a new variant
- **Completion stall:** If completion rate drops below 55%, enable a simplified one-click share flow via PostHog feature flag
- **CTA decay:** If CTA CTR drops below 5% for 2 weeks, queue a CTA A/B test in the experiment pipeline
- **Viewer re-engagement:** If a viewer clicks the CTA but abandons signup, trigger a Loops follow-up email within 1 hour
- **Viral loop boost:** If viral coefficient drops below 0.15, prompt share-acquired users who have been active 7+ days but have not shared

The health monitor generates a weekly performance report with: trend analysis, top-performing shares, intervention outcomes, viral loop analysis, and channel breakdown.

### 3. Manage convergence

The optimization loop should detect convergence: when 3 consecutive experiments produce less than 2% improvement on the primary KPI they targeted, the play has reached its local maximum for that variable.

At convergence for a specific variable:
1. Mark that variable as "optimized" in Attio
2. Shift experimentation focus to the next highest-leverage variable
3. Reduce monitoring frequency for the optimized variable from daily to weekly

At full convergence (all testable variables optimized):
1. Reduce overall monitoring frequency from daily to weekly
2. Generate a convergence report: "Public sharing has reached its local maximum. Current performance: [share rate], [conversion rate], [K-factor]. Further gains require strategic changes: new content types, new distribution channels, product changes to the share experience, or market expansion."
3. The agent continues weekly monitoring to detect if external changes (competitor moves, platform algorithm changes, seasonal effects) disrupt the optimized state. If disruption detected, re-enter the full optimization loop.

### 4. Guardrails

- **Experiment rate limit:** Maximum 1 active experiment per variable at a time. Maximum 4 experiments per month total.
- **Auto-revert:** If share rate drops >30% during any experiment, revert immediately.
- **Human approval required for:** incentive structure changes, changes affecting >50% of share page traffic, any change flagged as high-risk by hypothesis generation.
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable again.
- **Monthly cap:** If 4 experiments in a month all fail, pause the optimization loop and escalate for human strategic review.
- **Privacy guardrail:** Never expose user content publicly without the user's explicit opt-in action. The agent must never auto-enable sharing for users who have not clicked "share publicly."

## Time Estimate

- 20 hours: autonomous optimization loop setup (n8n workflows, PostHog anomaly detection, hypothesis generation prompts, experiment evaluation prompts)
- 10 hours: public share health monitor setup (8-metric dashboard, diagnostic triggers, automated interventions)
- 100 hours: ongoing autonomous operation over 6 months (~4 hours/week for monitoring, experimentation, and reporting — mostly automated, with periodic human review of weekly briefs)
- 10 hours: convergence analysis and documentation
- 10 hours: guardrail tuning and escalation handling

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, feature flags, dashboards | Growth: ~$100-200/mo at scale — https://posthog.com/pricing |
| n8n | Cron scheduling for monitoring, experiments, reports | Included in standard stack |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, weekly briefs | ~$20-50/mo at 4 experiments/mo — https://www.anthropic.com/pricing |
| Intercom | Automated share prompt rotation, interventions | ~$150-300/mo — https://www.intercom.com/pricing |
| Loops | Viewer re-engagement emails, lifecycle share CTAs | Included in standard stack |
| Attio | Experiment audit trail, campaign records, attribution | Included in standard stack |

**Play-specific cost:** ~$270-550/mo (PostHog Growth + Claude API + Intercom at scale)

## Drills Referenced

- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds and maintains the local maximum for public sharing performance
- `autonomous-optimization` — play-specific monitoring of 8 share funnel metrics with diagnostic triggers, automated interventions, and weekly performance reports
