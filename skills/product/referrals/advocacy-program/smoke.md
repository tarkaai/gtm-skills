---
name: advocacy-program-smoke
description: >
  Formal Advocacy Program — Smoke Test. Identify power users, design a tiered advocacy program,
  and recruit 15 advocates manually to prove the model generates referrals.
stage: "Product > Referrals"
motion: "LeadCaptureSurface"
channels: "Product, Email, Events"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=15 enrolled advocates with >=1 advocacy action completed"
kpis: ["Advocate enrollment count", "Time to first advocacy action", "Referral links generated"]
slug: "advocacy-program"
install: "npx gtm-skills add product/referrals/advocacy-program"
drills:
  - power-user-scoring
  - advocacy-program-design
  - threshold-engine
---

# Formal Advocacy Program — Smoke Test

> **Stage:** Product -> Referrals | **Motion:** LeadCaptureSurface | **Channels:** Product, Email, Events

## Outcomes

15 or more users enrolled in the advocacy program with at least 1 advocacy action completed (testimonial submitted, referral link shared, or survey completed). This proves that power users will participate in a structured program and take concrete actions when asked.

## Leading Indicators

- Power user scores computed for all active users (scoring pipeline operational)
- 30+ users identified with score >= 60 (sufficient candidate pool)
- Enrollment invitation open rate >= 40% (program positioning resonates)
- 50%+ of enrolled advocates view their perks page (they care about the benefits)

## Instructions

### 1. Score your user base

Run the `power-user-scoring` drill to compute composite scores for all active users. This builds the scoring pipeline across 5 dimensions (usage depth, tenure/consistency, collaboration signal, expansion signal, sentiment signal) and creates tiered cohorts in PostHog: Champions (score >= 80), Power Users (60-79), Rising Stars (40-59).

Sync scored users to Attio. Create the "Power User Candidates" list filtered to score >= 60.

### 2. Design the advocacy program structure

Run the `advocacy-program-design` drill to produce the complete program specification:

- Define 3 tiers: Insider (score 60-79, automatic enrollment), Advocate (score 80-89, invitation), Ambassador (score 90+, nomination)
- Map benefits per tier: early feature access, roadmap previews, advisory board seats
- Map asks per tier: survey responses, testimonials, referrals, speaking engagements
- Design the PostHog event schema: `advocacy_tier_enrolled`, `advocacy_action_completed`, `advocacy_referral_submitted`, `advocacy_tier_promoted`
- Draft Intercom in-app enrollment celebration messages
- Draft Loops welcome email sequences for each tier

**Human action required:** Review the tier structure and benefits. Confirm the product team can deliver the promised perks (feature flags for early access, roadmap preview calls, etc.). Approve the email copy.

### 3. Instrument advocacy events in PostHog

Using the `posthog-custom-events` fundamental, implement the event schema from step 2. At minimum, instrument:

- `advocacy_tier_enrolled` with properties: tier, power_user_score, enrollment_type
- `advocacy_action_completed` with properties: action_type, tier, reward_issued
- `advocacy_referral_submitted` with properties: referrer_tier, referee_email_domain

### 4. Manually recruit the first cohort

Query Attio for the top 30 users by power user score. For each:

1. Send a personal enrollment invitation via Loops (use the Insider or Advocate welcome email from step 2)
2. Enable the `advocacy-insider-perks` or `advocacy-advocate-perks` feature flag in PostHog for the user
3. Log the enrollment in Attio: set `advocacy_tier`, `advocacy_enrolled_date`

**Human action required:** The first 5-10 invitations should be sent personally by a founder or product lead. Observe responses. Adjust messaging before sending the remaining invitations.

### 5. Activate the first advocacy actions

For each enrolled advocate, send a specific ask within 3 days of enrollment:

- Insiders: "What is your favorite feature? Reply in one sentence." (lowest-friction ask)
- Advocates: "Would you share a short testimonial about your experience?" (include a pre-filled template with their usage data)
- Ambassadors: "We would love to feature your story. Can we schedule a 15-minute case study interview?"

Track which asks get responses. Log every `advocacy_action_completed` event.

### 6. Evaluate against threshold

Run the `threshold-engine` drill to measure results:

- **Pass**: >= 15 enrolled advocates AND >= 1 advocacy action completed across the cohort
- **Marginal pass**: 10-14 enrolled advocates with actions. Stay at Smoke, send a second batch of invitations.
- **Fail**: < 10 enrolled advocates OR 0 actions completed. Diagnose: was the candidate pool too small (scoring issue), the invitation ignored (messaging issue), or the ask too hard (program design issue)?

If PASS, document which tier/ask combinations worked best and proceed to Baseline.

## Time Estimate

- 1.5 hours: power user scoring pipeline setup and calibration
- 1 hour: advocacy program design and specification
- 0.5 hours: PostHog event instrumentation
- 1 hour: manual recruitment (30 invitations)
- 0.5 hours: follow-up asks and action tracking
- 0.5 hours: threshold evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Power user scoring, cohorts, event tracking, feature flags | Free tier: 1M events + 1M feature flag requests/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | CRM for advocate records, lists, scoring attributes | Standard stack |
| Loops | Enrollment emails, welcome sequences | Free up to 1,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | In-app enrollment messages | Standard stack |
| n8n | Automation orchestration | Standard stack |

**Estimated monthly cost: Free** (all within free tiers at Smoke volume)

## Drills Referenced

- `power-user-scoring` — compute composite scores and create tiered cohorts in PostHog/Attio
- `advocacy-program-design` — produce the full program spec: tiers, benefits, asks, event schema, message templates
- `threshold-engine` — evaluate pass/fail against the >=15 advocates threshold
