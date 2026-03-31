---
name: feature-spotlight-series-smoke
description: >
  Weekly Feature Spotlights — Smoke Test. Produce and deliver one feature spotlight to a
  targeted user segment to validate that highlighting underused features drives measurable
  discovery and trial.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥20% of targeted users try the spotlighted feature within 7 days"
kpis: ["Spotlight open rate", "Spotlight click-through rate", "Feature trial rate", "7-day feature retention"]
slug: "feature-spotlight-series"
install: "npx gtm-skills add product/retain/feature-spotlight-series"
drills:
  - feature-readiness-gating
  - feature-announcement
  - threshold-engine
---

# Weekly Feature Spotlights — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

20% or more of the targeted user segment tries the spotlighted feature within 7 days of receiving the spotlight. "Try" means the user performed the feature's primary action at least once. This proves that targeted feature highlights can move the needle on discovery — users are not finding the feature on their own, but a well-timed spotlight gets them to try it.

## Leading Indicators

- Spotlight message impressions — users actually saw the in-app message or opened the email
- Click-through rate on the spotlight CTA (>10% indicates the value proposition resonates)
- Feature page or feature area visits within 24 hours of spotlight delivery
- Time from spotlight delivery to first feature use (shorter means the content was compelling)

## Instructions

### 1. Select the feature to spotlight

Run the `feature-readiness-gating` drill to audit your product's features and identify the best candidate for the first spotlight. Pick one feature that:

- Has clear value for existing users but low current adoption (<30% of active users have used it in the last 30 days)
- Can be tried independently — the user does not need to complete a complex prerequisite workflow first
- Has PostHog events already tracking its usage (`feature_used` with `feature: "{name}"` property), or instrument them now using `posthog-custom-events`
- Has a concrete, describable benefit (not just "we have this feature" but "you can do [specific outcome] with this")

Define what "tried" means: the specific PostHog event that fires when a user performs the feature's core action for the first time.

### 2. Build the target audience

Query PostHog for active users (session in the last 14 days) who have NOT used this feature in the last 60 days. From this group, prioritize users who actively use a related feature — they are most likely to find value in the spotlighted feature.

For the Smoke test, select a small group: 30-50 users from this segment. Do not target the entire base yet.

### 3. Create and deliver the spotlight

Run the `feature-announcement` drill to produce the spotlight content and deliver it through two channels:

**In-app message via Intercom:**
- Format: Banner or card (not a modal — informative, not interruptive)
- Headline: Lead with the benefit, not the feature name. "Did you know you can [specific outcome]?" or "[Specific outcome] in [time/clicks]"
- Body: One sentence on the problem this solves, one sentence on how it works, one concrete example
- CTA: Deep link directly into the feature (not to a help article)
- Tracking: Fire PostHog events `spotlight_delivered`, `spotlight_clicked`

**Follow-up email via Loops** (48 hours later, only to users who did not engage with the in-app message):
- Subject: The same benefit-led headline
- Body: The same content plus a screenshot or GIF showing the feature in action
- CTA: Deep link to the feature with UTM `utm_source=spotlight&utm_medium=email&utm_campaign={feature-slug}`

**Human action required:** Review the message copy, targeting criteria, and deep link before launching. Verify the deep link takes users directly to the feature. Launch to the 30-50 user test group.

### 4. Track behavior for 7 days

Monitor PostHog daily:

- How many users saw the in-app spotlight (`spotlight_delivered` with `channel: "in-app"`)
- How many clicked through (`spotlight_clicked`)
- How many used the feature for the first time (`feature_used` where user had no prior usage)
- How many opened the follow-up email (`spotlight_delivered` with `channel: "email"`)
- What users did after trying the feature (session recordings for qualitative insight on whether they found it valuable)

Log drop-off points: if users click the CTA but do not complete the feature action, the feature has a UX problem that no spotlight will fix. Flag for product team.

### 5. Evaluate against threshold

Run the `threshold-engine` drill to measure against: 20% of targeted users tried the feature within 7 days.

- **Pass (>=20%):** The spotlight format works. Users respond to targeted feature highlights. Proceed to Baseline to prove this holds as an ongoing series with always-on automation.
- **Fail (<20%):** Diagnose where users dropped off. Was the message delivered? (Check impression rate.) Did users click? (Check CTR.) Did users who clicked actually try the feature? (Check conversion after click.) Fix the weakest step. Consider: wrong feature choice, weak value proposition, or broken deep link. Re-run with a different feature or revised content.

## Time Estimate

- 1 hour: Feature selection, adoption event verification, target segment definition
- 2 hours: Spotlight content creation, Intercom and Loops setup, deep link verification
- 1 hour: Human review, launch, and initial monitoring
- 1 hour: 7-day analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Feature usage tracking, cohort analysis, session recordings | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app spotlight message delivery | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Follow-up email for non-engagers | Free up to 1,000 contacts — https://loops.so/pricing |

**Play-specific cost:** Free (uses existing stack)

## Drills Referenced

- `feature-readiness-gating` — identify which feature to spotlight and define what "tried" means
- `feature-announcement` — produce and deliver the spotlight content via in-app and email
- `threshold-engine` — evaluate 7-day trial rate against the 20% threshold
