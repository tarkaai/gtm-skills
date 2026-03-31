---
name: ai-onboarding-coach-durable
description: >
  AI Onboarding Coach — Durable Intelligence. Always-on autonomous optimization loop
  monitors coach metrics, detects anomalies, generates improvement hypotheses, runs
  experiments, and auto-implements winners. Pass threshold: coach engagement >= 55%
  AND activation lift >= 10pp sustained or improving over 6 months via autonomous
  agent optimization.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "80 hours over 6 months"
outcome: "Coach engagement >= 55% AND activation lift >= 10pp sustained or improving over 6 months via autonomous optimization"
kpis: ["Coach engagement rate (6-month trend)", "Activation lift (coach vs no-coach, monthly cohorts)", "Autonomous experiment velocity", "Experiment win rate", "Content gap fill time", "Convergence detection"]
slug: "ai-onboarding-coach"
install: "npx gtm-skills add product/onboard/ai-onboarding-coach"
drills:
  - autonomous-optimization
  - onboarding-health-monitor
---

# AI Onboarding Coach — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The AI coaching system runs autonomously. An optimization agent monitors all coach metrics daily, detects anomalies (engagement drops, resolution rate degradation, activation lift decay, content gaps), generates hypotheses for improvement, runs A/B experiments, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs and converges when successive experiments yield < 2% improvement. Pass threshold: coach engagement >= 55% AND activation lift >= 10pp sustained or improving over 6 consecutive months without manual intervention.

## Leading Indicators

- Autonomous optimization loop runs daily without manual intervention or errors for 4+ consecutive weeks
- At least 2 experiments are completed per month (the agent is actively testing)
- Experiment win rate >= 30% (at least 1 in 3 experiments produces a measurable improvement)
- Content gap fill time drops below 24 hours (agent detects unanswered question patterns and drafts answers for human approval)
- Weekly optimization briefs are generated and posted without intervention
- No critical metric (engagement, lift, resolution rate) drops below threshold for 2+ consecutive weeks without the agent detecting and responding
- Convergence: if the last 3 experiments each produced < 2% improvement, the agent correctly detects convergence and reduces experiment frequency

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to build the always-on optimization agent:

**Phase 1 — Monitor (daily via n8n cron at 08:00 UTC):**
1. Query PostHog for the coach's primary KPIs: engagement rate, activation lift, resolution rate, proactive suggestion CTR, struggle intervention success rate
2. Compare each metric's last 2-week average against the 4-week rolling average
3. Classify: **normal** (within +/-10%), **plateau** (within +/-2% for 3+ weeks), **drop** (> 20% decline), **spike** (> 50% increase)
4. If normal -> log to Attio, no action
5. If anomaly detected -> trigger Phase 2

**Phase 2 — Diagnose (triggered by anomaly):**
1. Gather context: pull the coach's current configuration from Attio (active trigger rules, Fin custom answers count, last experiment results, persona distribution)
2. Pull 8-week metric history from PostHog
3. Pull the latest content gap report from the `autonomous-optimization` drill
4. Run `hypothesis-generation` with the anomaly + context. The hypothesis space for this play includes:
   - **Engagement hypotheses**: Greeting copy, Messenger widget placement, proactive trigger timing, suggestion format
   - **Resolution hypotheses**: Missing knowledge base content, outdated articles, Fin confidence threshold, handoff rules
   - **Activation lift hypotheses**: Post-resolution CTA copy, deep link targets, follow-up message timing, persona-specific response tuning
   - **Struggle intervention hypotheses**: Trigger sensitivity thresholds, intervention message format, rescue flow design
5. Receive 3 ranked hypotheses with expected impact and risk
6. High-risk hypotheses (e.g., disabling the coach for a persona, changing handoff rules to never escalate) -> Slack alert for human review, STOP
7. Low/medium risk -> proceed to Phase 3

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
1. Design the experiment: use PostHog feature flags to split coach behavior between control (current) and variant (hypothesis)
2. Implement the variant using the appropriate mechanism:
   - Greeting copy change -> update Fin custom answer via Intercom API
   - Trigger timing change -> update n8n workflow parameter
   - Response format change -> update Fin persona configuration
   - Content addition -> create new Fin custom answer (flag for human review before enabling)
3. Run for minimum 7 days or 100+ users per variant
4. Log experiment start in Attio: hypothesis, start date, duration, success criteria

**Phase 4 — Evaluate (triggered by experiment completion):**
1. Pull experiment results from PostHog
2. Run `experiment-evaluation` with control vs variant data
3. Decision:
   - **Adopt**: Variant outperforms control. Update live configuration. Log the change.
   - **Iterate**: Results directionally positive but not significant. Generate a refined hypothesis.
   - **Revert**: Variant underperforms. Restore control. Log the failure.
   - **Extend**: Insufficient data. Run for another period.
4. Store full evaluation in Attio

**Phase 5 — Report (weekly via n8n cron, Mondays at 09:00 UTC):**
1. Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
2. Calculate net metric change from adopted changes
3. Generate weekly optimization brief:
   - What changed and why
   - Net impact on coach engagement, activation lift, resolution rate
   - Estimated distance from local maximum
   - Recommended focus for next week
4. Post brief to Slack and store in Attio

### 2. Deploy coach-specific health monitoring

Run the `autonomous-optimization` drill to build the coach-specific monitoring layer:

1. **Daily health checks**: Engagement rate, resolution rate, activation lift, suggestion CTR, handoff rate — all compared against rolling averages with automated anomaly alerts
2. **Weekly content gap report**: Extract unanswered Fin queries, cluster by topic, identify missing articles and degraded articles, generate a prioritized content fix list
3. **Weekly regression analysis**: Compare coach effectiveness across weekly signup cohorts. Detect if the coach is becoming less effective for newer cohorts (content staleness, product changes not reflected in knowledge base, new user personas entering)
4. **Feed anomalies to the autonomous optimization loop**: Every critical or warning anomaly from the health monitor triggers Phase 2 (Diagnose) in the optimization loop

### 3. Deploy onboarding-wide health monitoring

Run the `onboarding-health-monitor` drill to monitor the broader onboarding system:

1. Per-persona activation rates and trends
2. Tour completion rates and email engagement rates
3. Cohort drift detection (is the mix of new users changing?)
4. Per-persona drop-off heatmaps

This ensures the optimization agent has visibility into the entire onboarding funnel, not just the AI coach layer. A drop in activation could be caused by a product bug, not a coach issue — the broader monitor helps the agent diagnose correctly.

### 4. Configure guardrails

Guardrails prevent the autonomous agent from causing harm:

- **Rate limit**: Maximum 1 active experiment at a time. Never stack coach experiments.
- **Revert threshold**: If coach engagement drops > 30% OR activation lift goes negative during an experiment, auto-revert immediately.
- **Human approval required for**:
  - Disabling the coach for any persona
  - Changing human handoff rules
  - Adding Fin custom answers that contain pricing, legal, or security information
  - Any hypothesis flagged as "high risk"
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable.
- **Maximum experiments per month**: 4. If all 4 fail, pause optimization and flag for human strategic review.
- **Content approval**: The agent can draft new Fin custom answers but must flag them for human review before enabling. Auto-enable only after explicit human approval.

### 5. Detect convergence and reduce to maintenance mode

The optimization agent monitors for convergence:

1. If the last 3 consecutive experiments each produced < 2% improvement on any primary metric, declare convergence
2. At convergence:
   - Reduce monitoring frequency from daily to every 3 days
   - Reduce experiment attempts from weekly to monthly
   - Generate a convergence report: "The AI onboarding coach has reached its local maximum. Current performance: [engagement rate]% engagement, [lift]pp activation lift, [resolution]% resolution rate. Further gains require strategic changes (new persona coverage, product feature changes, coach architecture changes) rather than tactical optimization."
3. Continue monitoring for regression: if any primary metric drops > 15% below the converged level, re-enter daily monitoring and active experimentation

## Time Estimate

- 12 hours: Autonomous optimization loop setup (n8n workflows, PostHog queries, Claude integration)
- 8 hours: Coach health monitor deployment and dashboard configuration
- 6 hours: Onboarding-wide health monitor deployment
- 4 hours: Guardrail configuration and testing
- 50 hours: Ongoing over 6 months — weekly brief review (30 min/week), monthly guardrail review (2 hours/month), quarterly strategic review (4 hours/quarter). Most time is the agent running autonomously; human time is review only.

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Fin AI Agent) | AI coaching surface at scale | $0.99/resolution; ~$400-900/mo at sustained 500+ signups with high engagement |
| Anthropic (Claude API) | Hypothesis generation, experiment evaluation, content gap analysis | ~$20-50/mo for weekly optimization loop |
| Loops | Lifecycle email sequences | ~$25-50/mo |

_CRM (Attio), automation (n8n), and PostHog are standard stack — not counted as play-specific costs._

## Drills Referenced

- `autonomous-optimization` — the core always-on optimization loop: daily metric monitoring with anomaly detection, hypothesis generation via Claude, A/B experiment execution via PostHog feature flags, automated evaluation and implementation of winners, and weekly optimization briefs
- `autonomous-optimization` — coach-specific daily health checks (engagement, resolution, activation lift), weekly content gap reports (unanswered Fin queries), and weekly regression analysis comparing coach effectiveness across signup cohorts
- `onboarding-health-monitor` — onboarding-wide monitoring: per-persona activation rates, tour completion, email engagement, and cohort drift detection providing the broader context the optimization agent needs to diagnose issues correctly
