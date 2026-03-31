---
name: refer-a-friend-incentive-scalable
description: >
  Referral Rewards Program — Scalable Automation. Segment users by referral propensity,
  personalize incentives per segment, A/B test variants, and scale to 500+ eligible
  users while maintaining >=10% referral rate with a viral coefficient >=0.2.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "40 hours over 2 months"
outcome: ">=10% referral rate at 500+ eligible users AND viral coefficient >=0.2"
kpis: ["Referral rate by segment", "Viral coefficient", "Referred user activation rate", "Reward cost per acquisition", "Referral channel mix", "Segment-level conversion rates"]
slug: "refer-a-friend-incentive"
install: "npx gtm-skills add product/referrals/refer-a-friend-incentive"
drills:
  - referral-segment-scaling
  - ab-test-orchestrator
---

# Referral Rewards Program — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Expand the referral program from a single incentive for all users to segment-specific incentive variants (power users, price-sensitive, team leads, new enthusiasts, long-tenured quiet). A/B test each variant against the baseline. Scale to 500+ eligible users across all segments while maintaining >=10% referral rate and achieving a viral coefficient >=0.2 (each 10 users generate 2+ new activated users through referrals).

## Leading Indicators

- At least 3 of 5 segments have 100+ eligible users (sufficient for testing)
- Segment-specific prompts show higher click rates than the generic prompt in at least 2 segments within the first 2 weeks
- A/B tests reach statistical significance within 4 weeks for at least 2 segments
- Viral coefficient trends upward week over week for the first month
- Reward cost per acquisition via referral is lower than the next-best acquisition channel
- Top 10% of referrers account for 30%+ of all referrals (power law distribution confirming the program rewards the right behavior)

## Instructions

### 1. Build referral segments and personalized variants

Run the `referral-segment-scaling` drill to:

- Create 5 PostHog cohorts based on referral propensity signals: Power Users (top 20% by usage), Price Sensitive (free plan or downgraded), Team Leads (invited 2+ members), New Enthusiasts (first 30 days, fast activators), Long-tenured Quiet (6+ months, moderate usage, never referred)
- Design segment-specific incentive copy and reward framing for each cohort
- Implement PostHog feature flag `referral-incentive-variant` that routes each user to their segment-appropriate incentive
- Create 5 Intercom in-app message variants, each targeted to its segment with segment-appropriate trigger timing
- Create 5 Loops email sequence variants with segment-appropriate copy

### 2. Run segment A/B tests

Run the `ab-test-orchestrator` drill for each segment:

- Create 5 PostHog experiments (one per segment): control = baseline (generic) incentive, treatment = segment-specific incentive
- Allocate 50/50 within each segment
- Primary metric: `referral_link_shared` rate within 14 days of prompt
- Secondary metrics: `referral_signup` conversion, `referral_activated` conversion, reward cost per acquisition
- Minimum sample size: 100 users per variant per segment
- Maximum test duration: 4 weeks per segment. If sample size is not reached in 4 weeks, extend to 6 weeks or merge smaller segments.

Run tests in parallel across segments. Monitor weekly using the `ab-test-orchestrator` guardrails:
- If any variant's referral rate drops below 5% (vs. 10%+ baseline), pause that segment's test and revert to control
- If reward cost per acquisition exceeds 2x the baseline for any variant, flag for review

### 3. Roll out winning variants

For each segment experiment that reaches significance:

- If the segment variant wins (>=2pp improvement in referral rate at 95% confidence): roll out to 100% of that segment. Update the feature flag.
- If no significant difference: keep the baseline variant (simpler to maintain)
- If the segment variant loses: log the result, generate a new hypothesis for that segment, and queue a second test

After all segments have been tested, calculate the blended referral rate across all segments. The personalized program should outperform the single-incentive baseline by at least 20% in aggregate referral rate.

### 4. Scale monitoring and viral coefficient tracking

Using the `referral-segment-scaling` drill's weekly report workflow:

- Track referral rate, conversion rate, reward cost, and viral coefficient per segment weekly
- Calculate overall viral coefficient: (average referrals per eligible user) * (share-to-activation conversion rate). Target: >=0.2.
- Monitor for segment saturation: if a segment's referral rate declines 3 weeks in a row, the segment may be exhausted. Investigate whether the pool refreshes fast enough or whether the segment definition needs updating.
- Track referral channel mix (email, social, direct link, in-app) per segment. Optimize prompt placement and share mechanics for the dominant channel per segment.

### 5. Evaluate against threshold

After 2 months:

- **Primary threshold**: >=10% referral rate across 500+ eligible users
- **Secondary threshold**: viral coefficient >=0.2
- **Guardrail**: reward cost per acquisition via referral is <= cost from the next-best acquisition channel
- If PASS: the referral program scales profitably across segments. Proceed to Durable.
- If primary PASS but viral coefficient <0.2: users are sharing but referrals are not converting. Focus optimization on the referee experience (landing page, onboarding for referred users, reward visibility).
- If primary FAIL: identify which segments underperform. Either the incentive does not resonate (test alternatives) or the segment is too small (merge segments or adjust definitions).

## Time Estimate

- 8 hours: build 5 referral segments, design variants, configure feature flags and Intercom/Loops variants
- 12 hours: set up and launch 5 A/B tests, monitor for 4 weeks
- 8 hours: analyze results, roll out winners, iterate on losing segments
- 8 hours: weekly monitoring, viral coefficient tracking, cross-segment reporting over 2 months
- 4 hours: final evaluation and documentation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Cohorts, feature flags, A/B experiments, funnel analysis | Free tier: 1M events/mo; experiments included ([posthog.com/pricing](https://posthog.com/pricing)) |
| Loops | 5 segment-specific email sequences, A/B testing | $49/mo for up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| Intercom | 5 segment-specific in-app prompts | Essential: $29/seat/mo annual ([intercom.com/pricing](https://www.intercom.com/pricing)) |
| Attio | Segment data, referrer leaderboard, reporting | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $50-130/mo (Loops $49/mo + Intercom $29/seat/mo if not already on standard stack; PostHog and Attio within free tiers at this volume)

## Drills Referenced

- `referral-segment-scaling` — builds the 5 referral segments, designs personalized variants, implements feature flag routing, runs segment experiments, and generates weekly cross-segment reports
- `ab-test-orchestrator` — structures hypotheses, calculates sample sizes, manages experiment lifecycle, and evaluates results with statistical rigor
