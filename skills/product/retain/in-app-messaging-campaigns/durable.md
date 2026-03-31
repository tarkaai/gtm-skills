---
name: in-app-messaging-campaigns-durable
description: >
  Behavioral In-App Messages — Durable Intelligence. Autonomous AI agent continuously monitors
  message campaign performance, detects engagement decay and fatigue, generates improvement
  hypotheses, runs A/B experiments, and auto-implements winners. Finds and maintains the
  local maximum for in-app messaging effectiveness.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Durable Intelligence"
time: "20 hours setup + ongoing autonomous operation over 6 months"
outcome: "Sustained or improving CTR ≥40% over 6 months with autonomous optimization"
kpis: ["Message CTR", "Message-to-action conversion rate", "Experiment velocity", "AI lift vs pre-optimization baseline", "Fatigue index trend"]
slug: "in-app-messaging-campaigns"
install: "npx gtm-skills add product/retain/in-app-messaging-campaigns"
drills:
  - autonomous-optimization
  - nps-feedback-loop
---

# Behavioral In-App Messages — Durable Intelligence

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

The in-app messaging portfolio sustains or improves 40% CTR over 6 months without manual campaign management. An autonomous AI agent runs the optimization loop: detect metric anomalies, generate hypotheses for what to change, run A/B experiments, evaluate results, and auto-implement winners. The agent also monitors message fatigue across the user base and rotates or retires campaigns before they degrade engagement. This level converges when successive experiments produce <2% improvement — the portfolio has reached its local maximum.

## Leading Indicators

- Experiment velocity: target 3-4 experiments per month across the portfolio
- Experiment win rate: target 30%+ of experiments produce a statistically significant winner
- AI lift: cumulative CTR improvement from agent-implemented changes vs. the Scalable baseline
- Fatigue index trend: the percentage of users in the "fatigued" cohort should be stable or declining
- Anomaly detection latency: time from metric drop to hypothesis generation (target: <24 hours)
- Convergence signal: 3 consecutive experiments producing <2% improvement indicates the local maximum

## Instructions

### 1. Deploy the autonomous optimization loop

Run the `autonomous-optimization` drill to configure the always-on agent loop for this play. The drill handles the core cycle: monitor, diagnose, experiment, evaluate, implement. Configure it with these play-specific parameters:

**Primary KPIs to monitor:**
- Portfolio CTR (clicked / seen across all campaigns)
- Portfolio conversion rate (converted / clicked)
- Per-campaign CTR (to detect individual campaign decay)
- Fatigue index (dismissals per user over trailing 14 days)

**Anomaly thresholds:**
- Normal: portfolio CTR within ±5% of 4-week rolling average
- Plateau: CTR ±2% for 3+ consecutive weeks
- Drop: any single campaign CTR drops >15% week-over-week
- Fatigue spike: fatigued user cohort grows >20% in a single week

**Hypothesis space (what the agent can change):**
- Message copy (headline, body, CTA text) — any campaign
- Message format (banner, tooltip, slideout) — any campaign
- Delivery timing (immediate vs. delayed vs. next-session) — any campaign
- Audience targeting (cohort criteria adjustments) — within existing segments only
- Frequency capping (increase or decrease cooldown periods) — any campaign
- Campaign retirement (pause a campaign whose variants are exhausted)

**What requires human approval:**
- Creating entirely new campaign types (new behavioral triggers)
- Changing the underlying trigger event definition
- Modifying segment definitions that affect >50% of users
- Any change to upgrade prompt pricing display or CTA destination

**Experiment constraints:**
- Maximum 1 active experiment per campaign at a time
- Maximum 4 total experiments running across the portfolio simultaneously
- Minimum experiment duration: 7 days or 200 impressions per variant
- Auto-revert if any campaign's CTR drops >30% during an experiment

### 2. Deploy the message health monitoring system

Run the `autonomous-optimization` drill to build the monitoring layer specific to in-app messaging. This drill creates:

**Fatigue detection (daily):** An n8n workflow that queries PostHog for the fatigued users cohort (dismissed 3+ messages in 14 days OR ignored 5+ messages in 30 days). Syncs the fatigue flag to Intercom so fatigued users are excluded from non-critical messages. Logs fatigue trend in Attio.

**Engagement decay alerting (every 3 days):** An n8n workflow that checks each campaign's week-over-week engagement rate. Stable (within ±5%): no action. Declining (>10% drop for 2 checks): alerts via Slack, queues the campaign for the autonomous optimization loop. Collapsing (>25% drop or below 8% CTR): pauses the campaign automatically.

**Message rotation (triggered by decay alert):** When a campaign's engagement decays, the agent checks for alternate variants. If variants exist, rotate to the next one. If no variants exist, reduce frequency by 50% and flag for the autonomous optimization loop to generate a new hypothesis. If 3+ variants have all decayed, retire the campaign and log it.

**Weekly health report:** Aggregates all messaging activity for the week: messages delivered, engagement rates, top and bottom performers, fatigue trend, experiments in progress, and recommendations for the next week. Delivered via Slack and stored in Attio.

### 3. Close the feedback loop with qualitative data

Run the `nps-feedback-loop` drill to collect qualitative signal that the agent uses to improve messaging:

1. Deploy micro-NPS surveys via Intercom at key milestones: after a user completes a feature adoption campaign's target action (they adopted), and after 30 days of receiving regular messaging.

2. Route responses into the optimization loop:
   - **Promoter feedback** (9-10): Extract what they value about the messaging. Feed positive patterns into the hypothesis generator as "keep doing this."
   - **Passive feedback** (7-8): Identify what is "fine but not great." These users are candidates for more targeted messaging.
   - **Detractor feedback** (0-6): Extract specific complaints about messaging frequency, relevance, or intrusiveness. Feed these into the hypothesis generator as "fix this."

3. Track NPS by messaging exposure: compare NPS scores between users who received 0, 1-3, 4-7, and 8+ messages in the last 30 days. If NPS declines with message volume, the fatigue threshold needs tightening.

### 4. Configure the convergence detection

The autonomous optimization loop should detect when the portfolio has reached its local maximum. Convergence criteria:

- 3 consecutive experiments across different campaigns each produce <2% improvement
- The fatigue index is stable (not growing)
- Portfolio CTR has been within ±3% of the peak for 4+ weeks

When convergence is detected:
1. Reduce monitoring frequency from daily to weekly
2. Reduce experiment velocity from 3-4/month to 1/month (maintenance mode)
3. Generate a convergence report: "In-app messaging has reached its local maximum. Current performance: [metrics]. Messaging portfolio generates [X conversions/week] and contributes to [Y% churn reduction]. Further gains require strategic changes: new behavioral triggers from product changes, new user segments, or new message formats."
4. Store the report in Attio and deliver via Slack

### 5. Evaluate sustainability

Measure over the full 6-month period:

- **Portfolio CTR sustained ≥40%:** The agent maintained or improved engagement through autonomous optimization
- **AI lift:** Total CTR improvement from agent-implemented changes vs. the Scalable baseline
- **Experiment efficiency:** Percentage of experiments that produced a winner (target: 30%+)
- **Fatigue management:** Fatigued user cohort remained below 10% of active users
- **Time saved:** Hours of manual campaign management replaced by autonomous operation

This level runs continuously. Monthly review: what the agent changed, what it learned, what converged, and what needs strategic input.

**Human action required:** Monthly review of the agent's optimization brief. Approve or reject any flagged changes. Provide strategic input on new campaign types or audience expansions that the agent cannot initiate on its own.

## Time Estimate

- 6 hours: Autonomous optimization loop configuration (play-specific parameters, hypothesis space, guardrails)
- 5 hours: Message health monitoring system (fatigue detection, decay alerting, rotation logic)
- 4 hours: NPS feedback loop integration (survey deployment, response routing, analysis)
- 3 hours: Convergence detection setup, reporting templates, Attio logging
- 2 hours: End-to-end testing of all automated workflows
- Ongoing: 1-2 hours/month for human review of optimization briefs and strategic input

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, cohorts, experiments, feature flags, anomaly detection | Free up to 1M events/mo, ~$0.00005/event beyond — https://posthog.com/pricing |
| Intercom | In-app message delivery, surveys, fatigue management | Advanced $85/seat/mo, Proactive Support $349/mo + usage — https://www.intercom.com/pricing |
| n8n | Automation for monitoring loops, decay alerting, rotation logic, weekly reports | Self-hosted free, Cloud from $24/mo — https://n8n.io/pricing |
| Anthropic Claude | Hypothesis generation, experiment evaluation, weekly optimization briefs | API usage-based, ~$15-50/mo at this experiment velocity — https://www.anthropic.com/pricing |
| Loops | Fallback email for users not reachable in-app | Free up to 1,000 contacts, $49/mo for 5K — https://loops.so/pricing |
| Attio | Logging optimization history, fatigue trends, convergence reports | Free up to 3 users — https://attio.com/pricing |

**Play-specific cost:** ~$150-500/mo (Intercom Proactive Support + Anthropic API are the primary costs; the rest is covered by existing stack)

## Drills Referenced

- `autonomous-optimization` — the core agent loop that monitors metrics, generates hypotheses, runs experiments, evaluates results, and auto-implements winners
- `autonomous-optimization` — monitors message fatigue, delivery rates, engagement decay, and triggers campaign rotation
- `nps-feedback-loop` — collects qualitative user feedback to inform the optimization loop's hypothesis generation
