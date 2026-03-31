---
name: refer-a-friend-incentive-smoke
description: >
  Referral Rewards Program — Smoke Test. Design a two-sided referral incentive,
  manually recruit 10-20 promoters to share referral links, and validate that at
  least 8% of prompted users share their link and at least one referred user activates.
stage: "Product > Referrals"
motion: "Lead Capture Surface"
channels: "Product, Email"
level: "Smoke Test"
time: "5 hours over 1 week"
outcome: ">=8% of prompted users share their referral link AND >=1 referred user activates"
kpis: ["Referral share rate", "Referral link click-through rate", "Referred signup count", "Referred activation count", "Reward cost per activated referral"]
slug: "refer-a-friend-incentive"
install: "npx gtm-skills add product/referrals/refer-a-friend-incentive"
drills:
  - referral-program
  - threshold-engine
---

# Referral Rewards Program — Smoke Test

> **Stage:** Product → Referrals | **Motion:** Lead Capture Surface | **Channels:** Product, Email

## Outcomes

Design the referral incentive structure, manually identify 10-20 promoters from usage data, equip them with referral links, and validate that at least 8% of prompted users share their link and at least one referred user signs up and activates. This proves that your happiest users will refer when given a frictionless mechanism and a clear reward.

## Leading Indicators

- Promoter list produces 10+ users who are genuinely active and satisfied (you recognize their names, they use advanced features)
- At least 50% of outreach emails are opened
- At least 3 users click the referral link generation CTA
- At least 2 referral links are shared to someone outside the product
- At least 1 referred person clicks a referral link and lands on the signup page

## Instructions

### 1. Design the referral incentive

Run the `referral-program` drill (steps 1-2) to design the incentive structure:

- Choose a two-sided reward: both referrer and referee get a benefit. Example: "Give a friend 1 month free, get 1 month free." Two-sided rewards outperform one-sided by 2-3x in referral share rate.
- Define the activation criteria for reward issuance: the referee must complete the product activation milestone (not just sign up). This prevents gaming.
- Write the incentive as a single sentence a user can repeat to a friend: "[Product] — refer a friend and you both get [reward]."
- Generate unique referral links or codes for each user. At Smoke level, this can be as simple as UTM-tagged links with the referrer's user ID: `https://yourproduct.com/?ref={user_id}`.

**Human action required:** Decide on the reward type (credit, free month, feature unlock) and confirm the product can fulfill it. If the reward requires engineering work (applying credits to accounts), build the minimum version before proceeding.

### 2. Identify your seed referrers

Run the `referral-program` drill (step 3) to identify 10-20 seed referrers:

- Query PostHog for users who are: active in the last 14 days, have been on the product for 30+ days, and use 3+ features regularly
- Cross-reference with NPS data if available: target promoters (score 9-10)
- Cross-reference with Attio: exclude users with open support tickets or recent negative interactions
- Build an Attio list: "Referral Smoke Test — Seed Referrers"

Do not blast the referral program to all users. Start with users who already love the product. They convert at higher rates and generate higher-quality referrals.

### 3. Send personal referral asks

For each seed referrer, send a personal email (not automated) from a real person on the team:

- Acknowledge their specific usage: "I noticed you've been using [specific feature] consistently — thanks for being a power user."
- Explain the referral reward in one sentence
- Include their unique referral link
- Make sharing frictionless: provide a pre-written message they can forward, tweet, or paste into Slack

**Human action required:** Write and send 10-20 personal emails. Log each send in Attio with the date and referral link.

### 4. Track referral activity

Instrument the referral funnel in PostHog using the `referral-program` drill (step 2):

- `referral_link_shared` — referrer clicked the share/copy button or forwarded the email
- `referral_link_clicked` — someone clicked a referral link
- `referral_signup` — a new user signed up via a referral link
- `referral_activated` — the referred user hit the activation milestone

At Smoke level, some of this tracking may be manual (checking UTM parameters in PostHog, confirming activations by hand). That is acceptable. The goal is signal, not automation.

### 5. Evaluate against threshold

Run the `threshold-engine` drill after 7 days:

- **Primary threshold**: >=8% of prompted users shared their referral link (e.g., 2+ out of 20)
- **Secondary threshold**: >=1 referred user activated
- If PASS on both: the incentive structure works and your users will refer. Proceed to Baseline.
- If PASS on primary but FAIL on secondary: users are sharing but referrals are not converting. The referee landing experience or the reward framing needs work. Iterate on the referee side and re-run.
- If FAIL on primary: users are not sharing. Test a different incentive (higher value, different reward type) or different trigger timing. Re-run with a new cohort.

Document: which users shared, what channels they used to share (email, social, direct message), and what the referred users said or did.

## Time Estimate

- 1 hour: design the incentive structure and generate referral links
- 1 hour: identify and validate 10-20 seed referrers from PostHog + Attio data
- 1 hour: write and send personal referral ask emails
- 0.5 hours: set up PostHog tracking for referral events
- 1.5 hours: 7-day monitoring and final threshold evaluation

## Tools & Pricing

| Tool | Purpose | Pricing |
|------|---------|---------|
| PostHog | Track referral events, identify promoters by usage | Free tier: 1M events/mo ([posthog.com/pricing](https://posthog.com/pricing)) |
| Attio | Store seed referrer list, log outreach | Free tier: 3 seats ([attio.com/pricing](https://attio.com/pricing)) |

**Estimated play-specific cost at this level:** Free (manual outreach to 10-20 users, within free tiers)

## Drills Referenced

- `referral-program` — designs the incentive structure, builds the referral mechanism, identifies seed referrers, and instruments the referral funnel
- `threshold-engine` — evaluates the pass/fail threshold and recommends next action (advance, iterate, or pivot)
