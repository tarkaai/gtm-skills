---
name: progressive-feature-reveal-smoke
description: >
  Progressive Feature Discovery — Smoke Test. Map product features into readiness
  tiers, instrument tracking, gate one feature behind a behavioral signal, and
  validate that users who unlock it adopt it at ≥35% within 14 days.
stage: "Product > Onboard"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: "≥35% of users who unlock an Intermediate feature use it within 14 days"
kpis: ["Unlock rate", "Post-unlock adoption rate", "Time to first unlock"]
slug: "progressive-feature-reveal"
install: "npx gtm-skills add product/onboard/progressive-feature-reveal"
drills:
  - feature-readiness-gating
  - posthog-gtm-events
  - threshold-engine
---

# Progressive Feature Discovery — Smoke Test

> **Stage:** Product → Onboard | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

≥35% of users who unlock an Intermediate-tier feature actually use it within 14 days. This proves the readiness-gating mechanic works: users who are told "you've earned this" engage with the feature, rather than ignoring it like they would in a feature dump.

## Leading Indicators

- Users completing Core actions at a rate that triggers the unlock criteria (proves the criteria are reachable)
- Users clicking on the unlock celebration message (proves the reveal moment gets attention)
- Time-to-unlock under 5 days for 50%+ of active users (proves the bar is not set too high)

## Instructions

### 1. Map features to readiness tiers

Run the `feature-readiness-gating` drill, Step 1 only. Categorize your product features into Core, Intermediate, Advanced, and Power tiers. For the Smoke test, pick ONE Intermediate feature to gate. Choose a feature that: (a) existing users already adopt at a measurable rate, so you have a baseline to compare against, and (b) has a clear prerequisite — users need to understand X before Y makes sense.

Document the tier map in a markdown file in your repo. Example:

```
Core: create-project, add-task, invite-member
Intermediate: templates, bulk-actions, basic-integrations  <-- gate "templates"
Advanced: automation-rules, custom-fields, api-access
Power: webhooks, custom-scripts, admin-controls
```

### 2. Define the readiness signal

Choose the specific behavioral signal that unlocks the gated feature. The signal must be: observable via PostHog events, achievable within the first 3-5 sessions, and causally related to the feature being unlocked (the user has done the prerequisite work).

Example: "Created 3+ projects AND added at least 1 task to each" unlocks Templates.

### 3. Instrument tracking events

Run the `posthog-gtm-events` drill scoped to feature readiness. Implement these PostHog events:

| Event | When it fires | Properties |
|-------|--------------|------------|
| `core_action_completed` | User completes a Core-tier action | `action`, `count`, `session_number` |
| `feature_tier_unlocked` | User meets the readiness criteria | `tier`, `trigger_action`, `time_to_unlock_hours` |
| `feature_first_used` | User uses the newly unlocked feature for the first time | `feature`, `tier`, `hours_since_unlock` |

### 4. Gate the feature

Run the `feature-readiness-gating` drill, Steps 2-5 for ONE feature only. Create a PostHog feature flag `tier-intermediate-templates` (or your equivalent) that is cohort-gated to users who have met the readiness criteria. In your product code, check the flag before rendering the feature. Show a locked/teased state for users who have not unlocked it yet.

**Human action required:** Deploy the feature flag check and locked-state UI to your product. This requires a code change — the agent prepares the PostHog flag and Intercom messages, but a developer must ship the product-side implementation.

### 5. Build the unlock moment

Configure an Intercom in-app message that fires when `feature_tier_unlocked` is captured. The message should: congratulate the user, name the feature they just unlocked, and link directly to it. Keep it to 2 sentences and one CTA button.

### 6. Launch to a small cohort

Enable the feature flag for 10-50 new signups. Do NOT apply it to existing users (they already discovered features organically — the test is only valid for new users experiencing the gated flow).

### 7. Evaluate against threshold

Run the `threshold-engine` drill after 14 days. Query PostHog:

- Count users who triggered `feature_tier_unlocked` (denominator)
- Count users who triggered `feature_first_used` within 14 days of unlock (numerator)
- Calculate adoption rate: numerator / denominator

**Pass:** ≥35% adoption rate. Proceed to Baseline.
**Fail:** Investigate — did users not unlock (criteria too hard), unlock but not notice (reveal moment too subtle), or notice but not use (feature not compelling)? Adjust and re-run.

## Time Estimate

- 1 hour: feature tier mapping and readiness signal definition
- 2 hours: PostHog event instrumentation and feature flag setup
- 1 hour: Intercom unlock message configuration
- 1 hour: testing end-to-end flow (locked state → unlock → reveal → usage)
- 1 hour: threshold evaluation after 14 days

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| [PostHog](https://posthog.com/pricing) | Feature flags, event tracking, cohorts | Free tier: 1M events/mo, 1M flag requests/mo |
| [Intercom](https://www.intercom.com/pricing) | Unlock celebration messages | Essential: $29/seat/mo; Proactive Support Plus add-on: $99/mo for 500 messages |

**Estimated play-specific cost:** Free (PostHog free tier covers 10-50 user test; Intercom Essential plan if already installed)

## Drills Referenced

- `feature-readiness-gating` — define tiers, instrument readiness signals, create feature flags and unlock messages
- `posthog-gtm-events` — establish event taxonomy for feature readiness tracking
- `threshold-engine` — evaluate 14-day adoption rate against ≥35% pass threshold
