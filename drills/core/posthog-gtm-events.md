---
name: posthog-gtm-events
description: Define and implement a standard event taxonomy in PostHog for all GTM motions
category: Analytics
tools:
  - PostHog
fundamentals:
  - posthog-custom-events
  - posthog-funnels
  - posthog-cohorts
---

# PostHog GTM Events

This drill establishes a standard event taxonomy in PostHog that all GTM plays, drills, and tools feed into. Consistent event naming and properties are the foundation for every measurement, threshold, and dashboard you build.

## Prerequisites

- PostHog account with project created
- PostHog tracking snippet installed on your website and product
- Understanding of your GTM motions (marketing, sales, product, etc.)

## Steps

### 1. Define the event naming convention

Establish a naming scheme every drill and play follows:

- **Format**: `object_action` in snake_case (e.g., `email_sent`, `meeting_booked`, `trial_started`)
- **Objects**: lead, contact, deal, email, meeting, campaign, page, feature, subscription
- **Actions**: created, viewed, clicked, sent, opened, replied, booked, started, completed, churned, upgraded

Never use vague names like "event1" or platform-specific names like "instantly_webhook_fire." Events should be tool-agnostic — the same `email_sent` event fires whether you use Instantly or Smartlead.

### 2. Define standard event properties

Using the `posthog-custom-events` fundamental, attach consistent properties to every event:

- **Source**: Which drill or play triggered the event (e.g., "cold-email-sequence", "webinar-pipeline")
- **Channel**: The communication channel (email, linkedin, phone, in-app, ad)
- **Stage**: Where in the funnel this event occurs (awareness, consideration, decision, onboarding, retention)
- **Campaign**: The specific campaign or play instance identifier
- **Level**: The play level if applicable (smoke, baseline, scalable, durable)

Plus event-specific properties: for `email_sent`, include subject line, template ID, and sequence step. For `meeting_booked`, include source channel and prospect tier.

### 3. Implement person properties

Set person properties that accumulate over time:

- `first_touch_channel`: The channel that first brought this person in
- `last_touch_channel`: Most recent interaction channel
- `lead_score`: Current score from the `enrich-and-score` drill
- `lifecycle_stage`: prospect, lead, qualified, customer, churned
- `total_emails_received`, `total_meetings_booked`, etc.

These properties enable cohort analysis and segmentation across all drills.

### 4. Build the core funnels

Using `posthog-funnels`, create standard funnels that every GTM team needs:

- **Acquisition funnel**: page_viewed -> lead_created -> meeting_booked -> deal_created -> deal_won
- **Activation funnel**: trial_started -> onboarding_step_completed (x N) -> activation_reached
- **Expansion funnel**: feature_used -> upgrade_prompt_shown -> upgrade_started -> upgrade_completed
- **Retention funnel**: session_started (weekly) with dropoff tracking over 90 days

### 5. Set up cohort definitions

Using `posthog-cohorts`, create reusable cohorts:

- Active users (session in last 7 days)
- At-risk users (no session in 14+ days, previously active)
- Power users (top 10% by usage volume)
- Churned users (no activity in 30+ days, was previously active)
- Upgrade candidates (approaching plan limits)

These cohorts feed into drills like `churn-prevention`, `upgrade-prompt`, and `winback-campaign`.

### 6. Document and enforce the taxonomy

Create a reference document listing every event, its properties, and which drills fire it. Review the taxonomy monthly. New events must follow the naming convention. Retire events that no one queries. A clean taxonomy is worth more than a comprehensive one — if nobody uses an event, remove it.
