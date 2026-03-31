---
name: community-champions-scalable
description: >
  Champion Recognition Program — Scalable Automation. Find the 10x multiplier
  for champion-driven referrals: A/B test recognition mechanics, launch
  co-marketing with top champions, expand the referral engine with tiered
  rewards, and build the self-reinforcing loop where recognition drives referrals
  and referrals surface new champions.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email, Social"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=30 active champion referrers producing >=2 referrals per quarter each, with referral conversion rate >=20%"
kpis: ["Active champion referrer count", "Referrals per champion per quarter", "Referral conversion rate (submitted -> activated)", "Revenue attributed to champion referrals", "Co-marketing content pieces published"]
slug: "community-champions"
install: "npx gtm-skills add product/referrals/community-champions"
drills:
  - ab-test-orchestrator
  - referral-program
---

# Champion Recognition Program — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email, Social

## Outcomes

The champion recognition program scales from early adopters to a self-sustaining referral and co-marketing engine. At least 30 active champion referrers each produce 2+ referrals per quarter. Referral conversion rate (link clicked to activated user) reaches 20%+. Co-marketing with top champions (guest posts, social amplification, community events) generates measurable signups without proportional manual effort.

## Leading Indicators

- A/B tests on recognition mechanics produce statistically significant winners within 2-week cycles
- Community channel champion celebrations receive increasing engagement (reactions, congratulations) month over month
- Co-marketing invitations are accepted at >=40% rate
- Social amplification kits are used by >=50% of recipients
- Champion-to-Recognized Contributor promotion pipeline is healthy (>=5 new Champions per quarter)
- Cost per champion-referred customer is <=50% of paid acquisition cost

## Instructions

### 1. A/B test champion recognition mechanics

Run the `ab-test-orchestrator` drill to systematically test and optimize each component of the program:

**Test 1 — Enrollment recognition messaging:**
- Control: current Intercom enrollment message ("Your contributions are making a difference")
- Variant A: community impact stats ("You've helped 23 people this month — that puts you in the top 5%")
- Variant B: peer recognition ("4 community members tagged you for help this month")
- Metric: enrollment celebration click-through rate
- Duration: 2 weeks or 50+ enrollments per variant

**Test 2 — Referral activation ask:**
- Control: generic referral link with standard CTA ("Share your invite link")
- Variant A: impact-framed ask ("Help someone else the way you help the community — share your invite")
- Variant B: social proof ask ("12 other champions shared their link this month — join them")
- Metric: referral link share rate within 14 days of receiving the ask
- Duration: 3 weeks or 40+ champions per variant

**Test 3 — Referral incentive structure:**
- Control: current reward (product credit for referrer)
- Variant A: two-sided reward (referrer and referee both get a benefit)
- Variant B: tiered reward (escalating rewards at 1, 3, 5 referrals with public leaderboard)
- Metric: referrals submitted per champion per quarter
- Duration: 4 weeks or 20+ referrals per variant

**Test 4 — Community celebration format:**
- Control: text-only bot message in community channel
- Variant A: message with the champion's contribution stats and a highlight quote from a user they helped
- Variant B: monthly champion spotlight thread featuring the top 3 champions with their stories
- Metric: community engagement rate (reactions + replies to celebration posts)
- Duration: 4 weeks (2 cycles per variant)

Implement winners immediately. Log each test result in Attio with the hypothesis, variants, sample sizes, results, and decision.

### 2. Expand the referral engine with tiered rewards

Run the `referral-program` drill to build a robust referral mechanism integrated with the champion tiers:

- Generate unique referral links per champion with PostHog tracking: link shared, link clicked, referee signed up, referee activated, reward unlocked
- Implement tier-based referral rewards:
  - Recognized Contributor: standard reward (e.g., 1 month free feature access)
  - Champion: 2x reward + public recognition in community channel
  - Top Referrer bonus: champions in the top 5 referrers per quarter get an additional reward (advisory board seat, product feature request priority, swag)
- Build the referral dashboard: links shared, click-through rate, signup rate, activation rate, revenue per referral, cost per referred customer vs other channels
- Automate reward delivery end-to-end: detect activation threshold, issue credit/unlock feature, notify champion, post in community channel
- Create a referral leaderboard visible in the community: top referrers this month with anonymized or opted-in counts

### 3. Launch co-marketing with top champions

Run the the champion co marketing pipeline workflow (see instructions below) drill to scale co-marketing without proportional effort:

- Build the opportunity matching engine: match champions to co-marketing activities based on their dimension scores (high content creators get blog invitations, high-reach champions get social amplification kits, high-helpfulness champions get webinar co-host invitations)
- Configure the monthly co-marketing cadence: automated opportunity matching, invitation emails via Loops, response tracking in Attio, burnout guardrails (max 1 ask per champion per month)
- Deploy biweekly social amplification kits: pre-written social posts with each champion's referral link embedded, sent via Loops with a "copy and post" CTA
- Track co-marketing content performance end-to-end: published -> viewed -> engaged -> CTA clicked -> signed up -> activated
- Enforce relationship guardrails: maximum ask frequency, cool-down after completion, decline tracking, gratitude loops with impact stats after every completed activity

### 4. Build the scalable reporting layer

Create a weekly champion program report that runs automatically via n8n:

- **Recognition pipeline**: eligible pool size, new enrollments, enrollment rate trend, tier distribution
- **Referral engine**: links shared, referral funnel metrics, revenue attributed, cost per referred customer vs other channels
- **Co-marketing output**: invitations sent, accepted, published, content performance by type
- **Community impact**: total questions answered by champions, total users helped, champion contribution as % of total community activity
- **Experiment log**: active tests, completed tests this month, cumulative improvement from winning variants
- **Top champions**: leaderboard by total referrals + co-marketing activities

Post to Slack weekly. Store in Attio.

### 5. Evaluate against threshold

After 2 months, measure:

- **Active champion referrer count**: champions with >=1 referral link share in the last 90 days. Target: >=30.
- **Referrals per champion per quarter**: total referrals / active champion referrers. Target: >=2.
- **Referral conversion rate**: activated referrals / referral link clicks. Target: >=20%.

If PASS: the program is self-sustaining and producing scalable champion-driven growth. Proceed to Durable.
If FAIL on champion referrer count: the recognition-to-referral pipeline is too narrow. Consider lowering the Champion threshold, improving the referral ask, or adding more compelling incentives.
If FAIL on referrals per champion: champions are sharing once but not repeatedly. Test gamification (leaderboard, streaks), refresh the social amplification kits more frequently, or introduce seasonal referral campaigns.
If FAIL on referral conversion: the referral landing page, onboarding for referred users, or incentive for the referee is broken. Test the referee experience independently.

## Time Estimate

- 15 hours: A/B test design, implementation, and evaluation (4 tests over 2 months)
- 12 hours: referral engine build-out with tiered rewards and leaderboard
- 15 hours: co-marketing pipeline setup, opportunity matching, social amplification kits
- 10 hours: reporting layer and weekly report automation
- 8 hours: 2-month monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards, referral tracking | Usage-based: ~$0.00005/event beyond 1M free/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app recognition messages, referral nudges, champion celebrations | Essential $29/seat/mo + Proactive Support Plus $99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Recognition sequences, referral notifications, social amplification kits, co-marketing invitations | Starter $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | All automation: scoring, enrollment, referral tracking, co-marketing cadence, reporting | Self-hosted: free; Cloud: from $20/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Champion records, referral tracking, co-marketing logs, experiment logs | Plus: $36/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $150-350/mo (Intercom Proactive Support Plus is the main driver; Loops and Attio Plus for scale)

## Drills Referenced

- `ab-test-orchestrator` — systematic A/B testing of recognition mechanics, referral asks, incentive structures, and celebration formats with PostHog experiments
- `referral-program` — builds the full referral mechanism with tracking, tier-based rewards, leaderboard, and automated reward delivery
- the champion co marketing pipeline workflow (see instructions below) — scales co-marketing with opportunity matching, social amplification kits, content tracking, and relationship lifecycle management
