---
name: push-notification-engagement-baseline
description: >
  Push Notification Strategy — Baseline Run. Deploy always-on push notification
  campaigns with behavioral segmentation, automated triggers, and continuous
  performance tracking across 200+ subscribers.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Baseline Run"
time: "16 hours over 2 weeks"
outcome: "≥35% CTR across 200+ subscribers, ≥15pp DAU lift on push-send days"
kpis: ["Push CTR", "Opt-in rate", "DAU lift"]
slug: "push-notification-engagement"
install: "npx gtm-skills add product/retain/push-notification-engagement"
drills:
  - posthog-gtm-events
---

# Push Notification Strategy — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes
Multiple always-on push notification campaigns running continuously across 200+ subscribers. CTR across all campaigns averages 35% or higher. DAU on push-send days is at least 15 percentage points higher than non-push days for the subscriber cohort. Opt-out rate stays below 1% per week.

## Leading Indicators
- Subscriber count growing week-over-week (net positive: new subscriptions minus unsubscribes)
- Event-triggered pushes fire within 60 seconds of the triggering event
- Scheduled pushes deliver at the configured timezone-adjusted time
- Per-campaign CTR is trackable in PostHog (not just aggregate)
- At-risk users receiving re-engagement pushes return within 48 hours at >20% rate

## Instructions

### 1. Expand event tracking
Run the `posthog-gtm-events` drill to set up the full push event taxonomy. Beyond the basic lifecycle events from Smoke, add:
- `push_campaign_type`: attach to every push event (habit, time_sensitive, re_engagement, value_delivery)
- `push_segment`: which segment the user belongs to
- `push_downstream_action`: did the user perform the intended action within 30 minutes of clicking?
- Build PostHog funnels: `push_sent` -> `push_delivered` -> `push_clicked` -> `push_downstream_action` per campaign type

### 2. Build behavioral segments
Run the the push notification segmentation workflow (see instructions below) drill. Create at least 4 segments based on engagement level:
- **Regular users** (2-4 sessions/week): habit reinforcement pushes
- **Casual users** (1 session/week or less): value highlight pushes
- **At-risk users** (was regular, no session in 7+ days): re-engagement pushes
- **New users** (account < 14 days): onboarding guidance pushes

Set up the n8n sync workflow to update OneSignal tags from PostHog cohorts every 4 hours.

### 3. Launch 4 always-on campaigns
Run the the push notification campaign workflow (see instructions below) drill to configure and launch one campaign per segment:

**Campaign 1 — Session Reminder (Regular users):**
Trigger: User has not opened the app today AND it is their peak-activity hour. Copy: personalized with their most-used feature or pending items. Frequency: max 1/day.

**Campaign 2 — Value Digest (Casual users):**
Trigger: Weekly, on the day they historically opened most often. Copy: summarize what happened in the product that week relevant to them. Frequency: 1/week.

**Campaign 3 — Re-engagement (At-risk users):**
Trigger: 3 days since last session for a user who previously averaged 3+ sessions/week. Copy: highlight what they are missing (teammate activity, new features, saved progress). Frequency: 1 per re-engagement attempt, max 2 attempts before stopping.

**Campaign 4 — Onboarding Nudge (New users):**
Trigger: User completed signup but has not completed the next setup step within 24 hours. Copy: guide to the specific next step with a direct deep link. Frequency: 1 per setup step, max 3 total.

### 4. Set frequency caps
Configure in n8n: no user receives more than 2 pushes per day across all campaigns. Enforce quiet hours (9 PM - 8 AM local time). Track `push_dismissed` events — if a user dismisses 5 consecutive pushes, auto-reduce their frequency to 1/week for 14 days.

### 5. Measure against threshold
After 2 weeks, evaluate:
- **Overall CTR**: `push_clicked / push_delivered` across all campaigns — target ≥35%
- **DAU lift**: Compare subscriber DAU on push-send days vs non-push days — target ≥15pp
- **Opt-out rate**: `push_unsubscribed` per week — must stay below 1%
- **Per-campaign CTR**: Identify which campaign type performs best and worst

If overall CTR is below 35%, analyze per-campaign performance. Kill campaigns with CTR below 15%. Double down on the highest-performing campaign type by adding variants.

## Time Estimate
- 3 hours: Expand event tracking and build PostHog funnels
- 4 hours: Build segments in PostHog and configure OneSignal tag sync
- 5 hours: Design, configure, and launch 4 campaigns with n8n automation
- 2 hours: Configure frequency caps, quiet hours, and fatigue detection
- 2 hours: Two-week review, per-campaign analysis, pass/fail decision

## Tools & Pricing
| Tool | Purpose | Pricing |
|------|---------|---------|
| OneSignal | Push delivery, segmentation, timezone send | Free tier (sufficient for 200+ subscribers) |
| PostHog | Event tracking, cohorts, funnels | Standard stack — excluded |
| n8n | Campaign automation, segment sync, frequency caps | Standard stack — excluded |

## Drills Referenced
- the push notification campaign workflow (see instructions below) — design and launch 4 always-on campaigns with behavioral triggers
- the push notification segmentation workflow (see instructions below) — build engagement-level segments and sync to OneSignal
- `posthog-gtm-events` — implement the full push event taxonomy and funnels
