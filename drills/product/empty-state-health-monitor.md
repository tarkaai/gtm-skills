---
name: empty-state-health-monitor
description: Continuously monitor empty state conversion rates across all surfaces, detect new untreated empty states, and generate weekly optimization reports
category: Product
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-anomaly-detection
  - posthog-dashboards
  - posthog-custom-events
  - posthog-funnels
  - n8n-scheduling
  - n8n-triggers
  - n8n-workflow-basics
  - attio-notes
  - attio-reporting
---

# Empty State Health Monitor

This drill creates an always-on monitoring system that tracks empty state conversion rates across every product surface, detects degradation, identifies newly shipped features that lack empty state treatment, and generates weekly reports on empty state health. It is the play-specific monitoring complement to the `autonomous-optimization` drill at the Durable level.

## Input

- PostHog tracking flowing on all empty state surfaces (events: `empty_state_viewed`, `empty_state_cta_clicked`, `first_item_created`)
- At least 4 weeks of baseline performance data per surface
- n8n instance for scheduled monitoring
- Attio for logging monitoring results and trends

## Steps

### 1. Build the master empty state dashboard

Using `posthog-dashboards`, create a single dashboard called "Empty State Health" with these panels:

**Panel 1 — Overall CTR trend:** Line chart of `empty_state_cta_clicked / empty_state_viewed` across all surfaces, 12-week trend, with the 45% target line overlaid.

**Panel 2 — Per-surface CTR table:** Table ranked by CTR descending. Columns: surface name, views (7d), CTR (7d), CTR (4-week avg), trend direction (arrow up/down/flat), status (green/yellow/red based on threshold).

**Panel 3 — Conversion funnel:** Stacked funnel `empty_state_viewed` -> `empty_state_cta_clicked` -> `first_item_created` for the top 5 surfaces by volume.

**Panel 4 — Persona breakdown:** CTR by persona type for P0 surfaces. Identifies if a specific persona is underperforming.

**Panel 5 — New user activation from empty states:** Percentage of activated users whose activation path included an empty state CTA click. Tracks how central empty states are to the overall activation flow.

**Panel 6 — Template performance:** Template selection rates and subsequent `first_item_created` rates. Identifies top and bottom performing templates.

### 2. Build the daily health check workflow

Using `n8n-scheduling`, create a daily cron workflow (runs at 8 AM):

1. Query PostHog API for empty state metrics over the last 7 days per surface
2. Compare each surface's 7-day CTR to its 4-week rolling average
3. Classify each surface:
   - **Healthy:** CTR within ±10% of rolling average and above 40%
   - **Warning:** CTR 10-25% below rolling average, OR CTR between 35-40%
   - **Critical:** CTR >25% below rolling average, OR CTR below 35%, OR zero `empty_state_viewed` events (surface may be broken)
4. For Warning surfaces: log a note in Attio using `attio-notes` with the degradation data
5. For Critical surfaces: send Slack alert with specific surface name, current CTR, baseline CTR, and days of degradation

Using `n8n-workflow-basics`, handle edge cases:
- New surfaces with <100 views: skip threshold check, log as "insufficient data"
- Surfaces with zero events for 3+ days: flag as possible tracking breakage (not a CTR problem but a technical problem)

### 3. Detect untreated empty states

Using `posthog-custom-events`, monitor for `page_viewed` events on routes where `empty_state_viewed` has never fired. This indicates a product screen that users visit but which has no empty state tracking — likely a new feature shipped without empty state design.

Build an n8n workflow that runs weekly:
1. Pull all unique `page_viewed` route paths from the last 30 days
2. Pull all unique `surface` values from `empty_state_viewed` events
3. Compare: any `page_viewed` route that does not have a corresponding `empty_state_viewed` surface AND has >50 unique users is a candidate for empty state treatment
4. Output a list of "untreated surfaces" sorted by user volume
5. Log this list in Attio and send to Slack

This creates a continuous feedback loop: as the product ships new features, the monitor flags surfaces that need empty state design.

### 4. Build the weekly optimization report

Using `n8n-scheduling`, create a weekly cron workflow (runs Monday 9 AM):

1. Pull 7-day and 4-week metrics for all surfaces from PostHog
2. Generate a report structured as:

```
EMPTY STATE HEALTH — WEEK OF [DATE]

SUMMARY
- Overall CTR: [X%] (target: 45%) [trend arrow]
- Surfaces monitored: [N]
- Critical surfaces: [N]
- Active experiments: [N]

TOP PERFORMERS (highest CTR, 7d)
1. [Surface A] — [X%] CTR, [N] views
2. [Surface B] — [X%] CTR, [N] views
3. [Surface C] — [X%] CTR, [N] views

NEEDS ATTENTION (below threshold or declining)
1. [Surface X] — [X%] CTR (down from [Y%]), [diagnosis]
2. [Surface Y] — [X%] CTR (below 40% for [N] days)

NEW UNTREATED SURFACES
1. [Route path] — [N] unique users, no empty state

TEMPLATE PERFORMANCE
- Best: [Template name] — [X%] selection rate, [Y%] item creation rate
- Worst: [Template name] — [X%] selection rate (consider replacing)

EXPERIMENTS THIS WEEK
- [Surface] — [Variable tested] — [Result: winner/loser/inconclusive]

RECOMMENDED ACTIONS
1. [Specific action for the highest-impact issue]
2. [Specific action for the second-highest-impact issue]
```

3. Post the report to Slack
4. Store in Attio using `attio-notes` for historical tracking

### 5. Track convergence

Using `posthog-funnels`, track whether empty state optimization is converging (diminishing returns from further experiments). Monitor:
- Rolling 4-week CTR trend: if the rate of improvement drops below 1% per month for 3 consecutive months, the play has reached its local maximum
- Experiment win rate: if fewer than 25% of experiments produce statistically significant improvements, experiments are yielding diminishing returns

When convergence is detected, the report should recommend: "Empty state optimization has converged at [X%] CTR. Further gains require product changes (new features, redesigned flows) rather than empty state optimization. Reduce monitoring to biweekly."

## Output

- Master empty state health dashboard in PostHog
- Daily automated health checks with anomaly alerts
- Weekly detection of untreated empty states from new features
- Weekly optimization report with specific recommendations
- Convergence tracking to know when to reduce optimization effort

## Triggers

- Daily health check: every day at 8 AM via n8n cron
- Untreated surface detection: every Monday at 7 AM via n8n cron
- Weekly report: every Monday at 9 AM via n8n cron
