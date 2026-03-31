---
name: add-on-discovery-smoke
description: >
  Module Cross-Sell — Smoke Test. Build one contextual add-on discovery surface for your
  highest-value module and validate that users engage when shown the right add-on at the
  right moment.
stage: "Product > Upsell"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥15% click-through on add-on discovery surface shown to triggered users"
kpis: ["Add-on discovery CTR", "Add-on activation rate", "Trigger accuracy"]
slug: "add-on-discovery"
install: "npx gtm-skills add product/upsell/add-on-discovery"
drills:
  - addon-discovery-surface-build
  - threshold-engine
---

# Module Cross-Sell — Smoke Test

> **Stage:** Product → Upsell | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

One in-product add-on discovery surface is live, targeted at users whose behavior indicates readiness. At least 15% of users who see the surface click through to learn more about the add-on. This validates that contextual, behavior-triggered discovery works better than static upsell banners.

## Leading Indicators

- Users who trigger the behavior threshold receive the discovery surface within 24 hours
- Dismissal rate stays below 40% (the surface feels relevant, not spammy)
- At least 1 user who clicked through completes add-on activation during the test window

## Instructions

### 1. Choose your highest-value add-on

Pick the single add-on with the highest revenue potential and the clearest usage trigger. You need an add-on where you can identify — from PostHog data — what behavior signals that a user would benefit from it. If you have multiple candidates, choose the one with the most historical adoption data to validate your trigger hypothesis.

### 2. Build the discovery surface

Run the `addon-discovery-surface-build` drill, but scope it to ONE add-on and ONE surface type (tooltip or banner). Specifically:

- Complete Step 1 (map the trigger behavior for this one add-on)
- Complete Step 2 (instrument the four PostHog events: `addon_discovery_impression`, `addon_discovery_clicked`, `addon_activation_started`, `addon_activated`)
- Complete Step 3 (build one contextual surface — use a tooltip if the trigger happens in a specific UI location, or a banner if the trigger is a cumulative behavior)
- Skip Steps 4-5 (no n8n automation or sales routing at Smoke level)
- Complete Step 6 (implement basic fatigue controls: suppress after 2 dismissals)

**Human action required:** Review the surface copy and placement before enabling. Verify the tooltip or banner appears at the right moment by triggering the behavior yourself. Confirm PostHog events fire correctly in Live Events. Enable the surface for a test group of 20-50 users who match the trigger criteria.

### 3. Observe for 5-7 days

Monitor PostHog daily:
- How many users saw the surface (impressions)?
- How many clicked through (CTR)?
- How many dismissed it?
- Did any user complete add-on activation?

Do not change the surface during the observation window. If the surface is completely broken (zero impressions, events not firing), fix the technical issue and restart the clock.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure: ≥15% click-through rate on the add-on discovery surface among triggered users (impressions that resulted in clicks). If PASS, proceed to Baseline. If FAIL, diagnose:
- CTR below 5%: the surface copy or placement is wrong — users see it but ignore it. Rewrite the copy to be more specific to their behavior.
- CTR 5-14%: the concept works but needs refinement. Test a different surface type or adjust the trigger threshold (maybe you are showing it too early or too late).
- Dismissal rate above 60%: the trigger is inaccurate — you are showing the add-on to users who do not need it. Tighten the cohort criteria.

## Time Estimate

- 2 hours: Analyze PostHog data to identify trigger behavior and build cohort
- 1.5 hours: Build the discovery surface (Intercom in-app message or product tour)
- 0.5 hours: Instrument PostHog events and verify they fire
- 1 hour: Monitor results over the week and compile evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Usage tracking, cohorts, event capture | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app message or product tour surface | Included in existing plan — https://www.intercom.com/pricing |

## Drills Referenced

- `addon-discovery-surface-build` — builds the in-product surface that shows users the add-on at the trigger moment
- `threshold-engine` — evaluates whether CTR hit the 15% pass threshold
