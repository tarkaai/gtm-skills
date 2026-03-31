---
name: invite-mechanism-durable
description: >
  Team Invite System — Durable Intelligence. Always-on AI agents monitor invite funnel
  health, detect metric anomalies, generate improvement hypotheses, run experiments, and
  auto-implement winners. The autonomous-optimization loop finds the local maximum of invite
  rate, acceptance rate, and viral coefficient, then maintains it as conditions change.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Upsell"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + continuous"
outcome: "Invite rate and acceptance rate sustained or improving for 6+ months via autonomous optimization; viral coefficient k >= 0.2 maintained"
kpis: ["Invite rate (sustained)", "Acceptance rate (sustained)", "Viral coefficient k (sustained)", "Experiment velocity (experiments/month)", "Autonomous lift (% improvement from agent-run experiments)", "Seat expansion revenue"]
slug: "invite-mechanism"
install: "npx gtm-skills add product/upsell/invite-mechanism"
drills:
  - autonomous-optimization
---

# Team Invite System — Durable Intelligence

> **Stage:** Product > Upsell | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The invite mechanism runs on autopilot with AI agents monitoring, diagnosing, experimenting, and optimizing. The `autonomous-optimization` drill creates the core loop: detect metric anomalies in the invite funnel, generate hypotheses for what to change, run A/B experiments, evaluate results, and auto-implement winners. The `autonomous-optimization` drill provides the continuous telemetry that feeds the optimization loop. Over 6 months, invite rate and acceptance rate sustain or improve without manual intervention. The system converges when successive experiments produce less than 2% improvement — meaning the invite mechanism has reached its local maximum given the current product, audience, and market conditions.

## Leading Indicators

- Anomalies detected within 6 hours of occurrence (the monitor is responsive)
- Hypotheses generated within 24 hours of anomaly detection (the agent diagnoses quickly)
- At least 2 experiments completed per month (the system is actively optimizing)
- Winning experiments auto-implemented without human intervention (low/medium risk changes)
- Weekly optimization briefs delivered on schedule with actionable insights
- Invited user retention remains higher than organic user retention (the invite experience continues to add value)

## Instructions

### 1. Deploy the invite health monitor

Run the `autonomous-optimization` drill to create the always-on monitoring layer:

1. Build the PostHog "Invite Mechanism — Health" dashboard with 4 panel groups: top-level metrics, trend charts, funnel breakdown, and segment comparison
2. Define health thresholds calibrated to your Scalable-level baselines:
   - Invite rate healthy threshold: your Scalable-level 4-week average (e.g., 28%)
   - Acceptance rate healthy threshold: your Scalable-level 4-week average (e.g., 57%)
   - Viral coefficient healthy threshold: your Scalable-level 4-week average (e.g., 0.22)
3. Build the n8n anomaly detection workflow running every 6 hours:
   - Queries PostHog for the last 7 days of invite funnel data
   - Compares each metric against its 4-week rolling average
   - Classifies: healthy (within +/-10%), warning (10-25% below), critical (>25% below)
   - For anomalies: identifies the worst-performing segment and possible cause
   - Posts alerts to Slack and stores in Attio
4. Build the invited-user retention monitor comparing invited vs organic user cohorts
5. Build the viral chain depth tracker (generation 0, 1, 2+ chains)
6. Build the weekly health report (Mondays 9 AM) summarizing all metrics, anomalies, and recommendations

### 2. Configure the autonomous optimization loop

Run the `autonomous-optimization` drill configured for the invite mechanism:

**Phase 1 — Monitor (daily via n8n cron):**
- Primary KPIs to monitor: invite rate, acceptance rate, viral coefficient (k)
- Secondary KPIs: invite email CTR, signup completion rate, invitee activation rate, viral cycle time
- Anomaly classification thresholds:
  - Normal: within +/-10% of 4-week rolling average
  - Plateau: +/-2% for 3+ consecutive weeks
  - Drop: >20% decline from rolling average
  - Spike: >50% increase from rolling average

**Phase 2 — Diagnose (triggered by anomaly):**
- Pull the invite mechanism's current configuration from Attio: which entry points are active, current email copy, current reminder sequence timing, active feature flags, current A/B test results
- Pull 8-week metric history from PostHog
- Run hypothesis generation with the anomaly data. Example hypotheses the agent might generate:
  - "Acceptance rate dropped 18% — email deliverability metrics show a domain reputation decline. Hypothesis: switch the invite email sender domain."
  - "Invite rate plateaued at 26% for 4 weeks — the onboarding checklist invite prompt has 0.8% CTR. Hypothesis: replace the checklist prompt with a post-milestone trigger."
  - "Viral coefficient dropped from 0.22 to 0.15 — generation 2 chains went to zero. Hypothesis: the invited-user invite prompt is showing too early (Day 3 instead of Day 7)."
- Rank hypotheses by expected impact and risk level
- Store in Attio as notes on the invite-mechanism campaign record
- If risk = "high" (e.g., changing invite email sender, removing an entry point): send to Slack for human review and STOP
- If risk = "low" or "medium": proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
- Use PostHog experiments to create a feature flag splitting traffic between control and variant
- Implement the variant:
  - For email changes: create variant template in Loops
  - For in-app prompt changes: create variant message in Intercom
  - For timing changes: adjust n8n workflow trigger timing
  - For entry point changes: toggle PostHog feature flag for the new entry point
- Minimum experiment duration: 7 days or 100+ samples per variant, whichever is longer
- Log the experiment in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
- Pull experiment results from PostHog
- Run experiment evaluation:
  - **Adopt:** Winner improves the target metric by the minimum detectable effect with 95% confidence. Update live configuration. Log the change.
  - **Iterate:** Results are directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
  - **Revert:** Variant performed worse than control. Disable the variant, restore control. Log the failure. Wait 7 days (cooldown) before testing the same variable.
  - **Extend:** Insufficient sample size. Keep running for another period.
- Store the full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from all adopted changes this week
- Generate a weekly optimization brief:
  - What changed and why
  - Net impact on invite rate, acceptance rate, and viral coefficient
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack and store in Attio

### 3. Configure guardrails

**Critical guardrails for the invite mechanism:**

- **Rate limit:** Maximum 1 active experiment at a time. Never stack experiments on the invite flow.
- **Revert threshold:** If invite rate or acceptance rate drops >25% at any point during an experiment, auto-revert immediately.
- **Human approval required for:**
  - Changes to the invite email sender domain or authentication
  - Removal of any invite entry point
  - Changes that affect the acceptance flow (signup form, landing page)
  - Any change the hypothesis generator flags as "high risk"
- **Cooldown:** After a failed experiment, wait 7 days before testing the same variable.
- **Maximum experiments per month:** 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Never experiment on email deliverability without testing:** Before changing invite email configuration, send test invites to a seed list and verify deliverability.

### 4. Monitor for convergence

The optimization loop runs indefinitely. It should detect convergence — when the invite mechanism has reached its local maximum:

- **Convergence signal:** 3 consecutive experiments produce less than 2% improvement on any primary KPI
- **At convergence:**
  1. Reduce anomaly detection frequency from every 6 hours to daily
  2. Reduce experiment cadence from 4/month to 1/month (maintenance experiments)
  3. Generate a convergence report: "The invite mechanism has reached its local maximum. Current performance: invite rate {{rate}}%, acceptance rate {{rate}}%, k = {{k}}. Further gains require strategic changes: new product features, new plan structures, or new user segments."
  4. Post convergence report to Slack and store in Attio
- **Breaking convergence:** If market conditions shift (competitor launches viral feature, user base composition changes, product adds new collaborative features), the monitor will detect the metric change and re-enter the active optimization loop

### 5. Evaluate sustainability

This level runs continuously. Monthly review:
- Are invite rate, acceptance rate, and viral coefficient at or above Scalable-level baselines?
- How many experiments ran this month? What was the net impact?
- Is the autonomous optimization loop running without errors?
- Are weekly briefs being generated and delivered?
- Has the system detected and responded to any anomalies appropriately?

**Pass criteria:** Invite rate and acceptance rate sustained or improving for 6+ months via autonomous optimization. Viral coefficient k >= 0.2 maintained. If metrics decay below Scalable baselines for 4+ consecutive weeks despite optimization attempts, diagnose whether the cause is strategic (requires product or market changes) or tactical (the optimization loop needs recalibration).

## Time Estimate

- 8 hours: Deploy invite health monitor (dashboard, anomaly detection, retention comparison, weekly report)
- 8 hours: Configure autonomous optimization loop (5 phases, guardrails, convergence detection)
- 4 hours: Initial calibration — set thresholds based on Scalable baselines, test the full loop with a manual trigger
- Ongoing: ~2 hours/month reviewing weekly briefs and approving high-risk experiments

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Dashboards, anomaly detection, experiments, feature flags, cohorts | Free up to 1M events/mo; paid from $0.00005/event ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app message variants for experiments | From $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email template variants for experiments | From $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Campaign records, experiment logging, optimization audit trail | From $29/user/mo ([attio.com](https://attio.com)) |
| n8n | Optimization loop scheduling (daily monitor, weekly report, experiment triggers) | Free self-hosted; Pro cloud at $60/mo ([n8n.io/pricing](https://n8n.io/pricing/)) |
| Anthropic Claude API | Hypothesis generation and experiment evaluation | From $3/MTok input, $15/MTok output ([anthropic.com/pricing](https://www.anthropic.com/pricing)) |

**Estimated play-specific cost at Durable:** $150-400/mo (same tooling as Scalable; incremental cost is Anthropic API for hypothesis generation — typically $10-30/mo for weekly optimization cycles)

## Drills Referenced

- `autonomous-optimization` — the core Durable loop: monitor metrics, detect anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, generate weekly briefs. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — continuous monitoring of invite funnel health, acceptance rates, viral coefficient trends, invited-user retention comparison, and viral chain depth tracking. Feeds anomaly data to the autonomous-optimization loop.
