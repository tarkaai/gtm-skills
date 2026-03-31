---
name: feature-announcement-campaign-baseline
description: >
  New Feature Announcements — Baseline Run. Always-on announcement pipeline that
  triggers coordinated in-app and email campaigns for every feature release. Tracks
  adoption funnels by channel and segment to establish performance baselines.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Baseline Run"
time: "16 hours over 4 weeks"
outcome: "≥30% feature trial rate AND ≥15% 7-day feature retention across 3+ consecutive announcements"
kpis: ["Feature trial rate", "7-day feature retention", "Channel click-through rate", "Announcement-to-adoption funnel conversion"]
slug: "feature-announcement-campaign"
install: "npx gtm-skills add product/retain/feature-announcement-campaign"
drills:
  - posthog-gtm-events
  - feature-announcement
  - feature-adoption-monitor
---

# New Feature Announcements — Baseline Run

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

Announcement pipeline runs continuously: every feature release triggers a coordinated in-app + email campaign. At least 30% feature trial rate and 15% 7-day retention rate sustained across 3 or more consecutive announcements. Channel-level and segment-level baselines established.

## Leading Indicators

- Event taxonomy fully deployed (all announcement events flowing into PostHog)
- Per-announcement funnel data available within 48 hours of launch
- Adoption funnel showing consistent shape across multiple announcements
- Channel attribution data showing which surface drives the most retained usage

## Instructions

### 1. Deploy the announcement event taxonomy

Run the `posthog-gtm-events` drill to establish standardized tracking for the announcement pipeline. Configure these events:

- `announcement_shown` — properties: `feature_slug`, `channel` (in-app|email|blog), `segment`, `tier` (major|notable|minor)
- `announcement_clicked` — properties: `feature_slug`, `channel`, `cta_text`
- `feature_first_used` — properties: `feature_slug`, `source` (announcement|organic|other)
- `feature_retained_7d` — properties: `feature_slug`, `usage_count`
- `feature_retained_30d` — properties: `feature_slug`, `usage_count`

Build a PostHog funnel: `announcement_shown` -> `announcement_clicked` -> `feature_first_used` -> `feature_retained_7d`. Break down by channel and segment.

### 2. Run announcements for 3+ features

For each new feature release, run the `feature-announcement` drill:
- Classify the feature tier (major, notable, minor)
- Write segment-specific copy — power users get technical details, newer users get benefit-first messaging
- Deploy Intercom in-app message targeting the relevant segment
- Send Loops email to the same segment, timed for the same day as the in-app activation
- Track all events with the standardized taxonomy from Step 1

Run at least 3 announcements over the 4-week period to generate enough data for baselines.

### 3. Track adoption beyond the announcement

Run the `feature-adoption-monitor` drill to measure what happens after users try the feature:
- Build the adoption funnel from first use through retained usage at 7 and 30 days
- Create the stalled-user detection workflow: users who saw the announcement and clicked but never used the feature
- Configure stalled-user nudges via Intercom (in-app reminder) and Loops (follow-up email with a specific use case)

### 4. Establish channel and segment baselines

After 3+ announcements, calculate baselines:
- In-app click-through rate (target: 15-25%)
- Email click-through rate (target: 8-15%)
- In-app to first-use conversion (target: 40-60%)
- Email to first-use conversion (target: 20-35%)
- 7-day retention by channel (which channel drives stickier adoption?)
- Trial rate by user segment (which segments respond best?)

Store these baselines in Attio as notes on the campaign record. These numbers are the foundation for Scalable-level optimization.

### 5. Evaluate against threshold

Measure against: ≥30% feature trial rate AND ≥15% 7-day feature retention across 3+ consecutive announcements.

If PASS: baselines are established and the pipeline is repeatable. Proceed to Scalable to test variations and expand reach.

If FAIL: identify the bottleneck. If trial is low, the announcement copy or targeting needs work. If retention is low, the feature itself may need better onboarding or the announcement is attracting the wrong users. Fix the weakest link and run 3 more announcements.

## Time Estimate

- 4 hours: event taxonomy setup and PostHog funnel configuration
- 6 hours: running 3+ announcements (2 hours each: copy, setup, launch)
- 4 hours: adoption monitor setup and stalled-user intervention configuration
- 2 hours: baseline calculation, analysis, and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app messages and stalled-user nudges | https://www.intercom.com/pricing — Essential $39/seat/mo |
| Loops | Email announcements and follow-up sequences | https://loops.so/pricing — Starter $49/mo for 5,000 contacts |
| PostHog | Event tracking, funnels, and cohort analysis | https://posthog.com/pricing — Free up to 1M events/mo |
| n8n | Stalled-user detection workflow automation | https://n8n.io/pricing — Free self-hosted |

**Play-specific cost:** ~$50-100/mo (Loops Starter plan if beyond free tier)

## Drills Referenced

- `posthog-gtm-events` — establishes the standard event taxonomy for all announcement tracking
- `feature-announcement` — executes each announcement across in-app and email channels
- `feature-adoption-monitor` — tracks post-announcement adoption, detects stalled users, and triggers re-engagement
