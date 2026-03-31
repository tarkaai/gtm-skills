---
name: ai-support-chatbot-durable
description: >
  AI In-App Support — Durable Intelligence. Always-on AI agents find the local maximum:
  autonomous optimization detects metric anomalies, generates hypotheses, runs A/B
  experiments on chatbot behavior, and auto-implements winners. Continuous support
  health monitoring and churn prediction refinement converge on optimal performance.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "AI resolution rate sustained ≥65% with improving CSAT; churn prediction precision ≥50%; autonomous optimization converges (<2% improvement for 3 consecutive experiments)"
kpis: ["AI resolution rate", "CSAT trend", "Churn prediction precision", "Experiment velocity", "Cost per resolution trend", "Convergence status"]
slug: "ai-support-chatbot"
install: "npx gtm-skills add product/retain/ai-support-chatbot"
drills:
  - autonomous-optimization
---

# AI In-App Support — Durable Intelligence

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

The AI chatbot operates at its local maximum. The `autonomous-optimization` drill runs the core loop: detect metric anomalies in chatbot performance, generate improvement hypotheses, run A/B experiments on chatbot configuration, evaluate results, and auto-implement winners. Weekly optimization briefs report what changed and why. The support health monitor tracks churn prediction accuracy and recalibrates when model drift occurs. The system converges when successive experiments produce <2% improvement — at that point, the chatbot is optimized and further gains require strategic changes (new product features, new support channels, new user segments) rather than tactical tuning.

## Leading Indicators

- Autonomous optimization completes its first full cycle (anomaly → hypothesis → experiment → evaluation → decision) within the first 2 weeks of Durable activation
- At least 2 of the first 4 experiments produce measurable improvement (>2%) in resolution rate or CSAT
- Churn prediction precision remains ≥45% across monthly recalibration checks (model is stable)
- Weekly optimization briefs are generated and posted to Slack without manual intervention (the loop is truly autonomous)

## Instructions

### 1. Activate autonomous optimization

Run the `autonomous-optimization` drill configured for the AI support chatbot play. This creates the always-on improvement loop:

**Monitor (daily via n8n cron):**
- Check chatbot KPIs via PostHog: resolution rate, CSAT, escalation rate, top unresolved topics, cost per resolution
- Compare last 2 weeks against 4-week rolling average
- Classify: normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), spike (>50% increase)
- If anomaly detected, trigger the diagnosis phase

**Diagnose (triggered by anomaly):**
- Gather context: current Fin AI configuration, knowledge base coverage stats, escalation rule set, user segment targeting
- Pull 8-week metric history from PostHog
- Run `hypothesis-generation` to produce 3 ranked hypotheses with expected impact and risk
- Store hypotheses in Attio. If highest-ranked hypothesis is "high risk," send Slack alert for human review and stop

**Experiment (triggered by hypothesis acceptance):**
- Take the top hypothesis. Examples of chatbot experiments:
  - "Increase Fin confidence threshold from 0.5 to 0.6 to reduce incorrect answers" → test via A/B split on user cohorts
  - "Add proactive help trigger on pricing page to catch billing questions before they become tickets" → test via PostHog feature flag
  - "Change escalation rule: hand off after 3 bot replies instead of 4 to reduce user frustration" → test via n8n routing logic A/B
  - "Add 5 custom answers for the top escalation topic this month" → test resolution rate for that topic before/after
- Use `posthog-experiments` to run the A/B test. Minimum 7 days or 100+ samples per variant.
- Log experiment in Attio: hypothesis, start date, duration, success criteria

**Evaluate (triggered by experiment completion):**
- Pull results from PostHog. Run `experiment-evaluation`.
- Decision: Adopt (implement winner), Iterate (refine hypothesis), Revert (restore control), or Extend (more data needed)
- Store full evaluation in Attio

**Report (weekly via n8n cron):**
- Aggregate all optimization activity: anomalies detected, hypotheses generated, experiments run, decisions made
- Calculate net metric change from adopted changes
- Generate weekly optimization brief:
  - What changed and why
  - Net impact on resolution rate, CSAT, cost per resolution
  - Current distance from estimated local maximum
  - Recommended focus for next week
- Post to Slack, store in Attio

### 2. Activate support health monitoring

Run the `autonomous-optimization` drill to create the ongoing observability layer:
- Build a PostHog dashboard for support ticket trends, churn score distributions, prediction accuracy, intervention funnel, CSAT trend, repeat issue tracker
- Configure anomaly alerts for ticket volume spikes, CSAT drops, churn score distribution shifts, and prediction accuracy degradation
- Generate weekly support health reports posted to Slack
- Track model drift monthly: if churn prediction precision drops below 35% or recall below 50%, trigger recalibration via `support-churn-correlation` drill

### 3. Maintain chatbot performance monitoring

Run the the chatbot resolution monitor workflow (see instructions below) drill continuously:
- Live dashboard tracking resolution rate, CSAT, escalation patterns, support load impact
- Anomaly alerts feeding into the autonomous optimization loop
- Weekly health reports comparing AI chatbot metrics to pre-chatbot baseline
- Knowledge gap closure tracking

### 4. Guardrails

The autonomous optimization drill includes built-in guardrails. For the chatbot play specifically, add:
- **Never reduce Fin confidence threshold below 0.4** — this would cause the bot to give uncertain answers
- **Never route enterprise accounts away from human-first** — this is a business rule, not an optimization variable
- **If CSAT for AI-resolved drops below 3.0 for any experiment, auto-revert immediately** — user satisfaction is non-negotiable
- **Maximum 1 active experiment at a time** — chatbot behavior changes are hard to isolate with multiple simultaneous experiments
- **If 4 consecutive experiments fail (revert), pause optimization and flag for human strategic review** — the chatbot may have reached its local maximum, or the problem is upstream (product issues, not chatbot configuration)

### 5. Convergence detection

The system has converged when 3 consecutive experiments produce <2% improvement in the primary metric (resolution rate). At convergence:
- Reduce monitoring frequency from daily to weekly
- Reduce experiment frequency from continuous to monthly check-ins
- Report to the team: "AI support chatbot is optimized. Current performance: [resolution rate]% resolution, [CSAT] satisfaction, [cost]/resolution. Further gains require strategic changes: expanding knowledge base to new product areas, adding new support channels (email, phone), or product improvements to reduce the need for support."
- Shift agent focus to monitoring for external disruptions (product launches, competitor changes, user base composition shifts) that would re-open the optimization space

### 6. Evaluate sustainability

Measure at 3-month and 6-month checkpoints:
- **AI resolution rate**: Sustained ≥65%. Pass/fail.
- **CSAT trend**: Stable or improving over 6 months. Pass/fail.
- **Churn prediction precision**: ≥50% at each monthly check. Pass/fail.
- **Experiment velocity**: ≥2 experiments completed per month for the first 3 months, reducing as convergence approaches. Pass/fail.
- **Cost per resolution**: Stable or declining. Pass/fail.
- **Convergence**: Has the system detected convergence? If yes, optimization is complete. If no after 6 months, investigate whether the optimization space is too large or the experiment design is too conservative.

## Time Estimate

- 20 hours: autonomous optimization setup (n8n workflows, PostHog experiments infrastructure, Attio logging)
- 15 hours: support health monitor setup (dashboard, anomaly alerts, weekly reports)
- 10 hours: chatbot resolution monitor maintenance and enhancement
- 40 hours: experiment execution and evaluation (~8 experiments over 6 months, 5 hours each)
- 30 hours: weekly review, report analysis, human-required decisions (1 hour/week for 6 months)
- 20 hours: monthly churn model recalibration checks and knowledge pipeline tuning
- 15 hours: convergence analysis, documentation, handoff

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom (Advanced) | Fin AI chatbot + routing + team inboxes | $85/seat/mo + $0.99/resolution — [intercom.com/pricing](https://www.intercom.com/pricing) |
| PostHog | Analytics, experiments, feature flags, dashboards | ~$50-200/mo depending on event volume — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic API | Hypothesis generation, experiment evaluation, reports, ticket classification, churn scoring | ~$60-120/mo — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |

**Estimated cost for Durable: ~$300–600/mo** (Intercom $85 base + $200-300 Fin resolutions + $60-120 Anthropic + $50-100 PostHog; costs should stabilize or decline as optimization converges)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor → diagnose → experiment → evaluate → implement. Detects metric anomalies, generates improvement hypotheses, runs A/B experiments, and auto-implements winners. Converges when successive experiments produce <2% improvement.
- `autonomous-optimization` — ongoing monitoring of support ticket trends, churn prediction accuracy, intervention effectiveness, and model drift
- the chatbot resolution monitor workflow (see instructions below) — live chatbot performance dashboard, anomaly alerts, weekly health reports, knowledge gap closure tracking
