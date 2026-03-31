---
name: feature-announcement-campaign-smoke
description: >
  New Feature Announcements — Smoke Test. Announce a single new feature through
  coordinated in-app messaging and email to a small user segment. Validate that
  the announcement drives measurable feature trial within 7 days.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "4 hours over 1 week"
outcome: "≥25% of notified users try the feature within 7 days"
kpis: ["Announcement click-through rate", "Feature first-use rate", "7-day feature retention"]
slug: "feature-announcement-campaign"
install: "npx gtm-skills add product/retain/feature-announcement-campaign"
drills:
  - feature-announcement
  - threshold-engine
---

# New Feature Announcements — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

25% or more of users who receive the announcement try the announced feature within 7 days. This proves the announcement format, copy approach, and targeting produce measurable behavior change — not just clicks.

## Leading Indicators

- Announcement impression count (are users seeing it?)
- Click-through rate above 15% within 48 hours of launch
- Feature page/screen views from announcement links within 24 hours

## Instructions

### 1. Select the feature and target segment

Pick one recently shipped feature that is stable and beneficial to an identifiable user segment. Define the segment in PostHog: users on a specific plan, users who use a related feature, or users who joined in a specific cohort. Keep the segment small — 50 to 200 users — so you can manually review results.

### 2. Run the `feature-announcement` drill

Execute the full `feature-announcement` drill for this feature:
- Classify the feature as Tier 1 (major) or Tier 2 (notable)
- Write benefit-first announcement copy with a direct CTA linking to the feature
- Create the Intercom in-app message targeting your selected segment
- Send the Loops email announcement to the same segment
- Set up PostHog tracking for `announcement_shown`, `announcement_clicked`, and `feature_first_used`

**Human action required:** Review the announcement copy before it goes live. Ensure the CTA links directly to the feature, not a generic page. Approve the user segment for targeting.

### 3. Observe behavior for 7 days

Monitor PostHog daily for the first 3 days:
- Are users seeing the announcement? (impression count)
- Are they clicking through? (click-through rate)
- Are they using the feature after clicking? (feature_first_used events)

Do not change anything during the observation period. Collect data cleanly.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: ≥25% of notified users tried the feature within 7 days. Count only unique users who triggered `feature_first_used` after `announcement_shown`.

If PASS: the announcement format works. Proceed to Baseline to add tracking infrastructure and segment expansion.

If FAIL: diagnose where the funnel broke. Low impressions means targeting is wrong. Low click-through means copy or placement is wrong. Low usage means the feature itself needs better discoverability or onboarding. Fix the weakest step and re-run.

## Time Estimate

- 1.5 hours: feature selection, segment definition, and copy writing
- 1 hour: Intercom message and Loops email setup
- 0.5 hours: PostHog event tracking configuration
- 1 hour: daily monitoring over 7 days (10-15 min/day) and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| Intercom | In-app announcement messages | https://www.intercom.com/pricing — Essential $39/seat/mo |
| Loops | Email announcement broadcast | https://loops.so/pricing — Free up to 1,000 contacts |
| PostHog | Event tracking and funnel analysis | https://posthog.com/pricing — Free up to 1M events/mo |

**Play-specific cost:** Free (within standard stack free tiers for a small test)

## Drills Referenced

- `feature-announcement` — coordinates the multi-channel announcement: in-app message, email, and blog post with PostHog tracking
- `threshold-engine` — evaluates pass/fail against the 25% trial threshold and recommends next action
