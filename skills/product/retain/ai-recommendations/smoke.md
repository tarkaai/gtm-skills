---
name: ai-recommendations-smoke
description: >
  AI-Powered Recommendations — Smoke Test. Build a minimal AI recommendation engine
  that analyzes user behavior via PostHog and surfaces contextual feature-discovery
  suggestions through Intercom. Run once on 10-20 users and measure adoption rate.
stage: "Product > Retain"
motion: "LeadCaptureSurface"
channels: "Product"
level: "Smoke Test"
time: "6 hours over 1 week"
outcome: ">=35% recommendation adoption rate (users who try the recommended feature within 7 days)"
kpis: ["Recommendation adoption rate", "Recommendation CTR", "Dismissal rate", "Feature discovery events"]
slug: "ai-recommendations"
install: "npx gtm-skills add product/retain/ai-recommendations"
drills:
  - threshold-engine
---

# AI-Powered Recommendations — Smoke Test

> **Stage:** Product > Retain | **Motion:** LeadCaptureSurface | **Channels:** Product

## Outcomes

Prove that AI-generated feature recommendations drive measurable engagement. A single batch of Claude-generated suggestions delivered via Intercom produces >=35% adoption rate among the test group. Adoption means the user actually uses the recommended feature within 7 days of seeing the recommendation.

## Leading Indicators

- Recommendation CTR > 20% (users click through to the feature)
- Dismissal rate < 40% (users are reading the suggestion before deciding)
- At least 3 distinct features recommended across the test group (model is not fixated on one feature)
- Time to adoption < 3 days for the majority of adopters

## Instructions

### 1. Build the recommendation engine prototype

Run the the recommendation engine prototype workflow (see instructions below) drill:

1. Create a feature catalog documenting 10-20 product features the AI can recommend, including the PostHog event that proves usage, the prerequisite behavior, and the quantified benefit.
2. For 10-20 active users, pull their behavior data from PostHog: last 50 events, feature usage counts, and any repeated action patterns.
3. Build a power-user benchmark by aggregating the top 20% of users by feature breadth.
4. Call the `ai-workflow-recommendation` fundamental for each user to generate 3 ranked suggestions.

**Human action required:** Review every generated suggestion before delivery. Reject suggestions that recommend a feature the user already uses, recommend a feature outside their plan, or provide a benefit claim that is not credible. Expect to reject 20-30% of output.

### 2. Deliver recommendations

From the the recommendation engine prototype workflow (see instructions below) drill output, deliver the top-ranked approved suggestion to each user via Intercom in-app message:

- Format: non-blocking banner or tooltip, not a modal
- Content: feature name, one-sentence benefit, quantified impact based on their actual usage
- CTA: "Try it now" deep-linking to the feature
- Show once per user, do not repeat if dismissed

### 3. Instrument tracking

Ensure PostHog captures the full recommendation lifecycle:

- `recommendation_shown` with properties: user_id, recommendation_id, feature_name, source: "ai"
- `recommendation_clicked` with same properties
- `recommendation_adopted` with days_to_adopt
- `recommendation_dismissed` with properties

### 4. Evaluate against threshold

Run the `threshold-engine` drill after 7 days. Measure:

- **Primary**: adoption rate = users who used the recommended feature / users who saw the recommendation. Pass threshold: >=35%.
- **Secondary**: CTR, dismissal rate, which features had highest adoption.

If PASS: document which features and framings drove the highest adoption. Proceed to Baseline.
If FAIL: analyze dismissals and non-adopters. Common failure modes: recommendations too obvious (user already knew about the feature), recommendations too irrelevant (wrong audience), or benefit not compelling enough. Adjust the feature catalog and prompt, then re-run.

## Time Estimate

- 2 hours: feature catalog creation and behavior data extraction
- 1 hour: AI recommendation generation and manual review
- 1 hour: Intercom message setup and PostHog event instrumentation
- 2 hours: monitoring over 7 days and threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | User behavior tracking, event capture, cohort analysis | Free tier: 1M events/mo; Paid: from $0 (usage-based) — [posthog.com/pricing](https://posthog.com/pricing) |
| Anthropic Claude API | Generate personalized recommendations from behavior data | Sonnet 4.6: $3/$15 per 1M input/output tokens; ~$0.50 for 20 users — [platform.claude.com/docs/en/about-claude/pricing](https://platform.claude.com/docs/en/about-claude/pricing) |
| Intercom | Deliver in-app recommendation messages | Essential: $29/seat/mo; Early Stage: up to 90% off — [intercom.com/pricing](https://intercom.com/pricing) |

**Play-specific cost:** Free (PostHog free tier + minimal Claude API usage + existing Intercom seat)

## Drills Referenced

- the recommendation engine prototype workflow (see instructions below) — builds the feature catalog, generates AI recommendations from user behavior, and delivers them via Intercom
- `threshold-engine` — evaluates adoption rate against the >=35% pass threshold and recommends next action
