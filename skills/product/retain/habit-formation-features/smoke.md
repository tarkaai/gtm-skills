---
name: habit-formation-features-smoke
description: >
  Habit-Building Features — Smoke Test. Identify the 1-2 retention-critical actions, design a
  minimal streak/reminder mechanic around them, ship to 10-20 users behind a feature flag, and
  measure whether daily active rate reaches 30% within the first week.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥30% daily active rate among test cohort in week 1"
kpis: ["Daily active rate", "Streak start rate", "Reminder open rate"]
slug: "habit-formation-features"
install: "npx gtm-skills add product/retain/habit-formation-features"
drills:
  - gamification-system-design
  - lead-capture-surface-setup
  - threshold-engine
---

# Habit-Building Features — Smoke Test

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

≥30% of the test cohort (10-20 users) performs the target action daily during week 1. This proves that the chosen habit mechanic creates a measurable pull-back signal before investing in automation.

## Leading Indicators

- Users view the streak counter or reminder UI within 24 hours of exposure
- At least 50% of test users complete the target action on day 1
- Streak start rate (users with a 2+ day streak by day 3) ≥40%
- Reminder email open rate ≥35%

## Instructions

### 1. Design the habit mechanic

Run the `gamification-system-design` drill scoped to a single mechanic. Do NOT build the full gamification system. Focus on:

- Query PostHog to identify the 1-2 actions that most differentiate retained users (active 30+ days) from churned users (inactive 14+ days). These are your habit targets.
- Select ONE mechanic: a daily streak counter tied to the top retention-critical action. Define the streak unit (daily), minimum qualifying action (1 per day), and the first 3 milestones (3-day, 7-day, 14-day).
- Design a reminder trigger: if the user has not performed the action by 6pm local time, send a push/email nudge via Loops.
- Document the event schema: `habit_action_completed`, `habit_streak_updated`, `habit_reminder_sent`, `habit_reminder_opened`.

### 2. Build the in-product capture surface

Run the `lead-capture-surface-setup` drill to build the habit UI surface:

- Deploy a lightweight streak counter widget on the product's main screen. The widget shows: current streak count, next milestone, and a CTA to perform the target action.
- Instrument PostHog events using `posthog-custom-events`: `habit_surface_impression` (widget enters viewport), `habit_surface_clicked` (user clicks the CTA), `habit_action_completed` (user performs the target action).
- Gate the widget behind a PostHog feature flag targeting 10-20 specific users.

**Human action required:** Review the streak counter UI and reminder email copy before enabling the feature flag. Ensure the mechanic is tied to a genuinely valuable action, not a vanity metric.

### 3. Launch and observe for 7 days

- Enable the feature flag for the test cohort.
- Configure a Loops transactional email for the daily reminder: subject line referencing the user's current streak count, single CTA linking directly to the target action.
- Monitor PostHog Live Events daily to verify events are firing correctly.
- Log any user feedback or confusion signals (support tickets mentioning the streak, session recordings showing hesitation on the widget).

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure:

- **Primary metric:** Daily active rate among test cohort ≥30% averaged across days 2-7.
- **Secondary metrics:** Streak start rate (2+ day streak) ≥40%, reminder open rate ≥35%.
- If PASS: document which action was chosen, which mechanic worked, and proceed to Baseline.
- If FAIL: examine PostHog funnel from `habit_surface_impression` → `habit_surface_clicked` → `habit_action_completed`. If the drop-off is at impression→click, the surface is not compelling. If at click→action, the action itself is too costly. Iterate on the weakest link and re-run.

## Time Estimate

- 1 hour: PostHog analysis to identify retention-critical actions
- 1 hour: design streak mechanic and event schema
- 1 hour: build streak widget and instrument events
- 0.5 hours: configure Loops reminder email and feature flag
- 1.5 hours: daily monitoring over 7 days (15 min/day) + threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature flags, event tracking, cohort analysis | Free tier: 1M events/mo, 5K recordings ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Daily reminder emails | Free tier: 1,000 contacts, 2,000 sends/mo ([loops.so/pricing](https://loops.so/pricing)) |

**Estimated play-specific cost:** Free

## Drills Referenced

- `gamification-system-design` — identify retention-critical actions and design the minimal streak mechanic
- `lead-capture-surface-setup` — build and instrument the in-product streak widget
- `threshold-engine` — evaluate daily active rate against the ≥30% pass threshold
