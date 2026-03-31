---
name: workflow-suggestion-delivery
description: Deliver AI-generated workflow optimization suggestions via in-app messages and email with timing and acceptance tracking
category: Enablement
tools:
  - Intercom
  - PostHog
  - Loops
  - n8n
fundamentals:
  - intercom-in-app-messages
  - intercom-bots
  - posthog-feature-flags
  - posthog-custom-events
  - loops-transactional
  - n8n-triggers
  - n8n-workflow-basics
---

# Workflow Suggestion Delivery

This drill takes validated workflow optimization suggestions (from `workflow-behavior-analysis`) and delivers them to users through the right channel at the right moment. It handles in-app delivery via Intercom, email fallback via Loops, delivery timing, and acceptance tracking in PostHog.

## Input

- Validated suggestion queue from the `workflow-behavior-analysis` drill (per-user or per-segment)
- Intercom configured with in-app messaging
- PostHog with feature flags enabled
- Loops configured for triggered transactional emails
- n8n instance for orchestration

## Steps

### 1. Design the suggestion UI pattern

Choose the delivery format based on suggestion category:

- **Efficiency suggestions** (shortcuts, faster paths): Intercom tooltip pointing at the relevant UI element. Triggered when the user starts the workflow the suggestion targets. Example: user clicks Menu > Search for the 3rd time in a session, tooltip appears: "Try Cmd+K for instant search — 3x faster."

- **Discovery suggestions** (unused features): Intercom in-app post shown on next login. Non-blocking, dismissible. Example: "You export data manually every week. Did you know you can schedule automatic exports? Set it up in 2 minutes."

- **Automation suggestions** (repeated manual patterns): Intercom Custom Bot that walks the user through setting up the automation. Triggered when the user begins the repetitive sequence. Example: "You've done this sequence 12 times this month. Want to automate it? I'll walk you through it."

### 2. Build the delivery orchestration workflow

Using `n8n-workflow-basics`, create the suggestion delivery pipeline:

1. **Trigger**: n8n cron runs daily (or on-demand after suggestion generation)
2. **Fetch**: Pull the suggestion queue — users with pending suggestions
3. **Filter**: Exclude users who:
   - Received a suggestion in the last 7 days (prevent fatigue)
   - Dismissed 3+ suggestions without acting (reduce to 1 suggestion per month)
   - Are currently in an onboarding flow (do not compete for attention)
   - Have a churn risk score > 70 (different intervention needed)
4. **Route**: For each eligible user, select the delivery channel:
   - If the user logged in within the last 24 hours → in-app via Intercom
   - If the user has not logged in for 3+ days → email via Loops
   - If the suggestion requires a walkthrough → Intercom Custom Bot
5. **Deliver**: Send via the selected channel using the appropriate fundamental
6. **Log**: Record `suggestion_delivered` event in PostHog with properties: `{user_id, suggestion_id, suggestion_category, delivery_channel, suggestion_text}`

### 3. Configure Intercom in-app delivery

Using `intercom-in-app-messages`, create message templates for each suggestion category:

**Tooltip template** (efficiency):
- Trigger: user performs the inefficient action
- Content: 1 sentence describing the better way + benefit
- CTA: "Try it now" (deep links to the feature)
- Display: show once per suggestion, do not repeat if dismissed

**Post template** (discovery):
- Trigger: next session start
- Content: feature name, 1-sentence benefit, "How [similar role] uses it" social proof
- CTA: "Show me" (opens the feature)
- Display: show once, auto-dismiss after 30 seconds

**Bot template** (automation):
- Trigger: user starts the repetitive sequence
- Content: "I noticed you do [X] frequently. Want me to help automate it?"
- Flow: Yes → 3-step guided setup; No → log dismissal, do not re-trigger for 30 days

### 4. Configure email fallback delivery

Using `loops-transactional`, create a suggestion email template:

- Subject: "A faster way to [workflow name]"
- Body: personalized suggestion with quantified benefit, step-by-step instructions, deep link to the feature in-app
- From: product team (not marketing)
- Send only if the user has not seen the in-app version (check PostHog for `suggestion_delivered` with `delivery_channel: in_app`)

### 5. Track suggestion acceptance and impact

Using `posthog-custom-events`, track the full suggestion lifecycle:

```
suggestion_delivered    → {suggestion_id, category, channel}
suggestion_viewed       → {suggestion_id, view_duration_seconds}
suggestion_clicked      → {suggestion_id, cta_type}
suggestion_adopted      → {suggestion_id, adopted_within_days}
suggestion_dismissed    → {suggestion_id, reason (if provided)}
```

Define adoption: the user performs the suggested action within 7 days of delivery. Track whether adopted suggestions lead to sustained behavior change (user continues using the suggested approach for 30+ days).

### 6. Build the delivery performance funnel

Using `posthog-custom-events`, create a funnel:

```
suggestion_delivered → suggestion_viewed → suggestion_clicked → suggestion_adopted
```

Break down by: suggestion category, delivery channel, and user segment. Target conversion rates:
- Delivered → Viewed: 70%+ (in-app), 25%+ (email)
- Viewed → Clicked: 30%+ (in-app), 15%+ (email)
- Clicked → Adopted: 40%+
- Overall Delivered → Adopted: 8%+ (email), 20%+ (in-app)

If a suggestion category consistently underperforms, revise the copy or targeting. If a channel underperforms, shift volume to the better-performing channel.

## Output

- Suggestion delivery pipeline in n8n (daily orchestration)
- 3 Intercom message templates (tooltip, post, bot) for in-app delivery
- 1 Loops email template for email fallback
- PostHog event tracking for the full suggestion lifecycle
- Delivery performance funnel in PostHog

## Triggers

The delivery pipeline runs daily via n8n cron. Review delivery performance weekly. Adjust channel routing and fatigue rules monthly based on acceptance data.
