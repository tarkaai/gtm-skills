---
name: deprecation-communication-setup
description: Build the multi-channel deprecation notification system with tiered messaging, in-app banners, and email sequences segmented by user dependency
category: Product Ops
tools:
  - Intercom
  - Loops
  - PostHog
fundamentals:
  - intercom-in-app-messages
  - intercom-product-tours
  - loops-sequences
  - loops-broadcasts
  - posthog-feature-flags
  - posthog-custom-events
---

# Deprecation Communication Setup

This drill builds the communication system that notifies affected users about a feature deprecation. It does not blast a generic email to everyone. Instead, it delivers segmented, tiered messages through in-app and email channels, calibrated to each user's dependency level on the deprecated feature.

## Input

- Completed deprecation impact assessment (cohorts by dependency tier, deprecation brief)
- Replacement feature or migration path defined
- Deprecation timeline (sunset date)
- PostHog cohorts: `deprecation-blast-radius-{feature_slug}` and per-tier sub-cohorts

## Steps

### 1. Design message templates per tier

Each dependency tier gets a different message. The higher the dependency, the more personal, detailed, and supportive the message:

**Critical tier (power dependents):**
- Channel: In-app banner (persistent) + dedicated email sequence (3 emails) + Intercom product tour for migration
- Tone: Direct, empathetic, supportive. Acknowledge that this feature is central to their workflow.
- Content: Why the feature is being deprecated, exact sunset date, step-by-step migration guide, link to migration tool/wizard, offer of 1:1 migration help session (Cal.com link), feedback channel
- Timing: 90+ days before sunset

**High tier (regular dependents):**
- Channel: In-app banner + email sequence (2 emails)
- Tone: Informative and helpful
- Content: What is changing, sunset date, migration guide link, self-serve migration tool link
- Timing: 60+ days before sunset

**Medium tier (occasional users):**
- Channel: In-app tooltip on the deprecated feature + single email
- Tone: Brief and clear
- Content: What is changing, sunset date, link to replacement feature
- Timing: 30+ days before sunset

**Low tier (lapsed users):**
- Channel: Single email only
- Tone: FYI
- Content: Feature being removed on X date, link to replacement if they return
- Timing: 30 days before sunset

### 2. Build in-app deprecation banners

Using the `intercom-in-app-messages` fundamental, create in-app messages targeted to each PostHog cohort:

For critical/high tiers: a persistent banner at the top of the deprecated feature's page. The banner shows:
- "This feature will be retired on {sunset_date}. [Migrate now] [Learn more]"
- A progress indicator if they have started migration: "3 of 7 workflows migrated"
- Dismiss button that snoozes for 7 days (not permanent dismiss — they need the reminder)

For medium tier: a tooltip that appears once when the user next accesses the deprecated feature. Dismissable after viewing.

Using `posthog-feature-flags`, gate the banners so they only appear for users in the relevant cohorts.

### 3. Build the migration product tour

Using the `intercom-product-tours` fundamental, create a guided tour for critical-tier users. The tour walks through:

1. Where to find the replacement feature
2. How to recreate their most common workflow using the replacement
3. How to export/migrate their data from the old feature
4. How to verify the migration is complete

Target the tour to the critical-tier PostHog cohort. Trigger it when a critical-tier user clicks "Migrate now" from the deprecation banner.

### 4. Build email sequences in Loops

Using the `loops-sequences` fundamental, create sequences for critical and high tiers:

**Critical tier sequence (3 emails over 90 days):**
- Email 1 (Day 0): Announcement. Why, when, what to do. Migration guide attached. Cal.com link for 1:1 help.
- Email 2 (Day 30): Progress check. "Have you started migrating? Here's what other users found helpful." Include usage data showing their dependency.
- Email 3 (Day 60): Urgency. "30 days until sunset. {X} of your workflows still use this feature." Direct link to migration wizard.

**High tier sequence (2 emails over 60 days):**
- Email 1 (Day 0): Announcement. What, when, how to migrate.
- Email 2 (Day 30): Reminder with migration link.

Using `loops-broadcasts`, send single emails to medium and low tiers.

### 5. Track communication engagement

Using `posthog-custom-events`, instrument every touchpoint:

```javascript
posthog.capture('deprecation_notice_shown', {
  feature_slug: '{feature_slug}',
  channel: 'in_app_banner',
  tier: 'critical',
  days_to_sunset: daysRemaining
});

posthog.capture('deprecation_notice_clicked', {
  feature_slug: '{feature_slug}',
  channel: 'in_app_banner',
  tier: 'critical',
  cta: 'migrate_now'
});

posthog.capture('migration_tour_started', {
  feature_slug: '{feature_slug}',
  tier: 'critical'
});

posthog.capture('migration_tour_completed', {
  feature_slug: '{feature_slug}',
  tier: 'critical'
});
```

### 6. Build the communication dashboard

Create a PostHog insight tracking:
- Notices shown vs. clicked by tier and channel
- Migration tour start vs. completion rate
- Email open and click rates by sequence step
- Days remaining to sunset vs. migration completion percentage

This dashboard is the primary view for monitoring whether communication is driving migration.

## Output

- Tier-segmented in-app deprecation banners in Intercom
- Guided migration product tour for critical-tier users
- Email sequences in Loops (3-email for critical, 2-email for high, single for medium/low)
- PostHog events tracking every communication touchpoint
- Communication engagement dashboard

## Triggers

Activate all channels simultaneously at the start of the deprecation timeline. The in-app banners persist until the user completes migration or the feature is sunset. Email sequences run on their own cadence. Re-evaluate if migration rates are below 50% at the halfway point.
