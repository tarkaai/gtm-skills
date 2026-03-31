---
name: deprecation-migration-tracker
description: Track per-user migration progress from deprecated feature to replacement, score completion, and route stalled users to intervention workflows
category: Product Ops
tools:
  - PostHog
  - n8n
  - Attio
  - Intercom
fundamentals:
  - posthog-funnels
  - posthog-cohorts
  - posthog-custom-events
  - posthog-dashboards
  - n8n-scheduling
  - n8n-triggers
  - attio-custom-attributes
  - attio-contacts
  - intercom-in-app-messages
---

# Deprecation Migration Tracker

This drill builds the always-on system that tracks whether affected users are actually migrating from the deprecated feature to its replacement. It scores each user's migration completeness, detects stalls, and routes incomplete migrations to intervention workflows. Without this, you are flying blind — sending deprecation notices but not knowing if anyone is acting on them.

## Input

- Deprecation impact assessment completed (user cohorts by tier)
- Deprecation communication active (notices being shown)
- Replacement feature defined with known PostHog events
- Migration steps defined (what a user needs to do to be "fully migrated")

## Steps

### 1. Define migration milestones

Break the migration into discrete, trackable steps. Every feature deprecation has its own milestones, but a common pattern:

| Milestone | PostHog Event | Weight |
|-----------|--------------|--------|
| Saw deprecation notice | `deprecation_notice_shown` | 0% (awareness only) |
| Clicked migration CTA | `deprecation_notice_clicked` | 10% |
| First use of replacement feature | `replacement_feature_first_use` | 30% |
| Recreated primary workflow in replacement | `replacement_workflow_created` | 60% |
| Zero usage of deprecated feature for 7 days | `deprecated_feature_inactive_7d` | 90% |
| Confirmed migration complete (explicit opt-in or 14 days inactive on old) | `migration_confirmed` | 100% |

Using `posthog-custom-events`, ensure all milestone events are being emitted by the product.

### 2. Build the migration funnel

Using `posthog-funnels`, create a funnel from the milestones above. Break down by:
- Dependency tier (critical, high, medium, low)
- User plan type
- Signup cohort (week)

This funnel shows where users are getting stuck in the migration process.

### 3. Compute per-user migration scores

Using `n8n-scheduling`, create a daily workflow that:

1. Queries PostHog for all users in the deprecation cohort
2. For each user, checks which milestones they have completed
3. Assigns a migration score (0-100) based on the highest milestone reached
4. Classifies migration status:
   - **Not started (0%):** Has not clicked any migration CTA
   - **Aware (10%):** Clicked CTA but has not used the replacement
   - **In progress (30-60%):** Started using replacement but not fully migrated
   - **Nearly complete (90%):** Stopped using deprecated feature but not yet confirmed
   - **Complete (100%):** Fully migrated
5. Using `attio-custom-attributes`, update each user's record with: `migration_score`, `migration_status`, `migration_last_updated`

### 4. Detect stalled migrations

Within the daily workflow, flag users who are stalled:

- **Stalled at Aware:** Clicked CTA 7+ days ago but never used replacement. They may not understand the migration path.
- **Stalled at In Progress:** Started replacement 14+ days ago but migration score has not increased. They may be blocked on a specific step.
- **Regressed:** Was in progress but went back to using the deprecated feature exclusively. The replacement is not meeting their needs.

Using `posthog-cohorts`, create dynamic cohorts: `migration-stalled-aware`, `migration-stalled-inprogress`, `migration-regressed`.

### 5. Route stalled users to interventions

Using `n8n-triggers`, fire webhooks when users enter stalled cohorts:

- **Stalled at Aware:** Use `intercom-in-app-messages` to show a contextual guide: "Need help migrating? Here's a 2-minute walkthrough." Link to the migration product tour.
- **Stalled at In Progress:** Trigger a targeted Loops email with the specific step they are stuck on (infer from which milestones they have and have not completed).
- **Regressed:** Flag in Attio using `attio-contacts` for personal outreach. These users tried the replacement and rejected it — this is critical feedback.

### 6. Build the migration dashboard

Using `posthog-dashboards`, create a dashboard with:

| Panel | Visualization | Purpose |
|-------|--------------|---------|
| Overall migration progress | Stacked bar (by status) | How many users at each migration stage |
| Migration by tier | Grouped bar chart | Are critical-tier users migrating faster or slower? |
| Migration velocity | Line chart (daily) | Is migration accelerating or decelerating? |
| Stalled users | Table with counts | How many stalled at each stage |
| Days to sunset countdown | Single number | Urgency context |
| Projected completion at sunset | Percentage | At current velocity, what % will be migrated by sunset? |

Set alerts:
- Projected completion below 80% at 30 days to sunset
- Critical-tier migration below 70% at 60 days to sunset
- Stalled user count exceeding 30% of any tier

### 7. Generate weekly migration reports

Using the daily data, compile a weekly report:
- Migration progress: X% complete across all tiers (up/down Y% from last week)
- Stalled users: X new stalls detected, Y resolved via intervention
- Projected completion at sunset: X%
- Risk flags: any tier significantly behind target
- Top blockers: most common stall points from funnel analysis

Store the report as an Attio note. If projected completion is below 80%, recommend action: extend sunset date, increase communication frequency, or add migration incentives.

## Output

- Daily per-user migration scoring running in n8n
- Migration funnel in PostHog with tier breakdowns
- Stalled-user detection with automatic intervention routing
- Migration dashboard with 6 panels and threshold alerts
- Weekly migration progress reports stored in Attio

## Triggers

Runs daily via n8n cron from the day deprecation is announced until 30 days after sunset (to catch late migrants). Weekly reports generated every Monday.
