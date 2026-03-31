---
name: usage-milestones-smoke
description: >
  Usage Milestone Celebrations — Smoke Test. Define a milestone ladder, instrument detection in PostHog,
  build a minimal in-app celebration for the first milestone tier, and validate that at least 60% of
  users who reach the threshold see the celebration message.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥60% of users who hit a milestone see the celebration message"
kpis: ["Milestone reach rate", "Celebration impression rate", "Post-celebration session count"]
slug: "usage-milestones"
install: "npx gtm-skills add product/retain/usage-milestones"
drills:
  - usage-milestone-rewards
  - threshold-engine
---

# Usage Milestone Celebrations — Smoke Test

> **Stage:** Product → Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

60% or more of users who cross a milestone threshold see the celebration message within their current or next session. This proves the detection-to-display pipeline works end to end before investing in polish or automation.

## Leading Indicators

- PostHog `milestone_reached` events are firing correctly with the right threshold values
- Intercom in-app messages are rendering in the correct context (right page, right timing)
- Users who see the celebration have a higher same-session action count than their pre-milestone average

## Instructions

### 1. Define the milestone ladder

Run the `usage-milestone-rewards` drill, Step 1. Choose 3-5 milestone thresholds tied to your product's core action. Example: 1 project created, 10 projects, 50 projects, 100 projects. Each threshold must be a cumulative count stored as a PostHog person property.

**Human action required:** Decide which product action defines a milestone. This must be the action most correlated with retention in your product. If unsure, query PostHog for the action that best predicts 30-day retention.

### 2. Instrument milestone detection

Run the `usage-milestone-rewards` drill, Step 2. Using the `posthog-custom-events` fundamental, add tracking:

- `milestone_reached` — fires once per user per threshold. Properties: `milestone_tier` (integer), `milestone_name` (string), `cumulative_count` (integer).
- `celebration_shown` — fires when the in-app message renders. Properties: `milestone_tier`, `celebration_type` (string: "confetti", "badge", "toast").
- `celebration_engaged` — fires when the user interacts with the celebration (clicks CTA, shares, etc.). Properties: `milestone_tier`, `cta_type`.

Set PostHog person properties: `highest_milestone_tier`, `milestones_reached_list`, `last_milestone_date`. Ensure each milestone fires only once per user by checking the person property before emitting.

### 3. Build the first celebration

Run the `usage-milestone-rewards` drill, Step 3 (early milestones only). Using the `intercom-in-app-messages` fundamental, create a single in-app message for the first milestone tier:

- Trigger: PostHog person property `highest_milestone_tier` = 1 AND `celebration_shown` event NOT yet fired for tier 1
- Message: congratulatory copy under 40 words. Lead with the user's achievement, not the product. Example: "You just created your 10th project. Most users never get past 3 — you are building something real."
- CTA: link to the next logical feature the user should try. No upgrade ask at this stage.
- Display: show once, dismiss on click or after 10 seconds

Use a PostHog feature flag to gate the celebration to a test group of 10-50 users.

### 4. Validate detection accuracy

Manually trigger the core action enough times to cross the first milestone threshold on a test account. Verify in PostHog:
- `milestone_reached` event fired with correct properties
- Person property `highest_milestone_tier` updated to 1
- Intercom in-app message triggered within the same session
- `celebration_shown` event fired

If any step fails, debug the event pipeline before proceeding.

### 5. Run for 1 week and measure

Enable the feature flag for the test group. After 7 days, run the `threshold-engine` drill to evaluate:

- **Primary metric:** Of users who fired `milestone_reached` for tier 1, what percentage also fired `celebration_shown`? Target: >=60%.
- **Secondary metric:** Of users who fired `celebration_shown`, what percentage fired `celebration_engaged`? Record but do not gate on this.
- **Leading indicator:** Compare average session count in the 7 days after milestone for celebrated vs. uncelebrated users (those who reached the milestone before the flag was enabled).

### 6. Pass/fail decision

If >=60% of milestone-reaching users saw the celebration: **PASS**. Document the impression rate, engagement rate, and any session count lift. Proceed to Baseline.

If <60%: diagnose. Common causes: (a) Intercom targeting rule mismatch — verify the PostHog-to-Intercom property sync, (b) message display timing — user left the session before the message rendered, (c) milestone event not firing — check the cumulative count logic. Fix and re-run for another week.

## Time Estimate

- 1 hour: define milestone ladder and choose thresholds
- 1.5 hours: instrument PostHog events and person properties
- 1 hour: build Intercom in-app celebration message
- 0.5 hours: validate on test account
- 1 hour: analyze results after 7 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, person properties, feature flags | Free tier: 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app celebration messages | Starter: $74/mo — https://www.intercom.com/pricing |

## Drills Referenced

- `usage-milestone-rewards` — defines the milestone ladder, instruments detection, and builds the celebration notification pipeline
- `threshold-engine` — evaluates the 60% impression rate threshold and generates pass/fail verdict
