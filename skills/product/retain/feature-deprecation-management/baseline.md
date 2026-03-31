---
name: feature-deprecation-management-baseline
description: >
  Feature Sunset Communication — Baseline Run. Deploy always-on migration tracking
  across all affected users with automated stall detection and intervention routing.
  First full deprecation cycle from announcement to sunset.
stage: "Product > Retain"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥90% migration completion rate AND <5% churn from sunset"
kpis: ["Migration completion rate", "Churn from sunset", "Migration velocity (users/week)", "Stall rate", "Communication engagement by channel"]
slug: "feature-deprecation-management"
install: "npx gtm-skills add product/retain/feature-deprecation-management"
drills:
  - posthog-gtm-events
  - deprecation-communication-setup
---

# Feature Sunset Communication — Baseline Run

> **Stage:** Product → Retain | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Run a complete deprecation cycle — from announcement through sunset — with always-on migration tracking. Every affected user gets tiered communication. Every migration is tracked per-user with milestone scoring. Stalled users are automatically detected and routed to intervention. This is the first time the system runs at full scale across all affected users, not just a test cohort.

## Leading Indicators

- Migration tracker scoring all affected users daily within 48 hours of launch
- Stalled users detected and routed to interventions within 7 days of stalling
- Migration velocity increasing week-over-week for the first 3 weeks
- Communication engagement rate (notice click-through) above 50% across all tiers
- Zero users surprised by the sunset (no "what happened?" support tickets after removal)

## Instructions

### 1. Configure comprehensive event tracking

Run the `posthog-gtm-events` drill to instrument the full deprecation lifecycle. Set up these events:

- `deprecation_notice_shown` — with properties: `feature_slug`, `tier`, `channel`, `days_to_sunset`
- `deprecation_notice_clicked` — with properties: `feature_slug`, `tier`, `channel`, `cta`
- `migration_tour_started` / `migration_tour_completed` — with properties: `feature_slug`, `tier`
- `replacement_feature_first_use` — with properties: `feature_slug`, `source` (organic vs. guided)
- `replacement_workflow_created` — with properties: `feature_slug`, `workflow_type`
- `deprecated_feature_used` — continue tracking usage of the old feature to detect regressions
- `migration_confirmed` — with properties: `feature_slug`, `days_from_announcement`, `tier`

Build PostHog funnels:
- Full migration funnel: notice shown → clicked → replacement first use → workflow created → migration confirmed
- Breakdown by tier, channel, and week

### 2. Deploy the migration tracker

Run the the deprecation migration tracker workflow (see instructions below) drill. This builds the always-on system that:

- Scores every affected user's migration progress daily (0-100%)
- Classifies migration status: not started, aware, in progress, nearly complete, complete
- Detects stalled migrations (aware but not acting for 7+ days, in progress but stuck for 14+ days, regressed to old feature)
- Routes stalled users to interventions automatically
- Generates a migration dashboard with 6 panels: overall progress, progress by tier, velocity trend, stalled users, days-to-sunset countdown, projected completion

The tracker runs as a daily n8n workflow starting from the day communication goes live.

### 3. Activate full-scale communication

Run the `deprecation-communication-setup` drill at full scale (remove the test cohort feature flag restriction from Smoke). All affected users now receive tier-appropriate communication:

- Critical tier: Persistent in-app banner + 3-email sequence + guided migration tour
- High tier: Persistent in-app banner + 2-email sequence
- Medium tier: Tooltip on deprecated feature + single email
- Low tier: Single email notification

The communication setup from Smoke should already be built. At this step, widen the PostHog feature flags to include all affected users and activate the Loops sequences for the full cohorts.

### 4. Monitor and intervene for 2 weeks

Over the 2-week Baseline period, the migration tracker runs daily. Monitor:

- **Week 1 target:** 40%+ of users at "aware" or beyond. If below 30%, communication is not reaching users — check that in-app messages are showing and emails are delivering.
- **Week 2 target:** 60%+ of users at "in progress" or beyond. If stall rate exceeds 30%, the migration path has friction — review the migration funnel to find the drop-off point.

When stalled users are detected, the tracker automatically routes them:
- Stalled at Aware → in-app guide shown
- Stalled at In Progress → targeted email with the specific step they are stuck on
- Regressed → Attio task for account owner for personal outreach

**Human action required:** Review the weekly migration report generated by the tracker. If projected completion is below 80% at the halfway point, decide whether to extend the sunset date, increase communication frequency, or add migration incentives.

### 5. Evaluate against threshold

At the end of 2 weeks (or at the sunset date, whichever comes first), measure:

- **Primary threshold:** ≥90% migration completion rate (users at 100% migration score)
- **Secondary threshold:** <5% churn attributable to the deprecation (users who cancelled or went inactive within 14 days of the sunset, filtered to those who were in the deprecation cohort)

If PASS: The always-on migration system works. Document: which tiers migrated fastest, which interventions had the highest save rate, total cost of the deprecation cycle. Proceed to Scalable.

If FAIL: Identify whether the failure is in communication (users did not know), migration path (users knew but could not migrate), or replacement quality (users tried but reverted). Fix the specific failure and extend the sunset date to re-run.

## Time Estimate

- 3 hours: Event tracking setup and funnel configuration
- 4 hours: Migration tracker deployment and testing
- 2 hours: Full-scale communication activation
- 5 hours: 2-week monitoring, intervention review, and report analysis
- 2 hours: Threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Events, funnels, cohorts, feature flags, dashboards | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app banners, product tours, stall interventions | Essential $29/seat/mo ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Loops | Email sequences and broadcast notifications | Starts at $49/mo ([loops.so/pricing](https://loops.so/pricing)) |
| Attio | Migration scores, account owner tasks, reports | Standard stack — excluded from play budget |
| n8n | Daily migration scoring workflow, stall detection | Standard stack — excluded from play budget |

**Estimated play-specific cost:** $49-78/mo (Loops paid plan for sequence volume + Intercom if not already on a paid seat)

## Drills Referenced

- `posthog-gtm-events` — instruments the full deprecation event lifecycle for tracking and funnel analysis
- the deprecation migration tracker workflow (see instructions below) — scores per-user migration progress daily, detects stalls, routes interventions, and generates migration dashboards
- `deprecation-communication-setup` — deploys tiered in-app and email notifications to all affected users at full scale
