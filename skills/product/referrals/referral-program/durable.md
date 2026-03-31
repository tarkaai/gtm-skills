---
name: referral-program-durable
description: >
  Incentivized Referral Program — Durable Intelligence. AI agents autonomously monitor
  referral metrics, detect anomalies, generate improvement hypotheses, run A/B experiments,
  and auto-implement winners. Finds and maintains the referral program's local maximum.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Durable Intelligence"
time: "20 hours setup + continuous autonomous operation"
outcome: "Referral rate sustained or improving >=8% over 3+ months with autonomous optimization; successive experiments produce <2% improvement (convergence)"
kpis: ["Referral rate (trailing 30-day)", "Referee activation rate", "Referral CAC", "Viral coefficient", "Experiment velocity (experiments/month)", "Optimization lift (cumulative % improvement from experiments)", "Convergence status"]
slug: "referral-program"
install: "npx gtm-skills add product/referrals/referral-program"
drills:
  - autonomous-optimization
  - referral-health-monitor
---

# Incentivized Referral Program — Durable Intelligence

> **Stage:** Product > Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

The referral program runs autonomously with AI agents monitoring metrics, detecting anomalies, generating hypotheses, running experiments, and implementing winners. Referral rate sustains or improves >=8% over 3+ consecutive months. The optimization loop converges when successive experiments produce <2% improvement for 3 consecutive experiments, indicating the program has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop executing without human intervention (daily monitoring, weekly briefs)
- At least 1 experiment running or recently completed at all times
- No referral health metrics in "critical" status for more than 48 hours
- Optimization lift trending positive (cumulative improvement from adopted experiments)
- Weekly optimization briefs being generated and posted to Slack
- Referral CAC staying below 50% of paid acquisition CAC as optimizations run

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the referral program. Set up the 5-phase loop:

**Phase 1 -- Monitor (daily via n8n cron):**
Use `posthog-anomaly-detection` to check the referral program's primary KPIs: referral rate, referee activation rate, referral CAC, and viral coefficient. Compare last 2 weeks against 4-week rolling average. Classify: normal (within +/-10%), plateau (+/-2% for 3+ weeks), drop (>20% decline), spike (>50% increase). If anomaly detected, trigger Phase 2.

**Phase 2 -- Diagnose (triggered by anomaly):**
Gather context from Attio: current referral surfaces, incentive structure, prompt timing, top referrer segments. Pull 8-week metric history from PostHog. Run `hypothesis-generation` with the anomaly data + context. Receive 3 ranked hypotheses with expected impact and risk. Store in Attio as notes. If top hypothesis is "high risk" (e.g., changing the reward structure entirely), send Slack alert for human review and stop. Otherwise proceed.

**Phase 3 -- Experiment (triggered by hypothesis acceptance):**
Use `posthog-experiments` to create a feature flag splitting traffic between control (current) and variant (hypothesis change). Examples of referral-specific experiments:
- Changing the referral prompt copy on the highest-traffic surface
- Adjusting the reward value (e.g., 2 weeks free vs 1 month free)
- Changing the trigger timing for the post-milestone referral prompt
- Testing a new share mechanic (pre-populated email vs social share button)

Set minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer. Maximum 1 active experiment at a time on the referral program. Log experiment start in Attio.

**Phase 4 -- Evaluate (triggered by experiment completion):**
Pull results from PostHog. Run `experiment-evaluation`. Decision tree:
- **Adopt (95% confidence, positive lift):** Implement the winning variant as the new default. Log the change and the lift.
- **Iterate (inconclusive or small lift):** Generate a new hypothesis building on the result. Return to Phase 2.
- **Revert (negative result or guardrail breach):** Disable the variant, restore control. Wait 7 days before testing the same variable again.
- **Extend (trending positive but insufficient sample):** Keep running for another period.

Store the full evaluation in Attio: hypothesis, variants tested, sample sizes, confidence level, decision, and reasoning.

**Phase 5 -- Report (weekly via n8n cron):**
Aggregate all optimization activity for the week. Generate a brief:
- Anomalies detected and their classification
- Experiments running, completed, or queued
- Net metric change from adopted experiments
- Current referral rate, viral coefficient, and referral CAC
- Distance from estimated local maximum
- Convergence status: are successive experiments producing diminishing returns?

Post to Slack and store in Attio.

### 2. Deploy referral-specific health monitoring

Run the `referral-health-monitor` drill. This provides the play-specific monitoring layer that feeds into the autonomous optimization loop:

- 8 referral health metrics tracked daily: referral rate, share-to-signup conversion, referee activation, reward fulfillment, referral CAC, referrer retention, viral coefficient, referred user quality
- Diagnostic triggers for each declining metric (e.g., referral rate declining -> check prompt delivery rate, check if top referrers went quiet, check if new user dilution)
- 4 automated interventions:
  - Rotate stale referral prompt copy when click rate drops below 2%
  - Extra referee onboarding nudge when 7-day activation drops below 25%
  - Re-engagement message to top referrers gone quiet for 60+ days
  - Immediate escalation for reward fulfillment backlog (pending >48 hours)
- Weekly health report with metric trends, intervention outcomes, and escalation flags

The health monitor's diagnostics feed directly into Phase 2 (Diagnose) of the autonomous optimization loop. When the health monitor detects a warning or critical metric, it provides the anomaly context that the optimization loop uses to generate hypotheses.

### 3. Configure guardrails

These guardrails override the optimization loop and prevent harmful experiments:

- **Reward budget guardrail:** If total referral reward cost in a month exceeds 120% of the planned budget, pause all reward-increasing experiments and alert.
- **Revert threshold:** If referral rate drops >30% during an experiment, auto-revert immediately.
- **Quality guardrail:** If referred user 30-day retention drops below 70% of organic user retention for 2 consecutive weeks, pause the referral program for review. The program may be attracting low-quality users.
- **Human approval required for:** reward value changes >25%, incentive structure changes (e.g., switching from two-sided to tiered), any change affecting >50% of referral traffic.
- **Cooldown:** After a failed experiment (reverted), wait 7 days before testing the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.

### 4. Detect and report convergence

The optimization loop should detect convergence -- when the referral program has reached its local maximum:

- Track the lift from each successive adopted experiment
- If 3 consecutive experiments produce <2% improvement each, the program has converged
- At convergence:
  1. Reduce monitoring frequency from daily to weekly
  2. Reduce experiment cadence from continuous to monthly check-ins
  3. Report: "Referral program optimized. Current performance: [referral rate]% rate, [viral coefficient] viral coefficient, $[CAC] referral CAC. Further gains require strategic changes (new incentive model, new channels, product changes) rather than tactical optimization."

**Human action required:** Review the convergence report. Decide whether to accept the local maximum or invest in strategic changes to shift the performance ceiling.

## Time Estimate

- 8 hours: configure the autonomous optimization loop (n8n workflows, PostHog experiments setup, Attio logging, Slack alerts)
- 6 hours: deploy the referral health monitor (8 metric definitions, diagnostic triggers, automated interventions)
- 4 hours: configure guardrails and escalation rules
- 2 hours: validate end-to-end loop with a test anomaly injection
- Continuous: autonomous operation requires ~1 hour/week of human review (reading weekly briefs, approving high-risk experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Anomaly detection, experiments/feature flags, funnel analysis, dashboards | Free up to 1M events/mo and 1M flag requests; usage-based after ([posthog.com/pricing](https://posthog.com/pricing)) |
| n8n | Optimization loop scheduling (daily monitor, weekly report), intervention triggers | EUR 60/mo Pro for 10K executions; free self-hosted ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Anthropic API | Hypothesis generation and experiment evaluation (Claude) | Usage-based; ~$3-15/1K input tokens depending on model ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |
| Intercom | In-app message rotation, referral prompt variant deployment | From $29/seat/mo; Proactive Support $349/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Referee onboarding nudges, referrer re-engagement, reward notifications | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Experiment logging, referral program records, optimization history | $29/user/mo Plus ([attio.com](https://attio.com)) |

**Estimated play-specific cost at this level:** $150-400/mo (n8n Pro + Anthropic API usage for hypothesis/evaluation + incremental Intercom/PostHog/Loops usage)

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor metrics, detect anomalies, generate hypotheses, run A/B experiments, evaluate results, auto-implement winners, generate weekly briefs
- `referral-health-monitor` -- referral-specific daily health checks on 8 metrics, diagnostic triggers for each declining metric, automated interventions for common failure modes, weekly health reports with convergence detection
