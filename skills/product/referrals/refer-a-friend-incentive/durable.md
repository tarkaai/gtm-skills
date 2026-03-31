---
name: refer-a-friend-incentive-durable
description: >
  Referral Rewards Program — Durable Intelligence. Deploy the autonomous optimization
  loop to continuously detect referral metric anomalies, generate improvement hypotheses,
  run A/B experiments, and auto-implement winners. Sustain >=10% referral rate and
  >=0.2 viral coefficient over 6 months via AI-driven optimization.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Sustained or improving referral rate >=10% and viral coefficient >=0.2 over 6 months via autonomous optimization"
kpis: ["Referral rate (trailing 4-week)", "Viral coefficient", "Experiment velocity (experiments/month)", "AI lift (cumulative improvement from experiments)", "Referrer retention at 90 days", "Referee quality (day-30 retention)", "Reward cost per acquisition", "Optimization convergence status"]
slug: "refer-a-friend-incentive"
install: "npx gtm-skills add product/referrals/refer-a-friend-incentive"
drills:
  - autonomous-optimization
---

# Referral Rewards Program — Durable Intelligence

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Deploy the always-on AI optimization loop that monitors referral metrics daily, detects anomalies, generates improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. Sustain or improve the referral rate at >=10% and viral coefficient at >=0.2 over 6 months. The agent finds the local maximum of the referral program and maintains it as user behavior and market conditions shift.

## Leading Indicators

- Daily health checks run without errors for 7 consecutive days after deployment
- First anomaly is detected and diagnosed within the first 2 weeks (proving the monitor works)
- First automated experiment launches within the first month
- At least 1 experiment produces a statistically significant improvement in the first 2 months
- Weekly optimization briefs are generated on schedule and contain actionable insights
- No metric enters "critical" status for more than 3 consecutive days without intervention
- Automated interventions fire correctly when triggered (verify with the first 2-3 events)

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the referral program:

**Monitor phase (daily via n8n cron):**
- Use `posthog-anomaly-detection` to check the 8 referral KPIs daily: referral rate, share-to-signup conversion, signup-to-activate conversion, reward fulfillment rate, viral coefficient, referrer retention, referee quality, reward cost efficiency
- Compare last 2 weeks against 4-week rolling average
- Classify each metric: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If all normal: log to Attio, no action
- If anomaly detected: trigger the diagnose phase

**Diagnose phase (triggered by anomaly):**
- Gather the referral program's current configuration from Attio: incentive structure per segment, prompt timing, email sequence copy, feature flag allocations
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` with the anomaly data + configuration context
- Receive 3 ranked hypotheses with expected impact and risk
- Store hypotheses in Attio as notes
- If top hypothesis is "high risk" (changes incentive structure, affects >50% of users, or modifies reward value): send Slack alert for human review and STOP
- If "low" or "medium" risk: proceed to experiment

**Experiment phase (triggered by hypothesis acceptance):**
- Take the top-ranked hypothesis (e.g., "Changing the referral prompt from post-workflow to post-milestone will increase share rate by 3pp because milestone moments have higher emotional valence")
- Use `posthog-experiments` to create an A/B test: control = current configuration, treatment = hypothesis change
- Implement the treatment using the appropriate tool: Intercom for in-app prompt changes, Loops for email changes, feature flags for incentive variant changes
- Run for minimum 7 days or until 100+ samples per variant
- Log experiment start in Attio

**Evaluate phase (triggered by experiment completion):**
- Pull results from PostHog
- Run `experiment-evaluation`:
  - **Adopt**: winning variant is statistically significant at 95% with practical significance >=2pp improvement. Update live config. Log the change.
  - **Iterate**: results are directionally positive but not significant. Generate a refined hypothesis and return to diagnose.
  - **Revert**: treatment performed worse. Disable variant, restore control. Log the failure. Return to monitoring.
  - **Extend**: insufficient sample size. Keep running for another week.
- Store full evaluation in Attio

**Report phase (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on referral rate and viral coefficient
  - Cumulative AI lift since Durable launch (total improvement attributable to automated experiments)
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Deploy the referral health monitor

Run the `autonomous-optimization` drill to build the play-specific monitoring layer that complements the generic optimization loop:

- Configure the 8 referral health metrics with healthy/warning/critical thresholds
- Build the daily health check workflow (independent of the optimization loop's anomaly detection — this is a parallel safety net)
- Implement diagnostic triggers for each metric: referral rate declining, share-to-signup conversion declining, fulfillment rate declining, viral coefficient declining, referrer retention declining, referee quality declining
- Deploy 5 automated interventions:
  - Stale referral prompt: auto-rotate Intercom message variant when click rate drops below 3%
  - Sharing drought: trigger bonus reward campaign to top 50 referrers when shares drop 30%+ week over week
  - Fulfillment failure: auto-retry failed rewards and send apology when fulfillment rate drops below 90%
  - Referee drop-off: trigger extra onboarding email when signup-to-activate drops below 30%
  - Referrer burnout: re-engagement email to lapsed referrers who stopped sharing after 3+ previous referrals
- Set escalation rules: any metric critical 3+ days, viral coefficient <0.1 for 2 weeks, fulfillment rate <85% for 3 days, or 3+ interventions with no improvement

### 3. Configure guardrails

Apply the `autonomous-optimization` guardrails to the referral program:

- **Rate limit**: maximum 1 active referral experiment at a time. Never stack experiments on the referral program.
- **Revert threshold**: if referral rate drops >30% at any point during an experiment, auto-revert immediately
- **Human approval required for**: incentive value changes (increasing or decreasing reward), eligibility criteria changes (who can refer), changes affecting >50% of the referral-eligible user base
- **Cooldown**: after a failed experiment, wait 7 days before testing a new hypothesis on the same variable (e.g., do not test two different prompt copy changes back-to-back)
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never optimize what is not measured**: if a new referral channel emerges that is not tracked in PostHog, add tracking (via `posthog-gtm-events`) before running experiments on it

### 4. Evaluate sustainability

This level runs continuously. Monthly review:

- Is referral rate sustained at >=10%? Is viral coefficient sustained at >=0.2?
- What is the cumulative AI lift? (Total referral rate improvement attributable to Durable-level experiments)
- What is the experiment velocity? (Target: 2-4 experiments/month in the first 3 months, tapering as convergence approaches)
- Has the optimization loop detected convergence? (3 consecutive experiments producing <2% improvement)

At convergence:
1. The referral program has reached its local maximum
2. Reduce monitoring frequency from daily to weekly
3. Report: "Referral program optimized. Current referral rate: [X]%. Viral coefficient: [Y]. Further gains require strategic changes (new referral surfaces, new user segments, product changes) rather than tactical optimization."

## Time Estimate

- 16 hours: configure autonomous optimization loop (monitor, diagnose, experiment, evaluate, report workflows in n8n)
- 12 hours: deploy referral health monitor (8 metrics, diagnostics, interventions, escalation)
- 8 hours: configure guardrails and test all automation paths
- 8 hours: month 1 monitoring — verify the loop runs correctly, intervene on misconfigurations
- 36 hours: months 2-6 ongoing monitoring — weekly brief review, monthly strategic assessment, escalation handling (~1.5 hours/week)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments, dashboards, cohorts | Free tier: 1M events/mo; may need paid for experiment volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Transactional reward emails, sequence variants for experiments | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app prompt rotation, intervention messages | Essential: $29/seat/mo annual ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Attio | Experiment log, hypothesis tracking, weekly briefs | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation | Usage-based; ~$5-15/mo at 2-4 experiments/mo ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated play-specific cost at this level:** $85-195/mo (Loops $49 + Intercom $29/seat + Claude API ~$5-15 + PostHog may exceed free tier at scale)

## Drills Referenced

- `autonomous-optimization` — the core Durable loop: monitor metrics for anomalies, generate improvement hypotheses via Claude, run A/B experiments in PostHog, evaluate results, auto-implement winners, generate weekly optimization briefs
- `autonomous-optimization` — play-specific monitoring layer: 8 referral health metrics, diagnostic triggers for each failure mode, 5 automated interventions, weekly health reports, and escalation rules for human handoff
