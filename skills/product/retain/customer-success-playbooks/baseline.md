---
name: customer-success-playbooks-baseline
description: >
  CS Intervention Playbooks -- Baseline Run. Deploy the 5 validated playbooks as always-on
  automations that trigger, execute, and log interventions daily without manual execution.
  Measure sustained playbook success rate over 4 weeks.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email, Direct"
level: "Baseline Run"
time: "16 hours over 4 weeks"
outcome: ">=60% playbook success rate sustained over 4 weeks"
kpis: ["Playbook success rate", "Intervention reach", "Save rate by tier", "Time-to-resolution"]
slug: "customer-success-playbooks"
install: "npx gtm-skills add product/retain/customer-success-playbooks"
drills:
  - churn-risk-scoring
  - churn-intervention-routing
  - posthog-gtm-events
---

# CS Intervention Playbooks -- Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Direct

## Outcomes

All 5 CS playbooks running as always-on automations via n8n. Every at-risk user (medium+ risk tier) whose churn signal matches a playbook receives the correct intervention within 24 hours. Sustained success rate of >=60% (interventions that reduce risk score within 14 days) over a 4-week evaluation window.

## Leading Indicators

- Daily churn scoring pipeline running without errors
- Intervention routing matching >90% of at-risk users to a playbook
- Playbook step completion rate >80% (interventions executing fully, not breaking mid-playbook)
- Risk score improvements appearing within 7 days of intervention for early cohorts

## Instructions

### 1. Deploy daily churn risk scoring

Run the `churn-risk-scoring` drill to build and deploy the daily scoring pipeline. This creates an n8n workflow triggered by daily cron (06:00 UTC) that:

1. Queries PostHog for all active users with their behavioral signal metrics
2. Computes a composite churn risk score (0-100) for each user
3. Classifies users into risk tiers: low (0-25), watch (26-45), medium (46-65), high (66-85), critical (86-100)
4. Identifies the primary churn signal driving each user's score
5. Syncs scores to PostHog (as `churn_risk_scored` events) and Attio (as custom attributes)
6. Creates dynamic PostHog cohorts per risk tier

Validate the scoring pipeline by checking: do the users scored high/critical match your intuition? Pull 10 high-risk users and review their actual usage in PostHog. If the model is flagging healthy users, adjust signal weights before proceeding.

### 2. Configure event tracking for playbook execution

Run the `posthog-gtm-events` drill to instrument all playbook-related events:

- `playbook_triggered` -- properties: `playbook_name`, `user_id`, `risk_score`, `risk_tier`, `primary_signal`, `trigger_timestamp`
- `playbook_step_completed` -- properties: `playbook_name`, `step_number`, `step_type` (email/in_app/task), `channel`, `timestamp`
- `playbook_step_failed` -- properties: `playbook_name`, `step_number`, `error_type`, `error_message`
- `playbook_outcome_logged` -- properties: `playbook_name`, `user_id`, `success` (boolean), `risk_score_before`, `risk_score_after`, `days_to_outcome`

Build a PostHog funnel: `playbook_triggered` -> `playbook_step_completed` (all steps) -> `playbook_outcome_logged (success=true)`. This is the core conversion funnel for the play.

### 3. Deploy automated intervention routing

Run the `churn-intervention-routing` drill to build the n8n workflow that matches at-risk users to playbooks and executes the interventions automatically. The workflow runs daily at 08:00 UTC (after scoring completes at 06:00):

1. Queries Attio for all users with `churn_risk_tier` in [medium, high, critical] who have NOT received an intervention in the last 14 days
2. For each user, matches their `primary_signal` to the appropriate playbook
3. Executes the playbook's intervention steps:
   - Medium risk: Intercom in-app message (from the playbook's step 1)
   - High risk: Loops email sequence (from the playbook's full step sequence)
   - Critical risk: Attio task for account owner + Intercom message (human-assisted)
4. Logs each step as a `playbook_step_completed` event in PostHog
5. Records the intervention in Attio as a note on the user's record with full context

### 4. Implement outcome tracking

Build an n8n workflow that runs 14 days after each intervention to measure outcomes:

1. Pull the user's current churn risk score from Attio
2. Compare to the score at intervention time (stored in the `playbook_triggered` event)
3. Classify outcome:
   - **Success:** Risk score decreased by 10+ points OR user moved to a lower risk tier
   - **Partial:** Risk score decreased 1-9 points but user stayed in same tier
   - **No effect:** Risk score unchanged or increased
   - **Churned:** User cancelled or went inactive during the 14-day window
4. Fire a `playbook_outcome_logged` event in PostHog with the classification
5. Update the intervention note in Attio with the outcome

### 5. Monitor and evaluate over 4 weeks

Run the play for 4 full weeks. At the end of each week, check:

- How many at-risk users were identified?
- How many received interventions (intervention reach)?
- How many interventions completed all steps (completion rate)?
- How many produced a successful outcome (success rate)?

Target: >=60% success rate (successful outcomes / completed interventions).

If success rate is below 60% after week 2, diagnose by playbook: which playbook is underperforming? Check the step drop-off in PostHog to find where interventions are breaking. Common fixes:
- Email not being opened: revise subject line and send timing
- In-app message not clicked: revise copy and targeting
- Risk score not improving despite engagement: the intervention addresses a symptom, not the root cause

**Human action required:** Review the first week's outcomes before letting the system run autonomously for weeks 2-4. Confirm that automated interventions are being sent to the right people with appropriate messaging. Spot-check 5 critical-tier interventions to ensure the Attio tasks contain enough context for account owners to act effectively.

## Time Estimate

- 4 hours: Deploying churn risk scoring pipeline and validating accuracy
- 3 hours: Configuring PostHog event tracking for all playbook events
- 4 hours: Building and testing the intervention routing workflow in n8n
- 2 hours: Building the 14-day outcome tracking workflow
- 3 hours: Weekly monitoring, diagnosis, and adjustment over 4 weeks

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage analytics, churn scoring, event tracking, funnels | Free up to 1M events/mo; https://posthog.com/pricing |
| Attio | CRM for risk scores, intervention logging, outcome tracking | Free for small teams; https://attio.com/pricing |
| Intercom | In-app messaging for medium-risk and critical-risk interventions | From $39/seat/mo; https://www.intercom.com/pricing |
| Loops | Email sequences for high-risk intervention playbooks | Free up to 1K contacts; https://loops.so/pricing |
| n8n | Workflow automation for scoring, routing, and outcome tracking | Free self-hosted; cloud from $20/mo; https://n8n.io/pricing |

## Drills Referenced

- `churn-risk-scoring` -- builds the daily churn risk scoring pipeline that feeds playbook triggers
- `churn-intervention-routing` -- routes at-risk users to the correct playbook and executes interventions
- `posthog-gtm-events` -- instruments all playbook events for tracking and measurement
