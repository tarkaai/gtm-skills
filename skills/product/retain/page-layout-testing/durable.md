---
name: page-layout-testing-durable
description: >
  UI/UX Experimentation — Durable Intelligence. An always-on AI agent autonomously
  detects engagement anomalies, generates layout hypotheses, runs A/B experiments,
  evaluates results, and implements winners — finding the local maximum for every page.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving engagement lift over 6 months via autonomous optimization"
kpis: ["Monthly engagement trend (sustained or improving)", "Experiment velocity (tests/month)", "Autonomous win rate (%)", "Cumulative lift from AI-implemented changes", "Time to detect and respond to engagement drops"]
slug: "page-layout-testing"
install: "npx gtm-skills add product/retain/page-layout-testing"
drills:
  - autonomous-optimization
  - ux-experiment-health-monitor
  - session-recording-friction-analysis
---

# UI/UX Experimentation — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

An always-on AI agent manages the entire page layout experimentation lifecycle autonomously. The agent detects engagement anomalies, generates layout hypotheses from data, runs A/B experiments, evaluates results, and implements winners — all without human intervention for low-risk changes. Engagement lift sustains or improves over 6 months. The agent converges when successive experiments produce <2% improvement, signaling that the page has reached its local maximum.

## Leading Indicators

- Autonomous optimization loop running daily via n8n within the first week
- First AI-generated hypothesis produced within 10 days of activation
- First AI-initiated experiment launched within 3 weeks
- Weekly optimization briefs generating automatically
- Engagement metrics stable or improving month-over-month

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill. This is the core of Durable and creates the always-on agent loop:

**Phase 1 — Monitor (daily via n8n cron):**
The agent checks all pages in the experiment pipeline for engagement anomalies. It compares the last 2 weeks of engagement metrics against a 4-week rolling average. Classifications:
- **Normal** (within +/-10%): log to Attio, no action
- **Plateau** (+/-2% for 3+ weeks): trigger hypothesis generation — the page has stopped improving
- **Drop** (>20% decline): trigger urgent hypothesis generation
- **Spike** (>50% increase): investigate cause — was this a released experiment winner or an external factor?

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current page layout configuration, 8-week metric history, active user segments, and recent experiment results. It runs the hypothesis generator (Claude API) to produce 3 ranked layout hypotheses with expected impact and risk levels.

- Low/medium risk hypotheses: proceed automatically to Phase 3
- High risk hypotheses (changes affecting >50% of page layout or >50% of traffic): send alert for human review and STOP

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent designs an A/B test: creates a PostHog feature flag splitting traffic 50/50, implements the variant change, sets experiment duration (minimum 7 days or until 100+ conversions per variant). It logs the experiment in Attio with hypothesis, start date, expected duration, and success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog and evaluates:
- **Adopt:** Variant wins at 95% significance. Roll out the variant as the new default. Log the change.
- **Iterate:** Result is directionally positive but not significant. Generate a refined hypothesis. Return to Phase 2.
- **Revert:** Variant loses or guardrails are breached. Disable the variant. Log the failure. Return to Phase 1 monitoring.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected and how they were classified
- Hypotheses generated with risk ratings
- Experiments started, completed, and their outcomes
- Net metric change from implemented winners
- Estimated distance from local maximum (based on diminishing experiment returns)

### 2. Configure UX experiment health monitoring

Run the `ux-experiment-health-monitor` drill to provide the safety layer around autonomous optimization:

- **Every 6 hours:** Check all AI-initiated experiments for guardrail breaches. Auto-pause experiments if bounce rate increases >15 percentage points or error rate spikes >2x.
- **Weekly:** Generate the experiment velocity and cumulative lift report. Track win rate of AI-generated hypotheses vs. historical human-generated ones.
- **On convergence:** When 3 consecutive experiments produce <2% lift, the agent detects convergence. It reduces monitoring frequency from daily to weekly and reports: "Page [X] has reached its local maximum. Current engagement: [metric]. Further gains require product-level changes."

### 3. Maintain the friction analysis pipeline

Run the `session-recording-friction-analysis` drill monthly to feed fresh signals into the autonomous loop. Even when the optimization loop is running autonomously, qualitative recording data reveals friction patterns that quantitative metrics miss. The agent:

1. Queries PostHog for session recordings of users who dropped off at the highest-volume drop-off step on each monitored page
2. Catalogs friction patterns (confusion, hesitation, rage-clicks, scroll-past)
3. Feeds the top friction patterns into the hypothesis generator as additional context
4. This enriches the hypotheses with qualitative grounding — the agent does not just optimize numbers, it understands WHY users struggle

### 4. Implement guardrails for autonomous operation

These guardrails are critical because the agent operates without human approval for low-risk changes:

- **Rate limit:** Maximum 1 active experiment per page at a time. Never stack experiments.
- **Revert threshold:** If primary engagement metric drops >30% during any experiment, auto-revert immediately.
- **Human approval required for:**
  - Layout changes affecting >50% of the page structure
  - Changes to primary navigation or core product flows
  - Any change the hypothesis generator flags as "high risk"
  - Budget changes >20% (if paid elements are involved)
- **Cooldown:** After a failed experiment (revert), wait 7 days before testing a new hypothesis on the same page element.
- **Monthly cap:** Maximum 4 experiments per page per month. If all 4 fail, pause autonomous optimization for that page and flag for human strategic review.
- **Fallback alert:** If the agent fails to run for 48+ hours (n8n workflow error, API failure), send an immediate alert. Engagement monitoring must not silently stop.

### 5. Evaluate sustainability

This level runs continuously. Monthly review criteria:

- **Engagement trend:** Is the primary engagement metric sustained or improving month-over-month?
- **Experiment win rate:** Are AI-generated hypotheses winning at >=30%?
- **Convergence status:** Which pages have reached their local maximum? Which still have room for improvement?
- **Agent reliability:** Has the autonomous loop run without interruption? Were any guardrails breached?

After 6 months, the play is Durable if: engagement lift is sustained or improving, the autonomous loop has run reliably, and converged pages maintain their metrics without regression.

## Time Estimate

- 16 hours: Configure the autonomous optimization loop (n8n workflows, PostHog connections, Claude API integration)
- 8 hours: Set up guardrails and health monitoring
- 4 hours: Configure monthly friction analysis pipeline
- 8 hours/month: Review weekly briefs, approve high-risk hypotheses, adjust guardrails (48 hours over 6 months)
- 74 hours: Agent compute and autonomous operation over 6 months

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, anomaly detection, session recording, dashboards | ~$100-300/mo at Durable traffic levels ([posthog.com/pricing](https://posthog.com/pricing)) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, optimization briefs | ~$20-50/mo at Sonnet 4.6 rates ($3/$15 per 1M tokens) ([platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing)) |
| n8n | Scheduling the daily/weekly optimization loops | Standard stack (excluded) |
| Attio | Experiment logging, learning log, optimization audit trail | Standard stack (excluded) |

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor engagement anomalies, generate layout hypotheses, run A/B experiments, evaluate results, implement winners, report weekly
- `ux-experiment-health-monitor` — guardrail monitoring, experiment velocity tracking, cumulative lift reporting, convergence detection
- `session-recording-friction-analysis` — monthly qualitative analysis feeding friction patterns into the hypothesis generator
