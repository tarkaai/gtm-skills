---
name: health-score-alerting
description: Route health score changes to interventions — in-app messages for at-risk, personal outreach for critical, expansion prompts for healthy
category: Product
tools:
  - Attio
  - Intercom
  - Loops
  - n8n
  - PostHog
fundamentals:
  - attio-health-score-sync
  - attio-notes
  - intercom-in-app-messages
  - loops-transactional
  - n8n-triggers
  - n8n-workflow-basics
  - posthog-cohorts
---

# Health Score Alerting

This drill connects health score outputs to concrete interventions. When a score changes, the right action fires automatically: in-app nudges for declining engagement, personal outreach for critical accounts, and expansion prompts for healthy accounts showing growth signals.

## Prerequisites

- Health scores computed and synced to Attio (run `health-score-model-design` drill first)
- Intercom configured with the product's Messenger installed
- Loops configured for triggered emails
- n8n instance connected to Attio, Intercom, Loops, and PostHog
- At least 2 weeks of health score history to establish baselines

## Steps

### 1. Define intervention tiers

Map health score transitions to intervention types. The trigger is the CHANGE, not the absolute score:

**Tier 1 — Proactive nudge (automated, in-app)**
- Trigger: Score drops from Healthy to Monitor, OR any dimension drops >15 points in one week
- Action: In-app message via Intercom highlighting the dimension that dropped
- Example: If engagement_score dropped because the account stopped using a core feature, send: "Your team hasn't used [Feature] in 2 weeks. Here's what's new: [link to changelog]."
- Use `intercom-in-app-messages` to send targeted messages based on the specific declining dimension

**Tier 2 — Outreach email (automated, email)**
- Trigger: Score drops to At Risk (40-59), OR score has been in Monitor for 3+ consecutive weeks with no improvement
- Action: Triggered email via Loops from the account owner
- Template: Personalized with the account's specific usage data. "I noticed your team's usage of [Product] has slowed down. Anything we can help with?"
- Use `loops-transactional` with dynamic properties: account name, declining dimension, specific feature or behavior that changed
- CC the account owner in Attio so they have context

**Tier 3 — Urgent intervention (human-assisted)**
- Trigger: Score drops to Critical (0-39), OR score drops >20 points in a single week regardless of tier
- Action: Create an urgent task in Attio for the account owner. Include: current score, dimension breakdown, score history for the last 8 weeks, specific signals that triggered the drop.
- Use `attio-notes` to log the intervention with full context
- **Human action required:** Account owner calls the customer within 48 hours with a specific plan to address the declining dimension

**Tier 4 — Expansion signal (automated, in-app + CRM)**
- Trigger: Score is Healthy (80+) AND usage_score is in the top 20th percentile AND team_penetration > 80%
- Action: In-app message suggesting next-tier features, team expansion, or plan upgrade. Flag the account in Attio as "Expansion Ready" for the sales team.
- Use `intercom-in-app-messages` for the in-app prompt and `attio-health-score-sync` to update the expansion flag

### 2. Build the alerting workflow in n8n

Using `n8n-triggers`, create a workflow triggered by the daily health score pipeline completing:

1. **Input:** Receive the list of accounts whose scores changed today (from the `health-score-model-design` scoring pipeline)
2. **Classify transitions:** For each account, determine:
   - Previous risk level and current risk level
   - Which dimensions changed and by how much
   - How long the account has been at the current risk level
3. **Route to intervention tier:** Apply the rules from step 1
4. **Execute actions:**
   - Tier 1: Call Intercom API via `intercom-in-app-messages` to queue the in-app message
   - Tier 2: Call Loops API via `loops-transactional` to trigger the outreach email
   - Tier 3: Create Attio note and task via `attio-notes`
   - Tier 4: Call Intercom API for expansion prompt and update Attio record
5. **Log all interventions:** Using PostHog `posthog-cohorts`, track which accounts received which interventions so you can measure intervention effectiveness

### 3. Build intervention effectiveness tracking

For each intervention, track whether it worked:

Using `n8n-workflow-basics`, create a follow-up workflow that runs 14 days after each intervention:

1. Pull the account's current health score from Attio
2. Compare to the score at intervention time
3. Classify outcome:
   - **Recovered:** Score improved by 10+ points or moved to a better risk tier
   - **Stabilized:** Score stopped declining (within +/- 5 points)
   - **Continued declining:** Score dropped further
   - **Churned:** Account cancelled or went inactive
4. Log the outcome in PostHog as `health_intervention_outcome` with properties: intervention_tier, dimension_targeted, days_to_response, outcome

### 4. Configure rate limiting

Prevent alert fatigue:

- Maximum 1 in-app message per account per 7 days (Tier 1)
- Maximum 1 outreach email per account per 14 days (Tier 2)
- No rate limit on Tier 3 (critical accounts need immediate attention)
- Maximum 1 expansion prompt per account per 30 days (Tier 4)
- If an account received a Tier 2 intervention in the last 14 days, do NOT escalate to Tier 3 unless the score drops to Critical. Give the previous intervention time to work.

### 5. Build the weekly intervention summary

Using `n8n-workflow-basics`, generate a weekly report:

```
# Health Score Intervention Summary — Week of [date]

## Overview
- Total accounts scored: [N]
- Healthy: [N] ([%])  |  Monitor: [N] ([%])  |  At Risk: [N] ([%])  |  Critical: [N] ([%])

## Interventions This Week
| Tier | Triggered | Accounts | Recovery Rate |
|------|-----------|----------|---------------|
| Tier 1 (Nudge) | [N] | [list] | [%] |
| Tier 2 (Email) | [N] | [list] | [%] |
| Tier 3 (Urgent) | [N] | [list] | [%] |
| Tier 4 (Expansion) | [N] | [list] | [N/A] |

## Biggest Movers
- Improved most: [Account] — [old score] → [new score] (reason)
- Declined most: [Account] — [old score] → [new score] (reason)

## Intervention Effectiveness (trailing 30 days)
- Recovery rate (all tiers): [%]
- Average time to recovery: [N] days
- Most effective intervention type: [Tier X]
```

Post to Slack and store in Attio.

## Output

- An n8n workflow that routes health score changes to the appropriate intervention
- Automated in-app messages for declining accounts (Tier 1)
- Automated outreach emails for at-risk accounts (Tier 2)
- CRM tasks for critical accounts requiring human intervention (Tier 3)
- Expansion signals for healthy accounts (Tier 4)
- Intervention effectiveness tracking with 14-day follow-up
- Weekly intervention summary report

## Triggers

- Alerting workflow: triggered by daily health score pipeline completion
- Intervention follow-up: 14 days after each intervention
- Weekly summary: cron, Monday 09:00 UTC
