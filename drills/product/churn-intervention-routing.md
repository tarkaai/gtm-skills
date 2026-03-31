---
name: churn-intervention-routing
description: Route at-risk users to tiered interventions based on churn risk score and primary signal
category: Retention
tools:
  - PostHog
  - Intercom
  - Loops
  - Attio
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-feature-flags
  - intercom-in-app-messages
  - loops-sequences
  - attio-contacts
  - attio-notes
  - n8n-triggers
  - n8n-workflow-basics
---

# Churn Intervention Routing

This drill takes the churn risk scores produced by `churn-signal-extraction` and routes each at-risk user to the appropriate intervention. Interventions are tiered by risk severity and personalized around the user's primary churn signal.

## Input

- At-risk user cohorts in PostHog (from `churn-signal-extraction`)
- Churn risk scores and primary signals stored in Attio
- Intercom configured for in-app messaging
- Loops configured for triggered email sequences
- n8n instance for workflow orchestration

## Steps

### 1. Build the routing workflow in n8n

Using `n8n-triggers`, create a workflow triggered daily after the churn scoring pipeline completes. The workflow queries Attio for all users with `churn_risk_tier` in [medium, high, critical] who have not already received an intervention in the last 14 days.

Using `n8n-workflow-basics`, implement the routing logic:

```
IF risk_tier = "critical" (76-100):
  -> Create Attio task for account owner with user's signal data
  -> Send Intercom targeted message: "Your account manager will reach out"
  -> Log intervention: type=personal_outreach, risk_score, primary_signal

IF risk_tier = "high" (51-75):
  -> Enroll in Loops re-engagement sequence personalized to primary_signal
  -> If primary_signal = "activity_decay": send "We noticed you've been less active" email
  -> If primary_signal = "feature_abandonment": send "Here's what's new in [feature]" email
  -> If primary_signal = "support_escalation": send "We want to make sure [product] is working for you" email
  -> Log intervention: type=email_sequence, risk_score, primary_signal

IF risk_tier = "medium" (26-50):
  -> Trigger Intercom in-app message highlighting an unused feature relevant to their signal
  -> If primary_signal = "engagement_narrowing": show tooltip for a feature they haven't tried
  -> If primary_signal = "login_gap": show "Welcome back" message with recent product updates
  -> Log intervention: type=in_app_message, risk_score, primary_signal
```

### 2. Create intervention templates

**For Intercom (in-app messages):**

Using `intercom-in-app-messages`, create message templates for each risk tier and signal combination. Use PostHog feature flags via `posthog-feature-flags` to control which users see which messages. Target by the PostHog cohort (medium-risk, high-risk).

**For Loops (email sequences):**

Using `loops-sequences`, create 3-email sequences per primary signal:
- Email 1 (Day 0): Acknowledge the signal, provide value (tutorial, update, feature highlight)
- Email 2 (Day 3): Social proof — how similar users got value from the product
- Email 3 (Day 7): Direct ask — "Is there something we can help with?" with a calendar booking link

### 3. Implement intervention cooldowns

No user should receive more than 1 intervention per 14-day window. Track intervention history in Attio using `attio-notes`:

```json
{
  "type": "churn_intervention",
  "date": "2026-03-30",
  "risk_score": 68,
  "risk_tier": "high",
  "primary_signal": "activity_decay",
  "intervention_type": "email_sequence",
  "sequence_id": "reengagement-activity-decay"
}
```

Before routing a user, check Attio for any intervention note in the last 14 days. If found, skip.

### 4. Track intervention outcomes

Using `posthog-cohorts`, create outcome cohorts:
- **Saved:** Was at-risk, received intervention, activity increased within 14 days
- **Declined:** Was at-risk, received intervention, activity continued declining
- **Churned despite intervention:** Was at-risk, received intervention, cancelled subscription

Log outcomes back to Attio and PostHog for model calibration.

## Output

- Users routed to appropriate interventions based on risk tier and primary signal
- Intervention history logged in Attio for cooldown tracking
- Outcome tracking configured for measuring intervention effectiveness
- Save rate metric: (saved users / total interventions) calculated weekly

## Triggers

- Run daily, 1 hour after churn scoring pipeline completes
- Respect 14-day cooldown per user
- Pause all interventions if save rate drops below 5% for 2 consecutive weeks (signals the model or interventions need recalibration)
