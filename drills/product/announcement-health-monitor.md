---
name: announcement-health-monitor
description: Monitor feature announcement effectiveness across channels, track adoption decay, and surface underperforming announcements for intervention
category: Product
tools:
  - PostHog
  - n8n
  - Intercom
  - Loops
  - Attio
fundamentals:
  - posthog-dashboards
  - posthog-cohorts
  - posthog-funnels
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - intercom-in-app-messages
  - loops-transactional
  - attio-notes
---

# Announcement Health Monitor

This drill builds the ongoing measurement and alerting layer for feature announcement campaigns. It tracks whether announcements actually drive sustained adoption (not just initial clicks), identifies which channels and segments produce the best results, and triggers interventions when adoption decays after launch.

## Input

- Feature announcement campaign running for at least 14 days (needs baseline data)
- PostHog tracking configured with announcement events: `announcement_shown`, `announcement_clicked`, `feature_first_used`, `feature_retained_7d`, `feature_retained_30d`
- n8n instance for scheduled monitoring
- Attio with campaign records for each announced feature

## Steps

### 1. Build the announcement effectiveness funnel

Using the `posthog-funnels` fundamental, create a per-announcement funnel:

```
announcement_shown (channel={in-app|email|blog|social})
  -> announcement_clicked
    -> feature_first_used
      -> feature_retained_7d (used feature again within 7 days)
        -> feature_retained_30d (used feature 3+ times within 30 days)
```

Break down by:
- Channel (which announcement surface drove the most sustained adoption)
- User segment (plan, tenure, usage level)
- Announcement tier (major, notable, minor)

The key insight is channel-level retention: email may drive more clicks but in-app may drive more sustained usage. Measure both.

### 2. Create the adoption decay tracker

Using `posthog-custom-events`, build a time-series analysis for each announced feature:

- **Day 0-3 spike**: Expected post-announcement usage surge
- **Day 4-14 decay**: How much usage drops after the novelty period
- **Day 15-30 steady state**: Where usage stabilizes — this is the true adoption rate

Calculate the decay ratio: `steady_state_usage / peak_usage`. A decay ratio above 0.4 means the feature has real stickiness. Below 0.2 means the announcement drove curiosity, not adoption. Track this ratio across announcements to benchmark.

### 3. Build the scheduled monitoring workflow

Using `n8n-scheduling`, create a workflow that runs every Monday:

1. Query PostHog for all features announced in the last 90 days
2. For each feature, pull: current weekly active users, decay ratio, channel breakdown
3. Classify each feature's adoption health:
   - **Healthy**: Steady state above 30% of target segment, decay ratio above 0.4
   - **Fading**: Usage declining week-over-week for 2+ consecutive weeks
   - **Failed**: Steady state below 10% of target segment after 30 days
4. For Healthy features: log status in Attio, no action
5. For Fading features: trigger re-engagement (Step 4)
6. For Failed features: flag for product team review, stop active announcements

### 4. Configure re-engagement interventions

For features classified as Fading:

Using `intercom-in-app-messages`, show a contextual reminder to users who tried the feature but stopped: "You tried [feature] last week. Here's a tip: [specific use case]. Try it now." Target only users who used it once but not in the last 7 days.

Using `loops-transactional`, send a follow-up email to users in the announcement segment who never clicked: "We launched [feature] recently and thought you'd find it useful for [specific benefit]. Here's a 2-minute walkthrough." Include a direct deep link.

### 5. Build the announcement performance dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Announcement funnel by feature | Funnel | Click-through and adoption for each recent launch |
| Channel effectiveness | Stacked bar | Which channel drives the most retained users |
| Adoption decay curves | Multi-line trend | Overlay decay curves for each feature launch |
| Segment response rates | Heatmap | Which user segments respond best to announcements |
| Feature health status | Table | Current status (Healthy/Fading/Failed) for each feature |
| Re-engagement effectiveness | Bar | Conversion rate of re-engagement nudges |
| Weekly announcement volume | Counter | How many announcements sent this week (fatigue check) |

Set alerts for:
- Any feature dropping from Healthy to Fading
- Announcement fatigue: more than 3 announcements shown to the same user in 7 days
- Overall announcement click-through rate dropping below 10%

### 6. Generate the weekly announcement brief

Using the n8n workflow from Step 3, produce a structured brief:

```
## Feature Announcement Health — Week of {date}

### Active Announcements
| Feature | Launched | Decay Ratio | Status | Channel Winner |
|---------|----------|-------------|--------|----------------|

### Interventions Triggered
- {feature}: Re-engagement email sent to {N} users
- {feature}: In-app reminder shown to {N} users

### Metrics Summary
- Avg click-through rate: {X}%
- Avg 7-day retention rate: {X}%
- Avg 30-day retention rate: {X}%
- Best channel this week: {channel}

### Recommendations
- {Actionable recommendation based on data}
```

Post to Slack and store in Attio as a note on the campaign record.

## Output

- Per-feature adoption funnel with channel breakdown
- Adoption decay ratio calculated for each announced feature
- Weekly health classification (Healthy/Fading/Failed)
- Automated re-engagement for Fading features
- Announcement performance dashboard with 7 panels
- Weekly announcement brief

## Triggers

The monitoring workflow runs every Monday via n8n cron. Re-engagement interventions fire within 24 hours of a feature being classified as Fading. The dashboard is always-on. Re-run the full drill setup when changing announcement channels or adding new feature tiers.
