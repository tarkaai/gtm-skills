---
name: habit-formation-features-scalable
description: >
  Habit-Building Features — Scalable Automation. Roll habit mechanics to 100% of users,
  personalize streak difficulty and reminders per segment, A/B test variations, and build
  churn prevention triggers — targeting ≥35% DAU sustained across 500+ users over 2 months.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: "≥35% DAU sustained across 500+ users"
kpis: ["Daily active rate at scale", "Streak survival rate at day 14", "Segment-level DAU variance", "Churn save rate"]
slug: "habit-formation-features"
install: "npx gtm-skills add product/retain/habit-formation-features"
drills:
  - ab-test-orchestrator
  - churn-prevention
---

# Habit-Building Features — Scalable Automation

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

≥35% daily active rate sustained across 500+ users for 2 months. Habit mechanics personalized per segment so no cohort falls below 25% DAU. Automated churn prevention saves ≥30% of at-risk users.

## Leading Indicators

- DAU holds ≥35% for the first 2 weeks after full rollout (no novelty cliff)
- Personalized segments show ≤10pp DAU variance between highest and lowest performing segment
- A/B test velocity: ≥2 experiments completed per month with clear winners
- Churn prevention interventions triggered for ≥80% of at-risk users within 24 hours of signal

## Instructions

### 1. Run systematic A/B testing on habit mechanics

Run the `ab-test-orchestrator` drill to test variations that find the 10x multiplier:

- **Test 1 — Streak forgiveness:** Control: streak breaks on any missed day. Variant: 1 grace day per 7-day window. Hypothesis: forgiveness reduces streak-break abandonment by ≥30%. Use PostHog feature flags to split traffic 50/50. Run for 14 days or until 200+ users per variant.
- **Test 2 — Reminder timing:** Control: 6pm local time. Variant A: 9am (habit stacking with morning routine). Variant B: event-driven (2 hours after last session if no action taken). Hypothesis: event-driven reminders convert ≥25% better than fixed-time. Run for 14 days.
- **Test 3 — Milestone rewards:** Control: congratulatory message only. Variant: unlock a tangible product benefit at milestones (e.g., 7-day streak unlocks a theme, 14-day unlocks an advanced feature). Hypothesis: tangible rewards increase streak survival at day 14 by ≥20%.
- **Test 4 — Social proof:** Control: solo streak counter. Variant: show "X users in your cohort are on a streak today." Hypothesis: social visibility increases day-1 streak starts by ≥15%.

For each test, use `posthog-experiments` to track primary metric (DAU or streak survival) and guard against degradation of secondary metrics. Implement winners immediately. Log all results.

### 2. Build automated churn prevention

Run the `churn-prevention` drill to catch users whose habits are decaying before they churn:

- **Signal: Streak decay** — user's streak broke AND they had a 7+ day streak previously AND they have not restarted within 48 hours. This user invested in the habit and lost it.
- **Signal: Reminder fatigue** — user has not opened the last 3 reminder emails. The channel is dead.
- **Signal: Action frequency decline** — user's weekly action count dropped ≥50% from their 4-week average.
- Build an n8n workflow that runs daily, queries PostHog for users matching any signal, scores them (streak decay = 30 points, reminder fatigue = 20, frequency decline = 40), and routes interventions:
  - Score 20-40: Intercom in-app message when they next log in. "Your [N]-day streak may be gone, but your progress isn't. Pick up where you left off." Link to the target action.
  - Score 40-60: Loops triggered email. Switch channel from reminder to re-engagement. Subject: "We saved your spot." Show their total actions, longest streak, and a restart CTA.
  - Score 60+: Create an Attio task for human outreach. Include the user's usage timeline, streak history, and specific decay signals so the conversation is data-informed.
- Track save rate: users who received intervention AND returned to ≥3 actions/week within 14 days, divided by total interventions sent. Target ≥30%.

### 3. Personalize habit mechanics per segment

Run the the gamification personalization workflow (see instructions below) drill to ensure the habit system works across user types:

- Use PostHog cohorts to identify behavioral segments: "Power Users" (top 20% by weekly actions), "Steady Users" (middle 60%), "Light Users" (bottom 20%).
- Personalize streak difficulty: Power Users get a harder qualifying action (e.g., 3 actions/day instead of 1). Steady Users keep the standard mechanic. Light Users get an easier entry (any product visit counts for day 1-3, then escalates).
- Personalize reminder content: Power Users get milestone-focused reminders ("5 more days to your 30-day streak"). Steady Users get action-focused reminders ("Continue where you left off on [specific item]"). Light Users get value-focused reminders ("See what's new since your last visit").
- Use PostHog feature flags to assign personalization variants by cohort.
- Build an n8n workflow that re-evaluates segment membership weekly and adjusts feature flags for users who moved segments.

### 4. Evaluate against threshold

After 2 months, measure:

- **Primary:** DAU ≥35% averaged across weeks 5-8, with 500+ users in the habit system.
- **Secondary:** No segment below 25% DAU. Churn save rate ≥30%. At least 4 A/B tests completed with 2+ winners implemented.
- If PASS: document the winning configuration per segment, compile A/B test results, and proceed to Durable.
- If FAIL: identify which segment is dragging DAU below threshold. Focus all testing on that segment for the next 4 weeks. If the overall system works but scale is the issue (fewer than 500 users), the problem is upstream (acquisition/activation) — flag this and re-run once user base grows.

## Time Estimate

- 8 hours: design and launch 4 A/B tests (2 hours each, staggered across weeks)
- 8 hours: build churn prevention signals, scoring, and intervention workflows
- 8 hours: segment analysis, personalization design, feature flag configuration
- 4 hours: weekly n8n workflow for segment reassignment
- 16 hours: weekly monitoring, analysis, and iteration across 8 weeks (2 hours/week)
- 16 hours: experiment evaluation, winner implementation, documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, cohorts, dashboards | Free tier likely sufficient; paid at $0.00005/event above 1M ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | Habit emails, re-engagement sequences | $49/mo for 5K contacts; $149/mo for 50K ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app churn intervention messages | $85/seat/mo Advanced for targeting rules ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| n8n | Churn detection, segment reassignment, intervention routing | Standard stack |

**Estimated play-specific cost:** ~$134-234/mo (Loops $49-149 + Intercom $85)

## Drills Referenced

- `ab-test-orchestrator` — design and run 4 systematic experiments on streak mechanics, timing, rewards, and social proof
- `churn-prevention` — detect habit-decay signals and trigger tiered interventions to save at-risk users
- the gamification personalization workflow (see instructions below) — segment users by behavior and personalize streak difficulty, reminders, and rewards
