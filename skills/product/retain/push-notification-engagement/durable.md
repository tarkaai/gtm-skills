---
name: push-notification-engagement-durable
description: >
  Push Notification Strategy — Durable Intelligence. Always-on AI agents autonomously
  optimize push notification campaigns by detecting metric anomalies, generating
  improvement hypotheses, running A/B experiments, and auto-implementing winners.
  Converges when successive experiments produce <2% improvement.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "150 hours over 6 months"
outcome: "Sustained or improving CTR ≥30% over 6 months via autonomous optimization"
kpis: ["Push CTR", "Opt-in rate", "DAU lift", "Experiment velocity", "AI lift"]
slug: "push-notification-engagement"
install: "npx gtm-skills add product/retain/push-notification-engagement"
drills:
  - autonomous-optimization
---

# Push Notification Strategy — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
An autonomous AI agent continuously monitors push notification performance, detects when metrics plateau or decline, generates hypotheses for improvement, designs and runs A/B experiments, evaluates results, and auto-implements winners. The agent produces weekly optimization briefs documenting every change and its impact. CTR sustains at or above 30% over 6 months. The agent converges when successive experiments produce less than 2% improvement — at that point the push program has found its local maximum.

## Leading Indicators
- Anomaly detection triggers within 24 hours of a metric shift
- Agent generates 3 ranked hypotheses per anomaly with expected impact and risk levels
- Experiments achieve statistical significance within planned duration
- Winning experiments are auto-implemented without human intervention (for low/medium risk)
- Weekly optimization briefs are generated on schedule with accurate metric attribution
- High-risk hypotheses are correctly flagged for human review (never auto-implemented)
- Month-over-month CTR is stable or improving, not declining

## Instructions

### 1. Deploy the autonomous optimization loop
Run the `autonomous-optimization` drill configured for push notification metrics. The drill creates a 5-phase always-on loop:

**Phase 1 — Monitor (daily via n8n cron):**
The agent queries PostHog for the push program's primary KPIs: overall CTR, per-segment CTR, opt-out rate, delivery rate, DAU lift, and push subscriber retention. It compares the last 2 weeks against a 4-week rolling average. It classifies each metric as normal (within ±10%), plateau (±2% for 3+ weeks), drop (>20% decline), or spike (>50% increase). Normal metrics are logged. Anomalies trigger Phase 2.

**Phase 2 — Diagnose (triggered by anomaly):**
The agent gathers context: current push campaigns, segment configurations, send schedules, recent A/B test results, and 8-week metric history from PostHog. It runs the `hypothesis-generation` fundamental with this context. It receives 3 ranked hypotheses, each with expected impact, risk level, and the specific change to test. Example hypotheses:
- "CTR plateau in the regular-user segment is caused by copy fatigue — test new copy templates emphasizing social proof instead of personal metrics" (medium risk, expected +5pp CTR)
- "Opt-out spike correlates with increased send frequency last week — test reducing frequency from 2/day to 1/day for casual users" (low risk, expected -60% opt-out rate)
- "DAU lift declining because push deep links go to the dashboard instead of the specific new content — test content-specific deep links" (low risk, expected +3pp DAU lift)

High-risk hypotheses (audience changes affecting >50% of subscribers, major frequency changes) are flagged for human review and paused until approved.

**Phase 3 — Experiment (triggered by hypothesis acceptance):**
The agent takes the top-ranked hypothesis and designs the experiment. It uses `posthog-experiments` to create a feature flag splitting traffic between control and variant. It implements the variant: if testing copy, create a new push template in OneSignal; if testing timing, modify the n8n schedule for the variant group; if testing deep links, update the URL in the push payload. The experiment runs for minimum 7 days or until 200+ users per variant, whichever is longer.

**Phase 4 — Evaluate (triggered by experiment completion):**
The agent pulls experiment results from PostHog and runs the `experiment-evaluation` fundamental. Four possible decisions:
- **Adopt**: Variant wins with statistical significance. Auto-implement the change across all campaigns. Log the change with before/after metrics.
- **Iterate**: Results are inconclusive or suggest a different angle. Generate a refined hypothesis and return to Phase 2.
- **Revert**: Variant performed worse than control. Disable variant, restore control. Log the failure. Wait 7-day cooldown before testing the same variable.
- **Extend**: Not enough data yet. Keep the experiment running for another period.

**Phase 5 — Report (weekly via n8n cron):**
The agent generates a weekly optimization brief:
- Anomalies detected this week and how they were classified
- Hypotheses generated and their risk assessments
- Experiments running, completed, or started this week
- Net metric change from all adopted changes
- Current performance vs estimated local maximum
- Recommended focus for next week

Post the brief to Slack and store in Attio.

### 2. Configure push-specific optimization targets
The `autonomous-optimization` drill is play-agnostic. Configure it with these push-specific parameters:

**Primary KPIs to monitor:**
- Overall CTR (target: ≥30%)
- Per-segment CTR (floor: 20% per segment)
- Weekly opt-out rate (ceiling: 1%)
- DAU lift (target: ≥15pp)
- Push subscriber 30-day retention vs non-subscriber retention (target: ≥10pp lift)

**Variables the agent can experiment on (without human approval):**
- Push copy (title, body text)
- Deep link destination
- Send time within the user's peak window (±2 hours)
- Emoji presence/absence
- Notification priority (normal vs high)

**Variables requiring human approval:**
- Send frequency changes (increase or decrease)
- New segment targeting (adding or removing a segment from a campaign)
- Opt-in prompt changes (copy, timing, placement)
- Adding or removing entire campaign types

**Guardrails:**
- Maximum 1 active experiment at a time across all push campaigns
- Auto-revert if any metric drops >30% during an experiment
- Cooldown: 7 days after a failed experiment before testing the same variable
- Maximum 4 experiments per month; if all 4 fail, pause optimization and flag for human strategic review
- Never optimize without sufficient data: minimum 200 deliveries per variant

### 3. Extend push health monitoring for Durable
Run the `autonomous-optimization` drill with expanded scope for the Durable level:

Add these panels to the PostHog dashboard:
- **Experiment timeline**: visual timeline showing every experiment, its duration, and outcome (adopted/reverted/iterated)
- **Cumulative AI lift**: the total CTR improvement attributable to autonomous optimization since Durable started
- **Convergence tracker**: CTR improvement per experiment, plotted over time. When 3 consecutive experiments produce <2% improvement, the play has converged.
- **Hypothesis quality**: percentage of hypotheses that led to adopted experiments (track whether the agent's hypotheses are getting better over time)

### 4. Expand campaign repertoire based on learnings
Run the the push notification campaign workflow (see instructions below) drill periodically to add new campaign types based on what the optimization loop discovers:

- If the agent finds that social-proof copy ("your team did X") consistently wins, build a dedicated social-activity notification campaign
- If send-time optimization shows specific time windows outperform others by >5pp, create time-window-specific campaigns with tailored copy
- If feature-discovery pushes drive adoption >20%, expand to cover more features

The agent should propose new campaign types when it detects that existing campaigns have converged but new user behaviors suggest untapped opportunities.

### 5. Monitor convergence and adapt
The optimization loop runs indefinitely. However, when the agent detects convergence (3 consecutive experiments produce <2% improvement):

1. The push program has found its local maximum for the current user base and product
2. Reduce monitoring frequency from daily to weekly
3. Generate a convergence report: current performance levels, what was optimized, what further gains would require (product changes, new features, new user segments)
4. The agent shifts to maintenance mode: monitoring for external changes (product updates, seasonal shifts, user base composition changes) that could create new optimization opportunities

If convergence breaks (metrics shift >10% due to external factors), the agent returns to daily monitoring and the full optimization loop.

## Time Estimate
- 15 hours: Configure autonomous optimization loop, push-specific parameters, guardrails
- 10 hours: Extend health monitoring dashboard with experiment and convergence tracking
- 100 hours: Agent runtime over 6 months (daily monitoring, monthly experiments, weekly reports)
- 15 hours: Monthly human review of optimization briefs, guardrail checks, strategic input
- 10 hours: Convergence analysis, documentation, strategic recommendations

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| OneSignal | Push delivery, variant management | Growth: $19/mo + ~$2-10/mo usage |
| Anthropic (Claude) | Hypothesis generation, experiment evaluation, weekly briefs | ~$20-50/mo based on loop frequency |
| PostHog | Analytics, experiments, feature flags, anomaly detection | Standard stack — excluded |
| n8n | Optimization loop orchestration, scheduling | Standard stack — excluded |
| Attio | Experiment audit trail, weekly brief storage | Standard stack — excluded |

## Drills Referenced
- `autonomous-optimization` — the core monitor-diagnose-experiment-evaluate-implement loop that finds the local maximum
- `autonomous-optimization` — extended with experiment timeline, AI lift tracking, and convergence detection
- the push notification campaign workflow (see instructions below) — expand campaign repertoire based on optimization discoveries
