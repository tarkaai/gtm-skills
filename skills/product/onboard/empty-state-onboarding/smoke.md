---
name: empty-state-onboarding-smoke
description: >
  Empty State Guidance — Smoke Test. Audit product empty states, design contextual CTAs with
  sample data and templates for the highest-priority surface, and validate that users click
  through at 40%+ in a small test group.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=40% empty state CTR on the primary P0 surface across 20+ users"
kpis: ["Empty state CTR", "CTA click-to-creation rate", "Time from empty state view to first item created"]
slug: "empty-state-onboarding"
install: "npx gtm-skills add product/onboard/empty-state-onboarding"
drills:
  - empty-state-design
  - posthog-gtm-events
  - threshold-engine
---

# Empty State Guidance — Smoke Test

> **Stage:** Product > Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

A single P0 empty state surface has been redesigned with a contextual CTA, sample data or templates, and full PostHog tracking. At least 20 users have seen the new empty state and 40%+ clicked the CTA. You have baseline data on which CTA copy, template, or sample data drove the most first-item creations.

## Leading Indicators

- `empty_state_viewed` events are flowing in PostHog within 1 hour of deploying the new design
- Users who click the CTA create their first item within 5 minutes (low friction confirmation)
- No users report confusion or file support tickets about the new empty state
- Session recordings show users scanning the empty state and clicking the CTA without hesitation

## Instructions

### 1. Set up event tracking

Run the `posthog-gtm-events` drill to define the empty state event taxonomy. At minimum, instrument these events in your product code:

- `empty_state_viewed` with properties: `surface`, `priority`, `user_signup_age_hours`
- `empty_state_cta_clicked` with properties: `surface`, `cta_text`
- `first_item_created` with properties: `surface`, `creation_method` (from_scratch / from_template)

Verify events are flowing by checking PostHog Live Events after deploying to staging.

### 2. Audit and design the primary empty state

Run the `empty-state-design` drill. Focus exclusively on the single highest-priority empty state surface — the one on the direct path to your product's activation metric.

Specifically:
1. Watch 10-20 new user session recordings in PostHog to identify which empty state users hit first and where they stall
2. Pick the P0 surface that the most users encounter before activating
3. Design the empty state with: contextual headline, 2-3 templates OR sample data, one specific CTA button, and a secondary help link
4. Implement the design and deploy behind a PostHog feature flag so you can control rollout

**Human action required:** Review the empty state design before deploying. Verify the CTA copy is specific ("Create your first project" not "Get started"), the templates are relevant to your target user, and the help link goes to useful content. Deploy to 20-50 users via the PostHog feature flag.

### 3. Observe behavior for 7 days

Let the test group use the product for 7 days. Do not change anything during this period. Monitor PostHog daily:
- Are `empty_state_viewed` events firing? If zero events, the feature flag or tracking is broken — fix immediately.
- Are `empty_state_cta_clicked` events following views? If yes, the design is working.
- Are `first_item_created` events following clicks? If clicks are high but creations are low, the creation flow after the CTA has friction.

Watch 5 session recordings of users who saw the empty state but did NOT click the CTA. Note what they did instead — did they navigate away, try a different path, or appear confused?

### 4. Evaluate against threshold

Run the `threshold-engine` drill. Compute:
- **Empty state CTR:** `empty_state_cta_clicked / empty_state_viewed` for the P0 surface
- **Click-to-creation rate:** `first_item_created / empty_state_cta_clicked`
- **Threshold:** CTR >= 40%

If PASS (CTR >= 40%): Document the winning design, the CTR, and the click-to-creation rate. Proceed to Baseline.

If FAIL (CTR < 40%): Diagnose from session recordings. Common fixes:
- CTA copy is too vague — make it more specific
- Templates are not relevant to the user's use case — change them
- Empty state is below the fold — move the CTA higher
- Users do not understand what the feature does — add a one-sentence explanation
Iterate and re-test with another 20-user cohort. You can run up to 3 iterations within the Smoke week.

## Time Estimate

- 1 hour: Set up PostHog event tracking
- 2 hours: Audit empty states, design the P0 surface, implement and deploy
- 1 hour: Monitor and watch session recordings during the week
- 1 hour: Evaluate threshold and document results

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, session recordings, feature flags | Free tier: 1M events + 5K recordings/mo. [posthog.com/pricing](https://posthog.com/pricing) |

**Estimated play-specific cost at this level:** $0 (free tier sufficient for 20-50 users)

## Drills Referenced

- `empty-state-design` — audit empty states, design the P0 surface with CTA, templates, and tracking
- `posthog-gtm-events` — define the event taxonomy for empty state tracking
- `threshold-engine` — evaluate the 40% CTR pass/fail threshold
