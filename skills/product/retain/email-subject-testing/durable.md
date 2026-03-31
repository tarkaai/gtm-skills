---
name: email-subject-testing-durable
description: >
  Email Subject-Line A/B Testing — Durable Intelligence. Autonomous AI agent continuously monitors
  email open rates, generates subject-line hypotheses, runs experiments, and auto-implements winners
  to find and maintain the local maximum for every retention email.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Email"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Open-rate lift sustained or improving over 6 months via autonomous optimization; convergence detected when successive experiments produce <2% improvement"
kpis: ["Open rate by email and segment", "Click rate", "Experiment velocity (tests/month)", "Win rate (% of tests where variant beats control)", "Convergence status per email", "Unsubscribe rate"]
slug: "email-subject-testing"
install: "npx gtm-skills add product/retain/email-subject-testing"
drills:
  - autonomous-optimization
  - email-subject-performance-monitor
  - dashboard-builder
---

# Email Subject-Line A/B Testing — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Email

## Outcomes

An always-on AI agent monitors open rates across every retention email, detects when performance plateaus or drops, generates subject-line improvement hypotheses, runs A/B experiments, evaluates results, and auto-implements winners. The agent finds the local maximum for each email's subject line and maintains it as audience behavior shifts. Weekly optimization briefs report what changed and why. The system converges when successive experiments produce <2% improvement for 3 consecutive tests on a given email.

## Leading Indicators

- The autonomous optimization loop runs daily without manual intervention
- At least 2 experiments per month are auto-generated from anomaly detection
- Win rate on auto-generated experiments is >40% (the agent is generating good hypotheses)
- No retention email has an open rate >15% below its 4-week rolling average for 2+ consecutive weeks without an active experiment
- Weekly optimization briefs are generated and posted to Slack on schedule

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill configured for email subject-line testing. The drill creates a 5-phase always-on loop:

**Phase 1 — Monitor (daily via n8n cron):**
The agent uses PostHog anomaly detection to check open rates for every retention email. It compares the last 2 weeks against the 4-week rolling average. Classification:
- **Normal:** within +/-10% of rolling average. No action.
- **Plateau:** within +/-2% for 3+ weeks. The current subject has maxed out. Trigger Phase 2.
- **Drop:** >15% decline. Something changed (audience fatigue, deliverability issue, or seasonal shift). Trigger Phase 2.
- **Spike:** >50% increase. Investigate whether a recent change caused it. Log and monitor.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: the email's current subject line, its historical open rates, the audience segment, the framing category used, and recent changes. It runs hypothesis generation via the Claude API with this context. It receives 3 ranked hypotheses, each specifying:
- A specific subject-line change (e.g., "Switch from direct-value framing to curiosity gap: change 'New: PDF export for reports' to 'The report feature your team has been asking about'")
- Rationale based on the data
- Expected impact
- Risk level

If the top hypothesis is high-risk, the agent sends a Slack alert for human review and stops. Otherwise, it proceeds to Phase 3.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent takes the top hypothesis and creates a subject-line A/B test in Loops:
- Control: current subject line
- Variant: the hypothesized improvement
- Split: 50/50 for sequences, or 25/25/50-holdback for broadcasts
- Duration: minimum 7 days or until 200+ sends per variant

The agent logs the experiment in Attio: hypothesis, start date, expected duration, success criteria.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls results from PostHog and runs experiment evaluation via the Claude API. Decision:
- **Adopt:** Variant wins by >3pp open rate with no unsubscribe increase. Update the Loops template to use the winning subject. Log the change.
- **Iterate:** Variant shows promise but <3pp lift. Generate a new hypothesis building on the variant. Return to Phase 2.
- **Revert:** Variant performs worse. Restore the control subject. Log the failure with reasoning. Return to Phase 1.
- **Extend:** Insufficient sends for reliable comparison. Keep running for another 7 days.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week
- Experiments running, completed, and their outcomes
- Net open-rate change from all adopted subject-line changes
- Current distance from estimated local maximum per email
- Convergence status: which emails have converged (3 consecutive experiments with <2% lift)

Post the brief to Slack and store in Attio.

### 2. Build the executive email performance dashboard

Run the `dashboard-builder` drill to create a Durable-level PostHog dashboard:

- **Aggregate open rate trend (6 months):** Shows the overall trajectory of retention email performance
- **Per-email convergence status:** Table showing each retention email, its current open rate, its estimated local maximum, and whether it has converged
- **Experiment log:** Timeline of all experiments run, their outcomes, and cumulative lift
- **Win rate trend:** Percentage of experiments where the variant beat the control, plotted monthly
- **Segment heatmap:** Open rate by email type x user segment, highlighting underperforming combinations

### 3. Configure Durable-specific monitoring

Run the `email-subject-performance-monitor` drill at Durable frequency:
- Anomaly checks run daily (up from weekly at Baseline)
- Pattern library is automatically updated by the optimization loop
- Monthly pattern analysis: the agent reviews the full pattern library and identifies emerging trends (e.g., "curiosity framing is losing effectiveness, social proof is gaining")

### 4. Set guardrails

**Critical guardrails the agent MUST enforce:**
- Maximum 1 active subject-line experiment per email at a time. Never stack experiments on the same email.
- If any email's unsubscribe rate exceeds 1% during a test, auto-revert immediately and flag for human review.
- Maximum 4 experiments per email per month. If all 4 fail on the same email, mark it as converged and pause optimization.
- After a failed experiment, wait 7 days before testing a new variant on the same email (cooldown).
- If aggregate open rate across all retention emails drops >20% for 2 consecutive weeks, pause all experiments and alert the team (likely a deliverability issue, not a subject-line issue).

### 5. Evaluate sustainability

This level runs continuously. Monthly check: are open rates across tested emails sustained or improving compared to 30 days ago? If yes, the play is durable. If open rates are decaying despite active optimization, the agent diagnoses whether the issue is subject-line exhaustion (need new framing categories), audience shift (segment definitions need updating), or deliverability degradation (separate from subject testing).

Convergence milestone: when >80% of retention emails have converged (3 consecutive experiments with <2% lift each), the play has found its local maximum. Reduce the monitoring cadence from daily to weekly. Report to the team: "Subject-line optimization has converged. Current aggregate open rate is X%. Further gains require strategic changes (new email types, audience expansion, send-time optimization) rather than subject-line testing."

## Time Estimate

- 20 hours: Configure autonomous optimization loop (n8n workflows, Claude API prompts, Loops integration)
- 10 hours: Build executive dashboard and Durable-level monitoring
- 8 hours: Configure guardrails and test the revert/cooldown logic
- 12 hours: Monitor and tune the agent during the first month (adjust anomaly thresholds, review hypothesis quality)
- 100 hours: Agent runs autonomously over 6 months (human oversight: ~4 hours/month reviewing briefs and approving high-risk experiments)

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Loops | Send emails, manage sequences, execute subject-line changes | Starter $49/mo (5K contacts); Growth scales with contacts — [loops.so/pricing](https://loops.so/pricing) |
| PostHog | Track events, run anomaly detection, build dashboards | Free up to 1M events/mo; usage-based above — [posthog.com/pricing](https://posthog.com/pricing) |
| n8n | Cron scheduling for daily monitor + weekly reports, experiment orchestration | Self-hosted free; Cloud from ~$24/mo — [n8n.io/pricing](https://n8n.io/pricing) |
| Anthropic API | Hypothesis generation and experiment evaluation via Claude | Usage-based; ~$3/MTok input, $15/MTok output for Sonnet — [anthropic.com/pricing](https://www.anthropic.com/pricing) |
| Attio | Log experiments, store pattern library, campaign records | Free for small teams; paid from $29/seat/mo — [attio.com/pricing](https://attio.com/pricing) |

**Estimated play-specific cost:** Loops ~$49-149/mo + Anthropic API ~$10-30/mo (est. 4-8 hypothesis + evaluation calls/month)

## Drills Referenced

- `autonomous-optimization` — the core always-on loop: monitor -> diagnose -> experiment -> evaluate -> implement. This is what makes Durable fundamentally different from Scalable.
- `email-subject-performance-monitor` — daily anomaly checks, pattern library maintenance, and monthly trend analysis at Durable frequency
- `dashboard-builder` — executive PostHog dashboard with convergence status, experiment log, and segment heatmap
