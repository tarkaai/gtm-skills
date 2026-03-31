---
name: wizard-completion-monitor
description: Monitor setup wizard completion rates, step-level dropoff, configuration success, and time-to-complete per persona and cohort
category: Onboarding
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-anomaly-detection
  - posthog-custom-events
  - n8n-scheduling
  - n8n-workflow-basics
  - attio-notes
---

# Wizard Completion Monitor

This drill creates a continuous monitoring system for setup wizard performance. It tracks completion rates, step-level dropoff, configuration success, and time-to-complete across personas and signup cohorts. Anomaly detection triggers alerts when any metric drifts outside normal bounds. This drill's output feeds directly into the `autonomous-optimization` drill for automated experimentation.

## Prerequisites

- Setup wizard running with PostHog events: `wizard_step_started`, `wizard_step_completed`, `wizard_step_failed`, `wizard_completed` (from `wizard-step-builder` drill)
- At least 2 weeks of wizard usage data in PostHog
- n8n instance for scheduled monitoring
- Attio configured for logging health observations

## Steps

### 1. Build the wizard health dashboard

Using the `posthog-dashboards` fundamental, create a dashboard titled "Setup Wizard Health" with these panels:

- **Overall completion rate (weekly trend)**: Line chart showing percentage of users who started the wizard and completed all steps, 12-week window. Add a target line at the play's threshold (65% for Smoke, 75% for Baseline, 70% at scale for Scalable+).
- **Step-level funnel**: Funnel visualization showing conversion between each wizard step. This is the most actionable panel -- the biggest dropoff shows where to focus.
- **Completion rate by persona**: Line chart, one line per persona variant, weekly. Identifies which personas struggle most with setup.
- **Time to complete by step**: Bar chart showing median time in minutes per wizard step. A step that takes >5 minutes is a friction signal.
- **Configuration success rate**: Percentage of completed wizard runs where the configuration actually works (e.g., data source connected and returning data, not just "Save" clicked). Tracks quality, not just completion.
- **Failure rate by step**: Bar chart showing `wizard_step_failed` events per step. Spikes indicate UX problems or integration breakage.
- **Stall rate**: Percentage of users who started a step but neither completed nor failed it within 24 hours. High stall = confusion, not error.

### 2. Build the step-level funnel

Using the `posthog-funnels` fundamental, create a funnel for each persona variant:

```
wizard_step_started (step_number=1)
  -> wizard_step_completed (step_number=1)
  -> wizard_step_started (step_number=2)
  -> wizard_step_completed (step_number=2)
  -> ... (all steps for this persona)
  -> wizard_completed
```

Filter by `persona_type` and `wizard_variant`. Set the conversion window to 7 days (users may complete setup across multiple sessions). Compare funnels across signup week cohorts to detect whether the wizard is improving or degrading over time.

### 3. Define anomaly thresholds

| Metric | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Overall completion rate | Within 10% of 4-week rolling avg | 10-20% below avg for 1 week | >20% below avg OR below play threshold for 2+ weeks |
| Step completion rate (any step) | Within 15% of avg | 15-30% below for 1 week | >30% below OR below 50% absolute |
| Step failure rate | Below 10% per step | 10-20% for any step | >20% failure rate on any step |
| Median time-to-complete | Within 25% of avg | 25-50% above avg | >50% above avg (wizard getting slower) |
| Config success rate | Above 85% | 75-85% | Below 75% (users "complete" but config broken) |
| Stall rate | Below 15% per step | 15-25% | >25% (users confused, not erroring) |

### 4. Build the daily monitoring workflow

Using `n8n-scheduling` and `n8n-workflow-basics`, create a workflow that runs daily at 08:00 UTC:

1. Query PostHog for wizard metrics from the last 7 days using the PostHog API
2. For each metric, compare against the 4-week rolling average (use `posthog-anomaly-detection`)
3. Classify each metric: normal, warning, or critical
4. If any metric is critical: send an immediate alert with this format:
   ```
   WIZARD ALERT: [metric] is [critical/warning]
   - Current value: [X]
   - Expected value: [Y] (4-week avg)
   - Affected persona: [persona_type or "all"]
   - Worst step: [step_name] ([step_number])
   - Suggested investigation:
     - If step failure spike: check integration APIs, review error logs
     - If completion drop: review recent product changes, check tour rendering
     - If time increase: look for new friction in session recordings
     - If config success drop: verify backend validation, check data source health
   ```
5. Log all observations to Attio using `attio-notes`

### 5. Build the weekly wizard report

Using `n8n-scheduling`, create a Monday 09:00 UTC workflow:

1. Pull 7-day and 4-week metrics from PostHog
2. Generate a structured report:

```
# Setup Wizard Report -- Week of [date]

## Summary
- New wizard starts: [N]
- Overall completion rate: [X%] (prev week: [Y%], target: [Z%])
- Median time to complete: [M] minutes
- Config success rate: [S%]

## Per-Persona Breakdown
| Persona | Starts | Completed | Rate | Avg Time | Config Success |
|---------|--------|-----------|------|----------|----------------|
| ...     | ...    | ...       | ...  | ...      | ...            |

## Step-Level Dropoff
| Step | Started | Completed | Failed | Stalled | Dropoff |
|------|---------|-----------|--------|---------|---------|
| ...  | ...     | ...       | ...    | ...     | ...     |

## Anomalies This Week
- [List of warning/critical anomalies with dates and values]

## Active Experiments
- [List any running A/B tests from autonomous-optimization]

## Top Priority
- [The single highest-impact issue based on this week's data]
```

3. Post to Slack and store in Attio

### 6. Build cohort comparison

Using `posthog-cohorts`, create weekly cohort tracking:

1. Each signup week becomes a cohort
2. Compare this week's cohort wizard performance against the previous 4 cohorts
3. Flag cohort drift: if a new cohort completes the wizard at a significantly different rate, investigate whether the user mix changed (different signup source, different persona distribution) or the wizard changed (deploy, feature flag change)
4. Log cohort observations in Attio

### 7. Connect to autonomous optimization

This drill's output feeds the `autonomous-optimization` drill:

- **Step dropoff anomaly** triggers hypothesis generation focused on that specific step (tour copy, step ordering, validation UX)
- **Persona-specific decline** triggers hypothesis generation focused on that persona's wizard variant (wrong steps, wrong guidance, missing context)
- **Config success drop** triggers investigation into backend health before running UX experiments
- **Time increase** triggers hypothesis generation focused on friction reduction (fewer fields, better defaults, smarter pre-fill)
- **Weekly report** provides the context data that hypothesis generation needs for informed experiment design

## Output

- Live dashboard showing wizard health across all dimensions
- Daily automated anomaly detection with immediate critical alerts
- Weekly structured report with per-persona and per-step breakdown
- Cohort comparison detecting wizard performance drift
- Direct feed into autonomous-optimization for automated response
