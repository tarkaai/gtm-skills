---
name: self-serve-signup-optimization-durable
description: >
  Signup Funnel Optimization — Durable Intelligence. Autonomous AI agents continuously monitor
  signup metrics, generate hypotheses, run experiments, and auto-implement winners to find and
  maintain the local maximum signup CVR.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Website, Product"
level: "Durable Intelligence"
time: "Ongoing — 4 hours/week agent compute + 1 hour/week human review"
outcome: "Signup CVR sustained at or above Scalable level for 3+ months with autonomous optimization producing weekly briefs and <2% experiment variance indicating convergence"
kpis: ["Signup CVR trend (90-day)", "Experiment velocity (tests/month)", "Cumulative lift from autonomous changes", "Time to detect regression", "Convergence status"]
slug: "self-serve-signup-optimization"
install: "npx gtm-skills add product/onboard/self-serve-signup-optimization"
drills:
  - autonomous-optimization
---

# Signup Funnel Optimization — Durable Intelligence

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Website, Product

## Outcomes

The signup funnel runs on autopilot. An AI agent monitors signup metrics daily, detects anomalies within hours, generates improvement hypotheses, runs A/B experiments via PostHog, evaluates results, and auto-implements winners. Weekly optimization briefs summarize what changed and why. The system converges when successive experiments produce <2% improvement, indicating the funnel has reached its local maximum. Human intervention is limited to reviewing weekly briefs and approving high-risk changes.

## Leading Indicators

- Daily anomaly detection catching regressions within 4 hours of deployment
- 2-4 autonomous experiments completed per month
- Each winning experiment documented with hypothesis, result, and confidence level
- Weekly optimization briefs delivered every Monday
- Cumulative lift log showing the running total improvement since Durable started
- Convergence signal: 3 consecutive experiments with <2% improvement indicates local maximum reached

## Instructions

### 1. Activate the autonomous optimization loop

Run the `autonomous-optimization` drill. This creates the always-on agent loop for the signup funnel:

**Phase 1 — Monitor (daily via n8n cron):**
The agent queries PostHog for signup funnel KPIs, compares last 2 weeks against 4-week rolling average, and classifies each metric as normal, plateau, drop, or spike. Anomalies trigger Phase 2 automatically.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context from PostHog (8-week metric history, per-segment breakdown, active feature flags) and generates 3 ranked hypotheses using Claude. Each hypothesis includes expected impact and risk level. High-risk hypotheses require human approval before proceeding.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent creates a PostHog experiment with a feature flag splitting traffic between control and the hypothesis variant. Experiment runs for minimum 7 days or until 100+ samples per variant. The agent implements the variant — for signup flow changes this means: updating form fields via feature flag, changing CTA copy, adjusting OAuth button prominence, modifying trust signals, or re-ordering form steps.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog, evaluates statistical significance, and decides: Adopt (implement winner permanently), Iterate (new hypothesis based on learnings), Revert (restore control), or Extend (keep running). All decisions logged in Attio with full reasoning.

**Phase 5 — Report (weekly via n8n cron):**
Weekly optimization brief including: anomalies detected, hypotheses generated, experiments run, decisions made, net metric change, current distance from estimated local maximum, and recommended focus for next week.

### 2. Deploy signup funnel health monitoring

Run the `autonomous-optimization` drill. This creates the monitoring infrastructure that feeds the autonomous optimization loop:

- **Dashboard**: 6-panel PostHog dashboard covering overall CVR trend, step-by-step conversion, per-segment performance, form error rate, time to complete, and email verification rate
- **Daily anomaly detection**: n8n workflow checking all metrics against baseline with tiered alerting (Warning, Critical)
- **Deployment regression detection**: webhook-triggered check after each production deploy, alerting if CVR drops >20% within 4 hours
- **Weekly brief generation**: structured report with data, insights, active experiments, and recommended actions
- **Cumulative experiment log**: running total of every autonomous change, its measured lift, and the aggregate improvement

### 3. Configure guardrails

Set up the safety boundaries from `autonomous-optimization`:

- **Rate limit**: Maximum 1 active experiment at a time on the signup funnel
- **Revert threshold**: If signup CVR drops >30% during an experiment, auto-revert immediately
- **Human approval required for**: changes affecting >50% of traffic, changes to OAuth providers, changes to required fields, or any change flagged as high-risk
- **Cooldown**: After a failed experiment, wait 7 days before testing the same variable
- **Monthly cap**: Maximum 4 experiments per month. If all 4 fail, pause and flag for human strategic review

**Human action required:** Review the weekly optimization brief every Monday. Approve or reject any queued high-risk hypotheses. If 3 consecutive experiments fail, conduct a strategic review of the signup funnel architecture.

### 4. Monitor for convergence

The autonomous loop detects convergence when 3 consecutive experiments produce <2% improvement. At convergence:

1. The signup funnel has reached its local maximum
2. The agent reduces monitoring frequency from daily to weekly
3. A convergence report is generated: current performance metrics, total lift achieved since Durable started, list of all changes implemented, and recommendation for what would unlock the next step-change (new signup methods, product architecture changes, or market positioning shifts)

The agent continues weekly monitoring post-convergence to detect if external changes (market shifts, competitor moves, traffic source changes) degrade the funnel, at which point it re-enters the daily optimization loop.

## Time Estimate

- 8 hours: Initial setup of autonomous optimization loop and health monitoring
- Ongoing: ~4 hours/week agent compute (monitoring, hypothesis generation, experiment management)
- Ongoing: ~1 hour/week human review of weekly briefs and high-risk approvals
- Expected convergence: 2-4 months after Durable activation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, experiments, feature flags, funnels, dashboards | Free tier: 1M events/mo. Paid: usage-based from $0.00005/event. [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Cron scheduling for daily monitoring and weekly briefs, webhook triggers | Community (self-hosted): Free. Cloud Pro: ~$60/mo. [n8n.io/pricing](https://n8n.io/pricing/) |
| Anthropic Claude API | Hypothesis generation, experiment evaluation, brief writing | Pay-per-token. ~$3-15/MTok depending on model. [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | Logging experiment results, decisions, and optimization history | Free tier available. Pro: from $29/user/mo. [attio.com/pricing](https://attio.com/pricing) |

## Drills Referenced

- `autonomous-optimization` — the core autonomous loop: monitor metrics, diagnose anomalies, generate hypotheses, run experiments, evaluate results, auto-implement winners, and report weekly
- `autonomous-optimization` — always-on dashboard, daily anomaly detection, deployment regression checks, weekly briefs, and cumulative experiment impact tracking
