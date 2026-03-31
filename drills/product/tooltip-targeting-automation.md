---
name: tooltip-targeting-automation
description: Automate tooltip delivery across user segments using usage-based triggers, feature-gap analysis, and personalized targeting rules
category: Product
tools:
  - PostHog
  - Intercom
  - n8n
fundamentals:
  - posthog-cohorts
  - posthog-custom-events
  - posthog-funnels
  - intercom-in-app-messages
  - intercom-user-properties
  - n8n-workflow-basics
  - n8n-scheduling
  - n8n-triggers
---

# Tooltip Targeting Automation

This drill builds the system that decides WHICH tooltip to show to WHICH user at WHAT moment. Instead of showing the same tooltip to everyone, it uses product usage data to identify each user's feature gap -- the features they would benefit from but have not discovered -- and surfaces the right tooltip at the right time.

## Input

- PostHog tracking tooltip impressions, clicks, dismissals, and downstream feature usage
- Intercom configured with user properties reflecting feature usage state
- At least 2 weeks of tooltip performance data from the Baseline level
- n8n instance for scheduling the targeting pipeline

## Steps

### 1. Build the feature usage matrix

Using `posthog-custom-events`, query each user's feature usage pattern. For every feature in your product, determine whether the user has: never seen it, seen but not tried, tried once, or uses regularly.

Create a PostHog insight that maps feature usage frequency per user cohort:

```
Event: feature_used
Breakdown: feature_name
Filter: distinct_id = {user_id}
Date range: last 30 days
```

Export this data per user. The features a user has NOT used but similar users HAVE used represent the feature gap -- these are the tooltip targets.

### 2. Define tooltip eligibility rules

Using `posthog-cohorts`, create cohorts for each tooltip target. A user is eligible for a feature tooltip when ALL of the following are true:

- The user has NOT used the target feature in the last 30 days
- The user HAS used at least 2 prerequisite features (features that logically precede the target)
- The user has been active in the last 7 days (do not tooltip dormant users -- that is a winback problem)
- The user has NOT been shown a tooltip in the last 48 hours (frequency cap)
- The user has NOT dismissed this specific tooltip before

Create one cohort per feature tooltip. Name them: `tooltip-eligible-{feature-name}`.

### 3. Build the targeting pipeline in n8n

Using `n8n-scheduling`, create a daily workflow that:

1. Queries PostHog for users in each tooltip-eligible cohort
2. Ranks features by predicted impact for each user (features used by similar users rank higher)
3. Selects the single highest-priority tooltip per user (never queue multiple)
4. Updates the user's Intercom properties using `intercom-user-properties`:
   ```
   PUT /contacts/{id}
   {
     "custom_attributes": {
       "next_tooltip_feature": "csv-export",
       "tooltip_priority_score": 85,
       "tooltip_eligible_since": "2025-03-15"
     }
   }
   ```

### 4. Configure trigger-based delivery in Intercom

Using `intercom-in-app-messages`, create tooltip messages that fire based on the targeting data:

- **Trigger condition**: `next_tooltip_feature` equals `{feature-name}` AND user visits a page where the feature is accessible
- **Display type**: Tooltip pointing at the feature's UI element (CSS selector)
- **Content**: One sentence explaining the benefit (not the feature name). Example: "Export this view as a spreadsheet in one click" not "CSV Export feature"
- **CTA**: "Try it" linking directly to the feature action
- **Dismiss behavior**: On dismiss, fire `tooltip_dismissed` event with feature name. Clear `next_tooltip_feature` in Intercom. Do not show again.

### 5. Implement the feedback loop

Using `n8n-triggers`, create a workflow triggered by PostHog webhook when a user completes `tooltip_cta_clicked` or `tooltip_dismissed`:

- On click: record conversion in PostHog, clear the tooltip from Intercom, wait 48 hours, then recalculate the user's next best tooltip
- On dismiss: record dismissal, blacklist this feature tooltip for this user, wait 48 hours, then offer the next-ranked feature
- On feature adoption (user returns to the feature 3+ times in 7 days): record as sustained adoption, update the user's feature usage matrix

### 6. Scale across segments

Using `posthog-cohorts`, create macro segments that share tooltip strategies:

- **New users (0-14 days)**: Prioritize core features. Show tooltips for features that correlate with activation.
- **Established users (14-60 days)**: Prioritize intermediate features. Show tooltips for features that correlate with retention.
- **Power users (60+ days)**: Prioritize advanced features. Show tooltips for features that correlate with expansion/upsell.

Each segment gets different tooltip content, timing, and frequency. New users get tooltips on first visit to a relevant page. Established users get tooltips after completing a related workflow. Power users get tooltips contextually when they hit a limitation the advanced feature solves.

## Output

- Feature usage matrix per user in PostHog
- Tooltip eligibility cohorts per feature
- Daily n8n pipeline selecting the best tooltip per user
- Intercom in-app tooltips with trigger-based delivery
- Feedback loop updating targeting after every interaction
- Segment-specific tooltip strategies

## Triggers

The targeting pipeline runs daily via n8n cron. The feedback loop triggers in real-time on tooltip interactions. Re-run the full setup when adding new features or changing the feature hierarchy.
