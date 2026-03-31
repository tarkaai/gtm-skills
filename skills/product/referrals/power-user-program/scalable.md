---
name: power-user-program-scalable
description: >
  Power User Program — Scalable Automation. Find the 10x multiplier for advocacy
  output: A/B test program mechanics, integrate referral rewards with usage milestones,
  expand to multi-channel advocacy, and build the self-reinforcing flywheel where
  advocacy actions feed back into product growth.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Scalable Automation"
time: "60 hours over 2 months"
outcome: ">=50 active advocates producing >=3 advocacy actions per quarter each, with referral conversion rate >=25%"
kpis: ["Active advocate count", "Advocacy actions per advocate per quarter", "Referral conversion rate (submitted -> activated)", "Revenue attributed to advocacy referrals", "Insider-to-Advocate promotion rate"]
slug: "power-user-program"
install: "npx gtm-skills add product/referrals/power-user-program"
drills:
  - ab-test-orchestrator
  - usage-milestone-rewards
  - referral-program
  - nps-feedback-loop
---

# Power User Program — Scalable Automation

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

The advocacy program scales from early adopters to a self-sustaining flywheel. At least 50 active advocates each produce 3+ advocacy actions per quarter (referrals, testimonials, reviews, case studies, social posts). Referral conversion rate (submitted to activated) reaches 25%+. The program generates measurable revenue attribution without proportional manual effort.

## Leading Indicators

- A/B tests on advocacy mechanics produce statistically significant winners within 2-week cycles
- Usage milestone moments convert to referral prompts at >=15% rate
- NPS promoters (9-10) are being automatically enrolled in the advocacy program at >=80% capture rate
- Advocate-to-Ambassador promotion pipeline is healthy (>=5 new Ambassadors per quarter)
- Social sharing events increasing month over month
- Cost per advocacy-referred customer is <=50% of paid acquisition cost

## Instructions

### 1. A/B test advocacy program mechanics

Run the `ab-test-orchestrator` drill to systematically test and optimize each component of the program:

**Test 1 — Enrollment messaging:**
- Control: current Intercom enrollment celebration message
- Variant A: emphasize exclusive access ("You've unlocked early access to features before anyone else")
- Variant B: emphasize community ("Join 47 other power users shaping the product roadmap")
- Metric: enrollment celebration click-through rate
- Duration: 2 weeks or 100+ users per variant

**Test 2 — First-action ask:**
- Control: testimonial request ("Share what you love about [Product] in one sentence")
- Variant A: referral request ("Know someone who'd benefit? Share your invite link")
- Variant B: public review request ("Leave a quick review on G2/Capterra")
- Metric: first-action completion rate within 14 days
- Duration: 2 weeks or 50+ users per variant

**Test 3 — Referral incentive:**
- Control: current reward (account credit or feature unlock)
- Variant A: two-sided reward (referrer and referee both get a benefit)
- Variant B: tiered reward (escalating rewards at 1, 3, 5 referrals)
- Metric: referrals submitted per advocate per quarter
- Duration: 4 weeks or 30+ referrals per variant

**Test 4 — Nudge timing:**
- Control: first nudge at Day 7 after enrollment
- Variant A: first nudge at Day 3 (strike while excitement is fresh)
- Variant B: first nudge triggered by a product success moment (after completing a workflow) instead of time-based
- Metric: first-action completion rate within 30 days
- Duration: 3 weeks or 50+ users per variant

Implement winners immediately. Log each test result in Attio with the hypothesis, variants, sample sizes, results, and decision.

### 2. Integrate advocacy with usage milestones

Run the `usage-milestone-rewards` drill to connect advocacy asks to moments of product delight:

- Configure milestone detection in PostHog: first project completed, 10th collaboration, 100th workflow run, team reaching 5 members
- At each milestone, the celebration message includes a secondary advocacy CTA:
  - Early milestones: "You're on a roll — know someone who'd love this?" (referral link)
  - Mid milestones: "You've accomplished a lot — mind sharing a quick review?" (review link)
  - Advanced milestones: "You're one of our most accomplished users — would you tell your story?" (case study invitation)
- Track conversion rates from milestone celebrations to advocacy actions in PostHog
- The milestone CTA should never overshadow the celebration. Primary message is congratulations; advocacy ask is secondary.

### 3. Expand the referral engine

Run the `referral-program` drill to build a robust referral mechanism that integrates with the advocacy tiers:

- Generate unique referral links per advocate with PostHog tracking: link shared, link clicked, referee signed up, referee activated, reward unlocked
- Implement tier-based referral rewards: Insider gets standard reward, Advocate gets 2x, Ambassador gets 3x
- Build the referral dashboard: links shared, click-through rate, signup rate, activation rate, revenue per referral
- Automate reward delivery end-to-end: detect activation threshold, issue credit/unlock, notify referrer
- Create referral leaderboard visible in the advocacy community channel: top referrers this month with anonymized counts

### 4. Capture NPS promoters into the advocacy pipeline

Run the `nps-feedback-loop` drill to systematically route promoters into the advocacy program:

- Configure NPS survey triggers at key moments: after 30 days active use, after milestone achievements, quarterly for long-term users
- Route promoters (9-10 score) directly into the advocacy enrollment pipeline:
  - If already enrolled: thank them and prompt the next advocacy action
  - If not yet enrolled but score >= 60: fast-track enrollment with a warm message referencing their positive NPS response
  - If not yet enrolled and score < 60: add to the Rising Star nurture sequence
- Route detractors (0-6) away from advocacy asks and toward support. Do not ask unhappy users to refer.
- Track NPS-to-advocacy conversion: what percentage of promoters complete an advocacy action within 30 days of their NPS response?

### 5. Build the scalable reporting layer

Create a weekly advocacy program report that runs automatically:

- **Enrollment pipeline**: eligible pool size, new enrollments, enrollment rate trend
- **Activation metrics**: first-action rate by cohort, time-to-first-action median, activation rate by advocacy action type
- **Referral engine**: referrals submitted, conversion funnel, revenue attributed, cost per referred customer vs. other channels
- **Program health**: tier distribution, promotion rates, advocate retention, inactive rate
- **Experiment log**: active tests, completed tests this month, cumulative improvement from winning variants
- **Top advocates**: leaderboard by total advocacy actions and referral conversions

Post to Slack weekly. Store in Attio.

### 6. Evaluate against threshold

After 2 months, measure:

- **Active advocate count**: users with >=1 advocacy action in the last 90 days. Target: >=50.
- **Advocacy actions per advocate per quarter**: total actions / active advocates. Target: >=3.
- **Referral conversion rate**: activated referrals / submitted referrals. Target: >=25%.

If PASS: the program is self-sustaining and producing scalable advocacy output. Proceed to Durable.
If FAIL on advocate count: the scoring model or enrollment pipeline is too narrow. Consider lowering the Insider threshold or expanding eligible actions.
If FAIL on actions per advocate: advocates are not being activated repeatedly. Test new asks, increase reward value, or add gamification.
If FAIL on referral conversion: the referral mechanism is broken. Check the referral landing page, the incentive, and the referee onboarding experience.

## Time Estimate

- 15 hours: A/B test design, implementation, and evaluation (4 tests over 2 months)
- 10 hours: usage milestone integration and configuration
- 10 hours: referral engine build-out and reward automation
- 8 hours: NPS promoter routing and integration
- 10 hours: reporting layer and weekly report automation
- 7 hours: 2-month monitoring and final evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Experiments, feature flags, funnels, cohorts, dashboards, milestone tracking | Usage-based: ~$0.00005/event beyond 1M free/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Intercom | In-app messages, enrollment celebrations, milestone CTAs, nudges | Essential $29/seat/mo + Proactive Support add-on $99/mo ([intercom.com/pricing](https://intercom.com/pricing)) |
| Loops | Advocacy sequences, referral notifications, NPS follow-ups | Starter $49/mo up to 5,000 contacts ([loops.so/pricing](https://loops.so/pricing)) |
| n8n | All automation workflows: enrollment, nudges, referral tracking, reporting | Self-hosted: free; Cloud: from $24/mo ([n8n.io/pricing](https://n8n.io/pricing)) |
| Attio | Advocate records, referral tracking, experiment logs, report storage | Pro: $34/seat/mo ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** $150-350/mo (Intercom Proactive Support is the main driver; Loops and Attio Pro for scale)

## Drills Referenced

- `ab-test-orchestrator` — systematic A/B testing of advocacy program mechanics with PostHog experiments
- `usage-milestone-rewards` — connects advocacy asks to moments of product delight at usage milestones
- `referral-program` — builds the full referral mechanism with tracking, rewards, and leaderboard
- `nps-feedback-loop` — captures NPS promoters and routes them into the advocacy enrollment pipeline
