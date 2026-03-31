---
name: gate-conversion-health-report
description: Weekly report on premium feature gate performance covering impression-to-upgrade funnels, trial conversion, revenue impact, and gate fatigue signals
category: Conversion
tools:
  - PostHog
  - Attio
  - n8n
  - Anthropic
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - attio-deals
  - n8n-scheduling
  - n8n-workflow-basics
---

# Gate Conversion Health Report

This drill generates a weekly structured report on how premium feature gates are performing. It tracks the full gate-to-upgrade funnel, detects gate fatigue, identifies high-value trial candidates, and surfaces revenue impact from gate-driven upgrades. The report feeds directly into the autonomous optimization loop at Durable level.

## Input

- PostHog tracking configured with gate events: `gate_impression`, `gate_preview_engaged`, `gate_trial_started`, `gate_trial_converted`, `gate_upgrade_completed`, `gate_dismissed`
- At least 14 days of gate interaction data
- Attio with upgrade deals tagged by gate source
- n8n instance for scheduling the report

## Steps

### 1. Build the gate funnel dashboard

Using the `posthog-dashboards` fundamental, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Gate funnel (overall) | Funnel chart | `gate_impression` -> `gate_preview_engaged` -> `gate_trial_started` -> `gate_upgrade_completed` |
| Gate funnel by feature | Funnel chart per gated feature | Which gates convert best |
| Trial-to-upgrade by cohort | Line chart (weekly cohorts) | Are newer cohorts converting better |
| Revenue from gate-driven upgrades | Trend line | MRR attributable to gate conversions |
| Gate fatigue index | Line chart | Dismissal rate trending over 4 weeks per gated feature |
| Gate interaction heatmap | Heatmap | Which features get the most gate impressions by day of week and time |
| Trial duration vs. conversion | Bar chart | Do 7-day trials convert differently than 14-day trials |

### 2. Define the gate fatigue metric

Gate fatigue occurs when users encounter the same gate repeatedly and stop engaging. Using `posthog-custom-events`, calculate per user per gated feature:

- **Impression count**: How many times has this user seen this gate
- **Engagement decay**: Compare first-impression engagement rate to nth-impression engagement rate
- **Dismissal acceleration**: Is the user dismissing faster (fewer seconds viewing the gate) over time

A feature is fatigued for a user when: the user has seen the gate 5+ times AND engagement rate dropped below 2% AND last 3 impressions were dismissed within 2 seconds.

When fatigue is detected, suppress the gate for that user for 14 days and try an alternative approach (email, in-app message about the feature's value, or a time-limited trial offer).

### 3. Schedule the weekly report workflow

Using `n8n-scheduling`, create a workflow that runs every Monday at 8:00 AM:

1. Query PostHog for last 7 days of gate funnel data using `posthog-funnels`
2. Pull per-feature breakdown using `posthog-cohorts` (cohort per gated feature)
3. Pull upgrade revenue data from Attio using `attio-deals` (filter by deals with source = "feature-gate")
4. Generate the report using Claude:
   - **Per-feature gate table**: feature name, impressions, preview engagements, trials started, upgrades completed, conversion rate, revenue, trend vs. 4-week average
   - **Top performer**: which gated feature drove the most upgrades this week and why
   - **Underperformer**: which gated feature has the worst funnel conversion and where the drop-off occurs
   - **Fatigue alerts**: features where fatigue is detected for >10% of exposed users
   - **Trial health**: active trials, expected conversion based on historical rate, trials at risk (low engagement during trial)
   - **Recommended action**: one specific experiment to run next week
5. Post to Slack and store in Attio as a note on the feature-gating campaign record

### 4. Track trial health during active trials

Using `posthog-custom-events`, monitor users who have active trials of premium features:

- **Healthy trial**: User engaged with the premium feature 3+ times in the first 3 days
- **At-risk trial**: User started a trial but has not engaged with the premium feature in 3+ days
- **Abandoned trial**: Trial period is >50% elapsed with zero feature engagement

For at-risk and abandoned trials, fire an n8n webhook that triggers an intervention via Intercom or Loops: a contextual message showing what the user can accomplish with the premium feature during their remaining trial time.

### 5. Calculate revenue attribution

Using `attio-deals`, tag every upgrade deal with the gate source:
- `gate_source_feature`: which gated feature triggered the upgrade
- `gate_path`: preview -> trial -> upgrade, or preview -> direct upgrade
- `gate_impressions_before_conversion`: how many gate encounters before the user converted
- `trial_duration_days`: how long the trial lasted before conversion

Aggregate monthly: total MRR from gate-driven upgrades, average deal value by gate source, fastest-converting gates.

## Output

- Weekly health report covering all active feature gates
- Gate fatigue detection and automatic suppression
- Trial health monitoring with automated interventions for at-risk trials
- Revenue attribution linking upgrades to specific gated features
- Recommended action feeding into the autonomous optimization loop

## Triggers

Runs weekly via n8n cron. Trial health monitoring runs daily. Fatigue detection runs with every gate impression event.
