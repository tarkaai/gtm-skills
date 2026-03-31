---
name: milestone-retention-monitor
description: Track milestone celebration effectiveness on retention, detect decay in celebration engagement, and surface users who hit milestones but still churn
category: Retention
tools:
  - PostHog
  - n8n
  - Attio
fundamentals:
  - posthog-cohorts
  - posthog-dashboards
  - posthog-custom-events
  - posthog-anomaly-detection
  - n8n-scheduling
  - n8n-triggers
  - attio-notes
---

# Milestone Retention Monitor

This drill builds the always-on measurement layer that answers: are milestone celebrations actually retaining users? It detects when celebration effectiveness decays, identifies users who hit milestones but still disengage, and generates the data the `autonomous-optimization` drill needs to run experiments.

## Input

- PostHog tracking milestone events (`milestone_reached`, `celebration_shown`, `celebration_engaged`, `celebration_cta_clicked`) from the `usage-milestone-rewards` drill
- At least 4 weeks of milestone data across multiple cohorts
- n8n instance for scheduled monitoring
- Attio for logging retention insights

## Steps

### 1. Build milestone-retention cohort comparisons

Using `posthog-cohorts`, create paired cohorts for each milestone tier:

- **Celebrated cohort**: Users who reached milestone N AND saw the celebration message AND engaged with it (clicked, shared, or completed the CTA)
- **Uncelebrated cohort**: Users who reached milestone N but did NOT engage with the celebration (dismissed, never saw it due to flag, or no celebration was configured at that threshold)

Compare 7-day, 14-day, and 30-day retention between these cohorts for each milestone tier. The delta is the celebration's retention lift. Store the baseline delta values — these are what the autonomous optimization loop will try to improve.

### 2. Build the milestone effectiveness dashboard

Using `posthog-dashboards`, create a dashboard with these panels:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Milestone funnel | Funnel chart | Drop-off rate between each milestone tier (1 -> 10 -> 50 -> 100 -> 500) |
| Celebration engagement rate by tier | Bar chart | What percentage of users who hit each milestone engage with the celebration |
| Retention lift by milestone | Line chart (trend) | Weekly trend of retention delta between celebrated and uncelebrated cohorts |
| CTA conversion by milestone | Bar chart | What percentage of celebration-engaged users complete the CTA (referral, upgrade, next feature) |
| Milestone velocity | Line chart | Median days between successive milestones — accelerating means habits are forming |
| Churned-despite-milestone | Table | Users who hit milestone N but churned within 30 days — these are the most informative failures |
| Celebration fatigue index | Line chart | Engagement rate for the same user across successive milestones — declining means fatigue |

### 3. Create the decay detection workflow

Using `n8n-scheduling`, build a weekly workflow:

1. Query PostHog for the celebration engagement rate for each milestone tier over the last 4 weeks
2. Compare against the 8-week rolling average
3. Use `posthog-anomaly-detection` to classify: **stable** (within +/-5%), **decaying** (3+ weeks of decline totaling >10%), **spiking** (>20% increase — indicates a recent change is working)
4. If decay detected on any tier: log the tier, decay magnitude, and affected user count to Attio using `attio-notes`
5. If decay exceeds 15% on any tier: trigger an alert via n8n for the autonomous optimization loop to prioritize this tier

### 4. Build the churned-despite-milestone analysis

Using `posthog-cohorts`, create a rolling cohort of users who:
- Reached at least milestone tier 2 (10+ actions) in the last 60 days
- Have not logged in for 14+ days
- Were previously active (logged in at least 3 of the 4 weeks before going silent)

This cohort represents the highest-value churn prevention targets — they demonstrated investment in the product but still left. For each user in this cohort, pull:
- Which milestones they reached
- Whether they engaged with celebrations
- Which CTA they were shown at their last milestone
- Their last 5 sessions (via PostHog session recording references)

Store this analysis in Attio as a note on the contact. This data feeds both manual outreach and the autonomous optimization loop's hypothesis generation.

### 5. Track celebration fatigue

Using `posthog-custom-events`, calculate per-user engagement rate across their milestone journey. If a user engaged with their first 3 milestone celebrations but dismissed the last 2, that signals fatigue. Create a `celebration_fatigue_score` person property in PostHog:

- Score = (celebrations dismissed or ignored) / (total celebrations shown)
- High fatigue (>0.5): User is tuning out celebrations — vary format or reduce frequency
- Low fatigue (<0.2): Celebrations are still working — maintain current approach

Surface fatigue scores in the dashboard and in the autonomous optimization loop's context data.

## Output

- Milestone-retention cohort comparisons with quantified retention lift per tier
- 7-panel effectiveness dashboard in PostHog
- Weekly decay detection workflow in n8n with Attio logging
- Churned-despite-milestone analysis cohort and per-user data
- Celebration fatigue scoring on PostHog person properties

## Triggers

Decay detection runs weekly via n8n cron. The dashboard is reviewed weekly. The churned-despite-milestone cohort is refreshed daily. Re-run full setup when adding new milestone tiers or changing celebration formats.
