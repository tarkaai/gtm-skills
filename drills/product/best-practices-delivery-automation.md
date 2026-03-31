---
name: best-practices-delivery-automation
description: Automate contextual delivery of best-practices cards via Intercom in-app messages and Loops emails based on user behavior signals
category: Product
tools:
  - Intercom
  - Loops
  - PostHog
  - n8n
fundamentals:
  - intercom-in-app-messages
  - loops-sequences
  - posthog-cohorts
  - posthog-feature-flags
  - n8n-scheduling
  - n8n-triggers
---

# Best Practices Delivery Automation

This drill builds always-on automation that delivers best-practices content cards to users at the exact moment they would benefit. Instead of blasting tips to everyone, it uses PostHog behavioral signals to match each user with the right tip at the right time.

## Input

- Best-practices content cards from the `best-practices-content-pipeline` drill (with `trigger_event` and `exclude_event` per card)
- PostHog tracking configured for the trigger and exclude events
- Intercom configured for in-app messaging
- Loops configured for automated email sequences
- n8n instance for orchestration

## Steps

### 1. Build behavioral trigger rules

For each content card, configure the delivery logic using `posthog-cohorts`:

**Eligibility cohort per card:**
- User has fired the card's `trigger_event` in the last 7 days (they are doing the task the slow/suboptimal way)
- User has NOT fired the card's `exclude_event` ever (they do not already follow this practice)
- User has NOT been shown this specific card in the last 30 days (frequency cap)
- User signed up more than 3 days ago (do not overwhelm new users with tips during onboarding)

Create a PostHog cohort for each card's eligibility criteria. Name it: `bp-eligible-{card_id}`.

### 2. Configure in-app delivery via Intercom

Using the `intercom-in-app-messages` fundamental, create an in-app message for each content card:

- **Format:** Tooltip or banner, not modal. Best practices should enhance the experience, not interrupt it.
- **Content:** Card title as headline, card hook as body, CTA button with the `cta_label`, deep link to the relevant product screen.
- **Targeting:** Users in the `bp-eligible-{card_id}` cohort (sync PostHog cohorts to Intercom via n8n or the PostHog-Intercom integration).
- **Frequency:** Maximum 1 best-practice tip per user per day. Maximum 3 per user per week. This prevents tip fatigue.
- **Placement:** Contextual — the tip appears on or near the screen where the user performs the suboptimal behavior. If the card is about a shortcut in the editor, the tooltip appears in the editor, not on the dashboard.

Priority order: deliver higher-retention-lift cards first. If a user is eligible for multiple cards, show the one with the highest `retention_lift` value.

### 3. Configure email delivery via Loops

Using the `loops-sequences` fundamental, create a "Best Practices Digest" email sequence as a fallback for users who did not engage with the in-app message:

- **Trigger:** User was shown an in-app tip 48+ hours ago but did not click it (fire `best_practice_shown` but no `best_practice_clicked` within 48h).
- **Email content:** The full card content — title, body, steps, and CTA deep link. Subject line: the card's `hook` text (under 80 characters, benefit-led).
- **Cadence:** Maximum 1 best-practices email per user per week. Bundle up to 2 tips per email if the user has multiple pending.
- **Unsubscribe:** Best-practices emails have their own preference category in Loops. Users can opt out of tips without unsubscribing from transactional emails.

### 4. Build the orchestration workflow in n8n

Using `n8n-scheduling` and `n8n-triggers`, create a daily workflow:

1. **Query eligible users:** For each card, query PostHog for users in the `bp-eligible-{card_id}` cohort who have not been shown this card.
2. **Apply frequency caps:** Filter out users who received any best-practice tip in the last 24 hours (in-app) or 7 days (email).
3. **Rank and assign:** For each eligible user, select the card with the highest retention lift they have not yet seen.
4. **Trigger delivery:** Push the user-card assignment to Intercom (for in-app) or Loops (for email fallback).
5. **Log delivery:** Fire `best_practice_shown` in PostHog with the card ID, surface, and timestamp.

The workflow runs at 09:00 UTC daily to queue up the day's tip deliveries.

### 5. Monitor delivery health

Set up n8n alerts for:
- **Low delivery rate:** If fewer than 10% of eligible users receive a tip in any given week, the cohort definitions may be too restrictive.
- **High dismissal rate:** If any card's dismissal rate exceeds 50%, pause it and rewrite the copy or adjust the trigger criteria.
- **Decreasing completion rate:** If the overall `best_practice_completed` rate drops below 10% for 2 consecutive weeks, review whether the tips are still relevant to the user base.
- **Cohort exhaustion:** If an eligibility cohort shrinks below 50 users, the card has reached most of its audience. Retire it and replace with a new card from the pipeline.

### 6. Track engagement in the CRM

Log each best-practice interaction in Attio as a note on the user's contact record:
- Which tips they saw, clicked, completed, or dismissed
- Total tips completed (cumulative engagement score)
- Whether the user's retention improved after completing tips (compare 30-day retention before vs. after first tip completion)

This data feeds into churn prediction models and customer health scoring.

## Output

- Always-on delivery system matching users to contextual tips via Intercom and Loops
- Frequency-capped orchestration workflow in n8n running daily
- Monitoring and alerting for delivery health
- CRM-integrated engagement tracking per user

## Triggers

Set up once at Baseline level. The orchestration workflow runs daily via n8n cron. Review delivery health weekly. Update card eligibility cohorts when the product ships changes that affect trigger or exclude events.
