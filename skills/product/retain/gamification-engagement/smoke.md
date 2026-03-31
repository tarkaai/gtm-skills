---
name: gamification-engagement-smoke
description: >
  Gamified Product Experience — Smoke Test. Design and instrument a gamification system
  with streaks, badges, and points. Launch to 10-20 users and measure whether gamification
  mechanics produce engagement signal above baseline.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=40% of test users interact with at least one gamification mechanic within 7 days"
kpis: ["Gamification participation rate", "Streak initiation rate", "First badge earn rate"]
slug: "gamification-engagement"
install: "npx gtm-skills add product/retain/gamification-engagement"
drills:
  - gamification-system-design
  - gamification-event-tracking
---

# Gamified Product Experience — Smoke Test

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product

## Outcomes

>=40% of test users interact with at least one gamification mechanic (earn points, start a streak, or earn a badge) within 7 days. This proves gamification produces engagement signal above the baseline product experience.

## Leading Indicators

- Users view the gamification UI (points counter, badge display, streak indicator) within first session
- At least 3 users earn their first badge within 48 hours
- At least 2 users maintain a 3-day streak
- Users who interact with gamification have higher session frequency than those who do not

## Instructions

### 1. Design the gamification system

Run the `gamification-system-design` drill to produce the full specification:

- Identify 3-5 retention-critical product actions by querying PostHog for behaviors that differentiate retained users from churned users
- Select which mechanics to deploy: streaks (for habitual actions), badges (for milestones), points (for overall engagement scoring)
- Define the progression map: 4 levels with point thresholds, 8-10 badges across 3 tiers, daily streak with milestones at 3, 7, 14 days
- Map rewards to Intercom delivery: design the onboarding checklist that teaches gamification through doing
- Output: specification document with event schema, badge definitions, streak rules, and point table

**Human action required:** Review the gamification specification before implementation. Verify that the retention-critical actions identified from PostHog data are correct. Approve the badge names, point values, and progression thresholds. Implement the gamification logic in the product codebase.

### 2. Instrument gamification events

Run the `gamification-event-tracking` drill to set up measurement:

- Implement all gamification events in PostHog: `gamification_points_earned`, `gamification_streak_updated`, `gamification_badge_awarded`, `gamification_level_up`
- Set person properties: `gamification_level`, `gamification_total_points`, `gamification_badges_count`, `gamification_current_streak`
- Build the gamification onboarding funnel: signup -> first points -> first badge -> 3-day streak -> level 2
- Create the "Gamification Active" and "Gamification Dormant" cohorts
- Build a minimal gamification dashboard: participation rate, streak distribution, badge award velocity

**Human action required:** Deploy the instrumented product code to a staging environment. Verify events fire correctly by triggering each gamification action manually and checking PostHog.

### 3. Launch to test group

Use PostHog feature flags to enable gamification for 10-20 users:

1. Create a feature flag `gamification-enabled` with rollout to a specific user list or 5% of active users
2. Ensure the control group (gamification disabled) is tracked for comparison
3. Monitor PostHog for the first 24 hours: verify events are flowing, no errors in the funnel, and the dashboard populates

### 4. Observe for 7 days

Monitor the gamification dashboard daily:

- Are users earning points? (signals discovery)
- Are users starting streaks? (signals habit formation)
- Are badges being awarded? (signals milestone progression)
- Where do users drop off in the onboarding funnel?

Do not intervene or change anything during the 7-day observation period.

### 5. Evaluate against threshold

After 7 days, compute:

- **Gamification participation rate**: count of users who triggered at least one `gamification_points_earned` event / total users with gamification enabled
- **Pass threshold**: >=40%

If PASS: document what worked, which mechanics had highest adoption, and proceed to Baseline.
If FAIL: diagnose from the funnel. If users are not seeing the gamification UI, it is a visibility problem. If they see it but do not engage, it is a relevance problem (wrong actions rewarded or wrong mechanics chosen). Iterate on the specification and re-run.

## Time Estimate

- 2 hours: gamification system design (drill execution + human review)
- 1.5 hours: event instrumentation and dashboard setup
- 0.5 hours: feature flag setup and launch
- 1 hour: 7-day monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnels, cohorts, feature flags, dashboard | Free tier: 1M events/mo, 1M feature flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | Onboarding checklist for gamification introduction | Essential: $29/seat/mo ([intercom.com/pricing](https://intercom.com/pricing)) |

**Estimated play-specific cost at this level:** Free (within PostHog free tier for 10-20 users; Intercom checklist uses existing seat)

## Drills Referenced

- `gamification-system-design` — designs the gamification mechanics, progression map, and event schema
- `gamification-event-tracking` — instruments all gamification events in PostHog and builds measurement layer
