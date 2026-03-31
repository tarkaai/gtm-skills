---
name: feature-adoption-campaign-smoke
description: >
  Targeted Adoption Campaigns — Smoke Test. Run a single feature adoption campaign for one user
  segment to validate that targeted messaging drives measurable feature adoption.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: "≥20% of targeted users adopt the feature within 7 days"
kpis: ["Feature adoption rate", "Campaign engagement rate", "7-day feature retention"]
slug: "feature-adoption-campaign"
install: "npx gtm-skills add product/retain/feature-adoption-campaign"
drills:
  - feature-readiness-gating
  - feature-announcement
  - threshold-engine
---

# Targeted Adoption Campaigns — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product, Email

## Outcomes

20% or more of the targeted user segment adopts the feature within 7 days of receiving the campaign. "Adoption" means the user performed the feature's core action at least once. This proves that targeted messaging can move the needle on feature usage, not just awareness.

## Leading Indicators

- Campaign message impressions (users actually saw the message)
- Click-through rate on the campaign CTA (>10% indicates compelling copy)
- Feature page or feature area visits within 24 hours of message delivery
- Time from message delivery to first feature use (shorter is better)

## Instructions

### 1. Select and gate the target feature

Run the `feature-readiness-gating` drill to identify which feature to target and define what "adoption" means for it. Pick one feature that:
- Has clear value for existing users but low current adoption (<30% of active users)
- Can be used independently (does not require completing a multi-step workflow first)
- Has PostHog events already tracking its usage, or instrument them now

Define the adoption event in PostHog: `feature_first_used` with property `feature: "{feature-name}"`. Define retention as the user performing the same action again 7+ days later.

### 2. Build and deliver the campaign

Run the `feature-announcement` drill to create targeted messaging for one segment. For the Smoke test, pick your highest-likelihood segment: active users who have never used this feature but regularly use a related feature.

Create one in-app message via Intercom targeting this segment. The message must:
- Lead with the specific benefit (not the feature name)
- Include a direct deep link to the feature
- Fire PostHog events: `adoption_campaign_impression`, `adoption_campaign_clicked`

Create one email via Loops targeting the same segment as a follow-up for users who did not engage with the in-app message within 48 hours. Subject line must reference the benefit, not the feature name.

**Human action required:** Review the message copy and targeting criteria before launching. Verify the deep link works. Launch to a small group of 20-50 users from the target segment.

### 3. Track behavior and measure

Monitor PostHog daily for 7 days:
- How many users saw the in-app message (`adoption_campaign_impression`)
- How many clicked through (`adoption_campaign_clicked`)
- How many used the feature for the first time (`feature_first_used`)
- What users did after first use (session recordings for qualitative signal)

Log drop-off points: if users click but do not complete the feature action, the feature itself has a UX problem that no campaign will fix.

### 4. Evaluate against threshold

Run the `threshold-engine` drill to measure against: 20% of targeted users adopted the feature within 7 days.

- **Pass (>=20%):** The campaign works. Proceed to Baseline to prove it holds at scale with always-on automation.
- **Fail (<20%):** Diagnose: Was the message delivered? (Check impression rate.) Did users click? (Check CTR.) Did users who clicked adopt? (Check conversion.) Fix the weakest step and re-run.

## Time Estimate

- 1 hour: Feature selection, adoption event definition, segment definition
- 2 hours: Message copy, Intercom and Loops setup, PostHog event instrumentation
- 1 hour: Human review, launch, and initial monitoring
- 1 hour: 7-day analysis and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Event tracking, funnel analysis, session recordings | Free up to 1M events/mo — https://posthog.com/pricing |
| Intercom | In-app message delivery to targeted segment | Included in existing plan — https://www.intercom.com/pricing |
| Loops | Follow-up email for non-engagers | Free up to 1,000 contacts — https://loops.so/pricing |

**Play-specific cost:** Free (uses existing stack)

## Drills Referenced

- `feature-readiness-gating` — define which feature to target and what adoption means
- `feature-announcement` — build and deliver targeted in-app and email messages
- `threshold-engine` — evaluate 7-day adoption rate against the 20% threshold
