---
name: addon-cross-sell-health-monitor
description: Monitor add-on discovery funnel health, cross-sell conversion rates, and ARPU impact with automated alerting
category: Revenue Ops
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - n8n-scheduling
  - n8n-triggers
  - attio-reporting
---

# Add-On Cross-Sell Health Monitor

This drill builds the monitoring layer for add-on discovery plays. It tracks the full funnel from trigger detection through add-on activation, measures ARPU impact, identifies underperforming add-ons and surfaces, and alerts when metrics deviate from baseline.

## Input

- Add-on discovery surfaces deployed and events flowing (from `addon-discovery-surface-build` drill)
- At least 14 days of discovery event data in PostHog
- n8n instance for scheduled monitoring
- Attio with expansion deal tracking

## Steps

### 1. Build the cross-sell funnel

Using the `posthog-funnels` fundamental, create the primary conversion funnel:

```
addon_discovery_impression
  -> addon_discovery_clicked
    -> addon_activation_started
      -> addon_activated
```

Break this funnel down by:
- **Add-on**: which add-on has the best impression-to-activation rate
- **Surface type**: tooltips vs. banners vs. email — which surface converts best
- **Trigger behavior**: which usage trigger produces the highest-quality leads
- **User plan**: free vs. paid vs. enterprise — where is expansion revenue coming from
- **Days since signup**: do newer or older users cross-sell better

The biggest drop-off step is where optimization effort should focus first.

### 2. Build the cross-sell dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Cross-sell funnel | Funnel chart | Overall impression -> activation conversion |
| Conversion by add-on | Bar chart | Which add-ons convert best |
| Conversion by surface | Bar chart | Which surface types convert best |
| ARPU trend | Line chart | Monthly ARPU with cross-sell revenue broken out |
| Discovery volume | Trend line | Daily impressions, clicks, activations |
| Fatigue metrics | Table | Dismissal rates by add-on, suppressed user count |
| Revenue impact | Number | Monthly revenue from add-on activations this period |
| Time-to-activation | Distribution | Days between first impression and activation |

### 3. Set up automated alerts

Using `n8n-scheduling`, create alert workflows:

**Daily check (9am UTC)**:
- Query PostHog for yesterday's cross-sell funnel metrics
- Alert if: impression-to-click rate drops below 3% (surfaces are being ignored)
- Alert if: click-to-activation rate drops below 10% (activation flow is broken)
- Alert if: dismissal rate exceeds 60% for any add-on (surface is annoying)
- Alert if: zero activations for 3 consecutive days (something is broken)

**Weekly check (Monday 9am UTC)**:
- Calculate week-over-week change in cross-sell conversion rate
- Alert if: conversion rate drops >20% WoW
- Calculate ARPU change attributable to cross-sell
- Generate weekly summary: total impressions, activations, revenue impact, best and worst performing add-on

**Monthly check (1st of month)**:
- Calculate monthly cross-sell revenue
- Compare against target (set during play setup)
- Identify add-ons with <5% activation rate for review
- Identify surfaces with highest fatigue (dismissal rate trending up)
- Flag users who hit 3+ triggers but activated zero add-ons (consider a different approach)

### 4. Track ARPU impact

Using `posthog-custom-events`, calculate ARPU segmented by cross-sell activity:

- **Base ARPU**: Average revenue per user across all users
- **Cross-sell ARPU**: Average revenue per user who activated at least one add-on
- **ARPU lift**: Cross-sell ARPU minus Base ARPU
- **Cross-sell penetration**: Percentage of users with at least one add-on

Track these monthly. The goal is increasing both penetration (more users buying add-ons) and lift (add-ons generating meaningful revenue).

### 5. Monitor add-on adoption retention

Not all activations stick. Using `posthog-cohorts`, create cohorts for users who activated each add-on and track:

- **7-day retention**: Did they use the add-on feature in the week after activation?
- **30-day retention**: Are they still actively using it a month later?
- **Churn-to-downgrade rate**: What percentage of add-on activations are reversed or downgraded within 60 days?

If 30-day retention is below 50% for an add-on, the discovery surface is converting users who are not ready — tighten the trigger threshold or improve the add-on's first-use experience.

### 6. Generate the weekly cross-sell brief

Using `n8n-scheduling`, automate a weekly report that includes:

1. **Top line**: Total add-on activations, revenue impact, ARPU change
2. **Funnel health**: Conversion rate at each step, change vs. prior week
3. **Best performer**: Which add-on + surface + trigger combination drove the most activations
4. **Worst performer**: Which combination has the lowest conversion — candidate for optimization or removal
5. **Fatigue check**: Are dismissal rates increasing? Any users hitting suppression thresholds?
6. **Recommendation**: One specific action to improve cross-sell performance next week

Post the brief to Slack and store in Attio as a note on the cross-sell campaign record.

## Output

- PostHog cross-sell funnel with breakdowns by add-on, surface, trigger, plan, and tenure
- Cross-sell dashboard with 8 panels
- Daily, weekly, and monthly alert workflows in n8n
- ARPU tracking segmented by cross-sell activity
- Add-on adoption retention tracking by cohort
- Weekly automated cross-sell brief

## Triggers

The daily alert runs on n8n cron. The weekly brief generates every Monday. The monthly review runs on the 1st. Re-run the full setup when adding new add-ons or restructuring the discovery surfaces.
