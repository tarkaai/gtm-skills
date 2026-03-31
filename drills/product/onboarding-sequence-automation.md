---
name: onboarding-sequence-automation
description: Wire onboarding email sequences to behavioral triggers using n8n, PostHog events, and Loops API for always-on delivery
category: Product
tools:
  - n8n
  - PostHog
  - Loops
fundamentals:
  - n8n-triggers
  - n8n-email-integration
  - n8n-workflow-basics
  - posthog-custom-events
  - posthog-funnels
  - loops-sequences
  - loops-audience
---

# Onboarding Sequence Automation

This drill wires the onboarding email sequence (designed in `onboarding-sequence-design`) into an always-on automation. It connects PostHog product events to Loops email triggers via n8n, so emails fire based on real user behavior — not just time delays.

## Prerequisites

- Onboarding sequence specification from the `onboarding-sequence-design` drill (email content, triggers, timing)
- n8n instance running with Loops and PostHog credentials configured
- PostHog tracking onboarding milestone events
- Loops account with the sequence created (emails loaded, branching configured)

## Steps

### 1. Set up the PostHog-to-Loops event bridge

Using the `n8n-triggers` fundamental, create an n8n workflow with a Webhook trigger. Configure PostHog to send webhook notifications to this endpoint when key onboarding events fire:

- `signup_completed` — triggers sequence enrollment
- `milestone_2_completed` (e.g., `profile_completed`) — updates Loops contact, may skip Email 2
- `milestone_3_completed` (e.g., `first_project_created`) — updates Loops contact
- `activation_reached` — exits the user from the non-activated email branch

For each event, the n8n workflow:
1. Receives the PostHog webhook payload
2. Extracts `distinct_id`, `email`, event name, and event properties
3. Updates the Loops contact properties via API using `n8n-email-integration`
4. Fires a Loops event that advances or branches the sequence

### 2. Build the enrollment workflow

Using `n8n-workflow-basics`, create the enrollment flow:

```
PostHog Webhook (signup_completed)
  → Extract user email, name, signup_source, plan_type
  → POST to Loops /api/v1/contacts/create with properties
  → Loops auto-starts the onboarding sequence (triggered by "Contact created")
  → Log enrollment event back to PostHog: onboarding_email_enrolled
```

Add error handling: if Loops returns a 409 (contact already exists), update the contact instead of failing. If Loops is unreachable, queue the enrollment for retry.

### 3. Build the milestone sync workflow

Create a separate n8n workflow for each milestone event:

```
PostHog Webhook (milestone_N_completed)
  → Extract user email and milestone details
  → PUT to Loops /api/v1/contacts/update with {milestone_N_completed: true, milestone_N_date: timestamp}
  → POST to Loops /api/v1/events/send with {eventName: "milestone_N_completed"}
  → Loops sequence uses this event to branch/skip emails
```

The Loops sequence's conditional branches check these contact properties to decide whether to send or skip each email.

### 4. Build the activation exit workflow

Using `n8n-triggers`, create a workflow that fires on the `activation_reached` PostHog event:

```
PostHog Webhook (activation_reached)
  → Extract user email and activation details
  → PUT to Loops /api/v1/contacts/update with {activation_date: timestamp, activated: true}
  → POST to Loops /api/v1/events/send with {eventName: "activation_reached"}
  → Loops sequence exits the "not activated" branch and sends Email 6 (celebration)
```

### 5. Build the onboarding funnel in PostHog

Using the `posthog-funnels` fundamental, create a funnel that tracks the full journey:

```
onboarding_email_enrolled → email_1_sent → email_1_opened → email_1_clicked
  → milestone_2_completed → milestone_3_completed → activation_reached
```

Add a breakdown by `signup_source` and `plan_type` to identify which user segments convert best through the email sequence. Set the funnel window to 14 days.

Also create a separate funnel for email engagement:
```
email_sent → email_opened → email_clicked → activation_reached
```
Break down by email step (1-7) to identify which emails drive the most activation.

### 6. Track email events in PostHog

Using `posthog-custom-events`, ensure every email interaction is tracked:

- `onboarding_email_sent` with properties: `{email_step: N, subject: "...", user_email: "..."}`
- `onboarding_email_opened` with properties: `{email_step: N}`
- `onboarding_email_clicked` with properties: `{email_step: N, cta_url: "..."}`

If Loops provides webhooks for open/click events, route them through n8n to PostHog. If not, use Loops API to pull metrics daily via a scheduled n8n workflow.

### 7. Set up monitoring alerts

Using `n8n-workflow-basics`, create a daily monitoring workflow:

1. Query PostHog for yesterday's onboarding email metrics: emails sent, opens, clicks, activations
2. Compare to thresholds: open rate < 25% or click rate < 3% triggers an alert
3. Check for errors: failed enrollments, bounced emails, broken webhook connections
4. Send a daily digest to Slack or email with: enrollments, open rate, click rate, activations, and any errors

### 8. Test the full pipeline

Before going live:

1. Create a test user in your app
2. Verify PostHog fires `signup_completed`
3. Verify n8n receives the webhook and enrolls the contact in Loops
4. Verify Email 1 arrives immediately
5. Simulate Milestone 2 completion and verify Email 2 is skipped
6. Simulate no activity for 5 days and verify Emails 3-5 arrive on schedule
7. Simulate activation and verify Email 6 fires and the non-activated branch exits
8. Verify all events appear in the PostHog funnel

Document any issues found during testing and fix before launching to real users.
