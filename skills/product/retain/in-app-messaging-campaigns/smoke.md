---
name: in-app-messaging-campaigns-smoke
description: >
  Behavioral In-App Messages — Smoke Test. Configure one behavior-triggered in-app message
  in Intercom, target a single user segment via PostHog cohort, and validate that behavioral
  triggers produce higher engagement than time-based messaging.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥35% CTR on the behavior-triggered message"
kpis: ["Message CTR", "Message-to-action conversion rate", "Dismissal rate"]
slug: "in-app-messaging-campaigns"
install: "npx gtm-skills add product/retain/in-app-messaging-campaigns"
drills:
  - posthog-gtm-events
  - feature-announcement
  - threshold-engine
---

# Behavioral In-App Messages — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A single behavior-triggered in-app message achieves 35% or more CTR within 7 days. This proves that targeting messages based on what users just did (behavioral trigger) produces meaningfully higher engagement than broadcasting to everyone or using time-based triggers. "CTR" means the user clicked the message CTA divided by users who saw the message.

## Leading Indicators

- Message delivery rate (delivered / eligible users) — target >90%
- Message visibility rate (seen / delivered) — target >70%, validates placement
- Time from trigger event to message delivery — should be <5 seconds for behavioral relevance
- Dismissal rate — target <25%, high dismissal means wrong timing or wrong audience

## Instructions

### 1. Instrument the behavioral events

Run the `posthog-gtm-events` drill to set up the event taxonomy for this play. Define these PostHog events:

- `in_app_msg_delivered` — message rendered in the user's browser
- `in_app_msg_seen` — message was in viewport for 2+ seconds
- `in_app_msg_clicked` — user clicked the CTA
- `in_app_msg_dismissed` — user closed the message
- `in_app_msg_converted` — user completed the target action within 24 hours

Properties on every event: `message_id`, `trigger_type` (behavioral, time-based), `trigger_event` (the user action that fired the trigger), `segment`.

Also define the behavioral trigger event itself. Pick one high-signal user action that indicates the user is in a moment of need. Good triggers:

- User completes a core workflow but has never used a related advanced feature
- User hits an error or dead-end in the product
- User visits the same help page 2+ times in a session
- User reaches 80% of a plan limit (seats, storage, API calls)

The trigger must be an action the user just took, not a calendar event or time since signup.

### 2. Build and deliver the behavior-triggered message

Run the `feature-announcement` drill, but instead of announcing a feature launch, configure it for a single behavioral trigger. Create one Intercom in-app message with these specifications:

**Targeting:** Build a PostHog cohort of users who performed the trigger event AND have not previously seen this message. Sync the cohort to Intercom via the Intercom user properties API.

**Message content:**
- Format: banner or tooltip (not modal — modals interrupt flow and inflate dismissal rates)
- Copy: under 40 words. Lead with what the user can do right now, not what you built. Reference the action they just took for contextual relevance.
- CTA: single button linking directly to the feature or action. No "Learn more" — go straight to the thing.
- Dismiss: always include a close button. Never force engagement.

**Trigger configuration:** Set the message to display within 3 seconds of the trigger event firing. Behavioral messages lose relevance with delay.

**Human action required:** Review the message copy, targeting logic, and trigger event before activating. Verify the deep link in the CTA works. Activate for 30-50 users from the target segment.

### 3. Monitor for 7 days

Check PostHog daily:
- How many users triggered the behavioral event
- How many were delivered the message (delivery rate)
- How many saw the message (visibility rate) — if low, the placement is wrong
- How many clicked the CTA (engagement rate)
- How many dismissed without clicking (fatigue signal)
- How many completed the target action within 24 hours (conversion)

If delivery rate is below 80% by day 3, check the cohort sync between PostHog and Intercom. If visibility rate is below 50%, move the message to a more prominent placement. Do not change the copy or targeting mid-test.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: 35% CTR (clicked / seen).

- **Pass (>=35%):** Behavioral triggering works for this audience and action. Proceed to Baseline to automate across multiple triggers and segments.
- **Fail (<35%):** Diagnose the funnel. If delivery is low, fix the sync. If visibility is low, fix placement. If visibility is high but clicks are low, the copy or CTA is not compelling — rewrite and re-run. If clicks are high but conversion is low, the feature itself has a UX problem that messaging cannot fix.

## Time Estimate

- 1 hour: Event taxonomy definition, trigger event selection, PostHog cohort creation
- 1.5 hours: Intercom message setup, targeting configuration, CTA deep link
- 0.5 hours: Human review and activation
- 1 hour: Daily monitoring over 7 days (10 minutes/day)
- 1 hour: Final analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Behavioral event tracking, cohort creation, funnel analysis | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app message delivery with behavioral targeting | Essential $29/seat/mo, Advanced $85/seat/mo — https://www.intercom.com/pricing |

**Play-specific cost:** Free if under PostHog free tier limits. Intercom cost is part of existing stack.

## Drills Referenced

- `posthog-gtm-events` — define the event taxonomy for behavioral message tracking
- `feature-announcement` — build and deliver the targeted in-app message via Intercom
- `threshold-engine` — evaluate 7-day CTR against the 35% pass threshold
