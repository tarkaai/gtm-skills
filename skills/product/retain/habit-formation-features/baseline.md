---
name: habit-formation-features-baseline
description: >
  Habit-Building Features — Baseline Run. Roll the validated streak mechanic to 50% of users
  via feature flag, add a full habit-building email sequence, instrument all gamification events,
  and run always-on for 2 weeks targeting ≥40% DAU and ≥20pp retention lift.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥40% DAU and ≥20pp retention lift vs control"
kpis: ["Daily active rate", "Streak survival rate at day 7", "Reminder-to-action conversion", "Retention lift vs control"]
slug: "habit-formation-features"
install: "npx gtm-skills add product/retain/habit-formation-features"
drills:
  - gamification-event-tracking
  - onboarding-sequence-design
  - feature-adoption-monitor
---

# Habit-Building Features — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

≥40% daily active rate among the treatment group AND ≥20 percentage point retention lift at day 14 compared to the control group. This proves the habit mechanic sustains engagement over time, not just during the novelty period.

## Leading Indicators

- Streak survival rate at day 7: ≥50% of treatment users maintain a 3+ day streak
- Reminder-to-action conversion: ≥20% of reminder email recipients perform the target action within 2 hours
- Feature flag treatment group DAU exceeds control by ≥15pp by end of week 1
- Email sequence open rates ≥40% across the first 4 emails

## Instructions

### 1. Instrument all habit events

Run the `gamification-event-tracking` drill to build the full measurement layer:

- Implement the complete event schema from Smoke: `habit_action_completed`, `habit_streak_updated`, `habit_streak_broken`, `habit_reminder_sent`, `habit_reminder_opened`, `habit_reminder_converted`.
- Set PostHog person properties: `habit_current_streak`, `habit_longest_streak`, `habit_total_actions`, `habit_reminder_opt_in`, `habit_first_streak_date`.
- Build the gamification onboarding funnel: `signup` → `habit_surface_impression` → `habit_action_completed` (first) → `habit_streak_updated` (streak=3) → `habit_streak_updated` (streak=7).
- Build the streak retention funnel: streak=3 → streak=7 → streak=14.
- Create cohorts: "Active Streakers" (current streak ≥3), "Broken Streak" (streak broken in last 7 days, current=0), "Reminder Responsive" (≥2 reminder-to-action conversions in last 7 days), "Habit Dormant" (had a streak ≥3 previously, no action in 7+ days).
- Build a "Habit Health" dashboard: streak distribution histogram, DAU trend (treatment vs control), streak survival curve, reminder conversion rate trend, broken streak recovery rate.

### 2. Design the habit-building email sequence

Run the `onboarding-sequence-design` drill to create a 5-email habit-building sequence in Loops:

- **Email 1 — Habit introduction** (trigger: user first sees streak widget). Subject: "Your [Product] streak starts now." Explain the streak mechanic, show the first milestone (3-day), and link directly to the target action.
- **Email 2 — Day 2 nudge** (trigger: 24h after Email 1, IF no action today). Subject: "Don't break the chain — day 2." Reference their current streak count. Single CTA to perform the action.
- **Email 3 — Milestone celebration** (trigger: streak hits 3). Subject: "3-day streak — you're building a habit." Congratulate, preview the 7-day milestone reward, and suggest a secondary action.
- **Email 4 — Streak save** (trigger: streak broken AND previous streak ≥3). Subject: "Your streak ended at [N] days — restart now." Acknowledge the break without guilt. Offer a "restart bonus" (e.g., 2x points on the first action back). CTA to perform the action.
- **Email 5 — Weekly summary** (trigger: every 7 days for active users). Subject: "Your week: [N] actions, [streak] day streak." Show progress, compare to personal best, preview upcoming milestone.

Set up the Loops audience with contact properties synced from PostHog person properties via n8n webhook.

### 3. Monitor feature adoption

Run the `feature-adoption-monitor` drill to track how users discover and engage with the habit mechanic:

- Build the adoption funnel: `habit_surface_impression` → `habit_surface_clicked` → `habit_action_completed` → `habit_streak_updated` (streak=3).
- Create a stalled-user detection workflow in n8n: users who saw the widget 3+ days ago but never started a streak get an Intercom in-app message with a contextual prompt.
- Track intervention effectiveness: did the nudge convert stalled users into streak starters?
- Set alerts: if adoption funnel conversion drops below 30%, or if streak survival at day 7 drops below 40%.

### 4. Evaluate against threshold

After 14 days, measure:

- **Primary:** Treatment group DAU ≥40% AND retention lift ≥20pp vs control.
- **Secondary:** Streak survival at day 7 ≥50%, reminder conversion ≥20%.
- Compare treatment vs control using PostHog experiments. Ensure statistical significance (p < 0.05).
- If PASS: document the winning mechanic, email sequence performance, and proceed to Scalable.
- If FAIL: analyze the streak survival curve. If users drop off at day 2-3, the action is too costly or the reminder timing is wrong. If they drop off at day 5-7, the mechanic lacks escalating reward. Fix the weakest point and re-run for another 2 weeks.

## Time Estimate

- 3 hours: instrument all events, build funnels, cohorts, and dashboard
- 3 hours: design and implement the 5-email sequence in Loops
- 2 hours: configure feature adoption monitor and stalled-user interventions
- 2 hours: expand feature flag to 50%, set up control group
- 6 hours: daily monitoring over 14 days (25 min/day) + threshold evaluation + analysis

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, experiments, cohorts, dashboards | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Habit-building email sequence, reminders | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | Stalled-user detection, PostHog→Loops sync | Standard stack |
| Intercom | In-app nudges for stalled users | $29/seat/mo Essential ([intercom.com/pricing](https://www.intercom.com/pricing)) |

**Estimated play-specific cost:** ~$78/mo (Loops $49 + Intercom $29)

## Drills Referenced

- `gamification-event-tracking` — instrument all habit events, build funnels, cohorts, and the habit health dashboard
- `onboarding-sequence-design` — design and implement the 5-email habit-building sequence
- `feature-adoption-monitor` — track widget adoption, detect stalled users, and trigger interventions
