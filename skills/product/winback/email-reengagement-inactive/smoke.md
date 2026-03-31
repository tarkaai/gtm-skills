---
name: email-reengagement-inactive-smoke
description: >
  Inactive User Re-engagement — Smoke Test. Send a single reengagement email to
  a small batch of inactive users to prove that personalized outreach can drive
  returns. No automation, no always-on. Agent prepares, human approves send.
stage: "Product > Winback"
motion: "LeadCaptureSurface"
channels: "Email, Product"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: ">=15% of recipients log back in within 7 days"
kpis: ["Email open rate", "Click-through rate", "7-day return rate"]
slug: "email-reengagement-inactive"
install: "npx gtm-skills add product/winback/email-reengagement-inactive"
drills:
  - onboarding-sequence-design
  - threshold-engine
---

# Inactive User Re-engagement — Smoke Test

> **Stage:** Product > Winback | **Motion:** LeadCaptureSurface | **Channels:** Email, Product

## Outcomes

At least 15% of the targeted inactive users log back into the product within 7 days of receiving the reengagement email. This proves that personalized email outreach can recover inactive users before investing in automation.

## Leading Indicators

- Email open rate above 30% (signals subject line relevance)
- Click-through rate above 5% (signals CTA and content resonance)
- At least 1 user completes a meaningful product action after returning (not just login)

## Instructions

### 1. Identify the inactive cohort

Query PostHog for users who have not logged in for 14-30 days but were previously active (at least 3 sessions in the 30 days before going inactive). Use the `posthog-cohorts` fundamental directly. Export the list to a CSV: `user_id`, `email`, `last_active_date`, `total_sessions_before_inactive`, `most_used_feature`. Cap the list at 50 users for this smoke test.

### 2. Design the reengagement email

Run the `onboarding-sequence-design` drill to create a single reengagement email (not a full sequence yet). The email must include:

- **Subject line:** Reference something specific about their usage. Example pattern: "Your [most_used_feature] data is still here" or "[Product] shipped [recent_feature] since you left."
- **Body:** Three sections: (a) acknowledge their absence without guilt-tripping, (b) highlight 1-2 product changes or improvements since their last login, (c) a single clear CTA that links directly to their most-used feature (not the homepage).
- **Personalization variables:** `{{firstName}}`, `{{most_used_feature}}`, `{{days_inactive}}`.

Do NOT include discounts or incentives at Smoke level. Test whether product value alone drives returns.

### 3. Send the email via Loops

Using the `loops-audience` fundamental, create a contact property `reengagement_cohort = "smoke_test_1"` and tag the 50 users. Using `loops-broadcasts`, send the email as a one-time broadcast to this segment.

**Human action required:** Review the email copy, subject line, and recipient list before approving the send. Verify that no currently-active users are in the list. Approve or request changes.

### 4. Track returns in PostHog

Using `posthog-custom-events`, fire the following events:
- `reengagement_email_sent` — when Loops confirms delivery (via n8n webhook or Loops webhook)
- `reengagement_user_returned` — when a user from the cohort logs in (match on user_id)
- `reengagement_user_reactivated` — when a returned user completes a meaningful action (define this as any core product event within 7 days of return)

Build a PostHog funnel: `reengagement_email_sent` -> `reengagement_user_returned` -> `reengagement_user_reactivated` with a 7-day conversion window.

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 7 days. Measure:
- Primary: return rate (users who logged in / emails delivered). Pass threshold: >=15%.
- Secondary: open rate (target >30%), click rate (target >5%), reactivation rate (any returned user who completed a core action).

If PASS: document which subject line, CTA, and personalization variables performed best. Proceed to Baseline.
If FAIL: examine the funnel. If open rate was low, test a different subject line on a fresh batch of 50. If open rate was fine but click rate was low, revise the CTA and body. Re-run Smoke with the revised email.

## Time Estimate

- 1 hour: Query PostHog for inactive users, build the cohort, export list
- 1 hour: Design the email using the onboarding-sequence-design drill
- 0.5 hours: Configure Loops broadcast and event tracking
- 0.5 hours: Human review and send approval
- 1 hour (after 7 days): Pull results, run threshold-engine, document findings

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohort identification, event tracking, funnel analysis | Free up to 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Send reengagement broadcast email | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost:** $0 (within free tiers for 50 users)

## Drills Referenced

- `onboarding-sequence-design` — design the reengagement email content, subject line, and personalization strategy
- `threshold-engine` — evaluate 7-day return rate against the >=15% pass threshold and recommend next action
