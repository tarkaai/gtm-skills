---
name: shortcut-adoption-monitor
description: Track shortcut discovery rates, usage frequency, efficiency gains per user, and identify stalled users for intervention
category: Enablement
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-sequences
---

# Shortcut Adoption Monitor

This drill builds the measurement and intervention layer for keyboard shortcut promotion. It tracks how users progress from mouse-only to shortcut-proficient, identifies where they stall, calculates actual efficiency gains, and triggers automated re-engagement when users regress or plateau.

## Input

- Shortcut discovery promotion already configured (`shortcut-discovery-promotion` drill)
- PostHog tracking `action_via_mouse`, `action_via_shortcut`, `shortcut_hint_shown`, `shortcut_hint_converted` events
- At least 7 days of shortcut interaction data
- n8n instance for scheduled monitoring
- Intercom and Loops configured for intervention delivery

## Steps

### 1. Build the shortcut adoption funnel

Using `posthog-funnels`, create a funnel tracking the progression from awareness to habitual usage:

```
shortcut_hint_shown
  -> shortcut_hint_converted (used shortcut within same session)
    -> shortcut_used_again (used same shortcut in a later session)
      -> shortcut_habitual (used shortcut 10+ times in 14 days)
```

Break down by:
- Shortcut ID (which shortcuts convert best)
- User cohort (beginner, intermediate, power)
- Hint trigger type (contextual tooltip, product tour, command palette)

Identify the largest drop-off. If users see hints but do not try the shortcut, the hint copy or timing is wrong. If they try once but do not repeat, the shortcut may not feel faster or the muscle memory is not building.

### 2. Calculate the shortcut ratio per user

Using `posthog-custom-events`, compute a per-user "shortcut ratio" — the percentage of actions performed via shortcut versus mouse for actions that have shortcut equivalents:

```
shortcut_ratio = count(action_via_shortcut) / (count(action_via_shortcut) + count(action_via_mouse))
```

Track this as a weekly trend per user and as a cohort average. Create PostHog insights for:

- **Overall shortcut ratio** (target: 25%+ across all users with 7+ days tenure)
- **Shortcut ratio by tenure cohort** (week 1, week 2-4, month 2-3, month 3+)
- **Shortcut ratio by individual shortcut** (which shortcuts get adopted vs. ignored)
- **Shortcut ratio trend** (is it climbing week over week)

Store the shortcut ratio as a PostHog person property so it can be used in cohort definitions and Intercom targeting.

### 3. Measure efficiency gains

Using `posthog-custom-events`, calculate the actual time saved per user from shortcut adoption. For each action with a shortcut equivalent:

- Measure median time-to-complete via mouse path (time from page load or previous action to click)
- Measure median time-to-complete via shortcut (time from page load or previous action to keystroke)
- Efficiency gain = mouse_time - shortcut_time

Aggregate per user per week:
```
weekly_time_saved = sum(efficiency_gain_per_action * shortcut_usage_count)
```

Surface this in the product: "You saved X minutes this week using shortcuts." This reinforces the behavior.

### 4. Build stalled-user detection

Using `n8n-scheduling`, create a daily workflow that queries PostHog for users who have stalled in their shortcut adoption:

- **Hint-ignored**: Shown 5+ shortcut hints in the last 14 days, shortcut ratio is still 0%. The hints are not working for this user. Move them to the `shortcut-dormant` cohort.
- **One-and-done**: Tried a shortcut 1-2 times but shortcut ratio has stayed below 5% for 14+ days. The initial trial did not convert to habit.
- **Regressing**: Shortcut ratio dropped by 10+ percentage points week-over-week. User is reverting to mouse. Something changed — new device, new workflow, or the shortcut no longer fits their pattern.
- **Plateaued**: Shortcut ratio has been between 15-25% for 3+ weeks. User adopted some shortcuts but stopped discovering new ones.

### 5. Configure stalled-user interventions

For **hint-ignored** users: Stop all tooltip-based hints using `intercom-in-app-messages`. Instead, try a different modality — send a Loops email using `loops-sequences` with a 30-second GIF showing the top 3 shortcuts in action: "3 shortcuts that save our fastest users 20 minutes/week." Include a deep link to the in-product shortcut reference.

For **one-and-done** users: Using `intercom-in-app-messages`, show a gentle reminder the next time they perform the specific action via mouse that they previously tried via shortcut: "Remember: `Cmd+K` does this in half the time." One reminder, then stop.

For **regressing** users: No intervention — regression is usually caused by context change (new device, changed workflow). Re-evaluate after 7 days. If shortcut ratio recovers, no action. If it stays low, re-enter them into the shortcut-ready-beginner cohort.

For **plateaued** users: Using `intercom-in-app-messages`, surface the "next best shortcut" — the shortcut with the highest predicted time savings based on the actions they still perform via mouse. One targeted nudge per week.

### 6. Build the shortcut adoption dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Overall shortcut ratio (trend) | Line chart | Is shortcut adoption growing across the user base |
| Shortcut ratio by tenure cohort | Grouped bar chart | Do newer users adopt faster than older cohorts did |
| Adoption funnel (hint to habitual) | Funnel chart | Where users drop off in the adoption journey |
| Individual shortcut adoption rates | Horizontal bar chart | Which shortcuts are popular vs. ignored |
| Time saved per week (aggregate) | Area chart | Total efficiency gains delivered to users |
| Stalled users by type | Table | How many users are stalled at each stage |
| Hint conversion rate by trigger type | Bar chart | Which hint delivery method works best |
| Shortcut ratio distribution | Histogram | Distribution of users across ratio buckets (0%, 1-10%, 11-25%, 26-50%, 50%+) |

Set alerts for:
- Overall shortcut ratio dropping below 20% for 2+ consecutive weeks
- Stalled user count exceeding 30% of active users
- Hint conversion rate dropping below 5% (hints are being ignored)
- Any single shortcut with 0% adoption after 4 weeks of promotion (remove it from the promotion list or reconsider the shortcut's design)

### 7. Generate the weekly shortcut adoption report

Using `n8n-scheduling`, create a weekly workflow that:

1. Pulls all dashboard metrics from PostHog
2. Compares against previous week
3. Generates a summary: shortcut ratio trend, top adopted shortcut this week, biggest stall segment, total time saved across all users
4. Posts to Slack and stores in Attio as a note on the product record
5. If any alert threshold was breached, flag it prominently at the top of the report

## Output

- Shortcut adoption funnel in PostHog
- Per-user shortcut ratio tracked as a person property
- Efficiency gain calculations (time saved per user per week)
- Daily stalled-user detection workflow in n8n
- Automated interventions for each stall type via Intercom and Loops
- Shortcut adoption dashboard with 8 panels and threshold alerts
- Weekly adoption report generated and posted automatically

## Triggers

The stalled-user detection runs daily via n8n cron. The dashboard and efficiency metrics are reviewed weekly. Re-run the full drill setup when adding new shortcuts or changing the shortcut promotion strategy.
