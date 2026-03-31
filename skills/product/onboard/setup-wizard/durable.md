---
name: setup-wizard-durable
description: >
  Guided Setup Wizard — Durable. AI agent autonomously monitors wizard metrics,
  detects anomalies, generates improvement hypotheses, runs A/B experiments,
  and auto-implements winners. Sustains >=70% completion over 6 months with
  continuous optimization toward the local maximum.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable"
time: "150 hours over 6 months"
outcome: "Wizard completion >=70% sustained or improving over 6 months via autonomous AI optimization"
kpis: ["Wizard completion rate (overall)", "Wizard completion rate (per persona)", "Experiment velocity (tests/month)", "AI-driven lift (cumulative % improvement)", "Config success rate", "Time to convergence"]
slug: "setup-wizard"
install: "npx gtm-skills add product/onboard/setup-wizard"
drills:
  - autonomous-optimization
  - wizard-completion-monitor
  - onboarding-health-monitor
---

# Guided Setup Wizard — Durable

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Wizard completion rate >=70% sustained or improving for 6 consecutive months without human intervention. The AI agent runs the full optimization loop: detect metric anomalies, generate improvement hypotheses, design and run A/B experiments, evaluate results, and auto-implement winners. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement, indicating the local maximum has been found.

## Leading Indicators

- Agent runs the daily monitoring check without failures for 30+ consecutive days
- At least 2 experiments completed per month (target: 3-4/month)
- Experiment win rate is >=40% (2 of 5 experiments produce measurable improvement)
- No critical anomaly goes undetected for more than 24 hours
- Cumulative AI-driven lift is measurable (>=5pp improvement over Scalable's final rate within first 3 months)
- Convergence detection triggers correctly when improvement plateaus

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to create the always-on agent loop for this play:

**Phase 1 — Monitor (daily via n8n cron at 08:00 UTC):**
1. Use PostHog anomaly detection to check all wizard KPIs: overall completion rate, per-persona completion rates, step-level dropoff rates, config success rate, median time-to-complete
2. Compare last 2 weeks against 4-week rolling average
3. Classify each metric: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
4. If normal: log to Attio, no action
5. If anomaly detected: trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: pull current wizard configuration from Attio (active variants, step definitions, recent experiment results)
2. Pull 8-week metric history from PostHog for the affected metric
3. Run hypothesis generation via Anthropic API with the anomaly data + wizard context
4. Receive 3 ranked hypotheses. Examples for wizard-specific anomalies:
   - Completion drop at step 3: "Integration partner changed their OAuth flow; users see an unfamiliar screen" -> test updated Product Tour copy
   - Time-to-complete increase: "New persona segment (larger companies) has more complex setup" -> test a simplified variant for enterprise users
   - Config success drop: "Backend API returning more errors" -> investigate before experimenting (not a UX problem)
   - Persona-specific decline: "Marketing persona tour copy references deprecated feature" -> update tour to reference current feature
5. If top hypothesis is high-risk (budget change >20%, affects >50% of users): send Slack alert and STOP for human review
6. If low/medium risk: proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment: create a PostHog feature flag splitting traffic between control (current wizard) and variant (hypothesis change)
2. Implement the variant:
   - For tour copy changes: update the Intercom Product Tour content for the variant group
   - For step ordering changes: create a new Intercom Checklist variant with different step sequence
   - For email changes: create a new Loops sequence variant
   - For step removal/addition: update the feature flag to show different wizard configuration
3. Set duration: minimum 7 days or 100+ users per variant, whichever is longer
4. Log experiment in Attio: hypothesis, start date, expected duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog experiments API
2. Run experiment evaluation via Anthropic API with control vs variant data
3. Decision:
   - **Adopt**: Variant won with >=95% confidence. Roll out to 100%. Update Attio.
   - **Iterate**: Result suggestive but not significant. Generate refined hypothesis. Return to Phase 2.
   - **Revert**: Variant lost or no difference. Disable variant. Log failure. Return to Phase 1.
   - **Extend**: Result trending positive but insufficient sample. Extend 7 more days.
4. Store full evaluation in Attio: decision, confidence, reasoning, impact size

**Phase 5 — Report (weekly via n8n cron, Monday 09:00 UTC):**
1. Aggregate all optimization activity for the week
2. Calculate net metric change from all adopted changes
3. Generate a weekly optimization brief:
   ```
   # Setup Wizard Optimization Brief — Week of [date]

   ## Status: [Optimizing / Converging / Converged]

   ## This Week
   - Anomalies detected: [N]
   - Experiments running: [N]
   - Experiments completed: [N] (wins: [W], losses: [L])
   - Net wizard completion impact: [+/-X pp]

   ## Cumulative AI Lift
   - Starting rate (Scalable exit): [X%]
   - Current rate: [Y%]
   - Total AI-driven improvement: [+Z pp]

   ## Active Experiment
   - Hypothesis: [description]
   - Variant: [what changed]
   - Running since: [date]
   - Current trend: [variant winning / control winning / too early]

   ## Per-Persona Health
   | Persona | Completion | Trend | Last Experiment |
   |---------|-----------|-------|-----------------|
   | ...     | ...       | ...   | ...             |

   ## Convergence Status
   - Last 3 experiment improvements: [X%, Y%, Z%]
   - Convergence: [Not yet / Approaching / Converged]
   ```
4. Post to Slack and store in Attio

### 2. Deploy wizard-specific health monitoring

Run the `wizard-completion-monitor` drill at Durable depth:
- All dashboards and funnels from Scalable continue running
- Add experiment tracking panels: active experiments, historical win/loss rate, cumulative lift chart
- Add convergence tracking: chart showing improvement size of each successive experiment
- Daily monitoring now feeds anomaly data directly into the autonomous-optimization Phase 1

### 3. Deploy cross-play onboarding health monitoring

Run the `onboarding-health-monitor` drill to monitor the wizard's impact on broader onboarding health:
- Track whether wizard completers activate at higher rates than non-completers
- Detect if wizard changes affect downstream metrics (feature adoption, retention, expansion)
- Alert if wizard optimization improves completion but harms config quality (optimizing for speed over correctness)
- Weekly health report includes wizard-to-activation correlation by persona

### 4. Configure guardrails

Guardrails that override the autonomous loop:

- **Rate limit:** Maximum 1 active wizard experiment at a time. Never stack experiments.
- **Revert threshold:** If wizard completion drops >30% during any experiment, auto-revert immediately.
- **Human approval required for:**
  - Removing a wizard step entirely
  - Changing the persona classification rules
  - Any change affecting >50% of new signups simultaneously
  - Adding steps that increase wizard length by >50%
- **Cooldown:** After a failed experiment, wait 7 days before testing the same step again.
- **Monthly cap:** Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review.
- **Quality floor:** If config success rate drops below 80%, pause all experiments and investigate backend health.

### 5. Evaluate sustainability

This level runs continuously. Monthly review:
- Is wizard completion >=70%? If not, the autonomous loop should be diagnosing and fixing.
- Is experiment velocity >=2/month? If not, check that monitoring is running and hypotheses are being generated.
- Has the system converged? If successive experiments produce <2% improvement for 3 consecutive tests:
  1. The wizard has reached its local maximum
  2. Reduce experiment frequency from weekly to monthly
  3. Shift monitoring to maintenance mode (weekly checks instead of daily)
  4. Report: "Setup wizard is optimized at [X%] completion. Further gains require strategic changes (new setup flow, new product features, new persona paths) rather than tactical optimization."

## Time Estimate

- 20 hours: Configure autonomous optimization loop (n8n workflows, PostHog experiments, Anthropic API integration)
- 15 hours: Expand monitoring dashboards with experiment tracking and convergence panels
- 10 hours: Configure onboarding health monitoring integration
- 5 hours: Set up guardrails and alerting
- 100 hours: Ongoing monitoring, experiment review, and brief generation over 6 months (mostly automated; ~4 hours/week human review time)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, experiments, feature flags, dashboards, anomaly detection | ~$100-400/mo at scale depending on volume ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Checklists, Product Tours, in-app messages (multiple variants) | $85/seat/mo Advanced plan; Proactive Support add-on $349/mo if sending >500 messages ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Per-persona email sequences, experiment variants | $49/mo for up to 5K contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Autonomous loop orchestration (daily monitoring, experiment triggers, weekly reports) | $60/mo Pro plan ([n8n.io/pricing](https://n8n.io/pricing)) |
| Anthropic API | Hypothesis generation, experiment evaluation | ~$20-50/mo for weekly agent runs ([anthropic.com/pricing](https://anthropic.com/pricing)) |

**Estimated play-specific cost at Durable:** $314-944/mo depending on Intercom plan and PostHog volume, plus agent compute

## Drills Referenced

- `autonomous-optimization` -- the core always-on loop: monitor, diagnose, experiment, evaluate, implement, report
- `wizard-completion-monitor` -- continuous wizard health tracking with anomaly detection feeding into the optimization loop
- `onboarding-health-monitor` -- cross-metric monitoring ensuring wizard optimization does not harm broader onboarding health
